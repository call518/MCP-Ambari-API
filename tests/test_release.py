"""Verify release validation and publication without Git or network writes."""

import io
import json
import tarfile
import tempfile
import unittest
import zipfile
from pathlib import Path
from unittest.mock import patch

from scripts.check_release import check_release, release_version
from scripts.publish_release import publish_release, release_notes


class ReleaseTests(unittest.TestCase):
    def test_release_tags(self):
        for tag in ("3.7.9", "0.1.0", "10.20.30"):
            self.assertEqual(release_version(tag), tag)
        for tag in (
            "main", "3.7", "3.07.9", "3.7.9; echo unsafe", "v3.7.9",
            "3.8.0a1", "3.8.0b1", "3.8.0rc1", "3.8.0.post1",
        ):
            with self.assertRaises(ValueError):
                release_version(tag)

    def test_distribution_metadata(self):
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            metadata = b"Name: mcp-ambari-api\nVersion: 3.7.9\n"
            with zipfile.ZipFile(directory / "package.whl", "w") as archive:
                archive.writestr("package.dist-info/METADATA", metadata)
            with tarfile.open(directory / "package.tar.gz", "w:gz") as archive:
                info = tarfile.TarInfo("package/PKG-INFO")
                info.size = len(metadata)
                archive.addfile(info, io.BytesIO(metadata))
            check_release("3.7.9", directory)
            with self.assertRaises(ValueError):
                check_release("3.8.0", directory)

    @patch("scripts.publish_release.command")
    def test_notes_include_full_messages_and_previous_release_range(self, command):
        command.side_effect = [
            "current", "previous", "",
            "abcdef123\0Fix issue\n\nDetails with ``` and $(echo unsafe)\n\0\n",
        ]
        notes = release_notes("owner/repo", "3.7.9", "3.7.8")
        self.assertIn("Details with ``` and $(echo unsafe)", notes)
        self.assertIn("````text", notes)
        self.assertIn("compare/3.7.8...3.7.9", notes)
        self.assertEqual(command.call_args.args[-2], "previous..current")

    @patch("scripts.publish_release.command")
    def test_initial_release_notes(self, command):
        command.side_effect = ["current", "abcdef123\0Initial commit\0"]
        self.assertIn("Initial release.", release_notes("owner/repo", "1.0.0", None))

    @patch("scripts.publish_release.command")
    def test_existing_release_is_unchanged(self, command):
        command.side_effect = [
            "sha", "sha", "sha",
            json.dumps([[{"tag_name": "3.7.9", "draft": False}]]),
        ]
        publish_release("owner/repo", "3.7.9")
        self.assertEqual(command.call_count, 4)

    @patch("scripts.publish_release.command")
    def test_mismatched_tag_stops_publication(self, command):
        command.side_effect = ["local", "remote"]
        with self.assertRaises(ValueError):
            publish_release("owner/repo", "3.7.9")

    @patch("scripts.publish_release.release_notes", return_value="notes\n")
    @patch("scripts.publish_release.command")
    def test_publish_uses_last_published_release(
        self, command, notes
    ):
        command.side_effect = [
            "sha", "sha", "sha",
            json.dumps([[
                {"tag_name": "3.7.8", "draft": False, "published_at": "2026-10-01"},
                {"tag_name": "3.7.9", "draft": False, "published_at": "2026-10-02"},
                {"tag_name": "future", "draft": True, "published_at": None},
            ]]),
            "",
        ]
        publish_release("owner/repo", "3.8.0")
        notes.assert_called_once_with("owner/repo", "3.8.0", "3.7.9")
        args = command.call_args.args
        self.assertEqual(args[:3], ("gh", "release", "create"))
        self.assertIn("--notes-file", args)
        self.assertNotIn("--prerelease", args)

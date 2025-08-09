import re
from mcp_ambari_api import get_prompt_template
import asyncio


def test_full_template_loads():
    txt = asyncio.run(get_prompt_template())
    assert 'Purpose' in txt and 'Tool Map' in txt


def test_headings_mode():
    headings = asyncio.run(get_prompt_template(mode='headings'))
    assert 'Section Headings:' in headings
    assert 'Purpose' in headings


def test_section_fetch_by_number():
    sec = asyncio.run(get_prompt_template('3'))  # Tool Map
    assert 'Tool Map' in sec
    assert '| get_cluster_info' in sec


def test_section_fetch_by_keyword():
    sec = asyncio.run(get_prompt_template('decision flow'))
    assert 'Decision Flow' in sec
    # Decision flow lists references like get_cluster_services / get_service_status etc.
    assert 'get_cluster_services' in sec and 'get_service_status' in sec


def test_section_no_arg_help_format_matches_headings():
    """Simulate logic used when prompt_template_section is called without arg: ensure headings block present multi-line."""
    headings = asyncio.run(get_prompt_template(mode='headings'))
    # Expect the headings list first line marker and at least two numbered lines
    assert 'Section Headings:' in headings
    numbered_lines = [ln for ln in headings.splitlines() if ln.strip().startswith('1.')]
    assert numbered_lines, 'Expected at least one numbered heading line'


# New tests for unified configuration tool reference in template (string-level only; functional tests would require Ambari fixture)
def test_template_references_dump_configurations_only():
    txt = asyncio.run(get_prompt_template())
    assert 'dump_configurations' in txt
    assert 'get_configurations' not in txt
    assert 'list_configurations' not in txt
    assert 'dump_all_configurations' not in txt

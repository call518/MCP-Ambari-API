#!/usr/bin/env bash
set -euo pipefail

if [[ $# -ne 2 ]]; then
  echo "Usage: $0 <X.Y.Z version> <output-directory>" >&2
  exit 2
fi

version=$1
output_dir=$2
if [[ ! $version =~ ^(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)$ ]]; then
  echo "Version must use canonical X.Y.Z format" >&2
  exit 2
fi

repo_dir=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
stage=$(mktemp -d)
trap 'rm -rf "$stage"' EXIT

mkdir -p "$stage/src/mcp_ambari_api" "$output_dir"
cp "$repo_dir/mcpb/server.py" "$stage/server.py"
cp "$repo_dir/pyproject.toml" "$repo_dir/uv.lock" "$stage/"
cp "$repo_dir/README.md" "$repo_dir/LICENSE" "$stage/"
cp "$repo_dir/img/icon-ambari.png" "$stage/icon.png"
cp "$repo_dir/src/mcp_ambari_api/__init__.py" \
  "$repo_dir/src/mcp_ambari_api/__main__.py" \
  "$repo_dir/src/mcp_ambari_api/functions.py" \
  "$repo_dir/src/mcp_ambari_api/mcp_main.py" \
  "$repo_dir/src/mcp_ambari_api/server_instructions.md" \
  "$stage/src/mcp_ambari_api/"
sed -e "s/\"version\": \"0.0.0\"/\"version\": \"$version\"/" \
  -e "s/\"SETUPTOOLS_SCM_PRETEND_VERSION\": \"0.0.0\"/\"SETUPTOOLS_SCM_PRETEND_VERSION\": \"$version\"/" \
  "$repo_dir/mcpb/manifest.json" > "$stage/manifest.json"

cli=${MCPB_CLI:-@anthropic-ai/mcpb@2.1.2}
npx -y "$cli" validate "$stage/manifest.json"
npx -y "$cli" pack "$stage" "$output_dir/mcp-ambari-api-$version.mcpb"

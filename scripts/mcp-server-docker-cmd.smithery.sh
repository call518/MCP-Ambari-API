#!/bin/bash
set -euo pipefail

echo "Starting MCP server with:"
echo "  PYTHONPATH: ${PYTHONPATH}"

python -m mcp_ambari_api.ambari_api --type stdio

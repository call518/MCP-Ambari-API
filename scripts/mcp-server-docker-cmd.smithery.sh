#!/bin/bash
set -euo pipefail

echo "Starting MCP server with:"
echo "  PYTHONPATH: ${PYTHONPATH}"
echo "  AMBARI_HOST: ${AMBARI_HOST}"
echo "  AMBARI_PORT: ${AMBARI_PORT}"

python -m mcp_ambari_api.ambari_api --type ${FASTMCP_TYPE} --host ${FASTMCP_HOST} --port ${FASTMCP_PORT}

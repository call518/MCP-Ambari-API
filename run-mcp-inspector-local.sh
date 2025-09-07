#!/bin/bash
set -euo pipefail

# Get the directory where this script is located and navigate to project root
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "🔍 Starting MCP Inspector with Ambari Operations server..."
echo "📁 Working directory: $(pwd)"

# Load environment variables if .env exists
if [ -f ".env" ]; then
    echo "📄 Loading environment from .env file"
    set -o allexport
    source .env
    set +o allexport
fi

echo "🚀 Launching MCP Inspector..."
echo "   Ambari Host: ${AMBARI_HOST:-localhost}:${AMBARI_PORT:-8080}"

npx -y @modelcontextprotocol/inspector \
    -e PYTHONPATH='./src' \
	  -e FASTMCP_TYPE='stdio' \
    -- uv run python -m mcp_ambari_api
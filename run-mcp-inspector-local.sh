#!/bin/bash
set -euo pipefail

# Run MCP Inspector with local source using uv
cd "$(dirname "$0")"

echo "🔍 Starting MCP Inspector with Ambari Operations server..."
echo "📁 Working directory: $(pwd)"

# Load environment variables if .env exists
if [ -f ".env" ]; then
    echo "📄 Loading environment from .env file"
    export $(cat .env | grep -v '^#' | xargs)
fi

# Set default log level for development
export MCP_LOG_LEVEL=${MCP_LOG_LEVEL:-INFO}

echo "🚀 Launching MCP Inspector..."
echo "   Log Level: $MCP_LOG_LEVEL"
echo "   Ambari Host: ${AMBARI_HOST:-localhost}:${AMBARI_PORT:-8080}"

npx -y @modelcontextprotocol/inspector \
  -- uv run python -m mcp_ambari_api.mcp_main

#!/bin/bash
set -eo pipefail

# Run MCP Inspector with published package from PyPI
cd "$(dirname "$0")/.."

echo "🔍 Starting MCP Inspector with published package..."
echo "📦 Package: mcp-ambari-api"

# Check if package name has been customized
if grep -q "mcp-ambari-api" pyproject.toml; then
    echo "⚠️  Warning: Package name 'mcp-ambari-api' hasn't been customized."
    echo "   Run ./scripts/rename-template.sh first to customize the package."
    echo ""
fi

echo "🚀 Launching MCP Inspector with uvx..."

npx -y @modelcontextprotocol/inspector \
  -- uvx mcp-ambari-api

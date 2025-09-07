"""
Entry point for running MCP Ambari API as a module.

This allows running the server with:
    python -m mcp_ambari_api

Instead of:
    python -m mcp_ambari_api.mcp_main
"""

from .mcp_main import main

if __name__ == "__main__":
    main()

"""MCPB stdio entry point."""

from mcp_ambari_api.mcp_main import main


if __name__ == "__main__":
    main(["--type", "stdio"])

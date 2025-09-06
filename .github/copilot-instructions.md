# Copilot Instructions for MCP-Ambari-API

## Architecture & Transport Selection
This MCP server supports dual transport modes with flexible configuration via CLI args and environment variables:
- **stdio mode**: Default for local usage (`uvx mcp-ambari-api`)
- **streamable-http mode**: For Docker/server deployment (`--type streamable-http` or `FASTMCP_TYPE=streamable-http`)

**Priority**: CLI args > Environment vars > Defaults. The `main()` function in `src/mcp_ambari_api/mcp_main.py` (~2181 lines) handles transport selection and runs the FastMCP server.

## Core Patterns
- **Tool Definition**: Every Ambari operation is an async function with `@mcp.tool()` + `@log_tool` decorators
- **API Abstraction**: All Ambari REST calls go through `make_ambari_request()` in `functions.py` with automatic auth, error handling, and timing
- **Environment Configuration**: Ambari connection via `AMBARI_HOST`, `AMBARI_PORT`, `AMBARI_USER`, `AMBARI_PASS`, `AMBARI_CLUSTER_NAME` env vars
- **Unified Tool Pattern**: Modern tools like `dump_configurations` replace multiple specialized tools (superseded `get_configurations`, `list_configurations`)
- **Error Handling**: Structured `{"error": "..."}` responses with HTTP status codes and timing info
- **Logging**: The `@log_tool` decorator provides uniform timing, argument preview, and result categorization (SUCCESS/ERROR/EXCEPTION)

## Development Workflows
- **Local Testing**: Use `run-mcp-inspector-local.sh` (not `scripts/`) with uv to test tools interactively
- **Docker Development**: `docker-compose up -d` starts full stack (OpenWebUI + MCP server + MCPO proxy)
- **Build & Deploy**: Version-specific Docker images via `build-mcp-server-docker-image.sh` and `build-mcpo-server-docker-image.sh`
- **Package Structure**: Entry point is `mcp-ambari-api` console script → `mcp_ambari_api.mcp_main:main`
- **Environment Setup**: Use `PYTHONPATH=./src` for local development, packaged resources in `mcp_ambari_api/prompt_template.md`

## Configuration Files
- `mcp-config.json.stdio`: Local/command-line MCP client configuration
- `mcp-config.json.http`: Docker-based MCP client configuration (uses streamable-http transport)
- `docker-compose.yml` maps `mcp-config.json.http` into MCPO proxy container

## AI Agent Integration
- **Canonical Prompt**: `src/mcp_ambari_api/prompt_template.md` contains the official system prompt with tool selection decision tree
- **Safety-First**: Bulk operations (start/stop/restart all services) require explicit user intent
- **Real Data Only**: AI agents must use tools for all cluster data—no guessing or hypothetical responses
- **Tool Mapping**: Comprehensive table maps user intents/keywords to specific tools (e.g., "services" → `get_cluster_services`)

## Error Handling & Debugging
- All tools return structured error responses with `{"error": "..."}` format
- `@log_tool` decorator provides detailed timing and categorized results in logs
- HTTP errors from Ambari API are captured and returned with status codes
- Connection failures include timing information for debugging

## Key Files to Understand
- `src/mcp_ambari_api/mcp_main.py`: Tool definitions, transport selection, main entrypoint
- `src/mcp_ambari_api/functions.py`: `make_ambari_request()`, `@log_tool` decorator, formatting utilities
- `src/mcp_ambari_api/prompt_template.md`: AI agent decision tree and tool selection guide
- `docker-compose.yml`: Multi-container orchestration with environment mapping

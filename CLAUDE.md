# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

MCP Ambari API is a Model Context Protocol (MCP) server that bridges AI/LLM agents to Apache Ambari's REST API, enabling natural-language Hadoop cluster management. Built with **FastMCP** and **aiohttp**.

## Development Commands

```bash
# Install dependencies (always use uv, never pip)
uv sync

# Run locally (stdio mode, for MCP Inspector)
PYTHONPATH=./src uv run python -m mcp_ambari_api

# Run locally (streamable-http mode)
PYTHONPATH=./src uv run python -m mcp_ambari_api --type streamable-http --host 0.0.0.0 --port 8000

# Run with .env config
source .env && PYTHONPATH=./src uv run python -m mcp_ambari_api --type ${FASTMCP_TYPE} --host ${FASTMCP_HOST} --port ${FASTMCP_PORT}

# MCP Inspector (interactive dev testing)
./run-mcp-inspector-local.sh

# Pre-commit (gitleaks secret scanning)
uv run pre-commit run --all-files

# Docker full stack (MCP server + MCPO proxy + OpenWebUI)
docker-compose up -d

# Build Docker images
./build-mcp-server-docker-image.sh
./build-mcpo-server-docker-image.sh
```

No tests or linting tools are currently configured.

## Architecture

### Two-module core design

- **`src/mcp_ambari_api/mcp_main.py`** (~3400 lines) — MCP tool/resource registration layer. Creates the `FastMCP` instance, decorates async functions with `@mcp.tool()` and `@mcp.resource()`, handles CLI argument parsing and server startup.
- **`src/mcp_ambari_api/functions.py`** (~1700 lines) — Business logic layer. HTTP request helpers (`make_ambari_request`, `make_ambari_metrics_request`), formatting utilities, metrics parsing/caching, and time-range resolution.

### Transport modes

- **stdio** — Direct pipe with LLM clients (Claude Desktop, MCP Inspector). Default for local use.
- **streamable-http** — HTTP server exposing `/mcp` endpoint. Used for Docker deployment with MCPO proxy.

### Docker stack flow

```
OpenWebUI (port 3001) → MCPO Proxy (port 8001) → MCP Server (port 18001) → Ambari REST API
```

The MCPO proxy converts MCP protocol to OpenAPI/REST, making tools accessible from OpenWebUI.

### Authentication

Optional Bearer token auth via FastMCP's `StaticTokenVerifier`. Configured via `REMOTE_AUTH_ENABLE` and `REMOTE_SECRET_KEY` environment variables or CLI flags.

### Key patterns in functions.py

- `log_tool(func)` decorator — uniform tool timing/logging for all MCP tools
- `ensure_metric_catalog(use_cache)` — builds and caches `appId → [metric_names]` map with configurable TTL
- `resolve_metrics_time_range(duration)` — converts duration strings (e.g. `"1h"`, `"30m"`) to epoch ms ranges
- In-memory metrics caching with TTL, invalidated by `refresh=True`

### MCP tools exposed

Cluster management, service lifecycle (start/stop/restart), configuration introspection, host/user management, alerting (current and historical), Ambari Metrics Service (AMS) time-series queries, and HDFS capacity reporting.

## Configuration

All configuration is via environment variables (see `.env.example`). Key variables:
- `AMBARI_HOST`, `AMBARI_PORT`, `AMBARI_USER`, `AMBARI_PASS`, `AMBARI_CLUSTER_NAME` — Ambari connection
- `AMBARI_METRICS_*` — AMS collector connection and caching
- `FASTMCP_TYPE`, `FASTMCP_HOST`, `FASTMCP_PORT` — transport configuration
- `REMOTE_AUTH_ENABLE`, `REMOTE_SECRET_KEY` — optional auth
- `MCP_LOG_LEVEL` — logging level

## CI/CD

PyPI publishing auto-triggers on git tag push. The tag value is injected as the package version into `pyproject.toml` during CI. Publishes to TestPyPI and PyPI via trusted OIDC publishing (no stored secrets). See `.github/workflows/pypi-publish.yml`.

## Dependencies

- `fastmcp>=2.12.3` — MCP server framework
- `aiohttp>=3.12.15` — async HTTP client for Ambari API calls
- Python `>=3.12`

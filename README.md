[![Deploy to PyPI with tag](https://github.com/call518/MCP-Ambari-API/actions/workflows/pypi-publish.yml/badge.svg)](https://github.com/call518/MCP-Ambari-API/actions/workflows/pypi-publish.yml)

[![smithery badge](https://smithery.ai/badge/@call518/mcp-ambari-api)](https://smithery.ai/server/@call518/mcp-ambari-api)

# MCP Ambari API

Model Context Protocol (MCP) server for Apache Ambari API integration. This project provides tools for managing Hadoop clusters, including service operations, configuration management, status monitoring, and request tracking.

- [Ambari API Documents](https://github.com/apache/ambari/blob/trunk/ambari-server/docs/api/v1/index.md)

## Features

- Manage Hadoop services (start, stop, restart)
- Monitor service and cluster status
- Unified configuration introspection (single type or bulk with filtering / summarization)
- Track request progress (request IDs surfaced for all operations)

## Available MCP Tools

This MCP server provides the following tools for Ambari cluster management:

### Cluster Management
- `get_cluster_info` - Retrieve basic cluster information and status
- `get_active_requests` - List currently active/running operations
- `get_request_status` - Check status and progress of specific requests

### Service Management
- `get_cluster_services` - List all services with their status
- `get_service_status` - Get detailed status of a specific service
- `get_service_components` - List components and host assignments for a service
- `get_service_details` - Get comprehensive service information
- `start_service` - Start a specific service
- `stop_service` - Stop a specific service
- `restart_service` - Restart a specific service
- `start_all_services` - Start all services in the cluster
- `stop_all_services` - Stop all services in the cluster
- `restart_all_services` - Restart all services in the cluster

### Configuration Management
- `dump_configurations` - Unified configuration tool (replaces `get_configurations`, `list_configurations`, and the former internal `dump_all_configurations`). Supports:
  - Single type: `dump_configurations(config_type="yarn-site")`
  - Bulk summary: `dump_configurations(summarize=True)`
  - Filter by substring (type or key): `dump_configurations(filter="memory")`
  - Service filter (narrow types by substring): `dump_configurations(service_filter="yarn", summarize=True)`
  - Keys only (no values): `dump_configurations(include_values=False)`
  - Limit number of types: `dump_configurations(limit=10, summarize=True)`

> Breaking Change: `get_configurations` and `list_configurations` were removed in favor of this single, more capable tool.

### Host Management
- `list_hosts` - List all hosts in the cluster
- `get_host_details` - Get detailed information for specific or all hosts (includes component states, hardware metrics, and service assignments)

## Prompt Template
The package exposes a tool `get_prompt_template` that returns either the entire template, a specific section, or just the headings. Three MCP prompts (`prompt_template_full`, `prompt_template_headings`, `prompt_template_section`) are also registered for discovery.

### MCP Prompts

For easier discoverability in MCP clients (so `prompts/list` is not empty), the server now registers three prompts:

- `prompt_template_full` – returns the full canonical template
- `prompt_template_headings` – returns only the section headings
- `prompt_template_section` – takes a `section` argument (number or keyword) and returns that section

You can still use the `get_prompt_template` tool for programmatic access or when you prefer tool invocation over prompt retrieval.

Single canonical English prompt template guides safe and efficient tool selection.

Files:

- Packaged: `src/mcp_ambari_api/prompt_template.md` (distributed with PyPI)
- (Optional workspace root copy `PROMPT_TEMPLATE.md` may exist for editing; packaged copy is the one loaded at runtime.)

Retrieve dynamically via MCP tool:

- `get_prompt_template()` – full template
- `get_prompt_template("tool map")` – only the tool mapping section
- `get_prompt_template("5")` – section 5 (formatting guidelines)
- `get_prompt_template(mode="headings")` – list all section headings

Policy: Only English is stored; LLM는 사용자 질의 언어와 무관하게 영어 지침을 내부 추론용으로 사용하고, 사용자 응답은 필요 시 다국어로 생성한다.

### Configuration Tool Migration Notes

| Removed | Replacement | Notes |
|---------|-------------|-------|
| `get_configurations` | `dump_configurations(config_type=...)` | Single type retrieval now goes through unified tool |
| `list_configurations` | `dump_configurations(summarize=True)` | Summary listing of all types (sample keys) |
| `dump_all_configurations` | `dump_configurations` | Renamed & expanded (adds service_filter, keys-only mode) |

If you maintained automation calling the old tools, update to the unified form. The semantic output structure (plain text) remains similar; summary mode minimizes payload size, while full mode provides key=value pairs.

## Main Tool Files

- **Main MCP tool file**: `src/mcp_ambari_api/ambari_api.py`
- **Utility functions**: `src/mcp_ambari_api/functions.py`

## How To Use

Using this Ambari API integration is very simple and straightforward. If you already have an MCP Tools environment running, just add the following configuration to your `mcp-config.json` file:

```json
{
  "mcpServers": {
    "ambari-api": {
      "command": "uvx",
      "args": ["--python", "3.11", "mcp-ambari-api"],
      "env": {
        "AMBARI_HOST": "host.docker.internal",
        "AMBARI_PORT": "8080",
        "AMBARI_USER": "admin",
        "AMBARI_PASS": "admin",
        "AMBARI_CLUSTER_NAME": "TEST-AMBARI",
        "AMBARI_LOG_LEVEL": "INFO"
      }
    }
  }
}
```

> Local Demo Tip: Start by copying the template: `cp mcp-config.json.local mcp-config.json` and then edit the values for your environment.

## Self QuickStart (Demo): Setting Up MCP Tools Environment with Docker

  "command": "mcp-ambari-api",
  "args": [],
### Tested Env.

- WSL2 Linux on Windows11
- Ambari-3.0 Cluster

### 1. Prepare Ambari Cluster (Test Target)

To set up a Ambari Demo cluster, follow the guide at: [Install Ambari 3.0 with Docker](https://medium.com/@call518/install-ambari-3-0-with-docker-297a8bb108c8)

![Example: Ambari Demo Cluster](img/ex-ambari.png)


If running inside the provided container image, the package is installed and exposes the `mcp-ambari-api` console script (entry point defined in `pyproject.toml`). Avoid invoking the module path directly to prevent relative import errors.
Once your Ambari cluster is ready, check the following environment variables in your `mcp-config.json` file:

```json
"PYTHONPATH": "/app/src",
"AMBARI_HOST": "host.docker.internal",
"AMBARI_PORT": "8080",
"AMBARI_USER": "admin",
"AMBARI_PASS": "admin",
"AMBARI_CLUSTER_NAME": "TEST-AMBARI",
"AMBARI_LOG_LEVEL": "INFO"
```
Make sure these values match your Ambari cluster setup.

### Logging & Observability

The server emits structured log lines for every tool invocation and HTTP request helper:

- Prefixes: `TOOL START`, `TOOL SUCCESS`, `TOOL ERROR_RETURN`, `TOOL EXCEPTION`
- Each line includes elapsed time (ms) and basic size metadata.
- Under DEBUG level, additional HTTP request diagnostics (endpoint, status, timing) are printed.

Control log verbosity via either environment variable or CLI flag:

| Method | Example |
|--------|---------|
| Environment variable | `export AMBARI_LOG_LEVEL=DEBUG` |
| CLI flag (takes precedence) | `mcp-ambari-api --log-level DEBUG` |
| Smithery config (added property) | Set `AMBARI_LOG_LEVEL` to desired level |

Supported levels: DEBUG, INFO (default), WARNING, ERROR, CRITICAL.

Recommendations:
- Use DEBUG temporarily when diagnosing failed Ambari requests or performance.
- Keep INFO for normal operations (includes start/success summaries only).
- Elevate to WARNING/ERROR in very noisy multi-tenant environments.

Example (one-off):
```bash
AMBARI_LOG_LEVEL=DEBUG mcp-ambari-api
```
or
```bash
mcp-ambari-api --log-level DEBUG
```

Smithery now passes the selected `AMBARI_LOG_LEVEL` both as env and `--log-level` flag so runtime overrides take effect immediately.

### 2. MCP Tools Environment Setup

1. Ensure Docker and Docker Compose are installed on your system.
2. Clone this repository and navigate to its root directory.
3. Start the OpenWebUI and MCPO-Proxy environment:
   ```bash
   docker-compose up -d
   ```

- OpenWebUI will be available at the port specified in your `docker-compose.yml` (default: 3000 or as configured). You can access OpenWebUI at: [http://localhost:3000](http://localhost:3000)
- The MCPO-Proxy will be accessible for API requests and cluster management, and its port is also specified in your `docker-compose.yml` (default: 8000 or as configured).
- The list of MCP tool features provided by `src/mcp_ambari_api/ambari_api.py` can be found in the MCPO API Docs: [http://localhost:8000/ambari-api/docs](http://localhost:8000/ambari-api/docs)
![Example: MCPO-Proxy](img/mcpo-proxy-api-docs.png)

### 4. Registering the Ambari-API MCP Tool in OpenWebUI

After logging in to OpenWebUI with an admin account, go to "Settings" → "Tools" from the top menu.
Here, enter the Ambari-API address (e.g., `http://localhost:8000/ambari-api`) to connect MCP Tools with your Ambari cluster.

### 5. Examples: Using MCP Tools to Query Ambari Cluster

Below is an example screenshot showing how to query the Ambari cluster using MCP Tools in OpenWebUI:

#### Example Query #1 - Cluster Info/Status
![Example: Querying Ambari Cluster(1)](img/ex-screenshot-1.png)

#### Example Query #2 - Cluster Configuration Review & Recommendations
![Example: Querying Ambari Cluster(2)](img/ex-screenshot-2.png)

#### Example Query #3 - Restart HDFS Service
![Example: Querying Ambari Cluster(3)](img/ex-screenshot-3-1.png)
![Example: Querying Ambari Cluster(3)](img/ex-screenshot-3-2.png)

## Roadmap

**✅: Implemented**  
**⬜: Planned / Useful (from [Ambari API v1 docs](https://github.com/apache/ambari/tree/trunk/ambari-server/docs/api/v1/))**

- [x] Cluster information & status (`clusters.md`, `clusters-cluster.md`, `cluster-resources.md`)
- [x] Service list & status (`services.md`, `services-service.md`, `service-resources.md`)
- [x] Start/Stop/Restart services (`update-service.md`, `update-services.md`, `services-service.md`)
- [x] Cluster configuration (get & update) (`configuration.md`, `config-groups.md`)
- [x] Request & task tracking (`requests.md`, `request-resources.md`, `tasks.md`, `task-resources.md`)
- [x] Service component/host information (`components.md`, `components-component.md`, `component-resources.md`, `hosts.md`, `hosts-host.md`, `host-resources.md`, `host-components.md`, `host-component.md`)
- [x] Host/HostComponent detailed management (`host-components.md`, `host-component.md`, `hosts-host.md`)
- [ ] User management (`user-*.md`)
- [ ] Permission management (`permission-*.md`)
- [ ] View management (`view-resources.md`)
- [ ] Alert definitions & dispatching (`alert-definitions.md`, `alert-dispatching.md`, `alerts.md`)
- [ ] Authentication source management (`authentication-source-*.md`)
- [ ] Config group management (`config-groups.md`)
- [ ] Credential management (`credential-*.md`)
- [ ] Repository/Stack version management (`repository-version-resources.md`, `stack-version-resources.md`)

> Only the most practical and useful features are selected. Contributions and suggestions are welcome!

## Appendix: Smithery Deployment

Public Smithery deployment available for quick trials (no local setup) if you have a publicly reachable Ambari cluster. Open the server page and supply your Ambari connection values in the configuration form, then invoke tools immediately. Do NOT enter sensitive credentials unless you trust the environment. Link: https://smithery.ai/server/@call518/mcp-ambari-api

![Smithery Deployment Screenshot](img/ex-screenshot-smithery.ai.png)

### Installing via Smithery

To install Ambari API Integration Server for Claude Desktop automatically via [Smithery](https://smithery.ai/server/@call518/mcp-ambari-api):

```bash
npx -y @smithery/cli install @call518/mcp-ambari-api --client claude
```

## License

This project is licensed under the MIT License.

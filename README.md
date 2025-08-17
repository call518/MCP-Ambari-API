# MCP Ambari API

[![MSeeP.ai Security Assessment Badge](https://mseep.net/pr/call518-mcp-ambari-api-badge.png)](https://mseep.ai/app/call518-mcp-ambari-api)

[![Verified on MSeeP](https://mseep.ai/badge.svg)](https://mseep.ai/app/2fd522d4-863d-479d-96f7-e24c7fb531db)

[![Deploy to PyPI with tag](https://github.com/call518/MCP-Ambari-API/actions/workflows/pypi-publish.yml/badge.svg)](https://github.com/call518/MCP-Ambari-API/actions/workflows/pypi-publish.yml)

Model Context Protocol (MCP) server for Apache Ambari API integration. This project provides tools for managing Hadoop clusters, including service operations, configuration management, status monitoring, and request tracking.

- [Ambari API Documents](https://github.com/apache/ambari/blob/trunk/ambari-server/docs/api/v1/index.md)

## Example Query - Cluster Info/Status

![Example: Querying Ambari Cluster(1)](img/ex-screenshot-1.png)

## Usages

This MCP server supports two connection modes: **stdio** (traditional) and **http** (Docker-based). The transport mode is automatically determined by the `MCP_SERVER_PORT` environment variable.

**Transport Selection Logic:**

- **http mode**: When `MCP_SERVER_PORT` environment variable is set
- **stdio mode**: When `MCP_SERVER_PORT` environment variable is NOT set

```python
    ### http mode
    if os.getenv("MCP_SERVER_PORT"):
        port = int(os.getenv("PORT", "18000"))
        logger.info(f"Starting HTTP server on port {port} for smithery.ai")
        mcp.run(transport="http", host="0.0.0.0", port=port)
    ### stdio mode
    else:
        logger.info("Starting stdio transport for local usage")
        mcp.run(transport='stdio')
```

Using this is very simple and straightforward. If you already have an MCP Tools environment running, just add the following configuration to your `mcp-config.json` file:

### Method 1: Local MCP (transport=stdio)

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

### Method 2: Remote MCP (transport=http)

**On MCP-Server Host:**

```bash
pip install uv
pip install mcp-ambari-api

export AMBARI_HOST="host.docker.internal""
export AMBARI_PORT="8080"
export AMBARI_USER="admin"
export AMBARI_PASS="admin"
export AMBARI_CLUSTER_NAME="TEST-AMBARI"
export AMBARI_LOG_LEVEL="INFO"

uvx mcp-ambari-api
```

**On MCP-Client Host:**

```json
{
  "mcpServers": {
    "ambari-api": {
      "type": "http",
      "url": "http://host.docker.internal:18001/mcp"
    }
  }
}
```

## Features

- Manage Hadoop services (start, stop, restart)
- Monitor service and cluster status
- Unified configuration introspection (single type or bulk with filtering / summarization)
- Track request progress (request IDs surfaced for all operations)
- Manage cluster users and access permissions

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

### User Management

- `list_users` - List all users in the Ambari system with their usernames and API links
- `get_user` - Get detailed information about a specific user including:
  - Basic profile (ID, username, display name, user type)
  - Status information (admin privileges, active status, login failures)
  - Authentication details (LDAP user status, authentication sources)
  - Group memberships, privileges, and widget layouts

### Alert Management

- `get_alerts_history` - **Unified alert tool** for both current and historical alerts:
  - **Current mode** (`mode="current"`): Retrieve current/active alerts with real-time status
    - Current alert states across cluster, services, or hosts
    - Maintenance mode filtering (ON/OFF)
    - Summary formats: basic summary and grouped by definition
    - Detailed alert information including timestamps and descriptions
  - **History mode** (`mode="history"`): Retrieve historical alert events from the cluster
    - Scope filtering: cluster-wide, service-specific, or host-specific alerts
    - Time range filtering: from/to timestamp support
    - Pagination support for large datasets
  - **Common features** (both modes):
    - State filtering: CRITICAL, WARNING, OK, UNKNOWN alerts
    - Definition filtering: filter by specific alert definition names
    - Multiple output formats: detailed, summary, compact
    - Unified API for consistent alert querying experience

---

## QuickStart (http Mode)

Running OpenWebUI and MCP-Ambari-API with Docker

### Tested Env.

- WSL2 Linux on Windows11
  - `.wslconfig `: tested with `networkingMode = bridged`
- Ambari-3.0 Cluster

### 1. Prepare Ambari Cluster (Test Target)

To set up a Ambari Demo cluster, follow the guide at: [Install Ambari 3.0 with Docker](https://medium.com/@call518/install-ambari-3-0-with-docker-297a8bb108c8)

![Example: Ambari Demo Cluster](img/ex-ambari.png)

#### Ambari Cluster Configurations

```json
"PYTHONPATH": "/app/src",
"AMBARI_HOST": "host.docker.internal",
"AMBARI_PORT": "8080",
"AMBARI_USER": "admin",
"AMBARI_PASS": "admin",
"AMBARI_CLUSTER_NAME": "TEST-AMBARI",
"AMBARI_LOG_LEVEL": "INFO"
```

(NOTE) Make sure these values match your Ambari cluster setup.

### 2. Run Docker-Compose

Startup `OpenWebUI` and `MCPO(MCP to OpenAPI)`, `MCP-Server`

1. Ensure Docker and Docker Compose are installed on your system.
1. Clone this repository and navigate to its root directory.
1. Check and update `docker-compose.yml`.
1. Check Networking for Host and Docker Containers.
1. Run:

   ```bash
   docker-compose up -d
   ```

- OpenWebUI will be available at the port specified in your `docker-compose.yml` (default: 3000 or as configured).
  - e.g: http://localhost:3000 or as configured.
- The MCPO-Proxy will be accessible for API requests and cluster management, and its port is also specified in your `docker-compose.yml`.
  - e.g: 8000 or as configured.
- The list of MCP tool features provided by `src/mcp_ambari_api/ambari_api.py` can be found in the MCPO API Docs.
  - e.g: http://localhost:8000/ambari-api/docs
![Example: MCPO-Proxy](img/mcpo-proxy-api-docs.png)

### 3. Registering the Tool in OpenWebUI

1. logging in to OpenWebUI with an admin account
1. go to "Settings" → "Tools" from the top menu.
1. Enter the `ambari-api` Tool address (e.g., `http://localhost:8000/ambari-api`) to connect MCP Tools with your Ambari cluster.

### 4. More Examples: Using MCP Tools to Query Ambari Cluster

Below is an example screenshot showing how to query the Ambari cluster using MCP Tools in OpenWebUI:

#### Example Query - Cluster Configuration Review & Recommendations

![Example: Querying Ambari Cluster(2)](img/ex-screenshot-2.png)

#### Example Query - Restart HDFS Service

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

## License

This project is licensed under the MIT License.

[![Deploy to PyPI with tag](https://github.com/call518/MCP-Ambari-API/actions/workflows/pypi-publish.yml/badge.svg)](https://github.com/call518/MCP-Ambari-API/actions/workflows/pypi-publish.yml)

# MCP Ambari API

Model Context Protocol (MCP) server for Apache Ambari API integration. This project provides tools for managing Hadoop clusters, including service operations, configuration management, status monitoring, and request tracking.

## Features

- Manage Hadoop services (start, stop, restart)
- Monitor service and cluster status
- Retrieve and update configurations
- Track request progress

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
- `get_configurations` - Retrieve service configuration types and values
- `list_configurations` - List all available configuration types in the cluster

### Host Management
- `list_hosts` - List all hosts in the cluster
- `get_host_details` - Get detailed information for specific or all hosts

## Main Tool Files

- **Main MCP tool file**: `src/mcp_ambari_api/ambari_api.py`
- **Utility functions**: `src/mcp_ambari_api/functions.py`

## How To Use

Using this Ambari API integration is very simple and straightforward. If you already have an MCP Tools environment running, just add the following configuration to your `mcp-config.json` file:

```json
{
  "mcpServers": {
    "ambar-api": {
      "command": "uvx",
      "args": ["--python", "3.11", "mcp-ambari-api"],
      "env": {
        "AMBARI_HOST": "host.docker.internal",
        "AMBARI_PORT": "8080",
        "AMBARI_USER": "admin",
        "AMBARI_PASS": "admin",
        "AMBARI_CLUSTER_NAME": "TEST-AMBARI"
      }
    }
  }
}
```

## Self QuickStart (Demo): Setting Up MCP Tools Environment with Docker

This section describes how to set up the MCP Tools environment to control an Ambari cluster using OpenWebUI and MCPO, leveraging the provided `docker-compose.yml` and `Dockerfile`.

### 1. Prepare Ambari Cluster (Test Target)

To set up a Ambari Demo cluster, follow the guide at:
https://medium.com/@call518/install-ambari-3-0-with-docker-297a8bb108c8
![Example: Ambari Demo Cluster](img/ex-ambari.png)

Once your Ambari cluster is ready, check the following environment variables in your `mcp-config.json` file:

```json
"AMBARI_HOST": "host.docker.internal",
"AMBARI_PORT": "8080",
"AMBARI_USER": "admin",
"AMBARI_PASS": "admin",
"AMBARI_CLUSTER_NAME": "TEST-AMBARI"
```
Make sure these values match your Ambari cluster setup.

### 2. MCP Tools Environment Setup

1. Ensure Docker and Docker Compose are installed on your system.
2. Clone this repository and navigate to its root directory.
3. Start the OpenWebUI and MCPO-Proxy environment:
   ```bash
   docker-compose up -d
   ```

- OpenWebUI will be available at the port specified in your `docker-compose.yml` (default: 3000 or as configured). You can access OpenWebUI at: [http://localhost:3000](http://localhost:3000)
- The MCPO-Proxy will be accessible for API requests and cluster management, and its port is also specified in your `docker-compose.yml` (default: 8000 or as configured).
- The list of MCP tool features provided by `src/mcp_ambari_api/ambari_api.py` can be found in the MCPO API Docs: [http://localhost:8000/ambar-api/docs](http://localhost:8000/ambar-api/docs)
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

## License

This project is licensed under the MIT License.
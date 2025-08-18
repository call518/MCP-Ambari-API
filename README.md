# MCP Ambari API - Apache Hadoop Cluster Management Automation

> **🚀 Automate Apache Ambari operations with AI/LLM**: Natural language commands for Hadoop cluster management, service control, configuration monitoring, and real-time status tracking via Model Context Protocol (MCP) tools.

## 🏷️ Tags

`apache-ambari` `hadoop-cluster` `mcp-server` `cluster-automation` `devops-tools` `big-data` `infrastructure-management` `ai-automation` `llm-tools` `python-mcp`

[![Verified on MSeeP](https://mseep.ai/badge.svg)](https://mseep.ai/app/2fd522d4-863d-479d-96f7-e24c7fb531db)

[![Deploy to PyPI with tag](https://github.com/call518/MCP-Ambari-API/actions/workflows/pypi-publish.yml/badge.svg)](https://github.com/call518/MCP-Ambari-API/actions/workflows/pypi-publish.yml)

## 📋 Overview

**MCP Ambari API** is a powerful Model Context Protocol (MCP) server that enables seamless Apache Ambari cluster management through natural language commands. Built for DevOps engineers, data engineers, and system administrators who work with Hadoop ecosystems.

### 🎯 What You Can Do

- **Automated Service Management**: Start, stop, restart Hadoop services (HDFS, YARN, Spark, etc.) with simple commands
- **Real-time Monitoring**: Monitor cluster health, service status, and performance metrics
- **Configuration Management**: View, update, and manage cluster configurations across all services  
- **Alert Management**: Track and manage cluster alerts and notifications
- **User & Host Management**: Manage cluster users, permissions, and host assignments
- **Request Tracking**: Monitor long-running operations with detailed progress tracking

### 🏗️ Architecture

This MCP server provides tools for managing Hadoop clusters through Apache Ambari REST API, supporting both local (`stdio`) and remote (`streamable-http`) connection modes for maximum flexibility in deployment scenarios.

- [Ambari API Documents](https://github.com/apache/ambari/blob/trunk/ambari-server/docs/api/v1/index.md)

## 🚀 Use Cases & Benefits

### For DevOps Engineers

- **Incident Response**: Quickly restart failed services during outages
- **Maintenance Automation**: Schedule and execute maintenance tasks via AI commands
- **Health Monitoring**: Get real-time cluster status without navigating complex UIs

### For Data Engineers

- **Pipeline Management**: Ensure data processing services are running before job execution
- **Configuration Tuning**: Easily adjust cluster settings for optimal performance
- **Troubleshooting**: Quickly identify and resolve service conflicts or issues

### For System Administrators

- **User Management**: Manage cluster access and permissions efficiently
- **Resource Monitoring**: Track cluster resources and host performance
- **Alert Management**: Stay informed about critical cluster events

## 💡 Why Choose MCP Ambari API?

- **Natural Language Interface**: No need to remember complex API endpoints
- **AI/LLM Integration**: Works seamlessly with modern AI tools and workflows  
- **Dual Transport Support**: Flexible deployment options (local or remote)
- **Comprehensive Coverage**: 25+ tools covering all major Ambari operations
- **Production Ready**: Built with error handling, logging, and monitoring

## Example Query - Cluster Info/Status

![Example: Querying Ambari Cluster(1)](img/ex-screenshot-1.png)

## ⚡ Quick Installation

### Prerequisites

- Python 3.11 (uv vene --python 3.11 --seed)
- Apache Ambari cluster (3.0+ recommended)
- UV package manager (or pip)

### Install from PyPI

```bash
pip install mcp-ambari-api
# or with uv
uvx mcp-ambari-api
```

## 🔧 Usage & Configuration

This MCP server supports two connection modes: **stdio** (traditional) and **streamable-http** (Docker-based). You can configure the transport mode using CLI arguments or environment variables.

**Configuration Priority:** CLI arguments > Environment variables > Default values

### CLI Arguments

- `--type` (`-t`): Transport type (`stdio` or `streamable-http`) - Default: `stdio`
- `--host`: Host address for HTTP transport - Default: `127.0.0.1`  
- `--port` (`-p`): Port number for HTTP transport - Default: `8080`

### Environment Variables

- `FASTMCP_TYPE`: Transport type (`stdio` or `streamable-http`)
- `FASTMCP_HOST`: Host address for HTTP transport
- `FASTMCP_PORT`: Port number for HTTP transport (also enables streamable-http mode when set)

**Transport Selection Logic:**

- **CLI Priority**: `--type streamable-http --host 0.0.0.0 --port 18002`
- **Environment Priority**: `FASTMCP_TYPE=streamable-http FASTMCP_HOST=0.0.0.0 FASTMCP_PORT=18002`
- **Legacy Support**: `FASTMCP_PORT=18002` (automatically enables streamable-http mode)
- **Default**: `stdio` mode when no configuration is provided

Using this is very simple and straightforward. If you already have an MCP Tools environment running, just add the following configuration to your `mcp-config.json` file:

### Method 1: Local MCP (transport="stdio")

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

### Method 2: Remote MCP (transport="streamable-http")

**On MCP-Server Host:**

```bash
pip install uv
pip install mcp-ambari-api

# Ambari connection settings
export AMBARI_HOST="host.docker.internal"
export AMBARI_PORT="8080"
export AMBARI_USER="admin"
export AMBARI_PASS="admin"
export AMBARI_CLUSTER_NAME="TEST-AMBARI"
export AMBARI_LOG_LEVEL="INFO"

# MCP transport settings (choose one method)
# Method A: Using environment variables
export FASTMCP_TYPE="streamable-http"
export FASTMCP_HOST="127.0.0.1" 
export FASTMCP_PORT="18001"

# Method B: Using CLI arguments
uvx mcp-ambari-api --type streamable-http --host 127.0.0.1 --port 18001

# Method C: Using legacy port-only setting (backward compatibility)
# export FASTMCP_PORT="18001"
# uvx mcp-ambari-api
```

**On MCP-Client Host:**

```json
{
  "mcpServers": {
    "ambari-api": {
      "type": "streamable-http",
      "url": "http://host.docker.internal:18001/mcp"
    }
  }
}
```

## 🎯 Core Features & Capabilities

### Service Operations

- **Hadoop Service Management**: Start, stop, restart HDFS, YARN, Spark, HBase, and more
- **Bulk Operations**: Control all cluster services simultaneously
- **Status Monitoring**: Real-time service health and performance tracking

### Configuration Management

- **Unified Config Tool**: Single interface for all configuration types (yarn-site, hdfs-site, etc.)
- **Bulk Configuration**: Export and manage multiple configurations with filtering
- **Configuration Validation**: Syntax checking and validation before applying changes

### Monitoring & Alerting

- **Real-time Alerts**: Current and historical cluster alerts with filtering
- **Request Tracking**: Monitor long-running operations with detailed progress
- **Host Monitoring**: Hardware metrics, component states, and resource utilization

### Administration

- **User Management**: Cluster user administration and permission control
- **Host Management**: Node registration, component assignments, and health monitoring
- **Security**: LDAP integration support and authentication source management

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

### Configuration Tools

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

## 🚀 Docker QuickStart Guide (Recommended)

### Deploy with OpenWebUI + MCP-Ambari-API in minutes

Perfect for production environments, testing, and enterprise deployments. This setup provides a complete AI-powered Hadoop cluster management solution.

### Tested Env

- WSL2 Linux on Windows11
  - `.wslconfig`: tested with `networkingMode = bridged`
- Ambari-3.0 Cluster

### 1. Prepare Ambari Cluster (Test Target)

To set up a Ambari Demo cluster, follow the guide at: [Install Ambari 3.0 with Docker](https://medium.com/@call518/install-ambari-3-0-with-docker-297a8bb108c8)

![Example: Ambari Demo Cluster](img/ex-ambari.png)

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
  - e.g: <http://localhost:3000> or as configured.
- The MCPO-Proxy will be accessible for API requests and cluster management, and its port is also specified in your `docker-compose.yml`.
  - e.g: 8000 or as configured.
- The list of MCP tool features provided by `src/mcp_ambari_api/ambari_api.py` can be found in the MCPO API Docs.
  - e.g: <http://localhost:8000/ambari-api/docs>
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

## 🗺️ Development Roadmap & Features

### ✅ Completed Features

- **Cluster Management**: Complete cluster information, status monitoring, and service management
- **Service Operations**: Start/stop/restart individual services or entire cluster
- **Configuration Management**: Unified configuration tools with filtering and bulk operations
- **Request Tracking**: Real-time monitoring of long-running cluster operations
- **Host Management**: Comprehensive host and component management
- **Alert System**: Current and historical alert management with advanced filtering
- **User Management**: Basic user administration and permission handling

### ⬜ Planned Features (Contributions Welcome!)

- **Advanced User Management**: Enhanced user profiles and bulk operations
- **Permission System**: Granular permission management and role-based access
- **View Management**: Custom dashboard and view configuration
- **Alert Definitions**: Custom alert creation and notification rules
- **Authentication Sources**: LDAP, Active Directory, and SSO integration
- **Config Groups**: Advanced configuration group management
- **Credential Management**: Secure credential storage and rotation
- **Repository Management**: Stack version and repository management tools

> **Note**: Features are prioritized based on community feedback and enterprise needs. [Submit feature requests](https://github.com/call518/MCP-Ambari-API/issues) or contribute via pull requests!

## 🤝 Contributing & Support

### How to Contribute

- 🐛 **Report Bugs**: [GitHub Issues](https://github.com/call518/MCP-Ambari-API/issues)
- 💡 **Request Features**: [Feature Requests](https://github.com/call518/MCP-Ambari-API/issues)  
- 🔧 **Submit PRs**: [Contributing Guidelines](https://github.com/call518/MCP-Ambari-API/blob/main/CONTRIBUTING.md)
- 📖 **Improve Docs**: Help make documentation better

### Getting Help

- **Documentation**: Check this README and inline code comments
- **Community**: GitHub Discussions for questions and best practices
- **Issues**: Bug reports and technical support via GitHub Issues

### Technologies Used

- **Language**: Python 3.11+
- **Framework**: Model Context Protocol (MCP)
- **API**: Apache Ambari REST API
- **Transport**: stdio (local) and streamable-http (remote)
- **Deployment**: Docker, Docker Compose, PyPI

## ❓ Frequently Asked Questions

### Q: What Ambari versions are supported?

**A**: Ambari 3.0+ is recommended. Earlier versions may work but are not officially tested.

### Q: Can I use this with cloud-managed Hadoop clusters?

**A**: Yes, as long as Ambari API endpoints are accessible, it works with on-premise, cloud, and hybrid deployments.

### Q: How do I troubleshoot connection issues?

**A**: Check your `AMBARI_HOST`, `AMBARI_PORT`, and network connectivity. Enable debug logging with `AMBARI_LOG_LEVEL=DEBUG`.

### Q: Is this safe for production use?

**A**: Yes, the tool only uses official Ambari APIs and includes comprehensive error handling and logging.

### Q: How does this compare to Ambari Web UI?

**A**: This provides programmatic access via AI/LLM commands, perfect for automation, scripting, and integration with modern DevOps workflows.

## 📄 License

This project is licensed under the MIT License.

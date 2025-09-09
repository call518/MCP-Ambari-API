# MCP Ambari API - Apache Hadoop Cluster Management Automation

> **🚀 Automate Apache Ambari operations with AI/LLM**: Natural language commands for Hadoop cluster management, service control, configuration monitoring, and real-time status tracking via Model Context Protocol (MCP) tools.

---

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Deploy to PyPI with tag](https://github.com/call518/MCP-Ambari-API/actions/workflows/pypi-publish.yml/badge.svg)](https://github.com/call518/MCP-Ambari-API/actions/workflows/pypi-publish.yml)
[![Ask DeepWiki](https://deepwiki.com/badge.svg)](https://deepwiki.com/call518/MCP-Ambari-API)
[![Verified on MSeeP](https://mseep.ai/badge.svg)](https://mseep.ai/app/2fd522d4-863d-479d-96f7-e24c7fb531db)
[![BuyMeACoffee](https://raw.githubusercontent.com/pachadotdev/buymeacoffee-badges/main/bmc-donate-yellow.svg)](https://www.buymeacoffee.com/call518)

## 📋 Overview

**MCP Ambari API** is a powerful Model Context Protocol (MCP) server that enables seamless Apache Ambari cluster management through natural language commands. Built for DevOps engineers, data engineers, and system administrators who work with Hadoop ecosystems.

---

### 🎯 What You Can Do

- **Automated Service Management**: Start, stop, restart Hadoop services (HDFS, YARN, Spark, etc.) with simple commands
- **Real-time Monitoring**: Monitor cluster health, service status, and performance metrics
- **Configuration Management**: View, update, and manage cluster configurations across all services  
- **Alert Management**: Track and manage cluster alerts and notifications
- **User & Host Management**: Manage cluster users, permissions, and host assignments
- **Request Tracking**: Monitor long-running operations with detailed progress tracking

### Docuement for Airflow REST-API
- [Ambari API Documents](https://github.com/apache/ambari/blob/trunk/ambari-server/docs/api/v1/index.md)

## Topics

`apache-ambari` `hadoop-cluster` `mcp-server` `cluster-automation` `devops-tools` `big-data` `infrastructure-management` `ai-automation` `llm-tools` `python-mcp`

---

## Example Queries - Cluster Info/Status

![Example: Querying Ambari Cluster(1)](img/ex-screenshot-1.png)

**[Go to More Example Queries](./src/mcp_ambari_api/prompt_template.md#5-example-queries)**

---

## 🚀 QuickStart Guide /w Docker

> **Note:** The following instructions assume you are using the `streamable-http` mode for MCP Server.

### Flow Diagram of Quickstart/Tutorial

![Flow Diagram of Quickstart/Tutorial](img/MCP-Workflow-of-Quickstart-Tutorial.png)

### 1. Prepare Ambari Cluster (Test Target)

To set up a Ambari Demo cluster, follow the guide at: [Install Ambari 3.0 with Docker](https://medium.com/@call518/install-ambari-3-0-with-docker-297a8bb108c8)

![Example: Ambari Demo Cluster](img/ex-ambari.png)

### 2. Run Docker-Compose

Start the `MCP-Server`, `MCPO`(MCP-Proxy for OpenAPI), and `OpenWebUI`.

1. Ensure Docker and Docker Compose are installed on your system.
1. Clone this repository and navigate to its root directory.
1. **Set up environment configuration:**
   ```bash
   # Copy environment template and configure your settings
   cp .env.example .env
   # Edit .env with your Ambari cluster information
   ```
1. **Configure your Ambari connection in `.env` file:**
   ```bash
   # Ambari cluster connection
   AMBARI_HOST=host.docker.internal
   AMBARI_PORT=7070
   AMBARI_USER=admin
   AMBARI_PASS=admin
   AMBARI_CLUSTER_NAME=TEST-AMBARI
   
   # (Optional) Enable authentication for streamable-http mode
   # Recommended for production environments
   REMOTE_AUTH_ENABLE=false
   REMOTE_SECRET_KEY=your-secure-secret-key-here
   ```
1. Run:
   ```bash
   docker-compose up -d
   ```

- OpenWebUI will be available at: `http://localhost:${DOCKER_EXTERNAL_PORT_OPENWEBUI}` (default: 3001)
- The MCPO-Proxy will be accessible at: `http://localhost:${DOCKER_EXTERNAL_PORT_MCPO_PROXY}` (default: 8001)  
- The MCPO API Docs: `http://localhost:${DOCKER_EXTERNAL_PORT_MCPO_PROXY}/ambari-api/docs`

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

---

## 💡 Tool Example Queries

### 🔍 Cluster & Service Management

**get_cluster_info**
- "Show cluster summary and basic information."
- "What's the cluster name and version?"
- "Display cluster overview with service counts."
- 📋 **Features**: Cluster name, version, service counts, basic cluster information

**get_cluster_services**
- "Show all cluster services and their current status."
- "List all services with their states."
- "Display service overview for the cluster."
- "Which services are running in the cluster?"
- 📋 **Features**: Service names, states, health status overview

**get_service_status**
- "What's the status of HDFS service?"
- "Check if YARN is running properly."
- "Show current state of HBase service."
- "Is the MapReduce service healthy?"
- 📋 **Features**: Individual service state, health check, status details

**get_service_components**
- "Show HDFS components and which hosts they're running on."
- "List all YARN components with their host assignments."
- "Display component distribution for Kafka service."
- "Which hosts are running NameNode components?"
- 📋 **Features**: Component-to-host mapping, service distribution analysis

**get_service_details**
- "Get detailed information about HDFS service including all components."
- "Show comprehensive YARN service overview with component states."
- "Display full service details for Spark with host assignments."
- 📋 **Features**: Complete service overview with components and host details

### ⚙️ Service Operations

**start_service / stop_service / restart_service**
- "Start the HDFS service."
- "Stop the MapReduce service."
- "Restart the YARN service."
- "Please restart the HBase service."
- 📋 **Features**: Individual service lifecycle management
- ⚠️ **Note**: Returns request ID for operation tracking

**start_all_services / stop_all_services / restart_all_services**
- "Start all cluster services."
- "Stop all services in the cluster."
- "Restart all cluster services."
- 📋 **Features**: Bulk service operations for entire cluster
- ⚠️ **Warning**: These are high-impact operations affecting the entire cluster

### 📊 Operations & Monitoring

**get_active_requests**
- "Show all running operations."
- "List current service requests in progress."
- "What operations are currently active?"
- "Display ongoing cluster operations."
- 📋 **Features**: Real-time operation status, request monitoring

**get_request_status**
- "Check the status of request ID 123."
- "Show progress for operation 456."
- "Get details for the last restart request."
- "Monitor request 789 completion status."
- 📋 **Features**: Detailed request progress, completion status, error tracking

### 🖥️ Host Management

**list_hosts**
- "List all hosts in the cluster."
- "Show cluster node inventory."
- "Display all available hosts."
- 📋 **Features**: Host inventory, cluster node overview

**get_host_details**
- "Show detailed information for host node1.example.com."
- "Get component status on host node2.example.com."
- "Display all host details with component states."
- "Show hardware and component information for specific host."
- 📋 **Features**: Hardware specs, component states, host health status
- 💡 **Tip**: Omit hostname parameter to get details for all hosts

### 🔧 Configuration Management

**dump_configurations**
- "Show all configuration types available."
- "Display HDFS configuration settings."
- "Get YARN resource manager configuration."
- "Show core-site.xml configuration values."
- "Find all configurations containing 'memory' settings."
- "Display summarized view of all service configurations."
- 📋 **Features**: Configuration type exploration, property search, service-specific configs
- 💡 **Usage**: Use `summarize=True` for overview, `filter` parameter for specific properties

### 👥 User Management

**list_users**
- "Show all cluster users."
- "List users with access to Ambari."
- "Display user accounts and their roles."
- 📋 **Features**: User accounts, role assignments, access permissions

**get_user**
- "Get detailed information for user 'admin'."
- "Show profile and permissions for user 'operator'."
- "Display authentication details for specific user."
- 📋 **Features**: User profile, permissions, authentication source, role details

### 🚨 Alert Management

**get_alerts_history (current mode)**
- "Show current active alerts."
- "Display all current alert states."
- "List active alerts for HDFS service."
- "Show critical alerts that are currently active."
- 📋 **Features**: Real-time alert monitoring, service-specific alerts, severity filtering

**get_alerts_history (history mode)**
- "Show alert history for the last 24 hours."
- "Display HDFS alerts from yesterday."
- "Get critical alerts from last week."
- "Show all alerts that occurred in the past month."
- "Find alerts for specific host from last 7 days."
- 📋 **Features**: Historical alert analysis, time-based filtering, trend analysis
- 💡 **Smart Time Processing**: Supports natural language time expressions in any language

### 📚 System Information

**get_prompt_template**
- "Show available prompt template sections."
- "Get tool usage guidelines."
- "Display example queries for reference."
- 📋 **Features**: Template documentation, usage guidelines, section navigation

---

## 🐛 Usage & Configuration

This MCP server supports two connection modes: **stdio** (traditional) and **streamable-http** (Docker-based). You can configure the transport mode using CLI arguments or environment variables.

**Configuration Priority:** CLI arguments > Environment variables > Default values

### CLI Arguments

- `--type` (`-t`): Transport type (`stdio` or `streamable-http`) - Default: `stdio`
- `--host`: Host address for HTTP transport - Default: `127.0.0.1`  
- `--port` (`-p`): Port number for HTTP transport - Default: `8000`
- `--auth-enable`: Enable Bearer token authentication for streamable-http mode - Default: `false`
- `--secret-key`: Secret key for Bearer token authentication (required when auth enabled)

### Environment Variables

| Variable | Description | Default | Project Default |
|----------|-------------|---------|-----------------|
| `PYTHONPATH` | Python module search path for MCP server imports | - | `/app/src` |
| `MCP_LOG_LEVEL` | Server logging verbosity (DEBUG, INFO, WARNING, ERROR) | `INFO` | `INFO` |
| `FASTMCP_TYPE` | MCP transport protocol (stdio for CLI, streamable-http for web) | `stdio` | `streamable-http` |
| `FASTMCP_HOST` | HTTP server bind address (0.0.0.0 for all interfaces) | `127.0.0.1` | `0.0.0.0` |
| `FASTMCP_PORT` | HTTP server port for MCP communication | `8000` | `8000` |
| `REMOTE_AUTH_ENABLE` | Enable Bearer token authentication for streamable-http mode<br/>**Default: false** (if undefined, empty, or null) | `false` | `false` |
| `REMOTE_SECRET_KEY` | Secret key for Bearer token authentication<br/>**Required when REMOTE_AUTH_ENABLE=true** | - | `your-secret-key-here` |
| `AMBARI_HOST` | Ambari server hostname or IP address | `127.0.0.1` | `host.docker.internal` |
| `AMBARI_PORT` | Ambari server port number | `8080` | `8080` |
| `AMBARI_USER` | Username for Ambari server authentication | `admin` | `admin` |
| `AMBARI_PASS` | Password for Ambari server authentication | `admin` | `admin` |
| `AMBARI_CLUSTER_NAME` | Name of the target Ambari cluster | `TEST-AMBARI` | `TEST-AMBARI` |
| `DOCKER_EXTERNAL_PORT_OPENWEBUI` | Host port mapping for Open WebUI container | `8080` | `3001` |
| `DOCKER_EXTERNAL_PORT_MCP_SERVER` | Host port mapping for MCP server container | `8080` | `18001` |
| `DOCKER_EXTERNAL_PORT_MCPO_PROXY` | Host port mapping for MCPO proxy container | `8000` | `8001` |

**Note**: `AMBARI_CLUSTER_NAME` serves as the default target cluster for operations when no specific cluster is specified. All environment variables can be configured via the `.env` file. 

**Transport Selection Logic:**

**Configuration Priority:** CLI arguments > Environment variables > Default values

**Transport Selection Logic:**

- **CLI Priority**: `--type streamable-http --host 0.0.0.0 --port 18001`
- **Environment Priority**: `FASTMCP_TYPE=streamable-http FASTMCP_HOST=0.0.0.0 FASTMCP_PORT=18001`
- **Legacy Support**: `FASTMCP_PORT=18001` (automatically enables streamable-http mode)
- **Default**: `stdio` mode when no configuration is provided

### Environment Setup

```bash
# 1. Clone the repository
git clone https://github.com/call518/MCP-Ambari-API.git
cd MCP-Ambari-API

# 2. Set up environment configuration
cp .env.example .env

# 3. Configure your Ambari connection in .env file
AMBARI_HOST=your-ambari-host
AMBARI_PORT=your-ambari-port  
AMBARI_USER=your-username
AMBARI_PASS=your-password
AMBARI_CLUSTER_NAME=your-cluster-name
```

---

## 🔐 Security & Authentication

### Bearer Token Authentication

For `streamable-http` mode, this MCP server supports Bearer token authentication to secure remote access. This is especially important when running the server in production environments.

#### Configuration

**Enable Authentication:**

```bash
# In .env file
REMOTE_AUTH_ENABLE=true
REMOTE_SECRET_KEY=your-secure-secret-key-here
```

**Or via CLI:**

```bash
python -m mcp_ambari_api --type streamable-http --auth-enable --secret-key your-secure-secret-key-here
```

#### Security Levels

1. **stdio mode** (Default): Local-only access, no authentication needed
2. **streamable-http + REMOTE_AUTH_ENABLE=false/undefined**: Remote access without authentication ⚠️ **NOT RECOMMENDED for production**
3. **streamable-http + REMOTE_AUTH_ENABLE=true**: Remote access with Bearer token authentication ✅ **RECOMMENDED for production**

> **🔒 Default Policy**: `REMOTE_AUTH_ENABLE` defaults to `false` if undefined, empty, or null. This ensures the server starts even without explicit authentication configuration.

#### Client Configuration

When authentication is enabled, MCP clients must include the Bearer token in the Authorization header:

```json
{
  "mcpServers": {
    "ambari-api": {
      "type": "streamable-http",
      "url": "http://your-server:8000/mcp",
      "headers": {
        "Authorization": "Bearer your-secure-secret-key-here"
      }
    }
  }
}
```

#### Security Best Practices

- **Always enable authentication** when using streamable-http mode in production
- **Use strong, randomly generated secret keys** (32+ characters recommended)
- **Use HTTPS** when possible (configure reverse proxy with SSL/TLS)
- **Restrict network access** using firewalls or network policies
- **Rotate secret keys regularly** for enhanced security
- **Monitor access logs** for unauthorized access attempts

#### Error Handling

When authentication fails, the server returns:
- **401 Unauthorized** for missing or invalid tokens
- **Detailed error messages** in JSON format for debugging

---

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
        "MCP_LOG_LEVEL": "INFO"
      }
    }
  }
}
```

### Method 2: Remote MCP (transport="streamable-http")

**On MCP-Client Host:**

```json
{
  "mcpServers": {
    "ambari-api": {
      "type": "streamable-http",
      "url": "http://localhost:18001/mcp"
    }
  }
}
```

**With Bearer Token Authentication (Recommended for production):**

```json
{
  "mcpServers": {
    "ambari-api": {
      "type": "streamable-http", 
      "url": "http://localhost:18001/mcp",
      "headers": {
        "Authorization": "Bearer your-secure-secret-key-here"
      }
    }
  }
}
```

---

## Example usage: Claude-Desktop

**claude_desktop_config.json**

```json
{
  "mcpServers": {
    "ambari-api": {
      "command": "uvx",
      "args": ["--python", "3.11", "mcp-ambari-api"],
      "env": {
        "AMBARI_HOST": "localhost",
        "AMBARI_PORT": "7070",
        "AMBARI_USER": "admin",
        "AMBARI_PASS": "admin",
        "AMBARI_CLUSTER_NAME": "TEST-AMBARI",
        "MCP_LOG_LEVEL": "INFO"
      }
    }
  }
}
```

![Example: Claude-Desktop(3)](img/ex-screenshot-claude-desktop-001.png)

**(Option) Configure Multiple Ambari Cluster**

```json
{
  "mcpServers": {
    "Ambari-Cluster-A": {
      "command": "uvx",
      "args": ["--python", "3.11", "mcp-ambari-api"],
      "env": {
        "AMBARI_HOST": "a.foo.com",
        "AMBARI_PORT": "8080",
        "AMBARI_USER": "admin-user",
        "AMBARI_PASS": "admin-pass",
        "AMBARI_CLUSTER_NAME": "AMBARI-A",
        "MCP_LOG_LEVEL": "INFO"
      }
    },
    "Ambari-Cluster-B": {
      "command": "uvx",
      "args": ["--python", "3.11", "mcp-ambari-api"],
      "env": {
        "AMBARI_HOST": "b.bar.com",
        "AMBARI_PORT": "8080",
        "AMBARI_USER": "admin-user",
        "AMBARI_PASS": "admin-pass",
        "AMBARI_CLUSTER_NAME": "AMBARI-B",
        "MCP_LOG_LEVEL": "INFO"
      }
    }
  }
}
```

**Remote Access with Authentication (Claude Desktop):**

```json
{
  "mcpServers": {
    "ambari-api-remote": {
      "type": "streamable-http",
      "url": "http://your-server-ip:18001/mcp",
      "headers": {
        "Authorization": "Bearer your-secure-secret-key-here"
      }
    }
  }
}
```

---

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

- **User Management**: Check cluster user administration
- **Host Management**: Node registration, component assignments, and health monitoring

---

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

## 🤝 Contributing & Support

### How to Contribute

- 🐛 **Report Bugs**: [GitHub Issues](https://github.com/call518/MCP-Ambari-API/issues)
- 💡 **Request Features**: [Feature Requests](https://github.com/call518/MCP-Ambari-API/issues)  
- 🔧 **Submit PRs**: [Contributing Guidelines](https://github.com/call518/MCP-Ambari-API/blob/main/CONTRIBUTING.md)
- 📖 **Improve Docs**: Help make documentation better

### Technologies Used

- **Language**: Python 3.11
- **Framework**: Model Context Protocol (MCP)
- **API**: Apache Ambari REST API
- **Transport**: stdio (local) and streamable-http (remote)
- **Deployment**: Docker, Docker Compose, PyPI

### Dev Env.

- WSL2(networkingMode = bridged) + Docker-Desktop
  - `.wslconfig`: tested with `networkingMode = bridged`
- Python 3.11 venv

  ```bash
  ### Option-1: with uv
  uv venv --python 3.11 --seed

  ### Option-2: with pip
  python3.11 -m venv .venv
  source .venv/bin/activate
  pip install -U pip
  ```

---

## ❓ Frequently Asked Questions

### Q: What Ambari versions are supported?

**A**: Ambari 2.7+ is recommended. Earlier versions may work but are not officially tested.

### Q: Can I use this with cloud-managed Hadoop clusters?

**A**: Yes, as long as Ambari API endpoints are accessible, it works with on-premise, cloud, and hybrid deployments.

### Q: How do I troubleshoot connection issues?

**A**: Check your `AMBARI_HOST`, `AMBARI_PORT`, and network connectivity. Enable debug logging with `MCP_LOG_LEVEL=DEBUG`.

### Q: How does this compare to Ambari Web UI?

**A**: This provides programmatic access via AI/LLM commands, perfect for automation, scripting, and integration with modern DevOps workflows.

---

## Contributing

🤝 **Got ideas? Found bugs? Want to add cool features?**

We're always excited to welcome new contributors! Whether you're fixing a typo, adding a new monitoring tool, or improving documentation - every contribution makes this project better.

**Ways to contribute:**
- 🐛 Report issues or bugs
- 💡 Suggest new PostgreSQL monitoring features
- 📝 Improve documentation 
- 🚀 Submit pull requests
- ⭐ Star the repo if you find it useful!

**Pro tip:** The codebase is designed to be super friendly for adding new tools. Check out the existing `@mcp.tool()` functions in `mcp_main.py`.

---

## 📄 License

This project is licensed under the MIT License.

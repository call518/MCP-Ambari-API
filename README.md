# MCP Ambari API

> Manage and inspect Apache Ambari clusters from Claude Desktop, OpenWebUI, or any MCP client.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![PyPI](https://img.shields.io/pypi/v/MCP-Ambari-API)](https://pypi.org/project/MCP-Ambari-API/)
[![Docker Pulls](https://img.shields.io/docker/pulls/call518/mcp-server-ambari-api)](https://hub.docker.com/r/call518/mcp-server-ambari-api)

MCP Ambari API turns common Hadoop operations into MCP tools. It can inspect
cluster health, services, hosts, alerts, configurations, requests, and Ambari
Metrics data, and can perform service operations with safety guidance for
high-impact actions.

Example requests:

- “Show the current status of every service.”
- “List critical Ambari alerts and their affected hosts.”
- “Generate an HDFS capacity report.”
- “Find NameNode heap metrics available in AMS.”
- “Restart HDFS after showing me the affected components.”

## Quick start

Choose one installation method. MCPB is the shortest path for Claude Desktop;
Docker Compose provides the full OpenWebUI, MCP server, and optional MCPO stack.

<a id="claude-desktop-integration"></a>

### Claude Desktop with MCPB

Prerequisites:

- Claude Desktop for macOS or Windows with MCPB extension support
- Network access from the desktop to the Ambari server and, when used, the
  Ambari Metrics collector

1. Download `mcp-ambari-api-<version>.mcpb` from the
   [latest GitHub Release](https://github.com/call518/MCP-Ambari-API/releases/latest).
2. In Claude Desktop, open **Settings → Extensions → Advanced settings →
   Install Extension…**.
3. Select the downloaded bundle.
4. Enter the Ambari host, port, username, password, cluster name, and Metrics
   collector settings. The password is declared as a sensitive field.
5. Ask a read-only verification question such as “Show the Ambari cluster
   status.”

The bundle uses stdio transport, `uv`, and Python `3.12`; it does not expose a
listening port.
MCPB settings are stored by the desktop host and are not written into this
repository.

### OpenWebUI with Docker Compose

Prerequisites:

- Docker Engine with Docker Compose
- A reachable Ambari cluster
- An OpenWebUI model provider and a model that supports tool calling

```bash
git clone https://github.com/call518/MCP-Ambari-API.git
cd MCP-Ambari-API
cp .env.example .env
cp mcp-config.json.http mcp-config.json.http.local
chmod 600 .env mcp-config.json.http.local
```

Edit `.env` with the Ambari connection values. If remote MCP authentication is
enabled, replace `<REMOTE_SECRET_KEY>` in both `.env` and
`mcp-config.json.http.local` with the same strong secret.

```bash
docker compose up -d
docker compose ps
```

Default host endpoints:

| Service | URL | Purpose |
|---|---|---|
| OpenWebUI | `http://localhost:3001` | Chat interface |
| MCP server | `http://localhost:18001/mcp` | Direct Streamable HTTP MCP |
| MCPO | `http://localhost:8001/mcp-ambari-api/docs` | Optional OpenAPI compatibility layer |

The published ports bind to `127.0.0.1` by default. Set
`DOCKER_BIND_ADDRESS` only when remote access is required, and enable
authentication plus TLS at the network boundary before exposing the services.

#### Configure OpenWebUI

Open `http://localhost:3001`, create the administrator account, and configure a
model provider under **Settings → Admin → Connections**. For OpenAI, add a
connection with these values:

| Field | Value |
|---|---|
| URL | `https://api.openai.com/v1` |
| Auth | `Bearer` |
| API key | Your OpenAI API key |
| API Type | `Chat Completions` |

`Chat Completions` must be used with the Quick Start's default
`DEFAULT_MODEL_PARAMS={"reasoning_effort":"none"}` setting. To use an OpenAI
reasoning model with reasoning enabled instead, set `DEFAULT_MODEL_PARAMS={}`
before the first start, select `Responses`, and leave **Reasoning Effort** at
**Default** in the global, per-model, and chat settings. Mixing `Responses`
with `reasoning_effort=none`, or `Chat Completions` with another reasoning
effort, can cause tool calls to fail.

Confirm that the model appears in a new chat, then add one of the following
external tool-server connections under **Settings → Admin → Tools →
Integrations**.

**Option A: Direct MCP (recommended)**

Add a connection of type `MCP (Streamable HTTP)` using the URL visible from the
OpenWebUI container:

```text
http://mcp-server:8000/mcp
```

Use `http://localhost:18001/mcp` only from a client running on the Docker host.
Use authentication `None` unless `REMOTE_AUTH_ENABLE=true`; when authentication
is enabled, use `Bearer` with the configured `REMOTE_SECRET_KEY`.

**Option B: MCPO (OpenAPI)**

Add a connection of type `OpenAPI` with this URL:

```text
http://mcpo-proxy:8000/mcp-ambari-api
```

MCPO is not required for OpenWebUI; it remains in the standard stack for
OpenAPI-compatible clients. Use the Compose service URLs above rather than
`localhost` because OpenWebUI resolves them from inside its container.

To start without MCPO:

```bash
docker compose up -d mcp-server open-webui
```

### Other installation methods

#### PyPI with uvx

```json
{
  "mcpServers": {
    "mcp-ambari-api": {
      "command": "uvx",
      "args": ["--python", "3.12", "mcp-ambari-api"],
      "env": {
        "AMBARI_HOST": "ambari.example.com",
        "AMBARI_PORT": "8080",
        "AMBARI_USER": "<AMBARI_USER>",
        "AMBARI_PASS": "<AMBARI_PASSWORD>",
        "AMBARI_CLUSTER_NAME": "<AMBARI_CLUSTER_NAME>",
        "MCP_LOG_LEVEL": "INFO"
      }
    }
  }
}
```

#### Remote Streamable HTTP

```json
{
  "mcpServers": {
    "mcp-ambari-api": {
      "type": "streamable-http",
      "url": "https://mcp.example.com/mcp",
      "headers": {
        "Authorization": "Bearer <REMOTE_SECRET_KEY>"
      }
    }
  }
}
```

## Capabilities

- Cluster, service, component, host, request, user, and alert inspection
- Service start, stop, restart, maintenance, and configuration workflows
- HDFS `dfsadmin`-style capacity and DataNode reports
- Live Ambari Metrics metadata discovery and exact-name time-series queries
- stdio and Streamable HTTP transports
- Optional bearer authentication for Streamable HTTP

The canonical tool-selection and safety guidance is in
[`prompt_template.md`](src/mcp_ambari_api/prompt_template.md). Tool availability
can evolve, so MCP clients should use `tools/list` rather than relying on a
copied static tool list.

## Configuration

CLI arguments take precedence over environment variables, which take
precedence over defaults.

### Server settings

| Variable | Default | Description |
|---|---:|---|
| `FASTMCP_TYPE` | `stdio` | `stdio` or `streamable-http` |
| `FASTMCP_HOST` | `127.0.0.1` | HTTP bind address |
| `FASTMCP_PORT` | `8000` | HTTP listen port |
| `MCP_LOG_LEVEL` | `INFO` | Log level |
| `REMOTE_AUTH_ENABLE` | `false` | Enable HTTP bearer authentication |
| `REMOTE_SECRET_KEY` | empty | Required when authentication is enabled |

CLI equivalents are `--type`, `--host`, `--port`, `--auth-enable`, and
`--secret-key`.

### Ambari settings

| Variable | Default | Description |
|---|---:|---|
| `AMBARI_HOST` | `localhost` | Ambari server host |
| `AMBARI_PORT` | `8080` | Ambari server port |
| `AMBARI_USER` | `admin` | Ambari username |
| `AMBARI_PASS` | `admin` | Ambari password |
| `AMBARI_CLUSTER_NAME` | `c1` | Default target cluster |
| `AMBARI_METRICS_HOST` | Ambari host | Metrics collector host |
| `AMBARI_METRICS_PORT` | `6188` | Metrics collector port |
| `AMBARI_METRICS_PROTOCOL` | `http` | Metrics collector protocol |
| `AMBARI_METRICS_TIMEOUT` | `10` | Metrics request timeout in seconds |

## Metrics workflow

Ambari metric names are exact identifiers rather than natural-language labels.
Use this sequence:

1. Call `list_ambari_metric_apps` to discover valid app IDs.
2. Call `list_common_metrics_catalog` or
   `list_ambari_metrics_metadata` to find an exact metric name.
3. Call `query_ambari_metrics` with an explicit `app_id` and exact metric name.

Example:

```text
query_ambari_metrics(
  metric_names="jvm.JvmMetrics.MemHeapUsedM",
  app_id="namenode",
  duration="1h",
  group_by_host=true
)
```

## Safety and security

- Keep `.env` and `mcp-config.json.http.local` outside Git. The tracked files
  contain placeholders only.
- Use a unique, strong `REMOTE_SECRET_KEY`; never reuse an Ambari password as
  the MCP bearer token.
- Plain HTTP does not protect credentials in transit. Use a TLS reverse proxy
  for remote access.
- Keep unauthenticated development services bound to localhost.
- Review service-wide start, stop, restart, and configuration changes before
  approving them in the MCP client.

## Compatibility

- Python `3.12.x`
- MCP stdio and Streamable HTTP transports
- Claude Desktop MCPB through the UV runtime
- Docker Compose stack with OpenWebUI `0.13.3`
- Apache Ambari environments that expose the Ambari REST API; exact behavior
  can vary by Ambari and Hadoop component version

## Troubleshooting

### OpenAI reasoning model rejects tool calls

The connection's **API Type** and **Reasoning Effort** must match:

| Setup | API Type | Reasoning Effort |
|---|---|---|
| Quick Start default | `Chat Completions` | `none` |
| Reasoning with tools | `Responses` | `Default` in every scope |

The Compose example seeds the Quick Start default into OpenWebUI with:

```dotenv
DEFAULT_MODEL_PARAMS={"reasoning_effort":"none"}
```

OpenWebUI stores this value in its database on first startup. For an existing
`open-webui-data` volume, set **Reasoning Effort** to `none` in the Admin UI or
per-model settings instead. Per-chat settings can override both. Do not delete
the data volume as a troubleshooting shortcut. If using `Responses`, remove
the parameter from the global, per-model, and chat settings and leave Reasoning
Effort at `Default`. Remove the global parameter if the selected provider does
not support it.

### MCPO returns 401 Unauthorized

Check, without printing the secret itself:

1. `REMOTE_AUTH_ENABLE` in `.env`.
2. Whether `REMOTE_SECRET_KEY` is set.
3. Whether `mcp-config.json.http.local` still contains the placeholder.
4. Whether its bearer token matches the server secret.
5. Whether the MCPO container was recreated after the change.

An error emitted while cleaning up the connection can follow the initial 401;
diagnose the first HTTP error first.

### Direct MCP works but MCPO fails

These are separate client paths. Verify the direct endpoint
`http://mcp-server:8000/mcp` and the MCPO-mounted local config independently.

### Ambari connection fails

Verify host reachability from the process or container, Ambari credentials,
cluster name spelling, and the server port. `localhost` inside a container is
the container itself; use `host.docker.internal` for a service on the Docker
host.

## Development

Install and run with the existing uv project:

```bash
uv sync --dev
uv run ruff check src tests scripts
uv run python -m unittest discover -s tests -v
```

Run MCP Inspector against local source:

```bash
./run-mcp-inspector-local.sh
```

Build a local MCPB using a canonical semantic version:

```bash
scripts/build-mcpb.sh 0.0.0 /tmp/mcp-ambari-api-mcpb
unzip -l /tmp/mcp-ambari-api-mcpb/mcp-ambari-api-0.0.0.mcpb
```

Tagged releases build the wheel, source distribution, and MCPB. Publication to
TestPyPI and PyPI completes before the GitHub Release is created with the MCPB
attached.

## Contributing

Keep changes focused, add tests for behavior changes, and verify documentation
commands against the current configuration. Open an issue before making a
breaking public API or configuration change.

## License

[MIT](LICENSE)

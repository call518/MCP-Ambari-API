# Usage guide

This guide collects example requests you can send to an MCP client (Claude
Desktop, Claude Code, OpenWebUI, or another client) connected to MCP Ambari API.
Each group names the tool the request is expected to use. The client's model
chooses tools itself, so the actual tool calls can differ.

## Example queries by area

### 🔍 Cluster & Service Management

**get_cluster_info**
- "Show cluster summary and basic information."
- "What's the cluster name and version?"
- "Display cluster overview with service counts."

**get_cluster_services**
- "Show all cluster services and their current status."
- "List all services with their states."
- "Display service overview for the cluster."
- "Which services are running in the cluster?"

**get_service_status**
- "What's the status of HDFS service?"
- "Check if YARN is running properly."
- "Show current state of HBase service."
- "Is the MapReduce service healthy?"

**get_service_components**
- "Show HDFS components and which hosts they're running on."
- "List all YARN components with their host assignments."
- "Display component distribution for Kafka service."
- "Which hosts are running NameNode components?"

**get_service_details**
- "Get detailed information about HDFS service including all components."
- "Show comprehensive YARN service overview with component states."
- "Display full service details for Spark with host assignments."

### ⚙️ Service Operations

State-changing tools are named `set_*` and take `action` = `start`, `stop`, or
`restart`. The server runs in read-only mode by default, so these tools are
available only after setting `MCP_READ_ONLY=false` or passing `--read-write`.

**set_service_state**
- "Start the HDFS service." → `set_service_state("HDFS", action="start")`
- "Stop the MapReduce service." → `set_service_state("MAPREDUCE2", action="stop")`
- "Restart the YARN service." → `set_service_state("YARN", action="restart")`
- "Please restart the HBase service."

**set_all_services_state**
- "Start all cluster services." → `set_all_services_state(action="start")`
- "Stop all services in the cluster." → `set_all_services_state(action="stop")`
- "Restart all cluster services." → `set_all_services_state(action="restart")`
- ⚠️ **Warning**: These are bulk operations that affect the entire cluster.

**set_host_component_state**
- "Restart the DataNode on node03." → `set_host_component_state("node03", "DATANODE", action="restart")`
- "Stop the NodeManager on node05." → `set_host_component_state("node05", "NODEMANAGER", action="stop")`

### 📊 Operations & Monitoring

**get_active_requests**
- "Show all running operations."
- "List current service requests in progress."
- "What operations are currently active?"
- "Display ongoing cluster operations."

**get_request_status**
- "Check the status of request ID 123."
- "Show progress for operation 456."
- "Get details for the last restart request."
- "Monitor request 789 completion status."

**get_request_tasks**
- "Which hosts failed in request 10?" → `get_request_tasks("10", status_filter="FAILED")`
- "Show all unfinished tasks for operation 10." → `get_request_tasks("10", status_filter="not:COMPLETED")`
- "List tasks still running in request 5." → `get_request_tasks("5", status_filter="IN_PROGRESS")`
- "What failed on node03 during request 10?" → `get_request_tasks("10", status_filter="FAILED", host_filter="node03")`
- "Show per-host task breakdown for request 10." → `get_request_tasks("10")`
- 💡 **Tip**: Use `status_filter="not:COMPLETED"` to see remaining tasks, `status_filter="FAILED"` for failures only, and `host_filter="<hostname>"` to narrow by host.

### 🖥️ Host Management

**get_hosts**
- "List all hosts in the cluster."
- "Show cluster node inventory."
- "Display all available hosts."

**get_host_details**
- "Show detailed information for host node1.example.com."
- "Get component status on host node2.example.com."
- "Display all host details with component states."
- "Show hardware and component information for specific host."
- 💡 **Tip**: Omit hostname to get details for all hosts.

### 🔧 Configuration Management

**get_configurations**
- "Show all configuration types available."
- "Display HDFS configuration settings."
- "Get YARN resource manager configuration."
- "Show core-site.xml configuration values."
- "Find all configurations containing 'memory' settings."
- "Display summarized view of all service configurations."

### 👥 User Management

**get_users**
- "Show all cluster users."
- "List users with access to Ambari."
- "Display user accounts and their roles."

**get_user**
- "Get detailed information for user 'admin'."
- "Show profile and permissions for user 'operator'."
- "Display authentication details for specific user."

### 🚨 Alert Management

**get_alerts_history (current mode)**
- "Show current active alerts."
- "Display all current alert states."
- "List active alerts for HDFS service."
- "Show critical alerts that are currently active."

**get_alerts_history (history mode)**
- "Show alert history for the last 24 hours."
- "Display HDFS alerts from yesterday."
- "Get critical alerts from last week."
- "Show all alerts that occurred in the past month."
- "Find alerts for specific host from last 7 days."
- 💡 **Smart Time Processing**: Supports natural language time expressions in any language.

### 📈 Metrics & Trends

**get_common_metrics_catalog**
- "What NameNode metrics can I query?"
- "Search the catalog for heap usage metrics."
- "Show common metrics for the ResourceManager."
- "List NodeManager metrics containing JVM threads."
- 💡 **Tip**: use `search="heap"`, `"gc"`, etc. to narrow the catalog, then copy the exact metric names for `get_ambari_metrics`.

**get_ambari_metrics**
- "Show the last hour of NameNode heap usage." → `get_ambari_metrics(metric_names="jvm.JvmMetrics.MemHeapUsedM", app_id="namenode", duration="1h")`
- "Trend SafeMode time for the past 6 hours." → `get_ambari_metrics(metric_names="dfs.FSNamesystem.SafeModeTime", app_id="namenode", duration="6h")`
- "Compare DataNode heap usage on bigtop-hostname0.demo.local and bigtop-hostname1.demo.local over 30 minutes." → `get_ambari_metrics(metric_names="jvm.JvmMetrics.MemHeapUsedM", app_id="datanode", duration="30m", hostnames="bigtop-hostname0.demo.local,bigtop-hostname1.demo.local", group_by_host=true)`
- "Show pending YARN memory for the last day." → `get_ambari_metrics(metric_names="yarn.QueueMetrics.Queue=root.PendingMB", app_id="resourcemanager", duration="24h")`
- 💡 **Tip**: Hostnames are optional—omit them for cluster-wide stats or specify explicit hosts to focus on particular nodes. If Ambari returns no datapoints, re-check the identifiers via `/ws/v1/timeline/metrics/metadata`.

**get_hdfs_dfsadmin_report**
- "Show the HDFS dfsadmin report."
- "Summarize NameNode capacity and DataNode usage like dfsadmin."
- 💡 **Tip**: Uses AMS metrics; include `cluster_name` when monitoring multiple clusters.

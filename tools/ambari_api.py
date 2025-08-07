from typing import Dict, Optional
from mcp.server.fastmcp import FastMCP
import os
import aiohttp
import json
from base64 import b64encode
import asyncio  # Add this import at the top of the file to use asyncio.sleep
import logging
import datetime

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("AmbariService")

# =============================================================================
# Utility Functions
# =============================================================================
def format_timestamp(timestamp, is_milliseconds=True):
    """Convert timestamp to human readable format with original value in parentheses"""
    if not timestamp:
        return "N/A"
    
    try:
        # If timestamp is in milliseconds, divide by 1000
        if is_milliseconds:
            dt = datetime.datetime.fromtimestamp(timestamp / 1000, tz=datetime.timezone.utc)
        else:
            dt = datetime.datetime.fromtimestamp(timestamp, tz=datetime.timezone.utc)
        
        formatted_time = dt.strftime('%Y-%m-%d %H:%M:%S UTC')
        return f"{timestamp} ({formatted_time})"
    except (ValueError, OSError) as e:
        return f"{timestamp} (Invalid timestamp)"

async def format_single_host_details(host_name: str, cluster_name: str, show_header: bool = True) -> str:
    """
    Format detailed information for a single host.
    
    Args:
        host_name: Name of the host to retrieve details for
        cluster_name: Name of the cluster
        show_header: Whether to show the host header information
    
    Returns:
        Formatted host details string
    """
    try:
        endpoint = f"/clusters/{cluster_name}/hosts/{host_name}"
        response_data = await make_ambari_request(endpoint)

        if response_data is None or "error" in response_data:
            return f"Error: Unable to retrieve details for host '{host_name}' in cluster '{cluster_name}'."

        host_info = response_data.get("Hosts", {})
        host_components = response_data.get("host_components", [])
        metrics = response_data.get("metrics", {})

        result_lines = []
        
        if show_header:
            result_lines.extend([
                f"Host Details for '{host_name}':",
                "=" * 50
            ])
        
        # Basic host information
        result_lines.append(f"Host Name: {host_info.get('host_name', host_name)}")
        result_lines.append(f"Cluster: {host_info.get('cluster_name', cluster_name)}")
        result_lines.append(f"Host State: {host_info.get('host_state', 'Unknown')}")
        result_lines.append(f"Host Status: {host_info.get('host_status', 'Unknown')}")
        result_lines.append(f"Public Host Name: {host_info.get('public_host_name', 'N/A')}")
        result_lines.append(f"IP Address: {host_info.get('ip', 'N/A')}")
        result_lines.append(f"Maintenance State: {host_info.get('maintenance_state', 'N/A')}")
        result_lines.append(f"OS Type: {host_info.get('os_type', 'N/A')}")
        result_lines.append(f"OS Family: {host_info.get('os_family', 'N/A')}")
        result_lines.append(f"OS Architecture: {host_info.get('os_arch', 'N/A')}")
        result_lines.append(f"Rack Info: {host_info.get('rack_info', 'N/A')}")
        result_lines.append("")

        # Timing and status information
        result_lines.append("Status Information:")
        last_heartbeat = host_info.get('last_heartbeat_time', 0)
        last_registration = host_info.get('last_registration_time', 0)
        if last_heartbeat:
            result_lines.append(f"  Last Heartbeat: {format_timestamp(last_heartbeat)}")
        if last_registration:
            result_lines.append(f"  Last Registration: {format_timestamp(last_registration)}")
        
        # Health report
        health_report = host_info.get('host_health_report', '')
        if health_report:
            result_lines.append(f"  Health Report: {health_report}")
        else:
            result_lines.append(f"  Health Report: No issues reported")
        
        # Recovery information
        recovery_summary = host_info.get('recovery_summary', 'N/A')
        recovery_report = host_info.get('recovery_report', {})
        result_lines.append(f"  Recovery Status: {recovery_summary}")
        if recovery_report:
            component_reports = recovery_report.get('component_reports', [])
            result_lines.append(f"  Recovery Components: {len(component_reports)} components")
        result_lines.append("")

        # Agent environment information
        last_agent_env = host_info.get('last_agent_env', {})
        if last_agent_env:
            result_lines.append("Agent Environment:")
            
            # Host health from agent
            host_health = last_agent_env.get('hostHealth', {})
            if host_health:
                live_services = host_health.get('liveServices', [])
                active_java_procs = host_health.get('activeJavaProcs', [])
                agent_timestamp = host_health.get('agentTimeStampAtReporting', 0)
                server_timestamp = host_health.get('serverTimeStampAtReporting', 0)
                
                result_lines.append(f"  Live Services: {len(live_services)}")
                for service in live_services[:5]:  # Show first 5 services
                    svc_name = service.get('name', 'Unknown')
                    svc_status = service.get('status', 'Unknown')
                    svc_desc = service.get('desc', '')
                    result_lines.append(f"    - {svc_name}: {svc_status} {svc_desc}".strip())
                if len(live_services) > 5:
                    result_lines.append(f"    ... and {len(live_services) - 5} more services")
                
                result_lines.append(f"  Active Java Processes: {len(active_java_procs)}")
                if agent_timestamp:
                    result_lines.append(f"  Agent Timestamp: {format_timestamp(agent_timestamp)}")
                if server_timestamp:
                    result_lines.append(f"  Server Timestamp: {format_timestamp(server_timestamp)}")
            
            # System information
            umask = last_agent_env.get('umask', 'N/A')
            firewall_running = last_agent_env.get('firewallRunning', False)
            firewall_name = last_agent_env.get('firewallName', 'N/A')
            has_unlimited_jce = last_agent_env.get('hasUnlimitedJcePolicy', False)
            reverse_lookup = last_agent_env.get('reverseLookup', False)
            transparent_huge_page = last_agent_env.get('transparentHugePage', '')
            
            result_lines.append(f"  Umask: {umask}")
            result_lines.append(f"  Firewall: {firewall_name} ({'Running' if firewall_running else 'Stopped'})")
            result_lines.append(f"  JCE Policy: {'Unlimited' if has_unlimited_jce else 'Limited'}")
            result_lines.append(f"  Reverse Lookup: {'Enabled' if reverse_lookup else 'Disabled'}")
            if transparent_huge_page:
                result_lines.append(f"  Transparent Huge Page: {transparent_huge_page}")
            
            # Package and repository information
            installed_packages = last_agent_env.get('installedPackages', [])
            existing_repos = last_agent_env.get('existingRepos', [])
            existing_users = last_agent_env.get('existingUsers', [])
            alternatives = last_agent_env.get('alternatives', [])
            stack_folders = last_agent_env.get('stackFoldersAndFiles', [])
            
            result_lines.append(f"  Installed Packages: {len(installed_packages)}")
            result_lines.append(f"  Existing Repositories: {len(existing_repos)}")
            result_lines.append(f"  Existing Users: {len(existing_users)}")
            result_lines.append(f"  Alternatives: {len(alternatives)}")
            result_lines.append(f"  Stack Folders: {len(stack_folders)}")
            result_lines.append("")

        # Alerts Summary
        alerts_summary = response_data.get('alerts_summary', {})
        if alerts_summary:
            result_lines.append("Alerts Summary:")
            critical = alerts_summary.get('CRITICAL', 0)
            warning = alerts_summary.get('WARNING', 0) 
            ok = alerts_summary.get('OK', 0)
            unknown = alerts_summary.get('UNKNOWN', 0)
            maintenance = alerts_summary.get('MAINTENANCE', 0)
            total_alerts = critical + warning + ok + unknown + maintenance
            
            result_lines.append(f"  Total Alerts: {total_alerts}")
            result_lines.append(f"  Critical: {critical}")
            result_lines.append(f"  Warning: {warning}")
            result_lines.append(f"  OK: {ok}")
            result_lines.append(f"  Unknown: {unknown}")
            result_lines.append(f"  Maintenance: {maintenance}")
            result_lines.append("")

        # Performance Metrics
        if metrics:
            result_lines.append("Performance Metrics:")
            
            # Boot time
            boottime = metrics.get('boottime', 0)
            if boottime:
                boot_dt = datetime.datetime.fromtimestamp(boottime/1000, tz=datetime.timezone.utc)
                result_lines.append(f"  Boot Time: {boottime} ({boot_dt.strftime('%Y-%m-%d %H:%M:%S UTC')})")
            
            # Hardware information (CPU and Memory from metrics)
            cpu_metrics = metrics.get('cpu', {})
            if cpu_metrics:
                cpu_count = cpu_metrics.get('cpu_num', host_info.get('cpu_count', 'N/A'))
                ph_cpu_count = host_info.get('ph_cpu_count', 'N/A')
                result_lines.append(f"  CPU Count: {cpu_count} (Physical: {ph_cpu_count})")
                result_lines.append("  CPU Usage:")
                result_lines.append(f"    Idle: {cpu_metrics.get('cpu_idle', 0)}%")
                result_lines.append(f"    User: {cpu_metrics.get('cpu_user', 0)}%")
                result_lines.append(f"    System: {cpu_metrics.get('cpu_system', 0)}%")
                result_lines.append(f"    Nice: {cpu_metrics.get('cpu_nice', 0)}%")
                result_lines.append(f"    I/O Wait: {cpu_metrics.get('cpu_wio', 0)}%")
            
            # Memory metrics  
            memory_metrics = metrics.get('memory', {})
            if memory_metrics:
                mem_total = memory_metrics.get('mem_total', 0)
                mem_free = memory_metrics.get('mem_free', 0)
                mem_cached = memory_metrics.get('mem_cached', 0)
                mem_shared = memory_metrics.get('mem_shared', 0)
                swap_total = memory_metrics.get('swap_total', 0)
                swap_free = memory_metrics.get('swap_free', 0)
                
                mem_used = mem_total - mem_free
                swap_used = swap_total - swap_free
                
                result_lines.append("  Memory Usage:")
                result_lines.append(f"    Total: {mem_total/1024/1024:.1f} GB")
                result_lines.append(f"    Used: {mem_used/1024/1024:.1f} GB ({(mem_used/mem_total)*100:.1f}%)")
                result_lines.append(f"    Free: {mem_free/1024/1024:.1f} GB")
                result_lines.append(f"    Cached: {mem_cached/1024/1024:.1f} GB")
                if mem_shared > 0:
                    result_lines.append(f"    Shared: {mem_shared/1024/1024:.1f} GB")
                result_lines.append(f"    Swap Total: {swap_total/1024/1024:.1f} GB")
                result_lines.append(f"    Swap Used: {swap_used/1024/1024:.1f} GB ({(swap_used/swap_total)*100 if swap_total > 0 else 0:.1f}%)")
            
            # Load average
            load_metrics = metrics.get('load', {})
            if load_metrics:
                result_lines.append("  Load Average:")
                result_lines.append(f"    1 minute: {load_metrics.get('load_one', 0)}")
                result_lines.append(f"    5 minutes: {load_metrics.get('load_five', 0)}")
                result_lines.append(f"    15 minutes: {load_metrics.get('load_fifteen', 0)}")
            
            # Disk metrics and detailed disk information combined
            disk_metrics = metrics.get('disk', {})
            disk_info = host_info.get('disk_info', [])
            
            if disk_metrics or disk_info:
                result_lines.append("  Disk Information:")
                
                # Show I/O metrics if available
                if disk_metrics:
                    disk_total = disk_metrics.get('disk_total', 0)
                    disk_free = disk_metrics.get('disk_free', 0)
                    read_bytes = disk_metrics.get('read_bytes', 0)
                    write_bytes = disk_metrics.get('write_bytes', 0)
                    read_count = disk_metrics.get('read_count', 0)
                    write_count = disk_metrics.get('write_count', 0)
                    
                    result_lines.append(f"    Total Space: {disk_total:.1f} GB")
                    result_lines.append(f"    Free Space: {disk_free:.1f} GB")
                    result_lines.append(f"    Used Space: {disk_total - disk_free:.1f} GB ({((disk_total - disk_free)/disk_total)*100:.1f}%)")
                    result_lines.append(f"    Read: {read_bytes/1024/1024/1024:.2f} GB ({read_count:,.0f} operations)")
                    result_lines.append(f"    Write: {write_bytes/1024/1024/1024:.2f} GB ({write_count:,.0f} operations)")
                
                # Show detailed disk info if available
                if disk_info:
                    result_lines.append(f"    Disk Details ({len(disk_info)} disks):")
                    total_size = 0
                    total_used = 0
                    total_available = 0
                    
                    for i, disk in enumerate(disk_info, 1):
                        size = int(disk.get('size', 0)) if disk.get('size', '0').isdigit() else 0
                        used = int(disk.get('used', 0)) if disk.get('used', '0').isdigit() else 0
                        available = int(disk.get('available', 0)) if disk.get('available', '0').isdigit() else 0
                        
                        total_size += size
                        total_used += used
                        total_available += available
                        
                        result_lines.append(f"      Disk {i} ({disk.get('device', 'Unknown')}): {disk.get('mountpoint', 'N/A')}")
                        result_lines.append(f"        Size: {size/1024/1024:.1f} GB, Used: {used/1024/1024:.1f} GB ({disk.get('percent', 'N/A')})")
                    
                    # Summary only if multiple disks
                    if len(disk_info) > 1:
                        result_lines.append(f"      Total Summary: {total_size/1024/1024:.1f} GB total, {total_used/1024/1024:.1f} GB used")
            
            # Network metrics
            network_metrics = metrics.get('network', {})
            if network_metrics:
                result_lines.append("  Network I/O:")
                result_lines.append(f"    Bytes In: {network_metrics.get('bytes_in', 0):.2f} KB/s")
                result_lines.append(f"    Bytes Out: {network_metrics.get('bytes_out', 0):.2f} KB/s")
                result_lines.append(f"    Packets In: {network_metrics.get('pkts_in', 0):.2f} pkt/s")
                result_lines.append(f"    Packets Out: {network_metrics.get('pkts_out', 0):.2f} pkt/s")
            
            # Process metrics
            process_metrics = metrics.get('process', {})
            if process_metrics:
                result_lines.append("  Process Information:")
                result_lines.append(f"    Total Processes: {process_metrics.get('proc_total', 0)}")
                result_lines.append(f"    Running Processes: {process_metrics.get('proc_run', 0)}")
            
            result_lines.append("")
        else:
            # Fallback to basic hardware info if no metrics available
            cpu_count = host_info.get('cpu_count', 'N/A')
            ph_cpu_count = host_info.get('ph_cpu_count', 'N/A')
            total_mem_kb = host_info.get('total_mem', 0)
            if cpu_count != 'N/A' or total_mem_kb > 0:
                result_lines.append("Hardware Information:")
                if cpu_count != 'N/A':
                    result_lines.append(f"  CPU Count: {cpu_count} (Physical: {ph_cpu_count})")
                if total_mem_kb > 0:
                    total_mem_gb = total_mem_kb / 1024 / 1024
                    result_lines.append(f"  Total Memory: {total_mem_gb:.1f} GB ({total_mem_kb} KB)")
                result_lines.append("")

        # Host components
        if host_components:
            result_lines.append(f"Host Components ({len(host_components)} components):")
            
            # Group components by service for better organization
            components_by_service = {}
            for component in host_components:
                host_roles = component.get("HostRoles", {})
                comp_name = host_roles.get("component_name", "Unknown")
                service_name = host_roles.get("service_name", "Unknown")
                comp_state = host_roles.get("state", "Unknown")
                actual_configs = host_roles.get("actual_configs", {})
                
                if service_name not in components_by_service:
                    components_by_service[service_name] = []
                
                components_by_service[service_name].append({
                    "name": comp_name,
                    "state": comp_state,
                    "configs": len(actual_configs),
                    "href": component.get("href", "")
                })
            
            for service_name, components in components_by_service.items():
                result_lines.append(f"  Service: {service_name}")
                for comp in components:
                    state_indicator = "[STARTED]" if comp["state"] == "STARTED" else "[STOPPED]" if comp["state"] in ["INSTALLED", "STOPPED"] else "[UNKNOWN]"
                    result_lines.append(f"    {comp['name']} {state_indicator}")
                    if comp["configs"] > 0:
                        result_lines.append(f"      Configurations: {comp['configs']} config types")
                    result_lines.append(f"      API: {comp['href']}")
                result_lines.append("")
            
            # Summary by state
            states = {}
            for component in host_components:
                state = component.get("HostRoles", {}).get("state", "Unknown")
                states[state] = states.get(state, 0) + 1
            
            result_lines.append("  Component State Summary:")
            for state, count in states.items():
                result_lines.append(f"    {state}: {count} components")
            result_lines.append("")
        else:
            result_lines.append("Host Components: None assigned")
            result_lines.append("")

        # Kerberos Information
        kerberos_identities = response_data.get('kerberos_identities', [])
        if kerberos_identities:
            result_lines.append("Kerberos Information:")
            result_lines.append(f"  Identities: {len(kerberos_identities)} configured")
            for i, identity in enumerate(kerberos_identities[:3], 1):  # Show first 3
                result_lines.append(f"    {i}. {identity}")
            if len(kerberos_identities) > 3:
                result_lines.append(f"    ... and {len(kerberos_identities) - 3} more identities")
            result_lines.append("")
        else:
            result_lines.append("Kerberos: No identities configured")
            result_lines.append("")

        if show_header:
            result_lines.append(f"API Endpoint: {response_data.get('href', 'Not available')}")

        return "\n".join(result_lines)

    except Exception as e:
        return f"Error: Exception occurred while retrieving host details for '{host_name}' - {str(e)}"

# =============================================================================
# Server Initialization
# =============================================================================
# TODO: Change "your-server-name" to the actual server name
mcp = FastMCP("ambari-api")

# =============================================================================
# Constants
# =============================================================================
# TODO: Add necessary constants here
# Example:
# API_BASE_URL = "https://api.example.com"
# USER_AGENT = "your-app/1.0"
# DEFAULT_TIMEOUT = 30.0

# Ambari API connection information environment variable settings
# These values are retrieved from environment variables or use default values.
AMBARI_HOST = os.environ.get("AMBARI_HOST", "localhost")
AMBARI_PORT = os.environ.get("AMBARI_PORT", "8080")
AMBARI_USER = os.environ.get("AMBARI_USER", "admin")
AMBARI_PASS = os.environ.get("AMBARI_PASS", "admin")
AMBARI_CLUSTER_NAME = os.environ.get("AMBARI_CLUSTER_NAME", "c1")

# AMBARI API base URL configuration
AMBARI_API_BASE_URL = f"http://{AMBARI_HOST}:{AMBARI_PORT}/api/v1"

# =============================================================================
# Helper Functions
# =============================================================================

async def make_ambari_request(endpoint: str, method: str = "GET", data: Optional[Dict] = None) -> Dict:
    """
    Sends HTTP requests to Ambari API.
    
    Args:
        endpoint: API endpoint (e.g., "/clusters/c1/services")
        method: HTTP method (default: "GET")
        data: Request payload for PUT/POST requests
        
    Returns:
        API response data (JSON format) or {"error": "error_message"} on error
    """
    try:
        auth_string = f"{AMBARI_USER}:{AMBARI_PASS}"
        auth_bytes = auth_string.encode('ascii')
        auth_b64 = b64encode(auth_bytes).decode('ascii')
        
        headers = {
            'Authorization': f'Basic {auth_b64}',
            'Content-Type': 'application/json'
        }
        
        url = f"{AMBARI_API_BASE_URL}{endpoint}"
        
        async with aiohttp.ClientSession() as session:
            kwargs = {'headers': headers}
            if data:
                kwargs['data'] = json.dumps(data)
                
            async with session.request(method, url, **kwargs) as response:
                if response.status in [200, 202]:  # Accept both OK and Accepted
                    return await response.json()
                else:
                    error_text = await response.text()
                    return {"error": f"HTTP {response.status}: {error_text}"}
                    
    except Exception as e:
        return {"error": f"Request failed: {str(e)}"}

#-----------------------------------------------------------------------------------


@mcp.tool()
async def get_configurations(service_name: str, config_type: Optional[str] = None) -> str:
    """
    Retrieves configuration information for a specific service in an Ambari cluster.

    [Tool Role]: Dedicated tool for retrieving service configuration types and values from Ambari.

    [Core Functions]:
    - List available configuration types for a service
    - Retrieve latest configuration values for a specific type
    - Provide clear output for LLM automation and troubleshooting

    [Required Usage Scenarios]:
    - When users request service configuration details or types
    - When troubleshooting or tuning service settings
    - When users mention config type, config value, or configuration list

    Args:
        service_name: Name of the service (e.g., "HDFS", "YARN", "HBASE")
        config_type: Specific configuration type to fetch (optional)

    Returns:
        Configuration information or a list of available configuration types (success: formatted list or values, failure: English error message)
    """
    cluster_name = AMBARI_CLUSTER_NAME
    try:
        # Fetch all configuration types for the service if no specific type is provided
        if not config_type:
            endpoint = f"/clusters/{cluster_name}/configurations"
            response_data = await make_ambari_request(endpoint)

            if "error" in response_data:
                return f"Error: Unable to retrieve configurations for service '{service_name}'. {response_data['error']}"

            items = response_data.get("items", [])
            if not items:
                return f"No configurations found for service '{service_name}'."

            # Filter configuration types related to the service
            config_types = [item.get("type", "Unknown") for item in items if service_name.lower() in item.get("type", "").lower()]

            if not config_types:
                return f"No configuration types found for service '{service_name}'."

            result_lines = [f"Available configuration types for service '{service_name}':"]
            result_lines.append("=" * 50)
            for config_type in config_types:
                result_lines.append(f"- {config_type}")

            result_lines.append("\nTip: Use get_configurations again with the 'config_type' argument to fetch specific configuration values.")
            return "\n".join(result_lines)

        # Fetch the latest configuration values for the specified type
        type_endpoint = f"/clusters/{cluster_name}/configurations?type={config_type}"
        type_data = await make_ambari_request(type_endpoint)
        items = type_data.get("items", []) if type_data else []
        if not items:
            return f"No configurations found for type '{config_type}'."

        # Get the latest tag
        latest_item = items[-1]
        tag = latest_item.get("tag", "Unknown")
        version = latest_item.get("version", "Unknown")

        # Fetch configuration values for the latest tag
        config_endpoint = f"/clusters/{cluster_name}/configurations?type={config_type}&tag={tag}"
        config_data = await make_ambari_request(config_endpoint)
        config_items = config_data.get("items", []) if config_data else []
        if not config_items:
            return f"No properties found for type '{config_type}' with tag '{tag}'."

        result_lines = [f"Configuration values for type '{config_type}' (tag: {tag}, version: {version}):"]
        result_lines.append("=" * 50)

        for item in config_items:
            properties = item.get("properties", {})
            if properties:
                result_lines.append("Properties:")
                for k, v in properties.items():
                    result_lines.append(f"  {k}: {v}")
            else:
                result_lines.append("No properties found.")

            prop_attrs = item.get("properties_attributes", {})
            if prop_attrs:
                result_lines.append("Properties Attributes:")
                for attr_type, attr_map in prop_attrs.items():
                    result_lines.append(f"  [{attr_type}]")
                    for k, v in attr_map.items():
                        result_lines.append(f"    {k}: {v}")

        return "\n".join(result_lines)

    except Exception as e:
        return f"Error: Exception occurred while retrieving configurations - {str(e)}"

@mcp.tool()
async def list_configurations() -> str:
    """
    Lists all configuration types available in the cluster.

    [Tool Role]: Dedicated tool for listing all Ambari cluster configuration types.

    [Core Functions]:
    - Retrieve all configuration types present in the cluster
    - Provide formatted output for LLM automation and cluster management

    [Required Usage Scenarios]:
    - When users request cluster configuration types or overview
    - When troubleshooting or auditing cluster settings
    - When users mention config type list, cluster config, or available configs

    Returns:
        A list of all configuration types in the cluster (success: formatted list, failure: English error message)
    """
    cluster_name = AMBARI_CLUSTER_NAME
    try:
        endpoint = f"/clusters/{cluster_name}/configurations"
        response_data = await make_ambari_request(endpoint)

        if "error" in response_data:
            return f"Error: Unable to retrieve cluster configurations. {response_data['error']}"

        items = response_data.get("items", [])
        if not items:
            return f"No configurations found in cluster '{cluster_name}'."

        config_types = [item.get("type", "Unknown") for item in items]

        result_lines = ["Available configuration types in the cluster:"]
        result_lines.append("=" * 50)
        for config_type in config_types:
            result_lines.append(f"- {config_type}")

        return "\n".join(result_lines)

    except Exception as e:
        return f"Error: Exception occurred while listing cluster configurations - {str(e)}"

@mcp.tool()
async def get_cluster_info() -> str:
    """
    Retrieves basic information for an Ambari cluster.

    [Tool Role]: Dedicated tool for real-time retrieval of overall status and basic information for an Ambari cluster.

    [Core Functions]:
    - Retrieve cluster name, version, provisioning state, and security type
    - Provide formatted output for LLM automation and cluster monitoring

    [Required Usage Scenarios]:
    - When users request cluster info, status, or summary
    - When monitoring cluster health or auditing cluster properties
    - When users mention cluster overview, Ambari cluster, or cluster details

    Returns:
        Cluster basic information (success: formatted info, failure: English error message)
    """
    cluster_name = AMBARI_CLUSTER_NAME
    try:
        endpoint = f"/clusters/{cluster_name}"
        response_data = await make_ambari_request(endpoint)
        
        if "error" in response_data:
            return f"Error: Unable to retrieve information for cluster '{cluster_name}'. {response_data['error']}"
        
        cluster_info = response_data.get("Clusters", {})
        
        result_lines = [f"Information for cluster '{cluster_name}':"]
        result_lines.append("=" * 30)
        result_lines.append(f"Cluster Name: {cluster_info.get('cluster_name', cluster_name)}")
        result_lines.append(f"Version: {cluster_info.get('version', 'Unknown')}")
        
        if "provisioning_state" in cluster_info:
            result_lines.append(f"Provisioning State: {cluster_info['provisioning_state']}")
        
        if "security_type" in cluster_info:
            result_lines.append(f"Security Type: {cluster_info['security_type']}")
        
        return "\n".join(result_lines)
        
    except Exception as e:
        return f"Error: Exception occurred while retrieving cluster information - {str(e)}"

@mcp.tool()
async def get_active_requests() -> str:
    """
    Retrieves currently active (in progress) requests/operations in an Ambari cluster.
    Shows running operations, in-progress tasks, pending requests.
    
    [Tool Role]: Dedicated tool for monitoring currently running Ambari operations
    
    [Core Functions]:
    - Retrieve active/running Ambari operations (IN_PROGRESS, PENDING status)
    - Show real-time progress of ongoing operations
    - Monitor current cluster activity
    
    [Required Usage Scenarios]:
    - When users ask for "active requests", "running operations", "current requests"
    - When users ask for "request list", "operation list", "task list"
    - When users want to see "current tasks", "running tasks", "in progress operations"
    - When users mention "running", "in progress", "current activity"
    - When users ask about Ambari requests, operations, or tasks
    - When checking if any operations are currently running
    
    Returns:
        Active requests information (success: active request list, failure: error message)
    """
    cluster_name = AMBARI_CLUSTER_NAME
    try:
        # Get requests that are in progress only (remove PENDING as it may not be supported)
        endpoint = f"/clusters/{cluster_name}/requests?fields=Requests/id,Requests/request_status,Requests/request_context,Requests/start_time,Requests/progress_percent&Requests/request_status=IN_PROGRESS"
        response_data = await make_ambari_request(endpoint)
        
        if "error" in response_data:
            # If IN_PROGRESS also fails, try without status filter and filter manually
            endpoint_fallback = f"/clusters/{cluster_name}/requests?fields=Requests/id,Requests/request_status,Requests/request_context,Requests/start_time,Requests/progress_percent&sortBy=Requests/id.desc"
            response_data = await make_ambari_request(endpoint_fallback)
            
            if "error" in response_data:
                return f"Error: Unable to retrieve active requests for cluster '{cluster_name}'. {response_data['error']}"
        
        if "items" not in response_data:
            return f"No active requests found in cluster '{cluster_name}'."
        
        # Filter for active requests manually if needed
        all_requests = response_data["items"]
        active_requests = []
        
        for request in all_requests:
            request_info = request.get("Requests", {})
            status = request_info.get("request_status", "")
            if status in ["IN_PROGRESS", "PENDING", "QUEUED", "STARTED"]:
                active_requests.append(request)
        
        if not active_requests:
            return f"No active requests - All operations completed in cluster '{cluster_name}'."
        
        result_lines = [f"Active Requests for Cluster '{cluster_name}' ({len(active_requests)} running):"]
        result_lines.append("=" * 60)
        
        for i, request in enumerate(active_requests, 1):
            request_info = request.get("Requests", {})
            request_id = request_info.get("id", "Unknown")
            status = request_info.get("request_status", "Unknown")
            context = request_info.get("request_context", "No context")
            progress = request_info.get("progress_percent", 0)
            start_time = request_info.get("start_time", "Unknown")
            
            result_lines.append(f"{i}. Request ID: {request_id}")
            result_lines.append(f"   Status: {status}")
            result_lines.append(f"   Progress: {progress}%")
            result_lines.append(f"   Context: {context}")
            result_lines.append(f"   Started: {start_time}")
            result_lines.append("")
        
        result_lines.append("Tip: Use get_request_status(request_id) for detailed progress information.")
        
        return "\n".join(result_lines)
        
    except Exception as e:
        return f"Error: Exception occurred while retrieving active requests - {str(e)}"

@mcp.tool()
async def get_cluster_services() -> str:
    """
    Retrieves the list of services with status in an Ambari cluster.
    
    [Tool Role]: Dedicated tool for real-time retrieval of all running services and basic status information in an Ambari cluster
    
    [Core Functions]: 
    - Retrieve cluster service list with status via Ambari REST API
    - Provide service names, current state, and cluster information
    - Include detailed link information for each service
    - Display visual indicators for service status
    
    [Required Usage Scenarios]:
    - When users mention "service list", "cluster services", "Ambari services"
    - When cluster status check is needed
    - When service management requires current status overview
    - When real-time cluster information is absolutely necessary
    
    [Absolutely Prohibited Scenarios]:
    - General Hadoop knowledge questions
    - Service installation or configuration changes
    - Log viewing or performance monitoring
    - Requests belonging to other cluster management tools
    
    Returns:
        Cluster service list with status information (success: service list with status, failure: error message)
    """
    cluster_name = AMBARI_CLUSTER_NAME
    try:
        endpoint = f"/clusters/{cluster_name}/services?fields=ServiceInfo/service_name,ServiceInfo/state,ServiceInfo/cluster_name"
        response_data = await make_ambari_request(endpoint)
        
        if response_data is None:
            return f"Error: Unable to retrieve service list for cluster '{cluster_name}'."
        
        if "items" not in response_data:
            return f"No results: No services found in cluster '{cluster_name}'."
        
        services = response_data["items"]
        if not services:
            return f"No results: No services installed in cluster '{cluster_name}'."
        
        # Format results
        result_lines = [f"Service list for cluster '{cluster_name}' ({len(services)} services):"]
        result_lines.append("=" * 50)
        
        for i, service in enumerate(services, 1):
            service_info = service.get("ServiceInfo", {})
            service_name = service_info.get("service_name", "Unknown")
            state = service_info.get("state", "Unknown")
            service_href = service.get("href", "")
            
            result_lines.append(f"{i}. Service Name: {service_name} [{state}]")
            result_lines.append(f"   Cluster: {service_info.get('cluster_name', cluster_name)}")
            result_lines.append(f"   API Link: {service_href}")
            result_lines.append("")
        
        return "\n".join(result_lines)
        
    except Exception as e:
        return f"Error: Exception occurred while retrieving service list - {str(e)}"

@mcp.tool()
async def get_service_status(service_name: str) -> str:
    """
    Retrieves the status information for a specific service in an Ambari cluster.
    
    [Tool Role]: Dedicated tool for real-time retrieval of specific service status and state information
    
    [Core Functions]:
    - Retrieve specific service status via Ambari REST API
    - Provide detailed service state information (STARTED, STOPPED, INSTALLING, etc.)
    - Include service configuration and component information
    
    [Required Usage Scenarios]:
    - When users ask about specific service status (e.g., "HDFS status", "YARN state")
    - When troubleshooting service issues
    - When monitoring specific service health
    
    Args:
        service_name: Name of the service to check (e.g., "HDFS", "YARN", "HBASE")
    
    Returns:
        Service status information (success: detailed status, failure: error message)
    """
    cluster_name = AMBARI_CLUSTER_NAME
    try:
        endpoint = f"/clusters/{cluster_name}/services/{service_name}?fields=ServiceInfo/state,ServiceInfo/service_name,ServiceInfo/cluster_name"
        response_data = await make_ambari_request(endpoint)
        
        if response_data is None:
            return f"Error: Unable to retrieve status for service '{service_name}' in cluster '{cluster_name}'."
        
        service_info = response_data.get("ServiceInfo", {})
        
        result_lines = [f"Service Status for '{service_name}':"]
        result_lines.append("=" * 40)
        result_lines.append(f"Service Name: {service_info.get('service_name', service_name)}")
        result_lines.append(f"Cluster: {service_info.get('cluster_name', cluster_name)}")
        result_lines.append(f"Current State: {service_info.get('state', 'Unknown')}")
        
        # Add state description
        state = service_info.get('state', 'Unknown')
        state_descriptions = {
            'STARTED': 'Service is running and operational',
            'INSTALLED': 'Service is installed but not running',
            'STARTING': 'Service is in the process of starting',
            'STOPPING': 'Service is in the process of stopping',
            'INSTALLING': 'Service is being installed',
            'INSTALL_FAILED': 'Service installation failed',
            'MAINTENANCE': 'Service is in maintenance mode',
            'UNKNOWN': 'Service state cannot be determined'
        }
        
        if state in state_descriptions:
            result_lines.append(f"Description: {state_descriptions[state]}")
        
        return "\n".join(result_lines)
        
    except Exception as e:
        return f"Error: Exception occurred while retrieving service status - {str(e)}"

@mcp.tool()
async def get_service_components(service_name: str) -> str:
    """
    Retrieves detailed components information for a specific service in the Ambari cluster.

    [Tool Role]: Dedicated tool for retrieving service component details and host assignments.

    [Core Functions]:
    - List all components for a service, including state and category
    - Show host assignments and instance counts
    - Provide formatted output for LLM automation and troubleshooting

    [Required Usage Scenarios]:
    - When users request service component details or host info
    - When troubleshooting service health or scaling
    - When users mention component list, host assignments, or service breakdown

    Args:
        service_name: Name of the service (e.g., "HDFS", "YARN", "HBASE")

    Returns:
        Service components detailed information (success: formatted list, failure: English error message)
    """
    cluster_name = AMBARI_CLUSTER_NAME
    try:
        # Get detailed component information including host components
        endpoint = f"/clusters/{cluster_name}/services/{service_name}/components?fields=ServiceComponentInfo/component_name,ServiceComponentInfo/state,ServiceComponentInfo/category,ServiceComponentInfo/started_count,ServiceComponentInfo/installed_count,ServiceComponentInfo/total_count,host_components/HostRoles/host_name,host_components/HostRoles/state"
        response_data = await make_ambari_request(endpoint)
        
        if response_data is None:
            return f"Error: Unable to retrieve components for service '{service_name}' in cluster '{cluster_name}'."
        
        if "items" not in response_data:
            return f"No components found for service '{service_name}' in cluster '{cluster_name}'."
        
        components = response_data["items"]
        if not components:
            return f"No components found for service '{service_name}' in cluster '{cluster_name}'."
        
        result_lines = [f"Detailed Components for service '{service_name}':"]
        result_lines.append("=" * 60)
        result_lines.append(f"Total Components: {len(components)}")
        result_lines.append("")
        
        for i, component in enumerate(components, 1):
            comp_info = component.get("ServiceComponentInfo", {})
            comp_name = comp_info.get("component_name", "Unknown")
            comp_state = comp_info.get("state", "Unknown")
            comp_category = comp_info.get("category", "Unknown")
            
            # Component counts
            started_count = comp_info.get("started_count", 0)
            installed_count = comp_info.get("installed_count", 0)
            total_count = comp_info.get("total_count", 0)
            
            # Host components information
            host_components = component.get("host_components", [])
            
            result_lines.append(f"{i}. Component: {comp_name}")
            result_lines.append(f"   State: {comp_state}")
            result_lines.append(f"   Category: {comp_category}")
            
            # Add component state description
            state_descriptions = {
                'STARTED': 'Component is running',
                'INSTALLED': 'Component is installed but not running',
                'STARTING': 'Component is starting',
                'STOPPING': 'Component is stopping',
                'INSTALL_FAILED': 'Component installation failed',
                'MAINTENANCE': 'Component is in maintenance mode',
                'UNKNOWN': 'Component state is unknown'
            }
            
            if comp_state in state_descriptions:
                result_lines.append(f"   Description: {state_descriptions[comp_state]}")
            
            # Add instance counts if available
            if total_count > 0:
                result_lines.append(f"   Instances: {started_count} started / {installed_count} installed / {total_count} total")
            
            # Add host information
            if host_components:
                result_lines.append(f"   Hosts ({len(host_components)} instances):")
                for j, host_comp in enumerate(host_components[:5], 1):  # Show first 5 hosts
                    host_roles = host_comp.get("HostRoles", {})
                    host_name = host_roles.get("host_name", "Unknown")
                    host_state = host_roles.get("state", "Unknown")
                    result_lines.append(f"      {j}. {host_name} [{host_state}]")
                
                if len(host_components) > 5:
                    result_lines.append(f"      ... and {len(host_components) - 5} more hosts")
            else:
                result_lines.append("   Hosts: No host assignments found")
            
            result_lines.append("")
        
        # Add summary statistics
        total_instances = sum(len(comp.get("host_components", [])) for comp in components)
        started_components = len([comp for comp in components if comp.get("ServiceComponentInfo", {}).get("state") == "STARTED"])
        
        result_lines.append("Summary:")
        result_lines.append(f"  - Components: {len(components)} total, {started_components} started")
        result_lines.append(f"  - Total component instances across all hosts: {total_instances}")
        
        return "\n".join(result_lines)
        
    except Exception as e:
        return f"Error: Exception occurred while retrieving components for service '{service_name}' - {str(e)}"

@mcp.tool()
async def get_service_details(service_name: str) -> str:
    """
    Retrieves detailed status and configuration information for a specific service in the Ambari cluster.

    [Tool Role]: Dedicated tool for retrieving comprehensive service details, including state, components, and configuration.

    [Core Functions]:
    - Retrieve service state, component list, and configuration availability
    - Provide formatted output for LLM automation and troubleshooting

    [Required Usage Scenarios]:
    - When users request detailed service info or breakdown
    - When troubleshooting service health or auditing service setup
    - When users mention service details, service summary, or configuration status

    Args:
        service_name: Name of the service to check (e.g., "HDFS", "YARN", "HBASE")

    Returns:
        Detailed service information (success: comprehensive details, failure: English error message)
    """
    cluster_name = AMBARI_CLUSTER_NAME
    try:
        # First check if cluster exists
        cluster_endpoint = f"/clusters/{cluster_name}"
        cluster_response = await make_ambari_request(cluster_endpoint)
        
        if cluster_response is None:
            return f"Error: Cluster '{cluster_name}' not found or inaccessible. Please check cluster name and Ambari server connection."
        
        # Get detailed service information
        service_endpoint = f"/clusters/{cluster_name}/services/{service_name}?fields=ServiceInfo,components/ServiceComponentInfo"
        service_response = await make_ambari_request(service_endpoint)
        
        if service_response is None:
            return f"Error: Service '{service_name}' not found in cluster '{cluster_name}'. Please check service name."
        
        service_info = service_response.get("ServiceInfo", {})
        components = service_response.get("components", [])
        
        result_lines = [f"Detailed Service Information:"]
        result_lines.append("=" * 50)
        result_lines.append(f"Service Name: {service_info.get('service_name', service_name)}")
        result_lines.append(f"Cluster: {service_info.get('cluster_name', cluster_name)}")
        result_lines.append(f"Current State: {service_info.get('state', 'Unknown')}")
        
        # Add state description
        state = service_info.get('state', 'Unknown')
        state_descriptions = {
            'STARTED': 'Service is running and operational',
            'INSTALLED': 'Service is installed but not running', 
            'STARTING': 'Service is in the process of starting',
            'STOPPING': 'Service is in the process of stopping',
            'INSTALLING': 'Service is being installed',
            'INSTALL_FAILED': 'Service installation failed',
            'MAINTENANCE': 'Service is in maintenance mode',
            'UNKNOWN': 'Service state cannot be determined'
        }
        
        if state in state_descriptions:
            result_lines.append(f"Description: {state_descriptions[state]}")
        
        # Add component information
        if components:
            result_lines.append(f"\nComponents ({len(components)} total):")
            for i, component in enumerate(components, 1):
                comp_info = component.get("ServiceComponentInfo", {})
                comp_name = comp_info.get("component_name", "Unknown")
                result_lines.append(f"   {i}. {comp_name}")
        else:
            result_lines.append(f"\nComponents: No components found")
        
        # Add additional service info if available
        if "desired_configs" in service_info:
            result_lines.append(f"\nConfiguration: Available")
        
        result_lines.append(f"\nAPI Endpoint: {service_response.get('href', 'Not available')}")
        
        return "\n".join(result_lines)
        
    except Exception as e:
        return f"Error: Exception occurred while retrieving service details - {str(e)}"

@mcp.tool()
async def start_all_services() -> str:
    """
    Starts all services in an Ambari cluster (equivalent to "Start All" in Ambari Web UI).

    [Tool Role]: Dedicated tool for bulk starting all services in the cluster, automating mass startup.

    [Core Functions]:
    - Start all installed services simultaneously
    - Return request information for progress tracking
    - Provide clear success or error message for LLM automation

    [Required Usage Scenarios]:
    - When users request to "start all services", "start everything", "cluster startup"
    - When recovering cluster after maintenance or outage
    - When users mention mass startup, bulk start, or cluster bring-up

    Returns:
        Start operation result (success: request info, failure: English error message)
    """
    cluster_name = AMBARI_CLUSTER_NAME
    try:
        # First check cluster exists
        cluster_endpoint = f"/clusters/{cluster_name}"
        cluster_response = await make_ambari_request(cluster_endpoint)
        
        if cluster_response.get("error"):
            return f"Error: Cluster '{cluster_name}' not found or inaccessible. {cluster_response['error']}"
        
        # Try the standard bulk start approach first
        endpoint = f"/clusters/{cluster_name}/services"
        payload = {
            "RequestInfo": {
                "context": "Start All Services via MCP API",
                "operation_level": {
                    "level": "CLUSTER",
                    "cluster_name": cluster_name
                }
            },
            "Body": {
                "ServiceInfo": {
                    "state": "STARTED"
                }
            }
        }
        
        response_data = await make_ambari_request(endpoint, method="PUT", data=payload)
        
        if response_data.get("error"):
            # If bulk approach fails, try alternative approach
            alt_endpoint = f"/clusters/{cluster_name}/services?ServiceInfo/state=INSTALLED"
            alt_payload = {
                "ServiceInfo": {
                    "state": "STARTED"
                }
            }
            
            response_data = await make_ambari_request(alt_endpoint, method="PUT", data=alt_payload)
            
            if response_data.get("error"):
                return f"Error: Failed to start services in cluster '{cluster_name}'. {response_data['error']}"
        
        # Extract request information
        request_info = response_data.get("Requests", {})
        request_id = request_info.get("id", "Unknown")
        request_status = request_info.get("status", "Unknown")
        request_href = response_data.get("href", "")
        
        result_lines = [f"Start All Services Operation Initiated:"]
        result_lines.append("=" * 50)
        result_lines.append(f"Cluster: {cluster_name}")
        result_lines.append(f"Request ID: {request_id}")
        result_lines.append(f"Status: {request_status}")
        result_lines.append(f"Monitor URL: {request_href}")
        result_lines.append("")
        result_lines.append("Note: This operation may take several minutes to complete.")
        result_lines.append("    Use get_request_status(request_id) to track progress.")
        
        return "\n".join(result_lines)
        
    except Exception as e:
        return f"Error: Exception occurred while starting all services - {str(e)}"

@mcp.tool()
async def stop_all_services() -> str:
    """
    Stops all services in an Ambari cluster (equivalent to "Stop All" in Ambari Web UI).

    [Tool Role]: Dedicated tool for bulk stopping all services in the cluster, automating mass shutdown.

    [Core Functions]:
    - Stop all running services simultaneously
    - Return request information for progress tracking
    - Provide clear success or error message for LLM automation

    [Required Usage Scenarios]:
    - When users request to "stop all services", "stop everything", "cluster shutdown"
    - When cluster maintenance or troubleshooting requires mass shutdown
    - When users mention mass shutdown, bulk stop, or cluster halt

    Returns:
        Stop operation result (success: request info, failure: English error message)
    """
    cluster_name = AMBARI_CLUSTER_NAME
    try:
        # First, check if cluster is accessible
        cluster_endpoint = f"/clusters/{cluster_name}"
        cluster_response = await make_ambari_request(cluster_endpoint)
        
        if cluster_response.get("error"):
            return f"Error: Cluster '{cluster_name}' not found or inaccessible. {cluster_response['error']}"
        
        # Get all services that are currently STARTED
        services_endpoint = f"/clusters/{cluster_name}/services?ServiceInfo/state=STARTED"
        services_response = await make_ambari_request(services_endpoint)
        
        if services_response.get("error"):
            return f"Error retrieving services: {services_response['error']}"
        
        services = services_response.get("items", [])
        if not services:
            return "No services are currently running. All services are already stopped."
        
        # Try the standard bulk stop approach first
        stop_endpoint = f"/clusters/{cluster_name}/services"
        stop_payload = {
            "RequestInfo": {
                "context": "Stop All Services via MCP API",
                "operation_level": {
                    "level": "CLUSTER",
                    "cluster_name": cluster_name
                }
            },
            "Body": {
                "ServiceInfo": {
                    "state": "INSTALLED"
                }
            }
        }
        
        stop_response = await make_ambari_request(stop_endpoint, method="PUT", data=stop_payload)
        
        if stop_response.get("error"):
            # If bulk approach fails, try alternative approach
            alt_endpoint = f"/clusters/{cluster_name}/services?ServiceInfo/state=STARTED"
            alt_payload = {
                "ServiceInfo": {
                    "state": "INSTALLED"
                }
            }
            
            stop_response = await make_ambari_request(alt_endpoint, method="PUT", data=alt_payload)
            
            if stop_response.get("error"):
                return f"Error: Failed to stop services in cluster '{cluster_name}'. {stop_response['error']}"
        
        # Parse successful response
        request_info = stop_response.get("Requests", {})
        request_id = request_info.get("id", "Unknown")
        request_status = request_info.get("status", "Unknown")
        request_href = stop_response.get("href", "")
        
        result_lines = [
            "STOP ALL SERVICES INITIATED",
            "",
            f"Cluster: {cluster_name}",
            f"Request ID: {request_id}",
            f"Status: {request_status}",
            f"Monitor URL: {request_href}",
            "",
            "Note: This operation may take several minutes to complete.",
            "    Use get_request_status(request_id) to track progress."
        ]
        
        return "\n".join(result_lines)
        
    except Exception as e:
        return f"Error: Exception occurred while stopping all services - {str(e)}"

@mcp.tool()
async def start_service(service_name: str) -> str:
    """
    Starts a specific service in the Ambari cluster.

    [Tool Role]: Dedicated tool for automated start of Ambari services, ensuring safe and monitored startup.

    [Core Functions]:
    - Start the specified service and initiate Ambari request
    - Return request information for progress tracking
    - Provide clear success or error message for LLM automation

    [Required Usage Scenarios]:
    - When users request to "start" a service (e.g., "start HDFS", "start YARN")
    - When recovering stopped services
    - When maintenance or configuration changes require a service start
    - When users mention service start, bring up service, or automated start

    Args:
        service_name: Name of the service to start (e.g., "HDFS", "YARN", "HBASE")

    Returns:
        Start operation result (success: request info, failure: error message)
        - Success: Multi-line string with request ID, status, monitor URL, and instructions for progress tracking
        - Failure: English error message describing the problem
    """
    cluster_name = AMBARI_CLUSTER_NAME
    try:
        # Check if service exists
        service_endpoint = f"/clusters/{cluster_name}/services/{service_name}"
        service_check = await make_ambari_request(service_endpoint)
        
        if service_check.get("error"):
            return f"Error: Service '{service_name}' not found in cluster '{cluster_name}'."
        
        # Start the service
        payload = {
            "RequestInfo": {
                "context": f"Start Service {service_name} via MCP API"
            },
            "Body": {
                "ServiceInfo": {
                    "state": "STARTED"
                }
            }
        }
        
        response_data = await make_ambari_request(service_endpoint, method="PUT", data=payload)
        
        if response_data.get("error"):
            return f"Error: Failed to start service '{service_name}' in cluster '{cluster_name}'."
        
        # Extract request information
        request_info = response_data.get("Requests", {})
        request_id = request_info.get("id", "Unknown")
        request_status = request_info.get("status", "Unknown")
        request_href = response_data.get("href", "")
        
        result_lines = [
            f"START SERVICE: {service_name}",
            "",
            f"Cluster: {cluster_name}",
            f"Service: {service_name}",
            f"Request ID: {request_id}",
            f"Status: {request_status}",
            f"Monitor URL: {request_href}",
            "",
            "Use get_request_status(request_id) to track progress."
        ]
        
        return "\n".join(result_lines)
        
    except Exception as e:
        return f"Error: Exception occurred while starting service '{service_name}' - {str(e)}"

@mcp.tool()
async def stop_service(service_name: str) -> str:
    """
    Stops a specific service in the Ambari cluster.

    [Tool Role]: Dedicated tool for automated stop of Ambari services, ensuring safe and monitored shutdown.

    [Core Functions]:
    - Stop the specified service and initiate Ambari request
    - Return request information for progress tracking
    - Provide clear success or error message for LLM automation

    [Required Usage Scenarios]:
    - When users request to "stop" a service (e.g., "stop HDFS", "stop YARN")
    - When maintenance or troubleshooting requires a service shutdown
    - When users mention service stop, shutdown, or automated stop

    Args:
        service_name: Name of the service to stop (e.g., "HDFS", "YARN", "HBASE")

    Returns:
        Stop operation result (success: request info, failure: error message)
        - Success: Multi-line string with request ID, status, monitor URL, and instructions for progress tracking
        - Failure: English error message describing the problem
    """
    cluster_name = AMBARI_CLUSTER_NAME
    try:
        # Check if service exists
        service_endpoint = f"/clusters/{cluster_name}/services/{service_name}"
        service_check = await make_ambari_request(service_endpoint)
        
        if service_check.get("error"):
            return f"Error: Service '{service_name}' not found in cluster '{cluster_name}'."
        
        # Stop the service (set state to INSTALLED)
        payload = {
            "RequestInfo": {
                "context": f"Stop Service {service_name} via MCP API"
            },
            "Body": {
                "ServiceInfo": {
                    "state": "INSTALLED"
                }
            }
        }
        
        response_data = await make_ambari_request(service_endpoint, method="PUT", data=payload)
        
        if response_data.get("error"):
            return f"Error: Failed to stop service '{service_name}' in cluster '{cluster_name}'."
        
        # Extract request information
        request_info = response_data.get("Requests", {})
        request_id = request_info.get("id", "Unknown")
        request_status = request_info.get("status", "Unknown")
        request_href = response_data.get("href", "")
        
        result_lines = [
            f"STOP SERVICE: {service_name}",
            "",
            f"Cluster: {cluster_name}",
            f"Service: {service_name}",
            f"Request ID: {request_id}",
            f"Status: {request_status}",
            f"Monitor URL: {request_href}",
            "",
            "Use get_request_status(request_id) to track progress."
        ]
        
        return "\n".join(result_lines)
        
    except Exception as e:
        return f"Error: Exception occurred while stopping service '{service_name}' - {str(e)}"

@mcp.tool()
async def get_request_status(request_id: str) -> str:
    """
    Retrieves the status and progress of a specific Ambari request operation.
    
    [Tool Role]: Dedicated tool for real-time tracking and reporting of Ambari request status.
    
    [Core Functions]:
    - Query the status, progress, and context of a request by its ID
    - Provide detailed status (PENDING, IN_PROGRESS, COMPLETED, FAILED, etc.)
    - Show progress percentage and timing information
    - Return actionable status for automation and LLM integration
    
    [Required Usage Scenarios]:
    - When users ask for the status or progress of a specific operation/request
    - When monitoring or troubleshooting Ambari operations
    - When tracking bulk or individual service actions
    - When users mention request ID, operation status, or progress
    
    Args:
        request_id: ID of the Ambari request to check (int)
    
    Returns:
        Request status information (success: detailed status and progress, failure: error message)
        - Success: Multi-line string with request ID, status, progress, context, start/end time, and status description
        - Failure: English error message describing the problem
    """
    cluster_name = AMBARI_CLUSTER_NAME
    try:
        endpoint = f"/clusters/{cluster_name}/requests/{request_id}"
        response_data = await make_ambari_request(endpoint)
        
        if response_data.get("error"):
            return f"Error: Request '{request_id}' not found in cluster '{cluster_name}'."
        
        request_info = response_data.get("Requests", {})
        
        result_lines = [
            f"REQUEST STATUS: {request_id}",
            "",
            f"Cluster: {cluster_name}",
            f"Request ID: {request_info.get('id', request_id)}",
            f"Status: {request_info.get('request_status', 'Unknown')}",
            f"Progress: {request_info.get('progress_percent', 0)}%"
        ]
        
        if "request_context" in request_info:
            result_lines.append(f"Context: {request_info['request_context']}")
        
        if "start_time" in request_info:
            result_lines.append(f"Start Time: {request_info['start_time']}")
        
        if "end_time" in request_info:
            result_lines.append(f"End Time: {request_info['end_time']}")
        
        # Add status explanation
        status = request_info.get('request_status', 'Unknown')
        status_descriptions = {
            'PENDING': 'Request is pending execution',
            'IN_PROGRESS': 'Request is currently running',
            'COMPLETED': 'Request completed successfully',
            'FAILED': 'Request failed',
            'ABORTED': 'Request was aborted',
            'TIMEDOUT': 'Request timed out'
        }
        
        if status in status_descriptions:
            result_lines.append(f"Description: {status_descriptions[status]}")
        
        return "\n".join(result_lines)
        
    except Exception as e:
        return f"Error: Exception occurred while retrieving request status - {str(e)}"

@mcp.tool()
async def restart_service(service_name: str) -> str:
    """
    Restarts a specific service in an Ambari cluster (stop then start).

    [Tool Role]: Dedicated tool for automated restart of Ambari services, ensuring safe stop and start sequence.

    [Core Functions]:
    - Stop the specified service and wait for completion
    - Start the service and wait for completion
    - Return clear success or error message for LLM automation

    [Required Usage Scenarios]:
    - When users request to "restart" a service (e.g., "restart HDFS", "restart YARN")
    - When troubleshooting or recovering service issues
    - When maintenance or configuration changes require a restart
    - When users mention service restart, safe restart, or automated restart

    Args:
        service_name: Name of the service to restart (e.g., "HDFS", "YARN")

    Returns:
        Restart operation result (success: English completion message, failure: English error message)
        - Success: "Service '<service_name>' restart operation completed successfully."
        - Failure: "Error: ..." with details
    """
    cluster_name = AMBARI_CLUSTER_NAME

    try:
        # Step 1: Stop the service
        logger.info("Stopping service '%s'...", service_name)
        stop_endpoint = f"/clusters/{cluster_name}/services/{service_name}"
        stop_payload = {
            "RequestInfo": {
                "context": f"Stop {service_name} service via MCP API",
                "operation_level": {
                    "level": "SERVICE",
                    "cluster_name": cluster_name,
                    "service_name": service_name
                }
            },
            "Body": {
                "ServiceInfo": {
                    "state": "INSTALLED"
                }
            }
        }

        stop_response = await make_ambari_request(stop_endpoint, method="PUT", data=stop_payload)

        if "error" in stop_response:
            return f"Error: Unable to stop service '{service_name}'. {stop_response['error']}"

        stop_request_id = stop_response.get("Requests", {}).get("id", "Unknown")
        if stop_request_id == "Unknown":
            return f"Error: Failed to retrieve stop request ID for service '{service_name}'."

        # Step 2: Wait for the stop operation to complete (print progress only for stop)
        while True:
            status_endpoint = f"/clusters/{cluster_name}/requests/{stop_request_id}"
            status_response = await make_ambari_request(status_endpoint)

            if "error" in status_response:
                return f"Error: Unable to check status of stop operation for service '{service_name}'. {status_response['error']}"

            request_status = status_response.get("Requests", {}).get("request_status", "Unknown")
            progress_percent = status_response.get("Requests", {}).get("progress_percent", 0)

            if request_status == "COMPLETED":
                break
            elif request_status in ["FAILED", "ABORTED"]:
                return f"Error: Stop operation for service '{service_name}' failed with status '{request_status}'."

            logger.info("Stopping service '%s'... Progress: %d%%", service_name, progress_percent)
            await asyncio.sleep(1)  # Wait for 5 seconds before checking again

        # Step 3: Start the service (no progress output, fire and forget)
        start_endpoint = f"/clusters/{cluster_name}/services/{service_name}"
        start_payload = {
            "RequestInfo": {
                "context": f"Start {service_name} service via MCP API",
                "operation_level": {
                    "level": "SERVICE",
                    "cluster_name": cluster_name,
                    "service_name": service_name
                }
            },
            "Body": {
                "ServiceInfo": {
                    "state": "STARTED"
                }
            }
        }

        start_response = await make_ambari_request(start_endpoint, method="PUT", data=start_payload)

        if "error" in start_response:
            return f"Error: Unable to start service '{service_name}'. {start_response['error']}"

        # No need to wait for start completion or print progress
        logger.info("Service '%s' successfully restarted.", service_name)
        return f"Service '{service_name}' restart operation completed successfully."

    except Exception as e:
        logger.error("Error occurred while restarting service '%s': %s", service_name, str(e))
        return f"Error: Service '{service_name}' restart operation failed: {str(e)}"

@mcp.tool()
async def restart_all_services() -> str:
    """
    Restarts all services in the Ambari cluster (stop all, then start all).

    [Tool Role]: Dedicated tool for automated bulk restart of all Ambari services, ensuring safe stop and start sequence.

    [Core Functions]:
    - Stop all running services and wait for completion
    - Start all services and wait for completion
    - Return clear success or error message for LLM automation

    [Required Usage Scenarios]:
    - When users request to "restart all services", "bulk restart", "cluster-wide restart"
    - When troubleshooting or recovering cluster-wide issues
    - When maintenance or configuration changes require a full restart

    Returns:
        Bulk restart operation result (success: English completion message, failure: English error message)
        - Success: "All services restart operation completed successfully."
        - Failure: "Error: ..." with details
    """
    cluster_name = AMBARI_CLUSTER_NAME
    try:
        # Step 1: Stop all services
        stop_result = await stop_all_services()
        if stop_result.startswith("Error"):
            return f"Error: Unable to stop all services. {stop_result}"

        # Extract stop request ID
        lines = stop_result.splitlines()
        stop_request_id = None
        for line in lines:
            if line.startswith("Request ID:"):
                stop_request_id = line.split(":", 1)[1].strip()
                break
        if not stop_request_id or stop_request_id == "Unknown":
            return f"Error: Failed to retrieve stop request ID for all services."

        # Wait for stop operation to complete (no progress output)
        while True:
            status_result = await get_request_status(stop_request_id)
            if status_result.startswith("Error"):
                return f"Error: Unable to check status of stop operation for all services. {status_result}"
            if "Status: COMPLETED" in status_result:
                break
            elif "Status: FAILED" in status_result or "Status: ABORTED" in status_result:
                return f"Error: Stop operation for all services failed. {status_result}"
            await asyncio.sleep(1)

        # Step 2: Start all services (no progress output, fire and forget)
        start_result = await start_all_services()
        if start_result.startswith("Error"):
            return f"Error: Unable to start all services. {start_result}"

        # No need to wait for start completion or print progress
        return "All services restart operation completed successfully."

    except Exception as e:
        return f"Error: All services restart operation failed: {str(e)}"

@mcp.tool()
async def list_hosts() -> str:
    """
    Retrieves the list of hosts in the Ambari cluster.

    [Tool Role]: Dedicated tool for listing all hosts registered in the Ambari cluster.

    [Core Functions]:
    - Query Ambari REST API for host list
    - Return host names and API links
    - Provide formatted output for LLM automation and cluster management

    [Required Usage Scenarios]:
    - When users request cluster host list or host details
    - When auditing or monitoring cluster nodes

    Returns:
        List of hosts (success: formatted list, failure: error message)
    """
    cluster_name = AMBARI_CLUSTER_NAME
    try:
        endpoint = f"/clusters/{cluster_name}/hosts"
        response_data = await make_ambari_request(endpoint)

        if response_data is None or "items" not in response_data:
            return f"Error: Unable to retrieve hosts for cluster '{cluster_name}'."

        hosts = response_data["items"]
        if not hosts:
            return f"No hosts found in cluster '{cluster_name}'."

        result_lines = [f"Host list for cluster '{cluster_name}' ({len(hosts)} hosts):"]
        result_lines.append("=" * 50)

        for i, host in enumerate(hosts, 1):
            host_info = host.get("Hosts", {})
            host_name = host_info.get("host_name", "Unknown")
            host_href = host.get("href", "")
            result_lines.append(f"{i}. Host Name: {host_name}")
            result_lines.append(f"   API Link: {host_href}")
            result_lines.append("")

        return "\n".join(result_lines)

    except Exception as e:
        return f"Error: Exception occurred while retrieving hosts - {str(e)}"

@mcp.tool()
async def get_host_details(host_name: Optional[str] = None) -> str:
    """
    Retrieves detailed information for a specific host or all hosts in the Ambari cluster.

    [Tool Role]: Dedicated tool for retrieving comprehensive host details including metrics, hardware info, and components.

    [Core Functions]:
    - If host_name provided: Query specific host information
    - If host_name not provided: Query all hosts and their detailed information
    - Return host hardware specs, state, metrics, and assigned components
    - Provide formatted output for LLM automation and cluster management

    [Required Usage Scenarios]:
    - When users request specific host details or host status
    - When users request all hosts details or cluster-wide host information
    - When auditing or monitoring individual or all cluster nodes
    - When troubleshooting host-specific issues

    Args:
        host_name: Name of the specific host to retrieve details for (optional, e.g., "bigtop-hostname0.demo.local")

    Returns:
        Detailed host information (success: formatted details, failure: error message)
    """
    cluster_name = AMBARI_CLUSTER_NAME
    try:
        # Single host mode
        if host_name is not None:
            return await format_single_host_details(host_name, cluster_name, show_header=True)
        
        # Multi-host mode (all hosts)
        hosts_endpoint = f"/clusters/{cluster_name}/hosts"
        hosts_response = await make_ambari_request(hosts_endpoint)

        if hosts_response is None or "items" not in hosts_response:
            return f"Error: Unable to retrieve host list for cluster '{cluster_name}'."

        hosts = hosts_response["items"]
        if not hosts:
            return f"No hosts found in cluster '{cluster_name}'."

        result_lines = [
            f"Detailed Information for All Hosts in Cluster '{cluster_name}' ({len(hosts)} hosts):",
            "=" * 80,
            ""
        ]

        # Process each host
        for i, host in enumerate(hosts, 1):
            host_info = host.get("Hosts", {})
            current_host_name = host_info.get("host_name", "Unknown")
            
            result_lines.append(f"[{i}/{len(hosts)}] HOST: {current_host_name}")
            result_lines.append("-" * 60)

            # Get formatted details for this host
            host_details = await format_single_host_details(current_host_name, cluster_name, show_header=False)
            
            if host_details.startswith("Error:"):
                result_lines.append(f"Error: Unable to retrieve details for host '{current_host_name}'")
            else:
                result_lines.append(host_details)
            
            result_lines.append("")

        # Summary
        result_lines.extend([
            "SUMMARY:",
            f"Total Hosts: {len(hosts)}"
        ])
        
        return "\n".join(result_lines)

    except Exception as e:
        return f"Error: Exception occurred while retrieving host details - {str(e)}"

# =============================================================================
# Server Execution
# =============================================================================

def main():
    """
    Entrypoint for MCP Ambari API server.
    """
    mcp.run(transport='stdio')

if __name__ == "__main__":
    main()

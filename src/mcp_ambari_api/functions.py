"""
Utility functions for Ambari API operations.
This module contains helper functions used by the main Ambari API tools.
"""

import os
import aiohttp
import json
import datetime
import logging
import time
from datetime import timedelta
from typing import Dict, Optional
from base64 import b64encode
from functools import wraps

# Set up logging
logger = logging.getLogger("AmbariService")

# -----------------------------------------------------------------------------
# Decorator for uniform tool call logging
# -----------------------------------------------------------------------------
def log_tool(func):
    """Decorator for uniform tool call logging with timing and result categorization."""
    tool_name = func.__name__

    @wraps(func)
    async def wrapper(*args, **kwargs):
        start = time.monotonic()
        # Avoid logging huge argument content; simple key=... pairs
        try:
            arg_preview = []
            if kwargs:
                for k, v in kwargs.items():
                    if v is None:
                        continue
                    sv = str(v)
                    if len(sv) > 120:
                        sv = sv[:117] + '…'
                    arg_preview.append(f"{k}={sv}")
            logger.info(f"TOOL START {tool_name} {' '.join(arg_preview)}")
            result = await func(*args, **kwargs)
            duration_ms = (time.monotonic() - start) * 1000
            # Categorize result
            if isinstance(result, str) and result.startswith("Error:"):
                logger.warning(f"TOOL ERROR_RETURN {tool_name} took={duration_ms:.1f}ms len={len(result)}")
            elif isinstance(result, str) and result.startswith("[ERROR]"):
                logger.warning(f"TOOL ERROR_RETURN {tool_name} took={duration_ms:.1f}ms len={len(result)}")
            else:
                logger.info(f"TOOL SUCCESS {tool_name} took={duration_ms:.1f}ms len={len(result) if hasattr(result,'__len__') else 'NA'}")
            return result
        except Exception:
            duration_ms = (time.monotonic() - start) * 1000
            logger.exception(f"TOOL EXCEPTION {tool_name} failed after {duration_ms:.1f}ms")
            raise

    return wrapper

# Ambari API connection information environment variable settings
AMBARI_HOST = os.environ.get("AMBARI_HOST", "localhost")
AMBARI_PORT = os.environ.get("AMBARI_PORT", "8080")
AMBARI_USER = os.environ.get("AMBARI_USER", "admin")
AMBARI_PASS = os.environ.get("AMBARI_PASS", "admin")
AMBARI_CLUSTER_NAME = os.environ.get("AMBARI_CLUSTER_NAME", "c1")

# AMBARI API base URL configuration
AMBARI_API_BASE_URL = f"http://{AMBARI_HOST}:{AMBARI_PORT}/api/v1"


def format_timestamp(timestamp, is_milliseconds=True):
    """Convert timestamp to human readable format with original value in parentheses"""
    if not timestamp:
        return "N/A"
    
    try:
        # Handle string timestamps by converting to int first
        if isinstance(timestamp, str):
            try:
                timestamp = int(timestamp)
            except ValueError:
                return f"{timestamp} (Invalid timestamp format)"
        
        # If timestamp is in milliseconds, divide by 1000
        if is_milliseconds:
            dt = datetime.datetime.fromtimestamp(timestamp / 1000, tz=datetime.timezone.utc)
        else:
            dt = datetime.datetime.fromtimestamp(timestamp, tz=datetime.timezone.utc)
        
        formatted_time = dt.strftime('%Y-%m-%d %H:%M:%S UTC')
        return f"{timestamp} ({formatted_time})"
    except (ValueError, OSError, TypeError) as e:
        return f"{timestamp} (Invalid timestamp)"


def safe_timestamp_compare(timestamp, threshold, operator='>='):
    """
    Safe timestamp comparison handling both str and int types.
    
    Args:
        timestamp: The timestamp to compare (can be str or int)
        threshold: The threshold to compare against (can be str or int)  
        operator: Comparison operator ('>', '>=', '<', '<=')
    
    Returns:
        bool: Result of comparison, False if conversion fails
    """
    try:
        # Convert string to int if needed
        if isinstance(timestamp, str):
            timestamp = int(timestamp)
        if isinstance(threshold, str):
            threshold = int(threshold)
            
        if operator == '>':
            return timestamp > threshold
        elif operator == '>=':
            return timestamp >= threshold
        elif operator == '<':
            return timestamp < threshold
        elif operator == '<=':
            return timestamp <= threshold
        else:
            return False
    except (ValueError, TypeError):
        return False


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
    start = time.monotonic()
    logger.debug(f"AMBARI_REQ start method={method} endpoint={endpoint} payload_keys={list(data.keys()) if data else []}")
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
                elapsed = (time.monotonic() - start) * 1000
                if response.status in [200, 202]:  # Accept both OK and Accepted
                    try:
                        js = await response.json()
                    except Exception as je:
                        text_body = await response.text()
                        logger.warning(f"AMBARI_REQ json-parse-fallback status={response.status} took={elapsed:.1f}ms endpoint={endpoint} err={je}")
                        return {"error": f"JSON_PARSE: {je}", "raw": text_body}
                    size_hint = len(str(js)) if js else 0
                    logger.debug(f"AMBARI_REQ success status={response.status} took={elapsed:.1f}ms size={size_hint}")
                    return js
                else:
                    error_text = await response.text()
                    logger.warning(f"AMBARI_REQ http-error status={response.status} took={elapsed:.1f}ms endpoint={endpoint} body_len={len(error_text)}")
                    return {"error": f"HTTP {response.status}: {error_text}"}
                    
    except Exception as e:
        elapsed = (time.monotonic() - start) * 1000
        logger.exception(f"AMBARI_REQ exception took={elapsed:.1f}ms endpoint={endpoint}")
        return {"error": f"Request failed: {str(e)}"}


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
        # Include host component states and service names in the request
        endpoint = f"/clusters/{cluster_name}/hosts/{host_name}?fields=Hosts,host_components/HostRoles/state,host_components/HostRoles/service_name,host_components/HostRoles/component_name,host_components/HostRoles/actual_configs,metrics,alerts_summary,kerberos_identities"
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


# -----------------------------------------------------------------------------
# Alert formatting utility functions
# -----------------------------------------------------------------------------

def format_alerts_output(items, mode, cluster, format_type, host_name, service_name, state_filter, **kwargs):
    """
    Unified alert output formatting function for both current alerts and alert history.
    
    Args:
        items: List of alert items from API response
        mode: "current" or "history"
        cluster: Cluster name
        format_type: "detailed", "summary", "compact", etc.
        host_name: Optional host name filter
        service_name: Optional service name filter  
        state_filter: Optional state filter
        **kwargs: Additional parameters (limit, from_timestamp, to_timestamp, etc.)
    
    Returns:
        Formatted string output
    """
    if not items:
        scope_desc = f"host '{host_name}'" if host_name else f"service '{service_name}'" if service_name else f"cluster '{cluster}'"
        return f"No {mode} alerts found for {scope_desc}"
    
    # Common header
    scope = f"host '{host_name}'" if host_name else f"service '{service_name}'" if service_name else f"cluster '{cluster}'"
    title = "Current Alerts" if mode == "current" else "Alert History"
    
    result_lines = [
        f"{title} for {scope}",
        "=" * 60,
        f"Found {len(items)} alerts"
    ]
    
    # Add filter information if any
    filters = []
    if state_filter:
        filters.append(f"State: {state_filter}")
    if kwargs.get('definition_name'):
        filters.append(f"Definition: {kwargs['definition_name']}")
    if mode == "current" and kwargs.get('maintenance_state'):
        filters.append(f"Maintenance: {kwargs['maintenance_state']}")
    if mode == "history":
        if kwargs.get('from_timestamp'):
            filters.append(f"From: {format_timestamp(kwargs['from_timestamp'])}")
        if kwargs.get('to_timestamp'):
            filters.append(f"To: {format_timestamp(kwargs['to_timestamp'])}")
    
    if filters:
        result_lines.append(f"Filters: {', '.join(filters)}")
    
    result_lines.append("")
    
    # Mode-specific field mapping
    field_prefix = "Alert" if mode == "current" else "AlertHistory"
    timestamp_field = "latest_timestamp" if mode == "current" else "timestamp"
    
    # Format based on type
    if format_type == "summary":
        result_lines.extend(format_alerts_summary(items, mode, field_prefix))
    elif format_type == "compact":
        result_lines.extend(format_alerts_compact(items, field_prefix, timestamp_field, mode, kwargs.get('limit')))
    else:  # detailed
        result_lines.extend(format_alerts_detailed(items, field_prefix, timestamp_field, mode, kwargs.get('limit')))
    
    return "\n".join(result_lines)


def format_alerts_summary(items, mode, field_prefix):
    """Format alerts in summary mode - grouped by state and definition."""
    result_lines = []
    
    # Group by state and definition
    state_counts = {}
    definition_counts = {}
    service_counts = {}
    
    for item in items:
        alert_data = item.get(field_prefix, {})
        state = alert_data.get("state", "UNKNOWN")
        definition = alert_data.get("definition_name", "Unknown")
        service = alert_data.get("service_name", "Unknown")
        
        state_counts[state] = state_counts.get(state, 0) + 1
        definition_counts[definition] = definition_counts.get(definition, 0) + 1
        service_counts[service] = service_counts.get(service, 0) + 1
    
    result_lines.append("Summary by State:")
    for state in ["CRITICAL", "WARNING", "OK", "UNKNOWN"]:
        count = state_counts.get(state, 0)
        if count > 0:
            result_lines.append(f"  {state}: {count}")
    
    result_lines.append("\nTop Alert Definitions:")
    sorted_definitions = sorted(definition_counts.items(), key=lambda x: x[1], reverse=True)[:10]
    for definition, count in sorted_definitions:
        result_lines.append(f"  {definition}: {count}")
    
    result_lines.append("\nTop Services:")
    sorted_services = sorted(service_counts.items(), key=lambda x: x[1], reverse=True)[:10]
    for service, count in sorted_services:
        result_lines.append(f"  {service}: {count}")
    
    return result_lines


def format_alerts_compact(items, field_prefix, timestamp_field, mode, limit=None):
    """Format alerts in compact mode - one line per alert."""
    result_lines = []
    
    # Treat limit=0 as no limit
    if limit == 0:
        limit = None

    if mode == "current":
        result_lines.append("Current Alerts (compact):")
        result_lines.append("State     | Maint | Service     | Host                    | Definition")
        result_lines.append("-" * 85)
        
        for item in items:
            alert = item.get(field_prefix, {})
            state = alert.get("state", "UNKNOWN")
            maintenance = alert.get("maintenance_state", "OFF")
            service = alert.get("service_name", "N/A")
            host = alert.get("host_name", "N/A")
            definition = alert.get("definition_name", "Unknown")
            
            state_padded = state.ljust(9)
            maint_padded = maintenance[:5].ljust(5)
            service_padded = service[:11].ljust(11)
            host_padded = host[:23].ljust(23)
            definition_short = definition[:25] + "..." if len(definition) > 25 else definition
            
            result_lines.append(f"{state_padded} | {maint_padded} | {service_padded} | {host_padded} | {definition_short}")
    
    else:  # history
        result_lines.append("Alert History Entries (compact):")
        result_lines.append("Timestamp                | State     | Service     | Host                    | Definition")
        result_lines.append("-" * 100)
        
        count = 0
        for item in items:
            alert = item.get(field_prefix, {})
            timestamp = alert.get(timestamp_field, 0)
            state = alert.get("state", "UNKNOWN")
            service = alert.get("service_name", "N/A")
            host = alert.get("host_name", "N/A")
            definition = alert.get("definition_name", "Unknown")
            
            time_formatted = format_timestamp(timestamp)
            time_str = time_formatted.split(" (")[1].rstrip(")") if " (" in time_formatted else time_formatted
            state_padded = state.ljust(9)
            service_padded = service[:11].ljust(11)
            host_padded = host[:23].ljust(23)
            definition_short = definition[:40] + "..." if len(definition) > 40 else definition
            
            result_lines.append(f"{time_str} | {state_padded} | {service_padded} | {host_padded} | {definition_short}")
            
            count += 1
            if limit and count >= limit:
                result_lines.append(f"... (showing first {limit} entries)")
                break
    
    return result_lines


def format_alerts_detailed(items, field_prefix, timestamp_field, mode, limit=None):
    """Format alerts in detailed mode - full information per alert."""
    result_lines = []
    
    # Treat limit=0 as no limit
    if limit == 0:
        limit = None
    
    if mode == "current":
        result_lines.append("Current Alerts (detailed):")
        result_lines.append("")
        
        # Group by state for better organization
        alerts_by_state = {"CRITICAL": [], "WARNING": [], "UNKNOWN": [], "OK": []}
        
        for item in items:
            alert = item.get(field_prefix, {})
            state = alert.get("state", "UNKNOWN")
            if state not in alerts_by_state:
                alerts_by_state[state] = []
            alerts_by_state[state].append(item)
        
        count = 0
        for state in ["CRITICAL", "WARNING", "UNKNOWN", "OK"]:
            alerts = alerts_by_state.get(state, [])
            if not alerts:
                continue
            
            if count > 0:
                result_lines.append("")
            
            result_lines.append(f"=== {state} ALERTS ({len(alerts)}) ===")
            result_lines.append("")
            
            for item in alerts:
                alert = item.get(field_prefix, {})
                count += 1
                result_lines.extend(format_single_alert_detailed(alert, count, mode, timestamp_field))
                result_lines.append("")
                
                if limit and count >= limit:
                    result_lines.append(f"... (showing first {limit} entries)")
                    break
            
            if limit and count >= limit:
                break
    
    else:  # history
        result_lines.append("Alert History Entries (detailed):")
        result_lines.append("")
        
        count = 0
        for item in items:
            alert = item.get(field_prefix, {})
            count += 1
            result_lines.extend(format_single_alert_detailed(alert, count, mode, timestamp_field))
            result_lines.append("")
            
            if limit and count >= limit:
                result_lines.append(f"... (showing first {limit} entries)")
                break
    
    return result_lines


def format_single_alert_detailed(alert, count, mode, timestamp_field):
    """Format a single alert in detailed view."""
    result_lines = []
    
    # Basic information
    alert_id = alert.get("id", "Unknown")
    state = alert.get("state", "UNKNOWN")
    definition_name = alert.get("definition_name", "Unknown")
    definition_id = alert.get("definition_id", "Unknown")
    service_name = alert.get("service_name", "Unknown")
    component_name = alert.get("component_name", "Unknown")
    host_name = alert.get("host_name", "N/A")
    label = alert.get("label", "No label")
    text = alert.get("text", "No description")
    instance = alert.get("instance", None)
    
    result_lines.extend([
        f"[{count}] Alert ID: {alert_id}",
        f"    State: {state}",
        f"    Service: {service_name}",
        f"    Component: {component_name}",
        f"    Host: {host_name}",
        f"    Definition: {definition_name} (ID: {definition_id})",
        f"    Label: {label}",
    ])
    
    if instance:
        result_lines.append(f"    Instance: {instance}")
    
    # Mode-specific fields
    if mode == "current":
        maintenance_state = alert.get("maintenance_state", "OFF")
        scope = alert.get("scope", "Unknown")
        result_lines.append(f"    Maintenance: {maintenance_state}")
        result_lines.append(f"    Scope: {scope}")
        
        # Timestamps for current alerts
        latest_timestamp = alert.get("latest_timestamp", 0)
        original_timestamp = alert.get("original_timestamp", 0)
        
        if latest_timestamp:
            result_lines.append(f"    Latest Update: {format_timestamp(latest_timestamp)}")
        if original_timestamp and original_timestamp != latest_timestamp:
            result_lines.append(f"    First Occurrence: {format_timestamp(original_timestamp)}")
    
    else:  # history
        timestamp = alert.get(timestamp_field, 0)
        if timestamp:
            result_lines.append(f"    Timestamp: {format_timestamp(timestamp)}")
    
    # Format alert text
    if text:
        if "\n" in text:
            result_lines.append("    Text:")
            for line in text.split("\n"):
                result_lines.append(f"      {line}")
        else:
            text_display = text if len(text) <= 100 else text[:97] + "..."
            result_lines.append(f"    Text: {text_display}")
    
    return result_lines


def get_current_time_context() -> str:
    """
    Returns the current time context for accurate relative date calculations.
    
    This utility function provides current date and time information for reference 
    in timestamp calculations.
    
    Returns:
        Current date/time context with calculation examples (success: formatted context info, failure: error message)
    """
    try:
        current_time = datetime.datetime.now(datetime.timezone.utc)
        current_date_str = current_time.strftime('%Y-%m-%d')
        current_time_str = current_time.strftime('%Y-%m-%d %H:%M:%S UTC')
        current_time_ms = int(current_time.timestamp() * 1000)
        
        current_time_context = f"""
CURRENT TIME CONTEXT FOR LLM CALCULATIONS:
Current Date: {current_date_str}
Current Time: {current_time_str}
Current Timestamp (ms): {current_time_ms}
Current Year: {current_time.year}
Current Month: {current_time.month}
Current Day: {current_time.day}

INSTRUCTIONS FOR LLM:
- Calculate your desired time range based on the current time above
- Convert your calculated datetime to Unix epoch milliseconds (multiply by 1000)
- Use the calculated timestamps in from_timestamp and to_timestamp parameters

EXAMPLE CALCULATIONS:
- "yesterday": Calculate start and end of {(current_time - timedelta(days=1)).strftime('%Y-%m-%d')}
- "last week": Calculate 7 days ago ({(current_time - timedelta(days=7)).strftime('%Y-%m-%d')}) to yesterday
- "last year": Calculate start and end of {current_time.year - 1}
- "10 years ago": Calculate around {current_time.year - 10}
- Any natural language time expression can be calculated from the current time above

"""
        return current_time_context.strip()
        
    except Exception as e:
        return f"Error: Exception occurred while getting current time context - {str(e)}"

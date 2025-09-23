"""Curated catalog of common Ambari Metrics per application.

The mapping is intentionally opinionated – it focuses on metrics that are
frequently used during cluster troubleshooting or capacity checks.  Each entry
contains a human friendly label, optional description, and a list of keywords
that help the natural-language matcher locate the right metric.

The catalog covers the following Ambari Metric Collector (AMS) appIds:

* ambari_server
* namenode
* datanode
* nodemanager
* resourcemanager

The helper functions at the bottom expose lightweight utilities for matching a
natural-language token stream to the closest curated metric entry.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Iterable, List, Optional, Tuple


@dataclass(frozen=True)
class CatalogEntry:
    metric: str
    label: str
    keywords: Tuple[str, ...]
    unit: Optional[str] = None
    description: Optional[str] = None


CURATED_METRICS: Dict[str, Tuple[CatalogEntry, ...]] = {
    "ambari_server": (
        CatalogEntry(
            metric="events.alerts",
            label="Alert events (total)",
            keywords=("alert", "alerts", "alarm", "event", "notification"),
            unit="count",
            description="Total number of alert events processed by Ambari server.",
        ),
        CatalogEntry(
            metric="events.alerts.avg",
            label="Alert events per second",
            keywords=("alert", "alerts", "rate", "avg", "per", "second"),
            unit="events/s",
        ),
        CatalogEntry(
            metric="events.requests",
            label="API requests (total)",
            keywords=("request", "api", "call", "rest"),
            unit="count",
        ),
        CatalogEntry(
            metric="events.requests.avg",
            label="API requests per second",
            keywords=("request", "api", "rate", "avg", "per", "second"),
            unit="req/s",
        ),
        CatalogEntry(
            metric="events.agentactions",
            label="Agent actions",
            keywords=("agent", "action", "command", "operation"),
            unit="count",
        ),
        CatalogEntry(
            metric="events.agentactions.avg",
            label="Agent actions per second",
            keywords=("agent", "action", "avg", "rate", "per", "second"),
            unit="actions/s",
        ),
        CatalogEntry(
            metric="events.services",
            label="Service change events",
            keywords=("service", "services", "component"),
            unit="count",
        ),
        CatalogEntry(
            metric="events.hosts",
            label="Host events",
            keywords=("host", "hosts", "node", "machine"),
            unit="count",
        ),
        CatalogEntry(
            metric="events.topology_update",
            label="Topology update events",
            keywords=("topology", "update", "layout", "structure"),
            unit="count",
        ),
        CatalogEntry(
            metric="live_hosts",
            label="Live agent hosts",
            keywords=("live", "host", "hosts", "agent", "status"),
            unit="hosts",
            description="Number of hosts currently reporting to Ambari server.",
        ),
        CatalogEntry(
            metric="alert_definitions",
            label="Alert definitions",
            keywords=("alert", "definition", "policy", "rule"),
            unit="count",
        ),
    ),
    "namenode": (
        CatalogEntry(
            metric="jvm.JvmMetrics.MemHeapUsedM",
            label="NameNode JVM heap used",
            keywords=("heap", "memory", "jvm", "usage", "used"),
            unit="MB",
        ),
        CatalogEntry(
            metric="jvm.JvmMetrics.MemHeapCommittedM",
            label="NameNode JVM heap committed",
            keywords=("heap", "committed", "memory", "jvm"),
            unit="MB",
        ),
        CatalogEntry(
            metric="dfs.FSNamesystem.CapacityTotalGB",
            label="HDFS capacity total",
            keywords=("capacity", "total", "hdfs", "storage", "overall"),
            unit="GB",
        ),
        CatalogEntry(
            metric="dfs.FSNamesystem.CapacityRemainingGB",
            label="HDFS capacity remaining",
            keywords=("capacity", "free", "remaining", "available", "hdfs"),
            unit="GB",
        ),
        CatalogEntry(
            metric="dfs.FSNamesystem.CapacityUsedGB",
            label="HDFS capacity used",
            keywords=("capacity", "used", "hdfs", "storage", "consumed"),
            unit="GB",
        ),
        CatalogEntry(
            metric="dfs.FSNamesystem.UnderReplicatedBlocks",
            label="Under-replicated blocks",
            keywords=("block", "under", "replica", "underreplicated"),
            unit="blocks",
        ),
        CatalogEntry(
            metric="dfs.FSNamesystem.PendingReplicationBlocks",
            label="Pending replication blocks",
            keywords=("pending", "replication", "block", "backlog"),
            unit="blocks",
        ),
        CatalogEntry(
            metric="dfs.namenode.PendingDeleteBlocksCount",
            label="Pending delete blocks",
            keywords=("pending", "delete", "block", "deletion"),
            unit="blocks",
        ),
        CatalogEntry(
            metric="dfs.namenode.GetBlockLocations",
            label="GetBlockLocations calls",
            keywords=("block", "location", "rpc", "calls"),
            unit="count",
        ),
        CatalogEntry(
            metric="dfs.namenode.SafeModeTime",
            label="Safe mode time",
            keywords=("safemode", "safe", "mode", "startup"),
            unit="ms",
        ),
        CatalogEntry(
            metric="jvm.JvmMetrics.GcTimeMillis",
            label="JVM GC time",
            keywords=("gc", "garbage", "collection", "pause"),
            unit="ms",
        ),
        CatalogEntry(
            metric="rpc.rpc.client.RpcAuthenticationSuccesses",
            label="Client RPC authentication successes",
            keywords=("rpc", "auth", "authentication", "success"),
            unit="count",
        ),
    ),
    "datanode": (
        CatalogEntry(
            metric="dfs.datanode.BlocksRead",
            label="Blocks read",
            keywords=("block", "read", "io"),
            unit="blocks",
        ),
        CatalogEntry(
            metric="dfs.datanode.BlocksWritten",
            label="Blocks written",
            keywords=("block", "write", "io"),
            unit="blocks",
        ),
        CatalogEntry(
            metric="dfs.datanode.BytesRead",
            label="Bytes read",
            keywords=("bytes", "read", "network", "throughput"),
            unit="bytes",
        ),
        CatalogEntry(
            metric="dfs.datanode.BytesWritten",
            label="Bytes written",
            keywords=("bytes", "write", "network", "throughput"),
            unit="bytes",
        ),
        CatalogEntry(
            metric="dfs.datanode.TotalWriteTime",
            label="Total write time",
            keywords=("write", "time", "latency", "duration"),
            unit="ms",
        ),
        CatalogEntry(
            metric="dfs.datanode.VolumeFailures",
            label="Volume failures",
            keywords=("volume", "failure", "disk", "fault"),
            unit="count",
        ),
        CatalogEntry(
            metric="FSDatasetState.org.apache.hadoop.hdfs.server.datanode.fsdataset.impl.FsDatasetImpl.Capacity",
            label="Dataset capacity",
            keywords=("capacity", "dataset", "storage", "total"),
            unit="bytes",
        ),
        CatalogEntry(
            metric="FSDatasetState.org.apache.hadoop.hdfs.server.datanode.fsdataset.impl.FsDatasetImpl.DfsUsed",
            label="Dataset DFS used",
            keywords=("dfs", "used", "storage", "utilization"),
            unit="bytes",
        ),
        CatalogEntry(
            metric="cpu_user",
            label="CPU user %",
            keywords=("cpu", "user", "usage", "utilization"),
            unit="percent",
        ),
        CatalogEntry(
            metric="cpu_system",
            label="CPU system %",
            keywords=("cpu", "system", "usage", "utilization"),
            unit="percent",
        ),
        CatalogEntry(
            metric="bytes_in",
            label="Network bytes in (KB/s)",
            keywords=("network", "in", "traffic", "bytes", "ingress"),
            unit="KB/s",
        ),
        CatalogEntry(
            metric="bytes_out",
            label="Network bytes out (KB/s)",
            keywords=("network", "out", "traffic", "bytes", "egress"),
            unit="KB/s",
        ),
        CatalogEntry(
            metric="disk_total",
            label="Disk total capacity",
            keywords=("disk", "total", "storage", "capacity"),
            unit="bytes",
        ),
    ),
    "nodemanager": (
        CatalogEntry(
            metric="yarn.NodeManagerMetrics.AllocatedVCores",
            label="Allocated vCores",
            keywords=("allocated", "vcpu", "vcore", "core", "capacity"),
            unit="vcores",
        ),
        CatalogEntry(
            metric="yarn.NodeManagerMetrics.AvailableVCores",
            label="Available vCores",
            keywords=("available", "vcpu", "vcore", "core", "free"),
            unit="vcores",
        ),
        CatalogEntry(
            metric="yarn.NodeManagerMetrics.AllocatedGB",
            label="Allocated memory (GB)",
            keywords=("allocated", "memory", "ram", "capacity"),
            unit="GB",
        ),
        CatalogEntry(
            metric="yarn.NodeManagerMetrics.AvailableGB",
            label="Available memory (GB)",
            keywords=("available", "memory", "ram", "free"),
            unit="GB",
        ),
        CatalogEntry(
            metric="yarn.NodeManagerMetrics.AllocatedContainers",
            label="Allocated containers",
            keywords=("container", "allocated", "count"),
            unit="containers",
        ),
        CatalogEntry(
            metric="yarn.NodeManagerMetrics.ContainersCompleted",
            label="Containers completed",
            keywords=("container", "completed", "finished"),
            unit="containers",
        ),
        CatalogEntry(
            metric="yarn.NodeManagerMetrics.ContainersFailed",
            label="Containers failed",
            keywords=("container", "failed", "error"),
            unit="containers",
        ),
        CatalogEntry(
            metric="yarn.NodeManagerMetrics.ContainersKilled",
            label="Containers killed",
            keywords=("container", "killed", "terminated"),
            unit="containers",
        ),
        CatalogEntry(
            metric="yarn.NodeManagerMetrics.ContainerLaunchDurationAvgTime",
            label="Container launch time (avg)",
            keywords=("container", "launch", "duration", "startup", "latency"),
            unit="ms",
        ),
        CatalogEntry(
            metric="bytes_out",
            label="Network bytes out (KB/s)",
            keywords=("network", "out", "traffic", "bytes", "egress"),
            unit="KB/s",
        ),
        CatalogEntry(
            metric="cpu_user",
            label="CPU user %",
            keywords=("cpu", "user", "usage", "utilization"),
            unit="percent",
        ),
        CatalogEntry(
            metric="mem_total",
            label="Total memory",
            keywords=("memory", "total", "ram", "capacity"),
            unit="MB",
        ),
    ),
    "resourcemanager": (
        CatalogEntry(
            metric="yarn.QueueMetrics.Queue=root.AllocatedMB",
            label="Root queue allocated MB",
            keywords=("root", "queue", "allocated", "memory", "mb"),
            unit="MB",
        ),
        CatalogEntry(
            metric="yarn.QueueMetrics.Queue=root.AllocatedVCores",
            label="Root queue allocated vCores",
            keywords=("root", "queue", "allocated", "vcore", "vcpu"),
            unit="vcores",
        ),
        CatalogEntry(
            metric="yarn.QueueMetrics.Queue=root.PendingMB",
            label="Root queue pending MB",
            keywords=("root", "queue", "pending", "memory"),
            unit="MB",
        ),
        CatalogEntry(
            metric="yarn.QueueMetrics.Queue=root.PendingVCores",
            label="Root queue pending vCores",
            keywords=("root", "queue", "pending", "vcore"),
            unit="vcores",
        ),
        CatalogEntry(
            metric="yarn.QueueMetrics.Queue=root.AppsRunning",
            label="Root queue apps running",
            keywords=("root", "queue", "app", "running"),
            unit="apps",
        ),
        CatalogEntry(
            metric="yarn.QueueMetrics.Queue=root.default.AllocatedMB",
            label="Default queue allocated MB",
            keywords=("default", "queue", "allocated", "memory"),
            unit="MB",
        ),
        CatalogEntry(
            metric="yarn.QueueMetrics.Queue=root.default.PendingMB",
            label="Default queue pending MB",
            keywords=("default", "queue", "pending", "memory"),
            unit="MB",
        ),
        CatalogEntry(
            metric="yarn.QueueMetrics.Queue=root.default.AppsPending",
            label="Default queue apps pending",
            keywords=("default", "queue", "app", "pending"),
            unit="apps",
        ),
        CatalogEntry(
            metric="yarn.QueueMetrics.Queue=root.default.AllocatedContainers",
            label="Default queue allocated containers",
            keywords=("default", "queue", "container", "allocated"),
            unit="containers",
        ),
        CatalogEntry(
            metric="yarn.QueueMetrics.Queue=root.default.AggregateContainersAllocated",
            label="Default queue containers allocated (agg)",
            keywords=("default", "queue", "container", "aggregate", "allocated"),
            unit="containers",
        ),
        CatalogEntry(
            metric="yarn.ClusterMetrics.AMLaunchDelayAvgTime",
            label="ApplicationMaster launch delay (avg)",
            keywords=("am", "launch", "delay", "avg", "latency"),
            unit="ms",
        ),
        CatalogEntry(
            metric="yarn.PartitionQueueMetrics.Queue=root.AppsSubmitted",
            label="Root partition apps submitted",
            keywords=("root", "queue", "partition", "app", "submitted"),
            unit="apps",
        ),
        CatalogEntry(
            metric="rpc.rpc.NumOpenConnections",
            label="RM RPC open connections",
            keywords=("rpc", "connections", "open", "active"),
            unit="connections",
        ),
        CatalogEntry(
            metric="jvm.JvmMetrics.MemHeapUsedM",
            label="ResourceManager JVM heap used",
            keywords=("heap", "memory", "jvm", "usage", "used"),
            unit="MB",
        ),
    ),
}


APP_SYNONYMS: Dict[str, Tuple[str, ...]] = {
    "ambari_server": ("ambari", "server", "ambari_server"),
    "namenode": ("namenode", "hdfs", "nn", "name node"),
    "datanode": ("datanode", "dn", "data node"),
    "nodemanager": ("nodemanager", "nm", "node manager"),
    "resourcemanager": ("resourcemanager", "rm", "resource manager", "yarn"),
}


def iter_catalog_entries(app_ids: Optional[Iterable[str]] = None) -> Iterable[Tuple[str, CatalogEntry]]:
    """Yield (app_id, entry) pairs for the requested app ids (or all)."""

    if app_ids:
        targets = [app for app in app_ids if app in CURATED_METRICS]
    else:
        targets = list(CURATED_METRICS.keys())

    for app in targets:
        for entry in CURATED_METRICS[app]:
            yield app, entry


def app_from_tokens(tokens: Iterable[str], app_hint: Optional[str] = None) -> Optional[str]:
    """Infer appId from token list (optionally seeded with an explicit hint)."""

    if app_hint and app_hint in CURATED_METRICS:
        return app_hint

    token_set = {tok.lower() for tok in tokens if tok}
    for app, synonyms in APP_SYNONYMS.items():
        if any(syn in token_set for syn in synonyms):
            return app

    return app_hint if app_hint in CURATED_METRICS else None


def keyword_match_score(entry: CatalogEntry, tokens: Iterable[str]) -> int:
    """Compute a heuristic score between a catalog entry and query tokens."""

    if not tokens:
        return 0

    lowered_tokens = [tok.lower() for tok in tokens if tok]
    score = 0

    metric_tokens = set()
    for part in entry.metric.replace('.', ' ').replace('_', ' ').split():
        metric_tokens.add(part.lower())

    label_tokens = set(entry.label.replace('/', ' ').replace('-', ' ').lower().split())
    keyword_tokens = {kw.lower() for kw in entry.keywords}

    for token in lowered_tokens:
        if token in keyword_tokens:
            score += 40
        elif token in label_tokens:
            score += 30
        elif token in metric_tokens:
            score += 25
        elif token in entry.metric.lower():
            score += 10

    # Small boost if multiple tokens matched anything
    if score >= 40 and len(lowered_tokens) > 1:
        score += 10

    return score


def best_catalog_match(tokens: Iterable[str], app_hint: Optional[str] = None) -> Optional[Tuple[str, CatalogEntry, int]]:
    """Return the best matching catalog entry for the provided tokens."""

    tokens = [tok for tok in tokens if tok]
    candidate_app = app_from_tokens(tokens, app_hint=app_hint)

    best: Optional[Tuple[str, CatalogEntry, int]] = None
    search_apps: List[str]

    if candidate_app:
        search_apps = [candidate_app]
    else:
        search_apps = list(CURATED_METRICS.keys())

    for app in search_apps:
        for entry in CURATED_METRICS[app]:
            score = keyword_match_score(entry, tokens)
            if score <= 0:
                continue
            if best is None or score > best[2]:
                best = (app, entry, score)

    return best


def rank_catalog_matches(
    tokens: Iterable[str],
    app_ids: Optional[Iterable[str]] = None,
    min_score: int = 0,
    limit: int = 40,
) -> List[Tuple[str, CatalogEntry, int]]:
    """Return ranked catalog matches for the provided tokens."""

    tokens = [tok for tok in tokens if tok]
    if not tokens:
        return []

    results: List[Tuple[str, CatalogEntry, int]] = []

    target_apps = [app for app in app_ids if app in CURATED_METRICS] if app_ids else list(CURATED_METRICS.keys())

    for app in target_apps:
        seen = set()
        for entry in CURATED_METRICS[app]:
            if entry.metric in seen:
                continue
            seen.add(entry.metric)
            score = keyword_match_score(entry, tokens)
            if score >= min_score:
                results.append((app, entry, score))

    results.sort(key=lambda item: (-item[2], item[0], item[1].metric))
    return results[:limit]

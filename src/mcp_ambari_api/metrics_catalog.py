"""Simplified catalog of curated Ambari Metrics per application.

This module now focuses on maintaining exact metric name collections per AMS appId.
All natural-language scoring helpers have been removed – callers should look up
metric identifiers via the catalog and pass exact strings to Ambari.
"""

from __future__ import annotations

from typing import Dict, Iterable, List, Optional, Set, Tuple

# ---------------------------------------------------------------------------
# Base metric name definitions
# ---------------------------------------------------------------------------
# These originate from the previous CatalogEntry-based structure.  Each tuple
# lists the canonical metric names that were curated for the corresponding appId.
# Additional helper sets (COMMON_JVM_METRICS, DATANODE_BLOCK_METRICS) are merged
# automatically in the builder below.
# ---------------------------------------------------------------------------
BASE_METRICS_BY_APP: Dict[str, Tuple[str, ...]] = {
    "HOST": (
        "cpu_idle",
        "cpu_user",
        "cpu_system",
        "mem_total",
        "mem_used",
        "mem_free",
        "swap_total",
        "swap_used",
        "swap_free",
        "disk_total",
        "FSDatasetState.org.apache.hadoop.hdfs.server.datanode.fsdataset.impl.FsDatasetImpl.Capacity",
        "FSDatasetState.org.apache.hadoop.hdfs.server.datanode.fsdataset.impl.FsDatasetImpl.DfsUsed",
        "FSDatasetState.org.apache.hadoop.hdfs.server.datanode.fsdataset.impl.FsDatasetImpl.Remaining",
        "dfs.datanode.DataNodeActiveXceiversCount",
        "dfs.datanode.BlocksRead",
        "dfs.datanode.BlocksWritten",
        "dfs.datanode.BlocksReplicated",
        "dfs.datanode.BlocksRemoved",
        "dfs.datanode.BlocksCached",
        "dfs.datanode.BlocksUncached",
        "dfs.datanode.BlocksInPendingIBR",
        "dfs.datanode.BlocksReceivingInPendingIBR",
        "dfs.datanode.BlocksReceivedInPendingIBR",
        "dfs.datanode.IncrementalBlockReportsNumOps",
        "disk_used",
        "disk_free",
        "bytes_in",
        "bytes_out",
        "pkts_in",
        "pkts_out",
        "load_one",
        "load_five",
        "load_fifteen",
        "proc_total",
        "proc_run",
        "mem_cached",
        "mem_buffered",
        "mem_shared",
        "cpu_wio",
    ),
    "ambari_server": (
        "events.alerts",
        "events.alerts.avg",
        "events.requests",
        "events.requests.avg",
        "events.agentactions",
        "events.agentactions.avg",
        "events.services",
        "events.hosts",
        "events.topology_update",
        "live_hosts",
        "alert_definitions",
    ),
    "namenode": (
        "jvm.JvmMetrics.MemHeapUsedM",
        "jvm.JvmMetrics.MemHeapCommittedM",
        "jvm.JvmMetrics.ThreadsBlocked",
        "dfs.FSNamesystem.CapacityTotalGB",
        "dfs.FSNamesystem.CapacityRemainingGB",
        "dfs.FSNamesystem.CapacityUsedGB",
        "dfs.FSNamesystem.CapacityTotal",
        "dfs.FSNamesystem.CapacityRemaining",
        "dfs.FSNamesystem.CapacityUsed",
        "dfs.FSNamesystem.CapacityUsedNonDFS",
        "dfs.FSNamesystem.UnderReplicatedBlocks",
        "dfs.FSNamesystem.PendingReplicationBlocks",
        "dfs.namenode.PendingDeleteBlocksCount",
        "dfs.FSNamesystem.CorruptBlocks",
        "dfs.FSNamesystem.MissingBlocks",
        "dfs.FSNamesystem.MissingReplOneBlocks",
        "dfs.FSNamesystem.LowRedundancyBlocks",
        "dfs.FSNamesystem.PendingReconstructionBlocks",
        "dfs.FSNamesystem.BlocksTotal",
        "dfs.FSNamesystem.PendingDataNodeMessageCount",
        "dfs.namenode.GetBlockLocations",
        "dfs.namenode.SafeModeTime",
        "jvm.JvmMetrics.GcTimeMillis",
        "rpc.rpc.client.RpcAuthenticationSuccesses",
    ),
    "datanode": (
        "dfs.datanode.BlockChecksumOpAvgTime",
        "dfs.datanode.BlockChecksumOpNumOps",
        "dfs.datanode.BlockReportsAvgTime",
        "dfs.datanode.BlockReportsNumOps",
        "dfs.datanode.BlocksCached",
        "dfs.datanode.BlocksDeletedInPendingIBR",
        "dfs.datanode.BlocksGetLocalPathInfo",
        "dfs.datanode.BlocksInPendingIBR",
        "dfs.datanode.BlocksRead",
        "dfs.datanode.BlocksReceivedInPendingIBR",
        "dfs.datanode.BlocksReceivingInPendingIBR",
        "dfs.datanode.BlocksRemoved",
        "dfs.datanode.BlocksReplicated",
        "dfs.datanode.BlocksUncached",
        "dfs.datanode.BlocksVerified",
        "dfs.datanode.BlocksWritten",
        "dfs.datanode.BlockVerificationFailures",
        "dfs.datanode.CopyBlockOpAvgTime",
        "dfs.datanode.CopyBlockOpNumOps",
        "dfs.datanode.DataNodeBlockRecoveryWorkerCount",
        "dfs.datanode.IncrementalBlockReportsAvgTime",
        "dfs.datanode.IncrementalBlockReportsNumOps",
        "dfs.datanode.RamDiskBlocksDeletedBeforeLazyPersisted",
        "dfs.datanode.RamDiskBlocksEvicted",
        "dfs.datanode.RamDiskBlocksEvictedWithoutRead",
        "dfs.datanode.RamDiskBlocksEvictionWindowMsAvgTime",
        "dfs.datanode.RamDiskBlocksEvictionWindowMsNumOps",
        "dfs.datanode.RamDiskBlocksLazyPersisted",
        "dfs.datanode.RamDiskBlocksLazyPersistWindowMsAvgTime",
        "dfs.datanode.RamDiskBlocksLazyPersistWindowMsNumOps",
        "dfs.datanode.RamDiskBlocksReadHits",
        "dfs.datanode.RamDiskBlocksWrite",
        "dfs.datanode.RamDiskBlocksWriteFallback",
        "dfs.datanode.ReadBlockOpAvgTime",
        "dfs.datanode.ReadBlockOpNumOps",
        "dfs.datanode.ReplaceBlockOpAvgTime",
        "dfs.datanode.ReplaceBlockOpNumOps",
        "dfs.datanode.SendDataPacketBlockedOnNetworkNanosAvgTime",
        "dfs.datanode.SendDataPacketBlockedOnNetworkNanosNumOps",
        "dfs.datanode.WriteBlockOpAvgTime",
        "dfs.datanode.WriteBlockOpNumOps",
        "dfs.datanode.BytesRead",
        "dfs.datanode.BytesWritten",
        "jvm.JvmMetrics.ThreadsBlocked",
        "dfs.datanode.TotalWriteTime",
        "dfs.datanode.VolumeFailures",
        "FSDatasetState.org.apache.hadoop.hdfs.server.datanode.fsdataset.impl.FsDatasetImpl.Capacity",
        "FSDatasetState.org.apache.hadoop.hdfs.server.datanode.fsdataset.impl.FsDatasetImpl.DfsUsed",
        "cpu_user",
        "cpu_system",
        "bytes_in",
        "bytes_out",
        "disk_total",
    ),
    "nodemanager": (
        "yarn.NodeManagerMetrics.AllocatedVCores",
        "yarn.NodeManagerMetrics.AvailableVCores",
        "yarn.NodeManagerMetrics.AllocatedGB",
        "yarn.NodeManagerMetrics.AvailableGB",
        "yarn.NodeManagerMetrics.AllocatedContainers",
        "yarn.NodeManagerMetrics.ContainersCompleted",
        "yarn.NodeManagerMetrics.ContainersFailed",
        "yarn.NodeManagerMetrics.ContainersKilled",
        "yarn.NodeManagerMetrics.ContainerLaunchDurationAvgTime",
        "bytes_out",
        "cpu_user",
        "mem_total",
        "jvm.JvmMetrics.MemHeapUsedM",
        "jvm.JvmMetrics.ThreadsBlocked",
    ),
    "resourcemanager": (
        "yarn.QueueMetrics.Queue=root.AllocatedMB",
        "yarn.QueueMetrics.Queue=root.AllocatedVCores",
        "yarn.QueueMetrics.Queue=root.PendingMB",
        "yarn.QueueMetrics.Queue=root.PendingVCores",
        "yarn.QueueMetrics.Queue=root.AppsRunning",
        "yarn.QueueMetrics.Queue=root.default.AllocatedMB",
        "yarn.QueueMetrics.Queue=root.default.PendingMB",
        "yarn.QueueMetrics.Queue=root.default.AppsPending",
        "yarn.QueueMetrics.Queue=root.default.AllocatedContainers",
        "yarn.QueueMetrics.Queue=root.default.AggregateContainersAllocated",
        "yarn.ClusterMetrics.AMLaunchDelayAvgTime",
        "yarn.PartitionQueueMetrics.Queue=root.AppsSubmitted",
        "rpc.rpc.NumOpenConnections",
        "jvm.JvmMetrics.MemHeapUsedM",
        "jvm.JvmMetrics.ThreadsBlocked",
    ),
}


DATANODE_BLOCK_METRICS: Tuple[str, ...] = (
    "dfs.datanode.BlockChecksumOpAvgTime",
    "dfs.datanode.BlockChecksumOpNumOps",
    "dfs.datanode.BlockReportsAvgTime",
    "dfs.datanode.BlockReportsNumOps",
    "dfs.datanode.BlocksCached",
    "dfs.datanode.BlocksDeletedInPendingIBR",
    "dfs.datanode.BlocksGetLocalPathInfo",
    "dfs.datanode.BlocksInPendingIBR",
    "dfs.datanode.BlocksRead",
    "dfs.datanode.BlocksReceivedInPendingIBR",
    "dfs.datanode.BlocksReceivingInPendingIBR",
    "dfs.datanode.BlocksRemoved",
    "dfs.datanode.BlocksReplicated",
    "dfs.datanode.BlocksUncached",
    "dfs.datanode.BlocksVerified",
    "dfs.datanode.BlocksWritten",
    "dfs.datanode.BlockVerificationFailures",
    "dfs.datanode.CopyBlockOpAvgTime",
    "dfs.datanode.CopyBlockOpNumOps",
    "dfs.datanode.DataNodeBlockRecoveryWorkerCount",
    "dfs.datanode.IncrementalBlockReportsAvgTime",
    "dfs.datanode.IncrementalBlockReportsNumOps",
    "dfs.datanode.RamDiskBlocksDeletedBeforeLazyPersisted",
    "dfs.datanode.RamDiskBlocksEvicted",
    "dfs.datanode.RamDiskBlocksEvictedWithoutRead",
    "dfs.datanode.RamDiskBlocksEvictionWindowMsAvgTime",
    "dfs.datanode.RamDiskBlocksEvictionWindowMsNumOps",
    "dfs.datanode.RamDiskBlocksLazyPersisted",
    "dfs.datanode.RamDiskBlocksLazyPersistWindowMsAvgTime",
    "dfs.datanode.RamDiskBlocksLazyPersistWindowMsNumOps",
    "dfs.datanode.RamDiskBlocksReadHits",
    "dfs.datanode.RamDiskBlocksWrite",
    "dfs.datanode.RamDiskBlocksWriteFallback",
    "dfs.datanode.ReadBlockOpAvgTime",
    "dfs.datanode.ReadBlockOpNumOps",
    "dfs.datanode.ReplaceBlockOpAvgTime",
    "dfs.datanode.ReplaceBlockOpNumOps",
    "dfs.datanode.SendDataPacketBlockedOnNetworkNanosAvgTime",
    "dfs.datanode.SendDataPacketBlockedOnNetworkNanosNumOps",
    "dfs.datanode.WriteBlockOpAvgTime",
    "dfs.datanode.WriteBlockOpNumOps",
)

COMMON_JVM_METRICS: Tuple[str, ...] = (
    "jvm.JvmMetrics.GcTotalExtraSleepTime",
    "jvm.JvmMetrics.GcCount",
    "jvm.JvmMetrics.GcCountPS MarkSweep",
    "jvm.JvmMetrics.MemNonHeapMaxM",
    "jvm.JvmMetrics.ThreadsWaiting",
    "jvm.JvmMetrics.GcTimeMillisPS MarkSweep",
    "jvm.JvmMetrics.MemNonHeapCommittedM",
    "jvm.JvmMetrics.MemMaxM",
    "jvm.JvmMetrics.MemHeapCommittedM",
    "jvm.JvmMetrics.ThreadsNew",
    "jvm.JvmMetrics.LogInfo",
    "jvm.JvmMetrics.MemHeapMaxM",
    "jvm.JvmMetrics.LogError",
    "jvm.JvmMetrics.ThreadsBlocked",
    "jvm.JvmMetrics.LogFatal",
    "jvm.JvmMetrics.GcTimeMillis",
    "jvm.JvmMetrics.LogWarn",
    "jvm.JvmMetrics.GcCountPS Scavenge",
    "jvm.JvmMetrics.ThreadsTerminated",
    "jvm.JvmMetrics.GcNumWarnThresholdExceeded",
    "jvm.JvmMetrics.GcTimeMillisPS Scavenge",
    "jvm.JvmMetrics.GcNumInfoThresholdExceeded",
    "jvm.JvmMetrics.MemHeapUsedM",
    "jvm.JvmMetrics.MemNonHeapUsedM",
    "jvm.JvmMetrics.ThreadsRunnable",
    "jvm.JvmMetrics.ThreadsTimedWaiting",
)

COMMON_JVM_APPS: Tuple[str, ...] = (
    "namenode",
    "datanode",
    "nodemanager",
    "resourcemanager",
)

# ---------------------------------------------------------------------------
# Derived catalog structures
# ---------------------------------------------------------------------------
CURATED_METRICS: Dict[str, Tuple[str, ...]] = {}
_METRICS_BY_APP_SET: Dict[str, Set[str]] = {}


def _build_metrics_by_app() -> None:
    for app, base_metrics in BASE_METRICS_BY_APP.items():
        names: Set[str] = set(base_metrics)
        if app == "datanode":
            names.update(DATANODE_BLOCK_METRICS)
        if app in COMMON_JVM_APPS:
            names.update(COMMON_JVM_METRICS)
        ordered = tuple(sorted(names))
        CURATED_METRICS[app] = ordered
        _METRICS_BY_APP_SET[app] = set(ordered)


_build_metrics_by_app()

# ---------------------------------------------------------------------------
# AppId canonicalisation helpers
# ---------------------------------------------------------------------------
APP_SYNONYMS: Dict[str, Tuple[str, ...]] = {
    "HOST": ("host", "hardware", "system"),
    "ambari_server": ("ambari", "server", "ambari_server"),
    "namenode": ("namenode", "hdfs", "nn", "name node"),
    "datanode": ("datanode", "dn", "data node"),
    "nodemanager": ("nodemanager", "nm", "node manager"),
    "resourcemanager": ("resourcemanager", "rm", "resource manager", "yarn"),
}


def canonicalize_app_id(app_id: Optional[str]) -> Optional[str]:
    """Return the canonical AMS appId (case-insensitive synonym support)."""

    if not app_id:
        return None

    normalized = app_id.strip()
    if not normalized:
        return None

    lowered = normalized.lower()

    for canonical, synonyms in APP_SYNONYMS.items():
        if lowered == canonical.lower():
            return canonical
        for synonym in synonyms:
            if lowered == synonym.lower():
                return canonical

    # Default: return lowercase version if unknown (avoids None -> breakage)
    return lowered


# ---------------------------------------------------------------------------
# Public access helpers
# ---------------------------------------------------------------------------

def get_metrics_for_app(app_id: Optional[str]) -> Tuple[str, ...]:
    """Return the tuple of supported metrics for the provided appId."""

    canonical = canonicalize_app_id(app_id)
    if not canonical:
        return ()
    return CURATED_METRICS.get(canonical, ())


def metric_supported_for_app(app_id: Optional[str], metric_name: Optional[str]) -> bool:
    """Return True when a metric is available for the given appId (exact match)."""

    if not metric_name:
        return False
    canonical = canonicalize_app_id(app_id)
    if not canonical:
        return False
    return metric_name in _METRICS_BY_APP_SET.get(canonical, set())


__all__ = [
    "BASE_METRICS_BY_APP",
    "CURATED_METRICS",
    "DATANODE_BLOCK_METRICS",
    "COMMON_JVM_METRICS",
    "COMMON_JVM_APPS",
    "APP_SYNONYMS",
    "canonicalize_app_id",
    "get_metrics_for_app",
    "metric_supported_for_app",
]

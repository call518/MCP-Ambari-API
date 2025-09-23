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
    "HOST": (
        CatalogEntry(
            metric="cpu_idle",
            label="Host CPU idle %",
            keywords=("cpu", "idle", "host", "utilization", "usage"),
            unit="percent",
        ),
        CatalogEntry(
            metric="cpu_user",
            label="Host CPU user %",
            keywords=("cpu", "user", "usage", "utilization"),
            unit="percent",
        ),
        CatalogEntry(
            metric="cpu_system",
            label="Host CPU system %",
            keywords=("cpu", "system", "usage", "utilization"),
            unit="percent",
        ),
        CatalogEntry(
            metric="mem_total",
            label="Host memory total",
            keywords=("memory", "total", "ram", "capacity"),
            unit="bytes",
        ),
        CatalogEntry(
            metric="mem_used",
            label="Host memory used",
            keywords=("memory", "used", "ram", "utilization"),
            unit="bytes",
        ),
        CatalogEntry(
            metric="mem_free",
            label="Host memory free",
            keywords=("memory", "free", "ram", "available"),
            unit="bytes",
        ),
        CatalogEntry(
            metric="swap_total",
            label="Swap total",
            keywords=("swap", "total", "memory"),
            unit="bytes",
        ),
        CatalogEntry(
            metric="swap_used",
            label="Swap used",
            keywords=("swap", "used", "memory"),
            unit="bytes",
        ),
        CatalogEntry(
            metric="swap_free",
            label="Swap free",
            keywords=("swap", "free", "memory"),
            unit="bytes",
        ),
        CatalogEntry(
            metric="disk_total",
            label="Disk total",
            keywords=("disk", "total", "storage", "capacity"),
            unit="bytes",
        ),
        CatalogEntry(
            metric="FSDatasetState.org.apache.hadoop.hdfs.server.datanode.fsdataset.impl.FsDatasetImpl.Capacity",
            label="Dataset capacity (per DataNode)",
            keywords=("dataset", "capacity", "datanode", "storage"),
            unit="bytes",
        ),
        CatalogEntry(
            metric="FSDatasetState.org.apache.hadoop.hdfs.server.datanode.fsdataset.impl.FsDatasetImpl.DfsUsed",
            label="Dataset DFS used (per DataNode)",
            keywords=("dataset", "dfs", "used", "datanode"),
            unit="bytes",
        ),
        CatalogEntry(
            metric="FSDatasetState.org.apache.hadoop.hdfs.server.datanode.fsdataset.impl.FsDatasetImpl.Remaining",
            label="Dataset remaining (per DataNode)",
            keywords=("dataset", "remaining", "datanode", "storage"),
            unit="bytes",
        ),
        CatalogEntry(
            metric="dfs.datanode.DataNodeActiveXceiversCount",
            label="Active DataNode xceivers",
            keywords=("datanode", "xceivers", "connections", "active"),
        ),
        CatalogEntry(
            metric="dfs.datanode.BlocksRead",
            label="Blocks read (cumulative)",
            keywords=("blocks", "read", "io", "throughput"),
        ),
        CatalogEntry(
            metric="dfs.datanode.BlocksWritten",
            label="Blocks written (cumulative)",
            keywords=("blocks", "written", "write"),
        ),
        CatalogEntry(
            metric="dfs.datanode.BlocksReplicated",
            label="Blocks replicated",
            keywords=("blocks", "replicated", "replication"),
        ),
        CatalogEntry(
            metric="dfs.datanode.BlocksRemoved",
            label="Blocks removed",
            keywords=("blocks", "removed", "deleted"),
        ),
        CatalogEntry(
            metric="dfs.datanode.BlocksCached",
            label="Blocks cached",
            keywords=("blocks", "cached", "cache"),
        ),
        CatalogEntry(
            metric="dfs.datanode.BlocksUncached",
            label="Blocks uncached",
            keywords=("blocks", "uncached", "cache"),
        ),
        CatalogEntry(
            metric="dfs.datanode.BlocksInPendingIBR",
            label="Blocks in pending IBR",
            keywords=("blocks", "pending", "ibr", "incremental"),
        ),
        CatalogEntry(
            metric="dfs.datanode.BlocksReceivingInPendingIBR",
            label="Blocks receiving (pending IBR)",
            keywords=("blocks", "receiving", "ibr", "pending"),
        ),
        CatalogEntry(
            metric="dfs.datanode.BlocksReceivedInPendingIBR",
            label="Blocks received (pending IBR)",
            keywords=("blocks", "received", "ibr"),
        ),
        CatalogEntry(
            metric="dfs.datanode.IncrementalBlockReportsNumOps",
            label="Incremental block reports",
            keywords=("block", "reports", "incremental", "ops"),
        ),
        CatalogEntry(
            metric="disk_used",
            label="Disk used",
            keywords=("disk", "used", "storage", "utilization"),
            unit="bytes",
        ),
        CatalogEntry(
            metric="disk_free",
            label="Disk free",
            keywords=("disk", "free", "storage", "available"),
            unit="bytes",
        ),
        CatalogEntry(
            metric="bytes_in",
            label="Network bytes in",
            keywords=("network", "bytes", "in", "traffic", "ingress"),
            unit="KB/s",
        ),
        CatalogEntry(
            metric="bytes_out",
            label="Network bytes out",
            keywords=("network", "bytes", "out", "traffic", "egress"),
            unit="KB/s",
        ),
        CatalogEntry(
            metric="pkts_in",
            label="Network packets in",
            keywords=("network", "packets", "in", "traffic"),
            unit="pkt/s",
        ),
        CatalogEntry(
            metric="pkts_out",
            label="Network packets out",
            keywords=("network", "packets", "out", "traffic"),
            unit="pkt/s",
        ),
        CatalogEntry(
            metric="load_one",
            label="Load average (1m)",
            keywords=("load", "average", "1m", "host"),
        ),
        CatalogEntry(
            metric="load_five",
            label="Load average (5m)",
            keywords=("load", "average", "5m", "host"),
        ),
        CatalogEntry(
            metric="load_fifteen",
            label="Load average (15m)",
            keywords=("load", "average", "15m", "host"),
        ),
        CatalogEntry(
            metric="proc_total",
            label="Total processes",
            keywords=("process", "count", "total", "host"),
        ),
        CatalogEntry(
            metric="proc_run",
            label="Running processes",
            keywords=("process", "running", "count", "host"),
        ),
        CatalogEntry(
            metric="mem_cached",
            label="Memory cached",
            keywords=("memory", "cached", "cache"),
            unit="bytes",
        ),
        CatalogEntry(
            metric="mem_buffered",
            label="Memory buffered",
            keywords=("memory", "buffered", "buffers"),
            unit="bytes",
        ),
        CatalogEntry(
            metric="mem_shared",
            label="Memory shared",
            keywords=("memory", "shared"),
            unit="bytes",
        ),
        CatalogEntry(
            metric="cpu_wio",
            label="CPU IO wait %",
            keywords=("cpu", "io", "wait", "usage"),
            unit="percent",
        ),
    ),
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
            metric="jvm.JvmMetrics.ThreadsBlocked",
            label="NameNode JVM threads blocked",
            keywords=("jvm", "threads", "thread", "blocked", "waiting"),
            unit="threads",
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
            metric="dfs.FSNamesystem.CapacityTotal",
            label="HDFS capacity total (bytes)",
            keywords=("capacity", "total", "bytes", "hdfs"),
            unit="bytes",
        ),
        CatalogEntry(
            metric="dfs.FSNamesystem.CapacityRemaining",
            label="HDFS capacity remaining (bytes)",
            keywords=("capacity", "remaining", "bytes", "free"),
            unit="bytes",
        ),
        CatalogEntry(
            metric="dfs.FSNamesystem.CapacityUsed",
            label="HDFS capacity used (bytes)",
            keywords=("capacity", "used", "bytes", "storage"),
            unit="bytes",
        ),
        CatalogEntry(
            metric="dfs.FSNamesystem.CapacityUsedNonDFS",
            label="Non-DFS capacity used",
            keywords=("capacity", "non", "dfs", "used"),
            unit="bytes",
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
            metric="dfs.FSNamesystem.CorruptBlocks",
            label="Corrupt blocks",
            keywords=("corrupt", "blocks", "bad"),
            unit="blocks",
        ),
        CatalogEntry(
            metric="dfs.FSNamesystem.MissingBlocks",
            label="Missing blocks",
            keywords=("missing", "blocks", "lost"),
            unit="blocks",
        ),
        CatalogEntry(
            metric="dfs.FSNamesystem.MissingReplOneBlocks",
            label="Missing blocks (replication 1)",
            keywords=("missing", "replication", "one", "blocks"),
            unit="blocks",
        ),
        CatalogEntry(
            metric="dfs.FSNamesystem.LowRedundancyBlocks",
            label="Low redundancy blocks",
            keywords=("low", "redundancy", "blocks"),
            unit="blocks",
        ),
        CatalogEntry(
            metric="dfs.FSNamesystem.PendingReconstructionBlocks",
            label="Pending reconstruction blocks",
            keywords=("pending", "reconstruction", "blocks"),
            unit="blocks",
        ),
        CatalogEntry(
            metric="dfs.FSNamesystem.BlocksTotal",
            label="Total HDFS blocks",
            keywords=("blocks", "total", "count"),
            unit="blocks",
        ),
        CatalogEntry(
            metric="dfs.FSNamesystem.PendingDataNodeMessageCount",
            label="Pending DataNode messages",
            keywords=("pending", "datanode", "messages"),
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
            keywords=("block", "blocks", "read", "reads", "io"),
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
            metric="jvm.JvmMetrics.ThreadsBlocked",
            label="DataNode JVM threads blocked",
            keywords=("jvm", "threads", "thread", "blocked", "waiting", "datanode"),
            unit="threads",
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
        CatalogEntry(
            metric="dfs.datanode.BlocksReplicated",
            label="Blocks replicated",
            keywords=("blocks", "replicated", "replication"),
            unit="blocks",
        ),
        CatalogEntry(
            metric="dfs.datanode.BlocksRemoved",
            label="Blocks removed",
            keywords=("blocks", "removed", "deleted"),
            unit="blocks",
        ),
        CatalogEntry(
            metric="dfs.datanode.BlocksCached",
            label="Blocks cached",
            keywords=("blocks", "cached", "cache"),
            unit="blocks",
        ),
        CatalogEntry(
            metric="dfs.datanode.BlocksUncached",
            label="Blocks uncached",
            keywords=("blocks", "uncached", "cache"),
            unit="blocks",
        ),
        CatalogEntry(
            metric="dfs.datanode.BlocksInPendingIBR",
            label="Blocks in pending IBR",
            keywords=("blocks", "pending", "ibr"),
            unit="blocks",
        ),
        CatalogEntry(
            metric="dfs.datanode.BlocksReceivingInPendingIBR",
            label="Blocks receiving (pending IBR)",
            keywords=("blocks", "receiving", "ibr"),
            unit="blocks",
        ),
        CatalogEntry(
            metric="dfs.datanode.BlocksReceivedInPendingIBR",
            label="Blocks received (pending IBR)",
            keywords=("blocks", "received", "ibr"),
            unit="blocks",
        ),
        CatalogEntry(
            metric="dfs.datanode.BlocksDeletedInPendingIBR",
            label="Blocks deleted (pending IBR)",
            keywords=("blocks", "deleted", "ibr"),
            unit="blocks",
        ),
        CatalogEntry(
            metric="dfs.datanode.BlocksVerified",
            label="Blocks verified",
            keywords=("blocks", "verified"),
            unit="blocks",
        ),
        CatalogEntry(
            metric="dfs.datanode.BlockVerificationFailures",
            label="Block verification failures",
            keywords=("block", "verification", "fail"),
            unit="count",
        ),
        CatalogEntry(
            metric="dfs.datanode.BlockChecksumOpAvgTime",
            label="Block checksum avg time",
            keywords=("block", "checksum", "average", "time"),
            unit="ms",
        ),
        CatalogEntry(
            metric="dfs.datanode.BlockChecksumOpNumOps",
            label="Block checksum operations",
            keywords=("block", "checksum", "ops"),
            unit="ops",
        ),
        CatalogEntry(
            metric="dfs.datanode.BlockReportsAvgTime",
            label="Block reports avg time",
            keywords=("block", "reports", "average", "time"),
            unit="ms",
        ),
        CatalogEntry(
            metric="dfs.datanode.BlockReportsNumOps",
            label="Block reports operations",
            keywords=("block", "reports", "ops"),
            unit="ops",
        ),
        CatalogEntry(
            metric="dfs.datanode.BlocksGetLocalPathInfo",
            label="Blocks get local path info",
            keywords=("blocks", "local", "path", "info"),
            unit="count",
        ),
        CatalogEntry(
            metric="dfs.datanode.CopyBlockOpAvgTime",
            label="Copy block avg time",
            keywords=("copy", "block", "average", "time"),
            unit="ms",
        ),
        CatalogEntry(
            metric="dfs.datanode.CopyBlockOpNumOps",
            label="Copy block operations",
            keywords=("copy", "block", "ops"),
            unit="ops",
        ),
        CatalogEntry(
            metric="dfs.datanode.DataNodeBlockRecoveryWorkerCount",
            label="Block recovery worker count",
            keywords=("block", "recovery", "worker", "count"),
            unit="count",
        ),
        CatalogEntry(
            metric="dfs.datanode.IncrementalBlockReportsAvgTime",
            label="Incremental block reports avg time",
            keywords=("incremental", "block", "reports", "average"),
            unit="ms",
        ),
        CatalogEntry(
            metric="dfs.datanode.IncrementalBlockReportsNumOps",
            label="Incremental block reports operations",
            keywords=("incremental", "block", "reports", "ops"),
            unit="ops",
        ),
        CatalogEntry(
            metric="dfs.datanode.RamDiskBlocksDeletedBeforeLazyPersisted",
            label="RamDisk blocks deleted before lazy persist",
            keywords=("ramdisk", "blocks", "deleted", "lazy"),
            unit="blocks",
        ),
        CatalogEntry(
            metric="dfs.datanode.RamDiskBlocksEvicted",
            label="RamDisk blocks evicted",
            keywords=("ramdisk", "blocks", "evicted"),
            unit="blocks",
        ),
        CatalogEntry(
            metric="dfs.datanode.RamDiskBlocksEvictedWithoutRead",
            label="RamDisk blocks evicted without read",
            keywords=("ramdisk", "blocks", "evicted", "read"),
            unit="blocks",
        ),
        CatalogEntry(
            metric="dfs.datanode.RamDiskBlocksEvictionWindowMsAvgTime",
            label="RamDisk blocks eviction window avg time",
            keywords=("ramdisk", "blocks", "eviction", "average"),
            unit="ms",
        ),
        CatalogEntry(
            metric="dfs.datanode.RamDiskBlocksEvictionWindowMsNumOps",
            label="RamDisk blocks eviction window ops",
            keywords=("ramdisk", "blocks", "eviction", "ops"),
            unit="ops",
        ),
        CatalogEntry(
            metric="dfs.datanode.RamDiskBlocksLazyPersisted",
            label="RamDisk blocks lazy persisted",
            keywords=("ramdisk", "blocks", "lazy", "persist"),
            unit="blocks",
        ),
        CatalogEntry(
            metric="dfs.datanode.RamDiskBlocksLazyPersistWindowMsAvgTime",
            label="RamDisk blocks lazy persist window avg time",
            keywords=("ramdisk", "blocks", "lazy", "persist", "average"),
            unit="ms",
        ),
        CatalogEntry(
            metric="dfs.datanode.RamDiskBlocksLazyPersistWindowMsNumOps",
            label="RamDisk blocks lazy persist window ops",
            keywords=("ramdisk", "blocks", "lazy", "persist", "ops"),
            unit="ops",
        ),
        CatalogEntry(
            metric="dfs.datanode.RamDiskBlocksReadHits",
            label="RamDisk blocks read hits",
            keywords=("ramdisk", "blocks", "read", "hits"),
            unit="blocks",
        ),
        CatalogEntry(
            metric="dfs.datanode.RamDiskBlocksWrite",
            label="RamDisk blocks write",
            keywords=("ramdisk", "blocks", "write"),
            unit="blocks",
        ),
        CatalogEntry(
            metric="dfs.datanode.RamDiskBlocksWriteFallback",
            label="RamDisk blocks write fallback",
            keywords=("ramdisk", "blocks", "write", "fallback"),
            unit="blocks",
        ),
        CatalogEntry(
            metric="dfs.datanode.ReadBlockOpAvgTime",
            label="Read block avg time",
            keywords=("read", "block", "average", "time"),
            unit="ms",
        ),
        CatalogEntry(
            metric="dfs.datanode.ReadBlockOpNumOps",
            label="Read block operations",
            keywords=("read", "block", "ops"),
            unit="ops",
        ),
        CatalogEntry(
            metric="dfs.datanode.ReplaceBlockOpAvgTime",
            label="Replace block avg time",
            keywords=("replace", "block", "average", "time"),
            unit="ms",
        ),
        CatalogEntry(
            metric="dfs.datanode.ReplaceBlockOpNumOps",
            label="Replace block operations",
            keywords=("replace", "block", "ops"),
            unit="ops",
        ),
        CatalogEntry(
            metric="dfs.datanode.SendDataPacketBlockedOnNetworkNanosAvgTime",
            label="Send data packet blocked avg time",
            keywords=("send", "data", "packet", "blocked", "average"),
            unit="ns",
        ),
        CatalogEntry(
            metric="dfs.datanode.SendDataPacketBlockedOnNetworkNanosNumOps",
            label="Send data packet blocked ops",
            keywords=("send", "data", "packet", "blocked", "ops"),
            unit="ops",
        ),
        CatalogEntry(
            metric="dfs.datanode.WriteBlockOpAvgTime",
            label="Write block avg time",
            keywords=("write", "block", "average", "time"),
            unit="ms",
        ),
        CatalogEntry(
            metric="dfs.datanode.WriteBlockOpNumOps",
            label="Write block operations",
            keywords=("write", "block", "ops"),
            unit="ops",
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
        CatalogEntry(
            metric="jvm.JvmMetrics.MemHeapUsedM",
            label="NodeManager JVM heap used",
            keywords=("heap", "memory", "jvm", "usage", "used", "nodemanager"),
            unit="MB",
        ),
        CatalogEntry(
            metric="jvm.JvmMetrics.ThreadsBlocked",
            label="NodeManager JVM threads blocked",
            keywords=("jvm", "threads", "thread", "blocked", "waiting", "nodemanager"),
            unit="threads",
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
        CatalogEntry(
            metric="jvm.JvmMetrics.ThreadsBlocked",
            label="ResourceManager JVM threads blocked",
            keywords=("jvm", "threads", "thread", "blocked", "waiting", "resourcemanager"),
            unit="threads",
        ),
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

_DATANODE_BLOCK_EXTRA_KEYWORDS: Tuple[str, ...] = ("datanode", "dfs", "host")
_DATANODE_RAMDIST_EXTRA_KEYWORDS: Tuple[str, ...] = ("ramdisk", "host")


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


def _normalize_common_metric_key(metric: str) -> str:
    return " ".join(metric.strip().lower().split()) if metric else ""


_COMMON_JVM_METRIC_LOOKUP = {
    _normalize_common_metric_key(metric): metric for metric in COMMON_JVM_METRICS
}


def resolve_common_jvm_metric_name(metric_name: Optional[str]) -> Optional[str]:
    """Return the canonical JVM metric name when it belongs to the common set."""

    if not metric_name:
        return None

    normalized = _normalize_common_metric_key(metric_name)
    return _COMMON_JVM_METRIC_LOOKUP.get(normalized)


def is_common_jvm_metric(metric_name: Optional[str]) -> bool:
    """Return True if the metric belongs to the shared JVM metric set."""

    return resolve_common_jvm_metric_name(metric_name) is not None


def _dedupe_keywords(keywords: Iterable[str]) -> Tuple[str, ...]:
    seen = set()
    result: List[str] = []

    for keyword in keywords:
        lowered = keyword.lower()
        if lowered in seen:
            continue
        seen.add(lowered)
        result.append(keyword)

    return tuple(result)


def _prioritize_datanode_block_metrics() -> None:
    entries = list(CURATED_METRICS.get("datanode", ()))
    if not entries:
        return

    entry_map: Dict[str, CatalogEntry] = {entry.metric: entry for entry in entries}
    prioritized: List[CatalogEntry] = []

    for metric in DATANODE_BLOCK_METRICS:
        entry = entry_map.get(metric)
        if not entry:
            continue

        if "RamDisk" in metric:
            extra_keywords = _DATANODE_RAMDIST_EXTRA_KEYWORDS
        else:
            extra_keywords = _DATANODE_BLOCK_EXTRA_KEYWORDS

        merged_keywords = _dedupe_keywords(entry.keywords + extra_keywords)
        if merged_keywords != entry.keywords:
            entry = CatalogEntry(
                metric=entry.metric,
                label=entry.label,
                keywords=merged_keywords,
                unit=entry.unit,
                description=entry.description,
            )

        prioritized.append(entry)

    remaining = [entry for entry in entries if entry.metric not in DATANODE_BLOCK_METRICS]
    prioritized.extend(remaining)

    CURATED_METRICS["datanode"] = tuple(prioritized)


_prioritize_datanode_block_metrics()


_METRIC_TO_APP_INDEX: Dict[str, str] = {}


def _rebuild_metric_to_app_index() -> None:
    _METRIC_TO_APP_INDEX.clear()
    for app_name, entries in CURATED_METRICS.items():
        for entry in entries:
            if entry.metric not in _METRIC_TO_APP_INDEX:
                _METRIC_TO_APP_INDEX[entry.metric] = app_name


_rebuild_metric_to_app_index()


def catalog_app_for_metric(metric_name: str) -> Optional[str]:
    """Return the catalog appId for a metric (if it is curated)."""

    if not metric_name:
        return None
    return _METRIC_TO_APP_INDEX.get(metric_name)


def is_datanode_block_metric(metric_name: Optional[str]) -> bool:
    """Return True when the metric is part of the curated DataNode block set."""

    if not metric_name:
        return False
    return metric_name in DATANODE_BLOCK_METRICS


def resolve_datanode_block_metric_name(metric_name: Optional[str]) -> Optional[str]:
    """Resolve common aliases to the canonical DataNode block metric name."""

    if not metric_name:
        return None

    candidate = metric_name.strip()
    if not candidate:
        return None

    lowered = candidate.lower()
    prefix = "dfs.datanode."

    best_match: Optional[str] = None
    best_score = -1

    for actual in DATANODE_BLOCK_METRICS:
        actual_lower = actual.lower()
        if lowered == actual_lower:
            return actual

        actual_core = actual_lower[len(prefix):] if actual_lower.startswith(prefix) else actual_lower
        candidate_core = lowered[len(prefix):] if lowered.startswith(prefix) else lowered

        if candidate_core == actual_core:
            return actual

        score = 0
        if actual_core.startswith(candidate_core):
            score = max(score, len(candidate_core))
        if candidate_core.startswith(actual_core):
            score = max(score, len(actual_core))
        if candidate_core in actual_core:
            score = max(score, len(candidate_core))

        if score > best_score:
            best_score = score
            best_match = actual

    # Require a minimum overlap to avoid noisy matches
    if best_score >= 4:
        return best_match

    return None


APP_SYNONYMS: Dict[str, Tuple[str, ...]] = {
    "HOST": ("host", "hardware", "system"),
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

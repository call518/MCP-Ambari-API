"""Regression tests for all-services operations and AMS outage handling."""

import pytest
from fastmcp import Client

import mcp_ambari_api.functions as functions
import mcp_ambari_api.mcp_main as mcp_main
from mcp_ambari_api.mcp_main import ALL_SERVICES_ALREADY_STOPPED, mcp

AMS_DOWN = "ERROR: Ambari Metrics Service is unavailable."


@pytest.fixture
def anyio_backend():
    return "asyncio"


@pytest.fixture
def fresh_metric_caches(monkeypatch):
    monkeypatch.setattr(functions, "_DYNAMIC_CATALOG_CACHE", {})
    monkeypatch.setattr(functions, "_METRICS_METADATA_CACHE", {})


@pytest.mark.anyio
async def test_stop_all_fallback_sends_alt_payload(monkeypatch):
    puts = []

    async def fake_request(endpoint, method="GET", data=None):
        if method == "GET":
            return {"items": [{"ServiceInfo": {"service_name": "HDFS"}}]}
        puts.append((endpoint, data))
        if len(puts) == 1:
            return {"error": "HTTP 400: bulk request rejected"}
        return {"Requests": {"id": 7, "status": "Accepted"}}

    monkeypatch.setattr(mcp_main, "make_ambari_request", fake_request)
    result = await mcp_main._stop_all_services()

    assert "Request ID: 7" in result
    endpoint, data = puts[1]
    assert endpoint.endswith("/services?ServiceInfo/state=STARTED")
    assert data == {"ServiceInfo": {"state": "INSTALLED"}}


@pytest.mark.anyio
async def test_restart_all_starts_when_everything_is_already_stopped(monkeypatch):
    async def already_stopped():
        return ALL_SERVICES_ALREADY_STOPPED

    async def started():
        return "Start All Services Operation Initiated:\nRequest ID: 42\n"

    monkeypatch.setattr(mcp_main, "_stop_all_services", already_stopped)
    monkeypatch.setattr(mcp_main, "_start_all_services", started)
    result = await mcp_main._restart_all_services()

    assert not result.startswith("Error"), result
    assert "Stop Request ID: N/A (already stopped)" in result
    assert "Start Request ID: 42" in result


@pytest.mark.anyio
@pytest.mark.parametrize(
    ("tool", "args"),
    [
        ("get_ambari_metrics", {"metric_names": "cpu_user", "app_id": "HOST"}),
        ("get_ambari_metric_apps", {"refresh": True}),
        ("get_common_metrics_catalog", {"search": "heap"}),
        ("get_ambari_metrics_metadata", {"app_id": "namenode"}),
    ],
)
async def test_metric_tools_report_ams_outage(monkeypatch, tool, args):
    async def unavailable():
        return False, "Cannot connect to Ambari Metrics Service."

    monkeypatch.setattr(mcp_main, "check_ams_availability", unavailable)
    async with Client(mcp) as client:
        result = await client.call_tool(tool, args)
    text = result.content[0].text
    assert text.startswith(AMS_DOWN), text
    assert "\\n" not in text


@pytest.mark.anyio
async def test_catalog_resource_raises_on_ams_outage(monkeypatch):
    async def unavailable():
        return False, "Cannot connect to Ambari Metrics Service."

    monkeypatch.setattr(mcp_main, "check_ams_availability", unavailable)
    async with Client(mcp) as client:
        with pytest.raises(Exception, match="Ambari Metrics Service is unavailable"):
            await client.read_resource("ambari-metrics://catalog/apps")


@pytest.mark.anyio
async def test_failed_ams_metadata_is_not_cached(monkeypatch, fresh_metric_caches):
    ams_up = False

    async def fake_ams(endpoint, params=None, method="GET"):
        if not ams_up:
            return {"error": "Metrics request failed: connection refused"}
        return {
            "metrics": {"namenode": [{"metricname": "jvm.JvmMetrics.MemHeapUsedM"}]}
        }

    monkeypatch.setattr(functions, "make_ambari_metrics_request", fake_ams)

    catalog, _ = await functions.ensure_metric_catalog()
    assert not any(catalog.values())
    assert functions._DYNAMIC_CATALOG_CACHE == {}
    assert functions._METRICS_METADATA_CACHE == {}

    ams_up = True
    catalog, _ = await functions.ensure_metric_catalog()
    assert catalog["namenode"] == ["jvm.JvmMetrics.MemHeapUsedM"]
    assert functions._DYNAMIC_CATALOG_CACHE["catalog"] is catalog

"""Verify the read (get_*) / write (set_*) tool split and read-only mode."""

import pytest
from fastmcp import Client
from fastmcp.exceptions import ToolError

import mcp_ambari_api.mcp_main as mcp_main
from mcp_ambari_api.mcp_main import WRITE_TOOL_TAG, mcp

WRITE_TOOLS = {
    "set_service_state",
    "set_all_services_state",
    "set_host_component_state",
}


@pytest.fixture
def anyio_backend():
    return "asyncio"


@pytest.fixture
def run_main(monkeypatch):
    """Run main() without starting a transport; restore write tools afterwards."""
    monkeypatch.setattr(mcp, "run", lambda *args, **kwargs: None)
    monkeypatch.delenv("MCP_READ_ONLY", raising=False)
    yield mcp_main.main
    mcp.enable(tags={WRITE_TOOL_TAG})


async def _list_tools():
    async with Client(mcp) as client:
        return await client.list_tools()


def _tags(tool) -> set[str]:
    return set((tool.meta or {}).get("fastmcp", {}).get("tags", []))


@pytest.mark.anyio
async def test_every_tool_is_get_or_set_with_matching_annotations():
    tools = await _list_tools()
    assert {t.name for t in tools if t.name.startswith("set_")} == WRITE_TOOLS
    for tool in tools:
        assert tool.name.startswith(("get_", "set_")), tool.name
        is_write = tool.name.startswith("set_")
        assert tool.annotations.readOnlyHint is (not is_write), tool.name
        assert _tags(tool) == ({"write"} if is_write else {"read"}), tool.name
        if is_write:
            assert tool.annotations.destructiveHint is True, tool.name


@pytest.mark.anyio
async def test_write_tools_accept_only_start_stop_restart():
    for tool in await _list_tools():
        if tool.name in WRITE_TOOLS:
            action = tool.inputSchema["properties"]["action"]
            assert action["enum"] == ["start", "stop", "restart"]
    async with Client(mcp) as client:
        with pytest.raises(ToolError):
            await client.call_tool(
                "set_service_state", {"service_name": "HDFS", "action": "pause"}
            )


@pytest.mark.anyio
@pytest.mark.parametrize("action", ["start", "stop", "restart"])
async def test_set_tools_dispatch_to_matching_operation(monkeypatch, action):
    calls = []

    def fake(name):
        async def handler(*args):
            calls.append((name, args))
            return f"{name} ok"

        return handler

    for scope in ("service", "all_services", "host_component"):
        helper = f"_{action}_{scope}"
        monkeypatch.setattr(mcp_main, helper, fake(helper))

    async with Client(mcp) as client:
        await client.call_tool(
            "set_service_state", {"service_name": "HDFS", "action": action}
        )
        await client.call_tool("set_all_services_state", {"action": action})
        await client.call_tool(
            "set_host_component_state",
            {"host_name": "node1", "component_name": "DATANODE", "action": action},
        )

    assert calls == [
        (f"_{action}_service", ("HDFS",)),
        (f"_{action}_all_services", ()),
        (f"_{action}_host_component", ("node1", "DATANODE")),
    ]


@pytest.mark.anyio
@pytest.mark.parametrize(
    "tool", ["get_service_status", "get_service_components", "get_service_details"]
)
async def test_service_read_tools_report_ambari_errors(monkeypatch, tool):
    async def fake_request(endpoint, method="GET", data=None):
        if "/services/" in endpoint:
            return {"error": "HTTP 404: Service not found"}
        return {"Clusters": {}}

    monkeypatch.setattr(mcp_main, "make_ambari_request", fake_request)
    async with Client(mcp) as client:
        result = await client.call_tool(tool, {"service_name": "NOSUCH"})
    text = result.content[0].text
    assert text.startswith("Error:"), text
    assert "HTTP 404" in text


@pytest.mark.anyio
async def test_read_only_flag_hides_and_blocks_write_tools(run_main):
    run_main(["--read-only"])
    names = {t.name for t in await _list_tools()}
    assert names and not names & WRITE_TOOLS
    assert all(name.startswith("get_") for name in names)
    async with Client(mcp) as client:
        with pytest.raises(ToolError):
            await client.call_tool("set_all_services_state", {"action": "stop"})


@pytest.mark.anyio
async def test_read_only_env_and_cli_precedence(run_main, monkeypatch):
    monkeypatch.setenv("MCP_READ_ONLY", "true")
    run_main(["--read-write"])
    assert WRITE_TOOLS <= {t.name for t in await _list_tools()}

    monkeypatch.setenv("MCP_READ_ONLY", "false")
    run_main(["--read-only"])
    assert not {t.name for t in await _list_tools()} & WRITE_TOOLS


@pytest.mark.anyio
async def test_write_tools_hidden_by_default(run_main):
    run_main([])
    assert not {t.name for t in await _list_tools()} & WRITE_TOOLS


@pytest.mark.anyio
@pytest.mark.parametrize(
    ("value", "write_enabled"),
    [
        ("false", True),
        ("0", True),
        ("No", True),
        (" OFF ", True),
        ("true", False),
        ("1", False),
        ("", False),
        ("maybe", False),
    ],
)
async def test_read_only_env_values(run_main, monkeypatch, value, write_enabled):
    monkeypatch.setenv("MCP_READ_ONLY", value)
    run_main([])
    exposed = WRITE_TOOLS <= {t.name for t in await _list_tools()}
    assert exposed is write_enabled

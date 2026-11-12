"""Verify that server instructions replace the former MCP prompt templates."""

import pytest
from fastmcp import Client

from mcp_ambari_api.mcp_main import SERVER_INSTRUCTIONS, mcp

# Claude Code truncates server instructions beyond this many characters.
CLAUDE_CODE_INSTRUCTIONS_LIMIT = 4096


@pytest.fixture
def anyio_backend():
    return "asyncio"


def test_instructions_are_non_empty_and_within_limit():
    assert SERVER_INSTRUCTIONS.strip()
    assert len(SERVER_INSTRUCTIONS) <= CLAUDE_CODE_INSTRUCTIONS_LIMIT
    assert mcp.instructions == SERVER_INSTRUCTIONS


@pytest.mark.anyio
async def test_client_receives_instructions_and_no_prompts():
    # FastMCP 3.4.x clients use the initialize handshake; the instructions
    # are exposed on the stored InitializeResult.
    async with Client(mcp) as client:
        assert client.initialize_result is not None
        assert client.initialize_result.instructions == SERVER_INSTRUCTIONS
        assert await client.list_prompts() == []
        tool_names = {tool.name for tool in await client.list_tools()}
        assert "get_prompt_template" not in tool_names

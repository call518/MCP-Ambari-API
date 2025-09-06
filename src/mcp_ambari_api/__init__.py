# Package initializer for mcp_ambari_api
# This file marks this directory as a Python package.
from .mcp_main import *  # noqa: F401,F403

__all__ = [
	# tools (selective explicit export for tests / external use)
	'get_prompt_template'
]

import re
from mcp_ambari_api import get_prompt_template
import asyncio


def test_full_template_contains_version():
    txt = asyncio.run(get_prompt_template())
    assert 'Template-Version:' in txt


def test_headings_mode():
    headings = asyncio.run(get_prompt_template(mode='headings'))
    assert 'Section Headings:' in headings
    assert 'Purpose' in headings


def test_section_fetch_by_number():
    sec = asyncio.run(get_prompt_template('3'))  # Tool Map
    assert 'Tool Map' in sec
    assert '| get_cluster_info' in sec


def test_section_fetch_by_keyword():
    sec = asyncio.run(get_prompt_template('decision flow'))
    assert 'Decision Flow' in sec
    # Decision flow lists references like get_cluster_services / get_service_status etc.
    assert 'get_cluster_services' in sec and 'get_service_status' in sec

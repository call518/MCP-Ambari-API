"""
Test user management tools - list_users and get_user
"""
import asyncio
from mcp_ambari_api import list_users, get_user


def test_list_users_function_structure():
    """Test that list_users function is properly structured"""
    # Test that the function exists and is async
    assert asyncio.iscoroutinefunction(list_users)
    

def test_get_user_function_structure():
    """Test that get_user function is properly structured"""
    # Test that the function exists and is async
    assert asyncio.iscoroutinefunction(get_user)


def test_get_user_empty_username():
    """Test get_user with empty username"""
    result = asyncio.run(get_user(""))
    assert "Error: user_name parameter is required" in result
    
    result = asyncio.run(get_user(None))
    assert "Error: user_name parameter is required" in result


def test_user_tools_exist_and_importable():
    """Test that user tools can be imported and have correct signatures"""
    from inspect import signature
    
    # Check list_users signature
    list_users_sig = signature(list_users)
    assert len(list_users_sig.parameters) == 0  # No parameters
    
    # Check get_user signature
    get_user_sig = signature(get_user)
    assert len(get_user_sig.parameters) == 1  # One parameter: user_name
    assert 'user_name' in get_user_sig.parameters

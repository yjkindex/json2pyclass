"""Tests for JSON structure analyzer."""

import json
from pathlib import Path
from json2pytype.structure_analyzer import analyze_json_structure


def test_analyze_simple_json():
    json_data = {
        "name": "Test",
        "age": 30,
        "is_active": True
    }
    
    result = analyze_json_structure(json_data, "TestClass")
    
    assert result["name"] == "TestClass"
    assert "fields" in result
    
    fields = result["fields"]
    assert len(fields) == 3
    assert "name" in fields
    assert fields["name"]["type"] == "str"
    assert "age" in fields
    assert fields["age"]["type"] == "int"
    assert "is_active" in fields
    assert fields["is_active"]["type"] == "bool"


def test_analyze_nested_json():
    json_data = {
        "user": {
            "name": "John",
            "address": {
                "street": "Main St",
                "zipcode": "12345"
            }
        }
    }
    
    result = analyze_json_structure(json_data, "Root")
    
    assert result["name"] == "Root"
    assert "user" in result["fields"]
    
    user_field = result["fields"]["user"]
    assert user_field["is_custom_class"] is True
    assert user_field["type"] == "RootUser"
    
    user_class = user_field["info"]
    assert user_class["name"] == "RootUser"
    assert "address" in user_class["fields"]
    
    address_field = user_class["fields"]["address"]
    assert address_field["is_custom_class"] is True
    assert address_field["type"] == "RootUserAddress"


def test_analyze_list_json():
    json_data = {
        "items": [1, 2, 3, 4]
    }
    
    result = analyze_json_structure(json_data, "ListTest")
    
    assert result["name"] == "ListTest"
    assert "items" in result["fields"]
    
    items_field = result["fields"]["items"]
    assert items_field["is_list"] is True
    assert items_field["type"] == "List[int]"
    assert items_field["list_element_type"] == "int"
    assert items_field["list_element_is_custom"] is False


def test_analyze_list_of_objects():
    json_data = {
        "users": [
            {"name": "John", "age": 30},
            {"name": "Jane", "age": 25}
        ]
    }
    
    result = analyze_json_structure(json_data, "UserList")
    
    assert result["name"] == "UserList"
    assert "users" in result["fields"]
    
    users_field = result["fields"]["users"]
    assert users_field["is_list"] is True
    assert users_field["type"] == "List[UsersItem]"
    assert users_field["list_element_type"] == "UsersItem"
    assert users_field["list_element_is_custom"] is True


def test_analyze_root_list():
    json_data = [
        {"name": "Item 1"},
        {"name": "Item 2"}
    ]
    
    result = analyze_json_structure(json_data, "RootList")
    
    assert result["name"] == "RootList"
    assert "items" in result["fields"]
    
    items_field = result["fields"]["items"]
    assert items_field["is_list"] is True
    assert items_field["type"] == "List[Item]"
    assert items_field["list_element_type"] == "Item"

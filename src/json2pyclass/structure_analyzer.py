"""
JSON structure analyzer.

Analyzes JSON data structures to generate class definition information
that can be used to create Python classes with proper type hints.
"""

from typing import Any, Dict, List, Optional
from .naming import camel_to_snake, snake_to_pascal
from .type_inference import get_python_type


def analyze_json_structure(json_data: Any, class_name: str = "Root") -> Dict[str, Any]:
    """
    Analyze a JSON data structure and generate class definition information.

    Args:
        json_data: The JSON data to analyze
        class_name: Name for the root class

    Returns:
        Dictionary containing class definition information with fields,
        types, and nested class information
    """
    if isinstance(json_data, dict):
        class_info: Dict[str, Any] = {
            "name": class_name,
            "type": "class",
            "fields": {}
        }
        
        for key, value in json_data.items():
            # Convert key to snake_case for class attribute
            field_name = camel_to_snake(key)
            # Convert key to PascalCase for potential nested class name
            pascal_key = snake_to_pascal(camel_to_snake(key))
            
            if isinstance(value, dict):
                # Create new class for nested object
                nested_class_name = f"{class_name}{pascal_key}"
                nested_class_info = analyze_json_structure(value, nested_class_name)
                class_info["fields"][field_name] = {
                    "type": nested_class_name,
                    "info": nested_class_info,
                    "is_custom_class": True,
                    "is_list": False,
                    "list_element_type": None,
                    "list_element_is_custom": False
                }
            elif isinstance(value, list):
                if value and isinstance(value[0], dict):
                    # Create new class for objects in list
                    element_class_name = f"{pascal_key}Item"
                    element_class_info = analyze_json_structure(value[0], element_class_name)
                    class_info["fields"][field_name] = {
                        "type": f"List[{element_class_name}]",
                        "info": element_class_info,
                        "is_custom_class": False,
                        "is_list": True,
                        "list_element_type": element_class_name,
                        "list_element_is_custom": True
                    }
                else:
                    # List of basic types
                    element_type = get_python_type(value[0]) if value else "Any"
                    class_info["fields"][field_name] = {
                        "type": f"List[{element_type}]",
                        "info": None,
                        "is_custom_class": False,
                        "is_list": True,
                        "list_element_type": element_type,
                        "list_element_is_custom": False
                    }
            else:
                # Basic type
                class_info["fields"][field_name] = {
                    "type": get_python_type(value),
                    "info": None,
                    "is_custom_class": False,
                    "is_list": False,
                    "list_element_type": None,
                    "list_element_is_custom": False
                }
        
        return class_info
    
    elif isinstance(json_data, list) and json_data and isinstance(json_data[0], dict):
        # Root is a list of objects, create a container class
        element_class_name = snake_to_pascal("item")
        element_class_info = analyze_json_structure(json_data[0], element_class_name)
        return {
            "name": class_name,
            "type": "class",
            "fields": {
                "items": {
                    "type": f"List[{element_class_name}]",
                    "info": element_class_info,
                    "is_custom_class": False,
                    "is_list": True,
                    "list_element_type": element_class_name,
                    "list_element_is_custom": True
                }
            }
        }
    else:
        # Simple type at root, create a wrapper class
        return {
            "name": class_name,
            "type": "class",
            "fields": {
                "value": {
                    "type": get_python_type(json_data),
                    "info": None,
                    "is_custom_class": False,
                    "is_list": False,
                    "list_element_type": None,
                    "list_element_is_custom": False
                }
            }
        }

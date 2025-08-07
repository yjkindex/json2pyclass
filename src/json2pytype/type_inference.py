"""
Type inference utilities.

Provides functionality to determine Python types from JSON values.
"""

from typing import Any, List, Dict


def get_python_type(json_value: Any) -> str:
    """
    Determine the corresponding Python type string from a JSON value.

    Args:
        json_value: A JSON value (int, str, bool, list, dict, None, etc.)

    Returns:
        String representation of the corresponding Python type
    """
    if isinstance(json_value, bool):
        return "bool"
    elif isinstance(json_value, int):
        return "int"
    elif isinstance(json_value, float):
        return "float"
    elif isinstance(json_value, str):
        return "str"
    elif isinstance(json_value, list):
        if not json_value:
            return "List[Any]"
        # Assume all elements in the list are of the same type
        element_type = get_python_type(json_value[0])
        return f"List[{element_type}]"
    elif isinstance(json_value, dict):
        return "Dict[str, Any]"  # Will be replaced with specific class type later
    elif json_value is None:
        return "None"
    else:
        return "Any"

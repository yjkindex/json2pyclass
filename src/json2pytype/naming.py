"""
Naming convention conversion utilities.

Provides functions to convert between different naming conventions:
- camelCase to snake_case
- snake_case to PascalCase
"""

import re
from typing import Optional


def camel_to_snake(name: str) -> str:
    """
    Convert a camelCase string to snake_case.

    Args:
        name: String in camelCase format

    Returns:
        String converted to snake_case
    """
    if not name:
        return ""
    
    # Handle consecutive uppercase letters (e.g., ABCDef -> abc_def)
    name = re.sub(r'([A-Z]+)([A-Z][a-z])', r'\1_\2', name)
    # Handle lowercase followed by uppercase (e.g., abcDef -> abc_def)
    name = re.sub(r'([a-z])([A-Z])', r'\1_\2', name)
    return name.lower()


def snake_to_pascal(name: str) -> str:
    """
    Convert a snake_case string to PascalCase.

    Args:
        name: String in snake_case format

    Returns:
        String converted to PascalCase
    """
    if not name:
        return ""
    return ''.join(word.capitalize() for word in name.split('_') if word)

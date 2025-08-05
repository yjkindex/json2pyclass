"""
json2pyclass - A tool to generate Python classes with type hints from JSON files
"""

from .code_generator import generate_class_code, generate_type_declare_file
from .naming import camel_to_snake, snake_to_pascal
from .structure_analyzer import analyze_json_structure
from .type_inference import get_python_type

__version__ = "0.1.0"
__all__ = [
    "camel_to_snake",
    "snake_to_pascal",
    "get_python_type",
    "analyze_json_structure",
    "generate_class_code",
    "generate_type_declare_file",
]

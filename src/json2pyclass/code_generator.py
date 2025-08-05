"""
Code generator.

Generates Python class code with type hints based on analyzed JSON structures.
"""

import json
import os
from typing import Any, Dict, List, Optional, Set
from .structure_analyzer import analyze_json_structure
from .naming import snake_to_pascal


def generate_class_code(class_info: Dict[str, Any], imported_classes: Set[str] = None) -> str:
    """
    Generate Python class code from class information.

    Args:
        class_info: Dictionary containing class definition information
        imported_classes: Set to track imported classes to avoid duplicates

    Returns:
        String containing the generated Python class code
    """
    if imported_classes is None:
        imported_classes = set()
        
    code: List[str] = []
    class_name = class_info["name"]
    imported_classes.add(class_name)
    
    # Collect nested classes
    nested_classes: List[str] = []
    for field in class_info["fields"].values():
        if field["info"]:
            nested_class_code = generate_class_code(field["info"], imported_classes)
            if nested_class_code not in nested_classes:
                nested_classes.append(nested_class_code)
    
    # Generate current class code
    code.append(f"class {class_name}:")
    
    # Generate class attributes with type hints
    for field_name, field_info in class_info["fields"].items():
        code.append(f"    {field_name}: {field_info['type']}")
    
    # Generate __init__ method
    code.append("")
    code.append("    def __init__(self, data: dict):")
    
    # Initialize each field
    for field_name, field_info in class_info["fields"].items():
        # Convert snake_case back to camelCase for JSON key
        json_key = field_name
        if '_' in field_name:
            json_key = ''.join(word.capitalize() for word in field_name.split('_'))
            json_key = json_key[0].lower() + json_key[1:]
        
        if field_info["is_custom_class"]:
            # Initialize custom class
            code.append(f"        self.{field_name} = {field_info['type']}(data.get('{json_key}', {{}}))")
        elif field_info["is_list"]:
            if field_info["list_element_is_custom"]:
                # Initialize list of custom classes
                code.append(f"        self.{field_name} = [")
                code.append(f"            {field_info['list_element_type']}(item) "
                            f"for item in data.get('{json_key}', [])")
                code.append(f"        ]")
            else:
                # Initialize list of basic types
                code.append(f"        self.{field_name} = data.get('{json_key}', [])")
        else:
            # Initialize basic type
            code.append(f"        self.{field_name} = data.get('{json_key}')")

    code.append("")
    
    # Generate __call__ method to convert back to dictionary
    code.append("    def __call__(self) -> dict:")
    code.append("        result = {}")
    for field_name, field_info in class_info["fields"].items():
        # Convert snake_case back to camelCase for JSON key
        json_key = field_name
        if '_' in field_name:
            json_key = ''.join(word.capitalize() for word in field_name.split('_'))
            json_key = json_key[0].lower() + json_key[1:]
            
        if field_info["is_custom_class"]:
            code.append(f"        result['{json_key}'] = self.{field_name}() if self.{field_name} else None")
        elif field_info["is_list"] and field_info["list_element_is_custom"]:
            code.append(f"        result['{json_key}'] = [item() for item in self.{field_name}] if self.{field_name} else []")
        else:
            code.append(f"        result['{json_key}'] = self.{field_name}")
    code.append("        return result")
    code.append("")
    
    # Combine nested classes and current class code
    return "\n".join(nested_classes + code)


def generate_type_declare_file(json_path: str, output_path: Optional[str] = None) -> None:
    """
    Generate a Python file with type declarations from a JSON file.

    Args:
        json_path: Path to the input JSON file
        output_path: Path for the output Python file (optional)
    """
    # Read JSON data
    with open(json_path, 'r', encoding='utf-8') as f:
        json_data = json.load(f)
    
    # Extract root class name from JSON filename
    file_name = os.path.splitext(os.path.basename(json_path))[0]
    root_class_name = snake_to_pascal(file_name)
    
    # Analyze JSON structure
    class_info = analyze_json_structure(json_data, root_class_name)
    
    # Generate class code
    imported_classes: Set[str] = set()
    class_code = generate_class_code(class_info, imported_classes)
    
    # Determine output path
    if not output_path:
        output_path = json_path.replace(".json", ".py")
    
    # Generate import statements
    imports = ["from typing import List, Dict, Any, Optional"]
    
    # Write output file
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("\n".join(imports) + "\n\n")
        f.write(class_code)
    
    print(f"Type declaration file generated: {output_path}")

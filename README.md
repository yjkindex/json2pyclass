# JSON to Python Class Generator

A tool that converts JSON files into Python classes with type hints, making it easier to work with structured JSON data in Python.

## Features

- Converts JSON structures to Python classes with proper type annotations
- Handles nested objects and arrays
- Maintains proper naming conventions (camelCase to snake_case, etc.)
- Generates `__init__` method for object initialization
- Includes `__call__` method to convert back to dictionary

## Installation

### From Source
# Clone the repository
```bash
git clone https://github.com/yourusername/json2pyclass.git
cd json2pyclass
```
# Install with pip
pip install .

# For development (includes testing dependencies)
pip install ".[dev]"
## Usage

### Command Line Interface
# Basic usage
json2pyclass input.json -o output.py

# If output path is not specified, it will use input filename with .py extension
json2pyclass data.json
### As a Library
from json2pyclass import generate_type_declare_file

# Generate Python classes from JSON file
generate_type_declare_file("input.json", "output.py")
## Example

For a JSON file like this:
{
  "userName": "john_doe",
  "age": 30,
  "isActive": true,
  "address": {
    "street": "123 Main St",
    "city": "Anytown"
  },
  "hobbies": ["reading", "hiking"]
}
The tool will generate a Python file with classes:
from typing import List, Dict, Any, Optional

class Address:
    street: str
    city: str

    def __init__(self, data: dict):
        self.street = data.get('street')
        self.city = data.get('city')
        pass

    def __call__(self) -> dict:
        result = {}
        result['street'] = self.street
        result['city'] = self.city
        return result

class User:
    user_name: str
    age: int
    is_active: bool
    address: Address
    hobbies: List[str]

    def __init__(self, data: dict):
        self.user_name = data.get('userName')
        self.age = data.get('age')
        self.is_active = data.get('isActive')
        self.address = Address(data.get('address', {}))
        self.hobbies = data.get('hobbies', [])
        pass

    def __call__(self) -> dict:
        result = {}
        result['userName'] = self.user_name
        result['age'] = self.age
        result['isActive'] = self.is_active
        result['address'] = self.address() if self.address else None
        result['hobbies'] = self.hobbies
        return result
## Testing

Run the test suite with:
pytest
## License

This project is licensed under the MIT License - see the LICENSE file for details.

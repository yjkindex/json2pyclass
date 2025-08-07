"""Tests for code generator."""

from json2pytype.structure_analyzer import analyze_json_structure
from json2pytype.code_generator import generate_class_code


def test_generate_simple_class():
    json_data = {
        "name": "Test",
        "age": 30
    }
    
    class_info = analyze_json_structure(json_data, "TestClass")
    code = generate_class_code(class_info)
    
    # Check if class is generated
    assert "class TestClass:" in code
    
    # Check if attributes are present
    assert "    name: str" in code
    assert "    age: int" in code
    
    # Check if __init__ method is generated
    assert "    def __init__(self, data: dict):" in code
    assert "        self.name = data.get('name')" in code
    assert "        self.age = data.get('age')" in code
    
    # Check if __call__ method is generated
    assert "    def __call__(self) -> dict:" in code
    assert "        result['name'] = self.name" in code
    assert "        result['age'] = self.age" in code


def test_generate_nested_class():
    json_data = {
        "user": {
            "name": "John",
            "age": 30
        }
    }
    
    class_info = analyze_json_structure(json_data, "Root")
    code = generate_class_code(class_info)
    
    # Check if both classes are generated
    assert "class RootUser:" in code
    assert "class Root:" in code
    
    # Check nested class attributes
    assert "    name: str" in code
    assert "    age: int" in code
    
    # Check root class has reference to nested class
    assert "    user: RootUser" in code
    assert "        self.user = RootUser(data.get('user', {}))" in code


def test_generate_class_with_list():
    json_data = {
        "hobbies": ["reading", "sports"]
    }
    
    class_info = analyze_json_structure(json_data, "Person")
    code = generate_class_code(class_info)
    
    # Check list type
    assert "    hobbies: List[str]" in code
    
    # Check initialization
    assert "        self.hobbies = data.get('hobbies', [])" in code
    
    # Check __call__ method
    assert "        result['hobbies'] = self.hobbies" in code


def test_generate_class_with_object_list():
    json_data = {
        "users": [
            {"name": "John"},
            {"name": "Jane"}
        ]
    }
    
    class_info = analyze_json_structure(json_data, "UserList")
    code = generate_class_code(class_info)
    
    # Check if item class is generated
    assert "class UsersItem:" in code
    assert "    name: str" in code
    
    # Check list type
    assert "    users: List[UsersItem]" in code
    
    # Check list initialization
    assert "        self.users = [" in code
    assert "            UsersItem(item) for item in data.get('users', [])" in code
    
    # Check __call__ method for list
    assert "        result['users'] = [item() for item in self.users] if self.users else []" in code

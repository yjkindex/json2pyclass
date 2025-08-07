"""Tests for type inference functions."""

from json2pytype.type_inference import get_python_type


def test_get_python_type_basic_types():
    assert get_python_type(42) == "int"
    assert get_python_type(3.14) == "float"
    assert get_python_type("hello") == "str"
    assert get_python_type(True) == "bool"
    assert get_python_type(False) == "bool"
    assert get_python_type(None) == "None"


def test_get_python_type_lists():
    assert get_python_type([]) == "List[Any]"
    assert get_python_type([1, 2, 3]) == "List[int]"
    assert get_python_type(["a", "b", "c"]) == "List[str]"
    assert get_python_type([1.5, 2.5]) == "List[float]"
    assert get_python_type([True, False]) == "List[bool]"


def test_get_python_type_dict():
    assert get_python_type({}) == "Dict[str, Any]"
    assert get_python_type({"key": "value"}) == "Dict[str, Any]"


def test_get_python_type_other_types():
    # For types not directly covered, should return "Any"
    assert get_python_type(set()) == "Any"
    assert get_python_type((1, 2, 3)) == "Any"

"""Tests for naming convention conversion functions."""

from json2pytype.naming import camel_to_snake, snake_to_pascal


def test_camel_to_snake_basic():
    assert camel_to_snake("camelCase") == "camel_case"
    assert camel_to_snake("CamelCase") == "camel_case"
    assert camel_to_snake("camelTwoWords") == "camel_two_words"


def test_camel_to_snake_with_abbreviations():
    assert camel_to_snake("ABCDef") == "abc_def"
    assert camel_to_snake("XMLParser") == "xml_parser"
    assert camel_to_snake("JSONData") == "json_data"


def test_camel_to_snake_edge_cases():
    assert camel_to_snake("") == ""
    assert camel_to_snake("singleword") == "singleword"
    assert camel_to_snake("With2Numbers") == "with2_numbers"


def test_snake_to_pascal_basic():
    assert snake_to_pascal("snake_case") == "SnakeCase"
    assert snake_to_pascal("snake_two_words") == "SnakeTwoWords"


def test_snake_to_pascal_edge_cases():
    assert snake_to_pascal("") == ""
    assert snake_to_pascal("singleword") == "Singleword"
    assert snake_to_pascal("with_2_numbers") == "With2Numbers"
    assert snake_to_pascal("_leading_underscore") == "LeadingUnderscore"
    assert snake_to_pascal("trailing_underscore_") == "TrailingUnderscore"

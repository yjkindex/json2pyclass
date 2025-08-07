"""
Command Line Interface for json2pyclass.

Provides a command line interface to convert JSON files to Python classes
with type hints.
"""

import argparse
from .code_generator import generate_type_declare_file


def main() -> None:
    """Main function for the command line interface."""
    parser = argparse.ArgumentParser(description='Convert JSON files to Python classes with type hints')
    parser.add_argument('input', help='Path to the input JSON file (e.g., data.json)')
    parser.add_argument('-o', '--output', help='Path for the output Python file (default: input filename with .py extension)')
    args = parser.parse_args()
    
    generate_type_declare_file(args.input, args.output)


if __name__ == "__main__":
    main()

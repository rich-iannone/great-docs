"""
gdtest_mixed_directives — Partial directives: some objects have them, some don't.

Dimensions: A1, B1, C4, D1, E5, F6, G1, H7
Focus: 6 items — 3 with %family, 3 without. Tests graceful mixing of
       directive-based and auto-generated sections.
"""

SPEC = {
    "name": "gdtest_mixed_directives",
    "description": "Mixed: some objects with directives, some without",
    "dimensions": ["A1", "B1", "C4", "D1", "E5", "F6", "G1", "H7"],
    "pyproject_toml": {
        "project": {
            "name": "gdtest-mixed-directives",
            "version": "0.1.0",
            "description": "A synthetic test package with mixed directive usage",
        },
        "build-system": {
            "requires": ["setuptools"],
            "build-backend": "setuptools.build_meta",
        },
    },
    "files": {
        "gdtest_mixed_directives/__init__.py": '''\
            """Package with a mix of directive-annotated and plain objects."""

            __version__ = "0.1.0"
            __all__ = [
                "Parser",
                "parse_json",
                "parse_csv",
                "format_output",
                "validate_schema",
                "count_records",
            ]


            class Parser:
                """
                A data parser.

                %family Parsing

                Parameters
                ----------
                fmt
                    Input format.
                """

                def __init__(self, fmt: str = "json"):
                    self.fmt = fmt

                def parse(self, data: str) -> dict:
                    """
                    Parse input data.

                    Parameters
                    ----------
                    data
                        Raw data string.

                    Returns
                    -------
                    dict
                        Parsed data.
                    """
                    return {}


            def parse_json(data: str) -> dict:
                """
                Parse JSON data.

                %family Parsing

                Parameters
                ----------
                data
                    JSON string.

                Returns
                -------
                dict
                    Parsed dictionary.
                """
                return {}


            def parse_csv(data: str) -> list:
                """
                Parse CSV data.

                %family Parsing

                Parameters
                ----------
                data
                    CSV string.

                Returns
                -------
                list
                    List of rows.
                """
                return []


            def format_output(data: dict, fmt: str = "json") -> str:
                """
                Format data for output.

                Parameters
                ----------
                data
                    Data to format.
                fmt
                    Output format.

                Returns
                -------
                str
                    Formatted string.
                """
                return ""


            def validate_schema(data: dict, schema: dict) -> bool:
                """
                Validate data against a schema.

                Parameters
                ----------
                data
                    Data to validate.
                schema
                    Schema definition.

                Returns
                -------
                bool
                    True if valid.
                """
                return True


            def count_records(data: list) -> int:
                """
                Count records in a dataset.

                Parameters
                ----------
                data
                    List of records.

                Returns
                -------
                int
                    Number of records.
                """
                return len(data)
        ''',
        "README.md": """\
            # gdtest-mixed-directives

            A synthetic test package with mixed directive usage.
        """,
    },
    "expected": {
        "detected_name": "gdtest-mixed-directives",
        "detected_module": "gdtest_mixed_directives",
        "detected_parser": "numpy",
        "export_names": [
            "Parser",
            "parse_json",
            "parse_csv",
            "format_output",
            "validate_schema",
            "count_records",
        ],
        "num_exports": 6,
        "families": {
            "Parsing": ["Parser", "parse_json", "parse_csv"],
        },
        "unfamilied": ["format_output", "validate_schema", "count_records"],
        "has_user_guide": False,
    },
}

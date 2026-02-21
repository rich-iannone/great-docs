"""
gdtest_mixed_families — Mixed docstrings + %family directives.

Dimensions: A1, B1, C1, D5, E1, F6, G1, H7
Focus: Some functions use NumPy docstrings, others use Google, all with
       %family tags. Verifies family grouping is independent of doc style.
"""

SPEC = {
    "name": "gdtest_mixed_families",
    "description": "Mixed docstring styles with %family directives",
    "dimensions": ["A1", "B1", "C1", "D5", "E1", "F6", "G1", "H7"],
    "pyproject_toml": {
        "project": {
            "name": "gdtest-mixed-families",
            "version": "0.1.0",
            "description": "Test mixed docstrings with family grouping",
        },
        "build-system": {
            "requires": ["setuptools"],
            "build-backend": "setuptools.build_meta",
        },
    },
    "files": {
        "gdtest_mixed_families/__init__.py": '''\
            """Package with mixed docstring styles and %family directives."""

            __version__ = "0.1.0"
            __all__ = ["read_csv", "read_json", "write_csv", "write_json"]


            def read_csv(path: str) -> list:
                """
                Read a CSV file.

                %family Input

                Parameters
                ----------
                path
                    Path to CSV file.

                Returns
                -------
                list
                    Rows of data.
                """
                return []


            def read_json(path: str) -> dict:
                """Read a JSON file.

                %family Input

                Args:
                    path: Path to JSON file.

                Returns:
                    Parsed JSON data.
                """
                return {}


            def write_csv(data: list, path: str) -> None:
                """
                Write data to a CSV file.

                %family Output

                Parameters
                ----------
                data
                    Rows to write.
                path
                    Output path.
                """
                pass


            def write_json(data: dict, path: str) -> None:
                """Write data to a JSON file.

                %family Output

                Args:
                    data: Data to write.
                    path: Output path.
                """
                pass
        ''',
        "README.md": """\
            # gdtest-mixed-families

            Tests mixed docstring styles with %family directives.
        """,
    },
    "expected": {
        "detected_name": "gdtest-mixed-families",
        "detected_module": "gdtest_mixed_families",
        "detected_parser": "numpy",
        "export_names": ["read_csv", "read_json", "write_csv", "write_json"],
        "num_exports": 4,
        "section_titles": ["Functions"],
        "has_user_guide": False,
    },
}

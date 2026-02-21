"""
gdtest_src_families — src/ layout + %family directives.

Dimensions: A2, B1, C4, D1, E1, F6, G1, H7
Focus: Combines src/ layout with %family-based section grouping to verify
       both features work together without interference.
"""

SPEC = {
    "name": "gdtest_src_families",
    "description": "src/ layout combined with %family directives",
    "dimensions": ["A2", "B1", "C4", "D1", "E1", "F6", "G1", "H7"],
    "pyproject_toml": {
        "project": {
            "name": "gdtest-src-families",
            "version": "0.1.0",
            "description": "Test src/ layout with family directives",
        },
        "build-system": {
            "requires": ["setuptools"],
            "build-backend": "setuptools.build_meta",
        },
        "tool": {
            "setuptools": {
                "package-dir": {"": "src"},
            },
        },
    },
    "files": {
        "src/gdtest_src_families/__init__.py": '''\
            """Package testing src/ layout with %family directives."""

            __version__ = "0.1.0"
            __all__ = [
                "FileHandler",
                "read_file",
                "write_file",
                "transform",
                "validate",
            ]


            class FileHandler:
                """
                Handle file I/O operations.

                %family IO

                Parameters
                ----------
                path
                    File path.
                """

                def __init__(self, path: str):
                    self.path = path

                def open(self) -> None:
                    """Open the file."""
                    pass

                def close(self) -> None:
                    """Close the file."""
                    pass


            def read_file(path: str) -> str:
                """
                Read a file and return its contents.

                %family IO

                Parameters
                ----------
                path
                    Path to the file.

                Returns
                -------
                str
                    File contents.
                """
                return ""


            def write_file(path: str, data: str) -> None:
                """
                Write data to a file.

                %family IO

                Parameters
                ----------
                path
                    Path to the file.
                data
                    Data to write.
                """
                pass


            def transform(data: str) -> str:
                """
                Transform data.

                %family Transform

                Parameters
                ----------
                data
                    Data to transform.

                Returns
                -------
                str
                    Transformed data.
                """
                return data


            def validate(data: str) -> bool:
                """
                Validate data.

                %family Transform

                Parameters
                ----------
                data
                    Data to validate.

                Returns
                -------
                bool
                    True if valid.
                """
                return True
        ''',
        "README.md": """\
            # gdtest-src-families

            Tests src/ layout with %family directive grouping.
        """,
    },
    "expected": {
        "detected_name": "gdtest-src-families",
        "detected_module": "gdtest_src_families",
        "detected_parser": "numpy",
        "export_names": ["FileHandler", "read_file", "write_file", "transform", "validate"],
        "num_exports": 5,
        "section_titles": ["Classes", "Functions"],
        "has_user_guide": False,
    },
}

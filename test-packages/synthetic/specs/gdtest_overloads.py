"""
gdtest_overloads — @overload typed functions.

Dimensions: A1, B1, C15, D1, E6, F6, G1, H7
Focus: Functions with @typing.overload decorators. Tests that overloaded
       signatures render without errors.
"""

SPEC = {
    "name": "gdtest_overloads",
    "description": "Functions with @overload signatures",
    "dimensions": ["A1", "B1", "C15", "D1", "E6", "F6", "G1", "H7"],
    "pyproject_toml": {
        "project": {
            "name": "gdtest-overloads",
            "version": "0.1.0",
            "description": "Test overloaded function documentation",
        },
        "build-system": {
            "requires": ["setuptools"],
            "build-backend": "setuptools.build_meta",
        },
    },
    "files": {
        "gdtest_overloads/__init__.py": '''\
            """Package with @overload decorated functions."""

            from typing import overload, Union

            __version__ = "0.1.0"
            __all__ = ["process", "convert"]


            @overload
            def process(data: str) -> str: ...

            @overload
            def process(data: int) -> int: ...

            @overload
            def process(data: list) -> list: ...

            def process(data):
                """
                Process data of varying types.

                Parameters
                ----------
                data
                    Input data — can be str, int, or list.

                Returns
                -------
                str or int or list
                    Processed output, same type as input.
                """
                return data


            @overload
            def convert(value: str, to: type) -> int: ...

            @overload
            def convert(value: int, to: type) -> str: ...

            def convert(value, to=str):
                """
                Convert a value to a different type.

                Parameters
                ----------
                value
                    The value to convert.
                to
                    Target type.

                Returns
                -------
                int or str
                    Converted value.
                """
                return to(value)
        ''',
        "README.md": """\
            # gdtest-overloads

            Tests documentation of @overload decorated functions.
        """,
    },
    "expected": {
        "detected_name": "gdtest-overloads",
        "detected_module": "gdtest_overloads",
        "detected_parser": "numpy",
        "export_names": ["process", "convert"],
        "num_exports": 2,
        "section_titles": ["Functions"],
        "has_user_guide": False,
    },
}

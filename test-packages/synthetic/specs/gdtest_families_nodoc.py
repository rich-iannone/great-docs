"""
gdtest_families_nodoc — %family + %nodoc combined in one module.

Dimensions: A1, B1, C1, D1, E1, E4, F6, G1, H7
Focus: Mix of %family-grouped and %nodoc-hidden exports to verify
       both directives work together correctly.
"""

SPEC = {
    "name": "gdtest_families_nodoc",
    "description": "%family and %nodoc directives combined",
    "dimensions": ["A1", "B1", "C1", "D1", "E1", "E4", "F6", "G1", "H7"],
    "pyproject_toml": {
        "project": {
            "name": "gdtest-families-nodoc",
            "version": "0.1.0",
            "description": "Test %family + %nodoc in the same module",
        },
        "build-system": {
            "requires": ["setuptools"],
            "build-backend": "setuptools.build_meta",
        },
    },
    "files": {
        "gdtest_families_nodoc/__init__.py": '''\
            """Package mixing %family and %nodoc directives."""

            __version__ = "0.1.0"
            __all__ = [
                "add",
                "subtract",
                "multiply",
                "internal_calc",
                "debug_dump",
            ]


            def add(a: int, b: int) -> int:
                """
                Add two numbers.

                %family Math

                Parameters
                ----------
                a
                    First number.
                b
                    Second number.

                Returns
                -------
                int
                    Sum.
                """
                return a + b


            def subtract(a: int, b: int) -> int:
                """
                Subtract b from a.

                %family Math

                Parameters
                ----------
                a
                    First number.
                b
                    Second number.

                Returns
                -------
                int
                    Difference.
                """
                return a - b


            def multiply(a: int, b: int) -> int:
                """
                Multiply two numbers.

                %family Math

                Parameters
                ----------
                a
                    First number.
                b
                    Second number.

                Returns
                -------
                int
                    Product.
                """
                return a * b


            def internal_calc(x: int) -> int:
                """
                Internal calculation — should not appear in docs.

                %nodoc

                Parameters
                ----------
                x
                    Input value.

                Returns
                -------
                int
                    Result.
                """
                return x * x


            def debug_dump() -> None:
                """
                Debug dump — should not appear in docs.

                %nodoc
                """
                pass
        ''',
        "README.md": """\
            # gdtest-families-nodoc

            Tests %family and %nodoc directives working together.
        """,
    },
    "expected": {
        "detected_name": "gdtest-families-nodoc",
        "detected_module": "gdtest_families_nodoc",
        "detected_parser": "numpy",
        "export_names": ["add", "subtract", "multiply", "internal_calc", "debug_dump"],
        "num_exports": 5,
        "section_titles": ["Functions"],
        "has_user_guide": False,
    },
}

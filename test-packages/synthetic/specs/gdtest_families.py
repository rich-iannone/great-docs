"""
gdtest_families — %family directive for section grouping.

Dimensions: A1, B1, C4, D1, E1, F6, G1, H7
Focus: 6 functions and 1 class spread across 2 families plus 1 unfamilied
       function.  Tests that Great Docs groups objects into named sections
       based on %family directives in docstrings.
"""

SPEC = {
    "name": "gdtest_families",
    "description": "%family directive for section grouping",
    "dimensions": ["A1", "B1", "C4", "D1", "E1", "F6", "G1", "H7"],
    # ── Project metadata ─────────────────────────────────────────────
    "pyproject_toml": {
        "project": {
            "name": "gdtest-families",
            "version": "0.1.0",
            "description": "Test package for %family directive grouping",
        },
        "build-system": {
            "requires": ["setuptools"],
            "build-backend": "setuptools.build_meta",
        },
    },
    # ── Source files ──────────────────────────────────────────────────
    "files": {
        "gdtest_families/__init__.py": '''\
            """Package demonstrating %family-based API section grouping."""

            __version__ = "0.1.0"
            __all__ = [
                "Validate",
                "col_vals_gt",
                "col_vals_lt",
                "col_vals_between",
                "col_exists",
                "fmt_number",
                "fmt_percent",
                "helper",
            ]


            class Validate:
                """
                Core validation class.

                %family Validation

                Parameters
                ----------
                data
                    The data to validate.
                """

                def __init__(self, data):
                    self.data = data

                def run(self) -> bool:
                    """
                    Run all validation steps.

                    Returns
                    -------
                    bool
                        True if all steps pass.
                    """
                    return True


            def col_vals_gt(data, column: str, value: float) -> bool:
                """
                Check that column values are greater than a threshold.

                %family Validation

                Parameters
                ----------
                data
                    Input data.
                column
                    Column to check.
                value
                    Threshold value.

                Returns
                -------
                bool
                    True if all values pass.
                """
                return True


            def col_vals_lt(data, column: str, value: float) -> bool:
                """
                Check that column values are less than a threshold.

                %family Validation

                Parameters
                ----------
                data
                    Input data.
                column
                    Column to check.
                value
                    Threshold value.

                Returns
                -------
                bool
                    True if all values pass.
                """
                return True


            def col_vals_between(data, column: str, low: float, high: float) -> bool:
                """
                Check that column values are between two thresholds.

                %family Validation

                Parameters
                ----------
                data
                    Input data.
                column
                    Column to check.
                low
                    Lower bound.
                high
                    Upper bound.

                Returns
                -------
                bool
                    True if all values pass.
                """
                return True


            def col_exists(data, column: str) -> bool:
                """
                Check that a column exists in the data.

                %family Validation

                Parameters
                ----------
                data
                    Input data.
                column
                    Column name to look for.

                Returns
                -------
                bool
                    True if column exists.
                """
                return True


            def fmt_number(value: float, decimals: int = 2) -> str:
                """
                Format a number for display.

                %family Formatting

                Parameters
                ----------
                value
                    The numeric value.
                decimals
                    Number of decimal places.

                Returns
                -------
                str
                    Formatted number string.
                """
                return f"{value:.{decimals}f}"


            def fmt_percent(value: float, decimals: int = 1) -> str:
                """
                Format a value as a percentage.

                %family Formatting

                Parameters
                ----------
                value
                    The numeric value (0-1 scale).
                decimals
                    Number of decimal places.

                Returns
                -------
                str
                    Formatted percentage string.
                """
                return f"{value * 100:.{decimals}f}%"


            def helper() -> None:
                """
                A helper function with no family assignment.

                This should end up in a default/uncategorized section.

                Returns
                -------
                None
                """
                pass
        ''',
        "README.md": """\
            # gdtest-families

            Test package for ``%family`` directive-based API organization.
        """,
    },
    # ── Expected outcomes ─────────────────────────────────────────────
    "expected": {
        "detected_name": "gdtest-families",
        "detected_module": "gdtest_families",
        "detected_parser": "numpy",
        "export_names": [
            "Validate",
            "col_vals_gt",
            "col_vals_lt",
            "col_vals_between",
            "col_exists",
            "fmt_number",
            "fmt_percent",
            "helper",
        ],
        "num_exports": 8,
        "families": {
            "Validation": [
                "Validate",
                "col_vals_gt",
                "col_vals_lt",
                "col_vals_between",
                "col_exists",
            ],
            "Formatting": ["fmt_number", "fmt_percent"],
        },
        "unfamilied": ["helper"],
        "has_user_guide": False,
    },
}

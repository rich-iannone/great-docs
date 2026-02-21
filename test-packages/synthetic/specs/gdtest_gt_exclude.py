"""
gdtest_gt_exclude — Legacy __gt_exclude__ directive.

Dimensions: A1, B4, C4, D1, E6, F6, G1, H7
Focus: Uses __all__ for exports plus __gt_exclude__ to filter out
       specific items from documentation. Tests legacy exclusion parsing.
"""

SPEC = {
    "name": "gdtest_gt_exclude",
    "description": "__gt_exclude__ legacy exclusion directive",
    "dimensions": ["A1", "B4", "C4", "D1", "E6", "F6", "G1", "H7"],
    "pyproject_toml": {
        "project": {
            "name": "gdtest-gt-exclude",
            "version": "0.1.0",
            "description": "A synthetic test package testing __gt_exclude__",
        },
        "build-system": {
            "requires": ["setuptools"],
            "build-backend": "setuptools.build_meta",
        },
    },
    "files": {
        "gdtest_gt_exclude/__init__.py": '''\
            """A test package with __gt_exclude__ for legacy exclusion."""

            __version__ = "0.1.0"
            __all__ = ["public_func", "PublicClass", "internal_func", "helper"]
            __gt_exclude__ = ["internal_func", "helper"]


            class PublicClass:
                """
                A public class that should be documented.

                Parameters
                ----------
                value
                    The initial value.
                """

                def __init__(self, value: int = 0):
                    self.value = value

                def get(self) -> int:
                    """
                    Get the current value.

                    Returns
                    -------
                    int
                        The current value.
                    """
                    return self.value


            def public_func(x: int) -> int:
                """
                A public function that should be documented.

                Parameters
                ----------
                x
                    Input value.

                Returns
                -------
                int
                    Doubled value.
                """
                return x * 2


            def internal_func() -> None:
                """
                An internal function excluded via __gt_exclude__.

                This should NOT appear in documentation.
                """
                pass


            def helper() -> None:
                """
                A helper function excluded via __gt_exclude__.

                This should NOT appear in documentation.
                """
                pass
        ''',
        "README.md": """\
            # gdtest-gt-exclude

            A synthetic test package testing the ``__gt_exclude__`` directive.
        """,
    },
    "expected": {
        "detected_name": "gdtest-gt-exclude",
        "detected_module": "gdtest_gt_exclude",
        "detected_parser": "numpy",
        "export_names": ["public_func", "PublicClass"],
        "num_exports": 2,
        "gt_excluded": ["internal_func", "helper"],
        "has_user_guide": False,
    },
}

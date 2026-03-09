"""
gdtest_gradient_no_dismiss — Gradient banner with dismissable: false.

Dimensions: K39
Focus: gradient style combined with non-dismissable banner.
"""

SPEC = {
    "name": "gdtest_gradient_no_dismiss",
    "description": "Tests gradient banner with dismissable disabled",
    "dimensions": ["K39"],
    "pyproject_toml": {
        "project": {
            "name": "gdtest-gradient-no-dismiss",
            "version": "0.1.0",
            "description": "Test gradient with no dismiss",
        },
        "build-system": {
            "requires": ["setuptools"],
            "build-backend": "setuptools.build_meta",
        },
    },
    "config": {
        "announcement": {
            "content": "Permanent flame banner!",
            "style": "flame",
            "dismissable": False,
        },
    },
    "files": {
        "gdtest_gradient_no_dismiss/__init__.py": '''\
            """Package testing gradient with dismissable disabled."""

            __version__ = "0.1.0"
            __all__ = ["persist", "hold"]


            def persist(value: str) -> str:
                """
                Persist a value.

                Parameters
                ----------
                value
                    Value to persist.

                Returns
                -------
                str
                    Confirmation.
                """
                return f"Persisted: {value}"


            def hold(item: str) -> str:
                """
                Hold an item in place.

                Parameters
                ----------
                item
                    Item to hold.

                Returns
                -------
                str
                    Status message.
                """
                return f"Holding {item}"
        ''',
    },
}

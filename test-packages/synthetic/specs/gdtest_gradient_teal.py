"""
gdtest_gradient_teal — Announcement banner with teal gradient preset.

Dimensions: K35
Focus: style: teal applies animated gradient class to the banner.
"""

SPEC = {
    "name": "gdtest_gradient_teal",
    "description": "Tests announcement banner with teal gradient preset",
    "dimensions": ["K35"],
    "pyproject_toml": {
        "project": {
            "name": "gdtest-gradient-teal",
            "version": "0.1.0",
            "description": "Test teal gradient preset",
        },
        "build-system": {
            "requires": ["setuptools"],
            "build-backend": "setuptools.build_meta",
        },
    },
    "config": {
        "announcement": {
            "content": "Teal gradient test banner!",
            "style": "teal",
        },
    },
    "files": {
        "gdtest_gradient_teal/__init__.py": '''\
            """Package testing teal gradient preset."""

            __version__ = "0.1.0"
            __all__ = ["refresh", "calm"]


            def refresh(source: str) -> str:
                """
                Refresh from a source.

                Parameters
                ----------
                source
                    The refreshment source.

                Returns
                -------
                str
                    Status message.
                """
                return f"Refreshed from {source}"


            def calm() -> str:
                """
                Find calm.

                Returns
                -------
                str
                    Status message.
                """
                return "Calm achieved"
        ''',
    },
}

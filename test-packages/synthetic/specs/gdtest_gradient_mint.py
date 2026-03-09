"""
gdtest_gradient_mint — Announcement banner with mint gradient preset.

Dimensions: K35
Focus: style: mint applies animated gradient class to the banner.
"""

SPEC = {
    "name": "gdtest_gradient_mint",
    "description": "Tests announcement banner with mint gradient preset",
    "dimensions": ["K35"],
    "pyproject_toml": {
        "project": {
            "name": "gdtest-gradient-mint",
            "version": "0.1.0",
            "description": "Test mint gradient preset",
        },
        "build-system": {
            "requires": ["setuptools"],
            "build-backend": "setuptools.build_meta",
        },
    },
    "config": {
        "announcement": {
            "content": "Mint gradient test banner!",
            "style": "mint",
        },
    },
    "files": {
        "gdtest_gradient_mint/__init__.py": '''\
            """Package testing mint gradient preset."""

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

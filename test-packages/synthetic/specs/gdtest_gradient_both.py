"""
gdtest_gradient_both — Same gradient preset on both banner and navbar.

Dimensions: K37
Focus: style + navbar_style using the same preset applies to both elements.
"""

SPEC = {
    "name": "gdtest_gradient_both",
    "description": "Tests same gradient preset on banner and navbar",
    "dimensions": ["K37"],
    "pyproject_toml": {
        "project": {
            "name": "gdtest-gradient-both",
            "version": "0.1.0",
            "description": "Test matching gradient on banner and navbar",
        },
        "build-system": {
            "requires": ["setuptools"],
            "build-backend": "setuptools.build_meta",
        },
    },
    "config": {
        "announcement": {
            "content": "Unified aurora gradient!",
            "style": "aurora",
        },
        "navbar_style": "aurora",
    },
    "files": {
        "gdtest_gradient_both/__init__.py": '''\
            """Package testing unified gradient on banner and navbar."""

            __version__ = "0.1.0"
            __all__ = ["sync", "align"]


            def sync(source: str, target: str) -> str:
                """
                Synchronize source with target.

                Parameters
                ----------
                source
                    Source name.
                target
                    Target name.

                Returns
                -------
                str
                    Sync status.
                """
                return f"Synced {source} -> {target}"


            def align(items: list) -> str:
                """
                Align a list of items.

                Parameters
                ----------
                items
                    Items to align.

                Returns
                -------
                str
                    Alignment result.
                """
                return f"Aligned {len(items)} items"
        ''',
    },
}

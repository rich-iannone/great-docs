"""
gdtest_gradient_slate — Announcement banner with slate gradient preset.

Dimensions: K32
Focus: style: slate applies animated gradient class to the banner.
"""

SPEC = {
    "name": "gdtest_gradient_slate",
    "description": "Tests announcement banner with slate gradient preset",
    "dimensions": ["K32"],
    "pyproject_toml": {
        "project": {
            "name": "gdtest-gradient-slate",
            "version": "0.1.0",
            "description": "Test slate gradient preset",
        },
        "build-system": {
            "requires": ["setuptools"],
            "build-backend": "setuptools.build_meta",
        },
    },
    "config": {
        "announcement": {
            "content": "Slate gradient test banner!",
            "style": "slate",
        },
    },
    "files": {
        "gdtest_gradient_slate/__init__.py": '''\
            """Package testing slate gradient preset."""

            __version__ = "0.1.0"
            __all__ = ["carve", "polish"]


            def carve(shape: str) -> str:
                """
                Carve a shape from slate.

                Parameters
                ----------
                shape
                    Desired shape.

                Returns
                -------
                str
                    Result description.
                """
                return f"Carved {shape}"


            def polish(grit: int) -> str:
                """
                Polish the slate surface.

                Parameters
                ----------
                grit
                    Sandpaper grit level.

                Returns
                -------
                str
                    Result description.
                """
                return f"Polished with {grit} grit"
        ''',
    },
}

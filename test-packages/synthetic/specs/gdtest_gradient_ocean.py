"""
gdtest_gradient_ocean — Announcement banner with ocean gradient preset.

Dimensions: K28
Focus: style: ocean applies animated gradient class to the banner.
"""

SPEC = {
    "name": "gdtest_gradient_ocean",
    "description": "Tests announcement banner with ocean gradient preset",
    "dimensions": ["K28"],
    "pyproject_toml": {
        "project": {
            "name": "gdtest-gradient-ocean",
            "version": "0.1.0",
            "description": "Test ocean gradient preset",
        },
        "build-system": {
            "requires": ["setuptools"],
            "build-backend": "setuptools.build_meta",
        },
    },
    "config": {
        "announcement": {
            "content": "Ocean gradient test banner!",
            "style": "ocean",
        },
    },
    "files": {
        "gdtest_gradient_ocean/__init__.py": '''\
            """Package testing ocean gradient preset."""

            __version__ = "0.1.0"
            __all__ = ["dive", "surface"]


            def dive(depth: int) -> str:
                """
                Dive to a given depth.

                Parameters
                ----------
                depth
                    Target depth in meters.

                Returns
                -------
                str
                    Status message.
                """
                return f"Diving to {depth}m"


            def surface() -> str:
                """
                Return to the surface.

                Returns
                -------
                str
                    Status message.
                """
                return "Surfacing"
        ''',
    },
}

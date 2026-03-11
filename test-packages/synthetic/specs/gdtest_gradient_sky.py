"""
gdtest_gradient_sky — Announcement banner with sky gradient preset.

Dimensions: K28
Focus: style: sky applies animated gradient class to the banner.
"""

SPEC = {
    "name": "gdtest_gradient_sky",
    "description": "Tests announcement banner with sky gradient preset",
    "dimensions": ["K28"],
    "pyproject_toml": {
        "project": {
            "name": "gdtest-gradient-sky",
            "version": "0.1.0",
            "description": "Test sky gradient preset",
        },
        "build-system": {
            "requires": ["setuptools"],
            "build-backend": "setuptools.build_meta",
        },
    },
    "config": {
        "announcement": {
            "content": "Sky gradient test banner!",
            "style": "sky",
        },
    },
    "files": {
        "gdtest_gradient_sky/__init__.py": '''\
            """Package testing sky gradient preset."""

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

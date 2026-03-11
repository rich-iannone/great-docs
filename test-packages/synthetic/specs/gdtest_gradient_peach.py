"""
gdtest_gradient_peach — Announcement banner with peach gradient preset.

Dimensions: K29
Focus: style: peach applies animated gradient class to the banner.
"""

SPEC = {
    "name": "gdtest_gradient_peach",
    "description": "Tests announcement banner with peach gradient preset",
    "dimensions": ["K29"],
    "pyproject_toml": {
        "project": {
            "name": "gdtest-gradient-peach",
            "version": "0.1.0",
            "description": "Test peach gradient preset",
        },
        "build-system": {
            "requires": ["setuptools"],
            "build-backend": "setuptools.build_meta",
        },
    },
    "config": {
        "announcement": {
            "content": "Peach gradient test banner!",
            "style": "peach",
        },
    },
    "files": {
        "gdtest_gradient_peach/__init__.py": '''\
            """Package testing peach gradient preset."""

            __version__ = "0.1.0"
            __all__ = ["glow", "fade"]


            def glow(intensity: float) -> str:
                """
                Emit a warm glow.

                Parameters
                ----------
                intensity
                    Brightness level (0.0–1.0).

                Returns
                -------
                str
                    Status message.
                """
                return f"Glowing at {intensity}"


            def fade() -> str:
                """
                Fade to twilight.

                Returns
                -------
                str
                    Status message.
                """
                return "Fading"
        ''',
    },
}

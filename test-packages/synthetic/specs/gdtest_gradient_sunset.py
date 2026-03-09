"""
gdtest_gradient_sunset — Announcement banner with sunset gradient preset.

Dimensions: K29
Focus: style: sunset applies animated gradient class to the banner.
"""

SPEC = {
    "name": "gdtest_gradient_sunset",
    "description": "Tests announcement banner with sunset gradient preset",
    "dimensions": ["K29"],
    "pyproject_toml": {
        "project": {
            "name": "gdtest-gradient-sunset",
            "version": "0.1.0",
            "description": "Test sunset gradient preset",
        },
        "build-system": {
            "requires": ["setuptools"],
            "build-backend": "setuptools.build_meta",
        },
    },
    "config": {
        "announcement": {
            "content": "Sunset gradient test banner!",
            "style": "sunset",
        },
    },
    "files": {
        "gdtest_gradient_sunset/__init__.py": '''\
            """Package testing sunset gradient preset."""

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

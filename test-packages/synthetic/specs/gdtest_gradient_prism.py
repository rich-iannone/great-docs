"""
gdtest_gradient_prism — Announcement banner with prism gradient preset.

Dimensions: K30
Focus: style: prism applies animated gradient class to the banner.
"""

SPEC = {
    "name": "gdtest_gradient_prism",
    "description": "Tests announcement banner with prism gradient preset",
    "dimensions": ["K30"],
    "pyproject_toml": {
        "project": {
            "name": "gdtest-gradient-prism",
            "version": "0.1.0",
            "description": "Test prism gradient preset",
        },
        "build-system": {
            "requires": ["setuptools"],
            "build-backend": "setuptools.build_meta",
        },
    },
    "config": {
        "announcement": {
            "content": "Prism gradient test banner!",
            "style": "prism",
        },
    },
    "files": {
        "gdtest_gradient_prism/__init__.py": '''\
            """Package testing prism gradient preset."""

            __version__ = "0.1.0"
            __all__ = ["shimmer", "pulse"]


            def shimmer(color: str) -> str:
                """
                Create a shimmering effect.

                Parameters
                ----------
                color
                    Base color name.

                Returns
                -------
                str
                    Effect description.
                """
                return f"Shimmering {color}"


            def pulse(rate: float) -> str:
                """
                Pulse at a given rate.

                Parameters
                ----------
                rate
                    Pulses per second.

                Returns
                -------
                str
                    Effect description.
                """
                return f"Pulsing at {rate}Hz"
        ''',
    },
}

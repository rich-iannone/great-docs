"""
gdtest_gradient_aurora — Announcement banner with aurora gradient preset.

Dimensions: K30
Focus: style: aurora applies animated gradient class to the banner.
"""

SPEC = {
    "name": "gdtest_gradient_aurora",
    "description": "Tests announcement banner with aurora gradient preset",
    "dimensions": ["K30"],
    "pyproject_toml": {
        "project": {
            "name": "gdtest-gradient-aurora",
            "version": "0.1.0",
            "description": "Test aurora gradient preset",
        },
        "build-system": {
            "requires": ["setuptools"],
            "build-backend": "setuptools.build_meta",
        },
    },
    "config": {
        "announcement": {
            "content": "Aurora gradient test banner!",
            "style": "aurora",
        },
    },
    "files": {
        "gdtest_gradient_aurora/__init__.py": '''\
            """Package testing aurora gradient preset."""

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

"""
gdtest_gradient_dusk — Announcement banner with dusk gradient preset.

Dimensions: K34
Focus: style: dusk applies animated gradient class to the banner.
"""

SPEC = {
    "name": "gdtest_gradient_dusk",
    "description": "Tests announcement banner with dusk gradient preset",
    "dimensions": ["K34"],
    "pyproject_toml": {
        "project": {
            "name": "gdtest-gradient-dusk",
            "version": "0.1.0",
            "description": "Test dusk gradient preset",
        },
        "build-system": {
            "requires": ["setuptools"],
            "build-backend": "setuptools.build_meta",
        },
    },
    "config": {
        "announcement": {
            "content": "Dusk gradient test banner!",
            "style": "dusk",
        },
    },
    "files": {
        "gdtest_gradient_dusk/__init__.py": '''\
            """Package testing dusk gradient preset."""

            __version__ = "0.1.0"
            __all__ = ["dream", "wake"]


            def dream(topic: str) -> str:
                """
                Start a dream sequence.

                Parameters
                ----------
                topic
                    Dream subject.

                Returns
                -------
                str
                    Dream description.
                """
                return f"Dreaming of {topic}"


            def wake() -> str:
                """
                Wake from a dream.

                Returns
                -------
                str
                    Status message.
                """
                return "Awake"
        ''',
    },
}

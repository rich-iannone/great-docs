"""
gdtest_gradient_midnight — Announcement banner with midnight gradient preset.

Dimensions: K34
Focus: style: midnight applies animated gradient class to the banner.
"""

SPEC = {
    "name": "gdtest_gradient_midnight",
    "description": "Tests announcement banner with midnight gradient preset",
    "dimensions": ["K34"],
    "pyproject_toml": {
        "project": {
            "name": "gdtest-gradient-midnight",
            "version": "0.1.0",
            "description": "Test midnight gradient preset",
        },
        "build-system": {
            "requires": ["setuptools"],
            "build-backend": "setuptools.build_meta",
        },
    },
    "config": {
        "announcement": {
            "content": "Midnight gradient test banner!",
            "style": "midnight",
        },
    },
    "files": {
        "gdtest_gradient_midnight/__init__.py": '''\
            """Package testing midnight gradient preset."""

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

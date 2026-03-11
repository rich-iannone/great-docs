"""
gdtest_gradient_lilac — Announcement banner with lilac gradient preset.

Dimensions: K31
Focus: style: lilac applies animated gradient class to the banner.
"""

SPEC = {
    "name": "gdtest_gradient_lilac",
    "description": "Tests announcement banner with lilac gradient preset",
    "dimensions": ["K31"],
    "pyproject_toml": {
        "project": {
            "name": "gdtest-gradient-lilac",
            "version": "0.1.0",
            "description": "Test lilac gradient preset",
        },
        "build-system": {
            "requires": ["setuptools"],
            "build-backend": "setuptools.build_meta",
        },
    },
    "config": {
        "announcement": {
            "content": "Lilac gradient test banner!",
            "style": "lilac",
        },
    },
    "files": {
        "gdtest_gradient_lilac/__init__.py": '''\
            """Package testing lilac gradient preset."""

            __version__ = "0.1.0"
            __all__ = ["pick", "blend"]


            def pick(variety: str) -> str:
                """
                Pick a lilac variety.

                Parameters
                ----------
                variety
                    Name of the lilac.

                Returns
                -------
                str
                    Confirmation.
                """
                return f"Picked {variety}"


            def blend(berries: list) -> str:
                """
                Blend berries together.

                Parameters
                ----------
                berries
                    List of lilac names.

                Returns
                -------
                str
                    Result description.
                """
                return f"Blended {len(berries)} berries"
        ''',
    },
}

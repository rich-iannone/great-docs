"""
gdtest_gradient_berry — Announcement banner with berry gradient preset.

Dimensions: K31
Focus: style: berry applies animated gradient class to the banner.
"""

SPEC = {
    "name": "gdtest_gradient_berry",
    "description": "Tests announcement banner with berry gradient preset",
    "dimensions": ["K31"],
    "pyproject_toml": {
        "project": {
            "name": "gdtest-gradient-berry",
            "version": "0.1.0",
            "description": "Test berry gradient preset",
        },
        "build-system": {
            "requires": ["setuptools"],
            "build-backend": "setuptools.build_meta",
        },
    },
    "config": {
        "announcement": {
            "content": "Berry gradient test banner!",
            "style": "berry",
        },
    },
    "files": {
        "gdtest_gradient_berry/__init__.py": '''\
            """Package testing berry gradient preset."""

            __version__ = "0.1.0"
            __all__ = ["pick", "blend"]


            def pick(variety: str) -> str:
                """
                Pick a berry variety.

                Parameters
                ----------
                variety
                    Name of the berry.

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
                    List of berry names.

                Returns
                -------
                str
                    Result description.
                """
                return f"Blended {len(berries)} berries"
        ''',
    },
}

"""
gdtest_gradient_honey — Announcement banner with honey gradient preset.

Dimensions: K33
Focus: style: honey applies animated gradient class to the banner.
"""

SPEC = {
    "name": "gdtest_gradient_honey",
    "description": "Tests announcement banner with honey gradient preset",
    "dimensions": ["K33"],
    "pyproject_toml": {
        "project": {
            "name": "gdtest-gradient-honey",
            "version": "0.1.0",
            "description": "Test honey gradient preset",
        },
        "build-system": {
            "requires": ["setuptools"],
            "build-backend": "setuptools.build_meta",
        },
    },
    "config": {
        "announcement": {
            "content": "Honey gradient test banner!",
            "style": "honey",
        },
    },
    "files": {
        "gdtest_gradient_honey/__init__.py": '''\
            """Package testing honey gradient preset."""

            __version__ = "0.1.0"
            __all__ = ["ignite", "extinguish"]


            def ignite(fuel: str) -> str:
                """
                Ignite a fuel source.

                Parameters
                ----------
                fuel
                    Type of fuel.

                Returns
                -------
                str
                    Ignition status.
                """
                return f"Ignited {fuel}"


            def extinguish() -> str:
                """
                Extinguish the honey.

                Returns
                -------
                str
                    Status message.
                """
                return "Extinguished"
        ''',
    },
}

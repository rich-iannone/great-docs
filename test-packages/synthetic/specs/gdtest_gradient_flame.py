"""
gdtest_gradient_flame — Announcement banner with flame gradient preset.

Dimensions: K33
Focus: style: flame applies animated gradient class to the banner.
"""

SPEC = {
    "name": "gdtest_gradient_flame",
    "description": "Tests announcement banner with flame gradient preset",
    "dimensions": ["K33"],
    "pyproject_toml": {
        "project": {
            "name": "gdtest-gradient-flame",
            "version": "0.1.0",
            "description": "Test flame gradient preset",
        },
        "build-system": {
            "requires": ["setuptools"],
            "build-backend": "setuptools.build_meta",
        },
    },
    "config": {
        "announcement": {
            "content": "Flame gradient test banner!",
            "style": "flame",
        },
    },
    "files": {
        "gdtest_gradient_flame/__init__.py": '''\
            """Package testing flame gradient preset."""

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
                Extinguish the flame.

                Returns
                -------
                str
                    Status message.
                """
                return "Extinguished"
        ''',
    },
}

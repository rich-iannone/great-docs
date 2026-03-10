"""
gdtest_navbar_color_dark — Solid navbar color for dark mode only.

Dimensions: K45
Focus: navbar_color set as a dict with only a ``dark`` key.  The light-mode
navbar keeps its default styling while the dark-mode navbar gets a pale
mint background with APCA-chosen black text.
"""

SPEC = {
    "name": "gdtest_navbar_color_dark",
    "description": "Tests navbar_color applied only to dark mode",
    "dimensions": ["K45"],
    "pyproject_toml": {
        "project": {
            "name": "gdtest-navbar-color-dark",
            "version": "0.1.0",
            "description": "Test navbar_color in dark mode only",
        },
        "build-system": {
            "requires": ["setuptools"],
            "build-backend": "setuptools.build_meta",
        },
    },
    "config": {
        "navbar_color": {
            "dark": "#b2dfdb",
        },
        "display_name": "Navbar Color (Dark Only)",
    },
    "files": {
        "gdtest_navbar_color_dark/__init__.py": '''\
            """Navbar color: dark-mode only."""

            __version__ = "0.1.0"
            __all__ = ["tint", "lighten"]


            def tint(color: str) -> str:
                """
                Apply a tint to a color.

                Parameters
                ----------
                color
                    A CSS color string.

                Returns
                -------
                str
                    Tinted color value.
                """
                return f"Tinted {color}"


            def lighten(base: str, amount: float = 0.2) -> str:
                """
                Lighten a base color by a relative amount.

                Parameters
                ----------
                base
                    Base CSS color.
                amount
                    Fraction to lighten (0–1).

                Returns
                -------
                str
                    The lightened color.
                """
                return f"{base} lightened by {amount}"
        ''',
    },
}

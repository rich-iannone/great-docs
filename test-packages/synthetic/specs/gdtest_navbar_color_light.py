"""
gdtest_navbar_color_light — Solid navbar color for light mode only.

Dimensions: K44
Focus: navbar_color set as a dict with only a ``light`` key.  The dark-mode
navbar keeps its default styling while the light-mode navbar gets a deep
blue-gray background with APCA-chosen white text.
"""

SPEC = {
    "name": "gdtest_navbar_color_light",
    "description": "Tests navbar_color applied only to light mode",
    "dimensions": ["K44"],
    "pyproject_toml": {
        "project": {
            "name": "gdtest-navbar-color-light",
            "version": "0.1.0",
            "description": "Test navbar_color in light mode only",
        },
        "build-system": {
            "requires": ["setuptools"],
            "build-backend": "setuptools.build_meta",
        },
    },
    "config": {
        "navbar_color": {
            "light": "#1b2838",
        },
        "display_name": "Navbar Color (Light Only)",
    },
    "files": {
        "gdtest_navbar_color_light/__init__.py": '''\
            """Navbar color: light-mode only."""

            __version__ = "0.1.0"
            __all__ = ["paint", "shade"]


            def paint(color: str) -> str:
                """
                Apply a paint color.

                Parameters
                ----------
                color
                    A CSS color string.

                Returns
                -------
                str
                    Confirmation message.
                """
                return f"Painted {color}"


            def shade(base: str, amount: float = 0.2) -> str:
                """
                Darken a base color by a relative amount.

                Parameters
                ----------
                base
                    Base CSS color.
                amount
                    Fraction to darken (0–1).

                Returns
                -------
                str
                    The shaded color.
                """
                return f"{base} darkened by {amount}"
        ''',
    },
}

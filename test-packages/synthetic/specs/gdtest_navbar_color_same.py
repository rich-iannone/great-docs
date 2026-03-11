"""
gdtest_navbar_color_same — Same solid navbar color for both light and dark modes.

Dimensions: K46
Focus: navbar_color set as a plain string (not a dict), so the same color is
used in both light and dark modes.  Uses ``steelblue`` (#4682B4), a mid-tone
blue that APCA selects white text for.
"""

SPEC = {
    "name": "gdtest_navbar_color_same",
    "description": "Tests navbar_color as a single string for both modes",
    "dimensions": ["K46"],
    "pyproject_toml": {
        "project": {
            "name": "gdtest-navbar-color-same",
            "version": "0.1.0",
            "description": "Test navbar_color with same color both modes",
        },
        "build-system": {
            "requires": ["setuptools"],
            "build-backend": "setuptools.build_meta",
        },
    },
    "config": {
        "navbar_color": "steelblue",
        "display_name": "Navbar Color (Same Both Modes)",
    },
    "files": {
        "gdtest_navbar_color_same/__init__.py": '''\
            """Navbar color: same for both modes."""

            __version__ = "0.1.0"
            __all__ = ["blend", "mix"]


            def blend(color_a: str, color_b: str) -> str:
                """
                Blend two colors together.

                Parameters
                ----------
                color_a
                    First CSS color.
                color_b
                    Second CSS color.

                Returns
                -------
                str
                    The blended result.
                """
                return f"Blend({color_a}, {color_b})"


            def mix(colors: list[str], weights: list[float] | None = None) -> str:
                """
                Mix multiple colors with optional weights.

                Parameters
                ----------
                colors
                    List of CSS color strings.
                weights
                    Optional weights for each color.

                Returns
                -------
                str
                    The mixed color value.
                """
                return f"Mix({', '.join(colors)})"
        ''',
    },
}

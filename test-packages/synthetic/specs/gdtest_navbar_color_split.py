"""
gdtest_navbar_color_split — Different navbar colors per mode (warm / cool).

Dimensions: K47
Focus: navbar_color dict with distinct ``light`` and ``dark`` values that
exercise different text-color choices.  Light mode uses a dark warm brown
(``#3e2723``, gets white text) while dark mode uses a pale sky blue
(``#bbdefb``, gets black text).
"""

SPEC = {
    "name": "gdtest_navbar_color_split",
    "description": "Tests navbar_color with contrasting light/dark choices",
    "dimensions": ["K47"],
    "pyproject_toml": {
        "project": {
            "name": "gdtest-navbar-color-split",
            "version": "0.1.0",
            "description": "Test navbar_color with different colors per mode",
        },
        "build-system": {
            "requires": ["setuptools"],
            "build-backend": "setuptools.build_meta",
        },
    },
    "config": {
        "navbar_color": {
            "light": "#3e2723",
            "dark": "#bbdefb",
        },
        "display_name": "Navbar Color (Split Warm/Cool)",
    },
    "files": {
        "gdtest_navbar_color_split/__init__.py": '''\
            """Navbar color: contrasting warm/cool per mode."""

            __version__ = "0.1.0"
            __all__ = ["warm", "cool"]


            def warm(temperature: float) -> str:
                """
                Create a warm color value from a temperature.

                Parameters
                ----------
                temperature
                    Color temperature in Kelvin (2000–4500).

                Returns
                -------
                str
                    A warm hex color.
                """
                return f"Warm({temperature}K)"


            def cool(temperature: float) -> str:
                """
                Create a cool color value from a temperature.

                Parameters
                ----------
                temperature
                    Color temperature in Kelvin (5500–10000).

                Returns
                -------
                str
                    A cool hex color.
                """
                return f"Cool({temperature}K)"
        ''',
    },
}

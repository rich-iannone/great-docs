"""
gdtest_hatch_families — Hatch build system + %family directives.

Dimensions: A5, B1, C1, D1, E1, F6, G1, H7
Focus: Module discovered via Hatch config, then grouped by %family
       directives. Tests both features together.
"""

SPEC = {
    "name": "gdtest_hatch_families",
    "description": "Hatch build system with %family directives",
    "dimensions": ["A5", "B1", "C1", "D1", "E1", "F6", "G1", "H7"],
    "pyproject_toml": {
        "project": {
            "name": "gdtest-hatch-families",
            "version": "0.1.0",
            "description": "Test Hatch build with family directives",
        },
        "build-system": {
            "requires": ["hatchling"],
            "build-backend": "hatchling.build",
        },
        "tool": {
            "hatch": {
                "build": {
                    "targets": {
                        "wheel": {
                            "packages": ["gdtest_hatch_fam"],
                        },
                    },
                },
            },
        },
    },
    "files": {
        "gdtest_hatch_fam/__init__.py": '''\
            """Package using Hatch with %family directives."""

            __version__ = "0.1.0"
            __all__ = ["load", "save", "render", "show"]


            def load(path: str) -> dict:
                """
                Load data from a file.

                %family Data

                Parameters
                ----------
                path
                    File path.

                Returns
                -------
                dict
                    Loaded data.
                """
                return {}


            def save(data: dict, path: str) -> None:
                """
                Save data to a file.

                %family Data

                Parameters
                ----------
                data
                    Data to save.
                path
                    File path.
                """
                pass


            def render(data: dict) -> str:
                """
                Render data as a string.

                %family Display

                Parameters
                ----------
                data
                    Data to render.

                Returns
                -------
                str
                    Rendered output.
                """
                return str(data)


            def show(data: dict) -> None:
                """
                Display data to the console.

                %family Display

                Parameters
                ----------
                data
                    Data to display.
                """
                print(data)
        ''',
        "README.md": """\
            # gdtest-hatch-families

            Tests Hatch build system with %family directive grouping.
        """,
    },
    "expected": {
        "detected_name": "gdtest-hatch-families",
        "detected_module": "gdtest_hatch_fam",
        "detected_parser": "numpy",
        "export_names": ["load", "save", "render", "show"],
        "num_exports": 4,
        "section_titles": ["Functions"],
        "has_user_guide": False,
    },
}

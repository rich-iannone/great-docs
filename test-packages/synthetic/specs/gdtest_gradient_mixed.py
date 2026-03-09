"""
gdtest_gradient_mixed — Different gradient presets on banner vs navbar.

Dimensions: K38
Focus: banner uses lilac preset, navbar uses dusk — they differ.
"""

SPEC = {
    "name": "gdtest_gradient_mixed",
    "description": "Tests different gradient presets on banner and navbar",
    "dimensions": ["K38"],
    "pyproject_toml": {
        "project": {
            "name": "gdtest-gradient-mixed",
            "version": "0.1.0",
            "description": "Test mismatched gradient presets",
        },
        "build-system": {
            "requires": ["setuptools"],
            "build-backend": "setuptools.build_meta",
        },
    },
    "config": {
        "announcement": {
            "content": "Lilac banner, dusk navbar!",
            "style": "lilac",
        },
        "navbar_style": "dusk",
    },
    "files": {
        "gdtest_gradient_mixed/__init__.py": '''\
            """Package testing mixed gradient presets."""

            __version__ = "0.1.0"
            __all__ = ["mix", "separate"]


            def mix(a: str, b: str) -> str:
                """
                Mix two elements.

                Parameters
                ----------
                a
                    First element.
                b
                    Second element.

                Returns
                -------
                str
                    Mixture result.
                """
                return f"Mixed {a} + {b}"


            def separate(compound: str) -> list:
                """
                Separate a compound into parts.

                Parameters
                ----------
                compound
                    Compound to separate.

                Returns
                -------
                list
                    Component parts.
                """
                return compound.split("+")
        ''',
    },
}

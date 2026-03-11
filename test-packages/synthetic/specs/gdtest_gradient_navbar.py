"""
gdtest_gradient_navbar — Navbar-only gradient style (no banner gradient).

Dimensions: K36
Focus: navbar_style applies gradient to the navbar without banner style.
"""

SPEC = {
    "name": "gdtest_gradient_navbar",
    "description": "Tests navbar gradient style without banner gradient",
    "dimensions": ["K36"],
    "pyproject_toml": {
        "project": {
            "name": "gdtest-gradient-navbar",
            "version": "0.1.0",
            "description": "Test navbar gradient style only",
        },
        "build-system": {
            "requires": ["setuptools"],
            "build-backend": "setuptools.build_meta",
        },
    },
    "config": {
        "announcement": {
            "content": "Plain banner, gradient navbar!",
            "type": "info",
        },
        "navbar_style": "peach",
    },
    "files": {
        "gdtest_gradient_navbar/__init__.py": '''\
            """Package testing navbar-only gradient style."""

            __version__ = "0.1.0"
            __all__ = ["navigate", "browse"]


            def navigate(url: str) -> str:
                """
                Navigate to a URL.

                Parameters
                ----------
                url
                    Target URL.

                Returns
                -------
                str
                    Navigation status.
                """
                return f"Navigating to {url}"


            def browse(query: str) -> str:
                """
                Browse for a query.

                Parameters
                ----------
                query
                    Search query.

                Returns
                -------
                str
                    Search results summary.
                """
                return f"Browsing: {query}"
        ''',
    },
}

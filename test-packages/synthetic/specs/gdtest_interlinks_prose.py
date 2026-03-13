"""
gdtest_interlinks_prose — interlink references in docstring prose.

Dimensions: A1, D1, E3, L26
Focus: Tests the ``[](`~pkg.Name`)`` interlinks syntax used directly in
       free-form docstring text.  The post-render resolver should convert
       these into proper hyperlinks to the corresponding reference pages.
"""

SPEC = {
    "name": "gdtest_interlinks_prose",
    "description": (
        "Interlinks syntax in docstring prose. "
        "Tests that [](`~Name`) references inside description text "
        "are resolved to proper hyperlinks by the post-render step."
    ),
    "dimensions": ["A1", "D1", "E3", "L26"],
    "pyproject_toml": {
        "project": {
            "name": "gdtest-interlinks-prose",
            "version": "0.1.0",
            "description": "Test interlinks in docstring prose",
        },
        "build-system": {
            "requires": ["setuptools"],
            "build-backend": "setuptools.build_meta",
        },
    },
    "files": {
        "gdtest_interlinks_prose/__init__.py": '''\
            """Package demonstrating interlinks in docstring prose."""

            __version__ = "0.1.0"
            __all__ = ["BaseStore", "DuckDBStore", "ChromaDBStore", "query"]


            class BaseStore:
                """Base class for all stores.

                Available implementations:

                - [](`~gdtest_interlinks_prose.DuckDBStore`): local storage with
                  embedded search.
                - [](`~gdtest_interlinks_prose.ChromaDBStore`): vector storage
                  using ChromaDB.

                Parameters
                ----------
                name
                    The name of the store.
                """

                def __init__(self, name: str) -> None:
                    self.name = name


            class DuckDBStore(BaseStore):
                """Local storage backed by DuckDB.

                Inherits from [](`~gdtest_interlinks_prose.BaseStore`).
                Use [](`~gdtest_interlinks_prose.query`) to search the store
                after loading data.

                Parameters
                ----------
                name
                    The name of the store.
                path
                    Path to the DuckDB database file.
                """

                def __init__(self, name: str, path: str = ":memory:") -> None:
                    super().__init__(name)
                    self.path = path


            class ChromaDBStore(BaseStore):
                """Vector storage using ChromaDB.

                Inherits from [](`~gdtest_interlinks_prose.BaseStore`).
                See [](`~gdtest_interlinks_prose.DuckDBStore`) for a
                simpler alternative.

                Parameters
                ----------
                name
                    The name of the store.
                collection
                    The ChromaDB collection name.
                """

                def __init__(self, name: str, collection: str = "default") -> None:
                    super().__init__(name)
                    self.collection = collection


            def query(store: BaseStore, text: str) -> list:
                """Search a store for matching documents.

                Works with any [](`~gdtest_interlinks_prose.BaseStore`)
                implementation, including
                [](`~gdtest_interlinks_prose.DuckDBStore`) and
                [](`~gdtest_interlinks_prose.ChromaDBStore`).

                Parameters
                ----------
                store
                    The store to search. Must be an instance of
                    [](`~gdtest_interlinks_prose.BaseStore`).
                text
                    The search query string.

                Returns
                -------
                list
                    Matching documents.
                """
                return []
        ''',
        "README.md": """\
            # gdtest-interlinks-prose

            A synthetic test package testing interlinks in docstring prose.
        """,
    },
    "expected": {
        "detected_name": "gdtest-interlinks-prose",
        "detected_module": "gdtest_interlinks_prose",
        "detected_parser": "numpy",
        "export_names": ["BaseStore", "ChromaDBStore", "DuckDBStore", "query"],
        "num_exports": 4,
        "section_titles": ["Classes", "Functions"],
        "has_user_guide": False,
        # Names referenced via interlinks in prose — these should become
        # clickable <a> links in the rendered HTML after post-render resolves
        # the ``[](`~pkg.Name`)`` syntax.
        "interlinks_in_prose": {
            "BaseStore": ["DuckDBStore", "ChromaDBStore"],
            "DuckDBStore": ["BaseStore", "query"],
            "ChromaDBStore": ["BaseStore", "DuckDBStore"],
            "query": ["BaseStore", "DuckDBStore", "ChromaDBStore"],
        },
    },
}

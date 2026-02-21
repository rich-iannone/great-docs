"""
gdtest_sphinx_families — Sphinx docstrings + %family directives.

Dimensions: A1, B1, C1, D3, E1, F6, G1, H7
Focus: Sphinx-style :param:/:returns: field lists combined with
       %family grouping to verify both render together.
"""

SPEC = {
    "name": "gdtest_sphinx_families",
    "description": "Sphinx docstrings with %family directives",
    "dimensions": ["A1", "B1", "C1", "D3", "E1", "F6", "G1", "H7"],
    "pyproject_toml": {
        "project": {
            "name": "gdtest-sphinx-families",
            "version": "0.1.0",
            "description": "Test Sphinx docstrings with family grouping",
        },
        "build-system": {
            "requires": ["setuptools"],
            "build-backend": "setuptools.build_meta",
        },
    },
    "files": {
        "gdtest_sphinx_families/__init__.py": '''\
            """Package with Sphinx docstrings and %family directives."""

            __version__ = "0.1.0"
            __all__ = ["connect", "disconnect", "status", "send", "receive"]


            def connect(host: str, port: int = 8080) -> bool:
                """
                Connect to a remote host.

                %family Network

                :param host: The hostname to connect to.
                :param port: The port number.
                :returns: True if connection was successful.
                :rtype: bool
                """
                return True


            def disconnect() -> None:
                """
                Disconnect from the current host.

                %family Network
                """
                pass


            def status() -> str:
                """
                Get the current connection status.

                %family Network

                :returns: Status string (connected, disconnected, etc.).
                :rtype: str
                """
                return "disconnected"


            def send(data: bytes) -> int:
                """
                Send data over the connection.

                %family Data

                :param data: The bytes to send.
                :returns: Number of bytes sent.
                :rtype: int
                """
                return len(data)


            def receive(max_bytes: int = 4096) -> bytes:
                """
                Receive data from the connection.

                %family Data

                :param max_bytes: Maximum number of bytes to receive.
                :returns: The received data.
                :rtype: bytes
                """
                return b""
        ''',
        "README.md": """\
            # gdtest-sphinx-families

            Tests Sphinx docstrings combined with %family directives.
        """,
    },
    "expected": {
        "detected_name": "gdtest-sphinx-families",
        "detected_module": "gdtest_sphinx_families",
        "detected_parser": "sphinx",
        "export_names": ["connect", "disconnect", "status", "send", "receive"],
        "num_exports": 5,
        "section_titles": ["Functions"],
        "has_user_guide": False,
    },
}

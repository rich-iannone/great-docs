try:
    from importlib.metadata import PackageNotFoundError, version
except ImportError:  # pragma: no cover
    from importlib_metadata import PackageNotFoundError, version  # type: ignore[import-not-found]

try:  # pragma: no cover
    __version__ = version("great-docs")
except PackageNotFoundError:  # pragma: no cover
    __version__ = "0.0.0"

from .cli import main
from .core import GreatDocs
from .directives import DocDirectives, extract_directives, has_directives, strip_directives

__all__ = [
    "GreatDocs",
    "main",
    "DocDirectives",
    "extract_directives",
    "strip_directives",
    "has_directives",
]

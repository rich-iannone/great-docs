try:
    from importlib.metadata import PackageNotFoundError, version
except ImportError:  # pragma: no cover
    from importlib_metadata import PackageNotFoundError, version  # type: ignore[import-not-found]

try:  # pragma: no cover
    __version__ = version("great-docs")
except PackageNotFoundError:  # pragma: no cover
    __version__ = "0.0.0"

from .cli import main
from .config import Config, create_default_config, load_config
from .core import GreatDocs

__all__ = [
    "Config",
    "GreatDocs",
    "create_default_config",
    "load_config",
    "main",
]

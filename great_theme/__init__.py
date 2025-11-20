try:
    from importlib.metadata import PackageNotFoundError, version
except ImportError:  # pragma: no cover
    from importlib_metadata import PackageNotFoundError, version  # type: ignore[import-not-found]

try:  # pragma: no cover
    __version__ = version("great-theme")
except PackageNotFoundError:  # pragma: no cover
    __version__ = "0.0.0"

from .cli import main
from .core import GreatTheme

__all__ = ["GreatTheme", "main"]

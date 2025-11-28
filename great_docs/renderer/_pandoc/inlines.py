from __future__ import annotations

from dataclasses import dataclass

from quartodoc.pandoc.inlines import Inline, Link


@dataclass
class InterLink(Link):
    """
    Link with target enclosed in colons

    These targets of these links are interlink references
    that are finally resolved by the interlinks filter.
    """

    def __post_init__(self):
        self.target = f"`{self.target}`"


class shortcode(Inline):
    """
    Create quarto shortcode

    Parameters
    ----------
    str :
        Name of the shortcode
    *args :
        Arguments to the shortcode
    **kwargs :
        Named arguments for the shortcode

    References
    ----------
    https://quarto.org/docs/extensions/shortcodes.html
    """

    def __init__(self, name: str, *args: str, **kwargs: str):
        self.name = name
        self.args = args
        self.kwargs = kwargs

    def __str__(self):
        _args = " ".join(self.args)
        _kwargs = " ".join(f"{k}={v}" for k, v in self.kwargs.items())
        content = f"{self.name} {_args} {_kwargs}".strip()
        return f"{{{{< {content} >}}}}"

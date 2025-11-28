from __future__ import annotations

from typing import TYPE_CHECKING, cast

from quartodoc.pandoc.blocks import (
    Blocks,
)

from .base import RenderBase

if TYPE_CHECKING:
    from quartodoc.layout import Layout
    from quartodoc.pandoc.blocks import BlockContent


class __RenderLayout(RenderBase):
    """
    Render a Layout object (layout.Layout)

    This is the object that holds the information about the
    reference page.
    """

    def __post_init__(self):
        self.layout = cast("Layout", self.layout_obj)
        """The layout of the reference page"""

        self.sections = self.layout.sections
        """Top level sections of the quarto config"""

        self.package = self.layout.package
        """The package being documented """

        self.options = self.layout.options

    def render_title(self) -> BlockContent:
        """
        The title page
        """
        # The header currently being rendered in quartodoc
        # should be rendered here.
        # We need to know title of the page. It is not passed
        # to the renderer.

    def render_body(self) -> BlockContent:
        from . import get_render_type

        render_objs = [
            get_render_type(s)(s, self.renderer, self.level)
            for s in self.sections
        ]
        return Blocks(render_objs)


class RenderLayout(__RenderLayout):
    """
    Extend Rendering of a layout.Layout object
    """

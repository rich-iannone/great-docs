from __future__ import annotations

from dataclasses import dataclass
from functools import cached_property
from typing import TYPE_CHECKING

import griffe as gf
from quartodoc.pandoc.blocks import (
    Block,
    BlockContent,
    Blocks,
)

from .extending import extend_base_class

if TYPE_CHECKING:
    from collections.abc import Sequence

    from quartodoc import layout

    from .. import QRenderer
    from ..typing import SummaryItem


@dataclass
class __RenderBase(Block):
    """
    Render an object
    """

    layout_obj: (
        layout.DocClass
        | layout.DocFunction
        | layout.DocAttribute
        | layout.DocModule
        | layout.Page
        | layout.Section
        | layout.Link
        | layout.Layout
    )
    """Layout object to be documented"""

    renderer: QRenderer
    """Renderer that holds the configured values"""

    level: int = 1
    """The depth of the object in the documentation"""

    show_title: bool = True
    """Whether to show the title of the object"""

    show_signature: bool = True
    """
    Whether to show the signature

    This only applies to objects that have signatures
    """

    show_description: bool = True
    """
    Whether to show the description of the object

    This only applies to objects that have descriptions that are not
    considered part of the body documentation body.

    This attribute is not well defined and it may change in the future.
    """

    show_body: bool = True
    """Whether to show the documentation body of the object"""

    def __post_init__(self):
        """
        Makes it possible for sub-classes to extend the method
        """

    def __str__(self):
        """
        The documentation as quarto markdown
        """
        return str(
            Blocks(
                [
                    self.title if self.show_title else None,
                    self.signature if self.show_signature else None,
                    self.description if self.show_description else None,
                    self.body if self.show_body else None,
                ]
            )
        )

    @cached_property
    def title(self) -> BlockContent:
        """
        The title/header of a docstring, including any anchors

        Do not override this property.
        """
        return self.render_title()

    @cached_property
    def signature(self) -> BlockContent:
        """
        The signature of the object (if any)

        Do not override this property.
        """
        return self.render_signature()

    @cached_property
    def description(self) -> BlockContent:
        """
        The description that the documented object

        Do not override this property.
        """
        return self.render_description()

    @cached_property
    def body(self) -> BlockContent:
        """
        The body that the documented object

        Do not override this property.
        """
        return self.render_body()

    @cached_property
    def summary(self) -> Sequence[SummaryItem]:
        """
        The summary of the documented object

        Do not override this property.
        """
        return self.render_summary()

    def _describe_object(self, obj: gf.Object | gf.Alias) -> str:
        """
        Return oneline description of the griffe object
        """
        # oneline description of the object being documented
        # This is the first line of the docstring
        parts = obj.docstring.parsed if obj.docstring else []
        section = parts[0] if parts else None
        return (
            section.value.split("\n")[0]
            if isinstance(section, gf.DocstringSectionText)
            else ""
        )

    def render_title(self) -> BlockContent:
        """
        Render the header of a docstring, including any anchors
        """

    def render_signature(self) -> BlockContent:
        """
        Render the signature of the object being documented
        """

    def render_description(self) -> BlockContent:
        """
        Render the description of the documentation page
        """

    def render_body(self) -> BlockContent:
        """
        Render the body of the object being documented
        """

    @property
    def summary_name(self) -> str:
        """
        The name of object as it will appear in the summary table
        """
        return ""

    def render_summary(self) -> Sequence[SummaryItem]:
        """
        Return a line(s) item that summarises the object
        """
        return []


class RenderBase(__RenderBase):
    """
    Extend the base render class

    This class is meant for internal use. Users should not have
    to extend it.
    """

    def __init_subclass__(cls) -> None:
        super().__init_subclass__()

        # We want users to extend the rendering by subclassing a Render*
        # class and overriding methods and/or attributes as necessary.
        #
        # This hook customises how user-defined Render subclasses behave.
        #
        # The package defines a set of empty base classes—extension points,
        # which contain no methods or attributes by default. Users are
        # encouraged to subclass a provided Render class and override these
        # extension points with their own methods and attributes.
        #
        # Internally, we also subclass these empty base classes. This ensures
        # that any user-defined overrides "fill in" the base and are used
        # throughout the package.
        #
        # The "filling in" should only happen when extending the Render*
        # classes outside the package.
        if cls.__module__[:10] != "qrenderer.":
            extend_base_class(cls)

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from quartodoc.pandoc.blocks import Div
from quartodoc.pandoc.components import Attr
from quartodoc.pandoc.inlines import Code

from .._format import pretty_code, render_attribute_declaration
from .doc import RenderDoc

if TYPE_CHECKING:
    import griffe as gf
    from quartodoc import layout
    from quartodoc.pandoc.blocks import BlockContent


@dataclass
class __RenderDocAttribute(RenderDoc):
    """
    Render documentation for an attribute (layout.DocAttribute)
    """

    show_signature_annotation: bool = True

    def __post_init__(self):
        super().__post_init__()
        # We narrow the type with a TypeAlias since we do not expect
        # any subclasses to have narrower types
        self.doc: layout.DocAttribute = self.doc
        self.obj: gf.Attribute = self.obj

    def render_signature(self) -> BlockContent:
        if self.kind in ("type", "typevar"):
            return self.render_type_signature()

        name = self.signature_name if self.show_signature_name else ""
        annotation = (
            pretty_code(str(self.render_annotation()))
            if self.show_signature_annotation
            else ""
        )
        declaration = str(
            self.render_variable_definition(name, annotation, self.obj.value)
        )
        return Div(
            Code(declaration).html,
            Attr(classes=["doc-signature", f"doc-{self.kind}"]),
        )

    def render_type_signature(self) -> BlockContent:
        """
        The signature of a TypeAlias
        """
        stmt = render_attribute_declaration(self.obj)
        i, j = stmt.find(":"), stmt.find("=")

        if self.show_signature_name:
            if not self.show_signature_annotation and i < j:
                stmt = f"{stmt[:i]}{stmt[j:].strip()}"
        else:
            start = (self.show_signature_annotation and i) or j
            value = stmt[start + 1].strip()

        value = stmt[stmt.find("=") + 1 :].strip()
        return Div(
            Code(pretty_code(value)).html,
            Attr(classes=["doc-signature", f"doc-{self.kind}"]),
        )


class RenderDocAttribute(__RenderDocAttribute):
    """
    Extend Rendering of a layout.DocAttribute object
    """

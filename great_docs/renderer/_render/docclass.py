from __future__ import annotations

from functools import cached_property
from typing import TYPE_CHECKING

from quartodoc.pandoc.blocks import (
    Blocks,
    DefinitionItem,
    DefinitionList,
    Div,
    Header,
)
from quartodoc.pandoc.components import Attr
from quartodoc.pandoc.inlines import Code

from .._format import (
    pretty_code,
    render_dataclass_init_parameter,
    render_dataclass_parameter,
)
from .doc import RenderDoc
from .mixin_call import RenderDocCallMixin
from .mixin_members import RenderDocMembersMixin

if TYPE_CHECKING:
    import griffe as gf
    from quartodoc import layout
    from quartodoc.pandoc.blocks import Block


class __RenderDocClass(RenderDocMembersMixin, RenderDocCallMixin, RenderDoc):
    """
    Render documentation for a class (layout.DocClass)
    """

    def __post_init__(self):
        super().__post_init__()
        # We narrow the type with a TypeAlias since we do not expect
        # any subclasses to have narrower types
        self.doc: layout.DocClass = self.doc
        self.obj: gf.Class = self.obj

    @cached_property
    def is_dataclass(self):
        """
        Return True if the class object is a dataclass
        """
        return "dataclass" in self.obj.labels

    @cached_property
    def attributes(self) -> list[layout.DocAttribute]:
        """
        Override to exclude dataclass parameters
        """
        attributes = super().attributes
        if self.is_dataclass:
            params = {p.name for p in self.parameters}
            attributes = [a for a in attributes if a.name not in params]
        return attributes

    @cached_property
    def _sections(self):
        sections, section_kinds = super()._sections

        # We only want to extend the sections for dataclasses
        # that do not have a parameters section
        if (
            not self.is_dataclass
            or "parameters" in set(section_kinds)
            or not len(self.parameters)
        ):
            return sections, section_kinds

        # Create Parameters
        idx = 1 if section_kinds and section_kinds[0] == "text" else 0

        if section := self._init_parameters_section:
            sections.insert(idx, section)
            section_kinds.insert(idx, "init parameters")
            idx += 1

        if section := self._parameter_attributes_section:
            sections.insert(idx, section)
            section_kinds.insert(idx, "parameter attributes")

        return sections, section_kinds

    @cached_property
    def _parameter_attributes_section(self) -> Block | None:
        """
        Create a "Parameter Attributes" section
        """
        items: list[DefinitionItem] = []
        for p in self.parameters:
            if p.name not in self.obj.attributes or p.annotation is None:
                continue
            desc = (p.docstring and p.docstring.value) or ""
            a = self.obj.attributes[p.name]
            stmt = render_dataclass_parameter(p, a)
            items.append((Code(pretty_code(stmt)).html, desc))

        if not items:
            return

        header = Header(
            self.level + 1,
            "Parameter Attributes",
            Attr(classes=["doc-parameter-attributes"]),
        )

        body = Div(
            DefinitionList(items),
            Attr(classes=["doc-definition-items"]),
        )
        return Blocks([header, body])

    @cached_property
    def _init_parameters_section(self) -> Block | None:
        """
        Create an "Init Parameters" section
        """
        items: list[DefinitionItem] = []
        for p in self.parameters:
            if p.name in self.obj.attributes:
                continue
            desc = (p.docstring and p.docstring.value) or ""
            stmt = render_dataclass_init_parameter(p)
            items.append((Code(pretty_code(stmt)).html, desc))

        if not items:
            return

        header = Header(
            self.level + 1,
            "Init Parameters",
            Attr(classes=["doc-init-parameters"]),
        )

        body = Div(
            DefinitionList(items),
            Attr(classes=["doc-definition-items"]),
        )
        return Blocks([header, body])


class RenderDocClass(__RenderDocClass):
    """
    Extend Rendering of a layout.DocClass object
    """

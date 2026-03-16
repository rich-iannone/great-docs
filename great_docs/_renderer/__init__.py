"""
Compatibility shim — all code now lives in great_docs._qrenderer.

This module re-exports symbols so that existing ``from great_docs._renderer …``
imports continue to work.  New code should import from ``great_docs._qrenderer``.
"""

from great_docs._qrenderer import layout  # noqa: F401 — re-export module
from great_docs._qrenderer._ast import preview
from great_docs._qrenderer._md_renderer import MdRenderer, Renderer
from great_docs._qrenderer.blueprint import blueprint, strip_package_name
from great_docs._qrenderer.collect import collect
from great_docs._qrenderer.introspection import Builder, get_function, get_object
from great_docs._qrenderer.inventory import convert_inventory, create_inventory
from great_docs._qrenderer.layout import Auto, Layout

__all__ = [
    "get_object",
    "get_function",
    "Builder",
    "blueprint",
    "strip_package_name",
    "collect",
    "MdRenderer",
    "Renderer",
    "create_inventory",
    "convert_inventory",
    "preview",
    "Auto",
    "Layout",
]

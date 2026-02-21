"""
Master catalog of all synthetic test packages.

Provides the registry of package names, their specs, and dimension metadata.
Specs are lazily imported from the ``specs`` sub-package so that adding a new
package is as simple as dropping a new file into ``specs/``.
"""

from __future__ import annotations

import importlib
from typing import Any

# ── Ordered list of all package names ─────────────────────────────────────────
# The canonical ordering follows the numbering in SYNTHETIC_TEST_PLAN.md.

ALL_PACKAGES: list[str] = [
    # 01–05: Docstring format variants
    "gdtest_minimal",  # 01
    "gdtest_google",  # 02
    "gdtest_sphinx",  # 03
    "gdtest_nodocs",  # 04
    "gdtest_mixed_docs",  # 05
    # 06–13: Package layout variants
    "gdtest_src_layout",  # 06
    "gdtest_python_layout",  # 07
    "gdtest_lib_layout",  # 08
    "gdtest_hatch",  # 09
    "gdtest_setuptools_find",  # 10
    "gdtest_setup_cfg",  # 11
    "gdtest_setup_py",  # 12
    "gdtest_auto_discover",  # 13
    # 14–17: Export discovery edge cases
    "gdtest_no_all",  # 14
    "gdtest_gt_exclude",  # 15
    "gdtest_config_exclude",  # 16
    "gdtest_auto_exclude",  # 17
    # 18–27: Object type archetypes
    "gdtest_small_class",  # 18
    "gdtest_big_class",  # 19
    "gdtest_dataclasses",  # 20
    "gdtest_enums",  # 21
    "gdtest_typed_containers",  # 22
    "gdtest_protocols",  # 23
    "gdtest_descriptors",  # 24
    "gdtest_dunders",  # 25
    "gdtest_nested_class",  # 26
    "gdtest_constants",  # 27
    # 28–32: Directive combinations
    "gdtest_families",  # 28
    "gdtest_ordered",  # 29
    "gdtest_seealso",  # 30
    "gdtest_nodoc",  # 31
    "gdtest_mixed_directives",  # 32
    # 33–38: User guide variants
    "gdtest_user_guide_auto",  # 33
    "gdtest_user_guide_sections",  # 34
    "gdtest_user_guide_subdirs",  # 35
    "gdtest_user_guide_explicit",  # 36
    "gdtest_user_guide_custom_dir",  # 37
    "gdtest_user_guide_hyphen",  # 38
    # 39–43: Landing page / index variants
    "gdtest_readme_rst",  # 39
    "gdtest_index_qmd",  # 40
    "gdtest_index_md",  # 41
    "gdtest_no_readme",  # 42
    "gdtest_index_wins",  # 43
    # 44–45: Supporting pages
    "gdtest_full_extras",  # 44
    "gdtest_github_contrib",  # 45
    # 46–47: CLI documentation
    "gdtest_cli_click",  # 46
    "gdtest_cli_nested",  # 47
    # 48–50: Config-driven features
    "gdtest_explicit_ref",  # 48
    "gdtest_kitchen_sink",  # 49
    "gdtest_name_mismatch",  # 50
]


# ── Dimension metadata ───────────────────────────────────────────────────────

DIMENSIONS: dict[str, dict[str, str]] = {
    "A1": {"axis": "layout", "label": "Flat layout"},
    "A2": {"axis": "layout", "label": "src/ layout"},
    "A3": {"axis": "layout", "label": "python/ layout"},
    "A4": {"axis": "layout", "label": "lib/ layout"},
    "A5": {"axis": "layout", "label": "Hatch layout"},
    "A6": {"axis": "layout", "label": "Setuptools find"},
    "A7": {"axis": "layout", "label": "setup.cfg only"},
    "A8": {"axis": "layout", "label": "setup.py only"},
    "A9": {"axis": "layout", "label": "Auto-discover"},
    "B1": {"axis": "exports", "label": "Explicit __all__"},
    "B2": {"axis": "exports", "label": "__all__ concatenation"},
    "B3": {"axis": "exports", "label": "No __all__ (griffe)"},
    "B4": {"axis": "exports", "label": "__gt_exclude__"},
    "B5": {"axis": "exports", "label": "Config exclude"},
    "B6": {"axis": "exports", "label": "Submodule exports"},
    "B7": {"axis": "exports", "label": "AUTO_EXCLUDE names"},
    "C1": {"axis": "objects", "label": "Functions only"},
    "C2": {"axis": "objects", "label": "Small classes (≤5)"},
    "C3": {"axis": "objects", "label": "Big class (>5)"},
    "C4": {"axis": "objects", "label": "Mixed class+func"},
    "C5": {"axis": "objects", "label": "Dataclasses"},
    "C6": {"axis": "objects", "label": "Enums"},
    "C7": {"axis": "objects", "label": "NamedTuple/TypedDict"},
    "C8": {"axis": "objects", "label": "ABC/Protocol"},
    "C9": {"axis": "objects", "label": "Descriptors"},
    "C10": {"axis": "objects", "label": "Dunder methods"},
    "C11": {"axis": "objects", "label": "Nested classes"},
    "C12": {"axis": "objects", "label": "Constants/aliases"},
    "D1": {"axis": "docstrings", "label": "NumPy"},
    "D2": {"axis": "docstrings", "label": "Google"},
    "D3": {"axis": "docstrings", "label": "Sphinx"},
    "D4": {"axis": "docstrings", "label": "No docstrings"},
    "D5": {"axis": "docstrings", "label": "Mixed styles"},
    "E1": {"axis": "directives", "label": "%family"},
    "E2": {"axis": "directives", "label": "%family + %order"},
    "E3": {"axis": "directives", "label": "%seealso"},
    "E4": {"axis": "directives", "label": "%nodoc"},
    "E5": {"axis": "directives", "label": "Mixed directives"},
    "E6": {"axis": "directives", "label": "No directives"},
    "F1": {"axis": "user_guide", "label": "Auto-discover"},
    "F2": {"axis": "user_guide", "label": "Frontmatter sections"},
    "F3": {"axis": "user_guide", "label": "Subdirectories"},
    "F4": {"axis": "user_guide", "label": "Explicit ordering"},
    "F5": {"axis": "user_guide", "label": "Custom dir"},
    "F6": {"axis": "user_guide", "label": "No user guide"},
    "F7": {"axis": "user_guide", "label": "Hyphenated dir"},
    "G1": {"axis": "landing", "label": "README.md"},
    "G2": {"axis": "landing", "label": "README.rst"},
    "G3": {"axis": "landing", "label": "index.qmd"},
    "G4": {"axis": "landing", "label": "index.md"},
    "G5": {"axis": "landing", "label": "No readme"},
    "G6": {"axis": "landing", "label": "index.qmd wins"},
    "H1": {"axis": "extras", "label": "LICENSE"},
    "H2": {"axis": "extras", "label": "CITATION.cff"},
    "H3": {"axis": "extras", "label": "CONTRIBUTING.md"},
    "H4": {"axis": "extras", "label": "CODE_OF_CONDUCT.md"},
    "H5": {"axis": "extras", "label": ".github/CONTRIBUTING.md"},
    "H6": {"axis": "extras", "label": "assets/"},
    "H7": {"axis": "extras", "label": "No extras"},
}


# ── Plain-English package descriptions ────────────────────────────────────────
# Each entry gives a human-friendly explanation of what the synthetic package
# exercises and why it matters. Displayed on the hub card and detail pages.

PACKAGE_DESCRIPTIONS: dict[str, str] = {
    "gdtest_minimal": (
        "The simplest possible package: a single flat module with one function "
        "that has a NumPy-style docstring and an explicit __all__. This is the "
        "baseline build — if this fails, nothing else will work. Verifies that "
        "Great Docs can detect the package name from pyproject.toml, find the "
        "module in a flat layout, and render a minimal reference page."
    ),
    "gdtest_google": (
        "A flat-layout package whose docstrings are written entirely in Google "
        "style (Args/Returns/Raises sections). Tests that the docstring format "
        "auto-detector correctly identifies Google style and that parameter "
        "tables, return values, and exception lists render properly."
    ),
    "gdtest_sphinx": (
        "Docstrings written in classic Sphinx/reST style using :param:, "
        ":returns:, :rtype:, and :raises: field lists. Verifies the docstring "
        "parser handles Sphinx conventions and that the rendered output "
        "correctly shows parameter types, defaults, and exception information."
    ),
    "gdtest_nodocs": (
        "A package where every exported object — functions, classes, and "
        "constants — has no docstring at all. Tests that Great Docs gracefully "
        "handles undocumented objects without crashing, still lists them in the "
        "reference, and does not produce broken HTML."
    ),
    "gdtest_mixed_docs": (
        "A single module that mixes NumPy-style and Google-style docstrings "
        "across different functions. Tests per-object docstring format "
        "detection and verifies that both styles render cleanly within the "
        "same reference page."
    ),
    "gdtest_src_layout": (
        "A modern src-layout package where the importable module lives under "
        "src/gdtest_src_layout/. This is the most common layout for packages "
        "using modern Python packaging. Tests that Great Docs correctly "
        "searches the src/ subdirectory when locating __init__.py."
    ),
    "gdtest_python_layout": (
        "Uses the less common python/ subdirectory layout (e.g., as used by "
        "some scientific packages). The module lives at python/gdtest_pylayout/. "
        "Verifies Great Docs expands its search path to include python/ as a "
        "source root."
    ),
    "gdtest_lib_layout": (
        "Uses a lib/ subdirectory layout for the module source. Similar to "
        "python/ but with lib/ as the source root. Tests that all three "
        "non-standard source roots (src/, python/, lib/) are handled."
    ),
    "gdtest_hatch": (
        "Configured with the Hatch build system, specifying an explicit wheel "
        "package location via [tool.hatch.build.targets.wheel]. The importable "
        "module name differs from the project name. Tests that Great Docs "
        "reads Hatch build metadata to resolve the correct module."
    ),
    "gdtest_setuptools_find": (
        "Uses setuptools find:packages with a where=src directive in "
        "pyproject.toml. The module is at src/gdtest_stfind/. Tests that Great "
        "Docs parses setuptools find configuration to locate the package root "
        "rather than relying on simple directory scanning."
    ),
    "gdtest_setup_cfg": (
        "An older-style package that uses only setup.cfg for metadata — there "
        "is no pyproject.toml. Tests that Great Docs can detect the package "
        "name and version from setup.cfg's [metadata] section and still "
        "produce a working documentation site."
    ),
    "gdtest_setup_py": (
        "A legacy package with only a setup.py file containing a setup() call. "
        "No pyproject.toml or setup.cfg. Tests the oldest supported metadata "
        "format and verifies that Great Docs falls back to parsing setup.py "
        "for the package name."
    ),
    "gdtest_auto_discover": (
        "A package with no metadata files at all — no pyproject.toml, no "
        "setup.cfg, no setup.py. The only signal is a single top-level "
        "directory containing __init__.py. Tests the auto-discovery fallback "
        "where Great Docs infers the package from directory structure alone."
    ),
    "gdtest_no_all": (
        "A module with no __all__ list defined. Functions and classes are "
        "defined at module scope alongside private names. Tests the griffe "
        "fallback discovery mode that infers the public API by examining "
        "module-level definitions and filtering out private names."
    ),
    "gdtest_gt_exclude": (
        "Defines __all__ with several exports but also sets __gt_exclude__ = "
        "['secret_func'] to exclude specific names from documentation. Tests "
        "the legacy exclusion mechanism that lets package authors hide objects "
        "without removing them from __all__."
    ),
    "gdtest_config_exclude": (
        "All functions are listed in __all__, but great-docs.yml contains an "
        "exclude list that removes specific names. Tests config-level "
        "exclusion as an alternative to code-level __gt_exclude__, useful when "
        "authors cannot or prefer not to modify package source."
    ),
    "gdtest_auto_exclude": (
        "Exports common utility names like main, cli, config, setup, and "
        "conftest that match Great Docs' AUTO_EXCLUDE set. Tests that these "
        "boilerplate names are automatically filtered out of the reference "
        "unless explicitly overridden."
    ),
    "gdtest_small_class": (
        "A package with small classes that have 5 or fewer public methods. "
        "Small classes are rendered inline in the reference page rather than "
        "getting their own separate method section. Tests the threshold logic "
        "that decides between inline and expanded rendering."
    ),
    "gdtest_big_class": (
        "Contains a class with more than 5 public methods, which triggers "
        "Great Docs' expanded rendering mode. Each method gets its own "
        "subsection on a dedicated methods page. Tests method extraction, "
        "sorting, and the big-class section generation pipeline."
    ),
    "gdtest_dataclasses": (
        "Uses Python @dataclass decorators with various field types including "
        "defaults, field() calls, and type annotations. Tests that Great Docs "
        "correctly represents dataclass fields in the reference and renders "
        "their docstrings and type hints."
    ),
    "gdtest_enums": (
        "Defines Enum and IntEnum subclasses with documented members. Tests "
        "that enum types are correctly identified, their values are displayed "
        "in the reference, and member docstrings (if any) are rendered."
    ),
    "gdtest_typed_containers": (
        "Uses NamedTuple and TypedDict — typed container types that have "
        "field-level documentation via docstrings or annotations. Tests that "
        "these special class forms are rendered with their field signatures "
        "intact."
    ),
    "gdtest_protocols": (
        "Defines ABC abstract base classes and Protocol types with abstract "
        "methods. Tests that abstract methods are marked correctly in the "
        "rendered docs and that Protocol structural typing is represented."
    ),
    "gdtest_descriptors": (
        "A class with @property, @classmethod, and @staticmethod descriptors. "
        "Tests that each descriptor kind is identified and rendered with the "
        "correct decorator label and signature."
    ),
    "gdtest_dunders": (
        "A class that defines dunder methods: __init__, __repr__, __eq__, "
        "__len__, __getitem__, and __iter__. Tests that dunder methods are "
        "included in documentation when they have docstrings, and that their "
        "signatures render correctly."
    ),
    "gdtest_nested_class": (
        "Contains a class with inner/nested class definitions. Tests how "
        "Great Docs handles nested classes — whether they appear as separate "
        "reference items or are nested under the parent class."
    ),
    "gdtest_constants": (
        "Module-level constants and type aliases (using TypeAlias or plain "
        "assignment). Tests that non-callable exports are recognized and "
        "rendered in the reference with their values and type annotations."
    ),
    "gdtest_families": (
        "Functions tagged with the %family directive in their docstrings to "
        "group them into named sections (e.g., 'Input/Output', 'Transform'). "
        "Tests that the %family directive is parsed and that the reference "
        "page organizes items under the correct section headings."
    ),
    "gdtest_ordered": (
        "Combines %family with %order directives to control both grouping and "
        "sort order within each section. Tests that items appear in the "
        "specified numeric order rather than alphabetically."
    ),
    "gdtest_seealso": (
        "Functions with %seealso directives linking to related functions. "
        "Tests that cross-reference links are generated correctly in the "
        "rendered output, pointing to other documented items on the same "
        "reference page."
    ),
    "gdtest_nodoc": (
        "Some functions are tagged with %nodoc in their docstrings to exclude "
        "them from documentation entirely. Tests that %nodoc items are "
        "filtered out during reference generation while other exports remain."
    ),
    "gdtest_mixed_directives": (
        "A package where some functions use directives (%family, %order, "
        "%seealso) and others have none. Tests that the directive parser "
        "handles the mix gracefully — directive-tagged items are grouped and "
        "ordered while plain items fall into a default section."
    ),
    "gdtest_user_guide_auto": (
        "Has a user_guide/ directory with numerically-prefixed .qmd files "
        "(01-intro.qmd, 02-basics.qmd, etc.). Tests the auto-discovery mode "
        "that finds user guide pages and orders them by their numeric prefix."
    ),
    "gdtest_user_guide_sections": (
        "User guide .qmd files include frontmatter with guide-section keys "
        "that group pages under section headings in the sidebar. Tests that "
        "guide-section metadata is parsed and reflected in the navigation."
    ),
    "gdtest_user_guide_subdirs": (
        "User guide pages are organized into subdirectories (getting-started/, "
        "advanced/) rather than a flat list. Tests that the recursive "
        "discovery walks subdirectories and preserves hierarchy."
    ),
    "gdtest_user_guide_explicit": (
        "The user guide page order is explicitly defined in great-docs.yml "
        "rather than auto-discovered. Tests config-driven user guide ordering "
        "as an alternative to filename-based sorting."
    ),
    "gdtest_user_guide_custom_dir": (
        "The user guide lives in a non-standard directory (docs/tutorials/ "
        "instead of user_guide/). The path is specified in great-docs.yml. "
        "Tests custom user guide directory configuration."
    ),
    "gdtest_user_guide_hyphen": (
        "Uses a hyphenated directory name (user-guide/) instead of the "
        "underscored default (user_guide/). Tests that both naming conventions "
        "are supported for user guide auto-discovery."
    ),
    "gdtest_readme_rst": (
        "The landing page is a README.rst written in reStructuredText rather "
        "than Markdown. Tests RST-to-QMD conversion and verifies that RST "
        "constructs (headings, code blocks, links) translate correctly."
    ),
    "gdtest_index_qmd": (
        "Provides an index.qmd file that Great Docs uses as-is for the "
        "landing page, without any conversion or generation. Tests the "
        "pass-through behavior for pre-authored Quarto index files."
    ),
    "gdtest_index_md": (
        "Has both README.md and index.md at the project root. index.md takes "
        "priority over README.md as the landing page source. Tests the file "
        "priority ordering in landing page detection."
    ),
    "gdtest_no_readme": (
        "Has no README.md, README.rst, index.md, or index.qmd. Great Docs "
        "must auto-generate a minimal landing page from package metadata. "
        "Tests the fallback landing page generation when no source file exists."
    ),
    "gdtest_index_wins": (
        "Has both a README.md and an index.qmd. The index.qmd should take "
        "priority and be used as-is. Tests the complete priority chain: "
        "index.qmd > index.md > README.md > README.rst > auto-generated."
    ),
    "gdtest_full_extras": (
        "Includes every supporting page type: LICENSE, CITATION.cff, "
        "CONTRIBUTING.md, CODE_OF_CONDUCT.md, CHANGELOG.md, and an assets/ "
        "directory. Tests that all optional supporting pages are detected, "
        "converted, and linked in the navigation."
    ),
    "gdtest_github_contrib": (
        "Stores CONTRIBUTING.md in the .github/ subdirectory rather than the "
        "project root — a common convention for GitHub repos. Tests the "
        "fallback search path that checks .github/ when the root file is missing."
    ),
    "gdtest_cli_click": (
        "A package with simple Click CLI commands and CLI documentation "
        "enabled in great-docs.yml. Tests automatic CLI reference generation "
        "from Click command definitions."
    ),
    "gdtest_cli_nested": (
        "A Click CLI with nested command groups and subcommands (e.g., "
        "main > sub-group > command). Tests that the CLI documentation "
        "generator handles multi-level group hierarchies and renders them "
        "with proper nesting."
    ),
    "gdtest_explicit_ref": (
        "The reference page structure is explicitly defined in great-docs.yml "
        "rather than auto-generated from exports. Tests config-driven "
        "reference sections where the author specifies exactly which objects "
        "appear in which section."
    ),
    "gdtest_kitchen_sink": (
        "The maximum-coverage package that combines as many features as "
        "possible: src/ layout, mixed docstring styles, big and small classes, "
        "directives, user guide, supporting pages, CLI docs, and more. Tests "
        "that all features coexist without conflicts in a single build."
    ),
    "gdtest_name_mismatch": (
        "The pyproject.toml project name ('gdtest-name-mismatch') does not "
        "match the importable module name ('gdtest_nm_mod'). The config "
        "overrides the module name. Tests the name/module disambiguation "
        "logic and config-driven module name resolution."
    ),
}


# ── Spec access ──────────────────────────────────────────────────────────────

_spec_cache: dict[str, dict[str, Any]] = {}


def get_spec(name: str) -> dict[str, Any]:
    """
    Load and return the spec dict for the given package name.

    Parameters
    ----------
    name
        One of the names in :data:`ALL_PACKAGES`.

    Returns
    -------
    dict
        The full spec dict (keys: name, dimensions, files, expected, …).
    """
    if name in _spec_cache:
        return _spec_cache[name]

    if name not in ALL_PACKAGES:
        raise ValueError(f"Unknown synthetic package: {name!r}")

    # Import from specs sub-package
    mod = importlib.import_module(f".specs.{name}", package=__package__)
    spec: dict[str, Any] = mod.SPEC  # type: ignore[attr-defined]

    # Validate minimal required keys
    assert spec.get("name") == name, f"Spec 'name' must be {name!r}, got {spec.get('name')!r}"
    assert "files" in spec, f"Spec for {name!r} must have a 'files' dict"

    _spec_cache[name] = spec
    return spec


def get_specs_by_dimension(dim_code: str) -> list[dict[str, Any]]:
    """
    Return all specs whose ``dimensions`` list contains *dim_code*.

    Parameters
    ----------
    dim_code
        A dimension code like ``"A2"`` or ``"C5"``.

    Returns
    -------
    list[dict]
        Matched specs (loaded lazily).
    """
    results: list[dict[str, Any]] = []
    for name in ALL_PACKAGES:
        spec = get_spec(name)
        if dim_code in spec.get("dimensions", []):
            results.append(spec)
    return results

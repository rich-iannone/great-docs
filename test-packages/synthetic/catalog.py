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
        "The simplest possible package: two functions (greet, add) with NumPy "
        "docstrings in a flat layout. On the Reference page you should see a "
        "single 'Functions' section listing both. Each function should show a "
        "Parameters table and a Returns block. If this build fails, nothing "
        "else will work."
    ),
    "gdtest_google": (
        "Three functions (connect, disconnect, send_message) documented in "
        "Google style with Args/Returns/Raises sections. On the Reference page "
        "you should see a 'Functions' section. Each function's rendered docs "
        "should display parameter tables and return types parsed from the "
        "Google-style format — not raw 'Args:' text."
    ),
    "gdtest_sphinx": (
        "Three exports (Timer class, start_timer, format_duration) with "
        "classic Sphinx :param:/:returns:/:rtype:/:raises: field lists. On "
        "the Reference page you should see 'Classes' and 'Functions' sections. "
        "Parameter types and defaults should be rendered from the Sphinx field "
        "list syntax, not shown as raw :param: markers."
    ),
    "gdtest_nodocs": (
        "Four exports (Processor class, run, stop, status) with zero "
        "docstrings. On the Reference page you should see 'Classes' and "
        "'Functions' sections listing all four items, but each entry should "
        "have no description text — just the signature. The page must not "
        "crash or show broken rendering."
    ),
    "gdtest_mixed_docs": (
        "Five exports (Converter class, encode, decode, validate, transform) "
        "mixing NumPy and Google docstrings in the same module. On the "
        "Reference page you should see 'Classes' and 'Functions' sections. "
        "Both docstring styles should be rendered cleanly — NumPy Parameters "
        "tables and Google Args sections should both appear correctly."
    ),
    "gdtest_src_layout": (
        "Module lives under src/gdtest_src_layout/ (modern src-layout). "
        "Three exports (Widget class, create_widget, destroy_widget). On the "
        "Reference page you should see 'Classes' and 'Functions' sections. "
        "The key test: Great Docs must find the module inside src/ without "
        "any explicit path configuration."
    ),
    "gdtest_python_layout": (
        "Module lives under python/gdtest_pylayout/ (less common convention). "
        "Two functions (read_file, write_file). On the Reference page you "
        "should see a 'Functions' section with both. The key test: Great Docs "
        "searches the python/ subdirectory as a source root."
    ),
    "gdtest_lib_layout": (
        "Module lives under lib/gdtest_lib_layout/. Two functions "
        "(open_connection, close_connection). On the Reference page you should "
        "see a 'Functions' section with both. The key test: lib/ is recognized "
        "as a source root alongside src/ and python/."
    ),
    "gdtest_hatch": (
        "Uses the Hatch build system with [tool.hatch.build.targets.wheel] "
        "specifying the package location. The module name (gdtest_hatch_pkg) "
        "differs from the project name (gdtest-hatch). On the Reference page "
        "you should see 'Classes' (Builder) and 'Functions' (build, clean). "
        "The key test: module discovery via Hatch metadata."
    ),
    "gdtest_setuptools_find": (
        "Uses setuptools find:packages with where=src. Module is at "
        "src/gdtest_stfind/ (different name from the project). Three exports "
        "(Scanner class, scan, report). On the Reference page you should see "
        "'Classes' and 'Functions' sections. The key test: Great Docs parses "
        "setuptools find configuration to locate the correct module."
    ),
    "gdtest_setup_cfg": (
        "No pyproject.toml — only setup.cfg for metadata. Two functions "
        "(ping, pong). On the Reference page you should see a 'Functions' "
        "section. The site title should be 'gdtest-setup-cfg' (read from "
        "setup.cfg [metadata]). The key test: metadata detection falls back "
        "to setup.cfg."
    ),
    "gdtest_setup_py": (
        "No pyproject.toml, no setup.cfg — only a legacy setup.py. Two "
        "functions (echo, reverse). On the Reference page you should see a "
        "'Functions' section. The site title should be 'gdtest-setup-py'. "
        "The key test: name detection falls back to parsing setup.py."
    ),
    "gdtest_auto_discover": (
        "No pyproject.toml, no setup.cfg, no setup.py — zero metadata files. "
        "Three exports (Engine class, ignite, shutdown). On the Reference page "
        "you should see 'Classes' and 'Functions' sections. The key test: "
        "Great Docs discovers the package purely from directory structure."
    ),
    "gdtest_no_all": (
        "Module defines functions and classes but has no __all__ list. Three "
        "exports (Registry class, create_registry, list_keys) discovered via "
        "griffe fallback. On the Reference page you should see these three "
        "items but NOT any names starting with underscore. The key test: "
        "griffe-based public API inference without __all__."
    ),
    "gdtest_gt_exclude": (
        "Defines __all__ with four items but sets __gt_exclude__ = "
        "['internal_func', 'helper'] to hide two. On the Reference page you "
        "should see only public_func and PublicClass — internal_func and "
        "helper must be absent. The key test: code-level exclusion via the "
        "legacy __gt_exclude__ mechanism."
    ),
    "gdtest_config_exclude": (
        "All four exports are in __all__, but great-docs.yml excludes "
        "helper_func and InternalClass. On the Reference page you should see "
        "only PublicAPI and transform — the excluded items must be absent. "
        "The key test: config-level exclusion as an alternative to code-level "
        "__gt_exclude__."
    ),
    "gdtest_auto_exclude": (
        "Module exports common boilerplate names (main, cli, config, utils, "
        "logger) alongside real API (MyClass, real_func). On the Reference "
        "page you should see only MyClass and real_func — the AUTO_EXCLUDE "
        "names must be filtered out automatically."
    ),
    "gdtest_small_class": (
        "Two small classes (Point, Color) each with ≤5 methods. On the "
        "Reference page you should see a 'Classes' section where methods are "
        "rendered inline within each class entry — there should be NO separate "
        "'Point Methods' or 'Color Methods' subsection pages."
    ),
    "gdtest_big_class": (
        "DataProcessor class has 8 public methods, exceeding the threshold "
        "for expanded rendering. On the Reference page you should see three "
        "sections: 'Classes', 'DataProcessor Methods' (a dedicated subsection "
        "listing all 8 methods), and 'Functions' (load_data, save_data). "
        "The key test: big-class method extraction into a separate section."
    ),
    "gdtest_dataclasses": (
        "Two @dataclass types (Config, Record) with typed fields, defaults, "
        "and field() calls. On the Reference page you should see a 'Classes' "
        "section. Each dataclass should show its field signatures with type "
        "annotations and default values rendered in the constructor docs."
    ),
    "gdtest_enums": (
        "Two enum types: Color (Enum with RED/GREEN/BLUE) and Priority "
        "(IntEnum with LOW/MEDIUM/HIGH). On the Reference page you should "
        "see a 'Classes' section listing both. Enum members and their values "
        "should be visible in the rendered docs."
    ),
    "gdtest_typed_containers": (
        "Coordinate (NamedTuple) and UserProfile (TypedDict) — typed "
        "container types with field-level annotations. On the Reference page "
        "you should see a 'Classes' section. Each type's fields should appear "
        "with their type annotations intact."
    ),
    "gdtest_protocols": (
        "Serializable (ABC) and Renderable (Protocol) with abstract methods. "
        "On the Reference page you should see a 'Classes' section listing "
        "both. Abstract methods should be shown with their signatures. "
        "The key test: ABC/Protocol types are handled without errors."
    ),
    "gdtest_descriptors": (
        "Resource class with @property (name), @classmethod (from_dict), and "
        "@staticmethod (validate). On the Reference page you should see a "
        "'Classes' section. Each descriptor should display with its correct "
        "decorator label — property, classmethod, or staticmethod markers."
    ),
    "gdtest_dunders": (
        "Collection class with 6 dunder methods: __init__, __repr__, __eq__, "
        "__len__, __getitem__, __iter__. On the Reference page you should see "
        "a 'Classes' section. The dunder methods should appear in the class "
        "documentation with their docstrings and signatures rendered."
    ),
    "gdtest_nested_class": (
        "Tree class with a nested Node inner class. On the Reference page you "
        "should see a 'Classes' section with Tree. The inner Node class should "
        "appear under Tree — check whether it renders as a nested entry or a "
        "separate top-level item."
    ),
    "gdtest_constants": (
        "Five exports: three constants (DEFAULT_TIMEOUT, MAX_RETRIES, "
        "SUPPORTED_FORMATS), one type alias (HandlerFunc), and one function "
        "(process). On the Reference page you should see both constants and "
        "the function listed. Constants should show their values and type "
        "annotations."
    ),
    "gdtest_families": (
        "Eight exports grouped by %family into 'Validation' (Validate, "
        "col_vals_gt, col_vals_lt, col_vals_between, col_exists) and "
        "'Formatting' (fmt_number, fmt_percent), plus one ungrouped (helper). "
        "On the Reference page you should see these as separate section "
        "headings — NOT a single flat 'Functions' list."
    ),
    "gdtest_ordered": (
        "Seven exports grouped by %family + %order: 'Processing' (Pipeline, "
        "step_validate, step_transform, step_load, step_export) and 'Logging' "
        "(log_start, log_end). On the Reference page the items within each "
        "section should appear in the specified numeric order, not "
        "alphabetically. Check that step_validate comes before step_transform."
    ),
    "gdtest_seealso": (
        "Four exports (Encoder class, encode, decode, validate) with %seealso "
        "cross-references. On the Reference page, each function's docs should "
        "include a 'See Also' block with links to the related functions. "
        "For example, encode's docs should link to decode and validate."
    ),
    "gdtest_nodoc": (
        "Four exports in __all__ (Calculator, compute, reset, debug_info) but "
        "reset and debug_info are tagged with %nodoc. On the Reference page "
        "you should see only Calculator and compute — reset and debug_info "
        "must be completely absent from the rendered docs."
    ),
    "gdtest_mixed_directives": (
        "Six exports: three tagged with %family 'Parsing' (Parser, parse_json, "
        "parse_csv) and three with no directives (format_output, "
        "validate_schema, count_records). On the Reference page you should "
        "see a 'Parsing' section heading for the tagged items and a separate "
        "default section for the untagged ones."
    ),
    "gdtest_user_guide_auto": (
        "Has user_guide/ with three numbered files: 01-intro.qmd, "
        "02-quickstart.qmd, 03-advanced.qmd. The sidebar should show a "
        "'User Guide' section with these three pages in numeric order. "
        "Clicking each should navigate to the corresponding guide page. "
        "The Reference page should show App (class) and run_app (function)."
    ),
    "gdtest_user_guide_sections": (
        "Has user_guide/ with four pages that use frontmatter guide-section "
        "keys: 01-welcome and 02-install under 'Getting Started', "
        "03-customization and 04-plugins under 'Advanced'. In the sidebar, "
        "user guide pages should be grouped under these section headings, "
        "not listed flat."
    ),
    "gdtest_user_guide_subdirs": (
        "User guide pages are in subdirectories: user_guide/basics/ "
        "(01-intro.qmd, 02-setup.qmd) and user_guide/advanced/ (01-tips.qmd). "
        "The sidebar should show user guide pages preserving the subdirectory "
        "hierarchy — basics and advanced as separate groups."
    ),
    "gdtest_user_guide_explicit": (
        "User guide order is defined in great-docs.yml: 'Get Started' section "
        "(Welcome → quickstart.qmd) then 'Advanced' section (advanced.qmd). "
        "The sidebar should show exactly this ordering, ignoring filename "
        "sort. 'Welcome' should use custom text (not the filename)."
    ),
    "gdtest_user_guide_custom_dir": (
        "User guide lives in docs/guides/ instead of user_guide/. The config "
        "specifies user_guide: 'docs/guides'. In the sidebar you should see "
        "user guide pages from this custom directory. Two functions (fetch, "
        "store) should appear on the Reference page."
    ),
    "gdtest_user_guide_hyphen": (
        "Uses user-guide/ (with hyphen) instead of user_guide/ (with "
        "underscore). One guide page: 01-intro.qmd. The sidebar should show "
        "a 'User Guide' section with this page. The key test: both naming "
        "conventions (hyphen and underscore) are supported."
    ),
    "gdtest_readme_rst": (
        "Landing page source is README.rst in reStructuredText. The landing "
        "page should show the converted content — RST headings, code blocks, "
        "and links should render as proper HTML, not raw RST markup. Two "
        "functions (convert, parse) on the Reference page."
    ),
    "gdtest_index_qmd": (
        "Provides an index.qmd with title 'Custom Landing Page'. The landing "
        "page should display this Quarto content as-is — look for the text "
        "'This is a custom landing page written in Quarto markdown.' The "
        "Reference page should show one function (hello)."
    ),
    "gdtest_index_md": (
        "Has both README.md and index.md. The landing page should show the "
        "index.md content ('Custom Index') NOT the README.md content. Look "
        "for the text 'This is index.md and should take priority over "
        "README.md.' One function (greet) on the Reference page."
    ),
    "gdtest_no_readme": (
        "Has no README, no index file — nothing for the landing page. Great "
        "Docs auto-generates a minimal landing page from package metadata. "
        "The landing page should show the package name and an installation "
        "command. One function (noop) on the Reference page."
    ),
    "gdtest_index_wins": (
        "Has both index.qmd and README.md. The landing page should show the "
        "index.qmd content ('Index Wins') NOT the README.md. Look for the "
        "text 'This index.qmd should take priority over README.md.' Tests the "
        "full priority chain: index.qmd > index.md > README.md."
    ),
    "gdtest_full_extras": (
        "Includes every supporting page type. The sidebar/nav should show "
        "links to: License, Citation, Contributing, and Code of Conduct. "
        "There should also be a User Guide section (Getting Started, "
        "Configuration). The Reference page should show Manager (class), "
        "start and stop (functions)."
    ),
    "gdtest_github_contrib": (
        "CONTRIBUTING.md lives in .github/ (not the project root). The "
        "sidebar should still show a Contributing link. Clicking it should "
        "display the contributing content. The Reference page should show "
        "two functions (process, validate). The key test: .github/ fallback "
        "path for contributing."
    ),
    "gdtest_cli_click": (
        "A package with Click CLI commands and cli.enabled=true in config. "
        "The sidebar should show a CLI Reference section alongside the API "
        "Reference. The CLI reference page should document the Click commands. "
        "The API Reference should show Formatter (class) and format_text "
        "(function)."
    ),
    "gdtest_cli_nested": (
        "Click CLI with nested groups: main command → task group (run, list) "
        "and config group (show, set). The CLI Reference should show the "
        "multi-level command hierarchy with subgroups. The API Reference "
        "should show Engine (class) and run_task (function)."
    ),
    "gdtest_explicit_ref": (
        "Reference structure is defined in great-docs.yml with two sections: "
        "'Core' (MyClass with members=false, helper_func) and 'Utilities' "
        "(util_a, util_b). On the Reference page you should see exactly these "
        "two named sections — not auto-generated ones. MyClass should appear "
        "WITHOUT its methods (members: false)."
    ),
    "gdtest_kitchen_sink": (
        "Maximum coverage: src/ layout, 10 exports, %family sections (Core "
        "and Utility), Pipeline as a big class with 6+ methods, user guide "
        "(3 pages), all supporting pages (License, Citation, Contributing, "
        "Code of Conduct), author metadata in sidebar, display_name 'Kitchen "
        "Sink'. Every feature should work together without conflicts."
    ),
    "gdtest_name_mismatch": (
        "Project name is 'gdtest-name-mismatch' but the module is 'gdtest_nm' "
        "(completely different). Config sets module: gdtest_nm. The site title "
        "should use the project name. The Reference page should show exports "
        "from gdtest_nm: Mapper (class) and transform (function). The key "
        "test: config-driven module name override."
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

from __future__ import annotations

import json
from pathlib import Path

from great_docs._api_diff import (
    ApiSnapshot,
    ParameterInfo,
    SymbolInfo,
    compute_version_badges,
    inject_badges_into_qmd,
    load_snapshots_for_annotations,
    render_badge_html,
)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


def _make_symbol(name: str, kind: str = "function", **kwargs) -> SymbolInfo:
    return SymbolInfo(name=name, kind=kind, **kwargs)


def _make_snapshot(version: str, symbols: dict[str, SymbolInfo] | None = None) -> ApiSnapshot:
    return ApiSnapshot(
        version=version,
        package_name="test_pkg",
        symbols=symbols or {},
    )


# ---------------------------------------------------------------------------
# ParameterInfo serialization
# ---------------------------------------------------------------------------


class TestParameterInfoSerialization:
    def test_roundtrip(self):
        p = ParameterInfo(name="x", annotation="int", default="0", kind="POSITIONAL_OR_KEYWORD")
        d = p.to_dict()
        assert d["name"] == "x"
        assert d["annotation"] == "int"
        assert d["default"] == "0"
        assert d["kind"] == "POSITIONAL_OR_KEYWORD"
        restored = ParameterInfo.from_dict(d)
        assert restored == p

    def test_minimal_roundtrip(self):
        p = ParameterInfo(name="y")
        d = p.to_dict()
        assert "annotation" not in d
        assert "default" not in d
        restored = ParameterInfo.from_dict(d)
        assert restored.name == "y"
        assert restored.annotation is None
        assert restored.default is None


# ---------------------------------------------------------------------------
# SymbolInfo serialization
# ---------------------------------------------------------------------------


class TestSymbolInfoSerialization:
    def test_roundtrip_function(self):
        sym = SymbolInfo(
            name="foo",
            kind="function",
            parameters=[
                ParameterInfo(name="x", annotation="int"),
                ParameterInfo(name="y", annotation="str", default="''"),
            ],
            return_annotation="bool",
            is_async=True,
            decorators=["@cache"],
        )
        d = sym.to_dict()
        assert d["name"] == "foo"
        assert d["kind"] == "function"
        assert d["is_async"] is True
        assert len(d["parameters"]) == 2
        assert d["return_annotation"] == "bool"
        assert d["decorators"] == ["@cache"]

        restored = SymbolInfo.from_dict(d)
        assert restored == sym

    def test_roundtrip_class(self):
        sym = SymbolInfo(
            name="Bar",
            kind="class",
            bases=["Base", "Mixin"],
        )
        d = sym.to_dict()
        assert d["bases"] == ["Base", "Mixin"]
        assert "parameters" not in d  # empty list omitted
        assert "is_async" not in d  # False omitted

        restored = SymbolInfo.from_dict(d)
        assert restored == sym

    def test_minimal(self):
        sym = SymbolInfo(name="x", kind="attribute")
        d = sym.to_dict()
        assert d == {"name": "x", "kind": "attribute"}
        restored = SymbolInfo.from_dict(d)
        assert restored == sym


# ---------------------------------------------------------------------------
# ApiSnapshot serialization
# ---------------------------------------------------------------------------


class TestApiSnapshotSerialization:
    def test_roundtrip(self):
        snap = _make_snapshot(
            "v1.0",
            {
                "foo": _make_symbol("foo", parameters=[ParameterInfo(name="x", annotation="int")]),
                "Bar": _make_symbol("Bar", kind="class", bases=["Base"]),
            },
        )
        d = snap.to_dict()
        assert d["version"] == "v1.0"
        assert d["package_name"] == "test_pkg"
        assert "foo" in d["symbols"]
        assert "Bar" in d["symbols"]

        restored = ApiSnapshot.from_dict(d)
        assert restored.version == snap.version
        assert restored.package_name == snap.package_name
        assert set(restored.symbols.keys()) == set(snap.symbols.keys())
        assert restored.symbols["foo"] == snap.symbols["foo"]
        assert restored.symbols["Bar"] == snap.symbols["Bar"]

    def test_empty_snapshot(self):
        snap = _make_snapshot("v0.0")
        d = snap.to_dict()
        assert d["symbols"] == {}
        restored = ApiSnapshot.from_dict(d)
        assert restored.symbol_count == 0

    def test_save_and_load(self, tmp_path: Path):
        snap = _make_snapshot(
            "v2.0",
            {"baz": _make_symbol("baz", return_annotation="str")},
        )
        out = tmp_path / "snapshots" / "v2.0.json"
        snap.save(out)

        assert out.exists()
        # Verify it's valid JSON
        data = json.loads(out.read_text())
        assert data["version"] == "v2.0"

        loaded = ApiSnapshot.load(out)
        assert loaded.version == "v2.0"
        assert loaded.symbols["baz"].return_annotation == "str"

    def test_save_creates_parent_dirs(self, tmp_path: Path):
        snap = _make_snapshot("v1.0")
        out = tmp_path / "deep" / "nested" / "snap.json"
        snap.save(out)
        assert out.exists()


# ---------------------------------------------------------------------------
# Version badges
# ---------------------------------------------------------------------------


class TestComputeVersionBadges:
    def test_new_symbol(self):
        prev = _make_snapshot("v0.1", {"foo": _make_symbol("foo")})
        curr = _make_snapshot(
            "v0.2",
            {
                "foo": _make_symbol("foo"),
                "bar": _make_symbol("bar"),
            },
        )
        badges = compute_version_badges(curr, prev)
        assert "bar" in badges
        assert badges["bar"]["badge"] == "new"
        assert badges["bar"]["version"] == "v0.2"
        assert "foo" not in badges  # unchanged

    def test_changed_symbol(self):
        prev = _make_snapshot(
            "v0.1",
            {
                "foo": _make_symbol("foo", parameters=[ParameterInfo(name="x")]),
            },
        )
        curr = _make_snapshot(
            "v0.2",
            {
                "foo": _make_symbol(
                    "foo",
                    parameters=[ParameterInfo(name="x"), ParameterInfo(name="y")],
                ),
            },
        )
        badges = compute_version_badges(curr, prev)
        assert "foo" in badges
        assert badges["foo"]["badge"] == "changed"

    def test_deprecated_symbol(self):
        curr = _make_snapshot(
            "v0.3",
            {
                "old_func": _make_symbol("old_func", decorators=["@deprecated"]),
            },
        )
        badges = compute_version_badges(curr, None)
        assert "old_func" in badges
        assert badges["old_func"]["badge"] == "deprecated"

    def test_deprecated_overrides_changed(self):
        prev = _make_snapshot(
            "v0.1",
            {
                "foo": _make_symbol("foo", parameters=[ParameterInfo(name="x")]),
            },
        )
        curr = _make_snapshot(
            "v0.2",
            {
                "foo": _make_symbol(
                    "foo",
                    parameters=[ParameterInfo(name="y")],
                    decorators=["@deprecated"],
                ),
            },
        )
        badges = compute_version_badges(curr, prev)
        assert badges["foo"]["badge"] == "deprecated"

    def test_no_previous_returns_only_deprecations(self):
        curr = _make_snapshot(
            "v0.1",
            {
                "foo": _make_symbol("foo"),
                "bar": _make_symbol("bar"),
            },
        )
        badges = compute_version_badges(curr, None)
        # No badges for normal symbols in first version
        assert "foo" not in badges
        assert "bar" not in badges

    def test_empty_when_unchanged(self):
        snap = _make_snapshot("v0.1", {"foo": _make_symbol("foo")})
        badges = compute_version_badges(snap, snap)
        assert badges == {}


# ---------------------------------------------------------------------------
# Badge rendering
# ---------------------------------------------------------------------------


class TestRenderBadgeHtml:
    def test_new_badge(self):
        html = render_badge_html({"badge": "new", "version": "0.3"})
        assert "gd-badge-new" in html
        assert "New in 0.3" in html

    def test_changed_badge(self):
        html = render_badge_html({"badge": "changed", "version": "0.3"})
        assert "gd-badge-changed" in html
        assert "Changed in 0.3" in html

    def test_deprecated_badge(self):
        html = render_badge_html({"badge": "deprecated", "version": "0.3"})
        assert "gd-badge-deprecated" in html
        assert "Deprecated in 0.3" in html

    def test_html_escaping(self):
        html = render_badge_html({"badge": "new", "version": '<script>"xss"</script>'})
        assert "<script>" not in html
        assert "&lt;script&gt;" in html


# ---------------------------------------------------------------------------
# QMD injection
# ---------------------------------------------------------------------------


class TestInjectBadgesIntoQmd:
    def test_injects_after_heading(self):
        content = "## foo\n\nSome docs."
        badges = {"foo": {"badge": "new", "version": "0.3"}}
        result = inject_badges_into_qmd(content, badges)
        lines = result.split("\n")
        assert lines[0] == "## foo"
        assert "gd-badge-new" in lines[1]
        assert lines[2] == ""

    def test_qualified_name_heading(self):
        content = "### pkg.submod.Bar\n\nClass docs."
        badges = {"Bar": {"badge": "changed", "version": "0.2"}}
        result = inject_badges_into_qmd(content, badges)
        assert "gd-badge-changed" in result

    def test_heading_with_quarto_classes(self):
        content = "## foo { .doc-heading }\n\nDocs."
        badges = {"foo": {"badge": "new", "version": "0.3"}}
        result = inject_badges_into_qmd(content, badges)
        assert "gd-badge-new" in result

    def test_no_badges_returns_unchanged(self):
        content = "## foo\n\nSome docs."
        result = inject_badges_into_qmd(content, {})
        assert result == content

    def test_non_matching_headings_unchanged(self):
        content = "## Introduction\n\n## Getting Started\n"
        badges = {"foo": {"badge": "new", "version": "0.3"}}
        result = inject_badges_into_qmd(content, badges)
        assert result == content


# ---------------------------------------------------------------------------
# Snapshot loading
# ---------------------------------------------------------------------------


class TestLoadSnapshotsForAnnotations:
    def test_loads_both(self, tmp_path: Path):
        snap1 = _make_snapshot("v0.1", {"foo": _make_symbol("foo")})
        snap2 = _make_snapshot("v0.2", {"foo": _make_symbol("foo"), "bar": _make_symbol("bar")})
        snap1.save(tmp_path / "v0.1.json")
        snap2.save(tmp_path / "v0.2.json")

        curr, prev = load_snapshots_for_annotations(tmp_path, "v0.2", "v0.1")
        assert curr is not None
        assert prev is not None
        assert curr.version == "v0.2"
        assert prev.version == "v0.1"

    def test_missing_previous(self, tmp_path: Path):
        snap = _make_snapshot("v0.1")
        snap.save(tmp_path / "v0.1.json")

        curr, prev = load_snapshots_for_annotations(tmp_path, "v0.1", "v0.0")
        assert curr is not None
        assert prev is None

    def test_no_previous_version(self, tmp_path: Path):
        snap = _make_snapshot("v0.1")
        snap.save(tmp_path / "v0.1.json")

        curr, prev = load_snapshots_for_annotations(tmp_path, "v0.1", None)
        assert curr is not None
        assert prev is None

    def test_missing_both(self, tmp_path: Path):
        curr, prev = load_snapshots_for_annotations(tmp_path, "v1.0", "v0.9")
        assert curr is None
        assert prev is None

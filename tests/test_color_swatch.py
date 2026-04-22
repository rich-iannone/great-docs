"""Tests for the {{< color-swatch >}} Quarto shortcode extension."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest
import yaml


def _ext_dir() -> Path:
    return Path(__file__).parent.parent / "great_docs" / "assets" / "_extensions" / "color-swatch"


def _helper() -> Path:
    return _ext_dir() / "_color_swatch_shortcode.py"


# ---------------------------------------------------------------------------
# Extension files
# ---------------------------------------------------------------------------


class TestColorSwatchExtensionFiles:
    """Verify that the color-swatch extension ships the required files."""

    def test_extension_yml_exists(self):
        assert (_ext_dir() / "_extension.yml").exists()

    def test_lua_filter_exists(self):
        assert (_ext_dir() / "color-swatch.lua").exists()

    def test_python_bridge_exists(self):
        assert _helper().exists()

    def test_extension_yml_declares_shortcode(self):
        ext_yml = _ext_dir() / "_extension.yml"
        data = yaml.safe_load(ext_yml.read_text())
        assert "contributes" in data
        assert "shortcodes" in data["contributes"]
        assert "color-swatch.lua" in data["contributes"]["shortcodes"]

    def test_lua_defines_color_swatch_function(self):
        lua_src = (_ext_dir() / "color-swatch.lua").read_text()
        assert '["color-swatch"]' in lua_src
        assert "function(args, kwargs, blocks)" in lua_src


# ---------------------------------------------------------------------------
# Python helper — importable unit tests
# ---------------------------------------------------------------------------


class TestHelperImports:
    """Verify the Python helper can be imported and its core utilities work."""

    @pytest.fixture(autouse=True)
    def _import_helper(self):
        """Import the helper module dynamically."""
        import importlib.util

        spec = importlib.util.spec_from_file_location("_color_swatch_shortcode", _helper())
        self.mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.mod)

    # -- hex_to_rgb --

    def test_hex_to_rgb_six_digit(self):
        assert self.mod.hex_to_rgb("#38bdf8") == (56, 189, 248)

    def test_hex_to_rgb_three_digit(self):
        assert self.mod.hex_to_rgb("#fff") == (255, 255, 255)

    def test_hex_to_rgb_named_color(self):
        assert self.mod.hex_to_rgb("red") == (255, 0, 0)

    def test_hex_to_rgb_invalid_raises(self):
        with pytest.raises(ValueError):
            self.mod.hex_to_rgb("not-a-color")

    # -- rgb_to_hsl --

    def test_rgb_to_hsl_red(self):
        h, s, l = self.mod.rgb_to_hsl(255, 0, 0)
        assert h == 0
        assert s == 100
        assert l == 50

    def test_rgb_to_hsl_white(self):
        h, s, l = self.mod.rgb_to_hsl(255, 255, 255)
        assert s == 0
        assert l == 100

    def test_rgb_to_hsl_black(self):
        h, s, l = self.mod.rgb_to_hsl(0, 0, 0)
        assert s == 0
        assert l == 0

    # -- needs_border_ring --

    def test_ring_very_light(self):
        ring, color = self.mod.needs_border_ring("#fefefe")
        assert ring is True
        assert color.startswith("#")

    def test_ring_very_dark(self):
        ring, color = self.mod.needs_border_ring("#010101")
        assert ring is True
        assert color.startswith("#")

    def test_ring_mid_range(self):
        ring, _ = self.mod.needs_border_ring("#808080")
        assert ring is False

    # -- compute_contrast_info --

    def test_contrast_info_keys(self):
        info = self.mod.compute_contrast_info("#38bdf8")
        assert "lc_vs_white" in info
        assert "lc_vs_black" in info
        assert "ideal_text" in info
        assert "aa_normal" in info
        assert "aa_large" in info

    def test_contrast_white_on_white(self):
        info = self.mod.compute_contrast_info("#ffffff")
        assert info["lc_vs_white"] == 0.0

    def test_contrast_black_has_high_lc(self):
        info = self.mod.compute_contrast_info("#000000")
        assert info["lc_vs_white"] > 90

    # -- GD_PALETTES --

    def test_all_palettes_defined(self):
        names = {"sky", "peach", "prism", "lilac", "slate", "honey", "dusk", "mint"}
        assert names == set(self.mod.GD_PALETTES.keys())

    def test_palette_has_light_and_dark(self):
        for name, preset in self.mod.GD_PALETTES.items():
            assert "light" in preset, f"{name} missing 'light'"
            assert "dark" in preset, f"{name} missing 'dark'"
            assert len(preset["light"]) > 0
            assert len(preset["dark"]) > 0

    def test_palette_colors_have_name_and_hex(self):
        for name, preset in self.mod.GD_PALETTES.items():
            for c in preset["light"] + preset["dark"]:
                assert "name" in c, f"{name}: color missing 'name'"
                assert "hex" in c, f"{name}: color missing 'hex'"

    # -- parse_colors --

    def test_parse_colors_palette(self):
        colors = self.mod.parse_colors("", "sky")
        assert len(colors) == 4
        assert all("hex" in c for c in colors)

    def test_parse_colors_all(self):
        colors = self.mod.parse_colors("", "all")
        assert len(colors) == 8 * 4  # 8 presets × 4 colors each

    def test_parse_colors_unknown_palette(self):
        with pytest.raises(ValueError, match="Unknown palette"):
            self.mod.parse_colors("", "nonexistent")

    def test_parse_colors_yaml_body(self):
        body = '- name: Test\n  hex: "#ff0000"\n'
        colors = self.mod.parse_colors(body, "")
        assert len(colors) == 1
        assert colors[0]["hex"] == "#ff0000"

    def test_parse_colors_palette_plus_body(self):
        body = '- name: Extra\n  hex: "#abcdef"\n'
        colors = self.mod.parse_colors(body, "sky")
        assert len(colors) == 5  # 4 from sky + 1 from body

    def test_parse_colors_empty(self):
        colors = self.mod.parse_colors("", "")
        assert colors == []

    # -- render_circles --

    def test_render_circles_basic(self):
        colors = [
            {"name": "Red", "hex": "#ff0000"},
            {"name": "Blue", "hex": "#0000ff"},
        ]
        html = self.mod.render_circles(colors)
        assert "gd-color-swatch--circles" in html
        assert "#ff0000" in html
        assert "#0000ff" in html
        assert "Red" in html
        assert "Blue" in html
        assert 'role="button"' in html
        assert "data-tooltip-html" in html

    def test_render_circles_no_names(self):
        colors = [{"name": "Red", "hex": "#ff0000"}]
        html = self.mod.render_circles(colors, show_names="false")
        assert "gd-swatch-name" not in html

    def test_render_circles_no_hex(self):
        colors = [{"name": "Red", "hex": "#ff0000"}]
        html = self.mod.render_circles(colors, show_hex="false")
        assert "gd-swatch-hex" not in html

    def test_render_circles_inline_contrast(self):
        colors = [{"name": "Red", "hex": "#ff0000"}]
        html = self.mod.render_circles(colors, show_contrast="inline")
        assert "gd-swatch-contrast" in html

    def test_render_circles_custom_size(self):
        colors = [{"name": "Red", "hex": "#ff0000"}]
        html = self.mod.render_circles(colors, size="80px")
        assert "--gd-cs-size:80px" in html

    def test_render_circles_title(self):
        colors = [{"name": "Red", "hex": "#ff0000"}]
        html = self.mod.render_circles(colors, title="My Palette")
        assert "My Palette" in html
        assert "gd-cs-title" in html

    # -- render_rectangles --

    def test_render_rectangles_basic(self):
        colors = [
            {"name": "Green", "hex": "#22c55e"},
            {"name": "Navy", "hex": "#1e3a5f"},
        ]
        html = self.mod.render_rectangles(colors)
        assert "gd-color-swatch--rectangles" in html
        assert "#22c55e" in html
        assert "Green" in html
        assert "gd-swatch-rect" in html
        assert "gd-swatch-aa-sample" in html

    def test_render_rectangles_no_contrast(self):
        colors = [{"name": "Red", "hex": "#ff0000"}]
        html = self.mod.render_rectangles(colors, show_contrast="false")
        assert "gd-swatch-aa-sample" not in html

    # -- build_tooltip_html --

    def test_tooltip_html_basic(self):
        color = {"name": "Sky Blue", "hex": "#38bdf8"}
        html = self.mod.build_tooltip_html(color, "true")
        assert "Sky Blue" in html
        assert "#38bdf8" in html
        assert "RGB" in html
        assert "HSL" in html
        assert "vs White" in html
        assert "vs Black" in html
        assert "WCAG" in html

    def test_tooltip_html_no_contrast(self):
        color = {"name": "Sky Blue", "hex": "#38bdf8"}
        html = self.mod.build_tooltip_html(color, "false")
        assert "vs White" not in html
        assert "WCAG" not in html


# ---------------------------------------------------------------------------
# CLI integration tests
# ---------------------------------------------------------------------------


class TestColorSwatchCLI:
    """Test the helper as a subprocess (simulates how Lua calls it)."""

    def test_help_succeeds(self):
        result = subprocess.run(
            [sys.executable, str(_helper()), "--help"],
            capture_output=True,
            text=True,
            timeout=10,
        )
        assert result.returncode == 0
        assert "palette" in result.stdout.lower()

    def test_palette_sky_circles(self):
        result = subprocess.run(
            [sys.executable, str(_helper()), "--palette", "sky"],
            capture_output=True,
            text=True,
            timeout=10,
        )
        assert result.returncode == 0
        assert "gd-color-swatch--circles" in result.stdout
        assert "Sky" in result.stdout

    def test_palette_sky_rectangles(self):
        result = subprocess.run(
            [sys.executable, str(_helper()), "--palette", "sky", "--mode", "rectangles"],
            capture_output=True,
            text=True,
            timeout=10,
        )
        assert result.returncode == 0
        assert "gd-color-swatch--rectangles" in result.stdout

    def test_stdin_yaml(self):
        yaml_body = '- name: Test Red\n  hex: "#ff0000"\n'
        result = subprocess.run(
            [sys.executable, str(_helper())],
            input=yaml_body,
            capture_output=True,
            text=True,
            timeout=10,
        )
        assert result.returncode == 0
        assert "Test Red" in result.stdout
        assert "#ff0000" in result.stdout

    def test_unknown_palette_fails(self):
        result = subprocess.run(
            [sys.executable, str(_helper()), "--palette", "nonexistent"],
            capture_output=True,
            text=True,
            timeout=10,
        )
        assert result.returncode != 0

    def test_no_input_fails(self):
        result = subprocess.run(
            [sys.executable, str(_helper())],
            input="",
            capture_output=True,
            text=True,
            timeout=10,
        )
        assert result.returncode != 0

    def test_unsupported_mode_fails(self):
        result = subprocess.run(
            [sys.executable, str(_helper()), "--palette", "sky", "--mode", "gradient"],
            capture_output=True,
            text=True,
            timeout=10,
        )
        assert result.returncode != 0

from __future__ import annotations

from pathlib import Path

import pytest
import yaml


def _ext_dir() -> Path:
    return Path(__file__).parent.parent / "great_docs" / "assets" / "_extensions" / "keys"


class TestKeysExtensionFiles:
    """Verify that the keys extension ships the required files."""

    def test_extension_yml_exists(self):
        assert (_ext_dir() / "_extension.yml").exists()

    def test_lua_filter_exists(self):
        assert (_ext_dir() / "keys.lua").exists()

    def test_extension_yml_declares_shortcode(self):
        ext_yml = _ext_dir() / "_extension.yml"
        data = yaml.safe_load(ext_yml.read_text())
        assert "contributes" in data
        assert "shortcodes" in data["contributes"]
        assert "keys.lua" in data["contributes"]["shortcodes"]

    def test_extension_yml_metadata(self):
        ext_yml = _ext_dir() / "_extension.yml"
        data = yaml.safe_load(ext_yml.read_text())
        assert data["title"] == "Keyboard Keys"
        assert data["author"] == "Great Docs"
        assert "version" in data
        assert "quarto-required" in data

    def test_lua_defines_keys_function(self):
        lua_src = (_ext_dir() / "keys.lua").read_text()
        assert '["keys"]' in lua_src
        assert "function(args, kwargs)" in lua_src


class TestKeysLuaContent:
    """Verify key logic markers in the Lua source."""

    @pytest.fixture()
    def lua_src(self) -> str:
        return (_ext_dir() / "keys.lua").read_text()

    def test_has_mac_key_table(self, lua_src):
        assert "MAC_KEYS" in lua_src

    def test_has_win_key_table(self, lua_src):
        assert "WIN_KEYS" in lua_src

    def test_mac_command_symbol(self, lua_src):
        assert "⌘" in lua_src

    def test_mac_option_symbol(self, lua_src):
        assert "⌥" in lua_src

    def test_mac_shift_symbol(self, lua_src):
        assert "⇧" in lua_src

    def test_mac_control_symbol(self, lua_src):
        assert "⌃" in lua_src

    def test_renders_gd_keys_class(self, lua_src):
        assert '"gd-keys"' in lua_src

    def test_renders_gd_keys_sep_class(self, lua_src):
        assert 'class="gd-keys-sep"' in lua_src

    def test_escape_html_function(self, lua_src):
        assert "escape_html" in lua_src

    def test_handles_shortcut_kwarg(self, lua_src):
        assert 'kwarg_str(kwargs, "shortcut")' in lua_src

    def test_handles_platform_kwarg(self, lua_src):
        assert 'kwarg_str(kwargs, "platform")' in lua_src

    def test_split_shortcut_function(self, lua_src):
        assert "split_shortcut" in lua_src

    def test_translate_key_function(self, lua_src):
        assert "translate_key" in lua_src

    def test_outputs_raw_inline_html(self, lua_src):
        assert 'pandoc.RawInline("html"' in lua_src

    def test_error_comment_on_missing_key(self, lua_src):
        assert "keys shortcode error" in lua_src

    def test_has_tooltips_table(self, lua_src):
        assert "TOOLTIPS" in lua_src

    def test_title_attribute_for_symbols(self, lua_src):
        assert 'title="' in lua_src

    def test_fn_key_detection(self, lua_src):
        assert "is_fn_key" in lua_src

    def test_fn_key_class(self, lua_src):
        assert "gd-keys-fn" in lua_src


class TestKeysScssStyles:
    """Verify keys styles are present in great-docs.scss."""

    @pytest.fixture()
    def scss_src(self) -> str:
        scss_path = Path(__file__).parent.parent / "great_docs" / "assets" / "great-docs.scss"
        return scss_path.read_text()

    def test_gd_keys_class(self, scss_src):
        assert ".gd-keys" in scss_src

    def test_gd_keys_sep_class(self, scss_src):
        assert ".gd-keys-sep" in scss_src

    def test_dark_mode_keys(self, scss_src):
        assert "quarto-dark .gd-keys" in scss_src

    def test_dark_mode_sep(self, scss_src):
        assert "quarto-dark .gd-keys-sep" in scss_src

    def test_3d_border_effect(self, scss_src):
        """The keys should have a subtle 3D border-bottom effect."""
        assert "border-bottom-width: 2px" in scss_src

    def test_monospace_font(self, scss_src):
        """Keyboard keys should use a monospace font."""
        idx = scss_src.index(".gd-keys {")
        block = scss_src[idx : idx + 500]
        assert "monospace" in block

    def test_fn_key_styles(self, scss_src):
        """Function keys should have smallcaps-height styling."""
        assert ".gd-keys-fn" in scss_src


class TestKeysOutputDir:
    """Verify that the extension was also copied to the output great-docs/ dir."""

    def _output_ext_dir(self) -> Path:
        return Path(__file__).parent.parent / "great-docs" / "_extensions" / "keys"

    def test_output_extension_yml_exists(self):
        assert (self._output_ext_dir() / "_extension.yml").exists()

    def test_output_lua_exists(self):
        assert (self._output_ext_dir() / "keys.lua").exists()

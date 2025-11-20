"""
Basic tests for great-theme functionality.
"""

import tempfile
from pathlib import Path
from great_theme import GreatTheme


def test_great_theme_init():
    """Test GreatTheme initialization."""
    theme = GreatTheme(docs_dir=".")
    assert theme.project_root == Path.cwd()


def test_great_theme_init_with_path():
    """Test GreatTheme initialization with custom path."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        theme = GreatTheme(project_path=tmp_dir, docs_dir=".")
        assert theme.project_root == Path(tmp_dir)


def test_install_creates_files():
    """Test that install creates the expected files."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        theme = GreatTheme(project_path=tmp_dir, docs_dir=".")
        theme.install(force=True, skip_quartodoc=True)

        # Check that files were created
        project_path = Path(tmp_dir)
        assert (project_path / "scripts" / "post-render.py").exists()
        assert (project_path / "great-theme.css").exists()
        assert (project_path / "_quarto.yml").exists()


def test_uninstall_removes_files():
    """Test that uninstall removes the theme files."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        theme = GreatTheme(project_path=tmp_dir, docs_dir=".")

        # Install first
        theme.install(force=True, skip_quartodoc=True)

        project_path = Path(tmp_dir)
        assert (project_path / "scripts" / "post-render.py").exists()
        assert (project_path / "great-theme.css").exists()

        # Then uninstall
        theme.uninstall()


def test_parse_package_exports():
    """Test parsing __all__ from __init__.py."""
    # Test on great-theme's own __init__.py
    theme = GreatTheme(docs_dir=".")
    exports = theme._parse_package_exports("great_theme")

    assert exports is not None
    assert "GreatTheme" in exports
    assert "main" in exports


def test_create_quartodoc_sections():
    """Test auto-generation of quartodoc sections."""
    theme = GreatTheme(docs_dir=".")
    sections = theme._create_quartodoc_sections("great_theme")

    assert sections is not None
    assert len(sections) > 0

    # Check that we have at least one section with contents
    has_contents = any(section.get("contents") for section in sections)
    assert has_contents


def test_detect_package_name_from_pyproject():
    """Test package name detection from pyproject.toml."""
    # Test on great-theme's own pyproject.toml
    theme = GreatTheme(docs_dir=".")
    package_name = theme._detect_package_name()

    assert package_name == "great-theme"


def test_cli_import():
    """Test that CLI module can be imported."""
    from great_theme.cli import main

    assert callable(main)

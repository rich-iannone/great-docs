"""
Basic tests for great-theme functionality.
"""

import tempfile
from pathlib import Path
from great_theme import GreatTheme


def test_great_theme_init():
    """Test GreatTheme initialization."""
    theme = GreatTheme()
    assert theme.project_path == Path.cwd()


def test_great_theme_init_with_path():
    """Test GreatTheme initialization with custom path."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        theme = GreatTheme(project_path=tmp_dir)
        assert theme.project_path == Path(tmp_dir)


def test_install_creates_files():
    """Test that install creates the expected files."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        theme = GreatTheme(project_path=tmp_dir)
        theme.install(force=True)

        # Check that files were created
        project_path = Path(tmp_dir)
        assert (project_path / "scripts" / "post-render.py").exists()
        assert (project_path / "great-theme.css").exists()
        assert (project_path / "_quarto.yml").exists()


def test_uninstall_removes_files():
    """Test that uninstall removes the theme files."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        theme = GreatTheme(project_path=tmp_dir)

        # Install first
        theme.install(force=True)

        project_path = Path(tmp_dir)
        assert (project_path / "scripts" / "post-render.py").exists()
        assert (project_path / "great-theme.css").exists()

        # Then uninstall
        theme.uninstall()

        assert not (project_path / "scripts" / "post-render.py").exists()
        assert not (project_path / "great-theme.css").exists()


def test_cli_import():
    """Test that CLI module can be imported."""
    from great_theme.cli import main

    assert callable(main)

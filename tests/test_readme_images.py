"""Tests for README image copying functionality."""

import tempfile
from pathlib import Path

import pytest

from great_docs import GreatDocs


def test_copy_readme_images_basic():
    """Test that images referenced in README are copied correctly."""
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir = Path(tmpdir)

        # Create project structure
        images_dir = tmpdir / "images"
        images_dir.mkdir()

        # Create a test image
        test_img = images_dir / "screenshot.png"
        test_img.write_bytes(b"fake png data")

        # Create README.md with image references
        readme = tmpdir / "README.md"
        readme.write_text("""
# My Project

![Screenshot](images/screenshot.png)

External images should be skipped:
![External](https://example.com/img.png)

Assets should be skipped (handled elsewhere):
![Logo](assets/logo.svg)
""")

        # Create great-docs directory
        gd_dir = tmpdir / "great-docs"
        gd_dir.mkdir()

        # Initialize GreatDocs and test the method
        gd = GreatDocs(str(tmpdir))

        # Call the method directly
        copied = gd._copy_readme_images(readme)

        # Verify
        assert copied == 1, f"Expected 1 image copied, got {copied}"

        dest_img = gd_dir / "images" / "screenshot.png"
        assert dest_img.exists(), f"Image not copied to {dest_img}"
        assert dest_img.read_bytes() == b"fake png data", "Image content mismatch"


def test_copy_readme_images_html_tags():
    """Test that HTML img tags are also detected."""
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir = Path(tmpdir)

        # Create project structure
        docs_dir = tmpdir / "docs"
        docs_dir.mkdir()
        test_img = docs_dir / "diagram.svg"
        test_img.write_bytes(b"<svg></svg>")

        # Create README.md with HTML image
        readme = tmpdir / "README.md"
        readme.write_text("""
# My Project

<img src="docs/diagram.svg" alt="Architecture">
""")

        # Create great-docs directory
        gd_dir = tmpdir / "great-docs"
        gd_dir.mkdir()

        gd = GreatDocs(str(tmpdir))
        copied = gd._copy_readme_images(readme)

        assert copied == 1
        assert (gd_dir / "docs" / "diagram.svg").exists()


def test_copy_readme_images_skips_urls():
    """Test that external URLs are not copied."""
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir = Path(tmpdir)

        readme = tmpdir / "README.md"
        readme.write_text("""
# My Project

![External 1](https://example.com/img.png)
![External 2](http://example.com/img.png)
![External 3](//example.com/img.png)
![Data URI](data:image/png;base64,abc123)
""")

        gd_dir = tmpdir / "great-docs"
        gd_dir.mkdir()

        gd = GreatDocs(str(tmpdir))
        copied = gd._copy_readme_images(readme)

        assert copied == 0


def test_copy_readme_images_skips_assets():
    """Test that assets/ paths are skipped (handled by _copy_assets)."""
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir = Path(tmpdir)

        # Create assets directory with an image
        assets_dir = tmpdir / "assets"
        assets_dir.mkdir()
        (assets_dir / "logo.svg").write_bytes(b"<svg></svg>")

        readme = tmpdir / "README.md"
        readme.write_text("""
# My Project

![Logo](assets/logo.svg)
""")

        gd_dir = tmpdir / "great-docs"
        gd_dir.mkdir()

        gd = GreatDocs(str(tmpdir))
        copied = gd._copy_readme_images(readme)

        # Should be 0 because assets/ is handled separately
        assert copied == 0


def test_copy_readme_images_none_source():
    """Test that None source file returns 0."""
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir = Path(tmpdir)

        gd_dir = tmpdir / "great-docs"
        gd_dir.mkdir()

        gd = GreatDocs(str(tmpdir))
        copied = gd._copy_readme_images(None)

        assert copied == 0


def test_copy_readme_images_missing_file():
    """Test that references to missing files are skipped."""
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir = Path(tmpdir)

        readme = tmpdir / "README.md"
        readme.write_text("""
# My Project

![Missing](images/nonexistent.png)
""")

        gd_dir = tmpdir / "great-docs"
        gd_dir.mkdir()

        gd = GreatDocs(str(tmpdir))
        copied = gd._copy_readme_images(readme)

        # File doesn't exist, so nothing is copied
        assert copied == 0

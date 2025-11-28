"""
Basic tests for great-docs functionality.
"""

import tempfile
from pathlib import Path
from great_docs import GreatDocs


def test_great_docs_init():
    """Test GreatDocs initialization."""
    docs = GreatDocs(docs_dir=".")
    assert docs.project_root == Path.cwd()


def test_great_docs_init_with_path():
    """Test GreatDocs initialization with custom path."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        docs = GreatDocs(project_path=tmp_dir, docs_dir=".")
        assert docs.project_root == Path(tmp_dir)


def test_install_creates_files():
    """Test that install creates the expected files."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        docs = GreatDocs(project_path=tmp_dir, docs_dir=".")
        docs.install(force=True, skip_quartodoc=True)

        # Check that files were created
        project_path = Path(tmp_dir)
        assert (project_path / "scripts" / "post-render.py").exists()
        assert (project_path / "great-docs.css").exists()
        assert (project_path / "_quarto.yml").exists()


def test_uninstall_removes_files():
    """Test that uninstall removes the docs files."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        docs = GreatDocs(project_path=tmp_dir, docs_dir=".")

        # Install first
        docs.install(force=True, skip_quartodoc=True)

        project_path = Path(tmp_dir)
        assert (project_path / "scripts" / "post-render.py").exists()
        assert (project_path / "great-docs.css").exists()

        # Then uninstall
        docs.uninstall()


def test_parse_package_exports():
    """Test parsing __all__ from __init__.py."""
    # Test on great-docs's own __init__.py
    docs = GreatDocs(docs_dir=".")
    exports = docs._parse_package_exports("great_docs")

    assert exports is not None
    assert "GreatDocs" in exports
    assert "main" in exports


def test_create_quartodoc_sections():
    """Test auto-generation of quartodoc sections."""
    docs = GreatDocs(docs_dir=".")
    sections = docs._create_quartodoc_sections("great_docs")

    assert sections is not None
    assert len(sections) > 0

    # Check that we have at least one section with contents
    has_contents = any(section.get("contents") for section in sections)
    assert has_contents


def test_detect_package_name_from_pyproject():
    """Test package name detection from pyproject.toml."""
    # Test on great-docs's own pyproject.toml
    docs = GreatDocs(docs_dir=".")
    package_name = docs._detect_package_name()

    assert package_name == "great-docs"


def test_find_package_init():
    """Test finding __init__.py in standard location."""
    docs = GreatDocs(docs_dir=".")
    init_file = docs._find_package_init("great_docs")

    assert init_file is not None
    assert init_file.exists()
    assert init_file.name == "__init__.py"


def test_find_package_init_with_nested_structure():
    """Test finding __init__.py in nested directories like python/."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        # Create a package structure in python/ subdirectory
        python_dir = Path(tmp_dir) / "python"
        python_dir.mkdir()
        package_dir = python_dir / "mypackage"
        package_dir.mkdir()

        # Create __init__.py with __version__ and __all__
        init_file = package_dir / "__init__.py"
        init_file.write_text('__version__ = "1.0.0"\n__all__ = ["MyClass"]')

        docs = GreatDocs(project_path=tmp_dir, docs_dir=".")
        found_init = docs._find_package_init("mypackage")

        assert found_init is not None
        assert found_init == init_file


def test_cli_import():
    """Test that CLI module can be imported."""
    from great_docs.cli import main

    assert callable(main)


def test_method_section_generation():
    """Test that classes with >5 methods get separate method sections."""
    import sys

    with tempfile.TemporaryDirectory() as tmp_dir:
        # Create a test package with a class that has many methods
        package_dir = Path(tmp_dir) / "testpkg"
        package_dir.mkdir()

        # Create __init__.py with __all__ and a class with many methods
        init_content = '''
"""Test package."""
__version__ = "1.0.0"
__all__ = ["BigClass", "SmallClass", "some_function"]

class BigClass:
    """A class with many methods."""
    def method1(self): pass
    def method2(self): pass
    def method3(self): pass
    def method4(self): pass
    def method5(self): pass
    def method6(self): pass
    def method7(self): pass

class SmallClass:
    """A class with few methods."""
    def method1(self): pass
    def method2(self): pass

def some_function():
    """A function."""
    pass
'''
        (package_dir / "__init__.py").write_text(init_content)

        # Add temp dir to sys.path so griffe can find the package
        sys.path.insert(0, tmp_dir)
        try:
            docs = GreatDocs(project_path=tmp_dir, docs_dir=".")
            sections = docs._create_quartodoc_sections("testpkg")

            assert sections is not None

            # Check that we have a Classes section
            class_section = next((s for s in sections if s["title"] == "Classes"), None)
            assert class_section is not None

            # BigClass should have members: [] since it has >5 methods
            big_class_entry = next(
                (
                    c
                    for c in class_section["contents"]
                    if isinstance(c, dict) and c.get("name") == "BigClass"
                ),
                None,
            )
            assert big_class_entry is not None
            assert big_class_entry == {"name": "BigClass", "members": []}

            # SmallClass should be a plain string (inline documentation)
            assert "SmallClass" in class_section["contents"]

            # Check that we have a separate method section for BigClass
            method_section = next((s for s in sections if s["title"] == "BigClass Methods"), None)
            assert method_section is not None
            assert len(method_section["contents"]) == 7
            assert "BigClass.method1" in method_section["contents"]
            assert "BigClass.method7" in method_section["contents"]

            # SmallClass should NOT have a separate method section
            small_method_section = next(
                (s for s in sections if s["title"] == "SmallClass Methods"), None
            )
            assert small_method_section is None

            # Check that functions section exists
            func_section = next((s for s in sections if s["title"] == "Functions"), None)
            assert func_section is not None
            assert "some_function" in func_section["contents"]
        finally:
            # Clean up sys.path
            sys.path.remove(tmp_dir)


def test_gt_exclude():
    """Test that __gt_exclude__ filters out non-documentable items."""
    import sys

    with tempfile.TemporaryDirectory() as tmp_dir:
        # Create a test package with __gt_exclude__
        package_dir = Path(tmp_dir) / "testpkg_exclude"
        package_dir.mkdir()

        # Create __init__.py with __all__ and __gt_exclude__
        init_content = '''
"""Test package with exclusions."""
__version__ = "1.0.0"
__all__ = ["Graph", "Node", "Edge", "some_function"]

# Exclude Rust types that can't be documented
__gt_exclude__ = ["Node", "Edge"]

class Graph:
    """A graph class."""
    def add_node(self): pass
    def add_edge(self): pass

class Node:
    """A Rust type (would fail in quartodoc)."""
    pass

class Edge:
    """Another Rust type (would fail in quartodoc)."""
    pass

def some_function():
    """A function."""
    pass
'''
        (package_dir / "__init__.py").write_text(init_content)

        docs = GreatDocs(project_path=tmp_dir, docs_dir=".")
        exports = docs._parse_package_exports("testpkg_exclude")

        # Should have filtered out Node and Edge
        assert exports is not None
        assert "Graph" in exports
        assert "some_function" in exports
        assert "Node" not in exports
        assert "Edge" not in exports
        assert len(exports) == 2


def test_setup_github_pages_command():
    """Test the setup-github-pages CLI command."""
    from click.testing import CliRunner
    from great_docs.cli import setup_github_pages

    runner = CliRunner()

    with tempfile.TemporaryDirectory() as tmp_dir:
        # Run the command
        result = runner.invoke(setup_github_pages, ["--project-path", tmp_dir, "--force"])

        # Check it succeeded
        assert result.exit_code == 0
        assert "✅ Created GitHub Actions workflow" in result.output

        # Check the file was created
        workflow_file = Path(tmp_dir) / ".github" / "workflows" / "docs.yml"
        assert workflow_file.exists()

        # Check the content is valid YAML and contains expected keys
        import yaml

        with open(workflow_file) as f:
            workflow = yaml.safe_load(f)

        assert "name" in workflow
        assert workflow["name"] == "CI Docs"
        assert "jobs" in workflow
        assert "build-docs" in workflow["jobs"]
        assert "publish-docs" in workflow["jobs"]
        assert "preview-docs" in workflow["jobs"]


def test_setup_github_pages_custom_options():
    """Test setup-github-pages with custom options."""
    from click.testing import CliRunner
    from great_docs.cli import setup_github_pages

    runner = CliRunner()

    with tempfile.TemporaryDirectory() as tmp_dir:
        result = runner.invoke(
            setup_github_pages,
            [
                "--project-path",
                tmp_dir,
                "--docs-dir",
                "site",
                "--main-branch",
                "develop",
                "--python-version",
                "3.12",
                "--force",
            ],
        )

        assert result.exit_code == 0

        workflow_file = Path(tmp_dir) / ".github" / "workflows" / "docs.yml"
        content = workflow_file.read_text()

        # Check customizations were applied
        assert "site" in content
        assert "develop" in content
        assert "3.12" in content


def test_setup_github_pages_overwrite_protection():
    """Test that setup-github-pages protects against overwrites."""
    from click.testing import CliRunner
    from great_docs.cli import setup_github_pages

    runner = CliRunner()

    with tempfile.TemporaryDirectory() as tmp_dir:
        # Create the workflow first
        runner.invoke(setup_github_pages, ["--project-path", tmp_dir, "--force"])

        # Try again without force
        result = runner.invoke(setup_github_pages, ["--project-path", tmp_dir], input="n\n")

        assert result.exit_code == 1
        assert "Aborted" in result.output

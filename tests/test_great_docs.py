import tempfile
from pathlib import Path
from great_docs import GreatDocs, Config, load_config, create_default_config


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


def test_generate_llms_txt():
    """Test generation of llms.txt file."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        docs = GreatDocs(project_path=tmp_dir, docs_dir=".")

        # Create a pyproject.toml with package info
        pyproject = Path(tmp_dir) / "pyproject.toml"
        pyproject.write_text("""
[project]
name = "test-package"
description = "A test package"
""")

        # Create a minimal _quarto.yml with quartodoc config
        quarto_yml = Path(tmp_dir) / "_quarto.yml"
        quarto_yml.write_text("""
quartodoc:
  package: test_package
  sections:
    - title: Main
      desc: Main functions
      contents:
        - foo
        - bar
    - title: Classes
      contents:
        - MyClass
""")

        # Generate llms.txt
        docs._generate_llms_txt()

        # Check the file was created
        llms_txt = Path(tmp_dir) / "llms.txt"
        assert llms_txt.exists()

        # Check content structure
        content = llms_txt.read_text()
        assert "# test_package" in content
        assert "> A test package" in content
        assert "## Docs" in content
        assert "### API Reference" in content
        assert "#### Main" in content
        assert "> Main functions" in content
        assert "- [foo](reference/foo.html)" in content
        assert "- [bar](reference/bar.html)" in content
        assert "#### Classes" in content
        assert "- [MyClass](reference/MyClass.html)" in content


def test_generate_llms_txt_with_site_url():
    """Test llms.txt generation with site URL."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        docs = GreatDocs(project_path=tmp_dir, docs_dir=".")

        # Create a minimal _quarto.yml with quartodoc config and site URL
        quarto_yml = Path(tmp_dir) / "_quarto.yml"
        quarto_yml.write_text("""
website:
  site-url: https://example.com/docs
quartodoc:
  package: test_package
  sections:
    - title: Main
      contents:
        - foo
""")

        # Generate llms.txt
        docs._generate_llms_txt()

        # Check the file was created with absolute URLs
        llms_txt = Path(tmp_dir) / "llms.txt"
        content = llms_txt.read_text()
        assert "https://example.com/docs/reference/foo.html" in content


def test_get_github_repo_info():
    """Test GitHub repository info extraction from pyproject.toml."""
    # Test on great-docs's own pyproject.toml
    docs = GreatDocs(docs_dir=".")
    owner, repo, base_url = docs._get_github_repo_info()

    assert owner == "rich-iannone"
    assert repo == "great-docs"
    assert base_url == "https://github.com/rich-iannone/great-docs"


def test_get_github_repo_info_no_repo():
    """Test GitHub repo info when no repository URL exists."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        # Create a minimal pyproject.toml without repository URL
        pyproject = Path(tmp_dir) / "pyproject.toml"
        pyproject.write_text("""
[project]
name = "test-package"
version = "0.1.0"
""")

        docs = GreatDocs(project_path=tmp_dir, docs_dir=".")
        owner, repo, base_url = docs._get_github_repo_info()

        assert owner is None
        assert repo is None
        assert base_url is None


def test_get_source_location():
    """Test source location detection for classes and methods."""
    docs = GreatDocs(docs_dir=".")
    source_loc = docs._get_source_location("great_docs", "GreatDocs")

    assert source_loc is not None
    assert "file" in source_loc
    assert "start_line" in source_loc
    assert "end_line" in source_loc
    assert source_loc["start_line"] > 0
    assert source_loc["end_line"] >= source_loc["start_line"]
    assert "core.py" in source_loc["file"]


def test_get_source_location_method():
    """Test source location detection for methods."""
    docs = GreatDocs(docs_dir=".")
    source_loc = docs._get_source_location("great_docs", "GreatDocs.install")

    assert source_loc is not None
    assert "file" in source_loc
    assert "start_line" in source_loc
    assert source_loc["start_line"] > 0


def test_get_source_location_not_found():
    """Test source location returns None for non-existent items."""
    docs = GreatDocs(docs_dir=".")
    source_loc = docs._get_source_location("great_docs", "NonExistentClass")

    assert source_loc is None


def test_build_github_source_url():
    """Test GitHub source URL construction."""
    docs = GreatDocs(docs_dir=".")

    source_loc = {
        "file": "/path/to/great_docs/core.py",
        "start_line": 42,
        "end_line": 58,
    }

    url = docs._build_github_source_url(source_loc, branch="main")

    assert url is not None
    assert "https://github.com/rich-iannone/great-docs" in url
    assert "blob/main" in url
    assert "#L42-L58" in url


def test_build_github_source_url_single_line():
    """Test GitHub source URL with single line."""
    docs = GreatDocs(docs_dir=".")

    source_loc = {
        "file": "/path/to/great_docs/core.py",
        "start_line": 42,
        "end_line": 42,
    }

    url = docs._build_github_source_url(source_loc, branch="main")

    assert url is not None
    assert "#L42" in url
    # Should not have the range format
    assert "#L42-L42" not in url


def test_source_link_config_defaults():
    """Test that source link configuration has proper defaults."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        # Create pyproject.toml without source config
        pyproject = Path(tmp_dir) / "pyproject.toml"
        pyproject.write_text("""
[project]
name = "test-package"
version = "0.1.0"
""")

        docs = GreatDocs(project_path=tmp_dir, docs_dir=".")
        metadata = docs._get_package_metadata()

        # Defaults should be: enabled=True, branch=None, path=None, placement="usage"
        assert metadata.get("source_link_enabled", True) is True
        assert metadata.get("source_link_branch") is None
        assert metadata.get("source_link_path") is None
        assert metadata.get("source_link_placement", "usage") == "usage"


def test_source_link_config_custom():
    """Test custom source link configuration."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        # Create pyproject.toml for project metadata
        pyproject = Path(tmp_dir) / "pyproject.toml"
        pyproject.write_text("""
[project]
name = "test-package"
version = "0.1.0"
""")

        # Create great-docs.yml with custom source config
        config_file = Path(tmp_dir) / "great-docs.yml"
        config_file.write_text("""
source:
  enabled: false
  branch: develop
  path: src/mypackage
  placement: title
""")

        docs = GreatDocs(project_path=tmp_dir, docs_dir=".")
        metadata = docs._get_package_metadata()

        assert metadata.get("source_link_enabled") is False
        assert metadata.get("source_link_branch") == "develop"
        assert metadata.get("source_link_path") == "src/mypackage"
        assert metadata.get("source_link_placement") == "title"


# ============================================================================
# Link Checker Tests
# ============================================================================


def test_check_links_extracts_urls():
    """Test that check_links extracts URLs from files."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        # Create a docs directory with a file containing URLs
        docs_dir = Path(tmp_dir) / "docs"
        docs_dir.mkdir()

        test_md = docs_dir / "test.md"
        test_md.write_text("""
# Test Document

Check out https://httpbin.org/status/200 for more info.
Also see https://httpbin.org/status/404 for errors.
        """)

        # Create _quarto.yml so it's detected
        quarto_yml = docs_dir / "_quarto.yml"
        quarto_yml.write_text("project:\n  type: website\n")

        docs = GreatDocs(project_path=tmp_dir, docs_dir="docs")
        results = docs.check_links(
            include_source=False,
            include_docs=True,
            timeout=5.0,
            verbose=False,
        )

        assert results["total"] >= 2
        assert "by_file" in results
        assert len(results["by_file"]) > 0


def test_check_links_ignore_patterns():
    """Test that ignore patterns work correctly."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        docs_dir = Path(tmp_dir) / "docs"
        docs_dir.mkdir()

        test_md = docs_dir / "test.md"
        test_md.write_text("""
# Test

https://localhost:8000/api
https://127.0.0.1:3000/test
https://example.com/page
        """)

        quarto_yml = docs_dir / "_quarto.yml"
        quarto_yml.write_text("project:\n  type: website\n")

        docs = GreatDocs(project_path=tmp_dir, docs_dir="docs")
        results = docs.check_links(
            include_source=False,
            include_docs=True,
            ignore_patterns=["localhost", "127.0.0.1", "example.com"],
            verbose=False,
        )

        # All URLs should be skipped
        assert len(results["skipped"]) == 3
        assert len(results["ok"]) == 0
        assert len(results["broken"]) == 0


def test_check_links_url_cleaning():
    """Test that URLs are properly cleaned of trailing punctuation."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        docs_dir = Path(tmp_dir) / "docs"
        docs_dir.mkdir()

        test_md = docs_dir / "test.md"
        test_md.write_text("""
See https://example.com/page.
Check https://example.com/other,
Visit https://example.com/test!
        """)

        quarto_yml = docs_dir / "_quarto.yml"
        quarto_yml.write_text("project:\n  type: website\n")

        docs = GreatDocs(project_path=tmp_dir, docs_dir="docs")
        results = docs.check_links(
            include_source=False,
            include_docs=True,
            ignore_patterns=["example.com"],
            verbose=False,
        )

        # Check that URLs don't have trailing punctuation
        for url in results["skipped"]:
            assert not url.endswith(".")
            assert not url.endswith(",")
            assert not url.endswith("!")


def test_check_links_returns_correct_structure():
    """Test that check_links returns the expected result structure."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        docs_dir = Path(tmp_dir) / "docs"
        docs_dir.mkdir()

        test_md = docs_dir / "test.md"
        test_md.write_text("No URLs here")

        quarto_yml = docs_dir / "_quarto.yml"
        quarto_yml.write_text("project:\n  type: website\n")

        docs = GreatDocs(project_path=tmp_dir, docs_dir="docs")
        results = docs.check_links(include_source=False, include_docs=True)

        # Check result structure
        assert "total" in results
        assert "ok" in results
        assert "redirects" in results
        assert "broken" in results
        assert "skipped" in results
        assert "by_file" in results

        assert isinstance(results["ok"], list)
        assert isinstance(results["redirects"], list)
        assert isinstance(results["broken"], list)
        assert isinstance(results["skipped"], list)
        assert isinstance(results["by_file"], dict)


# ============================================================================
# Config Module Tests
# ============================================================================


def test_config_defaults():
    """Test that Config provides sensible defaults when no file exists."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        config = Config(Path(tmp_dir))

        # Check defaults
        assert config.discovery_method == "dir"
        assert config.include == []
        assert config.exclude == []
        assert config.github_style == "widget"
        assert config.source_enabled is True
        assert config.source_branch is None
        assert config.source_path is None
        assert config.source_placement == "usage"
        assert config.sidebar_filter_enabled is True
        assert config.sidebar_filter_min_items == 20
        assert config.cli_enabled is False
        assert config.cli_module is None
        assert config.cli_name is None
        assert config.large_class_method_threshold == 5
        assert config.dark_mode_toggle is True
        assert config.reference == []
        assert config.authors == []


def test_config_load_yaml():
    """Test loading configuration from great-docs.yml."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        config_file = Path(tmp_dir) / "great-docs.yml"
        config_file.write_text("""
include:
  - main
  - cli
exclude:
  - InternalClass

github_style: icon

sidebar_filter:
  enabled: false
  min_items: 10

cli:
  enabled: true
  module: mypackage.cli
  name: app

large_class_method_threshold: 8
dark_mode_toggle: false

authors:
  - name: Test Author
    github: testuser
""")

        config = Config(Path(tmp_dir))

        assert config.include == ["main", "cli"]
        assert config.exclude == ["InternalClass"]
        assert config.github_style == "icon"
        assert config.sidebar_filter_enabled is False
        assert config.sidebar_filter_min_items == 10
        assert config.cli_enabled is True
        assert config.cli_module == "mypackage.cli"
        assert config.cli_name == "app"
        assert config.large_class_method_threshold == 8
        assert config.dark_mode_toggle is False
        assert len(config.authors) == 1
        assert config.authors[0]["name"] == "Test Author"


def test_config_partial_yaml():
    """Test that partial config merges with defaults."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        config_file = Path(tmp_dir) / "great-docs.yml"
        config_file.write_text("""
cli:
  enabled: true
""")

        config = Config(Path(tmp_dir))

        # CLI is set
        assert config.cli_enabled is True
        # But other CLI fields still have defaults
        assert config.cli_module is None
        assert config.cli_name is None
        # And other config has defaults
        assert config.github_style == "widget"
        assert config.dark_mode_toggle is True


def test_config_exists():
    """Test the exists() method."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        config = Config(Path(tmp_dir))
        assert config.exists() is False

        config_file = Path(tmp_dir) / "great-docs.yml"
        config_file.write_text("cli:\n  enabled: true\n")

        config2 = Config(Path(tmp_dir))
        assert config2.exists() is True


def test_config_to_dict():
    """Test converting config to dictionary."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        config_file = Path(tmp_dir) / "great-docs.yml"
        config_file.write_text("""
github_style: icon
""")

        config = Config(Path(tmp_dir))
        config_dict = config.to_dict()

        assert isinstance(config_dict, dict)
        assert config_dict["github_style"] == "icon"
        assert "cli" in config_dict
        assert "source" in config_dict


def test_config_get_nested():
    """Test getting nested config values with dot notation."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        config_file = Path(tmp_dir) / "great-docs.yml"
        config_file.write_text("""
source:
  enabled: false
  branch: develop
""")

        config = Config(Path(tmp_dir))

        assert config.get("source.enabled") is False
        assert config.get("source.branch") == "develop"
        assert config.get("source.nonexistent", "default") == "default"


def test_load_config_function():
    """Test the load_config helper function."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        config = load_config(tmp_dir)
        assert isinstance(config, Config)


def test_create_default_config():
    """Test creating default configuration content."""
    content = create_default_config()

    assert isinstance(content, str)
    assert "Great Docs Configuration" in content
    assert "discovery_method" in content
    assert "sidebar_filter" in content
    assert "cli:" in content
    assert "authors:" in content

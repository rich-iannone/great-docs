import os
import shutil
from pathlib import Path
from typing import Optional

import yaml

try:
    from importlib import resources
except ImportError:
    # Fallback for Python < 3.9
    import importlib_resources as resources  # type: ignore[import-not-found]


class GreatTheme:
    """
    GreatTheme class for applying enhanced theming to quartodoc sites.

    This class provides methods to install theme assets and configure
    Quarto projects with the great-theme styling and functionality.
    """

    def __init__(self, project_path: Optional[str] = None, docs_dir: Optional[str] = None):
        """
        Initialize GreatTheme instance.

        Parameters
        ----------
        project_path
            Path to the Quarto project root directory. Defaults to current directory.
        docs_dir
            Path to the documentation directory relative to project_path.
            If not provided, will be auto-detected or user will be prompted.
        """
        self.project_root = Path(project_path or os.getcwd())
        self.docs_dir = self._find_or_create_docs_dir(docs_dir)
        self.project_path = self.project_root / self.docs_dir
        try:
            # Python 3.9+
            self.package_path = Path(resources.files("great_theme"))
        except AttributeError:
            # Fallback for older Python versions
            import importlib_resources  # type: ignore[import-not-found]

            self.package_path = Path(importlib_resources.files("great_theme"))
        self.assets_path = self.package_path / "assets"

    def _find_or_create_docs_dir(self, docs_dir: Optional[str] = None) -> Path:
        """
        Find or create the documentation directory.

        Parameters
        ----------
        docs_dir
            User-specified docs directory path.

        Returns
        -------
        Path
            Path to the docs directory relative to project root.
        """
        if docs_dir:
            return Path(docs_dir)

        # Common documentation directory names
        common_docs_dirs = ["docs", "documentation", "site", "docsrc", "doc"]

        # First, look for existing _quarto.yml in common locations
        for dir_name in common_docs_dirs:
            potential_dir = self.project_root / dir_name
            if (potential_dir / "_quarto.yml").exists():
                print(f"Found existing Quarto project in '{dir_name}/' directory")
                return Path(dir_name)

        # Check if _quarto.yml exists in project root
        if (self.project_root / "_quarto.yml").exists():
            print("Found _quarto.yml in project root")
            return Path(".")

        # Look for any existing common docs directories (even without _quarto.yml)
        for dir_name in common_docs_dirs:
            potential_dir = self.project_root / dir_name
            if potential_dir.exists() and potential_dir.is_dir():
                response = input(
                    f"Found existing '{dir_name}/' directory. Install great-theme here? [Y/n]: "
                )
                if response.lower() != "n":
                    return Path(dir_name)

        # No existing docs directory found - ask user
        print("\nNo documentation directory detected.")
        print("Where would you like to install great-theme?")
        print("  1. docs/ (recommended for most projects)")
        print("  2. Current directory (project root)")
        print("  3. Custom directory")

        choice = input("Enter choice [1]: ").strip() or "1"

        if choice == "1":
            return Path("docs")
        elif choice == "2":
            return Path(".")
        elif choice == "3":
            custom_dir = input("Enter directory path: ").strip()
            return Path(custom_dir) if custom_dir else Path("docs")
        else:
            print("Invalid choice, using 'docs/' as default")
            return Path("docs")

    def install(self, force: bool = False, skip_quartodoc: bool = False) -> None:
        """
        Install great-theme assets and configuration to the project.

        This method copies the necessary CSS files and post-render script to your Quarto project
        directory, and automatically updates your `_quarto.yml` configuration file to use the
        great-theme styling.

        Parameters
        ----------
        force
            If True, overwrite existing files without prompting. Default is False.
        skip_quartodoc
            If True, skip adding quartodoc configuration. Useful for testing or when
            quartodoc is not needed. Default is False.

        Examples
        --------
        Install the theme in the current directory:

        ```python
        from great_theme import GreatTheme

        theme = GreatTheme()
        theme.install()
        ```

        Install the theme in a specific project directory, overwriting existing files:

        ```python
        theme = GreatTheme("/path/to/my/project")
        theme.install(force=True)
        ```

        See Also
        --------
        uninstall : Remove great-theme assets and configuration
        """
        print("Installing great-theme to your quartodoc project...")

        # Create docs directory if it doesn't exist
        self.project_path.mkdir(parents=True, exist_ok=True)
        print(f"Using directory: {self.project_path.relative_to(self.project_root)}")

        # Create necessary directories
        scripts_dir = self.project_path / "scripts"
        scripts_dir.mkdir(exist_ok=True)

        # Copy post-render script
        post_render_src = self.assets_path / "post-render.py"
        post_render_dst = scripts_dir / "post-render.py"

        if post_render_dst.exists() and not force:
            response = input(f"{post_render_dst} already exists. Overwrite? [y/N]: ")
            if response.lower() != "y":
                print("Skipping post-render.py")
            else:
                shutil.copy2(post_render_src, post_render_dst)
                print(f"Copied {post_render_dst}")
        else:
            shutil.copy2(post_render_src, post_render_dst)
            print(f"Copied {post_render_dst}")

        # Copy CSS file
        css_src = self.assets_path / "styles.css"
        css_dst = self.project_path / "great-theme.css"

        if css_dst.exists() and not force:
            response = input(f"{css_dst} already exists. Overwrite? [y/N]: ")
            if response.lower() != "y":
                print("Skipping great-theme.css")
            else:
                shutil.copy2(css_src, css_dst)
                print(f"Copied {css_dst}")
        else:
            shutil.copy2(css_src, css_dst)
            print(f"Copied {css_dst}")

        # Update _quarto.yml configuration
        self._update_quarto_config()

        # Create index.qmd from README.md if it doesn't exist
        self._create_index_from_readme()

        # Add quartodoc configuration if not present
        if not skip_quartodoc:
            self._add_quartodoc_config()

        print("\nGreat-theme installation complete!")
        if not skip_quartodoc:
            print("\nNext steps:")
            print("1. Review the generated quartodoc configuration in _quarto.yml")
            print("2. Run `quartodoc build` to generate API reference pages")
            print("3. Run `quarto render` to build your site with the new theme")
        else:
            print("\nNext steps:")
            print("1. Run `quarto render` to build your site with the new theme")

    def _detect_package_name(self) -> Optional[str]:
        """
        Detect the Python package name from project structure.

        Returns
        -------
        Optional[str]
            The detected package name, or None if not found.
        """
        # Look for pyproject.toml
        pyproject_path = self.project_root / "pyproject.toml"
        if pyproject_path.exists():
            try:
                import tomli  # type: ignore[import-not-found]
            except ImportError:
                try:
                    import tomllib as tomli  # Python 3.11+
                except ImportError:
                    # Fallback: try to parse manually
                    with open(pyproject_path, "r") as f:
                        for line in f:
                            if line.strip().startswith("name"):
                                # Extract name from: name = "package-name"
                                parts = line.split("=", 1)
                                if len(parts) == 2:
                                    name = parts[1].strip().strip('"').strip("'")
                                    return name
                    return None

            with open(pyproject_path, "rb") as f:
                try:
                    data = tomli.load(f)
                    return data.get("project", {}).get("name")
                except Exception:
                    return None

        # Look for setup.py
        setup_py = self.project_root / "setup.py"
        if setup_py.exists():
            with open(setup_py, "r") as f:
                content = f.read()
                # Simple regex to find name="..." in setup()
                import re

                match = re.search(r'name\s*=\s*["\']([^"\']+)["\']', content)
                if match:
                    return match.group(1)

        # Look for a single Python package directory
        potential_packages = [
            d
            for d in self.project_root.iterdir()
            if d.is_dir() and (d / "__init__.py").exists() and not d.name.startswith(".")
        ]
        if len(potential_packages) == 1:
            return potential_packages[0].name

        return None

    def _parse_package_exports(self, package_name: str) -> Optional[list]:
        """
        Parse __all__ from package's __init__.py to get public API.

        Parameters
        ----------
        package_name
            The name of the package to parse.

        Returns
        -------
        Optional[list]
            List of public names from __all__, or None if not found.
        """
        # Look for package directory
        package_dir = self.project_root / package_name
        if not package_dir.exists() or not package_dir.is_dir():
            # Try with underscores if package name has dashes
            package_dir = self.project_root / package_name.replace("-", "_")
            if not package_dir.exists() or not package_dir.is_dir():
                return None

        init_file = package_dir / "__init__.py"
        if not init_file.exists():
            return None

        try:
            with open(init_file, "r", encoding="utf-8") as f:
                content = f.read()

            # Try to extract __all__ using AST (safer than eval)
            import ast

            tree = ast.parse(content)

            for node in ast.walk(tree):
                if isinstance(node, ast.Assign):
                    for target in node.targets:
                        if isinstance(target, ast.Name) and target.id == "__all__":
                            # Found __all__ assignment
                            if isinstance(node.value, ast.List):
                                result = []
                                for elt in node.value.elts:
                                    if isinstance(elt, ast.Constant) and isinstance(elt.value, str):
                                        result.append(elt.value)
                                return result
            return None
        except Exception:
            return None

    def _categorize_api_objects(self, package_name: str, exports: list) -> dict:
        """
        Categorize API objects into classes, functions, etc.

        Parameters
        ----------
        package_name
            The name of the package.
        exports
            List of exported names from __all__.

        Returns
        -------
        dict
            Dictionary with categorized API objects.
        """
        # Try to introspect the package
        try:
            import importlib
            import inspect

            # Import the package
            pkg = importlib.import_module(package_name.replace("-", "_"))

            categories = {"classes": [], "functions": [], "other": []}

            for name in exports:
                try:
                    obj = getattr(pkg, name, None)
                    if obj is None:
                        categories["other"].append(name)
                    elif inspect.isclass(obj):
                        categories["classes"].append(name)
                    elif inspect.isfunction(obj) or inspect.isbuiltin(obj):
                        categories["functions"].append(name)
                    else:
                        categories["other"].append(name)
                except Exception:
                    categories["other"].append(name)

            return categories
        except Exception:
            # If introspection fails, return all as "other"
            return {"classes": [], "functions": [], "other": exports}

    def _create_quartodoc_sections(self, package_name: str) -> Optional[list]:
        """
        Create quartodoc sections based on package's __all__.

        Parameters
        ----------
        package_name
            The name of the package.

        Returns
        -------
        Optional[list]
            List of section dictionaries, or None if no sections could be created.
        """
        exports = self._parse_package_exports(package_name)
        if not exports:
            return None

        print(f"Found {len(exports)} exported names in __all__")

        # Categorize the exports
        categories = self._categorize_api_objects(package_name, exports)

        sections = []

        # Add classes section if there are any
        if categories["classes"]:
            sections.append(
                {
                    "title": "Classes",
                    "desc": "Core classes and types",
                    "contents": categories["classes"],
                }
            )

        # Add functions section if there are any
        if categories["functions"]:
            sections.append(
                {
                    "title": "Functions",
                    "desc": "Public functions",
                    "contents": categories["functions"],
                }
            )

        # Add other exports section if there are any
        if categories["other"]:
            sections.append(
                {"title": "Other", "desc": "Additional exports", "contents": categories["other"]}
            )

        return sections if sections else None

    def _create_index_from_readme(self) -> None:
        """
        Create index.qmd from README.md if it doesn't exist.

        This mimics pkgdown's behavior of using the README as the homepage.
        """
        index_qmd = self.project_path / "index.qmd"

        if index_qmd.exists():
            print("index.qmd already exists, skipping creation")
            return

        readme_path = self.project_root / "README.md"
        if not readme_path.exists():
            print("No README.md found in project root, skipping index.qmd creation")
            return

        print("Creating index.qmd from README.md...")

        # Read README content
        with open(readme_path, "r", encoding="utf-8") as f:
            readme_content = f.read()

        # Create a simple qmd file with the README content
        qmd_content = f"""---
title: "Home"
---

{readme_content}
"""

        with open(index_qmd, "w", encoding="utf-8") as f:
            f.write(qmd_content)

        print(f"Created {index_qmd}")

    def _add_quartodoc_config(self) -> None:
        """
        Add quartodoc configuration to _quarto.yml if not present.

        Adds sensible defaults for quartodoc with automatic package detection.
        """
        quarto_yml = self.project_path / "_quarto.yml"

        with open(quarto_yml, "r") as f:
            config = yaml.safe_load(f) or {}

        # Check if quartodoc config already exists
        if "quartodoc" in config:
            print("quartodoc configuration already exists, skipping")
            return

        # Detect package name
        package_name = self._detect_package_name()

        if not package_name:
            response = input(
                "\nCould not auto-detect package name. Enter package name for quartodoc (or press Enter to skip): "
            ).strip()
            if not response:
                print("Skipping quartodoc configuration")
                return
            package_name = response

        print(f"Adding quartodoc configuration for package: {package_name}")

        # Try to auto-generate sections from __all__
        sections = self._create_quartodoc_sections(package_name)

        # Add quartodoc configuration with sensible defaults
        quartodoc_config = {
            "package": package_name,
            "dir": "reference",
            "title": "API Reference",
            "style": "pkgdown",
            "dynamic": True,
            "renderer": {"style": "markdown", "table_style": "description-list"},
        }

        # Add sections if we found them
        if sections:
            quartodoc_config["sections"] = sections
            print(f"Auto-generated {len(sections)} section(s) from __all__")
        else:
            print("Could not auto-generate sections from __all__")
            print("You'll need to manually add sections to organize your API documentation.")

        config["quartodoc"] = quartodoc_config

        # Write back to file
        with open(quarto_yml, "w") as f:
            yaml.dump(config, f, default_flow_style=False, sort_keys=False)

        print(f"Added quartodoc configuration to {quarto_yml}")
        if not sections:
            print("See: https://machow.github.io/quartodoc/get-started/overview.html")

    def _update_quarto_config(self) -> None:
        """
        Update _quarto.yml with great-theme configuration.

        This private method modifies the Quarto configuration file to include the
        post-render script and CSS file required by great-theme. It preserves
        existing configuration while adding the necessary great-theme settings.
        """
        quarto_yml = self.project_path / "_quarto.yml"

        if not quarto_yml.exists():
            print("Warning: _quarto.yml not found. Creating minimal configuration...")
            config = {
                "project": {"type": "website", "post-render": "scripts/post-render.py"},
                "format": {"html": {"theme": "flatly", "css": ["great-theme.css"]}},
            }
        else:
            # Load existing configuration
            with open(quarto_yml, "r") as f:
                config = yaml.safe_load(f) or {}

        # Ensure required structure exists
        if "project" not in config:
            config["project"] = {}
        if "format" not in config:
            config["format"] = {}
        if "html" not in config["format"]:
            config["format"]["html"] = {}

        # Add post-render script
        config["project"]["post-render"] = "scripts/post-render.py"

        # Add CSS file
        if "css" not in config["format"]["html"]:
            config["format"]["html"]["css"] = []
        elif isinstance(config["format"]["html"]["css"], str):
            config["format"]["html"]["css"] = [config["format"]["html"]["css"]]

        if "great-theme.css" not in config["format"]["html"]["css"]:
            config["format"]["html"]["css"].append("great-theme.css")

        # Ensure flatly theme is used (works well with great-theme)
        if "theme" not in config["format"]["html"]:
            config["format"]["html"]["theme"] = "flatly"

        # Write back to file
        with open(quarto_yml, "w") as f:
            yaml.dump(config, f, default_flow_style=False, sort_keys=False)

        print(f"Updated {quarto_yml} with great-theme configuration")

    def uninstall(self) -> None:
        """
        Remove great-theme assets and configuration from the project.

        This method deletes the great-theme CSS file and post-render script,
        and cleans up the `_quarto.yml` configuration file by removing
        great-theme-specific settings.

        Examples
        --------
        Uninstall the theme from the current directory:

        ```python
        from great_theme import GreatTheme

        theme = GreatTheme()
        theme.uninstall()
        ```

        Uninstall from a specific project directory:

        ```python
        theme = GreatTheme("/path/to/my/project")
        theme.uninstall()
        ```

        See Also
        --------
        install : Install great-theme assets and configuration
        """
        print("Uninstalling great-theme from your quartodoc project...")
        print(f"Removing from: {self.project_path.relative_to(self.project_root)}")

        # Remove files
        files_to_remove = [
            self.project_path / "scripts" / "post-render.py",
            self.project_path / "great-theme.css",
        ]

        for file_path in files_to_remove:
            if file_path.exists():
                file_path.unlink()
                print(f"Removed {file_path}")

        # Clean up _quarto.yml
        self._clean_quarto_config()

        print("✅ Great-theme uninstalled successfully!")

    def _clean_quarto_config(self) -> None:
        """
        Remove great-theme configuration from _quarto.yml.

        This private method removes the post-render script reference and CSS file
        entry from the Quarto configuration file, reverting it to its pre-installation
        state while preserving other user settings.
        """
        quarto_yml = self.project_path / "_quarto.yml"

        if not quarto_yml.exists():
            return

        with open(quarto_yml, "r") as f:
            config = yaml.safe_load(f) or {}

        # Remove post-render script if it's ours
        if config.get("project", {}).get("post-render") == "scripts/post-render.py":
            del config["project"]["post-render"]

        # Remove CSS file
        css_list = config.get("format", {}).get("html", {}).get("css", [])
        if isinstance(css_list, list) and "great-theme.css" in css_list:
            css_list.remove("great-theme.css")
            if not css_list:
                del config["format"]["html"]["css"]

        # Write back to file
        with open(quarto_yml, "w") as f:
            yaml.dump(config, f, default_flow_style=False, sort_keys=False)

        print(f"Cleaned great-theme configuration from {quarto_yml}")

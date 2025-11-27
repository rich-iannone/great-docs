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


class GreatDocs:
    """
    GreatDocs class for applying enhanced theming to quartodoc sites.

    This class provides methods to install assets and configure
    Quarto projects with the great-docs styling and functionality.
    """

    def __init__(self, project_path: Optional[str] = None, docs_dir: Optional[str] = None):
        """
        Initialize GreatDocs instance.

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
            self.package_path = Path(resources.files("great_docs"))
        except AttributeError:
            # Fallback for older Python versions
            import importlib_resources  # type: ignore[import-not-found]

            self.package_path = Path(importlib_resources.files("great_docs"))
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
                    f"Found existing '{dir_name}/' directory. Install great-docs here? [Y/n]: "
                )
                if response.lower() != "n":
                    return Path(dir_name)

        # No existing docs directory found - ask user
        print("\nNo documentation directory detected.")
        print("Where would you like to install great-docs?")
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
        Install great-docs assets and configuration to the project.

        This method copies the necessary CSS files and post-render script to your Quarto project
        directory, and automatically updates your `_quarto.yml` configuration file to use the
        great-docs styling.

        Parameters
        ----------
        force
            If True, overwrite existing files without prompting. Default is False.
        skip_quartodoc
            If True, skip adding quartodoc configuration. Useful for testing or when
            quartodoc is not needed. Default is False.

        Examples
        --------
        Install documentation in the current directory:

        ```python
        from great_docs import GreatDocs

        docs = GreatDocs()
        docs.install()
        ```

        Install documentation in a specific project directory, overwriting existing files:

        ```python
        docs = GreatDocs("/path/to/my/project")
        docs.install(force=True)
        ```

        See Also
        --------
        uninstall : Remove great-docs assets and configuration
        """
        print("Installing great-docs to your quartodoc project...")

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
        css_dst = self.project_path / "great-docs.css"

        if css_dst.exists() and not force:
            response = input(f"{css_dst} already exists. Overwrite? [y/N]: ")
            if response.lower() != "y":
                print("Skipping great-docs.css")
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

        print("\nGreat Docs installation complete!")
        if not skip_quartodoc:
            print("\nNext steps:")
            print("1. Review the generated quartodoc configuration in _quarto.yml")
            print("2. Run `great-docs build` to generate docs and build your site")
            print("   (This runs `quartodoc build` followed by `quarto render`)")
            print(f"3. Open {self.project_path / '_site' / 'index.html'} to preview your site")
            print("\nOther helpful commands:")
            print("  great-docs build          # Build everything")
            print("  great-docs build --watch  # Watch for changes and rebuild")
            print("  great-docs preview        # Build and serve locally")
        else:
            print("\nNext steps:")
            print("1. Run `quarto render` to build your site")

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

    def _find_package_init(self, package_name: str) -> Optional[Path]:
        """
        Find the __init__.py file for a package, searching common locations.

        This handles packages with non-standard structures like Rust bindings
        that may have their Python code in subdirectories like python/, src/, etc.

        Parameters
        ----------
        package_name
            The name of the package to find.

        Returns
        -------
        Optional[Path]
            Path to the __init__.py file, or None if not found.
        """
        # Normalize package name (replace dashes with underscores)
        normalized_name = package_name.replace("-", "_")

        # Common locations to search for package directories
        search_paths = [
            self.project_root / package_name,
            self.project_root / normalized_name,
            self.project_root / "python" / package_name,
            self.project_root / "python" / normalized_name,
            self.project_root / "src" / package_name,
            self.project_root / "src" / normalized_name,
            self.project_root / "lib" / package_name,
            self.project_root / "lib" / normalized_name,
        ]

        for package_dir in search_paths:
            if not package_dir.exists() or not package_dir.is_dir():
                continue

            init_file = package_dir / "__init__.py"
            if init_file.exists():
                # Verify this is likely the right __init__.py by checking for __version__
                try:
                    with open(init_file, "r", encoding="utf-8") as f:
                        content = f.read()
                        # Check if it has __version__ (good indicator of main package __init__)
                        if "__version__" in content or "__all__" in content:
                            return init_file
                except Exception:
                    continue

        return None

    def _parse_package_exports(self, package_name: str) -> Optional[list]:
        """
        Parse __all__ from package's __init__.py to get public API.

        Also checks for __gt_exclude__ to filter out non-documentable items.

        Parameters
        ----------
        package_name
            The name of the package to parse.

        Returns
        -------
        Optional[list]
            List of public names from __all__ (filtered by __gt_exclude__), or None if not found.
        """
        # Find the package's __init__.py file
        init_file = self._find_package_init(package_name)
        if not init_file:
            print(f"Could not locate __init__.py for package '{package_name}'")
            return None

        print(f"Found package __init__.py at: {init_file.relative_to(self.project_root)}")

        try:
            with open(init_file, "r", encoding="utf-8") as f:
                content = f.read()

            # Try to extract __all__ and __gt_exclude__ using AST (safer than eval)
            import ast

            tree = ast.parse(content)

            all_exports = None
            gt_exclude = []

            for node in ast.walk(tree):
                if isinstance(node, ast.Assign):
                    for target in node.targets:
                        # Extract __all__
                        if isinstance(target, ast.Name) and target.id == "__all__":
                            if isinstance(node.value, ast.List):
                                all_exports = []
                                for elt in node.value.elts:
                                    if isinstance(elt, ast.Constant) and isinstance(elt.value, str):
                                        all_exports.append(elt.value)

                        # Extract __gt_exclude__
                        if isinstance(target, ast.Name) and target.id == "__gt_exclude__":
                            if isinstance(node.value, ast.List):
                                for elt in node.value.elts:
                                    if isinstance(elt, ast.Constant) and isinstance(elt.value, str):
                                        gt_exclude.append(elt.value)

            if all_exports:
                print(f"Successfully parsed __all__ with {len(all_exports)} exports")

                # Filter out excluded items
                if gt_exclude:
                    filtered = [e for e in all_exports if e not in gt_exclude]
                    excluded_count = len(all_exports) - len(filtered)
                    if excluded_count > 0:
                        print(
                            f"Filtered out {excluded_count} item(s) from __gt_exclude__: {', '.join(gt_exclude)}"
                        )
                    return filtered
                else:
                    return all_exports

            print("No __all__ definition found in __init__.py")
            return None
        except Exception as e:
            print(f"Error parsing __all__: {type(e).__name__}: {e}")
            return None

    def _categorize_api_objects(self, package_name: str, exports: list) -> dict:
        """
        Categorize API objects using griffe introspection.

        Uses griffe (quartodoc's introspection library) to analyze the package
        structure without importing it. This is safer and works with packages
        that have non-Python components (e.g., Rust bindings).

        Parameters
        ----------
        package_name
            The name of the package.
        exports
            List of exported names from __all__.

        Returns
        -------
        dict
            Dictionary with:
            - classes: list of class names
            - functions: list of function names
            - other: list of other object names
            - class_methods: dict mapping class name to method count
            - class_method_names: dict mapping class name to list of method names
        """
        try:
            import griffe

            # Load the package using griffe
            normalized_name = package_name.replace("-", "_")

            # Try to load the package with griffe
            try:
                pkg = griffe.load(normalized_name)
            except Exception as e:
                print(f"Warning: Could not load package with griffe ({type(e).__name__})")
                # Fallback to simple categorization
                skip_names = {"__version__", "__author__", "__email__", "__all__"}
                filtered_exports = [e for e in exports if e not in skip_names]
                return {
                    "classes": [],
                    "functions": [],
                    "other": filtered_exports,
                    "class_methods": {},
                    "class_method_names": {},
                }

            categories = {
                "classes": [],
                "functions": [],
                "other": [],
                "class_methods": {},
                "class_method_names": {},
            }
            failed_introspection = []

            # Skip common metadata variables
            skip_names = {"__version__", "__author__", "__email__", "__all__"}

            for name in exports:
                # Skip metadata variables
                if name in skip_names:
                    continue

                try:
                    # Get the object from the loaded package
                    if name not in pkg.members:
                        categories["other"].append(name)
                        failed_introspection.append(name)
                        continue

                    obj = pkg.members[name]

                    # Categorize based on griffe's kind
                    if obj.kind.value == "class":
                        categories["classes"].append(name)
                        # Get public methods (exclude private/magic methods)
                        method_names = [
                            member_name
                            for member_name, member in obj.members.items()
                            if not member_name.startswith("_")
                            and member.kind.value in ("function", "method")
                        ]
                        categories["class_methods"][name] = len(method_names)
                        categories["class_method_names"][name] = sorted(method_names)
                        print(f"  {name}: class with {len(method_names)} public methods")
                    elif obj.kind.value == "function":
                        categories["functions"].append(name)
                    else:
                        # Attributes, modules, etc.
                        categories["other"].append(name)

                except Exception as e:
                    # If introspection fails for a specific object, still include it
                    print(f"  Warning: Could not introspect '{name}': {type(e).__name__}")
                    categories["other"].append(name)
                    failed_introspection.append(name)

            if failed_introspection:
                print(
                    f"Note: Could not introspect {len(failed_introspection)} item(s), categorizing as 'Other'"
                )

            return categories

        except ImportError:
            print("Warning: griffe not available, using fallback categorization")
            # Fallback if griffe isn't installed
            skip_names = {"__version__", "__author__", "__email__", "__all__"}
            filtered_exports = [e for e in exports if e not in skip_names]
            return {
                "classes": [],
                "functions": [],
                "other": filtered_exports,
                "class_methods": {},
                "class_method_names": {},
            }

    def _create_quartodoc_sections(self, package_name: str) -> Optional[list]:
        """
        Create quartodoc sections based on package's __all__.

        Uses smart heuristics:
        - Classes with ≤5 methods: documented inline
        - Classes with >5 methods: separate pages for each method

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

        # Filter out metadata variables at the export level too
        skip_names = {"__version__", "__author__", "__email__", "__all__"}
        exports = [e for e in exports if e not in skip_names]

        if not exports:
            return None

        print(f"Found {len(exports)} exported names in __all__")

        # Categorize the exports
        categories = self._categorize_api_objects(package_name, exports)

        sections = []

        # Add classes section if there are any
        if categories["classes"]:
            class_contents = []
            classes_with_separate_methods = []

            for class_name in categories["classes"]:
                method_count = categories["class_methods"].get(class_name, 0)

                if method_count > 5:
                    # Class with many methods: add with members: [] to suppress inline docs
                    class_contents.append({"name": class_name, "members": []})
                    classes_with_separate_methods.append(class_name)
                else:
                    # Class with few methods: document inline
                    class_contents.append(class_name)

            sections.append(
                {
                    "title": "Classes",
                    "desc": "Core classes and types",
                    "contents": class_contents,
                }
            )

            # Create separate sections for methods of large classes
            for class_name in classes_with_separate_methods:
                method_names = categories["class_method_names"].get(class_name, [])
                method_count = len(method_names)

                # Create fully qualified method references
                method_contents = [f"{class_name}.{method}" for method in method_names]

                sections.append(
                    {
                        "title": f"{class_name} Methods",
                        "desc": f"Methods for the {class_name} class",
                        "contents": method_contents,
                    }
                )

                print(f"  Created separate section for {class_name} with {method_count} methods")

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
        # Use empty title so "Home" doesn't appear on landing page
        qmd_content = f"""---
title: ""
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
        Update _quarto.yml with great-docs configuration.

        This private method modifies the Quarto configuration file to include the
        post-render script, CSS file, and website navigation required by great-docs.
        It preserves existing configuration while adding the necessary great-docs
        settings. If website navigation is not present, it adds a navbar with Home
        and API Reference links, and sets the site title to the package name.
        """
        quarto_yml = self.project_path / "_quarto.yml"

        if not quarto_yml.exists():
            print("Warning: _quarto.yml not found. Creating minimal configuration...")
            config = {
                "project": {"type": "website", "post-render": "scripts/post-render.py"},
                "format": {"html": {"theme": "flatly", "css": ["great-docs.css"]}},
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

        if "great-docs.css" not in config["format"]["html"]["css"]:
            config["format"]["html"]["css"].append("great-docs.css")

        # Ensure flatly theme is used (works well with great-docs)
        if "theme" not in config["format"]["html"]:
            config["format"]["html"]["theme"] = "flatly"

        # Add website navigation if not present
        if "website" not in config:
            config["website"] = {}

        # Set title to package name if not already set
        if "title" not in config["website"]:
            package_name = self._detect_package_name()
            if package_name:
                config["website"]["title"] = package_name.title()

        # Add navbar with Home and API Reference links if not present
        if "navbar" not in config["website"]:
            config["website"]["navbar"] = {
                "left": [
                    {"text": "Home", "href": "index.qmd"},
                    {"text": "API Reference", "href": "reference/index.qmd"},
                ]
            }

        # Write back to file
        with open(quarto_yml, "w") as f:
            yaml.dump(config, f, default_flow_style=False, sort_keys=False)

        print(f"Updated {quarto_yml} with great-docs configuration")

    def uninstall(self) -> None:
        """
        Remove great-docs assets and configuration from the project.

        This method deletes the great-docs CSS file and post-render script,
        and cleans up the `_quarto.yml` configuration file by removing
        great-docs-specific settings.

        Examples
        --------
        Uninstall the docs from the current directory:

        ```python
        from great_docs import GreatDocs

        docs = GreatDocs()
        docs.uninstall()
        ```

        Uninstall from a specific project directory:

        ```python
        docs = GreatDocs("/path/to/my/project")
        docs.uninstall()
        ```

        See Also
        --------
        install : Install great-docs assets and configuration
        """
        print("Uninstalling great-docs from your quartodoc project...")
        print(f"Removing from: {self.project_path.relative_to(self.project_root)}")

        # Remove files
        files_to_remove = [
            self.project_path / "scripts" / "post-render.py",
            self.project_path / "great-docs.css",
        ]

        for file_path in files_to_remove:
            if file_path.exists():
                file_path.unlink()
                print(f"Removed {file_path}")

        # Clean up _quarto.yml
        self._clean_quarto_config()

        print("✅ Great-docs uninstalled successfully!")

    def _clean_quarto_config(self) -> None:
        """
        Remove great-docs configuration from _quarto.yml.

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
        if isinstance(css_list, list) and "great-docs.css" in css_list:
            css_list.remove("great-docs.css")
            if not css_list:
                del config["format"]["html"]["css"]

        # Write back to file
        with open(quarto_yml, "w") as f:
            yaml.dump(config, f, default_flow_style=False, sort_keys=False)

        print(f"Cleaned great-docs configuration from {quarto_yml}")

    def build(self, watch: bool = False) -> None:
        """
        Build the documentation site.

        Runs quartodoc build followed by quarto render.

        Parameters
        ----------
        watch
            If True, watch for changes and rebuild automatically.

        Examples
        --------
        Build the documentation:

        ```python
        from great_docs import GreatDocs

        docs = GreatDocs()
        docs.build()
        ```

        Build with watch mode:

        ```python
        docs.build(watch=True)
        ```
        """
        import subprocess
        import sys
        import threading
        import time

        def show_progress(stop_event, message):
            """Show a simple spinner while command is running."""
            spinner = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
            idx = 0
            while not stop_event.is_set():
                print(f"\r{message} {spinner[idx % len(spinner)]}", end="", flush=True)
                idx += 1
                time.sleep(0.1)
            print(f"\r{message} ", end="", flush=True)

        print("Building documentation with great-docs...")

        # Change to docs directory
        original_dir = os.getcwd()
        try:
            os.chdir(self.project_path)

            # Step 1: Run quartodoc build using Python module execution
            # This ensures it uses the same Python environment as great-theme
            print("\n📚 Step 1: Generating API reference with quartodoc...")

            stop_event = threading.Event()
            progress_thread = threading.Thread(
                target=show_progress, args=(stop_event, "   Processing")
            )
            progress_thread.start()

            result = subprocess.run(
                [sys.executable, "-m", "quartodoc", "build"], capture_output=True, text=True
            )

            stop_event.set()
            progress_thread.join()

            if result.returncode != 0:
                print("\n❌ quartodoc build failed:")
                print(result.stderr)
                sys.exit(1)
            else:
                print("\n✅ API reference generated")

            # Step 2: Run quarto render or preview
            if watch:
                print("\n🔄 Step 2: Starting Quarto in watch mode...")
                print("Press Ctrl+C to stop watching")
                subprocess.run(["quarto", "preview", "--no-browser"])
            else:
                print("\n🔨 Step 2: Building site with Quarto...")

                stop_event = threading.Event()
                progress_thread = threading.Thread(
                    target=show_progress, args=(stop_event, "   Rendering")
                )
                progress_thread.start()

                result = subprocess.run(["quarto", "render"], capture_output=True, text=True)

                stop_event.set()
                progress_thread.join()

                if result.returncode != 0:
                    print("\n❌ quarto render failed:")
                    print(result.stderr)
                    sys.exit(1)
                else:
                    print("\n✅ Site built successfully")
                    site_path = self.project_path / "_site" / "index.html"
                    if site_path.exists():
                        print(f"\n🎉 Your site is ready! Open: {site_path}")
                    else:
                        print(f"\n🎉 Your site is ready in: {self.project_path / '_site'}")

        finally:
            os.chdir(original_dir)

    def preview(self) -> None:
        """
        Build and serve the documentation site locally.

        Runs quartodoc build, then starts a local server with quarto preview.

        Examples
        --------
        Preview the documentation:

        ```python
        from great_docs import GreatDocs

        docs = GreatDocs()
        docs.preview()
        ```
        """
        import subprocess

        print("Building and previewing documentation...")

        # Change to docs directory
        original_dir = os.getcwd()
        try:
            os.chdir(self.project_path)

            # Step 1: Run quartodoc build
            print("\n📚 Step 1: Generating API reference with quartodoc...")
            result = subprocess.run(["quartodoc", "build"], capture_output=True, text=True)

            if result.returncode != 0:
                print("❌ quartodoc build failed:")
                print(result.stderr)
                return
            else:
                print("✅ API reference generated")

            # Step 2: Run quarto preview
            print("\n🌐 Step 2: Starting preview server...")
            print("Press Ctrl+C to stop the server")
            subprocess.run(["quarto", "preview"])

        finally:
            os.chdir(original_dir)

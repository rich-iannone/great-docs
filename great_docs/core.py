import os
import re
import shutil
from importlib import resources
from pathlib import Path

import yaml


class GreatDocs:
    """
    GreatDocs class for creating beautiful API documentation sites.

    This class provides methods to install assets and configure
    Quarto projects with the great-docs styling and functionality.
    """

    def __init__(self, project_path: str | None = None, docs_dir: str | None = None):
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

    def _find_or_create_docs_dir(self, docs_dir: str | None = None) -> Path:
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

        # No existing docs directory found so ask user
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
            If `True`, overwrite existing files without prompting. Default is `False`.
        skip_quartodoc
            If `True`, skip adding quartodoc configuration. Useful for testing or when quartodoc is
            not needed. Default is `False`.

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
        """
        print("Installing great-docs...")

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
        css_src = self.assets_path / "great-docs.css"
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

        # Copy .gitignore file
        gitignore_src = self.assets_path / ".gitignore"
        gitignore_dst = self.project_path / ".gitignore"

        if gitignore_dst.exists() and not force:
            # Append to existing .gitignore if it doesn't already contain our entries
            with open(gitignore_dst, "r") as f:
                existing_content = f.read()

            if "_site/" not in existing_content:
                with open(gitignore_src, "r") as f:
                    new_content = f.read()
                with open(gitignore_dst, "a") as f:
                    f.write("\n" + new_content)
                print(f"Appended to {gitignore_dst}")
            else:
                print("Skipping .gitignore (already contains _site/ entry)")
        else:
            shutil.copy2(gitignore_src, gitignore_dst)
            print(f"Copied {gitignore_dst}")

        # Copy GitHub widget JavaScript file
        gh_widget_src = self.assets_path / "github-widget.js"
        gh_widget_dst = self.project_path / "github-widget.js"

        if gh_widget_dst.exists() and not force:
            response = input(f"{gh_widget_dst} already exists. Overwrite? [y/N]: ")
            if response.lower() != "y":
                print("Skipping github-widget.js")
            else:
                shutil.copy2(gh_widget_src, gh_widget_dst)
                print(f"Copied {gh_widget_dst}")
        else:
            shutil.copy2(gh_widget_src, gh_widget_dst)
            print(f"Copied {gh_widget_dst}")

        # Copy sidebar filter JavaScript file
        sidebar_filter_src = self.assets_path / "sidebar-filter.js"
        sidebar_filter_dst = self.project_path / "sidebar-filter.js"

        if sidebar_filter_src.exists():
            if sidebar_filter_dst.exists() and not force:
                response = input(f"{sidebar_filter_dst} already exists. Overwrite? [y/N]: ")
                if response.lower() != "y":
                    print("Skipping sidebar-filter.js")
                else:
                    shutil.copy2(sidebar_filter_src, sidebar_filter_dst)
                    print(f"Copied {sidebar_filter_dst}")
            else:
                shutil.copy2(sidebar_filter_src, sidebar_filter_dst)
                print(f"Copied {sidebar_filter_dst}")

        # Copy reference switcher JavaScript file (for CLI docs)
        ref_switcher_src = self.assets_path / "reference-switcher.js"
        ref_switcher_dst = self.project_path / "reference-switcher.js"

        if ref_switcher_src.exists():
            if ref_switcher_dst.exists() and not force:
                response = input(f"{ref_switcher_dst} already exists. Overwrite? [y/N]: ")
                if response.lower() != "y":
                    print("Skipping reference-switcher.js")
                else:
                    shutil.copy2(ref_switcher_src, ref_switcher_dst)
                    print(f"Copied {ref_switcher_dst}")
            else:
                shutil.copy2(ref_switcher_src, ref_switcher_dst)
                print(f"Copied {ref_switcher_dst}")

        # Copy dark mode toggle JavaScript file
        dark_mode_src = self.assets_path / "dark-mode-toggle.js"
        dark_mode_dst = self.project_path / "dark-mode-toggle.js"

        if dark_mode_src.exists():
            if dark_mode_dst.exists() and not force:
                response = input(f"{dark_mode_dst} already exists. Overwrite? [y/N]: ")
                if response.lower() != "y":
                    print("Skipping dark-mode-toggle.js")
                else:
                    shutil.copy2(dark_mode_src, dark_mode_dst)
                    print(f"Copied {dark_mode_dst}")
            else:
                shutil.copy2(dark_mode_src, dark_mode_dst)
                print(f"Copied {dark_mode_dst}")

        # Copy theme initialization JavaScript file (for early theme detection)
        theme_init_src = self.assets_path / "theme-init.js"
        theme_init_dst = self.project_path / "theme-init.js"

        if theme_init_src.exists():
            if theme_init_dst.exists() and not force:
                response = input(f"{theme_init_dst} already exists. Overwrite? [y/N]: ")
                if response.lower() != "y":
                    print("Skipping theme-init.js")
                else:
                    shutil.copy2(theme_init_src, theme_init_dst)
                    print(f"Copied {theme_init_dst}")
            else:
                shutil.copy2(theme_init_src, theme_init_dst)
                print(f"Copied {theme_init_dst}")

        # Update _quarto.yml configuration
        self._update_quarto_config()

        # Create index.qmd from README.md if it doesn't exist
        self._create_index_from_readme()

        # Add quartodoc configuration if not present
        if not skip_quartodoc:
            self._add_quartodoc_config()
            self._update_sidebar_from_sections()
            self._update_reference_index_frontmatter()

        print("\nGreat Docs installation complete!")
        if not skip_quartodoc:
            print("\nNext steps:")
            print("1. Review the generated configuration in _quarto.yml")
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

    def _detect_package_name(self) -> str | None:
        """
        Detect the Python package name from project structure.

        Returns
        -------
        str | None
            The detected package name, or None if not found.
        """
        # Look for pyproject.toml
        pyproject_path = self.project_root / "pyproject.toml"
        if pyproject_path.exists():
            import tomllib

            with open(pyproject_path, "rb") as f:
                try:
                    data = tomllib.load(f)
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

    def _normalize_package_name(self, package_name: str) -> str:
        """
        Convert a package name to its importable form.

        PyPI package names can use hyphens (e.g., 'great-docs') but Python
        imports must use underscores (e.g., 'great_docs'). This method handles
        the conversion.

        Parameters
        ----------
        package_name
            The package name (potentially with hyphens)

        Returns
        -------
        str
            The importable package name (with underscores)
        """
        return package_name.replace("-", "_")

    def _find_package_root(self) -> Path:
        """
        Find the actual package root directory (where pyproject.toml or setup.py exists).

        When the docs directory is the current directory, project_root might point to
        the docs dir rather than the package root. This method searches upward to find
        the actual package root.

        Returns
        -------
        Path
            The package root directory
        """
        current = self.project_root

        # Search upward from current directory
        for _ in range(5):  # Limit search to 5 levels up
            if (current / "pyproject.toml").exists() or (current / "setup.py").exists():
                return current
            parent = current.parent
            if parent == current:  # Reached filesystem root
                break
            current = parent

        # Fallback to project_root if we can't find it
        return self.project_root

    def _get_package_metadata(self) -> dict:
        """
        Extract package metadata from pyproject.toml for sidebar.

        Returns
        -------
        dict
            Dictionary containing package metadata like license, authors, URLs, etc.
        """
        metadata = {}
        package_root = self._find_package_root()
        pyproject_path = package_root / "pyproject.toml"

        if not pyproject_path.exists():
            return metadata

        import tomllib

        try:
            with open(pyproject_path, "rb") as f:
                data = tomllib.load(f)
                project = data.get("project", {})

                # Extract relevant fields
                metadata["license"] = project.get("license", {}).get("text") or project.get(
                    "license", {}
                ).get("file", "")
                metadata["authors"] = project.get("authors", [])
                metadata["maintainers"] = project.get("maintainers", [])
                metadata["urls"] = project.get("urls", {})
                metadata["requires_python"] = project.get("requires-python", "")
                metadata["keywords"] = project.get("keywords", [])
                metadata["description"] = project.get("description", "")
                metadata["optional_dependencies"] = project.get("optional-dependencies", {})

                # Extract rich author metadata and exclude list from tool.great-docs if available
                tool_config = data.get("tool", {}).get("great-docs", {})
                metadata["rich_authors"] = tool_config.get("authors", [])
                metadata["exclude"] = tool_config.get("exclude", [])
                metadata["include"] = tool_config.get("include", [])
                # Discovery method: "dir" (default) or "all" (use __all__)
                metadata["discovery_method"] = tool_config.get("discovery_method", "dir")

                # Source link configuration
                source_config = tool_config.get("source", {})
                metadata["source_link_enabled"] = source_config.get("enabled", True)
                metadata["source_link_branch"] = source_config.get("branch", None)
                metadata["source_link_path"] = source_config.get("path", None)
                metadata["source_link_placement"] = source_config.get("placement", "usage")

                # Family/group configuration for API organization
                metadata["families"] = tool_config.get("families", {})

                # GitHub link style: "widget" (default) or "icon"
                metadata["github_style"] = tool_config.get("github_style", "widget")

                # Sidebar filter configuration
                # - enabled: True (default) or False to disable
                # - min_items: minimum number of items to show filter (default: 20)
                sidebar_filter_config = tool_config.get("sidebar_filter", {})
                metadata["sidebar_filter_enabled"] = sidebar_filter_config.get("enabled", True)
                metadata["sidebar_filter_min_items"] = sidebar_filter_config.get("min_items", 20)

                # CLI documentation configuration
                # - enabled: True to auto-discover and document Click CLIs
                # - module: optional module path to CLI (e.g., "mypackage.cli")
                # - name: optional CLI name override (defaults to package name)
                cli_config = tool_config.get("cli", {})
                metadata["cli_enabled"] = cli_config.get("enabled", False)
                metadata["cli_module"] = cli_config.get("module", None)
                metadata["cli_name"] = cli_config.get("name", None)

                # Large class method threshold configuration
                # Classes with more methods than this threshold get separate method pages
                # Default: 5 methods
                metadata["large_class_method_threshold"] = tool_config.get(
                    "large_class_method_threshold", 5
                )

                # Dark mode toggle configuration
                # - enabled: True (default) or False to disable the toggle
                metadata["dark_mode_toggle_enabled"] = tool_config.get("dark_mode_toggle", True)

        except Exception:
            pass

        return metadata

    def _update_navbar_github_link(
        self,
        config: dict,
        owner: str | None,
        repo: str | None,
        repo_url: str | None,
        github_style: str,
    ) -> None:
        """
        Update an existing navbar's GitHub link to use widget or icon style.

        Parameters
        ----------
        config
            The Quarto configuration dictionary.
        owner
            GitHub repository owner.
        repo
            GitHub repository name.
        repo_url
            Full GitHub repository URL.
        github_style
            Either "widget" (with stats dropdown) or "icon" (simple link).
        """
        if not repo_url:
            return

        navbar = config["website"]["navbar"]

        # Ensure right section exists
        if "right" not in navbar:
            navbar["right"] = []

        # Build the new GitHub entry based on style
        if github_style == "widget" and owner and repo:
            new_gh_entry = {
                "text": f'<div id="github-widget" data-owner="{owner}" data-repo="{repo}"></div>'
            }
        else:
            new_gh_entry = {"icon": "github", "href": repo_url}

        # Look for existing GitHub entry and replace it
        new_right = []
        found_github = False

        for item in navbar["right"]:
            if isinstance(item, dict):
                # Check for simple GitHub icon
                if item.get("icon") == "github":
                    new_right.append(new_gh_entry)
                    found_github = True
                # Check for existing widget
                elif "github-widget" in str(item.get("text", "")):
                    new_right.append(new_gh_entry)
                    found_github = True
                else:
                    new_right.append(item)
            else:
                new_right.append(item)

        # If no GitHub entry was found, add one
        if not found_github:
            new_right.append(new_gh_entry)

        navbar["right"] = new_right

    def _get_github_repo_info(self) -> tuple[str | None, str | None, str | None]:
        """
        Extract GitHub repository information from pyproject.toml.

        Returns
        -------
        tuple[str | None, str | None, str | None]
            A tuple of (owner, repo_name, base_url) or (None, None, None) if not found.
        """
        metadata = self._get_package_metadata()
        urls = metadata.get("urls", {})

        # Look for repository URL in various common key names
        repo_url = None
        for key in ["Repository", "repository", "Source", "source", "GitHub", "github"]:
            if key in urls:
                repo_url = urls[key]
                break

        if not repo_url or "github.com" not in repo_url:
            return None, None, None

        # Parse the GitHub URL to extract owner and repo
        # Handles formats like:
        # - https://github.com/owner/repo
        # - https://github.com/owner/repo.git
        # - git@github.com:owner/repo.git
        github_pattern = r"github\.com[/:]([^/]+)/([^/\s.]+)"
        match = re.search(github_pattern, repo_url)

        if match:
            owner = match.group(1)
            repo = match.group(2).rstrip(".git")
            base_url = f"https://github.com/{owner}/{repo}"
            return owner, repo, base_url

        return None, None, None

    # =========================================================================
    # CLI Documentation Methods
    # =========================================================================

    def _discover_click_cli(self, package_name: str) -> dict | None:
        """
        Discover Click CLI commands and groups from a package.

        Attempts to find and import the Click CLI from the package, then extracts
        command structure, help text, options, and arguments.

        Parameters
        ----------
        package_name
            The name of the package to search for CLI.

        Returns
        -------
        dict | None
            Dictionary containing CLI structure, or None if no Click CLI found.
            Structure: {
                "name": "cli-name",
                "help": "CLI help text",
                "commands": [...],  # List of command dicts
                "options": [...],   # Global options
            }
        """
        metadata = self._get_package_metadata()

        # Check if CLI documentation is enabled
        if not metadata.get("cli_enabled", False):
            return None

        try:
            import click
        except ImportError:
            print("Click not installed, skipping CLI documentation")
            return None

        # Determine the CLI module to import
        cli_module_path = metadata.get("cli_module")
        if not cli_module_path:
            # Try common CLI module locations
            common_cli_modules = [
                f"{package_name}.cli",
                f"{package_name}.__main__",
                f"{package_name}.main",
                f"{package_name}.console",
                f"{package_name}.commands",
            ]
            cli_module_path = None
            for module_path in common_cli_modules:
                try:
                    import importlib

                    module = importlib.import_module(module_path)
                    # Look for Click command/group in module
                    for attr_name in dir(module):
                        attr = getattr(module, attr_name)
                        if isinstance(attr, (click.Command, click.Group)):
                            cli_module_path = module_path
                            break
                    if cli_module_path:
                        break
                except ImportError:
                    continue

        if not cli_module_path:
            print(f"No Click CLI found in {package_name}")
            return None

        try:
            import importlib

            module = importlib.import_module(cli_module_path)
        except ImportError as e:
            print(f"Could not import CLI module {cli_module_path}: {e}")
            return None

        # Find the main Click command/group
        cli_obj = None
        cli_name = metadata.get("cli_name")

        # First, look for explicitly named CLI
        if cli_name:
            cli_obj = getattr(module, cli_name, None)

        # Otherwise, search for Click commands/groups
        if not cli_obj:
            for attr_name in ["cli", "main", "app", "command", package_name.replace("-", "_")]:
                attr = getattr(module, attr_name, None)
                if isinstance(attr, (click.Command, click.Group)):
                    cli_obj = attr
                    cli_name = attr_name
                    break

        # If still not found, look for any Click command/group
        if not cli_obj:
            for attr_name in dir(module):
                if attr_name.startswith("_"):
                    continue
                attr = getattr(module, attr_name)
                if isinstance(attr, (click.Command, click.Group)):
                    cli_obj = attr
                    cli_name = attr_name
                    break

        if not cli_obj:
            print(f"No Click command/group found in {cli_module_path}")
            return None

        print(f"Found Click CLI: {cli_name} in {cli_module_path}")

        # Get the entry point name from pyproject.toml
        entry_point_name = self._get_cli_entry_point_name(package_name)
        display_name = entry_point_name or package_name.replace("_", "-")

        # Extract CLI structure
        cli_info = self._extract_click_command(cli_obj, display_name)
        cli_info["entry_point_name"] = display_name
        return cli_info

    def _get_cli_entry_point_name(self, package_name: str) -> str | None:
        """
        Get the CLI entry point name from pyproject.toml.

        Parameters
        ----------
        package_name
            The name of the package.

        Returns
        -------
        str | None
            The entry point name (e.g., "great-docs" from "[project.scripts]"),
            or None if not found.
        """
        package_root = self._find_package_root()
        pyproject_path = package_root / "pyproject.toml"

        if not pyproject_path.exists():
            return None

        import tomllib

        try:
            with open(pyproject_path, "rb") as f:
                data = tomllib.load(f)

            # Look for [project.scripts]
            scripts = data.get("project", {}).get("scripts", {})
            if scripts:
                # Return the first entry point name
                return list(scripts.keys())[0]

            # Also check [project.gui-scripts] for GUI apps
            gui_scripts = data.get("project", {}).get("gui-scripts", {})
            if gui_scripts:
                return list(gui_scripts.keys())[0]

        except Exception:
            pass

        return None

    def _extract_click_command(
        self, cmd: "click.Command", name: str, parent_path: str = ""
    ) -> dict:
        """
        Extract information from a Click command or group.

        Parameters
        ----------
        cmd
            The Click Command or Group object.
        name
            The command name.
        parent_path
            The parent command path for nested commands.

        Returns
        -------
        dict
            Dictionary containing command information.
        """
        import click

        full_path = f"{parent_path} {name}".strip() if parent_path else name

        # Get the actual --help output from Click
        help_text = self._get_click_help_text(cmd, full_path)

        info = {
            "name": name,
            "full_path": full_path,
            "help": cmd.help or "",
            "short_help": getattr(cmd, "short_help", "") or "",
            "help_text": help_text,  # The actual --help output
            "deprecated": getattr(cmd, "deprecated", False),
            "hidden": getattr(cmd, "hidden", False),
            "commands": [],
            "is_group": isinstance(cmd, click.Group),
        }

        # Extract subcommands if this is a group
        if isinstance(cmd, click.Group):
            for subcmd_name, subcmd in cmd.commands.items():
                if not getattr(subcmd, "hidden", False):
                    subcmd_info = self._extract_click_command(subcmd, subcmd_name, full_path)
                    info["commands"].append(subcmd_info)

        return info

    def _get_click_help_text(self, cmd: "click.Command", full_path: str) -> str:
        """
        Get the formatted --help output from a Click command.

        Parameters
        ----------
        cmd
            The Click Command object.
        full_path
            The full command path (e.g., "great-docs build").

        Returns
        -------
        str
            The formatted help text as it would appear from --help.
        """
        import click

        # Create a context to get the help text
        ctx = click.Context(cmd, info_name=full_path)
        return cmd.get_help(ctx)

    def _generate_cli_reference_pages(self, cli_info: dict) -> list[str]:
        """
        Generate Quarto reference pages for CLI commands.

        Parameters
        ----------
        cli_info
            Dictionary containing CLI structure from _discover_click_cli.

        Returns
        -------
        list[str]
            List of generated .qmd file paths (relative to docs dir).
        """
        if not cli_info:
            return []

        cli_ref_dir = self.project_path / "reference" / "cli"
        cli_ref_dir.mkdir(parents=True, exist_ok=True)

        generated_files = []

        # Generate main CLI page
        main_page = self._generate_cli_command_page(cli_info, is_main=True)
        main_path = cli_ref_dir / "index.qmd"
        with open(main_path, "w") as f:
            f.write(main_page)
        generated_files.append("reference/cli/index.qmd")
        print(f"Generated CLI reference: {main_path.relative_to(self.project_path)}")

        # Generate pages for subcommands
        generated_files.extend(self._generate_subcommand_pages(cli_info, cli_ref_dir))

        return generated_files

    def _generate_subcommand_pages(self, cmd_info: dict, output_dir: Path) -> list[str]:
        """
        Recursively generate pages for subcommands.

        Parameters
        ----------
        cmd_info
            Command information dictionary.
        output_dir
            Directory to write pages to.

        Returns
        -------
        list[str]
            List of generated file paths.
        """
        generated = []

        for subcmd in cmd_info.get("commands", []):
            # Generate page for this subcommand
            page_content = self._generate_cli_command_page(subcmd, is_main=False)
            safe_name = subcmd["name"].replace("-", "_")
            page_path = output_dir / f"{safe_name}.qmd"

            with open(page_path, "w") as f:
                f.write(page_content)

            rel_path = f"reference/cli/{safe_name}.qmd"
            generated.append(rel_path)
            print(f"Generated CLI reference: {page_path.relative_to(self.project_path)}")

            # Recursively generate for nested subcommands
            if subcmd.get("commands"):
                subcmd_dir = output_dir / safe_name
                subcmd_dir.mkdir(exist_ok=True)
                generated.extend(self._generate_subcommand_pages(subcmd, subcmd_dir))

        return generated

    def _generate_cli_command_page(self, cmd_info: dict, is_main: bool = False) -> str:
        """
        Generate Quarto page content for a CLI command showing --help output.

        Parameters
        ----------
        cmd_info
            Command information dictionary.
        is_main
            Whether this is the main CLI entry point.

        Returns
        -------
        str
            Quarto markdown content with the CLI help output.
        """
        lines = []

        # Front matter: use just the command name/path as title
        title = cmd_info["full_path"] if not is_main else cmd_info["name"]
        lines.append("---")
        lines.append(f'title: "{title}"')
        lines.append("---")
        lines.append("")

        # Output the help text in a styled div
        lines.append("::: {.cli-manpage}")
        lines.append("")
        lines.append("```")
        lines.append(cmd_info.get("help_text", "").rstrip())
        lines.append("```")
        lines.append("")
        lines.append(":::")
        lines.append("")

        return "\n".join(lines)

    def _update_sidebar_with_cli(self, cli_files: list[str]) -> None:
        """
        Update the sidebar configuration to include CLI reference.

        Parameters
        ----------
        cli_files
            List of generated CLI reference file paths.
        """
        if not cli_files:
            return

        quarto_yml = self.project_path / "_quarto.yml"
        if not quarto_yml.exists():
            return

        with open(quarto_yml, "r") as f:
            config = yaml.safe_load(f) or {}

        if "website" not in config:
            config["website"] = {}

        # Ensure sidebar exists
        if "sidebar" not in config["website"]:
            config["website"]["sidebar"] = []

        # Check if CLI section already exists
        sidebar = config["website"]["sidebar"]
        cli_section_exists = False

        for section in sidebar:
            if isinstance(section, dict) and section.get("id") == "cli-reference":
                cli_section_exists = True
                # Update contents
                section["contents"] = cli_files
                break

        if not cli_section_exists:
            # Add CLI section
            cli_section = {
                "id": "cli-reference",
                "title": "CLI Reference",
                "contents": cli_files,
            }
            sidebar.append(cli_section)

        # Ensure the reference sidebar has an API link at the top
        for section in sidebar:
            if isinstance(section, dict) and section.get("id") == "reference":
                contents = section.get("contents", [])
                # Check if API link already exists at the top
                has_api_link = False
                if contents and isinstance(contents[0], dict):
                    if contents[0].get("text") == "API" or contents[0].get("href", "").endswith(
                        "reference/index.qmd"
                    ):
                        has_api_link = True
                if not has_api_link:
                    # Add API link at the top
                    section["contents"] = [
                        {"text": "API", "href": "reference/index.qmd"},
                    ] + contents
                break

        with open(quarto_yml, "w") as f:
            yaml.dump(config, f, default_flow_style=False, sort_keys=False)

        print(f"Updated sidebar with {len(cli_files)} CLI reference page(s)")

    # =========================================================================
    # User Guide Methods
    # =========================================================================

    def _discover_user_guide(self) -> dict | None:
        """
        Discover user guide content from the user_guide directory.

        Looks for a `user_guide/` directory in the project root and discovers
        all .qmd files within it. Files are sorted by filename to support
        ordering via prefixes like `00-intro.qmd`, `01-installation.qmd`.

        Returns
        -------
        dict | None
            Dictionary containing user guide structure, or None if no user guide found.
            Structure: {
                "files": [{"path": Path, "section": str | None, "title": str}, ...],
                "sections": {"Section Name": [file_info, ...], ...},
                "has_index": bool
            }
        """
        # Look for user_guide directory in project root (not docs dir)
        user_guide_dir = self._find_package_root() / "user_guide"

        if not user_guide_dir.exists() or not user_guide_dir.is_dir():
            return None

        # Find all .qmd files (not in subdirectories that are likely asset folders)
        qmd_files = []
        for item in user_guide_dir.iterdir():
            if item.is_file() and item.suffix == ".qmd":
                qmd_files.append(item)
            elif item.is_dir():
                # Check subdirectories for .qmd files (but not nested deeper)
                for subitem in item.iterdir():
                    if subitem.is_file() and subitem.suffix == ".qmd":
                        qmd_files.append(subitem)

        if not qmd_files:
            return None

        # Sort files by name to respect ordering prefixes
        qmd_files.sort(key=lambda p: p.name)

        # Parse each file to extract section and title from frontmatter
        files_info = []
        sections: dict[str, list] = {}
        has_index = False

        for qmd_path in qmd_files:
            file_info = self._parse_user_guide_file(qmd_path)
            if file_info:
                files_info.append(file_info)

                # Track if there's an index.qmd
                if qmd_path.name == "index.qmd":
                    has_index = True

                # Group by section
                section_name = file_info.get("section")
                if section_name:
                    if section_name not in sections:
                        sections[section_name] = []
                    sections[section_name].append(file_info)

        if not files_info:
            return None

        return {
            "files": files_info,
            "sections": sections,
            "has_index": has_index,
            "source_dir": user_guide_dir,
        }

    def _parse_user_guide_file(self, qmd_path: Path) -> dict | None:
        """
        Parse a user guide .qmd file to extract metadata from frontmatter.

        Parameters
        ----------
        qmd_path
            Path to the .qmd file.

        Returns
        -------
        dict | None
            Dictionary with file info: {"path": Path, "section": str | None, "title": str}
        """
        try:
            with open(qmd_path, "r", encoding="utf-8") as f:
                content = f.read()
        except Exception:
            return None

        # Extract YAML frontmatter
        frontmatter = {}
        if content.startswith("---"):
            parts = content.split("---", 2)
            if len(parts) >= 3:
                try:
                    frontmatter = yaml.safe_load(parts[1]) or {}
                except yaml.YAMLError:
                    pass

        # Get title from frontmatter or derive from filename
        title = frontmatter.get("title")
        if not title:
            # Derive title from filename: "01-getting-started.qmd" -> "Getting Started"
            name = qmd_path.stem
            # Remove leading number prefix like "01-" or "00_"
            name = re.sub(r"^\d+[-_]", "", name)
            # Convert to title case
            title = name.replace("-", " ").replace("_", " ").title()

        # Get section from frontmatter (use 'guide-section' to avoid conflict with Quarto's 'section')
        section = frontmatter.get("guide-section")

        return {
            "path": qmd_path,
            "section": section,
            "title": title,
            "frontmatter": frontmatter,
        }

    def _copy_user_guide_to_docs(self, user_guide_info: dict) -> list[str]:
        """
        Copy user guide files from project root to docs directory.

        Adds `bread-crumbs: false` to the frontmatter of each file to disable
        breadcrumb navigation on user guide pages.

        Parameters
        ----------
        user_guide_info
            User guide structure from _discover_user_guide.

        Returns
        -------
        list[str]
            List of copied file paths relative to docs dir.
        """
        if not user_guide_info:
            return []

        source_dir = user_guide_info["source_dir"]
        target_dir = self.project_path / "user-guide"
        target_dir.mkdir(parents=True, exist_ok=True)

        copied_files = []

        # Copy all .qmd files, adding bread-crumbs: false to frontmatter
        for file_info in user_guide_info["files"]:
            src_path = file_info["path"]

            # Determine relative path from source_dir
            try:
                rel_path = src_path.relative_to(source_dir)
            except ValueError:
                rel_path = Path(src_path.name)

            dst_path = target_dir / rel_path
            dst_path.parent.mkdir(parents=True, exist_ok=True)

            # Read the source file and modify frontmatter
            with open(src_path, "r", encoding="utf-8") as f:
                content = f.read()

            # Add bread-crumbs: false to frontmatter
            content = self._add_frontmatter_option(content, "bread-crumbs", False)

            # Write to destination
            with open(dst_path, "w", encoding="utf-8") as f:
                f.write(content)

            copied_files.append(f"user-guide/{rel_path}")

        # Also copy any asset directories (directories without .qmd files)
        for item in source_dir.iterdir():
            if item.is_dir():
                # Check if this directory has any .qmd files
                has_qmd = any(f.suffix == ".qmd" for f in item.rglob("*"))
                if not has_qmd:
                    # This is likely an asset directory, copy it
                    dst_dir = target_dir / item.name
                    if dst_dir.exists():
                        shutil.rmtree(dst_dir)
                    shutil.copytree(item, dst_dir)

        return copied_files

    def _add_frontmatter_option(self, content: str, key: str, value) -> str:
        """
        Add or update an option in the YAML frontmatter of a .qmd file.

        Parameters
        ----------
        content
            The file content.
        key
            The frontmatter key to add/update.
        value
            The value to set.

        Returns
        -------
        str
            The modified content with the frontmatter option added.
        """
        # Convert value to YAML string representation
        if isinstance(value, bool):
            yaml_value = "true" if value else "false"
        elif isinstance(value, str):
            yaml_value = f'"{value}"'
        else:
            yaml_value = str(value)

        if content.startswith("---"):
            parts = content.split("---", 2)
            if len(parts) >= 3:
                frontmatter = parts[1]
                rest = parts[2]

                # Check if the key already exists
                key_pattern = rf"^{re.escape(key)}:\s*.*$"
                if re.search(key_pattern, frontmatter, re.MULTILINE):
                    # Update existing key
                    frontmatter = re.sub(
                        key_pattern, f"{key}: {yaml_value}", frontmatter, flags=re.MULTILINE
                    )
                else:
                    # Add new key at the end of frontmatter
                    frontmatter = frontmatter.rstrip() + f"\n{key}: {yaml_value}\n"

                return f"---{frontmatter}---{rest}"

        # No frontmatter, create one
        return f"---\n{key}: {yaml_value}\n---\n\n{content}"

    def _generate_user_guide_sidebar(self, user_guide_info: dict) -> dict:
        """
        Generate sidebar configuration for the user guide.

        Parameters
        ----------
        user_guide_info
            User guide structure from _discover_user_guide.

        Returns
        -------
        dict
            Sidebar configuration dict for Quarto.
        """
        source_dir = user_guide_info["source_dir"]
        files_info = user_guide_info["files"]
        sections = user_guide_info["sections"]

        contents = []

        # If we have sections, organize by section
        if sections:
            # Track which files have been assigned to sections
            assigned_files = set()

            # First, preserve section order based on first file appearance
            section_order = []
            for file_info in files_info:
                section = file_info.get("section")
                if section and section not in section_order:
                    section_order.append(section)

            # Build section entries
            for section_name in section_order:
                section_files = sections[section_name]
                section_contents = []

                for file_info in section_files:
                    rel_path = file_info["path"].relative_to(source_dir)
                    href = f"user-guide/{rel_path}"
                    assigned_files.add(file_info["path"])

                    # Use custom text for index.qmd if it has a title
                    if file_info["path"].name == "index.qmd":
                        section_contents.append(
                            {
                                "text": file_info["title"],
                                "href": href,
                            }
                        )
                    else:
                        section_contents.append(href)

                contents.append(
                    {
                        "section": section_name,
                        "contents": section_contents,
                    }
                )

            # Add any files without sections at the end
            unsectioned = []
            for file_info in files_info:
                if file_info["path"] not in assigned_files:
                    rel_path = file_info["path"].relative_to(source_dir)
                    unsectioned.append(f"user-guide/{rel_path}")

            if unsectioned:
                contents.extend(unsectioned)

        else:
            # No sections, just list files in order
            for file_info in files_info:
                rel_path = file_info["path"].relative_to(source_dir)
                contents.append(f"user-guide/{rel_path}")

        return {
            "id": "user-guide",
            "title": "User Guide",
            "contents": contents,
        }

    def _update_config_with_user_guide(self, user_guide_info: dict) -> None:
        """
        Update _quarto.yml with user guide sidebar and navbar.

        Parameters
        ----------
        user_guide_info
            User guide structure from _discover_user_guide.
        """
        quarto_yml = self.project_path / "_quarto.yml"
        if not quarto_yml.exists():
            return

        with open(quarto_yml, "r") as f:
            config = yaml.safe_load(f) or {}

        if "website" not in config:
            config["website"] = {}

        # Generate and add/update user guide sidebar
        sidebar_config = self._generate_user_guide_sidebar(user_guide_info)

        if "sidebar" not in config["website"]:
            config["website"]["sidebar"] = []

        sidebar = config["website"]["sidebar"]

        # Remove existing user-guide sidebar if present
        sidebar = [s for s in sidebar if not (isinstance(s, dict) and s.get("id") == "user-guide")]

        # Add the new user guide sidebar
        sidebar.append(sidebar_config)
        config["website"]["sidebar"] = sidebar

        # Update navbar to include User Guide link
        if "navbar" in config["website"]:
            navbar = config["website"]["navbar"]
            if "left" in navbar:
                # Check if User Guide link already exists
                has_user_guide = any(
                    isinstance(item, dict) and item.get("text") == "User Guide"
                    for item in navbar["left"]
                )
                if not has_user_guide:
                    # Find the position after "Home" and before "Reference"
                    insert_idx = 1  # Default: after Home
                    for i, item in enumerate(navbar["left"]):
                        if isinstance(item, dict) and item.get("text") == "Reference":
                            insert_idx = i
                            break

                    # Determine the href for User Guide
                    if user_guide_info.get("has_index"):
                        user_guide_href = "user-guide/index.qmd"
                    else:
                        # Use the first file
                        first_file = user_guide_info["files"][0]
                        rel_path = first_file["path"].relative_to(user_guide_info["source_dir"])
                        user_guide_href = f"user-guide/{rel_path}"

                    navbar["left"].insert(
                        insert_idx,
                        {
                            "text": "User Guide",
                            "href": user_guide_href,
                        },
                    )

        with open(quarto_yml, "w") as f:
            yaml.dump(config, f, default_flow_style=False, sort_keys=False)

    def _process_user_guide(self) -> bool:
        """
        Process user guide content: discover, copy, and update configuration.

        Returns
        -------
        bool
            True if user guide was processed, False otherwise.
        """
        # Discover user guide
        user_guide_info = self._discover_user_guide()
        if not user_guide_info:
            return False

        print("\n📖 Processing User Guide...")
        print(f"   Found {len(user_guide_info['files'])} page(s)")

        # Copy files to docs directory
        copied_files = self._copy_user_guide_to_docs(user_guide_info)
        print(f"   Copied {len(copied_files)} file(s) to docs/user-guide/")

        # Update configuration
        self._update_config_with_user_guide(user_guide_info)

        # Report sections
        if user_guide_info["sections"]:
            section_names = list(user_guide_info["sections"].keys())
            print(f"   Sections: {', '.join(section_names)}")

        print("✅ User Guide configured")
        return True

    def _get_source_location(self, package_name: str, item_name: str) -> dict | None:
        """
        Get source file and line numbers for a class, method, or function.

        Uses griffe for static analysis to avoid import side effects.

        Parameters
        ----------
        package_name
            The name of the package containing the item.
        item_name
            The fully qualified name of the item (e.g., "ClassName" or "ClassName.method_name").

        Returns
        -------
        dict | None
            Dictionary with file path and line numbers, or None if not found.
        """
        try:
            import griffe

            normalized_name = package_name.replace("-", "_")

            # Load the package with griffe
            try:
                pkg = griffe.load(normalized_name)
            except Exception:
                return None

            # Navigate to the item (handle dotted names like "ClassName.method")
            parts = item_name.split(".")
            obj = pkg

            for part in parts:
                if part not in obj.members:
                    return None
                obj = obj.members[part]

            # Get source information
            if not hasattr(obj, "lineno") or obj.lineno is None:
                return None

            # Get the file path relative to package root
            if hasattr(obj, "filepath") and obj.filepath:
                filepath = str(obj.filepath)
            else:
                return None

            # Get end line number
            end_lineno = getattr(obj, "endlineno", obj.lineno)

            return {
                "file": filepath,
                "start_line": obj.lineno,
                "end_line": end_lineno or obj.lineno,
            }

        except ImportError:
            return None
        except Exception:
            return None

    def _build_github_source_url(
        self, source_location: dict, branch: str | None = None
    ) -> str | None:
        """
        Build a GitHub URL for viewing source code at specific line numbers.

        Parameters
        ----------
        source_location
            Dictionary with file path and line numbers.
        branch
            Git branch/tag to link to. If None, attempts to detect from git
            or falls back to 'main'.

        Returns
        -------
        str | None
            Full GitHub URL with line anchors, or None if repo info not available.
        """
        owner, repo, base_url = self._get_github_repo_info()

        if not base_url:
            return None

        # Determine the branch/ref to use
        if branch is None:
            branch = self._detect_git_ref()

        # Get the file path relative to the repository root
        filepath = source_location.get("file", "")
        package_root = self._find_package_root()

        # Handle source path configuration for monorepos
        metadata = self._get_package_metadata()
        source_path = metadata.get("source_link_path")

        if source_path:
            # Custom source path specified (for monorepos)
            relative_path = f"{source_path}/{Path(filepath).name}"
        else:
            # Try to make the path relative to package root
            try:
                filepath_obj = Path(filepath)
                if filepath_obj.is_absolute():
                    relative_path = str(filepath_obj.relative_to(package_root))
                else:
                    relative_path = filepath
            except ValueError:
                # Path is not relative to package root, use as-is
                relative_path = filepath

        # Build the URL with line number anchors
        start_line = source_location.get("start_line", 1)
        end_line = source_location.get("end_line", start_line)

        url = f"{base_url}/blob/{branch}/{relative_path}"

        if start_line == end_line:
            url += f"#L{start_line}"
        else:
            url += f"#L{start_line}-L{end_line}"

        return url

    def _detect_git_ref(self) -> str:
        """
        Detect the current git branch or tag.

        Returns
        -------
        str
            The current branch/tag name, or 'main' as fallback.
        """
        import subprocess

        package_root = self._find_package_root()

        # First check if there's a configured branch in metadata
        metadata = self._get_package_metadata()
        configured_branch = metadata.get("source_link_branch")
        if configured_branch:
            return configured_branch

        try:
            # Try to get the current tag first (for versioned docs)
            result = subprocess.run(
                ["git", "describe", "--tags", "--exact-match"],
                cwd=package_root,
                capture_output=True,
                text=True,
            )
            if result.returncode == 0:
                return result.stdout.strip()

            # Fall back to branch name
            result = subprocess.run(
                ["git", "rev-parse", "--abbrev-ref", "HEAD"],
                cwd=package_root,
                capture_output=True,
                text=True,
            )
            if result.returncode == 0:
                branch = result.stdout.strip()
                if branch != "HEAD":
                    return branch

        except Exception:
            pass

        # Default fallback
        return "main"

    def _generate_source_links_json(self, package_name: str) -> None:
        """
        Generate a JSON file mapping object names to their GitHub source URLs.

        This file is used by the post-render script to inject source links
        into the HTML documentation.

        Parameters
        ----------
        package_name
            The name of the package to generate source links for.
        """
        import json

        metadata = self._get_package_metadata()

        # Check if source links are enabled
        if not metadata.get("source_link_enabled", True):
            print("Source links disabled in configuration")
            return

        # Check if we have GitHub repo info
        owner, repo, base_url = self._get_github_repo_info()
        if not base_url:
            print("No GitHub repository URL found, skipping source links")
            return

        print(f"Generating source links for {package_name}...")

        source_links: dict[str, dict] = {}
        normalized_name = package_name.replace("-", "_")

        # Get all exports
        exports = self._get_package_exports(package_name)
        if not exports:
            return

        # Get branch for source links
        branch = self._detect_git_ref()
        print(f"Using git ref: {branch}")

        # Generate source links for each export
        for item_name in exports:
            source_loc = self._get_source_location(normalized_name, item_name)
            if source_loc:
                github_url = self._build_github_source_url(source_loc, branch)
                if github_url:
                    source_links[item_name] = {
                        "url": github_url,
                        "file": source_loc.get("file", ""),
                        "start_line": source_loc.get("start_line", 0),
                        "end_line": source_loc.get("end_line", 0),
                    }

            # Also get source links for methods of classes
            categories = self._categorize_api_objects(package_name, [item_name])
            if item_name in categories.get("classes", []):
                method_names = categories.get("class_method_names", {}).get(item_name, [])
                for method_name in method_names:
                    full_name = f"{item_name}.{method_name}"
                    method_loc = self._get_source_location(normalized_name, full_name)
                    if method_loc:
                        method_url = self._build_github_source_url(method_loc, branch)
                        if method_url:
                            source_links[full_name] = {
                                "url": method_url,
                                "file": method_loc.get("file", ""),
                                "start_line": method_loc.get("start_line", 0),
                                "end_line": method_loc.get("end_line", 0),
                            }

        # Write to JSON file in the docs directory
        source_links_path = self.project_path / "_source_links.json"
        with open(source_links_path, "w", encoding="utf-8") as f:
            json.dump(source_links, f, indent=2)

        print(f"Generated source links for {len(source_links)} items")

    def _find_package_init(self, package_name: str) -> Path | None:
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
        Path | None
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

    def _parse_package_exports(self, package_name: str) -> list | None:
        """
        Parse __all__ from package's __init__.py to get public API.

        Also checks for __gt_exclude__ in __init__.py or exclude in [tool.great-docs]
        to filter out non-documentable items.

        Parameters
        ----------
        package_name
            The name of the package to parse.

        Returns
        -------
        list | None
            List of public names from __all__ (filtered by exclusions), or None if not found.
        """
        # Find the package's __init__.py file
        init_file = self._find_package_init(package_name)
        if not init_file:
            print(f"Could not locate __init__.py for package '{package_name}'")
            return None

        print(f"Found package __init__.py at: {init_file.relative_to(self.project_root)}")

        # Get exclusions from pyproject.toml [tool.great-docs]
        metadata = self._get_package_metadata()
        config_exclude = metadata.get("exclude", [])

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

                        # Extract __gt_exclude__ (legacy support)
                        if isinstance(target, ast.Name) and target.id == "__gt_exclude__":
                            if isinstance(node.value, ast.List):
                                for elt in node.value.elts:
                                    if isinstance(elt, ast.Constant) and isinstance(elt.value, str):
                                        gt_exclude.append(elt.value)

            if all_exports:
                print(f"Successfully parsed __all__ with {len(all_exports)} exports")

                # Combine exclusions from both sources
                all_exclude = list(set(gt_exclude + config_exclude))

                # Filter out excluded items
                if all_exclude:
                    filtered = [e for e in all_exports if e not in all_exclude]
                    excluded_count = len(all_exports) - len(filtered)
                    if excluded_count > 0:
                        source = []
                        if gt_exclude:
                            source.append("__gt_exclude__")
                        if config_exclude:
                            source.append("[tool.great-docs] exclude")
                        print(
                            f"Filtered out {excluded_count} item(s) from {' and '.join(source)}: {', '.join(all_exclude)}"
                        )
                    return filtered
                else:
                    return all_exports

            print("No __all__ definition found in __init__.py")
            return None
        except Exception as e:
            print(f"Error parsing __all__: {type(e).__name__}: {e}")
            return None

    # Auto-excluded names that are typically not meant for documentation
    # These are common internal/utility exports that most packages don't want documented
    AUTO_EXCLUDE = {
        # CLI and entry points
        "main",  # CLI entry point function
        "cli",  # CLI module
        # Version and metadata
        "version",  # Version string/function
        "VERSION",  # Uppercase version constant
        "VERSION_INFO",  # Version info tuple
        # Common module re-exports
        "core",  # Core module
        "utils",  # Utilities module
        "helpers",  # Helpers module
        "constants",  # Constants module
        "config",  # Config module
        "settings",  # Settings module
        # Standard library re-exports
        "PackageNotFoundError",  # importlib.metadata exception
        "typing",  # typing module re-export
        "annotations",  # annotations module re-export
        "TYPE_CHECKING",  # typing.TYPE_CHECKING constant
        # Logging
        "logger",  # Module-level logger instance
        "log",  # Alternative logger name
        "logging",  # logging module re-export
    }

    def _discover_package_exports(self, package_name: str) -> list | None:
        """
        Discover public API objects using griffe introspection.

        This method uses griffe (quartodoc's introspection library) to statically analyze the
        package and discover all public objects by filtering out private/internal names (those
        starting with underscore).

        Auto-excludes common internal names (see `AUTO_EXCLUDE`) unless they are explicitly included
        via the `include` option in `pyproject.toml`.

        Parameters
        ----------
        package_name
            The name of the package to discover exports from.

        Returns
        -------
        list | None
            List of public names discovered (filtered by exclusions), or `None` if discovery failed.
        """
        try:
            import griffe

            # Normalize package name (replace dashes with underscores)
            normalized_name = package_name.replace("-", "_")

            # Load the package using griffe
            try:
                pkg = griffe.load(normalized_name)
            except Exception as e:
                print(f"Warning: Could not load package with griffe ({type(e).__name__})")
                return None

            # Get all members from the package (equivalent to dir(package))
            all_members = list(pkg.members.keys())

            # Filter out private names (starting with underscore)
            # This also filters out dunder names like __version__, __all__, etc.
            public_members = [name for name in all_members if not name.startswith("_")]

            print(f"Discovered {len(public_members)} public names")

            # Get config from pyproject.toml [tool.great-docs]
            metadata = self._get_package_metadata()
            config_exclude = set(metadata.get("exclude", []))
            config_include = set(metadata.get("include", []))

            # Apply auto-exclusions (but respect explicit includes)
            auto_excluded = self.AUTO_EXCLUDE - config_include
            if auto_excluded:
                auto_excluded_found = [name for name in public_members if name in auto_excluded]
                if auto_excluded_found:
                    print(
                        f"Auto-excluding {len(auto_excluded_found)} item(s): "
                        f"{', '.join(sorted(auto_excluded_found))}"
                    )

            # Combine all exclusions (auto + user-specified), minus explicit includes
            all_exclude = (auto_excluded | config_exclude) - config_include

            # Filter out excluded items
            filtered = [name for name in public_members if name not in all_exclude]

            # Report user-specified exclusions separately
            if config_exclude:
                user_excluded_found = [
                    name
                    for name in public_members
                    if name in config_exclude and name not in auto_excluded
                ]
                if user_excluded_found:
                    print(
                        f"Filtered out {len(user_excluded_found)} item(s) from [tool.great-docs] exclude: "
                        f"{', '.join(sorted(user_excluded_found))}"
                    )

            # Report explicit includes that overrode auto-exclusions
            if config_include:
                overridden = [
                    name
                    for name in public_members
                    if name in config_include and name in self.AUTO_EXCLUDE
                ]
                if overridden:
                    print(
                        f"Including {len(overridden)} auto-excluded item(s) via [tool.great-docs] include: "
                        f"{', '.join(sorted(overridden))}"
                    )

            # Super-safe filtering: try each object with quartodoc's get_object
            # If it fails for ANY reason, exclude it; this catches:
            # - Cyclic aliases
            # - Unresolvable aliases
            # - Rust/PyO3 objects (KeyError)
            # - Submodules (which would cause recursive documentation issues)
            # - Any other edge case that would crash quartodoc build
            safe_exports = []
            failed_exports = {}  # name -> error type for reporting

            # Try to use quartodoc's `get_object()` for validation
            quartodoc_get_object = None
            try:
                from functools import partial

                from quartodoc import get_object as qd_get_object

                # quartodoc uses `parser="numpy"` by default which affects alias resolution
                quartodoc_get_object = partial(qd_get_object, dynamic=True, parser="numpy")
            except ImportError:
                pass

            # Try to import the actual package to detect modules
            actual_package = None
            try:
                import importlib

                actual_package = importlib.import_module(normalized_name)
            except ImportError:
                pass

            for name in filtered:
                # First check if this is a submodule; these should be excluded
                # because documenting them recursively documents all their members
                if actual_package is not None:
                    runtime_obj = getattr(actual_package, name, None)
                    if runtime_obj is not None:
                        import types

                        if isinstance(runtime_obj, types.ModuleType):
                            failed_exports[name] = "submodule (excluded from top-level docs)"
                            continue

                if quartodoc_get_object is not None:
                    try:
                        # Try to load the object exactly as quartodoc would
                        qd_obj = quartodoc_get_object(f"{normalized_name}:{name}")
                        # Try to access members to trigger any lazy resolution errors
                        _ = qd_obj.members
                        _ = qd_obj.kind
                        safe_exports.append(name)
                    except griffe.CyclicAliasError:
                        failed_exports[name] = "cyclic alias"
                    except griffe.AliasResolutionError:
                        failed_exports[name] = "unresolvable alias"
                    except KeyError:
                        failed_exports[name] = "not found (likely Rust/PyO3)"
                    except Exception as e:
                        # Catch-all for any other error that would crash quartodoc
                        failed_exports[name] = f"{type(e).__name__}"
                else:
                    # Fallback: use basic griffe check if quartodoc not available
                    try:
                        obj = pkg.members[name]
                        _ = obj.kind
                        _ = obj.members
                        safe_exports.append(name)
                    except Exception as e:
                        failed_exports[name] = f"{type(e).__name__}"

            # Report excluded items grouped by error type
            if failed_exports:
                # Group by error type for cleaner output
                by_error = {}
                for name, error in failed_exports.items():
                    by_error.setdefault(error, []).append(name)

                for error_type, names in sorted(by_error.items()):
                    print(
                        f"Excluding {len(names)} object(s) ({error_type}): "
                        f"{', '.join(sorted(names))}"
                    )

            return safe_exports

        except ImportError:
            print("Warning: griffe not available, cannot use dir() discovery")
            return None
        except Exception as e:
            print(f"Error discovering exports via dir(): {type(e).__name__}: {e}")
            return None

    def _get_package_exports(self, package_name: str) -> list | None:
        """
        Get package exports using the configured discovery method.

        By default, uses dir() to discover public objects. If `discovery_method`
        is set to "all" in [tool.great-docs], uses __all__ instead.

        Parameters
        ----------
        package_name
            The name of the package to get exports from.

        Returns
        -------
        list | None
            List of exported/public names, or None if discovery failed.
        """
        metadata = self._get_package_metadata()
        discovery_method = metadata.get("discovery_method", "dir")

        if discovery_method == "all":
            print("Using __all__ discovery method (configured in pyproject.toml)")
            return self._parse_package_exports(package_name)
        else:
            print("Using griffe introspection discovery method (default)")
            exports = self._discover_package_exports(package_name)
            if exports is None:
                print("Falling back to __all__ discovery method")
                return self._parse_package_exports(package_name)
            return exports

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

            # Try to use quartodoc's `get_object()` for validation
            quartodoc_get_object = None
            try:
                from functools import partial

                from quartodoc import get_object as qd_get_object

                quartodoc_get_object = partial(qd_get_object, dynamic=True, parser="numpy")
            except ImportError:
                pass

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
            cyclic_aliases = []

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
                    # Note: Accessing obj.kind or obj.members on an Alias can trigger
                    # resolution which may raise CyclicAliasError or AliasResolutionError
                    if obj.kind.value == "class":
                        categories["classes"].append(name)
                        # Get public methods (exclude private/magic methods)
                        # We need to handle each member individually to catch cyclic aliases
                        # AND validate each method with quartodoc to catch type hint issues
                        # Collect (method_name, lineno) tuples to preserve source order
                        method_entries = []
                        skipped_methods = []
                        try:
                            for member_name, member in obj.members.items():
                                if member_name.startswith("_"):
                                    continue
                                try:
                                    # Accessing member.kind can trigger alias resolution
                                    if member.kind.value in ("function", "method"):
                                        # Get line number for source ordering
                                        lineno = getattr(member, "lineno", float("inf"))
                                        # Validate with quartodoc if available
                                        if quartodoc_get_object is not None:
                                            try:
                                                qd_obj = quartodoc_get_object(
                                                    f"{normalized_name}:{name}.{member_name}"
                                                )
                                                # Try to access properties that might fail
                                                _ = qd_obj.members
                                                _ = qd_obj.kind
                                                method_entries.append((member_name, lineno))
                                            except Exception:
                                                # Method can't be documented by quartodoc
                                                skipped_methods.append(member_name)
                                        else:
                                            method_entries.append((member_name, lineno))
                                except (
                                    griffe.CyclicAliasError,
                                    griffe.AliasResolutionError,
                                ):
                                    # Skip cyclic/unresolvable class members
                                    skipped_methods.append(member_name)
                                except Exception:
                                    # Skip members that can't be introspected
                                    pass
                        except (griffe.CyclicAliasError, griffe.AliasResolutionError):
                            # If we can't even iterate members, class has issues
                            skipped_methods.append("<members>")

                        # Sort by line number to preserve source file order
                        method_entries.sort(key=lambda x: x[1])
                        method_names = [entry[0] for entry in method_entries]

                        if skipped_methods:
                            print(
                                f"  {name}: class with {len(method_names)} public methods "
                                f"(skipped {len(skipped_methods)} undocumentable method(s): "
                                f"{', '.join(skipped_methods[:3])}{'...' if len(skipped_methods) > 3 else ''})"
                            )
                        else:
                            print(f"  {name}: class with {len(method_names)} public methods")

                        categories["class_methods"][name] = len(method_names)
                        categories["class_method_names"][name] = method_names
                    elif obj.kind.value == "function":
                        categories["functions"].append(name)
                    else:
                        # Attributes, modules, etc.
                        categories["other"].append(name)

                except griffe.CyclicAliasError:
                    # Cyclic alias detected (e.g., re-exported symbol pointing to itself)
                    # This can happen with complex re-export patterns
                    # Do NOT add to categories (these must be excluded entirely)
                    print(f"  Warning: Cyclic alias detected for '{name}', excluding from docs")
                    cyclic_aliases.append(name)
                except griffe.AliasResolutionError:
                    # Alias could not be resolved (target not found)
                    # Do NOT add to categories (these must be excluded entirely)
                    print(f"  Warning: Could not resolve alias for '{name}', excluding from docs")
                    failed_introspection.append(name)
                except Exception as e:
                    # If introspection fails for a specific object, still include it
                    print(f"  Warning: Could not introspect '{name}': {type(e).__name__}")
                    categories["other"].append(name)
                    failed_introspection.append(name)

            if cyclic_aliases:
                print(f"Note: Excluded {len(cyclic_aliases)} cyclic alias(es) from documentation")

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

    def _create_quartodoc_sections(self, package_name: str) -> list | None:
        """
        Create quartodoc sections based on discovered package exports.

        Uses the configured discovery method (dir() by default, or __all__ if specified).

        Uses this heuristic (threshold is configurable via `large_class_method_threshold`):

        - classes with ≤N methods: documented inline (N defaults to 5)
        - classes with >N methods: separate pages for each method

        Parameters
        ----------
        package_name
            The name of the package.

        Returns
        -------
        list | None
            List of section dictionaries, or None if no sections could be created.
        """
        exports = self._get_package_exports(package_name)
        if not exports:
            return None

        # Filter out metadata variables at the export level too
        skip_names = {"__version__", "__author__", "__email__", "__all__"}
        exports = [e for e in exports if e not in skip_names]

        if not exports:
            return None

        print(f"Found {len(exports)} exported names to document")

        # Categorize the exports
        categories = self._categorize_api_objects(package_name, exports)

        sections = []

        # Get the method threshold from configuration (default: 5)
        metadata = self._get_package_metadata()
        method_threshold = metadata.get("large_class_method_threshold", 5)

        # Add classes section if there are any
        if categories["classes"]:
            class_contents = []
            classes_with_separate_methods = []

            for class_name in categories["classes"]:
                method_count = categories["class_methods"].get(class_name, 0)

                if method_count > method_threshold:
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

    def _extract_all_directives(self, package_name: str) -> dict:
        """
        Extract Great Docs directives from all docstrings in the package.

        Scans all exported classes, methods, and functions for @family, @order,
        @seealso, and @nodoc directives.

        Parameters
        ----------
        package_name
            The name of the package to scan.

        Returns
        -------
        dict
            Mapping of object names to their DocDirectives.
            Keys are either simple names (e.g., "MyClass") or qualified names
            (e.g., "MyClass.my_method").
        """
        from ._directives import extract_directives

        try:
            import griffe

            normalized_name = package_name.replace("-", "_")

            try:
                pkg = griffe.load(normalized_name)
            except Exception as e:
                print(f"Warning: Could not load package with griffe ({type(e).__name__})")
                return {}

            directive_map = {}

            # Use list() to materialize the iterator and catch any alias resolution errors
            try:
                members_list = list(pkg.members.items())
            except (griffe.CyclicAliasError, griffe.AliasResolutionError):
                # Some members have unresolvable aliases so try to iterate more carefully
                members_list = []
                for name in list(pkg.members.keys()):
                    try:
                        members_list.append((name, pkg.members[name]))
                    except Exception:
                        # Skip members that can't be accessed
                        continue
            except Exception:
                # Fall back to empty if we can't enumerate members at all
                return {}

            for name, obj in members_list:
                # Skip private members
                if name.startswith("_"):
                    continue

                # Skip aliases that can't be resolved (e.g., re-exports from external packages)
                try:
                    # Access kind to trigger alias resolution
                    _ = obj.kind
                except Exception:
                    # Silently skip unresolvable aliases since they're usually re-exports
                    # from external packages that wouldn't be documented anyway
                    continue

                # Extract directives from the object's docstring
                try:
                    if obj.docstring:
                        directives = extract_directives(obj.docstring.value)
                        if directives:
                            directive_map[name] = directives
                except Exception:
                    continue

                # For classes, also process methods
                try:
                    if obj.kind.value == "class":
                        for method_name, method in obj.members.items():
                            if method_name.startswith("_"):
                                continue
                            try:
                                if method.docstring:
                                    method_directives = extract_directives(method.docstring.value)
                                    if method_directives:
                                        directive_map[f"{name}.{method_name}"] = method_directives
                            except Exception:
                                continue
                except Exception:
                    # Skip if we can't introspect the class
                    pass

            return directive_map

        except ImportError:
            print("Warning: griffe not available for directive extraction")
            return {}

    def _get_family_config(self) -> dict:
        """
        Get family configuration from pyproject.toml.

        Returns
        -------
        dict
            Family configuration with titles, descriptions, and ordering.
        """
        metadata = self._get_package_metadata()
        return metadata.get("families", {})

    def _auto_title(self, family_name: str) -> str:
        """
        Generate a display title from a family name.

        Converts kebab-case or snake_case to Title Case.

        Parameters
        ----------
        family_name
            The family name (e.g., "family-name" or "family_name").

        Returns
        -------
        str
            Title-cased name (e.g., "Family Name").
        """
        # Replace hyphens and underscores with spaces, then title case
        return family_name.replace("-", " ").replace("_", " ").title()

    def _normalize_family_key(self, family_name: str) -> str:
        """
        Normalize a family name to a configuration key.

        Converts "Family Name" -> "family-name" for config lookup.

        Parameters
        ----------
        family_name
            The family name as written in the docstring.

        Returns
        -------
        str
            Normalized key for configuration lookup.
        """
        return family_name.lower().replace(" ", "-").replace("_", "-")

    def _create_quartodoc_sections_from_families(self, package_name: str) -> list | None:
        """
        Create quartodoc sections based on @family directives in docstrings.

        This method scans all docstrings for @family, @order, and @nodoc directives and generates
        organized sections. Items without @family directives are placed in auto-generated
        categories (Classes, Functions, Other).

        Parameters
        ----------
        package_name
            The name of the package.

        Returns
        -------
        list | None
            List of section dictionaries organized by family, or None if
            no exports found.
        """
        from ._directives import DocDirectives

        exports = self._get_package_exports(package_name)
        if not exports:
            return None

        # Filter out metadata variables
        skip_names = {"__version__", "__author__", "__email__", "__all__"}
        exports = [e for e in exports if e not in skip_names]

        if not exports:
            return None

        # Extract directives from all docstrings
        directive_map = self._extract_all_directives(package_name)

        # Get family configuration from pyproject.toml
        family_config = self._get_family_config()

        # Categorize exports for fallback (items without @family)
        categories = self._categorize_api_objects(package_name, exports)

        # Build family map: family_name -> list of items
        family_map: dict[str, list[dict]] = {}
        items_with_family: set[str] = set()
        excluded_items: set[str] = set()  # Track %nodoc items

        # Process top-level exports
        for item_name in exports:
            directives = directive_map.get(item_name, DocDirectives())

            # Skip items marked %nodoc
            if directives.nodoc:
                print(f"  Excluding '{item_name}' (%nodoc)")
                excluded_items.add(item_name)
                continue

            if directives.family:
                family = directives.family
                if family not in family_map:
                    family_map[family] = []

                # Determine if this is a class with methods
                is_class = item_name in categories.get("classes", [])
                method_count = categories.get("class_methods", {}).get(item_name, 0)

                family_map[family].append(
                    {
                        "name": item_name,
                        "order": directives.order if directives.order is not None else 999,
                        "seealso": directives.seealso,
                        "is_class": is_class,
                        "method_count": method_count,
                    }
                )
                items_with_family.add(item_name)

        # Process class methods that might have their own %family
        for class_name in categories.get("classes", []):
            method_names = categories.get("class_method_names", {}).get(class_name, [])
            for method_name in method_names:
                full_name = f"{class_name}.{method_name}"
                directives = directive_map.get(full_name, DocDirectives())

                if directives.nodoc:
                    excluded_items.add(full_name)
                    continue

                if directives.family:
                    family = directives.family
                    if family not in family_map:
                        family_map[family] = []

                    family_map[family].append(
                        {
                            "name": full_name,
                            "order": directives.order if directives.order is not None else 999,
                            "seealso": directives.seealso,
                            "is_class": False,
                            "method_count": 0,
                        }
                    )
                    items_with_family.add(full_name)

        # If no families found, fall back to default categorization
        if not family_map:
            print("No @family directives found, using default categorization")
            return self._create_quartodoc_sections(package_name)

        print(f"Found {len(family_map)} family group(s) from @family directives")

        # Build sections from families
        sections = []

        # Sort families by their configured order, then alphabetically
        def family_sort_key(family_name: str) -> tuple:
            config_key = self._normalize_family_key(family_name)
            config = family_config.get(config_key, {})
            order = config.get("order", 999)
            return (order, family_name.lower())

        sorted_families = sorted(family_map.keys(), key=family_sort_key)

        for family_name in sorted_families:
            items = family_map[family_name]

            # Sort items by order, then alphabetically
            items.sort(key=lambda x: (x["order"], x["name"].lower()))

            # Get display name and description from config
            config_key = self._normalize_family_key(family_name)
            config = family_config.get(config_key, {})
            title = config.get("title", family_name)  # Use family name as-is if no config
            desc = config.get("desc", "")

            # Format contents for quartodoc
            contents = []
            for item in items:
                name = item["name"]
                if item["is_class"] and item["method_count"] > 5:
                    # Large class: suppress inline method docs
                    contents.append({"name": name, "members": []})
                else:
                    contents.append(name)

            sections.append(
                {
                    "title": title,
                    "desc": desc,
                    "contents": contents,
                }
            )

            print(f"  {title}: {len(items)} item(s)")

        # Add items without %family to fallback sections
        # Exclude both items with families AND items marked %nodoc
        unassigned_classes = [
            c
            for c in categories.get("classes", [])
            if c not in items_with_family and c not in excluded_items
        ]
        unassigned_functions = [
            f
            for f in categories.get("functions", [])
            if f not in items_with_family and f not in excluded_items
        ]
        unassigned_other = [
            o
            for o in categories.get("other", [])
            if o not in items_with_family and o not in excluded_items
        ]

        if unassigned_classes:
            class_contents = []
            for class_name in unassigned_classes:
                method_count = categories.get("class_methods", {}).get(class_name, 0)
                if method_count > 5:
                    class_contents.append({"name": class_name, "members": []})
                else:
                    class_contents.append(class_name)

            sections.append(
                {
                    "title": "Classes",
                    "desc": "Core classes and types",
                    "contents": class_contents,
                }
            )
            print(f"  Classes (unassigned): {len(unassigned_classes)} item(s)")

        if unassigned_functions:
            sections.append(
                {
                    "title": "Functions",
                    "desc": "Public functions",
                    "contents": unassigned_functions,
                }
            )
            print(f"  Functions (unassigned): {len(unassigned_functions)} item(s)")

        if unassigned_other:
            sections.append(
                {
                    "title": "Other",
                    "desc": "Additional exports",
                    "contents": unassigned_other,
                }
            )
            print(f"  Other (unassigned): {len(unassigned_other)} item(s)")

        return sections if sections else None

    def _find_index_source_file(self) -> tuple[Path | None, list[str]]:
        """
        Find the best source file for index.qmd based on priority.

        Priority order (highest to lowest):
        1. index.qmd in project root
        2. index.md in project root
        3. README.md in project root

        Returns
        -------
        tuple[Path | None, list[str]]
            A tuple of (source_file_path, warnings_list).
            source_file_path is None if no suitable file is found.
        """
        package_root = self._find_package_root()
        warnings = []

        index_qmd_root = package_root / "index.qmd"
        index_md_root = package_root / "index.md"
        readme_path = package_root / "README.md"

        # Check which files exist
        has_index_qmd = index_qmd_root.exists()
        has_index_md = index_md_root.exists()
        has_readme = readme_path.exists()

        # Generate warnings for multiple source files
        if has_index_qmd and (has_index_md or has_readme):
            other_files = []
            if has_index_md:
                other_files.append("index.md")
            if has_readme:
                other_files.append("README.md")
            warnings.append(
                f"⚠️  Multiple index source files detected. Using index.qmd "
                f"(ignoring {', '.join(other_files)})"
            )
            return index_qmd_root, warnings

        if has_index_md and has_readme:
            warnings.append(
                "⚠️  Multiple index source files detected. Using index.md (ignoring README.md)"
            )
            return index_md_root, warnings

        # Return based on priority
        if has_index_qmd:
            return index_qmd_root, warnings
        if has_index_md:
            return index_md_root, warnings
        if has_readme:
            return readme_path, warnings

        return None, warnings

    def _create_index_from_readme(self, force_rebuild: bool = False) -> None:
        """
        Create or update index.qmd from the best available source file.

        Source file priority (highest to lowest):
        1. index.qmd in project root
        2. index.md in project root
        3. README.md in project root

        This mimics pkgdown's behavior of using the README as the homepage.
        Includes a metadata sidebar with package information (license, authors, links, etc.)

        Parameters
        ----------
        force_rebuild
            If `True`, always rebuild `index.qmd` even if it exists. Used by the build command to
            sync with source file changes.
        """
        package_root = self._find_package_root()

        # Always create license.qmd if LICENSE file exists
        license_path = package_root / "LICENSE"
        license_link = None
        if license_path.exists():
            license_qmd = self.project_path / "license.qmd"
            with open(license_path, "r", encoding="utf-8") as f:
                license_content = f.read()

            license_qmd_content = f"""---
title: "License"
---

```
{license_content}
```
"""
            with open(license_qmd, "w", encoding="utf-8") as f:
                f.write(license_qmd_content)
            print(f"Created {license_qmd}")
            license_link = "license.qmd"

        # Always create citation.qmd if CITATION.cff exists
        citation_path = package_root / "CITATION.cff"
        citation_link = None
        if citation_path.exists():
            citation_qmd = self.project_path / "citation.qmd"

            # Get metadata first to access rich_authors
            metadata = self._get_package_metadata()

            # Parse CITATION.cff for structured data
            import yaml

            with open(citation_path, "r", encoding="utf-8") as f:
                citation_data = yaml.safe_load(f)

            # Build Authors section
            authors_section = "## Authors\n\n"
            if citation_data.get("authors"):
                for author in citation_data["authors"]:
                    given = author.get("given-names", "")
                    family = author.get("family-names", "")
                    full_name = f"{given} {family}".strip()

                    # Get role from rich_authors if available
                    role = "Author"
                    if metadata.get("rich_authors"):
                        for rich_author in metadata["rich_authors"]:
                            if rich_author.get("name") == full_name:
                                role = rich_author.get("role", "Author")
                                break

                    authors_section += f"{full_name}. {role}.  \n"

            # Build Citation section with text and BibTeX
            citation_section = "## Citation\n\n"
            citation_section += "**Source:** `CITATION.cff`\n\n"

            # Generate text citation
            if citation_data.get("authors"):
                author_names = []
                for author in citation_data["authors"]:
                    family = author.get("family-names", "")
                    given = author.get("given-names", "")
                    initial = given[0] if given else ""
                    author_names.append(f"{family} {initial}" if initial else family)

                authors_str = ", ".join(author_names)
                title = citation_data.get("title", "")
                version = citation_data.get("version", "")
                url = citation_data.get("url", "")
                year = "2025"  # Could parse from date-released if available

                citation_section += (
                    f"{authors_str} ({year}). {title} Python package version {version}, {url}.\n\n"
                )

            # Generate BibTeX
            citation_section += "```bibtex\n"
            citation_section += "@Manual{,\n"

            if citation_data.get("title"):
                citation_section += f"  title = {{{citation_data['title']}}},\n"

            if citation_data.get("authors"):
                author_names = []
                for author in citation_data["authors"]:
                    given = author.get("given-names", "")
                    family = author.get("family-names", "")
                    full_name = f"{given} {family}".strip()
                    author_names.append(full_name)
                citation_section += f"  author = {{{' and '.join(author_names)}}},\n"

            citation_section += "  year = {2025},\n"

            if citation_data.get("version"):
                citation_section += (
                    f"  note = {{Python package version {citation_data['version']}}},\n"
                )

            if citation_data.get("url"):
                citation_section += f"  url = {{{citation_data['url']}}},\n"

            citation_section += "}\n```\n"

            citation_qmd_content = f"""---
title: "Authors and Citation"
---

{authors_section}

{citation_section}
"""
            with open(citation_qmd, "w", encoding="utf-8") as f:
                f.write(citation_qmd_content)
            print(f"Created {citation_qmd}")
            citation_link = "citation.qmd"

        # Now check if we should create index.qmd
        index_qmd = self.project_path / "index.qmd"

        if index_qmd.exists() and not force_rebuild:
            print("index.qmd already exists, skipping creation")
            return

        # Find the best source file
        source_file, warnings = self._find_index_source_file()

        # Print any warnings about multiple source files
        for warning in warnings:
            print(warning)

        if source_file is None:
            print(
                "No index source file found (index.qmd, index.md, or README.md), skipping index.qmd creation"
            )
            return

        source_name = source_file.name
        if force_rebuild:
            print(f"Rebuilding index.qmd from {source_name}...")
        else:
            print(f"Creating index.qmd from {source_name}...")

        # Read source content
        with open(source_file, "r", encoding="utf-8") as f:
            readme_content = f.read()

        # Adjust heading levels: bump all headings up by one level
        # This prevents h1 from becoming paragraphs and keeps proper hierarchy
        # Replace headings from highest to lowest level to avoid double-replacement
        import re

        readme_content = re.sub(r"^######\s+", r"####### ", readme_content, flags=re.MULTILINE)
        readme_content = re.sub(r"^#####\s+", r"###### ", readme_content, flags=re.MULTILINE)
        readme_content = re.sub(r"^####\s+", r"##### ", readme_content, flags=re.MULTILINE)
        readme_content = re.sub(r"^###\s+", r"#### ", readme_content, flags=re.MULTILINE)
        readme_content = re.sub(r"^##\s+", r"### ", readme_content, flags=re.MULTILINE)
        readme_content = re.sub(r"^#\s+", r"## ", readme_content, flags=re.MULTILINE)

        # Get package metadata for sidebar
        metadata = self._get_package_metadata()

        # Build margin content sections (right sidebar)
        margin_sections = []

        # Links section
        links_added = []

        # Try to add PyPI link based on package name
        package_name = self._detect_package_name()
        if package_name:
            pypi_url = f"https://pypi.org/project/{package_name}/"
            margin_sections.append("#### Links\n")
            margin_sections.append(f"[View on PyPI]({pypi_url})<br>")
            links_added.append("pypi")

        if metadata.get("urls"):
            if not links_added:
                margin_sections.append("#### Links\n")

            urls = metadata["urls"]

            # Map common URL names to display text
            url_map = {
                "homepage": None,  # Skip if we already added PyPI
                "repository": "Browse source code",
                "bug_tracker": "Report a bug",
                "documentation": None,  # Skip for that's the site we're on
            }

            for name, url in urls.items():
                name_lower = name.lower().replace(" ", "_")
                display_name = url_map.get(name_lower, name.replace("_", " ").title())

                # Skip if display_name is None (homepage/documentation)
                if display_name:
                    margin_sections.append(f"[{display_name}]({url})<br>")

        # Add llms.txt link at the end of Links section
        if links_added or metadata.get("urls"):
            margin_sections.append("[llms.txt](llms.txt)<br>")
        else:
            # If no links section exists yet, create one just for llms.txt
            margin_sections.append("#### Links\n")
            margin_sections.append("[llms.txt](llms.txt)<br>")

        # License section
        if license_link:
            margin_sections.append("\n#### License\n")
            margin_sections.append(f"[Full license]({license_link})<br>")
        elif metadata.get("license"):
            margin_sections.append("\n#### License\n")
            margin_sections.append(f"{metadata['license']}")

        # Community section: check for CONTRIBUTING.md and CODE_OF_CONDUCT.md
        community_items = []

        # Check for CONTRIBUTING.md in root or .github directory
        contributing_path = package_root / "CONTRIBUTING.md"
        if not contributing_path.exists():
            contributing_path = package_root / ".github" / "CONTRIBUTING.md"

        # Check for CODE_OF_CONDUCT.md in root or .github directory
        coc_path = package_root / "CODE_OF_CONDUCT.md"
        if not coc_path.exists():
            coc_path = package_root / ".github" / "CODE_OF_CONDUCT.md"

        if contributing_path.exists():
            community_items.append("[Contributing guide](contributing.qmd)<br>")
            # Create contributing.qmd
            with open(contributing_path, "r", encoding="utf-8") as f:
                contributing_content = f.read()

            # Strip first heading if it exists to avoid duplication with title
            lines = contributing_content.split("\n")
            if lines and lines[0].startswith("# "):
                contributing_content = "\n".join(lines[1:]).lstrip()

            contributing_qmd = self.project_path / "contributing.qmd"
            contributing_qmd_content = f"""---
title: "Contributing"
---

{contributing_content}
"""
            with open(contributing_qmd, "w", encoding="utf-8") as f:
                f.write(contributing_qmd_content)
            print(f"Created {contributing_qmd}")

        if coc_path.exists():
            community_items.append("[Code of conduct](code-of-conduct.qmd)<br>")
            # Create code-of-conduct.qmd
            with open(coc_path, "r", encoding="utf-8") as f:
                coc_content = f.read()

            # Strip first heading if it exists to avoid duplication with title
            lines = coc_content.split("\n")
            if lines and lines[0].startswith("# "):
                coc_content = "\n".join(lines[1:]).lstrip()

            coc_qmd = self.project_path / "code-of-conduct.qmd"
            coc_qmd_content = f"""---
title: "Code of Conduct"
---

{coc_content}
"""
            with open(coc_qmd, "w", encoding="utf-8") as f:
                f.write(coc_qmd_content)
            print(f"Created {coc_qmd}")

        if community_items:
            margin_sections.append("\n#### Community\n")
            margin_sections.extend(community_items)

        # Developers section (Authors)
        # Use rich author metadata if available, otherwise fall back to standard authors
        authors_to_display = metadata.get("rich_authors") or metadata.get("authors", [])

        if authors_to_display:
            margin_sections.append("\n#### Developers\n")

            # Try to extract GitHub username from repository URL as fallback
            fallback_github = None
            if metadata.get("urls"):
                repo_url = metadata["urls"].get("repository", "") or metadata["urls"].get(
                    "Repository", ""
                )
                if "github.com/" in repo_url:
                    # Extract username from URL like https://github.com/username/repo
                    parts = repo_url.rstrip("/").split("github.com/")
                    if len(parts) > 1:
                        username_part = parts[1].split("/")[0]
                        if username_part:
                            fallback_github = username_part

            for idx, author in enumerate(authors_to_display):
                if isinstance(author, dict):
                    name = author.get("name", "")
                    email = author.get("email", "")

                    # Rich metadata fields (from tool.great-docs.authors)
                    role = author.get("role", "")
                    affiliation = author.get("affiliation", "")
                    github = author.get("github", "")
                    homepage = author.get("homepage", "")
                    orcid = author.get("orcid", "")

                    # Build author line with name
                    author_parts = [f"**{name}**" if role else name]

                    # Add role/affiliation on separate lines if available
                    if role:
                        author_parts.append(f"<br><small>{role}</small>")
                    if affiliation:
                        author_parts.append(
                            f'<br><small style="margin-top: -0.15em; display: block;">{affiliation}</small>'
                        )

                    # Add icon links
                    icon_links = []

                    if email:
                        icon_links.append(
                            f'<a href="mailto:{email}" title="Email"><i class="bi bi-envelope-fill"></i></a>'
                        )

                    if github:
                        icon_links.append(
                            f'<a href="https://github.com/{github}" title="GitHub"><i class="bi bi-github"></i></a>'
                        )
                    elif fallback_github:
                        icon_links.append(
                            f'<a href="https://github.com/{fallback_github}" title="GitHub"><i class="bi bi-github"></i></a>'
                        )

                    if homepage:
                        icon_links.append(
                            f'<a href="{homepage}" title="Homepage"><i class="bi bi-house-fill"></i></a>'
                        )

                    if orcid:
                        # ORCID should be a full URL or just the ID
                        orcid_url = (
                            orcid if orcid.startswith("http") else f"https://orcid.org/{orcid}"
                        )
                        icon_links.append(
                            f'<a href="{orcid_url}" title="ORCID"><i class="fa-brands fa-orcid"></i></a>'
                        )

                    if icon_links:
                        author_parts.append(
                            '<span style="margin-top: -0.15em; display: block;">'
                            + " ".join(icon_links)
                            + "</span>"
                        )

                    # Wrap in <p> tag with padding for non-first authors
                    author_content = " ".join(author_parts)
                    if idx == 0:
                        margin_sections.append(f"<p>{author_content}</p>")
                    else:
                        margin_sections.append(
                            f'<p style="padding-top: 10px;">{author_content}</p>'
                        )

        # Meta section (Python version and extras)
        meta_items = []
        if metadata.get("requires_python"):
            meta_items.append(f"**Requires:** Python `{metadata['requires_python']}`")

        if metadata.get("optional_dependencies"):
            extras = list(metadata["optional_dependencies"].keys())
            if extras:
                # Wrap each extra in backticks for monospace
                extras_formatted = ", ".join(f"`{extra}`" for extra in extras)
                meta_items.append(f"**Provides-Extra:** {extras_formatted}")

        if meta_items:
            margin_sections.append("\n#### Meta\n")
            margin_sections.append("<br>\n".join(meta_items))

        # Citation section (if CITATION.cff exists)
        if citation_link:
            margin_sections.append("\n#### Citation\n")
            margin_sections.append(f"[Citing great-docs]({citation_link})")

        # Build margin content
        margin_content = "\n".join(margin_sections) if margin_sections else ""

        # CSS to reduce top margin of first heading element
        # The heading ends up inside a section.level1 > h1 structure
        first_heading_style = """<style>
section.level1:first-of-type > h1:first-child,
section.level2:first-of-type > h2:first-child,
.column-body-outset-right > section.level1:first-of-type > h1,
#quarto-document-content > section:first-of-type > h1 {
  margin-top: 4px !important;
}
</style>

"""

        # Create a qmd file with the README content
        # Use empty title so "Home" doesn't appear on landing page
        # Add margin content in a special div that Quarto will place in the margin
        if margin_content:
            qmd_content = f"""---
title: ""
toc: false
---

{first_heading_style}::: {{.column-margin}}
{margin_content}
:::

{readme_content}
"""
        else:
            qmd_content = f"""---
title: ""
toc: false
---

{first_heading_style}{readme_content}
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

        # Convert package name to importable form (hyphens -> underscores)
        importable_name = self._normalize_package_name(package_name)

        # Try to auto-generate sections from discovered exports
        # First try family-based organization (from @family directives)
        # Falls back to default categorization if no directives found
        sections = self._create_quartodoc_sections_from_families(importable_name)

        # Add quartodoc configuration with sensible defaults
        # Use the importable name (with underscores) for the package field
        quartodoc_config = {
            "package": importable_name,
            "dir": "reference",
            "title": "Reference",
            "style": "pkgdown",
            "dynamic": True,
            "renderer": {"style": "markdown", "table_style": "description-list"},
        }

        # Add sections if we found them
        if sections:
            quartodoc_config["sections"] = sections
            print(f"Auto-generated {len(sections)} section(s) from package exports")
        else:
            print("Could not auto-generate sections from package exports")
            print("You'll need to manually add sections to organize your API documentation.")

        config["quartodoc"] = quartodoc_config

        # Write back to file
        with open(quarto_yml, "w") as f:
            yaml.dump(config, f, default_flow_style=False, sort_keys=False)

        print(f"Added quartodoc configuration to {quarto_yml}")
        if not sections:
            print("See: https://machow.github.io/quartodoc/get-started/overview.html")

    def _refresh_quartodoc_config(self) -> None:
        """
        Refresh the quartodoc sections in _quarto.yml based on current package exports.

        This method re-discovers the package API and updates the quartodoc sections without touching
        other configuration. Use this when your package API has changed (new classes, methods, or
        functions added/removed).

        The method preserves:

        - package name and other quartodoc settings
        - all non-quartodoc configuration in _quarto.yml

        Only the 'sections' key in quartodoc config is regenerated.
        """
        quarto_yml = self.project_path / "_quarto.yml"

        if not quarto_yml.exists():
            print("Error: _quarto.yml not found. Run 'great-docs init' first.")
            return

        with open(quarto_yml, "r") as f:
            config = yaml.safe_load(f) or {}

        if "quartodoc" not in config:
            print("Error: No quartodoc configuration found. Run 'great-docs init' first.")
            return

        # Get the package name from existing config
        package_name = config["quartodoc"].get("package")
        if not package_name:
            print("Error: No package name in quartodoc config.")
            return

        print(f"Re-discovering exports for package: {package_name}")

        # Re-generate sections from current package exports
        # Uses family-based organization if @family directives are found
        sections = self._create_quartodoc_sections_from_families(package_name)

        if sections:
            config["quartodoc"]["sections"] = sections
            print(f"Updated quartodoc config with {len(sections)} section(s)")

            # Write back to file first, so sidebar update reads the new sections
            with open(quarto_yml, "w") as f:
                yaml.dump(config, f, default_flow_style=False, sort_keys=False)

            # Now update the sidebar to match the new sections
            self._update_sidebar_from_sections()

            print(f"✅ Refreshed quartodoc configuration in {quarto_yml}")
        else:
            print("Warning: Could not discover package exports. Config unchanged.")

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

        # Add resources to copy static JS files to _site
        if "resources" not in config["project"]:
            config["project"]["resources"] = []
        elif isinstance(config["project"]["resources"], str):
            config["project"]["resources"] = [config["project"]["resources"]]

        # Ensure JS files are included as resources
        for js_file in [
            "github-widget.js",
            "sidebar-filter.js",
            "dark-mode-toggle.js",
            "theme-init.js",
        ]:
            if js_file not in config["project"]["resources"]:
                config["project"]["resources"].append(js_file)

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

        # Add table of contents configuration for API reference navigation
        if "toc" not in config["format"]["html"]:
            config["format"]["html"]["toc"] = True
        if "toc-depth" not in config["format"]["html"]:
            config["format"]["html"]["toc-depth"] = 2
        if "toc-title" not in config["format"]["html"]:
            config["format"]["html"]["toc-title"] = "On this page"
        if "shift-heading-level-by" not in config["format"]["html"]:
            config["format"]["html"]["shift-heading-level-by"] = -1

        # Add Font Awesome for ORCID icon support
        if "include-in-header" not in config["format"]["html"]:
            config["format"]["html"]["include-in-header"] = []
        elif isinstance(config["format"]["html"]["include-in-header"], str):
            config["format"]["html"]["include-in-header"] = [
                config["format"]["html"]["include-in-header"]
            ]

        # Add Font Awesome CDN if not already present
        fa_cdn = '<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">'
        fa_entry = {"text": fa_cdn}
        if fa_entry not in config["format"]["html"]["include-in-header"]:
            # Check if any Font Awesome link already exists
            has_fa = any(
                "font-awesome" in str(item).lower()
                for item in config["format"]["html"]["include-in-header"]
            )
            if not has_fa:
                config["format"]["html"]["include-in-header"].append(fa_entry)

        # Add website navigation if not present
        if "website" not in config:
            config["website"] = {}

        # Enable page navigation for TOC
        if "page-navigation" not in config["website"]:
            config["website"]["page-navigation"] = True

        # Set title to package name if not already set
        if "title" not in config["website"]:
            package_name = self._detect_package_name()
            if package_name:
                config["website"]["title"] = package_name.title()

        # Get GitHub info and style preference
        owner, repo, repo_url = self._get_github_repo_info()
        metadata = self._get_package_metadata()
        github_style = metadata.get("github_style", "widget")  # "widget" or "icon"

        # Add or update navbar
        if "navbar" not in config["website"]:
            navbar_config = {
                "left": [
                    {"text": "Home", "href": "index.qmd"},
                    {"text": "Reference", "href": "reference/index.qmd"},
                ]
            }

            # Add GitHub link on the right if repository URL is available
            if owner and repo and repo_url and github_style == "widget":
                gh_widget_html = (
                    f'<div id="github-widget" data-owner="{owner}" data-repo="{repo}"></div>'
                )
                navbar_config["right"] = [{"text": gh_widget_html}]
            elif repo_url:
                navbar_config["right"] = [{"icon": "github", "href": repo_url}]

            config["website"]["navbar"] = navbar_config
        else:
            # Update existing navbar: upgrade icon to widget if configured
            self._update_navbar_github_link(config, owner, repo, repo_url, github_style)

        # Add GitHub widget script to page if using widget style
        if owner and repo and github_style == "widget":
            if "include-after-body" not in config["format"]["html"]:
                config["format"]["html"]["include-after-body"] = []
            elif isinstance(config["format"]["html"]["include-after-body"], str):
                config["format"]["html"]["include-after-body"] = [
                    config["format"]["html"]["include-after-body"]
                ]

            # Add the GitHub widget script
            gh_script_entry = {"text": '<script src="github-widget.js"></script>'}
            if gh_script_entry not in config["format"]["html"]["include-after-body"]:
                # Check if github-widget.js is already included
                has_gh_widget = any(
                    "github-widget" in str(item)
                    for item in config["format"]["html"]["include-after-body"]
                )
                if not has_gh_widget:
                    config["format"]["html"]["include-after-body"].append(gh_script_entry)

        # Add sidebar filter script if enabled
        if metadata.get("sidebar_filter_enabled", True):
            if "include-after-body" not in config["format"]["html"]:
                config["format"]["html"]["include-after-body"] = []
            elif isinstance(config["format"]["html"]["include-after-body"], str):
                config["format"]["html"]["include-after-body"] = [
                    config["format"]["html"]["include-after-body"]
                ]

            # Add the sidebar filter script
            filter_script_entry = {"text": '<script src="sidebar-filter.js"></script>'}
            has_filter = any(
                "sidebar-filter" in str(item)
                for item in config["format"]["html"]["include-after-body"]
            )
            if not has_filter:
                config["format"]["html"]["include-after-body"].append(filter_script_entry)

            # Add data attributes for configuration (must be before sidebar-filter.js)
            min_items = metadata.get("sidebar_filter_min_items", 20)
            if min_items != 20:
                # Add custom min_items via body data attribute and insert BEFORE the filter script
                min_items_script = {
                    "text": f'<script>document.body.dataset.sidebarFilterMinItems = "{min_items}";</script>'
                }
                has_min_items = any(
                    "sidebarFilterMinItems" in str(item)
                    for item in config["format"]["html"]["include-after-body"]
                )
                if not has_min_items:
                    # Insert before the sidebar-filter.js script
                    filter_index = next(
                        (
                            i
                            for i, item in enumerate(config["format"]["html"]["include-after-body"])
                            if "sidebar-filter" in str(item)
                        ),
                        len(config["format"]["html"]["include-after-body"]),
                    )
                    config["format"]["html"]["include-after-body"].insert(
                        filter_index, min_items_script
                    )

        # Add dark mode toggle script (if enabled)
        dark_mode_enabled = metadata.get("dark_mode_toggle_enabled", True)
        if dark_mode_enabled:
            if "include-after-body" not in config["format"]["html"]:
                config["format"]["html"]["include-after-body"] = []
            elif isinstance(config["format"]["html"]["include-after-body"], str):
                config["format"]["html"]["include-after-body"] = [
                    config["format"]["html"]["include-after-body"]
                ]

            dark_mode_script_entry = {"text": '<script src="dark-mode-toggle.js"></script>'}
            has_dark_mode = any(
                "dark-mode-toggle" in str(item)
                for item in config["format"]["html"]["include-after-body"]
            )
            if not has_dark_mode:
                config["format"]["html"]["include-after-body"].append(dark_mode_script_entry)

            # Add early theme detection script in header to prevent flash of wrong theme
            if "include-in-header" not in config["format"]["html"]:
                config["format"]["html"]["include-in-header"] = []
            elif isinstance(config["format"]["html"]["include-in-header"], str):
                config["format"]["html"]["include-in-header"] = [
                    config["format"]["html"]["include-in-header"]
                ]

            # Reference external script file for early theme detection (cleaner YAML)
            early_theme_script = {"text": '<script src="theme-init.js"></script>'}
            has_early_theme = any(
                "theme-init" in str(item) for item in config["format"]["html"]["include-in-header"]
            )
            if not has_early_theme:
                config["format"]["html"]["include-in-header"].append(early_theme_script)

        # Add sidebar navigation for reference pages
        if "sidebar" not in config["website"]:
            config["website"]["sidebar"] = [
                {
                    "id": "reference",
                    "contents": "reference/",
                }
            ]

        # Add page footer with copyright notice if not present
        if "page-footer" not in config["website"]:
            import datetime

            current_year = datetime.datetime.now().year
            metadata = self._get_package_metadata()

            # Get author name from metadata
            author_name = None
            if metadata.get("authors"):
                first_author = metadata["authors"][0]
                if isinstance(first_author, dict):
                    author_name = first_author.get("name")
                elif isinstance(first_author, str):
                    author_name = first_author

            if author_name:
                config["website"]["page-footer"] = {"left": f"&copy; {current_year} {author_name}"}

        # Write back to file
        with open(quarto_yml, "w") as f:
            yaml.dump(config, f, default_flow_style=False, sort_keys=False)

        print(f"Updated {quarto_yml} with great-docs configuration")

    def _update_sidebar_from_sections(self) -> None:
        """
        Update sidebar navigation based on quartodoc sections.

        Builds a structured sidebar with sections and their contents, and excludes the index page
        from showing the sidebar.
        """
        quarto_yml = self.project_path / "_quarto.yml"

        if not quarto_yml.exists():
            return

        with open(quarto_yml, "r") as f:
            config = yaml.safe_load(f) or {}

        # Get quartodoc sections if they exist
        if "quartodoc" not in config or "sections" not in config["quartodoc"]:
            return

        sections = config["quartodoc"]["sections"]
        sidebar_contents = []

        # Build sidebar structure from sections
        for section in sections:
            section_entry = {"section": section["title"], "contents": []}

            # Add each item in the section
            for item in section.get("contents", []):
                # Handle both string and dict formats
                if isinstance(item, str):
                    section_entry["contents"].append(f"reference/{item}.qmd")
                elif isinstance(item, dict):
                    # Extract the name from dict format (e.g., {'name': 'Graph', 'members': []})
                    item_name = item.get("name", str(item))
                    section_entry["contents"].append(f"reference/{item_name}.qmd")
                else:
                    # Fallback for unexpected types
                    section_entry["contents"].append(f"reference/{item}.qmd")

            sidebar_contents.append(section_entry)

        # Update sidebar configuration
        if "website" not in config:
            config["website"] = {}

        # Build sidebar with API link at top (not subject to filtering)
        # followed by the sectioned contents
        full_contents = [
            {"text": "API", "href": "reference/index.qmd"},
        ] + sidebar_contents

        config["website"]["sidebar"] = [
            {
                "id": "reference",
                "contents": full_contents,
            }
        ]

        # Write back
        with open(quarto_yml, "w") as f:
            yaml.dump(config, f, default_flow_style=False, sort_keys=False)

    def _update_reference_index_frontmatter(self) -> None:
        """Ensure reference/index.qmd has proper frontmatter."""
        index_path = self.docs_dir / "reference" / "index.qmd"

        if not index_path.exists():
            return

        # Read the current content
        with open(index_path, "r") as f:
            content = f.read()

        # Check if frontmatter already exists; if so, leave it as is
        if content.startswith("---"):
            return

        # Add minimal frontmatter if none exists
        content = f"---\n---\n\n{content}"

        # Write updated content
        with open(index_path, "w") as f:
            f.write(content)

    def _generate_llms_txt(self) -> None:
        """
        Generate an llms.txt file for LLM documentation indexing.

        Creates a structured markdown file that indexes the API reference pages, following the
        llms.txt standard format for LLM-readable documentation. The file is saved to the docs
        directory and will be included in the built site.

        The format follows the structure:

        - package title with description
        - API Reference section with links to each documented item
        """
        quarto_yml = self.project_path / "_quarto.yml"

        if not quarto_yml.exists():
            return

        with open(quarto_yml, "r") as f:
            config = yaml.safe_load(f) or {}

        # Get quartodoc sections and package info
        if "quartodoc" not in config:
            return

        quartodoc_config = config["quartodoc"]
        sections = quartodoc_config.get("sections", [])
        package_name = quartodoc_config.get("package")

        if not package_name or not sections:
            return

        # Get package metadata for description and site URL
        metadata = self._get_package_metadata()
        description = metadata.get("description", "")

        # Get the site URL and prefer the Documentation URL from pyproject.toml,
        # fall back to site-url from _quarto.yml
        urls = metadata.get("urls", {})
        site_url = urls.get("Documentation", "") or config.get("website", {}).get("site-url", "")

        # Clean up site URL and remove any trailing anchors or paths that aren't the base
        if site_url:
            # Remove trailing #readme or similar anchors
            if "#" in site_url:
                site_url = site_url.split("#")[0]
            # Ensure trailing slash
            if not site_url.endswith("/"):
                site_url += "/"

        # Build the llms.txt content
        lines = []

        # Header with package name
        lines.append(f"# {package_name}")
        lines.append("")

        # Description
        if description:
            lines.append(f"> {description}")
            lines.append("")

        # API Reference section
        lines.append("## Docs")
        lines.append("")
        lines.append("### API Reference")
        lines.append("")

        # Process each section
        for section in sections:
            section_title = section.get("title", "")
            section_desc = section.get("desc", "")

            # Add section header as a comment or sub-heading if there are multiple sections
            if len(sections) > 1 and section_title:
                lines.append(f"#### {section_title}")
                if section_desc:
                    lines.append(f"> {section_desc}")
                lines.append("")

            # Add each item in the section
            for item in section.get("contents", []):
                # Handle both string and dict formats
                if isinstance(item, str):
                    item_name = item
                    item_desc = ""
                elif isinstance(item, dict):
                    item_name = item.get("name", str(item))
                    item_desc = ""
                else:
                    continue

                # Get description from docstring if available
                if not item_desc:
                    item_desc = self._get_docstring_summary(package_name, item_name)

                # Build the URL
                if site_url:
                    url = f"{site_url}reference/{item_name}.html"
                else:
                    url = f"reference/{item_name}.html"

                # Format the line
                if item_desc:
                    lines.append(f"- [{item_name}]({url}): {item_desc}")
                else:
                    lines.append(f"- [{item_name}]({url})")

            lines.append("")

        # Write the llms.txt file
        llms_txt_path = self.project_path / "llms.txt"
        with open(llms_txt_path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))

        print(f"Created {llms_txt_path}")

    def _get_docstring_summary(self, package_name: str, item_name: str) -> str:
        """
        Get the first line of a docstring for an item.

        Parameters
        ----------
        package_name
            The name of the package containing the item.
        item_name
            The name of the class, function, or module to get the docstring for.

        Returns
        -------
        str
            The first line of the docstring, or empty string if not available.
        """
        try:
            import importlib

            # Normalize package name
            normalized_name = package_name.replace("-", "_")
            module = importlib.import_module(normalized_name)

            # Try to get the object
            obj = getattr(module, item_name, None)
            if obj is None:
                return ""

            # Get docstring
            docstring = getattr(obj, "__doc__", None)
            if not docstring:
                return ""

            # Extract first line/sentence
            first_line = docstring.strip().split("\n")[0].strip()

            # Clean up the line (remove trailing periods, normalize whitespace)
            first_line = first_line.rstrip(".")

            return first_line

        except Exception:
            return ""

    def uninstall(self) -> None:
        """
        Remove great-docs assets and configuration from the project.

        This method deletes the great-docs CSS file and post-render script, and cleans up the
        `_quarto.yml` configuration file by removing great-docs-specific settings.

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
        """
        print("Uninstalling great-docs from your quartodoc project...")
        print(f"Removing from: {self.project_path.relative_to(self.project_root)}")

        # Remove files
        files_to_remove = [
            self.project_path / "scripts" / "post-render.py",
            self.project_path / "great-docs.css",
            self.project_path / ".gitignore",
        ]

        for file_path in files_to_remove:
            if file_path.exists():
                # For .gitignore, only remove if it matches our template exactly
                if file_path.name == ".gitignore":
                    with open(file_path, "r") as f:
                        content = f.read()
                    # Only remove if it's purely our .gitignore (starts with our comment)
                    if content.strip().startswith("# Quarto build output"):
                        file_path.unlink()
                        print(f"Removed {file_path}")
                    else:
                        print(f"Skipping {file_path} (contains user modifications)")
                else:
                    file_path.unlink()
                    print(f"Removed {file_path}")

        # Clean up _quarto.yml
        self._clean_quarto_config()

        print("✅ Great-docs uninstalled successfully!")

    def _clean_quarto_config(self) -> None:
        """
        Remove great-docs configuration from _quarto.yml.

        This private method removes the post-render script reference and CSS file entry from the
        Quarto configuration file, reverting it to its pre-installation state while preserving other
        user settings.
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

    def build(self, watch: bool = False, refresh: bool = True) -> None:
        """
        Build the documentation site.

        Runs `quartodoc build` followed by `quarto render`. By default, re-discovers package exports
        and updates the quartodoc configuration before building.

        Parameters
        ----------
        watch
            If `True`, watch for changes and rebuild automatically.
        refresh
            If `True` (default), re-discover package exports and update quartodoc config before
            building. Set to False for faster rebuilds when your package API hasn't changed.

        Examples
        --------
        Build the documentation (with API refresh):

        ```python
        from great_docs import GreatDocs

        docs = GreatDocs()
        docs.build()
        ```

        Build with watch mode:

        ```python
        docs.build(watch=True)
        ```

        Quick rebuild without API refresh:

        ```python
        docs.build(refresh=False)
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

            # Ensure latest CSS and post-render script from package assets are in place
            css_src = self.assets_path / "great-docs.css"
            css_dst = self.project_path / "great-docs.css"
            if css_src.exists():
                shutil.copy2(css_src, css_dst)

            scripts_dir = self.project_path / "scripts"
            scripts_dir.mkdir(exist_ok=True)
            post_render_src = self.assets_path / "post-render.py"
            post_render_dst = scripts_dir / "post-render.py"
            if post_render_src.exists():
                shutil.copy2(post_render_src, post_render_dst)

            # Ensure GitHub widget JS is in place
            gh_widget_src = self.assets_path / "github-widget.js"
            gh_widget_dst = self.project_path / "github-widget.js"
            if gh_widget_src.exists():
                shutil.copy2(gh_widget_src, gh_widget_dst)

            # Ensure sidebar filter JS is in place
            sidebar_filter_src = self.assets_path / "sidebar-filter.js"
            sidebar_filter_dst = self.project_path / "sidebar-filter.js"
            if sidebar_filter_src.exists():
                shutil.copy2(sidebar_filter_src, sidebar_filter_dst)

            # Ensure reference switcher JS is in place (for CLI docs)
            ref_switcher_src = self.assets_path / "reference-switcher.js"
            ref_switcher_dst = self.project_path / "reference-switcher.js"
            if ref_switcher_src.exists():
                shutil.copy2(ref_switcher_src, ref_switcher_dst)

            # Update navbar to use GitHub widget (if configured)
            quarto_yml = self.project_path / "_quarto.yml"
            if quarto_yml.exists():
                with open(quarto_yml) as f:
                    config = yaml.safe_load(f)

                owner, repo, repo_url = self._get_github_repo_info()
                metadata = self._get_package_metadata()
                github_style = metadata.get("github_style", "widget")

                if config and "website" in config and "navbar" in config["website"]:
                    self._update_navbar_github_link(config, owner, repo, repo_url, github_style)

                    # Also ensure the GitHub widget script is included
                    if owner and repo and github_style == "widget":
                        if "format" not in config:
                            config["format"] = {"html": {}}
                        if "html" not in config["format"]:
                            config["format"]["html"] = {}
                        if "include-after-body" not in config["format"]["html"]:
                            config["format"]["html"]["include-after-body"] = []
                        elif isinstance(config["format"]["html"]["include-after-body"], str):
                            config["format"]["html"]["include-after-body"] = [
                                config["format"]["html"]["include-after-body"]
                            ]

                        gh_script_entry = {"text": '<script src="github-widget.js"></script>'}
                        has_gh_widget = any(
                            "github-widget" in str(item)
                            for item in config["format"]["html"]["include-after-body"]
                        )
                        if not has_gh_widget:
                            config["format"]["html"]["include-after-body"].append(gh_script_entry)

                # Add sidebar filter script if enabled
                if metadata.get("sidebar_filter_enabled", True):
                    if "format" not in config:
                        config["format"] = {"html": {}}
                    if "html" not in config["format"]:
                        config["format"]["html"] = {}
                    if "include-after-body" not in config["format"]["html"]:
                        config["format"]["html"]["include-after-body"] = []
                    elif isinstance(config["format"]["html"]["include-after-body"], str):
                        config["format"]["html"]["include-after-body"] = [
                            config["format"]["html"]["include-after-body"]
                        ]

                    filter_script_entry = {"text": '<script src="sidebar-filter.js"></script>'}
                    has_filter = any(
                        "sidebar-filter" in str(item)
                        for item in config["format"]["html"]["include-after-body"]
                    )
                    if not has_filter:
                        config["format"]["html"]["include-after-body"].append(filter_script_entry)

                    # Add min_items configuration if different from default
                    min_items = metadata.get("sidebar_filter_min_items", 20)
                    if min_items != 20:
                        min_items_script = {
                            "text": f'<script>document.body.dataset.sidebarFilterMinItems = "{min_items}";</script>'
                        }
                        has_min_items = any(
                            "sidebarFilterMinItems" in str(item)
                            for item in config["format"]["html"]["include-after-body"]
                        )
                        if not has_min_items:
                            # Insert before the sidebar-filter.js script
                            filter_index = next(
                                (
                                    i
                                    for i, item in enumerate(
                                        config["format"]["html"]["include-after-body"]
                                    )
                                    if "sidebar-filter" in str(item)
                                ),
                                len(config["format"]["html"]["include-after-body"]),
                            )
                            config["format"]["html"]["include-after-body"].insert(
                                filter_index, min_items_script
                            )

                # Add resources to copy static JS files to _site
                if "project" not in config:
                    config["project"] = {}
                if "resources" not in config["project"]:
                    config["project"]["resources"] = []
                elif isinstance(config["project"]["resources"], str):
                    config["project"]["resources"] = [config["project"]["resources"]]

                for js_file in [
                    "github-widget.js",
                    "sidebar-filter.js",
                    "reference-switcher.js",
                    "dark-mode-toggle.js",
                    "theme-init.js",
                ]:
                    if js_file not in config["project"]["resources"]:
                        config["project"]["resources"].append(js_file)

                # Add reference switcher script if CLI documentation is enabled
                if metadata.get("cli_enabled", False):
                    ref_switcher_entry = {"text": '<script src="reference-switcher.js"></script>'}
                    has_ref_switcher = any(
                        "reference-switcher" in str(item)
                        for item in config["format"]["html"]["include-after-body"]
                    )
                    if not has_ref_switcher:
                        config["format"]["html"]["include-after-body"].append(ref_switcher_entry)

                with open(quarto_yml, "w") as f:
                    yaml.dump(config, f, default_flow_style=False, sort_keys=False)

            # Step 0: Rebuild index.qmd from source file (README.md, index.md, or index.qmd)
            print("\n📄 Step 0: Syncing landing page with source file...")
            self._create_index_from_readme(force_rebuild=True)

            # Step 0.5: Refresh quartodoc config if requested
            if refresh:
                print("\n🔄 Refreshing quartodoc configuration...")
                self._refresh_quartodoc_config()

            # Step 0.6: Generate llms.txt file
            print("\n📝 Generating llms.txt...")
            self._generate_llms_txt()

            # Step 0.7: Generate source links JSON
            print("\n🔗 Generating source links...")
            package_name = self._detect_package_name()
            if package_name:
                self._generate_source_links_json(package_name)

            # Step 0.8: Generate CLI documentation if enabled
            metadata = self._get_package_metadata()
            if metadata.get("cli_enabled", False):
                print("\n🖥️  Generating CLI reference...")
                try:
                    cli_info = self._discover_click_cli(package_name)
                    if cli_info:
                        cli_files = self._generate_cli_reference_pages(cli_info)
                        if cli_files:
                            self._update_sidebar_with_cli(cli_files)
                            print(f"✅ Generated {len(cli_files)} CLI reference page(s)")
                    else:
                        print("   No Click CLI found or CLI documentation disabled")
                except Exception as e:
                    print(f"   ⚠️  Error generating CLI documentation: {e}")
                    import traceback

                    traceback.print_exc()

            # Step 0.9: Process User Guide if present
            try:
                self._process_user_guide()
            except Exception as e:
                print(f"   ⚠️  Error processing User Guide: {e}")
                import traceback

                traceback.print_exc()

            # Step 1: Run quartodoc build using Python module execution
            # This ensures it uses the same Python environment as great-docs
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
                # Check if quartodoc is not installed
                if "No module named quartodoc" in result.stderr:
                    print("\n⚠️  quartodoc is not installed in your environment.")
                    print("\nTo fix this, install quartodoc:")
                    print(f"  {sys.executable} -m pip install quartodoc")
                    print("\nOr if using pip directly:")
                    print("  pip install quartodoc")
                else:
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
        import sys

        print("Building and previewing documentation...")

        # Change to docs directory
        original_dir = os.getcwd()
        try:
            os.chdir(self.project_path)

            # Step 1: Run quartodoc build
            print("\n📚 Step 1: Generating API reference with quartodoc...")
            result = subprocess.run(
                [sys.executable, "-m", "quartodoc", "build"], capture_output=True, text=True
            )

            if result.returncode != 0:
                print("❌ quartodoc build failed:")
                # Check if quartodoc is not installed
                if "No module named quartodoc" in result.stderr:
                    print("\n⚠️  quartodoc is not installed in your environment.")
                    print("\nTo fix this, install quartodoc:")
                    print(f"  {sys.executable} -m pip install quartodoc")
                    print("\nOr if using pip directly:")
                    print("  pip install quartodoc")
                else:
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

    def check_links(
        self,
        include_source: bool = True,
        include_docs: bool = True,
        timeout: float = 10.0,
        ignore_patterns: list[str] | None = None,
        verbose: bool = False,
    ) -> dict:
        """
        Check all links in source code and documentation for broken links.

        This method scans Python source files and documentation files (`.qmd`, `.md`)
        for URLs and checks their HTTP status. It reports broken links (404s) and
        warns about redirects.

        In `.qmd` files, you can exclude specific URLs from checking by adding
        `{.gd-no-link}` immediately after the URL::

            Visit http://example.com{.gd-no-link} for an example.

        Parameters
        ----------
        include_source
            If `True`, scan Python source files in the package directory for URLs.
            Default is `True`.
        include_docs
            If `True`, scan documentation files (`.qmd`, `.md`) for URLs.
            Default is `True`.
        timeout
            Timeout in seconds for each HTTP request. Default is `10.0`.
        ignore_patterns
            List of URL patterns (strings or regex) to ignore. URLs matching any
            pattern will be skipped. Default is `None`.
        verbose
            If `True`, print detailed progress information. Default is `False`.

        Returns
        -------
        dict
            A dictionary containing:
            - `total`: Total number of unique links checked
            - `ok`: List of links that returned 2xx status
            - `redirects`: List of dicts with `url`, `status`, `location` for 3xx responses
            - `broken`: List of dicts with `url`, `status`, `error` for 4xx/5xx or errors
            - `skipped`: List of URLs that were skipped (matched ignore patterns)
            - `by_file`: Dict mapping file paths to lists of links found in each file

        Examples
        --------
        Check all links in a project:

        ```python
        from great_docs import GreatDocs

        docs = GreatDocs()
        results = docs.check_links()

        print(f"Checked {results['total']} links")
        print(f"Broken: {len(results['broken'])}")
        print(f"Redirects: {len(results['redirects'])}")
        ```

        Check only documentation files with custom timeout:

        ```python
        results = docs.check_links(
            include_source=False,
            timeout=5.0,
            ignore_patterns=["localhost", "127.0.0.1", "example.com"]
        )
        ```
        """
        import requests

        # URL regex pattern - matches http and https URLs
        url_pattern = re.compile(
            r'https?://[^\s<>"\')\]}`\\]+',
            re.IGNORECASE,
        )

        # Pattern to detect URLs marked with {.gd-no-link} in .qmd files
        # This allows marking example/fake links for exclusion: http://example.com{.gd-no-link}
        gd_no_link_pattern = re.compile(
            r'(https?://[^\s<>"\')\]}`\\{]+)\{\.gd-no-link\}',
            re.IGNORECASE,
        )

        # Compile ignore patterns
        ignore_regexes = []
        if ignore_patterns:
            for pattern in ignore_patterns:
                try:
                    ignore_regexes.append(re.compile(pattern, re.IGNORECASE))
                except re.error:
                    # Treat as literal string if not valid regex
                    ignore_regexes.append(re.compile(re.escape(pattern), re.IGNORECASE))

        # Collect all files to scan
        files_to_scan: list[Path] = []

        if include_source:
            # Find package directory
            package_name = self._detect_package_name()
            if package_name:
                package_dir = self.project_root / package_name.replace("-", "_")
                if package_dir.exists():
                    files_to_scan.extend(package_dir.rglob("*.py"))

        if include_docs:
            # Scan docs directory
            if self.project_path.exists():
                files_to_scan.extend(self.project_path.rglob("*.qmd"))
                files_to_scan.extend(self.project_path.rglob("*.md"))

            # Also check README in project root
            readme = self.project_root / "README.md"
            if readme.exists():
                files_to_scan.append(readme)

        # Extract URLs from all files
        url_to_files: dict[str, list[str]] = {}
        by_file: dict[str, list[str]] = {}

        for file_path in files_to_scan:
            try:
                content = file_path.read_text(encoding="utf-8", errors="ignore")

                # For .qmd files, find URLs marked with {.gd-no-link} and exclude them
                excluded_urls: set[str] = set()
                if file_path.suffix == ".qmd":
                    for match in gd_no_link_pattern.finditer(content):
                        excluded_urls.add(match.group(1))

                urls = url_pattern.findall(content)

                # Clean URLs (remove trailing punctuation)
                cleaned_urls = []
                for url in urls:
                    # Remove trailing punctuation that's likely not part of the URL
                    url = url.rstrip(".,;:!?")
                    # Remove trailing parentheses if unbalanced
                    while url.endswith(")") and url.count(")") > url.count("("):
                        url = url[:-1]
                    # Skip URLs with f-string placeholders (e.g., {variable} or partial {var)
                    # This catches both complete {var} and incomplete {var patterns
                    if "{" in url:
                        continue
                    # Skip URLs marked with {.gd-no-link}
                    if url in excluded_urls:
                        continue
                    cleaned_urls.append(url)

                if cleaned_urls:
                    rel_path = str(file_path.relative_to(self.project_root))
                    by_file[rel_path] = cleaned_urls

                    for url in cleaned_urls:
                        if url not in url_to_files:
                            url_to_files[url] = []
                        url_to_files[url].append(rel_path)

            except Exception as e:
                if verbose:
                    print(f"Warning: Could not read {file_path}: {e}")

        # Check each unique URL
        results = {
            "total": len(url_to_files),
            "ok": [],
            "redirects": [],
            "broken": [],
            "skipped": [],
            "by_file": by_file,
        }

        if verbose:
            print(f"\n🔍 Found {len(url_to_files)} unique URLs to check\n")

        for url in url_to_files:
            # Check if URL matches any ignore pattern
            should_skip = False
            for pattern in ignore_regexes:
                if pattern.search(url):
                    should_skip = True
                    break

            if should_skip:
                results["skipped"].append(url)
                if verbose:
                    print(f"⏭️  Skipped: {url}")
                continue

            try:
                # Use HEAD request first (faster), fall back to GET if needed
                response = requests.head(
                    url,
                    timeout=timeout,
                    allow_redirects=False,
                    headers={"User-Agent": "great-docs-link-checker/1.0"},
                )

                # Some servers don't support HEAD, try GET
                if response.status_code == 405:
                    response = requests.get(
                        url,
                        timeout=timeout,
                        allow_redirects=False,
                        headers={"User-Agent": "great-docs-link-checker/1.0"},
                        stream=True,  # Don't download body
                    )
                    response.close()

                status = response.status_code

                if 200 <= status < 300:
                    results["ok"].append(url)
                    if verbose:
                        print(f"✅ {status} {url}")
                elif 300 <= status < 400:
                    location = response.headers.get("Location", "Unknown")
                    results["redirects"].append(
                        {
                            "url": url,
                            "status": status,
                            "location": location,
                            "files": url_to_files[url],
                        }
                    )
                    if verbose:
                        print(f"↪️  {status} {url} -> {location}")
                else:
                    results["broken"].append(
                        {
                            "url": url,
                            "status": status,
                            "error": f"HTTP {status}",
                            "files": url_to_files[url],
                        }
                    )
                    if verbose:
                        print(f"❌ {status} {url}")

            except requests.exceptions.Timeout:
                results["broken"].append(
                    {
                        "url": url,
                        "status": None,
                        "error": "Timeout",
                        "files": url_to_files[url],
                    }
                )
                if verbose:
                    print(f"⏱️  Timeout: {url}")
            except requests.exceptions.SSLError as e:
                results["broken"].append(
                    {
                        "url": url,
                        "status": None,
                        "error": f"SSL Error: {str(e)[:50]}",
                        "files": url_to_files[url],
                    }
                )
                if verbose:
                    print(f"🔐 SSL Error: {url}")
            except requests.exceptions.ConnectionError:
                results["broken"].append(
                    {
                        "url": url,
                        "status": None,
                        "error": "Connection failed",
                        "files": url_to_files[url],
                    }
                )
                if verbose:
                    print(f"🔌 Connection failed: {url}")
            except Exception as e:
                results["broken"].append(
                    {
                        "url": url,
                        "status": None,
                        "error": str(e)[:100],
                        "files": url_to_files[url],
                    }
                )
                if verbose:
                    print(f"⚠️  Error: {url} - {e}")

        return results

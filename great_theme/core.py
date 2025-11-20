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

    def install(self, force: bool = False) -> None:
        """
        Install great-theme assets and configuration to the project.

        This method copies the necessary CSS files and post-render script to your Quarto project
        directory, and automatically updates your `_quarto.yml` configuration file to use the
        great-theme styling.

        Parameters
        ----------
        force
            If True, overwrite existing files without prompting. Default is False.

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

        print("\nGreat-theme installation complete!")
        print("\nNext steps:")
        print("1. Run `quarto render` to build your site with the new theme")
        print("2. The theme will automatically enhance your quartodoc reference pages")

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

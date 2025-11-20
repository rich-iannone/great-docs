import os
import shutil
from pathlib import Path
from typing import Optional

import yaml

try:
    from importlib import resources
except ImportError:
    # Fallback for Python < 3.9
    import importlib_resources as resources


class GreatTheme:
    """
    GreatTheme class for applying enhanced theming to quartodoc sites.

    This class provides methods to install theme assets and configure
    Quarto projects with the great-theme styling and functionality.
    """

    def __init__(self, project_path: Optional[str] = None):
        """
        Initialize GreatTheme instance.

        Args:
            project_path: Path to the Quarto project directory.
                         Defaults to current directory.
        """
        self.project_path = Path(project_path or os.getcwd())
        try:
            # Python 3.9+
            self.package_path = Path(resources.files("great_theme"))
        except AttributeError:
            # Fallback for older Python versions
            import importlib_resources

            self.package_path = Path(importlib_resources.files("great_theme"))
        self.assets_path = self.package_path / "assets"

    def install(self, force: bool = False) -> None:
        """
        Install great-theme assets and configuration to the project.

        Args:
            force: If True, overwrite existing files without prompting.
        """
        print("Installing great-theme to your quartodoc project...")

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
        """Update _quarto.yml with great-theme configuration."""
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
        """Remove great-theme assets and configuration from the project."""
        print("Uninstalling great-theme from your quartodoc project...")

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
        """Remove great-theme configuration from _quarto.yml."""
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

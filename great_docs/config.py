from pathlib import Path
from typing import Any

import yaml

# Default configuration values
DEFAULT_CONFIG: dict[str, Any] = {
    # API discovery settings
    "discovery_method": "dir",  # "dir" (default) or "all" (use __all__)
    "exclude": [],
    # GitHub integration
    "github_style": "widget",  # "widget" (shows stars) or "icon"
    # Source link configuration
    "source": {
        "enabled": True,
        "branch": None,  # Auto-detect from git
        "path": None,  # Auto-detect
        "placement": "usage",  # "usage" (default) or "title"
    },
    # Sidebar filter configuration
    "sidebar_filter": {
        "enabled": True,
        "min_items": 20,
    },
    # CLI documentation configuration
    "cli": {
        "enabled": False,
        "module": None,
        "name": None,
    },
    # Dark mode toggle
    "dark_mode_toggle": True,
    # Authors (rich author metadata)
    "authors": [],
    # Site settings (forwarded to _quarto.yml format.html)
    "site": {
        "theme": "flatly",
        "toc": True,
        "toc-depth": 2,
        "toc-title": "On this page",
    },
    # API Reference configuration (explicit section ordering)
    # If not provided, auto-generates sections from discovered exports
    "reference": [],
}


class Config:
    """
    Configuration manager for Great Docs.

    Loads configuration from great-docs.yml and provides access to settings
    with sensible defaults.
    """

    def __init__(self, project_root: Path):
        """
        Initialize configuration from great-docs.yml.

        Parameters
        ----------
        project_root
            Path to the project root directory where great-docs.yml is located.
        """
        self.project_root = project_root
        self.config_path = project_root / "great-docs.yml"
        self._config = self._load_config()

    def _load_config(self) -> dict[str, Any]:
        """
        Load configuration from great-docs.yml.

        Returns
        -------
        dict
            The loaded configuration merged with defaults.
        """
        config = DEFAULT_CONFIG.copy()

        if self.config_path.exists():
            try:
                with open(self.config_path, "r", encoding="utf-8") as f:
                    user_config = yaml.safe_load(f) or {}

                # Deep merge user config with defaults
                config = self._merge_config(config, user_config)
            except yaml.YAMLError as e:
                print(f"Warning: Error parsing great-docs.yml: {e}")
            except Exception as e:
                print(f"Warning: Could not read great-docs.yml: {e}")

        return config

    def _merge_config(self, defaults: dict[str, Any], user: dict[str, Any]) -> dict[str, Any]:
        """
        Deep merge user configuration with defaults.

        Parameters
        ----------
        defaults
            Default configuration values.
        user
            User-provided configuration values.

        Returns
        -------
        dict
            Merged configuration.
        """
        result = defaults.copy()

        for key, value in user.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self._merge_config(result[key], value)
            else:
                result[key] = value

        return result

    def get(self, key: str, default: Any = None) -> Any:
        """
        Get a configuration value.

        Parameters
        ----------
        key
            The configuration key (supports dot notation for nested keys).
        default
            Default value if key is not found.

        Returns
        -------
        Any
            The configuration value or default.
        """
        keys = key.split(".")
        value = self._config

        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default

        return value

    @property
    def discovery_method(self) -> str:
        """Get the API discovery method."""
        return self.get("discovery_method", "dir")

    @property
    def exclude(self) -> list[str]:
        """Get the list of items to exclude."""
        return self.get("exclude", [])

    @property
    def github_style(self) -> str:
        """Get the GitHub link style."""
        return self.get("github_style", "widget")

    @property
    def source_enabled(self) -> bool:
        """Check if source links are enabled."""
        return self.get("source.enabled", True)

    @property
    def source_branch(self) -> str | None:
        """Get the source link branch."""
        return self.get("source.branch")

    @property
    def source_path(self) -> str | None:
        """Get the custom source path."""
        return self.get("source.path")

    @property
    def source_placement(self) -> str:
        """Get the source link placement."""
        return self.get("source.placement", "usage")

    @property
    def sidebar_filter_enabled(self) -> bool:
        """Check if sidebar filter is enabled."""
        return self.get("sidebar_filter.enabled", True)

    @property
    def sidebar_filter_min_items(self) -> int:
        """Get the minimum items for sidebar filter."""
        return self.get("sidebar_filter.min_items", 20)

    @property
    def cli_enabled(self) -> bool:
        """Check if CLI documentation is enabled."""
        return self.get("cli.enabled", False)

    @property
    def cli_module(self) -> str | None:
        """Get the CLI module path."""
        return self.get("cli.module")

    @property
    def cli_name(self) -> str | None:
        """Get the CLI command name."""
        return self.get("cli.name")

    @property
    def dark_mode_toggle(self) -> bool:
        """Check if dark mode toggle is enabled."""
        return self.get("dark_mode_toggle", True)

    @property
    def reference(self) -> list[dict[str, Any]]:
        """Get the API reference configuration (explicit section ordering)."""
        return self.get("reference", [])

    @property
    def authors(self) -> list[dict[str, Any]]:
        """Get the rich author metadata."""
        return self.get("authors", [])

    @property
    def site(self) -> dict[str, Any]:
        """Get the site settings (forwarded to _quarto.yml format.html)."""
        return self.get("site", {})

    def exists(self) -> bool:
        """Check if the configuration file exists."""
        return self.config_path.exists()

    def to_dict(self) -> dict[str, Any]:
        """
        Get the full configuration as a dictionary.

        Returns
        -------
        dict
            The complete configuration.
        """
        return self._config.copy()


def load_config(project_root: Path | str) -> Config:
    """
    Load Great Docs configuration from a project.

    Parameters
    ----------
    project_root
        Path to the project root directory.

    Returns
    -------
    Config
        The loaded configuration.
    """
    return Config(Path(project_root))


def create_default_config() -> str:
    """
    Generate a default great-docs.yml configuration file content.

    Returns
    -------
    str
        YAML content for a default configuration file.
    """
    return """# Great Docs Configuration
# See https://rich-iannone.github.io/great-docs/user-guide/03-configuration.html

# API Discovery Settings
# ----------------------
# Discovery method: "dir" (default) uses static analysis to find public objects,
# "all" uses __all__ from __init__.py
# discovery_method: dir

# Exclude items from auto-documentation (affects 'init' and 'scan' commands)
# exclude:
#   - InternalClass
#   - helper_function

# GitHub Integration
# ------------------
# GitHub link style: "widget" (shows stars count) or "icon" (simple icon)
# github_style: widget

# Source Link Configuration
# -------------------------
# source:
#   enabled: true              # Enable/disable source links (default: true)
#   branch: main               # Git branch/tag to link to (default: auto-detect)
#   path: src/package          # Custom source path for monorepos (default: auto-detect)
#   placement: usage           # Where to place the link: "usage" (default) or "title"

# Sidebar Filter
# --------------
# sidebar_filter:
#   enabled: true              # Enable/disable filter (default: true)
#   min_items: 20              # Minimum items before showing filter (default: 20)

# CLI Documentation
# -----------------
# cli:
#   enabled: false             # Enable CLI documentation (default: false)
#   module: my_package.cli     # Module containing Click commands (auto-detected)
#   name: cli                  # Name of the Click command object (auto-detected)

# Dark Mode Toggle
# ----------------
# Enable/disable the dark mode toggle in navbar (default: true)
# dark_mode_toggle: true

# Author Information
# ------------------
# Author metadata for display in the landing page sidebar
# authors:
#   - name: Your Name
#     email: you@example.com
#     role: Lead Developer
#     affiliation: Organization
#     github: yourusername
#     homepage: https://yoursite.com
#     orcid: 0000-0002-1234-5678

# Site Settings
# -------------
# These settings are forwarded to _quarto.yml (format.html section)
# site:
#   theme: flatly              # Quarto theme (default: flatly)
#   toc: true                  # Show table of contents (default: true)
#   toc-depth: 2               # TOC heading depth (default: 2)
#   toc-title: On this page    # TOC title (default: "On this page")

# API Reference Structure
# -----------------------
# Explicit control over API reference sections. If not provided, sections are
# auto-generated from discovered exports. Each section has a title, description,
# and list of contents.
#
# For classes, use `members: true` (default) to document methods inline on the
# class page, or `members: false` to exclude methods (you can place them
# explicitly elsewhere in the reference if needed).
#
# reference:
#   - title: Core Classes
#     desc: Main classes for working with the package
#     contents:
#       - name: MyClass
#         members: false       # Don't document methods here
#       - SimpleClass          # Methods documented inline (default)
#
#   - title: Utility Functions
#     desc: Helper functions for common tasks
#     contents:
#       - helper_func
#       - another_func
"""

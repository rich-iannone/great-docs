# Great Theme for Quarto-Based Documentation Sites

This is comprehensive theming package that provides enhanced styling and functionality for Python documentation sites built with Quarto and `quartodoc`.

## Features

- **enhanced typography**: monospace fonts for code elements and improved readability
- **smart classification**: automatic function/method/class labeling with color-coded badges
- **smart method splitting**: classes with >5 methods get separate pages for better navigation
- **modern styling**: clean, professional appearance with gradient effects
- **mobile responsive**: optimized for all device sizes
- **streamlined workflow**: single `great-theme build` command handles everything
- **easy installation**: simple CLI tool for quick setup
- **intelligent setup**: auto-generates quartodoc configuration from your package's `__all__`
- **zero configuration**: works out of the box with sensible defaults

## Quick Start

### Installation

#### From PyPI (when published)

```bash
pip install great-theme
```

#### From GitHub

Install the latest version directly from the GitHub repository:

```bash
pip install git+https://github.com/rich-iannone/great-theme.git
```

Or install a specific branch, tag, or commit:

```bash
# Install from a specific branch
pip install git+https://github.com/rich-iannone/great-theme.git@main

# Install from a specific tag
pip install git+https://github.com/rich-iannone/great-theme.git@v0.1.0

# Install from a specific commit
pip install git+https://github.com/rich-iannone/great-theme.git@abc1234
```

For development or editable installation:

```bash
# Clone the repository
git clone https://github.com/rich-iannone/great-theme.git
cd great-theme

# Install in editable mode
pip install -e .

# Or install with development dependencies
pip install -e ".[dev]"
```

### Apply to Your Project

Navigate to your project root directory and run:

```bash
great-theme install
```

The installer will:

1. Automatically detect existing documentation directories (`docs/`, `site/`, etc.)
2. Look for existing `_quarto.yml` files to determine the correct location
3. Prompt you to choose a location if no docs directory is found
4. Install all necessary files to the detected or chosen directory
5. **Auto-create `index.qmd` from your `README.md`** (like pkgdown does)
6. **Auto-detect your package name** from `pyproject.toml`, `setup.py`, or directory structure
7. **Auto-generate API sections** by parsing `__all__` from your package's `__init__.py`
8. **Add website navigation** with Home and API Reference links in the navbar

That's it! The theme will automatically enhance your documentation site.

## What Gets Enhanced

Great Theme automatically improves your quartodoc site through:

### Visual Enhancements

- **function signatures** styled with monospace fonts
- **type annotations** with improved formatting
- **parameter descriptions** with better spacing
- **code blocks** with enhanced syntax highlighting

### Smart Labeling

- **classes** get green labels and styling
- **methods** get blue labels (e.g., `Class.method()`)
- **functions** get orange labels (e.g., `function()`)

### Responsive Design

- mobile-friendly navigation
- optimized sidebar behavior
- touch-friendly interface elements

### Interactive Elements

- animated gradient headers for Examples sections
- hover effects on navigation elements
- smooth transitions and animations

## Usage

### CLI Commands

```bash
# Install theme (auto-detects docs directory)
great-theme install

# Install to specific docs directory
great-theme install --docs-dir docs

# Install to specific project
great-theme install --project-path /path/to/project

# Install with specific docs directory in a project
great-theme install --project-path /path/to/project --docs-dir documentation

# Force overwrite existing files
great-theme install --force

# Build documentation (runs quartodoc build + quarto render)
great-theme build

# Build and watch for changes
great-theme build --watch

# Build and serve locally with live preview
great-theme preview

# Remove theme from project
great-theme uninstall

# Uninstall from specific docs directory
great-theme uninstall --docs-dir docs
```

### Python API

```python
from great_theme import GreatTheme

# Initialize for current directory (auto-detects docs dir)
theme = GreatTheme()

# Install theme files and configuration
theme.install()

# Build documentation
theme.build()

# Build with watch mode
theme.build(watch=True)

# Preview locally
theme.preview()

# Initialize with specific project root
theme = GreatTheme(project_path="/path/to/project")
theme.install()

# Initialize with specific docs directory
theme = GreatTheme(project_path="/path/to/project", docs_dir="docs")
theme.install()

# Remove theme
theme.uninstall()
```

## What Gets Installed

When you run `great-theme install`, the following files are added to your documentation directory:

```
your-project/
├── docs/                # Or your chosen docs directory
│   ├── _quarto.yml      # Updated with theme configuration
│   ├── index.qmd        # Auto-created from README.md
│   ├── great-theme.css  # Main theme stylesheet
│   └── scripts/
│       └── post-render.py   # HTML post-processing script
```

If you have an existing `_quarto.yml` or documentation directory, great-theme will detect and use it.

### Auto-Generated Configuration

The installer intelligently configures your project:

1. **index.qmd from README.md**: Your README becomes your documentation homepage (like pkgdown)
2. **quartodoc configuration**: Auto-detects your package name from:
   - `pyproject.toml`
   - `setup.py`
   - Package directory structure
3. **Auto-generated API sections**: Parses your package's `__init__.py` to read `__all__` and automatically creates organized sections for:
   - Classes
   - Functions
   - Other exports
4. **Sensible defaults**: Includes recommended settings:
   ```yaml
   quartodoc:
     package: your-package # Auto-detected
     dir: reference
     title: API Reference
     style: pkgdown
     dynamic: true
     renderer:
       style: markdown
       table_style: description-list
     sections: # Auto-generated from __all__
       - title: Classes
         desc: Core classes and types
         contents:
           - YourClass
           - AnotherClass
       - title: Functions
         desc: Public functions
         contents:
           - your_function
   ```

**Requirements for auto-generation**:

- Your package must have `__all__` defined in `__init__.py`
- Names in `__all__` should be importable from the package

Great-theme will search for your package in standard locations including:

- Project root (e.g., `your-package/`)
- `python/` directory (common for Rust/Python hybrid packages)
- `src/` directory
- `lib/` directory

If `__all__` is not found, great-theme will create a basic configuration and you can manually add sections.

### Smart Method Splitting

Great-theme automatically applies smart heuristics for documenting classes:

- **Classes with ≤5 methods**: Methods are documented inline on the class page
- **Classes with >5 methods**: Methods get separate pages (like `Graph.add_node`, `Graph.add_edge`)

This prevents overwhelming single-page documentation and improves navigation for large classes.

## Building Your Documentation

After installation, the easiest way to build your documentation:

```bash
great-theme build
```

This single command runs both `quartodoc build` and `quarto render` for you.

### Detailed Steps

If you prefer to run commands separately or customize the workflow:

1. **(Optional) Edit the quartodoc sections** in `_quarto.yml` to organize your API:

   ```yaml
   quartodoc:
     sections:
       - title: Core Classes
         desc: Main classes for your package
         contents:
           - name: Graph
             members: [] # Empty list = separate pages for methods
   ```

2. **Generate API reference pages**:

   ```bash
   quartodoc build
   # or use: great-theme build
   ```

3. **Build your site**:

   ```bash
   quarto render
   # or use: great-theme build (does both steps)
   ```

4. **Preview locally with live reload**:

   ```bash
   great-theme preview
   # or: quarto preview
   ```

Your documentation is now live with great-theme styling!

### Troubleshooting

**CyclicAliasError from quartodoc**: If `quartodoc build` fails with a `CyclicAliasError` for certain exports, you may need to exclude problematic items from your quartodoc configuration. This can happen with re-exported constants or objects that create circular references in the import graph.

**quartodoc not installed**: Great-theme requires `quartodoc` to generate API documentation. Install it with:

```bash
pip install quartodoc
```

Your documentation is now live with great-theme styling!

## Configuration

The theme works with your existing `_quarto.yml` configuration. After installation, your config will include:

```yaml
project:
  type: website
  post-render: scripts/post-render.py

format:
  html:
    theme: flatly # Recommended base theme
    css:
      - great-theme.css
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

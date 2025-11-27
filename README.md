# Great Docs for Quarto-Based Documentation Sites

This is comprehensive theming package that provides enhanced styling and functionality for Python documentation sites built with Quarto and `quartodoc`.

## Features

- **enhanced typography**: monospace fonts for code elements and improved readability
- **smart classification**: automatic function/method/class labeling with color-coded badges
- **smart method splitting**: classes with >5 methods get separate pages for better navigation (uses griffe introspection)
- **modern styling**: clean, professional appearance
- **mobile responsive**: optimized for all device sizes
- **streamlined workflow**: single `great-docs build` command handles everything
- **easy installation**: simple CLI tool for quick setup
- **intelligent setup**: auto-generates quartodoc configuration from your package's `__all__`
- **safe introspection**: works with packages containing non-Python components
- **zero configuration**: works out of the box with sensible defaults

## Quick Start

### Installation

#### From PyPI (when published)

```bash
pip install great-docs
```

#### From GitHub

Install the latest version directly from the GitHub repository:

```bash
pip install git+https://github.com/rich-iannone/great-docs.git
```

Or install a specific branch, tag, or commit:

```bash
# Install from a specific branch
pip install git+https://github.com/rich-iannone/great-docs.git@main

# Install from a specific tag
pip install git+https://github.com/rich-iannone/great-docs.git@v0.1.0

# Install from a specific commit
pip install git+https://github.com/rich-iannone/great-docs.git@abc1234
```

For development or editable installation:

```bash
# Clone the repository
git clone https://github.com/rich-iannone/great-docs.git
cd great-docs

# Install in editable mode
pip install -e .

# Or install with development dependencies
pip install -e ".[dev]"
```

### Apply to Your Project

Navigate to your project root directory and run:

```bash
great-docs init
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

This up-and-running site sets you up for success with your documentation dreams.

## What Gets Enhanced

Great Docs automatically initializes a quartodoc site and includes:

### Nice Visuals

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

## Usage

### CLI Commands

```bash
# Initialize theme (auto-detects docs directory)
great-docs init

# Initialize to specific docs directory
great-docs init --docs-dir docs

# Initialize to specific project
great-docs init --project-path /path/to/project

# Initialize with specific docs directory in a project
great-docs init --project-path /path/to/project --docs-dir documentation

# Force overwrite existing files
great-docs init --force

# Build documentation (runs quartodoc build + quarto render)
great-docs build

# Build and watch for changes
great-docs build --watch

# Build and serve locally with live preview
great-docs preview

# Remove theme from project
great-docs uninstall

# Uninstall from specific docs directory
great-docs uninstall --docs-dir docs
```

### Python API

```python
from great_docs import GreatDocs

# Initialize for current directory (auto-detects docs dir)
theme = GreatDocs()

# Install theme files and configuration
theme.install()

# Build documentation
theme.build()

# Build with watch mode
theme.build(watch=True)

# Preview locally
theme.preview()

# Initialize with specific project root
theme = GreatDocs(project_path="/path/to/project")
theme.install()

# Initialize with specific docs directory
theme = GreatDocs(project_path="/path/to/project", docs_dir="docs")
theme.install()

# Remove theme
theme.uninstall()
```

## What Gets Installed

When you run `great-docs init`, the following files are added to your documentation directory:

```
your-project/
├── docs/                # Or your chosen docs directory
│   ├── _quarto.yml      # Updated with theme configuration
│   ├── index.qmd        # Auto-created from README.md
│   ├── great-docs.css  # Main theme stylesheet
│   └── scripts/
│       └── post-render.py   # HTML post-processing script
```

If you have an existing `_quarto.yml` or documentation directory, great-docs will detect and use it.

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

**Filtering non-documentable items**:

If your package includes items that can't be documented by quartodoc (e.g., Rust types, C bindings), you can exclude them using `__gt_exclude__`:

```python
# In your package's __init__.py
__all__ = ["Graph", "Node", "Edge", "some_function"]

# Exclude items that quartodoc can't document
__gt_exclude__ = ["Node", "Edge"]  # Rust types
```

Great Docs will automatically filter out items in `__gt_exclude__` when generating the quartodoc configuration.

Great Docs will search for your package in standard locations including:

- Project root (e.g., `your-package/`)
- `python/` directory (common for Rust/Python hybrid packages)
- `src/` directory
- `lib/` directory

If `__all__` is not found, Great Docs will create a basic configuration and you can manually add sections.

### Smart Method Splitting

Great Docs uses **griffe** to analyze your package without importing it. This enables:

- **Safe introspection**: Works with packages containing non-Python components
- **Accurate method counting**: Counts actual public methods on each class
- **Smart categorization**: Automatically identifies classes, functions, and other objects
- **Automatic method enumeration**: Explicitly lists all methods for quartodoc to document

Based on method count:

- **Classes with ≤5 methods**: Methods are documented inline on the class page
- **Classes with >5 methods**:
  - Class page is created with `members: []` to suppress inline method documentation
  - Creates a separate section with all methods explicitly listed
  - Each method gets its own documentation page

For example, if your `Graph` class has 191 methods, Great Docs will:

1. Add `Graph` to the Classes section with `members: []` (suppresses inline method docs)
2. Create a new "Graph Methods" section listing all 191 methods: `Graph.add_node`, `Graph.add_edge`, etc.
3. Each method gets its own documentation page for better navigation

Generated configuration:

```yaml
quartodoc:
  sections:
    - title: Classes
      desc: Core classes and types
      contents:
        - name: Graph
          members: [] # Suppresses inline method documentation

    - title: Graph Methods
      desc: Methods for the Graph class
      contents:
        - Graph.add_node
        - Graph.add_edge
        # ... all 191 methods
```

This prevents overwhelming single-page documentation and improves navigation for large classes.

## Building Your Documentation

After installation, the easiest way to build your documentation:

```bash
great-docs build
```

This single command runs both `quartodoc build` and `quarto render` for you, with a progress indicator so you can see the build activity.

### Detailed Steps

If you prefer to run commands separately or customize the workflow:

1. **(Optional) Edit the quartodoc sections** in `_quarto.yml` to organize your API documentation as needed.

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

Your documentation is now live with Great Theme styling!

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
      - great-docs.css
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

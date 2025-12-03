# Great Docs for Python Documentation Sites

A comprehensive documentation site generator for Python packages. Great Docs automatically creates beautiful, professional documentation sites with auto-generated API references, smart navigation, and modern styling.

## Features

- one-command setup: single `great-docs init` creates your entire docs site
- auto-generated API docs: automatically discovers and documents your package's API
- smart organization: intelligent class/method/function categorization
- enhanced typography: monospace fonts for code elements and improved readability
- modern styling: clean, professional appearance
- mobile responsive: optimized for all device sizes
- streamlined workflow: single `great-docs build` command handles everything
- intelligent setup: auto-generates configuration from your package's public API
- safe introspection: uses static analysis by default, with `__all__` as an option
- zero configuration: works out of the box with sensible defaults
- LLM-friendly docs: auto-generates `llms.txt` file for AI/LLM documentation indexing

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

1. automatically detect existing documentation directories (`docs/`, `site/`, etc.)
2. look for existing `_quarto.yml` files to determine the correct location
3. prompt you to choose a location if no docs directory is found
4. install all necessary files to the detected or chosen directory
5. auto-create `index.qmd` from your `README.md`
6. auto-detect your package name from `pyproject.toml`, `setup.py`, or directory structure
7. auto-generate API sections by discovering public objects in your package
8. add website navigation with Home and API Reference links in the navbar

This up-and-running site sets you up for success with your documentation dreams.

## What Gets Enhanced

Great Docs automatically creates a complete documentation site with:

### Nice Visuals

- function signatures styled with monospace fonts
- type annotations with improved formatting
- parameter descriptions with better spacing
- code blocks with enhanced syntax highlighting

### Smart Labeling

- _classes_ get green labels and styling
- _methods_ get blue labels (e.g., `Class.method()`)
- _functions_ get orange labels (e.g., `function()`)

### Responsive Design

- mobile-friendly navigation
- optimized sidebar behavior
- touch-friendly interface elements

## Usage

### CLI Commands

```bash
# Initialize the docs (auto-detects docs directory)
great-docs init

# Initialize to specific docs directory
great-docs init --docs-dir docs

# Initialize to specific project
great-docs init --project-path /path/to/project

# Initialize with specific docs directory in a project
great-docs init --project-path /path/to/project --docs-dir documentation

# Force overwrite existing files
great-docs init --force

# Build documentation (re-discovers API and updates config)
great-docs build

# Build without refreshing API config (faster when API unchanged)
great-docs build --no-refresh

# Build and watch for changes
great-docs build --watch

# Build and serve locally with live preview
great-docs preview

# Set up GitHub Pages deployment workflow
great-docs setup-github-pages

# Set up with custom options
great-docs setup-github-pages --docs-dir site --main-branch develop --python-version 3.12

# Force overwrite existing workflow
great-docs setup-github-pages --force

# Remove docs from project
great-docs uninstall

# Uninstall from specific docs directory
great-docs uninstall --docs-dir docs
```

### Python API

```python
from great_docs import GreatDocs

# Initialize for current directory (auto-detects docs dir)
docs = GreatDocs()

# Install docs files and configuration
docs.install()

# Build documentation (re-discovers API by default)
docs.build()

# Build without refreshing API config (faster rebuild)
docs.build(refresh=False)

# Build with watch mode
docs.build(watch=True)

# Preview locally
docs.preview()

# Initialize with specific project root
docs = GreatDocs(project_path="/path/to/project")
docs.install()

# Initialize with specific docs directory
docs = GreatDocs(project_path="/path/to/project", docs_dir="docs")
docs.install()

# Remove the docs
docs.uninstall()
```

## What Gets Installed

When you run `great-docs init`, the following files are added to your documentation directory:

```
your-project/
├── docs/                # Or your chosen docs directory
│   ├── _quarto.yml      # Updated with configuration
│   ├── index.qmd        # Auto-created from README.md
│   ├── great-docs.css   # Main stylesheet
│   └── scripts/
│       └── post-render.py   # HTML post-processing script
```

If you have an existing `_quarto.yml` or documentation directory, great-docs will detect and use it.

### Auto-Generated Configuration

The installer intelligently configures your documentation site:

1. **index.qmd from README.md**: Your README becomes your documentation homepage (like pkgdown)
2. **API reference configuration**: Auto-detects your package name from:
   - `pyproject.toml`
   - `setup.py`
   - Package directory structure
3. **Auto-generated API sections**: Discovers your package's public API and automatically creates organized sections for:
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
     sections: # Auto-generated from package exports
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

**API Discovery Methods**:

Great Docs uses static analysis to discover public objects in your package. This safely finds all non-private names (e.g., those not starting with an underscore) without importing your package or requiring `__all__` to be defined.

**Auto-excluded objects**:

Great Docs automatically excludes common internal/utility names that most packages don't want in their documentation:

| Category          | Names                                                            |
| ----------------- | ---------------------------------------------------------------- |
| CLI/Entry points  | `main`, `cli`                                                    |
| Version/Metadata  | `version`, `VERSION`, `VERSION_INFO`                             |
| Module re-exports | `core`, `utils`, `helpers`, `constants`, `config`, `settings`    |
| Standard library  | `PackageNotFoundError`, `typing`, `annotations`, `TYPE_CHECKING` |
| Logging           | `logger`, `log`, `logging`                                       |

To force-include any auto-excluded items, use the `include` option:

```toml
# In your pyproject.toml
[tool.great-docs]
include = ["main", "cli"]  # Force-include auto-excluded items
```

**Filtering objects from documentation**:

If your package includes additional items that shouldn't be documented, you can exclude them in your `pyproject.toml`:

```toml
# In your pyproject.toml
[tool.great-docs]
exclude = ["Node", "Edge"]  # Items to exclude from documentation
```

Great Docs will automatically filter out these items when generating the configuration.

Great Docs will search for your package in standard locations including:

- Project root (e.g., `your-package/`)
- `python/` directory (common for Rust/Python hybrid packages)
- `src/` directory
- `lib/` directory

If discovery fails (e.g., the package cannot be loaded), Great Docs will create a basic configuration and you can manually add sections.

### Smart Method Splitting

Great Docs will analyze your package to enable:

- automatically identify classes, functions, and other objects
- enumerate all methods for documentation

Based on method count:

- classes with ≤5 methods are documented inline on the class page
- for classes with >5 methods:
  - the class page will suppress inline method documentation
  - a separate section will be created with all these methods explicitly listed
  - each method gets its own documentation page

For example, if your `Graph` class has 190 methods, Great Docs will:

1. add `Graph` to the Classes section with `members: []` (suppressing inline method docs)
2. create a new `"Graph Methods"` section listing all 190 methods: `Graph.add_node`, `Graph.add_edge`, etc.
3. build documentation pages for each of the methods for better navigation

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
        # ... all 190 methods
```

This prevents overwhelming single-page documentation and improves navigation for large classes.

## Building Your Documentation

After installation, the easiest way to build your documentation:

```bash
great-docs build
```

This single command handles all the build steps for you, with a progress indicator so you can see the activity.

## Deploying to GitHub Pages

Great Docs makes it easy to deploy your documentation to GitHub Pages with a single command:

```bash
great-docs setup-github-pages
```

This command creates a complete GitHub Actions workflow (`.github/workflows/docs.yml`) that will:

- build documentation automatically on every push to main
- deploy to GitHub Pages when changes are merged to main
- create preview deployments for pull requests
- cache dependencies for faster builds

### Customizing the Workflow

You can customize the workflow generation with options:

```bash
# Use a different docs directory
great-docs setup-github-pages --docs-dir site

# Deploy from a different branch
great-docs setup-github-pages --main-branch develop

# Use a different Python version
great-docs setup-github-pages --python-version 3.12

# Combine options
great-docs setup-github-pages --docs-dir site --main-branch develop --python-version 3.12
```

### Enabling GitHub Pages

After generating the workflow:

1. commit and push the workflow file to your repository
2. go to your repository _Settings -> Pages_
3. set _Source_ to `GitHub Actions`
4. push changes to your main branch to trigger the first deployment

Your documentation will be automatically published at `https://[username].github.io/[repository]`.

### What the Workflow Does

The generated workflow includes three jobs:

- `build-docs`: Installs dependencies, sets up Quarto, and builds your documentation
- `publish-docs`: Deploys to GitHub Pages (main branch only)
- `preview-docs`: Creates preview deployments for pull requests

All builds are cached for faster execution on subsequent runs.

## Customization

### Landing Page Metadata Sidebar

Great Docs automatically creates a metadata sidebar on your landing page that displays:

- links to PyPI, source code, bug tracker
- a link to the full license text
- author information with contact links
- metadata such as Python version requirements and optional dependencies

The sidebar is automatically populated from your `pyproject.toml` metadata. To enhance the developer information with such metadata, add a `[tool.great-docs]` section to `pyproject.toml`:

```toml
# Standard author information (used by PyPI)
[project]
authors = [
    {name = "Your Name", email = "you@example.com"}
]

# Author metadata for documentation (optional)
[tool.great-docs]

[[tool.great-docs.authors]]
name = "Your Name"
email = "you@example.com"
role = "Lead Developer"         # Optional: e.g., "Lead Developer", "Contributor"
affiliation = "Organization"    # Optional: e.g., "Company Name", "University Name"
github = "yourusername"         # Optional: GitHub username
homepage = "https://asite.com"  # Optional: Personal website
orcid = "0000-0002-1234-5678"   # Optional: ORCID ID or full URL

# Add more authors by repeating the [[tool.great-docs.authors]] section
[[tool.great-docs.authors]]
name = "Second Author"
email = "second@example.com"
role = "Contributor"
github = "secondauthor"
```

Supported fields (all optional except for `name`):

- `name` (required): Author's full name
- `email`: Email address (creates a clickable email icon)
- `role`: Role in the project (e.g., "Lead Developer", "Contributor", "Maintainer")
- `affiliation`: Organization or institution (e.g., "Posit", "MIT")
- `github`: GitHub username (creates a clickable GitHub icon)
- `homepage`: Personal website URL (creates a clickable home icon)
- `orcid`: ORCID identifier or full URL (creates a clickable ORCID icon)

If `[tool.great-docs.authors]` is not present, Great Docs falls back to using the standard `project.authors` with automatically extracted GitHub information from your repository URL.

## Configuration

This all should work with any existing `_quarto.yml` configuration. After installation, your config will include:

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

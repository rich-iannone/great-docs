# Great Theme for quartodoc

A comprehensive theming package that provides enhanced styling and functionality for Python documentation sites built with quartodoc.

## Features

- enhanced Typography: monospace fonts for code elements and improved readability
- smart Classification: automatic function/method/class labeling with color-coded badges
- modern Styling: clean, professional appearance with gradient effects
- mobile Responsive: optimized for all device sizes
- easy Installation: simple CLI tool for quick setup
- zero Configuration: works out of the box with sensible defaults

## 🚀 Quick Start

### Installation

```bash
pip install great-theme
```

### Apply to Your Project

Navigate to your quartodoc project directory and run:

```bash
great-theme install
```

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
# Install theme to current directory
great-theme install

# Install to specific directory
great-theme install --project-path /path/to/project

# Force overwrite existing files
great-theme install --force

# Remove theme from project
great-theme uninstall
```

### Python API

```python
from great_theme import GreatTheme

# Initialize for current directory
theme = GreatTheme()

# Install theme files and configuration
theme.install()

# Install to specific directory
theme = GreatTheme(project_path="/path/to/project")
theme.install()

# Remove theme
theme.uninstall()
```

## What Gets Installed

When you run `great-theme install`, the following files are added to your project:

```
your-project/
├── _quarto.yml          # Updated with theme configuration
├── great-theme.css      # Main theme stylesheet
└── scripts/
    └── post-render.py   # HTML post-processing script
```

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

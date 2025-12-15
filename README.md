# Great Docs

Beautiful documentation sites for Python packages.

Great Docs automatically creates professional documentation with auto-generated API references, CLI documentation, smart navigation, and modern styling.

## Features

- **One-command setup** — `great-docs init` creates your entire docs site
- **Auto-generated API docs** — discovers and documents your package's public API
- **CLI documentation** — generates reference pages for Click-based CLIs
- **Smart organization** — intelligent class/method/function categorization
- **User Guide support** — write narrative documentation alongside API reference
- **Source links** — automatic links to source code on GitHub
- **LLM-friendly** — auto-generates `llms.txt` and `llms-full.txt` for AI documentation indexing
- **GitHub Pages ready** — one command sets up deployment workflow

## Quick Start

### Install

Great Docs is not yet available on PyPI, so, install from GitHub:

```bash
pip install git+https://github.com/rich-iannone/great-docs.git
```

### Initialize

Navigate to your Python project and run:

```bash
great-docs init
```

This auto-detects your package, creates configuration, and sets up your docs site.

### Build

```bash
great-docs build
```

Your documentation site is ready in `docs/_site/`.

### Preview

```bash
great-docs preview
```

Opens a local server with live reload for development.

### Deploy

```bash
great-docs setup-github-pages
```

Creates a GitHub Actions workflow for automatic deployment.

## What You Get

- **Landing page** from your README with a metadata sidebar (authors, license, links)
- **API reference** with classes, functions, and methods organized and styled
- **CLI reference** with `--help` output in terminal style
- **User Guide** from your `user_guide/` directory
- **Source links** to GitHub for every documented item
- **Mobile-friendly** responsive design

## Documentation

The User Guide covers:

- [Installation](https://rich-iannone.github.io/great-docs/user-guide/01-installation.html)
- [Quick Start](https://rich-iannone.github.io/great-docs/user-guide/02-quickstart.html)
- [Configuration](https://rich-iannone.github.io/great-docs/user-guide/03-configuration.html)
- [API Documentation](https://rich-iannone.github.io/great-docs/user-guide/04-api-documentation.html)
- [CLI Documentation](https://rich-iannone.github.io/great-docs/user-guide/05-cli-documentation.html)
- [User Guides](https://rich-iannone.github.io/great-docs/user-guide/06-user-guides.html)
- [Deployment](https://rich-iannone.github.io/great-docs/user-guide/07-deployment.html)

## License

MIT License. See [LICENSE](https://rich-iannone.github.io/great-docs/license.html) for details.

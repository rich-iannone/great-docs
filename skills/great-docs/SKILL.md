---
name: great-docs
description: >
  Generate beautiful documentation sites for Python packages with Great Docs.
  Use when creating, configuring, building, or troubleshooting Python package
  documentation. Covers configuration (great-docs.yml), API reference generation,
  CLI documentation, user guides, theming, logos, hero sections, deployment, and
  the llms.txt/llms-full.txt agent context files.
license: MIT
compatibility: Requires Python 3.10+, Quarto CLI installed.
metadata:
  author: rich-iannone
  version: "1.0"
---

# Great Docs

Great Docs generates documentation sites for Python packages. It introspects your
package's API, renders reference pages, and produces a Quarto-based static site with
user guides, CLI docs, changelogs, and more.

## When to use this skill

- Setting up a new documentation site for a Python package
- Configuring `great-docs.yml` options
- Troubleshooting build or rendering errors
- Customizing themes, logos, hero sections, or navigation
- Adding user guide pages, recipes, or custom sections
- Generating CLI reference documentation

## Installation

```bash
pip install great-docs
```

Quarto must also be installed: <https://quarto.org/docs/get-started/>

## Quick start

```bash
# Initialize a docs site in your package root
great-docs init

# Build the documentation
great-docs build

# Preview locally
great-docs preview
```

This creates a `great-docs/` directory with the rendered site in `great-docs/_site/`.

## Configuration decision table

All configuration goes in `great-docs.yml` at the project root.

| Need                            | Config key          | Example value                                       |
| ------------------------------- | ------------------- | --------------------------------------------------- |
| Change docstring parser         | `parser`            | `google`, `numpy`, or `sphinx`                      |
| Add CLI reference docs          | `cli.enabled`       | `true`                                              |
| Set a custom logo               | `logo`              | `assets/logo.svg` or `{light: ..., dark: ...}`      |
| Toggle dark mode switch         | `dark_mode_toggle`  | `true` (default) or `false`                         |
| GitHub stars widget             | `github_style`      | `widget` or `icon`                                  |
| Announcement banner             | `announcement`      | `"v2 is out!"` or `{content: ..., type: info}`      |
| Navbar gradient                 | `navbar_style`      | `sky`, `peach`, `lilac`, `mint`, etc.               |
| Content area glow               | `content_style`     | `lilac` or `{preset: sky, pages: homepage}`         |
| Exclude items from API docs     | `exclude`           | `["InternalClass", "helper_fn"]`                    |
| Custom page sections            | `sections`          | `[{title: Examples, dir: examples}]`                |
| Hero section on homepage        | `hero`              | `true`, `false`, or `{enabled: true, tagline: ...}` |
| Solid navbar color              | `navbar_color`      | `"#1a1a2e"` or `{light: ..., dark: ...}`            |
| Disable attribution footer      | `attribution`       | `false`                                             |
| Control changelog               | `changelog.enabled` | `true` (default) or `false`                         |
| Homepage mode                   | `homepage`          | `index` (default) or `user_guide`                   |
| Static analysis for tricky pkgs | `dynamic`           | `false`                                             |

## Gotchas

1. **Run from project root.** All commands (`init`, `build`, `preview`) must run from the
   directory containing `great-docs.yml`.
2. **`module` vs package name.** The `module` config key is the Python importable name,
   not the PyPI distribution name. For a package installed as `py-shiny`, set
   `module: shiny`.
3. **Circular imports.** If the package uses lazy loading or circular aliases, set
   `dynamic: false` to use static (griffe-based) analysis instead of runtime introspection.
4. **User guide ordering.** User guide `.qmd` files must have numeric prefixes
   (`00-introduction.qmd`, `01-installation.qmd`) for deterministic ordering.
5. **Don't edit `great-docs/` directly.** The `great-docs/` directory is regenerated on
   every build. Make changes in source files (`great-docs.yml`, `user_guide/`, `recipes/`)
   instead.
6. **Quarto must be installed.** Great Docs delegates HTML rendering to Quarto. If
   `quarto` is not on PATH, the build will fail at step 2.

## Capabilities and boundaries

**What agents can configure (via `great-docs.yml` or source files):**

- All `great-docs.yml` settings listed above
- User guide `.qmd` pages in `user_guide/`
- Recipe `.qmd` pages in `recipes/`
- Custom section `.qmd` pages
- Custom CSS/SCSS overrides
- Logo and favicon assets

**Requires human setup:**

- Initial `pip install great-docs` and `quarto` installation
- PyPI publishing of the documented package
- GitHub Pages or other hosting deployment configuration
- Custom domain DNS setup
- GitHub repository creation and access tokens

## Build pipeline

The build runs in this order:

1. Prepare build directory (copy assets, JS, SCSS to `great-docs/`)
2. Generate `_quarto.yml` configuration
3. Refresh API reference config (if `--refresh`)
4. Generate `llms.txt` and `llms-full.txt`
5. Generate source links JSON
6. Generate changelog from GitHub Releases
7. Generate CLI reference pages (if `cli.enabled: true`)
8. Process user guide
9. Process custom sections
10. Build API reference via internal renderer
11. Run `quarto render` to produce final HTML in `_site/`

## Common tasks

### Add a user guide page

Create a `.qmd` file in `user_guide/` with a numeric prefix:

```
user_guide/05-advanced-usage.qmd
```

It will be auto-discovered and added to the sidebar on next build.

### Add a recipe

Create a `.qmd` file in `recipes/`:

```
recipes/07-custom-theme.qmd
```

### Enable CLI documentation

```yaml
# great-docs.yml
cli:
  enabled: true
  module: my_package.cli # module containing the Click app
  name: my-cli # CLI command name
```

### Override the homepage

```yaml
# great-docs.yml
homepage: user_guide # Use the first user guide page as landing
```

## Resources

- [Full documentation](https://posit-dev.github.io/great-docs/)
- [llms.txt](https://posit-dev.github.io/great-docs/llms.txt) — Indexed API reference
- [llms-full.txt](https://posit-dev.github.io/great-docs/llms-full.txt) — Comprehensive docs
- [Configuration guide](https://posit-dev.github.io/great-docs/user-guide/03-configuration.html)
- [GitHub repository](https://github.com/posit-dev/great-docs)

import sys

import click

from . import __version__
from .core import GreatDocs


class OrderedGroup(click.Group):
    """Click group that lists commands in the order they were added."""

    def list_commands(self, ctx):
        return list(self.commands.keys())


@click.group(cls=OrderedGroup)
@click.version_option(version=__version__, prog_name="great-docs")
def cli():
    """Great Docs - Beautiful documentation for Python packages.

    Great Docs generates professional documentation sites with auto-generated
    API references, CLI documentation, smart navigation, and modern styling.

    Get started with 'great-docs init' to set up your docs, then use
    'great-docs build' to generate your site.
    """
    pass


@click.command()
@click.option(
    "--project-path",
    type=click.Path(exists=True, file_okay=False, dir_okay=True),
    help="Path to your Quarto project root directory (default: current directory)",
)
@click.option(
    "--docs-dir",
    type=str,
    help="Path to documentation directory relative to project root (e.g., 'docs', 'site')",
)
@click.option(
    "--force",
    is_flag=True,
    help="Overwrite existing files without prompting",
)
def init(project_path, docs_dir, force):
    """Initialize great-docs in your project.

    This command sets up everything needed for your documentation site:

    \b
    • Installs CSS, JavaScript, and configuration files
    • Auto-detects your package name and public API
    • Creates index.qmd from your README.md
    • Configures navigation and sidebar
    • Sets up quartodoc for API reference generation

    Run this once to get started, then use 'great-docs build' to generate
    your documentation.

    \b
    Examples:
      great-docs init                       # Initialize in current directory
      great-docs init --docs-dir site       # Use 'site/' instead of 'docs/'
      great-docs init --force               # Overwrite existing files
      great-docs init --project-path ../pkg # Initialize in another project
    """
    try:
        docs = GreatDocs(project_path=project_path, docs_dir=docs_dir)
        docs.install(force=force)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


@click.command()
@click.option(
    "--project-path",
    type=click.Path(exists=True, file_okay=False, dir_okay=True),
    help="Path to your Quarto project root directory (default: current directory)",
)
@click.option(
    "--docs-dir",
    type=str,
    help="Path to documentation directory relative to project root (e.g., 'docs', 'site')",
)
@click.option(
    "--watch",
    is_flag=True,
    help="Watch for changes and rebuild automatically",
)
@click.option(
    "--no-refresh",
    is_flag=True,
    help="Skip re-discovering package exports (faster rebuild when API unchanged)",
)
def build(project_path, docs_dir, watch, no_refresh):
    """Build your documentation site.

    This command runs the complete build process:

    \b
    1. Refreshes quartodoc configuration (discovers API changes)
    2. Generates llms.txt for AI/LLM documentation indexing
    3. Creates source links to GitHub
    4. Generates CLI reference pages (if enabled)
    5. Runs quartodoc to generate API reference
    6. Runs Quarto to render the final HTML site

    Use --no-refresh to skip API discovery for faster rebuilds when your
    package's public API hasn't changed.

    \b
    Examples:
      great-docs build                      # Full build with API refresh
      great-docs build --no-refresh         # Fast rebuild (skip API discovery)
      great-docs build --watch              # Rebuild on file changes
      great-docs build --project-path ../pkg
    """
    try:
        docs = GreatDocs(project_path=project_path, docs_dir=docs_dir)
        docs.build(watch=watch, refresh=not no_refresh)
    except KeyboardInterrupt:
        click.echo("\n👋 Stopped watching")
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


@click.command()
@click.option(
    "--project-path",
    type=click.Path(exists=True, file_okay=False, dir_okay=True),
    help="Path to your Quarto project root directory (default: current directory)",
)
@click.option(
    "--docs-dir",
    type=str,
    help="Path to documentation directory relative to project root (e.g., 'docs', 'site')",
)
def uninstall(project_path, docs_dir):
    """Remove great-docs from your project.

    This command removes all great-docs assets and configuration:

    \b
    • Deletes CSS, JavaScript, and asset files
    • Removes great-docs entries from _quarto.yml
    • Preserves your content files (*.qmd, reference/, etc.)

    Use this if you want to stop using great-docs or switch to a different
    documentation system.

    \b
    Examples:
      great-docs uninstall                  # Remove from current project
      great-docs uninstall --docs-dir site  # Remove from 'site/' directory
    """
    try:
        docs = GreatDocs(project_path=project_path, docs_dir=docs_dir)
        docs.uninstall()
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


@click.command()
@click.option(
    "--project-path",
    type=click.Path(exists=True, file_okay=False, dir_okay=True),
    help="Path to your Quarto project root directory (default: current directory)",
)
@click.option(
    "--docs-dir",
    type=str,
    help="Path to documentation directory relative to project root (e.g., 'docs', 'site')",
)
def preview(project_path, docs_dir):
    """Build and preview your documentation locally.

    This command builds your docs and starts a local server with live reload.
    Open the displayed URL in your browser to preview your site.

    Press Ctrl+C to stop the server.

    \b
    Examples:
      great-docs preview                    # Build and start preview server
      great-docs preview --docs-dir site    # Preview from 'site/' directory
    """
    try:
        docs = GreatDocs(project_path=project_path, docs_dir=docs_dir)
        docs.preview()
    except KeyboardInterrupt:
        click.echo("\n👋 Server stopped")
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


# Register commands in the desired order
cli.add_command(init)
cli.add_command(build)
cli.add_command(preview)
cli.add_command(uninstall)


@click.command()
@click.option(
    "--project-path",
    type=click.Path(exists=True, file_okay=False, dir_okay=True),
    help="Path to your project root directory (default: current directory)",
)
@click.option(
    "--docs-dir",
    type=str,
    help="Path to documentation directory relative to project root",
)
@click.option(
    "--verbose",
    "-v",
    is_flag=True,
    help="Show detailed information including %seealso and %order values",
)
def scan(project_path, docs_dir, verbose):
    """Scan docstrings for %family directives and preview API organization.

    This command analyzes your package's docstrings to find %family, %order,
    %seealso, and %nodoc directives, then shows how the API reference would
    be organized.

    Use this to preview your documentation structure before building.

    \b
    Examples:
      great-docs scan                       # Preview API organization
      great-docs scan --verbose             # Include @seealso and @order details
      great-docs scan -v                    # Short form of --verbose
    """

    try:
        docs = GreatDocs(project_path=project_path, docs_dir=docs_dir)

        # Detect package name
        package_name = docs._detect_package_name()
        if not package_name:
            click.echo("Error: Could not detect package name.", err=True)
            sys.exit(1)

        importable_name = docs._normalize_package_name(package_name)
        click.echo(f"Scanning package: {importable_name}\n")

        # Extract all directives
        directive_map = docs._extract_all_directives(importable_name)

        if not directive_map:
            click.echo("No %family directives found in docstrings.")
            click.echo("\nTo organize your API documentation, add directives to your docstrings:")
            click.echo("    %family Family Name")
            click.echo("    %order 1")
            click.echo("    %seealso other_func, AnotherClass")
            sys.exit(0)

        # Group by family
        families: dict[str, list] = {}
        nodoc_items = []

        for name, directives in directive_map.items():
            if directives.nodoc:
                nodoc_items.append(name)
                continue

            if directives.family:
                family = directives.family
                if family not in families:
                    families[family] = []
                families[family].append(
                    {
                        "name": name,
                        "order": directives.order,
                        "seealso": directives.seealso,
                    }
                )

        # Display results
        click.echo(f"Found {len(directive_map)} item(s) with directives:\n")

        # Show families
        if families:
            click.echo("📁 Families:")
            click.echo("-" * 50)

            for family_name in sorted(families.keys()):
                items = families[family_name]
                # Sort by order, then name
                items.sort(key=lambda x: (x["order"] or 999, x["name"]))

                click.echo(f"\n  {family_name} ({len(items)} item(s)):")
                for item in items:
                    order_str = f" [%order {item['order']}]" if item["order"] is not None else ""
                    click.echo(f"    • {item['name']}{order_str}")

                    if verbose and item["seealso"]:
                        seealso_str = ", ".join(item["seealso"])
                        click.echo(f"      └─ %seealso {seealso_str}")

        # Show nodoc items
        if nodoc_items:
            click.echo(f"\n🚫 Excluded (%nodoc): {len(nodoc_items)} item(s)")
            if verbose:
                for item in sorted(nodoc_items):
                    click.echo(f"    • {item}")

        # Show configuration hint
        family_config = docs._get_family_config()
        unconfigured = [
            f for f in families.keys() if docs._normalize_family_key(f) not in family_config
        ]

        if unconfigured:
            click.echo("\n💡 Tip: Add descriptions for your families in pyproject.toml:")
            click.echo("   [tool.great-docs.families.validation-steps]")
            click.echo('   title = "Family Name"')
            click.echo('   desc = "Methods for validating data."')
            click.echo("   order = 1")

    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


cli.add_command(scan)


@click.command(name="setup-github-pages")
@click.option(
    "--project-path",
    type=click.Path(exists=True, file_okay=False, dir_okay=True),
    help="Path to your project root directory (default: current directory)",
)
@click.option(
    "--docs-dir",
    type=str,
    default="docs",
    help="Path to documentation directory relative to project root (default: docs)",
)
@click.option(
    "--main-branch",
    type=str,
    default="main",
    help="Main branch name for deployment (default: main)",
)
@click.option(
    "--python-version",
    type=str,
    default="3.11",
    help="Python version for CI (default: 3.11)",
)
@click.option(
    "--force",
    is_flag=True,
    help="Overwrite existing workflow file without prompting",
)
def setup_github_pages(project_path, docs_dir, main_branch, python_version, force):
    """Set up automatic deployment to GitHub Pages.

    This command creates a GitHub Actions workflow that automatically builds
    and deploys your documentation when you push to the main branch.

    \b
    The workflow will:
    • Build docs on every push and pull request
    • Deploy to GitHub Pages on main branch pushes
    • Use Quarto's official GitHub Action for reliable builds

    After running this command, commit the workflow file and enable GitHub
    Pages in your repository settings (Settings → Pages → Source: GitHub Actions).

    \b
    Examples:
      great-docs setup-github-pages                     # Use defaults
      great-docs setup-github-pages --main-branch dev   # Deploy from 'dev' branch
      great-docs setup-github-pages --python-version 3.12
      great-docs setup-github-pages --force             # Overwrite existing workflow
    """
    from pathlib import Path

    try:
        # Determine project root
        project_root = Path(project_path) if project_path else Path.cwd()

        # Create .github/workflows directory
        workflow_dir = project_root / ".github" / "workflows"
        workflow_file = workflow_dir / "docs.yml"

        # Check if workflow file already exists
        if workflow_file.exists() and not force:
            if not click.confirm(
                f"⚠️  Workflow file already exists at {workflow_file.relative_to(project_root)}\n"
                "   Overwrite it?",
                default=False,
            ):
                click.echo("❌ Aborted. Use --force to overwrite without prompting.")
                sys.exit(1)

        # Create directory structure
        workflow_dir.mkdir(parents=True, exist_ok=True)

        # Load template
        try:
            # For Python 3.9+
            from importlib.resources import files

            template_file = files("great_docs").joinpath("assets/github-workflow-template.yml")
            template_content = template_file.read_text()
        except (ImportError, AttributeError):
            # For Python 3.8 or earlier
            from importlib_resources import files

            template_file = files("great_docs").joinpath("assets/github-workflow-template.yml")
            template_content = template_file.read_text()

        # Replace placeholders
        workflow_content = template_content.format(
            main_branch=main_branch,
            python_version=python_version,
            docs_dir=docs_dir,
        )

        # Write workflow file
        workflow_file.write_text(workflow_content)

        click.echo(
            f"✅ Created GitHub Actions workflow at {workflow_file.relative_to(project_root)}"
        )
        click.echo()
        click.echo("📋 Next steps:")
        click.echo("   1. Commit and push the workflow file to your repository")
        click.echo("   2. Go to your repository Settings → Pages")
        click.echo("   3. Set Source to 'GitHub Actions' (or 'gh-pages branch' if using that)")
        click.echo(f"   4. Push changes to '{main_branch}' branch to trigger deployment")
        click.echo()
        click.echo("💡 The workflow will:")
        click.echo(f"   • Build docs on every push to '{main_branch}' and pull requests")
        click.echo("   • Automatically deploy to GitHub Pages on main branch")
        click.echo("   • Create preview deployments for pull requests")

    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


# Register commands in the desired order
cli.add_command(setup_github_pages)


@click.command(name="check-links")
@click.option(
    "--project-path",
    type=click.Path(exists=True, file_okay=False, dir_okay=True),
    help="Path to your project root directory (default: current directory)",
)
@click.option(
    "--docs-dir",
    type=str,
    help="Path to documentation directory relative to project root",
)
@click.option(
    "--source-only",
    is_flag=True,
    help="Only check links in Python source files",
)
@click.option(
    "--docs-only",
    is_flag=True,
    help="Only check links in documentation files",
)
@click.option(
    "--timeout",
    type=float,
    default=10.0,
    help="Timeout in seconds for each HTTP request (default: 10)",
)
@click.option(
    "--ignore",
    "-i",
    multiple=True,
    help="URL pattern to ignore (can be used multiple times)",
)
@click.option(
    "--verbose",
    "-v",
    is_flag=True,
    help="Show detailed progress for each URL checked",
)
@click.option(
    "--json-output",
    is_flag=True,
    help="Output results as JSON",
)
def check_links(
    project_path, docs_dir, source_only, docs_only, timeout, ignore, verbose, json_output
):
    """Check for broken links in source code and documentation.

    This command scans Python source files and documentation (`.qmd`, `.md`)
    for URLs and checks their HTTP status. It reports broken links (404s)
    and warns about redirects.

    \b
    Default ignore patterns include:
    • localhost and 127.0.0.1 URLs
    • example.com, example.org, yoursite.com URLs
    • Placeholder URLs with brackets like [username]

    \b
    Examples:
      great-docs check-links                        # Check all links
      great-docs check-links --verbose              # Show progress for each URL
      great-docs check-links --docs-only            # Only check documentation
      great-docs check-links --source-only          # Only check source code
      great-docs check-links -i "github.com/.*#"    # Ignore GitHub anchor links
      great-docs check-links --timeout 5            # Use 5 second timeout
      great-docs check-links --json-output          # Output as JSON
    """
    import json as json_module

    try:
        docs = GreatDocs(project_path=project_path, docs_dir=docs_dir)

        # Determine what to scan
        include_source = not docs_only
        include_docs = not source_only

        # Build ignore patterns list
        ignore_patterns = list(ignore) if ignore else []
        # Add default ignore patterns
        default_ignores = [
            r"localhost",
            r"127\.0\.0\.1",
            r"0\.0\.0\.0",
            r"example\.com",
            r"example\.org",
            r"example\.net",
            r"\[",  # URLs with brackets (placeholders like [username])
            r"yoursite\.com",
            r"your-package",
            r"YOUR-USERNAME",
            r"\.git(@|$)",  # Git URLs (pip install git+...) with optional branch/tag
        ]
        ignore_patterns.extend(default_ignores)

        if not json_output:
            click.echo("🔗 Checking links...")
            if not include_source:
                click.echo("   (documentation files only)")
            elif not include_docs:
                click.echo("   (source files only)")

        results = docs.check_links(
            include_source=include_source,
            include_docs=include_docs,
            timeout=timeout,
            ignore_patterns=ignore_patterns,
            verbose=verbose,
        )

        if json_output:
            # Output as JSON
            click.echo(json_module.dumps(results, indent=2))
            sys.exit(1 if results["broken"] else 0)

        # Print summary
        click.echo("\n" + "=" * 60)
        click.echo("📊 Link Check Summary")
        click.echo("=" * 60)

        total_checked = results["total"] - len(results["skipped"])
        click.echo(f"\n   Total URLs found: {results['total']}")
        click.echo(f"   URLs checked: {total_checked}")
        click.echo(f"   URLs skipped: {len(results['skipped'])}")

        click.echo(f"\n   ✅ OK: {len(results['ok'])}")
        click.echo(f"   ↪️  Redirects: {len(results['redirects'])}")
        click.echo(f"   ❌ Broken: {len(results['broken'])}")

        # Show broken links
        if results["broken"]:
            click.echo("\n" + "-" * 60)
            click.echo("❌ Broken Links:")
            click.echo("-" * 60)
            for item in results["broken"]:
                status = item["status"] or "N/A"
                click.echo(f"\n   [{status}] {item['url']}")
                click.echo(f"   Error: {item['error']}")
                click.echo("   Found in:")
                for f in item["files"]:
                    click.echo(f"     • {f}")

        # Show redirects
        if results["redirects"]:
            click.echo("\n" + "-" * 60)
            click.echo("↪️  Redirects (consider updating):")
            click.echo("-" * 60)
            for item in results["redirects"]:
                click.echo(f"\n   [{item['status']}] {item['url']}")
                click.echo(f"   → {item['location']}")
                click.echo("   Found in:")
                for f in item["files"]:
                    click.echo(f"     • {f}")

        # Exit with error code if broken links found
        if results["broken"]:
            click.echo("\n⚠️  Found broken links. Please fix them before deployment.")
            sys.exit(1)
        else:
            click.echo("\n✅ All links are valid!")
            sys.exit(0)

    except ImportError as e:
        click.echo(f"Error: {e}", err=True)
        click.echo("\nInstall the requests package with: pip install requests", err=True)
        sys.exit(1)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


cli.add_command(check_links)


def main():
    """Main CLI entry point for great-docs."""
    cli()


if __name__ == "__main__":
    main()

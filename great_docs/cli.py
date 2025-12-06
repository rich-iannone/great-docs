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
    """Great Docs - A great way to quickly initialize your Python docs site."""
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
    """Initialize great-docs in your quartodoc project."""
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
    """Build documentation (runs quartodoc build + quarto render)."""
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
    """Remove great-docs from your quartodoc project."""
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
    """Build and serve documentation locally."""
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
    help="Show detailed information including @seealso and @order values",
)
def scan(project_path, docs_dir, verbose):
    """Scan docstrings for @family directives and preview API organization.

    This command analyzes your package's docstrings to find @family, @order,
    @seealso, and @nodoc directives, then shows how the API reference would
    be organized.

    Use this to preview your documentation structure before building.
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
            click.echo("No @family directives found in docstrings.")
            click.echo("\nTo organize your API documentation, add directives to your docstrings:")
            click.echo("    @family: Family Name")
            click.echo("    @order: 1")
            click.echo("    @seealso: other_func, AnotherClass")
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
                    order_str = f" [@order: {item['order']}]" if item["order"] is not None else ""
                    click.echo(f"    • {item['name']}{order_str}")

                    if verbose and item["seealso"]:
                        seealso_str = ", ".join(item["seealso"])
                        click.echo(f"      └─ @seealso: {seealso_str}")

        # Show nodoc items
        if nodoc_items:
            click.echo(f"\n🚫 Excluded (@nodoc): {len(nodoc_items)} item(s)")
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
    """Generate GitHub Actions workflow for deploying docs to GitHub Pages."""
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


def main():
    """Main CLI entry point for great-docs."""
    cli()


if __name__ == "__main__":
    main()

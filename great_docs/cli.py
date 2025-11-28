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
def build(project_path, docs_dir, watch):
    """Build documentation (runs quartodoc build + quarto render)."""
    try:
        docs = GreatDocs(project_path=project_path, docs_dir=docs_dir)
        docs.build(watch=watch)
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
            import importlib.resources as resources

            template_content = (
                resources.files("great_docs.assets")
                .joinpath("github-workflow-template.yml")
                .read_text()
            )
        except AttributeError:
            # For Python 3.8
            import importlib_resources as resources

            template_content = (
                resources.files("great_docs.assets")
                .joinpath("github-workflow-template.yml")
                .read_text()
            )

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

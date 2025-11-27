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


def main():
    """Main CLI entry point for great-docs."""
    cli()


if __name__ == "__main__":
    main()

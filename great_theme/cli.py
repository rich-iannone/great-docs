import sys

import click

from . import __version__
from .core import GreatTheme


@click.group()
@click.version_option(version=__version__, prog_name="great-theme")
def cli():
    """Great Theme for quartodoc - Enhanced styling for Python documentation sites."""
    pass


@cli.command()
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
def install(project_path, docs_dir, force):
    """Install great-theme to your quartodoc project."""
    try:
        theme = GreatTheme(project_path=project_path, docs_dir=docs_dir)
        theme.install(force=force)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


@cli.command()
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
    """Remove great-theme from your quartodoc project."""
    try:
        theme = GreatTheme(project_path=project_path, docs_dir=docs_dir)
        theme.uninstall()
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


@cli.command()
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
        theme = GreatTheme(project_path=project_path, docs_dir=docs_dir)
        theme.build(watch=watch)
    except KeyboardInterrupt:
        click.echo("\n👋 Stopped watching")
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


@cli.command()
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
        theme = GreatTheme(project_path=project_path, docs_dir=docs_dir)
        theme.preview()
    except KeyboardInterrupt:
        click.echo("\n👋 Server stopped")
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


def main():
    """Main CLI entry point for great-theme."""
    cli()


if __name__ == "__main__":
    main()

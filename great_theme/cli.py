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
    help="Path to your Quarto project directory (default: current directory)",
)
@click.option(
    "--force",
    is_flag=True,
    help="Overwrite existing files without prompting",
)
def install(project_path, force):
    """Install great-theme to your quartodoc project."""
    try:
        theme = GreatTheme(project_path=project_path)
        theme.install(force=force)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.option(
    "--project-path",
    type=click.Path(exists=True, file_okay=False, dir_okay=True),
    help="Path to your Quarto project directory (default: current directory)",
)
def uninstall(project_path):
    """Remove great-theme from your quartodoc project."""
    try:
        theme = GreatTheme(project_path=project_path)
        theme.uninstall()
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


def main():
    """Main CLI entry point for great-theme."""
    cli()


if __name__ == "__main__":
    main()

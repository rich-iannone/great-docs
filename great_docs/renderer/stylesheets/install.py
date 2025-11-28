import importlib.resources
import shutil
import sys
from pathlib import Path


def install(dest_dir: str | Path | None = None):
    """
    Install qrenderer stylesheets into a directory

    If dest_dir is None, the stylesheets are install into the current
    working directory.
    """
    if dest_dir is None:
        dest_dir = Path.cwd()
    elif isinstance(dest_dir, str):
        dest_dir = Path(dest_dir)

    exts = {".scss", ".css"}
    resource = importlib.resources.files("qrenderer.stylesheets")
    with importlib.resources.as_file(resource) as styles_path:
        for src in styles_path.iterdir():
            if src.suffix in exts:
                _ = shutil.copyfile(src, dest_dir / src.name)


if __name__ == "__main__":
    if len(sys.argv) > 2:
        script_name = sys.argv[0]
        print(
            f"""
Usage:
{script_name} [DIR]

Accepts at most one argument (a directory).

If no DIR is provided, the current directory is used.
The provided directory must exist.
"""
        )
        sys.exit(1)

    dest_dir = sys.argv[1] if len(sys.argv) == 2 else None
    install(dest_dir)

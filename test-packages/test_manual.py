#!/usr/bin/env python3
"""Manual test script to verify integration tests work"""

import subprocess
import sys
from pathlib import Path

TEST_PACKAGES_DIR = Path(__file__).parent
GREAT_DOCS_CMD = TEST_PACKAGES_DIR.parent / ".venv" / "bin" / "great-docs"


def test_package(package_name):
    package_dir = TEST_PACKAGES_DIR / package_name
    print(f"\n{'=' * 60}")
    print(f"Testing {package_name}")
    print(f"{'=' * 60}\n")

    # Test init
    print("Running: great-docs init --force")
    result = subprocess.run(
        [str(GREAT_DOCS_CMD), "init", "--force"],
        cwd=package_dir,
        capture_output=True,
        text=True,
        input="",
        timeout=60,
    )

    print(f"Exit code: {result.returncode}")
    if result.stdout:
        print(f"STDOUT:\n{result.stdout}")
    if result.stderr:
        print(f"STDERR:\n{result.stderr}")

    if result.returncode == 0:
        print("✓ Init succeeded")

        # Test build
        print("\nRunning: great-docs build")
        result = subprocess.run(
            [str(GREAT_DOCS_CMD), "build"],
            cwd=package_dir,
            capture_output=True,
            text=True,
            input="",
            timeout=180,
        )

        print(f"Exit code: {result.returncode}")
        if result.returncode == 0:
            print("✓ Build succeeded")
        else:
            print("✗ Build failed")
            if result.stdout:
                print(f"STDOUT:\n{result.stdout[-1000:]}")  # Last 1000 chars
            if result.stderr:
                print(f"STDERR:\n{result.stderr[-1000:]}")
    else:
        print("✗ Init failed")

    return result.returncode == 0


if __name__ == "__main__":
    packages = ["time-machine", "python-dateutil"]

    for pkg in packages:
        if (TEST_PACKAGES_DIR / pkg).exists():
            success = test_package(pkg)
            if not success:
                print(f"\n✗ {pkg} test failed")
                sys.exit(1)
        else:
            print(f"Skipping {pkg} (not found)")

    print("\n✓ All tests passed!")

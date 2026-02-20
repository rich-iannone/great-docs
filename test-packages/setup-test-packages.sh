#!/bin/bash
# Helper script to set up test packages for integration testing

set -e

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
TEST_PACKAGES_DIR="$SCRIPT_DIR"

echo "Setting up test packages for great-docs integration testing..."
echo "Target directory: $TEST_PACKAGES_DIR"
echo ""

# Create test-packages directory if it doesn't exist
mkdir -p "$TEST_PACKAGES_DIR"

# Function to clone or update a repo
setup_repo() {
    local repo_url=$1
    local repo_name=$2
    local repo_dir="$TEST_PACKAGES_DIR/$repo_name"

    if [ -d "$repo_dir" ]; then
        echo "✓ $repo_name already exists at $repo_dir"
        read -p "  Update to latest? (y/N) " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            echo "  Updating $repo_name..."
            (cd "$repo_dir" && git pull)
            echo "  ✓ Updated"
        fi
    else
        echo "Cloning $repo_name..."
        git clone "$repo_url" "$repo_dir"
        echo "✓ Cloned $repo_name"
    fi
    echo ""
}

# Small/simple packages for quick testing
echo "Small packages (fast builds):"
echo "=============================="
setup_repo "https://github.com/dateutil/dateutil" "python-dateutil"
setup_repo "https://github.com/adamchainz/time-machine" "time-machine"

echo ""
echo "Medium packages:"
echo "================"
# Setup py-shiny (large package, slower builds)
setup_repo "https://github.com/posit-dev/py-shiny" "py-shiny"

# Add more test packages here as needed
# setup_repo "https://github.com/other/package" "package-name"

echo "=========================================="
echo "Setup complete!"
echo "=========================================="
echo ""
echo "To run integration tests:"
echo "  cd .. && pytest tests/test_integration.py -v"
echo ""
echo "Or use the Makefile (from project root):"
echo "  cd .. && make test-integration"
echo ""
echo "To run tests for a specific package:"
echo "  cd .. && pytest tests/test_integration.py -v -k py-shiny"
echo ""
echo "To view generated docs for a package:"
echo "  open py-shiny/great-docs/_site/index.html"
echo ""

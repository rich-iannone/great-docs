#!/bin/bash
# Quick test to verify integration tests work

set -e

echo "Integration Test Quick Start"
echo "============================="
echo ""

# Check if py-shiny exists
if [ ! -d "py-shiny" ]; then
    echo "⚠️  py-shiny not found. Run setup first:"
    echo "    cd test-packages && ./setup-test-packages.sh"
    echo ""
    exit 1
fi

echo "✓ py-shiny found"
echo ""
echo "Running integration tests..."
echo ""

# Run from project root
cd .. && pytest tests/test_integration.py -v -k py-shiny

echo ""
echo "============================="
echo "To view the generated site:"
echo "    open test-packages/py-shiny/great-docs/_site/index.html"
echo ""

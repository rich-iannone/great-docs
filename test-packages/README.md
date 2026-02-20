# Integration Test Packages

This directory contains external Python packages used for integration testing of great-docs.

## Purpose

These tests verify that great-docs can successfully document real-world Python packages by:

1. Running `great-docs init` to initialize documentation
2. Running `great-docs build` to generate the documentation site
3. Checking for runtime failures

## Setup

### Adding a Test Package

You can use the setup script to clone test packages:

```bash
cd test-packages
./setup-test-packages.sh
```

Or clone manually:

```bash
cd test-packages
git clone https://github.com/posit-dev/py-shiny
```

### Running Tests

The integration tests are in `tests/test_integration.py`. Run them with:

```bash
# From project root
pytest tests/test_integration.py -v

# Or use the Makefile target
make test-integration

# Or use the convenience script from test-packages/
cd test-packages
./test-integration.sh
```

## Current Test Packages

### Small Packages (Fast Builds)

#### python-dateutil

- **Repository**: https://github.com/dateutil/dateutil
- **Purpose**: Extensions to the standard Python datetime module
- **Setup**: Included in `setup-test-packages.sh`
- **Build time**: ~30 seconds

#### time-machine

- **Repository**: https://github.com/adamchainz/time-machine
- **Purpose**: Time mocking library
- **Setup**: Included in `setup-test-packages.sh`
- **Build time**: ~15 seconds

### Medium/Large Packages

#### py-shiny

- **Repository**: https://github.com/posit-dev/py-shiny
- **Purpose**: Framework for reactive web apps
- **Setup**: Included in `setup-test-packages.sh`
- **Build time**: ~2-5 minutes
- **Note**: Large package, good for comprehensive testing

## Notes

- **All package subdirectories in this directory are git-ignored** (but not this README or scripts)
- The rendered documentation sites can be manually inspected in each package's `great-docs/` directory
- Tests only verify that build completes without runtime errors
- Manual inspection of the generated sites is recommended for quality assurance
- To add more test packages, update both `test-packages/setup-test-packages.sh` and the `TEST_PACKAGES` list in `tests/test_integration.py`

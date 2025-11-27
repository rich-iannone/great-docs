# Contributing to Great Docs

Thank you for your interest in contributing to Great Docs! We welcome contributions from the community.

## How to Contribute

### Reporting Issues

If you find a bug or have a suggestion for improvement:

1. Check if the issue already exists in the [issue tracker](https://github.com/rich-iannone/great-docs/issues)
2. If not, create a new issue with a clear description
3. Include steps to reproduce (for bugs) or use cases (for features)

### Submitting Pull Requests

1. Fork the repository
2. Create a new branch for your changes: `git checkout -b feature/your-feature-name`
3. Make your changes and commit them with clear, descriptive messages
4. Add tests for new functionality
5. Ensure all tests pass: `pytest`
6. Push to your fork and submit a pull request

### Development Setup

```bash
# Clone your fork
git clone https://github.com/YOUR-USERNAME/great-docs.git
cd great-docs

# Create a virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install in development mode
pip install -e ".[dev]"

# Run tests
pytest
```

### Code Style

- Follow PEP 8 guidelines
- Use meaningful variable and function names
- Add docstrings to functions and classes
- Keep functions focused and concise

## Questions?

Feel free to open an issue for questions or discussions about contributing.

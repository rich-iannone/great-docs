"""
Docstring directive extraction and stripping for Great Docs.

This module provides functionality to extract Great Docs directives from
docstrings (like @family:, @order:, @seealso:, @nodoc:) and strip them
for clean rendering in documentation.

Directives use a simple single-line format with an @ prefix:

    @directive: value

Example docstring with directives:

    def my_function():
        '''
        Short description.

        @family: Family Name
        @order: 1
        @seealso: other_func, AnotherClass

        Parameters
        ----------
        ...
        '''
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field


@dataclass
class DocDirectives:
    """
    Extracted directives from a docstring.

    Attributes
    ----------
    family
        The family/group this item belongs to (e.g., "Family Name").
    order
        Ordering within the family (lower numbers appear first).
    seealso
        List of related items to cross-reference.
    nodoc
        If True, exclude this item from documentation.
    """

    family: str | None = None
    order: int | None = None
    seealso: list[str] = field(default_factory=list)
    nodoc: bool = False

    def __bool__(self) -> bool:
        """Return True if any directive was found."""
        return bool(self.family or self.order is not None or self.seealso or self.nodoc)


# Single-line directive patterns (with @ prefix)
# Each pattern matches a complete line starting with the directive
DIRECTIVE_PATTERNS = {
    "family": re.compile(r"^\s*@family:\s*(.+?)\s*$", re.MULTILINE),
    "order": re.compile(r"^\s*@order:\s*(\d+)\s*$", re.MULTILINE),
    "seealso": re.compile(r"^\s*@seealso:\s*(.+?)\s*$", re.MULTILINE),
    "nodoc": re.compile(r"^\s*@nodoc:\s*(true|yes|1)?\s*$", re.MULTILINE | re.IGNORECASE),
}

# Combined pattern for stripping all directives (matches the whole line including newline)
ALL_DIRECTIVES_PATTERN = re.compile(
    r"^\s*@(?:family|order|seealso|nodoc):.*$\n?", re.MULTILINE | re.IGNORECASE
)


def extract_directives(docstring: str | None) -> DocDirectives:
    """
    Extract Great Docs directives from a docstring.

    Parameters
    ----------
    docstring
        The docstring to parse. Can be None.

    Returns
    -------
    DocDirectives
        A dataclass containing extracted directive values.

    Examples
    --------
    >>> doc = '''
    ... Short description.
    ...
    ... @family: Family Name
    ... @order: 1
    ... @seealso: func_a, func_b
    ...
    ... Parameters
    ... ----------
    ... x : int
    ... '''
    >>> directives = extract_directives(doc)
    >>> directives.family
    'Family Name'
    >>> directives.order
    1
    >>> directives.seealso
    ['func_a', 'func_b']
    """
    directives = DocDirectives()

    if not docstring:
        return directives

    # Extract @family
    if match := DIRECTIVE_PATTERNS["family"].search(docstring):
        directives.family = match.group(1).strip()

    # Extract @order
    if match := DIRECTIVE_PATTERNS["order"].search(docstring):
        directives.order = int(match.group(1))

    # Extract @seealso (comma-separated list)
    if match := DIRECTIVE_PATTERNS["seealso"].search(docstring):
        items = [item.strip() for item in match.group(1).split(",")]
        directives.seealso = [item for item in items if item]

    # Extract @nodoc
    if DIRECTIVE_PATTERNS["nodoc"].search(docstring):
        directives.nodoc = True

    return directives


def strip_directives(docstring: str | None) -> str:
    """
    Remove all Great Docs directives from a docstring.

    This produces a clean docstring for rendering in documentation,
    while the original docstring with directives remains in source
    code for IDE display.

    Parameters
    ----------
    docstring
        The docstring to clean. Can be None.

    Returns
    -------
    str
        The docstring with all @directive: lines removed.

    Examples
    --------
    >>> doc = '''
    ... Short description.
    ...
    ... @family: Family Name
    ... @order: 1
    ...
    ... Parameters
    ... ----------
    ... x : int
    ... '''
    >>> print(strip_directives(doc))
    Short description.
    <BLANKLINE>
    Parameters
    ----------
    x : int
    """
    if not docstring:
        return docstring or ""

    # Remove all directive lines
    cleaned = ALL_DIRECTIVES_PATTERN.sub("", docstring)

    # Clean up resulting multiple blank lines (more than 2 newlines -> 2 newlines)
    cleaned = re.sub(r"\n{3,}", "\n\n", cleaned)

    # Strip leading/trailing whitespace but preserve internal structure
    return cleaned.strip()


def has_directives(docstring: str | None) -> bool:
    """
    Check if a docstring contains any Great Docs directives.

    Parameters
    ----------
    docstring
        The docstring to check.

    Returns
    -------
    bool
        True if any @directive: pattern is found.
    """
    if not docstring:
        return False

    return bool(ALL_DIRECTIVES_PATTERN.search(docstring))

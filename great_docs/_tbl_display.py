from __future__ import annotations

from typing import Any


def enable_tbl_preview(**kwargs: Any) -> None:
    """Register `tbl_preview` as the default DataFrame display formatter.

    After calling this, any Polars or Pandas DataFrame that is the last expression in a cell (or
    passed to `display()`) will be rendered as a `tbl_preview()` table instead of the library's
    default HTML.

    Parameters
    ----------
    **kwargs
        Keyword arguments forwarded to `tbl_preview()` (e.g., `n_head=10`, `show_all=True`,
        `show_dimensions=False`).

    Examples
    --------
    In a notebook or `.qmd` file:

    ```python
    import great_docs as gd
    gd.enable_tbl_preview(n_head=8, n_tail=3)
    ```

    Now any DataFrame displayed will use `tbl_preview()` automatically:

    ```python
    import pandas as pd
    pd.read_csv("data.csv")  # rendered as a preview table
    ```
    """
    try:
        ip = _get_ipython()
    except RuntimeError:
        return

    from great_docs._tbl_preview import _is_pandas, _is_polars, tbl_preview

    def _tbl_preview_formatter(obj: Any) -> str | None:
        if _is_polars(obj) or _is_pandas(obj):
            return tbl_preview(obj, **kwargs).as_html()
        return None

    html_formatter = ip.display_formatter.formatters["text/html"]  # type: ignore[union-attr]

    # Register for known DataFrame types (if available)
    try:
        import polars as pl

        html_formatter.for_type(pl.DataFrame, _tbl_preview_formatter)
    except ImportError:
        pass

    try:
        import pandas as pd

        html_formatter.for_type(pd.DataFrame, _tbl_preview_formatter)
    except ImportError:
        pass


def disable_tbl_preview() -> None:
    """Remove the `tbl_preview` display formatter and restore defaults."""
    try:
        ip = _get_ipython()
    except RuntimeError:
        return

    html_formatter = ip.display_formatter.formatters["text/html"]  # type: ignore[union-attr]

    try:
        import polars as pl

        html_formatter.pop(pl.DataFrame, None)
    except ImportError:
        pass

    try:
        import pandas as pd

        html_formatter.pop(pd.DataFrame, None)
    except ImportError:
        pass


def _get_ipython() -> Any:
    """Get the active IPython instance or raise RuntimeError."""
    try:
        from IPython import get_ipython

        ip = get_ipython()
        if ip is None:
            raise RuntimeError("No active IPython session.")
        return ip
    except ImportError:
        raise RuntimeError("IPython is not installed.")

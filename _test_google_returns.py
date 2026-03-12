import griffe as gf

src = (
    "Process a list of items and return a summary.\n"
    "\n"
    "Iterates through the items, applies validation and\n"
    "aggregation, and returns a summary dictionary with\n"
    "counts and status information.\n"
    "\n"
    "Args:\n"
    "    items: A list of items to process. Each item should\n"
    "        be a string or convertible to string.\n"
    "    strict: If True, raise on invalid items instead of\n"
    "        skipping them. Defaults to False.\n"
    "\n"
    "Returns:\n"
    "    A dictionary with the following keys:\n"
    "\n"
    '    - ``"processed"`` -- number of successfully processed items.\n'
    '    - ``"skipped"`` -- number of skipped items (0 if strict).\n'
    '    - ``"status"`` -- ``"complete"`` or ``"partial"``.\n'
)

ds = gf.Docstring(src, parser="google")
parsed = ds.parsed
for i, section in enumerate(parsed):
    kind = section.kind
    tname = type(section).__name__
    print(f"Section {i}: kind={kind}, type={tname}")
    val = getattr(section, "value", None)
    if isinstance(val, list):
        for j, item in enumerate(val):
            n = getattr(item, "name", "")
            a = getattr(item, "annotation", "")
            d = getattr(item, "description", "")
            print(f"  [{j}] {type(item).__name__}: name={n!r} annotation={a!r} description={d!r}")
    elif val is not None:
        vstr = repr(val)
        if len(vstr) > 300:
            vstr = vstr[:300] + "..."
        print(f"  value={vstr}")

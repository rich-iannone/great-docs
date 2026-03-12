"""
gdtest_kitchen_sink_q — Kitchen sink with qrenderer enabled.

Identical to gdtest_kitchen_sink but with renderer: "q" to validate
the new rendering pipeline against the classic baseline.
"""

import copy

from .gdtest_kitchen_sink import SPEC as _BASE

SPEC = copy.deepcopy(_BASE)
SPEC["name"] = "gdtest_kitchen_sink_q"
SPEC["description"] = "Kitchen sink with qrenderer (renderer: q)"
SPEC["config"]["renderer"] = "q"

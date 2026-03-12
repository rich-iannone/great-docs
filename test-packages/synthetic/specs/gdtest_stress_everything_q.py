"""
gdtest_stress_everything_q — Stress-everything with qrenderer enabled.

Identical to gdtest_stress_everything but with renderer: "q" to validate
the new rendering pipeline against the classic baseline.
"""

import copy

from .gdtest_stress_everything import SPEC as _BASE

SPEC = copy.deepcopy(_BASE)
SPEC["name"] = "gdtest_stress_everything_q"
SPEC["description"] = "Stress-everything with qrenderer (renderer: q)"
SPEC["config"]["renderer"] = "q"

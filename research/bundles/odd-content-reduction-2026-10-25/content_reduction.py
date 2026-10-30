"""Public content-probe protocol; a genuine marked-source backend is not supplied."""

from pathlib import Path
import sys

from sympy import eye

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "cyclic-odd-degree-source-2026-10-25"))
from cyclic_source import checked_factors, crt_query


def probe_schedule(n, factors):
    """Public Sp4 queries, independent of the unknown isogeny/kernel."""
    factors = checked_factors(n, factors)
    records = []
    for p, e in factors:
        for axis, row, col in (("upper", 0, 1), ("lower", 1, 0)):
            for k in range(e+1):
                query = eye(4)
                query[row, col] = p**k
                records.append({"key": (p, axis, k), "query": crt_query(query, p**e, n)})
    return tuple(records)


def recover_content(n, factors, matches):
    """Decode exact f(query)==f(I) outcomes, CONDITIONAL on the source promise."""
    factors = checked_factors(n, factors)
    keys = {(p, axis, k) for p, e in factors
            for axis in ("upper", "lower") for k in range(e+1)}
    if set(matches) != keys or any(type(value) is not bool for value in matches.values()):
        raise ValueError("complete exact boolean comparison record required")
    components, content, residual = [], 1, 1
    for p, e in factors:
        thresholds = []
        for axis in ("upper", "lower"):
            values = [matches[(p, axis, k)] for k in range(e+1)]
            if not values[-1] or values != sorted(values):
                raise ValueError("source record fails monotone stabilizer-period promise")
            thresholds.append(values.index(True))
        depth = max(thresholds)
        if (e-depth) % 2 or any(k and (depth-k) % 2 for k in thresholds):
            raise ValueError("source record fails kernel-order/valuation parity promise")
        a = (e-depth)//2
        content *= p**a
        residual *= p**depth
        components.append({"prime": p, "input_exponent": e, "content_exponent": a,
                           "direction_exponent": depth, "thresholds": thresholds})
    if content*content*residual != n:
        raise AssertionError("degree content identity failed")
    return {"degree": n, "content": content, "cyclic_residual_degree": residual,
            "components": components, "native_source_executed": False,
            "direction_recovered": False, "source_promise_verified": False}

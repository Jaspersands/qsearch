"""Short-sum count enclosures and partial-observation simulation bounds.

The external trace-sum theorem is a mathematical import. These estimates
are not exact counters, conditional samplers, or full-word simulators.
"""
from fractions import Fraction

from theorems.balanced_codeword_filter import integer
from theorems.inverse_trace_short_sums import _q_half_power_upper


def syndrome_count_error(bits, length, checks):
    """Uniform relative error around (q/2)**length/q**checks, at EVERY h."""
    integer(bits, 2, 127, "field degree")
    integer(length, 1, min(1 << bits, 100_000), "retained length")
    integer(checks, 0, length-1, "parity checks")
    if checks == 0:
        return Fraction(0)
    return 24**length*_q_half_power_upper(1 << bits, checks+1-length)


def partial_transcript_error(bits, length, checks, observed):
    """TV upper bound for adaptive classical coordinate observations only.

At most observed distinct coordinates may be queried; repeats are cached.
The simulator samples each new coordinate independently and uniformly from
its accepted alphabet. None means the count bound cannot certify a law.
The original full syndrome can be any fixed public value. This does not
sample the unobserved completion and does not answer coherent queries.
"""
    integer(observed, 0, length, "observed coordinate cap")
    full = syndrome_count_error(bits, length, checks)
    if full >= 1:
        return None
    if observed == 0 or checks == 0:
        return Fraction(0)
    remaining = length-observed
    if remaining <= checks:
        return None
    # The bound is geometric in length; either endpoint is its maximum.
    residual = max(full, syndrome_count_error(bits, remaining, checks))
    return min(Fraction(1), (residual+full)/(2*(1-full)))

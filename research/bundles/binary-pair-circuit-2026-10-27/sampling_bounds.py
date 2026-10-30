"""Exact conservative bounds for the uniform-fiber sampling consequence.

Supplied decoder/Gram/channel bounds remain mathematical premises; this
helper does not certify a source or prove classical sampling hardness.
"""

from fractions import Fraction
from math import isqrt


def sqrt_upper(value, bits=100):
    value = Fraction(value)
    if value < 0 or type(bits) is not int or bits < 1:
        raise ValueError("nonnegative radicand and positive precision required")
    scaled = value.numerator << (2 * bits)
    root = isqrt(scaled // value.denominator)
    if root * root * value.denominator < scaled:
        root += 1
    return Fraction(root, 1 << bits)


def sampling_bound(p0, gram_upper, raw_tv_error=0, *, failure_bits=40, sqrt_bits=100):
    if any(type(x) not in (int, Fraction) for x in (p0, gram_upper, raw_tv_error)):
        raise ValueError("exact rational premise bounds required")
    p0, upper, delta = map(Fraction, (p0, gram_upper, raw_tv_error))
    if not 0 < p0 <= 1 or upper < p0:
        raise ValueError("require 0<p0<=1 and gram upper bound >=p0")
    if type(failure_bits) is not int or failure_bits < 1:
        raise ValueError("positive integer failure bits required")
    raw = p0*p0/upper
    if not 0 <= delta < raw:
        raise ValueError("whole raw-trial error must be below success margin")
    intrinsic_squared = 1 - p0/upper
    intrinsic = sqrt_upper(intrinsic_squared, sqrt_bits)
    conditioning = delta/raw
    conditional = min(Fraction(1), intrinsic + conditioning)
    abort = Fraction(1, 2**failure_bits)
    trials = Fraction(failure_bits, 1)/(raw-delta)
    cap = (trials.numerator + trials.denominator - 1)//trials.denominator
    return {"intrinsic_tv_squared_upper": intrinsic_squared,
            "intrinsic_tv_upper": intrinsic,
            "compiled_conditioning_tv_upper": conditioning,
            "verified_conditional_tv_upper": conditional,
            "abort_probability_upper": abort,
            "tv_including_abort_upper": min(Fraction(1), conditional + abort),
            "compiled_raw_success_lower": raw - delta,
            "fresh_independent_raw_trial_cap": cap,
            "exact_uniformity_claimed": False,
            "arbitrary_requested_precision_at_fixed_input": False,
            "premises_verified_by_helper": False}

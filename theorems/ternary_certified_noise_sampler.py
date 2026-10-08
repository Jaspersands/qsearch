"""Public native paired-noise rejection with rational interval decisions.

Explicit aborts are charged; conditioning away them is NOT an exact sampler.
No unknown state, hidden secret, q-square table or floating trig is used.
"""
from __future__ import annotations

from functools import lru_cache
from fractions import Fraction
import math

from flint import fmpq

from ternary_covariant_noise import root_digits
from ternary_measured_lattice_decoder import integer


def rational(value, name):
    if isinstance(value, fmpq):
        return value
    if isinstance(value, Fraction):
        return fmpq(value.numerator, value.denominator)
    if type(value) is int or type(value) is str:
        try:
            return fmpq(value)
        except (ValueError, ZeroDivisionError):
            pass
    raise ValueError(f"exact rational {name} required")


def sqrt_box(value, bits):
    x = rational(value, "nonnegative square-root argument")
    integer(bits, "positive square-root interval bits", 1)
    if x < 0:
        raise ValueError("nonnegative square-root argument required")
    scale = 2**bits
    k = math.isqrt((int(x.numerator)*scale*scale)//int(x.denominator))
    lower = fmpq(k, scale)
    upper = lower if lower*lower == x else fmpq(k+1, scale)
    return lower, upper


@lru_cache(maxsize=64)
def pi_box(bits):
    integer(bits, "positive enclosure bits", 1)
    tolerance = fmpq(1, 2**(bits+10))
    def atan_box(denominator):
        total, power, k = fmpq(0), denominator, 0
        while True:
            total += fmpq((-1)**k, (2*k+1)*power)
            k += 1
            power *= denominator**2
            next_term = fmpq((-1)**k, (2*k+1)*power)
            if abs(next_term) <= tolerance:
                return min(total, total+next_term), max(total, total+next_term), k
    a, b = atan_box(5), atan_box(239)
    lower, upper = 16*a[0]-4*b[1], 16*a[1]-4*b[0]
    if not 3 < lower <= upper < 4 or upper-lower > 20*tolerance:
        raise ArithmeticError("Machin alternating-series enclosure failed")
    return lower, upper, (a[2], b[2])


def cosine_box(q, residue, bits):
    root_digits(q)
    integer(bits, "positive cosine bits", 1)
    if type(residue) is not int:
        raise ValueError("exact integer phase required")
    residue %= q
    if residue == 0:
        return fmpq(1), fmpq(1)
    if residue in (q//3, 2*q//3):
        return fmpq(-1, 2), fmpq(-1, 2)
    residue = min(residue, q-residue)
    left, right, _ = pi_box(bits)
    angle = fmpq(residue, q)*(left+right)
    angle_error = fmpq(residue, q)*(right-left)
    term, total, remainder, k = fmpq(1), fmpq(1), fmpq(8), 0
    tolerance = fmpq(1, 2**(bits+8))
    # Taylor's Lagrange bound uses |angle|<4 and derivatives bounded by1,
    # not an assumed alternating decrease near the first terms.
    while remainder > tolerance:
        k += 1
        term *= -angle*angle/fmpq((2*k-1)*(2*k))
        total += term
        remainder *= fmpq(16, (2*k+1)*(2*k+2))
    error = remainder+angle_error
    lower, upper = max(fmpq(-1), total-error), min(fmpq(1), total+error)
    if lower > upper or upper-lower > fmpq(1, 2**bits):
        raise ArithmeticError("complete rational cosine enclosure failed")
    return lower, upper


def acceptance_box(q, pair, bits):
    pair = tuple(pair)
    if len(pair) != 2 or any(type(x) is not int or not 0 <= x < q for x in pair):
        raise ValueError("canonical public paired proposal required")
    boxes = tuple(cosine_box(q, x, bits) for x in (pair[0], pair[1], pair[0]-pair[1]))
    lower = max(fmpq(0), (3+2*sum((a for a, _ in boxes), fmpq(0)))/9)
    upper = min(fmpq(1), (3+2*sum((b for _, b in boxes), fmpq(0)))/9)
    return lower, upper


def sampler_failure_bound(max_bits=64, max_proposals=128):
    integer(max_bits, "positive coin/enclosure cap", 1)
    integer(max_proposals, "positive proposal cap", 1)
    return min(fmpq(1), fmpq(2, 3)**max_proposals+fmpq(3*max_proposals, 2**max_bits))


def certified_sample_noise(q, rng, max_bits=64, max_proposals=128, block_bits=8):
    root_digits(q)
    integer(block_bits, "positive coin block bits", 1)
    failure = sampler_failure_bound(max_bits, max_proposals)
    trace = []
    total_bits = 0
    for _ in range(max_proposals):
        pair = tuple(rng.randrange(q) for _ in range(2))
        prefix, bits, decisions = 0, 0, []
        while bits < max_bits:
            width = min(block_bits, max_bits-bits)
            draw = rng.getrandbits(width)
            if type(draw) is not int or not 0 <= draw < 2**width:
                raise ValueError("canonical random-bit block required")
            prefix = (prefix << width)+draw
            bits += width
            total_bits += width
            lower, upper = acceptance_box(q, pair, bits)
            coin_lower, coin_upper = fmpq(prefix, 2**bits), fmpq(prefix+1, 2**bits)
            decision = "ACCEPT" if coin_upper <= lower else "REJECT" if coin_lower >= upper else "REFINE"
            decisions.append({"bits": bits, "coin_prefix": prefix,
                              "acceptance_lower": str(lower), "acceptance_upper": str(upper),
                              "decision": decision})
            if decision != "REFINE":
                break
        trace.append({"proposal": pair, "decisions": decisions})
        if decision == "ACCEPT":
            return {"status": "CERTIFIED_DECISIONS_WITH_EXPLICIT_ABORT_BUDGET", "noise": pair,
                    "trace": trace, "coin_bits_read": total_bits,
                    "failure_probability_upper": str(failure),
                    "successful_channel_conditioned_on_no_abort_is_exact": False}
        if decision == "REFINE":
            return {"status": "UNKNOWN_COIN_PRECISION_CAP", "noise": None,
                    "trace": trace, "coin_bits_read": total_bits,
                    "failure_probability_upper": str(failure),
                    "successful_channel_conditioned_on_no_abort_is_exact": False}
    return {"status": "UNKNOWN_PROPOSAL_CAP", "noise": None, "trace": trace,
            "coin_bits_read": total_bits, "failure_probability_upper": str(failure),
            "successful_channel_conditioned_on_no_abort_is_exact": False}

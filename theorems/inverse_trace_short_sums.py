"""Exact arithmetic for the short-trace-sum norm acceptance argument.

This imports mathematical theorems, not proof-assistant certificates. It
certifies an IID rejection algorithm, not a seeded run or uniform output.
See research/INVERSE_TRACE_GENERAL_SEARCH.md for hypotheses and derivation.
"""
from fractions import Fraction
from math import comb, isqrt

from theorems.balanced_codeword_filter import ceil_log2_fraction, integer


def _q_half_power_upper(q, exponent):
    """Rational upper bound on q**(exponent/2), for either sign."""
    root = isqrt(q)
    root += int(root*root < q)
    power, odd = divmod(exponent, 2)
    scale = root if odd else 1
    return Fraction(scale*q**power) if power >= 0 else Fraction(scale, q**(-power))


def short_sum_certificate(bits, length, checks, zeros):
    """Use the absolute first-moment error; never clip a failed bound."""
    integer(bits, 2, 127, "field degree")
    integer(length, 2, min(1 << bits, 100_000), "block length")
    integer(checks, 1, length-1, "original parity checks")
    integer(zeros, 0, length, "zero target count")
    q, M, K = 1 << bits, length, checks
    e, s = 2*(M-K-1)+1, M-2*K-1
    result = {"status": "BOUND_INCONCLUSIVE", "bits": bits, "length": M,
              "checks": K, "zeros": zeros, "degree": e, "parameter_degree": s,
              "iid_trial_success_lower_bound": None,
              "local_trace_sum_constant": 8,
              "source": "https://arxiv.org/pdf/2512.24080v1",
              "theorem": "1.3 and proof in Section 4, with separate delta/deletion terms",
              "second_moment_source": "https://arxiv.org/pdf/2102.09730",
              "second_moment_lemma": "8.7, divisor parameter 4",
              "trace_affine_target_and_nonzero_slope_required": True,
              "uniform_factor_allocation_required": True,
              "published_theorem_import_not_formally_verified": True,
              "uniform_native_sampler": False}
    if s < 0:
        return {**result, "status": "OUTSIDE_CERTIFICATE_SCOPE"}
    error = 2*24**M*_q_half_power_upper(q, 3*K+3-M)
    result["first_moment_error_power2_upper"] = ceil_log2_fraction(error)
    lower = Fraction(q-1, q)**zeros-error
    if lower <= 0:
        return result
    C1 = (4**M-comb(M+3, 3))*comb(3*M-4, s)
    C2 = 4**(M-1)*comb(3*M-3, s+1)
    divisor_error = (2*C1*_q_half_power_upper(q, -s)
                     +2*C2*_q_half_power_upper(q, 1-s))
    second = Fraction(q, q-1)**M*comb(e+3, 3)+divisor_error
    reciprocal = second/(lower*lower)
    trials = (reciprocal.numerator+reciprocal.denominator-1)//reciprocal.denominator
    result.update(status="CERTIFIED_IID_SHORT_SUM_TRIAL_BOUND",
                  iid_trial_success_lower_bound=[1, trials],
                  expected_iid_trials_upper=trials,
                  first_moment_greater_than_half=lower > Fraction(1, 2),
                  second_moment_less_than_twice_binomial=second < 2*comb(e+3, 3),
                  divisor_error_power2_upper=ceil_log2_fraction(divisor_error)
                  if divisor_error else None)
    return result

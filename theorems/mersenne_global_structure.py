"""Exact certificates for MDS completion moments and coordinate Schmidt ranks.

These are analytic deductions, not a completion algorithm, global sampler,
tensor-network construction, hardness certificate, or native quantum run.
The generic moment routine ASSUMES balanced local Fourier moments and an
MDS dual. The canonical wrapper supplies the Mersenne family's proved bounds.
"""
import argparse
from fractions import Fraction
from hashlib import sha256
import json
from math import comb, isqrt
from pathlib import Path

from theorems.balanced_codeword_filter import ceil_log2_fraction, integer
from theorems.inverse_trace_gibbs_target import mds_character_bound
from theorems.mersenne_reciprocal_access import differential_uniformity_bound


def dyadic_sqrt_upper(value, precision):
    """Outward rational square root, without floating-point underestimation."""
    if type(value) is not Fraction or value < 0:
        raise ValueError("nonnegative exact rational required")
    integer(precision, 1, 10000, "square-root precision")
    scale = 1 << precision
    numerator = value.numerator*scale*scale
    root = isqrt(numerator//value.denominator)
    root += root*root*value.denominator < numerator
    return Fraction(root, scale)


def mds_moment_bounds(bits, length, checks, beta, fourth):
    """Bound uniform relative count error and uniform-syndrome variance.

    Premises: dual [M,K] MDS over F_(2^bits), and each normalized local
    Fourier r has r(0)=1, sum_(u!=0)|r(u)|^2=1,
    sum_(u!=0)|r(u)|^4<=fourth, max_(u!=0)|r(u)|<=beta.
    The returned numbers do not certify those premises for arbitrary input.
    Support-wise Holder bounds use shortened dimension d=w-(M-K), an
    application of Horinaga--Yamakawa's MDS Brascamp--Lieb inequality.
    """
    integer(bits, 2, 127, "field bits")
    integer(length, 2, min(1 << bits, 127**2), "length")
    integer(checks, 1, length-1, "checks")
    for value, name in ((beta, "beta"), (fourth, "fourth moment")):
        if type(value) is not Fraction or not 0 < value <= 1:
            raise ValueError(f"{name} must be an exact rational in (0,1]")
    q, t = 1 << bits, length-checks
    fourth = min(fourth, beta*beta)
    if beta*beta*(q-1) < 1 or fourth*(q-1) < 1:
        raise ValueError("moment premises contradict nonzero-frequency Parseval")
    root_fourth = dyadic_sqrt_upper(fourth, bits)
    root_q = isqrt(q)+int(isqrt(q)**2 != q)
    uniform = variance = Fraction(0)
    for weight in range(t+1, length+1):
        dimension = weight-t
        if weight >= 2*t:
            squared = fourth**t
        else:
            squared = fourth**dimension*beta**(2*(2*t-weight))
        squared = min(squared, beta**(2*t), (q**dimension-1)*beta**(2*weight))
        if weight > 2*t:
            absolute = Fraction(root_q**(weight-2*t))
        elif 3*weight >= 4*t:
            absolute = root_fourth**(2*t-weight)
        else:
            absolute = fourth**dimension*beta**(4*t-3*weight)
        if weight <= 2*t:
            absolute = min(absolute, beta**(2*t-weight))
        absolute = min(absolute, (q**dimension-1)*beta**weight)
        uniform += comb(length, weight)*absolute
        variance += comb(length, weight)*squared
    old_uniform = mds_character_bound(bits, length, checks, beta)
    parseval_uniform = (sum((comb(length, j)*beta**(length-2*checks+j)
                            for j in range(checks)), Fraction(0))
                        if length >= 2*checks else None)
    mean_count = Fraction(q**t, 1 << length)
    return {
        "bits": bits, "length": length, "checks": checks, "free_symbols": t,
        "beta": beta, "fourth_moment_upper": fourth,
        "uniform_error_upper": min(uniform, old_uniform),
        "uniform_error_moment_upper": uniform,
        "uniform_error_old_upper": old_uniform,
        "uniform_error_parseval_upper": parseval_uniform,
        "syndrome_variance_upper": variance,
        "mean_completion_count": mean_count,
        "syndrome_variance_integer_lower": max(Fraction(0), 1/mean_count-1),
        "generic_mds_and_moment_premises_assumed": True,
        "all_syndromes_nonempty_certified": min(uniform, old_uniform) < 1,
        "completion_solver_implemented": False,
    }


def canonical_moments(bits, remaining):
    delta = differential_uniformity_bound(bits)
    q, checks, s = 1 << bits, bits*bits//8, (bits-3)//4
    integer(remaining, checks+1, bits*bits, "remaining coordinates")
    beta = Fraction(1+(1 << s)*(isqrt(q)+1), q)
    return mds_moment_bounds(bits, remaining, checks, beta, Fraction(delta, q))


def single_term_importance_certificate(bits, remaining):
    """Exact native-family lower bounds for an unbiased single-term estimator.

    For M remaining symbols and t=M-K, B=q^-t*(1+1/a)^M bounds 1+L
    from below, where L is the nonzero dual coefficients' absolute mass.
    Even granting the optimal proposal, E[(X-1)^2]>=L^2. The relative
    variance bound requires the ACTUAL g_y in [1/2,3/2]; that condition
    is not certified for every syndrome here. Small syndrome variance can
    make the biased constant estimate 1 useful despite this obstruction.
    No spectrum, field table, conditional count, or native solver is built.
    """
    differential_uniformity_bound(bits)
    q, length, checks, s = 1 << bits, bits*bits, (bits*bits-1)//8, (bits-3)//4
    integer(remaining, checks, length, "remaining coordinates")
    t = remaining-checks
    numerator = 2*((1 << s)-1)*(isqrt(q)+1)+3
    a = Fraction(numerator, q)
    b_lower = Fraction((q+numerator)**remaining, q**t*numerator**remaining)
    l_lower = max(Fraction(0), b_lower-1)
    second_moment = l_lower*l_lower
    return {
        "bits": bits, "length": length, "checks": checks, "s": s,
        "remaining": remaining, "free_symbols": t,
        "A": numerator, "a": a, "B_lower": b_lower, "L_lower": l_lower,
        "second_moment_lower": second_moment,
        "relative_variance_lower": max(Fraction(0), (4*second_moment-1)/9),
        "relative_variance_g_interval": (Fraction(1, 2), Fraction(3, 2)),
        "bound_scope": "unbiased single-term estimator and independent arithmetic mean only",
        "optimal_proposal_access_granted": True,
        "relative_variance_requires_g_interval": True,
        "all_syndromes_in_g_interval_certified": False,
        "all_estimator_hardness_claimed": False,
        "native_solver_implemented": False,
        "field_tables_materialized": False,
    }


def coordinate_schmidt_certificate(bits, trace_distance=Fraction(1, 10)):
    """Uniform-instance analytic bound, not a numerically constructed state.

    Uses the existing all-syndrome/all-pattern bounds on 4K and 4K+1
    coordinates, not the new moment lemma. Covers whole-coordinate orderings
    and qubit layouts keeping each field symbol contiguous, not arbitrary
    interleavings or general samplers. Pure-state trace distance is intended.
    """
    differential_uniformity_bound(bits)
    if type(trace_distance) is not Fraction or not 0 <= trace_distance < 1:
        raise ValueError("exact rational pure-state trace distance in [0,1) required")
    q, length, checks, s = 1 << bits, bits*bits, bits*bits//8, (bits-3)//4
    left, right, radius = 4*checks, 4*checks+1, 3*length//5
    beta = Fraction(1+(1 << s)*(isqrt(q)+1), q)
    eta = [mds_character_bound(bits, m, checks, beta) for m in (left, right, length)]
    if any(e >= 1 for e in eta):
        raise ArithmeticError("nonempty syndrome-pattern sectors not certified")
    kappa = (1+eta[0])*(1+eta[1])/(1-eta[2])
    fraction = (1-trace_distance**2)/kappa
    return {
        "bits": bits, "length": length, "checks": checks,
        "left_coordinates": left, "right_coordinates": right, "radius": radius,
        "syndrome_sector_count_log2": bits*checks,
        "uniform_native_rank": {"power_of_two": bits*checks, "multiplier": 1},
        "radius_filtered_rank": {"power_of_two": bits*checks, "multiplier": length-radius+1},
        "squared_schmidt_coefficient_upper": kappa/Fraction(q**checks),
        "pure_trace_distance": trace_distance,
        "required_rank_power2_lower": bits*checks-ceil_log2_fraction(1/fraction),
        "bound_scope": "every ordering of whole field coordinates, before and after local Fourier",
        "covers_arbitrary_qubit_interleavings": False,
        "sampling_hardness_claimed": False,
        "global_sampler_implemented": False,
        "native_state_materialized": False,
    }


def build_global_structure_report():
    rows = []
    importance = []
    for bits in (17, 31, 61):
        length, checks = bits*bits, bits*bits//8
        for remaining in (checks+(4*checks+bits-1)//bits, 2*checks+1,
                          2*checks+(8*checks+bits-1)//bits):
            bounds = canonical_moments(bits, remaining)
            rows.append({
                "bits": bits, "checks": checks, "remaining": remaining,
                "fixed_coordinates": length-remaining,
                "uniform_error_power2_upper": ceil_log2_fraction(bounds["uniform_error_upper"]),
                "old_uniform_error_power2_upper": ceil_log2_fraction(bounds["uniform_error_old_upper"]),
                "syndrome_variance_power2_upper": ceil_log2_fraction(bounds["syndrome_variance_upper"]),
                "mean_count_log2": bits*(remaining-checks)-remaining,
                "all_syndromes_nonempty_certified": bounds["all_syndromes_nonempty_certified"],
                "completion_solver_implemented": False,
            })
        certificate = single_term_importance_certificate(bits, checks+(4*checks+bits-1)//bits)
        for key in ("B_lower", "L_lower", "second_moment_lower", "relative_variance_lower"):
            value = certificate.pop(key)
            certificate[key.replace("_lower", "_power2_lower")] = (
                -ceil_log2_fraction(1/value) if value else None)
        a = certificate["a"]
        certificate["a"] = [a.numerator, a.denominator]
        certificate["relative_variance_g_interval"] = [
            [v.numerator, v.denominator] for v in certificate["relative_variance_g_interval"]]
        importance.append(certificate)
    schmidt = []
    for bits in (17, 31, 61):
        row = coordinate_schmidt_certificate(bits)
        row["squared_schmidt_coefficient_power2_upper"] = ceil_log2_fraction(
            row.pop("squared_schmidt_coefficient_upper"))
        distance = row["pure_trace_distance"]
        row["pure_trace_distance"] = [distance.numerator, distance.denominator]
        schmidt.append(row)
    root = Path(__file__).resolve().parents[1]
    sources = (
        "theorems/mersenne_global_structure.py", "tests/test_mersenne_global_structure.py",
        "theorems/mersenne_reciprocal_access.py", "theorems/inverse_trace_gibbs_target.py",
        "research/MERSENNE_COMPLETION_MOMENTS.md", "research/MERSENNE_COORDINATE_SCHMIDT_FILTER.md",
        "research/audits/reviews/2026-10-30-mersenne-conditional-estimator.md",
    )
    return {
        "status": "ANALYTIC_GLOBAL_STRUCTURE_NOT_A_NATIVE_SOLVER",
        "completion_bounds": rows, "coordinate_schmidt_bounds": schmidt,
        "single_term_importance_bounds": importance,
        "field_tables_materialized": False, "quantum_advantage_claimed": False,
        "hardness_claimed": False, "native_solver_implemented": False,
        "source_sha256": {p: sha256((root/p).read_bytes()).hexdigest() for p in sources},
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args(argv)
    payload = json.dumps(build_global_structure_report(), indent=2, sort_keys=True)+"\n"
    if args.output is None:
        print(payload, end="")
    else:
        args.output.write_text(payload, encoding="ascii")


if __name__ == "__main__":
    main()

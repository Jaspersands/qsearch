"""Bounded primitives for explicitly tagged Mersenne reciprocal-trace inputs.

For odd 3 <= n <= 127, 1 <= s < n, gcd(s,n)=1, and d=2^s-1, require
sum_i alpha_i^j x_i = 0 (0 <= j < K) and f_s(x_i)=Tr(inv0(x_i)^d)=b_i
on distinct public points, with inv0(0)=0. The s=1 subcase is the old
inverse trace, s=2 is inverse cubic, and s=floor((n-3)/4) is the growing-genus
research hypothesis (only when the stated contracts hold). No novelty,
quantum advantage, or classical hardness is claimed for any subcase.

gcd(d,q-1)=2^gcd(s,n)-1=1 makes u -> u^(-d_inverse mod (q-1)), with
zero mapped to zero, a bijection from each trace hyperplane to a local
fiber. It costs polynomial field arithmetic, but does not solve Hx=0.
For k=s^(-1) mod n, d_inverse is sum_{j=0}^{k-1} 2^(j*s mod n), so its
binary weight is k and the reciprocal root power has weight n-k. Report
that actual degree even for low-degree root maps such as (n,s)=(17,4).
The predicate has Boolean degree n-s: its trace polynomial has n distinct
cyclic rotations of the exponent q-2^s, all of binary weight n-s.

For u!=0, y^2+y=x^-d+u*x has poles of odd orders d and 1. Its smooth
projective completion has genus (d+1)/2=2^(s-1) and q+W(u) rational points,
where W includes x=0 with sign +1. Hasse-Weil gives
|W(u)-1| <= 2^s*sqrt(q), hence |W(u)| <= 1+2^s*sqrt(q).
The two-pole assertion excludes u=0. Finite controls are not proofs.

Generic classical point counting polynomial in genus is exponential in s;
for growing s this is NOT polynomial classical Walsh/source access. The
ideal budget is conditional on paid exact coherent known-source preparation,
complete reversible list decoding, clean fixed-padding projection, and final
native verification. No quantum algorithm or circuit is implemented here.
"""
import argparse
from fractions import Fraction
import hashlib
import json
from math import gcd, isqrt
from pathlib import Path

from flint import fmpz

from theorems.balanced_codeword_filter import ceil_log2_fraction, integer
from theorems.balanced_filter_channel_audit import projection_size
from theorems.explicit_quadratic_opi import element, encoded, field
from theorems.inverse_trace_gibbs_target import mds_character_bound
from theorems.inverse_trace_smt import validate_instance as _validate_arithmetic_shape


PROBLEM_FAMILY = "mersenne_reciprocal_trace_v1"
SCHEMA_VERSION = 1
_INSTANCE_KEYS = frozenset({
    "problem_family", "schema_version", "bits", "s", "points", "targets",
    "checks", "field_modulus_coefficients",
})


def _parameters(bits, s):
    integer(bits, 3, 127, "field bits")
    if bits % 2 == 0:
        raise ValueError("odd field degree required")
    integer(s, 1, bits-1, "Mersenne parameter s")
    if gcd(s, bits) != 1:
        raise ValueError("gcd(s,n)=1 required for the balanced permutation")
    return (1 << s)-1


def _metadata(bits, s):
    d = _parameters(bits, s)
    order = (1 << bits)-1
    d_inverse = pow(d, -1, order)
    root_power = (-d_inverse) % order
    weight = root_power.bit_count()
    prime_degree = bool(fmpz(bits).is_prime())
    canonical = prime_degree and bits >= 17 and s == (bits-3)//4
    role = "OTHER_VALID_PARAMETER"
    if s == 1:
        role = "LEGACY_INVERSE_TRACE_SUBCASE"
    elif s == 2:
        role = "CUBIC_SUBCASE"
    elif canonical:
        role = "CANONICAL_GROWING_GENUS_CANDIDATE"
    if (bits, s) == (17, 4):
        role = "LOW_DEGREE_ROOT_CONTROL_N17_S4"
    return {
        "problem_family": PROBLEM_FAMILY, "schema_version": SCHEMA_VERSION,
        "bits": bits, "s": s, "exponent": d,
        "predicate": f"Tr(inv0(x)^{d})", "inv0_at_zero": 0,
        "predicate_degree": bits-s, "s_inverse_mod_n": pow(s, -1, bits),
        "d_inverse": d_inverse, "d_inverse_binary_weight": d_inverse.bit_count(),
        "root_power": root_power, "root_power_binary_weight": weight,
        "root_map_degree_label": f"BOOLEAN_VECTOR_DEGREE_{weight}",
        "canonical_growing_s": (bits-3)//4, "parameter_role": role,
        "prime_field_degree": prime_degree,
        "matches_growing_s_formula": s == (bits-3)//4,
        "canonical_research_parameters": canonical,
    }


def _sequence(values, name):
    if type(values) not in (list, tuple):
        raise ValueError(f"{name} must be a list or tuple")


def validate_instance(instance):
    """Reject untagged, missing-s, extra-field, or noncanonical instances.

    Only backend arithmetic/modulus and basic shape validation is delegated
    to the old validator. No legacy predicate, verifier, or bound is used.
    Returns (bits, s, points, targets, checks).
    """
    if type(instance) is not dict or set(instance) != _INSTANCE_KEYS:
        raise ValueError("exact Mersenne reciprocal instance schema required")
    if (type(instance["problem_family"]) is not str
            or instance["problem_family"] != PROBLEM_FAMILY):
        raise ValueError("wrong problem_family: mersenne_reciprocal_trace_v1 required")
    integer(instance["schema_version"], SCHEMA_VERSION, SCHEMA_VERSION, "schema version")
    bits, s = instance["bits"], instance["s"]
    _parameters(bits, s)
    points, targets = instance["points"], instance["targets"]
    _sequence(points, "points")
    _sequence(targets, "targets")
    integer(len(points), 2, min(1 << bits, 100_000), "length")
    if len(targets) != len(points):
        raise ValueError("target length must match point length")
    integer(instance["checks"], 1, len(points)-1, "parity checks")
    for point in points:
        integer(point, 0, (1 << bits)-1, "field point")
    for target in targets:
        integer(target, 0, 1, "target bit")
    modulus = instance["field_modulus_coefficients"]
    if type(modulus) is not list or len(modulus) != bits+1:
        raise ValueError("canonical backend modulus coefficient list required")
    for coefficient in modulus:
        integer(coefficient, 0, 1, "modulus coefficient")
    bits, points, targets, checks = _validate_arithmetic_shape(instance)
    return bits, s, points, targets, checks


def make_instance(bits, s, points, targets, checks):
    """Explicitly construct this parameter-bound family, without a witness."""
    _parameters(bits, s)
    _sequence(points, "points")
    _sequence(targets, "targets")
    integer(len(points), 2, min(1 << bits, 100_000), "length")
    if len(targets) != len(points):
        raise ValueError("target length must match point length")
    instance = {
        "problem_family": PROBLEM_FAMILY, "schema_version": SCHEMA_VERSION,
        "bits": bits, "s": s, "points": list(points), "targets": list(targets),
        "checks": checks,
        "field_modulus_coefficients": list(map(int, field(bits).modulus().coeffs())),
    }
    validate_instance(instance)
    return instance


def _canonical_parameters(bits):
    integer(bits, 17, 127, "native field bits")
    if not fmpz(bits).is_prime():
        raise ValueError("native research fixture requires prime field degree")
    s = (bits-3)//4
    return s, bits-4*s


def native_instance(bits=17, *, s=None):
    """Prime n>=17, N=n^2, K=floor(N/8), all-one fixture; no hidden witness.

    The default s=floor((n-3)/4) must still pass the ordinary contracts.
    Explicit low-degree choices remain allowed. No primality search, random
    point sampling, field enumeration, or curve construction is performed.
    """
    canonical_s, _ = _canonical_parameters(bits)
    s = canonical_s if s is None else s
    _parameters(bits, s)
    length = bits*bits
    return make_instance(bits, s, list(range(length)), [1]*length, length//8)


def partial_norm_value(bits, word):
    """Canonical quartic permutation Phi(t), NOT a parity-preserving transfer.

    With n=4s+r, Phi(t)=(product_{j=0}^3 t^(2^(j*s)))^(2^r) satisfies
    f_s(Phi(t))=Tr(t^(2^r-1)). Thus local predicates become cubic/quintic,
    but H*Phi(t)=0 becomes quartic, not linear. Zero is included exactly.
    """
    s, remainder = _canonical_parameters(bits)
    integer(word, 0, (1 << bits)-1, "field element")
    power, value = element(bits, word), field(bits).one()
    for _ in range(4):
        value *= power
        power = power**(1 << s)
    return encoded(value**(1 << remainder))


def reciprocal_value(bits, s, word):
    """Return inv0(word)^(2^s-1) in canonical polynomial-basis encoding."""
    d = _parameters(bits, s)
    integer(word, 0, (1 << bits)-1, "field element")
    return encoded(element(bits, word)**((1 << bits)-1-d))


def reciprocal_trace(bits, s, word):
    """Parameter-bound predicate, including f_s(0)=0; no acceptance table."""
    return int(element(bits, reciprocal_value(bits, s, word)).trace())


def root_from_trace(bits, s, u, target):
    """Bijection from Tr(u)=target to f_s(x)=target, preserving zero.

    Exact uniform hyperplane input gives exact uniform LOCAL roots. Binary
    powering costs O(n) field multiplications plus polynomial integer work
    for d_inverse, even for growing s. There is no O(q) table setup.
    """
    d = _parameters(bits, s)
    integer(u, 0, (1 << bits)-1, "trace hyperplane element")
    integer(target, 0, 1, "target bit")
    if int(element(bits, u).trace()) != target:
        raise ValueError("u is outside the requested trace hyperplane")
    if u == 0:
        return 0
    exponent = (-pow(d, -1, (1 << bits)-1)) % ((1 << bits)-1)
    return encoded(element(bits, u)**exponent)


def root_from_seed(bits, s, target, seed):
    """Bijection from n-1 uniform bits to accepted LOCAL roots.

    Tr(1)=1 for odd n, so the constant coefficient uniquely fixes the trace.
    Recover the seed as reciprocal_value(bits,s,root) >> 1. This classical
    local sampler is not an implemented coherent source or native sampler,
    nor does it supply classical Fourier amplitudes.
    """
    _parameters(bits, s)
    integer(target, 0, 1, "target bit")
    integer(seed, 0, (1 << (bits-1))-1, "root seed")
    u = seed << 1
    u ^= int(element(bits, u).trace()) ^ target
    return root_from_trace(bits, s, u, target)


def verify_word(instance, values):
    """Independently check every H row and the s-bound reciprocal predicate.

    Malformed symbols raise ValueError; a well-formed nonwitness returns
    False. Cost is O(N*K + N*n) field operations; H is streamed, not stored.
    """
    bits, s, points, targets, checks = validate_instance(instance)
    _sequence(values, "witness")
    if len(values) != len(points):
        return False
    for value in values:
        integer(value, 0, (1 << bits)-1, "witness symbol")
    syndrome = [field(bits).zero() for _ in range(checks)]
    predicates_match = True
    for point, value, target in zip(points, values, targets, strict=True):
        alpha, x, power = element(bits, point), element(bits, value), field(bits).one()
        for j in range(checks):
            syndrome[j] += power*x
            power *= alpha
        predicates_match &= reciprocal_trace(bits, s, value) == target
    return all(value == 0 for value in syndrome) and predicates_match


def _binomial_prefix(length, radius):
    coefficient = total = 1
    for j in range(1, radius+1):
        coefficient = coefficient*(length-j+1)//j
        total += coefficient
    return total


def ideal_budget(instance, radius):
    """Exact rational conditional ideal per-attempt bound, not a run result.

    Balance and the local Walsh bound give |lambda_b-1| <= eta via the
    existing MDS character bound. For the support ball of radius r,
    tau=Pr[Bin(N,1/2)<=r] exactly. Clean full-list projection with public
    padding P gives native success lambda_b*tau^2/P, hence the lower bound
    max(0,1-eta)*tau^2/P. Only conditioned on native success (not merely
    heralding) is the ideal output uniform over the original native fiber.
    This uses the unnormalized source-filter protocol, not a preconditioned
    normalized-ball source. No field/curve/codeword table is constructed.
    """
    bits, s, points, _, checks = validate_instance(instance)
    length, q = len(points), 1 << bits
    integer(radius, 0, length-1, "decoder radius")
    johnson_gap = (length-radius)**2-length*(checks-1)
    if johnson_gap <= 0:
        raise ValueError("strict Johnson agreement required")
    ceil_sqrt_q = isqrt(q)+int(isqrt(q)**2 != q)
    beta = min(Fraction(1), Fraction(1+(1 << s)*ceil_sqrt_q, q))
    eta = mds_character_bound(bits, length, checks, beta)
    tau = Fraction(_binomial_prefix(length, radius), 1 << length)
    padding = projection_size(length, checks, radius, q**checks)
    return {
        **_metadata(bits, s),
        "proof_scope": "CONDITIONAL_IDEAL_BOUND_NOT_QUANTUM_IMPLEMENTATION",
        "length": length, "checks": checks, "radius": radius,
        "genus": 1 << (s-1), "johnson_gap": johnson_gap,
        "beta": beta, "eta": eta, "tau": tau, "tail": 1-tau, "padding": padding,
        "native_success_per_attempt_lower": max(Fraction(0), 1-eta)*tau**2/padding,
        "ideal_output_conditioned_on_native_success_is_uniform": True,
        "conditional_uniformity_requires_positive_native_success": True,
        "requires_paid_known_source_preparation": True,
        "requires_complete_reversible_list_decoder": True,
        "requires_clean_fixed_padding_projection": True,
        "requires_final_native_verification": True,
        "source_premise": "exact signed root-product Fourier source; clean uncomputation",
        "projection_premise": "fixed public padding; erase all message/list/index/work records",
        "root_arithmetic_cost": "O(N*n) field operations plus polynomial integer work",
        "source_access_model": "paid coherent root preparation and Fourier transform, not a classical Walsh oracle",
        "source_additional_cost": "coherent compilation, Fourier operations and cleanup must be charged",
        "verification_arithmetic_cost": "O(N*K + N*n) field operations",
        "field_operation_bit_cost": "polynomial in n; arithmetic is not unit-cost/free",
        "decoder_cost": "complete reversible list construction and cleanup must be charged",
        "generic_classical_point_count_cost": "polynomial in genus is exponential in s; canonical s grows linearly in n",
        "polynomial_classical_walsh_access_established": False,
        "polynomial_classical_source_access_claimed": False,
        "quantum_premises_verified": False,
        "full_quantum_algorithm_implemented": False,
        "field_tables_materialized": False, "curves_materialized": False,
        "novelty_claimed": False, "quantum_advantage_claimed": False,
        "classical_hardness_claimed": False,
        "n3_s2_linear_dequantized": (bits, s) == (3, 2),
        "predicate_binary_linear": s == bits-1,
    }


def finite_curve_count(bits, s, u):
    """Count affine (x!=0,y) and add the two smooth rational pole points.

    Strictly n<=5 (genus<=8); u=0 is NOT a two-pole instance. This counts
    the smooth completion, not a singular cleared-denominator plane model.
    O(q^2) arithmetic is confined to this control; no formal curve is built.
    """
    d = _parameters(bits, s)
    integer(bits, 3, 5, "finite curve control bits")
    integer(u, 1, (1 << bits)-1, "nonzero two-pole coefficient")
    q, coefficient = 1 << bits, element(bits, u)
    affine = 0
    for word in range(1, q):
        x = element(bits, word)
        rhs = x**(-d)+coefficient*x
        for label in range(q):
            y = element(bits, label)
            affine += y*y+y == rhs
    return affine+2


def finite_walsh_control(bits, s):
    """Exhaustive q<=32, genus<=8 control; never called by ideal_budget."""
    d = _parameters(bits, s)
    integer(bits, 3, 5, "finite Walsh control bits")
    q = 1 << bits
    walsh = tuple(sum(
        1-2*(reciprocal_trace(bits, s, x)
             ^ int((element(bits, u)*element(bits, x)).trace()))
        for x in range(q)) for u in range(q))
    counts = {u: finite_curve_count(bits, s, u) for u in range(1, q)}
    return {
        **_metadata(bits, s),
        "proof_scope": "BOUNDED_FINITE_CONTROL_NOT_ASYMPTOTIC_PROOF",
        "walsh": walsh, "parseval_sum": sum(w*w for w in walsh),
        "curve_counts": counts, "genus": 1 << (s-1), "pole_orders": (d, 1),
        "u_zero_excluded_from_curve_count": True,
        "curve_identity_checked": all(counts[u] == q+walsh[u] for u in counts),
        "hasse_weil_checked": all((walsh[u]-1)**2 <= (1 << (2*s))*q for u in counts),
        "exponential_control": True, "formal_curve_materialized": False,
        "novelty_claimed": False, "quantum_advantage_claimed": False,
        "classical_hardness_claimed": False,
    }


def functional_degree_control(bits, s):
    """Exact polynomial-basis Boolean ANF control, strictly capped at n<=7.

    Measures the total FUNCTION, including zero, not the rational formula.
    For s=2 the n=3,5,7 degrees are 1,3,5. When s=n-1, f_s(x)=Tr(x)
    by Frobenius invariance, so the entire coupled problem is binary linear.
    No general classical hardness inference follows from nonlinear degree.
    """
    _parameters(bits, s)
    integer(bits, 3, 7, "finite functional control bits")
    coefficients = [reciprocal_trace(bits, s, x) for x in range(1 << bits)]
    for bit in range(bits):
        for mask in range(1 << bits):
            if mask & (1 << bit):
                coefficients[mask] ^= coefficients[mask ^ (1 << bit)]
    degree = max(mask.bit_count() for mask, c in enumerate(coefficients) if c)
    classification = "LINEAR_DEQUANTIZED" if degree == 1 else "FINITE_NONLINEAR_CONTROL"
    if (bits, s) == (3, 2):
        classification = "LINEAR_DEQUANTIZED_N3_S2"
    return {
        **_metadata(bits, s),
        "proof_scope": "BOUNDED_FUNCTIONAL_DEGREE_CONTROL",
        "algebraic_degree": degree,
        "anf_support": tuple(mask for mask, c in enumerate(coefficients) if c),
        "classification": classification,
        "coupled_problem_binary_linear": degree == 1,
        "exponential_control": True,
        "novelty_claimed": False, "quantum_advantage_claimed": False,
        "classical_hardness_claimed": False,
    }


def analytic_report():
    """Replay bounded analytic certificates, not quantum executions or searches.

    Huge exact fractions are computed but serialized as outward dyadic bounds.
    The point/target recipe, backend modulus and canonical input hash bind each
    row to a reproducible input. No full-field or witness enumeration occurs.
    """
    rows = []
    for bits in (17, 31, 61):
        instance = native_instance(bits)
        budget = ideal_budget(instance, 3*bits*bits//5)
        lower = budget["native_success_per_attempt_lower"]
        numerator = lower.numerator*(1 << 128)//lower.denominator
        q, length = 1 << bits, bits*bits
        oil_upper = (1+budget["eta"])*Fraction(q, q-1)**length/q**instance["checks"]
        _, remainder = _canonical_parameters(bits)
        rows.append({
            key: budget[key] for key in (
                "problem_family", "schema_version", "bits", "s", "exponent",
                "length", "checks", "radius", "genus", "predicate_degree",
                "root_power", "root_power_binary_weight", "parameter_role",
                "canonical_research_parameters", "prime_field_degree",
                "johnson_gap", "padding", "proof_scope",
            )
        } | {
            "points_recipe": "integers 0 through n*n-1 in the recorded polynomial basis",
            "targets_recipe": "all one; bounds also hold for arbitrary target bits",
            "field_modulus_coefficients": instance["field_modulus_coefficients"],
            "instance_sha256": hashlib.sha256(json.dumps(
                instance, sort_keys=True, separators=(",", ":")
            ).encode("ascii")).hexdigest(),
            "beta": [budget["beta"].numerator, budget["beta"].denominator],
            "eta_power2_upper": ceil_log2_fraction(budget["eta"]),
            "tail_power2_upper": ceil_log2_fraction(budget["tail"]),
            "ideal_native_success_lower": [numerator, 1 << 128],
            "ideal_native_success_above_one_ninth": lower > Fraction(1, 9),
            "classical_completion_success": "lambda_b * 2^(-checks)",
            "classical_completion_accepted_law": "exactly uniform on the native fiber",
            "independent_uniform_oil_success_power2_upper": ceil_log2_fraction(oil_upper),
            "common_oil_all_ones_excluded": True,
            "lifted_affine_dimension_upper": min(instance["s"], remainder+4),
            "quartic_partial_norm_local_predicate_degree": remainder,
            "partial_norm_preserves_original_linear_parity": False,
            "native_quantum_execution": False,
            "native_classical_search_execution": False,
        })
    root = Path(__file__).resolve().parents[1]
    sources = (
        "theorems/mersenne_reciprocal_curve.py",
        "theorems/balanced_codeword_filter.py",
        "theorems/balanced_filter_channel_audit.py",
        "theorems/inverse_trace_gibbs_target.py",
        "theorems/inverse_trace_smt.py",
        "theorems/explicit_quadratic_opi.py",
        "research/EXACT_PREDICATE_CHANNEL.md",
        "research/MERSENNE_RECIPROCAL_RESEARCH_TARGET.md",
    )
    return {
        "problem_family": PROBLEM_FAMILY, "schema_version": SCHEMA_VERSION,
        "status": "ANALYTIC_NEW_RELATION_CLASSICAL_ATTACKS_OPEN",
        "source_sha256": {path: hashlib.sha256((root/path).read_bytes()).hexdigest()
                          for path in sources},
        "replay": "python -m theorems.mersenne_reciprocal_curve",
        "native_budgets": rows,
        "controls": {
            "n17_s4_root_degree": _metadata(17, 4)["root_power_binary_weight"],
            "n3_s2_predicate_degree": functional_degree_control(3, 2)["algebraic_degree"],
            "n3_s2_coupled_problem_binary_linear": True,
        },
        "changed_predicate_not_original_inverse_trace": True,
        "classical_hardness_established": False,
        "quantum_advantage_established": False,
        "novelty_established": False,
        "compiled_quantum_algorithm": False,
        "independent_human_peer_review_complete": False,
        "obligations": [
            "Attack the coupled binary quadratic and Frobenius-ratio equations.",
            "Local Walsh access is constructed; test global Fourier-output sampling or native completion.",
            "Seek a meaningful reduction without changing the input or adding an oracle.",
            "Pay coherent source, complete decoder, clean fixed padding, and gate errors.",
        ],
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, help="write the bounded analytic report to this path")
    args = parser.parse_args(argv)
    payload = json.dumps(analytic_report(), indent=2)+"\n"
    if args.output is None:
        print(payload, end="")
    else:
        args.output.write_text(payload, encoding="ascii")


if __name__ == "__main__":
    main()

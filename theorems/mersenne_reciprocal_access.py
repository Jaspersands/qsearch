"""Bounded access controls for the tagged Mersenne reciprocal family.

Differential ranks and individual quadratic Gauss blocks use polynomial
field arithmetic. Full Walsh spectra explicitly cost exponential time and
space and are capped at n=17. Neither interface supplies a coupled solver.
Completion budgets are conditional rational certificates, not executions.
Clipped Fourier sampling requires a caller-supplied exact Walsh oracle.
mersenne_carry_walsh now supplies a capped reference for a separately
reviewed polynomial construction; its practical runtime is not established.
No classical hardness, quantum advantage, or quantum implementation is claimed.
"""
import argparse
from collections import Counter
from fractions import Fraction
import hashlib
import json
from math import isqrt
from pathlib import Path
from random import SystemRandom

from flint import nmod_mat

from theorems.balanced_codeword_filter import ceil_log2_fraction, integer
from theorems.balanced_filter_channel_audit import projection_size
from theorems.balanced_signed_mpi import trace_indices, walsh
from theorems.explicit_quadratic_opi import element, encoded, field
from theorems.inverse_trace_gibbs_target import mds_character_bound
from theorems.mersenne_reciprocal_curve import (
    _binomial_prefix,
    _metadata,
    _parameters,
    native_instance,
    validate_instance,
)


MAX_FINITE_BITS = 17


def differential_uniformity_bound(bits):
    """Canonical-family bound on every D(c), not an observed maximum.

    Four Frobenius iterations of L_c(x)=0 give a nonzero polynomial of
    degree 16 (n-4*s=3) or 32 (n-4*s=5). Remove the roots 0,1 for c!=1;
    handle c=0,1 separately using prime n, giving D(0)=0 and D(1)=2.
    This bound does not apply to arbitrary odd composite degrees or s.
    """
    integer(bits, 17, 127, "canonical field bits")
    s = (bits-3)//4
    if not _metadata(bits, s)["canonical_research_parameters"]:
        raise ValueError("canonical prime field degree required")
    return 14 if bits-4*s == 3 else 30


def clipped_sampler_budget(bits, epsilon=Fraction(1, 8), abort_bits=16):
    """Oracle-relative approximate P(a)=W(a)^2/q^2 sampling certificate.

    The fourth-moment bound sum W^4 <= delta*q^3 bounds lost mass after
    clipping P at T/q by delta/T. Rejection from uniform proposals then
    costs at most T/(1-epsilon) expected oracle queries. The capped law
    includes an explicit ABORT symbol. These are conditional guarantees,
    not a claim that exact Walsh evaluation or iid randomness was verified.
    """
    delta = differential_uniformity_bound(bits)
    if type(epsilon) not in (int, Fraction) or not 0 < epsilon <= Fraction(1, 2):
        raise ValueError("epsilon must be an exact rational in (0, 1/2]")
    if type(abort_bits) is not int or abort_bits < 1:
        raise ValueError("abort confidence bits must be a positive integer")
    epsilon = Fraction(epsilon)
    threshold = (delta*epsilon.denominator+epsilon.numerator-1)//epsilon.numerator
    expected = Fraction(threshold)/(1-epsilon)
    cap = expected*abort_bits
    abort = Fraction(1, 1 << abort_bits)
    return {
        **_metadata(bits, (bits-3)//4),
        "proof_scope": "EXACT_WALSH_ORACLE_RELATIVE_APPROXIMATE_SAMPLER",
        "differential_uniformity_upper": delta,
        "collision_probability_upper": Fraction(delta, 1 << bits),
        "epsilon": epsilon, "clip_threshold": threshold,
        "trial_cap": (cap.numerator+cap.denominator-1)//cap.denominator,
        "expected_oracle_queries_upper": expected,
        "conditional_tv_upper": epsilon,
        "abort_confidence_bits": abort_bits, "abort_probability_upper": abort,
        "unconditional_tv_upper": epsilon+abort,
        "accepted_law": "Q(a)=min(W(a)^2/q^2,T/q)/Z",
        "comparison_law": "P(a)=W(a)^2/q^2, with zero ABORT mass",
        "walsh_oracle_required": True,
        "oracle_correctness_assumed_not_verified": True,
        "independent_uniform_randomness_required": True,
        "polynomial_classical_walsh_access_established": False,
        "access_claim_scope": "this oracle-relative primitive alone; see carry evaluator for a separate construction",
        "exact_target_distribution_claimed": False,
        "coherent_source_implemented": False,
        "native_completion_solver_implemented": False,
        "field_tables_materialized": False,
        "table_accounting_scope": "sampler overhead only; external oracle storage must be charged separately",
        "external_oracle_time_accounted": False,
        "external_oracle_space_accounted": False,
        "polynomial_total_classical_runtime_established": False,
        "classical_hardness_claimed": False, "quantum_advantage_claimed": False,
    }


def sample_clipped_fourier(bits, walsh_oracle, epsilon=Fraction(1, 8),
                           abort_bits=16, rng=None):
    """Run capped rejection with an external exact signed Walsh evaluator.

    walsh_oracle(bits,s,a) must return W(a) in the canonical field-word
    frequency order. Checks below only reject malformed values; they do
    NOT establish oracle correctness. An exact W^2 oracle would suffice
    mathematically, but this interface accepts signed W for existing controls.
    rng must supply independent uniform randrange draws. SystemRandom is
    the default; seeded or scripted generators are finite test controls.
    No full-table fallback is silently substituted for the missing oracle.
    """
    budget = clipped_sampler_budget(bits, epsilon, abort_bits)
    if not callable(walsh_oracle):
        raise ValueError("a caller-supplied exact Walsh oracle is required")
    if rng is None:
        rng = SystemRandom()
    q, threshold, s = 1 << bits, budget["clip_threshold"], budget["s"]
    denominator = threshold*q
    for queries in range(1, budget["trial_cap"]+1):
        a = rng.randrange(q)
        integer(a, 0, q-1, "random frequency")
        value = walsh_oracle(bits, s, a)
        integer(value, -q, q, "signed Walsh oracle output")
        if value % 2 or (a == 0 and value != 0):
            raise ValueError("Walsh output violates parity or balance")
        draw = rng.randrange(denominator)
        integer(draw, 0, denominator-1, "random acceptance draw")
        if draw < min(value*value, denominator):
            return budget | {"status": "ACCEPTED", "frequency": a,
                             "oracle_queries": queries}
    return budget | {"status": "ABORT", "frequency": None,
                     "oracle_queries": budget["trial_cap"]}


def differential_count(bits, s, c):
    """Count F(x+1)+F(x)=c for F(x)=x^(2^(n-s)-1), including zero.

    F is the 2^(n-s)-Frobenius of inv0(x)^(2^s-1), so their traces
    agree, but their vector-valued differential output labels differ. For
    native reciprocal output c, query this function at c^(2^(n-s)).
    Clearing x(x+1) gives L_c(X)=X^(2^(n-s))+c*X^2+(c+1)*X.
    Its kernel always contains 0 and 1; these two excluded roots contribute
    to the differential precisely when c=1. Only n basis images and an n*n
    binary matrix are built, never a field table.
    """
    _parameters(bits, s)
    integer(c, 0, (1 << bits)-1, "differential output")
    coefficient = element(bits, c)
    one = field(bits).one()
    columns = []
    for bit in range(bits):
        x = element(bits, 1 << bit)
        columns.append(encoded(x**(1 << (bits-s))
                               + coefficient*x*x+(coefficient+one)*x))
    matrix = nmod_mat([[column >> row & 1 for column in columns]
                       for row in range(bits)], 2)
    nullity = bits-int(matrix.rank())
    return (1 << nullity)-2+2*int(c == 1)


def gauss_block(bits, s, t, a, b):
    """Exact sum over x,v of chi(t*Q_b(x,v)+a*x), with b a target bit.

    Q_b(x,v)=v^2+x^(2^(s-1))*v+x+b*x^(2^s), chi(z)=(-1)^Tr(z).
    Summing v forces x=t^(-2^(n-s)) for t!=0. The unguarded quadratic
    lift includes (x,v)=(0,0) even at b=1; this is NOT a native fiber count
    or a complete Walsh oracle. A single block needs no field enumeration.
    """
    _parameters(bits, s)
    q = 1 << bits
    integer(t, 0, q-1, "Gauss multiplier")
    integer(a, 0, q-1, "Fourier coefficient")
    integer(b, 0, 1, "target bit")
    if t == 0:
        return q*q*int(a == 0)
    multiplier = element(bits, t)
    phase = element(bits, b)+(multiplier+element(bits, a))*multiplier**(-(1 << (bits-s)))
    return q*(1-2*int(phase.trace()))


def finite_walsh_spectrum(bits, s):
    """Return W(u) in FIELD-word order, capped at n<=17.

    W(u)=sum_x (-1)^(Tr(x^(2^(n-s)-1))+Tr(u*x)). Frobenius invariance
    makes this the native reciprocal-trace Walsh spectrum. The transform's
    bit-dot-product indices are converted with trace_indices, not mistaken
    for field elements. Modulus 2*q+1 recovers every signed sum in [-q,q].
    This is an explicit O(q*n) transform and O(q) table, not polynomial
    access in n. Predicate evaluation additionally costs O(q*n) field work.
    """
    _parameters(bits, s)
    integer(bits, 3, MAX_FINITE_BITS, "finite Walsh control bits")
    q = 1 << bits
    exponent = (1 << (bits-s))-1
    vector = [1-2*int((element(bits, x)**exponent).trace()) for x in range(q)]
    modulus = 2*q+1
    transformed = walsh(vector, modulus=modulus)
    return tuple(transformed[index] if transformed[index] <= q
                 else transformed[index]-modulus for index in trace_indices(bits))


def finite_fourier_report(bits, s):
    """Compact finite certificate; exact Fraction TV, no embedded spectrum.

    The SHA-256 commits to the full FIELD-ordered signed integer spectrum,
    encoded as a compact ASCII JSON array. Fractions remain exact Python
    objects for the caller to serialize; this helper writes no artifact.
    """
    spectrum = finite_walsh_spectrum(bits, s)
    q = 1 << bits
    parseval = sum(value*value for value in spectrum)
    vector = [encoded(element(bits, x)**((1 << (bits-s))-1)) for x in range(q)]
    differential = Counter(vector[x ^ 1] ^ vector[x] for x in range(q))
    histogram = Counter(spectrum)
    differential_moment = sum(value*value for value in differential.values())
    fourth_moment = sum(count*value**4 for value, count in histogram.items())
    canonical = _metadata(bits, s)["canonical_research_parameters"]
    delta = differential_uniformity_bound(bits) if canonical else None
    thresholds = (1, 4, clipped_sampler_budget(bits)["clip_threshold"]) if canonical else (1, 4)
    clipping = []
    for threshold in thresholds:
        mass_numerator = sum(count*min(value*value, threshold*q)
                             for value, count in histogram.items())
        loss = 1-Fraction(mass_numerator, q*q)
        tv = sum((count*abs(Fraction(value*value, q*q)
                           - Fraction(min(value*value, threshold*q), mass_numerator))
                  for value, count in histogram.items()), Fraction(0))/2
        clipping.append({
            "clip_threshold": threshold, "lost_mass": loss, "tv_from_target": tv,
            "acceptance_probability": Fraction(mass_numerator, threshold*q*q),
            "expected_proposals": Fraction(threshold*q*q, mass_numerator),
            "tv_bounded_by_lost_mass": tv <= loss,
        })
    return {
        **_metadata(bits, s),
        "proof_scope": "BOUNDED_EXPONENTIAL_FOURIER_CONTROL",
        "field_basis": "polynomial basis: word=sum_i coefficient_i*2^i",
        "field_modulus_coefficients": list(map(int, field(bits).modulus().coeffs())),
        "frequency_order": "field words u=0,...,q-1; character (-1)^Tr(u*x)",
        "transform_modulus": 2*q+1,
        "walsh_at_zero": spectrum[0], "walsh_at_one": spectrum[1],
        "parseval_sum": parseval, "parseval_checked": parseval == q*q,
        "histogram": dict(sorted(histogram.items())),
        "distinct_values": len(histogram),
        "differential_maximum_observed": max(differential.values()),
        "differential_count_histogram": dict(sorted(Counter(
            differential.get(c, 0) for c in range(q)).items())),
        "differential_second_moment": differential_moment,
        "walsh_fourth_moment": fourth_moment,
        "fourth_moment_identity_checked": fourth_moment == q*q*differential_moment,
        "collision_probability": Fraction(fourth_moment, q**4),
        "canonical_differential_bound": delta,
        "canonical_differential_bound_checked": max(differential.values()) <= delta if canonical else None,
        "finite_clipping_controls": clipping,
        "probability_law": "P(u)=W(u)^2/q^2",
        "tv_from_uniform": Fraction(sum(abs(value*value-q) for value in spectrum), 2*q*q),
        "spectrum_sha256": hashlib.sha256(json.dumps(
            spectrum, separators=(",", ":")
        ).encode("ascii")).hexdigest(),
        "spectrum_hash_encoding": "compact ASCII JSON integer array in field-word order",
        "full_field_entries": q, "exponential_control": True,
        "field_tables_materialized": True,
        "polynomial_classical_walsh_access_established": False,
        "polynomial_classical_source_access_claimed": False,
        "classical_hardness_claimed": False, "quantum_advantage_claimed": False,
        "full_quantum_algorithm_implemented": False,
    }


def partial_completion_budget(instance, fixed_count):
    """Parameter-only certificate for any t accepted fixed coordinates.

    The remaining M=N-t>K coordinates keep their original distinct public
    points and targets; their syndrome is the PUBLIC contribution of the
    fixed values. No coordinates/values are selected or solved here. eta_M<1
    guarantees every such assignment extends. The TV bound compares the
    fixed-coordinate marginal of a uniform native witness with independent
    uniform accepted fixed symbols, assuming the native fiber is nonempty.

    At radius floor(M/2), the ideal per-attempt bound is conditional on a
    paid exact syndrome-offset Fourier source, complete reversible decoding,
    clean fixed-padding projection, and final native verification. It is not
    an unknown-syndrome algorithm. Without strict Johnson agreement, tau,
    padding and the ideal success bound are None, not a positive claim.
    """
    bits, s, points, _, checks = validate_instance(instance)
    length, q = len(points), 1 << bits
    integer(fixed_count, 0, length-checks-1, "fixed coordinate count (remaining > checks)")
    remaining = length-fixed_count
    root = isqrt(q)
    ceil_sqrt_q = root+int(root*root != q)
    beta = min(Fraction(1), Fraction(1+(1 << s)*ceil_sqrt_q, q))
    eta_n = mds_character_bound(bits, length, checks, beta)
    eta_m = mds_character_bound(bits, remaining, checks, beta)
    tv_upper = min(Fraction(1), eta_m/(1-eta_n)) if eta_n < 1 else Fraction(1)
    radius = remaining//2
    johnson_gap = (remaining-radius)**2-remaining*(checks-1)
    tau = padding = success = None
    if johnson_gap > 0:
        tau = Fraction(_binomial_prefix(remaining, radius), 1 << remaining)
        padding = projection_size(remaining, checks, radius, q**checks)
        success = max(Fraction(0), 1-eta_m)*tau**2/padding
    return {
        **_metadata(bits, s),
        "proof_scope": "CONDITIONAL_PARTIAL_COMPLETION_PARAMETER_BOUND",
        "length": length, "fixed_count": fixed_count, "remaining": remaining,
        "checks": checks, "beta": beta, "eta_N": eta_n, "eta_M": eta_m,
        "all_accepted_fixed_assignments_extend": eta_m < 1,
        "native_fiber_nonempty_guaranteed": eta_n < 1,
        "fixed_marginal_tv_upper": tv_upper,
        "tv_requires_nonempty_native_fiber": True,
        "radius": radius, "johnson_gap": johnson_gap,
        "strict_johnson": johnson_gap > 0,
        "tau": tau, "padding": padding,
        "native_success_per_attempt_lower": success,
        "syndrome_scope": "PUBLIC_SYNDROME_FROM_ACCEPTED_FIXED_COORDINATES",
        "requires_paid_syndrome_offset_source": True,
        "requires_paid_known_source_preparation": True,
        "requires_complete_reversible_list_decoder": True,
        "requires_clean_fixed_padding_projection": True,
        "requires_final_native_verification": True,
        "source_premise": "exact signed root-product Fourier source with public syndrome phase and clean uncomputation",
        "unknown_syndrome_algorithm": False, "completion_solver_implemented": False,
        "field_tables_materialized": False, "quantum_premises_verified": False,
        "full_quantum_algorithm_implemented": False,
        "classical_hardness_claimed": False, "quantum_advantage_claimed": False,
    }


def access_report():
    """Compact reproducible report; n17 local table only, no native solver.

    Large exact completion fractions are serialized with outward rounding,
    never converted to floats. The finite Fourier control is exponential
    and is not the backend for the oracle-relative asymptotic sampler.
    """
    rows = []
    for bits in (17, 31, 61):
        instance = native_instance(bits)
        length, checks = len(instance["points"]), instance["checks"]
        budget = partial_completion_budget(instance, length-4*checks)
        success = budget["native_success_per_attempt_lower"]
        numerator = success.numerator*(1 << 128)//success.denominator
        rows.append({
            key: budget[key] for key in (
                "bits", "s", "length", "checks", "fixed_count", "remaining", "radius",
                "johnson_gap", "padding", "proof_scope", "canonical_research_parameters",
                "all_accepted_fixed_assignments_extend", "full_quantum_algorithm_implemented",
                "syndrome_scope", "completion_solver_implemented",
            )
        } | {
            "bound_scope": "uniform over every valid choice of public distinct points, targets, and accepted fixed values",
            "eta_N_power2_upper": ceil_log2_fraction(budget["eta_N"]),
            "eta_M_power2_upper": ceil_log2_fraction(budget["eta_M"]),
            "marginal_tv_power2_upper": ceil_log2_fraction(budget["fixed_marginal_tv_upper"]),
            "conditional_quantum_success_lower": [numerator, 1 << 128],
            "quantum_success_above_one_over_twice_N": success > Fraction(1, 2*length),
            "quantum_premises": [
                "paid exact clean syndrome-offset source", "complete reversible list decoding",
                "clean fixed-padding projection", "final native verification and gate precision",
            ],
            "clipped_sampler": clipped_sampler_budget(bits),
        })
    root = Path(__file__).resolve().parents[1]
    sources = (
        "theorems/mersenne_reciprocal_access.py", "theorems/mersenne_reciprocal_curve.py",
        "theorems/balanced_codeword_filter.py", "theorems/balanced_signed_mpi.py",
        "theorems/balanced_filter_channel_audit.py", "theorems/explicit_quadratic_opi.py",
        "theorems/inverse_trace_gibbs_target.py", "theorems/inverse_trace_smt.py",
        "research/MERSENNE_CLASSICAL_ACCESS_AUDIT.md",
        "theorems/mersenne_carry_walsh.py", "research/MERSENNE_CARRY_WALSH_DRAFT.md",
    )
    return {
        "status": "LOCAL_ACCESS_CONSTRUCTED_NATIVE_COMPLETION_UNRESOLVED",
        "replay": "python -m theorems.mersenne_reciprocal_access",
        "source_sha256": {path: hashlib.sha256((root/path).read_bytes()).hexdigest()
                          for path in sources},
        "native_parameter_bounds": rows,
        "local_exponential_control": finite_fourier_report(17, 3),
        "compiled_quantum_algorithm": False, "native_classical_solver": False,
        "polynomial_classical_walsh_access_established": True,
        "walsh_access_scope": "reviewed written canonical-family algorithm; capped reference, no full-precision native execution",
        "walsh_access_report": "research/classical_baselines/mersenne_carry_walsh.json",
        "walsh_theoretical_bit_time_upper": "O(n^45)",
        "polynomial_approximate_local_sampling_construction": True,
        "practical_classical_runtime_established": False,
        "exact_local_fourier_sampler_established": False,
        "quantum_advantage_established": False, "classical_hardness_established": False,
        "standard_problem_reduction_established": False, "novelty_established": False,
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, help="write the bounded access report")
    args = parser.parse_args(argv)

    def exact_json(value):
        if isinstance(value, Fraction):
            return [value.numerator, value.denominator]
        raise TypeError(f"unsupported report value: {type(value).__name__}")

    payload = json.dumps(access_report(), indent=2, default=exact_json)+"\n"
    if args.output is None:
        print(payload, end="")
    else:
        args.output.write_text(payload, encoding="ascii")


if __name__ == "__main__":
    main()

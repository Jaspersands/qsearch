"""Adversarial representation checks, actual fiber counts and native witnesses."""

from collections import Counter
from fractions import Fraction
import hashlib
import json
import math
from pathlib import Path

import pytest
from sympy import Matrix, Poly, eye, nextprime, symbols

import theorems.prime_character_exterior_bound as module
from theorems.prime_character_exterior_bound import (
    REPORT, complete_quartic_trace_control, exterior_bound, exterior_characters, run_controls,
)
from theorems.prime_character_morse_attack import attack, morse_certificate
from theorems.prime_character_opi import from_specification, instance, ring


def partitions(n, maximum=None):
    if n == 0:
        yield ()
    else:
        for first in range(min(n, maximum or n), 0, -1):
            for tail in partitions(n - first, first):
                yield (first,) + tail


def class_size(parts):
    counts = Counter(parts)
    centralizer = math.prod(length ** count * math.factorial(count) for length, count in counts.items())
    return math.factorial(sum(parts)) // centralizer


@pytest.mark.parametrize("n", range(2, 13))
def test_cycle_indicator_and_zero_invariants_on_every_conjugacy_class(n):
    averages = [0] * n
    cycle_count = 0
    for parts in partitions(n):
        chars = exterior_characters(parts)
        assert len(chars) == n
        assert chars[0] == 1
        assert all(abs(c) <= math.comb(n - 1, j) for j, c in enumerate(chars))
        indicator = sum((-1) ** j * c for j, c in enumerate(chars))
        assert indicator == n * int(len(parts) == 1)
        size = class_size(parts)
        cycle_count += size * int(len(parts) == 1)
        averages = [a + size * c for a, c in zip(averages, chars)]
    assert averages == [math.factorial(n)] + [0] * (n - 1)
    assert cycle_count == math.factorial(n - 1)


def test_characters_match_an_independent_standard_representation_matrix():
    permutation = [1, 2, 0, 4, 3, 5]  # cycle lengths3,2,1
    n, z = len(permutation), symbols("z")
    matrix = Matrix(n - 1, n - 1,
                    lambda r, c: int(permutation[c] == r) - int(permutation[-1] == r))
    polynomial = Poly((eye(n - 1) + z * matrix).det(), z)
    assert [int(polynomial.nth(j)) for j in range(n)] == exterior_characters([3, 2, 1])


def test_geometric_An_would_invalidate_the_zero_invariant_argument():
    n = 6
    even_sum = [0] * n
    for parts in partitions(n):
        if (n - len(parts)) % 2 == 0:
            size = class_size(parts)
            even_sum = [a + size * c for a, c in zip(even_sum, exterior_characters(parts))]
    # Top exterior power is sign and becomes trivial on A_n. Hc2 cannot be dropped.
    assert even_sum[-1] == math.factorial(n) // 2
    assert even_sum[1:-1] == [0] * (n - 2)


@pytest.mark.parametrize("bad", [[], [0], [-1, 2], [True, 2], [2.0]])
def test_invalid_cycle_types_are_not_silently_coerced(bad):
    with pytest.raises(ValueError, match="positive integer"):
        exterior_characters(bad)


def test_bound_sharpens_the_actual_large_degree_without_claiming_61_bit_coverage():
    p = 2 ** 192 - 2 ** 64 - 1
    bound = exterior_bound(p, 76, 58)
    A = 132 * (2 ** 75 - 1)
    assert int(bound["exterior_trace_error_coefficient_decimal"]) == A
    assert int(bound["exterior_rank_sum_decimal"]) == 2 ** 75 - 1
    assert Fraction(bound["twist_probability_lower_exact"]) == 0
    assert Fraction(bound["irreducible_fiber_probability_lower_exact"]) >= Fraction(1, 152)
    assert int(bound["exterior_sufficient_field_threshold_decimal"]).bit_length() == 169
    assert int(bound["twist_sufficient_field_threshold_decimal"]).bit_length() == 756
    assert bound["selected_bound"] == "exterior_trace"
    small = exterior_bound(2 ** 61 - 1, 76, 58)
    assert Fraction(small["irreducible_fiber_probability_lower_exact"]) == 0
    assert not small["field_meets_sufficient_threshold"]
    assert not bound["exponential_rank_objects_constructed"]
    assert not bound["this_bound_alone_verifies_the_Morse_hypotheses"]


@pytest.mark.parametrize("n,b", [(4, 1), (6, 1), (6, 3), (10, 4), (10, 5), (76, 58)])
def test_exact_rounding_and_sufficient_threshold_are_conservative(n, b):
    provisional = exterior_bound(2 ** 192 - 2 ** 64 - 1, n, b)
    threshold = int(provisional["exterior_sufficient_field_threshold_decimal"])
    p = int(nextprime(threshold))
    bound = exterior_bound(p, n, b)
    root = math.isqrt(p)
    A, R = int(bound["exterior_trace_error_coefficient_decimal"]), n + b
    assert int(bound["sqrt_p_upper_integer"]) == root + 1
    probability = Fraction(p + 1 - R - A * (root + 1), n * p)
    assert Fraction(bound["exterior_probability_lower_exact"]) == probability >= Fraction(1, 2 * n)
    assert bound["field_meets_sufficient_threshold"]


def test_twist_is_retained_when_its_bound_is_stronger():
    bound = exterior_bound(10007, 4, 1)
    assert bound["selected_bound"] == "Galois_twist"
    assert Fraction(bound["exterior_probability_lower_exact"]) < Fraction(bound["twist_probability_lower_exact"])
    assert int(bound["sufficient_p_for_probability_at_least_1_over_2n_decimal"]) == 5184


def test_positive_numeric_bound_never_certifies_a_non_morse_map():
    p, C = 2 ** 61 - 1, ring(2 ** 61 - 1)
    assert Fraction(exterior_bound(p, 4, 1)["irreducible_fiber_probability_lower_exact"]) > 0
    cert = morse_certificate(p, C([-1, 1]) ** 4, C([0, 1]), bound_method="exterior")
    assert not cert["Morse_conditions_verified"]
    assert cert["status"] == "NON_MORSE_REPEATED_CRITICAL_POINT"
    with pytest.raises(ValueError, match="bound_method"):
        morse_certificate(p, C([1, 0, 0, 0, 1]), C([0, 1]), bound_method="unproved")
    with pytest.raises(ValueError, match="bound_method"):
        attack(instance(p, 15, 12, 2, 29), bound_method="unproved")


@pytest.mark.parametrize("p", [29, 101, 1009, 10007])
def test_actual_fiber_factorizations_satisfy_the_trace_identity_and_bounds(p):
    record = complete_quartic_trace_control(p)
    assert record["field_parameters_enumerated_and_charged"] == p
    assert record["unramified_fibers"] == record["exterior_character_sums"][0]
    signed = sum((-1) ** j * total for j, total in enumerate(record["exterior_character_sums"]))
    assert signed == 4 * record["irreducible_fibers"]
    if p == 10007:
        assert record["irreducible_fibers"] == 2528
    assert record["this_enumeration_is_not_the_large_field_algorithm"]


def test_original_field_guard_does_not_call_norm_sampler(monkeypatch):
    import theorems.prime_character_morse_attack as morse
    def forbidden(*args, **kwargs):
        raise AssertionError("zero-bound input cannot enter the norm stage")
    monkeypatch.setattr(morse, "polynomial_norm", forbidden)
    record = attack(instance(2 ** 61 - 1, 127, 77, 2, 29), 3040, bound_method="exterior")
    assert record["status"] == "MORSE_CERTIFIED_FIELD_TOO_SMALL_FOR_THIS_EXPLICIT_BOUND"
    assert record["small_field_failure_is_not_hardness"]


def test_192_bit_fixed_input_witness_replays_without_search_or_factorization(monkeypatch):
    report = json.loads(REPORT.read_text())
    lift = report["large_fixed_input_control"]
    record = lift["fixed_input_attack"]
    original = from_specification(lift["original_specification"])
    problem = from_specification(record["preparation"]["specification"])
    def forbidden(*args, **kwargs):
        raise AssertionError("saved witness replay cannot rerun the search")
    monkeypatch.setattr(module, "attack", forbidden)
    assert problem.prime == 2 ** 192 - 2 ** 64 - 1
    assert problem.shifts == original.shifts and problem.orientations == original.orientations
    assert not problem.include_zero and not lift["is_original_61_bit_input"]
    assert problem.score_count(tuple(record["polynomial_coefficients"])) == 127
    assert len(record["polynomial_coefficients"]) <= 77
    assert not lift["source_is_IID_assumed"]
    cert = record["geometry_attempts"][-1]["certificate"]
    C, p = ring(problem.prime), problem.prime
    f, g = C(cert["f_coefficients"]), C(cert["g_coefficients"])
    W, B = f.derivative() * g - f * g.derivative(), C(cert["critical_value_polynomial_coefficients"])
    assert W.degree() == B.degree() == 133
    assert W.gcd(W.derivative()).degree() == 0 and B.gcd(B.derivative()).degree() == 0
    assert f.gcd(g).degree() == 0 and g.gcd(g.derivative()).degree() == 0
    samples = cert["critical_resultant_samples"]
    anchor = next(i for i, value in enumerate(samples) if value)
    multiplier = samples[anchor] * pow(int(B(anchor)), -1, p) % p
    for y, sample in enumerate(samples):
        assert int(W.resultant(f - y * g)) == sample == int(B(y)) * multiplier % p
    bound = cert["arithmetic_bound"]
    assert Fraction(bound["twist_probability_lower_exact"]) == 0
    assert Fraction(bound["irreducible_fiber_probability_lower_exact"]) >= Fraction(1, 152)
    assert lift["fiber_trial_budget"] == 2 * 76 * (lift["uniform_fiber_failure_budget_bits"] + 1)
    fiber = record["fiber_attempts"][-1]
    F = f - int(fiber["fiber_parameter_decimal"]) * g
    norm = fiber["norm_certificate"]
    nu = int(record["preparation"]["nu_decimal"])
    R, Z = C(norm["R_coefficients"]), C(norm["Z_coefficients"])
    assert R ** 2 - nu * Z ** 2 == F
    rotated = fiber["strict_rotation"]
    R, Z = C(rotated["R_coefficients"]), C(rotated["Z_coefficients"])
    assert R ** 2 - nu * Z ** 2 == F
    Q = C(record["preparation"]["Q0_coefficients"]) + int(record["preparation"]["beta_decimal"]) * R ** 2
    assert list(map(int, Q.coeffs())) == record["polynomial_coefficients"]
    assert record["local_proof_review_pending"] and not record["accepted_speedup_candidate"]


def test_live_artifact_replay_and_provenance():
    report = run_controls()
    assert report == json.loads(REPORT.read_text())
    source = Path(module.__file__)
    assert hashlib.sha256(source.read_bytes()).hexdigest() == report["source_sha256"]
    for name, digest in report["dependency_sha256"].items():
        assert hashlib.sha256(source.with_name(name).read_bytes()).hexdigest() == digest
    assert report["local_application_review_pending"]
    assert not report["all_field_or_low_rate_dequantization_claimed"]
    assert not report["new_central_candidate_negative_or_proof_registered"]
    assert not report["independent_or_formal_proof_review_completed"]

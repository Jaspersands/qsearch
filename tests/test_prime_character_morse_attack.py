"""Exact ramification geometry, field guards and native fixed-input witnesses."""

from fractions import Fraction
import hashlib
import json
import math
from pathlib import Path

import pytest
from sympy import Poly, resultant, symbols

import theorems.prime_character_morse_attack as module
from theorems.prime_character_morse_attack import (
    REPORT, attack, coeffs, geometry_bound, morse_certificate, prepare,
    quartic_control, run_controls,
)
from theorems.prime_character_opi import from_specification, instance, ring


def test_quartic_geometry_matches_closed_forms_and_a_complete_fiber_count():
    record = quartic_control()
    cert = record["certificate"]
    p, C = 10007, ring(10007)
    assert cert["Morse_conditions_verified"]
    assert C(cert["critical_numerator_coefficients"]) == C([-1, 0, 0, 0, 3])
    expected = C([-256 * pow(27, -1, p), 0, 0, 0, 1])
    assert C(cert["critical_value_polynomial_coefficients"]) == expected
    bound = cert["arithmetic_bound"]
    assert int(bound["Galois_group_order_decimal"]) == 24
    assert int(bound["Galois_closure_genus_decimal"]) == 9
    assert bound["finite_simple_branch_count"] == 4 and bound["infinity_pole_order"] == 3
    assert int(bound["sufficient_p_for_probability_at_least_1_over_2n_decimal"]) == 5184
    assert record["actual_irreducible_fibers"] == 2528
    assert Fraction(record["actual_irreducible_fibers"], p) >= Fraction(bound["irreducible_fiber_probability_lower_exact"]) >= Fraction(1, 8)
    assert record["all_fibers_enumerated_and_charged"] == p


def test_critical_value_resultant_is_independently_reconstructed_over_the_integers():
    x, y = symbols("x y")
    p, C = 10007, ring(10007)
    f, g = C([1, 0, 0, 0, 1]), C([0, 1])
    cert = morse_certificate(p, f, g)
    expression = resultant(3 * x ** 4 - 1, x ** 4 + 1 - y * x, x)
    poly = Poly(expression, y)
    values = [int(a) % p for a in reversed(poly.all_coeffs())]
    independent = C(values) * pow(values[-1], -1, p)
    assert independent == C(cert["critical_value_polynomial_coefficients"])


def test_simple_critical_points_do_not_suffice_when_critical_values_collide():
    C = ring(10007)
    f, g = C([1, 0, 0, 0, 0, 0, 1]), C([-1, 0, 1])
    W = f.derivative() * g - f * g.derivative()
    assert W.gcd(W.derivative()).degree() == 0
    record = morse_certificate(10007, f, g)
    assert record["status"] == "NON_MORSE_COLLIDING_CRITICAL_VALUES"
    assert not record["Morse_conditions_verified"]


def test_repeated_critical_points_and_invalid_poles_are_not_certified():
    C = ring(10007)
    bad = morse_certificate(10007, C([-1, 1]) ** 4, C([0, 1]))
    assert bad["status"] == "NON_MORSE_REPEATED_CRITICAL_POINT"
    with pytest.raises(ValueError, match="coprime"):
        morse_certificate(10007, C([0, 0, 0, 0, 1]), C([0, 1]))
    with pytest.raises(ValueError, match="squarefree"):
        morse_certificate(10007, C([1, 0, 0, 0, 0, 0, 1]), C([0, 0, 1]))
    with pytest.raises(ValueError, match="monic"):
        morse_certificate(10007, C([1, 0, 0, 0, 2]), C([0, 1]))
    with pytest.raises(ValueError, match="prime"):
        geometry_bound(10000, 4, 1)
    with pytest.raises(ValueError, match="slack"):
        geometry_bound(10007, 4, 2)


def test_preparation_uses_real_degree_slack_and_a_unit_residue_for_either_coset():
    for seed in (29, 71):
        problem = instance(2 ** 61 - 1, 15, 12, 2, seed, mode="mixed", include_zero=False)
        preparation, data = prepare(problem)
        assert data is not None and preparation["status"] == "EXACT_UNIT_ARITHMETIC_PROGRESSION_PREPARED"
        base, g, Q0, beta, nu = data
        assert preparation["first_orientation"] == {29: 1, 71: 0}[seed]
        assert g.degree() in (4, 5) and base.degree() == 10
        assert base.gcd(g).degree() == 0 and g.gcd(g.derivative()).degree() == 0
        for i in preparation["A_positions"]:
            assert int(Q0(i + 1)) == problem.shifts[i]
        for i in preparation["B_positions"]:
            assert int(base(i + 1)) == (problem.shifts[i] - int(Q0(i + 1))) * pow(beta, -1, problem.prime) % problem.prime
        assert pow(nu, (problem.prime - 1) // 2, problem.prime) == problem.prime - 1
    low = instance(2 ** 61 - 1, 127, 39, 2, 29)
    record, data = prepare(low)
    assert data is None and record["status"].startswith("NOT_APPLICABLE")
    assert not record["original_problem_unsatisfiability_claimed"]


def test_exact_certificates_and_witnesses_replay_without_new_search(monkeypatch):
    report = json.loads(REPORT.read_text())
    def forbidden(*args, **kwargs):
        raise AssertionError("native witness replay must not rerun search")
    monkeypatch.setattr(module, "attack", forbidden)
    for record in report["native_controls"]:
        preparation = record["preparation"]
        problem = from_specification(preparation["specification"])
        assert record["status"] == "CLASSICAL_PERFECT_WITNESS_WITH_FIXED_INPUT_GEOMETRIC_BOUND"
        assert problem.score_count(tuple(record["polynomial_coefficients"])) == 15
        assert len(record["polynomial_coefficients"]) <= problem.dimension
        cert = record["geometry_attempts"][-1]["certificate"]
        C, p = ring(problem.prime), problem.prime
        f, g = C(cert["f_coefficients"]), C(cert["g_coefficients"])
        W = f.derivative() * g - f * g.derivative()
        assert coeffs(W) == cert["critical_numerator_coefficients"]
        assert W.gcd(W.derivative()).degree() == 0
        B = C(cert["critical_value_polynomial_coefficients"])
        assert B.degree() == W.degree() and B.gcd(B.derivative()).degree() == 0
        # Normalize fresh resultant values by one known nonzero specialization.
        samples = cert["critical_resultant_samples"]
        anchor = next(i for i, value in enumerate(samples) if value)
        multiplier = samples[anchor] * pow(int(B(anchor)), -1, p) % p
        for y in range(W.degree() + 1):
            assert int(W.resultant(f - y * g)) == samples[y] == multiplier * int(B(y)) % p
        n, b = f.degree(), g.degree()
        h = math.factorial(n)
        ramification = -2 + Fraction(n + b - 1, 2) + 1 - Fraction(1, n - b)
        genus = 1 + h * ramification / 2
        bound = cert["arithmetic_bound"]
        assert genus.denominator == 1 and str(genus.numerator) == bound["Galois_closure_genus_decimal"]
        upper_sqrt = math.isqrt(p) + int(math.isqrt(p) ** 2 != p)
        numerator = p + 1 - 2 * genus * upper_sqrt - (n + b) * h
        assert Fraction(bound["irreducible_fiber_probability_lower_exact"]) == numerator / (n * p)
        assert Fraction(bound["irreducible_fiber_probability_lower_exact"]) >= Fraction(1, 2 * n)
        fiber = record["fiber_attempts"][-1]
        F = f - int(fiber["fiber_parameter_decimal"]) * g
        assert coeffs(F) == fiber["target_F_coefficients"]
        assert F.is_irreducible()
        norm = fiber["norm_certificate"]
        R, Z = C(norm["R_coefficients"]), C(norm["Z_coefficients"])
        nu = int(preparation["nu_decimal"])
        assert R ** 2 - nu * Z ** 2 == F
        if fiber["strict_rotation"]:
            rotation = fiber["strict_rotation"]
            R, Z = C(rotation["R_coefficients"]), C(rotation["Z_coefficients"])
            assert R ** 2 - nu * Z ** 2 == F
        Q = C(preparation["Q0_coefficients"]) + int(preparation["beta_decimal"]) * R ** 2
        assert coeffs(Q) == record["polynomial_coefficients"]


def test_larger_field_guard_cannot_promote_morse_geometry_to_a_probability_claim(monkeypatch):
    def forbidden(*args, **kwargs):
        raise AssertionError("no fibers may be sampled under a zero probability certificate")
    monkeypatch.setattr(module, "polynomial_norm", forbidden)
    problem = instance(2 ** 61 - 1, 127, 77, 2, 29)
    record = attack(problem, 3040)
    assert record["status"] == "MORSE_CERTIFIED_FIELD_TOO_SMALL_FOR_THIS_EXPLICIT_BOUND"
    assert record["small_field_failure_is_not_hardness"]
    cert = record["geometry_attempts"][-1]["certificate"]
    assert cert["Morse_conditions_verified"] and not cert["fixed_input_probability_bound_available"]
    bound = cert["arithmetic_bound"]
    assert Fraction(bound["irreducible_fiber_probability_lower_exact"]) == 0
    assert not bound["field_meets_sufficient_threshold"]
    assert bound["no_Galois_group_or_factorial_degree_extension_enumerated"]
    threshold = int(bound["sufficient_p_for_probability_at_least_1_over_2n_decimal"])
    assert threshold.bit_length() < 4 * 76 * (76).bit_length()


def test_large_field_fixed_input_witness_is_a_declared_lift_with_a_real_bound():
    report = json.loads(REPORT.read_text())
    lift = report["large_field_fixed_input_control"]
    original = from_specification(lift["original_specification"])
    record = lift["lifted_fixed_input_attack"]
    prepared = record["preparation"]
    problem = from_specification(prepared["specification"])
    assert problem.prime == 2 ** 1279 - 1 and problem.prime.bit_length() == 1279
    assert problem.shifts == original.shifts and problem.orientations == original.orientations
    assert not problem.include_zero and not lift["is_the_original_61_bit_problem"]
    assert problem.score_count(tuple(record["polynomial_coefficients"])) == 127
    assert record["status"] == "CLASSICAL_PERFECT_WITNESS_WITH_FIXED_INPUT_GEOMETRIC_BOUND"
    cert = record["geometry_attempts"][-1]["certificate"]
    bound = cert["arithmetic_bound"]
    n, b = bound["cover_degree"], bound["modulus_degree"]
    assert n == 76 and b == 58
    assert bound["field_meets_sufficient_threshold"]
    assert Fraction(bound["irreducible_fiber_probability_lower_exact"]) >= Fraction(1, 2 * n)
    assert Fraction(bound["generic_Morse_pair_probability_lower_under_local_discriminant_proof"]) >= Fraction(1, 2)
    assert lift["fiber_trial_budget"] == 2 * n * (lift["uniform_fiber_failure_budget_bits"] + 1)
    assert len(record["fiber_attempts"]) == 69
    C = ring(problem.prime)
    f, g = C(cert["f_coefficients"]), C(cert["g_coefficients"])
    W = f.derivative() * g - f * g.derivative()
    B = C(cert["critical_value_polynomial_coefficients"])
    assert W.degree() == 133 and W.gcd(W.derivative()).degree() == 0
    assert B.degree() == 133 and B.gcd(B.derivative()).degree() == 0
    samples = cert["critical_resultant_samples"]
    anchor = next(i for i, value in enumerate(samples) if value)
    multiplier = samples[anchor] * pow(int(B(anchor)), -1, problem.prime) % problem.prime
    for y in range(W.degree() + 1):
        assert int(W.resultant(f - y * g)) == samples[y] == multiplier * int(B(y)) % problem.prime
    fiber = record["fiber_attempts"][-1]
    F = f - int(fiber["fiber_parameter_decimal"]) * g
    norm = fiber["norm_certificate"]
    R, Z = C(norm["R_coefficients"]), C(norm["Z_coefficients"])
    nu = int(prepared["nu_decimal"])
    assert R ** 2 - nu * Z ** 2 == F
    rotated = fiber["strict_rotation"]
    R, Z = C(rotated["R_coefficients"]), C(rotated["Z_coefficients"])
    assert R ** 2 - nu * Z ** 2 == F
    Q = C(prepared["Q0_coefficients"]) + int(prepared["beta_decimal"]) * R ** 2
    assert coeffs(Q) == record["polynomial_coefficients"]
    assert lift["seeded_run_is_not_an_IID_confidence_certificate"]


def test_live_morse_artifact_replays_without_fixed_degree_or_speedup_promotion():
    report = run_controls()
    assert report == json.loads(REPORT.read_text())
    source = Path(module.__file__)
    assert report["source_sha256"] == hashlib.sha256(source.read_bytes()).hexdigest()
    for name, digest in report["dependency_sha256"].items():
        assert hashlib.sha256(source.with_name(name).read_bytes()).hexdigest() == digest
    assert not report["fixed_degree_asymptotic_used_as_a_uniform_bound"]
    assert not report["all_input_or_all_field_dequantization_claimed"]
    assert not report["new_central_candidate_negative_or_proof_registered"]
    assert not report["independent_or_formal_proof_review_completed"]

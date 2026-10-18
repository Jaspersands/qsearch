"""Exact norm identities, native OPI witnesses and an all-pencil counterexample."""

import hashlib
import itertools
import json
from pathlib import Path

import pytest

import theorems.prime_character_norm_attack as module
from theorems.prime_character_norm_attack import (
    REPORT, adversarial_pencil_control, attack, extension, polynomial_norm,
    one_trial_IID_source_bound, run_controls, strict_norm_rotation,
)
from theorems.prime_character_opi import (
    REPORT as OLD_REPORT, PrimeCharacterOPI, from_specification, instance, interpolate, ring,
)


def convolve(a, b, p):
    values = [0] * max(0, len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            values[i + j] = (values[i + j] + x * y) % p
    return values


def norm_coefficients(a, b, p, nu):
    a2, b2 = convolve(a, a, p), convolve(b, b, p)
    result = [(a2[j] if j < len(a2) else 0) - nu * (b2[j] if j < len(b2) else 0)
              for j in range(max(len(a2), len(b2)))]
    result = [x % p for x in result]
    while result and result[-1] == 0:
        result.pop()
    return tuple(result)


def test_norm_factor_criterion_matches_exhaustive_small_polynomial_representations():
    p, nu, C = 3, 2, ring(3)
    roots = list(itertools.product(range(p), repeat=3))
    possible = {norm_coefficients(a, b, p, nu) for a in roots for b in roots}
    for degree in range(5):
        for lower in itertools.product(range(p), repeat=degree):
            f = (*lower, 1)
            result = polynomial_norm(p, nu, C(list(f)))
            success = result["status"] == "EXACT_POLYNOMIAL_NORM_REPRESENTATION"
            assert success == (f in possible)
            if success:
                assert norm_coefficients(result["R_coefficients"], result["Z_coefficients"], p, nu) == f
            else:
                assert result["odd_degree_odd_multiplicity_factors"]


def test_repeated_inert_factors_are_legal_but_odd_multiplicity_is_not():
    C = ring(11)
    assert polynomial_norm(11, 2, C([0, 0, 1]))["status"] == "EXACT_POLYNOMIAL_NORM_REPRESENTATION"
    assert polynomial_norm(11, 2, C([0, 1]))["status"] == "THIS_POLYNOMIAL_IS_NOT_A_CONSTANT_EXTENSION_NORM"
    for bad in (C([]), C([2, 0, 2])):
        with pytest.raises(ValueError, match="monic"):
            polynomial_norm(11, 2, bad)
    with pytest.raises(ValueError, match="nonresidue"):
        extension(11, 1)
    scaled = polynomial_norm(11, 2, 9 * C([0, 0, 1]), leading_root=3)
    assert norm_coefficients(scaled["R_coefficients"], scaled["Z_coefficients"], 11, 2) == (0, 0, 9)


def test_strict_cayley_rotation_preserves_norm_and_removes_an_actual_zero():
    p, nu, C = 101, 2, ring(101)
    problem = PrimeCharacterOPI(p, 4, 2, nu, (0,) * 4, (0, 0, 1, 1), include_zero=False)
    R, Z = C([-1, 1]), C([1])
    F = R ** 2 - nu * Z ** 2
    assert int(R(1)) == 0 and all(int(F(x)) for x in range(1, 5))
    a, b, record = strict_norm_rotation(problem, R, Z, F, nu)
    assert record["parameter"] == 1 and record["parameters_tested"] == 2
    assert norm_coefficients(list(map(int, a.coeffs())), list(map(int, b.coeffs())), p, nu) == tuple(map(int, F.coeffs()))
    assert all(int((a if problem.orientations[i] == 0 else b)(i + 1)) for i in range(4))
    assert a.degree() <= 1 and b.degree() <= 1
    # Norm zero at a rational native point forces both components to zero.
    zero_F = R ** 2
    a, b, failed = strict_norm_rotation(problem, R, C([]), zero_F, nu)
    assert a is None and b is None
    assert failed["status"] == "THIS_NORM_TARGET_FORCES_ZERO_ROOTS"
    assert not failed["original_problem_unsatisfiability_claimed"]


def test_degree_nonapplicability_and_budget_failure_are_not_hardness():
    low = instance(2 ** 61 - 1, 127, 39, 2, 29, mode="mixed")
    result = attack(low)
    assert result["status"] == "NOT_APPLICABLE_DEGREE_BUDGET" and result["trials"] == []
    assert not result["original_problem_unsatisfiability_claimed"]
    high = instance(2 ** 61 - 1, 127, 77, 2, 29, mode="mixed")
    limited = attack(high, 1038, trials=1, variable_leading=False)
    assert limited["status"] == "NO_PERFECT_WITNESS_WITHIN_PAID_PENCIL_BUDGET_UNKNOWN"
    assert len(limited["trials"]) == 1 and limited["no_witness_is_not_hardness_or_unsatisfiability"]
    assert not limited["source_rerolled_or_rejected"]


def test_a_common_coset_or_higher_power_is_not_silently_reinterpreted_as_mixed_quadratic():
    global_input = instance(131, 15, 13, 2, 29, mode="global")
    assert attack(global_input)["status"] == "NOT_APPLICABLE_REQUIRES_TWO_QUADRATIC_COSETS"
    higher = instance(127, 15, 13, 3, 29, mode="mixed")
    assert attack(higher)["status"] == "NOT_APPLICABLE_REQUIRES_TWO_QUADRATIC_COSETS"


def test_all_parameter_counterexample_is_norm_search_failure_on_a_strictly_easy_input():
    record = adversarial_pencil_control()
    problem = from_specification(record["specification"])
    assert not problem.include_zero and problem.score_count((13,)) == 8
    p, C = problem.prime, ring(problem.prime)
    D = C(record["D_coefficients"])
    assert D.degree() == 3 and [x for x in range(p) if int(D(x)) == 0] == [0, 9, 16]
    assert all(int(D.derivative()(x)) != 0 for x in (0, 9, 16))
    F_base = C(record["F_base_coefficients"])
    assert F_base == D * C.gen() * pow(16, -1, p)
    _, V_A = interpolate(p, (1, 2, 3, 4), (0,) * 4)
    for lam in range(p):
        target, V_B = interpolate(p, (5, 6, 7, 8), tuple((problem.shifts[i] - lam * int(V_A(i + 1))) % p for i in range(4, 8)))
        F = target + V_B
        assert F == F_base - lam * D
        # At most one of the three fixed distinct linear roots can gain
        # another multiplicity from a single linear moving factor.
        odd_roots = 0
        for root in (0, 9, 16):
            poly, count = F, 0
            while not int(poly(root)):
                poly, remainder = divmod(poly, C([-root, 1]))
                assert remainder.is_zero()
                count += 1
            odd_roots += count % 2
        assert odd_roots >= 2
    assert record["entire_monic_pencil_norm_obstructed"]
    assert not record["OPI_itself_is_unsatisfiable_or_hard"]
    repair = record["expanded_square_leading_repair"]
    assert repair["variable_square_leading_pencil"]
    assert problem.score_count(tuple(repair["polynomial_coefficients"])) == 8
    # The expanded pencil no longer shares any of the three inert roots.
    _, V_B = interpolate(p, (5, 6, 7, 8), (0,) * 4)
    assert (D.gcd(V_B)).degree() == 0


def test_large_native_perfect_witnesses_replay_without_any_factorization(monkeypatch):
    report = json.loads(REPORT.read_text())
    def forbidden(*args, **kwargs):
        raise AssertionError("certificate replay needs no new factorization or search")
    monkeypatch.setattr(module, "polynomial_norm", forbidden)
    accepted = [r for r in report["results"] if r["status"] == "CLASSICAL_NATIVE_PERFECT_WITNESS"]
    assert len(accepted) == 4
    for record in accepted:
        problem = from_specification(record["specification"])
        p, nu, C = problem.prime, int(record["nu_decimal"]), ring(problem.prime)
        q = tuple(record["polynomial_coefficients"])
        assert len(q) <= problem.dimension and problem.score_count(q) == 127
        assert [problem.accepted(i, y) for i, y in enumerate(problem.evaluations(q))] == [True] * 127
        for trial in record["trials"]:
            F = tuple(trial["target_F_coefficients"])
            factors = trial["norm_attempt"]["factors"]
            product = (int(trial["norm_attempt"]["factorization_unit_decimal"]),)
            for f in factors:
                assert C(f["coefficients"]).is_irreducible()
                for _ in range(f["multiplicity"]):
                    product = tuple(convolve(product, f["coefficients"], p))
            assert product == F
            if trial["norm_attempt"]["status"] == "EXACT_POLYNOMIAL_NORM_REPRESENTATION":
                norm = trial["norm_attempt"]
                assert norm_coefficients(norm["R_coefficients"], norm["Z_coefficients"], p, nu) == F
                if "strict_rotation" in trial:
                    rotated = trial["strict_rotation"]
                    assert rotated["status"] == "STRICT_NONZERO_NORM_ROTATION"
                    assert norm_coefficients(rotated["R_coefficients"], rotated["Z_coefficients"], p, nu) == F
        assert not record["uniform_polynomial_success_for_this_pencil_proved"]


def test_existing_zero_including_sources_are_unchanged_not_favorable_replacements():
    old = json.loads(OLD_REPORT.read_text())
    # Locate specifications without depending on the old attack's output schema.
    def specifications(value):
        if isinstance(value, dict):
            if "prime_decimal" in value and "shifts_decimal" in value:
                yield value
            for child in value.values():
                yield from specifications(child)
        elif isinstance(value, list):
            for child in value:
                yield from specifications(child)
    originals = list(specifications(old["instances"]))
    for K, seed in itertools.product((39, 77), (29, 71)):
        current = instance(2 ** 61 - 1, 127, K, 2, seed, mode="mixed").specification()
        assert current in originals


def test_average_case_bound_has_an_exact_exhaustive_source_calibration():
    from fractions import Fraction
    p, C, nu = 11, ring(11), 2
    irreducibles = 0
    for t3, t4 in itertools.product(range(p), repeat=2):
        problem = PrimeCharacterOPI(p, 3, 2, nu, (0, 0, t3, t4), (0, 0, 1, 1), include_zero=False)
        F0, V_B = interpolate(p, (3, 4), (t3, t4))
        F = F0 + V_B
        if not F.is_irreducible():
            continue
        irreducibles += 1
        norm = polynomial_norm(p, nu, F)
        R, Z = C(norm["R_coefficients"]), C(norm["Z_coefficients"])
        R, Z, rotation = strict_norm_rotation(problem, R, Z, F, nu)
        assert rotation["status"] == "STRICT_NONZERO_NORM_ROTATION"
        Q = R ** 2
        assert Q.degree() < 3 and problem.score_count(tuple(map(int, Q.coeffs()))) == 4
    bound = one_trial_IID_source_bound(problem)
    assert irreducibles == 55
    assert Fraction(bound["success_probability_lower_exact"]) == Fraction(55, 121)
    assert bound["strict_zero_avoidance_covered"]
    assert not bound["fixed_instance_probability_bound"]
    assert not bound["pencil_trials_are_assumed_independent"]


def test_large_IID_population_bound_is_non_negligible_without_fixed_input_amplification():
    from fractions import Fraction
    for seed in (29, 71):
        problem = instance(2 ** 61 - 1, 127, 77, 2, seed, mode="mixed", include_zero=False)
        bound = one_trial_IID_source_bound(problem)
        probability = Fraction(bound["success_probability_lower_exact"])
        assert probability >= Fraction(1, 2 * problem.length)
        assert probability <= Fraction(1, bound["norm_target_degree"])
        assert not bound["high_probability_or_worst_case_solver_claimed"]
        assert not bound["seeded_replays_are_an_IID_certificate"]
    low = instance(2 ** 61 - 1, 127, 39, 2, 29)
    assert one_trial_IID_source_bound(low)["status"].startswith("NOT_APPLICABLE")


def test_large_prime_support_does_not_hit_the_python_decimal_digit_limit():
    from flint import fmpq, fmpz
    original = instance(2 ** 61 - 1, 127, 77, 2, 29, mode="mixed", include_zero=False)
    p = 2 ** 1279 - 1
    problem = PrimeCharacterOPI(p, 77, 2, 3, original.shifts, original.orientations, include_zero=False)
    bound = one_trial_IID_source_bound(problem)
    assert len(bound["polynomial_population_size_decimal"]) > 4300
    assert fmpz(bound["polynomial_population_size_decimal"]) == fmpz(p) ** bound["norm_target_degree"]
    assert fmpq(bound["success_probability_lower_exact"]) >= fmpq(1, 254)


def test_live_norm_attack_artifact_replays_without_asymptotic_promotion():
    report = run_controls()
    assert report == json.loads(REPORT.read_text())
    source = Path(module.__file__)
    assert report["source_sha256"] == hashlib.sha256(source.read_bytes()).hexdigest()
    assert report["dependency_sha256"] == hashlib.sha256(source.with_name("prime_character_opi.py").read_bytes()).hexdigest()
    assert not report["all_input_or_asymptotic_dequantization_proved"]
    assert not report["accepted_speedup_candidate"] and not report["new_central_negative_registered"]

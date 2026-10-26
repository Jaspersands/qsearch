"""Independent Fourier counts and ORIGINAL-target checks for native masking."""

from collections import Counter
from fractions import Fraction
from itertools import product
import json

import pytest

from theorems import moment_target_masking as module


@pytest.mark.parametrize("p,points,rank", [(7, (1, 2), 1), (7, (2, 4, 6), 2), (11, (3, 4, 8), 1)])
def test_mds_fourier_identity_matches_exact_native_collision_distribution(p, points, rank):
    counts = Counter(tuple(module.native_moments(p, list(x), rank, points=points))
                     for x in product(range(p), repeat=len(points)))
    total, targets = p ** len(points), p ** rank
    # chi-square(P||uniform) = p^r*sum_b P(b)^2-1.
    energy = targets * sum(Fraction(n, total) ** 2 for n in counts.values()) - 1
    assert energy == module.mask_fourier_energy(p, len(points), rank)
    tv = sum(abs(Fraction(counts.get(b, 0), total) - Fraction(1, targets))
             for b in product(range(p), repeat=rank)) / 2
    assert tv * tv <= energy / 4


def test_large_field_certificate_has_a_positive_floor_for_every_fixed_target():
    row = module.masking_certificate((1 << 61) - 1, 127, 31, 32)
    floor = Fraction(row["EVERY_fixed_target_one_attempt_success_lower_exact"])
    assert row["norm_degree_gate"]
    assert row["remaining_coordinates"] == 95
    assert row["remaining_OPI_dimension"] == 64
    assert row["remaining_orientation_counts"] == [48, 47]
    assert Fraction(1, 49) < floor < Fraction(1, 48)
    assert floor == (Fraction(row["IID_norm_population_success_lower_exact"])
                     - Fraction(row["mask_total_variation_upper_exact"])
                     - Fraction(row["zero_prefix_rejection_probability_upper_exact"]))
    budget = row["independent_uniform_coin_trial_budget"]
    assert floor * budget >= 10
    assert (1 - floor) ** budget < Fraction(1, 1 << 10)
    assert not row["independent_review_or_formal_verification_completed"]


def test_total_variation_square_root_rounds_outward_exactly():
    p, reserve, rank = (1 << 61) - 1, 32, 31
    row = module.masking_certificate(p, 127, rank, reserve)
    energy = module.mask_fourier_energy(p, reserve, rank)
    tv = Fraction(row["mask_total_variation_upper_exact"])
    assert tv * tv >= energy / 4
    assert (tv - Fraction(1, 1 << 96)) ** 2 < energy / 4


def test_population_floor_matches_the_existing_norm_source_theorem():
    from theorems.prime_character_norm_attack import one_trial_IID_source_bound
    p = (1 << 61) - 1
    problem, _ = module.consecutive_moment_opi_reduction(p, [0] * 31, length=95)
    existing = one_trial_IID_source_bound(problem)
    exact = Fraction(existing["success_probability_lower_exact"])
    row = module.masking_certificate(p, 127, 31, 32)
    lower = Fraction(row["IID_norm_population_success_lower_exact"])
    assert existing["norm_target_degree"] == row["norm_target_degree"] == 48
    assert lower <= exact < lower + Fraction(1, 1 << 96)
    assert not existing["fixed_instance_probability_bound"]


def test_full_small_fixed_target_distribution_survives_the_bound():
    row = module.masking_certificate(7, 6, 1, 2)
    floor = Fraction(row["EVERY_fixed_target_one_attempt_success_lower_exact"])
    control = module.exact_small_amplification_control()
    assert control["explicit_cases_enumerated"] == 2401
    assert [x["masked_irreducible_hits"] for x in control["rows"]] == [136, 144, 136, 144, 144, 168, 136]
    assert all(Fraction(x["masked_irreducible_hits"], 343) >= floor for x in control["rows"])
    bad = control["rows"][5]
    assert bad["no_prefix_irreducible_hits"] == 0
    assert bad["masked_irreducible_hits"] > 0
    # The unmasked monic pencil failure is not unsatisfiability.
    assert module.native_moments(7, [1, 2, 0, 0, 0, 0], 1, points=(1, 2, 3, 4, 5, 6)) == [5]


def test_bad_norm_degree_budget_does_not_create_a_probability_claim():
    row = module.masking_certificate((1 << 61) - 1, 127, 50, 51)
    assert row["status"] == "UNKNOWN_NO_POSITIVE_SUCCESS_FLOOR"
    assert row["EVERY_fixed_target_one_attempt_success_lower_exact"] == "0"
    assert row["independent_uniform_coin_trial_budget"] is None
    result = module.attack((1 << 61) - 1, [0] * 50, length=127, reserve=51)
    assert result["status"] == "UNKNOWN_CERTIFICATE_GATE"


def test_seeded_small_attack_verifies_the_unchanged_target_and_prefix():
    for target in ([0], [5]):
        row = module.attack(7, target, length=6, reserve=2, seed=7711, trials=64)
        assert row["status"] == "CLASSICAL_FIXED_TARGET_MASKED_NORM_WITNESS"
        values = row["native_square_roots_x"]
        assert any(values)
        assert module.native_moments(7, values, 1, points=(1, 2, 3, 4, 5, 6)) == target
        winner = row["attempts"][row["winning_attempt"]]
        assert values[-2:] == winner["reserved_values"]
        assert row["randomness_policy"] == "SEEDED_REPLAY_NOT_A_CONFIDENCE_CERTIFICATE"


def test_failed_attempt_budget_retains_original_target_and_is_unknown(monkeypatch):
    monkeypatch.setattr(module, "norm_attack", lambda *a, **k: {"status": "TEST_FORCED_NO_WITNESS"})
    target = [1] * 31
    row = module.attack((1 << 61) - 1, target, length=127, reserve=32, trials=2)
    assert row["status"] == "UNKNOWN_PAID_NATIVE_MASK_BUDGET"
    assert row["ORIGINAL_target"] == target
    assert row["source_rerolls"] == 0
    assert len(row["attempts"]) == 2
    assert not row["original_field_or_coefficients_changed"]


@pytest.mark.parametrize("args", [(7, 6, 2, 1), (5, 4, 1, 2), (7, 7, 1, 2)])
def test_certificate_refuses_unsupported_domains(args):
    with pytest.raises(ValueError):
        module.masking_certificate(*args)


def test_saved_report_binds_sources_and_native_outputs_not_just_status_flags():
    report = json.loads(module.REPORT.read_text())
    assert report["source_sha256"] == module.sha256(module.__file__)
    for f, digest in report["dependency_sha256"].items():
        assert module.sha256(module.ROOT / "theorems" / f) == digest
    assert report["no_central_candidate_negative_or_proof_promotion"]
    for row in report["native_controls"]:
        assert row["status"] == "CLASSICAL_FIXED_TARGET_MASKED_NORM_WITNESS"
        values = row["native_square_roots_x"]
        assert len(values) == 127 and any(values)
        assert module.native_moments((1 << 61) - 1, values, 31,
                                     points=tuple(range(1, 128))) == row["ORIGINAL_target"]
        assert row["certificate"]["nontrivial_homogeneous_output_guaranteed_on_success"]
        assert not row["accepted_speedup_or_central_proof_promotion"]


@pytest.mark.parametrize("p", [7, 11, 19, 31, 43, 67])
def test_even_consecutive_derivatives_have_exactly_balanced_square_classes(p):
    from math import prod
    for n in range(2, min(14, p - 1) + 1, 2):
        derivatives = [prod(a - b for b in range(1, n + 1) if a != b) % p
                       for a in range(1, n + 1)]
        assert all((left + right) % p == 0 for left, right in zip(derivatives, reversed(derivatives)))
        assert sum(pow(d, (p - 1) // 2, p) == 1 for d in derivatives) == n // 2


def test_reflection_balance_cannot_be_assumed_for_other_fields_or_supports():
    from math import prod
    for p, points in ((13, (1, 2, 3, 4)), (11, (1, 2, 3, 6))):
        classes = {pow(prod(a - b for b in points if b != a) % p, (p - 1) // 2, p) for a in points}
        assert len(classes) == 1


def test_uniform_parameters_need_no_derivative_table_or_matrix(monkeypatch):
    monkeypatch.setattr(module, "consecutive_moment_opi_reduction",
                        lambda *a, **k: pytest.fail("analytic parameters must not build a native matrix"))
    row = module.uniform_family_parameters((1 << 31) - 1, 4096, 1024)
    assert row["status"] == "UNIFORM_FAMILY_LOCAL_REVIEW_PENDING"
    assert row["remaining_coordinates"] % 2 == 0
    assert row["remaining_coordinates"] >= 2 * row["rank"] + 4
    assert row["no_derivative_table_or_matrix_was_built"]
    assert row["scalar_parameter_arithmetic_only_no_large_solver_execution"]
    assert not row["independent_review_or_formal_verification_completed"]


def test_uniform_parameter_inequalities_are_exact_not_floating_point_guesses():
    for p, L, r in (((1 << 61) - 1, 127, 31), (8191, 1024, 256), ((1 << 31) - 1, 4096, 1024)):
        row = module.uniform_family_parameters(p, L, r)
        s, n = row["reserved_coordinates"], row["remaining_coordinates"]
        assert 64 * L * L * 2 ** s <= p ** (s - r)
        assert p ** s >= 16 * L
        assert n % 2 == 0 and n >= 2 * r + 4
        assert 2 ** row["required_bound_precision_bits"] >= 64 * L
        assert Fraction(row["uniform_one_attempt_success_floor_exact"]) == Fraction(1, 4 * L)
        assert row["norm_target_degree"] < n - r


def test_every_small_quarter_window_has_the_uniform_split_over_smallest_eligible_primes():
    from sympy import nextprime
    for L in range(64, 513):
        p = int(nextprime(L))
        while p % 4 != 3:
            p = int(nextprime(p))
        row = module.uniform_family_parameters(p, L, L // 4)
        assert row["status"] == "UNIFORM_FAMILY_LOCAL_REVIEW_PENDING"
        assert row["all_p_gt_L_ge_64_and_4r_le_L_are_in_uniform_regime"]


def test_uniform_unknown_gate_is_not_an_unsatisfiability_claim():
    row = module.attack_uniform(67, [0] * 21, length=64)
    assert row["status"] == "UNKNOWN_UNIFORM_PARAMETER_GATE"
    assert row["uniform_parameters"]["uniform_one_attempt_success_floor_exact"] == "0"
    with pytest.raises(ValueError, match="p3mod4"):
        module.uniform_family_parameters(97, 64, 16)


def test_uniform_workflow_keeps_actual_certificate_and_native_input():
    report = json.loads(module.REPORT.read_text())
    assert report["schema_version"] == "moment-target-masking-v2"
    controls = report["uniform_family_actual_native_controls"]
    assert [(r["certificate"]["ORIGINAL_length"], len(r["ORIGINAL_target"])) for r in controls] == [
        (127, 31), (127, 31), (320, 80)]
    for row in controls:
        assert row["status"] == "CLASSICAL_FIXED_TARGET_MASKED_NORM_WITNESS"
        c, params = row["certificate"], row["uniform_parameters"]
        L, p, rank = c["ORIGINAL_length"], c["prime"], c["rank"]
        assert c["remaining_orientation_counts"] == params["remaining_orientation_counts_from_reflection"]
        assert Fraction(c["EVERY_fixed_target_one_attempt_success_lower_exact"]) >= Fraction(1, 4 * L)
        assert module.native_moments(p, row["native_square_roots_x"], rank,
                                     points=tuple(range(1, L + 1))) == row["ORIGINAL_target"]
        assert not row["original_field_or_coefficients_changed"]

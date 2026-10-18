"""Independent finite-difference, native-field, flat and restricted-ANF controls."""
from dataclasses import replace
from fractions import Fraction
import hashlib
import json
import random

import pytest

from theorems.bpqm_gibbs_frontier import affine_system
from theorems.explicit_cubic_opi import (
    BooleanCubic, CubicOPI, REPORT, accepted_flat, arbitrary_flat_bound,
    blind_pool_tail_bound, flat_attack, from_specification, instance, monomials, optimize_affine_space,
)
from theorems.explicit_quadratic_opi import (
    OPIReferenceLimit, _affine_words, evaluation_masks, exact_small_filter_law, filter_bound,
)


def span_points(origin, basis):
    points = [origin]
    for v in basis:
        points += [x ^ v for x in points]
    return points


@pytest.mark.parametrize("m", [2, 3, 6])
def test_polarization_equals_all_eight_native_values_and_is_alternating(m):
    rng = random.Random(29)
    g = BooleanCubic(m, rng.getrandbits(len(monomials(m))))
    for _ in range(70):
        a, v, w, x = [rng.getrandbits(m) for _ in range(4)]
        third = 0
        for mask in range(8):
            y = x
            for i, direction in enumerate((a, v, w)):
                if (mask >> i) & 1:
                    y ^= direction
            third ^= g.value(y)
        assert third == (g.polar_row(v, w) & a).bit_count() % 2
        assert g.polar_row(v, v) == 0
        assert g.polar_row(v, w) == g.polar_row(w, v)
        assert (g.polar_row(v, w) & v).bit_count() % 2 == 0


def test_all_small_cubics_remain_balanced_including_degenerate_sources():
    transforms = (tuple(1 << j for j in range(4)),)
    for coefficients in range(1 << len(monomials(3))):
        p = CubicOPI(4, 1, 1, transforms, (BooleanCubic(3, coefficients),))
        assert sum(p.accepted(0, y) for y in range(16)) == 8
    with pytest.raises(ValueError):
        BooleanCubic(3, 1 << len(monomials(3)))
    with pytest.raises(ValueError):
        replace(p, transforms=((1, 1, 4, 8),))


@pytest.mark.parametrize("bits,N,K", [(4, 7, 3), (15, 5, 2), (31, 5, 2)])
def test_large_field_small_length_geometry_agrees_with_independent_FLINT_Horner(bits, N, K):
    p, rng = instance(bits, N, K, 71), random.Random(29)
    for _ in range(8):
        word = rng.getrandbits(bits*K)
        symbols = p.evaluations(word)
        for i, row in enumerate(evaluation_masks(bits, K, N)):
            assert symbols[i] == sum(((h & word).bit_count() % 2) << j for j, h in enumerate(row))
            z = sum(((h & word).bit_count() % 2) << j for j, h in enumerate(p.forms[i]))
            assert p.accepted(i, symbols[i]) == p.transformed_accepted(i, z)
    assert from_specification(p.specification()) == p
    wrong = p.specification()
    wrong["field_modulus_coefficients"][0] ^= 1
    with pytest.raises(ValueError, match="basis/modulus"):
        from_specification(wrong)
    with pytest.raises(ValueError):
        evaluation_masks(bits, K, 1 << bits)


@pytest.mark.parametrize("m", [3, 8, 14, 30])
def test_constructed_affine_flats_are_independent_and_every_point_is_accepted(m):
    g = BooleanCubic(m, random.Random(71).getrandbits(len(monomials(m))))
    flat = accepted_flat(g, 29)
    assert len(flat["parity_checks"]) == m+1-flat["dimension"]
    assert affine_system(tuple((v, 0) for v in flat["directions"]), m+1)["rank"] == flat["dimension"]
    for z in span_points(flat["origin"], flat["directions"]):
        assert (z & 1) == g.value(z >> 1)
        assert all(((z ^ flat["origin"]) & h).bit_count() % 2 == 0 for h in flat["parity_checks"])
    assert flat["linear_solves"] > 0
    assert flat["polynomial_evaluations"] >= 1 << flat["dimension"]
    assert flat["source_rejected_or_resampled"] is False
    assert flat["maximum_flat_certified"] is False


def test_incompatible_isotropic_directions_fall_back_without_resampling_the_polynomial():
    # g(x)=x0*x1: full 2-space is cubic-isotropic but has a nonzero quadratic term.
    coefficients = 1 << monomials(2).index(3)
    g = BooleanCubic(2, coefficients)
    flat = accepted_flat(g, 29, attempts=2, target_dimension=2)
    assert [t["base_consistent"] for t in flat["attempt_trace"][:2]] == [False, False]
    assert flat["dimension"] == 1
    assert g.coefficients == coefficients


@pytest.mark.parametrize("seed", [29, 71])
def test_restricted_cubic_Mobius_scores_match_every_native_field_message(seed):
    p = instance(4, 7, 3, seed)
    system = affine_system(((0b10101, 1), (0b101000, 0), (0b110000000, 1)), p.message_bits)
    all_scores = [p.score_count(word) for word in _affine_words(system, p.message_bits, 12)]
    expected = max(all_scores)
    out = optimize_affine_space(p, system)
    assert out["score_count"] == expected
    assert out["affine_score_histogram"] == [all_scores.count(j) for j in range(p.length+1)]
    assert p.score_count(int(out["message_hex"], 16)) == expected
    assert out["candidate_messages_enumerated"] == 1 << len(system["free"])
    assert out["Mobius_xor_cells"] == p.length*len(system["free"])*(1 << (len(system["free"])-1))
    assert out["global_optimum_claimed"] is False
    assert out["peak_candidate_dense_table_bytes"] == 5*(1 << len(system["free"]))


def test_zero_dimensional_affine_space_and_caps_have_correct_meaning():
    p = instance(4, 7, 3, 29)
    word = 123
    system = affine_system(tuple((1 << j, (word >> j) & 1) for j in range(p.message_bits)), p.message_bits)
    out = optimize_affine_space(p, system, max_free_bits=0)
    assert out["message_hex"] == hex(word)
    assert out["candidate_messages_enumerated"] == 1
    assert out["score_count"] == p.score_count(word)
    with pytest.raises(OPIReferenceLimit, match="UNKNOWN"):
        optimize_affine_space(p, affine_system((), p.message_bits), max_free_bits=0)
    out = flat_attack(p, 29, max_free_bits=0)
    assert out["status"] == "RESIDUAL_OPTIMIZER_UNKNOWN_UNIFORM_FALLBACK"
    assert not out["classical_hardness_inferred"]


def test_all_forced_positions_survive_original_native_not_relaxed_verification():
    p = instance(15, 31, 9, 29)
    out = flat_attack(p, 10029)
    symbols = p.evaluations(int(out["message_hex"], 16))
    assert sum(p.accepted(i, y) for i, y in enumerate(symbols)) == out["score_count"]
    assert all(p.accepted(i, symbols[i]) for i in out["forced_positions"])
    assert out["flat_finder_work_including_unused_terminal_flat"]["linear_solves"] > 0
    assert out["source_rejected_or_resampled"] is False


def test_ideal_DQI_small_cubic_law_is_normalized_and_no_source_prep_is_claimed():
    p = instance(4, 7, 3, 71)
    law, bound = exact_small_filter_law(p), filter_bound(p)
    assert law["normalization"] == pytest.approx(1, abs=1e-12)
    assert law["mean_score"] == pytest.approx(float(Fraction(bound["expected_score_lower"])), abs=1e-12)
    assert not bound["coherent_RS_decoder_and_filter_circuit_executed"]
    assert not bound["oracle_classical_lower_bound_transferred_to_explicit_predicates"]


def test_arbitrary_flat_first_moment_bound_is_exact_for_all_RM3_polynomials_in_two_variables():
    # A 2-flat in the 3-bit graph must project to the entire 2D base: g must be affine.
    affine_graphs = sum(not (coeff & (1 << monomials(2).index(3))) for coeff in range(16))
    out = arbitrary_flat_bound(3, 2)
    assert Fraction(out["raw_first_moment_union_bound"]) == Fraction(affine_graphs, 16) == Fraction(1, 2)
    out = arbitrary_flat_bound(63, 20, 127)
    assert Fraction(out["probability_upper"]) < Fraction(1, 1 << 300)
    assert not out["absence_of_large_flats_proves_OPI_hardness"]


def test_large_exact_flat_bound_does_not_disable_Python_integer_string_safety():
    out = arbitrary_flat_bound(100, 80)
    assert out["raw_first_moment_union_bound"] is None
    raw = Fraction(int(out["raw_first_moment_numerator_hex"], 16),
                   1 << out["raw_first_moment_denominator_power_two"])
    assert raw <= Fraction(1, 1 << out["probability_upper_power_two_exponent"])


def test_suffix_pool_bound_covers_exhaustive_sources_and_is_not_generic_hardness():
    out = blind_pool_tail_bound(3, 1, 1, 3)
    # Give the exposed predicate a free success: two independent remaining
    # coefficient constants yield four equally likely outcomes at any fixed word.
    assert Fraction(out["success_probability_union_upper"]) == Fraction(1, 4)
    assert blind_pool_tail_bound(3, 1, 8, 3)["success_probability_union_upper"] == "1"
    assert out["pool_must_be_fixed_before_suffix_scores_are_seen"]
    assert out["bounds_only_this_pool_not_all_classical_algorithms"]
    assert not out["quantum_tail_or_runtime_comparison_supplied"]
    # Analytic model calculation, not a generated or solved large instance.
    asymptotic_control = blind_pool_tail_bound(4095, 1300, 1 << 40, 3400)
    assert Fraction(asymptotic_control["success_probability_union_upper"]) < Fraction(1, 1 << 200)


def test_saved_report_keeps_every_instance_attempt_and_no_speedup_admission():
    if not REPORT.exists():
        pytest.skip("live report not generated yet")
    report = json.loads(REPORT.read_text())
    from pathlib import Path
    assert report["source_sha256"] == hashlib.sha256(Path("theorems/explicit_cubic_opi.py").read_bytes()).hexdigest()
    for name, digest in report["dependency_sha256"].items():
        assert digest == hashlib.sha256((Path("theorems")/name).read_bytes()).hexdigest()
    assert len(report["instances"]) == 8
    assert not report["accepted_speedup_candidate"]
    for row in report["instances"]:
        p = from_specification(row["specification"])
        trials = row["paid_classical_trials"]
        assert len(trials) == 4
        assert row["best_score_count"] == max(t["score_count"] for t in trials)
        for trial in trials:
            word = int(trial["message_hex"], 16)
            assert p.score_count(word) == trial["score_count"]
            symbols = p.evaluations(word)
            assert all(p.accepted(i, symbols[i]) for i in trial["forced_positions"])
            assert trial["attack_seed"] >= 10000
            if trial["exact_optimum_on_this_affine_space"]:
                assert sum(trial["affine_score_histogram"]) == trial["candidate_messages_enumerated"]

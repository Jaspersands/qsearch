"""Divisor-free fibers: character-count constants, public setup and native output."""

from fractions import Fraction
import hashlib
from itertools import combinations, product
import json
import math

from flint import fmpz
import pytest

import theorems.interval_split_fibers as module
from theorems.interval_split_fibers import REPORT, construct, public_frame, run_controls, setup_bound, solve
from theorems.interval_subgroup_rounding import nearest_certificate, round_frame, translation_frame
from theorems.interval_character_rounding import particular_for_syndrome


def moments(p, d, word):
    return [sum(pow(x, j, p) * a for x, a in enumerate(word)) % p for j in range(d)]


def polynomial_from_roots(p, roots):
    coefficients = [1]
    for r in roots:
        result = [0] * (len(coefficients) + 1)
        for i, a in enumerate(coefficients):
            result[i] = (result[i] - r * a) % p
            result[i + 1] = (result[i + 1] + a) % p
        coefficients = result
    return coefficients


def test_uniform_character_expansion_and_zero_correction_independently_exhausted():
    for p in (3, 5, 7, 11, 13):
        squares = {a * a % p for a in range(1, p)}
        chi = lambda x: 0 if x % p == 0 else (1 if x % p in squares else -1)
        for M in range(1, min(4, p - 1) + 1):
            certificate = setup_bound(p, M)
            lower = Fraction(certificate["legal_shifts_uniform_count_lower_exact"])
            expected_K = sum((Fraction(math.comb(M, r) * (r - 1), 1 << M) for r in range(1, M + 1)), Fraction(0))
            assert Fraction(certificate["squarefree_Weil_sum_coefficient_exact"]) == expected_K
            assert certificate["sqrt_p_outward_upper_integer"] ** 2 >= p
            for values in combinations(range(p), M):
                good = sum(all((v - b) % p in squares for v in values) for b in range(p))
                expanded = sum((Fraction(math.prod(1 + chi(v - b) for v in values), 1 << M) for b in range(p)), Fraction(0))
                assert 0 <= expanded - good <= Fraction(M, 2)
                assert good >= lower
                if M == 1:
                    assert good == lower == Fraction(p - 1, 2)
                # Independent exact-squared bounded checks of the only
                # character-sum hypothesis used in the setup derivation.
                for r in range(1, M + 1):
                    for subset in combinations(values, r):
                        total = sum(math.prod(chi(v - b) for v in subset) for b in range(p))
                        assert total * total <= (r - 1) ** 2 * p


@pytest.mark.parametrize("p,ell", [(7, 1), (47, 4), (347, 8), (1019, 16), (4093, 8)])
def test_composed_split_fibers_full_degree_disjointness_and_native_moments(p, ell):
    setup = construct(p, ell)
    assert setup["status"] == "VERIFIED_TWO_FULLY_SPLIT_FIBERS"
    A, B, w = set(setup["fiber_zero"]), set(setup["fiber_one"]), setup["waveform"]
    assert len(A) == len(B) == ell and not A & B
    FA, FB = polynomial_from_roots(p, sorted(A)), polynomial_from_roots(p, sorted(B))
    assert FA == setup["fiber_zero_polynomial_coefficients"]
    assert FB == setup["fiber_one_polynomial_coefficients"]
    assert [(a - b) % p for a, b in zip(FA, FB)] == [1] + [0] * ell
    assert moments(p, ell, w) == [0] * ell
    assert moments(p, ell + 1, w)[-1] == (-ell) % p
    assert sum(a * a for a in w) == 2 * ell
    shifts = [stage["selected_shift"] for stage in setup["stages"]]
    for x in range(p):
        value = x
        for b in reversed(shifts):
            value = (value * value + b) % p
        assert (value == 0) == (x in A)
        assert (value == 1) == (x in B)
    assert not setup["affine_target_used_to_select_setup"]
    if ell >= 8:
        assert (p - 1) % ell and (p + 1) % ell


def test_every_shift_scan_and_modular_root_cost_replays_without_prime_residue_oracle():
    for p, ell in ((347, 8), (1019, 16), (347, 16)):
        setup = construct(p, ell)
        squares = {x * x % p for x in range(1, p)}
        tests = root_calls = 0
        for i, stage in enumerate(setup["stages"]):
            A, B = set(stage["input_fiber_zero"]), set(stage["input_fiber_one"])
            values = sorted(A | B)
            selected, zero, nonsquare = stage["selected_shift"], 0, 0
            budget = p if selected is None else selected + 1
            for b in range(budget):
                for v in values:
                    tests += 1
                    difference = (v - b) % p
                    if difference not in squares:
                        zero += int(difference == 0)
                        nonsquare += int(difference != 0)
                        break
                else:
                    assert b == selected
            assert stage["candidate_shifts_tested"] == budget
            assert stage["rejected_zero_shifts"] == zero
            assert stage["rejected_nonsquare_shifts"] == nonsquare
            if selected is not None:
                root_calls += len(values)
                next_A = {x for x in range(p) if (x * x + selected) % p in A}
                next_B = {x for x in range(p) if (x * x + selected) % p in B}
                target = setup["stages"][i + 1] if i + 1 < len(setup["stages"]) else setup
                assert next_A == set(target.get("input_fiber_zero", target.get("fiber_zero", [])))
                assert next_B == set(target.get("input_fiber_one", target.get("fiber_one", [])))
        assert tests == setup["modular_character_tests_charged"]
        assert root_calls == setup["modular_square_roots_charged"]


def test_positive_uniform_bound_is_distinct_from_a_successful_instance_and_large_arrays():
    good = construct(1021, 4)
    assert good["setup_Weil_certificate"]["every_distinct_constraint_set_has_a_legal_shift_certified"]
    assert Fraction(good["setup_Weil_certificate"]["legal_shifts_uniform_count_lower_exact"]) == Fraction(445, 16)
    explicit = construct(347, 8)
    assert not explicit["setup_Weil_certificate"]["every_distinct_constraint_set_has_a_legal_shift_certified"]
    assert explicit["waveform"] is not None  # A sufficient criterion is not necessary.
    large = setup_bound((1 << 61) - 1, 16)
    assert large["every_distinct_constraint_set_has_a_legal_shift_certified"]
    assert not large["full_field_table_or_quantum_state_materialized"]
    assert "waveform" not in large
    with pytest.raises(ValueError):
        construct((1 << 61) - 1, 16)


@pytest.mark.parametrize("p", [347, 4093])
def test_failed_public_setup_never_promotes_partial_frame_or_original_hardness(p):
    setup = construct(p, 16)
    assert setup["status"] == "PUBLIC_FRAME_SETUP_EXHAUSTED_NOT_HARDNESS"
    assert setup["ell"] == 16 and setup["achieved_degree"] == 8
    assert setup["waveform"] is None and not setup["original_problem_unsatisfiability_claimed"]
    assert setup["stages"][-1]["candidate_shifts_tested"] == p
    assert not any(all(pow((v - b) % p, (p - 1) // 2, p) == 1
                       for v in set(setup["stages"][-1]["input_fiber_zero"] + setup["stages"][-1]["input_fiber_one"])) for b in range(p))
    # Even a trivial zero target/full interval is not assigned an unbuilt frame.
    result = solve(p, 16, 16, p // 2, [0] * p)
    assert result["solution"] is None and not result["affine_target_admitted_to_rounding"]


def test_generic_frame_gates_reject_zero_nonzero_integer_sum_and_undercounted_norm():
    with pytest.raises(ValueError):
        translation_frame(7, 1, [0] * 7, expected_first=0, expected_norm=0)
    with pytest.raises(ValueError):
        translation_frame(7, 1, [1] * 7, expected_first=0, expected_norm=7)
    with pytest.raises(ArithmeticError):
        translation_frame(7, 1, [1, -1] + [0] * 5, expected_first=6, expected_norm=1)
    _, model = public_frame(47, 4)
    bad = dict(model, squared_waveform_norm=model["squared_waveform_norm"] - 1)
    with pytest.raises(ValueError):
        round_frame(bad, 4, 6, [0] * 47)


def test_nearest_sparse_bound_solves_all_small_syndromes_without_randomness(monkeypatch):
    _, model = public_frame(7, 2)
    certificate = nearest_certificate(model, 2)
    B = [[1] * 7] + [[model["waveform"][(x - t) % 7] for x in range(7)] for t in range(6)]
    assert certificate["maximum_column_l1_exact"] == max(sum(abs(row[x]) for row in B) for x in range(7)) == 5
    assert certificate["all_target_centered_integer_radius"] == 2

    def forbidden_rng(*args, **kwargs):
        raise AssertionError("nearest rounding must not construct a PRNG")

    monkeypatch.setattr(module.random, "Random", forbidden_rng)
    for a in range(7):
        for b in range(7):
            y = particular_for_syndrome(7, 2, [a, b])
            result = round_frame(model, 2, 2, y, rounding="nearest")
            assert result["solution"] is not None and result["rounding_seed_for_replay_only"] is None
            assert result["nearest_rounding_certificate"]["requested_interval_uniformly_solved"]
            assert result["failure_certificate"]["comparison_only_not_active_rounding_model"]
            e = result["solution"]["centered_affine_witness"]
            assert moments(7, 2, e) == [a, b] and max(map(abs, e)) <= 2


def test_nearest_actual_success_below_uniform_radius_does_not_upgrade_the_bound():
    _, model = public_frame(7, 2)
    success = round_frame(model, 2, 0, [0] * 7, rounding="nearest")
    assert success["solution"] is not None
    assert not success["nearest_rounding_certificate"]["requested_interval_uniformly_solved"]
    y = particular_for_syndrome(7, 2, [1, 0])
    failure = round_frame(model, 2, 0, y, rounding="nearest")
    assert failure["solution"] is None
    assert failure["status"] == "NEAREST_FAILED_REQUESTED_WIDTH_NOT_HARDNESS"
    assert len(failure["attempts"]) == 1


def test_small_integer_moment_rows_respect_the_Newton_mass_lower_bound():
    # The proof is in the research note. This checks both unit coefficients
    # and multiplicities2, not only a preferred construction's own flags.
    for p, alphabet in ((5, (-2, -1, 0, 1, 2)), (7, (-1, 0, 1))):
        for w in product(alphabet, repeat=p):
            if sum(w) or not any(w):
                continue
            mass = sum(max(a, 0) for a in w)
            for ell in range(1, p // 2 + 1):
                if not any(moments(p, ell, w)):
                    assert mass >= ell
                    assert sum(abs(a) for a in w) >= 2 * ell
                    assert sum(a * a for a in w) >= 2 * ell
    setup = construct(347, 8)
    w = setup["waveform"]
    assert sum(abs(a) for a in w) == sum(a * a for a in w) == 16


@pytest.mark.parametrize("p,ell", [(9, 4), (7, 4), (47, 3), (47, True), (47, 0)])
def test_invalid_source_degrees_or_prime_models_are_rejected(p, ell):
    with pytest.raises(ValueError):
        construct(p, ell)


def test_saved_native_artifact_provenance_and_independent_Horner_replay():
    report = json.loads(REPORT.read_text())
    assert report == run_controls()
    assert report["source_sha256"] == hashlib.sha256(module.Path(module.__file__).read_bytes()).hexdigest()
    assert report["all_declared_native_targets_verified"] and len(report["controls"]) == 4
    for r in report["controls"]:
        p, d, y, ell = r["p"], r["d"], r["public_particular_word"], r["ell"]
        assert r["affine_target_admitted_to_rounding"]
        assert r["u"] <= r["best_torus_certified_radius"]
        e, coefficients = r["solution"]["centered_affine_witness"], r["solution"]["polynomial_coefficients"]
        assert moments(p, d, e) == moments(p, d, y) == r["target_syndrome"]
        assert max(map(abs, e)) <= r["u"] and len(coefficients) == p - ell
        for x in range(p):
            value = 0
            for a in reversed(coefficients):
                value = (value * x + a) % p
            assert (y[x] - e[x] - value) % p == 0
        if r["rounding_mode"] == "nearest":
            assert r["nearest_rounding_certificate"]["requested_interval_uniformly_solved"]
            assert r["failure_certificate"]["comparison_only_not_active_rounding_model"]
        else:
            assert Fraction(r["failure_certificate"]["per_attempt_all_target_failure_upper_exact"]) <= Fraction(1, 2)
        assert r["coordinate_denominator_bits"] == int(fmpz(r["coordinate_common_denominator_decimal"])).bit_length()
        assert r["quantum_uniform_interval_sufficient_condition_met"]
    assert not report["general_unconditional_setup_at_arbitrary_degree_claimed"]
    assert not report["novelty_quantum_speedup_or_prescribed_sampling_claimed"]

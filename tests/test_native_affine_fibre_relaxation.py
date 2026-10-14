"""Exact affine-coordinate/filter price with known F3 escape and real ring carries."""
from dataclasses import replace
from fractions import Fraction
from itertools import product
import json
import subprocess

import pytest

from theorems import native_affine_fibre_relaxation as A
from native_short_preimage_reduction import PublicWordFamily, verify_receipt


@pytest.mark.parametrize("r", (1, 2, 7, 64, 128))
def test_unit_minor_inverse_lifts_over_composite_moduli_without_field_assumption(r):
    q = 3**r
    S = ((0, 1), (1, q-1))
    X, steps = A.unit_minor_inverse(S, q)
    assert A.matrix_product(S, X, q) == ((1, 0), (0, 1))
    assert A.matrix_product(X, S, q) == ((1, 0), (0, 1))
    assert steps[0] == 1 and steps[-1] == r
    assert all(b == min(2*a, r) for a, b in zip(steps, steps[1:]))


def test_nonunit_inverse_is_unsupported_not_proof_of_no_solution():
    with pytest.raises(A.NonFreeRank, match="not no solutions"):
        A.unit_minor_inverse(((3,),), 9)
    with pytest.raises(A.NonFreeRank, match="not no solutions"):
        A.affine_recipe(((3,),), 9)
    assert 3*1 % 9 == 3  # A nonfree map has this actual solution.


@pytest.mark.parametrize("r", (1, 2, 16, 64))
def test_public_coordinate_bijection_uses_off_diagonal_unit_pivots(r):
    q = 3**r
    matrix = ((0, 1, q-1, 0), (1, 1, 0, 1))
    recipe = A.affine_recipe(matrix, q)
    for z in ((0, 0, 0, 0), (1, 2, q-1, 0), (q-1,)*4):
        target, free = recipe.coordinates(z)
        assert recipe.solve(target, free) == z
    rec = recipe.record()
    assert rec["free_registers"] == 2 and rec["uniform_free_register_trits"] == 2*r
    assert not rec["uses_composite_modulus_field_inverse"]
    assert not rec["physical_gate_synthesis_and_precision_supplied"]


@pytest.mark.parametrize("matrix,q", ((((0, 0),), 9), (((True, 0),), 3), (((1., 0),), 3),
                                     (((9, 0),), 9), (((1,), (0,)), 3), (((1, 0), (1,)), 3)))
def test_invalid_or_nonfree_matrix_is_rejected(matrix, q):
    with pytest.raises(ValueError): A.affine_recipe(matrix, q)


def test_malformed_recipe_cannot_return_an_unverified_affine_solution():
    recipe = A.affine_recipe(((1, 2),), 9)
    forged = replace(recipe, pivot_inverse=((0,),))
    with pytest.raises(ArithmeticError, match="invert"):
        forged.solve((1,), (0,))


@pytest.mark.parametrize("target,free", (((9,), (0,)), ((0,), (9,)), ((True,), (0,)), ((0,), ()), ((), (0,))))
def test_affine_coordinates_require_canonical_exact_inputs(target, free):
    recipe = A.affine_recipe(((1, 2),), 9)
    with pytest.raises(ValueError): recipe.solve(target, free)


def test_complete_finite_coordinate_map_is_a_permutation_and_membership_count_is_exact():
    q, matrix = 9, ((3, 1, 4, 2),)
    recipe = A.affine_recipe(matrix, q)
    seen = set()
    counts = [0]*q
    for target in product(range(q), repeat=1):
        for free in product(range(q), repeat=3):
            z = recipe.solve(target, free)
            assert recipe.coordinates(z) == (target, free)
            seen.add(z)
            if A.selector_word(z, q) is not None: counts[target[0]] += 1
    assert len(seen) == q**4 and sum(counts) == 9
    assert sum(Fraction(c, q**3) for c in counts)/q == Fraction(1, 729)


@pytest.mark.parametrize("r", (1, 2, 16, 64))
def test_membership_checks_actual_signed_selector_pairs(r):
    q = 3**r
    for word in product(range(3), repeat=3):
        z = tuple(a for t in word for a in ((1, 0), (q-1, 1), (0, q-1))[t])
        assert A.selector_word(z, q) == word
    assert A.selector_word((0, 0, 1, 0), q) is None
    with pytest.raises(ValueError): A.selector_word((1,), q)


@pytest.mark.parametrize("r", (1, 2, 16, 64))
def test_F3_linearization_and_cyclic_closure_do_not_extend_to_higher_root(r):
    q = 3**r
    certificate = A.selector_affine_certificate(q)
    v0, slope, third = (1, 0), (-2, 1), (0, -1)
    defect = tuple((third[i]-v0[i]-2*slope[i]) % q for i in range(2))
    assert certificate["third_selector_affine_extrapolation_defect"] == defect == (3 % q, -3 % q)
    assert certificate["F3_slope_cyclic_closure_defect"] == tuple(3*s % q for s in slope)
    assert certificate["native_selector_is_an_F3_affine_line_for_arbitrary_public_pairs"] == (r == 1)
    assert not certificate["higher_root_carries_may_be_discarded"]


def test_particular_label_extrapolation_is_not_a_general_F3_group_map():
    family = PublicWordFamily(9, 1, 1, 1, ((((1,), (1,)),),))
    outputs = [family.frequency(0, (t,))[0] for t in range(3)]
    assert outputs == [1, 0, 8]
    assert outputs[2] == (outputs[0]+2*(outputs[1]-outputs[0])) % 9
    assert 3*(outputs[1]-outputs[0]) % 9 != 0  # Wrapping t modulo3 is still illegal.
    with pytest.raises(ValueError, match="higher roots"):
        A.EndpointLabelHelper(family)


def test_endpoint_preimages_are_label_only_and_recover_actual_original_values():
    c = A.endpoint_control()
    assert c["matches_truth_fixture"] and c["label_only_helper_calls"] == 2
    assert c["actual_original_data_reconstruction"]["original_secret"] == (2, 0)
    assert not c["growing_root_helper_or_new_quantum_algorithm"]
    assert not c["actual_original_data_reconstruction"]["new_quantum_algorithm_or_speedup"]


def test_endpoint_direct_fibres_have_no_unrestricted_membership_penalty():
    pairs = (((1, 0), (1, 0)), ((0, 1), (0, 1)), ((1, 1), (2, 1)))
    family = PublicWordFamily(3, 2, 1, 3, (pairs,))
    b, offset, recipe = A.endpoint_recipes(family)[0]
    helper = A.EndpointLabelHelper(family)
    for target in product(range(3), repeat=2):
        direct = {recipe.solve(tuple((x-y) % 3 for x, y in zip(target, offset)), free)
                  for free in product(range(3), repeat=len(recipe.free_columns))}
        actual = {w for w in product(range(3), repeat=3) if family.frequency(b, w) == target}
        assert direct == actual and len(actual) == 3
        verify_receipt(family, target, helper(family, target))


def test_endpoint_helper_rejects_nonfree_cohorts_without_calling_all_native_fibres_empty():
    family = PublicWordFamily(3, 1, 1, 1, ((((1,), (2,)),),))
    with pytest.raises(A.NonFreeRank, match="not no native solutions"): A.EndpointLabelHelper(family)
    assert all(family.frequency(0, (t,)) == (1,) for t in range(3))


@pytest.mark.parametrize("n", (8, 32, 64, 128))
def test_growing_filter_ledger_is_compact_and_scoped_not_a_universal_bound(n):
    M = n*n+24
    L = A.filter_ledger(n, n, 1, M)
    E = n*(2*M-n)-M
    assert L["per_target_filter_acceptance_upper"] == {"base": 3, "negative_exponent": E}
    assert L["uniform_target_mean_filter_acceptance"]["negative_exponent"] == (2*n-1)*M
    assert L["half_success_requires_ordinary_amplification_multiplier_square_at_least"] == {"base": 3, "exponent": E, "denominator": 2}
    assert len(json.dumps(L)) < 1600
    assert not L["target_word_counts_or_population_balance_assumed"]
    assert not L["arbitrary_coherent_fibre_algorithms_excluded"]
    assert not L["endpoint_linear_bypass_excluded"]


def test_exhaustive_control_preserves_unsupported_and_nonzero_failure():
    report = json.loads(A.REPORT.read_text())
    controls = report["bounded_filter_controls"]
    assert any(c["status"] == "NONFREE_RANK_UNSUPPORTED_NOT_NO_SOLUTIONS" for c in controls)
    for c in controls:
        if c["status"].startswith("NONFREE"):
            assert not c["target_failure_or_general_no_go_inferred"]
        else:
            assert c["complete_native_memberships_checked"] == c["public_family"]["cohorts"]*3**c["public_family"]["sites"]
            for row in c["all_target_filter_laws"]:
                assert Fraction(row["raw_filter_acceptance"])+Fraction(row["complete_failure_probability"]) == 1
    assert not report["general_quantum_fibre_lower_bound_proved"]


def test_exhaustive_coordinate_preflight_refuses_large_replay():
    with pytest.raises(ValueError, match="finite cap"):
        A.finite_control(1, 4, 1, 3, 90011)


def test_independent_checker_replays_all_integer_coordinates():
    checker = A.ROOT/"research/certificates/native_affine_fibre_crosscheck.js"
    p = subprocess.run(["node", str(checker)], capture_output=True, text=True)
    assert p.returncode == 0, p.stderr


@pytest.mark.parametrize("mutation", ("inverse", "membership", "failure", "exponent", "scope", "endpoint", "carry", "nonfree"))
def test_independent_checker_rejects_forged_relaxation_or_endpoint_claims(mutation, tmp_path):
    p = json.loads(A.REPORT.read_text()); c = p["bounded_filter_controls"][0]
    if mutation == "inverse": c["public_affine_recipes"][0]["pivot_minor_inverse"][0][0] = 0
    if mutation == "membership": c["accepted_word_receipts"][0]["word"][0] = (c["accepted_word_receipts"][0]["word"][0]+1) % 3
    if mutation == "failure": c["all_target_filter_laws"][0]["complete_failure_probability"] = "0"
    if mutation == "exponent": p["growing_relaxation_ledgers"][0]["per_target_filter_acceptance_upper"]["negative_exponent"] = 0
    if mutation == "scope": p["general_quantum_fibre_lower_bound_proved"] = True
    if mutation == "endpoint": p["actual_F3_endpoint_countercontrol"]["actual_original_data_reconstruction"]["original_secret"][0] = 1
    if mutation == "carry": p["selector_linearization_checks"][1]["native_selector_is_an_F3_affine_line_for_arbitrary_public_pairs"] = True
    if mutation == "nonfree": p["bounded_filter_controls"][2]["target_failure_or_general_no_go_inferred"] = True
    target = tmp_path/"forged.json"; target.write_text(json.dumps(p))
    checker = A.ROOT/"research/certificates/native_affine_fibre_crosscheck.js"
    result = subprocess.run(["node", str(checker), str(target)], capture_output=True, text=True)
    assert result.returncode != 0, mutation

from fractions import Fraction as Q
from itertools import combinations, product
import json

import pytest
from flint import nmod_mat

from theorems import nonlinear_residual_lift as f


@pytest.fixture
def chain():
    return f.Chain(7, 2, tuple(range(1, 7)), (1, 2, 4, 1, 3))


def test_square_is_convolution_not_pointwise_coefficient_square():
    assert f.square((1, 2, 3), 7) == (1, 4, 3, 5, 2)


def test_lift_identity_for_every_original_polynomial(chain):
    matrix = nmod_mat([chain.row(i) for i in range(chain.M)], chain.p)
    for c in product(range(chain.p), repeat=chain.n):
        q = f.square(c, chain.p)
        linear = matrix*nmod_mat([[v] for v in c+q], chain.p)
        r = f.residuals(chain, c)
        assert r == tuple(int(linear[i, 0]) for i in range(chain.M))
        values = [f.evaluate(c, x, chain.p) for x in chain.points]
        assert r == tuple((values[i+1]+a*values[i]**2) % chain.p
                          for i, a in enumerate(chain.multipliers))


def test_arbitrary_evaluation_order_is_not_silently_a_translation():
    chain = f.Chain(11, 2, (3, 8, 1, 10, 2, 6, 5), (1, 2, 4, 1, 3, 7))
    c = (4, 2)
    r = f.residuals(chain, c)
    translated = tuple((f.evaluate(c, x+1, 11)+a*f.evaluate(c, x, 11)**2) % 11
                       for x, a in zip(chain.points, chain.multipliers))
    assert r != translated
    result = f.classify_residual(chain, tuple(range(5)), r)
    assert result["status"] == "VERIFIED_ORIGINAL_POLYNOMIAL"
    assert result["coefficients"] == list(c)


def test_every_native_residual_is_recovered_without_coefficients_supplied(chain):
    for c in product(range(chain.p), repeat=chain.n):
        decoded = f.classify_residual(chain, tuple(range(chain.dimension)), f.residuals(chain, c))
        assert decoded["status"] == "VERIFIED_ORIGINAL_POLYNOMIAL"
        assert decoded["coefficients"] == list(c)
        assert not decoded["no_alternative_original_polynomial"]


@pytest.mark.parametrize("q", [(1, 0, 0), (4, 4, 1), (0, 1, 2)])
def test_invalid_square_or_square_of_wrong_polynomial_is_not_a_witness(chain, q):
    c = (1, 1)
    assert q != f.square(c, chain.p)
    decoded = f.classify_residual(chain, tuple(range(5)), f.residuals(chain, c, q))
    assert decoded["status"] == "OUTSIDE_ORIGINAL_IMAGE"
    assert decoded["no_alternative_original_polynomial"]
    assert decoded["whole_residual_mismatch_edges"] == []


def test_whole_residual_replay_checks_more_than_basis_rows():
    chain = f.Chain(11, 2, (3, 8, 1, 10, 2, 6, 5), (1, 2, 4, 1, 3, 7))
    r = list(f.residuals(chain, (2, 3)))
    r[-1] = (r[-1]+1) % 11
    result = f.classify_residual(chain, tuple(range(5)), r)
    assert result["status"] == "OUTSIDE_LINEAR_LIFT"
    assert result["whole_residual_mismatch_edges"] == [5]


def test_small_complete_lift_image_and_acceptance_count():
    result = f.exhaustive_control()
    assert result["lifted_residuals_enumerated"] == 7**5
    assert result["native_polynomials"] == 7**2
    assert Q(result["uniform_lift_acceptance"]) == Q(1, 7**3)
    assert result["accepted_exactly_original_image"]


def test_rank_deficient_structure_is_not_a_false_infeasibility_certificate():
    result = f.constant_multiplier_collision_control()
    assert result["lift_rank"] == 3 < result["nominal_lift_dimension"]
    chain = f.Chain(7, 2, tuple(range(1, 7)), (1,)*5)
    invalid = result["invalid_lift_with_same_feasible_residual"]
    assert any(f.square_defect(chain, invalid["P"], invalid["Q"]))
    assert f.residuals(chain, invalid["P"], invalid["Q"]) == f.residuals(chain, (0, 0))
    with pytest.raises(ValueError, match="singular"):
        f.classify_residual(chain, tuple(range(5)), (0,)*5)


def test_uniform_halfset_ensemble_identity_by_actual_all_input_enumeration():
    chain = f.Chain(5, 1, (1, 2, 3, 4), (1, 2, 3))
    count = lifted_total = original_total = square_consistent = tail = 0
    for allowed in product(tuple(combinations(range(5), 2)), repeat=3):
        for r0, r1 in product(allowed[0], allowed[1]):
            # Independent inverse of [1 1; 1 2], not the producer's solver.
            c, q = ((2*r0-r1) % 5,), ((r1-r0) % 5,)
            lifted = f.residuals(chain, c, q)
            original = f.residuals(chain, c)
            score = sum(v in row for v, row in zip(lifted, allowed))
            lifted_total += score
            original_total += sum(v in row for v, row in zip(original, allowed))
            square_consistent += q == f.square(c, 5)
            tail += score >= 3
            count += 1
    contract = f.uniform_ensemble_contract(chain, (0, 1), 3)
    assert count == 4000
    assert Q(lifted_total, count) == Q(contract["relaxed_mean_exact"]) == Q(12, 5)
    assert Q(original_total, count) == Q(contract["projected_original_mean_exact"]) == Q(6, 5)
    assert Q(square_consistent, count) == Q(contract["square_consistency_probability_exact"])
    assert Q(contract["relaxed_tail_lower"]) <= Q(tail, count) == Q(2, 5)
    assert not contract["full_original_score_law_identified"]
    assert not contract["bound_on_optimized_or_correlated_lift_search"]


def test_full_relaxed_score_does_not_accept_an_infeasible_witness(chain):
    allowed = [(0, 1, 2)]*chain.M
    row = f.forced_relaxation(chain, allowed, tuple(range(5)), seed=48211)
    assert row["relaxed_score_NOT_a_witness"] == chain.M
    assert row["all_forced_edges_replayed"]
    assert not row["exact_original_image_membership"]
    assert row["square_defect_nonzero_coefficients"] > 0
    assert row["complete_work"]["rerolls"] == 0
    c = row["coefficients"]
    assert row["original_polynomial_score"] == sum(v in a for v, a in zip(f.residuals(chain, c), allowed))


@pytest.mark.parametrize("operation", [
    lambda: f.Chain(9, 2, (1, 2, 3), (1, 1)),
    lambda: f.Chain(7, 0, (1, 2), (1,)),
    lambda: f.Chain(7, 1, (1, 1), (1,)),
    lambda: f.Chain(7, 1, (0, 1), (1,)),
    lambda: f.Chain(7, 1, (1, 2), (0,)),
    lambda: f.square((1, True), 7),
    lambda: f.square((), 7),
])
def test_invalid_algebra_inputs_fail_closed(operation):
    with pytest.raises(ValueError):
        operation()


def test_bad_basis_and_bad_sets_fail_closed(chain):
    with pytest.raises(ValueError, match="distinct-edge"):
        f.checked_basis(chain, (0, 1, 2, 3, 3))
    with pytest.raises(ValueError):
        f.checked_basis(chain, (0, 1, 2, 3, 6))
    with pytest.raises(ValueError, match="distinct"):
        f.forced_relaxation(chain, [(0, 0, 1)]*chain.M, tuple(range(5)))
    with pytest.raises(ValueError, match="canonical"):
        f.classify_residual(chain, tuple(range(5)), (0, 1, 2, 3, 7))


def test_native_residual_span_is_full_lift_span_in_odd_characteristic(chain):
    native = [list(f.residuals(chain, c)) for c in product(range(chain.p), repeat=chain.n)]
    assert nmod_mat(native, chain.p).rank() == chain.dimension


def test_reference_index_is_pinned_not_just_self_checksumming(tmp_path):
    index = tmp_path / "index.json"
    index.write_text("{}")
    (tmp_path / "SHA256SUMS").write_text(f"{f.sha256(index)}  index.json\n")
    with pytest.raises(ValueError, match="checksum"):
        f.load_reference(tmp_path)


def test_saved_native_relaxation_and_frozen_880_witness_inventory():
    report = json.loads(f.REPORT.read_text())
    native = report["native"]
    chain = f.Chain(native["p"], native["n"], tuple(native["points"]), tuple(native["multipliers"]))
    row = native["attack"]
    assert f.checked_basis(chain, row["basis_edges"]).rank() == 614
    assert list(f.residuals(chain, row["coefficients"], row["lifted_square"])) == row["relaxed_residuals"]
    assert list(f.residuals(chain, row["coefficients"])) == row["original_residuals"]
    assert list(f.square_defect(chain, row["coefficients"], row["lifted_square"])) == row["square_defect"]
    assert sum(v != 0 for v in row["square_defect"]) == 409
    assert not row["exact_original_image_membership"]
    assert not report["quantum_speedup_established"]
    assert not report["general_classical_hardness_established"]
    assert native["provenance"]["index_sha256"] == f.REFERENCE_INDEX_SHA256
    assert native["provenance"]["original_batches_available"] == 116
    assert not native["provenance"]["all_original_witnesses_verified_by_this_pass"]

    inventory = native["frozen_witness_and_attack_inventory"]
    assert inventory["all_880_final_witnesses_independently_verified"]
    assert inventory["witnesses_verified"] == 880
    assert inventory["instances_verified"] == 20
    assert inventory["available_raw_batches"] == 116
    assert inventory["expected_raw_batches"] == 120
    assert not inventory["complete_raw_archive"]
    assert not inventory["missing_raw_batches_rerun_or_invented"]
    assert inventory["recovery_provenance_counts"] == {
        "authenticated_accepted_campaign": 800,
        "earlier_attempt_matching_final_table_witness_only": 80,
    }
    assert inventory["full_table_access_and_preprocessing_charged"]
    assert not inventory["folded_oracle_lower_bound_applies_to_public_scalar_tables"]
    assert inventory["overall_best_witness"]["score"] == 1252
    assert inventory["overall_best_witness"]["method"] == "warm-relax-project-from-moving"
    assert inventory["primary_instance_best_witness"]["score"] == 1252
    assert len(inventory["classical_attack_inventory"]) == 22
    assert all(m["runs_verified"] == 40 and m["full_table_access_required"]
               and not m["folded_oracle_lower_bound_applies"]
               for m in inventory["classical_attack_inventory"])

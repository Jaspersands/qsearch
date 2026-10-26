from fractions import Fraction as Q
import hashlib
import itertools
import json
from pathlib import Path

import pytest

from theorems import integer_character_babai as babai
from theorems import integer_character_feedback as feedback
from theorems import integer_character_interpolation as integer
from theorems import integer_character_near_vector as near
from theorems import integer_character_uniform as uniform
from theorems.native_rlwe_primal_babai import exact_row_profile


def independent_completion(rows, target, incumbent, full_plane, offset):
    profile = exact_row_profile(rows)
    mu, gs = profile["mu"], profile["gs_squared"]
    inner = []
    for i, row in enumerate(rows):
        inner.append(sum(x*y for x, y in zip(row, target))
                     - sum(mu[i][j]*inner[j] for j in range(i)))
    coordinates = [v/g for v, g in zip(inner, gs)]
    coefficients = [0]*len(rows)
    for i in range(len(rows)-1, -1, -1):
        if i > full_plane:
            coefficients[i] = incumbent[i]
        else:
            x = coordinates[i]
            coefficients[i] = (2*x.numerator+x.denominator)//(2*x.denominator)
            if i == full_plane:
                coefficients[i] += offset
        for j in range(i):
            coordinates[j] -= coefficients[i]*mu[i][j]
    return coefficients


@pytest.mark.parametrize("order", [21, 2*3**50])
@pytest.mark.parametrize("coordinate_prefix", [False, True])
def test_forced_tail_completion_matches_independent_full_fraction_reference(order, coordinate_prefix):
    labels = [1, 5, 3, 7]
    _, rows = near.lattice_bases(labels, order)
    if coordinate_prefix:
        rows = [[-x for x in rows[3]], rows[1], rows[0], rows[2]]
    target = [order//3, order//7, order//2, order-1]
    exact = babai.exact_normalized_babai(rows, labels, order, target)
    incumbent = list(exact["basis_coefficients"])
    incumbent[-1] += 3
    rank = exact["orthogonal_integer_prefix_rank"]
    for plane in range(exact["exact_core_dimension"]):
        for offset in [-2, 0, 2]:
            actual = feedback.complete_tail(rows, order, target, exact, incumbent, plane, offset)
            expected = independent_completion(rows, target, incumbent, rank+plane, offset)
            assert actual == expected
            evaluated = feedback.evaluate(rows, labels, order, target, actual)
            assert evaluated["mean_square"] <= evaluated["raw_mean_square"]


def test_feedback_really_changes_later_candidate_generation_when_only_prefix_changes():
    labels, order = [1, 5, 3, 7], 21
    _, base = near.lattice_bases(labels, order)
    rows = [base[3], base[1], base[0], base[2]]
    later_pools, blind_pools = [], []
    for c1, c3 in itertools.product([0, 7, 20], repeat=2):
        target = [4, c1, 6, c3]
        exact = babai.exact_normalized_babai(rows, labels, order, target)
        blind = babai.bounded_last_plane_search(rows, labels, order, target, exact, radius=2)
        blind_pools.append(tuple(t["assignment_decimal"] for t in blind["trials"]))
        result = feedback.feedback_search(rows, labels, order, target, exact,
                                          exact["basis_coefficients"], [1, 0], radius=2)
        later_pools.append(tuple(t["assignment_decimal"] for t in result["trials"] if t["step"] == 1))
        for trial in result["trials"]:
            witness = near.witness(labels, target, order, int(trial["assignment_decimal"]))
            assert str(witness["mean_square"]) == trial["mean_square"]
        assert all(Q(h["after_mean_square"]) <= Q(h["before_mean_square"]) for h in result["history"])
    assert len(set(blind_pools)) == 1
    assert len(set(later_pools)) > 1


def test_repeated_planes_retain_incumbent_and_charge_every_proposal():
    labels, order = [1, 5, 3, 7], 21
    _, rows = near.lattice_bases(labels, order)
    target = [4, 20, 6, 7]
    exact = babai.exact_normalized_babai(rows, labels, order, target)
    result = feedback.feedback_search(rows, labels, order, target, exact,
                                      exact["basis_coefficients"], [3, 2, 3, 2], radius=2)
    assert result["proposal_count"] == 20
    assert result["score_evaluations_including_initial"] == 21
    assert all(Q(h["after_mean_square"]) <= Q(h["before_mean_square"]) for h in result["history"])
    assert result["candidate_generation_uses_full_target_feedback"]
    assert result["visited_candidates_are_not_a_target_blind_pool"]
    assert not result["asymptotic_dequantization_claimed"]
    assert not result["global_optimum_or_convergence_claimed"]


def test_multilevel_beam_search_monotonicity_and_validation():
    labels, order = [1, 5, 3, 7], 21
    _, rows = near.lattice_bases(labels, order)
    target = [4, 20, 6, 7]
    exact = babai.exact_normalized_babai(rows, labels, order, target)
    branch = babai.bounded_last_plane_search(rows, labels, order, target, exact, radius=2)
    seeds = [
        babai._round_profile(
            rows, order, target, exact["normalized_gram_pivots"],
            exact["rounding_profile"]["upper_rows"], exact["rounding_profile"]["prefix"],
            int(tr["offset"]),
        )[0]
        for tr in branch["trials"][:3]
    ]
    beam = feedback.multilevel_beam_search(rows, labels, order, target, exact,
                                           seeds, [2, 1], beam_width=2, radius=1)
    assert beam["beam_width"] == 2
    assert all(Q(h["after_best_mean_square"]) <= Q(h["before_best_mean_square"])
               for h in beam["level_history"])
    assert Q(beam["best"]["mean_square"]) <= Q(beam["initial_best_mean_square"])
    with pytest.raises(ValueError):
        feedback.multilevel_beam_search(rows, labels, order, target, exact, [], [1], beam_width=2)


def test_invalid_plane_offset_and_coefficients_fail_closed():
    labels, order = [1, 5], 18
    _, rows = near.lattice_bases(labels, order)
    target = [4, 5]
    exact = babai.exact_normalized_babai(rows, labels, order, target)
    for plane, offset in [(-1, 0), (2, 0), (0, .5), (True, 0)]:
        with pytest.raises(ValueError):
            feedback.complete_tail(rows, order, target, exact, exact["basis_coefficients"], plane, offset)
    with pytest.raises(ValueError):
        feedback.evaluate(rows, labels, order, target, [0])
    with pytest.raises(ValueError):
        feedback.feedback_search(rows, labels, order, target, exact, [0, 0], [1], radius=-1)


def test_native_all_coordinate_witness_and_trace_replay():
    saved = json.loads(feedback.REPORT.read_text())
    assert saved["schema"] == "integer_character_feedback_v2"
    assert saved["producer_sha256"] == hashlib.sha256(Path(feedback.__file__).read_bytes()).hexdigest()
    assert saved["babai_artifact_sha256"] == hashlib.sha256(babai.REPORT.read_bytes()).hexdigest()
    input_bytes = near.REPORT.read_bytes()
    assert saved["input_artifact_sha256"] == hashlib.sha256(input_bytes).hexdigest()
    native = json.loads(input_bytes)["native"]
    labels, centers = list(map(int, native["public_labels_decimal"])), list(map(int, native["centers_decimal"]))
    order = int(native["cyclic_order_decimal"])
    basis_path = feedback.ROOT/saved["basis_artifact"]
    assert saved["basis_artifact_sha256"] == hashlib.sha256(basis_path.read_bytes()).hexdigest()
    search = saved["search"]
    assert search["core_plane_schedule"] == list(range(188, 164, -1))
    assert search["proposal_count"] == len(search["trials"]) == 216
    assert search["score_evaluations_including_initial"] == 217
    assert search["unique_proposed_assignments"] == 193
    assert len({t["assignment_decimal"] for t in search["trials"] if t["threshold_met"]}) == 6
    assert all(h["selected_offset"] is None for h in search["history"])
    current_mean = Q(search["initial_mean_square"])
    current_assignment = search["initial_assignment_decimal"]
    for step, record in enumerate(search["history"]):
        proposals = [t for t in search["trials"] if t["step"] == step]
        assert len(proposals) == 9
        assert all(t["parent_assignment_decimal"] == current_assignment for t in proposals)
        for trial in proposals:
            replay = near.witness(labels, centers, order, int(trial["assignment_decimal"]))
            assert str(replay["mean_square"]) == trial["mean_square"]
            assert replay["accepted"] == trial["threshold_met"]
        assert Q(record["before_mean_square"]) == current_mean
        expected_mean = min([current_mean]+[Q(t["mean_square"]) for t in proposals])
        assert Q(record["after_mean_square"]) == expected_mean
        current_mean, current_assignment = expected_mean, record["selected_assignment_decimal"]
        assert near.witness(labels, centers, order, int(current_assignment))["mean_square"] == current_mean
    best = search["best"]
    assert Q(best["mean_square"]) == current_mean <= Q(search["initial_mean_square"])
    assert best["assignment_decimal"] == current_assignment
    rows = babai.read_basis(basis_path)
    result = feedback.evaluate(rows, labels, order, centers, list(map(int, best["basis_coefficients_decimal"])))
    assert list(map(str, result["point"])) == best["basis_point_decimal"]
    assert list(map(str, result["canonical_point"])) == best["canonical_point_decimal"]
    assert str(result["mean_square"]) == best["mean_square"]
    assert str(result["raw_mean_square"]) == best["raw_mean_square"]
    assert result["threshold_met"] and not saved["classical_asymptotic_dequantization_proved"]

    beam = saved["multilevel_beam_search"]
    assert beam["beam_width"] == 4
    assert beam["core_plane_schedule"] == [188, 187, 186]
    assert beam["proposal_count"] == 60
    assert beam["distinct_threshold_witnesses_found"] >= 2
    assert Q(beam["best"]["mean_square"]) <= Q(beam["initial_best_mean_square"])
    beam_eval = feedback.evaluate(rows, labels, order, centers, list(map(int, beam["best"]["basis_coefficients_decimal"])))
    assert str(beam_eval["mean_square"]) == beam["best"]["mean_square"]

    scaling = saved["multi_length_j16_campaign"]
    assert scaling["lengths_tested"] == [32, 64, 96, 128]
    assert [r["read_fraction"] for r in scaling["records"]] == ["1", "1", "29/32", "45/64"]
    assert not scaling["asymptotic_dequantization_claimed"]
    assert all(
        cr["multilevel_beam_improved_over_last_plane"]
        for rec in scaling["records"] if rec["length"] in (96, 128)
        for cr in rec["center_runs"]
    )

    cosine = saved["cosine_family_924bit_attack_campaign"]
    assert cosine["interpolation_artifact_sha256"] == hashlib.sha256(integer.REPORT.read_bytes()).hexdigest()
    assert cosine["cyclic_order_bits"] == 924
    assert not cosine["int64_cast_used_on_labels_or_centers"]
    assert cosine["arb_interval_verifier_used"]
    assert not cosine["any_run_accepted_at_0_3"]
    interp_native = json.loads(integer.REPORT.read_text())["native"]
    c_labels = list(map(int, interp_native["public_labels_decimal"]))
    c_order = int(interp_native["cyclic_order_decimal"])
    import random
    for sr in cosine["seed_runs"]:
        rng = random.Random(sr["center_seed"])
        c_centers = [rng.randrange(c_order) for _ in range(len(c_labels))]
        best_m = next(m for m in sr["methods"] if m["name"] == sr["best_method"])
        ver = uniform.verify_score(c_labels, c_centers, c_order, int(best_m["assignment_decimal"]))
        assert ver == best_m["arb_score_verification"]
        assert Q(sr["best_score_lower"]) > Q(11, 100)

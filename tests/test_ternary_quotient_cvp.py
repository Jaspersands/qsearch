from fractions import Fraction
from itertools import product
import json
import subprocess

from flint import fmpz_mat
import pytest

from ternary_covariant_noise import CovariantRecord
from ternary_full_record_cvp import exact_repair_paths, public_repairs
from ternary_measured_lattice_decoder import compile_code_lattice
from ternary_quotient_cvp import (
    REPORT, beam_search, compile_quotient, conditional_point, decode_saved,
    systematic_projection_certificate, systematic_quotient_rows, target_coordinates,
)


def control():
    records = (CovariantRecord((1,), (1,), (2, 1), 3),
               CovariantRecord((1,), (1,), (0, 2), 3))
    model = compile_code_lattice(records)
    rows = ((0, 3, 0, 0), (0, 0, 3, 0), (0, 0, 0, 3), (1, 1, 1, 1))
    return records, model, rows


def test_exact_elimination_matches_bruteforce_over_all_dead_coefficients():
    records, model, rows = control()
    compiled = compile_quotient(model, rows)
    assert compiled["status"] == "EXACT_ORTHOGONAL_DEAD_ELIMINATION"
    live, dead = compiled["certificate"]["live_positions"], compiled["certificate"]["dead_positions"]
    assert len(live) == 1 and len(dead) == 3
    for target in product(range(3), repeat=4):
        for active in ((-1,), (0,), (2,)):
            optimal = conditional_point(compiled, target, active)
            for other in product(range(-2, 3), repeat=len(dead)):
                c = dict(zip(live, active)) | dict(zip(dead, other))
                point = tuple(sum(c[i]*row[j] for i, row in enumerate(rows)) for j in range(4))
                cost = sum((a-b)**2 for a, b in zip(target, point))
                assert optimal["supplied_Euclidean_cost"] <= cost


def test_code_zero_directions_do_not_license_elimination_when_coupled():
    records = (CovariantRecord((1,), (0,), (0, 0), 3),
               CovariantRecord((0,), (0,), (0, 0), 3))
    model = compile_code_lattice(records)
    rows = ((1, 0, 0, 0), (0, 3, 0, 0), (0, 3, 3, 0), (0, 0, 0, 3))
    compiled = compile_quotient(model, rows)
    assert compiled["status"] == "UNKNOWN_COUPLED_DEAD_DIRECTIONS"
    assert compiled["certificate"]["dead_dead_GS_edges"] == ((2, 1),)
    assert not beam_search(compiled, (0, 0, 0, 0))["CVP_optimality_certified"]
    with pytest.raises(ValueError):
        conditional_point(compiled, (0, 0, 0, 0), (0,))


def test_periodic_dead_cost_is_not_a_constant_or_discardable_penalty():
    records, model, rows = control()
    compiled = compile_quotient(model, rows)
    target = (1, 1, 1, 1)
    initial, profile = target_coordinates(compiled, target), compiled["profile"]
    live = compiled["certificate"]["live_positions"]
    periodic = []
    for a in range(3):
        path = conditional_point(compiled, target, (a,), initial)
        i = live[0]
        active_cost = Fraction(str(profile["gs_squared"][i]*(initial[i]-a)**2))
        periodic.append(Fraction(path["supplied_Euclidean_cost"])-active_cost)
    assert len(set(periodic)) > 1


def test_discarding_periodic_term_changes_the_actual_optimal_secret_class():
    _, model, rows = control()
    compiled = compile_quotient(model, rows)
    target = (0, 1, 1, 1)
    assert target_coordinates(compiled, target)[-1] == 0
    naive = conditional_point(compiled, target, (0,))
    better = conditional_point(compiled, target, (1,))
    assert naive["candidate"] == (0,) and naive["supplied_Euclidean_cost"] == 3
    assert better["candidate"] == (1,) and better["supplied_Euclidean_cost"] == 1


def test_single_state_zero_radius_exactly_matches_original_babai():
    records, model, rows = control()
    target = tuple(x for r in records for x in r.outcome)
    compiled = compile_quotient(model, rows)
    beam = beam_search(compiled, target, width=1, radius=0)
    old = next(exact_repair_paths(rows, target, public_repairs(4, 0, 0)))
    assert beam["candidates"][0]["point"] == old["point"]
    assert not beam["CVP_optimality_certified"]
    assert beam["stages"][-1]["best_exact_partial_cost"] == str(beam["candidates"][0]["supplied_Euclidean_cost"])


def test_beam_score_at_finish_is_exact_full_original_distance_and_reproducible():
    records, model, rows = control()
    compiled = compile_quotient(model, rows)
    target = tuple(x for r in records for x in r.outcome)
    beam = beam_search(compiled, target, width=4, radius=2)
    assert beam == beam_search(compiled, target, width=4, radius=2)
    assert len(beam["candidates"]) == 4
    assert len({tuple(x["active_coefficients"]) for x in beam["candidates"]}) == 4
    assert all(path["supplied_Euclidean_cost"] == sum((a-b)**2 for a, b in zip(path["point"], target))
               for path in beam["candidates"])
    assert not beam["complete_integer_coefficient_enumeration"]


def test_noiseless_arithmetic_control_and_inherited_proposals_are_accounted():
    records = (CovariantRecord((1,), (0,), (2, 0), 3),
               CovariantRecord((1,), (1,), (2, 2), 3))
    model = compile_code_lattice(records)
    rows = tuple(tuple(map(int, row)) for row in fmpz_mat(model["lattice_rows"]).lll(gram="exact").tolist())
    result = decode_saved(model, rows, records, ((0,), (1,)), inherited_lll_calls=3)
    assert result["selections"]["Euclidean"] == (2,)
    assert result["selections"]["native_likelihood"] == (2,)
    assert result["cost"]["new_LLL_calls"] == 0
    assert result["cost"]["inherited_LLL_calls"] == 3
    assert result["inherited_candidates"] == ((0,), (1,))
    assert not result["hidden_secret_or_validation_supplied_to_optimizer"]


@pytest.mark.parametrize("values", ((1, 2), (True,), (1.5,)))
def test_conditional_optimizer_rejects_bad_active_coefficients(values):
    _, model, rows = control()
    with pytest.raises(ValueError):
        conditional_point(compile_quotient(model, rows), (0, 0, 0, 0), values)


def test_saved_basis_cannot_be_applied_to_other_labels_or_improper_sublattice():
    records, model, rows = control()
    other = (CovariantRecord((2,), (0,), (2, 1), 3), records[1])
    with pytest.raises(ValueError):
        decode_saved(model, rows, other)
    with pytest.raises(ValueError):
        compile_quotient(model, tuple(tuple(2*x for x in row) for row in rows))


def test_identical_labels_do_not_license_reusing_a_basis_from_a_different_root():
    records, model, rows = control()
    changed = tuple(CovariantRecord(r.first, r.second, r.outcome, 9) for r in records)
    with pytest.raises(ValueError, match="identical full-root"):
        decode_saved(model, rows, changed)


@pytest.mark.parametrize("q", (3, 9, 3**80))
def test_systematic_basis_already_has_n_live_unknowns_and_same_canonical_cost(q):
    records = (CovariantRecord((1, 0), (0, 1), (2, 1), q),
               CovariantRecord((1, 1), (2, 1), (1, 0), q))
    model = compile_code_lattice(records)
    compiled = compile_quotient(model, systematic_quotient_rows(model))
    assert compiled["certificate"]["live_positions"] == (2, 3)
    assert compiled["certificate"]["dead_positions"] == (0, 1)
    assert compiled["profile"]["gs_squared"][-2:] == [1, 1]
    assert 2 not in compiled["profile"]["mu"][3]
    critique = systematic_projection_certificate(model)
    assert critique["complete_mod_q_secret_classes"] == q**2
    assert not critique["systematic_projection_is_new_algorithmic_dimension_reduction"]
    target = tuple(x for record in records for x in record.outcome)
    for secret in ((0, 0), (1, 2), (q-1, q-2)):
        active = tuple(target[i]-((target[i]-s+q//2) % q-q//2) for i, s in enumerate(secret))
        path = conditional_point(compiled, target, active)
        assert path["candidate"] == secret
        canonical = sum(((e+q//2) % q-q//2)**2 for record in records for e in record.residual(secret))
        assert path["supplied_Euclidean_cost"] == canonical


def test_independent_exact_live_replay_checks_entire_search_not_just_final_points():
    checker = REPORT.parents[1]/"certificates/ternary_quotient_cvp_crosscheck.js"
    result = subprocess.run(["node", str(checker)], capture_output=True, text=True, check=True)
    replay = json.loads(result.stdout)
    assert replay["status"] == "PASS" and replay["full_cohorts"] == 8
    assert replay["largest_original_dimension"] == 1024
    assert replay["exact_eliminated_directions"] == 2460
    assert replay["independently_replayed_beam_expansions"] == 28992
    assert replay["conditional_minimizers"] == 256
    assert replay["exact_9_over_8_counterexamples"] == 4
    assert replay["improved_training_Euclidean_cost"] == 5
    assert replay["recoveries"] == {"Euclidean": 2, "native_likelihood": 2}
    assert not replay["near_exact_CVP_guarantee"]


@pytest.mark.parametrize("mutation", ("pruning", "dead_coupling", "reused_validation"))
def test_checker_rejects_false_search_and_source_certificates(tmp_path, mutation):
    report = json.loads(REPORT.read_text())
    control = report["controls"][0]
    if mutation == "pruning":
        control["decoder"]["search"]["stages"][0]["best_exact_partial_cost"] = "-1"
    elif mutation == "dead_coupling":
        control["decoder"]["certificate"]["dead_dead_GS_edges"].append([1, 0])
    else:
        control["old_heldout_records_used_by_optimizer_or_validator"] = True
    file = tmp_path/"false.json"
    file.write_text(json.dumps(report))
    checker = REPORT.parents[1]/"certificates/ternary_quotient_cvp_crosscheck.js"
    assert subprocess.run(["node", str(checker), str(file)], capture_output=True).returncode != 0

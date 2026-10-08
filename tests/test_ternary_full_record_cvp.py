from fractions import Fraction
from itertools import product
import json
import random
import subprocess

from flint import fmpz_mat
import pytest

from native_rlwe_primal_babai import exact_row_profile, nearest_plane
from ternary_covariant_noise import CovariantRecord
from ternary_full_record_cvp import (
    REPORT, attach_comparison_certificate, bdd_gate, compact_model, decode, embedding_proposals, exact_repair_paths,
    exact_sparse_profile, public_repairs, rounding_influence,
)
from ternary_measured_lattice_decoder import compile_code_lattice, code_point_to_secret


def honest(q=9):
    secret = (2, 4)
    rows = (((1, 0), (0, 1)), ((1, 1), (2, 1)), ((3, 4), (4, 5)))
    return tuple(CovariantRecord(tuple(x % q for x in a), tuple(x % q for x in c),
                                tuple(sum(x*s for x, s in zip(row, secret)) % q for row in (a, c)), q)
                 for a, c in rows), tuple(x % q for x in secret)


@pytest.mark.parametrize("rank", (2, 4, 8))
def test_exact_sparse_ldl_matches_every_dense_fraction_free_coefficient(rank):
    rng = random.Random(98700+rank)
    rows = [[rng.randrange(-7, 8) for _ in range(rank)] for _ in range(rank)]
    rows = tuple(tuple(row)+tuple(int(i == j) for j in range(rank)) for i, row in enumerate(rows))
    sparse, dense = exact_sparse_profile(rows), exact_row_profile(rows)
    assert sparse["gram_determinant"] == dense["leading_gram_determinants"][-1]
    for i in range(rank):
        assert Fraction(str(sparse["gs_squared"][i])) == dense["gs_squared"][i]
        for j in range(i):
            assert Fraction(str(sparse["mu"][i].get(j, 0))) == dense["mu"][i][j]


def test_exact_full_babai_and_public_multi_repairs_match_integer_lattice_points():
    records, _ = honest()
    model = compile_code_lattice(records)
    rows = tuple(tuple(map(int, row)) for row in fmpz_mat(model["lattice_rows"]).lll(gram="exact").tolist())
    target = tuple(x for r in records for x in r.outcome)
    paths = tuple(exact_repair_paths(rows, target, public_repairs(6, 12, 981)))
    assert paths[0]["point"] == tuple(nearest_plane(rows, target)["point"])
    assert len(paths) == 13
    for p in paths:
        assert p["point"] == tuple(sum(x*row[j] for x, row in zip(p["coefficients"], rows)) for j in range(6))
        assert len(code_point_to_secret(model, p["point"])) == 2


def test_public_repair_menu_is_exact_reproducible_and_not_full_enumeration():
    paths = public_repairs(32, 32, 103)
    assert paths == public_repairs(32, 32, 103)
    assert paths[0] == (0,)*32
    assert all(1 <= sum(bool(x) for x in row) <= 4 for row in paths[1:])


@pytest.mark.parametrize("q", (9, 3**32))
def test_full_cohort_noiseless_arithmetic_control_recovers_without_grid_search(q):
    records, secret = honest(q)
    result = decode(records, ("a", "b", "c"), repair_count=8, seed=35)
    assert result["selections"]["Euclidean"] == secret
    assert result["selections"]["native_likelihood"] == secret
    assert result["cost"]["original_measured_qutrits"] == 3
    assert not result["cost"]["secret_or_root_value_enumeration"]
    assert not result["near_exact_CVP_guarantee"] and not result["Gaussian_error_promise"]


def test_every_embedding_row_has_accounted_modular_extraction_or_nonunit_reason():
    records, _ = honest()
    model = compile_code_lattice(records)
    target = tuple(x for r in records for x in r.outcome)
    run = embedding_proposals(model, target, 2)
    assert len(run["candidates"])+len(run["rejected_rows"]) == 7
    for c in run["candidates"]:
        base = code_point_to_secret(model, c["code_lattice_point"])
        assert c["candidate"] == tuple(-pow(c["target_coefficient"], -1, 9)*x % 9 for x in base)
        assert c["literal_CVP_error_vector"] == (abs(c["target_coefficient"]) == 1)


def test_plain_code_lattice_selection_reads_labels_not_outcomes():
    records, _ = honest()
    changed = tuple(CovariantRecord(r.first, r.second, ((r.outcome[0]+1) % 9, (r.outcome[1]+2) % 9), 9) for r in records)
    assert compile_code_lattice(records) == compile_code_lattice(changed)
    assert compact_model(compile_code_lattice(records)) == compact_model(compile_code_lattice(changed))


def test_bdd_gate_is_scoped_and_does_not_supply_gaussian_or_approximation_promise():
    records, _ = honest()
    gate = bdd_gate(records*20)
    assert gate["shortest_lattice_vector_length_upper"] == 9
    assert gate["true_secret_BDD_squared_distance_necessary_upper"] == "81/4"
    assert gate["BDD_promise_probability_upper_diagnostic"] < 1
    assert not gate["Gaussian_or_BDD_source_promise_granted"]
    assert not gate["general_CVP_or_quantum_receiver_impossibility"]


def test_whole_caps_and_rank_failure_do_not_run_partial_full_record_optimizer():
    records, _ = honest()
    result = decode(records, ("a", "b", "c"), max_equations=5)
    assert result["status"] == "WHOLE_LATTICE_CAP_EXHAUSTED"
    assert not result["partial_cohort_or_decoder_used"]
    singular = (CovariantRecord((0, 0), (0, 0), (0, 0), 9),)*3
    result = decode(singular, ("a", "b", "c"))
    assert result["status"] == "UNKNOWN_NO_UNIT_ROW_BASIS" and not result["selections"]


@pytest.mark.parametrize("rows", ((), ((0, 0),), ((1,), (1, 2))))
def test_bad_or_singular_sparse_profiles_rejected(rows):
    with pytest.raises(ValueError):
        exact_sparse_profile(rows)


def test_dead_only_repairs_preserve_secret_for_every_small_target():
    records = (CovariantRecord((1,), (0,), (0, 0), 3), CovariantRecord((0,), (0,), (0, 0), 3))
    model = compile_code_lattice(records)
    rows = model["lattice_rows"]
    influence = rounding_influence(model, rows)
    assert influence["influential_rounding_positions"] == (0,)
    assert influence["dead_rounding_positions"] == (1, 2, 3)
    profile = exact_sparse_profile(rows)
    for target in product(range(3), repeat=4):
        repairs = ((0, 0, 0, 0), (0, 1, -1, 1), (0, -1, 1, -1))
        secrets = tuple(code_point_to_secret(model, p["point"])
                        for p in exact_repair_paths(rows, target, repairs, profile))
        assert len(set(secrets)) == 1


def test_zero_code_row_cannot_be_pruned_when_feedforward_reaches_a_live_row():
    model = compile_code_lattice((CovariantRecord((1,), (0,), (0, 0), 3),))
    rows = ((1, 3), (3, 12))
    assert code_point_to_secret(model, rows[1]) == (0,)
    influence = rounding_influence(model, rows)
    assert influence["influential_rounding_positions"] == (0, 1)
    paths = tuple(exact_repair_paths(rows, (0, 0), ((0, 0), (0, 1))))
    assert code_point_to_secret(model, paths[0]["point"]) != code_point_to_secret(model, paths[1]["point"])


def test_compiled_live_menu_does_not_claim_that_every_repair_changes_secret():
    paths = public_repairs(12, 20, 93, positions=(1, 3, 8))
    assert all(not x or j in (1, 3, 8) for row in paths for j, x in enumerate(row))
    with pytest.raises(ValueError):
        public_repairs(12, 3, 4, positions=(3, 3))


def test_valid_public_comparison_witness_falsifies_factor_without_assuming_optimality():
    records, secret = honest()
    control = {"training_records": [r.public() for r in records], "calibration_secret": secret,
               "modulus": 9, "decoder": decode(records, ("a", "b", "c"), repair_count=0)}
    certificate = attach_comparison_certificate(control)["CVP_comparison_certificate"]
    assert certificate["valid_point_squared_distance"] == 0
    assert not certificate["norm_9_over_8_approximation_falsified_on_this_instance"]
    assert not certificate["globally_nearest_point_or_true_secret_optimality_assumed"]
    assert not certificate["comparison_truth_supplied_to_decoder"]


def test_live_independent_replay_covers_full_dimensions_and_exact_factor_failures():
    checker = REPORT.parents[1]/"certificates/ternary_full_record_cvp_crosscheck.js"
    result = subprocess.run(["node", str(checker)], capture_output=True, text=True, check=True)
    replay = json.loads(result.stdout)
    assert replay["status"] == "PASS" and replay["largest_lattice_dimension"] == 1024
    assert replay["exact_repair_paths"] == 264 and replay["exact_unimodular_reductions"] == 24
    assert replay["exact_9_over_8_counterexamples"] == 5
    assert not replay["near_exact_CVP_guarantee"]


@pytest.mark.parametrize("mutation", ("dead_rounding", "CVP_factor"))
def test_independent_checker_rejects_false_quotient_and_approximation_certificates(tmp_path, mutation):
    report = json.loads(REPORT.read_text())
    control = report["controls"][0]
    if mutation == "dead_rounding":
        influence = control["decoder"]["rounding_influence_certificate"]
        influence["dead_rounding_positions"].append(influence["influential_rounding_positions"][0])
    else:
        control["CVP_comparison_certificate"]["strict_integer_factor_failure_margin"] = 1
    file = tmp_path/"false.json"
    file.write_text(json.dumps(report))
    checker = REPORT.parents[1]/"certificates/ternary_full_record_cvp_crosscheck.js"
    assert subprocess.run(["node", str(checker), str(file)], capture_output=True).returncode != 0

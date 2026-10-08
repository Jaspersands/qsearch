import json
from itertools import product
import subprocess

from flint import fmpz_mat
import pytest

from ternary_covariant_noise import CovariantRecord, heldout_score
from ternary_measured_lattice_decoder import (
    REPORT, calibration, compile_lattice, decode, exact_json, metric_countercontrol,
    native_loss, paired_embed, paired_unembed, point_to_secret, public_subset_schedule,
    reduce_basis, verify_fresh,
)


def honest(q=9):
    secret = (2, 4)
    pairs = (((1, 0), (0, 1)), ((1, 1), (2, 1)), ((3, 4), (4, 5)))
    records = tuple(CovariantRecord(tuple(x % q for x in a), tuple(x % q for x in c),
                      tuple(sum(x*s for x, s in zip(v, secret)) % q for v in (a, c)), q)
                    for a, c in pairs)
    return records, tuple(x % q for x in secret)


@pytest.mark.parametrize("q", (3, 9, 81, 3**64))
def test_whole_code_lattice_and_correlation_metric_have_exact_indices(q):
    records, secret = honest(q)
    model = compile_lattice(records)
    assert model["status"] == "EXACT_PUBLIC_PAIRED_CODE_LATTICE"
    assert model["lattice_index"] == q**4
    assert abs(int(fmpz_mat(model["lattice_rows"]).det())) == q**4
    E = fmpz_mat(model["embedded_rows"])
    assert int((E*E.transpose()).det()) == 3**3*q**8
    assert not model["basis_reads_outcomes"] and not model["Gaussian_error_promise"]
    point = paired_embed(tuple(x for r in records for x in r.outcome))
    assert point_to_secret(model, point) == secret


def test_complete_small_modular_lattice_equals_native_code_not_a_sublattice():
    records, _ = honest(3)
    model = compile_lattice(records[:2])
    residues = {tuple(sum(a*s for a, s in zip(row, secret)) % 3 for row in model["frequency_rows"])
                for secret in product(range(3), repeat=2)}
    for point in product(range(3), repeat=4):
        if point in residues:
            assert point_to_secret(model, paired_embed(point)) in tuple(product(range(3), repeat=2))
        else:
            with pytest.raises(ValueError, match="not in the native"):
                point_to_secret(model, paired_embed(point))


def test_basis_and_subset_choices_ignore_outcomes():
    records, _ = honest()
    changed = tuple(CovariantRecord(r.first, r.second, ((r.outcome[0]+2) % 9, (r.outcome[1]+3) % 9), 9)
                    for r in records)
    first, second = compile_lattice(records), compile_lattice(changed)
    assert first == second
    assert reduce_basis(first, 12, 1) == reduce_basis(second, 12, 1)
    assert public_subset_schedule(96, 4, 18) == public_subset_schedule(96, 4, 18)


def test_exact_lll_certificate_and_every_repair_point_stay_in_same_code():
    records, _ = honest()
    result = decode(records, ("a", "b", "c"), seed=28)
    paths = 0
    for case in result["cases"]:
        model = case["model"]
        for reduction in case["reductions"]:
            U, E = fmpz_mat(reduction["transform"]), fmpz_mat(model["embedded_rows"])
            assert abs(int(U.det())) == 1
            assert U*E == fmpz_mat(reduction["rows"])
        for witness in case["attempts"]:
            assert point_to_secret(model, witness["point"]) == witness["candidate"]
            rows = case["reductions"][witness["basis_index"]]["rows"]
            assert tuple(sum(a*row[j] for a, row in zip(witness["coefficients"], rows))
                         for j in range(len(rows[0]))) == witness["point"]
            paths += 1
    assert result["cost"]["nearest_plane_paths"] == paths
    assert result["cost"]["training_score_evaluations"] == len(result["proposals"])


@pytest.mark.parametrize("q", (9, 3**32, 3**200))
def test_noiseless_arithmetic_control_recovers_without_enumerating_root(q):
    records, secret = honest(q)
    result = decode(records, ("a", "b", "c"), seed=0, basis_count=1)
    assert result["candidate"] == secret
    assert result["training_score"] == pytest.approx(3)
    assert not result["cost"]["root_value_or_secret_grid_enumeration"]
    assert not result["training_secret_or_heldout_used"]
    assert not result["asymptotic_recovery_proved"]


def test_large_root_score_tie_does_not_erase_nonzero_residual_loss():
    records, secret = honest(3**32)
    assert heldout_score(records, secret) == heldout_score(records, (0, 5))
    assert native_loss(records, secret) == 0
    assert native_loss(records, (0, 5)) > 0


def test_stable_loss_is_the_same_native_score_not_a_gaussian_surrogate():
    records, _ = honest()
    for trial in product(range(9), repeat=2):
        assert 3-2*native_loss(records, trial) == pytest.approx(heldout_score(records, trial), abs=2e-14)


def test_rank_failure_and_whole_caps_never_report_secret_or_hardness():
    records, _ = honest()
    capped = compile_lattice(records, max_equations=5)
    assert capped["status"] == "WHOLE_LATTICE_CAP_EXHAUSTED" and not capped["partial_lattice_compiled"]
    singular = (CovariantRecord((0, 0), (0, 0), (0, 0), 9),)*3
    assert compile_lattice(singular)["status"] == "UNKNOWN_NO_UNIT_ROW_BASIS"
    result = decode(singular, ("a", "b", "c"))
    assert result["candidate"] is None and not result["failure_proves_classical_hardness"]
    empty = decode(records, ("a", "b", "c"), max_equations=3)
    assert empty["candidate"] is None and empty["cost"]["LLL_calls"] == 0


def test_pair_geometry_rejects_garbage_and_noncode_points():
    assert paired_unembed(paired_embed((2, -4, 6, 8))) == (2, -4, 6, 8)
    with pytest.raises(ValueError):
        paired_embed((True, 2))
    with pytest.raises(ValueError):
        paired_unembed((1, 2, 0))
    model = compile_lattice(honest()[0])
    with pytest.raises(ValueError):
        point_to_secret(model, paired_embed((0, 0)))


def test_metric_countercontrol_kills_exact_cvp_equals_likelihood_claim():
    result = metric_countercontrol()
    closer, farther = result["closer_but_worse"], result["farther_but_better"]
    assert closer["torus_paired_distance_squared"] < farther["torus_paired_distance_squared"]
    assert closer["native_score"] < farther["native_score"]
    assert not result["Euclidean_CVP_equals_native_likelihood_maximization"]


def test_fresh_verifier_rejects_reused_source_and_does_not_tune_candidates():
    records, secret = honest()
    result = verify_fresh(records, secret, ("f1", "f2", "f3"), ("t1",))
    assert result["threshold_passed"] and result["gate"]["tested_candidates"] == 1
    assert not result["physical_IID_from_IDs_proved"]
    with pytest.raises(ValueError, match="disjoint"):
        verify_fresh(records, secret, ("t1", "f2", "f3"), ("t1",))
    assert not verify_fresh(records, None, ("f1", "f2", "f3"), ("t1",))["threshold_passed"]


@pytest.mark.parametrize("kwargs", ({"basis_count": 0}, {"subset_rounds": True}, {"seed": -1},
                                    {"max_equations": 0}, {"single_repairs": 1}))
def test_bad_work_or_mode_contracts_rejected(kwargs):
    with pytest.raises(ValueError):
        decode(honest()[0], ("a", "b", "c"), **kwargs)


def test_reused_or_missing_original_ids_rejected():
    records, _ = honest()
    for ids in (("a", "a", "c"), ("a", "b"), ("a", "b", "")):
        with pytest.raises(ValueError):
            decode(records, ids)


def test_actual_native_law_calibration_keeps_failure_and_source_cost():
    result = calibration(2, 3, 95888, training_count=12, heldout_count=24)
    assert result["training_plus_fresh_original_qutrits"] == 36
    assert result["records_are_native_law_simulation_not_unknown_source_supply"]
    assert result["calibration_recovered"] == (result["decoder"]["candidate"] == result["calibration_secret"])
    records = tuple(CovariantRecord(**r) for r in result["training_records"])
    candidate = result["decoder"]["candidate"]
    assert result["decoder"]["training_score"] == pytest.approx(heldout_score(records, candidate))
    assert not result["bounded_success_is_asymptotic_recovery"]


def test_big_certificate_integers_keep_exact_cross_language_json_encoding():
    integer = 3**100
    payload = exact_json({"large": integer, "small": 3, "bool": False, "array": (integer, -integer)})
    output = json.loads(json.dumps(payload))
    assert output["large"] == str(integer) and output["small"] == 3 and output["bool"] is False
    assert output["array"] == [str(integer), str(-integer)]


def test_live_report_independent_exact_replay_and_fixed_controls():
    report = json.loads(REPORT.read_text())
    assert report["control_count"] == 12
    assert report["recoveries"] == sum(c["calibration_recovered"] for c in report["controls"])
    checker = REPORT.parents[1]/"certificates/ternary_measured_lattice_decoder_crosscheck.js"
    output = subprocess.run(["node", str(checker)], text=True, capture_output=True, check=True)
    result = json.loads(output.stdout)
    assert result["status"] == "PASS" and result["exact_rational_Babai_paths"] == 2734


@pytest.mark.parametrize("mutation", ("point", "transform", "source_claim", "Gaussian"))
def test_independent_checker_rejects_forged_lattice_and_access_claims(tmp_path, mutation):
    report = json.loads(REPORT.read_text())
    case = report["controls"][0]["decoder"]["cases"][0]
    if mutation == "point":
        case["attempts"][0]["point"][0] += 1
    elif mutation == "transform":
        case["reductions"][0]["transform"][0][0] += 1
    elif mutation == "source_claim":
        report["classical_simulation_of_original_quantum_inputs"] = True
    else:
        case["model"]["Gaussian_error_promise"] = True
    file = tmp_path/"forged.json"
    file.write_text(json.dumps(report))
    checker = REPORT.parents[1]/"certificates/ternary_measured_lattice_decoder_crosscheck.js"
    assert subprocess.run(["node", str(checker), str(file)], capture_output=True).returncode != 0

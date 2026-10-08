import copy
import hashlib
import json
from pathlib import Path
import subprocess

import numpy as np
import pytest

from ternary_character_cyclic_decoder import (
    DERIVATION, GAP_REPORT, REPORT, SOURCE_REPORT, augment_model, complete_cyclic_groups,
    exact_old_witness_audit, represented_differences,
)
from ternary_character_sdp_decoder import audit_matrix, character_matrix, compile_model, rounded_proposals, solve_relaxation
from ternary_covariant_noise import CovariantRecord


def test_actual_orders_and_unit_generator_canonicalization():
    nodes = tuple((j,) for j in range(9))
    result = complete_cyclic_groups(nodes, 9)
    assert result["status"] == "ALL_REPRESENTED_COMPLETE_CYCLIC_GROUPS"
    assert [(g["order"], g["generator"]) for g in result["groups"]] == [(3, (3,)), (9, (1,))]
    assert result["constraints"] == 12
    differences = represented_differences(nodes, 9)
    for group in result["groups"]:
        assert group["power_entries"] == tuple(differences[tuple(k*x % 9 for x in group["generator"])]
                                               for k in range(group["order"]))


def test_missing_cycle_members_are_not_filled_with_zero():
    result = complete_cyclic_groups(((0,), (1,)), 9)
    assert result["groups"] == [] and result["constraints"] == 0
    assert not result["incomplete_subgroups_silently_completed"]
    assert not result["all_full_group_cyclic_subgroups_enumerated"]


@pytest.mark.parametrize("kwargs,status", [({"max_order": 3}, "CYCLIC_ORDER_CAP_EXHAUSTED"),
                                          ({"max_constraints": 3}, "CYCLIC_CONSTRAINT_CAP_EXHAUSTED")])
def test_whole_scan_caps_are_explicit_failed_attempts(kwargs, status):
    result = complete_cyclic_groups(tuple((j,) for j in range(9)), 9, **kwargs)
    assert result["status"] == status and not result["partial_cyclic_scan_used"]


@pytest.mark.parametrize("nodes,q", [((), 9), (((0,), (0,)), 9), (((0,), (9,)), 9), (((0,),), 8)])
def test_invalid_node_charts_and_field_shadows_are_rejected(nodes, q):
    with pytest.raises(ValueError):
        represented_differences(nodes, q)


def test_every_native_character_passes_complete_cyclic_positivity_including_divisible_secrets():
    records = (CovariantRecord((1, 0), (0, 1), (3, 6), 9),
               CovariantRecord((4, 2), (7, 8), (1, 4), 9))
    model = augment_model(compile_model(records))
    for a in range(9):
        for b in range(9):
            X = character_matrix(model, (a, b))
            values = model["cyclic_fourier_operator"] @ X.reshape(-1)
            assert min(values.real) > -1e-12 and max(abs(values.imag)) < 1e-12
            offset = 0
            for group in model["cyclic_description"]["groups"]:
                assert sum(values[offset:offset+group["order"]]) == pytest.approx(1)
                offset += group["order"]
            assert audit_matrix(model, X)["numerically_feasible"]


def test_compilation_does_not_depend_on_observation_phases():
    records = (CovariantRecord((1, 0), (0, 1), (3, 6), 9),)
    changed = (CovariantRecord((1, 0), (0, 1), (1, 5), 9),)
    first, second = augment_model(compile_model(records)), augment_model(compile_model(changed))
    assert first["cyclic_description"] == second["cyclic_description"]
    assert (first["cyclic_fourier_operator"] != second["cyclic_fourier_operator"]).nnz == 0
    assert not first["cyclic_compilation_reads_truth_or_outcomes"]


@pytest.mark.parametrize("index,count", [(0, 24), (1, 35)])
def test_exact_old_points_pass_root_polygons_but_fail_cyclic_measurements(index, count):
    gaps = json.loads(GAP_REPORT.read_text())
    source = json.loads(SOURCE_REPORT.read_text())
    c = gaps["certificates"][index]
    audit = exact_old_witness_audit(c)
    assert audit["first_moment_polygons_pass_exactly"] and int(audit["minimum_polygon_margin_integer"]) >= 0
    assert audit["negative_laws_certified"] == count
    assert all(int(v["probability_upper_numerator"]) < 0 for v in audit["exact_negative_cyclic_probabilities"])
    original = next(x for x in source["native_controls"] if x["seed"] == c["seed"])
    records = tuple(CovariantRecord(tuple(r["first"]), tuple(r["second"]), tuple(r["outcome"]), r["modulus"])
                    for r in original["training_records"])
    base = compile_model(records, max_matrix_nodes=384)
    X = (np.array(c["witness"]["matrix_real_integer"])+1j*np.array(c["witness"]["matrix_imag_integer"]))/2**24
    assert audit_matrix(base, X)["numerically_feasible"]
    repaired = augment_model(base)
    assert not audit_matrix(repaired, X)["numerically_feasible"]
    assert rounded_proposals(repaired, X)["status"] == "ROUNDING_REFUSED_INFEASIBLE_MATRIX"


def test_actual_strengthened_solver_retains_a_valid_full_group_calibration():
    pytest.importorskip("cvxpy")
    model = augment_model(compile_model((CovariantRecord((1,), (2,), (1, 2), 3),)))
    result = solve_relaxation(model, max_iterations=3000)
    assert result["status"] == "SOLVED_NUMERICALLY"
    assert result["audit"]["minimum_complete_cyclic_probability"] > -2e-5
    assert result["audit"]["complete_cyclic_probabilities_checked"] == 3
    assert not result["dual_optimality_or_integrality_gap_certified"]
    assert model["full_group_saturation"]


def test_live_artifact_pins_inputs_and_preserves_new_fresh_supply_and_failures():
    report = json.loads(REPORT.read_text())
    for field, path in (("source_report_sha256", SOURCE_REPORT), ("gap_report_sha256", GAP_REPORT), ("derivation_sha256", DERIVATION)):
        assert report[field] == hashlib.sha256(path.read_bytes()).hexdigest()
    assert not report["global_realizability_or_population_recovery_proved"]
    assert not report["accepted_candidate_or_speedup"]
    assert [a["negative_laws_certified"] for a in report["exact_old_witness_audits"]] == [24, 35]
    assert [a["negative_cyclic_groups_certified"] for a in report["exact_old_witness_audits"]] == [20, 22]
    originals = {c["seed"]: c for c in json.loads(SOURCE_REPORT.read_text())["native_controls"]}
    for c in report["controls"]:
        assert not c["old_holdout_used_for_validation"] and not c["population_recovery_proved"]
        assert c["new_fresh_native_qutrits"] == len(c["fresh_source"]["records"]) == 256
        for v in c["fresh_verification"].values():
            assert all("NEW-fresh" in x for x in v["fresh_original_ids"])
            assert not v["speedup_claim_allowed"]
        truth = originals[c["seed"]]["calibration_secret_NOT_decoder_input"]
        for method, v in c["fresh_verification"].items():
            assert c["calibration_recovery_NOT_decoder_input"][method] == (v["candidate"] == truth)


CHECKER = Path(__file__).resolve().parents[1]/"research/certificates/ternary_character_cyclic_decoder_crosscheck.js"


def test_independent_exact_cyclic_rejection_and_numerical_repair_replay():
    output = subprocess.run(["node", str(CHECKER)], check=True, capture_output=True, text=True)
    result = json.loads(output.stdout)
    assert result["status"] == "PASS" and result["exact_negative_laws"] == 59
    assert result["root_polygon_checks_exact"] > 100000
    assert not result["global_realizability_or_population_recovery_certified"]


@pytest.mark.parametrize("mutation", ["scope", "order", "missing_power", "negative_bound", "holdout"])
def test_tampered_new_constraints_and_access_claims_are_rejected(tmp_path, mutation):
    report = copy.deepcopy(json.loads(REPORT.read_text()))
    if mutation == "scope":
        report["global_realizability_or_population_recovery_proved"] = True
    elif mutation == "order":
        report["exact_old_witness_audits"][0]["description"]["groups"][0]["order"] = 9
    elif mutation == "missing_power":
        report["exact_old_witness_audits"][0]["description"]["groups"][0]["power_entries"].pop()
    elif mutation == "negative_bound":
        report["exact_old_witness_audits"][0]["exact_negative_cyclic_probabilities"][0]["probability_upper_numerator"] = "-1"
    else:
        report["controls"][0]["old_holdout_used_for_validation"] = True
    target = tmp_path/"tampered.json"
    target.write_text(json.dumps(report))
    output = subprocess.run(["node", str(CHECKER), str(target)], capture_output=True, text=True)
    assert output.returncode != 0

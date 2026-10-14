"""Tests for the corrected conditional native phase lift, not a full receiver."""
import inspect
import json
import subprocess

import numpy as np
import pytest

from theorems.nil3_state_hsp_descent_receiver import (
    CENTRAL, LEVEL, REPORT, SuppliedPhaseSample, conditional_batch_control,
    conditional_phase_lift, full_nil3_receiver_simulation, phase_exponents,
    recover_top_digits, ring_model_countercontrols, run_all_controls,
    solve_full_rank_f3, tree_dilation_complexity_ledger,
)
from cyclotomic_rescaling_gate import multiply, plus, reduce_element
from native_state_hsp_bridge import NativeGroup


@pytest.mark.parametrize("lower", ((0, 0), (1, 0), (2, 2)))
@pytest.mark.parametrize("u", (0, 1, 2))
def test_actual_original_source_is_corrected_using_only_known_lower_parameters(lower, u):
    label = ((1, 0),)
    s = plus(reduce_element(lower, 3), multiply(CENTRAL, (u, 0), 3), 3)
    sample = SuppliedPhaseSample(label, NativeGroup(3).supplied_phase_state(label, (s,)))
    lift = conditional_phase_lift(sample, (lower,))
    assert lift["central_character_row"] == (2,)
    assert lift["measurement_probabilities"][(2*u) % 3] > 1-1e-12
    assert lift["phase_correction_exponents_mod9"] == tuple((-e) % 9 for e in phase_exponents(label, (reduce_element(lower, 3),)))
    assert not lift["top_secret_used_in_gate_parameters"]
    assert tuple(inspect.signature(conditional_phase_lift).parameters) == ("sample", "known_lower")


def test_wrong_lower_premise_is_not_silently_verified_or_a_deterministic_residual():
    G = NativeGroup(3)
    label, secret = ((1, 0),), ((1, 0),)
    sample = SuppliedPhaseSample(label, G.supplied_phase_state(label, secret))
    bad = conditional_phase_lift(sample, ((0, 0),))
    assert max(bad["measurement_probabilities"]) < .99
    good = conditional_phase_lift(sample, secret)
    assert good["measurement_probabilities"][0] > 1-1e-12


def test_ramified_ring_and_hidden_generator_order_are_not_the_polynomial_model():
    r = ring_model_countercontrols()
    assert r["native_three_times_one"] == (3, 0)
    assert r["native_pi_squared"] == (6, 0)
    assert r["native_hidden_generator_cube"] == (((0, 0),), 0)
    assert r["incorrect_truncated_polynomial_generator_cube_z_digit"] == 2
    assert not r["native_cyclotomic_ring_is_F3_truncated_polynomial_ring"]


@pytest.mark.parametrize("n", (2, 4, 8))
def test_conditional_vector_recovery_charges_supplied_samples_and_does_not_recover_lower_digits(n):
    r = conditional_batch_control(n, 9000+n)
    result = r["result"]
    assert result["recovered_top_digits"] == r["top_truth_fixture_only"]
    assert n <= result["consumed_samples"] <= result["available_samples"] == n+8
    assert not result["known_lower_premise_verified_here"]
    assert not r["lower_quotient_receiver_executed"]
    assert not result["full_secret_receiver_supplied"]


def test_rank_deficient_source_returns_unknown_without_guessing_or_free_fresh_samples():
    sample = SuppliedPhaseSample(((0, 0),), np.ones(3)/np.sqrt(3))
    r = recover_top_digits((sample, sample), ((0, 0),), np.random.default_rng(1))
    assert r["status"] == "INSUFFICIENT_INDEPENDENT_LABELS"
    assert r["recovered_top_digits"] is None
    assert r["consumed_samples"] == r["available_samples"] == 2


def test_missing_full_receiver_is_explicit_instead_of_secret_assignment():
    with pytest.raises(NotImplementedError, match="not implemented"):
        full_nil3_receiver_simulation(n=3)
    assert "secret" not in inspect.signature(recover_top_digits).parameters
    r = run_all_controls()
    assert len(r["complete_scalar_phase_controls"]) == 729
    assert not r["summary"]["nil3_state_hsp_solved_in_polynomial_time"]
    assert not r["summary"]["lower_quotient_receiver_supplied"]


def test_f3_solver_requires_full_rank_and_detects_inconsistency():
    assert solve_full_rank_f3(((1, 0), (0, 1)), (2, 1), 2) == (2, 1)
    assert solve_full_rank_f3(((1, 0),), (2,), 2) is None
    with pytest.raises(ValueError, match="inconsistent"):
        solve_full_rank_f3(((1,), (1,)), (0, 1), 1)


def test_every_fixed_depth_is_polynomial_and_the_tree_model_is_not_a_lower_bound():
    for c in tree_dilation_complexity_ledger((4, 8), (2, 3, 4, 8)):
        n, r = c["dimension_n"], c["nilpotency_class_r"]
        assert int(c["total_copies_in_specified_disjoint_tree"]) == n*n*(n+1)**(2*(r-2))
        assert c["fixed_depth_polynomial_degree_in_n"] == 2*r-2
        assert c["every_fixed_r_is_polynomial_in_n"]
        assert not c["implemented_receiver_or_universal_copy_lower_bound"]


def test_independent_native_ring_and_phase_replay():
    checker = REPORT.parents[1]/"certificates/nil3_state_hsp_descent_crosscheck.js"
    result = subprocess.run(["node", str(checker)], capture_output=True, text=True, check=True)
    r = json.loads(result.stdout)
    assert r["status"] == "PASS" and r["native_scalar_phase_controls"] == 729
    assert r["conditional_vector_batches"] == 3 and not r["full_receiver_supplied"]


@pytest.mark.parametrize("mutation", ("ring", "correction", "source", "coefficient", "known_lower", "output", "rank", "full_receiver", "hardness", "tree", "legacy_recovery"))
def test_independent_checker_rejects_wrong_source_free_lower_data_and_general_promotion(tmp_path, mutation):
    r = json.loads(REPORT.read_text())
    c = r["complete_scalar_phase_controls"][100]
    if mutation == "ring":
        r["ring_model_countercontrols"]["native_three_times_one"] = [0, 0]
    elif mutation == "correction":
        c["phase_correction_exponents_mod9"][1] ^= 1
    elif mutation == "source":
        c["source_phase_exponents_mod9_fixture"][1] ^= 1
    elif mutation == "coefficient":
        c["central_character_row"][0] = (c["central_character_row"][0]+1) % 3
    elif mutation == "known_lower":
        r["conditional_batch_controls"][0]["result"]["known_lower_premise_verified_here"] = True
    elif mutation == "output":
        r["conditional_batch_controls"][0]["result"]["recovered_top_digits"][0] ^= 1
    elif mutation == "rank":
        r["conditional_batch_controls"][0]["result"]["rows"][0][0] = 5
    elif mutation == "full_receiver":
        r["summary"]["nil3_state_hsp_solved_in_polynomial_time"] = True
    elif mutation == "hardness":
        r["summary"]["growing_depth_LWE_hardness_proved"] = True
    elif mutation == "tree":
        r["tree_dilation_ledger"][0]["implemented_receiver_or_universal_copy_lower_bound"] = True
    else:
        r["end_to_end_simulation"] = {"full_secret_recovered_identically": True}
    target = tmp_path/"forged.json"
    target.write_text(json.dumps(r))
    result = subprocess.run(["node", str(REPORT.parents[1]/"certificates/nil3_state_hsp_descent_crosscheck.js"), str(target)], capture_output=True)
    assert result.returncode != 0


@pytest.mark.parametrize("call", (
    lambda: SuppliedPhaseSample((), np.ones(3)/np.sqrt(3)),
    lambda: SuppliedPhaseSample(((1, 0),), np.zeros(3)),
    lambda: conditional_phase_lift(SuppliedPhaseSample(((1, 0),), np.ones(3)/np.sqrt(3)), ((8, 0),)),
    lambda: solve_full_rank_f3(((1, True),), (1,), 2),
))
def test_invalid_source_norm_lower_premises_and_field_parameters_rejected(call):
    with pytest.raises(ValueError):
        call()

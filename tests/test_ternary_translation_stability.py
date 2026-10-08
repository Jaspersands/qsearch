from fractions import Fraction
import hashlib
import json
from pathlib import Path
import subprocess

import numpy as np
import pytest

from ternary_translation_stability import (
    DERIVATION, REPORT, numerical_pair_control, pair_rounding_gate,
    sequential_rounding_ledger, weyl_falsifier,
)


@pytest.mark.parametrize("q", [3, 9, 27])
def test_actual_clock_shift_orders_commutator_and_winding_at_entire_root(q):
    z = np.exp(2j*np.pi*np.arange(q)/q)
    Z, X = np.diag(z), np.roll(np.eye(q, dtype=complex), 1, axis=0)
    C = Z@X@Z.conj().T@X.conj().T
    assert np.linalg.norm(np.linalg.matrix_power(Z, q)-np.eye(q), 2) < 1e-10
    assert np.array_equal(np.linalg.matrix_power(X, q), np.eye(q))
    assert np.linalg.norm(C-np.exp(2j*np.pi/q)*np.eye(q), 2) < 1e-10
    assert np.angle(np.linalg.eigvals(C)).sum()/(2*np.pi) == pytest.approx(1)
    norm = np.linalg.norm(Z@X-X@Z, 2)
    witness = weyl_falsifier(q)
    assert float(Fraction(witness["commutator_operator_norm_lower"])) <= norm
    assert norm <= float(Fraction(witness["commutator_operator_norm_upper"]))


@pytest.mark.parametrize("r", [10, 20, 50])
def test_small_commutator_threshold_does_not_certify_operator_rounding(r):
    w = weyl_falsifier(3**r)
    assert w["commutator_only_threshold_status"] == "PASSES_CERTIFIED"
    assert w["distance_to_every_commuting_unitary_pair_operator_norm_lower"] == "1/4"
    assert not w["finite_order_pair_gate"]["sufficient_invertibility_condition_met"]
    assert not w["dense_q_by_q_operators_allocated"]
    assert not w["is_supplied_native_flat_moment_completion"]
    assert not w["normalized_Hilbert_Schmidt_rounding_obstructed"]
    assert not w["all_source_specific_approximate_flatness_ruled_out"]


@pytest.mark.parametrize("q", [9, 27])
def test_conditional_positive_pair_law_replays_known_order_preserving_inputs(q):
    c = numerical_pair_control(q)
    t, cosine, sine = [Fraction(c[k]) for k in ("rotation_parameter", "rotation_cosine_exact", "rotation_sine_exact")]
    assert cosine*cosine+sine*sine == 1
    assert Fraction(c["commutator_upper_follows_from_conjugation_not_measured_tolerance"]) == 8*t
    g, m = c["finite_order_pair_gate"], c["numerical_metrics"]
    assert g["sufficient_invertibility_condition_met"]
    assert m["rounding_distance_observed"] <= float(Fraction(g["distance_to_commuting_exact_q_order_pair_upper"]))
    assert m["rounded_commutator_norm_observed"] < 1e-10
    assert m["rounded_q_power_error_observed"] < 1e-10
    assert m["rounded_unitarity_error_observed"] < 1e-10
    assert not c["numerical_output_is_exact_operator_certificate"]


def test_exact_pair_gate_is_strict_at_the_invertibility_boundary():
    assert pair_rounding_gate(9, 0)["distance_to_commuting_exact_q_order_pair_upper"] == "0"
    assert not pair_rounding_gate(9, Fraction(1, 4))["sufficient_invertibility_condition_met"]
    assert pair_rounding_gate(9, Fraction(1, 8))["sufficient_invertibility_condition_met"]
    assert pair_rounding_gate(9, Fraction(1, 8))["distance_to_commuting_exact_q_order_pair_upper"] == "2"


@pytest.mark.parametrize("bad", [-1, .0001, True, "1/1000"])
def test_float_or_negative_residuals_are_not_analytic_bounds(bad):
    with pytest.raises(ValueError, match="exact rational"):
        pair_rounding_gate(9, bad)


def test_dense_numerical_cap_does_not_block_symbolic_full_root_falsifiers():
    with pytest.raises(ValueError, match="dense numerical replay capped"):
        numerical_pair_control(81)
    assert weyl_falsifier(3**50)["operator_dimension"] == str(3**50)


@pytest.mark.parametrize("n,q", [(8, 9), (32, 81), (128, 243)])
def test_sequential_precision_bound_exposes_growth_without_a_generic_no_go(n, q):
    ledger = sequential_rounding_ledger(n, q)
    e = [int(x) for x in ledger["sequential_error_coefficients"]]
    assert e[0] == 0
    assert e[1] == 2*(q-1)
    assert all(e[j] == 2*(q-1)*(j+2*sum(e[:j])) for j in range(1, n))
    delta = Fraction(ledger["sufficient_uniform_commutator_error_upper"])
    target = Fraction(ledger["target_operator_norm_error"])
    assert all(c*delta <= target < 1 for c in e)
    assert ledger["coefficient_growth_is_a_strategy_bound_not_general_impossibility"]
    assert not ledger["polynomial_precision_in_n_established"]
    assert not ledger["group_size_q_to_n_enumerated"]


def test_live_scope_and_derivation_hash():
    r = json.loads(REPORT.read_text())
    assert r["derivation_sha256"] == hashlib.sha256(DERIVATION.read_bytes()).hexdigest()
    assert r["known_operator_theory_not_novelty_claim"]
    for k in ("native_approximate_flatness_proved", "native_noisy_decoder_supplied", "quantum_speedup_proved", "candidate_record_accepted"):
        assert not r[k]


CHECKER = Path(__file__).resolve().parents[1]/"research/certificates/ternary_translation_stability_crosscheck.js"


def test_independent_symbolic_bounds_and_pair_repair_checker():
    p = subprocess.run(["node", str(CHECKER)], capture_output=True, text=True, check=True)
    r = json.loads(p.stdout)
    assert r["status"] == "PASS"
    assert r["symbolic_full_root_weyl_falsifiers"] == 6
    assert r["positive_pair_calibrations"] == 2
    assert not r["native_noisy_decoder_supplied"]


@pytest.mark.parametrize("mutation", ["index", "dimension", "distance", "commutator", "pair", "rotation", "sequence", "norm_scope", "native_claim"])
def test_independent_checker_rejects_wrong_topology_precision_or_scope(tmp_path, mutation):
    r = json.loads(REPORT.read_text())
    w = r["weyl_falsifiers"][-1]
    if mutation == "index":
        w["principal_log_winding_index_exact"] = 0
    elif mutation == "dimension":
        w["operator_dimension"] = "3"
    elif mutation == "distance":
        w["distance_to_every_commuting_unitary_pair_operator_norm_lower"] = "1/2"
    elif mutation == "commutator":
        w["commutator_operator_norm_upper"] = "0"
    elif mutation == "pair":
        r["positive_pair_calibrations"][0]["finite_order_pair_gate"]["distance_to_commuting_exact_q_order_pair_upper"] = "0"
    elif mutation == "rotation":
        r["positive_pair_calibrations"][0]["rotation_cosine_exact"] = "1"
    elif mutation == "sequence":
        r["sequential_precision_ledgers"][0]["sequential_error_coefficients"][-1] = "1"
    elif mutation == "norm_scope":
        w["normalized_Hilbert_Schmidt_rounding_obstructed"] = True
    elif mutation == "native_claim":
        r["native_approximate_flatness_proved"] = True
    target = tmp_path/"corrupt.json"
    target.write_text(json.dumps(r))
    p = subprocess.run(["node", str(CHECKER), str(target)], capture_output=True, text=True)
    assert p.returncode != 0

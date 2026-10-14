from copy import deepcopy
from fractions import Fraction
import json
import subprocess

import numpy as np
import pytest

from theorems import native_word_collision_symmetry as A


def stored():
    return json.loads(A.REPORT.read_text())


def node_check(payload):
    return subprocess.run([
        "node", "-e",
        "const A=require('./research/certificates/native_word_collision_symmetry_crosscheck.js');"
        "let s='';process.stdin.on('data',x=>s+=x);process.stdin.on('end',()=>console.log(JSON.stringify(A.verify(JSON.parse(s)))));",
    ], input=json.dumps(payload), text=True, capture_output=True, cwd=A.ROOT)


@pytest.mark.parametrize("index", range(4))
def test_literal_joint_circuit_keeps_every_branch(index):
    c = stored()["actual_source_controls"][index]
    base = c["native_spectral_reference"]
    out = A.literal_branches(base["actual_native_word_rows"], base["original_records"][0]["modulus"])
    for key, expected in c["literal_joint_branches"].items():
        if isinstance(expected, float):
            assert out[key] == pytest.approx(expected)
        else:
            assert out[key] == expected
    assert sum(out[k] for k in ("equal_plus", "equal_minus", "unequal_plus", "unequal_minus")) == pytest.approx(1)
    assert out["equal_plus"] + out["equal_minus"] == pytest.approx(float(Fraction(c["exact_equal_total_probability"])))
    assert not out["branch_discarded_for_free"]


def test_entire_measured_word_pair_law_matches_classical_readout_not_only_total():
    c = stored()["actual_source_controls"][1]
    base = c["native_spectral_reference"]
    rows, D, q = base["actual_native_word_rows"], base["word_dimension"], base["original_records"][0]["modulus"]
    psi = np.exp(2j * np.pi * np.asarray([r["known_phase"] for r in rows]) / q) / np.sqrt(D)
    initial = np.outer(psi, np.ones(D) / np.sqrt(D))
    for sign in (-1, 1):
        literal = abs((initial + sign * initial.T) / 2) ** 2
        phase = np.asarray([r["known_phase"] for r in rows])
        classical = (1 + sign * np.cos(2 * np.pi * (phase[:, None] - phase[None, :]) / q)) / (2 * D * D)
        assert literal == pytest.approx(classical, abs=1e-12)
    assert not c["classical_full_measured_readout_identity"]["coherent_amplification_or_retained_unmeasured_output_simulated"]


def test_noise_factorization_is_verified_and_falsified_when_labels_enter_errors():
    p = stored()
    assert p["independent_error_label_census"] == A.label_noise_census()
    assert p["independent_error_label_census"]["independent_error_averaging_identity_holds"]
    c = p["label_dependent_error_countercensus"]
    assert c == A.label_noise_census(True)
    assert c["exact_mean_C_minus_R"] == "0"
    assert c["one_over_N_times_mean_one_minus_error_fidelity"] == "8/27"
    assert not c["errors_independent_of_labels"]
    assert not c["independent_error_averaging_identity_holds"]


def test_effective_word_observable_commutes_and_matches_joint_circuit_on_arbitrary_state():
    c = stored()["actual_source_controls"][0]
    base = c["native_spectral_reference"]
    rows, D = base["actual_native_word_rows"], base["word_dimension"]
    frequencies = [tuple(r["frequency"]) for r in rows]
    equal = np.asarray([[a == b for b in frequencies] for a in frequencies])
    K = equal.astype(float) / D
    diagonal = np.diag(equal.sum(axis=1) / D)
    assert diagonal @ K == pytest.approx(K @ diagonal)
    psi = np.arange(1, D + 1) + 1j * np.arange(D, 0, -1)
    psi /= np.linalg.norm(psi)
    initial = np.outer(psi, np.ones(D) / np.sqrt(D))
    for sign in (-1, 1):
        effect = (diagonal + sign * K) / 2
        joint = float(np.sum(abs(((initial + sign * initial.T) / 2)[equal]) ** 2))
        assert np.vdot(psi, effect @ psi).real == pytest.approx(joint)
        assert np.linalg.eigvalsh(effect).min() >= -1e-12
        assert np.linalg.eigvalsh(effect).max() <= 1 + 1e-12
    assert c["effective_original_word_effect_commutes_with_raw_Gram"]
    assert c["phase_independent_diagonal_term_cancels_source_vs_IID_null"]


def test_large_conditional_gap_does_not_erase_exponential_amplification_price():
    for p in stored()["scaling_ensemble_ledgers"]:
        assert Fraction(p["conditional_antisymmetric_gap_lower"]) > Fraction(49, 100)
        assert int(p["necessary_standard_amplification_iterations_lower"]) > 10 ** 14
        assert not p["amplified_ensemble_source_gap_certified"]
        assert not p["generic_trace_error_safe_after_rare_branch_conditioning"]
        assert not p["arbitrary_nonstandard_quantum_algorithm_lower_bound"]


def test_noisy_moment_bound_can_erase_signal():
    p = A.ensemble_ledger(8, 8, 12, "1")
    assert p["conditional_antisymmetric_gap_lower"] == "0"


def test_independent_checker_replays_entire_current_reference():
    r = node_check(stored())
    assert r.returncode == 0, r.stderr
    assert json.loads(r.stdout)["verified"]


@pytest.mark.parametrize("kind", (
    "exact-plus", "exact-minus", "mass", "null", "conditional-gap", "amplification-cost",
    "classical-law", "physical-claim", "noise-scope", "countercensus", "source-census", "speedup", "hash",
))
def test_independent_checker_rejects_output_and_scope_tampering(kind):
    p = deepcopy(stored())
    c, ledger = p["actual_source_controls"][0], p["scaling_ensemble_ledgers"][0]
    if kind == "exact-plus":
        c["exact_equal_plus_root_polynomial"] = []
    elif kind == "exact-minus":
        c["exact_equal_minus_root_polynomial"] = ["1"]
    elif kind == "mass":
        c["literal_joint_branches"]["unequal_minus"] += .1
    elif kind == "null":
        c["IID_null_equal_minus_probability"] = "0"
    elif kind == "conditional-gap":
        ledger["conditional_antisymmetric_gap_lower"] = "1"
    elif kind == "amplification-cost":
        ledger["necessary_standard_amplification_iterations_lower"] = "1"
    elif kind == "classical-law":
        c["classical_full_measured_readout_identity"]["coherent_amplification_or_retained_unmeasured_output_simulated"] = True
    elif kind == "physical-claim":
        c["scalable_logical_recipe"]["physical_gate_compilation_and_precision_certified"] = True
    elif kind == "noise-scope":
        ledger["original_errors_independent_of_full_root_original_labels_required"] = False
    elif kind == "countercensus":
        p["label_dependent_error_countercensus"]["independent_error_averaging_identity_holds"] = True
    elif kind == "source-census":
        p["independent_error_label_census"]["exact_mean_raw_acceptance"] = "1"
    elif kind == "speedup":
        p["accepted_speedup_candidate"] = True
    else:
        p["producer_sha256"] = "0" * 64
    assert node_check(p).returncode != 0

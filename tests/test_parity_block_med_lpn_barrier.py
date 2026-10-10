"""Tests for parity block minimum-error state discrimination and LPN reduction."""
from __future__ import annotations

import hashlib
from pathlib import Path
import pytest
from flint import fmpq

from theorems.parity_block_med_lpn_barrier import (
    DERIVATION,
    REPORT,
    global_coherent_pgm_bound,
    gram_eigenvalues,
    lpn_scaling_ledger,
    noise_spectrum_closed_form,
    physical_helstrom_control,
    run_all_controls,
)


def test_gram_eigenvalues_trace_and_multiplicities():
    for c_val in (fmpq(1, 5), fmpq(1, 3), fmpq(1, 2), fmpq(2, 3), fmpq(4, 5)):
        res = gram_eigenvalues(c_val)
        assert res["is_trace_8"] is True
        assert res["exact_trace"] == "8"

        # Check positivity of all eigenvalues
        l0 = fmpq(res["lambda_000"])
        lw2 = fmpq(res["lambda_w2"])
        lw1 = fmpq(res["lambda_w1_w3"])
        assert l0 > 0
        assert lw2 > 0
        assert lw1 > 0

        # Multiplicity weighted sum must be 8
        assert l0 + 3 * lw2 + 4 * lw1 == 8


def test_noise_spectrum_closed_form_identities():
    for c_val in (fmpq(1, 4), fmpq(1, 2), fmpq(3, 4)):
        spec = noise_spectrum_closed_form(c_val)
        assert spec["algebraic_conservation_certified"] is True
        assert abs(spec["sum_probabilities_diagnostic"] - 1.0) < 1e-12

        # Probabilities lie in valid intervals
        assert 0.0 < spec["p_success"] < 1.0
        assert 0.0 <= spec["p_error_single_word"] < 1.0
        assert 0.0 <= spec["p_error_tail_111"] < 1.0

        # Marginal bit error is strictly positive and less than total block error
        assert 0.0 < spec["marginal_bit_error_rate"] < spec["total_block_error"]

        # For c <= 1/2 (low-to-moderate overlap), marginal error beats raw unencoded channel error
        if float(c_val) <= 0.5:
            assert spec["marginal_bit_error_rate"] < spec["raw_binary_channel_error_rate"]


def test_physical_helstrom_control_optimality():
    for c_val in (fmpq(1, 4), fmpq(1, 2), fmpq(3, 4)):
        ctrl = physical_helstrom_control(c_val)
        assert ctrl["helstrom_optimality_verified"] is True
        assert ctrl["gram_matrix_max_error"] < 1e-12
        assert ctrl["lambda_hermiticity_error"] < 1e-12
        assert ctrl["helstrom_condition_min_eigenvalue"] >= -1e-11
        assert ctrl["transition_matrix_max_error"] < 1e-12

        # Check simulated probabilities agree with closed form
        spec = noise_spectrum_closed_form(c_val)
        assert abs(ctrl["p_success_simulated"] - spec["p_success"]) < 1e-12
        assert abs(ctrl["p_error_single_word_simulated"] - spec["p_error_single_word"]) < 1e-12
        assert abs(ctrl["p_error_tail_111_simulated"] - spec["p_error_tail_111"]) < 1e-12


def test_lpn_scaling_ledger_profiles():
    ledger = lpn_scaling_ledger(fmpq(1, 2), h_dims=(16, 32, 64, 128))
    assert 0.0 < ledger["block_error_rate_eta"] < 1.0
    assert 0.0 < ledger["marginal_bit_error_rate"] < 1.0

    profiles = ledger["profiles"]
    assert len(profiles) == 4

    for p in profiles:
        assert p["clean_information_set_probability"] > 0
        assert p["expected_isd_prange_trials"] >= 1.0
        assert p["log2_expected_isd_trials"] >= 0.0

    # Dimension 64 and 128 must be marked as NP-hard LPN
    assert profiles[2]["decoding_regime"] == "NP-hard LPN"
    assert profiles[3]["decoding_regime"] == "NP-hard LPN"
    # Trials must grow strictly monotonically with h
    assert profiles[0]["log2_expected_isd_trials"] < profiles[1]["log2_expected_isd_trials"]
    assert profiles[1]["log2_expected_isd_trials"] < profiles[2]["log2_expected_isd_trials"]
    assert profiles[2]["log2_expected_isd_trials"] < profiles[3]["log2_expected_isd_trials"]


def test_global_coherent_pgm_bounds():
    bound = global_coherent_pgm_bound(fmpq(1, 2), 64, 128)
    assert bound["channel_cutoff_rate_R0"] > 0.0
    assert bound["global_pgm_is_walsh_hadamard"] is True
    assert bound["global_coherent_pgm_escapes_cutoff"] is False


def test_run_all_controls_and_report_integrity():
    report = run_all_controls()
    assert report["status"] == "PARITY_BLOCK_MED_LPN_BARRIER_CERTIFIED"
    assert report["derivation_sha256"] == hashlib.sha256(DERIVATION.read_bytes()).hexdigest()
    assert report["producer_sha256"] == hashlib.sha256(Path("theorems/parity_block_med_lpn_barrier.py").read_bytes()).hexdigest()

    summary = report["summary"]
    assert summary["local_helstrom_measurement_is_hadamard"] is True
    assert summary["algebraic_noise_conservation_proven"] is True
    assert summary["block_wise_med_reduces_to_lpn"] is True
    assert summary["usd_avoids_lpn_via_exact_erasure_at_cost_of_prange_dequantization"] is True
    assert summary["med_improves_local_fidelity_but_incurs_exponential_isd_decoding"] is True
    assert summary["quantum_speedup_claimed"] is False
    assert summary["shor_level_speedup_falsified_for_this_architecture"] is True


def test_invalid_parameters():
    with pytest.raises(ValueError):
        gram_eigenvalues(0)  # overlap 0 not in (0, 1)
    with pytest.raises(ValueError):
        gram_eigenvalues(1)  # overlap 1 not in (0, 1)
    with pytest.raises(ValueError):
        noise_spectrum_closed_form(-0.5)
    with pytest.raises(ValueError):
        lpn_scaling_ledger(fmpq(1, 2), h_dims=(0,))

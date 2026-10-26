from fractions import Fraction as Q
import hashlib
import json
from pathlib import Path
import random

import numpy as np
import pytest

from theorems import balanced_mpi_product_target as target
from theorems import balanced_signed_mpi as mpi


def test_center_average_identity():
    result = target.center_average_control()
    assert result["centers_enumerated"] == 125
    assert result["average_discarded_target_energy"] == pytest.approx(
        float(Q(result["discarded_source_mass"])), abs=2e-14)
    assert result["average_target_tv"] <= result["average_tv_bound"]
    assert result["maximum_pointwise_bound_violation"] < 2e-14


@pytest.mark.parametrize("bits", [3, 4])
def test_mpi_product_and_truncated_identities(bits):
    result = target.mpi_control(bits)
    assert result["retained_norm"] == pytest.approx(
        float(Q(result["retained_mass"])), abs=2e-13)
    assert result["product_amplitude_identity_max_error"] < 2e-13
    assert result["target_tv"] <= result["pointwise_tv_bound"] + 2e-13
    assert result["patterns_enumerated"] == 81
    assert result["retained_patterns"] == 21


def test_worst_case_tail_shortcut_is_false():
    result = target.worst_case_amplification_control()
    assert Q(result["discarded_mass_upper"]) < Q(1, 100)
    assert result["actual_target_tv"] > 0.5
    assert result["incorrect_worst_case_bound"] < 0.101
    assert result["actual_target_tv"] > 5*result["incorrect_worst_case_bound"]
    assert not result["is_log_cauchy_mpi_instance"]


def test_gauge_randomization_does_not_improve_tv():
    result = target.worst_case_amplification_control()
    assert result["gauge_shifted_tv"] == pytest.approx(result["actual_target_tv"], abs=1e-14)
    assert result["gauge_permutation_max_error"] < 1e-14


@pytest.mark.parametrize("model", ["fixed", "planted", "uniform_code_shift"])
def test_center_assumption_is_enforced(model):
    with pytest.raises(ValueError, match="independent uniform"):
        target.transfer_certificate(4, 4, 1, Q(1, 20), center_model=model)


def test_score_guard_is_not_just_norm_injectivity():
    with pytest.raises(ValueError, match="separation"):
        target.transfer_certificate(5, 3, 1, Q(1, 20), center_model=target.CENTER_MODEL)


def test_invalid_source_box_is_rejected():
    with pytest.raises(ValueError, match="syndrome-injective"):
        target.finite_transfer_control([[1], [1]], 7, 1, Q(1, 20), [0, 0])


def test_enumeration_is_not_a_native_sampler():
    with pytest.raises(ValueError, match="budget"):
        target.finite_transfer_control([[1]]*6, 7, 0, Q(1, 20), [0]*6)


def test_product_log_evaluation():
    t, order = Q(1, 20), 15
    residues = np.array([0, 1, 5, 11, 14], dtype=np.int64)
    explicit = np.prod((float(1-t)**.5 + float(2*t)**.5 *
                        np.cos(2*np.pi*residues/order))**2)
    assert np.exp(target.product_log_weight(residues, order, t)) == pytest.approx(explicit)
    assert target.product_log_weight(residues+order, order, t) == pytest.approx(
        target.product_log_weight(residues, order, t))
    with pytest.raises(ValueError, match="integer residues"):
        target.product_log_weight(np.array([0.25]), order, t)
    with pytest.raises(ValueError, match="positive"):
        target.product_log_weight(residues, order, Q(1, 3))


def test_conditional_certificate_uses_outward_bounds():
    result = target.transfer_certificate(4, 4, 1, Q(1, 20),
                                         center_model=target.CENTER_MODEL)
    z = mpi.multinomial_box(4, 1, 1, Q(1, 20))
    lo, hi = map(Q, result["retained_mass_interval"])
    assert lo <= z <= hi
    assert Q(result["discarded_mass_upper"]) >= 1-z
    assert Q(result["center_averaged_target_tv_upper"])**2 >= (1-z)/z
    assert not result["sampling_premise_proved"]
    assert not result["worst_case_center_guarantee"]
    assert not result["gauge_randomization_supplies_center_model"]


@pytest.mark.parametrize("order", [7, 15, 21])
def test_harmonic_fft_with_nonunit_slopes(order):
    t, harmonics = Q(1, 20), 9
    residuals = np.array([0, 1, 4, 6, 2, 1], dtype=np.int64)
    slopes = np.array([0, 1, 3, 5, 7, 0], dtype=np.int64)
    computed = target.harmonic_line_log_weights(residuals, slopes, order, t, harmonics)
    ratio = float(2*t)**.5/(float(1-t)**.5 + float(1-3*t)**.5)
    constant = 2*len(slopes)*np.log((float(1-t)**.5+float(1-3*t)**.5)/2)
    error = float(Q(target.harmonic_certificate(len(slopes), t, harmonics)[
        "uniform_log_weight_error_upper"]))
    for step, value in enumerate(computed):
        residues = (residuals+step*slopes) % order
        direct_truncation = constant + sum(
            4*(-1)**(k+1)*ratio**k/k*np.cos(2*np.pi*k*residues/order).sum()
            for k in range(1, harmonics+1))
        assert value == pytest.approx(direct_truncation, abs=1e-13)
        assert abs(value-target.product_log_weight(residues, order, t)) < error+1e-13


def test_harmonic_stationary_tv_is_not_mixing():
    t = Q(1, 20)
    result = target.harmonic_certificate(6000, t, 9)
    assert Q(result["stationary_target_tv_upper"]) < Q(1, 10000)
    assert result["coefficient_accumulations_per_line"] == 108000
    assert not result["invertible_slopes_required"]
    assert not result["mixing_time_proved"]
    assert not result["floating_fft_roundoff_certified"]
    assert Q(target.harmonic_certificate(6000, t, 0)["stationary_target_tv_upper"]) == 1


def test_unsigned_slopes_do_not_wrap_negative_frequencies():
    residues = np.array([0, 2, 7], dtype=np.uint64)
    slopes = np.array([1, 3, 5], dtype=np.uint64)
    unsigned = target.harmonic_line_log_weights(residues, slopes, 15, Q(1, 20), 9)
    signed = target.harmonic_line_log_weights(
        residues.astype(np.int64), slopes.astype(np.int64), 15, Q(1, 20), 9)
    np.testing.assert_allclose(unsigned, signed, rtol=0, atol=0)


def test_exact_stationary_laws_obey_harmonic_bound():
    order, t, harmonics = 15, Q(1, 20), 3
    residuals, slopes = np.array([0, 2, 4]), np.array([1, 3, 5])
    truncated = target.harmonic_line_log_weights(residuals, slopes, order, t, harmonics)
    exact = np.array([target.product_log_weight((residuals+step*slopes) % order, order, t)
                      for step in range(order)])
    left, right = np.exp(truncated-truncated.max()), np.exp(exact-exact.max())
    left, right = left/left.sum(), right/right.sum()
    bound = target.harmonic_certificate(3, t, harmonics)["stationary_target_tv_upper"]
    assert np.sum(abs(left-right))/2 <= float(Q(bound))


def test_categorical_line_sampler_and_small_detailed_balance():
    probs = target.categorical_line_probabilities([0.0, 2.0, -1.0], beta=0.5)
    assert probs.sum() == pytest.approx(1.0)
    assert probs[1] > probs[0] > probs[2]
    with pytest.raises(ValueError, match="beta"):
        target.categorical_line_probabilities([0.0, 1.0], beta=0.0)
    rng = random.Random(42)
    samples = [target.sample_categorical_step(probs, rng) for _ in range(200)]
    assert set(samples).issubset({0, 1, 2})

    small = target.small_mcmc_stationary_and_detailed_balance_control()
    assert small["states_enumerated"] == 49
    assert small["G_systematic_top_block_is_identity"]
    assert small["max_detailed_balance_violation_original_basis"] < 1e-14
    assert small["max_detailed_balance_violation_systematic_basis"] < 1e-14
    assert small["harmonic_vs_exact_stationary_tv"] <= float(Q(small["certified_stationary_tv_upper"]))
    assert small["empirical_histogram_tv_to_harmonic_stationary"] < 0.03


def test_saved_native_certificate():
    artifact = json.loads(target.REPORT.read_text())
    assert artifact["schema"] == "balanced_mpi_product_target_v2"
    assert artifact["producer_sha256"] == hashlib.sha256(
        Path(target.__file__).read_bytes()).hexdigest()
    assert artifact["balanced_source_sha256"] == hashlib.sha256(
        Path(mpi.__file__).read_bytes()).hexdigest()
    native = artifact["native_attack_target"]
    assert native == target.transfer_certificate(
        6000, 420, 209, Q(1, 20), center_model=target.CENTER_MODEL, sampler_tv=Q(1, 1000))
    assert native["active_probability"] == "1/20"
    assert native["center_model"] == target.CENTER_MODEL
    assert Q(native["center_averaged_target_tv_upper"]) < Q(18, 10000)
    assert Q(native["conditional_joint_success_lower"]) > Q(89, 10000)
    assert Q(native["truncated_quantum_mean_lower"]) > Q(308, 1000)
    original = artifact["original_pilot_comparator"]
    assert original["active_probability"] == "13/200"
    assert Q(original["conditional_joint_success_lower"]) == 0
    assert not artifact["classical_sampler_executed"]
    assert not artifact["native_optimizer_executed"]
    assert artifact["bounded_native_mcmc_and_mode_campaign_executed"]
    assert not artifact["dequantization_claim_admitted"]
    line = artifact["native_line_control"]
    assert line["certificate"] == target.harmonic_certificate(6000, Q(1, 20), 9)
    assert line["all_line_values_computed"] == 8191
    assert not line["classical_sampler_executed"]
    assert line["maximum_checked_log_error"] < float(Q(
        line["certificate"]["uniform_log_weight_error_upper"]))

    campaign = artifact["native_product_target_campaign"]
    assert campaign["center_seed"] == 20261020
    assert campaign["center_sha256"] == line["center_sha256"]
    assert not campaign["mixing_time_certified"]
    assert not campaign["any_chain_reached_0_3_threshold"]
    assert campaign["best_mean_cosine"] > 0.117
    chains_by_name = {c["name"]: c for c in campaign["chains"]}
    assert chains_by_name["cold_original_coordinate_heatbath_from_pinned_I0"]["nontrivial_moves_accepted"] == 0
    assert chains_by_name["systematic_basis_heatbath_I0"]["nontrivial_moves_accepted"] > 0
    assert chains_by_name["two_replica_tempered_systematic_chain_I0"]["accepted_replica_exchanges"] > 0

    supports, evaluations = mpi.points(13, 6000, 420)
    rng = random.Random(20261020)
    centers = np.array([rng.randrange(8191) for _ in range(6000)], dtype=np.int64)
    for chain in campaign["chains"]:
        x = chain["best_assignment"]
        assert len(x) == 420
        vals = np.array(mpi.fast_public_matvec(13, supports, evaluations, x), dtype=np.int64)
        res = (vals - centers) % 8191
        assert float(np.cos(2*np.pi*res/8191).mean()) == pytest.approx(chain["best_mean_cosine"], abs=1e-12)
        assert target.product_log_weight(res, 8191, Q(1, 20)) == pytest.approx(
            chain["best_product_log_weight"], abs=1e-9)

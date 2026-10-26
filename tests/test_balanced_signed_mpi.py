from fractions import Fraction as Q
from itertools import product
import json

import numpy as np
import pytest

from theorems import balanced_signed_mpi as work


@pytest.mark.parametrize("trials", range(7))
def test_exact_multinomial_against_full_ternary_enumeration(trials):
    t = Q(2, 5)
    for plus_cap in range(3):
        for minus_cap in range(3):
            expected = sum(((t/2)**sum(x != 0 for x in word)
                            *(1-t)**sum(x == 0 for x in word)
                            for word in product((-1, 0, 1), repeat=trials)
                            if word.count(1) <= plus_cap and word.count(-1) <= minus_cap), Q(0))
            assert work.multinomial_box(trials, plus_cap, minus_cap, t) == expected


def test_mean_formula_by_explicit_ternary_edges():
    m, cap, t = 5, 2, Q(1, 3)
    words = [y for y in product((-1, 0, 1), repeat=m)
             if y.count(1) <= cap and y.count(-1) <= cap]
    Z = work.multinomial_box(m, cap, cap, t)
    weights = {y: float((t/2)**sum(x != 0 for x in y)
                       *(1-t)**sum(x == 0 for x in y)/Z)**.5 for y in words}
    observed = 0.
    for y in words:
        for i in range(m):
            for sign in (-1, 1):
                target = list(y)
                target[i] += sign
                observed += .5*weights[y]*weights.get(tuple(target), 0)/m
    cert = work.mean_certificate(m, 6, cap, t)
    assert observed == pytest.approx(float(Q(cert["mean_cosine_lower"])), abs=1e-13)


@pytest.mark.parametrize("bits,prime", [(3, True), (4, False)])
def test_prime_and_composite_target_state_and_decoder(bits, prime):
    result = work.small_control(bits)
    assert result["order_is_prime"] is prime
    assert result["decoded_patterns"] == 21
    assert result["observable_pairs_checked"] == 3528
    assert result["target_norm"] == pytest.approx(1., abs=2e-13)
    assert result["target_mean_cosine"] == pytest.approx(
        float(Q(result["source_mean_interval"][0])), abs=2e-13)


def test_moment_guard_has_real_counterexample():
    result = work.readout_alias_control()
    assert result["box_injective"]
    assert result["shifted"] != result["different_box_pattern"]
    assert work.license_box(3, 1, 1, 0)["strict_root_bound_required"] == 3
    with pytest.raises(ValueError, match="separation"):
        work.license_box(3, 1, 1, 1)
    assert work.license_box(4, 1, 1, 1)["strict_root_bound_required"] == 4


def test_decoder_rejects_unsupported_box_and_zero_field_truthiness_regression():
    t, z = work.points(4, 5, 4)
    y = (1, -1, 0, 0, 0)
    assert work.decode(4, t, z, work.syndrome(4, t, z, y), 1) == y
    outside = (1, 1, 0, 0, 0)
    assert work.decode(4, t, z, work.syndrome(4, t, z, outside), 1) is None
    with pytest.raises(ValueError, match="separation"):
        work.decode(4, t, z[:2], (0, 0), 1)
    with pytest.raises(ValueError, match="canonical"):
        work.decode(4, t, z, (15, 0, 0, 0), 1)
    with pytest.raises(ValueError, match="disjoint"):
        work.syndrome(4, t, (0, 5, 6, 7), y)


def test_every_two_cap_pattern_including_unbalanced_signs():
    t, z = work.points(4, 5, 6)
    for y in product((-1, 0, 1), repeat=5):
        if y.count(1) <= 2 and y.count(-1) <= 2:
            assert work.decode(4, t, z, work.syndrome(4, t, z, y), 2) == y


def test_empty_pattern_and_invalid_contracts():
    t, z = work.points(4, 4, 4)
    assert work.decode(4, t, z, (0,)*4, 1) == (0,)*4
    assert work.multinomial_box(3, -1, 1, Q(1, 2)) == 0
    assert Q(work.mean_certificate(5, 2, 0, Q(1, 3))["mean_cosine_lower"]) == 0
    with pytest.raises(ValueError):
        work.multinomial_box(3, 1, 1, .5)
    with pytest.raises(ValueError):
        work.points(3, 5, 4)


@pytest.mark.parametrize("bits", [3, 4])
def test_classical_walsh_convolution_against_dense_matrix(bits):
    order = (1 << bits)-1
    _, logs, _ = work.presentation(bits)
    vector = tuple((3*i*i+2*i-7) % order for i in range(order+1))
    expected = tuple(sum((logs[a ^ b] if a != b else 0)*x for b, x in enumerate(vector)) % order
                     for a in range(order+1))
    assert work.log_cauchy_product(bits, vector) == expected
    assert work.spectrum_control(bits)["zero_eigenvalues_of_full_completion"] == 2
    assert work.walsh(work.walsh(vector, order), order) == list(vector)
    with pytest.raises(ValueError, match="power-of-two"):
        work.walsh([1, 2, 3], order)


def test_fast_public_matvec_and_composite_module_invariants():
    sup, ev = work.points(4, 8, 4)
    _, logs, _ = work.presentation(4)
    B = np.array([[logs[t ^ z] for z in ev] for t in sup], dtype=np.int64)
    x = [3, 11, 7, 14]
    assert work.fast_public_matvec(4, sup, ev, x) == tuple(((B @ np.array(x)) % 15).tolist())

    comp = work.module_and_rank_audit(4, 8, 4)
    assert not comp["order_is_prime"]
    assert comp["Z_N_smith_invariant_factors"] == [1, 1, 1, 3]
    assert not comp["free_rank_n_submodule_over_Z_N"]
    assert not comp["invertible_n_by_n_information_set_exists"]
    witness = comp["nonzero_nonunit_determinant_witness"]
    assert witness["determinant_mod_N"] == 6
    assert witness["gcd_with_N"] == 3
    assert not witness["invertible_over_Z_N"]

    prime_mod = work.module_and_rank_audit(3, 4, 4)
    assert prime_mod["order_is_prime"]
    assert prime_mod["field_rank"] == 4
    assert prime_mod["Z_N_smith_invariant_factors"] == [1, 1, 1, 1]


def test_native_exact_mean_syndrome_replay_and_matched_portfolio():
    report = json.loads(work.REPORT.read_text())
    assert report["schema"] == "balanced_signed_mpi_v2"
    assert report["producer_sha256"] == work.hashlib.sha256(work.Path(work.__file__).read_bytes()).hexdigest()
    cert = work.mean_certificate(6000, 420, 209, Q(13, 200))
    assert cert == report["native_mean"]
    assert Q(cert["mean_cosine_lower"]) > Q(342, 1000)
    assert Q(cert["old_radial_degree_cap_mean_upper"]) < Q(26, 100)
    assert Q(cert["normalization_lower"]) > Q(72, 100)
    assert Q(cert["ideal_tail"]["probability_lower"]) > Q(6, 100)
    native = report["native_decoder"]
    error = [0]*6000
    for i in native["positive_positions"]:
        error[i] = 1
    for i in native["negative_positions"]:
        assert error[i] == 0
        error[i] = -1
    supports, evaluations = tuple(native["support_points"]), tuple(native["evaluation_points"])
    observed = work.syndrome(13, supports, evaluations, tuple(error))
    assert observed == tuple(native["syndrome"])
    assert work.decode(13, supports, evaluations, observed, 209) == tuple(error)
    assert native["positive_errors"]+native["negative_errors"] == 380 > 209
    assert not native["optimizer_matrix_rank_claimed"]

    portfolio = report["matched_classical_portfolio"]
    assert portfolio["module_and_rank"]["field_rank"] == 420
    assert portfolio["module_and_rank"]["first_n_rows_invertible_over_Z_N"]
    assert portfolio["composite_module_control"]["Z_N_smith_invariant_factors"] == [1, 1, 1, 3]
    assert portfolio["fast_matvec_crosschecked_against_explicit_matrix"]
    assert portfolio["all_runs_and_nonimproving_controls_retained"]
    assert portfolio["full_m_row_objective_scored_on_every_candidate"]
    assert 0.11 < portfolio["best_mean_cosine"] < portfolio["target_threshold"]
    assert not portfolio["threshold_reached"]
    assert not portfolio["classical_hardness_or_quantum_speedup_proved"]
    assert not report["asymptotic"]["Mersenne_prime_infinitude_assumed"]
    assert not report["quantum_optimizer_executed"]
    assert not report["speedup_claim_admitted"]
    assert work.spectrum_control(13) == report["classical_spectrum"][-1]

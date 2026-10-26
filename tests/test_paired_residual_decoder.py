from fractions import Fraction as Q
from itertools import product
import json

import numpy as np
import pytest

from theorems import paired_residual_decoder as f


def test_two_syndrome_rows_are_one_original_polynomial_not_two_copies():
    p, M, n = 13, 6, 8
    left, right = (0, 1, 3, 0, 9, 5), (2, 0, 7, 0, 1, 4)
    rows = f.pair_syndrome(p, M, n, left, right)
    error = [0]*(p-1)
    for i, (u, v) in enumerate(zip(left, right), 1):
        error[i-1], error[p-i-1] = u, v
    scalar = f.syndrome(p, error, n)
    assert scalar[::2] == rows[0]
    assert scalar[1::2] == rows[1]


@pytest.mark.parametrize("allowed", [(0, 1, 2), (1, 2, 4), (2, 4, 5)])
@pytest.mark.parametrize("multiplier", [1, 3, 6])
def test_actual_fixed_predicate_fourier_law_has_uniform_left_and_nonzero_right(allowed, multiplier):
    p = 7
    _, coefficients = f.local_fourier(p, multiplier, allowed)
    indicator = np.isin(np.arange(p), allowed).astype(float)
    rho = len(allowed)/p
    one = np.fft.fft((indicator-rho)/np.sqrt(rho*(1-rho)))/p
    assert np.max(abs(coefficients[:, 0])) < 1e-15
    assert np.allclose(abs(coefficients)**2, abs(one)[None, :]**2/p, atol=1e-15)
    assert abs(np.sum(abs(coefficients)**2)-1) < 1e-14


def test_exhaustive_small_source_rank_bound_and_invalid_frequency_countercontrol():
    result = f.rank_control()
    for row in result["rows"][:2]:
        assert row["failed"] == 10
        assert Q(row["actual_failure_exact"]) == Q(10, 121)
        assert Q(row["actual_failure_exact"]) <= Q(result["proved_upper_for_nonzero_right"])
    invalid = result["rows"][-1]
    assert not invalid["satisfies_nonzero_right_premise"]
    assert Q(invalid["actual_failure_exact"]) > Q(result["proved_upper_for_nonzero_right"])


def test_bounded_actual_decoder_failure_exactly_matches_the_cap_rank_event():
    p, M, n, cap = 11, 5, 8, 3
    passed = failed = 0
    for u, w in product(range(p), repeat=2):
        left, right = [u, w, 0, 0, 0], [2, 7, 0, 0, 0]
        result = f.decode_pairs(p, M, n, cap, f.pair_syndrome(p, M, n, left, right))
        rank_good = f.cap_rank(p, n, cap, (1, 2), (u, w), (2, 7)) == 2
        if rank_good:
            assert result["status"] == "VERIFIED_UNIQUE_PAIR_LABEL"
            assert (result["left"], result["right"]) == (left, right)
            assert result["decoder"]["whole_cap_uniqueness_certified"]
            assert result["extra_quantum_copies"] == 0
            passed += 1
        else:
            assert result["status"] == "ABSTAIN"
            failed += 1
    assert (passed, failed) == (111, 10)


def test_decoder_does_not_narrow_the_uniqueness_ball_to_pilot_right_nonzero():
    left, right = [3, 0, 0, 0, 0], [0]*5
    rows = f.pair_syndrome(11, 5, 8, left, right)
    result = f.decode_pairs(11, 5, 8, 3, rows)
    assert result["status"] == "VERIFIED_UNIQUE_PAIR_LABEL"
    assert result["left"] == left and result["right"] == right


def test_zero_error_and_corrupt_syndromes_do_not_return_an_unchecked_original():
    rows = f.pair_syndrome(11, 5, 8, [0]*5, [0]*5)
    result = f.decode_pairs(11, 5, 8, 3, rows)
    assert result["status"] == "VERIFIED_UNIQUE_PAIR_LABEL"
    rows[0][-1] = 1
    assert f.decode_pairs(11, 5, 8, 3, rows)["status"] == "ABSTAIN"


def test_observable_radius_is_paid_and_unknown_regime_raises():
    record = f.score_certificate()
    assert record["observable_guard_cap"] == record["degree"]+1
    assert record["cap_equations"] == 68
    assert Q(record["rank_failure_upper_exact"]) < Q(246, 10**9)
    assert Q(record["one_attempt_mean_lower_ABORT_score_zero"]) > Q(7322, 10000)
    assert Q(record["one_attempt_tail_lower_exact"]) > Q(108, 1000)
    assert record["ordinary_pairwise_guarantee_degree"] == 50
    assert Q(record["ordinary_pairwise_source_Rayleigh"]["ambient_Rayleigh_upper_exact"]) < Q(701, 1000)
    assert not record["full_unheralded_target_filter_law_claimed"]
    assert not record["classical_separation_or_novelty_claimed"]
    with pytest.raises(ValueError, match="enough cap equations"):
        f.failure_bound(2053, 204, 68, 69)


def test_union_bound_includes_projective_nullvectors_not_just_determinant_degree():
    # m=2, two columns. The projective support count is p+1.
    assert f.failure_bound(11, 8, 2, 3) == Q(12, 121)
    assert f.failure_bound(11, 8, 1, 3) == 0
    assert f.failure_bound(11, 8, 0, 3) == 0


def test_sparse_fourier_expectation_aggregates_aliases_and_matches_dense_qft():
    p = 3
    labels = [[0, 0], [1, 1], [1, 1], [2, 1]]
    amplitude = np.array([0.3, 0.2+0.1j, 0.1-0.2j, 0.4j])
    observable = np.array([[0, 1, 0], [1, 1, 0], [0, 0, 1]])
    hat = np.fft.fft2(observable)/p**2
    shifts = [(list(x), hat[x]) for x in product(range(p), repeat=2)]
    norm, moment = f.sparse_expectation(p, labels, amplitude, shifts)
    Fourier = np.zeros((p, p), dtype=complex)
    for label, value in zip(labels, amplitude):
        Fourier[tuple(label)] += value
    state = np.fft.ifft2(Fourier)*p
    assert abs(norm-np.sum(abs(state)**2)) < 1e-14
    assert abs(moment-np.sum(observable*abs(state)**2)) < 1e-14


@pytest.mark.parametrize("args", [(11, 6, 8), (11, 5, 7), (11, 5, 12), (9, 4, 6)])
def test_bad_public_domains_fail_closed(args):
    with pytest.raises(ValueError):
        f.parameters(*args)


def test_saved_native_decoder_and_guarded_observable_are_real_evidence():
    if not f.REPORT.exists():
        pytest.skip("live producer artifact not generated yet")
    result = json.loads(f.REPORT.read_text())
    native = result["native"]
    assert native["decoder"]["status"] == "VERIFIED_UNIQUE_PAIR_LABEL"
    assert native["decoder"]["left"] == native["source_left"]
    assert native["decoder"]["right"] == native["source_right"]
    assert native["actual_scalar_weight"] > 102
    assert native["ordinary_scalar_decoder_status"] != "VERIFIED_UNIQUE_BURST"
    assert native["bad_source_control_status"] == "ABSTAIN"
    control = result["guarded_observable_control"]
    assert abs(control["source_norm"]-1) < 1e-12
    assert abs(control["unguarded_target_norm"]-1) < 1e-12
    assert control["unsafe_mean_transfer_error"] > 1e-8
    assert control["guarded_mean_identity_error"] < 1e-12
    assert abs(control["kept_source_norm"]-control["kept_target_norm"]) < 1e-12
    assert abs(control["rejected_mass"]-float(Q(control["known_failure_mass_exact"]))) < 1e-12
    assert native["published_chain_scores_NOT_comparable"]
    assert native["one_information_set_comparator"]["strong_classical_portfolio_NOT_run"]
    assert not result["accepted_speedup_candidate"]

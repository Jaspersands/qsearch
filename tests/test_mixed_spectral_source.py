"""Exact spectral and finite-matrix controls, not copies-only source execution."""
from fractions import Fraction as F
from itertools import product

import numpy as np
import pytest

from theorems.mixed_spectral_source import (
    SpectralGridPlan, flag_preparation_caps, reference_bad_offsets, reference_profile,
)


@pytest.mark.parametrize("spectrum", [
    (F(1), F(0)), (F(1, 2), F(1, 2)), (F(1, 2), F(1, 3), F(1, 6)),
    (F(1, 2), F(1, 4)+F(1, 2**80), F(1, 4)-F(1, 2**80)),
    (F(1, 2), F(1, 2)-F(1, 2**100), F(1, 2**100), F(0)),
])
def test_grid_union_bound_and_exact_layer_cake_on_all_offsets(spectrum):
    rank = sum(x > 0 for x in spectrum)
    plan = SpectralGridPlan(rank, F(1, 2), F(1, 2))
    bad = reference_bad_offsets(plan, spectrum)
    assert len(bad) <= rank
    assert F(len(bad), plan.offset_count) <= plan.offset_failure_bound <= plan.failure_budget/8
    for offset in range(plan.offset_count):
        profile = reference_profile(plan, spectrum, offset)
        assert profile["good_offset"] == (offset not in bad)
        assert 0 <= profile["trace_residual"] < plan.trace_gap/8
        assert profile["trace_rounded"]+profile["trace_residual"] == 1
        assert all(0 <= y <= x for x, y in zip(spectrum, profile["rounded_eigenvalues"]))
        flags = profile["distinct_flags"]
        assert [x["rank"] for x in flags] == sorted({x["rank"] for x in flags}, reverse=True)
        assert len(flags) <= rank
        assert profile["physical_registers_per_flag_product"] <= min(rank*(rank+1)//2, 1/plan.width)
        for flag in flags:
            retained = [x for x in spectrum if x >= flag["threshold"]]
            mass = sum(retained)
            assert mass >= plan.width
            assert min(x/mass for x in retained) >= plan.width


def test_single_bad_offset_and_threshold_boundary_are_not_heralded_certificates():
    plan = SpectralGridPlan(1, F(1, 2), F(1, 4))
    assert 0 in reference_bad_offsets(plan, [F(1)])
    assert not reference_profile(plan, [F(1)], 0)["good_offset"]
    # The rounding identity still holds on the bad offset; it is filter
    # implementation precision, not symmetry preservation, which needs margin.
    assert plan.rounded_eigenvalue(F(1), 0) == 1


def test_one_extra_grid_period_is_not_required_and_zero_is_never_near_threshold():
    plan = SpectralGridPlan(2, F(2, 3), F(1, 10))
    for offset in (0, plan.offset_count-1):
        assert plan.threshold(offset, 0) >= plan.width > plan.spectral_margin
        assert plan.threshold(offset, plan.threshold_count-1) >= 1
        assert plan.rounded_eigenvalue(F(0), offset) == 0


def test_weighted_spectrum_estimator_counts_multiplicity_not_probability_mass():
    spectrum = (F(1, 2), F(1, 4), F(1, 4))
    plan = SpectralGridPlan(3, F(1, 4), F(1, 8))
    profile = reference_profile(plan, spectrum, plan.offset_count//2)
    for flag in profile["distinct_flags"]:
        threshold = flag["threshold"]
        expectation = sum(x*(1/x if x >= threshold else 0) for x in spectrum)
        assert expectation == flag["rank"]
    assert sum(x for x in spectrum) == 1 and len(spectrum) == 3


def test_rank_estimator_bias_and_hoeffding_schedule_are_paid():
    spectrum = (F(1, 2), F(1, 3), F(1, 6))
    plan = SpectralGridPlan(3, F(1, 4), F(1, 8))
    profile = reference_profile(plan, spectrum, plan.offset_count//2)
    assert profile["good_offset"]
    nu, kappa = plan.rank_estimation_precision, plan.rank_estimation_tail
    assert nu <= plan.spectral_margin/2
    for signs in product((-1, 1), repeat=3):
        estimates = [x+s*nu for x, s in zip(spectrum, signs)]
        for flag in profile["distinct_flags"]:
            threshold = flag["threshold"]
            expectation = sum(x*(1/y if y >= threshold else 0)
                              for x, y in zip(spectrum, estimates))
            # Worst-case contamination of the bounded statistic on PE failure.
            assert abs(expectation-flag["rank"])+kappa/plan.width < F(1, 32)
    exponent = plan.rank_training_samples*plan.width**2/128
    assert 2**exponent.__floor__() >= 2*plan.threshold_count/plan.failure_budget


def _unitary(d, seed):
    rng = np.random.default_rng(seed)
    return np.linalg.qr(rng.normal(size=(d, d))+1j*rng.normal(size=(d, d)))[0]


def _td(a, b):
    return np.linalg.svd(a-b, compute_uv=False).sum()/2


def test_joint_flag_gap_for_noncommuting_actions_and_hidden_eigenbasis():
    spectrum = (F(1, 2), F(1, 3), F(1, 6), F(0))
    plan = SpectralGridPlan(3, F(1, 8), F(1, 8))
    profile = reference_profile(plan, spectrum, plan.offset_count//2)
    basis = _unitary(4, 29)
    rho = (basis*np.array(list(map(float, spectrum)))) @ basis.conj().T
    rounded = (basis*np.array(list(map(float, profile["rounded_eigenvalues"])))) @ basis.conj().T
    checked = 0
    for seed in range(12):
        action = _unitary(4, seed)
        td = _td(rho, action @ rho @ action.conj().T)
        if td < float(plan.trace_gap):
            continue
        overlap = 1.0
        for flag in profile["distinct_flags"]:
            frame = basis[:, [i for i, x in enumerate(spectrum) if x >= flag["threshold"]]]
            overlap *= abs(np.linalg.det(frame.conj().T @ action @ frame))
        assert 1-overlap >= float(plan.joint_overlap_gap)-1e-12
        assert _td(rounded, action @ rounded @ action.conj().T) >= td-float(profile["trace_residual"])-1e-12
        checked += 1
    assert checked >= 8
    action = (basis*np.exp(1j*np.arange(4))) @ basis.conj().T
    assert _td(rho, action @ rho @ action.conj().T) < 1e-12
    for flag in profile["distinct_flags"]:
        frame = basis[:, [i for i, x in enumerate(spectrum) if x >= flag["threshold"]]]
        assert abs(np.linalg.det(frame.conj().T @ action @ frame)) == pytest.approx(1)


def test_global_gap_promise_is_essential_to_exact_symmetry_preservation():
    tiny = F(1, 2**80)
    spectrum = (F(1, 3)+tiny, F(1, 3), F(1, 3)-tiny)
    plan = SpectralGridPlan(3, F(1, 4), F(1, 8))  # Deliberately FALSE gap.
    profile = reference_profile(plan, spectrum, plan.offset_count//2)
    assert len(set(profile["rounded_eigenvalues"])) == 1
    assert len(set(spectrum)) == 3
    cyclic_gap = sum(abs(spectrum[i]-spectrum[(i+1) % 3]) for i in range(3))/2
    assert 0 < cyclic_gap < plan.trace_gap


@pytest.mark.parametrize("ranks", [(1,), (3, 1), (4, 3, 2, 1)])
def test_caps_cover_initial_copies_failures_and_all_components(ranks):
    plan = SpectralGridPlan(4, F(1, 2), F(1, 16))
    cap = flag_preparation_caps(plan, ranks, 7)
    assert cap["filtered_inputs_cap"] == 7*len(ranks)+cap["growth_attempt_cap"]
    assert cap["filter_target_copy_cap"] == cap["filtered_inputs_cap"]*cap["filter_trials_per_input"]
    assert cap["growth_abort_bound"] <= plan.failure_budget
    assert cap["filter_abort_bound"] <= plan.failure_budget
    assert cap["controlled_original_actions_per_product"] == sum(ranks)
    assert not cap["dme_program_copies_included"] and not cap["quantum_preparer_implemented"]


@pytest.mark.parametrize("ranks", [(), (2, 2), (1, 3), (True,), (0,), (5,)])
def test_wrong_rank_flags_rejected(ranks):
    with pytest.raises(ValueError):
        flag_preparation_caps(SpectralGridPlan(4, F(1), F(1, 2)), ranks, 1)


@pytest.mark.parametrize("rank,gap,beta", [(True, F(1), F(1)), (0, F(1), F(1)),
                                         (2, 0.5, F(1)), (2, F(0), F(1)),
                                         (2, F(2), F(1)), (2, F(1), 0.1)])
def test_invalid_public_plans(rank, gap, beta):
    with pytest.raises(ValueError):
        SpectralGridPlan(rank, gap, beta)


def test_reference_caps_and_false_rank_promise_are_not_silently_ignored():
    plan = SpectralGridPlan(1, F(1, 100), F(1, 100))
    with pytest.raises(ValueError, match="threshold enumeration"):
        reference_profile(plan, [F(1)], 0, max_thresholds=10)
    with pytest.raises(ValueError, match="offset enumeration"):
        reference_bad_offsets(plan, [F(1)], max_offsets=10)
    with pytest.raises(ValueError, match="trace or rank"):
        reference_profile(plan, [F(1, 2), F(1, 2)], 0)
    with pytest.raises(ValueError, match="offset"):
        plan.threshold(plan.offset_count, 0)

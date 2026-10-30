from fractions import Fraction as F
import math

import mpmath as mp
import numpy as np
import pytest

from flux_gap import (Interval, ceil_log2, coherent_ledger, conditional, exp_interval,
    gap_certificate, log_interval, log_partition, pi_interval, sample_flux, source)
from flux_controls import (coherent_control, finite_control, flux_table,
                           pilot_from_flux, trace_word_control,
                           line_graph_positivity_falsifier, gaussian_decomposition_control)
from audit_controls import dense_pilot


ROOTS = [
    (4, [(0, 1), (1, 2), (2, 3), (3, 0)]),
    (4, [(0, 1), (1, 2), (2, 0), (2, 3), (3, 0)]),
    (4, [(i, j) for i in range(4) for j in range(i + 1, 4)]),
    (6, [(0, 1), (1, 2), (2, 0), (3, 4), (4, 5), (5, 3)]),
    (5, [(i, j) for i in range(5) for j in range(i + 1, 5)]),
]


def mp_fraction(q):
    return mp.mpf(q.numerator) / q.denominator


@pytest.mark.parametrize("tolerance", [F(1, 16), F(1, 1024), F(1, 1 << 40)])
def test_pi_certificate(tolerance):
    with mp.workdps(100):
        bounds = pi_interval(tolerance)
        assert mp_fraction(bounds.lo) < mp.pi < mp_fraction(bounds.hi)
        assert bounds.width <= tolerance


@pytest.mark.parametrize("x", [F(1), F(1, 1000), F(9, 7), F(2), F(1 << 300), F(1, 1 << 300)])
def test_log_certificate(x):
    with mp.workdps(150):
        bounds = log_interval(x, F(1, 1 << 35))
        expected = mp.log(mp_fraction(x))
        assert mp_fraction(bounds.lo) <= expected <= mp_fraction(bounds.hi)
        assert bounds.width <= F(1, 1 << 35)


@pytest.mark.parametrize("x", [F(-1), F(-1, 4), F(0), F(1, 7), F(1)])
def test_exponential_certificate(x):
    with mp.workdps(100):
        bounds = exp_interval(x, F(1, 1 << 30))
        assert mp_fraction(bounds.lo) <= mp.exp(mp_fraction(x)) <= mp_fraction(bounds.hi)
        assert bounds.width <= F(1, 1 << 30)


@pytest.mark.parametrize("n,edges", ROOTS)
@pytest.mark.parametrize("beta", [F(0), F(1, 32), F(1, 8)])
def test_all_fluxes_mixing_gap_and_parent(n, edges, beta):
    src = source(n, edges)
    data = finite_control(src, beta)
    assert data["max_mixed_difference_column_sum"] <= data["analytic_influence_bound"] + 1e-12
    assert data["max_conditional_influence_column_sum"] <= data["analytic_influence_bound"] + 1e-12
    assert data["gap"] >= data["analytic_gap_lower"] - 1e-12
    for name in ("ground_residual", "parent_similarity_error", "stationarity_error",
                 "row_normalization_error"):
        assert data[name] < 1e-12


@pytest.mark.parametrize("flux", range(4))
def test_trace_word_lemma_at_common_resolvent(flux):
    src = source(*ROOTS[1])
    data = trace_word_control(src, flux, F(1, 16), max_length=7)
    assert data["max_trace_bound_excess"] < 1e-12
    assert data["max_cross_block_sum"] <= data["cross_block_bound"] + 1e-12
    assert data["resolvent_norm"] <= 1 + 1e-12


@pytest.mark.parametrize("flux", range(8))
def test_certified_native_log_partition(flux):
    src = source(*ROOTS[2], [F(1), F(-1, 3), F(1, 2), F(0), F(3, 4), F(1, 5)])
    bounds = log_partition(src, F(1, 8), flux, F(1, 1024))
    expected = float(flux_table(src, F(1, 8))[flux])
    assert float(bounds["interval"].lo) <= expected <= float(bounds["interval"].hi)
    assert bounds["interval"].width <= F(1, 1024)
    assert bounds["determinant_dimension"] == 4


@pytest.mark.parametrize("bit", range(3))
def test_certified_conditionals_have_same_value_for_both_old_bits(bit):
    src = source(*ROOTS[2])
    result = conditional(src, F(1, 8), 0, bit, F(1, 256))
    other = conditional(src, F(1, 8), 1 << bit, bit, F(1, 256))
    assert result == other
    logs = flux_table(src, F(1, 8))
    expected = 1 / (1 + math.exp(logs[0] - logs[1 << bit]))
    assert float(result["interval"].lo) <= expected <= float(result["interval"].hi)
    assert result["interval"].width <= F(1, 256)


def test_certified_access_does_not_use_eigenvalue_or_sector_table(monkeypatch):
    import fermion_sampler
    monkeypatch.setattr(fermion_sampler, "matrix_function", lambda *_: pytest.fail("float oracle"))
    src = source(*ROOTS[0])
    data = sample_flux(src, F(1, 8), F(1, 2), seed=19)
    assert data["native_conditional_access"]
    assert data["steps"] == 3 and data["determinants"] == 36
    assert data["tv_bound"] == F(1, 2)
    assert data["seeded_reproducibility_control"]
    assert data["tv_bound_assumes_independent_random_bits"]


def test_coherent_composition_preserves_signed_native_state():
    src = source(*ROOTS[1])
    logs = flux_table(src, F(1, 8))
    state = np.exp(logs / 2)
    state /= np.linalg.norm(state)
    assembled = pilot_from_flux(src, F(1, 8), state)
    native = dense_pilot(src.topology, 1 / 8)
    assert np.linalg.norm(assembled - native) < 1e-12


@pytest.mark.parametrize("flux", range(8))
@pytest.mark.parametrize("beta", [F(0), F(1, 8)])
def test_gaussian_pair_construction_fixes_each_sector_phase(flux, beta):
    src = source(*ROOTS[2], [1, F(-1, 2), 1, F(1, 3), 0, -1])
    data = gaussian_decomposition_control(src, beta, flux)
    assert data["phase_sensitive_vector_error"] < 1e-12
    assert data["norm_error"] < 1e-12
    assert data["vacuum_amplitude_positive"]
    assert not data["global_phase_alignment_used"]


def test_gaussian_pair_construction_odd_modes_degenerate_blocks():
    data = gaussian_decomposition_control(source(5, [(0,1),(1,2),(2,3),(3,0)]), F(1,8), 1)
    assert data["phase_sensitive_vector_error"] < 1e-12
    assert data["vacuum_amplitude_positive"]


def test_finite_adiabatic_control_not_a_hardware_claim():
    data = coherent_control(source(*ROOTS[1]), F(1, 8), time=32, slices=128)
    assert data["dense_simulation_not_quantum_execution"]
    assert data["flux_trace_distance"] < 1e-5
    assert data["native_pilot_vector_error_up_to_global_phase"] < 1e-5
    assert abs(data["native_pilot_norm"] - 1) < 1e-12
    assert not data["uniform_flux_is_exact"]


def test_extensive_cycle_rank_ledger_without_enumeration():
    # A ladder has r=k-1, hence 2^r fluxes, but input and certificate are linear.
    k = 128
    edges = [(2 * i, 2 * i + 1) for i in range(k)]
    edges += [(2 * i + a, 2 * i + a + 2) for i in range(k - 1) for a in (0, 1)]
    src = source(2 * k, edges)
    assert src.r == 127
    cert = gap_certificate(src, F(1, 32))
    assert cert["gap_lower"] > 0
    ledger = coherent_ledger(src, F(1, 32))
    assert not ledger["exponential_flux_table_required"]
    assert not ledger["quantum_execution"]
    assert ledger["conditional_rotations"] == 127 * ledger["first_order_product_steps"]
    assert ledger["conditional_interval_tolerance"] == ledger["rotation_error_budget"] / 16
    assert ledger["total_determinants_upper"] == (ledger["determinants_per_rotation"]
                                                * ledger["conditional_rotations"])
    assert ledger["determinants_are_not_elementary_gate_counts"]
    assert ledger["polynomial_in_input_requires_inverse_polynomial_gap_slack"]


@pytest.mark.parametrize("flux", range(8))
def test_common_resolvent_lemma_signed_couplings_shared_vertices(flux):
    src = source(*ROOTS[2], [F(-1), F(1, 7), F(1), F(-2, 3), F(1, 4), F(-1)])
    result = trace_word_control(src, flux, F(7), max_length=5)
    assert result["max_trace_bound_excess"] < 1e-12
    assert result["max_cross_block_sum"] <= result["cross_block_bound"] + 1e-12


def test_zero_temperature_ledger_does_not_charge_nonzero_determinants():
    ledger = coherent_ledger(source(*ROOTS[2]), F(0))
    assert ledger["total_determinants_upper"] == 0
    assert ledger["first_derivative_bound"] == ledger["second_derivative_bound"] == 0


@pytest.mark.parametrize("time", [F(1, 64), F(1, 128), F(1, 256)])
def test_free_fermion_structure_does_not_restore_paired_positivity(time):
    data = line_graph_positivity_falsifier(time)
    assert F(data["activity_interval"]["hi"]) < 0
    assert data["this_root_has_existing_classical_sampler"]
    assert not data["classical_hardness_claim"]


def test_zero_and_forest_cases():
    src = source(3, [(0, 1), (1, 2)])
    assert gap_certificate(src, F(10))["status"] == "NO_FLUX_BITS"
    assert sample_flux(src, F(10))["steps"] == 0
    cyclic = source(*ROOTS[0], [0, 0, 0, 0])
    assert log_partition(cyclic, F(10), 0)["interval"] == Interval(F(0), F(0))
    assert conditional(cyclic, F(1, 8), 0, 0)["interval"] == Interval(F(1, 2), F(1, 2))


def test_out_of_regime_and_work_caps_are_not_admitted():
    src = source(*ROOTS[2])
    assert gap_certificate(src, F(1, 4))["status"] == "INCONCLUSIVE"
    with pytest.raises(ValueError, match="mixing bound"):
        sample_flux(src, F(1, 4))
    with pytest.raises(RuntimeError, match="INCONCLUSIVE"):
        log_partition(src, F(1, 8), 0, F(1, 10000), max_terms=1)
    with pytest.raises(ValueError, match="capped"):
        flux_table(source(6, [(i, j) for i in range(6) for j in range(i + 1, 6)]), F(1, 8))


@pytest.mark.parametrize("bad", [0.125, True, "1/8"])
def test_no_silent_float_native_inputs(bad):
    with pytest.raises(ValueError):
        gap_certificate(source(*ROOTS[0]), bad)
    with pytest.raises(ValueError):
        source(2, [(0, 1)], [bad])


@pytest.mark.parametrize("x,answer", [(F(1), 0), (F(2), 1), (F(3), 2), (F(8), 3), (F(9), 4)])
def test_exact_bit_budget(x, answer):
    assert ceil_log2(x) == answer

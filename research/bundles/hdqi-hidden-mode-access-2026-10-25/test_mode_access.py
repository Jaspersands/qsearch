from fractions import Fraction as Q
from itertools import combinations

import networkx as nx
import numpy as np
import pytest
import sympy as sp

from controls import (audit, continuous_filter, dense_modes, filtered_audit,
                      hermitian_polar, midpoint_filter, native_matrices,
                      prepare_matrix, reference_matrix)
from mode_access import (Inconclusive, Interval, X, certify, evaluate,
                         dyadic_enclosure, independence_polynomial, point,
                         spectral_intervals, sqrt_interval)


@pytest.mark.parametrize("m,radius", [(2, 1), (5, 2), (7, 2), (8, 3), (9, 4)])
def test_independence_recurrence_against_all_subsets(m, radius):
    couplings = [Q((-1)**i, i+1) for i in range(m)]
    expected = 0
    for mask in range(1 << m):
        sites = [i for i in range(m) if mask >> i & 1]
        if all(b-a > radius for a, b in zip(sites, sites[1:])):
            weight = sp.prod(sp.Rational(couplings[i]**2) for i in sites)
            expected += (-X)**len(sites)*weight
    assert independence_polynomial(couplings, radius) == sp.Poly(expected, X)


@pytest.mark.parametrize("couplings,radius,probe", [([1]*5, 2, 1), ([1]*5, 2, 3),
    ([1]*7, 2, 3), ([1, -1, Q(1, 2), 1, -1], 2, 2), ([1]*6, 3, 4)])
def test_native_full_state_not_just_spectrum(couplings, radius, probe):
    result = audit(couplings, radius, probe)
    assert result["full_tfd_vector_error"] < 1e-10
    assert result["car_operator_error"] < 1e-10
    assert not result["quantum_execution"]


def test_non_line_graph_control():
    graph = nx.power(nx.path_graph(7), 2)
    assert nx.is_chordal(graph)
    for sites in combinations(graph, 4):
        assert sorted(dict(graph.subgraph(sites).degree()).values()) != [1, 1, 1, 3]
    with pytest.raises(nx.NetworkXError, match="not a line graph"):
        nx.inverse_line_graph(graph)


def test_thermally_inactive_mode_may_be_omitted_not_deleted_at_low_temperature():
    couplings = [Q(1, 4096)]+[1]*6
    warm = certify(couplings, 2, 3)
    cold = certify(couplings, 2, 3, beta=4096)
    assert warm["omitted_modes"] == [0]
    assert cold["omitted_modes"] == []
    result = audit(couplings, 2, 3)
    assert 0 < result["temperature_truncated_vector_error"] <= result["omitted_state_distance_bound"]


def test_zero_temperature_parameter_is_uniform_without_filters():
    result = certify([1]*7, 2, 3, beta=0)
    assert not result["active_modes"]
    assert result["omitted_state_distance_upper"] == 0


@pytest.mark.parametrize("bits", [4, 12, 32])
def test_small_probe_overlap_is_charged_despite_constant_spectral_gap(bits):
    weak = certify([Q(1, 1 << bits), 1], 1, 1)
    good = certify([Q(1, 1 << bits), 1], 1, 2)
    assert weak["filters"][0]["frequency_gap_lower"] >= 2
    assert weak["filters"][0]["polar_query_scale_not_gate_count"] >= 1 << bits
    assert good["filters"][0]["probe_weight_lower"] == 1
    assert weak["filters"][0]["filter_time"] > good["filters"][0]["filter_time"]


@pytest.mark.parametrize("probe_size", [1, 3])
def test_filter_sign_and_error_bound(probe_size):
    h, probe, modes, certificate = dense_modes([1]*5, 2, probe_size)
    for i, (energy, weight, c, d) in enumerate(modes):
        time = 500
        gap = float(certificate["filters"][i]["frequency_gap_lower"])
        bound = 4*(len(modes)+1)/(time*gap)
        assert np.linalg.norm(continuous_filter(h, probe, 2*energy, time)-weight*c, 2) <= bound
        assert np.linalg.norm(continuous_filter(h, probe, 2*energy, time, sine=True)-weight*d, 2) <= bound
        assert np.linalg.norm(continuous_filter(h, probe, 2*energy, time, sine=True)+weight*d, 2) > 0.1


def test_quadrature_omission_is_stronger_than_linear_bound_on_native_input():
    couplings = [Q(1, 1100)]*7
    result = certify(couplings, 2, 3)
    assert result["omitted_modes"] == [0, 1, 2]
    assert result["omitted_linear_state_distance_upper"] > result["error"]/8
    assert result["omitted_state_distance_upper"] <= result["error"]/8
    h, _, modes, _ = dense_modes(couplings, 2, 3)
    cos_product = np.prod([np.cos(np.arctan(np.tanh(energy/2))) for energy, *_ in modes])
    distance_squared = np.linalg.norm(prepare_matrix(modes, len(h), 1, [])-reference_matrix(h, 1))**2
    assert abs(distance_squared-2*(1-cos_product)) < 1e-14
    assert distance_squared <= float(result["omitted_squared_state_distance_upper"])


def test_transpose_and_relative_phase_are_essential():
    h, _, modes, _ = dense_modes([1]*5, 2, 3)
    rng = np.random.default_rng(187)
    raw = rng.normal(size=h.shape)+1j*rng.normal(size=h.shape)
    change, _ = np.linalg.qr(raw)
    rotated_h = change @ h @ change.conj().T
    rotated_modes = [(e, w, change @ c @ change.conj().T, change @ d @ change.conj().T)
                     for e, w, c, d in modes]
    reference = reference_matrix(rotated_h, 1)
    assert np.linalg.norm(prepare_matrix(rotated_modes, len(h), 1)-reference) < 1e-10
    assert np.linalg.norm(prepare_matrix(rotated_modes, len(h), 1, wrong_transpose=True)-reference) > 0.1


@pytest.mark.parametrize("sine", [False, True])
def test_closed_midpoint_filter_against_explicit_lcu(sine):
    h, probe = native_matrices([1]*3, 1, 2)
    values, basis = np.linalg.eigh(h)
    frequency, time, terms = 0.71, 2, 17
    direct = np.zeros_like(h)
    for j in range(terms):
        t = -time+(j+0.5)*2*time/terms
        unitary = (basis*np.exp(1j*t*values)) @ basis.conj().T
        coefficient = -np.sin(frequency*t) if sine else np.cos(frequency*t)
        direct += (2/terms)*coefficient*unitary @ probe @ unitary.conj().T
    assert np.linalg.norm(direct-midpoint_filter(h, probe, frequency, time, terms, sine), 2) < 1e-12


@pytest.mark.parametrize("probe", [1, 3])
def test_filtered_modes_prepare_full_state(probe):
    result = filtered_audit([1]*5, 2, probe)
    assert result["filtered_tfd_vector_error"] < 0.01
    assert not result["qsvt_circuit_compiled"]


def test_singular_filter_cannot_be_normalized_by_dense_reference():
    with pytest.raises(ValueError, match="singular"):
        hermitian_polar(np.zeros((2, 2)))


def test_all_analytic_filter_allowances_and_frequency_precision():
    result = certify([1]*64, 7, 8)
    for row in result["filters"]:
        allowance = result["per_mode_unitary_error_target"]*row["probe_weight_lower"]/8
        for key in ("frequency_error_bound", "window_error_bound", "quadrature_error_bound"):
            assert row[key] <= allowance
    assert result["thermal_angle_error_upper"] <= result["error"]/8
    assert not result["quantum_circuit_compiled"]
    assert not result["uniform_polynomial_parameter_bound_proved"]


def test_precision_exhaustion_is_inconclusive():
    with pytest.raises(Inconclusive):
        certify([Q(1, 1 << 32), 1], 1, 1, initial_bits=8, max_bits=8)


@pytest.mark.parametrize("value", [0, Q(1, 3), 2, Q(9, 4), Q(1, 1 << 80)])
def test_outward_square_root(value):
    interval = sqrt_interval(point(value), 64)
    assert interval.lo**2 <= value <= interval.hi**2


def test_interval_horner_encloses_values():
    polynomial = sp.Poly(3*X**3-4*X+2, X)
    enclosure = evaluate(polynomial, Interval(Q(-1), Q(2)))
    for i in range(-10, 21):
        value = polynomial.eval(sp.Rational(i, 10))
        assert enclosure.lo <= value <= enclosure.hi


@pytest.mark.parametrize("value", [Q(-1, 3), Q(1, 7), Q(1, 1 << 80)])
def test_outward_dyadic_rounding(value):
    enclosed = dyadic_enclosure(point(value), 64)
    assert enclosed.lo <= value <= enclosed.hi
    assert enclosed.width <= Q(1, 1 << 64)


@pytest.mark.parametrize("probe", [1, 3])
def test_reciprocal_residue_agrees_with_original_formula(probe):
    poly, residual, rows, _ = spectral_intervals([1]*7, 2, probe, 128)
    for row in rows:
        energy = row["energy"]
        x = (energy*energy).inverse()
        original = -evaluate(residual, x)*(x*evaluate(poly.diff(), x)).inverse()
        assert max(original.lo, row["weight_squared"].lo) <= min(original.hi, row["weight_squared"].hi)


@pytest.mark.parametrize("couplings,radius,probe", [([1., 1], 1, 1), ([0, 1], 1, 1),
    ([2, 1], 1, 1), ([1, 1], 0, 1), ([1, 1], 2, 1), ([1, 1], 1, 3)])
def test_bad_native_inputs_rejected(couplings, radius, probe):
    with pytest.raises((ValueError, TypeError)):
        certify(couplings, radius, probe)

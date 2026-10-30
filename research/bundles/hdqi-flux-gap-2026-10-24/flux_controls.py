"""Capped exponential controls; NEVER used by the rational access backend."""

from itertools import product
from fractions import Fraction as F
import math
from pathlib import Path
import sys

import numpy as np
from scipy.linalg import expm, schur
from scipy.special import expit, logsumexp

from flux_gap import gap_certificate, skew
from fermion_sampler import matrix_function, minor, pfaffian, chord_word, word_phase
from audit_controls import dense_pilot

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "hdqi-paired-positivity-2026-10-24"))
from paired_positivity import (Graph, leading_paired_coefficients,
    paired_activity_interval, power_coefficients, symmetry_zero_certificate)


def flux_table(src, beta):
    if src.r > 7:
        raise ValueError("flux table audit capped at cycle rank 7")
    return np.array([matrix_function(src.topology, float(beta), z)[2]
                     for z in range(1 << src.r)])


def parent_from_table(values, r):
    n = len(values)
    p = np.zeros((n, n))
    parent = np.zeros((n, n))
    if r == 0:
        return np.ones(1), np.ones((1, 1)), parent
    for i in range(r):
        for z0 in range(n):
            if (z0 >> i) & 1:
                continue
            z1 = z0 | (1 << i)
            one = float(expit(values[z1] - values[z0]))
            for z in (z0, z1):
                p[z, z0] += (1 - one) / r
                p[z, z1] += one / r
            parent[np.ix_([z0, z1], [z0, z1])] += np.array([
                [one, -math.sqrt(one * (1 - one))],
                [-math.sqrt(one * (1 - one)), 1 - one]]) / r
    pi = np.exp(values - logsumexp(values))
    return pi, p, parent


def finite_control(src, beta):
    values = flux_table(src, beta)
    r = src.r
    pi, p, parent = parent_from_table(values, r)
    if not r:
        return {"cycle_rank": 0, "ground_residual": 0.0}
    max_difference_sum = max_conditional_sum = 0.0
    for z in range(1 << r):
        differences = np.zeros((r, r))
        influence = np.zeros((r, r))
        for i in range(r):
            for j in range(r):
                if i == j:
                    continue
                differences[i, j] = abs(values[z] + values[z ^ (1 << i) ^ (1 << j)]
                                         - values[z ^ (1 << i)] - values[z ^ (1 << j)]) / 4
                z0 = z & ~(1 << i)
                z1 = z0 | (1 << i)
                influence[i, j] = abs(expit(values[z1] - values[z0])
                    - expit(values[z1 ^ (1 << j)] - values[z0 ^ (1 << j)]))
        assert np.all(influence <= differences + 2e-14)
        max_difference_sum = max(max_difference_sum, float(np.max(differences.sum(axis=0))))
        max_conditional_sum = max(max_conditional_sum, float(np.max(influence.sum(axis=0))))
    conjugate = np.eye(len(pi)) - np.sqrt(pi)[:, None] * p / np.sqrt(pi)[None, :]
    spectrum = np.linalg.eigvalsh(parent)
    certificate = gap_certificate(src, beta)
    return {"cycle_rank": r, "flux_states_enumerated_for_audit": 1 << r,
            "max_mixed_difference_column_sum": max_difference_sum,
            "max_conditional_influence_column_sum": max_conditional_sum,
            "analytic_influence_bound": float(certificate["influence_upper"]),
            "gap": float(spectrum[1]), "analytic_gap_lower": float(certificate["gap_lower"]),
            "ground_residual": float(np.linalg.norm(parent @ np.sqrt(pi))),
            "parent_similarity_error": float(np.max(abs(parent - conjugate))),
            "stationarity_error": float(np.max(abs(pi @ p - pi))),
            "row_normalization_error": float(np.max(abs(p.sum(axis=1) - 1)))}


def trace_word_control(src, flux, t, max_length=6):
    if src.r > 6 or max_length > 8:
        raise ValueError("literal trace-word audit cap exceeded")
    a = np.array(skew(src, flux), dtype=float)
    resolvent = np.linalg.inv(np.eye(len(a)) + float(t) * a)
    es, supports = [], []
    for e in src.topology.chords:
        u, v = src.topology.edges[e]
        b = np.zeros_like(a)
        b[u, v], b[v, u] = 1, -1
        es.append(b)
        supports.append([u, v])
    worst_excess, worst_row = 0.0, 0.0
    for i in range(src.r):
        row_bound = 0.0
        for j in range(src.r):
            if i == j:
                continue
            cross = (np.linalg.norm(resolvent[np.ix_(supports[i], supports[j])], "fro")
                     * np.linalg.norm(resolvent[np.ix_(supports[j], supports[i])], "fro"))
            row_bound += cross
            for length in range(2, max_length + 1):
                for word in product((i, j), repeat=length):
                    if len(set(word)) != 2:
                        continue
                    matrix = np.eye(len(a))
                    for letter in word:
                        matrix = matrix @ resolvent @ es[letter]
                    worst_excess = max(worst_excess, abs(float(np.trace(matrix))) - cross)
        worst_row = max(worst_row, row_bound)
    return {"max_trace_bound_excess": worst_excess, "max_cross_block_sum": worst_row,
            "cross_block_bound": 2 * src.chord_degree,
            "resolvent_norm": float(np.linalg.norm(resolvent, 2))}


def pilot_from_flux(src, beta, state):
    if len(src.topology.edges) > 8:
        raise ValueError("full pilot output audit capped at 8 generators")
    sectors = []
    for z in range(1 << src.r):
        k, _, _ = matrix_function(src.topology, float(beta), z)
        norm = math.sqrt(float(np.linalg.det(np.eye(len(k)) + k)))
        sectors.append((k, norm))
    answer = []
    for y in range(1 << len(src.topology.edges)):
        phase, x = word_phase(src.topology, y)
        c = chord_word(src.topology, y)
        value = 0j
        for z, (k, norm) in enumerate(sectors):
            coefficient = (-1j) ** (x.bit_count() // 2) * float(pfaffian(minor(k, x))) / norm
            value += (-1 if (z & c).bit_count() % 2 else 1) * state[z] * coefficient
        answer.append(value * (1j) ** (-phase) / math.sqrt(1 << src.r))
    return np.array(answer)


def gaussian_decomposition_control(src, beta, flux):
    """Dense Fock audit of pair preparation + vacuum-fixing mode rotations."""
    n = src.topology.n
    if n > 7:
        raise ValueError("Gaussian decomposition Fock audit capped at seven modes")
    k, _, _ = matrix_function(src.topology, float(beta), flux)
    blocks, modes = schur(k, output="real")
    coefficients = {0: 1+0j}
    i = 0
    while i + 1 < n:
        if abs(blocks[i, i+1]) < 1e-14:
            i += 1
            continue
        value = blocks[i, i+1]
        normalization = math.sqrt(1 + value*value)
        updated = {}
        for mask, amplitude in coefficients.items():
            updated[mask] = amplitude / normalization
            updated[mask | (3 << i)] = -1j * value * amplitude / normalization
        coefficients = updated
        i += 2
    state = np.zeros(1 << n, dtype=complex)
    for x in range(1 << n):
        occupied = [j for j in range(n) if x >> j & 1]
        for y, amplitude in coefficients.items():
            if x.bit_count() == y.bit_count():
                initial = [j for j in range(n) if y >> j & 1]
                state[x] += amplitude * np.linalg.det(modes[np.ix_(occupied, initial)])
    norm = math.sqrt(float(np.linalg.det(np.eye(n) + k)))
    target = np.array([(-1j)**(x.bit_count()//2) * float(pfaffian(minor(k, x))) / norm
                       if x.bit_count() % 2 == 0 else 0 for x in range(1 << n)])
    return {"phase_sensitive_vector_error": float(np.linalg.norm(state-target)),
            "norm_error": float(abs(np.linalg.norm(state)-1)),
            "vacuum_amplitude_positive": bool(state[0].real > 0 and abs(state[0].imag) < 1e-14),
            "global_phase_alignment_used": False,
            "dense_fock_control_not_quantum_execution": True}


def coherent_control(src, beta, time=32, slices=256):
    if src.r > 4:
        raise ValueError("dense adiabatic audit capped at cycle rank 4")
    uniform = np.ones(1 << src.r, dtype=complex) / math.sqrt(1 << src.r)
    state = uniform.copy()
    for step in range(slices):
        b = float(beta) * (step + 0.5) / slices
        _, _, parent = parent_from_table(flux_table(src, b), src.r)
        state = expm(-1j * time / slices * parent) @ state
    values = flux_table(src, beta)
    target = np.sqrt(np.exp(values - logsumexp(values)))
    native = dense_pilot(src.topology, float(beta))
    assembled = pilot_from_flux(src, beta, state)
    phase = np.vdot(native, assembled)
    aligned = assembled * np.exp(-1j * np.angle(phase))
    uniform_overlap = float(np.dot(target, uniform.real))
    return {"dense_simulation_not_quantum_execution": True, "time": time, "slices": slices,
            "flux_trace_distance": float(np.linalg.norm(state - target * np.vdot(target, state))),
            "native_pilot_vector_error_up_to_global_phase": float(np.linalg.norm(native - aligned)),
            "native_pilot_norm": float(np.linalg.norm(assembled)),
            "uniform_flux_overlap": uniform_overlap,
            "uniform_flux_is_exact": bool(np.max(abs(target - uniform)) < 1e-14)}


def line_graph_positivity_falsifier(time=F(1, 64)):
    """The earlier claw-containing witness alone did not exclude line graphs."""
    if not isinstance(time, F) or not 0 < time <= F(1, 64):
        raise ValueError("exact time must lie in (0,1/64]")
    edges = [(i, j) for i in range(2) for j in range(2, 5)]
    graph = Graph.create(6, [(i, j) for i in range(6) for j in range(i+1, 6)
                              if set(edges[i]) & set(edges[j])])
    label = 15
    symmetry = symmetry_zero_certificate(graph, (0, 2, 1, 3, 5, 4), label)
    powers = power_coefficients(graph, 31, label, 8)
    leading = leading_paired_coefficients(graph)[label]
    interval = paired_activity_interval(graph, 63, label, time)
    assert symmetry["identically_zero_for_unit_couplings"]
    assert powers[:6] == (0,) * 6 and powers[6] == 16
    assert leading == -F(2, 2025) and interval.upper < 0
    return {"root_graph": "K_2,3", "root_edges": edges,
            "anticommutation_edges": graph.edges, "cycle_rank": 2,
            "label": label, "symmetry": symmetry, "time_beta_over_two": str(time),
            "leading_activity_coefficient_at_time_power_12": str(leading),
            "activity_interval": {"lo": str(interval.lower), "hi": str(interval.upper)},
            "all_time_identity": "W(full,label)=-2*a_(full-minus-edge5)(label)^2",
            "rejected_route": "nonnegative paired-visit-support weights on line graphs",
            "classical_hardness_claim": False,
            "this_root_has_existing_classical_sampler": True}

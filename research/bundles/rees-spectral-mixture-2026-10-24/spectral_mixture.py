"""Costed spectral-packet reduction and bounded physical controls.

Not a mixed-state HSP implementation. No eigenbasis is supplied to the
proposed algorithm; numerical eigenvectors appear ONLY in finite controls.
"""

from fractions import Fraction as F
import importlib.util
from math import ceil
from pathlib import Path

import numpy as np


def _rational(value, name):
    if not isinstance(value, (int, F)) or isinstance(value, bool) or not 0 < value <= 1:
        raise ValueError(f"{name} must be an exact rational in (0,1]")
    return F(value)


def _integer(value, name):
    if type(value) is not int or value < 1:
        raise ValueError(f"{name} must be a positive integer")


def _ceil_log2(value):
    return max(0, (ceil(value) - 1).bit_length())


def packet_budget(*, receiver_leaves, design_size, cover_order_bits,
                  minimum_weight, spectral_gap, orbit_trace_gap, error):
    """An all-history clock, including failed eigenvalue-matching attempts.

    Promises are supplied, not certified. Source amplitude error and total
    error allocations use complete channels with explicit ABORT outcomes.
    """
    for name, value in (("receiver leaves", receiver_leaves), ("design size", design_size),
                        ("cover order bits", cover_order_bits)):
        _integer(value, name)
    weight = _rational(minimum_weight, "minimum positive eigenvalue")
    gap = _rational(spectral_gap, "positive spectral separation")
    delta = _rational(orbit_trace_gap, "conjugation orbit trace gap")
    eps = _rational(error, "total error")
    gamma = delta**2 / 2
    amplification_bits = _ceil_log2(8 * receiver_leaves / eps)
    repetitions = ceil(F(cover_order_bits + amplification_bits) / gamma)
    packets = receiver_leaves * repetitions
    matching_bits = _ceil_log2(8 * packets * design_size / eps)
    attempts = ceil(F(matching_bits) / weight)
    measurements = packets * (1 + (design_size - 1) * attempts)
    estimate_failure = eps / (8 * measurements)
    dme_error = eps / (16 * measurements)
    public_circuit_error = dme_error
    phase_bits = _ceil_log2(128 / (gap * estimate_failure))
    # U=exp(i*pi*rho/2). QPE time at bitj is <2*2^j.
    # A partial-swap step has half-diamond error<=2*(time/steps)^2.
    copies_per_measurement = sum(ceil(8 * phase_bits * F(4**j) / dme_error)
                                 for j in range(phase_bits))
    return {
        "receiver_leaf_cap": receiver_leaves,
        "design_size": design_size,
        "promised_cover_order_log2_upper_bound": cover_order_bits,
        "overlap_gap_lower_bound": str(gamma),
        "amplification_blocks_per_leaf": repetitions,
        "spectral_packets": packets,
        "matching_attempts_per_required_copy_cap": attempts,
        "spectral_measurement_cap": measurements,
        "phase_estimation_bits": phase_bits,
        "phase_grid": str(1 << phase_bits),
        "per_estimate_bad_value_budget": str(estimate_failure),
        "per_measurement_dme_channel_budget": str(dme_error),
        "per_measurement_public_gate_budget": str(public_circuit_error),
        "program_copies_per_spectral_measurement_cap": str(copies_per_measurement),
        "total_raw_copy_cap": str(measurements * (1 + copies_per_measurement)),
        "source_amplification_error_budget": str(eps / 8),
        "matching_abort_budget": str(eps / 8),
        "spectral_bad_value_budget": str(eps / 8),
        "spectral_implementation_error_budget": str(eps / 8),
        "address_and_receiver_budget": str(eps / 2),
        "global_total_error_budget": str(eps),
        "unknown_state_inverse_calls": 0,
        "conjugate_copy_calls": 0,
        "all_promises_certified": False,
        "polynomial_only_with_inverse_polynomial_promised_gaps": True,
    }


def trace_distance(a, b):
    return float(np.abs(np.linalg.eigvalsh(a - b)).sum() / 2)


def matched_packet_overlap(weights, eigenvectors, unitaries):
    """Literal finite conditional tensor packet, then mix over its seed label."""
    result = 0j
    for weight, vector in zip(weights, eigenvectors.T):
        original, evolved = np.ones(1, dtype=complex), np.ones(1, dtype=complex)
        for unitary in unitaries:
            original = np.kron(original, vector)
            evolved = np.kron(evolved, unitary @ vector)
        result += weight * np.vdot(original, evolved)
    return result


def controlled_partial_swap_step(sigma, rho, angle, reference=1):
    """Literal finite controlled-SWAP exponential with the program traced out."""
    d = len(rho)
    system = 2 * d * reference
    if sigma.shape != (system, system):
        raise ValueError("control x target x reference density required")
    total = system * d
    p0, p1, swap = (np.zeros((total, total), dtype=complex) for _ in range(3))
    for control in (0, 1):
        for target in range(d):
            for ref in range(reference):
                for program in range(d):
                    i = ((control * d + target) * reference + ref) * d + program
                    if not control:
                        p0[i, i] = 1
                    else:
                        p1[i, i] = 1
                        j = ((control * d + program) * reference + ref) * d + target
                        swap[j, i] = 1
    unitary = p0 + np.cos(angle) * p1 - 1j * np.sin(angle) * swap
    joint = unitary @ np.kron(sigma, rho) @ unitary.conj().T
    return np.einsum("iaja->ij", joint.reshape(system, d, system, d))


def ideal_controlled_evolution(sigma, rho, time, reference=1):
    values, vectors = np.linalg.eigh(rho)
    evolution = (vectors * np.exp(-1j * time * values)) @ vectors.conj().T
    d = len(rho)
    unitary = np.zeros((2*d, 2*d), dtype=complex)
    unitary[:d, :d] = np.eye(d)
    unitary[d:, d:] = evolution
    unitary = np.kron(unitary, np.eye(reference))
    return unitary @ sigma @ unitary.conj().T


def native_fixture():
    path = Path(__file__).resolve().parent.parent / "rees-formal-core-2026-10-24/native_source_controls.py"
    spec = importlib.util.spec_from_file_location("spectral_native_fixture", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def heisenberg_representation(g):
    x, y, z = g
    omega = np.exp(2j * np.pi / 3)
    shift = np.roll(np.eye(3), x, axis=0)
    phase = np.diag([omega**((-y * j) % 3) for j in range(3)])
    return omega**((z - 2*x*y) % 3) * shift @ phase


def audit():
    native = native_fixture()
    design = (1, 2, 1, 2, 1, 2)
    weights = np.array([2/3, 1/3, 0.])
    vectors = np.eye(3, dtype=complex)
    rho = np.diag(weights).astype(complex)
    rep = {g: heisenberg_representation(g) for g in native.GROUP}
    representation_error = max(float(np.max(np.abs(rep[native.mul(g, h)] - rep[g] @ rep[h])))
                               for g in native.GROUP for h in native.GROUP)
    mixed_hidden = {g for g in native.GROUP if trace_distance(rep[g] @ rho @ rep[g].conj().T, rho) < 1e-10}
    scalar_hidden = {g for g in native.GROUP if abs(abs(np.trace(rho @ rep[g])) - 1) < 1e-10}
    worst = 0.
    for a in native.COVER:
        evaluations = tuple(native.evaluate(a, s) for s in design)
        overlap = matched_packet_overlap(weights, vectors, [rep[g] for g in evaluations])
        expected = int(all(g in mixed_hidden for g in evaluations))
        worst = max(worst, abs(overlap - expected))
    address = (0, 1, 0, 0)
    operations = [rep[native.evaluate(address, s)] for s in design]
    iid_wrong = np.prod([np.trace(rho @ unitary) for unitary in operations])
    mixed_degenerate = np.eye(3) / 3
    bad_address = (1, 0, 0, 0)
    operations_degenerate = [rep[native.evaluate(bad_address, s)] for s in design]
    degenerate_overlap = matched_packet_overlap(np.ones(3)/3, vectors, operations_degenerate)

    rng = np.random.default_rng(241024)
    trials, worst_gap_excess = 64, 0.
    for _ in range(trials):
        unitary, _ = np.linalg.qr(rng.normal(size=(3, 3)) + 1j*rng.normal(size=(3, 3)))
        diagonal_amplitude = float(np.dot(weights, np.abs(np.diag(unitary))))
        distance = trace_distance(rho, unitary @ rho @ unitary.conj().T)
        worst_gap_excess = max(worst_gap_excess, diagonal_amplitude - (1-distance**2/2))
    vector = rng.normal(size=12) + 1j * rng.normal(size=12)
    vector /= np.linalg.norm(vector)
    sigma = np.outer(vector, vector.conj())
    dme_rows = []
    for steps in (1, 2, 4, 8, 16):
        actual = sigma.copy()
        for _ in range(steps):
            actual = controlled_partial_swap_step(actual, rho, .7/steps, reference=2)
        ideal = ideal_controlled_evolution(sigma, rho, .7, reference=2)
        dme_rows.append({"steps": steps, "distance": trace_distance(actual, ideal), "bound": 2 * .7**2/steps})
    angle = 2 * np.pi / 3
    rotation = np.eye(3, dtype=complex)
    rotation[1:, 1:] = np.array([[np.cos(angle), 1j*np.sin(angle)],
                                 [1j*np.sin(angle), np.cos(angle)]])
    near = np.eye(3, dtype=complex)
    small = 2**-12
    near[:2, :2] = [[np.cos(small), -np.sin(small)], [np.sin(small), np.cos(small)]]
    perturbed = near @ rotation @ near.conj().T
    full_rho = np.diag([.5, .3, .2]).astype(complex)
    return {
        "representation_homomorphism_error": representation_error,
        "mixed_conjugation_hidden_order": len(mixed_hidden),
        "old_scalar_support_hidden_order": len(scalar_hidden),
        "actual_cover_elements_checked": len(native.COVER),
        "matched_packet_maximum_overlap_error": float(worst),
        "independent_marginals_wrong_hidden_overlap_error": float(abs(1-iid_wrong)),
        "degenerate_conjugation_distance": trace_distance(mixed_degenerate,
                                                          operations_degenerate[0] @ mixed_degenerate @ operations_degenerate[0].conj().T),
        "degenerate_packet_overlap": float(abs(degenerate_overlap)),
        "purification_gap_trials": trials,
        "maximum_gap_inequality_excess": worst_gap_excess,
        "controlled_dme_with_reference": dme_rows,
        "principal_only_false_symmetry_distance": trace_distance(full_rho, rotation @ full_rho @ rotation.conj().T),
        "principal_only_fixed_vector_error": float(np.linalg.norm(rotation[:, 0] - np.eye(3)[:, 0])),
        "individual_eigenstate_gap_countercontrol": {
            "finite_order_three_error": float(np.max(np.abs(np.linalg.matrix_power(perturbed, 3) - np.eye(3)))),
            "one_eigenstate_overlap_gap": float(1 - abs(perturbed[0, 0])),
            "mixed_conjugation_distance": trace_distance(full_rho, perturbed @ full_rho @ perturbed.conj().T),
        },
        "scope": {
            "conditional_reduction_for_nondegenerate_positive_spectrum": True,
            "general_mixed_state_solver": False,
            "spectral_preprocessor_implemented": False,
            "quantum_receiver_executed": False,
            "independent_review": False,
            "novelty_or_speedup_claim": False,
        },
    }

"""Bounded dense controls of mode access and the full canonical purification.

Dense diagonalization is a validation oracle here, never an algorithmic input.
"""

import numpy as np

from mode_access import certify


def native_matrices(couplings, radius, probe_size):
    m = len(couplings)
    if m > 8:
        raise ValueError("dense validation limited to eight native generators")
    dimension = 1 << m
    h = np.zeros((dimension, dimension), dtype=complex)
    for column in range(dimension):
        for i, coupling in enumerate(couplings):
            neighbors = sum(1 << j for j in range(max(0, i-radius), i))
            sign = (-1)**((column & neighbors).bit_count())
            h[column ^ (1 << i), column] += float(coupling)*sign
    mask = (1 << probe_size)-1
    probe = np.diag([(-1)**((column & mask).bit_count()) for column in range(dimension)])
    return h, probe.astype(complex)


def dense_modes(couplings, radius, probe_size, *, beta=1):
    certificate = certify(couplings, radius, probe_size, beta=beta, initial_bits=128)
    h, probe = native_matrices(couplings, radius, probe_size)
    values, basis = np.linalg.eigh(h)
    in_basis = basis.conj().T @ probe @ basis
    differences = values[:, None]-values[None, :]
    modes = []
    for row in certificate["modes"]:
        energy = float(row["energy"].midpoint)
        weight = float(row["weight_squared"].midpoint)**0.5
        if weight < 1e-7:
            raise ValueError("dense float mode extraction is not a small-overlap certificate")
        raised = basis @ (in_basis * (abs(differences-2*energy) < 1e-8)) @ basis.conj().T
        c = (raised+raised.conj().T)/weight
        d = -1j*(raised-raised.conj().T)/weight
        modes.append((energy, weight, c, d))
    return h, probe, modes, certificate


def prepare_matrix(modes, dimension, beta, active=None, *, wrong_transpose=False):
    matrix = np.eye(dimension, dtype=complex)/dimension**0.5
    active = range(len(modes)) if active is None else active
    for k in active:
        energy, _, c, d = modes[k]
        theta = np.arctan(np.tanh(float(beta)*energy/2))
        right = c.T if wrong_transpose else c
        matrix = np.cos(theta)*matrix-1j*np.sin(theta)*(d @ matrix @ right)
    return matrix


def reference_matrix(h, beta):
    values, basis = np.linalg.eigh(h)
    weights = np.exp(-float(beta)*(values-values.min())/2)
    return (basis*weights) @ basis.conj().T / np.linalg.norm(weights)


def continuous_filter(h, probe, frequency, time, sine=False):
    values, basis = np.linalg.eigh(h)
    differences = values[:, None]-values[None, :]
    minus = np.sinc((differences-frequency)*time/np.pi)
    plus = np.sinc((differences+frequency)*time/np.pi)
    factors = 1j*(plus-minus) if sine else plus+minus
    return basis @ ((basis.conj().T @ probe @ basis)*factors) @ basis.conj().T


def midpoint_filter(h, probe, frequency, time, terms, sine=False):
    """Closed geometric sum of the finite midpoint LCU, dense validation only."""
    values, basis = np.linalg.eigh(h)
    differences = values[:, None]-values[None, :]

    def kernel(argument):
        return np.sinc(argument*time/np.pi)/np.sinc(argument*time/(terms*np.pi))

    minus = kernel(differences-frequency)
    plus = kernel(differences+frequency)
    factors = 1j*(plus-minus) if sine else plus+minus
    return basis @ ((basis.conj().T @ probe @ basis)*factors) @ basis.conj().T


def hermitian_polar(matrix):
    if not np.allclose(matrix, matrix.conj().T, atol=1e-10):
        raise ValueError("filter is not Hermitian")
    values, basis = np.linalg.eigh(matrix)
    if np.min(abs(values)) < 1e-12:
        raise ValueError("dense polar reference is singular or unresolved")
    return (basis*np.sign(values)) @ basis.conj().T


def filtered_audit(couplings, radius, probe_size):
    h, probe, modes, certificate = dense_modes(couplings, radius, probe_size)
    filtered = list(modes)
    largest_error = 0.0
    for budget in certificate["filters"]:
        k = budget["mode"]
        energy, weight, c, d = modes[k]
        args = (h, probe, 2*energy, budget["filter_time"], budget["midpoint_terms"])
        c_filtered = hermitian_polar(midpoint_filter(*args))
        d_filtered = hermitian_polar(midpoint_filter(*args, sine=True))
        largest_error = max(largest_error, float(np.linalg.norm(c_filtered-c, 2)),
                            float(np.linalg.norm(d_filtered-d, 2)))
        filtered[k] = energy, weight, c_filtered, d_filtered
    prepared = prepare_matrix(filtered, len(h), 1, certificate["active_modes"])
    distance = float(np.linalg.norm(prepared-reference_matrix(h, 1)))
    if largest_error > float(certificate["per_mode_unitary_error_target"])+1e-8:
        raise ArithmeticError("filtered mode error exceeds ledger")
    if distance > float(certificate["error"]):
        raise ArithmeticError("filtered full-state control exceeds error target")
    return {"native_generators": len(couplings), "radius": radius, "probe_size": probe_size,
            "filtered_mode_operator_error": largest_error, "filtered_tfd_vector_error": distance,
            "quantum_execution": False, "qsvt_circuit_compiled": False,
            "dense_reference_is_algorithm_input": False,
            "floating_controls_are_rigorous_certificates": False}


def audit(couplings, radius, probe_size, beta=1):
    h, probe, modes, certificate = dense_modes(couplings, radius, probe_size, beta=beta)
    dimension = h.shape[0]
    identity = np.eye(dimension)
    majoranas = [matrix for _, _, c, d in modes for matrix in (c, d)]
    car_error = max(np.linalg.norm(a @ b+b @ a-(2*identity if i == j else 0), 2)
                    for i, a in enumerate(majoranas) for j, b in enumerate(majoranas))
    recovered_h = sum(-1j*energy*(c @ d) for energy, _, c, d in modes)
    prepared = prepare_matrix(modes, dimension, beta)
    reference = reference_matrix(h, beta)
    truncated = prepare_matrix(modes, dimension, beta, certificate["active_modes"])
    result = {
        "native_generators": len(couplings), "radius": radius, "probe_size": probe_size,
        "beta": float(beta), "car_operator_error": float(car_error),
        "hamiltonian_operator_error": float(np.linalg.norm(recovered_h-h, 2)),
        "full_tfd_vector_error": float(np.linalg.norm(prepared-reference)),
        "temperature_truncated_vector_error": float(np.linalg.norm(truncated-reference)),
        "omitted_state_distance_bound": float(certificate["omitted_state_distance_upper"]),
        "dense_reference_is_algorithm_input": False, "quantum_execution": False,
        "floating_controls_are_rigorous_certificates": False,
    }
    for key in ("car_operator_error", "hamiltonian_operator_error", "full_tfd_vector_error"):
        if result[key] > 1e-8:
            raise ArithmeticError(f"native dense identity failed: {key}")
    if result["temperature_truncated_vector_error"] > result["omitted_state_distance_bound"]+1e-8:
        raise ArithmeticError("omitted-mode bound failed")
    return result

"""Code-support source accounting and bounded falsification controls.

The antisymmetrization primitive is prior work (arXiv:2610.06737).
Dense matrices below are calibration controls, not a scalable receiver.
"""

from fractions import Fraction as F
from functools import lru_cache
import importlib.util
from itertools import permutations, product
from math import ceil, factorial, sqrt
from pathlib import Path

import numpy as np


def positive_integer(value, name):
    if type(value) is not int or value < 1:
        raise ValueError(f"{name} must be a positive integer")


def probability(value, name):
    if not isinstance(value, (int, F)) or isinstance(value, bool) or not 0 < value <= 1:
        raise ValueError(f"{name} must be an exact rational in (0,1]")
    return F(value)


def ceil_log2(value):
    return max(0, (ceil(value) - 1).bit_length())


def growth_probability(rank, size):
    positive_integer(rank, "rank")
    positive_integer(size, "current wedge size")
    if size >= rank:
        raise ValueError("growth requires size < the promised rank")
    return F(rank - size, rank * (size + 1))


def source_plan(*, rank, receiver_leaves, design_size, cover_order_bits,
                support_operator_gap, error):
    for name, value in (("rank", rank), ("receiver leaves", receiver_leaves),
                        ("design size", design_size), ("cover order bits", cover_order_bits)):
        positive_integer(value, name)
    gap = probability(support_operator_gap, "support operator gap")
    eps = probability(error, "total error")
    gamma = gap**2 / 2
    repetitions = ceil((cover_order_bits + ceil_log2(8 * receiver_leaves / eps)) / gamma)
    wedge_sources = receiver_leaves * repetitions * design_size
    tail_bits = ceil_log2(8 * wedge_sources * max(1, rank - 1) / eps)
    stages = []
    for size in range(1, rank):
        p = growth_probability(rank, size)
        attempts = ceil(F(tail_bits) / p)
        stages.append({"size": size, "success_probability": str(p), "attempt_cap": attempts})
    attempts_per_source = sum(row["attempt_cap"] for row in stages)
    measurements = wedge_sources * attempts_per_source
    return {
        "promised_rank": rank,
        "promised_flat_code_state": True,
        "promises_certified": False,
        "receiver_leaf_cap": receiver_leaves,
        "design_size": design_size,
        "cover_order_bits": cover_order_bits,
        "ray_overlap_gap_lower_bound": str(gamma),
        "amplification_blocks_per_leaf": repetitions,
        "independent_wedge_sources": wedge_sources,
        "growth_stages": stages,
        "growth_measurement_cap": measurements,
        "native_copies_per_wedge_cap": 1 + attempts_per_source,
        "native_copy_cap": wedge_sources * (1 + attempts_per_source),
        "controlled_register_swaps_cap": wedge_sources * sum(2 * row["size"] * row["attempt_cap"] for row in stages),
        "controlled_original_action_calls": rank * wedge_sources,
        "per_growth_instrument_half_diamond_budget": str(eps / (8 * measurements)) if measurements else None,
        "per_original_action_half_diamond_budget": str(eps / (8 * rank * wedge_sources)),
        "source_amplification_budget": str(eps / 8),
        "extraction_abort_budget": str(eps / 8),
        "growth_implementation_budget": str(eps / 8),
        "original_action_implementation_budget": str(eps / 8),
        "public_addresses_and_receiver_budget": str(eps / 2),
        "global_error_budget": str(eps),
        "unknown_preparation_inverse_calls": 0,
        "source_dimension_enumeration_required": False,
        "spectral_nondegeneracy_required": False,
        "scalable_receiver_implemented": False,
    }


def sign(perm):
    return (-1)**sum(perm[i] > perm[j] for i in range(len(perm)) for j in range(i+1, len(perm)))


def permutation_matrix(dimension, perm):
    size = len(perm)
    total = dimension**size
    if total > 256 or size > 4:
        raise ValueError("dense calibration cap exceeded")
    matrix = np.zeros((total, total), dtype=complex)
    for word in product(range(dimension), repeat=size):
        destination = tuple(word[perm[i]] for i in range(size))
        matrix[np.ravel_multi_index(destination, (dimension,)*size),
               np.ravel_multi_index(word, (dimension,)*size)] = 1
    return matrix


@lru_cache(maxsize=None)
def antisymmetric_projector(dimension, size):
    return sum(sign(perm) * permutation_matrix(dimension, perm)
               for perm in permutations(range(size))) / factorial(size)


def tensor_power(matrix, count):
    result = np.ones((1, 1), dtype=complex)
    for _ in range(count):
        result = np.kron(result, matrix)
    return result


def wedge_vector(frame):
    dimension, rank = frame.shape
    if dimension**rank > 256:
        raise ValueError("dense calibration cap exceeded")
    result = np.zeros(dimension**rank, dtype=complex)
    for perm in permutations(range(rank)):
        vector = np.ones(1, dtype=complex)
        for j in perm:
            vector = np.kron(vector, frame[:, j])
        result += sign(perm) * vector / sqrt(factorial(rank))
    return result


def trace_distance(a, b):
    return float(np.abs(np.linalg.eigvalsh(a-b)).sum()/2)


def growth_instrument(dimension, size):
    """Literal LCU ancilla, including the required failure correction."""
    count = size + 1
    n = dimension**count
    w = np.exp(2j*np.pi*np.outer(np.arange(count), np.arange(count))/count) / sqrt(count)
    operations = [np.eye(n, dtype=complex)]
    for i in range(size):
        perm = list(range(count))
        perm[i], perm[size] = perm[size], perm[i]
        operations.append(-permutation_matrix(dimension, tuple(perm)))
    select = np.zeros((count*n, count*n), dtype=complex)
    for i, op in enumerate(operations):
        select[i*n:(i+1)*n, i*n:(i+1)*n] = op
    prepare = np.kron(w, np.eye(n))
    before = prepare.conj().T @ select @ prepare
    success = before[:n, :n]
    rejected = before[:, :n].copy()
    rejected[:n] = 0
    correction = select @ prepare
    corrected = correction @ rejected
    fine_grained = [correction[b*n:(b+1)*n, j*n:(j+1)*n] @ rejected[j*n:(j+1)*n]
                    for j in range(1, count) for b in range(count)]
    return (success,
            [corrected[i*n:(i+1)*n] for i in range(count)],
            [rejected[i*n:(i+1)*n] for i in range(count)], fine_grained)


def apply_channel(kraus, state):
    return sum(k @ state @ k.conj().T for k in kraus)


def trace_last(state, dimension):
    remaining = len(state) // dimension
    return np.einsum("iaja->ij", state.reshape(remaining, dimension, remaining, dimension))


def native_module():
    path = Path(__file__).resolve().parent.parent / "rees-spectral-mixture-2026-10-24/spectral_mixture.py"
    spec = importlib.util.spec_from_file_location("support_spectral_fixture", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def audit():
    rng = np.random.default_rng(241025)
    basis, _ = np.linalg.qr(rng.normal(size=(4, 4)) + 1j*rng.normal(size=(4, 4)))
    frame = basis[:, :3]
    rho = frame @ frame.conj().T / 3
    sigma = rho.copy()
    probability_error = failure_support_error = instrument_error = 0.
    wrong_failure_leakage = fine_grained_leakage = 0.
    for size in (1, 2):
        success, corrected, uncorrected, fine_grained = growth_instrument(4, size)
        prior = np.kron(antisymmetric_projector(4, size), np.eye(4))
        larger = antisymmetric_projector(4, size+1)
        instrument_error = max(instrument_error, float(np.linalg.norm((success-larger) @ prior)))
        for k in corrected:
            expected = (np.eye(len(larger))-larger) @ prior / sqrt(size+1)
            instrument_error = max(instrument_error, float(np.linalg.norm(k @ prior-expected)))
        for _ in range(3):
            joint = np.kron(sigma, rho)
            accepted = success @ joint @ success.conj().T
            mass = float(np.trace(accepted).real)
            probability_error = max(probability_error, abs(mass-float(growth_probability(3, size))))
            rejected = apply_channel(corrected, joint)
            wrong = apply_channel(uncorrected, joint)
            measured_index = apply_channel(fine_grained, joint)
            wrong_failure_leakage = max(wrong_failure_leakage,
                                        float(np.trace((np.eye(len(prior))-prior) @ wrong).real))
            fine_grained_leakage = max(fine_grained_leakage,
                                       float(np.trace((np.eye(len(prior))-prior) @ measured_index).real))
            sigma = trace_last(rejected, 4) / float(np.trace(rejected).real)
            projector = antisymmetric_projector(4, size)
            failure_support_error = max(failure_support_error, float(np.linalg.norm(sigma-projector @ sigma @ projector)))
        accepted = success @ np.kron(sigma, rho) @ success.conj().T
        sigma = accepted / float(np.trace(accepted).real)
    wedge = wedge_vector(frame)
    extraction_error = trace_distance(sigma, np.outer(wedge, wedge.conj()))
    partial = antisymmetric_projector(4, 2) @ np.kron(rho, rho) @ antisymmetric_projector(4, 2)
    partial /= np.trace(partial)

    fixture = native_module()
    native = fixture.native_fixture()
    design = (1, 2, 1, 2, 1, 2)
    representation = {g: fixture.heisenberg_representation(g) for g in native.GROUP}
    flat = np.diag([.5, .5, 0])
    small_frame = np.eye(3)[:, :2]
    small_wedge = wedge_vector(small_frame)
    hidden = {g for g, u in representation.items() if trace_distance(flat, u @ flat @ u.conj().T) < 1e-10}
    overlaps = {g: np.vdot(small_wedge, tensor_power(u, 2) @ small_wedge) for g, u in representation.items()}
    rees_error = max(abs(np.prod([overlaps[native.evaluate(a, s)] for s in design]) -
                         int(all(native.evaluate(a, s) in hidden for s in design))) for a in native.COVER)

    # Sparse left-regular support is a nonnormal interface control, not a hard code.
    line = {(x, 0, 0) for x in range(3)}
    ordered_line = tuple(sorted(line))
    wedge_signs = {tuple(ordered_line[j] for j in perm): sign(perm)
                   for perm in permutations(range(3))}
    regular_overlaps = {}
    for g in native.GROUP:
        regular_overlaps[g] = sum(F(value * wedge_signs.get(tuple(native.mul(g, h) for h in word), 0), 6)
                                  for word, value in wedge_signs.items())
    line_hidden = {g for g in native.GROUP if {native.mul(g, h) for h in line} == line}
    identity = (0, 0, 0)
    inverses = {g: next(h for h in native.GROUP if native.mul(g, h) == identity) for g in native.GROUP}
    core = set.intersection(*({native.mul(native.mul(g, h), inverses[g]) for h in line_hidden}
                             for g in native.GROUP))
    nonnormal_error = F(0)
    for a in native.COVER:
        overlap = F(1)
        for s in design:
            overlap *= regular_overlaps[native.evaluate(a, s)]
        expected = int(all(native.evaluate(a, s) in line_hidden for s in design))
        nonnormal_error = max(nonnormal_error, abs(overlap-expected))

    determinant_error = gap_excess = 0.
    for _ in range(48):
        unitary, _ = np.linalg.qr(rng.normal(size=(4, 4)) + 1j*rng.normal(size=(4, 4)))
        overlap = np.vdot(wedge, tensor_power(unitary, 3) @ wedge)
        compressed = frame.conj().T @ unitary @ frame
        determinant_error = max(determinant_error, abs(overlap - np.linalg.det(compressed)))
        projector = frame @ frame.conj().T
        gap = np.linalg.norm(projector - unitary @ projector @ unitary.conj().T, ord=2)
        gap_excess = max(gap_excess, abs(overlap)**2 - (1-gap**2))

    angle = 2*np.pi/3
    inside = np.eye(3, dtype=complex)
    inside[:2, :2] = [[np.cos(angle), 1j*np.sin(angle)], [1j*np.sin(angle), np.cos(angle)]]
    nonflat = np.diag([.6, .4, 0])
    return {
        "growth_probability_max_error": probability_error,
        "growth_instrument_operator_error": instrument_error,
        "corrected_failure_antisymmetry_error": failure_support_error,
        "uncorrected_failure_antisymmetry_leakage": wrong_failure_leakage,
        "fine_grained_ancilla_measurement_leakage": fine_grained_leakage,
        "final_extracted_wedge_trace_distance": extraction_error,
        "understated_rank_output_purity": float(np.trace(partial @ partial).real),
        "flat_code_hidden_order": len(hidden),
        "actual_rees_addresses_checked": len(native.COVER),
        "rees_hidden_overlap_max_error": float(rees_error),
        "nonnormal_code_hidden_order": len(line_hidden),
        "nonnormal_code_normal_core_order": len(core),
        "nonnormal_rees_hidden_overlap_error_exact": str(nonnormal_error),
        "determinant_identity_max_error": float(determinant_error),
        "principal_angle_gap_max_excess": float(gap_excess),
        "nonflat_support_false_conjugation_distance": trace_distance(nonflat, inside @ nonflat @ inside.conj().T),
        "nonflat_support_wedge_overlap_modulus": float(abs(np.vdot(small_wedge, tensor_power(inside, 2) @ small_wedge))),
        "scope": {"conditional_code_support_reduction": True,
                  "antisymmetrization_primitive_is_prior_art": True,
                  "arbitrary_mixed_conjugation_solver": False,
                  "quantum_receiver_executed": False,
                  "independent_review": False,
                  "novelty_or_speedup_claim": False},
    }

"""Exact ledgers and finite controls for gap-preserving mixed-state sources.

No density matrix, spectral projectors or rank data are granted to a quantum
algorithm. Functions accepting spectra/frames are diagnostic references only.
"""
from fractions import Fraction as F
from functools import lru_cache
import importlib.util
from itertools import product
from math import ceil
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent
SUPPORT = ROOT.parent / "rees-code-support-2026-10-24/code_support.py"


def positive(value, name):
    if type(value) is not int or value < 1:
        raise ValueError(f"positive integer {name} required")


def probability(value, name):
    if not isinstance(value, (int, F)) or isinstance(value, bool) or not 0 < value <= 1:
        raise ValueError(f"exact rational {name} in (0,1] required")
    return F(value)


def ceil_log2(value):
    return max(0, (ceil(value)-1).bit_length())


def grid_plan(rank_cap, orbit_gap, error):
    positive(rank_cap, "rank cap")
    delta, eps = probability(orbit_gap, "orbit gap"), probability(error, "error")
    h = delta/(32*rank_cap)
    K = 2**ceil_log2(128*rank_cap/eps)
    margin = eps*h/(128*rank_cap)
    return {"rank_cap": rank_cap, "orbit_gap": delta, "error": eps,
            "bin_width": h, "grid_choices": K, "boundary_margin": margin,
            "bin_count_cap": ceil(1/h)+1,
            "bad_grid_probability_upper": 2*rank_cap*margin/h+F(2*rank_cap, K),
            "coarsening_trace_norm_upper": 2*rank_cap*h,
            "off_group_projector_operator_gap_lower": delta-2*rank_cap*h,
            "ray_gap_lower": delta*delta/8,
            "global_gap_and_rank_are_promises_not_certified": True}


def coarsen_reference(spectrum, plan, offset_index):
    """Exact supplied-spectrum control, NOT spectral acquisition from copies."""
    spectrum = tuple(spectrum)
    if any(not isinstance(x, (int, F)) or isinstance(x, bool) for x in spectrum):
        raise ValueError("exact rational reference eigenvalues required")
    values = tuple(F(x) for x in spectrum)
    if not values or any(x < 0 for x in values) or sum(values) != 1:
        raise ValueError("normalized nonnegative reference spectrum required")
    if sum(x > 0 for x in values) > plan["rank_cap"]:
        raise ValueError("reference spectrum violates supplied rank cap")
    K, h = plan["grid_choices"], plan["bin_width"]
    if type(offset_index) is not int or not 0 <= offset_index < K:
        raise ValueError("offset must be an actual uniform-grid index")
    cutoff = h+F(offset_index, K)*h
    labels, rounded, bins = [], [], {}
    bad = False
    for i, value in enumerate(values):
        coordinate = (value-cutoff)/h
        lower = coordinate.numerator//coordinate.denominator
        boundary_candidates = {max(0, lower), max(0, lower+1)}
        if value > 0 and min(abs(value-(cutoff+j*h)) for j in boundary_candidates) <= plan["boundary_margin"]:
            bad = True
        if value < cutoff:
            labels.append(None)
            rounded.append(F(0))
        else:
            labels.append(lower)
            rounded.append(cutoff+lower*h)
            bins.setdefault(lower, []).append(i)
    loss = sum(x-y for x, y in zip(values, rounded))
    return {"spectrum": values, "rounded": tuple(rounded), "labels": tuple(labels),
            "bins": {j: tuple(indices) for j, indices in bins.items()},
            "cutoff": cutoff, "bad_grid": bad, "trace_norm_loss": loss,
            "retained_rank": sum(len(v) for v in bins.values()),
            "status": "EXACT_SUPPLIED_SPECTRUM_REFERENCE_NOT_QUANTUM_ACQUISITION"}


def source_plan(*, rank_cap, orbit_gap, error, receiver_leaves, design_size, cover_order_bits):
    for name, value in [("leaves", receiver_leaves), ("design", design_size), ("cover bits", cover_order_bits)]:
        positive(value, name)
    result = grid_plan(rank_cap, orbit_gap, error)
    R, B, M, eps = rank_cap, receiver_leaves, design_size, result["error"]
    h, J, gamma = result["bin_width"], result["bin_count_cap"], result["ray_gap_lower"]
    repetitions = ceil((cover_order_bits+ceil_log2(8*B/eps))/gamma)
    W = B*repetitions*M
    V = J*(R+1)+W*R
    growth_cap = ceil((R+1)/h*ceil_log2(32*V/eps))
    requests = J+W*R+V*growth_cap
    fetch_cap = ceil(ceil_log2(32*requests/eps)/h)
    attempts = requests*fetch_cap
    zeta = eta = eps/(32*attempts)
    bits = ceil_log2(256/(result["boundary_margin"]*zeta))
    per_bit = tuple(ceil(8*bits*4**b/eta) for b in range(bits))
    result.update({"receiver_leaf_cap": B, "design_size": M, "cover_order_bits": cover_order_bits,
        "amplification_blocks_per_leaf": repetitions, "independent_packet_cap": W,
        "growth_stage_cap": V, "growth_attempts_per_stage": growth_cap,
        "growth_measurement_cap": V*growth_cap, "filtered_target_requests": requests,
        "spectral_attempts_per_fetch": fetch_cap, "spectral_attempt_cap": attempts,
        "spectral_bad_estimate_budget_per_attempt": zeta,
        "dme_half_diamond_budget_per_attempt": eta,
        "spectral_public_gates_budget_per_attempt": eps/(32*attempts),
        "qpe_bits": bits, "qpe_grid": 2**bits,
        "program_copies_per_bit": per_bit,
        "raw_copy_cap": attempts*(1+sum(per_bit)),
        "growth_instrument_error_per_call": eps/(32*V*growth_cap),
        "controlled_register_swaps_cap": 2*R*V*growth_cap,
        "original_controlled_action_cap": R*W,
        "original_action_error_per_call": eps/(32*R*W),
        "total_allocated_error_upper": 7*eps/8,
        "amplification_error_budget": eps/8,
        "each_of_eight_source_error_categories": eps/32,
        "public_receiver_and_addresses_budget": eps/2,
        "unknown_exact_rank_required": False, "minimum_original_eigenvalue_required": False,
        "minimum_distinct_eigenvalue_gap_required": False,
        "arbitrary_high_rank_mixed_state_solved": False,
        "spectrum_or_frame_supplied_to_algorithm": False,
        "quantum_execution": False, "accepted_speedup_candidate": False})
    return result


@lru_cache(maxsize=1)
def support_module():
    spec = importlib.util.spec_from_file_location("coarse_support_primitive", SUPPORT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def permute(values, permutation):
    if sorted(permutation) != list(range(len(values))):
        raise ValueError("permutation of the full reference space required")
    result = [None]*len(values)
    for i, destination in enumerate(permutation):
        result[destination] = values[i]
    return tuple(result)


def diagonal_distance(values, permutation):
    return sum(abs(x-y) for x, y in zip(values, permute(values, permutation)))/2


def coordinate_wedge_overlap_modulus(bins, permutation):
    """Exact determinant modulus for coordinate-subspace regression fixtures."""
    return int(all({permutation[i] for i in indices} == set(indices) for indices in bins.values()))


def near_degenerate_control():
    tiny = F(1, 2**300)
    split = F(1, 2**200)
    base = (F(1, 6)-split, F(1, 6), F(1, 6)+split, F(1, 4), F(1, 6), F(1, 12))
    spectrum = tuple((1-tiny)*x for x in base)+(tiny,)
    plan = grid_plan(7, F(1, 7), F(1, 16))
    coarse = coarsen_reference(spectrum, plan, plan["grid_choices"]//4)
    generator = (1, 2, 0, 4, 5, 3, 6)
    square = tuple(generator[generator[i]] for i in range(7))
    distances = tuple(diagonal_distance(spectrum, g) for g in (generator, square))
    return {"minimum_positive_weight": tiny,
            "explicit_tiny_splitting": (1-tiny)*split,
            "promised_global_gap": F(1, 7), "actual_nonidentity_distances": distances,
            "retained_rank": coarse["retained_rank"],
            "retained_bin_ranks": tuple(len(v) for v in coarse["bins"].values()),
            "trace_norm_loss": coarse["trace_norm_loss"], "coarsening_bound": plan["coarsening_trace_norm_upper"],
            "good_grid": not coarse["bad_grid"],
            "original_and_coarse_stabilizers_equal": all(diagonal_distance(coarse["rounded"], g) > 0 for g in (generator, square)),
            "packet_outside_overlap_moduli": tuple(coordinate_wedge_overlap_modulus(coarse["bins"], g) for g in (generator, square)),
            "whole_support_wedge_outside_overlap_modulus": 1,
            "classically_easy_reference_not_application": True}


def nonnormal_control():
    elements = tuple(product(range(3), repeat=3))
    index = {g: i for i, g in enumerate(elements)}
    multiply = lambda g, h: ((g[0]+h[0]) % 3, (g[1]+h[1]) % 3, (g[2]+h[2]+g[0]*h[1]) % 3)
    H = {(a, 0, 0) for a in range(3)}
    other = {multiply(g, (0, 1, 0)) for g in H}
    spectrum = tuple(F(1, 5) if g in H else F(2, 15) if g in other else F(0) for g in elements)
    plan = grid_plan(6, F(1, 5), F(1, 16))
    coarse = coarsen_reference(spectrum, plan, plan["grid_choices"]//4)
    actual, rounded, rays, outside = [], [], [], []
    for g in elements:
        permutation = tuple(index[multiply(g, h)] for h in elements)
        distance = diagonal_distance(spectrum, permutation)
        if distance == 0:
            actual.append(g)
        else:
            outside.append(distance)
        if diagonal_distance(coarse["rounded"], permutation) == 0:
            rounded.append(g)
        if coordinate_wedge_overlap_modulus(coarse["bins"], permutation):
            rays.append(g)
    inverse = lambda g: ((-g[0]) % 3, (-g[1]) % 3, (-g[2]+g[0]*g[1]) % 3)
    core = set(H)
    for g in elements:
        core &= {multiply(multiply(g, h), inverse(g)) for h in H}
    return {"group_order": 27, "hidden_order": len(actual), "normal_core_order": len(core),
            "minimum_outside_trace_distance": min(outside),
            "original_coarse_and_packet_subgroups_equal": actual == rounded == rays,
            "matches_expected_subgroup": set(actual) == H,
            "classically_easy_reference_not_application": True}


def nonflat_growth_control():
    primitive = support_module()
    rng = np.random.default_rng(261024)
    basis, _ = np.linalg.qr(rng.normal(size=(3, 3))+1j*rng.normal(size=(3, 3)))
    rho = basis@np.diag([1/2, 1/3, 1/6])@basis.conj().T
    retained = rho.copy()
    rows, leakage = [], 0.0
    for size in (1, 2):
        success, corrected, _, _ = primitive.growth_instrument(3, size)
        for history in range(3):
            joint = np.kron(retained, rho)
            mass = float(np.trace(success@joint@success.conj().T).real)
            lower = F(3-size, 6*(size+1))
            rows.append({"size": size, "previous_failures": history,
                         "success_probability": mass, "proven_lower": lower})
            rejected = primitive.apply_channel(corrected, joint)
            retained = primitive.trace_last(rejected, 3)/float(np.trace(rejected).real)
            projector = primitive.antisymmetric_projector(3, size)
            leakage = max(leakage, float(np.linalg.norm(retained-projector@retained@projector)))
        accepted = success@np.kron(retained, rho)@success.conj().T
        retained = accepted/float(np.trace(accepted).real)
    frame_wedge = primitive.wedge_vector(basis)
    full_wedge_error = primitive.trace_distance(retained, np.outer(frame_wedge, frame_wedge.conj()))
    impossible = primitive.antisymmetric_projector(3, 4)
    terminal_mass = float(np.trace(impossible@np.kron(retained, rho)@impossible).real)
    return {"status": "FLOATING_POINT_LITERAL_GROWTH_CONTROL_NOT_QUANTUM_EXECUTION",
            "rows": rows, "failure_sector_leakage": leakage,
            "full_wedge_trace_error": full_wedge_error, "beyond_true_rank_success": terminal_mass}


def rotated_gap_control():
    rng = np.random.default_rng(1717)
    basis, _ = np.linalg.qr(rng.normal(size=(4, 4))+1j*rng.normal(size=(4, 4)))
    omega = np.exp(2j*np.pi/3)
    U = basis@np.diag([omega, omega**2, 1, 1])@basis.conj().T
    values = (F(1, 2), F(1, 4), F(1, 4), F(0))
    p = grid_plan(3, F(1, 20), F(1, 16))
    coarse = coarsen_reference(values, p, p["grid_choices"]//4)
    rho, A = np.diag([float(x) for x in values]), np.diag([float(x) for x in coarse["rounded"]])
    rows = []
    for g in (U, U@U):
        overlap, operator_gaps = 1+0j, []
        for indices in coarse["bins"].values():
            frame = np.eye(4)[:, indices]
            P = frame@frame.T
            overlap *= np.linalg.det(frame.T@g@frame)
            operator_gaps.append(float(np.linalg.norm(P-g@P@g.conj().T, 2)))
        distance = lambda matrix: float(np.abs(np.linalg.eigvalsh(matrix-g@matrix@g.conj().T)).sum()/2)
        rows.append({"original_trace_distance": distance(rho), "coarse_trace_distance": distance(A),
                     "maximum_projector_gap": max(operator_gaps), "packet_overlap_modulus": float(abs(overlap))})
    return {"status": "FLOATING_POINT_NONDIAGONAL_GAP_CONTROL_NOT_PROOF",
            "promised_gap_in_this_fixture": F(1, 20), "coarsening_bound": p["coarsening_trace_norm_upper"],
            "rows": rows}

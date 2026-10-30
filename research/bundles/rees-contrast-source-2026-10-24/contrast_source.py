"""Contrast-source ledgers and controls, not quantum spectral acquisition."""
from fractions import Fraction as F
from functools import lru_cache
import importlib.util
from itertools import product
from math import ceil
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent
PREDECESSOR = ROOT.parent / "rees-coarse-spectrum-2026-10-24/coarse_spectrum.py"


@lru_cache(maxsize=1)
def predecessor():
    spec = importlib.util.spec_from_file_location("contrast_coarse_source", PREDECESSOR)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def contract_plan(dimension, contrast_rank, orbit_gap, error):
    old = predecessor()
    old.positive(dimension, "dimension")
    old.positive(contrast_rank, "contrast rank")
    if contrast_rank > dimension:
        raise ValueError("contrast rank cannot exceed dimension")
    delta = old.probability(orbit_gap, "orbit gap")
    eta, h0 = delta/256, delta/(64*contrast_rank)
    threshold = contrast_rank+2*(1+eta)/h0
    small = dimension <= threshold
    cap = dimension if small else 2*contrast_rank
    result = old.grid_plan(cap, delta, error)
    result.update({
        "dimension": dimension, "contrast_rank": contrast_rank,
        "branch": "POLYNOMIAL_DIMENSION" if small else "CENTERED_CONTRAST",
        "dimension_switch_threshold": threshold,
        "contrast_trace_residual_promise": eta,
        "rank_cap_scope": "RETAINED_AND_NEAR_BOUNDARY_SPECTRUM_NOT_FULL_STATE",
        "coarsening_trace_norm_upper": delta/16 if small else 9*delta/256,
        "off_group_projector_operator_gap_lower": delta*(F(15, 16) if small else F(247, 256)),
        "unknown_background_upper": None if small else (1+eta)/(dimension-contrast_rank),
        "retained_rank_upper": F(cap) if small else F(3*contrast_rank, 2),
        "near_boundary_rank_upper": cap,
        "state_rank_cap_supplied": False, "background_value_supplied": False,
        "global_gap_and_compressibility_are_uncertified_promises": True,
        "empty_retained_metadata_action": "RETURN_WHOLE_PUBLIC_GROUP",
        "arbitrary_symmetry_breaking_noise_corrected": False,
        "quantum_execution": False, "accepted_speedup_candidate": False,
    })
    result.pop("global_gap_and_rank_are_promises_not_certified")
    return result


def source_plan(*, dimension, contrast_rank, orbit_gap, error,
                receiver_leaves, design_size, cover_order_bits):
    contract = contract_plan(dimension, contrast_rank, orbit_gap, error)
    old = predecessor().source_plan(rank_cap=contract["rank_cap"], orbit_gap=orbit_gap,
        error=error, receiver_leaves=receiver_leaves, design_size=design_size,
        cover_order_bits=cover_order_bits)
    old.update(contract)
    old.pop("global_gap_and_rank_are_promises_not_certified")
    old["ledger_is_upper_bound_including_empty_shortcut"] = True
    return old


def classical_sample_plan(plan, failure):
    old = predecessor()
    failure = old.probability(failure, "failure")
    # ceil(log2 x) >= ln x; integer arithmetic avoids huge-D float conversion.
    logarithm_upper = old.ceil_log2(2*plan["dimension"]/failure)
    cap = ceil(2*logarithm_upper/plan["boundary_margin"]**2)
    return {"sample_cap": cap, "uniform_frequency_error": plan["boundary_margin"]/2,
            "failure_upper": failure, "basis_must_be_known": True,
            "stores_observed_labels_only": True, "quantum_input_measured_in_known_basis": True,
            "final_affine_p_group_backend": "PUBLISHED_LUKS_NOT_IMPLEMENTED",
            "arbitrary_succinct_permutation_backend_supplied": False}


def classical_colored_support(counts, sample_count, plan, offset_index):
    """Classify observed counts; correctness requires the stated uniform event."""
    old = predecessor()
    old.positive(sample_count, "sample count")
    if any(type(label) is not int or not 0 <= label < plan["dimension"] for label in counts):
        raise ValueError("basis labels outside dimension")
    for count in counts.values():
        old.positive(count, "observed count")
    if sum(counts.values()) != sample_count:
        raise ValueError("counts must include every sample, including background")
    choices, h = plan["grid_choices"], plan["bin_width"]
    if type(offset_index) is not int or not 0 <= offset_index < choices:
        raise ValueError("actual grid index required")
    cutoff = h+F(offset_index, choices)*h
    colors = {}
    for label, count in counts.items():
        value = F(count, sample_count)
        if value >= cutoff:
            colors[label] = (value-cutoff)//h
    return colors


def centered_tail_reference(buckets, background, contrast_rank):
    """Exact singular-value tail for a supplied compressed spectrum only."""
    remaining = contrast_rank
    tail = F(0)
    for deviation, count in sorted(((abs(value-background), count) for value, count in buckets), reverse=True):
        removed = min(remaining, count)
        remaining -= removed
        tail += (count-removed)*deviation
    return tail


def coarsen_reference(buckets, plan, offset_index, *, proof_background):
    """Weighted exact spectrum; never given to the proposed source algorithm."""
    old = predecessor()
    checked = []
    for value, count in buckets:
        old.positive(count, "multiplicity")
        if not isinstance(value, (F, int)) or isinstance(value, bool) or value < 0:
            raise ValueError("nonnegative exact rational eigenvalue required")
        checked.append((F(value), count))
    if sum(count for _, count in checked) != plan["dimension"]:
        raise ValueError("spectrum dimension mismatch")
    if sum(value*count for value, count in checked) != 1:
        raise ValueError("normalized spectrum required")
    if not isinstance(proof_background, (F, int)) or isinstance(proof_background, bool) or proof_background < 0:
        raise ValueError("nonnegative exact rational proof background required")
    choices, h = plan["grid_choices"], plan["bin_width"]
    if type(offset_index) is not int or not 0 <= offset_index < choices:
        raise ValueError("actual grid index required")
    small = plan["branch"] == "POLYNOMIAL_DIMENSION"
    background = F(0) if small else F(proof_background)
    tail = centered_tail_reference(checked, background, plan["contrast_rank"])
    if not small:
        if background > plan["unknown_background_upper"] or tail > plan["contrast_trace_residual_promise"]:
            raise ValueError("reference witness violates centered compressibility promise")
    cutoff = h+F(offset_index, choices)*h
    bins, rows = {}, []
    loss = contrast_mass = F(0)
    near = 0
    bad = False
    for value, count in checked:
        coordinate = (value-cutoff)/h
        lower = coordinate.numerator//coordinate.denominator
        nearest = min(abs(value-cutoff-j*h) for j in {max(0, lower), max(0, lower+1)})
        bad |= nearest <= plan["boundary_margin"]
        near += count if value >= h-plan["boundary_margin"] else 0
        label = lower if value >= cutoff else None
        rounded = cutoff+lower*h if label is not None else background
        if label is not None:
            bins[label] = bins.get(label, 0)+count
            contrast_mass += (rounded-background)*count
        loss += abs(value-rounded)*count
        rows.append({"value": value, "multiplicity": count, "bin": label, "proof_rounded_value": rounded})
    return {"status": "SUPPLIED_COMPRESSED_SPECTRUM_REFERENCE_ONLY",
            "rows": rows, "bins": bins, "bad_grid": bad,
            "centered_tail": tail, "proof_trace_norm_loss": loss,
            "contrast_trace": contrast_mass, "retained_rank": sum(bins.values()),
            "near_boundary_rank": near, "all_bins_empty": not bins,
            "empty_decision_if_promises_hold": "RETURN_WHOLE_PUBLIC_GROUP" if not bins else None}


def full_rank_control(dimension=2**256):
    rank, delta, weight = 3, F(1, 10), F(4, 5)
    plan = contract_plan(dimension, rank, delta, F(1, 16))
    background = weight/dimension
    reference = coarsen_reference([(background+(1-weight)/rank, rank), (background, dimension-rank)],
        plan, plan["grid_choices"]//3, proof_background=background)
    return {"dimension": dimension, "full_state_rank": dimension,
            "background_mass": weight, "plan": plan, "reference": reference,
            "known_diagonal_basis_is_classically_easy": True,
            "classical_baseline": classical_sample_plan(plan, F(1, 32))}


def empty_control():
    dimension = 2**128
    plan = contract_plan(dimension, 1, F(1, 2), F(1, 16))
    return coarsen_reference([(F(1, dimension), dimension)], plan,
        plan["grid_choices"]//3, proof_background=F(1, dimension))


def high_rank_bias_falsifier():
    dimension, rank, alpha = 2**128, 3, F(1, 4)
    plan = contract_plan(dimension, rank, alpha, F(1, 16))
    return {"dimension": dimension, "true_translation_gap": alpha,
            "both_eigenvalues_below_cutoff": (1+alpha)/dimension < plan["bin_width"],
            "optimal_centered_rank_residual": alpha*(1-F(2*rank, dimension)),
            "allowed_residual": plan["contrast_trace_residual_promise"],
            "global_gap_alone_does_not_authorize_source": True}


def broken_symmetry_falsifier():
    delta, tau = F(1, 4), F(1, 2**40)
    # C3 permutes a formerly flat three-dimensional block.
    spectrum = (F(1, 3)+tau, F(1, 3), F(1, 3)-tau)
    distance = predecessor().diagonal_distance(spectrum, (1, 2, 0))
    return {"formerly_symmetric_generator_is_now_outside_H": distance > 0,
            "actual_outside_distance": distance, "invalid_old_gap": delta,
            "new_gap_promise_is_false": distance < delta,
            "arbitrary_noise_correction_claim_rejected": True}


def noncommuting_control():
    """27-dimensional active block + implicit scalar complement, not acquisition."""
    elements = tuple(product(range(3), repeat=3))
    index = {g: i for i, g in enumerate(elements)}
    multiply = lambda g, h: ((g[0]+h[0]) % 3, (g[1]+h[1]) % 3,
                            (g[2]+h[2]+g[0]*h[1]) % 3)
    hidden = {(a, 0, 0) for a in range(3)}
    dimension, delta = 2**40, F(1, 10)
    weight, noise = F(4, 5), delta/512
    signal = 1-weight-noise
    background = float(weight/dimension)
    rho0 = np.eye(27)*background
    perturbation = np.zeros((27, 27))
    for element in hidden:
        i, j = index[element], index[multiply(element, (0, 1, 0))]
        rho0[i, i] += float(signal/3)
        perturbation[np.ix_([i, j], [i, j])] += float(noise/6)
    rho = rho0+perturbation
    plan = contract_plan(dimension, 3, delta, F(1, 16))
    eigenvalues, vectors = np.linalg.eigh(rho)
    h = float(plan["bin_width"])
    cutoff = h*(1+float(F(plan["grid_choices"]//3, plan["grid_choices"])))
    bins = {}
    rounded = np.eye(27)*background
    for i, value in enumerate(eigenvalues):
        if value >= cutoff:
            label = int(np.floor((value-cutoff)/h))
            bins.setdefault(label, []).append(i)
            rounded += (cutoff+label*h-background)*np.outer(vectors[:, i], vectors[:, i])
    norm1 = lambda matrix: float(np.abs(np.linalg.eigvalsh(matrix)).sum())
    actual, packet, outside = [], [], []
    for element in elements:
        permutation = [index[multiply(element, g)] for g in elements]
        U = np.eye(27)[:, permutation]
        distance = norm1(rho-U@rho@U.T)/2
        overlap = 1.0
        for indices in bins.values():
            frame = vectors[:, indices]
            overlap *= abs(np.linalg.det(frame.T@U@frame))
        if distance < 1e-12:
            actual.append(element)
        else:
            outside.append((distance, overlap))
        if abs(overlap-1) < 1e-9:
            packet.append(element)
    return {"status": "FLOATING_ACTIVE_BLOCK_CONTROL_NOT_QUANTUM_EXECUTION",
            "implicit_full_rank": dimension, "active_block_dimension": 27,
            "branch": plan["branch"], "promised_gap": delta,
            "contrast_rank": 3, "retained_rank": sum(map(len, bins.values())),
            "noncommuting_approximant_commutator_norm": float(np.linalg.norm(rho@rho0-rho0@rho)),
            "approximation_trace_residual": norm1(perturbation),
            "allowed_trace_residual": plan["contrast_trace_residual_promise"],
            "coarsening_trace_error": norm1(rho-rounded),
            "coarsening_error_bound": plan["coarsening_trace_norm_upper"],
            "minimum_outside_distance": min(row[0] for row in outside),
            "maximum_outside_wedge_modulus": max(row[1] for row in outside),
            "original_packet_and_expected_H_equal": actual == packet and set(actual) == hidden,
            "hidden_subgroup_order": len(hidden),
            "hidden_subgroup_is_nonnormal": any(
                multiply(g, h) not in {multiply(k, g) for k in hidden} for g in elements for h in hidden),
            "not_a_hard_family_or_classical_lower_bound": True}

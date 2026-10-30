"""Conditional copy/query ledgers and capped controls, not a quantum learner."""

from fractions import Fraction as F
from functools import lru_cache
import importlib.util
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent


@lru_cache(maxsize=None)
def dependency(name):
    paths = {
        "coarse": "rees-coarse-spectrum-2026-10-24/coarse_spectrum.py",
        "dilation": "rees-dilation-average-2026-10-25/dilation_average.py",
    }
    spec = importlib.util.spec_from_file_location("mixed_average_" + name, ROOT.parent / paths[name])
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def source_plan(*, p, nilpotency_class, rank_cap, twirl_gap, error,
                receiver_leaves, design_size, cover_order_bits):
    coarse, dilation = dependency("coarse"), dependency("dilation")
    dilation.theorem_gap(p)
    if type(nilpotency_class) is not int or not 1 <= nilpotency_class <= 3:
        raise ValueError("only classes one through three are covered")
    delta = coarse.probability(twirl_gap, "subgroup twirl gap")
    eps = coarse.probability(error, "error")
    if eps == 1:
        raise ValueError("error must be strictly less than one")
    # Reuse only the old clock arithmetic, NOT its pointwise-gap theorem.
    out = coarse.source_plan(rank_cap=rank_cap, orbit_gap=delta/4, error=eps,
        receiver_leaves=receiver_leaves, design_size=design_size,
        cover_order_bits=cover_order_bits)
    charged_gap = out.pop("ray_gap_lower")
    out.pop("orbit_gap")
    out.pop("off_group_projector_operator_gap_lower")
    scales = receiver_leaves * out["amplification_blocks_per_leaf"]
    trials = coarse.ceil_log2(32*scales/eps)
    out.update({
        "p": p, "nilpotency_class": nilpotency_class,
        "subgroup_twirl_gap_promise": delta,
        "pure_packet_twirl_gap_lower": delta/2,
        "curve_overlap_gap_lower": delta*delta/64,
        "charged_amplification_gap_lower": charged_gap,
        "random_scale_count": scales, "random_scale_trial_cap": trials,
        "random_scale_bit_cap": scales*trials*p.bit_length(),
        "random_scale_abort_budget": eps/32,
        "total_allocated_error_upper": 29*eps/32,
        "grid_reused_across_all_sources": True,
        "fresh_scale_per_moment_packet_required": True,
        "source_independence": "conditional on one correct grid/metadata record",
        "pointwise_orbit_gap_required": False,
        "query_interface": "uniform coherent SELECT(U)",
        "total_gate_cost_certified": False,
        "unpriced_resources": [
            "native width q and acquisition cost for every raw mixed copy",
            "uniform SELECT(U) implementation at the allocated half-diamond precision",
            "DME, QPE, growth gates, public arithmetic, grid and random-bit generation",
            "valid zero-moment design and complete charged Rees receiver",
        ],
        "independent_review_of_this_composition": False,
        "native_application_established": False,
    })
    return out


def marginal(state, dimension, registers, keep):
    """Finite partial trace control with an explicit dense-size cap."""
    if type(dimension) is not int or dimension < 1 or type(registers) is not int or registers < 1:
        raise ValueError("positive dimensions required")
    size = dimension**registers
    if size > 256 or state.shape != (size, size) or not 0 <= keep < registers:
        raise ValueError("invalid or oversized dense control")
    others = [i for i in range(registers) if i != keep]
    axes = [keep] + others + [registers+keep] + [registers+i for i in others]
    tensor = state.reshape((dimension,)*(2*registers)).transpose(axes)
    tensor = tensor.reshape(dimension, size//dimension, dimension, size//dimension)
    return np.einsum("aibi->ab", tensor)


def decode_reference(state, dimension, bin_ranks, bin_weights):
    """Weighted one-register partial traces; no eigenbasis enters this channel."""
    if not bin_ranks or len(bin_ranks) != len(bin_weights):
        raise ValueError("nonempty matching bin ranks and weights required")
    if any(type(r) is not int or r < 1 for r in bin_ranks):
        raise ValueError("positive bin ranks required")
    if any(not isinstance(w, (int, F)) or isinstance(w, bool) or w <= 0 for w in bin_weights):
        raise ValueError("positive exact bin probabilities required")
    if sum(bin_weights) != 1:
        raise ValueError("bin probabilities must sum to one")
    result = np.zeros((dimension, dimension), dtype=complex)
    start = 0
    for rank, weight in zip(bin_ranks, bin_weights):
        result += float(weight)*marginal(state, dimension, sum(bin_ranks), start)
        start += rank
    return result


def packet_reference(spectrum, frame, delta=F(1, 4), error=F(1, 16), offset_index=None):
    """Supplied-spectrum diagnostic, NEVER native spectral acquisition."""
    coarse = dependency("coarse")
    delta = coarse.probability(delta, "subgroup twirl gap")
    dimension = len(spectrum)
    if frame.shape != (dimension, dimension) or not np.allclose(frame.conj().T@frame, np.eye(dimension)):
        raise ValueError("unitary reference frame required")
    plan = coarse.grid_plan(dimension, delta/4, error)
    offset = plan["grid_choices"]//4 if offset_index is None else offset_index
    rounded = coarse.coarsen_reference(spectrum, plan, offset)
    bins = list(rounded["bins"].values())
    ranks = tuple(len(indices) for indices in bins)
    if dimension**sum(ranks) > 256:
        raise ValueError("dense packet calibration cap exceeded")
    mass = sum(rounded["rounded"])
    weights = tuple(rounded["rounded"][indices[0]]*len(indices)/mass for indices in bins)
    packet = np.ones(1, dtype=complex)
    for indices in bins:
        packet = np.kron(packet, coarse.support_module().wedge_vector(frame[:, indices]))
    return {
        "rho": frame@np.diag([float(x) for x in spectrum])@frame.conj().T,
        "rounded_density": frame@np.diag([float(x) for x in rounded["rounded"]])@frame.conj().T,
        "packet": np.outer(packet, packet.conj()), "ranks": ranks, "weights": weights,
        "mass": mass, "loss": rounded["trace_norm_loss"], "bad_grid": rounded["bad_grid"],
        "supplied_frame_is_diagnostic_only": True,
    }


def adjacent_mixed_control(p=131):
    dilation = dependency("dilation")
    dilation.theorem_gap(p)
    frame = np.array([[1, 1], [1, -1]], dtype=complex)/np.sqrt(2)
    ref = packet_reference((F(3, 4), F(1, 4)), frame)
    sigma = ref["packet"]
    U = np.diag([1, np.exp(2j*np.pi/p)])
    primitive = dependency("coarse").support_module()
    rho = ref["rho"]
    mixed_twirl = np.diag(np.diag(rho))
    output = decode_reference(sigma, 2, ref["ranks"], ref["weights"])
    twirled_packet = np.zeros_like(sigma)
    for t in range(p):
        u = np.diag([1, np.exp(2j*np.pi*t/p)])
        action = primitive.tensor_power(u, 2)
        twirled_packet += action@sigma@action.conj().T/p
    decoded_twirl = decode_reference(twirled_packet, 2, ref["ranks"], ref["weights"])
    distance = primitive.trace_distance
    return {
        "p": p, "mixed_rank": 2,
        "subgroup_twirl_distance_exact": "1/4",
        "old_minimum_pointwise_distance": float(np.sin(np.pi/p)/2),
        "pointwise_formula_error": abs(distance(rho, U@rho@U.conj().T)-np.sin(np.pi/p)/2),
        "mixed_twirl_formula_error": abs(distance(rho, mixed_twirl)-.25),
        "decode_identity_error": float(np.linalg.norm(output-ref["rounded_density"]/float(ref["mass"]))),
        "twirl_covariance_error": float(np.linalg.norm(decoded_twirl-np.diag(np.diag(output)))),
        "packet_twirl_distance": distance(sigma, twirled_packet),
        "decoded_twirl_distance": distance(output, decoded_twirl),
        "transferred_lower_bound": str((F(1, 4)-ref["loss"])/ref["mass"]),
        "packet_twirl_fidelity": float(np.trace(sigma@twirled_packet).real),
        "packet_twirl_fidelity_exact": "3/8",
        "classically_easy_calibration_not_algorithm_candidate": True,
    }

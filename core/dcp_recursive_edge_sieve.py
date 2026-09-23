"""Symmetric edge preparation as a clean, recursively composable DCP sieve.

This is a locally derived, review-pending baseline, not a new speedup. Two
actual support-register preparations give equal endpoint amplitudes. Natural
high labels stay uniform; failed attempts and recursive sample costs count.
"""

from __future__ import annotations

from fractions import Fraction
from functools import lru_cache
from itertools import product
from math import isqrt, log2

import numpy as np

from dcp_affine_marked_pairing import _jsonable
from dcp_balanced_pairing import BalancedPairingProgram, balanced_certificate
from dcp_coherent_edge_sampling import marked_amplitude, support_from_index


SUCCESS_LOWER = Fraction(1, 1 << 17)


@lru_cache(maxsize=2048)
def merge_certificate(low_bits: int) -> dict:
    if type(low_bits) is not int or low_bits < 2:
        raise ValueError("balanced merging requires at least two low bits")
    family = balanced_certificate(low_bits, 2*low_bits)
    padded = 1 << (family["supports"]-1).bit_length()
    iterations = isqrt(padded)//8
    lam = family["mean_degree"]
    good_mass = lam-family["degree_second_moment"]/4
    return {"low_bits": low_bits, "input_states": 2*low_bits,
            "support_weight": family["radius"],
            "block_weight": family["per_block_weight"],
            "list_length": family["each_list_length"],
            "supports": family["supports"], "padded_supports": padded,
            "iterations_per_preparation": iterations,
            "boolean_predicate_calls_per_attempt": 4*iterations+2,
            "mean_degree": lam, "degree_second_moment": family["degree_second_moment"],
            "bounded_degree_oriented_mass_lower": good_mass,
            "bounded_degree_amplitude_lower": Fraction(1, 16),
            "success_lower": SUCCESS_LOWER,
            "source_success_lower_from_moments": good_mass/Fraction(16**4),
            "all_failures_consume_input_batch": True,
            "ideal_inputs_only": True, "novelty_established": False}


def _finite_graph(labels: tuple[int, ...], n_bits: int, low_bits: int):
    if (type(n_bits) is not int or type(low_bits) is not int
            or not 2 <= low_bits < n_bits or len(labels) != 2*low_bits
            or any(type(a) is not int or not 0 <= a < 1 << n_bits for a in labels)):
        raise ValueError("require 2r natural labels modulo 2^n and 2 <= r < n")
    cert = merge_certificate(low_bits)
    size, padded = 1 << len(labels), cert["padded_supports"]
    if size*padded*padded > 65536:
        raise ValueError("explicit finite-state diagnostic budget exceeded")
    program = BalancedPairingProgram(tuple(a % (1 << low_bits) for a in labels),
                                     low_bits, cert["block_weight"], (), 0)
    masks = [support_from_index(program, j) for j in range(padded)]
    marked = np.zeros((size, padded), dtype=bool)
    endpoints = np.zeros((size, padded), dtype=int)
    for b in range(size):
        for j, support in enumerate(masks):
            endpoints[b, j] = b ^ (support or 0)
            if support is not None:
                delta = sum((-a if b & (1 << i) else a)
                            for i, a in enumerate(labels) if support & (1 << i))
                marked[b, j] = delta % (1 << low_bits) == 0
    return masks, marked, endpoints


def double_endpoint_kernel(labels: tuple[int, ...], n_bits: int, low_bits: int,
                           iterations: int, second_iterations: int | None = None):
    """Execute both oracle/reflection preparations on explicit (b,j,k) wires.

    The diagnostic uses dense arrays; the described quantum algorithm does
    not store these arrays or endpoint tables. k==j heralds clean k xor j=0.
    """
    if second_iterations is None:
        second_iterations = iterations
    if any(type(t) is not int or not 0 <= t <= 64 for t in (iterations, second_iterations)):
        raise ValueError("finite diagnostic requires iteration counts in 0..64")
    masks, marked, endpoints = _finite_graph(labels, n_bits, low_bits)
    size, padded = marked.shape
    first = np.full((size, padded), 1/np.sqrt(padded))
    for _ in range(iterations):
        first *= np.where(marked, -1, 1)
        first = 2*first.mean(axis=1, keepdims=True)-first
    first *= marked
    first_success = float(np.sum(first*first)/size)
    state = np.repeat(first[:, :, None]/np.sqrt(padded), padded, axis=2)
    second_oracle = marked[endpoints, :]
    for _ in range(second_iterations):
        state *= np.where(second_oracle, -1, 1)
        state = 2*state.mean(axis=2, keepdims=True)-state
    # Project k xor j onto zero. Its known-zero register carries no endpoint tag.
    accepted = state[:, np.arange(padded), np.arange(padded)].copy()
    accepted *= marked  # Symmetry also verifies the second endpoint.
    return accepted, masks, marked, endpoints, first_success


def physical_merge(labels: tuple[int, ...], n_bits: int, low_bits: int,
                   iterations: int, secret: int, eta: float = 1.,
                   second_iterations: int | None = None) -> dict:
    if type(secret) is not int or not 0 <= secret < 1 << n_bits or not 0 <= eta <= 1:
        raise ValueError("invalid secret or independent dephasing visibility")
    accepted, masks, marked, endpoints, first_success = double_endpoint_kernel(
        labels, n_bits, low_bits, iterations, second_iterations)
    size, padded = marked.shape
    degrees = marked.sum(axis=1).tolist()
    residues = [sum(a for i, a in enumerate(labels) if b & (1 << i)) % (1 << n_bits)
                for b in range(size)]
    psi = np.exp(2j*np.pi*secret*np.array(residues)/(1 << n_bits))/np.sqrt(size)
    source = np.outer(psi, psi.conj())
    source *= np.array([[eta**(b ^ c).bit_count() for c in range(size)] for b in range(size)])
    outputs: dict[int, np.ndarray] = {}
    symmetry_error = formula_error = clean_error = model_error = 0.
    total_success = 0.
    t2 = iterations if second_iterations is None else second_iterations
    for b in range(size):
        for j, support in enumerate(masks):
            if not marked[b, j]:
                continue
            c = int(endpoints[b, j])
            expected = (marked_amplitude(degrees[b], padded, iterations)
                        * marked_amplitude(degrees[c], padded, t2))
            formula_error = max(formula_error, abs(accepted[b, j]-expected))
            symmetry_error = max(symmetry_error, abs(accepted[b, j]-accepted[c, j]))
            if b & (support & -support):
                continue
            delta = (residues[c]-residues[b]) % (1 << n_bits)
            assert delta % (1 << low_bits) == 0
            amp = np.array([accepted[b, j], accepted[c, j]])
            actual = source[np.ix_([b, c], [b, c])]*np.outer(amp, amp)
            probability = float(np.trace(actual).real)
            phase = np.array([1., np.exp(2j*np.pi*secret*delta/(1 << n_bits))])/np.sqrt(2)
            ideal = probability*np.outer(phase, phase.conj())
            clean_error = max(clean_error, float(np.max(abs(actual-ideal))))
            dephased = ideal.copy()
            dephased[0, 1] *= eta**support.bit_count()
            dephased[1, 0] *= eta**support.bit_count()
            model_error = max(model_error, float(np.max(abs(actual-dephased))))
            total_success += probability
            outputs.setdefault(delta >> low_bits, np.zeros((2, 2), dtype=complex))
            outputs[delta >> low_bits] += actual
    return {"labels": list(labels), "n_bits": n_bits, "low_bits": low_bits,
            "iterations": iterations, "second_iterations": t2, "secret": secret, "eta": eta,
            "first_herald_probability": first_success, "success_probability": total_success,
            "success_residual": abs(total_success-float(np.sum(accepted*accepted)/size)),
            "amplitude_formula_residual": float(formula_error),
            "endpoint_amplitude_residual": float(symmetry_error),
            "clean_phase_state_residual": clean_error, "dephased_phase_state_residual": model_error,
            "output_label_probabilities": {str(k): float(np.trace(v).real) for k, v in outputs.items()},
            "conditional_normalization_used": False, "endpoint_specific_records_retained": False}


def natural_label_control() -> dict:
    """Exhaust all 8^4 labels, including every high lift of each low transcript."""
    n_bits, low_bits, size, padded = 3, 2, 16, 4
    first_moment = second_moment = good_mass = 0
    uniform_error = 0.
    success_sums = {t: 0. for t in (0, 1, 2)}
    for lows in product(range(4), repeat=4):
        for t in success_sums:
            amp, masks, marked, endpoints, _ = double_endpoint_kernel(lows, n_bits, low_bits, t)
            if t == 0:
                degrees = marked.sum(axis=1)
                first_moment += int(degrees.sum())
                second_moment += int(np.sum(degrees*degrees))
                good_mass += sum(degrees[b] <= 8 and degrees[endpoints[b, j]] <= 8
                                 for b in range(size) for j in range(padded) if marked[b, j])
            bins = np.zeros(2)
            for highs in product(range(2), repeat=4):
                labels = [a+4*h for a, h in zip(lows, highs)]
                for b in range(size):
                    for j, support in enumerate(masks):
                        if not marked[b, j] or b & (support & -support):
                            continue
                        delta = sum((-a if b & (1 << i) else a)
                                    for i, a in enumerate(labels) if support & (1 << i)) % 8
                        bins[delta//4] += 2*amp[b, j]**2/size/16
            uniform_error = max(uniform_error, float(abs(bins[0]-bins[1])))
            success_sums[t] += float(bins.sum())/256
    count = 256*size
    return {"full_label_tuples": 4096, "low_transcripts": 256,
            "mean_degree": Fraction(first_moment, count),
            "degree_second_moment": Fraction(second_moment, count),
            "bounded_degree_edge_mass": Fraction(good_mass, count),
            "maximum_conditional_high_label_mass_difference": uniform_error,
            "success_by_shared_iterations": success_sums,
            "checks": {"mean": first_moment == count,
                       "second_moment": Fraction(second_moment, count) == Fraction(7, 4),
                       "uniform_for_every_low_transcript": uniform_error < 1e-12,
                       "zero_step_success": abs(success_sums[0]-1/16) < 1e-12,
                       "charged_constant_success": success_sums[0] >= float(SUCCESS_LOWER)}}


def recursive_blocks(n_bits: int, block_bits: int) -> list[int]:
    if type(n_bits) is not int or n_bits < 3 or type(block_bits) is not int or block_bits < 2:
        raise ValueError("require n >=3 and block size >=2")
    blocks = [block_bits]*((n_bits-1)//block_bits)
    remainder = (n_bits-1) % block_bits
    if remainder == 1 and blocks:
        blocks[-1] += 1
    elif remainder:
        blocks.append(remainder)
    return blocks


def _logadd(left: float, right: float) -> float:
    high, low = max(left, right), min(left, right)
    return high+log2(1+2**(low-high))


def recursive_resources(n_bits: int, block_bits: int) -> dict:
    blocks = recursive_blocks(n_bits, block_bits)
    log_samples = log_work = 0.
    support_product = 1
    rows = []
    for r in blocks:
        cert = merge_certificate(r)
        log_retry = -log2(float(SUCCESS_LOWER))
        log_samples += log2(2*r)+log_retry
        log_work = _logadd(log2(2*r)+log_work,
                           log2(cert["boolean_predicate_calls_per_attempt"]))+log_retry
        support_product *= cert["support_weight"]
        rows.append({"new_zero_bits": r, "input_states": 2*r,
                     "success_lower": SUCCESS_LOWER,
                     "log2_expected_fresh_states_upper": log_samples,
                     "log2_expected_work_units_upper": log_work})
    # Final uniform Z_2 label is 1 with probability 1/2; label zero is discarded.
    log_samples += 1
    log_work += 1
    max_block = max(blocks)
    # A common coarse bound covers every smaller modulus in full-secret recovery.
    depth_bound = (n_bits-2)//block_bits+1
    max_fanout = 2*(min(n_bits-1, block_bits+1))
    max_call = max(merge_certificate(r)["boolean_predicate_calls_per_attempt"]
                   for r in range(2, min(n_bits-1, block_bits+1)+1))
    full_log = (log2(2*n_bits)+depth_bound*log2(max_fanout/float(SUCCESS_LOWER))
                +log2(1+max_call))
    return {"n_bits": n_bits, "block_bits": block_bits, "blocks": blocks, "levels": rows,
            "log2_expected_parity_fresh_states_upper": log_samples,
            "log2_expected_parity_work_units_upper": log_work,
            "log2_expected_full_secret_work_units_upper": full_log,
            "peak_retained_phase_qubits_upper": sum(2*r for r in blocks),
            "public_label_storage_bits_upper": 2*n_bits*(n_bits-1),
            "additional_workspace": "poly(n,max block); two index registers and reversible arithmetic, not lists",
            "independent_input_visibility_power": support_product,
            "log2_output_visibility_at_inverse_n_dephasing": support_product*log2(1-1/n_bits),
            "maximum_block": max_block,
            "primitive_cost_unit": "one fresh input or one reversible Boolean predicate call; polynomial arithmetic factors excluded explicitly",
            "expected_cost_not_worst_case": True, "analytical_not_large_quantum_execution": True,
            "noise_robustness_established": False, "polynomial_time_claimed": False,
            "novel_speedup_claim_allowed": False}


def build_recursive_edge_audit() -> dict:
    physical = [physical_merge(labels, n, r, t, secret, eta)
                for labels, n, r in (((0, 1, 1, 1), 3, 2), ((0, 1, 2, 3), 3, 2),
                                     ((1, 1, 1, 1), 3, 2), ((0, 1, 2, 3, 4, 5), 4, 3))
                for t in (0, 1, 2) for secret in (0, 1, (1 << n)-1) for eta in (1., .75)]
    asymmetric = physical_merge((0, 1, 1, 1), 3, 2, 0, 1, second_iterations=1)
    natural = natural_label_control()
    scaling = []
    for n in (16, 32, 64, 128, 256, 512):
        rows = [recursive_resources(n, r) for r in range(2, n)]
        best = min(rows, key=lambda x: x["log2_expected_parity_work_units_upper"])
        scaling.append(best)
    failures = sum(max(row["success_residual"], row["amplitude_formula_residual"],
                       row["endpoint_amplitude_residual"], row["dephased_phase_state_residual"]) > 1e-10
                   or row["success_probability"] > row["first_herald_probability"]+1e-12
                   or (row["eta"] == 1. and row["clean_phase_state_residual"] > 1e-10)
                   for row in physical)
    failures += not all(natural["checks"].values())
    failures += asymmetric["endpoint_amplitude_residual"] < 1e-8
    failures += any(merge_certificate(r)["source_success_lower_from_moments"] < SUCCESS_LOWER
                    for r in range(2, 513))
    return _jsonable({"physical_controls": physical, "natural_label_control": natural,
                      "unequal_schedule_counterexample": asymmetric, "scaling": scaling,
                      "control_failures": int(failures),
                      "status": "derived-clean-recursive-sieve-known-asymptotic-review-pending",
                      "contract": {
                          "merge": "Run the SAME support preparation at b and b xor S_j; herald the second index equals j, then retain common representative/index and orientation. Accepted amplitude is g(q_b)g(q_c), exactly symmetric.",
                          "distribution": "The predicate uses only r low label bits. Conditioned on all low data and successful common-label outcomes, unused high bits give a uniform output quotient label. Fresh disjoint attempts restore iid ideal phase states.",
                          "success": "For m=2r,r>=2, D=L^2,P=nextpower2(D), t=floor(sqrt(P)/8), natural success >=2^-17. No vertex isolation, degree oracle, unknown-state reflection or uncharged postselection.",
                          "recurrence": "S_i<=2r_i*S_(i-1)/p0; W_i<=(2r_i*W_(i-1)+4t_i+2)/p0. Final nonzero Z_2 label costs factor two. All failed batches are charged.",
                          "asymptotic": "r=Theta(sqrt(n log n)) gives expected time and fresh states 2^O(sqrt(n log n)), polynomial workspace, IDEAL independent phase-state source only. Same asymptotic class as Regev, not an improvement claim.",
                          "noise": "For independent label-independent input visibility eta and fixed support weights w_i, output visibility is eta^(product w_i), not eta. Symmetrization removes amplitude imbalance, not physical dephasing; inverse-n noise need not survive recursion.",
                          "full_secret": "Known low-bit phase corrections and fresh uniform labels reduce to smaller moduli. Polynomial factors, rotation precision and expectation-to-bounded-error conversion remain explicit; no gate exporter supplied.",
                          "novelty_established": False, "independently_reviewed": False,
                          "speedup_claim_allowed": False, "noise_robustness_established": False,
                          "gate_export_implemented": False},
                      "literature": [
                          {"url": "https://arxiv.org/abs/quant-ph/0406151", "role": "Prior polynomial-space recursive sieve and 2^O(sqrt(n log n)) baseline, Section 3."},
                          {"url": "https://arxiv.org/abs/1112.3333", "role": "Prior collimation and time/space tradeoffs; no frontier improvement inferred."},
                          {"url": "https://arxiv.org/abs/2206.14408", "role": "Prior DCP time/query tradeoffs; linear samples per merge are not linear total samples."}]})

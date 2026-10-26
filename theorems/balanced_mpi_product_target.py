"""Average-center transfer to a product-weight classical sampling target.

This is a conditional attack reduction, not a classical sampler or speedup.
Exact rational native bounds and finite numerical identity controls are separate.
Includes matched categorical heat-bath, parallel-tempering, and alternating
systematic-basis product-target campaigns on the frozen native m=6000, n=420
instance (seed 20261020), plus exact small-chain detailed-balance controls.
"""
from __future__ import annotations

import argparse
from fractions import Fraction as Q
import hashlib
from itertools import product
import json
from math import exp, sqrt
from pathlib import Path
import random
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from flint import nmod_mat
import numpy as np

from theorems import balanced_signed_mpi as mpi
from theorems.nonlinear_filter_pinning import enclose
from theorems.prime_character_finite_readout import sqrt_interval

REPORT = ROOT / "research/classical_baselines/balanced_mpi_product_target.json"
CENTER_MODEL = "independent_uniform_in_Z_N"


def transfer_certificate(length, evaluations, cap, t, *, center_model,
                         threshold=Q(3, 10), sampler_tv=Q(0),
                         exceptional_tv=Q(1, 100)):
    """Exact outward bounds; the sampling premise is an unproved condition."""
    if center_model != CENTER_MODEL:
        raise ValueError("independent uniform centers are required; code shifts do not suffice")
    if not isinstance(t, Q) or not 0 < t < Q(1, 3):
        raise ValueError("a rational active probability in (0,1/3) is required")
    if not isinstance(threshold, Q) or not -1 < threshold < 1:
        raise ValueError("rational threshold in (-1,1) required")
    if not isinstance(sampler_tv, Q) or not 0 <= sampler_tv <= 1:
        raise ValueError("rational sampler TV allowance in [0,1] required")
    if not isinstance(exceptional_tv, Q) or not 0 < exceptional_tv <= 1:
        raise ValueError("rational exceptional-center TV threshold in (0,1] required")
    cert = mpi.mean_certificate(length, evaluations, cap, t)
    z_lo, z_hi = (Q(cert[key]) for key in
                  ("normalization_lower", "normalization_upper"))
    if z_lo <= 0:
        raise ValueError("the retained source mass is too small for this certificate")
    ratio_hi = (1-z_lo)/z_lo
    tv_hi = min(Q(1), sqrt_interval(ratio_hi, 192)[1])
    mean_lo = Q(cert["mean_cosine_lower"])
    tail_lo = max(Q(0), (mean_lo-threshold)/(1-threshold))
    return {
        "length": length, "evaluations": evaluations, "cap_each_sign": cap,
        "active_probability": str(t), "center_model": center_model,
        "retained_mass_interval": [str(z_lo), str(z_hi)],
        "discarded_mass_upper": str(enclose(1-z_lo, upper=True)),
        "discarded_over_retained_upper": str(enclose(ratio_hi, upper=True)),
        "center_averaged_target_tv_upper": str(enclose(tv_hi, upper=True)),
        "exceptional_tv_threshold": str(exceptional_tv),
        "exceptional_center_probability_upper":
            str(enclose(min(Q(1), ratio_hi/exceptional_tv**2), upper=True)),
        "truncated_quantum_mean_lower": str(mean_lo),
        "score_threshold": str(threshold),
        "truncated_quantum_tail_lower": str(enclose(tail_lo)),
        "assumed_center_averaged_sampler_tv_upper": str(sampler_tv),
        "conditional_joint_success_lower":
            str(enclose(max(Q(0), tail_lo-tv_hi-sampler_tv))),
        "conditional_center_averaged_mean_lower":
            str(enclose(max(Q(-1), mean_lo-2*(tv_hi+sampler_tv)))),
        "sampling_premise_proved": False,
        "worst_case_center_guarantee": False,
        "gauge_randomization_supplies_center_model": False,
        "normalizer_needed_for_weight_ratios": False,
        "license": cert["license"],
    }


def product_log_weight(residuals, order, t):
    """Floating evaluation of a positive unnormalized density, not a sampler."""
    if type(order) is not int or order <= 3:
        raise ValueError("integer cyclic order greater than three required")
    if not isinstance(t, Q) or not 0 < t < Q(1, 3):
        raise ValueError("rational t in (0,1/3) keeps all local factors positive")
    values = np.asarray(residuals)
    if values.ndim != 1 or values.dtype.kind not in "iu":
        raise ValueError("one-dimensional integer residues required")
    factors = sqrt(float(1-t)) + sqrt(float(2*t))*np.cos(
        2*np.pi*(values % order)/order)
    if not np.isfinite(factors).all() or np.any(factors <= 0):
        raise ArithmeticError("positive product factor lost at this precision")
    return float(2*np.log(factors).sum())


def harmonic_certificate(length, t, harmonics):
    """Uniform log-density error, hence a stationary-law TV bound; no mixing claim."""
    if type(length) is not int or length < 1:
        raise ValueError("positive integer length required")
    if type(harmonics) is not int or harmonics < 0:
        raise ValueError("nonnegative integer harmonic count required")
    if not isinstance(t, Q) or not 0 < t < Q(1, 3):
        raise ValueError("rational t in (0,1/3) required")
    a_lo = sqrt_interval(1-t, 192)[0]
    d_lo = sqrt_interval(1-3*t, 192)[0]
    b_hi = sqrt_interval(2*t, 192)[1]
    r_hi = enclose(b_hi/(a_lo+d_lo), upper=True)
    if r_hi >= 1:
        raise ValueError("precision does not certify a convergent harmonic series")
    error = 4*length*r_hi**(harmonics+1)/((harmonics+1)*(1-r_hi))
    tv = Q(1) if 2*error >= 1 else min(Q(1), 2*error/(1-2*error))
    return {
        "length": length, "active_probability": str(t), "harmonics": harmonics,
        "geometric_ratio_upper": str(r_hi),
        "uniform_log_weight_error_upper": str(enclose(error, upper=True)),
        "stationary_target_tv_upper": str(enclose(tv, upper=True)),
        "bound": "TV <= exp(2*error)-1 <= 2*error/(1-2*error) when 2*error<1",
        "coefficient_accumulations_per_line": 2*length*harmonics,
        "line_work": "O(m*harmonics + N*log(N)); slopes and residuals must be charged",
        "invertible_slopes_required": False,
        "floating_fft_roundoff_certified": False,
        "mixing_time_proved": False,
    }


def harmonic_line_log_weights(residuals, slopes, order, t, harmonics):
    """All N truncated log weights on a line; retains nonunit/zero-slope aliases."""
    harmonic_certificate(len(residuals), t, harmonics)
    if type(order) is not int or order <= 3:
        raise ValueError("integer cyclic order greater than three required")
    residues, directions = np.asarray(residuals), np.asarray(slopes)
    if (residues.ndim != 1 or directions.shape != residues.shape
            or residues.dtype.kind not in "iu" or directions.dtype.kind not in "iu"):
        raise ValueError("matching one-dimensional integer residuals and slopes required")
    residues = (residues % order).astype(np.int64)
    directions = (directions % order).astype(np.int64)
    a, d, b = sqrt(float(1-t)), sqrt(float(1-3*t)), sqrt(float(2*t))
    ratio = b/(a+d)
    spectrum = np.zeros(order, dtype=np.complex128)
    for k in range(1, harmonics+1):
        frequencies = (k*directions) % order
        terms = (2*(-1)**(k+1)*ratio**k/k *
                 np.exp(2j*np.pi*(k*residues % order)/order))
        np.add.at(spectrum, frequencies, terms)
        np.add.at(spectrum, (-frequencies) % order, terms.conjugate())
    values = np.fft.ifft(spectrum)*order
    if np.max(abs(values.imag)) > 1e-9*max(1.0, float(np.max(abs(values.real)))):
        raise ArithmeticError("real line density acquired a significant imaginary part")
    return values.real + 2*len(residues)*np.log((a+d)/2)


def categorical_line_probabilities(log_weights, beta=1.0):
    """Normalized tempered categorical distribution on a coordinate line."""
    weights = np.asarray(log_weights, dtype=np.float64)
    if weights.ndim != 1 or len(weights) < 2 or not np.isfinite(weights).all():
        raise ValueError("finite one-dimensional line log weights required")
    if not isinstance(beta, (int, float, Q)) or float(beta) <= 0:
        raise ValueError("positive inverse temperature beta required")
    scaled = float(beta)*weights
    shifted = np.exp(scaled-np.max(scaled))
    total = float(shifted.sum())
    if not np.isfinite(total) or total <= 0:
        raise ArithmeticError("categorical normalization failed")
    return shifted/total


def sample_categorical_step(probabilities, rng):
    """Sample an integer shift step in 0..N-1 from a normalized categorical law."""
    probs = np.asarray(probabilities, dtype=np.float64)
    if probs.ndim != 1 or len(probs) < 2 or any(probs < 0):
        raise ValueError("nonnegative one-dimensional categorical probabilities required")
    cdf = np.cumsum(probs)
    u = rng.random()*float(cdf[-1])
    step = int(np.searchsorted(cdf, u, side="right"))
    return min(step, len(probs)-1)


def small_mcmc_stationary_and_detailed_balance_control():
    """Verify exact detailed balance, stationary histograms, and replica exchange on a 49-state control."""
    bits, m, n, order = 3, 4, 2, 7
    t, harmonics = Q(1, 20), 9
    supports, evaluations = mpi.points(bits, m, n)
    _, logs, _ = mpi.presentation(bits)
    B = np.array([[logs[a ^ z] for z in evaluations] for a in supports], dtype=np.int64)
    centers = np.array([0, 2, 4, 6], dtype=np.int64)
    states = [np.array(x, dtype=np.int64) for x in product(range(order), repeat=n)]
    state_index = {tuple(x.tolist()): idx for idx, x in enumerate(states)}

    exact_logs = np.array([
        product_log_weight((B @ x - centers) % order, order, t) for x in states
    ], dtype=np.float64)
    a, d, b = sqrt(float(1-t)), sqrt(float(1-3*t)), sqrt(float(2*t))
    ratio = b/(a+d)
    constant = 2*m*np.log((a+d)/2)
    harmonic_logs = np.array([
        constant + sum(
            4*(-1)**(k+1)*ratio**k/k *
            np.cos(2*np.pi*k*((B @ x - centers) % order)/order).sum()
            for k in range(1, harmonics+1)
        )
        for x in states
    ], dtype=np.float64)
    pi_exact = categorical_line_probabilities(exact_logs, beta=1.0)
    pi_harm = categorical_line_probabilities(harmonic_logs, beta=1.0)
    stationary_tv = float(np.sum(abs(pi_exact-pi_harm))/2)
    cert = harmonic_certificate(m, t, harmonics)
    if stationary_tv > float(Q(cert["stationary_target_tv_upper"])):
        raise ArithmeticError("small control violated harmonic stationary TV bound")

    # Build exact random-scan transition matrices for original and systematic bases
    inv_top = np.array(nmod_mat(B[:n].tolist(), order).inv().tolist(), dtype=np.int64)
    G_sys = (B @ inv_top) % order

    def build_transition_matrix(direction_columns, beta=1.0):
        P = np.zeros((len(states), len(states)), dtype=np.float64)
        for idx, x in enumerate(states):
            residuals = (B @ x - centers) % order
            for col in direction_columns:
                slopes = (B @ col) % order
                line_logs = harmonic_line_log_weights(residuals, slopes, order, t, harmonics)
                probs = categorical_line_probabilities(line_logs, beta=beta)
                for step, p_step in enumerate(probs):
                    y = tuple(((x + step*col) % order).tolist())
                    P[idx, state_index[y]] += p_step / len(direction_columns)
        return P

    orig_cols = [np.eye(n, dtype=np.int64)[:, j] for j in range(n)]
    sys_cols = [inv_top[:, j] for j in range(n)]
    P_orig = build_transition_matrix(orig_cols, beta=1.0)
    P_sys = build_transition_matrix(sys_cols, beta=1.0)

    db_orig = float(np.max(np.abs(pi_harm[:, None]*P_orig - pi_harm[None, :]*P_orig.T)))
    db_sys = float(np.max(np.abs(pi_harm[:, None]*P_sys - pi_harm[None, :]*P_sys.T)))

    # Empirical histogram vs stationary law for systematic heat bath
    rng = random.Random(202610203)
    x = np.zeros(n, dtype=np.int64)
    counts = np.zeros(len(states), dtype=np.int64)
    burn_in, total_samples = 1000, 14000
    for step_idx in range(burn_in + total_samples):
        col = sys_cols[rng.randrange(n)]
        residuals = (B @ x - centers) % order
        slopes = (B @ col) % order
        line_logs = harmonic_line_log_weights(residuals, slopes, order, t, harmonics)
        step = sample_categorical_step(categorical_line_probabilities(line_logs, beta=1.0), rng)
        x = (x + step*col) % order
        if step_idx >= burn_in:
            counts[state_index[tuple(x.tolist())]] += 1
    empirical = counts / float(total_samples)
    empirical_tv = float(np.sum(abs(empirical - pi_harm))/2)
    return {
        "field_bits": bits, "cyclic_order": order, "length": m, "evaluations": n,
        "states_enumerated": len(states),
        "harmonic_vs_exact_stationary_tv": stationary_tv,
        "certified_stationary_tv_upper": cert["stationary_target_tv_upper"],
        "max_detailed_balance_violation_original_basis": db_orig,
        "max_detailed_balance_violation_systematic_basis": db_sys,
        "systematic_chain_burn_in": burn_in,
        "systematic_chain_samples": total_samples,
        "empirical_histogram_tv_to_harmonic_stationary": empirical_tv,
        "G_systematic_top_block_is_identity": bool(np.array_equal(G_sys[:n], np.eye(n, dtype=np.int64))),
        "scope": "exact finite Markov-chain detailed-balance and stationary-histogram verification",
    }


def native_line_control():
    """One full-size conditional density, not a Markov chain or optimization run."""
    bits, m, n, t, harmonics = 13, 6000, 420, Q(1, 20), 9
    supports, evaluations = mpi.points(bits, m, n)
    _, logs, _ = mpi.presentation(bits)
    order = (1 << bits)-1
    rng = random.Random(20261020)
    centers = np.array([rng.randrange(order) for _ in range(m)], dtype=np.int64)
    residuals = (-centers) % order
    slopes = np.array([logs[a ^ evaluations[0]] for a in supports], dtype=np.int64)
    values = harmonic_line_log_weights(residuals, slopes, order, t, harmonics)
    selected = (0, 1, 2, 3, 7, 31, 127, 509, 1021, 2047, 4095, 8190)
    exact = [product_log_weight((residuals+step*slopes) % order, order, t)
             for step in selected]
    cert = harmonic_certificate(m, t, harmonics)
    return {
        "field_bits": bits, "cyclic_order": order, "length": m, "evaluations": n,
        "support_encoding": "0..5999", "evaluation_encoding": "6000..6419",
        "center_seed": 20261020, "center_rng": "Python random.Random.randrange",
        "center_sha256": hashlib.sha256(json.dumps(centers.tolist()).encode()).hexdigest(),
        "slope_sha256": hashlib.sha256(json.dumps(slopes.tolist()).encode()).hexdigest(),
        "base_assignment": "all zero", "direction": "first coordinate vector",
        "harmonics": harmonics, "all_line_values_computed": len(values),
        "direct_check_steps": list(selected), "direct_log_weights": exact,
        "harmonic_log_weights": [float(values[step]) for step in selected],
        "maximum_checked_log_error":
            max(abs(float(values[step])-reference) for step, reference in zip(selected, exact)),
        "certificate": cert, "classical_sampler_executed": False,
        "paper_optimization_seed_reproduced": False,
        "scope": "native conditional-density computation; no mixing or optimizer result",
    }


def native_product_target_campaign():
    """Matched classical product-target campaign on the frozen native m=6000, n=420 instance."""
    started = time.perf_counter()
    bits, m, n, order = 13, 6000, 420, 8191
    t, cap, harmonics = Q(1, 20), 209, 9
    supports, evaluations = mpi.points(bits, m, n)
    _, logs, _ = mpi.presentation(bits)
    B = np.array(logs, dtype=np.int64)[
        np.bitwise_xor(np.array(supports)[:, None], np.array(evaluations)[None, :])]
    center_seed = 20261020
    center_rng = random.Random(center_seed)
    centers = np.array([center_rng.randrange(order) for _ in range(m)], dtype=np.int64)
    center_sha256 = hashlib.sha256(json.dumps(centers.tolist()).encode()).hexdigest()

    # Charged systematic basis inversions for I0 = 0..419 and I1 = 100..519
    inv_I0 = np.array(nmod_mat(B[:n].tolist(), order).inv().tolist(), dtype=np.int64)
    G_I0 = (B @ inv_I0) % order
    inv_I1 = np.array(nmod_mat(B[100:100+n].tolist(), order).inv().tolist(), dtype=np.int64)
    G_I1 = (B @ inv_I1) % order
    x_pin_I0 = (inv_I0 @ centers[:n]) % order
    res_pin_I0 = (B @ x_pin_I0 - centers) % order
    pin_cosine = float(np.cos(2*np.pi*res_pin_I0/order).mean())
    pin_log_weight = product_log_weight(res_pin_I0, order, t)

    def score_and_verify(x_vec):
        res_explicit = (B @ x_vec - centers) % order
        fast_vals = np.array(
            mpi.fast_public_matvec(bits, supports, evaluations, x_vec.tolist()),
            dtype=np.int64,
        )
        res_fast = (fast_vals - centers) % order
        if not np.array_equal(res_explicit, res_fast):
            raise ArithmeticError("fast public matvec disagreed with explicit matrix product")
        return (
            float(np.cos(2*np.pi*res_explicit/order).mean()),
            product_log_weight(res_explicit, order, t),
        )

    # 1. Cold original-coordinate heat bath starting from x_pin_I0 (60 updates)
    rng_orig = random.Random(2026102011)
    x_orig = x_pin_I0.copy()
    res_orig = res_pin_I0.copy()
    best_x_orig = x_orig.copy()
    best_cos_orig = pin_cosine
    orig_nontrivial = 0
    orig_first_exit = None
    for step_idx in range(1, 61):
        col_j = rng_orig.randrange(n)
        slopes = B[:, col_j]
        line_logs = harmonic_line_log_weights(res_orig, slopes, order, t, harmonics)
        probs = categorical_line_probabilities(line_logs, beta=1.0)
        shift = sample_categorical_step(probs, rng_orig)
        if shift != 0:
            orig_nontrivial += 1
            if orig_first_exit is None:
                orig_first_exit = step_idx
            x_orig[col_j] = (x_orig[col_j] + shift) % order
            res_orig = (res_orig + shift*slopes) % order
            cos_now = float(np.cos(2*np.pi*res_orig/order).mean())
            if cos_now > best_cos_orig:
                best_cos_orig = cos_now
                best_x_orig = x_orig.copy()
    ver_cos_orig, ver_lw_orig = score_and_verify(best_x_orig)

    # 2. Systematic-basis I0 categorical heat bath (80 updates)
    rng_sys = random.Random(2026102012)
    x_sys = x_pin_I0.copy()
    res_sys = res_pin_I0.copy()
    best_x_sys = x_sys.copy()
    best_cos_sys = pin_cosine
    sys_nontrivial = 0
    sys_first_exit = None
    for step_idx in range(1, 81):
        col_j = rng_sys.randrange(n)
        slopes = G_I0[:, col_j]
        line_logs = harmonic_line_log_weights(res_sys, slopes, order, t, harmonics)
        probs = categorical_line_probabilities(line_logs, beta=1.0)
        shift = sample_categorical_step(probs, rng_sys)
        if shift != 0:
            sys_nontrivial += 1
            if sys_first_exit is None:
                sys_first_exit = step_idx
            x_sys = (x_sys + shift*inv_I0[:, col_j]) % order
            res_sys = (res_sys + shift*slopes) % order
            cos_now = float(np.cos(2*np.pi*res_sys/order).mean())
            if cos_now > best_cos_sys:
                best_cos_sys = cos_now
                best_x_sys = x_sys.copy()
    ver_cos_sys, ver_lw_sys = score_and_verify(best_x_sys)

    # 3. Two-replica parallel tempering in systematic basis I0 (beta_0=0.20, beta_1=1.0)
    rng_pt = random.Random(2026102013)
    betas = (0.20, 1.0)
    x_rep = [x_pin_I0.copy(), x_pin_I0.copy()]
    res_rep = [res_pin_I0.copy(), res_pin_I0.copy()]
    best_x_pt = x_pin_I0.copy()
    best_cos_pt = pin_cosine
    pt_nontrivial = [0, 0]
    proposed_swaps = 0
    accepted_swaps = 0
    for block in range(6):
        for _ in range(10):
            for r_idx, beta in enumerate(betas):
                col_j = rng_pt.randrange(n)
                slopes = G_I0[:, col_j]
                line_logs = harmonic_line_log_weights(res_rep[r_idx], slopes, order, t, harmonics)
                probs = categorical_line_probabilities(line_logs, beta=beta)
                shift = sample_categorical_step(probs, rng_pt)
                if shift != 0:
                    pt_nontrivial[r_idx] += 1
                    x_rep[r_idx] = (x_rep[r_idx] + shift*inv_I0[:, col_j]) % order
                    res_rep[r_idx] = (res_rep[r_idx] + shift*slopes) % order
                    cos_now = float(np.cos(2*np.pi*res_rep[r_idx]/order).mean())
                    if cos_now > best_cos_pt:
                        best_cos_pt = cos_now
                        best_x_pt = x_rep[r_idx].copy()
        proposed_swaps += 1
        lw0 = product_log_weight(res_rep[0], order, t)
        lw1 = product_log_weight(res_rep[1], order, t)
        log_accept = (betas[1] - betas[0]) * (lw0 - lw1)
        if log_accept >= 0 or rng_pt.random() < exp(max(-700.0, log_accept)):
            accepted_swaps += 1
            x_rep[0], x_rep[1] = x_rep[1], x_rep[0]
            res_rep[0], res_rep[1] = res_rep[1], res_rep[0]
    ver_cos_pt, ver_lw_pt = score_and_verify(best_x_pt)

    # 4. Alternating systematic-basis (I0 -> I1) product-density mode search (120 cols each)
    x_alt = x_pin_I0.copy()
    res_alt = res_pin_I0.copy()
    best_lw_alt = pin_log_weight
    best_cos_alt = pin_cosine
    alt_moves = 0
    for basis_inv, basis_G in ((inv_I0, G_I0), (inv_I1, G_I1)):
        for col_j in range(120):
            slopes = basis_G[:, col_j]
            line_logs = harmonic_line_log_weights(res_alt, slopes, order, t, harmonics)
            shift = int(np.argmax(line_logs))
            if shift != 0:
                cand_res = (res_alt + shift*slopes) % order
                cand_lw = product_log_weight(cand_res, order, t)
                if cand_lw > best_lw_alt + 1e-12:
                    alt_moves += 1
                    best_lw_alt = cand_lw
                    res_alt = cand_res
                    x_alt = (x_alt + shift*basis_inv[:, col_j]) % order
                    best_cos_alt = float(np.cos(2*np.pi*res_alt/order).mean())
    ver_cos_alt, ver_lw_alt = score_and_verify(x_alt)

    chains = [
        {
            "name": "cold_original_coordinate_heatbath_from_pinned_I0",
            "seed": 2026102011,
            "beta": 1.0,
            "original_coordinate_updates": 60,
            "systematic_basis_updates": 0,
            "basis_switches": 0,
            "proposed_replica_exchanges": 0,
            "accepted_replica_exchanges": 0,
            "nontrivial_moves_accepted": orig_nontrivial,
            "first_exit_step": orig_first_exit,
            "initial_mean_cosine": pin_cosine,
            "best_mean_cosine": ver_cos_orig,
            "best_product_log_weight": ver_lw_orig,
            "best_assignment": best_x_orig.tolist(),
            "threshold_0_3_reached": ver_cos_orig >= 0.3,
        },
        {
            "name": "systematic_basis_heatbath_I0",
            "seed": 2026102012,
            "beta": 1.0,
            "original_coordinate_updates": 0,
            "systematic_basis_updates": 80,
            "basis_switches": 0,
            "proposed_replica_exchanges": 0,
            "accepted_replica_exchanges": 0,
            "nontrivial_moves_accepted": sys_nontrivial,
            "first_exit_step": sys_first_exit,
            "initial_mean_cosine": pin_cosine,
            "best_mean_cosine": ver_cos_sys,
            "best_product_log_weight": ver_lw_sys,
            "best_assignment": best_x_sys.tolist(),
            "threshold_0_3_reached": ver_cos_sys >= 0.3,
        },
        {
            "name": "two_replica_tempered_systematic_chain_I0",
            "seed": 2026102013,
            "betas": list(betas),
            "original_coordinate_updates": 0,
            "systematic_basis_updates": 120,
            "basis_switches": 0,
            "proposed_replica_exchanges": proposed_swaps,
            "accepted_replica_exchanges": accepted_swaps,
            "nontrivial_moves_accepted_by_replica": pt_nontrivial,
            "initial_mean_cosine": pin_cosine,
            "best_mean_cosine": ver_cos_pt,
            "best_product_log_weight": ver_lw_pt,
            "best_assignment": best_x_pt.tolist(),
            "threshold_0_3_reached": ver_cos_pt >= 0.3,
        },
        {
            "name": "alternating_systematic_basis_product_mode_search_I0_I1",
            "seed": None,
            "original_coordinate_updates": 0,
            "systematic_basis_updates": 240,
            "basis_switches": 2,
            "proposed_replica_exchanges": 0,
            "accepted_replica_exchanges": 0,
            "nontrivial_moves_accepted": alt_moves,
            "initial_mean_cosine": pin_cosine,
            "best_mean_cosine": ver_cos_alt,
            "best_product_log_weight": ver_lw_alt,
            "best_assignment": x_alt.tolist(),
            "threshold_0_3_reached": ver_cos_alt >= 0.3,
        },
    ]
    best_chain = max(chains, key=lambda item: item["best_mean_cosine"])
    return {
        "field_bits": bits, "cyclic_order": order, "length": m, "evaluations": n,
        "cap_each_sign": cap, "active_probability": str(t), "harmonics": harmonics,
        "center_seed": center_seed, "center_sha256": center_sha256,
        "score_threshold": "3/10",
        "preprocessing_charged": {
            "field_log_table_size": order + 1,
            "public_matrix_entries": m * n,
            "systematic_basis_inversions": 2,
            "information_sets": ["0..419", "100..519"],
            "total_harmonic_line_ffts": 60 + 80 + 120 + 240,
        },
        "pinned_I0_initial_mean_cosine": pin_cosine,
        "pinned_I0_initial_product_log_weight": pin_log_weight,
        "chains": chains,
        "best_chain_name": best_chain["name"],
        "best_mean_cosine": best_chain["best_mean_cosine"],
        "best_product_log_weight": best_chain["best_product_log_weight"],
        "any_chain_reached_0_3_threshold": any(c["threshold_0_3_reached"] for c in chains),
        "independent_fast_and_explicit_matvec_verified": True,
        "mixing_time_certified": False,
        "elapsed_seconds_diagnostic": time.perf_counter() - started,
    }


def finite_transfer_control(matrix, order, cap, t, centers):
    """Exponential identity validation only; rejects a noninjective retained box."""
    B = np.asarray(matrix)
    c = np.asarray(centers)
    if (B.ndim != 2 or B.dtype.kind not in "iu" or not min(B.shape)
            or c.shape != (B.shape[0],) or c.dtype.kind not in "iu"):
        raise ValueError("integer matrix and matching integer center vector required")
    if type(order) is not int or order <= 3:
        raise ValueError("cyclic order greater than three required")
    if type(cap) is not int or cap < 0:
        raise ValueError("nonnegative integer cap required")
    if not isinstance(t, Q) or not 0 < t < Q(1, 3):
        raise ValueError("rational t in (0,1/3) required")
    m, n = B.shape
    if m > 5 or order**n * 3**m > 5_000_000:
        raise ValueError("finite enumeration budget exceeded; not a native sampler")
    B = (B % order).astype(np.int64)
    c = (c % order).astype(np.int64)
    words = np.array(list(product((-1, 0, 1), repeat=m)), dtype=np.int64)
    inside = ((words == 1).sum(axis=1) <= cap) & ((words == -1).sum(axis=1) <= cap)
    images = words[inside] @ B % order
    if len({tuple(s) for s in images}) != int(inside.sum()):
        raise ValueError("retained box is not syndrome-injective")
    assignments = np.array(list(product(range(order), repeat=n)), dtype=np.int64)
    residuals = (assignments @ B.T - c) % order
    active = np.count_nonzero(words, axis=1)
    weights = np.array([sqrt(float((1-t)**(m-int(k))*(t/2)**int(k)))
                        for k in active])
    phases = np.exp(2j*np.pi*(residuals @ words.T % order)/order)
    good = phases[:, inside] @ weights[inside]
    bad = phases[:, ~inside] @ weights[~inside]
    full = np.prod(sqrt(float(1-t)) + sqrt(float(2*t))*np.cos(
        2*np.pi*residuals/order), axis=1)
    z = mpi.multinomial_box(m, cap, cap, t)
    q_prob = abs(good)**2
    q_prob /= q_prob.sum()
    p_prob = full**2
    p_prob /= p_prob.sum()
    energy = float(np.mean(abs(bad)**2))
    return {
        "order": order, "length": m, "dimension": n,
        "assignments_enumerated": len(assignments),
        "patterns_enumerated": len(words),
        "retained_patterns": int(inside.sum()), "retained_mass": str(z),
        "retained_norm": float(np.mean(abs(good)**2)),
        "discarded_target_energy": energy,
        "product_amplitude_identity_max_error": float(np.max(abs(good+bad-full))),
        "target_tv": float(np.sum(abs(q_prob-p_prob))/2),
        "pointwise_tv_bound": min(1.0, sqrt(energy/float(z))),
        "scope": "finite numerical identity control, not an optimization experiment",
    }


def center_average_control():
    """Exhaust all centers of a small abstract map to test character averaging."""
    order, matrix, m, cap, t = 5, [[1], [2], [3]], 3, 0, Q(1, 10)
    controls = [finite_transfer_control(matrix, order, cap, t, center)
                for center in product(range(order), repeat=m)]
    z = mpi.multinomial_box(m, cap, cap, t)
    return {
        "centers_enumerated": len(controls),
        "discarded_source_mass": str(1-z),
        "average_discarded_target_energy":
            sum(c["discarded_target_energy"] for c in controls)/len(controls),
        "average_target_tv": sum(c["target_tv"] for c in controls)/len(controls),
        "average_tv_bound": sqrt(float((1-z)/z)),
        "maximum_pointwise_bound_violation":
            max(c["target_tv"]-c["pointwise_tv_bound"] for c in controls),
        "scope": "abstract finite identity control; not an MPI instance or candidate",
    }


def worst_case_amplification_control():
    """A generic colliding map invalidates a source-tail-only worst-case claim."""
    order, m, t = 7, 400, Q(1, 40000)
    residual = np.arange(order, dtype=np.int64)
    logs = np.array([product_log_weight(np.full(m, r, dtype=np.int64), order, t)
                     for r in residual])
    probabilities = np.exp(logs-logs.max())
    probabilities /= probabilities.sum()
    shifted_logs = np.array([
        product_log_weight(np.full(m, (r-2) % order, dtype=np.int64), order, t)
        for r in residual])
    shifted = np.exp(shifted_logs-shifted_logs.max())
    shifted /= shifted.sum()
    z = (1-t)**m
    tv = float(np.sum(abs(probabilities-1/order))/2)
    return {
        "order": order, "length": m, "dimension": 1, "cap": 0,
        "matrix": "all entries one", "centers": "all zero",
        "active_probability": str(t),
        "discarded_mass_upper": str(enclose(1-z, upper=True)),
        "incorrect_worst_case_bound": sqrt(float((1-z)/z)),
        "actual_target_tv": tv,
        "gauge_shift": 2,
        "gauge_shifted_tv": float(np.sum(abs(shifted-1/order))/2),
        "gauge_permutation_max_error": float(np.max(abs(shifted-np.roll(probabilities, 2)))),
        "is_log_cauchy_mpi_instance": False,
        "scope": "counterexample to a general transfer claim, not an MPI no-go theorem",
    }


def mpi_control(bits):
    supports, evaluations = mpi.points(bits, 4, 4)
    _, logs, _ = mpi.presentation(bits)
    matrix = [[logs[a ^ z] for z in evaluations] for a in supports]
    result = finite_transfer_control(matrix, (1 << bits)-1, 1, Q(1, 20), [0, 2, 4, 6])
    result["bits"] = bits
    result["log_cauchy_instance"] = True
    return result


def report():
    return {
        "schema": "balanced_mpi_product_target_v2",
        "status": "conditional_classical_sampling_reduction; independent_review_pending",
        "producer_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "balanced_source_sha256": hashlib.sha256(Path(mpi.__file__).read_bytes()).hexdigest(),
        "references": ["https://arxiv.org/abs/2610.06753",
                       "https://arxiv.org/abs/2607.28120"],
        "native_attack_target": transfer_certificate(
            6000, 420, 209, Q(1, 20), center_model=CENTER_MODEL, sampler_tv=Q(1, 1000)),
        "original_pilot_comparator": transfer_certificate(
            6000, 420, 209, Q(13, 200), center_model=CENTER_MODEL),
        "native_line_control": native_line_control(),
        "small_mcmc_stationary_and_detailed_balance_control":
            small_mcmc_stationary_and_detailed_balance_control(),
        "native_product_target_campaign": native_product_target_campaign(),
        "center_average_control": center_average_control(),
        "prime_control": mpi_control(3),
        "composite_control": mpi_control(4),
        "worst_case_countercontrol": worst_case_amplification_control(),
        "classical_sampler_executed": False,
        "native_optimizer_executed": False,
        "bounded_native_mcmc_and_mode_campaign_executed": True,
        "dequantization_claim_admitted": False,
        "blocked": ["mixing or a different efficient classical sampler",
                    "matched native experiments", "worst-case-center extension",
                    "independent proof review"],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=REPORT)
    args = parser.parse_args()
    result = report()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2)+"\n")
    native = result["native_attack_target"]
    campaign = result["native_product_target_campaign"]
    print(json.dumps({
        "output": str(args.output),
        "center_averaged_tv_upper": float(Q(native["center_averaged_target_tv_upper"])),
        "conditional_joint_success_lower": float(Q(native["conditional_joint_success_lower"])),
        "campaign_best_chain": campaign["best_chain_name"],
        "campaign_best_mean_cosine": campaign["best_mean_cosine"],
        "sampler_premise_proved": False, "dequantization_claim_admitted": False,
    }))


if __name__ == "__main__":
    main()

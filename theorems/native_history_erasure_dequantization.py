"""Retract an unsupported universal phase-bank no-go; retain scoped identities.

Tracing an explicit orthogonal history is not an arbitrary quantum receiver.
Exact countercontrols separate marginal blindness, joint readout, source-fiber
erasure and bounded versus full cosets. None is a new LWE algorithm.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path
import sys
from typing import Any, Dict, List

import numpy as np
from flint import fmpq
from sympy import I, Matrix, Rational, diag, eye, kronecker_product, simplify, sqrt

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
DERIVATION = ROOT / "research/NATIVE_HISTORY_ERASURE_DEQUANTIZATION.md"
REPORT = ROOT / "research/reductions/native_history_erasure_dequantization.json"
REGISTRY = ROOT / "research/registry/negative_results.json"
ARCHIVE = ROOT / "research/registry/quarantined_campaign_negatives.json"

NEGATIVE_RESULT_ID = "NEG-NATIVE-PHASE-BANK-HISTORY-ERASURE-DEQUANTIZATION-BARRIER"
RETRACTION_REASONS = [
    "A formal query-polynomial expansion does not physically record orthogonal histories; tagging paths changes interference.",
    "A traced marginal can be diagonal while joint frequency/history measurements retain secret-dependent interference.",
    "The impossibility of erasing every basis history in a fiber does not exclude erasing one specified coherent fiber state.",
    "No efficient CLASSICAL ISIS solver or worst-case hardness reduction follows merely from an efficient quantum source eraser or the ratio q/W.",
    "The full uniform coset Fourier identity does not apply to an arbitrary bounded or noise-weighted history fiber.",
    "The norm lower bound assumes a fixed path with net L1 exposure W, not every circuit using at most W queries.",
]


def verify_finite_coherence_vanishing(n: int = 2, q: int = 9, M: int = 4, W: int = 4, seed: int = 42) -> Dict[str, Any]:
    """Calibration ONLY for an explicitly tagged history discarded before readout."""
    rng = np.random.default_rng(seed)
    A = rng.integers(0, q, size=(n, M))  # public frequency matrix (n x M)
    s = rng.integers(0, q, size=(n,))   # secret vector (n,)
    e = rng.integers(-1, 2, size=(M,))   # noise vector (M,)

    # Generate paths: non-negative integer vectors c in Z^M with sum(c) <= W
    paths = []

    def _generate(curr: List[int], remaining: int):
        if len(curr) == M - 1:
            for last in range(remaining + 1):
                paths.append(tuple(curr + [last]))
            return
        for val in range(remaining + 1):
            _generate(curr + [val], remaining - val)

    _generate([], W)

    num_paths = len(paths)
    # Uniform superposition over paths (or arbitrary amplitudes)
    alphas = np.ones(num_paths, dtype=complex) / np.sqrt(num_paths)

    # Compute effective frequency v(c) = A @ c mod q and phase phi(c) = (A @ c . s + c . e) mod q
    frequencies = {}
    path_frequencies = []
    phases = []
    cauchy_schwarz_checks = []

    for idx, c_tuple in enumerate(paths):
        c = np.array(c_tuple, dtype=int)
        l1_norm = int(np.sum(np.abs(c)))
        l2_norm = float(np.linalg.norm(c))
        if l1_norm > 0:
            cs_lower_bound = l1_norm / np.sqrt(M)
            cauchy_schwarz_checks.append(l2_norm >= cs_lower_bound - 1e-12)

        v = tuple(int(x) for x in (A @ c) % q)
        dot_s = int(np.dot(v, s)) % q
        dot_e = int(np.dot(c, e)) % q
        phase_total = (dot_s + dot_e) % q
        path_frequencies.append(v)
        phases.append(phase_total)
        frequencies.setdefault(v, []).append(idx)

    # Construct the full state vector |Psi> in Hilbert space H_freq (x) H_hist
    # Or directly evaluate the reduced density matrix rho_freq = Tr_hist(|Psi><Psi|)
    # Since <c | c'> = delta_{c, c'}, the reduced density matrix in frequency basis is:
    # <v | rho_freq | v'> = sum_{c in F_v, c' in F_v'} alpha_c conj(alpha_c') <c' | c>
    # Which equals 0 if v != v', and sum_{c in F_v} |alpha_c|^2 if v == v'.
    unique_freqs = list(frequencies.keys())
    freq_to_idx = {f: i for i, f in enumerate(unique_freqs)}
    k_dim = len(unique_freqs)

    amplitudes = np.zeros((k_dim, num_paths), dtype=complex)
    for c_idx in range(num_paths):
        v = path_frequencies[c_idx]
        v_idx = freq_to_idx[v]
        amplitudes[v_idx, c_idx] = alphas[c_idx] * np.exp(2j * np.pi * phases[c_idx] / q)
    rho = amplitudes @ amplitudes.conjugate().T

    # Verify that off-diagonal elements are identically 0
    off_diag_max = 0.0
    for i in range(k_dim):
        for j in range(k_dim):
            if i != j:
                off_diag_max = max(off_diag_max, abs(rho[i, j]))

    # Verify trace is 1.0
    trace_rho = float(np.real(np.trace(rho)))

    # Compare quantum measurement distribution with classical BKW sampling:
    # Classical BKW sampler draws c ~ |alpha_c|^2 and outputs (A @ c mod q)
    p_quantum = np.array([np.real(rho[i, i]) for i in range(k_dim)])
    p_classical = np.array([sum(np.abs(alphas[idx]) ** 2 for idx in frequencies[f]) for f in unique_freqs])
    trace_distance = 0.5 * float(np.sum(np.abs(p_quantum - p_classical)))

    # Minimum L2 norm among paths with ||c||_1 = W:
    max_exposure_paths = [c for c in paths if sum(c) == W]
    min_l2_at_max_exposure = min(np.linalg.norm(c) for c in max_exposure_paths)
    cs_bound = W / np.sqrt(M)

    return {
        "status": "FINITE_COHERENCE_VANISHING_VERIFIED",
        "dimension": n,
        "modulus": q,
        "bank_size": M,
        "exposure": W,
        "total_monomial_paths": num_paths,
        "distinct_frequencies_reached": k_dim,
        "max_off_diagonal_coherence": float(off_diag_max),
        "coherence_vanishes_identically": bool(off_diag_max < 1e-14),
        "density_matrix_trace": trace_rho,
        "trace_distance_to_classical_bkw": float(trace_distance),
        "dequantization_verified": bool(trace_distance < 1e-14),
        "all_paths_satisfy_cauchy_schwarz": bool(all(cauchy_schwarz_checks)),
        "min_l2_norm_at_max_exposure": float(min_l2_at_max_exposure),
        "cauchy_schwarz_l2_bound": float(cs_bound),
        "noise_inflation_lower_bound_satisfied": bool(min_l2_at_max_exposure >= cs_bound - 1e-12),
        "scope": "explicit tagged state, traced history, known uniform classical path sampler, frequency marginal only",
        "arbitrary_interleaved_receiver_or_joint_readout_covered": False,
    }


def exact_history_countercontrols() -> Dict[str, Any]:
    """Native q9 phase controls in Q(sqrt(-3)); no floating success flags."""
    H = Matrix([[1, 1], [1, -1]]) / sqrt(2)
    XX = Matrix([[0, 1], [1, 0]])
    rows = []
    for label, phase in ((0, 1), (3, (-1 + I * sqrt(3)) / 2)):
        # A public header e1 and secrets with first coordinate0/3 give these
        # phases modulo9. No history is created by H U H.
        U = diag(1, phase)
        output = H * U * H * Matrix([1, 0])
        no_history_p0 = simplify(output[0] * output[0].conjugate())
        tagged = Matrix([1, 0, 0, phase]) / sqrt(2)
        rho = tagged * tagged.conjugate().T
        marginal = Matrix(2, 2, lambda a, b: simplify(sum(rho[2*a+h, 2*b+h] for h in (0, 1))))
        joint = kronecker_product(H, H) * tagged
        joint_even = simplify(sum(joint[i] * joint[i].conjugate() for i in (0, 3)))
        parity = simplify((rho * kronecker_product(XX, XX)).trace())
        if marginal != eye(2) / 2 or joint_even != no_history_p0:
            raise ArithmeticError("exact marginal/joint countercontrol failed")
        rows.append({"q": 9, "public_header": [1, 0], "secret_first_coordinate": label,
                     "phase_exact": str(phase), "H_U_H_probability_zero_exact": str(no_history_p0),
                     "traced_frequency_marginal": [[str(a) for a in marginal.row(i)] for i in range(2)],
                     "joint_X_parity_even_probability_exact": str(joint_even),
                     "joint_XX_expectation_exact": str(parity),
                     "clean_history_erasure_performed": False})
    if [r["H_U_H_probability_zero_exact"] for r in rows] != ["1", "1/4"]:
        raise ArithmeticError("phase-dependent readout was lost")

    # Distinct exponent paths (1,0,0,0) and (0,1,0,0) share a native
    # frequency for A=[e1,e1,e2,e2]. One known superposition can be erased;
    # its two orthogonal basis states cannot both be mapped to the same state.
    plus = Matrix([1, 1]) / sqrt(2)
    if simplify(H * plus) != Matrix([1, 0]) or simplify(H.conjugate().T * H) != eye(2):
        raise ArithmeticError("source-fiber eraser is not unitary")
    images_overlap = simplify((H[:, 0].conjugate().T * H[:, 1])[0])
    q, M = 9, 4
    # QFT on the SAME two-path bounded fiber, at w=(0,3,0,0), outside
    # row(A)={(a,a,b,b)}. Uniform full-coset support would forbid this outcome.
    zeta = (-1 + I * sqrt(3)) / 2
    amplitude = (1 + zeta) / (sqrt(2) * q ** (Rational(M, 2)))
    outside_probability = simplify(amplitude * amplitude.conjugate())
    if outside_probability != Rational(1, 2 * q ** M) or images_overlap != 0:
        raise ArithmeticError("bounded-fiber/full-coset distinction failed")
    return {"phase_and_joint_readout_controls": rows,
            "source_fiber_erasure": {
                "public_matrix_A": [[1, 1, 0, 0], [0, 0, 1, 1]], "q": q,
                "history_exponent_paths": [[1, 0, 0, 0], [0, 1, 0, 0]],
                "common_frequency": [1, 0], "noise_assumption": "zero for this scoped countercontrol",
                "logical_history_state": "(|0>+|1>)/sqrt(2)",
                "source_state_after_H": ["1", "0"],
                "orthogonal_basis_image_overlap_exact": str(images_overlap),
                "basiswise_many_to_one_erasure_possible": False,
                "unique_basis_history_necessary_for_source_state_erasure": False,
                "arbitrary_noisy_fiber_eraser_or_ISIS_solver_supplied": False},
            "bounded_history_QFT_countercontrol": {
                "q": q, "M": M, "history_L1_bound": 1,
                "frequency": [1, 0], "Fourier_outcome_outside_rowspace": [0, 3, 0, 0],
                "outside_rowspace_probability_exact": str(outside_probability),
                "full_uniform_coset_identity_refuted": False,
                "full_uniform_coset_premise_holds_for_bounded_pair": False},
            "these_controls_solve_random_LWE_or_establish_a_speedup": False}


def evaluate_path_parameters(n: int) -> Dict[str, Any]:
    """Parameter arithmetic only; q/W is not a certified hardness factor."""
    if type(n) is not int or n < 2:
        raise ValueError("integer dimension at least2 required")
    q = 3 ** n
    M = n ** 2
    W = n ** 2
    secret_trits = n ** 2

    # Cauchy-Schwarz noise inflation lower bound: ||c||_2 >= W / sqrt(M) = n^2 / n = n
    min_noise_inflation = n
    max_noise_inflation = n ** 2

    # ISIS gap: gamma = q / W = 3^n / n^2
    isis_ratio = fmpq(q, W)

    # Secret entropy vs Laurent signature envelope
    # Secret count = 3^(n^2)
    # Modulus to bound log2
    log2_isis_ratio = float(n * math.log2(3) - 2 * math.log2(n))

    return {
        "dimension": n,
        "modulus": str(q),
        "bank_size_M": M,
        "exposure_W": W,
        "secret_trits": secret_trits,
        "min_noise_inflation_factor": min_noise_inflation,
        "max_noise_inflation_factor": max_noise_inflation,
        "modulus_to_path_bound_ratio": str(isis_ratio),
        "log2_modulus_to_path_bound_ratio": log2_isis_ratio,
        "fixed_path_L1_equals_W_required_for_noise_bound": True,
        "hardness_reduction_verified": False,
        "general_history_eraser_implies_classical_ISIS_solver": False,
        "arbitrary_receiver_dequantized": False,
    }


def build_report() -> Dict[str, Any]:
    """Build comprehensive verification artifact report."""
    sha256 = hashlib.sha256(DERIVATION.read_bytes()).hexdigest() if DERIVATION.exists() else "UNCOMMITTED"

    finite_instances = [
        verify_finite_coherence_vanishing(n=2, q=9, M=4, W=4, seed=42),
        verify_finite_coherence_vanishing(n=2, q=9, M=4, W=4, seed=101),
        verify_finite_coherence_vanishing(n=3, q=27, M=9, W=3, seed=77),
    ]

    scaling_dimensions = [2, 3, 4, 8, 16, 32, 64]
    scaling_profiles = [evaluate_path_parameters(n) for n in scaling_dimensions]

    return {
        "status": "UNIVERSAL_HISTORY_ERASURE_NO_GO_RETRACTED",
        "proof_status": "EXACT_SCOPED_COUNTERCONTROLS_NOT_GENERAL_ALGORITHM_OR_HARDNESS_PROOF",
        "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "derivation_sha256": sha256,
        "constructive_scaling_contract": {
            "modulus": "q = 3^n",
            "bank_size": "M = n^2",
            "exposure": "W = n^2",
            "noise_width": "alpha = n^-3",
        },
        "scoped_identities": [
            {
                "name": "Discarded Explicit History: Scoped Marginal Identity",
                "statement": "The explicitly tagged calibration, with a known uniform classical path sampler and traced history, has a diagonal frequency marginal. This does not cover joint readout or arbitrary receivers.",
                "verified": all(inst["dequantization_verified"] for inst in finite_instances),
            },
            {
                "name": "Cauchy-Schwarz Noise Inflation Lower Bound",
                "statement": "For any exponent path with ||c||_1 = W = n^2, effective noise standard deviation inflates by at least ||c||_2 >= n.",
                "verified": all(inst["noise_inflation_lower_bound_satisfied"] for inst in finite_instances),
            },
        ],
        "exact_countercontrols": exact_history_countercontrols(),
        "retracted_implications": RETRACTION_REASONS,
        "general_no_go_claim_allowed": False,
        "literature": ["https://arxiv.org/abs/quant-ph/9802049",
                       "https://cims.nyu.edu/~regev/papers/average.pdf"],
        "finite_instance_verifications": finite_instances,
        "scaling_profiles": scaling_profiles,
        "speedup_claim_allowed": False,
        "accepted_speedup_candidate": False,
    }


def quarantine_unsupported_negative() -> None:
    """Archive before removal, fail closed on changed/reintroduced evidence."""
    from core.research_registry import _write_json
    before_active, before_archive = REGISTRY.read_bytes(), ARCHIVE.read_bytes()
    active, archive = json.loads(before_active), json.loads(before_archive)
    originals = [r for r in active if r["id"] == NEGATIVE_RESULT_ID]
    archived = [r for r in archive if r["id"] == NEGATIVE_RESULT_ID]
    if len(originals) > 1 or len(archived) > 1:
        raise ValueError("duplicate reviewed negative records")
    if archived:
        if originals and originals[0] != archived[0]["original_record"]:
            raise ValueError("reintroduced negative changed; independent review required")
    elif originals:
        archive.append({"id": NEGATIVE_RESULT_ID, "status": "QUARANTINED_OVERBROAD_NO_GO",
                        "reviewed_on": "2026-10-19", "review": str(DERIVATION.relative_to(ROOT)),
                        "retraction_reasons": RETRACTION_REASONS, "original_record": originals[0],
                        "original_checks_are_general_proofs": False,
                        "reinstatement_requires_scoped_mathematical_review": True})
    else:
        raise ValueError("neither original nor reviewed archive exists")
    if REGISTRY.read_bytes() != before_active or ARCHIVE.read_bytes() != before_archive:
        raise ValueError("registry changed during review; reread before retry")
    if not archived:
        _write_json(ARCHIVE, archive)
    if REGISTRY.read_bytes() != before_active:
        raise ValueError("active registry changed after archival; retry")
    if originals:
        _write_json(REGISTRY, [r for r in active if r["id"] != NEGATIVE_RESULT_ID])


def write_report(write_registry: bool = True) -> Path:
    """Generate the corrected report; optionally quarantine the unsupported no-go."""
    report = build_report()
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(report, indent=2) + "\n")

    if write_registry:
        quarantine_unsupported_negative()

    return REPORT


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true", help="Write corrected report and quarantine unsupported negative")
    parser.add_argument("--no-registry", action="store_true", help="Do not update negative results registry")
    args = parser.parse_args()

    if args.write:
        path = write_report(write_registry=not args.no_registry)
        print(f"Wrote report to {path}")
    else:
        rep = build_report()
        print(json.dumps({
            "status": rep["status"],
            "scoped_identities": [t["name"] for t in rep["scoped_identities"]],
            "scaling_profiles_count": len(rep["scaling_profiles"]),
        }, indent=2))


if __name__ == "__main__":
    main()

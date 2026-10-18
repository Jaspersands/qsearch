from __future__ import annotations

import argparse
from fractions import Fraction
import hashlib
import itertools
import json
import math
from pathlib import Path
import sys
from typing import Any

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


SCHEMA_VERSION = "2026-10-16.planted-qary-noisy-parity-check-likelihood-bridge.v2"
DEFAULT_CONTRACT_PATH = (
    ROOT
    / "research"
    / "hypotheses"
    / "planted_qary_noisy_parity_check_likelihood_bridge_contract.json"
)
DEFAULT_ARTIFACT_PATH = (
    ROOT
    / "research"
    / "reductions"
    / "planted_qary_noisy_parity_check_likelihood_bridge.json"
)
DEFAULT_DOC_PATH = (
    ROOT / "research" / "PLANTED_QARY_NOISY_PARITY_CHECK_LIKELIHOOD_BRIDGE.md"
)


def canonical_sha256(payload: dict[str, Any]) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _frac_str(val: Fraction) -> str:
    return f"{val.numerator}/{val.denominator}"


def load_contract(path: Path = DEFAULT_CONTRACT_PATH) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def hamming_weight(vec: tuple[int, ...]) -> int:
    return sum(1 for c in vec if c != 0)


def source_geometry(q: int, n: int, generator_matrix: list[list[int]], *, cap: int):
    """Bounded prime-field controls, not arithmetic over composite residue rings."""
    if type(q) is not int or q < 2 or q > 127 or any(q % p == 0 for p in range(2, math.isqrt(q) + 1)):
        raise ValueError("q must be a prime <=127; extension fields are not implemented")
    if type(n) is not int or not 1 <= n <= 10 or q ** n > cap:
        raise ValueError("UNKNOWN: explicit source enumeration cap")
    if not isinstance(generator_matrix, (list, tuple)) or not 1 <= len(generator_matrix) <= n:
        raise ValueError("generator_matrix must have 1..n independent rows")
    if any(not isinstance(row, (list, tuple)) or len(row) != n or
           any(type(c) is not int for c in row) for row in generator_matrix):
        raise ValueError("generator_matrix must be a rectangular integer matrix")
    M = np.array(generator_matrix, dtype=int) % q
    d = len(M)
    vectors = list(itertools.product(range(q), repeat=n))
    B = {tuple(((np.array(c, dtype=int) @ M) % q).tolist())
         for c in itertools.product(range(q), repeat=d)}
    if len(B) != q ** d:
        raise ValueError("generator_matrix must have full row rank d")
    dual = {u for u in vectors if np.all((M @ np.array(u, dtype=int)) % q == 0)}
    return M, vectors, B, dual


def noise_rate(numerator: int, denominator: int) -> Fraction:
    if type(numerator) is not int or type(denominator) is not int or denominator <= 0:
        raise ValueError("noise rate needs integer numerator and positive denominator")
    rate = Fraction(numerator, denominator)
    if not 0 <= rate <= 1:
        raise ValueError("noise rate must lie in [0,1]")
    return rate


def evaluate_quantum_source_control(*, q: int, n: int, generator_matrix: list[list[int]],
                                    gamma_num: int, gamma_den: int) -> dict[str, Any]:
    """Apply an actual QFT to three density operators with the SAME Z marginal.

    X translation does not damp Fourier probabilities. Z phase noise does.
    Classical sampling alone supplies neither coherent density operator.
    """
    M, vectors, B, dual = source_geometry(q, n, generator_matrix, cap=128)
    gamma = noise_rate(gamma_num, gamma_den)
    v = 1 - gamma
    size = len(vectors)
    p0, p1 = 1 - Fraction(q - 1, q) * gamma, gamma / q
    weights = [p0 ** (n - hamming_weight(e)) * p1 ** hamming_weight(e) for e in vectors]
    rho_x = np.zeros((size, size), dtype=complex)
    for e, pe in zip(vectors, weights):
        psi = np.array([1 / math.sqrt(len(B))
                        if tuple((x[j] - e[j]) % q for j in range(n)) in B else 0
                        for x in vectors])
        rho_x += float(pe) * np.outer(psi, psi.conj())
    # Averaging independent Z phases multiplies each x,x' entry by v^distance.
    # The tests replay explicit Z^e Kraus operators rather than this shortcut.
    damping = np.array([[float(v ** sum(a != b for a, b in zip(x, y)))
                         for y in vectors] for x in vectors])
    rho_xz = rho_x * damping
    rho_classical = np.diag(np.diag(rho_x))
    fourier = np.array([[np.exp(2j * np.pi * sum(a*b for a, b in zip(u, x)) / q)
                         / math.sqrt(size) for x in vectors] for u in vectors])
    target_x = [Fraction(1, len(dual)) if u in dual else Fraction(0) for u in vectors]
    target_xz = [sum((p0 ** (n - sum(a != b for a, b in zip(u, w))) *
                      p1 ** sum(a != b for a, b in zip(u, w)) for w in dual), Fraction(0))
                 / len(dual) for u in vectors]
    targets = {"coherent_random_translation": target_x,
               "coherent_translation_and_phase_noise": target_xz,
               "incoherent_classical_samples": [Fraction(1, size)] * size}
    sources = {"coherent_random_translation": rho_x,
               "coherent_translation_and_phase_noise": rho_xz,
               "incoherent_classical_samples": rho_classical}
    modes = {}
    residuals = []
    for name, rho in sources.items():
        born = np.diag(fourier @ rho @ fourier.conj().T).real
        expected = np.array([float(p) for p in targets[name]])
        residual = float(np.max(np.abs(born - expected)))
        residuals.append(residual)
        modes[name] = {"Born_probabilities": born.tolist(),
                       "target_probabilities_exact": [_frac_str(p) for p in targets[name]],
                       "max_Born_residual": residual,
                       "outside_dual_mass_exact": _frac_str(sum((p for p, u in zip(targets[name], vectors)
                                                                   if u not in dual), Fraction(0))),
                       "purity": float(np.trace(rho @ rho).real)}
    marginals_equal = all(np.allclose(np.diag(rho), np.diag(rho_x), atol=1e-13, rtol=0)
                          for rho in sources.values())
    return {"q": q, "n": n, "d": len(M), "generator_matrix": M.tolist(),
            "gamma_exact": _frac_str(gamma), "vector_order": [list(u) for u in vectors],
            "dual_vectors": [list(u) for u in sorted(dual)], "modes": modes,
            "same_computational_marginal_for_all_three_sources": marginals_equal,
            "translation_only_equals_claimed_phase_convolution": target_x == target_xz,
            "classical_samples_determine_quantum_Fourier_readout": False,
            "coherent_state_preparation_from_classical_samples_supplied": False,
            "enumerated_density_dimension": size, "scalable_state_preparation": False,
            "all_physical_laws_verified": marginals_equal and max(residuals) < 1e-12}


def evaluate_noisy_parity_check_case(
    *,
    case_id: str,
    q: int,
    n: int,
    generator_matrix: list[list[int]],
    gamma_num: int,
    gamma_den: int,
    window: list[int],
    tolerance: float = 1e-12,
) -> dict[str, Any]:
    """Exhaustively verify Theorems 1, 2, and 3 over all b in B, e in F_q^n, and u in F_q^n."""
    M, all_vectors, B_set, B_perp_set = source_geometry(q, n, generator_matrix, cap=1024)
    d, n_cols = M.shape
    gamma_frac = noise_rate(gamma_num, gamma_den)
    one_minus_gamma = Fraction(1, 1) - gamma_frac
    if any(type(w) is not int or not 0 <= w < q for w in window) or len(set(window)) != len(window):
        raise ValueError("window must contain distinct canonical field elements")
    if not math.isfinite(tolerance) or not 0 < tolerance <= 1e-10:
        raise ValueError("tolerance must be finite, positive and <=1e-10")
    R = len(window)
    window_set = set(window)
    zero_in_window = 0 in window_set

    zero_vec = tuple([0] * n)
    B_perp_nonzero = sorted(B_perp_set - {zero_vec})
    d_perp = min((hamming_weight(u) for u in B_perp_nonzero), default=None)

    # Single-coordinate depolarizing probabilities:
    # p0 = 1 - (q-1)/q * gamma, p_nonzero = gamma / q
    p0_frac = Fraction(1, 1) - Fraction(q - 1, q) * gamma_frac
    p1_frac = gamma_frac / Fraction(q, 1)

    # Exact rational probability P(e) for every e in F_q^n:
    # P(e) = p0^{n - wt_H(e)} * p1^{wt_H(e)}
    e_probs_frac = [
        (p0_frac ** (n - hamming_weight(e))) * (p1_frac ** hamming_weight(e))
        for e in all_vectors
    ]
    if sum(e_probs_frac, Fraction(0, 1)) != Fraction(1, 1):
        raise ValueError("Error distribution does not sum to 1")

    # Compute exact marginal noisy codeword distribution P_X(x) = (1/q^d) sum_{b in B} P_e(x - b)
    x_probs_frac: dict[tuple[int, ...], Fraction] = {}
    q_pow_d_frac = Fraction(q ** d, 1)
    for x in all_vectors:
        prob_sum = Fraction(0, 1)
        for b in B_set:
            diff_wt = sum(1 for j in range(n) if (x[j] - b[j]) % q != 0)
            prob_sum += (p0_frac ** (n - diff_wt)) * (p1_frac ** diff_wt)
        x_probs_frac[x] = prob_sum / q_pow_d_frac

    # Verify Theorem 1 & Theorem 2 & Theorem 3 across all u in F_q^n
    max_char_residual = 0.0
    off_dual_invariance_holds = True
    on_dual_weight_law_holds = True
    max_bias_observed = Fraction(0, 1)
    weight_strata_summary: dict[int, dict[str, Any]] = {}

    r_over_q = Fraction(R, q)
    ind_zero = Fraction(1, 1) if zero_in_window else Fraction(0, 1)

    for u in all_vectors:
        wt_u = hamming_weight(u)
        in_dual = u in B_perp_set

        # 1. Character expectation E_X[omega_q^{<u, X>}]
        char_val = 0.0 + 0.0j
        acc_prob_frac = Fraction(0, 1)
        for x, px_frac in x_probs_frac.items():
            dot_ux = sum(u[j] * x[j] for j in range(n)) % q
            angle = 2.0 * math.pi * dot_ux / float(q)
            char_val += float(px_frac) * complex(math.cos(angle), math.sin(angle))
            if dot_ux in window_set:
                acc_prob_frac += px_frac

        theo_char = float(one_minus_gamma ** wt_u) if in_dual else 0.0
        char_res = abs(char_val - complex(theo_char, 0.0))
        max_char_residual = max(max_char_residual, char_res)

        # 2. Window acceptance probability p_W(u | B, gamma)
        if not in_dual:
            if acc_prob_frac != r_over_q:
                off_dual_invariance_holds = False
        else:
            theo_acc = r_over_q + (one_minus_gamma ** wt_u) * (ind_zero - r_over_q)
            if acc_prob_frac != theo_acc:
                on_dual_weight_law_holds = False
            if u != zero_vec:
                weight_strata_summary[wt_u] = {
                    "hamming_weight": wt_u,
                    "character_expectation_exact": _frac_str(one_minus_gamma ** wt_u),
                    "window_acceptance_prob_exact": _frac_str(acc_prob_frac),
                    "window_acceptance_prob_float": float(acc_prob_frac),
                    "distinguishing_bias_exact": _frac_str(abs(acc_prob_frac - r_over_q)),
                    "distinguishing_bias_float": float(abs(acc_prob_frac - r_over_q)),
                }

        if u != zero_vec:
            bias_u = abs(acc_prob_frac - r_over_q)
            if bias_u > max_bias_observed:
                max_bias_observed = bias_u

    expected_max_bias = ((one_minus_gamma ** d_perp) * abs(ind_zero - r_over_q)
                         if d_perp is not None else Fraction(0))
    theorem1_verified = max_char_residual <= tolerance
    theorem2_verified = off_dual_invariance_holds and on_dual_weight_law_holds
    theorem3_verified = (max_bias_observed == expected_max_bias)

    return {
        "case_id": case_id,
        "q": q,
        "n": n,
        "d": d,
        "generator_matrix": M.tolist(),
        "R": R,
        "window": list(window),
        "zero_in_window": zero_in_window,
        "gamma_exact": _frac_str(gamma_frac),
        "gamma_float": float(gamma_frac),
        "one_minus_gamma_exact": _frac_str(one_minus_gamma),
        "dual_minimum_distance_d_perp": d_perp,
        "nonzero_dual_exists": d_perp is not None,
        "off_dual_acceptance_prob_exact": _frac_str(r_over_q),
        "max_nonzero_probe_bias_exact": _frac_str(max_bias_observed),
        "max_nonzero_probe_bias_float": float(max_bias_observed),
        "expected_max_bias_exact": _frac_str(expected_max_bias),
        "max_character_residual": max_char_residual,
        "off_dual_invariance_holds": off_dual_invariance_holds,
        "on_dual_weight_law_holds": on_dual_weight_law_holds,
        "dual_weight_strata": [
            weight_strata_summary[w] for w in sorted(weight_strata_summary.keys())
        ],
        "theorem1_verified": theorem1_verified,
        "theorem2_verified": theorem2_verified,
        "theorem3_verified": theorem3_verified,
        "all_theorems_verified": (
            theorem1_verified and theorem2_verified and theorem3_verified
        ),
    }


def build_planted_qary_noisy_parity_check_likelihood_bridge(
    contract_path: Path = DEFAULT_CONTRACT_PATH,
) -> dict[str, Any]:
    contract = load_contract(contract_path)

    case_specs = [
        {
            "case_id": "q3_n3_d2_gamma_1_over_4_zerofree_R2",
            "q": 3,
            "n": 3,
            "generator_matrix": [[1, 0, 1], [0, 1, 1]],
            "gamma_num": 1,
            "gamma_den": 4,
            "window": [1, 2],
        },
        {
            "case_id": "q3_n3_d2_gamma_1_over_2_with_zero_R2",
            "q": 3,
            "n": 3,
            "generator_matrix": [[1, 0, 1], [0, 1, 1]],
            "gamma_num": 1,
            "gamma_den": 2,
            "window": [0, 1],
        },
        {
            "case_id": "q3_n4_d2_mixed_weights_gamma_1_over_3_zerofree_R2",
            "q": 3,
            "n": 4,
            "generator_matrix": [[1, 0, 1, 0], [0, 1, 1, 1]],
            "gamma_num": 1,
            "gamma_den": 3,
            "window": [1, 2],
        },
        {
            "case_id": "q3_n4_d2_dperp3_gamma_1_over_3_zerofree_R2",
            "q": 3,
            "n": 4,
            "generator_matrix": [[1, 0, 2, 1], [0, 1, 1, 2]],
            "gamma_num": 1,
            "gamma_den": 3,
            "window": [1, 2],
        },
        {
            "case_id": "q5_n3_d2_gamma_1_over_5_zerofree_R2",
            "q": 5,
            "n": 3,
            "generator_matrix": [[1, 0, 2], [0, 1, 3]],
            "gamma_num": 1,
            "gamma_den": 5,
            "window": [1, 4],
        },
    ]

    cases = [evaluate_noisy_parity_check_case(**spec) for spec in case_specs]
    quantum_controls = [evaluate_quantum_source_control(q=q, n=n, generator_matrix=M,
                                                        gamma_num=gn, gamma_den=gd)
                        for q, n, M in ((3, 2, [[1, 0]]), (2, 3, [[1, 0, 1], [0, 1, 1]]),
                                        (5, 2, [[1, 2]]))
                        for gn, gd in ((0, 1), (1, 2), (1, 1))]
    all_verified = (all(c["all_theorems_verified"] for c in cases) and
                    all(c["all_physical_laws_verified"] for c in quantum_controls))

    summary = {
        "case_count": len(cases),
        "all_cases_verified": all_verified,
        "quantum_source_control_count": len(quantum_controls),
        "translation_noise_convolution_claim_retracted": True,
        "max_character_residual": max(c["max_character_residual"] for c in cases),
        "scientific_verdict": (
            "Exhaustive summation over F_q^n confirms that under i.i.d. q-ary depolarizing noise of rate gamma, "
            "every off-dual probe u not in B^perp retains the exact unperturbed acceptance probability R/q "
            "independent of gamma and wt_H(u), whereas every dual parity check u in B^perp has character "
            "expectation (1 - gamma)^{wt_H(u)} and window acceptance probability R/q + (1 - gamma)^{wt_H(u)}"
            "(1_{0 in W} - R/q), with maximum non-zero distinguishing bias governed by the dual minimum "
            "distance d^perp(B). These are classical sample character laws. Actual QFT density controls "
            "separately verify that coherent random translations preserve the uniform dual distribution, "
            "phase noise convolves it, and incoherent classical samples give uniform Fourier outcomes. "
            "All three quantum sources can have identical computational marginals; no coherent preparation "
            "is supplied by a classical sample source. The former translation-QFT convolution claim is retracted."
        ),
    }

    payload_without_digest = {
        "schema_version": SCHEMA_VERSION,
        "contract_id": contract["contract_id"],
        "title": contract["title"],
        "status": (
            "VERIFIED_EXACT_NOISY_PARITY_CHECK_WEIGHT_POWER_LAWS"
            if all_verified
            else "FAILED"
        ),
        "contract_path": str(contract_path.relative_to(ROOT)),
        "doc_path": str(DEFAULT_DOC_PATH.relative_to(ROOT)),
        "guardrails": contract["guardrails"],
        "theorems": contract["theorems"],
        "summary": summary,
        "cases": cases,
        "quantum_source_controls": quantum_controls,
    }
    digest = canonical_sha256(payload_without_digest)
    return {
        **payload_without_digest,
        "certificate_sha256": digest,
    }


def write_planted_qary_noisy_parity_check_likelihood_bridge(
    output_path: Path = DEFAULT_ARTIFACT_PATH,
    contract_path: Path = DEFAULT_CONTRACT_PATH,
) -> dict[str, Any]:
    payload = build_planted_qary_noisy_parity_check_likelihood_bridge(
        contract_path=contract_path
    )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return payload


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Build or write the planted q-ary noisy parity-check likelihood bridge."
    )
    parser.add_argument("--write", action="store_true", help="Write artifact JSON to disk.")
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_ARTIFACT_PATH,
        help="Output artifact path.",
    )
    args = parser.parse_args()

    if args.write:
        payload = write_planted_qary_noisy_parity_check_likelihood_bridge(
            output_path=args.output
        )
    else:
        payload = build_planted_qary_noisy_parity_check_likelihood_bridge()

    print(
        json.dumps(
            {
                "status": payload["status"],
                "case_count": payload["summary"]["case_count"],
                "all_cases_verified": payload["summary"]["all_cases_verified"],
                "certificate_sha256": payload["certificate_sha256"],
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0 if payload["summary"]["all_cases_verified"] else 1


if __name__ == "__main__":
    raise SystemExit(main())

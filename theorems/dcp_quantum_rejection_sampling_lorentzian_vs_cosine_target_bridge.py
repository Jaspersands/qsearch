r"""DCP single-shot quantum rejection sampling box-to-sine vs. Lorentzian window reshaping bridge.

Establishes the exact maximum acceptance probability P_accept*(box -> f) of transforming
a uniform box-window superposition |psi_box> = P^{-1/2} sum_{x=0}^{P-1} |x> into a target
low-leakage window state |psi_f> = sum_{x=0}^{P-1} psi_f(x) |x> via a single diagonal
ancilla-filtering POVM {M_acc, M_rej}:

1. Exact Sup-Norm / L2-Norm Acceptance Probability Theorem:
   Any trace-non-increasing diagonal measurement operator M_acc = diag(m_0, ..., m_{P-1})
   satisfying M_acc |psi_box> = sqrt(p_acc) |psi_f> and M_acc^dagger M_acc <= I_P must
   satisfy |m_x|^2 = p_acc * P * |psi_f(x)|^2 <= 1 for all x in {0, ..., P - 1}.
   Therefore, the exact maximum physical acceptance probability is:
       P_accept*(box -> f) = 1 / ( P * max_{0 <= x < P} |psi_f(x)|^2 ) = ||psi_f||_2^2 / ( P * ||psi_f||_infty^2 ).

2. Exact > 50% Acceptance Law for the Optimal Dirichlet-Sine Window:
   For the Dirichlet-Laplacian optimal discrete sine window (Subsystem 89):
       psi_sin*(x) = sqrt(2 / (P + 1)) * sin( pi * (x + 1) / (P + 1) ),
   the peak squared amplitude satisfies max_x |psi_sin*(x)|^2 <= 2 / (P + 1) (with exact
   equality when P is odd, and (2 / (P + 1)) * cos^2(pi / (2*(P + 1))) when P is even).
   Consequently, for EVERY finite window size P >= 1:
       P_accept*(box -> sin*) >= (P + 1) / (2 * P) > 1 / 2,
   with exact closed forms:
   - Odd P:  P_accept*(box -> sin*) = (P + 1) / (2 * P),
   - Even P: P_accept*(box -> sin*) = (P + 1) / ( 2 * P * cos^2(pi / (2 * (P + 1))) ),
   converging monotonically to 1/2 = 50% as P -> infty!

3. Comparison Against Peaked Lorentzian / Narrow Gaussian Targets:
   For a peaked discrete Lorentzian window psi_lor(x; w) propto 1 / (1 + ((x - mu) / w)^2)
   with narrow width w = alpha * P (alpha < 0.25), the peak-to-average ratio P * ||psi_lor||_infty^2
   exceeds 2, yielding strictly lower acceptance P_accept*(box -> lor) < 1 / 2 and strictly
   lower unit-shift overlap gamma(1) than the optimal sine window!
"""

from __future__ import annotations

import hashlib
import json
import math
from typing import Any, Dict, List


THEOREM_ID = "dcp_quantum_rejection_sampling_lorentzian_vs_cosine_target_bridge"
SCHEMA_VERSION = "dcp-quantum-rejection-sampling-lorentzian-vs-cosine-target-bridge-v1"


def _normalize(vec: List[float]) -> List[float]:
    nrm = math.sqrt(sum(v * v for v in vec))
    return [v / nrm for v in vec]


def evaluate_quantum_rejection_sampling_box_to_target(
    p_len: int,
    lorentzian_width_ratio: float = 0.20,
) -> Dict[str, Any]:
    """Evaluate exact quantum rejection sampling acceptance probability and post-selected fidelity for sine vs Lorentzian targets."""
    if type(p_len) is not int or p_len < 3:
        raise ValueError("p_len must be an integer >= 3")

    psi_sin = _normalize([
        math.sin(math.pi * float(x + 1) / float(p_len + 1))
        for x in range(p_len)
    ])
    center = 0.5 * float(p_len - 1)
    w_lor = lorentzian_width_ratio * float(p_len)
    psi_lor = _normalize([
        1.0 / (1.0 + (((float(x) - center) / w_lor) ** 2))
        for x in range(p_len)
    ])

    max_sq_sin = max(v * v for v in psi_sin)
    max_sq_lor = max(v * v for v in psi_lor)

    p_acc_sin_exp = 1.0 / (float(p_len) * max_sq_sin)
    p_acc_lor_exp = 1.0 / (float(p_len) * max_sq_lor)

    if (p_len % 2) == 1:
        p_acc_sin_cf = float(p_len + 1) / (2.0 * float(p_len))
    else:
        p_acc_sin_cf = float(p_len + 1) / (2.0 * float(p_len) * (math.cos(math.pi / (2.0 * float(p_len + 1))) ** 2))

    # Construct explicit ancilla rotation angles theta_x = arccos(m_x) where m_x = sqrt(p_acc * P) * psi_sin(x) in [0, 1]
    m_diag_sin = [math.sqrt(p_acc_sin_exp * float(p_len)) * v for v in psi_sin]
    max_m_sin = max(m_diag_sin)
    # Apply M_acc to |psi_box> = [1/sqrt(P), ..., 1/sqrt(P)]:
    unnorm_post = [m_diag_sin[x] / math.sqrt(float(p_len)) for x in range(p_len)]
    norm_sq_post = sum(v * v for v in unnorm_post)
    post_state = [v / math.sqrt(norm_sq_post) for v in unnorm_post]
    fidelity_post = sum(a * b for a, b in zip(post_state, psi_sin)) ** 2

    gamma1_sin = sum(psi_sin[x] * psi_sin[x + 1] for x in range(p_len - 1))
    gamma1_lor = sum(psi_lor[x] * psi_lor[x + 1] for x in range(p_len - 1))

    return {
        "P_window_size": p_len,
        "p_accept_sine_explicit": p_acc_sin_exp,
        "p_accept_sine_closed_form": p_acc_sin_cf,
        "p_accept_sine_lower_bound": float(p_len + 1) / (2.0 * float(p_len)),
        "p_accept_lorentzian": p_acc_lor_exp,
        "max_povm_singular_value_sine": max_m_sin,
        "post_selected_state_fidelity_sine": fidelity_post,
        "gamma1_sine": gamma1_sin,
        "gamma1_lorentzian": gamma1_lor,
        "exact_laws_verified": (
            abs(p_acc_sin_exp - p_acc_sin_cf) < 1e-12
            and abs(norm_sq_post - p_acc_sin_exp) < 1e-12
            and abs(max_m_sin - 1.0) < 1e-12
            and abs(fidelity_post - 1.0) < 1e-12
            and p_acc_sin_exp >= float(p_len + 1) / (2.0 * float(p_len)) - 1e-12
            and p_acc_sin_exp > 0.5
            and p_acc_sin_exp > p_acc_lor_exp
            and gamma1_sin > gamma1_lor
        ),
    }


def generate_dcp_quantum_rejection_sampling_lorentzian_vs_cosine_target_certificate() -> Dict[str, Any]:
    """Generate the complete certificate for the quantum rejection sampling box-to-sine window bridge."""
    sweep = [
        evaluate_quantum_rejection_sampling_box_to_target(p_len=p_val, lorentzian_width_ratio=0.20)
        for p_val in (7, 8, 15, 16, 31, 32)
    ]

    all_passed = all(r["exact_laws_verified"] for r in sweep)

    payload = {
        "theorem_id": THEOREM_ID,
        "schema_version": SCHEMA_VERSION,
        "proof_status": "LOCAL_DERIVATION_REVIEW_PENDING_NOT_FORMALLY_VERIFIED",
        "scope_constraints": {
            "applies_to": "Single-shot quantum rejection sampling from a uniform box window to the Dirichlet-optimal sine window vs. peaked Lorentzian targets",
            "does_not_claim": "Unitary (post-selection-free) conversion without coherent amplitude amplification or direct state preparation",
            "controls_included": "Evaluates odd and even window lengths P in {7, 8, 15, 16, 31, 32}, verifying exact closed-form P_accept*(box -> sin*) > (P+1)/(2P) > 0.5, 100% post-selected fidelity, and strict dominance over Lorentzian targets.",
        },
        "rejection_sampling_sweep": sweep,
        "all_checks_passed": all_passed,
        "honesty_guardrails": {
            "accepted_speedup_candidate": False,
            "new_active_negative_result_created": False,
            "novelty_claim": False,
        },
    }
    digest = hashlib.sha256(
        json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()[:16]
    payload["certificate_sha256_16"] = digest
    return payload

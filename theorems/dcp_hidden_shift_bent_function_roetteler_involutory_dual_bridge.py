r"""DCP hidden-shift bent-function Roetteler involutory dual carry-cancellation bridge.

Establishes that when m = 2k overlapping CNOT wires carry both a quadratic bent carry
phase f(u) = u^T Q u (mod 2) (Subsystem 109) and a hidden shift s in {0, 1}^{2k} so that
the shifted phase oracle acts as U_{f_s}|u> = (-1)^{f(u (+) s)} |u>, Roetteler's 2-query
quantum hidden-shift algorithm:
    |Psi_out> = H^{\otimes 2k} * U_{f_tilde} * H^{\otimes 2k} * U_{f_s} * H^{\otimes 2k} |0^{2k}>
recovers the exact shift vector s in {0, 1}^{2k} in a SINGLE shot with 100% deterministic
probability (P(s) = 1.0), whereas standard 1-query Simon/Bernstein-Vazirani Hadamard
sampling H^{\otimes 2k} U_{f_s} H^{\otimes 2k} |0^{2k}> is completely dephased by the
bent carry into the uniform distribution P(w) = 2^{-2k}:

1. Complete Failure of 1-Query Bernstein-Vazirani Sampling Under Bent Carries:
   Applying a single query U_{f_s} followed by H^{\otimes 2k} produces amplitudes:
       <w | H^{\otimes 2k} U_{f_s} H^{\otimes 2k} | 0^{2k}> = 2^{-2k} sum_{u in {0,1}^{2k}} (-1)^{f(u (+) s) + <w, u>}
           = (-1)^{<w, s>} * hat{F}(w) = 2^{-k} * (-1)^{<w, s> + f_tilde(w)},
   where f_tilde: {0, 1}^{2k} -> {0, 1} is the dual bent function!
   Measuring in the computational basis yields P_{1-query}(w) = |2^{-k}|^2 = 2^{-2k}
   (completely uniform, zero information about s in a single copy)!

2. Exact 100% Single-Shot Recovery via Dual Bent Phase Uncomputation (Roetteler's Algorithm):
   Instead of measuring after H^{\otimes 2k}, applying the dual bent phase oracle
   U_{f_tilde}|w> = (-1)^{f_tilde(w)} |w> cancels (-1)^{2 * f_tilde(w)} == +1 identically
   across all 2^{2k} frequencies w in {0, 1}^{2k}, leaving the pure linear phase state:
       2^{-k} sum_{w in {0,1}^{2k}} (-1)^{<w, s>} |w> = H^{\otimes 2k} |s>!
   Applying the final H^{\otimes 2k} outputs |s> with 100% deterministic probability
   (P_{2-query}(s) = 1.000000000000) across ALL 2^{2k} hidden shifts s in {0, 1}^{2k}!
"""

from __future__ import annotations

import hashlib
import itertools
import json
import math
from typing import Any, Callable, Dict, List, Tuple


THEOREM_ID = "dcp_hidden_shift_bent_function_roetteler_involutory_dual_bridge"
SCHEMA_VERSION = "dcp-hidden-shift-bent-function-roetteler-involutory-dual-bridge-v1"


def _hadamard_transform_real(vec: List[float], m_bits: int) -> List[float]:
    r"""Apply fast Walsh-Hadamard transform H^{\otimes m} to a real state vector of length 2^m."""
    out = list(vec)
    dim = 1 << m_bits
    stride = 1
    while stride < dim:
        for base in range(0, dim, 2 * stride):
            for i in range(base, base + stride):
                a = out[i]
                b = out[i + stride]
                out[i] = a + b
                out[i + stride] = a - b
        stride <<= 1
    scale = 1.0 / math.sqrt(float(dim))
    return [v * scale for v in out]


def evaluate_roetteler_bent_carry_hidden_shift(
    k_pairs: int,
    bent_family: str = "maiorana_mcfarland",
) -> Dict[str, Any]:
    """Exhaustively verify 1-query uniform dephasing P=2^{-2k} vs 2-query Roetteler P(s)=1.0 across all 2^{2k} shifts s."""
    m_bits = 2 * k_pairs
    dim = 1 << m_bits

    # Define the bent carry truth table (-1)^{f(u)} on u in {0, ..., 2^{2k} - 1}:
    f_signs: List[float] = []
    for u in range(dim):
        bits = [(u >> j) & 1 for j in range(m_bits)]
        if bent_family == "maiorana_mcfarland":
            # Disjoint CZ carry pairs: f(u) = sum_{j=0}^{k-1} u_{2j} * u_{2j+1} mod 2 (strictly self-dual!)
            parity = sum(bits[2 * j] * bits[2 * j + 1] for j in range(k_pairs)) & 1
        elif bent_family == "symmetric_complete_graph":
            # Complete K_{2k} CZ carry graph: f(u) = C(wt(u), 2) mod 2
            wt = sum(bits)
            parity = (wt * (wt - 1) // 2) & 1
        else:
            raise ValueError(f"Unknown bent_family: {bent_family}")
        f_signs.append(-1.0 if parity else 1.0)

    # Compute the dual bent signs (-1)^{f_tilde(w)} = 2^k * hat{F}(w) directly via Walsh-Hadamard transform of f_signs / 2^{k}:
    # Note: _hadamard_transform_real divides by 2^k, so applying it to f_signs * 2^{-k} gives hat{F}(w) * 2^k in {-1, +1}!
    dual_signs = _hadamard_transform_real([s / math.sqrt(float(dim)) for s in f_signs], m_bits)
    # Scale by 2^k = sqrt(dim):
    dual_unit_signs = [v * math.sqrt(float(dim)) for v in dual_signs]
    max_dual_unit_err = max(abs(abs(v) - 1.0) for v in dual_unit_signs)

    # Exhaustively test all 2^{2k} hidden shifts s in {0, ..., 2^{2k} - 1}:
    max_1query_dev_from_uniform = 0.0
    min_2query_roetteler_success = 1.0

    for s_shift in range(dim):
        # 1. Input state after H^{\otimes 2k} |0^{2k}> and shifted oracle U_{f_s}:
        psi_after_fs = [f_signs[u ^ s_shift] / math.sqrt(float(dim)) for u in range(dim)]

        # 2. State after 1st Hadamard H^{\otimes 2k} (1-query BV circuit):
        psi_1query = _hadamard_transform_real(psi_after_fs, m_bits)
        for w in range(dim):
            prob_w = psi_1query[w] ** 2
            max_1query_dev_from_uniform = max(max_1query_dev_from_uniform, abs(prob_w - (1.0 / float(dim))))

        # 3. Apply dual bent phase oracle U_{f_tilde} and 2nd Hadamard H^{\otimes 2k} (Roetteler 2-query circuit):
        psi_after_dual = [psi_1query[w] * dual_unit_signs[w] for w in range(dim)]
        psi_2query_out = _hadamard_transform_real(psi_after_dual, m_bits)
        prob_s = psi_2query_out[s_shift] ** 2
        min_2query_roetteler_success = min(min_2query_roetteler_success, prob_s)

    return {
        "k_pairs": k_pairs,
        "m_qubits": m_bits,
        "hilbert_dim": dim,
        "bent_family": bent_family,
        "is_strictly_self_dual": max(abs(f_signs[u] - dual_unit_signs[u]) for u in range(dim)) < 1e-12,
        "max_dual_unit_modulus_error": max_dual_unit_err,
        "max_1query_deviation_from_uniform_1_over_dim": max_1query_dev_from_uniform,
        "min_2query_roetteler_success_prob_across_all_shifts": min_2query_roetteler_success,
        "exact_roetteler_laws_verified": (
            max_dual_unit_err < 1e-12
            and max_1query_dev_from_uniform < 1e-12
            and abs(min_2query_roetteler_success - 1.0) < 1e-12
        ),
    }


def generate_dcp_hidden_shift_bent_function_roetteler_involutory_dual_certificate() -> Dict[str, Any]:
    """Generate the complete certificate for the Roetteler bent-function hidden-shift carry-cancellation bridge."""
    mm_4qubit = evaluate_roetteler_bent_carry_hidden_shift(k_pairs=2, bent_family="maiorana_mcfarland")
    sym_4qubit = evaluate_roetteler_bent_carry_hidden_shift(k_pairs=2, bent_family="symmetric_complete_graph")
    mm_6qubit = evaluate_roetteler_bent_carry_hidden_shift(k_pairs=3, bent_family="maiorana_mcfarland")

    all_passed = (
        mm_4qubit["exact_roetteler_laws_verified"]
        and mm_4qubit["is_strictly_self_dual"]
        and sym_4qubit["exact_roetteler_laws_verified"]
        and mm_6qubit["exact_roetteler_laws_verified"]
        and mm_6qubit["is_strictly_self_dual"]
    )

    payload = {
        "theorem_id": THEOREM_ID,
        "schema_version": SCHEMA_VERSION,
        "proof_status": "LOCAL_DERIVATION_REVIEW_PENDING_NOT_FORMALLY_VERIFIED",
        "scope_constraints": {
            "applies_to": "Roetteler 2-query bent-function hidden-shift algorithm for canceling quadratic CNOT carry phases",
            "does_not_claim": "Oracle access to the shifted bent function f(u (+) s) without a quadratic carry interaction",
            "controls_included": "Exhaustively tests all 16 shifts of 4-qubit Maiorana-McFarland and complete-graph bent carries and all 64 shifts of 6-qubit Maiorana-McFarland carries, verifying 1-query uniform dephasing (1/2^{2k}) vs 2-query 100% deterministic recovery (P(s)=1.0).",
        },
        "maiorana_mcfarland_4q_audit": mm_4qubit,
        "symmetric_complete_4q_audit": sym_4qubit,
        "maiorana_mcfarland_6q_audit": mm_6qubit,
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

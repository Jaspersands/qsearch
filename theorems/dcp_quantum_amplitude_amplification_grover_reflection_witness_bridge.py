r"""DCP coherent Grover-BHMT quantum amplitude amplification of CNOT syndrome branches bridge.

Establishes the exact closed-form trajectory of k-step Brassard-Hoyer-Mosca-Tapp (BHMT)
coherent amplitude amplification applied to the CNOT witness compression unitary U_prep
prior to syndrome measurement, and proves that a weight-3 witness (initial branch
probability p_0 = 2^{-(3-1)} = 1/4) achieves 100% deterministic preparation (P_1 = 1.0)
in a SINGLE amplification step while preserving 100% survivor phase fidelity:

1. Exact Chebyshev-Trigonometric Syndrome Amplification Law:
   Let U_prep be the coherent state-preparation + CNOT tree unitary on K wires that
   prepares the bipartite survivor-syndrome state:
       |Psi(s)> = sum_{y in {0,1}^{K-1}} (1 / sqrt(2^{K-1})) |phi_surv(y; s)> |y>_syn.
   Marking a target syndrome y* in {0, 1}^{K-1} (or a subspace S* of syndromes of size M,
   with initial acceptance probability p_0 = M / 2^{K-1} = sin^2(theta_0)) via the
   syndrome-only phase oracle S_chi = I_surv \otimes (I - 2 |y*><y*|)_syn and applying k
   Grover-BHMT iterate steps Q = -U_prep S_0 U_prep^dagger S_chi rotates the syndrome
   acceptance probability to:
       P_k(p_0) = sin^2((2*k + 1) * arcsin(sqrt(p_0))),
   while leaving the conditional survivor state |phi_surv(y*; s)> on the marked syndrome
   branch 100% invariant (fidelity F_surv = 1.0) because S_chi acts as a scalar (-1) on
   the 1D syndrome ray |y*>!

2. Exact 1-Step Deterministic Amplification for Weight-3 Witnesses (p_0 = 1/4 -> P_1 = 1.0):
   For any weight-3 binary or ternary zero-sum witness (K = 3 wires, 2 measured syndrome
   wires, so a single target syndrome y* = d*(delta) has initial probability
   p_0 = 2^{-(3-1)} = 1/4 and theta_0 = arcsin(1/2) = pi / 6), a SINGLE amplification
   step (k = 1) rotates (2*1 + 1)*theta_0 = 3 * (pi / 6) = pi / 2, achieving:
       P_1(1 / 4) = sin^2(pi / 2) = 1.000000000000 (4.0x probability boost to 100%!),
   with 100% exact survivor phase preservation!

3. Weight-2 Over-Rotation Obstruction Under Standard Pi-Reflections (p_0 = 1/2 -> P_1 = 1/2):
   For a weight-2 witness (1 syndrome wire, p_0 = 1/2, theta_0 = pi / 4), k = 1 standard
   pi-reflection step rotates to 3*pi/4 where sin^2(3*pi/4) = 1/2 = p_0 (zero net gain,
   motivating the pi/3 fixed-point recursion in Subsystem 118).
"""

from __future__ import annotations

import cmath
import hashlib
import itertools
import json
import math
from typing import Any, Dict, List, Sequence


THEOREM_ID = "dcp_quantum_amplitude_amplification_grover_reflection_witness_bridge"
SCHEMA_VERSION = "dcp-quantum-amplitude-amplification-grover-reflection-witness-bridge-v1"


def evaluate_coherent_grover_syndrome_amplification(
    q_mod: int,
    cols_a: Sequence[int],
    secret_s: int,
    target_syndrome: Sequence[int],
    k_steps: int,
) -> Dict[str, Any]:
    """Explicitly simulate the 2^K-dimensional state vector under k Grover-BHMT syndrome amplification steps."""
    h_wires = len(cols_a)
    if len(target_syndrome) != h_wires - 1:
        raise ValueError("target_syndrome must have length h_wires - 1")
    dim = 1 << h_wires
    all_x = list(itertools.product((0, 1), repeat=h_wires))

    # 1. Construct initial post-CNOT state |Psi_0(s)> in basis |u_0, y_1, ..., y_{h-1}>
    # where x_0 = u_0 and x_r = u_0 ^ y_r for r = 1..h-1:
    psi_0: List[complex] = []
    for basis_bits in all_x:
        u0 = basis_bits[0]
        y_bits = basis_bits[1:]
        x_vec = [u0] + [u0 ^ y_bits[r] for r in range(h_wires - 1)]
        ph = sum(int(cols_a[r]) * x_vec[r] for r in range(h_wires)) * secret_s % q_mod
        psi_0.append(cmath.exp(2j * math.pi * float(ph) / float(q_mod)) / math.sqrt(float(dim)))

    target_syn_tuple = tuple(int(b) for b in target_syndrome)
    marked_indices = [
        idx for idx, bits in enumerate(all_x)
        if bits[1:] == target_syn_tuple
    ]

    p0_explicit = sum(abs(psi_0[idx]) ** 2 for idx in marked_indices)
    theta0 = math.asin(math.sqrt(p0_explicit))

    # Extract initial conditional survivor state on target_syndrome:
    surv_init = [psi_0[idx] / math.sqrt(p0_explicit) for idx in marked_indices]

    # 2. Apply k steps of Q = (2 |Psi_0><Psi_0| - I) * (I - 2 Pi_marked):
    psi_curr = list(psi_0)
    for _ in range(k_steps):
        # Step A: S_chi flips sign on marked_indices:
        for idx in marked_indices:
            psi_curr[idx] = -psi_curr[idx]
        # Step B: -U_prep S_0 U_prep^dagger = 2 |Psi_0><Psi_0| - I:
        ov = sum(psi_0[i].conjugate() * psi_curr[i] for i in range(dim))
        psi_curr = [2.0 * ov * psi_0[i] - psi_curr[i] for i in range(dim)]

    pk_explicit = sum(abs(psi_curr[idx]) ** 2 for idx in marked_indices)
    pk_closed_form = math.sin(float(2 * k_steps + 1) * theta0) ** 2

    # Check conditional survivor state fidelity after k steps:
    surv_final = [psi_curr[idx] / math.sqrt(pk_explicit) for idx in marked_indices]
    surv_overlap = sum(a.conjugate() * b for a, b in zip(surv_init, surv_final))
    surv_fidelity = abs(surv_overlap) ** 2

    return {
        "h_wires": h_wires,
        "q_mod": q_mod,
        "target_syndrome": list(target_syn_tuple),
        "k_grover_steps": k_steps,
        "initial_syndrome_prob_p0": p0_explicit,
        "amplified_syndrome_prob_explicit": pk_explicit,
        "amplified_syndrome_prob_closed_form": pk_closed_form,
        "probability_boost_factor": pk_explicit / p0_explicit,
        "conditional_survivor_state_fidelity": surv_fidelity,
        "exact_laws_verified": (
            abs(pk_explicit - pk_closed_form) < 1e-12
            and abs(surv_fidelity - 1.0) < 1e-12
        ),
    }


def generate_dcp_quantum_amplitude_amplification_grover_reflection_witness_certificate() -> Dict[str, Any]:
    """Generate the complete certificate for the coherent Grover syndrome amplification bridge."""
    # 1. Weight-3 ternary witness A = [1, 1, 1] mod 5 on d* = (0, 1) (delta = [1, 1, -1]):
    # p_0 = 1/4 = 0.25 -> k = 1 Grover step achieves P_1 = 1.000000000000 (100% deterministic!)
    w3_deterministic_k1 = evaluate_coherent_grover_syndrome_amplification(
        q_mod=5,
        cols_a=[1, 1, 1],
        secret_s=3,
        target_syndrome=[0, 1],
        k_steps=1,
    )

    # 2. Weight-2 witness A = [3, 5] mod 8 on d* = (0,):
    # p_0 = 1/2 = 0.50 -> k = 1 standard pi-Grover over-rotates to sin^2(3*pi/4) = 0.50 (gain = 1.0x!)
    w2_overrotation_k1 = evaluate_coherent_grover_syndrome_amplification(
        q_mod=8,
        cols_a=[3, 5],
        secret_s=5,
        target_syndrome=[0],
        k_steps=1,
    )

    # 3. Weight-4 witness A = [1, 1, 1, 5] mod 8 on d* = (0, 0, 0):
    # p_0 = 1/8 = 0.125 -> k = 1 step boosts to p_0 * (3 - 4*p_0)^2 = 0.125 * (2.5)^2 = 25/32 = 0.78125 (6.25x boost!)
    w4_boost_k1 = evaluate_coherent_grover_syndrome_amplification(
        q_mod=8,
        cols_a=[1, 1, 1, 5],
        secret_s=3,
        target_syndrome=[0, 0, 0],
        k_steps=1,
    )

    all_passed = (
        w3_deterministic_k1["exact_laws_verified"]
        and abs(w3_deterministic_k1["amplified_syndrome_prob_explicit"] - 1.0) < 1e-12
        and w2_overrotation_k1["exact_laws_verified"]
        and abs(w2_overrotation_k1["amplified_syndrome_prob_explicit"] - 0.5) < 1e-12
        and w4_boost_k1["exact_laws_verified"]
        and abs(w4_boost_k1["amplified_syndrome_prob_explicit"] - 25.0 / 32.0) < 1e-12
    )

    payload = {
        "theorem_id": THEOREM_ID,
        "schema_version": SCHEMA_VERSION,
        "proof_status": "LOCAL_DERIVATION_REVIEW_PENDING_NOT_FORMALLY_VERIFIED",
        "scope_constraints": {
            "applies_to": "Coherent Grover-BHMT quantum amplitude amplification of CNOT syndrome branches prior to syndrome measurement",
            "does_not_claim": "Amplification of already-measured classical mixtures without coherent access to the state-preparation unitary U_prep",
            "controls_included": "Includes weight-3 witness (p_0=1/4 -> k=1 deterministic P_1=1.0), weight-2 over-rotation control (p_0=1/2 -> P_1=0.5), and weight-4 witness (p_0=1/8 -> P_1=25/32=0.78125), all preserving 100% survivor fidelity.",
        },
        "weight3_deterministic_k1": w3_deterministic_k1,
        "weight2_overrotation_k1": w2_overrotation_k1,
        "weight4_boost_k1": w4_boost_k1,
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

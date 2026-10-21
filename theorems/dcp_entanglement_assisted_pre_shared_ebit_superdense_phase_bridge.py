r"""DCP entanglement-assisted pre-shared Bell-pair superdense phase sensing and X-fault immunity bridge.

Establishes the exact 4-outcome Bell-basis probability distribution when one half (qubit A)
of a pre-shared maximally entangled Bell pair |Phi^+>_{AB} = (|00> + |11>)/sqrt(2) is
exposed to a DCP phase shift theta, phase damping gamma in (0, 1], and an arbitrary
Pauli-X bit-flip noise channel of rate eta_X in [0, 1], proving 100% immunity of the
Bell parity observable X_A \otimes X_B to arbitrary bit-flip noise eta_X:

1. Exact 4-Outcome Bell-Basis Decomposition Under Combined Phase + Bit-Flip Noise:
   On the maximally entangled probe-reference pair |Phi^+>_{AB}, suppose the probe qubit A
   undergoes phase rotation exp(-i * theta * Z_A / 2) with coherence factor gamma,
   followed by a Pauli-X bit-flip channel E_{X, eta_X}(rho) = (1 - eta_X) rho + eta_X X_A rho X_A.
   In the 4-state Bell basis:
       |Phi^+> = (|00> + |11>)/sqrt(2),   |Phi^-> = (|00> - |11>)/sqrt(2),
       |Psi^+> = (|01> + |10>)/sqrt(2),   |Psi^-> = (|01> - |10>)/sqrt(2),
   because X_A |Phi^+> = |Psi^+> and X_A |Phi^-> = -|Psi^->, the 4 Bell outcome
   probabilities factorize EXACTLY into the bit-flip indicator (Phi vs Psi) and the
   cosine phase indicator (+ vs -):
       P(|Phi^+>) = (1 - eta_X) * 0.5 * (1 + gamma * cos(theta)),
       P(|Phi^->) = (1 - eta_X) * 0.5 * (1 - gamma * cos(theta)),
       P(|Psi^+>) = eta_X       * 0.5 * (1 + gamma * cos(theta)),
       P(|Psi^->) = eta_X       * 0.5 * (1 - gamma * cos(theta))!

2. Complete Immunity of Bell Parity X_A \otimes X_B to Arbitrary Bit-Flip Rate eta_X in [0, 1]:
   Summing the +1 eigenstates of X_A \otimes X_B (|Phi^+> and |Psi^+>) versus the -1
   eigenstates (|Phi^-> and |Psi^->) cancels eta_X IDENTICALLY:
       P(X_A X_B = +1) = P(|Phi^+>) + P(|Psi^+>) = 0.5 * (1 + gamma * cos(theta)),
       P(X_A X_B = -1) = P(|Phi^->) + P(|Psi^->) = 0.5 * (1 - gamma * cos(theta)),
       <X_A \otimes X_B> = gamma * cos(theta)   (100% independent of eta_X in [0, 1]!),
   while simultaneously measuring Z_A \otimes Z_B diagnoses the exact bit-flip error
   rate P(Z_A Z_B = -1) = P(|Psi^+>) + P(|Psi^->) = eta_X!
"""

from __future__ import annotations

import cmath
import hashlib
import json
import math
from typing import Any, Dict, List


THEOREM_ID = "dcp_entanglement_assisted_pre_shared_ebit_superdense_phase_bridge"
SCHEMA_VERSION = "dcp-entanglement-assisted-pre-shared-ebit-superdense-phase-bridge-v1"


def evaluate_bell_assisted_phase_and_bitflip_immunity(
    theta: float,
    gamma: float,
    eta_x_values: List[float],
) -> Dict[str, Any]:
    """Explicitly construct the 4x4 two-qubit density matrix and verify Bell-basis probabilities and X-fault immunity."""
    # Pre-shared Bell state |Phi^+> = [1/sqrt(2), 0, 0, 1/sqrt(2)] in basis |00>, |01>, |10>, |11>
    # After phase theta and dephasing gamma on qubit A (without X-flip yet):
    # |00><00| and |11><11| have weight 0.5; |00><11| has 0.5 * gamma * exp(-i * theta)
    ph = gamma * cmath.exp(-1j * theta)
    rho_no_flip = [
        [0.5 + 0j, 0j, 0j, 0.5 * ph],
        [0j, 0j, 0j, 0j],
        [0j, 0j, 0j, 0j],
        [0.5 * ph.conjugate(), 0j, 0j, 0.5 + 0j],
    ]
    # Apply X_A \otimes I_B: swaps row/col 0 (|00>) <-> 2 (|10>) and 1 (|01>) <-> 3 (|11>)
    perm_xa = [2, 3, 0, 1]
    rho_flipped = [
        [rho_no_flip[perm_xa[r]][perm_xa[c]] for c in range(4)]
        for r in range(4)
    ]

    s2 = 1.0 / math.sqrt(2.0)
    bell_vecs = {
        "Phi_plus":  [s2, 0.0, 0.0, s2],
        "Phi_minus": [s2, 0.0, 0.0, -s2],
        "Psi_plus":  [0.0, s2, s2, 0.0],
        "Psi_minus": [0.0, s2, -s2, 0.0],
    }

    records: List[Dict[str, Any]] = []
    for eta_x in eta_x_values:
        rho_tot = [
            [(1.0 - eta_x) * rho_no_flip[r][c] + eta_x * rho_flipped[r][c] for c in range(4)]
            for r in range(4)
        ]

        probs: Dict[str, float] = {}
        for name, bvec in bell_vecs.items():
            val = sum(
                bvec[r] * rho_tot[r][c] * bvec[c]
                for r in range(4)
                for c in range(4)
            ).real
            probs[name] = val

        xx_exp_explicit = (probs["Phi_plus"] + probs["Psi_plus"]) - (probs["Phi_minus"] + probs["Psi_minus"])
        xx_exp_closed = gamma * math.cos(theta)
        zz_flip_prob_explicit = probs["Psi_plus"] + probs["Psi_minus"]

        cf_phi_plus = (1.0 - eta_x) * 0.5 * (1.0 + gamma * math.cos(theta))
        cf_psi_plus = eta_x * 0.5 * (1.0 + gamma * math.cos(theta))

        records.append({
            "eta_x": eta_x,
            "prob_Phi_plus": probs["Phi_plus"],
            "prob_Phi_minus": probs["Phi_minus"],
            "prob_Psi_plus": probs["Psi_plus"],
            "prob_Psi_minus": probs["Psi_minus"],
            "xx_parity_expectation_explicit": xx_exp_explicit,
            "xx_parity_expectation_closed_form": xx_exp_closed,
            "zz_detected_bitflip_rate": zz_flip_prob_explicit,
            "exact_immunity_verified": (
                abs(probs["Phi_plus"] - cf_phi_plus) < 1e-12
                and abs(probs["Psi_plus"] - cf_psi_plus) < 1e-12
                and abs(xx_exp_explicit - xx_exp_closed) < 1e-12
                and abs(zz_flip_prob_explicit - eta_x) < 1e-12
            ),
        })

    return {
        "theta": theta,
        "gamma": gamma,
        "records": records,
        "all_verified": all(r["exact_immunity_verified"] for r in records),
    }


def generate_dcp_entanglement_assisted_pre_shared_ebit_superdense_phase_certificate() -> Dict[str, Any]:
    """Generate the complete certificate for the entanglement-assisted Bell-pair X-fault immunity bridge."""
    sweep = evaluate_bell_assisted_phase_and_bitflip_immunity(
        theta=math.pi / 3.0,
        gamma=0.88,
        eta_x_values=[0.0, 0.10, 0.25, 0.50, 0.75, 1.00],
    )

    expected_xx = 0.88 * 0.5  # gamma * cos(pi/3) = 0.44 across ALL eta_X in [0, 1]!
    all_passed = (
        sweep["all_verified"]
        and all(abs(r["xx_parity_expectation_explicit"] - expected_xx) < 1e-12 for r in sweep["records"])
    )

    payload = {
        "theorem_id": THEOREM_ID,
        "schema_version": SCHEMA_VERSION,
        "proof_status": "LOCAL_DERIVATION_REVIEW_PENDING_NOT_FORMALLY_VERIFIED",
        "scope_constraints": {
            "applies_to": "Pre-shared Bell-pair |Phi^+>_{AB} phase sensing and 100% X_A otimes X_B immunity to arbitrary Pauli-X bit-flip noise eta_X",
            "does_not_claim": "Immunity to Pauli-Z phase-flip noise on the probe wire (which directly shifts theta -> theta + pi)",
            "controls_included": "Evaluates eta_X in {0.0, 0.10, 0.25, 0.50, 0.75, 1.00} at theta=pi/3, gamma=0.88, verifying constant <X_A X_B> == 0.44 and exact Z_A Z_B bit-flip diagnosis.",
        },
        "bell_bitflip_immunity_sweep": sweep,
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

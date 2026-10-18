r"""DCP Walsh-Hadamard bent-function nonlinear carry spectrum bridge.

Establishes the exact Walsh-Hadamard Fourier spectrum of the quadratic binary-XOR carry
phase function f_sym(u) = sum_{1 <= j < l <= m} u_j u_l (mod 2) generated on m overlapping
CNOT survivor wires at modulus q = 4 (t = 2, Subsystem 87):

1. Exact Bent-Function Flat Spectrum for Even Overlap Multiplicity (m = 2k):
   When a row r participates in an EVEN number m = 2k >= 2 of overlapping CNOT trees with
   odd inner product <A_{., r}, s> == 1 (mod 2), the quadratic carry factor is:
       (-1)^{sum_{1 <= j < l <= 2k} u_j u_l} = (-1)^{C(|u|, 2)}.
   Because the associated 2k x 2k binary symplectic adjacency matrix J_{2k} - I_{2k}
   (all 1s off the diagonal, 0s on the diagonal) has full rank 2k over GF(2) for every
   even 2k, f_sym(u) is an EXACT maximally nonlinear BENT Boolean function!
   Consequently, its normalized Walsh-Hadamard transform:
       hat{F}(w) = 2^{-2k} sum_{u in {0,1}^{2k}} (-1)^{f_sym(u) + <w, u>}
   has completely flat magnitude across all 2^{2k} frequency strings w in {0, 1}^{2k}:
       |hat{F}(w)| = 2^{-k} = 2^{-m/2},   and   P_Hadamard(w) = |hat{F}(w)|^2 = 2^{-2k}!
   Therefore, measuring the 2k overlapping wires in the Hadamard X^{\otimes 2k} basis
   without CZ repair produces an EXACT uniform distribution 2^{-2k} (zero Shannon mutual
   information with any linear Pauli-Z shift)!

2. Exact Semi-Bent / Near-Bent Spectrum for Odd Overlap Multiplicity (m = 2k + 1):
   When m = 2k + 1 is ODD, the matrix J_{2k+1} - I_{2k+1} over GF(2) has rank 2k and a
   1-dimensional kernel spanned by the all-ones vector 1^{2k+1}.
   Consequently, |hat{F}(w)|^2 takes only two values across {0, 1}^{2k+1}:
   - P_Hadamard(w) = 2^{-2k} on the 2^{2k} strings w of one parity,
   - P_Hadamard(w) = 0       on the 2^{2k} strings w of the opposite parity!
"""

from __future__ import annotations

import hashlib
import itertools
import json
import math
from typing import Any, Dict, List


THEOREM_ID = "dcp_walsh_hadamard_gold_bent_nonlinear_carry_spectrum_bridge"
SCHEMA_VERSION = "dcp-walsh-hadamard-gold-bent-nonlinear-carry-spectrum-bridge-v1"


def evaluate_quadratic_carry_walsh_spectrum(m_trees: int) -> Dict[str, Any]:
    """Compute the exact Walsh-Hadamard spectrum of (-1)^{sum_{j<l} u_j u_l} on {0,1}^m."""
    if type(m_trees) is not int or m_trees < 2 or m_trees > 7:
        raise ValueError("m_trees must be an integer in [2, 7]")

    dim = 1 << m_trees
    all_u = list(itertools.product((0, 1), repeat=m_trees))

    # Truth table of (-1)^{C(wt(u), 2)}
    f_sign = [
        -1.0 if ((sum(u) * (sum(u) - 1) // 2) & 1) else 1.0
        for u in all_u
    ]

    probabilities: List[float] = []
    for w in all_u:
        acc = 0.0
        for idx, u in enumerate(all_u):
            dot = sum(w[j] * u[j] for j in range(m_trees)) & 1
            w_sign = -1.0 if dot else 1.0
            acc += f_sign[idx] * w_sign
        hat_f = acc / float(dim)
        probabilities.append(hat_f ** 2)

    is_even_m = (m_trees % 2) == 0
    k_half = m_trees // 2

    if is_even_m:
        # Bent function: all 2^{2k} probabilities equal 2^{-2k} = 1 / dim!
        expected_p = 1.0 / float(dim)
        max_flat_err = max(abs(p - expected_p) for p in probabilities)
        non_zero_count = sum(1 for p in probabilities if p > 1e-12)
        spectrum_verified = (max_flat_err < 1e-12) and (non_zero_count == dim)
    else:
        # Semi-bent function (m = 2k + 1): exactly half (2^{2k}) have p = 2^{-2k} = 2 / dim, half have p = 0!
        expected_nonzero_p = 2.0 / float(dim)
        non_zero_count = sum(1 for p in probabilities if p > 1e-12)
        zero_count = sum(1 for p in probabilities if p <= 1e-12)
        max_flat_err = max(
            abs(p - expected_nonzero_p) if p > 1e-12 else abs(p)
            for p in probabilities
        )
        spectrum_verified = (
            max_flat_err < 1e-12
            and non_zero_count == (dim // 2)
            and zero_count == (dim // 2)
        )

    shannon_entropy_bits = -sum(p * math.log2(p) for p in probabilities if p > 1e-15)

    return {
        "m_trees": m_trees,
        "is_even_bent_dimension": is_even_m,
        "hilbert_dim": dim,
        "non_zero_hadamard_outcomes": non_zero_count,
        "shannon_entropy_bits": shannon_entropy_bits,
        "expected_entropy_bits": float(m_trees if is_even_m else m_trees - 1),
        "max_spectrum_error": max_flat_err,
        "exact_bent_or_semibent_law_verified": (
            spectrum_verified
            and abs(shannon_entropy_bits - float(m_trees if is_even_m else m_trees - 1)) < 1e-12
        ),
    }


def generate_dcp_walsh_hadamard_gold_bent_nonlinear_carry_spectrum_certificate() -> Dict[str, Any]:
    """Generate the complete certificate for the Walsh-Hadamard bent-function carry spectrum bridge."""
    sweep = [evaluate_quadratic_carry_walsh_spectrum(m) for m in (2, 3, 4, 5, 6)]
    all_passed = all(r["exact_bent_or_semibent_law_verified"] for r in sweep)

    payload = {
        "theorem_id": THEOREM_ID,
        "schema_version": SCHEMA_VERSION,
        "proof_status": "LOCAL_DERIVATION_REVIEW_PENDING_NOT_FORMALLY_VERIFIED",
        "scope_constraints": {
            "applies_to": "Walsh-Hadamard Fourier spectrum of quadratic binary-XOR carry states (-1)^{sum_{j<l} u_j u_l} across even (bent) and odd (semi-bent) overlap multiplicities m",
            "does_not_claim": "Flatness of the Hadamard spectrum after applying conditional pairwise CZ carry repair (Subsystem 87)",
            "controls_included": "Evaluates m in {2, 3, 4, 5, 6}, verifying exact bent flatness (H = m bits, P(w) = 2^{-m}) for even m in {2, 4, 6} and exact semi-bent half-support (H = m - 1 bits) for odd m in {3, 5}.",
        },
        "carry_spectrum_sweep": sweep,
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

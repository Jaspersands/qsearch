r"""DCP banded-QFT truncation phase-leakage vs. exact dyadic sublattice fidelity bridge.

Establishes for the band-b truncated inverse Quantum Fourier Transform QFT_{2^m}^{(b)\dagger}
(retaining controlled-R_d^\dagger gates only up to distance 1 <= d <= b <= m, where
b = 1 is the entanglement-free Hadamard layer H^{\otimes m}):

1. Exact Bitwise Product Formula for Band-b Peak Survival Probability:
   For any pure dyadic progression state |psi(K_0)> = 2^{-m/2} sum_{U=0}^{2^m - 1} exp(2*pi*i * U * K_0 / 2^m) |U>
   with integer frequency K_0 = sum_{l=0}^{m-1} k_l 2^{m - 1 - l} in Z_{2^m} (where k_0 is MSB and k_{m-1} is LSB
   of the bit-reversed Fourier output), omitting controlled phase rotations of distance d = l - j + 1 > b
   leaves a residual angle delta_j^{(b)}(K_0) = 2*pi * sum_{l = j + b}^{m - 1} k_l 2^{j - 1 - l} on each wire j.
   Consequently, the exact probability of observing the true frequency K_0 under QFT_{2^m}^{(b)\dagger} is:
       P_{QFT^{(b)}}(K_0 | K_0) = prod_{j=0}^{m - 1 - b} cos^2(pi * sum_{l = j + b}^{m - 1} k_l 2^{j - 1 - l}).

2. Exact Zero-Leakage Sublattice Criterion (K_0 in 2^{m - b} Z_{2^m}):
   P_{QFT^{(b)}}(K_0 | K_0) == 1.0 (zero truncation loss) holds if and only if k_l == 0
   for all l >= b, which is equivalent to K_0 == 0 (mod 2^{m - b}).
   In particular:
     - At b = 1 (H^{\otimes m} with zero two-qubit gates): Exact 100% concentration holds
       if and only if K_0 in {0, 2^{m - 1}} (the half-period dyadic subgroup targeted after
       L = m - 1 stages of CNOT elimination!).
     - For odd frequencies K_0 == 1 (mod 2) (e.g. K_0 = 1), b = 1 suffers severe phase
       leakage P_{H^{\otimes m}}(1 | 1) = prod_{j=0}^{m-2} cos^2(pi / 2^{m - j}), whereas
       increasing bandwidth to b >= m - v_2(K_0) restores 100% unit fidelity.
"""

from __future__ import annotations

import cmath
import hashlib
import json
import math
from typing import Any, Dict, List


THEOREM_ID = "dcp_banded_qft_truncation_vs_dyadic_cnot_fidelity_bridge"
SCHEMA_VERSION = "dcp-banded-qft-truncation-vs-dyadic-cnot-fidelity-bridge-v1"


def banded_qft_peak_probability_explicit_circuit(
    m_wires: int,
    k0_freq: int,
    band_b: int,
) -> float:
    """Compute P_{QFT^{(b)}}(K_0 | K_0) by explicit 2^m-dimensional summation with truncated phase kernel."""
    if type(m_wires) is not int or not 2 <= m_wires <= 7:
        raise ValueError("m_wires must be in [2, 7]")
    if type(band_b) is not int or not 1 <= band_b <= m_wires:
        raise ValueError("band_b must satisfy 1 <= band_b <= m_wires")
    dim = 1 << m_wires
    k0 = k0_freq % dim
    k_bits = [(k0 >> (m_wires - 1 - l_idx)) & 1 for l_idx in range(m_wires)]

    amp = 0j
    for u_int in range(dim):
        u_bits = [(u_int >> j_idx) & 1 for j_idx in range(m_wires)]
        true_phase = 2.0 * math.pi * float(u_int * k0) / float(dim)
        trunc_phase = 0.0
        for j_idx in range(m_wires):
            if u_bits[j_idx] == 0:
                continue
            for l_idx in range(j_idx, min(m_wires, j_idx + band_b)):
                if k_bits[l_idx]:
                    trunc_phase += 2.0 * math.pi * (2.0 ** (j_idx - 1 - l_idx))
        amp += cmath.exp(1j * (true_phase - trunc_phase)) / float(dim)
    return abs(amp) ** 2


def banded_qft_peak_probability_closed_form(
    m_wires: int,
    k0_freq: int,
    band_b: int,
) -> float:
    """Closed-form product prod_{j=0}^{m-1-b} cos^2(pi * sum_{l=j+b}^{m-1} k_l 2^{j-1-l})."""
    if type(m_wires) is not int or not 2 <= m_wires <= 12:
        raise ValueError("m_wires must be in [2, 12]")
    if type(band_b) is not int or not 1 <= band_b <= m_wires:
        raise ValueError("band_b must satisfy 1 <= band_b <= m_wires")
    dim = 1 << m_wires
    k0 = k0_freq % dim
    k_bits = [(k0 >> (m_wires - 1 - l_idx)) & 1 for l_idx in range(m_wires)]

    prod_val = 1.0
    for j_idx in range(m_wires - band_b):
        angle = math.pi * sum(
            k_bits[l_idx] * (2.0 ** (j_idx - 1 - l_idx))
            for l_idx in range(j_idx + band_b, m_wires)
        )
        prod_val *= math.cos(angle) ** 2
    return prod_val


def verify_banded_qft_product_law_and_sublattice_criterion(
    m_wires: int,
    band_b: int,
) -> Dict[str, Any]:
    """Verify across all K_0 in Z_{2^m} that explicit banded QFT matches the product formula and K_0 == 0 mod 2^{m-b} iff P == 1."""
    dim = 1 << m_wires
    sublattice_step = 1 << (m_wires - band_b)
    max_formula_err = 0.0
    iff_sublattice_verified = True
    unit_fidelity_count = 0

    for k0 in range(dim):
        p_exp = banded_qft_peak_probability_explicit_circuit(m_wires, k0, band_b)
        p_cf = banded_qft_peak_probability_closed_form(m_wires, k0, band_b)
        max_formula_err = max(max_formula_err, abs(p_exp - p_cf))

        is_unit = abs(p_exp - 1.0) < 1e-12
        in_sublattice = (k0 % sublattice_step) == 0
        if is_unit != in_sublattice:
            iff_sublattice_verified = False
        if is_unit:
            unit_fidelity_count += 1

    return {
        "m_wires": m_wires,
        "band_b": band_b,
        "dim_2_to_m": dim,
        "sublattice_modulus_2_to_m_minus_b": sublattice_step,
        "unit_fidelity_frequency_count": unit_fidelity_count,
        "expected_sublattice_size": 1 << band_b,
        "odd_k0_1_peak_probability": banded_qft_peak_probability_closed_form(m_wires, 1, band_b),
        "half_period_peak_probability": banded_qft_peak_probability_closed_form(m_wires, dim // 2, band_b),
        "max_formula_error": max_formula_err,
        "exact_product_and_sublattice_iff_verified": (
            max_formula_err < 1e-12
            and iff_sublattice_verified
            and unit_fidelity_count == (1 << band_b)
        ),
    }


def generate_dcp_banded_qft_truncation_vs_dyadic_cnot_fidelity_certificate() -> Dict[str, Any]:
    """Generate the complete certificate for the banded-QFT truncation vs dyadic CNOT fidelity bridge."""
    audits = [
        verify_banded_qft_product_law_and_sublattice_criterion(m_wires=4, band_b=1),
        verify_banded_qft_product_law_and_sublattice_criterion(m_wires=4, band_b=2),
        verify_banded_qft_product_law_and_sublattice_criterion(m_wires=4, band_b=3),
        verify_banded_qft_product_law_and_sublattice_criterion(m_wires=4, band_b=4),
    ]

    all_passed = (
        all(a["exact_product_and_sublattice_iff_verified"] for a in audits)
        and abs(audits[0]["half_period_peak_probability"] - 1.0) < 1e-12
        and audits[0]["odd_k0_1_peak_probability"] < 0.42
        and abs(audits[3]["odd_k0_1_peak_probability"] - 1.0) < 1e-12
    )

    payload = {
        "theorem_id": THEOREM_ID,
        "schema_version": SCHEMA_VERSION,
        "proof_status": "LOCAL_DERIVATION_REVIEW_PENDING_NOT_FORMALLY_VERIFIED",
        "scope_constraints": {
            "applies_to": "Band-b truncated inverse QFT_{2^m}^{(b)_dagger} on m-wire dyadic progression phase states",
            "does_not_claim": "Unit fidelity of b=1 (H^{tensor m}) outside the half-period sublattice {0, 2^{m-1}}",
            "controls_included": "Includes exhaustive verification across m=4, b=1..4 showing P(K_0|K_0) == 1.0 iff K_0 in 2^{m-b} Z_{2^m}, exact b=1 unit survival on the half-period target K_0=8, and odd-frequency leakage P(1|1) = 0.4106 at b=1.",
        },
        "banded_qft_audits": audits,
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

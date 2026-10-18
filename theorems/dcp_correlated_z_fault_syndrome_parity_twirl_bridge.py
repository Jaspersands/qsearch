r"""DCP multi-wire correlated Z-fault syndrome-parity Walsh-Hadamard twirl bridge.

Establishes the exact conditional visibility law for h-wire CNOT star compression
under arbitrary (independent or correlated) multi-wire Z-fault distributions p(e)
over e in {0, 1}^h:

1. Exact Global-Parity Walsh-Hadamard Visibility Identity:
   Let rho(theta; p) = sum_{e in {0,1}^h} p(e) (Z^{e_0} tensor ... tensor Z^{e_{h-1}})
   |psi(theta)><psi(theta)| (Z^{e_0} tensor ... tensor Z^{e_{h-1}}) be an h-qubit
   DCP phase packet subject to an arbitrary joint Z-error distribution p(e).
   Because U_{star} conjugates Z^{e_0} tensor ... tensor Z^{e_{h-1}} to
       Z_0^{e_0 xor ... xor e_{h-1}} tensor Z_1^{e_1} tensor ... tensor Z_{h-1}^{e_{h-1}},
   and computational-basis measurement of the h - 1 syndrome wires absorbs all
   diagonal Z_1^{e_1} tensor ... tensor Z_{h-1}^{e_{h-1}} phases, the conditional
   visibility on the retained target wire 0 for EVERY syndrome d in {0, 1}^{h-1}
   equals the global-parity Walsh-Hadamard coefficient hat_p(1^h):
       gamma_{cond}(p) = E_{e ~ p}[(-1)^{e_0 xor ... xor e_{h-1}}] = hat_p(1^h),
   with conditional off-diagonal coherence:
       2 * <0, d | U_{star} rho(theta; p) U_{star}^dagger | 1, d>
           = 2^{-(h - 1)} * hat_p(1^h) * exp(-i * theta_{eff}(d)).

2. Scoped Consequences — Even-Weight Noise Immunity vs. Single-Fault Collapse:
   - Independent Dephasing Control: For IID Z-errors with marginal visibility gamma_0,
     hat_p(1^h) = gamma_0^h.
   - Even-Weight Correlated Z-Fault Immunity: For any distribution p(e) supported
     exclusively on even Hamming weights wt(e) == 0 (mod 2) (e.g. uniform over all
     even-weight error strings), every single-wire marginal visibility is zero
     (gamma_{marg, j} = E[(-1)^{e_j}] == 0 for h >= 2), yet the CNOT packet retains
     100% noiseless conditional visibility gamma_{cond}(p) = hat_p(1^h) == 1.0!
   - Weight-1 / Balanced Single-Fault Collapse Counterexample: For a 50/50 mixture
     of the no-error string e = 0^h and a uniform weight-1 error wt(e) == 1 on h >= 2
     wires, every individual wire has high marginal visibility gamma_{marg, j} = 1 - 1/h,
     yet hat_p(1^h) = 0.5*(+1) + 0.5*(-1) == 0.0, completely erasing packet coherence!
"""

from __future__ import annotations

import cmath
import hashlib
import itertools
import json
import math
from typing import Any, Dict, List, Mapping, Sequence, Tuple


THEOREM_ID = "dcp_correlated_z_fault_syndrome_parity_twirl_bridge"
SCHEMA_VERSION = "dcp-correlated-z-fault-syndrome-parity-twirl-bridge-v1"


def walsh_parity_visibility(
    error_dist: Mapping[Tuple[int, ...], float],
    h_wires: int,
) -> float:
    """Compute hat_p(1^h) = sum_{e in {0,1}^h} p(e) (-1)^{wt(e)}."""
    total_mass = sum(error_dist.values())
    if abs(total_mass - 1.0) > 1e-12:
        raise ValueError("error_dist probabilities must sum to 1.0")
    acc = 0.0
    for e_vec, prob in error_dist.items():
        if len(e_vec) != h_wires or any(b not in (0, 1) for b in e_vec) or prob < -1e-15:
            raise ValueError("invalid error vector or negative probability")
        parity = sum(e_vec) & 1
        acc += float(prob) * (-1.0 if parity else 1.0)
    return acc


def single_wire_marginal_visibilities(
    error_dist: Mapping[Tuple[int, ...], float],
    h_wires: int,
) -> List[float]:
    """Compute single-wire marginal visibilities gamma_{marg, j} = E_{e ~ p}[(-1)^{e_j}]."""
    marginals = [0.0] * h_wires
    for e_vec, prob in error_dist.items():
        for j in range(h_wires):
            marginals[j] += float(prob) * (-1.0 if e_vec[j] else 1.0)
    return marginals


def verify_cnot_packet_density_walsh_parity_law(
    thetas: Sequence[float],
    error_dist: Mapping[Tuple[int, ...], float],
) -> Dict[str, Any]:
    """Verify by explicit 2^h x 2^h density-matrix CNOT evolution that every syndrome branch has visibility hat_p(1^h)."""
    h_wires = len(thetas)
    if not 2 <= h_wires <= 6:
        raise ValueError("h_wires must be in [2, 6]")
    hat_p_all_ones = walsh_parity_visibility(error_dist, h_wires)
    marginals = single_wire_marginal_visibilities(error_dist, h_wires)
    product_of_marginals = math.prod(marginals)

    dim = 1 << h_wires
    all_bits = list(itertools.product((0, 1), repeat=h_wires))

    # Precompute attenuation kernel A(x, y) = sum_e p(e) (-1)^{<e, x xor y>}
    atten: List[List[float]] = [[0.0] * dim for _ in range(dim)]
    for idx_x, x_vec in enumerate(all_bits):
        for idx_y, y_vec in enumerate(all_bits):
            acc = 0.0
            for e_vec, prob in error_dist.items():
                dot = sum(e_vec[j] * (x_vec[j] ^ y_vec[j]) for j in range(h_wires)) & 1
                acc += float(prob) * (-1.0 if dot else 1.0)
            atten[idx_x][idx_y] = acc

    # Verify across all 2^{h-1} syndromes d in {0,1}^{h-1}
    num_syndromes = 1 << (h_wires - 1)
    max_branch_coherence_err = 0.0

    for d_vec in itertools.product((0, 1), repeat=h_wires - 1):
        # For u = 0: x^{(0)} = (0, d_1, ..., d_{h-1})
        # For u = 1: x^{(1)} = (1, 1 - d_1, ..., 1 - d_{h-1})
        x0_vec = (0, *d_vec)
        x1_vec = (1, *(1 - b for b in d_vec))
        idx_0 = sum(x0_vec[j] << (h_wires - 1 - j) for j in range(h_wires))
        idx_1 = sum(x1_vec[j] << (h_wires - 1 - j) for j in range(h_wires))

        # Notice x0_vec xor x1_vec == (1, 1, ..., 1) = 1^h for EVERY syndrome d!
        phase_0 = sum(x0_vec[j] * float(thetas[j]) for j in range(h_wires))
        phase_1 = sum(x1_vec[j] * float(thetas[j]) for j in range(h_wires))
        rho_01_explicit = (
            cmath.exp(1j * (phase_0 - phase_1)) * atten[idx_0][idx_1] / float(dim)
        )

        theta_eff = float(thetas[0]) + sum(
            (1 - 2 * d_vec[j - 1]) * float(thetas[j]) for j in range(1, h_wires)
        )
        rho_01_closed_form = (
            hat_p_all_ones * cmath.exp(-1j * theta_eff) / float(dim)
        )
        max_branch_coherence_err = max(
            max_branch_coherence_err, abs(rho_01_explicit - rho_01_closed_form)
        )

    return {
        "h_wires": h_wires,
        "num_syndromes": num_syndromes,
        "walsh_global_parity_visibility": hat_p_all_ones,
        "single_wire_marginal_visibilities": marginals,
        "naive_product_of_marginals": product_of_marginals,
        "max_branch_coherence_error": max_branch_coherence_err,
        "exact_walsh_parity_law_verified": max_branch_coherence_err < 1e-12,
    }


def generate_dcp_correlated_z_fault_syndrome_parity_twirl_certificate() -> Dict[str, Any]:
    """Generate the complete certificate for the correlated Z-fault syndrome-parity twirl bridge."""
    thetas_3 = [0.4, 1.1, 2.3]

    # 1. Independent dephasing control (gamma_0 = 0.8 -> p_err = 0.1 per wire)
    p_err = 0.1
    iid_dist = {
        e: ((p_err) ** sum(e)) * ((1.0 - p_err) ** (3 - sum(e)))
        for e in itertools.product((0, 1), repeat=3)
    }
    iid_control = verify_cnot_packet_density_walsh_parity_law(thetas_3, iid_dist)

    # 2. Constructive even-weight correlated Z-fault immunity: uniform over the 4 even-weight strings in {0,1}^3
    # Every single wire has marginal visibility 0.0, yet packet conditional visibility is 1.0!
    even_wt_dist = {
        e: (0.25 if (sum(e) % 2) == 0 else 0.0)
        for e in itertools.product((0, 1), repeat=3)
    }
    even_weight_immunity_control = verify_cnot_packet_density_walsh_parity_law(
        thetas_3, even_wt_dist
    )

    # 3. Balanced single-fault collapse counterexample: 1/2 prob e=(0,0,0), 1/6 prob each of weight-1 strings
    # Each wire has marginal visibility 2/3, naive product is 8/27, yet packet conditional visibility is 0.0!
    single_fault_collapse_dist = {
        e: (0.5 if sum(e) == 0 else (1.0 / 6.0 if sum(e) == 1 else 0.0))
        for e in itertools.product((0, 1), repeat=3)
    }
    single_fault_collapse_audit = verify_cnot_packet_density_walsh_parity_law(
        thetas_3, single_fault_collapse_dist
    )

    all_passed = (
        iid_control["exact_walsh_parity_law_verified"]
        and abs(iid_control["walsh_global_parity_visibility"] - (0.8 ** 3)) < 1e-12
        and abs(iid_control["walsh_global_parity_visibility"] - iid_control["naive_product_of_marginals"]) < 1e-12
        and even_weight_immunity_control["exact_walsh_parity_law_verified"]
        and abs(even_weight_immunity_control["walsh_global_parity_visibility"] - 1.0) < 1e-12
        and abs(even_weight_immunity_control["naive_product_of_marginals"] - 0.0) < 1e-12
        and single_fault_collapse_audit["exact_walsh_parity_law_verified"]
        and abs(single_fault_collapse_audit["walsh_global_parity_visibility"] - 0.0) < 1e-12
        and abs(single_fault_collapse_audit["naive_product_of_marginals"] - (8.0 / 27.0)) < 1e-12
    )

    payload = {
        "theorem_id": THEOREM_ID,
        "schema_version": SCHEMA_VERSION,
        "proof_status": "LOCAL_DERIVATION_REVIEW_PENDING_NOT_FORMALLY_VERIFIED",
        "scope_constraints": {
            "applies_to": "h-wire CNOT star compression under arbitrary joint Z-fault distributions p(e) on {0,1}^h",
            "does_not_claim": "Noise immunity against odd-weight Z-faults or X/depolarizing faults that flip syndrome bits",
            "controls_included": "Includes IID control (hat_p(1^3) = 0.8^3 = 0.512), constructive even-weight correlated fault immunity (hat_p(1^3) = 1.0 despite zero single-wire marginals), and balanced single-fault collapse counterexample (hat_p(1^3) = 0.0 despite 2/3 single-wire marginals).",
        },
        "iid_dephasing_control": iid_control,
        "even_weight_correlated_fault_immunity_control": even_weight_immunity_control,
        "single_fault_collapse_counterexample": single_fault_collapse_audit,
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

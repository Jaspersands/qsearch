r"""DCP bipartite entanglement entropy across the survivor-syndrome CNOT cut bridge.

Establishes the exact pre-measurement bipartite purity Tr(rho_surv(s)^2) and Renyi-2
entanglement entropy S_2(rho_surv(s)) = -log_2 Tr(rho_surv(s)^2) across the cut
separating the compressed survivor wire u_0 from the (h - 1) syndrome wires y in {0, 1}^{h-1}
after a weight-h CNOT witness tree:

1. Exact Post-CNOT Bipartite State Decomposition:
   For a weight-h CNOT star tree on pure input wires |psi_A(s)> = 2^{-h/2} sum_{x in {0,1}^h} exp(2*pi*i <A x, s>/q) |x>,
   where wire 0 is the control/survivor u_0 = x_0 and wires 1..h-1 are syndrome targets
   y_r = x_0 (+) x_r, tracing out the (h - 1) syndrome wires yields the reduced 2x2
   survivor density matrix:
       rho_surv(s) = 2^{-(h-1)} sum_{y in {0,1}^{h-1}} |phi(y; s)><phi(y; s)|,
   where |phi(y; s)> = (|0> + exp(i * DeltaPhi(y; s)) |1>) / sqrt(2) has conditional
   phase:
       DeltaPhi(y; s) = (2*pi / q) * < A_{., 0} + sum_{r=1}^{h-1} (1 - 2*y_r) A_{., r}, s >.

2. Exact Purity and Product-Factorized Syndrome Coherence Identity:
   Because the off-diagonal entry of rho_surv(s) is:
       (rho_surv(s))_{0, 1} = 0.5 * 2^{-(h-1)} sum_{y in {0,1}^{h-1}} exp(-i * DeltaPhi(y; s))
                            = 0.5 * exp(-2*pi*i <A_{.,0}, s>/q) * prod_{r=1}^{h-1} ( cos(2*pi <A_{.,r}, s>/q) ),
    wait: let's verify that exact product identity!
   Since (1 - 2*y_r) takes values +1 (at y_r = 0) and -1 (at y_r = 1), the average over
   y_r in {0, 1} is:
       0.5 * ( exp(2*pi*i <A_{.,r}, s>/q) + exp(-2*pi*i <A_{.,r}, s>/q) ) = cos(2*pi <A_{.,r}, s> / q)!
   Therefore, the pre-measurement reduced survivor state has exact Bloch coherence length:
       C_surv(s) = prod_{r=1}^{h-1} |cos(2*pi * <A_{., r}, s> / q)|,
   and exact bipartite purity:
       Tr(rho_surv(s)^2) = 0.5 * ( 1 + prod_{r=1}^{h-1} cos^2(2*pi * <A_{., r}, s> / q) )!

3. Exact Separability vs. Maximal Bell Entanglement Criteria:
   - Separable (S_2 = 0, Tr(rho_surv^2) = 1.0) if and only if 2 * <A_{., r}, s> == 0 (mod q)
     for EVERY syndrome wire r in {1, ..., h - 1}.
   - Maximally entangled (S_2 = 1.0 bit, Tr(rho_surv^2) = 0.5) if and only if AT LEAST ONE
     syndrome wire r in {1, ..., h - 1} satisfies 4 * <A_{., r}, s> == q (mod 2*q)
     (i.e. cos(2*pi * <A_{., r}, s> / q) = 0), proving that tracing out unmeasured syndrome
     wires completely dephases the survivor wire whenever any target wire sits at a quarter-period!
"""

from __future__ import annotations

import cmath
import hashlib
import itertools
import json
import math
from typing import Any, Dict, List, Sequence


THEOREM_ID = "dcp_bipartite_entanglement_entropy_syndrome_cut_bridge"
SCHEMA_VERSION = "dcp-bipartite-entanglement-entropy-syndrome-cut-bridge-v1"


def evaluate_bipartite_survivor_syndrome_entanglement(
    q_mod: int,
    col_phases_mod_q: Sequence[int],
) -> Dict[str, Any]:
    """Compare explicit partial trace over 2^{h-1} syndrome states against the closed-form cosine-product purity law."""
    h_weight = len(col_phases_mod_q)
    if h_weight < 2:
        raise ValueError("h_weight must be >= 2")

    num_syn = 1 << (h_weight - 1)
    # Explicit 2x2 reduced density matrix rho_surv by summing over all y in {0,1}^{h-1}:
    rho_00 = 0.0
    rho_11 = 0.0
    rho_01 = 0j

    for y_vec in itertools.product((0, 1), repeat=h_weight - 1):
        # For u_0 = 0, x = (0, y_1, ..., y_{h-1}); for u_0 = 1, x = (1, 1 - y_1, ..., 1 - y_{h-1})
        ph_u0 = sum(y_vec[r - 1] * int(col_phases_mod_q[r]) for r in range(1, h_weight)) % q_mod
        ph_u1 = (int(col_phases_mod_q[0]) + sum((1 - y_vec[r - 1]) * int(col_phases_mod_q[r]) for r in range(1, h_weight))) % q_mod
        amp0 = cmath.exp(2j * math.pi * float(ph_u0) / float(q_mod)) / math.sqrt(2.0)
        amp1 = cmath.exp(2j * math.pi * float(ph_u1) / float(q_mod)) / math.sqrt(2.0)

        rho_00 += (abs(amp0) ** 2) / float(num_syn)
        rho_11 += (abs(amp1) ** 2) / float(num_syn)
        rho_01 += (amp0 * amp1.conjugate()) / float(num_syn)

    purity_explicit = (rho_00 ** 2) + (rho_11 ** 2) + 2.0 * (abs(rho_01) ** 2)

    # Closed-form cosine product law:
    cos_sq_prod = 1.0
    for r in range(1, h_weight):
        c_val = math.cos(2.0 * math.pi * float(col_phases_mod_q[r]) / float(q_mod))
        cos_sq_prod *= (c_val ** 2)
    purity_closed_form = 0.5 * (1.0 + cos_sq_prod)
    s2_entropy_bits = -math.log2(purity_closed_form)

    return {
        "q_mod": q_mod,
        "h_weight": h_weight,
        "col_phases_mod_q": [int(v) for v in col_phases_mod_q],
        "purity_explicit": purity_explicit,
        "purity_closed_form": purity_closed_form,
        "renyi_2_entropy_bits": 0.0 if abs(s2_entropy_bits) < 1e-12 else s2_entropy_bits,
        "bloch_coherence_squared": cos_sq_prod,
        "exact_purity_law_verified": abs(purity_explicit - purity_closed_form) < 1e-12,
    }


def generate_dcp_bipartite_entanglement_entropy_syndrome_cut_certificate() -> Dict[str, Any]:
    """Generate the complete certificate for the bipartite survivor-syndrome entanglement bridge."""
    # 1. Separable half-period case: q = 8, h = 3, phases = [3, 4, 0] -> 2 * 4 == 0 mod 8, purity = 1.0, S_2 = 0.0!
    separable_control = evaluate_bipartite_survivor_syndrome_entanglement(
        q_mod=8, col_phases_mod_q=[3, 4, 0]
    )

    # 2. Maximally entangled quarter-period case: q = 8, h = 3, phases = [1, 2, 3] -> wire 1 has phase 2 = q/4, cos(pi/2) = 0 -> purity = 0.5, S_2 = 1.0 bit!
    maximal_bell_control = evaluate_bipartite_survivor_syndrome_entanglement(
        q_mod=8, col_phases_mod_q=[1, 2, 3]
    )

    # 3. Partial entanglement eighth-period case: q = 8, h = 3, phases = [1, 1, 1] -> cos^2(pi/4) = 0.5 per target wire -> cos_sq_prod = 0.25, purity = 0.625!
    partial_entanglement_audit = evaluate_bipartite_survivor_syndrome_entanglement(
        q_mod=8, col_phases_mod_q=[1, 1, 1]
    )

    all_passed = (
        separable_control["exact_purity_law_verified"]
        and abs(separable_control["purity_closed_form"] - 1.0) < 1e-12
        and maximal_bell_control["exact_purity_law_verified"]
        and abs(maximal_bell_control["purity_closed_form"] - 0.5) < 1e-12
        and abs(maximal_bell_control["renyi_2_entropy_bits"] - 1.0) < 1e-12
        and partial_entanglement_audit["exact_purity_law_verified"]
        and abs(partial_entanglement_audit["purity_closed_form"] - 0.625) < 1e-12
    )

    payload = {
        "theorem_id": THEOREM_ID,
        "schema_version": SCHEMA_VERSION,
        "proof_status": "LOCAL_DERIVATION_REVIEW_PENDING_NOT_FORMALLY_VERIFIED",
        "scope_constraints": {
            "applies_to": "Pre-measurement bipartite purity Tr(rho_surv^2) and Renyi-2 entanglement entropy across the survivor-syndrome CNOT cut",
            "does_not_claim": "Preservation of survivor coherence when syndrome wires are discarded without classical measurement readout",
            "controls_included": "Includes separable control (phases=[3,4,0] mod 8, purity=1.0, S_2=0), maximal Bell entanglement control (phases=[1,2,3] mod 8, purity=0.5, S_2=1.0 bit), and partial entanglement audit (phases=[1,1,1] mod 8, purity=0.625).",
        },
        "separable_control": separable_control,
        "maximal_bell_control": maximal_bell_control,
        "partial_entanglement_audit": partial_entanglement_audit,
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

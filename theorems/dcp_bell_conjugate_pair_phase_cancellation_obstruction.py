"""DCP two-copy Bell-basis / conjugate-pair measurement output law and sign-invariance obstruction.

Establishes for two single-qubit DCP phase states
    rho(a_r, s, gamma_r) = (1/2) * [[1, gamma_r * exp(-i*theta_r)], [gamma_r * exp(i*theta_r), 1]]
with theta_r = 2*pi * <a_r, s> / q (r in {1, 2}):

1. Exact Four-Outcome Bell-Basis Measurement Distribution:
   In the Bell basis |Phi^pm> = (|00> +/- |11>)/sqrt(2), |Psi^pm> = (|01> +/- |10>)/sqrt(2),
   the joint state rho(a_1, s, gamma_1) tensor rho(a_2, s, gamma_2) yields exact outcome probabilities:
       P(Phi^+ | a_1, a_2, s) = (1 / 4) * (1 + gamma_1 * gamma_2 * cos(2*pi * <a_1 + a_2, s> / q)),
       P(Phi^- | a_1, a_2, s) = (1 / 4) * (1 - gamma_1 * gamma_2 * cos(2*pi * <a_1 + a_2, s> / q)),
       P(Psi^+ | a_1, a_2, s) = (1 / 4) * (1 + gamma_1 * gamma_2 * cos(2*pi * <a_1 - a_2, s> / q)),
       P(Psi^- | a_1, a_2, s) = (1 / 4) * (1 - gamma_1 * gamma_2 * cos(2*pi * <a_1 - a_2, s> / q)).

2. Global Sign Invariance & Classical Simulation from Single-Copy Marginals:
   - Because cos(theta_1 +/- theta_2) is an even function of s, all four Bell outcome
     probabilities are strictly invariant under s -> -s mod q.
   - For fixed, header-independent coherences, an ordinary uniform random-header
     X observation (h, b) suffices: choose a uniform anchor a_1 and a fair branch;
     set a_2=h-a_1 for Phi or a_2=a_1-h for Psi. Add independent bit noise to
     reduce source coherence to gamma_1*gamma_2. This reproduces the FULL public
     header/outcome transcript, not just its outcome marginal. No chosen query
     or hidden shift is used by the simulator. It does not simulate observations
     conditioned on two headers supplied in advance, correlated sources, or
     header-dependent coherence. It is not a classical DCP solver.

3. Scoped Constructive Swap-Test / Matched-Header Control:
   When a_1 == a_2 mod q and gamma_1 == gamma_2 == gamma, the Psi^pm outcomes depend only on
   coherence (P(Psi^+) = (1 + gamma^2)/4, P(Psi^-) = (1 - gamma^2)/4), directly estimating
   state purity gamma^2 independently of s, while the Phi^pm outcomes sample the doubled
   header 2*a_1 mod q.
"""

from __future__ import annotations

import cmath
import hashlib
import json
import math
import itertools
import random
from typing import Any, Callable, Dict, List, Sequence


THEOREM_ID = "dcp_bell_conjugate_pair_phase_cancellation_obstruction"
SCHEMA_VERSION = "dcp-bell-conjugate-pair-phase-cancellation-obstruction-v2"


def _header(value: Sequence[int], q: int) -> tuple[int, ...]:
    if isinstance(q, bool) or not isinstance(q, int) or q < 2:
        raise ValueError("q must be an integer >= 2")
    result = tuple(value)
    if not result or any(type(x) is not int or not 0 <= x < q for x in result):
        raise ValueError("headers must be nonempty canonical integer vectors")
    return result


def lift_random_x_observation(
    q: int, h: Sequence[int], bit: int, anchor: Sequence[int], branch: int,
) -> Dict[str, Any]:
    """Public transcript map; bit is an observed, already attenuated X outcome."""
    h, anchor = _header(h, q), _header(anchor, q)
    if len(h) != len(anchor) or type(bit) is not int or bit not in (0, 1):
        raise ValueError("matching dimensions and a binary observed bit required")
    if type(branch) is not int or branch not in (0, 1):
        raise ValueError("branch must be 0 (Phi/sum) or 1 (Psi/difference)")
    a2 = tuple((x - a if branch == 0 else a - x) % q for x, a in zip(h, anchor))
    return {
        "a1": list(anchor), "a2": list(a2),
        "outcome": ("Phi" if branch == 0 else "Psi") + ("_plus" if bit == 0 else "_minus"),
    }


def _attenuation(gamma_source: float, gamma_1: float, gamma_2: float) -> float:
    if any(not math.isfinite(g) or not 0 <= g <= 1 for g in (gamma_source, gamma_1, gamma_2)):
        raise ValueError("coherences must be finite numbers in [0,1]")
    product = gamma_1 * gamma_2
    if product > gamma_source:
        raise ValueError("a classical bit flip cannot increase source coherence")
    return product / gamma_source if gamma_source else 0.0


def simulate_random_header_bell(
    q: int, random_x_sample: Callable[[], tuple[Sequence[int], int]],
    rng: random.Random, *, gamma_source: float, gamma_1: float, gamma_2: float,
) -> Dict[str, Any]:
    """Consume ONE random-header X sample; no secret/evaluator/chosen-header API."""
    ratio = _attenuation(gamma_source, gamma_1, gamma_2)
    h, bit = random_x_sample()
    h = _header(h, q)
    if type(bit) is not int or bit not in (0, 1):
        raise ValueError("source must return a binary observed bit")
    flip = int(rng.random() < (1.0 - ratio) / 2.0)
    anchor = tuple(rng.randrange(q) for _ in h)
    return lift_random_x_observation(q, h, bit ^ flip, anchor, rng.randrange(2))


def verify_random_header_transcript_simulation(
    q: int, s_vec: Sequence[int], gamma_source: float, gamma_1: float, gamma_2: float,
) -> Dict[str, Any]:
    """Finite calibration of the whole joint law against native Bell densities.

    The secret is used ONLY to define the calibration source and reference law,
    never by lift_random_x_observation or simulate_random_header_bell.
    """
    secret = _header(s_vec, q)
    ratio = _attenuation(gamma_source, gamma_1, gamma_2)
    group_size = q ** len(secret)
    if group_size > 64:
        raise ValueError("full transcript calibration is limited to 64 headers")
    headers = list(itertools.product(range(q), repeat=len(secret)))
    joint: Dict[tuple, float] = {}
    for h in headers:
        theta = 2 * math.pi * (sum(a * s for a, s in zip(h, secret)) % q) / q
        for bit in (0, 1):
            source_mass = (1 + (1 - 2 * bit) * gamma_source * math.cos(theta)) / (2 * group_size)
            for anchor in headers:
                for branch in (0, 1):
                    for flip in (0, 1):
                        flip_mass = (1 + (1 - 2 * flip) * ratio) / 2
                        record = lift_random_x_observation(q, h, bit ^ flip, anchor, branch)
                        key = (tuple(record["a1"]), tuple(record["a2"]), record["outcome"])
                        joint[key] = joint.get(key, 0.0) + source_mass * flip_mass / (2 * group_size)
    max_error = 0.0
    for a1 in headers:
        for a2 in headers:
            angles = [2 * math.pi * (sum(a * s for a, s in zip(h, secret)) % q) / q for h in (a1, a2)]
            native = bell_probabilities_explicit_density(*angles, gamma_1, gamma_2)
            for outcome, prob in native.items():
                max_error = max(max_error, abs(joint[(a1, a2, outcome)] - prob / group_size ** 2))
    return {
        "q": q, "secret": list(secret), "gamma_source": gamma_source,
        "gamma_1": gamma_1, "gamma_2": gamma_2,
        "transcripts_compared": 4 * group_size ** 2,
        "max_full_joint_probability_error": max_error,
        "total_simulated_mass": sum(joint.values()),
        "random_x_samples_per_bell_transcript": 1,
        "chosen_header_queries": 0,
        "full_joint_law_verified": max_error < 1e-12 and abs(sum(joint.values()) - 1) < 1e-12,
    }


def fixed_header_countercontrol() -> Dict[str, Any]:
    """Same individual X laws, disjoint Bell laws: synthetic != given headers."""
    first = bell_probabilities_explicit_density(math.pi / 2, math.pi / 2, 1, 1)
    second = bell_probabilities_explicit_density(math.pi / 2, -math.pi / 2, 1, 1)
    return {
        "q": 4, "headers": [[1, 0], [0, 1]], "secrets": [[1, 1], [1, 3]],
        "all_individual_x_bits_are_fair": True,
        "bell_total_variation": 0.5 * sum(abs(first[k] - second[k]) for k in first),
        "does_not_support_simulation_at_given_headers": True,
    }


def bell_probabilities_explicit_density(
    theta_1: float,
    theta_2: float,
    gamma_1: float,
    gamma_2: float,
) -> Dict[str, float]:
    """Compute exact Bell measurement outcome probabilities from explicit 4x4 density matrix inner products."""
    # rho_r in basis {|0>, |1>}: [[0.5, 0.5*gamma_r*e^{-i theta_r}], [0.5*gamma_r*e^{i theta_r}, 0.5]]
    r1 = [
        [0.5 + 0j, 0.5 * gamma_1 * cmath.exp(-1j * theta_1)],
        [0.5 * gamma_1 * cmath.exp(1j * theta_1), 0.5 + 0j],
    ]
    r2 = [
        [0.5 + 0j, 0.5 * gamma_2 * cmath.exp(-1j * theta_2)],
        [0.5 * gamma_2 * cmath.exp(1j * theta_2), 0.5 + 0j],
    ]

    # Tensor product rho_12 in basis {|00>, |01>, |10>, |11>}
    rho12 = [[0j] * 4 for _ in range(4)]
    for i1 in range(2):
        for j1 in range(2):
            for i2 in range(2):
                for j2 in range(2):
                    row = 2 * i1 + i2
                    col = 2 * j1 + j2
                    rho12[row][col] = r1[i1][j1] * r2[i2][j2]

    s2 = 1.0 / math.sqrt(2.0)
    bell_vecs = {
        "Phi_plus": [s2, 0.0, 0.0, s2],
        "Phi_minus": [s2, 0.0, 0.0, -s2],
        "Psi_plus": [0.0, s2, s2, 0.0],
        "Psi_minus": [0.0, s2, -s2, 0.0],
    }

    probs: Dict[str, float] = {}
    for name, vec in bell_vecs.items():
        val = 0j
        for r in range(4):
            for c in range(4):
                val += vec[r] * rho12[r][c] * vec[c]
        probs[name] = val.real
    return probs


def bell_probabilities_closed_form(
    theta_1: float,
    theta_2: float,
    gamma_1: float,
    gamma_2: float,
) -> Dict[str, float]:
    """Closed-form Bell outcome probabilities in terms of theta_1 + theta_2 and theta_1 - theta_2."""
    g12 = gamma_1 * gamma_2
    c_sum = math.cos(theta_1 + theta_2)
    c_diff = math.cos(theta_1 - theta_2)
    return {
        "Phi_plus": 0.25 * (1.0 + g12 * c_sum),
        "Phi_minus": 0.25 * (1.0 - g12 * c_sum),
        "Psi_plus": 0.25 * (1.0 + g12 * c_diff),
        "Psi_minus": 0.25 * (1.0 - g12 * c_diff),
    }


def verify_bell_measurement_law_and_sign_invariance(
    q: int,
    a1: Sequence[int],
    a2: Sequence[int],
    s_vec: Sequence[int],
    gamma_1: float,
    gamma_2: float,
) -> Dict[str, Any]:
    """Verify exact match between 4x4 density matrix Bell probabilities, closed-form law, and s -> -s invariance."""
    n = len(s_vec)
    neg_s = [(-int(x)) % q for x in s_vec]

    theta_1 = 2.0 * math.pi * (sum(int(a1[i]) * int(s_vec[i]) for i in range(n)) % q) / float(q)
    theta_2 = 2.0 * math.pi * (sum(int(a2[i]) * int(s_vec[i]) for i in range(n)) % q) / float(q)

    neg_theta_1 = 2.0 * math.pi * (sum(int(a1[i]) * neg_s[i] for i in range(n)) % q) / float(q)
    neg_theta_2 = 2.0 * math.pi * (sum(int(a2[i]) * neg_s[i] for i in range(n)) % q) / float(q)

    p_exp = bell_probabilities_explicit_density(theta_1, theta_2, gamma_1, gamma_2)
    p_cf = bell_probabilities_closed_form(theta_1, theta_2, gamma_1, gamma_2)
    p_neg = bell_probabilities_explicit_density(neg_theta_1, neg_theta_2, gamma_1, gamma_2)

    max_formula_err = max(abs(p_exp[k] - p_cf[k]) for k in p_exp)
    max_sign_diff = max(abs(p_exp[k] - p_neg[k]) for k in p_exp)

    return {
        "q": q,
        "a1": list(a1),
        "a2": list(a2),
        "s": list(s_vec),
        "gamma_1": gamma_1,
        "gamma_2": gamma_2,
        "explicit_probabilities": p_exp,
        "closed_form_probabilities": p_cf,
        "max_formula_error": max_formula_err,
        "max_sign_inversion_diff": max_sign_diff,
        "exact_law_and_sign_invariance": (
            max_formula_err < 1e-12 and max_sign_diff < 1e-12
        ),
    }


def generate_dcp_bell_conjugate_pair_phase_cancellation_certificate() -> Dict[str, Any]:
    """Generate the complete certificate for the two-copy Bell measurement audit."""
    distinct_header_audit = verify_bell_measurement_law_and_sign_invariance(
        q=8,
        a1=[1, 3],
        a2=[2, 5],
        s_vec=[3, 1],
        gamma_1=0.8,
        gamma_2=0.7,
    )

    # Constructive matched-header swap-test control: a1 == a2 -> Psi_plus = (1 + gamma^2)/4 независимо от s
    matched_header_control_s1 = verify_bell_measurement_law_and_sign_invariance(
        q=8,
        a1=[3, 5],
        a2=[3, 5],
        s_vec=[1, 2],
        gamma_1=0.6,
        gamma_2=0.6,
    )
    matched_header_control_s2 = verify_bell_measurement_law_and_sign_invariance(
        q=8,
        a1=[3, 5],
        a2=[3, 5],
        s_vec=[7, 4],
        gamma_1=0.6,
        gamma_2=0.6,
    )

    expected_psi_plus = 0.25 * (1.0 + 0.6 * 0.6)
    swap_test_secret_independent = (
        abs(matched_header_control_s1["explicit_probabilities"]["Psi_plus"] - expected_psi_plus) < 1e-12
        and abs(matched_header_control_s2["explicit_probabilities"]["Psi_plus"] - expected_psi_plus) < 1e-12
    )

    transcript_controls = [
        verify_random_header_transcript_simulation(4, [1, 3], 0.8, 0.8, 0.7),
        verify_random_header_transcript_simulation(5, [2], 1.0, 0.6, 0.4),
        verify_random_header_transcript_simulation(4, [1], 0.0, 0.0, 1.0),
    ]
    fixed_header_control = fixed_header_countercontrol()

    all_passed = (
        distinct_header_audit["exact_law_and_sign_invariance"]
        and matched_header_control_s1["exact_law_and_sign_invariance"]
        and matched_header_control_s2["exact_law_and_sign_invariance"]
        and swap_test_secret_independent
        and all(c["full_joint_law_verified"] for c in transcript_controls)
        and abs(fixed_header_control["bell_total_variation"] - 1) < 1e-12
    )

    payload = {
        "theorem_id": THEOREM_ID,
        "schema_version": SCHEMA_VERSION,
        "proof_status": "LOCAL_DERIVATION_REVIEW_PENDING_NOT_FORMALLY_VERIFIED",
        "scope_constraints": {
            "applies_to": "Two-copy Bell-basis measurements on single-qubit DCP phase states rho(a_1, s) tensor rho(a_2, s)",
            "does_not_claim": "Inability to estimate state purity gamma^2 on matched headers a_1 == a_2 or doubled-header cosines on Phi^pm",
            "controls_included": "Includes both general distinct-header Bell probabilities and the matched-header swap-test control (a_1 == a_2) where P(Psi^+) = (1 + gamma^2)/4 is secret-independent.",
        },
        "distinct_header_audit": distinct_header_audit,
        "random_header_transcript_simulation": transcript_controls,
        "fixed_header_countercontrol": fixed_header_control,
        "simulation_scope": {
            "input": "IID uniform random-header X observations with fixed known coherence",
            "output": "IID full Bell transcripts with synthetic independent uniform public headers",
            "classical_work": "O(n log q) bit operations up to integer arithmetic and random sampling",
            "excludes": ["prespecified/correlated input headers", "header-dependent coherence", "additional header-correlated side information", "unmeasured retained quantum outputs"],
            "classical_DCP_solver_claimed": False,
        },
        "matched_header_swap_test_controls": {
            "s_1": matched_header_control_s1,
            "s_2": matched_header_control_s2,
            "swap_test_secret_independent": swap_test_secret_independent,
        },
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

"""Clean DCP dyadic prefix-peeling error propagation, character depolarization & verifier bridge.

Certifies:
1. Theorem 1 (Correct-Prefix Phase Reduction & Exact Fiber Uniformity):
   When hat_p_k == s mod 2^k, writing s = hat_p_k + 2^k s^{(k)} and a = tilde_a + 2^{t-k} h_a
   (tilde_a = a mod 2^{t-k}, h_a = floor(a / 2^{t-k})) yields
     omega_{2^t}^{a(s - hat_p_k)} = omega_{2^{t-k}}^{tilde_a s^{(k)}}
   for every h_a in Z_{2^k}, so tilde_a is uniform on Z_{2^{t-k}} with fiber size 2^k
   and conditional state |psi_{tilde_a}(s^{(k)})> of pure visibility 1.
2. Theorem 2 (Incorrect-Prefix Character Depolarization Theorem):
   Whenever hat_p_k != s mod 2^k, delta = (s - hat_p_k) mod 2^t has 2-adic valuation
   v_2(delta) in {0, ..., k-1}, so averaging over unobserved high label bits h_a in Z_{2^k}
   annihilates the off-diagonal coherence identically:
     bar{rho}_{tilde_a}(s, hat_p_k) = I_2 / 2
   for every tilde_a in Z_{2^{t-k}} and all 2^k - 1 wrong prefixes.
3. Theorem 3 (Exact Binomial Majority-Vote Tail & Non-Primitive Verifier Orthogonality):
   For odd R = 2m + 1 invocations at advantage eps in (0, 1/2], exact majority error satisfies
     P_maj(R, eps) = sum_{j=0}^m C(R, j)(1/2+eps)^j(1/2-eps)^{R-j}
                   <= (1 - 4 eps^2)^{R/2} <= exp(-2 R eps^2).
   For any complete candidate c != s mod 2^t of arbitrary 2-adic valuation v_2(s - c) in {0, ..., t-1},
   the X-basis verifier has exact single-shot acceptance P_+(s, c) = 1/2 and L_ver-shot
   false survival 2^{-L_ver}.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import sys
from fractions import Fraction
from pathlib import Path
from typing import Any, Dict, List

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


DEFAULT_CONTRACT_PATH = (
    ROOT
    / "research"
    / "hypotheses"
    / "dcp_prefix_peeling_error_propagation_union_bridge_contract.json"
)
DEFAULT_ARTIFACT_PATH = (
    ROOT
    / "research"
    / "reductions"
    / "dcp_prefix_peeling_error_propagation_union_bridge.json"
)


def two_adic_valuation(x: int, t: int) -> int:
    """Return v_2(x mod 2^t), or t if x == 0 mod 2^t."""
    val = int(x) % (1 << t)
    if val == 0:
        return int(t)
    v = 0
    while (val & 1) == 0:
        val >>= 1
        v += 1
    return int(v)


def adapted_phase_density(a: int, s: int, p_hat: int, q: int) -> np.ndarray:
    """Return 2x2 density matrix of |psi_a(s)> after rotating by -2*pi*a*p_hat/q."""
    num = (int(a) * (int(s) - int(p_hat))) % q
    phase = np.exp(-2j * np.pi * num / q)
    return 0.5 * np.array(
        [[1.0 + 0.0j, phase], [np.conj(phase), 1.0 + 0.0j]], dtype=complex
    )


def exact_majority_error(R: int, eps: Fraction) -> Fraction:
    """Compute exact binomial majority-vote error probability for odd R = 2m + 1."""
    assert R % 2 == 1 and R >= 1
    m = R // 2
    p = Fraction(1, 2) + Fraction(eps)
    q_prob = Fraction(1, 2) - Fraction(eps)
    total = Fraction(0, 1)
    for j in range(m + 1):
        total += Fraction(math.comb(R, j), 1) * (p ** j) * (q_prob ** (R - j))
    return total


def evaluate_instance(instance: Dict[str, Any]) -> Dict[str, Any]:
    """Verify Theorems 1, 2, and 3 on a dyadic prefix-peeling instance."""
    instance_id = str(instance["instance_id"])
    t = int(instance["t"])
    k = int(instance["k"])
    q = 1 << t
    q_res = 1 << (t - k)
    q_pref = 1 << k
    R_maj = int(instance["R_majority"])
    eps_frac = Fraction(instance["epsilon"])
    L_ver = int(instance["L_verifier"])

    I_half = 0.5 * np.eye(2, dtype=complex)

    # Check fiber sizes of truncation a -> a mod 2^{t-k}
    fiber_counts = [0] * q_res
    for a in range(q):
        fiber_counts[a % q_res] += 1
    truncation_uniform = all(c == q_pref for c in fiber_counts)

    # --- Theorem 1 & Theorem 2 across all secrets s in Z_q and all prefix guesses p_hat in Z_{2^k} ---
    max_correct_prefix_state_err = 0.0
    max_wrong_prefix_depolarized_err = 0.0
    correct_prefix_pairs_checked = 0
    wrong_prefix_pairs_checked = 0

    for s in range(q):
        s_true_prefix = s % q_pref
        s_res = s >> k
        for p_hat in range(q_pref):
            is_correct = p_hat == s_true_prefix
            if is_correct:
                correct_prefix_pairs_checked += 1
            else:
                wrong_prefix_pairs_checked += 1

            for a_tilde in range(q_res):
                emp_rho = np.zeros((2, 2), dtype=complex)
                for h_a in range(q_pref):
                    a_full = a_tilde + q_res * h_a
                    emp_rho += adapted_phase_density(a_full, s, p_hat, q)
                emp_rho /= float(q_pref)

                if is_correct:
                    expected_rho = adapted_phase_density(a_tilde, s_res, 0, q_res)
                    err = float(np.max(np.abs(emp_rho - expected_rho)))
                    max_correct_prefix_state_err = max(
                        max_correct_prefix_state_err, err
                    )
                else:
                    err = float(np.max(np.abs(emp_rho - I_half)))
                    max_wrong_prefix_depolarized_err = max(
                        max_wrong_prefix_depolarized_err, err
                    )

    theorem1_passed = bool(
        truncation_uniform
        and correct_prefix_pairs_checked == q
        and max_correct_prefix_state_err <= 1e-12
    )
    theorem2_passed = bool(
        wrong_prefix_pairs_checked == q * (q_pref - 1)
        and max_wrong_prefix_depolarized_err <= 1e-12
    )

    # --- Theorem 3: Binomial Majority Error & X-Basis Verifier Across All 2-Adic Valuations ---
    maj_err_exact = exact_majority_error(R_maj, eps_frac)
    bhattacharyya_bound = float((1.0 - 4.0 * float(eps_frac) ** 2) ** (R_maj / 2.0))
    hoeffding_bound = float(math.exp(-2.0 * R_maj * (float(eps_frac) ** 2)))

    # X-basis verifier across all secrets s and all candidates c in Z_q
    # Group false candidates by 2-adic valuation v_2(s - c) in {0, ..., t-1}
    valuation_counts = {v: 0 for v in range(t)}
    max_verifier_prob_err = 0.0
    true_candidate_checks = 0
    false_candidate_checks = 0

    for s in range(q):
        for c in range(q):
            # Exact rational cosine sum: sum_{a=0}^{q-1} (1 + cos(2*pi*a*(s-c)/q)) / (2*q)
            diff = (s - c) % q
            p_plus_emp = sum(
                0.5 * (1.0 + math.cos(2.0 * math.pi * ((a * diff) % q) / q))
                for a in range(q)
            ) / float(q)
            if diff == 0:
                true_candidate_checks += 1
                max_verifier_prob_err = max(
                    max_verifier_prob_err, abs(p_plus_emp - 1.0)
                )
            else:
                false_candidate_checks += 1
                v2 = two_adic_valuation(diff, t)
                valuation_counts[v2] += 1
                max_verifier_prob_err = max(
                    max_verifier_prob_err, abs(p_plus_emp - 0.5)
                )

    false_survival_exact = Fraction(1, 1 << L_ver)
    theorem3_passed = bool(
        float(maj_err_exact) <= bhattacharyya_bound + 1e-12
        and bhattacharyya_bound <= hoeffding_bound + 1e-12
        and true_candidate_checks == q
        and false_candidate_checks == q * (q - 1)
        and all(valuation_counts[v] > 0 for v in range(t))
        and max_verifier_prob_err <= 1e-12
    )

    return {
        "instance_id": instance_id,
        "t": int(t),
        "k": int(k),
        "q": int(q),
        "q_residual": int(q_res),
        "q_prefix": int(q_pref),
        "R_majority": int(R_maj),
        "epsilon_exact": str(eps_frac),
        "L_verifier": int(L_ver),
        "peeling_channel_audit": {
            "truncation_fiber_multiplicity": int(q_pref),
            "truncation_uniform": bool(truncation_uniform),
            "correct_prefix_pairs_checked": int(correct_prefix_pairs_checked),
            "wrong_prefix_pairs_checked": int(wrong_prefix_pairs_checked),
            "max_correct_prefix_state_error": float(max_correct_prefix_state_err),
            "max_wrong_prefix_depolarized_error": float(
                max_wrong_prefix_depolarized_err
            ),
            "theorem1_passed": bool(theorem1_passed),
            "theorem2_passed": bool(theorem2_passed),
        },
        "majority_and_verifier_audit": {
            "majority_error_exact": str(maj_err_exact),
            "majority_error_float": float(maj_err_exact),
            "bhattacharyya_upper_bound": float(bhattacharyya_bound),
            "hoeffding_upper_bound": float(hoeffding_bound),
            "true_candidate_pairs_checked": int(true_candidate_checks),
            "false_candidate_pairs_checked": int(false_candidate_checks),
            "false_pairs_by_2adic_valuation": {
                str(v): int(c) for v, c in valuation_counts.items()
            },
            "max_verifier_single_shot_prob_error": float(max_verifier_prob_err),
            "false_candidate_L_shot_survival_exact": str(false_survival_exact),
            "theorem3_passed": bool(theorem3_passed),
        },
        "instance_passed": bool(
            theorem1_passed and theorem2_passed and theorem3_passed
        ),
    }


def build_dcp_prefix_peeling_error_propagation_union_bridge_report(
    contract_path: Path = DEFAULT_CONTRACT_PATH,
) -> Dict[str, Any]:
    """Build the full reduction artifact from the locked contract."""
    contract = json.loads(contract_path.read_text(encoding="utf-8"))
    instances = [evaluate_instance(inst) for inst in contract["test_instances"]]

    all_t1 = bool(
        all(inst["peeling_channel_audit"]["theorem1_passed"] for inst in instances)
    )
    all_t2 = bool(
        all(inst["peeling_channel_audit"]["theorem2_passed"] for inst in instances)
    )
    all_t3 = bool(
        all(
            inst["majority_and_verifier_audit"]["theorem3_passed"]
            for inst in instances
        )
    )
    all_passed = bool(all_t1 and all_t2 and all_t3)

    max_corr_err = float(
        max(
            inst["peeling_channel_audit"]["max_correct_prefix_state_error"]
            for inst in instances
        )
    )
    max_wrong_err = float(
        max(
            inst["peeling_channel_audit"]["max_wrong_prefix_depolarized_error"]
            for inst in instances
        )
    )
    max_ver_err = float(
        max(
            inst["majority_and_verifier_audit"]["max_verifier_single_shot_prob_error"]
            for inst in instances
        )
    )

    payload_for_hash = {
        "contract_id": contract["contract_id"],
        "instances": instances,
        "all_passed": all_passed,
    }
    digest = hashlib.sha256(
        json.dumps(payload_for_hash, sort_keys=True).encode("utf-8")
    ).hexdigest()

    return {
        "schema_version": "1.0",
        "subsystem": "dcp_prefix_peeling_error_propagation_union_bridge",
        "contract_id": str(contract["contract_id"]),
        "title": str(contract["title"]),
        "family": str(contract["family"]),
        "note_path": "research/DCP_PREFIX_PEELING_ERROR_PROPAGATION_UNION_BRIDGE.md",
        "contract_path": "research/hypotheses/dcp_prefix_peeling_error_propagation_union_bridge_contract.json",
        "summary": {
            "num_instances": int(len(instances)),
            "theorem1_correct_prefix_reduction_passed": bool(all_t1),
            "theorem2_wrong_prefix_depolarization_passed": bool(all_t2),
            "theorem3_majority_and_verifier_passed": bool(all_t3),
            "all_theorems_passed": bool(all_passed),
            "max_correct_prefix_state_error": float(max_corr_err),
            "max_wrong_prefix_depolarized_error": float(max_wrong_err),
            "max_verifier_single_shot_prob_error": float(max_ver_err),
        },
        "instances": instances,
        "honesty_guardrails": {
            "accepted_speedup_candidate": False,
            "new_active_negative_result_created": False,
            "novelty_claim": False,
        },
        "sha256": str(digest),
    }


def write_dcp_prefix_peeling_error_propagation_union_bridge_report(
    artifact_path: Path = DEFAULT_ARTIFACT_PATH,
    contract_path: Path = DEFAULT_CONTRACT_PATH,
) -> Dict[str, Any]:
    """Generate and write the JSON reduction artifact to disk."""
    report = build_dcp_prefix_peeling_error_propagation_union_bridge_report(
        contract_path=contract_path
    )
    artifact_path.parent.mkdir(parents=True, exist_ok=True)
    artifact_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    return report


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Run the clean DCP dyadic prefix-peeling error propagation and depolarization audit."
    )
    parser.add_argument(
        "--write",
        action="store_true",
        help="Write the reduction JSON artifact to research/reductions/.",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Print the full report as JSON to stdout.",
    )
    args = parser.parse_args()

    if args.write:
        report = write_dcp_prefix_peeling_error_propagation_union_bridge_report()
    else:
        report = build_dcp_prefix_peeling_error_propagation_union_bridge_report()

    if args.json:
        print(json.dumps(report, indent=2))
    else:
        s = report["summary"]
        print(
            f"[dcp_prefix_peeling_error_propagation_union_bridge] "
            f"instances={s['num_instances']} "
            f"all_passed={s['all_theorems_passed']} "
            f"max_corr_err={s['max_correct_prefix_state_error']:.3e} "
            f"max_wrong_err={s['max_wrong_prefix_depolarized_error']:.3e} "
            f"sha256={report['sha256'][:16]}"
        )
    return 0 if report["summary"]["all_theorems_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())

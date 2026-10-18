from __future__ import annotations

import argparse
from fractions import Fraction
import hashlib
import json
import math
from pathlib import Path
import sys
from typing import Any

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from theorems.dcp_noisy_tree_merge_error_propagation_audit import (
    fourier_cos_harmonics,
    symmetric_nearest_neighbor_kernel,
)
from theorems.dcp_adaptive_direction_rank_gate import integer
from theorems.dcp_latent_error_access_audit import coincidence_access_receipt


SCHEMA_VERSION = "2026-10-16.conditional-classical-coincidence-identities.v2"
DEFAULT_CONTRACT_PATH = (
    ROOT
    / "research"
    / "hypotheses"
    / "dcp_interleaved_tree_merge_syndrome_pruning_audit_contract.json"
)
DEFAULT_ARTIFACT_PATH = (
    ROOT
    / "research"
    / "phase_workbench"
    / "dcp_interleaved_tree_merge_syndrome_pruning_audit.json"
)
DEFAULT_DOC_PATH = (
    ROOT / "research" / "DCP_INTERLEAVED_TREE_MERGE_SYNDROME_PRUNING_AUDIT.md"
)


def canonical_sha256(payload: dict[str, Any]) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _frac_str(val: Fraction) -> str:
    return f"{val.numerator}/{val.denominator}"


def load_contract(path: Path = DEFAULT_CONTRACT_PATH) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def evaluate_syndrome_pruning_case(
    *,
    case_id: str,
    q: int,
    p_err_num: int,
    p_err_den: int,
    max_depth: int,
    tolerance: float = 1e-12,
) -> dict[str, Any]:
    """Classical latent-error posterior identities, NOT a phase-qubit filter."""
    integer(q,"noise modulus",3,65536)
    integer(max_depth,"bounded conditional depth",1,8)
    integer(p_err_den,"positive probability denominator",1)
    integer(p_err_num,"probability numerator",0,p_err_den)
    p_frac = Fraction(p_err_num, p_err_den)
    p_float = float(p_frac)
    base_kernel = symmetric_nearest_neighbor_kernel(q, p_float)
    cos_val = math.cos(2.0 * math.pi / float(q))

    # Exact rational weights of base_kernel: K(0) = 1-p, K(1) = p/2, K(q-1) = p/2
    k0_frac = Fraction(1, 1) - p_frac
    k1_frac = p_frac / Fraction(2, 1)

    # Baseline visibility lambda_1(p)
    lambda_1_base = float(fourier_cos_harmonics(base_kernel)[1])
    exact_cos = {3:Fraction(-1,2),4:Fraction(0),6:Fraction(1,2)}.get(q)
    exact_base = k0_frac + 2*k1_frac*exact_cos if exact_cos is not None else None
    if exact_base is not None:
        lambda_1_base = float(exact_base)

    # Theorem 1: Single-step coincidence acceptance P_acc^{(1)}(p) = (1-p)^2 + p^2 / 2
    p_acc_1_exact = (k0_frac ** 2) + Fraction(2, 1) * (k1_frac ** 2)
    p_acc_1_formula = Fraction(1, 1) - Fraction(2, 1) * p_frac + Fraction(3, 2) * (p_frac ** 2)
    k_step_1 = (base_kernel ** 2) / float(np.sum(base_kernel ** 2))
    lambda_1_step_1 = float(fourier_cos_harmonics(k_step_1)[1])
    if exact_cos is not None:
        lambda_1_step_1 = float((k0_frac**2+2*k1_frac**2*exact_cos)/p_acc_1_exact)

    vis_gain_emp = lambda_1_step_1 - lambda_1_base
    vis_gain_formula = (
        p_float
        * (1.0 - p_float)
        * (2.0 - 3.0 * p_float)
        * (1.0 - cos_val)
        / (2.0 * float(p_acc_1_exact))
    )
    vis_gain_residual = abs(vis_gain_emp - vis_gain_formula)

    if p_frac in (0,1):
        expected_regime = "ENDPOINT_NEUTRAL"
        regime_holds = abs(vis_gain_emp) <= tolerance
    elif p_frac < Fraction(2, 3):
        expected_regime = "PURIFYING"
        regime_holds = vis_gain_formula >= 0 and vis_gain_residual <= tolerance
    elif p_frac == Fraction(2, 3):
        expected_regime = "CRITICAL_NEUTRAL"
        regime_holds = abs(vis_gain_emp) <= tolerance
    else:
        expected_regime = "DEGRADING"
        regime_holds = vis_gain_formula <= 0 and vis_gain_residual <= tolerance

    theorem1_verified = (
        p_acc_1_exact == p_acc_1_formula
        and vis_gain_residual <= tolerance
        and regime_holds
    )

    # Theorem 2 & Theorem 3 across depths L = 1, ..., max_depth
    depth_rows = []
    cur_dist = base_kernel.copy()
    cur_k0_frac = k0_frac
    cur_k1_frac = k1_frac

    max_telescoping_residual = 0.0
    max_dist_formula_residual = 0.0
    theorem2_exact_match = True
    theorem3_bound_holds = True

    for L in range(1, max_depth + 1):
        K_leaves = 2 ** L
        # Layer L conditional coincidence probability on current rational distribution
        layer_acc_exact = (cur_k0_frac ** 2) + Fraction(2, 1) * (cur_k1_frac ** 2)
        # Wait: at layer ell in {1, ..., L}, in a depth-L tree, layer 1 (leaves) has 2^{L-1} nodes,
        # layer 2 has 2^{L-2} nodes, ..., layer L (root) has 2^0 = 1 node!
        # Let's compute the exact product prod_{ell=1}^L (P_acc^{(ell)})^{2^{L-ell}}!
        cur_k0_frac = (cur_k0_frac ** 2) / layer_acc_exact
        cur_k1_frac = (cur_k1_frac ** 2) / layer_acc_exact

        # Step-by-step float distribution update
        step_sq = cur_dist ** 2
        cur_dist = step_sq / float(np.sum(step_sq))

        # Direct 2^L-power closed form
        closed_k0_frac = k0_frac ** K_leaves
        closed_k1_frac = k1_frac ** K_leaves
        moment_sum_exact = closed_k0_frac + Fraction(2, 1) * closed_k1_frac

        # Compute prod_{ell=1}^L (P_acc^{(ell)})^{2^{L-ell}} explicitly across ell = 1..L
        telescoping_prod_exact = Fraction(1, 1)
        tmp_k0 = k0_frac
        tmp_k1 = k1_frac
        for ell in range(1, L + 1):
            p_acc_ell = (tmp_k0 ** 2) + Fraction(2, 1) * (tmp_k1 ** 2)
            num_nodes_at_layer_ell = 2 ** (L - ell)
            telescoping_prod_exact *= (p_acc_ell ** num_nodes_at_layer_ell)
            tmp_k0 = (tmp_k0 ** 2) / p_acc_ell
            tmp_k1 = (tmp_k1 ** 2) / p_acc_ell

        if telescoping_prod_exact != moment_sum_exact:
            theorem2_exact_match = False
        if cur_k0_frac != (closed_k0_frac / moment_sum_exact):
            theorem2_exact_match = False

        # Compare float recursive cur_dist against closed-form K_eta^{2^L} / S_{2^L}
        closed_dist = (base_kernel ** K_leaves) / float(np.sum(base_kernel ** K_leaves))
        dist_res = float(np.max(np.abs(cur_dist - closed_dist)))
        max_dist_formula_residual = max(max_dist_formula_residual, dist_res)

        tel_res = abs(float(telescoping_prod_exact) - float(np.sum(base_kernel ** K_leaves)))
        max_telescoping_residual = max(max_telescoping_residual, tel_res)

        cond_root_vis = float(fourier_cos_harmonics(cur_dist)[1])
        if exact_cos is not None:
            cond_root_vis = float(cur_k0_frac+2*cur_k1_frac*exact_cos)
        surv_prob_float = float(moment_sum_exact)
        throughput_snr_pruned = surv_prob_float * (cond_root_vis ** 2)
        classical_leaf_snr = float(K_leaves) * (lambda_1_base ** 2)

        if not (throughput_snr_pruned <= surv_prob_float + tolerance <= 1+tolerance):
            theorem3_bound_holds = False
        exact_zero_tie = exact_base == 0 and exact_cos is not None
        comparison = ("EXACT_ZERO_TIE" if exact_zero_tie else
                      "STRICT_NUMERIC_LEAF_DOMINANCE" if classical_leaf_snr-throughput_snr_pruned > tolerance else
                      "TIE_OR_NUMERICALLY_UNRESOLVED" if abs(classical_leaf_snr-throughput_snr_pruned) <= tolerance else
                      "NUMERIC_PRUNED_PROXY_LARGER")

        depth_rows.append(
            {
                "depth_L": L,
                "k_leaves": K_leaves,
                "telescoping_product_survival_exact": _frac_str(telescoping_prod_exact),
                "moment_sum_survival_exact": _frac_str(moment_sum_exact),
                "survival_probability_float": surv_prob_float,
                "conditional_root_visibility": cond_root_vis,
                "throughput_adjusted_pruned_snr": throughput_snr_pruned,
                "classical_k_leaf_snr": classical_leaf_snr,
                "pruned_to_leaf_snr_ratio": throughput_snr_pruned / classical_leaf_snr if classical_leaf_snr else None,
                "direct_leaf_comparison": comparison,
                "recursive_vs_closed_dist_residual": dist_res,
            }
        )

    theorem2_verified = (
        theorem2_exact_match
        and max_telescoping_residual <= tolerance
        and max_dist_formula_residual <= tolerance
    )

    return {
        "case_id": case_id,
        "q": q,
        "analysis_model": "CONDITIONAL_CLASSICAL_LATENT_ERROR_RETAIN_ONE_LEAF",
        "physical_equality_instrument_supplied": False,
        "CNOT_sum_merge_error_law_claimed": False,
        "source_access_receipt": coincidence_access_receipt("phase-qubits-only",3 if 0<p_frac<1 else 1 if p_frac==0 else 2),
        "direct_leaf_dominance_is_a_universal_theorem": False,
        "strict_direct_leaf_dominance_in_this_finite_case": all(row["direct_leaf_comparison"]=="STRICT_NUMERIC_LEAF_DOMINANCE" for row in depth_rows),
        "p_err_exact": _frac_str(p_frac),
        "p_err_float": p_float,
        "expected_purification_regime": expected_regime,
        "baseline_lambda_1": lambda_1_base,
        "step1_acceptance_exact": _frac_str(p_acc_1_exact),
        "step1_acceptance_float": float(p_acc_1_exact),
        "step1_lambda_1": lambda_1_step_1,
        "step1_visibility_gain": vis_gain_emp,
        "step1_visibility_gain_formula_residual": vis_gain_residual,
        "max_telescoping_residual": max_telescoping_residual,
        "max_dist_formula_residual": max_dist_formula_residual,
        "depth_rows": depth_rows,
        "theorem1_verified": theorem1_verified,
        "theorem2_verified": theorem2_verified,
        "theorem3_verified": theorem3_bound_holds,
        "all_theorems_verified": (
            theorem1_verified and theorem2_verified and theorem3_bound_holds
        ),
    }


def build_dcp_interleaved_tree_merge_syndrome_pruning_audit(
    contract_path: Path = DEFAULT_CONTRACT_PATH,
) -> dict[str, Any]:
    contract = load_contract(contract_path)

    case_specs = [
        {
            "case_id": "q8_purifying_regime_p_1_over_4",
            "q": 8,
            "p_err_num": 1,
            "p_err_den": 4,
            "max_depth": 4,
        },
        {
            "case_id": "q8_purifying_regime_p_1_over_2",
            "q": 8,
            "p_err_num": 1,
            "p_err_den": 2,
            "max_depth": 4,
        },
        {
            "case_id": "q8_critical_crossover_p_2_over_3",
            "q": 8,
            "p_err_num": 2,
            "p_err_den": 3,
            "max_depth": 4,
        },
        {
            "case_id": "q8_degrading_regime_p_3_over_4",
            "q": 8,
            "p_err_num": 3,
            "p_err_den": 4,
            "max_depth": 4,
        },
        {
            "case_id": "q16_purifying_regime_p_1_over_3",
            "q": 16,
            "p_err_num": 1,
            "p_err_den": 3,
            "max_depth": 4,
        },
        {"case_id":"q3_exact_zero_visibility_tie","q":3,"p_err_num":2,"p_err_den":3,"max_depth":4},
        {"case_id":"q8_endpoint_p_zero","q":8,"p_err_num":0,"p_err_den":1,"max_depth":4},
        {"case_id":"q8_endpoint_p_one","q":8,"p_err_num":1,"p_err_den":1,"max_depth":4},
    ]

    cases = [evaluate_syndrome_pruning_case(**spec) for spec in case_specs]
    all_verified = all(c["all_theorems_verified"] for c in cases)

    summary = {
        "case_count": len(cases),
        "all_cases_verified": all_verified,
        "critical_purification_threshold_exact": "2/3",
        "max_telescoping_residual": max(c["max_telescoping_residual"] for c in cases),
        "max_dist_formula_residual": max(c["max_dist_formula_residual"] for c in cases),
        "scientific_verdict": (
            "Conditional CLASSICAL latent-error equality identities only. No physical equality "
            "instrument is supplied on phase qubits, and retaining an original error e is not "
            "a CNOT sum error law. The posterior-power telescoping identity and SNR_proxy<=survival<=1 "
            "are retained. Direct-leaf comparisons are finite diagnostics, not a universal dominance "
            "theorem; q3,p2/3 is an exact zero tie, and p0/p1 have neutral gain."
        ),
    }

    payload_without_digest = {
        "schema_version": SCHEMA_VERSION,
        "contract_id": contract["contract_id"],
        "title": contract["title"],
        "status": (
            "CONDITIONAL_CLASSICAL_IDENTITIES_PHYSICAL_ACCESS_NOT_SUPPLIED"
            if all_verified
            else "FAILED"
        ),
        "contract_path": str(contract_path.relative_to(ROOT)),
        "doc_path": str(DEFAULT_DOC_PATH.relative_to(ROOT)),
        "guardrails": contract["guardrails"],
        "theorems": contract["theorems"],
        "summary": summary,
        "cases": cases,
    }
    digest = canonical_sha256(payload_without_digest)
    return {
        **payload_without_digest,
        "certificate_sha256": digest,
    }


def write_dcp_interleaved_tree_merge_syndrome_pruning_audit(
    output_path: Path = DEFAULT_ARTIFACT_PATH,
    contract_path: Path = DEFAULT_CONTRACT_PATH,
) -> dict[str, Any]:
    payload = build_dcp_interleaved_tree_merge_syndrome_pruning_audit(
        contract_path=contract_path
    )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return payload


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Build or write the DCP interleaved tree-merge syndrome-pruning audit."
    )
    parser.add_argument("--write", action="store_true", help="Write artifact JSON to disk.")
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_ARTIFACT_PATH,
        help="Output artifact path.",
    )
    args = parser.parse_args()

    if args.write:
        payload = write_dcp_interleaved_tree_merge_syndrome_pruning_audit(
            output_path=args.output
        )
    else:
        payload = build_dcp_interleaved_tree_merge_syndrome_pruning_audit()

    print(
        json.dumps(
            {
                "status": payload["status"],
                "case_count": payload["summary"]["case_count"],
                "all_cases_verified": payload["summary"]["all_cases_verified"],
                "certificate_sha256": payload["certificate_sha256"],
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0 if payload["summary"]["all_cases_verified"] else 1


if __name__ == "__main__":
    raise SystemExit(main())

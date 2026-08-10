"""No-go theorem for pairwise reciprocal-carrier magnitude arguments.

Let ``m=d^2``.  Take the standard basis ``e_x`` and Fourier basis ``f_y`` of
``C^m`` as two child leaf families.  Then

    |<e_x,f_y>| = 1/sqrt(m) = 1/d                      (1)

for every crossing pair, and distinct one-dimensional leaves have no common
range.  Nevertheless both child spans equal ``C^m``.  Their cross-dependency
quotient has dimension ``m`` and residual principal correlation one.

Thus pairwise noncommon correlations bounded by ``1/d`` do not imply pair
generation once a child contains ``d^2`` leaves.  Setting ``d=n-1`` matches
the exact symmetric-group noncommon bound at only quadratic width.  Any
all-depth wreath proof must use the signed/Racah structure of its cross Gram,
not reciprocal magnitudes alone.

This is an abstract subspace counterfamily.  It is not claimed to occur with
positive mass in the natural wreath portfolio.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import numpy as np

from research_registry import utc_now
from self_dual_wreath_pair_quotient_overlap import audit_pair_quotient_overlap


REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_reciprocal_carrier_accumulation_no_go.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-RECIPROCAL-CARRIER-ACCUMULATION-NO-GO"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


@dataclass(frozen=True)
class ReciprocalCarrierAccumulationControl:
    carrier_dimension_parameter: int
    child_width: int
    physical_dimension: int
    crossing_pair_count: int
    maximum_cross_correlation_magnitude_residual: float
    exact_cross_correlation_magnitude: float
    crossing_pair_common_dimension: int
    left_child_span_dimension: int
    right_child_span_dimension: int
    child_span_intersection_dimension: int
    augmented_h0_dimension: int
    exact_residual_principal_correlation: float
    absolute_weight_cross_norm: float
    local_reciprocal_bound_satisfied: bool
    emergent_dependency_despite_reciprocal_bound: bool
    exact_accumulation_no_go_audit: bool
    status: str


@dataclass(frozen=True)
class ReciprocalCarrierAccumulationReport:
    created_at: str
    theorem_contract: dict[str, Any]
    finite_controls: list[ReciprocalCarrierAccumulationControl]
    scaling_records: list[dict[str, Any]]
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def reciprocal_carrier_accumulation_control(
    carrier_dimension: int,
    *,
    tolerance: float = 1e-8,
) -> ReciprocalCarrierAccumulationControl:
    if carrier_dimension < 2:
        raise ValueError("carrier dimension must be at least two")
    child_width = carrier_dimension**2
    identity = np.eye(child_width, dtype=complex)
    indices = np.arange(child_width)
    fourier = np.exp(
        2j * np.pi * np.outer(indices, indices) / child_width
    ) / math.sqrt(child_width)
    fibers = tuple(identity[:, index : index + 1] for index in indices) + tuple(
        fourier[:, index : index + 1] for index in indices
    )
    projectors = tuple(fiber @ fiber.conj().T for fiber in fibers)
    left = tuple(range(child_width))
    right = tuple(range(child_width, 2 * child_width))
    quotient = audit_pair_quotient_overlap(
        f"RECIPROCAL-CARRIER-D{carrier_dimension}",
        projectors,
        left,
        right,
        tolerance=tolerance,
    )
    cross = np.abs(identity.conj().T @ fourier)
    correlation = 1 / carrier_dimension
    correlation_residual = float(np.max(np.abs(cross - correlation)))
    synthesis = np.concatenate((identity, fourier), axis=1)
    raw_dependency = synthesis.shape[1] - int(
        np.sum(np.linalg.svd(synthesis, compute_uv=False) > 100 * tolerance)
    )
    absolute_cross_norm = float(np.linalg.norm(cross, ord=2))
    verified = bool(
        quotient.exact_pair_quotient_overlap_audit
        and correlation_residual <= 100 * tolerance
        and quotient.crossing_pair_core_span_dimension == 0
        and quotient.emergent_cross_dependency_dimension == child_width
        and raw_dependency == child_width
        and abs(quotient.exact_residual_principal_correlation - 1) <= 100 * tolerance
        and abs(absolute_cross_norm - carrier_dimension) <= 100 * tolerance
    )
    return ReciprocalCarrierAccumulationControl(
        carrier_dimension_parameter=carrier_dimension,
        child_width=child_width,
        physical_dimension=child_width,
        crossing_pair_count=child_width**2,
        maximum_cross_correlation_magnitude_residual=correlation_residual,
        exact_cross_correlation_magnitude=correlation,
        crossing_pair_common_dimension=quotient.crossing_pair_core_span_dimension,
        left_child_span_dimension=quotient.left_span_dimension,
        right_child_span_dimension=quotient.right_span_dimension,
        child_span_intersection_dimension=quotient.child_intersection_dimension,
        augmented_h0_dimension=raw_dependency,
        exact_residual_principal_correlation=quotient.exact_residual_principal_correlation,
        absolute_weight_cross_norm=absolute_cross_norm,
        local_reciprocal_bound_satisfied=correlation == 1 / carrier_dimension,
        emergent_dependency_despite_reciprocal_bound=(
            quotient.emergent_cross_dependency_dimension == child_width
        ),
        exact_accumulation_no_go_audit=verified,
        status=(
            "exact-reciprocal-carrier-accumulation-no-go"
            if verified
            else "reciprocal-carrier-accumulation-audit-failure"
        ),
    )


def run_reciprocal_carrier_accumulation_no_go(
) -> ReciprocalCarrierAccumulationReport:
    controls = [
        reciprocal_carrier_accumulation_control(d) for d in (2, 3, 4, 5)
    ]
    failures = sum(not control.exact_accumulation_no_go_audit for control in controls)
    scaling = [
        {
            "n": n,
            "minimum_nontrivial_irrep_dimension": n - 1,
            "pair_correlation": 1 / (n - 1),
            "counterfamily_child_width": (n - 1) ** 2,
            "counterfamily_augmented_h0_dimension": (n - 1) ** 2,
            "absolute_weight_cross_norm": n - 1,
            "natural_wreath_realization_proved": False,
            "status": "magnitude-only-proof-falsified-natural-realization-open",
        }
        for n in (5, 8, 16, 32, 64, 128, 256, 512)
    ]
    metrics: dict[str, int | float] = {
        "reciprocal_carrier_accumulation_no_go_theorem_count": int(failures == 0),
        "finite_control_count": len(controls),
        "finite_audit_failure_count": failures,
        "maximum_tested_carrier_dimension": max(
            control.carrier_dimension_parameter for control in controls
        ),
        "maximum_tested_child_width": max(control.child_width for control in controls),
        "maximum_tested_emergent_h0_dimension": max(
            control.augmented_h0_dimension for control in controls
        ),
        "quadratic_width_reciprocal_bound_counterexample_count": len(controls) - failures,
        "natural_wreath_counterfamily_count": 0,
        "new_quantum_algorithm_count": 0,
    }
    return ReciprocalCarrierAccumulationReport(
        created_at=utc_now(),
        theorem_contract={
            "construction": "The two children are the standard and Fourier bases of C^(d^2).",
            "pair_angles": "Every crossing principal correlation is exactly 1/d and every crossing pair intersection is zero.",
            "global_dependency": "Both child spans are the full d^2-dimensional carrier, so the cross H0 quotient has dimension d^2.",
            "width_boundary": "The failure occurs at child width d^2, polynomial in the reciprocal carrier dimension.",
            "scope": "This falsifies magnitude-only arguments; realization by natural wreath recoupling blocks is not asserted.",
        },
        finite_controls=controls,
        scaling_records=scaling,
        proof_obligations=[
            {
                "obligation": "reciprocal_magnitude_accumulation_no_go",
                "resolved": failures == 0,
                "resolution": "Mutually unbiased bases give exact 1/d local correlations and maximal emergent H0 at width d^2.",
            },
            {
                "obligation": "exclude_fourier_like_racah_blocks_in_natural_wreath_portfolio",
                "resolved": False,
                "resolution": "A natural all-n theorem must constrain phases or singular structure beyond the known reciprocal magnitudes.",
            },
        ],
        adversarial_audit=[
            {
                "objection": "Pair correlations tending to zero force child spans apart.",
                "resolved": True,
                "resolution": "The correlations are 1/d yet the child spans are identical when width is d^2.",
            },
            {
                "objection": "Exponential width is required to accumulate reciprocal overlaps.",
                "resolved": True,
                "resolution": "Quadratic width suffices, much smaller than the threshold orientation family.",
            },
            {
                "objection": "The abstract family kills the natural wreath route.",
                "resolved": False,
                "resolution": "Natural Racah blocks may obey additional signed structure excluding mutually unbiased accumulation.",
            },
        ],
        headline_metrics=metrics,
        claim_gate={
            "pairwise_reciprocal_magnitude_sufficient_for_pair_generation": False,
            "quadratic_width_accumulation_counterfamily_verified": failures == 0,
            "signed_racah_structure_required": True,
            "natural_wreath_fourier_like_accumulation_excluded": False,
            "uniform_all_n_pair_quotient_gap_proved": False,
            "speedup_claim_allowed": False,
            "reason": "The local 1/d theorem is asymptotically insufficient by itself; only additional natural recoupling structure can rescue the quotient gap.",
        },
        status="reciprocal-magnitude-proof-killed-signed-racah-structure-required",
        summary=(
            "Constructed a quadratic-width family with exact 1/d pair "
            "correlations, no pair cores, and maximal emergent dependency."
        ),
        falsifiers_triggered=[
            "The inverse-irrep-dimension pair-angle bound cannot by itself prove all-depth pair generation.",
            "Polynomial width is enough for small pair correlations to accumulate to a norm-one cross block.",
            "Any surviving proof must exploit signed Fourier/Racah structure specific to natural wreath sectors.",
        ],
    )


def write_reciprocal_carrier_accumulation_no_go_report(
    path: Path = REPORT_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = (
        "EXP-CODE-SELF-DUAL-WREATH-RECIPROCAL-CARRIER-ACCUMULATION-NO-GO"
    ),
    registry_candidate_id: str = "CODE-COSET-COLLECTIVE",
    registry_result_id: str = "",
) -> dict[str, Any]:
    payload = asdict(run_reciprocal_carrier_accumulation_no_go())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True))

    if write_registry:
        _res_payload = report if "report" in locals() else (payload if "payload" in locals() else result)
        from research_registry import (
            ExperimentResultRecord,
            NegativeResultRecord,
            upsert_experiment_result,
            upsert_negative_result,
        )

        upsert_negative_result(
            NegativeResultRecord(
                id="NEG-SELF-DUAL-WREATH-RECIPROCAL-CARRIER-ACCUMULATION-NO-GO",
                source=registry_experiment_id,
                claim=(
                    "Initial negative claim for EXP-CODE-SELF-DUAL-WREATH-RECIPROCAL-CARRIER-ACCUMULATION-NO-GO."
                ),
                reason_invalid=(
                    "Falsified or refined by exact theorem evaluation."
                ),
                lesson=(
                    "Lesson from exact theorem analysis for EXP-CODE-SELF-DUAL-WREATH-RECIPROCAL-CARRIER-ACCUMULATION-NO-GO."
                ),
                applies_to=[
                    registry_candidate_id,
                    registry_experiment_id,
                    "PO-MEASUREMENT",
                ],
                evidence=_res_payload.get("headline_metrics", {}),
            )
        )
        upsert_experiment_result(
            ExperimentResultRecord(
                id=(
                    registry_result_id
                    or f"RESULT-{registry_experiment_id}-LATEST"
                ),
                experiment_id=registry_experiment_id,
                candidate_id=registry_candidate_id,
                created_at=_res_payload.get("created_at", ""),
                status=_res_payload.get("status", "completed"),
                summary=_res_payload.get("summary", ""),
                metrics=_res_payload.get("headline_metrics", {}),
                falsifiers_triggered=_res_payload.get("falsifiers_triggered", []),
                artifacts={
                    "self_dual_wreath_reciprocal_carrier_accumulation_no_go": str(path)
                },
            )
        )
    return payload


if __name__ == "__main__":
    report = write_reciprocal_carrier_accumulation_no_go_report()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))

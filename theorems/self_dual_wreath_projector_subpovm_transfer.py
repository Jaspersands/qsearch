"""Transfer the projector sub-POVM theorem to code-equivalence wreath HSPs.

Rigid code equivalence produces bridge involutions ``h_s`` in

    W_n = (S_n x S_n) semidirect Z_2.

For every unitary irrep and every copy count, ``(I+R(h_s))/2`` is a projector.
Thus the whitening-free covariant projector sub-POVM theorem applies exactly
to the physical wreath hidden-state ensemble.

This transfer is algebraic, not numerical.  The existing global wreath frame
ledger provides exact first and second moments but not the operator norm or
condition at information-threshold copy count.  Those moments alone yield only
a factorially weak conclusive lower bound.  Small finite condition numbers on
selected equal-pair blocks do not establish a natural all-sector bound.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from research_registry import (
    ExperimentResultRecord,
    NegativeResultRecord,
    upsert_experiment_result,
    upsert_negative_result,
    utc_now,
)
from self_dual_wreath_pgm_polar_audit import (
    run_self_dual_wreath_pgm_polar_audit,
)
from self_dual_wreath_physical_frame_blocks import (
    run_self_dual_wreath_physical_frame_blocks,
)


REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_projector_subpovm_transfer.json"
)
WREATH_PGM_PATH = Path(
    "research/representation/self_dual_wreath_pgm_polar_audit.json"
)
PHYSICAL_BLOCK_PATH = Path(
    "research/representation/self_dual_wreath_physical_frame_blocks.json"
)
DEFAULT_EXPERIMENT_ID = "EXP-CODE-SELF-DUAL-WREATH-PROJECTOR-SUBPOVM"
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


@dataclass(frozen=True)
class WreathProjectorSubPOVMScalingRecord:
    n: int
    hidden_label_count_decimal: str
    log2_hidden_label_count: float
    copy_count: int
    projector_rank_fraction: float
    frame_second_moment_scale: float
    moment_only_conclusive_lower_bound: float
    moment_only_conclusive_log2_lower_bound: float
    direct_uniform_projector_conclusive_probability: float
    direct_uniform_projector_conclusive_log2_probability: float
    inverse_polynomial_moment_only_bound: bool
    condition_based_conclusive_formula_available: bool
    natural_global_frame_condition_known: bool
    status: str


@dataclass(frozen=True)
class WreathProjectorSubPOVMTransferReport:
    created_at: str
    theorem_contract: dict[str, object]
    scaling_records: list[WreathProjectorSubPOVMScalingRecord]
    finite_physical_block_evidence: dict[str, int | float | str]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, bool | str]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _read_json(path: Path, fallback: Any) -> Any:
    if not path.exists():
        return fallback
    try:
        return json.loads(path.read_text())
    except (json.JSONDecodeError, OSError):
        return fallback


def moment_only_conclusive_lower_bound(
    hidden_label_count: int,
    copy_count: int,
) -> float:
    """Lower bound q using only ||B||<=1 and exact wreath frame moments."""

    subset_count = 1 << copy_count
    return (subset_count + hidden_label_count - 1) / (
        hidden_label_count * subset_count
    )


def build_wreath_projector_subpovm_transfer_report(
    wreath_pgm_path: Path = WREATH_PGM_PATH,
    physical_block_path: Path = PHYSICAL_BLOCK_PATH,
) -> WreathProjectorSubPOVMTransferReport:
    wreath = _read_json(wreath_pgm_path, {})
    physical = _read_json(physical_block_path, {})
    if not wreath:
        wreath = asdict(run_self_dual_wreath_pgm_polar_audit())
    if not physical:
        physical = asdict(run_self_dual_wreath_physical_frame_blocks())
    scaling: list[WreathProjectorSubPOVMScalingRecord] = []
    for record in wreath.get("records", []):
        labels = int(record["hidden_label_count_decimal"])
        copies = int(record["copy_count"])
        lower = moment_only_conclusive_lower_bound(labels, copies)
        expected_scale = float(record["frame_eigenvalue_second_moment_scale"])
        if abs(lower - expected_scale) > 1e-12:
            raise ArithmeticError("wreath moment lower bound formula mismatch")
        n = int(record["n"])
        scaling.append(
            WreathProjectorSubPOVMScalingRecord(
                n=n,
                hidden_label_count_decimal=str(labels),
                log2_hidden_label_count=float(
                    record["log2_hidden_label_count"]
                ),
                copy_count=copies,
                projector_rank_fraction=float(
                    record["projector_rank_fraction"]
                ),
                frame_second_moment_scale=expected_scale,
                moment_only_conclusive_lower_bound=lower,
                moment_only_conclusive_log2_lower_bound=math.log2(lower),
                direct_uniform_projector_conclusive_probability=lower,
                direct_uniform_projector_conclusive_log2_probability=(
                    math.log2(lower)
                ),
                inverse_polynomial_moment_only_bound=lower >= n**-3,
                condition_based_conclusive_formula_available=True,
                natural_global_frame_condition_known=False,
                status=(
                    "wreath-projector-subpovm-transfer-condition-open"
                ),
            )
        )
    physical_records = physical.get("records", [])
    threshold_blocks = [
        record
        for record in physical_records
        if bool(record.get("reaches_information_threshold"))
        and float(record.get("support_condition_number", 0)) > 0
    ]
    minimum_inverse_condition = min(
        (
            1 / float(record["support_condition_number"])
            for record in threshold_blocks
        ),
        default=0.0,
    )
    maximum_condition = max(
        (
            float(record["support_condition_number"])
            for record in threshold_blocks
        ),
        default=0.0,
    )
    finite_evidence: dict[str, int | float | str] = {
        "selected_information_threshold_block_count": len(threshold_blocks),
        "maximum_selected_support_condition_number": maximum_condition,
        "minimum_selected_inverse_condition_conclusive_floor": (
            minimum_inverse_condition
        ),
        "scope": (
            "Selected finite equal-pair physical blocks only; not the complete "
            "natural wreath source law or global frame."
        ),
    }
    tail = scaling[-1] if scaling else None
    metrics: dict[str, int | float] = {
        "group_general_normalized_projector_theorem_count": 1,
        "wreath_projector_subpovm_transfer_theorem_count": 1,
        "condition_only_conclusive_formula_theorem_count": 1,
        "scaling_record_count": len(scaling),
        "moment_only_inverse_polynomial_row_count": sum(
            record.inverse_polynomial_moment_only_bound for record in scaling
        ),
        "tail_n": tail.n if tail else 0,
        "tail_moment_only_conclusive_log2_lower_bound": (
            tail.moment_only_conclusive_log2_lower_bound if tail else 0.0
        ),
        "direct_uniform_label_projector_dilation_schema_count": 1,
        "tail_direct_uniform_projector_conclusive_log2_probability": (
            tail.direct_uniform_projector_conclusive_log2_probability
            if tail
            else 0.0
        ),
        "structured_maximal_effect_dilation_count": 0,
        "selected_information_threshold_block_count": len(threshold_blocks),
        "maximum_selected_support_condition_number": maximum_condition,
        "minimum_selected_inverse_condition_conclusive_floor": (
            minimum_inverse_condition
        ),
        "natural_all_sector_polynomial_condition_theorem_count": 0,
        "uniform_wreath_covariant_subpovm_circuit_count": 0,
        "compressed_permutation_outcome_transform_count": 0,
        "polynomial_hidden_permutation_decoder_count": 0,
        "classical_code_equivalence_separation_count": 0,
    }
    return WreathProjectorSubPOVMTransferReport(
        created_at=utc_now(),
        theorem_contract={
            "group_general_projector": (
                "For every order-two h and unitary representation R, "
                "P_h=(I+R(h))/2 is an orthogonal projector."
            ),
            "wreath_hidden_state": (
                "The k-copy bridge state is P_s/rank(P_s), with "
                "P_s=((I+R(h_s))/2)^tensor k."
            ),
            "subpovm": (
                "E_s=rho_s/||sum_t rho_t|| plus a failure effect; "
                "q=Tr(F^2)/||F||>=1/kappa(F)."
            ),
            "moment_only_bound": (
                "Using only ||B||<=1 and the exact wreath second moment gives "
                "q >= (2^k+n!-1)/(n! 2^k), which is factorially weak."
            ),
            "direct_dilation": (
                "Uniformly prepare s and apply controlled P_s. Measuring s "
                "implements effects P_s/n! with exact conclusive probability "
                "(2^k+n!-1)/(n!2^k), equal to the recorded moment scale."
            ),
            "maximal_effect_boundary": (
                "The condition-only maximal effects are "
                "P_s/(n!||B||). Reaching them from the direct dilation requires "
                "structured amplification or a different harmonic Naimark "
                "construction; the effect theorem is not that circuit."
            ),
            "transfer_boundary": (
                "Symmetric-group S_5 information and condition numbers do not "
                "transfer numerically. The physical wreath source law and "
                "global frame require their own condition and information "
                "analysis."
            ),
        },
        scaling_records=scaling,
        finite_physical_block_evidence=finite_evidence,
        headline_metrics=metrics,
        claim_gate={
            "projector_subpovm_transfers_to_wreath_exactly": True,
            "symmetric_group_finite_performance_transfers_to_wreath": False,
            "moment_only_bound_is_polynomial_on_tail": False,
            "direct_uniform_projector_dilation_is_polynomially_conclusive_on_tail": False,
            "known_circuit_implements_maximal_condition_normalization": False,
            "natural_all_sector_polynomial_condition_proved": False,
            "uniform_wreath_covariant_subpovm_circuit_proved": False,
            "compressed_permutation_outcome_proved": False,
            "polynomial_hidden_permutation_decoder_proved": False,
            "classical_separation_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The algebraic maximal sub-POVM transfer is exact, but the "
                "direct uniform-label projector dilation has factorially weak "
                "conclusive probability. No structured maximal-scale dilation "
                "is known, and selected finite block conditions do not cover "
                "the natural wreath ensemble."
            ),
        },
        status="wreath-projector-subpovm-transferred-global-condition-open",
        summary=(
            f"Transferred the whitening-free projector sub-POVM theorem to "
            f"{len(scaling)} physical wreath scaling rows. The tail moment-only "
            "conclusive lower bound has log2 "
            f"{metrics['tail_moment_only_conclusive_log2_lower_bound']:.3f}; "
            "a natural all-sector condition theorem and orbit circuit remain "
            "open."
        ),
        falsifiers_triggered=[
            (
                "The normalized-projector and condition-only conclusive "
                "theorems transfer to the bridge wreath HSP exactly."
            ),
            (
                "The finite S_5 information values do not transfer to the "
                "wreath ensemble."
            ),
            (
                "Existing wreath first and second moments alone give only a "
                "factorially weak unconditional conclusive guarantee."
            ),
            (
                "The direct uniform-label controlled-projector dilation "
                "realizes P_s/n!, not the maximal P_s/(n!||B||) effects."
            ),
            (
                "Condition at selected finite equal-pair blocks does not prove "
                "condition under the full natural source law."
            ),
        ],
    )


def write_wreath_projector_subpovm_transfer_report(
    output_path: Path = REPORT_PATH,
    *,
    write_registry: bool = True,
    registry_experiment_id: str = DEFAULT_EXPERIMENT_ID,
    registry_candidate_id: str = DEFAULT_CANDIDATE_ID,
    registry_result_id: str | None = None,
) -> dict[str, object]:
    payload = asdict(build_wreath_projector_subpovm_transfer_report())
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    if write_registry:
        upsert_negative_result(
            NegativeResultRecord(
                id="NEG-CODE-WREATH-SN-SUBPOVM-PERFORMANCE-TRANSFER",
                source=str(output_path),
                claim=(
                    "Finite S_n projector-sub-POVM information and condition "
                    "numbers automatically transfer to code equivalence."
                ),
                reason_invalid=(
                    "Only the normalized-projector and covariant sub-POVM "
                    "identities are group-general. The physical wreath source "
                    "law, global frame condition, outcome transform, and "
                    "decoder are distinct."
                ),
                lesson=(
                    "Use the projector sub-POVM as the physical wreath "
                    "architecture target, but prove its all-sector condition "
                    "and Naimark dilation directly."
                ),
                applies_to=[
                    registry_candidate_id,
                    registry_experiment_id,
                    "PO-REDUCTION",
                    "PO-MEASUREMENT",
                    "PO-SUCCESS",
                ],
                evidence=payload["headline_metrics"],
            )
        )
        result_id = (
            registry_result_id
            or f"RESULT-{registry_experiment_id}-CODE"
        )
        upsert_experiment_result(
            ExperimentResultRecord(
                id=result_id,
                experiment_id=registry_experiment_id,
                candidate_id=registry_candidate_id,
                created_at=str(payload["created_at"]),
                status=str(payload["status"]),
                summary=str(payload["summary"]),
                metrics=dict(payload["headline_metrics"]),
                falsifiers_triggered=list(payload["falsifiers_triggered"]),
                artifacts={
                    "self_dual_wreath_projector_subpovm_transfer": str(
                        output_path
                    )
                },
            )
        )
    return payload


if __name__ == "__main__":
    report = write_wreath_projector_subpovm_transfer_report()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))

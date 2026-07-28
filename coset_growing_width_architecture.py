"""Typed architecture compiler for growing-width coset measurements.

The multiregister lower bound requires more than a polynomial sample count:
``Theta(n log n)`` coset states must participate in one entangled measurement.
This module makes that requirement machine-checkable.

It evaluates three architecture classes:

* a balanced carrier-preserving covariant recoupling network;
* separate strong Fourier measurements with classical postprocessing;
* a bounded-copy Racah-label measurement.

Only the first satisfies the structural no-go constraints.  It is still not
an algorithm because the growing-copy associator synthesis, state-dependent
measurement, compressed covariant outcome, information theorem, decoder, and
classical separation are unproved.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path

from research_registry import (
    ExperimentResultRecord,
    NegativeResultRecord,
    upsert_experiment_result,
    upsert_negative_result,
    utc_now,
)


REPORT_PATH = Path(
    "research/representation/coset_growing_width_architecture.json"
)
DEFAULT_EXPERIMENT_ID = "EXP-COSET-GROWING-WIDTH-ARCHITECTURE"
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


@dataclass(frozen=True)
class ArchitectureScalingRow:
    n: int
    required_joint_register_width: int
    architecture_joint_register_width: int
    merge_count: int
    merge_depth: int
    level_merge_counts: list[int]
    width_lower_bound_satisfied: bool


@dataclass(frozen=True)
class ArchitectureValidationIssue:
    obligation: str
    severity: str
    message: str


@dataclass(frozen=True)
class GrowingWidthArchitectureRecord:
    id: str
    topology: str
    joint_quantum_measurement: bool
    width_formula: str
    carrier_register_policy: str
    intermediate_effect_algebra: str
    final_povm_effect_class: str
    outcome_representation: str
    decoder_contract: str
    natural_source_access: str
    classical_baseline: str
    associator_circuit_proved: bool
    state_dependent_measurement_proved: bool
    compressed_outcome_proved: bool
    information_lower_bound_proved: bool
    decoder_proved: bool
    classical_separation_proved: bool
    scaling_rows: list[ArchitectureScalingRow]
    validation_issues: list[ArchitectureValidationIssue]
    structurally_compliant_with_entanglement_width_gate: bool
    proof_complete: bool
    status: str


@dataclass(frozen=True)
class GrowingWidthArchitectureReport:
    created_at: str
    schema_contract: dict[str, object]
    architectures: list[GrowingWidthArchitectureRecord]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, bool | str]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def required_joint_width(n: int) -> int:
    if n < 2:
        raise ValueError("growing-width architecture requires n at least two")
    return math.ceil(n * math.log2(n))


def balanced_merge_levels(leaf_count: int) -> tuple[int, ...]:
    if leaf_count < 1:
        raise ValueError("leaf count must be positive")
    levels: list[int] = []
    active = leaf_count
    while active > 1:
        merges = active // 2
        levels.append(merges)
        active = merges + active % 2
    if sum(levels) != leaf_count - 1:
        raise ArithmeticError("balanced merge tree must have leaves-1 merges")
    return tuple(levels)


def _scaling_rows(
    *,
    width_mode: str,
    n_values: tuple[int, ...],
) -> list[ArchitectureScalingRow]:
    rows: list[ArchitectureScalingRow] = []
    for n in n_values:
        required = required_joint_width(n)
        if width_mode == "theta-n-log-n":
            width = required
            levels = balanced_merge_levels(width)
        elif width_mode == "separate":
            width = 1
            levels = ()
        elif width_mode == "bounded-three":
            width = 3
            levels = balanced_merge_levels(width)
        else:
            raise ValueError(f"unknown width mode: {width_mode}")
        rows.append(
            ArchitectureScalingRow(
                n=n,
                required_joint_register_width=required,
                architecture_joint_register_width=width,
                merge_count=sum(levels),
                merge_depth=len(levels),
                level_merge_counts=list(levels),
                width_lower_bound_satisfied=width >= required,
            )
        )
    return rows


def _validate_architecture(
    *,
    joint_quantum_measurement: bool,
    carrier_register_policy: str,
    final_povm_effect_class: str,
    outcome_representation: str,
    decoder_contract: str,
    natural_source_access: str,
    classical_baseline: str,
    associator_circuit_proved: bool,
    state_dependent_measurement_proved: bool,
    compressed_outcome_proved: bool,
    information_lower_bound_proved: bool,
    decoder_proved: bool,
    classical_separation_proved: bool,
    scaling_rows: list[ArchitectureScalingRow],
) -> list[ArchitectureValidationIssue]:
    issues: list[ArchitectureValidationIssue] = []
    if not joint_quantum_measurement:
        issues.append(
            ArchitectureValidationIssue(
                obligation="entanglement-width",
                severity="fatal",
                message=(
                    "Registers are measured separately; sample count does not "
                    "satisfy the joint entanglement-width lower bound."
                ),
            )
        )
    if not all(row.width_lower_bound_satisfied for row in scaling_rows):
        issues.append(
            ArchitectureValidationIssue(
                obligation="entanglement-width",
                severity="fatal",
                message="Joint width is below ceil(n log2 n).",
            )
        )
    if carrier_register_policy != "preserve-through-final-covariant-povm":
        issues.append(
            ArchitectureValidationIssue(
                obligation="carrier-information",
                severity="fatal",
                message=(
                    "Carrier registers are discarded before an "
                    "information-bearing covariant POVM."
                ),
            )
        )
    if final_povm_effect_class == "diagonal-action-commutant":
        issues.append(
            ArchitectureValidationIssue(
                obligation="commutant-zero-information",
                severity="fatal",
                message=(
                    "Every final effect is in the diagonal-action commutant "
                    "and therefore has zero hidden-element information."
                ),
            )
        )
    proof_checks = (
        (
            associator_circuit_proved,
            "growing-associator",
            "No uniform polynomial growing-copy associator circuit is proved.",
        ),
        (
            state_dependent_measurement_proved,
            "measurement-synthesis",
            "No state-dependent growing-width POVM implementation is proved.",
        ),
        (
            compressed_outcome_proved,
            "outcome-compression",
            "No polynomial-size covariant outcome representation is proved.",
        ),
        (
            information_lower_bound_proved,
            "information",
            "No inverse-polynomial information or recovery theorem is proved.",
        ),
        (
            decoder_proved,
            "decoder",
            "No polynomial hidden-involution decoder is proved.",
        ),
        (
            classical_separation_proved,
            "dequantization",
            "No separation from legal classical representation baselines is proved.",
        ),
    )
    for passed, obligation, message in proof_checks:
        if not passed:
            issues.append(
                ArchitectureValidationIssue(
                    obligation=obligation,
                    severity="blocking",
                    message=message,
                )
            )
    if "natural" not in natural_source_access.lower():
        issues.append(
            ArchitectureValidationIssue(
                obligation="natural-access",
                severity="fatal",
                message="Source labels are selected or postselected rather than natural.",
            )
        )
    if not outcome_representation:
        issues.append(
            ArchitectureValidationIssue(
                obligation="outcome-compression",
                severity="fatal",
                message="Outcome representation is unspecified.",
            )
        )
    if not decoder_contract:
        issues.append(
            ArchitectureValidationIssue(
                obligation="decoder",
                severity="fatal",
                message="Decoder contract is unspecified.",
            )
        )
    if not classical_baseline:
        issues.append(
            ArchitectureValidationIssue(
                obligation="dequantization",
                severity="fatal",
                message="Classical baseline is unspecified.",
            )
        )
    return issues


def _architecture_record(
    *,
    identifier: str,
    topology: str,
    joint_quantum_measurement: bool,
    width_mode: str,
    width_formula: str,
    carrier_register_policy: str,
    intermediate_effect_algebra: str,
    final_povm_effect_class: str,
    outcome_representation: str,
    decoder_contract: str,
    natural_source_access: str,
    classical_baseline: str,
    associator_circuit_proved: bool = False,
    state_dependent_measurement_proved: bool = False,
    compressed_outcome_proved: bool = False,
    information_lower_bound_proved: bool = False,
    decoder_proved: bool = False,
    classical_separation_proved: bool = False,
    n_values: tuple[int, ...] = (8, 16, 32, 64),
) -> GrowingWidthArchitectureRecord:
    scaling_rows = _scaling_rows(
        width_mode=width_mode,
        n_values=n_values,
    )
    issues = _validate_architecture(
        joint_quantum_measurement=joint_quantum_measurement,
        carrier_register_policy=carrier_register_policy,
        final_povm_effect_class=final_povm_effect_class,
        outcome_representation=outcome_representation,
        decoder_contract=decoder_contract,
        natural_source_access=natural_source_access,
        classical_baseline=classical_baseline,
        associator_circuit_proved=associator_circuit_proved,
        state_dependent_measurement_proved=state_dependent_measurement_proved,
        compressed_outcome_proved=compressed_outcome_proved,
        information_lower_bound_proved=information_lower_bound_proved,
        decoder_proved=decoder_proved,
        classical_separation_proved=classical_separation_proved,
        scaling_rows=scaling_rows,
    )
    fatal = [issue for issue in issues if issue.severity == "fatal"]
    blocking = [issue for issue in issues if issue.severity == "blocking"]
    structurally_compliant = not fatal
    proof_complete = not issues
    return GrowingWidthArchitectureRecord(
        id=identifier,
        topology=topology,
        joint_quantum_measurement=joint_quantum_measurement,
        width_formula=width_formula,
        carrier_register_policy=carrier_register_policy,
        intermediate_effect_algebra=intermediate_effect_algebra,
        final_povm_effect_class=final_povm_effect_class,
        outcome_representation=outcome_representation,
        decoder_contract=decoder_contract,
        natural_source_access=natural_source_access,
        classical_baseline=classical_baseline,
        associator_circuit_proved=associator_circuit_proved,
        state_dependent_measurement_proved=state_dependent_measurement_proved,
        compressed_outcome_proved=compressed_outcome_proved,
        information_lower_bound_proved=information_lower_bound_proved,
        decoder_proved=decoder_proved,
        classical_separation_proved=classical_separation_proved,
        scaling_rows=scaling_rows,
        validation_issues=issues,
        structurally_compliant_with_entanglement_width_gate=(
            structurally_compliant
        ),
        proof_complete=proof_complete,
        status=(
            "structurally-compliant-proof-obligations-open"
            if structurally_compliant and blocking
            else (
                "proof-complete"
                if proof_complete
                else "structurally-rejected"
            )
        ),
    )


def build_growing_width_architecture_report(
) -> GrowingWidthArchitectureReport:
    architectures = [
        _architecture_record(
            identifier="ARCH-BALANCED-CARRIER-COVARIANT",
            topology="balanced binary recoupling tree",
            joint_quantum_measurement=True,
            width_mode="theta-n-log-n",
            width_formula="ceil(n log2 n)",
            carrier_register_policy="preserve-through-final-covariant-povm",
            intermediate_effect_algebra=(
                "diagonal-action commutant routing plus carrier-preserving "
                "associators"
            ),
            final_povm_effect_class="carrier-sensitive-covariant",
            outcome_representation=(
                "proposed polynomial covariant sketch register; theorem missing"
            ),
            decoder_contract=(
                "proposed polynomial map from covariant sketch to hidden "
                "involution; theorem missing"
            ),
            natural_source_access=(
                "all source labels arise from natural coset-state QFT outcomes"
            ),
            classical_baseline=(
                "natural strong Fourier, character/tensor contractions, "
                "and graph/code canonicalization"
            ),
        ),
        _architecture_record(
            identifier="ARCH-SEPARATE-STRONG-FOURIER",
            topology="independent per-register measurement",
            joint_quantum_measurement=False,
            width_mode="separate",
            width_formula="1 joint register despite polynomial samples",
            carrier_register_policy="measure-and-discard-per-register",
            intermediate_effect_algebra="none",
            final_povm_effect_class="product-strong-fourier",
            outcome_representation="classical list of separate outcomes",
            decoder_contract="classical postprocessing of separate outcomes",
            natural_source_access="natural coset-state QFT outcomes",
            classical_baseline="natural strong Fourier information scaling",
        ),
        _architecture_record(
            identifier="ARCH-BOUNDED-RACAH-LABELS",
            topology="fixed three-register Racah control",
            joint_quantum_measurement=True,
            width_mode="bounded-three",
            width_formula="3",
            carrier_register_policy="discard-after-invariant-labels",
            intermediate_effect_algebra="diagonal-action commutant",
            final_povm_effect_class="diagonal-action-commutant",
            outcome_representation="target and multiplicity/Racah labels",
            decoder_contract="unspecified label-to-involution map",
            natural_source_access="selected rather than natural source branch",
            classical_baseline="finite tensor and character contractions",
        ),
    ]
    compliant = [
        architecture
        for architecture in architectures
        if architecture.structurally_compliant_with_entanglement_width_gate
    ]
    metrics: dict[str, int | float] = {
        "architecture_count": len(architectures),
        "structurally_compliant_architecture_count": len(compliant),
        "structurally_rejected_architecture_count": (
            len(architectures) - len(compliant)
        ),
        "proof_complete_architecture_count": sum(
            architecture.proof_complete
            for architecture in architectures
        ),
        "scaling_row_count": sum(
            len(architecture.scaling_rows)
            for architecture in architectures
        ),
        "maximum_compliant_joint_register_width_at_n64": max(
            (
                next(
                    row.architecture_joint_register_width
                    for row in architecture.scaling_rows
                    if row.n == 64
                )
                for architecture in compliant
            ),
            default=0,
        ),
        "minimum_compliant_merge_depth_at_n64": min(
            (
                next(
                    row.merge_depth
                    for row in architecture.scaling_rows
                    if row.n == 64
                )
                for architecture in compliant
            ),
            default=0,
        ),
        "fatal_validation_issue_count": sum(
            issue.severity == "fatal"
            for architecture in architectures
            for issue in architecture.validation_issues
        ),
        "blocking_proof_issue_count": sum(
            issue.severity == "blocking"
            for architecture in architectures
            for issue in architecture.validation_issues
        ),
        "polynomial_growing_associator_circuit_count": 0,
        "compressed_covariant_outcome_count": 0,
        "growing_width_information_theorem_count": 0,
        "growing_width_hidden_involution_decoder_count": 0,
    }
    return GrowingWidthArchitectureReport(
        created_at=utc_now(),
        schema_contract={
            "required_fields": [
                "joint quantum width",
                "topology and merge schedule",
                "carrier preservation",
                "intermediate and final effect algebras",
                "natural source access",
                "compressed outcome representation",
                "decoder",
                "information theorem",
                "classical baseline",
            ],
            "fatal_rejections": [
                "separate measurements",
                "joint width below ceil(n log2 n)",
                "carrier discarded before final covariant POVM",
                "commutant-only final effects",
                "selected/non-natural source access",
            ],
            "proof_blockers": [
                "growing associator circuit",
                "state-dependent measurement synthesis",
                "outcome compression",
                "information lower bound",
                "decoder",
                "classical separation",
            ],
        },
        architectures=architectures,
        headline_metrics=metrics,
        claim_gate={
            "growing_width_structural_skeleton_exists": bool(compliant),
            "separate_measurement_architecture_rejected": True,
            "bounded_commutant_architecture_rejected": True,
            "proof_complete_growing_width_architecture_exists": False,
            "speedup_claim_allowed": False,
            "reason": (
                "A balanced carrier-preserving skeleton satisfies the known "
                "width and symmetry constraints, but every mathematical and "
                "algorithmic component that could create a speedup remains "
                "an explicit proof obligation."
            ),
        },
        status=(
            "growing-width-skeleton-typed-associator-outcome-information-decoder-open"
        ),
        summary=(
            f"Type-checked {len(architectures)} multiregister architectures. "
            f"{len(compliant)} survives structural no-go gates, but zero has "
            "proved growing associators, outcomes, information, decoding, and "
            "classical separation."
        ),
        falsifiers_triggered=[
            (
                "Polynomial sample count with separate measurements fails the "
                "entanglement-width contract."
            ),
            (
                "A bounded Racah-label architecture fails both width and "
                "commutant-information gates."
            ),
            (
                "A balanced tree and polynomial merge count do not prove that "
                "the required associators or POVM are implementable."
            ),
            (
                "Naming a covariant sketch and decoder does not satisfy their "
                "information or complexity obligations."
            ),
        ],
    )


def write_growing_width_architecture_report(
    output_path: Path = REPORT_PATH,
    *,
    write_registry: bool = True,
    registry_experiment_id: str = DEFAULT_EXPERIMENT_ID,
    registry_candidate_id: str = DEFAULT_CANDIDATE_ID,
    registry_result_id: str | None = None,
) -> dict[str, object]:
    payload = asdict(build_growing_width_architecture_report())
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    if write_registry:
        upsert_negative_result(
            NegativeResultRecord(
                id="NEG-COSET-MANY-SEPARATE-COPIES-NOT-GROWING-WIDTH-MEASUREMENT",
                source=str(output_path),
                claim=(
                    "Polynomially many separately measured coset states "
                    "satisfy the multiregister entanglement-width requirement."
                ),
                reason_invalid=(
                    "The joint quantum width remains one; classical "
                    "postprocessing cannot retroactively create the required "
                    "entangled POVM."
                ),
                lesson=(
                    "Require a typed growing-width quantum DAG with carrier "
                    "preservation and a noncommutant covariant final POVM."
                ),
                applies_to=[
                    registry_candidate_id,
                    registry_experiment_id,
                    "PO-MEASUREMENT",
                    "PO-COMPLEXITY",
                    "PO-NO-GO",
                ],
                evidence=payload["headline_metrics"],
            )
        )
        result_id = (
            registry_result_id
            or f"RESULT-{registry_experiment_id}-COSET"
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
                artifacts={"coset_growing_width_architecture": str(output_path)},
            )
        )
    return payload


if __name__ == "__main__":
    report = write_growing_width_architecture_report()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))

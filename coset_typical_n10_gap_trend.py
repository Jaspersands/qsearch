"""Numerical real-gap trend on exactly square-free n=10 blocks."""

from __future__ import annotations

import hashlib
import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path

import numpy as np

from research_registry import (
    ExperimentResultRecord,
    NegativeResultRecord,
    upsert_experiment_result,
    upsert_negative_result,
    utc_now,
)


CERTIFICATE_PATH = Path(
    "research/certificates/coset_typical_n10_m8_numerical_gap_certificate.json"
)
INVARIANT_REPORT_PATH = Path(
    "research/representation/coset_typical_invariant_contraction.json"
)
MODULAR_REPORT_PATH = Path(
    "research/representation/coset_typical_modular_yjm_contraction.json"
)
REPORT_PATH = Path(
    "research/representation/coset_typical_n10_gap_trend.json"
)
DEFAULT_EXPERIMENT_ID = "EXP-COSET-TYPICAL-N10-GAP-TREND"
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"
DEPENDENCY_PATH = Path("symmetric_yjm_multiplicity_contraction.py")


@dataclass(frozen=True)
class NumericalGapTrendRecord:
    target_partition: list[int]
    multiplicity: int
    target_dimension: int
    penalty_gap: float
    maximum_penalty_residual: float
    maximum_fiber_orthogonality_residual: float
    maximum_tableau_propagation_residual: float
    separator_eigenvalues: list[float]
    minimum_numerical_raw_gap: float
    minimum_numerical_lcu_normalized_gap: float
    exact_modular_square_free: bool
    floating_point_only_gap_magnitude: bool
    declared_budget_block_error_upper_bound: float
    declared_budget_conditional_gap_lower_bound: float
    declared_budget_survives: bool
    machine_verified_roundoff_bound: bool


@dataclass(frozen=True)
class N10GapTrendReport:
    created_at: str
    evidence_contract: dict[str, object]
    records: list[NumericalGapTrendRecord]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, bool | str]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _read_json(path: Path) -> dict:
    resolved = path
    if not resolved.exists():
        resolved = Path(__file__).resolve().parent / path
    return json.loads(resolved.read_text())


def _load_m8_certificate() -> dict:
    payload = _read_json(CERTIFICATE_PATH)
    root = Path(__file__).resolve().parent
    expected = hashlib.sha256((root / DEPENDENCY_PATH).read_bytes()).hexdigest()
    if payload.get("certificate_contract", {}).get(
        "dependency_sha256", {}
    ).get(str(DEPENDENCY_PATH)) != expected:
        raise ArithmeticError("m8 numerical-gap dependency hash changed")
    record = payload["record"]
    eigenvalues = np.array(record["separator_eigenvalues"])
    traces = [
        float(np.sum(eigenvalues**degree))
        for degree in range(1, record["kronecker_multiplicity"] + 1)
    ]
    if not np.allclose(
        traces,
        record["numerical_power_traces"],
        atol=1e-11,
    ):
        raise ArithmeticError("m8 numerical power traces are inconsistent")
    if float(min(np.diff(eigenvalues))) != record["minimum_numerical_raw_gap"]:
        raise ArithmeticError("m8 numerical minimum gap is inconsistent")
    return record


def _declared_budget(
    record: dict,
    *,
    normwise_roundoff_budget: float = 1e-6,
) -> tuple[float, float, bool]:
    multiplicity = int(record["kronecker_multiplicity"])
    root_subspace_distance = math.sqrt(multiplicity) * (
        float(record["maximum_penalty_residual"])
        + normwise_roundoff_budget
    )
    cumulative_propagation = (
        int(record["target_dimension"]) - 1
    ) * (
        float(record["maximum_tableau_propagation_residual"])
        + normwise_roundoff_budget
    )
    block_error = (
        16 * root_subspace_distance
        + 8
        * (
            float(record["maximum_fiber_orthogonality_residual"])
            + cumulative_propagation
        )
        + normwise_roundoff_budget
    )
    conditional_gap = (
        float(record["minimum_numerical_raw_gap"]) - 2 * block_error
    )
    return block_error, conditional_gap, conditional_gap > 0


def _trend_record(record: dict, exact_targets: set[tuple[int, ...]]) -> NumericalGapTrendRecord:
    block_error, conditional_gap, survives = _declared_budget(record)
    target = tuple(record["target_partition"])
    return NumericalGapTrendRecord(
        target_partition=list(target),
        multiplicity=int(record["kronecker_multiplicity"]),
        target_dimension=int(record["target_dimension"]),
        penalty_gap=float(record["penalty_gap"]),
        maximum_penalty_residual=float(record["maximum_penalty_residual"]),
        maximum_fiber_orthogonality_residual=float(
            record["maximum_fiber_orthogonality_residual"]
        ),
        maximum_tableau_propagation_residual=float(
            record["maximum_tableau_propagation_residual"]
        ),
        separator_eigenvalues=list(record["separator_eigenvalues"]),
        minimum_numerical_raw_gap=float(record["minimum_numerical_raw_gap"]),
        minimum_numerical_lcu_normalized_gap=(
            float(record["minimum_numerical_raw_gap"]) / 2
        ),
        exact_modular_square_free=target in exact_targets,
        floating_point_only_gap_magnitude=True,
        declared_budget_block_error_upper_bound=block_error,
        declared_budget_conditional_gap_lower_bound=conditional_gap,
        declared_budget_survives=survives,
        machine_verified_roundoff_bound=False,
    )


def build_n10_gap_trend_report() -> N10GapTrendReport:
    invariant = _read_json(INVARIANT_REPORT_PATH)
    modular = _read_json(MODULAR_REPORT_PATH)
    exact_targets = {
        tuple(record["target_partition"])
        for record in modular.get("n10_prime_certificates", [])
        if record.get(
            "rational_characteristic_polynomial_square_free_consequence",
            False,
        )
    }
    m6 = next(
        record
        for record in invariant["records"]
        if tuple(record["target_partition"]) == (5, 5)
    )
    m8 = _load_m8_certificate()
    records = [
        _trend_record(m6, exact_targets),
        _trend_record(m8, exact_targets),
    ]
    gap_ratio = (
        records[1].minimum_numerical_lcu_normalized_gap
        / records[0].minimum_numerical_lcu_normalized_gap
    )
    metrics: dict[str, int | float] = {
        "numerical_gap_target_count": len(records),
        "exact_square_free_numerical_gap_target_count": sum(
            int(record.exact_modular_square_free) for record in records
        ),
        "minimum_audited_multiplicity": min(
            record.multiplicity for record in records
        ),
        "maximum_audited_multiplicity": max(
            record.multiplicity for record in records
        ),
        "multiplicity6_lcu_normalized_gap": (
            records[0].minimum_numerical_lcu_normalized_gap
        ),
        "multiplicity8_lcu_normalized_gap": (
            records[1].minimum_numerical_lcu_normalized_gap
        ),
        "multiplicity8_to_multiplicity6_gap_ratio": gap_ratio,
        "multiplicity6_to_multiplicity8_gap_drop_factor": 1 / gap_ratio,
        "declared_budget_survival_count": sum(
            int(record.declared_budget_survives) for record in records
        ),
        "machine_verified_roundoff_bound_count": 0,
        "inverse_polynomial_normalized_gap_theorem_count": 0,
        "all_n_gap_trend_sample_count": 0,
        "coherent_typical_multiplicity_transform_count": 0,
        "typical_label_hidden_involution_decoder_count": 0,
    }
    return N10GapTrendReport(
        created_at=utc_now(),
        evidence_contract={
            "exactness": (
                "Good-prime certificates prove both characteristic polynomials "
                "are square-free, but do not certify their real gap magnitudes."
            ),
            "numerics": (
                "Sparse YJM eigensolves isolate each multiplicity fiber and "
                "stream target tableaux without explicit group rows."
            ),
            "error_status": (
                "A conservative declared 1e-6 normwise budget survives both "
                "observed gaps, but it is not a machine-verified roundoff or "
                "interval certificate."
            ),
            "interpretation": (
                "The two-point multiplicity trend is a falsification signal, "
                "not an asymptotic fit or proof of gap collapse."
            ),
        },
        records=records,
        headline_metrics=metrics,
        claim_gate={
            "both_blocks_exactly_square_free": all(
                record.exact_modular_square_free for record in records
            ),
            "real_gap_magnitudes_exactly_certified": False,
            "machine_verified_roundoff_bounds": False,
            "inverse_polynomial_normalized_gap_proved": False,
            "all_n_trend_established": False,
            "coherent_transform_proved": False,
            "hidden_involution_decoder_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The observed normalized gap drops by more than seven-fold "
                "between multiplicities six and eight, and neither magnitude "
                "nor an all-n inverse-polynomial bound is exact."
            ),
        },
        status=(
            "exact-square-free-ladder-numerical-normalized-gap-shrinks-precision-proof-open"
        ),
        summary=(
            "The exactly square-free multiplicity-eight block has numerical "
            f"LCU-normalized gap {records[1].minimum_numerical_lcu_normalized_gap:.6g}, "
            f"a {1 / gap_ratio:.2f}-fold drop from multiplicity six; this "
            "strengthens the precision blocker and does not establish a trend theorem."
        ),
        falsifiers_triggered=[
            "Exact square-freeness does not prevent a sharp drop in the observed real gap.",
            "Two multiplicities at one n do not establish asymptotic gap scaling.",
            "Declared floating-point budgets are not machine-verified interval proofs.",
            "No inverse-polynomial normalized gap, coherent transform, decoder, or classical separation is supplied.",
        ],
    )


def write_n10_gap_trend_report(
    output_path: Path = REPORT_PATH,
    *,
    write_registry: bool = True,
    registry_experiment_id: str = DEFAULT_EXPERIMENT_ID,
    registry_candidate_id: str = DEFAULT_CANDIDATE_ID,
    registry_result_id: str | None = None,
) -> dict:
    payload = asdict(build_n10_gap_trend_report())
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    if write_registry:
        upsert_negative_result(
            NegativeResultRecord(
                id="NEG-COSET-TYPICAL-EXISTING-FINITE-GAPS-DO-NOT-ESTABLISH-STABLE-PRECISION",
                source=str(output_path),
                claim=(
                    "The existing exactly square-free n=10 blocks provide "
                    "evidence of stable phase-estimation precision."
                ),
                reason_invalid=(
                    "The numerical LCU-normalized gap drops by "
                    f"{payload['headline_metrics']['multiplicity6_to_multiplicity8_gap_drop_factor']:.2f}x "
                    "from multiplicity six to eight, and neither magnitude has "
                    "a machine-verified interval certificate."
                ),
                lesson=(
                    "Measure higher exact-ladder gaps and derive a "
                    "separator-specific all-n bound; treat current numerics only "
                    "as a kill signal against unsupported precision claims."
                ),
                applies_to=[registry_candidate_id, registry_experiment_id],
                evidence=payload["headline_metrics"],
            )
        )
        result_id = registry_result_id or f"RESULT-{registry_experiment_id}-LATEST"
        upsert_experiment_result(
            ExperimentResultRecord(
                id=result_id,
                experiment_id=registry_experiment_id,
                candidate_id=registry_candidate_id,
                created_at=payload["created_at"],
                status=payload["status"],
                summary=payload["summary"],
                metrics=payload["headline_metrics"],
                falsifiers_triggered=payload["falsifiers_triggered"],
                artifacts={"coset_typical_n10_gap_trend": str(output_path)},
            )
        )
    return payload


if __name__ == "__main__":
    print(
        json.dumps(
            write_n10_gap_trend_report()["headline_metrics"],
            indent=2,
            sort_keys=True,
        )
    )

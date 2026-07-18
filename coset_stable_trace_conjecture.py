"""Generate a falsifiable exact-trace conjecture from sparse Racah quartics.

The trace is minus the linear coefficient of the reconstructed monic
characteristic polynomial.  Four consecutive rows determine a cubic candidate;
all later rows are held out.  This module records the fit and holdout checks but
does not call interpolation a proof.  The missing proof is an exact evaluation
of the marked-cycle character sum for the bounded-support orbit Hamiltonian.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Sequence

import sympy as sp

from research_registry import (
    ExperimentResultRecord,
    NegativeResultRecord,
    upsert_experiment_result,
    upsert_negative_result,
    utc_now,
)


COSET_SPARSE_STABLE_GAP_PATH = Path(
    "research/representation/coset_sparse_stable_gap_probe.json"
)
COSET_STABLE_TRACE_CONJECTURE_PATH = Path(
    "research/representation/coset_stable_trace_conjecture.json"
)
DEFAULT_EXPERIMENT_ID = "EXP-COSET-STABLE-TRACE-CONJECTURE"
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


@dataclass(frozen=True)
class TraceHoldoutRecord:
    n: int
    observed_trace: int
    predicted_trace: int
    residual: int
    matched: bool


@dataclass(frozen=True)
class StableTraceConjectureReport:
    created_at: str
    source_artifact: str
    channel_contract: dict[str, object]
    training_n_values: tuple[int, ...]
    training_trace_values: tuple[int, ...]
    finite_difference_rows: list[list[int]]
    interpolated_degree: int
    candidate_trace_formula: str
    candidate_trace_formula_expanded: str
    holdout_records: list[TraceHoldoutRecord]
    proof_obligation: dict[str, object]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, bool | str]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _finite_differences(values: Sequence[int]) -> list[list[int]]:
    rows = [list(values)]
    while len(rows[-1]) > 1:
        rows.append(
            [right - left for left, right in zip(rows[-1], rows[-1][1:])]
        )
    return rows


def build_stable_trace_conjecture(
    sparse_records: Sequence[dict],
    training_count: int = 4,
    source_artifact: str = str(COSET_SPARSE_STABLE_GAP_PATH),
) -> StableTraceConjectureReport:
    records = sorted(sparse_records, key=lambda item: int(item["n"]))
    if len(records) <= training_count:
        raise ValueError("at least one out-of-sample holdout row is required")
    training = records[:training_count]
    holdouts = records[training_count:]
    training_n = tuple(int(record["n"]) for record in training)
    if any(right != left + 1 for left, right in zip(training_n, training_n[1:])):
        raise ValueError("training n values must be consecutive")
    training_traces = tuple(
        -int(record["integer_characteristic_polynomial"][1])
        for record in training
    )
    n_symbol = sp.symbols("n", integer=True, positive=True)
    polynomial = sp.interpolate(
        list(zip(training_n, training_traces)), n_symbol
    )
    polynomial = sp.factor(polynomial)
    holdout_records = []
    for record in holdouts:
        n = int(record["n"])
        observed = -int(record["integer_characteristic_polynomial"][1])
        predicted = int(polynomial.subs(n_symbol, n))
        holdout_records.append(
            TraceHoldoutRecord(
                n=n,
                observed_trace=observed,
                predicted_trace=predicted,
                residual=observed - predicted,
                matched=observed == predicted,
            )
        )
    differences = _finite_differences(training_traces)
    degree = int(sp.degree(polynomial, n_symbol))
    holdout_matches = sum(record.matched for record in holdout_records)
    metrics: dict[str, int | float] = {
        "training_row_count": len(training),
        "holdout_row_count": len(holdout_records),
        "holdout_match_count": holdout_matches,
        "interpolated_degree": degree,
        "constant_third_difference_count": int(
            degree == 3 and len(set(differences[3])) == 1
        ),
        "maximum_holdout_residual": max(
            (abs(record.residual) for record in holdout_records), default=0
        ),
        "exact_marked_cycle_trace_theorem_count": 0,
        "all_n_quartic_theorem_count": 0,
        "all_n_root_separation_theorem_count": 0,
    }
    all_holdouts_match = holdout_matches == len(holdout_records)
    return StableTraceConjectureReport(
        created_at=utc_now(),
        source_artifact=source_artifact,
        channel_contract={
            "source": "W_n=(n-2,2)",
            "intermediate_and_final": "alpha_n=xi_n=(n-3,2,1)",
            "operator": "support-intersection-two transposition/3-cycle orbit Hamiltonian",
            "trace_source": "minus the linear coefficient of the multiplicity-four characteristic polynomial",
            "stable_range_under_test": f"n>={training_n[0]}",
        },
        training_n_values=training_n,
        training_trace_values=training_traces,
        finite_difference_rows=differences,
        interpolated_degree=degree,
        candidate_trace_formula=str(polynomial),
        candidate_trace_formula_expanded=str(sp.expand(polynomial)),
        holdout_records=holdout_records,
        proof_obligation={
            "exact_identity_to_prove": (
                "Tr H_n = 4*n^3 - 46*n^2 + 149*n - 118 on Hom_Sn(V_xi, V_xi tensor V_W)"
            ),
            "character_sum": (
                "n(n-1)(n-2)/n! times sum_g chi_xi(g) chi_xi(g tau) chi_W(g c), "
                "with tau=(1 2), c=(1 2 3)"
            ),
            "character_polynomials": {
                "W_n": "binomial(X1,2)+X2-X1",
                "xi_n": "(X1^3-6*X1^2+8*X1)/3-X3",
            },
            "acceptable_routes": [
                "marked-cycle factorial-moment enumeration",
                "partition-algebra trace evaluation",
                "explicit stable Specht intertwiners",
            ],
            "interpolation_is_not_acceptable_as_proof": True,
        },
        headline_metrics=metrics,
        claim_gate={
            "cubic_candidate_generated": degree == 3,
            "out_of_sample_holdouts_match": all_holdouts_match,
            "exact_marked_cycle_trace_proved": False,
            "complete_quartic_formula_proved": False,
            "root_separation_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The cubic trace formula survives holdout data, but interpolation gives neither an exact character "
                "identity nor the remaining quartic coefficients or root separation."
            ),
        },
        status=(
            "stable-trace-cubic-survives-holdout-exact-proof-open"
            if degree == 3 and all_holdouts_match
            else "stable-trace-cubic-falsified-by-holdout"
        ),
        summary=(
            f"The cubic trace candidate {sp.expand(polynomial)} matches {holdout_matches}/"
            f"{len(holdout_records)} out-of-sample rows; an exact marked-cycle proof remains open."
        ),
        falsifiers_triggered=[
            "A cubic interpolation, even with holdout matches, is not an all-n character identity.",
            "The trace alone does not determine a multiplicity-four spectrum.",
            "Integer characteristic coefficients do not imply inverse-polynomial root separation.",
            "A spectral theorem still would not supply a coherent circuit or decoder.",
        ],
    )


def load_and_build_stable_trace_conjecture(
    source_path: Path = COSET_SPARSE_STABLE_GAP_PATH,
    training_count: int = 4,
) -> StableTraceConjectureReport:
    if not source_path.exists():
        raise FileNotFoundError(
            f"missing {source_path}; run qsearch.py coset-racah-sparse-gap first"
        )
    payload = json.loads(source_path.read_text())
    return build_stable_trace_conjecture(
        payload.get("records", []),
        training_count=training_count,
        source_artifact=str(source_path),
    )


def write_stable_trace_conjecture_report(
    output_path: Path = COSET_STABLE_TRACE_CONJECTURE_PATH,
    source_path: Path = COSET_SPARSE_STABLE_GAP_PATH,
    training_count: int = 4,
    write_registry: bool = True,
    registry_experiment_id: str = DEFAULT_EXPERIMENT_ID,
    registry_candidate_id: str = DEFAULT_CANDIDATE_ID,
    registry_result_id: str | None = None,
) -> dict:
    payload = asdict(
        load_and_build_stable_trace_conjecture(
            source_path=source_path, training_count=training_count
        )
    )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    if write_registry:
        upsert_negative_result(
            NegativeResultRecord(
                id="NEG-COSET-TRACE-HOLDOUT-AS-EXACT-CHARACTER-IDENTITY",
                source=str(output_path),
                claim=(
                    "A cubic trace interpolation with an n=11 holdout match proves the stable character identity."
                ),
                reason_invalid=(
                    "No degree bound or exact marked-cycle character-sum evaluation has been proved, and the trace "
                    "does not determine the full quartic spectrum."
                ),
                lesson=(
                    "Use the formula as a precise theorem target and prove it by marked-cycle factorial moments or "
                    "partition algebra before deriving any gap consequence."
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
                artifacts={"coset_stable_trace_conjecture": str(output_path)},
            )
        )
    return payload

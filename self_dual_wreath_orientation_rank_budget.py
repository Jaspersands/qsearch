"""Rank-retention calibration for direct orientation filters.

The physical frame on ``k`` unequal wreath labels has dimension

    D = 2^k C

and trace ``C``, hence mean eigenvalue ``mu=2^-k``.  For every multiplier
``A>=1``, the elementary trace bound gives

    rank(1[B>A mu]) < D/A.                                   (1)

An orientation filter on a subspace ``H`` of dimension ``r`` rejects exactly
``D/2^r`` Hilbert-space dimensions.  Choosing ``A=2^r`` therefore gives the
filter precisely enough rank capacity, in principle, to remove every spectral
direction above ``A mu``.  This is only a capacity theorem: it does not prove
that the structured orientation subspace aligns with those directions.

The natural-source retention identity supplies the complementary probability
bound.  For iid Plancherel source labels,

    E[L_H] = 2^-r + (1-2^-r)/n!.

Set ``r=ceil(a log_2 n)`` and test the event ``L_H<=n^-b`` with ``0<b<a``.
Markov gives failure probability ``O(n^{b-a})`` and the gentle-measurement loss
is ``O(n^-b/2)``.  Thus a logarithmic-dimensional subspace simultaneously has

* polynomial spectral cutoff ``A mu=poly(n)2^-k``;
* enough rejection rank to match the universal high-eigenvalue count bound;
* acceptance ``1-o(1)`` and vanishing information loss.

This corrects the earlier emphasis on ``r=Omega(k)``.  Linear ``r`` proves
stronger retention than needed but leaves exponentially less rejection rank
than trace information alone can justify.  The next mathematical obligation
is alignment: select ``Theta(log n)`` source-adapted block directions and prove
that they span the actual high-spectrum subspace rather than only one known
common core.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import numpy as np

from research_registry import utc_now
from self_dual_wreath_orientation_retention_theorem import (
    expected_rejection_fraction_log2,
)


REPORT_PATH = Path(
    "research/representation/self_dual_wreath_orientation_rank_budget.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-ORIENTATION-RANK-BUDGET"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


@dataclass(frozen=True)
class TraceRankControl:
    control_id: str
    dimension: int
    mean_eigenvalue: float
    cutoff_multiplier: int
    cutoff: float
    high_eigenvalue_count: int
    strict_trace_count_upper_bound: float
    orientation_subspace_dimension: int
    orientation_rejection_rank: int
    rank_capacity_covers_high_spectrum: bool
    trace_count_bound_verified: bool
    status: str


@dataclass(frozen=True)
class OrientationRankBudgetScalingRecord:
    n: int
    log2_hidden_label_count: float
    information_threshold_copy_count: int
    cutoff_polynomial_degree: int
    retention_threshold_power: int
    orientation_subspace_dimension: int
    orientation_subspace_size_decimal: str
    log2_cutoff_multiplier: int
    cutoff_multiplier_at_least_n_to_degree: bool
    cutoff_multiplier_less_than_twice_n_to_degree: bool
    rejected_hilbert_fraction_log2: int
    trace_high_spectrum_fraction_upper_bound_log2: int
    rejection_rank_matches_trace_bound: bool
    expected_rejection_fraction_log2: float
    retention_threshold_log2: float
    markov_failure_probability_log2_upper_bound: float
    gentle_information_loss_upper_bound: float
    high_probability_retention_certified: bool
    logarithmic_subspace_is_sublinear_in_copy_count: bool
    legacy_linear_subspace_dimension: int
    legacy_rejected_hilbert_fraction_log2: int
    legacy_rank_budget_covers_same_polynomial_tail_from_trace_alone: bool
    source_adapted_alignment_proved: bool
    conditioned_polynomial_frame_norm_proved: bool
    status: str


@dataclass(frozen=True)
class OrientationRankBudgetReport:
    created_at: str
    theorem_contract: dict[str, Any]
    finite_controls: list[TraceRankControl]
    scaling_records: list[OrientationRankBudgetScalingRecord]
    proof_obligations: list[dict[str, bool | str]]
    adversarial_audit: list[dict[str, bool | str]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, bool | str]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def trace_high_spectrum_count_bound(
    dimension: int,
    cutoff_multiplier: float,
) -> float:
    """Strict upper bound on ``rank(1[B>A*Tr(B)/D])``."""

    if dimension < 1:
        raise ValueError("dimension must be positive")
    if cutoff_multiplier < 1:
        raise ValueError("cutoff multiplier must be at least one")
    return dimension / cutoff_multiplier


def audit_trace_rank_control(
    eigenvalues: tuple[float, ...],
    subspace_dimension: int,
    *,
    control_id: str,
    tolerance: float = 1e-12,
) -> TraceRankControl:
    if not eigenvalues or any(value < 0 for value in eigenvalues):
        raise ValueError("a nonempty nonnegative spectrum is required")
    if subspace_dimension < 0:
        raise ValueError("subspace dimension must be nonnegative")
    dimension = len(eigenvalues)
    multiplier = 1 << subspace_dimension
    mean = float(sum(eigenvalues) / dimension)
    cutoff = multiplier * mean
    high_count = int(sum(value > cutoff + tolerance for value in eigenvalues))
    upper = trace_high_spectrum_count_bound(dimension, multiplier)
    rejection_rank = dimension // multiplier
    integral_rank = dimension % multiplier == 0
    trace_verified = high_count < upper + tolerance
    covers = integral_rank and rejection_rank >= high_count
    return TraceRankControl(
        control_id=control_id,
        dimension=dimension,
        mean_eigenvalue=mean,
        cutoff_multiplier=multiplier,
        cutoff=cutoff,
        high_eigenvalue_count=high_count,
        strict_trace_count_upper_bound=upper,
        orientation_subspace_dimension=subspace_dimension,
        orientation_rejection_rank=rejection_rank,
        rank_capacity_covers_high_spectrum=covers,
        trace_count_bound_verified=trace_verified,
        status=(
            "exact-trace-rank-capacity-control"
            if trace_verified and covers
            else "trace-rank-control-failure"
        ),
    )


def rank_budget_scaling_record(
    n: int,
    *,
    cutoff_polynomial_degree: int = 8,
    retention_threshold_power: int = 4,
    legacy_block_size: int = 8,
) -> OrientationRankBudgetScalingRecord:
    if n < 3:
        raise ValueError("n must be at least three")
    if cutoff_polynomial_degree <= retention_threshold_power:
        raise ValueError("cutoff degree must exceed retention threshold power")
    if retention_threshold_power <= 0:
        raise ValueError("retention threshold power must be positive")
    if legacy_block_size < 1:
        raise ValueError("legacy block size must be positive")

    log_group_order = math.lgamma(n + 1) / math.log(2)
    copies = math.ceil(log_group_order)
    logarithmic_dimension = math.ceil(
        cutoff_polynomial_degree * math.log2(n)
    )
    multiplier = 1 << logarithmic_dimension
    expected_log = expected_rejection_fraction_log2(
        log_group_order,
        logarithmic_dimension,
    )
    threshold_log = -retention_threshold_power * math.log2(n)
    markov_log = expected_log - threshold_log
    gentle_loss = n ** (-retention_threshold_power / 2)
    legacy_dimension = max(1, copies // legacy_block_size)
    # Trace alone bounds the relevant high-spectrum fraction by 2^-r.  A
    # smaller rejection fraction cannot guarantee capacity for the same tail.
    legacy_covers = legacy_dimension <= logarithmic_dimension
    return OrientationRankBudgetScalingRecord(
        n=n,
        log2_hidden_label_count=log_group_order,
        information_threshold_copy_count=copies,
        cutoff_polynomial_degree=cutoff_polynomial_degree,
        retention_threshold_power=retention_threshold_power,
        orientation_subspace_dimension=logarithmic_dimension,
        orientation_subspace_size_decimal=str(multiplier),
        log2_cutoff_multiplier=logarithmic_dimension,
        cutoff_multiplier_at_least_n_to_degree=(
            logarithmic_dimension
            >= cutoff_polynomial_degree * math.log2(n)
        ),
        cutoff_multiplier_less_than_twice_n_to_degree=(
            logarithmic_dimension
            < cutoff_polynomial_degree * math.log2(n) + 1
        ),
        rejected_hilbert_fraction_log2=-logarithmic_dimension,
        trace_high_spectrum_fraction_upper_bound_log2=-logarithmic_dimension,
        rejection_rank_matches_trace_bound=True,
        expected_rejection_fraction_log2=expected_log,
        retention_threshold_log2=threshold_log,
        markov_failure_probability_log2_upper_bound=markov_log,
        gentle_information_loss_upper_bound=gentle_loss,
        high_probability_retention_certified=markov_log < 0,
        logarithmic_subspace_is_sublinear_in_copy_count=(
            logarithmic_dimension < copies
        ),
        legacy_linear_subspace_dimension=legacy_dimension,
        legacy_rejected_hilbert_fraction_log2=-legacy_dimension,
        legacy_rank_budget_covers_same_polynomial_tail_from_trace_alone=(
            legacy_covers
        ),
        source_adapted_alignment_proved=False,
        conditioned_polynomial_frame_norm_proved=False,
        status=(
            "logarithmic-rank-retention-window-certified-alignment-open"
            if markov_log < 0 and logarithmic_dimension < copies
            else "finite-scale-logarithmic-window-not-separated"
        ),
    )


def run_orientation_rank_budget() -> OrientationRankBudgetReport:
    controls = [
        audit_trace_rank_control(
            (0.45, 0.25, 0.1, 0.08, 0.05, 0.03, 0.02, 0.02),
            1,
            control_id="NONUNIFORM-D8-R1",
        ),
        audit_trace_rank_control(
            tuple(np.linspace(1, 64, 64) / 2080),
            3,
            control_id="RAMP-D64-R3",
        ),
        audit_trace_rank_control(
            tuple([0.125] * 64),
            3,
            control_id="FLAT-D64-R3",
        ),
    ]
    scaling = [
        rank_budget_scaling_record(n)
        for n in (16, 32, 64, 128, 256, 512, 1024)
    ]
    control_failures = sum(
        not row.trace_count_bound_verified
        or not row.rank_capacity_covers_high_spectrum
        for row in controls
    )
    separated = [
        row
        for row in scaling
        if row.high_probability_retention_certified
        and row.logarithmic_subspace_is_sublinear_in_copy_count
    ]
    legacy_insufficient = sum(
        not row.legacy_rank_budget_covers_same_polynomial_tail_from_trace_alone
        for row in scaling
    )
    verified = control_failures == 0 and len(separated) == len(scaling)
    proof_obligations: list[dict[str, bool | str]] = [
        {
            "obligation": "trace_high_spectrum_count_bound",
            "resolved": True,
            "resolution": (
                "Every eigenvalue counted by 1[B>A Tr(B)/D] contributes more "
                "than A Tr(B)/D to the fixed trace, so the count is <D/A."
            ),
        },
        {
            "obligation": "orientation_rejection_rank_identity",
            "resolved": True,
            "resolution": (
                "The trivial H character occupies one of 2^r Fourier characters "
                "in every quotient coset, hence rejected rank is exactly D/2^r."
            ),
        },
        {
            "obligation": "logarithmic_rank_capacity_match",
            "resolved": verified,
            "resolution": (
                "Taking A=2^r makes rejection rank D/A equal the universal "
                "trace upper bound at cutoff A 2^-k."
            ),
        },
        {
            "obligation": "natural_logarithmic_subspace_retention",
            "resolved": verified,
            "resolution": (
                "The exact Plancherel expectation plus Markov gives failure "
                "O(n^(b-a)) and gentle loss O(n^-b/2) for r=ceil(a log2 n)."
            ),
        },
        {
            "obligation": "source_adapted_high_spectrum_alignment",
            "resolved": False,
            "resolution": (
                "Rank capacity is not alignment. No theorem yet proves that a "
                "Theta(log n)-dimensional block subspace contains every bad "
                "eigenvector or controls the compressed norm."
            ),
        },
    ]
    return OrientationRankBudgetReport(
        created_at=utc_now(),
        theorem_contract={
            "frame_mean": "Tr(B)/D=2^-k for every fixed unequal-label tuple.",
            "trace_count": (
                "rank(1[B>A*2^-k])<D/A for every A>=1."
            ),
            "filter_rank": (
                "An r-dimensional orientation subspace rejects rank D/2^r."
            ),
            "calibration": (
                "Set A=2^r; structured filter capacity then matches the full "
                "trace-allowed high-spectrum count at cutoff A*2^-k."
            ),
            "polynomial_regime": (
                "r=ceil(a log2 n) gives A in [n^a,2n^a), a polynomial cutoff."
            ),
            "retention": (
                "For threshold n^-b and 0<b<a, Markov failure is O(n^(b-a)) "
                "and gentle information loss is O(n^-b/2)."
            ),
            "design_change": (
                "Use Theta(log n), not Theta(k), source-adapted orientation "
                "directions unless a sharper spectral-count theorem justifies "
                "the exponentially smaller rank budget of linear r."
            ),
        },
        finite_controls=controls,
        scaling_records=scaling,
        proof_obligations=proof_obligations,
        adversarial_audit=[
            {
                "objection": "Enough rejected rank proves the filter works.",
                "resolved": False,
                "resolution": (
                    "No. The rejected subspace is highly structured; capacity "
                    "does not imply alignment with the high-spectrum projector."
                ),
            },
            {
                "objection": "Inverse-polynomial rejection destroys the known information.",
                "resolved": True,
                "resolution": (
                    "The exact expectation, Markov, and gentle measurement bounds "
                    "give acceptance 1-o(1) and vanishing success loss."
                ),
            },
            {
                "objection": "Linear r is always better because it rejects less mass.",
                "resolved": True,
                "resolution": (
                    "It also rejects exponentially fewer Hilbert dimensions. "
                    "Without a sparse-spike theorem, that sacrifices the rank "
                    "needed to flatten a polynomial-height spectral tail."
                ),
            },
            {
                "objection": "The trace bound proves the high spectrum actually fills D/A dimensions.",
                "resolved": False,
                "resolution": (
                    "It is only an upper bound. A sharper typical spectral law "
                    "could justify larger r, but no such theorem currently exists."
                ),
            },
        ],
        headline_metrics={
            "trace_high_spectrum_count_theorem_count": 1,
            "orientation_rejection_rank_theorem_count": 1,
            "logarithmic_rank_capacity_match_theorem_count": 1,
            "logarithmic_natural_retention_theorem_count": 1,
            "finite_control_count": len(controls),
            "finite_control_failure_count": control_failures,
            "scaling_record_count": len(scaling),
            "separated_logarithmic_window_count": len(separated),
            "legacy_linear_rank_insufficient_from_trace_only_count": (
                legacy_insufficient
            ),
            "tail_n": scaling[-1].n,
            "tail_logarithmic_subspace_dimension": (
                scaling[-1].orientation_subspace_dimension
            ),
            "tail_copy_count": scaling[-1].information_threshold_copy_count,
            "tail_markov_failure_probability_log2_upper_bound": (
                scaling[-1].markov_failure_probability_log2_upper_bound
            ),
            "source_adapted_alignment_theorem_count": 0,
            "conditioned_polynomial_frame_norm_theorem_count": 0,
            "polynomial_hidden_permutation_decoder_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "trace_rank_calibration_proved": verified,
            "logarithmic_subspace_retains_information_with_high_probability": (
                verified
            ),
            "linear_dimension_subspace_is_default_choice": False,
            "source_adapted_high_spectrum_alignment_proved": False,
            "conditioned_polynomial_frame_norm_proved": False,
            "complete_hidden_permutation_measurement_proved": False,
            "polynomial_hidden_permutation_decoder_proved": False,
            "classical_separation_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "Theta(log n) orientation dimension is now the calibrated "
                "rank-retention regime, but no theorem aligns its structured "
                "rejection subspace with the actual high-spectrum projector."
            ),
        },
        status=(
            "logarithmic-rank-retention-regime-proved-alignment-open"
            if verified
            else "rank-retention-calibration-validation-failure"
        ),
        summary=(
            "Calibrated orientation dimension to the spectral task: "
            "Theta(log n) simultaneously matches the universal polynomial-tail "
            "rank bound and retains natural-source information with high probability."
        ),
        falsifiers_triggered=[
            (
                "Near-perfect retention from dim(H)=Omega(k) is not sufficient "
                "reason to prefer that regime; its rejection rank is exponentially "
                "smaller than trace alone can justify."
            ),
            (
                "A logarithmic-dimensional H is enough for vanishing natural "
                "information loss while preserving polynomial spectral capacity."
            ),
            (
                "Rank matching is not a norm theorem; structured alignment remains "
                "the decisive unresolved obligation."
            ),
        ],
    )


def write_orientation_rank_budget_report(
    path: Path = REPORT_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = (
        "EXP-CODE-SELF-DUAL-WREATH-ORIENTATION-RANK-BUDGET"
    ),
    registry_candidate_id: str = "CODE-COSET-COLLECTIVE",
    registry_result_id: str = "",
) -> dict[str, Any]:
    payload = asdict(run_orientation_rank_budget())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True))

    if write_registry:
        from research_registry import (
            ExperimentResultRecord,
            NegativeResultRecord,
            upsert_experiment_result,
            upsert_negative_result,
        )

        upsert_negative_result(
            NegativeResultRecord(
                id="NEG-SELF-DUAL-WREATH-ORIENTATION-RANK-BUDGET",
                source=registry_experiment_id,
                claim=(
                    "Initial negative claim for EXP-CODE-SELF-DUAL-WREATH-ORIENTATION-RANK-BUDGET."
                ),
                reason_invalid=(
                    "Falsified or refined by exact theorem evaluation."
                ),
                lesson=(
                    "Lesson from exact theorem analysis for EXP-CODE-SELF-DUAL-WREATH-ORIENTATION-RANK-BUDGET."
                ),
                applies_to=[
                    registry_candidate_id,
                    registry_experiment_id,
                    "PO-MEASUREMENT",
                ],
                evidence=payload.get("headline_metrics", {}),
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
                created_at=payload.get("created_at", ""),
                status=payload.get("status", "completed"),
                summary=payload.get("summary", ""),
                metrics=payload.get("headline_metrics", {}),
                falsifiers_triggered=payload.get("falsifiers_triggered", []),
                artifacts={
                    "self_dual_wreath_orientation_rank_budget": str(path)
                },
            )
        )
    return payload


if __name__ == "__main__":
    report = write_orientation_rank_budget_report()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))

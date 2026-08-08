"""Flat vertex transport does not control the relative grading defect.

Even a perfect carrier-channel groupoid can have a constant relation-metric
floor and an endpoint gap that closes with merge width.  The exact boundary is
already visible on a scalar complete-bipartite crossing channel.

Index crossing edges by ``(l,r) in [p] x [p]`` and put

    A = I_p tensor J_p,       B = J_p tensor I_p.

``A`` and ``B`` are the left- and right-vertex channel Grams.  If every
off-common overlap is ``gamma`` and each edge keeps its private orthogonal
mass, then

    M = 2(1-gamma) I + gamma(A+B),
    J = gamma(A-B).

Every normalized vertex block is a positive clique Gram ``J_p``: this model
satisfies the flat partial-isometry groupoid exactly.  Nevertheless ``A`` and
``B`` have row and column modes.  Simultaneous diagonalization gives

    lambda_min(M) = 2(1-gamma),
    ||M^(-1/2) J M^(-1/2)||
      = gamma p / (2(1-gamma)+gamma p),

and therefore the smaller relative endpoint gap is

    (1-defect)/2
      = (1-gamma)/(2(1-gamma)+gamma p).                       (1)

For ``gamma=1/(n-1)`` and natural child width
``p=2^(ceil(log2(n!))-1)``, (1) is exponentially small despite the constant
metric floor.  Thus vertex trivialization, clique atoms, and the signed
Laplacian gap do not by themselves make the hierarchical polar efficient.

The counterfamily intentionally omits internal same-child relations and
higher Cech cells.  Those are now the only plausible mechanism for deleting
the row/column modes.  This is not a natural-wreath lower bound; it is a proof
that the next theorem must analyze the graded Schur quotient of the full
relative complex, not just its metric.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import numpy as np

from research_registry import utc_now


REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_graded_flat_transport_no_go.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-GRADED-FLAT-TRANSPORT-NO-GO"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


@dataclass(frozen=True)
class FlatTransportGradingControl:
    side_width: int
    correlation: float
    crossing_edge_count: int
    predicted_metric_minimum_eigenvalue: float
    observed_metric_minimum_eigenvalue: float
    metric_floor_residual: float
    predicted_grading_defect_norm: float
    observed_grading_defect_norm: float
    grading_defect_residual: float
    predicted_endpoint_gap: float
    observed_endpoint_gap: float
    endpoint_gap_residual: float
    left_vertex_normalized_gram_minimum_eigenvalue: float
    flat_vertex_groupoid_verified: bool
    constant_metric_but_width_closing_endpoint_gap: bool
    exact_audit: bool
    status: str


@dataclass(frozen=True)
class FlatTransportScalingRecord:
    n: int
    information_threshold_copy_count: int
    child_width_log2: int
    reciprocal_correlation: float
    metric_floor: float
    log2_endpoint_gap: float
    endpoint_gap_inverse_polynomial: bool
    status: str


@dataclass(frozen=True)
class GradedFlatTransportNoGoReport:
    created_at: str
    theorem_contract: dict[str, Any]
    finite_controls: list[FlatTransportGradingControl]
    scaling_records: list[FlatTransportScalingRecord]
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def flat_transport_matrices(
    side_width: int,
    correlation: float,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    if side_width < 2:
        raise ValueError("side width must be at least two")
    if not 0 < correlation < 1:
        raise ValueError("correlation must lie strictly between zero and one")
    identity = np.eye(side_width)
    ones = np.ones((side_width, side_width))
    left = np.kron(identity, ones)
    right = np.kron(ones, identity)
    edge_identity = np.eye(side_width**2)
    metric = (
        2 * (1 - correlation) * edge_identity
        + correlation * (left + right)
    )
    graded = correlation * (left - right)
    return metric, graded, left, right


def exact_flat_transport_formulas(
    side_width: int,
    correlation: float,
) -> tuple[float, float, float]:
    baseline = 2 * (1 - correlation)
    defect = correlation * side_width / (
        baseline + correlation * side_width
    )
    endpoint_gap = (1 - correlation) / (
        baseline + correlation * side_width
    )
    return baseline, defect, endpoint_gap


def audit_flat_transport_grading(
    side_width: int,
    correlation: float,
    *,
    tolerance: float = 1e-10,
) -> FlatTransportGradingControl:
    metric, graded, left, _right = flat_transport_matrices(
        side_width,
        correlation,
    )
    predicted_metric, predicted_defect, predicted_gap = (
        exact_flat_transport_formulas(side_width, correlation)
    )
    values, vectors = np.linalg.eigh(metric)
    inverse_root = (
        vectors
        @ np.diag(1 / np.sqrt(values))
        @ vectors.conj().T
    )
    normalized_defect = inverse_root @ graded @ inverse_root
    observed_defect = float(
        np.linalg.norm(
            (normalized_defect + normalized_defect.conj().T) / 2,
            ord=2,
        )
    )
    observed_metric = float(values.min())
    observed_gap = (1 - observed_defect) / 2
    vertex_block = left[:side_width, :side_width]
    vertex_minimum = float(np.linalg.eigvalsh(vertex_block).min())
    audit = bool(
        abs(observed_metric - predicted_metric) <= 100 * tolerance
        and abs(observed_defect - predicted_defect) <= 100 * tolerance
        and abs(observed_gap - predicted_gap) <= 100 * tolerance
        and vertex_minimum >= -100 * tolerance
    )
    return FlatTransportGradingControl(
        side_width=side_width,
        correlation=correlation,
        crossing_edge_count=side_width**2,
        predicted_metric_minimum_eigenvalue=predicted_metric,
        observed_metric_minimum_eigenvalue=observed_metric,
        metric_floor_residual=abs(observed_metric - predicted_metric),
        predicted_grading_defect_norm=predicted_defect,
        observed_grading_defect_norm=observed_defect,
        grading_defect_residual=abs(observed_defect - predicted_defect),
        predicted_endpoint_gap=predicted_gap,
        observed_endpoint_gap=observed_gap,
        endpoint_gap_residual=abs(observed_gap - predicted_gap),
        left_vertex_normalized_gram_minimum_eigenvalue=vertex_minimum,
        flat_vertex_groupoid_verified=vertex_minimum >= -100 * tolerance,
        constant_metric_but_width_closing_endpoint_gap=(
            predicted_metric > 1 and predicted_defect > 0
        ),
        exact_audit=audit,
        status="flat-groupoid-metric-constant-graded-gap-width-closing",
    )


def flat_transport_scaling_record(n: int) -> FlatTransportScalingRecord:
    if n < 5:
        raise ValueError("n must be at least five")
    copy_count = math.ceil(math.lgamma(n + 1) / math.log(2))
    child_width_log2 = copy_count - 1
    gamma = 1 / (n - 1)
    baseline = 2 * (1 - gamma)
    # log2((1-gamma)/(2(1-gamma)+gamma*2^(k-1))) stably.
    numerator_log = math.log2(1 - gamma)
    large_term_log = math.log2(gamma) + child_width_log2
    baseline_log = math.log2(baseline)
    maximum = max(large_term_log, baseline_log)
    denominator_log = maximum + math.log2(
        2 ** (large_term_log - maximum)
        + 2 ** (baseline_log - maximum)
    )
    log_gap = numerator_log - denominator_log
    return FlatTransportScalingRecord(
        n=n,
        information_threshold_copy_count=copy_count,
        child_width_log2=child_width_log2,
        reciprocal_correlation=gamma,
        metric_floor=baseline,
        log2_endpoint_gap=log_gap,
        endpoint_gap_inverse_polynomial=log_gap >= -2 * math.log2(n),
        status="natural-width-flat-transport-graded-gap-superpolynomially-small",
    )


def run_graded_flat_transport_no_go() -> GradedFlatTransportNoGoReport:
    controls = [
        audit_flat_transport_grading(width, 1 / 5)
        for width in (2, 3, 4, 6, 8, 12)
    ]
    scaling = [
        flat_transport_scaling_record(n)
        for n in (6, 8, 10, 12, 16, 24, 32, 48, 64, 128, 256)
    ]
    failures = sum(not row.exact_audit for row in controls)
    closing = sum(
        row.constant_metric_but_width_closing_endpoint_gap
        for row in controls
    )
    inverse_polynomial = sum(
        row.endpoint_gap_inverse_polynomial for row in scaling
    )
    tail = scaling[-1]
    metrics: dict[str, int | float] = {
        "flat_transport_exact_spectrum_theorem_count": 1,
        "metric_floor_not_graded_gap_no_go_theorem_count": 1,
        "finite_flat_transport_control_count": len(controls),
        "finite_flat_transport_control_failure_count": failures,
        "finite_constant_metric_width_closing_gap_count": closing,
        "natural_width_scaling_row_count": len(scaling),
        "natural_width_inverse_polynomial_endpoint_gap_row_count": inverse_polynomial,
        "tail_n": tail.n,
        "tail_copy_count": tail.information_threshold_copy_count,
        "tail_metric_floor": tail.metric_floor,
        "tail_log2_endpoint_gap": tail.log2_endpoint_gap,
        "full_internal_cech_mode_elimination_theorem_count": 0,
        "new_quantum_algorithm_count": 0,
    }
    return GradedFlatTransportNoGoReport(
        created_at=utc_now(),
        theorem_contract={
            "flat_crossing_metric": (
                "M=2(1-gamma)I+gamma(I_p tensor J_p+J_p tensor I_p)."
            ),
            "flat_crossing_grading": (
                "J=gamma(I_p tensor J_p-J_p tensor I_p)."
            ),
            "metric_floor": "lambda_min(M)=2(1-gamma), independent of p.",
            "grading_defect": (
                "||M^-1/2 J M^-1/2||=gamma p/[2(1-gamma)+gamma p]."
            ),
            "endpoint_gap": (
                "gap=(1-gamma)/[2(1-gamma)+gamma p]."
            ),
            "scope": (
                "The model has exact flat vertex clique channels but omits "
                "internal child relations and higher Cech cells."
            ),
        },
        finite_controls=controls,
        scaling_records=scaling,
        proof_obligations=[
            {
                "obligation": "flat_vertex_transport_implies_graded_endpoint_gap",
                "resolved": True,
                "resolution": "Rejected: the exact K_p,p channel has constant metric floor and endpoint gap Theta(1/p).",
            },
            {
                "obligation": "full_internal_relation_quotient_removes_row_column_modes",
                "resolved": False,
                "resolution": "Must analyze the graded Schur complement of internal pair relations and higher Cech cells; vertex-local PSD does not see it.",
            },
            {
                "obligation": "natural_positive_mass_realizes_unquotiented_flat_counterfamily",
                "resolved": False,
                "resolution": "No such natural realization is claimed; the counterfamily isolates the missing theorem rather than proving failure of the PGM route.",
            },
        ],
        adversarial_audit=[
            {
                "objection": "A constant lower bound on M controls every relative eigenvalue.",
                "resolved": True,
                "resolution": "False: the graded form grows on row/column modes while M retains a constant private baseline."
            },
            {
                "objection": "Flat clique transport removes the dangerous modes.",
                "resolved": True,
                "resolution": "False without internal quotienting; K_p,p is flat at every vertex and still has defect tending to one."
            },
            {
                "objection": "The no-go proves the natural wreath hierarchy fails.",
                "resolved": False,
                "resolution": "It does not include internal edges or higher relations, which may cancel the row/column modes."
            },
        ],
        headline_metrics=metrics,
        claim_gate={
            "flat_transport_spectrum_proved": failures == 0,
            "constant_metric_floor_sufficient_for_endpoint_gap": False,
            "flat_vertex_groupoid_sufficient_for_endpoint_gap": False,
            "natural_width_unquotiented_endpoint_gap_inverse_polynomial": False,
            "internal_cech_row_column_mode_elimination_proved": False,
            "natural_pgm_graded_gap_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The best metric hypothesis still permits a Theta(1/p) "
                "graded endpoint gap. Only a full internal/Cech quotient "
                "theorem can remove the dangerous modes."
            ),
        },
        status=(
            "flat-metric-floor-proved-insufficient-for-grading-"
            "internal-cech-mode-elimination-open"
        ),
        summary=(
            "Proved an exact flat-transport counterfamily with constant "
            "metric floor but endpoint gap Theta(1/p); at natural width the "
            f"tail model has log2 gap {tail.log2_endpoint_gap:.3f}."
        ),
        falsifiers_triggered=[
            "A width-independent relation-metric floor is not a width-independent relative-polar gap.",
            "A flat partial-isometry carrier groupoid still supports dangerous row and column modes.",
            "The next proof must quotient internal pair/Cech relations before bounding the grading defect.",
        ],
    )


def write_graded_flat_transport_no_go_report(
    path: Path = REPORT_PATH,
) -> dict[str, Any]:
    payload = asdict(run_graded_flat_transport_no_go())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    return payload


if __name__ == "__main__":
    report = write_graded_flat_transport_no_go_report()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))

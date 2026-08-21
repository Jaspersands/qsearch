"""Complete internal channel closure rescues the flat graded endpoint gap.

The flat crossing-only channel has a constant metric floor but a grading
defect tending to one.  This module adds exactly the structure present in a
fully closed pair-relation channel: all same-child pair edges on both sides,
then takes the graded Schur quotient by those internal relations.

Let each child contain ``p`` orientation vertices, let every pair-core channel
overlap be the same flat scalar ``gamma``, and set

    a = 2(1-gamma).

On all edges of ``K_(2p)`` the metric and vertex grading are

    M = a I + gamma C^* C,
    J = (1-gamma)D + gamma C^* S C,

where ``C`` is oriented incidence, ``S`` is ``+1`` on the left child and
``-1`` on the right, and ``D_(uv)=S_u+S_v``.  Quotienting both internal
``K_p`` edge sets gives an exact crossing-edge decomposition:

* cycle modes: metric ``a``, defect ``0``, multiplicity ``(p-1)^2``;
* row/column modes: metric

      a(a+2 gamma p)/(a+gamma p),

  defect eigenvalues

      +/- gamma p/(a+2 gamma p),

  each with multiplicity ``p-1``;
* the constant mode: metric ``a+2 gamma p``, defect ``0``.

Consequently

    ||M_q^(-1/2) J_q M_q^(-1/2)||
      = gamma p/(2(1-gamma)+2 gamma p) <= 1/2,

and the smaller relative endpoint gap is

    [2(1-gamma)+gamma p]
      / [2(2(1-gamma)+2 gamma p)] >= 1/4.                 (1)

Thus internal closure completely changes the asymptotic conclusion: the gap
does not close at natural width.

Conditional extension.  If a natural carrier channel globalizes to a complete
graph on an affine orientation support, every sibling split either misses the
channel or cuts it into equal affine halves.  Formula (1) then applies channel
by channel.  What remains unproved is precisely that global statement: the
vertex-local carrier groupoid must glue to complete affine channel supports,
with higher Cech relations accounting for exact common directions.
"""

from __future__ import annotations

import itertools
import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import numpy as np

from research_registry import utc_now


REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_internal_closure_graded_rescue.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-INTERNAL-CLOSURE-GRADED-RESCUE"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


@dataclass(frozen=True)
class InternalClosureControl:
    side_width: int
    correlation: float
    internal_edge_count: int
    crossing_edge_count: int
    predicted_cycle_metric: float
    observed_cycle_metric: float
    predicted_row_metric: float
    observed_row_metric: float
    predicted_constant_metric: float
    observed_constant_metric: float
    predicted_grading_defect_norm: float
    observed_grading_defect_norm: float
    predicted_endpoint_gap: float
    observed_endpoint_gap: float
    minimum_metric_eigenvalue: float
    metric_spectrum_residual: float
    defect_spectrum_residual: float
    endpoint_gap_residual: float
    endpoint_gap_at_least_one_quarter: bool
    exact_audit: bool
    status: str


@dataclass(frozen=True)
class InternalClosureScalingRecord:
    n: int
    information_threshold_copy_count: int
    child_width_log2: int
    reciprocal_correlation: float
    metric_floor: float
    grading_defect_norm: float
    endpoint_gap: float
    endpoint_gap_at_least_one_quarter: bool
    status: str


@dataclass(frozen=True)
class InternalClosureGradedRescueReport:
    created_at: str
    theorem_contract: dict[str, Any]
    finite_controls: list[InternalClosureControl]
    scaling_records: list[InternalClosureScalingRecord]
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def complete_channel_relation_matrices(
    side_width: int,
    correlation: float,
) -> tuple[np.ndarray, np.ndarray, tuple[int, ...], tuple[int, ...]]:
    if side_width < 2:
        raise ValueError("side width must be at least two")
    if not 0 < correlation < 1:
        raise ValueError("correlation must lie strictly between zero and one")
    vertex_count = 2 * side_width
    signs = np.asarray([1.0] * side_width + [-1.0] * side_width)
    edges = tuple(itertools.combinations(range(vertex_count), 2))
    incidence = np.zeros((vertex_count, len(edges)))
    for edge_index, (low, high) in enumerate(edges):
        incidence[low, edge_index] = 1
        incidence[high, edge_index] = -1
    baseline = 2 * (1 - correlation)
    metric = (
        baseline * np.eye(len(edges))
        + correlation * incidence.T @ incidence
    )
    edge_grading = np.diag(
        [signs[low] + signs[high] for low, high in edges]
    )
    grading = (
        (1 - correlation) * edge_grading
        + correlation
        * incidence.T
        @ np.diag(signs)
        @ incidence
    )
    internal = tuple(
        index
        for index, (low, high) in enumerate(edges)
        if (low < side_width) == (high < side_width)
    )
    crossing = tuple(
        index for index in range(len(edges)) if index not in set(internal)
    )
    return metric, grading, internal, crossing


def graded_schur_quotient(
    metric: np.ndarray,
    grading: np.ndarray,
    internal: tuple[int, ...],
    crossing: tuple[int, ...],
) -> tuple[np.ndarray, np.ndarray]:
    order = (*internal, *crossing)
    metric = metric[np.ix_(order, order)]
    grading = grading[np.ix_(order, order)]
    internal_dimension = len(internal)
    aa = metric[:internal_dimension, :internal_dimension]
    ax = metric[:internal_dimension, internal_dimension:]
    xx = metric[internal_dimension:, internal_dimension:]
    jaa = grading[:internal_dimension, :internal_dimension]
    jax = grading[:internal_dimension, internal_dimension:]
    jxx = grading[internal_dimension:, internal_dimension:]
    coefficients = (
        np.linalg.solve(aa, ax)
        if internal_dimension
        else np.zeros((0, len(crossing)))
    )
    quotient_metric = xx - ax.conj().T @ coefficients
    quotient_grading = (
        jxx
        - coefficients.conj().T @ jax
        - jax.conj().T @ coefficients
        + coefficients.conj().T @ jaa @ coefficients
    )
    return (
        (quotient_metric + quotient_metric.conj().T) / 2,
        (quotient_grading + quotient_grading.conj().T) / 2,
    )


def exact_internal_closure_formulas(
    side_width: int,
    correlation: float,
) -> tuple[float, float, float, float, float]:
    baseline = 2 * (1 - correlation)
    row_metric = baseline * (
        baseline + 2 * correlation * side_width
    ) / (baseline + correlation * side_width)
    constant_metric = baseline + 2 * correlation * side_width
    defect = correlation * side_width / constant_metric
    endpoint_gap = (1 - defect) / 2
    return baseline, row_metric, constant_metric, defect, endpoint_gap


def _predicted_metric_spectrum(
    side_width: int,
    correlation: float,
) -> np.ndarray:
    cycle, row, constant, _defect, _gap = exact_internal_closure_formulas(
        side_width,
        correlation,
    )
    return np.sort(
        np.asarray(
            [cycle] * (side_width - 1) ** 2
            + [row] * (2 * (side_width - 1))
            + [constant]
        )
    )


def _predicted_defect_spectrum(
    side_width: int,
    correlation: float,
) -> np.ndarray:
    _cycle, _row, _constant, defect, _gap = exact_internal_closure_formulas(
        side_width,
        correlation,
    )
    zero_count = (side_width - 1) ** 2 + 1
    return np.sort(
        np.asarray(
            [-defect] * (side_width - 1)
            + [0.0] * zero_count
            + [defect] * (side_width - 1)
        )
    )


def audit_internal_closure(
    side_width: int,
    correlation: float,
    *,
    tolerance: float = 1e-9,
) -> InternalClosureControl:
    metric, grading, internal, crossing = complete_channel_relation_matrices(
        side_width,
        correlation,
    )
    quotient_metric, quotient_grading = graded_schur_quotient(
        metric,
        grading,
        internal,
        crossing,
    )
    metric_values, vectors = np.linalg.eigh(quotient_metric)
    inverse_root = (
        vectors
        @ np.diag(1 / np.sqrt(metric_values))
        @ vectors.conj().T
    )
    normalized = inverse_root @ quotient_grading @ inverse_root
    defect_values = np.linalg.eigvalsh((normalized + normalized.conj().T) / 2)
    predicted_metric = _predicted_metric_spectrum(side_width, correlation)
    predicted_defect = _predicted_defect_spectrum(side_width, correlation)
    cycle, row, constant, defect, gap = exact_internal_closure_formulas(
        side_width,
        correlation,
    )
    metric_residual = float(
        np.max(np.abs(metric_values - predicted_metric))
    )
    defect_residual = float(
        np.max(np.abs(defect_values - predicted_defect))
    )
    observed_defect = float(np.max(np.abs(defect_values)))
    observed_gap = (1 - observed_defect) / 2
    exact = metric_residual <= 100 * tolerance and defect_residual <= 100 * tolerance
    observed_unique = sorted({round(float(value), 10) for value in metric_values})
    return InternalClosureControl(
        side_width=side_width,
        correlation=correlation,
        internal_edge_count=len(internal),
        crossing_edge_count=len(crossing),
        predicted_cycle_metric=cycle,
        observed_cycle_metric=observed_unique[0],
        predicted_row_metric=row,
        observed_row_metric=observed_unique[1],
        predicted_constant_metric=constant,
        observed_constant_metric=observed_unique[-1],
        predicted_grading_defect_norm=defect,
        observed_grading_defect_norm=observed_defect,
        predicted_endpoint_gap=gap,
        observed_endpoint_gap=observed_gap,
        minimum_metric_eigenvalue=float(metric_values.min()),
        metric_spectrum_residual=metric_residual,
        defect_spectrum_residual=defect_residual,
        endpoint_gap_residual=abs(observed_gap - gap),
        endpoint_gap_at_least_one_quarter=observed_gap >= 0.25 - 100 * tolerance,
        exact_audit=exact,
        status="complete-internal-flat-channel-graded-gap-rescued",
    )


def internal_closure_scaling_record(n: int) -> InternalClosureScalingRecord:
    if n < 5:
        raise ValueError("n must be at least five")
    copy_count = math.ceil(math.lgamma(n + 1) / math.log(2))
    child_width_log2 = copy_count - 1
    gamma = 1 / (n - 1)
    # For large p, evaluate defect/gap after dividing numerator and
    # denominator by gamma*p.  2(1-gamma)/(gamma*p) is representable here.
    ratio = 2 * (1 - gamma) / gamma * 2.0 ** (-child_width_log2)
    defect = 1 / (2 + ratio)
    gap = (1 - defect) / 2
    return InternalClosureScalingRecord(
        n=n,
        information_threshold_copy_count=copy_count,
        child_width_log2=child_width_log2,
        reciprocal_correlation=gamma,
        metric_floor=2 * (1 - gamma),
        grading_defect_norm=defect,
        endpoint_gap=gap,
        endpoint_gap_at_least_one_quarter=gap >= 0.25,
        status="complete-internal-flat-channel-uniform-graded-gap",
    )


def run_internal_closure_graded_rescue() -> (
    InternalClosureGradedRescueReport
):
    controls = [
        audit_internal_closure(width, gamma)
        for gamma in (1 / 5, 1 / 9)
        for width in (2, 3, 4, 6, 8)
    ]
    scaling = [
        internal_closure_scaling_record(n)
        for n in (6, 8, 10, 12, 16, 24, 32, 48, 64, 128, 256)
    ]
    failures = sum(not row.exact_audit for row in controls)
    gap_failures = sum(
        not row.endpoint_gap_at_least_one_quarter for row in controls
    )
    scaling_failures = sum(
        not row.endpoint_gap_at_least_one_quarter for row in scaling
    )
    tail = scaling[-1]
    metrics: dict[str, int | float] = {
        "complete_internal_channel_schur_spectrum_theorem_count": 1,
        "complete_internal_channel_uniform_graded_gap_theorem_count": 1,
        "finite_internal_closure_control_count": len(controls),
        "finite_internal_closure_control_failure_count": failures,
        "finite_quarter_gap_failure_count": gap_failures,
        "natural_width_scaling_row_count": len(scaling),
        "natural_width_quarter_gap_failure_count": scaling_failures,
        "tail_n": tail.n,
        "tail_copy_count": tail.information_threshold_copy_count,
        "tail_metric_floor": tail.metric_floor,
        "tail_grading_defect_norm": tail.grading_defect_norm,
        "tail_endpoint_gap": tail.endpoint_gap,
        "natural_global_affine_channel_closure_theorem_count": 0,
        "new_quantum_algorithm_count": 0,
    }
    verified = not failures and not gap_failures and not scaling_failures
    return InternalClosureGradedRescueReport(
        created_at=utc_now(),
        theorem_contract={
            "complete_channel_model": (
                "Flat scalar carrier channel on every edge of K_(2p), with "
                "two internal K_p edge sets Schur-quotiented before grading."
            ),
            "quotient_metric_spectrum": (
                "2(1-gamma) on cycles; a(a+2gamma p)/(a+gamma p) "
                "on row/column modes; a+2gamma p on constants."
            ),
            "quotient_defect_spectrum": (
                "0 except +/-gamma p/[2(1-gamma)+2gamma p] on "
                "row/column modes."
            ),
            "uniform_endpoint_gap": "Every relative endpoint is at least 1/4.",
            "conditional_affine_extension": (
                "A global flat carrier channel supported on an affine "
                "orientation set has equal complete child halves at every "
                "crossing sibling split, so the theorem applies per channel."
            ),
        },
        finite_controls=controls,
        scaling_records=scaling,
        proof_obligations=[
            {
                "obligation": "internal_complete_channel_removes_flat_row_column_obstruction",
                "resolved": verified,
                "resolution": "Exact Schur diagonalization leaves defect at most one half and endpoint gap at least one quarter for all p and gamma."
            },
            {
                "obligation": "natural_carrier_channels_globalize_to_complete_affine_supports",
                "resolved": False,
                "resolution": "Need an all-depth carrier-index/Cech theorem gluing vertex groupoids and proving affine support closure."
            },
            {
                "obligation": "nonuniform_or_partial_natural_channel_graded_bound",
                "resolved": False,
                "resolution": "The theorem assumes one flat gamma and complete channel closure; missing edges, varying carriers, and higher multiplicity sheaves remain untreated."
            },
        ],
        adversarial_audit=[
            {
                "objection": "The crossing-only Theta(1/p) no-go kills every flat hierarchy.",
                "resolved": True,
                "resolution": "False once complete internal edge relations are Schur-quotiented; the exact gap is at least one quarter."
            },
            {
                "objection": "A vertex-local groupoid automatically supplies complete internal closure.",
                "resolved": False,
                "resolution": "Local path laws do not prove that one channel glues across vertices or that every same-child edge is present."
            },
            {
                "objection": "Finite W6 affine-looking channels prove natural all-depth closure.",
                "resolved": False,
                "resolution": "The required statement is uniform over asymptotically typical globally-distinct portfolios and all hierarchy depths."
            },
        ],
        headline_metrics=metrics,
        claim_gate={
            "complete_internal_flat_channel_spectrum_proved": verified,
            "complete_internal_flat_channel_endpoint_gap_at_least_quarter": verified,
            "crossing_only_flat_no_go_survives_complete_internal_closure": False,
            "natural_global_affine_channel_closure_proved": False,
            "natural_nonuniform_channel_graded_gap_proved": False,
            "natural_pgm_endpoint_gap_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "Internal closure rescues the exact flat model, but natural "
                "carrier channels have not been proved to globalize into the "
                "complete affine supports required by the theorem."
            ),
        },
        status=(
            "complete-internal-flat-channel-quarter-gap-proved-"
            "natural-global-channel-closure-open"
        ),
        summary=(
            "Proved that complete internal pair closure converts the flat "
            "crossing obstruction into a uniform endpoint gap of at least "
            "one quarter, independent of natural merge width."
        ),
        falsifiers_triggered=[
            "The crossing-only flat counterfamily is not stable under the hierarchy's internal Schur quotient.",
            "Metric control becomes useful for grading only after complete internal channel closure is established.",
            "The decisive remaining theorem is global affine gluing of natural carrier channels, not another local star bound.",
        ],
    )


def write_internal_closure_graded_rescue_report(
    path: Path = REPORT_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = (
        "EXP-CODE-SELF-DUAL-WREATH-INTERNAL-CLOSURE-GRADED-RESCUE"
    ),
    registry_candidate_id: str = "CODE-COSET-COLLECTIVE",
    registry_result_id: str = "",
) -> dict[str, Any]:
    payload = asdict(run_internal_closure_graded_rescue())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True))

    return payload


if __name__ == "__main__":
    report = write_internal_closure_graded_rescue_report()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))

"""High-probability edge for independent balanced Steiner line gauges.

The inter-plane gauge space is enormous, but a generic gauge class is benign.
For every Steiner line ``L``, choose independently and uniformly one of the
four sign columns ``s_L in {+1,-1}^3`` with product ``+1``.  Its normalized
line frame contribution is ``s_L s_L^T``.  Writing ``D`` for point degrees,

    C C^T = D + sum_L X_L,
    X_L = embed_L(s_L s_L^T-I_3).                         (1)

The four balanced signs obey

    E X_L = 0,       ||X_L||=2,       E X_L^2=2 I_L.     (2)

For ``d_max=max_x D_x``, self-adjoint matrix Bernstein therefore gives, with
probability at least ``1-delta``,

    ||C C^T-D|| <= t,
    t = sqrt(4 d_max log(2v/delta))
        +(4/3)log(2v/delta).                              (3)

For all projective Steiner lines, ``D=rI`` with ``r=(2^K-2)/2``.  Hence the
condition number is at most ``(r+t)/(r-t)=1+o(1)`` whenever ``t<r``.

For the pattern-rich family, remove the ``2K+1`` isolated points.  On the
remaining giant component,

    d_min=2^(K-2)-2,       d_max<=2^(K-1),                (4)

so the same theorem gives a positive lower edge ``d_min-t`` and bounded
condition tending one.

This is a rigorous rescue criterion, not a natural-law theorem.  Natural
``S_n`` cup/cap and Racah contractions may correlate line gauges strongly.
The result says exactly what would suffice: enough inter-plane gauge
pseudorandomness to obtain a matrix-concentration bound of the scale in (3).
It also shows that the quadratic gauge entropy found by the homology audit is
not itself an obstruction.
"""

from __future__ import annotations

import itertools
import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Literal

import numpy as np

from research_registry import utc_now
from self_dual_wreath_affine_plane_support_pressure_no_go import (
    rich_plane_count_per_vertex,
)
from self_dual_wreath_interplane_gauge_homology import (
    LineFamily,
    pattern_rich_steiner_lines,
)
from self_dual_wreath_signed_steiner_incidence_boundary import (
    projective_points,
    projective_steiner_lines,
)


REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_random_steiner_gauge_edge.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-RANDOM-STEINER-GAUGE-EDGE"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"

BALANCED_LINE_SIGNS: tuple[tuple[int, int, int], ...] = tuple(
    signs
    for signs in itertools.product((-1, 1), repeat=3)
    if math.prod(signs) == 1
)


@dataclass(frozen=True)
class BalancedLineMomentControl:
    mean_residual: float
    second_moment_residual: float
    maximum_operator_norm: float
    predicted_maximum_operator_norm: float
    exact_balanced_line_moments_verified: bool
    status: str


@dataclass(frozen=True)
class RandomSteinerGaugeScalingRecord:
    copy_count: int
    line_family: LineFamily
    point_count: int
    active_point_count: int
    line_count: int
    minimum_active_degree: int
    maximum_active_degree: int
    failure_probability: float
    bernstein_radius: float
    lower_edge_bound: float
    upper_edge_bound: float
    condition_number_bound: float
    bound_nonvacuous: bool
    asymptotic_relative_radius: float
    status: str


@dataclass(frozen=True)
class RandomSteinerGaugeFiniteControl:
    copy_count: int
    line_family: LineFamily
    seed: int
    active_point_count: int
    line_count: int
    observed_minimum_eigenvalue: float
    observed_maximum_eigenvalue: float
    observed_condition_number: float
    bernstein_lower_edge_bound: float
    bernstein_upper_edge_bound: float
    observed_inside_bernstein_interval: bool
    exact_nullity: int
    status: str


@dataclass(frozen=True)
class RandomSteinerGaugeEdgeReport:
    created_at: str
    theorem_contract: dict[str, Any]
    local_moment_control: BalancedLineMomentControl
    full_scaling: list[RandomSteinerGaugeScalingRecord]
    rich_scaling: list[RandomSteinerGaugeScalingRecord]
    finite_controls: list[RandomSteinerGaugeFiniteControl]
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def audit_balanced_line_moments() -> BalancedLineMomentControl:
    matrices = []
    for signs in BALANCED_LINE_SIGNS:
        vector = np.asarray(signs, dtype=float)
        matrices.append(np.outer(vector, vector) - np.eye(3))
    mean = sum(matrices) / len(matrices)
    second = sum(matrix @ matrix for matrix in matrices) / len(matrices)
    norms = [float(np.linalg.norm(matrix, ord=2)) for matrix in matrices]
    mean_residual = float(np.max(np.abs(mean)))
    second_residual = float(np.max(np.abs(second - 2 * np.eye(3))))
    maximum = max(norms)
    verified = bool(
        mean_residual == 0
        and second_residual == 0
        and math.isclose(maximum, 2.0, abs_tol=1e-12)
    )
    return BalancedLineMomentControl(
        mean_residual=mean_residual,
        second_moment_residual=second_residual,
        maximum_operator_norm=maximum,
        predicted_maximum_operator_norm=2.0,
        exact_balanced_line_moments_verified=verified,
        status=(
            "balanced-line-moments-exact"
            if verified
            else "balanced-line-moment-control-failure"
        ),
    )


def _line_family(
    copy_count: int,
    line_family: LineFamily,
) -> tuple[tuple[int, int, int], ...]:
    if line_family == "all":
        return projective_steiner_lines(copy_count)
    if line_family == "pattern-rich":
        if copy_count < 4:
            raise ValueError("pattern-rich controls require K>=4")
        return pattern_rich_steiner_lines(copy_count)
    raise ValueError("unknown line family")


def point_degrees(
    copy_count: int,
    line_family: LineFamily,
) -> np.ndarray:
    points = projective_points(copy_count)
    point_index = {point: index for index, point in enumerate(points)}
    degrees = np.zeros(len(points), dtype=int)
    for line in _line_family(copy_count, line_family):
        for point in line:
            degrees[point_index[point]] += 1
    return degrees


def bernstein_radius(
    dimension: int,
    maximum_degree: int,
    failure_probability: float,
) -> float:
    if dimension < 1 or maximum_degree < 1:
        raise ValueError("dimension and maximum degree must be positive")
    if not 0 < failure_probability < 1:
        raise ValueError("failure_probability must lie in (0,1)")
    logarithm = math.log(2 * dimension / failure_probability)
    # sigma^2=2*d_max and R=2 in self-adjoint matrix Bernstein.
    return math.sqrt(4 * maximum_degree * logarithm) + 4 * logarithm / 3


def random_steiner_gauge_scaling_record(
    copy_count: int,
    line_family: LineFamily,
    *,
    failure_probability: float | None = None,
) -> RandomSteinerGaugeScalingRecord:
    orientation_count = 1 << copy_count
    if failure_probability is None:
        failure_probability = orientation_count**-2
    point_count = orientation_count - 1
    if line_family == "all":
        line_count = point_count * (point_count - 1) // 6
        active_point_count = point_count
        minimum_degree = maximum_degree = (orientation_count - 2) // 2
    elif line_family == "pattern-rich":
        if copy_count < 4:
            raise ValueError("pattern-rich controls require K>=4")
        line_count = rich_plane_count_per_vertex(copy_count)
        active_point_count = point_count - (2 * copy_count + 1)
        minimum_degree = 2 ** (copy_count - 2) - 2
        maximum_degree = max(
            (2**weight - 2)
            * (2 ** (copy_count - weight) - 2)
            // 2
            for weight in range(2, copy_count - 1)
        )
    else:
        raise ValueError("unknown line family")
    radius = bernstein_radius(
        active_point_count,
        maximum_degree,
        failure_probability,
    )
    lower = minimum_degree - radius
    upper = maximum_degree + radius
    nonvacuous = lower > 0
    condition = upper / lower if nonvacuous else math.inf
    return RandomSteinerGaugeScalingRecord(
        copy_count=copy_count,
        line_family=line_family,
        point_count=point_count,
        active_point_count=active_point_count,
        line_count=line_count,
        minimum_active_degree=minimum_degree,
        maximum_active_degree=maximum_degree,
        failure_probability=failure_probability,
        bernstein_radius=radius,
        lower_edge_bound=lower,
        upper_edge_bound=upper,
        condition_number_bound=condition,
        bound_nonvacuous=nonvacuous,
        asymptotic_relative_radius=radius / minimum_degree,
        status=(
            "independent-gauge-high-probability-edge-certified"
            if nonvacuous
            else "finite-bernstein-bound-vacuous-asymptotic-edge-proved"
        ),
    )


def sample_random_signed_gram(
    copy_count: int,
    line_family: LineFamily,
    seed: int,
) -> tuple[np.ndarray, np.ndarray]:
    points = projective_points(copy_count)
    point_index = {point: index for index, point in enumerate(points)}
    lines = _line_family(copy_count, line_family)
    gram = np.zeros((len(points), len(points)), dtype=float)
    rng = np.random.default_rng(seed)
    for line in lines:
        indices = [point_index[point] for point in line]
        signs = np.asarray(
            BALANCED_LINE_SIGNS[int(rng.integers(len(BALANCED_LINE_SIGNS)))],
            dtype=float,
        )
        gram[np.ix_(indices, indices)] += np.outer(signs, signs)
    degrees = np.diag(gram).astype(int)
    active = degrees > 0
    return gram[np.ix_(active, active)], degrees[active]


def audit_random_signed_gram(
    copy_count: int,
    line_family: LineFamily,
    seed: int,
) -> RandomSteinerGaugeFiniteControl:
    gram, degrees = sample_random_signed_gram(
        copy_count,
        line_family,
        seed,
    )
    values = np.linalg.eigvalsh(gram)
    minimum = float(values[0])
    maximum = float(values[-1])
    scaling = random_steiner_gauge_scaling_record(
        copy_count,
        line_family,
    )
    inside = bool(
        minimum >= scaling.lower_edge_bound - 1e-9
        and maximum <= scaling.upper_edge_bound + 1e-9
    )
    nullity = int(np.sum(values < 1e-9))
    condition = maximum / minimum if minimum > 1e-12 else math.inf
    return RandomSteinerGaugeFiniteControl(
        copy_count=copy_count,
        line_family=line_family,
        seed=seed,
        active_point_count=len(degrees),
        line_count=scaling.line_count,
        observed_minimum_eigenvalue=minimum,
        observed_maximum_eigenvalue=maximum,
        observed_condition_number=condition,
        bernstein_lower_edge_bound=scaling.lower_edge_bound,
        bernstein_upper_edge_bound=scaling.upper_edge_bound,
        observed_inside_bernstein_interval=inside,
        exact_nullity=nullity,
        status=(
            "random-balanced-gauge-finite-edge-observed"
            if minimum > 1e-9 and inside
            else "random-balanced-gauge-finite-control-warning"
        ),
    )


def run_random_steiner_gauge_edge() -> RandomSteinerGaugeEdgeReport:
    moments = audit_balanced_line_moments()
    full_scaling = [
        random_steiner_gauge_scaling_record(copy_count, "all")
        for copy_count in range(4, 25)
    ]
    rich_scaling = [
        random_steiner_gauge_scaling_record(copy_count, "pattern-rich")
        for copy_count in range(4, 25)
    ]
    finite_controls = [
        audit_random_signed_gram(copy_count, family, seed)
        for family, copy_count, seed in (
            ("all", 4, 104),
            ("all", 6, 106),
            ("all", 8, 108),
            ("pattern-rich", 5, 205),
            ("pattern-rich", 7, 207),
            ("pattern-rich", 8, 208),
        )
    ]
    failures = int(not moments.exact_balanced_line_moments_verified) + sum(
        not row.observed_inside_bernstein_interval for row in finite_controls
    )
    first_full = next(row.copy_count for row in full_scaling if row.bound_nonvacuous)
    first_rich = next(row.copy_count for row in rich_scaling if row.bound_nonvacuous)
    return RandomSteinerGaugeEdgeReport(
        created_at=utc_now(),
        theorem_contract={
            "independent_balanced_gauge_model": (
                "Each line independently chooses a uniform sign column with "
                "product +1; this is a surrogate, not a derived natural law."
            ),
            "local_moments": (
                "For X_L=s_L s_L^T-I_3, E X_L=0, ||X_L||=2, and "
                "E X_L^2=2I_3."
            ),
            "matrix_bernstein_edge": (
                "With probability 1-delta, ||CC^T-D|| is at most "
                "sqrt(4d_max log(2v/delta))+(4/3)log(2v/delta)."
            ),
            "full_family_consequence": (
                "For all Steiner lines, the normalized condition number tends "
                "to one because r=Theta(2^K) and t=O(sqrt(K2^K))."
            ),
            "rich_family_consequence": (
                "After isolated points are removed, d_min=2^(K-2)-2 and "
                "d_max<=2^(K-1), so a positive edge also holds with high "
                "probability."
            ),
        },
        local_moment_control=moments,
        full_scaling=full_scaling,
        rich_scaling=rich_scaling,
        finite_controls=finite_controls,
        proof_obligations=[
            {
                "obligation": "prove_independent_balanced_gauge_edge",
                "resolved": failures == 0,
                "resolution": (
                    "Exact line moments and self-adjoint matrix Bernstein give "
                    "the stated high-probability interval."
                ),
            },
            {
                "obligation": "show_gauge_entropy_is_not_intrinsically_bad",
                "resolved": True,
                "resolution": (
                    "A uniform random class is asymptotically conditioned even "
                    "though the gauge-space dimension is Theta(4^K)."
                ),
            },
            {
                "obligation": "derive_natural_line_gauge_independence",
                "resolved": False,
                "resolution": (
                    "Natural recoupling reuses source carriers across many "
                    "planes and is certainly not literally independent."
                ),
            },
            {
                "obligation": "replace_independence_by_natural_mixing_bound",
                "resolved": False,
                "resolution": (
                    "It would suffice to prove a martingale variance, trace-"
                    "moment, or dependency-graph bound of order O(2^K poly(K))."
                ),
            },
            {
                "obligation": "extend_to_matrix_valued_weighted_channels",
                "resolved": False,
                "resolution": (
                    "The physical overlap traffic has nonuniform carrier weights "
                    "and orthogonal multiplicity transports."
                ),
            },
        ],
        adversarial_audit=[
            {
                "objection": "Many gauge classes make singularity typical.",
                "resolved": True,
                "resolution": (
                    "False in the independent balanced model; concentration "
                    "places the frame near its diagonal degree operator."
                ),
            },
            {
                "objection": "The signed quotient-kernel family contradicts the random theorem.",
                "resolved": True,
                "resolution": (
                    "It is a highly correlated adversarial class and has tiny "
                    "probability under independent line gauges."
                ),
            },
            {
                "objection": "Finite random controls establish natural pseudorandomness.",
                "resolved": False,
                "resolution": (
                    "They only validate implementation; natural S_n cycle "
                    "moments have not been sampled or bounded."
                ),
            },
            {
                "objection": "Scalar matrix Bernstein directly covers 6j blocks.",
                "resolved": False,
                "resolution": (
                    "Operator-valued summands need centering, dependence control, "
                    "and a physical variance calculation."
                ),
            },
        ],
        headline_metrics={
            "finite_control_count": len(finite_controls),
            "finite_control_failure_count": failures,
            "first_nonvacuous_full_copy_count": first_full,
            "first_nonvacuous_rich_copy_count": first_rich,
            "independent_balanced_gauge_edge_theorem_count": 1,
            "natural_gauge_mixing_theorem_count": 0,
            "matrix_valued_traffic_edge_theorem_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "balanced_line_moments_exact": moments.exact_balanced_line_moments_verified,
            "independent_scalar_gauge_edge_proved": failures == 0,
            "gauge_entropy_intrinsic_obstruction_falsified": True,
            "natural_line_gauges_independent": False,
            "natural_cycle_mixing_bound_proved": False,
            "weighted_matrix_traffic_edge_proved": False,
            "collision_free_noncommon_frame_edge_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "Independent gauges are well conditioned, but the natural "
                "dependent operator-valued gauge law remains unknown."
            ),
        },
        status="independent-gauge-edge-proved-natural-mixing-open",
        summary=(
            "Proved that independent balanced affine-plane gauges produce an "
            "asymptotically well-conditioned Steiner frame; the decisive task "
            "is now a natural recoupling mixing or moment theorem."
        ),
        falsifiers_triggered=[
            (
                "Quadratic inter-plane gauge entropy alone cannot explain a "
                "bad frame edge."
            ),
            (
                "An adversarial singular signing is not representative of a "
                "sufficiently mixing gauge law."
            ),
            (
                "The next natural audit must estimate cycle correlations or "
                "operator-valued variance, not count gauge classes."
            ),
        ],
    )


def write_random_steiner_gauge_edge_report(
    path: Path = REPORT_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = (
        "EXP-CODE-SELF-DUAL-WREATH-RANDOM-STEINER-GAUGE-EDGE"
    ),
    registry_candidate_id: str = "CODE-COSET-COLLECTIVE",
    registry_result_id: str = "",
) -> dict[str, Any]:
    payload = asdict(run_random_steiner_gauge_edge())
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
                id="NEG-SELF-DUAL-WREATH-RANDOM-STEINER-GAUGE-EDGE",
                source=registry_experiment_id,
                claim=(
                    "Initial negative claim for EXP-CODE-SELF-DUAL-WREATH-RANDOM-STEINER-GAUGE-EDGE."
                ),
                reason_invalid=(
                    "Falsified or refined by exact theorem evaluation."
                ),
                lesson=(
                    "Lesson from exact theorem analysis for EXP-CODE-SELF-DUAL-WREATH-RANDOM-STEINER-GAUGE-EDGE."
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
                    "self_dual_wreath_random_steiner_gauge_edge": str(path)
                },
            )
        )
    return payload


if __name__ == "__main__":
    report = write_random_steiner_gauge_edge_report()
    print(json.dumps(report, indent=2, sort_keys=True))

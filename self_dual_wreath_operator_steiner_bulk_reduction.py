"""Operator-valued Steiner bulk reduction to diagonal coverage.

Let each Steiner line ``L`` carry a coefficient fiber ``E_L``.  At each of its
three incident points ``x``, let ``W_(x,L):E_L->H_x`` be an isometry.  The
global incidence map is

    C : direct_sum_L E_L -> direct_sum_x H_x,
    (C z)_x = sum_(L contains x) W_(x,L) z_L.              (1)

No commutation, flatness, or holonomy assumption is made.  Its Gram has
diagonal coverage blocks

    D_x = sum_(L contains x) W_(x,L) W_(x,L)^*,           (2)

and, because a Steiner point pair has at most one common line,

    (CC^*)_(x,y) = W_(x,L) W_(y,L)^*.                    (3)

Every off-diagonal block in (3) has squared Hilbert--Schmidt norm
``dim(E_L)``.  Counting six ordered point pairs per line gives the exact,
holonomy-blind identity

    ||CC^*-D||_F^2 = 6 sum_L dim(E_L).                    (4)

Suppose ``D_x >= d_0 I`` on a retained point fiber.  Whitening by ``D`` and
using ``||D_x^-1/2 W_x W_y^* D_y^-1/2||_F^2
<=dim(E_L)/d_0^2`` yields

    ||D^-1/2 CC^* D^-1/2-I||_F^2
      <= 6 sum_L dim(E_L)/d_0^2.                          (5)

Therefore at most the right side divided by ``delta^2`` eigenvalues lie
outside ``[1-delta,1+delta]``.

For a common ``m``-dimensional fiber with unitary incidence maps on every
point, ``D=rI`` and (5) reproduces the scalar constant-outlier theorem with a
trim fraction ``4/(delta^2(v-1))``, independent of ``m`` and of all
nonabelian holonomy.

This reduction identifies the active natural obligation: prove that the
overlapping carrier-channel coverage operators ``D_x`` have a large retained
lower edge relative to their total line-fiber burden.  Support pressure alone
proves overlap is unavoidable but does not establish this coverage edge.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import numpy as np

from research_registry import utc_now
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
    "self_dual_wreath_operator_steiner_bulk_reduction.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-OPERATOR-STEINER-BULK-REDUCTION"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


@dataclass(frozen=True)
class OperatorSteinerFiniteControl:
    control_id: str
    copy_count: int
    line_family: LineFamily
    point_fiber_dimension: int
    line_fiber_dimension: int
    point_count: int
    active_point_count: int
    line_count: int
    total_line_fiber_dimension: int
    minimum_diagonal_coverage_eigenvalue: float
    maximum_diagonal_coverage_eigenvalue: float
    centered_hilbert_schmidt_squared: float
    predicted_centered_hilbert_schmidt_squared: int
    centered_burden_residual: float
    whitened_hilbert_schmidt_squared: float
    whitened_hilbert_schmidt_upper_bound: float
    relative_window_delta: float
    observed_whitened_outlier_count: int
    proved_whitened_outlier_count_bound: float
    exact_operator_burden_verified: bool
    whitened_outlier_bound_respected: bool
    status: str


@dataclass(frozen=True)
class UniformOperatorSteinerScalingRecord:
    copy_count: int
    point_fiber_dimension: int
    point_count: int
    line_count: int
    point_degree: int
    relative_window_delta: float
    spectral_outlier_count_bound: float
    spectral_outlier_rank_fraction_bound: float
    multiplicity_independent_trim_fraction: bool
    status: str


@dataclass(frozen=True)
class OperatorSteinerBulkReductionReport:
    created_at: str
    theorem_contract: dict[str, Any]
    finite_controls: list[OperatorSteinerFiniteControl]
    uniform_scaling: list[UniformOperatorSteinerScalingRecord]
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _line_family(
    copy_count: int,
    line_family: LineFamily,
) -> tuple[tuple[int, int, int], ...]:
    if line_family == "all":
        return projective_steiner_lines(copy_count)
    if line_family == "pattern-rich":
        return pattern_rich_steiner_lines(copy_count)
    raise ValueError("unknown line family")


def _random_isometry(
    row_dimension: int,
    column_dimension: int,
    rng: np.random.Generator,
) -> np.ndarray:
    if not 1 <= column_dimension <= row_dimension:
        raise ValueError("line fiber must embed into point fiber")
    matrix = rng.normal(size=(row_dimension, column_dimension))
    orthogonal, triangular = np.linalg.qr(matrix, mode="reduced")
    signs = np.sign(np.diag(triangular))
    signs[signs == 0] = 1
    return orthogonal * signs


def operator_steiner_incidence(
    copy_count: int,
    line_family: LineFamily,
    point_fiber_dimension: int,
    line_fiber_dimension: int,
    seed: int,
) -> tuple[np.ndarray, np.ndarray, tuple[int, ...]]:
    points = projective_points(copy_count)
    lines = _line_family(copy_count, line_family)
    point_index = {point: index for index, point in enumerate(points)}
    rng = np.random.default_rng(seed)
    incidence = np.zeros(
        (
            len(points) * point_fiber_dimension,
            len(lines) * line_fiber_dimension,
        ),
        dtype=float,
    )
    diagonal = np.zeros(
        (len(points) * point_fiber_dimension,) * 2,
        dtype=float,
    )
    degrees = [0] * len(points)
    for line_index, line in enumerate(lines):
        column_slice = slice(
            line_index * line_fiber_dimension,
            (line_index + 1) * line_fiber_dimension,
        )
        for point in line:
            index = point_index[point]
            row_slice = slice(
                index * point_fiber_dimension,
                (index + 1) * point_fiber_dimension,
            )
            isometry = _random_isometry(
                point_fiber_dimension,
                line_fiber_dimension,
                rng,
            )
            incidence[row_slice, column_slice] = isometry
            diagonal[row_slice, row_slice] += isometry @ isometry.T
            degrees[index] += 1
    active_points = tuple(index for index, degree in enumerate(degrees) if degree)
    active_rows = [
        index * point_fiber_dimension + coordinate
        for index in active_points
        for coordinate in range(point_fiber_dimension)
    ]
    return (
        incidence[np.ix_(active_rows, range(incidence.shape[1]))],
        diagonal[np.ix_(active_rows, active_rows)],
        active_points,
    )


def _positive_inverse_sqrt(
    matrix: np.ndarray,
    *,
    tolerance: float = 1e-10,
) -> tuple[np.ndarray, float, float]:
    values, vectors = np.linalg.eigh((matrix + matrix.T) / 2)
    if values[0] <= tolerance:
        raise ValueError("diagonal coverage is not positive definite")
    inverse = (vectors * (1 / np.sqrt(values))) @ vectors.T
    return inverse, float(values[0]), float(values[-1])


def audit_operator_steiner_control(
    control_id: str,
    copy_count: int,
    line_family: LineFamily,
    point_fiber_dimension: int,
    line_fiber_dimension: int,
    seed: int,
    *,
    delta: float = 0.5,
) -> OperatorSteinerFiniteControl:
    incidence, diagonal, active_points = operator_steiner_incidence(
        copy_count,
        line_family,
        point_fiber_dimension,
        line_fiber_dimension,
        seed,
    )
    lines = _line_family(copy_count, line_family)
    gram = incidence @ incidence.T
    centered = gram - diagonal
    burden = float(np.linalg.norm(centered, ord="fro") ** 2)
    predicted = 6 * len(lines) * line_fiber_dimension
    residual = abs(burden - predicted)
    inverse_sqrt, minimum_coverage, maximum_coverage = _positive_inverse_sqrt(
        diagonal
    )
    whitened = inverse_sqrt @ gram @ inverse_sqrt
    whitened_burden = float(
        np.linalg.norm(whitened - np.eye(whitened.shape[0]), ord="fro") ** 2
    )
    whitened_bound = predicted / minimum_coverage**2
    values = np.linalg.eigvalsh((whitened + whitened.T) / 2)
    outliers = int(
        np.sum(values < 1 - delta - 1e-9)
        + np.sum(values > 1 + delta + 1e-9)
    )
    outlier_bound = whitened_bound / delta**2
    exact = residual <= 1e-8 * max(1, predicted)
    respected = bool(
        whitened_burden <= whitened_bound + 1e-8
        and outliers <= outlier_bound + 1e-9
    )
    return OperatorSteinerFiniteControl(
        control_id=control_id,
        copy_count=copy_count,
        line_family=line_family,
        point_fiber_dimension=point_fiber_dimension,
        line_fiber_dimension=line_fiber_dimension,
        point_count=(1 << copy_count) - 1,
        active_point_count=len(active_points),
        line_count=len(lines),
        total_line_fiber_dimension=len(lines) * line_fiber_dimension,
        minimum_diagonal_coverage_eigenvalue=minimum_coverage,
        maximum_diagonal_coverage_eigenvalue=maximum_coverage,
        centered_hilbert_schmidt_squared=burden,
        predicted_centered_hilbert_schmidt_squared=predicted,
        centered_burden_residual=residual,
        whitened_hilbert_schmidt_squared=whitened_burden,
        whitened_hilbert_schmidt_upper_bound=whitened_bound,
        relative_window_delta=delta,
        observed_whitened_outlier_count=outliers,
        proved_whitened_outlier_count_bound=outlier_bound,
        exact_operator_burden_verified=exact,
        whitened_outlier_bound_respected=respected,
        status=(
            "operator-steiner-burden-and-whitened-trim-verified"
            if exact and respected
            else "operator-steiner-bulk-control-failure"
        ),
    )


def uniform_operator_steiner_scaling_record(
    copy_count: int,
    point_fiber_dimension: int,
    *,
    delta: float = 0.5,
) -> UniformOperatorSteinerScalingRecord:
    if copy_count < 3 or point_fiber_dimension < 1:
        raise ValueError("require K>=3 and positive multiplicity")
    point_count = (1 << copy_count) - 1
    degree = (point_count - 1) // 2
    line_count = point_count * (point_count - 1) // 6
    outliers = 4 * point_count * point_fiber_dimension / (
        delta**2 * (point_count - 1)
    )
    total_dimension = point_count * point_fiber_dimension
    return UniformOperatorSteinerScalingRecord(
        copy_count=copy_count,
        point_fiber_dimension=point_fiber_dimension,
        point_count=point_count,
        line_count=line_count,
        point_degree=degree,
        relative_window_delta=delta,
        spectral_outlier_count_bound=outliers,
        spectral_outlier_rank_fraction_bound=min(
            1.0,
            outliers / total_dimension,
        ),
        multiplicity_independent_trim_fraction=True,
        status="uniform-operator-steiner-bulk-edge-proved",
    )


def run_operator_steiner_bulk_reduction(
) -> OperatorSteinerBulkReductionReport:
    finite_controls = [
        audit_operator_steiner_control(*args)
        for args in (
            ("FULL-K4-Q2-M2", 4, "all", 2, 2, 704),
            ("FULL-K5-Q4-M2", 5, "all", 4, 2, 705),
            ("FULL-K6-Q3-M1", 6, "all", 3, 1, 706),
            ("RICH-K5-Q3-M1", 5, "pattern-rich", 3, 1, 805),
            ("RICH-K6-Q4-M2", 6, "pattern-rich", 4, 2, 806),
        )
    ]
    uniform_scaling = [
        uniform_operator_steiner_scaling_record(copy_count, multiplicity)
        for multiplicity in (1, 4, 64)
        for copy_count in (5, 8, 12, 16, 20, 24)
    ]
    failures = sum(
        not (
            row.exact_operator_burden_verified
            and row.whitened_outlier_bound_respected
        )
        for row in finite_controls
    )
    tail_fractions = {
        row.point_fiber_dimension: row.spectral_outlier_rank_fraction_bound
        for row in uniform_scaling
        if row.copy_count == 24
    }
    return OperatorSteinerBulkReductionReport(
        created_at=utc_now(),
        theorem_contract={
            "operator_incidence_gram": (
                "For arbitrary line-fiber isometries, CC^* has diagonal "
                "coverage D_x=sum_L W_xL W_xL^* and unique-line off-diagonal "
                "blocks W_xL W_yL^*."
            ),
            "exact_hilbert_schmidt_burden": (
                "Holonomy-independently, ||CC^*-D||_F^2=6 sum_L dim(E_L)."
            ),
            "coverage_to_bulk_edge": (
                "If retained D>=d0 I, whitening has squared centered "
                "Hilbert-Schmidt norm at most 6 sum_L dim(E_L)/d0^2."
            ),
            "uniform_fiber_consequence": (
                "For common m-dimensional unitary fibers, the relative outlier "
                "trim is 4/(delta^2(v-1)), independent of m and holonomy."
            ),
            "natural_reduction": (
                "The unresolved natural quantity is the lower spectral coverage "
                "of D relative to total carrier-fiber burden."
            ),
        },
        finite_controls=finite_controls,
        uniform_scaling=uniform_scaling,
        proof_obligations=[
            {
                "obligation": "remove_scalar_sign_restriction_from_bulk_trim",
                "resolved": failures == 0,
                "resolution": (
                    "The exact block Hilbert-Schmidt identity holds for arbitrary "
                    "isometric matrix transports and holonomy."
                ),
            },
            {
                "obligation": "identify_sufficient_diagonal_coverage_condition",
                "resolved": True,
                "resolution": (
                    "A retained lower bound D>=d0I converts directly to the "
                    "whitened constant-outlier estimate."
                ),
            },
            {
                "obligation": "prove_natural_diagonal_coverage_edge",
                "resolved": False,
                "resolution": (
                    "Support pressure proves channels overlap but does not show "
                    "their incidence projectors cover coefficient space evenly."
                ),
            },
            {
                "obligation": "bound_natural_line_fiber_burden_over_coverage_squared",
                "resolved": False,
                "resolution": (
                    "One needs 6 sum dim(E_L)/d0^2=o(total retained dimension) "
                    "after carrier and Plancherel weighting."
                ),
            },
            {
                "obligation": "transfer_coverage_trim_to_physical_pgm_mass",
                "resolved": False,
                "resolution": (
                    "The retained coefficient dimension must be related to the "
                    "post-filter state distribution, not only ambient rank."
                ),
            },
        ],
        adversarial_audit=[
            {
                "objection": "Nonabelian holonomy can increase centered block burden.",
                "resolved": True,
                "resolution": (
                    "It cannot: every off-diagonal block is a product of two "
                    "isometries and has Hilbert-Schmidt square dim(E_L)."
                ),
            },
            {
                "objection": "Matrix multiplicity by itself destroys the vanishing trim fraction.",
                "resolved": True,
                "resolution": (
                    "For uniform fibers both outlier count and ambient dimension "
                    "scale by m, so their ratio is multiplicity-independent."
                ),
            },
            {
                "objection": "Large support demand proves D has a lower edge.",
                "resolved": False,
                "resolution": (
                    "Demand controls trace, while projectors can still align and "
                    "leave a large uncovered complement."
                ),
            },
            {
                "objection": "Finite random isometry controls model natural Racah coverage.",
                "resolved": False,
                "resolution": (
                    "They validate the identity only; natural projectors are "
                    "highly structured and dependent."
                ),
            },
        ],
        headline_metrics={
            "finite_control_count": len(finite_controls),
            "finite_control_failure_count": failures,
            "uniform_scaling_record_count": len(uniform_scaling),
            "tail_multiplicity_one_trim_fraction": tail_fractions[1],
            "tail_multiplicity_four_trim_fraction": tail_fractions[4],
            "tail_multiplicity_sixty_four_trim_fraction": tail_fractions[64],
            "operator_hilbert_schmidt_burden_theorem_count": 1,
            "coverage_to_bulk_edge_reduction_count": 1,
            "natural_diagonal_coverage_theorem_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "operator_centered_burden_exact": failures == 0,
            "arbitrary_holonomy_bulk_reduction_proved": failures == 0,
            "uniform_matrix_fiber_trim_fraction_vanishes": failures == 0,
            "natural_diagonal_coverage_edge_proved": False,
            "natural_weighted_burden_ratio_vanishes": False,
            "pgm_bad_state_mass_controlled": False,
            "collision_free_noncommon_frame_edge_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "Holonomy and matrix multiplicity no longer obstruct the bulk "
                "once diagonal coverage is good; proving natural coverage is "
                "the remaining representation-theoretic bottleneck."
            ),
        },
        status="operator-bulk-reduced-to-natural-diagonal-coverage",
        summary=(
            "Proved an exact operator-valued Hilbert-Schmidt identity and "
            "reduced matrix Steiner bulk conditioning to a lower-edge theorem "
            "for the natural diagonal coverage operator."
        ),
        falsifiers_triggered=[
            (
                "Arbitrary scalar or nonabelian cycle holonomy cannot by itself "
                "create macroscopic bulk outlier rank under good coverage."
            ),
            (
                "Matrix multiplicity is not intrinsically fatal; uneven or "
                "low-rank diagonal coverage is the concrete failure mode."
            ),
            (
                "Future experiments should measure coverage spectra and the "
                "line-fiber-burden/coverage-squared ratio, not cycle signs alone."
            ),
        ],
    )


def write_operator_steiner_bulk_reduction_report(
    path: Path = REPORT_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = (
        "EXP-CODE-SELF-DUAL-WREATH-OPERATOR-STEINER-BULK-REDUCTION"
    ),
    registry_candidate_id: str = "CODE-COSET-COLLECTIVE",
    registry_result_id: str = "",
) -> dict[str, Any]:
    payload = asdict(run_operator_steiner_bulk_reduction())
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
                id="NEG-SELF-DUAL-WREATH-OPERATOR-STEINER-BULK-REDUCTION",
                source=registry_experiment_id,
                claim=(
                    "Initial negative claim for EXP-CODE-SELF-DUAL-WREATH-OPERATOR-STEINER-BULK-REDUCTION."
                ),
                reason_invalid=(
                    "Falsified or refined by exact theorem evaluation."
                ),
                lesson=(
                    "Lesson from exact theorem analysis for EXP-CODE-SELF-DUAL-WREATH-OPERATOR-STEINER-BULK-REDUCTION."
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
                    "self_dual_wreath_operator_steiner_bulk_reduction": str(path)
                },
            )
        )
    return payload


if __name__ == "__main__":
    report = write_operator_steiner_bulk_reduction_report()
    print(json.dumps(report, indent=2, sort_keys=True))

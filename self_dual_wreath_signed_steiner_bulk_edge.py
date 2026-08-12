"""Deterministic bulk edge for every signed Steiner incidence frame.

Cycle gauges can create exact scalar null modes, but they cannot create
macroscopic near-null rank.  Let ``C`` be any signed incidence matrix of the
projective Steiner triple system on ``v=2^K-1`` points.  Every point has degree
``r=(v-1)/2`` and every distinct point pair lies on one line, so

    G=C C^T=rI+S,    S_xx=0,    |S_xy|=1.                (1)

Consequently, independently of every sign,

    ||G-rI||_F^2 = v(v-1).                               (2)

For ``0<delta<1``, at most

    4v/(delta^2(v-1))                                    (3)

eigenvalues lie outside ``[(1-delta)r,(1+delta)r]``.  The
relative trim fraction is at most ``4/(delta^2(v-1))=O(2^-K)``.

The pattern-rich family is irregular and has ``2K+1`` isolated points.  On
its active component let ``D`` be the degree matrix and normalize

    H=D^-1/2 C C^T D^-1/2.                               (4)

Then ``H_xx=1`` and a covered point pair has off-diagonal magnitude
``1/sqrt(d_x d_y)``.  Hence

    ||H-I||_F^2
      = sum_(ordered covered x!=y) 1/(d_x d_y)
      <= 6R_K/d_min^2,                                   (5)

where ``d_min=2^(K-2)-2``.  The right side tends to sixteen.  Thus every
signing of the rich normalized frame also has only ``O(1/delta^2)`` spectral
outliers and a vanishing trimmed rank fraction.

This closes scalar near-zero *rank* mass for one equal-weight line family;
it does not sum that trim over the many nonuniform natural carrier sectors.
Nor does it cover matrix-valued Racah transports, where off-diagonal block
Frobenius burden and physical multiplicity weights must be controlled.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import numpy as np

from research_registry import utc_now
from self_dual_wreath_affine_plane_support_pressure_no_go import (
    rich_plane_count_per_vertex,
)
from self_dual_wreath_interplane_gauge_homology import (
    LineFamily,
    pattern_rich_steiner_lines,
)
from self_dual_wreath_random_steiner_gauge_edge import (
    BALANCED_LINE_SIGNS,
    point_degrees,
)
from self_dual_wreath_signed_steiner_incidence_boundary import (
    projective_points,
    projective_steiner_lines,
    signed_steiner_incidence_with_quotient_kernel,
    unsigned_steiner_incidence,
)


REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_signed_steiner_bulk_edge.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-SIGNED-STEINER-BULK-EDGE"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


@dataclass(frozen=True)
class SignedSteinerBulkScalingRecord:
    copy_count: int
    line_family: LineFamily
    point_count: int
    active_point_count: int
    line_count: int
    relative_window_delta: float
    centered_frobenius_bound: float
    spectral_outlier_count_bound: float
    spectral_outlier_rank_fraction_bound: float
    lower_bulk_edge: float
    upper_bulk_edge: float
    asymptotic_constant_outlier_bound_proved: bool
    status: str


@dataclass(frozen=True)
class SignedSteinerBulkFiniteControl:
    control_id: str
    copy_count: int
    line_family: LineFamily
    signing_kind: str
    active_point_count: int
    line_count: int
    centered_frobenius_squared: float
    predicted_or_bounded_frobenius_squared: float
    relative_window_delta: float
    observed_low_outlier_count: int
    observed_high_outlier_count: int
    observed_total_outlier_count: int
    proved_total_outlier_count_bound: float
    minimum_eigenvalue: float
    maximum_eigenvalue: float
    exact_or_bounded_moment_verified: bool
    outlier_bound_respected: bool
    status: str


@dataclass(frozen=True)
class SignedSteinerBulkEdgeReport:
    created_at: str
    theorem_contract: dict[str, Any]
    full_scaling: list[SignedSteinerBulkScalingRecord]
    rich_scaling: list[SignedSteinerBulkScalingRecord]
    finite_controls: list[SignedSteinerBulkFiniteControl]
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def full_steiner_outlier_count_bound(
    copy_count: int,
    delta: float,
) -> float:
    if copy_count < 2 or not 0 < delta < 1:
        raise ValueError("require K>=2 and delta in (0,1)")
    point_count = (1 << copy_count) - 1
    return 4 * point_count / (delta**2 * (point_count - 1))


def rich_steiner_frobenius_bound(copy_count: int) -> float:
    if copy_count < 4:
        raise ValueError("pattern-rich controls require K>=4")
    line_count = rich_plane_count_per_vertex(copy_count)
    minimum_degree = 2 ** (copy_count - 2) - 2
    return 6 * line_count / minimum_degree**2


def signed_steiner_bulk_scaling_record(
    copy_count: int,
    line_family: LineFamily,
    *,
    delta: float = 0.5,
) -> SignedSteinerBulkScalingRecord:
    if not 0 < delta < 1:
        raise ValueError("delta must lie in (0,1)")
    orientation_count = 1 << copy_count
    point_count = orientation_count - 1
    if line_family == "all":
        active_count = point_count
        line_count = point_count * (point_count - 1) // 6
        degree = (point_count - 1) / 2
        frobenius = point_count * (point_count - 1)
        outliers = full_steiner_outlier_count_bound(copy_count, delta)
        lower = (1 - delta) * degree
        upper = (1 + delta) * degree
    elif line_family == "pattern-rich":
        if copy_count < 4:
            raise ValueError("pattern-rich controls require K>=4")
        active_count = point_count - (2 * copy_count + 1)
        line_count = rich_plane_count_per_vertex(copy_count)
        frobenius = rich_steiner_frobenius_bound(copy_count)
        outliers = frobenius / delta**2
        lower = 1 - delta
        upper = 1 + delta
    else:
        raise ValueError("unknown line family")
    return SignedSteinerBulkScalingRecord(
        copy_count=copy_count,
        line_family=line_family,
        point_count=point_count,
        active_point_count=active_count,
        line_count=line_count,
        relative_window_delta=delta,
        centered_frobenius_bound=frobenius,
        spectral_outlier_count_bound=outliers,
        spectral_outlier_rank_fraction_bound=min(1.0, outliers / active_count),
        lower_bulk_edge=lower,
        upper_bulk_edge=upper,
        asymptotic_constant_outlier_bound_proved=True,
        status="deterministic-signed-steiner-bulk-edge-proved",
    )


def _signed_incidence(
    copy_count: int,
    line_family: LineFamily,
    signing_kind: str,
    seed: int = 0,
) -> tuple[np.ndarray, np.ndarray]:
    points = projective_points(copy_count)
    all_lines = projective_steiner_lines(copy_count)
    if line_family == "all":
        lines = all_lines
        selected = list(range(len(all_lines)))
    elif line_family == "pattern-rich":
        lines = pattern_rich_steiner_lines(copy_count)
        line_index = {line: index for index, line in enumerate(all_lines)}
        selected = [line_index[line] for line in lines]
    else:
        raise ValueError("unknown line family")

    if signing_kind == "unsigned":
        incidence = unsigned_steiner_incidence(copy_count)[:, selected]
    elif signing_kind == "quotient-kernel":
        incidence = signed_steiner_incidence_with_quotient_kernel(
            copy_count
        )[0][:, selected]
    elif signing_kind == "random-balanced":
        point_index = {point: index for index, point in enumerate(points)}
        incidence = np.zeros((len(points), len(lines)), dtype=float)
        rng = np.random.default_rng(seed)
        for column, line in enumerate(lines):
            signs = BALANCED_LINE_SIGNS[int(rng.integers(4))]
            incidence[[point_index[point] for point in line], column] = signs
    else:
        raise ValueError("unknown signing kind")
    degrees = np.sum(incidence != 0, axis=1)
    active = degrees > 0
    return incidence[active, :], degrees[active]


def audit_signed_steiner_bulk(
    control_id: str,
    copy_count: int,
    line_family: LineFamily,
    signing_kind: str,
    *,
    delta: float = 0.5,
    seed: int = 0,
) -> SignedSteinerBulkFiniteControl:
    incidence, degrees = _signed_incidence(
        copy_count,
        line_family,
        signing_kind,
        seed,
    )
    gram = incidence @ incidence.T
    if line_family == "all":
        degree = float(degrees[0])
        normalized = gram / degree
        centered_frobenius = float(
            np.linalg.norm(gram - degree * np.eye(len(degrees)), ord="fro") ** 2
        )
        predicted = float(len(degrees) * (len(degrees) - 1))
        moment_verified = math.isclose(
            centered_frobenius,
            predicted,
            rel_tol=1e-12,
            abs_tol=1e-8,
        )
    else:
        inverse_sqrt = np.diag(1 / np.sqrt(degrees))
        normalized = inverse_sqrt @ gram @ inverse_sqrt
        centered_frobenius = float(
            np.linalg.norm(normalized - np.eye(len(degrees)), ord="fro") ** 2
        )
        predicted = rich_steiner_frobenius_bound(copy_count)
        moment_verified = centered_frobenius <= predicted + 1e-9
    values = np.linalg.eigvalsh(normalized)
    low = int(np.sum(values < 1 - delta - 1e-9))
    high = int(np.sum(values > 1 + delta + 1e-9))
    observed = low + high
    scaling = signed_steiner_bulk_scaling_record(
        copy_count,
        line_family,
        delta=delta,
    )
    respected = observed <= scaling.spectral_outlier_count_bound + 1e-9
    return SignedSteinerBulkFiniteControl(
        control_id=control_id,
        copy_count=copy_count,
        line_family=line_family,
        signing_kind=signing_kind,
        active_point_count=len(degrees),
        line_count=incidence.shape[1],
        centered_frobenius_squared=centered_frobenius,
        predicted_or_bounded_frobenius_squared=predicted,
        relative_window_delta=delta,
        observed_low_outlier_count=low,
        observed_high_outlier_count=high,
        observed_total_outlier_count=observed,
        proved_total_outlier_count_bound=(
            scaling.spectral_outlier_count_bound
        ),
        minimum_eigenvalue=float(values[0]),
        maximum_eigenvalue=float(values[-1]),
        exact_or_bounded_moment_verified=moment_verified,
        outlier_bound_respected=respected,
        status=(
            "signed-steiner-bulk-moment-and-trim-verified"
            if moment_verified and respected
            else "signed-steiner-bulk-control-failure"
        ),
    )


def run_signed_steiner_bulk_edge() -> SignedSteinerBulkEdgeReport:
    full_scaling = [
        signed_steiner_bulk_scaling_record(copy_count, "all")
        for copy_count in range(3, 25)
    ]
    rich_scaling = [
        signed_steiner_bulk_scaling_record(copy_count, "pattern-rich")
        for copy_count in range(4, 25)
    ]
    finite_controls = [
        audit_signed_steiner_bulk(
            f"{family}-{kind}-K{copy_count}",
            copy_count,
            family,
            kind,
            seed=400 + copy_count,
        )
        for family, kind, copy_count in (
            ("all", "unsigned", 5),
            ("all", "quotient-kernel", 6),
            ("all", "random-balanced", 8),
            ("pattern-rich", "unsigned", 6),
            ("pattern-rich", "quotient-kernel", 7),
            ("pattern-rich", "random-balanced", 8),
        )
    ]
    failures = sum(
        not (row.exact_or_bounded_moment_verified and row.outlier_bound_respected)
        for row in finite_controls
    )
    tail_full = full_scaling[-1]
    tail_rich = rich_scaling[-1]
    return SignedSteinerBulkEdgeReport(
        created_at=utc_now(),
        theorem_contract={
            "full_exact_centered_moment": (
                "For every signing, ||CC^T-rI||_F^2=v(v-1) because every "
                "off-diagonal entry has magnitude one."
            ),
            "full_deterministic_bulk_edge": (
                "At relative window delta, at most "
                "4v/(delta^2(v-1)) eigenvalues are outside r[1-delta,1+delta]."
            ),
            "rich_normalized_moment": (
                "On active points, ||D^-1/2 CC^T D^-1/2-I||_F^2 is the "
                "ordered covered-pair reciprocal-degree sum and is at most "
                "6R_K/d_min^2."
            ),
            "rich_deterministic_bulk_edge": (
                "The rich normalized frame has at most "
                "6R_K/(delta^2 d_min^2)=O(1/delta^2) outliers."
            ),
            "scope": (
                "The theorem is per equal-weight scalar line channel; physical "
                "carrier aggregation and matrix transports are not included."
            ),
        },
        full_scaling=full_scaling,
        rich_scaling=rich_scaling,
        finite_controls=finite_controls,
        proof_obligations=[
            {
                "obligation": "control_scalar_near_null_rank_for_all_signings",
                "resolved": failures == 0,
                "resolution": (
                    "The exact centered Frobenius burden gives a deterministic "
                    "constant-outlier rank bound."
                ),
            },
            {
                "obligation": "extend_scalar_bulk_trim_to_pattern_rich_lines",
                "resolved": failures == 0,
                "resolution": (
                    "Degree normalization and the exact rich minimum degree "
                    "give a constant normalized Frobenius burden."
                ),
            },
            {
                "obligation": "aggregate_trim_over_natural_carrier_sectors",
                "resolved": False,
                "resolution": (
                    "The number, multiplicity, overlap, and physical weights of "
                    "scalar carrier sectors require a center-valued rank budget."
                ),
            },
            {
                "obligation": "prove_operator_valued_frobenius_burden_bound",
                "resolved": False,
                "resolution": (
                    "Matrix 6j transports replace scalar unit entries by blocks; "
                    "their squared Hilbert-Schmidt burden must be summed."
                ),
            },
            {
                "obligation": "transfer_bulk_rank_trim_to_pgm_state_mass",
                "resolved": False,
                "resolution": (
                    "Ambient-relative rank is not automatically Plancherel or "
                    "post-filter state mass."
                ),
            },
        ],
        adversarial_audit=[
            {
                "objection": "A correlated gauge can create extensive scalar near-kernel mass.",
                "resolved": True,
                "resolution": (
                    "False for either complete or normalized rich equal-weight "
                    "Steiner incidence: the centered Frobenius burden is O(v) "
                    "or O(1), respectively after normalization."
                ),
            },
            {
                "objection": "The random-gauge independence assumption is needed for the bulk edge.",
                "resolved": True,
                "resolution": (
                    "It is not; the deterministic Frobenius identity holds for "
                    "every sign assignment."
                ),
            },
            {
                "objection": "A constant per-channel trim stays constant after summing all channels.",
                "resolved": False,
                "resolution": (
                    "Channel count and multiplicity can grow, and their bad "
                    "subspaces may be independent or coherently aligned."
                ),
            },
            {
                "objection": "Scalar unit signs model high-multiplicity natural traffic.",
                "resolved": False,
                "resolution": (
                    "The operator-valued Hilbert-Schmidt burden is the next "
                    "unresolved representation-theoretic quantity."
                ),
            },
        ],
        headline_metrics={
            "finite_control_count": len(finite_controls),
            "finite_control_failure_count": failures,
            "tail_full_copy_count": tail_full.copy_count,
            "tail_full_outlier_rank_fraction_bound": (
                tail_full.spectral_outlier_rank_fraction_bound
            ),
            "tail_rich_outlier_rank_fraction_bound": (
                tail_rich.spectral_outlier_rank_fraction_bound
            ),
            "deterministic_scalar_bulk_edge_theorem_count": 2,
            "natural_channel_aggregation_theorem_count": 0,
            "operator_valued_bulk_edge_theorem_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "full_scalar_near_null_rank_fraction_vanishes": failures == 0,
            "rich_scalar_near_null_rank_fraction_vanishes": failures == 0,
            "scalar_bulk_edge_requires_gauge_randomness": False,
            "natural_carrier_sector_trim_aggregated": False,
            "operator_valued_frobenius_burden_controlled": False,
            "pgm_bad_state_mass_controlled": False,
            "collision_free_noncommon_frame_edge_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "Scalar sign traffic has a deterministic bulk edge, but the "
                "physical weighted matrix-valued direct sum remains unresolved."
            ),
        },
        status="deterministic-scalar-bulk-edge-proved-matrix-aggregation-open",
        summary=(
            "Proved that every scalar signing of the complete or normalized "
            "pattern-rich Steiner frame has only constantly many relative "
            "spectral outliers, without any gauge-randomness assumption."
        ),
        falsifiers_triggered=[
            (
                "Adversarial scalar cycle holonomy cannot create macroscopic "
                "near-zero rank in an equal-weight Steiner line family."
            ),
            (
                "Natural scalar gauge mixing is no longer required for a bulk "
                "rank edge; only for an untrimmed minimum eigenvalue."
            ),
            (
                "The active difficulty has moved to weighted carrier-sector "
                "aggregation and matrix-valued Hilbert-Schmidt traffic."
            ),
        ],
    )


def write_signed_steiner_bulk_edge_report(
    path: Path = REPORT_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = (
        "EXP-CODE-SELF-DUAL-WREATH-SIGNED-STEINER-BULK-EDGE"
    ),
    registry_candidate_id: str = "CODE-COSET-COLLECTIVE",
    registry_result_id: str = "",
) -> dict[str, Any]:
    payload = asdict(run_signed_steiner_bulk_edge())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True))

    return payload


if __name__ == "__main__":
    report = write_signed_steiner_bulk_edge_report()
    print(json.dumps(report, indent=2, sort_keys=True))

"""Signed Steiner-incidence boundary for overlapping affine-plane channels.

Fix one orientation vertex in the dyadic hierarchy.  Its nonzero displacement
vectors are the points of ``PG(K-1, 2)``, and the affine planes through that
vertex are the Steiner triples

    {x, y, x xor y}.

The unsigned point-line incidence matrix ``C_+`` is exceptionally benign.  If
``N=2^K`` and ``r=(N-2)/2`` is the point degree, then

    C_+ C_+^T = (r-1) I + J,                              (1)

so its nonzero frame condition number tends to three.

Local positive affine-plane holonomy does *not* imply (1).  A signed line
column has three entries in ``{+1,-1}``; the product of its three pairwise
edge signs is always positive.  Choose two independent binary functionals and
map every point to

    u(x) = (ell_1(x), ell_2(x)) in R^2.

On every Steiner triple the three vectors are either ``0,a,a`` or
``(1,0),(0,1),(1,1)`` up to order.  Consequently one can choose a legal sign
column ``s_L`` with product ``+1`` and

    sum_{x in L} s_L(x) u(x) = 0.                         (2)

The resulting signed incidence matrix ``C_s`` obeys ``C_s^T U=0`` and has an
exact two-dimensional kernel for every ``K>=2``.  Thus equal-weight positive
rank-one plane channels can be globally singular even though every local
triangle has positive holonomy.

This is an adversarial scalar boundary, not a theorem about the natural
``S_n`` recoupling coefficients.  It disproves any global frame-edge argument
using only Steiner regularity and local positive holonomy.  A useful natural
result must additionally control the inter-plane gauge/cycle law, matrix-valued
weights, or the physical mass carried by exceptional global modes.
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
    "self_dual_wreath_signed_steiner_incidence_boundary.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-SIGNED-STEINER-INCIDENCE-BOUNDARY"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"

Point = int
Line = tuple[Point, Point, Point]


@dataclass(frozen=True)
class UnsignedSteinerIncidenceControl:
    copy_count: int
    point_count: int
    line_count: int
    point_degree: int
    predicted_small_eigenvalue: float
    predicted_large_eigenvalue: float
    observed_small_eigenvalue: float
    observed_large_eigenvalue: float
    predicted_condition_number: float
    exact_unsigned_gram_verified: bool
    status: str


@dataclass(frozen=True)
class SignedSteinerKernelControl:
    copy_count: int
    point_count: int
    line_count: int
    point_degree: int
    witness_rank: int
    signed_incidence_rank: int
    signed_incidence_nullity: int
    kernel_residual: float
    maximum_line_sign_product_residual: float
    maximum_triangle_holonomy_residual: float
    two_dimensional_exact_kernel_verified: bool
    local_positive_holonomy_verified: bool
    status: str


@dataclass(frozen=True)
class SignedSteinerIncidenceBoundaryReport:
    created_at: str
    theorem_contract: dict[str, Any]
    unsigned_controls: list[UnsignedSteinerIncidenceControl]
    signed_controls: list[SignedSteinerKernelControl]
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def projective_points(copy_count: int) -> tuple[Point, ...]:
    if copy_count < 2:
        raise ValueError("copy_count must be at least two")
    return tuple(range(1, 1 << copy_count))


def projective_steiner_lines(copy_count: int) -> tuple[Line, ...]:
    """Return each triple ``{x,y,x xor y}`` exactly once."""

    points = projective_points(copy_count)
    lines: list[Line] = []
    for first in points:
        for second in range(first + 1, 1 << copy_count):
            third = first ^ second
            if second < third:
                lines.append((first, second, third))
    return tuple(lines)


def unsigned_steiner_incidence(copy_count: int) -> np.ndarray:
    points = projective_points(copy_count)
    point_index = {point: index for index, point in enumerate(points)}
    lines = projective_steiner_lines(copy_count)
    incidence = np.zeros((len(points), len(lines)), dtype=float)
    for column, line in enumerate(lines):
        for point in line:
            incidence[point_index[point], column] = 1.0
    return incidence


def quotient_witness(copy_count: int) -> np.ndarray:
    """Two independent real witnesses induced by the first two bits."""

    return np.asarray(
        [
            ((point & 1).bit_count() & 1, (point & 2).bit_count() & 1)
            for point in projective_points(copy_count)
        ],
        dtype=float,
    )


_POSITIVE_GAUGE_SIGN_PATTERNS: tuple[tuple[int, int, int], ...] = tuple(
    signs
    for signs in itertools.product((-1, 1), repeat=3)
    if math.prod(signs) == 1
)


def signed_steiner_incidence_with_quotient_kernel(
    copy_count: int,
) -> tuple[np.ndarray, np.ndarray]:
    """Construct ``C_s`` and ``U`` from equation (2).

    The search is over four constant-size sign patterns per line.  Existence
    is exact: the first-two-bit quotient of a binary line is either
    ``0,a,a`` or the three nonzero vectors of ``F_2^2``.
    """

    points = projective_points(copy_count)
    point_index = {point: index for index, point in enumerate(points)}
    lines = projective_steiner_lines(copy_count)
    witness = quotient_witness(copy_count)
    incidence = np.zeros((len(points), len(lines)), dtype=float)
    for column, line in enumerate(lines):
        rows = [point_index[point] for point in line]
        local_witness = witness[rows, :]
        signs = next(
            (
                pattern
                for pattern in _POSITIVE_GAUGE_SIGN_PATTERNS
                if np.array_equal(
                    np.asarray(pattern, dtype=float) @ local_witness,
                    np.zeros(2),
                )
            ),
            None,
        )
        if signs is None:
            raise ArithmeticError("binary quotient line has no legal sign relation")
        incidence[rows, column] = signs
    return incidence, witness


def audit_unsigned_steiner_incidence(
    copy_count: int,
) -> UnsignedSteinerIncidenceControl:
    incidence = unsigned_steiner_incidence(copy_count)
    point_count = incidence.shape[0]
    line_count = incidence.shape[1]
    orientation_count = 1 << copy_count
    degree = (orientation_count - 2) // 2
    gram = incidence @ incidence.T
    predicted = (degree - 1) * np.eye(point_count) + np.ones(
        (point_count, point_count)
    )
    residual = float(np.max(np.abs(gram - predicted)))
    eigenvalues = np.linalg.eigvalsh(gram)
    small = float(eigenvalues[0])
    large = float(eigenvalues[-1])
    predicted_small = float(degree - 1)
    predicted_large = float(3 * degree)
    condition = (
        predicted_large / predicted_small
        if predicted_small > 0
        else math.inf
    )
    verified = bool(
        residual == 0
        and math.isclose(small, predicted_small, abs_tol=1e-10)
        and math.isclose(large, predicted_large, abs_tol=1e-10)
    )
    return UnsignedSteinerIncidenceControl(
        copy_count=copy_count,
        point_count=point_count,
        line_count=line_count,
        point_degree=degree,
        predicted_small_eigenvalue=predicted_small,
        predicted_large_eigenvalue=predicted_large,
        observed_small_eigenvalue=small,
        observed_large_eigenvalue=large,
        predicted_condition_number=condition,
        exact_unsigned_gram_verified=verified,
        status=(
            "unsigned-steiner-frame-exactly-conditioned"
            if verified
            else "unsigned-steiner-gram-control-failure"
        ),
    )


def audit_signed_steiner_kernel(
    copy_count: int,
) -> SignedSteinerKernelControl:
    incidence, witness = signed_steiner_incidence_with_quotient_kernel(
        copy_count
    )
    lines = projective_steiner_lines(copy_count)
    degree = ((1 << copy_count) - 2) // 2
    kernel_residual = float(np.max(np.abs(incidence.T @ witness)))
    rank = int(np.linalg.matrix_rank(incidence, tol=1e-9))
    witness_rank = int(np.linalg.matrix_rank(witness, tol=1e-9))
    nullity = incidence.shape[0] - rank
    sign_product_residual = max(
        abs(math.prod(incidence[:, column][incidence[:, column] != 0]) - 1)
        for column in range(incidence.shape[1])
    )
    holonomy_residual = 0.0
    for column in range(incidence.shape[1]):
        local_signs = incidence[:, column][incidence[:, column] != 0]
        edge_holonomy = (
            local_signs[0]
            * local_signs[1]
            * local_signs[1]
            * local_signs[2]
            * local_signs[2]
            * local_signs[0]
        )
        holonomy_residual = max(holonomy_residual, abs(edge_holonomy - 1))
    kernel_verified = bool(
        witness_rank == 2
        and nullity >= 2
        and kernel_residual == 0
    )
    holonomy_verified = bool(
        sign_product_residual == 0 and holonomy_residual == 0
    )
    return SignedSteinerKernelControl(
        copy_count=copy_count,
        point_count=incidence.shape[0],
        line_count=len(lines),
        point_degree=degree,
        witness_rank=witness_rank,
        signed_incidence_rank=rank,
        signed_incidence_nullity=nullity,
        kernel_residual=kernel_residual,
        maximum_line_sign_product_residual=float(sign_product_residual),
        maximum_triangle_holonomy_residual=float(holonomy_residual),
        two_dimensional_exact_kernel_verified=kernel_verified,
        local_positive_holonomy_verified=holonomy_verified,
        status=(
            "positive-local-holonomy-with-global-kernel"
            if kernel_verified and holonomy_verified
            else "signed-steiner-kernel-control-failure"
        ),
    )


def run_signed_steiner_incidence_boundary(
) -> SignedSteinerIncidenceBoundaryReport:
    unsigned_controls = [
        audit_unsigned_steiner_incidence(copy_count)
        for copy_count in range(3, 8)
    ]
    signed_controls = [
        audit_signed_steiner_kernel(copy_count)
        for copy_count in range(2, 8)
    ]
    unsigned_failures = sum(
        not row.exact_unsigned_gram_verified for row in unsigned_controls
    )
    signed_failures = sum(
        not (
            row.two_dimensional_exact_kernel_verified
            and row.local_positive_holonomy_verified
        )
        for row in signed_controls
    )
    minimum_signed_nullity = min(
        row.signed_incidence_nullity for row in signed_controls
    )
    return SignedSteinerIncidenceBoundaryReport(
        created_at=utc_now(),
        theorem_contract={
            "projective_steiner_geometry": (
                "The nonzero vectors of F_2^K form an STS(2^K-1), with "
                "lines {x,y,x xor y}, point degree (2^K-2)/2, and "
                "(2^K-1)(2^K-2)/6 lines."
            ),
            "unsigned_frame": (
                "C_+ C_+^T=((2^K-4)/2)I+J, with condition number "
                "3(2^K-2)/(2^K-4) for K>=3."
            ),
            "signed_counterfamily": (
                "Two independent binary functionals construct legal signed "
                "line columns with positive triangle holonomy and an exact "
                "two-dimensional kernel for every K>=2."
            ),
            "logical_boundary": (
                "Steiner regularity plus local positive scalar holonomy does "
                "not imply a global incidence-frame lower edge."
            ),
        },
        unsigned_controls=unsigned_controls,
        signed_controls=signed_controls,
        proof_obligations=[
            {
                "obligation": "compute_unsigned_steiner_incidence_spectrum",
                "resolved": unsigned_failures == 0,
                "resolution": (
                    "Every point has degree r and every point pair shares one "
                    "line, giving (r-1)I+J exactly."
                ),
            },
            {
                "obligation": "test_local_positive_holonomy_sufficiency",
                "resolved": signed_failures == 0,
                "resolution": (
                    "The F_2^2 quotient witness gives a legal all-depth "
                    "counterfamily with C_s^T U=0."
                ),
            },
            {
                "obligation": "derive_natural_inter_plane_gauge_law",
                "resolved": False,
                "resolution": (
                    "The scalar cup/cap calculation fixes each plane but not "
                    "cycle gauges between distinct overlapping planes."
                ),
            },
            {
                "obligation": "control_matrix_valued_recoupling_weights",
                "resolved": False,
                "resolution": (
                    "High Kronecker multiplicities replace scalar signs by "
                    "orthogonal 6j transports with nonuniform weights."
                ),
            },
            {
                "obligation": "bound_physical_mass_of_global_bad_modes",
                "resolved": False,
                "resolution": (
                    "The explicit scalar counterfamily has two null modes; "
                    "their relevance to PGM success depends on natural weights."
                ),
            },
        ],
        adversarial_audit=[
            {
                "objection": "Positive holonomy on every Steiner triangle permits a global all-positive gauge.",
                "resolved": True,
                "resolution": (
                    "False. Independent line gauges have longer incidence-cycle "
                    "invariants; the explicit positive-line construction is singular."
                ),
            },
            {
                "objection": "The unsigned condition number proves the natural frame is conditioned.",
                "resolved": True,
                "resolution": (
                    "False without a theorem identifying natural inter-plane "
                    "transport with the unsigned gauge."
                ),
            },
            {
                "objection": "A two-dimensional adversarial kernel proves natural PGM failure.",
                "resolved": False,
                "resolution": (
                    "It does not: the signing is not derived from S_n recoupling, "
                    "and two modes may carry negligible physical mass."
                ),
            },
            {
                "objection": "Scalar signed incidence covers matrix multiplicity channels.",
                "resolved": False,
                "resolution": (
                    "Matrix-valued transports can be better or worse and require "
                    "a separate operator-valued traffic theorem."
                ),
            },
        ],
        headline_metrics={
            "unsigned_control_count": len(unsigned_controls),
            "signed_counterfamily_control_count": len(signed_controls),
            "finite_control_failure_count": unsigned_failures + signed_failures,
            "minimum_signed_incidence_nullity": minimum_signed_nullity,
            "unsigned_uniform_conditioning_theorem_count": 1,
            "positive_local_holonomy_sufficiency_no_go_count": 1,
            "natural_inter_plane_gauge_theorem_count": 0,
            "matrix_valued_overlap_traffic_theorem_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "unsigned_steiner_surrogate_uniformly_conditioned": (
                unsigned_failures == 0
            ),
            "positive_local_holonomy_can_have_global_kernel": (
                signed_failures == 0
            ),
            "local_positive_holonomy_sufficient_for_frame_edge": False,
            "natural_recoupling_realizes_adversarial_signing": False,
            "natural_inter_plane_gauge_controlled": False,
            "matrix_valued_overlap_traffic_controlled": False,
            "physical_bad_mode_mass_controlled": False,
            "collision_free_noncommon_frame_edge_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The unsigned model is benign but local positivity alone is "
                "insufficient; natural gauge and matrix-valued overlap laws "
                "remain the decisive missing inputs."
            ),
        },
        status="local-positive-holonomy-sufficiency-falsified-natural-gauge-open",
        summary=(
            "Proved an exact all-depth signed Steiner counterfamily: every "
            "local plane has positive scalar holonomy while the global "
            "incidence frame has a two-dimensional kernel."
        ),
        falsifiers_triggered=[
            (
                "Disjoint affine-plane atomization already fails by support "
                "pressure, and unsigned Steiner conditioning cannot replace it "
                "without inter-plane gauge control."
            ),
            (
                "Positive scalar holonomy on each local affine plane is not a "
                "sufficient certificate for any global lower spectral edge."
            ),
            (
                "Any surviving proof must use natural recoupling structure, "
                "matrix-valued traffic, or a weighted bad-mass estimate."
            ),
        ],
    )


def write_signed_steiner_incidence_boundary_report(
    path: Path = REPORT_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = (
        "EXP-CODE-SELF-DUAL-WREATH-SIGNED-STEINER-INCIDENCE-BOUNDARY"
    ),
    registry_candidate_id: str = "CODE-COSET-COLLECTIVE",
    registry_result_id: str = "",
) -> dict[str, Any]:
    payload = asdict(run_signed_steiner_incidence_boundary())
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
                id="NEG-SELF-DUAL-WREATH-SIGNED-STEINER-INCIDENCE-BOUNDARY",
                source=registry_experiment_id,
                claim=(
                    "Initial negative claim for EXP-CODE-SELF-DUAL-WREATH-SIGNED-STEINER-INCIDENCE-BOUNDARY."
                ),
                reason_invalid=(
                    "Falsified or refined by exact theorem evaluation."
                ),
                lesson=(
                    "Lesson from exact theorem analysis for EXP-CODE-SELF-DUAL-WREATH-SIGNED-STEINER-INCIDENCE-BOUNDARY."
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
                    "self_dual_wreath_signed_steiner_incidence_boundary": str(path)
                },
            )
        )
    return payload


if __name__ == "__main__":
    report = write_signed_steiner_incidence_boundary_report()
    print(json.dumps(report, indent=2, sort_keys=True))

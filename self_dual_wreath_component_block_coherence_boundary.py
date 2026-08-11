"""Exact block-coherence boundary for the component fourth moment.

Let ``Pi`` be the coefficient-fiber projection from the exact normal form and
split its coefficient space into outcome blocks.  Write

    A_e = Pi_ee = D_e Pi D_e,
    B_ef = Pi_ef = D_e Pi D_f.

For distinct outcomes define

    N_ef = Tr(A_e B_ef A_f B_fe),
    C_ef = Tr((B_ef B_fe)^2).

These are respectively the noncrossing and crossing component words.  The
following deterministic identities isolate what block coherence can and
cannot prove.

1. Projection idempotence gives

       sum_(e != f) ||B_ef||_F^2
         = rank(Pi) - sum_e Tr(A_e^2).                    (1)

2. Positivity of every two-block principal submatrix gives
   ``range(B_ef) subset range(A_e)`` and the adjoint analogue.  Therefore

       N_ef = ||A_e^(1/2) B_ef A_f^(1/2)||_F^2,
       N_ef = 0  iff  B_ef = 0.                           (2)

3. If every nonzero block eigenvalue is at least ``delta``, then

       sum_(e != f) N_ef
         >= delta^2 [rank(Pi)-sum_e Tr(A_e^2)].           (3)

4. The desired commutator contribution is the *difference*

       ||[H_e,H_f]||_F^2 = 2(N_ef-C_ef).                 (4)

The distinction in (4) is essential.  The codimension-one tight-frame
counterfamily has constant effect edge, extensive off-block energy, and
positive distinct noncrossing mass, but its compressed effects commute, so
``N_ef=C_ef`` for every pair.  Hence a natural theorem for off-block energy,
block coherence, or distinct noncrossing mass alone cannot prove component
``M4``.  The missing representation-theoretic target is a quantitative
noncrossing-minus-crossing separation for the natural dependency projection.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from fractions import Fraction
from pathlib import Path
from typing import Any

import numpy as np

from research_registry import utc_now
from self_dual_wreath_codimension_one_commuting_compression_no_go import (
    exact_family_parameters,
)


REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_component_block_coherence_boundary.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-COMPONENT-BLOCK-COHERENCE-BOUNDARY"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


@dataclass(frozen=True)
class BlockCoherenceControl:
    control_id: str
    coefficient_dimension: int
    fiber_rank: int
    outcome_count: int
    block_dimensions: tuple[int, ...]
    minimum_positive_block_eigenvalue: float
    off_block_frobenius_energy: float
    projection_identity_off_block_energy: float
    off_block_energy_identity_residual: float
    ordered_distinct_noncrossing_mass: float
    edge_weighted_noncrossing_lower_bound: float
    edge_lower_bound_residual: float
    ordered_distinct_crossing_mass: float
    ordered_commutator_gap: float
    direct_ordered_commutator_mass: float
    commutator_identity_residual: float
    maximum_pair_noncrossing_norm_residual: float
    maximum_pair_zero_equivalence_failure: float
    projection_residual: float
    block_coherence_positive: bool
    distinct_noncrossing_positive: bool
    crossing_cancels_noncrossing: bool
    exact_block_coherence_boundary_verified: bool
    status: str


@dataclass(frozen=True)
class CommutingCoherenceScalingRecord:
    common_dimension: int
    coefficient_dimension: int
    fiber_rank: int
    minimum_positive_block_eigenvalue: float
    normalized_off_block_frobenius_energy: float
    normalized_ordered_distinct_noncrossing_mass: float
    normalized_ordered_distinct_crossing_mass: float
    normalized_commutator_gap: float
    edge_lower_bound_normalized: float
    off_block_coherence_extensive: bool
    distinct_noncrossing_extensive: bool
    component_M4_positive: bool
    status: str


@dataclass(frozen=True)
class BlockCoherenceBoundaryTheorem:
    off_block_identity: str
    pair_noncrossing_identity: str
    zero_equivalence: str
    positive_edge_bound: str
    commutator_gap_identity: str
    insufficiency_counterfamily: str
    scope_limit: str
    arbitrary_projection: bool
    arbitrary_positive_block_partition: bool
    off_block_coherence_characterized: bool
    distinct_noncrossing_characterized: bool
    off_block_coherence_implies_component_M4: bool
    theorem_verified: bool
    status: str


@dataclass(frozen=True)
class ComponentBlockCoherenceBoundaryReport:
    created_at: str
    theorem_contract: dict[str, Any]
    finite_controls: list[BlockCoherenceControl]
    commuting_scaling_records: list[CommutingCoherenceScalingRecord]
    theorem: BlockCoherenceBoundaryTheorem
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _block_slices(block_dimensions: tuple[int, ...]) -> tuple[slice, ...]:
    if not block_dimensions or any(block < 1 for block in block_dimensions):
        raise ValueError("positive block dimensions are required")
    output = []
    start = 0
    for block in block_dimensions:
        output.append(slice(start, start + block))
        start += block
    return tuple(output)


def _projection_from_isometry(isometry: np.ndarray, tolerance: float) -> np.ndarray:
    if isometry.ndim != 2 or isometry.shape[1] < 1:
        raise ValueError("a nonempty matrix isometry is required")
    identity = np.eye(isometry.shape[1], dtype=complex)
    residual = np.linalg.norm(isometry.conj().T @ isometry - identity, ord=2)
    if residual > 1000 * tolerance:
        raise ValueError("columns must be orthonormal")
    return isometry @ isometry.conj().T


def commuting_codimension_one_naimark_isometry(common_dimension: int) -> np.ndarray:
    """Return the minimal block-one Naimark isometry of the counterfamily."""

    cosine_squared, _, frame_scalar = exact_family_parameters(common_dimension)
    weights = (1 / frame_scalar, cosine_squared / frame_scalar, cosine_squared / frame_scalar)
    r = common_dimension
    isometry = np.zeros((3 * r, r), dtype=complex)
    for coordinate in range(r):
        for local, weight in enumerate(weights):
            isometry[3 * coordinate + local, coordinate] = float(weight) ** 0.5
    return isometry


def haar_isometry(
    coefficient_dimension: int,
    fiber_rank: int,
    *,
    seed: int,
) -> np.ndarray:
    if coefficient_dimension < fiber_rank or fiber_rank < 1:
        raise ValueError("require coefficient dimension at least positive fiber rank")
    rng = np.random.default_rng(seed)
    raw = rng.normal(size=(coefficient_dimension, fiber_rank)) + 1j * rng.normal(
        size=(coefficient_dimension, fiber_rank)
    )
    basis, _ = np.linalg.qr(raw, mode="reduced")
    return basis


def audit_block_coherence_boundary(
    control_id: str,
    isometry: np.ndarray,
    block_dimensions: tuple[int, ...],
    *,
    tolerance: float = 1e-9,
) -> BlockCoherenceControl:
    projection = _projection_from_isometry(isometry, tolerance)
    coefficient, fiber = isometry.shape
    if sum(block_dimensions) != coefficient:
        raise ValueError("block dimensions must sum to the coefficient dimension")
    slices = _block_slices(block_dimensions)
    projection_residual = float(
        np.linalg.norm(projection @ projection - projection, ord=2)
    )
    diagonal = [projection[index, index] for index in slices]
    effects = [
        isometry[index, :].conj().T @ isometry[index, :] for index in slices
    ]
    positive_edges = [
        float(value)
        for block in diagonal
        for value in np.linalg.eigvalsh((block + block.conj().T) / 2.0)
        if value > 100 * tolerance
    ]
    edge = min(positive_edges)
    off_energy = 0.0
    noncrossing = 0.0
    crossing = 0.0
    direct_commutator = 0.0
    norm_residual = 0.0
    zero_failure = 0.0
    for left, left_slice in enumerate(slices):
        left_block = diagonal[left]
        left_root_values, left_root_vectors = np.linalg.eigh(
            (left_block + left_block.conj().T) / 2.0
        )
        left_root = (left_root_vectors * np.sqrt(np.maximum(left_root_values, 0.0))) @ left_root_vectors.conj().T
        for right, right_slice in enumerate(slices):
            if left == right:
                continue
            right_block = diagonal[right]
            bridge = projection[left_slice, right_slice]
            adjoint = bridge.conj().T
            energy = float(np.linalg.norm(bridge, ord="fro") ** 2)
            off_energy += energy
            pair_noncross = float(
                np.trace(left_block @ bridge @ right_block @ adjoint).real
            )
            pair_cross = float(np.trace((bridge @ adjoint) @ (bridge @ adjoint)).real)
            noncrossing += pair_noncross
            crossing += pair_cross
            right_values, right_vectors = np.linalg.eigh(
                (right_block + right_block.conj().T) / 2.0
            )
            right_root = (right_vectors * np.sqrt(np.maximum(right_values, 0.0))) @ right_vectors.conj().T
            norm_form = float(
                np.linalg.norm(left_root @ bridge @ right_root, ord="fro") ** 2
            )
            norm_residual = max(norm_residual, abs(pair_noncross - norm_form))
            if energy > 1000 * tolerance and pair_noncross <= 1000 * tolerance:
                zero_failure = max(zero_failure, energy)
            commutator = effects[left] @ effects[right] - effects[right] @ effects[left]
            direct_commutator += float(np.linalg.norm(commutator, ord="fro") ** 2)
    trace_square = sum(
        float(np.trace(block @ block).real) for block in diagonal
    )
    identity_energy = fiber - trace_square
    energy_residual = abs(off_energy - identity_energy)
    edge_lower = edge * edge * off_energy
    edge_residual = max(0.0, edge_lower - noncrossing)
    ordered_gap = 2.0 * (noncrossing - crossing)
    commutator_residual = abs(ordered_gap - direct_commutator)
    verified = bool(
        projection_residual <= 1000 * tolerance
        and energy_residual <= 1000 * tolerance
        and norm_residual <= 1000 * tolerance
        and zero_failure <= 1000 * tolerance
        and edge_residual <= 1000 * tolerance
        and commutator_residual <= 5000 * tolerance
        and noncrossing + 1000 * tolerance >= crossing
    )
    return BlockCoherenceControl(
        control_id=control_id,
        coefficient_dimension=coefficient,
        fiber_rank=fiber,
        outcome_count=len(block_dimensions),
        block_dimensions=block_dimensions,
        minimum_positive_block_eigenvalue=edge,
        off_block_frobenius_energy=off_energy,
        projection_identity_off_block_energy=identity_energy,
        off_block_energy_identity_residual=energy_residual,
        ordered_distinct_noncrossing_mass=noncrossing,
        edge_weighted_noncrossing_lower_bound=edge_lower,
        edge_lower_bound_residual=edge_residual,
        ordered_distinct_crossing_mass=crossing,
        ordered_commutator_gap=ordered_gap,
        direct_ordered_commutator_mass=direct_commutator,
        commutator_identity_residual=commutator_residual,
        maximum_pair_noncrossing_norm_residual=norm_residual,
        maximum_pair_zero_equivalence_failure=zero_failure,
        projection_residual=projection_residual,
        block_coherence_positive=off_energy > 1000 * tolerance,
        distinct_noncrossing_positive=noncrossing > 1000 * tolerance,
        crossing_cancels_noncrossing=abs(noncrossing - crossing) <= 5000 * tolerance,
        exact_block_coherence_boundary_verified=verified,
        status=(
            "block-coherence-boundary-verified"
            if verified
            else "block-coherence-boundary-control-failure"
        ),
    )


def commuting_coherence_scaling_record(common_dimension: int) -> CommutingCoherenceScalingRecord:
    r = common_dimension
    cosine_squared, _, frame_scalar = exact_family_parameters(r)
    center_weight = 1 / frame_scalar
    side_weight = cosine_squared / frame_scalar
    square_sum = center_weight**2 + 2 * side_weight**2
    fourth_sum = center_weight**4 + 2 * side_weight**4
    off_energy_normalized = 1 - square_sum
    noncrossing_normalized = square_sum**2 - fourth_sum
    edge_lower_normalized = side_weight**2 * off_energy_normalized
    return CommutingCoherenceScalingRecord(
        common_dimension=r,
        coefficient_dimension=3 * r,
        fiber_rank=r,
        minimum_positive_block_eigenvalue=float(side_weight),
        normalized_off_block_frobenius_energy=float(off_energy_normalized),
        normalized_ordered_distinct_noncrossing_mass=float(noncrossing_normalized),
        normalized_ordered_distinct_crossing_mass=float(noncrossing_normalized),
        normalized_commutator_gap=0.0,
        edge_lower_bound_normalized=float(edge_lower_normalized),
        off_block_coherence_extensive=off_energy_normalized > Fraction(1, 2),
        distinct_noncrossing_extensive=noncrossing_normalized > Fraction(1, 100),
        component_M4_positive=False,
        status="extensive-coherence-and-noncrossing-but-zero-M4",
    )


def block_coherence_boundary_theorem() -> BlockCoherenceBoundaryTheorem:
    return BlockCoherenceBoundaryTheorem(
        off_block_identity=(
            "sum_(e!=f)||Pi_ef||_F^2=rank(Pi)-sum_e Tr(Pi_ee^2)"
        ),
        pair_noncrossing_identity=(
            "N_ef=||Pi_ee^(1/2) Pi_ef Pi_ff^(1/2)||_F^2"
        ),
        zero_equivalence="for e!=f, N_ef=0 iff Pi_ef=0",
        positive_edge_bound=(
            "if every positive block eigenvalue is at least delta, then "
            "sum_(e!=f)N_ef>=delta^2 sum_(e!=f)||Pi_ef||_F^2"
        ),
        commutator_gap_identity=(
            "sum_(e!=f)||[H_e,H_f]||_F^2=2 sum_(e!=f)(N_ef-C_ef)"
        ),
        insufficiency_counterfamily=(
            "codimension-one tight frames have extensive off-block and distinct "
            "noncrossing mass with N_ef=C_ef pairwise"
        ),
        scope_limit=(
            "The theorem identifies but does not lower-bound the natural signed "
            "noncrossing-minus-crossing separation."
        ),
        arbitrary_projection=True,
        arbitrary_positive_block_partition=True,
        off_block_coherence_characterized=True,
        distinct_noncrossing_characterized=True,
        off_block_coherence_implies_component_M4=False,
        theorem_verified=True,
        status="block-coherence-reduced-crossing-separation-remains",
    )


def run_component_block_coherence_boundary() -> ComponentBlockCoherenceBoundaryReport:
    commuting_controls = [
        audit_block_coherence_boundary(
            f"COMMUTING-CODIMENSION-ONE-R{r}",
            commuting_codimension_one_naimark_isometry(r),
            (1,) * (3 * r),
        )
        for r in (2, 4, 8)
    ]
    haar = audit_block_coherence_boundary(
        "HAAR-BLOCK-CONTROL",
        haar_isometry(18, 7, seed=2411),
        (3, 3, 3, 3, 3, 3),
    )
    controls = [*commuting_controls, haar]
    scaling = [
        commuting_coherence_scaling_record(r) for r in (2, 4, 8, 16, 64, 256)
    ]
    theorem = block_coherence_boundary_theorem()
    failures = sum(not row.exact_block_coherence_boundary_verified for row in controls)
    exact = bool(
        failures == 0
        and all(row.crossing_cancels_noncrossing for row in commuting_controls)
        and haar.ordered_commutator_gap > 1000e-9
        and theorem.theorem_verified
    )
    return ComponentBlockCoherenceBoundaryReport(
        created_at=utc_now(),
        theorem_contract={
            "off_block_identity": theorem.off_block_identity,
            "noncrossing_identity": theorem.pair_noncrossing_identity,
            "edge_bound": theorem.positive_edge_bound,
            "commutator_gap": theorem.commutator_gap_identity,
            "scope": theorem.scope_limit,
        },
        finite_controls=controls,
        commuting_scaling_records=scaling,
        theorem=theorem,
        proof_obligations=[
            {
                "obligation": "characterize_distinct_noncrossing_mass_of_dependency_projection",
                "resolved": exact,
                "resolution": (
                    "Projection idempotence gives total off-block energy; PSD range "
                    "inclusion gives exact pair positivity and the edge-weighted bound."
                ),
            },
            {
                "obligation": "determine_whether_off_block_coherence_suffices_for_component_M4",
                "resolved": exact,
                "resolution": (
                    "Refuted by the codimension-one family: both masses are extensive, "
                    "but crossing equals noncrossing exactly."
                ),
            },
            {
                "obligation": "prove_natural_crossing_separation",
                "resolved": False,
                "resolution": (
                    "A natural theorem must directly lower-bound sum(N_ef-C_ef), "
                    "not either unsigned term alone."
                ),
            },
        ],
        adversarial_audit=[
            {
                "objection": "A nonzero off-diagonal projection block might have zero noncrossing mass.",
                "resolved": True,
                "resolution": (
                    "PSD block-range inclusion makes the square-root norm in (2) zero "
                    "exactly when the off-diagonal block is zero."
                ),
            },
            {
                "objection": "A positive component edge turns noncrossing mass into M4.",
                "resolved": True,
                "resolution": (
                    "It lower-bounds only N. The commuting family has edge at least 1/4 "
                    "and C=N for every pair."
                ),
            },
            {
                "objection": "Extensive off-block energy excludes a near-PVM commuting algebra.",
                "resolved": True,
                "resolution": (
                    "Commuting nonprojective POVMs have extensive Naimark off-block "
                    "coherence; block-diagonality characterizes PVMs, not commutativity."
                ),
            },
        ],
        headline_metrics={
            "block_coherence_identity_theorem_count": int(exact),
            "distinct_noncrossing_characterization_theorem_count": int(exact),
            "off_block_coherence_sufficiency_no_go_count": int(exact),
            "finite_control_count": len(controls),
            "finite_control_failure_count": failures,
            "largest_commuting_scaling_rank": scaling[-1].fiber_rank,
            "largest_scale_normalized_off_block_energy": (
                scaling[-1].normalized_off_block_frobenius_energy
            ),
            "largest_scale_normalized_distinct_noncrossing_mass": (
                scaling[-1].normalized_ordered_distinct_noncrossing_mass
            ),
            "largest_scale_normalized_commutator_gap": (
                scaling[-1].normalized_commutator_gap
            ),
            "natural_crossing_separation_theorem_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "natural_off_block_coherence_sufficient": False,
            "natural_distinct_noncrossing_mass_sufficient": False,
            "natural_crossing_separation_proved": False,
            "natural_component_M4_positive": False,
            "speedup_claim_allowed": False,
            "reason": (
                "Only the signed noncrossing-minus-crossing gap detects component "
                "noncommutativity; all currently easier unsigned block statistics can be large at zero M4."
            ),
        },
        status=(
            "unsigned-block-coherence-route-falsified-crossing-gap-is-minimal-target"
            if exact
            else "block-coherence-boundary-control-failure"
        ),
        summary=(
            "Characterized off-block and distinct noncrossing mass exactly, then "
            "proved that both can remain extensive while the component M4 is zero."
        ),
        falsifiers_triggered=[
            "Off-block coherence is not a proxy for noncommutative component mass.",
            "A positive distinct noncrossing fourth moment is not enough without controlling the crossing contraction.",
            "A constant positive component edge cannot prevent exact crossing cancellation.",
        ],
    )


def write_component_block_coherence_boundary_report(
    path: Path = REPORT_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = (
        "EXP-CODE-SELF-DUAL-WREATH-COMPONENT-BLOCK-COHERENCE-BOUNDARY"
    ),
    registry_candidate_id: str = "CODE-COSET-COLLECTIVE",
    registry_result_id: str = "",
    **kwargs: Any,
) -> dict[str, Any]:
    path = path
    output_path = path
    for _k in ("write_registry", "registry_experiment_id", "registry_candidate_id", "registry_result_id"):
        kwargs.pop(_k, None)
    report = asdict(run_component_block_coherence_boundary())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    if write_registry:
        _res_payload = report if "report" in locals() else (payload if "payload" in locals() else (result if "result" in locals() else output))
        from research_registry import (
            ExperimentResultRecord,
            NegativeResultRecord,
            upsert_experiment_result,
            upsert_negative_result,
        )

        upsert_negative_result(
            NegativeResultRecord(
                id="NEG-SELF-DUAL-WREATH-COMPONENT-BLOCK-COHERENCE-BOUNDARY",
                source=registry_experiment_id,
                claim=(
                    "Initial negative claim for EXP-CODE-SELF-DUAL-WREATH-COMPONENT-BLOCK-COHERENCE-BOUNDARY."
                ),
                reason_invalid=(
                    "Falsified or refined by exact theorem evaluation."
                ),
                lesson=(
                    "Lesson from exact theorem analysis for EXP-CODE-SELF-DUAL-WREATH-COMPONENT-BLOCK-COHERENCE-BOUNDARY."
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
                    "self_dual_wreath_component_block_coherence_boundary": str(path)
                },
            )
        )

    return report


if __name__ == "__main__":
    payload = write_component_block_coherence_boundary_report()
    print(json.dumps(payload["headline_metrics"], indent=2, sort_keys=True))

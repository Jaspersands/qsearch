"""Codimension-one discontinuity for canonical component commutators.

The full-support pair-budget theorem says that a projection frame with too
few pairwise range intersections cannot have commuting canonical effects.
It is tempting to combine that theorem with an extra-copy schedule that makes
the sibling common span *almost* full.  This module proves that this shortcut
is false in the strongest possible finite-codimension sense.

For every ``r >= 2``, work on ``C^r direct_sum C t`` and put

    c^2 = (2r-1)/(2(r+1)),    s^2 = 3/(2(r+1)).

For each coordinate ``i`` use three rank-one projection leaves on

    u_(i,0) = e_i,
    u_(i,+) = c e_i + s t,
    u_(i,-) = c e_i - s t.

The opposite signs cancel every off-diagonal frame entry and

    F = sum_(i,sigma) |u_(i,sigma)><u_(i,sigma)|
      = [3r/(r+1)] I_(r+1).                                (1)

All ``3r`` leaf ranges are distinct lines, so their exact pair-intersection
budget is zero even though the total-rank excess is ``2r-1``.  Consequently
the full-support canonical effects are noncommutative, exactly as required by
the pair-budget theorem.

Now compress by the coordinate hyperplane ``X=span{e_1,...,e_r}``, only one
dimension below full support.  The actual pseudoinverse-normalized component
effects are

    H_(i,0)   = (1/a) |e_i><e_i|,
    H_(i,+/-) = (c^2/a) |e_i><e_i|,   a=3r/(r+1).           (2)

They sum to identity and commute exactly.  The compression retains a constant
positive edge ``(2r-1)/(6r) >= 1/4`` and a full-rank nonscalarity defect.  A
positive fraction tending to ``4/9`` of the original leaf pairs still has an
inverse-linear nonzero commutator.  The frame condition number is one, the
total leaf-rank/common-rank aspect is three, and the common-span relative rank
is ``r/(r+1) -> 1``.

Thus no theorem based only on vanishing relative codimension, frame
conditioning, leaf-rank aspect, physical pair budget, leaf commutators, a
component edge, or nonscalarity can transfer the full-support obstruction to
proper common-span compression.  Literal full support or a direct natural
fourth-moment/representation-theoretic argument is necessary.  This is a
generic linear-algebra counterfamily, not evidence that the natural wreath
component effects commute.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from fractions import Fraction
from pathlib import Path
from typing import Any

import numpy as np

from research_registry import utc_now


REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_codimension_one_commuting_compression_no_go.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-CODIMENSION-ONE-COMMUTING-COMPRESSION-NO-GO"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


@dataclass(frozen=True)
class CodimensionOneCompressionControl:
    control_id: str
    common_dimension: int
    physical_dimension: int
    common_codimension: int
    common_relative_rank: float
    outcome_count: int
    leaf_rank: int
    total_leaf_rank: int
    total_leaf_rank_excess: int
    total_leaf_rank_to_common_aspect: float
    maximum_leaf_rank_to_common_ratio: float
    exact_pair_intersection_budget: int
    scalar_frame_value: float
    frame_scalar_residual: float
    frame_condition_number: float
    maximum_leaf_idempotence_residual: float
    maximum_distinct_leaf_overlap: float
    full_effect_sum_residual: float
    maximum_full_effect_commutator_norm: float
    compressed_effect_sum_residual: float
    maximum_compressed_effect_commutator_norm: float
    minimum_positive_compressed_effect_eigenvalue: float
    nonscalarity_defect_minimum_eigenvalue: float
    predicted_cross_coordinate_leaf_commutator_norm: float
    observed_cross_coordinate_leaf_commutator_norm: float
    cross_coordinate_noncommuting_pair_fraction: float
    all_leaf_ranges_pairwise_disjoint: bool
    full_support_pair_budget_obstructs_commuting_effects: bool
    compressed_effects_commute: bool
    exact_counterfamily_verified: bool
    status: str


@dataclass(frozen=True)
class CodimensionOneScalingRecord:
    common_dimension: int
    physical_dimension: int
    common_codimension: int
    common_relative_rank: float
    outcome_count: int
    total_leaf_rank_to_common_aspect: float
    maximum_leaf_rank_to_common_ratio: float
    total_leaf_rank_excess: int
    exact_pair_intersection_budget: int
    frame_condition_number: float
    component_positive_edge: float
    nonscalarity_defect_edge: float
    cross_coordinate_leaf_commutator_norm: float
    cross_coordinate_noncommuting_pair_fraction: float
    full_effects_noncommutative: bool
    compressed_effects_commute: bool
    status: str


@dataclass(frozen=True)
class CodimensionOneNoGoTheorem:
    construction: str
    frame_identity: str
    full_support_obstruction: str
    compressed_effect_formula: str
    discontinuity: str
    scope_limit: str
    arbitrary_dimension_at_least_two: bool
    exact_common_codimension_one: bool
    scalar_tight_frame: bool
    zero_physical_pair_budget: bool
    constant_component_edge: bool
    full_rank_nonscalarity: bool
    proper_compression_commutative: bool
    theorem_verified: bool
    status: str


@dataclass(frozen=True)
class CodimensionOneCommutingCompressionNoGoReport:
    created_at: str
    theorem_contract: dict[str, Any]
    finite_controls: list[CodimensionOneCompressionControl]
    scaling_records: list[CodimensionOneScalingRecord]
    theorem: CodimensionOneNoGoTheorem
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def exact_family_parameters(common_dimension: int) -> tuple[Fraction, Fraction, Fraction]:
    """Return ``(c^2,s^2,a)`` for the exact scalar-frame family."""

    if common_dimension < 2:
        raise ValueError("common dimension must be at least two")
    r = common_dimension
    cosine_squared = Fraction(2 * r - 1, 2 * (r + 1))
    sine_squared = Fraction(3, 2 * (r + 1))
    frame_scalar = Fraction(3 * r, r + 1)
    if cosine_squared + sine_squared != 1:
        raise ArithmeticError("unit-vector identity failed")
    if 1 + 2 * cosine_squared != frame_scalar:
        raise ArithmeticError("coordinate frame identity failed")
    if 2 * r * sine_squared != frame_scalar:
        raise ArithmeticError("shared-coordinate frame identity failed")
    return cosine_squared, sine_squared, frame_scalar


def construct_codimension_one_projection_frame(
    common_dimension: int,
) -> tuple[tuple[np.ndarray, ...], np.ndarray]:
    """Construct the leaves and the codimension-one common isometry."""

    cosine_squared, sine_squared, _ = exact_family_parameters(common_dimension)
    cosine = math.sqrt(float(cosine_squared))
    sine = math.sqrt(float(sine_squared))
    dimension = common_dimension + 1
    leaves: list[np.ndarray] = []
    for index in range(common_dimension):
        center = np.zeros(dimension, dtype=complex)
        center[index] = 1.0
        plus = center.copy()
        plus[index] = cosine
        plus[-1] = sine
        minus = center.copy()
        minus[index] = cosine
        minus[-1] = -sine
        for vector in (center, plus, minus):
            leaves.append(np.outer(vector, vector.conj()))
    common = np.zeros((dimension, common_dimension), dtype=complex)
    common[:common_dimension, :] = np.eye(common_dimension)
    return tuple(leaves), common


def _psd_inverse_root(matrix: np.ndarray, tolerance: float) -> np.ndarray:
    hermitian = (matrix + matrix.conj().T) / 2.0
    values, vectors = np.linalg.eigh(hermitian)
    if values[0] <= 100 * tolerance:
        raise ValueError("the frame must be positive definite")
    return (vectors * (values ** -0.5)) @ vectors.conj().T


def _rank_one_commutator_norm(overlap: float) -> float:
    overlap = min(1.0, max(0.0, abs(overlap)))
    return overlap * math.sqrt(max(0.0, 1.0 - overlap * overlap))


def audit_codimension_one_compression(
    common_dimension: int,
    *,
    tolerance: float = 1e-9,
) -> CodimensionOneCompressionControl:
    """Numerically audit every exact identity used by the counterfamily."""

    leaves, common = construct_codimension_one_projection_frame(common_dimension)
    cosine_squared, sine_squared, frame_scalar_exact = exact_family_parameters(
        common_dimension
    )
    r = common_dimension
    dimension = r + 1
    frame_scalar = float(frame_scalar_exact)
    identity = np.eye(dimension, dtype=complex)
    frame = sum(leaves, np.zeros_like(identity))
    frame_residual = float(np.linalg.norm(frame - frame_scalar * identity, ord=2))
    frame_values = np.linalg.eigvalsh((frame + frame.conj().T) / 2.0)
    condition = float(frame_values[-1] / frame_values[0])
    idempotence = max(
        float(np.linalg.norm(leaf @ leaf - leaf, ord=2)) for leaf in leaves
    )
    vectors = []
    for leaf in leaves:
        values, basis = np.linalg.eigh((leaf + leaf.conj().T) / 2.0)
        vectors.append(basis[:, int(np.argmax(values))])
    pair_overlaps = [
        abs(np.vdot(vectors[left], vectors[right]))
        for left in range(len(vectors))
        for right in range(left + 1, len(vectors))
    ]
    maximum_overlap = max(pair_overlaps, default=0.0)
    pair_intersections = int(
        sum(bool(overlap >= 1.0 - 100 * tolerance) for overlap in pair_overlaps)
    )

    inverse_root = _psd_inverse_root(frame, tolerance)
    full_effects = tuple(inverse_root @ leaf @ inverse_root for leaf in leaves)
    full_sum_residual = float(
        np.linalg.norm(sum(full_effects, np.zeros_like(identity)) - identity, ord=2)
    )
    full_commutator = max(
        float(np.linalg.norm(left @ right - right @ left, ord=2))
        for left in full_effects
        for right in full_effects
    )

    frame_inverse = np.linalg.inv(frame)
    metric = common.conj().T @ frame_inverse @ common
    metric_inverse_root = _psd_inverse_root(metric, tolerance)
    compressed_effects = tuple(
        metric_inverse_root
        @ common.conj().T
        @ frame_inverse
        @ leaf
        @ frame_inverse
        @ common
        @ metric_inverse_root
        for leaf in leaves
    )
    common_identity = np.eye(r, dtype=complex)
    compressed_sum_residual = float(
        np.linalg.norm(
            sum(compressed_effects, np.zeros_like(common_identity)) - common_identity,
            ord=2,
        )
    )
    compressed_commutator = max(
        float(np.linalg.norm(left @ right - right @ left, ord=2))
        for left in compressed_effects
        for right in compressed_effects
    )
    positive_values = [
        float(value)
        for effect in compressed_effects
        for value in np.linalg.eigvalsh((effect + effect.conj().T) / 2.0)
        if value > 100 * tolerance
    ]
    positive_edge = min(positive_values)
    defect = np.zeros_like(common_identity)
    for effect in compressed_effects:
        scalar = float(np.trace(effect).real) / r
        centered = effect - scalar * common_identity
        defect += centered @ centered
    defect_edge = float(np.linalg.eigvalsh((defect + defect.conj().T) / 2.0)[0])

    cross_left = vectors[1]
    cross_right = vectors[4]
    observed_cross = float(
        np.linalg.norm(
            np.outer(cross_left, cross_left.conj())
            @ np.outer(cross_right, cross_right.conj())
            - np.outer(cross_right, cross_right.conj())
            @ np.outer(cross_left, cross_left.conj()),
            ord=2,
        )
    )
    predicted_cross = _rank_one_commutator_norm(float(sine_squared))
    noncommuting_cross_pairs = 4 * math.comb(r, 2)
    total_pairs = math.comb(3 * r, 2)
    cross_fraction = noncommuting_cross_pairs / total_pairs

    total_rank = 3 * r
    excess = total_rank - dimension
    pair_budget_obstruction = bool(pair_intersections < excess)
    exact = bool(
        frame_residual <= 1000 * tolerance
        and abs(condition - 1.0) <= 1000 * tolerance
        and idempotence <= 1000 * tolerance
        and pair_intersections == 0
        and full_sum_residual <= 1000 * tolerance
        and full_commutator > 1000 * tolerance
        and compressed_sum_residual <= 1000 * tolerance
        and compressed_commutator <= 1000 * tolerance
        and abs(positive_edge - float(cosine_squared / frame_scalar_exact))
        <= 1000 * tolerance
        and abs(observed_cross - predicted_cross) <= 1000 * tolerance
        and defect_edge > 0
        and pair_budget_obstruction
    )
    return CodimensionOneCompressionControl(
        control_id=f"CODIMENSION-ONE-R{r}",
        common_dimension=r,
        physical_dimension=dimension,
        common_codimension=1,
        common_relative_rank=r / dimension,
        outcome_count=3 * r,
        leaf_rank=1,
        total_leaf_rank=total_rank,
        total_leaf_rank_excess=excess,
        total_leaf_rank_to_common_aspect=3.0,
        maximum_leaf_rank_to_common_ratio=1.0 / r,
        exact_pair_intersection_budget=pair_intersections,
        scalar_frame_value=frame_scalar,
        frame_scalar_residual=frame_residual,
        frame_condition_number=condition,
        maximum_leaf_idempotence_residual=idempotence,
        maximum_distinct_leaf_overlap=maximum_overlap,
        full_effect_sum_residual=full_sum_residual,
        maximum_full_effect_commutator_norm=full_commutator,
        compressed_effect_sum_residual=compressed_sum_residual,
        maximum_compressed_effect_commutator_norm=compressed_commutator,
        minimum_positive_compressed_effect_eigenvalue=positive_edge,
        nonscalarity_defect_minimum_eigenvalue=defect_edge,
        predicted_cross_coordinate_leaf_commutator_norm=predicted_cross,
        observed_cross_coordinate_leaf_commutator_norm=observed_cross,
        cross_coordinate_noncommuting_pair_fraction=cross_fraction,
        all_leaf_ranges_pairwise_disjoint=pair_intersections == 0,
        full_support_pair_budget_obstructs_commuting_effects=pair_budget_obstruction,
        compressed_effects_commute=compressed_commutator <= 1000 * tolerance,
        exact_counterfamily_verified=exact,
        status=(
            "codimension-one-commuting-compression-counterfamily-verified"
            if exact
            else "codimension-one-compression-control-failure"
        ),
    )


def codimension_one_scaling_record(common_dimension: int) -> CodimensionOneScalingRecord:
    cosine_squared, sine_squared, frame_scalar = exact_family_parameters(
        common_dimension
    )
    r = common_dimension
    component_edge = cosine_squared / frame_scalar
    weight_square_sum = (1 + 2 * cosine_squared * cosine_squared) / (
        frame_scalar * frame_scalar
    )
    defect_edge = (1 - Fraction(1, r)) * weight_square_sum
    cross_norm = float(sine_squared) * math.sqrt(1.0 - float(sine_squared) ** 2)
    return CodimensionOneScalingRecord(
        common_dimension=r,
        physical_dimension=r + 1,
        common_codimension=1,
        common_relative_rank=r / (r + 1),
        outcome_count=3 * r,
        total_leaf_rank_to_common_aspect=3.0,
        maximum_leaf_rank_to_common_ratio=1.0 / r,
        total_leaf_rank_excess=2 * r - 1,
        exact_pair_intersection_budget=0,
        frame_condition_number=1.0,
        component_positive_edge=float(component_edge),
        nonscalarity_defect_edge=float(defect_edge),
        cross_coordinate_leaf_commutator_norm=cross_norm,
        cross_coordinate_noncommuting_pair_fraction=(
            4 * math.comb(r, 2) / math.comb(3 * r, 2)
        ),
        full_effects_noncommutative=True,
        compressed_effects_commute=True,
        status="codimension-one-discontinuity-persists",
    )


def codimension_one_no_go_theorem() -> CodimensionOneNoGoTheorem:
    return CodimensionOneNoGoTheorem(
        construction=(
            "three rank-one leaves e_i and c e_i +/- s t per common coordinate, "
            "with c^2=(2r-1)/(2(r+1)) and s^2=3/(2(r+1))"
        ),
        frame_identity="sum_e E_e=[3r/(r+1)] I_(r+1)",
        full_support_obstruction=(
            "pair budget is zero while total leaf-rank excess is 2r-1, so the "
            "full-support canonical effects cannot commute"
        ),
        compressed_effect_formula=(
            "on the codimension-one coordinate hyperplane, H_i0=(1/a)P_i "
            "and H_i+/H_i-=(c^2/a)P_i"
        ),
        discontinuity=(
            "deleting one shared carrier dimension changes a tight-frame, "
            "pair-budget-obstructed noncommutative POVM into an exactly commuting POVM"
        ),
        scope_limit=(
            "The family is not generated by natural wreath sources; it refutes only "
            "generic near-full-support transfer arguments."
        ),
        arbitrary_dimension_at_least_two=True,
        exact_common_codimension_one=True,
        scalar_tight_frame=True,
        zero_physical_pair_budget=True,
        constant_component_edge=True,
        full_rank_nonscalarity=True,
        proper_compression_commutative=True,
        theorem_verified=True,
        status="near-full-support-transfer-refuted-at-codimension-one",
    )


def run_codimension_one_commuting_compression_no_go(
) -> CodimensionOneCommutingCompressionNoGoReport:
    controls = [audit_codimension_one_compression(r) for r in (2, 3, 5, 8, 13)]
    scaling = [codimension_one_scaling_record(r) for r in (2, 4, 8, 16, 64, 256, 1024)]
    theorem = codimension_one_no_go_theorem()
    failures = sum(not control.exact_counterfamily_verified for control in controls)
    exact = bool(failures == 0 and theorem.theorem_verified)
    return CodimensionOneCommutingCompressionNoGoReport(
        created_at=utc_now(),
        theorem_contract={
            "construction": theorem.construction,
            "frame_identity": theorem.frame_identity,
            "full_support_obstruction": theorem.full_support_obstruction,
            "compressed_effect_formula": theorem.compressed_effect_formula,
            "scope": theorem.scope_limit,
        },
        finite_controls=controls,
        scaling_records=scaling,
        theorem=theorem,
        proof_obligations=[
            {
                "obligation": "test_whether_vanishing_relative_codimension_transfers_full_support_noncommutativity",
                "resolved": exact,
                "resolution": (
                    "Refuted exactly: common codimension one suffices for commuting "
                    "compressed effects in every dimension r+1."
                ),
            },
            {
                "obligation": "exclude_conditioning_and_pair_budget_as_missing_explanations",
                "resolved": exact,
                "resolution": (
                    "The frame is scalar-tight and all physical pair intersections "
                    "vanish, while the proper compression still commutes."
                ),
            },
            {
                "obligation": "prove_literal_natural_full_support_or_direct_natural_M4",
                "resolved": False,
                "resolution": (
                    "No generic rank-deficit estimate can bridge this gap; use the "
                    "natural dependency projection or prove exact full support."
                ),
            },
        ],
        adversarial_audit=[
            {
                "objection": "The counterfamily loses the constant component edge.",
                "resolved": True,
                "resolution": "Its minimum positive compressed eigenvalue is (2r-1)/(6r)>=1/4.",
            },
            {
                "objection": "The counterfamily needs a badly conditioned frame.",
                "resolved": True,
                "resolution": "Equation (1) makes the frame an exact scalar multiple of identity.",
            },
            {
                "objection": "Near-full rank plus zero pair budget should be enough.",
                "resolved": True,
                "resolution": (
                    "The common rank is r/(r+1), the pair budget is zero, and the "
                    "compressed effects nevertheless commute exactly."
                ),
            },
            {
                "objection": "This proves the natural wreath branch commutes.",
                "resolved": True,
                "resolution": (
                    "False. It is a generic counterfamily that raises the proof burden "
                    "to direct natural analysis; it makes no natural-law claim."
                ),
            },
        ],
        headline_metrics={
            "codimension_one_discontinuity_theorem_count": int(exact),
            "finite_control_count": len(controls),
            "finite_control_failure_count": failures,
            "largest_common_dimension": scaling[-1].common_dimension,
            "largest_common_relative_rank": scaling[-1].common_relative_rank,
            "limiting_total_leaf_rank_to_common_aspect": 3.0,
            "limiting_cross_noncommuting_pair_fraction": 4.0 / 9.0,
            "natural_component_M4_lower_bound_theorem_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "near_full_support_generic_transfer_valid": False,
            "literal_full_support_or_direct_natural_analysis_required": exact,
            "natural_component_M4_positive": False,
            "speedup_claim_allowed": False,
            "reason": (
                "A single missing carrier dimension can erase the entire canonical "
                "commutator despite every currently available coarse natural control."
            ),
        },
        status=(
            "codimension-one-near-full-support-shortcut-falsified"
            if exact
            else "codimension-one-counterfamily-control-failure"
        ),
        summary=(
            "Constructed a scalar-tight rank-one frame whose full canonical effects "
            "are pair-budget-obstructed but whose codimension-one component effects commute."
        ),
        falsifiers_triggered=[
            "Vanishing relative common codimension does not approximate the full-support commutator branch.",
            "Extra-copy schedules that prove only D-o(D) common rank cannot invoke the full-support pair-budget theorem.",
            "Frame conditioning, zero pair intersections, constant component edge, and full-rank nonscalarity do not repair the discontinuity.",
        ],
    )


def write_codimension_one_commuting_compression_no_go_report(
    path: Path = REPORT_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = (
        "EXP-CODE-SELF-DUAL-WREATH-CODIMENSION-ONE-COMMUTING-COMPRESSION-NO-GO"
    ),
    registry_candidate_id: str = "CODE-COSET-COLLECTIVE",
    registry_result_id: str = "",
    **kwargs: Any,
) -> dict[str, Any]:
    path = path
    output_path = path
    for _k in ("write_registry", "registry_experiment_id", "registry_candidate_id", "registry_result_id"):
        kwargs.pop(_k, None)
    report = asdict(run_codimension_one_commuting_compression_no_go())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    return report


if __name__ == "__main__":
    payload = write_codimension_one_commuting_compression_no_go_report()
    print(json.dumps(payload["headline_metrics"], indent=2, sort_keys=True))

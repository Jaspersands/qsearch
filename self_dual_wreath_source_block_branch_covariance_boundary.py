"""Branch covariance moves the source block; it is not a sibling compiler.

For an ordered source tuple

    Lambda=((lambda_1,mu_1),...,(lambda_K,mu_K))

and orientation ``e in F_2^K``, let ``E_e^Lambda`` be the corresponding
orientation-invariant projector.  A branch flip ``t`` canonically swaps the
two carrier factors in every selected source pair.  It gives an exact unitary
between *different Fourier source blocks*:

    U_t E_e^Lambda U_t^* = E_(e+t)^(t Lambda).              (1)

Equation (1) does not imply

    E_e^Lambda ~= E_(e+t)^Lambda.                           (2)

For unequal ordered source pairs, every nonzero ``t`` changes ``Lambda``.
For globally distinct source partitions the branch stabilizer is therefore
trivial.  Leaf ranks can differ inside one fixed block, giving an immediate
unitary-conjugacy obstruction to (2), while the cross-block ranks in (1)
agree exactly.

Independent Plancherel source sampling is invariant under pair swaps, so (1)
does imply equality in distribution across source blocks.  Annealed symmetry
does not imply blockwise short-metric equality, a Hadamard endpoint mixer, or
a coherent fixed-block compiler.  The physical S6 partial-support node has
leaf ranks ``(225,125)`` versus ``(225,2025)`` across its affine sibling
translation, making the distinction explicit.

This is a covariance-scope theorem, not a lower bound on direct rectangular
CS transforms.  Matrix-valued recursive child embeddings remain open.  No
complete polar, decoder, classical separation, or speedup is claimed.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from representation_obstruction import hook_length_dimension
from research_registry import utc_now
from self_dual_wreath_orientation_fusion_moment import (
    tensor_product_multiplicities,
)


REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_source_block_branch_covariance_boundary.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-SOURCE-BLOCK-BRANCH-COVARIANCE-BOUNDARY"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"

Partition = tuple[int, ...]
Label = tuple[Partition, Partition]


@dataclass(frozen=True)
class SourceBlockCovarianceControl:
    control_id: str
    n: int
    target_partition: Partition
    labels: tuple[Label, ...]
    translation_mask: int
    left_orientation_masks: tuple[int, ...]
    right_orientation_masks: tuple[int, ...]
    globally_distinct_source_partitions: bool
    every_source_pair_unequal: bool
    source_block_stabilized_by_translation: bool
    original_leaf_ranks: tuple[tuple[int, int], ...]
    translated_source_leaf_ranks: tuple[tuple[int, int], ...]
    cross_block_covariance_rank_mismatch_count: int
    within_fixed_block_rank_mismatch_count: int
    left_child_leaf_coefficient_dimension: int
    right_child_leaf_coefficient_dimension: int
    maximum_within_block_leaf_rank_difference: int
    fixed_block_internal_branch_unitary_possible: bool
    exact_cross_block_covariance_scope_verified: bool
    status: str


@dataclass(frozen=True)
class SourceBlockCovarianceScalingRecord:
    n: int
    information_threshold_copy_count: int
    branch_group_dimension: int
    unequal_source_tuple_branch_stabilizer_trivial: bool
    cross_source_block_branch_covariance_exact: bool
    independent_plancherel_law_branch_invariant: bool
    annealed_symmetry_implies_fixed_block_metric_equality: bool
    fixed_block_hadamard_endpoint_mixer_proved: bool
    matrix_recursive_child_compiler_proved: bool
    status: str


@dataclass(frozen=True)
class SourceBlockCovarianceTheorem:
    cross_block_covariance: str
    source_action: str
    stabilizer: str
    fixed_block_boundary: str
    annealed_scope: str
    surviving_target: str
    theorem_verified: bool
    status: str


@dataclass(frozen=True)
class SourceBlockCovarianceReport:
    created_at: str
    theorem_contract: dict[str, Any]
    theorem: SourceBlockCovarianceTheorem
    finite_controls: list[SourceBlockCovarianceControl]
    scaling_records: list[SourceBlockCovarianceScalingRecord]
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def swap_source_labels(
    labels: tuple[Label, ...],
    translation_mask: int,
) -> tuple[Label, ...]:
    if not 0 <= translation_mask < 1 << len(labels):
        raise ValueError("translation mask out of range")
    return tuple(
        (right, left) if translation_mask & (1 << index) else (left, right)
        for index, (left, right) in enumerate(labels)
    )


def orientation_leaf_rank(
    target_partition: Partition,
    labels: tuple[Label, ...],
    orientation_mask: int,
) -> int:
    if not 0 <= orientation_mask < 1 << len(labels):
        raise ValueError("orientation mask out of range")
    n = sum(target_partition)
    selected: list[Partition] = []
    companions: list[Partition] = []
    for index, (left, right) in enumerate(labels):
        if orientation_mask & (1 << index):
            selected.append(right)
            companions.append(left)
        else:
            selected.append(left)
            companions.append(right)
    multiplicity = dict(
        tensor_product_multiplicities(tuple(selected), n)
    ).get(target_partition, 0)
    return multiplicity * math.prod(
        hook_length_dimension(partition) for partition in companions
    )


def audit_source_block_covariance(
    control_id: str,
    target_partition: Partition,
    labels: tuple[Label, ...],
    translation_mask: int,
    left_orientation_masks: tuple[int, ...],
) -> SourceBlockCovarianceControl:
    if not labels or not translation_mask:
        raise ValueError("a nonzero branch translation is required")
    orientation_count = 1 << len(labels)
    if not left_orientation_masks:
        raise ValueError("at least one left orientation is required")
    if any(not 0 <= mask < orientation_count for mask in left_orientation_masks):
        raise ValueError("left orientation mask out of range")
    right_orientation_masks = tuple(
        mask ^ translation_mask for mask in left_orientation_masks
    )
    if set(left_orientation_masks) & set(right_orientation_masks):
        raise ValueError("the translation must produce a disjoint sibling set")

    swapped = swap_source_labels(labels, translation_mask)
    original = tuple(
        (mask, orientation_leaf_rank(target_partition, labels, mask))
        for mask in range(orientation_count)
    )
    translated = tuple(
        (mask, orientation_leaf_rank(target_partition, swapped, mask))
        for mask in range(orientation_count)
    )
    original_by_mask = dict(original)
    translated_by_mask = dict(translated)
    cross_mismatches = sum(
        original_by_mask[mask]
        != translated_by_mask[mask ^ translation_mask]
        for mask in range(orientation_count)
    )
    within_mismatches = sum(
        original_by_mask[left] != original_by_mask[right]
        for left, right in zip(left_orientation_masks, right_orientation_masks)
    )
    rank_differences = tuple(
        abs(original_by_mask[left] - original_by_mask[right])
        for left, right in zip(left_orientation_masks, right_orientation_masks)
    )
    source = tuple(partition for label in labels for partition in label)
    globally_distinct = len(source) == len(set(source))
    unequal = all(left != right for left, right in labels)
    stabilized = swapped == labels
    internal_possible = within_mismatches == 0
    verified = bool(
        cross_mismatches == 0
        and not stabilized
        and within_mismatches > 0
        and unequal
    )
    return SourceBlockCovarianceControl(
        control_id=control_id,
        n=sum(target_partition),
        target_partition=target_partition,
        labels=labels,
        translation_mask=translation_mask,
        left_orientation_masks=left_orientation_masks,
        right_orientation_masks=right_orientation_masks,
        globally_distinct_source_partitions=globally_distinct,
        every_source_pair_unequal=unequal,
        source_block_stabilized_by_translation=stabilized,
        original_leaf_ranks=original,
        translated_source_leaf_ranks=translated,
        cross_block_covariance_rank_mismatch_count=cross_mismatches,
        within_fixed_block_rank_mismatch_count=within_mismatches,
        left_child_leaf_coefficient_dimension=sum(
            original_by_mask[mask] for mask in left_orientation_masks
        ),
        right_child_leaf_coefficient_dimension=sum(
            original_by_mask[mask] for mask in right_orientation_masks
        ),
        maximum_within_block_leaf_rank_difference=max(rank_differences),
        fixed_block_internal_branch_unitary_possible=internal_possible,
        exact_cross_block_covariance_scope_verified=verified,
        status=(
            "cross-block-covariance-exact-fixed-block-conjugacy-falsified"
            if verified
            else "source-block-covariance-control-failure"
        ),
    )


def source_block_covariance_scaling_record(
    n: int,
) -> SourceBlockCovarianceScalingRecord:
    if n < 5:
        raise ValueError("n must be at least five")
    copies = math.ceil(math.lgamma(n + 1) / math.log(2)) + 2
    return SourceBlockCovarianceScalingRecord(
        n=n,
        information_threshold_copy_count=copies,
        branch_group_dimension=copies,
        unequal_source_tuple_branch_stabilizer_trivial=True,
        cross_source_block_branch_covariance_exact=True,
        independent_plancherel_law_branch_invariant=True,
        annealed_symmetry_implies_fixed_block_metric_equality=False,
        fixed_block_hadamard_endpoint_mixer_proved=False,
        matrix_recursive_child_compiler_proved=False,
        status="annealed-branch-covariance-not-fixed-block-sibling-compiler",
    )


def _finite_controls() -> list[SourceBlockCovarianceControl]:
    return [
        audit_source_block_covariance(
            "S3-ONE-PAIR-RANK-MISMATCH",
            (3,),
            (((3,), (2, 1)),),
            1,
            (0,),
        ),
        audit_source_block_covariance(
            "S4-TWO-PAIR-RANK-MISMATCH",
            (2, 2),
            (((4,), (3, 1)), ((2, 2), (2, 1, 1))),
            3,
            (0, 1),
        ),
        audit_source_block_covariance(
            "S5-INVERSE-DIMENSION-PAIR-RANK-MISMATCH",
            (2, 1, 1, 1),
            (((5,), (4, 1)), ((2, 1, 1, 1), (1, 1, 1, 1, 1))),
            3,
            (0, 1),
        ),
        audit_source_block_covariance(
            "S6-MATRIX-PARTIAL-SUPPORT-SIBLINGS",
            (6,),
            (
                ((6,), (4, 2)),
                ((5, 1), (2, 2, 2)),
                ((3, 3), (2, 1, 1, 1, 1)),
                ((2, 2, 1, 1), (1, 1, 1, 1, 1, 1)),
            ),
            9,
            (2, 5),
        ),
    ]


def run_source_block_branch_covariance_boundary() -> SourceBlockCovarianceReport:
    controls = _finite_controls()
    scaling = [
        source_block_covariance_scaling_record(n)
        for n in (5, 6, 8, 10, 12, 16, 20, 24, 32, 48, 64, 96, 128)
    ]
    failures = sum(
        not row.exact_cross_block_covariance_scope_verified for row in controls
    )
    verified = failures == 0
    theorem = SourceBlockCovarianceTheorem(
        cross_block_covariance="U_t E_e^Lambda U_t^*=E_(e+t)^(tLambda)",
        source_action="tLambda swaps lambda_i and mu_i wherever t_i=1",
        stabilizer=(
            "an ordered tuple of unequal source pairs has trivial branch stabilizer"
        ),
        fixed_block_boundary=(
            "cross-block covariance supplies no unitary between sibling leaves "
            "inside one fixed source block"
        ),
        annealed_scope=(
            "independent Plancherel sampling is swap invariant, giving equality "
            "in distribution but not blockwise metric equality"
        ),
        surviving_target=(
            "matrix-valued child POVM/endpoint compilation inside each fixed block"
        ),
        theorem_verified=verified,
        status=(
            "branch-covariance-crosses-source-block-fixed-block-shortcut-rejected"
            if verified
            else "source-block-branch-covariance-theorem-control-failure"
        ),
    )
    s6 = next(row for row in controls if row.n == 6)
    return SourceBlockCovarianceReport(
        created_at=utc_now(),
        theorem_contract=asdict(theorem),
        theorem=theorem,
        finite_controls=controls,
        scaling_records=scaling,
        proof_obligations=[
            {
                "obligation": "state_exact_branch_covariance_with_source_action",
                "resolved": True,
                "resolution": (
                    "Canonical tensor-factor swaps intertwine the diagonal "
                    "invariant projector after swapping the ordered source labels."
                ),
            },
            {
                "obligation": "test_fixed_block_sibling_conjugacy",
                "resolved": verified,
                "resolution": (
                    "Every control has exact cross-block rank covariance and a "
                    "within-block sibling rank mismatch."
                ),
            },
            {
                "obligation": "compile_matrix_fixed_block_child_embeddings",
                "resolved": False,
                "resolution": (
                    "Annealed source symmetry does not prepare a coherent "
                    "block-conditioned endpoint or child POVM dilation."
                ),
            },
            {
                "obligation": "prove_natural_blockwise_endpoint_conditioning",
                "resolved": False,
                "resolution": (
                    "Distributional exchange symmetry supplies neither a "
                    "per-block hard edge nor a state-weighted trim theorem."
                ),
            },
        ],
        adversarial_audit=[
            {
                "objection": "The branch bit makes every affine sibling split unitarily conjugate.",
                "resolved": True,
                "resolution": (
                    "Only after moving to the swapped source block. Fixed-block "
                    "leaf ranks can differ."
                ),
            },
            {
                "objection": "Plancherel exchangeability proves a blockwise Hadamard mixer.",
                "resolved": True,
                "resolution": (
                    "Exchangeability is an annealed law. The coherent decoder "
                    "must act correctly after the source block is observed."
                ),
            },
            {
                "objection": "Equal total source probability repairs rank mismatch coherently.",
                "resolved": True,
                "resolution": (
                    "A classical mixture over swapped blocks does not create a "
                    "unitary identification inside either block."
                ),
            },
            {
                "objection": "This rules out the full connected-group transform.",
                "resolved": True,
                "resolution": (
                    "No. An induced orbit transform may coherently include all "
                    "swapped blocks, but still faces the rectangular CS polar."
                ),
            },
        ],
        headline_metrics={
            "source_block_covariance_scope_theorem_count": int(verified),
            "finite_control_count": len(controls),
            "finite_control_failure_count": failures,
            "cross_block_covariance_rank_mismatch_count": sum(
                row.cross_block_covariance_rank_mismatch_count for row in controls
            ),
            "fixed_block_rank_mismatch_control_count": sum(
                row.within_fixed_block_rank_mismatch_count > 0 for row in controls
            ),
            "maximum_within_block_leaf_rank_difference": max(
                row.maximum_within_block_leaf_rank_difference for row in controls
            ),
            "s6_left_child_leaf_coefficient_dimension": (
                s6.left_child_leaf_coefficient_dimension
            ),
            "s6_right_child_leaf_coefficient_dimension": (
                s6.right_child_leaf_coefficient_dimension
            ),
            "scaling_record_count": len(scaling),
            "fixed_block_hadamard_endpoint_compiler_count": 0,
            "matrix_recursive_child_compiler_count": 0,
            "complete_orientation_polar_compiler_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "cross_source_block_branch_covariance_proved": verified,
            "unequal_source_tuple_branch_stabilizer_trivial": True,
            "independent_plancherel_source_law_branch_invariant": True,
            "annealed_branch_symmetry_implies_fixed_block_sibling_conjugacy": False,
            "fixed_block_hadamard_endpoint_mixer_compiled": False,
            "matrix_recursive_child_compiler_proved": False,
            "direct_rectangular_cs_polar_compiled": False,
            "complete_natural_orientation_polar_compiled": False,
            "classical_separation_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "Branch flips intertwine different swapped source blocks. "
                "Fixed-block leaf-rank mismatch rejects the internal sibling "
                "conjugacy needed for a Hadamard shortcut."
            ),
        },
        status=theorem.status,
        summary=(
            "Separated exact cross-source-block branch covariance from the "
            "false fixed-block sibling-conjugacy shortcut."
        ),
        falsifiers_triggered=[
            "Affine sibling translation does not act internally on a fixed unequal-source Fourier block.",
            "Plancherel exchangeability is not a block-conditioned coherent compiler.",
            "The S6 matrix partial-support node has a 1900-dimensional paired leaf-rank mismatch.",
        ],
    )


def write_source_block_branch_covariance_boundary_report(
    path: Path = REPORT_PATH,
) -> dict[str, Any]:
    payload = asdict(run_source_block_branch_covariance_boundary())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    return payload


if __name__ == "__main__":
    report = write_source_block_branch_covariance_boundary_report()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))

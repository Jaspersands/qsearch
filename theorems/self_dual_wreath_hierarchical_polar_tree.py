"""Hierarchical relative-frame factorization of the orientation polar map.

For a set of orientation projectors indexed by a binary subtree ``T``, write

    R_T = vertical_stack_(epsilon in T) E_epsilon,
    S_T = R_T^* R_T = sum_(epsilon in T) E_epsilon,
    Q_T = R_T S_T^(-1/2).

If ``T=L disjoint_union R``, polar decomposition gives the exact chain rule

    Q_T = (Q_L direct_sum Q_R) W_(L,R),

    W_(L,R)
      = vertical_stack(S_L^(1/2), S_R^(1/2)) S_T^(-1/2).       (1)

The relative merge isometry obeys ``W^*W=Pi_supp(S_T)``.  Its left outcome
effect is

    C_(L|T) = S_T^(-1/2) S_L S_T^(-1/2),

and the right effect is the support identity minus ``C_(L|T)``.  Thus the
global nonorthogonal sampler can be organized as a binary tree of matrix-valued
conditional probabilities.  In the commuting case this is exactly the usual
count ratio ``t_L/t_T``.

For ``2^k`` orientation leaves arranged by a nested subspace flag, all nodes at
one depth are addressed coherently by the quotient label.  The circuit depth is
therefore ``k``, not ``2^k``, provided one can implement the controlled relative
isometry (1) uniformly at every level.

The base level is supplied by the constant-conditioned pair polar theorem.
Complete ``W_4`` controls verify the two-level chain exactly.  Their first
higher-level relative effects have spectrum contained in ``{0,1/2,1}``, even
when the child frames do not commute.  This is positive finite evidence for an
operator-valued counting recursion, not an all-n theorem.  No typical large-n
bound or circuit for higher-level relative effects is proved here.
"""

from __future__ import annotations

import itertools
import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import numpy as np

from representation_obstruction import integer_partitions
from research_registry import utc_now
from self_dual_wreath_collision_free_frame_probe import Label
from self_dual_wreath_orientation_fourier_reduction import (
    _w4_collision_free_labels,
    orientation_invariant_projector,
)


REPORT_PATH = Path(
    "research/representation/self_dual_wreath_hierarchical_polar_tree.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-HIERARCHICAL-POLAR-TREE"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


@dataclass(frozen=True)
class HierarchicalPolarControl:
    control_id: str
    n: int
    target_partition: tuple[int, ...]
    labels: tuple[Label, ...]
    leaf_order: tuple[int, ...]
    orientation_count: int
    carrier_dimension: int
    parent_support_rank: int
    left_child_support_rank: int
    right_child_support_rank: int
    parent_frame_condition_number: float
    left_child_frame_condition_number: float
    right_child_frame_condition_number: float
    child_frame_commutator_norm: float
    relative_effect_fractional_eigenvalues: tuple[float, ...]
    relative_effect_minimum_fractional_gap: float
    relative_effect_half_integral_spectrum_residual: float
    relative_merge_isometry_residual: float
    recursive_to_direct_polar_residual: float
    exact_hierarchical_polar_chain_verified: bool
    finite_half_integral_relative_effect_observed: bool
    status: str


@dataclass(frozen=True)
class HierarchicalPolarScalingRecord:
    n: int
    information_threshold_copy_count: int
    orientation_leaf_count_log2: int
    binary_tree_depth: int
    explicitly_compiled_node_count_decimal: str
    coherently_indexed_level_count: int
    base_pair_relative_sampler_polynomial: bool
    higher_level_relative_sampler_polynomial: bool
    typical_relative_effect_gap_proved: bool
    formal_mrs_sieve_model_uses_only_pairwise_state_isotypic_measurements: bool
    proposed_leaf_projector_acts_globally_on_all_source_labels: bool
    proposed_sampler_preserves_coherent_internal_labels: bool
    formal_mrs_sieve_theorem_directly_applies: bool
    status: str


@dataclass(frozen=True)
class HierarchicalPolarTreeReport:
    created_at: str
    theorem_contract: dict[str, Any]
    finite_controls: list[HierarchicalPolarControl]
    scaling_records: list[HierarchicalPolarScalingRecord]
    proof_obligations: list[dict[str, bool | str]]
    adversarial_audit: list[dict[str, bool | str]]
    literature_links: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, bool | str]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _psd_powers(
    matrix: np.ndarray,
    tolerance: float,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    hermitian = (matrix + matrix.conj().T) / 2
    eigenvalues, eigenvectors = np.linalg.eigh(hermitian)
    if eigenvalues[0] < -100 * tolerance:
        raise ValueError("matrix must be positive semidefinite")
    positive = eigenvalues > tolerance
    square_values = np.zeros_like(eigenvalues)
    inverse_values = np.zeros_like(eigenvalues)
    square_values[positive] = np.sqrt(eigenvalues[positive])
    inverse_values[positive] = eigenvalues[positive] ** -0.5
    square_root = (eigenvectors * square_values) @ eigenvectors.conj().T
    inverse_root = (eigenvectors * inverse_values) @ eigenvectors.conj().T
    support_basis = eigenvectors[:, positive]
    support = support_basis @ support_basis.conj().T
    return square_root, inverse_root, support, support_basis


def _condition_number(matrix: np.ndarray, tolerance: float) -> float:
    eigenvalues = np.linalg.eigvalsh((matrix + matrix.conj().T) / 2)
    positive = eigenvalues[eigenvalues > tolerance]
    return float(positive[-1] / positive[0]) if len(positive) else 1.0


def projector_frame_analysis(projectors: tuple[np.ndarray, ...]) -> np.ndarray:
    if not projectors:
        raise ValueError("at least one leaf projector is required")
    dimension = len(projectors[0])
    if any(projector.shape != (dimension, dimension) for projector in projectors):
        raise ValueError("all projectors must share a carrier")
    return np.vstack(projectors)


def polar_frame(projectors: tuple[np.ndarray, ...], tolerance: float = 1e-10) -> tuple[np.ndarray, np.ndarray]:
    analysis = projector_frame_analysis(projectors)
    frame = analysis.conj().T @ analysis
    _, inverse, _, _ = _psd_powers(frame, tolerance)
    return analysis @ inverse, frame


def relative_merge_isometry(
    left_frame: np.ndarray,
    right_frame: np.ndarray,
    *,
    tolerance: float = 1e-10,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    if left_frame.shape != right_frame.shape:
        raise ValueError("child frames must share a carrier")
    parent = left_frame + right_frame
    left_root, _, _, _ = _psd_powers(left_frame, tolerance)
    right_root, _, _, _ = _psd_powers(right_frame, tolerance)
    _, parent_inverse, parent_support, _ = _psd_powers(parent, tolerance)
    relative = np.vstack((left_root, right_root)) @ parent_inverse
    effect = parent_inverse @ left_frame @ parent_inverse
    effect = (effect + effect.conj().T) / 2
    return relative, effect, parent_support


def _block_diagonal(left: np.ndarray, right: np.ndarray) -> np.ndarray:
    output = np.zeros(
        (left.shape[0] + right.shape[0], left.shape[1] + right.shape[1]),
        dtype=complex,
    )
    output[: left.shape[0], : left.shape[1]] = left
    output[left.shape[0] :, left.shape[1] :] = right
    return output


def recursive_polar_chain(
    projectors: tuple[np.ndarray, ...],
    *,
    tolerance: float = 1e-10,
) -> tuple[np.ndarray, np.ndarray, list[tuple[np.ndarray, np.ndarray]]]:
    """Return the recursively factored polar, frame, and merge effects."""

    if not projectors or len(projectors) & (len(projectors) - 1):
        raise ValueError("a nonempty power-of-two leaf family is required")
    if len(projectors) == 1:
        polar, frame = polar_frame(projectors, tolerance)
        return polar, frame, []
    middle = len(projectors) // 2
    left_polar, left_frame, left_effects = recursive_polar_chain(
        projectors[:middle],
        tolerance=tolerance,
    )
    right_polar, right_frame, right_effects = recursive_polar_chain(
        projectors[middle:],
        tolerance=tolerance,
    )
    relative, effect, _ = relative_merge_isometry(
        left_frame,
        right_frame,
        tolerance=tolerance,
    )
    polar = _block_diagonal(left_polar, right_polar) @ relative
    return (
        polar,
        left_frame + right_frame,
        [*left_effects, *right_effects, (effect, left_frame + right_frame)],
    )


def audit_hierarchical_polar_chain(
    control_id: str,
    n: int,
    target: tuple[int, ...],
    labels: tuple[Label, ...],
    leaf_order: tuple[int, ...],
    *,
    tolerance: float = 1e-8,
) -> HierarchicalPolarControl:
    if len(leaf_order) != 4 or set(leaf_order) != set(range(4)):
        raise ValueError("the W4 control requires one ordering of four leaves")
    projectors = tuple(
        orientation_invariant_projector(target, labels, mask)
        for mask in leaf_order
    )
    left = projectors[:2]
    right = projectors[2:]
    left_polar, left_frame = polar_frame(left, tolerance)
    right_polar, right_frame = polar_frame(right, tolerance)
    relative, effect, parent_support = relative_merge_isometry(
        left_frame,
        right_frame,
        tolerance=tolerance,
    )
    composed = _block_diagonal(left_polar, right_polar) @ relative
    direct, parent_frame = polar_frame(projectors, tolerance)
    recursion_residual = float(np.linalg.norm(composed - direct, ord=2))
    merge_residual = float(
        np.linalg.norm(
            relative.conj().T @ relative - parent_support,
            ord=2,
        )
    )
    _, _, _, parent_basis = _psd_powers(parent_frame, tolerance)
    restricted_effect = parent_basis.conj().T @ effect @ parent_basis
    effect_eigenvalues = np.linalg.eigvalsh(
        (restricted_effect + restricted_effect.conj().T) / 2
    )
    fractional = tuple(
        float(value)
        for value in effect_eigenvalues
        if tolerance < value < 1 - tolerance
    )
    half_residual = max(
        (min(abs(value), abs(value - 0.5), abs(value - 1)) for value in effect_eigenvalues),
        default=0.0,
    )
    fractional_gap = min(
        (min(value, 1 - value) for value in fractional),
        default=0.5,
    )
    left_support_rank = int(
        np.count_nonzero(
            np.linalg.eigvalsh((left_frame + left_frame.conj().T) / 2)
            > tolerance
        )
    )
    right_support_rank = int(
        np.count_nonzero(
            np.linalg.eigvalsh((right_frame + right_frame.conj().T) / 2)
            > tolerance
        )
    )
    verified = bool(
        recursion_residual <= 100 * tolerance
        and merge_residual <= 100 * tolerance
        and effect_eigenvalues[0] >= -100 * tolerance
        and effect_eigenvalues[-1] <= 1 + 100 * tolerance
    )
    half_integral = bool(half_residual <= 100 * tolerance)
    return HierarchicalPolarControl(
        control_id=control_id,
        n=n,
        target_partition=target,
        labels=labels,
        leaf_order=leaf_order,
        orientation_count=4,
        carrier_dimension=len(projectors[0]),
        parent_support_rank=parent_basis.shape[1],
        left_child_support_rank=left_support_rank,
        right_child_support_rank=right_support_rank,
        parent_frame_condition_number=_condition_number(parent_frame, tolerance),
        left_child_frame_condition_number=_condition_number(left_frame, tolerance),
        right_child_frame_condition_number=_condition_number(right_frame, tolerance),
        child_frame_commutator_norm=float(
            np.linalg.norm(
                left_frame @ right_frame - right_frame @ left_frame,
                ord=2,
            )
        ),
        relative_effect_fractional_eigenvalues=fractional,
        relative_effect_minimum_fractional_gap=fractional_gap,
        relative_effect_half_integral_spectrum_residual=half_residual,
        relative_merge_isometry_residual=merge_residual,
        recursive_to_direct_polar_residual=recursion_residual,
        exact_hierarchical_polar_chain_verified=verified,
        finite_half_integral_relative_effect_observed=half_integral,
        status=(
            "exact-two-level-half-integral-polar-chain"
            if verified and half_integral
            else "exact-two-level-polar-chain-non-half-integral-effect"
            if verified
            else "hierarchical-polar-chain-validation-failure"
        ),
    )


def hierarchical_polar_scaling_record(n: int) -> HierarchicalPolarScalingRecord:
    if n < 5:
        raise ValueError("n must be at least five")
    copies = math.ceil(math.lgamma(n + 1) / math.log(2))
    leaf_count = 1 << copies
    return HierarchicalPolarScalingRecord(
        n=n,
        information_threshold_copy_count=copies,
        orientation_leaf_count_log2=copies,
        binary_tree_depth=copies,
        explicitly_compiled_node_count_decimal=str(leaf_count - 1),
        coherently_indexed_level_count=copies,
        base_pair_relative_sampler_polynomial=True,
        higher_level_relative_sampler_polynomial=False,
        typical_relative_effect_gap_proved=False,
        formal_mrs_sieve_model_uses_only_pairwise_state_isotypic_measurements=True,
        proposed_leaf_projector_acts_globally_on_all_source_labels=True,
        proposed_sampler_preserves_coherent_internal_labels=True,
        formal_mrs_sieve_theorem_directly_applies=False,
        status="k-level-relative-sampler-higher-level-ratios-open",
    )


def _finite_controls() -> list[HierarchicalPolarControl]:
    pairings = (
        (0, 1, 2, 3),
        (0, 2, 1, 3),
        (0, 3, 1, 2),
    )
    controls: list[HierarchicalPolarControl] = []
    for tuple_index, labels in enumerate(_w4_collision_free_labels()):
        for target in integer_partitions(4):
            if not any(
                float(
                    np.trace(
                        orientation_invariant_projector(target, labels, mask)
                    ).real
                )
                > 1e-8
                for mask in range(4)
            ):
                continue
            for pairing_index, leaf_order in enumerate(pairings):
                controls.append(
                    audit_hierarchical_polar_chain(
                        (
                            f"W4-{tuple_index}-{'-'.join(map(str, target))}-"
                            f"PAIRING-{pairing_index}"
                        ),
                        4,
                        target,
                        labels,
                        leaf_order,
                    )
                )
    return controls


def run_hierarchical_polar_tree() -> HierarchicalPolarTreeReport:
    controls = _finite_controls()
    scaling = [
        hierarchical_polar_scaling_record(n)
        for n in (5, 8, 16, 32, 64, 128, 256, 512)
    ]
    failures = sum(not row.exact_hierarchical_polar_chain_verified for row in controls)
    half_integral_failures = sum(
        not row.finite_half_integral_relative_effect_observed for row in controls
    )
    noncommuting = sum(row.child_frame_commutator_norm > 1e-8 for row in controls)
    fractional = [
        value
        for row in controls
        for value in row.relative_effect_fractional_eigenvalues
    ]
    verified = failures == 0
    return HierarchicalPolarTreeReport(
        created_at=utc_now(),
        theorem_contract={
            "polar_chain_rule": (
                "Q_T=(Q_L direct_sum Q_R)[S_L^(1/2);S_R^(1/2)]S_T^(-1/2)."
            ),
            "relative_isometry": (
                "W_(L,R)^*W_(L,R)=Pi_supp(S_T), with left effect "
                "C=S_T^(-1/2)S_LS_T^(-1/2)."
            ),
            "commuting_reduction": (
                "When all leaf projectors share an eigenbasis, C is the "
                "classical subtree count ratio t_L/t_T."
            ),
            "coherent_level_parallelism": (
                "For nested orientation subspaces, quotient labels address all "
                "nodes at one depth coherently, giving k controlled levels."
            ),
            "base_level": (
                "The pair-polar theorem implements level one with a constant "
                "singular gap for n>=5."
            ),
            "open_level": (
                "For level at least two, prove a typical spectral gap and a "
                "direct controlled circuit for the matrix-valued relative effect."
            ),
            "sieve_scope": (
                "The leaf E_epsilon already acts on the target and all k source "
                "representations, and internal labels remain coherent. This is "
                "outside the formal combine-two-states-and-measure-an-irrep "
                "transcript model, but no extended sieve separation is proved."
            ),
        },
        finite_controls=controls,
        scaling_records=scaling,
        proof_obligations=[
            {
                "obligation": "exact_polar_chain_rule",
                "resolved": verified,
                "resolution": (
                    "Substituting R_child=Q_child S_child^(1/2) gives the "
                    "identity; all complete W4 controls match the direct polar."
                ),
            },
            {
                "obligation": "coherent_polynomial_level_count",
                "resolved": True,
                "resolution": (
                    "A nested F_2^k flag has k levels and each quotient register "
                    "coherently indexes that level's nodes."
                ),
            },
            {
                "obligation": "base_pair_relative_sampler",
                "resolved": True,
                "resolution": (
                    "The companion pair-polar theorem supplies a constant-gap "
                    "implementation for every two-leaf node."
                ),
            },
            {
                "obligation": "higher_level_relative_effect_structure",
                "resolved": False,
                "resolution": (
                    "W4 effects are exactly projective or balanced, but no all-n "
                    "theorem controls spectra or coherent eigenbases at growing depth."
                ),
            },
            {
                "obligation": "formal_sieve_scope_audit",
                "resolved": True,
                "resolution": (
                    "The proposed primitive uses global all-register invariant "
                    "projectors and coherent internal labels, operations absent "
                    "from the paper's pairwise measured-transcript definition."
                ),
            },
            {
                "obligation": "extended_sieve_lower_bound_escape",
                "resolved": False,
                "resolution": (
                    "Syntactic noncoverage is not evidence of algorithmic power; "
                    "an equivalent simulation or stronger lower bound may exist."
                ),
            },
        ],
        adversarial_audit=[
            {
                "objection": "A binary tree requires compiling n!-many nodes.",
                "resolved": True,
                "resolution": (
                    "Not for a uniform nested orientation flag: quotient bits "
                    "coherently select all nodes at a level, so only k levels remain."
                ),
            },
            {
                "objection": "The chain rule removes every inverse square root.",
                "resolved": False,
                "resolution": (
                    "It replaces one absolute inverse by k relative isometries. "
                    "Higher-level relative implementations are the new obligation."
                ),
            },
            {
                "objection": "Finite half-integral effects imply an all-n count recursion.",
                "resolved": False,
                "resolution": (
                    "W4 has only four leaves and sparse active sectors. Typical "
                    "large-n frames may have genuinely continuous relative spectra."
                ),
            },
            {
                "objection": "Being outside the formal sieve definition proves the lower bound evaded.",
                "resolved": False,
                "resolution": (
                    "It proves only that the theorem cannot be cited directly. "
                    "The primitive may still admit a sieve simulation or a new no-go."
                ),
            },
        ],
        literature_links=[
            {
                "paper_id": "moore-russell-sniady-2007",
                "title": (
                    "On the impossibility of a quantum sieve algorithm for "
                    "graph isomorphism: unconditional results"
                ),
                "url": "https://arxiv.org/abs/quant-ph/0612089",
                "use": (
                    "Defines the excluded algorithm class as pairwise state "
                    "combination followed by measured isotypic labels and a "
                    "classical transcript."
                ),
                "external_theorem_not_reproved_here": True,
            }
        ],
        headline_metrics={
            "hierarchical_polar_chain_rule_theorem_count": 1,
            "matrix_valued_conditional_probability_reduction_count": 1,
            "coherent_k_level_compilation_theorem_count": 1,
            "finite_w4_control_count": len(controls),
            "finite_hierarchical_validation_failure_count": failures,
            "finite_half_integral_relative_effect_failure_count": half_integral_failures,
            "finite_noncommuting_child_frame_count": noncommuting,
            "finite_fractional_relative_effect_eigenvalue_count": len(fractional),
            "minimum_finite_fractional_relative_effect_gap": min(
                (min(value, 1 - value) for value in fractional),
                default=0.5,
            ),
            "maximum_recursive_to_direct_polar_residual": max(
                row.recursive_to_direct_polar_residual for row in controls
            ),
            "tail_n": scaling[-1].n,
            "tail_tree_depth": scaling[-1].binary_tree_depth,
            "higher_level_relative_sampler_count": 0,
            "typical_relative_effect_gap_theorem_count": 0,
            "global_nonorthogonal_sampler_count": 0,
            "polynomial_hidden_permutation_decoder_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "exact_hierarchical_polar_factorization_proved": verified,
            "exponential_node_compilation_required": False,
            "base_pair_level_polynomial": True,
            "higher_level_relative_sampler_polynomial": False,
            "typical_large_n_relative_effect_gap_proved": False,
            "formal_mrs_sieve_theorem_directly_applies": False,
            "extended_sieve_lower_bound_evaded": False,
            "global_pgm_circuit_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The absolute factorial-scale polar is now an exact k-level "
                "operator-valued conditional-sampling problem. The base level "
                "is polynomial and W4 level-two effects are simple, but no "
                "typical higher-level ratio theorem or circuit exists."
            ),
        },
        status=(
            "hierarchical-relative-polar-sampler-higher-level-open"
            if verified
            else "hierarchical-polar-chain-validation-failure"
        ),
        summary=(
            "Factored the global orientation polar into k coherently indexed "
            "binary relative-frame isometries. The first level is polynomial; "
            "all complete W4 level-two effects are projective or exactly "
            "balanced. The decisive open theorem is the typical large-n "
            "relative-effect spectrum and its direct circuit."
        ),
        falsifiers_triggered=[
            (
                "Do not require explicit compilation of every orientation-tree "
                "node; a nested flag addresses nodes coherently by level."
            ),
            (
                "Do not claim the chain rule alone removes whitening; it moves "
                "whitening into matrix-valued conditional frame ratios."
            ),
            (
                "Do not cite the Moore--Russell--Sniady theorem directly against "
                "this global coherent primitive, or claim noncoverage as success."
            ),
        ],
    )


def write_hierarchical_polar_tree_report(
    path: Path = REPORT_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = (
        "EXP-CODE-SELF-DUAL-WREATH-HIERARCHICAL-POLAR-TREE"
    ),
    registry_candidate_id: str = "CODE-COSET-COLLECTIVE",
    registry_result_id: str = "",
) -> dict[str, Any]:
    payload = asdict(run_hierarchical_polar_tree())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True))

    return payload


if __name__ == "__main__":
    report = write_hierarchical_polar_tree_report()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))

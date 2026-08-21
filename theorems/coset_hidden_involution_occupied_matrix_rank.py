"""Natural occupied-rank theorem for hidden-involution matrix CS blocks.

Let ``W`` be the unnormalized orbit-synthesis map on the source permutation
module ``Ind_B^L(1)``.  If ``x`` is the eigenvalue of ``W^*W`` under uniform
source dimension, the exact moment theorem gives

    E[(x-1)^2] = eta = (M-1)/2^k.

Every kernel direction contributes one to this centered second moment, so the
global kernel fraction is at most ``eta``.  In an ``L``-irrep block, write
``m_B`` for its source multiplicity and ``r`` for the rank of the matrix
Cosine-Sine overlap.  A block with ``r<=m_B/2`` has at least half of its source
space in the kernel.  Such blocks therefore occupy at most ``2 eta`` of total
source dimension.

The natural matrix-multiplicity theorem independently bounds the source
fraction in blocks with ``m_B<=T`` by ``delta_low``, for
``T=|S_n|^(k/4)``.  Thus all but ``delta_low+2 eta`` of source dimension lies
in blocks with

    m_B > T,       r > m_B/2 > T/2.

At ``k=ceil(log2(64M))``, at least ``29/32`` of alternative mass has
``x in [1/2,3/2]``.  Size-bias transfer proves alternative mass at least

    29/32 - (3/2)(delta_low + 2 eta)

in the huge occupied-rank blocks.  The stored family is above 0.85 from
``S_8`` onward.

This eliminates the possibility that natural huge multiplicity spaces are
almost entirely kernel.  It still does not construct a basis or circuit for
the occupied matrix blocks, nor prove that no succinct transform exists.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import numpy as np

from coset_hidden_involution_binary_decision_reduction import involution_class_size
from coset_hidden_involution_incidence_walk_boundary import incidence_matrix
from coset_hidden_involution_natural_matrix_multiplicity import (
    natural_matrix_multiplicity_scaling_record,
)
from coset_hidden_involution_orbit_synthesis_flatness import (
    exact_synthesis_centered_second_moment,
    flatness_copy_count,
)
from research_registry import utc_now


REPORT_PATH = Path(
    "research/representation/"
    "coset_hidden_involution_occupied_matrix_rank.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-COSET-HIDDEN-INVOLUTION-OCCUPIED-MATRIX-RANK"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


@dataclass(frozen=True)
class OccupiedRankFiniteControl:
    n: int
    transposition_count: int
    copy_count: int
    candidate_count: int
    source_dimension: int
    synthesis_rank: int
    kernel_dimension: int
    exact_kernel_fraction: float
    centered_second_moment: float
    theorem_kernel_fraction_upper_bound: float
    kernel_fraction_bound_verified: bool
    status: str


@dataclass(frozen=True)
class OccupiedRankScalingRecord:
    half_degree: int
    degree: int
    candidate_count_decimal: str
    copy_count: int
    multiplicity_threshold_log2: float
    occupied_rank_threshold_log2: float
    low_multiplicity_source_fraction_log2_upper_bound: float
    low_multiplicity_source_fraction_upper_bound: float
    synthesis_centered_second_moment: float
    source_kernel_fraction_upper_bound: float
    half_rank_deficient_block_source_fraction_upper_bound: float
    huge_half_rank_source_fraction_lower_bound: float
    flat_alternative_mass_lower_bound: float
    huge_occupied_rank_alternative_mass_lower_bound: float
    constant_alternative_mass_in_huge_occupied_rank_blocks: bool
    succinct_occupied_block_basis_constructed: bool
    status: str


@dataclass(frozen=True)
class OccupiedMatrixRankTheorem:
    kernel_moment_bound: str
    block_kernel_accounting: str
    multiplicity_intersection: str
    alternative_size_bias_transfer: str
    occupied_rank_conclusion: str
    scope_limit: str
    global_kernel_fraction_bound_proved: bool
    half_rank_block_fraction_bound_proved: bool
    constant_alternative_mass_in_huge_occupied_rank_blocks_proved: bool
    succinct_occupied_block_basis_constructed: bool
    matrix_cosine_sine_transform_compiled: bool
    binary_hidden_involution_detector_constructed: bool
    theorem_verified: bool
    status: str


@dataclass(frozen=True)
class OccupiedMatrixRankReport:
    created_at: str
    theorem_contract: dict[str, Any]
    finite_controls: list[OccupiedRankFiniteControl]
    scaling_records: list[OccupiedRankScalingRecord]
    theorem: OccupiedMatrixRankTheorem
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def audit_occupied_rank_kernel(
    n: int,
    transposition_count: int,
    copy_count: int,
    *,
    tolerance: float = 1e-9,
) -> OccupiedRankFiniteControl:
    incidence, _ = incidence_matrix(n, transposition_count, copy_count)
    candidates = involution_class_size(n, transposition_count)
    synthesis = incidence / math.sqrt(2**copy_count)
    singular_values = np.linalg.svd(synthesis, compute_uv=False)
    rank = int(np.count_nonzero(singular_values > tolerance))
    source_dimension = incidence.shape[1]
    kernel = source_dimension - rank
    fraction = kernel / source_dimension
    moment = float(
        exact_synthesis_centered_second_moment(candidates, copy_count)
    )
    verified = fraction <= moment + 100 * tolerance
    return OccupiedRankFiniteControl(
        n=n,
        transposition_count=transposition_count,
        copy_count=copy_count,
        candidate_count=candidates,
        source_dimension=source_dimension,
        synthesis_rank=rank,
        kernel_dimension=kernel,
        exact_kernel_fraction=fraction,
        centered_second_moment=moment,
        theorem_kernel_fraction_upper_bound=moment,
        kernel_fraction_bound_verified=verified,
        status=(
            "exact-kernel-fraction-below-second-moment"
            if verified
            else "occupied-rank-kernel-control-failure"
        ),
    )


def occupied_rank_scaling_record(half_degree: int) -> OccupiedRankScalingRecord:
    if half_degree < 2:
        raise ValueError("half_degree must be at least two")
    n = 2 * half_degree
    candidates = involution_class_size(n, half_degree)
    copies = flatness_copy_count(candidates)
    multiplicity = natural_matrix_multiplicity_scaling_record(half_degree)
    eta = float(exact_synthesis_centered_second_moment(candidates, copies))
    low = multiplicity.low_multiplicity_source_fraction_upper_bound
    half_rank_bad = min(1.0, 2.0 * eta)
    good_source = max(0.0, 1.0 - low - half_rank_bad)
    flat_mass = 29.0 / 32.0
    good_alternative = max(
        0.0,
        flat_mass - 1.5 * min(1.0, low + half_rank_bad),
    )
    constant = good_alternative >= 0.8
    return OccupiedRankScalingRecord(
        half_degree=half_degree,
        degree=n,
        candidate_count_decimal=str(candidates),
        copy_count=copies,
        multiplicity_threshold_log2=multiplicity.multiplicity_threshold_log2,
        occupied_rank_threshold_log2=(
            multiplicity.multiplicity_threshold_log2 - 1.0
        ),
        low_multiplicity_source_fraction_log2_upper_bound=(
            multiplicity.low_multiplicity_source_fraction_log2_upper_bound
        ),
        low_multiplicity_source_fraction_upper_bound=low,
        synthesis_centered_second_moment=eta,
        source_kernel_fraction_upper_bound=eta,
        half_rank_deficient_block_source_fraction_upper_bound=half_rank_bad,
        huge_half_rank_source_fraction_lower_bound=good_source,
        flat_alternative_mass_lower_bound=flat_mass,
        huge_occupied_rank_alternative_mass_lower_bound=good_alternative,
        constant_alternative_mass_in_huge_occupied_rank_blocks=constant,
        succinct_occupied_block_basis_constructed=False,
        status=(
            "constant-alternative-mass-in-huge-occupied-matrix-rank"
            if constant
            else "finite-preasymptotic-occupied-rank-bound"
        ),
    )


def build_occupied_matrix_rank_report(
    *,
    scaling_half_degrees: tuple[int, ...] = (4, 6, 8, 12, 16, 32, 64),
) -> OccupiedMatrixRankReport:
    finite = [
        audit_occupied_rank_kernel(3, 1, copy_count)
        for copy_count in (1, 2)
    ]
    scaling = [occupied_rank_scaling_record(value) for value in scaling_half_degrees]
    exact = all(row.kernel_fraction_bound_verified for row in finite)
    constant = all(
        row.constant_alternative_mass_in_huge_occupied_rank_blocks
        for row in scaling
    )
    theorem = OccupiedMatrixRankTheorem(
        kernel_moment_bound=(
            "Kernel fraction is at most E[(x-1)^2]=(M-1)/2^k because "
            "every zero eigenvalue contributes one."
        ),
        block_kernel_accounting=(
            "A block with CS rank r<=m_B/2 contributes at least half its "
            "source dimension to the kernel, so such blocks have source "
            "fraction at most 2 eta."
        ),
        multiplicity_intersection=(
            "Intersect with the proved m_B>|S_n|^(k/4) source mass; the "
            "remaining blocks have r>|S_n|^(k/4)/2."
        ),
        alternative_size_bias_transfer=(
            "On the x<=3/2 flat window, alternative bad-block mass is at "
            "most 1.5 times bad source dimension, plus the 3/32 tail."
        ),
        occupied_rank_conclusion=(
            "A constant natural alternative mass lies in blocks of occupied "
            "matrix rank greater than |S_n|^(k/4)/2."
        ),
        scope_limit=(
            "Rank does not imply a hard basis change; no circuit or classical "
            "lower bound follows."
        ),
        global_kernel_fraction_bound_proved=exact,
        half_rank_block_fraction_bound_proved=True,
        constant_alternative_mass_in_huge_occupied_rank_blocks_proved=constant,
        succinct_occupied_block_basis_constructed=False,
        matrix_cosine_sine_transform_compiled=False,
        binary_hidden_involution_detector_constructed=False,
        theorem_verified=exact and constant,
        status=(
            "natural-huge-occupied-matrix-rank-proved-basis-transform-open"
            if exact and constant
            else "occupied-matrix-rank-control-failure"
        ),
    )
    return OccupiedMatrixRankReport(
        created_at=utc_now(),
        theorem_contract={
            "source_spectral_law": (
                "Uniform source dimension includes the synthesis kernel and has "
                "exact mean one and centered second moment eta."
            ),
            "block_rank": (
                "In each L-irrep, W is identity on the carrier tensored with a "
                "matrix from the B-fixed source multiplicity to the A-fixed "
                "physical multiplicity; r is that matrix rank."
            ),
            "claim_boundary": (
                "Proves occupied dimension on natural mass, not transform "
                "complexity or a speedup."
            ),
        },
        finite_controls=finite,
        scaling_records=scaling,
        theorem=theorem,
        proof_obligations=[
            {
                "id": "PO-HIDDEN-INVOLUTION-OCCUPIED-BLOCK-BASIS",
                "statement": (
                    "Find a succinct basis/recoupling description for the huge "
                    "occupied A/B invariant overlap blocks."
                ),
                "resolved": False,
            },
            {
                "id": "PO-HIDDEN-INVOLUTION-OCCUPIED-BLOCK-CS-TRANSFORM",
                "statement": (
                    "Compile their matrix Cosine-Sine transform with polynomial "
                    "normalization and coherent physical label handling."
                ),
                "resolved": False,
            },
        ],
        adversarial_audit=[
            {
                "challenge": "Huge B-fixed blocks could be almost entirely kernel.",
                "answer": (
                    "Resolved negatively on natural mass: the global kernel "
                    "fraction is at most 1/64 and half-rank blocks at most 1/32."
                ),
                "resolved": True,
            },
            {
                "challenge": "High occupied rank proves the transform is hard.",
                "answer": (
                    "False: QFTs and Schur transforms have high rank but succinct "
                    "circuits. Basis and matrix structure remain decisive."
                ),
                "resolved": True,
            },
            {
                "challenge": "A few flat eigenvectors could carry all alternative mass.",
                "answer": (
                    "The block dimension and kernel accounting force constant "
                    "alternative mass into huge-rank blocks after size bias."
                ),
                "resolved": True,
            },
        ],
        headline_metrics={
            "finite_kernel_control_count": len(finite),
            "finite_kernel_control_failure_count": sum(
                not row.kernel_fraction_bound_verified for row in finite
            ),
            "constant_huge_occupied_rank_scaling_count": sum(
                row.constant_alternative_mass_in_huge_occupied_rank_blocks
                for row in scaling
            ),
            "minimum_huge_occupied_rank_alternative_mass_lower_bound": min(
                row.huge_occupied_rank_alternative_mass_lower_bound
                for row in scaling
            ),
            "tail_occupied_rank_threshold_log2": (
                scaling[-1].occupied_rank_threshold_log2
            ),
            "tail_source_kernel_fraction_upper_bound": (
                scaling[-1].source_kernel_fraction_upper_bound
            ),
            "succinct_occupied_block_basis_count": 0,
            "matrix_cosine_sine_transform_compiler_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "global_source_kernel_fraction_small": exact,
            "half_rank_deficient_blocks_negligible": exact,
            "constant_alternative_mass_in_huge_occupied_rank_blocks": constant,
            "occupied_cosine_sine_rank_lower_bound_proved": exact and constant,
            "succinct_occupied_block_basis_constructed": False,
            "matrix_cosine_sine_transform_compiled": False,
            "binary_hidden_involution_detector_constructed": False,
            "speedup_claim_allowed": False,
            "reason": (
                "Natural signal occupies enormous-rank matrix blocks, but their "
                "basis, principal-angle transform, and physical implementation "
                "remain unresolved."
            ),
        },
        status=theorem.status,
        summary=(
            "Combined exact synthesis variance, source multiplicity counting, "
            "and alternative size bias to prove constant natural mass in "
            "enormous occupied matrix Cosine-Sine blocks."
        ),
        falsifiers_triggered=[
            "The natural high-multiplicity blocks are not mostly synthesis kernel.",
            "A scalar or bounded-rank treatment cannot be justified by natural-mass trimming.",
            "Occupied rank alone remains insufficient evidence of computational hardness.",
        ],
    )


def write_occupied_matrix_rank_report(
    output_path: Path = REPORT_PATH,
    **kwargs: Any,
) -> dict[str, Any]:
    payload = asdict(build_occupied_matrix_rank_report(**kwargs))
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return payload


if __name__ == "__main__":
    report = write_occupied_matrix_rank_report()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))

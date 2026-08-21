"""Natural-mass theorem for matrix-valued double-coset multiplicities.

The double-coset row-polar reduction writes the source as the permutation
module ``Ind_B^L(1)`` for

    L = S_n^k x S_n,
    B = {(eps_1 r,...,eps_k r;r): r in C_G(h), eps_i in <h>}.

For an irreducible ``pi`` of ``L``, let ``m_B(pi)=dim(pi^B)``.  The fraction
of the source module carried by blocks with ``m_B(pi)<=T`` is at most

    T * (sum_(lambda|-n) d_lambda)^(k+1) / |L:B|.       (1)

Robinson--Schensted gives the exact identity

    sum_lambda d_lambda = I_n,

where ``I_n`` is the number of involutions in ``S_n``.  Since
``|L:B|=M(n!/2)^k`` for a conjugacy class of ``M`` involutions, (1) is an
explicit all-``n`` theorem.

At the orbit-flatness copy count ``k=ceil(log2(64M))``, choose
``T=(n!)^(k/4)``.  The resulting low-multiplicity source fraction is already
below ``2^-8`` at ``n=8`` and then falls super-exponentially.  The physical
alternative law is the exact size bias of the source synthesis eigenvalue
``x``.  At least ``29/32`` of alternative mass has ``x in [1/2,3/2]``.
Therefore the alternative mass in blocks with ``m_B>T`` is at least

    29/32 - (3/2) delta_low.                            (2)

This proves that matrix-valued source multiplicity is not a negligible
exceptional sector.  It does not prove that the occupied Cosine-Sine rank is
large inside each block, that a succinct multiplicity basis is impossible,
or that the binary hidden-involution problem is hard.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from functools import lru_cache
from pathlib import Path
from typing import Any

from coset_hidden_involution_binary_decision_reduction import involution_class_size
from coset_hidden_involution_orbit_synthesis_flatness import flatness_copy_count
from representation_obstruction import hook_length_dimension, integer_partitions
from research_registry import utc_now


REPORT_PATH = Path(
    "research/representation/"
    "coset_hidden_involution_natural_matrix_multiplicity.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-COSET-HIDDEN-INVOLUTION-NATURAL-MATRIX-MULTIPLICITY"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


@dataclass(frozen=True)
class InvolutionDimensionSumControl:
    n: int
    partition_count: int
    exact_irrep_dimension_sum: int
    involution_recurrence_count: int
    robinson_schensted_dimension_sum_verified: bool
    status: str


@dataclass(frozen=True)
class NaturalMatrixMultiplicityScalingRecord:
    half_degree: int
    degree: int
    group_order_log2: float
    candidate_count_decimal: str
    copy_count: int
    source_module_dimension_log2: float
    symmetric_group_involution_count_decimal: str
    symmetric_group_involution_count_log2: float
    multiplicity_threshold_formula: str
    multiplicity_threshold_log2: float
    low_multiplicity_source_fraction_log2_upper_bound: float
    low_multiplicity_source_fraction_upper_bound: float
    flat_alternative_mass_lower_bound: float
    high_multiplicity_alternative_mass_lower_bound: float
    high_multiplicity_threshold_superpolynomial: bool
    high_multiplicity_blocks_carry_constant_alternative_mass: bool
    occupied_cosine_sine_rank_lower_bound_proved: bool
    status: str


@dataclass(frozen=True)
class NaturalMatrixMultiplicityTheorem:
    source_module: str
    block_multiplicity: str
    low_multiplicity_dimension_bound: str
    involution_dimension_sum: str
    natural_threshold: str
    alternative_transfer: str
    conclusion: str
    scope_limit: str
    exact_dimension_bound_proved: bool
    robinson_schensted_sum_used: bool
    constant_alternative_mass_in_huge_multiplicity_blocks_proved: bool
    occupied_cosine_sine_rank_lower_bound_proved: bool
    matrix_cosine_sine_transform_compiled: bool
    binary_hidden_involution_detector_constructed: bool
    theorem_verified: bool
    status: str


@dataclass(frozen=True)
class NaturalMatrixMultiplicityReport:
    created_at: str
    theorem_contract: dict[str, Any]
    dimension_sum_controls: list[InvolutionDimensionSumControl]
    scaling_records: list[NaturalMatrixMultiplicityScalingRecord]
    theorem: NaturalMatrixMultiplicityTheorem
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


@lru_cache(maxsize=None)
def symmetric_group_involution_count(n: int) -> int:
    """Return ``I_n=I_(n-1)+(n-1)I_(n-2)`` with ``I_0=I_1=1``."""

    if n < 0:
        raise ValueError("n must be nonnegative")
    if n <= 1:
        return 1
    return symmetric_group_involution_count(n - 1) + (n - 1) * (
        symmetric_group_involution_count(n - 2)
    )


def audit_involution_dimension_sum(n: int) -> InvolutionDimensionSumControl:
    if n < 1:
        raise ValueError("n must be positive")
    dimensions = tuple(
        hook_length_dimension(partition) for partition in integer_partitions(n)
    )
    total = sum(dimensions)
    involutions = symmetric_group_involution_count(n)
    exact = total == involutions
    return InvolutionDimensionSumControl(
        n=n,
        partition_count=len(dimensions),
        exact_irrep_dimension_sum=total,
        involution_recurrence_count=involutions,
        robinson_schensted_dimension_sum_verified=exact,
        status=(
            "exact-robinson-schensted-dimension-sum-verified"
            if exact
            else "involution-dimension-sum-control-failure"
        ),
    )


def low_source_multiplicity_fraction_log2_bound(
    n: int,
    copy_count: int,
    multiplicity_threshold_log2: float,
) -> float:
    """Log bound from ``T (sum d_lambda)^(k+1) / |L:B|``."""

    if n < 2 or copy_count < 1:
        raise ValueError("n>=2 and positive copy count are required")
    if multiplicity_threshold_log2 < 0:
        raise ValueError("multiplicity threshold must be at least one")
    group_log2 = math.lgamma(n + 1) / math.log(2)
    candidate_log2 = math.log2(involution_class_size(n, n // 2))
    involution_sum_log2 = math.log2(symmetric_group_involution_count(n))
    source_dimension_log2 = candidate_log2 + copy_count * (group_log2 - 1.0)
    return (
        multiplicity_threshold_log2
        + (copy_count + 1) * involution_sum_log2
        - source_dimension_log2
    )


def natural_matrix_multiplicity_scaling_record(
    half_degree: int,
) -> NaturalMatrixMultiplicityScalingRecord:
    if half_degree < 2:
        raise ValueError("half_degree must be at least two")
    n = 2 * half_degree
    group_log2 = math.lgamma(n + 1) / math.log(2)
    candidates = involution_class_size(n, half_degree)
    copies = flatness_copy_count(candidates)
    source_dimension_log2 = math.log2(candidates) + copies * (group_log2 - 1.0)
    involutions = symmetric_group_involution_count(n)
    involution_log2 = math.log2(involutions)
    threshold_log2 = copies * group_log2 / 4.0
    low_log2 = low_source_multiplicity_fraction_log2_bound(
        n, copies, threshold_log2
    )
    low = min(1.0, 2**low_log2) if low_log2 > -1074 else 0.0
    flat_mass = 29.0 / 32.0
    high_mass = max(0.0, flat_mass - 1.5 * low)
    constant = high_mass >= 0.9
    return NaturalMatrixMultiplicityScalingRecord(
        half_degree=half_degree,
        degree=n,
        group_order_log2=group_log2,
        candidate_count_decimal=str(candidates),
        copy_count=copies,
        source_module_dimension_log2=source_dimension_log2,
        symmetric_group_involution_count_decimal=str(involutions),
        symmetric_group_involution_count_log2=involution_log2,
        multiplicity_threshold_formula="T=|S_n|^(k/4)",
        multiplicity_threshold_log2=threshold_log2,
        low_multiplicity_source_fraction_log2_upper_bound=low_log2,
        low_multiplicity_source_fraction_upper_bound=low,
        flat_alternative_mass_lower_bound=flat_mass,
        high_multiplicity_alternative_mass_lower_bound=high_mass,
        high_multiplicity_threshold_superpolynomial=True,
        high_multiplicity_blocks_carry_constant_alternative_mass=constant,
        occupied_cosine_sine_rank_lower_bound_proved=False,
        status=(
            "constant-alternative-mass-in-huge-matrix-blocks"
            if constant
            else "finite-preasymptotic-multiplicity-bound"
        ),
    )


def build_natural_matrix_multiplicity_report(
    *,
    control_degrees: tuple[int, ...] = (3, 4, 5, 6, 7, 8),
    scaling_half_degrees: tuple[int, ...] = (4, 6, 8, 12, 16, 32, 64),
) -> NaturalMatrixMultiplicityReport:
    controls = [audit_involution_dimension_sum(n) for n in control_degrees]
    scaling = [
        natural_matrix_multiplicity_scaling_record(value)
        for value in scaling_half_degrees
    ]
    exact = all(row.robinson_schensted_dimension_sum_verified for row in controls)
    constant = all(
        row.high_multiplicity_blocks_carry_constant_alternative_mass
        for row in scaling
    )
    theorem = NaturalMatrixMultiplicityTheorem(
        source_module="The source is Ind_B^L(1) with dimension M(|S_n|/2)^k.",
        block_multiplicity="Each L-irrep pi occurs with m_B(pi)=dim(pi^B).",
        low_multiplicity_dimension_bound=(
            "The source fraction in m_B<=T blocks is at most "
            "T (sum_lambda d_lambda)^(k+1)/|L:B|."
        ),
        involution_dimension_sum=(
            "Robinson--Schensted gives sum_lambda d_lambda=I_n, the exact "
            "number of involutions in S_n."
        ),
        natural_threshold=(
            "At k=ceil(log2(64M)), set T=|S_n|^(k/4); the low-multiplicity "
            "source fraction vanishes super-exponentially."
        ),
        alternative_transfer=(
            "The alternative is the x-size-biased source law, and at least "
            "29/32 of its mass has x<=3/2, giving high-block mass at least "
            "29/32-(3/2)delta_low."
        ),
        conclusion=(
            "Huge matrix B-fixed spaces carry constant natural alternative "
            "mass; they cannot be discarded as exceptional sectors."
        ),
        scope_limit=(
            "No lower bound is proved on occupied Cosine-Sine rank inside a "
            "block, transform complexity, or classical simulation."
        ),
        exact_dimension_bound_proved=True,
        robinson_schensted_sum_used=exact,
        constant_alternative_mass_in_huge_multiplicity_blocks_proved=constant,
        occupied_cosine_sine_rank_lower_bound_proved=False,
        matrix_cosine_sine_transform_compiled=False,
        binary_hidden_involution_detector_constructed=False,
        theorem_verified=exact and constant,
        status=(
            "natural-huge-matrix-multiplicity-mass-proved-occupied-rank-open"
            if exact and constant
            else "natural-matrix-multiplicity-control-failure"
        ),
    )
    return NaturalMatrixMultiplicityReport(
        created_at=utc_now(),
        theorem_contract={
            "module_law": (
                "Fourier block weights are representation dimensions times "
                "B-fixed multiplicities in the exact permutation module L/B."
            ),
            "flatness_dependency": (
                "Uses the proved 29/32 alternative x-size-biased flatness at "
                "k=ceil(log2(64M))."
            ),
            "threshold_scope": (
                "The multiplicity threshold is a counting theorem, not a claim "
                "that all those directions are in the synthesis support."
            ),
        },
        dimension_sum_controls=controls,
        scaling_records=scaling,
        theorem=theorem,
        proof_obligations=[
            {
                "id": "PO-HIDDEN-INVOLUTION-OCCUPIED-CS-RANK",
                "statement": (
                    "Lower-bound the rank or entropy of the nonzero principal-"
                    "angle spectrum inside naturally occupied high-multiplicity "
                    "L blocks."
                ),
                "resolved": False,
            },
            {
                "id": "PO-HIDDEN-INVOLUTION-MATRIX-CS-BASIS",
                "statement": (
                    "Construct a succinct basis and direct Cosine-Sine transform "
                    "for the A/B invariant spaces, or prove a natural access "
                    "obstruction."
                ),
                "resolved": False,
            },
        ],
        adversarial_audit=[
            {
                "challenge": "Non-multiplicity-free blocks might have negligible source mass.",
                "answer": (
                    "Resolved negatively: blocks below |S_n|^(k/4) multiplicity "
                    "have super-exponentially vanishing source fraction."
                ),
                "resolved": True,
            },
            {
                "challenge": "Source dimension mass need not transfer to the alternative.",
                "answer": (
                    "The exact size-bias law and the x<=3/2 flat window transfer "
                    "all but at most 3/32 plus 1.5 delta_low."
                ),
                "resolved": True,
            },
            {
                "challenge": "Huge m_B means the polar has huge occupied rank.",
                "answer": (
                    "Not proved. Most B-fixed directions could be kernel or admit "
                    "a succinct structured basis."
                ),
                "resolved": True,
            },
            {
                "challenge": "Large matrix blocks imply quantum hardness.",
                "answer": (
                    "False: representation-theoretic transforms routinely act on "
                    "exponentially large spaces with polynomial circuits."
                ),
                "resolved": True,
            },
        ],
        headline_metrics={
            "robinson_schensted_control_count": len(controls),
            "robinson_schensted_control_failure_count": sum(
                not row.robinson_schensted_dimension_sum_verified for row in controls
            ),
            "constant_high_multiplicity_alternative_mass_scaling_count": sum(
                row.high_multiplicity_blocks_carry_constant_alternative_mass
                for row in scaling
            ),
            "minimum_high_multiplicity_alternative_mass_lower_bound": min(
                row.high_multiplicity_alternative_mass_lower_bound
                for row in scaling
            ),
            "tail_multiplicity_threshold_log2": scaling[-1].multiplicity_threshold_log2,
            "tail_low_multiplicity_fraction_log2_upper_bound": (
                scaling[-1].low_multiplicity_source_fraction_log2_upper_bound
            ),
            "occupied_cosine_sine_rank_theorem_count": 0,
            "matrix_cosine_sine_transform_compiler_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "natural_matrix_multiplicity_mass_proved": exact and constant,
            "low_multiplicity_blocks_negligible_on_alternative": exact and constant,
            "scalar_spherical_transform_sufficient": False,
            "occupied_cosine_sine_rank_lower_bound_proved": False,
            "matrix_cosine_sine_transform_compiled": False,
            "binary_hidden_involution_detector_constructed": False,
            "speedup_claim_allowed": False,
            "reason": (
                "Natural signal reaches enormous matrix multiplicity blocks, but "
                "their occupied principal-angle rank and efficient transform remain open."
            ),
        },
        status=theorem.status,
        summary=(
            "Proved by exact module counting and alternative size bias that huge "
            "B-fixed matrix blocks carry constant natural mass, eliminating the "
            "possibility that non-scalar double-coset structure is negligible."
        ),
        falsifiers_triggered=[
            "Finite non-Gelfand witnesses were not enough; the natural-mass counting theorem is required.",
            "Scalar spherical processing cannot be justified by trimming all high-multiplicity source blocks.",
            "Ambient multiplicity alone does not certify occupied rank or computational hardness.",
        ],
    )


def write_natural_matrix_multiplicity_report(
    output_path: Path = REPORT_PATH,
    **kwargs: Any,
) -> dict[str, Any]:
    payload = asdict(build_natural_matrix_multiplicity_report(**kwargs))
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return payload


if __name__ == "__main__":
    report = write_natural_matrix_multiplicity_report()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))

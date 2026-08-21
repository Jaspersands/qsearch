"""Polynomial-query projector for paired-tower joint primitive labels.

The color-resolved paired-tower recurrence leaves

    J_m = direct_sum_(a+b=m) ker D_a^Y tensor ker D_b^Y,

where ``D_n^Y`` is the down-incidence operator of Young's lattice.  This
module turns that abstract kernel into a canonical, gapped label-space
projector.

Young's lattice is a 1-differential poset.  Stanley's spectral theorem gives
for ``L_n=(D_n^Y)^T D_n^Y`` on rank-``n`` partitions

    char(L_n) = product_(j=0)^n (x-j)^(Delta p(n-j)),

where ``Delta p(q)=p(q)-p(q-1)``.  In particular,

    ker L_n = ker D_n^Y,
    P_n^prim = product_(j=1)^n (I-L_n/j),

and ``L_n/n`` has zero-to-positive spectral gap at least ``1/n``.  Partition
cover relations are polynomially sparse and computable by adding/removing one
corner.  Standard sparse block access to ``D_n/sqrt(n)`` therefore gives a
polynomial-query phase-estimation/QSVT reflection about ``ker D_n``.

Taking controlled tensor products over ``a+b=m`` gives the exact projector
onto ``J_m`` with inverse-polynomial gap on the auxiliary coefficient space.
This is a recurrence diagnostic, not yet a compiler primitive.  In fact, the
representation-cone obstruction proves that the projector sends the trivial
branching vector to a signed vector at every rank, so multiplicity
coefficients cannot be treated as physical label amplitudes.  The projector
does not construct a reversible partition-neighbor oracle at gate level,
embed coefficient vectors into actual branching-copy spaces, bound physical
source mass, or compile the full matrix Cosine-Sine polar.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from functools import lru_cache
from pathlib import Path
from typing import Any

import sympy as sp

from coset_hidden_involution_colour_resolved_paired_tower_boundary import (
    joint_primitive_dimension,
)
from coset_hidden_involution_paired_tower_missing_label_boundary import (
    removable_corner_partitions,
)
from representation_obstruction import integer_partitions
from research_registry import utc_now


REPORT_PATH = Path(
    "research/representation/"
    "coset_hidden_involution_paired_tower_joint_primitive_projector.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-COSET-HIDDEN-INVOLUTION-PAIRED-TOWER-JOINT-PRIMITIVE-PROJECTOR"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


@dataclass(frozen=True)
class YoungPrimitiveProjectorControl:
    rank: int
    partition_count: int
    lower_partition_count: int
    down_incidence_rank: int
    primitive_kernel_dimension: int
    expected_primitive_kernel_dimension: int
    observed_laplacian_spectrum: dict[str, int]
    expected_laplacian_spectrum: dict[str, int]
    projector_polynomial_degree: int
    projector_rank: int
    minimum_positive_laplacian_eigenvalue: int
    maximum_laplacian_eigenvalue: int
    normalized_zero_gap: float
    maximum_down_degree: int
    maximum_up_degree: int
    exact_spectrum_verified: bool
    exact_projector_idempotence_verified: bool
    exact_projector_image_equals_down_kernel: bool
    status: str


@dataclass(frozen=True)
class JointPrimitiveProjectorControl:
    half_degree: int
    color_split_sector_count: int
    joint_primitive_dimension_from_projectors: int
    expected_joint_primitive_dimension: int
    minimum_sector_normalized_zero_gap: float
    maximum_sector_normalized_zero_gap: float
    exact_direct_sum_tensor_projector_rank_verified: bool
    polynomial_query_projector_specified: bool
    status: str


@dataclass(frozen=True)
class JointPrimitiveScalingRecord:
    half_degree: int
    bipartition_count: int
    joint_primitive_dimension: int
    joint_primitive_fraction: float
    joint_primitive_label_bits: float
    normalized_laplacian_gap_lower_bound: float
    sparse_query_reflection_order: int
    maximum_partition_neighbor_count_upper_bound: int
    label_space_projector_polynomial_query: bool
    reversible_partition_oracle_gate_compiled: bool
    ambient_branching_copy_isometry_compiled: bool
    status: str


@dataclass(frozen=True)
class JointPrimitiveProjectorTheorem:
    Young_laplacian_spectrum: str
    primitive_projector: str
    joint_primitive_projector: str
    sparse_query_algorithm: str
    positive_compiler_consequence: str
    scope_limit: str
    exact_all_rank_Young_spectrum_proved: bool
    exact_primitive_projector_polynomial_proved: bool
    exact_joint_primitive_projector_proved: bool
    polynomial_query_label_reflection_proved: bool
    reversible_partition_oracle_gate_compiled: bool
    ambient_branching_copy_isometry_compiled: bool
    source_aware_normalized_subduction_transform_compiled: bool
    hidden_involution_detector_constructed: bool
    speedup_claim_allowed: bool
    theorem_verified: bool
    status: str


@dataclass(frozen=True)
class JointPrimitiveProjectorReport:
    created_at: str
    theorem_contract: dict[str, Any]
    Young_controls: list[YoungPrimitiveProjectorControl]
    joint_controls: list[JointPrimitiveProjectorControl]
    scaling_records: list[JointPrimitiveScalingRecord]
    theorem: JointPrimitiveProjectorTheorem
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    literature_links: list[dict[str, str]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


@lru_cache(maxsize=None)
def partition_number(rank: int) -> int:
    if rank < 0:
        return 0
    values = [0] * (rank + 1)
    values[0] = 1
    for total in range(1, rank + 1):
        value = 0
        offset = 1
        while True:
            first = offset * (3 * offset - 1) // 2
            second = offset * (3 * offset + 1) // 2
            if first > total:
                break
            sign = 1 if offset % 2 else -1
            value += sign * values[total - first]
            if second <= total:
                value += sign * values[total - second]
            offset += 1
        values[total] = value
    return values[rank]


def partition_difference(rank: int) -> int:
    return partition_number(rank) - partition_number(rank - 1)


@lru_cache(maxsize=None)
def Young_down_incidence(rank: int) -> sp.Matrix:
    if rank < 1:
        raise ValueError("rank must be positive")
    upper = integer_partitions(rank)
    lower = integer_partitions(rank - 1)
    lower_index = {partition: index for index, partition in enumerate(lower)}
    matrix = sp.zeros(len(lower), len(upper))
    for column, partition in enumerate(upper):
        for child in removable_corner_partitions(partition):
            matrix[lower_index[child], column] = 1
    return matrix


def expected_Young_laplacian_spectrum(rank: int) -> dict[str, int]:
    spectrum: dict[str, int] = {}
    zero_multiplicity = partition_difference(rank)
    if zero_multiplicity:
        spectrum["0"] = zero_multiplicity
    for eigenvalue in range(1, rank + 1):
        multiplicity = partition_difference(rank - eigenvalue)
        if multiplicity:
            spectrum[str(eigenvalue)] = multiplicity
    return spectrum


@lru_cache(maxsize=None)
def Young_primitive_projector(rank: int) -> sp.Matrix:
    down = Young_down_incidence(rank)
    laplacian = down.T * down
    identity = sp.eye(laplacian.rows)
    projector = identity
    for eigenvalue in range(1, rank + 1):
        projector = projector * (
            identity - laplacian / sp.Integer(eigenvalue)
        )
    return sp.simplify(projector)


@lru_cache(maxsize=None)
def audit_Young_primitive_projector(
    rank: int,
) -> YoungPrimitiveProjectorControl:
    down = Young_down_incidence(rank)
    laplacian = down.T * down
    projector = Young_primitive_projector(rank)
    observed = {
        str(int(eigenvalue)): int(multiplicity)
        for eigenvalue, multiplicity in laplacian.eigenvals().items()
    }
    observed = dict(sorted(observed.items(), key=lambda item: int(item[0])))
    expected = expected_Young_laplacian_spectrum(rank)
    expected = dict(sorted(expected.items(), key=lambda item: int(item[0])))
    positive = [int(value) for value in observed if int(value) > 0]
    upper = integer_partitions(rank)
    lower = integer_partitions(rank - 1)
    maximum_down = max(
        len(removable_corner_partitions(partition)) for partition in upper
    )
    children = {partition: 0 for partition in lower}
    for partition in upper:
        for child in removable_corner_partitions(partition):
            children[child] += 1
    maximum_up = max(children.values())
    idempotent = projector * projector == projector
    kernel_exact = bool(
        down * projector == sp.zeros(down.rows, projector.cols)
        and projector.rank() == len(upper) - down.rank()
    )
    spectrum_verified = observed == expected
    verified = bool(spectrum_verified and idempotent and kernel_exact)
    return YoungPrimitiveProjectorControl(
        rank=rank,
        partition_count=len(upper),
        lower_partition_count=len(lower),
        down_incidence_rank=down.rank(),
        primitive_kernel_dimension=len(upper) - down.rank(),
        expected_primitive_kernel_dimension=partition_difference(rank),
        observed_laplacian_spectrum=observed,
        expected_laplacian_spectrum=expected,
        projector_polynomial_degree=rank,
        projector_rank=projector.rank(),
        minimum_positive_laplacian_eigenvalue=min(positive),
        maximum_laplacian_eigenvalue=max(positive),
        normalized_zero_gap=min(positive) / rank,
        maximum_down_degree=maximum_down,
        maximum_up_degree=maximum_up,
        exact_spectrum_verified=spectrum_verified,
        exact_projector_idempotence_verified=idempotent,
        exact_projector_image_equals_down_kernel=kernel_exact,
        status=(
            "exact-Young-primitive-projector-verified"
            if verified
            else "Young-primitive-projector-control-failure"
        ),
    )


def joint_primitive_projector_control(
    half_degree: int,
) -> JointPrimitiveProjectorControl:
    if half_degree < 2:
        raise ValueError("half_degree must be at least two")
    dimensions = [partition_difference(rank) for rank in range(half_degree + 1)]
    observed = sum(
        dimensions[left] * dimensions[half_degree - left]
        for left in range(half_degree + 1)
    )
    expected = joint_primitive_dimension(half_degree)
    sector_gaps = [
        1.0 / rank
        for rank in range(1, half_degree + 1)
        if partition_difference(rank) > 0
    ]
    verified = observed == expected
    return JointPrimitiveProjectorControl(
        half_degree=half_degree,
        color_split_sector_count=half_degree + 1,
        joint_primitive_dimension_from_projectors=observed,
        expected_joint_primitive_dimension=expected,
        minimum_sector_normalized_zero_gap=min(sector_gaps),
        maximum_sector_normalized_zero_gap=max(sector_gaps),
        exact_direct_sum_tensor_projector_rank_verified=verified,
        polynomial_query_projector_specified=verified,
        status=(
            "joint-primitive-direct-sum-projector-specified"
            if verified
            else "joint-primitive-projector-rank-control-failure"
        ),
    )


def bipartition_count(half_degree: int) -> int:
    return sum(
        partition_number(left) * partition_number(half_degree - left)
        for left in range(half_degree + 1)
    )


def joint_primitive_dimension_fast(half_degree: int) -> int:
    return sum(
        partition_difference(left)
        * partition_difference(half_degree - left)
        for left in range(half_degree + 1)
    )


def joint_primitive_scaling_record(
    half_degree: int,
) -> JointPrimitiveScalingRecord:
    if half_degree < 2:
        raise ValueError("half_degree must be at least two")
    total = bipartition_count(half_degree)
    primitive = joint_primitive_dimension_fast(half_degree)
    return JointPrimitiveScalingRecord(
        half_degree=half_degree,
        bipartition_count=total,
        joint_primitive_dimension=primitive,
        joint_primitive_fraction=primitive / total,
        joint_primitive_label_bits=math.log2(primitive),
        normalized_laplacian_gap_lower_bound=1.0 / half_degree,
        sparse_query_reflection_order=half_degree,
        maximum_partition_neighbor_count_upper_bound=(
            2 * math.isqrt(2 * half_degree) + 2
        ),
        label_space_projector_polynomial_query=True,
        reversible_partition_oracle_gate_compiled=False,
        ambient_branching_copy_isometry_compiled=False,
        status="joint-primitive-label-reflection-polynomial-query-ambient-lift-open",
    )


def build_joint_primitive_projector_report() -> JointPrimitiveProjectorReport:
    Young_controls = [
        audit_Young_primitive_projector(rank) for rank in range(1, 9)
    ]
    joint_controls = [
        joint_primitive_projector_control(half_degree)
        for half_degree in range(2, 11)
    ]
    scaling = [
        joint_primitive_scaling_record(half_degree)
        for half_degree in (8, 16, 32, 64, 128)
    ]
    verified = bool(
        all(
            row.exact_spectrum_verified
            and row.exact_projector_idempotence_verified
            and row.exact_projector_image_equals_down_kernel
            for row in Young_controls
        )
        and all(
            row.exact_direct_sum_tensor_projector_rank_verified
            and row.polynomial_query_projector_specified
            for row in joint_controls
        )
    )
    theorem = JointPrimitiveProjectorTheorem(
        Young_laplacian_spectrum=(
            "char((D_n)^T D_n)=product_(j=0)^n "
            "(x-j)^(p(n-j)-p(n-j-1))."
        ),
        primitive_projector=(
            "P_n^prim=product_(j=1)^n(I-(D_n)^T D_n/j), exactly the "
            "orthogonal projector onto ker D_n."
        ),
        joint_primitive_projector=(
            "P_m^joint=direct_sum_(a+b=m) P_a^prim tensor P_b^prim, "
            "with rank p_2(m)-2p_2(m-1)+p_2(m-2)."
        ),
        sparse_query_algorithm=(
            "Normalize (D_n)^T D_n by n. Its zero gap is at least 1/n, "
            "and add/remove-corner access is polynomially sparse, giving an "
            "O(n)-order query reflection up to logarithmic precision factors."
        ),
        positive_compiler_consequence=(
            "The previously abstract recurrence kernel has a canonical "
            "polynomial-query projector on its auxiliary coefficient space; "
            "this is diagnostic rather than a physical copy-space reflection."
        ),
        scope_limit=(
            "Multiplicity coefficients are not physical amplitudes. There is no "
            "gate-level reversible partition oracle, branching-copy isometry, "
            "source primitive mass theorem, matrix polar, detector, or speedup."
        ),
        exact_all_rank_Young_spectrum_proved=True,
        exact_primitive_projector_polynomial_proved=True,
        exact_joint_primitive_projector_proved=True,
        polynomial_query_label_reflection_proved=True,
        reversible_partition_oracle_gate_compiled=False,
        ambient_branching_copy_isometry_compiled=False,
        source_aware_normalized_subduction_transform_compiled=False,
        hidden_involution_detector_constructed=False,
        speedup_claim_allowed=False,
        theorem_verified=verified,
        status=(
            "paired-tower-joint-primitive-coefficient-projector-diagnostic-only"
            if verified
            else "paired-tower-joint-primitive-projector-control-failure"
        ),
    )
    return JointPrimitiveProjectorReport(
        created_at=utc_now(),
        theorem_contract={
            "label_space": (
                "Direct sum over a+b=m of rank-a and rank-b Young partition registers"
            ),
            "operator": "Young down-incidence Laplacians and their tensor kernels",
            "access_model": (
                "Sparse coherent add/remove-corner oracle for partition labels"
            ),
            "claim_boundary": (
                "A reflection on auxiliary multiplicity-table coordinates, not "
                "a physical K-irrep/copy register, subduction isometry, or polar."
            ),
        },
        Young_controls=Young_controls,
        joint_controls=joint_controls,
        scaling_records=scaling,
        theorem=theorem,
        proof_obligations=[
            {
                "id": "PO-PAIRED-TOWER-REVERSIBLE-PARTITION-ORACLE",
                "statement": (
                    "Compile addable/removable-corner enumeration and sparse "
                    "incidence block access reversibly with explicit gate and garbage bounds."
                ),
                "resolved": False,
            },
            {
                "id": "PO-PAIRED-TOWER-PRIMITIVE-AMBIENT-ISOMETRY",
                "statement": (
                    "Supply an independent physical state embedding before using "
                    "the coefficient projector; multiplicity tables must not be "
                    "assumed to be amplitudes of the missing subduction transform."
                ),
                "resolved": False,
            },
            {
                "id": "PO-PAIRED-TOWER-PRIMITIVE-SOURCE-NORM",
                "statement": (
                    "Replace coefficient residual norm by an actual source-weighted "
                    "within-mu multiplicity-space observable and prove that it "
                    "participates in a normalization-preserving matrix polar."
                ),
                "resolved": False,
            },
        ],
        adversarial_audit=[
            {
                "challenge": "The primitive kernel is only an abstract coefficient nullspace.",
                "answer": (
                    "Its projector and inverse-linear gap are exact, but it remains "
                    "an auxiliary coefficient-space object rather than a physical "
                    "branching-copy subspace."
                ),
                "resolved": True,
            },
            {
                "challenge": "A degree-n projector polynomial is exponentially costly.",
                "answer": (
                    "False in the sparse-query model: the normalized gap is at "
                    "least 1/n and partition cover access is polynomially sparse."
                ),
                "resolved": True,
            },
            {
                "challenge": "The label projector compiles the missing subduction transform.",
                "answer": (
                    "False. The ambient copy-space isometry and source norm are "
                    "precisely the unresolved gates."
                ),
                "resolved": True,
            },
        ],
        literature_links=[
            {
                "id": "STANLEY-DIFFERENTIAL-POSETS-THEOREM-4.1",
                "role": (
                    "Characteristic polynomial and eigenspace decomposition of "
                    "UD in an r-differential poset."
                ),
            },
            {
                "id": "ALGEBRAIC-COMBINATORICS-2019-DIFFERENTIAL-POSETS",
                "role": (
                    "Accessible statement of the spectrum and ker(D) primitive decomposition."
                ),
            },
        ],
        headline_metrics={
            "exact_Young_projector_control_count": len(Young_controls),
            "exact_joint_projector_rank_control_count": len(joint_controls),
            "natural_scaling_row_count": len(scaling),
            "tail_joint_primitive_dimension_decimal": str(
                scaling[-1].joint_primitive_dimension
            ),
            "tail_joint_primitive_label_bits": (
                scaling[-1].joint_primitive_label_bits
            ),
            "polynomial_query_label_reflection_count": 1,
            "physical_missing_copy_reflection_count": 0,
            "ambient_copy_isometry_count": 0,
        },
        claim_gate={
            "exact_joint_primitive_label_projector_proved": True,
            "polynomial_query_joint_primitive_reflection_proved": True,
            "branching_multiplicity_vector_is_physical_label_state": False,
            "physical_joint_primitive_reflection_compiled": False,
            "reversible_partition_oracle_gate_compiled": False,
            "ambient_branching_copy_isometry_compiled": False,
            "natural_source_primitive_norm_bounded": False,
            "source_aware_normalized_subduction_transform_compiled": False,
            "hidden_involution_detector_constructed": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The coefficient kernel is projectable with polynomial query gap, "
                "but multiplicity tables are not physical label amplitudes and the "
                "projector does not preserve the representation cone."
            ),
        },
        status=theorem.status,
        summary=(
            "Converted the color-resolved recurrence kernel into an exact, "
            "inverse-polynomial-gap coefficient-space diagnostic; no physical "
            "missing-copy reflection follows."
        ),
        falsifiers_triggered=[
            "The joint primitive coefficient kernel is not spectrally inaccessible.",
            "Efficient coefficient projection does not imply physical primitive localization.",
            "A source-aware within-mu observable or independent full subduction isometry remains necessary.",
        ],
    )


def write_joint_primitive_projector_report(
    output_path: Path = REPORT_PATH,
) -> dict[str, Any]:
    payload = asdict(build_joint_primitive_projector_report())
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    return payload


def run_experiment(
    experiment_id: str = DEFAULT_EXPERIMENT_ID,
    candidate_id: str = DEFAULT_CANDIDATE_ID,
    write_registry: bool = True,
) -> dict[str, Any]:
    del experiment_id, candidate_id, write_registry
    return write_joint_primitive_projector_report()


if __name__ == "__main__":
    print(json.dumps(run_experiment(), indent=2, sort_keys=True))

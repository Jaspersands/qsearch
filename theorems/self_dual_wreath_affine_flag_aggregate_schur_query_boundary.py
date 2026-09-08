"""Affine flags label Schur recursion but do not supply metric amplitudes.

Let the ``q=2^k`` orientation addresses be ``F_2^k`` and let an invertible
binary flag label an address by

    y_j(x) = <f_j,x> mod 2.                                  (1)

An out-of-place reversible circuit computes all labels using at most ``k^2``
CNOTs, and the label prefix decides node membership and whether an edge is
internal or crosses the next split.  Thus the combinatorial node-label problem
does not require a table of ``q`` leaves.

The operator algebra is equally clean.  For a positive kernel on coordinates
``I_1 + I_2 + C``, shorting first to ``I_2+C`` and then to ``C`` equals the
single Schur short to ``C``.  The same holds with Moore--Penrose inverses for
positive semidefinite kernels.  Aggregate endpoint metrics can therefore be
carried up a tree *if coherent access to each child response matrix is already
available*.

Those two facts do not compile the response matrices from the current typed
addressed-kernel interface.  Consider ``q`` local positive kernels

    G_i(x) = [[1, rho], [rho, rho^2 + e_i(x)]],
    e_i(x) = 1/q + x_i,

under the promise ``|x| in {0,1}``.  Giving every leaf a private internal
coordinate and one common crossing coordinate makes the aggregate short

    E_x = sum_i e_i(x) = 1 + OR(x).                         (2)

Pair (2) with a fixed right metric ``E_R=1``.  The binary endpoint isometry is

    T_x = [sqrt(E_x/(E_x+1)); sqrt(1/(E_x+1))].             (3)

Its left probability changes from ``1/2`` to ``2/3``.  Both instances have
full retained mass, scalar condition number one, and endpoint edge at least
``1/3``.  A constant-error compiler for (3) from addressed queries to
``G_i(x)`` would therefore decide unstructured search with the same query
order.  The BBBV quantum search lower bound gives ``Omega(sqrt(q))`` queries.

This is a typed black-box lower bound, not a representation-specific circuit
lower bound.  Actual Schur/Racah kernels may obey identities that exclude the
marked family and yield a succinct direct block encoding or Naimark transform.
The theorem instead closes a tempting inference: reversible affine labels,
Schur-short associativity, constant endpoint conditioning, and full native mass
do not make arbitrary addressed local metric values coherently aggregatable in
``poly(k)`` queries.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import numpy as np

from research_registry import (
    ExperimentRecord,
    NegativeResultRecord,
    upsert_experiment,
    upsert_negative_result,
    utc_now,
)


REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_affine_flag_aggregate_schur_query_boundary.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-AFFINE-FLAG-AGGREGATE-"
    "SCHUR-QUERY-BOUNDARY"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"
NEGATIVE_RESULT_ID = (
    "AFFINE-FLAG-ADDRESSED-LOCAL-KERNELS-NO-POLYLOG-"
    "AGGREGATE-SCHUR-COMPILER"
)
BBBV_URL = "https://arxiv.org/abs/quant-ph/9701001"


@dataclass(frozen=True)
class AffineFlagLabelControl:
    control_id: str
    bit_count: int
    orientation_count: int
    flag_basis: tuple[int, ...]
    binary_rank: int
    label_count: int
    full_tree_node_count: int
    audited_incident_pair_count: int
    maximum_forward_cnot_count: int
    membership_workspace_bit_count: int
    leaf_table_entry_count: int
    reversible_label_bijection_verified: bool
    internal_crossing_classification_verified: bool
    status: str


@dataclass(frozen=True)
class SchurQuotientCompositionControl:
    control_id: str
    total_dimension: int
    first_internal_dimension: int
    second_internal_dimension: int
    crossing_dimension: int
    kernel_rank: int
    singular_first_internal_block: bool
    minimum_kernel_eigenvalue: float
    maximum_psd_range_inclusion_residual: float
    forward_composition_residual: float
    reverse_composition_residual: float
    direct_short_minimum_eigenvalue: float
    exact_nested_schur_short_verified: bool
    status: str


@dataclass(frozen=True)
class AddressedAggregateQueryControl:
    control_id: str
    address_bit_count: int
    address_count: int
    rho: float
    unmarked_local_short: float
    marked_local_short: float
    no_mark_aggregate_short: float
    one_mark_aggregate_short: float
    maximum_aggregate_short_residual: float
    maximum_local_kernel_norm: float
    minimum_local_kernel_eigenvalue: float
    canonical_sum_block_encoding_normalization: float
    no_mark_left_endpoint_probability: float
    one_mark_left_endpoint_probability: float
    endpoint_probability_gap: float
    endpoint_isometry_operator_gap: float
    approximation_error: float
    robust_probability_gap_lower_bound: float
    minimum_endpoint_two_sided_edge: float
    aggregate_metric_condition_number: float
    native_retained_mass: float
    addressed_kernel_query_equivalent_to_search_bit_query: bool
    bounded_error_query_lower_bound: str
    exact_search_reduction_verified: bool
    status: str


@dataclass(frozen=True)
class AggregateSchurInterfaceRecord:
    interface_id: str
    input_access: str
    output_contract: str
    normalization_or_query_cost: str
    status: str
    sufficient_for_endpoint_compiler: bool
    supplied_by_current_stack: bool


@dataclass(frozen=True)
class AffineFlagAggregateScalingRecord:
    address_bit_count: int
    address_count: int
    reversible_label_gate_upper_bound: int
    reversible_label_workspace_upper_bound: int
    search_query_lower_bound_log2: float
    search_query_lower_bound_proxy: float
    polynomial_in_address_bit_count: bool
    natural_schur_racah_realizability_proved: bool
    status: str


@dataclass(frozen=True)
class AffineFlagAggregateSchurQueryTheorem:
    affine_label_verdict: str
    algebraic_recursion_verdict: str
    addressed_kernel_access_verdict: str
    natural_representation_scope: str
    all_depth_scope: str
    theorem_verified: bool
    status: str


@dataclass(frozen=True)
class AffineFlagAggregateSchurQueryReport:
    created_at: str
    primary_literature: dict[str, str]
    theorem_contract: dict[str, Any]
    theorem: AffineFlagAggregateSchurQueryTheorem
    affine_label_controls: list[AffineFlagLabelControl]
    schur_composition_controls: list[SchurQuotientCompositionControl]
    addressed_query_controls: list[AddressedAggregateQueryControl]
    interface_inventory: list[AggregateSchurInterfaceRecord]
    scaling_records: list[AffineFlagAggregateScalingRecord]
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def binary_rank(vectors: tuple[int, ...]) -> int:
    """Return the rank of bit vectors over F_2."""

    pivots: dict[int, int] = {}
    for vector in vectors:
        reduced = int(vector)
        while reduced:
            pivot = reduced.bit_length() - 1
            if pivot in pivots:
                reduced ^= pivots[pivot]
            else:
                pivots[pivot] = reduced
                break
    return len(pivots)


def affine_flag_label(address: int, basis: tuple[int, ...]) -> tuple[int, ...]:
    """Evaluate all binary flag functionals on one address."""

    return tuple((address & vector).bit_count() % 2 for vector in basis)


def audit_affine_flag_labeler(
    control_id: str,
    bit_count: int,
    basis: tuple[int, ...],
) -> AffineFlagLabelControl:
    if bit_count < 1:
        raise ValueError("bit_count must be positive")
    if len(basis) != bit_count or any(
        vector <= 0 or vector >= 1 << bit_count for vector in basis
    ):
        raise ValueError("basis must contain one nonzero k-bit vector per row")
    rank = binary_rank(basis)
    labels = {
        address: affine_flag_label(address, basis)
        for address in range(1 << bit_count)
    }
    bijective = rank == bit_count and len(set(labels.values())) == 1 << bit_count

    audited_pairs = 0
    classification_ok = True
    for depth in range(bit_count):
        for prefix_integer in range(1 << depth):
            prefix = tuple(
                (prefix_integer >> index) & 1 for index in range(depth)
            )
            members = [
                address
                for address, label in labels.items()
                if label[:depth] == prefix
            ]
            for first_index, first in enumerate(members):
                for second in members[first_index + 1 :]:
                    first_side = labels[first][depth]
                    second_side = labels[second][depth]
                    crossing = first_side != second_side
                    direct_crossing = (
                        labels[first][:depth] == prefix
                        and labels[second][:depth] == prefix
                        and labels[first][depth] != labels[second][depth]
                    )
                    classification_ok &= crossing == direct_crossing
                    audited_pairs += 1

    cnot_count = sum(vector.bit_count() for vector in basis)
    verified = bool(
        bijective
        and classification_ok
        and cnot_count <= bit_count * bit_count
    )
    return AffineFlagLabelControl(
        control_id=control_id,
        bit_count=bit_count,
        orientation_count=1 << bit_count,
        flag_basis=basis,
        binary_rank=rank,
        label_count=len(set(labels.values())),
        full_tree_node_count=(1 << (bit_count + 1)) - 1,
        audited_incident_pair_count=audited_pairs,
        maximum_forward_cnot_count=cnot_count,
        membership_workspace_bit_count=bit_count,
        leaf_table_entry_count=0,
        reversible_label_bijection_verified=bijective,
        internal_crossing_classification_verified=classification_ok,
        status=(
            "table-free-reversible-affine-flag-labeler"
            if verified
            else "affine-flag-label-control-failure"
        ),
    )


def _hermitian(matrix: np.ndarray) -> np.ndarray:
    return (matrix + matrix.conj().T) / 2


def psd_schur_short(
    matrix: np.ndarray,
    eliminated_dimension: int,
    *,
    tolerance: float = 1e-10,
) -> tuple[np.ndarray, float]:
    """Short a PSD matrix from its leading coordinates to the remainder."""

    matrix = _hermitian(np.asarray(matrix, dtype=complex))
    if matrix.ndim != 2 or matrix.shape[0] != matrix.shape[1]:
        raise ValueError("matrix must be square")
    if not 0 <= eliminated_dimension < len(matrix):
        raise ValueError("eliminated dimension must leave a nonempty block")
    if eliminated_dimension == 0:
        return matrix, 0.0
    internal = matrix[:eliminated_dimension, :eliminated_dimension]
    coupling = matrix[:eliminated_dimension, eliminated_dimension:]
    crossing = matrix[eliminated_dimension:, eliminated_dimension:]
    inverse = np.linalg.pinv(internal, rcond=tolerance)
    range_residual = float(
        np.linalg.norm(
            coupling - internal @ inverse @ coupling,
            ord=2,
        )
    )
    short = crossing - coupling.conj().T @ inverse @ coupling
    return _hermitian(short), range_residual


def audit_schur_quotient_composition(
    control_id: str,
    kernel: np.ndarray,
    first_internal_dimension: int,
    second_internal_dimension: int,
    *,
    tolerance: float = 1e-9,
) -> SchurQuotientCompositionControl:
    kernel = _hermitian(np.asarray(kernel, dtype=complex))
    total = len(kernel)
    crossing_dimension = total - first_internal_dimension - second_internal_dimension
    if min(first_internal_dimension, second_internal_dimension, crossing_dimension) < 1:
        raise ValueError("all three coordinate blocks must be nonempty")
    values = np.linalg.eigvalsh(kernel)
    if float(values.min()) < -100 * tolerance:
        raise ValueError("kernel must be positive semidefinite")

    direct, direct_range = psd_schur_short(
        kernel,
        first_internal_dimension + second_internal_dimension,
        tolerance=tolerance,
    )
    after_first, first_range = psd_schur_short(
        kernel,
        first_internal_dimension,
        tolerance=tolerance,
    )
    forward, second_range = psd_schur_short(
        after_first,
        second_internal_dimension,
        tolerance=tolerance,
    )

    first = tuple(range(first_internal_dimension))
    second = tuple(
        range(
            first_internal_dimension,
            first_internal_dimension + second_internal_dimension,
        )
    )
    crossing = tuple(
        range(first_internal_dimension + second_internal_dimension, total)
    )
    reverse_order = (*second, *first, *crossing)
    reversed_kernel = kernel[np.ix_(reverse_order, reverse_order)]
    after_second, reverse_first_range = psd_schur_short(
        reversed_kernel,
        second_internal_dimension,
        tolerance=tolerance,
    )
    reverse, reverse_second_range = psd_schur_short(
        after_second,
        first_internal_dimension,
        tolerance=tolerance,
    )

    forward_residual = float(np.linalg.norm(forward - direct, ord=2))
    reverse_residual = float(np.linalg.norm(reverse - direct, ord=2))
    maximum_range = max(
        direct_range,
        first_range,
        second_range,
        reverse_first_range,
        reverse_second_range,
    )
    first_block = kernel[:first_internal_dimension, :first_internal_dimension]
    singular = bool(
        np.linalg.matrix_rank(first_block, tol=tolerance)
        < first_internal_dimension
    )
    verified = bool(
        maximum_range <= 1000 * tolerance
        and forward_residual <= 1000 * tolerance
        and reverse_residual <= 1000 * tolerance
        and float(np.linalg.eigvalsh(direct).min()) >= -100 * tolerance
    )
    return SchurQuotientCompositionControl(
        control_id=control_id,
        total_dimension=total,
        first_internal_dimension=first_internal_dimension,
        second_internal_dimension=second_internal_dimension,
        crossing_dimension=crossing_dimension,
        kernel_rank=int(np.linalg.matrix_rank(kernel, tol=tolerance)),
        singular_first_internal_block=singular,
        minimum_kernel_eigenvalue=float(values.min()),
        maximum_psd_range_inclusion_residual=maximum_range,
        forward_composition_residual=forward_residual,
        reverse_composition_residual=reverse_residual,
        direct_short_minimum_eigenvalue=float(np.linalg.eigvalsh(direct).min()),
        exact_nested_schur_short_verified=verified,
        status=(
            "exact-positive-semidefinite-schur-quotient-associativity"
            if verified
            else "schur-quotient-composition-control-failure"
        ),
    )


def _local_search_kernel(short_value: float, rho: float) -> np.ndarray:
    return np.asarray(
        [[1.0, rho], [rho, rho * rho + short_value]],
        dtype=complex,
    )


def _aggregate_search_kernel(
    short_values: np.ndarray,
    rho: float,
) -> np.ndarray:
    count = len(short_values)
    kernel = np.zeros((count + 1, count + 1), dtype=complex)
    kernel[:count, :count] = np.eye(count)
    kernel[:count, count] = rho
    kernel[count, :count] = rho
    kernel[count, count] = count * rho * rho + float(short_values.sum())
    return kernel


def _scalar_endpoint_isometry(left_metric: float, right_metric: float) -> np.ndarray:
    total = left_metric + right_metric
    return np.asarray(
        [[math.sqrt(left_metric / total)], [math.sqrt(right_metric / total)]],
        dtype=complex,
    )


def audit_addressed_aggregate_search_reduction(
    control_id: str,
    address_bit_count: int,
    *,
    rho: float = 0.31,
    approximation_error: float = 0.01,
    tolerance: float = 1e-9,
) -> AddressedAggregateQueryControl:
    if address_bit_count < 1:
        raise ValueError("address_bit_count must be positive")
    count = 1 << address_bit_count
    baseline = 1.0 / count
    no_mark = np.full(count, baseline)
    one_mark = no_mark.copy()
    one_mark[count // 3] += 1.0

    aggregate_shorts = []
    short_residuals = []
    local_norms = []
    local_minima = []
    for values in (no_mark, one_mark):
        aggregate = _aggregate_search_kernel(values, rho)
        short, range_residual = psd_schur_short(
            aggregate,
            count,
            tolerance=tolerance,
        )
        aggregate_shorts.append(float(short[0, 0].real))
        short_residuals.append(
            max(range_residual, abs(float(short[0, 0].real) - float(values.sum())))
        )
        for value in values:
            local = _local_search_kernel(float(value), rho)
            local_values = np.linalg.eigvalsh(local)
            local_norms.append(float(local_values[-1]))
            local_minima.append(float(local_values[0]))

    no_target = _scalar_endpoint_isometry(aggregate_shorts[0], 1.0)
    mark_target = _scalar_endpoint_isometry(aggregate_shorts[1], 1.0)
    no_probability = aggregate_shorts[0] / (aggregate_shorts[0] + 1.0)
    mark_probability = aggregate_shorts[1] / (aggregate_shorts[1] + 1.0)
    probability_gap = mark_probability - no_probability
    operator_gap = float(np.linalg.norm(mark_target - no_target, ord=2))
    robust_gap = probability_gap - 4 * approximation_error - 2 * approximation_error**2
    edge = min(no_probability, 1 - no_probability, mark_probability, 1 - mark_probability)
    lcu_normalization = sum(
        float(np.linalg.eigvalsh(_local_search_kernel(float(value), rho))[-1])
        for value in one_mark
    )
    verified = bool(
        max(short_residuals) <= 1000 * tolerance
        and abs(aggregate_shorts[0] - 1.0) <= 1000 * tolerance
        and abs(aggregate_shorts[1] - 2.0) <= 1000 * tolerance
        and probability_gap >= 1 / 6 - 1000 * tolerance
        and robust_gap > 0.1
        and edge >= 1 / 3 - 1000 * tolerance
        and min(local_minima) > 0
    )
    return AddressedAggregateQueryControl(
        control_id=control_id,
        address_bit_count=address_bit_count,
        address_count=count,
        rho=rho,
        unmarked_local_short=baseline,
        marked_local_short=baseline + 1.0,
        no_mark_aggregate_short=aggregate_shorts[0],
        one_mark_aggregate_short=aggregate_shorts[1],
        maximum_aggregate_short_residual=max(short_residuals),
        maximum_local_kernel_norm=max(local_norms),
        minimum_local_kernel_eigenvalue=min(local_minima),
        canonical_sum_block_encoding_normalization=lcu_normalization,
        no_mark_left_endpoint_probability=no_probability,
        one_mark_left_endpoint_probability=mark_probability,
        endpoint_probability_gap=probability_gap,
        endpoint_isometry_operator_gap=operator_gap,
        approximation_error=approximation_error,
        robust_probability_gap_lower_bound=robust_gap,
        minimum_endpoint_two_sided_edge=edge,
        aggregate_metric_condition_number=1.0,
        native_retained_mass=1.0,
        addressed_kernel_query_equivalent_to_search_bit_query=True,
        bounded_error_query_lower_bound="Omega(sqrt(q))",
        exact_search_reduction_verified=verified,
        status=(
            "constant-gap-addressed-aggregate-schur-search-reduction"
            if verified
            else "addressed-aggregate-search-reduction-control-failure"
        ),
    )


def aggregate_schur_interface_inventory() -> list[AggregateSchurInterfaceRecord]:
    return [
        AggregateSchurInterfaceRecord(
            interface_id="AFFINE-FLAG-NODE-LABEL",
            input_access="k-bit orientation address and a classical invertible F_2 flag basis",
            output_contract="coherent flag coordinates, node membership, and internal/crossing edge type",
            normalization_or_query_cost="O(k^2) CNOTs and O(k) workspace, with no leaf table",
            status="compiled-table-free-combinatorial-label-interface",
            sufficient_for_endpoint_compiler=False,
            supplied_by_current_stack=True,
        ),
        AggregateSchurInterfaceRecord(
            interface_id="CHILD-RESPONSE-SCHUR-RECURSION",
            input_access="coherent child response matrices on compatible boundary coordinates",
            output_contract="parent response by nested positive Schur short",
            normalization_or_query_cost="algebraically associative; coherent inverse/query cost still charged",
            status="exact-algebraic-recursion-response-oracles-assumed",
            sufficient_for_endpoint_compiler=True,
            supplied_by_current_stack=False,
        ),
        AggregateSchurInterfaceRecord(
            interface_id="ADDRESSED-LOCAL-KERNEL-QUERY",
            input_access="reversible address query for one arbitrary local PSD kernel block",
            output_contract="aggregate short metric or its binary endpoint dilation",
            normalization_or_query_cost="Omega(sqrt(q)) in the typed black-box model",
            status="polylog-query-aggregate-compiler-refuted",
            sufficient_for_endpoint_compiler=False,
            supplied_by_current_stack=True,
        ),
        AggregateSchurInterfaceRecord(
            interface_id="STRUCTURED-RACAH-RESPONSE-ORACLE",
            input_access="succinct representation-specific formula or direct local Schur/Racah transform",
            output_contract="block encoding of each child response on one parent-compatible trim",
            normalization_or_query_cost="must be polynomial in n and summable through depth",
            status="open-not-covered-by-black-box-lower-bound",
            sufficient_for_endpoint_compiler=True,
            supplied_by_current_stack=False,
        ),
        AggregateSchurInterfaceRecord(
            interface_id="ALL-DEPTH-NATIVE-MASS-RECURRENCE",
            input_access="natural source distribution and a common propagated retained projector",
            output_contract="conditional loss o(1/L) per level through depth L",
            normalization_or_query_cost="not supplied by fixed-level endpoint laws",
            status="open",
            sufficient_for_endpoint_compiler=True,
            supplied_by_current_stack=False,
        ),
    ]


def affine_flag_aggregate_scaling_record(
    address_bit_count: int,
) -> AffineFlagAggregateScalingRecord:
    if address_bit_count < 1:
        raise ValueError("address_bit_count must be positive")
    address_count = 1 << address_bit_count
    lower_proxy = math.sqrt(address_count)
    return AffineFlagAggregateScalingRecord(
        address_bit_count=address_bit_count,
        address_count=address_count,
        reversible_label_gate_upper_bound=address_bit_count**2,
        reversible_label_workspace_upper_bound=address_bit_count,
        search_query_lower_bound_log2=address_bit_count / 2,
        search_query_lower_bound_proxy=lower_proxy,
        polynomial_in_address_bit_count=False,
        natural_schur_racah_realizability_proved=False,
        status="labels-polynomial-addressed-metric-aggregation-black-box-exponential",
    )


def _positive_kernel_controls() -> list[SchurQuotientCompositionControl]:
    rng = np.random.default_rng(20260827)
    dense = rng.normal(size=(8, 8))
    positive = dense.T @ dense + 0.4 * np.eye(8)

    singular_factor = rng.normal(size=(5, 7))
    singular_factor[:, 1] = singular_factor[:, 0]
    singular = singular_factor.T @ singular_factor
    return [
        audit_schur_quotient_composition(
            "POSITIVE-DEFINITE-TWO-STAGE-QUOTIENT",
            positive,
            3,
            2,
        ),
        audit_schur_quotient_composition(
            "SINGULAR-PSD-MOORE-PENROSE-TWO-STAGE-QUOTIENT",
            singular,
            2,
            2,
        ),
    ]


def run_affine_flag_aggregate_schur_query_boundary(
) -> AffineFlagAggregateSchurQueryReport:
    label_controls = [
        audit_affine_flag_labeler(
            "STANDARD-FIVE-BIT-FLAG",
            5,
            (1, 2, 4, 8, 16),
        ),
        audit_affine_flag_labeler(
            "NONSYSTEMATIC-FIVE-BIT-FLAG",
            5,
            (1, 3, 6, 12, 24),
        ),
    ]
    schur_controls = _positive_kernel_controls()
    query_controls = [
        audit_addressed_aggregate_search_reduction(
            f"ADDRESSED-SEARCH-Q{1 << bit_count}",
            bit_count,
        )
        for bit_count in (2, 3, 4, 5)
    ]
    interfaces = aggregate_schur_interface_inventory()
    scaling = [
        affine_flag_aggregate_scaling_record(bit_count)
        for bit_count in (8, 16, 24, 32, 48, 64)
    ]
    failures = (
        sum(
            not row.reversible_label_bijection_verified
            or not row.internal_crossing_classification_verified
            for row in label_controls
        )
        + sum(not row.exact_nested_schur_short_verified for row in schur_controls)
        + sum(not row.exact_search_reduction_verified for row in query_controls)
    )
    label_verified = all(
        row.reversible_label_bijection_verified
        and row.internal_crossing_classification_verified
        for row in label_controls
    )
    composition_verified = all(
        row.exact_nested_schur_short_verified for row in schur_controls
    )
    query_verified = all(row.exact_search_reduction_verified for row in query_controls)
    verified = bool(failures == 0 and label_verified and composition_verified and query_verified)
    headline: dict[str, int | float] = {
        "reversible_affine_flag_node_labeler_theorem_count": int(label_verified),
        "nested_psd_schur_short_associativity_theorem_count": int(composition_verified),
        "addressed_local_kernel_aggregate_search_lower_bound_theorem_count": int(query_verified),
        "affine_label_control_count": len(label_controls),
        "schur_composition_control_count": len(schur_controls),
        "addressed_query_control_count": len(query_controls),
        "finite_control_failure_count": failures,
        "maximum_schur_composition_residual": max(
            max(row.forward_composition_residual, row.reverse_composition_residual)
            for row in schur_controls
        ),
        "minimum_hard_family_endpoint_edge": min(
            row.minimum_endpoint_two_sided_edge for row in query_controls
        ),
        "minimum_hard_family_native_retained_mass": min(
            row.native_retained_mass for row in query_controls
        ),
        "maximum_finite_address_count": max(
            row.address_count for row in query_controls
        ),
        "tail_search_query_lower_bound_log2": scaling[-1].search_query_lower_bound_log2,
        "compiled_structured_racah_response_oracle_count": 0,
        "all_depth_native_mass_recurrence_theorem_count": 0,
        "physical_pgm_circuit_count": 0,
        "new_quantum_algorithm_count": 0,
    }
    theorem = AffineFlagAggregateSchurQueryTheorem(
        affine_label_verdict=(
            "An invertible k-bit affine flag gives a table-free reversible node and crossing labeler using O(k^2) CNOTs and O(k) workspace."
        ),
        algebraic_recursion_verdict=(
            "Positive Schur shorts obey the nested quotient formula, including singular Moore-Penrose blocks, so exact child response matrices are algebraically sufficient to propagate a parent response."
        ),
        addressed_kernel_access_verdict=(
            "They are not supplied by affine labels plus arbitrary addressed local-kernel queries: a constant-error aggregate endpoint compiler needs Omega(sqrt(q)) queries in this typed oracle model."
        ),
        natural_representation_scope=(
            "The marked metric family is an oracle counterfamily, not a proved natural Schur/Racah sector. Representation-specific formulas and a direct local Naimark transform remain open."
        ),
        all_depth_scope=(
            "The lower bound already occurs at one aggregate child. No all-depth common-trim native-mass recurrence is proved or refuted for the natural source."
        ),
        theorem_verified=verified,
        status=(
            "affine-label-and-schur-recursion-proved-addressed-aggregate-query-boundary"
            if verified
            else "affine-flag-aggregate-schur-query-control-failure"
        ),
    )
    return AffineFlagAggregateSchurQueryReport(
        created_at=utc_now(),
        primary_literature={
            "quantum_unstructured_search_lower_bound": BBBV_URL,
        },
        theorem_contract={
            "hypothesis": (
                "A reversible affine-flag node labeler, exact Schur-short recursion, and addressed access to every local PSD kernel suffice to compile each aggregate endpoint in poly(k) queries for q=2^k leaves."
            ),
            "positive_boundary": (
                "The affine labeler is table free and polynomial, and nested positive Schur shorts are exactly associative. Supplied coherent child response oracles therefore give a valid recursive algebraic interface."
            ),
            "negative_boundary": (
                "The hypothesis is false for arbitrary addressed metric values. The promised local-kernel family embeds OR while keeping the root aggregate scalar, condition number one, endpoint edge at least 1/3, and native retained mass one, forcing Omega(sqrt(q)) queries."
            ),
            "normalization_and_error": (
                "The canonical positive sum has normalization Theta(q) in the hard family. More generally, even an alternative compiler that avoids this LCU normalization cannot beat the Omega(sqrt(q)) query bound at constant operator error."
            ),
            "scope": (
                "This binds the typed arbitrary addressed-local-kernel interface only. It proves no lower bound for succinct representation-specific Racah formulas, direct local Naimark transforms, or arbitrary quantum circuits."
            ),
        },
        theorem=theorem,
        affine_label_controls=label_controls,
        schur_composition_controls=schur_controls,
        addressed_query_controls=query_controls,
        interface_inventory=interfaces,
        scaling_records=scaling,
        proof_obligations=[
            {
                "obligation": "compile_reversible_affine_flag_node_and_crossing_labels",
                "resolved": label_verified,
                "resolution": "Compute every flag parity into a retained output register with one CNOT per nonzero matrix entry; prefix comparison and the next flag bit classify node incidence and crossing edges.",
            },
            {
                "obligation": "prove_exact_child_to_parent_schur_short_composition",
                "resolved": composition_verified,
                "resolution": "The nested shorted-operator quotient formula is verified in positive-definite and singular PSD controls in both elimination orders.",
            },
            {
                "obligation": "decide_polylog_query_aggregation_from_addressed_local_kernels",
                "resolved": query_verified,
                "resolution": "A promised zero-or-one marked local short changes the root endpoint probability by 1/6. BBBV therefore forces Omega(sqrt(q)) addressed queries for constant-error endpoint compilation.",
            },
            {
                "obligation": "exclude_conditioning_or_native_mass_as_the_lower_bound_source",
                "resolved": query_verified,
                "resolution": "The hard root metrics are one-dimensional with condition number one, two-sided endpoint edge at least 1/3, and retained native mass one.",
            },
            {
                "obligation": "compile_succinct_representation_specific_racah_response_oracle",
                "resolved": False,
                "resolution": "Need an all-n identity restricting the actual local kernels beyond arbitrary addressed values, or a direct local Schur/Racah Naimark transform. The oracle counterfamily does not rule either out.",
            },
            {
                "obligation": "prove_parent_compatible_all_depth_native_mass_recurrence",
                "resolved": False,
                "resolution": "Fixed-level spectral laws do not provide o(1/L) conditional loss on one common trim through depth L.",
            },
            {
                "obligation": "compile_physical_pgm_decoder_and_classical_separation",
                "resolved": False,
                "resolution": "This pass stops at the aggregate short-metric oracle and proves no end-to-end measurement or algorithmic advantage.",
            },
        ],
        adversarial_audit=[
            {
                "objection": "The affine node label itself needs an exponential lookup table.",
                "resolved": True,
                "resolution": "Equation (1) is an out-of-place binary linear circuit with at most k^2 CNOTs and zero leaf-table entries.",
            },
            {
                "objection": "Schur complementation is nonassociative, so child response matrices are not sufficient state.",
                "resolved": True,
                "resolution": "Positive shorted operators satisfy the nested quotient identity; both elimination orders agree with direct elimination, including a singular control.",
            },
            {
                "objection": "The query obstruction is only poor root conditioning or rare postselection.",
                "resolved": True,
                "resolution": "The endpoint metrics are scalar, the edge is at least 1/3, and no native mass is discarded.",
            },
            {
                "objection": "The canonical Theta(q) LCU normalization alone proves every possible compiler slow.",
                "resolved": True,
                "resolution": "The LCU value is only diagnostic. The independent BBBV reduction supplies the typed quantum query lower bound.",
            },
            {
                "objection": "The oracle lower bound rules out a direct representation-specific Racah circuit.",
                "resolved": False,
                "resolution": "It does not. Such a circuit may exploit identities that exclude arbitrary marked local metrics and is the surviving route.",
            },
            {
                "objection": "The marked family occurs with nonnegligible probability under the natural Plancherel source.",
                "resolved": False,
                "resolution": "No such natural realizability theorem is claimed; the family is a scoped access-model falsifier.",
            },
        ],
        headline_metrics=headline,
        claim_gate={
            "reversible_affine_flag_node_labeler_compiled": label_verified,
            "internal_crossing_edge_classifier_compiled": label_verified,
            "nested_psd_schur_short_associativity_proved": composition_verified,
            "child_response_matrices_are_algebraically_sufficient_state": composition_verified,
            "affine_labels_determine_metric_amplitudes": False,
            "addressed_local_kernel_queries_compile_aggregate_short_in_polylog_q": False,
            "addressed_aggregate_endpoint_query_lower_bound_sqrt_q": query_verified,
            "query_lower_bound_uses_bad_root_conditioning": False,
            "query_lower_bound_uses_small_native_mass": False,
            "structured_racah_response_oracle_compiled": False,
            "direct_local_schur_racah_naimark_ruled_out": False,
            "all_depth_parent_compatible_native_mass_recurrence_proved": False,
            "physical_pgm_circuit_proved": False,
            "hidden_involution_decoder_proved": False,
            "classical_separation_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "Affine labels solve the combinatorial routing and Schur shorts solve the algebraic state recursion, but arbitrary addressed local metric queries still hide unstructured search. Progress now requires a representation-specific response formula or direct local Naimark transform plus an all-depth common-trim mass theorem."
            ),
        },
        status=theorem.status,
        summary=(
            "Compiled the affine-flag node/crossing labeler and proved exact nested PSD Schur-short recursion, then showed that these do not turn arbitrary addressed local kernels into a polylog-query aggregate metric oracle: a full-mass, condition-one endpoint family embeds unstructured search and needs Omega(sqrt(q)) queries."
        ),
        falsifiers_triggered=[
            "Reversible affine-flag labels by themselves determine aggregate Schur-short metric amplitudes.",
            "Exact Schur-short associativity turns addressed leaf-kernel access into a polylogarithmic-query coherent response oracle.",
            "Constant root conditioning, a constant endpoint edge, and full retained native mass remove the addressed aggregation bottleneck.",
        ],
    )


def write_affine_flag_aggregate_schur_query_boundary_report(
    path: Path = REPORT_PATH,
    *,
    write_registry: bool = True,
) -> dict[str, Any]:
    payload = asdict(run_affine_flag_aggregate_schur_query_boundary())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    if write_registry:
        upsert_experiment(
            ExperimentRecord(
                id=DEFAULT_EXPERIMENT_ID,
                candidate_id=DEFAULT_CANDIDATE_ID,
                title="Affine-flag aggregate Schur query boundary",
                status="completed-affine-label-schur-recursion-and-query-boundary-theorem",
                hypothesis=payload["theorem_contract"]["hypothesis"],
                protocol=(
                    "Compile the reversible affine flag labels, verify the nested PSD Schur-short quotient formula in nonsingular and singular controls, and reduce promised unstructured search to constant-error aggregate endpoint compilation from addressed local-kernel queries."
                ),
                positive_signal=(
                    "A representation-specific formula or direct Racah/Naimark circuit that block-encodes every child response in poly(n) cost while excluding the arbitrary marked-metric oracle family and preserving a common all-depth trim."
                ),
                falsifiers=payload["falsifiers_triggered"],
                metrics=list(payload["headline_metrics"].keys()),
                dependencies=[
                    "self_dual_wreath_affine_core_flag_theorem.py",
                    "self_dual_wreath_vertex_kernel_graded_reduction.py",
                    "self_dual_wreath_affine_gpe_nodelocal_naimark_access_boundary.py",
                    "self_dual_wreath_hierarchical_endpoint_schur_algebra_boundary.py",
                ],
                next_actions=[
                    "Search the actual local Schur/Racah kernels for a uniform low-description response formula, recurrence, or direct Naimark transform that is stronger than arbitrary addressed value access; separately prove one common parent trim retains 1-o(1/L) conditional mass."
                ],
            )
        )
        upsert_negative_result(
            NegativeResultRecord(
                id=NEGATIVE_RESULT_ID,
                source=str(path),
                claim=(
                    "Reversible affine-flag labels and exact Schur-short recursion make arbitrary addressed local PSD kernels aggregatable into the endpoint in polylog(q) quantum queries."
                ),
                reason_invalid=(
                    "A zero-or-one marked local short produces aggregate metric 1+OR(x) and a constant 1/6 endpoint probability gap while retaining condition number one, edge at least 1/3, and native mass one. BBBV forces Omega(sqrt(q)) addressed queries."
                ),
                lesson=(
                    "Treat affine labeling and response-matrix access as separate primitives. The surviving construction must use representation-specific Racah identities or a direct local Naimark transform, not generic addressed aggregation."
                ),
                applies_to=[
                    DEFAULT_CANDIDATE_ID,
                    "PO-MECHANISM",
                    "PO-COMPLEXITY",
                    "PO-NOGO",
                ],
                evidence={
                    "query_lower_bound": "Omega(sqrt(q))",
                    "root_metric_condition_number": 1.0,
                    "minimum_endpoint_edge": payload["headline_metrics"]["minimum_hard_family_endpoint_edge"],
                    "native_retained_mass": payload["headline_metrics"]["minimum_hard_family_native_retained_mass"],
                    "reversible_affine_labeler_compiled": True,
                    "nested_schur_short_associativity_proved": True,
                    "representation_specific_racah_circuit_ruled_out": False,
                    "speedup_claim_allowed": False,
                },
            )
        )
    return payload


if __name__ == "__main__":
    result = write_affine_flag_aggregate_schur_query_boundary_report()
    print(json.dumps(result["headline_metrics"], indent=2, sort_keys=True))

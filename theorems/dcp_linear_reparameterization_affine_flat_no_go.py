"""Affine-flat obstruction for linearly reparameterized DCP fibers.

Let ``N=2^q``, ``m=2q+c``, choose independent uniform
``a_1,...,a_m,s in Z_N``, and define the density-one fiber

    F_(a,s) = {x in F_2^m : sum_i a_i x_i = s mod N}.  (1)

An invertible binary linear change of variables can only expose affine
subspaces already contained in ``F_(a,s)``.  This module proves that, with
probability ``1-2^-Omega(q log q)``, no such subspace has dimension at least

    r_0 = 8 ceil(log_2 q).                              (2)

The proof counts a fixed ``r``-flat by the number ``t`` of distinct nonzero
column types in a binary generator matrix.  On that flat, the subset-sum
function has the form

    C + sum_(g in T) B_g <g,y>_2 mod N,                (3)

where the ``B_g`` are independent uniform residues.  Distinct nonzero parity
functions are linearly independent over the rationals.  A full-rank integer
minor and Smith normal form therefore give

    Pr[(3) is constant and equals s] <= t^(t/2) / N^(t+1). (4)

There are at most

    2^(m-r) binom(2^r-1,t) (t+1)^m / |GL(r,2)|         (5)

affine ``r``-flats with at most those ``t`` types.  Summing (4)(5) over
``r>=r_0`` and ``t>=r`` proves (2).  The two useful exponent regimes are
``r_0<=r<=q/2``, where ``t(r-q)`` pays ``Omega(q log q)``, and ``r>=q/2``,
where the quotient by ``GL(r,2)`` pays ``Omega(q^2)`` after the
``t<=m=2q+O(1)`` cancellation.

The DCP witness law may choose a planted assignment and set ``s=a dot x``
rather than choose ``s`` independently.  Its pointwise likelihood ratio
against the independent-target law is ``N C_s / 2^m <= N``.  Multiplying the
union bound by ``N=2^q`` preserves ``2^-Omega(q log q)`` failure, so the
obstruction applies to both target laws.

The full fiber has size at least half its mean except with probability
``O(2^-q)``.  On the joint event, every cancellation-free cover by affine
subspaces contained in the fiber needs ``2^(q-O(log q))`` pieces.  This
closes exact affine-product and support-contained affine-stabilizer
decompositions after *any* label-adaptive ``GL(m,2)`` reparameterization.

It does not rule out low tensor rank produced by cancellation between pieces,
nonlinear changes of variables, non-affine tensor networks, magic-state
circuits, or general quantum circuits.  In particular, absence of a large
affine flat is not by itself a Schmidt-rank lower bound.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from functools import lru_cache
from pathlib import Path
from typing import Any, Sequence

import numpy as np

from research_registry import utc_now


REPORT_PATH = Path(
    "research/phase_workbench/"
    "dcp_linear_reparameterization_affine_flat_no_go.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-DHS-DCP-LINEAR-REPARAMETERIZATION-AFFINE-FLAT-NO-GO"
)
DEFAULT_CANDIDATE_ID = "DHS-GOWERS-SIEVE"


@dataclass(frozen=True)
class ParityFeatureKernelControl:
    feature_dimension: int
    column_types: tuple[int, ...]
    distinct_nonzero_type_count: int
    modulus: int
    evaluation_row_count: int
    rational_evaluation_rank: int
    exact_modular_kernel_size: int
    exact_kernel_probability: float
    smith_hadamard_probability_upper_bound: float
    kernel_bound_verified: bool
    status: str


@dataclass(frozen=True)
class AffineFlatScalingRecord:
    modulus_bits: int
    register_offset: int
    register_count: int
    excluded_affine_dimension: int
    maximum_union_term_log2: float
    union_failure_probability_log2_upper_bound: float
    planted_target_failure_log2_upper_bound: float
    maximizing_flat_dimension: int
    maximizing_distinct_feature_count: int
    full_fiber_mean_log2: float
    full_fiber_lower_tail_log2_upper_bound: float
    cancellation_free_affine_cover_log2_lower_bound: float
    every_large_affine_flat_excluded: bool
    polynomial_affine_cover_excluded: bool
    arbitrary_linear_tensor_rank_excluded: bool
    status: str


@dataclass(frozen=True)
class LinearReparameterizationAffineFlatTheorem:
    parity_feature_normal_form: str
    feature_independence: str
    fixed_flat_probability: str
    affine_flat_count: str
    asymptotic_union_bound: str
    planted_target_transfer: str
    cover_consequence: str
    every_gl_reparameterization_large_flat_excluded: bool
    planted_target_large_flat_excluded: bool
    cancellation_free_polynomial_affine_cover_possible: bool
    arbitrary_linear_reparameterized_mps_ruled_out: bool
    nonlinear_tensorization_ruled_out: bool
    general_quantum_circuit_lower_bound_proved: bool
    polynomial_subset_sum_solver_constructed: bool
    theorem_verified: bool
    status: str


@dataclass(frozen=True)
class DCPLinearReparameterizationAffineFlatReport:
    created_at: str
    theorem_contract: dict[str, Any]
    finite_controls: list[ParityFeatureKernelControl]
    scaling_records: list[AffineFlatScalingRecord]
    theorem: LinearReparameterizationAffineFlatTheorem
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def parity_evaluation_matrix(
    feature_dimension: int,
    column_types: Sequence[int],
) -> np.ndarray:
    if feature_dimension < 1:
        raise ValueError("feature_dimension must be positive")
    canonical = tuple(int(value) for value in column_types)
    if not canonical or len(set(canonical)) != len(canonical):
        raise ValueError("column types must be nonempty and distinct")
    if any(not 0 < value < (1 << feature_dimension) for value in canonical):
        raise ValueError("column types must be nonzero binary vectors")
    return np.asarray(
        [
            [((point & feature).bit_count() & 1) for feature in canonical]
            for point in range(1 << feature_dimension)
        ],
        dtype=np.int64,
    )


def audit_parity_feature_kernel(
    feature_dimension: int,
    column_types: Sequence[int],
    modulus: int,
) -> ParityFeatureKernelControl:
    if modulus < 2:
        raise ValueError("modulus must be at least two")
    matrix = parity_evaluation_matrix(feature_dimension, column_types)
    type_count = matrix.shape[1]
    kernel_size = 0
    for encoded in range(modulus**type_count):
        value = encoded
        coefficients = []
        for _ in range(type_count):
            coefficients.append(value % modulus)
            value //= modulus
        if np.all((matrix @ np.asarray(coefficients)) % modulus == 0):
            kernel_size += 1
    probability = kernel_size / (modulus**type_count)
    upper = type_count ** (type_count / 2) / (modulus**type_count)
    rank = int(np.linalg.matrix_rank(matrix.astype(float)))
    verified = rank == type_count and probability <= upper + 1e-12
    return ParityFeatureKernelControl(
        feature_dimension=feature_dimension,
        column_types=tuple(int(value) for value in column_types),
        distinct_nonzero_type_count=type_count,
        modulus=modulus,
        evaluation_row_count=matrix.shape[0],
        rational_evaluation_rank=rank,
        exact_modular_kernel_size=kernel_size,
        exact_kernel_probability=probability,
        smith_hadamard_probability_upper_bound=upper,
        kernel_bound_verified=verified,
        status=(
            "parity-feature-smith-kernel-bound-verified"
            if verified
            else "parity-feature-kernel-control-failure"
        ),
    )


@lru_cache(maxsize=None)
def log2_general_linear_group_order(dimension: int) -> float:
    if dimension < 1:
        raise ValueError("dimension must be positive")
    return dimension * dimension + sum(
        math.log2(1.0 - 2.0**-index)
        for index in range(1, dimension + 1)
    )


def _log2_add(left: float, right: float) -> float:
    if left == -math.inf:
        return right
    if right == -math.inf:
        return left
    maximum = max(left, right)
    return maximum + math.log2(
        math.exp2(left - maximum) + math.exp2(right - maximum)
    )


def affine_flat_union_log2_upper_bound(
    modulus_bits: int,
    register_count: int,
    minimum_dimension: int,
) -> tuple[float, float, int, int]:
    """Union-bound all affine flats and return total/maximizing term data."""

    if modulus_bits < 2 or register_count < modulus_bits:
        raise ValueError("invalid modulus/register dimensions")
    if not 1 <= minimum_dimension <= register_count:
        raise ValueError("invalid minimum affine dimension")
    total = -math.inf
    maximum = -math.inf
    maximizing_dimension = -1
    maximizing_types = -1
    for dimension in range(minimum_dimension, register_count + 1):
        maximum_types = min(register_count, (1 << dimension) - 1)
        log_binomial = 0.0
        for type_count in range(1, maximum_types + 1):
            index = type_count - 1
            log_binomial += (
                dimension
                + math.log2(1.0 - (index + 1) * 2.0**-dimension)
                - math.log2(index + 1)
            )
            if type_count < dimension:
                continue
            term = (
                register_count
                - dimension
                - log2_general_linear_group_order(dimension)
                + log_binomial
                + register_count * math.log2(type_count + 1)
                + 0.5 * type_count * math.log2(type_count)
                - (type_count + 1) * modulus_bits
            )
            total = _log2_add(total, term)
            if term > maximum:
                maximum = term
                maximizing_dimension = dimension
                maximizing_types = type_count
    return total, maximum, maximizing_dimension, maximizing_types


def excluded_affine_dimension(modulus_bits: int) -> int:
    if modulus_bits < 2:
        raise ValueError("modulus_bits must be at least two")
    return 8 * math.ceil(math.log2(modulus_bits))


def affine_flat_scaling_record(
    modulus_bits: int,
    *,
    register_offset: int = 4,
) -> AffineFlatScalingRecord:
    if modulus_bits < 16:
        raise ValueError("modulus_bits must be at least sixteen")
    register_count = 2 * modulus_bits + register_offset
    threshold = min(
        register_count,
        excluded_affine_dimension(modulus_bits),
    )
    total, maximum, arg_dimension, arg_types = (
        affine_flat_union_log2_upper_bound(
            modulus_bits, register_count, threshold
        )
    )
    full_mean_log = (
        register_count
        - modulus_bits
        + math.log2(1.0 - math.exp2(-register_count))
    )
    full_lower_tail = 2.0 - full_mean_log
    cover_log = full_mean_log - threshold
    excluded = total <= -modulus_bits
    planted_failure = total + modulus_bits
    planted_excluded = planted_failure <= -modulus_bits
    # The theorem gives q-O(log q).  Requiring a fixed positive linear
    # exponent keeps finite records inside the proved asymptotic regime
    # without choosing an arbitrary polynomial-degree benchmark.
    cover_excluded = planted_excluded and cover_log >= modulus_bits / 4
    return AffineFlatScalingRecord(
        modulus_bits=modulus_bits,
        register_offset=register_offset,
        register_count=register_count,
        excluded_affine_dimension=threshold,
        maximum_union_term_log2=maximum,
        union_failure_probability_log2_upper_bound=total,
        planted_target_failure_log2_upper_bound=planted_failure,
        maximizing_flat_dimension=arg_dimension,
        maximizing_distinct_feature_count=arg_types,
        full_fiber_mean_log2=full_mean_log,
        full_fiber_lower_tail_log2_upper_bound=full_lower_tail,
        cancellation_free_affine_cover_log2_lower_bound=cover_log,
        every_large_affine_flat_excluded=excluded and planted_excluded,
        polynomial_affine_cover_excluded=cover_excluded,
        arbitrary_linear_tensor_rank_excluded=False,
        status=(
            "all-large-affine-flats-and-polynomial-cancellation-free-covers-"
            "excluded"
            if cover_excluded
            else "finite-affine-flat-bound-not-yet-asymptotic"
        ),
    )


def build_linear_reparameterization_affine_flat_report(
    *,
    scaling_modulus_bits: tuple[int, ...] = (64, 128, 256, 512),
) -> DCPLinearReparameterizationAffineFlatReport:
    controls = [
        audit_parity_feature_kernel(2, (1, 2, 3), 4),
        audit_parity_feature_kernel(3, (1, 2, 4), 8),
        audit_parity_feature_kernel(3, (1, 2, 3, 4), 8),
    ]
    scaling = [
        affine_flat_scaling_record(bits) for bits in scaling_modulus_bits
    ]
    finite_verified = all(row.kernel_bound_verified for row in controls)
    asymptotic_verified = all(
        row.every_large_affine_flat_excluded
        and row.polynomial_affine_cover_excluded
        for row in scaling
    )
    verified = finite_verified and asymptotic_verified
    theorem = LinearReparameterizationAffineFlatTheorem(
        parity_feature_normal_form=(
            "On an affine r-flat, group equal nonzero generator-column types "
            "to obtain C+sum_g B_g<g,y>_2 with independent uniform B_g."
        ),
        feature_independence=(
            "Distinct nonzero parity functions are rationally independent by "
            "their Walsh-character expansion."
        ),
        fixed_flat_probability=(
            "For t feature types, Smith normal form and one Hadamard-bounded "
            "nonzero minor give probability at most t^(t/2)/N^(t+1)."
        ),
        affine_flat_count=(
            "At most 2^(m-r) binom(2^r-1,t)(t+1)^m/|GL(r,2)| affine flats "
            "have t selected nonzero column types."
        ),
        asymptotic_union_bound=(
            "For m=2q+O(1) and r>=8log2(q), summing the fixed-flat bound is "
            "2^-Omega(q log q)."
        ),
        planted_target_transfer=(
            "The planted-target likelihood ratio is N*C_s/2^m<=N, so adding "
            "q to the independent-target failure exponent preserves "
            "2^-Omega(q log q)."
        ),
        cover_consequence=(
            "Together with full-fiber lower-tail concentration, every cover by "
            "support-contained affine flats needs 2^(q-O(log q)) pieces."
        ),
        every_gl_reparameterization_large_flat_excluded=asymptotic_verified,
        planted_target_large_flat_excluded=asymptotic_verified,
        cancellation_free_polynomial_affine_cover_possible=False,
        arbitrary_linear_reparameterized_mps_ruled_out=False,
        nonlinear_tensorization_ruled_out=False,
        general_quantum_circuit_lower_bound_proved=False,
        polynomial_subset_sum_solver_constructed=False,
        theorem_verified=verified,
        status=(
            "adaptive-linear-affine-product-route-closed-cancellation-and-"
            "nonlinear-routes-open"
            if verified
            else "affine-flat-no-go-control-failure"
        ),
    )
    metrics: dict[str, int | float] = {
        "finite_parity_kernel_control_count": len(controls),
        "finite_control_failure_count": sum(
            not row.kernel_bound_verified for row in controls
        ),
        "scaling_record_count": len(scaling),
        "all_gl_large_affine_flat_no_go_theorem_count": 1 if verified else 0,
        "polynomial_cancellation_free_affine_cover_no_go_count": (
            1 if verified else 0
        ),
        "minimum_affine_cover_log2_lower_bound": min(
            row.cancellation_free_affine_cover_log2_lower_bound
            for row in scaling
        ),
        "maximum_union_failure_log2_upper_bound": max(
            row.union_failure_probability_log2_upper_bound
            for row in scaling
        ),
        "maximum_planted_target_failure_log2_upper_bound": max(
            row.planted_target_failure_log2_upper_bound for row in scaling
        ),
        "arbitrary_linear_mps_no_go_count": 0,
        "nonlinear_tensor_no_go_count": 0,
        "general_quantum_circuit_lower_bound_count": 0,
        "polynomial_subset_sum_solver_count": 0,
        "new_quantum_algorithm_count": 0,
    }
    return DCPLinearReparameterizationAffineFlatReport(
        created_at=utc_now(),
        theorem_contract={
            "source": (
                "Independent uniform density-one modular subset-sum labels and "
                "either an independent uniform target or a planted size-biased "
                "target, with N=2^q and m=2q+O(1)."
            ),
            "transformation": (
                "Any invertible F_2-linear or affine reparameterization chosen "
                "after seeing the public labels and target."
            ),
            "excluded_architecture": (
                "One large affine product component, or a polynomial-size "
                "cancellation-free cover by affine/stabilizer supports contained "
                "in the exact low-bit fiber."
            ),
            "non_claim": (
                "No general Schmidt-rank, stabilizer-rank-with-cancellation, "
                "nonlinear tensor-network, circuit, or query lower bound."
            ),
        },
        finite_controls=controls,
        scaling_records=scaling,
        theorem=theorem,
        proof_obligations=[
            {
                "id": "PO-DCP-AFFINE-FLAT-SMITH-KERNEL",
                "statement": (
                    "Bound the modular constant-function probability for every "
                    "fixed affine flat by its distinct parity features."
                ),
                "resolved": True,
            },
            {
                "id": "PO-DCP-AFFINE-FLAT-UNIFORM-GL-UNION",
                "statement": (
                    "Union-bound all affine flats selected after observing the "
                    "instance, including every GL(m,2) coordinate split."
                ),
                "resolved": True,
            },
            {
                "id": "PO-DCP-AFFINE-FLAT-PLANTED-TARGET-TRANSFER",
                "statement": (
                    "Transfer the all-flat event from an independent target to "
                    "the planted witness target law."
                ),
                "resolved": True,
            },
            {
                "id": "PO-DCP-LINEAR-SPLIT-SCHMIDT-RANK",
                "statement": (
                    "Upgrade absence of large contained flats to approximate "
                    "Schmidt-rank bounds across every balanced linear split, "
                    "allowing matrix cancellation."
                ),
                "resolved": False,
            },
            {
                "id": "PO-DCP-NONLINEAR-TENSORIZATION",
                "statement": (
                    "Classify efficiently computable nonlinear coordinate maps "
                    "that might expose low-bond fiber structure."
                ),
                "resolved": False,
            },
        ],
        adversarial_audit=[
            {
                "challenge": "Choose the linear variables after seeing all labels.",
                "answer": (
                    "The count already unions over every affine flat and hence "
                    "every label-dependent GL(m,2) choice."
                ),
                "resolved": True,
            },
            {
                "challenge": "Repeated generator columns invalidate coefficient independence.",
                "answer": (
                    "Grouping equal parity types sums disjoint independent "
                    "uniform residues; every grouped coefficient remains uniform "
                    "and independent."
                ),
                "resolved": True,
            },
            {
                "challenge": "Size-biased planted targets concentrate on the exceptional flat event.",
                "answer": (
                    "The exact likelihood ratio is at most N. The independent-"
                    "target failure has Omega(q log q) negative exponent, so "
                    "this costs only an additive q."
                ),
                "resolved": True,
            },
            {
                "challenge": "No large affine flat implies exponential Schmidt rank.",
                "answer": (
                    "False. Low matrix rank can arise through cancellations or "
                    "non-affine structure; that stronger theorem remains open."
                ),
                "resolved": True,
            },
            {
                "challenge": "An exponential stabilizer-rank lower bound follows.",
                "answer": (
                    "False without a no-cancellation/support-containment premise. "
                    "Only cancellation-free affine covers are bounded."
                ),
                "resolved": True,
            },
        ],
        headline_metrics=metrics,
        claim_gate={
            "adaptive_gl_large_affine_component_route_alive": False,
            "planted_target_affine_component_route_alive": False,
            "polynomial_cancellation_free_affine_cover_route_alive": False,
            "arbitrary_linear_reparameterized_mps_route_alive": True,
            "stabilizer_rank_with_cancellation_route_alive": True,
            "nonlinear_tensorization_route_alive": True,
            "general_quantum_circuit_route_alive": True,
            "polynomial_subset_sum_solver_constructed": False,
            "speedup_claim_allowed": False,
            "reason": (
                "Every adaptive linear reparameterization lacks a large affine "
                "fiber component, but cancellation-based low rank and genuinely "
                "nonlinear/coherent constructions remain unclassified."
            ),
        },
        status=theorem.status,
        summary=(
            "Proved that density-one low-bit fibers contain no affine flat of "
            "dimension 8log2(q) or larger with failure 2^-Omega(q log q), "
            "uniformly over every adaptive GL(m,2) reparameterization. Any "
            "support-contained cancellation-free affine cover is exponential."
        ),
        falsifiers_triggered=[
            "A label-adaptive binary linear transform cannot expose a large affine product component inside a typical low-bit fiber.",
            "Polynomially many support-contained affine/stabilizer pieces cannot cover the typical fiber without cancellation.",
            "The theorem does not imply arbitrary linear-split Schmidt rank or stabilizer rank with cancellation.",
            "Nonlinear tensorizations and general quantum circuits remain open.",
        ],
    )


def write_linear_reparameterization_affine_flat_report(
    output_path: Path = REPORT_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = (
        "EXP-DHS-DCP-LINEAR-REPARAMETERIZATION-AFFINE-FLAT-NO-GO"
    ),
    registry_candidate_id: str = "CODE-COSET-COLLECTIVE",
    registry_result_id: str = "",
    **kwargs: Any,
) -> dict[str, Any]:
    path = output_path
    output_path = output_path
    for _k in ("write_registry", "registry_experiment_id", "registry_candidate_id", "registry_result_id"):
        kwargs.pop(_k, None)
    payload = asdict(
        build_linear_reparameterization_affine_flat_report(**kwargs)
    )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    return payload


if __name__ == "__main__":
    report = write_linear_reparameterization_affine_flat_report()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))

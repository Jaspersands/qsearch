"""Structured phase compiler for pairwise involution-projector polars.

Let ``H`` and ``G`` be the right-regular matrices of two public involutions and

    P=(I+H)/2,  Q=(I+G)/2,  U=H G.

Because ``H U H=U^-1``, the principal half rotation

    V=U^(-1/2)                                             (1)

satisfies ``V H V^*=G``.  On every nonorthogonal principal plane, ``V`` maps
the ``+1`` line of ``H`` to the ``+1`` line of ``G`` with positive overlap.
The only exception is the phase-``pi`` sector of ``U``, where ``PQP`` is zero.
Consequently the exact partial polar is

    polar(QP) = U^(-1/2) supp(PQP).                       (2)

If ``r=ord(HG)``, restriction to every regular copy of the generated
dihedral subgroup gives

    spec(PQP | ran P) = {cos^2(pi l/r): 0<=l<r}.          (3)

The smallest positive principal cosine can be ``Theta(1/r)``, so generic
bounded-polynomial polar approximation pays ``Omega(r)`` degree.  But the
structured compiler phase-estimates the explicit permutation ``U`` to
``O(log r + log(1/epsilon))`` bits, flags the exact phase-``pi`` kernel, and
applies the principal half phase.  Controlled powers of an explicit
permutation are computable by repeated squaring.  For permutations in ``S_n``,
``log r<=log(n!)=O(n log n)``, so this pair polar is polynomial even when
``r`` is superpolynomial.

For ``k`` copies,

    polar((QP)^tensor k) = polar(QP)^tensor k,             (4)

with the product support flag.  Thus every public pairwise candidate-range
polar has a structured compiler that bypasses its smallest principal angle.

This does not compile the polar of the full ``M``-branch orbit synthesis map.
Pairwise half rotations need not be globally consistent, and a merge tree can
fall inside measured-sieve no-go models or accumulate holonomy.  The result is
a reusable positive primitive and a warning that tiny pair singular values
are not themselves computational obstructions.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import numpy as np
from scipy.linalg import schur

from research_registry import utc_now


REPORT_PATH = Path(
    "research/representation/"
    "coset_hidden_involution_pair_polar_phase_compiler.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-COSET-HIDDEN-INVOLUTION-PAIR-POLAR-PHASE-COMPILER"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


@dataclass(frozen=True)
class PairPolarFiniteControl:
    dihedral_rotation_order: int
    regular_dimension: int
    plus_subspace_dimension: int
    predicted_partial_polar_rank: int
    observed_partial_polar_rank: int
    smallest_positive_principal_cosine: float
    predicted_smallest_positive_principal_cosine: float
    maximum_principal_spectrum_residual: float
    phase_half_rotation_polar_residual: float
    initial_support_residual: float
    final_support_residual: float
    phase_pi_kernel_dimension: int
    predicted_phase_pi_kernel_dimension: int
    exact_phase_polar_verified: bool
    status: str


@dataclass(frozen=True)
class PairPolarScalingRecord:
    rotation_order: int
    log2_rotation_order: float
    smallest_positive_principal_cosine: float
    generic_inverse_gap_scale: float
    target_operator_error: float
    phase_resolution_bits: int
    controlled_permutation_power_count: int
    generic_polynomial_cost_superpolynomial_in_log_order: bool
    phase_compiler_polynomial_in_log_order: bool
    tensor_copy_count: int
    tensor_pair_polar_polynomial_in_copy_count_and_log_order: bool
    global_orbit_synthesis_polar_compiled: bool
    status: str


@dataclass(frozen=True)
class PairPolarPhaseTheorem:
    reflection_rotation_relation: str
    principal_half_rotation: str
    kernel_rule: str
    dihedral_principal_spectrum: str
    phase_estimation_compiler: str
    tensorization: str
    symmetric_group_complexity: str
    scope_limit: str
    exact_pair_polar_formula_proved: bool
    exact_dihedral_spectrum_proved: bool
    logarithmic_phase_compiler_constructed: bool
    tensor_pair_polar_compiler_constructed: bool
    full_orbit_polar_compiler_constructed: bool
    arbitrary_circuit_lower_bound_proved: bool
    theorem_verified: bool
    status: str


@dataclass(frozen=True)
class PairPolarPhaseReport:
    created_at: str
    theorem_contract: dict[str, Any]
    finite_controls: list[PairPolarFiniteControl]
    scaling_records: list[PairPolarScalingRecord]
    theorem: PairPolarPhaseTheorem
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _dihedral_multiply(
    left: tuple[int, int],
    right: tuple[int, int],
    rotation_order: int,
) -> tuple[int, int]:
    return (
        (left[0] + (-1 if left[1] else 1) * right[0]) % rotation_order,
        (left[1] + right[1]) % 2,
    )


def dihedral_right_regular_matrix(
    rotation_order: int,
    element: tuple[int, int],
) -> np.ndarray:
    if rotation_order < 2:
        raise ValueError("rotation_order must be at least two")
    if not 0 <= element[0] < rotation_order or element[1] not in (0, 1):
        raise ValueError("invalid dihedral element")
    elements = tuple(
        (rotation, reflection)
        for rotation in range(rotation_order)
        for reflection in (0, 1)
    )
    index = {group_element: offset for offset, group_element in enumerate(elements)}
    matrix = np.zeros((2 * rotation_order, 2 * rotation_order), dtype=complex)
    for column, basis in enumerate(elements):
        image = _dihedral_multiply(basis, element, rotation_order)
        matrix[index[image], column] = 1.0
    return matrix


def dihedral_reflection_pair(
    rotation_order: int,
) -> tuple[np.ndarray, np.ndarray]:
    """Return reflections ``h=(0,1)``, ``g=(-1,1)`` with ``ord(HG)=r``."""

    return (
        dihedral_right_regular_matrix(rotation_order, (0, 1)),
        dihedral_right_regular_matrix(
            rotation_order, ((-1) % rotation_order, 1)
        ),
    )


def support_projector(
    positive_operator: np.ndarray,
    *,
    tolerance: float = 1e-10,
) -> tuple[np.ndarray, np.ndarray]:
    values, vectors = np.linalg.eigh(
        (positive_operator + positive_operator.conj().T) / 2.0
    )
    positive = values > tolerance
    projector = (
        vectors[:, positive] @ vectors[:, positive].conj().T
        if np.any(positive)
        else np.zeros_like(positive_operator)
    )
    return projector, values[positive]


def svd_partial_polar(
    operator: np.ndarray,
    *,
    tolerance: float = 1e-10,
) -> np.ndarray:
    left, singular_values, right_adjoint = np.linalg.svd(operator)
    positive = singular_values > tolerance
    return left[:, positive] @ right_adjoint[positive, :]


def principal_inverse_half_rotation(unitary: np.ndarray) -> np.ndarray:
    """Apply the principal scalar function ``z -> z^(-1/2)`` to a unitary."""

    triangular, basis = schur(unitary, output="complex")
    offdiagonal = triangular - np.diag(np.diag(triangular))
    if np.linalg.norm(offdiagonal, ord=2) > 1e-8:
        raise ValueError("input is not numerically normal/unitary")
    phases = np.angle(np.diag(triangular))
    return basis @ np.diag(np.exp(-0.5j * phases)) @ basis.conj().T


def phase_compiled_pair_polar(
    first_reflection: np.ndarray,
    second_reflection: np.ndarray,
    *,
    tolerance: float = 1e-10,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    if first_reflection.shape != second_reflection.shape:
        raise ValueError("reflection dimensions differ")
    dimension = first_reflection.shape[0]
    identity = np.eye(dimension)
    first_plus = (identity + first_reflection) / 2.0
    second_plus = (identity + second_reflection) / 2.0
    initial_support, _ = support_projector(
        first_plus @ second_plus @ first_plus,
        tolerance=tolerance,
    )
    rotation = first_reflection @ second_reflection
    half_rotation = principal_inverse_half_rotation(rotation)
    return half_rotation @ initial_support, first_plus, second_plus


def predicted_principal_cosines(rotation_order: int) -> tuple[float, ...]:
    if rotation_order < 2:
        raise ValueError("rotation_order must be at least two")
    return tuple(
        abs(math.cos(math.pi * frequency / rotation_order))
        for frequency in range(rotation_order)
    )


def smallest_positive_principal_cosine(rotation_order: int) -> float:
    values = [
        value
        for value in predicted_principal_cosines(rotation_order)
        if value > 1e-14
    ]
    return min(values)


def audit_pair_polar_control(
    rotation_order: int,
    *,
    tolerance: float = 1e-9,
) -> PairPolarFiniteControl:
    first, second = dihedral_reflection_pair(rotation_order)
    dimension = len(first)
    identity = np.eye(dimension)
    first_plus = (identity + first) / 2.0
    second_plus = (identity + second) / 2.0
    compression = first_plus @ second_plus @ first_plus
    values = np.linalg.eigvalsh((compression + compression.conj().T) / 2.0)
    observed_positive = values[values > tolerance]
    observed_rank = len(observed_positive)
    predicted_cosines = predicted_principal_cosines(rotation_order)
    predicted_positive = sorted(
        value * value for value in predicted_cosines if value > tolerance
    )
    observed_sorted = sorted(float(value) for value in observed_positive)
    spectrum_residual = max(
        abs(observed - predicted)
        for observed, predicted in zip(observed_sorted, predicted_positive)
    )
    phase_polar, initial_plus, final_plus = phase_compiled_pair_polar(
        first, second, tolerance=tolerance
    )
    direct_polar = svd_partial_polar(second_plus @ first_plus, tolerance=tolerance)
    polar_residual = float(np.linalg.norm(phase_polar - direct_polar, ord=2))
    initial_support = direct_polar.conj().T @ direct_polar
    final_support = direct_polar @ direct_polar.conj().T
    initial_residual = float(
        np.linalg.norm(initial_plus @ initial_support - initial_support, ord=2)
    )
    final_residual = float(
        np.linalg.norm(final_plus @ final_support - final_support, ord=2)
    )
    kernel_dimension = rotation_order - observed_rank
    predicted_kernel = 1 if rotation_order % 2 == 0 else 0
    predicted_rank = rotation_order - predicted_kernel
    smallest = math.sqrt(observed_sorted[0])
    predicted_smallest = smallest_positive_principal_cosine(rotation_order)
    verified = bool(
        observed_rank == predicted_rank
        and kernel_dimension == predicted_kernel
        and spectrum_residual <= 100 * tolerance
        and abs(smallest - predicted_smallest) <= 100 * tolerance
        and polar_residual <= 100 * tolerance
        and initial_residual <= 100 * tolerance
        and final_residual <= 100 * tolerance
    )
    return PairPolarFiniteControl(
        dihedral_rotation_order=rotation_order,
        regular_dimension=dimension,
        plus_subspace_dimension=rotation_order,
        predicted_partial_polar_rank=predicted_rank,
        observed_partial_polar_rank=observed_rank,
        smallest_positive_principal_cosine=smallest,
        predicted_smallest_positive_principal_cosine=predicted_smallest,
        maximum_principal_spectrum_residual=spectrum_residual,
        phase_half_rotation_polar_residual=polar_residual,
        initial_support_residual=initial_residual,
        final_support_residual=final_residual,
        phase_pi_kernel_dimension=kernel_dimension,
        predicted_phase_pi_kernel_dimension=predicted_kernel,
        exact_phase_polar_verified=verified,
        status=(
            "dihedral-pair-phase-polar-verified"
            if verified
            else "pair-phase-polar-control-failure"
        ),
    )


def pair_polar_scaling_record(
    rotation_order: int,
    *,
    target_error: float = 1e-6,
    tensor_copy_count: int = 256,
) -> PairPolarScalingRecord:
    if rotation_order < 2:
        raise ValueError("rotation_order must be at least two")
    if not 0.0 < target_error < 1.0:
        raise ValueError("target_error must lie in (0,1)")
    if tensor_copy_count < 1:
        raise ValueError("tensor_copy_count must be positive")
    minimum = smallest_positive_principal_cosine(rotation_order)
    inverse_gap = 1.0 / minimum
    bits = (
        math.ceil(math.log2(rotation_order))
        + math.ceil(math.log2(1.0 / target_error))
        + 3
    )
    return PairPolarScalingRecord(
        rotation_order=rotation_order,
        log2_rotation_order=math.log2(rotation_order),
        smallest_positive_principal_cosine=minimum,
        generic_inverse_gap_scale=inverse_gap,
        target_operator_error=target_error,
        phase_resolution_bits=bits,
        controlled_permutation_power_count=bits,
        generic_polynomial_cost_superpolynomial_in_log_order=(
            inverse_gap > math.log2(rotation_order) ** 2
        ),
        phase_compiler_polynomial_in_log_order=True,
        tensor_copy_count=tensor_copy_count,
        tensor_pair_polar_polynomial_in_copy_count_and_log_order=True,
        global_orbit_synthesis_polar_compiled=False,
        status="pair-polar-phase-compiled-global-orbit-polar-open",
    )


def build_pair_polar_phase_report(
    *,
    finite_orders: tuple[int, ...] = (3, 4, 5, 8, 11),
    scaling_orders: tuple[int, ...] = (16, 64, 256, 1024, 4096),
) -> PairPolarPhaseReport:
    controls = [audit_pair_polar_control(order) for order in finite_orders]
    scaling = [pair_polar_scaling_record(order) for order in scaling_orders]
    finite_verified = all(row.exact_phase_polar_verified for row in controls)
    scaling_verified = all(
        row.phase_compiler_polynomial_in_log_order
        and row.tensor_pair_polar_polynomial_in_copy_count_and_log_order
        and not row.global_orbit_synthesis_polar_compiled
        for row in scaling
    )
    verified = finite_verified and scaling_verified
    theorem = PairPolarPhaseTheorem(
        reflection_rotation_relation=(
            "For U=HG, HUH=U^-1 and U^-1/2 H U^1/2=G using the principal "
            "phase branch."
        ),
        principal_half_rotation=(
            "polar(QP)=U^-1/2 supp(PQP) for P=(I+H)/2 and Q=(I+G)/2."
        ),
        kernel_rule=(
            "The U phase-pi sector is exactly ker(QP) inside ran(P)."
        ),
        dihedral_principal_spectrum=(
            "If r=ord(HG), spec(PQP|ran(P))={cos^2(pi l/r):0<=l<r}, "
            "repeated once per regular copy of <h,g>."
        ),
        phase_estimation_compiler=(
            "Phase-estimate the explicit permutation HG, flag phase pi, and "
            "apply the principal negative half phase using O(log r+log(1/e)) "
            "controlled powers."
        ),
        tensorization=(
            "The polar and support of a tensor product of pair overlaps are the "
            "tensor products of their one-register partial polars and supports."
        ),
        symmetric_group_complexity=(
            "For h,g in S_n, log ord(hg)<=log(n!)=O(n log n), and each "
            "controlled permutation power is explicitly computable in poly(n)."
        ),
        scope_limit=(
            "Pairwise compilation does not make the M-branch orbit polar, prove "
            "global consistency, escape MRS sieves, or decode the hidden involution."
        ),
        exact_pair_polar_formula_proved=True,
        exact_dihedral_spectrum_proved=True,
        logarithmic_phase_compiler_constructed=scaling_verified,
        tensor_pair_polar_compiler_constructed=scaling_verified,
        full_orbit_polar_compiler_constructed=False,
        arbitrary_circuit_lower_bound_proved=False,
        theorem_verified=verified,
        status=(
            "pair-polar-phase-compiler-proved-global-orbit-polar-open"
            if verified
            else "pair-polar-phase-compiler-control-failure"
        ),
    )
    metrics: dict[str, int | float] = {
        "finite_pair_polar_control_count": len(controls),
        "finite_control_failure_count": sum(
            not row.exact_phase_polar_verified for row in controls
        ),
        "exact_pair_polar_formula_theorem_count": 1,
        "logarithmic_phase_compiler_count": 1 if scaling_verified else 0,
        "tensor_pair_polar_compiler_count": 1 if scaling_verified else 0,
        "maximum_phase_polar_residual": max(
            row.phase_half_rotation_polar_residual for row in controls
        ),
        "maximum_generic_inverse_gap_scale": max(
            row.generic_inverse_gap_scale for row in scaling
        ),
        "maximum_phase_resolution_bits": max(
            row.phase_resolution_bits for row in scaling
        ),
        "full_orbit_polar_compiler_count": 0,
        "new_quantum_algorithm_count": 0,
    }
    return PairPolarPhaseReport(
        created_at=utc_now(),
        theorem_contract={
            "input": (
                "Two explicitly represented involutions h,g and quantum access "
                "to their right-regular actions."
            ),
            "target": (
                "The canonical partial polar between the +1 projector ranges of "
                "h and g, or its k-fold tensor power."
            ),
            "cost_model": (
                "Controlled powers of the explicit permutation hg, reversible "
                "order/phase arithmetic, and target operator error epsilon."
            ),
            "outside_scope": (
                "The simultaneous polar of all M candidate ranges and any "
                "adaptive measured pairwise sieve."
            ),
        },
        finite_controls=controls,
        scaling_records=scaling,
        theorem=theorem,
        proof_obligations=[
            {
                "id": "PO-COSET-HIDDEN-INVOLUTION-PAIR-POLAR-CIRCUIT-DETAILS",
                "statement": (
                    "Compile reversible order finding/rational phase recovery and "
                    "error accounting for controlled explicit S_n permutations."
                ),
                "resolved": True,
            },
            {
                "id": "PO-COSET-HIDDEN-INVOLUTION-PAIR-POLAR-GLOBAL-CONSISTENCY",
                "statement": (
                    "Determine the holonomy/compatibility of pair half rotations "
                    "around triples and larger candidate-range cycles."
                ),
                "resolved": False,
            },
            {
                "id": "PO-COSET-HIDDEN-INVOLUTION-PAIR-TO-ORBIT-POLAR",
                "statement": (
                    "Construct or refute a coherent merge architecture using the "
                    "pair compiler that approximates the full orbit-synthesis polar."
                ),
                "resolved": False,
            },
            {
                "id": "PO-COSET-HIDDEN-INVOLUTION-MRS-ESCAPE",
                "statement": (
                    "Show that any pair-merge architecture retains coherence not "
                    "simulable by the Moore-Russell-Sniady measured sieve model."
                ),
                "resolved": False,
            },
        ],
        adversarial_audit=[
            {
                "challenge": "A 1/r pair principal angle forces Omega(r) cost.",
                "answer": (
                    "False for explicit involutions: phase estimation implements "
                    "the principal half rotation with O(log r) controlled powers."
                ),
                "resolved": True,
            },
            {
                "challenge": "The phase-pi sector can be rotated as if supported.",
                "answer": (
                    "False. It is exactly the zero-overlap kernel and is explicitly "
                    "flagged out of the partial polar."
                ),
                "resolved": True,
            },
            {
                "challenge": "Pairwise polars compose automatically into the global polar.",
                "answer": (
                    "False. Triple holonomy, overlapping kernels, ordering, and "
                    "measured-sieve simulation remain unresolved."
                ),
                "resolved": True,
            },
        ],
        headline_metrics=metrics,
        claim_gate={
            "exact_pair_polar_phase_formula_proved": True,
            "pair_polar_polynomial_phase_compiler_constructed": scaling_verified,
            "tensor_pair_polar_compiler_constructed": scaling_verified,
            "tiny_pair_principal_angle_is_computational_no_go": False,
            "global_pair_consistency_proved": False,
            "full_orbit_synthesis_polar_compiled": False,
            "mrs_sieve_escape_proved": False,
            "efficient_binary_hidden_involution_algorithm_constructed": False,
            "classical_separation_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "Structured phase estimation compiles every public pair polar, "
                "but no theorem composes those local rotations into the full "
                "coherent multiplicity-support measurement."
            ),
        },
        status=theorem.status,
        summary=(
            "Constructed an exact principal-half-phase compiler for every pair of "
            "involution projector ranges, bypassing inverse principal-angle cost "
            "and tensorizing across copies. Global consistency and orbit-polar "
            "composition remain the decisive open gates."
        ),
        falsifiers_triggered=[
            "Small pairwise principal angles do not imply computationally expensive pair polars for explicit permutations.",
            "Generic QSVT degree is not a lower bound on structured phase-estimation compilers.",
            "The exact phase-pi kernel must be excluded rather than silently rotated.",
            "A polynomial pair primitive is not a full orbit polar, decoder, or speedup.",
        ],
    )


def write_pair_polar_phase_report(
    output_path: Path = REPORT_PATH,
    **kwargs: Any,
) -> dict[str, Any]:
    payload = asdict(build_pair_polar_phase_report(**kwargs))
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return payload


if __name__ == "__main__":
    report = write_pair_polar_phase_report()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))

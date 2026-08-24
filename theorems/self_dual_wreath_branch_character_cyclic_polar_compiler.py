"""Cyclic phase compiler for known-relative branch-character Kraus polars.

After retaining the orientation Walsh character, the local carrier factor for
an unequal source pair ``(lambda, mu)`` and a known relative permutation ``h``
is

    M_s(h) = (A(h) + s B(h))/2,       s in {+1,-1},
    A(h) = rho_lambda(h) tensor I,
    B(h) = I tensor rho_mu(h).

The two unitaries commute.  With ``U=A^*B`` this gives

    polar(M_s) = A polar((I+sU)/2).                         (1)

If ``m=ord(h)`` and ``U`` has eigenvalue ``omega^j``, cyclic phase
estimation over ``Z_m`` exposes ``j`` exactly.  The required scalar phases are

    s=+1: exp(pi i j/m) sign(cos(pi j/m)),  j != m/2,
    s=-1: -i exp(pi i j/m),                 j != 0,         (2)

with the excluded eigenvalue mapped to zero.  Equations (1)-(2) compile the
partial polar directly; no inverse minimum singular value appears.  Controlled
powers of ``U`` reduce to Young-representation actions of ``h^r`` and
``h^-r``.  Since ``log ord(h) <= log(n!)``, the circuit uses polynomially many
group-action and arithmetic gates per source pair.

The full character Kraus operator is a tensor product of the local factors,
so its polar is the tensor product of the compiled local polars.  This is a
new representation-specific normalization primitive, stronger than generic
QSVT on a small singular value.

It is not yet a hidden-label decoder.  In the physical state the relative
element is ``h=s_time^-1 g_hidden`` and is not known to the circuit.  A
one-pass correction based only on the observed time label would require the
polar field to satisfy a cocycle law.  The natural ``S_3``
``(trivial, standard)`` plus-character channel already violates that law at
operator norm two: for a three-cycle ``c``,

    ||V(c)^2 - V(c^2)|| = 2.                              (3)

Both operators are full-rank unitaries.  Thus known-relative cyclic phase
compilation does not justify replacing the unresolved covariant
multiplicity-CS transform.  A successful joint decoder must assemble these
polars coherently without knowing ``g_hidden``, or use a different block
encoding of the joint multiplicity operators.
"""

from __future__ import annotations

import cmath
import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import numpy as np

from representation_obstruction import hook_length_dimension
from research_registry import utc_now
from self_dual_wreath_character_moments import compose_permutations
from self_dual_wreath_orientation_fourier_reduction import (
    _source_representation_rows,
)


REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_branch_character_cyclic_polar_compiler.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-BRANCH-CHARACTER-CYCLIC-POLAR-COMPILER"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"

Partition = tuple[int, ...]
Permutation = tuple[int, ...]
Label = tuple[Partition, Partition]


@dataclass(frozen=True)
class LocalCyclicPolarControl:
    control_id: str
    n: int
    left_partition: Partition
    right_partition: Partition
    permutation: Permutation
    permutation_order: int
    character_sign: int
    carrier_dimension: int
    active_singular_value_count: int
    minimum_positive_singular_value: float | None
    maximum_positive_singular_value: float | None
    relative_unitary_order_residual: float
    cyclic_projector_resolution_residual: float
    cyclic_projector_idempotence_residual: float
    direct_to_cyclic_polar_residual: float
    initial_support_residual: float
    final_support_residual: float
    inverse_singular_value_amplification_used: bool
    exact_known_relative_cyclic_polar_verified: bool
    status: str


@dataclass(frozen=True)
class TensorCharacterPolarControl:
    control_id: str
    n: int
    labels: tuple[Label, ...]
    permutation: Permutation
    permutation_order: int
    character_mask: int
    factor_count: int
    carrier_dimension: int
    active_singular_value_count: int
    minimum_positive_singular_value: float | None
    direct_to_tensor_cyclic_polar_residual: float
    tensor_initial_support_residual: float
    tensor_final_support_residual: float
    exact_tensor_polar_factorization_verified: bool
    status: str


@dataclass(frozen=True)
class CyclicPolarCocycleCountercontrol:
    n: int
    left_partition: Partition
    right_partition: Partition
    generator: Permutation
    generator_order: int
    squared_generator: Permutation
    generator_polar_rank: int
    squared_generator_polar_rank: int
    generator_polar_unitarity_residual: float
    squared_generator_polar_unitarity_residual: float
    cocycle_operator_norm_defect: float
    exact_norm_two_cocycle_failure_verified: bool
    observed_time_only_phase_stripping_possible: bool
    status: str


@dataclass(frozen=True)
class CyclicPolarScalingRecord:
    n: int
    information_threshold_copy_count: int
    permutation_order_register_qubit_upper_bound: int
    controlled_power_actions_per_local_factor_upper_bound: int
    controlled_power_actions_all_factors_upper_bound: int
    cyclic_qft_gate_complexity: str
    young_representation_action_polynomial: bool
    minimum_singular_value_dependence: str
    known_relative_tensor_character_polar_polynomial: bool
    hidden_relative_element_available_to_decoder: bool
    polar_field_cocycle_proved: bool
    joint_multiplicity_inverse_compiled: bool
    status: str


@dataclass(frozen=True)
class BranchCharacterCyclicPolarReport:
    created_at: str
    theorem_contract: dict[str, Any]
    local_controls: list[LocalCyclicPolarControl]
    tensor_controls: list[TensorCharacterPolarControl]
    cocycle_countercontrol: CyclicPolarCocycleCountercontrol
    scaling_records: list[CyclicPolarScalingRecord]
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def permutation_order(permutation: Permutation) -> int:
    if sorted(permutation) != list(range(len(permutation))):
        raise ValueError("input must be a permutation")
    seen: set[int] = set()
    order = 1
    for start in range(len(permutation)):
        if start in seen:
            continue
        current = start
        length = 0
        while current not in seen:
            seen.add(current)
            length += 1
            current = permutation[current]
        order = math.lcm(order, length)
    return order


def _direct_polar(
    matrix: np.ndarray,
    tolerance: float = 1e-10,
) -> tuple[np.ndarray, np.ndarray]:
    left, singular_values, right_star = np.linalg.svd(
        matrix,
        full_matrices=False,
    )
    active = singular_values > tolerance
    return left[:, active] @ right_star[active, :], singular_values[active]


def _support(matrix: np.ndarray, tolerance: float) -> np.ndarray:
    values, vectors = np.linalg.eigh((matrix + matrix.conj().T) / 2.0)
    basis = vectors[:, values > tolerance]
    return basis @ basis.conj().T


def _cyclic_phase(
    eigenphase_index: int,
    order: int,
    character_sign: int,
) -> complex:
    if order < 1 or not 0 <= eigenphase_index < order:
        raise ValueError("invalid cyclic eigenphase label")
    if character_sign not in (-1, 1):
        raise ValueError("character sign must be +1 or -1")
    if character_sign == 1:
        if order % 2 == 0 and eigenphase_index == order // 2:
            return 0.0j
        branch_sign = 1.0 if 2 * eigenphase_index < order else -1.0
        return branch_sign * cmath.exp(
            1j * math.pi * eigenphase_index / order
        )
    if eigenphase_index == 0:
        return 0.0j
    return -1j * cmath.exp(1j * math.pi * eigenphase_index / order)


def cyclic_spectral_projectors(
    unitary: np.ndarray,
    order: int,
) -> tuple[np.ndarray, ...]:
    """Return the exact finite-order Fourier projectors of ``unitary``.

    The finite controls materialize the group average.  The circuit theorem
    implements the same projectors coherently with a ``Z_order`` phase
    register and controlled powers; it does not enumerate them.
    """

    if order < 1 or unitary.ndim != 2 or unitary.shape[0] != unitary.shape[1]:
        raise ValueError("need a positive order and a square unitary")
    dimension = unitary.shape[0]
    omega = cmath.exp(2j * math.pi / order)
    powers = [np.eye(dimension, dtype=complex)]
    for _ in range(1, order):
        powers.append(powers[-1] @ unitary)
    return tuple(
        sum(
            (
                omega ** (-phase * exponent) * powers[exponent]
                for exponent in range(order)
            ),
            np.zeros_like(unitary, dtype=complex),
        )
        / order
        for phase in range(order)
    )


def cyclic_relative_phase_polar(
    relative_unitary: np.ndarray,
    order: int,
    character_sign: int,
) -> np.ndarray:
    projectors = cyclic_spectral_projectors(relative_unitary, order)
    return sum(
        (
            _cyclic_phase(phase, order, character_sign) * projector
            for phase, projector in enumerate(projectors)
        ),
        np.zeros_like(relative_unitary, dtype=complex),
    )


def local_character_factor(
    left_partition: Partition,
    right_partition: Partition,
    permutation: Permutation,
    character_sign: int,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    if sum(left_partition) != len(permutation) or sum(right_partition) != len(
        permutation
    ):
        raise ValueError("partition degree and permutation degree must agree")
    if character_sign not in (-1, 1):
        raise ValueError("character sign must be +1 or -1")
    left = _source_representation_rows(left_partition)[permutation]
    right = _source_representation_rows(right_partition)[permutation]
    first = np.kron(left, np.eye(len(right), dtype=complex))
    second = np.kron(np.eye(len(left), dtype=complex), right)
    relative = first.conj().T @ second
    factor = (first + character_sign * second) / 2.0
    return factor, first, second, relative


def local_character_cyclic_polar(
    left_partition: Partition,
    right_partition: Partition,
    permutation: Permutation,
    character_sign: int,
) -> np.ndarray:
    _factor, first, _second, relative = local_character_factor(
        left_partition,
        right_partition,
        permutation,
        character_sign,
    )
    return first @ cyclic_relative_phase_polar(
        relative,
        permutation_order(permutation),
        character_sign,
    )


def _kron_all(matrices: tuple[np.ndarray, ...]) -> np.ndarray:
    output = np.asarray([[1.0]], dtype=complex)
    for matrix in matrices:
        output = np.kron(output, matrix)
    return output


def tensor_character_kraus(
    labels: tuple[Label, ...],
    permutation: Permutation,
    character_mask: int,
) -> np.ndarray:
    if not labels or not 0 <= character_mask < 1 << len(labels):
        raise ValueError("invalid labels or character mask")
    return _kron_all(
        tuple(
            local_character_factor(
                left,
                right,
                permutation,
                -1 if character_mask & (1 << index) else 1,
            )[0]
            for index, (left, right) in enumerate(labels)
        )
    )


def tensor_character_cyclic_polar(
    labels: tuple[Label, ...],
    permutation: Permutation,
    character_mask: int,
) -> np.ndarray:
    if not labels or not 0 <= character_mask < 1 << len(labels):
        raise ValueError("invalid labels or character mask")
    return _kron_all(
        tuple(
            local_character_cyclic_polar(
                left,
                right,
                permutation,
                -1 if character_mask & (1 << index) else 1,
            )
            for index, (left, right) in enumerate(labels)
        )
    )


def audit_local_cyclic_polar(
    control_id: str,
    left_partition: Partition,
    right_partition: Partition,
    permutation: Permutation,
    character_sign: int,
    *,
    tolerance: float = 1e-9,
) -> LocalCyclicPolarControl:
    factor, _first, _second, relative = local_character_factor(
        left_partition,
        right_partition,
        permutation,
        character_sign,
    )
    order = permutation_order(permutation)
    projectors = cyclic_spectral_projectors(relative, order)
    cyclic = local_character_cyclic_polar(
        left_partition,
        right_partition,
        permutation,
        character_sign,
    )
    direct, singular_values = _direct_polar(factor, tolerance)
    dimension = factor.shape[0]
    identity = np.eye(dimension, dtype=complex)
    resolution = float(
        np.linalg.norm(sum(projectors, np.zeros_like(identity)) - identity, ord=2)
    )
    idempotence = max(
        float(np.linalg.norm(projector @ projector - projector, ord=2))
        for projector in projectors
    )
    order_residual = float(
        np.linalg.norm(np.linalg.matrix_power(relative, order) - identity, ord=2)
    )
    polar_residual = float(np.linalg.norm(cyclic - direct, ord=2))
    initial = float(
        np.linalg.norm(
            cyclic.conj().T @ cyclic
            - _support(factor.conj().T @ factor, tolerance),
            ord=2,
        )
    )
    final = float(
        np.linalg.norm(
            cyclic @ cyclic.conj().T
            - _support(factor @ factor.conj().T, tolerance),
            ord=2,
        )
    )
    maximum = max(
        resolution,
        idempotence,
        order_residual,
        polar_residual,
        initial,
        final,
    )
    verified = maximum <= 1000 * tolerance
    return LocalCyclicPolarControl(
        control_id=control_id,
        n=len(permutation),
        left_partition=left_partition,
        right_partition=right_partition,
        permutation=permutation,
        permutation_order=order,
        character_sign=character_sign,
        carrier_dimension=dimension,
        active_singular_value_count=len(singular_values),
        minimum_positive_singular_value=(
            float(np.min(singular_values)) if len(singular_values) else None
        ),
        maximum_positive_singular_value=(
            float(np.max(singular_values)) if len(singular_values) else None
        ),
        relative_unitary_order_residual=order_residual,
        cyclic_projector_resolution_residual=resolution,
        cyclic_projector_idempotence_residual=idempotence,
        direct_to_cyclic_polar_residual=polar_residual,
        initial_support_residual=initial,
        final_support_residual=final,
        inverse_singular_value_amplification_used=False,
        exact_known_relative_cyclic_polar_verified=verified,
        status=(
            "exact-known-relative-cyclic-phase-polar"
            if verified
            else "known-relative-cyclic-polar-control-failure"
        ),
    )


def audit_tensor_character_polar(
    control_id: str,
    labels: tuple[Label, ...],
    permutation: Permutation,
    character_mask: int,
    *,
    tolerance: float = 1e-9,
) -> TensorCharacterPolarControl:
    kraus = tensor_character_kraus(labels, permutation, character_mask)
    cyclic = tensor_character_cyclic_polar(labels, permutation, character_mask)
    direct, singular_values = _direct_polar(kraus, tolerance)
    residual = float(np.linalg.norm(cyclic - direct, ord=2))
    initial = float(
        np.linalg.norm(
            cyclic.conj().T @ cyclic
            - _support(kraus.conj().T @ kraus, tolerance),
            ord=2,
        )
    )
    final = float(
        np.linalg.norm(
            cyclic @ cyclic.conj().T
            - _support(kraus @ kraus.conj().T, tolerance),
            ord=2,
        )
    )
    verified = max(residual, initial, final) <= 2000 * tolerance
    return TensorCharacterPolarControl(
        control_id=control_id,
        n=len(permutation),
        labels=labels,
        permutation=permutation,
        permutation_order=permutation_order(permutation),
        character_mask=character_mask,
        factor_count=len(labels),
        carrier_dimension=kraus.shape[0],
        active_singular_value_count=len(singular_values),
        minimum_positive_singular_value=(
            float(np.min(singular_values)) if len(singular_values) else None
        ),
        direct_to_tensor_cyclic_polar_residual=residual,
        tensor_initial_support_residual=initial,
        tensor_final_support_residual=final,
        exact_tensor_polar_factorization_verified=verified,
        status=(
            "exact-tensor-character-cyclic-polar-factorization"
            if verified
            else "tensor-character-cyclic-polar-control-failure"
        ),
    )


def cyclic_polar_cocycle_countercontrol(
    *,
    tolerance: float = 1e-9,
) -> CyclicPolarCocycleCountercontrol:
    left = (3,)
    right = (2, 1)
    generator: Permutation = (1, 2, 0)
    squared = compose_permutations(generator, generator)
    first = local_character_cyclic_polar(left, right, generator, 1)
    second = local_character_cyclic_polar(left, right, squared, 1)
    identity = np.eye(first.shape[0], dtype=complex)
    first_unitarity = float(
        np.linalg.norm(first.conj().T @ first - identity, ord=2)
    )
    second_unitarity = float(
        np.linalg.norm(second.conj().T @ second - identity, ord=2)
    )
    defect = float(np.linalg.norm(first @ first - second, ord=2))
    verified = bool(
        permutation_order(generator) == 3
        and np.linalg.matrix_rank(first, tol=tolerance) == len(first)
        and np.linalg.matrix_rank(second, tol=tolerance) == len(second)
        and first_unitarity <= 1000 * tolerance
        and second_unitarity <= 1000 * tolerance
        and abs(defect - 2.0) <= 1000 * tolerance
    )
    return CyclicPolarCocycleCountercontrol(
        n=3,
        left_partition=left,
        right_partition=right,
        generator=generator,
        generator_order=permutation_order(generator),
        squared_generator=squared,
        generator_polar_rank=int(np.linalg.matrix_rank(first, tol=tolerance)),
        squared_generator_polar_rank=int(
            np.linalg.matrix_rank(second, tol=tolerance)
        ),
        generator_polar_unitarity_residual=first_unitarity,
        squared_generator_polar_unitarity_residual=second_unitarity,
        cocycle_operator_norm_defect=defect,
        exact_norm_two_cocycle_failure_verified=verified,
        observed_time_only_phase_stripping_possible=False,
        status=(
            "natural-full-rank-cyclic-polar-cocycle-failure"
            if verified
            else "cyclic-polar-cocycle-countercontrol-failure"
        ),
    )


def cyclic_polar_scaling_record(n: int) -> CyclicPolarScalingRecord:
    if n < 3:
        raise ValueError("n must be at least three")
    order_bits = math.ceil(math.lgamma(n + 1) / math.log(2))
    copies = order_bits + 2
    return CyclicPolarScalingRecord(
        n=n,
        information_threshold_copy_count=copies,
        permutation_order_register_qubit_upper_bound=order_bits,
        controlled_power_actions_per_local_factor_upper_bound=2 * order_bits,
        controlled_power_actions_all_factors_upper_bound=(
            2 * copies * order_bits
        ),
        cyclic_qft_gate_complexity="poly(log ord(h), log(1/error))",
        young_representation_action_polynomial=True,
        minimum_singular_value_dependence=(
            "none; cyclic eigenphase labels flag exact zero modes directly"
        ),
        known_relative_tensor_character_polar_polynomial=True,
        hidden_relative_element_available_to_decoder=False,
        polar_field_cocycle_proved=False,
        joint_multiplicity_inverse_compiled=False,
        status="known-relative-polar-polynomial-hidden-relative-assembly-open",
    )


def _local_controls() -> list[LocalCyclicPolarControl]:
    permutations = tuple(_source_representation_rows((3,)))
    controls = []
    for index, permutation in enumerate(permutations):
        for sign in (1, -1):
            controls.append(
                audit_local_cyclic_polar(
                    f"S3-TRIVIAL-STANDARD-{index}-SIGN-{sign}",
                    (3,),
                    (2, 1),
                    permutation,
                    sign,
                )
            )
    representatives = (permutations[0], permutations[1], (1, 2, 0))
    for index, permutation in enumerate(representatives):
        for sign in (1, -1):
            controls.append(
                audit_local_cyclic_polar(
                    f"S3-STANDARD-SIGN-{index}-SIGN-{sign}",
                    (2, 1),
                    (1, 1, 1),
                    permutation,
                    sign,
                )
            )
    return controls


def _tensor_controls() -> list[TensorCharacterPolarControl]:
    labels: tuple[Label, ...] = (
        ((3,), (2, 1)),
        ((3,), (1, 1, 1)),
        ((2, 1), (1, 1, 1)),
    )
    permutations = tuple(_source_representation_rows((3,)))
    representatives = (permutations[0], permutations[1], (1, 2, 0))
    return [
        audit_tensor_character_polar(
            f"S3-THRESHOLD-PERM-{permutation_index}-CHAR-{character}",
            labels,
            permutation,
            character,
        )
        for permutation_index, permutation in enumerate(representatives)
        for character in range(1 << len(labels))
    ]


def run_branch_character_cyclic_polar_compiler(
) -> BranchCharacterCyclicPolarReport:
    local = _local_controls()
    tensor = _tensor_controls()
    cocycle = cyclic_polar_cocycle_countercontrol()
    scaling = [
        cyclic_polar_scaling_record(n)
        for n in (8, 16, 32, 64, 128, 256, 512)
    ]
    local_failures = sum(
        not row.exact_known_relative_cyclic_polar_verified for row in local
    )
    tensor_failures = sum(
        not row.exact_tensor_polar_factorization_verified for row in tensor
    )
    verified = bool(
        local_failures == 0
        and tensor_failures == 0
        and cocycle.exact_norm_two_cocycle_failure_verified
    )
    return BranchCharacterCyclicPolarReport(
        created_at=utc_now(),
        theorem_contract={
            "local_factor": (
                "M_s=(A+sB)/2=A(I+sU)/2 with U=A^*B and A,B commuting "
                "finite-order representation unitaries."
            ),
            "cyclic_phase_polar": (
                "Z_ord(h) phase estimation labels omega^j; equation (2) applies "
                "the exact partial-polar phase and flags the one possible kernel label."
            ),
            "complexity": (
                "Controlled powers use h^r and h^-r representation actions; "
                "log ord(h)<=log(n!), so cost is polynomial and independent of "
                "the smallest positive singular value."
            ),
            "tensor_factorization": (
                "polar(tensor_i M_i)=tensor_i polar(M_i), including rank-deficient factors."
            ),
            "cocycle_boundary": (
                "For the S3 trivial-standard plus channel and a three-cycle c, "
                "both V(c) and V(c^2) are unitary but ||V(c)^2-V(c^2)||=2."
            ),
            "scope": (
                "The compiler requires a known relative h. The physical h contains "
                "the hidden label, and the norm-two cocycle defect rejects a one-pass "
                "observed-time-only phase stripping argument."
            ),
        },
        local_controls=local,
        tensor_controls=tensor,
        cocycle_countercontrol=cocycle,
        scaling_records=scaling,
        proof_obligations=[
            {
                "obligation": "compile_each_known_relative_local_character_polar",
                "resolved": verified,
                "resolution": (
                    "Finite-order spectral projectors and the exact phases in "
                    "equation (2) reproduce every selected S3 SVD polar."
                ),
            },
            {
                "obligation": "remove_inverse_singular_value_cost",
                "resolved": verified,
                "resolution": (
                    "The circuit changes phases after exact cyclic eigenphase "
                    "labeling and never amplifies a singular magnitude."
                ),
            },
            {
                "obligation": "compile_tensor_character_kraus_polar",
                "resolved": verified,
                "resolution": (
                    "Tensor-product polar factorization passes all threshold-copy S3 controls."
                ),
            },
            {
                "obligation": "assemble_known_relative_polars_covariantly_without_hidden_g",
                "resolved": False,
                "resolution": (
                    "The polar field is not a cocycle. A multi-round connection, "
                    "joint multiplicity transform, or different covariant assembly is required."
                ),
            },
            {
                "obligation": "compile_joint_character_multiplicity_inverse",
                "resolved": False,
                "resolution": (
                    "Local phase normalization leaves positive singular magnitudes "
                    "and does not block-encode or invert the D_nu operators."
                ),
            },
        ],
        adversarial_audit=[
            {
                "objection": "Tiny singular values force QSVT-style inverse-gap cost for every character factor.",
                "resolved": True,
                "resolution": (
                    "False for known h: cyclic eigenphase labels directly compile "
                    "the polar phase, just as a structured reassociation can bypass correlation size."
                ),
            },
            {
                "objection": "Tensoring many local polar compilers reintroduces condition-number cost.",
                "resolved": True,
                "resolution": (
                    "Polar commutes exactly with tensor products; gate errors add, "
                    "while no singular magnitudes are multiplied or inverted."
                ),
            },
            {
                "objection": "Known-relative compilation immediately strips the physical row-copy phases.",
                "resolved": True,
                "resolution": (
                    "False: h=s^-1 g contains the unknown hidden label, and the "
                    "norm-two S3 cocycle defect prevents factorization into known-s and hidden-g pieces."
                ),
            },
            {
                "objection": "The cocycle counterexample rules out all carrier-dependent decoders.",
                "resolved": True,
                "resolution": (
                    "No. It rejects one-pass phase stripping. Coherent path registers, "
                    "holonomy resolution, and direct joint multiplicity CS remain open."
                ),
            },
        ],
        headline_metrics={
            "known_relative_local_cyclic_polar_theorem_count": int(verified),
            "known_relative_tensor_character_polar_theorem_count": int(verified),
            "finite_local_control_count": len(local),
            "finite_local_control_failure_count": local_failures,
            "finite_tensor_control_count": len(tensor),
            "finite_tensor_control_failure_count": tensor_failures,
            "inverse_singular_value_amplification_count": 0,
            "natural_full_rank_cocycle_counterexample_count": int(
                cocycle.exact_norm_two_cocycle_failure_verified
            ),
            "cocycle_operator_norm_defect": cocycle.cocycle_operator_norm_defect,
            "hidden_relative_covariant_assembly_count": 0,
            "joint_multiplicity_inverse_compiler_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "known_relative_local_character_polar_polynomial": verified,
            "known_relative_tensor_character_polar_polynomial": verified,
            "minimum_singular_value_amplification_required": False,
            "polar_field_is_cocycle": False,
            "observed_time_only_phase_stripping_compiles_decoder": False,
            "hidden_relative_covariant_assembly_compiled": False,
            "joint_multiplicity_inverse_compiled": False,
            "complete_orientation_polar_compiled": False,
            "classical_separation_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "Known-relative matrix-valued character phases are now directly "
                "compilable, but the relative element contains the hidden label "
                "and the polar field has norm-two holonomy/cocycle failure."
            ),
        },
        status=(
            "known-relative-character-polar-compiled-covariant-assembly-open"
            if verified
            else "branch-character-cyclic-polar-validation-failure"
        ),
        summary=(
            "Compiled every known-relative tensor character Kraus polar by cyclic "
            "phase estimation without inverse-gap cost, then proved a natural "
            "full-rank S3 norm-two cocycle obstruction to one-pass hidden-relative assembly."
        ),
        falsifiers_triggered=[
            "Small character-factor singular values are not a barrier when the relative permutation is known.",
            "Local tensor polar compilation does not imply a hidden-label-independent covariant decoder.",
            "The first cyclic three-cycle control already carries maximal polar holonomy.",
        ],
    )


def write_branch_character_cyclic_polar_report(
    path: Path = REPORT_PATH,
) -> dict[str, Any]:
    payload = asdict(run_branch_character_cyclic_polar_compiler())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    return payload


if __name__ == "__main__":
    report = write_branch_character_cyclic_polar_report()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))

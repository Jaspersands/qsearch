"""Positive Young-star decomposition of the point PGM relative collision.

Let ``omega=T_H(tau)`` be the point-stabilizer quotient seed,
``B=T_G(tau)`` its full-group average, and ``Delta=omega-B``.  The exact
uniform-ensemble PGM identity makes

    Xi = Tr(B^-1/2 Delta B^-1/2 Delta)                    (1)

the relevant point signal: ``p_PGM=1/n+Xi/n`` by covariance.

In the Young basis for ``H=S_(n-1)``,

    omega = direct_sum_alpha I_(d_alpha) tensor Z^H_alpha,
    B     = direct_sum_alpha I_(d_alpha) tensor Z^G_alpha.

Consequently (1) has the exact positive decomposition

    Xi = sum_alpha d_alpha
      ||(Z^G_alpha)^-1/4
        (Z^H_alpha-Z^G_alpha)
        (Z^G_alpha)^-1/4||_F^2.                          (2)

The full-twirl child operator is parent diagonal,

    Z^G_alpha = direct_sum_(nu covers alpha) D_nu/d_nu.

Splitting the centered operator into parent blocks therefore refines (2) to

    Xi = sum_(alpha,nu,mu) d_alpha
      ||(D_nu/d_nu)^-1/4 Delta_(alpha;nu,mu)
        (D_mu/d_mu)^-1/4||_F^2.                          (3)

Every term in (3) is nonnegative.  This is the relative analogue of the
ambient child-energy theorem and prevents cancellation-prone scalar probes.

The exact orientation projection-Gram identity gives

    D_nu/d_nu = (q dim(C))^-1
      [I_(d_nu) tensor W H_nu W^*],       q=2^k.          (4)

Thus multiplying both ``Z^H_alpha`` and ``Z^G_alpha`` by ``q dim(C)`` leaves
the PGM child effect

    n^-1 (Z^G_alpha)^-1/2 Z^H_alpha (Z^G_alpha)^-1/2

unchanged.  The density normalization cancels exactly.  The remaining hard
problem is the signal-weighted relative spectrum of the dimensionless
orientation kernels, not generic amplification of a ``1/(q dim(C))`` scalar.

Equations (1)--(4) do not bound the natural critical ``Xi`` asymptotically and
do not compile the child-star square roots.  They identify the exact positive
channels on which either theorem must be proved.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import numpy as np

from representation_obstruction import hook_length_dimension
from research_registry import utc_now
from self_dual_wreath_joint_character_correlation_decoder import (
    _pretty_good_success,
    schur_multiplicity_operators,
)
from self_dual_wreath_orientation_fourier_reduction import _w4_collision_free_labels
from self_dual_wreath_point_child_star_energy import (
    _child_star_layout,
    _parent_slices,
)
from self_dual_wreath_point_stabilizer_quotient import point_quotient_states
from self_dual_wreath_point_young_star_naimark import (
    _fourier_child_star_factorization,
)


REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_point_child_star_relative_collision.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-POINT-CHILD-STAR-RELATIVE-COLLISION"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"

Partition = tuple[int, ...]
Label = tuple[Partition, Partition]


@dataclass(frozen=True)
class ChildStarRelativeCollisionRecord:
    child: Partition
    child_irrep_dimension: int
    parent_partitions: tuple[Partition, ...]
    child_star_dimension: int
    relative_collision: float
    parent_diagonal_relative_collision: float
    parent_offdiagonal_relative_collision: float
    offdiagonal_relative_fraction: float
    active_parent_pair_count: int
    active_offdiagonal_parent_pair_count: int
    strongest_parent_pair: tuple[Partition, Partition]
    strongest_parent_pair_relative_collision: float


@dataclass(frozen=True)
class PointChildStarRelativeCollisionControl:
    control_id: str
    n: int
    labels: tuple[Label, ...]
    copy_count: int
    orientation_count: int
    carrier_dimension: int
    register_dimension: int
    direct_relative_collision: float
    decomposed_relative_collision: float
    parent_diagonal_relative_collision: float
    parent_offdiagonal_relative_collision: float
    parent_offdiagonal_relative_fraction: float
    direct_pgm_success: float
    relative_collision_predicted_pgm_success: float
    maximum_child_factorization_residual: float
    maximum_parent_diagonal_average_residual: float
    relative_collision_decomposition_residual: float
    maximum_rescaled_effect_cancellation_residual: float
    strongest_child: Partition
    strongest_parent_pair: tuple[Partition, Partition]
    strongest_parent_pair_relative_collision: float
    child_records: tuple[ChildStarRelativeCollisionRecord, ...]
    exact_child_star_relative_collision_verified: bool
    status: str


@dataclass(frozen=True)
class PointChildStarRelativeCollisionScalingRecord:
    n: int
    critical_copy_count: int
    orientation_log2_width: int
    young_child_count: int
    maximum_parent_count_per_child_upper_bound: float
    exact_positive_relative_channel_formula_available: bool
    common_density_normalization_cancels_from_pgm_effect: bool
    natural_critical_relative_collision_lower_bound_proved: bool
    natural_critical_relative_collision_upper_bound_proved: bool
    dimensionless_orientation_kernel_transform_compiled: bool
    harmonic_point_measurement_compiled: bool
    status: str


@dataclass(frozen=True)
class PointChildStarRelativeCollisionTheorem:
    pgm_signal: str
    child_star_decomposition: str
    parent_pair_decomposition: str
    orientation_gram_normalization: str
    scalar_cancellation: str
    asymptotic_boundary: str
    theorem_verified: bool
    status: str


@dataclass(frozen=True)
class PointChildStarRelativeCollisionReport:
    created_at: str
    theorem_contract: dict[str, Any]
    theorem: PointChildStarRelativeCollisionTheorem
    finite_controls: list[PointChildStarRelativeCollisionControl]
    scaling_records: list[PointChildStarRelativeCollisionScalingRecord]
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _psd_power(
    matrix: np.ndarray,
    exponent: float,
    tolerance: float,
) -> np.ndarray:
    hermitian = (matrix + matrix.conj().T) / 2
    eigenvalues, eigenvectors = np.linalg.eigh(hermitian)
    if eigenvalues[0] < -100 * tolerance:
        raise ValueError("matrix must be positive semidefinite")
    powered = np.zeros_like(eigenvalues)
    positive = eigenvalues > tolerance
    powered[positive] = eigenvalues[positive] ** exponent
    return (eigenvectors * powered) @ eigenvectors.conj().T


def _partition_number(n: int) -> int:
    if n < 0:
        raise ValueError("n must be nonnegative")
    counts = [0] * (n + 1)
    counts[0] = 1
    for part in range(1, n + 1):
        for total in range(part, n + 1):
            counts[total] += counts[total - part]
    return counts[n]


def relative_collision(
    average: np.ndarray,
    centered: np.ndarray,
    *,
    tolerance: float = 1e-10,
) -> float:
    inverse_root = _psd_power(average, -0.5, tolerance)
    value = np.trace(inverse_root @ centered @ inverse_root @ centered)
    return float(value.real)


def audit_point_child_star_relative_collision(
    n: int,
    labels: tuple[Label, ...],
    *,
    control_id: str,
    tolerance: float = 1e-9,
) -> PointChildStarRelativeCollisionControl:
    states = point_quotient_states(labels, point=n - 1)
    seed = states[n - 1]
    average = sum(states) / n
    centered = seed - average
    direct = relative_collision(average, centered, tolerance=tolerance)
    pgm_success, _, _ = _pretty_good_success(states, tolerance)
    predicted_success = 1.0 / n + direct / n

    character_count = 1 << len(labels)
    carrier_dimension = math.prod(
        hook_length_dimension(left) * hook_length_dimension(right)
        for left, right in labels
    )
    seed_residual, seed_operators, _ = _fourier_child_star_factorization(
        seed,
        n,
        character_count,
        tolerance=tolerance,
    )
    average_residual, average_operators, _ = _fourier_child_star_factorization(
        average,
        n,
        character_count,
        tolerance=tolerance,
    )
    centered_residual, centered_operators, _ = _fourier_child_star_factorization(
        centered,
        n,
        character_count,
        tolerance=tolerance,
    )
    layout = _child_star_layout(n, character_count)
    multiplicity, schur_residual = schur_multiplicity_operators(
        n,
        character_count,
        average,
        tolerance,
    )

    maximum_parent_residual = 0.0
    maximum_scale_residual = 0.0
    records = []
    strongest: tuple[float, Partition, tuple[Partition, Partition]] = (
        0.0,
        (),
        ((), ()),
    )
    for child, delta_operator in centered_operators.items():
        parents, _, _ = layout[child]
        child_dimension = hook_length_dimension(child)
        parent_slices = _parent_slices(parents, character_count)
        average_operator = average_operators[child]
        seed_operator = seed_operators[child]
        full_formula = np.zeros_like(average_operator)
        for parent in parents:
            section = parent_slices[parent]
            full_formula[section, section] = (
                multiplicity[parent] / hook_length_dimension(parent)
            )
        maximum_parent_residual = max(
            maximum_parent_residual,
            float(np.linalg.norm(average_operator - full_formula)),
        )

        inverse_quarter = _psd_power(average_operator, -0.25, tolerance)
        whitened = inverse_quarter @ delta_operator @ inverse_quarter
        child_collision = child_dimension * float(
            np.vdot(whitened, whitened).real
        )
        diagonal = 0.0
        offdiagonal = 0.0
        active = 0
        active_offdiagonal = 0
        local_strongest = (0.0, (parents[0], parents[0]))
        for left in parents:
            for right in parents:
                block = whitened[
                    parent_slices[left],
                    parent_slices[right],
                ]
                contribution = child_dimension * float(np.vdot(block, block).real)
                if contribution > tolerance:
                    active += 1
                    active_offdiagonal += left != right
                if left == right:
                    diagonal += contribution
                else:
                    offdiagonal += contribution
                if contribution > local_strongest[0]:
                    local_strongest = contribution, (left, right)
                if contribution > strongest[0]:
                    strongest = contribution, child, (left, right)

        scale = character_count * carrier_dimension
        inverse_half = _psd_power(average_operator, -0.5, tolerance)
        original_effect = inverse_half @ seed_operator @ inverse_half / n
        scaled_average = scale * average_operator
        scaled_seed = scale * seed_operator
        scaled_inverse_half = _psd_power(scaled_average, -0.5, tolerance)
        scaled_effect = scaled_inverse_half @ scaled_seed @ scaled_inverse_half / n
        maximum_scale_residual = max(
            maximum_scale_residual,
            float(np.linalg.norm(original_effect - scaled_effect)),
        )
        records.append(
            ChildStarRelativeCollisionRecord(
                child=child,
                child_irrep_dimension=child_dimension,
                parent_partitions=parents,
                child_star_dimension=len(delta_operator),
                relative_collision=child_collision,
                parent_diagonal_relative_collision=diagonal,
                parent_offdiagonal_relative_collision=offdiagonal,
                offdiagonal_relative_fraction=(
                    offdiagonal / child_collision
                    if child_collision > tolerance
                    else 0.0
                ),
                active_parent_pair_count=active,
                active_offdiagonal_parent_pair_count=active_offdiagonal,
                strongest_parent_pair=local_strongest[1],
                strongest_parent_pair_relative_collision=local_strongest[0],
            )
        )

    decomposed = sum(row.relative_collision for row in records)
    diagonal_total = sum(
        row.parent_diagonal_relative_collision for row in records
    )
    offdiagonal_total = sum(
        row.parent_offdiagonal_relative_collision for row in records
    )
    decomposition_residual = max(
        abs(direct - decomposed),
        abs(decomposed - diagonal_total - offdiagonal_total),
        abs(pgm_success - predicted_success),
        seed_residual,
        average_residual,
        centered_residual,
        schur_residual,
    )
    verified = bool(
        direct > tolerance
        and decomposition_residual <= 100 * tolerance
        and maximum_parent_residual <= 100 * tolerance
        and maximum_scale_residual <= 100 * tolerance
        and strongest[0] > tolerance
    )
    return PointChildStarRelativeCollisionControl(
        control_id=control_id,
        n=n,
        labels=labels,
        copy_count=len(labels),
        orientation_count=character_count,
        carrier_dimension=carrier_dimension,
        register_dimension=len(seed),
        direct_relative_collision=direct,
        decomposed_relative_collision=decomposed,
        parent_diagonal_relative_collision=diagonal_total,
        parent_offdiagonal_relative_collision=offdiagonal_total,
        parent_offdiagonal_relative_fraction=offdiagonal_total / decomposed,
        direct_pgm_success=pgm_success,
        relative_collision_predicted_pgm_success=predicted_success,
        maximum_child_factorization_residual=max(
            seed_residual,
            average_residual,
            centered_residual,
            schur_residual,
        ),
        maximum_parent_diagonal_average_residual=maximum_parent_residual,
        relative_collision_decomposition_residual=decomposition_residual,
        maximum_rescaled_effect_cancellation_residual=maximum_scale_residual,
        strongest_child=strongest[1],
        strongest_parent_pair=strongest[2],
        strongest_parent_pair_relative_collision=strongest[0],
        child_records=tuple(records),
        exact_child_star_relative_collision_verified=verified,
        status=(
            "exact-positive-child-star-relative-collision-decomposition"
            if verified
            else "child-star-relative-collision-validation-failure"
        ),
    )


def point_child_star_relative_collision_scaling_record(
    n: int,
) -> PointChildStarRelativeCollisionScalingRecord:
    if n < 3:
        raise ValueError("n must be at least three")
    copies = math.ceil(2.0 * math.lgamma(n + 1) / math.log(2.0))
    return PointChildStarRelativeCollisionScalingRecord(
        n=n,
        critical_copy_count=copies,
        orientation_log2_width=copies,
        young_child_count=_partition_number(n - 1),
        maximum_parent_count_per_child_upper_bound=math.sqrt(2 * n) + 1,
        exact_positive_relative_channel_formula_available=True,
        common_density_normalization_cancels_from_pgm_effect=True,
        natural_critical_relative_collision_lower_bound_proved=False,
        natural_critical_relative_collision_upper_bound_proved=False,
        dimensionless_orientation_kernel_transform_compiled=False,
        harmonic_point_measurement_compiled=False,
        status="relative-child-channels-exact-natural-critical-asymptotics-open",
    )


def build_point_child_star_relative_collision_report(
) -> PointChildStarRelativeCollisionReport:
    controls = [
        audit_point_child_star_relative_collision(
            3,
            (
                ((3,), (2, 1)),
                ((3,), (1, 1, 1)),
                ((2, 1), (1, 1, 1)),
            ),
            control_id="W3-INFORMATION-THRESHOLD",
        ),
        audit_point_child_star_relative_collision(
            4,
            _w4_collision_free_labels()[0],
            control_id="W4-COLLISION-FREE-PAIR",
        ),
        audit_point_child_star_relative_collision(
            4,
            (((4,), (2, 2)), ((3, 1), (1, 1, 1, 1))),
            control_id="W4-COLLECTIVE-PARENT-COHERENCE",
        ),
    ]
    scaling = [
        point_child_star_relative_collision_scaling_record(n)
        for n in (8, 16, 32, 64, 128, 256, 512)
    ]
    failures = sum(
        not row.exact_child_star_relative_collision_verified
        for row in controls
    )
    verified = failures == 0
    theorem = PointChildStarRelativeCollisionTheorem(
        pgm_signal=(
            "Xi=Tr(B^-1/2 Delta B^-1/2 Delta) and p_point_PGM=1/n+Xi/n."
        ),
        child_star_decomposition=(
            "Xi=sum_alpha d_alpha ||(Z_alpha^G)^-1/4 "
            "Delta_alpha (Z_alpha^G)^-1/4||_F^2."
        ),
        parent_pair_decomposition=(
            "Because Z_alpha^G=direct_sum_(nu covers alpha)D_nu/d_nu, Xi is "
            "the sum of nonnegative whitened (alpha,nu,mu) block energies."
        ),
        orientation_gram_normalization=(
            "D_nu/d_nu=(q dim(C))^-1[I_dnu tensor W H_nu W^*]."
        ),
        scalar_cancellation=(
            "Rescaling Z_alpha^H and Z_alpha^G by q dim(C) leaves every PGM "
            "child effect exactly unchanged."
        ),
        asymptotic_boundary=(
            "The natural critical relative-channel mass and a coherent transform "
            "for the dimensionless orientation kernels remain unproved."
        ),
        theorem_verified=verified,
        status=(
            "relative-child-star-channels-exact-critical-asymptotics-open"
            if verified
            else "child-star-relative-collision-validation-failure"
        ),
    )
    return PointChildStarRelativeCollisionReport(
        created_at=utc_now(),
        theorem_contract={
            "source": "fixed public source labels; finite exact controls",
            "point_seed": "omega=T_Stab(n)(tau), B=T_Sn(tau)",
            "measurement": "uniform point PGM",
            "relative_quantity": (
                "Tr(B^-1/2(omega-B)B^-1/2(omega-B))"
            ),
            "claim_boundary": (
                "exact positive channel decomposition, not natural c=2 asymptotics or a circuit"
            ),
        },
        theorem=theorem,
        finite_controls=controls,
        scaling_records=scaling,
        proof_obligations=[
            {
                "id": "PO-POINT-RELATIVE-CHILD-STAR-DECOMPOSITION",
                "statement": "Derive the exact positive child and parent-pair formula.",
                "resolved": verified,
            },
            {
                "id": "PO-POINT-CRITICAL-NATURAL-RELATIVE-MASS",
                "statement": (
                    "At k=ceil(2log2 n!), prove a typical natural lower or upper "
                    "bound on the sum of information-carrying relative channels."
                ),
                "resolved": False,
            },
            {
                "id": "PO-POINT-DIMENSIONLESS-ORIENTATION-KERNEL-TRANSFORM",
                "statement": (
                    "Compile or obstruct the child-star relative effect after the "
                    "q dim(C) scalar cancellation."
                ),
                "resolved": False,
            },
        ],
        adversarial_audit=[
            {
                "challenge": "Relative collision can cancel across Young channels.",
                "answer": (
                    "False. Quarter-whitening turns it into a Frobenius square, and "
                    "the parent-diagonal average refines it into nonnegative blocks."
                ),
                "resolved": True,
            },
            {
                "challenge": "The 1/(2^k dim(C)) density scalar forces factorial QSVT amplification.",
                "answer": (
                    "False for the mathematical PGM effect: simultaneous rescaling of "
                    "seed and average cancels exactly. A structured transform is still open."
                ),
                "resolved": True,
            },
            {
                "challenge": "Exact positive channels prove natural critical advantage.",
                "answer": (
                    "False. Their total and typical source mass have no all-n bound."
                ),
                "resolved": True,
            },
            {
                "challenge": "Scalar cancellation compiles the inverse square root.",
                "answer": (
                    "False. It removes one normalization objection but leaves wide, "
                    "source-dependent orientation kernels and their spectral transform."
                ),
                "resolved": True,
            },
        ],
        headline_metrics={
            "exact_relative_collision_pgm_identity_count": int(verified),
            "exact_positive_child_star_relative_decomposition_count": int(verified),
            "exact_positive_parent_pair_relative_decomposition_count": int(verified),
            "density_scalar_cancellation_theorem_count": int(verified),
            "finite_control_count": len(controls),
            "finite_control_failure_count": failures,
            "finite_active_relative_parent_pair_count": sum(
                row.active_parent_pair_count
                for control in controls
                for row in control.child_records
            ),
            "finite_active_offdiagonal_relative_parent_pair_count": sum(
                row.active_offdiagonal_parent_pair_count
                for control in controls
                for row in control.child_records
            ),
            "maximum_finite_relative_collision": max(
                row.direct_relative_collision for row in controls
            ),
            "natural_critical_relative_mass_theorem_count": 0,
            "dimensionless_kernel_transform_count": 0,
            "harmonic_point_measurement_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "point_pgm_relative_collision_identity_proved": verified,
            "positive_child_star_relative_decomposition_proved": verified,
            "positive_parent_pair_relative_decomposition_proved": verified,
            "common_density_scalar_cancels_from_pgm_effect": verified,
            "generic_factorial_scalar_amplification_is_intrinsic": False,
            "natural_critical_relative_collision_lower_bound_proved": False,
            "natural_critical_relative_collision_upper_bound_proved": False,
            "dimensionless_orientation_kernel_transform_compiled": False,
            "critical_harmonic_point_measurement_compiled": False,
            "full_hidden_permutation_decoder_constructed": False,
            "classical_separation_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The exact relative signal is now localized in positive dimensionless "
                "Young channels, but no natural all-rank mass theorem or coherent "
                "kernel transform exists."
            ),
        },
        status=theorem.status,
        summary=(
            "Converted the point PGM signal into positive whitened Young-child and "
            "parent-pair channels and proved exact cancellation of the common density "
            "normalization, leaving natural critical channel mass and kernel access open."
        ),
        falsifiers_triggered=[
            "Critical relative collision cannot be inferred from ambient child energy.",
            "The common 1/(2^k dim(C)) density scalar is not itself a PGM-effect obstruction.",
            "Positive finite relative channels do not imply typical natural critical mass.",
            "The next asymptotic target is a signal-weighted orientation-kernel theorem, not a global norm bound.",
        ],
    )


def write_point_child_star_relative_collision_report(
    path: Path = REPORT_PATH,
    **_: Any,
) -> dict[str, Any]:
    payload = asdict(build_point_child_star_relative_collision_report())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    return payload


if __name__ == "__main__":
    report = write_point_child_star_relative_collision_report()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))

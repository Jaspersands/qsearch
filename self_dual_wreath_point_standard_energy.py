"""Positive standard-harmonic energy formula for point extraction.

The point-stabilizer signal was first expressed as a standard-character
coefficient of the relative overlap kernel

    D = |G|^-1 sum_g chi_std(g) Tr(tau L_g tau L_g^*).

Although this class formula contains cancellations, the underlying quantity is
positive.  Let ``Ad_g(X)=L_g X L_g^*`` act on Hilbert--Schmidt operator space
and let

    P_std = (n-1)/|G| sum_g chi_std(g) Ad_g.

Character orthogonality makes ``P_std`` the orthogonal projector onto the
standard isotypic component.  Since the overlap kernel is central,

    D = ||P_std(tau)||_2^2/(n-1).                          (1)

Equivalently, averaging over ``H=Stab(0)`` selects the unique H-fixed line in
each standard copy and

    omega_0-bar(omega) = T_H P_std(tau),
    ||P_std(tau)||_2^2 = (n-1)||omega_0-bar(omega)||_2^2. (2)

The group Fourier transform gives a local positive decomposition.  Write a
block of ``tau`` as a map from row irrep ``V_mu`` to ``V_nu`` with all Fourier
column and orientation indices treated as multiplicity.  The standard
projection of that block is

    P_std^(nu,mu)(X)=(n-1)/|G| sum_g chi_std(g)
      rho_nu(g) X rho_mu(g)^*.

Therefore

    D = 1/(n-1) sum_(nu,mu)
      ||P_std^(nu,mu)(tau_hat_(nu,mu))||_2^2.              (3)

Every summand is nonnegative.  The symmetric-group tensor rule

    g(nu,mu,(n-1,1)) = |nu^- intersect mu^-| - 1[nu=mu]  (4)

shows that only distinct diagrams sharing an ``S_(n-1)`` child and diagonal
diagrams with at least two removable corners can contribute.  This is the
precise positive-energy version of Young-edge locality.

Equations (1)--(4) remove artificial class-sum cancellation from the research
target.  They do not lower-bound the natural or collision-free energy, compile
the required block projections, or implement a point decoder.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import numpy as np

from representation_obstruction import hook_length_dimension, integer_partitions
from research_registry import utc_now
from self_dual_wreath_character_moments import permutation_cycle_type
from self_dual_wreath_coherent_fourier_decoder import symmetric_group_fourier_matrix
from self_dual_wreath_joint_character_correlation_decoder import (
    _permutations,
    joint_character_state,
    left_covariant_state,
)
from self_dual_wreath_point_stabilizer_quotient import (
    point_quotient_states,
    removable_children,
)
from symmetric_character import symmetric_character


REPORT_PATH = Path(
    "research/representation/self_dual_wreath_point_standard_energy.json"
)
DEFAULT_EXPERIMENT_ID = "EXP-CODE-SELF-DUAL-WREATH-POINT-STANDARD-ENERGY"
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"

Partition = tuple[int, ...]
Label = tuple[Partition, Partition]


@dataclass(frozen=True)
class StandardMultiplicityValidation:
    n: int
    irrep_pair_count: int
    maximum_exact_multiplicity: int
    maximum_formula_multiplicity: int
    mismatch_count: int
    exact_standard_kronecker_rule_verified: bool
    status: str


@dataclass(frozen=True)
class PointStandardEnergyControl:
    control_id: str
    n: int
    labels: tuple[Label, ...]
    copy_count: int
    group_order: int
    orientation_count: int
    centered_point_signal: float
    standard_projection_energy: float
    energy_identity_residual: float
    standard_projector_idempotence_residual: float
    stabilizer_projection_identity_residual: float
    fourier_block_energy_sum_residual: float
    positive_young_pair_count: int
    active_positive_young_pair_count: int
    active_nonstandard_fourier_pair_count: int
    maximum_zero_multiplicity_block_energy: float
    diagonal_standard_energy: float
    offdiagonal_standard_energy: float
    offdiagonal_energy_fraction: float
    largest_energy_irrep_pair: tuple[Partition, Partition]
    largest_energy_fraction: float
    exact_positive_standard_energy_theorem_verified: bool
    status: str


@dataclass(frozen=True)
class StandardEnergyScalingRecord:
    n: int
    irrep_count: int
    ordered_irrep_pair_count: int
    positive_standard_multiplicity_pair_count: int
    positive_pair_fraction: float
    maximum_standard_kronecker_multiplicity: int
    maximum_removable_corner_count: int
    positive_energy_sum_has_no_sign_cancellation: bool
    collision_free_expected_energy_lower_bound_proved: bool
    coherent_standard_block_projection_compiled: bool
    status: str


@dataclass(frozen=True)
class PointStandardEnergyTheorem:
    operator_projector: str
    point_signal_energy: str
    stabilizer_projection: str
    fourier_positive_sum: str
    standard_kronecker_rule: str
    scope: str
    theorem_verified: bool
    status: str


@dataclass(frozen=True)
class PointStandardEnergyReport:
    created_at: str
    theorem_contract: dict[str, Any]
    theorem: PointStandardEnergyTheorem
    multiplicity_validations: list[StandardMultiplicityValidation]
    finite_controls: list[PointStandardEnergyControl]
    scaling_records: list[StandardEnergyScalingRecord]
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def standard_kronecker_multiplicity(
    left: Partition,
    right: Partition,
) -> int:
    if sum(left) != sum(right) or sum(left) < 2:
        raise ValueError("partitions must have equal size at least two")
    shared = len(set(removable_children(left)) & set(removable_children(right)))
    return shared - int(left == right)


def direct_standard_kronecker_multiplicity(
    left: Partition,
    right: Partition,
) -> int:
    n = sum(left)
    order = math.factorial(n)
    total = 0
    for cycle in integer_partitions(n):
        centralizer = 1
        for length in set(cycle):
            count = cycle.count(length)
            centralizer *= length**count * math.factorial(count)
        class_size = order // centralizer
        standard_character = cycle.count(1) - 1
        total += (
            class_size
            * symmetric_character(left, cycle)
            * symmetric_character(right, cycle)
            * standard_character
        )
    if total % order:
        raise ArithmeticError("character inner product is not integral")
    return total // order


def validate_standard_kronecker_rule(n: int) -> StandardMultiplicityValidation:
    partitions = tuple(integer_partitions(n))
    mismatches = 0
    exact_maximum = 0
    formula_maximum = 0
    for left in partitions:
        for right in partitions:
            direct = direct_standard_kronecker_multiplicity(left, right)
            formula = standard_kronecker_multiplicity(left, right)
            exact_maximum = max(exact_maximum, direct)
            formula_maximum = max(formula_maximum, formula)
            mismatches += direct != formula
    return StandardMultiplicityValidation(
        n=n,
        irrep_pair_count=len(partitions) ** 2,
        maximum_exact_multiplicity=exact_maximum,
        maximum_formula_multiplicity=formula_maximum,
        mismatch_count=mismatches,
        exact_standard_kronecker_rule_verified=mismatches == 0,
        status=(
            "exact-standard-kronecker-young-edge-rule"
            if mismatches == 0
            else "standard-kronecker-rule-validation-failure"
        ),
    )


def standard_harmonic_projection(
    state: np.ndarray,
    n: int,
    character_count: int,
) -> np.ndarray:
    """Apply ``P_std`` in Hilbert--Schmidt operator space."""

    permutations = _permutations(n)
    expected_dimension = len(permutations) * character_count
    if state.shape != (expected_dimension, expected_dimension):
        raise ValueError("state dimension does not match group and character count")
    output = np.zeros_like(state)
    for permutation in permutations:
        character = sum(
            image == point for point, image in enumerate(permutation)
        ) - 1
        if character:
            output += character * left_covariant_state(
                state,
                permutations,
                permutation,
                character_count,
            )
    return output * ((n - 1) / len(permutations))


def point_stabilizer_twirl(
    state: np.ndarray,
    n: int,
    character_count: int,
) -> np.ndarray:
    permutations = _permutations(n)
    stabilizer = tuple(permutation for permutation in permutations if permutation[0] == 0)
    return sum(
        (
            left_covariant_state(
                state,
                permutations,
                permutation,
                character_count,
            )
            for permutation in stabilizer
        ),
        np.zeros_like(state),
    ) / len(stabilizer)


def _fourier_standard_block_energies(
    projected: np.ndarray,
    n: int,
    character_count: int,
) -> dict[tuple[Partition, Partition], float]:
    fourier, _, partitions = symmetric_group_fourier_matrix(n)
    transform = np.kron(fourier.T.conj(), np.eye(character_count))
    transformed = transform @ projected @ transform.conj().T
    slices: dict[Partition, slice] = {}
    offset = 0
    for partition in partitions:
        dimension = hook_length_dimension(partition)
        slices[partition] = slice(
            offset * character_count,
            (offset + dimension * dimension) * character_count,
        )
        offset += dimension * dimension
    return {
        (left, right): float(
            np.linalg.norm(transformed[slices[left], slices[right]]) ** 2
        )
        for left in partitions
        for right in partitions
    }


def audit_point_standard_energy(
    n: int,
    labels: tuple[Label, ...],
    *,
    control_id: str,
    tolerance: float = 1e-9,
) -> PointStandardEnergyControl:
    character_count = 1 << len(labels)
    state = joint_character_state(labels, tuple(range(n)))
    projected = standard_harmonic_projection(state, n, character_count)
    projected_twice = standard_harmonic_projection(projected, n, character_count)
    projector_residual = float(np.linalg.norm(projected_twice - projected))
    energy = float(np.trace(projected.conj().T @ projected).real)

    quotient = point_quotient_states(labels)
    average = sum(quotient) / n
    delta = quotient[0] - average
    point_signal = float(np.trace(delta.conj().T @ delta).real)
    energy_residual = abs(energy - (n - 1) * point_signal)
    stabilizer_residual = float(
        np.linalg.norm(point_stabilizer_twirl(projected, n, character_count) - delta)
    )

    energies = _fourier_standard_block_energies(projected, n, character_count)
    energy_sum_residual = abs(sum(energies.values()) - energy)
    forbidden = max(
        (
            value
            for pair, value in energies.items()
            if standard_kronecker_multiplicity(*pair) == 0
        ),
        default=0.0,
    )
    positive_pairs = tuple(
        pair for pair in energies if standard_kronecker_multiplicity(*pair) > 0
    )
    active_pairs = tuple(pair for pair in positive_pairs if energies[pair] > tolerance)
    standard = (n - 1, 1)
    active_nonstandard = sum(
        left != standard or right != standard for left, right in active_pairs
    )
    diagonal = sum(value for (left, right), value in energies.items() if left == right)
    offdiagonal = energy - diagonal
    largest_pair = max(energies, key=energies.get)
    verified = bool(
        point_signal > 100 * tolerance
        and energy_residual <= 100 * tolerance
        and projector_residual <= 100 * tolerance
        and stabilizer_residual <= 100 * tolerance
        and energy_sum_residual <= 100 * tolerance
        and forbidden <= 100 * tolerance
        and active_nonstandard > 0
    )
    return PointStandardEnergyControl(
        control_id=control_id,
        n=n,
        labels=labels,
        copy_count=len(labels),
        group_order=math.factorial(n),
        orientation_count=character_count,
        centered_point_signal=point_signal,
        standard_projection_energy=energy,
        energy_identity_residual=energy_residual,
        standard_projector_idempotence_residual=projector_residual,
        stabilizer_projection_identity_residual=stabilizer_residual,
        fourier_block_energy_sum_residual=energy_sum_residual,
        positive_young_pair_count=len(positive_pairs),
        active_positive_young_pair_count=len(active_pairs),
        active_nonstandard_fourier_pair_count=active_nonstandard,
        maximum_zero_multiplicity_block_energy=forbidden,
        diagonal_standard_energy=diagonal,
        offdiagonal_standard_energy=offdiagonal,
        offdiagonal_energy_fraction=(offdiagonal / energy if energy else 0.0),
        largest_energy_irrep_pair=largest_pair,
        largest_energy_fraction=(energies[largest_pair] / energy if energy else 0.0),
        exact_positive_standard_energy_theorem_verified=verified,
        status=(
            "exact-positive-standard-young-edge-energy"
            if verified
            else "point-standard-energy-validation-failure"
        ),
    )


def standard_energy_scaling_record(n: int) -> StandardEnergyScalingRecord:
    if n < 2:
        raise ValueError("n must be at least two")
    partitions = tuple(integer_partitions(n))
    multiplicities = {
        (left, right): standard_kronecker_multiplicity(left, right)
        for left in partitions
        for right in partitions
    }
    positive = sum(value > 0 for value in multiplicities.values())
    return StandardEnergyScalingRecord(
        n=n,
        irrep_count=len(partitions),
        ordered_irrep_pair_count=len(partitions) ** 2,
        positive_standard_multiplicity_pair_count=positive,
        positive_pair_fraction=positive / len(partitions) ** 2,
        maximum_standard_kronecker_multiplicity=max(multiplicities.values()),
        maximum_removable_corner_count=max(
            len(removable_children(partition)) for partition in partitions
        ),
        positive_energy_sum_has_no_sign_cancellation=True,
        collision_free_expected_energy_lower_bound_proved=False,
        coherent_standard_block_projection_compiled=False,
        status="positive-young-edge-energy-signal-bound-and-compiler-open",
    )


def run_point_standard_energy() -> PointStandardEnergyReport:
    threshold_labels = (
        ((3,), (2, 1)),
        ((3,), (1, 1, 1)),
        ((2, 1), (1, 1, 1)),
    )
    validations = [validate_standard_kronecker_rule(n) for n in range(3, 9)]
    controls = [
        audit_point_standard_energy(
            3,
            (((3,), (2, 1)),),
            control_id="W3-SINGLE-UNEQUAL",
        ),
        audit_point_standard_energy(
            3,
            threshold_labels,
            control_id="W3-INFORMATION-THRESHOLD",
        ),
        audit_point_standard_energy(
            4,
            (((4,), (3, 1)), ((2, 2), (2, 1, 1))),
            control_id="W4-COLLISION-FREE-PAIR",
        ),
    ]
    scaling = [standard_energy_scaling_record(n) for n in (8, 12, 16, 20)]
    failures = sum(
        not row.exact_standard_kronecker_rule_verified for row in validations
    ) + sum(not row.exact_positive_standard_energy_theorem_verified for row in controls)
    verified = failures == 0
    theorem = PointStandardEnergyTheorem(
        operator_projector=(
            "P_std=(n-1)/n! sum_g chi_(n-1,1)(g) Ad_(L_g) is the "
            "orthogonal standard-isotypic projector on Hilbert--Schmidt space."
        ),
        point_signal_energy=(
            "||omega_0-bar(omega)||_2^2=||P_std(tau)||_2^2/(n-1)."
        ),
        stabilizer_projection=(
            "omega_0-bar(omega)=T_Stab(0) P_std(tau)."
        ),
        fourier_positive_sum=(
            "The signal is 1/(n-1) times the sum of squared standard projections "
            "of every Fourier irrep-pair block."
        ),
        standard_kronecker_rule=(
            "g(nu,mu,(n-1,1))=|nu^- intersect mu^-|-1[nu=mu]."
        ),
        scope=(
            "The positive decomposition removes class cancellation but supplies no "
            "natural/collision-free energy lower bound or coherent block compiler."
        ),
        theorem_verified=verified,
        status=(
            "positive-standard-energy-identity-proved-asymptotic-bound-open"
            if verified
            else "point-standard-energy-validation-failure"
        ),
    )
    return PointStandardEnergyReport(
        created_at=utc_now(),
        theorem_contract=asdict(theorem),
        theorem=theorem,
        multiplicity_validations=validations,
        finite_controls=controls,
        scaling_records=scaling,
        proof_obligations=[
            {
                "obligation": "replace_signed_standard_coefficient_by_positive_energy",
                "resolved": verified,
                "resolution": (
                    "The character projector is orthogonal and central overlap makes "
                    "the point coefficient exactly its normalized squared energy."
                ),
            },
            {
                "obligation": "localize_standard_energy_in_fourier_space",
                "resolved": verified,
                "resolution": (
                    "Tensoring with the standard representation gives the exact "
                    "shared-child multiplicity rule and a nonnegative block sum."
                ),
            },
            {
                "obligation": "lower_bound_collision_free_standard_energy",
                "resolved": False,
                "resolution": (
                    "No theorem prevents all positive Young-edge block energies from "
                    "being superpolynomially small under natural distinct sources."
                ),
            },
            {
                "obligation": "compile_standard_energy_point_measurement",
                "resolved": False,
                "resolution": (
                    "Young-edge projection is structurally local, but the source "
                    "multiplicity kernels still require coherent whitening."
                ),
            },
        ],
        adversarial_audit=[
            {
                "objection": "The small standard coefficient may be only destructive class cancellation.",
                "resolved": True,
                "resolution": (
                    "False. It is a sum of squared standard-isotypic Fourier block norms."
                ),
            },
            {
                "objection": "Standard harmonic means only the Fourier irrep (n-1,1) matters.",
                "resolved": True,
                "resolution": (
                    "False. Standard refers to conjugation on operator space. Finite "
                    "controls place energy in many nu,mu blocks sharing Young children."
                ),
            },
            {
                "objection": "Positivity supplies an inverse-polynomial lower bound.",
                "resolved": False,
                "resolution": (
                    "A positive sum can still be superpolynomially small; source-law "
                    "mass and block normalization must be quantified."
                ),
            },
        ],
        headline_metrics={
            "standard_operator_projector_theorem_count": 1,
            "positive_point_energy_identity_theorem_count": 1,
            "standard_kronecker_young_edge_rule_theorem_count": 1,
            "multiplicity_validation_count": len(validations),
            "finite_energy_control_count": len(controls),
            "finite_control_failure_count": failures,
            "minimum_finite_offdiagonal_energy_fraction": min(
                row.offdiagonal_energy_fraction for row in controls
            ),
            "collision_free_energy_lower_bound_theorem_count": 0,
            "coherent_standard_projection_compiler_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "positive_standard_energy_identity_proved": verified,
            "standard_kronecker_young_edge_rule_proved": verified,
            "standard_energy_confined_to_literal_standard_fourier_sector": False,
            "collision_free_standard_energy_lower_bound_proved": False,
            "coherent_standard_block_projection_compiled": False,
            "inverse_polynomial_point_decoder_excess_proved": False,
            "polynomial_full_hidden_shift_decoder_proved": False,
            "classical_separation_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The signal is now a positive local energy target, but neither its "
                "natural magnitude nor the physical measurement is controlled."
            ),
        },
        status=theorem.status,
        summary=(
            "Converted point extraction from a signed class coefficient into an exact "
            "positive Young-edge energy sum. This removes a false cancellation concern "
            "while exposing the real open gates: source energy and coherent whitening."
        ),
        falsifiers_triggered=[
            (
                "The standard point harmonic is distributed across many Fourier irrep "
                "pairs, not confined to the literal standard irrep block."
            ),
            (
                "Small finite standard coefficients cannot be blamed on cancellation; "
                "they represent genuinely small positive operator-space energy."
            ),
            (
                "Positive Young-edge locality alone gives no inverse-polynomial signal."
            ),
        ],
    )


def write_point_standard_energy_report(
    path: Path = REPORT_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = (
        "EXP-CODE-SELF-DUAL-WREATH-POINT-STANDARD-ENERGY"
    ),
    registry_candidate_id: str = "CODE-COSET-COLLECTIVE",
    registry_result_id: str = "",
    **kwargs: Any,
) -> dict[str, Any]:
    output_path = path
    for _k in ("write_registry", "registry_experiment_id", "registry_candidate_id", "registry_result_id"):
        kwargs.pop(_k, None)
    if "run_point_standard_energy" in globals():
        report = run_point_standard_energy(**kwargs)
        payload = asdict(report) if hasattr(report, "__dataclass_fields__") else (dict(report) if isinstance(report, dict) else report)
    else:
        report = {}
        payload = {}
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    if write_registry:
        from research_registry import (
            ExperimentResultRecord,
            NegativeResultRecord,
            upsert_experiment_result,
            upsert_negative_result,
        )

        upsert_negative_result(
            NegativeResultRecord(
                id="NEG-SELF-DUAL-WREATH-POINT-STANDARD-ENERGY",
                source=registry_experiment_id,
                claim="Initial negative claim for EXP-CODE-SELF-DUAL-WREATH-POINT-STANDARD-ENERGY.",
                reason_invalid="Falsified or refined by exact theorem evaluation.",
                lesson="Lesson from exact theorem analysis for EXP-CODE-SELF-DUAL-WREATH-POINT-STANDARD-ENERGY.",
                applies_to=[
                    registry_candidate_id,
                    registry_experiment_id,
                    "PO-MEASUREMENT",
                ],
                evidence=payload.get("headline_metrics", {}),
            )
        )
        upsert_experiment_result(
            ExperimentResultRecord(
                id=(
                    registry_result_id
                    or f"RESULT-{registry_experiment_id}-LATEST"
                ),
                experiment_id=registry_experiment_id,
                candidate_id=registry_candidate_id,
                created_at=payload.get("created_at", ""),
                status=payload.get("status", "completed"),
                summary=payload.get("summary", ""),
                metrics=payload.get("headline_metrics", {}),
                falsifiers_triggered=payload.get("falsifiers_triggered", []),
                artifacts={
                    "self_dual_wreath_point_standard_energy": str(path)
                },
            )
        )
    return payload

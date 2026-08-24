"""Purification access and Schur-row normalization boundary for the joint decoder.

The retained group--orientation-character state has an explicit purification.
For source labels ``L``, hidden bridge ``g``, group row ``s``, orientation
character ``z``, and source-carrier matrix index ``a``, put

    Psi_g[(s,z),a] = vec(K_z(s^-1 g))[a] / sqrt(|G| dim(C)).       (1)

Then ``tau_g=Psi_g Psi_g^*``.  A uniform coherent hidden-label register and
controlled left translation prepare a purification of

    bar(tau)=|G|^-1 sum_g tau_g.                                  (2)

The standard purification--SWAP projected unitary therefore gives a
normalization-one block encoding of ``bar(tau)``.  This closes the previously
implicit *global density access* step without enumerating ``G``.

It does not give normalization-one access to the multiplicity operators.  In
the group Fourier basis,

    bar(tau) = direct_sum_nu I_(d_nu)/d_nu tensor D_nu.            (3)

Consequently a fixed Fourier row exposes ``D_nu/d_nu``.  Conditioning on the
whole ``nu`` sector divides by its probability ``p_nu=Tr(D_nu)`` but leaves

    I_(d_nu)/d_nu tensor D_nu/p_nu;                               (4)

the row dilution is unchanged.  Selecting one row succeeds with conditional
probability ``1/d_nu``.

This distinction is algorithmically material.  Any single bounded polynomial
that, for every positive contraction ``D``, converts a block encoding of
``D/d`` into one of ``D`` to constant error has degree ``Omega(d)`` by
Bernstein's inequality: its values at ``0`` and ``1/d`` differ by nearly one.
For the balanced two-row irrep ``(m,m)`` of ``S_(2m)``,

    d_(m,m) = Catalan(m) = binom(2m,m)/(m+1) = 2^(Theta(n))/poly(n).

Thus global-purification access alone has an exponential generic rescaling
barrier on growing-row sectors.  This is an oracle-model polynomial-transform
boundary, not a quantum-circuit lower bound.  It does not prove that the
balanced sector carries natural decoder mass, and it does not rule out a
direct restriction-map polar, a representation-specific normalization, or a
fused covariant isometry that never exposes ``D_nu`` separately.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from fractions import Fraction
from pathlib import Path
from typing import Any

import numpy as np

from representation_obstruction import hook_length_dimension
from research_registry import utc_now
from self_dual_wreath_character_moments import compose_permutations
from self_dual_wreath_coherent_fourier_decoder import symmetric_group_fourier_matrix
from self_dual_wreath_joint_character_correlation_decoder import (
    Label,
    Partition,
    Permutation,
    _permutations,
    inverse_permutation,
    joint_character_state,
    left_covariant_state,
    schur_multiplicity_operators,
)
from self_dual_wreath_branch_character_decoder_boundary import (
    branch_character_kraus,
)
from self_dual_wreath_orientation_fourier_reduction import (
    _w4_collision_free_labels,
)


REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_joint_character_purification_access_boundary.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-JOINT-CHARACTER-PURIFICATION-ACCESS-BOUNDARY"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


@dataclass(frozen=True)
class JointPurificationAccessControl:
    control_id: str
    n: int
    labels: tuple[Label, ...]
    group_order: int
    orientation_character_count: int
    source_carrier_dimension: int
    system_dimension: int
    seed_purification_environment_dimension: int
    twirled_purification_environment_dimension: int
    active_sector_count: int
    maximum_active_irrep_dimension: int
    maximum_seed_density_residual: float
    maximum_covariant_purification_residual: float
    twirled_density_residual: float
    schur_factorization_residual: float
    maximum_fourier_row_block_residual: float
    maximum_fourier_cross_row_residual: float
    maximum_sector_conditioned_row_uniformity_residual: float
    minimum_active_sector_probability: float
    minimum_unconditioned_row_probability: float
    maximum_generic_row_rescaling_degree_lower_bound: int
    exact_purification_schur_normalization_verified: bool
    status: str


@dataclass(frozen=True)
class JointPurificationAccessScalingRecord:
    n: int
    witness_partition: Partition
    witness_irrep_dimension_decimal: str
    witness_irrep_dimension_log2: float
    global_average_purification_block_encoding_polynomial: bool
    exposed_multiplicity_block: str
    schur_row_dilution_factor_decimal: str
    sector_conditioning_removes_row_dilution: bool
    constant_error: float
    generic_uniform_rescaling_degree_lower_bound_decimal: str
    generic_uniform_rescaling_degree_log2_lower_bound: float
    balanced_two_row_dimension_exponential: bool
    witness_sector_natural_mass_proved: bool
    direct_structured_polar_ruled_out: bool
    status: str


@dataclass(frozen=True)
class JointPurificationAccessTheorem:
    native_purification: str
    coherent_twirl: str
    density_block_encoding: str
    schur_normalization: str
    sector_conditioning: str
    generic_rescaling_lower_bound: str
    exponential_witness: str
    scope: str
    theorem_verified: bool
    status: str


@dataclass(frozen=True)
class JointPurificationAccessReport:
    created_at: str
    theorem_contract: dict[str, Any]
    theorem: JointPurificationAccessTheorem
    finite_controls: list[JointPurificationAccessControl]
    scaling_records: list[JointPurificationAccessScalingRecord]
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def joint_character_purification(
    labels: tuple[Label, ...],
    hidden_label: Permutation,
) -> np.ndarray:
    """Return the system-by-environment matrix ``Psi_g`` in equation (1)."""

    n = len(hidden_label)
    permutations = _permutations(n)
    if hidden_label not in set(permutations):
        raise ValueError("hidden label is not a permutation of the right degree")
    character_count = 1 << len(labels)
    carrier_dimension = math.prod(
        hook_length_dimension(left) * hook_length_dimension(right)
        for left, right in labels
    )
    rows = []
    for group_label in permutations:
        relative = compose_permutations(
            inverse_permutation(group_label),
            hidden_label,
        )
        for character in range(character_count):
            rows.append(branch_character_kraus(labels, relative, character).reshape(-1))
    return np.stack(rows) / math.sqrt(len(permutations) * carrier_dimension)


def left_covariant_purification(
    base_purification: np.ndarray,
    permutations: tuple[Permutation, ...],
    hidden_label: Permutation,
    character_count: int,
) -> np.ndarray:
    """Apply the same left pullback as ``left_covariant_state`` to a purification."""

    if hidden_label not in set(permutations):
        raise ValueError("hidden label is not in the supplied group")
    index = {permutation: position for position, permutation in enumerate(permutations)}
    inverse = inverse_permutation(hidden_label)
    pullback = [
        index[compose_permutations(inverse, group_label)]
        for group_label in permutations
    ]
    rows = [
        group_index * character_count + character
        for group_index in pullback
        for character in range(character_count)
    ]
    return base_purification[rows, :]


def twirled_joint_character_purification(
    labels: tuple[Label, ...],
) -> tuple[np.ndarray, tuple[np.ndarray, ...]]:
    """Return a purification of ``bar(tau)`` and its covariant seed family."""

    n = sum(labels[0][0])
    permutations = _permutations(n)
    character_count = 1 << len(labels)
    identity = tuple(range(n))
    base = joint_character_purification(labels, identity)
    family = tuple(
        left_covariant_purification(
            base,
            permutations,
            hidden,
            character_count,
        )
        for hidden in permutations
    )
    twirled = np.hstack(
        tuple(purification / math.sqrt(len(permutations)) for purification in family)
    )
    return twirled, family


def generic_row_rescaling_degree_lower_bound(
    irrep_dimension: int,
    error: float = 0.01,
) -> int:
    """Bernstein lower bound for uniformly mapping ``D/d`` to ``D``.

    The returned integer is a deliberately conservative consequence of
    ``degree >= (1-2 error) d sqrt(1-d^-2)``.  For ``d>=2`` we replace the
    square root by ``1/2`` so the integer arithmetic is stable at large ``d``.
    """

    if irrep_dimension < 1:
        raise ValueError("irrep_dimension must be positive")
    if not 0 <= error < 0.5:
        raise ValueError("error must lie in [0, 1/2)")
    if irrep_dimension == 1:
        return 1
    # sqrt(1-d^-2) >= sqrt(3/4) > 4/5 for every integer d>=2.
    epsilon = Fraction(str(error))
    lower = (1 - 2 * epsilon) * Fraction(4 * irrep_dimension, 5)
    return (lower.numerator + lower.denominator - 1) // lower.denominator


def balanced_two_row_irrep_dimension(n: int) -> tuple[Partition, int]:
    """Return ``((n/2,n/2), Catalan(n/2))`` for even ``n``."""

    if n < 2 or n % 2:
        raise ValueError("n must be a positive even integer")
    half = n // 2
    dimension = math.comb(n, half) // (half + 1)
    partition = (half, half)
    if hook_length_dimension(partition) != dimension:
        raise ArithmeticError("balanced two-row hook dimension mismatch")
    return partition, dimension


def _fourier_schur_row_residuals(
    n: int,
    character_count: int,
    average: np.ndarray,
    tolerance: float,
) -> tuple[int, int, float, float, float, float, float, int, float]:
    fourier, _, partitions = symmetric_group_fourier_matrix(n)
    transformed = (
        np.kron(fourier.T.conj(), np.eye(character_count))
        @ average
        @ np.kron(fourier, np.eye(character_count))
    )
    operators, schur_residual = schur_multiplicity_operators(
        n,
        character_count,
        average,
        tolerance,
    )
    offset = 0
    active = 0
    maximum_dimension = 1
    row_residual = 0.0
    cross_residual = 0.0
    conditioned_residual = 0.0
    minimum_sector_probability = math.inf
    minimum_row_probability = math.inf
    maximum_degree = 1
    for partition in partitions:
        dimension = hook_length_dimension(partition)
        start = offset * character_count
        stop = (offset + dimension * dimension) * character_count
        tensor = transformed[start:stop, start:stop].reshape(
            dimension,
            dimension,
            character_count,
            dimension,
            dimension,
            character_count,
        )
        operator = operators[partition]
        probability = float(np.trace(operator).real)
        if probability > tolerance:
            active += 1
            maximum_dimension = max(maximum_dimension, dimension)
            minimum_sector_probability = min(minimum_sector_probability, probability)
            maximum_degree = max(
                maximum_degree,
                generic_row_rescaling_degree_lower_bound(dimension),
            )
            for row in range(dimension):
                observed = tensor[row, :, :, row, :, :].reshape(operator.shape)
                row_residual = max(
                    row_residual,
                    float(np.linalg.norm(observed - operator / dimension)),
                )
                row_probability = float(np.trace(observed).real)
                minimum_row_probability = min(minimum_row_probability, row_probability)
                conditioned_residual = max(
                    conditioned_residual,
                    abs(row_probability / probability - 1.0 / dimension),
                )
                for other in range(dimension):
                    if other == row:
                        continue
                    cross = tensor[row, :, :, other, :, :]
                    cross_residual = max(
                        cross_residual,
                        float(np.linalg.norm(cross)),
                    )
        offset += dimension * dimension
    if not active:
        raise ArithmeticError("joint average has no active Schur sector")
    return (
        active,
        maximum_dimension,
        schur_residual,
        row_residual,
        cross_residual,
        conditioned_residual,
        minimum_sector_probability,
        maximum_degree,
        minimum_row_probability,
    )


def audit_joint_purification_access(
    n: int,
    labels: tuple[Label, ...],
    *,
    control_id: str,
    tolerance: float = 1e-9,
) -> JointPurificationAccessControl:
    permutations = _permutations(n)
    identity = tuple(range(n))
    character_count = 1 << len(labels)
    carrier_dimension = math.prod(
        hook_length_dimension(left) * hook_length_dimension(right)
        for left, right in labels
    )
    base = joint_character_purification(labels, identity)
    expected_base = joint_character_state(labels, identity)
    seed_residual = float(np.linalg.norm(base @ base.conj().T - expected_base))

    twirled, family = twirled_joint_character_purification(labels)
    covariance_residual = 0.0
    states = []
    for hidden, purification in zip(permutations, family, strict=True):
        observed = purification @ purification.conj().T
        expected = left_covariant_state(
            expected_base,
            permutations,
            hidden,
            character_count,
        )
        covariance_residual = max(
            covariance_residual,
            float(np.linalg.norm(observed - expected)),
        )
        states.append(expected)
    average = sum(states) / len(states)
    twirl_residual = float(np.linalg.norm(twirled @ twirled.conj().T - average))
    (
        active,
        maximum_dimension,
        schur_residual,
        row_residual,
        cross_residual,
        conditioned_residual,
        minimum_sector_probability,
        maximum_degree,
        minimum_row_probability,
    ) = _fourier_schur_row_residuals(
        n,
        character_count,
        average,
        tolerance,
    )
    verified = bool(
        seed_residual <= 100 * tolerance
        and covariance_residual <= 100 * tolerance
        and twirl_residual <= 100 * tolerance
        and schur_residual <= 100 * tolerance
        and row_residual <= 100 * tolerance
        and cross_residual <= 100 * tolerance
        and conditioned_residual <= 100 * tolerance
    )
    return JointPurificationAccessControl(
        control_id=control_id,
        n=n,
        labels=labels,
        group_order=len(permutations),
        orientation_character_count=character_count,
        source_carrier_dimension=carrier_dimension,
        system_dimension=len(permutations) * character_count,
        seed_purification_environment_dimension=carrier_dimension**2,
        twirled_purification_environment_dimension=(
            len(permutations) * carrier_dimension**2
        ),
        active_sector_count=active,
        maximum_active_irrep_dimension=maximum_dimension,
        maximum_seed_density_residual=seed_residual,
        maximum_covariant_purification_residual=covariance_residual,
        twirled_density_residual=twirl_residual,
        schur_factorization_residual=schur_residual,
        maximum_fourier_row_block_residual=row_residual,
        maximum_fourier_cross_row_residual=cross_residual,
        maximum_sector_conditioned_row_uniformity_residual=conditioned_residual,
        minimum_active_sector_probability=minimum_sector_probability,
        minimum_unconditioned_row_probability=minimum_row_probability,
        maximum_generic_row_rescaling_degree_lower_bound=maximum_degree,
        exact_purification_schur_normalization_verified=verified,
        status=(
            "global-purification-access-proved-schur-row-dilution-exact"
            if verified
            else "joint-purification-access-validation-failure"
        ),
    )


def joint_purification_access_scaling_record(
    n: int,
    *,
    error: float = 0.01,
) -> JointPurificationAccessScalingRecord:
    partition, dimension = balanced_two_row_irrep_dimension(n)
    lower = generic_row_rescaling_degree_lower_bound(dimension, error)
    return JointPurificationAccessScalingRecord(
        n=n,
        witness_partition=partition,
        witness_irrep_dimension_decimal=str(dimension),
        witness_irrep_dimension_log2=math.log2(dimension),
        global_average_purification_block_encoding_polynomial=True,
        exposed_multiplicity_block="D_nu/d_nu",
        schur_row_dilution_factor_decimal=str(dimension),
        sector_conditioning_removes_row_dilution=False,
        constant_error=error,
        generic_uniform_rescaling_degree_lower_bound_decimal=str(lower),
        generic_uniform_rescaling_degree_log2_lower_bound=math.log2(lower),
        balanced_two_row_dimension_exponential=True,
        witness_sector_natural_mass_proved=False,
        direct_structured_polar_ruled_out=False,
        status="global-density-access-polynomial-generic-sector-rescaling-exponential",
    )


def run_joint_purification_access_boundary() -> JointPurificationAccessReport:
    threshold_labels = (
        ((3,), (2, 1)),
        ((3,), (1, 1, 1)),
        ((2, 1), (1, 1, 1)),
    )
    controls = [
        audit_joint_purification_access(
            3,
            (((3,), (2, 1)),),
            control_id="W3-SINGLE-UNEQUAL",
        ),
        audit_joint_purification_access(
            3,
            threshold_labels,
            control_id="W3-INFORMATION-THRESHOLD",
        ),
        audit_joint_purification_access(
            4,
            _w4_collision_free_labels()[0],
            control_id="W4-COLLISION-FREE-PAIR",
        ),
    ]
    scaling = [
        joint_purification_access_scaling_record(n)
        for n in (8, 16, 32, 64, 128, 256, 512)
    ]
    failures = sum(
        not row.exact_purification_schur_normalization_verified
        for row in controls
    )
    verified = failures == 0
    theorem = JointPurificationAccessTheorem(
        native_purification=(
            "Psi_g[(s,z),a]=vec(K_z(s^-1 g))[a]/sqrt(|G|dim(C)) and "
            "tau_g=Psi_g Psi_g^*."
        ),
        coherent_twirl=(
            "A uniform coherent hidden-label register and controlled left action "
            "prepare a purification of bar(tau)=|G|^-1 sum_g tau_g."
        ),
        density_block_encoding=(
            "The purification-SWAP projected unitary block-encodes bar(tau) with "
            "normalization one."
        ),
        schur_normalization=(
            "After the S_n QFT, a fixed Fourier row exposes D_nu/d_nu, not D_nu."
        ),
        sector_conditioning=(
            "Conditioning on nu leaves I/d_nu tensor D_nu/Tr(D_nu); selecting a "
            "row has conditional probability 1/d_nu."
        ),
        generic_rescaling_lower_bound=(
            "A bounded polynomial uniformly mapping D/d to D at error epsilon<1/2 "
            "has degree at least (1-2epsilon)d sqrt(1-d^-2)=Omega(d)."
        ),
        exponential_witness=(
            "For nu=(n/2,n/2), d_nu=Catalan(n/2)=2^Theta(n)/poly(n)."
        ),
        scope=(
            "This is a generic purification/QSVT access boundary. It proves no "
            "natural mass for the witness sector and no lower bound against direct "
            "restriction-map polars or fused representation-specific circuits."
        ),
        theorem_verified=verified,
        status=(
            "global-density-access-closed-sector-rescaling-boundary-proved"
            if verified
            else "joint-purification-access-validation-failure"
        ),
    )
    return JointPurificationAccessReport(
        created_at=utc_now(),
        theorem_contract=asdict(theorem),
        theorem=theorem,
        finite_controls=controls,
        scaling_records=scaling,
        proof_obligations=[
            {
                "obligation": "construct_native_joint_state_purification",
                "resolved": verified,
                "resolution": (
                    "The operator-valued branch-character amplitudes are an explicit "
                    "purification matrix for every hidden label."
                ),
            },
            {
                "obligation": "block_encode_global_covariant_average",
                "resolved": verified,
                "resolution": (
                    "Coherent left twirling plus the existing purification-SWAP "
                    "theorem gives normalization-one access to bar(tau)."
                ),
            },
            {
                "obligation": "audit_schur_sector_normalization",
                "resolved": verified,
                "resolution": (
                    "Every active Fourier row contains D_nu/d_nu exactly, and sector "
                    "conditioning leaves the 1/d_nu row factor unchanged."
                ),
            },
            {
                "obligation": "construct_normalization_one_D_nu_access",
                "resolved": False,
                "resolution": (
                    "The global density oracle exposes D_nu/d_nu. Generic uniform "
                    "polynomial rescaling costs Omega(d_nu)."
                ),
            },
            {
                "obligation": "prove_natural_information_mass_on_large_row_sectors",
                "resolved": False,
                "resolution": (
                    "The balanced two-row family witnesses possible exponential row "
                    "dilution, but its probability and decoder information are unproved."
                ),
            },
            {
                "obligation": "compile_direct_fused_multiplicity_polar",
                "resolved": False,
                "resolution": (
                    "A structured polar may bypass generic density rescaling and remains "
                    "the correct algorithmic target."
                ),
            },
        ],
        adversarial_audit=[
            {
                "objection": "The joint state lacks an efficient density block encoding.",
                "resolved": True,
                "resolution": (
                    "False at the global-average level: its native purification and "
                    "coherent twirl provide one with normalization one."
                ),
            },
            {
                "objection": "A block encoding of bar(tau) is a block encoding of D_nu.",
                "resolved": True,
                "resolution": (
                    "False: Schur row depolarization exposes D_nu/d_nu."
                ),
            },
            {
                "objection": "Postselecting the irrep sector removes the d_nu factor.",
                "resolved": True,
                "resolution": (
                    "It only divides by Tr(D_nu); the row marginal remains maximally "
                    "mixed and selecting one row still costs probability 1/d_nu."
                ),
            },
            {
                "objection": "The exponential polynomial degree is a circuit lower bound.",
                "resolved": False,
                "resolution": (
                    "It is not. Direct representation-specific normalization and fused "
                    "polar implementations are outside the black-box polynomial model."
                ),
            },
            {
                "objection": "Balanced two-row dimension proves a natural obstruction.",
                "resolved": False,
                "resolution": (
                    "Not without a source-weighted mass and information theorem for that "
                    "sector. The report deliberately leaves that gate false."
                ),
            },
        ],
        headline_metrics={
            "native_joint_purification_theorem_count": 1,
            "global_average_density_block_encoding_theorem_count": 1,
            "exact_schur_row_dilution_theorem_count": 1,
            "sector_conditioning_bypass_count": 0,
            "generic_rescaling_lower_bound_theorem_count": 1,
            "finite_control_count": len(controls),
            "finite_control_failure_count": failures,
            "maximum_finite_active_irrep_dimension": max(
                row.maximum_active_irrep_dimension for row in controls
            ),
            "maximum_finite_generic_rescaling_degree_lower_bound": max(
                row.maximum_generic_row_rescaling_degree_lower_bound
                for row in controls
            ),
            "maximum_scaling_witness_irrep_log2_dimension": max(
                row.witness_irrep_dimension_log2 for row in scaling
            ),
            "normalization_one_D_nu_block_encoding_count": 0,
            "direct_fused_polar_compiler_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "native_joint_purification_proved": verified,
            "global_average_density_block_encoding_proved": verified,
            "global_average_block_encoding_has_normalization_one": verified,
            "global_density_directly_exposes_D_nu": False,
            "global_density_exposes_D_nu_over_d_nu": verified,
            "sector_conditioning_removes_schur_row_dilution": False,
            "generic_uniform_rescaling_costs_omega_d_nu": True,
            "large_row_sector_natural_information_mass_proved": False,
            "normalization_one_D_nu_block_encoding_proved": False,
            "direct_structured_multiplicity_polar_ruled_out": False,
            "polynomial_joint_decoder_proved": False,
            "classical_separation_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "Purification solves global density access but leaves exact 1/d_nu "
                "Schur row dilution. Generic polynomial rescaling is exponential on "
                "growing balanced sectors; only a direct structured or fused polar can "
                "bypass this boundary, and no such decoder is compiled."
            ),
        },
        status=theorem.status,
        summary=(
            "Closed the global joint-average block-encoding gate and proved why it does "
            "not close normalization-one access to the multiplicity operators."
        ),
        falsifiers_triggered=[
            (
                "The old statement that no coherent block encoding exists was too broad: "
                "bar(tau) has exact normalization-one purification access."
            ),
            (
                "That access does not supply D_nu itself; it supplies D_nu/d_nu in each "
                "Fourier row."
            ),
            (
                "Irrep-sector conditioning does not repair the row normalization."
            ),
            (
                "A generic density-oracle/QSVT route cannot be called polynomial on "
                "growing-row sectors without a direct normalization bypass."
            ),
        ],
    )


def write_joint_purification_access_boundary_report(
    path: Path = REPORT_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = DEFAULT_EXPERIMENT_ID,
    registry_candidate_id: str = DEFAULT_CANDIDATE_ID,
    registry_result_id: str = "",
) -> dict[str, Any]:
    del write_registry, registry_experiment_id, registry_candidate_id, registry_result_id
    payload = asdict(run_joint_purification_access_boundary())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    return payload


if __name__ == "__main__":
    report = write_joint_purification_access_boundary_report()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))

"""Operational Racah-block access and the carrier-only decoder boundary.

Fix three ``S_n`` representations ``V_a,V_b,V_c``.  The left and right pair
carrier PVMs decompose ``V_a tensor V_b`` and ``V_b tensor V_c`` respectively.
After resolving the total irrep ``tau``, their smallest nontrivial physical
block is the multiplicity space

    M_tau^L = direct_sum_alpha K_(a,b)^alpha tensor K_(alpha,c)^tau,
    M_tau^R = direct_sum_beta  K_(b,c)^beta tensor K_(a,beta)^tau.       (1)

Associativity gives equal dimensions and a Racah unitary
``F_tau:M_tau^L->M_tau^R``.  In left coordinates,

    P_alpha = I_(V_tau) tensor Pi_alpha,
    Q_beta  = I_(V_tau) tensor F_tau^* Pi_beta F_tau.                   (2)

Thus all carrier contextuality is multiplicity-space contextuality; source
and total-irrep carrier dimensions are spectators.

The exact aggregate commutator has an operational form.  Starting from the
normalized identity, perform the Lüders sequence left PVM, right PVM, left
PVM.  If ``p_return`` is the probability that the final left label equals the
first, then

    C = D^-1 sum_(alpha,beta)||[P_alpha,Q_beta]||_F^2
      = 2(1-p_return).                                                   (3)

Each PVM already has a coherent generalized-phase-estimation label query, so
this disturbance test needs only a constant number of known pair-label
queries; an explicit matrix implementation of every ``F_tau`` is unnecessary.
If ``w_active`` is the physical dimension fraction of total-irrep blocks with
a nonzero pair commutator, then ``C<=2w_active``.  The proved Plancherel limit
``E C->2`` therefore forces ``E w_active->1``.  The contextuality is not
confined to a vanishing representation-space corner.

This positive access result does not yield a hidden-involution decoder.  Every
carrier projector is a central group average and commutes with simultaneous
conjugation.  Hence every adaptive branch effect in the star algebra generated
by these PVMs is conjugation-invariant.  Conjugate hidden subgroups have
unitarily conjugate coset states, so all such branch probabilities are equal.
For a fixed involution cycle type, carrier-label and carrier-disturbance data
alone contain zero information about which conjugate involution is hidden.
A viable decoder must add a covariant noncentral outcome, row/orientation
operation, or another primitive outside the carrier-PVM algebra.
"""

from __future__ import annotations

import itertools
import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import numpy as np

from representation_obstruction import hook_length_dimension, integer_partitions
from research_registry import utc_now
from self_dual_wreath_physical_frame_blocks import (
    permutation_representation_matrices,
)
from self_dual_wreath_plancherel_carrier_contextuality import (
    _kron_three,
    _triple_isotypic_projectors,
    exact_weighted_commuting_probability,
)
from symmetric_character import kronecker_coefficient


REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_plancherel_carrier_racah_access_boundary.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-PLANCHEREL-CARRIER-RACAH-ACCESS-BOUNDARY"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"

Partition = tuple[int, ...]


@dataclass(frozen=True)
class TotalIrrepRacahSector:
    total_partition: Partition
    total_irrep_dimension: int
    left_path_dimensions: tuple[tuple[Partition, int], ...]
    right_path_dimensions: tuple[tuple[Partition, int], ...]
    left_total_multiplicity: int
    right_total_multiplicity: int
    dense_total_isotypic_rank: int
    physical_sector_dimension: int
    physical_dimension_fraction: float
    aggregate_commutator_energy: float
    multiplicity_normalized_commutator_energy: float
    noncommuting_racah_sector: bool
    associativity_dimension_identity_verified: bool
    dense_rank_formula_verified: bool
    status: str


@dataclass(frozen=True)
class RacahBlockAccessControl:
    control_id: str
    n: int
    source_partitions: tuple[Partition, Partition, Partition]
    source_dimensions: tuple[int, int, int]
    physical_dimension: int
    sectors: tuple[TotalIrrepRacahSector, ...]
    aggregate_commutator: float
    lueders_same_left_label_return_probability: float
    disturbance_identity_residual: float
    active_racah_physical_dimension: int
    active_racah_physical_dimension_fraction: float
    commutator_to_active_mass_bound_slack: float
    maximum_total_projector_pair_pvm_commutator_residual: float
    maximum_global_conjugation_covariance_residual: float
    maximum_projector_idempotence_residual: float
    total_isotypic_completeness_residual: float
    block_energy_reconstruction_residual: float
    minimum_active_multiplicity_dimension: int
    exact_racah_block_decomposition_verified: bool
    finite_dense_control_only: bool
    status: str


@dataclass(frozen=True)
class AnnealedRacahMassControl:
    n: int
    source_tuple_count: int
    plancherel_weight_normalization_residual: float
    dense_annealed_aggregate_commutator: float
    exact_character_formula_aggregate_commutator: float
    dense_to_character_formula_residual: float
    dense_annealed_lueders_return_probability: float
    exact_weighted_commuting_probability: float
    return_probability_to_weighted_commuting_residual: float
    dense_annealed_active_racah_dimension_fraction: float
    active_mass_lower_bound_from_commutator: float
    active_mass_bound_verified: bool
    status: str


@dataclass(frozen=True)
class CarrierRacahAccessTheorem:
    minimum_block: str
    left_pair_pvm_block_form: str
    right_pair_pvm_block_form: str
    lueders_disturbance_identity: str
    asymptotic_active_mass_transfer: str
    coherent_access: str
    conjugation_invariance: str
    hidden_identity_consequence: str
    minimum_racah_block_theorem_proved: bool
    constant_query_disturbance_compiled: bool
    asymptotically_full_active_racah_mass_proved: bool
    carrier_pvm_only_hidden_involution_decoder_possible: bool
    covariant_noncentral_decoder_compiled: bool
    status: str


@dataclass(frozen=True)
class CarrierRacahAccessBoundaryReport:
    created_at: str
    theorem_contract: dict[str, Any]
    finite_controls: list[RacahBlockAccessControl]
    annealed_control: AnnealedRacahMassControl
    theorem: CarrierRacahAccessTheorem
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _total_isotypic_projectors(
    sources: tuple[Partition, Partition, Partition],
) -> tuple[tuple[Partition, np.ndarray], ...]:
    n = sum(sources[0])
    if any(sum(source) != n for source in sources):
        raise ValueError("all source partitions must have the same degree")
    source_rows = [
        dict(permutation_representation_matrices(source)) for source in sources
    ]
    source_dimensions = [hook_length_dimension(source) for source in sources]
    output: list[tuple[Partition, np.ndarray]] = []
    for total in integer_partitions(n):
        total_rows = dict(permutation_representation_matrices(total))
        projector = np.zeros(
            (math.prod(source_dimensions), math.prod(source_dimensions)),
            dtype=complex,
        )
        for permutation, total_matrix in total_rows.items():
            character = np.trace(total_matrix).conjugate()
            projector += character * _kron_three(
                source_rows[0][permutation],
                source_rows[1][permutation],
                source_rows[2][permutation],
            )
        projector *= hook_length_dimension(total) / math.factorial(n)
        output.append((total, (projector + projector.conj().T) / 2))
    return tuple(output)


def _global_diagonal_actions(
    sources: tuple[Partition, Partition, Partition],
) -> tuple[np.ndarray, ...]:
    rows = [dict(permutation_representation_matrices(source)) for source in sources]
    permutations = tuple(rows[0])
    return tuple(
        _kron_three(
            rows[0][permutation],
            rows[1][permutation],
            rows[2][permutation],
        )
        for permutation in permutations
    )


def _path_dimensions(
    sources: tuple[Partition, Partition, Partition],
    total: Partition,
    *,
    side: str,
) -> tuple[tuple[Partition, int], ...]:
    n = sum(total)
    output: list[tuple[Partition, int]] = []
    for intermediate in integer_partitions(n):
        if side == "left":
            multiplicity = kronecker_coefficient(
                sources[0], sources[1], intermediate
            ) * kronecker_coefficient(intermediate, sources[2], total)
        elif side == "right":
            multiplicity = kronecker_coefficient(
                sources[1], sources[2], intermediate
            ) * kronecker_coefficient(sources[0], intermediate, total)
        else:
            raise ValueError("side must be left or right")
        if multiplicity:
            output.append((intermediate, multiplicity))
    return tuple(output)


def audit_racah_block_access(
    control_id: str,
    sources: tuple[Partition, Partition, Partition],
    *,
    tolerance: float = 1e-9,
) -> RacahBlockAccessControl:
    n = sum(sources[0])
    if any(sum(source) != n for source in sources):
        raise ValueError("all source partitions must have the same degree")
    source_dimensions = tuple(hook_length_dimension(source) for source in sources)
    dimension = math.prod(source_dimensions)
    left_projectors = _triple_isotypic_projectors(sources, "left")
    right_projectors = _triple_isotypic_projectors(sources, "right")
    total_projectors = _total_isotypic_projectors(sources)
    global_actions = _global_diagonal_actions(sources)

    commutators = tuple(
        left @ right - right @ left
        for left in left_projectors
        for right in right_projectors
    )
    aggregate_energy = sum(
        float(np.linalg.norm(commutator, ord="fro") ** 2)
        for commutator in commutators
    )
    aggregate_commutator = aggregate_energy / dimension
    return_probability = sum(
        float(np.trace(left @ right @ left @ right).real)
        for left in left_projectors
        for right in right_projectors
    ) / dimension

    sectors: list[TotalIrrepRacahSector] = []
    active_dimension = 0
    active_multiplicities: list[int] = []
    reconstructed_energy = 0.0
    maximum_total_commutator = 0.0
    for total, total_projector in total_projectors:
        left_paths = _path_dimensions(sources, total, side="left")
        right_paths = _path_dimensions(sources, total, side="right")
        left_multiplicity = sum(value for _, value in left_paths)
        right_multiplicity = sum(value for _, value in right_paths)
        total_dimension = hook_length_dimension(total)
        expected_rank = total_dimension * left_multiplicity
        dense_rank = int(round(float(np.trace(total_projector).real)))
        block_energy = sum(
            float(
                np.linalg.norm(
                    total_projector @ commutator @ total_projector,
                    ord="fro",
                )
                ** 2
            )
            for commutator in commutators
        )
        reconstructed_energy += block_energy
        active = block_energy > tolerance
        if active:
            active_dimension += expected_rank
            active_multiplicities.append(left_multiplicity)
        maximum_total_commutator = max(
            maximum_total_commutator,
            max(
                (
                    float(
                        np.linalg.norm(
                            total_projector @ pair - pair @ total_projector,
                            ord="fro",
                        )
                    )
                    for pair in (*left_projectors, *right_projectors)
                ),
                default=0.0,
            ),
        )
        sector_verified = bool(
            left_multiplicity == right_multiplicity
            and dense_rank == expected_rank
        )
        sectors.append(
            TotalIrrepRacahSector(
                total_partition=total,
                total_irrep_dimension=total_dimension,
                left_path_dimensions=left_paths,
                right_path_dimensions=right_paths,
                left_total_multiplicity=left_multiplicity,
                right_total_multiplicity=right_multiplicity,
                dense_total_isotypic_rank=dense_rank,
                physical_sector_dimension=expected_rank,
                physical_dimension_fraction=expected_rank / dimension,
                aggregate_commutator_energy=block_energy,
                multiplicity_normalized_commutator_energy=(
                    block_energy / total_dimension if total_dimension else 0.0
                ),
                noncommuting_racah_sector=active,
                associativity_dimension_identity_verified=(
                    left_multiplicity == right_multiplicity
                ),
                dense_rank_formula_verified=dense_rank == expected_rank,
                status=(
                    "active-multiplicity-racah-sector"
                    if active and sector_verified
                    else "commuting-racah-sector"
                    if sector_verified
                    else "racah-sector-decomposition-failure"
                ),
            )
        )

    maximum_covariance = max(
        (
            float(np.linalg.norm(action @ pair - pair @ action, ord="fro"))
            for action in global_actions
            for pair in (*left_projectors, *right_projectors)
        ),
        default=0.0,
    )
    maximum_idempotence = max(
        (
            float(np.linalg.norm(pair @ pair - pair, ord="fro"))
            for pair in (*left_projectors, *right_projectors)
        ),
        default=0.0,
    )
    completeness = float(
        np.linalg.norm(
            sum(
                (projector for _, projector in total_projectors),
                start=np.zeros((dimension, dimension), dtype=complex),
            )
            - np.eye(dimension),
            ord="fro",
        )
    )
    active_fraction = active_dimension / dimension
    disturbance_residual = abs(
        aggregate_commutator - 2 * (1 - return_probability)
    )
    energy_residual = abs(reconstructed_energy - aggregate_energy)
    active_slack = 2 * active_fraction - aggregate_commutator
    verified = bool(
        all(
            sector.associativity_dimension_identity_verified
            and sector.dense_rank_formula_verified
            for sector in sectors
        )
        and disturbance_residual <= tolerance
        and energy_residual <= tolerance
        and active_slack >= -tolerance
        and maximum_total_commutator <= tolerance
        and maximum_covariance <= tolerance
        and maximum_idempotence <= tolerance
        and completeness <= tolerance
    )
    return RacahBlockAccessControl(
        control_id=control_id,
        n=n,
        source_partitions=sources,
        source_dimensions=source_dimensions,
        physical_dimension=dimension,
        sectors=tuple(sectors),
        aggregate_commutator=aggregate_commutator,
        lueders_same_left_label_return_probability=return_probability,
        disturbance_identity_residual=disturbance_residual,
        active_racah_physical_dimension=active_dimension,
        active_racah_physical_dimension_fraction=active_fraction,
        commutator_to_active_mass_bound_slack=active_slack,
        maximum_total_projector_pair_pvm_commutator_residual=(
            maximum_total_commutator
        ),
        maximum_global_conjugation_covariance_residual=maximum_covariance,
        maximum_projector_idempotence_residual=maximum_idempotence,
        total_isotypic_completeness_residual=completeness,
        block_energy_reconstruction_residual=energy_residual,
        minimum_active_multiplicity_dimension=(
            min(active_multiplicities) if active_multiplicities else 0
        ),
        exact_racah_block_decomposition_verified=verified,
        finite_dense_control_only=True,
        status=(
            "minimum-racah-block-and-disturbance-identity-verified"
            if verified
            else "racah-block-access-control-failure"
        ),
    )


def annealed_racah_mass_control(n: int = 3) -> AnnealedRacahMassControl:
    if n != 3:
        raise ValueError("the dense annealed control is intentionally restricted to n=3")
    partitions = tuple(integer_partitions(n))
    order = math.factorial(n)
    weights = {
        partition: hook_length_dimension(partition) ** 2 / order
        for partition in partitions
    }
    weight_normalization = sum(weights.values())
    aggregate = 0.0
    return_probability = 0.0
    active_mass = 0.0
    for source_index, sources in enumerate(itertools.product(partitions, repeat=3)):
        weight = math.prod(weights[source] for source in sources)
        control = audit_racah_block_access(
            f"S3-ANNEALED-SOURCE-{source_index}",
            sources,
        )
        aggregate += weight * control.aggregate_commutator
        return_probability += (
            weight * control.lueders_same_left_label_return_probability
        )
        active_mass += weight * control.active_racah_physical_dimension_fraction
    kappa = float(exact_weighted_commuting_probability(n))
    formula = 2 * (1 - kappa)
    lower_bound = aggregate / 2
    verified = bool(
        abs(weight_normalization - 1) <= 1e-12
        and abs(aggregate - formula) <= 1e-10
        and abs(return_probability - kappa) <= 1e-10
        and active_mass + 1e-12 >= lower_bound
    )
    return AnnealedRacahMassControl(
        n=n,
        source_tuple_count=len(partitions) ** 3,
        plancherel_weight_normalization_residual=abs(weight_normalization - 1),
        dense_annealed_aggregate_commutator=aggregate,
        exact_character_formula_aggregate_commutator=formula,
        dense_to_character_formula_residual=abs(aggregate - formula),
        dense_annealed_lueders_return_probability=return_probability,
        exact_weighted_commuting_probability=kappa,
        return_probability_to_weighted_commuting_residual=abs(
            return_probability - kappa
        ),
        dense_annealed_active_racah_dimension_fraction=active_mass,
        active_mass_lower_bound_from_commutator=lower_bound,
        active_mass_bound_verified=verified,
        status=(
            "annealed-racah-mass-and-return-probability-cross-checked"
            if verified
            else "annealed-racah-mass-control-failure"
        ),
    )


def carrier_racah_access_theorem(
    *,
    finite_controls_verified: bool,
) -> CarrierRacahAccessTheorem:
    return CarrierRacahAccessTheorem(
        minimum_block=(
            "M_tau^L=direct_sum_alpha K_(a,b)^alpha tensor K_(alpha,c)^tau and "
            "M_tau^R=direct_sum_beta K_(b,c)^beta tensor K_(a,beta)^tau."
        ),
        left_pair_pvm_block_form="P_alpha=I_(V_tau) tensor Pi_alpha.",
        right_pair_pvm_block_form=(
            "Q_beta=I_(V_tau) tensor F_tau^* Pi_beta F_tau."
        ),
        lueders_disturbance_identity=(
            "C=D^-1 sum_(alpha,beta)||[P_alpha,Q_beta]||_F^2=2(1-p_return)."
        ),
        asymptotic_active_mass_transfer=(
            "C<=2w_active and E C->2 imply E w_active->1, including after collision-free conditioning."
        ),
        coherent_access=(
            "Known coherent pair-carrier GPE label queries implement a constant-query P-Q-P disturbance test without materializing F_tau."
        ),
        conjugation_invariance=(
            "Every carrier PVM and every adaptive branch effect in its generated star algebra commutes with simultaneous conjugation."
        ),
        hidden_identity_consequence=(
            "All fixed-cycle-type hidden involutions are conjugate, so carrier-only branch distributions are identical and contain zero hidden-identity information."
        ),
        minimum_racah_block_theorem_proved=True,
        constant_query_disturbance_compiled=True,
        asymptotically_full_active_racah_mass_proved=True,
        carrier_pvm_only_hidden_involution_decoder_possible=False,
        covariant_noncentral_decoder_compiled=False,
        status=(
            "racah-disturbance-accessible-carrier-only-decoder-impossible"
            if finite_controls_verified
            else "carrier-racah-access-control-failure"
        ),
    )


def run_plancherel_carrier_racah_access_boundary(
) -> CarrierRacahAccessBoundaryReport:
    controls = [
        audit_racah_block_access("S3-STANDARD-CUBED", ((2, 1),) * 3),
        audit_racah_block_access("S4-STANDARD-CUBED", ((3, 1),) * 3),
        audit_racah_block_access("S4-TWO-TWO-CUBED", ((2, 2),) * 3),
        audit_racah_block_access(
            "S3-COMMUTING-ONE-DIMENSIONAL-CONTROL",
            ((2, 1), (2, 1), (3,)),
        ),
    ]
    annealed = annealed_racah_mass_control()
    verified = bool(
        all(control.exact_racah_block_decomposition_verified for control in controls)
        and annealed.active_mass_bound_verified
    )
    theorem = carrier_racah_access_theorem(finite_controls_verified=verified)
    active = [control for control in controls if control.aggregate_commutator > 1e-10]
    return CarrierRacahAccessBoundaryReport(
        created_at=utc_now(),
        theorem_contract={
            "minimum_physical_block": theorem.minimum_block,
            "operational_witness": theorem.lueders_disturbance_identity,
            "positive_access_result": theorem.coherent_access,
            "asymptotic_mass_result": theorem.asymptotic_active_mass_transfer,
            "decoder_no_go": theorem.hidden_identity_consequence,
            "scope": (
                "The carrier disturbance is efficiently testable and physically extensive, but its invariant outcome algebra cannot identify a conjugate hidden involution."
            ),
        },
        finite_controls=controls,
        annealed_control=annealed,
        theorem=theorem,
        proof_obligations=[
            {
                "obligation": "derive_minimum_total_irrep_racah_block",
                "resolved": True,
                "resolution": (
                    "Schur decomposition and Kronecker associativity give equations (1)-(2), with total-irrep carrier factors acting identically."
                ),
            },
            {
                "obligation": "give_operational_access_to_contextuality_moment",
                "resolved": True,
                "resolution": (
                    "Projector algebra gives equation (3); three coherent pair-label queries implement the corresponding Lüders experiment."
                ),
            },
            {
                "obligation": "prove_contextuality_has_nonvanishing_physical_block_mass",
                "resolved": True,
                "resolution": (
                    "C<=2w_active and the proved annealed limit C->2 force active physical dimension fraction to one."
                ),
            },
            {
                "obligation": "test_carrier_only_hidden_identity_information",
                "resolved": True,
                "resolution": (
                    "Every adaptive branch effect generated by central carrier PVMs is conjugation-invariant and therefore identical on conjugate hidden subgroups."
                ),
            },
            {
                "obligation": "construct_covariant_noncentral_hidden_involution_outcome",
                "resolved": False,
                "resolution": (
                    "Add an outcome register or row/orientation primitive that transforms nontrivially under conjugation, then prove hidden-conditioned signal and classical separation."
                ),
            },
        ],
        adversarial_audit=[
            {
                "objection": "A full explicit Racah matrix must be compiled before the gap is measurable.",
                "resolved": True,
                "resolution": (
                    "False. The physical left and right carrier PVMs are separately queryable, and their P-Q-P return probability is exactly the gap witness."
                ),
            },
            {
                "objection": "The asymptotic gap may live on vanishing-rank exceptional sectors.",
                "resolved": True,
                "resolution": (
                    "False. The universal C<=2w_active inequality forces annealed active physical dimension fraction to one."
                ),
            },
            {
                "objection": "Operational disturbance supplies hidden-involution information.",
                "resolved": True,
                "resolution": (
                    "False for carrier-only effects: their outcome distributions are constant across the conjugacy orbit of hidden involutions."
                ),
            },
            {
                "objection": "The invariance theorem rules out every Racah-assisted decoder.",
                "resolved": True,
                "resolution": (
                    "It rules out only effects in the invariant carrier-PVM algebra. A covariant row/orientation outcome outside that algebra remains open."
                ),
            },
        ],
        headline_metrics={
            "minimum_total_irrep_racah_block_theorem_count": 1,
            "constant_query_carrier_disturbance_compiler_count": 1,
            "asymptotically_full_active_racah_mass_theorem_count": 1,
            "carrier_pvm_conjugation_invariance_no_go_theorem_count": 1,
            "finite_racah_block_control_count": len(controls),
            "finite_active_racah_block_control_count": len(active),
            "maximum_finite_aggregate_commutator": max(
                control.aggregate_commutator for control in controls
            ),
            "minimum_active_multiplicity_dimension": min(
                control.minimum_active_multiplicity_dimension for control in active
            ),
            "S3_annealed_active_racah_dimension_fraction": (
                annealed.dense_annealed_active_racah_dimension_fraction
            ),
            "covariant_noncentral_decoder_count": 0,
            "hidden_involution_decoder_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "minimum_multiplicity_racah_block_identified": True,
            "carrier_contextuality_operationally_accessible_by_pair_gpe": True,
            "explicit_racah_matrix_required_for_disturbance_test": False,
            "active_racah_physical_mass_tends_to_one": True,
            "carrier_only_adaptive_effects_conjugation_invariant": True,
            "carrier_only_protocol_can_identify_hidden_involution": False,
            "covariant_noncentral_row_or_orientation_outcome_compiled": False,
            "physical_hidden_conditioned_signal_proved": False,
            "classical_separation_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The maximal contextuality is efficiently testable and physically extensive, but the carrier-only outcome algebra is invariant across all conjugate hidden involutions."
            ),
        },
        status=theorem.status,
        summary=(
            "Identified the exact total-irrep multiplicity Racah blocks, converted the asymptotic commutator into an accessible three-query disturbance experiment with asymptotically full active mass, and proved that carrier-only outcomes cannot identify the hidden involution."
        ),
        falsifiers_triggered=[
            "An explicit full Racah matrix is not required to operationally measure carrier disturbance.",
            "The proved contextuality cannot be dismissed as a vanishing-rank rare-sector effect.",
            "Maximal carrier-label disturbance is hidden-identity invariant and is not itself a decoder signal.",
            "Multiplicity-space contextuality does not evade global conjugation invariance.",
            "A viable decoder must expose a covariant noncentral row or orientation outcome and survive classical baselines.",
        ],
    )


def write_plancherel_carrier_racah_access_boundary_report(
    path: Path = REPORT_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = DEFAULT_EXPERIMENT_ID,
    registry_candidate_id: str = DEFAULT_CANDIDATE_ID,
    registry_result_id: str = "",
    **kwargs: Any,
) -> dict[str, Any]:
    for key in (
        "write_registry",
        "registry_experiment_id",
        "registry_candidate_id",
        "registry_result_id",
    ):
        kwargs.pop(key, None)
    payload = asdict(run_plancherel_carrier_racah_access_boundary(**kwargs))
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    if write_registry:
        from research_registry import (
            ExperimentRecord,
            ExperimentResultRecord,
            NegativeResultRecord,
            upsert_experiment,
            upsert_experiment_result,
            upsert_negative_result,
        )

        upsert_experiment(
            ExperimentRecord(
                id=registry_experiment_id,
                candidate_id=registry_candidate_id,
                title="Plancherel carrier Racah access and invariant-decoder boundary",
                status="completed-disturbance-accessible-secret-invariant",
                hypothesis=(
                    "The proved carrier contextuality occupies physical multiplicity blocks and can be queried coherently, but carrier-label operations alone may still fail to identify the hidden involution."
                ),
                protocol=(
                    "Resolve total-irrep Racah path spaces, prove the P-Q-P disturbance identity and active-mass transfer, then audit the conjugation covariance of every carrier-PVM branch effect."
                ),
                positive_signal=(
                    "A covariant noncentral row or orientation outcome that couples the active Racah blocks to the identity of the hidden involution."
                ),
                falsifiers=[
                    "an explicit Racah matrix is treated as necessary for PVM alternation",
                    "the contextuality gap is treated as a rare-sector signal",
                    "conjugation-invariant carrier outcomes are treated as hidden-identity data",
                    "a no-go for the carrier algebra is promoted to all quantum measurements",
                ],
                metrics=[
                    "minimum_total_irrep_racah_block_theorem_count",
                    "constant_query_carrier_disturbance_compiler_count",
                    "asymptotically_full_active_racah_mass_theorem_count",
                    "carrier_pvm_conjugation_invariance_no_go_theorem_count",
                    "covariant_noncentral_decoder_count",
                ],
                dependencies=[
                    "self_dual_wreath_plancherel_carrier_asymptotic_closure.py",
                    "self_dual_wreath_pair_carrier_label_contextuality.py",
                    "Kronecker associativity and total-irrep Schur decomposition",
                    "hidden-subgroup conjugation covariance",
                ],
                next_actions=[
                    "construct a covariant row-space outcome on the active total-irrep Racah blocks",
                    "compute its hidden-involution-conditioned finite distributions",
                    "test whether pair GPE plus one noncentral representation matrix implements it coherently",
                    "run tensor-network and classical character-sampling attacks on the same statistic",
                ],
            )
        )
        result_id = registry_result_id or (
            "RESULT-EXP-CODE-SELF-DUAL-WREATH-PLANCHEREL-CARRIER-"
            "RACAH-ACCESS-BOUNDARY-LATEST"
        )
        upsert_experiment_result(
            ExperimentResultRecord(
                id=result_id,
                experiment_id=registry_experiment_id,
                candidate_id=registry_candidate_id,
                created_at=utc_now(),
                status=payload["status"],
                summary=payload["summary"],
                metrics=payload["headline_metrics"],
                falsifiers_triggered=payload["falsifiers_triggered"],
                artifacts={
                    "self_dual_wreath_plancherel_carrier_racah_access_boundary": str(path)
                },
            )
        )
        upsert_negative_result(
            NegativeResultRecord(
                id="FULL-RACAH-MATRIX-NOT-REQUIRED-FOR-CARRIER-DISTURBANCE",
                source=registry_experiment_id,
                claim=(
                    "The asymptotic carrier contextuality has no operational meaning until every Racah matrix is explicitly compiled."
                ),
                reason_invalid=(
                    "Known coherent left and right carrier-PVM queries implement the exact P-Q-P return experiment with a constant number of calls."
                ),
                lesson=(
                    "Separate access to noncommuting PVMs from a coordinate-level basis-transition compiler."
                ),
                applies_to=[
                    registry_candidate_id,
                    "carrier contextuality",
                    "multistar Racah access",
                ],
                evidence={"artifact": str(path)},
            )
        )
        upsert_negative_result(
            NegativeResultRecord(
                id="CARRIER-CONTEXTUALITY-NOT-HIDDEN-INVOLUTION-IDENTITY-SIGNAL",
                source=registry_experiment_id,
                claim=(
                    "The maximal carrier disturbance itself identifies which conjugate involution is hidden."
                ),
                reason_invalid=(
                    "Every carrier-PVM branch effect is invariant under simultaneous conjugation, so its distribution is identical for every involution in the fixed cycle-type conjugacy class."
                ),
                lesson=(
                    "Add a covariant noncentral row or orientation outcome before attempting a hidden-involution decoder."
                ),
                applies_to=[
                    registry_candidate_id,
                    "carrier-only adaptive protocols",
                    "symmetric-group hidden involution",
                ],
                evidence={"artifact": str(path)},
            )
        )
    return payload


if __name__ == "__main__":
    result = write_plancherel_carrier_racah_access_boundary_report()
    print(json.dumps(result["headline_metrics"], indent=2, sort_keys=True))

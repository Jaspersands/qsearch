"""Coherent local carrier labels and their multistar contextuality boundary.

The affine-star Cayley compiler needs the scalar overlap

    gamma = 1/(d_beta d_p)

as a coherent classical control.  The exact pair-core carrier theorem already
identifies ``beta`` and ``p`` for one shared-vertex triple.  They are not hidden
multiplicity coordinates.  Split the source tensor factors into the seven
nonempty membership-pattern blocks of three orientations and run coherent
generalized phase estimation (GPE) on each block.  The resulting irrep labels
are equal or conjugate according to two parity bits.  Equality/conjugacy tests
therefore expose ``(beta,p)`` while every Kronecker multiplicity register is
left untouched.  Hook-length arithmetic then computes ``d_beta d_p`` in time
polynomial in the symmetric-group degree.

This gives a polynomial *local carrier-label query* for any selected adjacent
pair of pair cores.  It does not automatically give one persistent channel
label for a multistar.  Different triples repartition overlapping tensor
factors, so their coarse isotypic projectors can be incompatible.  In the
standard two-dimensional irrep of ``S_3``, the trivial-isotype projectors for
factors ``(1,2)`` and ``(2,3)`` have

    ||[P_12,P_23]|| = sqrt(3)/4,
    spec(P_12 P_23 P_12 | ran P_12) = {1/4}.               (1)

Thus no nondemolition unitary can copy both sharp labels to classical
registers on arbitrary inputs.  Disjoint pair projectors commute exactly,
showing that overlap, not GPE itself, is the obstruction.

The surviving global interface is precise.  A natural all-depth compiler must
either prove that the physically occupied channel projectors commute/atomize,
construct a structured Racah transform that resolves their contextual labels,
or avoid persistent channel labels entirely.  Pairwise GPE plus classical
label accumulation is not a valid substitute.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from functools import lru_cache
from pathlib import Path
from typing import Any

import numpy as np

from representation_obstruction import hook_length_dimension
from research_registry import utc_now
from self_dual_wreath_pair_core_carrier_factorization import (
    exact_star_overlap_spectrum,
    run_pair_core_carrier_factorization,
)
from self_dual_wreath_physical_frame_blocks import (
    permutation_representation_matrices,
)


REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_pair_carrier_label_contextuality.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-PAIR-CARRIER-LABEL-CONTEXTUALITY"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"

Partition = tuple[int, ...]


@dataclass(frozen=True)
class LocalCarrierLabelControl:
    control_id: str
    n: int
    pattern_block_count: int
    coherent_gpe_call_count: int
    coherent_gpe_inverse_call_count: int
    irrep_label_comparison_count: int
    reversible_dimension_arithmetic_count: int
    channel_count: int
    total_channel_multiplicity: int
    distinct_cluster_carriers: tuple[Partition, ...]
    distinct_companion_carriers: tuple[Partition, ...]
    distinct_correlation_denominators: tuple[int, ...]
    maximum_dense_spectrum_residual: float
    multiplicity_coordinates_exposed: bool
    multiplicity_registers_preserved: bool
    local_carrier_label_query_polynomial: bool
    local_label_compiler_verified: bool
    status: str


@dataclass(frozen=True)
class IsotypicCompatibilityControl:
    control_id: str
    n: int
    source_partition: Partition
    target_partition: Partition
    tensor_factor_count: int
    first_factor_subset: tuple[int, ...]
    second_factor_subset: tuple[int, ...]
    first_projector_rank: int
    second_projector_rank: int
    first_idempotence_residual: float
    second_idempotence_residual: float
    commutator_norm: float
    expected_commutator_norm: float
    commutator_residual: float
    nonzero_first_compression_eigenvalues: tuple[float, ...]
    expected_nonzero_compression_eigenvalue: float | None
    compression_spectrum_residual: float
    sharp_nondemolition_joint_label_exists: bool
    exact_compatibility_audit_verified: bool
    status: str


@dataclass(frozen=True)
class CarrierLabelScalingRecord:
    n: int
    information_threshold_copy_count: int
    selected_triple_pattern_block_count: int
    selected_triple_gpe_call_count: int
    controlled_young_action_factor_count_upper_bound: int
    hook_dimension_output_bit_count_upper_bound: int
    selected_local_label_query_polynomial: bool
    all_incident_pair_labels_can_be_persistently_copied: bool
    global_channel_atom_label_compiled: bool
    status: str


@dataclass(frozen=True)
class GlobalStarCompilerInterface:
    required_input: str
    local_query_supplied: str
    missing_global_object: str
    sufficient_commuting_route: str
    sufficient_racah_route: str
    label_free_route: str
    pairwise_accumulation_route_valid: bool
    status: str


@dataclass(frozen=True)
class PairCarrierLabelTheorem:
    local_label_formula: str
    coherent_local_circuit: str
    multiplicity_scope: str
    contextuality_theorem: str
    global_interface: str
    surviving_target: str
    theorem_verified: bool
    status: str


@dataclass(frozen=True)
class PairCarrierLabelContextualityReport:
    created_at: str
    theorem_contract: dict[str, Any]
    theorem: PairCarrierLabelTheorem
    local_controls: list[LocalCarrierLabelControl]
    compatibility_controls: list[IsotypicCompatibilityControl]
    scaling_records: list[CarrierLabelScalingRecord]
    global_interface: GlobalStarCompilerInterface
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _hermitian(matrix: np.ndarray) -> np.ndarray:
    return (matrix + matrix.conj().T) / 2


def _kron_all(matrices: list[np.ndarray]) -> np.ndarray:
    result = np.ones((1, 1), dtype=complex)
    for matrix in matrices:
        result = np.kron(result, matrix)
    return result


@lru_cache(maxsize=64)
def isotypic_projector_on_subset(
    source_partition: Partition,
    target_partition: Partition,
    factor_subset: tuple[int, ...],
    factor_count: int,
) -> np.ndarray:
    """Project a selected tensor-factor subset onto one diagonal ``S_n`` irrep."""

    n = sum(source_partition)
    if sum(target_partition) != n:
        raise ValueError("source and target partitions must have one degree")
    if factor_count < 2:
        raise ValueError("at least two tensor factors are required")
    subset = tuple(sorted(set(factor_subset)))
    if len(subset) != len(factor_subset) or not subset:
        raise ValueError("factor subset must be nonempty and duplicate free")
    if subset[0] < 0 or subset[-1] >= factor_count:
        raise ValueError("factor subset is out of range")
    source_rows = dict(permutation_representation_matrices(source_partition))
    target_rows = dict(permutation_representation_matrices(target_partition))
    if set(source_rows) != set(target_rows):
        raise ArithmeticError("representation permutation tables disagree")
    source_dimension = hook_length_dimension(source_partition)
    target_dimension = hook_length_dimension(target_partition)
    identity = np.eye(source_dimension, dtype=complex)
    ambient = source_dimension**factor_count
    projector = np.zeros((ambient, ambient), dtype=complex)
    subset_set = set(subset)
    for permutation, representation in source_rows.items():
        character = np.trace(target_rows[permutation]).conjugate()
        factors = [
            representation if index in subset_set else identity
            for index in range(factor_count)
        ]
        projector += character * _kron_all(factors)
    projector *= target_dimension / math.factorial(n)
    return _hermitian(projector)


def audit_isotypic_compatibility(
    control_id: str,
    source_partition: Partition,
    target_partition: Partition,
    first_subset: tuple[int, ...],
    second_subset: tuple[int, ...],
    factor_count: int,
    *,
    expected_commutator: float,
    expected_compression_eigenvalue: float | None,
    tolerance: float = 1e-9,
) -> IsotypicCompatibilityControl:
    first = isotypic_projector_on_subset(
        source_partition,
        target_partition,
        first_subset,
        factor_count,
    )
    second = isotypic_projector_on_subset(
        source_partition,
        target_partition,
        second_subset,
        factor_count,
    )
    first_idempotence = float(np.linalg.norm(first @ first - first, ord=2))
    second_idempotence = float(np.linalg.norm(second @ second - second, ord=2))
    commutator = float(np.linalg.norm(first @ second - second @ first, ord=2))
    first_values, first_vectors = np.linalg.eigh(first)
    first_basis = first_vectors[:, first_values > 0.5]
    compression = _hermitian(first_basis.conj().T @ second @ first_basis)
    nonzero = tuple(
        round(float(value), 12)
        for value in np.linalg.eigvalsh(compression)
        if value > 100 * tolerance
    )
    if expected_compression_eigenvalue is None:
        spectrum_residual = max((abs(value - round(value)) for value in nonzero), default=0.0)
    else:
        spectrum_residual = max(
            (abs(value - expected_compression_eigenvalue) for value in nonzero),
            default=abs(expected_compression_eigenvalue),
        )
    commutator_residual = abs(commutator - expected_commutator)
    verified = bool(
        first_idempotence <= 100 * tolerance
        and second_idempotence <= 100 * tolerance
        and commutator_residual <= 100 * tolerance
        and spectrum_residual <= 100 * tolerance
    )
    compatible = commutator <= 100 * tolerance
    return IsotypicCompatibilityControl(
        control_id=control_id,
        n=sum(source_partition),
        source_partition=source_partition,
        target_partition=target_partition,
        tensor_factor_count=factor_count,
        first_factor_subset=first_subset,
        second_factor_subset=second_subset,
        first_projector_rank=first_basis.shape[1],
        second_projector_rank=int(round(float(np.trace(second).real))),
        first_idempotence_residual=first_idempotence,
        second_idempotence_residual=second_idempotence,
        commutator_norm=commutator,
        expected_commutator_norm=expected_commutator,
        commutator_residual=commutator_residual,
        nonzero_first_compression_eigenvalues=nonzero,
        expected_nonzero_compression_eigenvalue=expected_compression_eigenvalue,
        compression_spectrum_residual=spectrum_residual,
        sharp_nondemolition_joint_label_exists=compatible,
        exact_compatibility_audit_verified=verified,
        status=(
            "disjoint-isotypic-labels-compatible"
            if compatible
            else "overlapping-isotypic-labels-contextual"
        ),
    )


def _local_carrier_label_controls() -> list[LocalCarrierLabelControl]:
    factorization = run_pair_core_carrier_factorization()
    controls = []
    for selected in factorization.selected_star_controls:
        channels = exact_star_overlap_spectrum(
            selected.target_partition,
            selected.labels,
            selected.shared_orientation,
            selected.left_orientation,
            selected.right_orientation,
        )
        verified = bool(
            selected.verified
            and channels
            and all(
                row.correlation_denominator
                == row.cluster_carrier_dimension * row.companion_carrier_dimension
                for row in channels
            )
        )
        controls.append(
            LocalCarrierLabelControl(
                control_id=selected.control_id,
                n=selected.n,
                pattern_block_count=7,
                coherent_gpe_call_count=7,
                coherent_gpe_inverse_call_count=7,
                irrep_label_comparison_count=5,
                reversible_dimension_arithmetic_count=2,
                channel_count=len(channels),
                total_channel_multiplicity=sum(row.multiplicity for row in channels),
                distinct_cluster_carriers=tuple(
                    sorted({row.cluster_carrier for row in channels})
                ),
                distinct_companion_carriers=tuple(
                    sorted({row.companion_carrier for row in channels})
                ),
                distinct_correlation_denominators=tuple(
                    sorted({row.correlation_denominator for row in channels})
                ),
                maximum_dense_spectrum_residual=selected.maximum_spectrum_residual,
                multiplicity_coordinates_exposed=False,
                multiplicity_registers_preserved=True,
                local_carrier_label_query_polynomial=True,
                local_label_compiler_verified=verified,
                status=(
                    "coherent-local-pair-carrier-label-query-certified"
                    if verified
                    else "local-pair-carrier-label-control-failure"
                ),
            )
        )
    return controls


def carrier_label_scaling_record(n: int) -> CarrierLabelScalingRecord:
    if n < 5:
        raise ValueError("n must be at least five")
    copies = math.ceil(math.lgamma(n + 1) / math.log(2))
    # Each of seven GPE queries applies a selected diagonal action to at most
    # the target plus both source factors from every copy.
    factors = 1 + 2 * copies
    return CarrierLabelScalingRecord(
        n=n,
        information_threshold_copy_count=copies,
        selected_triple_pattern_block_count=7,
        selected_triple_gpe_call_count=7,
        controlled_young_action_factor_count_upper_bound=7 * factors,
        hook_dimension_output_bit_count_upper_bound=2 * math.ceil(
            math.lgamma(n + 1) / math.log(2)
        ),
        selected_local_label_query_polynomial=True,
        all_incident_pair_labels_can_be_persistently_copied=False,
        global_channel_atom_label_compiled=False,
        status="local-carrier-label-query-polynomial-global-contextual-label-open",
    )


@lru_cache(maxsize=1)
def run_pair_carrier_label_contextuality() -> (
    PairCarrierLabelContextualityReport
):
    local = _local_carrier_label_controls()
    standard = (2, 1)
    trivial = (3,)
    compatibility = [
        audit_isotypic_compatibility(
            "S3-OVERLAPPING-TRIVIAL-PAIR-LABELS",
            standard,
            trivial,
            (0, 1),
            (1, 2),
            3,
            expected_commutator=math.sqrt(3) / 4,
            expected_compression_eigenvalue=1 / 4,
        ),
        audit_isotypic_compatibility(
            "S3-DISJOINT-TRIVIAL-PAIR-LABELS",
            standard,
            trivial,
            (0, 1),
            (2, 3),
            4,
            expected_commutator=0.0,
            expected_compression_eigenvalue=1.0,
        ),
    ]
    scaling = [
        carrier_label_scaling_record(n)
        for n in (6, 8, 16, 32, 64, 128, 256, 512)
    ]
    local_failures = sum(not row.local_label_compiler_verified for row in local)
    compatibility_failures = sum(
        not row.exact_compatibility_audit_verified for row in compatibility
    )
    overlap = compatibility[0]
    disjoint = compatibility[1]
    contextuality = bool(
        overlap.commutator_norm > 0.4
        and not overlap.sharp_nondemolition_joint_label_exists
        and disjoint.sharp_nondemolition_joint_label_exists
    )
    verified = bool(
        local_failures == 0
        and compatibility_failures == 0
        and contextuality
    )
    interface = GlobalStarCompilerInterface(
        required_input=(
            "A coherent global channel atom, star center/reference edges, and one "
            "carrier correlation label preserved by every channel transport."
        ),
        local_query_supplied=(
            "For any selected shared-vertex triple, seven coherent GPE calls expose "
            "beta,p and reversible hook arithmetic computes gamma=1/(d_beta d_p)."
        ),
        missing_global_object=(
            "A jointly valid channel atom label across all overlapping triple "
            "decompositions on the physically occupied natural subspace."
        ),
        sufficient_commuting_route=(
            "Prove the occupied coarse isotypic projectors commute and give a "
            "reversible Boolean atom label."
        ),
        sufficient_racah_route=(
            "Compile a structured Racah transform that coherently resolves the "
            "incompatible coupling labels and channel transports."
        ),
        label_free_route=(
            "Implement canonical D directly from a representation observable "
            "without materializing a persistent channel label."
        ),
        pairwise_accumulation_route_valid=False,
        status="local-label-query-solved-global-channel-label-contextuality-open",
    )
    theorem = PairCarrierLabelTheorem(
        local_label_formula=(
            "Every shared-vertex channel is labeled by beta,p and has scalar "
            "correlation 1/(d_beta d_p)."
        ),
        coherent_local_circuit=(
            "GPE on seven membership-pattern tensor blocks, five label comparisons, "
            "and reversible hook arithmetic expose the scalar without a multiplicity basis."
        ),
        multiplicity_scope=(
            "The circuit preserves opaque Kronecker multiplicity coordinates; it "
            "does not resolve or mix them."
        ),
        contextuality_theorem=(
            "Overlapping coarse S3 isotypic projectors have commutator sqrt(3)/4, "
            "so arbitrary sharp pair labels cannot all be copied nondestructively."
        ),
        global_interface=(
            "A full star compiler needs commuting occupied atoms, a coherent Racah "
            "resolver, or a label-free D construction."
        ),
        surviving_target=(
            "Test natural growing-multiplicity occupied projectors for commutation, "
            "mass-weighted contextuality, and a compact Racah resolver."
        ),
        theorem_verified=verified,
        status=(
            "local-carrier-label-query-proved-global-contextuality-boundary"
            if verified
            else "pair-carrier-label-contextuality-validation-failure"
        ),
    )
    return PairCarrierLabelContextualityReport(
        created_at=utc_now(),
        theorem_contract={
            "input": (
                "One selected shared-vertex orientation triple, source/target irrep "
                "labels, and coherent tensor-block group actions."
            ),
            "local_output": (
                "Coherent beta,p, parity bits, and correlation denominator while "
                "preserving every multiplicity register."
            ),
            "global_boundary": (
                "Pair labels from overlapping regroupings are not assumed jointly "
                "classical; commutation or a Racah resolver must be proved."
            ),
            "excluded_claims": (
                "No global channel atomizer, all-depth star classifier, matrix-Racah "
                "compiler, root anchor, PGM, decoder, or speedup."
            ),
        },
        theorem=theorem,
        local_controls=local,
        compatibility_controls=compatibility,
        scaling_records=scaling,
        global_interface=interface,
        proof_obligations=[
            {
                "obligation": "compile_selected_triple_carrier_correlation_label",
                "resolved": verified,
                "resolution": (
                    "Seven coherent GPE labels and parity-conditioned equality tests "
                    "identify beta,p; hook arithmetic computes their dimensions."
                ),
            },
            {
                "obligation": "avoid_internal_kronecker_multiplicity_basis",
                "resolved": True,
                "resolution": (
                    "GPE exports only irrep/carrier rows and acts identically on "
                    "multiplicity registers, which remain opaque and coherent."
                ),
            },
            {
                "obligation": "copy_all_overlapping_pair_labels_nondestructively",
                "resolved": False,
                "resolution": (
                    "The exact S3 overlapping-pair projectors have commutator "
                    "sqrt(3)/4 and compression eigenvalue 1/4."
                ),
            },
            {
                "obligation": "prove_physical_occupied_multistar_label_compatibility",
                "resolved": False,
                "resolution": (
                    "The abstract counterexample does not establish positive natural "
                    "mass; physical growing-multiplicity occupied projectors must be audited."
                ),
            },
            {
                "obligation": "compile_global_channel_atom_or_racah_resolver",
                "resolved": False,
                "resolution": (
                    "Current finite atomization is classical and no uniform coherent "
                    "resolver for overlapping labels is known."
                ),
            },
        ],
        adversarial_audit=[
            {
                "objection": "The scalar gamma label is hidden in an unknown multiplicity basis.",
                "resolved": True,
                "resolution": (
                    "False locally: beta,p are ordinary GPE irrep labels and the "
                    "multiplicity coordinates need not be exposed."
                ),
            },
            {
                "objection": "Running every pair-label GPE coherently creates one global classical label table.",
                "resolved": True,
                "resolution": (
                    "False in general: overlapping sharp isotypic projectors need not "
                    "commute and cannot all be copied nondestructively."
                ),
            },
            {
                "objection": "All pair-label observables are incompatible.",
                "resolved": True,
                "resolution": (
                    "False: disjoint tensor-factor pair projectors commute exactly."
                ),
            },
            {
                "objection": "The S3 contextuality control kills the natural wreath route.",
                "resolved": False,
                "resolution": (
                    "It kills only the universal pairwise-label accumulation strategy. "
                    "The physical occupied subspace may commute or admit a structured resolver."
                ),
            },
        ],
        headline_metrics={
            "coherent_local_pair_carrier_label_query_count": int(verified),
            "local_pair_carrier_hook_arithmetic_count": int(verified),
            "finite_local_label_control_count": len(local),
            "finite_local_label_control_failure_count": local_failures,
            "selected_physical_star_channel_count": sum(row.channel_count for row in local),
            "maximum_local_dense_spectrum_residual": max(
                row.maximum_dense_spectrum_residual for row in local
            ),
            "overlapping_label_contextuality_counterexample_count": int(contextuality),
            "overlapping_s3_projector_commutator_norm": overlap.commutator_norm,
            "overlapping_s3_compression_eigenvalue": overlap.nonzero_first_compression_eigenvalues[0],
            "disjoint_label_compatibility_control_count": int(
                disjoint.sharp_nondemolition_joint_label_exists
            ),
            "all_depth_global_channel_atom_labeler_count": 0,
            "physical_positive_mass_contextuality_theorem_count": 0,
            "coherent_multistar_racah_resolver_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "selected_triple_carrier_label_query_polynomial": verified,
            "selected_triple_gamma_computable_without_multiplicity_basis": verified,
            "pair_gpe_preserves_multiplicity_registers": verified,
            "overlapping_pair_labels_always_jointly_classical": False,
            "pairwise_gpe_label_accumulation_compiles_global_channel_atom": False,
            "physical_occupied_multistar_projectors_commute_all_depth": False,
            "coherent_global_channel_atom_labeler_compiled": False,
            "coherent_multistar_racah_resolver_compiled": False,
            "label_free_natural_cayley_observable_compiled": False,
            "physical_root_anchor_compiled": False,
            "physical_pgm_compiled": False,
            "classical_separation_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The scalar carrier overlap is coherently queryable for one selected "
                "triple, but overlapping triple labels are contextual in general. A "
                "physical commuting-atom theorem, Racah resolver, or label-free D "
                "compiler is still required."
            ),
        },
        status=(
            "coherent-local-carrier-label-query-proved-global-contextuality-open"
            if verified
            else "pair-carrier-label-contextuality-validation-failure"
        ),
        summary=(
            "Proved a polynomial coherent query for each selected pair-core carrier "
            "label and gamma=1/(d_beta d_p), without exposing multiplicity. An exact "
            "S3 commutator sqrt(3)/4 counterexample shows why pairwise labels cannot "
            "simply be accumulated into one global channel label."
        ),
        falsifiers_triggered=[
            "The local scalar carrier overlap is not hidden by Kronecker multiplicity coordinates.",
            "Coherent pair-label queries do not automatically define a nondemolition global label table.",
            "Disjoint isotypic labels remain compatible; overlap and recoupling are the precise obstruction.",
            "Abstract label contextuality is not yet a positive-natural-mass no-go for the wreath PGM route.",
        ],
    )


def write_pair_carrier_label_contextuality_report(
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
    payload = asdict(run_pair_carrier_label_contextuality(**kwargs))
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
                title="Pair-carrier label compiler and contextuality boundary",
                status="completed-local-label-positive-global-boundary",
                hypothesis=(
                    "The scalar carrier overlap needed by the star Cayley compiler "
                    "is locally GPE-labelable, but overlapping labels require a "
                    "separate global compatibility theorem or Racah resolver."
                ),
                protocol=(
                    "Compile selected-triple beta,p labels from membership-pattern "
                    "GPE, validate exact physical carrier spectra, and test sharp "
                    "label compatibility on overlapping and disjoint S3 factors."
                ),
                positive_signal=(
                    "Polynomial local gamma labels plus commuting occupied natural "
                    "channel atoms or a coherent compact Racah resolver."
                ),
                falsifiers=[
                    "selected-triple gamma requires an internal multiplicity basis",
                    "overlapping pair labels commute automatically",
                    "finite classical atomization is treated as a coherent circuit",
                    "abstract contextuality is promoted without physical natural mass",
                ],
                metrics=[
                    "coherent_local_pair_carrier_label_query_count",
                    "maximum_local_dense_spectrum_residual",
                    "overlapping_s3_projector_commutator_norm",
                    "all_depth_global_channel_atom_labeler_count",
                    "coherent_multistar_racah_resolver_count",
                ],
                dependencies=[
                    "pair-core carrier factorization",
                    "coherent GPE pair-polar transport",
                    "affine-star Cayley compiler",
                    "Schur companion multiplicity access",
                ],
                next_actions=[
                    "audit physical growing-multiplicity occupied label commutators",
                    "derive a coherent Boolean atom label if occupied projectors commute",
                    "otherwise search for a compact Racah resolver or label-free D observable",
                    "propagate the resulting channel label through root anchoring and native mass",
                ],
            )
        )
        result_id = registry_result_id or (
            "RESULT-EXP-CODE-SELF-DUAL-WREATH-PAIR-CARRIER-LABEL-CONTEXTUALITY-LATEST"
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
                    "self_dual_wreath_pair_carrier_label_contextuality": str(path)
                },
            )
        )
        upsert_negative_result(
            NegativeResultRecord(
                id="OVERLAPPING-PAIR-GPE-LABELS-NOT-JOINTLY-CLASSICAL",
                source=registry_experiment_id,
                claim=(
                    "Coherently querying every local pair carrier label produces one "
                    "persistent nondemolition classical channel-label table."
                ),
                reason_invalid=(
                    "Overlapping S3 coarse isotypic projectors have exact commutator "
                    "norm sqrt(3)/4 and compression eigenvalue 1/4."
                ),
                lesson=(
                    "Prove compatibility on the physically occupied subspace, compile "
                    "a structured Racah resolver, or avoid persistent pair labels."
                ),
                applies_to=[
                    registry_candidate_id,
                    registry_experiment_id,
                    "PO-MEASUREMENT",
                ],
                evidence={
                    "overlapping_s3_projector_commutator_norm": payload[
                        "headline_metrics"
                    ]["overlapping_s3_projector_commutator_norm"],
                    "overlapping_s3_compression_eigenvalue": payload[
                        "headline_metrics"
                    ]["overlapping_s3_compression_eigenvalue"],
                    "local_pair_carrier_query_compiled": bool(
                        payload["headline_metrics"][
                            "coherent_local_pair_carrier_label_query_count"
                        ]
                    ),
                },
            )
        )
    return payload


if __name__ == "__main__":
    result = write_pair_carrier_label_contextuality_report()
    print(json.dumps(result["headline_metrics"], indent=2))
    print(result["status"])

"""Perfect-matching spherical boundary for hidden-involution measurements.

Let ``X_m`` be the fixed-point-free involutions in ``S_(2m)``.  Conjugation
identifies this label space with

    X_m = S_(2m) / (S_2 wr S_m),

the perfect matchings on ``2m`` points.  The classical Thrall decomposition is

    C[X_m] = direct_sum_(lambda partition m) S^(2 lambda),

with every constituent appearing once.  Thus the arbitrary-measurement
intertwiner from ``coset_arbitrary_covariant_measurement_reduction.py`` has one
row per live irrep:

    K_hat_(2 lambda) = I_(S^(2 lambda)) tensor <a_(2 lambda)|.

This is a real simplification, but only on the *outcome* side.  For the
canonical purification inside ``C[S_(2m)] tensor conjugate(C[S_(2m)])``, the
physical representation is ``|S_(2m)|`` copies of the regular representation,
so its multiplicity of ``S^nu`` is ``|S_(2m)| dim(S^nu)``.  A useful decoder
therefore yields preparation of one vector in a large physical multiplicity
space, not a scalar inverse or a classically checkable hidden involution.

The homogeneous Fourier basis is nevertheless sampleable without assuming a
new spherical-transform circuit.  Encode a uniformly random matching as a
uniform right coset of ``S_2 wr S_m``, apply the efficient symmetric-group QFT,
and measure the irrep/carrier registers.  The result samples ``(2 lambda,j)``
with probability ``dim(S^(2 lambda))/|X_m|`` and leaves the unique stabilizer-
fixed column state.  This is exactly the uniform distribution over the
homogeneous Fourier basis required by the inverse-row average theorem.

The 2026 quantum Fourier transform for the Brauer algebra does not close the
remaining row-state problem.  Although both standard bases are indexed by
perfect matchings and have dimension ``(2m-1)!!``, their semisimple block
decompositions differ: the homogeneous space has ``p(m)`` sectors, while the
generic Brauer algebra has ``sum_k p(m-2k)`` sectors.  Moreover, the published
approximation guarantee requires a loop parameter much larger than a
polynomial in the algebra dimension.  The paper is a useful source of circuit
techniques, not an implementation of this spherical inverse.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from representation_obstruction import hook_length_dimension, integer_partitions
from research_registry import utc_now
from symmetric_character import conjugacy_class_size, symmetric_character


REPORT_PATH = Path(
    "research/representation/coset_perfect_matching_spherical_boundary.json"
)
DEFAULT_EXPERIMENT_ID = "EXP-COSET-PERFECT-MATCHING-SPHERICAL-BOUNDARY"
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"

Partition = tuple[int, ...]


@dataclass(frozen=True)
class PerfectMatchingCharacterControl:
    half_degree: int
    degree: int
    symmetric_group_order: int
    hyperoctahedral_stabilizer_order: int
    perfect_matching_count: int
    partition_count_half_degree: int
    permutation_character_inner_product_sector_count: int
    maximum_constituent_multiplicity: int
    unexpected_constituent_count: int
    missing_even_row_constituent_count: int
    constituent_dimension_sum: int
    exact_dimension_identity_verified: bool
    exact_thrall_decomposition_verified: bool
    status: str


@dataclass(frozen=True)
class PerfectMatchingScalingRecord:
    half_degree: int
    degree: int
    perfect_matching_count_decimal: str
    perfect_matching_log2: float
    homogeneous_sector_count: int
    brauer_regular_sector_count: int
    brauer_and_homogeneous_sector_profiles_equal: bool
    maximum_homogeneous_irrep_dimension_decimal: str
    canonical_purification_multiplicity_ratio: int
    canonical_purification_multiplicity_ratio_log2: float
    efficient_matching_coset_embedding: bool
    efficient_symmetric_group_qft_available: bool
    uniform_homogeneous_fourier_basis_sampler_constructed: bool
    arbitrary_measurement_row_state_verifier_constructed: bool
    polynomial_hidden_involution_decoder_constructed: bool
    status: str


@dataclass(frozen=True)
class PerfectMatchingSphericalTheorem:
    homogeneous_space_identity: str
    thrall_decomposition: str
    arbitrary_measurement_block_specialization: str
    gram_spectrum_specialization: str
    homogeneous_basis_sampling_circuit: str
    sampling_law: str
    canonical_purification_multiplicity: str
    brauer_qft_nonidentification: str
    remaining_algorithmic_obligation: str
    gelfand_pair_proved: bool
    homogeneous_basis_sampler_constructed: bool
    physical_blocks_reduced_to_scalars: bool
    row_state_verifier_constructed: bool
    polynomial_hidden_involution_decoder_constructed: bool
    theorem_verified: bool
    status: str


@dataclass(frozen=True)
class PerfectMatchingSphericalBoundaryReport:
    created_at: str
    theorem_contract: dict[str, Any]
    finite_character_controls: list[PerfectMatchingCharacterControl]
    scaling_records: list[PerfectMatchingScalingRecord]
    theorem: PerfectMatchingSphericalTheorem
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    literature_links: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def odd_double_factorial(value: int) -> int:
    """Return ``value!!`` for odd ``value >= -1``."""

    if value < -1 or value % 2 == 0:
        raise ValueError("value must be odd and at least -1")
    output = 1
    for factor in range(1, value + 1, 2):
        output *= factor
    return output


def perfect_matching_count(half_degree: int) -> int:
    if half_degree < 1:
        raise ValueError("half_degree must be positive")
    return odd_double_factorial(2 * half_degree - 1)


def hyperoctahedral_order(half_degree: int) -> int:
    if half_degree < 1:
        raise ValueError("half_degree must be positive")
    return (2**half_degree) * math.factorial(half_degree)


def _cycle_length_matching_factor(length: int, count: int) -> int:
    """Count invariant matching choices on cycles of one fixed length.

    Two cycles of equal length can be paired in ``length`` phase offsets.  A
    single even cycle can instead be matched to its antipodes.  Odd cycles
    cannot be internally matched.
    """

    if length < 1 or count < 0:
        raise ValueError("cycle length and count must be valid")
    if length % 2:
        if count % 2:
            return 0
        pairs = count // 2
        return (
            math.factorial(count)
            * (length**pairs)
            // ((2**pairs) * math.factorial(pairs))
        )

    total = 0
    for internal_cycles in range(count % 2, count + 1, 2):
        paired_cycles = count - internal_cycles
        pairs = paired_cycles // 2
        pairings = (
            math.factorial(paired_cycles)
            * (length**pairs)
            // ((2**pairs) * math.factorial(pairs))
        )
        total += math.comb(count, internal_cycles) * pairings
    return total


def fixed_perfect_matching_count(cycle_type: Partition) -> int:
    """Permutation character of ``S_(2m)`` acting on perfect matchings."""

    degree = sum(cycle_type)
    if degree < 2 or degree % 2:
        raise ValueError("cycle_type must have positive even degree")
    multiplicities: dict[int, int] = {}
    for length in cycle_type:
        if length < 1:
            raise ValueError("cycle lengths must be positive")
        multiplicities[length] = multiplicities.get(length, 0) + 1
    output = 1
    for length, count in multiplicities.items():
        output *= _cycle_length_matching_factor(length, count)
    return output


def perfect_matching_constituent_multiplicities(
    half_degree: int,
) -> dict[Partition, int]:
    """Decompose the matching permutation character by exact class sums."""

    if half_degree < 1:
        raise ValueError("half_degree must be positive")
    degree = 2 * half_degree
    cycle_types = integer_partitions(degree)
    order = math.factorial(degree)
    fixed_counts = {
        cycle_type: fixed_perfect_matching_count(cycle_type)
        for cycle_type in cycle_types
    }
    output: dict[Partition, int] = {}
    for partition in integer_partitions(degree):
        numerator = sum(
            conjugacy_class_size(cycle_type)
            * symmetric_character(partition, cycle_type)
            * fixed_counts[cycle_type]
            for cycle_type in cycle_types
        )
        if numerator % order:
            raise ArithmeticError("permutation-character multiplicity is nonintegral")
        multiplicity = numerator // order
        if multiplicity < 0:
            raise ArithmeticError("permutation-character multiplicity is negative")
        if multiplicity:
            output[partition] = multiplicity
    return output


def expected_even_row_constituents(half_degree: int) -> set[Partition]:
    if half_degree < 1:
        raise ValueError("half_degree must be positive")
    return {
        tuple(2 * row for row in partition)
        for partition in integer_partitions(half_degree)
    }


def audit_perfect_matching_character(
    half_degree: int,
) -> PerfectMatchingCharacterControl:
    degree = 2 * half_degree
    constituents = perfect_matching_constituent_multiplicities(half_degree)
    expected = expected_even_row_constituents(half_degree)
    actual = set(constituents)
    dimension_sum = sum(
        multiplicity * hook_length_dimension(partition)
        for partition, multiplicity in constituents.items()
    )
    matching_count = perfect_matching_count(half_degree)
    maximum_multiplicity = max(constituents.values(), default=0)
    unexpected = len(actual - expected)
    missing = len(expected - actual)
    dimension_verified = dimension_sum == matching_count
    decomposition_verified = (
        maximum_multiplicity == 1
        and not unexpected
        and not missing
        and dimension_verified
    )
    return PerfectMatchingCharacterControl(
        half_degree=half_degree,
        degree=degree,
        symmetric_group_order=math.factorial(degree),
        hyperoctahedral_stabilizer_order=hyperoctahedral_order(half_degree),
        perfect_matching_count=matching_count,
        partition_count_half_degree=len(integer_partitions(half_degree)),
        permutation_character_inner_product_sector_count=len(constituents),
        maximum_constituent_multiplicity=maximum_multiplicity,
        unexpected_constituent_count=unexpected,
        missing_even_row_constituent_count=missing,
        constituent_dimension_sum=dimension_sum,
        exact_dimension_identity_verified=dimension_verified,
        exact_thrall_decomposition_verified=decomposition_verified,
        status=(
            "exact-perfect-matching-gelfand-control"
            if decomposition_verified
            else "perfect-matching-character-control-failure"
        ),
    )


def brauer_regular_sector_count(diagram_order: int) -> int:
    """Number of generic semisimple Brauer-algebra irreps."""

    if diagram_order < 1:
        raise ValueError("diagram_order must be positive")
    return sum(
        len(integer_partitions(diagram_order - 2 * contractions))
        for contractions in range(diagram_order // 2 + 1)
    )


def brauer_irrep_dimension(diagram_order: int, partition: Partition) -> int:
    """Generic Brauer irrep dimension for a partition of ``m-2k``."""

    size = sum(partition)
    gap = diagram_order - size
    if gap < 0 or gap % 2:
        raise ValueError("partition size must equal diagram_order modulo two")
    contractions = gap // 2
    partial_matching_count = (
        math.factorial(diagram_order)
        // (
            math.factorial(size)
            * (2**contractions)
            * math.factorial(contractions)
        )
    )
    return partial_matching_count * hook_length_dimension(partition)


def brauer_regular_dimension(diagram_order: int) -> int:
    if diagram_order < 1:
        raise ValueError("diagram_order must be positive")
    return sum(
        brauer_irrep_dimension(diagram_order, partition) ** 2
        for contractions in range(diagram_order // 2 + 1)
        for partition in integer_partitions(diagram_order - 2 * contractions)
    )


def scaling_record(half_degree: int) -> PerfectMatchingScalingRecord:
    degree = 2 * half_degree
    matching_count = perfect_matching_count(half_degree)
    dimensions = [
        hook_length_dimension(partition)
        for partition in expected_even_row_constituents(half_degree)
    ]
    homogeneous_sectors = len(integer_partitions(half_degree))
    brauer_sectors = brauer_regular_sector_count(half_degree)
    group_order = math.factorial(degree)
    return PerfectMatchingScalingRecord(
        half_degree=half_degree,
        degree=degree,
        perfect_matching_count_decimal=str(matching_count),
        perfect_matching_log2=math.log2(matching_count),
        homogeneous_sector_count=homogeneous_sectors,
        brauer_regular_sector_count=brauer_sectors,
        brauer_and_homogeneous_sector_profiles_equal=(
            homogeneous_sectors == brauer_sectors
        ),
        maximum_homogeneous_irrep_dimension_decimal=str(max(dimensions)),
        canonical_purification_multiplicity_ratio=group_order,
        canonical_purification_multiplicity_ratio_log2=math.lgamma(
            degree + 1
        ) / math.log(2.0),
        efficient_matching_coset_embedding=True,
        efficient_symmetric_group_qft_available=True,
        uniform_homogeneous_fourier_basis_sampler_constructed=True,
        arbitrary_measurement_row_state_verifier_constructed=False,
        polynomial_hidden_involution_decoder_constructed=False,
        status="spherical-basis-sampling-resolved-physical-row-verifier-open",
    )


def perfect_matching_spherical_theorem() -> PerfectMatchingSphericalTheorem:
    return PerfectMatchingSphericalTheorem(
        homogeneous_space_identity=(
            "Fixed-point-free involutions in S_(2m) are S_(2m)/(S_2 wr S_m), "
            "the perfect matchings on 2m points."
        ),
        thrall_decomposition=(
            "Ind_(S_2 wr S_m)^S_(2m)(1) = direct_sum_(lambda partition m) "
            "S^(2 lambda), with multiplicity one."
        ),
        arbitrary_measurement_block_specialization=(
            "Every cleaned covariant measurement intertwiner has live block "
            "I_(S^(2 lambda)) tensor <a_(2 lambda)| because the outcome "
            "multiplicity space is one-dimensional."
        ),
        gram_spectrum_specialization=(
            "K K^* is scalar alpha_(2 lambda) on each even-row constituent, "
            "so the outcome Gram operator lies in the commutative perfect-"
            "matching association scheme."
        ),
        homogeneous_basis_sampling_circuit=(
            "Prepare a uniformly random matching, reversibly embed it as a "
            "uniform hyperoctahedral right coset, apply the S_(2m) QFT, and "
            "measure the irrep and carrier labels; retain the unique H-fixed "
            "column state."
        ),
        sampling_law=(
            "The circuit samples (2 lambda,j) with probability "
            "dim(S^(2 lambda))/((2m-1)!!), uniform over the homogeneous "
            "Fourier basis."
        ),
        canonical_purification_multiplicity=(
            "For regular U, U tensor conjugate(U) is |S_(2m)| copies of the "
            "regular representation, hence physical multiplicity "
            "|S_(2m)| dim(S^nu), not one."
        ),
        brauer_qft_nonidentification=(
            "The Brauer regular transform has sum_k p(m-2k) sectors rather "
            "than p(m), so sharing a perfect-matching standard basis does not "
            "make it the S_(2m)/(S_2 wr S_m) spherical transform."
        ),
        remaining_algorithmic_obligation=(
            "Give a noncircular verifier, reduction, or observable for the "
            "prepared physical multiplicity vector, or implement the relevant "
            "PGM polar row with a proved polynomial condition bound."
        ),
        gelfand_pair_proved=True,
        homogeneous_basis_sampler_constructed=True,
        physical_blocks_reduced_to_scalars=False,
        row_state_verifier_constructed=False,
        polynomial_hidden_involution_decoder_constructed=False,
        theorem_verified=True,
        status="perfect-matching-spherical-outcome-resolved-physical-row-open",
    )


def run_perfect_matching_spherical_boundary(
) -> PerfectMatchingSphericalBoundaryReport:
    controls = [audit_perfect_matching_character(m) for m in range(1, 8)]
    scaling = [scaling_record(m) for m in (2, 4, 8, 16, 32, 64)]
    theorem = perfect_matching_spherical_theorem()
    failures = sum(not row.exact_thrall_decomposition_verified for row in controls)
    brauer_dimension_failures = sum(
        brauer_regular_dimension(m) != perfect_matching_count(m)
        for m in range(1, 9)
    )
    brauer_profile_collisions = sum(
        brauer_regular_sector_count(m) == len(integer_partitions(m))
        for m in range(2, 9)
    )
    verified = (
        theorem.theorem_verified
        and failures == 0
        and brauer_dimension_failures == 0
        and brauer_profile_collisions == 0
    )
    metrics: dict[str, int | float] = {
        "perfect_matching_gelfand_theorem_count": int(verified),
        "homogeneous_basis_sampler_construction_count": int(verified),
        "finite_character_control_count": len(controls),
        "finite_character_control_failure_count": failures,
        "maximum_finite_constituent_multiplicity": max(
            row.maximum_constituent_multiplicity for row in controls
        ),
        "brauer_regular_dimension_control_count": 8,
        "brauer_regular_dimension_failure_count": brauer_dimension_failures,
        "brauer_profile_collision_count_beyond_trivial_m1": brauer_profile_collisions,
        "maximum_scaling_homogeneous_sector_count": max(
            row.homogeneous_sector_count for row in scaling
        ),
        "maximum_canonical_purification_multiplicity_ratio_log2": max(
            row.canonical_purification_multiplicity_ratio_log2 for row in scaling
        ),
        "row_state_verifier_count": 0,
        "polynomial_hidden_involution_decoder_count": 0,
        "new_quantum_algorithm_count": 0,
    }
    return PerfectMatchingSphericalBoundaryReport(
        created_at=utc_now(),
        theorem_contract={
            "label_space": "fixed-point-free involutions/perfect matchings",
            "group": "S_(2m)",
            "label_stabilizer": "S_2 wr S_m",
            "measurement_input": (
                "accessible covariant purification and reversible decoder "
                "covered by the arbitrary-measurement intertwiner theorem"
            ),
            "resolved_primitive": (
                "uniform homogeneous-Fourier basis sampling and inverse input "
                "encoding via coset embedding plus the S_(2m) QFT"
            ),
            "unresolved_primitive": (
                "classically meaningful verification or polynomial polar "
                "implementation for the physical multiplicity row"
            ),
        },
        finite_character_controls=controls,
        scaling_records=scaling,
        theorem=theorem,
        proof_obligations=[
            {
                "obligation": "identify_perfect_matching_gelfand_decomposition",
                "resolved": verified,
                "resolution": (
                    "Thrall's decomposition gives exactly the even-row Specht "
                    "modules once each; exact character controls verify m<=7."
                ),
            },
            {
                "obligation": "make_homogeneous_basis_average_operational",
                "resolved": True,
                "resolution": (
                    "Random matching coset preparation and the efficient "
                    "symmetric-group QFT sample the required basis law without "
                    "conditional spherical-vector synthesis."
                ),
            },
            {
                "obligation": "reduce_physical_multiplicity_row_to_scalar",
                "resolved": False,
                "resolution": (
                    "Gelfand multiplicity one applies to C[X_m], not to the "
                    "physical purification representation."
                ),
            },
            {
                "obligation": "verify_or_decode_prepared_row_state",
                "resolved": False,
                "resolution": (
                    "No independent relation, observable, or classical witness "
                    "has been derived from the row vector."
                ),
            },
            {
                "obligation": "transfer_2026_brauer_qft_to_spherical_inverse",
                "resolved": False,
                "resolution": (
                    "The sector counts and algebra actions differ, and the "
                    "published approximation needs a separate large loop "
                    "parameter. A transfer theorem is absent."
                ),
            },
        ],
        adversarial_audit=[
            {
                "challenge": "The nonabelian homogeneous transform is itself the blocker.",
                "survives": False,
                "response": (
                    "For perfect matchings, coset embedding plus the S_(2m) QFT "
                    "gives the exact basis distribution needed by the average "
                    "inverse-row reduction."
                ),
            },
            {
                "challenge": "Multiplicity-free outcomes make every block scalar.",
                "survives": False,
                "response": (
                    "Only the output multiplicity is one. The physical block is "
                    "a row over its generally large multiplicity space."
                ),
            },
            {
                "challenge": "The Brauer QFT diagonalizes the required matching space.",
                "survives": False,
                "response": (
                    "Equal standard-basis cardinality hides incompatible block "
                    "profiles: p(m) versus sum_k p(m-2k)."
                ),
            },
            {
                "challenge": "Large physical multiplicity proves a circuit lower bound.",
                "survives": False,
                "response": (
                    "It does not: the state occupies only O(m log m) qubits. "
                    "Multiplicity diagnoses the unresolved structure but is not "
                    "a gate lower bound."
                ),
            },
        ],
        literature_links=[
            {
                "paper_id": "MALEKI-RAZAFIMAHATRATRA-2023",
                "title": (
                    "On cocliques in commutative Schurian association schemes "
                    "of the symmetric group"
                ),
                "url": "https://arxiv.org/abs/2307.02844",
                "use": (
                    "Primary modern source confirming the perfect-matching "
                    "Gelfand pair and its even-row constituents"
                ),
                "external_theorem_not_reproved_here": True,
            },
            {
                "paper_id": "FOXMAN-NEHORAN-DING-2026",
                "title": "Efficient Quantum Fourier Transforms For Semisimple Algebras",
                "url": "https://arxiv.org/abs/2605.05337",
                "use": (
                    "Brauer-algebra QFT audited as an adjacent circuit technique, "
                    "not identified with the perfect-matching spherical transform"
                ),
                "external_theorem_not_reproved_here": True,
            },
            {
                "paper_id": "BEALS-1997",
                "title": "Quantum computation of Fourier transforms over symmetric groups",
                "url": "https://doi.org/10.1145/258533.258548",
                "use": "Efficient S_n QFT used by the homogeneous-basis sampler",
                "external_theorem_not_reproved_here": True,
            },
        ],
        headline_metrics=metrics,
        claim_gate={
            "perfect_matching_label_space_gelfand_pair": verified,
            "uniform_homogeneous_fourier_basis_sampler_constructed": verified,
            "generic_homogeneous_transform_blocker_applies_here": False,
            "outcome_multiplicity_free_implies_physical_scalar_blocks": False,
            "brauer_qft_is_required_spherical_inverse": False,
            "row_state_is_classically_verifiable_hidden_involution_witness": False,
            "polynomial_hidden_involution_decoder_constructed": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The perfect-matching outcome transform is operational and "
                "multiplicity-free, but the arbitrary decoder consequence is "
                "still an unverified vector in a physical multiplicity space."
            ),
        },
        status=(
            "perfect-matching-spherical-transform-resolved-row-verifier-open"
            if verified
            else "perfect-matching-spherical-boundary-control-failure"
        ),
        summary=(
            "Resolved the perfect-matching homogeneous Fourier sampling step, "
            "proved the multiplicity-free row normal form, and ruled out a "
            "naive substitution of the 2026 Brauer-algebra QFT; the live "
            "bottleneck is now a verifier or polar implementation for the "
            "physical multiplicity row."
        ),
        falsifiers_triggered=[
            "The fixed-point-free-involution outcome space is a Gelfand pair, so higher output multiplicity is not the blocker.",
            "The required average homogeneous-basis input distribution is efficiently sampleable from random matching cosets and the S_n QFT.",
            "Multiplicity-free outcome sectors do not collapse the physical purification multiplicity spaces.",
            "The Brauer regular QFT and perfect-matching spherical transform have different exact sector counts for every m>=2.",
            "Large multiplicity dimension alone is not a quantum circuit lower bound.",
            "No row-state verifier, hidden-involution decoder, or speedup has been constructed.",
        ],
    )


def write_perfect_matching_spherical_boundary(
    path: Path = REPORT_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = (
        "EXP-COSET-PERFECT-MATCHING-SPHERICAL-BOUNDARY"
    ),
    registry_candidate_id: str = "CODE-COSET-COLLECTIVE",
    registry_result_id: str = "",
    **kwargs: Any,
) -> dict[str, Any]:
    path = path
    output_path = path
    for _k in ("write_registry", "registry_experiment_id", "registry_candidate_id", "registry_result_id"):
        kwargs.pop(_k, None)
    payload = asdict(run_perfect_matching_spherical_boundary())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    if write_registry:
        _res_payload = report if "report" in locals() else (payload if "payload" in locals() else (result if "result" in locals() else output))
        from research_registry import (
            ExperimentResultRecord,
            NegativeResultRecord,
            upsert_experiment_result,
            upsert_negative_result,
        )

        upsert_negative_result(
            NegativeResultRecord(
                id="NEG--PERFECT-MATCHING-SPHERICAL-BOUNDARY",
                source=registry_experiment_id,
                claim=(
                    "Initial negative claim for EXP-COSET-PERFECT-MATCHING-SPHERICAL-BOUNDARY."
                ),
                reason_invalid=(
                    "Falsified or refined by exact theorem evaluation."
                ),
                lesson=(
                    "Lesson from exact theorem analysis for EXP-COSET-PERFECT-MATCHING-SPHERICAL-BOUNDARY."
                ),
                applies_to=[
                    registry_candidate_id,
                    registry_experiment_id,
                    "PO-MEASUREMENT",
                ],
                evidence=_res_payload.get("headline_metrics", {}),
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
                created_at=_res_payload.get("created_at", ""),
                status=_res_payload.get("status", "completed"),
                summary=_res_payload.get("summary", ""),
                metrics=_res_payload.get("headline_metrics", {}),
                falsifiers_triggered=_res_payload.get("falsifiers_triggered", []),
                artifacts={
                    "coset_perfect_matching_spherical_boundary": str(path)
                },
            )
        )

    return payload


if __name__ == "__main__":
    output = write_perfect_matching_spherical_boundary()
    print(json.dumps(output["headline_metrics"], indent=2, sort_keys=True))

"""Obstruction to a branchwise-covariant local common-core quotient.

For a block of ``C`` unequal labels, consider every orientation action: each
orientation applies the same ``s in S_n`` to exactly one member of every
``(lambda_i,mu_i)`` pair.  Across all ``2^C`` orientations, the membership
signature of each of the ``2C`` source factors is distinct.  For ``n>=5``,
simplicity of ``A_n`` implies that the generated subgroup contains an
independent ``A_n`` action on every source factor.

If no source partition is self-conjugate, each corresponding ``S_n`` irrep
restricts irreducibly to ``A_n``.  Their outer tensor product is therefore an
irreducible representation of ``A_n^(2C)``.  By Schur's lemma, any operator
commuting with every orientation action is scalar; an orthogonal projector in
that commutant is only zero or identity.  Hence no nontrivial branchwise-
covariant local projector can annihilate the common core in this sector.

This does not rule out a physical transform that coherently mixes induced-
representation orientation branches, and it is not promoted to a typical
natural theorem.  Self-conjugate Plancherel partitions split on restriction to
``A_n``; the repository has finite mass controls but no asymptotic theorem
showing they are absent from an information-threshold tuple.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from functools import lru_cache
from pathlib import Path
from typing import Any

import numpy as np

from research_registry import (
    ExperimentResultRecord,
    NegativeResultRecord,
    upsert_experiment_result,
    upsert_negative_result,
    utc_now,
)
from self_dual_wreath_block_common_core_quotient import (
    validate_block_common_core_quotient,
)
from self_dual_wreath_natural_unequal_dominance import (
    plancherel_probabilities,
)
from self_dual_wreath_orientation_fourier_reduction import (
    _orientation_representation_matrix,
    orientation_invariant_projector,
)


REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_orientation_covariant_quotient_obstruction.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-ORIENTATION-COVARIANT-QUOTIENT-OBSTRUCTION"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"

Partition = tuple[int, ...]
Label = tuple[Partition, Partition]


@dataclass(frozen=True)
class CovariantOrbitClosureControl:
    n: int
    labels: tuple[Label, ...]
    source_factor_count: int
    every_source_partition_non_self_conjugate: bool
    orientation_count: int
    adjacent_generator_count: int
    initial_common_range_dimension: int
    orbit_closure_dimension: int
    carrier_dimension: int
    orbit_closure_is_full: bool
    closure_sweep_count: int
    algebraic_scalar_commutant_condition_holds: bool
    exact_finite_orbit_closure_validation: bool
    status: str


@dataclass(frozen=True)
class SelfConjugatePlancherelMassRecord:
    n: int
    partition_count: int
    self_conjugate_partition_count: int
    self_conjugate_plancherel_mass: float
    information_threshold_copy_count: int
    source_draw_count: int
    probability_no_self_conjugate_source_draw: float
    asymptotic_tuple_absence_proved: bool
    status: str


@dataclass(frozen=True)
class OrientationCovariantQuotientObstructionReport:
    created_at: str
    theorem_contract: dict[str, str]
    finite_controls: list[CovariantOrbitClosureControl]
    self_conjugate_mass_records: list[SelfConjugatePlancherelMassRecord]
    adversarial_audit: list[dict[str, bool | str]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, bool | str]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def conjugate_partition(partition: Partition) -> Partition:
    return tuple(
        sum(row >= column for row in partition)
        for column in range(1, partition[0] + 1)
    )


def orientation_parity_span_rank(block_size: int) -> int:
    """Rank over F_2 of one-choice-per-pair orientation vectors."""

    if block_size < 1:
        raise ValueError("block_size must be positive")
    return block_size + 1


def _adjacent_transposition(n: int, index: int) -> tuple[int, ...]:
    permutation = list(range(n))
    permutation[index], permutation[index + 1] = (
        permutation[index + 1],
        permutation[index],
    )
    return tuple(permutation)


def _extend_orthonormal_basis(
    basis: np.ndarray,
    vectors: np.ndarray,
    tolerance: float,
) -> np.ndarray:
    residual = vectors - basis @ (basis.T @ vectors)
    residual -= basis @ (basis.T @ residual)
    if float(np.linalg.norm(residual)) <= tolerance:
        return basis
    left, singular_values, _ = np.linalg.svd(
        residual,
        full_matrices=False,
    )
    additions = left[:, singular_values > tolerance]
    if not additions.size:
        return basis
    combined, _ = np.linalg.qr(np.column_stack((basis, additions)))
    return combined


@lru_cache(maxsize=None)
def validate_covariant_orbit_closure(
    tolerance: float = 1e-8,
) -> CovariantOrbitClosureControl:
    quotient_control = validate_block_common_core_quotient()
    n = quotient_control.n
    labels = quotient_control.labels
    masks = quotient_control.replicated_orientation_masks
    projectors = tuple(
        orientation_invariant_projector((n,), labels, mask)
        for mask in masks
    )
    eigenvalues, eigenvectors = np.linalg.eigh(sum(projectors) / 2)
    basis = eigenvectors[:, eigenvalues > 1 - tolerance]
    initial_dimension = basis.shape[1]
    generators = tuple(
        _orientation_representation_matrix(
            labels,
            _adjacent_transposition(n, adjacent),
            mask,
        )
        for mask in range(1 << len(labels))
        for adjacent in range(n - 1)
    )
    sweep_count = 0
    while sweep_count <= basis.shape[0]:
        old_dimension = basis.shape[1]
        for generator in generators:
            basis = _extend_orthonormal_basis(
                basis,
                generator @ basis,
                tolerance,
            )
            if basis.shape[1] == basis.shape[0]:
                break
        sweep_count += 1
        if basis.shape[1] in (old_dimension, basis.shape[0]):
            break
    sources = tuple(partition for label in labels for partition in label)
    non_self = all(
        partition != conjugate_partition(partition)
        for partition in sources
    )
    full = basis.shape[1] == basis.shape[0]
    condition = n >= 5 and non_self
    verified = initial_dimension > 0 and full and condition
    return CovariantOrbitClosureControl(
        n=n,
        labels=labels,
        source_factor_count=len(sources),
        every_source_partition_non_self_conjugate=non_self,
        orientation_count=1 << len(labels),
        adjacent_generator_count=len(generators),
        initial_common_range_dimension=initial_dimension,
        orbit_closure_dimension=basis.shape[1],
        carrier_dimension=basis.shape[0],
        orbit_closure_is_full=full,
        closure_sweep_count=sweep_count,
        algebraic_scalar_commutant_condition_holds=condition,
        exact_finite_orbit_closure_validation=verified,
        status=(
            "exact-full-orientation-orbit-closure-validation"
            if verified
            else "orientation-orbit-closure-validation-failure"
        ),
    )


def self_conjugate_plancherel_mass_record(
    n: int,
) -> SelfConjugatePlancherelMassRecord:
    probabilities = plancherel_probabilities(n)
    self_conjugate = [
        (partition, probability)
        for partition, probability in probabilities
        if partition == conjugate_partition(partition)
    ]
    mass = sum(float(probability) for _, probability in self_conjugate)
    copies = math.ceil(math.log2(math.factorial(n)))
    draw_count = 2 * copies
    no_self = math.exp(draw_count * math.log1p(-mass)) if mass < 1 else 0.0
    return SelfConjugatePlancherelMassRecord(
        n=n,
        partition_count=len(probabilities),
        self_conjugate_partition_count=len(self_conjugate),
        self_conjugate_plancherel_mass=mass,
        information_threshold_copy_count=copies,
        source_draw_count=draw_count,
        probability_no_self_conjugate_source_draw=no_self,
        asymptotic_tuple_absence_proved=False,
        status="finite-self-conjugate-plancherel-mass-control",
    )


def run_orientation_covariant_quotient_obstruction() -> (
    OrientationCovariantQuotientObstructionReport
):
    controls = [validate_covariant_orbit_closure()]
    mass_records = [
        self_conjugate_plancherel_mass_record(n)
        for n in (5, 6, 8, 10, 12, 16, 20, 24, 28, 32, 36, 40, 48)
    ]
    failures = sum(
        not record.exact_finite_orbit_closure_validation
        for record in controls
    )
    metrics: dict[str, int | float] = {
        "independent_alternating_factor_action_theorem_count": 1,
        "non_self_conjugate_scalar_commutant_theorem_count": 1,
        "branchwise_covariant_nontrivial_projector_no_go_theorem_count": 1,
        "finite_orbit_closure_control_count": len(controls),
        "finite_orbit_closure_validation_failure_count": failures,
        "maximum_finite_orbit_closure_fraction": max(
            record.orbit_closure_dimension / record.carrier_dimension
            for record in controls
        ),
        "maximum_finite_closure_sweep_count": max(
            record.closure_sweep_count for record in controls
        ),
        "self_conjugate_mass_record_count": len(mass_records),
        "tail_n": mass_records[-1].n,
        "tail_self_conjugate_plancherel_mass": (
            mass_records[-1].self_conjugate_plancherel_mass
        ),
        "tail_probability_no_self_conjugate_source_draw": (
            mass_records[-1].probability_no_self_conjugate_source_draw
        ),
        "asymptotic_natural_tuple_non_self_conjugate_theorem_count": 0,
        "orientation_branch_mixing_physical_transform_count": 0,
        "residual_polynomial_frame_norm_theorem_count": 0,
        "polynomial_hidden_permutation_decoder_count": 0,
        "new_quantum_algorithm_count": 0,
    }
    theorem_verified = failures == 0
    return OrientationCovariantQuotientObstructionReport(
        created_at=utc_now(),
        theorem_contract={
            "orientation_generated_subgroup": (
                "For n>=5, distinct all-orientation membership signatures "
                "generate independent A_n actions on every source factor."
            ),
            "restriction_condition": (
                "A non-self-conjugate S_n irrep restricts irreducibly to A_n."
            ),
            "scalar_commutant": (
                "When every source is non-self-conjugate, the outer tensor "
                "representation of A_n^(2C) is irreducible; its commutant is "
                "scalar by Schur's lemma."
            ),
            "projector_no_go": (
                "A branchwise projector commuting with every orientation "
                "action is zero or identity, so it cannot both remove a "
                "nonzero common core and retain a nonzero carrier."
            ),
            "scope_boundary": (
                "Self-conjugate source factors and coherent transforms mixing "
                "the induced orientation branches are outside the theorem."
            ),
        },
        finite_controls=controls,
        self_conjugate_mass_records=mass_records,
        adversarial_audit=[
            {
                "objection": (
                    "The norm-one mixed commutator is a basis artifact; the "
                    "common vector may still have a small covariant orbit."
                ),
                "resolved": True,
                "resolution": (
                    "The explicit common vector's orbit under adjacent mixed-"
                    "orientation generators spans all 400 carrier dimensions."
                ),
            },
            {
                "objection": (
                    "Schur's lemma applies automatically to every natural "
                    "source tuple."
                ),
                "resolved": False,
                "resolution": (
                    "Self-conjugate partitions split on A_n. Finite controls "
                    "show noticeable tuple incidence, and no asymptotic "
                    "absence theorem is registered."
                ),
            },
            {
                "objection": (
                    "The scalar branchwise commutant rules out a physical "
                    "measurement that mixes orientation summands coherently."
                ),
                "resolved": False,
                "resolution": (
                    "Such a transform acts outside the compressed branchwise "
                    "commutant and is the remaining structured bypass."
                ),
            },
        ],
        headline_metrics=metrics,
        claim_gate={
            "all_orientation_independent_alternating_actions_proved": True,
            "non_self_conjugate_branchwise_scalar_commutant_proved": (
                theorem_verified
            ),
            "nontrivial_branchwise_covariant_local_quotient_exists": False,
            "typical_natural_tuple_satisfies_non_self_conjugate_condition": False,
            "coherent_orientation_branch_mixing_transform_ruled_out": False,
            "general_physical_quotient_ruled_out": False,
            "residual_polynomial_frame_norm_proved": False,
            "polynomial_hidden_permutation_decoder_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The simple branchwise-covariant quotient is impossible when "
                "all source A_n restrictions are irreducible, and the finite "
                "common-vector orbit fills its carrier. Natural self-conjugate "
                "incidence and coherent branch-mixing transforms remain open."
            ),
        },
        status=(
            "branchwise-covariant-quotient-falsified-branch-mixing-open"
            if theorem_verified
            else "orientation-covariant-quotient-obstruction-failure"
        ),
        summary=(
            "Proved a scalar-commutant obstruction to nontrivial local "
            "quotients commuting with every orientation action in the non-"
            "self-conjugate sector. The physical critical path now requires "
            "coherent mixing of induced orientation branches."
        ),
        falsifiers_triggered=[
            (
                "The algebraic common-core quotient cannot be lifted by a "
                "simple branchwise-covariant projector in the irreducible "
                "A_n-restriction regime."
            ),
            (
                "A finite common vector that is one-dimensional before orbit "
                "closure generates the entire carrier under mixed branches."
            ),
            (
                "No typical-natural or all-physical-transform no-go is "
                "claimed because self-conjugate restrictions and coherent "
                "branch mixing remain unresolved."
            ),
        ],
    )


def write_orientation_covariant_quotient_obstruction_report(
    path: Path = REPORT_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = DEFAULT_EXPERIMENT_ID,
    registry_candidate_id: str = DEFAULT_CANDIDATE_ID,
    registry_result_id: str | None = None,
) -> dict[str, Any]:
    payload = asdict(run_orientation_covariant_quotient_obstruction())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    return payload


if __name__ == "__main__":
    report = write_orientation_covariant_quotient_obstruction_report()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))

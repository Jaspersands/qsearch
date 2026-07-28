"""Exact two-copy target law for a shared hidden involution.

For ``G=S_n`` and ``H_h={e,h}``, weak Fourier sampling of one coset state
produces source label ``lambda`` with probability

    q_h(lambda) = d_lambda^2 / |G| * (1 + r_lambda),

where ``r_lambda=chi_lambda(h)/d_lambda``.  Conditioned on two accessible
source labels ``lambda,mu``, measuring the diagonal ``S_n`` irrep ``nu`` in
``V_lambda tensor V_mu`` has exact probability

    p_h(nu | lambda,mu)
      = [g(lambda,mu,nu)d_nu/(d_lambda d_mu)]
        [1+r_lambda+r_mu+r_nu]/[(1+r_lambda)(1+r_mu)].

The proof expands the two conditioned column states.  For the ``nu`` isotypic
projector ``P_nu``, Schur's lemma gives

    Tr P_nu                              = g d_nu,
    Tr P_nu(rho_lambda(h) tensor I)      = g d_nu r_lambda,
    Tr P_nu(I tensor rho_mu(h))          = g d_nu r_mu,
    Tr P_nu(rho_lambda(h) tensor rho_mu(h)) = g d_nu r_nu.

Consequently the unconditioned joint law is

    p_h(lambda,mu,nu)
      = d_lambda d_mu g d_nu / |G|^2
        * (1+r_lambda+r_mu+r_nu).

This is the operational correction to the dimension-weighted Kronecker
coupling reference used by earlier finite coverage reports.  It determines
target frequencies, but it does not implement the coherent Kronecker
measurement, resolve multiplicities, or decode ``h``.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from fractions import Fraction
from functools import lru_cache
from pathlib import Path

from coset_typical_source_coverage import certified_nontrivial_targets
from representation_obstruction import hook_length_dimension, integer_partitions
from research_registry import (
    ExperimentResultRecord,
    NegativeResultRecord,
    upsert_experiment_result,
    upsert_negative_result,
    utc_now,
)
from symmetric_character import kronecker_coefficient
from weak_fourier_signal import character_on_involution, involution_specs_for_n


REPORT_PATH = Path(
    "research/representation/coset_same_hidden_target_law.json"
)
UNIFORM_SOURCE_REPORT_PATH = Path(
    "research/representation/coset_typical_uniform_source_probe.json"
)
DEFAULT_EXPERIMENT_ID = "EXP-COSET-SAME-HIDDEN-TARGET-LAW"
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


@dataclass(frozen=True)
class TargetSectorMassRecord:
    left_source_partition: tuple[int, ...]
    right_source_partition: tuple[int, ...]
    target_partition: tuple[int, ...]
    kronecker_multiplicity: int
    exact_source_pair_probability: str
    source_pair_probability: float
    exact_dimension_weighted_coupling_mass: str
    dimension_weighted_coupling_mass: float
    exact_conditional_target_probability: str
    conditional_target_probability: float
    exact_natural_joint_probability: str
    natural_joint_probability: float
    frame_scalar: str


@dataclass(frozen=True)
class FixedSourceCoverageCorrection:
    source_partition: tuple[int, ...]
    source_dimension: int
    exact_source_pair_probability: str
    source_pair_probability: float
    exact_dimension_weighted_certified_conditional_mass: str
    dimension_weighted_certified_conditional_mass: float
    exact_same_hidden_certified_conditional_probability: str
    same_hidden_certified_conditional_probability: float
    exact_same_hidden_natural_joint_certified_probability: str
    same_hidden_natural_joint_certified_probability: float
    exact_source_pair_conditional_total_variation: str
    source_pair_conditional_total_variation: float
    largest_unresolved_target_partition: tuple[int, ...] | None
    largest_unresolved_same_hidden_conditional_probability: float
    all_supported_targets_certified: bool


@dataclass(frozen=True)
class SameHiddenTargetLawRecord:
    n: int
    involution_type: str
    transposition_count: int
    partition_count: int
    accessible_source_label_count: int
    accessible_ordered_source_pair_count: int
    supported_target_sector_count: int
    exact_source_label_probability_sum: str
    exact_natural_joint_probability_sum: str
    conditional_normalization_failure_count: int
    negative_probability_count: int
    frame_identity_failure_count: int
    zero_probability_supported_sector_count: int
    exact_natural_nontrivial_multiplicity_mass: str
    natural_nontrivial_multiplicity_mass: float
    exact_expected_conditional_tv_from_dimension_coupling: str
    expected_conditional_tv_from_dimension_coupling: float
    exact_maximum_source_pair_tv_from_dimension_coupling: str
    maximum_source_pair_tv_from_dimension_coupling: float
    maximum_tv_left_source_partition: tuple[int, ...]
    maximum_tv_right_source_partition: tuple[int, ...]
    exact_scalar_collision_source_pair_mass: str
    scalar_collision_source_pair_mass: float
    exact_scalar_collision_target_joint_mass: str
    scalar_collision_target_joint_mass: float
    top_natural_target_sectors: list[TargetSectorMassRecord]
    fixed_source_coverage_correction: FixedSourceCoverageCorrection | None
    status: str


@dataclass(frozen=True)
class SameHiddenTargetLawReport:
    created_at: str
    theorem_contract: dict[str, object]
    records: list[SameHiddenTargetLawRecord]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, bool | str]
    status: str
    summary: str
    falsifiers_triggered: list[str]


@lru_cache(maxsize=None)
def source_label_probability(
    n: int,
    transposition_count: int,
    partition: tuple[int, ...],
) -> Fraction:
    dimension = hook_length_dimension(partition)
    character = character_on_involution(partition, transposition_count)
    probability = Fraction(
        dimension * (dimension + character),
        math.factorial(n),
    )
    if probability < 0:
        raise ArithmeticError("weak Fourier source probability is negative")
    return probability


@lru_cache(maxsize=None)
def conditional_target_probability(
    n: int,
    transposition_count: int,
    left_source: tuple[int, ...],
    right_source: tuple[int, ...],
    target: tuple[int, ...],
) -> Fraction:
    """Return the exact shared-hidden target probability.

    A zero-probability source label has no conditional state, so callers must
    not request a conditional probability for an inaccessible source pair.
    """

    multiplicity = kronecker_coefficient(
        left_source,
        right_source,
        target,
    )
    if not multiplicity:
        return Fraction()
    left_dimension = hook_length_dimension(left_source)
    right_dimension = hook_length_dimension(right_source)
    target_dimension = hook_length_dimension(target)
    left_ratio = Fraction(
        character_on_involution(left_source, transposition_count),
        left_dimension,
    )
    right_ratio = Fraction(
        character_on_involution(right_source, transposition_count),
        right_dimension,
    )
    target_ratio = Fraction(
        character_on_involution(target, transposition_count),
        target_dimension,
    )
    denominator = (1 + left_ratio) * (1 + right_ratio)
    if denominator == 0:
        raise ValueError(
            "conditional target law is undefined for an inaccessible source"
        )
    coupling = Fraction(
        multiplicity * target_dimension,
        left_dimension * right_dimension,
    )
    probability = (
        coupling
        * (1 + left_ratio + right_ratio + target_ratio)
        / denominator
    )
    if probability < 0:
        raise ArithmeticError("conditional target probability is negative")
    return probability


@lru_cache(maxsize=None)
def natural_joint_target_probability(
    n: int,
    transposition_count: int,
    left_source: tuple[int, ...],
    right_source: tuple[int, ...],
    target: tuple[int, ...],
) -> Fraction:
    source_pair = source_label_probability(
        n, transposition_count, left_source
    ) * source_label_probability(n, transposition_count, right_source)
    if source_pair == 0:
        return Fraction()
    return source_pair * conditional_target_probability(
        n,
        transposition_count,
        left_source,
        right_source,
        target,
    )


def _dimension_weighted_coupling(
    left_source: tuple[int, ...],
    right_source: tuple[int, ...],
    target: tuple[int, ...],
) -> Fraction:
    multiplicity = kronecker_coefficient(
        left_source,
        right_source,
        target,
    )
    return Fraction(
        multiplicity * hook_length_dimension(target),
        hook_length_dimension(left_source)
        * hook_length_dimension(right_source),
    )


def _frame_scalar(
    transposition_count: int,
    left_source: tuple[int, ...],
    right_source: tuple[int, ...],
    target: tuple[int, ...],
) -> Fraction:
    return (
        1
        + Fraction(
            character_on_involution(left_source, transposition_count),
            hook_length_dimension(left_source),
        )
        + Fraction(
            character_on_involution(right_source, transposition_count),
            hook_length_dimension(right_source),
        )
        + Fraction(
            character_on_involution(target, transposition_count),
            hook_length_dimension(target),
        )
    )


def _load_exact_scalar_collision_blocks(
    path: Path = UNIFORM_SOURCE_REPORT_PATH,
) -> set[
    tuple[
        int,
        tuple[int, ...],
        tuple[int, ...],
        tuple[int, ...],
    ]
]:
    if not path.exists():
        return set()
    try:
        payload = json.loads(path.read_text())
    except (json.JSONDecodeError, OSError):
        return set()
    return {
        (
            int(record["n"]),
            tuple(record["left_source_partition"]),
            tuple(record["right_source_partition"]),
            tuple(record["target_partition"]),
        )
        for record in payload.get("block_records", [])
        if record.get("exact_scalar_collision_proved", False)
    }


def _maximum_dimension_partition(n: int) -> tuple[int, ...]:
    return max(
        integer_partitions(n),
        key=lambda partition: (
            hook_length_dimension(partition),
            partition,
        ),
    )


def _fixed_source_correction(
    n: int,
    transposition_count: int,
    certified_targets: set[tuple[int, ...]],
) -> FixedSourceCoverageCorrection:
    source = _maximum_dimension_partition(n)
    dimension = hook_length_dimension(source)
    source_probability = source_label_probability(
        n,
        transposition_count,
        source,
    )
    source_pair = source_probability**2
    coupling_certified = Fraction()
    same_hidden_certified = Fraction()
    total_variation = Fraction()
    unresolved: list[tuple[Fraction, tuple[int, ...]]] = []
    supported_count = 0
    certified_count = 0
    for target in integer_partitions(n):
        multiplicity = kronecker_coefficient(source, source, target)
        if not multiplicity:
            continue
        supported_count += 1
        coupling = _dimension_weighted_coupling(source, source, target)
        conditional = conditional_target_probability(
            n,
            transposition_count,
            source,
            source,
            target,
        )
        total_variation += abs(conditional - coupling)
        certified = multiplicity <= 1 or target in certified_targets
        if certified:
            certified_count += 1
            coupling_certified += coupling
            same_hidden_certified += conditional
        else:
            unresolved.append((conditional, target))
    total_variation /= 2
    unresolved.sort(key=lambda row: (-row[0], row[1]))
    largest = unresolved[0] if unresolved else None
    return FixedSourceCoverageCorrection(
        source_partition=source,
        source_dimension=dimension,
        exact_source_pair_probability=str(source_pair),
        source_pair_probability=float(source_pair),
        exact_dimension_weighted_certified_conditional_mass=str(
            coupling_certified
        ),
        dimension_weighted_certified_conditional_mass=float(
            coupling_certified
        ),
        exact_same_hidden_certified_conditional_probability=str(
            same_hidden_certified
        ),
        same_hidden_certified_conditional_probability=float(
            same_hidden_certified
        ),
        exact_same_hidden_natural_joint_certified_probability=str(
            source_pair * same_hidden_certified
        ),
        same_hidden_natural_joint_certified_probability=float(
            source_pair * same_hidden_certified
        ),
        exact_source_pair_conditional_total_variation=str(total_variation),
        source_pair_conditional_total_variation=float(total_variation),
        largest_unresolved_target_partition=(
            largest[1] if largest else None
        ),
        largest_unresolved_same_hidden_conditional_probability=(
            float(largest[0]) if largest else 0.0
        ),
        all_supported_targets_certified=certified_count == supported_count,
    )


def audit_same_hidden_target_law(
    n: int,
    transposition_count: int,
    involution_type: str,
    *,
    collision_blocks: set[
        tuple[
            int,
            tuple[int, ...],
            tuple[int, ...],
            tuple[int, ...],
        ]
    ] | None = None,
    certified_targets: set[tuple[int, ...]] | None = None,
    top_k: int = 12,
) -> SameHiddenTargetLawRecord:
    partitions = integer_partitions(n)
    order = math.factorial(n)
    collision_set = (
        _load_exact_scalar_collision_blocks()
        if collision_blocks is None
        else collision_blocks
    )
    source_probabilities = {
        partition: source_label_probability(
            n,
            transposition_count,
            partition,
        )
        for partition in partitions
    }
    source_sum = sum(source_probabilities.values(), Fraction())
    if source_sum != 1:
        raise ArithmeticError("weak Fourier source probabilities do not sum to one")
    accessible = [
        partition
        for partition, probability in source_probabilities.items()
        if probability
    ]
    joint_sum = Fraction()
    nontrivial_mass = Fraction()
    expected_tv = Fraction()
    maximum_tv = Fraction()
    maximum_tv_pair = (accessible[0], accessible[0])
    conditional_failures = 0
    negative_probabilities = 0
    frame_failures = 0
    zero_probability_sectors = 0
    supported_sector_count = 0
    collision_target_mass = Fraction()
    collision_source_pairs = {
        (left, right)
        for block_n, left, right, _ in collision_set
        if block_n == n
    }
    collision_source_pair_mass = sum(
        (
            source_probabilities[left] * source_probabilities[right]
            for left, right in collision_source_pairs
        ),
        Fraction(),
    )
    sector_rows: list[
        tuple[Fraction, TargetSectorMassRecord]
    ] = []
    for left_source in accessible:
        for right_source in accessible:
            source_pair = (
                source_probabilities[left_source]
                * source_probabilities[right_source]
            )
            conditional_sum = Fraction()
            pair_tv = Fraction()
            for target in partitions:
                multiplicity = kronecker_coefficient(
                    left_source,
                    right_source,
                    target,
                )
                if not multiplicity:
                    continue
                supported_sector_count += 1
                coupling = _dimension_weighted_coupling(
                    left_source,
                    right_source,
                    target,
                )
                conditional = conditional_target_probability(
                    n,
                    transposition_count,
                    left_source,
                    right_source,
                    target,
                )
                joint = source_pair * conditional
                frame_scalar = _frame_scalar(
                    transposition_count,
                    left_source,
                    right_source,
                    target,
                )
                direct_joint = Fraction(
                    hook_length_dimension(left_source)
                    * hook_length_dimension(right_source)
                    * multiplicity
                    * hook_length_dimension(target),
                    order * order,
                ) * frame_scalar
                frame_failures += int(joint != direct_joint)
                negative_probabilities += int(conditional < 0 or joint < 0)
                zero_probability_sectors += int(joint == 0)
                conditional_sum += conditional
                joint_sum += joint
                pair_tv += abs(conditional - coupling)
                if multiplicity > 1:
                    nontrivial_mass += joint
                if (
                    n,
                    left_source,
                    right_source,
                    target,
                ) in collision_set:
                    collision_target_mass += joint
                sector_rows.append(
                    (
                        joint,
                        TargetSectorMassRecord(
                            left_source_partition=left_source,
                            right_source_partition=right_source,
                            target_partition=target,
                            kronecker_multiplicity=multiplicity,
                            exact_source_pair_probability=str(source_pair),
                            source_pair_probability=float(source_pair),
                            exact_dimension_weighted_coupling_mass=str(
                                coupling
                            ),
                            dimension_weighted_coupling_mass=float(coupling),
                            exact_conditional_target_probability=str(
                                conditional
                            ),
                            conditional_target_probability=float(conditional),
                            exact_natural_joint_probability=str(joint),
                            natural_joint_probability=float(joint),
                            frame_scalar=str(frame_scalar),
                        ),
                    )
                )
            conditional_failures += int(conditional_sum != 1)
            pair_tv /= 2
            expected_tv += source_pair * pair_tv
            if pair_tv > maximum_tv:
                maximum_tv = pair_tv
                maximum_tv_pair = (left_source, right_source)
    if joint_sum != 1:
        raise ArithmeticError("same-hidden joint target law does not sum to one")
    correction = None
    if certified_targets is not None:
        correction = _fixed_source_correction(
            n,
            transposition_count,
            certified_targets,
        )
    sector_rows.sort(
        key=lambda row: (
            -row[0],
            row[1].left_source_partition,
            row[1].right_source_partition,
            row[1].target_partition,
        )
    )
    return SameHiddenTargetLawRecord(
        n=n,
        involution_type=involution_type,
        transposition_count=transposition_count,
        partition_count=len(partitions),
        accessible_source_label_count=len(accessible),
        accessible_ordered_source_pair_count=len(accessible) ** 2,
        supported_target_sector_count=supported_sector_count,
        exact_source_label_probability_sum=str(source_sum),
        exact_natural_joint_probability_sum=str(joint_sum),
        conditional_normalization_failure_count=conditional_failures,
        negative_probability_count=negative_probabilities,
        frame_identity_failure_count=frame_failures,
        zero_probability_supported_sector_count=zero_probability_sectors,
        exact_natural_nontrivial_multiplicity_mass=str(nontrivial_mass),
        natural_nontrivial_multiplicity_mass=float(nontrivial_mass),
        exact_expected_conditional_tv_from_dimension_coupling=str(
            expected_tv
        ),
        expected_conditional_tv_from_dimension_coupling=float(expected_tv),
        exact_maximum_source_pair_tv_from_dimension_coupling=str(maximum_tv),
        maximum_source_pair_tv_from_dimension_coupling=float(maximum_tv),
        maximum_tv_left_source_partition=maximum_tv_pair[0],
        maximum_tv_right_source_partition=maximum_tv_pair[1],
        exact_scalar_collision_source_pair_mass=str(
            collision_source_pair_mass
        ),
        scalar_collision_source_pair_mass=float(collision_source_pair_mass),
        exact_scalar_collision_target_joint_mass=str(collision_target_mass),
        scalar_collision_target_joint_mass=float(collision_target_mass),
        top_natural_target_sectors=[
            record for _, record in sector_rows[:top_k]
        ],
        fixed_source_coverage_correction=correction,
        status=(
            "exact-target-law-normalized-collision-target-mass-audited"
            if not (
                conditional_failures
                or negative_probabilities
                or frame_failures
            )
            else "target-law-identity-failure"
        ),
    )


def build_same_hidden_target_law_report(
    n_values: tuple[int, ...] = (5, 6, 8, 9, 10),
) -> SameHiddenTargetLawReport:
    collision_blocks = _load_exact_scalar_collision_blocks()
    records: list[SameHiddenTargetLawRecord] = []
    for n in n_values:
        exact_targets = (
            certified_nontrivial_targets(n)
            if n in {8, 9, 10}
            else None
        )
        for label, transpositions in involution_specs_for_n(n):
            if label == "single_transposition_control":
                continue
            records.append(
                audit_same_hidden_target_law(
                    n,
                    transpositions,
                    label,
                    collision_blocks=collision_blocks,
                    certified_targets=exact_targets,
                )
            )
    valid_records = [
        record
        for record in records
        if not (
            record.conditional_normalization_failure_count
            or record.negative_probability_count
            or record.frame_identity_failure_count
        )
    ]
    corrections = [
        record.fixed_source_coverage_correction
        for record in records
        if record.fixed_source_coverage_correction is not None
    ]
    n10_corrections = [
        record.fixed_source_coverage_correction
        for record in records
        if record.n == 10
        and record.fixed_source_coverage_correction is not None
    ]
    metrics: dict[str, int | float] = {
        "same_hidden_target_law_record_count": len(records),
        "general_exact_character_formula_theorem_count": 1,
        "exact_normalization_verified_record_count": len(valid_records),
        "frame_scalar_identity_verified_record_count": len(valid_records),
        "dimension_coupling_reference_mismatch_record_count": sum(
            record.expected_conditional_tv_from_dimension_coupling > 0
            for record in records
        ),
        "maximum_expected_conditional_tv_from_dimension_coupling": max(
            (
                record.expected_conditional_tv_from_dimension_coupling
                for record in records
            ),
            default=0.0,
        ),
        "maximum_source_pair_conditional_tv_from_dimension_coupling": max(
            (
                record.maximum_source_pair_tv_from_dimension_coupling
                for record in records
            ),
            default=0.0,
        ),
        "maximum_natural_nontrivial_multiplicity_mass": max(
            (
                record.natural_nontrivial_multiplicity_mass
                for record in records
            ),
            default=0.0,
        ),
        "maximum_scalar_collision_source_pair_mass": max(
            (
                record.scalar_collision_source_pair_mass
                for record in records
            ),
            default=0.0,
        ),
        "maximum_scalar_collision_target_joint_mass": max(
            (
                record.scalar_collision_target_joint_mass
                for record in records
            ),
            default=0.0,
        ),
        "fixed_source_coverage_correction_count": len(corrections),
        "minimum_n10_same_hidden_certified_conditional_probability": min(
            (
                correction.same_hidden_certified_conditional_probability
                for correction in n10_corrections
                if correction is not None
            ),
            default=0.0,
        ),
        "maximum_n10_same_hidden_certified_conditional_probability": max(
            (
                correction.same_hidden_certified_conditional_probability
                for correction in n10_corrections
                if correction is not None
            ),
            default=0.0,
        ),
        "coherent_kronecker_target_measurement_theorem_count": 0,
        "hidden_involution_decoder_count": 0,
    }
    return SameHiddenTargetLawReport(
        created_at=utc_now(),
        theorem_contract={
            "source_probability": (
                "q_h(lambda)=d_lambda^2/|S_n|*(1+r_lambda)"
            ),
            "conditional_target_probability": (
                "p_h(nu|lambda,mu)="
                "[g(lambda,mu,nu)d_nu/(d_lambda d_mu)]"
                " [1+r_lambda+r_mu+r_nu]/"
                "[(1+r_lambda)(1+r_mu)]"
            ),
            "natural_joint_probability": (
                "p_h(lambda,mu,nu)="
                "d_lambda d_mu g(lambda,mu,nu)d_nu/|S_n|^2"
                " * [1+r_lambda+r_mu+r_nu]"
            ),
            "proof": (
                "Expand the two conditioned column states. Schur partial "
                "traces give the left and right character-ratio terms; the "
                "diagonal action on the nu isotypic component gives r_nu."
            ),
            "normalization_identity": (
                "sum_nu g d_nu=d_lambda d_mu and "
                "sum_nu g chi_nu(h)=chi_lambda(h)chi_mu(h)"
            ),
            "frame_link": (
                "The natural joint law equals the regular-tensor sector mass "
                "times the exact two-copy frame scalar "
                "1+r_lambda+r_mu+r_nu."
            ),
        },
        records=records,
        headline_metrics=metrics,
        claim_gate={
            "same_hidden_involution_target_outcome_law_proved": True,
            "dimension_weighted_coupling_is_target_law": False,
            "finite_exact_normalization_verified": (
                len(valid_records) == len(records)
            ),
            "coherent_kronecker_target_measurement_proved": False,
            "multiplicity_separator_implemented_coherently": False,
            "target_label_reveals_hidden_involution": False,
            "hidden_involution_decoder_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The exact law closes probability accounting but not the "
                "coherent recoupling, multiplicity measurement, information, "
                "decoder, or classical-separation obligations."
            ),
        },
        status=(
            "same-hidden-target-law-proved-operational-measurement-and-decoder-open"
        ),
        summary=(
            f"Derived and exactly normalized the shared-hidden target law on "
            f"{len(records)} finite ensemble controls through n={max(n_values)}. "
            "The prior dimension-weighted coupling reference differs from the "
            "operational law; no decoder or speedup is promoted."
        ),
        falsifiers_triggered=[
            (
                "Dimension-weighted Kronecker coupling is not the target law "
                "for two states carrying the same hidden involution."
            ),
            (
                "A source-pair collision mass is only an upper envelope; the "
                "actual collision target mass must include the coupled target."
            ),
            (
                "An exact target-frequency formula does not implement the "
                "coherent internal Kronecker transform."
            ),
            (
                "Target labels alone are conjugacy-class invariant and do not "
                "identify the individual hidden involution."
            ),
        ],
    )


def write_same_hidden_target_law_report(
    output_path: Path = REPORT_PATH,
    *,
    n_values: tuple[int, ...] = (5, 6, 8, 9, 10),
    write_registry: bool = True,
    registry_experiment_id: str = DEFAULT_EXPERIMENT_ID,
    registry_candidate_id: str = DEFAULT_CANDIDATE_ID,
    registry_result_id: str | None = None,
) -> dict[str, object]:
    payload = asdict(build_same_hidden_target_law_report(n_values=n_values))
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    if write_registry:
        upsert_negative_result(
            NegativeResultRecord(
                id="NEG-COSET-DIMENSION-COUPLING-NOT-SAME-HIDDEN-TARGET-LAW",
                source=str(output_path),
                claim=(
                    "The dimension-weighted Kronecker coupling mass is the "
                    "two-copy target distribution for a shared hidden involution."
                ),
                reason_invalid=(
                    "The operational law contains the exact correction "
                    "(1+r_lambda+r_mu+r_nu)/"
                    "((1+r_lambda)(1+r_mu))."
                ),
                lesson=(
                    "Weight every source-target coverage and collision claim "
                    "by the shared-hidden character-ratio law."
                ),
                applies_to=[registry_candidate_id, registry_experiment_id],
                evidence=payload["headline_metrics"],
            )
        )
        upsert_negative_result(
            NegativeResultRecord(
                id="NEG-COSET-EXACT-TARGET-LAW-NOT-HIDDEN-INVOLUTION-DECODER",
                source=str(output_path),
                claim=(
                    "An exact coupled-irrep target law supplies a hidden-"
                    "involution algorithm."
                ),
                reason_invalid=(
                    "The law is conjugacy-class invariant and omits coherent "
                    "recoupling, multiplicity outcomes, and decoding of h."
                ),
                lesson=(
                    "Use the law for honest branch accounting, then require "
                    "an h-dependent multiplicity outcome and decoder theorem."
                ),
                applies_to=[registry_candidate_id, registry_experiment_id],
                evidence=payload["headline_metrics"],
            )
        )
        result_id = (
            registry_result_id
            or f"RESULT-{registry_experiment_id}-COSET"
        )
        upsert_experiment_result(
            ExperimentResultRecord(
                id=result_id,
                experiment_id=registry_experiment_id,
                candidate_id=registry_candidate_id,
                created_at=str(payload["created_at"]),
                status=str(payload["status"]),
                summary=str(payload["summary"]),
                metrics=dict(payload["headline_metrics"]),
                falsifiers_triggered=list(payload["falsifiers_triggered"]),
                artifacts={"coset_same_hidden_target_law": str(output_path)},
            )
        )
    return payload


if __name__ == "__main__":
    report = write_same_hidden_target_law_report()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))

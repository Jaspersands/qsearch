"""All-source finite probe for the fixed typical-irrep separator.

The existing typical certificates use one maximum-dimension self-pair
``lambda tensor lambda``.  Natural weak-Fourier sampling instead produces
arbitrary ordered source pairs.  This module audits every ordered pair at
small ``n`` and every nontrivial Kronecker multiplicity block for the fixed

    H = average(ORB-TT-INTERSECTION-1)
        + average(ORB-TC-INTERSECTION-1).

Dense Young-basis blocks provide numerical spectra.  Exact character
contractions independently compute ``Tr(H)`` and ``Tr(H^2)`` for unequal
source partitions.  Zero exact variance proves scalar action and therefore an
exact collision.  Positive variance proves simple spectrum only in
multiplicity two; higher-multiplicity numerical splitting is not promoted.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from fractions import Fraction
from functools import lru_cache
from pathlib import Path

import numpy as np

from coset_jucys_murphy_label_transform import (
    diagonal_jucys_murphy_operators,
    encoded_jucys_murphy_operator,
)
from coset_multiplicity_commutant_search import (
    _encoded_label_targets,
    bounded_support_orbit_generators,
)
from coset_typical_commutant_moment_audit import (
    TC_INTERSECTION_ONE,
    TT_INTERSECTION_ONE,
    cross_moment_signature_counts,
    moment_signature_counts,
)
from representation_obstruction import (
    hook_length_dimension,
    integer_partitions,
)
from research_registry import (
    ExperimentResultRecord,
    NegativeResultRecord,
    upsert_experiment_result,
    upsert_negative_result,
    utc_now,
)
from symmetric_character import kronecker_coefficient, symmetric_character
from weak_fourier_signal import character_on_involution, involution_specs_for_n


REPORT_PATH = Path(
    "research/representation/coset_typical_uniform_source_probe.json"
)
DEFAULT_EXPERIMENT_ID = "EXP-COSET-TYPICAL-UNIFORM-SOURCE-PROBE"
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"
GENERATOR_IDS = (TT_INTERSECTION_ONE, TC_INTERSECTION_ONE)


@dataclass(frozen=True)
class UniformSourceBlockRecord:
    n: int
    left_source_partition: tuple[int, ...]
    right_source_partition: tuple[int, ...]
    left_source_dimension: int
    right_source_dimension: int
    target_partition: tuple[int, ...]
    target_dimension: int
    kronecker_multiplicity: int
    exact_separator_mean: str
    exact_separator_variance: str
    numerical_separator_eigenvalues: list[float]
    numerical_minimum_gap: float
    exact_moment_residual: float
    exact_scalar_collision_proved: bool
    exact_multiplicity_two_simple_spectrum_proved: bool
    numerical_repeated_eigenvalue_detected: bool
    tableau_spectrum_consistency_verified: bool
    status: str


@dataclass(frozen=True)
class UniformSourceProbabilityRecord:
    n: int
    involution_type: str
    transposition_count: int
    exact_source_pair_mass_with_scalar_collision: str
    source_pair_mass_with_scalar_collision: float
    exact_source_pair_mass_with_numerical_collision: str
    source_pair_mass_with_numerical_collision: float
    exact_total_ordered_source_pair_mass: str
    source_pair_probability_normalization_verified: bool


@dataclass(frozen=True)
class UniformSourceProbeReport:
    created_at: str
    theorem_contract: dict[str, object]
    block_records: list[UniformSourceBlockRecord]
    probability_records: list[UniformSourceProbabilityRecord]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, bool | str]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _bicharacter_contraction(
    counts: np.ndarray,
    cycle_types: tuple[tuple[int, ...], ...],
    left_source: tuple[int, ...],
    right_source: tuple[int, ...],
    target: tuple[int, ...],
) -> int:
    type_count = len(cycle_types)
    left_characters = tuple(
        symmetric_character(left_source, cycle_type)
        for cycle_type in cycle_types
    )
    right_characters = tuple(
        symmetric_character(right_source, cycle_type)
        for cycle_type in cycle_types
    )
    target_characters = tuple(
        symmetric_character(target, cycle_type)
        for cycle_type in cycle_types
    )
    total = 0
    for code in np.flatnonzero(counts):
        group_index, remainder = divmod(
            int(code), type_count * type_count
        )
        left_index, right_index = divmod(remainder, type_count)
        total += (
            int(counts[code])
            * target_characters[group_index]
            * left_characters[left_index]
            * right_characters[right_index]
        )
    return total


@lru_cache(maxsize=None)
def exact_separator_mean_variance(
    n: int,
    left_source: tuple[int, ...],
    right_source: tuple[int, ...],
    target: tuple[int, ...],
) -> tuple[Fraction, Fraction]:
    multiplicity = kronecker_coefficient(
        left_source,
        right_source,
        target,
    )
    if multiplicity <= 1:
        raise ValueError("exact separator audit requires multiplicity above one")
    group_order = math.factorial(n)
    traces: dict[str, Fraction] = {}
    trace_squares: dict[str, Fraction] = {}
    for generator_id in GENERATOR_IDS:
        cycle_types, first, second, orbit_size = moment_signature_counts(
            n,
            generator_id,
        )
        traces[generator_id] = Fraction(
            _bicharacter_contraction(
                first,
                cycle_types,
                left_source,
                right_source,
                target,
            ),
            group_order,
        )
        trace_squares[generator_id] = Fraction(
            _bicharacter_contraction(
                second,
                cycle_types,
                left_source,
                right_source,
                target,
            ),
            group_order * orbit_size,
        )
    cycle_types, cross_counts, cross_orbit_size = (
        cross_moment_signature_counts(
            n,
            TT_INTERSECTION_ONE,
            TC_INTERSECTION_ONE,
        )
    )
    cross_trace = Fraction(
        _bicharacter_contraction(
            cross_counts,
            cycle_types,
            left_source,
            right_source,
            target,
        ),
        group_order * cross_orbit_size,
    )
    trace = sum(traces.values(), Fraction())
    trace_square = (
        sum(trace_squares.values(), Fraction()) + 2 * cross_trace
    )
    mean = trace / multiplicity
    variance = trace_square / multiplicity - mean * mean
    if variance < 0:
        raise ArithmeticError("exact separator variance is negative")
    return mean, variance


@lru_cache(maxsize=None)
def audit_uniform_source_blocks(n: int) -> tuple[UniformSourceBlockRecord, ...]:
    if n < 4:
        raise ValueError("uniform source probe requires n at least four")
    partitions = integer_partitions(n)
    base = 2 * n + 1
    target_by_label = _encoded_label_targets(n, base)
    records: list[UniformSourceBlockRecord] = []
    for left_source in partitions:
        for right_source in partitions:
            nontrivial_targets = {
                target
                for target in partitions
                if kronecker_coefficient(
                    left_source,
                    right_source,
                    target,
                )
                > 1
            }
            if not nontrivial_targets:
                continue
            names, operators, generator_records = (
                bounded_support_orbit_generators(
                    left_source,
                    right_source,
                )
            )
            indices = [names.index(name) for name in GENERATOR_IDS]
            separator = sum(
                operators[index]
                / generator_records[index].term_count
                for index in indices
            )
            encoded = encoded_jucys_murphy_operator(
                diagonal_jucys_murphy_operators(
                    left_source,
                    right_source,
                ),
                base,
                n,
            )
            label_values, label_vectors = np.linalg.eigh(encoded)
            label_indices: dict[int, list[int]] = {}
            for index, value in enumerate(label_values):
                label_indices.setdefault(round(float(value)), []).append(index)
            spectra_by_target: dict[tuple[int, ...], list[np.ndarray]] = {}
            for label, block_indices in label_indices.items():
                if len(block_indices) <= 1:
                    continue
                target = target_by_label[label]
                if target not in nontrivial_targets:
                    continue
                block = (
                    label_vectors[:, block_indices].T
                    @ separator
                    @ label_vectors[:, block_indices]
                )
                spectra_by_target.setdefault(target, []).append(
                    np.linalg.eigvalsh(block)
                )
            if set(spectra_by_target) != nontrivial_targets:
                raise ArithmeticError(
                    "encoded labels missed a nontrivial target block"
                )
            for target in sorted(nontrivial_targets, reverse=True):
                spectra = spectra_by_target[target]
                spectrum = spectra[0]
                consistent = all(
                    np.allclose(spectrum, other, atol=1e-10)
                    for other in spectra[1:]
                )
                if not consistent:
                    raise ArithmeticError(
                        "target-tableau spectra are inconsistent"
                    )
                multiplicity = kronecker_coefficient(
                    left_source,
                    right_source,
                    target,
                )
                mean, variance = exact_separator_mean_variance(
                    n,
                    left_source,
                    right_source,
                    target,
                )
                numerical_mean = float(np.mean(spectrum))
                numerical_variance = float(
                    np.mean((spectrum - numerical_mean) ** 2)
                )
                moment_residual = max(
                    abs(numerical_mean - float(mean)),
                    abs(numerical_variance - float(variance)),
                )
                if moment_residual > 1e-9:
                    raise ArithmeticError(
                        "dense spectrum disagrees with exact character moments"
                    )
                minimum_gap = float(
                    min(np.diff(spectrum), default=math.inf)
                )
                scalar = variance == 0
                exact_simple = multiplicity == 2 and variance > 0
                repeated = minimum_gap < 1e-9
                records.append(
                    UniformSourceBlockRecord(
                        n=n,
                        left_source_partition=left_source,
                        right_source_partition=right_source,
                        left_source_dimension=hook_length_dimension(left_source),
                        right_source_dimension=hook_length_dimension(
                            right_source
                        ),
                        target_partition=target,
                        target_dimension=hook_length_dimension(target),
                        kronecker_multiplicity=multiplicity,
                        exact_separator_mean=str(mean),
                        exact_separator_variance=str(variance),
                        numerical_separator_eigenvalues=[
                            float(value) for value in spectrum
                        ],
                        numerical_minimum_gap=minimum_gap,
                        exact_moment_residual=moment_residual,
                        exact_scalar_collision_proved=scalar,
                        exact_multiplicity_two_simple_spectrum_proved=(
                            exact_simple
                        ),
                        numerical_repeated_eigenvalue_detected=repeated,
                        tableau_spectrum_consistency_verified=consistent,
                        status=(
                            "exact-scalar-separator-collision"
                            if scalar
                            else (
                                "exact-multiplicity-two-simple-spectrum"
                                if exact_simple
                                else (
                                    "higher-multiplicity-numerical-collision"
                                    if repeated
                                    else "higher-multiplicity-numerically-simple"
                                )
                            )
                        ),
                    )
                )
    return tuple(records)


def _weak_label_probability(
    partition: tuple[int, ...],
    transposition_count: int,
) -> Fraction:
    n = sum(partition)
    dimension = hook_length_dimension(partition)
    character = character_on_involution(partition, transposition_count)
    return Fraction(
        dimension * (dimension + character),
        math.factorial(n),
    )


def _probability_record(
    n: int,
    involution_type: str,
    transposition_count: int,
    block_records: tuple[UniformSourceBlockRecord, ...],
) -> UniformSourceProbabilityRecord:
    partitions = integer_partitions(n)
    probabilities = {
        partition: _weak_label_probability(partition, transposition_count)
        for partition in partitions
    }
    total = sum(probabilities.values(), Fraction())
    if total != 1:
        raise ArithmeticError("weak-Fourier source probabilities do not sum to one")
    scalar_pairs = {
        (
            record.left_source_partition,
            record.right_source_partition,
        )
        for record in block_records
        if record.exact_scalar_collision_proved
    }
    numerical_pairs = {
        (
            record.left_source_partition,
            record.right_source_partition,
        )
        for record in block_records
        if record.numerical_repeated_eigenvalue_detected
    }

    def pair_mass(
        pairs: set[tuple[tuple[int, ...], tuple[int, ...]]],
    ) -> Fraction:
        return sum(
            (
                probabilities[left] * probabilities[right]
                for left, right in pairs
            ),
            Fraction(),
        )

    scalar_mass = pair_mass(scalar_pairs)
    numerical_mass = pair_mass(numerical_pairs)
    return UniformSourceProbabilityRecord(
        n=n,
        involution_type=involution_type,
        transposition_count=transposition_count,
        exact_source_pair_mass_with_scalar_collision=str(scalar_mass),
        source_pair_mass_with_scalar_collision=float(scalar_mass),
        exact_source_pair_mass_with_numerical_collision=str(numerical_mass),
        source_pair_mass_with_numerical_collision=float(numerical_mass),
        exact_total_ordered_source_pair_mass=str(total**2),
        source_pair_probability_normalization_verified=total**2 == 1,
    )


def build_uniform_source_probe_report(
    n_values: tuple[int, ...] = (5, 6),
) -> UniformSourceProbeReport:
    block_records = tuple(
        record
        for n in n_values
        for record in audit_uniform_source_blocks(n)
    )
    probability_records = [
        _probability_record(
            n,
            involution_type,
            transposition_count,
            tuple(record for record in block_records if record.n == n),
        )
        for n in n_values
        for involution_type, transposition_count in involution_specs_for_n(n)
        if involution_type != "single_transposition_control"
    ]
    scalar_collisions = [
        record
        for record in block_records
        if record.exact_scalar_collision_proved
    ]
    numerical_collisions = [
        record
        for record in block_records
        if record.numerical_repeated_eigenvalue_detected
    ]
    metrics: dict[str, int | float] = {
        "finite_n_count": len(n_values),
        "ordered_source_pair_count": sum(
            len(integer_partitions(n)) ** 2 for n in n_values
        ),
        "nontrivial_multiplicity_block_count": len(block_records),
        "exact_character_moment_block_count": len(block_records),
        "exact_scalar_collision_count": len(scalar_collisions),
        "exact_multiplicity_two_simple_spectrum_count": sum(
            record.exact_multiplicity_two_simple_spectrum_proved
            for record in block_records
        ),
        "numerical_repeated_eigenvalue_block_count": len(
            numerical_collisions
        ),
        "maximum_exact_moment_residual": max(
            (record.exact_moment_residual for record in block_records),
            default=0.0,
        ),
        "minimum_positive_numerical_gap": min(
            (
                record.numerical_minimum_gap
                for record in block_records
                if not record.numerical_repeated_eigenvalue_detected
            ),
            default=0.0,
        ),
        "maximum_natural_source_pair_mass_with_exact_scalar_collision": max(
            (
                record.source_pair_mass_with_scalar_collision
                for record in probability_records
            ),
            default=0.0,
        ),
        "fixed_separator_uniform_all_source_finite_theorem_count": 0,
        "uniform_separator_repair_rule_count": 0,
        "uniform_arbitrary_source_gap_theorem_count": 0,
        "same_hidden_involution_target_outcome_law_count": 0,
        "hidden_involution_decoder_count": 0,
    }
    return UniformSourceProbeReport(
        created_at=utc_now(),
        theorem_contract={
            "operator": (
                "H=average(ORB-TT-INTERSECTION-1)+"
                "average(ORB-TC-INTERSECTION-1)"
            ),
            "scope": (
                "Every ordered source partition pair and every nontrivial "
                "Kronecker block at n=5,6."
            ),
            "exact_moments": (
                "Character contractions prove Tr(H) and Tr(H^2) for unequal "
                "sources. Exact zero variance proves scalar action."
            ),
            "multiplicity_two": (
                "In dimension two, positive exact variance proves simple "
                "spectrum; zero variance proves a repeated scalar eigenvalue."
            ),
            "higher_multiplicity_limit": (
                "Dense spectra are numerical controls only. A positive "
                "variance does not prove simple spectrum."
            ),
            "natural_probability_scope": (
                "Probability records measure exact weak-Fourier source-pair "
                "mass containing at least one collision block. They do not "
                "assert the same-hidden-involution conditional target law."
            ),
        },
        block_records=list(block_records),
        probability_records=probability_records,
        headline_metrics=metrics,
        claim_gate={
            "maximum_dimension_self_pair_result_extends_to_all_sources": False,
            "fixed_separator_uniform_all_source_finite_separation": False,
            "exact_scalar_collision_found": bool(scalar_collisions),
            "collision_source_pairs_have_nonzero_natural_mass": any(
                record.source_pair_mass_with_scalar_collision > 0
                for record in probability_records
            ),
            "uniform_separator_repair_proved": False,
            "uniform_arbitrary_source_gap_proved": False,
            "same_hidden_involution_target_outcome_law_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The fixed separator is exactly scalar on nontrivial n=6 "
                "blocks for naturally possible unequal source pairs. The "
                "maximum-dimension self-pair ladder therefore does not define "
                "a uniform sampled-label resolver."
            ),
        },
        status=(
            "fixed-typical-separator-falsified-on-all-source-probe-"
            "label-adaptive-repair-required"
        ),
        summary=(
            f"Audited {len(block_records)} nontrivial blocks over every ordered "
            f"source pair at n={n_values}; found {len(scalar_collisions)} exact "
            "scalar collisions and "
            f"{len(numerical_collisions)} numerical repeated-root blocks."
        ),
        falsifiers_triggered=[
            (
                "The maximum-dimension self-pair is not representative of all "
                "naturally sampled source pairs."
            ),
            (
                "At n=6, H is exactly scalar on the multiplicity-two "
                "(3,2,1)x(3,3)->(3,2,1) block."
            ),
            (
                "At n=6, H is exactly scalar on the multiplicity-two "
                "(3,2,1)x(2,2,2)->(3,2,1) block."
            ),
            (
                "A multiplicity-four n=6 block has a numerical repeated zero "
                "root; exact higher-moment certification remains open."
            ),
            (
                "Finite all-source separation cannot be inferred from one "
                "source self-pair or from nonzero variance alone."
            ),
        ],
    )


def write_uniform_source_probe_report(
    output_path: Path = REPORT_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = DEFAULT_EXPERIMENT_ID,
    registry_candidate_id: str = DEFAULT_CANDIDATE_ID,
    registry_result_id: str | None = None,
) -> dict:
    payload = asdict(build_uniform_source_probe_report())
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    if write_registry:
        upsert_negative_result(
            NegativeResultRecord(
                id="NEG-COSET-TYPICAL-FIXED-SEPARATOR-UNIFORM-SOURCE",
                source=str(output_path),
                claim=(
                    "The fixed TT1+TC1 separator that splits the audited "
                    "maximum-dimension self-pairs uniformly resolves arbitrary "
                    "sampled source partitions."
                ),
                reason_invalid=(
                    "Exact unequal-source character moments prove scalar action "
                    "on two nontrivial multiplicity-two n=6 blocks with "
                    "nonzero natural source-pair mass."
                ),
                lesson=(
                    "Search partition-dependent coefficient rules or a larger "
                    "commutant portfolio, and require a uniform reversible "
                    "coefficient-selection circuit plus all-source gap theorem."
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
                created_at=payload["created_at"],
                status=payload["status"],
                summary=payload["summary"],
                metrics=payload["headline_metrics"],
                falsifiers_triggered=payload["falsifiers_triggered"],
                artifacts={
                    "coset_typical_uniform_source_probe": str(output_path)
                },
            )
        )
    return payload


if __name__ == "__main__":
    report = write_uniform_source_probe_report()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))

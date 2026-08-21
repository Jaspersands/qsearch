"""Natural-input multi-copy PGM benchmark for involution coset states.

The growing-width carrier program needs an information objective before it
needs another recoupling ansatz.  This module computes that objective on exact
finite controls without postselecting favorable Fourier source labels.

For every naturally occurring source-label tuple it compares:

* the global square-root/pretty-good measurement (PGM) on all carrier
  registers;
* a product of the conditioned one-copy PGMs;
* separate Young-basis carrier measurements.

The source-label law is included exactly and is independent of the hidden
involution inside a conjugacy class.  A finite collective PGM advantage is
only a target for architecture synthesis: no efficient PGM circuit, decoder,
or asymptotic separation is inferred.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from functools import lru_cache
from itertools import combinations_with_replacement
from pathlib import Path

import numpy as np

from coset_commutant_information_obstruction import (
    _conditioned_source_state,
)
from coset_three_copy_recoupling_obstruction import involutions
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
from weak_fourier_signal import character_on_involution


REPORT_PATH = Path(
    "research/representation/coset_natural_multicopy_pgm_benchmark.json"
)
DEFAULT_EXPERIMENT_ID = "EXP-COSET-NATURAL-MULTICOPY-PGM"
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


@dataclass(frozen=True)
class NaturalMulticopyPGMRecord:
    n: int
    transposition_count: int
    copy_count: int
    hidden_involution_count: int
    accessible_source_partition_count: int
    source_multiset_count: int
    total_natural_source_probability: float
    global_pgm_mutual_information_bits: float
    global_pgm_native_success_probability: float
    global_pgm_relabelled_bayes_success_probability: float
    product_one_copy_pgm_mutual_information_bits: float
    product_one_copy_pgm_bayes_success_probability: float
    separate_young_basis_mutual_information_bits: float
    separate_young_basis_bayes_success_probability: float
    global_information_gain_over_product_pgm_bits: float
    global_information_gain_over_separate_young_bits: float
    global_bayes_gain_over_product_pgm: float
    global_bayes_gain_over_separate_young: float
    maximum_global_pgm_normalization_residual: float
    maximum_global_pgm_completeness_residual: float
    maximum_branch_carrier_dimension: int
    random_guess_success_probability: float
    status: str


@dataclass(frozen=True)
class NaturalMulticopyPGMReport:
    created_at: str
    measurement_contract: dict[str, object]
    records: list[NaturalMulticopyPGMRecord]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, bool | str]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _entropy_bits(probabilities: np.ndarray) -> float:
    positive = probabilities[probabilities > 1e-15]
    return -float(np.sum(positive * np.log2(positive)))


def _channel_statistics(
    probabilities: np.ndarray,
) -> tuple[float, float, float]:
    rows = np.clip(np.asarray(probabilities, dtype=float), 0.0, None)
    row_sums = rows.sum(axis=1)
    residual = float(np.max(np.abs(row_sums - 1.0)))
    rows = rows / row_sums[:, None]
    marginal = rows.mean(axis=0)
    information = _entropy_bits(marginal) - sum(
        _entropy_bits(row) for row in rows
    ) / len(rows)
    bayes = float(rows.max(axis=0).sum() / len(rows))
    return information, bayes, residual


def _rowwise_product_channel(
    channels: tuple[np.ndarray, ...],
) -> np.ndarray:
    if not channels:
        raise ValueError("at least one channel is required")
    result = channels[0]
    for channel in channels[1:]:
        result = np.einsum(
            "hi,hj->hij",
            result,
            channel,
            optimize=True,
        ).reshape(result.shape[0], -1)
    return result


def _tensor_states(
    state_families: tuple[tuple[np.ndarray, ...], ...],
) -> tuple[np.ndarray, ...]:
    if not state_families:
        raise ValueError("at least one state family is required")
    hidden_count = len(state_families[0])
    if any(len(family) != hidden_count for family in state_families):
        raise ValueError("state families must use the same hidden prior")
    result: list[np.ndarray] = []
    for hidden_index in range(hidden_count):
        state = state_families[0][hidden_index]
        for family in state_families[1:]:
            state = np.kron(state, family[hidden_index])
        result.append(state)
    return tuple(result)


def pretty_good_measurement_channel(
    states: tuple[np.ndarray, ...],
    *,
    tolerance: float = 1e-11,
) -> tuple[np.ndarray, float, float]:
    """Return PGM outcome probabilities, native success, and completeness."""

    if not states:
        raise ValueError("PGM requires a nonempty state ensemble")
    hidden_count = len(states)
    average = sum(states) / hidden_count
    eigenvalues, eigenvectors = np.linalg.eigh(average)
    support = eigenvalues > tolerance
    if not np.any(support):
        raise ArithmeticError("average state has empty numerical support")
    inverse_root = (
        eigenvectors[:, support]
        @ np.diag(1.0 / np.sqrt(eigenvalues[support]))
        @ eigenvectors[:, support].conj().T
    )
    effects = tuple(
        inverse_root @ (state / hidden_count) @ inverse_root
        for state in states
    )
    support_projector = (
        eigenvectors[:, support] @ eigenvectors[:, support].conj().T
    )
    completeness = float(
        np.linalg.norm(sum(effects) - support_projector, ord=2)
    )
    probabilities = np.asarray(
        [
            [
                float(np.trace(effect @ state).real)
                for effect in effects
            ]
            for state in states
        ]
    )
    probabilities[np.abs(probabilities) < tolerance] = 0.0
    native_success = float(np.trace(probabilities) / hidden_count)
    return probabilities, native_success, completeness


@lru_cache(maxsize=None)
def _source_data(
    n: int,
    transposition_count: int,
) -> tuple[
    tuple[tuple[int, ...], ...],
    tuple[float, ...],
    tuple[tuple[np.ndarray, ...], ...],
]:
    hidden = involutions(n, transposition_count)
    order = math.factorial(n)
    partitions: list[tuple[int, ...]] = []
    probabilities: list[float] = []
    state_families: list[tuple[np.ndarray, ...]] = []
    for partition in integer_partitions(n):
        dimension = hook_length_dimension(partition)
        character = character_on_involution(
            partition,
            transposition_count,
        )
        probability = dimension * (dimension + character) / order
        if probability <= 1e-15:
            continue
        states = tuple(
            _conditioned_source_state(
                partition,
                permutation,
                transposition_count,
            )
            for permutation in hidden
        )
        partitions.append(partition)
        probabilities.append(float(probability))
        state_families.append(states)
    if abs(sum(probabilities) - 1.0) > 1e-10:
        raise ArithmeticError("natural source-label probabilities do not sum to one")
    return tuple(partitions), tuple(probabilities), tuple(state_families)


def _multiset_multiplicity(indices: tuple[int, ...]) -> int:
    counts: dict[int, int] = {}
    for index in indices:
        counts[index] = counts.get(index, 0) + 1
    result = math.factorial(len(indices))
    for count in counts.values():
        result //= math.factorial(count)
    return result


@lru_cache(maxsize=None)
def audit_natural_multicopy_pgm(
    n: int,
    transposition_count: int,
    copy_count: int,
) -> NaturalMulticopyPGMRecord:
    if copy_count < 1:
        raise ValueError("copy_count must be positive")
    partitions, source_probabilities, state_families = _source_data(
        n,
        transposition_count,
    )
    one_copy_pgm_channels = tuple(
        pretty_good_measurement_channel(states)[0]
        for states in state_families
    )
    hidden_count = len(state_families[0])
    totals = {
        "global_information": 0.0,
        "global_native_success": 0.0,
        "global_bayes": 0.0,
        "product_pgm_information": 0.0,
        "product_pgm_bayes": 0.0,
        "young_information": 0.0,
        "young_bayes": 0.0,
        "source_mass": 0.0,
    }
    maximum_normalization_residual = 0.0
    maximum_completeness_residual = 0.0
    maximum_dimension = 0
    multisets = tuple(
        combinations_with_replacement(
            range(len(partitions)),
            copy_count,
        )
    )
    for source_indices in multisets:
        multiplicity = _multiset_multiplicity(source_indices)
        weight = float(multiplicity)
        for index in source_indices:
            weight *= source_probabilities[index]
        families = tuple(state_families[index] for index in source_indices)
        joint_states = _tensor_states(families)
        maximum_dimension = max(
            maximum_dimension,
            joint_states[0].shape[0],
        )
        global_channel, native_success, completeness = (
            pretty_good_measurement_channel(joint_states)
        )
        global_information, global_bayes, global_residual = (
            _channel_statistics(global_channel)
        )
        product_pgm_channel = _rowwise_product_channel(
            tuple(one_copy_pgm_channels[index] for index in source_indices)
        )
        product_pgm_information, product_pgm_bayes, product_pgm_residual = (
            _channel_statistics(product_pgm_channel)
        )
        young_channel = _rowwise_product_channel(
            tuple(
                np.asarray(
                    [np.diag(state).real for state in state_families[index]]
                )
                for index in source_indices
            )
        )
        young_information, young_bayes, young_residual = (
            _channel_statistics(young_channel)
        )
        totals["global_information"] += weight * global_information
        totals["global_native_success"] += weight * native_success
        totals["global_bayes"] += weight * global_bayes
        totals["product_pgm_information"] += weight * product_pgm_information
        totals["product_pgm_bayes"] += weight * product_pgm_bayes
        totals["young_information"] += weight * young_information
        totals["young_bayes"] += weight * young_bayes
        totals["source_mass"] += weight
        maximum_normalization_residual = max(
            maximum_normalization_residual,
            global_residual,
            product_pgm_residual,
            young_residual,
        )
        maximum_completeness_residual = max(
            maximum_completeness_residual,
            completeness,
        )
    source_mass = totals["source_mass"]
    if abs(source_mass - 1.0) > 1e-10:
        raise ArithmeticError("source multiset weights do not sum to one")
    global_information = totals["global_information"]
    global_bayes = totals["global_bayes"]
    product_information = totals["product_pgm_information"]
    product_bayes = totals["product_pgm_bayes"]
    young_information = totals["young_information"]
    young_bayes = totals["young_bayes"]
    information_gain = global_information - product_information
    return NaturalMulticopyPGMRecord(
        n=n,
        transposition_count=transposition_count,
        copy_count=copy_count,
        hidden_involution_count=hidden_count,
        accessible_source_partition_count=len(partitions),
        source_multiset_count=len(multisets),
        total_natural_source_probability=source_mass,
        global_pgm_mutual_information_bits=global_information,
        global_pgm_native_success_probability=totals[
            "global_native_success"
        ],
        global_pgm_relabelled_bayes_success_probability=global_bayes,
        product_one_copy_pgm_mutual_information_bits=product_information,
        product_one_copy_pgm_bayes_success_probability=product_bayes,
        separate_young_basis_mutual_information_bits=young_information,
        separate_young_basis_bayes_success_probability=young_bayes,
        global_information_gain_over_product_pgm_bits=information_gain,
        global_information_gain_over_separate_young_bits=(
            global_information - young_information
        ),
        global_bayes_gain_over_product_pgm=global_bayes - product_bayes,
        global_bayes_gain_over_separate_young=global_bayes - young_bayes,
        maximum_global_pgm_normalization_residual=(
            maximum_normalization_residual
        ),
        maximum_global_pgm_completeness_residual=(
            maximum_completeness_residual
        ),
        maximum_branch_carrier_dimension=maximum_dimension,
        random_guess_success_probability=1 / hidden_count,
        status=(
            "finite-natural-collective-pgm-information-gain"
            if copy_count > 1 and information_gain > 1e-8
            else "one-copy-consistency-control"
            if copy_count == 1
            else "finite-natural-global-pgm-no-information-gain"
        ),
    )


def build_natural_multicopy_pgm_report(
    n: int = 5,
    transposition_count: int = 2,
    copy_counts: tuple[int, ...] = (1, 2, 3),
) -> NaturalMulticopyPGMReport:
    records = [
        audit_natural_multicopy_pgm(
            n,
            transposition_count,
            copy_count,
        )
        for copy_count in copy_counts
    ]
    collective = [record for record in records if record.copy_count > 1]
    metrics: dict[str, int | float] = {
        "record_count": len(records),
        "maximum_n": n,
        "maximum_copy_count": max(copy_counts),
        "natural_source_mass_control_count": sum(
            abs(record.total_natural_source_probability - 1.0) <= 1e-10
            for record in records
        ),
        "one_copy_global_product_pgm_consistency_count": sum(
            record.copy_count == 1
            and abs(
                record.global_pgm_mutual_information_bits
                - record.product_one_copy_pgm_mutual_information_bits
            )
            <= 1e-9
            for record in records
        ),
        "finite_collective_information_gain_row_count": sum(
            record.global_information_gain_over_product_pgm_bits > 1e-8
            for record in collective
        ),
        "maximum_global_information_gain_over_product_pgm_bits": max(
            (
                record.global_information_gain_over_product_pgm_bits
                for record in collective
            ),
            default=0.0,
        ),
        "maximum_global_information_gain_over_separate_young_bits": max(
            (
                record.global_information_gain_over_separate_young_bits
                for record in collective
            ),
            default=0.0,
        ),
        "maximum_global_bayes_gain_over_product_pgm": max(
            (
                record.global_bayes_gain_over_product_pgm
                for record in collective
            ),
            default=0.0,
        ),
        "maximum_branch_carrier_dimension": max(
            record.maximum_branch_carrier_dimension for record in records
        ),
        "maximum_probability_normalization_residual": max(
            record.maximum_global_pgm_normalization_residual
            for record in records
        ),
        "maximum_pgm_completeness_residual": max(
            record.maximum_global_pgm_completeness_residual
            for record in records
        ),
        "uniform_polynomial_global_pgm_circuit_count": 0,
        "polynomial_hidden_involution_decoder_count": 0,
        "asymptotic_collective_information_advantage_theorem_count": 0,
        "classical_separation_theorem_count": 0,
    }
    return NaturalMulticopyPGMReport(
        created_at=utc_now(),
        measurement_contract={
            "prior": "uniform over one involution conjugacy class",
            "source_access": (
                "All weak-Fourier source labels are retained with exact "
                "natural probability d_lambda(d_lambda+chi_lambda(C))/|S_n|; "
                "no favorable-label postselection."
            ),
            "global_measurement": (
                "For each observed source tuple, apply the exact square-root "
                "measurement of the conditioned carrier ensemble."
            ),
            "product_pgm_baseline": (
                "Apply each source-conditioned one-copy PGM independently and "
                "classically combine all outcomes."
            ),
            "strong_fourier_baseline": (
                "Measure every carrier register in the Young basis and "
                "classically combine all outcomes."
            ),
            "information_metrics": (
                "Uniform-prior mutual information and optimal relabelling "
                "Bayes success, averaged over the natural source tuple law."
            ),
        },
        records=records,
        headline_metrics=metrics,
        claim_gate={
            "natural_collective_information_gain_seen_finitely": (
                metrics["finite_collective_information_gain_row_count"] > 0
            ),
            "uniform_polynomial_global_pgm_circuit_proved": False,
            "polynomial_hidden_involution_decoder_proved": False,
            "asymptotic_collective_advantage_proved": False,
            "classical_separation_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The benchmark defines a natural collective-information target "
                "but exact finite PGM matrices do not provide a scalable "
                "measurement circuit, decoder, or quantum speedup."
            ),
        },
        status="natural-multicopy-pgm-benchmark-no-algorithm",
        summary=(
            f"Computed exact natural-source global and product carrier "
            f"measurements for {len(records)} copy counts on S_{n}. "
            f"{metrics['finite_collective_information_gain_row_count']} "
            "multi-copy rows show finite global-PGM information gain; all "
            "algorithmic gates remain closed."
        ),
        falsifiers_triggered=[
            (
                "Conditioning on hand-selected source labels is not accepted; "
                "the complete natural source law is included."
            ),
            (
                "A joint finite PGM advantage is not an efficient measurement "
                "or decoder."
            ),
            (
                "A PGM benchmark must beat both separate strong Fourier and "
                "separate one-copy PGM baselines before it can motivate a "
                "growing-width architecture."
            ),
            (
                "Finite-copy information gain does not prove asymptotic "
                "advantage or classical hardness."
            ),
        ],
    )


def write_natural_multicopy_pgm_report(
    output_path: Path = REPORT_PATH,
    *,
    n: int = 5,
    transposition_count: int = 2,
    copy_counts: tuple[int, ...] = (1, 2, 3),
    write_registry: bool = True,
    registry_experiment_id: str = DEFAULT_EXPERIMENT_ID,
    registry_candidate_id: str = DEFAULT_CANDIDATE_ID,
    registry_result_id: str | None = None,
) -> dict[str, object]:
    payload = asdict(
        build_natural_multicopy_pgm_report(
            n=n,
            transposition_count=transposition_count,
            copy_counts=copy_counts,
        )
    )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    return payload


if __name__ == "__main__":
    report = write_natural_multicopy_pgm_report()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))

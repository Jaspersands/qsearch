"""Quantized tensor-train search for dense subset-sum contractions.

The exact density-one subset-sum count vector has length ``N=2^n``:

    F_a(t) = |{x in {0,1}^m : <a,x>=t mod N}|.

Reshaping the target index into ``n`` binary axes turns this vector into an
order-``n`` tensor.  A quantized tensor train (QTT) with polynomial bond
dimension would be a concrete way to contract exponentially many Fourier
characters without materializing all ``N`` terms.

For every target-bit ordering and cut, the singular values of the corresponding
matricization give exact lower bounds on any QTT crossing that cut.  In
particular, entrywise additive error below ``1/2`` implies Frobenius error below
``sqrt(N)/2``.  If the best rank-``R`` matricization approximation has larger
Frobenius error, no QTT of bond ``R`` can support exact integer count recovery
under that ordering.

This is a finite source-native architecture audit, not an asymptotic tensor-rank
lower bound.  It compares exact subset-sum count tensors with
histogram-preserving random permutations, searches several fixed and random bit
orders, and keeps witness extraction and subinstance stability as explicit
proof obligations.
"""

from __future__ import annotations

import json
import math
import random
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Sequence

import numpy as np

from research_registry import (
    ExperimentResultRecord,
    NegativeResultRecord,
    upsert_experiment_result,
    upsert_negative_result,
    utc_now,
)


DCP_SUBSET_SUM_QTT_PATH = Path(
    "research/classical_baselines/dcp_subset_sum_qtt_contraction_search.json"
)
DEFAULT_EXPERIMENT_ID = "EXP-DHS-DCP-SUBSET-SUM-QTT-DENSE-CONTRACTION"
DEFAULT_CANDIDATE_ID = "DHS-GOWERS-SIEVE"


@dataclass(frozen=True)
class QTTAccessContract:
    input: str
    tensorization: str
    legal_preprocessing: str
    positive_interface: str
    hidden_costs_rejected: list[str]


@dataclass(frozen=True)
class QTTUnfoldingRow:
    n_bits: int
    register_count: int
    trial: int
    vector_kind: str
    ordering_id: str
    cut: int
    left_dimension: int
    right_dimension: int
    exact_rank: int
    maximum_rank: int
    exact_rank_fraction: float
    stable_rank: float
    additive_half_required_rank: int
    additive_half_required_rank_fraction: float
    registered_bond_cap: int
    registered_cap_frobenius_error: float
    additive_half_frobenius_threshold: float
    registered_cap_additive_half_impossible: bool
    singular_entropy_bits: float


@dataclass(frozen=True)
class QTTApproximationRow:
    n_bits: int
    register_count: int
    trial: int
    vector_kind: str
    ordering_id: str
    registered_bond_cap: int
    maximum_realized_bond: int
    legal_target_count: int
    legal_target_fraction: float
    additive_half_legal_target_coverage: float
    zero_frequency_constant_count: int
    zero_frequency_constant_legal_target_coverage: float
    coverage_excess_over_zero_frequency_constant: float
    relative_frobenius_error: float
    construction_materializes_full_vector: bool
    witness_decoder_available: bool


@dataclass(frozen=True)
class QTTInstanceSummary:
    n_bits: int
    register_count: int
    trial: int
    label_digest: str
    count_mean: float
    count_variance: float
    maximum_count: int
    ordering_count: int
    best_source_required_rank: int
    best_permuted_required_rank: int
    source_to_permuted_best_rank_ratio: float
    source_registered_cap_survivor_count: int
    permuted_registered_cap_survivor_count: int
    best_source_qtt_legal_coverage: float
    best_permuted_qtt_legal_coverage: float
    zero_frequency_constant_legal_coverage: float
    source_qtt_coverage_excess_over_zero_frequency_constant: float
    source_qtt_coverage_excess_over_permuted: float


@dataclass(frozen=True)
class DCPSubsetSumQTTReport:
    created_at: str
    access_contract: QTTAccessContract
    rows: list[QTTUnfoldingRow]
    approximation_rows: list[QTTApproximationRow]
    instances: list[QTTInstanceSummary]
    scaling_fits: dict[str, float | int | str]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, bool | str]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def exact_cyclic_subset_sum_counts(
    labels: Sequence[int],
    modulus: int,
) -> np.ndarray:
    if modulus < 2 or modulus & (modulus - 1):
        raise ValueError("modulus must be a power of two")
    if any(not 0 <= int(label) < modulus for label in labels):
        raise ValueError("label outside modulus")
    counts = np.zeros(modulus, dtype=np.int64)
    counts[0] = 1
    for label in labels:
        counts = counts + np.roll(counts, int(label))
    return counts


def target_bit_orderings(
    n_bits: int,
    random_order_count: int,
    seed: int,
) -> list[tuple[str, tuple[int, ...]]]:
    if n_bits < 2 or random_order_count < 0:
        raise ValueError("invalid ordering parameters")
    natural = tuple(range(n_bits))
    even_odd = tuple(range(0, n_bits, 2)) + tuple(range(1, n_bits, 2))
    odd_even = tuple(range(1, n_bits, 2)) + tuple(range(0, n_bits, 2))
    center_out = tuple(
        sorted(
            range(n_bits),
            key=lambda index: (abs(2 * index - (n_bits - 1)), index),
        )
    )
    records = [
        ("natural", natural),
        ("reversed", tuple(reversed(natural))),
        ("even-odd", even_odd),
        ("odd-even", odd_even),
        ("center-out", center_out),
    ]
    rng = random.Random(seed)
    seen = {order for _, order in records}
    attempts = 0
    while len(records) < 5 + random_order_count and attempts < 1000:
        attempts += 1
        order_list = list(natural)
        rng.shuffle(order_list)
        order = tuple(order_list)
        if order in seen:
            continue
        seen.add(order)
        records.append((f"random-{len(records) - 5}", order))
    return records


def _singular_entropy_bits(singular_values: np.ndarray) -> float:
    energies = np.square(singular_values)
    total = float(np.sum(energies))
    if total <= 0.0:
        return 0.0
    probabilities = energies / total
    positive = probabilities[probabilities > 0.0]
    return float(-np.sum(positive * np.log2(positive)))


def unfolding_row(
    vector: np.ndarray,
    *,
    n_bits: int,
    register_count: int,
    trial: int,
    vector_kind: str,
    ordering_id: str,
    ordering: Sequence[int],
    cut: int,
    registered_bond_power: int,
) -> QTTUnfoldingRow:
    modulus = 1 << n_bits
    if vector.shape != (modulus,):
        raise ValueError("vector length does not match n_bits")
    if tuple(sorted(ordering)) != tuple(range(n_bits)):
        raise ValueError("ordering is not a target-bit permutation")
    if not 0 < cut < n_bits:
        raise ValueError("cut must be internal")
    tensor = vector.astype(np.float64).reshape((2,) * n_bits)
    matrix = np.transpose(tensor, tuple(ordering)).reshape(
        1 << cut,
        1 << (n_bits - cut),
    )
    singular_values = np.linalg.svd(matrix, compute_uv=False)
    maximum_rank = min(matrix.shape)
    tolerance = (
        max(matrix.shape)
        * np.finfo(np.float64).eps
        * (float(singular_values[0]) if len(singular_values) else 0.0)
    )
    exact_rank = int(np.sum(singular_values > tolerance))
    energies = np.square(singular_values)
    tail_energies = np.concatenate(
        ([float(np.sum(energies))], np.cumsum(energies[::-1])[:-1][::-1])
    )
    additive_threshold = math.sqrt(modulus) / 2.0
    required_rank = next(
        (
            rank
            for rank, tail_energy in enumerate(tail_energies)
            if math.sqrt(max(0.0, float(tail_energy))) < additive_threshold
        ),
        maximum_rank,
    )
    registered_cap = min(maximum_rank, max(1, n_bits**registered_bond_power))
    registered_tail_energy = (
        float(np.sum(energies[registered_cap:]))
        if registered_cap < len(energies)
        else 0.0
    )
    registered_error = math.sqrt(max(0.0, registered_tail_energy))
    frobenius_squared = float(np.sum(energies))
    spectral_squared = float(energies[0]) if len(energies) else 0.0
    stable_rank = (
        frobenius_squared / spectral_squared if spectral_squared > 0.0 else 0.0
    )
    return QTTUnfoldingRow(
        n_bits=n_bits,
        register_count=register_count,
        trial=trial,
        vector_kind=vector_kind,
        ordering_id=ordering_id,
        cut=cut,
        left_dimension=matrix.shape[0],
        right_dimension=matrix.shape[1],
        exact_rank=exact_rank,
        maximum_rank=maximum_rank,
        exact_rank_fraction=exact_rank / maximum_rank,
        stable_rank=stable_rank,
        additive_half_required_rank=required_rank,
        additive_half_required_rank_fraction=required_rank / maximum_rank,
        registered_bond_cap=registered_cap,
        registered_cap_frobenius_error=registered_error,
        additive_half_frobenius_threshold=additive_threshold,
        registered_cap_additive_half_impossible=(
            registered_error >= additive_threshold
        ),
        singular_entropy_bits=_singular_entropy_bits(singular_values),
    )


def qtt_svd_approximation(
    vector: np.ndarray,
    *,
    n_bits: int,
    ordering: Sequence[int],
    bond_cap: int,
) -> tuple[np.ndarray, list[int]]:
    modulus = 1 << n_bits
    if vector.shape != (modulus,):
        raise ValueError("vector length does not match n_bits")
    if tuple(sorted(ordering)) != tuple(range(n_bits)):
        raise ValueError("ordering is not a target-bit permutation")
    if bond_cap < 1:
        raise ValueError("bond cap must be positive")
    tensor = np.transpose(
        vector.reshape((2,) * n_bits),
        tuple(ordering),
    )
    cores: list[np.ndarray] = []
    realized_bonds: list[int] = []
    current = tensor
    previous_rank = 1
    for _ in range(n_bits - 1):
        matrix = current.reshape(previous_rank * 2, -1)
        left, singular_values, right = np.linalg.svd(
            matrix,
            full_matrices=False,
        )
        rank = min(bond_cap, len(singular_values))
        cores.append(left[:, :rank].reshape(previous_rank, 2, rank))
        current = singular_values[:rank, None] * right[:rank, :]
        realized_bonds.append(rank)
        previous_rank = rank
    cores.append(current.reshape(previous_rank, 2, 1))
    reconstructed = cores[0]
    for core in cores[1:]:
        reconstructed = np.tensordot(
            reconstructed,
            core,
            axes=([-1], [0]),
        )
    ordered_tensor = np.squeeze(reconstructed, axis=(0, -1))
    inverse_order = tuple(int(index) for index in np.argsort(ordering))
    approximation = np.transpose(
        ordered_tensor,
        inverse_order,
    ).reshape(modulus)
    return approximation, realized_bonds


def qtt_approximation_row(
    vector: np.ndarray,
    *,
    n_bits: int,
    register_count: int,
    trial: int,
    vector_kind: str,
    ordering_id: str,
    ordering: Sequence[int],
    registered_bond_power: int,
) -> QTTApproximationRow:
    modulus = 1 << n_bits
    bond_cap = max(1, n_bits**registered_bond_power)
    approximation, bonds = qtt_svd_approximation(
        vector.astype(np.float64),
        n_bits=n_bits,
        ordering=ordering,
        bond_cap=bond_cap,
    )
    legal = vector > 0
    legal_count = int(np.sum(legal))
    additive_half_coverage = (
        float(
            np.mean(
                np.abs(approximation[legal] - vector[legal]) < 0.5
            )
        )
        if legal_count
        else 0.0
    )
    constant_count = int(round(float(np.sum(vector)) / modulus))
    constant_coverage = (
        float(np.mean(vector[legal] == constant_count))
        if legal_count
        else 0.0
    )
    vector_norm = float(np.linalg.norm(vector))
    relative_error = (
        float(np.linalg.norm(approximation - vector)) / vector_norm
        if vector_norm > 0.0
        else 0.0
    )
    return QTTApproximationRow(
        n_bits=n_bits,
        register_count=register_count,
        trial=trial,
        vector_kind=vector_kind,
        ordering_id=ordering_id,
        registered_bond_cap=bond_cap,
        maximum_realized_bond=max(bonds, default=1),
        legal_target_count=legal_count,
        legal_target_fraction=legal_count / modulus,
        additive_half_legal_target_coverage=additive_half_coverage,
        zero_frequency_constant_count=constant_count,
        zero_frequency_constant_legal_target_coverage=constant_coverage,
        coverage_excess_over_zero_frequency_constant=(
            additive_half_coverage - constant_coverage
        ),
        relative_frobenius_error=relative_error,
        construction_materializes_full_vector=True,
        witness_decoder_available=False,
    )


def _label_digest(labels: Sequence[int]) -> str:
    accumulator = 0xCBF29CE484222325
    for label in labels:
        accumulator ^= int(label)
        accumulator = (accumulator * 0x100000001B3) & ((1 << 64) - 1)
    return f"{accumulator:016x}"


def _linear_fit(xs: Sequence[int], ys: Sequence[float]) -> tuple[float, float]:
    if len(xs) < 2 or len(set(xs)) < 2:
        return 0.0, float(ys[0]) if ys else 0.0
    slope, intercept = np.polyfit(
        np.asarray(xs, dtype=np.float64),
        np.asarray(ys, dtype=np.float64),
        1,
    )
    return float(slope), float(intercept)


def run_qtt_contraction_search(
    n_values: Sequence[int] = (8, 10, 12, 14, 16, 18),
    register_offset: int = 2,
    trials_per_size: int = 2,
    random_order_count: int = 3,
    registered_bond_power: int = 1,
    seed: int = 0,
) -> DCPSubsetSumQTTReport:
    if not n_values or trials_per_size < 1:
        raise ValueError("nonempty sizes and positive trial count required")
    if register_offset < 0 or registered_bond_power < 0:
        raise ValueError("invalid register offset or bond power")
    rng = random.Random(seed)
    rows: list[QTTUnfoldingRow] = []
    approximation_rows: list[QTTApproximationRow] = []
    instances: list[QTTInstanceSummary] = []
    cut_by_n = {n_bits: n_bits // 2 for n_bits in n_values}
    for n_bits in n_values:
        modulus = 1 << n_bits
        register_count = n_bits + register_offset
        cut = cut_by_n[n_bits]
        for trial in range(trials_per_size):
            labels = [rng.randrange(modulus) for _ in range(register_count)]
            counts = exact_cyclic_subset_sum_counts(labels, modulus)
            surrogate_rng = np.random.default_rng(
                seed + 1000003 * n_bits + trial
            )
            permuted = surrogate_rng.permutation(counts)
            orderings = target_bit_orderings(
                n_bits,
                random_order_count,
                seed + 65537 * n_bits + trial,
            )
            instance_rows: list[QTTUnfoldingRow] = []
            instance_approximation_rows: list[QTTApproximationRow] = []
            for vector_kind, vector in (
                ("source-count-vector", counts),
                ("histogram-permuted-control", permuted),
            ):
                for ordering_id, ordering in orderings:
                    row = unfolding_row(
                        vector,
                        n_bits=n_bits,
                        register_count=register_count,
                        trial=trial,
                        vector_kind=vector_kind,
                        ordering_id=ordering_id,
                        ordering=ordering,
                        cut=cut,
                        registered_bond_power=registered_bond_power,
                    )
                    rows.append(row)
                    instance_rows.append(row)
                    approximation = qtt_approximation_row(
                        vector,
                        n_bits=n_bits,
                        register_count=register_count,
                        trial=trial,
                        vector_kind=vector_kind,
                        ordering_id=ordering_id,
                        ordering=ordering,
                        registered_bond_power=registered_bond_power,
                    )
                    approximation_rows.append(approximation)
                    instance_approximation_rows.append(approximation)
            source_rows = [
                row
                for row in instance_rows
                if row.vector_kind == "source-count-vector"
            ]
            permuted_rows = [
                row
                for row in instance_rows
                if row.vector_kind == "histogram-permuted-control"
            ]
            best_source = min(
                row.additive_half_required_rank for row in source_rows
            )
            best_permuted = min(
                row.additive_half_required_rank for row in permuted_rows
            )
            source_approximations = [
                row
                for row in instance_approximation_rows
                if row.vector_kind == "source-count-vector"
            ]
            permuted_approximations = [
                row
                for row in instance_approximation_rows
                if row.vector_kind == "histogram-permuted-control"
            ]
            best_source_coverage = max(
                row.additive_half_legal_target_coverage
                for row in source_approximations
            )
            best_permuted_coverage = max(
                row.additive_half_legal_target_coverage
                for row in permuted_approximations
            )
            constant_coverage = source_approximations[
                0
            ].zero_frequency_constant_legal_target_coverage
            instances.append(
                QTTInstanceSummary(
                    n_bits=n_bits,
                    register_count=register_count,
                    trial=trial,
                    label_digest=_label_digest(labels),
                    count_mean=float(np.mean(counts)),
                    count_variance=float(np.var(counts)),
                    maximum_count=int(np.max(counts)),
                    ordering_count=len(orderings),
                    best_source_required_rank=best_source,
                    best_permuted_required_rank=best_permuted,
                    source_to_permuted_best_rank_ratio=(
                        best_source / best_permuted
                        if best_permuted
                        else math.inf
                    ),
                    source_registered_cap_survivor_count=sum(
                        not row.registered_cap_additive_half_impossible
                        for row in source_rows
                    ),
                    permuted_registered_cap_survivor_count=sum(
                        not row.registered_cap_additive_half_impossible
                        for row in permuted_rows
                    ),
                    best_source_qtt_legal_coverage=best_source_coverage,
                    best_permuted_qtt_legal_coverage=best_permuted_coverage,
                    zero_frequency_constant_legal_coverage=constant_coverage,
                    source_qtt_coverage_excess_over_zero_frequency_constant=(
                        best_source_coverage - constant_coverage
                    ),
                    source_qtt_coverage_excess_over_permuted=(
                        best_source_coverage - best_permuted_coverage
                    ),
                )
            )

    best_by_instance = {
        (instance.n_bits, instance.trial): instance.best_source_required_rank
        for instance in instances
    }
    fit_x = [
        n_bits
        for (n_bits, _), rank in sorted(best_by_instance.items())
        if rank > 0
    ]
    fit_y = [
        math.log2(rank)
        for (_, _), rank in sorted(best_by_instance.items())
        if rank > 0
    ]
    slope, intercept = _linear_fit(fit_x, fit_y)
    coverage_fit_instances = [
        instance
        for instance in instances
        if instance.source_qtt_coverage_excess_over_zero_frequency_constant
        > 0.0
    ]
    coverage_slope, coverage_intercept = _linear_fit(
        [instance.n_bits for instance in coverage_fit_instances],
        [
            math.log2(
                instance.source_qtt_coverage_excess_over_zero_frequency_constant
            )
            for instance in coverage_fit_instances
        ],
    )
    tail_n = max(n_values)
    tail_instances = [
        instance for instance in instances if instance.n_bits == tail_n
    ]
    source_rows = [
        row for row in rows if row.vector_kind == "source-count-vector"
    ]
    metrics: dict[str, int | float] = {
        "instance_count": len(instances),
        "unfolding_row_count": len(rows),
        "qtt_approximation_row_count": len(approximation_rows),
        "source_unfolding_row_count": len(source_rows),
        "maximum_n_bits": tail_n,
        "registered_bond_power": registered_bond_power,
        "source_full_exact_rank_row_count": sum(
            row.exact_rank == row.maximum_rank for row in source_rows
        ),
        "source_registered_cap_additive_half_impossible_row_count": sum(
            row.registered_cap_additive_half_impossible
            for row in source_rows
        ),
        "source_registered_cap_survivor_row_count": sum(
            not row.registered_cap_additive_half_impossible
            for row in source_rows
        ),
        "tail_source_registered_cap_survivor_count": sum(
            instance.source_registered_cap_survivor_count
            for instance in tail_instances
        ),
        "tail_best_source_required_rank": min(
            instance.best_source_required_rank for instance in tail_instances
        ),
        "tail_best_permuted_required_rank": min(
            instance.best_permuted_required_rank
            for instance in tail_instances
        ),
        "mean_source_to_permuted_best_rank_ratio": float(
            np.mean(
                [
                    instance.source_to_permuted_best_rank_ratio
                    for instance in instances
                ]
            )
        ),
        "fitted_log2_required_rank_slope_per_n": slope,
        "tail_best_source_qtt_legal_coverage": max(
            instance.best_source_qtt_legal_coverage
            for instance in tail_instances
        ),
        "tail_best_permuted_qtt_legal_coverage": max(
            instance.best_permuted_qtt_legal_coverage
            for instance in tail_instances
        ),
        "tail_mean_zero_frequency_constant_legal_coverage": float(
            np.mean(
                [
                    instance.zero_frequency_constant_legal_coverage
                    for instance in tail_instances
                ]
            )
        ),
        "tail_mean_source_qtt_coverage_excess_over_zero_frequency_constant": float(
            np.mean(
                [
                    instance.source_qtt_coverage_excess_over_zero_frequency_constant
                    for instance in tail_instances
                ]
            )
        ),
        "tail_mean_source_qtt_coverage_excess_over_permuted": float(
            np.mean(
                [
                    instance.source_qtt_coverage_excess_over_permuted
                    for instance in tail_instances
                ]
            )
        ),
        "tail_inverse_polynomial_nontrivial_coverage_excess_instance_count": sum(
            instance.source_qtt_coverage_excess_over_zero_frequency_constant
            >= 1.0 / instance.n_bits
            and instance.source_qtt_coverage_excess_over_permuted
            >= 1.0 / instance.n_bits
            for instance in tail_instances
        ),
        "fitted_log2_source_coverage_excess_slope_per_n": coverage_slope,
        "full_vector_materializing_qtt_construction_count": len(
            approximation_rows
        ),
        "proved_asymptotic_qtt_bond_lower_bound_count": 0,
        "proved_uniform_polynomial_qtt_construction_count": 0,
        "proved_polynomial_dense_character_contraction_count": 0,
        "proved_uniform_additive_half_count_oracle_count": 0,
        "polynomial_witness_decoder_count": 0,
    }
    tail_survivors = int(
        metrics["tail_source_registered_cap_survivor_count"]
    )
    return DCPSubsetSumQTTReport(
        created_at=utc_now(),
        access_contract=QTTAccessContract(
            input=(
                "m=n+c independent uniform labels in Z_(2^n); the complete "
                "target count vector is computed exactly only for finite audit"
            ),
            tensorization=(
                "reshape the 2^n target index into n binary axes and search "
                "multiple target-bit orderings"
            ),
            legal_preprocessing=(
                "any ordering derived from public labels is legal, but the "
                "finite audit searches only the recorded family"
            ),
            positive_interface=(
                "a uniform polynomial-bond construction with entrywise count "
                "error below 1/2, stable under variable-fixing self-reduction"
            ),
            hidden_costs_rejected=[
                "materializing the 2^n count vector in a proposed algorithm",
                "bond or intermediate dimension exponential in n",
                "Frobenius error presented as entrywise integer-count accuracy",
                "compression of the original instance without fixed-variable subinstance stability",
                "count approximation without verified Boolean witness extraction",
            ],
        ),
        rows=rows,
        approximation_rows=approximation_rows,
        instances=instances,
        scaling_fits={
            "rank_fit_model": (
                "log2(best additive-half central-cut rank)="
                "rank_slope*n+rank_intercept"
            ),
            "rank_slope": slope,
            "rank_intercept": intercept,
            "rank_fit_point_count": len(fit_x),
            "coverage_fit_model": (
                "log2(best source QTT legal-coverage excess over the "
                "zero-frequency constant)=coverage_slope*n+coverage_intercept"
            ),
            "coverage_slope": coverage_slope,
            "coverage_intercept": coverage_intercept,
            "coverage_fit_point_count": len(coverage_fit_instances),
            "interpretation": (
                "positive rank slope and negative excess slope are finite "
                "architecture evidence, not asymptotic theorems"
            ),
        },
        headline_metrics=metrics,
        claim_gate={
            "finite_registered_bond_cap_survivor_found": (
                int(metrics["source_registered_cap_survivor_row_count"]) > 0
            ),
            "tail_registered_bond_cap_survivor_found": tail_survivors > 0,
            "source_beats_histogram_permuted_control": (
                float(metrics["mean_source_to_permuted_best_rank_ratio"]) < 0.5
            ),
            "raw_partial_legal_target_coverage_found": (
                float(metrics["tail_best_source_qtt_legal_coverage"])
                >= 1.0 / tail_n
            ),
            "inverse_polynomial_nontrivial_coverage_excess_found": (
                int(
                    metrics[
                        "tail_inverse_polynomial_nontrivial_coverage_excess_instance_count"
                    ]
                )
                > 0
            ),
            "qtt_construction_avoids_full_vector": False,
            "asymptotic_qtt_bond_lower_bound_proved": False,
            "uniform_polynomial_qtt_construction_proved": False,
            "polynomial_dense_character_contraction_constructed": False,
            "uniform_additive_half_count_oracle_constructed": False,
            "witness_decoder_constructed": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The registered QTT retains raw partial count accuracy, but its "
                "source-specific excess over the zero-frequency and permuted "
                "baselines falls below 1/n at the tail, and its TT-SVD "
                "construction materializes the full vector. This is finite "
                "negative evidence, not an asymptotic tensor-rank lower bound."
                if tail_survivors == 0
                else "A finite low-bond survivor requires held-out scaling, a "
                "uniform construction, subinstance stability, and witness extraction."
            ),
        },
        status=(
            "finite-qtt-compression-negative-dense-contraction-open"
            if tail_survivors == 0
            else "finite-qtt-survivor-requires-uniform-construction"
        ),
        summary=(
            f"Audited {len(instances)} source instances and {len(rows)} central "
            f"QTT unfoldings through n={tail_n}. Tail registered-cap survivors="
            f"{tail_survivors}; best raw legal coverage="
            f"{metrics['tail_best_source_qtt_legal_coverage']:.6g}; "
            f"mean source excess over zero-frequency baseline="
            f"{metrics['tail_mean_source_qtt_coverage_excess_over_zero_frequency_constant']:.6g}; "
            f"fitted log-rank/excess slopes={slope:.6g}/{coverage_slope:.6g}; "
            "uniform constructions and witness decoders remain zero."
        ),
        falsifiers_triggered=[
            "A low Frobenius reconstruction error is insufficient unless it is below the additive-half integer-count threshold.",
            "The best searched target-bit ordering is charged; one convenient ordering is not treated as canonical.",
            "Histogram-preserving random controls test whether compression comes only from the count histogram.",
            "Raw partial legal-target accuracy is compared with the zero-frequency constant-count baseline before it is treated as structure.",
            "The finite TT-SVD materializes the full count vector and is not a polynomial construction.",
            "Finite exponential-looking rank growth is not promoted to an asymptotic tensor-rank lower bound.",
            "Even a count oracle must remain accurate on fixed-variable subinstances before self-reduction yields a witness.",
        ],
    )


def write_qtt_contraction_search(
    path: Path = DCP_SUBSET_SUM_QTT_PATH,
    *,
    write_registry: bool = True,
    registry_experiment_id: str = DEFAULT_EXPERIMENT_ID,
    registry_candidate_id: str = DEFAULT_CANDIDATE_ID,
    registry_result_id: str | None = None,
    **kwargs: object,
) -> dict[str, object]:
    payload = asdict(run_qtt_contraction_search(**kwargs))
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    return payload


if __name__ == "__main__":
    print(
        json.dumps(
            write_qtt_contraction_search()["headline_metrics"],
            indent=2,
            sort_keys=True,
        )
    )

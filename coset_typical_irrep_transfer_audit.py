"""Bounded-tail no-go and typical-irrep transfer audit for coset recoupling.

Every solved stable recoupling certificate uses partitions (n-|tau|,tau) with
fixed tail size.  Such an irrep has dimension at most n^|tau|: choose the
entries in the fixed number of boxes below the first row, then the first row is
forced.  For a fixed tail budget K, weak Fourier probability of the entire
bounded-tail family is therefore at most

    2 P_K n^(2K) / n!,

where P_K is the constant number of partition tails of size at most K.  This is
superpolynomially small for every fixed K.  A natural-input algorithm must be
label-adaptive on typical high-dimensional partitions; selecting any fixed
stable family cannot work.

The finite audit then chooses a maximum-dimension (high Plancherel mass) source
partition and computes its exact self-Kronecker profile using character inner
products.  It measures support proliferation, multiplicity growth, coupling
entropy, and the coupling mass retained by bounded-tail targets.  These rows do
not prove asymptotic hardness, but they define the missing transfer problem and
prevent stable-sector circuits from being promoted without a typical-label
uniformity theorem.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from fractions import Fraction
from functools import lru_cache
from pathlib import Path
from typing import Sequence

from representation_obstruction import hook_length_dimension, integer_partitions
from research_registry import (
    ExperimentResultRecord,
    NegativeResultRecord,
    upsert_experiment_result,
    upsert_negative_result,
    utc_now,
)
from symmetric_character import kronecker_coefficient
from weak_fourier_signal import character_on_involution


COSET_TYPICAL_IRREP_TRANSFER_PATH = Path(
    "research/representation/coset_typical_irrep_transfer_audit.json"
)
DEFAULT_EXPERIMENT_ID = "EXP-COSET-TYPICAL-IRREP-TRANSFER-AUDIT"
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


@dataclass(frozen=True)
class TypicalIrrepTransferRecord:
    n: int
    partition_count: int
    source_partition: tuple[int, ...]
    source_dimension: int
    source_tail_size: int
    source_plancherel_mass: float
    partial_matching_character_ratio: float
    partial_matching_weak_probability: float
    dense_matching_character_ratio: float
    dense_matching_weak_probability: float
    kronecker_target_support_count: int
    kronecker_target_support_fraction: float
    maximum_kronecker_multiplicity: int
    log2_maximum_kronecker_multiplicity: float
    sum_kronecker_multiplicities: int
    exact_weighted_dimension_identity_verified: bool
    bounded_tail_limit: int
    bounded_tail_supported_target_count: int
    exact_bounded_tail_coupling_mass: str
    bounded_tail_coupling_mass: float
    coupling_target_entropy_bits: float
    targets_for_ninety_percent_coupling_mass: int
    top_coupling_target: tuple[int, ...]
    top_coupling_target_mass: float
    finite_character_profile_only: bool
    status: str


@dataclass(frozen=True)
class TypicalIrrepTransferReport:
    created_at: str
    bounded_tail_no_go: dict[str, object]
    required_typical_label_interface: dict[str, object]
    records: list[TypicalIrrepTransferRecord]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, bool | str]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def bounded_tail_count(maximum_tail_size: int) -> int:
    if maximum_tail_size < 0:
        raise ValueError("tail size must be nonnegative")
    return sum(len(integer_partitions(size)) for size in range(maximum_tail_size + 1))


def bounded_tail_weak_probability_upper_bound(n: int, maximum_tail_size: int) -> Fraction:
    return Fraction(
        2 * bounded_tail_count(maximum_tail_size) * n ** (2 * maximum_tail_size),
        math.factorial(n),
    )


def _maximum_dimension_partition(n: int) -> tuple[int, ...]:
    return max(
        integer_partitions(n),
        key=lambda partition: (hook_length_dimension(partition), partition),
    )


def _weak_probability(
    partition: tuple[int, ...], transposition_count: int
) -> tuple[float, float]:
    n = sum(partition)
    dimension = hook_length_dimension(partition)
    character = character_on_involution(partition, transposition_count)
    ratio = character / dimension
    plancherel = dimension * dimension / math.factorial(n)
    return ratio, plancherel * (1 + ratio)


@lru_cache(maxsize=None)
def audit_typical_irrep_transfer(
    n: int,
    bounded_tail_limit: int = 4,
) -> TypicalIrrepTransferRecord:
    if n < 2 * bounded_tail_limit:
        raise ValueError("n must be at least twice the bounded tail limit")
    partitions = integer_partitions(n)
    source = _maximum_dimension_partition(n)
    source_dimension = hook_length_dimension(source)
    plancherel = Fraction(source_dimension**2, math.factorial(n))
    partial_ratio, partial_probability = _weak_probability(source, n // 4)
    dense_ratio, dense_probability = _weak_probability(source, n // 2)
    rows: list[tuple[tuple[int, ...], int, int, Fraction]] = []
    weighted_dimension_sum = 0
    for target in partitions:
        multiplicity = kronecker_coefficient(source, source, target)
        if not multiplicity:
            continue
        target_dimension = hook_length_dimension(target)
        weighted_dimension_sum += multiplicity * target_dimension
        mass = Fraction(
            multiplicity * target_dimension,
            source_dimension**2,
        )
        rows.append((target, multiplicity, target_dimension, mass))
    if weighted_dimension_sum != source_dimension**2:
        raise ArithmeticError("Kronecker weighted-dimension identity failed")
    bounded = [row for row in rows if n - row[0][0] <= bounded_tail_limit]
    bounded_mass = sum((row[3] for row in bounded), Fraction())
    entropy = -sum(
        float(row[3]) * math.log2(float(row[3])) for row in rows if row[3]
    )
    ordered = sorted(rows, key=lambda row: (-row[3], row[0]))
    accumulated = Fraction()
    ninety_count = 0
    for row in ordered:
        accumulated += row[3]
        ninety_count += 1
        if accumulated >= Fraction(9, 10):
            break
    top = ordered[0]
    maximum_multiplicity = max(row[1] for row in rows)
    return TypicalIrrepTransferRecord(
        n=n,
        partition_count=len(partitions),
        source_partition=source,
        source_dimension=source_dimension,
        source_tail_size=n - source[0],
        source_plancherel_mass=float(plancherel),
        partial_matching_character_ratio=partial_ratio,
        partial_matching_weak_probability=partial_probability,
        dense_matching_character_ratio=dense_ratio,
        dense_matching_weak_probability=dense_probability,
        kronecker_target_support_count=len(rows),
        kronecker_target_support_fraction=len(rows) / len(partitions),
        maximum_kronecker_multiplicity=maximum_multiplicity,
        log2_maximum_kronecker_multiplicity=math.log2(maximum_multiplicity),
        sum_kronecker_multiplicities=sum(row[1] for row in rows),
        exact_weighted_dimension_identity_verified=True,
        bounded_tail_limit=bounded_tail_limit,
        bounded_tail_supported_target_count=len(bounded),
        exact_bounded_tail_coupling_mass=str(bounded_mass),
        bounded_tail_coupling_mass=float(bounded_mass),
        coupling_target_entropy_bits=entropy,
        targets_for_ninety_percent_coupling_mass=ninety_count,
        top_coupling_target=top[0],
        top_coupling_target_mass=float(top[3]),
        finite_character_profile_only=True,
        status="typical-source-broad-growing-multiplicity-transfer-theorem-open",
    )


@lru_cache(maxsize=1)
def build_typical_irrep_transfer_report(
    n_values: tuple[int, ...] = (8, 10, 12, 14, 16, 18, 20),
    bounded_tail_limit: int = 4,
) -> TypicalIrrepTransferReport:
    records = [
        audit_typical_irrep_transfer(n, bounded_tail_limit=bounded_tail_limit)
        for n in n_values
    ]
    metrics: dict[str, int | float] = {
        "typical_transfer_record_count": len(records),
        "bounded_tail_natural_access_no_go_theorem_count": 1,
        "exact_kronecker_weighted_dimension_identity_count": sum(
            record.exact_weighted_dimension_identity_verified for record in records
        ),
        "maximum_partition_count": max(record.partition_count for record in records),
        "maximum_kronecker_target_support_fraction": max(
            record.kronecker_target_support_fraction for record in records
        ),
        "maximum_kronecker_multiplicity": max(
            record.maximum_kronecker_multiplicity for record in records
        ),
        "minimum_bounded_tail_coupling_mass": min(
            record.bounded_tail_coupling_mass for record in records
        ),
        "maximum_targets_for_ninety_percent_coupling_mass": max(
            record.targets_for_ninety_percent_coupling_mass for record in records
        ),
        "uniform_typical_label_commutant_gap_theorem_count": 0,
        "uniform_typical_label_encoded_tree_transform_count": 0,
        "typical_label_frame_conditioning_theorem_count": 0,
        "typical_label_hidden_involution_decoder_count": 0,
    }
    return TypicalIrrepTransferReport(
        created_at=utc_now(),
        bounded_tail_no_go={
            "theorem": (
                "For fixed K, every lambda=(n-|tau|,tau) with |tau|<=K has d_lambda<=n^K, so the union weak-Fourier "
                "probability is at most 2*P_K*n^(2K)/n!, where P_K=sum_(j<=K) p(j)."
            ),
            "dimension_proof": (
                "Choose the at most K tableau entries below the first row in at most n^K ways; the first row is then forced."
            ),
            "character_ratio_step": "P_H(lambda)<=2*d_lambda^2/n! because abs(chi_lambda(h)/d_lambda)<=1",
            "asymptotic_consequence": "The probability is smaller than every inverse polynomial for each fixed K.",
            "algorithmic_consequence": (
                "No predetermined bounded-tail stable family is naturally accessible. A viable Fourier algorithm must "
                "accept sampled high-dimensional labels and adapt all later representation primitives to them."
            ),
        },
        required_typical_label_interface={
            "input": "arbitrary weak-Fourier labels lambda_1,...,lambda_k sampled from the natural coset state",
            "forbidden_step": "postselect any predetermined bounded-tail label family",
            "required_uniformity": (
                "gate complexity and inverse gaps polynomial uniformly in n and the bit descriptions of sampled partitions"
            ),
            "required_operations": [
                "label-adaptive bounded-support commutant block encoding",
                "multiplicity resolution for growing Kronecker coefficients",
                "overlapping coupling-tree transitions for broad target support",
                "frame conditioning on naturally weighted sectors",
                "compressed outcome decoder and classical comparison",
            ],
            "current_proved_operation_count": 0,
        },
        records=records,
        headline_metrics=metrics,
        claim_gate={
            "bounded_tail_stable_route_naturally_accessible": False,
            "typical_label_adaptation_required": True,
            "finite_typical_profiles_are_complexity_theorems": False,
            "uniform_typical_label_multiplicity_transform_proved": False,
            "uniform_typical_label_frame_filter_proved": False,
            "typical_label_hidden_involution_decoder_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "Bounded-tail families have factorially small natural mass. Typical sources show broad target support "
                "and growing multiplicities, but no uniform commutant gap, recoupling, frame, or decoder theorem exists."
            ),
        },
        status="bounded-tail-route-falsified-typical-label-transfer-frontier-open",
        summary=(
            f"Proved the fixed-bounded-tail natural-access no-go and audited {len(records)} exact high-Plancherel "
            f"self-Kronecker profiles. At n={max(n_values)}, bounded-tail target coupling mass is "
            f"{records[-1].bounded_tail_coupling_mass:.3e}; a label-adaptive typical-sector architecture is now mandatory."
        ),
        falsifiers_triggered=[
            "Every predetermined fixed-tail Fourier family has superpolynomially small natural probability.",
            "Stable character-polynomial tractability is anti-correlated with natural Plancherel accessibility.",
            "Finite typical self-Kronecker profiles spread over nearly all target partitions and growing multiplicities.",
            "A circuit proved only for fixed stable tails cannot be counted as progress toward a natural-input coset algorithm.",
            "Finite multiplicity growth is search guidance, not a quantum hardness or speedup theorem.",
        ],
    )


def write_typical_irrep_transfer_report(
    output_path: Path = COSET_TYPICAL_IRREP_TRANSFER_PATH,
    n_values: tuple[int, ...] = (8, 10, 12, 14, 16, 18, 20),
    bounded_tail_limit: int = 4,
    write_registry: bool = True,
    registry_experiment_id: str = DEFAULT_EXPERIMENT_ID,
    registry_candidate_id: str = DEFAULT_CANDIDATE_ID,
    registry_result_id: str | None = None,
) -> dict:
    payload = asdict(
        build_typical_irrep_transfer_report(
            n_values=n_values,
            bounded_tail_limit=bounded_tail_limit,
        )
    )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    if write_registry:
        upsert_negative_result(
            NegativeResultRecord(
                id="NEG-COSET-FIXED-BOUNDED-TAIL-FOURIER-ROUTE",
                source=str(output_path),
                claim=(
                    "A polynomial recoupling algorithm restricted to a predetermined bounded-tail partition family can process natural coset states efficiently."
                ),
                reason_invalid=(
                    "For every fixed tail budget K, the entire family's weak-Fourier probability is at most "
                    "2*P_K*n^(2K)/n!, smaller than every inverse polynomial."
                ),
                lesson=(
                    "Require uniform label-adaptive primitives on sampled typical partitions. Stable families may be "
                    "used only to discover algebraic mechanisms that are subsequently transferred and reproved."
                ),
                applies_to=[registry_candidate_id, registry_experiment_id],
                evidence=payload["headline_metrics"],
            )
        )
        result_id = registry_result_id or f"RESULT-{registry_experiment_id}-LATEST"
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
                artifacts={"coset_typical_irrep_transfer_audit": str(output_path)},
            )
        )
    return payload


if __name__ == "__main__":
    report = write_typical_irrep_transfer_report()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))

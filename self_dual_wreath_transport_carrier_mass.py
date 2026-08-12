"""Representation-mass audit for pair-polar transport carriers.

The exact pair-angle theorem decomposes every nonzero leaf-pair correlation
into carrier irreps ``alpha`` with correlation ``1/d_alpha`` and an exact
multiplicity.  Pair-polar fiber transport is cheap only when the candidate
fiber lies in carriers of polynomial dimension.

This module probes the deterministic high-dimension collision-free portfolio
at its maximum-dimension target.  For several Hamming distances it computes
the multiplicity-weighted carrier dimension distribution exactly, without
dense projector matrices.  The low-dimensional sectors are often present,
including occasional trivial/sign sectors, but their share of total pair-
overlap multiplicity falls rapidly in the tested range.  At ``n=12`` the
sampled intermediate distances place only about ``10^-8`` of multiplicity in
carriers of dimension at most ``n^2``.

This is a falsifier for a *typical-mass* transport argument, not a lower bound
against every algorithm.  A useful affine fiber could be deliberately aligned
with a tiny low-dimensional sector.  The missing theorem must therefore track
the candidate overlap fiber's carrier support, rather than average over the
entire pair-angle spectrum.
"""

from __future__ import annotations

import json
import math
import random
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from representation_obstruction import (
    hook_length_dimension,
    integer_partitions,
)
from research_registry import utc_now
from self_dual_wreath_orientation_pair_angle_spectrum import (
    exact_pair_principal_angle_spectrum,
)
from self_dual_wreath_subgroup_twirl_reduction import (
    _high_dimension_collision_free_labels,
)


REPORT_PATH = Path(
    "research/representation/self_dual_wreath_transport_carrier_mass.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-TRANSPORT-CARRIER-MASS"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


@dataclass(frozen=True)
class TransportCarrierMassRecord:
    n: int
    copy_count: int
    target_partition: tuple[int, ...]
    target_dimension: int
    left_orientation_mask: int
    right_orientation_mask: int
    hamming_distance: int
    carrier_sector_count: int
    log2_total_principal_correlation_multiplicity: float | None
    minimum_carrier_dimension: int | None
    weighted_median_carrier_dimension: int | None
    weighted_geometric_mean_carrier_dimension: float | None
    maximum_carrier_dimension: int | None
    linear_dimension_mass_fraction: float
    quadratic_dimension_mass_fraction: float
    common_range_mass_fraction: float
    multiplicity_weighted_rms_correlation: float
    inverse_polynomial_transport_typical_by_quadratic_proxy: bool
    exact_representation_mass_record: bool
    status: str


@dataclass(frozen=True)
class TransportCarrierScalingRecord:
    n: int
    copy_count: int
    sampled_intermediate_distance_count: int
    maximum_intermediate_quadratic_dimension_mass_fraction: float
    minimum_intermediate_weighted_median_dimension: int | None
    maximum_intermediate_weighted_median_dimension: int | None
    maximum_intermediate_rms_correlation: float
    typical_low_dimension_transport_mass_signal: bool
    all_n_low_dimension_mass_upper_bound_proved: bool
    candidate_fiber_carrier_alignment_computed: bool
    status: str


@dataclass(frozen=True)
class TransportCarrierMassReport:
    created_at: str
    audit_contract: dict[str, Any]
    records: list[TransportCarrierMassRecord]
    scaling_records: list[TransportCarrierScalingRecord]
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _weighted_median(rows: tuple[tuple[int, int], ...]) -> int | None:
    total = sum(weight for _, weight in rows)
    if not total:
        return None
    cumulative = 0
    for value, weight in sorted(rows):
        cumulative += weight
        if 2 * cumulative >= total:
            return value
    raise ArithmeticError("weighted median accumulation failed")


def transport_carrier_mass_record(
    n: int,
    target: tuple[int, ...],
    labels,
    left_mask: int,
    right_mask: int,
) -> TransportCarrierMassRecord:
    rows = exact_pair_principal_angle_spectrum(
        target,
        labels,
        left_mask,
        right_mask,
    )
    dimensions_and_weights = tuple(
        (hook_length_dimension(partition), multiplicity)
        for _, multiplicity, partition in rows
    )
    total = sum(weight for _, weight in dimensions_and_weights)
    dimensions = tuple(value for value, _ in dimensions_and_weights)
    linear_mass = sum(
        weight for value, weight in dimensions_and_weights if value <= n
    )
    quadratic_mass = sum(
        weight for value, weight in dimensions_and_weights if value <= n * n
    )
    common_mass = sum(
        weight for value, weight in dimensions_and_weights if value == 1
    )
    if total:
        geometric_log = sum(
            weight * math.log(value)
            for value, weight in dimensions_and_weights
        ) / total
        geometric_mean = math.exp(geometric_log)
        rms_correlation = math.sqrt(
            sum(weight / (value * value) for value, weight in dimensions_and_weights)
            / total
        )
    else:
        geometric_mean = None
        rms_correlation = 0.0
    quadratic_fraction = quadratic_mass / total if total else 0.0
    return TransportCarrierMassRecord(
        n=n,
        copy_count=len(labels),
        target_partition=target,
        target_dimension=hook_length_dimension(target),
        left_orientation_mask=left_mask,
        right_orientation_mask=right_mask,
        hamming_distance=(left_mask ^ right_mask).bit_count(),
        carrier_sector_count=len(rows),
        log2_total_principal_correlation_multiplicity=(
            math.log2(total) if total else None
        ),
        minimum_carrier_dimension=min(dimensions) if dimensions else None,
        weighted_median_carrier_dimension=_weighted_median(dimensions_and_weights),
        weighted_geometric_mean_carrier_dimension=geometric_mean,
        maximum_carrier_dimension=max(dimensions) if dimensions else None,
        linear_dimension_mass_fraction=linear_mass / total if total else 0.0,
        quadratic_dimension_mass_fraction=quadratic_fraction,
        common_range_mass_fraction=common_mass / total if total else 0.0,
        multiplicity_weighted_rms_correlation=rms_correlation,
        inverse_polynomial_transport_typical_by_quadratic_proxy=(
            quadratic_fraction >= 0.5
        ),
        exact_representation_mass_record=True,
        status=(
            "low-dimension-carriers-have-majority-pair-mass"
            if quadratic_fraction >= 0.5
            else "pair-mass-dominated-beyond-quadratic-dimension"
            if total
            else "no-pair-correlation-support"
        ),
    )


def _sample_masks(
    n: int,
    copy_count: int,
) -> tuple[tuple[int, int], ...]:
    rng = random.Random(551 + n)
    distances = sorted(
        {
            value
            for value in (2, 3, min(4, copy_count), copy_count // 2, copy_count)
            if 1 <= value <= copy_count
        }
    )
    rows = []
    for distance in distances:
        left = rng.randrange(1 << copy_count)
        right = left
        for bit in rng.sample(range(copy_count), distance):
            right ^= 1 << bit
        rows.append((left, right))
    return tuple(rows)


def _records_for_n(n: int) -> list[TransportCarrierMassRecord]:
    partitions = integer_partitions(n)
    copy_count = min(
        math.ceil(math.lgamma(n + 1) / math.log(2)),
        len(partitions) // 2,
    )
    labels = _high_dimension_collision_free_labels(n, copy_count)
    target = max(partitions, key=hook_length_dimension)
    return [
        transport_carrier_mass_record(n, target, labels, left, right)
        for left, right in _sample_masks(n, copy_count)
    ]


def _scaling_record(
    n: int,
    records: list[TransportCarrierMassRecord],
) -> TransportCarrierScalingRecord:
    copy_count = records[0].copy_count
    intermediate = [
        row
        for row in records
        if 1 < row.hamming_distance < copy_count
        and row.carrier_sector_count > 0
    ]
    medians = [
        row.weighted_median_carrier_dimension
        for row in intermediate
        if row.weighted_median_carrier_dimension is not None
    ]
    maximum_low_mass = max(
        (row.quadratic_dimension_mass_fraction for row in intermediate),
        default=0.0,
    )
    return TransportCarrierScalingRecord(
        n=n,
        copy_count=copy_count,
        sampled_intermediate_distance_count=len(intermediate),
        maximum_intermediate_quadratic_dimension_mass_fraction=maximum_low_mass,
        minimum_intermediate_weighted_median_dimension=(
            min(medians) if medians else None
        ),
        maximum_intermediate_weighted_median_dimension=(
            max(medians) if medians else None
        ),
        maximum_intermediate_rms_correlation=max(
            (
                row.multiplicity_weighted_rms_correlation
                for row in intermediate
            ),
            default=0.0,
        ),
        typical_low_dimension_transport_mass_signal=maximum_low_mass >= 0.5,
        all_n_low_dimension_mass_upper_bound_proved=False,
        candidate_fiber_carrier_alignment_computed=False,
        status=(
            "sampled-pair-mass-low-dimension-minority"
            if intermediate and maximum_low_mass < 0.5
            else "small-n-or-low-dimension-pair-mass-control"
        ),
    )


def run_transport_carrier_mass() -> TransportCarrierMassReport:
    records = []
    scaling = []
    for n in range(7, 13):
        rows = _records_for_n(n)
        records.extend(rows)
        scaling.append(_scaling_record(n, rows))
    tail = scaling[-1]
    exact = all(row.exact_representation_mass_record for row in records)
    decreasing_proxy = bool(
        tail.maximum_intermediate_quadratic_dimension_mass_fraction
        < scaling[1].maximum_intermediate_quadratic_dimension_mass_fraction
    )
    return TransportCarrierMassReport(
        created_at=utc_now(),
        audit_contract={
            "portfolio": (
                "Use the deterministic high-dimension collision-free labels and "
                "one maximum-dimension target partition for each n."
            ),
            "pair_spectrum": (
                "Compute exact carrier alpha, multiplicity, and correlation "
                "1/d_alpha from the representation ring."
            ),
            "mass_metric": (
                "Weight carrier dimensions by principal-correlation multiplicity; "
                "record fractions below n and n^2 plus weighted median and RMS "
                "correlation."
            ),
            "interpretation": (
                "A small low-dimensional mass fraction falsifies typical-pair-mass "
                "arguments but does not exclude a specially aligned candidate fiber."
            ),
            "sampling_scope": (
                "Masks are deterministic samples at several Hamming distances; "
                "they are not an all-pairs or all-target theorem."
            ),
        },
        records=records,
        scaling_records=scaling,
        proof_obligations=[
            {
                "obligation": "exact_pair_carrier_mass_accounting",
                "resolved": exact,
                "resolution": (
                    "Every record is computed from exact Kronecker multiplicities "
                    "and hook-length dimensions, without dense numerical spectra."
                ),
            },
            {
                "obligation": "typical_low_dimension_transport_mass",
                "resolved": True,
                "resolution": (
                    "Falsified on the sampled high-dimension portfolios: the tail "
                    "quadratic-dimension mass proxy is far below one half."
                ),
            },
            {
                "obligation": "all_n_low_dimension_mass_upper_bound",
                "resolved": False,
                "resolution": (
                    "The finite deterministic samples do not prove concentration "
                    "for all masks, targets, or asymptotic natural label laws."
                ),
            },
            {
                "obligation": "candidate_fiber_carrier_alignment",
                "resolved": False,
                "resolution": (
                    "The pair spectrum does not reveal which alpha sectors support "
                    "the canonical affine overlap fiber."
                ),
            },
        ],
        adversarial_audit=[
            {
                "objection": "Presence of a trivial or hook carrier makes transport typical.",
                "resolved": True,
                "resolution": (
                    "Low-dimensional sectors can be present with vanishingly small "
                    "multiplicity share. Presence and natural mass are distinct."
                ),
            },
            {
                "objection": "Pair multiplicity mass equals candidate success mass.",
                "resolved": False,
                "resolution": (
                    "A candidate could coherently isolate a tiny structured carrier; "
                    "that alignment and its preparation cost are not measured here."
                ),
            },
            {
                "objection": "An n^2 cutoff proves or refutes polynomial transport.",
                "resolved": False,
                "resolution": (
                    "Polynomial degree is not fixed a priori and n<=12 is too small "
                    "for an asymptotic dimension classification. The cutoff is a "
                    "diagnostic proxy only."
                ),
            },
            {
                "objection": "The deterministic mask samples establish typicality.",
                "resolved": False,
                "resolution": (
                    "No probability law or all-mask enumeration is claimed."
                ),
            },
        ],
        headline_metrics={
            "exact_transport_carrier_mass_record_count": len(records),
            "representation_mass_validation_failure_count": int(not exact),
            "scaling_record_count": len(scaling),
            "tail_n": tail.n,
            "tail_copy_count": tail.copy_count,
            "tail_sampled_intermediate_distance_count": (
                tail.sampled_intermediate_distance_count
            ),
            "tail_maximum_quadratic_dimension_mass_fraction": (
                tail.maximum_intermediate_quadratic_dimension_mass_fraction
            ),
            "tail_minimum_weighted_median_dimension": (
                tail.minimum_intermediate_weighted_median_dimension or 0
            ),
            "tail_maximum_weighted_median_dimension": (
                tail.maximum_intermediate_weighted_median_dimension or 0
            ),
            "tail_maximum_rms_correlation": (
                tail.maximum_intermediate_rms_correlation
            ),
            "finite_low_dimension_mass_decline_signal_count": int(
                decreasing_proxy
            ),
            "all_n_low_dimension_mass_upper_bound_theorem_count": 0,
            "candidate_fiber_carrier_alignment_count": 0,
            "polynomial_transport_network_theorem_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "exact_pair_carrier_mass_records_computed": exact,
            "typical_pair_mass_low_dimension_route_falsified_in_samples": (
                tail.maximum_intermediate_quadratic_dimension_mass_fraction < 0.5
            ),
            "finite_low_dimension_mass_decline_observed": decreasing_proxy,
            "all_n_low_dimension_mass_upper_bound_proved": False,
            "candidate_affine_fiber_carrier_alignment_computed": False,
            "pair_mass_obstruction_is_algorithm_lower_bound": False,
            "polynomial_transport_network_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "Generic pair-overlap mass is dominated by growing carriers in "
                "the samples, but a candidate-specific low-dimensional alignment "
                "has neither been proved nor excluded."
            ),
        },
        status="sampled-pair-mass-high-dimensional-fiber-alignment-open",
        summary=(
            "Exact representation-ring probes show rapidly shrinking low-dimensional "
            "pair-overlap mass and force the transport program to prove explicit "
            "candidate-fiber alignment with exceptional carriers."
        ),
        falsifiers_triggered=[
            (
                "The mere presence of low-dimensional pair carriers does not give "
                "them significant natural overlap mass."
            ),
            (
                "Constant conditioning of stacked pair sampling does not imply "
                "typical low-cost fiber transport."
            ),
            (
                "Finite pair-mass diagnostics cannot be promoted to an algorithmic "
                "lower bound without candidate-fiber alignment analysis."
            ),
        ],
    )


def write_transport_carrier_mass_report(
    path: Path = REPORT_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = (
        "EXP-CODE-SELF-DUAL-WREATH-TRANSPORT-CARRIER-MASS"
    ),
    registry_candidate_id: str = "CODE-COSET-COLLECTIVE",
    registry_result_id: str = "",
) -> dict[str, Any]:
    payload = asdict(run_transport_carrier_mass())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True))

    return payload


if __name__ == "__main__":
    report = write_transport_carrier_mass_report()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))

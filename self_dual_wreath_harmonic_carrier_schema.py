"""Harmonic block schema for depth-three wreath carrier labels.

After fixing the first bridge label, a depth-three carrier word is indexed by
two permutations under simultaneous conjugation.  Let

    K_n = C[S_n]

with the conjugation action.  Peter--Weyl and Kronecker decomposition give

    K_n = direct_sum_nu V_nu tensor C^{m_nu},
    m_nu = sum_lambda g(lambda, lambda, nu).

Because every S_n irrep is self-dual, the invariant subspace of
K_n tensor K_n has dimension

    sum_nu m_nu^2.

This equals the Burnside count sum_alpha z_alpha for simultaneous-conjugacy
orbits of permutation pairs.  The identity gives a compressed mathematical
schema: a carrier coordinate is addressed by a partition nu and two
multiplicity indices.

It does not give an efficient transform.  There are p(n) possible outer
labels, and some multiplicity block has at least n!/p(n) matrix coordinates.
Even granting an efficient S_n group QFT, an internal Kronecker basis,
carrier-product recoupling rules, and a conditioned coherent block transform
remain missing.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

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
from self_dual_wreath_carrier_orbit_growth import (
    simultaneous_conjugacy_orbit_count,
)
from self_dual_wreath_hecke_audit import partition_number
from symmetric_character import kronecker_coefficient


SELF_DUAL_WREATH_HARMONIC_CARRIER_SCHEMA_PATH = Path(
    "research/representation/self_dual_wreath_harmonic_carrier_schema.json"
)
DEFAULT_EXPERIMENT_ID = "EXP-CODE-SELF-DUAL-WREATH-HARMONIC-CARRIER-SCHEMA"
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


@dataclass(frozen=True)
class WreathHarmonicCarrierSpec:
    exact_n_values: tuple[int, ...] = tuple(range(2, 13))
    tail_n_values: tuple[int, ...] = (16, 20, 24, 32, 48, 64)


@dataclass(frozen=True)
class HarmonicMultiplicityBlockRecord:
    n: int
    target_partition: tuple[int, ...]
    target_irrep_dimension: int
    conjugation_multiplicity: int
    contributing_source_partition_count: int
    source_kronecker_contributions: list[dict[str, Any]]
    invariant_matrix_coordinate_count: int
    multiplicity_index_bits: int
    multiplicity_free: bool


@dataclass(frozen=True)
class HarmonicCarrierScalingRecord:
    n: int
    exact: bool
    partition_count: int
    active_harmonic_block_count: int | None
    exact_pair_orbit_count_decimal: str | None
    exact_harmonic_invariant_dimension_decimal: str | None
    harmonic_burnside_identity_verified: bool | None
    maximum_exact_multiplicity: int | None
    maximum_exact_multiplicity_target: tuple[int, ...] | None
    maximum_exact_block_coordinate_count_decimal: str | None
    factorial_average_block_coordinate_lower_bound_decimal: str
    certified_maximum_block_coordinate_lower_bound_decimal: str
    log2_certified_maximum_block_coordinate_lower_bound: float
    certified_maximum_multiplicity_lower_bound_decimal: str
    log2_certified_maximum_multiplicity_lower_bound: float
    outer_partition_label_bits: int
    maximum_exact_coordinate_address_bits: int | None
    compact_coordinate_address: bool
    polynomial_outer_block_count: bool
    polynomial_dense_block_dimension_proved: bool
    internal_kronecker_basis_transform_proved: bool
    sparse_carrier_product_rules_proved: bool
    status: str


@dataclass(frozen=True)
class SelfDualWreathHarmonicCarrierReport:
    created_at: str
    spec: WreathHarmonicCarrierSpec
    representation_reduction: dict[str, Any]
    block_records: list[HarmonicMultiplicityBlockRecord]
    scaling_records: list[HarmonicCarrierScalingRecord]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, bool | str]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _ceil_log2(value: int) -> int:
    if value < 1:
        return 0
    return (value - 1).bit_length()


def _ceil_sqrt(value: int) -> int:
    root = math.isqrt(value)
    return root if root * root == value else root + 1


def _ceil_ratio(numerator: int, denominator: int) -> int:
    return (numerator + denominator - 1) // denominator


def conjugation_multiplicity(
    target: tuple[int, ...],
    partitions: tuple[tuple[int, ...], ...] | None = None,
) -> int:
    """Multiplicity of V_target in C[S_n] under conjugation."""

    n = sum(target)
    sources = partitions or integer_partitions(n)
    return sum(
        kronecker_coefficient(source, source, target)
        for source in sources
    )


def harmonic_multiplicity_blocks(
    n: int,
) -> list[HarmonicMultiplicityBlockRecord]:
    if n < 2:
        raise ValueError("n must be at least two")
    partitions = integer_partitions(n)
    records: list[HarmonicMultiplicityBlockRecord] = []
    for target in partitions:
        contributions = []
        for source in partitions:
            multiplicity = kronecker_coefficient(source, source, target)
            if multiplicity:
                contributions.append(
                    {
                        "source_partition": source,
                        "kronecker_multiplicity": multiplicity,
                    }
                )
        total = sum(
            int(item["kronecker_multiplicity"])
            for item in contributions
        )
        records.append(
            HarmonicMultiplicityBlockRecord(
                n=n,
                target_partition=target,
                target_irrep_dimension=hook_length_dimension(target),
                conjugation_multiplicity=total,
                contributing_source_partition_count=len(contributions),
                source_kronecker_contributions=contributions,
                invariant_matrix_coordinate_count=total * total,
                multiplicity_index_bits=_ceil_log2(total),
                multiplicity_free=total <= 1,
            )
        )
    return records


def audit_harmonic_carrier_scaling(
    n: int,
    exact: bool = True,
) -> tuple[HarmonicCarrierScalingRecord, list[HarmonicMultiplicityBlockRecord]]:
    if n < 2:
        raise ValueError("n must be at least two")
    partition_count = partition_number(n)
    factorial = math.factorial(n)
    factorial_average_coordinates = _ceil_ratio(factorial, partition_count)
    blocks = harmonic_multiplicity_blocks(n) if exact else []

    if blocks:
        active = [block for block in blocks if block.conjugation_multiplicity]
        harmonic_dimension = sum(
            block.invariant_matrix_coordinate_count for block in blocks
        )
        pair_orbits = simultaneous_conjugacy_orbit_count(n, 2)
        maximum = max(
            blocks,
            key=lambda block: (
                block.conjugation_multiplicity,
                block.target_partition,
            ),
        )
        exact_average_coordinates = _ceil_ratio(
            pair_orbits,
            len(active),
        )
        certified_coordinates = max(
            factorial_average_coordinates,
            exact_average_coordinates,
        )
        exact_identity: bool | None = harmonic_dimension == pair_orbits
        maximum_multiplicity: int | None = maximum.conjugation_multiplicity
        maximum_target: tuple[int, ...] | None = maximum.target_partition
        maximum_coordinates: str | None = str(
            maximum.invariant_matrix_coordinate_count
        )
        address_bits: int | None = (
            _ceil_log2(partition_count)
            + 2 * _ceil_log2(maximum.conjugation_multiplicity)
        )
        active_count: int | None = len(active)
        exact_pair_orbits: str | None = str(pair_orbits)
        exact_harmonic_dimension: str | None = str(harmonic_dimension)
    else:
        certified_coordinates = factorial_average_coordinates
        exact_identity = None
        maximum_multiplicity = None
        maximum_target = None
        maximum_coordinates = None
        address_bits = None
        active_count = None
        exact_pair_orbits = None
        exact_harmonic_dimension = None

    multiplicity_lower = _ceil_sqrt(certified_coordinates)
    return (
        HarmonicCarrierScalingRecord(
            n=n,
            exact=exact,
            partition_count=partition_count,
            active_harmonic_block_count=active_count,
            exact_pair_orbit_count_decimal=exact_pair_orbits,
            exact_harmonic_invariant_dimension_decimal=(
                exact_harmonic_dimension
            ),
            harmonic_burnside_identity_verified=exact_identity,
            maximum_exact_multiplicity=maximum_multiplicity,
            maximum_exact_multiplicity_target=maximum_target,
            maximum_exact_block_coordinate_count_decimal=(
                maximum_coordinates
            ),
            factorial_average_block_coordinate_lower_bound_decimal=str(
                factorial_average_coordinates
            ),
            certified_maximum_block_coordinate_lower_bound_decimal=str(
                certified_coordinates
            ),
            log2_certified_maximum_block_coordinate_lower_bound=round(
                math.log2(certified_coordinates),
                12,
            ),
            certified_maximum_multiplicity_lower_bound_decimal=str(
                multiplicity_lower
            ),
            log2_certified_maximum_multiplicity_lower_bound=round(
                math.log2(multiplicity_lower),
                12,
            ),
            outer_partition_label_bits=_ceil_log2(partition_count),
            maximum_exact_coordinate_address_bits=address_bits,
            compact_coordinate_address=True,
            polynomial_outer_block_count=False,
            polynomial_dense_block_dimension_proved=False,
            internal_kronecker_basis_transform_proved=False,
            sparse_carrier_product_rules_proved=False,
            status=(
                "exact-harmonic-identity-dense-multiplicity-blocks"
                if exact_identity
                else (
                    "failed-harmonic-burnside-identity"
                    if exact_identity is False
                    else "theorem-tail-factorial-average-block-lower-bound"
                )
            ),
        ),
        blocks,
    )


def run_self_dual_wreath_harmonic_carrier_schema(
    spec: WreathHarmonicCarrierSpec = WreathHarmonicCarrierSpec(),
) -> SelfDualWreathHarmonicCarrierReport:
    scaling_records: list[HarmonicCarrierScalingRecord] = []
    block_records: list[HarmonicMultiplicityBlockRecord] = []
    for n in spec.exact_n_values:
        scaling, blocks = audit_harmonic_carrier_scaling(n, exact=True)
        scaling_records.append(scaling)
        block_records.extend(blocks)
    for n in spec.tail_n_values:
        if n in spec.exact_n_values:
            continue
        scaling, _ = audit_harmonic_carrier_scaling(n, exact=False)
        scaling_records.append(scaling)

    exact_records = [record for record in scaling_records if record.exact]
    identity_records = [
        record
        for record in exact_records
        if record.harmonic_burnside_identity_verified
    ]
    non_multiplicity_free = [
        block
        for block in block_records
        if block.conjugation_multiplicity > 1
    ]
    metrics: dict[str, int | float] = {
        "scaling_record_count": len(scaling_records),
        "exact_scaling_record_count": len(exact_records),
        "harmonic_burnside_identity_verification_count": len(
            identity_records
        ),
        "exact_block_record_count": len(block_records),
        "non_multiplicity_free_block_count": len(non_multiplicity_free),
        "maximum_n": max(
            (record.n for record in scaling_records),
            default=0,
        ),
        "maximum_exact_conjugation_multiplicity": max(
            (
                record.maximum_exact_multiplicity or 0
                for record in exact_records
            ),
            default=0,
        ),
        "maximum_log2_certified_block_coordinate_lower_bound": max(
            (
                record.log2_certified_maximum_block_coordinate_lower_bound
                for record in scaling_records
            ),
            default=0.0,
        ),
        "maximum_log2_certified_multiplicity_lower_bound": max(
            (
                record.log2_certified_maximum_multiplicity_lower_bound
                for record in scaling_records
            ),
            default=0.0,
        ),
        "compact_harmonic_coordinate_schema_count": len(scaling_records),
        "internal_kronecker_basis_transform_count": 0,
        "sparse_carrier_product_rule_count": 0,
        "uniform_coherent_harmonic_transform_count": 0,
        "polynomial_structured_frame_preconditioner_count": 0,
        "polynomial_frame_inverse_count": 0,
        "carrier_sensitive_povm_circuit_count": 0,
        "polynomial_hidden_permutation_decoder_count": 0,
    }
    all_identities = (
        len(identity_records) == len(exact_records) and bool(exact_records)
    )
    return SelfDualWreathHarmonicCarrierReport(
        created_at=utc_now(),
        spec=spec,
        representation_reduction={
            "conjugation_module": (
                "K_n=C[S_n]=direct_sum_lambda End(V_lambda)"
            ),
            "kronecker_decomposition": (
                "K_n=direct_sum_nu V_nu tensor C^{m_nu}, with "
                "m_nu=sum_lambda g(lambda,lambda,nu)"
            ),
            "depth_three_invariants": (
                "(K_n tensor K_n)^{S_n}=direct_sum_nu "
                "C^{m_nu} tensor C^{m_nu}"
            ),
            "dimension_identity": (
                "sum_nu m_nu^2=sum_{alpha partition n} z_alpha"
            ),
            "factorial_block_lower_bound": (
                "max_nu m_nu^2 >= n!/p(n), because the identity "
                "conjugacy class alone contributes n! invariant coordinates"
            ),
            "compact_address": (
                "One coordinate can be named by (nu,a,b) using polynomially "
                "many bits, despite a superpolynomial number of coordinates."
            ),
            "qft_boundary": (
                "Even granting an efficient S_n group QFT, resolving the "
                "internal lambda tensor lambda Kronecker multiplicity basis "
                "and carrier-product recouplings remains a separate problem."
            ),
        },
        block_records=block_records,
        scaling_records=scaling_records,
        headline_metrics=metrics,
        claim_gate={
            "depth_three_harmonic_burnside_identity_verified": all_identities,
            "compact_coordinate_addresses_exist": True,
            "outer_partition_block_count_is_polynomial": False,
            "all_multiplicity_blocks_are_polynomial_dimensional": False,
            "efficient_sn_qft_alone_resolves_carrier_blocks": False,
            "internal_kronecker_basis_transform_proved": False,
            "sparse_carrier_product_rules_proved": False,
            "uniform_coherent_harmonic_transform_proved": False,
            "polynomial_structured_frame_preconditioner_proved": False,
            "polynomial_frame_inverse_proved": False,
            "carrier_sensitive_povm_circuit_proved": False,
            "polynomial_hidden_permutation_decoder_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The exact harmonic labels are now known, but p(n) outer "
                "sectors and a certified n!/p(n) dense multiplicity-block "
                "coordinate lower bound prevent dense enumeration. No sparse "
                "Kronecker transform or carrier-product recurrence is proved."
            ),
        },
        status="harmonic-block-schema-derived-factorial-multiplicity-open",
        summary=(
            f"Verified the harmonic/Burnside identity on "
            f"{len(identity_records)}/{len(exact_records)} exact sizes through "
            f"n={max(spec.exact_n_values, default=0)}; the tail through "
            f"n={metrics['maximum_n']} forces a maximum multiplicity block "
            "with at least "
            f"2^{metrics['maximum_log2_certified_block_coordinate_lower_bound']:.3f} "
            "coordinates, while coherent internal transforms remain zero."
        ),
        falsifiers_triggered=[
            "Replacing simultaneous-conjugacy orbits by partition labels does not make the number of outer sectors polynomial.",
            "A compact (partition,multiplicity-index) address does not make dense multiplicity-block operations efficient.",
            "At least one depth-three harmonic block has n!/p(n) matrix coordinates.",
            "An S_n group QFT does not by itself choose an internal Kronecker multiplicity basis.",
            "Exact finite Kronecker tables are not sparse all-n carrier-product or recoupling rules.",
        ],
    )


def write_self_dual_wreath_harmonic_carrier_schema(
    path: Path = SELF_DUAL_WREATH_HARMONIC_CARRIER_SCHEMA_PATH,
    spec: WreathHarmonicCarrierSpec = WreathHarmonicCarrierSpec(),
    write_registry: bool = True,
    registry_experiment_id: str = DEFAULT_EXPERIMENT_ID,
    registry_candidate_id: str = DEFAULT_CANDIDATE_ID,
    registry_result_id: str | None = None,
) -> dict[str, Any]:
    payload = asdict(
        run_self_dual_wreath_harmonic_carrier_schema(spec=spec)
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    if write_registry:
        upsert_negative_result(
            NegativeResultRecord(
                id="NEG-CODE-SELF-DUAL-WREATH-COMPACT-HARMONIC-LABELS-NOT-TRANSFORM",
                source=str(path),
                claim=(
                    "Compact irreducible and multiplicity labels make the "
                    "depth-three carrier transform polynomial."
                ),
                reason_invalid=(
                    "The harmonic/Burnside identity forces p(n) outer labels "
                    "and at least one multiplicity block with n!/p(n) matrix "
                    "coordinates. Compact addresses do not provide sparse "
                    "matrix elements, recoupling rules, or a coherent basis."
                ),
                lesson=(
                    "Search for uniform sparse Kronecker recurrences or "
                    "implicit block encodings; never materialize dense "
                    "multiplicity blocks."
                ),
                applies_to=[registry_candidate_id, registry_experiment_id],
                evidence=payload["headline_metrics"],
            )
        )
        result_id = (
            registry_result_id
            or f"RESULT-{registry_experiment_id}-LATEST"
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
                    "self_dual_wreath_harmonic_carrier_schema": str(path)
                },
            )
        )
    return payload


if __name__ == "__main__":
    report = write_self_dual_wreath_harmonic_carrier_schema()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))

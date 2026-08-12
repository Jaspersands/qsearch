"""Transfer a proved Kronecker commutant gap into the wreath carrier schema.

The bounded-support commutant certificate proves an all-n normalized gap for

    lambda_n = (n-2,2),
    nu_n = (n-3,2,1),
    g(lambda_n,lambda_n,nu_n) = 2.

This is directly relevant to the conjugation-module decomposition used by the
depth-three wreath carrier: equal-source sectors V_lambda tensor V_lambda are
exactly its internal Kronecker summands.  Conditional on routing to this
source/target sector, a polynomial LCU Hamiltonian separates the two
multiplicity copies with normalized gap 2/[n(n-1)].

The transfer is real but extremely narrow.  It resolves four invariant matrix
coordinates inside a simultaneous-conjugacy carrier space with at least n!
coordinates, and it does not control carrier-induced mixing between source
lambda sectors.  Its coverage is therefore at most 4/n!, while the remaining
equal-source multiplicity sectors grow rapidly.  This audit records the useful
primitive without promoting it to a frame transform or decoder.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from coset_commutant_gap_certificate import (
    build_commutant_gap_certificate,
)
from representation_obstruction import integer_partitions
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
from symmetric_character import kronecker_coefficient


SELF_DUAL_WREATH_COMMUTANT_TRANSFER_PATH = Path(
    "research/representation/self_dual_wreath_commutant_transfer_audit.json"
)
DEFAULT_EXPERIMENT_ID = "EXP-CODE-SELF-DUAL-WREATH-COMMUTANT-TRANSFER-AUDIT"
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


@dataclass(frozen=True)
class WreathCommutantTransferSpec:
    exact_n_values: tuple[int, ...] = tuple(range(6, 13))
    tail_n_values: tuple[int, ...] = (16, 20, 24, 32, 48, 64)


@dataclass(frozen=True)
class RestrictedCommutantTransferRecord:
    n: int
    exact: bool
    source_partition: tuple[int, ...]
    target_partition: tuple[int, ...]
    kronecker_multiplicity: int
    resolved_multiplicity_basis_state_count: int
    resolved_invariant_matrix_coordinate_count: int
    normalized_gap_exact: str
    normalized_gap: float
    inverse_gap_query_bound: int
    equal_source_nonzero_sector_count: int | None
    equal_source_nontrivial_multiplicity_sector_count: int | None
    equal_source_internal_multiplicity_state_count: int | None
    unresolved_internal_multiplicity_state_count: int | None
    exact_total_invariant_coordinate_count_decimal: str | None
    restricted_coordinate_coverage_upper_bound: float
    negative_log2_restricted_coordinate_coverage_upper_bound: float
    source_target_routing_proved: bool
    internal_multiplicity_label_proved: bool
    cross_source_carrier_mixing_controlled: bool
    carrier_frame_invariant_subspace_proved: bool
    status: str


@dataclass(frozen=True)
class SelfDualWreathCommutantTransferReport:
    created_at: str
    spec: WreathCommutantTransferSpec
    source_certificate: dict[str, Any]
    interface_contract: dict[str, Any]
    records: list[RestrictedCommutantTransferRecord]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, bool | str]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _equal_source_sector_statistics(
    n: int,
) -> tuple[int, int, int]:
    partitions = integer_partitions(n)
    multiplicities = [
        kronecker_coefficient(source, source, target)
        for source in partitions
        for target in partitions
    ]
    nonzero = [value for value in multiplicities if value]
    nontrivial = [value for value in nonzero if value > 1]
    return len(nonzero), len(nontrivial), sum(nontrivial)


def audit_restricted_commutant_transfer(
    n: int,
    exact: bool = True,
) -> RestrictedCommutantTransferRecord:
    if n < 6:
        raise ValueError("the restricted gap theorem requires n >= 6")
    source = (n - 2, 2)
    target = (n - 3, 2, 1)
    multiplicity = (
        kronecker_coefficient(source, source, target)
        if exact
        else 2
    )
    if multiplicity != 2:
        raise ArithmeticError(
            "restricted commutant family must have multiplicity two"
        )

    if exact:
        nonzero_count, nontrivial_count, nontrivial_states = (
            _equal_source_sector_statistics(n)
        )
        invariant_coordinates = simultaneous_conjugacy_orbit_count(n, 2)
        coverage = 4.0 / invariant_coordinates
        unresolved_states = max(0, nontrivial_states - multiplicity)
        invariant_decimal: str | None = str(invariant_coordinates)
    else:
        nonzero_count = None
        nontrivial_count = None
        nontrivial_states = None
        unresolved_states = None
        coverage = 4.0 / math.factorial(n)
        invariant_decimal = None

    normalized_gap = 2.0 / (n * (n - 1))
    return RestrictedCommutantTransferRecord(
        n=n,
        exact=exact,
        source_partition=source,
        target_partition=target,
        kronecker_multiplicity=multiplicity,
        resolved_multiplicity_basis_state_count=2,
        resolved_invariant_matrix_coordinate_count=4,
        normalized_gap_exact=f"2/({n}*{n - 1})",
        normalized_gap=normalized_gap,
        inverse_gap_query_bound=n * (n - 1) // 2,
        equal_source_nonzero_sector_count=nonzero_count,
        equal_source_nontrivial_multiplicity_sector_count=nontrivial_count,
        equal_source_internal_multiplicity_state_count=nontrivial_states,
        unresolved_internal_multiplicity_state_count=unresolved_states,
        exact_total_invariant_coordinate_count_decimal=invariant_decimal,
        restricted_coordinate_coverage_upper_bound=coverage,
        negative_log2_restricted_coordinate_coverage_upper_bound=round(
            -math.log2(coverage),
            12,
        ),
        source_target_routing_proved=True,
        internal_multiplicity_label_proved=True,
        cross_source_carrier_mixing_controlled=False,
        carrier_frame_invariant_subspace_proved=False,
        status=(
            "exact-restricted-gap-transfer-factorial-coverage"
            if exact
            else "theorem-tail-restricted-gap-factorial-coverage-upper-bound"
        ),
    )


def run_self_dual_wreath_commutant_transfer_audit(
    spec: WreathCommutantTransferSpec = WreathCommutantTransferSpec(),
) -> SelfDualWreathCommutantTransferReport:
    source = build_commutant_gap_certificate()
    source_metrics = source.headline_metrics
    theorem_proved = bool(
        source_metrics.get("all_n_critical_gap_theorem_count", 0)
    )
    records = [
        audit_restricted_commutant_transfer(n, exact=True)
        for n in spec.exact_n_values
    ]
    records.extend(
        audit_restricted_commutant_transfer(n, exact=False)
        for n in spec.tail_n_values
        if n not in spec.exact_n_values
    )
    exact_records = [record for record in records if record.exact]
    metrics: dict[str, int | float] = {
        "record_count": len(records),
        "exact_record_count": len(exact_records),
        "maximum_n": max((record.n for record in records), default=0),
        "restricted_all_n_inverse_polynomial_gap_theorem_count": int(
            theorem_proved
        ),
        "restricted_equal_source_family_count": 1,
        "restricted_multiplicity_basis_state_count": 2,
        "restricted_invariant_matrix_coordinate_count": 4,
        "maximum_exact_equal_source_nonzero_sector_count": max(
            (
                record.equal_source_nonzero_sector_count or 0
                for record in exact_records
            ),
            default=0,
        ),
        "maximum_exact_nontrivial_multiplicity_sector_count": max(
            (
                record.equal_source_nontrivial_multiplicity_sector_count or 0
                for record in exact_records
            ),
            default=0,
        ),
        "maximum_exact_unresolved_internal_multiplicity_state_count": max(
            (
                record.unresolved_internal_multiplicity_state_count or 0
                for record in exact_records
            ),
            default=0,
        ),
        "maximum_inverse_gap_query_bound": max(
            (record.inverse_gap_query_bound for record in records),
            default=0,
        ),
        "maximum_negative_log2_restricted_coordinate_coverage_upper_bound": max(
            (
                record.negative_log2_restricted_coordinate_coverage_upper_bound
                for record in records
            ),
            default=0.0,
        ),
        "general_equal_source_gap_theorem_count": 0,
        "cross_source_carrier_mixing_rule_count": 0,
        "carrier_frame_invariant_subspace_count": 0,
        "uniform_coherent_harmonic_transform_count": 0,
        "polynomial_structured_frame_preconditioner_count": 0,
        "polynomial_frame_inverse_count": 0,
        "polynomial_hidden_permutation_decoder_count": 0,
    }
    return SelfDualWreathCommutantTransferReport(
        created_at=utc_now(),
        spec=spec,
        source_certificate={
            "module": "coset_commutant_gap_certificate.py",
            "status": source.status,
            "theorem": source.theorem,
            "exact_gap_certificate": source.exact_gap_certificate,
            "headline_metrics": source_metrics,
        },
        interface_contract={
            "input": (
                "A state routed to source lambda_n=(n-2,2) and target "
                "nu_n=(n-3,2,1) inside V_lambda tensor V_lambda."
            ),
            "operation": (
                "Block encode the transposition/3-cycle same-support orbit "
                "sum and phase-estimate its two multiplicity eigenvalues."
            ),
            "normalized_gap": "2/[n(n-1)]",
            "cost": "O(n^2 log(1/error)) block-encoding queries",
            "produces": (
                "A coherent parity/multiplicity label for this one "
                "multiplicity-two equal-source sector."
            ),
            "does_not_produce": [
                "matrix elements of the actual wreath carrier generators",
                "control of mixing between different source lambda sectors",
                "a proof that the restricted sector is invariant under B_k",
                "a complete internal Kronecker transform",
                "a frame preconditioner or hidden-permutation decoder",
            ],
        },
        records=records,
        headline_metrics=metrics,
        claim_gate={
            "restricted_equal_source_gap_transfers": theorem_proved,
            "restricted_internal_multiplicity_label_is_polynomial": (
                theorem_proved
            ),
            "restricted_sector_has_nonnegligible_carrier_coverage": False,
            "general_equal_source_gap_theorem_proved": False,
            "cross_source_carrier_mixing_controlled": False,
            "restricted_sector_invariant_under_carrier_frame_proved": False,
            "uniform_coherent_harmonic_transform_proved": False,
            "polynomial_structured_frame_preconditioner_proved": False,
            "polynomial_frame_inverse_proved": False,
            "polynomial_hidden_permutation_decoder_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "One multiplicity-two equal-source block has a genuine "
                "inverse-polynomial label gap, but it covers at most 4/n! "
                "carrier coordinates and lacks carrier invariance or "
                "cross-source matrix elements."
            ),
        },
        status=(
            "restricted-commutant-gap-transfers-factorial-coverage-fails"
            if theorem_proved
            else "restricted-commutant-gap-source-certificate-failed"
        ),
        summary=(
            "Transferred one all-n multiplicity-two commutant gap into the "
            "wreath harmonic schema, but its carrier-coordinate coverage is "
            "at most 2^-"
            f"{metrics['maximum_negative_log2_restricted_coordinate_coverage_upper_bound']:.3f} "
            f"through n={metrics['maximum_n']}; general and cross-source "
            "transforms remain zero."
        ),
        falsifiers_triggered=[
            "The existing all-n commutant gap does apply to one equal-source wreath harmonic sector.",
            "That sector resolves only four invariant matrix coordinates.",
            "Restricted coordinate coverage is at most 4/n! and is factorially small.",
            "A source/target multiplicity label does not prove invariance under the actual wreath frame.",
            "No matrix elements controlling carrier-induced mixing between source partitions are supplied.",
        ],
    )


def write_self_dual_wreath_commutant_transfer_audit(
    path: Path = SELF_DUAL_WREATH_COMMUTANT_TRANSFER_PATH,
    spec: WreathCommutantTransferSpec = WreathCommutantTransferSpec(),
    write_registry: bool = True,
    registry_experiment_id: str = DEFAULT_EXPERIMENT_ID,
    registry_candidate_id: str = DEFAULT_CANDIDATE_ID,
    registry_result_id: str | None = None,
) -> dict[str, Any]:
    payload = asdict(
        run_self_dual_wreath_commutant_transfer_audit(spec=spec)
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    return payload


if __name__ == "__main__":
    report = write_self_dual_wreath_commutant_transfer_audit()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))

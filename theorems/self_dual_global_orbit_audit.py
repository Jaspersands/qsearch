"""Global orbit and Construction-A audit for self-dual code equivalence.

Bounded local rank/hull profiles are forced to collapse on growing-distance
self-dual codes.  The next classical architecture is global: choose an
information set, normalize its columns to the identity, and compare the
resulting column multiset.  Enumerating every information set is exact, but can
be exponential when the rank grows.  Sampling can find exact equivalence
witnesses, but failure to find an intersection is not non-equivalence evidence.

This module:

* certifies basis-normalized column-multiset invariance under row operations
  and mapped coordinate permutations;
* measures information-set density and normalized-orbit diversity;
* searches for exact matching normalized keys without treating misses as
  rejections;
* audits the standard Construction-A unimodular lattice invariants, including
  parity, minimum norm, and the exact norm-two vector count
  ``2n + 16 A_4``;
* records the missing reverse/frame-preservation argument explicitly.

The experiment diagnoses two classical routes.  It does not prove that all
polynomial canonicalization is impossible and does not imply a quantum
advantage.
"""

from __future__ import annotations

import hashlib
import itertools
import json
import math
import random
from collections import Counter
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Sequence

import numpy as np

from code_schur_filtration import row_basis
from research_registry import (
    ExperimentResultRecord,
    NegativeResultRecord,
    upsert_experiment_result,
    upsert_negative_result,
    utc_now,
)
from self_dual_code_boundary_search import SELF_DUAL_CODE_BOUNDARY_PATH


SELF_DUAL_GLOBAL_ORBIT_PATH = Path(
    "research/code_equivalence/self_dual_global_orbit_audit.json"
)
DEFAULT_EXPERIMENT_ID = "EXP-CODE-SELF-DUAL-GLOBAL-ORBIT-AUDIT"
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


@dataclass(frozen=True)
class GlobalOrbitAuditSpec:
    sampled_information_sets: int = 768
    exact_subset_cap: int = 20_000
    maximum_pair_audits_per_family: int = 4
    seed: int = 72_911


@dataclass(frozen=True)
class InformationSetOrbitRecord:
    family_id: str
    instance_id: str
    dimension: int
    length: int
    total_candidate_subsets: int
    subset_trials: int
    exact_subset_enumeration: bool
    accepted_information_set_count: int
    information_set_fraction: float
    information_set_fraction_interval_95: tuple[float, float]
    estimated_log2_information_set_count: float | None
    normalized_key_count: int
    maximum_key_multiplicity: int
    normalized_key_unique_fraction: float
    mapped_permutation_control_passed: bool
    cost_model: str
    status: str
    interpretation: str


@dataclass(frozen=True)
class ConstructionALatticeRecord:
    family_id: str
    instance_id: str
    dimension: int
    length: int
    preimage_lattice_determinant: int
    scaled_lattice_covolume: float
    unimodular_certificate_passed: bool
    lattice_parity: str
    weight_two_codeword_count: int
    weight_four_codeword_count: int
    minimum_norm: float
    norm_two_vector_count: int
    frame_preserving_reverse_reduction_proved: bool
    status: str
    interpretation: str


@dataclass(frozen=True)
class GlobalOrbitPairAudit:
    id: str
    family_id: str
    left_id: str
    right_id: str
    sampled_left_key_count: int
    sampled_right_key_count: int
    exact_normalized_key_intersection_count: int
    equivalence_witness_found: bool
    no_intersection_is_nonequivalence_evidence: bool
    status: str
    interpretation: str


@dataclass(frozen=True)
class GlobalOrbitFamilyRecord:
    family_id: str
    dimension: int
    instance_count: int
    mean_information_set_fraction: float
    maximum_estimated_log2_information_sets: float | None
    mapped_control_failure_count: int
    sampled_equivalence_witness_count: int
    no_intersection_proof_debt_count: int
    construction_a_unimodular_count: int
    construction_a_invariant_class_count: int
    frame_preserving_reverse_reduction_count: int
    status: str
    interpretation: str


@dataclass(frozen=True)
class SelfDualGlobalOrbitReport:
    created_at: str
    spec: GlobalOrbitAuditSpec
    reduction_contracts: list[dict[str, Any]]
    information_set_records: list[InformationSetOrbitRecord]
    lattice_records: list[ConstructionALatticeRecord]
    pair_audits: list[GlobalOrbitPairAudit]
    family_records: list[GlobalOrbitFamilyRecord]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, bool | str]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _read_json(path: Path, fallback: Any) -> Any:
    if not path.exists():
        return fallback
    try:
        return json.loads(path.read_text())
    except (json.JSONDecodeError, OSError):
        return fallback


def gf2_inverse(matrix: np.ndarray) -> np.ndarray | None:
    values = np.asarray(matrix, dtype=np.uint8).copy() & 1
    if values.ndim != 2 or values.shape[0] != values.shape[1]:
        raise ValueError("matrix must be square")
    size = int(values.shape[0])
    augmented = np.concatenate((values, np.eye(size, dtype=np.uint8)), axis=1)
    rank = 0
    for column in range(size):
        pivot = next((row for row in range(rank, size) if augmented[row, column]), None)
        if pivot is None:
            return None
        if pivot != rank:
            augmented[[rank, pivot]] = augmented[[pivot, rank]]
        for row in range(size):
            if row != rank and augmented[row, column]:
                augmented[row] ^= augmented[rank]
        rank += 1
    return augmented[:, size:]


def basis_normalized_column_key(
    generator: np.ndarray,
    basis_coordinates: Sequence[int],
) -> tuple[int, ...] | None:
    code = row_basis(generator)
    coordinates = tuple(int(value) for value in basis_coordinates)
    if len(coordinates) != code.shape[0] or len(set(coordinates)) != len(coordinates):
        raise ValueError("basis coordinate count must equal code dimension")
    basis = code[:, coordinates]
    inverse = gf2_inverse(basis)
    if inverse is None:
        return None
    normalized = (inverse @ code) & 1
    columns = []
    for coordinate in range(normalized.shape[1]):
        value = 0
        for row, bit in enumerate(normalized[:, coordinate].tolist()):
            if bit:
                value |= 1 << row
        columns.append(value)
    return tuple(sorted(columns))


def _key_digest(key: tuple[int, ...]) -> str:
    return hashlib.sha256(repr(key).encode("ascii")).hexdigest()[:24]


def _candidate_subsets(
    length: int,
    dimension: int,
    sample_count: int,
    exact_cap: int,
    rng: random.Random,
) -> tuple[list[tuple[int, ...]], bool, int]:
    total = math.comb(length, dimension)
    if total <= exact_cap:
        return list(itertools.combinations(range(length), dimension)), True, total
    target = min(sample_count, total)
    selected: set[tuple[int, ...]] = set()
    while len(selected) < target:
        selected.add(tuple(sorted(rng.sample(range(length), dimension))))
    return sorted(selected), False, total


def _wilson_interval(successes: int, trials: int) -> tuple[float, float]:
    if trials <= 0:
        return (0.0, 1.0)
    z = 1.959963984540054
    fraction = successes / trials
    denominator = 1 + z * z / trials
    center = (fraction + z * z / (2 * trials)) / denominator
    radius = (
        z
        * math.sqrt(fraction * (1 - fraction) / trials + z * z / (4 * trials * trials))
        / denominator
    )
    return (max(0.0, center - radius), min(1.0, center + radius))


def _permutation_control(
    generator: np.ndarray,
    accepted_basis: tuple[int, ...] | None,
    seed: int,
) -> bool:
    if accepted_basis is None:
        return False
    rng = random.Random(seed)
    length = int(generator.shape[1])
    permutation = list(range(length))
    rng.shuffle(permutation)
    permuted = generator[:, permutation]
    inverse_permutation = [0] * length
    for new_coordinate, old_coordinate in enumerate(permutation):
        inverse_permutation[old_coordinate] = new_coordinate
    mapped_basis = tuple(inverse_permutation[coordinate] for coordinate in accepted_basis)
    left = basis_normalized_column_key(generator, accepted_basis)
    right = basis_normalized_column_key(permuted, mapped_basis)
    return left is not None and left == right


def audit_information_set_orbit(
    family_id: str,
    instance: dict[str, Any],
    spec: GlobalOrbitAuditSpec,
) -> tuple[InformationSetOrbitRecord, dict[tuple[int, ...], int]]:
    generator = row_basis(np.asarray(instance["generator"], dtype=np.uint8))
    dimension, length = map(int, generator.shape)
    seed = spec.seed + sum(ord(char) for char in str(instance.get("id", "")))
    subsets, exact, total = _candidate_subsets(
        length,
        dimension,
        spec.sampled_information_sets,
        spec.exact_subset_cap,
        random.Random(seed),
    )
    keys: Counter[tuple[int, ...]] = Counter()
    first_basis = None
    for coordinates in subsets:
        key = basis_normalized_column_key(generator, coordinates)
        if key is None:
            continue
        keys[key] += 1
        if first_basis is None:
            first_basis = coordinates
    accepted = sum(keys.values())
    fraction = accepted / len(subsets) if subsets else 0.0
    interval = _wilson_interval(accepted, len(subsets))
    estimated = (
        math.log2(total * fraction)
        if fraction > 0
        else None
    )
    control = _permutation_control(generator, first_basis, seed + 31)
    unique_fraction = len(keys) / accepted if accepted else 0.0
    return (
        InformationSetOrbitRecord(
            family_id=family_id,
            instance_id=str(instance.get("id", "unknown-self-dual-instance")),
            dimension=dimension,
            length=length,
            total_candidate_subsets=total,
            subset_trials=len(subsets),
            exact_subset_enumeration=exact,
            accepted_information_set_count=accepted,
            information_set_fraction=round(fraction, 9),
            information_set_fraction_interval_95=tuple(round(value, 9) for value in interval),
            estimated_log2_information_set_count=round(estimated, 6) if estimated is not None else None,
            normalized_key_count=len(keys),
            maximum_key_multiplicity=max(keys.values(), default=0),
            normalized_key_unique_fraction=round(unique_fraction, 9),
            mapped_permutation_control_passed=control,
            cost_model=(
                "Exact enumeration of every k-subset."
                if exact
                else (
                    f"Uniform sample without replacement of {len(subsets)} among C({length},{dimension})={total} "
                    "candidate information sets. Estimates are not lower bounds."
                )
            ),
            status=(
                "information-set-orbit-audit-complete"
                if control
                else "rejected-information-set-mapped-control-failure"
            ),
            interpretation=(
                "Basis-normalized keys are exact equivalence witnesses when they match. Orbit size estimates diagnose "
                "exhaustive information-set canonization only; a sampled miss is not a rejection."
                if control
                else "The mapped-basis permutation control failed; reject the orbit audit."
            ),
        ),
        dict(keys),
    )


def _column_values(generator: np.ndarray) -> list[int]:
    code = row_basis(generator)
    values = []
    for coordinate in range(code.shape[1]):
        value = 0
        for row, bit in enumerate(code[:, coordinate].tolist()):
            if bit:
                value |= 1 << row
        values.append(value)
    return values


def _zero_sum_support_count(generator: np.ndarray, order: int) -> int:
    columns = _column_values(generator)
    count = 0
    for coordinates in itertools.combinations(range(len(columns)), order):
        total = 0
        for coordinate in coordinates:
            total ^= columns[coordinate]
        count += total == 0
    return int(count)


def construction_a_lattice_record(
    family_id: str,
    instance: dict[str, Any],
) -> ConstructionALatticeRecord:
    generator = row_basis(np.asarray(instance["generator"], dtype=np.uint8))
    dimension, length = map(int, generator.shape)
    systematic = bool(
        length == 2 * dimension
        and np.array_equal(generator[:, :dimension], np.eye(dimension, dtype=np.uint8))
    )
    preimage_determinant = 1 << dimension
    covolume = preimage_determinant / (2 ** (length / 2))
    weight_two = _zero_sum_support_count(generator, 2)
    weight_four = _zero_sum_support_count(generator, 4)
    minimum_norm = 1.0 if weight_two else 2.0
    doubly_even = all(int(row.sum()) % 4 == 0 for row in generator)
    roots = 2 * length + 16 * weight_four
    unimodular = systematic and length == 2 * dimension and abs(covolume - 1.0) < 1e-12
    return ConstructionALatticeRecord(
        family_id=family_id,
        instance_id=str(instance.get("id", "unknown-self-dual-instance")),
        dimension=dimension,
        length=length,
        preimage_lattice_determinant=preimage_determinant,
        scaled_lattice_covolume=covolume,
        unimodular_certificate_passed=unimodular,
        lattice_parity="even" if doubly_even else "odd",
        weight_two_codeword_count=weight_two,
        weight_four_codeword_count=weight_four,
        minimum_norm=minimum_norm,
        norm_two_vector_count=roots,
        frame_preserving_reverse_reduction_proved=False,
        status=(
            "construction-a-unimodular-local-invariants-certified"
            if unimodular
            else "rejected-construction-a-certificate-failure"
        ),
        interpretation=(
            "Code equivalence gives a coordinate-frame-preserving lattice isometry. Determinant, parity, minimum norm, "
            "and norm-two counts are valid lattice invariants, but the converse requires proving that an arbitrary "
            "lattice isometry preserves the coordinate frame or adding a certified gadget."
        ),
    )


def _pair_audit(
    family_id: str,
    audit: dict[str, Any],
    key_cache: dict[str, dict[tuple[int, ...], int]],
) -> GlobalOrbitPairAudit | None:
    left_id = str(audit.get("left_id", ""))
    right_id = str(audit.get("right_id", ""))
    if left_id not in key_cache or right_id not in key_cache:
        return None
    left_keys = key_cache[left_id]
    right_keys = key_cache[right_id]
    intersection = set(left_keys).intersection(right_keys)
    witness = bool(intersection)
    return GlobalOrbitPairAudit(
        id=f"global-orbit-{audit.get('id', 'unknown-pair')}",
        family_id=family_id,
        left_id=left_id,
        right_id=right_id,
        sampled_left_key_count=len(left_keys),
        sampled_right_key_count=len(right_keys),
        exact_normalized_key_intersection_count=len(intersection),
        equivalence_witness_found=witness,
        no_intersection_is_nonequivalence_evidence=False,
        status=(
            "exact-equivalence-witness-from-normalized-information-set"
            if witness
            else "no-sampled-information-set-intersection-proof-debt"
        ),
        interpretation=(
            "A shared full normalized column multiset is an exact GL(k,2)-plus-coordinate-permutation equivalence witness."
            if witness
            else (
                "No sampled normalized key intersects. Because the information-set orbit is enormous, this miss is "
                "proof debt and supplies no non-equivalence or hardness evidence."
            )
        ),
    )


def run_self_dual_global_orbit_audit(
    source_path: Path = SELF_DUAL_CODE_BOUNDARY_PATH,
    spec: GlobalOrbitAuditSpec = GlobalOrbitAuditSpec(),
) -> SelfDualGlobalOrbitReport:
    source = _read_json(source_path, {})
    information_records = []
    lattice_records = []
    pair_audits = []
    family_records = []
    key_cache: dict[str, dict[tuple[int, ...], int]] = {}
    for family in source.get("family_records", []):
        family_id = str(family.get("spec", {}).get("id", "unknown-self-dual-family"))
        family_information = []
        family_lattices = []
        for instance in family.get("instances", []):
            orbit, keys = audit_information_set_orbit(family_id, instance, spec)
            lattice = construction_a_lattice_record(family_id, instance)
            information_records.append(orbit)
            lattice_records.append(lattice)
            family_information.append(orbit)
            family_lattices.append(lattice)
            key_cache[orbit.instance_id] = keys
        audits = []
        for source_audit in family.get("collision_audits", [])[: spec.maximum_pair_audits_per_family]:
            pair = _pair_audit(family_id, source_audit, key_cache)
            if pair is not None:
                pair_audits.append(pair)
                audits.append(pair)
        control_failures = sum(not record.mapped_permutation_control_passed for record in family_information)
        witnesses = sum(record.equivalence_witness_found for record in audits)
        misses = sum(not record.equivalence_witness_found for record in audits)
        lattice_classes = {
            (
                record.lattice_parity,
                record.minimum_norm,
                record.norm_two_vector_count,
            )
            for record in family_lattices
        }
        maximum_estimate = max(
            (
                record.estimated_log2_information_set_count
                for record in family_information
                if record.estimated_log2_information_set_count is not None
            ),
            default=None,
        )
        family_records.append(
            GlobalOrbitFamilyRecord(
                family_id=family_id,
                dimension=int(family.get("spec", {}).get("dimension", 0) or 0),
                instance_count=len(family_information),
                mean_information_set_fraction=round(
                    sum(record.information_set_fraction for record in family_information)
                    / max(1, len(family_information)),
                    9,
                ),
                maximum_estimated_log2_information_sets=maximum_estimate,
                mapped_control_failure_count=control_failures,
                sampled_equivalence_witness_count=witnesses,
                no_intersection_proof_debt_count=misses,
                construction_a_unimodular_count=sum(
                    record.unimodular_certificate_passed for record in family_lattices
                ),
                construction_a_invariant_class_count=len(lattice_classes),
                frame_preserving_reverse_reduction_count=sum(
                    record.frame_preserving_reverse_reduction_proved for record in family_lattices
                ),
                status=(
                    "rejected-global-orbit-control-failure"
                    if control_failures
                    else "global-orbit-and-lattice-reduction-proof-debt"
                ),
                interpretation=(
                    "Information-set enumeration grows rapidly and low-norm Construction-A invariants may collapse. "
                    "Neither fact is a lower bound; polynomial global canonicalization and a frame-preserving reverse "
                    "reduction remain open."
                    if not control_failures
                    else "A mapped permutation control failed; reject this family audit."
                ),
            )
        )
    estimated_values = [
        record.estimated_log2_information_set_count
        for record in information_records
        if record.estimated_log2_information_set_count is not None
    ]
    metrics: dict[str, int | float] = {
        "family_count": len(family_records),
        "instance_count": len(information_records),
        "maximum_dimension": max((record.dimension for record in information_records), default=0),
        "information_set_subset_trial_count": sum(record.subset_trials for record in information_records),
        "accepted_information_set_count": sum(record.accepted_information_set_count for record in information_records),
        "normalized_information_set_key_count": sum(record.normalized_key_count for record in information_records),
        "mapped_permutation_control_failure_count": sum(record.mapped_control_failure_count for record in family_records),
        "maximum_estimated_log2_information_set_count": max(estimated_values, default=0.0),
        "sampled_equivalence_witness_count": sum(record.sampled_equivalence_witness_count for record in family_records),
        "no_intersection_proof_debt_count": sum(record.no_intersection_proof_debt_count for record in family_records),
        "construction_a_unimodular_count": sum(record.unimodular_certificate_passed for record in lattice_records),
        "construction_a_single_invariant_class_family_count": sum(
            record.construction_a_invariant_class_count == 1 for record in family_records
        ),
        "frame_preserving_reverse_reduction_count": sum(
            record.frame_preserving_reverse_reduction_count for record in family_records
        ),
        "proved_polynomial_global_canonicalization_count": 0,
        "classical_superpolynomial_lower_bound_count": 0,
        "nonabelian_measurement_necessity_count": 0,
    }
    return SelfDualGlobalOrbitReport(
        created_at=utc_now(),
        spec=spec,
        reduction_contracts=[
            {
                "id": "SELF-DUAL-CODE-TO-BINARY-MATROID",
                "direction": "iff",
                "statement": (
                    "Over F_2, code equivalence is exactly equivalence of the generator-column configuration under "
                    "GL(k,2) and coordinate permutation; this is binary linear matroid isomorphism with multiplicities."
                ),
                "implementation": "basis-normalized full column-multiset keys",
                "unresolved_obligation": (
                    "No polynomial canonical labeling for growing-rank binary matroids is implemented or proved impossible."
                ),
            },
            {
                "id": "SELF-DUAL-CODE-TO-CONSTRUCTION-A-LATTICE",
                "direction": "forward-only-in-this-module",
                "statement": (
                    "A coordinate permutation of codes induces an isometry of their scaled Construction-A unimodular lattices."
                ),
                "implementation": "determinant, parity, minimum norm, and exact norm-two vector count",
                "unresolved_obligation": (
                    "An arbitrary lattice isometry need not preserve the coordinate frame; prove frame recovery or use "
                    "a certified equivalence-preserving gadget before claiming an iff reduction."
                ),
            },
            {
                "id": "GI-HARDNESS-CONTEXT",
                "direction": "literature-context-only",
                "statement": (
                    "Petrank and Roth reduce graph isomorphism to code equivalence. This establishes a barrier for "
                    "generic polynomial classical resolution, not evidence for a quantum speedup."
                ),
                "literature_ids": [
                    "Petrank-Roth-1997-Code-Equivalence",
                    "Ducas-et-al-2024-Code-Equivalence-Isomorphism-Relations",
                    "Bardet-et-al-2019-Trivial-Hull-Code-to-GI",
                ],
            },
        ],
        information_set_records=information_records,
        lattice_records=lattice_records,
        pair_audits=pair_audits,
        family_records=family_records,
        headline_metrics=metrics,
        claim_gate={
            "mapped_information_set_controls_pass": metrics["mapped_permutation_control_failure_count"] == 0,
            "matching_normalized_key_is_exact_equivalence_witness": True,
            "sampled_key_miss_is_nonequivalence_evidence": False,
            "information_set_growth_is_general_classical_lower_bound": False,
            "construction_a_forward_reduction_certified": metrics["construction_a_unimodular_count"] == metrics["instance_count"],
            "construction_a_reverse_frame_preservation_proved": False,
            "low_norm_lattice_collision_is_hardness_evidence": False,
            "polynomial_global_canonicalization_exhausted": False,
            "classical_superpolynomial_lower_bound_proved": False,
            "nonabelian_measurement_necessity_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "Exhaustive information-set canonization has a large measured orbit and low-norm lattice invariants "
                "collapse on tail families, but these are architecture failures rather than lower bounds."
            ),
        },
        status="self-dual-global-orbit-and-lattice-routes-remain-proof-debt",
        summary=(
            f"Audited {metrics['instance_count']} self-dual codes; the largest estimated information-set count is "
            f"2^{metrics['maximum_estimated_log2_information_set_count']:.2f}, sampled exact witnesses="
            f"{metrics['sampled_equivalence_witness_count']}, sampled misses kept as debt="
            f"{metrics['no_intersection_proof_debt_count']}, and frame-preserving reverse lattice reductions="
            f"{metrics['frame_preserving_reverse_reduction_count']}."
        ),
        falsifiers_triggered=[
            "Mapped coordinate-permutation bases must produce identical full normalized column multisets.",
            "A shared normalized key is an exact equivalence witness, not a heuristic score.",
            "Failure of independent information-set samples to intersect is never a non-equivalence certificate.",
            "Estimated information-set orbit growth rejects exhaustive enumeration only, not every classical algorithm.",
            "Construction-A determinant, parity, minimum norm, and norm-two counts are charged as legal classical invariants.",
            "A forward code-to-lattice map is not represented as an iff reduction without coordinate-frame recovery.",
            "Graph-isomorphism hardness context is not represented as a classical lower bound or quantum advantage.",
        ],
    )


def write_self_dual_global_orbit_audit(
    path: Path = SELF_DUAL_GLOBAL_ORBIT_PATH,
    source_path: Path = SELF_DUAL_CODE_BOUNDARY_PATH,
    spec: GlobalOrbitAuditSpec = GlobalOrbitAuditSpec(),
    write_registry: bool = True,
    registry_experiment_id: str = DEFAULT_EXPERIMENT_ID,
    registry_candidate_id: str = DEFAULT_CANDIDATE_ID,
    registry_result_id: str | None = None,
) -> dict[str, Any]:
    payload = asdict(run_self_dual_global_orbit_audit(source_path=source_path, spec=spec))
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    return payload


if __name__ == "__main__":
    report = write_self_dual_global_orbit_audit()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))

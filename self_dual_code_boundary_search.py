"""Boundary search for self-dual binary code-equivalence families.

Random and algebraic code families in the repository are often rejected by
small or trivial hulls, low-weight structure, or an obvious canonical model.
This module probes a deliberately different natural family: binary self-dual
codes with generator ``[I | A]`` for an orthogonal matrix ``A``.  Their hull
dimension grows with the code dimension, so the trivial-hull projector route
does not apply.

The search is intentionally conservative:

* polynomial-time, basis-invariant signatures are applied at every size;
* coordinate-permutation controls must preserve every signature;
* exact weight/support and incidence-graph checks are charged as exponential
  finite-size controls;
* caps and timeouts are proof debt, never hardness or quantum evidence.

The output is a source of code-equivalence boundary rows for later
nonabelian-HSP work, not an algorithm or a speedup claim.
"""

from __future__ import annotations

import hashlib
import itertools
import json
import random
from collections import Counter
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Sequence

import numpy as np

from code_equivalence_workbench import gf2_rank, support_splitting_signature, weight_enumerator
from code_family_search import (
    gf2_nullspace_basis,
    hull_dimension,
    punctured_weight_profile,
    shortened_weight_profile,
)
from code_incidence_resolver import IncidenceIsomorphismWitness, exact_code_incidence_isomorphism
from code_schur_filtration import row_basis
from research_registry import (
    ExperimentResultRecord,
    NegativeResultRecord,
    upsert_experiment_result,
    upsert_negative_result,
    utc_now,
)


SELF_DUAL_CODE_BOUNDARY_PATH = Path("research/code_equivalence/self_dual_code_boundary_search.json")
DEFAULT_EXPERIMENT_ID = "EXP-CODE-SELF-DUAL-BOUNDARY-SEARCH"
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


@dataclass(frozen=True)
class SelfDualSearchSpec:
    id: str
    dimension: int
    instance_count: int
    transvection_steps: int
    max_collision_pairs: int
    exact_dimension_cap: int = 10
    exact_incidence_codeword_cap: int = 2_048
    exact_incidence_seconds: float = 3.0
    seed: int = 0


@dataclass(frozen=True)
class SelfDualConstructionCertificate:
    full_rank: bool
    orthogonal_matrix: bool
    self_orthogonal_generator: bool
    self_dual_dimension: bool
    hull_equals_dimension: bool
    passed: bool


@dataclass(frozen=True)
class SelfDualScalableSignature:
    length: int
    dimension: int
    hull_dimension: int
    schur_square_dimension: int
    schur_cube_dimension: int
    doubly_even: bool
    zero_column_count: int
    column_multiplicity_histogram: tuple[tuple[int, int], ...]
    coordinate_puncture_shorten_profile: tuple[tuple[tuple[int, int, int, int], int], ...]
    pair_puncture_shorten_profile: tuple[tuple[tuple[int, int, int, int], int], ...]
    digest: str


@dataclass(frozen=True)
class SelfDualExactSignature:
    evaluated: bool
    cost_model: str
    weight_enumerator: tuple[tuple[int, int], ...] | None
    support_splitting_digest: str | None
    punctured_weight_digest: str | None
    shortened_weight_digest: str | None
    digest: str | None


@dataclass(frozen=True)
class SelfDualCodeInstance:
    id: str
    certificate: SelfDualConstructionCertificate
    scalable_signature: SelfDualScalableSignature
    exact_signature: SelfDualExactSignature
    generator: list[list[int]]


@dataclass(frozen=True)
class SelfDualPairAudit:
    id: str
    pair_kind: str
    left_id: str
    right_id: str
    scalable_signatures_match: bool
    exact_signatures_evaluated: bool
    exact_signatures_match: bool | None
    incidence_witness: IncidenceIsomorphismWitness | None
    status: str
    interpretation: str
    generator_a: list[list[int]]
    generator_b: list[list[int]]


@dataclass(frozen=True)
class SelfDualFamilyRecord:
    spec: SelfDualSearchSpec
    instances: list[SelfDualCodeInstance]
    control_audits: list[SelfDualPairAudit]
    collision_audits: list[SelfDualPairAudit]
    construction_failure_count: int
    scalable_signature_class_count: int
    scalable_collision_pair_count: int
    scalable_invariant_rejection_count: int
    exact_invariant_rejection_count: int
    exact_equivalent_pair_count: int
    exact_nonequivalent_boundary_count: int
    incidence_timeout_count: int
    incidence_cap_count: int
    scalable_proof_debt_pair_count: int
    status: str
    interpretation: str


@dataclass(frozen=True)
class SelfDualBoundaryReport:
    created_at: str
    family_records: list[SelfDualFamilyRecord]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, bool | str]
    status: str
    summary: str
    falsifiers_triggered: list[str]


DEFAULT_SPECS = (
    SelfDualSearchSpec("self-dual-k6", 6, 12, 48, 4, seed=606),
    SelfDualSearchSpec("self-dual-k8", 8, 12, 64, 4, seed=808),
    SelfDualSearchSpec("self-dual-k10", 10, 10, 80, 4, seed=1010),
    SelfDualSearchSpec("self-dual-k12", 12, 8, 96, 4, seed=1212),
    SelfDualSearchSpec("self-dual-k16", 16, 8, 128, 4, seed=1616),
    SelfDualSearchSpec("self-dual-k24", 24, 6, 192, 4, seed=2424),
    SelfDualSearchSpec("self-dual-k32", 32, 6, 256, 4, seed=3232),
)


def _digest(value: Any) -> str:
    return hashlib.sha256(repr(value).encode("ascii")).hexdigest()[:24]


def random_orthogonal_matrix(
    dimension: int,
    rng: random.Random,
    steps: int,
) -> np.ndarray:
    """Generate an orthogonal binary matrix from certified generators.

    Coordinate swaps are orthogonal.  For every nonzero even-weight vector
    ``v``, ``I + vv^T`` is an orthogonal involution over F_2.  Products of
    these operations therefore remain orthogonal without rejection sampling.
    """

    if dimension < 2:
        raise ValueError("dimension must be at least two")
    matrix = np.eye(dimension, dtype=np.uint8)
    for _ in range(steps):
        if rng.random() < 0.25:
            left, right = rng.sample(range(dimension), 2)
            matrix[:, [left, right]] = matrix[:, [right, left]]
            continue
        weight = rng.randrange(2, dimension + 1, 2)
        support = rng.sample(range(dimension), weight)
        vector = np.zeros(dimension, dtype=np.uint8)
        vector[support] = 1
        matrix ^= np.outer((matrix @ vector) & 1, vector).astype(np.uint8)
    return matrix & 1


def systematic_self_dual_generator(orthogonal: np.ndarray) -> np.ndarray:
    matrix = np.asarray(orthogonal, dtype=np.uint8) & 1
    if matrix.ndim != 2 or matrix.shape[0] != matrix.shape[1]:
        raise ValueError("orthogonal matrix must be square")
    identity = np.eye(matrix.shape[0], dtype=np.uint8)
    return np.concatenate((identity, matrix), axis=1)


def construction_certificate(
    orthogonal: np.ndarray,
    generator: np.ndarray,
) -> SelfDualConstructionCertificate:
    matrix = np.asarray(orthogonal, dtype=np.uint8) & 1
    code = np.asarray(generator, dtype=np.uint8) & 1
    dimension = int(matrix.shape[0])
    identity = np.eye(dimension, dtype=np.uint8)
    full_rank = gf2_rank(code) == dimension
    orthogonal_matrix = bool(np.array_equal((matrix @ matrix.T) & 1, identity))
    self_orthogonal = not bool(np.any((code @ code.T) & 1))
    self_dual_dimension = code.shape == (dimension, 2 * dimension) and full_rank
    full_hull = hull_dimension(code) == dimension
    return SelfDualConstructionCertificate(
        full_rank=full_rank,
        orthogonal_matrix=orthogonal_matrix,
        self_orthogonal_generator=self_orthogonal,
        self_dual_dimension=self_dual_dimension,
        hull_equals_dimension=full_hull,
        passed=all((full_rank, orthogonal_matrix, self_orthogonal, self_dual_dimension, full_hull)),
    )


def _schur_power_dimension(generator: np.ndarray, degree: int) -> int:
    basis = row_basis(generator)
    products = []
    for indices in itertools.combinations_with_replacement(range(len(basis)), degree):
        product = np.ones(basis.shape[1], dtype=np.uint8)
        for index in indices:
            product &= basis[index]
        products.append(product)
    if not products:
        return 0
    return int(row_basis(np.asarray(products, dtype=np.uint8)).shape[0])


def _column_multiplicity_profile(generator: np.ndarray) -> tuple[int, tuple[tuple[int, int], ...]]:
    basis = row_basis(generator)
    columns = []
    for coordinate in range(basis.shape[1]):
        value = 0
        for row, bit in enumerate(basis[:, coordinate].tolist()):
            if bit:
                value |= 1 << row
        columns.append(value)
    multiplicities = Counter(columns)
    histogram = Counter(multiplicities.values())
    return multiplicities.get(0, 0), tuple(sorted((int(size), int(count)) for size, count in histogram.items()))


def puncture_shorten_invariant(generator: np.ndarray, coordinates: Sequence[int]) -> tuple[int, int, int, int]:
    code = row_basis(generator)
    remove = sorted(set(int(value) for value in coordinates))
    keep = [index for index in range(code.shape[1]) if index not in remove]
    punctured = row_basis(code[:, keep])
    coefficient_basis = gf2_nullspace_basis(code[:, remove].T)
    shortened = row_basis(((coefficient_basis @ code) & 1)[:, keep])
    return (
        int(punctured.shape[0]),
        hull_dimension(punctured),
        int(shortened.shape[0]),
        hull_dimension(shortened),
    )


def _profile_histogram(values: Sequence[tuple[int, int, int, int]]) -> tuple[tuple[tuple[int, int, int, int], int], ...]:
    return tuple(sorted((key, int(count)) for key, count in Counter(values).items()))


def scalable_signature(generator: np.ndarray) -> SelfDualScalableSignature:
    code = row_basis(generator)
    length = int(code.shape[1])
    coordinate_profile = _profile_histogram(
        [puncture_shorten_invariant(code, (coordinate,)) for coordinate in range(length)]
    )
    pair_profile = _profile_histogram(
        [puncture_shorten_invariant(code, pair) for pair in itertools.combinations(range(length), 2)]
    )
    zero_columns, multiplicities = _column_multiplicity_profile(code)
    square = _schur_power_dimension(code, 2)
    cube = _schur_power_dimension(code, 3)
    doubly_even = all(int(row.sum()) % 4 == 0 for row in code)
    key = (
        length,
        int(code.shape[0]),
        hull_dimension(code),
        square,
        cube,
        doubly_even,
        zero_columns,
        multiplicities,
        coordinate_profile,
        pair_profile,
    )
    return SelfDualScalableSignature(
        length=length,
        dimension=int(code.shape[0]),
        hull_dimension=hull_dimension(code),
        schur_square_dimension=square,
        schur_cube_dimension=cube,
        doubly_even=doubly_even,
        zero_column_count=zero_columns,
        column_multiplicity_histogram=multiplicities,
        coordinate_puncture_shorten_profile=coordinate_profile,
        pair_puncture_shorten_profile=pair_profile,
        digest=_digest(key),
    )


def exact_signature(generator: np.ndarray, dimension_cap: int) -> SelfDualExactSignature:
    code = row_basis(generator)
    dimension = int(code.shape[0])
    if dimension > dimension_cap:
        return SelfDualExactSignature(
            evaluated=False,
            cost_model=(
                f"Skipped at dimension {dimension}: exact codeword signatures require 2^{dimension} words, "
                f"above the declared dimension cap {dimension_cap}."
            ),
            weight_enumerator=None,
            support_splitting_digest=None,
            punctured_weight_digest=None,
            shortened_weight_digest=None,
            digest=None,
        )
    enumerator = weight_enumerator(code)
    support_digest = _digest(support_splitting_signature(code))
    punctured_digest = _digest(punctured_weight_profile(code))
    shortened_digest = _digest(shortened_weight_profile(code))
    key = (enumerator, support_digest, punctured_digest, shortened_digest)
    return SelfDualExactSignature(
        evaluated=True,
        cost_model=f"Complete enumeration of all 2^{dimension} codewords; exponential finite-size control.",
        weight_enumerator=enumerator,
        support_splitting_digest=support_digest,
        punctured_weight_digest=punctured_digest,
        shortened_weight_digest=shortened_digest,
        digest=_digest(key),
    )


def generate_self_dual_instances(spec: SelfDualSearchSpec) -> list[SelfDualCodeInstance]:
    rng = random.Random(spec.seed)
    instances = []
    for index in range(spec.instance_count):
        orthogonal = random_orthogonal_matrix(spec.dimension, rng, spec.transvection_steps)
        generator = systematic_self_dual_generator(orthogonal)
        instances.append(
            SelfDualCodeInstance(
                id=f"{spec.id}-instance-{index:02d}",
                certificate=construction_certificate(orthogonal, generator),
                scalable_signature=scalable_signature(generator),
                exact_signature=exact_signature(generator, spec.exact_dimension_cap),
                generator=generator.astype(int).tolist(),
            )
        )
    return instances


def _control_audit(spec: SelfDualSearchSpec, instance: SelfDualCodeInstance) -> SelfDualPairAudit:
    generator = np.asarray(instance.generator, dtype=np.uint8)
    rng = random.Random(spec.seed + 1_000_003)
    permutation = list(range(generator.shape[1]))
    rng.shuffle(permutation)
    permuted = generator[:, permutation]
    right_scalable = scalable_signature(permuted)
    right_exact = exact_signature(permuted, spec.exact_dimension_cap)
    scalable_match = instance.scalable_signature.digest == right_scalable.digest
    exact_match = (
        instance.exact_signature.digest == right_exact.digest
        if instance.exact_signature.evaluated and right_exact.evaluated
        else None
    )
    passed = scalable_match and exact_match is not False
    status = (
        "equivalent-control-self-dual-invariants-preserved"
        if passed
        else "rejected-self-dual-signature-control-failure"
    )
    return SelfDualPairAudit(
        id=f"{spec.id}-permutation-control",
        pair_kind="known-coordinate-permutation-control",
        left_id=instance.id,
        right_id=f"{instance.id}-permuted",
        scalable_signatures_match=scalable_match,
        exact_signatures_evaluated=right_exact.evaluated,
        exact_signatures_match=exact_match,
        incidence_witness=None,
        status=status,
        interpretation=(
            "Known coordinate permutation preserves every completed code invariant."
            if passed
            else "A known coordinate permutation changed a purported code invariant; reject the audit pipeline."
        ),
        generator_a=instance.generator,
        generator_b=permuted.astype(int).tolist(),
    )


def _unrelated_pair_audit(
    spec: SelfDualSearchSpec,
    left: SelfDualCodeInstance,
    right: SelfDualCodeInstance,
) -> SelfDualPairAudit:
    scalable_match = left.scalable_signature.digest == right.scalable_signature.digest
    exact_evaluated = left.exact_signature.evaluated and right.exact_signature.evaluated
    exact_match = (
        left.exact_signature.digest == right.exact_signature.digest
        if exact_evaluated
        else None
    )
    witness = None
    if not scalable_match:
        status = "rejected-by-scalable-self-dual-invariant"
        interpretation = "Polynomial Schur, column-matroid, or puncture/shorten data separates the pair."
    elif exact_match is False:
        status = "rejected-by-exact-self-dual-codeword-invariant"
        interpretation = "Complete exponential codeword signatures separate this finite pair."
    elif exact_evaluated:
        witness = exact_code_incidence_isomorphism(
            np.asarray(left.generator, dtype=np.uint8),
            np.asarray(right.generator, dtype=np.uint8),
            max_codewords=spec.exact_incidence_codeword_cap,
            max_search_seconds=spec.exact_incidence_seconds,
        )
        if witness.evaluated and witness.equivalent is True and witness.verification_passed:
            status = "equivalent-control-under-exact-incidence-isomorphism"
            interpretation = (
                "Independently generated matrices define coordinate-permutation-equivalent finite codes; "
                "the collision is a control, not a hard row."
            )
        elif witness.evaluated and witness.equivalent is False:
            status = "finite-nonequivalent-self-dual-boundary-proof-debt"
            interpretation = (
                "The finite pair matches completed signatures and is exactly non-equivalent. This is a boundary "
                "control only; no scalable construction, classical lower bound, or measurement necessity follows."
            )
        elif witness.timed_out:
            status = "self-dual-incidence-timeout-proof-debt"
            interpretation = "Exact finite incidence search timed out; timeout is proof debt, not hardness evidence."
        else:
            status = "self-dual-incidence-cap-proof-debt"
            interpretation = "Exact finite incidence search hit a declared cap; cap debt is not hardness evidence."
    else:
        status = "scalable-self-dual-collision-proof-debt"
        interpretation = (
            "The pair matches all implemented polynomial signatures, while exponential codeword and incidence "
            "checks are deliberately unavailable at this dimension. Add polynomial canonicalization or prove a "
            "lower bound; the collision is not quantum evidence."
        )
    return SelfDualPairAudit(
        id=f"{spec.id}-{left.id.rsplit('-', 1)[-1]}-{right.id.rsplit('-', 1)[-1]}",
        pair_kind="independently-generated-pair",
        left_id=left.id,
        right_id=right.id,
        scalable_signatures_match=scalable_match,
        exact_signatures_evaluated=exact_evaluated,
        exact_signatures_match=exact_match,
        incidence_witness=witness,
        status=status,
        interpretation=interpretation,
        generator_a=left.generator,
        generator_b=right.generator,
    )


def audit_self_dual_family(spec: SelfDualSearchSpec) -> SelfDualFamilyRecord:
    instances = generate_self_dual_instances(spec)
    control = _control_audit(spec, instances[0])
    pairs = list(itertools.combinations(instances, 2))
    pairs.sort(
        key=lambda pair: (
            pair[0].scalable_signature.digest != pair[1].scalable_signature.digest,
            pair[0].exact_signature.digest != pair[1].exact_signature.digest
            if pair[0].exact_signature.evaluated and pair[1].exact_signature.evaluated
            else False,
            pair[0].id,
            pair[1].id,
        )
    )
    audits = [_unrelated_pair_audit(spec, *pair) for pair in pairs[: spec.max_collision_pairs]]
    construction_failures = sum(not instance.certificate.passed for instance in instances)
    scalable_classes = len({instance.scalable_signature.digest for instance in instances})
    scalable_collisions = sum(audit.scalable_signatures_match for audit in audits)
    scalable_rejections = sum(audit.status == "rejected-by-scalable-self-dual-invariant" for audit in audits)
    exact_rejections = sum(audit.status == "rejected-by-exact-self-dual-codeword-invariant" for audit in audits)
    exact_equivalent = sum(audit.status == "equivalent-control-under-exact-incidence-isomorphism" for audit in audits)
    exact_nonequivalent = sum(audit.status == "finite-nonequivalent-self-dual-boundary-proof-debt" for audit in audits)
    timeouts = sum(audit.status == "self-dual-incidence-timeout-proof-debt" for audit in audits)
    caps = sum(audit.status == "self-dual-incidence-cap-proof-debt" for audit in audits)
    scalable_debt = sum(audit.status == "scalable-self-dual-collision-proof-debt" for audit in audits)
    if construction_failures or "control-failure" in control.status:
        status = "rejected-self-dual-construction-or-control-failure"
        interpretation = "Construction certification or permutation invariance failed; discard this family run."
    elif exact_nonequivalent:
        status = "finite-self-dual-boundary-proof-debt"
        interpretation = f"{exact_nonequivalent} exactly non-equivalent finite pair(s) survive completed signatures."
    elif timeouts or caps or scalable_debt:
        status = "self-dual-scalable-classical-proof-debt"
        interpretation = (
            f"{timeouts + caps + scalable_debt} pair(s) remain unresolved only after explicit classical caps "
            "or polynomial-signature collisions."
        )
    elif exact_equivalent:
        status = "self-dual-collisions-are-equivalent-controls"
        interpretation = f"All deepest completed collisions are equivalent finite controls ({exact_equivalent})."
    else:
        status = "self-dual-pairs-classically-separated"
        interpretation = "Every audited unrelated pair is separated by a completed classical invariant."
    return SelfDualFamilyRecord(
        spec=spec,
        instances=instances,
        control_audits=[control],
        collision_audits=audits,
        construction_failure_count=construction_failures,
        scalable_signature_class_count=scalable_classes,
        scalable_collision_pair_count=scalable_collisions,
        scalable_invariant_rejection_count=scalable_rejections,
        exact_invariant_rejection_count=exact_rejections,
        exact_equivalent_pair_count=exact_equivalent,
        exact_nonequivalent_boundary_count=exact_nonequivalent,
        incidence_timeout_count=timeouts,
        incidence_cap_count=caps,
        scalable_proof_debt_pair_count=scalable_debt,
        status=status,
        interpretation=interpretation,
    )


def run_self_dual_code_boundary(
    specs: Sequence[SelfDualSearchSpec] = DEFAULT_SPECS,
) -> SelfDualBoundaryReport:
    records = [audit_self_dual_family(spec) for spec in specs]
    metrics: dict[str, int | float] = {
        "family_count": len(records),
        "instance_count": sum(len(record.instances) for record in records),
        "maximum_dimension": max(record.spec.dimension for record in records),
        "maximum_length": 2 * max(record.spec.dimension for record in records),
        "construction_failure_count": sum(record.construction_failure_count for record in records),
        "growing_hull_family_count": sum(
            all(
                instance.scalable_signature.hull_dimension == record.spec.dimension
                for instance in record.instances
            )
            for record in records
        ),
        "permutation_control_count": sum(len(record.control_audits) for record in records),
        "permutation_control_failure_count": sum(
            "control-failure" in audit.status for record in records for audit in record.control_audits
        ),
        "scalable_collision_pair_count": sum(record.scalable_collision_pair_count for record in records),
        "scalable_invariant_rejection_count": sum(record.scalable_invariant_rejection_count for record in records),
        "exact_invariant_rejection_count": sum(record.exact_invariant_rejection_count for record in records),
        "exact_equivalent_pair_count": sum(record.exact_equivalent_pair_count for record in records),
        "exact_nonequivalent_boundary_count": sum(record.exact_nonequivalent_boundary_count for record in records),
        "incidence_timeout_count": sum(record.incidence_timeout_count for record in records),
        "incidence_cap_count": sum(record.incidence_cap_count for record in records),
        "scalable_proof_debt_pair_count": sum(record.scalable_proof_debt_pair_count for record in records),
        "polynomial_canonicalization_count": 0,
        "nonabelian_measurement_necessity_count": 0,
        "classical_superpolynomial_lower_bound_count": 0,
    }
    return SelfDualBoundaryReport(
        created_at=utc_now(),
        family_records=records,
        headline_metrics=metrics,
        claim_gate={
            "certified_self_dual_construction": metrics["construction_failure_count"] == 0,
            "growing_hull_family_generated": metrics["growing_hull_family_count"] == len(records),
            "known_permutation_controls_pass": metrics["permutation_control_failure_count"] == 0,
            "finite_nonequivalence_is_asymptotic_hardness": False,
            "timeout_or_cap_is_hardness_evidence": False,
            "scalable_signature_collision_is_quantum_evidence": False,
            "polynomial_classical_canonicalization_exhausted": False,
            "nonabelian_measurement_necessity_proved": False,
            "classical_superpolynomial_lower_bound_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "Growing hull removes one known trivial reduction, but matching polynomial signatures, finite exact "
                "non-equivalence, and incidence timeouts do not establish asymptotic code-equivalence hardness or "
                "the necessity of a collective nonabelian measurement."
            ),
        },
        status="self-dual-growing-hull-frontier-generated-proof-debt-only",
        summary=(
            f"Generated {metrics['instance_count']} certified self-dual codes through dimension "
            f"{metrics['maximum_dimension']}; scalable collisions/exact finite boundary/cap-timeout debt="
            f"{metrics['scalable_collision_pair_count']}/{metrics['exact_nonequivalent_boundary_count']}/"
            f"{metrics['incidence_cap_count'] + metrics['incidence_timeout_count']}."
        ),
        falsifiers_triggered=[
            "Any self-duality or full-hull certificate failure rejects the construction.",
            "Known coordinate permutations must preserve every completed invariant.",
            "Schur, column-matroid, or puncture/shorten mismatches are polynomial classical separations.",
            "Exact codeword-signature mismatches dequantize the finite collision.",
            "Independent samples that are exactly equivalent are controls, not hard instances.",
            "Finite exact non-equivalence does not imply an asymptotically hard natural family.",
            "Incidence caps and timeouts are proof debt, never hardness evidence.",
            "No code row is promoted without a classical lower bound and nonabelian measurement necessity."
        ],
    )


def write_self_dual_code_boundary(
    path: Path = SELF_DUAL_CODE_BOUNDARY_PATH,
    specs: Sequence[SelfDualSearchSpec] = DEFAULT_SPECS,
    write_registry: bool = True,
    registry_experiment_id: str = DEFAULT_EXPERIMENT_ID,
    registry_candidate_id: str = DEFAULT_CANDIDATE_ID,
    registry_result_id: str | None = None,
) -> dict[str, Any]:
    payload = asdict(run_self_dual_code_boundary(specs))
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    return payload


if __name__ == "__main__":
    report = write_self_dual_code_boundary()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))

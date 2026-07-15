"""Scalable punctured Goppa/alternant frontier for code equivalence.

The original Goppa search stops at lengths 8 and 16 and only rediscovers
semilinear controls.  This module generates punctured rootless binary
alternant/Goppa codes over GF(2^m) at lengths 48, 96, and 160.  It applies
invariants that remain meaningful when the primal code has too many words to
enumerate:

* rank, hull dimension, and primal/dual Schur-square dimensions;
* exact dual weight enumerators when the dual dimension is at most 22;
* minimum-dual-word coordinate and pair incidence histograms;
* affine-semilinear support-set equivalence checks;
* explicit baseline-cap debt at larger dual dimension.

Matching signatures are proof debt, not quantum evidence.  Sampled dual data
is never used as an exact rejection.  Known coordinate-permutation controls
verify invariance of the exact signature pipeline.
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
from typing import Sequence

import numpy as np

from code_family_search import gf2_nullspace_basis, hull_dimension
from code_schur_filtration import row_basis
from goppa_code_search import GF2m, evaluate_monic_polynomial
from research_registry import (
    ExperimentResultRecord,
    NegativeResultRecord,
    upsert_experiment_result,
    upsert_negative_result,
    utc_now,
)


GOPPA_SCALING_FRONTIER_PATH = Path(
    "research/code_equivalence/goppa_scaling_frontier.json"
)
DEFAULT_EXPERIMENT_ID = "EXP-CODE-GOPPA-SCALING-FRONTIER"
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


@dataclass(frozen=True)
class ScalableGoppaSpec:
    id: str
    field_degree: int
    goppa_degree: int
    support_length: int
    code_count: int
    exact_dual_dimension_cap: int = 22
    max_collision_pairs: int = 6
    seed: int = 0


@dataclass(frozen=True)
class ScalableGoppaSignature:
    length: int
    dimension: int
    dual_dimension: int
    hull_dimension: int
    primal_schur_square_dimension: int
    dual_schur_square_dimension: int
    exact_dual_enumeration: bool
    dual_weight_enumerator: list[int] | None
    minimum_dual_weight: int | None
    minimum_dual_word_count: int | None
    minimum_dual_coordinate_incidence_histogram: list[list[int]] | None
    minimum_dual_pair_incidence_histogram: list[list[int]] | None
    incidence_complete: bool
    exact_signature_digest: str | None
    coarse_signature: tuple[int, ...]


@dataclass(frozen=True)
class ScalableGoppaInstance:
    id: str
    coefficients: tuple[int, ...]
    support: tuple[int, ...]
    parity_rank: int
    generator: list[list[int]]
    signature: ScalableGoppaSignature


@dataclass(frozen=True)
class ScalableGoppaPairAudit:
    id: str
    left_id: str
    right_id: str
    known_equivalent: bool
    coarse_invariants_match: bool
    exact_signatures_available: bool
    exact_signatures_match: bool | None
    semilinear_support_check_complete: bool
    semilinear_support_equivalent: bool | None
    checked_semilinear_maps: int
    status: str
    interpretation: str


@dataclass(frozen=True)
class ScalableGoppaFamilyRecord:
    spec: ScalableGoppaSpec
    instances: list[ScalableGoppaInstance]
    control_audits: list[ScalableGoppaPairAudit]
    collision_audits: list[ScalableGoppaPairAudit]
    exact_dual_signature_count: int
    coarse_collision_pair_count: int
    exact_invariant_rejection_count: int
    semilinear_support_control_count: int
    proof_debt_pair_count: int
    baseline_cap_pair_count: int
    status: str
    interpretation: str


@dataclass(frozen=True)
class GoppaScalingFrontierReport:
    created_at: str
    records: list[ScalableGoppaFamilyRecord]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, bool | str]
    status: str
    summary: str
    falsifiers_triggered: list[str]


DEFAULT_SPECS = (
    ScalableGoppaSpec("goppa-scale-m6-t3-n48", 6, 3, 48, 6, seed=601),
    ScalableGoppaSpec("goppa-scale-m7-t3-n96", 7, 3, 96, 4, seed=701),
    ScalableGoppaSpec("goppa-scale-m8-t4-n160", 8, 4, 160, 3, seed=801),
)


def punctured_goppa_parity_check(
    field: GF2m,
    coefficients: Sequence[int],
    support: Sequence[int],
) -> np.ndarray:
    degree = len(coefficients)
    parity = np.zeros((degree * field.degree, len(support)), dtype=np.uint8)
    coefficient_tuple = tuple(int(value) for value in coefficients)
    for column, point in enumerate(support):
        denominator = evaluate_monic_polynomial(field, coefficient_tuple, int(point))
        if denominator == 0:
            raise ValueError("support contains a root of the Goppa polynomial")
        inverse = field.inv(denominator)
        power = 1
        for block in range(degree):
            value = field.mul(power, inverse)
            parity[block * field.degree : (block + 1) * field.degree, column] = field.bits(value)
            power = field.mul(power, int(point))
    return parity


def _random_rootless_coefficients(
    field: GF2m, degree: int, rng: random.Random, max_attempts: int = 20_000
) -> tuple[int, ...]:
    for _ in range(max_attempts):
        coefficients = tuple(rng.randrange(field.size) for _ in range(degree))
        if all(
            evaluate_monic_polynomial(field, coefficients, point) != 0
            for point in range(field.size)
        ):
            return coefficients
    raise RuntimeError("failed to sample a rootless monic polynomial")


def _schur_square_dimension(generator: np.ndarray) -> int:
    basis = row_basis(generator)
    if not len(basis):
        return 0
    products = np.asarray(
        [basis[left] & basis[right] for left in range(len(basis)) for right in range(left, len(basis))],
        dtype=np.uint8,
    )
    return int(row_basis(np.unique(products, axis=0)).shape[0])


def _row_int(row: np.ndarray) -> int:
    value = 0
    for index in np.flatnonzero(np.asarray(row, dtype=np.uint8) & 1):
        value |= 1 << int(index)
    return value


def _histogram(values: Sequence[int]) -> list[list[int]]:
    return [[int(value), int(count)] for value, count in sorted(Counter(int(item) for item in values).items())]


def exact_dual_low_weight_signature(
    dual_basis: np.ndarray,
    maximum_minimum_words: int = 50_000,
) -> tuple[list[int], int, int, list[list[int]] | None, list[list[int]] | None, bool]:
    basis = row_basis(dual_basis)
    dimension, length = map(int, basis.shape)
    row_ints = [_row_int(row) for row in basis]
    histogram = [0] * (length + 1)
    histogram[0] = 1
    minimum = length + 1
    minimum_count = 0
    minimum_words: list[int] = []
    current = 0
    previous_gray = 0
    for coefficient in range(1, 1 << dimension):
        gray = coefficient ^ (coefficient >> 1)
        changed = (gray ^ previous_gray).bit_length() - 1
        current ^= row_ints[changed]
        previous_gray = gray
        weight = current.bit_count()
        histogram[weight] += 1
        if weight < minimum:
            minimum = weight
            minimum_count = 1
            minimum_words = [current]
        elif weight == minimum:
            minimum_count += 1
            if len(minimum_words) < maximum_minimum_words:
                minimum_words.append(current)
    complete = minimum_count <= maximum_minimum_words
    if not complete:
        return histogram, minimum, minimum_count, None, None, False
    coordinate_counts = [0] * length
    pair_counts = [[0] * length for _ in range(length)]
    for word in minimum_words:
        support = [index for index in range(length) if (word >> index) & 1]
        for index in support:
            coordinate_counts[index] += 1
        for left, right in itertools.combinations(support, 2):
            pair_counts[left][right] += 1
    pair_values = [pair_counts[left][right] for left in range(length) for right in range(left + 1, length)]
    return (
        histogram,
        minimum,
        minimum_count,
        _histogram(coordinate_counts),
        _histogram(pair_values),
        True,
    )


def scalable_signature(
    generator: np.ndarray,
    exact_dual_dimension_cap: int,
) -> ScalableGoppaSignature:
    primal = row_basis(generator)
    dual = row_basis(gf2_nullspace_basis(primal))
    exact = len(dual) <= exact_dual_dimension_cap
    weight_enumerator = None
    minimum_weight = None
    minimum_count = None
    coordinate_histogram = None
    pair_histogram = None
    incidence_complete = False
    if exact:
        (
            weight_enumerator,
            minimum_weight,
            minimum_count,
            coordinate_histogram,
            pair_histogram,
            incidence_complete,
        ) = exact_dual_low_weight_signature(dual)
    primal_square = _schur_square_dimension(primal)
    dual_square = _schur_square_dimension(dual)
    hull = hull_dimension(primal)
    coarse = (
        int(primal.shape[1]),
        int(primal.shape[0]),
        int(dual.shape[0]),
        int(hull),
        int(primal_square),
        int(dual_square),
        int(minimum_weight if minimum_weight is not None else -1),
    )
    exact_payload = None
    digest = None
    if exact and incidence_complete:
        exact_payload = (
            coarse,
            tuple(weight_enumerator or ()),
            minimum_count,
            tuple(tuple(item) for item in coordinate_histogram or ()),
            tuple(tuple(item) for item in pair_histogram or ()),
        )
        digest = hashlib.sha256(repr(exact_payload).encode("ascii")).hexdigest()[:24]
    return ScalableGoppaSignature(
        length=int(primal.shape[1]),
        dimension=int(primal.shape[0]),
        dual_dimension=int(dual.shape[0]),
        hull_dimension=int(hull),
        primal_schur_square_dimension=primal_square,
        dual_schur_square_dimension=dual_square,
        exact_dual_enumeration=exact,
        dual_weight_enumerator=weight_enumerator,
        minimum_dual_weight=minimum_weight,
        minimum_dual_word_count=minimum_count,
        minimum_dual_coordinate_incidence_histogram=coordinate_histogram,
        minimum_dual_pair_incidence_histogram=pair_histogram,
        incidence_complete=incidence_complete,
        exact_signature_digest=digest,
        coarse_signature=coarse,
    )


def generate_scalable_instances(spec: ScalableGoppaSpec) -> list[ScalableGoppaInstance]:
    field = GF2m(spec.field_degree)
    if spec.support_length > field.size:
        raise ValueError("support length exceeds field size")
    instances: list[ScalableGoppaInstance] = []
    for index in range(spec.code_count):
        rng = random.Random(spec.seed + 1_000_003 * index)
        coefficients = _random_rootless_coefficients(field, spec.goppa_degree, rng)
        support = tuple(sorted(rng.sample(range(field.size), spec.support_length)))
        parity = punctured_goppa_parity_check(field, coefficients, support)
        generator = row_basis(gf2_nullspace_basis(parity))
        signature = scalable_signature(generator, spec.exact_dual_dimension_cap)
        instances.append(
            ScalableGoppaInstance(
                id=f"{spec.id}-code-{index}",
                coefficients=coefficients,
                support=support,
                parity_rank=int(row_basis(parity).shape[0]),
                generator=[[int(bit) for bit in row] for row in generator.tolist()],
                signature=signature,
            )
        )
    return instances


def semilinear_support_equivalence(
    field: GF2m,
    left_support: Sequence[int],
    right_support: Sequence[int],
    map_cap: int = 250_000,
) -> tuple[bool | None, int, bool]:
    right = set(int(value) for value in right_support)
    checked = 0
    for frobenius_power in range(field.degree):
        frobenius = [field.pow(point, 1 << frobenius_power) for point in range(field.size)]
        for scale in range(1, field.size):
            scaled = [field.mul(scale, frobenius[int(point)]) for point in left_support]
            for translate in range(field.size):
                if checked >= map_cap:
                    return None, checked, False
                checked += 1
                if {field.add(value, translate) for value in scaled} == right:
                    return True, checked, True
    return False, checked, True


def _permuted_generator(generator: np.ndarray, permutation: Sequence[int]) -> np.ndarray:
    return np.asarray(generator, dtype=np.uint8)[:, list(permutation)]


def audit_known_permutation_control(
    spec: ScalableGoppaSpec,
    instance: ScalableGoppaInstance,
) -> ScalableGoppaPairAudit:
    generator = np.asarray(instance.generator, dtype=np.uint8)
    rng = random.Random(spec.seed + 9_999_991)
    permutation = list(range(generator.shape[1]))
    rng.shuffle(permutation)
    permuted = _permuted_generator(generator, permutation)
    signature = scalable_signature(permuted, spec.exact_dual_dimension_cap)
    exact_available = (
        instance.signature.exact_signature_digest is not None
        and signature.exact_signature_digest is not None
    )
    exact_match = (
        instance.signature.exact_signature_digest == signature.exact_signature_digest
        if exact_available
        else None
    )
    coarse_match = instance.signature.coarse_signature == signature.coarse_signature
    verified = coarse_match and (exact_match is not False)
    return ScalableGoppaPairAudit(
        id=f"{spec.id}-known-permutation-control",
        left_id=instance.id,
        right_id=f"{instance.id}-permuted",
        known_equivalent=True,
        coarse_invariants_match=coarse_match,
        exact_signatures_available=exact_available,
        exact_signatures_match=exact_match,
        semilinear_support_check_complete=True,
        semilinear_support_equivalent=True,
        checked_semilinear_maps=0,
        status=(
            "equivalent-control-scalable-invariants-preserved"
            if verified
            else "control-failure-scalable-signature-not-invariant"
        ),
        interpretation=(
            "Known coordinate permutation preserves every exact scalable signature."
            if verified
            else "A purported invariant failed on a known permutation control; reject the signature pipeline."
        ),
    )


def audit_unrelated_pair(
    spec: ScalableGoppaSpec,
    left: ScalableGoppaInstance,
    right: ScalableGoppaInstance,
) -> ScalableGoppaPairAudit:
    coarse_match = left.signature.coarse_signature == right.signature.coarse_signature
    exact_available = (
        left.signature.exact_signature_digest is not None
        and right.signature.exact_signature_digest is not None
    )
    exact_match = (
        left.signature.exact_signature_digest == right.signature.exact_signature_digest
        if exact_available
        else None
    )
    semilinear = None
    checked = 0
    complete = False
    if coarse_match and (exact_match is True or not exact_available):
        semilinear, checked, complete = semilinear_support_equivalence(
            GF2m(spec.field_degree), left.support, right.support
        )
    if not coarse_match or exact_match is False:
        status = "rejected-by-scalable-goppa-invariant"
        interpretation = (
            "Polynomial Schur/hull data or exact dual weight-incidence signatures separate the pair."
        )
    elif semilinear is True:
        status = "semilinear-support-control-needs-code-map"
        interpretation = (
            "The supports are affine-semilinearly equivalent; this row is a control candidate until the polynomial/code map is checked."
        )
    elif not exact_available:
        status = "goppa-scaling-baseline-cap-proof-debt"
        interpretation = (
            "Coarse scalable invariants match, but dual dimension exceeds the exact enumeration cap. This is baseline "
            "debt, not nonabelian hardness evidence."
        )
    elif not complete:
        status = "goppa-scaling-semilinear-cap-proof-debt"
        interpretation = (
            "Exact signatures match but the semilinear support search hit its cap; resolve the classical orbit before promotion."
        )
    else:
        status = "goppa-scaling-collision-proof-debt"
        interpretation = (
            "The pair survives exact dual weight/incidence, Schur/hull, and complete semilinear-support checks. It "
            "requires stronger support recovery and canonicalization; it is not quantum evidence."
        )
    return ScalableGoppaPairAudit(
        id=f"{spec.id}-{left.id.rsplit('-', 1)[-1]}-{right.id.rsplit('-', 1)[-1]}",
        left_id=left.id,
        right_id=right.id,
        known_equivalent=False,
        coarse_invariants_match=coarse_match,
        exact_signatures_available=exact_available,
        exact_signatures_match=exact_match,
        semilinear_support_check_complete=complete,
        semilinear_support_equivalent=semilinear,
        checked_semilinear_maps=checked,
        status=status,
        interpretation=interpretation,
    )


def audit_scalable_family(spec: ScalableGoppaSpec) -> ScalableGoppaFamilyRecord:
    instances = generate_scalable_instances(spec)
    control = audit_known_permutation_control(spec, instances[0])
    pair_candidates = list(itertools.combinations(instances, 2))
    pair_candidates.sort(
        key=lambda pair: (
            pair[0].signature.coarse_signature != pair[1].signature.coarse_signature,
            pair[0].id,
            pair[1].id,
        )
    )
    audits = [
        audit_unrelated_pair(spec, left, right)
        for left, right in pair_candidates[: spec.max_collision_pairs]
    ]
    exact_rejections = sum(audit.status == "rejected-by-scalable-goppa-invariant" for audit in audits)
    semilinear_controls = sum(audit.status == "semilinear-support-control-needs-code-map" for audit in audits)
    proof_debt = sum(audit.status == "goppa-scaling-collision-proof-debt" for audit in audits)
    baseline_caps = sum("cap-proof-debt" in audit.status for audit in audits)
    coarse_collisions = sum(audit.coarse_invariants_match for audit in audits)
    if control.status.startswith("control-failure"):
        status = "rejected-signature-pipeline-control-failure"
        interpretation = control.interpretation
    elif proof_debt:
        status = "goppa-scaling-collision-proof-debt"
        interpretation = f"{proof_debt} unrelated pair(s) survive every completed scalable classical invariant."
    elif baseline_caps:
        status = "goppa-scaling-baseline-cap-proof-debt"
        interpretation = f"{baseline_caps} pair(s) are unresolved only because exact dual/semilinear baselines hit caps."
    elif coarse_collisions:
        status = "goppa-scaling-collisions-classically-resolved"
        interpretation = f"All {coarse_collisions} coarse collision(s) are separated or controlled by stronger classical checks."
    else:
        status = "no-scalable-goppa-coarse-collision"
        interpretation = "The generated natural family produced no pair matching even the coarse scalable invariants."
    return ScalableGoppaFamilyRecord(
        spec=spec,
        instances=instances,
        control_audits=[control],
        collision_audits=audits,
        exact_dual_signature_count=sum(instance.signature.exact_signature_digest is not None for instance in instances),
        coarse_collision_pair_count=coarse_collisions,
        exact_invariant_rejection_count=exact_rejections,
        semilinear_support_control_count=semilinear_controls,
        proof_debt_pair_count=proof_debt,
        baseline_cap_pair_count=baseline_caps,
        status=status,
        interpretation=interpretation,
    )


def run_goppa_scaling_frontier(
    specs: Sequence[ScalableGoppaSpec] = DEFAULT_SPECS,
) -> GoppaScalingFrontierReport:
    records = [audit_scalable_family(spec) for spec in specs]
    metrics: dict[str, int | float] = {
        "family_count": len(records),
        "maximum_length": max(record.spec.support_length for record in records),
        "instance_count": sum(len(record.instances) for record in records),
        "known_permutation_control_count": sum(len(record.control_audits) for record in records),
        "control_failure_count": sum(
            audit.status.startswith("control-failure")
            for record in records
            for audit in record.control_audits
        ),
        "exact_dual_signature_count": sum(record.exact_dual_signature_count for record in records),
        "coarse_collision_pair_count": sum(record.coarse_collision_pair_count for record in records),
        "exact_invariant_rejection_count": sum(record.exact_invariant_rejection_count for record in records),
        "semilinear_support_control_count": sum(record.semilinear_support_control_count for record in records),
        "proof_debt_pair_count": sum(record.proof_debt_pair_count for record in records),
        "baseline_cap_pair_count": sum(record.baseline_cap_pair_count for record in records),
        "natural_scaling_family_count": len(records),
        "nonabelian_measurement_required_pair_count": 0,
        "classical_superpolynomial_lower_bound_count": 0,
    }
    return GoppaScalingFrontierReport(
        created_at=utc_now(),
        records=records,
        headline_metrics=metrics,
        claim_gate={
            "known_permutation_controls_pass": metrics["control_failure_count"] == 0,
            "proof_debt_is_quantum_evidence": False,
            "baseline_caps_are_hardness_evidence": False,
            "natural_scaling_family_generated": True,
            "nonabelian_measurement_necessity_proved": False,
            "classical_superpolynomial_lower_bound_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The search now reaches natural punctured Goppa/alternant lengths through 160 with scalable exact "
                "dual signatures where feasible. Surviving rows and cap rows remain classical proof debt; no "
                "nonabelian measurement necessity or classical lower bound is proved."
            ),
        },
        status="natural-goppa-scaling-frontier-generated-classical-proof-debt-only",
        summary=(
            f"Generated {metrics['instance_count']} punctured Goppa/alternant codes through length "
            f"{metrics['maximum_length']}; exact rejections/proof-debt/cap pairs="
            f"{metrics['exact_invariant_rejection_count']}/{metrics['proof_debt_pair_count']}/"
            f"{metrics['baseline_cap_pair_count']}."
        ),
        falsifiers_triggered=[
            "Length-8/16 semilinear controls are not retained as the Goppa frontier.",
            "Known coordinate permutations must preserve every exact signature.",
            "Exact dual weight/incidence mismatches are classical separations.",
            "Sampled or cap-limited dual data is never used as an exact rejection or hardness claim.",
            "A surviving invariant collision is proof debt until support recovery and canonicalization are exhausted.",
            "No finite collision is promoted to a nonabelian measurement necessity or speedup."
        ],
    )


def write_goppa_scaling_frontier(
    path: Path = GOPPA_SCALING_FRONTIER_PATH,
    specs: Sequence[ScalableGoppaSpec] = DEFAULT_SPECS,
    write_registry: bool = True,
    registry_experiment_id: str = DEFAULT_EXPERIMENT_ID,
    registry_candidate_id: str = DEFAULT_CANDIDATE_ID,
    registry_result_id: str | None = None,
) -> dict:
    payload = asdict(run_goppa_scaling_frontier(specs))
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    if write_registry:
        for record in payload["records"]:
            for audit in record["collision_audits"]:
                if audit["status"] != "rejected-by-scalable-goppa-invariant":
                    continue
                upsert_negative_result(
                    NegativeResultRecord(
                        id=f"NEG-CODE-GOPPA-SCALING-{audit['id'].upper()}",
                        source=str(path),
                        claim=f"{audit['id']} supplies a hard code-equivalence row beyond scalable classical invariants.",
                        reason_invalid=audit["interpretation"],
                        lesson=(
                            "Run exact dual weight/incidence, Schur/hull, semilinear support, support recovery, and "
                            "canonicalization before using a Goppa row in nonabelian measurement design."
                        ),
                        applies_to=[registry_candidate_id, registry_experiment_id],
                        evidence=audit,
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
                artifacts={"goppa_scaling_frontier": str(path)},
            )
        )
    return payload


if __name__ == "__main__":
    report = write_goppa_scaling_frontier()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))

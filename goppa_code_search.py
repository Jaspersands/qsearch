"""Binary Goppa/alternant-family search for code-equivalence frontiers.

Small random code collisions are weak evidence for nonabelian HSP progress.
Binary Goppa and alternant-style codes are at least a natural algebraic source
connected to real code-equivalence hardness discussions.  This module generates
small binary Goppa codes over GF(2^m), searches for coordinate tuple-profile
collisions, and immediately tries to kill every signal with structural
invariants, semilinear field automorphisms, and profile-pruned canonicalization.
"""

from __future__ import annotations

import itertools
import json
from dataclasses import asdict, dataclass, is_dataclass
from pathlib import Path
from typing import Any

import numpy as np

from code_canonicalization_baseline import audit_code_canonicalization_pair
from code_equivalence_workbench import codeword_int_set, gf2_rank, permute_codeword_set
from code_family_search import gf2_nullspace_basis, strong_invariant_differences
from code_tuple_profile_baseline import audit_code_tuple_profile_pair, tuple_profile_key
from research_registry import ExperimentResultRecord, NegativeResultRecord, upsert_experiment_result, upsert_negative_result, utc_now


CODE_EQUIVALENCE_DIR = Path("research/code_equivalence")
GOPPA_CODE_SEARCH_PATH = CODE_EQUIVALENCE_DIR / "goppa_code_search.json"

IRREDUCIBLE_POLYS = {
    2: 0b111,
    3: 0b1011,
    4: 0b10011,
    5: 0b100101,
    6: 0b1000011,
    7: 0b10000011,
    8: 0b100011101,
}


@dataclass(frozen=True)
class GoppaSearchSpec:
    id: str
    field_degree: int
    goppa_degree: int
    max_polynomials: int
    tuple_size: int
    max_collisions: int
    min_dimension: int = 2
    max_dimension: int = 12
    seed: int = 0


@dataclass(frozen=True)
class GoppaCodeDescriptor:
    coefficients: tuple[int, ...]
    length: int
    dimension: int
    parity_rank: int
    generator: list[list[int]]


@dataclass(frozen=True)
class SemilinearWitness:
    evaluated: bool
    equivalent: bool | None
    checked_permutations: int
    frobenius_power: int | None
    scale: int | None
    translate: int | None
    interpretation: str


@dataclass(frozen=True)
class GoppaCollisionAudit:
    id: str
    generator_poly_a: str
    generator_poly_b: str
    length: int
    dimension_a: int
    dimension_b: int
    structural_distinguishing_invariants: list[str]
    tuple_profile_status: str
    semilinear_witness: SemilinearWitness
    canonical_status: str
    canonical_equal: bool | None
    estimated_assignments: int
    status: str
    interpretation: str
    generator_a: list[list[int]]
    generator_b: list[list[int]]


@dataclass(frozen=True)
class GoppaSearchRecord:
    spec: GoppaSearchSpec
    code_count: int
    tuple_profile_key_count: int
    tuple_collision_count: int
    semilinear_control_count: int
    structural_rejection_count: int
    tuple_profile_rejection_count: int
    canonicalization_rejection_count: int
    proof_debt_collision_count: int
    max_profile_bucket_size: int
    control_audits: list[GoppaCollisionAudit]
    collision_audits: list[GoppaCollisionAudit]
    status: str
    interpretation: str


@dataclass(frozen=True)
class GoppaCodeSearchReport:
    created_at: str
    records: list[GoppaSearchRecord]
    headline_metrics: dict[str, int]
    status: str
    summary: str
    falsifiers_triggered: list[str]


DEFAULT_GOPPA_SPECS = [
    GoppaSearchSpec("goppa-m3-t2", field_degree=3, goppa_degree=2, max_polynomials=48, tuple_size=2, max_collisions=4, seed=301),
    GoppaSearchSpec("goppa-m4-t2", field_degree=4, goppa_degree=2, max_polynomials=96, tuple_size=2, max_collisions=4, seed=401),
    GoppaSearchSpec("goppa-m4-t3", field_degree=4, goppa_degree=3, max_polynomials=128, tuple_size=2, max_collisions=4, seed=402),
]


class GF2m:
    def __init__(self, degree: int, modulus: int | None = None) -> None:
        if degree not in IRREDUCIBLE_POLYS and modulus is None:
            raise ValueError(f"no irreducible polynomial configured for GF(2^{degree})")
        self.degree = degree
        self.modulus = int(modulus if modulus is not None else IRREDUCIBLE_POLYS[degree])
        self.size = 1 << degree
        self.mask = self.size - 1

    def add(self, left: int, right: int) -> int:
        return int(left) ^ int(right)

    def mul(self, left: int, right: int) -> int:
        a = int(left)
        b = int(right)
        value = 0
        while b:
            if b & 1:
                value ^= a
            b >>= 1
            a <<= 1
            if a & self.size:
                a ^= self.modulus
        return value & self.mask

    def pow(self, value: int, exponent: int) -> int:
        result = 1
        base = int(value)
        exp = int(exponent)
        while exp:
            if exp & 1:
                result = self.mul(result, base)
            base = self.mul(base, base)
            exp >>= 1
        return result

    def inv(self, value: int) -> int:
        if int(value) == 0:
            raise ZeroDivisionError("zero has no inverse")
        return self.pow(int(value), self.size - 2)

    def div(self, left: int, right: int) -> int:
        return self.mul(left, self.inv(right))

    def bits(self, value: int) -> list[int]:
        return [(int(value) >> bit) & 1 for bit in range(self.degree)]


def evaluate_monic_polynomial(field: GF2m, coefficients: tuple[int, ...], point: int) -> int:
    degree = len(coefficients)
    value = field.pow(point, degree)
    power = 1
    for coefficient in coefficients:
        if coefficient:
            value = field.add(value, field.mul(coefficient, power))
        power = field.mul(power, point)
    return value


def coefficient_label(coefficients: tuple[int, ...]) -> str:
    return "x^%d+" % len(coefficients) + "+".join(f"{coef}x^{index}" for index, coef in enumerate(coefficients) if coef)


def rootless_on_full_support(field: GF2m, coefficients: tuple[int, ...]) -> bool:
    return all(evaluate_monic_polynomial(field, coefficients, point) != 0 for point in range(field.size))


def goppa_parity_check(field: GF2m, coefficients: tuple[int, ...]) -> np.ndarray:
    degree = len(coefficients)
    support = list(range(field.size))
    parity = np.zeros((degree * field.degree, len(support)), dtype=np.uint8)
    for column, point in enumerate(support):
        denominator = evaluate_monic_polynomial(field, coefficients, point)
        if denominator == 0:
            raise ValueError("Goppa support contains a polynomial root")
        inverse = field.inv(denominator)
        power = 1
        for row_block in range(degree):
            value = field.mul(power, inverse)
            for bit, bit_value in enumerate(field.bits(value)):
                parity[row_block * field.degree + bit, column] = bit_value
            power = field.mul(power, point)
    return parity


def goppa_generator(field: GF2m, coefficients: tuple[int, ...]) -> np.ndarray:
    parity = goppa_parity_check(field, coefficients)
    return gf2_nullspace_basis(parity)


def _permutation_from_old_to_new(generator: np.ndarray, old_to_new: list[int]) -> np.ndarray:
    inverse = [0] * len(old_to_new)
    for old_index, new_index in enumerate(old_to_new):
        inverse[int(new_index)] = old_index
    return np.asarray(generator, dtype=np.uint8)[:, inverse]


def enumerate_goppa_descriptors(spec: GoppaSearchSpec) -> list[GoppaCodeDescriptor]:
    field = GF2m(spec.field_degree)
    all_coefficients = list(itertools.product(range(field.size), repeat=spec.goppa_degree))
    rng = np.random.default_rng(spec.seed)
    order = rng.permutation(len(all_coefficients)).tolist()
    descriptors: list[GoppaCodeDescriptor] = []
    for index in order:
        coefficients = tuple(int(value) for value in all_coefficients[index])
        if not rootless_on_full_support(field, coefficients):
            continue
        generator = goppa_generator(field, coefficients)
        dimension = int(generator.shape[0])
        if dimension < spec.min_dimension or dimension > spec.max_dimension:
            continue
        descriptors.append(
            GoppaCodeDescriptor(
                coefficients=coefficients,
                length=int(generator.shape[1]),
                dimension=dimension,
                parity_rank=field.size - dimension,
                generator=[[int(bit) for bit in row] for row in generator.tolist()],
            )
        )
        if len(descriptors) >= spec.max_polynomials:
            break
    return descriptors


def semilinear_equivalence_witness(field: GF2m, left: np.ndarray, right: np.ndarray) -> SemilinearWitness:
    if left.shape[1] != field.size or right.shape[1] != field.size:
        return SemilinearWitness(
            evaluated=False,
            equivalent=None,
            checked_permutations=0,
            frobenius_power=None,
            scale=None,
            translate=None,
            interpretation="Skipped semilinear test because the support is not the full field.",
        )
    left_words = codeword_int_set(left)
    right_words = codeword_int_set(right)
    checked = 0
    frobenius_tables = [
        [field.pow(point, 1 << power) for point in range(field.size)]
        for power in range(field.degree)
    ]
    for power, table in enumerate(frobenius_tables):
        for scale in range(1, field.size):
            for translate in range(field.size):
                permutation = [field.add(field.mul(scale, table[point]), translate) for point in range(field.size)]
                checked += 1
                if permute_codeword_set(left_words, field.size, permutation) == right_words:
                    return SemilinearWitness(
                        evaluated=True,
                        equivalent=True,
                        checked_permutations=checked,
                        frobenius_power=power,
                        scale=scale,
                        translate=translate,
                        interpretation=(
                            "The code pair is equivalent under a full-support affine semilinear field permutation; "
                            "this is an algebraic control, not hardness evidence."
                        ),
                    )
    return SemilinearWitness(
        evaluated=True,
        equivalent=False,
        checked_permutations=checked,
        frobenius_power=None,
        scale=None,
        translate=None,
        interpretation="No full-support affine semilinear field permutation maps the first code to the second.",
    )


def audit_goppa_pair(
    spec: GoppaSearchSpec,
    left_descriptor: GoppaCodeDescriptor,
    right_descriptor: GoppaCodeDescriptor,
    pair_id: str,
    tuple_cap: int,
    canonical_max_assignments: int,
) -> GoppaCollisionAudit:
    field = GF2m(spec.field_degree)
    left = np.asarray(left_descriptor.generator, dtype=np.uint8)
    right = np.asarray(right_descriptor.generator, dtype=np.uint8)
    structural = strong_invariant_differences(left, right)
    tuple_audit = audit_code_tuple_profile_pair(
        record_id=f"{pair_id}-tuple",
        source="goppa_code_search",
        left=left,
        right=right,
        known_equivalent=None,
        max_tuple_size=min(3, spec.tuple_size + 1),
        tuple_cap=tuple_cap,
    )
    semilinear = semilinear_equivalence_witness(field, left, right)

    canonical_status = "not-run-after-structural-tuple-or-semilinear-decision"
    canonical_equal: bool | None = None
    estimated = 0
    if not structural and tuple_audit.status != "rejected-by-coordinate-tuple-profile" and semilinear.equivalent is not True:
        canonical = audit_code_canonicalization_pair(
            record_id=f"{pair_id}-canonical",
            source="goppa_code_search",
            left=left,
            right=right,
            known_equivalent=None,
            max_assignments=canonical_max_assignments,
        )
        canonical_status = canonical.status
        canonical_equal = canonical.canonical_equal
        estimated = max(
            int(canonical.left_canonical.estimated_assignments),
            int(canonical.right_canonical.estimated_assignments),
        )

    if structural:
        status = "rejected-by-structural-code-invariant"
        interpretation = "Goppa-code pair is separated by structural classical invariants: " + ", ".join(structural)
    elif tuple_audit.status == "rejected-by-coordinate-tuple-profile":
        status = "rejected-by-coordinate-tuple-profile"
        interpretation = tuple_audit.interpretation
    elif semilinear.equivalent is True:
        status = "equivalent-control-under-semilinear-field-automorphism"
        interpretation = semilinear.interpretation
    elif canonical_status in {"rejected-by-coordinate-profile-partition", "rejected-by-exact-profile-canonical-form"}:
        status = canonical_status
        interpretation = "Profile-pruned canonicalization rejects this Goppa tuple-profile collision."
    elif canonical_status.startswith("canonical-equivalent"):
        status = "canonical-equivalent-control"
        interpretation = "Profile-pruned canonicalization identifies this row as an equivalent control."
    else:
        status = "goppa-collision-proof-debt"
        interpretation = (
            "This Goppa row survived implemented structural, tuple-profile, semilinear, and configured "
            "canonicalization checks; it is proof debt only."
        )

    return GoppaCollisionAudit(
        id=pair_id,
        generator_poly_a=coefficient_label(left_descriptor.coefficients),
        generator_poly_b=coefficient_label(right_descriptor.coefficients),
        length=left_descriptor.length,
        dimension_a=left_descriptor.dimension,
        dimension_b=right_descriptor.dimension,
        structural_distinguishing_invariants=structural,
        tuple_profile_status=tuple_audit.status,
        semilinear_witness=semilinear,
        canonical_status=canonical_status,
        canonical_equal=canonical_equal,
        estimated_assignments=estimated,
        status=status,
        interpretation=interpretation,
        generator_a=left_descriptor.generator,
        generator_b=right_descriptor.generator,
    )


def _semilinear_control_descriptor(spec: GoppaSearchSpec, descriptor: GoppaCodeDescriptor) -> GoppaCodeDescriptor:
    field = GF2m(spec.field_degree)
    generator = np.asarray(descriptor.generator, dtype=np.uint8)
    if field.size <= 1:
        old_to_new = list(range(field.size))
    else:
        old_to_new = [field.add(point, 1) for point in range(field.size)]
    permuted = _permutation_from_old_to_new(generator, old_to_new)
    return GoppaCodeDescriptor(
        coefficients=descriptor.coefficients,
        length=descriptor.length,
        dimension=descriptor.dimension,
        parity_rank=descriptor.parity_rank,
        generator=[[int(bit) for bit in row] for row in permuted.tolist()],
    )


def run_goppa_search_spec(
    spec: GoppaSearchSpec,
    tuple_cap: int = 50_000,
    canonical_max_assignments: int = 200_000,
) -> GoppaSearchRecord:
    descriptors = enumerate_goppa_descriptors(spec)
    seen: dict[str, list[GoppaCodeDescriptor]] = {}
    collisions: list[GoppaCollisionAudit] = []
    controls: list[GoppaCollisionAudit] = []
    max_bucket = 0

    if descriptors:
        control_descriptor = _semilinear_control_descriptor(spec, descriptors[0])
        controls.append(
            audit_goppa_pair(
                spec,
                descriptors[0],
                control_descriptor,
                f"{spec.id}-semilinear-control",
                tuple_cap=tuple_cap,
                canonical_max_assignments=canonical_max_assignments,
            )
        )

    for descriptor in descriptors:
        generator = np.asarray(descriptor.generator, dtype=np.uint8)
        key = tuple_profile_key(generator, tuple_size=spec.tuple_size, tuple_cap=tuple_cap)
        if key == "skipped":
            break
        bucket = seen.setdefault(key, [])
        max_bucket = max(max_bucket, len(bucket) + 1)
        for prior_index, previous in enumerate(bucket):
            if previous.dimension != descriptor.dimension:
                continue
            if codeword_int_set(np.asarray(previous.generator, dtype=np.uint8)) == codeword_int_set(generator):
                continue
            audit = audit_goppa_pair(
                spec,
                previous,
                descriptor,
                f"{spec.id}-collision-{len(collisions) + 1}-prior-{prior_index}",
                tuple_cap=tuple_cap,
                canonical_max_assignments=canonical_max_assignments,
            )
            collisions.append(audit)
            if len(collisions) >= spec.max_collisions:
                break
        if len(collisions) >= spec.max_collisions:
            break
        if len(bucket) < 4:
            bucket.append(descriptor)

    structural_rejections = sum(1 for audit in collisions if audit.status == "rejected-by-structural-code-invariant")
    tuple_rejections = sum(1 for audit in collisions if audit.status == "rejected-by-coordinate-tuple-profile")
    canonical_rejections = sum(1 for audit in collisions if audit.status.startswith("rejected-by") and audit.status not in {"rejected-by-structural-code-invariant", "rejected-by-coordinate-tuple-profile"})
    semilinear_controls = sum(1 for audit in collisions + controls if "control" in audit.status)
    proof_debt = sum(1 for audit in collisions if audit.status == "goppa-collision-proof-debt")

    if proof_debt:
        status = "goppa-tuple-collision-proof-debt"
        interpretation = "At least one Goppa tuple-profile collision survived implemented baselines as proof debt."
    elif structural_rejections or tuple_rejections or canonical_rejections:
        status = "goppa-collisions-rejected-by-classical-baselines"
        interpretation = "Goppa tuple-profile collisions were rejected by structural, tuple-profile, or canonicalization baselines."
    elif collisions and semilinear_controls >= len(collisions):
        status = "goppa-collisions-all-semilinear-controls"
        interpretation = "Goppa tuple-profile collisions found so far are semilinear/equivalent controls."
    else:
        status = "no-goppa-tuple-profile-collision-found"
        interpretation = "No nontrivial Goppa tuple-profile collision was found under this deterministic search budget."

    return GoppaSearchRecord(
        spec=spec,
        code_count=len(descriptors),
        tuple_profile_key_count=len(seen),
        tuple_collision_count=len(collisions),
        semilinear_control_count=semilinear_controls,
        structural_rejection_count=structural_rejections,
        tuple_profile_rejection_count=tuple_rejections,
        canonicalization_rejection_count=canonical_rejections,
        proof_debt_collision_count=proof_debt,
        max_profile_bucket_size=max_bucket,
        control_audits=controls,
        collision_audits=collisions,
        status=status,
        interpretation=interpretation,
    )


def run_goppa_code_search(
    specs: list[GoppaSearchSpec] | None = None,
    tuple_cap: int = 50_000,
    canonical_max_assignments: int = 200_000,
) -> GoppaCodeSearchReport:
    active_specs = specs or DEFAULT_GOPPA_SPECS
    records = [
        run_goppa_search_spec(spec, tuple_cap=tuple_cap, canonical_max_assignments=canonical_max_assignments)
        for spec in active_specs
    ]
    metrics = {
        "search_count": len(records),
        "code_count": sum(record.code_count for record in records),
        "tuple_profile_key_count": sum(record.tuple_profile_key_count for record in records),
        "tuple_collision_count": sum(record.tuple_collision_count for record in records),
        "semilinear_control_count": sum(record.semilinear_control_count for record in records),
        "structural_rejection_count": sum(record.structural_rejection_count for record in records),
        "tuple_profile_rejection_count": sum(record.tuple_profile_rejection_count for record in records),
        "canonicalization_rejection_count": sum(record.canonicalization_rejection_count for record in records),
        "proof_debt_collision_count": sum(record.proof_debt_collision_count for record in records),
        "no_collision_count": sum(1 for record in records if record.status == "no-goppa-tuple-profile-collision-found"),
    }
    if metrics["proof_debt_collision_count"]:
        status = "goppa-code-search-proof-debt"
    elif metrics["tuple_collision_count"] and (
        metrics["structural_rejection_count"]
        or metrics["tuple_profile_rejection_count"]
        or metrics["canonicalization_rejection_count"]
        or metrics["semilinear_control_count"]
    ):
        status = "goppa-code-search-dequantized-or-controls"
    else:
        status = "goppa-code-search-no-hard-row"

    summary = (
        f"Searched {metrics['search_count']} Goppa/alternant parameter window(s), enumerating "
        f"{metrics['code_count']} code(s). Found {metrics['tuple_collision_count']} tuple-profile collision(s): "
        f"{metrics['semilinear_control_count']} semilinear/equivalent control(s), "
        f"{metrics['structural_rejection_count'] + metrics['tuple_profile_rejection_count'] + metrics['canonicalization_rejection_count']} "
        f"classical rejection(s), and {metrics['proof_debt_collision_count']} proof-debt row(s)."
    )
    falsifiers = []
    if metrics["semilinear_control_count"]:
        falsifiers.append("Semilinear field automorphisms explain some Goppa rows as controls.")
    if metrics["structural_rejection_count"] or metrics["tuple_profile_rejection_count"] or metrics["canonicalization_rejection_count"]:
        falsifiers.append("Classical code baselines reject some Goppa tuple-profile collisions.")
    if metrics["no_collision_count"]:
        falsifiers.append("Some Goppa search windows found no tuple-profile collision under the configured budget.")
    if metrics["proof_debt_collision_count"]:
        falsifiers.append("Some Goppa rows remain proof debt rather than positive evidence.")
    return GoppaCodeSearchReport(utc_now(), records, metrics, status, summary, falsifiers)


def _json_ready(value: Any) -> Any:
    if is_dataclass(value):
        return _json_ready(asdict(value))
    if isinstance(value, dict):
        return {str(key): _json_ready(item) for key, item in value.items()}
    if isinstance(value, list):
        return [_json_ready(item) for item in value]
    if isinstance(value, tuple):
        return _json_ready(list(value))
    if isinstance(value, np.integer):
        return int(value)
    if isinstance(value, np.bool_):
        return bool(value)
    return value


def _safe_id(value: str) -> str:
    return "".join(ch if ch.isalnum() else "_" for ch in value.upper()).strip("_")


def write_goppa_negative_results(report: GoppaCodeSearchReport) -> int:
    written = 0
    for record in report.records:
        if record.status == "goppa-tuple-collision-proof-debt":
            continue
        upsert_negative_result(
            NegativeResultRecord(
                id=f"GOPPA-CODE-SEARCH-{_safe_id(record.spec.id)}",
                source="goppa_code_search.py",
                claim=f"{record.spec.id} supplies hard code-equivalence coset evidence.",
                reason_invalid=record.interpretation,
                lesson=(
                    "Natural algebraic code families still need to survive structural invariants, tuple profiles, "
                    "semilinear automorphism controls, and canonicalization before motivating nonabelian coset measurements."
                ),
                applies_to=["CODE-COSET-COLLECTIVE", "PO-DEQUANTIZATION", "PO-FALSIFIERS"],
                evidence={
                    "status": record.status,
                    "code_count": record.code_count,
                    "tuple_collision_count": record.tuple_collision_count,
                    "semilinear_control_count": record.semilinear_control_count,
                    "proof_debt_collision_count": record.proof_debt_collision_count,
                },
            )
        )
        written += 1
    return written


def write_goppa_code_search(
    output_path: Path = GOPPA_CODE_SEARCH_PATH,
    specs: list[GoppaSearchSpec] | None = None,
    tuple_cap: int = 50_000,
    canonical_max_assignments: int = 200_000,
    write_registry: bool = True,
    registry_experiment_id: str = "EXP-CODE-GOPPA-ALGEBRAIC-SEARCH",
    registry_candidate_id: str = "CODE-COSET-COLLECTIVE",
    registry_result_id: str = "RESULT-EXP-CODE-GOPPA-ALGEBRAIC-SEARCH-GOPPA-CODE",
) -> dict[str, Any]:
    report = run_goppa_code_search(specs=specs, tuple_cap=tuple_cap, canonical_max_assignments=canonical_max_assignments)
    payload = _json_ready(report)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    negative_results_written = 0
    if write_registry:
        negative_results_written = write_goppa_negative_results(report)
        upsert_experiment_result(
            ExperimentResultRecord(
                id=registry_result_id,
                experiment_id=registry_experiment_id,
                candidate_id=registry_candidate_id,
                created_at=report.created_at,
                status=report.status,
                summary=report.summary,
                metrics=payload["headline_metrics"],
                falsifiers_triggered=report.falsifiers_triggered,
                artifacts={"goppa_code_search": str(output_path)},
            )
        )
    payload["negative_results_written"] = negative_results_written
    return payload

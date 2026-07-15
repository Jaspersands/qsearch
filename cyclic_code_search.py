"""Algebraic cyclic-code family search for code-equivalence frontiers.

Random weak-invariant collisions and quasi-cyclic controls are not enough.  A
credible code-equivalence frontier should also test honest algebraic families.
This module enumerates binary cyclic codes from divisors of ``x^n - 1`` over
``F_2``, searches for weak/tuple-profile collisions, and immediately attacks
them with structural invariants, higher tuple profiles, the natural cyclic
dihedral automorphism group, and profile-pruned canonicalization.

Survivors are proof debt.  Collisions explained by reciprocal generator
polynomials or dihedral coordinate symmetries are controls, not evidence.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, is_dataclass
from itertools import combinations
from math import gcd
from pathlib import Path
from typing import Any

import numpy as np

from code_canonicalization_baseline import audit_code_canonicalization_pair
from code_equivalence_workbench import codeword_int_set, gf2_rank, permute_codeword_set
from code_family_search import strong_invariant_differences, weak_invariant_key
from code_tuple_profile_baseline import audit_code_tuple_profile_pair, tuple_profile_key
from research_registry import ExperimentResultRecord, NegativeResultRecord, upsert_experiment_result, upsert_negative_result, utc_now


CODE_EQUIVALENCE_DIR = Path("research/code_equivalence")
CYCLIC_CODE_SEARCH_PATH = CODE_EQUIVALENCE_DIR / "cyclic_code_search.json"


@dataclass(frozen=True)
class CyclicCodeSearchSpec:
    id: str
    length: int
    min_dimension: int
    max_dimension: int
    tuple_size: int
    max_collisions: int


@dataclass(frozen=True)
class DihedralEquivalenceResult:
    evaluated: bool
    equivalent: bool
    reflection: bool | None
    shift: int | None
    interpretation: str


@dataclass(frozen=True)
class MultiplierAffineEquivalenceResult:
    evaluated: bool
    equivalent: bool
    multiplier: int | None
    shift: int | None
    maps_checked: int
    interpretation: str


@dataclass(frozen=True)
class CyclicCollisionAudit:
    id: str
    length: int
    dimension: int
    generator_poly_a: str
    generator_poly_b: str
    tuple_profile_bucket_size: int
    strong_distinguishing_invariants: list[str]
    tuple_profile_status: str
    dihedral_equivalence: DihedralEquivalenceResult
    multiplier_affine_equivalence: MultiplierAffineEquivalenceResult
    canonical_status: str
    canonical_equal: bool | None
    status: str
    interpretation: str
    generator_a: list[list[int]]
    generator_b: list[list[int]]


@dataclass(frozen=True)
class CyclicCodeSearchRecord:
    spec: CyclicCodeSearchSpec
    divisor_count: int
    code_count: int
    profile_key_count: int
    tuple_collision_count: int
    structural_rejection_count: int
    tuple_profile_rejection_count: int
    dihedral_equivalent_count: int
    multiplier_equivalent_count: int
    canonicalization_rejection_count: int
    proof_debt_collision_count: int
    collision_audits: list[CyclicCollisionAudit]
    status: str
    interpretation: str


@dataclass(frozen=True)
class CyclicCodeSearchReport:
    created_at: str
    records: list[CyclicCodeSearchRecord]
    headline_metrics: dict[str, int]
    status: str
    summary: str
    falsifiers_triggered: list[str]


DEFAULT_CYCLIC_SPECS = [
    CyclicCodeSearchSpec("cyclic-n7", length=7, min_dimension=2, max_dimension=6, tuple_size=2, max_collisions=6),
    CyclicCodeSearchSpec("cyclic-n15", length=15, min_dimension=3, max_dimension=10, tuple_size=2, max_collisions=8),
    CyclicCodeSearchSpec("cyclic-n21", length=21, min_dimension=4, max_dimension=10, tuple_size=2, max_collisions=8),
]


def poly_degree(poly: int) -> int:
    return int(poly.bit_length() - 1)


def poly_mul(left: int, right: int) -> int:
    result = 0
    a = int(left)
    b = int(right)
    while b:
        if b & 1:
            result ^= a
        a <<= 1
        b >>= 1
    return result


def poly_divmod(dividend: int, divisor: int) -> tuple[int, int]:
    if divisor == 0:
        raise ZeroDivisionError("polynomial divisor cannot be zero")
    quotient = 0
    remainder = int(dividend)
    divisor_degree = poly_degree(divisor)
    while remainder and poly_degree(remainder) >= divisor_degree:
        shift = poly_degree(remainder) - divisor_degree
        quotient ^= 1 << shift
        remainder ^= divisor << shift
    return quotient, remainder


def poly_divides(divisor: int, dividend: int) -> bool:
    return poly_divmod(dividend, divisor)[1] == 0


def factor_binary_polynomial(poly: int) -> list[int]:
    """Naively factor a small square-free binary polynomial.

    The default cyclic lengths are small enough that trial division by monic
    odd polynomials is preferable to pulling in a computer-algebra dependency.
    """

    factors: list[int] = []
    remainder = int(poly)
    degree = 1
    while poly_degree(remainder) > 0 and degree <= poly_degree(remainder) // 2:
        found = False
        for lower in range(1 << degree):
            candidate = (1 << degree) | lower
            if not (candidate & 1):
                continue
            if poly_divides(candidate, remainder):
                factors.append(candidate)
                remainder = poly_divmod(remainder, candidate)[0]
                found = True
                break
        degree = 1 if found else degree + 1
    if remainder != 1:
        factors.append(remainder)
    return factors


def divisor_polynomials_from_factors(factors: list[int]) -> list[int]:
    divisors = {1}
    for factor in factors:
        divisors |= {poly_mul(divisor, factor) for divisor in list(divisors)}
    return sorted(divisors, key=lambda value: (poly_degree(value), value))


def cyclic_generator_matrix(length: int, generator_poly: int) -> np.ndarray:
    degree = poly_degree(generator_poly)
    dimension = int(length - degree)
    if dimension <= 0:
        raise ValueError("cyclic generator polynomial must have degree below the code length")
    rows = []
    for shift in range(dimension):
        row = [0] * length
        for offset in range(degree + 1):
            if (generator_poly >> offset) & 1:
                row[shift + offset] = 1
        rows.append(row)
    generator = np.asarray(rows, dtype=np.uint8)
    if gf2_rank(generator) != dimension:
        raise ValueError("cyclic generator matrix unexpectedly lost rank")
    return generator


def enumerate_cyclic_codes(spec: CyclicCodeSearchSpec) -> list[tuple[int, np.ndarray]]:
    modulus = (1 << spec.length) | 1
    factors = factor_binary_polynomial(modulus)
    codes = []
    for generator_poly in divisor_polynomials_from_factors(factors):
        if generator_poly in {1, modulus}:
            continue
        dimension = spec.length - poly_degree(generator_poly)
        if spec.min_dimension <= dimension <= spec.max_dimension:
            codes.append((generator_poly, cyclic_generator_matrix(spec.length, generator_poly)))
    return codes


def _dihedral_permutation(length: int, reflection: bool, shift: int) -> list[int]:
    return [(((-index if reflection else index) + shift) % length) for index in range(length)]


def _multiplier_affine_permutation(length: int, multiplier: int, shift: int) -> list[int]:
    return [((multiplier * index + shift) % length) for index in range(length)]


def dihedral_equivalence(left: np.ndarray, right: np.ndarray) -> DihedralEquivalenceResult:
    length = int(left.shape[1])
    source = codeword_int_set(left)
    target = codeword_int_set(right)
    for reflection in (False, True):
        for shift in range(length):
            permutation = _dihedral_permutation(length, reflection, shift)
            if permute_codeword_set(source, length, permutation) == target:
                return DihedralEquivalenceResult(
                    evaluated=True,
                    equivalent=True,
                    reflection=reflection,
                    shift=shift,
                    interpretation=(
                        "The collision is an equivalent control under the natural cyclic dihedral coordinate group "
                        f"(reflection={reflection}, shift={shift})."
                    ),
                )
    return DihedralEquivalenceResult(
        evaluated=True,
        equivalent=False,
        reflection=None,
        shift=None,
        interpretation="No cyclic rotation or reversal maps the first cyclic code to the second.",
    )


def multiplier_affine_equivalence(left: np.ndarray, right: np.ndarray) -> MultiplierAffineEquivalenceResult:
    """Check coordinate maps i -> a*i+b over Z_n with gcd(a,n)=1.

    For cyclic/BCH-style codes these multiplier automorphisms are the natural
    finite-field/cyclotomic control group.  Dihedral checks only cover
    a in {1,-1}; length-31 primitive cyclic rows can look like proof debt if
    this larger classical symmetry is not tested.
    """

    length = int(left.shape[1])
    source = codeword_int_set(left)
    target = codeword_int_set(right)
    checked = 0
    for multiplier in range(length):
        if gcd(multiplier, length) != 1:
            continue
        for shift in range(length):
            checked += 1
            permutation = _multiplier_affine_permutation(length, multiplier, shift)
            if permute_codeword_set(source, length, permutation) == target:
                return MultiplierAffineEquivalenceResult(
                    evaluated=True,
                    equivalent=True,
                    multiplier=multiplier,
                    shift=shift,
                    maps_checked=checked,
                    interpretation=(
                        "The collision is an equivalent control under the cyclic multiplier-affine coordinate group "
                        f"(multiplier={multiplier}, shift={shift})."
                    ),
                )
    return MultiplierAffineEquivalenceResult(
        evaluated=True,
        equivalent=False,
        multiplier=None,
        shift=None,
        maps_checked=checked,
        interpretation="No multiplier-affine coordinate map over Z_n carries the first cyclic code to the second.",
    )


def _poly_label(poly: int) -> str:
    return f"0b{poly:b}"


def audit_cyclic_collision(
    spec: CyclicCodeSearchSpec,
    generator_poly_a: int,
    generator_a: np.ndarray,
    generator_poly_b: int,
    generator_b: np.ndarray,
    bucket_size: int,
    canonical_max_assignments: int = 200_000,
    tuple_cap: int = 50_000,
) -> CyclicCollisionAudit:
    record_id = f"{spec.id}-{_poly_label(generator_poly_a)}-{_poly_label(generator_poly_b)}"
    strong = strong_invariant_differences(generator_a, generator_b)
    tuple_audit = audit_code_tuple_profile_pair(
        record_id=record_id,
        source="cyclic_code_search",
        left=generator_a,
        right=generator_b,
        known_equivalent=None,
        max_tuple_size=max(3, spec.tuple_size + 1),
        tuple_cap=tuple_cap,
    )
    dihedral = dihedral_equivalence(generator_a, generator_b)
    multiplier_affine = multiplier_affine_equivalence(generator_a, generator_b)
    canonical_status = "skipped-after-earlier-baseline"
    canonical_equal: bool | None = None
    if strong:
        status = "rejected-by-structural-code-invariant"
        interpretation = "Cyclic-code collision is separated by structural invariants: " + ", ".join(strong)
    elif tuple_audit.status == "rejected-by-coordinate-tuple-profile":
        status = "rejected-by-coordinate-tuple-profile"
        interpretation = "Cyclic-code collision is separated by higher-order coordinate tuple profiles."
    elif dihedral.equivalent:
        status = "equivalent-under-cyclic-dihedral-automorphism"
        interpretation = dihedral.interpretation
    elif multiplier_affine.equivalent:
        status = "equivalent-under-cyclic-multiplier-automorphism"
        interpretation = multiplier_affine.interpretation
    else:
        canonical = audit_code_canonicalization_pair(
            record_id=record_id,
            source="cyclic_code_search",
            left=generator_a,
            right=generator_b,
            known_equivalent=None,
            max_assignments=canonical_max_assignments,
        )
        canonical_status = canonical.status
        canonical_equal = canonical.canonical_equal
        if canonical.status.startswith("canonical-equivalent"):
            status = "canonical-equivalent-control"
            interpretation = "Profile-pruned canonicalization proves this cyclic collision is an equivalent control."
        elif canonical.status == "canonicalization-proof-debt":
            status = "cyclic-canonicalization-proof-debt"
            interpretation = "Cyclic collision survives implemented invariants but canonicalization exceeded the cap."
        else:
            status = "rejected-by-canonicalization"
            interpretation = "Profile-pruned canonicalization rejects this cyclic-code collision."

    return CyclicCollisionAudit(
        id=record_id,
        length=int(generator_a.shape[1]),
        dimension=int(generator_a.shape[0]),
        generator_poly_a=_poly_label(generator_poly_a),
        generator_poly_b=_poly_label(generator_poly_b),
        tuple_profile_bucket_size=bucket_size,
        strong_distinguishing_invariants=strong,
        tuple_profile_status=tuple_audit.status,
        dihedral_equivalence=dihedral,
        multiplier_affine_equivalence=multiplier_affine,
        canonical_status=canonical_status,
        canonical_equal=canonical_equal,
        status=status,
        interpretation=interpretation,
        generator_a=[[int(bit) for bit in row] for row in generator_a.tolist()],
        generator_b=[[int(bit) for bit in row] for row in generator_b.tolist()],
    )


def run_cyclic_search_spec(
    spec: CyclicCodeSearchSpec,
    tuple_cap: int = 50_000,
    canonical_max_assignments: int = 200_000,
) -> CyclicCodeSearchRecord:
    codes = enumerate_cyclic_codes(spec)
    buckets: dict[str, list[tuple[int, np.ndarray]]] = {}
    for generator_poly, generator in codes:
        key = tuple_profile_key(generator, tuple_size=spec.tuple_size, tuple_cap=tuple_cap)
        if key == "skipped":
            key = repr(weak_invariant_key(generator))
        buckets.setdefault(key, []).append((generator_poly, generator))

    audits: list[CyclicCollisionAudit] = []
    for bucket in buckets.values():
        if len(bucket) < 2:
            continue
        for (poly_a, generator_a), (poly_b, generator_b) in combinations(bucket, 2):
            if codeword_int_set(generator_a) == codeword_int_set(generator_b):
                continue
            audits.append(
                audit_cyclic_collision(
                    spec,
                    poly_a,
                    generator_a,
                    poly_b,
                    generator_b,
                    bucket_size=len(bucket),
                    canonical_max_assignments=canonical_max_assignments,
                    tuple_cap=tuple_cap,
                )
            )
            if len(audits) >= spec.max_collisions:
                break
        if len(audits) >= spec.max_collisions:
            break

    structural = sum(1 for audit in audits if audit.status == "rejected-by-structural-code-invariant")
    tuple_rejected = sum(1 for audit in audits if audit.status == "rejected-by-coordinate-tuple-profile")
    dihedral = sum(1 for audit in audits if audit.status == "equivalent-under-cyclic-dihedral-automorphism")
    multiplier = sum(1 for audit in audits if audit.status == "equivalent-under-cyclic-multiplier-automorphism")
    canonical_rejected = sum(1 for audit in audits if audit.status == "rejected-by-canonicalization")
    proof_debt = sum(1 for audit in audits if audit.status == "cyclic-canonicalization-proof-debt")
    if proof_debt:
        status = "cyclic-code-search-proof-debt"
        interpretation = "Some cyclic-code collisions survived implemented baselines and remain canonicalization proof debt."
    elif structural or tuple_rejected or canonical_rejected:
        status = "cyclic-code-search-dequantized"
        interpretation = "Cyclic-code collisions are rejected by classical structural, tuple, or canonicalization baselines."
    elif multiplier:
        status = "cyclic-collisions-all-automorphism-controls"
        interpretation = "Cyclic-code collisions found so far are equivalent controls under multiplier-affine cyclic automorphisms."
    elif dihedral:
        status = "cyclic-collisions-all-dihedral-controls"
        interpretation = "Cyclic-code collisions found so far are equivalent controls under the natural dihedral automorphism group."
    else:
        status = "no-cyclic-code-collision-found"
        interpretation = "No nontrivial cyclic-code tuple-profile collision was found for this length and dimension window."

    return CyclicCodeSearchRecord(
        spec=spec,
        divisor_count=len(divisor_polynomials_from_factors(factor_binary_polynomial((1 << spec.length) | 1))),
        code_count=len(codes),
        profile_key_count=len(buckets),
        tuple_collision_count=len(audits),
        structural_rejection_count=structural,
        tuple_profile_rejection_count=tuple_rejected,
        dihedral_equivalent_count=dihedral,
        multiplier_equivalent_count=multiplier,
        canonicalization_rejection_count=canonical_rejected,
        proof_debt_collision_count=proof_debt,
        collision_audits=audits,
        status=status,
        interpretation=interpretation,
    )


def run_cyclic_code_search(
    specs: list[CyclicCodeSearchSpec] | None = None,
    tuple_cap: int = 50_000,
    canonical_max_assignments: int = 200_000,
) -> CyclicCodeSearchReport:
    active_specs = specs or DEFAULT_CYCLIC_SPECS
    records = [
        run_cyclic_search_spec(spec, tuple_cap=tuple_cap, canonical_max_assignments=canonical_max_assignments)
        for spec in active_specs
    ]
    metrics = {
        "search_count": len(records),
        "code_count": sum(record.code_count for record in records),
        "tuple_collision_count": sum(record.tuple_collision_count for record in records),
        "structural_rejection_count": sum(record.structural_rejection_count for record in records),
        "tuple_profile_rejection_count": sum(record.tuple_profile_rejection_count for record in records),
        "dihedral_equivalent_count": sum(record.dihedral_equivalent_count for record in records),
        "multiplier_equivalent_count": sum(record.multiplier_equivalent_count for record in records),
        "canonicalization_rejection_count": sum(record.canonicalization_rejection_count for record in records),
        "proof_debt_collision_count": sum(record.proof_debt_collision_count for record in records),
        "no_collision_count": sum(1 for record in records if record.status == "no-cyclic-code-collision-found"),
        "max_length": max((record.spec.length for record in records), default=0),
    }
    if metrics["proof_debt_collision_count"]:
        status = "cyclic-code-search-proof-debt"
    elif metrics["tuple_collision_count"]:
        status = "cyclic-code-search-dequantized-or-controls"
    else:
        status = "cyclic-code-search-incomplete"
    summary = (
        f"Searched {metrics['search_count']} cyclic-code length window(s), enumerating {metrics['code_count']} code(s). "
        f"Found {metrics['tuple_collision_count']} tuple-profile collision(s): "
        f"{metrics['dihedral_equivalent_count']} dihedral control(s), "
        f"{metrics['multiplier_equivalent_count']} multiplier-affine control(s), "
        f"{metrics['structural_rejection_count'] + metrics['tuple_profile_rejection_count'] + metrics['canonicalization_rejection_count']} "
        f"classical rejection(s), and {metrics['proof_debt_collision_count']} proof-debt row(s)."
    )
    falsifiers = []
    if metrics["dihedral_equivalent_count"]:
        falsifiers.append("Cyclic-code collisions are explained by the natural cyclic dihedral automorphism group.")
    if metrics["multiplier_equivalent_count"]:
        falsifiers.append("Cyclic-code collisions are explained by the larger multiplier-affine automorphism group.")
    if metrics["structural_rejection_count"] or metrics["tuple_profile_rejection_count"] or metrics["canonicalization_rejection_count"]:
        falsifiers.append("Some cyclic-code collisions are rejected by classical structural, tuple, or canonicalization baselines.")
    if metrics["no_collision_count"]:
        falsifiers.append("Some cyclic-code length windows contain no nontrivial tuple-profile collision under current bounds.")
    if metrics["proof_debt_collision_count"]:
        falsifiers.append("Cyclic-code proof-debt collisions require stronger canonicalization and asymptotic family evidence.")
    return CyclicCodeSearchReport(utc_now(), records, metrics, status, summary, falsifiers)


def _json_ready(value: Any) -> Any:
    if is_dataclass(value):
        return _json_ready(asdict(value))
    if isinstance(value, dict):
        return {str(key): _json_ready(item) for key, item in value.items()}
    if isinstance(value, list):
        return [_json_ready(item) for item in value]
    if isinstance(value, tuple):
        return [_json_ready(item) for item in value]
    if isinstance(value, np.integer):
        return int(value)
    if isinstance(value, np.bool_):
        return bool(value)
    return value


def _safe_id(value: str) -> str:
    return "".join(ch if ch.isalnum() else "_" for ch in value.upper()).strip("_")


def write_cyclic_code_negative_results(report: CyclicCodeSearchReport) -> int:
    written = 0
    for record in report.records:
        if record.status not in {
            "cyclic-code-search-dequantized",
            "cyclic-collisions-all-dihedral-controls",
            "cyclic-collisions-all-automorphism-controls",
        }:
            continue
        upsert_negative_result(
            NegativeResultRecord(
                id=f"CYCLIC-CODE-SEARCH-{_safe_id(record.spec.id)}",
                source="cyclic_code_search.py",
                claim=f"{record.spec.id} cyclic-code tuple-profile collisions provide hard code-equivalence coset evidence.",
                reason_invalid=record.interpretation,
                lesson=(
                    "Cyclic algebraic structure is not hard evidence when collisions are reciprocal/dihedral controls "
                    "or are rejected by structural, tuple-profile, or canonicalization baselines."
                ),
                applies_to=["CODE-COSET-COLLECTIVE", "PO-DEQUANTIZATION", "PO-FALSIFIERS"],
                evidence=asdict(record),
            )
        )
        written += 1
    return written


def write_cyclic_code_search(
    output_path: Path = CYCLIC_CODE_SEARCH_PATH,
    specs: list[CyclicCodeSearchSpec] | None = None,
    tuple_cap: int = 50_000,
    canonical_max_assignments: int = 200_000,
    write_registry: bool = True,
    registry_experiment_id: str = "EXP-CODE-CYCLIC-ALGEBRAIC-SEARCH",
    registry_candidate_id: str = "CODE-COSET-COLLECTIVE",
    registry_result_id: str = "RESULT-CODE-CYCLIC-ALGEBRAIC-SEARCH-LATEST",
) -> dict[str, Any]:
    report = run_cyclic_code_search(
        specs=specs,
        tuple_cap=tuple_cap,
        canonical_max_assignments=canonical_max_assignments,
    )
    payload = _json_ready(report)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2, sort_keys=True))

    if write_registry:
        negative_results_written = write_cyclic_code_negative_results(report)
        metrics = dict(report.headline_metrics)
        metrics["negative_results_written"] = negative_results_written
        upsert_experiment_result(
            ExperimentResultRecord(
                id=registry_result_id,
                experiment_id=registry_experiment_id,
                candidate_id=registry_candidate_id,
                created_at=report.created_at,
                status=report.status,
                summary=report.summary,
                metrics=metrics,
                falsifiers_triggered=report.falsifiers_triggered,
                artifacts={"cyclic_code_search": str(output_path)},
            )
        )
    return payload

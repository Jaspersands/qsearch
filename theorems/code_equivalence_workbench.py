"""Linear-code equivalence workbench for hidden-permutation HSP candidates.

Code equivalence is one of the nonabelian hidden-permutation frontiers where a
Shor-level idea would matter.  This module does not try to solve it.  It builds
small auditable families and classical invariant baselines so low-ceiling coset
signals are rejected before they become candidate evidence.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, is_dataclass
from itertools import permutations
from pathlib import Path
from typing import Any, Sequence

import numpy as np

from research_registry import ExperimentResultRecord, NegativeResultRecord, upsert_experiment_result, upsert_negative_result, utc_now


CODE_EQUIVALENCE_DIR = Path("research/code_equivalence")
CODE_EQUIVALENCE_AUDIT_PATH = CODE_EQUIVALENCE_DIR / "code_equivalence_audit.json"


@dataclass(frozen=True)
class CodePairSpec:
    id: str
    code_a: str
    code_b: str
    length: int
    dimension: int
    known_equivalent: bool
    reason: str


@dataclass(frozen=True)
class CodeInvariantResult:
    name: str
    distinguishes: bool
    signature_a: str
    signature_b: str
    interpretation: str


@dataclass(frozen=True)
class CodeEquivalenceCertificate:
    name: str
    evaluated: bool
    equivalent: bool | None
    cost_model: str
    interpretation: str


@dataclass(frozen=True)
class CodePairAudit:
    pair: CodePairSpec
    invariants: list[CodeInvariantResult]
    certificate: CodeEquivalenceCertificate
    positive_signal: str
    falsifiers_triggered: list[str]


@dataclass(frozen=True)
class CodeEquivalenceWorkbenchResult:
    created_at: str
    pair_audits: list[CodePairAudit]
    summary: str
    falsifiers_triggered: list[str]


def hamming_7_4_generator() -> np.ndarray:
    return np.array(
        [
            [1, 0, 0, 0, 0, 1, 1],
            [0, 1, 0, 0, 1, 0, 1],
            [0, 0, 1, 0, 1, 1, 0],
            [0, 0, 0, 1, 1, 1, 1],
        ],
        dtype=np.uint8,
    )


def twisted_hamming_7_4_generator() -> np.ndarray:
    generator = hamming_7_4_generator().copy()
    generator[:, 6] = generator[:, 0]
    return generator


def weak_invariant_collision_8_4_generators() -> tuple[np.ndarray, np.ndarray]:
    """A deterministic [8,4] pair with matching weak invariants.

    The pair was selected because weight enumerator, generator-column weights,
    and pairwise inner-product multisets match, while support-splitting and
    bounded exact permutation search reject equivalence.  This is a useful
    boundary control: low-cost invariants are insufficient, but stronger
    classical fingerprints still dequantize the signal.
    """

    left = np.array(
        [
            [1, 0, 1, 1, 0, 1, 0, 0],
            [0, 0, 0, 1, 0, 0, 1, 1],
            [0, 1, 1, 0, 1, 0, 1, 1],
            [0, 1, 1, 0, 1, 0, 0, 0],
        ],
        dtype=np.uint8,
    )
    right = np.array(
        [
            [0, 1, 0, 1, 1, 1, 1, 0],
            [1, 0, 0, 0, 1, 0, 0, 1],
            [0, 0, 1, 1, 1, 1, 1, 1],
            [0, 0, 1, 0, 0, 0, 0, 0],
        ],
        dtype=np.uint8,
    )
    return left, right


def permute_columns(generator: np.ndarray, permutation: Sequence[int]) -> np.ndarray:
    return np.asarray(generator, dtype=np.uint8)[:, list(permutation)]


def gf2_rank(matrix: np.ndarray) -> int:
    values = np.asarray(matrix, dtype=np.uint8).copy() & 1
    rows, cols = values.shape
    rank = 0
    for col in range(cols):
        pivot = None
        for row in range(rank, rows):
            if values[row, col]:
                pivot = row
                break
        if pivot is None:
            continue
        if pivot != rank:
            values[[rank, pivot]] = values[[pivot, rank]]
        for row in range(rows):
            if row != rank and values[row, col]:
                values[row] ^= values[rank]
        rank += 1
        if rank == rows:
            break
    return rank


def enumerate_codewords(generator: np.ndarray) -> np.ndarray:
    matrix = np.asarray(generator, dtype=np.uint8) & 1
    dimension, length = matrix.shape
    codewords = np.zeros((1 << dimension, length), dtype=np.uint8)
    for mask in range(1 << dimension):
        word = np.zeros(length, dtype=np.uint8)
        for row in range(dimension):
            if (mask >> row) & 1:
                word ^= matrix[row]
        codewords[mask] = word
    return codewords


def codeword_int_set(generator: np.ndarray) -> frozenset[int]:
    encoded = []
    for word in enumerate_codewords(generator):
        value = 0
        for index, bit in enumerate(word.tolist()):
            if bit:
                value |= 1 << index
        encoded.append(value)
    return frozenset(encoded)


def permute_codeword_set(codewords: frozenset[int], length: int, permutation: Sequence[int]) -> frozenset[int]:
    permuted = []
    for word in codewords:
        value = 0
        for old_index, new_index in enumerate(permutation):
            if (word >> old_index) & 1:
                value |= 1 << int(new_index)
        permuted.append(value)
    return frozenset(permuted)


def weight_enumerator(generator: np.ndarray) -> tuple[tuple[int, int], ...]:
    weights = enumerate_codewords(generator).sum(axis=1)
    counts: dict[int, int] = {}
    for weight in weights.tolist():
        counts[int(weight)] = counts.get(int(weight), 0) + 1
    return tuple(sorted(counts.items()))


def column_weight_signature(generator: np.ndarray) -> tuple[int, ...]:
    return tuple(sorted(int(value) for value in np.asarray(generator, dtype=np.uint8).sum(axis=0)))


def pairwise_column_inner_signature(generator: np.ndarray) -> tuple[int, ...]:
    matrix = np.asarray(generator, dtype=np.uint8) & 1
    length = matrix.shape[1]
    values = []
    for left in range(length):
        for right in range(left + 1, length):
            values.append(int(np.dot(matrix[:, left], matrix[:, right]) % 2))
    return tuple(sorted(values))


def support_splitting_signature(generator: np.ndarray) -> tuple[tuple[int, ...], ...]:
    codewords = enumerate_codewords(generator)
    weights = codewords.sum(axis=1)
    signatures = []
    for coordinate in range(codewords.shape[1]):
        containing_weights = sorted(int(weights[index]) for index in range(codewords.shape[0]) if codewords[index, coordinate])
        signatures.append(tuple(containing_weights))
    return tuple(sorted(signatures))


def _invariant_result(name: str, sig_a: Any, sig_b: Any, label: str) -> CodeInvariantResult:
    distinguishes = sig_a != sig_b
    return CodeInvariantResult(
        name=name,
        distinguishes=distinguishes,
        signature_a=str(sig_a),
        signature_b=str(sig_b),
        interpretation=(
            f"{label} distinguishes the code pair; a matching coset observable would be classically dequantized."
            if distinguishes
            else f"{label} matches on this code pair."
        ),
    )


def code_invariant_suite(generator_a: np.ndarray, generator_b: np.ndarray) -> list[CodeInvariantResult]:
    return [
        _invariant_result("length_dimension_rank", (generator_a.shape[1], gf2_rank(generator_a)), (generator_b.shape[1], gf2_rank(generator_b)), "Length/dimension/rank"),
        _invariant_result("weight_enumerator", weight_enumerator(generator_a), weight_enumerator(generator_b), "Full codeword weight enumerator"),
        _invariant_result("column_weight_multiset", column_weight_signature(generator_a), column_weight_signature(generator_b), "Generator column-weight multiset"),
        _invariant_result("pairwise_column_inner_products", pairwise_column_inner_signature(generator_a), pairwise_column_inner_signature(generator_b), "Pairwise column inner-product multiset"),
        _invariant_result("support_splitting_fingerprint", support_splitting_signature(generator_a), support_splitting_signature(generator_b), "Support-splitting-style coordinate fingerprint"),
    ]


def known_permutation_certificate(
    generator_a: np.ndarray,
    generator_b: np.ndarray,
    permutation: Sequence[int] | None,
) -> CodeEquivalenceCertificate:
    if permutation is None:
        return CodeEquivalenceCertificate(
            name="known_generation_permutation",
            evaluated=False,
            equivalent=None,
            cost_model="No generation permutation was supplied.",
            interpretation="No exact equivalence certificate attached; rely on invariant baselines only.",
        )
    permuted = permute_columns(generator_a, permutation)
    equivalent = bool(np.array_equal(permuted, generator_b))
    return CodeEquivalenceCertificate(
        name="known_generation_permutation",
        evaluated=True,
        equivalent=equivalent,
        cost_model="O(k n) verification for a supplied generation permutation; not a scalable solver.",
        interpretation=(
            "Supplied generation permutation certifies equivalence for the control pair."
            if equivalent
            else "Supplied permutation does not map code A to code B; inspect the generator."
        ),
    )


def bounded_exact_permutation_certificate(
    generator_a: np.ndarray,
    generator_b: np.ndarray,
    max_permutations: int = 100_000,
) -> CodeEquivalenceCertificate:
    length = int(generator_a.shape[1])
    total = math_factorial(length)
    if total > max_permutations:
        return CodeEquivalenceCertificate(
            name="bounded_exact_permutation_search",
            evaluated=False,
            equivalent=None,
            cost_model=f"Skipped: {length}! = {total} permutations exceeds cap {max_permutations}.",
            interpretation="Exact permutation search skipped; use stronger scalable canonicalization baselines.",
        )
    target = codeword_int_set(generator_b)
    source = codeword_int_set(generator_a)
    checked = 0
    for permutation in permutations(range(length)):
        checked += 1
        if permute_codeword_set(source, length, permutation) == target:
            return CodeEquivalenceCertificate(
                name="bounded_exact_permutation_search",
                evaluated=True,
                equivalent=True,
                cost_model=f"Checked {checked} of {total} column permutations; exponential sanity check only.",
                interpretation="Exact bounded search found an equivalence permutation.",
            )
    return CodeEquivalenceCertificate(
        name="bounded_exact_permutation_search",
        evaluated=True,
        equivalent=False,
        cost_model=f"Checked all {total} column permutations; exponential sanity check only.",
        interpretation="Exact bounded search certifies no column permutation equivalence at this size.",
    )


def math_factorial(value: int) -> int:
    result = 1
    for item in range(2, value + 1):
        result *= item
    return result


def audit_code_pair(pair_id: str) -> CodePairAudit:
    if pair_id == "hamming-7-4-permuted":
        generator_a = hamming_7_4_generator()
        permutation = [2, 0, 6, 1, 5, 3, 4]
        generator_b = permute_columns(generator_a, permutation)
        spec = CodePairSpec(
            id=pair_id,
            code_a="[7,4] Hamming generator",
            code_b="Column-permuted [7,4] Hamming generator",
            length=7,
            dimension=4,
            known_equivalent=True,
            reason="Control pair with a known hidden permutation.",
        )
    elif pair_id == "hamming-7-4-column-twist":
        generator_a = hamming_7_4_generator()
        generator_b = twisted_hamming_7_4_generator()
        permutation = None
        spec = CodePairSpec(
            id=pair_id,
            code_a="[7,4] Hamming generator",
            code_b="Hamming generator with one duplicated column",
            length=7,
            dimension=4,
            known_equivalent=False,
            reason="Control non-equivalent pair that classical code invariants should reject.",
        )
    elif pair_id == "random-8-4-weak-invariant-collision":
        generator_a, generator_b = weak_invariant_collision_8_4_generators()
        permutation = None
        spec = CodePairSpec(
            id=pair_id,
            code_a="Random full-rank [8,4] generator A with weak invariant collision",
            code_b="Random full-rank [8,4] generator B with matching weak invariants",
            length=8,
            dimension=4,
            known_equivalent=False,
            reason=(
                "Weight enumerator, column weights, and pairwise inner-product multisets match; "
                "support splitting and exact bounded permutation search reject equivalence."
            ),
        )
    else:
        raise ValueError(f"unknown code pair: {pair_id}")

    invariants = code_invariant_suite(generator_a, generator_b)
    certificate = (
        known_permutation_certificate(generator_a, generator_b, permutation)
        if permutation is not None
        else bounded_exact_permutation_certificate(generator_a, generator_b)
    )
    falsifiers = []
    if any(item.distinguishes for item in invariants):
        falsifiers.append("A classical code invariant distinguishes the pair; any matching coset observable is dequantized.")
    if spec.known_equivalent and certificate.evaluated and not certificate.equivalent:
        falsifiers.append("Known-permutation certificate failed for an equivalent control pair.")

    if spec.known_equivalent and certificate.equivalent and not any(item.distinguishes for item in invariants):
        positive = "control equivalent pair: hidden permutation certificate verifies and invariants match"
    elif any(item.distinguishes for item in invariants):
        positive = "control: classical code-equivalence baseline distinguishes this pair"
    else:
        positive = "boundary-like code pair: invariants match but no equivalence certificate is known"

    return CodePairAudit(spec, invariants, certificate, positive, falsifiers)


def run_code_equivalence_workbench(pair_ids: Sequence[str] | None = None) -> CodeEquivalenceWorkbenchResult:
    active_pairs = list(pair_ids) if pair_ids is not None else [
        "hamming-7-4-permuted",
        "hamming-7-4-column-twist",
        "random-8-4-weak-invariant-collision",
    ]
    audits = [audit_code_pair(pair_id) for pair_id in active_pairs]
    falsifiers = sorted({item for audit in audits for item in audit.falsifiers_triggered})
    equivalent_controls = sum(1 for audit in audits if audit.positive_signal.startswith("control equivalent"))
    classically_solved = sum(1 for audit in audits if "classical code-equivalence baseline" in audit.positive_signal)
    summary = (
        f"Audited {len(audits)} code-equivalence pairs. "
        f"{equivalent_controls} equivalent control pair(s) verified; "
        f"{classically_solved} non-equivalent control pair(s) classically distinguished."
    )
    return CodeEquivalenceWorkbenchResult(utc_now(), audits, summary, falsifiers)


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


def write_code_equivalence_negative_results(result: CodeEquivalenceWorkbenchResult) -> int:
    written = 0
    for audit in result.pair_audits:
        distinguishing = [item.name for item in audit.invariants if item.distinguishes]
        if not distinguishing:
            continue
        upsert_negative_result(
            NegativeResultRecord(
                id=f"CODE-EQUIV-DEQUANTIZED-{audit.pair.id.upper().replace('-', '_')}",
                source="code_equivalence_workbench.py",
                claim=f"{audit.pair.id} provides nonclassical code-equivalence coset evidence.",
                reason_invalid="Classical code invariant(s) distinguish the pair: " + ", ".join(distinguishing),
                lesson="Do not count a code-equivalence coset signal if weight enumerators, support splitting, or simple code invariants already separate the instances.",
                applies_to=["CODE-COSET-COLLECTIVE", "MUT-CAND-CODE-COSET-COLLECTIVE-CFI-WL-HARD-COSET", "PO-DEQUANTIZATION", "PO-FALSIFIERS"],
                evidence={
                    "pair_id": audit.pair.id,
                    "distinguishing_invariants": distinguishing,
                    "positive_signal": audit.positive_signal,
                },
            )
        )
        written += 1
    return written


def write_code_equivalence_workbench(
    output_path: Path = CODE_EQUIVALENCE_AUDIT_PATH,
    pair_ids: Sequence[str] | None = None,
    write_registry: bool = True,
    registry_experiment_id: str = "EXP-CODE-COSET-RANK",
    registry_candidate_id: str = "CODE-COSET-COLLECTIVE",
    registry_result_id: str = "RESULT-CODE-EQUIVALENCE-WORKBENCH-LATEST",
) -> dict[str, Any]:
    result = run_code_equivalence_workbench(pair_ids=pair_ids)
    payload = _json_ready(result)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2, sort_keys=True))

    if write_registry:
        negative_results_written = write_code_equivalence_negative_results(result)
        metrics = {
            "pair_audit_count": len(result.pair_audits),
            "equivalent_control_verified_count": sum(
                1 for audit in result.pair_audits if audit.certificate.evaluated and audit.certificate.equivalent
            ),
            "exact_nonequivalence_certificate_count": sum(
                1 for audit in result.pair_audits if audit.certificate.evaluated and audit.certificate.equivalent is False
            ),
            "classically_distinguished_pair_count": sum(
                1 for audit in result.pair_audits if any(item.distinguishes for item in audit.invariants)
            ),
            "weak_invariant_collision_count": sum(
                1
                for audit in result.pair_audits
                if not any(
                    item.name in {
                        "length_dimension_rank",
                        "weight_enumerator",
                        "column_weight_multiset",
                        "pairwise_column_inner_products",
                    }
                    and item.distinguishes
                    for item in audit.invariants
                )
                and any(item.name == "support_splitting_fingerprint" and item.distinguishes for item in audit.invariants)
            ),
            "support_splitting_distinguishes_count": sum(
                1
                for audit in result.pair_audits
                if any(item.name == "support_splitting_fingerprint" and item.distinguishes for item in audit.invariants)
            ),
            "negative_results_written": negative_results_written,
        }
        upsert_experiment_result(
            ExperimentResultRecord(
                id=registry_result_id,
                experiment_id=registry_experiment_id,
                candidate_id=registry_candidate_id,
                created_at=result.created_at,
                status="blocked-by-code-invariants" if result.falsifiers_triggered else "needs-harder-code-family",
                summary=result.summary,
                metrics=metrics,
                falsifiers_triggered=result.falsifiers_triggered,
                artifacts={"code_equivalence_audit": str(output_path)},
            )
        )
    return payload

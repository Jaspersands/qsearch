"""Literature-grounded complexity and preprocessing ledger for character shifts.

Shifted Legendre and quartic characters have efficient quantum Fourier
algorithms, but their classical status is a computational decoding gap rather
than a query lower bound.  This module records the relevant classical upper
bounds and tests a nonuniform preprocessing attack: fixed public query
positions fingerprint every shift after O(log p) symbols on the tested rows,
while a domain-size table makes online decoding a dictionary lookup.

The attack does not dequantize the uniform single-instance problem because its
preprocessing and advice are exponential in log p.  It does force every claim
to state whether preprocessing, advice, and repeated-instance amortization are
allowed, and it prevents logarithmic-query evidence from being mislabeled as a
computational lower bound.
"""

from __future__ import annotations

import json
import math
from collections import Counter
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Sequence

import numpy as np

from phase_state_workbench import apply_hidden_shift, generate_cyclic_phase_family
from research_registry import NegativeResultRecord, upsert_negative_result, upsert_scaling_run, utc_now


CHARACTER_SHIFT_COMPLEXITY_PATH = Path("research/classical_baselines/character_shift_complexity.json")

LITERATURE_SOURCES = {
    "van-dam-hallgren-shifted-character-2000": "https://arxiv.org/abs/quant-ph/0011067",
    "ip-shift-deconvolution-2002": "https://arxiv.org/abs/quant-ph/0205034",
    "bourgain-hidden-shifted-power-2011": "https://arxiv.org/abs/1110.0812",
}


@dataclass(frozen=True)
class CharacterClassicalUpperBound:
    family_id: str
    n_bits: int
    prime: int
    character_order: int
    shifted_power_exponent: int
    algorithm: str
    literature_id: str
    theorem_or_section: str
    access_model: str
    query_bound: str
    time_bound: str
    time_exponent_in_prime: float | None
    preprocessing_bound: str
    implication: str


@dataclass(frozen=True)
class PrefixCollisionProfile:
    prefix_length: int
    distinct_signature_count: int
    max_bucket_size: int
    collision_pair_count: int


@dataclass(frozen=True)
class CharacterPreprocessingRecord:
    family_id: str
    n_bits: int
    prime: int
    character_order: int
    true_shift: int
    fixed_query_positions: list[int]
    first_globally_unique_prefix: int | None
    prefix_over_n_bits: float | None
    recovered_shift: int | None
    success: bool
    preprocessing_operations: int
    preprocessing_memory_labels: int
    advice_bits_upper_bound: int
    online_queries: int
    online_lookup_operations: int
    single_instance_total_operations: int
    preprocessing_operation_exponent_per_bit: float
    memory_exponent_per_bit: float
    online_operation_exponent_per_bit: float
    amortized_operations_by_batch: dict[str, float]
    collision_profile: list[PrefixCollisionProfile]
    access_model: str
    status: str
    interpretation: str
    use_as_positive_evidence: bool


def _character_order(family_id: str) -> int:
    if family_id == "legendre_symbol":
        return 2
    if family_id == "quartic_character":
        return 4
    raise ValueError(f"character complexity ledger only supports Legendre/quartic families, got {family_id}")


def _phase_labels(signal: np.ndarray) -> list[tuple[float, float]]:
    return [(round(float(value.real), 8), round(float(value.imag), 8)) for value in signal]


def _signature(
    labels: Sequence[tuple[float, float]],
    shift: int,
    positions: Sequence[int],
) -> tuple[tuple[float, float], ...]:
    size = len(labels)
    return tuple(labels[(int(position) + int(shift)) % size] for position in positions)


def _collision_profile(signatures: Sequence[tuple[Any, ...]], prefix_length: int) -> PrefixCollisionProfile:
    counts = Counter(signatures)
    collision_pairs = sum(count * (count - 1) // 2 for count in counts.values())
    return PrefixCollisionProfile(
        prefix_length=int(prefix_length),
        distinct_signature_count=len(counts),
        max_bucket_size=max(counts.values(), default=0),
        collision_pair_count=int(collision_pairs),
    )


def audit_fixed_prefix_preprocessing(
    family_id: str,
    n_bits: int,
    shift: int = 7,
    max_prefix_factor: int = 8,
) -> CharacterPreprocessingRecord:
    spec, signal = generate_cyclic_phase_family(family_id, n_bits=n_bits)
    order = _character_order(spec.id)
    labels = _phase_labels(np.asarray(signal, dtype=complex))
    max_prefix = min(spec.domain_size, max(1, int(max_prefix_factor) * spec.n_bits))
    profiles: list[PrefixCollisionProfile] = []
    first_unique: int | None = None
    signature_table: dict[tuple[tuple[float, float], ...], list[int]] = {}

    for prefix_length in range(1, max_prefix + 1):
        positions = list(range(prefix_length))
        signatures = [_signature(labels, candidate, positions) for candidate in range(spec.domain_size)]
        profile = _collision_profile(signatures, prefix_length)
        profiles.append(profile)
        if profile.distinct_signature_count == spec.domain_size:
            first_unique = prefix_length
            for candidate, signature in enumerate(signatures):
                signature_table.setdefault(signature, []).append(candidate)
            break

    selected_prefix = first_unique if first_unique is not None else max_prefix
    positions = list(range(selected_prefix))
    if first_unique is None:
        for candidate in range(spec.domain_size):
            signature_table.setdefault(_signature(labels, candidate, positions), []).append(candidate)

    true_shift = int(shift) % spec.domain_size
    shifted = apply_hidden_shift(spec, signal, true_shift)
    shifted_labels = _phase_labels(np.asarray(shifted, dtype=complex))
    observed_signature = tuple(shifted_labels[position] for position in positions)
    candidates = signature_table.get(observed_signature, [])
    recovered_shift = candidates[0] if len(candidates) == 1 else None
    success = recovered_shift == true_shift

    preprocessing_operations = int(spec.domain_size * selected_prefix)
    memory_labels = int(spec.domain_size * selected_prefix)
    label_bits = max(1, int(math.ceil(math.log2(order + 1))))
    advice_bits = int(memory_labels * label_bits + spec.domain_size * spec.n_bits)
    online_operations = max(1, selected_prefix)
    single_total = preprocessing_operations + online_operations
    batches = sorted({1, max(1, spec.n_bits), max(1, spec.domain_size)})
    amortized = {
        str(batch): float(preprocessing_operations / batch + online_operations)
        for batch in batches
    }
    exponent_denominator = max(1, spec.n_bits)

    if success and first_unique is not None:
        status = "fixed-query-fingerprint-with-domain-preprocessing"
        interpretation = (
            "A fixed public prefix uniquely fingerprints every shift and a precomputed domain-size table decodes the "
            "observed prefix online. Online query/time cost is polynomial in log p, but preprocessing and advice remain "
            "Theta(p log p), exponential in the encoded input length."
        )
    else:
        status = "fixed-prefix-still-ambiguous"
        interpretation = (
            "The configured fixed prefix did not uniquely fingerprint every shift; increase the prefix or prove an "
            "asymptotic collision bound."
        )
    return CharacterPreprocessingRecord(
        family_id=spec.id,
        n_bits=spec.n_bits,
        prime=spec.modulus,
        character_order=order,
        true_shift=true_shift,
        fixed_query_positions=positions,
        first_globally_unique_prefix=first_unique,
        prefix_over_n_bits=(float(first_unique / spec.n_bits) if first_unique is not None else None),
        recovered_shift=recovered_shift,
        success=bool(success),
        preprocessing_operations=preprocessing_operations,
        preprocessing_memory_labels=memory_labels,
        advice_bits_upper_bound=advice_bits,
        online_queries=selected_prefix,
        online_lookup_operations=online_operations,
        single_instance_total_operations=single_total,
        preprocessing_operation_exponent_per_bit=float(math.log2(max(1, preprocessing_operations)) / exponent_denominator),
        memory_exponent_per_bit=float(math.log2(max(1, memory_labels)) / exponent_denominator),
        online_operation_exponent_per_bit=float(math.log2(max(1, online_operations)) / exponent_denominator),
        amortized_operations_by_batch=amortized,
        collision_profile=profiles,
        access_model="fixed chosen queries plus public modulus-dependent nonuniform preprocessing/advice",
        status=status,
        interpretation=interpretation,
        use_as_positive_evidence=False,
    )


def literature_classical_upper_bounds(family_id: str, n_bits: int) -> list[CharacterClassicalUpperBound]:
    spec, _signal = generate_cyclic_phase_family(family_id, n_bits=n_bits)
    order = _character_order(spec.id)
    exponent = (spec.modulus - 1) // order
    query_denominator = max(math.log(max(1.000001, spec.modulus / exponent)), 1e-9)
    theorem_43_queries = max(1, int(math.ceil(math.log(spec.modulus) / query_denominator)))
    common = {
        "family_id": spec.id,
        "n_bits": spec.n_bits,
        "prime": spec.modulus,
        "character_order": order,
        "shifted_power_exponent": exponent,
    }
    return [
        CharacterClassicalUpperBound(
            **common,
            algorithm="dense shifted-power interpolation",
            literature_id="bourgain-hidden-shifted-power-2011",
            theorem_or_section="Introduction, interpolation baseline",
            access_model="classical evaluator oracle returning (x+s)^e",
            query_bound=f"e+1={exponent + 1}",
            time_bound="e * poly(log p)",
            time_exponent_in_prime=float(math.log(max(1, exponent), spec.modulus)),
            preprocessing_bound="none",
            implication="A uniform deterministic recovery upper bound is already domain-scale for fixed character order.",
        ),
        CharacterClassicalUpperBound(
            **common,
            algorithm="deterministic hidden-shifted-power candidate reduction",
            literature_id="bourgain-hidden-shifted-power-2011",
            theorem_or_section="Theorem 43",
            access_model="classical shifted-power evaluator oracle",
            query_bound=f"O(log p / log(p/e)); numeric ceiling={theorem_43_queries}",
            time_bound="p * poly(log p)",
            time_exponent_in_prime=1.0,
            preprocessing_bound="none",
            implication=(
                "For e=(p-1)/character_order, classical query complexity is logarithmic even though the known "
                "uniform decoding time remains domain-linear."
            ),
        ),
        CharacterClassicalUpperBound(
            **common,
            algorithm="known-shift identity test",
            literature_id="bourgain-hidden-shifted-power-2011",
            theorem_or_section="Theorem 46",
            access_model="classical evaluator oracle plus proposed candidate t",
            query_bound="included in p^(1/4+o(1)) running time",
            time_bound="p^(1/4+o(1)) for deciding s=t",
            time_exponent_in_prime=0.25,
            preprocessing_bound="none",
            implication="Sublinear candidate verification exists, but testing all p candidates is not a poly(log p) decoder.",
        ),
        CharacterClassicalUpperBound(
            **common,
            algorithm="fixed-prefix signature table",
            literature_id="project-character-preprocessing-baseline",
            theorem_or_section="executable baseline",
            access_model="fixed chosen queries with modulus-dependent preprocessing/advice",
            query_bound="empirical O(log p) fixed prefix on tested rows",
            time_bound="online O(log p), preprocessing O(p log p)",
            time_exponent_in_prime=1.0,
            preprocessing_bound="Theta(p log p) labels plus shift dictionary",
            implication="Any online hardness claim must exclude exponential advice/preprocessing and state amortization assumptions.",
        ),
    ]


def build_character_shift_complexity_report(
    families: Sequence[str] | None = None,
    n_values: Sequence[int] | None = None,
    shift: int = 7,
    max_prefix_factor: int = 8,
) -> dict[str, Any]:
    active_families = list(families) if families is not None else ["legendre_symbol", "quartic_character"]
    active_n = list(n_values) if n_values is not None else [5, 6, 7, 8, 9, 10]
    preprocessing = [
        audit_fixed_prefix_preprocessing(family, n_bits, shift=shift, max_prefix_factor=max_prefix_factor)
        for family in active_families
        for n_bits in active_n
    ]
    upper_bounds = [
        bound
        for family in active_families
        for n_bits in active_n
        for bound in literature_classical_upper_bounds(family, n_bits)
    ]
    successful = sum(1 for row in preprocessing if row.success and row.first_globally_unique_prefix is not None)
    all_preprocessed = successful == len(preprocessing) and bool(preprocessing)
    status = (
        "conditional-uniform-decoding-gap-only"
        if all_preprocessed
        else "prefix-collision-proof-debt"
    )
    summary = (
        f"Audited {len(preprocessing)} shifted-character preprocessing row(s) and {len(upper_bounds)} "
        f"literature upper-bound row(s). Fixed O(log p)-scale prefixes plus domain-size advice decoded "
        f"{successful} row(s); no unconditional superpolynomial decoding lower bound or natural-problem reduction is recorded."
    )
    return {
        "id": "CHARACTER-SHIFT-COMPLEXITY-LATEST",
        "created_at": utc_now(),
        "kind": "multiplicative-character-complexity-and-preprocessing-ledger",
        "families": active_families,
        "n_values": active_n,
        "literature_ids": sorted(LITERATURE_SOURCES),
        "literature_sources": LITERATURE_SOURCES,
        "status": status,
        "summary": summary,
        "headline_metrics": {
            "preprocessing_row_count": len(preprocessing),
            "fixed_prefix_decode_success_count": successful,
            "fixed_prefix_ambiguous_count": len(preprocessing) - successful,
            "known_classical_upper_bound_count": len(upper_bounds),
            "logarithmic_query_domain_time_upper_bound_count": sum(
                1 for row in upper_bounds if row.theorem_or_section == "Theorem 43"
            ),
            "nonuniform_online_polylog_count": successful,
            "uniform_polylog_classical_decoder_count": 0,
            "unconditional_superpolynomial_lower_bound_count": 0,
            "natural_problem_reduction_count": 0,
            "max_unique_prefix_over_n_bits": max(
                (row.prefix_over_n_bits or 0.0 for row in preprocessing), default=0.0
            ),
            "max_preprocessing_operation_exponent_per_bit": max(
                (row.preprocessing_operation_exponent_per_bit for row in preprocessing), default=0.0
            ),
            "max_online_operation_exponent_per_bit": max(
                (row.online_operation_exponent_per_bit for row in preprocessing), default=0.0
            ),
            "positive_evidence_count": 0,
        },
        "preprocessing_records": [asdict(row) for row in preprocessing],
        "classical_upper_bounds": [asdict(row) for row in upper_bounds],
        "claim_gate": {
            "query_advantage_allowed": False,
            "online_advantage_requires_no_preprocessing_model": True,
            "single_instance_uniform_model_required": True,
            "unconditional_lower_bound_known": False,
            "natural_reduction_known": False,
            "required_statement": (
                "State the problem as a uniform single-instance computational decoding conjecture with explicit "
                "preprocessing/advice exclusions; supply a natural reduction or named hardness assumption before "
                "treating it as more than an oracle separation."
            ),
        },
        "falsifiers_triggered": [
            "Known classical hidden-shifted-power algorithms already use logarithmically many queries with domain-scale time.",
            "Fixed public query prefixes admit polynomial-online decoding after domain-size preprocessing on every tested row."
            if all_preprocessed
            else "Some fixed-prefix rows remain ambiguous and need larger-scale collision analysis.",
            "No unconditional superpolynomial decoding lower bound or natural-problem reduction is present.",
        ],
    }


def write_character_shift_complexity_report(
    output_path: Path = CHARACTER_SHIFT_COMPLEXITY_PATH,
    families: Sequence[str] | None = None,
    n_values: Sequence[int] | None = None,
    shift: int = 7,
    max_prefix_factor: int = 8,
    write_registry: bool = True,
) -> dict[str, Any]:
    payload = build_character_shift_complexity_report(
        families=families,
        n_values=n_values,
        shift=shift,
        max_prefix_factor=max_prefix_factor,
    )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    if write_registry:
        upsert_scaling_run(
            {
                "id": payload["id"],
                "created_at": payload["created_at"],
                "kind": payload["kind"],
                "status": payload["status"],
                "summary": payload["summary"],
                "row_count": payload["headline_metrics"]["preprocessing_row_count"],
                "artifacts": {"character_shift_complexity": str(output_path)},
                "headline_metrics": payload["headline_metrics"],
            }
        )
        for family_id in payload["families"]:
            family_rows = [
                row
                for row in payload["preprocessing_records"]
                if row["family_id"] == family_id and row["success"]
            ]
            if not family_rows:
                continue
            upsert_negative_result(
                NegativeResultRecord(
                    id=f"CHARACTER-QUERY-ADVANTAGE-KILLED-{family_id.upper()}",
                    source="character_shift_complexity.py",
                    claim=f"{family_id} supplies a character-shift query advantage or unconditional online decoding separation.",
                    reason_invalid=(
                        "Known hidden-shifted-power upper bounds use logarithmically many classical queries with "
                        "domain-scale uniform time, and every tested row admits fixed-prefix online decoding after "
                        "modulus-dependent domain-size preprocessing/advice."
                    ),
                    lesson=(
                        "The only unresolved claim is a uniform single-instance computational decoding gap. State "
                        "preprocessing/advice exclusions and attach a natural reduction or named hardness assumption."
                    ),
                    applies_to=[
                        "DHS-GOWERS-SIEVE",
                        "HYP-LIT-HIDDEN-SHIFT-SIEVE",
                        "PO-DEQUANTIZATION",
                        "PO-FALSIFIERS",
                    ],
                    evidence={
                        "family_id": family_id,
                        "tested_n_bits": sorted({int(row["n_bits"]) for row in family_rows}),
                        "fixed_prefix_success_count": len(family_rows),
                        "max_unique_prefix_over_n_bits": max(
                            float(row["prefix_over_n_bits"] or 0.0) for row in family_rows
                        ),
                        "uniform_polylog_classical_decoder_known": False,
                        "natural_problem_reduction_known": False,
                    },
                )
            )
    return payload

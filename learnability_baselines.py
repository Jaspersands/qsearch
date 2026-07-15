"""Low-degree and sparse-structure learnability baselines.

Major hidden-shift candidates are worthless if their phase functions are
classically learnable as low-degree objects.  This module adds a direct
learnability layer that is separate from shift-recovery experiments: it asks
whether the function family itself is algebraically simple enough that a
classical evaluator adversary should be expected to reconstruct it.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Sequence

import numpy as np

from phase_state_workbench import generate_cyclic_phase_family
from research_registry import NegativeResultRecord, upsert_negative_result, upsert_scaling_run, utc_now


LEARNABILITY_DIR = Path("research/classical_baselines")
LEARNABILITY_REPORT_PATH = LEARNABILITY_DIR / "learnability_baselines.json"


@dataclass(frozen=True)
class LearnabilityRecord:
    family_id: str
    n_bits: int
    group: str
    domain_size: int
    exact_algebraic_degree: int | None
    exact_sparsity: int | None
    empirical_degree_bound: int | None
    low_degree_acceptance: float | None
    reconstruction_query_estimate: int | None
    verdict: str
    notes: str


@dataclass(frozen=True)
class LearnabilityFamilySummary:
    family_id: str
    tested_n_bits: list[int]
    dequantized_low_degree_count: int
    high_degree_or_unresolved_count: int
    best_verdict: str
    lesson: str


def _boolean_phase_bits(signal: Sequence[complex]) -> np.ndarray | None:
    values = np.asarray(signal, dtype=complex)
    if not np.allclose(np.abs(values), 1.0, atol=1e-8):
        return None
    real = np.real(values)
    if not np.allclose(np.imag(values), 0.0, atol=1e-8):
        return None
    if not np.all((np.isclose(real, 1.0, atol=1e-8)) | (np.isclose(real, -1.0, atol=1e-8))):
        return None
    return (real < 0).astype(np.uint8)


def anf_coefficients(bits: Sequence[int]) -> np.ndarray:
    coeffs = np.asarray(bits, dtype=np.uint8).copy() & 1
    size = coeffs.size
    if size == 0 or size & (size - 1):
        raise ValueError("ANF input length must be a non-zero power of two")
    n_bits = int(math.log2(size))
    for bit in range(n_bits):
        step = 1 << bit
        for mask in range(size):
            if mask & step:
                coeffs[mask] ^= coeffs[mask ^ step]
    return coeffs


def anf_degree_and_sparsity(bits: Sequence[int]) -> tuple[int, int]:
    coeffs = anf_coefficients(bits)
    active = [index for index, value in enumerate(coeffs.tolist()) if value & 1]
    if not active:
        return 0, 0
    return max(index.bit_count() for index in active), len(active)


def f2_third_derivative_acceptance(bits: Sequence[int], samples: int = 128, seed: int = 0) -> float:
    values = np.asarray(bits, dtype=np.uint8) & 1
    size = values.size
    n_bits = int(math.log2(size))
    rng = np.random.default_rng(seed)
    accepted = 0
    for _ in range(samples):
        x = int(rng.integers(0, size))
        a = int(rng.integers(1, size))
        b = int(rng.integers(1, size))
        c = int(rng.integers(1, size))
        total = 0
        for mask in range(8):
            point = x
            if mask & 1:
                point ^= a
            if mask & 2:
                point ^= b
            if mask & 4:
                point ^= c
            total ^= int(values[point])
        accepted += int(total == 0)
    return accepted / max(1, samples)


def _decode_prime_root_phases(signal: Sequence[complex], modulus: int) -> np.ndarray | None:
    values = np.asarray(signal, dtype=complex)
    angles = np.mod(np.angle(values), 2 * np.pi)
    phases = np.rint((angles * modulus) / (2 * np.pi)).astype(int) % modulus
    reconstructed = np.exp(2j * np.pi * phases / modulus)
    if not np.allclose(values, reconstructed, atol=1e-6):
        return None
    return phases


def _univariate_difference_zero_rate(
    phases: np.ndarray,
    modulus: int,
    degree: int,
    samples: int = 128,
    seed: int = 0,
) -> float:
    rng = np.random.default_rng(seed)
    order = degree + 1
    coefficients = [(-1) ** (order - index) * math.comb(order, index) for index in range(order + 1)]
    accepted = 0
    for _ in range(samples):
        x = int(rng.integers(0, modulus))
        h = int(rng.integers(1, modulus))
        total = 0
        for index, coefficient in enumerate(coefficients):
            total += coefficient * int(phases[(x + index * h) % modulus])
        accepted += int(total % modulus == 0)
    return accepted / max(1, samples)


def _fp2_difference_zero_rate(
    phases: np.ndarray,
    prime: int,
    degree: int,
    samples: int = 128,
    seed: int = 0,
) -> float:
    rng = np.random.default_rng(seed)
    order = degree + 1
    accepted = 0
    grid = phases.reshape((prime, prime))
    for _ in range(samples):
        x0 = int(rng.integers(0, prime))
        y0 = int(rng.integers(0, prime))
        directions = [
            (int(rng.integers(0, prime)), int(rng.integers(0, prime))) for _ in range(order)
        ]
        if all(dx == 0 and dy == 0 for dx, dy in directions):
            directions[0] = (1, 0)
        total = 0
        for mask in range(1 << order):
            x = x0
            y = y0
            parity = 0
            for bit, (dx, dy) in enumerate(directions):
                if mask & (1 << bit):
                    x = (x + dx) % prime
                    y = (y + dy) % prime
                    parity ^= 1
            total += (-1 if (order - parity) & 1 else 1) * int(grid[x, y])
        accepted += int(total % prime == 0)
    return accepted / max(1, samples)


def _binomial_monomial_count(n_bits: int, degree: int) -> int:
    return sum(math.comb(n_bits, item) for item in range(degree + 1))


def audit_family_learnability(family_id: str, n_bits: int, samples: int = 128, seed: int = 0) -> LearnabilityRecord:
    spec, signal = generate_cyclic_phase_family(family_id, n_bits=n_bits)
    exact_degree: int | None = None
    exact_sparsity: int | None = None
    empirical_degree: int | None = None
    acceptance: float | None = None
    query_estimate: int | None = None
    verdict = "unresolved-learnability"
    notes = "No low-degree model was certified by implemented tests."

    if spec.group == "F2^n":
        bits = _boolean_phase_bits(signal)
        if bits is not None:
            exact_degree, exact_sparsity = anf_degree_and_sparsity(bits)
            acceptance = f2_third_derivative_acceptance(bits, samples=samples, seed=seed)
            empirical_degree = 2 if acceptance >= 0.999 else None
            if exact_degree <= 2:
                query_estimate = _binomial_monomial_count(spec.n_bits, exact_degree)
                verdict = "dequantized-exact-low-degree"
                notes = f"Exact ANF degree {exact_degree} with {exact_sparsity} monomial(s); polynomial interpolation is a classical baseline."
            elif exact_degree <= 3:
                query_estimate = _binomial_monomial_count(spec.n_bits, exact_degree)
                verdict = "dequantized-exact-low-degree"
                notes = f"Exact ANF degree {exact_degree} is still constant-degree; polynomial interpolation is a classical baseline."
            elif exact_sparsity <= max(8, int(0.10 * spec.domain_size)):
                query_estimate = exact_sparsity * max(1, spec.n_bits)
                verdict = "dequantized-sparse-anf"
                notes = (
                    f"Exact ANF has degree {exact_degree} but only {exact_sparsity} monomial(s); "
                    "sparse polynomial learning is a classical baseline."
                )
            elif acceptance >= 0.95:
                verdict = "suspect-low-degree-by-third-derivative-test"
                notes = "Random third-derivative test often vanishes; run exact or noise-tolerant low-degree reconstruction."
            else:
                verdict = "not-low-degree-under-current-tests"
                notes = f"Exact ANF degree {exact_degree}; third-derivative acceptance {acceptance:.3f}."

    elif spec.group == "Z_p":
        phases = _decode_prime_root_phases(signal, spec.modulus)
        if phases is not None:
            for degree in range(0, 5):
                rate = _univariate_difference_zero_rate(phases, spec.modulus, degree=degree, samples=samples, seed=seed + degree)
                if rate >= 0.999:
                    empirical_degree = degree
                    acceptance = rate
                    break
            if empirical_degree is not None and empirical_degree <= 3:
                query_estimate = empirical_degree + 2
                verdict = "dequantized-prime-field-low-degree"
                notes = f"Finite-difference test certifies degree <= {empirical_degree}; evaluator interpolation should be treated as a classical baseline."
            elif empirical_degree is not None:
                query_estimate = empirical_degree + 2
                verdict = "low-degree-but-not-immediate-rejection"
                notes = f"Finite-difference test suggests degree <= {empirical_degree}; add explicit interpolation attack."
            else:
                acceptance = _univariate_difference_zero_rate(phases, spec.modulus, degree=4, samples=samples, seed=seed + 99)
                verdict = "not-low-degree-under-current-tests"
                notes = "Prime-root phase is not degree <=4 under sampled finite-difference tests."

    elif spec.group == "F_p^2":
        phases = _decode_prime_root_phases(signal, spec.modulus)
        if phases is not None:
            acceptance = _fp2_difference_zero_rate(phases, spec.modulus, degree=2, samples=samples, seed=seed)
            if acceptance >= 0.999:
                empirical_degree = 2
                query_estimate = (spec.n_bits + 1) * (spec.n_bits + 2) // 2
                verdict = "dequantized-vector-field-low-degree"
                notes = "Third finite differences vanish over F_p^2; low-degree interpolation/reconstruction is a classical baseline."
            else:
                verdict = "not-low-degree-under-current-tests"
                notes = f"F_p^2 third-difference acceptance {acceptance:.3f}; no degree-2 certificate."

    return LearnabilityRecord(
        family_id=spec.id,
        n_bits=spec.n_bits,
        group=spec.group,
        domain_size=spec.domain_size,
        exact_algebraic_degree=exact_degree,
        exact_sparsity=exact_sparsity,
        empirical_degree_bound=empirical_degree,
        low_degree_acceptance=acceptance,
        reconstruction_query_estimate=query_estimate,
        verdict=verdict,
        notes=notes,
    )


def build_learnability_report(
    families: Sequence[str] | None = None,
    n_values: Sequence[int] | None = None,
    samples: int = 128,
    seed: int = 0,
) -> dict[str, Any]:
    active_families = list(families) if families is not None else [
        "quadratic_chirp",
        "cubic_chirp",
        "noisy_cubic_chirp",
        "kloosterman_trace",
        "quartic_character",
        "fp2_quadratic_form",
        "mm_majority_bent_f2",
        "bent_quadratic_f2",
        "masked_quadratic_f2",
    ]
    active_n = list(n_values) if n_values is not None else [5, 6, 7, 8]
    records = [
        audit_family_learnability(family_id, n_bits, samples=samples, seed=seed + n_bits * 37 + index)
        for n_bits in active_n
        for index, family_id in enumerate(active_families)
    ]
    summaries = build_family_summaries(records)
    dequantized_count = sum(1 for record in records if record.verdict.startswith("dequantized"))
    return {
        "id": "LEARNABILITY-BASELINES-LATEST",
        "created_at": utc_now(),
        "kind": "hidden-shift-learnability-baselines",
        "status": "blocked-by-low-degree-learnability" if dequantized_count else "needs-stronger-learnability-tests",
        "families": active_families,
        "n_values": active_n,
        "record_count": len(records),
        "summary": (
            f"Ran {len(records)} low-degree learnability audits over {len(active_families)} families and {len(active_n)} n-values; "
            f"{dequantized_count} records are low-degree dequantized."
        ),
        "headline_metrics": {
            "low_degree_dequantized_count": dequantized_count,
            "not_low_degree_count": sum(1 for record in records if record.verdict == "not-low-degree-under-current-tests"),
            "suspect_low_degree_count": sum(1 for record in records if "suspect" in record.verdict),
        },
        "family_summaries": [asdict(summary) for summary in summaries],
        "records": [asdict(record) for record in records],
    }


def build_family_summaries(records: Sequence[LearnabilityRecord]) -> list[LearnabilityFamilySummary]:
    by_family: dict[str, list[LearnabilityRecord]] = {}
    for record in records:
        by_family.setdefault(record.family_id, []).append(record)
    summaries = []
    for family_id, items in sorted(by_family.items()):
        dequantized_count = sum(1 for item in items if item.verdict.startswith("dequantized"))
        unresolved_count = len(items) - dequantized_count
        if dequantized_count:
            best_verdict = "reject-low-degree-learnable-family"
            lesson = "Do not use this family as hidden-shift evidence unless the low-degree evaluator model is formally illegal."
        else:
            best_verdict = "not-low-degree-under-current-tests"
            lesson = "Continue with stronger reconstruction attacks; absence of low-degree evidence is not a lower bound."
        summaries.append(
            LearnabilityFamilySummary(
                family_id=family_id,
                tested_n_bits=sorted({item.n_bits for item in items}),
                dequantized_low_degree_count=dequantized_count,
                high_degree_or_unresolved_count=unresolved_count,
                best_verdict=best_verdict,
                lesson=lesson,
            )
        )
    return summaries


def write_learnability_report(
    output_path: Path = LEARNABILITY_REPORT_PATH,
    families: Sequence[str] | None = None,
    n_values: Sequence[int] | None = None,
    samples: int = 128,
    seed: int = 0,
    write_registry: bool = True,
) -> dict[str, Any]:
    payload = build_learnability_report(families=families, n_values=n_values, samples=samples, seed=seed)
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
                "row_count": payload["record_count"],
                "artifacts": {"learnability_baselines": str(output_path)},
                "headline_metrics": payload["headline_metrics"],
            }
        )
        write_negative_results_from_learnability(payload)
    return payload


def write_negative_results_from_learnability(payload: dict[str, Any]) -> int:
    written = 0
    for summary in payload.get("family_summaries", []):
        if summary.get("dequantized_low_degree_count", 0) <= 0:
            continue
        upsert_negative_result(
            NegativeResultRecord(
                id=f"LEARNABILITY-DEQUANTIZED-{summary['family_id'].upper()}",
                source="learnability_baselines.py",
                claim=f"{summary['family_id']} is a viable hidden-shift family despite low-degree structure.",
                reason_invalid=f"{summary['dequantized_low_degree_count']} learnability audit record(s) identify low-degree classical reconstruction pressure.",
                lesson=summary["lesson"],
                applies_to=["DHS-GOWERS-SIEVE", "HYP-LIT-HIDDEN-SHIFT-SIEVE", "PO-DEQUANTIZATION", "PO-FALSIFIERS"],
                evidence={
                    "family_id": summary["family_id"],
                    "tested_n_bits": summary["tested_n_bits"],
                    "best_verdict": summary["best_verdict"],
                },
            )
        )
        written += 1
    return written

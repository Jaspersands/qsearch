"""Sparse Fourier and derivative-spectrum dequantization baselines.

Low-degree tests are not enough.  Many hidden-shift families that avoid exact
polynomial reconstruction can still be classically vulnerable if the base phase
or a small set of derivatives has concentrated Fourier mass.  This module turns
that suspicion into a registry artifact: it reports exact full-table spectra,
query estimates for sparse Fourier/Goldreich-Levin style learners, sample
budget legality, and negative results when the learner is polynomial under a
legal access model.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Sequence

import numpy as np

from phase_state_workbench import (
    PhaseFamilySpec,
    generate_cyclic_phase_family,
    shifted_index,
    walsh_hadamard_complex,
)
from research_registry import NegativeResultRecord, upsert_negative_result, upsert_scaling_run, utc_now


FOURIER_BASELINE_DIR = Path("research/classical_baselines")
FOURIER_COMPRESSIBILITY_REPORT_PATH = FOURIER_BASELINE_DIR / "fourier_compressibility_baselines.json"


@dataclass(frozen=True)
class SpectrumCompressionProfile:
    transform: str
    entropy_bits: float
    normalized_entropy: float
    support_90_percent: int
    support_99_percent: int
    top_mass: float
    top_8_mass: float
    inverse_participation_ratio: float
    sparse_recovery_query_estimate: int
    compressibility_class: str


@dataclass(frozen=True)
class FourierCompressibilityRow:
    family_id: str
    n_bits: int
    group: str
    domain_size: int
    sample_count: int
    base_profile: SpectrumCompressionProfile
    derivative_shift_count: int
    derivative_best_shift: int
    derivative_best_profile: SpectrumCompressionProfile
    derivative_median_support_99: float
    derivative_median_entropy_bits: float
    best_sparse_query_estimate: int
    full_table_compressible: bool
    explicit_evaluator_sparse_recovery: bool
    random_sample_sparse_recovery: bool
    attack_legal_query_models: list[str]
    verdict: str
    notes: str


@dataclass(frozen=True)
class FourierFamilySummary:
    family_id: str
    tested_n_bits: list[int]
    tested_sample_counts: list[int]
    explicit_evaluator_sparse_recovery_count: int
    random_sample_sparse_recovery_count: int
    full_table_compressible_count: int
    derivative_sparse_count: int
    best_verdict: str
    lesson: str


def _poly_query_threshold(n_bits: int) -> int:
    return max(64, int(n_bits) ** 4)


def _support_for_mass(probabilities: np.ndarray, mass: float) -> int:
    ordered = np.sort(probabilities)[::-1]
    return int(np.searchsorted(np.cumsum(ordered), mass) + 1)


def _group_spectrum_power(spec: PhaseFamilySpec, signal: Sequence[complex]) -> tuple[str, np.ndarray]:
    values = np.asarray(signal, dtype=complex)
    if spec.group == "F2^n":
        spectrum = walsh_hadamard_complex(values) / math.sqrt(values.size)
        transform = "walsh-hadamard-F2n"
    elif spec.group == "F_p^2":
        prime = int(spec.modulus)
        spectrum = np.fft.fft2(values.reshape((prime, prime))).reshape(values.size) / math.sqrt(values.size)
        transform = "two-dimensional-fft-Fp2"
    else:
        spectrum = np.fft.fft(values) / math.sqrt(values.size)
        transform = "cyclic-fft-Zp"

    power = np.abs(spectrum) ** 2
    total = float(power.sum())
    if total <= 0:
        raise ValueError("signal has zero Fourier power")
    return transform, power / total


def spectrum_compression_profile(spec: PhaseFamilySpec, signal: Sequence[complex]) -> SpectrumCompressionProfile:
    transform, probabilities = _group_spectrum_power(spec, signal)
    nonzero = probabilities[probabilities > 1e-15]
    entropy = float(-np.sum(nonzero * np.log2(nonzero))) if nonzero.size else 0.0
    log_domain = max(1.0, math.log2(max(2, spec.domain_size)))
    ordered = np.sort(probabilities)[::-1]
    support_90 = _support_for_mass(probabilities, 0.90)
    support_99 = _support_for_mass(probabilities, 0.99)
    top_mass = float(ordered[0]) if ordered.size else 0.0
    top_8_mass = float(np.sum(ordered[: min(8, ordered.size)])) if ordered.size else 0.0
    ipr = float(1.0 / max(float(np.sum(probabilities**2)), 1e-15))

    sparse_query_estimate = int(
        math.ceil(
            max(
                support_90 * log_domain,
                log_domain / max(top_mass, 1e-12),
            )
        )
    )

    poly_support = max(8, spec.n_bits**2)
    if support_99 <= 1:
        compressibility = "one-sparse"
    elif support_99 <= poly_support:
        compressibility = "poly-sparse"
    elif support_99 <= max(poly_support, int(math.sqrt(spec.domain_size))):
        compressibility = "sublinear-compressible"
    else:
        compressibility = "broad"

    return SpectrumCompressionProfile(
        transform=transform,
        entropy_bits=entropy,
        normalized_entropy=float(entropy / log_domain),
        support_90_percent=support_90,
        support_99_percent=support_99,
        top_mass=top_mass,
        top_8_mass=top_8_mass,
        inverse_participation_ratio=ipr,
        sparse_recovery_query_estimate=sparse_query_estimate,
        compressibility_class=compressibility,
    )


def _default_derivative_shifts(spec: PhaseFamilySpec) -> list[int]:
    if spec.group == "F2^n":
        basis = [1 << bit for bit in range(spec.n_bits)]
        mixed = [3, 5, 9, 17, (1 << max(1, spec.n_bits // 2)) + 1]
        return sorted({shift for shift in basis + mixed if 0 < shift < spec.domain_size})
    if spec.group == "F_p^2":
        prime = int(spec.modulus)
        shifts = [1, prime, prime + 1, 2 * prime + 1, prime + 2, 2 * prime + 3]
        return [shift for shift in shifts if 0 < shift < spec.domain_size]
    base = [1, 2, 3, 5, 8, 13, 21, 34]
    return [shift for shift in base if 0 < shift < spec.domain_size]


def _derivative_signal(spec: PhaseFamilySpec, signal: Sequence[complex], shift: int) -> np.ndarray:
    values = np.asarray(signal, dtype=complex)
    shift = int(shift)
    if spec.group == "F2^n":
        return np.array([np.conjugate(values[x]) * values[x ^ shift] for x in range(spec.domain_size)], dtype=complex)
    if spec.group == "F_p^2":
        return np.array(
            [np.conjugate(values[x]) * values[shifted_index(spec, x, shift)] for x in range(spec.domain_size)],
            dtype=complex,
        )
    return np.conjugate(values) * np.roll(values, -shift % spec.domain_size)


def _profile_is_poly_sparse(profile: SpectrumCompressionProfile, n_bits: int) -> bool:
    return profile.compressibility_class in {"one-sparse", "poly-sparse"} and (
        profile.sparse_recovery_query_estimate <= _poly_query_threshold(n_bits)
    )


def audit_family_fourier_compressibility(
    family_id: str,
    n_bits: int,
    sample_count: int,
) -> FourierCompressibilityRow:
    spec, signal = generate_cyclic_phase_family(family_id, n_bits=n_bits)
    base_profile = spectrum_compression_profile(spec, signal)

    derivative_profiles: list[tuple[int, SpectrumCompressionProfile]] = []
    for shift in _default_derivative_shifts(spec):
        derivative_profiles.append((shift, spectrum_compression_profile(spec, _derivative_signal(spec, signal, shift))))

    if not derivative_profiles:
        raise ValueError(f"no derivative shifts available for {spec.id}")

    best_shift, best_derivative = min(
        derivative_profiles,
        key=lambda item: (
            item[1].sparse_recovery_query_estimate,
            item[1].support_99_percent,
            -item[1].top_mass,
        ),
    )
    best_query = min(base_profile.sparse_recovery_query_estimate, best_derivative.sparse_recovery_query_estimate)
    full_table_compressible = base_profile.compressibility_class != "broad" or best_derivative.compressibility_class != "broad"
    explicit_recovery = _profile_is_poly_sparse(base_profile, spec.n_bits) or _profile_is_poly_sparse(best_derivative, spec.n_bits)
    random_recovery = explicit_recovery and int(sample_count) >= best_query

    legal_models = ["full_table"] if full_table_compressible else []
    if explicit_recovery:
        legal_models.append("explicit_evaluator")
    if random_recovery:
        legal_models.append("random_sample")

    derivative_supports = [profile.support_99_percent for _shift, profile in derivative_profiles]
    derivative_entropies = [profile.entropy_bits for _shift, profile in derivative_profiles]

    if random_recovery:
        verdict = "dequantized-by-sample-sparse-fourier"
        notes = (
            f"Sample_count={sample_count} reaches estimated sparse-recovery query budget {best_query}; "
            "sample-limited Fourier/derivative learning is a live dequantization attack."
        )
    elif explicit_recovery:
        verdict = "dequantized-by-evaluator-sparse-fourier"
        notes = (
            f"Exact spectrum exposes a poly-query sparse Fourier or derivative learner with budget {best_query}; "
            "random samples at this budget may still be insufficient."
        )
    elif full_table_compressible:
        verdict = "full-table-spectral-compressibility"
        notes = "The full table has spectral concentration, but implemented query estimates are not polynomial under legal sparse-learning access."
    else:
        verdict = "spectrally-unresolved"
        notes = "No sparse Fourier or derivative-spectrum learner is certified by the implemented compressibility tests."

    return FourierCompressibilityRow(
        family_id=spec.id,
        n_bits=spec.n_bits,
        group=spec.group,
        domain_size=spec.domain_size,
        sample_count=int(sample_count),
        base_profile=base_profile,
        derivative_shift_count=len(derivative_profiles),
        derivative_best_shift=int(best_shift),
        derivative_best_profile=best_derivative,
        derivative_median_support_99=float(np.median(derivative_supports)),
        derivative_median_entropy_bits=float(np.median(derivative_entropies)),
        best_sparse_query_estimate=int(best_query),
        full_table_compressible=bool(full_table_compressible),
        explicit_evaluator_sparse_recovery=bool(explicit_recovery),
        random_sample_sparse_recovery=bool(random_recovery),
        attack_legal_query_models=legal_models,
        verdict=verdict,
        notes=notes,
    )


def build_fourier_compressibility_report(
    families: Sequence[str] | None = None,
    n_values: Sequence[int] | None = None,
    sample_counts: Sequence[int] | None = None,
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
    active_samples = list(sample_counts) if sample_counts is not None else [4, 8, 16, 32, 64, 128]

    rows = [
        audit_family_fourier_compressibility(family_id, n_bits, sample_count)
        for n_bits in active_n
        for family_id in active_families
        for sample_count in active_samples
    ]
    summaries = build_family_summaries(rows)
    evaluator_count = sum(1 for row in rows if row.explicit_evaluator_sparse_recovery)
    random_count = sum(1 for row in rows if row.random_sample_sparse_recovery)

    return {
        "id": "FOURIER-COMPRESSIBILITY-BASELINES-LATEST",
        "created_at": utc_now(),
        "kind": "hidden-shift-fourier-compressibility-baselines",
        "families": active_families,
        "n_values": active_n,
        "sample_counts": active_samples,
        "status": "blocked-by-spectral-compressibility" if evaluator_count else "needs-stronger-spectral-learners",
        "row_count": len(rows),
        "summary": (
            f"Ran {len(rows)} sparse Fourier and derivative-spectrum audits over {len(active_families)} families, "
            f"{len(active_n)} n-values, and {len(active_samples)} sample budgets; "
            f"{evaluator_count} rows are evaluator-sparse dequantized."
        ),
        "headline_metrics": {
            "explicit_evaluator_sparse_recovery_count": evaluator_count,
            "random_sample_sparse_recovery_count": random_count,
            "full_table_compressible_count": sum(1 for row in rows if row.full_table_compressible),
            "derivative_sparse_count": sum(
                1 for row in rows if row.derivative_best_profile.compressibility_class in {"one-sparse", "poly-sparse"}
            ),
            "spectrally_unresolved_count": sum(1 for row in rows if row.verdict == "spectrally-unresolved"),
        },
        "family_summaries": [asdict(summary) for summary in summaries],
        "rows": [asdict(row) for row in rows],
    }


def build_family_summaries(rows: Sequence[FourierCompressibilityRow]) -> list[FourierFamilySummary]:
    by_family: dict[str, list[FourierCompressibilityRow]] = {}
    for row in rows:
        by_family.setdefault(row.family_id, []).append(row)

    summaries: list[FourierFamilySummary] = []
    for family_id, family_rows in sorted(by_family.items()):
        evaluator_count = sum(1 for row in family_rows if row.explicit_evaluator_sparse_recovery)
        random_count = sum(1 for row in family_rows if row.random_sample_sparse_recovery)
        full_table_count = sum(1 for row in family_rows if row.full_table_compressible)
        derivative_count = sum(
            1 for row in family_rows if row.derivative_best_profile.compressibility_class in {"one-sparse", "poly-sparse"}
        )
        if random_count:
            verdict = "reject-sample-sparse-fourier"
            lesson = "Sample-limited sparse Fourier or derivative learning is enough to demote this family under tested budgets."
        elif evaluator_count:
            verdict = "reject-evaluator-sparse-fourier"
            lesson = "A polynomial-query evaluator learner is a dequantization route unless the input model formally excludes it."
        elif full_table_count:
            verdict = "full-table-compressible-needs-access-model"
            lesson = "Spectral concentration exists only under full-table evidence so far; clarify legal access and increase sampled tests."
        else:
            verdict = "spectrally-unresolved"
            lesson = "Current spectral learners did not certify recovery; this is not a lower bound."

        summaries.append(
            FourierFamilySummary(
                family_id=family_id,
                tested_n_bits=sorted({row.n_bits for row in family_rows}),
                tested_sample_counts=sorted({row.sample_count for row in family_rows}),
                explicit_evaluator_sparse_recovery_count=evaluator_count,
                random_sample_sparse_recovery_count=random_count,
                full_table_compressible_count=full_table_count,
                derivative_sparse_count=derivative_count,
                best_verdict=verdict,
                lesson=lesson,
            )
        )
    return summaries


def write_fourier_compressibility_report(
    output_path: Path = FOURIER_COMPRESSIBILITY_REPORT_PATH,
    families: Sequence[str] | None = None,
    n_values: Sequence[int] | None = None,
    sample_counts: Sequence[int] | None = None,
    write_registry: bool = True,
) -> dict[str, Any]:
    payload = build_fourier_compressibility_report(
        families=families,
        n_values=n_values,
        sample_counts=sample_counts,
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
                "row_count": payload["row_count"],
                "artifacts": {"fourier_compressibility_baselines": str(output_path)},
                "headline_metrics": payload["headline_metrics"],
            }
        )
        write_negative_results_from_fourier_compressibility(payload)
    return payload


def write_negative_results_from_fourier_compressibility(payload: dict[str, Any]) -> int:
    written = 0
    for summary in payload.get("family_summaries", []):
        if summary.get("explicit_evaluator_sparse_recovery_count", 0) <= 0 and summary.get("random_sample_sparse_recovery_count", 0) <= 0:
            continue
        upsert_negative_result(
            NegativeResultRecord(
                id=f"FOURIER-COMPRESSIBILITY-DEQUANTIZED-{summary['family_id'].upper()}",
                source="fourier_compressibility_baselines.py",
                claim=f"{summary['family_id']} remains a viable hidden-shift family after sparse Fourier and derivative-spectrum attacks.",
                reason_invalid=(
                    f"{summary['explicit_evaluator_sparse_recovery_count']} evaluator-sparse row(s) and "
                    f"{summary['random_sample_sparse_recovery_count']} sample-sparse row(s) identify a dequantization route."
                ),
                lesson=summary["lesson"],
                applies_to=["DHS-GOWERS-SIEVE", "HYP-LIT-HIDDEN-SHIFT-SIEVE", "PO-DEQUANTIZATION", "PO-FALSIFIERS"],
                evidence={
                    "family_id": summary["family_id"],
                    "tested_n_bits": summary["tested_n_bits"],
                    "tested_sample_counts": summary["tested_sample_counts"],
                    "best_verdict": summary["best_verdict"],
                },
            )
        )
        written += 1
    return written

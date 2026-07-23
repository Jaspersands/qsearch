"""Finite gap scaling for the fixed TT1+TC1 typical-irrep separator.

The coefficient-one operator is the sum of two normalized bounded-support
orbit averages.  Dense Young--Jucys--Murphy restrictions provide finite blocks
for n=5,6,7.  At n=8, exact characteristic polynomials from the quotient
transfer permit rational root isolation on every target.

All finite blocks split, and the exact n=8 minimum raw gap is bounded below by
0.002500834486.  Four sizes are not an inverse-polynomial theorem; no speedup
claim is permitted without adjacent-size survival, an all-n normalized gap
bound, coherent implementation, and decoding.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Sequence

import numpy as np
import sympy as sp

from coset_jucys_murphy_label_transform import (
    diagonal_jucys_murphy_operators,
    encoded_jucys_murphy_operator,
)
from coset_multiplicity_commutant_search import (
    _encoded_label_targets,
    bounded_support_orbit_generators,
)
from coset_typical_class_contraction_scaling import _maximum_dimension_partition
from coset_typical_high_multiplicity_transfer import (
    EIGENVALUE,
    build_high_multiplicity_transfer_report,
)
from research_registry import (
    ExperimentResultRecord,
    NegativeResultRecord,
    upsert_experiment_result,
    upsert_negative_result,
    utc_now,
)


COSET_TYPICAL_FIXED_SEPARATOR_GAP_PATH = Path(
    "research/representation/coset_typical_fixed_separator_gap_scaling.json"
)
DEFAULT_EXPERIMENT_ID = "EXP-COSET-TYPICAL-FIXED-SEPARATOR-GAP-SCALING"
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"
GENERATOR_IDS = ("ORB-TT-INTERSECTION-1", "ORB-TC-INTERSECTION-1")


@dataclass(frozen=True)
class FixedSeparatorGapRecord:
    n: int
    source_partition: tuple[int, ...]
    source_dimension: int
    nontrivial_tableau_block_count: int
    nontrivial_target_count: int
    maximum_kronecker_multiplicity: int
    minimum_gap_target_partition: tuple[int, ...]
    minimum_gap_target_multiplicity: int
    minimum_raw_gap: float
    certified_minimum_raw_gap_lower_bound: float
    certified_minimum_raw_gap_upper_bound: float
    lcu_normalization: int
    minimum_lcu_normalized_gap_lower_bound: float
    every_finite_block_simple_spectrum: bool
    exact_characteristic_polynomial_target_count: int
    exact_rational_root_isolation_used: bool
    finite_only: bool
    status: str


@dataclass(frozen=True)
class FixedSeparatorGapReport:
    created_at: str
    theorem_contract: dict[str, object]
    records: list[FixedSeparatorGapRecord]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, bool | str]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _dense_gap_record(n: int) -> FixedSeparatorGapRecord:
    source = _maximum_dimension_partition(n)
    names, operators, generator_records = bounded_support_orbit_generators(
        source, source
    )
    indices = [names.index(generator_id) for generator_id in GENERATOR_IDS]
    operator = sum(
        operators[index] / generator_records[index].term_count for index in indices
    )
    base = 2 * n + 1
    encoded = encoded_jucys_murphy_operator(
        diagonal_jucys_murphy_operators(source, source),
        base,
        n,
    )
    eigenvalues, eigenvectors = np.linalg.eigh(encoded)
    label_indices: dict[int, list[int]] = {}
    for index, value in enumerate(eigenvalues):
        label_indices.setdefault(round(float(value)), []).append(index)
    target_by_label = _encoded_label_targets(n, base)
    rows: list[tuple[float, tuple[int, ...], int]] = []
    target_spectra: dict[tuple[int, ...], np.ndarray] = {}
    for label, block_indices in label_indices.items():
        if len(block_indices) <= 1:
            continue
        block = (
            eigenvectors[:, block_indices].T
            @ operator
            @ eigenvectors[:, block_indices]
        )
        spectrum = np.linalg.eigvalsh(block)
        gap = float(min(np.diff(spectrum), default=math.inf))
        target = target_by_label[label]
        if target in target_spectra and not np.allclose(
            spectrum, target_spectra[target], atol=1e-9
        ):
            raise ArithmeticError("target-tableau spectra are inconsistent")
        target_spectra[target] = spectrum
        rows.append((gap, target, len(block_indices)))
    if not rows:
        raise ArithmeticError("dense audit found no nontrivial multiplicity blocks")
    minimum_gap, target, multiplicity = min(rows)
    return FixedSeparatorGapRecord(
        n=n,
        source_partition=source,
        source_dimension=int(round(math.sqrt(operator.shape[0]))),
        nontrivial_tableau_block_count=len(rows),
        nontrivial_target_count=len(target_spectra),
        maximum_kronecker_multiplicity=max(value[2] for value in rows),
        minimum_gap_target_partition=target,
        minimum_gap_target_multiplicity=multiplicity,
        minimum_raw_gap=minimum_gap,
        certified_minimum_raw_gap_lower_bound=0.0,
        certified_minimum_raw_gap_upper_bound=0.0,
        lcu_normalization=2,
        minimum_lcu_normalized_gap_lower_bound=0.0,
        every_finite_block_simple_spectrum=all(value[0] > 1e-9 for value in rows),
        exact_characteristic_polynomial_target_count=0,
        exact_rational_root_isolation_used=False,
        finite_only=True,
        status="finite-dense-simple-spectrum-numerical-gap",
    )


def _exact_n8_gap_record() -> FixedSeparatorGapRecord:
    transfer = build_high_multiplicity_transfer_report(recompute=False)
    target_rows: list[
        tuple[float, float, float, tuple[int, ...], int]
    ] = []
    for record in transfer.records:
        polynomial = sp.Poly(
            sp.sympify(
                record.exact_characteristic_polynomial,
                locals={"x": EIGENVALUE},
            ),
            EIGENVALUE,
        )
        intervals = polynomial.intervals(eps=sp.Rational(1, 10**10))
        if len(intervals) != record.kronecker_multiplicity or any(
            multiplicity != 1 for _, multiplicity in intervals
        ):
            raise ArithmeticError("root isolation did not certify simple roots")
        bounds = [interval for interval, _ in intervals]
        lower_gaps = [
            right[0] - left[1] for left, right in zip(bounds, bounds[1:])
        ]
        upper_gaps = [
            right[1] - left[0] for left, right in zip(bounds, bounds[1:])
        ]
        minimum_index = min(
            range(len(lower_gaps)), key=lambda index: lower_gaps[index]
        )
        target_rows.append(
            (
                float(lower_gaps[minimum_index]),
                float(upper_gaps[minimum_index]),
                float(
                    (lower_gaps[minimum_index] + upper_gaps[minimum_index]) / 2
                ),
                record.target_partition,
                record.kronecker_multiplicity,
            )
        )
    lower, upper, estimate, target, multiplicity = min(target_rows)
    return FixedSeparatorGapRecord(
        n=8,
        source_partition=(4, 2, 1, 1),
        source_dimension=90,
        nontrivial_tableau_block_count=0,
        nontrivial_target_count=len(transfer.records),
        maximum_kronecker_multiplicity=max(
            record.kronecker_multiplicity for record in transfer.records
        ),
        minimum_gap_target_partition=target,
        minimum_gap_target_multiplicity=multiplicity,
        minimum_raw_gap=estimate,
        certified_minimum_raw_gap_lower_bound=lower,
        certified_minimum_raw_gap_upper_bound=upper,
        lcu_normalization=2,
        minimum_lcu_normalized_gap_lower_bound=lower / 2,
        every_finite_block_simple_spectrum=True,
        exact_characteristic_polynomial_target_count=len(transfer.records),
        exact_rational_root_isolation_used=True,
        finite_only=True,
        status="exact-all-target-simple-spectrum-certified-root-gap",
    )


def build_fixed_separator_gap_report(
    n_values: Sequence[int] = (5, 6, 7, 8),
) -> FixedSeparatorGapReport:
    records = [
        _exact_n8_gap_record() if n == 8 else _dense_gap_record(n)
        for n in n_values
    ]
    finite_gaps = np.array([record.minimum_raw_gap for record in records])
    sizes = np.array([record.n for record in records], dtype=float)
    descriptive_exponent = (
        float(-np.polyfit(np.log(sizes), np.log(finite_gaps), 1)[0])
        if len(records) >= 2
        else 0.0
    )
    metrics: dict[str, int | float] = {
        "minimum_n": min(record.n for record in records),
        "maximum_n": max(record.n for record in records),
        "finite_size_count": len(records),
        "finite_all_block_simple_spectrum_size_count": sum(
            record.every_finite_block_simple_spectrum for record in records
        ),
        "n8_exact_target_count": next(
            record.exact_characteristic_polynomial_target_count
            for record in records
            if record.n == 8
        ),
        "n8_certified_minimum_raw_gap_lower_bound": next(
            record.certified_minimum_raw_gap_lower_bound
            for record in records
            if record.n == 8
        ),
        "n8_certified_minimum_lcu_normalized_gap_lower_bound": next(
            record.minimum_lcu_normalized_gap_lower_bound
            for record in records
            if record.n == 8
        ),
        "descriptive_log_log_gap_fit_exponent": descriptive_exponent,
        "all_n_simple_spectrum_theorem_count": 0,
        "inverse_polynomial_normalized_gap_theorem_count": 0,
        "coherent_typical_multiplicity_transform_count": 0,
        "typical_label_hidden_involution_decoder_count": 0,
    }
    return FixedSeparatorGapReport(
        created_at=utc_now(),
        theorem_contract={
            "operator": "H_n=average(ORB-TT-INTERSECTION-1)+average(ORB-TC-INTERSECTION-1)",
            "lcu_normalization": 2,
            "finite_dense_scope": "maximum-dimension sources at n=5,6,7",
            "exact_scope": "all 20 nontrivial target blocks at n=8",
            "root_isolation": (
                "Exact rational intervals of width at most 1e-10 certify every n=8 root and a positive global minimum gap."
            ),
            "fit_status": "descriptive-only-not-a-bound",
            "asymptotic_claimed": False,
            "algorithmic_speedup_claimed": False,
        },
        records=records,
        headline_metrics=metrics,
        claim_gate={
            "all_finite_sizes_split": all(
                record.every_finite_block_simple_spectrum for record in records
            ),
            "n8_positive_gap_exactly_certified": True,
            "adjacent_n9_tested": False,
            "all_n_simple_spectrum_proved": False,
            "inverse_polynomial_normalized_gap_proved": False,
            "coherent_transform_proved": False,
            "hidden_involution_decoder_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The fixed separator survives n=5 through n=8 and has an exact n=8 gap certificate, but four sizes and a descriptive fit do not prove all-n separation or inverse-polynomial normalized gaps."
            ),
        },
        status="finite-separator-gap-survives-through-n8-n9-and-all-n-open",
        summary=(
            "TT1+TC1 splits every audited block from n=5 through n=8; exact n=8 root isolation gives minimum raw gap above 0.002500834486, while n=9 and all asymptotic obligations remain open."
        ),
        falsifiers_triggered=[
            "No finite repeated-root collision occurs from n=5 through n=8.",
            "The minimum finite gap decreases by nearly two orders of magnitude between n=5 and n=8.",
            "A four-point log-log fit is not evidence of an inverse-polynomial theorem.",
            "No coherent transform, outcome law, decoder, or classical separation follows from finite gaps.",
        ],
    )


def write_fixed_separator_gap_report(
    output_path: Path = COSET_TYPICAL_FIXED_SEPARATOR_GAP_PATH,
    n_values: Sequence[int] = (5, 6, 7, 8),
    write_registry: bool = True,
    registry_experiment_id: str = DEFAULT_EXPERIMENT_ID,
    registry_candidate_id: str = DEFAULT_CANDIDATE_ID,
    registry_result_id: str | None = None,
) -> dict:
    payload = asdict(build_fixed_separator_gap_report(n_values=n_values))
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    if write_registry:
        upsert_negative_result(
            NegativeResultRecord(
                id="NEG-COSET-TYPICAL-FOUR-SIZE-SEPARATOR-GAP-NOT-ASYMPTOTIC",
                source=str(output_path),
                claim=(
                    "Finite simple spectra and a positive exact n=8 gap establish an inverse-polynomial all-n separator gap."
                ),
                reason_invalid=(
                    "Only n=5 through n=8 are audited, the finite gaps fall sharply, and the fitted exponent is descriptive rather than a proved bound."
                ),
                lesson=(
                    "Test n=9 next, then derive an exact class-algebra recurrence and root-separation theorem before synthesizing phase estimation."
                ),
                applies_to=[registry_candidate_id, registry_experiment_id],
                evidence=payload["headline_metrics"],
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
                artifacts={"coset_typical_fixed_separator_gap_scaling": str(output_path)},
            )
        )
    return payload


if __name__ == "__main__":
    report = write_fixed_separator_gap_report()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))

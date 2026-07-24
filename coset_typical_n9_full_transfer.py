"""Exact all-target n=9 certificate for the fixed TT1+TC1 separator.

The degree-28 simultaneous-conjugacy transfer and class-Fourier character
contraction recover every power trace needed for all 27 nontrivial
Kronecker-multiplicity targets of the n=9 source (4,3,1,1).  Every exact
characteristic polynomial is square-free at coefficient one.

This is a complete finite n=9 separator theorem.  It is not an all-n gap
theorem, a coherent multiplicity transform, a hidden-involution decoder, or a
quantum speedup.
"""

from __future__ import annotations

import hashlib
import json
import tempfile
from dataclasses import asdict, dataclass
from fractions import Fraction
from pathlib import Path

import sympy as sp

from coset_typical_high_multiplicity_transfer import (
    EIGENVALUE,
    TRANSFER_KERNEL_PATH,
    run_exact_transfer_kernel,
)
from coset_typical_n9_low_multiplicity_probe import (
    N,
    SOURCE_PARTITION,
    _characteristic_polynomial,
    _exact_translation_contraction,
)
from representation_obstruction import hook_length_dimension, integer_partitions
from research_registry import (
    ExperimentResultRecord,
    NegativeResultRecord,
    upsert_experiment_result,
    upsert_negative_result,
    utc_now,
)
from symmetric_character import kronecker_coefficient


COSET_TYPICAL_N9_FULL_CERTIFICATE_PATH = Path(
    "research/certificates/coset_typical_n9_full_transfer_certificate.json"
)
COSET_TYPICAL_N9_FULL_TRANSFER_PATH = Path(
    "research/representation/coset_typical_n9_full_transfer.json"
)
DEFAULT_EXPERIMENT_ID = "EXP-COSET-TYPICAL-N9-FULL-TRANSFER"
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"
NONTRIVIAL_TARGET_COUNT = 27
MAXIMUM_MULTIPLICITY = 28
TRANSFER_STATE_COUNTS = {
    1: 2,
    2: 87,
    3: 2070,
    4: 26062,
    5: 78328,
    6: 148830,
    7: 189168,
    **{
        degree: 189192 if degree % 2 == 0 else 189168
        for degree in range(8, 29)
    },
}


@dataclass(frozen=True)
class N9FullTargetRecord:
    target_partition: tuple[int, ...]
    target_dimension: int
    kronecker_multiplicity: int
    exact_power_traces: list[str]
    exact_characteristic_polynomial: str
    exact_square_free_gcd: str
    certified_minimum_raw_gap_lower_bound: float
    certified_minimum_raw_gap_upper_bound: float
    characteristic_polynomial_square_free: bool
    exact_transfer_recomputed: bool
    status: str


@dataclass(frozen=True)
class N9FullTransferReport:
    created_at: str
    theorem_contract: dict[str, object]
    records: list[N9FullTargetRecord]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, bool | str]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _target_specs() -> tuple[dict[str, object], ...]:
    specs = []
    for target in integer_partitions(N):
        multiplicity = kronecker_coefficient(
            SOURCE_PARTITION,
            SOURCE_PARTITION,
            target,
        )
        if multiplicity > 1:
            specs.append(
                {
                    "target": target,
                    "dimension": hook_length_dimension(target),
                    "multiplicity": multiplicity,
                }
            )
    return tuple(
        sorted(specs, key=lambda item: (item["multiplicity"], item["target"]))
    )


def _load_certificate(
    certificate_path: Path = COSET_TYPICAL_N9_FULL_CERTIFICATE_PATH,
) -> dict:
    resolved_certificate_path = certificate_path
    if not resolved_certificate_path.exists():
        resolved_certificate_path = Path(__file__).resolve().parent / certificate_path
    if not resolved_certificate_path.exists():
        raise FileNotFoundError(
            f"missing exact n=9 full-transfer certificate: {certificate_path}"
        )
    payload = json.loads(resolved_certificate_path.read_text())
    if (
        payload.get("n") != N
        or payload.get("maximum_degree") != MAXIMUM_MULTIPLICITY
        or len(payload.get("records", [])) != NONTRIVIAL_TARGET_COUNT
    ):
        raise ArithmeticError("invalid n=9 full-transfer certificate envelope")
    kernel_path = Path(__file__).resolve().parent / TRANSFER_KERNEL_PATH
    kernel_digest = hashlib.sha256(kernel_path.read_bytes()).hexdigest()
    if (
        payload.get("certificate_contract", {}).get("kernel_sha256")
        != kernel_digest
    ):
        raise ArithmeticError("n=9 certificate does not match the transfer kernel")
    return payload


def _validated_records(
    certificate: dict,
    recomputed_traces: dict[tuple[int, ...], tuple[Fraction, ...]] | None,
) -> list[N9FullTargetRecord]:
    expected_specs = _target_specs()
    certificate_rows = certificate["records"]
    records = []
    for spec, row in zip(expected_specs, certificate_rows):
        target = tuple(row["target"])
        if (
            target != spec["target"]
            or int(row["dimension"]) != spec["dimension"]
            or int(row["multiplicity"]) != spec["multiplicity"]
        ):
            raise ArithmeticError("certificate target ordering or multiplicity changed")
        traces = tuple(Fraction(value) for value in row["traces"])
        if recomputed_traces is not None and recomputed_traces[target] != traces:
            raise ArithmeticError(f"recomputed n=9 traces differ on {target}")
        polynomial = sp.Poly(_characteristic_polynomial(traces), EIGENVALUE)
        polynomial_text = str(sp.factor(polynomial.as_expr()))
        gcd = sp.gcd(polynomial, polynomial.diff())
        intervals = polynomial.intervals(eps=sp.Rational(1, 10**12))
        bounds = [interval for interval, _ in intervals]
        lower = min(
            right[0] - left[1] for left, right in zip(bounds, bounds[1:])
        )
        upper = min(
            right[1] - left[0] for left, right in zip(bounds, bounds[1:])
        )
        if (
            polynomial_text != row["characteristic_polynomial"]
            or str(gcd.as_expr()) != row["square_free_gcd"]
            or str(lower) != row["gap_lower"]
            or str(upper) != row["gap_upper"]
        ):
            raise ArithmeticError(f"stored polynomial certificate changed on {target}")
        square_free = gcd.degree() == 0 and all(
            multiplicity == 1 for _, multiplicity in intervals
        )
        if not square_free:
            raise ArithmeticError(f"exact repeated root found on n=9 target {target}")
        records.append(
            N9FullTargetRecord(
                target_partition=target,
                target_dimension=int(row["dimension"]),
                kronecker_multiplicity=int(row["multiplicity"]),
                exact_power_traces=[str(value) for value in traces],
                exact_characteristic_polynomial=polynomial_text,
                exact_square_free_gcd=str(gcd.as_expr()),
                certified_minimum_raw_gap_lower_bound=float(lower),
                certified_minimum_raw_gap_upper_bound=float(upper),
                characteristic_polynomial_square_free=True,
                exact_transfer_recomputed=recomputed_traces is not None,
                status="exact-n9-full-target-simple-spectrum",
            )
        )
    return records


def build_n9_full_transfer_report(
    recompute: bool = False,
) -> N9FullTransferReport:
    certificate = _load_certificate()
    recomputed_traces = None
    if recompute:
        distributions, _ = run_exact_transfer_kernel(
            max_degree=MAXIMUM_MULTIPLICITY,
            n=N,
            cache_path=Path(tempfile.gettempdir())
            / "qsearch-transfer"
            / "n9-degree28.tsv",
        )
        recomputed_traces = _exact_translation_contraction(
            distributions,
            _target_specs(),
        )
    records = _validated_records(certificate, recomputed_traces)
    weakest = min(
        records,
        key=lambda item: item.certified_minimum_raw_gap_lower_bound,
    )
    all_square_free = all(
        record.characteristic_polynomial_square_free for record in records
    )
    metrics: dict[str, int | float] = {
        "n": N,
        "maximum_exact_transfer_degree": MAXIMUM_MULTIPLICITY,
        "maximum_exact_transfer_state_count": max(TRANSFER_STATE_COUNTS.values()),
        "saturated_pair_state_union_count": 378360,
        "certified_n9_target_count": len(records),
        "certified_n9_simple_spectrum_target_count": sum(
            record.characteristic_polynomial_square_free for record in records
        ),
        "n9_nontrivial_multiplicity_target_count": NONTRIVIAL_TARGET_COUNT,
        "n9_unaudited_target_count": NONTRIVIAL_TARGET_COUNT - len(records),
        "maximum_certified_kronecker_multiplicity": max(
            record.kronecker_multiplicity for record in records
        ),
        "n9_exact_target_coverage_fraction": len(records)
        / NONTRIVIAL_TARGET_COUNT,
        "certified_n9_minimum_raw_gap_lower_bound": (
            weakest.certified_minimum_raw_gap_lower_bound
        ),
        "certified_n9_minimum_lcu_normalized_gap_lower_bound": (
            weakest.certified_minimum_raw_gap_lower_bound / 2
        ),
        "minimum_gap_target_multiplicity": weakest.kronecker_multiplicity,
        "conjugacy_class_count": 30,
        "class_fourier_amortized_target_count": len(records),
        "unique_left_translation_count": 3909,
        "unique_right_translation_count": 10755,
        "temporary_character_table_bytes": 7805548800,
        "maximum_in_memory_character_chunk_rows": 128,
        "maximum_in_memory_character_chunk_bytes": 92897280,
        "parallel_exact_transfer_count": 1,
        "kernel_hash_gated_transfer_cache_count": 1,
        "exact_transfer_recomputed_count": int(recompute),
        "all_n9_target_simple_spectrum_theorem_count": int(
            len(records) == NONTRIVIAL_TARGET_COUNT and all_square_free
        ),
        "all_n_simple_spectrum_theorem_count": 0,
        "inverse_polynomial_normalized_gap_theorem_count": 0,
        "coherent_typical_multiplicity_transform_count": 0,
        "typical_label_hidden_involution_decoder_count": 0,
    }
    return N9FullTransferReport(
        created_at=utc_now(),
        theorem_contract={
            "operator": "H_9=average(TT1)+average(TC1)",
            "source": "lambda=(4,3,1,1), dimension 216",
            "transfer": (
                "Exact arbitrary-precision simultaneous-conjugacy quotient through degree 28; state counts alternate between 189192 and 189168 after saturation."
            ),
            "contraction": (
                "Order S_9 rows by 30 conjugacy classes, reduce each left/right translation pair to 30 exact class sums, and amortize all 27 target-character contractions."
            ),
            "scope": (
                "All 27 nontrivial n=9 Kronecker-multiplicity targets through multiplicity 28 at fixed coefficient one."
            ),
            "all_n9_targets_claimed": True,
            "all_n_claimed": False,
            "algorithmic_speedup_claimed": False,
        },
        records=records,
        headline_metrics=metrics,
        claim_gate={
            "all_n9_targets_audited": True,
            "all_n9_targets_simple_spectrum": True,
            "all_n_simple_spectrum_proved": False,
            "inverse_polynomial_normalized_gap_proved": False,
            "coherent_transform_proved": False,
            "hidden_involution_decoder_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The fixed coefficient has exact simple spectrum on every n=9 block, but this remains a second finite size with no all-n gap, coherent implementation, hidden-involution outcome law, decoder, or classical separation."
            ),
        },
        status="fixed-coefficient-exactly-separates-all-n9-targets-asymptotic-obligations-open",
        summary=(
            "Exact degree-28 transfer and class-Fourier contraction prove TT1+TC1 has simple spectrum on all 27 nontrivial n=9 targets; the smallest certified raw gap is below 0.00043 and no speedup claim follows."
        ),
        falsifiers_triggered=[
            "No repeated root occurs on any n=9 target through multiplicity 28.",
            "The minimum certified raw gap falls below 0.00043 on a multiplicity-14 block.",
            "Two complete finite sizes do not establish all-n square-freeness or inverse-polynomial normalized gaps.",
            "No coherent transform, hidden-involution outcome law, decoder, or classical separation is supplied.",
        ],
    )


def write_n9_full_transfer_report(
    output_path: Path = COSET_TYPICAL_N9_FULL_TRANSFER_PATH,
    recompute: bool = False,
    write_registry: bool = True,
    registry_experiment_id: str = DEFAULT_EXPERIMENT_ID,
    registry_candidate_id: str = DEFAULT_CANDIDATE_ID,
    registry_result_id: str | None = None,
) -> dict:
    payload = asdict(build_n9_full_transfer_report(recompute=recompute))
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    if write_registry:
        upsert_negative_result(
            NegativeResultRecord(
                id="NEG-COSET-TYPICAL-N9-FULL-SEPARATION-NOT-ASYMPTOTIC-ALGORITHM",
                source=str(output_path),
                claim=(
                    "Exact separation of every n=8 and n=9 typical multiplicity block establishes an efficient uniform resolver."
                ),
                reason_invalid=(
                    "Only two finite sizes are complete; the n=9 minimum raw gap is below 0.00043, and all-n normalized-gap, coherent-transform, outcome-law, decoder, and classical-separation obligations remain open."
                ),
                lesson=(
                    "Derive an all-n class-algebra recurrence and normalized root bound before any circuit claim; otherwise search for the first collision or superpolynomial gap collapse at n>=10."
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
                artifacts={"coset_typical_n9_full_transfer": str(output_path)},
            )
        )
    return payload


if __name__ == "__main__":
    report = write_n9_full_transfer_report(recompute=True)
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))

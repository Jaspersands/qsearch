"""Lazy bridge-walk mixing for the natural moment word-map statistic.

For a random bridge sequence c_1,...,c_m, the all-order reduction defines

    a_m=2^-m(N_e+N_C/|C|).

Averaging over the bridge sequence is equivalent to the central lazy walk

    nu=(delta_e+uniform(C))/2

on W_n.  In physical irrep pi its eigenvalue is

    theta_pi=(1+chi_pi(h)/d_pi)/2.

The exact natural character law gives

    E[a_m]=sum_pi p_pi theta_pi^m.

Exactly two physical irreps have theta_pi=1: the plus extensions of the two
one-dimensional S_n irreps.  Their total natural mass is 2/(n!)^2.  Every
other sector has theta_pi<=3/4 because every remaining source dimension is at
least two.  Therefore

    2/(n!)^2 <= E[a_m]
      <= 2/(n!)^2 + (1-2/(n!)^2)(3/4)^m.

At the moment orders required by the sub-POVM certificate the mean is
essentially stationary.  This does not control E[a_m^k]: Jensen and
0<=a_m<=1 leave the wide interval E[a_m]^k <= E[a_m^k] <= E[a_m].
The missing theorem is concentration or a coupled-walk contraction.
"""

from __future__ import annotations

import itertools
import json
import math
from dataclasses import asdict, dataclass
from fractions import Fraction
from pathlib import Path
from typing import Any

from research_registry import (
    ExperimentResultRecord,
    NegativeResultRecord,
    upsert_experiment_result,
    upsert_negative_result,
    utc_now,
)
from self_dual_wreath_natural_moment_word_map import (
    natural_irrep_probability,
    physical_irrep_descriptors,
    word_map_single_label_factor,
)
from self_dual_wreath_pgm_polar_audit import (
    run_self_dual_wreath_pgm_polar_audit,
)


REPORT_PATH = Path(
    "research/representation/self_dual_wreath_word_map_mixing.json"
)
WREATH_PGM_PATH = Path(
    "research/representation/self_dual_wreath_pgm_polar_audit.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-WORD-MAP-MIXING"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


@dataclass(frozen=True)
class LazyWalkValidationRecord:
    n: int
    moment_order: int
    bridge_sequence_count: int
    direct_word_map_mean: str
    spectral_mean: str
    exact_match: bool


@dataclass(frozen=True)
class LazyWalkScalingRecord:
    n: int
    copy_count: int
    required_moment_order: int
    log2_stationary_mean: float
    log2_nonstationary_error_upper_bound: float
    log2_error_to_stationary_ratio_upper_bound: float
    log2_kth_moment_jensen_lower_bound: float
    log2_kth_moment_bounded_upper_bound: float
    log2_unresolved_kth_moment_interval_width: float
    single_walk_mean_mixed: bool
    coupled_k_walk_contraction_proved: bool
    word_map_concentration_proved: bool
    status: str


@dataclass(frozen=True)
class WreathWordMapMixingReport:
    created_at: str
    theorem_contract: dict[str, Any]
    validations: list[LazyWalkValidationRecord]
    scaling_records: list[LazyWalkScalingRecord]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, bool | str]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        payload = json.loads(path.read_text())
    except (json.JSONDecodeError, OSError):
        return {}
    return payload if isinstance(payload, dict) else {}


def exact_lazy_walk_spectral_mean(
    n: int,
    moment_order: int,
) -> Fraction:
    if moment_order < 0:
        raise ValueError("moment_order must be nonnegative")
    return sum(
        (
            natural_irrep_probability(descriptor)
            * Fraction(
                descriptor.dimension + descriptor.bridge_character,
                2 * descriptor.dimension,
            )
            ** moment_order
            for descriptor in physical_irrep_descriptors(n)
        ),
        Fraction(),
    )


def exact_direct_word_map_mean(
    n: int,
    moment_order: int,
) -> Fraction:
    permutations = tuple(itertools.permutations(range(n)))
    total = sum(
        (
            word_map_single_label_factor(sequence)
            for sequence in itertools.product(
                permutations,
                repeat=moment_order,
            )
        ),
        Fraction(),
    )
    return total / len(permutations) ** moment_order


def lazy_walk_validation(
    n: int,
    moment_order: int,
) -> LazyWalkValidationRecord:
    direct = exact_direct_word_map_mean(n, moment_order)
    spectral = exact_lazy_walk_spectral_mean(n, moment_order)
    return LazyWalkValidationRecord(
        n=n,
        moment_order=moment_order,
        bridge_sequence_count=math.factorial(n) ** moment_order,
        direct_word_map_mean=str(direct),
        spectral_mean=str(spectral),
        exact_match=direct == spectral,
    )


def _log2_add(left: float, right: float) -> float:
    high = max(left, right)
    low = min(left, right)
    if high == -math.inf:
        return high
    return high + math.log2(1 + 2 ** (low - high))


def scaling_record(
    n: int,
    copy_count: int,
    moment_order: int,
) -> LazyWalkScalingRecord:
    log2_hidden_labels = math.lgamma(n + 1) / math.log(2)
    stationary_log2 = 1 - 2 * log2_hidden_labels
    error_log2 = moment_order * math.log2(Fraction(3, 4))
    error_ratio_log2 = error_log2 - stationary_log2
    mean_upper_log2 = _log2_add(stationary_log2, error_log2)
    lower = copy_count * stationary_log2
    upper = mean_upper_log2
    return LazyWalkScalingRecord(
        n=n,
        copy_count=copy_count,
        required_moment_order=moment_order,
        log2_stationary_mean=stationary_log2,
        log2_nonstationary_error_upper_bound=error_log2,
        log2_error_to_stationary_ratio_upper_bound=error_ratio_log2,
        log2_kth_moment_jensen_lower_bound=lower,
        log2_kth_moment_bounded_upper_bound=upper,
        log2_unresolved_kth_moment_interval_width=upper - lower,
        single_walk_mean_mixed=error_ratio_log2 <= -20,
        coupled_k_walk_contraction_proved=False,
        word_map_concentration_proved=False,
        status="single-walk-mixed-kcoupled-concentration-open",
    )


def run_wreath_word_map_mixing() -> WreathWordMapMixingReport:
    validations = [
        lazy_walk_validation(n, order)
        for n, order in (
            (3, 1),
            (3, 2),
            (3, 3),
            (3, 4),
            (3, 5),
            (4, 1),
            (4, 2),
            (4, 3),
        )
    ]
    wreath = _read_json(WREATH_PGM_PATH)
    if not wreath:
        wreath = asdict(run_self_dual_wreath_pgm_polar_audit())
    scaling = [
        scaling_record(
            n=int(record["n"]),
            copy_count=int(record["copy_count"]),
            moment_order=math.ceil(
                float(record["log2_kcopy_hilbert_dimension"])
            ),
        )
        for record in wreath.get("records", [])
    ]
    failures = sum(not record.exact_match for record in validations)
    tail = scaling[-1]
    metrics: dict[str, int | float] = {
        "lazy_walk_validation_count": len(validations),
        "failed_lazy_walk_validation_count": failures,
        "maximum_validation_n": max(record.n for record in validations),
        "maximum_validation_moment_order": max(
            record.moment_order for record in validations
        ),
        "exact_stationary_mean_theorem_count": 1,
        "uniform_three_quarter_nonstationary_spectral_bound_count": 1,
        "single_walk_mean_mixing_theorem_count": 1,
        "tail_log2_stationary_mean": tail.log2_stationary_mean,
        "tail_log2_error_to_stationary_ratio_upper_bound": (
            tail.log2_error_to_stationary_ratio_upper_bound
        ),
        "tail_log2_unresolved_kth_moment_interval_width": (
            tail.log2_unresolved_kth_moment_interval_width
        ),
        "coupled_k_walk_contraction_count": 0,
        "word_map_concentration_theorem_count": 0,
        "growing_order_word_map_contraction_count": 0,
        "natural_average_inverse_polynomial_conclusive_theorem_count": 0,
        "structured_maximal_effect_dilation_count": 0,
        "polynomial_hidden_permutation_decoder_count": 0,
    }
    verified = failures == 0
    return WreathWordMapMixingReport(
        created_at=utc_now(),
        theorem_contract={
            "lazy_step": "nu=(delta_e+uniform(C))/2",
            "physical_sector_eigenvalue": (
                "theta_pi=(1+chi_pi(h)/d_pi)/2"
            ),
            "exact_mean": "E[a_m]=sum_pi p_pi theta_pi^m",
            "stationary_floor": (
                "exactly two plus one-dimensional sectors give 2/(n!)^2"
            ),
            "nonstationary_bound": (
                "every other theta_pi<=3/4, so error<=(3/4)^m"
            ),
            "concentration_boundary": (
                "E[a_m]^k<=E[a_m^k]<=E[a_m]; closing this interval needs "
                "a coupled k-walk contraction or concentration theorem"
            ),
        },
        validations=validations,
        scaling_records=scaling,
        headline_metrics=metrics,
        claim_gate={
            "exact_lazy_walk_spectral_formula_proved": verified,
            "single_walk_mean_mixes_to_two_over_factorial_squared": verified,
            "required_order_single_walk_mean_mixed": all(
                record.single_walk_mean_mixed for record in scaling
            ),
            "coupled_k_walk_contraction_proved": False,
            "word_map_concentration_proved": False,
            "growing_order_word_map_contraction_proved": False,
            "natural_average_inverse_polynomial_conclusive_bound_proved": False,
            "structured_maximal_effect_dilation_proved": False,
            "polynomial_hidden_permutation_decoder_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The one-walk mean is completely mixed at the required order, "
                "but the desired normalized frame moment is the kth moment of "
                "the quenched word statistic. Its concentration and coupled "
                "walk contraction remain open."
            ),
        },
        status=(
            "single-word-lazy-walk-mixing-proved-"
            "coupled-concentration-open"
        ),
        summary=(
            "Proved uniform 3/4 spectral mixing of the natural subset-word "
            "mean to 2/(n!)^2 and validated every finite control; the tail "
            "Jensen-to-bounded kth-moment interval remains "
            f"{tail.log2_unresolved_kth_moment_interval_width:.6g} bits wide."
        ),
        falsifiers_triggered=[
            "Direct subset-word averages match the exact physical-irrep lazy-walk spectrum.",
            "Only the two plus extensions of one-dimensional S_n irreps remain stationary.",
            "All other lazy-walk eigenvalues are at most 3/4 without a typical-partition assumption.",
            "Rapid mixing of E[a_m] does not imply concentration of a_m or control E[a_m^k].",
            "The finite kth-moment interval remains enormous at the target order.",
            "No coherent measurement, decoder, or classical separation follows from single-walk mixing.",
        ],
    )


def write_wreath_word_map_mixing_report(
    path: Path = REPORT_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = DEFAULT_EXPERIMENT_ID,
    registry_candidate_id: str = DEFAULT_CANDIDATE_ID,
    registry_result_id: str | None = None,
) -> dict[str, Any]:
    payload = asdict(run_wreath_word_map_mixing())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    if write_registry:
        upsert_negative_result(
            NegativeResultRecord(
                id=(
                    "NEG-CODE-WREATH-WORD-MAP-MEAN-MIXING-"
                    "NOT-KTH-MOMENT"
                ),
                source=str(path),
                claim=(
                    "Rapid mixing of the mean subset word-map statistic proves "
                    "the growing natural frame moment bound."
                ),
                reason_invalid=(
                    "The frame quantity is E[a_m^k], not E[a_m]. Jensen and "
                    "boundedness leave an exponentially wide interval without "
                    "a coupled-walk or concentration theorem."
                ),
                lesson=(
                    "Analyze the shared-generator k-walk transfer operator or "
                    "prove a quenched tail bound for identity/bridge subset "
                    "word counts."
                ),
                applies_to=[
                    registry_candidate_id,
                    registry_experiment_id,
                    "PO-COMPLEXITY",
                    "PO-SUCCESS",
                ],
                evidence=payload["headline_metrics"],
            )
        )
        upsert_experiment_result(
            ExperimentResultRecord(
                id=(
                    registry_result_id
                    or f"RESULT-{registry_experiment_id}-LATEST"
                ),
                experiment_id=registry_experiment_id,
                candidate_id=registry_candidate_id,
                created_at=payload["created_at"],
                status=payload["status"],
                summary=payload["summary"],
                metrics=payload["headline_metrics"],
                falsifiers_triggered=payload["falsifiers_triggered"],
                artifacts={
                    "self_dual_wreath_word_map_mixing": str(path)
                },
            )
        )
    return payload


if __name__ == "__main__":
    report = write_wreath_word_map_mixing_report()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))

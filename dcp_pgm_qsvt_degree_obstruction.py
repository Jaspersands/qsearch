"""Markov-degree obstruction for generic DCP PGM spectral rescaling.

The direct subset-sum equality circuit block-encodes

    A = diag(c_s / D),  D = 2^m.

Implementing normalized fiber weights by a bounded polynomial transform must
distinguish the eigenvalues 1/D and 2/D whenever singleton and doubleton
fibers are both present.  If a degree-d polynomial is bounded by one on
[-1, 1], Markov's inequality gives ``max |p'| <= d^2``.  Approximating
``1/sqrt(c)`` at c=1,2 therefore forces

    d >= sqrt((1 - 1/sqrt(2) - 2 epsilon) D).

Even if an amplitude encoding exposes singular values ``sqrt(c/D)``, the same
argument gives degree ``Omega(D^(1/4))``.  Both are exponential for m=Theta(n).

The theorem is deliberately route-specific.  It closes generic bounded
polynomial/QSVT transforms of these direct encodings.  It does not rule out a
source-aware block encoding with better normalization, a collision walk, or a
different collective measurement.  An explicit all-n label family certifies a
uniform worst-case obstruction; random-label prevalence is measured but not
promoted to an average-case theorem.
"""

from __future__ import annotations

import json
import math
import random
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Sequence

import numpy as np

from dcp_subset_sum_qtt_contraction_search import (
    exact_cyclic_subset_sum_counts,
)
from research_registry import (
    ExperimentResultRecord,
    NegativeResultRecord,
    upsert_experiment_result,
    upsert_negative_result,
    utc_now,
)


REPORT_PATH = Path(
    "research/phase_workbench/dcp_pgm_qsvt_degree_obstruction.json"
)
QUENCHED_OCCUPANCY_PATH = Path(
    "research/classical_baselines/"
    "dcp_subset_sum_quenched_occupancy_theorem.json"
)
DEFAULT_EXPERIMENT_ID = "EXP-DHS-DCP-PGM-QSVT-DEGREE-OBSTRUCTION"
DEFAULT_CANDIDATE_ID = "DHS-GOWERS-SIEVE"
DEFAULT_APPROXIMATION_ERROR = 1 / 32


@dataclass(frozen=True)
class LiftedSourceCertificate:
    n_bits: int
    register_count: int
    labels: tuple[int, ...]
    zero_fiber_count: int
    singleton_fiber_count: int
    doubleton_fiber_count: int
    other_positive_fiber_count: int
    exact_pattern_verified: bool
    count_encoding_degree_lower_bound: float
    amplitude_encoding_degree_lower_bound: float
    status: str


@dataclass(frozen=True)
class RandomSourceControl:
    n_bits: int
    register_count: int
    trial: int
    label_digest: str
    singleton_fiber_count: int
    doubleton_fiber_count: int
    maximum_fiber_size: int
    singleton_doubleton_obstruction_present: bool


@dataclass(frozen=True)
class QSVTDegreeScalingRow:
    n_bits: int
    register_count: int
    approximation_error: float
    target_weight_gap: float
    count_encoding_degree_lower_bound_log2: float
    amplitude_encoding_degree_lower_bound_log2: float
    polynomial_degree_threshold_log2: float
    count_encoding_superpolynomial: bool
    amplitude_encoding_superpolynomial: bool


@dataclass(frozen=True)
class DCPPGMQSVTDegreeReport:
    created_at: str
    theorem: dict[str, str]
    lifted_source_certificates: list[LiftedSourceCertificate]
    random_source_controls: list[RandomSourceControl]
    scaling_rows: list[QSVTDegreeScalingRow]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, bool | str]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _target_weight_gap(error: float) -> float:
    gap = 1 - 1 / math.sqrt(2) - 2 * error
    if gap <= 0:
        raise ValueError(
            "approximation error is too large to separate fiber sizes one and two"
        )
    return gap


def count_encoding_degree_lower_bound(
    register_count: int,
    approximation_error: float = DEFAULT_APPROXIMATION_ERROR,
) -> float:
    """Markov lower bound for p(c/D) approximating 1/sqrt(c)."""

    if register_count < 1:
        raise ValueError("register_count must be positive")
    return (
        math.sqrt(_target_weight_gap(approximation_error))
        * math.exp2(register_count / 2)
    )


def amplitude_encoding_degree_lower_bound(
    register_count: int,
    approximation_error: float = DEFAULT_APPROXIMATION_ERROR,
) -> float:
    """Markov lower bound for p(sqrt(c/D)) at c=1,2."""

    if register_count < 1:
        raise ValueError("register_count must be positive")
    return (
        math.sqrt(
            _target_weight_gap(approximation_error)
            / (math.sqrt(2) - 1)
        )
        * math.exp2(register_count / 4)
    )


def lifted_singleton_doubleton_labels(n_bits: int) -> tuple[int, ...]:
    """All-n source with repeated low label and independent high bits."""

    if n_bits < 2:
        raise ValueError("n_bits must be at least two")
    return (1, 1, *(1 << bit for bit in range(2, n_bits)))


def audit_lifted_source(
    n_bits: int,
    approximation_error: float = DEFAULT_APPROXIMATION_ERROR,
) -> LiftedSourceCertificate:
    labels = lifted_singleton_doubleton_labels(n_bits)
    counts = exact_cyclic_subset_sum_counts(labels, 1 << n_bits)
    zero = int(np.count_nonzero(counts == 0))
    singleton = int(np.count_nonzero(counts == 1))
    doubleton = int(np.count_nonzero(counts == 2))
    other = int(np.count_nonzero(counts > 2))
    block_count = 1 << (n_bits - 2)
    verified = (
        zero == block_count
        and singleton == 2 * block_count
        and doubleton == block_count
        and other == 0
        and int(counts.sum()) == (1 << n_bits)
    )
    return LiftedSourceCertificate(
        n_bits=n_bits,
        register_count=len(labels),
        labels=labels,
        zero_fiber_count=zero,
        singleton_fiber_count=singleton,
        doubleton_fiber_count=doubleton,
        other_positive_fiber_count=other,
        exact_pattern_verified=verified,
        count_encoding_degree_lower_bound=(
            count_encoding_degree_lower_bound(
                len(labels), approximation_error
            )
        ),
        amplitude_encoding_degree_lower_bound=(
            amplitude_encoding_degree_lower_bound(
                len(labels), approximation_error
            )
        ),
        status=(
            "exact-all-n-singleton-doubleton-source-certificate"
            if verified
            else "lifted-source-pattern-failed"
        ),
    )


def _label_digest(labels: Sequence[int]) -> str:
    accumulator = 0xCBF29CE484222325
    for label in labels:
        accumulator ^= int(label)
        accumulator = (
            accumulator * 0x100000001B3
        ) & ((1 << 64) - 1)
    return f"{accumulator:016x}"


def audit_random_source(
    n_bits: int,
    trial: int,
    seed: int,
) -> RandomSourceControl:
    modulus = 1 << n_bits
    rng = random.Random(seed)
    labels = [rng.randrange(modulus) for _ in range(n_bits)]
    counts = exact_cyclic_subset_sum_counts(labels, modulus)
    singleton = int(np.count_nonzero(counts == 1))
    doubleton = int(np.count_nonzero(counts == 2))
    return RandomSourceControl(
        n_bits=n_bits,
        register_count=n_bits,
        trial=trial,
        label_digest=_label_digest(labels),
        singleton_fiber_count=singleton,
        doubleton_fiber_count=doubleton,
        maximum_fiber_size=int(np.max(counts)),
        singleton_doubleton_obstruction_present=(
            singleton > 0 and doubleton > 0
        ),
    )


def degree_scaling_row(
    n_bits: int,
    approximation_error: float = DEFAULT_APPROXIMATION_ERROR,
    polynomial_degree_power: int = 8,
) -> QSVTDegreeScalingRow:
    if n_bits < 2:
        raise ValueError("n_bits must be at least two")
    count_bound = count_encoding_degree_lower_bound(
        n_bits, approximation_error
    )
    amplitude_bound = amplitude_encoding_degree_lower_bound(
        n_bits, approximation_error
    )
    polynomial_threshold_log2 = (
        polynomial_degree_power * math.log2(n_bits)
    )
    return QSVTDegreeScalingRow(
        n_bits=n_bits,
        register_count=n_bits,
        approximation_error=approximation_error,
        target_weight_gap=_target_weight_gap(approximation_error),
        count_encoding_degree_lower_bound_log2=math.log2(count_bound),
        amplitude_encoding_degree_lower_bound_log2=math.log2(
            amplitude_bound
        ),
        polynomial_degree_threshold_log2=polynomial_threshold_log2,
        count_encoding_superpolynomial=(
            math.log2(count_bound) > polynomial_threshold_log2
        ),
        amplitude_encoding_superpolynomial=(
            math.log2(amplitude_bound) > polynomial_threshold_log2
        ),
    )


def build_qsvt_degree_obstruction_report(
    exact_n_values: tuple[int, ...] = tuple(range(2, 15)),
    random_n_values: tuple[int, ...] = (8, 10, 12, 14, 16, 18),
    random_trials: int = 4,
    scaling_n_values: tuple[int, ...] = (64, 128, 256, 512, 1024),
    approximation_error: float = DEFAULT_APPROXIMATION_ERROR,
    seed: int = 0,
    occupancy_theorem_path: Path = QUENCHED_OCCUPANCY_PATH,
) -> DCPPGMQSVTDegreeReport:
    lifted = [
        audit_lifted_source(n_bits, approximation_error)
        for n_bits in exact_n_values
    ]
    random_controls = [
        audit_random_source(
            n_bits,
            trial,
            seed + 1009 * n_bits + trial,
        )
        for n_bits in random_n_values
        for trial in range(random_trials)
    ]
    scaling = [
        degree_scaling_row(n_bits, approximation_error)
        for n_bits in scaling_n_values
    ]
    exact_failures = sum(
        not row.exact_pattern_verified for row in lifted
    )
    random_survivors = sum(
        row.singleton_doubleton_obstruction_present
        for row in random_controls
    )
    try:
        occupancy_payload = (
            json.loads(occupancy_theorem_path.read_text())
            if occupancy_theorem_path.exists()
            else {}
        )
    except (json.JSONDecodeError, OSError):
        occupancy_payload = {}
    average_prevalence_proved = bool(
        occupancy_payload.get("claim_gate", {}).get(
            "random_source_singleton_doubleton_prevalence_proved",
            False,
        )
    )
    metrics: dict[str, int | float] = {
        "exact_lifted_source_count": len(lifted),
        "exact_lifted_source_failure_count": exact_failures,
        "random_source_control_count": len(random_controls),
        "random_source_singleton_doubleton_count": random_survivors,
        "random_source_singleton_doubleton_fraction": (
            random_survivors / len(random_controls)
            if random_controls
            else 0.0
        ),
        "count_encoding_markov_theorem_count": 1,
        "amplitude_encoding_markov_theorem_count": 1,
        "uniform_worst_case_qsvt_obstruction_count": (
            int(exact_failures == 0)
        ),
        "average_case_random_source_prevalence_theorem_count": int(
            average_prevalence_proved
        ),
        "structured_preconditioner_lower_bound_count": 0,
        "collision_walk_lower_bound_count": 0,
        "general_collective_measurement_lower_bound_count": 0,
        "tail_count_encoding_superpolynomial_row_count": sum(
            row.count_encoding_superpolynomial for row in scaling
        ),
        "tail_amplitude_encoding_superpolynomial_row_count": sum(
            row.amplitude_encoding_superpolynomial for row in scaling
        ),
        "maximum_n_bits": max(scaling_n_values),
        "tail_count_encoding_degree_lower_bound_log2": (
            scaling[-1].count_encoding_degree_lower_bound_log2
        ),
        "tail_amplitude_encoding_degree_lower_bound_log2": (
            scaling[-1].amplitude_encoding_degree_lower_bound_log2
        ),
    }
    return DCPPGMQSVTDegreeReport(
        created_at=utc_now(),
        theorem={
            "markov_inequality": (
                "For real degree-d p bounded by one on [-1,1], "
                "max_{[-1,1]} |p'| <= d^2."
            ),
            "target_weights": (
                "|p(1/D)-1|<=epsilon and "
                "|p(2/D)-1/sqrt(2)|<=epsilon."
            ),
            "count_encoding_bound": (
                "d>=sqrt((1-1/sqrt(2)-2epsilon)D)."
            ),
            "amplitude_encoding_bound": (
                "For singular values sqrt(c/D), "
                "d>=sqrt((1-1/sqrt(2)-2epsilon)"
                "*sqrt(D)/(sqrt(2)-1))."
            ),
            "explicit_source_family": (
                "a=(1,1,4,8,...,2^(n-1)) has N/2 singleton, "
                "N/4 doubleton, and N/4 empty fibers for every n>=2."
            ),
        },
        lifted_source_certificates=lifted,
        random_source_controls=random_controls,
        scaling_rows=scaling,
        headline_metrics=metrics,
        claim_gate={
            "generic_count_encoding_qsvt_rescaling_polynomial": False,
            "generic_amplitude_encoding_qsvt_rescaling_polynomial": False,
            "uniform_worst_case_obstruction_proved": exact_failures == 0,
            "average_case_obstruction_proved": average_prevalence_proved,
            "structured_preconditioner_ruled_out": False,
            "collision_walk_ruled_out": False,
            "general_collective_measurement_ruled_out": False,
            "speedup_claim_allowed": False,
            "reason": (
                "Markov's inequality gives exponential degree for generic "
                "bounded polynomial transforms of the direct count and "
                "amplitude encodings. The all-n source family proves a uniform "
                "worst-case obstruction. The quenched occupancy theorem "
                f"{'transfers it to almost every random source' if average_prevalence_proved else 'has not yet transferred it to random sources'}; "
                "source-structured alternatives remain open."
            ),
        },
        status=(
            "generic-direct-qsvt-rescaling-exponential-"
            "average-source-structured-routes-open"
        ),
        summary=(
            f"Verified {len(lifted)} all-n lifted source controls with "
            f"{exact_failures} failures. Singleton and doubleton fibers co-"
            f"occurred in {random_survivors}/{len(random_controls)} finite "
            "random controls. Generic direct QSVT rescaling is exponentially "
            "degree-limited; the average-source transfer is "
            f"{'proved' if average_prevalence_proved else 'unproved'}, and no "
            "source-structured lower bound is claimed."
        ),
        falsifiers_triggered=[
            "A polynomial-size direct block encoding does not imply a polynomial-degree bounded spectral transform.",
            "QSVT degree must include the exponentially small spectral spacing, not only the fiber condition-number ratio.",
            "Switching from count eigenvalues to square-root amplitudes weakens but does not remove the exponential Markov bound.",
            "An explicit worst-case label family is not evidence for random-source prevalence.",
            "The theorem does not cover source-aware encodings, collision walks, or different collective measurements.",
        ],
    )


def write_qsvt_degree_obstruction_report(
    output_path: Path = REPORT_PATH,
    *,
    write_registry: bool = True,
    registry_experiment_id: str = DEFAULT_EXPERIMENT_ID,
    registry_candidate_id: str = DEFAULT_CANDIDATE_ID,
    registry_result_id: str | None = None,
    exact_n_values: tuple[int, ...] = tuple(range(2, 15)),
    random_n_values: tuple[int, ...] = (8, 10, 12, 14, 16, 18),
    random_trials: int = 4,
    scaling_n_values: tuple[int, ...] = (64, 128, 256, 512, 1024),
    approximation_error: float = DEFAULT_APPROXIMATION_ERROR,
    seed: int = 0,
    occupancy_theorem_path: Path = QUENCHED_OCCUPANCY_PATH,
) -> dict[str, object]:
    payload = asdict(
        build_qsvt_degree_obstruction_report(
            exact_n_values=exact_n_values,
            random_n_values=random_n_values,
            random_trials=random_trials,
            scaling_n_values=scaling_n_values,
            approximation_error=approximation_error,
            seed=seed,
            occupancy_theorem_path=occupancy_theorem_path,
        )
    )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(payload, indent=2, sort_keys=True)
    )
    return payload


if __name__ == "__main__":
    report = write_qsvt_degree_obstruction_report()
    print(
        json.dumps(
            report["headline_metrics"], indent=2, sort_keys=True
        )
    )

"""Bernstein-degree obstruction for generic wreath spectral trimming.

The trimmed sub-POVM requires the low-spectrum projector

    R = 1[B <= tau],       tau = c Tr(B^2)/rank(P_s).

At the information threshold ``k=ceil(log2(n!))`` and fixed ``c``,
``tau=Theta(1/n!)``.  A bounded polynomial that uniformly approximates a
low-pass filter must change by a constant between eigenvalues ``tau`` and
``2*tau``.  Bernstein's inequality for polynomials bounded on ``[-1,1]`` is
linear in the degree away from the endpoints.  Since this transition is near
the interior point zero, it gives

    degree = Omega(tau^-1) = Omega(n!).

If a projected block encoding exposes singular values ``sqrt(lambda)``
instead, the transition occurs over
``(sqrt(2)-1)sqrt(tau)`` and still requires

    degree = Omega(tau^-1/2) = Omega(sqrt(n!)).

This rules out a uniform generic polynomial/QSVT realization from the
normalization-one frame block encoding.  It is not a circuit lower bound for
all access models: a representation-theoretic transform, promised spectral
gap, better-scaled block encoding, or direct quotient construction could
bypass the polynomial approximation route.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from research_registry import (
    ExperimentResultRecord,
    NegativeResultRecord,
    upsert_experiment_result,
    upsert_negative_result,
    utc_now,
)
REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_spectral_filter_degree_obstruction.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-SPECTRAL-FILTER-DEGREE-OBSTRUCTION"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"
DEFAULT_APPROXIMATION_ERROR = 1 / 16
DEFAULT_CLIP_MULTIPLIER = 2.0


@dataclass(frozen=True)
class SpectralFilterDegreeScalingRecord:
    n: int
    hidden_label_count_decimal: str
    log2_hidden_label_count: float
    information_threshold_copy_count: int
    frame_second_moment_per_rank: float
    frame_second_moment_per_rank_log2: float
    clip_multiplier: float
    clip_threshold: float
    clip_threshold_log2: float
    approximation_error: float
    required_filter_value_gap: float
    eigenvalue_transition_width: float
    eigenvalue_transition_width_log2: float
    singular_value_transition_width: float
    singular_value_transition_width_log2: float
    eigenvalue_encoding_degree_lower_bound_log2: float
    singular_value_encoding_degree_lower_bound_log2: float
    polynomial_degree_benchmark_log2: float
    eigenvalue_encoding_superpolynomial: bool
    singular_value_encoding_superpolynomial: bool
    status: str


@dataclass(frozen=True)
class SpectralFilterDegreeObstructionReport:
    created_at: str
    theorem_contract: dict[str, str]
    scaling_records: list[SpectralFilterDegreeScalingRecord]
    adversarial_audit: list[dict[str, bool | str]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, bool | str]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _required_filter_gap(approximation_error: float) -> float:
    if not 0 <= approximation_error < 0.5:
        raise ValueError("approximation_error must lie in [0,1/2)")
    return 1 - 2 * approximation_error


def eigenvalue_filter_degree_lower_bound(
    clip_threshold: float,
    approximation_error: float = DEFAULT_APPROXIMATION_ERROR,
) -> float:
    """Bernstein lower bound for a low-pass polynomial on B eigenvalues."""

    if not 0 < clip_threshold <= 0.5:
        raise ValueError("clip_threshold must lie in (0,1/2]")
    return (
        _required_filter_gap(approximation_error)
        * math.sqrt(1 - 4 * clip_threshold * clip_threshold)
        / clip_threshold
    )


def singular_filter_degree_lower_bound(
    clip_threshold: float,
    approximation_error: float = DEFAULT_APPROXIMATION_ERROR,
) -> float:
    """Bernstein bound when singular values sqrt(lambda) are exposed."""

    if not 0 < clip_threshold <= 0.5:
        raise ValueError("clip_threshold must lie in (0,1/2]")
    transition_width = (math.sqrt(2) - 1) * math.sqrt(clip_threshold)
    return (
        _required_filter_gap(approximation_error)
        * math.sqrt(1 - 2 * clip_threshold)
        / transition_width
    )


def _wreath_second_moment_per_rank_log2(
    hidden_label_count: int,
    copy_count: int,
) -> float:
    subset_count = 1 << copy_count
    return (
        math.log2(subset_count + hidden_label_count - 1)
        - math.log2(hidden_label_count)
        - copy_count
    )


def spectral_filter_degree_scaling_record(
    n: int,
    *,
    clip_multiplier: float = DEFAULT_CLIP_MULTIPLIER,
    approximation_error: float = DEFAULT_APPROXIMATION_ERROR,
    polynomial_degree_power: int = 12,
) -> SpectralFilterDegreeScalingRecord:
    if n < 3:
        raise ValueError("n must be at least three")
    if clip_multiplier <= 1:
        raise ValueError("clip_multiplier must exceed one")
    hidden_count = math.factorial(n)
    copies = math.ceil(math.log2(hidden_count))
    second_scale_log2 = _wreath_second_moment_per_rank_log2(
        hidden_count, copies
    )
    threshold_log2 = math.log2(clip_multiplier) + second_scale_log2
    threshold = math.exp2(threshold_log2)
    if threshold_log2 > -1:
        raise ValueError("scaling row is outside the low-spectrum regime")
    filter_gap_log2 = math.log2(
        _required_filter_gap(approximation_error)
    )
    threshold = math.exp2(threshold_log2)
    eigen_correction_log2 = 0.5 * math.log2(
        max(1 - 4 * threshold * threshold, 2**-1074)
    )
    eigen_bound_log2 = (
        filter_gap_log2 + eigen_correction_log2 - threshold_log2
    )
    singular_transition_log2 = (
        math.log2(math.sqrt(2) - 1) + 0.5 * threshold_log2
    )
    singular_correction_log2 = 0.5 * math.log2(
        max(1 - 2 * threshold, 2**-1074)
    )
    singular_bound_log2 = (
        filter_gap_log2
        + singular_correction_log2
        - singular_transition_log2
    )
    benchmark = polynomial_degree_power * math.log2(n)
    return SpectralFilterDegreeScalingRecord(
        n=n,
        hidden_label_count_decimal=str(hidden_count),
        log2_hidden_label_count=math.log2(hidden_count),
        information_threshold_copy_count=copies,
        frame_second_moment_per_rank=math.exp2(second_scale_log2),
        frame_second_moment_per_rank_log2=second_scale_log2,
        clip_multiplier=clip_multiplier,
        clip_threshold=threshold,
        clip_threshold_log2=threshold_log2,
        approximation_error=approximation_error,
        required_filter_value_gap=_required_filter_gap(
            approximation_error
        ),
        eigenvalue_transition_width=threshold,
        eigenvalue_transition_width_log2=threshold_log2,
        singular_value_transition_width=math.exp2(
            singular_transition_log2
        ),
        singular_value_transition_width_log2=singular_transition_log2,
        eigenvalue_encoding_degree_lower_bound_log2=eigen_bound_log2,
        singular_value_encoding_degree_lower_bound_log2=(
            singular_bound_log2
        ),
        polynomial_degree_benchmark_log2=benchmark,
        eigenvalue_encoding_superpolynomial=(
            eigen_bound_log2 > benchmark
        ),
        singular_value_encoding_superpolynomial=(
            singular_bound_log2 > benchmark
        ),
        status="generic-spectral-filter-degree-superpolynomial",
    )


def run_spectral_filter_degree_obstruction(
    n_values: tuple[int, ...] = (
        16,
        24,
        32,
        48,
        64,
        96,
        128,
        192,
        256,
        384,
        512,
    ),
) -> SpectralFilterDegreeObstructionReport:
    scaling = [
        spectral_filter_degree_scaling_record(n) for n in n_values
    ]
    metrics: dict[str, int | float] = {
        "bounded_polynomial_bernstein_theorem_count": 1,
        "bounded_polynomial_markov_theorem_count": 0,
        "eigenvalue_filter_degree_obstruction_theorem_count": 1,
        "singular_filter_degree_obstruction_theorem_count": 1,
        "asymptotic_eigenvalue_filter_superpolynomial_theorem_count": 1,
        "asymptotic_singular_filter_superpolynomial_theorem_count": 1,
        "scaling_record_count": len(scaling),
        "eigenvalue_encoding_superpolynomial_row_count": sum(
            record.eigenvalue_encoding_superpolynomial
            for record in scaling
        ),
        "singular_value_encoding_superpolynomial_row_count": sum(
            record.singular_value_encoding_superpolynomial
            for record in scaling
        ),
        "maximum_n": scaling[-1].n,
        "tail_log2_hidden_label_count": scaling[-1].log2_hidden_label_count,
        "tail_eigenvalue_degree_lower_bound_log2": (
            scaling[-1].eigenvalue_encoding_degree_lower_bound_log2
        ),
        "tail_singular_degree_lower_bound_log2": (
            scaling[-1].singular_value_encoding_degree_lower_bound_log2
        ),
        "promised_inverse_polynomial_relative_gap_theorem_count": 0,
        "better_scaled_frame_block_encoding_count": 0,
        "representation_structured_low_pass_transform_count": 0,
        "polynomial_hidden_permutation_decoder_count": 0,
        "general_quantum_circuit_lower_bound_count": 0,
        "new_quantum_algorithm_count": 0,
    }
    tail_eigen_super = scaling[-1].eigenvalue_encoding_superpolynomial
    tail_singular_super = scaling[-1].singular_value_encoding_superpolynomial
    return SpectralFilterDegreeObstructionReport(
        created_at=utc_now(),
        theorem_contract={
            "normalized_access": (
                "The available LCU/projected block encoding has normalization "
                "one and exposes B with spectrum in [0,1]."
            ),
            "uniform_low_pass": (
                "A generic filter must be within epsilon of one on [0,tau] "
                "and within epsilon of zero on [2tau,1]."
            ),
            "bernstein_step": (
                "The mean-value theorem requires derivative at least "
                "(1-2epsilon)/Delta. Bernstein's inequality bounds the "
                "derivative of a degree-d polynomial bounded by one on "
                "[-1,1] by d/sqrt(1-x^2); both transitions lie near x=0."
            ),
            "eigenvalue_bound": (
                "d>=(1-2epsilon)sqrt(1-4tau^2)/tau=Omega(n!)."
            ),
            "singular_value_bound": (
                "Across sqrt(tau) to sqrt(2tau), "
                "d>=(1-2epsilon)sqrt(1-2tau)/"
                "((sqrt(2)-1)sqrt(tau))=Omega(sqrt(n!))."
            ),
            "scope_boundary": (
                "The bound applies to uniform bounded-polynomial transforms "
                "of the normalization-one encoding. It does not rule out a "
                "promised spectral gap, a better normalization, an exact "
                "representation transform, or a non-polynomial circuit."
            ),
        },
        scaling_records=scaling,
        adversarial_audit=[
            {
                "objection": (
                    "The Bernstein argument proves an instance-specific lower "
                    "bound for the actual natural frame spectrum."
                ),
                "resolved": False,
                "resolution": (
                    "It proves a uniform generic-filter lower bound. An actual "
                    "frame could have a favorable spectral gap or algebraic "
                    "diagonalization; neither is currently proved."
                ),
            },
            {
                "objection": (
                    "Passing from eigenvalues to singular values makes the "
                    "filter polynomial degree polynomial in n."
                ),
                "resolved": True,
                "resolution": (
                    "The transition widens only to Theta((n!)^-1/2), and "
                    "Bernstein still gives Omega(sqrt(n!)) degree."
                ),
            },
            {
                "objection": (
                    "The degree obstruction rules out every structured "
                    "preconditioner or representation-theoretic measurement."
                ),
                "resolved": False,
                "resolution": (
                    "The theorem is deliberately access-model specific. A "
                    "transform that exposes rescaled eigenvalue labels or "
                    "quotients common channels need not approximate this step "
                    "function through the normalized frame oracle."
                ),
            },
        ],
        headline_metrics=metrics,
        claim_gate={
            "generic_eigenvalue_polynomial_filter_superpolynomial": (
                True
            ),
            "generic_singular_value_polynomial_filter_superpolynomial": (
                True
            ),
            "normalization_one_qsvt_route_viable": False,
            "instance_specific_natural_spectral_gap_ruled_out": False,
            "better_scaled_block_encoding_ruled_out": False,
            "representation_structured_transform_ruled_out": False,
            "general_quantum_circuit_lower_bound_proved": False,
            "polynomial_hidden_permutation_decoder_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The spectral trimming measurement has constant "
                "information-theoretic success, but generic polynomial/QSVT "
                "filtering of the normalization-one frame requires factorial "
                "degree on eigenvalues or square-root-factorial degree on "
                "singular values. Only a structured spectral representation or "
                "better-scaled access can bypass this obstruction."
            ),
        },
        status=(
            "generic-spectral-qsvt-falsified-structured-transform-open"
            if tail_eigen_super and tail_singular_super
            else "spectral-filter-degree-scaling-inconclusive"
        ),
        summary=(
            "Proved that a uniform low-pass realization of the trimmed "
            "sub-POVM from the normalization-one frame encoding needs degree "
            "Omega(n!) on eigenvalues or Omega(sqrt(n!)) on singular "
            "values. A representation-structured bypass remains open."
        ),
        falsifiers_triggered=[
            (
                "Generic QSVT does not turn the information-theoretic trimmed "
                "measurement into an efficient algorithm."
            ),
            (
                "Square-root singular-value access weakens but does not remove "
                "the factorial spectral-resolution barrier."
            ),
            (
                "No instance-specific gap or all-circuit lower bound is "
                "claimed; a structured transform is now the decisive target."
            ),
        ],
    )


def write_spectral_filter_degree_obstruction_report(
    path: Path = REPORT_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = DEFAULT_EXPERIMENT_ID,
    registry_candidate_id: str = DEFAULT_CANDIDATE_ID,
    registry_result_id: str | None = None,
) -> dict[str, Any]:
    payload = asdict(run_spectral_filter_degree_obstruction())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    if write_registry:
        upsert_negative_result(
            NegativeResultRecord(
                id="NEG-CODE-WREATH-GENERIC-SPECTRAL-TRIM-QSVT",
                source=str(path),
                claim=(
                    "A generic bounded-polynomial transform of the "
                    "normalization-one average-frame encoding implements the "
                    "constant-success spectral trimming in polynomial degree."
                ),
                reason_invalid=(
                    "The cutoff is Theta(1/n!). Bernstein's inequality forces "
                    "Omega(n!) eigenvalue-polynomial degree or "
                    "Omega(sqrt(n!)) singular-value-polynomial degree."
                ),
                lesson=(
                    "Search for an exact representation-basis classifier, a "
                    "better-scaled block encoding, or an intrinsic quotient; "
                    "do not apply generic QSVT to B."
                ),
                applies_to=[
                    registry_candidate_id,
                    registry_experiment_id,
                    "PO-MEASUREMENT",
                    "PO-COMPLEXITY",
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
                    "self_dual_wreath_spectral_filter_degree_obstruction": str(
                        path
                    )
                },
            )
        )
    return payload


if __name__ == "__main__":
    report = write_spectral_filter_degree_obstruction_report()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))

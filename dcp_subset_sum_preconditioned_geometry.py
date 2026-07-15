"""Exact residual-density audit for low-bit-conditioned modular subset sum.

Fix the low ``b`` bits of every label and a target low residue.  Let ``S`` be
the binary assignments satisfying that low congruence and let ``F=|S|``.  The
remaining high parts of the labels and target are independent and uniform in
``Z_Q`` for ``Q=2^(n-b)``.  Each assignment in ``S`` therefore has a uniform
high residual.  More strongly, residuals of any two distinct assignments are
independent: after adjoining the target variable, their two coefficient rows
have a 2x2 minor with determinant +/-1 at any coordinate where the assignments
differ.

For any residual window W of width w, the candidate count K obeys exactly

    E[K | low data] = F w / Q
    E[K(K-1) | low data] = F(F-1) (w/Q)^2
    Var[K | low data] = F (w/Q) (1-w/Q).

Thus logarithmic low-bit conditioning does not by itself improve expected
exact-solution or near-residual density: the candidate fiber and quotient
modulus shrink by the same factor.  This is a no-go result for count-only or
residual-window explanations, not for higher-order correlations, LLL basis
geometry, or a new implicit decoder.
"""

from __future__ import annotations

import json
import math
import random
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Sequence

import numpy as np

from dcp_hashed_fiber_measurement_audit import subset_sum_counts
from research_registry import (
    ExperimentResultRecord,
    NegativeResultRecord,
    upsert_experiment_result,
    upsert_negative_result,
    utc_now,
)


DCP_SUBSET_SUM_PRECONDITIONED_GEOMETRY_PATH = Path(
    "research/classical_baselines/dcp_subset_sum_preconditioned_geometry.json"
)
DEFAULT_EXPERIMENT_ID = "EXP-DHS-DCP-SUBSET-SUM-PRECONDITIONED-GEOMETRY"
DEFAULT_CANDIDATE_ID = "DHS-GOWERS-SIEVE"


@dataclass(frozen=True)
class ConditionalResidualTheoremCertificate:
    n_bits: int
    register_offset: int
    register_count: int
    constrained_low_bits: int
    quotient_bits: int
    quotient_modulus: int
    exact_conditional_first_moment_proved: bool
    exact_conditional_second_factorial_moment_proved: bool
    exact_conditional_variance_proved: bool
    ensemble_exact_solution_mean: float
    unconditioned_exact_solution_mean: float
    density_exponent_change: float
    pairwise_independence_proof: str
    limitations: list[str]


@dataclass(frozen=True)
class PreconditionedGeometryRow:
    n_bits: int
    register_offset: int
    register_count: int
    log_multiplier: int
    constrained_low_bits: int
    quotient_bits: int
    trial_index: int
    residual_window_radius: int
    residual_window_width: int
    low_fiber_assignment_count: int
    expected_low_fiber_assignment_count: float
    low_fiber_log2_ratio_to_expectation: float | None
    conditional_expected_window_count: float
    conditional_window_count_variance: float
    observed_window_count: int
    observed_exact_solution_count: int
    source_target_legal: bool
    nearest_nonzero_supported_residual: int | None
    conditional_exact_solution_density: float
    unconditioned_exact_solution_density: float
    conditional_to_unconditioned_density_ratio: float
    count_geometry_improvement_proved: bool
    lll_geometry_improvement_proved: bool


@dataclass(frozen=True)
class DCPSubsetSumPreconditionedGeometryReport:
    created_at: str
    theorem_contract: dict[str, str]
    theorem_certificates: list[ConditionalResidualTheoremCertificate]
    rows: list[PreconditionedGeometryRow]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, bool | str]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def constrained_low_bits(n_bits: int, log_multiplier: int) -> int:
    if n_bits < 4:
        raise ValueError("n_bits must be at least 4")
    if log_multiplier < 1:
        raise ValueError("log_multiplier must be positive")
    return min(n_bits - 1, max(1, math.ceil(log_multiplier * math.log2(n_bits))))


def conditional_window_moments(
    low_fiber_size: int,
    quotient_modulus: int,
    window_width: int,
) -> tuple[float, float, float]:
    if low_fiber_size < 0:
        raise ValueError("low_fiber_size must be nonnegative")
    if quotient_modulus < 1:
        raise ValueError("quotient_modulus must be positive")
    if not 0 <= window_width <= quotient_modulus:
        raise ValueError("window_width must lie between zero and the quotient modulus")
    probability = window_width / quotient_modulus
    mean = low_fiber_size * probability
    second_factorial = low_fiber_size * max(0, low_fiber_size - 1) * probability**2
    variance = low_fiber_size * probability * (1.0 - probability)
    return float(mean), float(second_factorial), float(variance)


def theorem_certificate(
    n_bits: int,
    register_offset: int,
    log_multiplier: int,
) -> ConditionalResidualTheoremCertificate:
    low_bits = constrained_low_bits(n_bits, log_multiplier)
    quotient_bits = n_bits - low_bits
    quotient_modulus = 1 << quotient_bits
    register_count = n_bits + register_offset
    solution_mean = float(2**register_offset)
    return ConditionalResidualTheoremCertificate(
        n_bits=n_bits,
        register_offset=register_offset,
        register_count=register_count,
        constrained_low_bits=low_bits,
        quotient_bits=quotient_bits,
        quotient_modulus=quotient_modulus,
        exact_conditional_first_moment_proved=True,
        exact_conditional_second_factorial_moment_proved=True,
        exact_conditional_variance_proved=True,
        ensemble_exact_solution_mean=solution_mean,
        unconditioned_exact_solution_mean=solution_mean,
        density_exponent_change=0.0,
        pairwise_independence_proof=(
            "Condition on all low label residues and the target low residue. For distinct assignments x,y in the "
            "low fiber, append the target coefficient -1. At a coordinate where x and y differ, the two extended "
            "coefficient rows have a 2x2 determinant +/-1, a unit modulo 2^(n-b). Their high residual pair is "
            "therefore uniform on Z_Q^2, including assignment zero and assignment-complement cases."
        ),
        limitations=[
            "Pairwise independence does not imply mutual independence of three or more residuals.",
            "The theorem rules out count-only and fixed residual-window explanations, not all LLL basis effects.",
            "A decoder may exploit higher-order correlations, representation structure, or a non-window observable.",
            "Finite empirical rows validate implementation only; the moment identities carry the theorem claim.",
        ],
    )


def _window_width(radius: int, modulus: int) -> int:
    if radius < 0:
        raise ValueError("window radius must be nonnegative")
    return min(modulus, 2 * radius + 1)


def _circular_distance(left: int, right: int, modulus: int) -> int:
    delta = (left - right) % modulus
    return min(delta, modulus - delta)


def analyze_preconditioned_geometry(
    n_bits: int,
    register_offset: int,
    log_multiplier: int,
    trial_index: int,
    residual_window_radius: int,
    seed: int,
) -> PreconditionedGeometryRow:
    low_bits = constrained_low_bits(n_bits, log_multiplier)
    low_modulus = 1 << low_bits
    quotient_modulus = 1 << (n_bits - low_bits)
    modulus = 1 << n_bits
    register_count = n_bits + register_offset
    rng = random.Random(seed)
    labels = [rng.randrange(modulus) for _ in range(register_count)]
    target = rng.randrange(modulus)
    counts = subset_sum_counts(n_bits, labels).astype(np.int64)
    target_low = target & (low_modulus - 1)
    quotient_counts = counts[target_low::low_modulus]
    low_fiber_size = int(np.sum(quotient_counts))
    expected_low_fiber = float(2 ** (register_count - low_bits))
    low_ratio = (
        math.log2(low_fiber_size / expected_low_fiber)
        if low_fiber_size > 0 and expected_low_fiber > 0
        else None
    )
    target_quotient = target >> low_bits
    window_width = _window_width(residual_window_radius, quotient_modulus)
    supported_indices = np.flatnonzero(quotient_counts)
    window_indices = [
        index
        for index in range(quotient_modulus)
        if _circular_distance(index, target_quotient, quotient_modulus) <= residual_window_radius
    ]
    observed_window = int(np.sum(quotient_counts[window_indices]))
    exact_count = int(quotient_counts[target_quotient])
    nonzero_distances = [
        _circular_distance(int(index), target_quotient, quotient_modulus)
        for index in supported_indices
        if int(index) != target_quotient
    ]
    mean, _, variance = conditional_window_moments(
        low_fiber_size,
        quotient_modulus,
        window_width,
    )
    conditional_exact_density = low_fiber_size / quotient_modulus
    unconditioned_density = float(2**register_offset)
    density_ratio = conditional_exact_density / unconditioned_density
    return PreconditionedGeometryRow(
        n_bits=n_bits,
        register_offset=register_offset,
        register_count=register_count,
        log_multiplier=log_multiplier,
        constrained_low_bits=low_bits,
        quotient_bits=n_bits - low_bits,
        trial_index=trial_index,
        residual_window_radius=residual_window_radius,
        residual_window_width=window_width,
        low_fiber_assignment_count=low_fiber_size,
        expected_low_fiber_assignment_count=expected_low_fiber,
        low_fiber_log2_ratio_to_expectation=low_ratio,
        conditional_expected_window_count=mean,
        conditional_window_count_variance=variance,
        observed_window_count=observed_window,
        observed_exact_solution_count=exact_count,
        source_target_legal=exact_count > 0,
        nearest_nonzero_supported_residual=min(nonzero_distances) if nonzero_distances else None,
        conditional_exact_solution_density=conditional_exact_density,
        unconditioned_exact_solution_density=unconditioned_density,
        conditional_to_unconditioned_density_ratio=density_ratio,
        count_geometry_improvement_proved=False,
        lll_geometry_improvement_proved=False,
    )


def run_preconditioned_geometry_audit(
    n_values: Sequence[int] = (10, 12, 14, 16, 18),
    register_offsets: Sequence[int] = (2, 4),
    log_multipliers: Sequence[int] = (1,),
    residual_window_radii: Sequence[int] = (0, 1, 4),
    trials_per_row: int = 4,
    seed: int = 0,
) -> DCPSubsetSumPreconditionedGeometryReport:
    if trials_per_row < 1:
        raise ValueError("trials_per_row must be positive")
    certificates = [
        theorem_certificate(n_bits, offset, multiplier)
        for n_bits in n_values
        for offset in register_offsets
        for multiplier in log_multipliers
    ]
    rows = [
        analyze_preconditioned_geometry(
            n_bits,
            offset,
            multiplier,
            trial,
            radius,
            seed
            + 1_000_003 * n_index
            + 10_007 * offset_index
            + 101 * multiplier_index
            + 17 * trial
            ,
        )
        for n_index, n_bits in enumerate(n_values)
        for offset_index, offset in enumerate(register_offsets)
        for multiplier_index, multiplier in enumerate(log_multipliers)
        for trial in range(trials_per_row)
        for radius in residual_window_radii
    ]
    exact_rows = [row for row in rows if row.residual_window_radius == 0]
    tail_n = max(n_values)
    tail_exact_rows = [row for row in exact_rows if row.n_bits == tail_n]
    log_ratios = [
        abs(row.low_fiber_log2_ratio_to_expectation)
        for row in rows
        if row.low_fiber_log2_ratio_to_expectation is not None
    ]
    metrics: dict[str, int | float] = {
        "row_count": len(rows),
        "theorem_certificate_count": len(certificates),
        "exact_conditional_first_moment_certificate_count": sum(
            item.exact_conditional_first_moment_proved for item in certificates
        ),
        "exact_conditional_second_factorial_moment_certificate_count": sum(
            item.exact_conditional_second_factorial_moment_proved for item in certificates
        ),
        "exact_conditional_variance_certificate_count": sum(
            item.exact_conditional_variance_proved for item in certificates
        ),
        "maximum_absolute_density_exponent_change": max(
            abs(item.density_exponent_change) for item in certificates
        ),
        "maximum_observed_low_fiber_log2_deviation": max(log_ratios, default=0.0),
        "mean_tail_conditional_to_unconditioned_density_ratio": (
            sum(row.conditional_to_unconditioned_density_ratio for row in tail_exact_rows)
            / max(1, len(tail_exact_rows))
        ),
        "tail_legal_target_count": sum(row.source_target_legal for row in tail_exact_rows),
        "count_based_geometry_improvement_proved_count": 0,
        "lll_geometry_improvement_proved_count": 0,
        "polynomial_witness_solver_proved_count": 0,
        "source_contract_satisfying_row_count": 0,
    }
    return DCPSubsetSumPreconditionedGeometryReport(
        created_at=utc_now(),
        theorem_contract={
            "source": "uniform labels and independent uniform target modulo 2^n",
            "conditioning": "fix all label low residues and target modulo 2^b; retain the exact binary low fiber S",
            "residual": "high quotient in Z_(2^(n-b)), including the assignment-dependent low-sum carry",
            "theorem": "for every fixed low fiber and residual window W, residual indicators are pairwise independent",
            "promotion": "must exhibit higher-order, basis-geometric, or implicit-decoder structure not explained by these exact moments",
        },
        theorem_certificates=certificates,
        rows=rows,
        headline_metrics=metrics,
        claim_gate={
            "conditional_pairwise_independence_proved": True,
            "expected_exact_solution_density_improves_after_conditioning": False,
            "count_or_residual_window_geometry_improves_after_conditioning": False,
            "all_lll_geometry_improvement_ruled_out": False,
            "higher_order_structure_ruled_out": False,
            "polynomial_witness_solver_constructed": False,
            "source_contract_satisfied": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The exact moment theorem removes candidate-count and fixed residual-window explanations for the "
                "logarithmic low-bit preconditioner. A surviving route must use higher-order correlations, changed "
                "basis geometry, or an implicit decoder and prove inverse-polynomial legal coverage."
            ),
        },
        status="log-low-bit-conditioning-preserves-expected-residual-density",
        summary=(
            f"Certified exact conditional first/second-factorial moments and variance for {len(certificates)} scaling "
            f"setting(s), audited {len(rows)} finite rows through n={tail_n}, and found density exponent change 0. "
            "No LLL geometry theorem or polynomial witness solver is claimed."
        ),
        falsifiers_triggered=[
            "Shrinking the low-valid fiber by 2^b also shrinks the high quotient modulus by 2^b.",
            "Exact solution and fixed residual-window densities have no ensemble exponent improvement.",
            "Pairwise residual independence blocks variance-reduction claims based only on low-bit filtering.",
            "Finite LLL success remains proof debt unless tied to higher-order or basis-geometric structure.",
        ],
    )


def write_preconditioned_geometry_audit(
    path: Path = DCP_SUBSET_SUM_PRECONDITIONED_GEOMETRY_PATH,
    n_values: Sequence[int] = (10, 12, 14, 16, 18),
    register_offsets: Sequence[int] = (2, 4),
    log_multipliers: Sequence[int] = (1,),
    residual_window_radii: Sequence[int] = (0, 1, 4),
    trials_per_row: int = 4,
    seed: int = 0,
    write_registry: bool = True,
    registry_experiment_id: str = DEFAULT_EXPERIMENT_ID,
    registry_candidate_id: str = DEFAULT_CANDIDATE_ID,
    registry_result_id: str | None = None,
) -> dict:
    report = run_preconditioned_geometry_audit(
        n_values=n_values,
        register_offsets=register_offsets,
        log_multipliers=log_multipliers,
        residual_window_radii=residual_window_radii,
        trials_per_row=trials_per_row,
        seed=seed,
    )
    payload = asdict(report)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    if write_registry:
        upsert_negative_result(
            NegativeResultRecord(
                id="NEG-DCP-LOW-BIT-PRECONDITIONER-COUNT-GEOMETRY",
                source=str(path),
                claim=(
                    "Conditioning O(log n) low subset-sum bits creates an improved exact-solution or near-residual "
                    "density that explains a polynomial high-bit solver."
                ),
                reason_invalid=(
                    "For every fixed low fiber, high residual indicators are pairwise independent with exact mean "
                    "F|W|/Q and binomial variance; the ensemble density exponent is unchanged."
                ),
                lesson=(
                    "Retain the low-bit BDD only as a representation primitive. Require a theorem about higher-order "
                    "correlations, LLL basis geometry, or an implicit decoder before further solver promotion."
                ),
                applies_to=[registry_candidate_id, registry_experiment_id],
                evidence={
                    "theorem_certificate_count": payload["headline_metrics"]["theorem_certificate_count"],
                    "maximum_absolute_density_exponent_change": payload["headline_metrics"][
                        "maximum_absolute_density_exponent_change"
                    ],
                    "lll_geometry_improvement_proved_count": 0,
                    "polynomial_witness_solver_proved_count": 0,
                },
            )
        )
        result_id = registry_result_id or f"RESULT-{registry_experiment_id}-DCP-SUBSET-SUM-PRECONDITIONED-GEOMETRY"
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
                artifacts={"dcp_subset_sum_preconditioned_geometry": str(path)},
            )
        )
    return payload

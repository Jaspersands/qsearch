"""Fourth-order obstruction audit for low-bit-conditioned subset sum.

After fixing a low-bit fiber S, high residuals indexed by assignments in S are
three-wise independent.  Four-wise independence can fail only for distinct
affine parallelograms x1 xor x2 xor x3 xor x4 = 0 in S.  The number of such
ordered quadruples is the distinct additive energy of S and is computed exactly
with a Walsh-Hadamard transform.

For exact high-residue solutions over Z_Q, affine-independent quadruples have
joint probability Q^-4.  Every dependent quadruple contains three affinely
independent points, so its joint probability is at most Q^-3.  Consequently

  E[(C)_4 | low data] <= (F)_4 / Q^4 + D (Q^-3 - Q^-4),

where F=|S| and D is its distinct additive energy.  This localizes every
possible fourth-order gain to low-fiber additive energy.

The source average can be evaluated more sharply.  Ordered distinct affine
quadruples split into integer-rank-three tuples and tuples with Smith invariants
(1,1,1,2).  Their joint exact-target probabilities are respectively Q^-3 and
2Q^-4.  Exact counting proves that, at fixed register offset, the resulting
fourth-factorial excess decays as O((3/4)^n)+O(2^-n).  This source-average
theorem does not prove concentration for individual low fibers, control
growing-order statistics, or supply a polynomial witness decoder.
"""

from __future__ import annotations

import json
import random
from dataclasses import asdict, dataclass
from fractions import Fraction
from pathlib import Path
from typing import Sequence

import numpy as np

from dcp_subset_sum_preconditioned_geometry import constrained_low_bits
from research_registry import (
    ExperimentResultRecord,
    NegativeResultRecord,
    upsert_experiment_result,
    upsert_negative_result,
    utc_now,
)


DCP_SUBSET_SUM_FOURTH_MOMENT_PATH = Path(
    "research/classical_baselines/dcp_subset_sum_fourth_moment_obstruction.json"
)
DEFAULT_EXPERIMENT_ID = "EXP-DHS-DCP-SUBSET-SUM-FOURTH-MOMENT-OBSTRUCTION"
DEFAULT_CANDIDATE_ID = "DHS-GOWERS-SIEVE"


@dataclass(frozen=True)
class LowOrderResidualTheoremCertificate:
    n_bits: int
    register_offset: int
    register_count: int
    constrained_low_bits: int
    quotient_modulus: int
    pairwise_independence_proved: bool
    triplewise_independence_proved: bool
    fourth_order_localized_to_affine_parallelograms: bool
    fourth_factorial_upper_bound: str
    proof: str
    limitations: list[str]


@dataclass(frozen=True)
class SourceFourthMomentCertificate:
    n_bits: int
    register_offset: int
    register_count: int
    assignment_count: int
    source_modulus: int
    ordered_distinct_affine_quadruple_count: int
    integer_rank_three_quadruple_count: int
    smith_two_quadruple_count: int
    affine_independent_quadruple_count: int
    exact_expected_fourth_factorial_moment_numerator: int
    exact_expected_fourth_factorial_moment_denominator: int
    exact_independent_baseline_numerator: int
    exact_independent_baseline_denominator: int
    exact_fourth_excess_numerator: int
    exact_fourth_excess_denominator: int
    fourth_excess: float
    rank_three_excess_upper_bound: float
    smith_two_excess_upper_bound: float
    fixed_offset_fourth_excess_vanishes: bool
    proof: str
    limitations: list[str]


@dataclass(frozen=True)
class FourthMomentEnergyRow:
    n_bits: int
    register_offset: int
    register_count: int
    log_multiplier: int
    constrained_low_bits: int
    quotient_modulus: int
    trial_index: int
    low_fiber_size: int
    assignment_universe_size: int
    total_additive_energy: float
    diagonal_additive_energy: int
    distinct_additive_energy: float
    uniform_fixed_size_expected_distinct_energy: float
    source_expected_distinct_energy: float
    observed_to_source_expected_energy_ratio: float
    additive_energy_inflation: float
    exact_triple_factorial_moment: float
    independent_fourth_factorial_baseline: float
    fourth_factorial_upper_bound: float
    fourth_excess_upper_bound: float
    fourth_excess_to_independent_baseline_upper_bound: float
    finite_upper_bound_is_asymptotic_theorem: bool
    polynomial_energy_inflation_bound_proved: bool
    polynomial_witness_solver_proved: bool


@dataclass(frozen=True)
class DCPSubsetSumFourthMomentReport:
    created_at: str
    theorem_contract: dict[str, str]
    theorem_certificates: list[LowOrderResidualTheoremCertificate]
    source_fourth_moment_certificates: list[SourceFourthMomentCertificate]
    rows: list[FourthMomentEnergyRow]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, bool | str]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _falling(value: int, order: int) -> int:
    result = 1
    for index in range(order):
        result *= max(0, value - index)
    return result


def affine_quadruple_type_counts(register_count: int) -> tuple[int, int, int, int]:
    """Count ordered distinct quadruples by their integer Smith type.

    The returned tuple is ``(affine_dependent, rank_three, smith_two,
    affine_independent)``.  Directions ``u,v`` are nonzero and distinct.  An
    affine quadruple has integer rank three exactly when one of the coordinate
    categories ``u only``, ``v only``, or ``u and v`` is absent.
    """

    if register_count < 2:
        raise ValueError("register_count must be at least 2")
    assignment_count = 1 << register_count
    affine_dependent = assignment_count * (assignment_count - 1) * (assignment_count - 2)
    rank_three_direction_pairs = 3 * (
        3**register_count - 2 * assignment_count + 1
    )
    rank_three = assignment_count * rank_three_direction_pairs
    smith_two = affine_dependent - rank_three
    affine_independent = _falling(assignment_count, 4) - affine_dependent
    if min(rank_three, smith_two, affine_independent) < 0:
        raise AssertionError("quadruple type count became negative")
    return affine_dependent, rank_three, smith_two, affine_independent


def source_fourth_moment_certificate(
    n_bits: int,
    register_offset: int,
) -> SourceFourthMomentCertificate:
    """Return the exact source-averaged fourth-factorial moment certificate."""

    if n_bits < 1:
        raise ValueError("n_bits must be positive")
    register_count = n_bits + register_offset
    if register_count < 2:
        raise ValueError("n_bits + register_offset must be at least 2")
    assignment_count = 1 << register_count
    modulus = 1 << n_bits
    affine_dependent, rank_three, smith_two, affine_independent = (
        affine_quadruple_type_counts(register_count)
    )
    denominator = modulus**4
    moment = Fraction(
        affine_independent + rank_three * modulus + 2 * smith_two,
        denominator,
    )
    baseline = Fraction(_falling(assignment_count, 4), denominator)
    excess = moment - baseline
    rank_three_excess = Fraction(rank_three * (modulus - 1), denominator)
    smith_two_excess = Fraction(smith_two, denominator)
    if excess != rank_three_excess + smith_two_excess:
        raise AssertionError("fourth-moment decomposition failed")
    return SourceFourthMomentCertificate(
        n_bits=n_bits,
        register_offset=register_offset,
        register_count=register_count,
        assignment_count=assignment_count,
        source_modulus=modulus,
        ordered_distinct_affine_quadruple_count=affine_dependent,
        integer_rank_three_quadruple_count=rank_three,
        smith_two_quadruple_count=smith_two,
        affine_independent_quadruple_count=affine_independent,
        exact_expected_fourth_factorial_moment_numerator=moment.numerator,
        exact_expected_fourth_factorial_moment_denominator=moment.denominator,
        exact_independent_baseline_numerator=baseline.numerator,
        exact_independent_baseline_denominator=baseline.denominator,
        exact_fourth_excess_numerator=excess.numerator,
        exact_fourth_excess_denominator=excess.denominator,
        fourth_excess=float(excess),
        rank_three_excess_upper_bound=float(rank_three_excess),
        smith_two_excess_upper_bound=float(smith_two_excess),
        fixed_offset_fourth_excess_vanishes=True,
        proof=(
            "Among ordered distinct affine quadruples, integer-rank-three tuples number "
            "U*3*(3^m-2U+1); all remaining affine tuples have Smith invariants (1,1,1,2). "
            "Their exact-target probabilities are P^-3 and 2P^-4, respectively. Thus the "
            "excess is L(P^-3-P^-4)+T*P^-4. At fixed register offset, these terms are "
            "O((3/4)^n) and O(2^-n)."
        ),
        limitations=[
            "The theorem averages over uniformly random source labels and target.",
            "It does not prove concentration for an individual low-bit fiber.",
            "It controls fixed fourth order only, not moments whose order grows with n.",
            "It supplies neither an efficient decoder nor a computational lower bound.",
        ],
    )


def low_order_theorem_certificate(
    n_bits: int,
    register_offset: int,
    log_multiplier: int,
) -> LowOrderResidualTheoremCertificate:
    low_bits = constrained_low_bits(n_bits, log_multiplier)
    return LowOrderResidualTheoremCertificate(
        n_bits=n_bits,
        register_offset=register_offset,
        register_count=n_bits + register_offset,
        constrained_low_bits=low_bits,
        quotient_modulus=1 << (n_bits - low_bits),
        pairwise_independence_proved=True,
        triplewise_independence_proved=True,
        fourth_order_localized_to_affine_parallelograms=True,
        fourth_factorial_upper_bound="(F)_4/Q^4 + D*(Q^-3-Q^-4)",
        proof=(
            "Append the target coefficient -1 to every binary assignment. Any two or three distinct assignments are "
            "affinely independent over F_2, so their extended coefficient rows contain a unit minor and their residuals "
            "are jointly uniform over Z_Q. Four rows fail this test exactly when their assignments xor to zero. Every "
            "such distinct quadruple contains an independent triple, so its exact-zero probability is at most Q^-3."
        ),
        limitations=[
            "The Q^-3 bound can be loose for quadruples with a 2-adic fourth Smith invariant.",
            "No asymptotic additive-energy bound is proved for random modular low fibers.",
            "Fixed fourth order does not control statistics whose order grows with n.",
            "No implication from additive energy to an efficient witness decoder is supplied.",
        ],
    )


def _low_fiber_indicator(
    low_labels: Sequence[int],
    target_low: int,
    low_modulus: int,
) -> np.ndarray:
    residues = np.zeros(1, dtype=np.int64)
    for label in low_labels:
        residues = np.concatenate((residues, (residues + int(label)) % low_modulus))
    return (residues == int(target_low) % low_modulus).astype(np.float64)


def walsh_hadamard(values: np.ndarray) -> np.ndarray:
    spectrum = np.asarray(values, dtype=np.float64).copy()
    size = int(spectrum.size)
    if size < 1 or size & (size - 1):
        raise ValueError("Walsh transform length must be a positive power of two")
    width = 1
    while width < size:
        blocks = spectrum.reshape(-1, 2 * width)
        left = blocks[:, :width].copy()
        right = blocks[:, width:].copy()
        blocks[:, :width] = left + right
        blocks[:, width:] = left - right
        width *= 2
    return spectrum


def additive_energy(indicator: np.ndarray) -> tuple[float, int, float]:
    values = np.asarray(indicator, dtype=np.float64)
    size = int(values.size)
    fiber_size = int(round(float(np.sum(values))))
    spectrum = walsh_hadamard(values)
    total = float(np.sum(spectrum**4) / size)
    diagonal = 3 * fiber_size * fiber_size - 2 * fiber_size
    distinct = max(0.0, total - diagonal)
    return total, diagonal, distinct


def uniform_fixed_size_expected_distinct_energy(universe_size: int, fiber_size: int) -> float:
    if fiber_size < 4 or universe_size < 4:
        return 0.0
    return float(_falling(fiber_size, 4) / (universe_size - 3))


def analyze_fourth_moment_energy(
    n_bits: int,
    register_offset: int,
    log_multiplier: int,
    trial_index: int,
    seed: int,
) -> FourthMomentEnergyRow:
    low_bits = constrained_low_bits(n_bits, log_multiplier)
    low_modulus = 1 << low_bits
    quotient_modulus = 1 << (n_bits - low_bits)
    register_count = n_bits + register_offset
    universe_size = 1 << register_count
    rng = random.Random(seed)
    low_labels = [rng.randrange(low_modulus) for _ in range(register_count)]
    target_low = rng.randrange(low_modulus)
    indicator = _low_fiber_indicator(low_labels, target_low, low_modulus)
    fiber_size = int(round(float(np.sum(indicator))))
    total_energy, diagonal_energy, distinct_energy = additive_energy(indicator)
    random_energy = uniform_fixed_size_expected_distinct_energy(universe_size, fiber_size)
    _, rank_three, smith_two, _ = affine_quadruple_type_counts(register_count)
    source_expected_energy = rank_three / low_modulus**3 + 2 * smith_two / low_modulus**4
    source_energy_ratio = (
        distinct_energy / source_expected_energy if source_expected_energy > 0 else 0.0
    )
    inflation = distinct_energy / random_energy if random_energy > 0 else 0.0
    triple = _falling(fiber_size, 3) / quotient_modulus**3
    independent_fourth = _falling(fiber_size, 4) / quotient_modulus**4
    excess = distinct_energy * (quotient_modulus - 1) / quotient_modulus**4
    upper = independent_fourth + excess
    relative_excess = excess / independent_fourth if independent_fourth > 0 else 0.0
    return FourthMomentEnergyRow(
        n_bits=n_bits,
        register_offset=register_offset,
        register_count=register_count,
        log_multiplier=log_multiplier,
        constrained_low_bits=low_bits,
        quotient_modulus=quotient_modulus,
        trial_index=trial_index,
        low_fiber_size=fiber_size,
        assignment_universe_size=universe_size,
        total_additive_energy=total_energy,
        diagonal_additive_energy=diagonal_energy,
        distinct_additive_energy=distinct_energy,
        uniform_fixed_size_expected_distinct_energy=random_energy,
        source_expected_distinct_energy=source_expected_energy,
        observed_to_source_expected_energy_ratio=source_energy_ratio,
        additive_energy_inflation=inflation,
        exact_triple_factorial_moment=triple,
        independent_fourth_factorial_baseline=independent_fourth,
        fourth_factorial_upper_bound=upper,
        fourth_excess_upper_bound=excess,
        fourth_excess_to_independent_baseline_upper_bound=relative_excess,
        finite_upper_bound_is_asymptotic_theorem=False,
        polynomial_energy_inflation_bound_proved=False,
        polynomial_witness_solver_proved=False,
    )


def _fit_log2_slope(rows: Sequence[FourthMomentEnergyRow], field: str) -> float:
    by_n: dict[int, list[float]] = {}
    for row in rows:
        value = max(float(getattr(row, field)), 1e-300)
        by_n.setdefault(row.n_bits, []).append(value)
    if len(by_n) < 2:
        return 0.0
    n_values = np.asarray(sorted(by_n), dtype=float)
    medians = np.asarray([np.median(by_n[int(n)]) for n in n_values], dtype=float)
    return float(np.polyfit(n_values, np.log2(medians), 1)[0])


def run_fourth_moment_obstruction(
    n_values: Sequence[int] = (8, 10, 12, 14),
    register_offsets: Sequence[int] = (2, 4),
    log_multipliers: Sequence[int] = (1,),
    trials_per_row: int = 2,
    seed: int = 0,
) -> DCPSubsetSumFourthMomentReport:
    if trials_per_row < 1:
        raise ValueError("trials_per_row must be positive")
    certificates = [
        low_order_theorem_certificate(n_bits, offset, multiplier)
        for n_bits in n_values
        for offset in register_offsets
        for multiplier in log_multipliers
    ]
    source_certificates = [
        source_fourth_moment_certificate(n_bits, offset)
        for n_bits in n_values
        for offset in register_offsets
    ]
    rows = [
        analyze_fourth_moment_energy(
            n_bits,
            offset,
            multiplier,
            trial,
            seed + 1_000_003 * n_index + 10_007 * offset_index + 101 * multiplier_index + trial,
        )
        for n_index, n_bits in enumerate(n_values)
        for offset_index, offset in enumerate(register_offsets)
        for multiplier_index, multiplier in enumerate(log_multipliers)
        for trial in range(trials_per_row)
    ]
    tail_n = max(n_values)
    tail_rows = [row for row in rows if row.n_bits == tail_n]
    metrics: dict[str, int | float] = {
        "row_count": len(rows),
        "theorem_certificate_count": len(certificates),
        "source_fourth_moment_certificate_count": len(source_certificates),
        "triplewise_independence_certificate_count": sum(
            item.triplewise_independence_proved for item in certificates
        ),
        "fourth_order_localization_certificate_count": sum(
            item.fourth_order_localized_to_affine_parallelograms for item in certificates
        ),
        "maximum_tail_additive_energy_inflation": max(
            row.additive_energy_inflation for row in tail_rows
        ),
        "maximum_tail_fourth_excess_relative_upper_bound": max(
            row.fourth_excess_to_independent_baseline_upper_bound for row in tail_rows
        ),
        "fitted_log2_additive_energy_inflation_slope_per_n": _fit_log2_slope(
            rows, "additive_energy_inflation"
        ),
        "fitted_log2_fourth_excess_relative_upper_bound_slope_per_n": _fit_log2_slope(
            rows, "fourth_excess_to_independent_baseline_upper_bound"
        ),
        "proved_uniform_polynomial_energy_inflation_bound_count": 0,
        "proved_source_fixed_offset_fourth_excess_vanishing_count": sum(
            item.fixed_offset_fourth_excess_vanishes for item in source_certificates
        ),
        "proved_asymptotic_fixed_fourth_order_obstruction_count": sum(
            item.fixed_offset_fourth_excess_vanishes for item in source_certificates
        ),
        "proved_growing_order_obstruction_count": 0,
        "polynomial_witness_solver_proved_count": 0,
    }
    return DCPSubsetSumFourthMomentReport(
        created_at=utc_now(),
        theorem_contract={
            "conditioned_object": "exact low-bit fiber S inside F_2^m",
            "exact_invariant": "distinct additive energy D=#{distinct ordered quadruples in S with xor zero}",
            "computation": "D is obtained exactly from 2^-m sum_chi |hat(1_S)(chi)|^4 minus diagonal pairings",
            "moment_bound": "E[(C)_4|low] <= (F)_4/Q^4 + D(Q^-3-Q^-4)",
            "source_average_theorem": (
                "E[(C)_4]-(U)_4/P^4=L(P^-3-P^-4)+T*P^-4, with "
                "L=U*3*(3^m-2U+1) and T=U(U-1)(U-2)-L"
            ),
            "promotion": (
                "prove per-fiber concentration or growing-order control, or construct a decoder exploiting "
                "structure not erased by the source-average theorem"
            ),
        },
        theorem_certificates=certificates,
        source_fourth_moment_certificates=source_certificates,
        rows=rows,
        headline_metrics=metrics,
        claim_gate={
            "residuals_three_wise_independent": True,
            "fourth_order_signal_localized_to_additive_energy": True,
            "source_averaged_fixed_fourth_excess_vanishes_at_fixed_offset": True,
            "finite_energy_scaling_is_asymptotic_theorem": False,
            "all_growing_order_structure_ruled_out": False,
            "polynomial_energy_inflation_bound_proved": False,
            "polynomial_witness_solver_constructed": False,
            "speedup_claim_allowed": False,
            "reason": (
                "Every fixed-order signal through degree three is exactly absent, and fourth-order deviations are "
                "completely charged to low-fiber additive energy. Exact Smith-type counting proves source-averaged "
                "fixed-fourth excess vanishes at fixed offset; per-fiber concentration, growing-order structure, "
                "and an efficient decoder remain open."
            ),
        },
        status="source-average-fixed-fourth-order-signal-asymptotically-obstructed",
        summary=(
            f"Certified three-wise residual independence and fourth-order localization for {len(certificates)} setting(s); "
            f"audited {len(rows)} exact low fibers through n={tail_n}. Tail maximum energy inflation="
            f"{metrics['maximum_tail_additive_energy_inflation']:.6g} and relative fourth-excess upper bound="
            f"{metrics['maximum_tail_fourth_excess_relative_upper_bound']:.6g}. Exact source averaging proves the "
            "fixed-fourth excess vanishes at fixed offset; no per-fiber concentration, growing-order obstruction, "
            "or decoder is claimed."
        ),
        falsifiers_triggered=[
            "No pairwise or triplewise residual statistic can distinguish the conditioned ensemble.",
            "Affine-independent fourth-order tuples are exactly uniform and carry no signal.",
            "Every possible fourth-order deviation must pay the measured low-fiber additive-energy budget.",
            "Source-averaged fixed-fourth excess decays exponentially at fixed register offset.",
            "Finite per-fiber additive-energy decay or growth remains proof debt until concentration is proved.",
        ],
    )


def write_fourth_moment_obstruction(
    path: Path = DCP_SUBSET_SUM_FOURTH_MOMENT_PATH,
    n_values: Sequence[int] = (8, 10, 12, 14),
    register_offsets: Sequence[int] = (2, 4),
    log_multipliers: Sequence[int] = (1,),
    trials_per_row: int = 2,
    seed: int = 0,
    write_registry: bool = True,
    registry_experiment_id: str = DEFAULT_EXPERIMENT_ID,
    registry_candidate_id: str = DEFAULT_CANDIDATE_ID,
    registry_result_id: str | None = None,
) -> dict:
    report = run_fourth_moment_obstruction(
        n_values=n_values,
        register_offsets=register_offsets,
        log_multipliers=log_multipliers,
        trials_per_row=trials_per_row,
        seed=seed,
    )
    payload = asdict(report)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    if write_registry:
        upsert_negative_result(
            NegativeResultRecord(
                id="NEG-DCP-LOW-FIBER-ORDER-LE-3-AND-GENERIC-ORDER-4-SIGNAL",
                source=str(path),
                claim=(
                    "Pairwise, triplewise, or affine-independent fourth-order high residual correlations provide a "
                    "hidden signal after logarithmic low-bit conditioning."
                ),
                reason_invalid=(
                    "Residuals are exactly three-wise independent. At fourth order, only distinct xor-zero affine "
                    "parallelograms can deviate, and their total contribution is explicitly bounded by additive energy. "
                    "Exact Smith-type counting proves the source-averaged excess vanishes exponentially at fixed offset."
                ),
                lesson=(
                    "Restrict future low-order searches to additive-energy-bearing fourth tuples. Any broader route must "
                    "prove atypical-fiber concentration, use growing order, exploit reduced-basis geometry, or provide an "
                    "implicit decoder and state that distinction."
                ),
                applies_to=[registry_candidate_id, registry_experiment_id],
                evidence={
                    "triplewise_independence_certificate_count": payload["headline_metrics"][
                        "triplewise_independence_certificate_count"
                    ],
                    "fourth_order_localization_certificate_count": payload["headline_metrics"][
                        "fourth_order_localization_certificate_count"
                    ],
                    "proved_asymptotic_fixed_fourth_order_obstruction_count": payload[
                        "headline_metrics"
                    ]["proved_asymptotic_fixed_fourth_order_obstruction_count"],
                },
            )
        )
        result_id = registry_result_id or f"RESULT-{registry_experiment_id}-DCP-SUBSET-SUM-FOURTH-MOMENT"
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
                artifacts={"dcp_subset_sum_fourth_moment_obstruction": str(path)},
            )
        )
    return payload

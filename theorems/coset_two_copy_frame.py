"""Exact two-copy frame spectrum and the recoupling obstruction to its PGM.

In the product Fourier block ``lambda tensor mu``, the two-copy average frame is

    S_2 = |G|^-2 [I + A_lambda + A_mu + A_{lambda tensor mu}],

where each A is the normalized involution class sum.  Recoupling
``lambda tensor mu = direct_sum_nu g(lambda,mu,nu) nu`` diagonalizes the final
term, so sector ``(lambda,mu,nu)`` has scalar

    1 + r_lambda + r_mu + r_nu.

The regular-representation multiplicity gives normalized Hilbert mass
``d_lambda d_mu g(lambda,mu,nu) d_nu / |G|^2``.  This diagonalizes the average
frame, but it does *not* diagonalize an individual coset state.  Consequently,
the tempting rank formula ``4 rank(S)/(M |G|^2)`` for PGM success is false.
Computing the PGM requires transition weights between Kronecker sectors, not
only their character ratios and multiplicities.  This module records rigorous
spectral bounds and an explicit S_3 counterexample to the commuting shortcut.
"""

from __future__ import annotations

import json
import itertools
import math
from dataclasses import asdict, dataclass
from fractions import Fraction
from math import factorial
from pathlib import Path
from typing import Sequence

import numpy as np

from coset_state_distinguishability import involution_count
from representation_obstruction import hook_length_dimension, integer_partitions
from research_registry import (
    ExperimentResultRecord,
    NegativeResultRecord,
    upsert_experiment_result,
    upsert_negative_result,
    utc_now,
)
from symmetric_character import kronecker_coefficient, symmetric_character
from weak_fourier_signal import involution_specs_for_n


COSET_TWO_COPY_FRAME_PATH = Path("research/representation/coset_two_copy_frame.json")
DEFAULT_EXPERIMENT_ID = "EXP-COSET-TWO-COPY-FRAME"
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


@dataclass(frozen=True)
class TwoCopyFrameSector:
    left_partition: tuple[int, ...]
    right_partition: tuple[int, ...]
    coupled_partition: tuple[int, ...]
    left_dimension: int
    right_dimension: int
    coupled_dimension: int
    kronecker_multiplicity: int
    left_character_ratio: float
    right_character_ratio: float
    coupled_character_ratio: float
    frame_eigenvalue_times_group_order_squared: float
    normalized_hilbert_mass: float
    in_frame_support: bool


@dataclass(frozen=True)
class TwoCopyFrameRecord:
    n: int
    involution_type: str
    transposition_count: int
    ensemble_size: int
    partition_count: int
    nonzero_recoupling_sector_count: int
    frame_trace: float
    support_hilbert_mass: float
    kernel_hilbert_mass: float
    minimum_positive_frame_scalar: float
    maximum_frame_scalar: float
    support_condition_number: float
    pgm_success_spectral_lower_bound: float
    pgm_success_spectral_upper_bound: float
    rejected_commuting_rank_formula: float
    uniform_guess_success_probability: float
    pgm_advantage_lower_bound: float
    pgm_advantage_upper_bound: float
    pgm_exact_from_sector_spectrum: bool
    individual_state_commutes_with_average_frame_proved: bool
    polynomial_transition_algebra_proved: bool
    coherent_kronecker_transform_proved: bool
    polynomial_outcome_decoder_proved: bool
    smallest_positive_sectors: list[TwoCopyFrameSector]
    status: str
    interpretation: str


@dataclass(frozen=True)
class CosetTwoCopyFrameReport:
    created_at: str
    theorem_contract: dict[str, str]
    records: list[TwoCopyFrameRecord]
    noncommutation_control: dict[str, int | float | bool]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, bool | str]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def theoretical_two_copy_scalar_multiplicities(
    n: int,
    transposition_count: int,
) -> dict[Fraction, int]:
    """Return exact frame scalars and full regular-tensor multiplicities."""

    partitions = integer_partitions(n)
    cycle_type = tuple(
        sorted(
            (2,) * transposition_count + (1,) * (n - 2 * transposition_count),
            reverse=True,
        )
    )
    dimensions = {partition: hook_length_dimension(partition) for partition in partitions}
    ratios = {
        partition: Fraction(symmetric_character(partition, cycle_type), dimensions[partition])
        for partition in partitions
    }
    spectrum: dict[Fraction, int] = {}
    for left in partitions:
        for right in partitions:
            for coupled in partitions:
                multiplicity = kronecker_coefficient(left, right, coupled)
                if not multiplicity:
                    continue
                scalar = 1 + ratios[left] + ratios[right] + ratios[coupled]
                hilbert_multiplicity = (
                    dimensions[left]
                    * dimensions[right]
                    * multiplicity
                    * dimensions[coupled]
                )
                spectrum[scalar] = spectrum.get(scalar, 0) + hilbert_multiplicity
    return dict(sorted(spectrum.items()))


def _compose(left: tuple[int, ...], right: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(left[right[index]] for index in range(len(left)))


def explicit_s3_noncommutation_control() -> dict[str, int | float | bool]:
    """Compute the two-copy PGM and frame commutator in the S_3 regular model."""

    permutations = list(itertools.permutations(range(3)))
    index = {permutation: i for i, permutation in enumerate(permutations)}
    identity = tuple(range(3))
    transpositions = [
        permutation
        for permutation in permutations
        if permutation != identity and _compose(permutation, permutation) == identity
    ]
    order = len(permutations)
    states: list[np.ndarray] = []
    for hidden in transpositions:
        right = np.zeros((order, order))
        for i, group_element in enumerate(permutations):
            right[index[_compose(group_element, hidden)], i] = 1.0
        one_copy = (np.eye(order) + right) / order
        states.append(np.kron(one_copy, one_copy))
    average = sum(states) / len(states)
    eigenvalues, eigenvectors = np.linalg.eigh(average)
    inverse_sqrt = eigenvectors @ np.diag(
        [1 / math.sqrt(value) if value > 1e-12 else 0.0 for value in eigenvalues]
    ) @ eigenvectors.T
    pgm_success = 0.0
    for state in states:
        measurement = inverse_sqrt @ (state / len(states)) @ inverse_sqrt
        pgm_success += float(np.trace(measurement @ state).real) / len(states)
    commutator = average @ states[0] - states[0] @ average
    rank_formula = 4 * np.linalg.matrix_rank(average, tol=1e-12) / (
        len(states) * order * order
    )
    return {
        "n": 3,
        "ensemble_size": len(states),
        "hilbert_dimension": order * order,
        "frame_rank": int(np.linalg.matrix_rank(average, tol=1e-12)),
        "commutator_frobenius_norm": float(np.linalg.norm(commutator)),
        "exact_numerical_pgm_success_probability": pgm_success,
        "rejected_commuting_rank_formula": float(rank_formula),
        "absolute_formula_gap": abs(float(rank_formula) - pgm_success),
        "individual_state_commutes_with_average_frame": bool(
            np.linalg.norm(commutator) <= 1e-12
        ),
        "rank_formula_falsified": bool(abs(float(rank_formula) - pgm_success) > 1e-8),
    }


def audit_two_copy_frame(
    n: int,
    transposition_count: int,
    involution_type: str,
    top_k: int = 8,
) -> TwoCopyFrameRecord:
    partitions = integer_partitions(n)
    order = factorial(n)
    cycle_type = tuple(
        sorted(
            (2,) * transposition_count + (1,) * (n - 2 * transposition_count),
            reverse=True,
        )
    )
    dimensions = {partition: hook_length_dimension(partition) for partition in partitions}
    ratios = {
        partition: symmetric_character(partition, cycle_type) / dimensions[partition]
        for partition in partitions
    }
    sectors: list[TwoCopyFrameSector] = []
    trace = 0.0
    support_mass = 0.0
    positive: list[float] = []
    for left in partitions:
        for right in partitions:
            for coupled in partitions:
                multiplicity = kronecker_coefficient(left, right, coupled)
                if not multiplicity:
                    continue
                scalar = 1 + ratios[left] + ratios[right] + ratios[coupled]
                if scalar < -1e-12:
                    raise ArithmeticError("two-copy frame has a negative representation-sector scalar")
                scalar = max(0.0, scalar)
                mass = (
                    dimensions[left]
                    * dimensions[right]
                    * multiplicity
                    * dimensions[coupled]
                    / (order * order)
                )
                in_support = scalar > 1e-15
                trace += mass * scalar
                if in_support:
                    support_mass += mass
                    positive.append(scalar)
                sectors.append(
                    TwoCopyFrameSector(
                        left_partition=left,
                        right_partition=right,
                        coupled_partition=coupled,
                        left_dimension=dimensions[left],
                        right_dimension=dimensions[right],
                        coupled_dimension=dimensions[coupled],
                        kronecker_multiplicity=multiplicity,
                        left_character_ratio=ratios[left],
                        right_character_ratio=ratios[right],
                        coupled_character_ratio=ratios[coupled],
                        frame_eigenvalue_times_group_order_squared=scalar,
                        normalized_hilbert_mass=mass,
                        in_frame_support=in_support,
                    )
                )
    ensemble_size = involution_count(n, transposition_count)
    minimum = min(positive) if positive else 0.0
    maximum = max(positive) if positive else 0.0
    lower = min(1.0, 4 / (ensemble_size * maximum)) if maximum else 0.0
    upper = min(1.0, 4 / (ensemble_size * minimum)) if minimum else 0.0
    rank_formula = 4 * support_mass / ensemble_size
    frontier = involution_type != "single_transposition_control"
    return TwoCopyFrameRecord(
        n=n,
        involution_type=involution_type,
        transposition_count=transposition_count,
        ensemble_size=ensemble_size,
        partition_count=len(partitions),
        nonzero_recoupling_sector_count=len(sectors),
        frame_trace=trace,
        support_hilbert_mass=support_mass,
        kernel_hilbert_mass=1 - support_mass,
        minimum_positive_frame_scalar=minimum,
        maximum_frame_scalar=maximum,
        support_condition_number=maximum / minimum if minimum else math.inf,
        pgm_success_spectral_lower_bound=lower,
        pgm_success_spectral_upper_bound=upper,
        rejected_commuting_rank_formula=rank_formula,
        uniform_guess_success_probability=1 / ensemble_size,
        pgm_advantage_lower_bound=lower * ensemble_size,
        pgm_advantage_upper_bound=upper * ensemble_size,
        pgm_exact_from_sector_spectrum=False,
        individual_state_commutes_with_average_frame_proved=False,
        polynomial_transition_algebra_proved=False,
        coherent_kronecker_transform_proved=False,
        polynomial_outcome_decoder_proved=False,
        smallest_positive_sectors=sorted(
            (sector for sector in sectors if sector.in_frame_support),
            key=lambda sector: (
                sector.frame_eigenvalue_times_group_order_squared,
                -sector.normalized_hilbert_mass,
                sector.left_partition,
                sector.right_partition,
                sector.coupled_partition,
            ),
        )[:top_k],
        status=(
            "two-copy-recoupling-control"
            if not frontier
            else "coherent-kronecker-transform-and-decoder-proof-debt"
        ),
        interpretation=(
            "The average frame is exactly diagonal in Kronecker sectors, but an individual state has off-diagonal "
            "sector transitions. Character multiplicities give only spectral PGM bounds; recoupling transition "
            "weights, a coherent transform, and a compressed decoder remain open."
        ),
    )


def build_two_copy_frame_report(
    n_values: Sequence[int] = (4, 5, 6, 7, 8),
) -> CosetTwoCopyFrameReport:
    records = [
        audit_two_copy_frame(n, transpositions, label)
        for n in n_values
        for label, transpositions in involution_specs_for_n(n)
    ]
    control = explicit_s3_noncommutation_control()
    frontier = [record for record in records if "control" not in record.status]
    metrics: dict[str, int | float] = {
        "record_count": len(records),
        "n_count": len(n_values),
        "exact_two_copy_recoupling_spectrum_count": len(records),
        "exact_two_copy_pgm_formula_count": 0,
        "spectral_pgm_bound_count": len(records),
        "rank_formula_counterexample_count": int(control["rank_formula_falsified"]),
        "polynomial_transition_algebra_count": 0,
        "coherent_kronecker_transform_proof_debt_count": len(frontier),
        "coherent_kronecker_transform_count": 0,
        "polynomial_outcome_decoder_count": 0,
        "maximum_n": max(n_values),
        "maximum_partition_count": max(record.partition_count for record in records),
        "maximum_recoupling_sector_count": max(
            record.nonzero_recoupling_sector_count for record in records
        ),
        "maximum_frontier_pgm_advantage_upper_bound": max(
            (record.pgm_advantage_upper_bound for record in frontier), default=0.0
        ),
        "minimum_frontier_support_mass": min(
            (record.support_hilbert_mass for record in frontier), default=0.0
        ),
        "maximum_frontier_condition_number": max(
            (record.support_condition_number for record in frontier), default=0.0
        ),
    }
    return CosetTwoCopyFrameReport(
        created_at=utc_now(),
        theorem_contract={
            "two_copy_sector": "lambda tensor mu recoupled into nu with Kronecker multiplicity",
            "frame_scalar": "1+r_lambda+r_mu+r_nu",
            "sector_mass": "d_lambda*d_mu*g(lambda,mu,nu)*d_nu/|S_n|^2",
            "pgm_bounds": "4/(M*max_scalar) <= P_PGM <= min(1,4/(M*min_positive_scalar))",
            "rejected_shortcut": "4*support_hilbert_mass/M assumes false commutation with an individual state",
            "open_mechanism": "Kronecker-sector transition weights, coherent transform, k>=3 algebra, decoder",
        },
        records=records,
        noncommutation_control=control,
        headline_metrics=metrics,
        claim_gate={
            "two_copy_frame_spectrally_explicit": True,
            "two_copy_pgm_exact_from_spectrum": False,
            "commuting_rank_formula_falsified": True,
            "two_copy_pgm_is_hidden_involution_algorithm": False,
            "coherent_kronecker_transform_proved": False,
            "polynomial_outcome_decoder_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The sector spectrum does not determine PGM success because individual states connect sectors. "
                "Transition coefficients, coherent recoupling, and hidden-involution decoding remain unresolved."
            ),
        },
        status="two-copy-spectrum-solved-rank-formula-falsified-transition-algebra-open",
        summary=(
            f"Derived exact two-copy frame spectra for {len(records)} ensembles through n={max(n_values)} and "
            f"falsified the rank-only PGM shortcut on S_3; {len(frontier)} frontier rows retain transition-algebra, "
            "coherent-transform, and decoder proof debt."
        ),
        falsifiers_triggered=[
            "The exact average-frame spectrum does not determine mixed-state PGM success.",
            "An S_3 regular-representation control has a nonzero frame/state commutator and rejects the rank formula.",
            "Explicit Kronecker-sector enumeration is not a polynomial coherent transform.",
            "An exact spectrum is not an outcome decoder.",
            "The k>=3 overlapping recoupling algebra remains unsolved.",
        ],
    )


def write_two_copy_frame_report(
    output_path: Path = COSET_TWO_COPY_FRAME_PATH,
    n_values: Sequence[int] = (4, 5, 6, 7, 8),
    write_registry: bool = True,
    registry_experiment_id: str = DEFAULT_EXPERIMENT_ID,
    registry_candidate_id: str = DEFAULT_CANDIDATE_ID,
    registry_result_id: str | None = None,
) -> dict:
    payload = asdict(build_two_copy_frame_report(n_values=n_values))
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    if write_registry:
        upsert_negative_result(
            NegativeResultRecord(
                id="NEG-COSET-TWO-COPY-SPECTRUM-AS-ALGORITHM",
                source=str(output_path),
                claim="An explicit two-copy Kronecker-sector frame spectrum supplies a hidden-involution algorithm.",
                reason_invalid=(
                    "The PGM gains at most a factor four over guessing, while coherent recoupling and outcome decoding "
                    "remain unimplemented."
                ),
                lesson=(
                    "Treat the spectrum as a design primitive. Build a uniform coherent Kronecker transform and solve "
                    "the k>=3 overlapping recoupling/decoder problem."
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
                artifacts={"coset_two_copy_frame": str(output_path)},
            )
        )
    return payload

"""Smith-normal-form spectrum for density-one modular subset-sum moments.

For random labels ``a in Z_(2^n)^m`` and an independent random target ``t``, let
``C`` count binary assignments ``x`` satisfying ``a.x=t``.  For a fixed ordered
tuple of distinct assignments, the joint hit probability is determined exactly
by the Smith normal form of the integer matrix whose rows are ``(x,-1)``.

This module enumerates assignment tuples when the finite census is tractable and
otherwise samples tuple types.  Complete rows are exact finite identities.
Sampled rows are theorem-discovery diagnostics only: rare affine dependencies
can dominate a factorial moment while being exponentially unlikely under tuple
sampling.  No sampled flatness is promoted to an asymptotic obstruction.
"""

from __future__ import annotations

import itertools
import json
import math
import random
from collections import Counter
from dataclasses import asdict, dataclass
from fractions import Fraction
from pathlib import Path
from typing import Iterable, Sequence

from sympy import Matrix, ZZ
from sympy.matrices.normalforms import smith_normal_form

from dcp_subset_sum_fourth_moment_obstruction import (
    affine_quadruple_type_counts,
    source_fourth_moment_certificate,
)
from research_registry import (
    ExperimentResultRecord,
    NegativeResultRecord,
    upsert_experiment_result,
    upsert_negative_result,
    utc_now,
)


DCP_SUBSET_SUM_SMITH_MOMENT_PATH = Path(
    "research/classical_baselines/dcp_subset_sum_smith_moment_spectrum.json"
)
DEFAULT_EXPERIMENT_ID = "EXP-DHS-DCP-SUBSET-SUM-SMITH-MOMENT-SPECTRUM"
DEFAULT_CANDIDATE_ID = "DHS-GOWERS-SIEVE"


@dataclass(frozen=True)
class SmithTypeCount:
    signature: str
    integer_rank: int
    two_adic_valuations: list[int]
    observed_tuple_count: int
    observed_frequency: float


@dataclass(frozen=True)
class SourceFifthMomentCertificate:
    n_bits: int
    register_offset: int
    register_count: int
    assignment_count: int
    source_modulus: int
    affine_independent_five_set_count: int
    integer_rank_four_five_set_count: int
    smith_two_rank_five_set_count: int
    exact_expected_fifth_factorial_moment_numerator: int
    exact_expected_fifth_factorial_moment_denominator: int
    exact_independent_baseline_numerator: int
    exact_independent_baseline_denominator: int
    exact_fifth_excess_numerator: int
    exact_fifth_excess_denominator: int
    fifth_excess: float
    fixed_offset_fifth_excess_vanishes: bool
    proof: str
    limitations: list[str]


@dataclass(frozen=True)
class SmithMomentRow:
    n_bits: int
    register_offset: int
    register_count: int
    moment_order: int
    modulus: int
    assignment_count: int
    unordered_tuple_population: int
    evaluated_tuple_count: int
    census_mode: str
    complete_census: bool
    source_dimension_rank_capped: bool
    sampled_row_is_rare_event_blind: bool
    exact_expected_factorial_moment_numerator: int | None
    exact_expected_factorial_moment_denominator: int | None
    estimated_expected_factorial_moment: float
    independent_factorial_moment_baseline: float
    factorial_moment_excess: float
    relative_excess: float
    sampling_standard_error: float
    mod2_dependent_tuple_fraction: float
    integer_rank_deficient_tuple_fraction: float
    torsion_tuple_fraction: float
    maximum_observed_two_adic_valuation: int
    distinct_smith_type_count: int
    smith_types: list[SmithTypeCount]
    fourth_moment_formula_crosscheck: bool | None
    fifth_moment_formula_crosscheck: bool | None
    finite_row_is_asymptotic_theorem: bool


@dataclass(frozen=True)
class DCPSubsetSumSmithMomentReport:
    created_at: str
    source_contract: dict[str, str]
    source_fifth_moment_certificates: list[SourceFifthMomentCertificate]
    rows: list[SmithMomentRow]
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


def source_fifth_moment_certificate(
    n_bits: int,
    register_offset: int,
) -> SourceFifthMomentCertificate:
    """Return the exact source-averaged fifth-factorial moment certificate.

    Every dependent five-set contains a unique affine parallelogram.  A
    rank-three parallelogram plus the fifth point has integer rank four.  A
    Smith-two parallelogram has exactly four additional cube vertices in its
    rational affine span; those extensions have rank four, while every other
    extension has rank five and retains one factor of two.
    """

    if n_bits < 1:
        raise ValueError("n_bits must be positive")
    register_count = n_bits + register_offset
    if register_count < 3:
        raise ValueError("the fifth-moment formula requires at least three registers")
    assignment_count = 1 << register_count
    modulus = 1 << n_bits
    affine_quadruples, rank_three_ordered, smith_two_ordered, _ = (
        affine_quadruple_type_counts(register_count)
    )
    affine_quadruple_sets = affine_quadruples // math.factorial(4)
    rank_three_quadruple_sets = rank_three_ordered // math.factorial(4)
    smith_two_quadruple_sets = smith_two_ordered // math.factorial(4)
    if (
        affine_quadruple_sets
        != rank_three_quadruple_sets + smith_two_quadruple_sets
    ):
        raise AssertionError("quadruple set decomposition failed")

    rank_four_five_sets = (
        rank_three_quadruple_sets * (assignment_count - 4)
        + 4 * smith_two_quadruple_sets
    )
    smith_two_rank_five_sets = smith_two_quadruple_sets * (assignment_count - 8)
    dependent_five_sets = affine_quadruple_sets * (assignment_count - 4)
    if rank_four_five_sets + smith_two_rank_five_sets != dependent_five_sets:
        raise AssertionError("five-set dependency decomposition failed")
    independent_five_sets = math.comb(assignment_count, 5) - dependent_five_sets
    orderings = math.factorial(5)
    moment = orderings * (
        Fraction(independent_five_sets, modulus**5)
        + Fraction(rank_four_five_sets, modulus**4)
        + Fraction(2 * smith_two_rank_five_sets, modulus**5)
    )
    baseline = Fraction(_falling(assignment_count, 5), modulus**5)
    excess = moment - baseline
    return SourceFifthMomentCertificate(
        n_bits=n_bits,
        register_offset=register_offset,
        register_count=register_count,
        assignment_count=assignment_count,
        source_modulus=modulus,
        affine_independent_five_set_count=independent_five_sets,
        integer_rank_four_five_set_count=rank_four_five_sets,
        smith_two_rank_five_set_count=smith_two_rank_five_sets,
        exact_expected_fifth_factorial_moment_numerator=moment.numerator,
        exact_expected_fifth_factorial_moment_denominator=moment.denominator,
        exact_independent_baseline_numerator=baseline.numerator,
        exact_independent_baseline_denominator=baseline.denominator,
        exact_fifth_excess_numerator=excess.numerator,
        exact_fifth_excess_denominator=excess.denominator,
        fifth_excess=float(excess),
        fixed_offset_fifth_excess_vanishes=True,
        proof=(
            "A dependent five-set contains a unique xor-zero four-set. Rank-three quadruples admit every outside "
            "point as an integer-rank-four extension. Each Smith-two quadruple has exactly four additional Boolean "
            "vertices in its rational affine span; its other U-8 extensions have rank five and Smith valuations "
            "(0,0,0,0,1). Substitution gives excess O((3/4)^n)+O(2^-n) at fixed offset."
        ),
        limitations=[
            "The theorem averages over uniformly random labels and independent target.",
            "It controls fixed fifth order only.",
            "It does not prove concentration for conditioned low fibers.",
            "It supplies no implicit statistic, decoder, or computational lower bound.",
        ],
    )


def _gf2_rank(rows: Iterable[int]) -> int:
    basis: dict[int, int] = {}
    for row in rows:
        value = int(row)
        while value:
            pivot = value.bit_length() - 1
            if pivot in basis:
                value ^= basis[pivot]
            else:
                basis[pivot] = value
                break
    return len(basis)


def _two_adic_valuation(value: int) -> int:
    value = abs(int(value))
    if value == 0:
        raise ValueError("zero has no finite two-adic valuation")
    return (value & -value).bit_length() - 1


def smith_joint_probability(
    assignments: Sequence[int],
    register_count: int,
    n_bits: int,
) -> tuple[int, tuple[int, ...], Fraction, bool]:
    """Return integer rank, 2-adic Smith valuations, and joint hit probability."""

    if len(set(assignments)) != len(assignments):
        raise ValueError("assignments must be distinct")
    if any(mask < 0 or mask >= 1 << register_count for mask in assignments):
        raise ValueError("assignment outside the register cube")
    order = len(assignments)
    modulus = 1 << n_bits
    extended_masks = [int(mask) | (1 << register_count) for mask in assignments]
    mod2_rank = _gf2_rank(extended_masks)
    if mod2_rank == order:
        return order, (0,) * order, Fraction(1, modulus**order), False

    matrix = Matrix(
        [
            [((mask >> column) & 1) for column in range(register_count)] + [-1]
            for mask in assignments
        ]
    )
    diagonal = smith_normal_form(matrix, domain=ZZ)
    invariant_factors = [
        abs(int(diagonal[index, index]))
        for index in range(min(diagonal.rows, diagonal.cols))
        if diagonal[index, index] != 0
    ]
    valuations = tuple(_two_adic_valuation(value) for value in invariant_factors)
    numerator = math.prod(1 << min(n_bits, valuation) for valuation in valuations)
    probability = Fraction(numerator, modulus ** len(invariant_factors))
    return len(invariant_factors), valuations, probability, mod2_rank < order


def _signature(rank: int, valuations: Sequence[int]) -> str:
    return f"rank={rank};v2={','.join(str(value) for value in valuations)}"


def _tuple_stream(
    assignment_count: int,
    order: int,
    complete: bool,
    sample_count: int,
    rng: random.Random,
) -> Iterable[tuple[int, ...]]:
    if complete:
        return itertools.combinations(range(assignment_count), order)
    return (
        tuple(sorted(rng.sample(range(assignment_count), order)))
        for _ in range(sample_count)
    )


def analyze_smith_moment(
    n_bits: int,
    register_offset: int,
    moment_order: int,
    exact_combination_cap: int = 20_000,
    sample_count: int = 2_000,
    seed: int = 0,
) -> SmithMomentRow:
    if n_bits < 1:
        raise ValueError("n_bits must be positive")
    register_count = n_bits + register_offset
    if register_count < 1:
        raise ValueError("register count must be positive")
    assignment_count = 1 << register_count
    if moment_order < 2 or moment_order > assignment_count:
        raise ValueError("moment order must be between 2 and the assignment count")
    if exact_combination_cap < 1 or sample_count < 1:
        raise ValueError("census and sample budgets must be positive")

    population = math.comb(assignment_count, moment_order)
    rank_capped = moment_order > register_count + 1
    complete = population <= exact_combination_cap and not rank_capped
    evaluated = population if complete else sample_count
    rng = random.Random(seed)
    probabilities: list[Fraction] = []
    types: Counter[tuple[int, tuple[int, ...]]] = Counter()
    mod2_dependent = 0
    rank_deficient = 0
    torsion = 0
    maximum_valuation = 0

    for assignments in _tuple_stream(
        assignment_count, moment_order, complete, sample_count, rng
    ):
        rank, valuations, probability, dependent = smith_joint_probability(
            assignments, register_count, n_bits
        )
        probabilities.append(probability)
        types[(rank, valuations)] += 1
        mod2_dependent += int(dependent)
        rank_deficient += int(rank < moment_order)
        has_torsion = any(value > 0 for value in valuations)
        torsion += int(has_torsion)
        maximum_valuation = max(maximum_valuation, max(valuations, default=0))

    ordered_population = _falling(assignment_count, moment_order)
    baseline_fraction = Fraction(ordered_population, (1 << n_bits) ** moment_order)
    if complete:
        exact_moment = math.factorial(moment_order) * sum(probabilities, Fraction())
        estimate = float(exact_moment)
        standard_error = 0.0
        exact_numerator: int | None = exact_moment.numerator
        exact_denominator: int | None = exact_moment.denominator
    else:
        float_probabilities = [float(value) for value in probabilities]
        mean_probability = sum(float_probabilities) / evaluated
        estimate = ordered_population * mean_probability
        if evaluated > 1:
            variance = sum(
                (value - mean_probability) ** 2 for value in float_probabilities
            ) / (evaluated - 1)
            standard_error = ordered_population * math.sqrt(variance / evaluated)
        else:
            standard_error = 0.0
        exact_moment = None
        exact_numerator = None
        exact_denominator = None
    baseline = float(baseline_fraction)
    excess = estimate - baseline
    relative_excess = excess / baseline if baseline else 0.0

    fourth_crosscheck: bool | None = None
    if complete and moment_order == 4:
        fourth = source_fourth_moment_certificate(n_bits, register_offset)
        expected = Fraction(
            fourth.exact_expected_fourth_factorial_moment_numerator,
            fourth.exact_expected_fourth_factorial_moment_denominator,
        )
        fourth_crosscheck = exact_moment == expected
    fifth_crosscheck: bool | None = None
    if complete and moment_order == 5 and register_count >= 3:
        fifth = source_fifth_moment_certificate(n_bits, register_offset)
        expected = Fraction(
            fifth.exact_expected_fifth_factorial_moment_numerator,
            fifth.exact_expected_fifth_factorial_moment_denominator,
        )
        fifth_crosscheck = exact_moment == expected

    smith_types = [
        SmithTypeCount(
            signature=_signature(rank, valuations),
            integer_rank=rank,
            two_adic_valuations=list(valuations),
            observed_tuple_count=count,
            observed_frequency=count / evaluated,
        )
        for (rank, valuations), count in sorted(
            types.items(), key=lambda item: (-item[1], item[0])
        )
    ]
    return SmithMomentRow(
        n_bits=n_bits,
        register_offset=register_offset,
        register_count=register_count,
        moment_order=moment_order,
        modulus=1 << n_bits,
        assignment_count=assignment_count,
        unordered_tuple_population=population,
        evaluated_tuple_count=evaluated,
        census_mode="complete-exact" if complete else "sampled-type-probe",
        complete_census=complete,
        source_dimension_rank_capped=rank_capped,
        sampled_row_is_rare_event_blind=not complete,
        exact_expected_factorial_moment_numerator=exact_numerator,
        exact_expected_factorial_moment_denominator=exact_denominator,
        estimated_expected_factorial_moment=estimate,
        independent_factorial_moment_baseline=baseline,
        factorial_moment_excess=excess,
        relative_excess=relative_excess,
        sampling_standard_error=standard_error,
        mod2_dependent_tuple_fraction=mod2_dependent / evaluated,
        integer_rank_deficient_tuple_fraction=rank_deficient / evaluated,
        torsion_tuple_fraction=torsion / evaluated,
        maximum_observed_two_adic_valuation=maximum_valuation,
        distinct_smith_type_count=len(types),
        smith_types=smith_types,
        fourth_moment_formula_crosscheck=fourth_crosscheck,
        fifth_moment_formula_crosscheck=fifth_crosscheck,
        finite_row_is_asymptotic_theorem=False,
    )


def run_smith_moment_spectrum(
    n_values: Sequence[int] = (3, 4, 6, 8),
    register_offsets: Sequence[int] = (0, 2),
    moment_orders: Sequence[int] = (2, 3, 4, 5, 6),
    exact_combination_cap: int = 20_000,
    sample_count: int = 2_000,
    seed: int = 0,
) -> DCPSubsetSumSmithMomentReport:
    rows = [
        analyze_smith_moment(
            n_bits,
            offset,
            order,
            exact_combination_cap=exact_combination_cap,
            sample_count=sample_count,
            seed=seed + 1_000_003 * n_index + 10_007 * offset_index + 101 * order,
        )
        for n_index, n_bits in enumerate(n_values)
        for offset_index, offset in enumerate(register_offsets)
        for order in moment_orders
        if order <= 1 << (n_bits + offset)
    ]
    exact_rows = [row for row in rows if row.complete_census]
    sampled_rows = [row for row in rows if not row.complete_census]
    unresolved_rows = [row for row in rows if row.moment_order >= 5]
    unresolved_order_six_rows = [row for row in rows if row.moment_order >= 6]
    fifth_certificates = [
        source_fifth_moment_certificate(n_bits, offset)
        for n_bits in n_values
        for offset in register_offsets
        if n_bits + offset >= 3
    ]
    fourth_crosschecks = [
        row for row in rows if row.fourth_moment_formula_crosscheck is not None
    ]
    fifth_crosschecks = [
        row for row in rows if row.fifth_moment_formula_crosscheck is not None
    ]
    observed_valuations = [row.maximum_observed_two_adic_valuation for row in rows]
    metrics: dict[str, int | float] = {
        "row_count": len(rows),
        "complete_exact_census_row_count": len(exact_rows),
        "sampled_rare_event_blind_row_count": len(sampled_rows),
        "fourth_moment_formula_crosscheck_count": sum(
            row.fourth_moment_formula_crosscheck is True for row in fourth_crosschecks
        ),
        "fourth_moment_formula_crosscheck_failure_count": sum(
            row.fourth_moment_formula_crosscheck is False for row in fourth_crosschecks
        ),
        "source_fifth_moment_certificate_count": len(fifth_certificates),
        "fifth_moment_formula_crosscheck_count": sum(
            row.fifth_moment_formula_crosscheck is True for row in fifth_crosschecks
        ),
        "fifth_moment_formula_crosscheck_failure_count": sum(
            row.fifth_moment_formula_crosscheck is False for row in fifth_crosschecks
        ),
        "proved_source_fixed_offset_fifth_excess_vanishing_count": sum(
            item.fixed_offset_fifth_excess_vanishes for item in fifth_certificates
        ),
        "proved_asymptotic_fixed_fifth_order_obstruction_count": sum(
            item.fixed_offset_fifth_excess_vanishes for item in fifth_certificates
        ),
        "unresolved_order_at_least_five_row_count": len(unresolved_rows),
        "unresolved_order_at_least_six_row_count": len(unresolved_order_six_rows),
        "maximum_observed_two_adic_valuation": max(observed_valuations, default=0),
        "proved_asymptotic_order_at_least_five_obstruction_count": 0,
        "proved_asymptotic_order_at_least_six_obstruction_count": 0,
        "proved_growing_order_obstruction_count": 0,
        "polynomial_witness_decoder_count": 0,
    }
    return DCPSubsetSumSmithMomentReport(
        created_at=utc_now(),
        source_contract={
            "labels": "independent uniform a_i in Z_(2^n)",
            "target": "independent uniform t in Z_(2^n)",
            "representation_count": "C=#{x in {0,1}^m : sum_i a_i x_i=t mod 2^n}",
            "joint_probability": (
                "For rows (x,-1) with nonzero Smith factors d_i, Pr[all hits]="
                "prod_i gcd(2^n,d_i)/(2^n)^rank"
            ),
            "exactness_boundary": "Only complete-exact rows are finite identities; sampled rows are rare-event blind",
        },
        source_fifth_moment_certificates=fifth_certificates,
        rows=rows,
        headline_metrics=metrics,
        claim_gate={
            "orders_two_and_three_closed": True,
            "source_average_order_four_closed": True,
            "source_average_fixed_fifth_order_closed": True,
            "orders_at_least_six_asymptotically_closed": False,
            "growing_order_closed": False,
            "sampled_type_flatness_is_evidence_of_absence": False,
            "polynomial_witness_decoder_constructed": False,
            "speedup_claim_allowed": False,
            "reason": (
                "Smith spectra give exact finite source moments when fully enumerated and identify 2-adic dependency "
                "types elsewhere. Exact five-set classification closes source-average fixed fifth order. Sampled tuple "
                "probes cannot see exponentially rare configurations, and no uniform order>=6 theorem, growing-order "
                "bound, or decoder follows."
            ),
        },
        status="smith-moment-spectrum-maps-first-unresolved-orders",
        summary=(
            f"Computed {len(exact_rows)} complete Smith moment censuses and {len(sampled_rows)} explicitly rare-event-blind "
            f"type probes across {len(rows)} rows. Exact order-four cross-checks passed "
            f"{metrics['fourth_moment_formula_crosscheck_count']}/{len(fourth_crosschecks)} and exact order-five "
            f"cross-checks passed {metrics['fifth_moment_formula_crosscheck_count']}/{len(fifth_crosschecks)}. Source-average "
            "fixed fifth order is asymptotically obstructed; order>=6 and growing-order asymptotics remain open."
        ),
        falsifiers_triggered=[
            "Generic source-average fixed fifth-order excess vanishes by exact five-set Smith classification.",
            "Any sampled absence of dependent Smith types is rejected as a rare-event lower bound.",
            "Any complete finite census is rejected as an asymptotic theorem without a uniform counting argument.",
            "Moment excess without an implicit statistic and witness decoder is not algorithmic progress.",
            "Orders above the source matrix rank at small n are marked as finite dimension-capped artifacts.",
        ],
    )


def write_smith_moment_spectrum(
    path: Path = DCP_SUBSET_SUM_SMITH_MOMENT_PATH,
    n_values: Sequence[int] = (3, 4, 6, 8),
    register_offsets: Sequence[int] = (0, 2),
    moment_orders: Sequence[int] = (2, 3, 4, 5, 6),
    exact_combination_cap: int = 20_000,
    sample_count: int = 2_000,
    seed: int = 0,
    write_registry: bool = True,
    registry_experiment_id: str = DEFAULT_EXPERIMENT_ID,
    registry_candidate_id: str = DEFAULT_CANDIDATE_ID,
    registry_result_id: str | None = None,
) -> dict:
    report = run_smith_moment_spectrum(
        n_values=n_values,
        register_offsets=register_offsets,
        moment_orders=moment_orders,
        exact_combination_cap=exact_combination_cap,
        sample_count=sample_count,
        seed=seed,
    )
    payload = asdict(report)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    if write_registry:
        upsert_negative_result(
            NegativeResultRecord(
                id="NEG-DCP-SUBSET-SUM-SAMPLED-SMITH-FLATNESS",
                source=str(path),
                claim=(
                    "Failure to observe atypical fifth-order or order>=6 dependent Smith types in polynomially many "
                    "sampled assignment tuples proves density-one subset-sum counts have no useful high-order structure."
                ),
                reason_invalid=(
                    "Exponentially rare affine configurations can make a nonnegligible factorial-moment contribution. "
                    "Only complete enumeration or a uniform analytic count can establish absence."
                ),
                lesson=(
                    "Use sampled Smith spectra to generate exact dependency classes and conjectures, never as a lower "
                    "bound. Promotion requires asymptotic class counts and an algorithmic observable."
                ),
                applies_to=[registry_candidate_id, registry_experiment_id],
                evidence=payload["headline_metrics"],
            )
        )
        result_id = registry_result_id or f"RESULT-{registry_experiment_id}-SMITH-MOMENT-SPECTRUM"
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
                artifacts={"dcp_subset_sum_smith_moment_spectrum": str(path)},
            )
        )
    return payload

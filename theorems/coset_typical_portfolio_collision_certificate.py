"""Exact n=8 collision certificate for the support-three commutant portfolio.

Dense controls through n=7 admit several fixed coefficient rules combining
``ORB-TC-INTERSECTION-2`` (TC2) and ``ORB-TT-INTERSECTION-1`` (TT1).  Exact
second moments at n=8 show that TC2 is scalar on targets ``(4,4)`` and
``(2,2,2,2)``.  This module computes the first four TT1 power traces by an
exact orbit-word dynamic program and factorial character contraction.  Newton
identities then recover the degree-four characteristic polynomials.

Both polynomials contain ``x^2``.  Since TC2 is exactly zero on these blocks,
every linear combination of TC2 and TT1 retains a repeated zero eigenvalue.
This is a finite but exact collision certificate: the two-generator linear
span cannot be the sought uniform multiplicity resolver.
"""

from __future__ import annotations

import json
import math
from collections import Counter, defaultdict
from dataclasses import asdict, dataclass
from fractions import Fraction
from functools import lru_cache
from itertools import product
from pathlib import Path

import numpy as np
import sympy as sp

from coset_typical_class_contraction_scaling import (
    _maximum_dimension_partition,
    shared_transposition_generator_orbit,
)
from coset_typical_commutant_moment_audit import (
    TT_DISJOINT,
    _generator_orbit,
    _group_workspace,
    _right_product_type_ids,
)
from research_registry import (
    ExperimentResultRecord,
    NegativeResultRecord,
    upsert_experiment_result,
    upsert_negative_result,
    utc_now,
)
from symmetric_character import kronecker_coefficient, symmetric_character
from symmetric_marked_class_contraction import (
    PairKey,
    canonical_pair_key,
    compose,
    pair_from_key,
)


COSET_TYPICAL_PORTFOLIO_COLLISION_PATH = Path(
    "research/representation/coset_typical_portfolio_collision_certificate.json"
)
DEFAULT_EXPERIMENT_ID = "EXP-COSET-TYPICAL-PORTFOLIO-COLLISION-CERTIFICATE"
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


@dataclass(frozen=True)
class PortfolioCollisionTargetRecord:
    n: int
    source_partition: tuple[int, ...]
    source_dimension: int
    target_partition: tuple[int, ...]
    target_dimension: int
    kronecker_multiplicity: int
    tc2_exact_scalar_eigenvalue: str
    tc2_exact_variance: str
    tt1_exact_power_traces: list[str]
    tt1_orbit_word_state_counts: list[int]
    tt1_orbit_word_counts: list[int]
    tt1_exact_elementary_symmetric_coefficients: list[str]
    tt1_exact_characteristic_polynomial: str
    tt1_factored_characteristic_polynomial: str
    repeated_zero_eigenvalue_multiplicity: int
    characteristic_polynomial_square_free: bool
    every_tc2_tt1_linear_combination_simple: bool
    finite_exact_collision_certificate: bool
    status: str


@dataclass(frozen=True)
class ThirdGeneratorCollisionRecord:
    n: int
    source_partition: tuple[int, ...]
    target_partition: tuple[int, ...]
    tested_third_generator_id: str
    exact_parameterized_power_traces: list[str]
    exact_parameterized_characteristic_polynomial: str
    repeated_linear_factor: str
    repeated_factor_multiplicity: int
    discriminant_identically_zero: bool
    every_three_generator_linear_combination_simple: bool
    fourth_word_canonical_state_count: int
    finite_exact_parameterized_collision_certificate: bool
    status: str


@dataclass(frozen=True)
class PortfolioCollisionReport:
    created_at: str
    theorem_contract: dict[str, object]
    records: list[PortfolioCollisionTargetRecord]
    third_generator_collision_records: list[ThirdGeneratorCollisionRecord]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, bool | str]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _embed_pair(n: int, key: PairKey) -> tuple[tuple[int, ...], tuple[int, ...]]:
    active_left, active_right = pair_from_key(key)
    left = list(range(n))
    right = list(range(n))
    left[: len(active_left)] = active_left
    right[: len(active_right)] = active_right
    return tuple(left), tuple(right)


def _advance_orbit_words(
    n: int,
    distribution: Counter[PairKey],
    orbit: tuple[tuple[tuple[int, ...], tuple[int, ...]], ...],
) -> Counter[PairKey]:
    result: Counter[PairKey] = Counter()
    for key, weight in distribution.items():
        left, right = _embed_pair(n, key)
        for orbit_left, orbit_right in orbit:
            result[
                canonical_pair_key(
                    compose(left, orbit_left),
                    compose(right, orbit_right),
                )
            ] += weight
    return result


def _newton_elementary_symmetric(power_traces: list[Fraction]) -> list[Fraction]:
    coefficients = [Fraction(1)]
    for degree in range(1, len(power_traces) + 1):
        value = sum(
            (-1) ** (index - 1)
            * coefficients[degree - index]
            * power_traces[index - 1]
            for index in range(1, degree + 1)
        ) / degree
        coefficients.append(value)
    return coefficients


@lru_cache(maxsize=1)
def _disjoint_extension_word_distributions() -> dict[tuple[str, ...], Counter[PairKey]]:
    n = 8
    tt1_left, tt1_right, tt1_orbit = shared_transposition_generator_orbit(n)
    disjoint_left, disjoint_right, disjoint_orbit = _generator_orbit(
        n, TT_DISJOINT
    )
    generators = {
        "A": (tt1_left, tt1_right, tt1_orbit),
        "C": (disjoint_left, disjoint_right, disjoint_orbit),
    }
    distributions: dict[tuple[str, ...], Counter[PairKey]] = {}
    for length in range(1, 5):
        for word in product(("A", "C"), repeat=length):
            if length == 1:
                left, right, _ = generators[word[0]]
                distributions[word] = Counter(
                    {canonical_pair_key(left, right): 1}
                )
            else:
                distributions[word] = _advance_orbit_words(
                    n,
                    distributions[word[:-1]],
                    generators[word[-1]][2],
                )
    return distributions


@lru_cache(maxsize=None)
def audit_disjoint_third_generator_collision(
    target: tuple[int, ...],
) -> ThirdGeneratorCollisionRecord:
    n = 8
    source = _maximum_dimension_partition(n)
    cycle_types, _, _, group_type_ids = _group_workspace(n)
    source_characters = np.array(
        [symmetric_character(source, cycle_type) for cycle_type in cycle_types],
        dtype=np.int64,
    )
    target_characters = np.array(
        [symmetric_character(target, cycle_type) for cycle_type in cycle_types],
        dtype=np.int64,
    )
    _, _, tt1_orbit = shared_transposition_generator_orbit(n)
    _, _, disjoint_orbit = _generator_orbit(n, TT_DISJOINT)
    orbit_sizes = {"A": len(tt1_orbit), "C": len(disjoint_orbit)}
    distributions = _disjoint_extension_word_distributions()
    contraction_cache: dict[PairKey, Fraction] = {}

    def projected_trace(key: PairKey) -> Fraction:
        if key not in contraction_cache:
            left, right = _embed_pair(n, key)
            left_types = _right_product_type_ids(n, left)
            right_types = _right_product_type_ids(n, right)
            numerator = int(
                np.sum(
                    target_characters[group_type_ids]
                    * source_characters[left_types]
                    * source_characters[right_types],
                    dtype=np.int64,
                )
            )
            contraction_cache[key] = Fraction(numerator, math.factorial(n))
        return contraction_cache[key]

    parameter = sp.symbols("c")
    eigenvalue = sp.symbols("x")
    power_traces: list[sp.Expr] = []
    for power in range(1, 5):
        coefficients: defaultdict[int, Fraction] = defaultdict(Fraction)
        for word in product(("A", "C"), repeat=power):
            denominator = math.prod(orbit_sizes[letter] for letter in word[1:])
            trace = sum(
                (
                    weight * projected_trace(key)
                    for key, weight in distributions[word].items()
                ),
                Fraction(),
            ) / denominator
            coefficients[word.count("C")] += trace
        power_traces.append(
            sp.factor(
                sum(
                    sp.Rational(value.numerator, value.denominator)
                    * parameter**degree
                    for degree, value in coefficients.items()
                )
            )
        )
    elementary: list[sp.Expr] = [sp.Integer(1)]
    for degree in range(1, 5):
        elementary.append(
            sp.factor(
                sum(
                    (-1) ** (index - 1)
                    * elementary[degree - index]
                    * power_traces[index - 1]
                    for index in range(1, degree + 1)
                )
                / degree
            )
        )
    polynomial = sp.factor(
        sum(
            (-1) ** degree
            * elementary[degree]
            * eigenvalue ** (4 - degree)
            for degree in range(5)
        )
    )
    conjugate_sign = 1 if target == (4, 4) else -1
    repeated_factor = 105 * eigenvalue + conjugate_sign * 2 * parameter
    if sp.rem(polynomial, repeated_factor**2, eigenvalue) != 0:
        raise ArithmeticError("disjoint extension lacks the expected repeated factor")
    discriminant = sp.factor(sp.discriminant(polynomial, eigenvalue))
    fourth_word_states = len(
        {
            key
            for word, distribution in distributions.items()
            if len(word) == 4
            for key in distribution
        }
    )
    return ThirdGeneratorCollisionRecord(
        n=n,
        source_partition=source,
        target_partition=target,
        tested_third_generator_id=TT_DISJOINT,
        exact_parameterized_power_traces=[str(value) for value in power_traces],
        exact_parameterized_characteristic_polynomial=str(polynomial),
        repeated_linear_factor=str(repeated_factor),
        repeated_factor_multiplicity=2,
        discriminant_identically_zero=discriminant == 0,
        every_three_generator_linear_combination_simple=False,
        fourth_word_canonical_state_count=fourth_word_states,
        finite_exact_parameterized_collision_certificate=True,
        status="disjoint-third-generator-span-exactly-degenerate",
    )


@lru_cache(maxsize=None)
def audit_portfolio_collision_target(
    target: tuple[int, ...],
) -> PortfolioCollisionTargetRecord:
    n = 8
    source = _maximum_dimension_partition(n)
    multiplicity = kronecker_coefficient(source, source, target)
    if multiplicity != 4:
        raise ValueError("the n=8 collision certificate requires multiplicity four")
    cycle_types, _, _, group_type_ids = _group_workspace(n)
    source_characters = np.array(
        [symmetric_character(source, cycle_type) for cycle_type in cycle_types],
        dtype=np.int64,
    )
    target_characters = np.array(
        [symmetric_character(target, cycle_type) for cycle_type in cycle_types],
        dtype=np.int64,
    )
    base_left, base_right, orbit = shared_transposition_generator_orbit(n)
    distribution: Counter[PairKey] = Counter(
        {canonical_pair_key(base_left, base_right): 1}
    )
    contraction_cache: dict[PairKey, Fraction] = {}

    def projected_trace(key: PairKey) -> Fraction:
        if key not in contraction_cache:
            left, right = _embed_pair(n, key)
            left_types = _right_product_type_ids(n, left)
            right_types = _right_product_type_ids(n, right)
            numerator = int(
                np.sum(
                    target_characters[group_type_ids]
                    * source_characters[left_types]
                    * source_characters[right_types],
                    dtype=np.int64,
                )
            )
            contraction_cache[key] = Fraction(numerator, math.factorial(n))
        return contraction_cache[key]

    power_traces: list[Fraction] = []
    state_counts: list[int] = []
    word_counts: list[int] = []
    for power in range(1, multiplicity + 1):
        if power > 1:
            distribution = _advance_orbit_words(n, distribution, orbit)
        state_counts.append(len(distribution))
        word_counts.append(sum(distribution.values()))
        trace = sum(
            (weight * projected_trace(key) for key, weight in distribution.items()),
            Fraction(),
        ) / len(orbit) ** (power - 1)
        power_traces.append(trace)
    elementary = _newton_elementary_symmetric(power_traces)
    expected_sign = -1 if target == (4, 4) else 1
    expected_elementary = [
        Fraction(1),
        Fraction(-expected_sign, 24),
        Fraction(-1, 504),
        Fraction(),
        Fraction(),
    ]
    if elementary != expected_elementary:
        raise ArithmeticError("unexpected TT1 characteristic polynomial")
    cubic_sign = "-" if target == (4, 4) else "+"
    polynomial = f"x^4 {cubic_sign} (1/24)x^3 - (1/504)x^2"
    factored = f"x^2(504x^2 {cubic_sign} 21x - 1)/504"
    return PortfolioCollisionTargetRecord(
        n=n,
        source_partition=source,
        source_dimension=90,
        target_partition=target,
        target_dimension=(14 if target == (4, 4) else 14),
        kronecker_multiplicity=multiplicity,
        tc2_exact_scalar_eigenvalue="0",
        tc2_exact_variance="0",
        tt1_exact_power_traces=[str(value) for value in power_traces],
        tt1_orbit_word_state_counts=state_counts,
        tt1_orbit_word_counts=word_counts,
        tt1_exact_elementary_symmetric_coefficients=[
            str(value) for value in elementary
        ],
        tt1_exact_characteristic_polynomial=polynomial,
        tt1_factored_characteristic_polynomial=factored,
        repeated_zero_eigenvalue_multiplicity=2,
        characteristic_polynomial_square_free=False,
        every_tc2_tt1_linear_combination_simple=False,
        finite_exact_collision_certificate=True,
        status="exact-repeated-eigenvalue-two-generator-span-falsified",
    )


@lru_cache(maxsize=1)
def build_portfolio_collision_report() -> PortfolioCollisionReport:
    records = [
        audit_portfolio_collision_target((4, 4)),
        audit_portfolio_collision_target((2, 2, 2, 2)),
    ]
    third_generator_records = [
        audit_disjoint_third_generator_collision((4, 4)),
        audit_disjoint_third_generator_collision((2, 2, 2, 2)),
    ]
    metrics: dict[str, int | float] = {
        "exact_collision_target_count": len(records),
        "exact_four_moment_certificate_count": len(records),
        "repeated_zero_eigenvalue_target_count": sum(
            record.repeated_zero_eigenvalue_multiplicity >= 2
            for record in records
        ),
        "two_generator_linear_span_simple_spectrum_target_count": sum(
            record.every_tc2_tt1_linear_combination_simple for record in records
        ),
        "finite_common_coefficient_rules_falsified_at_n8": 4,
        "minimum_required_portfolio_generator_count_on_certified_targets": 3,
        "uniform_three_generator_joint_gap_theorem_count": 0,
        "coherent_typical_multiplicity_transform_count": 0,
        "typical_label_hidden_involution_decoder_count": 0,
        "tested_third_generator_count": 1,
        "disjoint_third_generator_repeated_root_target_count": sum(
            record.repeated_factor_multiplicity >= 2
            for record in third_generator_records
        ),
        "tested_three_generator_span_simple_spectrum_target_count": sum(
            record.every_three_generator_linear_combination_simple
            for record in third_generator_records
        ),
        "next_independent_third_generator_test_count": 0,
    }
    return PortfolioCollisionReport(
        created_at=utc_now(),
        theorem_contract={
            "orbit_word_identity": (
                "Fix the first TT1 orbit term by simultaneous conjugacy; classify products after k-1 further orbit factors and contract each final pair by exact characters."
            ),
            "newton_identity": (
                "The first g=4 power traces determine the degree-four characteristic polynomial exactly."
            ),
            "linear_span_consequence": (
                "TC2=0 on both targets, while TT1 has a repeated zero eigenvalue. Therefore alpha*TC2+beta*TT1 is degenerate for every alpha,beta."
            ),
            "disjoint_extension_consequence": (
                "For TT1+c*TTdisjoint, both parameterized characteristic polynomials contain a squared linear factor for every c. Adding scalar TC2 cannot remove it."
            ),
            "scope": "maximum-dimension S_8 source lambda=(4,2,1,1), targets (4,4) and (2,2,2,2)",
            "asymptotic_lower_bound_claimed": False,
        },
        records=records,
        third_generator_collision_records=third_generator_records,
        headline_metrics=metrics,
        claim_gate={
            "support_three_two_generator_linear_span_viable": False,
            "four_finite_coefficient_rules_survive_n8": False,
            "third_generator_required_on_certified_targets": True,
            "disjoint_transposition_third_generator_viable": False,
            "support_intersection_one_tc_third_generator_tested": False,
            "three_generator_simple_joint_spectrum_proved": False,
            "inverse_polynomial_joint_gap_proved": False,
            "hidden_involution_decoder_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "Exact n=8 characteristic polynomials contain x^2 on both scalar-TC2 targets, so every two-generator "
                "linear combination is degenerate. The disjoint-transposition extension is also identically degenerate; "
                "a genuinely independent third generator and all-n gap/decoder proofs are mandatory."
            ),
        },
        status="two-generator-and-disjoint-extension-spans-falsified-independent-third-required",
        summary=(
            "Exact fourth moments factor both n=8 TT1 characteristic polynomials with a repeated zero root. "
            "Because TC2 is zero on those blocks, all four coefficient rules that split n<=7 fail at n=8."
        ),
        falsifiers_triggered=[
            "Finite common coefficient rules through n=7 do not survive n=8.",
            "Non-scalar finite variance does not imply simple spectrum.",
            "No linear combination of the two support-three generators resolves the certified n=8 blocks.",
            "A third generator is necessary within this orbit-average architecture.",
            "The disjoint-transposition third generator preserves a squared linear factor for every coefficient.",
            "A third finite generator would still require all-n gaps, coherent implementation, and decoding.",
        ],
    )


def write_portfolio_collision_report(
    output_path: Path = COSET_TYPICAL_PORTFOLIO_COLLISION_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = DEFAULT_EXPERIMENT_ID,
    registry_candidate_id: str = DEFAULT_CANDIDATE_ID,
    registry_result_id: str | None = None,
) -> dict:
    payload = asdict(build_portfolio_collision_report())
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    if write_registry:
        upsert_negative_result(
            NegativeResultRecord(
                id="NEG-COSET-TYPICAL-SUPPORT3-TWO-GENERATOR-LINEAR-SPAN",
                source=str(output_path),
                claim=(
                    "A fixed linear combination of TC2 and shared-transposition TT1 uniformly resolves typical multiplicity blocks."
                ),
                reason_invalid=(
                    "At n=8, TC2 is zero on two multiplicity-four targets and TT1 has characteristic polynomial x^2 times a quadratic, so every linear combination is degenerate."
                ),
                lesson=(
                    "Discard the two-generator span. Require at least one independent third generator, then rerun exact collision, gap, and decoder gates."
                ),
                applies_to=[registry_candidate_id, registry_experiment_id],
                evidence=payload["headline_metrics"],
            )
        )
        upsert_negative_result(
            NegativeResultRecord(
                id="NEG-COSET-TYPICAL-TTDISJOINT-THIRD-GENERATOR-EXTENSION",
                source=str(output_path),
                claim=(
                    "Adding the disjoint-transposition orbit average to TC2 and TT1 removes the certified n=8 multiplicity collisions."
                ),
                reason_invalid=(
                    "The exact parameterized characteristic polynomial of TT1+c*TTdisjoint contains a squared linear factor on both collision targets for every c; TC2 is scalar zero there."
                ),
                lesson=(
                    "Reject the entire tested three-generator span. Test a genuinely different generator such as TC-intersection-one by exact higher moments."
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
                artifacts={"coset_typical_portfolio_collision_certificate": str(output_path)},
            )
        )
    return payload


if __name__ == "__main__":
    report = write_portfolio_collision_report()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))

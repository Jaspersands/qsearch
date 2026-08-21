"""Exact Plancherel stationarity and thin invariant-sector obstruction.

Let ``lambda_1,...,lambda_C`` be independent Plancherel irreps of ``S_n``.
For a target ``nu``, write ``m_nu`` for its multiplicity in their tensor
product and ``D=product_i d_lambda_i``.  Character orthogonality gives

    E[m_nu / D] = d_nu / n!,
    E[m_nu d_nu / D] = d_nu^2 / n!.

Thus the expected normalized isotypic distribution is exactly Plancherel for
every fixed positive block size ``C``.  In particular, the trivial and sign
invariant sectors each occupy expected fraction ``1/n!``.  Independent left
and right blocks have expected matched one-dimensional fraction ``2/(n!)^2``.

This complements Sellke's tensor-covering theorem.  A fixed sufficiently
large block contains every irrep with probability ``1-o(1)``, but support does
not imply substantial carrier mass.  Markov's inequality shows that the
trivial or sign fraction is at most ``poly(n)/n!`` with high probability.
Directly postselecting the common-core invariant sectors is therefore
factorially weak on average even though those sectors are typically nonzero.

The theorem does not rule out efficiently rejecting these thin sectors,
coherently quotienting them, or exploiting a different high-dimensional
target.  It rules out treating constant-block support positivity as an
inverse-polynomial postselection guarantee.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from fractions import Fraction
from pathlib import Path
from typing import Any

from representation_obstruction import (
    hook_length_dimension,
    integer_partitions,
)
from research_registry import (
    ExperimentResultRecord,
    NegativeResultRecord,
    upsert_experiment_result,
    upsert_negative_result,
    utc_now,
)
from symmetric_character import (
    conjugacy_class_size,
    symmetric_character,
)


REPORT_PATH = Path(
    "research/representation/self_dual_wreath_plancherel_block_mass.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-PLANCHEREL-BLOCK-MASS"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"
SELLKE_PAPER_ID = "sellke-irrep-tensor-covering-2022"
SELLKE_PAPER_URL = "https://arxiv.org/abs/2004.05283"

Partition = tuple[int, ...]


@dataclass(frozen=True)
class PlancherelStationarityControl:
    n: int
    block_size: int
    target_partition: Partition
    target_dimension: int
    expected_normalized_multiplicity: str
    expected_normalized_isotypic_fraction: str
    predicted_normalized_multiplicity: str
    predicted_normalized_isotypic_fraction: str
    maximum_nonidentity_regular_character_average_numerator: int
    exact_stationarity_verified: bool
    status: str


@dataclass(frozen=True)
class InvariantMassScalingRecord:
    n: int
    group_order_decimal: str
    log2_group_order: float
    single_trivial_expected_fraction: float
    single_trivial_expected_fraction_log2: float
    single_sign_expected_fraction: float
    matched_trivial_or_sign_joint_expected_fraction: float
    matched_joint_expected_fraction_log2: float
    markov_polynomial_power: int
    single_sector_high_probability_upper_bound_log2: float
    matched_sector_high_probability_upper_bound_log2: float
    markov_failure_probability_upper_bound: float
    inverse_polynomial_direct_postselection_proved: bool
    status: str


@dataclass(frozen=True)
class PlancherelBlockMassReport:
    created_at: str
    literature: dict[str, str]
    theorem_contract: dict[str, str]
    exact_controls: list[PlancherelStationarityControl]
    scaling_records: list[InvariantMassScalingRecord]
    adversarial_audit: list[dict[str, bool | str]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, bool | str]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _plancherel_normalized_character_average(
    n: int,
    cycle_type: Partition,
) -> Fraction:
    order = math.factorial(n)
    numerator = sum(
        hook_length_dimension(partition)
        * symmetric_character(partition, cycle_type)
        for partition in integer_partitions(n)
    )
    return Fraction(numerator, order)


def expected_normalized_target_multiplicity(
    n: int,
    block_size: int,
    target: Partition,
) -> Fraction:
    """Compute E[m_target/product dimensions] by exact class sums."""

    if n < 2:
        raise ValueError("n must be at least two")
    if block_size < 1:
        raise ValueError("block_size must be positive")
    if sum(target) != n:
        raise ValueError("target partition must have size n")
    order = math.factorial(n)
    return sum(
        Fraction(conjugacy_class_size(cycle_type), order)
        * symmetric_character(target, cycle_type)
        * _plancherel_normalized_character_average(n, cycle_type)
        ** block_size
        for cycle_type in integer_partitions(n)
    )


def expected_normalized_target_isotypic_fraction(
    n: int,
    block_size: int,
    target: Partition,
) -> Fraction:
    return (
        hook_length_dimension(target)
        * expected_normalized_target_multiplicity(n, block_size, target)
    )


def audit_plancherel_stationarity(
    n: int,
    block_size: int,
    target: Partition,
) -> PlancherelStationarityControl:
    order = math.factorial(n)
    dimension = hook_length_dimension(target)
    multiplicity = expected_normalized_target_multiplicity(
        n,
        block_size,
        target,
    )
    isotypic = dimension * multiplicity
    predicted_multiplicity = Fraction(dimension, order)
    predicted_isotypic = Fraction(dimension * dimension, order)
    identity = (1,) * n
    nonidentity_residual = max(
        (
            abs(
                _plancherel_normalized_character_average(n, cycle_type).numerator
            )
            for cycle_type in integer_partitions(n)
            if cycle_type != identity
        ),
        default=0,
    )
    verified = (
        multiplicity == predicted_multiplicity
        and isotypic == predicted_isotypic
        and nonidentity_residual == 0
    )
    return PlancherelStationarityControl(
        n=n,
        block_size=block_size,
        target_partition=target,
        target_dimension=dimension,
        expected_normalized_multiplicity=str(multiplicity),
        expected_normalized_isotypic_fraction=str(isotypic),
        predicted_normalized_multiplicity=str(predicted_multiplicity),
        predicted_normalized_isotypic_fraction=str(predicted_isotypic),
        maximum_nonidentity_regular_character_average_numerator=(
            nonidentity_residual
        ),
        exact_stationarity_verified=verified,
        status=(
            "exact-plancherel-tensor-stationarity"
            if verified
            else "plancherel-tensor-stationarity-failure"
        ),
    )


def invariant_mass_scaling_record(
    n: int,
    markov_polynomial_power: int = 6,
) -> InvariantMassScalingRecord:
    if n < 2:
        raise ValueError("n must be at least two")
    if markov_polynomial_power < 1:
        raise ValueError("markov_polynomial_power must be positive")
    order = math.factorial(n)
    log_order = math.log2(order)
    inflation = markov_polynomial_power * math.log2(n)
    single_log = -log_order
    matched_log = 1 - 2 * log_order
    return InvariantMassScalingRecord(
        n=n,
        group_order_decimal=str(order),
        log2_group_order=log_order,
        single_trivial_expected_fraction=math.exp2(single_log),
        single_trivial_expected_fraction_log2=single_log,
        single_sign_expected_fraction=math.exp2(single_log),
        matched_trivial_or_sign_joint_expected_fraction=math.exp2(
            matched_log
        ),
        matched_joint_expected_fraction_log2=matched_log,
        markov_polynomial_power=markov_polynomial_power,
        single_sector_high_probability_upper_bound_log2=(
            single_log + inflation
        ),
        matched_sector_high_probability_upper_bound_log2=(
            matched_log + inflation
        ),
        markov_failure_probability_upper_bound=n ** (-markov_polynomial_power),
        inverse_polynomial_direct_postselection_proved=False,
        status="factorially-thin-invariant-sector-markov-bound",
    )


def run_plancherel_block_mass() -> PlancherelBlockMassReport:
    controls = [
        audit_plancherel_stationarity(n, block_size, target)
        for n in range(3, 11)
        for block_size in (1, 2, 3, 8)
        for target in integer_partitions(n)
    ]
    scaling = [
        invariant_mass_scaling_record(n)
        for n in (4, 6, 8, 10, 16, 24, 32, 48, 64, 96, 128)
    ]
    failures = sum(
        not record.exact_stationarity_verified for record in controls
    )
    metrics: dict[str, int | float] = {
        "exact_stationarity_control_count": len(controls),
        "exact_stationarity_failure_count": failures,
        "maximum_nonidentity_regular_character_average_numerator": max(
            record.maximum_nonidentity_regular_character_average_numerator
            for record in controls
        ),
        "plancherel_tensor_stationarity_theorem_count": 1,
        "normalized_target_multiplicity_expectation_theorem_count": 1,
        "normalized_target_isotypic_expectation_theorem_count": 1,
        "trivial_invariant_expected_mass_theorem_count": 1,
        "sign_invariant_expected_mass_theorem_count": 1,
        "independent_matched_one_dimensional_joint_mass_theorem_count": 1,
        "polynomial_inflation_markov_typical_upper_bound_theorem_count": 1,
        "sellke_support_without_mass_separation_theorem_count": 1,
        "scaling_record_count": len(scaling),
        "tail_n": scaling[-1].n,
        "tail_single_invariant_mass_log2": (
            scaling[-1].single_trivial_expected_fraction_log2
        ),
        "tail_matched_joint_mass_log2": (
            scaling[-1].matched_joint_expected_fraction_log2
        ),
        "inverse_polynomial_direct_invariant_postselection_count": 0,
        "efficient_invariant_complement_projection_count": 0,
        "polynomial_hidden_permutation_decoder_count": 0,
        "new_quantum_algorithm_count": 0,
    }
    theorem_verified = failures == 0
    return PlancherelBlockMassReport(
        created_at=utc_now(),
        literature={
            "paper_id": SELLKE_PAPER_ID,
            "title": "Covering Irrep(S_n) With Tensor Products and Powers",
            "url": SELLKE_PAPER_URL,
            "relevance": (
                "Constant Plancherel tensor blocks have full irrep support "
                "with probability 1-o(1); the present theorem separates that "
                "support statement from normalized mass."
            ),
        },
        theorem_contract={
            "normalized_character_average": (
                "For Plancherel lambda, E[chi_lambda(g)/d_lambda] is one at "
                "the identity and zero elsewhere, by the regular character."
            ),
            "multiplicity_stationarity": (
                "For every target nu and fixed C>=1, "
                "E[m_nu/product_i d_lambda_i]=d_nu/n!."
            ),
            "isotypic_stationarity": (
                "The expected normalized nu-isotypic dimension is "
                "d_nu^2/n!, exactly the Plancherel probability of nu."
            ),
            "one_dimensional_corollary": (
                "Trivial and sign invariant fractions each have expectation "
                "1/n!, independent of block size."
            ),
            "matched_two_side_corollary": (
                "Independent left/right blocks have expected matched "
                "trivial-or-sign fraction 2/(n!)^2."
            ),
            "typical_upper_bound": (
                "For every fixed a>0, Markov gives invariant fraction at most "
                "n^a/n! except with probability n^-a; the matched fraction is "
                "at most 2n^a/(n!)^2 with the same failure bound."
            ),
            "scope_boundary": (
                "Thin invariant mass blocks direct postselection onto the "
                "common core. It does not block efficient rejection of that "
                "core, a coherent quotient, or high-dimensional targets."
            ),
        },
        exact_controls=controls,
        scaling_records=scaling,
        adversarial_audit=[
            {
                "objection": (
                    "Sellke covering implies the trivial sector occupies a "
                    "constant fraction of a typical block tensor product."
                ),
                "resolved": True,
                "resolution": (
                    "Support probability can tend to one while expected "
                    "normalized mass remains exactly 1/n!. Markov makes the "
                    "support-versus-mass separation quantitative."
                ),
            },
            {
                "objection": (
                    "The 1/n! law holds only for block size one or two."
                ),
                "resolved": True,
                "resolution": (
                    "The Plancherel normalized-character average vanishes at "
                    "every nonidentity class before taking its Cth power, so "
                    "the identity is exact for every fixed C>=1."
                ),
            },
            {
                "objection": (
                    "Factorially thin positive sectors cannot be efficiently "
                    "removed from a state."
                ),
                "resolved": False,
                "resolution": (
                    "The theorem rules out accepting/postselecting those "
                    "sectors at inverse-polynomial rate. A high-success "
                    "complement projection may still exist if the diagonal "
                    "irrep label can be measured efficiently."
                ),
            },
            {
                "objection": (
                    "Stationarity for arbitrary high-dimensional targets "
                    "makes every such target factorially thin."
                ),
                "resolved": False,
                "resolution": (
                    "The expected isotypic mass is d_nu^2/n!, which is large "
                    "for Plancherel-typical high-dimensional targets. Only "
                    "fixed low-dimensional targets are forced thin."
                ),
            },
        ],
        headline_metrics=metrics,
        claim_gate={
            "plancherel_tensor_isotypic_stationarity_proved": theorem_verified,
            "trivial_and_sign_expected_fraction_one_over_factorial_proved": (
                theorem_verified
            ),
            "matched_left_right_one_dimensional_mass_two_over_factorial_squared_proved": (
                theorem_verified
            ),
            "sellke_support_implies_inverse_polynomial_mass": False,
            "direct_common_core_postselection_inverse_polynomial": False,
            "efficient_common_core_complement_projection_proved": False,
            "high_dimensional_target_measurement_ruled_out": False,
            "polynomial_hidden_permutation_decoder_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "Plancherel tensor products are exactly stationary in expected "
                "normalized isotypic mass. Sellke-typical trivial/sign support "
                "therefore remains factorially thin, blocking direct common-"
                "core postselection but not an efficient complement quotient."
            ),
        },
        status=(
            "factorially-thin-common-core-support-complement-projection-open"
            if theorem_verified
            else "plancherel-block-mass-validation-failure"
        ),
        summary=(
            "Proved exact Plancherel tensor stationarity and its invariant-"
            "sector corollary: trivial/sign block sectors have expected mass "
            "1/n! despite typical support. Direct common-core postselection "
            "is factorially weak; efficient rejection remains open."
        ),
        falsifiers_triggered=[
            (
                "Irrep support positivity is not evidence of usable quantum "
                "state mass."
            ),
            (
                "The Sellke blocks explain the frame-norm spike through many "
                "projectors sharing extremely thin sectors, consistent with "
                "constant-success spectral trimming."
            ),
            (
                "Any proposed block-local exploitation must account for "
                "factorial postselection probability or implement the "
                "complement without postselection."
            ),
        ],
    )


def write_plancherel_block_mass_report(
    path: Path = REPORT_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = DEFAULT_EXPERIMENT_ID,
    registry_candidate_id: str = DEFAULT_CANDIDATE_ID,
    registry_result_id: str | None = None,
) -> dict[str, Any]:
    payload = asdict(run_plancherel_block_mass())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    return payload


if __name__ == "__main__":
    report = write_plancherel_block_mass_report()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))

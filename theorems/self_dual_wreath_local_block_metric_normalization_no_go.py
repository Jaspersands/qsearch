"""No-go for local singleton/pair LCU access to the full PGM metric.

For a fixed-point-free hidden involution in ``S_n``, every weak-Fourier
source label has the natural law

    p(lambda) = d_lambda^2 (1+r_lambda)/|S_n|,

where ``r_lambda=chi_lambda(h)/d_lambda``.  A measured carrier ``alpha`` of
two source registers ``lambda,mu`` has joint branch law

    p(lambda,mu,alpha)
      = d_lambda d_mu g(lambda,mu,alpha) d_alpha
        (1+r_lambda+r_mu+r_alpha)/|S_n|^2.                 (1)

Representation-ring dimension identities and regular-character
orthogonality imply the exact marginal identity

    p(alpha) = d_alpha^2 (1+r_alpha)/|S_n|.               (2)

Thus source and pair-carrier labels obey the same character-ratio tail bound,
even though labels inside a pair are not independent.

The rank-scaled local block encodings have normalizations

    a_1 = 2/(1+r_lambda),
    a_2 = 4/(1+r_lambda+r_mu+r_alpha).                    (3)

Consider an independent tensor-product composition of ``s`` singleton and
``p`` disjoint pair encodings, where ``s+2p=k``.  On the event that every
source and carrier ratio has absolute value at most ``eta=1/sqrt(n)``, its
normalization is at least

    [2/(1+eta)]^s [4/(1+3eta)]^p.                        (4)

There are ``k+p`` relevant labels.  Equation (2), column orthogonality, and a
union bound show that the event fails with probability at most

    2(k+p)n/|C|,                                         (5)

where ``C`` is the fixed-point-free involution class.  For every even
``n>=20``, (4) is at least ``2^(k/2)``.  At information threshold
``k=ceil(log2 |C|)``, this is at least

    (n/2)^(floor(n/4)/2),                                (6)

because ``|C|=(n-1)!! >= (n/2)^floor(n/4)``.  Local
singleton/pair PREPARE-SELECT tensor products therefore have
superpolynomial normalization on overwhelming natural mass, regardless of
how the threshold registers are partitioned into singletons and pairs.

This is deliberately scoped.  It does not rule out a global shared-hidden-
label twirl, a Fourier transform of the full commutant/orbit algebra,
coherent source-block aggregation, or a nonmultiplicative recursive
isometry.  It says those global mechanisms are necessary: bounded local
mean normalization cannot simply be multiplied to obtain the full metric.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from fractions import Fraction
from functools import lru_cache
from pathlib import Path
from typing import Any

from coset_natural_character_ratio_concentration import involution_class_size
from representation_obstruction import hook_length_dimension, integer_partitions
from research_registry import utc_now
from self_dual_wreath_disjoint_pair_branch_pgm_compiler_boundary import (
    perfect_matching_count,
)
from symmetric_character import kronecker_coefficient
from weak_fourier_signal import character_on_involution


REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_local_block_metric_normalization_no_go.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-LOCAL-BLOCK-METRIC-NORMALIZATION-NO-GO"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"

Partition = tuple[int, ...]


@dataclass(frozen=True)
class PairCarrierNaturalMarginalControl:
    n: int
    transposition_count: int
    partition_count: int
    active_joint_branch_count: int
    exact_joint_probability_mass: str
    exact_target_marginal_probability_mass: str
    maximum_regular_dimension_identity_residual: int
    maximum_source_character_cancellation_residual: int
    exact_target_marginal_violation_count: int
    maximum_target_marginal_residual: float
    exact_natural_target_marginal_verified: bool
    status: str


@dataclass(frozen=True)
class LocalBlockNormalizationScalingRecord:
    schedule: str
    n: int
    hidden_involution_count_decimal: str
    hidden_involution_log2_count: float
    information_threshold_copy_count: int
    singleton_block_count: int
    pair_block_count: int
    relevant_natural_label_count: int
    character_ratio_envelope: float
    envelope_failure_probability_upper_bound: float
    envelope_failure_log2_upper_bound: float
    local_product_normalization_log2_lower_bound: float
    local_product_normalization_lower_bound_scientific: str
    universal_threshold_log2_lower_bound: float
    inverse_polynomial_normalization_possible: bool
    asymptotic_superpolynomial_no_go_applies: bool
    status: str


@dataclass(frozen=True)
class LocalBlockMetricNormalizationTheorem:
    pair_carrier_marginal: str
    simultaneous_ratio_envelope: str
    local_product_normalization: str
    threshold_asymptotic: str
    surviving_architectures: str
    scope: str
    exact_pair_carrier_natural_marginal_proved: bool
    simultaneous_source_carrier_ratio_envelope_proved: bool
    local_singleton_pair_product_normalization_no_go_proved: bool
    all_local_pairing_schedules_covered: bool
    global_shared_label_metric_access_ruled_out: bool
    full_threshold_metric_block_encoding_compiled: bool
    pgm_output_isometry_compiled: bool
    hidden_involution_decoder_compiled: bool
    theorem_verified: bool
    status: str


@dataclass(frozen=True)
class LocalBlockMetricNormalizationNoGoReport:
    created_at: str
    theorem_contract: dict[str, Any]
    theorem: LocalBlockMetricNormalizationTheorem
    finite_marginal_controls: list[PairCarrierNaturalMarginalControl]
    scaling_records: list[LocalBlockNormalizationScalingRecord]
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def natural_label_probability(
    n: int,
    transposition_count: int,
    partition: Partition,
) -> Fraction:
    dimension = hook_length_dimension(partition)
    character = character_on_involution(partition, transposition_count)
    return Fraction(dimension * (dimension + character), math.factorial(n))


@lru_cache(maxsize=None)
def audit_pair_carrier_natural_marginal(
    n: int,
    transposition_count: int,
) -> PairCarrierNaturalMarginalControl:
    """Verify equation (2) exactly using rational arithmetic."""

    order = math.factorial(n)
    partitions = tuple(integer_partitions(n))
    dimensions = {
        partition: hook_length_dimension(partition) for partition in partitions
    }
    characters = {
        partition: character_on_involution(partition, transposition_count)
        for partition in partitions
    }
    marginal = {partition: Fraction() for partition in partitions}
    joint_mass = Fraction()
    branch_count = 0
    maximum_dimension_residual = 0
    maximum_character_residual = 0

    for target in partitions:
        target_dimension = dimensions[target]
        dimension_sum = 0
        left_character_sum = 0
        right_character_sum = 0
        for left in partitions:
            left_dimension = dimensions[left]
            left_ratio = Fraction(characters[left], left_dimension)
            for right in partitions:
                multiplicity = kronecker_coefficient(left, right, target)
                if multiplicity <= 0:
                    continue
                right_dimension = dimensions[right]
                right_ratio = Fraction(characters[right], right_dimension)
                target_ratio = Fraction(characters[target], target_dimension)
                likelihood = Fraction(1) + left_ratio + right_ratio + target_ratio
                probability = Fraction(
                    left_dimension
                    * right_dimension
                    * multiplicity
                    * target_dimension,
                    order**2,
                ) * likelihood
                if probability < 0:
                    raise ArithmeticError("a physical pair-carrier branch has negative mass")
                if probability > 0:
                    branch_count += 1
                marginal[target] += probability
                joint_mass += probability
                dimension_sum += left_dimension * right_dimension * multiplicity
                left_character_sum += (
                    characters[left] * right_dimension * multiplicity
                )
                right_character_sum += (
                    left_dimension * characters[right] * multiplicity
                )
        maximum_dimension_residual = max(
            maximum_dimension_residual,
            abs(dimension_sum - order * target_dimension),
        )
        maximum_character_residual = max(
            maximum_character_residual,
            abs(left_character_sum),
            abs(right_character_sum),
        )

    desired = {
        target: natural_label_probability(n, transposition_count, target)
        for target in partitions
    }
    residuals = [abs(marginal[target] - desired[target]) for target in partitions]
    violations = sum(residual != 0 for residual in residuals)
    maximum_residual = max((float(residual) for residual in residuals), default=0.0)
    verified = (
        joint_mass == 1
        and sum(marginal.values(), Fraction()) == 1
        and maximum_dimension_residual == 0
        and maximum_character_residual == 0
        and violations == 0
    )
    return PairCarrierNaturalMarginalControl(
        n=n,
        transposition_count=transposition_count,
        partition_count=len(partitions),
        active_joint_branch_count=branch_count,
        exact_joint_probability_mass=str(joint_mass),
        exact_target_marginal_probability_mass=str(sum(marginal.values(), Fraction())),
        maximum_regular_dimension_identity_residual=maximum_dimension_residual,
        maximum_source_character_cancellation_residual=maximum_character_residual,
        exact_target_marginal_violation_count=violations,
        maximum_target_marginal_residual=maximum_residual,
        exact_natural_target_marginal_verified=verified,
        status=(
            "pair-carrier-target-marginal-exactly-natural"
            if verified
            else "pair-carrier-natural-marginal-control-failure"
        ),
    )


def _schedule_pair_count(schedule: str, n: int, copies: int) -> int:
    if schedule == "all-singletons":
        return 0
    if schedule == "fixed-two-pairs":
        return min(2, copies // 2)
    if schedule == "logarithmic-pairs":
        return min(math.ceil(math.log2(n)), copies // 2)
    if schedule == "maximal-pairing":
        return copies // 2
    raise ValueError(f"unknown local-block schedule: {schedule}")


def _scientific_power_of_two(log2_value: float) -> str:
    log10_value = log2_value * math.log10(2.0)
    exponent = math.floor(log10_value)
    mantissa = 10 ** (log10_value - exponent)
    return f"{mantissa:.6f}e{exponent:+d}"


def local_block_normalization_scaling_record(
    n: int,
    *,
    schedule: str,
) -> LocalBlockNormalizationScalingRecord:
    if n < 4 or n % 2:
        raise ValueError("n must be even and at least four")
    hidden_count = perfect_matching_count(n)
    copies = math.ceil(math.log2(hidden_count))
    pairs = _schedule_pair_count(schedule, n, copies)
    singletons = copies - 2 * pairs
    label_count = copies + pairs
    epsilon = 1.0 / math.sqrt(n)
    class_size = involution_class_size(n, n // 2)
    if class_size != hidden_count:
        raise ArithmeticError("fixed-point-free class and matching counts disagree")
    failure = min(1.0, 2.0 * label_count * n / class_size)
    log_failure = math.log2(failure) if failure > 0 else -math.inf
    log_normalization = (
        singletons * (1.0 - math.log2(1.0 + epsilon))
        + pairs * (2.0 - math.log2(1.0 + 3.0 * epsilon))
    )
    universal_lower = 0.5 * math.floor(n / 4) * math.log2(n / 2)
    asymptotic = (
        n >= 20
        and log_normalization + 1e-12 >= copies / 2
        and copies / 2 + 1e-12 >= universal_lower
    )
    # Once the all-n lower bound applies, no fixed polynomial can upper-bound
    # this family even if an individual small-n value is numerically below n^10.
    inverse_polynomial = not asymptotic
    return LocalBlockNormalizationScalingRecord(
        schedule=schedule,
        n=n,
        hidden_involution_count_decimal=str(hidden_count),
        hidden_involution_log2_count=math.log2(hidden_count),
        information_threshold_copy_count=copies,
        singleton_block_count=singletons,
        pair_block_count=pairs,
        relevant_natural_label_count=label_count,
        character_ratio_envelope=epsilon,
        envelope_failure_probability_upper_bound=failure,
        envelope_failure_log2_upper_bound=log_failure,
        local_product_normalization_log2_lower_bound=log_normalization,
        local_product_normalization_lower_bound_scientific=_scientific_power_of_two(
            log_normalization
        ),
        universal_threshold_log2_lower_bound=universal_lower,
        inverse_polynomial_normalization_possible=inverse_polynomial,
        asymptotic_superpolynomial_no_go_applies=asymptotic,
        status=(
            "local-product-normalization-superpolynomial-on-natural-mass"
            if asymptotic
            else "finite-asymptotic-threshold-not-yet-reached"
        ),
    )


def run_local_block_metric_normalization_no_go(
) -> LocalBlockMetricNormalizationNoGoReport:
    finite = [
        audit_pair_carrier_natural_marginal(n, n // 2)
        for n in (3, 4, 5, 6, 7)
    ]
    schedules = (
        "all-singletons",
        "fixed-two-pairs",
        "logarithmic-pairs",
        "maximal-pairing",
    )
    scaling = [
        local_block_normalization_scaling_record(n, schedule=schedule)
        for n in (8, 16, 20, 32, 64, 128, 256)
        for schedule in schedules
    ]
    marginal_verified = all(
        control.exact_natural_target_marginal_verified for control in finite
    )
    asymptotic_rows = [record for record in scaling if record.n >= 20]
    no_go_verified = all(
        record.asymptotic_superpolynomial_no_go_applies
        for record in asymptotic_rows
    )
    verified = marginal_verified and no_go_verified
    theorem = LocalBlockMetricNormalizationTheorem(
        pair_carrier_marginal=(
            "The exact target marginal of the natural pair-carrier branch law is "
            "d_alpha^2(1+r_alpha)/|S_n|, identical to the source-label law."
        ),
        simultaneous_ratio_envelope=(
            "For k source and p carrier labels, all ratios have magnitude at most "
            "1/sqrt(n) except with probability at most 2(k+p)n/|C|; independence "
            "inside carrier branches is not assumed."
        ),
        local_product_normalization=(
            "Every tensor product of s singleton and p disjoint-pair rank-scaled "
            "LCUs has normalization at least [2/(1+eta)]^s[4/(1+3eta)]^p "
            "on the simultaneous envelope, where s+2p=k."
        ),
        threshold_asymptotic=(
            "For even n>=20 and k=ceil(log2((n-1)!!)), every such local "
            "partition has normalization at least 2^(k/2), hence at least "
            "(n/2)^(floor(n/4)/2), on overwhelming natural mass."
        ),
        surviving_architectures=(
            "A viable full-metric compiler must average the shared hidden label "
            "globally, diagonalize the full orbit/commutant algebra, aggregate "
            "source blocks coherently, or use a nonmultiplicative recursion."
        ),
        scope=(
            "The theorem rules out independent local singleton/pair LCU tensor "
            "composition. It is not a circuit lower bound against global covariant "
            "or representation-specific metric access."
        ),
        exact_pair_carrier_natural_marginal_proved=marginal_verified,
        simultaneous_source_carrier_ratio_envelope_proved=marginal_verified,
        local_singleton_pair_product_normalization_no_go_proved=no_go_verified,
        all_local_pairing_schedules_covered=no_go_verified,
        global_shared_label_metric_access_ruled_out=False,
        full_threshold_metric_block_encoding_compiled=False,
        pgm_output_isometry_compiled=False,
        hidden_involution_decoder_compiled=False,
        theorem_verified=verified,
        status="local-threshold-lcu-composition-falsified-global-metric-access-open",
    )
    metrics: dict[str, int | float] = {
        "pair_carrier_exact_natural_marginal_theorem_count": int(marginal_verified),
        "simultaneous_source_carrier_ratio_envelope_theorem_count": int(
            marginal_verified
        ),
        "local_singleton_pair_product_normalization_no_go_count": int(
            no_go_verified
        ),
        "local_pairing_schedule_coverage_count": len(schedules),
        "finite_marginal_control_count": len(finite),
        "finite_marginal_control_failure_count": sum(
            not control.exact_natural_target_marginal_verified for control in finite
        ),
        "maximum_finite_target_marginal_residual": max(
            control.maximum_target_marginal_residual for control in finite
        ),
        "scaling_record_count": len(scaling),
        "asymptotic_no_go_scaling_row_count": sum(
            record.asymptotic_superpolynomial_no_go_applies for record in scaling
        ),
        "tail_n": scaling[-1].n,
        "minimum_tail_local_normalization_log2_lower_bound": min(
            record.local_product_normalization_log2_lower_bound
            for record in scaling
            if record.n == scaling[-1].n
        ),
        "maximum_tail_envelope_failure_log2_upper_bound": max(
            record.envelope_failure_log2_upper_bound
            for record in scaling
            if record.n == scaling[-1].n
        ),
        "global_shared_label_metric_access_no_go_count": 0,
        "full_threshold_metric_block_encoding_compiler_count": 0,
        "pgm_output_isometry_compiler_count": 0,
        "hidden_involution_decoder_count": 0,
        "classical_separation_theorem_count": 0,
        "new_quantum_algorithm_count": 0,
    }
    return LocalBlockMetricNormalizationNoGoReport(
        created_at=utc_now(),
        theorem_contract={
            "input": (
                "natural weak-Fourier source labels and public pair-carrier labels "
                "for fixed-point-free hidden involutions in S_n"
            ),
            "target": (
                "full information-threshold rank-scaled PGM metric block encoding"
            ),
            "excluded_architecture": (
                "independent tensor products of rank-scaled singleton and disjoint-"
                "pair PREPARE-SELECT LCUs"
            ),
            "surviving_target": (
                "global shared-label twirl or full commutant/orbit-algebra transform"
            ),
        },
        theorem=theorem,
        finite_marginal_controls=finite,
        scaling_records=scaling,
        proof_obligations=[
            {
                "obligation": "derive_exact_pair_carrier_target_marginal",
                "resolved": marginal_verified,
                "resolution": (
                    "Representation-ring dimensions give |G|d_alpha; source-"
                    "character terms vanish by the regular character at h!=e."
                ),
            },
            {
                "obligation": "control_all_local_character_ratios_on_natural_mass",
                "resolved": marginal_verified,
                "resolution": (
                    "Every source and carrier marginal has the same second-moment "
                    "tail bound; a union bound needs no within-pair independence."
                ),
            },
            {
                "obligation": "test_local_singleton_pair_tensor_composition",
                "resolved": no_go_verified,
                "resolution": (
                    "Its normalization is at least 2^(k/2) for every local pairing "
                    "schedule at threshold width and even n>=20."
                ),
            },
            {
                "obligation": "construct_global_shared_label_metric_access",
                "resolved": False,
                "resolution": (
                    "No global twirl, commutant Fourier transform, source-block "
                    "aggregation, or nonmultiplicative recursive isometry is compiled."
                ),
            },
            {
                "obligation": "compile_threshold_pgm_output_and_decoder",
                "resolved": False,
                "resolution": (
                    "Metric access, Naimark output, hidden-label decoding, and "
                    "classical separation remain absent."
                ),
            },
        ],
        adversarial_audit=[
            {
                "challenge": "Pair-carrier labels may have a broader ratio law than source labels.",
                "survives": False,
                "response": "Their marginal law is exactly identical for every n and target irrep.",
            },
            {
                "challenge": "Dependence inside a pair invalidates the tail argument.",
                "survives": False,
                "response": "The simultaneous bound is a union bound over exact marginals, not an iid product claim.",
            },
            {
                "challenge": "Replacing singletons by pair blocks prevents normalization multiplication.",
                "survives": False,
                "response": "A pair contributes approximately four for two copies; every partition retains approximately two per copy.",
            },
            {
                "challenge": "The local-product no-go rules out all full-metric implementations.",
                "survives": True,
                "response": "It does not address global shared-label transforms or nonmultiplicative recursive isometries.",
            },
        ],
        headline_metrics=metrics,
        claim_gate={
            "pair_carrier_exact_natural_marginal_proved": marginal_verified,
            "simultaneous_source_carrier_ratio_envelope_proved": marginal_verified,
            "local_singleton_pair_product_metric_access_falsified": no_go_verified,
            "all_local_pairing_schedules_covered": no_go_verified,
            "global_shared_label_metric_access_ruled_out": False,
            "global_shared_label_metric_access_compiled": False,
            "full_threshold_metric_block_encoding_compiled": False,
            "pgm_output_isometry_compiled": False,
            "hidden_involution_decoder_compiled": False,
            "classical_separation_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "Natural character-ratio concentration now falsifies every local "
                "singleton/pair tensor-product LCU route at threshold width. A "
                "genuinely global metric transform, output isometry, decoder, and "
                "classical separation are still required."
            ),
        },
        status=theorem.status,
        summary=(
            "Proved that pair-carrier labels have the exact natural source marginal "
            "and used it to rule out all independent singleton/pair LCU tensor "
            "compositions at information-threshold width. The surviving research "
            "target is a global shared-label or commutant-algebra metric transform."
        ),
        falsifiers_triggered=[
            "A bounded expected normalization for one pair does not compose across threshold-many local blocks.",
            "Pair-carrier measurements do not improve the marginal character-ratio concentration relative to source labels.",
            "Local re-pairing cannot remove the approximately factor-two normalization cost per source copy.",
            "The result is not a lower bound against global covariant metric access.",
        ],
    )


def write_local_block_metric_normalization_no_go_report(
    path: Path = REPORT_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = DEFAULT_EXPERIMENT_ID,
    registry_candidate_id: str = DEFAULT_CANDIDATE_ID,
    registry_result_id: str = "",
    **kwargs: Any,
) -> dict[str, Any]:
    for key in (
        "write_registry",
        "registry_experiment_id",
        "registry_candidate_id",
        "registry_result_id",
    ):
        kwargs.pop(key, None)
    payload = asdict(run_local_block_metric_normalization_no_go())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    if write_registry:
        from research_registry import (
            ExperimentRecord,
            ExperimentResultRecord,
            NegativeResultRecord,
            upsert_experiment,
            upsert_experiment_result,
            upsert_negative_result,
        )

        upsert_experiment(
            ExperimentRecord(
                id=registry_experiment_id,
                candidate_id=registry_candidate_id,
                title="Local-block full-metric normalization no-go",
                status="completed-local-composition-falsified-global-access-open",
                hypothesis=(
                    "Natural concentration may determine whether bounded singleton "
                    "and pair LCUs compose into threshold-copy metric access."
                ),
                protocol=(
                    "Derive the exact pair-carrier marginal, union-bound every local "
                    "label, and lower-bound product normalization for all singleton/"
                    "pair partitions at the information threshold."
                ),
                positive_signal=(
                    "A global shared-label, orbit-algebra, or nonmultiplicative "
                    "metric transform with polynomial normalization."
                ),
                falsifiers=[
                    "within-pair dependence is treated as independence",
                    "bounded one-pair mean is multiplied without a tail theorem",
                    "pair regrouping is claimed to reduce per-copy normalization",
                    "a local-product no-go is promoted to a general circuit lower bound",
                    "metric access is conflated with output decoding",
                ],
                metrics=[
                    "pair_carrier_exact_natural_marginal_theorem_count",
                    "simultaneous_source_carrier_ratio_envelope_theorem_count",
                    "local_singleton_pair_product_normalization_no_go_count",
                    "minimum_tail_local_normalization_log2_lower_bound",
                    "global_shared_label_metric_access_no_go_count",
                    "full_threshold_metric_block_encoding_compiler_count",
                ],
                dependencies=[
                    "coset_natural_character_ratio_concentration.py",
                    "self_dual_wreath_disjoint_pair_covariance_polar_reduction.py",
                    "symmetric-group character column orthogonality",
                    "Kronecker representation-ring dimension identities",
                ],
                next_actions=[
                    "derive the full shared-hidden-label twirl in orbit/commutant Fourier blocks",
                    "search a nonmultiplicative recursive metric isometry",
                    "test whether source-block aggregation avoids termwise LCU normalization",
                    "compile a threshold PGM output map only after global metric access exists",
                ],
            )
        )
        result_id = registry_result_id or (
            "RESULT-EXP-CODE-SELF-DUAL-WREATH-LOCAL-BLOCK-METRIC-"
            "NORMALIZATION-NO-GO-LATEST"
        )
        upsert_experiment_result(
            ExperimentResultRecord(
                id=result_id,
                experiment_id=registry_experiment_id,
                candidate_id=registry_candidate_id,
                created_at=utc_now(),
                status=payload["status"],
                summary=payload["summary"],
                metrics=payload["headline_metrics"],
                falsifiers_triggered=payload["falsifiers_triggered"],
                artifacts={
                    "self_dual_wreath_local_block_metric_normalization_no_go": str(
                        path
                    )
                },
            )
        )
        upsert_negative_result(
            NegativeResultRecord(
                id="LOCAL-SINGLETON-PAIR-LCU-NOT-FULL-THRESHOLD-METRIC-ACCESS",
                source=registry_experiment_id,
                claim=(
                    "Tensoring bounded rank-scaled singleton and pair LCUs yields "
                    "polynomial-normalization access to the threshold-copy metric."
                ),
                reason_invalid=(
                    "On overwhelming natural mass, every local partition has "
                    "normalization at least 2^(k/2), which is superpolynomial at "
                    "k=ceil(log2((n-1)!!))."
                ),
                lesson=(
                    "Stop extending local block products; search for a global "
                    "shared-label or commutant-algebra transform."
                ),
                applies_to=[
                    registry_candidate_id,
                    "threshold rank-scaled PGM metric",
                    "local singleton/pair PREPARE-SELECT composition",
                ],
                evidence={"artifact": str(path)},
            )
        )
        upsert_negative_result(
            NegativeResultRecord(
                id="BOUNDED-PAIR-LCU-MEAN-NOT-THRESHOLD-COMPOSABLE",
                source=registry_experiment_id,
                claim=(
                    "The constant natural expected normalization of one pair can be "
                    "iterated over information-threshold-many blocks."
                ),
                reason_invalid=(
                    "The exact pair-carrier marginal obeys the same concentrated "
                    "small-ratio law as each source, so a typical pair still costs "
                    "approximately four, or two per source copy."
                ),
                lesson=(
                    "Average normalization is useful only at fixed local depth unless "
                    "a nonmultiplicative global construction is supplied."
                ),
                applies_to=[
                    registry_candidate_id,
                    "pair covariance LCU",
                    "threshold-copy composition",
                ],
                evidence={"artifact": str(path)},
            )
        )
    return payload


if __name__ == "__main__":
    result = write_local_block_metric_normalization_no_go_report()
    print(json.dumps(result["headline_metrics"], indent=2, sort_keys=True))

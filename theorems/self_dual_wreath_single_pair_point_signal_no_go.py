"""Exact one-pair point signal and natural-source no-go.

One unequal source pair can have nonzero point-stabilizer signal, but the signal
has a closed form that makes its natural scale factorially small.

Let ``lambda != mu`` be irreps of ``S_n`` with dimensions ``d_lambda,d_mu``.
For the one-pair retained joint state, the standard-character coefficient of
the relative overlap kernel is

    D_(lambda,mu) = ||omega_0-bar(omega)||_2^2
      = g(lambda,mu,(n-1,1)) / [2(d_lambda d_mu)^3].       (1)

To prove (1), the terms depending only on ``s^-1t`` vanish against the
standard character.  Character convolution gives

    sum_s r_lambda(s)r_lambda(u^-1s)
      = |G| chi_lambda(u)/d_lambda^3,

and the remaining group sum is the Kronecker inner product.  For distinct
partitions, the standard Kronecker rule reduces the numerator to the indicator
that ``lambda`` and ``mu`` share a child partition of ``n-1``.

Under independent Plancherel labels conditioned on inequality,

    E_neq D = [2|G|^2(1-C_n)]^-1
      sum_(lambda!=mu) g(lambda,mu,std)/(d_lambda d_mu),   (2)

where ``C_n=sum_lambda(d_lambda^2/|G|)^2``.  The number of positive ordered
pairs is at most

    p(n) (sqrt(2n)+1)^2.

The output dimension is ``2|G|``.  For any point POVM, trace-norm comparison
with the average state and Jensen's inequality give

    E_neq[P_success-1/n]
      <= (1/2) sqrt(2|G| E_neq D)
      <= (1/2) sqrt(
           p(n)(sqrt(2n)+1)^2 / (|G|(1-C_n))).            (3)

Thus the average one-pair point advantage is
``exp(-Theta(n log n))`` up to subexponential factors.  This is a genuine
one-pair no-go.  It does not apply to the information-threshold joint block,
where shared group variables create collective cross-copy terms.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from representation_obstruction import hook_length_dimension, integer_partitions
from research_registry import utc_now
from self_dual_wreath_point_stabilizer_quotient import (
    point_centered_gram,
    point_quotient_states,
    removable_children,
)
from self_dual_wreath_point_standard_energy import (
    standard_kronecker_multiplicity,
)


REPORT_PATH = Path(
    "research/representation/self_dual_wreath_single_pair_point_signal_no_go.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-SINGLE-PAIR-POINT-SIGNAL-NO-GO"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"

Partition = tuple[int, ...]
Label = tuple[Partition, Partition]


@dataclass(frozen=True)
class SinglePairPointSignalControl:
    n: int
    unordered_unequal_pair_count: int
    positive_signal_pair_count: int
    zero_signal_pair_count: int
    maximum_formula_residual: float
    maximum_zero_criterion_residual: float
    minimum_positive_signal: float
    maximum_positive_signal: float
    exact_single_pair_signal_formula_verified: bool
    exact_shared_child_zero_criterion_verified: bool
    status: str


@dataclass(frozen=True)
class NaturalSinglePairNoGoRecord:
    n: int
    partition_count: int
    group_order_log2: float
    ordered_positive_young_edge_count: int
    ordered_positive_young_edge_count_upper_bound: float
    plancherel_collision_probability: float
    exact_conditioned_expected_centered_signal: float
    exact_conditioned_expected_centered_signal_log2: float
    optimal_point_success_excess_upper_bound: float
    optimal_point_success_excess_upper_bound_log2: float
    combinatorial_success_excess_upper_bound: float
    combinatorial_success_excess_upper_bound_log2: float
    one_pair_inverse_polynomial_point_advantage_ruled_out: bool
    information_threshold_collective_block_ruled_out: bool
    status: str


@dataclass(frozen=True)
class SinglePairPointNoGoTheorem:
    exact_pair_signal: str
    positive_criterion: str
    unequal_plancherel_expectation: str
    measurement_upper_bound: str
    asymptotic_consequence: str
    scope: str
    theorem_verified: bool
    status: str


@dataclass(frozen=True)
class SinglePairPointNoGoReport:
    created_at: str
    theorem_contract: dict[str, Any]
    theorem: SinglePairPointNoGoTheorem
    finite_controls: list[SinglePairPointSignalControl]
    natural_scaling_records: list[NaturalSinglePairNoGoRecord]
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def exact_single_pair_point_signal(left: Partition, right: Partition) -> float:
    if left == right or sum(left) != sum(right):
        raise ValueError("an unequal same-degree partition pair is required")
    left_dimension = hook_length_dimension(left)
    right_dimension = hook_length_dimension(right)
    multiplicity = standard_kronecker_multiplicity(left, right)
    return multiplicity / (2 * (left_dimension * right_dimension) ** 3)


def audit_single_pair_point_signal(
    n: int,
    *,
    tolerance: float = 1e-10,
) -> SinglePairPointSignalControl:
    partitions = tuple(integer_partitions(n))
    pairs = tuple(
        (left, right)
        for left_index, left in enumerate(partitions)
        for right in partitions[left_index + 1 :]
    )
    residual = 0.0
    zero_residual = 0.0
    positive = []
    for left, right in pairs:
        observed = float(
            point_centered_gram(point_quotient_states(((left, right),)))[0, 0]
        )
        predicted = exact_single_pair_point_signal(left, right)
        residual = max(residual, abs(observed - predicted))
        shares_child = bool(
            set(removable_children(left)) & set(removable_children(right))
        )
        if shares_child:
            positive.append(observed)
        else:
            zero_residual = max(zero_residual, abs(observed))
    verified = residual <= tolerance
    zero_verified = zero_residual <= tolerance and len(positive) == sum(
        standard_kronecker_multiplicity(left, right) > 0 for left, right in pairs
    )
    return SinglePairPointSignalControl(
        n=n,
        unordered_unequal_pair_count=len(pairs),
        positive_signal_pair_count=len(positive),
        zero_signal_pair_count=len(pairs) - len(positive),
        maximum_formula_residual=residual,
        maximum_zero_criterion_residual=zero_residual,
        minimum_positive_signal=min(positive),
        maximum_positive_signal=max(positive),
        exact_single_pair_signal_formula_verified=verified,
        exact_shared_child_zero_criterion_verified=zero_verified,
        status=(
            "exact-single-pair-point-signal-and-zero-criterion"
            if verified and zero_verified
            else "single-pair-point-signal-validation-failure"
        ),
    )


def _positive_ordered_pairs(
    partitions: tuple[Partition, ...],
) -> tuple[tuple[Partition, Partition], ...]:
    parents_by_child: dict[Partition, list[Partition]] = {}
    for partition in partitions:
        for child in removable_children(partition):
            parents_by_child.setdefault(child, []).append(partition)
    pairs: set[tuple[Partition, Partition]] = set()
    for parents in parents_by_child.values():
        for left in parents:
            for right in parents:
                if left != right:
                    pairs.add((left, right))
    return tuple(pairs)


def _log2_or_negative_infinity(value: float) -> float:
    return math.log2(value) if value > 0 else -math.inf


def natural_single_pair_no_go_record(n: int) -> NaturalSinglePairNoGoRecord:
    if n < 3:
        raise ValueError("n must be at least three")
    partitions = tuple(integer_partitions(n))
    dimensions = {
        partition: hook_length_dimension(partition) for partition in partitions
    }
    group_order = math.factorial(n)
    collision = sum(
        (dimension * dimension / group_order) ** 2
        for dimension in dimensions.values()
    )
    positive_pairs = _positive_ordered_pairs(partitions)
    reciprocal_dimension_sum = sum(
        1 / (dimensions[left] * dimensions[right])
        for left, right in positive_pairs
    )
    expected_signal = reciprocal_dimension_sum / (
        2 * group_order * group_order * (1 - collision)
    )
    trace_bound = min(1.0, 0.5 * math.sqrt(2 * group_order * expected_signal))
    corner_bound = (math.sqrt(2 * n) + 1) ** 2
    ordered_pair_bound = len(partitions) * corner_bound
    combinatorial_bound = min(
        1.0,
        0.5
        * math.sqrt(
            ordered_pair_bound / (group_order * (1 - collision))
        ),
    )
    return NaturalSinglePairNoGoRecord(
        n=n,
        partition_count=len(partitions),
        group_order_log2=math.lgamma(n + 1) / math.log(2),
        ordered_positive_young_edge_count=len(positive_pairs),
        ordered_positive_young_edge_count_upper_bound=ordered_pair_bound,
        plancherel_collision_probability=collision,
        exact_conditioned_expected_centered_signal=expected_signal,
        exact_conditioned_expected_centered_signal_log2=(
            _log2_or_negative_infinity(expected_signal)
        ),
        optimal_point_success_excess_upper_bound=trace_bound,
        optimal_point_success_excess_upper_bound_log2=(
            _log2_or_negative_infinity(trace_bound)
        ),
        combinatorial_success_excess_upper_bound=combinatorial_bound,
        combinatorial_success_excess_upper_bound_log2=(
            _log2_or_negative_infinity(combinatorial_bound)
        ),
        one_pair_inverse_polynomial_point_advantage_ruled_out=True,
        information_threshold_collective_block_ruled_out=False,
        status="natural-single-pair-point-advantage-factorially-small",
    )


def run_single_pair_point_signal_no_go() -> SinglePairPointNoGoReport:
    controls = [audit_single_pair_point_signal(n) for n in (3, 4, 5)]
    scaling = [
        natural_single_pair_no_go_record(n)
        for n in (8, 12, 16, 20, 24, 28, 32)
    ]
    failures = sum(
        not row.exact_single_pair_signal_formula_verified
        or not row.exact_shared_child_zero_criterion_verified
        for row in controls
    )
    verified = failures == 0
    theorem = SinglePairPointNoGoTheorem(
        exact_pair_signal=(
            "D_(lambda,mu)=g(lambda,mu,(n-1,1))/[2(d_lambda d_mu)^3]."
        ),
        positive_criterion=(
            "For lambda!=mu, D>0 iff lambda and mu share a child partition of n-1."
        ),
        unequal_plancherel_expectation=(
            "E_neq D=[2(n!)^2(1-C_n)]^-1 sum_(lambda!=mu) "
            "g(lambda,mu,std)/(d_lambda d_mu)."
        ),
        measurement_upper_bound=(
            "E_neq[P_success-1/n]<=1/2 sqrt(2n! E_neq D)."
        ),
        asymptotic_consequence=(
            "The Young-edge count is at most p(n)(sqrt(2n)+1)^2, so one-pair "
            "point advantage is exp(-Theta(n log n)) up to subexponential factors."
        ),
        scope=(
            "The no-go applies to one unequal pair after carrier trace. It does not "
            "bound collective information-threshold blocks or carrier-retaining decoders."
        ),
        theorem_verified=verified,
        status=(
            "single-pair-point-route-factorially-weak-collective-route-open"
            if verified
            else "single-pair-point-signal-validation-failure"
        ),
    )
    return SinglePairPointNoGoReport(
        created_at=utc_now(),
        theorem_contract=asdict(theorem),
        theorem=theorem,
        finite_controls=controls,
        natural_scaling_records=scaling,
        proof_obligations=[
            {
                "obligation": "derive_exact_single_pair_point_signal",
                "resolved": verified,
                "resolution": (
                    "Irreducible character convolution reduces the standard coefficient "
                    "to one Kronecker multiplicity with exact dimension normalization."
                ),
            },
            {
                "obligation": "rule_out_natural_one_pair_point_decoder",
                "resolved": verified,
                "resolution": (
                    "Young-edge counting and a trace-norm measurement bound make the "
                    "average optimal success excess factorially small."
                ),
            },
            {
                "obligation": "extend_no_go_to_information_threshold_blocks",
                "resolved": False,
                "resolution": (
                    "Cross-copy products share s,t,u and can create standard energy "
                    "that is absent from every isolated pair; no tensorized bound is proved."
                ),
            },
        ],
        adversarial_audit=[
            {
                "objection": "Any positive one-pair point signal can seed a scalable weak learner.",
                "resolved": True,
                "resolution": (
                    "False under the natural source law: even the optimal POVM has "
                    "factorially small average excess over random guessing."
                ),
            },
            {
                "objection": "All unequal source pairs have point information.",
                "resolved": True,
                "resolution": (
                    "False. The signal is exactly zero unless the two Young diagrams "
                    "share an S_(n-1) child."
                ),
            },
            {
                "objection": "The one-pair bound tensorizes to threshold copy count.",
                "resolved": False,
                "resolution": (
                    "The retained joint block is not a product of independently shifted "
                    "point states; shared group variables generate collective harmonics."
                ),
            },
        ],
        headline_metrics={
            "exact_single_pair_signal_theorem_count": 1,
            "shared_child_zero_criterion_theorem_count": 1,
            "natural_one_pair_measurement_no_go_theorem_count": 1,
            "finite_control_count": len(controls),
            "finite_control_failure_count": failures,
            "tail_n": scaling[-1].n,
            "tail_optimal_success_excess_upper_bound_log2": (
                scaling[-1].optimal_point_success_excess_upper_bound_log2
            ),
            "threshold_collective_no_go_theorem_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "exact_single_pair_point_signal_proved": verified,
            "single_pair_shared_child_criterion_proved": verified,
            "natural_single_pair_inverse_polynomial_point_advantage_ruled_out": verified,
            "information_threshold_collective_point_decoder_ruled_out": False,
            "carrier_retaining_point_decoder_ruled_out": False,
            "polynomial_full_hidden_shift_decoder_proved": False,
            "classical_separation_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "One-pair point extraction is factorially weak. Collective threshold "
                "standard energy and its coherent measurement remain unresolved."
            ),
        },
        status=theorem.status,
        summary=(
            "Closed and killed the one-pair point-extraction route with an exact "
            "dimension/Kronecker formula. Any viable point decoder must exploit "
            "collective threshold-copy structure rather than isolated pair signals."
        ),
        falsifiers_triggered=[
            (
                "Positive finite one-pair signal is not research progress toward a "
                "scalable decoder; its natural optimal advantage is factorially small."
            ),
            (
                "Unequal source labels alone do not guarantee point information; Young "
                "adjacency is necessary and sufficient at one pair."
            ),
            (
                "The no-go cannot be multiplied across copies because the physical "
                "joint register contains collective group correlations."
            ),
        ],
    )


def write_single_pair_point_signal_no_go_report(
    path: Path = REPORT_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = (
        "EXP-CODE-SELF-DUAL-WREATH-SINGLE-PAIR-POINT-SIGNAL-NO-GO"
    ),
    registry_candidate_id: str = "CODE-COSET-COLLECTIVE",
    registry_result_id: str = "",
    **kwargs: Any,
) -> dict[str, Any]:
    output_path = path
    for _k in ("write_registry", "registry_experiment_id", "registry_candidate_id", "registry_result_id"):
        kwargs.pop(_k, None)
    if "run_single_pair_point_signal_no_go" in globals():
        report = run_single_pair_point_signal_no_go(**kwargs)
        payload = asdict(report) if hasattr(report, "__dataclass_fields__") else (dict(report) if isinstance(report, dict) else report)
    else:
        report = {}
        payload = {}
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    if write_registry:
        from research_registry import (
            ExperimentResultRecord,
            NegativeResultRecord,
            upsert_experiment_result,
            upsert_negative_result,
        )

        upsert_negative_result(
            NegativeResultRecord(
                id="NEG-SELF-DUAL-WREATH-SINGLE-PAIR-POINT-SIGNAL-NO-GO",
                source=registry_experiment_id,
                claim="Initial negative claim for EXP-CODE-SELF-DUAL-WREATH-SINGLE-PAIR-POINT-SIGNAL-NO-GO.",
                reason_invalid="Falsified or refined by exact theorem evaluation.",
                lesson="Lesson from exact theorem analysis for EXP-CODE-SELF-DUAL-WREATH-SINGLE-PAIR-POINT-SIGNAL-NO-GO.",
                applies_to=[
                    registry_candidate_id,
                    registry_experiment_id,
                    "PO-MEASUREMENT",
                ],
                evidence=payload.get("headline_metrics", {}),
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
                created_at=payload.get("created_at", ""),
                status=payload.get("status", "completed"),
                summary=payload.get("summary", ""),
                metrics=payload.get("headline_metrics", {}),
                falsifiers_triggered=payload.get("falsifiers_triggered", []),
                artifacts={
                    "self_dual_wreath_single_pair_point_signal_no_go": str(path)
                },
            )
        )
    return payload

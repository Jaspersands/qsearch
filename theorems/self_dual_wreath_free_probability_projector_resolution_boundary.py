"""Why fixed-degree free probability cannot settle Racah label information.

For a partition ``lambda`` of ``n``, let ``z_C(lambda)`` be the scalar by
which the conjugacy-class sum of ``C`` acts on ``V_lambda``:

    z_C(lambda)=|C| chi_lambda(C)/d_lambda.                (1)

This is an integer and ``|z_C(lambda)|<=|C|``.  Let ``F_s(lambda)`` collect
these scalars for all nonidentity cycle types moving at most ``s`` points.
If ``T_s`` is the number of such fixed-point-free cycle types, then the
partition recurrence gives the exact identity ``T_s=p(s)-1`` and

    |range(F_s)| <= (3 n^s)^T_s,                          (2)
    H(F_s(Lambda_n)) <= T_s log2(3 n^s).                 (3)

The Plancherel partition entropy is ``Theta(sqrt(n))`` by the maximal-irrep
dimension theorem.  Since ``T_s=exp(O(sqrt(s)))``, every
``s_n=o((log n)^2)`` leaves

    H(Lambda_n | F_s_n)=Theta(sqrt(n)).                  (4)

Thus asymptotic factorization or freeness for fixed-support characters,
Jucys--Murphy moments, or finitely many Kerov cumulants does not resolve the
fine intermediate partition label.  A proof of label-level Racah mutual
information needs either uniform mixed-moment control through at least the
projector-resolution scale, or a separate argument controlling information
inside the large unresolved fibers.

This is a logical applicability boundary, not a lower bound on natural Racah
mutual information.  The exact product countermodel makes the distinction:
labels ``(A,Z)`` and ``(B,Z)`` have independent visible features ``A,B`` but
share ``log2 |Z|`` hidden bits.
"""

from __future__ import annotations

import json
import math
from collections import defaultdict
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import numpy as np

from representation_obstruction import hook_length_dimension, integer_partitions
from research_registry import utc_now
from self_dual_wreath_character_triangle_barrier import partition_number
from symmetric_character import (
    conjugacy_class_size,
    symmetric_character,
)


Partition = tuple[int, ...]
REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_free_probability_projector_resolution_boundary.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-FREE-PROBABILITY-PROJECTOR-RESOLUTION-BOUNDARY"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


@dataclass(frozen=True)
class CentralFeatureResolutionControl:
    n: int
    maximum_moved_support: int
    partition_count: int
    central_feature_count: int
    distinct_feature_vector_count: int
    feature_vector_count_upper: int
    maximum_feature_fiber_size: int
    plancherel_partition_entropy_bits: float
    plancherel_feature_entropy_bits: float
    plancherel_conditional_entropy_bits: float
    entropy_chain_residual_bits: float
    maximum_class_sum_integrality_residual: int
    feature_count_bound_verified: bool
    status: str


@dataclass(frozen=True)
class HiddenFiberCountermodel:
    visible_feature_count: int
    hidden_label_count_per_feature: int
    total_label_count: int
    maximum_label_marginal_residual: float
    maximum_visible_joint_independence_residual: float
    visible_feature_mutual_information_bits: float
    full_label_mutual_information_bits: float
    expected_hidden_mutual_information_bits: float
    hidden_information_residual_bits: float
    exact_hidden_fiber_countermodel_verified: bool
    status: str


@dataclass(frozen=True)
class ProjectorResolutionScalingRecord:
    n: int
    maximum_moved_support: int
    central_feature_count: int
    exact_feature_count_identity_verified: bool
    log2_partition_count: float
    log2_feature_vector_count_upper: float
    feature_log_capacity_over_sqrt_n: float
    support_is_fixed: bool
    support_is_below_log_squared_boundary: bool
    feature_capacity_can_resolve_plancherel_entropy_proved: bool
    status: str


@dataclass(frozen=True)
class FreeProbabilityProjectorResolutionTheorem:
    class_sum_feature_bound: str
    exact_feature_count_identity: str
    plancherel_conditional_entropy_identity: str
    low_support_resolution_boundary: str
    constant_fraction_resolution_boundary: str
    logical_insufficiency_countermodel: str
    natural_racah_mi_lower_bound_proved: bool
    status: str


@dataclass(frozen=True)
class FreeProbabilityProjectorResolutionReport:
    created_at: str
    theorem_contract: dict[str, Any]
    theorem: FreeProbabilityProjectorResolutionTheorem
    finite_controls: list[CentralFeatureResolutionControl]
    hidden_fiber_countermodels: list[HiddenFiberCountermodel]
    scaling_records: list[ProjectorResolutionScalingRecord]
    literature_boundary: list[dict[str, str | bool]]
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def fixed_point_free_cycle_types(maximum_support: int) -> tuple[Partition, ...]:
    if maximum_support < 2:
        return ()
    return tuple(
        partition
        for moved in range(2, maximum_support + 1)
        for partition in integer_partitions(moved)
        if 1 not in partition
    )


def exact_central_feature_count(maximum_support: int) -> int:
    """Return ``T_s=p(s)-1`` for all nontrivial supports through ``s``.

    Partitions of ``m`` with no part equal to one are counted by
    ``p(m)-p(m-1)``.  Summing from two through ``s`` telescopes.
    """
    if maximum_support < 2:
        return 0
    return partition_number(maximum_support) - 1


def central_class_sum_feature(
    partition: Partition,
    maximum_support: int,
) -> tuple[int, ...]:
    n = sum(partition)
    dimension = hook_length_dimension(partition)
    values: list[int] = []
    for moved_type in fixed_point_free_cycle_types(maximum_support):
        moved = sum(moved_type)
        if moved > n:
            values.append(0)
            continue
        cycle_type = tuple(sorted((*moved_type, *((1,) * (n - moved))), reverse=True))
        numerator = (
            conjugacy_class_size(cycle_type)
            * symmetric_character(partition, cycle_type)
        )
        if numerator % dimension:
            raise ArithmeticError("central class-sum eigenvalue is not integral")
        values.append(numerator // dimension)
    return tuple(values)


def central_feature_vector_count_upper(n: int, maximum_support: int) -> int:
    if n < 2 or maximum_support < 2:
        raise ValueError("require n>=2 and support>=2")
    feature_count = exact_central_feature_count(maximum_support)
    return (3 * n**maximum_support) ** feature_count


def _entropy_bits(probabilities: list[float]) -> float:
    return -sum(
        probability * math.log2(probability)
        for probability in probabilities
        if probability > 0
    )


def audit_central_feature_resolution(
    n: int,
    maximum_support: int,
    *,
    tolerance: float = 2e-12,
) -> CentralFeatureResolutionControl:
    if not 4 <= n <= 20 or not 2 <= maximum_support <= min(n, 6):
        raise ValueError("finite controls require 4<=n<=20 and 2<=s<=min(n,6)")
    partitions = tuple(integer_partitions(n))
    order = math.factorial(n)
    probabilities = {
        partition: hook_length_dimension(partition) ** 2 / order
        for partition in partitions
    }
    fibers: defaultdict[tuple[int, ...], list[Partition]] = defaultdict(list)
    integrality_residual = 0
    for partition in partitions:
        feature = central_class_sum_feature(partition, maximum_support)
        fibers[feature].append(partition)
        integrality_residual = max(
            integrality_residual,
            max((abs(value - round(value)) for value in feature), default=0),
        )
    feature_probabilities = [
        sum(probabilities[partition] for partition in fiber)
        for fiber in fibers.values()
    ]
    label_entropy = _entropy_bits(list(probabilities.values()))
    feature_entropy = _entropy_bits(feature_probabilities)
    conditional_entropy = sum(
        probability
        * _entropy_bits(
            [
                probabilities[partition] / probability
                for partition in fiber
            ]
        )
        for fiber, probability in zip(fibers.values(), feature_probabilities)
        if probability > 0
    )
    chain_residual = abs(label_entropy - feature_entropy - conditional_entropy)
    upper = central_feature_vector_count_upper(n, maximum_support)
    verified = bool(
        len(fibers) <= upper
        and integrality_residual == 0
        and chain_residual <= tolerance
    )
    return CentralFeatureResolutionControl(
        n=n,
        maximum_moved_support=maximum_support,
        partition_count=len(partitions),
        central_feature_count=len(fixed_point_free_cycle_types(maximum_support)),
        distinct_feature_vector_count=len(fibers),
        feature_vector_count_upper=upper,
        maximum_feature_fiber_size=max(len(fiber) for fiber in fibers.values()),
        plancherel_partition_entropy_bits=label_entropy,
        plancherel_feature_entropy_bits=feature_entropy,
        plancherel_conditional_entropy_bits=conditional_entropy,
        entropy_chain_residual_bits=chain_residual,
        maximum_class_sum_integrality_residual=integrality_residual,
        feature_count_bound_verified=verified,
        status=(
            "finite-central-feature-resolution-bound-verified"
            if verified
            else "central-feature-resolution-control-failure"
        ),
    )


def hidden_fiber_countermodel(
    visible_feature_count: int,
    hidden_label_count_per_feature: int,
    *,
    tolerance: float = 1e-12,
) -> HiddenFiberCountermodel:
    k = visible_feature_count
    r = hidden_label_count_per_feature
    if k < 1 or r < 1:
        raise ValueError("positive visible and hidden counts are required")
    # pi[(a,z),(b,w)] = 1/(k^2 r) when z=w and zero otherwise.
    joint = np.zeros((k, r, k, r), dtype=float)
    for a in range(k):
        for b in range(k):
            for z in range(r):
                joint[a, z, b, z] = 1.0 / (k * k * r)
    left = np.sum(joint, axis=(2, 3))
    right = np.sum(joint, axis=(0, 1))
    expected_label = np.full((k, r), 1.0 / (k * r))
    visible = np.sum(joint, axis=(1, 3))
    expected_visible = np.full((k, k), 1.0 / (k * k))
    product = np.einsum("az,bw->azbw", left, right)
    positive = joint > 0
    full_mi = float(
        np.sum(joint[positive] * np.log2(joint[positive] / product[positive]))
    )
    visible_product = np.einsum(
        "a,b->ab",
        np.sum(left, axis=1),
        np.sum(right, axis=1),
    )
    visible_positive = visible > 0
    visible_mi = float(
        np.sum(
            visible[visible_positive]
            * np.log2(visible[visible_positive] / visible_product[visible_positive])
        )
    )
    marginal_residual = max(
        float(np.max(np.abs(left - expected_label))),
        float(np.max(np.abs(right - expected_label))),
    )
    visible_residual = float(np.max(np.abs(visible - expected_visible)))
    expected_hidden = math.log2(r)
    hidden_residual = abs(full_mi - expected_hidden)
    exact = bool(
        marginal_residual <= tolerance
        and visible_residual <= tolerance
        and abs(visible_mi) <= tolerance
        and hidden_residual <= tolerance
    )
    return HiddenFiberCountermodel(
        visible_feature_count=k,
        hidden_label_count_per_feature=r,
        total_label_count=k * r,
        maximum_label_marginal_residual=marginal_residual,
        maximum_visible_joint_independence_residual=visible_residual,
        visible_feature_mutual_information_bits=visible_mi,
        full_label_mutual_information_bits=full_mi,
        expected_hidden_mutual_information_bits=expected_hidden,
        hidden_information_residual_bits=hidden_residual,
        exact_hidden_fiber_countermodel_verified=exact,
        status=(
            "independent-central-features-can-hide-label-mutual-information"
            if exact
            else "hidden-fiber-countermodel-control-failure"
        ),
    )


def projector_resolution_scaling_record(
    n: int,
    maximum_support: int,
) -> ProjectorResolutionScalingRecord:
    if n < 20 or maximum_support < 2:
        raise ValueError("scaling records require n>=20 and support>=2")
    feature_count = len(fixed_point_free_cycle_types(maximum_support))
    count_identity = feature_count == exact_central_feature_count(maximum_support)
    log_feature_upper = feature_count * (
        math.log2(3.0) + maximum_support * math.log2(n)
    )
    log_partition_count = math.log2(partition_number(n))
    fixed = maximum_support <= 6
    below_boundary = maximum_support / (math.log(n) ** 2) < 0.1
    return ProjectorResolutionScalingRecord(
        n=n,
        maximum_moved_support=maximum_support,
        central_feature_count=feature_count,
        exact_feature_count_identity_verified=count_identity,
        log2_partition_count=log_partition_count,
        log2_feature_vector_count_upper=log_feature_upper,
        feature_log_capacity_over_sqrt_n=log_feature_upper / math.sqrt(n),
        support_is_fixed=fixed,
        support_is_below_log_squared_boundary=below_boundary,
        feature_capacity_can_resolve_plancherel_entropy_proved=False,
        status="low-support-central-feature-algebra-has-unresolved-projector-fibers",
    )


def run_free_probability_projector_resolution_boundary(
) -> FreeProbabilityProjectorResolutionReport:
    finite = [
        audit_central_feature_resolution(n, support)
        for n, support in (
            (6, 2),
            (6, 3),
            (8, 2),
            (8, 3),
            (10, 2),
            (10, 3),
            (12, 2),
            (12, 3),
            (15, 2),
            (15, 3),
            (20, 2),
            (20, 3),
        )
    ]
    countermodels = [
        hidden_fiber_countermodel(k, r)
        for k, r in ((1, 8), (2, 8), (4, 16), (8, 32))
    ]
    scaling = [
        projector_resolution_scaling_record(n, support)
        for n in (20, 50, 100, 1_000, 10_000)
        for support in (2, 3, 4)
    ]
    failures = sum(not row.feature_count_bound_verified for row in finite)
    failures += sum(
        not row.exact_hidden_fiber_countermodel_verified for row in countermodels
    )
    verified = failures == 0
    theorem = FreeProbabilityProjectorResolutionTheorem(
        class_sum_feature_bound="|range(F_s)|<=(3n^s)^T_s",
        exact_feature_count_identity="T_s=p(s)-1",
        plancherel_conditional_entropy_identity=(
            "H_Plancherel(lambda|F_s)=H_Plancherel(lambda)-H(F_s)"
        ),
        low_support_resolution_boundary=(
            "H_Plancherel(lambda|F_s_n)=Theta(sqrt(n)) for s_n=o((log n)^2)"
        ),
        constant_fraction_resolution_boundary=(
            "The same conclusion holds when limsup s_n/(ln n)^2 < 3/(8 pi^2)."
        ),
        logical_insufficiency_countermodel=(
            "A,B independent visible features and a shared hidden Z give I(A;B)=0 but I((A,Z);(B,Z))=H(Z)."
        ),
        natural_racah_mi_lower_bound_proved=False,
        status=(
            "fixed-degree-free-probability-insufficient-without-projector-resolution"
            if verified
            else "free-probability-projector-resolution-control-failure"
        ),
    )
    return FreeProbabilityProjectorResolutionReport(
        created_at=utc_now(),
        theorem_contract={
            "central_feature": (
                "integer class-sum eigenvalues for every nonidentity cycle type moving <=s points"
            ),
            "feature_count": "T_s=sum_(m=2)^s p_no_fixed_points(m)",
            "feature_count_identity": (
                "T_s=sum_(m=2)^s (p(m)-p(m-1))=p(s)-1"
            ),
            "class_size_bound": "|C|<=n^s",
            "plancherel_entropy_input": (
                "H_Plancherel(lambda)=Theta(sqrt(n)) from maximal irrep dimension asymptotics"
            ),
            "asymptotic_derivation": (
                "Hardy-Ramanujan gives log T_s=pi sqrt(2s/3)+O(log s); "
                "therefore H(F_s)=o(sqrt(n)) if s=o((ln n)^2), and more "
                "generally if limsup s/(ln n)^2<3/(8 pi^2)."
            ),
            "applicability_boundary": (
                "fixed-degree mixed moments control only the coarse F_s algebra, not individual partition projectors"
            ),
            "scope": (
                "logical insufficiency theorem; no lower bound on the natural Racah coupling"
            ),
        },
        theorem=theorem,
        finite_controls=finite,
        hidden_fiber_countermodels=countermodels,
        scaling_records=scaling,
        literature_boundary=[
            {
                "id": "biane-symmetric-groups-free-probability-1998",
                "url": "https://doi.org/10.1006/aima.1998.1745",
                "primary_source": True,
                "boundary": (
                    "Kronecker tensor-product components concentrate at the Plancherel/semicircle limit shape, but the theorem controls fixed moments and typical shapes, not fine pair-channel projector overlap."
                ),
            },
            {
                "id": "biane-approximate-factorization-2001",
                "url": "https://arxiv.org/abs/math/0006111",
                "primary_source": True,
                "boundary": (
                    "Approximate character factorization gives concentration of component shapes; it does not provide uniform degree growing to the partition-projector resolution scale."
                ),
            },
            {
                "id": "sniady-free-probability-large-symmetric-groups-2003",
                "url": "https://arxiv.org/abs/math/0304275",
                "primary_source": True,
                "boundary": (
                    "Fixed-order Jucys--Murphy cumulant expansions do not control the full central spectral sigma-algebra."
                ),
            },
            {
                "id": "jankowski-asymptotic-freeness-jucys-murphy-2012",
                "url": "https://arxiv.org/abs/1202.0888",
                "primary_source": True,
                "boundary": (
                    "The proved asymptotic freeness explains outer products induced to S_(2n), not the same-S_n Kronecker Racah associator studied here."
                ),
            },
        ],
        proof_obligations=[
            {
                "obligation": "prove_low_support_central_feature_cardinality_bound",
                "resolved": verified,
                "resolution": (
                    "Each central scalar is an integer in a polynomial interval and "
                    "T_s=p(s)-1 exactly by telescoping p(m)-p(m-1)."
                ),
            },
            {
                "obligation": "show_fixed_feature_independence_does_not_upper_bound_label_mi",
                "resolved": verified,
                "resolution": (
                    "The exact shared-hidden-label countermodel has product visible features and arbitrary hidden MI."
                ),
            },
            {
                "obligation": "extend_mixed_moment_control_to_projector_resolution_scale",
                "resolved": False,
                "resolution": (
                    "Need uniform character/Jucys estimates for support or polynomial degree at least comparable to the log-squared boundary, plus approximation error strong enough for entropy."
                ),
            },
            {
                "obligation": "control_information_inside_central_feature_fibers",
                "resolved": False,
                "resolution": (
                    "An alternative proof may bypass high-degree moments by showing natural recoupling is conditionally delocalized within every physically relevant fiber."
                ),
            },
        ],
        adversarial_audit=[
            {
                "objection": "Biane already proves Kronecker tensor products become Plancherel.",
                "resolved": True,
                "resolution": (
                    "That is a limit-shape statement for one decomposition. Fine labels can retain Theta(sqrt(n)) entropy inside the common limit shape."
                ),
            },
            {
                "objection": "Asymptotic freeness of Jucys--Murphy elements directly applies.",
                "resolved": True,
                "resolution": (
                    "The located theorem concerns outer products in S_(2n); even fixed-degree same-n freeness would still require projector-resolution control."
                ),
            },
            {
                "objection": "One exact real-valued moment can encode every partition.",
                "resolved": True,
                "resolution": (
                    "The relevant class-sum eigenvalues are integers with polynomial range at fixed moved support, so their joint range is explicitly bounded."
                ),
            },
            {
                "objection": (
                    "Support-three features distinguish almost every partition at the "
                    "small n accessible to exact computation."
                ),
                "resolved": True,
                "resolution": (
                    "This finite injectivity is transient: two integer coordinates have "
                    "only polynomial joint range, whereas p(n)=exp(Theta(sqrt(n)))."
                ),
            },
            {
                "objection": "Large unresolved entropy proves natural Racah MI survives.",
                "resolved": True,
                "resolution": (
                    "It does not. It only proves that coarse-feature independence cannot upper-bound the hidden conditional dependence."
                ),
            },
        ],
        headline_metrics={
            "central_feature_resolution_boundary_theorem_count": int(verified),
            "finite_feature_control_count": len(finite),
            "exact_feature_count_identity_control_count": sum(
                row.exact_feature_count_identity_verified for row in scaling
            ),
            "hidden_fiber_countermodel_count": len(countermodels),
            "finite_control_failure_count": failures,
            "fixed_degree_free_probability_suffices_for_label_mi_count": 0,
            "growing_degree_projector_approximation_theorem_count": 0,
            "natural_racah_mi_lower_bound_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "fixed_support_central_feature_count_bound_proved": verified,
            "sub_log_squared_support_leaves_plancherel_entropy_unresolved_proved": verified,
            "coarse_feature_independence_sufficient_for_label_independence": False,
            "cited_fixed_degree_free_probability_results_reach_projector_resolution": False,
            "natural_racah_mi_vanishes_proved": False,
            "natural_racah_mi_survives_proved": False,
            "classical_separation_proved": False,
            "algorithm_claim_allowed": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The cited fixed-degree asymptotics do not resolve fine partition projectors, and unresolved fibers can hide large dependence in principle."
            ),
        },
        status=(
            "free-probability-route-requires-growing-degree-projector-resolution"
            if verified
            else "free-probability-projector-resolution-control-failure"
        ),
        summary=(
            "Proved that fixed-support central asymptotics leave superlogarithmic "
            "partition entropy unresolved and cannot alone decide Racah label MI."
        ),
        falsifiers_triggered=[
            "Typical Plancherel limit shape does not identify a partition label.",
            "Fixed-degree moment factorization does not imply independence of the full central spectral labels.",
            "Outer-product Jucys--Murphy freeness is not a same-n Kronecker recoupling theorem.",
        ],
    )


def write_free_probability_projector_resolution_report(
    path: Path = REPORT_PATH,
) -> dict[str, Any]:
    payload = asdict(run_free_probability_projector_resolution_boundary())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    return payload


if __name__ == "__main__":
    result = write_free_probability_projector_resolution_report()
    print(json.dumps(result["headline_metrics"], indent=2, sort_keys=True))

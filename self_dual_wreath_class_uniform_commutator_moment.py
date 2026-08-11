"""Natural-source obstruction for class-uniform commutator targets.

The translated-parity family leaves the target commutator ``[p,q]`` while
sampling ``p`` uniformly by conjugacy class and ``q`` uniformly in the group.
For an irrep ``rho`` this gives the normalized target moment

    A_rho = (1 / (d_rho^2 k(G))) sum_C |chi_rho(C)|^2.

Low-dimensional representations can retain inverse-polynomial signal.  That
does not make the signal typical.  Under the Plancherel law on irreps, column
orthogonality gives the exact identity

    E_Plancherel A_rho = (1 / k(G)) sum_C 1 / |C|.

For ``S_n``, every nonidentity conjugacy class has size at least
``n(n-1)/2`` when ``n>=5``.  Therefore

    E_Plancherel A_rho
        <= 1 / p(n) + 2 / (n(n-1)),

and Markov's inequality bounds the Plancherel mass of any sector retaining a
specified target moment.  This is an exact natural-source no-go, not a worst-
case irrep bound: trivial/sign sectors have moment one, and the standard
representation has moment ``12/(pi^2 n)+o(1/n)`` but negligible Plancherel
mass.

An exhaustive character-table scan is also included.  It finds the standard
representation and its sign twist to be extremal among non-one-dimensional
irreps for every ``7<=n<=20``.  Small-degree exceptions at ``n=4`` and ties at
``n=6`` are retained deliberately.  No all-n extremality theorem is claimed.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from fractions import Fraction
from pathlib import Path
from typing import Any

from representation_obstruction import hook_length_dimension, integer_partitions
from research_registry import utc_now
from symmetric_character import conjugacy_class_size, symmetric_character


REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_class_uniform_commutator_moment.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-CLASS-UNIFORM-COMMUTATOR-MOMENT"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


Partition = tuple[int, ...]


@dataclass(frozen=True)
class IrrepClassMoment:
    partition: Partition
    conjugate_partition: Partition
    dimension: int
    class_second_moment_sum: int
    conjugacy_class_count: int
    exact_normalized_moment: str
    normalized_moment: float


@dataclass(frozen=True)
class ExtremalCharacterMomentControl:
    symmetric_group_degree: int
    conjugacy_class_count: int
    non_one_dimensional_irrep_count: int
    maximizing_partitions: tuple[Partition, ...]
    maximum_exact_moment: str
    maximum_moment: float
    standard_exact_moment: str
    standard_moment: float
    standard_and_sign_twist_are_only_maximizers: bool
    known_small_degree_exception_or_tie: bool
    exhaustive_finite_control_verified: bool
    status: str


@dataclass(frozen=True)
class PlancherelMomentControl:
    symmetric_group_degree: int
    group_order: int
    conjugacy_class_count: int
    smallest_nonidentity_class_size: int
    transposition_class_size: int
    exact_reciprocal_class_average: str
    reciprocal_class_average: float
    exact_direct_irrep_average: str | None
    column_orthogonality_identity_verified: bool | None
    exact_theorem_upper_bound: str
    theorem_upper_bound: float
    inverse_n_threshold_tail_bound: float
    class_size_lemma_verified: bool
    theorem_bound_verified: bool
    status: str


@dataclass(frozen=True)
class ClassUniformCommutatorTheorem:
    finite_group_moment_formula: str
    plancherel_average_identity: str
    symmetric_group_class_size_lemma: str
    symmetric_group_average_bound: str
    threshold_tail_bound: str
    standard_representation_asymptotic: str
    scope_limit: str
    arbitrary_finite_group_identity: bool
    all_n_symmetric_group_bound_from_degree_five: bool
    worst_case_irrep_bound_proved: bool
    standard_extremality_proved_for_all_n: bool
    natural_source_obstruction_verified: bool
    status: str


@dataclass(frozen=True)
class ClassUniformCommutatorMomentReport:
    created_at: str
    theorem_contract: dict[str, Any]
    extremal_controls: list[ExtremalCharacterMomentControl]
    plancherel_controls: list[PlancherelMomentControl]
    theorem: ClassUniformCommutatorTheorem
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, bool | str]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def conjugate_partition(partition: Partition) -> Partition:
    if not partition:
        return ()
    return tuple(
        sum(row >= column for row in partition)
        for column in range(1, partition[0] + 1)
    )


def irrep_class_moment(partition: Partition) -> IrrepClassMoment:
    """Return the exact class-uniform squared normalized character moment."""

    degree = sum(partition)
    if degree < 1 or tuple(sorted(partition, reverse=True)) != partition:
        raise ValueError("partition must be a nonempty integer partition")
    classes = integer_partitions(degree)
    dimension = hook_length_dimension(partition)
    numerator = sum(symmetric_character(partition, row) ** 2 for row in classes)
    exact = Fraction(numerator, dimension * dimension * len(classes))
    return IrrepClassMoment(
        partition=partition,
        conjugate_partition=conjugate_partition(partition),
        dimension=dimension,
        class_second_moment_sum=numerator,
        conjugacy_class_count=len(classes),
        exact_normalized_moment=str(exact),
        normalized_moment=float(exact),
    )


def extremal_character_moment_control(
    degree: int,
) -> ExtremalCharacterMomentControl:
    """Exhaustively maximize the moment, excluding trivial and sign irreps."""

    if degree < 3:
        raise ValueError("extremal control requires degree at least three")
    rows = [
        irrep_class_moment(partition)
        for partition in integer_partitions(degree)
        if hook_length_dimension(partition) > 1
    ]
    maximum = max(Fraction(row.exact_normalized_moment) for row in rows)
    maximizers = tuple(
        row.partition
        for row in rows
        if Fraction(row.exact_normalized_moment) == maximum
    )
    standard = irrep_class_moment((degree - 1, 1))
    expected = {(degree - 1, 1), conjugate_partition((degree - 1, 1))}
    standard_only = set(maximizers) == expected
    known_exception_or_tie = degree in {4, 6}
    verified = (
        all(0.0 <= row.normalized_moment <= 1.0 for row in rows)
        and (degree < 7 or standard_only)
        and (degree != 4 or (2, 2) in maximizers)
        and (degree != 6 or len(maximizers) == 4)
    )
    return ExtremalCharacterMomentControl(
        symmetric_group_degree=degree,
        conjugacy_class_count=len(integer_partitions(degree)),
        non_one_dimensional_irrep_count=len(rows),
        maximizing_partitions=maximizers,
        maximum_exact_moment=str(maximum),
        maximum_moment=float(maximum),
        standard_exact_moment=standard.exact_normalized_moment,
        standard_moment=standard.normalized_moment,
        standard_and_sign_twist_are_only_maximizers=standard_only,
        known_small_degree_exception_or_tie=known_exception_or_tie,
        exhaustive_finite_control_verified=verified,
        status=(
            "finite-standard-extremality-control"
            if standard_only
            else "finite-small-degree-exception-or-tie"
        ),
    )


def reciprocal_class_average(degree: int) -> Fraction:
    """Exact ``(1/p(n)) sum_C 1/|C|`` for ``S_n``."""

    if degree < 1:
        raise ValueError("degree must be positive")
    classes = integer_partitions(degree)
    return sum(
        (Fraction(1, conjugacy_class_size(row)) for row in classes),
        start=Fraction(0),
    ) / len(classes)


def direct_plancherel_moment_average(degree: int) -> Fraction:
    """Direct irrep-side average used to audit column orthogonality."""

    if degree < 1:
        raise ValueError("degree must be positive")
    classes = integer_partitions(degree)
    order = math.factorial(degree)
    total = Fraction(0)
    for partition in classes:
        dimension = hook_length_dimension(partition)
        moment = Fraction(irrep_class_moment(partition).exact_normalized_moment)
        total += Fraction(dimension * dimension, order) * moment
    return total


def plancherel_moment_control(
    degree: int,
    *,
    verify_irrep_side: bool = False,
) -> PlancherelMomentControl:
    if degree < 5:
        raise ValueError("the symmetric-group class-size theorem starts at n=5")
    classes = integer_partitions(degree)
    nonidentity_sizes = [
        conjugacy_class_size(row)
        for row in classes
        if row != (1,) * degree
    ]
    smallest = min(nonidentity_sizes)
    transpositions = degree * (degree - 1) // 2
    average = reciprocal_class_average(degree)
    direct = direct_plancherel_moment_average(degree) if verify_irrep_side else None
    identity_verified = direct == average if direct is not None else None
    bound = Fraction(1, len(classes)) + Fraction(2, degree * (degree - 1))
    class_lemma = smallest >= transpositions
    theorem_bound = average <= bound
    threshold_tail = min(1.0, float(average * degree))
    return PlancherelMomentControl(
        symmetric_group_degree=degree,
        group_order=math.factorial(degree),
        conjugacy_class_count=len(classes),
        smallest_nonidentity_class_size=smallest,
        transposition_class_size=transpositions,
        exact_reciprocal_class_average=str(average),
        reciprocal_class_average=float(average),
        exact_direct_irrep_average=str(direct) if direct is not None else None,
        column_orthogonality_identity_verified=identity_verified,
        exact_theorem_upper_bound=str(bound),
        theorem_upper_bound=float(bound),
        inverse_n_threshold_tail_bound=threshold_tail,
        class_size_lemma_verified=class_lemma,
        theorem_bound_verified=theorem_bound,
        status=(
            "plancherel-class-moment-obstruction-verified"
            if class_lemma and theorem_bound and identity_verified is not False
            else "plancherel-class-moment-certificate-failure"
        ),
    )


def class_uniform_commutator_theorem() -> ClassUniformCommutatorTheorem:
    return ClassUniformCommutatorTheorem(
        finite_group_moment_formula=(
            "A_rho=(1/(d_rho^2*k(G)))*sum_C |chi_rho(C)|^2"
        ),
        plancherel_average_identity=(
            "E_{rho~Plancherel} A_rho=(1/k(G))*sum_C 1/|C|"
        ),
        symmetric_group_class_size_lemma=(
            "For n>=5 every nonidentity S_n class has size at least n(n-1)/2"
        ),
        symmetric_group_average_bound=(
            "E_Plancherel A_rho <= 1/p(n)+2/(n(n-1))"
        ),
        threshold_tail_bound=(
            "Pr_Plancherel[A_rho>=tau] <= "
            "(1/p(n)+2/(n(n-1)))/tau"
        ),
        standard_representation_asymptotic="12/(pi^2*n)+o(1/n)",
        scope_limit=(
            "This controls natural Plancherel source mass, not adversarially "
            "postselected low-dimensional irreps or a non-Plancherel source law."
        ),
        arbitrary_finite_group_identity=True,
        all_n_symmetric_group_bound_from_degree_five=True,
        worst_case_irrep_bound_proved=False,
        standard_extremality_proved_for_all_n=False,
        natural_source_obstruction_verified=True,
        status="exact-plancherel-source-moment-no-go",
    )


def run_class_uniform_commutator_moment(
    maximum_extremal_degree: int = 20,
) -> ClassUniformCommutatorMomentReport:
    if maximum_extremal_degree < 7:
        raise ValueError("maximum extremal degree must be at least seven")
    extremal = [
        extremal_character_moment_control(degree)
        for degree in range(3, maximum_extremal_degree + 1)
    ]
    plancherel = [
        plancherel_moment_control(
            degree,
            verify_irrep_side=degree <= 10,
        )
        for degree in range(5, maximum_extremal_degree + 1)
    ]
    theorem = class_uniform_commutator_theorem()
    finite_verified = all(row.exhaustive_finite_control_verified for row in extremal)
    plancherel_verified = all(
        row.class_size_lemma_verified
        and row.theorem_bound_verified
        and row.column_orthogonality_identity_verified is not False
        for row in plancherel
    )
    natural_no_go = theorem.natural_source_obstruction_verified and plancherel_verified
    return ClassUniformCommutatorMomentReport(
        created_at=utc_now(),
        theorem_contract={
            "target_law": theorem.finite_group_moment_formula,
            "natural_source_identity": theorem.plancherel_average_identity,
            "symmetric_group_bound": theorem.symmetric_group_average_bound,
            "scope_limit": theorem.scope_limit,
        },
        extremal_controls=extremal,
        plancherel_controls=plancherel,
        theorem=theorem,
        proof_obligations=[
            {
                "obligation": "derive_exact_per_irrep_commutator_moment",
                "resolved": True,
                "resolution": (
                    "Schur averaging over q gives |chi_rho(p)|^2/d_rho^2, "
                    "and commuting-pair sampling makes p uniform by class."
                ),
            },
            {
                "obligation": "average_over_natural_irrep_source",
                "resolved": True,
                "resolution": (
                    "Plancherel weights cancel d_rho^2 and character-table "
                    "column orthogonality gives the reciprocal-class identity."
                ),
            },
            {
                "obligation": "bound_symmetric_group_natural_source_signal",
                "resolved": True,
                "resolution": (
                    "The identity class contributes 1/p(n); the minimum "
                    "nonidentity class-size theorem bounds every other term."
                ),
            },
            {
                "obligation": "prove_standard_irrep_is_worst_case_for_all_n",
                "resolved": False,
                "resolution": (
                    "Exhaustive data through the stored degree supports this from "
                    "n=7, but no all-n character inequality is known here."
                ),
            },
            {
                "obligation": "exclude_adversarial_low_dimensional_postselection",
                "resolved": False,
                "resolution": (
                    "A decoder may alter the source law; its postselection cost "
                    "must be charged before applying the Plancherel obstruction."
                ),
            },
        ],
        adversarial_audit=[
            {
                "objection": "The standard irrep's inverse-polynomial moment is typical.",
                "resolved": True,
                "resolution": (
                    "Its Plancherel mass is (n-1)^2/n!, while the exact natural "
                    "average obeys the reciprocal-class bound."
                ),
            },
            {
                "objection": "Finite extremal data proves an all-n inequality.",
                "resolved": True,
                "resolution": (
                    "The report marks global extremality false and preserves the "
                    "n=4 exception and n=6 ties."
                ),
            },
            {
                "objection": "A vanishing average rules out every irrep.",
                "resolved": True,
                "resolution": (
                    "False: trivial and sign moments equal one. The theorem bounds "
                    "their source mass, not their pointwise signal."
                ),
            },
            {
                "objection": "Postselection can expose a rare sector for free.",
                "resolved": False,
                "resolution": (
                    "Any such construction must supply and charge an efficient "
                    "non-Plancherel preparation or amplification mechanism."
                ),
            },
        ],
        headline_metrics={
            "exact_natural_source_no_go_theorem_count": int(natural_no_go),
            "maximum_exhaustive_extremal_degree": maximum_extremal_degree,
            "finite_extremal_control_failure_count": sum(
                not row.exhaustive_finite_control_verified for row in extremal
            ),
            "plancherel_control_failure_count": sum(
                not (
                    row.class_size_lemma_verified
                    and row.theorem_bound_verified
                    and row.column_orthogonality_identity_verified is not False
                )
                for row in plancherel
            ),
            "standard_extremal_degree_count_from_seven": sum(
                row.standard_and_sign_twist_are_only_maximizers
                for row in extremal
                if row.symmetric_group_degree >= 7
            ),
            "stored_degree_count_from_seven": sum(
                row.symmetric_group_degree >= 7 for row in extremal
            ),
            "largest_degree_reciprocal_class_average": (
                plancherel[-1].reciprocal_class_average
            ),
            "largest_degree_inverse_n_tail_bound": (
                plancherel[-1].inverse_n_threshold_tail_bound
            ),
            "all_n_standard_extremality_theorem_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "exact_per_irrep_moment_derived": natural_no_go,
            "natural_plancherel_source_signal_survives": False,
            "rare_low_dimensional_signal_exists": True,
            "rare_sector_preparation_is_free": False,
            "standard_irrep_globally_extremal": False,
            "worst_case_irrep_obstruction_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The commutator moment is suppressed on natural Plancherel source "
                "mass; exploiting rare sectors requires a separately costed source."
            ),
        },
        status=(
            "class-uniform-commutator-natural-source-falsified"
            if natural_no_go and finite_verified
            else "class-uniform-commutator-certificate-failure"
        ),
        summary=(
            "Converted a target-surviving commutator bias into an exact natural-"
            "source no-go while retaining adversarial postselection as the boundary."
        ),
        falsifiers_triggered=[
            "Inverse-polynomial signal in one low-dimensional irrep is not typical.",
            "Finite standard-irrep extremality is not an all-n theorem.",
            "Natural-source suppression does not rule out costed postselection.",
        ],
    )


def write_class_uniform_commutator_moment_report(
    path: Path = REPORT_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = (
        "EXP-CODE-SELF-DUAL-WREATH-CLASS-UNIFORM-COMMUTATOR-MOMENT"
    ),
    registry_candidate_id: str = "CODE-COSET-COLLECTIVE",
    registry_result_id: str = "",
    **kwargs: Any,
) -> dict[str, Any]:
    path = path
    output_path = path
    for _k in ("write_registry", "registry_experiment_id", "registry_candidate_id", "registry_result_id"):
        kwargs.pop(_k, None)
    maximum_extremal_degree = kwargs.get("maximum_extremal_degree", 20)
    report = asdict(run_class_uniform_commutator_moment(maximum_extremal_degree))
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    if write_registry:
        _res_payload = report if "report" in locals() else (payload if "payload" in locals() else (result if "result" in locals() else output))
        from research_registry import (
            ExperimentResultRecord,
            NegativeResultRecord,
            upsert_experiment_result,
            upsert_negative_result,
        )

        upsert_negative_result(
            NegativeResultRecord(
                id="NEG-SELF-DUAL-WREATH-CLASS-UNIFORM-COMMUTATOR-MOMENT",
                source=registry_experiment_id,
                claim=(
                    "Initial negative claim for EXP-CODE-SELF-DUAL-WREATH-CLASS-UNIFORM-COMMUTATOR-MOMENT."
                ),
                reason_invalid=(
                    "Falsified or refined by exact theorem evaluation."
                ),
                lesson=(
                    "Lesson from exact theorem analysis for EXP-CODE-SELF-DUAL-WREATH-CLASS-UNIFORM-COMMUTATOR-MOMENT."
                ),
                applies_to=[
                    registry_candidate_id,
                    registry_experiment_id,
                    "PO-MEASUREMENT",
                ],
                evidence=_res_payload.get("headline_metrics", {}),
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
                created_at=_res_payload.get("created_at", ""),
                status=_res_payload.get("status", "completed"),
                summary=_res_payload.get("summary", ""),
                metrics=_res_payload.get("headline_metrics", {}),
                falsifiers_triggered=_res_payload.get("falsifiers_triggered", []),
                artifacts={
                    "self_dual_wreath_class_uniform_commutator_moment": str(path)
                },
            )
        )

    return report


if __name__ == "__main__":
    result = write_class_uniform_commutator_moment_report()
    print(json.dumps(result["headline_metrics"], indent=2, sort_keys=True))

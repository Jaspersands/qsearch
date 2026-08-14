"""All-n proper-multiplicity theorem for hidden-involution support tests.

Let ``G=S_n``, let ``C`` be the fixed-point-free involution class of size
``M=(n-1)!!``, and let ``U_g`` simultaneously conjugate ``k`` regular basis
registers.  Write ``Pi_nu`` for the diagonal-action isotypic projector.  For a
conjugacy class ``K`` of size ``s_K`` and representative ``g_K``, define

    z_K = |{h in C : g_K h is conjugate to g_K}|.

The null and class-mixture probabilities of the diagonal irrep label are

    p_nu = d_nu/|G| sum_K chi_nu(K) / s_K^(k-1),

    q_nu = d_nu/|G| sum_K chi_nu(K) / s_K^(k-1)
             [1 + (2^k-1) z_K/M].                       (1)

The proof is a fixed-point count.  ``Tr(U_g)=|C_G(g)|=|G|/s_K``.  Moreover

    Tr[U_g R_h] = |G|/s_K  if g h is conjugate to g,
                  0        otherwise.

Equation (1) follows after taking tensor powers and averaging over ``h``.

Character bounds give a uniform total-variation estimate.  Since
``|chi_nu(K)|<=d_nu`` and ``sum_nu d_nu^2=|G|``, if ``s_min`` is the smallest
nonidentity class size and ``p(n)`` the partition number, then

    TV(p,q) <= (2^k-1)(p(n)-1)/(2 s_min^(k-1)).           (2)

For ``n>=6``, ``s_min>=n(n-1)/2>=n^2/3``, ``p(n)<=2^(n-1)``, and
``M<=n^(n/2)``.  At ``k=ceil(log2(4M))`` one has ``k>=n`` and ``2^k<=8M``;
therefore

    TV(p,q) <= 4/n^((n-2)/2) <= 1/9.                    (3)

Now let ``T=supp(A_k)`` be the information-theoretic support-span test.
It accepts the alternative perfectly and has null acceptance at most
``M/2^k<=1/4``.  If every diagonal isotypic block of ``T`` were either zero
or the whole block, accepting the occupied irrep labels would give
``TV(p,q)>=3/4``, contradicting (3).  Hence at least one isotypic sector has
a proper nonzero multiplicity-support projector for every even ``n>=6``.

This upgrades the previous ``S_3/S_4`` finite witness to an all-n theorem.
It rules out every support compiler built only from diagonal group actions or
whole isotypic labels.  It does not rule out an efficient commutant-side,
recoupling, association-scheme, or fused multiplicity-support transform.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from fractions import Fraction
from pathlib import Path
from typing import Any

from coset_hidden_involution_binary_decision_reduction import (
    compose_permutations,
    inverse_permutation,
    involution_class_size,
    involution_conjugacy_class,
    symmetric_group,
)
from coset_hidden_involution_multiplicity_support_obstruction import permutation_cycle_type
from representation_obstruction import hook_length_dimension, integer_partitions
from research_registry import utc_now
from symmetric_character import (
    conjugacy_class_size as permutation_class_size,
    symmetric_character,
)


REPORT_PATH = Path(
    "research/representation/"
    "coset_hidden_involution_isotypic_support_no_go.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-COSET-HIDDEN-INVOLUTION-ISOTYPIC-SUPPORT-NO-GO"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"

Partition = tuple[int, ...]
Permutation = tuple[int, ...]


@dataclass(frozen=True)
class IsotypicLawFiniteControl:
    n: int
    transposition_count: int
    copy_count: int
    conjugacy_class_size: int
    conjugacy_class_count: int
    nonzero_fixed_point_class_count: int
    null_probability_sum: float
    alternative_probability_sum: float
    exact_isotypic_total_variation: float
    direct_fixed_point_total_variation: float
    exact_direct_law_residual: float
    character_bound_total_variation_upper_bound: float
    character_bound_respected: bool
    finite_control_verified: bool
    status: str


@dataclass(frozen=True)
class IsotypicSupportScalingRecord:
    n: int
    conjugacy_class_size: int
    copy_count: int
    partition_count_upper_bound: int
    minimum_nonidentity_class_size_lower_bound: int
    class_count_total_variation_upper_bound: float
    elementary_total_variation_upper_bound: float
    support_test_null_acceptance_upper_bound: float
    support_test_alternative_acceptance: float
    whole_isotypic_support_required_total_variation: float
    proper_multiplicity_support_forced: bool
    diagonal_group_algebra_support_compiler_possible: bool
    commutant_side_support_compiler_ruled_out: bool
    status: str


@dataclass(frozen=True)
class IsotypicSupportNoGoTheorem:
    fixed_point_trace_identity: str
    exact_isotypic_law: str
    character_total_variation_bound: str
    symmetric_group_uniform_bound: str
    proper_support_contradiction: str
    compiler_consequence: str
    scope_limit: str
    exact_isotypic_law_proved: bool
    all_n_total_variation_bound_proved: bool
    all_n_proper_multiplicity_support_proved: bool
    diagonal_group_action_compiler_refuted: bool
    commutant_side_compiler_refuted: bool
    arbitrary_circuit_lower_bound_proved: bool
    theorem_verified: bool
    status: str


@dataclass(frozen=True)
class IsotypicSupportNoGoReport:
    created_at: str
    primary_literature: list[dict[str, str]]
    theorem_contract: dict[str, Any]
    finite_controls: list[IsotypicLawFiniteControl]
    scaling_records: list[IsotypicSupportScalingRecord]
    theorem: IsotypicSupportNoGoTheorem
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def permutation_of_cycle_type(cycle_type: Partition) -> Permutation:
    if not cycle_type or any(length < 1 for length in cycle_type):
        raise ValueError("cycle_type must be a nonempty integer partition")
    degree = sum(cycle_type)
    permutation = list(range(degree))
    offset = 0
    for length in cycle_type:
        cycle = list(range(offset, offset + length))
        for source, target in zip(cycle, cycle[1:] + cycle[:1]):
            permutation[source] = target
        offset += length
    return tuple(permutation)


def fixed_point_class_count(
    n: int,
    transposition_count: int,
    cycle_type: Partition,
) -> int:
    """Return ``z_K=|{h in C:g_K h~g_K}|`` exactly."""

    if sum(cycle_type) != n:
        raise ValueError("cycle type has the wrong degree")
    representative = permutation_of_cycle_type(cycle_type)
    return sum(
        permutation_cycle_type(
            compose_permutations(representative, hidden)
        )
        == cycle_type
        for hidden in involution_conjugacy_class(n, transposition_count)
    )


def diagonal_isotypic_label_laws(
    n: int,
    transposition_count: int,
    copy_count: int,
) -> tuple[
    tuple[tuple[Partition, Fraction, Fraction], ...],
    dict[Partition, int],
]:
    if copy_count < 1:
        raise ValueError("copy_count must be positive")
    order = math.factorial(n)
    hidden_size = involution_class_size(n, transposition_count)
    cycle_types = integer_partitions(n)
    fixed_counts = {
        cycle_type: fixed_point_class_count(
            n, transposition_count, cycle_type
        )
        for cycle_type in cycle_types
    }
    class_sizes = {
        cycle_type: permutation_class_size(cycle_type)
        for cycle_type in cycle_types
    }
    laws = []
    for partition in integer_partitions(n):
        dimension = hook_length_dimension(partition)
        null = Fraction(dimension, order) * sum(
            Fraction(
                symmetric_character(partition, cycle_type),
                class_sizes[cycle_type] ** (copy_count - 1),
            )
            for cycle_type in cycle_types
        )
        alternative = Fraction(dimension, order) * sum(
            Fraction(
                symmetric_character(partition, cycle_type),
                class_sizes[cycle_type] ** (copy_count - 1),
            )
            * (
                1
                + Fraction(
                    ((1 << copy_count) - 1)
                    * fixed_counts[cycle_type],
                    hidden_size,
                )
            )
            for cycle_type in cycle_types
        )
        if null < 0 or alternative < 0:
            raise ArithmeticError("isotypic label law became negative")
        laws.append((partition, null, alternative))
    if sum(row[1] for row in laws) != 1:
        raise ArithmeticError("null isotypic law failed normalization")
    if sum(row[2] for row in laws) != 1:
        raise ArithmeticError("alternative isotypic law failed normalization")
    return tuple(laws), fixed_counts


def isotypic_total_variation(
    n: int,
    transposition_count: int,
    copy_count: int,
) -> Fraction:
    laws, _ = diagonal_isotypic_label_laws(
        n, transposition_count, copy_count
    )
    return sum(abs(alternative - null) for _, null, alternative in laws) / 2


def direct_fixed_point_isotypic_label_laws(
    n: int,
    transposition_count: int,
    copy_count: int,
) -> tuple[tuple[Partition, Fraction, Fraction], ...]:
    """Enumerate the defining fixed-point traces without class grouping."""

    if copy_count < 1:
        raise ValueError("copy_count must be positive")
    group = symmetric_group(n)
    order = len(group)
    hidden_class = involution_conjugacy_class(n, transposition_count)
    cycle_types = {element: permutation_cycle_type(element) for element in group}
    fixed_counts: dict[Permutation, int] = {}
    twisted_counts: dict[tuple[Permutation, Permutation], int] = {}
    for conjugator in group:
        inverse = inverse_permutation(conjugator)
        fixed_counts[conjugator] = sum(
            compose_permutations(
                compose_permutations(conjugator, basis), inverse
            )
            == basis
            for basis in group
        )
        for hidden in hidden_class:
            twisted_counts[(conjugator, hidden)] = sum(
                compose_permutations(
                    compose_permutations(
                        conjugator,
                        compose_permutations(basis, hidden),
                    ),
                    inverse,
                )
                == basis
                for basis in group
            )

    laws = []
    for partition in integer_partitions(n):
        dimension = hook_length_dimension(partition)
        null = Fraction(dimension, order) * sum(
            symmetric_character(partition, cycle_types[conjugator])
            * Fraction(fixed_counts[conjugator], order) ** copy_count
            for conjugator in group
        )
        alternative = Fraction(dimension, order) * sum(
            symmetric_character(partition, cycle_types[conjugator])
            * sum(
                Fraction(
                    fixed_counts[conjugator]
                    + twisted_counts[(conjugator, hidden)],
                    order,
                )
                ** copy_count
                for hidden in hidden_class
            )
            / len(hidden_class)
            for conjugator in group
        )
        laws.append((partition, null, alternative))
    if sum(row[1] for row in laws) != 1 or sum(row[2] for row in laws) != 1:
        raise ArithmeticError("direct fixed-point law failed normalization")
    return tuple(laws)


def character_total_variation_upper_bound(
    n: int,
    transposition_count: int,
    copy_count: int,
) -> Fraction:
    """Return the exact class-sum upper bound before coarse inequalities."""

    if copy_count < 1:
        raise ValueError("copy_count must be positive")
    hidden_size = involution_class_size(n, transposition_count)
    _, fixed_counts = diagonal_isotypic_label_laws(
        n, transposition_count, copy_count
    )
    identity_type = (1,) * n
    return Fraction((1 << copy_count) - 1, 2 * hidden_size) * sum(
        Fraction(
            fixed_count,
            permutation_class_size(cycle_type) ** (copy_count - 1),
        )
        for cycle_type, fixed_count in fixed_counts.items()
        if cycle_type != identity_type
    )


def fixed_point_free_threshold_copy_count(n: int) -> int:
    if n < 2 or n % 2:
        raise ValueError("n must be positive and even")
    size = involution_class_size(n, n // 2)
    return (4 * size - 1).bit_length()


def elementary_isotypic_tv_upper_bound(n: int) -> Fraction:
    """Return ``4/n^((n-2)/2)`` for even ``n>=6``."""

    if n < 6 or n % 2:
        raise ValueError("n must be even and at least six")
    return Fraction(4, n ** ((n - 2) // 2))


def class_count_isotypic_tv_upper_bound(n: int) -> Fraction:
    """Apply ``p(n)<=2^(n-1)`` and ``s_min>=n(n-1)/2`` at threshold."""

    if n < 6 or n % 2:
        raise ValueError("n must be even and at least six")
    copies = fixed_point_free_threshold_copy_count(n)
    partition_count_upper = 1 << (n - 1)
    return Fraction(
        ((1 << copies) - 1) * (partition_count_upper - 1),
        2 * (n * (n - 1) // 2) ** (copies - 1),
    )


def audit_isotypic_law_control(
    n: int,
    transposition_count: int,
    copy_count: int,
) -> IsotypicLawFiniteControl:
    laws, fixed_counts = diagonal_isotypic_label_laws(
        n, transposition_count, copy_count
    )
    exact_tv = sum(
        abs(alternative - null) for _, null, alternative in laws
    ) / 2
    direct_laws = direct_fixed_point_isotypic_label_laws(
        n, transposition_count, copy_count
    )
    direct_tv = sum(
        abs(alternative - null)
        for _, null, alternative in direct_laws
    ) / 2
    direct_residual = max(
        abs(float(exact_null - direct_null))
        + abs(float(exact_alternative - direct_alternative))
        for (
            exact_partition,
            exact_null,
            exact_alternative,
        ), (
            direct_partition,
            direct_null,
            direct_alternative,
        ) in zip(laws, direct_laws)
        if exact_partition == direct_partition
    )
    character_bound = character_total_variation_upper_bound(
        n, transposition_count, copy_count
    )
    verified = bool(
        sum(row[1] for row in laws) == 1
        and sum(row[2] for row in laws) == 1
        and exact_tv <= character_bound
        and direct_residual <= 1e-12
        and exact_tv == direct_tv
    )
    return IsotypicLawFiniteControl(
        n=n,
        transposition_count=transposition_count,
        copy_count=copy_count,
        conjugacy_class_size=involution_class_size(n, transposition_count),
        conjugacy_class_count=len(integer_partitions(n)),
        nonzero_fixed_point_class_count=sum(
            fixed_count > 0 for fixed_count in fixed_counts.values()
        ),
        null_probability_sum=float(sum(row[1] for row in laws)),
        alternative_probability_sum=float(sum(row[2] for row in laws)),
        exact_isotypic_total_variation=float(exact_tv),
        direct_fixed_point_total_variation=float(direct_tv),
        exact_direct_law_residual=direct_residual,
        character_bound_total_variation_upper_bound=float(character_bound),
        character_bound_respected=exact_tv <= character_bound,
        finite_control_verified=verified,
        status=(
            "exact-isotypic-law-and-fixed-point-formula-verified"
            if verified
            else "isotypic-law-control-failure"
        ),
    )


def isotypic_support_scaling_record(n: int) -> IsotypicSupportScalingRecord:
    if n < 6 or n % 2:
        raise ValueError("n must be even and at least six")
    size = involution_class_size(n, n // 2)
    copies = fixed_point_free_threshold_copy_count(n)
    partition_count_upper = 1 << (n - 1)
    class_bound = class_count_isotypic_tv_upper_bound(n)
    elementary_bound = elementary_isotypic_tv_upper_bound(n)
    null_acceptance = Fraction(size, 1 << copies)
    required_tv = 1 - null_acceptance
    proper = bool(
        class_bound <= elementary_bound
        and elementary_bound <= Fraction(1, 9)
        and required_tv >= Fraction(3, 4)
    )
    return IsotypicSupportScalingRecord(
        n=n,
        conjugacy_class_size=size,
        copy_count=copies,
        partition_count_upper_bound=partition_count_upper,
        minimum_nonidentity_class_size_lower_bound=n * (n - 1) // 2,
        class_count_total_variation_upper_bound=float(class_bound),
        elementary_total_variation_upper_bound=float(elementary_bound),
        support_test_null_acceptance_upper_bound=float(null_acceptance),
        support_test_alternative_acceptance=1.0,
        whole_isotypic_support_required_total_variation=float(required_tv),
        proper_multiplicity_support_forced=proper,
        diagonal_group_algebra_support_compiler_possible=False,
        commutant_side_support_compiler_ruled_out=False,
        status=(
            "all-n-proper-multiplicity-support-forced-commutant-route-open"
            if proper
            else "isotypic-support-scaling-proof-failure"
        ),
    )


def build_isotypic_support_no_go_report(
    *,
    finite_specs: tuple[tuple[int, int, int], ...] = (
        (3, 1, 1),
        (3, 1, 2),
        (3, 1, 3),
        (4, 2, 2),
    ),
    scaling_n_values: tuple[int, ...] = (6, 8, 16, 32, 64, 128),
) -> IsotypicSupportNoGoReport:
    controls = [
        audit_isotypic_law_control(n, transpositions, copies)
        for n, transpositions, copies in finite_specs
    ]
    scaling = [isotypic_support_scaling_record(n) for n in scaling_n_values]
    finite_verified = all(row.finite_control_verified for row in controls)
    all_n_verified = all(row.proper_multiplicity_support_forced for row in scaling)
    verified = finite_verified and all_n_verified
    theorem = IsotypicSupportNoGoTheorem(
        fixed_point_trace_identity=(
            "Tr(U_g)=|G|/|g^G| and Tr(U_g R_h) equals the same value iff "
            "gh is conjugate to g, otherwise zero."
        ),
        exact_isotypic_law=(
            "p_nu=d_nu/|G| sum_K chi_nu(K)/s_K^(k-1), with the alternative "
            "summand multiplied by 1+(2^k-1)z_K/M."
        ),
        character_total_variation_bound=(
            "TV(p,q)<=(2^k-1)(p(n)-1)/(2 s_min^(k-1))."
        ),
        symmetric_group_uniform_bound=(
            "For fixed-point-free S_n, even n>=6 and k=ceil(log2(4M)), "
            "TV(p,q)<=4/n^((n-2)/2)<=1/9."
        ),
        proper_support_contradiction=(
            "A union of whole isotypic sectors with alternative acceptance one "
            "and null acceptance at most 1/4 would force label TV at least 3/4; "
            "therefore some support block is proper nonzero."
        ),
        compiler_consequence=(
            "Diagonal S_n actions, subgroup actions inside the same represented "
            "group algebra, and whole-isotypic GPE cannot compile the support test."
        ),
        scope_limit=(
            "No lower bound is proved for commutant-side recoupling, copy "
            "permutations, association-scheme transforms, fused multiplicity "
            "support circuits, or arbitrary quantum algorithms."
        ),
        exact_isotypic_law_proved=True,
        all_n_total_variation_bound_proved=all_n_verified,
        all_n_proper_multiplicity_support_proved=all_n_verified,
        diagonal_group_action_compiler_refuted=all_n_verified,
        commutant_side_compiler_refuted=False,
        arbitrary_circuit_lower_bound_proved=False,
        theorem_verified=verified,
        status=(
            "all-n-diagonal-isotypic-support-compiler-refuted-commutant-route-open"
            if verified
            else "isotypic-support-no-go-control-failure"
        ),
    )
    metrics: dict[str, int | float] = {
        "finite_control_count": len(controls),
        "finite_control_failure_count": sum(
            not row.finite_control_verified for row in controls
        ),
        "exact_isotypic_law_theorem_count": 1,
        "all_n_isotypic_tv_bound_theorem_count": 1 if all_n_verified else 0,
        "all_n_proper_multiplicity_support_theorem_count": 1 if all_n_verified else 0,
        "maximum_scaling_elementary_isotypic_tv_bound": max(
            row.elementary_total_variation_upper_bound for row in scaling
        ),
        "minimum_whole_isotypic_required_tv": min(
            row.whole_isotypic_support_required_total_variation for row in scaling
        ),
        "commutant_side_compiler_no_go_count": 0,
        "arbitrary_circuit_lower_bound_count": 0,
        "new_quantum_algorithm_count": 0,
    }
    return IsotypicSupportNoGoReport(
        created_at=utc_now(),
        primary_literature=[
            {
                "id": "HAYASHI-KAWACHI-KOBAYASHI-2006-HSP-SAMPLE-COMPLEXITY",
                "title": "Quantum Measurements for Hidden Subgroup Problems with Optimal Sample Complexity",
                "url": "https://arxiv.org/abs/quant-ph/0604174",
                "scope": (
                    "Provides the support-span test; this theorem proves that its "
                    "fixed-point-free S_n support cannot be a union of diagonal "
                    "isotypic sectors at the useful copy threshold."
                ),
            }
        ],
        theorem_contract={
            "family": (
                "Fixed-point-free involutions in S_n for every even n>=6."
            ),
            "copy_threshold": "k=ceil(log2(4(n-1)!!)).",
            "measurement_under_test": (
                "Measure only the simultaneous-conjugation S_n irrep label and "
                "classically decide whether that whole isotypic sector belongs "
                "to the support span."
            ),
            "outside_scope": (
                "Measurements resolving or coherently transforming the global "
                "multiplicity space inside an isotypic sector."
            ),
        },
        finite_controls=controls,
        scaling_records=scaling,
        theorem=theorem,
        proof_obligations=[
            {
                "id": "PO-COSET-HIDDEN-INVOLUTION-COMMUTANT-SUPPORT-BASIS",
                "statement": (
                    "Construct or obstruct a uniform polynomial basis/projector "
                    "for the proper multiplicity support inside typical sectors."
                ),
                "resolved": False,
            },
            {
                "id": "PO-COSET-HIDDEN-INVOLUTION-RELATIVE-SPECTRAL-GAP",
                "statement": (
                    "Bound the source-conditioned relative spectrum after the "
                    "best legal multiplicity-side normalization."
                ),
                "resolved": False,
            },
            {
                "id": "PO-COSET-HIDDEN-INVOLUTION-STRUCTURED-INPUT-REDUCTION",
                "statement": (
                    "Supply a natural graph/code input reduction and classical "
                    "comparison before interpreting binary detection as a speedup."
                ),
                "resolved": False,
            },
        ],
        adversarial_audit=[
            {
                "challenge": "The finite proper-support witnesses may disappear with n.",
                "answer": (
                    "False for fixed-point-free S_n at threshold: the all-n "
                    "isotypic TV contradiction forces a proper block."
                ),
                "resolved": True,
            },
            {
                "challenge": "A diagonal S_n irrep label can compile the support test.",
                "answer": (
                    "False: whole-sector support would need TV at least 3/4, "
                    "whereas the exact character law is bounded by 1/9."
                ),
                "resolved": True,
            },
            {
                "challenge": "Proper support proves computational hardness.",
                "answer": (
                    "False. It demands a multiplicity-side primitive but gives no "
                    "lower bound on such a transform."
                ),
                "resolved": True,
            },
        ],
        headline_metrics=metrics,
        claim_gate={
            "all_n_proper_multiplicity_support_proved": all_n_verified,
            "diagonal_irrep_label_support_compiler_refuted": all_n_verified,
            "diagonal_group_algebra_support_compiler_refuted": all_n_verified,
            "commutant_side_support_compiler_constructed": False,
            "commutant_side_support_compiler_refuted": False,
            "efficient_binary_hidden_involution_algorithm_constructed": False,
            "classical_separation_proved": False,
            "arbitrary_quantum_lower_bound_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The support test provably needs a proper multiplicity-space "
                "projector. Whether that projector has an efficient structured "
                "compiler remains the central open question."
            ),
        },
        status=theorem.status,
        summary=(
            "Derived the exact diagonal-isotypic binary law and proved an all-n "
            "1/9 total-variation bound at the support-test threshold. This "
            "forces proper multiplicity support for every fixed-point-free S_n "
            "family with even n>=6, while leaving commutant-side compilation open."
        ),
        falsifiers_triggered=[
            "Finite proper multiplicity support is no longer merely finite evidence for fixed-point-free S_n.",
            "Whole diagonal-isotypic labels cannot implement the logarithmic-copy support-span test.",
            "Any surviving structured compiler must act nontrivially inside global multiplicity spaces.",
            "Proper multiplicity support alone is not a circuit lower bound or a quantum speedup.",
        ],
    )


def write_isotypic_support_no_go_report(
    output_path: Path = REPORT_PATH,
    **kwargs: Any,
) -> dict[str, Any]:
    payload = asdict(build_isotypic_support_no_go_report(**kwargs))
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return payload


if __name__ == "__main__":
    report = write_isotypic_support_no_go_report()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))

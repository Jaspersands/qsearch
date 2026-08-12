"""Fourth-moment threshold theorem for binary hidden-involution detection.

This module closes the information-theoretic gap left by
``coset_hidden_involution_binary_decision_reduction.py``.  Let ``C`` be a
conjugacy class of ``M >= 2`` nonidentity involutions in a finite group and put

    L_k = |G|^k (M^-1 sum_(h in C) rho_h^tensor k),
    X_k = L_k - I.                                      (1)

With normalized trace ``tau=Tr/|G|^k``, the previous second-moment identity is

    v_k = tau(X_k^2) = (2^k-1)/M.                       (2)

The fourth moment has an exact relation-count formula.  Define

    c = |C intersect C_G(a)|                            (3)
    T = |{(a,b,c) in C^3 : abc=e}|,
    E = |{(a,b,c,d) in C^4 : abcd=e}|.

The first quantity is independent of ``a`` because ``C`` is a conjugacy
class.  Put

    A=M(M-c), B=M(M-1), Q=M(c-1),
    F=E-(2A+2B+Q+M).                                   (4)

Here ``F`` counts four-product relations with no repeated pair.  For

    P2 = 2^k-1,
    P3f = 3^k-2^k,
    P3p = 3^k-2*2^k+1,
    P4p = 4^k-2*2^k+1,
    P4t = 4^k-3*2^k+2,
    P8 = 8^k-4*4^k+6*2^k-3,                            (5)

the exact identity is

    tau(X_k^4) = M^-4 [
        F P2 + 2A P3f + A P3p + (2B+Q) P4p
        + 6T P4t + M P8].                              (6)

The proof classifies identity subwords of four ordered nonidentity
involutions.  With no repeated pair, only a lone triple or the full word can
be identity.  With one repeated pair, the only covering possibilities are a
crossing pair plus the full word, or that pair plus the two corresponding
triple identities.  Two repeated pairs give the three pairings, with the
alternating pairing split by commutation.  Three equal elements do not cover
the fourth factor, and four equal elements give all even subsets.  Elementary
inclusion--exclusion gives the six polynomials in (5).

Since ``E<=M^3``, ``T<=M^2``, and every other relation count in (6) is at most
``M^2``, at ``k=ceil(log2 M)`` equation (6) is less than 55.  Also
``v_k>=1/2``.  The normalized Schatten interpolation inequality

    tau|X| >= tau(X^2)^(3/2) / tau(X^4)^(1/2)           (7)

therefore proves

    D(rho_C^k,rho_0^k)
      >= 1 / (2^(5/2) sqrt(55)) > 0.023.                (8)

Together with the chi-square upper bound, binary detection has copy
complexity ``Theta(log M)`` information-theoretically, uniformly over every
finite-group conjugacy class of nonidentity involutions.  Conjugation
symmetrization makes the alternative acceptance probability the same for
every hidden ``h`` in ``C``.

This is not an efficient algorithm.  The Helstrom effect may require an
exponentially hard sign transform on diagonal-action multiplicity spaces.
The result changes the research bottleneck from "does threshold information
exist?" to "can the invariant threshold sign be compiled, or dequantized, on
a natural family?"  It proves no graph-isomorphism transfer, classical lower
bound, or quantum speedup.
"""

from __future__ import annotations

import itertools
import json
import math
from dataclasses import asdict, dataclass
from fractions import Fraction
from pathlib import Path
from typing import Any

import numpy as np

from coset_hidden_involution_binary_decision_reduction import (
    Permutation,
    compose_permutations,
    dense_binary_states,
    involution_class_size,
    involution_conjugacy_class,
)
from research_registry import utc_now


REPORT_PATH = Path(
    "research/representation/"
    "coset_hidden_involution_fourth_moment_threshold.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-COSET-HIDDEN-INVOLUTION-FOURTH-MOMENT-THRESHOLD"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"
UNIVERSAL_FOURTH_MOMENT_BOUND = 55.0
UNIVERSAL_TRACE_DISTANCE_CONSTANT = 1.0 / (
    (2.0 ** 2.5) * math.sqrt(UNIVERSAL_FOURTH_MOMENT_BOUND)
)


@dataclass(frozen=True)
class InvolutionClassRelationStatistics:
    n: int
    transposition_count: int
    conjugacy_class_size: int
    commuting_class_neighbors_per_element: int
    ordered_triple_identity_count: int
    ordered_four_identity_count: int
    noncommuting_ordered_pair_count: int
    distinct_ordered_pair_count: int
    commuting_distinct_ordered_pair_count: int
    full_relation_without_repeated_pair_count: int
    relation_counts_valid: bool


@dataclass(frozen=True)
class FourthMomentFiniteControl:
    n: int
    transposition_count: int
    copy_count: int
    conjugacy_class_size: int
    exact_second_moment: float
    exact_relation_formula_fourth_moment: float
    direct_identity_pattern_fourth_moment: float
    relation_formula_pattern_residual: float
    dense_matrix_fourth_moment: float | None
    dense_matrix_residual: float | None
    interpolation_trace_distance_lower_bound: float
    dense_helstrom_trace_distance: float | None
    interpolation_bound_respected: bool
    finite_control_verified: bool
    status: str


@dataclass(frozen=True)
class FourthMomentThresholdScalingRecord:
    n: int
    conjugacy_class_size: int
    threshold_copy_count: int
    threshold_second_moment: float
    relation_count_fourth_moment_upper_bound: float
    coarse_universal_fourth_moment_bound: float
    certified_trace_distance_lower_bound: float
    coarse_universal_trace_distance_lower_bound: float
    certified_equal_prior_bayes_advantage: float
    logarithmic_copy_information_sufficiency_proved: bool
    polynomial_block_sign_compiler_known: bool
    status: str


@dataclass(frozen=True)
class HiddenInvolutionFourthMomentTheorem:
    exact_fourth_moment_identity: str
    universal_relation_bounds: str
    interpolation_inequality: str
    threshold_conclusion: str
    exact_relation_classification_proved: bool
    fourth_moment_constant_at_log_class_size_proved: bool
    constant_trace_distance_at_log_class_size_proved: bool
    theta_log_class_copy_complexity_proved: bool
    efficient_helstrom_compiler_constructed: bool
    theorem_verified: bool
    status: str


@dataclass(frozen=True)
class HiddenInvolutionFourthMomentReport:
    created_at: str
    primary_literature: list[dict[str, str]]
    theorem_contract: dict[str, Any]
    finite_controls: list[FourthMomentFiniteControl]
    scaling_records: list[FourthMomentThresholdScalingRecord]
    theorem: HiddenInvolutionFourthMomentTheorem
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _identity(n: int) -> Permutation:
    return tuple(range(n))


def _ordered_product(elements: tuple[Permutation, ...]) -> Permutation:
    if not elements:
        raise ValueError("ordered product needs a degree witness")
    product = _identity(len(elements[0]))
    for element in elements:
        product = compose_permutations(product, element)
    return product


def identity_subword_masks(elements: tuple[Permutation, ...]) -> tuple[int, ...]:
    """Return subsets whose increasing-index ordered product is identity."""

    if not elements:
        raise ValueError("at least one element is required")
    identity = _identity(len(elements[0]))
    masks = []
    for mask in range(1 << len(elements)):
        product = identity
        for index, element in enumerate(elements):
            if (mask >> index) & 1:
                product = compose_permutations(product, element)
        if product == identity:
            masks.append(mask)
    return tuple(masks)


def covered_identity_pattern_count(
    identity_masks: tuple[int, ...],
    copies: int,
    *,
    factor_count: int = 4,
) -> int:
    """Count identity-pattern choices that use every ordered factor."""

    if copies < 1:
        raise ValueError("copies must be positive")
    total = 0
    for omitted in range(1 << factor_count):
        allowed = sum(mask & omitted == 0 for mask in identity_masks)
        sign = -1 if omitted.bit_count() % 2 else 1
        total += sign * (allowed**copies)
    if total < 0:
        raise ArithmeticError("coverage inclusion-exclusion became negative")
    return total


def fourth_moment_pattern_polynomials(copies: int) -> dict[str, int]:
    if copies < 1:
        raise ValueError("copies must be positive")
    two = 2**copies
    three = 3**copies
    four = 4**copies
    eight = 8**copies
    return {
        "full_only": two - 1,
        "one_crossing_pair_plus_full": three - two,
        "alternating_noncommuting_pairs": three - 2 * two + 1,
        "two_pair_cover": four - 2 * two + 1,
        "pair_plus_two_triples": four - 3 * two + 2,
        "all_equal": eight - 4 * four + 6 * two - 3,
    }


def audit_involution_class_relations(
    n: int,
    transposition_count: int,
) -> InvolutionClassRelationStatistics:
    conjugacy_class = involution_conjugacy_class(n, transposition_count)
    class_set = set(conjugacy_class)
    size = len(conjugacy_class)
    identity = _identity(n)
    reference = conjugacy_class[0]
    commuting_neighbors = sum(
        compose_permutations(reference, other)
        == compose_permutations(other, reference)
        for other in conjugacy_class
    )
    triple_count = 0
    for left in conjugacy_class:
        for right in conjugacy_class:
            inverse_product = compose_permutations(right, left)
            triple_count += inverse_product in class_set
    four_count = 0
    for first in conjugacy_class:
        for second in conjugacy_class:
            for third in conjugacy_class:
                inverse_product = compose_permutations(
                    compose_permutations(third, second), first
                )
                four_count += inverse_product in class_set
    noncommuting = size * (size - commuting_neighbors)
    distinct = size * (size - 1)
    commuting_distinct = size * (commuting_neighbors - 1)
    repeated_pair_full_relations = (
        2 * noncommuting
        + 2 * distinct
        + commuting_distinct
        + size
    )
    full_without_pair = four_count - repeated_pair_full_relations
    valid = bool(
        size == involution_class_size(n, transposition_count)
        and 1 <= commuting_neighbors <= size
        and 0 <= triple_count <= size * size
        and 0 <= four_count <= size**3
        and full_without_pair >= 0
        and all(
            _ordered_product((first, second, third, inverse_product))
            == identity
            for first, second, third in itertools.islice(
                itertools.product(conjugacy_class, repeat=3), 16
            )
            for inverse_product in (
                compose_permutations(
                    compose_permutations(third, second), first
                ),
            )
        )
    )
    return InvolutionClassRelationStatistics(
        n=n,
        transposition_count=transposition_count,
        conjugacy_class_size=size,
        commuting_class_neighbors_per_element=commuting_neighbors,
        ordered_triple_identity_count=triple_count,
        ordered_four_identity_count=four_count,
        noncommuting_ordered_pair_count=noncommuting,
        distinct_ordered_pair_count=distinct,
        commuting_distinct_ordered_pair_count=commuting_distinct,
        full_relation_without_repeated_pair_count=full_without_pair,
        relation_counts_valid=valid,
    )


def exact_fourth_moment_from_relations(
    statistics: InvolutionClassRelationStatistics,
    copies: int,
) -> Fraction:
    if not statistics.relation_counts_valid:
        raise ValueError("invalid involution relation statistics")
    polynomials = fourth_moment_pattern_polynomials(copies)
    size = statistics.conjugacy_class_size
    numerator = (
        statistics.full_relation_without_repeated_pair_count
        * polynomials["full_only"]
        + 2
        * statistics.noncommuting_ordered_pair_count
        * polynomials["one_crossing_pair_plus_full"]
        + statistics.noncommuting_ordered_pair_count
        * polynomials["alternating_noncommuting_pairs"]
        + (
            2 * statistics.distinct_ordered_pair_count
            + statistics.commuting_distinct_ordered_pair_count
        )
        * polynomials["two_pair_cover"]
        + 6
        * statistics.ordered_triple_identity_count
        * polynomials["pair_plus_two_triples"]
        + size * polynomials["all_equal"]
    )
    return Fraction(numerator, size**4)


def direct_identity_pattern_fourth_moment(
    n: int,
    transposition_count: int,
    copies: int,
) -> Fraction:
    conjugacy_class = involution_conjugacy_class(n, transposition_count)
    total = sum(
        covered_identity_pattern_count(
            identity_subword_masks(elements), copies
        )
        for elements in itertools.product(conjugacy_class, repeat=4)
    )
    return Fraction(total, len(conjugacy_class) ** 4)


def universal_fourth_moment_upper_bound(
    conjugacy_class_size: int,
    copies: int,
) -> Fraction:
    """Bound (6) using only ``E<=M^3`` and ``T,c<=M^2``."""

    if conjugacy_class_size < 2 or copies < 1:
        raise ValueError("class size must be at least two and copies positive")
    size = conjugacy_class_size
    polynomial = fourth_moment_pattern_polynomials(copies)
    numerator = (
        size**3 * polynomial["full_only"]
        + 2 * size**2 * polynomial["one_crossing_pair_plus_full"]
        + size**2 * polynomial["alternating_noncommuting_pairs"]
        + 3 * size**2 * polynomial["two_pair_cover"]
        + 6 * size**2 * polynomial["pair_plus_two_triples"]
        + size * polynomial["all_equal"]
    )
    return Fraction(numerator, size**4)


def interpolation_trace_distance_lower_bound(
    second_moment: Fraction | float,
    fourth_moment_upper_bound: Fraction | float,
) -> float:
    second = float(second_moment)
    fourth = float(fourth_moment_upper_bound)
    if second < 0.0 or fourth <= 0.0:
        raise ValueError("moments must be nonnegative with positive fourth moment")
    return 0.5 * (second**1.5) / math.sqrt(fourth)


def audit_fourth_moment_finite_control(
    n: int,
    transposition_count: int,
    copies: int,
    *,
    maximum_dense_dimension: int = 2048,
) -> FourthMomentFiniteControl:
    statistics = audit_involution_class_relations(n, transposition_count)
    relation_moment = exact_fourth_moment_from_relations(statistics, copies)
    pattern_moment = direct_identity_pattern_fourth_moment(
        n, transposition_count, copies
    )
    second_moment = Fraction((1 << copies) - 1, statistics.conjugacy_class_size)
    lower_bound = interpolation_trace_distance_lower_bound(
        second_moment, relation_moment
    )

    dimension = math.factorial(n) ** copies
    dense_moment: float | None = None
    dense_residual: float | None = None
    dense_distance: float | None = None
    bound_respected = True
    if dimension <= maximum_dense_dimension:
        null, alternative = dense_binary_states(
            n,
            transposition_count,
            copies,
            maximum_dimension=maximum_dense_dimension,
        )
        likelihood_difference = dimension * (alternative - null)
        dense_moment = float(
            np.trace(
                likelihood_difference
                @ likelihood_difference
                @ likelihood_difference
                @ likelihood_difference
            ).real
            / dimension
        )
        dense_residual = abs(dense_moment - float(relation_moment))
        dense_distance = 0.5 * float(
            np.abs(np.linalg.eigvalsh(alternative - null)).sum()
        )
        bound_respected = dense_distance + 1e-9 >= lower_bound

    formula_residual = abs(float(relation_moment - pattern_moment))
    verified = bool(
        statistics.relation_counts_valid
        and formula_residual <= 1e-12
        and (dense_residual is None or dense_residual <= 1e-9)
        and bound_respected
    )
    return FourthMomentFiniteControl(
        n=n,
        transposition_count=transposition_count,
        copy_count=copies,
        conjugacy_class_size=statistics.conjugacy_class_size,
        exact_second_moment=float(second_moment),
        exact_relation_formula_fourth_moment=float(relation_moment),
        direct_identity_pattern_fourth_moment=float(pattern_moment),
        relation_formula_pattern_residual=formula_residual,
        dense_matrix_fourth_moment=dense_moment,
        dense_matrix_residual=dense_residual,
        interpolation_trace_distance_lower_bound=lower_bound,
        dense_helstrom_trace_distance=dense_distance,
        interpolation_bound_respected=bound_respected,
        finite_control_verified=verified,
        status=(
            "exact-fourth-moment-threshold-control-verified"
            if verified
            else "fourth-moment-threshold-control-failure"
        ),
    )


def fourth_moment_threshold_scaling_record(
    n: int,
) -> FourthMomentThresholdScalingRecord:
    if n < 2 or n % 2:
        raise ValueError("n must be positive and even")
    size = involution_class_size(n, n // 2)
    copies = math.ceil(math.log2(size))
    second = Fraction((1 << copies) - 1, size)
    fourth_upper = universal_fourth_moment_upper_bound(size, copies)
    lower = interpolation_trace_distance_lower_bound(second, fourth_upper)
    return FourthMomentThresholdScalingRecord(
        n=n,
        conjugacy_class_size=size,
        threshold_copy_count=copies,
        threshold_second_moment=float(second),
        relation_count_fourth_moment_upper_bound=float(fourth_upper),
        coarse_universal_fourth_moment_bound=UNIVERSAL_FOURTH_MOMENT_BOUND,
        certified_trace_distance_lower_bound=lower,
        coarse_universal_trace_distance_lower_bound=(
            UNIVERSAL_TRACE_DISTANCE_CONSTANT
        ),
        certified_equal_prior_bayes_advantage=lower / 2.0,
        logarithmic_copy_information_sufficiency_proved=(
            lower >= UNIVERSAL_TRACE_DISTANCE_CONSTANT - 1e-12
            and float(fourth_upper) < UNIVERSAL_FOURTH_MOMENT_BOUND
        ),
        polynomial_block_sign_compiler_known=False,
        status="logarithmic-copy-information-sufficient-compiler-open",
    )


def build_hidden_involution_fourth_moment_report(
    *,
    finite_specs: tuple[tuple[int, int, int], ...] = (
        (3, 1, 2),
        (4, 1, 3),
        (4, 2, 2),
        (5, 2, 4),
        (6, 3, 4),
    ),
    scaling_n_values: tuple[int, ...] = (8, 16, 32, 64, 128),
) -> HiddenInvolutionFourthMomentReport:
    controls = [
        audit_fourth_moment_finite_control(n, transpositions, copies)
        for n, transpositions, copies in finite_specs
    ]
    scaling = [
        fourth_moment_threshold_scaling_record(n)
        for n in scaling_n_values
    ]
    verified = all(row.finite_control_verified for row in controls)
    scaling_verified = all(
        row.logarithmic_copy_information_sufficiency_proved
        for row in scaling
    )
    theorem = HiddenInvolutionFourthMomentTheorem(
        exact_fourth_moment_identity=(
            "tau(X_k^4)=M^-4[F P2+2A P3f+A P3p+"
            "(2B+Q)P4p+6T P4t+M P8]."
        ),
        universal_relation_bounds=(
            "F<=E<=M^3, T<=M^2, and A,B,Q<=M^2."
        ),
        interpolation_inequality=(
            "tau|X|>=tau(X^2)^(3/2)/tau(X^4)^(1/2)."
        ),
        threshold_conclusion=(
            "At k=ceil(log2 M), tau(X^2)>=1/2, tau(X^4)<55, "
            "and trace distance exceeds 1/(2^(5/2)sqrt(55))."
        ),
        exact_relation_classification_proved=True,
        fourth_moment_constant_at_log_class_size_proved=True,
        constant_trace_distance_at_log_class_size_proved=True,
        theta_log_class_copy_complexity_proved=True,
        efficient_helstrom_compiler_constructed=False,
        theorem_verified=verified and scaling_verified,
        status=(
            "theta-log-class-information-threshold-proved-compiler-open"
            if verified and scaling_verified
            else "fourth-moment-threshold-theorem-control-failure"
        ),
    )
    metrics: dict[str, int | float] = {
        "finite_control_count": len(controls),
        "finite_validation_failure_count": sum(
            not row.finite_control_verified for row in controls
        ),
        "exact_relation_formula_control_count": sum(
            row.relation_formula_pattern_residual <= 1e-12
            for row in controls
        ),
        "dense_matrix_control_count": sum(
            row.dense_matrix_fourth_moment is not None for row in controls
        ),
        "scaling_record_count": len(scaling),
        "universal_fourth_moment_bound": UNIVERSAL_FOURTH_MOMENT_BOUND,
        "universal_trace_distance_lower_bound": (
            UNIVERSAL_TRACE_DISTANCE_CONSTANT
        ),
        "threshold_information_sufficiency_theorem_count": 1,
        "polynomial_block_sign_compiler_count": 0,
        "new_quantum_algorithm_count": 0,
    }
    return HiddenInvolutionFourthMomentReport(
        created_at=utc_now(),
        primary_literature=[
            {
                "id": "HAYASHI-KAWACHI-KOBAYASHI-2006-HSP-SAMPLE-COMPLEXITY",
                "title": "Quantum Measurements for Hidden Subgroup Problems with Optimal Sample Complexity",
                "url": "https://arxiv.org/abs/quant-ph/0604174",
                "scope": (
                    "The published TCS theorem already gives Theta(log |H|) "
                    "sample complexity for equal prime-order candidate subgroups. "
                    "This report supplies a separate exact fourth-moment certificate."
                ),
            }
        ],
        theorem_contract={
            "access_model": (
                "Independent standard mixed coset states for H={e,h}, with "
                "h promised in one conjugacy class of M>=2 nonidentity involutions."
            ),
            "decision_problem": (
                "Trivial subgroup versus the promised involution class; no "
                "individual hidden-element output."
            ),
            "complexity_scope": (
                "Information-theoretic copy complexity only. Helstrom circuit "
                "size, oracle preparation, and classical query complexity are "
                "outside the theorem."
            ),
            "non_claim": (
                "No efficient measurement, natural GI/code-equivalence transfer, "
                "decision-to-search reduction, classical separation, or speedup."
            ),
        },
        finite_controls=controls,
        scaling_records=scaling,
        theorem=theorem,
        proof_obligations=[
            {
                "id": "PO-COSET-BINARY-BLOCK-SIGN-COMPILER",
                "statement": (
                    "Compile or falsify the invariant k-copy Helstrom sign at "
                    "k=Theta(log |C|) using a polynomial sequence of subgroup, "
                    "recoupling, or algebraic transforms."
                ),
                "resolved": False,
            },
            {
                "id": "PO-COSET-BINARY-SIGN-DEQUANTIZATION",
                "statement": (
                    "Test whether the threshold sign statistic collapses to "
                    "classical collision, character, Weisfeiler--Leman, or code "
                    "invariants under the same access model."
                ),
                "resolved": False,
            },
            {
                "id": "PO-COSET-BINARY-NATURAL-INPUT-TRANSFER",
                "statement": (
                    "Prove a promise-preserving reduction from a natural rigid-GI "
                    "or code-equivalence decision family to the mixed coset-state "
                    "experiment, including automorphisms and preparation cost."
                ),
                "resolved": False,
            },
            {
                "id": "PO-COSET-BINARY-CLASSICAL-QUERY-LOWER-BOUND",
                "statement": (
                    "Establish the best classical randomized query complexity for "
                    "the exact conjugacy-class hidden-subgroup decision promise."
                ),
                "resolved": False,
            },
        ],
        adversarial_audit=[
            {
                "challenge": (
                    "The second moment may be concentrated in exponentially rare "
                    "likelihood spikes, leaving negligible trace distance."
                ),
                "answer": (
                    "Ruled out at k=ceil(log2 M): the exact relation formula bounds "
                    "the fourth moment by a universal constant, and interpolation "
                    "forces constant L1 distance."
                ),
                "resolved": True,
            },
            {
                "challenge": (
                    "Special commutation or high multiplicative energy can destroy "
                    "the constant bound."
                ),
                "answer": (
                    "The proof permits maximal T=M^2 and E=M^3; these worst-case "
                    "counts are already charged in the constant 55."
                ),
                "resolved": True,
            },
            {
                "challenge": (
                    "Theta(log M) states imply a polynomial quantum algorithm."
                ),
                "answer": (
                    "False. Copy complexity ignores the circuit complexity of the "
                    "Helstrom block sign, which may encode the original hard problem."
                ),
                "resolved": True,
            },
            {
                "challenge": (
                    "The theorem identifies h and therefore solves search."
                ),
                "answer": (
                    "False. The symmetrized effect has identical acceptance on "
                    "every h and intentionally carries no individual-h label."
                ),
                "resolved": True,
            },
            {
                "challenge": (
                    "The result is already a graph-isomorphism speedup."
                ),
                "answer": (
                    "False. It is a coset-state promise theorem with no efficient "
                    "measurement, graph input reduction, or matched classical lower bound."
                ),
                "resolved": True,
            },
        ],
        headline_metrics=metrics,
        claim_gate={
            "threshold_trace_distance_lower_bound_proved": True,
            "theta_log_class_copy_complexity_proved": True,
            "information_theoretic_binary_measurement_exists": True,
            "individual_hidden_involution_identified": False,
            "polynomial_higher_copy_block_sign_compiler_constructed": False,
            "natural_graph_or_code_input_transfer_proved": False,
            "classical_superpolynomial_query_lower_bound_proved": False,
            "graph_isomorphism_algorithm_constructed": False,
            "speedup_claim_allowed": False,
            "sample_complexity_result_new_to_literature": False,
            "published_equal_prime_order_sample_theorem_rederived": True,
            "reason": (
                "The information exists at logarithmic copy count, but the "
                "threshold Helstrom sign has not been compiled or separated from "
                "matched classical access on a natural input family."
            ),
        },
        status=theorem.status,
        summary=(
            "Re-derived the published Theta(log |C|) decision sample complexity "
            "through an explicit exact fourth-moment identity. The identity rules "
            "out rare-spike collapse and sharpens compiler diagnostics, but is not "
            "a new sample-complexity theorem."
        ),
        falsifiers_triggered=[
            "The threshold chi-square signal cannot be dismissed as an exponentially rare likelihood spike.",
            "Constant-copy evidence remains invalid even though logarithmic-copy information is sufficient.",
            "Information-theoretic Helstrom existence does not certify an efficient measurement or speedup.",
        ],
    )


def write_hidden_involution_fourth_moment_report(
    output_path: Path = REPORT_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = (
        "EXP-COSET-HIDDEN-INVOLUTION-FOURTH-MOMENT-THRESHOLD"
    ),
    registry_candidate_id: str = "CODE-COSET-COLLECTIVE",
    registry_result_id: str = "",
    **kwargs: Any,
) -> dict[str, Any]:
    path = output_path
    output_path = output_path
    for _k in ("write_registry", "registry_experiment_id", "registry_candidate_id", "registry_result_id"):
        kwargs.pop(_k, None)
    for _k in ("write_registry", "registry_experiment_id", "registry_candidate_id", "registry_result_id"):
        kwargs.pop(_k, None)
    payload = asdict(build_hidden_involution_fourth_moment_report(**kwargs))
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True))


    return payload


if __name__ == "__main__":
    report = write_hidden_involution_fourth_moment_report()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))

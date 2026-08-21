"""Matched classical/quantum query boundary for hidden involution detection.

Consider the standard hiding-oracle promise on a finite group ``G``.  In the
null case ``f`` is injective.  In the alternative case

    f(x)=f(y)  iff  x H_h = y H_h,     H_h={e,h},        (1)

where ``h`` lies in a known conjugacy class ``C`` of ``M`` nonidentity
involutions.  Give the cosets independent random opaque labels.  This is a
hard distribution for classical algorithms and removes accidental structure
from the output alphabet.

For any deterministic adaptive classical algorithm making ``q`` distinct
queries, couple its execution to the null oracle.  Until a collision, all
answers are fresh random labels, so the selected queries are independent of
the uniformly random ``h``.  A queried pair ``x,y`` collides for at most one
hidden involution, namely the nonidentity element of ``y^-1 x H``.  Therefore

    TV(classical transcripts) <= binom(q,2)/M.           (2)

By Yao's principle, equal-prior Bayes advantage ``epsilon`` requires

    q(q-1) >= 4 epsilon M,                               (3)

even for randomized adaptive algorithms.  Repeated queries can be deleted and
do not weaken the bound.

On the quantum side, one coherent oracle call followed by discarding the
output label prepares the standard mixed coset state

    rho_h=(I+R_h)/|G|.                                  (4)

The fourth-moment threshold theorem proves a class-symmetric Helstrom test
with trace distance greater than ``0.023`` from
``k=ceil(log2 M)`` such states.  Hence quantum query complexity is
``O(log M)``, while classical randomized query complexity is
``Omega(sqrt M)``.  Within the restricted independent mixed-coset-state model,
the copy count is ``Theta(log M)``; this module does not prove an
``Omega(log M)`` lower bound against arbitrary coherent quantum-query
strategies.  Repeating a constant number of independent threshold blocks
amplifies the fixed quantum bias without changing the asymptotic query count.

This is an exponential *query* separation, not an efficient quantum
algorithm.  Query complexity treats the potentially exponential Helstrom
measurement as free.  The random-label hiding oracle is also stronger and
less natural than direct graph or code input.  The result is useful as a
matched dequantization boundary and as a precise target for a compiler, but it
does not satisfy the repository's Shor-level computational goal by itself.
"""

from __future__ import annotations

import itertools
import json
import math
from dataclasses import asdict, dataclass
from fractions import Fraction
from pathlib import Path
from typing import Any

from coset_hidden_involution_binary_decision_reduction import (
    Permutation,
    compose_permutations,
    inverse_permutation,
    involution_class_size,
    involution_conjugacy_class,
    symmetric_group,
)
from coset_hidden_involution_fourth_moment_threshold import (
    UNIVERSAL_TRACE_DISTANCE_CONSTANT,
)
from research_registry import utc_now


REPORT_PATH = Path(
    "research/classical_baselines/"
    "coset_hidden_involution_query_separation_boundary.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-COSET-HIDDEN-INVOLUTION-QUERY-SEPARATION-BOUNDARY"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"
DEFAULT_TARGET_BAYES_ADVANTAGE = Fraction(1, 100)


@dataclass(frozen=True)
class ClassicalQueryFiniteControl:
    n: int
    transposition_count: int
    distinct_query_count: int
    conjugacy_class_size: int
    queried_pair_count: int
    exposed_hidden_involution_count: int
    exact_uniform_hidden_collision_probability: float
    pair_union_upper_bound: float
    maximum_candidate_multiplicity: int
    exact_collision_candidate_identity_verified: bool
    pair_bound_verified: bool
    status: str


@dataclass(frozen=True)
class QuerySeparationScalingRecord:
    n: int
    conjugacy_class_size: int
    log2_conjugacy_class_size: float
    target_equal_prior_bayes_advantage: float
    quantum_threshold_query_count: int
    coset_state_information_lower_bound: int
    classical_randomized_query_lower_bound: int
    log2_classical_query_lower_bound: float
    classical_lower_bound_over_quantum_threshold: float
    exponential_query_separation_certified: bool
    polynomial_time_quantum_measurement_known: bool
    natural_input_reduction_known: bool
    status: str


@dataclass(frozen=True)
class HiddenInvolutionQuerySeparationTheorem:
    coupling_statement: str
    classical_transcript_bound: str
    yao_consequence: str
    quantum_query_upper: str
    query_separation: str
    adaptive_classical_coupling_proved: bool
    randomized_classical_sqrt_class_lower_bound_proved: bool
    quantum_log_class_query_upper_bound_proved: bool
    arbitrary_coherent_quantum_query_lower_bound_proved: bool
    exponential_query_separation_proved: bool
    polynomial_time_quantum_algorithm_constructed: bool
    theorem_verified: bool
    status: str


@dataclass(frozen=True)
class HiddenInvolutionQuerySeparationReport:
    created_at: str
    primary_literature: list[dict[str, str]]
    theorem_contract: dict[str, Any]
    finite_controls: list[ClassicalQueryFiniteControl]
    scaling_records: list[QuerySeparationScalingRecord]
    theorem: HiddenInvolutionQuerySeparationTheorem
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def hidden_candidates_exposed_by_queries(
    queries: tuple[Permutation, ...],
    conjugacy_class: tuple[Permutation, ...],
) -> dict[Permutation, int]:
    """Count queried pairs that would collide for each promised hidden element."""

    if len(set(queries)) != len(queries):
        raise ValueError("classical lower-bound controls require distinct queries")
    class_set = set(conjugacy_class)
    multiplicities: dict[Permutation, int] = {}
    for left_index in range(len(queries)):
        for right_index in range(left_index + 1, len(queries)):
            left = queries[left_index]
            right = queries[right_index]
            candidate = compose_permutations(
                inverse_permutation(left), right
            )
            if candidate in class_set:
                multiplicities[candidate] = multiplicities.get(candidate, 0) + 1
    return multiplicities


def queries_collide_for_hidden(
    queries: tuple[Permutation, ...],
    hidden: Permutation,
) -> bool:
    for left_index in range(len(queries)):
        for right_index in range(left_index + 1, len(queries)):
            relative = compose_permutations(
                inverse_permutation(queries[left_index]),
                queries[right_index],
            )
            if relative == hidden:
                return True
    return False


def audit_classical_query_control(
    n: int,
    transposition_count: int,
    query_count: int,
) -> ClassicalQueryFiniteControl:
    group = symmetric_group(n)
    conjugacy_class = involution_conjugacy_class(n, transposition_count)
    if not 1 <= query_count <= len(group):
        raise ValueError("query_count is outside the finite group")

    identity = tuple(range(n))
    seeded_queries = [identity]
    seeded_queries.extend(conjugacy_class[: max(0, query_count - 1)])
    if len(seeded_queries) < query_count:
        seeded_queries.extend(
            element
            for element in group
            if element not in seeded_queries
        )
    queries = tuple(seeded_queries[:query_count])
    candidates = hidden_candidates_exposed_by_queries(
        queries, conjugacy_class
    )
    collision_hidden = {
        hidden
        for hidden in conjugacy_class
        if queries_collide_for_hidden(queries, hidden)
    }
    pair_count = math.comb(query_count, 2)
    exact_probability = len(collision_hidden) / len(conjugacy_class)
    union_upper = min(1.0, pair_count / len(conjugacy_class))
    identity_verified = collision_hidden == set(candidates)
    bound_verified = len(candidates) <= pair_count
    return ClassicalQueryFiniteControl(
        n=n,
        transposition_count=transposition_count,
        distinct_query_count=query_count,
        conjugacy_class_size=len(conjugacy_class),
        queried_pair_count=pair_count,
        exposed_hidden_involution_count=len(candidates),
        exact_uniform_hidden_collision_probability=exact_probability,
        pair_union_upper_bound=union_upper,
        maximum_candidate_multiplicity=max(candidates.values(), default=0),
        exact_collision_candidate_identity_verified=identity_verified,
        pair_bound_verified=bound_verified,
        status=(
            "classical-collision-candidate-bound-verified"
            if identity_verified and bound_verified
            else "classical-query-control-failure"
        ),
    )


def minimum_classical_queries_for_bayes_advantage(
    conjugacy_class_size: int,
    advantage: Fraction = DEFAULT_TARGET_BAYES_ADVANTAGE,
) -> int:
    """Smallest integer not ruled out by ``q(q-1)>=4 epsilon M``."""

    if conjugacy_class_size < 1:
        raise ValueError("conjugacy_class_size must be positive")
    if not Fraction() < advantage <= Fraction(1, 2):
        raise ValueError("advantage must lie in (0,1/2]")
    numerator = 4 * advantage.numerator * conjugacy_class_size
    denominator = advantage.denominator
    estimate = max(1, math.isqrt(numerator // denominator))
    while denominator * estimate * (estimate - 1) < numerator:
        estimate += 1
    while (
        estimate > 1
        and denominator * (estimate - 1) * (estimate - 2) >= numerator
    ):
        estimate -= 1
    return estimate


def minimum_quantum_copies_from_chi_square(
    conjugacy_class_size: int,
    advantage: Fraction = DEFAULT_TARGET_BAYES_ADVANTAGE,
) -> int:
    """Necessary copies for equal-prior Bayes advantage ``advantage``."""

    target = (
        Fraction(1)
        + 16 * advantage * advantage * conjugacy_class_size
    )
    copies = 0
    while (1 << copies) < target:
        copies += 1
    return copies


def query_separation_scaling_record(
    n: int,
    *,
    target_advantage: Fraction = DEFAULT_TARGET_BAYES_ADVANTAGE,
) -> QuerySeparationScalingRecord:
    if n < 2 or n % 2:
        raise ValueError("n must be positive and even")
    size = involution_class_size(n, n // 2)
    quantum_threshold = math.ceil(math.log2(size))
    quantum_lower = minimum_quantum_copies_from_chi_square(
        size, target_advantage
    )
    classical_lower = minimum_classical_queries_for_bayes_advantage(
        size, target_advantage
    )
    # The exact lower bound is Omega(sqrt(M)); finite rows only check that its
    # certified value has already overtaken the logarithmic quantum threshold.
    separation = classical_lower > quantum_threshold
    return QuerySeparationScalingRecord(
        n=n,
        conjugacy_class_size=size,
        log2_conjugacy_class_size=math.log2(size),
        target_equal_prior_bayes_advantage=float(target_advantage),
        quantum_threshold_query_count=quantum_threshold,
        coset_state_information_lower_bound=quantum_lower,
        classical_randomized_query_lower_bound=classical_lower,
        log2_classical_query_lower_bound=math.log2(classical_lower),
        classical_lower_bound_over_quantum_threshold=(
            classical_lower / quantum_threshold
        ),
        exponential_query_separation_certified=separation,
        polynomial_time_quantum_measurement_known=False,
        natural_input_reduction_known=False,
        status="exponential-query-separation-computational-compiler-open",
    )


def build_hidden_involution_query_separation_report(
    *,
    finite_specs: tuple[tuple[int, int, int], ...] = (
        (3, 1, 2),
        (3, 1, 3),
        (4, 1, 4),
        (4, 2, 3),
        (5, 2, 6),
        (6, 3, 6),
    ),
    scaling_n_values: tuple[int, ...] = (16, 32, 64, 128),
) -> HiddenInvolutionQuerySeparationReport:
    if float(DEFAULT_TARGET_BAYES_ADVANTAGE) >= (
        UNIVERSAL_TRACE_DISTANCE_CONSTANT / 2.0
    ):
        raise ArithmeticError(
            "target advantage exceeds the fourth-moment quantum certificate"
        )
    controls = [
        audit_classical_query_control(n, transpositions, queries)
        for n, transpositions, queries in finite_specs
    ]
    scaling = [
        query_separation_scaling_record(n)
        for n in scaling_n_values
    ]
    verified = all(
        row.exact_collision_candidate_identity_verified
        and row.pair_bound_verified
        for row in controls
    )
    scaling_verified = all(
        row.exponential_query_separation_certified for row in scaling
    )
    theorem = HiddenInvolutionQuerySeparationTheorem(
        coupling_statement=(
            "Run the adaptive algorithm against random injective null labels; "
            "for uniform h, the alternative transcript is identical until h "
            "appears as a queried pair difference."
        ),
        classical_transcript_bound=(
            "TV(T_null,T_alt)<=|D_C(Q)|/M<=binom(q,2)/M."
        ),
        yao_consequence=(
            "Randomized worst-case Bayes advantage epsilon requires "
            "q(q-1)>=4 epsilon M."
        ),
        quantum_query_upper=(
            "ceil(log2 M) coherent queries prepare enough coset states for "
            "the class-symmetric fourth-moment Helstrom test; constant repetition "
            "amplifies its fixed bias."
        ),
        query_separation=(
            "Quantum O(log M) versus classical Omega(sqrt M) oracle queries; "
            "Theta(log M) is proved only for independent mixed coset states."
        ),
        adaptive_classical_coupling_proved=True,
        randomized_classical_sqrt_class_lower_bound_proved=True,
        quantum_log_class_query_upper_bound_proved=True,
        arbitrary_coherent_quantum_query_lower_bound_proved=False,
        exponential_query_separation_proved=scaling_verified,
        polynomial_time_quantum_algorithm_constructed=False,
        theorem_verified=verified and scaling_verified,
        status=(
            "exponential-hidden-involution-query-separation-compiler-open"
            if verified and scaling_verified
            else "hidden-involution-query-separation-control-failure"
        ),
    )
    metrics: dict[str, int | float] = {
        "finite_control_count": len(controls),
        "finite_control_failure_count": sum(
            not (
                row.exact_collision_candidate_identity_verified
                and row.pair_bound_verified
            )
            for row in controls
        ),
        "scaling_record_count": len(scaling),
        "certified_scaling_separation_count": sum(
            row.exponential_query_separation_certified for row in scaling
        ),
        "target_bayes_advantage": float(DEFAULT_TARGET_BAYES_ADVANTAGE),
        "quantum_trace_distance_constant": (
            UNIVERSAL_TRACE_DISTANCE_CONSTANT
        ),
        "exponential_query_separation_theorem_count": 1,
        "polynomial_time_quantum_algorithm_count": 0,
        "natural_input_speedup_count": 0,
    }
    return HiddenInvolutionQuerySeparationReport(
        created_at=utc_now(),
        primary_literature=[
            {
                "id": "ETTINGER-HOYER-KNILL-2004-HSP-QUERY",
                "title": "The quantum query complexity of the hidden subgroup problem is polynomial",
                "url": "https://arxiv.org/abs/quant-ph/0401083",
                "scope": (
                    "Already proves polynomial quantum query complexity for arbitrary "
                    "finite-group HSP while explicitly allowing exponential time."
                ),
            },
            {
                "id": "HAYASHI-KAWACHI-KOBAYASHI-2006-HSP-SAMPLE-COMPLEXITY",
                "title": "Quantum Measurements for Hidden Subgroup Problems with Optimal Sample Complexity",
                "url": "https://arxiv.org/abs/quant-ph/0604174",
                "scope": (
                    "Already proves the equal-prime-order logarithmic sample bound "
                    "for both triviality and identification."
                ),
            },
        ],
        theorem_contract={
            "oracle_promise": (
                "Random opaque injective labels on elements under H={e}, or on "
                "right cosets under H={e,h} for h in a known involution class."
            ),
            "classical_model": (
                "Randomized adaptive point queries; repeated queries removed "
                "without loss; arbitrary computation between queries."
            ),
            "quantum_model": (
                "Coherent oracle queries, efficient or free uniform group-state "
                "preparation, and arbitrary query-free postprocessing. The "
                "Omega(log M) information lower bound is scoped only to "
                "independent mixed coset states."
            ),
            "non_claim": (
                "No polynomial gate complexity, direct graph/code input result, "
                "decision-to-search reduction, or computational speedup."
            ),
        },
        finite_controls=controls,
        scaling_records=scaling,
        theorem=theorem,
        proof_obligations=[
            {
                "id": "PO-COSET-BINARY-POLYNOMIAL-HELSTROM-COMPILER",
                "statement": (
                    "Implement the threshold invariant sign with polynomial gate "
                    "complexity; query complexity currently treats it as free."
                ),
                "resolved": False,
            },
            {
                "id": "PO-COSET-BINARY-NATURAL-INPUT-TRANSFER",
                "statement": (
                    "Replace the random opaque hiding oracle by a natural rigid-GI "
                    "or code-equivalence input without assuming the desired canonizer."
                ),
                "resolved": False,
            },
            {
                "id": "PO-COSET-BINARY-DECISION-TO-SEARCH",
                "statement": (
                    "Determine whether binary subgroup existence can recover an "
                    "isomorphism/transporter with polynomially many natural calls."
                ),
                "resolved": False,
            },
            {
                "id": "PO-COSET-BINARY-STRUCTURED-CLASSICAL-BASELINE",
                "statement": (
                    "Re-run the comparison when oracle labels expose graph/code "
                    "structure rather than independent random names."
                ),
                "resolved": False,
            },
        ],
        adversarial_audit=[
            {
                "challenge": "Adaptive classical queries evade the pair count.",
                "answer": (
                    "False under the hard random-label distribution. Before the "
                    "first collision every response is fresh and independent of h, "
                    "so the null-coupled query set exposes at most one h per pair."
                ),
                "resolved": True,
            },
            {
                "challenge": "Randomized algorithms evade the deterministic coupling.",
                "answer": (
                    "False. Yao's minimax principle applies the uniform-h, random-label "
                    "distribution to every deterministic algorithm in the support."
                ),
                "resolved": True,
            },
            {
                "challenge": "The logarithmic-state theorem is not a query algorithm.",
                "answer": (
                    "It is a query algorithm only in the formal model where arbitrary "
                    "oracle-independent Helstrom postprocessing is free; it is not a "
                    "polynomial-time algorithm."
                ),
                "resolved": True,
            },
            {
                "challenge": "An exponential oracle-query gap is Shor-level progress.",
                "answer": (
                    "Not by itself. The opaque oracle can hide all computational work "
                    "inside state discrimination, and no natural-input compiler exists."
                ),
                "resolved": True,
            },
            {
                "challenge": "The result dequantizes on structured labels.",
                "answer": (
                    "Unresolved. Random labels prove a worst-case query lower bound, "
                    "not hardness when graph or code labels expose extra invariants."
                ),
                "resolved": False,
            },
        ],
        headline_metrics=metrics,
        claim_gate={
            "adaptive_classical_sqrt_class_query_lower_bound_proved": True,
            "quantum_log_class_query_upper_bound_proved": True,
            "independent_coset_state_theta_log_class_copy_bound_proved": True,
            "arbitrary_coherent_quantum_query_lower_bound_proved": False,
            "exponential_oracle_query_separation_proved": scaling_verified,
            "polynomial_time_quantum_measurement_constructed": False,
            "natural_graph_or_code_input_reduction_proved": False,
            "decision_to_search_reduction_proved": False,
            "structured_label_dequantization_passed": False,
            "shor_level_algorithm_discovered": False,
            "oracle_query_separation_new_to_literature": False,
            "published_unbounded_postprocessing_boundary_recovered": True,
            "speedup_claim_allowed": False,
            "reason": (
                "The oracle-query gap is exact, but its quantum postprocessing is "
                "unbounded and the opaque-label promise is not a natural input model."
            ),
        },
        status=theorem.status,
        summary=(
            "Recovered the known unbounded-postprocessing HSP query boundary in "
            "the promised involution class and supplied an explicit adaptive "
            "classical pair-exposure bound. This is not a new oracle separation; "
            "polynomial gate complexity remains the real open problem."
        ),
        falsifiers_triggered=[
            "The logarithmic-copy signal is not classically recoverable with logarithmically many opaque-label point queries.",
            "The query separation cannot be promoted to a polynomial-time or natural-input speedup.",
            "Adaptive classical query selection does not beat the pre-collision pair-exposure bound.",
        ],
    )


def write_hidden_involution_query_separation_report(
    output_path: Path = REPORT_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = (
        "EXP-COSET-HIDDEN-INVOLUTION-QUERY-SEPARATION-BOUNDARY"
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
    payload = asdict(build_hidden_involution_query_separation_report(**kwargs))
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True))


    return payload


if __name__ == "__main__":
    report = write_hidden_involution_query_separation_report()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))

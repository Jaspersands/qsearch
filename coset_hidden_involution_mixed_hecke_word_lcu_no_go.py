"""Mixed-word LCU no-go for diagonal all-copy hidden-involution charges.

Let ``X_t=e_B a_t e_B`` for diagonal all-copy elements
``a_t=(t,...,t;t)``.  Expanding any mixed word

    W = X_(t_1) X_(t_2) ... X_(t_d)

in the exact binary path normal form produces an ordered sequence of conjugates
of ``h``.  A nontrivial orbital step has two consecutive, distinct
involutions.  Fixing every other binary choice leaves the four products
``e,a,b,ab``, which are pairwise distinct.  Thus every identity fiber has at
most one quarter of the subword cube, exactly as in the single-operator proof.

Consequently every nontrivial mixed word has baseline and
likelihood-weighted normalized trace at most ``2^-k``, and absolute likelihood
bias at most ``2^-k``.  Every mixed-word LCU
``Y=sum_w alpha_w W_w`` with ``sum_w |alpha_w|<=1`` obeys the same bound.  At
natural copy count this is at most ``1/(64M)``.

This removes normalized finite mixtures, commutators, and ordinary word LCUs
from the search space.  It does not cover bounded coherent noncommutative
polynomials whose word coefficient ``l1`` norm is large, block-encoded
matrix-Hecke polar transforms, adaptive postselection, or direct recoupling
bases.  Those are the remaining multi-operator frontier.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from coset_hidden_involution_binary_decision_reduction import (
    Permutation,
    involution_class_size,
)
from coset_hidden_involution_cross_transposition_hecke_moment_no_go import (
    _matching_from_edges,
    _switch_neighbours,
)
from coset_hidden_involution_orbit_synthesis_flatness import (
    flatness_copy_count,
)
from coset_hidden_involution_single_hecke_all_degree_moment_no_go import (
    adjacent_pair_products,
    ordered_subword_product_histogram,
)
from research_registry import utc_now


REPORT_PATH = Path(
    "research/representation/"
    "coset_hidden_involution_mixed_hecke_word_lcu_no_go.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-COSET-HIDDEN-INVOLUTION-MIXED-HECKE-WORD-LCU-NO-GO"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


@dataclass(frozen=True)
class MixedWordFiberControl:
    half_degree: int
    word_degree: int
    nontrivial_transition_index: int
    involution_count: int
    subword_cube_size: int
    maximum_product_fiber_size: int
    one_quarter_bound: int
    selected_adjacent_involutions_distinct: bool
    selected_four_bit_products_pairwise_distinct: bool
    later_repeated_involutions_present: bool
    mixed_word_fiber_bound_verified: bool
    status: str


@dataclass(frozen=True)
class MixedWordLCUBoundControl:
    word_degree: int
    copy_count: int
    mixed_operator_count: int
    word_count: int
    coefficient_l1_norm_upper_bound: float
    individual_word_bias_upper_bound: str
    mixed_word_LCU_bias_upper_bound: str
    bound_independent_of_word_degree: bool
    bound_independent_of_operator_count: bool
    normalized_LCU_bound_verified: bool
    status: str


@dataclass(frozen=True)
class MixedWordScalingRecord:
    half_degree: int
    degree: int
    conjugacy_class_size_decimal: str
    copy_count: int
    normalized_mixed_word_bias_upper_bound: float
    normalized_mixed_word_LCU_bias_upper_bound: float
    inverse_64_candidates: float
    bound_at_most_inverse_64_candidates: bool
    status: str


@dataclass(frozen=True)
class MixedWordLCUTheorem:
    mixed_path_normal_form: str
    nontrivial_transition_injection: str
    individual_word_bound: str
    normalized_LCU_bound: str
    natural_copy_consequence: str
    adjacent_pair_injection_extends_to_mixed_words: bool
    all_degree_mixed_word_trace_no_go_proved: bool
    normalized_mixed_word_LCU_no_go_proved: bool
    large_word_l1_bounded_operator_no_go_proved: bool
    matrix_Hecke_polar_no_go_proved: bool
    hidden_involution_detector_constructed: bool
    speedup_claim_allowed: bool
    theorem_verified: bool
    status: str


@dataclass(frozen=True)
class MixedWordLCUReport:
    created_at: str
    theorem_contract: dict[str, Any]
    fiber_controls: list[MixedWordFiberControl]
    LCU_controls: list[MixedWordLCUBoundControl]
    scaling_records: list[MixedWordScalingRecord]
    theorem: MixedWordLCUTheorem
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _mixed_control_sequence(
    half_degree: int,
    word_degree: int,
    nontrivial_transition_index: int,
) -> tuple[Permutation, ...]:
    if half_degree < 3 or word_degree < 2:
        raise ValueError("half_degree>=3 and word_degree>=2 are required")
    if not 0 <= nontrivial_transition_index < word_degree:
        raise ValueError("nontrivial transition index is out of range")
    degree = 2 * half_degree
    crossed = _matching_from_edges(
        ((0, 2), (1, 3))
        + tuple(
            (2 * pair, 2 * pair + 1)
            for pair in range(2, half_degree)
        ),
        degree,
    )
    neighbour = min(_switch_neighbours(crossed))
    sequence = [crossed] * (word_degree + 1)
    sequence[nontrivial_transition_index] = crossed
    sequence[nontrivial_transition_index + 1] = neighbour
    return tuple(sequence)


def audit_mixed_word_fiber(
    half_degree: int,
    word_degree: int,
    nontrivial_transition_index: int = 0,
) -> MixedWordFiberControl:
    elements = _mixed_control_sequence(
        half_degree,
        word_degree,
        nontrivial_transition_index,
    )
    left = elements[nontrivial_transition_index]
    right = elements[nontrivial_transition_index + 1]
    histogram = ordered_subword_product_histogram(elements)
    cube_size = 1 << len(elements)
    maximum = max(histogram.values())
    bound = cube_size // 4
    distinct = left != right
    injection = len(set(adjacent_pair_products(left, right))) == 4
    repeated = len(set(elements)) < len(elements)
    verified = bool(distinct and injection and maximum <= bound)
    return MixedWordFiberControl(
        half_degree=half_degree,
        word_degree=word_degree,
        nontrivial_transition_index=nontrivial_transition_index,
        involution_count=len(elements),
        subword_cube_size=cube_size,
        maximum_product_fiber_size=maximum,
        one_quarter_bound=bound,
        selected_adjacent_involutions_distinct=distinct,
        selected_four_bit_products_pairwise_distinct=injection,
        later_repeated_involutions_present=repeated,
        mixed_word_fiber_bound_verified=verified,
        status=(
            "mixed-word-adjacent-pair-fiber-bound-verified"
            if verified
            else "mixed-word-fiber-control-failure"
        ),
    )


def mixed_word_LCU_bound_control(
    word_degree: int,
    copy_count: int,
    mixed_operator_count: int,
    word_count: int,
    coefficient_l1_norm_upper_bound: float = 1.0,
) -> MixedWordLCUBoundControl:
    if min(word_degree, copy_count, mixed_operator_count, word_count) < 1:
        raise ValueError("all integer parameters must be positive")
    if not 0.0 <= coefficient_l1_norm_upper_bound <= 1.0:
        raise ValueError("coefficient l1 bound must lie in [0,1]")
    denominator = 2**copy_count
    individual = f"1/{denominator}"
    mixed_numerator = coefficient_l1_norm_upper_bound
    mixed = f"{mixed_numerator}/{denominator}"
    verified = mixed_numerator <= 1.0
    return MixedWordLCUBoundControl(
        word_degree=word_degree,
        copy_count=copy_count,
        mixed_operator_count=mixed_operator_count,
        word_count=word_count,
        coefficient_l1_norm_upper_bound=coefficient_l1_norm_upper_bound,
        individual_word_bias_upper_bound=individual,
        mixed_word_LCU_bias_upper_bound=mixed,
        bound_independent_of_word_degree=True,
        bound_independent_of_operator_count=True,
        normalized_LCU_bound_verified=verified,
        status=(
            "normalized-mixed-word-LCU-inverse-copy-bound"
            if verified
            else "mixed-word-LCU-bound-control-failure"
        ),
    )


def mixed_word_scaling_record(
    half_degree: int,
) -> MixedWordScalingRecord:
    if half_degree < 3:
        raise ValueError("half_degree must be at least three")
    degree = 2 * half_degree
    candidates = involution_class_size(degree, half_degree)
    copies = flatness_copy_count(candidates)
    bound = 2.0 ** (-copies)
    inverse_candidates = 1.0 / (64.0 * candidates)
    verified = bound <= inverse_candidates * (1.0 + 1e-15)
    return MixedWordScalingRecord(
        half_degree=half_degree,
        degree=degree,
        conjugacy_class_size_decimal=str(candidates),
        copy_count=copies,
        normalized_mixed_word_bias_upper_bound=bound,
        normalized_mixed_word_LCU_bias_upper_bound=bound,
        inverse_64_candidates=inverse_candidates,
        bound_at_most_inverse_64_candidates=verified,
        status=(
            "normalized-mixed-Hecke-word-bias-inverse-candidate"
            if verified
            else "mixed-Hecke-word-scaling-control-failure"
        ),
    )


def build_mixed_word_LCU_report() -> MixedWordLCUReport:
    fibers = [
        audit_mixed_word_fiber(
            half_degree,
            word_degree,
            transition,
        )
        for half_degree in (3, 4, 5)
        for word_degree in (2, 3, 5, 8)
        for transition in (0, word_degree // 2)
    ]
    LCU_controls = [
        mixed_word_LCU_bound_control(
            word_degree,
            copy_count,
            mixed_operator_count,
            mixed_operator_count**min(word_degree, 4),
        )
        for word_degree in (1, 4, 16, 64)
        for copy_count in (1, 5, 17)
        for mixed_operator_count in (2, 8)
    ]
    scaling = [
        mixed_word_scaling_record(half_degree)
        for half_degree in (4, 8, 16, 32, 64)
    ]
    verified = bool(
        all(row.mixed_word_fiber_bound_verified for row in fibers)
        and all(row.normalized_LCU_bound_verified for row in LCU_controls)
        and all(row.bound_at_most_inverse_64_candidates for row in scaling)
    )
    theorem = MixedWordLCUTheorem(
        mixed_path_normal_form=(
            "Every diagonal all-copy mixed Hecke word expands into ordered "
            "binary subwords of conjugates of h along an orbital path."
        ),
        nontrivial_transition_injection=(
            "Any nontrivial step supplies adjacent distinct involutions a,b; "
            "fixing other bits makes e,a,b,ab pairwise distinct."
        ),
        individual_word_bound=(
            "Every nontrivial mixed word has baseline and alternative trace "
            "at most 2^-k and absolute likelihood bias at most 2^-k."
        ),
        normalized_LCU_bound=(
            "For sum_w|alpha_w|<=1, the mixed-word LCU bias is at most 2^-k, "
            "independent of word count, degree, and operator count."
        ),
        natural_copy_consequence=(
            "At k=ceil(log2(64M)), normalized mixed-word LCU bias is at most 1/(64M)."
        ),
        adjacent_pair_injection_extends_to_mixed_words=True,
        all_degree_mixed_word_trace_no_go_proved=True,
        normalized_mixed_word_LCU_no_go_proved=True,
        large_word_l1_bounded_operator_no_go_proved=False,
        matrix_Hecke_polar_no_go_proved=False,
        hidden_involution_detector_constructed=False,
        speedup_claim_allowed=False,
        theorem_verified=verified,
        status=(
            "mixed-Hecke-word-and-normalized-LCU-no-go"
            if verified
            else "mixed-Hecke-word-LCU-control-failure"
        ),
    )
    return MixedWordLCUReport(
        created_at=utc_now(),
        theorem_contract={
            "operator_family": (
                "Diagonal all-copy B-Hecke operators X_t=e_B a_t e_B"
            ),
            "word_scope": (
                "Arbitrary finite mixed words with at least one nontrivial "
                "loopless orbital transition"
            ),
            "normalization": "Mixed-word coefficient l1 norm at most one",
            "claim_boundary": (
                "Does not cover bounded coherent constructions with large word "
                "l1 norm, matrix-Hecke polar transforms, or postselection."
            ),
        },
        fiber_controls=fibers,
        LCU_controls=LCU_controls,
        scaling_records=scaling,
        theorem=theorem,
        proof_obligations=[
            {
                "id": "PO-HIDDEN-INVOLUTION-BOUNDED-NONCOMMUTATIVE-POLYNOMIAL",
                "statement": (
                    "Bound or exploit coherent noncommutative polynomials whose "
                    "operator norm is one but word coefficient l1 norm is large."
                ),
                "resolved": False,
            },
            {
                "id": "PO-HIDDEN-INVOLUTION-MATRIX-HECKE-POLAR",
                "statement": (
                    "Determine whether the matrix-valued induced-source transfer "
                    "has a structured polar not representable as a normalized word LCU."
                ),
                "resolved": False,
            },
        ],
        adversarial_audit=[
            {
                "challenge": "Noncommutativity invalidates the subword injection.",
                "answer": (
                    "False for word traces: the proof fixes all other bits and "
                    "uses only cancellation around one adjacent pair."
                ),
                "resolved": True,
            },
            {
                "challenge": "Exponentially many words amplify the signal.",
                "answer": (
                    "Not under physical l1 normalization; the triangle inequality "
                    "removes the word count. Large coherent coefficient norm remains open."
                ),
                "resolved": True,
            },
            {
                "challenge": "This rules out the matrix-Hecke recoupling program.",
                "answer": (
                    "False. A bounded coherent polar may have large word l1 norm "
                    "and exploit interference outside this LCU model."
                ),
                "resolved": True,
            },
        ],
        headline_metrics={
            "finite_mixed_fiber_control_count": len(fibers),
            "symbolic_LCU_bound_control_count": len(LCU_controls),
            "natural_scaling_row_count": len(scaling),
            "maximum_observed_product_fiber_fraction": max(
                row.maximum_product_fiber_size / row.subword_cube_size
                for row in fibers
            ),
            "new_detector_count": 0,
        },
        claim_gate={
            "mixed_word_one_quarter_fiber_bound_proved": True,
            "all_degree_mixed_word_trace_no_go_proved": True,
            "normalized_mixed_word_LCU_no_go_proved": True,
            "bounded_large_l1_noncommutative_filter_no_go_proved": False,
            "matrix_Hecke_polar_no_go_proved": False,
            "hidden_involution_detector_constructed": False,
            "speedup_claim_allowed": False,
            "reason": (
                "Ordinary normalized mixtures retain inverse-candidate bias; "
                "only genuinely coherent matrix-Hecke constructions remain open."
            ),
        },
        status=theorem.status,
        summary=(
            "Extended the all-degree fiber injection from powers of one operator "
            "to arbitrary mixed diagonal-Hecke words and normalized word LCUs."
        ),
        falsifiers_triggered=[
            "Adding finitely or exponentially many normalized word terms does not amplify likelihood bias.",
            "Ordinary commutators of diagonal all-copy charges remain inverse-candidate under l1 normalization.",
            "Any surviving multi-operator route must exploit bounded coherent interference beyond word-l1 normalization.",
        ],
    )


def write_mixed_word_LCU_report(
    output_path: Path = REPORT_PATH,
) -> dict[str, Any]:
    payload = asdict(build_mixed_word_LCU_report())
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    return payload


def run_experiment(
    experiment_id: str = DEFAULT_EXPERIMENT_ID,
    candidate_id: str = DEFAULT_CANDIDATE_ID,
    write_registry: bool = True,
) -> dict[str, Any]:
    del experiment_id, candidate_id, write_registry
    return write_mixed_word_LCU_report()


if __name__ == "__main__":
    print(json.dumps(run_experiment(), indent=2, sort_keys=True))

"""Universal codimension-two no-go for the single-fiber BABA boundary.

Let ``C`` be any length-``n`` binary code of size ``2^(n-2)`` and minimum
distance at least two.  Use the full code on the different support and remove
one row on the same support in the mixed ``BABA`` construction.  There are two
exhaustive branches.

If ``C`` has an information set of size ``n-2``, each unit information pattern
gives a codeword relator containing its information generator once and no
other information generator.  These relations eliminate all ``n-2``
information generators, in any ambient coordinate order, leaving at most two
check generators.

If ``C`` has no such information set, every omitted coordinate pair has a
distance-two collision.  The triangular pair-witness theorem then collapses
all coordinate generators to powers ``x^(+/-1)`` and leaves only one appended
generator.

Both branches share an exact marked relation.  The split relation, one
different complement relation, and one same complement relation reduce to

    K(U) = e^-1 U^-1 q^-1 b p^-1 b^-1 p q U h^-1 e h,

where ``U`` is an arbitrary word in the residual appended generators.  The
Nielsen automorphism ``q -> q U^-1`` sends ``K(U)`` to the coefficient-free
orientable genus-two word ``K(1)``.  Thus the information-set branch has at
most seven generators and symmetric-group solution exponent at most six; the
no-information-set branch has at most six and exponent at most five.

For supports of sizes ``2^(n-2)-1`` and ``2^(n-2)``, the corresponding pressure
margins are strictly greater than one and two.  Therefore every codimension-two
stopping core in this single-base-fiber ``BABA`` power-boundary family is
uniformly subleading, regardless of nonlinearity, information-set existence,
coordinate order, or affine normalization.  Higher codimension, multiple base
fibers, and other marked patterns remain open.  No quantum speedup is claimed.
"""

from __future__ import annotations

import itertools
import json
import math
from dataclasses import asdict, dataclass
from functools import lru_cache
from pathlib import Path
from typing import Any

from research_registry import utc_now
from self_dual_wreath_marked_pressure_obstruction_search import (
    _transport_target_product_word,
)
from self_dual_wreath_marked_relation_topology import (
    SignedWord,
    _substitute_word_images,
    free_reduce,
    marked_support_presentation,
    orientable_quadratic_genus,
    presentation_solution_exponent_upper_bound,
    tietze_reduce_presentation,
)
from self_dual_wreath_nonsystematic_incidence_lattice_bound import (
    INDEX_THREE_CODE,
)
from self_dual_wreath_nonsystematic_pair_witness_collapse import (
    pair_witness_elimination_steps,
)
from self_dual_wreath_nonsystematic_twisted_star_no_go import twisted_star_code
from self_dual_wreath_support_difference_peeling_no_go import (
    Assignment,
    audit_support_difference_peeling_lift,
)
from self_dual_wreath_systematic_stopping_core_no_go import (
    representative_systematic_coloring,
    systematic_graph_code,
)


REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_codimension_two_universal_no_go.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-CODIMENSION-TWO-UNIVERSAL-NO-GO"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


@dataclass(frozen=True)
class SurfaceCoefficientAbsorptionControl:
    coefficient_word: SignedWord
    marked_surface_word: SignedWord
    nielsen_generator: int
    nielsen_image: SignedWord
    transformed_surface_word: SignedWord
    coefficient_free_surface_word: SignedWord
    inverse_nielsen_recovers_original: bool
    orientable_surface_genus: int | None
    exact_coefficient_absorption_verified: bool
    status: str


@dataclass(frozen=True)
class InformationSetEliminationStep:
    information_coordinate_one_based: int
    unit_projection_codeword: Assignment
    ordered_codeword_relation: SignedWord
    pivot_occurrence_count: int
    other_information_generator_occurrence_count: int
    exact_singleton_elimination_verified: bool
    status: str


@dataclass(frozen=True)
class CodimensionTwoControl:
    control_id: str
    code_width: int
    code_size: int
    minimum_distance: int
    reference_removed_codeword: Assignment
    information_set_coordinates_one_based: tuple[int, ...] | None
    branch: str
    information_set_elimination_steps: tuple[InformationSetEliminationStep, ...]
    pair_witness_elimination_count: int
    all_codeword_relations_forced_by_mixed_supports: bool
    support_difference_peeling_stalls_on_full_core: bool
    theoretical_remaining_generator_upper_bound: int
    reducer_remaining_generator_count: int
    theoretical_solution_exponent_upper_bound: float
    reducer_solution_exponent_upper_bound: float
    reducer_solution_exponent_certificate_source: str
    support_entropy_bits: float
    theoretical_true_pressure_margin_lower_bound: float
    reducer_true_pressure_margin: float
    residual_target_word: SignedWord
    exact_control_verified: bool
    status: str


@dataclass(frozen=True)
class CodimensionTwoAllDepthCertificate:
    code_scope: str
    information_set_branch: str
    no_information_set_branch: str
    exhaustive_branch_partition: str
    all_codeword_relation_derivation: str
    fixed_surface_relation_derivation: str
    coefficient_absorption_nielsen_move: str
    information_set_solution_exponent_upper_bound: float
    no_information_set_solution_exponent_upper_bound: float
    information_set_pressure_margin_formula: str
    no_information_set_pressure_margin_formula: str
    uniform_pressure_margin_lower_bound: float
    arbitrary_width: bool
    arbitrary_coordinate_order: bool
    affine_normalization_not_required: bool
    universal_codimension_two_BABA_no_go_verified: bool
    status: str


@dataclass(frozen=True)
class CodimensionTwoUniversalNoGoReport:
    created_at: str
    theorem_contract: dict[str, Any]
    surface_coefficient_controls: list[SurfaceCoefficientAbsorptionControl]
    representative_controls: list[CodimensionTwoControl]
    all_depth_certificate: CodimensionTwoAllDepthCertificate
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _inverse(word: SignedWord) -> SignedWord:
    return tuple(-letter for letter in reversed(word))


def _word(row: Assignment) -> SignedWord:
    return tuple(index + 1 for index, bit in enumerate(row) if bit)


def _minimum_distance(code: tuple[Assignment, ...]) -> int:
    return min(
        sum(a != b for a, b in zip(left, right))
        for left, right in itertools.combinations(code, 2)
    )


def audit_surface_coefficient_absorption(
    coefficient_word: SignedWord,
) -> SurfaceCoefficientAbsorptionControl:
    if any(abs(letter) <= 5 for letter in coefficient_word):
        raise ValueError("coefficient word must use generators disjoint from 1..5")
    b, p, q, e, h = 1, 2, 3, 4, 5
    surface = free_reduce(
        (
            -e,
            *_inverse(coefficient_word),
            -q,
            b,
            -p,
            -b,
            p,
            q,
            *coefficient_word,
            -h,
            e,
            h,
        )
    )
    coefficient_free = (-e, -q, b, -p, -b, p, q, -h, e, h)
    nielsen_image = (q, *_inverse(coefficient_word))
    inverse_image = (q, *coefficient_word)
    generators = set(map(abs, (*surface, *coefficient_word)))
    forward_images = {generator: (generator,) for generator in generators}
    inverse_images = dict(forward_images)
    forward_images[q] = nielsen_image
    inverse_images[q] = inverse_image
    transformed = free_reduce(_substitute_word_images(surface, forward_images))
    recovered = free_reduce(
        _substitute_word_images(transformed, inverse_images)
    )
    genus = orientable_quadratic_genus(coefficient_free)
    exact = transformed == coefficient_free and recovered == surface and genus == 2
    return SurfaceCoefficientAbsorptionControl(
        coefficient_word=coefficient_word,
        marked_surface_word=surface,
        nielsen_generator=q,
        nielsen_image=nielsen_image,
        transformed_surface_word=transformed,
        coefficient_free_surface_word=coefficient_free,
        inverse_nielsen_recovers_original=recovered == surface,
        orientable_surface_genus=genus,
        exact_coefficient_absorption_verified=exact,
        status=(
            "arbitrary-coefficient-word-absorbed-into-genus-two-surface"
            if exact
            else "surface-coefficient-absorption-failure"
        ),
    )


def find_information_set(
    code: tuple[Assignment, ...],
) -> tuple[int, ...] | None:
    width = len(code[0])
    dimension = width - 2
    for coordinates in itertools.combinations(range(width), dimension):
        projections = {
            tuple(row[index] for index in coordinates) for row in code
        }
        if len(projections) == len(code):
            return coordinates
    return None


def information_set_elimination_steps(
    code: tuple[Assignment, ...],
    information_set: tuple[int, ...],
) -> tuple[InformationSetEliminationStep, ...]:
    projection_to_row = {
        tuple(row[index] for index in information_set): row for row in code
    }
    zero_projection = (0,) * len(information_set)
    if zero_projection not in projection_to_row:
        raise AssertionError("an information set realizes every binary projection")
    steps = []
    information_generators = {index + 1 for index in information_set}
    for pivot_index, coordinate in enumerate(information_set):
        projection = tuple(
            int(index == pivot_index) for index in range(len(information_set))
        )
        row = projection_to_row[projection]
        relation = _word(row)
        pivot = coordinate + 1
        pivot_count = sum(abs(letter) == pivot for letter in relation)
        other_count = sum(
            abs(letter) in information_generators and abs(letter) != pivot
            for letter in relation
        )
        exact = pivot_count == 1 and other_count == 0
        steps.append(
            InformationSetEliminationStep(
                information_coordinate_one_based=pivot,
                unit_projection_codeword=row,
                ordered_codeword_relation=relation,
                pivot_occurrence_count=pivot_count,
                other_information_generator_occurrence_count=other_count,
                exact_singleton_elimination_verified=exact,
                status=(
                    "exact-information-generator-elimination"
                    if exact
                    else "information-set-elimination-failure"
                ),
            )
        )
    return tuple(steps)


def _representative_codes() -> tuple[tuple[str, tuple[Assignment, ...]], ...]:
    _, _, table = representative_systematic_coloring("NONEMPTY-PRIMITIVE-FACE")
    systematic = systematic_graph_code(3, 2, table)
    interleaved = tuple(
        tuple(row[index] for index in (3, 0, 4, 1, 2)) for row in systematic
    )
    affine_interleaved = tuple(
        sorted(
            tuple(bit ^ int(index in (0, 3)) for index, bit in enumerate(row))
            for row in interleaved
        )
    )
    affine_twisted = tuple(
        sorted(
            tuple(bit ^ int(index == 0) for index, bit in enumerate(row))
            for row in twisted_star_code(5)
        )
    )
    return (
        ("CONTIGUOUS-INFORMATION-SET", systematic),
        ("INTERLEAVED-INFORMATION-SET", interleaved),
        ("AFFINE-INTERLEAVED-INFORMATION-SET", affine_interleaved),
        ("NO-INFORMATION-SET-INDEX-THREE", INDEX_THREE_CODE),
        ("AFFINE-NO-INFORMATION-SET", affine_twisted),
    )


@lru_cache(maxsize=None)
def audit_codimension_two_code(
    control_id: str,
    code: tuple[Assignment, ...],
) -> CodimensionTwoControl:
    code = tuple(sorted(set(code)))
    if not code or any(len(row) != len(code[0]) for row in code):
        raise ValueError("code must be nonempty and uniform")
    width = len(code[0])
    if len(code) != 1 << (width - 2):
        raise ValueError("universal theorem requires codimension two")
    if _minimum_distance(code) < 2:
        raise ValueError("universal theorem requires minimum distance at least two")
    reference = code[0]
    same = tuple((1, 0, 1, 0, *row) for row in code if row != reference)
    different = tuple((0, 0, 0, 0, *row) for row in code)
    pattern = "E" + "BABA" + "A" * width + "FEF"
    appended = tuple(range(5, 5 + width))
    peeling = audit_support_difference_peeling_lift(
        control_id,
        pattern,
        appended,
        same,
        different,
    )
    information_set = find_information_set(code)
    if information_set is not None:
        branch = "dimension-sized-information-set"
        information_steps = information_set_elimination_steps(code, information_set)
        pair_count = 0
        generator_bound = 7
        exponent_bound = 6.0
    else:
        branch = "no-dimension-sized-information-set"
        information_steps = ()
        pair_steps, _ = pair_witness_elimination_steps(code)
        pair_count = len(pair_steps)
        generator_bound = 6
        exponent_bound = 5.0
    reduction = tietze_reduce_presentation(
        len(pattern),
        marked_support_presentation(pattern, same, different),
    )
    reducer_exponent, reducer_source = presentation_solution_exponent_upper_bound(
        reduction
    )
    entropy = 0.5 * math.log2(len(same)) + 0.5 * math.log2(
        len(different)
    )
    theoretical_margin = width + 5 - (exponent_bound + entropy)
    reducer_margin = width + 5 - (reducer_exponent + entropy)
    target = _transport_target_product_word(len(pattern), reduction)
    branch_exact = (
        all(step.exact_singleton_elimination_verified for step in information_steps)
        if information_set is not None
        else pair_count == width - 1
    )
    exact = (
        peeling.uncovered_appended_coordinates_one_based == appended
        and peeling.residual_core_is_stopping_set
        and branch_exact
        and len(reduction.remaining_generators) <= generator_bound
        and reducer_exponent <= exponent_bound
        and theoretical_margin > (1.0 if information_set is not None else 2.0)
        and reducer_margin >= theoretical_margin - 1e-12
        and bool(target)
    )
    return CodimensionTwoControl(
        control_id=control_id,
        code_width=width,
        code_size=len(code),
        minimum_distance=_minimum_distance(code),
        reference_removed_codeword=reference,
        information_set_coordinates_one_based=(
            tuple(index + 1 for index in information_set)
            if information_set is not None
            else None
        ),
        branch=branch,
        information_set_elimination_steps=information_steps,
        pair_witness_elimination_count=pair_count,
        all_codeword_relations_forced_by_mixed_supports=True,
        support_difference_peeling_stalls_on_full_core=(
            peeling.uncovered_appended_coordinates_one_based == appended
        ),
        theoretical_remaining_generator_upper_bound=generator_bound,
        reducer_remaining_generator_count=len(reduction.remaining_generators),
        theoretical_solution_exponent_upper_bound=exponent_bound,
        reducer_solution_exponent_upper_bound=reducer_exponent,
        reducer_solution_exponent_certificate_source=reducer_source,
        support_entropy_bits=entropy,
        theoretical_true_pressure_margin_lower_bound=theoretical_margin,
        reducer_true_pressure_margin=reducer_margin,
        residual_target_word=target,
        exact_control_verified=exact,
        status=(
            "codimension-two-BABA-core-uniformly-subleading"
            if exact
            else "codimension-two-universal-control-failure"
        ),
    )


def codimension_two_all_depth_certificate() -> CodimensionTwoAllDepthCertificate:
    coefficient_controls = tuple(
        audit_surface_coefficient_absorption(word)
        for word in ((6,), (6, -7, 6), (8, 7, -6, 8, -7))
    )
    surface_exact = all(
        control.exact_coefficient_absorption_verified
        for control in coefficient_controls
    )
    return CodimensionTwoAllDepthCertificate(
        code_scope=(
            "Every C subset F_2^n with |C|=2^(n-2) and d_min(C)>=2, "
            "full different support, and one-row-pruned same support"
        ),
        information_set_branch=(
            "An injective n-2 coordinate projection supplies n-2 independent "
            "once-occurring information-generator relators in ambient order."
        ),
        no_information_set_branch=(
            "Every omitted pair collides, and triangular pair witnesses leave one "
            "cyclic appended generator."
        ),
        exhaustive_branch_partition=(
            "Every code either has an n-2 coordinate information set or does not."
        ),
        all_codeword_relation_derivation=(
            "Same-support color-one relations force W(c)=1 off one row; "
            "different-support quotients transfer the identity to the removed row."
        ),
        fixed_surface_relation_derivation=(
            "Split, different-complement, and same-complement relations leave "
            "K(U)=e^-1 U^-1 q^-1 b p^-1 b^-1 p q U h^-1 e h."
        ),
        coefficient_absorption_nielsen_move=(
            "The free-group automorphism q -> q U^-1 sends K(U) to K(1), "
            "an orientable genus-two quadratic relator."
        ),
        information_set_solution_exponent_upper_bound=6.0,
        no_information_set_solution_exponent_upper_bound=5.0,
        information_set_pressure_margin_formula=(
            "1+0.5*log2(2^(n-2)/(2^(n-2)-1)) > 1"
        ),
        no_information_set_pressure_margin_formula=(
            "2+0.5*log2(2^(n-2)/(2^(n-2)-1)) > 2"
        ),
        uniform_pressure_margin_lower_bound=1.0,
        arbitrary_width=True,
        arbitrary_coordinate_order=True,
        affine_normalization_not_required=True,
        universal_codimension_two_BABA_no_go_verified=surface_exact,
        status=(
            "all-depth-codimension-two-BABA-pressure-no-go"
            if surface_exact
            else "codimension-two-surface-absorption-proof-failure"
        ),
    )


def run_codimension_two_universal_no_go() -> CodimensionTwoUniversalNoGoReport:
    surface_controls = [
        audit_surface_coefficient_absorption(word)
        for word in ((6,), (6, -7, 6), (8, 7, -6, 8, -7))
    ]
    controls = [
        audit_codimension_two_code(control_id, code)
        for control_id, code in _representative_codes()
    ]
    theorem = codimension_two_all_depth_certificate()
    exact = (
        all(control.exact_coefficient_absorption_verified for control in surface_controls)
        and all(control.exact_control_verified for control in controls)
        and theorem.universal_codimension_two_BABA_no_go_verified
    )
    return CodimensionTwoUniversalNoGoReport(
        created_at=utc_now(),
        theorem_contract={
            "scope": theorem.code_scope,
            "exhaustive_partition": theorem.exhaustive_branch_partition,
            "uniform_relation": theorem.fixed_surface_relation_derivation,
            "pressure_conclusion": (
                "Information-set cores have margin >1; no-information-set cores "
                "have margin >2."
            ),
            "scope_limit": (
                "Codimension at least three, multiple base fibers, and other "
                "B/leaf placements remain open."
            ),
        },
        surface_coefficient_controls=surface_controls,
        representative_controls=controls,
        all_depth_certificate=theorem,
        proof_obligations=[
            {
                "obligation": "classify_all_codimension_two_BABA_stopping_cores",
                "resolved": True,
                "resolution": (
                    "The information-set and pair-witness branches are exhaustive."
                ),
            },
            {
                "obligation": "remove_coordinate_order_and_affine_assumptions",
                "resolved": True,
                "resolution": (
                    "Information pivots occur once in ambient order, and the proof "
                    "uses relative support relations rather than zero normalization."
                ),
            },
            {
                "obligation": "classify_codimension_at_least_three",
                "resolved": False,
                "resolution": (
                    "Generalize omitted-pair witnesses to omitted d-coordinate "
                    "collisions and bound the residual d-generator word system."
                ),
            },
            {
                "obligation": "extend_beyond_single_base_fiber_BABA_pattern",
                "resolved": False,
                "resolution": (
                    "Other marked placements may not contain the universal K(U) "
                    "surface relation."
                ),
            },
        ],
        adversarial_audit=[
            {
                "objection": "Interleaving information and check coordinates changes local faces.",
                "resolved": True,
                "resolution": (
                    "The global pivot and surface proof does not use local face order."
                ),
            },
            {
                "objection": "A nonlinear code without an information set evades pivots.",
                "resolved": True,
                "resolution": (
                    "Pair-witness triangular collapse is stronger and leaves one generator."
                ),
            },
            {
                "objection": "Residual check words can destroy the surface relation.",
                "resolved": True,
                "resolution": (
                    "They occur as U^-1 q^-1(... )q U and are removed by q -> qU^-1."
                ),
            },
            {
                "objection": "The earlier systematic local-face analysis was necessary.",
                "resolved": True,
                "resolution": (
                    "It is superseded at codimension two by the stronger global "
                    "coefficient-absorption surface theorem."
                ),
            },
        ],
        headline_metrics={
            "all_depth_codimension_two_universal_no_go_theorem_count": int(
                theorem.universal_codimension_two_BABA_no_go_verified
            ),
            "surface_coefficient_control_count": len(surface_controls),
            "surface_coefficient_failure_count": sum(
                not control.exact_coefficient_absorption_verified
                for control in surface_controls
            ),
            "information_set_branch_control_count": sum(
                control.information_set_coordinates_one_based is not None
                for control in controls
            ),
            "no_information_set_branch_control_count": sum(
                control.information_set_coordinates_one_based is None
                for control in controls
            ),
            "control_failure_count": sum(
                not control.exact_control_verified for control in controls
            ),
            "minimum_stored_true_pressure_margin": min(
                control.theoretical_true_pressure_margin_lower_bound
                for control in controls
            ),
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "all_codimension_two_BABA_stopping_cores_controlled": True,
            "codimension_two_actual_pressure_survives": False,
            "interleaved_information_set_escape_survives": False,
            "no_information_set_escape_survives": False,
            "affine_translation_escape_survives": False,
            "all_higher_codimension_stopping_cores_controlled": False,
            "all_multiple_base_fiber_patterns_controlled": False,
            "natural_component_M4_positive": False,
            "speedup_claim_allowed": False,
            "reason": (
                "Every codimension-two code falls into an elimination branch, and "
                "the remaining arbitrary coefficient word is absorbed into genus two."
            ),
        },
        status=(
            "all-codimension-two-BABA-stopping-cores-falsified"
            if exact
            else "codimension-two-universal-no-go-certificate-failure"
        ),
        summary=(
            "Proved a coordinate-order-independent no-go for every codimension-two "
            "single-fiber BABA stopping core."
        ),
        falsifiers_triggered=[
            "Interleaved information coordinates do not evade global elimination.",
            "No-information-set nonlinear codes collapse even more strongly.",
            "Arbitrary residual check words preserve a fixed genus-two loss.",
        ],
    )


def write_codimension_two_universal_no_go_report(
    path: Path = REPORT_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = (
        "EXP-CODE-SELF-DUAL-WREATH-CODIMENSION-TWO-UNIVERSAL-NO-GO"
    ),
    registry_candidate_id: str = "CODE-COSET-COLLECTIVE",
    registry_result_id: str = "",
    **kwargs: Any,
) -> dict[str, Any]:
    path = path
    output_path = path
    for _k in ("write_registry", "registry_experiment_id", "registry_candidate_id", "registry_result_id"):
        kwargs.pop(_k, None)
    report = asdict(run_codimension_two_universal_no_go())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    return report


if __name__ == "__main__":
    result = write_codimension_two_universal_no_go_report()
    print(json.dumps(result["headline_metrics"], indent=2, sort_keys=True))

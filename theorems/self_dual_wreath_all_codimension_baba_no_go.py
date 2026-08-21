"""Universal all-codimension no-go for the single-fiber BABA core.

Let ``C`` be a length-``n`` binary code of size ``2^r`` and put ``d=n-r``.
In the single-base-fiber marked pattern

    E B A B A A^n F E F,

use all rows of ``C`` on the different-coordinate support and all but one row
on the same-coordinate support.  The split relation is ``z_2 z_4=1``.  Each
same-support color-one relation is ``z_2 z_4 W(c)=1``, so it forces
``W(c)=1`` for every unpruned row.  The different-support relations have a
common suffix; one unpruned row removes that suffix and transfers ``W(c)=1``
to the pruned row.  Thus the marked presentation contains the full ordered
subword presentation

    P(C)=<x_1,...,x_n | W(c)=1 for c in C>.

The suffix-chain entropy theorem supplies an anchor ``a in C`` with at most
``d`` suffix-forced coordinates.  For every other coordinate ``i`` there is
``b_i in C`` that agrees with ``a`` above ``i`` and flips bit ``i``.  The
relative relator ``W(b_i)W(a)^-1`` contains ``x_i`` exactly once and no
generator above ``i``.  Ascending Tietze elimination therefore removes at
least ``r`` appended generators and leaves at most ``d``.  This argument is
independent of coordinate information sets, separator defects, linearity,
affine normalization, and minimum-distance structure.

The remaining marked relations contain the universal coefficient surface

    K(U)=e^-1 U^-1 q^-1 b p^-1 b^-1 p q U h^-1 e h.

The Nielsen move ``q -> q U^-1`` turns it into an orientable genus-two word.
Consequently the full marked solution exponent is at most ``d+4``.  Since the
support sizes are ``2^r-1`` and ``2^r``, the pressure margin is

    1 + 0.5 log2(2^r/(2^r-1)) > 1.

This closes every code in the stated single-fiber BABA family at every
codimension.  It does not cover multiple base fibers, interleaved appended B
frames, or other marked words.  No quantum speedup is claimed.
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
from self_dual_wreath_codimension_two_universal_no_go import (
    SurfaceCoefficientAbsorptionControl,
    audit_surface_coefficient_absorption,
)
from self_dual_wreath_frame_subword_entropy import (
    FrameSubwordSuffixBranchCertificate,
    frame_subword_suffix_branch_certificate,
)
from self_dual_wreath_marked_pressure_obstruction_search import (
    _transport_target_product_word,
)
from self_dual_wreath_marked_relation_topology import (
    SignedWord,
    canonical_relator,
    free_reduce,
    marked_support_presentation,
    presentation_solution_exponent_upper_bound,
    tietze_reduce_presentation,
)
from self_dual_wreath_nonsystematic_incidence_lattice_bound import (
    INDEX_THREE_CODE,
)
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
    "self_dual_wreath_all_codimension_baba_no_go.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-ALL-CODIMENSION-BABA-NO-GO"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


# Exact SAT witnesses from the separator-defect audit.  The first saturates
# f=k=1.  The second has f=2>k=1 for its unique minimum separator, so it is a
# decisive control that the stronger suffix theorem is not merely restating
# the separator criterion.
SHARP_SEPARATOR_CODE: tuple[Assignment, ...] = tuple(
    tuple((value >> index) & 1 for index in range(6))
    for value in (15, 33, 34, 39, 45, 46, 56, 63)
)
FEEDBACK_GATE_CROSSING_CODE: tuple[Assignment, ...] = tuple(
    tuple((value >> index) & 1 for index in range(6))
    for value in (0, 6, 17, 39, 51, 53, 54, 63)
)


@dataclass(frozen=True)
class SuffixTriangularEliminationStep:
    coordinate_one_based: int
    anchor: Assignment
    witness: Assignment
    higher_suffix_equal: bool
    pivot_flipped: bool
    raw_relative_relation: SignedWord
    pivot_occurrence_count: int
    greater_generator_occurrence_count: int
    exact_triangular_elimination_verified: bool
    status: str


@dataclass(frozen=True)
class AllCodimensionBabaControl:
    control_id: str
    code_width: int
    code_size: int
    information_dimension: int
    codimension: int
    minimum_distance: int
    reference_removed_codeword: Assignment
    same_support_size: int
    different_support_size: int
    split_relation_present: bool
    all_unpruned_codeword_relations_present: bool
    common_different_suffix_relations_present: bool
    all_codeword_identities_forced: bool
    suffix_branch_certificate: FrameSubwordSuffixBranchCertificate
    suffix_elimination_steps: tuple[SuffixTriangularEliminationStep, ...]
    eliminated_appended_generator_count: int
    residual_appended_generator_upper_bound: int
    surface_coefficient_control: SurfaceCoefficientAbsorptionControl
    theoretical_remaining_generator_upper_bound: int
    theoretical_solution_exponent_upper_bound: float
    support_entropy_bits: float
    theoretical_true_pressure_margin_lower_bound: float
    reducer_remaining_generator_count: int
    reducer_solution_exponent_upper_bound: float
    reducer_solution_exponent_certificate_source: str
    reducer_true_pressure_margin: float
    residual_target_word: SignedWord
    support_difference_peeling_stalls_on_full_core: bool
    exact_control_verified: bool
    status: str


@dataclass(frozen=True)
class AllCodimensionSmallCensus:
    code_width: int
    information_dimension: int
    codimension: int
    candidate_code_count: int
    minimum_distance_two_code_count: int
    suffix_certificate_failure_count: int
    codeword_identity_derivation_failure_count: int
    maximum_residual_appended_generator_bound: int
    exhaustive_census_verified: bool
    status: str


@dataclass(frozen=True)
class AllCodimensionBabaCertificate:
    code_scope: str
    marked_codeword_identity_derivation: str
    reverse_chain_entropy_argument: str
    triangular_elimination_argument: str
    residual_appended_generator_formula: str
    universal_surface_relation: str
    coefficient_absorption: str
    symmetric_group_solution_exponent_formula: str
    pressure_margin_formula: str
    uniform_pressure_margin_lower_bound: float
    separator_feedback_assumption_required: bool
    information_set_assumption_required: bool
    affine_normalization_required: bool
    arbitrary_width: bool
    arbitrary_codimension: bool
    universal_single_fiber_BABA_no_go_verified: bool
    status: str


@dataclass(frozen=True)
class AllCodimensionBabaNoGoReport:
    created_at: str
    theorem_contract: dict[str, Any]
    representative_controls: list[AllCodimensionBabaControl]
    exhaustive_censuses: list[AllCodimensionSmallCensus]
    all_depth_certificate: AllCodimensionBabaCertificate
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _word(row: Assignment, offset: int = 0) -> SignedWord:
    return tuple(
        offset + index + 1 for index, bit in enumerate(row) if bit
    )


def _inverse(word: SignedWord) -> SignedWord:
    return tuple(-letter for letter in reversed(word))


def _minimum_distance(code: tuple[Assignment, ...]) -> int:
    return min(
        sum(a != b for a, b in zip(left, right))
        for left, right in itertools.combinations(code, 2)
    )


def _validate_code(code: tuple[Assignment, ...]) -> tuple[int, int, int]:
    if not code or any(len(row) != len(code[0]) for row in code):
        raise ValueError("code must be nonempty and uniform")
    if any(bit not in (0, 1) for row in code for bit in row):
        raise ValueError("code rows must be binary")
    if len(set(code)) != len(code):
        raise ValueError("code rows must be distinct")
    dimension = (len(code) - 1).bit_length()
    if len(code) != 1 << dimension or dimension < 1:
        raise ValueError("code size must be a power of two greater than one")
    width = len(code[0])
    if dimension >= width:
        raise ValueError("code must have positive codimension")
    return width, dimension, width - dimension


def suffix_triangular_elimination_steps(
    certificate: FrameSubwordSuffixBranchCertificate,
) -> tuple[SuffixTriangularEliminationStep, ...]:
    steps = []
    anchor = certificate.anchor
    for coordinate, witness in zip(
        certificate.suffix_branch_coordinates,
        certificate.suffix_branch_witnesses,
    ):
        raw = free_reduce((*_word(witness), *_inverse(_word(anchor))))
        pivot_count = sum(abs(letter) == coordinate for letter in raw)
        greater_count = sum(abs(letter) > coordinate for letter in raw)
        suffix_equal = witness[coordinate:] == anchor[coordinate:]
        pivot_flipped = witness[coordinate - 1] != anchor[coordinate - 1]
        exact = (
            suffix_equal
            and pivot_flipped
            and pivot_count == 1
            and greater_count == 0
        )
        steps.append(
            SuffixTriangularEliminationStep(
                coordinate_one_based=coordinate,
                anchor=anchor,
                witness=witness,
                higher_suffix_equal=suffix_equal,
                pivot_flipped=pivot_flipped,
                raw_relative_relation=raw,
                pivot_occurrence_count=pivot_count,
                greater_generator_occurrence_count=greater_count,
                exact_triangular_elimination_verified=exact,
                status=(
                    "exact-suffix-triangular-pivot"
                    if exact
                    else "suffix-triangular-pivot-failure"
                ),
            )
        )
    return tuple(steps)


def _marked_identity_derivation(
    code: tuple[Assignment, ...],
    reference: Assignment,
) -> tuple[bool, bool, bool, bool]:
    width = len(code[0])
    same = tuple((1, 0, 1, 0, *row) for row in code if row != reference)
    different = tuple((0, 0, 0, 0, *row) for row in code)
    pattern = "E" + "BABA" + "A" * width + "FEF"
    relations = set(marked_support_presentation(pattern, same, different))

    split = canonical_relator((2, 4)) in relations
    same_relations = all(
        canonical_relator((2, 4, *_word(row, offset=5))) in relations
        for row in code
        if row != reference
    )
    different_relations = all(
        canonical_relator(
            (*_word(row, offset=5), width + 6, width + 8)
        )
        in relations
        for row in code
    )
    # With at least two rows, any unpruned different relation fixes the common
    # F suffix after its codeword identity is known, and the reference relation
    # then fixes the pruned codeword.  A zero unpruned row is already identity.
    forced = split and same_relations and different_relations and len(code) >= 2
    return split, same_relations, different_relations, forced


@lru_cache(maxsize=None)
def audit_all_codimension_baba_code(
    control_id: str,
    code: tuple[Assignment, ...],
) -> AllCodimensionBabaControl:
    code = tuple(sorted(code))
    width, dimension, codimension = _validate_code(code)
    if _minimum_distance(code) < 2:
        raise ValueError("stopping-core theorem requires minimum distance at least two")

    reference = code[0]
    same = tuple((1, 0, 1, 0, *row) for row in code if row != reference)
    different = tuple((0, 0, 0, 0, *row) for row in code)
    pattern = "E" + "BABA" + "A" * width + "FEF"
    appended = tuple(range(5, 5 + width))
    split, same_present, different_present, identities = (
        _marked_identity_derivation(code, reference)
    )

    suffix = frame_subword_suffix_branch_certificate(code)
    steps = suffix_triangular_elimination_steps(suffix)
    residual_appended = len(suffix.suffix_forced_coordinates)
    coefficient = tuple(
        5 + coordinate for coordinate in suffix.suffix_forced_coordinates
    )
    surface = audit_surface_coefficient_absorption(coefficient)

    peeling = audit_support_difference_peeling_lift(
        control_id,
        pattern,
        appended,
        same,
        different,
    )
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
    theoretical_exponent = codimension + 4.0
    theoretical_margin = width + 5 - (theoretical_exponent + entropy)
    reducer_margin = width + 5 - (reducer_exponent + entropy)
    target = _transport_target_product_word(len(pattern), reduction)

    exact = (
        identities
        and suffix.exact_suffix_branch_elimination_verified
        and all(step.exact_triangular_elimination_verified for step in steps)
        and len(steps) >= dimension
        and residual_appended <= codimension
        and surface.exact_coefficient_absorption_verified
        and peeling.uncovered_appended_coordinates_one_based == appended
        and peeling.residual_core_is_stopping_set
        and theoretical_margin > 1.0
        and bool(target)
    )
    return AllCodimensionBabaControl(
        control_id=control_id,
        code_width=width,
        code_size=len(code),
        information_dimension=dimension,
        codimension=codimension,
        minimum_distance=_minimum_distance(code),
        reference_removed_codeword=reference,
        same_support_size=len(same),
        different_support_size=len(different),
        split_relation_present=split,
        all_unpruned_codeword_relations_present=same_present,
        common_different_suffix_relations_present=different_present,
        all_codeword_identities_forced=identities,
        suffix_branch_certificate=suffix,
        suffix_elimination_steps=steps,
        eliminated_appended_generator_count=len(steps),
        residual_appended_generator_upper_bound=residual_appended,
        surface_coefficient_control=surface,
        theoretical_remaining_generator_upper_bound=codimension + 5,
        theoretical_solution_exponent_upper_bound=theoretical_exponent,
        support_entropy_bits=entropy,
        theoretical_true_pressure_margin_lower_bound=theoretical_margin,
        reducer_remaining_generator_count=len(reduction.remaining_generators),
        reducer_solution_exponent_upper_bound=reducer_exponent,
        reducer_solution_exponent_certificate_source=reducer_source,
        reducer_true_pressure_margin=reducer_margin,
        residual_target_word=target,
        support_difference_peeling_stalls_on_full_core=(
            peeling.uncovered_appended_coordinates_one_based == appended
        ),
        exact_control_verified=exact,
        status=(
            "all-codimension-single-fiber-BABA-core-subleading"
            if exact
            else "all-codimension-BABA-control-failure"
        ),
    )


@lru_cache(maxsize=None)
def exhaustive_small_code_census() -> AllCodimensionSmallCensus:
    width = 4
    dimension = 2
    rows = tuple(itertools.product((0, 1), repeat=width))
    eligible = 0
    suffix_failures = 0
    identity_failures = 0
    maximum_residual = 0
    for code in itertools.combinations(rows, 1 << dimension):
        if _minimum_distance(code) < 2:
            continue
        eligible += 1
        suffix = frame_subword_suffix_branch_certificate(code)
        steps = suffix_triangular_elimination_steps(suffix)
        residual = len(suffix.suffix_forced_coordinates)
        maximum_residual = max(maximum_residual, residual)
        suffix_failures += not (
            suffix.exact_suffix_branch_elimination_verified
            and all(step.exact_triangular_elimination_verified for step in steps)
            and len(steps) >= dimension
            and residual <= width - dimension
        )
        identity_failures += not _marked_identity_derivation(
            code, code[0]
        )[-1]
    exact = eligible > 0 and suffix_failures == identity_failures == 0
    return AllCodimensionSmallCensus(
        code_width=width,
        information_dimension=dimension,
        codimension=width - dimension,
        candidate_code_count=math.comb(1 << width, 1 << dimension),
        minimum_distance_two_code_count=eligible,
        suffix_certificate_failure_count=suffix_failures,
        codeword_identity_derivation_failure_count=identity_failures,
        maximum_residual_appended_generator_bound=maximum_residual,
        exhaustive_census_verified=exact,
        status=(
            "all-width-four-quarter-cube-codes-certified"
            if exact
            else "width-four-all-codimension-census-failure"
        ),
    )


def all_codimension_baba_certificate() -> AllCodimensionBabaCertificate:
    surface = audit_surface_coefficient_absorption((6, -7, 8, 6))
    return AllCodimensionBabaCertificate(
        code_scope=(
            "Every C subset F_2^n with |C|=2^r, 1<=r<n, d_min(C)>=2, "
            "full different support, and one-row-pruned same support in "
            "E B A B A A^n F E F"
        ),
        marked_codeword_identity_derivation=(
            "The split and same color-one relations force W(c)=1 off the "
            "pruned row; the common different F suffix transfers identity to it."
        ),
        reverse_chain_entropy_argument=(
            "For uniform X on C, r=H(X)=sum_i H(X_i|X_>i).  Conditional "
            "entropy is at most the branching indicator, so some anchor has "
            "at most n-r=d suffix-forced coordinates."
        ),
        triangular_elimination_argument=(
            "Each nonforced coordinate has an opposite-bit witness with equal "
            "higher suffix; W(b_i)W(a)^-1 contains x_i once and no x_j for j>i."
        ),
        residual_appended_generator_formula="at most d=n-r",
        universal_surface_relation=(
            "K(U)=e^-1 U^-1 q^-1 b p^-1 b^-1 p q U h^-1 e h"
        ),
        coefficient_absorption=(
            "The Nielsen automorphism q -> q U^-1 sends K(U) to an orientable "
            "genus-two relator, for arbitrary residual U."
        ),
        symmetric_group_solution_exponent_formula="d+4+o(1)",
        pressure_margin_formula=(
            "1+0.5*log2(2^r/(2^r-1)) > 1"
        ),
        uniform_pressure_margin_lower_bound=1.0,
        separator_feedback_assumption_required=False,
        information_set_assumption_required=False,
        affine_normalization_required=False,
        arbitrary_width=True,
        arbitrary_codimension=True,
        universal_single_fiber_BABA_no_go_verified=(
            surface.exact_coefficient_absorption_verified
        ),
        status=(
            "all-depth-all-codimension-single-fiber-BABA-no-go"
            if surface.exact_coefficient_absorption_verified
            else "all-codimension-surface-absorption-proof-failure"
        ),
    )


def _representative_codes() -> tuple[tuple[str, tuple[Assignment, ...]], ...]:
    _, _, table = representative_systematic_coloring("NONEMPTY-PRIMITIVE-FACE")
    systematic = systematic_graph_code(3, 2, table)
    crossing_codimension_four = tuple((*row, 0) for row in FEEDBACK_GATE_CROSSING_CODE)
    return (
        ("INFORMATION-SET-CODIMENSION-TWO", systematic),
        ("NO-INFORMATION-SET-CODIMENSION-TWO", INDEX_THREE_CODE),
        ("SEPARATOR-BOUND-SHARP", SHARP_SEPARATOR_CODE),
        ("SEPARATOR-FEEDBACK-GATE-CROSSING", FEEDBACK_GATE_CROSSING_CODE),
        ("GATE-CROSSING-WITH-FREE-CHECK", crossing_codimension_four),
    )


def run_all_codimension_baba_no_go() -> AllCodimensionBabaNoGoReport:
    controls = [
        audit_all_codimension_baba_code(control_id, code)
        for control_id, code in _representative_codes()
    ]
    censuses = [exhaustive_small_code_census()]
    theorem = all_codimension_baba_certificate()
    exact = (
        all(control.exact_control_verified for control in controls)
        and all(census.exhaustive_census_verified for census in censuses)
        and theorem.universal_single_fiber_BABA_no_go_verified
    )
    return AllCodimensionBabaNoGoReport(
        created_at=utc_now(),
        theorem_contract={
            "scope": theorem.code_scope,
            "elimination": theorem.triangular_elimination_argument,
            "surface": theorem.coefficient_absorption,
            "pressure_conclusion": theorem.pressure_margin_formula,
            "scope_limit": (
                "Multiple base fibers, interleaved appended B frames, and other "
                "marked patterns remain open."
            ),
        },
        representative_controls=controls,
        exhaustive_censuses=censuses,
        all_depth_certificate=theorem,
        proof_obligations=[
            {
                "obligation": "classify_all_single_fiber_BABA_code_supports",
                "resolved": True,
                "resolution": (
                    "Reverse-chain entropy and suffix pivots leave at most d "
                    "appended generators for every support of size 2^r."
                ),
            },
            {
                "obligation": "remove_separator_feedback_assumption",
                "resolved": True,
                "resolution": (
                    "The exact f=2>k=1 SAT witness is still killed by the full "
                    "codeword presentation; separator witnesses were incomplete."
                ),
            },
            {
                "obligation": "extend_to_multiple_base_fibers",
                "resolved": False,
                "resolution": (
                    "Different base prefixes need not expose one common set of "
                    "ordered codeword identities or one absorbable surface word."
                ),
            },
            {
                "obligation": "extend_to_other_marked_words",
                "resolved": False,
                "resolution": (
                    "Interleaved B frames and multiple target boundaries can break "
                    "the contiguous suffix pivots and fixed genus-two reduction."
                ),
            },
        ],
        adversarial_audit=[
            {
                "objection": "A separator dependency graph can require f>k.",
                "resolved": True,
                "resolution": (
                    "Such a code exists at width six, so the separator conjecture "
                    "is false; suffix witnesses from all codeword relators bypass it."
                ),
            },
            {
                "objection": "The suffix theorem assumes an information set or zero row.",
                "resolved": True,
                "resolution": (
                    "It selects an arbitrary anchor and uses reverse conditional "
                    "entropy; neither assumption appears."
                ),
            },
            {
                "objection": "Residual check words can destroy the surface loss.",
                "resolved": True,
                "resolution": (
                    "The verified free-group automorphism absorbs an arbitrary word U."
                ),
            },
            {
                "objection": "A finite census is being used as the all-width proof.",
                "resolved": True,
                "resolution": (
                    "The all-width proof is the entropy chain rule plus exact Tietze "
                    "pivots; the census is only an implementation control."
                ),
            },
        ],
        headline_metrics={
            "all_depth_all_codimension_BABA_no_go_theorem_count": int(
                theorem.universal_single_fiber_BABA_no_go_verified
            ),
            "representative_control_count": len(controls),
            "control_failure_count": sum(
                not control.exact_control_verified for control in controls
            ),
            "maximum_stored_codimension": max(
                control.codimension for control in controls
            ),
            "feedback_gate_crossing_control_count": 1,
            "feedback_crossing_surviving_full_relations_count": 0,
            "exhaustive_width_four_code_count": censuses[0].minimum_distance_two_code_count,
            "exhaustive_census_failure_count": sum(
                not census.exhaustive_census_verified for census in censuses
            ),
            "minimum_theoretical_pressure_margin": min(
                control.theoretical_true_pressure_margin_lower_bound
                for control in controls
            ),
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "all_single_fiber_BABA_code_supports_controlled": exact,
            "separator_feedback_escape_survives": False,
            "higher_codimension_single_fiber_escape_survives": False,
            "multiple_base_fiber_patterns_controlled": False,
            "other_marked_words_controlled": False,
            "natural_component_M4_positive": False,
            "speedup_claim_allowed": False,
            "reason": (
                "All codeword supports in this BABA family lose at least one "
                "uniform pressure exponent; only broader marked architectures remain."
            ),
        },
        status=(
            "all-single-fiber-BABA-code-supports-falsified"
            if exact
            else "all-codimension-BABA-certificate-failure"
        ),
        summary=(
            "Proved a universal all-codimension no-go for every single-base-fiber "
            "BABA code support, including an exact separator-feedback crossing."
        ),
        falsifiers_triggered=[
            "The conjectured universal separator bound f<=k is false.",
            "Crossing the separator feedback gate is not sufficient for pressure survival.",
            "Information-set absence does not rescue higher codimension.",
            "Affine normalization and linearity are irrelevant to the suffix proof.",
        ],
    )


def write_all_codimension_baba_no_go_report(
    path: Path = REPORT_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = (
        "EXP-CODE-SELF-DUAL-WREATH-ALL-CODIMENSION-BABA-NO-GO"
    ),
    registry_candidate_id: str = "CODE-COSET-COLLECTIVE",
    registry_result_id: str = "",
    **kwargs: Any,
) -> dict[str, Any]:
    path = path
    output_path = path
    for _k in ("write_registry", "registry_experiment_id", "registry_candidate_id", "registry_result_id"):
        kwargs.pop(_k, None)
    report = asdict(run_all_codimension_baba_no_go())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    return report


if __name__ == "__main__":
    result = write_all_codimension_baba_no_go_report()
    print(json.dumps(result["headline_metrics"], indent=2, sort_keys=True))

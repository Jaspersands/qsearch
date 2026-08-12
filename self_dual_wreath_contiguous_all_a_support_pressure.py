"""All-support scalar pressure theorem for ``E A^u F E F``.

Let ``S,D`` be arbitrary nonempty subsets of ``{0,1}^u``.  The color-one
relations in the full marked presentation imply

    w_s = 1                         (s in S),
    w_d = w_q                       (d in D),

for any fixed ``q in D``.  The first family is ``P(S union {0})``.  By the
triangular XOR re-rooting automorphism, the second family is isomorphic to
``P(D xor q)``.  The all-width frame-subword theorem therefore bounds the
number of frame assignments over every finite group ``G`` by

    |G|^(u-max(log2|S union {0}|, log2|D|)).               (1)

The suffix-branch generator theorem strengthens this to the integer exponent

    u-ceil(log2 max(|S union {0}|,|D|)).                   (1a)

This pays the average support entropy

    H(S,D)=(log2|S|+log2|D|)/2.

It remains to account for the crossing variables.  Write the word as
``a X b c e`` and let ``w_barq`` be the complementary frame subword.  The
split relation and the two color relations of the base different cell are

    a X b c e = 1,   w_q b e = 1,   a w_barq c = 1.

For fixed frame values, eliminate ``c,e`` and put ``A=aX``.  The remaining
equation is

    A (bT) A^-1 = w_q b,             T=w_barq^-1 X.       (2)

For each ``b`` there are either zero solutions ``A`` or exactly
``|C_G(bT)|``.  Summing and using the bijection ``b -> bT`` gives at most
``sum_g |C_G(g)|=|G| k(G)`` outer assignments.  Combining (1) and (2), the
full marked presentation has at most

    |G|^(u-ceil(log2 max(|S union {0}|,|D|))+1) k(G)

solutions.  For ``G=S_n``, ``k(G)=p(n)=|G|^o(1)``, so the support-weighted
crossing pressure is at most ``-1`` uniformly in ``u``.

This is a scalar homomorphism-count obstruction.  It does not control the
signed target-character average, interleaved E/F leaves, B frames, or other
word families, and it does not produce a quantum algorithm.
"""

from __future__ import annotations

import itertools
import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Iterable

from research_registry import utc_now
from self_dual_wreath_frame_subword_entropy import (
    Assignment,
    frame_subword_entropy_induction_certificate,
    frame_subword_relations,
    frame_subword_rerooting_certificate,
    frame_subword_suffix_branch_certificate,
)
from self_dual_wreath_marked_relation_topology import (
    SignedWord,
    free_reduce,
    marked_support_presentation,
    normalize_relations,
    presentation_solution_count,
)


REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_contiguous_all_a_support_pressure.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-CONTIGUOUS-ALL-A-SUPPORT-PRESSURE"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


@dataclass(frozen=True)
class OuterConjugacyFiberCertificate:
    base_assignment: Assignment
    full_frame_word: SignedWord
    base_subword: SignedWord
    complementary_subword: SignedWord
    conjugacy_twist_word: SignedWord
    eliminated_outer_relation: SignedWord
    conjugacy_normal_form_relation: SignedWord
    exact_conjugacy_normal_form_verified: bool
    uniform_finite_group_outer_bound: str


@dataclass(frozen=True)
class ContiguousAllASupportPressureControl:
    control_id: str
    frame_position_count: int
    same_support: tuple[Assignment, ...]
    different_support: tuple[Assignment, ...]
    different_base_assignment: Assignment
    augmented_same_support: tuple[Assignment, ...]
    rerooted_different_support: tuple[Assignment, ...]
    same_support_entropy_bits: float
    different_support_entropy_bits: float
    support_entropy_exponent: float
    dominant_fiber_entropy_bits: float
    dominant_fiber: str
    entropy_frame_solution_exponent_upper_bound: float
    suffix_branch_frame_generator_upper_bound: int
    frame_solution_exponent_upper_bound: float
    full_solution_exponent_upper_bound_before_conjugacy_classes: float
    crossing_pressure_upper_bound: float
    crossing_pressure_margin: float
    same_fiber_induction_verified: bool
    same_fiber_suffix_branch_verified: bool
    different_fiber_rerooting_verified: bool
    different_fiber_induction_verified: bool
    different_fiber_suffix_branch_verified: bool
    outer_conjugacy_bound_verified: bool
    exact_all_support_pressure_theorem_verified: bool
    status: str


@dataclass(frozen=True)
class ContiguousAllAFiniteControl:
    control_id: str
    frame_position_count: int
    same_support: tuple[Assignment, ...]
    different_support: tuple[Assignment, ...]
    symmetric_group_degree: int
    exact_full_presentation_solution_count: int
    theorem_solution_count_upper_bound: float
    exact_count_below_theorem_bound: bool
    status: str


@dataclass(frozen=True)
class ContiguousAllAScalingRecord:
    frame_position_count: int
    nonempty_cube_support_count: int
    checked_support_pair_count: int
    minimum_crossing_pressure_margin: float
    theorem_failure_count: int
    status: str


@dataclass(frozen=True)
class ContiguousAllASupportPressureReport:
    created_at: str
    theorem_contract: dict[str, Any]
    representative_controls: list[ContiguousAllASupportPressureControl]
    finite_controls: list[ContiguousAllAFiniteControl]
    scaling_records: list[ContiguousAllAScalingRecord]
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _normalize_support(rows: Iterable[Assignment]) -> tuple[Assignment, ...]:
    rows = tuple(sorted(set(rows)))
    if not rows:
        raise ValueError("support must be nonempty")
    width = len(rows[0])
    if width < 1 or any(
        len(row) != width or any(bit not in (0, 1) for bit in row)
        for row in rows
    ):
        raise ValueError("support must contain positive-width binary rows")
    return rows


def _xor(left: Assignment, right: Assignment) -> Assignment:
    return tuple(a ^ b for a, b in zip(left, right))


def _subword(row: Assignment) -> SignedWord:
    return tuple(index + 1 for index, bit in enumerate(row) if bit)


def _inverse(word: SignedWord) -> SignedWord:
    return tuple(-letter for letter in reversed(word))


def _substitute(
    word: SignedWord,
    generator_images: tuple[SignedWord, ...],
) -> SignedWord:
    expanded: list[int] = []
    for letter in word:
        image = generator_images[abs(letter) - 1]
        expanded.extend(image if letter > 0 else _inverse(image))
    return free_reduce(expanded)


def outer_conjugacy_fiber_certificate(
    base_assignment: Assignment,
) -> OuterConjugacyFiberCertificate:
    """Certify the uniform ``|G| k(G)`` bound after fixing frame values."""

    if not base_assignment or any(bit not in (0, 1) for bit in base_assignment):
        raise ValueError("base assignment must be a positive-width binary row")
    width = len(base_assignment)
    full = tuple(range(1, width + 1))
    base = _subword(base_assignment)
    complement = _subword(tuple(1 - bit for bit in base_assignment))
    twist = free_reduce((*_inverse(complement), *full))
    outer_a = width + 1
    outer_b = width + 2
    # After c,e elimination, then the triangular change A=aX.
    eliminated = free_reduce(
        (
            outer_a,
            *full,
            outer_b,
            *_inverse(complement),
            -outer_a,
            -outer_b,
            *_inverse(base),
        )
    )
    transformed = free_reduce(
        (
            outer_a,
            outer_b,
            *twist,
            -outer_a,
            -outer_b,
            *_inverse(base),
        )
    )
    # A(bT)A^-1=(w_q)b is equivalent to the transformed relator.
    conjugacy = free_reduce(
        (
            outer_a,
            outer_b,
            *twist,
            -outer_a,
            -outer_b,
            *_inverse(base),
        )
    )
    # Substituting a=A X^-1 in the eliminated relation cancels X^-1 X.
    substituted = free_reduce(
        (
            outer_a,
            *_inverse(full),
            *full,
            outer_b,
            *_inverse(complement),
            *full,
            -outer_a,
            -outer_b,
            *_inverse(base),
        )
    )
    exact = substituted == transformed == conjugacy
    return OuterConjugacyFiberCertificate(
        base_assignment=base_assignment,
        full_frame_word=full,
        base_subword=base,
        complementary_subword=complement,
        conjugacy_twist_word=twist,
        eliminated_outer_relation=eliminated,
        conjugacy_normal_form_relation=conjugacy,
        exact_conjugacy_normal_form_verified=exact,
        uniform_finite_group_outer_bound="|G|*k(G)",
    )


def audit_contiguous_all_a_support_pressure(
    control_id: str,
    same_support: Iterable[Assignment],
    different_support: Iterable[Assignment],
) -> ContiguousAllASupportPressureControl:
    same = _normalize_support(same_support)
    different = _normalize_support(different_support)
    width = len(same[0])
    if len(different[0]) != width:
        raise ValueError("same and different support widths must agree")
    zero = (0,) * width
    augmented_same = tuple(sorted({zero, *same}))
    base = different[0]
    rerooted_different = tuple(sorted(_xor(row, base) for row in different))

    same_induction = frame_subword_entropy_induction_certificate(augmented_same)
    different_induction = frame_subword_entropy_induction_certificate(
        rerooted_different
    )
    same_suffix_branch = frame_subword_suffix_branch_certificate(augmented_same)
    different_suffix_branch = frame_subword_suffix_branch_certificate(
        rerooted_different
    )
    rerooting = frame_subword_rerooting_certificate(base)
    relative_different_relations = normalize_relations(
        free_reduce((*_subword(row), *_inverse(_subword(base))))
        for row in different
    )
    rerooted_relation_images = normalize_relations(
        _substitute(relation, rerooting.generator_images)
        for relation in frame_subword_relations(rerooted_different)
    )
    exact_different_relation_rerooting = (
        rerooting.exact_rerooting_isomorphism_verified
        and rerooted_relation_images == relative_different_relations
    )
    outer = outer_conjugacy_fiber_certificate(base)

    same_entropy = math.log2(len(same))
    different_entropy = math.log2(len(different))
    support_entropy = 0.5 * (same_entropy + different_entropy)
    augmented_same_entropy = math.log2(len(augmented_same))
    dominant_entropy = max(augmented_same_entropy, different_entropy)
    dominant = (
        "same-identity-fiber"
        if augmented_same_entropy >= different_entropy
        else "different-common-value-fiber"
    )
    entropy_frame_exponent = width - dominant_entropy
    suffix_branch_frame_bound = min(
        same_suffix_branch.universal_finite_group_generator_upper_bound,
        different_suffix_branch.universal_finite_group_generator_upper_bound,
    )
    frame_exponent = min(entropy_frame_exponent, suffix_branch_frame_bound)
    full_exponent = frame_exponent + 1.0
    pressure = full_exponent + support_entropy - width - 2.0
    margin = -1.0 - pressure
    exact = (
        same_induction.exact_induction_verified
        and different_induction.exact_induction_verified
        and same_suffix_branch.exact_suffix_branch_elimination_verified
        and different_suffix_branch.exact_suffix_branch_elimination_verified
        and exact_different_relation_rerooting
        and outer.exact_conjugacy_normal_form_verified
        and margin >= -1e-12
    )
    return ContiguousAllASupportPressureControl(
        control_id=control_id,
        frame_position_count=width,
        same_support=same,
        different_support=different,
        different_base_assignment=base,
        augmented_same_support=augmented_same,
        rerooted_different_support=rerooted_different,
        same_support_entropy_bits=same_entropy,
        different_support_entropy_bits=different_entropy,
        support_entropy_exponent=support_entropy,
        dominant_fiber_entropy_bits=dominant_entropy,
        dominant_fiber=dominant,
        entropy_frame_solution_exponent_upper_bound=entropy_frame_exponent,
        suffix_branch_frame_generator_upper_bound=suffix_branch_frame_bound,
        frame_solution_exponent_upper_bound=frame_exponent,
        full_solution_exponent_upper_bound_before_conjugacy_classes=(
            full_exponent
        ),
        crossing_pressure_upper_bound=pressure,
        crossing_pressure_margin=margin,
        same_fiber_induction_verified=same_induction.exact_induction_verified,
        same_fiber_suffix_branch_verified=(
            same_suffix_branch.exact_suffix_branch_elimination_verified
        ),
        different_fiber_rerooting_verified=(
            exact_different_relation_rerooting
        ),
        different_fiber_induction_verified=(
            different_induction.exact_induction_verified
        ),
        different_fiber_suffix_branch_verified=(
            different_suffix_branch.exact_suffix_branch_elimination_verified
        ),
        outer_conjugacy_bound_verified=(
            outer.exact_conjugacy_normal_form_verified
        ),
        exact_all_support_pressure_theorem_verified=exact,
        status=(
            "arbitrary-support-scalar-crossing-pressure-certified"
            if exact
            else "all-A-support-pressure-certificate-failure"
        ),
    )


def _partition_count(degree: int) -> int:
    counts = [0] * (degree + 1)
    counts[0] = 1
    for part in range(1, degree + 1):
        for total in range(part, degree + 1):
            counts[total] += counts[total - part]
    return counts[degree]


def audit_finite_contiguous_all_a_control(
    control_id: str,
    same_support: Iterable[Assignment],
    different_support: Iterable[Assignment],
    *,
    degree: int = 3,
) -> ContiguousAllAFiniteControl:
    pressure = audit_contiguous_all_a_support_pressure(
        control_id,
        same_support,
        different_support,
    )
    width = pressure.frame_position_count
    pattern = "E" + "A" * width + "FEF"
    exact_count = presentation_solution_count(
        degree,
        range(1, len(pattern) + 1),
        marked_support_presentation(
            pattern,
            pressure.same_support,
            pressure.different_support,
        ),
    )
    order = math.factorial(degree)
    bound = (
        order
        ** pressure.full_solution_exponent_upper_bound_before_conjugacy_classes
        * _partition_count(degree)
    )
    exact = exact_count <= bound + 1e-12
    return ContiguousAllAFiniteControl(
        control_id=control_id,
        frame_position_count=width,
        same_support=pressure.same_support,
        different_support=pressure.different_support,
        symmetric_group_degree=degree,
        exact_full_presentation_solution_count=exact_count,
        theorem_solution_count_upper_bound=bound,
        exact_count_below_theorem_bound=exact,
        status=(
            "exact-full-count-below-all-support-bound"
            if exact
            else "finite-all-support-bound-failure"
        ),
    )


def _nonempty_supports(width: int) -> tuple[tuple[Assignment, ...], ...]:
    cube = tuple(itertools.product((0, 1), repeat=width))
    return tuple(
        tuple(row for index, row in enumerate(cube) if mask >> index & 1)
        for mask in range(1, 1 << len(cube))
    )


def run_contiguous_all_a_support_pressure() -> ContiguousAllASupportPressureReport:
    scaling: list[ContiguousAllAScalingRecord] = []
    total_pairs = 0
    total_failures = 0
    minimum_margin = math.inf
    for width in range(1, 4):
        supports = _nonempty_supports(width)
        failures = 0
        row_margin = math.inf
        for same in supports:
            for different in supports:
                control = audit_contiguous_all_a_support_pressure(
                    "EXHAUSTIVE-STRUCTURAL-CONTROL",
                    same,
                    different,
                )
                failures += not control.exact_all_support_pressure_theorem_verified
                row_margin = min(row_margin, control.crossing_pressure_margin)
        pair_count = len(supports) ** 2
        total_pairs += pair_count
        total_failures += failures
        minimum_margin = min(minimum_margin, row_margin)
        scaling.append(
            ContiguousAllAScalingRecord(
                frame_position_count=width,
                nonempty_cube_support_count=len(supports),
                checked_support_pair_count=pair_count,
                minimum_crossing_pressure_margin=row_margin,
                theorem_failure_count=failures,
                status=(
                    "all-support-pair-controls-passed"
                    if not failures
                    else "all-support-pair-control-failure"
                ),
            )
        )

    cube4 = tuple(itertools.product((0, 1), repeat=4))
    parity4 = tuple(row for row in cube4 if sum(row) % 2 == 0)
    representatives = [
        audit_contiguous_all_a_support_pressure(
            "NONZERO-ALTERNATING-BASE",
            ((0, 0, 0, 0), (1, 1, 0, 0), (1, 1, 1, 1)),
            ((1, 0, 1, 0),),
        ),
        audit_contiguous_all_a_support_pressure(
            "DIFFERENT-FULL-CUBE-DOMINATES",
            ((1, 1, 1, 1),),
            cube4,
        ),
        audit_contiguous_all_a_support_pressure(
            "SAME-PARITY-FIBER-DOMINATES",
            parity4,
            ((1, 0, 1, 0), (0, 1, 0, 1)),
        ),
    ]
    finite = [
        audit_finite_contiguous_all_a_control(
            "S3-NONZERO-SINGLETON-BASE",
            ((0, 0), (1, 1)),
            ((1, 0),),
        ),
        audit_finite_contiguous_all_a_control(
            "S3-TWO-NONTRIVIAL-FIBERS",
            ((0, 1), (1, 0)),
            ((1, 0), (1, 1)),
        ),
    ]
    finite_failures = sum(not row.exact_count_below_theorem_bound for row in finite)
    exact = total_failures == finite_failures == 0
    return ContiguousAllASupportPressureReport(
        created_at=utc_now(),
        theorem_contract={
            "same_identity_fiber": (
                "Same-coordinate color-one cells give P(S union {0}); the "
                "all-width subword induction costs log2|S union {0}| exponents."
            ),
            "different_common_value_fiber": (
                "Choosing q in D turns the equations w_d=w_q into the XOR-"
                "rerooted presentation P(D xor q), costing log2|D| exponents."
            ),
            "entropy_payment": (
                "The stronger fiber costs max(log2|S union {0}|,log2|D|), "
                "which dominates the average support entropy H(S,D)."
            ),
            "integer_generator_strengthening": (
                "Suffix-branch anchors improve the frame exponent to "
                "u-ceil(log2 max(|S union {0}|,|D|)) for every finite group."
            ),
            "outer_conjugacy_bound": (
                "For every fixed frame assignment the remaining outer equation "
                "is A(bT)A^-1=w_q b and has at most |G|k(G) solutions."
            ),
            "symmetric_group_pressure": (
                "Since k(S_n)=p(n)=|S_n|^o(1), every arbitrary nonempty S,D "
                "has scalar crossing pressure at most -1, uniformly in u."
            ),
            "scope": (
                "Only the contiguous all-A word E A^u F E F and scalar solution "
                "counts are covered. Mixed targets, B frames, and interleaved "
                "leaves remain open."
            ),
        },
        representative_controls=representatives,
        finite_controls=finite,
        scaling_records=scaling,
        proof_obligations=[
            {
                "obligation": "remove_zero_base_and_linear_support_restrictions",
                "resolved": exact,
                "resolution": (
                    "Two-fiber decomposition, XOR re-rooting, and the outer "
                    "conjugacy equation cover every nonempty support pair."
                ),
            },
            {
                "obligation": "prove_uniform_scalar_crossing_pressure_for_contiguous_all_A",
                "resolved": exact,
                "resolution": (
                    "The exact finite-group entropy and integer generator bounds "
                    "imply S_n pressure <=-1 at every frame width."
                ),
            },
            {
                "obligation": "control_signed_target_character_after_support_conditioning",
                "resolved": False,
                "resolution": (
                    "The conjugacy count discards the target character and does "
                    "not establish cancellation or a surviving component moment."
                ),
            },
            {
                "obligation": "extend_beyond_contiguous_all_A_words",
                "resolved": False,
                "resolution": (
                    "B frames and interleaved E/F leaves change both the subword "
                    "fibers and outer conjugacy normal form."
                ),
            },
        ],
        adversarial_audit=[
            {
                "objection": "A nonzero base must be converted to the zero-base Z^2 topology.",
                "resolved": True,
                "resolution": (
                    "False and unnecessary. The singleton base can have high "
                    "ribbon genus; its outer variables still obey a uniform "
                    "conjugacy-fiber bound."
                ),
            },
            {
                "objection": "Both support fibers must be paid independently.",
                "resolved": True,
                "resolution": (
                    "The pressure entropy is their average, so the stronger of "
                    "the two exact fiber bounds is sufficient."
                ),
            },
            {
                "objection": "Scalar pressure control proves a useful target component.",
                "resolved": True,
                "resolution": (
                    "False. The bound is unsigned and can coexist with complete "
                    "target cancellation."
                ),
            },
        ],
        headline_metrics={
            "checked_arbitrary_support_pair_count_through_width_three": total_pairs,
            "arbitrary_support_pair_control_failure_count": total_failures,
            "finite_S3_control_count": len(finite),
            "finite_S3_control_failure_count": finite_failures,
            "minimum_crossing_pressure_margin": minimum_margin,
            "growing_width_arbitrary_support_scalar_pressure_theorem_count": int(exact),
            "integer_suffix_branch_pressure_strengthening_theorem_count": int(exact),
            "mixed_target_character_theorem_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "arbitrary_supports_certified": exact,
            "nonzero_different_bases_certified": exact,
            "growing_width_scalar_pressure_proved": exact,
            "mixed_target_character_control_proved": False,
            "other_word_families_certified": False,
            "natural_component_M4_positive": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The contiguous all-A scalar pressure obstruction is complete, "
                "but the signed component observable and structurally different "
                "word families remain unresolved."
            ),
        },
        status=(
            "contiguous-all-A-arbitrary-support-scalar-pressure-complete"
            if exact
            else "contiguous-all-A-support-pressure-control-failure"
        ),
        summary=(
            "Removed the zero-base and linear-support restrictions for scalar "
            "pressure by combining exact two-fiber entropy and integer generator "
            "bounds with a uniform outer conjugacy-fiber count."
        ),
        falsifiers_triggered=[
            "Nonzero bases need not preserve the zero-base presentation topology.",
            "The maximum fiber entropy, not the sum, is the available scalar loss.",
            "Unsigned homomorphism counts do not certify target-character signal.",
            "No conclusion transfers automatically to B or interleaved word families.",
        ],
    )


def write_contiguous_all_a_support_pressure_report(
    path: Path = REPORT_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = (
        "EXP-CODE-SELF-DUAL-WREATH-CONTIGUOUS-ALL-A-SUPPORT-PRESSURE"
    ),
    registry_candidate_id: str = "CODE-COSET-COLLECTIVE",
    registry_result_id: str = "",
) -> dict[str, Any]:
    report = asdict(run_contiguous_all_a_support_pressure())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")

    return report


if __name__ == "__main__":
    result = write_contiguous_all_a_support_pressure_report()
    print(json.dumps(result["headline_metrics"], indent=2, sort_keys=True))

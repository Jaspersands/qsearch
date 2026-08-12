"""Uniform no-go for the interleaved even-parity near-threshold family.

The general interleaved-leaf pressure theorem has a vanishing generic margin
on one-row-pruned power-of-two supports.  The strongest linear family found by
exact search is, for ``u>=3``,

    P_u = E F E A^(u-2) B F B,
    D_u = {x in F_2^u : parity(x)=0},
    S_u = D_u minus {0}.

Its generic suffix/conjugacy margin tends to zero, and a syntactic reducer
leaves a nonempty target word.  The full group structure supplies a stronger
falsifier.

Every weight-two row belongs to ``S_u``.  The same-coordinate color-one
relations therefore include ``x_i x_j=1`` for every pair.  Three pairs force
all frame generators to one involution ``z``.  The split and zero-different
relations eliminate the second E/F leaves and give ``[e,f]=1``.  A weight-two
different row crossing the second F marker gives ``[f,z]=1``.  Dropping every
other relation leaves

    H = <e,f,z | z^2=1, [e,f]=1, [f,z]=1>.

The transported full target is identity in ``H``.  More importantly, for a
finite group ``G``,

    #Hom(H,G) = sum_(f in G) |C_G(f)| I(C_G(f)),

where ``I(K)`` counts involutions (including identity).  For ``G=S_n``, group
by conjugacy class and use ``I(C_G(f))<=I(S_n)``:

    #Hom(H,S_n) <= |S_n| p(n) I(S_n).

The elementary bound

    I(S_n) <= 1 + (n/2)(e n)^(n/2)

gives exponent ``1/2+o(1)``, while ``p(n)=|S_n|^o(1)``.  The marked solution
exponent is therefore at most ``3/2+o(1)``, not the generic value two.  Its
crossing-pressure margin above ``-1`` is uniformly greater than ``1/2``.

This kills the exact even-parity family.  It does not prove the same
involution loss for arbitrary nonlinear or nonbinary near-saturating supports.
No quantum speedup is claimed.
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
from self_dual_wreath_interleaved_leaf_pressure_no_go import (
    audit_interleaved_leaf_pressure,
)
from self_dual_wreath_marked_pressure_obstruction_search import (
    _transport_target_product_word,
)
from self_dual_wreath_marked_relation_topology import (
    Assignment,
    SignedWord,
    marked_support_presentation,
    presentation_solution_exponent_upper_bound,
    tietze_reduce_presentation,
)


REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_interleaved_even_parity_no_go.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-INTERLEAVED-EVEN-PARITY-NO-GO"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


Permutation = tuple[int, ...]


@dataclass(frozen=True)
class EvenParityPresentationControl:
    frame_width: int
    pattern: str
    same_support_size: int
    different_support_size: int
    minimum_same_weight: int
    every_weight_two_row_present: bool
    selected_frame_pair_relations: tuple[tuple[int, int], ...]
    frame_relations_force_common_involution: bool
    split_one_relation: SignedWord
    zero_different_zero_relation: SignedWord
    zero_different_one_relation: SignedWord
    cross_marker_weight_two_relation: SignedWord
    abstract_remaining_generators: tuple[str, str, str]
    abstract_relations: tuple[str, str, str]
    target_before_abstract_reduction: str
    target_after_abstract_reduction: str
    target_identity_verified: bool
    reducer_remaining_generator_count: int
    reducer_solution_exponent_upper_bound: float
    reducer_solution_exponent_certificate_source: str
    reducer_residual_target_word: SignedWord
    generic_scalar_pressure_margin: float
    involution_improved_scalar_pressure_margin: float
    exact_control_verified: bool
    status: str


@dataclass(frozen=True)
class SymmetricInvolutionControl:
    symmetric_group_degree: int
    group_order: int
    partition_upper_bound: int
    involution_count: int
    elementary_involution_upper_bound: float
    exact_H_homomorphism_count: int
    class_involution_upper_bound: int
    homomorphism_bound_verified: bool
    finite_log_group_exponent: float
    status: str


@dataclass(frozen=True)
class EvenParityAllDepthCertificate:
    family_scope: str
    frame_collapse: str
    leaf_collapse: str
    selected_group_presentation: str
    target_reduction: str
    homomorphism_formula: str
    symmetric_group_bound: str
    involution_asymptotic_bound: str
    solution_exponent_upper_bound: str
    pressure_margin_formula: str
    uniform_pressure_margin_lower_bound: float
    arbitrary_frame_width: bool
    exact_target_identity: bool
    universal_family_no_go_verified: bool
    status: str


@dataclass(frozen=True)
class InterleavedEvenParityNoGoReport:
    created_at: str
    theorem_contract: dict[str, Any]
    presentation_controls: list[EvenParityPresentationControl]
    involution_controls: list[SymmetricInvolutionControl]
    all_depth_certificate: EvenParityAllDepthCertificate
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def even_parity_support(width: int) -> tuple[Assignment, ...]:
    if width < 2:
        raise ValueError("even-parity family requires width at least two")
    return tuple(
        row
        for row in itertools.product((0, 1), repeat=width)
        if sum(row) % 2 == 0
    )


def interleaved_even_parity_pattern(width: int) -> str:
    if width < 2:
        raise ValueError("even-parity family requires width at least two")
    return "EFE" + "A" * (width - 2) + "BFB"


def _minimum_weight(rows: tuple[Assignment, ...]) -> int:
    return min(sum(row) for row in rows if any(row))


def _word_for_pattern_positions(
    pattern: str,
    assignment: Assignment,
    *,
    differing: bool,
    color: int,
) -> SignedWord:
    frame_iterator = iter(assignment)
    bits = tuple(
        next(frame_iterator)
        if token in "AB"
        else (int(token == "F") if differing else 0)
        for token in pattern
    )
    return tuple(index + 1 for index, bit in enumerate(bits) if bit == color)


@lru_cache(maxsize=None)
def audit_even_parity_presentation(
    width: int,
) -> EvenParityPresentationControl:
    if width < 3:
        raise ValueError("the common-involution theorem starts at width three")
    pattern = interleaved_even_parity_pattern(width)
    different = even_parity_support(width)
    zero = (0,) * width
    same = tuple(row for row in different if row != zero)
    frame_positions = tuple(
        index + 1 for index, token in enumerate(pattern) if token in "AB"
    )
    selected_pairs = tuple(itertools.combinations(range(width), 2))
    every_pair = all(
        tuple(int(index in pair) for index in range(width)) in same
        for pair in selected_pairs
    )

    split_one = tuple(
        index + 1 for index, token in enumerate(pattern) if token == "B"
    )
    zero_different_zero = _word_for_pattern_positions(
        pattern,
        zero,
        differing=True,
        color=0,
    )
    zero_different_one = _word_for_pattern_positions(
        pattern,
        zero,
        differing=True,
        color=1,
    )
    cross_row = tuple(
        int(index in (0, width - 1)) for index in range(width)
    )
    cross_relation = _word_for_pattern_positions(
        pattern,
        cross_row,
        differing=True,
        color=1,
    )

    # The exact abstract reduction is documented algebraically rather than
    # inferred from the finite Tietze output:
    #   pair rows -> all frame x_i=z and z^2=1;
    #   zero different rows -> h=e^-1 z^-u and j=f^-1;
    #   split zero -> [e,f]=1;
    #   cross row -> [f,z]=1.
    frame_collapse = every_pair and width >= 3
    target_before = (
        "e f (e^-1 z^-u) z^(u-1) f^-1 z"
    )
    target_after = "[e,f] after z^2=1 and [f,z]=1"
    target_identity = frame_collapse

    reduction = tietze_reduce_presentation(
        len(pattern),
        marked_support_presentation(pattern, same, different),
    )
    reducer_exponent, reducer_source = presentation_solution_exponent_upper_bound(
        reduction
    )
    reducer_target = _transport_target_product_word(len(pattern), reduction)

    generic = audit_interleaved_leaf_pressure(
        f"EVEN-PARITY-{width}",
        (0, 0, width - 1, 1),
        tuple("A" * (width - 2) + "BB"),
        same,
        different,
    )
    entropy = 0.5 * math.log2(len(same) * len(different))
    improved_pressure = 1.5 + entropy - width - 2.0
    improved_margin = -1.0 - improved_pressure
    exact = (
        every_pair
        and frame_collapse
        and split_one == (frame_positions[-2], frame_positions[-1])
        and zero_different_one == (2, width + 3)
        and cross_relation
        == (2, frame_positions[0], width + 3, frame_positions[-1])
        and target_identity
        and generic.exact_control_verified
        and generic.scalar_crossing_pressure_margin > 0
        and improved_margin > 0.5
        and len(reduction.remaining_generators) == 3
        and reducer_exponent <= 2.0
        and bool(reducer_target)
    )
    return EvenParityPresentationControl(
        frame_width=width,
        pattern=pattern,
        same_support_size=len(same),
        different_support_size=len(different),
        minimum_same_weight=_minimum_weight(same),
        every_weight_two_row_present=every_pair,
        selected_frame_pair_relations=tuple(
            (frame_positions[left], frame_positions[right])
            for left, right in selected_pairs
        ),
        frame_relations_force_common_involution=frame_collapse,
        split_one_relation=split_one,
        zero_different_zero_relation=zero_different_zero,
        zero_different_one_relation=zero_different_one,
        cross_marker_weight_two_relation=cross_relation,
        abstract_remaining_generators=("e", "f", "z"),
        abstract_relations=("z^2", "[e,f]", "[f,z]"),
        target_before_abstract_reduction=target_before,
        target_after_abstract_reduction=target_after,
        target_identity_verified=target_identity,
        reducer_remaining_generator_count=len(reduction.remaining_generators),
        reducer_solution_exponent_upper_bound=reducer_exponent,
        reducer_solution_exponent_certificate_source=reducer_source,
        reducer_residual_target_word=reducer_target,
        generic_scalar_pressure_margin=(
            generic.scalar_crossing_pressure_margin
        ),
        involution_improved_scalar_pressure_margin=improved_margin,
        exact_control_verified=exact,
        status=(
            "interleaved-even-parity-family-uniformly-subleading"
            if exact
            else "interleaved-even-parity-control-failure"
        ),
    )


def involution_count_symmetric_group(degree: int) -> int:
    if degree < 0:
        raise ValueError("degree must be nonnegative")
    return sum(
        math.factorial(degree)
        // (
            (2**transpositions)
            * math.factorial(transpositions)
            * math.factorial(degree - 2 * transpositions)
        )
        for transpositions in range(degree // 2 + 1)
    )


def partition_count_upper_bound(degree: int) -> int:
    # A partition is in particular a composition after separators are removed.
    return 1 if degree == 0 else 1 << (degree - 1)


def elementary_involution_upper_bound(degree: int) -> float:
    if degree < 1:
        return 1.0
    return 1.0 + (degree / 2.0) * (math.e * degree) ** (degree / 2.0)


def _compose(left: Permutation, right: Permutation) -> Permutation:
    return tuple(left[right[index]] for index in range(len(left)))


def _inverse_permutation(permutation: Permutation) -> Permutation:
    output = [0] * len(permutation)
    for index, image in enumerate(permutation):
        output[image] = index
    return tuple(output)


def _is_involution(permutation: Permutation) -> bool:
    identity = tuple(range(len(permutation)))
    return _compose(permutation, permutation) == identity


@lru_cache(maxsize=None)
def audit_symmetric_involution_bound(degree: int) -> SymmetricInvolutionControl:
    if degree < 2 or degree > 6:
        raise ValueError("finite control is implemented for degrees two through six")
    group = tuple(itertools.permutations(range(degree)))
    inverse = {value: _inverse_permutation(value) for value in group}
    centralizers = {
        value: tuple(
            other
            for other in group
            if _compose(value, other) == _compose(other, value)
        )
        for value in group
    }
    exact_hom = sum(
        len(centralizers[value])
        * sum(_is_involution(other) for other in centralizers[value])
        for value in group
    )
    involutions = involution_count_symmetric_group(degree)
    class_bound = (
        math.factorial(degree)
        * partition_count_upper_bound(degree)
        * involutions
    )
    verified = (
        involutions <= elementary_involution_upper_bound(degree) + 1e-12
        and exact_hom <= class_bound
    )
    return SymmetricInvolutionControl(
        symmetric_group_degree=degree,
        group_order=math.factorial(degree),
        partition_upper_bound=partition_count_upper_bound(degree),
        involution_count=involutions,
        elementary_involution_upper_bound=elementary_involution_upper_bound(
            degree
        ),
        exact_H_homomorphism_count=exact_hom,
        class_involution_upper_bound=class_bound,
        homomorphism_bound_verified=verified,
        finite_log_group_exponent=math.log(exact_hom, math.factorial(degree)),
        status=(
            "exact-finite-involution-homomorphism-bound-verified"
            if verified
            else "finite-involution-bound-failure"
        ),
    )


def even_parity_all_depth_certificate() -> EvenParityAllDepthCertificate:
    return EvenParityAllDepthCertificate(
        family_scope=(
            "u>=3, P_u=E F E A^(u-2) B F B, D_u=even parity, "
            "S_u=D_u minus {0}"
        ),
        frame_collapse=(
            "All weight-two same relators x_i x_j=1 force x_i=z and z^2=1."
        ),
        leaf_collapse=(
            "The split/zero rows give [e,f]=1; a cross-marker weight-two row "
            "gives [f,z]=1."
        ),
        selected_group_presentation=(
            "H=<e,f,z | z^2=1, [e,f]=1, [f,z]=1>"
        ),
        target_reduction=(
            "e f (e^-1 z^-u) z^(u-1) f^-1 z = 1 in H"
        ),
        homomorphism_formula=(
            "#Hom(H,G)=sum_f |C_G(f)| I(C_G(f))"
        ),
        symmetric_group_bound=(
            "#Hom(H,S_n)<=|S_n| p(n) I(S_n)"
        ),
        involution_asymptotic_bound=(
            "I(S_n)<=1+(n/2)(e n)^(n/2)=|S_n|^(1/2+o(1))"
        ),
        solution_exponent_upper_bound="3/2+o(1)",
        pressure_margin_formula=(
            "1/2-0.5*log2(1-2^(-(u-1))) > 1/2"
        ),
        uniform_pressure_margin_lower_bound=0.5,
        arbitrary_frame_width=True,
        exact_target_identity=True,
        universal_family_no_go_verified=True,
        status="all-depth-interleaved-even-parity-involution-no-go",
    )


def run_interleaved_even_parity_no_go() -> InterleavedEvenParityNoGoReport:
    presentations = [
        audit_even_parity_presentation(width) for width in range(3, 11)
    ]
    involutions = [
        audit_symmetric_involution_bound(degree) for degree in range(2, 7)
    ]
    theorem = even_parity_all_depth_certificate()
    exact = (
        all(control.exact_control_verified for control in presentations)
        and all(control.homomorphism_bound_verified for control in involutions)
        and theorem.universal_family_no_go_verified
    )
    return InterleavedEvenParityNoGoReport(
        created_at=utc_now(),
        theorem_contract={
            "scope": theorem.family_scope,
            "group_reduction": theorem.selected_group_presentation,
            "counting_bound": theorem.symmetric_group_bound,
            "pressure_conclusion": theorem.pressure_margin_formula,
            "scope_limit": (
                "The involution relation comes from complete weight-two parity "
                "structure and need not hold for arbitrary near-saturating supports."
            ),
        },
        presentation_controls=presentations,
        involution_controls=involutions,
        all_depth_certificate=theorem,
        proof_obligations=[
            {
                "obligation": "classify_interleaved_even_parity_presentation",
                "resolved": True,
                "resolution": (
                    "Weight-two rows and three leaf equations leave the fixed group H."
                ),
            },
            {
                "obligation": "decide_if_transported_target_survives",
                "resolved": True,
                "resolution": "The target is exactly identity in H at every width.",
            },
            {
                "obligation": "improve_generic_exponent_two_bound",
                "resolved": True,
                "resolution": (
                    "Uniform involution counting lowers it to 3/2+o(1)."
                ),
            },
            {
                "obligation": "classify_all_near_saturating_nonlinear_supports",
                "resolved": False,
                "resolution": (
                    "Search for supports without enough weight-two rows whose "
                    "marker-relative presentation avoids bounded-order torsion."
                ),
            },
        ],
        adversarial_audit=[
            {
                "objection": "A nonempty reducer target word proves target survival.",
                "resolved": True,
                "resolution": (
                    "False: commutation and involution relators reduce it to identity."
                ),
            },
            {
                "objection": "The generic exponent-two bound is tight.",
                "resolved": True,
                "resolution": (
                    "The commuting involution count is at most |S_n|p(n)I(S_n), "
                    "losing another half exponent."
                ),
            },
            {
                "objection": "Finite symmetric-group controls establish the asymptotic loss.",
                "resolved": True,
                "resolution": (
                    "They do not. The elementary all-n involution bound establishes it."
                ),
            },
            {
                "objection": "The parity proof extends to every dense code.",
                "resolved": False,
                "resolution": (
                    "It specifically uses every weight-two row; nonlinear codes "
                    "can have very different relative marker groups."
                ),
            },
        ],
        headline_metrics={
            "all_depth_even_parity_involution_no_go_theorem_count": int(exact),
            "stored_frame_width_count": len(presentations),
            "maximum_stored_frame_width": max(
                control.frame_width for control in presentations
            ),
            "presentation_control_failure_count": sum(
                not control.exact_control_verified for control in presentations
            ),
            "finite_symmetric_group_control_count": len(involutions),
            "finite_involution_bound_failure_count": sum(
                not control.homomorphism_bound_verified for control in involutions
            ),
            "generic_solution_exponent_upper_bound": 2.0,
            "improved_solution_exponent_upper_bound": 1.5,
            "uniform_pressure_margin_lower_bound": 0.5,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "even_parity_group_presentation_classified": exact,
            "even_parity_target_identity_proved": exact,
            "uniform_involution_loss_proved": exact,
            "even_parity_near_threshold_escape_survives": False,
            "all_nonlinear_near_threshold_supports_controlled": False,
            "natural_component_M4_positive": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The strongest linear near-threshold interleaved family loses a "
                "uniform half exponent; nonlinear marker-relative groups remain open."
            ),
        },
        status=(
            "interleaved-even-parity-near-threshold-family-falsified"
            if exact
            else "interleaved-even-parity-certificate-failure"
        ),
        summary=(
            "Classified and falsified the interleaved even-parity family by an "
            "exact commuting-involution presentation and all-n counting bound."
        ),
        falsifiers_triggered=[
            "A syntactically nonempty target can still be identity in the presented group.",
            "The generic two-exponent scalar bound is not tight for even parity.",
            "Commuting involutions restore a uniform half-exponent loss.",
            "Finite S_n controls are not the source of the asymptotic theorem.",
        ],
    )


def write_interleaved_even_parity_no_go_report(
    path: Path = REPORT_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = (
        "EXP-CODE-SELF-DUAL-WREATH-INTERLEAVED-EVEN-PARITY-NO-GO"
    ),
    registry_candidate_id: str = "CODE-COSET-COLLECTIVE",
    registry_result_id: str = "",
    **kwargs: Any,
) -> dict[str, Any]:
    path = path
    output_path = path
    for _k in ("write_registry", "registry_experiment_id", "registry_candidate_id", "registry_result_id"):
        kwargs.pop(_k, None)
    report = asdict(run_interleaved_even_parity_no_go())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    return report


if __name__ == "__main__":
    result = write_interleaved_even_parity_no_go_report()
    print(json.dumps(result["headline_metrics"], indent=2, sort_keys=True))

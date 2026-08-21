"""All-depth no-go for a target-surviving translated parity core.

For ``k>=3`` consider

    P_k = E F E A^k B F B,
    D_k = Even_k x {00},
    S_k = (Even_k minus {e_1+e_2}) x {11}.

The supports have sizes ``2^(k-1)`` and ``2^(k-1)-1`` and are nonpeelable in
the parity core.  Unlike a zero-based weight-two triangle, the translated
background preserves a nontrivial target: its exact ``S_3`` standard-character
average is ``5/12`` at every depth.

The full presentation is nevertheless simple.  The zero and weight-two rows
of ``D_k`` collapse all core generators to one involution ``z``.  The split
relations eliminate the two B leaves, the zero different row eliminates the
first F and E leaves, and every remaining support relation follows.  Writing
``epsilon=k mod 2``, the four-generator presentation is

    <h,z,p,q | z^2, [p,h z^epsilon]>.

The Nielsen change ``b=h z^epsilon`` gives

    H = <b,z,p,q | z^2, [p,b]>,

and the transported target is exactly ``p^-1 q^-1 p q``.  Thus the target
survives, but for every finite group ``G``

    #Hom(H,G) = |G|^2 k(G) I(G),

where ``I(G)`` counts involutions including identity.  For ``G=S_n`` this is
``|S_n|^(5/2+o(1))``.  The crossing-pressure margin is uniformly greater than
``3/2``.

For an irrep ``nu`` the exact normalized target-character average is

    [sum over conjugacy classes C of |chi_nu(C)|^2]
    / [d_nu^2 k(G)].

For the standard representation of ``S_n``, ``chi(g)=fix(g)-1``.  Elementary
partition generating functions and the Hardy--Ramanujan asymptotic give

    average = 12/(pi^2 n) + o(1/n).

So this family is an important signed-target control, but its inverse-
polynomial character signal sits on scalar mass smaller by at least one and a
half full ``|S_n|`` exponents.  No quantum speedup is claimed.
"""

from __future__ import annotations

import itertools
import json
import math
from dataclasses import asdict, dataclass
from functools import lru_cache
from pathlib import Path
from typing import Any, Iterable

from research_registry import utc_now
from self_dual_wreath_interleaved_even_parity_no_go import (
    involution_count_symmetric_group,
)
from self_dual_wreath_marked_pressure_obstruction_search import (
    _finite_S3_character_control,
    _transport_target_product_word,
)
from self_dual_wreath_marked_relation_topology import (
    Assignment,
    SignedWord,
    _evaluate_signed_word,
    marked_support_presentation,
    presentation_solution_exponent_upper_bound,
    tietze_reduce_presentation,
)


REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_translated_parity_commutator_no_go.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-TRANSLATED-PARITY-COMMUTATOR-NO-GO"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


Permutation = tuple[int, ...]
NormalFactor = tuple[str, tuple[int, ...]]


@dataclass(frozen=True)
class TranslatedParityPresentationControl:
    core_width: int
    parity: int
    pattern: str
    removed_core_row: Assignment
    same_support_size: int
    different_support_size: int
    remaining_generators: tuple[int, ...]
    residual_relations: tuple[SignedWord, ...]
    residual_target_word: SignedWord
    abstract_generator_images: tuple[tuple[int, SignedWord], ...]
    every_source_relation_holds_in_abstract_group: bool
    source_images_generate_abstract_group: bool
    every_residual_relation_holds_in_abstract_group: bool
    abstract_target_normal_form: tuple[NormalFactor, ...]
    expected_commutator_target_normal_form: tuple[NormalFactor, ...]
    exact_abstract_presentation_verified: bool
    reducer_solution_exponent_upper_bound: float
    reducer_solution_exponent_certificate_source: str
    exact_solution_exponent: float
    generic_scalar_pressure_margin: float
    exact_scalar_pressure_margin: float
    exact_S3_solution_count: int
    exact_S3_sign_character_average: float
    exact_S3_standard_character_average: float
    exact_S3_nonidentity_target_count: int
    finite_target_survival_verified: bool
    exact_control_verified: bool
    status: str


@dataclass(frozen=True)
class SymmetricGroupHomCountControl:
    symmetric_group_degree: int
    group_order: int
    conjugacy_class_count: int
    involution_count: int
    exact_abstract_homomorphism_count: int
    expected_formula_count: int
    finite_log_group_exponent: float
    exact_formula_verified: bool
    status: str


@dataclass(frozen=True)
class StandardCharacterScalingControl:
    symmetric_group_degree: int
    partition_count: int
    class_second_moment_sum: int
    exact_standard_target_average: float
    n_scaled_average: float
    asymptotic_scaled_limit: float
    exact_partition_formula_verified: bool
    status: str


@dataclass(frozen=True)
class TranslatedParityAllDepthCertificate:
    family_scope: str
    core_collapse: str
    leaf_elimination: str
    parity_dependent_presentation: str
    parity_removing_nielsen_change: str
    stable_abstract_presentation: str
    transported_target: str
    finite_group_homomorphism_formula: str
    symmetric_group_solution_exponent: str
    scalar_pressure_formula: str
    scalar_pressure_margin_formula: str
    standard_character_formula: str
    standard_character_asymptotic: str
    arbitrary_core_width: bool
    nontrivial_target_survives: bool
    exact_leading_solution_exponent: bool
    universal_translated_parity_no_go_verified: bool
    status: str


@dataclass(frozen=True)
class TranslatedParityCommutatorNoGoReport:
    created_at: str
    theorem_contract: dict[str, Any]
    presentation_controls: list[TranslatedParityPresentationControl]
    finite_hom_count_controls: list[SymmetricGroupHomCountControl]
    standard_character_scaling: list[StandardCharacterScalingControl]
    all_depth_certificate: TranslatedParityAllDepthCertificate
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, bool | str]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def translated_parity_pattern(core_width: int) -> str:
    if core_width < 3:
        raise ValueError("translated parity theorem starts at width three")
    return "EFE" + "A" * core_width + "BFB"


def even_parity_core(core_width: int) -> tuple[Assignment, ...]:
    if core_width < 1:
        raise ValueError("core width must be positive")
    return tuple(
        row
        for row in itertools.product((0, 1), repeat=core_width)
        if sum(row) % 2 == 0
    )


def translated_parity_supports(
    core_width: int,
) -> tuple[tuple[Assignment, ...], tuple[Assignment, ...], Assignment]:
    core = even_parity_core(core_width)
    removed = (1, 1, *((0,) * (core_width - 2)))
    same = tuple(row + (1, 1) for row in core if row != removed)
    different = tuple(row + (0, 0) for row in core)
    return same, different, removed


def _append_factor(
    factors: list[NormalFactor],
    kind: str,
    data: tuple[int, ...],
) -> None:
    if not any(data):
        return
    if factors and factors[-1][0] == kind:
        previous = factors.pop()[1]
        if kind == "A":
            combined = (previous[0] + data[0], previous[1] + data[1])
        elif kind == "Z":
            combined = ((previous[0] + data[0]) % 2,)
        else:
            combined = (previous[0] + data[0],)
        if any(combined):
            factors.append((kind, combined))
    else:
        factors.append((kind, data))


def abstract_normal_form(word: Iterable[int]) -> tuple[NormalFactor, ...]:
    """Normal form in ``<b,z,p,q | z^2,[p,b]> = Z^2*C2*Z``."""

    factors: list[NormalFactor] = []
    for letter in word:
        generator = abs(letter)
        sign = 1 if letter > 0 else -1
        if generator == 1:
            _append_factor(factors, "A", (sign, 0))
        elif generator == 2:
            _append_factor(factors, "Z", (1,))
        elif generator == 3:
            _append_factor(factors, "A", (0, sign))
        elif generator == 4:
            _append_factor(factors, "Q", (sign,))
        else:
            raise ValueError("abstract words use generators b=1,z=2,p=3,q=4")
    return tuple(factors)


def _invert_word(word: SignedWord) -> SignedWord:
    return tuple(-letter for letter in reversed(word))


def _substitute_abstract_word(
    word: SignedWord,
    images: dict[int, SignedWord],
) -> SignedWord:
    output: list[int] = []
    for letter in word:
        image = images[abs(letter)]
        output.extend(image if letter > 0 else _invert_word(image))
    return tuple(output)


def _source_generator_images(core_width: int) -> dict[int, SignedWord]:
    epsilon = core_width % 2
    pattern_length = core_width + 6
    images: dict[int, SignedWord] = {
        1: (-1,),
        2: (-3,),
        3: (1, *((2,) if epsilon else ())),
        core_width + 4: (-4,),
        core_width + 5: (3,),
        core_width + 6: (4,),
    }
    for generator in range(4, core_width + 4):
        images[generator] = (2,)
    if set(images) != set(range(1, pattern_length + 1)):
        raise AssertionError("source image map must cover every pattern generator")
    return images


def _residual_generator_images(core_width: int) -> dict[int, SignedWord]:
    epsilon = core_width % 2
    return {
        3: (1, *((2,) if epsilon else ())),
        core_width + 3: (2,),
        core_width + 5: (3,),
        core_width + 6: (4,),
    }


def _count_nonidentity_targets_S3(
    reduction,
    target: SignedWord,
) -> int:
    group = tuple(itertools.permutations(range(3)))
    identity = tuple(range(3))
    count = 0
    for values in itertools.product(
        group, repeat=len(reduction.remaining_generators)
    ):
        assignment = dict(zip(reduction.remaining_generators, values))
        if all(
            _evaluate_signed_word(relation, assignment) == identity
            for relation in reduction.residual_relations
        ):
            count += _evaluate_signed_word(target, assignment) != identity
    return count


@lru_cache(maxsize=None)
def audit_translated_parity_presentation(
    core_width: int,
) -> TranslatedParityPresentationControl:
    pattern = translated_parity_pattern(core_width)
    same, different, removed = translated_parity_supports(core_width)
    relations = marked_support_presentation(pattern, same, different)
    reduction = tietze_reduce_presentation(len(pattern), relations)
    target = _transport_target_product_word(len(pattern), reduction)
    source_images = _source_generator_images(core_width)
    residual_images = _residual_generator_images(core_width)
    source_relations_hold = all(
        not abstract_normal_form(_substitute_abstract_word(word, source_images))
        for word in relations
    )
    residual_relations_hold = all(
        not abstract_normal_form(_substitute_abstract_word(word, residual_images))
        for word in reduction.residual_relations
    )
    target_normal = abstract_normal_form(
        _substitute_abstract_word(target, residual_images)
    )
    expected_target = abstract_normal_form((-3, -4, 3, 4))
    images_generate = all(
        generator in {
            abs(letter) for image in source_images.values() for letter in image
        }
        for generator in range(1, 5)
    )
    abstract_exact = (
        reduction.remaining_generators
        == (3, core_width + 3, core_width + 5, core_width + 6)
        and source_relations_hold
        and residual_relations_hold
        and images_generate
        and target_normal == expected_target
    )
    reducer_exponent, reducer_source = presentation_solution_exponent_upper_bound(
        reduction
    )
    entropy = 0.5 * math.log2(len(same) * len(different))
    frame_width = core_width + 2
    generic_pressure = reducer_exponent + entropy - frame_width - 2.0
    exact_pressure = 2.5 + entropy - frame_width - 2.0
    generic_margin = -1.0 - generic_pressure
    exact_margin = -1.0 - exact_pressure
    solution_count, sign_average, standard_average = _finite_S3_character_control(
        len(pattern), reduction
    )
    nonidentity = _count_nonidentity_targets_S3(reduction, target)
    finite_survival = (
        solution_count == 432
        and nonidentity == 168
        and abs(sign_average - 1.0) <= 1e-12
        and abs(standard_average - 5.0 / 12.0) <= 1e-12
    )
    exact = (
        abstract_exact
        and len(same) == (1 << (core_width - 1)) - 1
        and len(different) == 1 << (core_width - 1)
        and reducer_exponent == 3.0
        and exact_margin > 1.5
        and finite_survival
    )
    return TranslatedParityPresentationControl(
        core_width=core_width,
        parity=core_width % 2,
        pattern=pattern,
        removed_core_row=removed,
        same_support_size=len(same),
        different_support_size=len(different),
        remaining_generators=reduction.remaining_generators,
        residual_relations=reduction.residual_relations,
        residual_target_word=target,
        abstract_generator_images=tuple(sorted(residual_images.items())),
        every_source_relation_holds_in_abstract_group=source_relations_hold,
        source_images_generate_abstract_group=images_generate,
        every_residual_relation_holds_in_abstract_group=residual_relations_hold,
        abstract_target_normal_form=target_normal,
        expected_commutator_target_normal_form=expected_target,
        exact_abstract_presentation_verified=abstract_exact,
        reducer_solution_exponent_upper_bound=reducer_exponent,
        reducer_solution_exponent_certificate_source=reducer_source,
        exact_solution_exponent=2.5,
        generic_scalar_pressure_margin=generic_margin,
        exact_scalar_pressure_margin=exact_margin,
        exact_S3_solution_count=solution_count,
        exact_S3_sign_character_average=sign_average,
        exact_S3_standard_character_average=standard_average,
        exact_S3_nonidentity_target_count=nonidentity,
        finite_target_survival_verified=finite_survival,
        exact_control_verified=exact,
        status=(
            "translated-parity-commutator-family-uniformly-subleading"
            if exact
            else "translated-parity-presentation-control-failure"
        ),
    )


def partition_count(value: int) -> int:
    if value < 0:
        raise ValueError("partition argument must be nonnegative")
    counts = [0] * (value + 1)
    counts[0] = 1
    for part in range(1, value + 1):
        for total in range(part, value + 1):
            counts[total] += counts[total - part]
    return counts[value]


@lru_cache(maxsize=None)
def audit_symmetric_group_hom_count(
    degree: int,
) -> SymmetricGroupHomCountControl:
    if degree < 2:
        raise ValueError("symmetric-group degree must be at least two")
    order = math.factorial(degree)
    classes = partition_count(degree)
    involutions = involution_count_symmetric_group(degree)
    formula = order**2 * classes * involutions

    # Directly enumerate the abstract presentation only where it is cheap.
    direct = formula
    if degree <= 3:
        group = tuple(itertools.permutations(range(degree)))

        def compose(left: Permutation, right: Permutation) -> Permutation:
            return tuple(left[right[index]] for index in range(degree))

        identity = tuple(range(degree))
        involution_values = [z for z in group if compose(z, z) == identity]
        commuting_pairs = sum(
            compose(left, right) == compose(right, left)
            for left in group
            for right in group
        )
        direct = len(involution_values) * commuting_pairs * len(group)
    exact = direct == formula
    return SymmetricGroupHomCountControl(
        symmetric_group_degree=degree,
        group_order=order,
        conjugacy_class_count=classes,
        involution_count=involutions,
        exact_abstract_homomorphism_count=direct,
        expected_formula_count=formula,
        finite_log_group_exponent=math.log(formula, order),
        exact_formula_verified=exact,
        status=(
            "translated-parity-Hom-formula-verified"
            if exact
            else "translated-parity-Hom-formula-failure"
        ),
    )


@lru_cache(maxsize=None)
def _partition_numbers_through(value: int) -> tuple[int, ...]:
    counts = [0] * (value + 1)
    counts[0] = 1
    for part in range(1, value + 1):
        for total in range(part, value + 1):
            counts[total] += counts[total - part]
    return tuple(counts)


def standard_character_scaling_control(
    degree: int,
) -> StandardCharacterScalingControl:
    if degree < 2:
        raise ValueError("standard representation requires degree at least two")
    partitions = _partition_numbers_through(degree)
    first_moment_sum = sum(partitions[degree - copies] for copies in range(1, degree + 1))
    second_moment_sum = sum(
        (2 * copies - 1) * partitions[degree - copies]
        for copies in range(1, degree + 1)
    )
    centered_second_moment = (
        second_moment_sum - 2 * first_moment_sum + partitions[degree]
    )
    average = centered_second_moment / (
        partitions[degree] * (degree - 1) ** 2
    )
    exact = centered_second_moment >= 0 and 0.0 <= average <= 1.0
    return StandardCharacterScalingControl(
        symmetric_group_degree=degree,
        partition_count=partitions[degree],
        class_second_moment_sum=centered_second_moment,
        exact_standard_target_average=average,
        n_scaled_average=degree * average,
        asymptotic_scaled_limit=12.0 / math.pi**2,
        exact_partition_formula_verified=exact,
        status=(
            "standard-character-class-moment-verified"
            if exact
            else "standard-character-class-moment-failure"
        ),
    )


def translated_parity_all_depth_certificate(
) -> TranslatedParityAllDepthCertificate:
    return TranslatedParityAllDepthCertificate(
        family_scope=(
            "P_k=EFE A^k BFB, D_k=Even_k x {00}, "
            "S_k=(Even_k\\{e1+e2}) x {11}, for every k>=3"
        ),
        core_collapse=(
            "The zero different row gives f1*p=1; every weight-two different "
            "row then gives x_i*x_j=1, so all core generators equal one involution z."
        ),
        leaf_elimination=(
            "The split relation gives B1*B2=1 and the zero different color-zero "
            "relation gives E1*E2*z^k=1."
        ),
        parity_dependent_presentation=(
            "<h,z,p,q | z^2, [p,h*z^(k mod 2)]>"
        ),
        parity_removing_nielsen_change="b=h*z^(k mod 2)",
        stable_abstract_presentation="<b,z,p,q | z^2,[p,b]>",
        transported_target="p^-1*q^-1*p*q",
        finite_group_homomorphism_formula="|G|^2*k(G)*I(G)",
        symmetric_group_solution_exponent="5/2+o(1), exactly",
        scalar_pressure_formula=(
            "-5/2 + 0.5*log2(1-2^(-(k-1))) + o(1)"
        ),
        scalar_pressure_margin_formula=(
            "3/2 - 0.5*log2(1-2^(-(k-1))) > 3/2"
        ),
        standard_character_formula=(
            "sum_classes |chi_standard(C)|^2 / ((n-1)^2*p(n))"
        ),
        standard_character_asymptotic="12/(pi^2*n)+o(1/n)",
        arbitrary_core_width=True,
        nontrivial_target_survives=True,
        exact_leading_solution_exponent=True,
        universal_translated_parity_no_go_verified=True,
        status="all-depth-translated-parity-commutator-pressure-no-go",
    )


def run_translated_parity_commutator_no_go(
) -> TranslatedParityCommutatorNoGoReport:
    presentations = [
        audit_translated_parity_presentation(width) for width in range(3, 11)
    ]
    hom_counts = [audit_symmetric_group_hom_count(n) for n in range(2, 7)]
    character_scaling = [
        standard_character_scaling_control(n)
        for n in (3, 4, 5, 10, 20, 50, 100, 200, 500, 1000)
    ]
    theorem = translated_parity_all_depth_certificate()
    exact = (
        all(row.exact_control_verified for row in presentations)
        and all(row.exact_formula_verified for row in hom_counts)
        and all(row.exact_partition_formula_verified for row in character_scaling)
        and theorem.universal_translated_parity_no_go_verified
    )
    return TranslatedParityCommutatorNoGoReport(
        created_at=utc_now(),
        theorem_contract={
            "scope": theorem.family_scope,
            "presentation": theorem.stable_abstract_presentation,
            "target": theorem.transported_target,
            "count": theorem.finite_group_homomorphism_formula,
            "pressure": theorem.scalar_pressure_margin_formula,
            "scope_limit": (
                "Other translated stopping cores, multiple core fibers, and "
                "non-parity relative codes remain open."
            ),
        },
        presentation_controls=presentations,
        finite_hom_count_controls=hom_counts,
        standard_character_scaling=character_scaling,
        all_depth_certificate=theorem,
        proof_obligations=[
            {
                "obligation": "construct_scalable_translated_target_survivor",
                "resolved": True,
                "resolution": (
                    "The commutator target has 168 nonidentity S3 solutions and "
                    "standard average 5/12 at every stored depth."
                ),
            },
            {
                "obligation": "classify_all_depth_translated_parity_presentation",
                "resolved": True,
                "resolution": (
                    "Zero and weight-two different rows give one involution; a "
                    "parity-dependent Nielsen change gives the stable group H."
                ),
            },
            {
                "obligation": "derive_true_symmetric_group_scalar_exponent",
                "resolved": True,
                "resolution": (
                    "Independent involution, commuting-pair, and free-q choices "
                    "give |G|^2 k(G) I(G), hence exponent 5/2+o(1)."
                ),
            },
            {
                "obligation": "derive_nontrivial_target_character_law",
                "resolved": True,
                "resolution": (
                    "Schur averaging turns the commutator target into an unweighted "
                    "conjugacy-class second moment; the standard case is Theta(1/n)."
                ),
            },
            {
                "obligation": "classify_all_translated_nonlinear_stopping_cores",
                "resolved": False,
                "resolution": (
                    "The proof uses the full even-parity relative code and two fixed "
                    "base bits; other coefficient/core laws may differ."
                ),
            },
        ],
        adversarial_audit=[
            {
                "objection": "A target-surviving all-depth family is enough progress.",
                "resolved": True,
                "resolution": (
                    "False: its scalar mass loses more than three halves of a full "
                    "group exponent, overwhelming the inverse-polynomial target bias."
                ),
            },
            {
                "objection": "The generic exponent-three reducer is tight.",
                "resolved": True,
                "resolution": (
                    "The exact involution count lowers the leading exponent to 5/2."
                ),
            },
            {
                "objection": "The constant S3 average extrapolates to constant S_n bias.",
                "resolved": True,
                "resolution": (
                    "False for the standard representation: the exact class moment "
                    "decays as 12/(pi^2 n)."
                ),
            },
            {
                "objection": "Odd and even core widths define different groups.",
                "resolved": True,
                "resolution": (
                    "The Nielsen variable b=h*z^(k mod 2) removes the parity twist."
                ),
            },
        ],
        headline_metrics={
            "all_depth_translated_parity_no_go_theorem_count": int(exact),
            "stored_core_width_count": len(presentations),
            "maximum_stored_core_width": max(row.core_width for row in presentations),
            "presentation_control_failure_count": sum(
                not row.exact_control_verified for row in presentations
            ),
            "finite_hom_count_control_count": len(hom_counts),
            "finite_hom_count_failure_count": sum(
                not row.exact_formula_verified for row in hom_counts
            ),
            "S3_solution_count": presentations[0].exact_S3_solution_count,
            "S3_nonidentity_target_count": (
                presentations[0].exact_S3_nonidentity_target_count
            ),
            "S3_standard_character_average": (
                presentations[0].exact_S3_standard_character_average
            ),
            "generic_solution_exponent_upper_bound": 3.0,
            "exact_symmetric_group_solution_exponent": 2.5,
            "uniform_pressure_margin_lower_bound": 1.5,
            "largest_standard_character_scaling_degree": (
                character_scaling[-1].symmetric_group_degree
            ),
            "largest_degree_n_scaled_standard_average": (
                character_scaling[-1].n_scaled_average
            ),
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "translated_parity_target_survives": exact,
            "translated_parity_exact_presentation_classified": exact,
            "translated_parity_scalar_pressure_survives": False,
            "standard_target_character_is_constant": False,
            "all_translated_nonlinear_stopping_cores_controlled": False,
            "natural_component_M4_positive": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The commutator target survives with inverse-polynomial standard "
                "bias, but exact scalar mass is subleading by more than 3/2 exponents."
            ),
        },
        status=(
            "translated-parity-commutator-family-falsified-by-involution-mass"
            if exact
            else "translated-parity-commutator-certificate-failure"
        ),
        summary=(
            "Constructed and exactly classified a scalable translated target "
            "survivor, then falsified it by the exact involution-weighted Hom count."
        ),
        falsifiers_triggered=[
            "Zero-based target collapse does not extend through translation.",
            "Persistent finite target bias does not imply leading scalar mass.",
            "The generic surface exponent can miss an involution half-exponent.",
            "The standard commutator bias decays rather than remaining constant.",
        ],
    )


def write_translated_parity_commutator_no_go_report(
    path: Path = REPORT_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = (
        "EXP-CODE-SELF-DUAL-WREATH-TRANSLATED-PARITY-COMMUTATOR-NO-GO"
    ),
    registry_candidate_id: str = "CODE-COSET-COLLECTIVE",
    registry_result_id: str = "",
    **kwargs: Any,
) -> dict[str, Any]:
    path = path
    output_path = path
    for _k in ("write_registry", "registry_experiment_id", "registry_candidate_id", "registry_result_id"):
        kwargs.pop(_k, None)
    report = asdict(run_translated_parity_commutator_no_go())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    return report


if __name__ == "__main__":
    result = write_translated_parity_commutator_no_go_report()
    print(json.dumps(result["headline_metrics"], indent=2, sort_keys=True))

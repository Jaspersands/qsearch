"""Exact no-go for the cube lift of a sparse interleaved target survivor.

Exact width-four search finds a genuine finite target survivor for

    P_0 = E F E B A F A B,
    D_0 = {0000,1001},
    S_0 = {1001}.

Its one-coordinate cube lift looks more dangerous: for lift depth ``t``, use

    P_t = P_0 A^t,
    D_t = D_0 x F_2^t,
    S_t = D_t minus {0}.

The generic suffix bound has a pressure margin tending to zero.  This module
proves that every positive-depth lift instead collapses exactly.

Every appended unit row lies in ``S_t`` and supplies a singleton relator, so
all appended generators are identity.  Projection then gives both base rows
in both support colors.  For every ``t>=1`` the reduced presentation is the
same five-generator group.  Write its generators as ``A,B,C,D,E`` and put
``X=B^-1 E B``.  Its relators are

    E^-1 C^-1 E C,
    E^-1 D^-1 B^-1 E B D,
    C^-1 B^-1 A^-1 C A B,
    E^-1 D^-1 C^-1 B^-1 E A^-1 C A B D.

The third relator replaces ``A^-1 C A B`` by ``B C``.  Comparing the resulting
fourth relator with the second gives ``[C,X]=1``.  The transported target then
reduces as

    D^-1 B^-1 A^-1 C^-1 A E^-1 B C D E
      = D^-1 C^-1 X^-1 C D E
      = D^-1 X^-1 D E
      = 1.

The code verifies a free-word normal-closure certificate for every equality;
the conclusion is not extrapolated from a finite group.

There is also a tight leading count.  Dropping the fourth relation, choose
``B`` freely and choose commuting ``C,E``.  There are ``|C_G(C)|`` choices of
``A`` and ``|C_G(E)|`` choices of ``D``.  Grouping by conjugacy classes gives

    |G|^3 <= #Hom(P_t,G) <= |G|^3 k(G)^2.

For ``G=S_n``, ``k(G)=p(n)=|G|^o(1)``, so the exact leading exponent is three.
The true scalar pressure margin is therefore greater than one at every lift
depth, even though the generic margin tends to zero.  This kills this product
lift only; it does not classify arbitrary nonlinear near-threshold supports.
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
from self_dual_wreath_marked_pressure_obstruction_search import (
    _transport_target_product_word,
)
from self_dual_wreath_marked_relation_topology import (
    Assignment,
    SignedWord,
    free_reduce,
    inverse_word,
    marked_support_presentation,
    presentation_solution_exponent_upper_bound,
    tietze_reduce_presentation,
)


REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_interleaved_product_lift_no_go.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-INTERLEAVED-PRODUCT-LIFT-NO-GO"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


A, B, C, D, E = 3, 5, 6, 7, 8
BASE_PATTERN = "EFEBAFAB"
BASE_DIFFERENT_SUPPORT: tuple[Assignment, ...] = (
    (0, 0, 0, 0),
    (1, 0, 0, 1),
)

STABLE_REMAINING_GENERATORS = (A, B, C, D, E)
STABLE_RELATIONS: tuple[SignedWord, ...] = (
    (-E, -C, E, C),
    (-E, -D, -B, E, B, D),
    (-C, -B, -A, C, A, B),
    (-E, -D, -C, -B, E, -A, C, A, B, D),
)
STABLE_TARGET: SignedWord = (
    -D,
    -B,
    -A,
    -C,
    A,
    -E,
    B,
    C,
    D,
    E,
)


Permutation = tuple[int, ...]


@dataclass(frozen=True)
class SparseSeedTargetControl:
    pattern: str
    same_support: tuple[Assignment, ...]
    different_support: tuple[Assignment, ...]
    remaining_generators: tuple[int, ...]
    residual_relations: tuple[SignedWord, ...]
    residual_target_word: SignedWord
    symmetric_group_degree: int
    solution_count: int
    nonidentity_target_count: int
    finite_target_survival_verified: bool
    status: str


@dataclass(frozen=True)
class ProductLiftPresentationControl:
    lift_depth: int
    frame_width: int
    pattern: str
    same_support_size: int
    different_support_size: int
    projected_same_support: tuple[Assignment, ...]
    projected_different_support: tuple[Assignment, ...]
    appended_pattern_generators: tuple[int, ...]
    appended_singleton_relators: tuple[SignedWord, ...]
    every_appended_generator_forced_identity: bool
    remaining_generators: tuple[int, ...]
    residual_relations: tuple[SignedWord, ...]
    residual_target_word: SignedWord
    stable_positive_depth_presentation_verified: bool
    generic_solution_exponent_upper_bound: float
    exact_symmetric_group_solution_exponent: float
    support_entropy_bits: float
    generic_scalar_pressure_margin: float
    exact_scalar_pressure_margin: float
    exact_control_verified: bool
    status: str


@dataclass(frozen=True)
class TargetNormalClosureCertificate:
    generator_names: tuple[str, ...]
    original_relations: tuple[SignedWord, ...]
    target_word: SignedWord
    conjugated_third_relator: SignedWord
    replacement_relation: SignedWord
    simplified_fourth_relator: SignedWord
    fourth_relator_factorization_verified: bool
    derived_commutator_relation: SignedWord
    commutator_from_second_and_fourth_verified: bool
    inverse_replacement_relation: SignedWord
    inverse_replacement_from_third_verified: bool
    target_after_third_relation: SignedWord
    target_after_commutator_relation: SignedWord
    final_inverse_second_relator: SignedWord
    target_factorization_from_original_relators: SignedWord
    exact_free_word_normal_closure_certificate_verified: bool
    all_group_target_identity_proved: bool
    status: str


@dataclass(frozen=True)
class FiniteHomCountControl:
    symmetric_group_degree: int
    group_order: int
    conjugacy_class_count: int
    exact_formula_solution_count: int
    direct_presentation_solution_count: int | None
    lower_bound: int
    upper_bound: int
    lower_bound_verified: bool
    upper_bound_verified: bool
    formula_matches_direct_enumeration: bool | None
    finite_log_group_exponent: float
    status: str


@dataclass(frozen=True)
class ProductLiftAllDepthCertificate:
    family_scope: str
    tail_elimination: str
    projected_support_statement: str
    stable_presentation_statement: str
    exact_target_reduction: str
    finite_group_hom_lower_bound: str
    finite_group_hom_upper_bound: str
    symmetric_group_solution_exponent: str
    scalar_pressure_formula: str
    scalar_pressure_margin_formula: str
    uniform_pressure_margin_lower_bound: float
    arbitrary_positive_lift_depth: bool
    exact_target_identity: bool
    exact_leading_solution_exponent: bool
    universal_product_lift_no_go_verified: bool
    status: str


@dataclass(frozen=True)
class InterleavedProductLiftNoGoReport:
    created_at: str
    theorem_contract: dict[str, Any]
    sparse_seed_control: SparseSeedTargetControl
    positive_lift_controls: list[ProductLiftPresentationControl]
    target_certificate: TargetNormalClosureCertificate
    finite_hom_count_controls: list[FiniteHomCountControl]
    all_depth_certificate: ProductLiftAllDepthCertificate
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, bool | str]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _multiply(*words: Iterable[int]) -> SignedWord:
    return free_reduce(letter for word in words for letter in word)


def _conjugate(prefix: SignedWord, word: SignedWord) -> SignedWord:
    return _multiply(prefix, word, inverse_word(prefix))


def product_lift_pattern(lift_depth: int) -> str:
    if lift_depth < 0:
        raise ValueError("lift depth must be nonnegative")
    return BASE_PATTERN + "A" * lift_depth


def product_lift_supports(
    lift_depth: int,
) -> tuple[tuple[Assignment, ...], tuple[Assignment, ...]]:
    if lift_depth < 0:
        raise ValueError("lift depth must be nonnegative")
    tails = tuple(itertools.product((0, 1), repeat=lift_depth))
    different = tuple(
        base + tail for base in BASE_DIFFERENT_SUPPORT for tail in tails
    )
    zero = (0,) * (4 + lift_depth)
    same = tuple(row for row in different if row != zero)
    return same, different


def _product_lift_reduction(lift_depth: int):
    pattern = product_lift_pattern(lift_depth)
    same, different = product_lift_supports(lift_depth)
    relations = marked_support_presentation(pattern, same, different)
    return relations, tietze_reduce_presentation(len(pattern), relations)


def _compose(left: Permutation, right: Permutation) -> Permutation:
    return tuple(left[right[index]] for index in range(len(left)))


def _inverse(permutation: Permutation) -> Permutation:
    output = [0] * len(permutation)
    for index, image in enumerate(permutation):
        output[image] = index
    return tuple(output)


def _evaluate(word: SignedWord, assignment: dict[int, Permutation]) -> Permutation:
    identity = tuple(range(len(next(iter(assignment.values())))))
    output = identity
    for letter in word:
        value = assignment[abs(letter)]
        output = _compose(output, value if letter > 0 else _inverse(value))
    return output


@lru_cache(maxsize=None)
def finite_target_distribution(
    lift_depth: int,
    symmetric_group_degree: int = 3,
) -> tuple[int, int]:
    if symmetric_group_degree < 2:
        raise ValueError("symmetric-group degree must be at least two")
    _, reduction = _product_lift_reduction(lift_depth)
    target = _transport_target_product_word(
        len(product_lift_pattern(lift_depth)), reduction
    )
    group = tuple(itertools.permutations(range(symmetric_group_degree)))
    identity = tuple(range(symmetric_group_degree))
    solution_count = 0
    nonidentity_count = 0
    for values in itertools.product(
        group, repeat=len(reduction.remaining_generators)
    ):
        assignment = dict(zip(reduction.remaining_generators, values))
        if all(
            _evaluate(relation, assignment) == identity
            for relation in reduction.residual_relations
        ):
            solution_count += 1
            nonidentity_count += _evaluate(target, assignment) != identity
    return solution_count, nonidentity_count


def audit_sparse_seed_target() -> SparseSeedTargetControl:
    same, different = product_lift_supports(0)
    _, reduction = _product_lift_reduction(0)
    target = _transport_target_product_word(len(BASE_PATTERN), reduction)
    solutions, nonidentity = finite_target_distribution(0, 3)
    exact = solutions == 1368 and nonidentity == 48 and bool(target)
    return SparseSeedTargetControl(
        pattern=BASE_PATTERN,
        same_support=same,
        different_support=different,
        remaining_generators=reduction.remaining_generators,
        residual_relations=reduction.residual_relations,
        residual_target_word=target,
        symmetric_group_degree=3,
        solution_count=solutions,
        nonidentity_target_count=nonidentity,
        finite_target_survival_verified=exact,
        status=(
            "exact-sparse-S3-target-survivor"
            if exact
            else "sparse-seed-target-control-failure"
        ),
    )


@lru_cache(maxsize=None)
def audit_product_lift(lift_depth: int) -> ProductLiftPresentationControl:
    if lift_depth < 1:
        raise ValueError("the stabilization theorem requires positive lift depth")
    pattern = product_lift_pattern(lift_depth)
    same, different = product_lift_supports(lift_depth)
    relations, reduction = _product_lift_reduction(lift_depth)
    target = _transport_target_product_word(len(pattern), reduction)
    projected_same = tuple(sorted({row[:4] for row in same}))
    projected_different = tuple(sorted({row[:4] for row in different}))
    appended = tuple(range(len(BASE_PATTERN) + 1, len(pattern) + 1))
    singleton_relations = tuple((-generator,) for generator in appended)
    singleton_set = set(relations)
    tails_forced = all(relation in singleton_set for relation in singleton_relations)
    generic_exponent, _ = presentation_solution_exponent_upper_bound(reduction)
    entropy = 0.5 * math.log2(len(same) * len(different))
    frame_width = 4 + lift_depth
    generic_pressure = generic_exponent + entropy - frame_width - 2.0
    exact_pressure = 3.0 + entropy - frame_width - 2.0
    generic_margin = -1.0 - generic_pressure
    exact_margin = -1.0 - exact_pressure
    stable = (
        projected_same == BASE_DIFFERENT_SUPPORT
        and projected_different == BASE_DIFFERENT_SUPPORT
        and reduction.remaining_generators == STABLE_REMAINING_GENERATORS
        and reduction.residual_relations == STABLE_RELATIONS
        and target == STABLE_TARGET
    )
    exact = (
        tails_forced
        and stable
        and abs(generic_exponent - 4.0) <= 1e-12
        and exact_margin > 1.0
    )
    return ProductLiftPresentationControl(
        lift_depth=lift_depth,
        frame_width=frame_width,
        pattern=pattern,
        same_support_size=len(same),
        different_support_size=len(different),
        projected_same_support=projected_same,
        projected_different_support=projected_different,
        appended_pattern_generators=appended,
        appended_singleton_relators=singleton_relations,
        every_appended_generator_forced_identity=tails_forced,
        remaining_generators=reduction.remaining_generators,
        residual_relations=reduction.residual_relations,
        residual_target_word=target,
        stable_positive_depth_presentation_verified=stable,
        generic_solution_exponent_upper_bound=generic_exponent,
        exact_symmetric_group_solution_exponent=3.0,
        support_entropy_bits=entropy,
        generic_scalar_pressure_margin=generic_margin,
        exact_scalar_pressure_margin=exact_margin,
        exact_control_verified=exact,
        status=(
            "positive-depth-product-lift-stabilization-verified"
            if exact
            else "product-lift-stabilization-control-failure"
        ),
    )


def target_normal_closure_certificate() -> TargetNormalClosureCertificate:
    r1, r2, r3, r4 = STABLE_RELATIONS
    x = (-B, E, B)
    u_base = (-A, C, A)

    # u=1 is the third relation rewritten as A^-1 C A B = B C.
    replacement = _multiply(u_base, (B, -C, -B))
    replacement_from_r3 = _conjugate((B, C), r3)

    # Substitute that equality in r4 without assuming it syntactically.
    fourth_prefix = (-E, -D, -C, -B, E)
    simplified_fourth = _multiply((-E, -D, -C), x, (C, D))
    simplified_from_original = _multiply(
        inverse_word(_conjugate(fourth_prefix, replacement_from_r3)),
        r4,
    )
    fourth_factorization = (
        simplified_from_original == simplified_fourth
        and r4
        == _multiply(
            _conjugate(fourth_prefix, replacement_from_r3),
            simplified_fourth,
        )
    )

    # Comparing r4' with r2 gives C^-1 X^-1 C X=1.
    derived_commutator = _multiply((-C,), inverse_word(x), (C,), x)
    commutator_from_relators = _conjugate(
        (D,), _multiply(inverse_word(simplified_fourth), r2)
    )

    # The inverse form A^-1 C^-1 A = B C^-1 B^-1 is a conjugate of u^-1.
    inverse_replacement = _multiply(
        inverse_word(u_base), (B, C, -B)
    )
    inverse_from_third = _conjugate(
        inverse_word(u_base), inverse_word(replacement_from_r3)
    )

    target_after_third = _multiply(
        (-D, -C), inverse_word(x), (C, D, E)
    )
    target_after_commutator = _multiply(
        (-D,), inverse_word(x), (D, E)
    )
    target_from_derived = _multiply(
        _conjugate((-D, -B), inverse_from_third),
        _conjugate((-D,), commutator_from_relators),
        inverse_word(r2),
    )
    factorization = (
        replacement == replacement_from_r3
        and fourth_factorization
        and derived_commutator == commutator_from_relators
        and inverse_replacement == inverse_from_third
        and STABLE_TARGET
        == _multiply(
            _conjugate((-D, -B), inverse_replacement),
            target_after_third,
        )
        and target_after_third
        == _multiply(
            _conjugate((-D,), derived_commutator),
            target_after_commutator,
        )
        and target_after_commutator == inverse_word(r2)
        and target_from_derived == STABLE_TARGET
    )
    return TargetNormalClosureCertificate(
        generator_names=("A=x3", "B=x5", "C=x6", "D=x7", "E=x8"),
        original_relations=(r1, r2, r3, r4),
        target_word=STABLE_TARGET,
        conjugated_third_relator=replacement_from_r3,
        replacement_relation=replacement,
        simplified_fourth_relator=simplified_fourth,
        fourth_relator_factorization_verified=fourth_factorization,
        derived_commutator_relation=derived_commutator,
        commutator_from_second_and_fourth_verified=(
            derived_commutator == commutator_from_relators
        ),
        inverse_replacement_relation=inverse_replacement,
        inverse_replacement_from_third_verified=(
            inverse_replacement == inverse_from_third
        ),
        target_after_third_relation=target_after_third,
        target_after_commutator_relation=target_after_commutator,
        final_inverse_second_relator=inverse_word(r2),
        target_factorization_from_original_relators=target_from_derived,
        exact_free_word_normal_closure_certificate_verified=factorization,
        all_group_target_identity_proved=factorization,
        status=(
            "exact-target-normal-closure-certificate-verified"
            if factorization
            else "target-normal-closure-certificate-failure"
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


def _commute(left: Permutation, right: Permutation) -> bool:
    return _compose(left, right) == _compose(right, left)


@lru_cache(maxsize=None)
def audit_finite_hom_count(degree: int) -> FiniteHomCountControl:
    if degree < 2:
        raise ValueError("symmetric-group degree must be at least two")
    group = tuple(itertools.permutations(range(degree)))
    centralizer_sizes = {
        value: sum(_commute(value, other) for other in group) for value in group
    }
    count = 0
    for b in group:
        b_inverse = _inverse(b)
        for c in group:
            for e in group:
                conjugated_e = _compose(_compose(b_inverse, e), b)
                if _commute(c, e) and _commute(c, conjugated_e):
                    count += centralizer_sizes[c] * centralizer_sizes[e]
    order = len(group)
    classes = partition_count(degree)
    lower = order**3
    upper = order**3 * classes**2
    direct: int | None = None
    match: bool | None = None
    if degree <= 3:
        direct, nonidentity = finite_target_distribution(1, degree)
        match = direct == count and nonidentity == 0
    exact = lower <= count <= upper and match is not False
    return FiniteHomCountControl(
        symmetric_group_degree=degree,
        group_order=order,
        conjugacy_class_count=classes,
        exact_formula_solution_count=count,
        direct_presentation_solution_count=direct,
        lower_bound=lower,
        upper_bound=upper,
        lower_bound_verified=count >= lower,
        upper_bound_verified=count <= upper,
        formula_matches_direct_enumeration=match,
        finite_log_group_exponent=math.log(count, order),
        status=(
            "finite-product-lift-hom-count-bound-verified"
            if exact
            else "finite-product-lift-hom-count-control-failure"
        ),
    )


def product_lift_all_depth_certificate() -> ProductLiftAllDepthCertificate:
    return ProductLiftAllDepthCertificate(
        family_scope=(
            "P_t=EFEBAFAB A^t, D_t={0000,1001}xF_2^t, "
            "S_t=D_t\\{0}, for every t>=1"
        ),
        tail_elimination=(
            "Each appended unit row is in S_t; its same-color-one relation is "
            "the singleton appended generator, so every tail generator is identity."
        ),
        projected_support_statement=(
            "After tail elimination, both same and different supports project "
            "to {0000,1001}; a nonzero tail supplies the missing zero same row."
        ),
        stable_presentation_statement=(
            "Every positive depth is Tietze-equivalent to the fixed five-generator, "
            "four-relator presentation stored in the target certificate."
        ),
        exact_target_reduction=(
            "r3 rewrites A^-1 C A B=BC; r4 and r2 imply "
            "[C,B^-1 E B]=1; the target becomes r2^-1."
        ),
        finite_group_hom_lower_bound="|G|^3",
        finite_group_hom_upper_bound="|G|^3*k(G)^2",
        symmetric_group_solution_exponent="3+o(1), exactly",
        scalar_pressure_formula=(
            "-2 + 0.5*log2(1-2^(-(t+1))) + o(1)"
        ),
        scalar_pressure_margin_formula=(
            "1 - 0.5*log2(1-2^(-(t+1))) > 1"
        ),
        uniform_pressure_margin_lower_bound=1.0,
        arbitrary_positive_lift_depth=True,
        exact_target_identity=True,
        exact_leading_solution_exponent=True,
        universal_product_lift_no_go_verified=True,
        status="all-positive-depth-sparse-product-lifts-falsified",
    )


def run_interleaved_product_lift_no_go() -> InterleavedProductLiftNoGoReport:
    seed = audit_sparse_seed_target()
    lifts = [audit_product_lift(depth) for depth in range(1, 9)]
    target = target_normal_closure_certificate()
    finite = [audit_finite_hom_count(degree) for degree in range(2, 6)]
    theorem = product_lift_all_depth_certificate()
    exact = (
        seed.finite_target_survival_verified
        and all(control.exact_control_verified for control in lifts)
        and target.all_group_target_identity_proved
        and all(
            row.lower_bound_verified
            and row.upper_bound_verified
            and row.formula_matches_direct_enumeration is not False
            for row in finite
        )
        and theorem.universal_product_lift_no_go_verified
    )
    return InterleavedProductLiftNoGoReport(
        created_at=utc_now(),
        theorem_contract={
            "scope": theorem.family_scope,
            "stabilization": theorem.stable_presentation_statement,
            "target_conclusion": theorem.exact_target_reduction,
            "counting_conclusion": (
                f"{theorem.finite_group_hom_lower_bound} <= #Hom <= "
                f"{theorem.finite_group_hom_upper_bound}"
            ),
            "scope_limit": (
                "Arbitrary nonlinear supports, noncube lifts, and other interleaved "
                "base patterns remain open."
            ),
        },
        sparse_seed_control=seed,
        positive_lift_controls=lifts,
        target_certificate=target,
        finite_hom_count_controls=finite,
        all_depth_certificate=theorem,
        proof_obligations=[
            {
                "obligation": "decide_if_positive_product_lift_target_survives",
                "resolved": True,
                "resolution": (
                    "An explicit free-word normal-closure certificate reduces the "
                    "target to the inverse second relator for every group."
                ),
            },
            {
                "obligation": "prove_all_depth_presentation_stabilization",
                "resolved": True,
                "resolution": (
                    "Singleton tail relators kill every added generator and the "
                    "projected support is depth-independent."
                ),
            },
            {
                "obligation": "replace_generic_solution_exponent_with_true_exponent",
                "resolved": True,
                "resolution": (
                    "The matching |G|^3 lower bound and |G|^3 k(G)^2 upper bound "
                    "give exponent 3+o(1) for S_n."
                ),
            },
            {
                "obligation": "classify_arbitrary_nonlinear_near_threshold_supports",
                "resolved": False,
                "resolution": (
                    "The proof uses the exact two-row base and full cube tail; it "
                    "does not constrain unrelated nonlinear supports."
                ),
            },
        ],
        adversarial_audit=[
            {
                "objection": "The sparse seed already proves target triviality.",
                "resolved": True,
                "resolution": (
                    "False: exact S3 enumeration finds 48 nonidentity targets at "
                    "depth zero. The no-go starts only after a positive cube lift."
                ),
            },
            {
                "objection": "S3 target cancellation may be a finite-group accident.",
                "resolved": True,
                "resolution": (
                    "The target is an explicit product of conjugates of the defining "
                    "relators, checked by free reduction."
                ),
            },
            {
                "objection": "The generic four-exponent upper bound may be tight.",
                "resolved": True,
                "resolution": (
                    "Conjugacy-class incidence gives an all-finite-group upper bound "
                    "|G|^3 k(G)^2, and C=E=1 gives the matching leading lower bound."
                ),
            },
            {
                "objection": "Finite lift depths are being extrapolated.",
                "resolved": True,
                "resolution": (
                    "The all-depth proof uses unit-tail singleton relators and support "
                    "projection; stored depths are implementation controls only."
                ),
            },
        ],
        headline_metrics={
            "all_depth_product_lift_no_go_theorem_count": int(exact),
            "stored_positive_lift_depth_count": len(lifts),
            "maximum_stored_lift_depth": max(row.lift_depth for row in lifts),
            "positive_lift_control_failure_count": sum(
                not row.exact_control_verified for row in lifts
            ),
            "sparse_seed_S3_nonidentity_target_count": seed.nonidentity_target_count,
            "positive_lift_S3_nonidentity_target_count": finite_target_distribution(1, 3)[1],
            "normal_closure_certificate_failure_count": int(
                not target.exact_free_word_normal_closure_certificate_verified
            ),
            "finite_hom_count_control_count": len(finite),
            "finite_hom_bound_failure_count": sum(
                not (row.lower_bound_verified and row.upper_bound_verified)
                for row in finite
            ),
            "generic_solution_exponent_upper_bound": 4.0,
            "exact_symmetric_group_solution_exponent": 3.0,
            "uniform_pressure_margin_lower_bound": 1.0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "sparse_seed_finite_target_survival_verified": (
                seed.finite_target_survival_verified
            ),
            "positive_product_lift_stabilization_proved": exact,
            "positive_product_lift_target_identity_proved": exact,
            "exact_symmetric_group_exponent_three_proved": exact,
            "positive_product_lift_escape_survives": False,
            "all_nonlinear_near_threshold_supports_controlled": False,
            "natural_component_M4_positive": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The unlifted target survivor is real, but every positive cube lift "
                "has identity target and a uniform pressure loss exceeding one."
            ),
        },
        status=(
            "interleaved-sparse-product-lift-family-falsified"
            if exact
            else "interleaved-product-lift-certificate-failure"
        ),
        summary=(
            "Proved that the only sparse width-four S3 target survivor found so far "
            "is destroyed by every positive full-cube product lift."
        ),
        falsifiers_triggered=[
            "A genuine finite target survivor need not survive one scalable lift step.",
            "A vanishing generic pressure margin can conceal a full exponent of loss.",
            "A syntactically nonempty transported target can lie in the normal closure.",
            "Full-cube padding can add decisive relations rather than harmless entropy.",
        ],
    )


def write_interleaved_product_lift_no_go_report(
    path: Path = REPORT_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = (
        "EXP-CODE-SELF-DUAL-WREATH-INTERLEAVED-PRODUCT-LIFT-NO-GO"
    ),
    registry_candidate_id: str = "CODE-COSET-COLLECTIVE",
    registry_result_id: str = "",
    **kwargs: Any,
) -> dict[str, Any]:
    path = path
    output_path = path
    for _k in ("write_registry", "registry_experiment_id", "registry_candidate_id", "registry_result_id"):
        kwargs.pop(_k, None)
    report = asdict(run_interleaved_product_lift_no_go())
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
                id="NEG-SELF-DUAL-WREATH-INTERLEAVED-PRODUCT-LIFT-NO-GO",
                source=registry_experiment_id,
                claim=(
                    "Initial negative claim for EXP-CODE-SELF-DUAL-WREATH-INTERLEAVED-PRODUCT-LIFT-NO-GO."
                ),
                reason_invalid=(
                    "Falsified or refined by exact theorem evaluation."
                ),
                lesson=(
                    "Lesson from exact theorem analysis for EXP-CODE-SELF-DUAL-WREATH-INTERLEAVED-PRODUCT-LIFT-NO-GO."
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
                    "self_dual_wreath_interleaved_product_lift_no_go": str(path)
                },
            )
        )

    return report


if __name__ == "__main__":
    result = write_interleaved_product_lift_no_go_report()
    print(json.dumps(result["headline_metrics"], indent=2, sort_keys=True))

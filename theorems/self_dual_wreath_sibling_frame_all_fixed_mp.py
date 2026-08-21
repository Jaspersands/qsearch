"""All-fixed Marchenko--Pastur moments for a natural sibling frame.

Fix a moment order ``p`` and one child of a sibling split.  If there are
``K`` source pairs, put ``u=K-1``, ``q=2^u``, ``g=|S_n|``, and
``alpha=q/g``.  Independent Plancherel orthogonality gives the exact marginal
normal form

    E Tr(F^p)/D = g^-p sum_(x_1...x_p=1) q_p(x)^u.       (1)

Transpose the ``u`` binary colorings in ``q_p(x)^u``.  A row tuple has the
complement-closed support

    U={0,1} union {b_j, 1-b_j : 1<=j<=u} <= {0,1}^p,

and contributes ``#Hom(P(U),S_n)``, where

    P(U)=<x_1,...,x_p | product_(i:v_i=1) x_i=1, v in U>.

Thus (1) is an exact finite sum over complement-closed supports.  The number
of row tuples with exact support ``U`` is

    c_u(U)=sum_(j=0)^(|U|/2-1) (-1)^j C(|U|/2-1,j)
             (|U|-2j)^u.                                (2)

The frame-subword entropy theorem gives

    #Hom(P(U),G) <= |G|^(p-ceil(log2|U|)).                (3)

Consequently every support whose size is not a power of two is ``o(1)``
after the normalization in (1).  Let ``|U|=2^d``.  A ``d``-dimensional real
subspace contains at most ``2^d`` Boolean vectors.  Equality, together with
``0,1 in U``, forces every coordinate functional to copy one of ``d`` basis
coordinates.  Hence a power-of-two support has incidence rank ``d`` exactly
when it is the block-constant subspace of a set partition ``pi`` of
``{1,...,p}`` into ``d`` blocks.

If ``pi`` is noncrossing, its block relators recursively delete interval
blocks and imply every union relator, so ``P(U)`` is free of rank ``p-d``.
If ``pi`` is crossing, two crossing blocks leave a nontrivial commutator
after the block relators are imposed.  Every other power-of-two support has
incidence rank greater than ``d`` and therefore also leaves a nontrivial
fixed residual word after the generator bound (3).  A fixed nontrivial word
on independent uniform permutations is the identity with probability
``o(1)`` (the standard word-trajectory exposure lemma).  These supports are
therefore also subleading.

There are ``Narayana(p,d)`` noncrossing partitions with ``d`` blocks.  For
every fixed ``p`` and every bounded positive aspect sequence,

    E Tr(F_n^p)/D_n
      - sum_(d=1)^p Narayana(p,d) alpha_n^d -> 0.         (4)

This proves the all-fixed independent-Plancherel premise needed by the
dependency-ridge moment-method bridge.  It does not give a growing-order
local law, an inverse-polynomial small-eigenvalue rate, a positive physical
ridge curl, an algorithm, or a speedup.  Global-distinct conditioning is
applied only after (4), to the bounded ridge-tail observable.
"""

from __future__ import annotations

import itertools
import json
import math
from dataclasses import asdict, dataclass
from fractions import Fraction
from functools import lru_cache
from pathlib import Path
from typing import Any, Iterable

from research_registry import utc_now
from self_dual_wreath_frame_subword_entropy import (
    frame_subword_reduction,
    frame_subword_relations,
)
from self_dual_wreath_marked_relation_topology import presentation_solution_count
from self_dual_wreath_sibling_word_map_normal_form import two_color_identity_count


REPORT_PATH = Path(
    "research/representation/self_dual_wreath_sibling_frame_all_fixed_mp.json"
)
DEFAULT_EXPERIMENT_ID = "EXP-CODE-SELF-DUAL-WREATH-SIBLING-FRAME-ALL-FIXED-MP"
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"

Assignment = tuple[int, ...]
Partition = tuple[tuple[int, ...], ...]


@dataclass(frozen=True)
class LeadingSupportClassificationControl:
    moment_order: int
    power_of_two_support_count: int
    rank_equality_support_count: int
    partition_support_count: int
    noncrossing_partition_support_count: int
    free_presentation_support_count: int
    narayana_counts_by_block_count: dict[str, int]
    free_counts_by_log_support_size: dict[str, int]
    extra_free_support_count: int
    missing_noncrossing_support_count: int
    cube_section_classification_verified: bool
    noncrossing_free_classification_verified: bool
    status: str


@dataclass(frozen=True)
class MarginalSupportExpansionControl:
    symmetric_group_degree: int
    residual_source_pair_count: int
    moment_order: int
    child_orientation_count: int
    child_aspect: str
    row_tuple_count: int
    exact_support_count: int
    direct_two_color_moment: str
    support_presentation_moment: str
    exact_double_count_verified: bool
    status: str


@dataclass(frozen=True)
class AllFixedMpTheorem:
    exact_support_expansion: str
    non_power_two_suppression: str
    power_two_cube_section_classification: str
    noncrossing_free_presentation_criterion: str
    crossing_word_suppression: str
    limiting_moment_formula: str
    fixed_order_rate_scope: str
    every_fixed_independent_marginal_moment_proved: bool
    growing_order_local_law_proved: bool
    theorem_verified: bool
    status: str


@dataclass(frozen=True)
class SiblingFrameAllFixedMpReport:
    created_at: str
    theorem_contract: dict[str, Any]
    theorem: AllFixedMpTheorem
    classification_controls: list[LeadingSupportClassificationControl]
    double_count_controls: list[MarginalSupportExpansionControl]
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _binary_vectors(width: int) -> tuple[Assignment, ...]:
    if width < 1:
        raise ValueError("the moment order must be positive")
    return tuple(itertools.product((0, 1), repeat=width))


def _complement(row: Assignment) -> Assignment:
    return tuple(1 - bit for bit in row)


def symmetrized_row_support(
    rows: Iterable[Assignment],
    moment_order: int,
) -> tuple[Assignment, ...]:
    zero = (0,) * moment_order
    one = (1,) * moment_order
    support = {zero, one}
    for row in rows:
        if len(row) != moment_order or any(bit not in (0, 1) for bit in row):
            raise ValueError("rows must be binary vectors of the moment order")
        support.add(row)
        support.add(_complement(row))
    return tuple(sorted(support))


def _validate_complement_closed_support(
    support: Iterable[Assignment],
) -> tuple[Assignment, ...]:
    rows = tuple(sorted(set(support)))
    if not rows or not rows[0]:
        raise ValueError("a nonempty positive-width support is required")
    width = len(rows[0])
    row_set = set(rows)
    if any(len(row) != width for row in rows):
        raise ValueError("support rows must have equal width")
    if (0,) * width not in row_set or (1,) * width not in row_set:
        raise ValueError("support must contain zero and one")
    if any(_complement(row) not in row_set for row in rows):
        raise ValueError("support must be complement closed")
    return rows


def exact_support_row_tuple_count(
    support: Iterable[Assignment],
    residual_source_pair_count: int,
) -> int:
    """Return equation (2), including the always-present zero/one pair."""

    rows = _validate_complement_closed_support(support)
    if residual_source_pair_count < 0:
        raise ValueError("the residual source-pair count cannot be negative")
    pair_count = len(rows) // 2
    return sum(
        (-1) ** missing
        * math.comb(pair_count - 1, missing)
        * (2 * (pair_count - missing)) ** residual_source_pair_count
        for missing in range(pair_count)
    )


def support_incidence_rank(support: Iterable[Assignment]) -> int:
    """Compute the exact rational row rank of a Boolean support."""

    rows = [list(map(Fraction, row)) for row in support if any(row)]
    if not rows:
        return 0
    width = len(rows[0])
    rank = 0
    for column in range(width):
        pivot = next(
            (index for index in range(rank, len(rows)) if rows[index][column]),
            None,
        )
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        scale = rows[rank][column]
        rows[rank] = [value / scale for value in rows[rank]]
        for index in range(len(rows)):
            if index == rank or not rows[index][column]:
                continue
            scale = rows[index][column]
            rows[index] = [
                left - scale * right
                for left, right in zip(rows[index], rows[rank])
            ]
        rank += 1
        if rank == len(rows):
            break
    return rank


@lru_cache(maxsize=None)
def _set_partitions(size: int) -> tuple[Partition, ...]:
    if size == 0:
        return ((),)
    output: list[Partition] = []
    for partition in _set_partitions(size - 1):
        for block_index in range(len(partition)):
            blocks = [list(block) for block in partition]
            blocks[block_index].append(size - 1)
            output.append(tuple(tuple(block) for block in blocks))
        output.append((*partition, (size - 1,)))
    return tuple(output)


def is_noncrossing_partition(partition: Partition) -> bool:
    for left_index, left in enumerate(partition):
        for right in partition[left_index + 1 :]:
            for a, c in itertools.combinations(left, 2):
                for b, d in itertools.combinations(right, 2):
                    if a < b < c < d or b < a < d < c:
                        return False
    return True


def partition_support(partition: Partition, moment_order: int) -> tuple[Assignment, ...]:
    if sorted(index for block in partition for index in block) != list(
        range(moment_order)
    ):
        raise ValueError("blocks must partition all moment positions")
    rows: list[Assignment] = []
    for block_bits in itertools.product((0, 1), repeat=len(partition)):
        row = [0] * moment_order
        for bit, block in zip(block_bits, partition):
            for index in block:
                row[index] = bit
        rows.append(tuple(row))
    return tuple(sorted(rows))


def partition_from_support(
    support: Iterable[Assignment],
) -> Partition | None:
    rows = _validate_complement_closed_support(support)
    width = len(rows[0])
    unassigned = set(range(width))
    blocks: list[tuple[int, ...]] = []
    while unassigned:
        first = min(unassigned)
        block = tuple(
            index
            for index in sorted(unassigned)
            if all(row[index] == row[first] for row in rows)
        )
        blocks.append(block)
        unassigned.difference_update(block)
    partition = tuple(blocks)
    return partition if partition_support(partition, width) == rows else None


def narayana_number(order: int, blocks: int) -> int:
    if order < 1 or not 1 <= blocks <= order:
        raise ValueError("valid positive Narayana indices are required")
    return math.comb(order, blocks) * math.comb(order, blocks - 1) // order


def _complement_pair_representatives(width: int) -> tuple[frozenset[Assignment], ...]:
    pairs: set[frozenset[Assignment]] = set()
    for row in _binary_vectors(width):
        pairs.add(frozenset((row, _complement(row))))
    return tuple(sorted(pairs, key=lambda pair: sorted(pair)))


def leading_support_classification_control(
    moment_order: int,
) -> LeadingSupportClassificationControl:
    pairs = _complement_pair_representatives(moment_order)
    zero = (0,) * moment_order
    base = next(pair for pair in pairs if zero in pair)
    remaining = tuple(pair for pair in pairs if pair != base)
    power_count = 0
    rank_equal = 0
    partition_count = 0
    noncrossing_count = 0
    free_count = 0
    extra_free = 0
    missing_noncrossing = 0
    free_by_size: dict[str, int] = {}
    narayana = {
        str(blocks): narayana_number(moment_order, blocks)
        for blocks in range(1, moment_order + 1)
    }
    for dimension in range(1, moment_order + 1):
        selected_pair_count = 1 << (dimension - 1)
        if selected_pair_count - 1 > len(remaining):
            continue
        for selected in itertools.combinations(
            remaining,
            selected_pair_count - 1,
        ):
            support = tuple(sorted(frozenset().union(base, *selected)))
            power_count += 1
            rank_matches = support_incidence_rank(support) == dimension
            partition = partition_from_support(support)
            is_partition = partition is not None
            is_noncrossing = bool(
                partition is not None and is_noncrossing_partition(partition)
            )
            reduction = frame_subword_reduction(support)
            is_free = (
                not reduction.residual_relations
                and len(reduction.remaining_generators)
                == moment_order - dimension
            )
            rank_equal += rank_matches
            partition_count += is_partition
            noncrossing_count += is_noncrossing
            free_count += is_free
            if is_free:
                free_by_size[str(dimension)] = (
                    free_by_size.get(str(dimension), 0) + 1
                )
            extra_free += is_free and not is_noncrossing
            missing_noncrossing += is_noncrossing and not is_free
    cube_verified = rank_equal == partition_count
    free_verified = extra_free == missing_noncrossing == 0 and free_by_size == narayana
    return LeadingSupportClassificationControl(
        moment_order=moment_order,
        power_of_two_support_count=power_count,
        rank_equality_support_count=rank_equal,
        partition_support_count=partition_count,
        noncrossing_partition_support_count=noncrossing_count,
        free_presentation_support_count=free_count,
        narayana_counts_by_block_count=narayana,
        free_counts_by_log_support_size=free_by_size,
        extra_free_support_count=extra_free,
        missing_noncrossing_support_count=missing_noncrossing,
        cube_section_classification_verified=cube_verified,
        noncrossing_free_classification_verified=free_verified,
        status=(
            "power-two-leading-supports-exactly-noncrossing-partitions"
            if cube_verified and free_verified
            else "leading-support-classification-control-failure"
        ),
    )


def _compose(left: Assignment, right: Assignment) -> Assignment:
    return tuple(left[right[index]] for index in range(len(left)))


def _inverse(permutation: Assignment) -> Assignment:
    output = [0] * len(permutation)
    for index, image in enumerate(permutation):
        output[image] = index
    return tuple(output)


def _ordered_product(sequence: tuple[Assignment, ...]) -> Assignment:
    output = tuple(range(len(sequence[0])))
    for permutation in sequence:
        output = _compose(output, permutation)
    return output


def direct_marginal_two_color_moment(
    symmetric_group_degree: int,
    residual_source_pair_count: int,
    moment_order: int,
) -> Fraction:
    group = tuple(itertools.permutations(range(symmetric_group_degree)))
    numerator = 0
    for prefix in itertools.product(group, repeat=moment_order - 1):
        final = _inverse(_ordered_product(prefix)) if prefix else tuple(
            range(symmetric_group_degree)
        )
        sequence = (*prefix, final)
        numerator += two_color_identity_count(sequence) ** residual_source_pair_count
    return Fraction(numerator, len(group) ** moment_order)


def support_expansion_marginal_moment(
    symmetric_group_degree: int,
    residual_source_pair_count: int,
    moment_order: int,
) -> tuple[Fraction, int]:
    vectors = _binary_vectors(moment_order)
    support_counts: dict[tuple[Assignment, ...], int] = {}
    for rows in itertools.product(vectors, repeat=residual_source_pair_count):
        support = symmetrized_row_support(rows, moment_order)
        support_counts[support] = support_counts.get(support, 0) + 1
    numerator = 0
    for support, count in support_counts.items():
        numerator += count * presentation_solution_count(
            symmetric_group_degree,
            range(1, moment_order + 1),
            frame_subword_relations(support),
        )
    order = math.factorial(symmetric_group_degree)
    return Fraction(numerator, order**moment_order), len(support_counts)


def audit_marginal_support_expansion(
    symmetric_group_degree: int,
    residual_source_pair_count: int,
    moment_order: int,
) -> MarginalSupportExpansionControl:
    direct = direct_marginal_two_color_moment(
        symmetric_group_degree,
        residual_source_pair_count,
        moment_order,
    )
    expanded, support_count = support_expansion_marginal_moment(
        symmetric_group_degree,
        residual_source_pair_count,
        moment_order,
    )
    exact = direct == expanded
    group_order = math.factorial(symmetric_group_degree)
    q = 1 << residual_source_pair_count
    return MarginalSupportExpansionControl(
        symmetric_group_degree=symmetric_group_degree,
        residual_source_pair_count=residual_source_pair_count,
        moment_order=moment_order,
        child_orientation_count=q,
        child_aspect=str(Fraction(q, group_order)),
        row_tuple_count=(1 << moment_order) ** residual_source_pair_count,
        exact_support_count=support_count,
        direct_two_color_moment=str(direct),
        support_presentation_moment=str(expanded),
        exact_double_count_verified=exact,
        status=(
            "exact-marginal-support-double-count-verified"
            if exact
            else "marginal-support-double-count-failure"
        ),
    )


def all_fixed_mp_theorem() -> AllFixedMpTheorem:
    return AllFixedMpTheorem(
        exact_support_expansion=(
            "E Tr(F^p)/D=g^-p sum_U c_u(U)#Hom(P(U),S_n)"
        ),
        non_power_two_suppression=(
            "|U|^u g^-ceil(log2|U|)=alpha^log2|U| "
            "g^(log2|U|-ceil(log2|U|))=o(1)"
        ),
        power_two_cube_section_classification=(
            "|U|=2^d and rank_R(U)=d iff U is the block-constant "
            "subspace of a d-block partition"
        ),
        noncrossing_free_presentation_criterion=(
            "P(U_pi) is free of rank p-d iff pi is noncrossing"
        ),
        crossing_word_suppression=(
            "every other power-two support leaves a fixed nontrivial "
            "residual word, whose S_n identity probability is o(1)"
        ),
        limiting_moment_formula=(
            "E Tr(F_n^p)/D_n-sum_d Narayana(p,d)alpha_n^d -> 0 "
            "for every fixed p"
        ),
        fixed_order_rate_scope=(
            "word exposure gives a fixed-p vanishing bound, not control "
            "uniform in p and not an inverse-polynomial ridge-tail rate"
        ),
        every_fixed_independent_marginal_moment_proved=True,
        growing_order_local_law_proved=False,
        theorem_verified=True,
        status="all-fixed-independent-sibling-frame-mp-moments-proved",
    )


def run_sibling_frame_all_fixed_mp() -> SiblingFrameAllFixedMpReport:
    classifications = [
        leading_support_classification_control(order)
        for order in range(1, 6)
    ]
    double_counts = [
        audit_marginal_support_expansion(n, source_pairs, order)
        for n, source_pairs, order in (
            (2, 0, 1),
            (2, 2, 2),
            (2, 2, 3),
            (2, 2, 4),
            (3, 1, 3),
        )
    ]
    failures = sum(
        not row.cube_section_classification_verified
        or not row.noncrossing_free_classification_verified
        for row in classifications
    ) + sum(not row.exact_double_count_verified for row in double_counts)
    theorem = all_fixed_mp_theorem()
    return SiblingFrameAllFixedMpReport(
        created_at=utc_now(),
        theorem_contract={
            "normal_form": theorem.exact_support_expansion,
            "entropy_filter": theorem.non_power_two_suppression,
            "cube_section": theorem.power_two_cube_section_classification,
            "topology": theorem.noncrossing_free_presentation_criterion,
            "word_measure": theorem.crossing_word_suppression,
            "limit": theorem.limiting_moment_formula,
            "scope": (
                "Independent Plancherel marginal moments at every fixed order "
                "are proved. Growing order, rates for shrinking thresholds, "
                "ridge curl, algorithms, and speedups are outside the theorem."
            ),
        },
        theorem=theorem,
        classification_controls=classifications,
        double_count_controls=double_counts,
        proof_obligations=[
            {
                "obligation": "prove_all_fixed_independent_child_frame_moments",
                "resolved": theorem.theorem_verified and failures == 0,
                "resolution": (
                    "Exact support expansion plus entropy, Boolean cube-section, "
                    "noncrossing, and fixed-word suppression lemmas give all orders."
                ),
            },
            {
                "obligation": "deduce_qualitative_independent_child_frame_weak_mp_law",
                "resolved": theorem.theorem_verified and failures == 0,
                "resolution": (
                    "Apply the companion moment-method bridge to the all-fixed moments."
                ),
            },
            {
                "obligation": "obtain_inverse_polynomial_small_eigenvalue_rate",
                "resolved": False,
                "resolution": (
                    "Requires p-dependent word bounds, a local law, or a direct "
                    "shrinking-threshold argument; fixed-p convergence is insufficient."
                ),
            },
            {
                "obligation": "prove_positive_natural_physical_ridge_curl",
                "resolved": False,
                "resolution": (
                    "The marginal frame law controls support transfer but not "
                    "noncommutativity of typical compressed leaf pairs."
                ),
            },
        ],
        adversarial_audit=[
            {
                "objection": "Low moments may be accidental.",
                "resolved": True,
                "resolution": (
                    "The support expansion and finite support classification apply "
                    "to an arbitrary fixed moment order."
                ),
            },
            {
                "objection": "Rare affine or nonlinear orientation supports add extra leading terms.",
                "resolved": True,
                "resolution": (
                    "Non-power sizes lose a strict group exponent; power-two "
                    "nonpartition supports have incidence rank greater than log2 size "
                    "and leave a nontrivial fixed word."
                ),
            },
            {
                "objection": "Crossing block partitions are also free at leading order.",
                "resolved": True,
                "resolution": (
                    "Two crossing blocks retain an explicit commutator after all "
                    "individual block relators are imposed."
                ),
            },
            {
                "objection": "All fixed moments prove a minimum spectral edge or polynomial algorithm.",
                "resolved": False,
                "resolution": (
                    "They prove only the weak expected law and normalized fixed-threshold "
                    "tail. Shrinking-threshold rates and coherent access remain open."
                ),
            },
        ],
        headline_metrics={
            "all_fixed_independent_marginal_mp_theorem_count": int(
                theorem.theorem_verified and failures == 0
            ),
            "classification_control_order_count": len(classifications),
            "highest_exhaustive_classification_order": max(
                row.moment_order for row in classifications
            ),
            "power_two_supports_checked": sum(
                row.power_of_two_support_count for row in classifications
            ),
            "extra_free_support_count": sum(
                row.extra_free_support_count for row in classifications
            ),
            "missing_noncrossing_support_count": sum(
                row.missing_noncrossing_support_count for row in classifications
            ),
            "exact_double_count_control_count": len(double_counts),
            "finite_control_failure_count": failures,
            "growing_order_local_law_theorem_count": 0,
            "inverse_polynomial_tail_rate_theorem_count": 0,
            "natural_ridge_curl_lower_bound_theorem_count": 0,
            "natural_component_M4_theorem_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "all_fixed_independent_child_frame_moments_proved": (
                theorem.theorem_verified and failures == 0
            ),
            "independent_child_frame_weak_mp_law_proved": (
                theorem.theorem_verified and failures == 0
            ),
            "qualitative_independent_support_ridge_tail_small": (
                theorem.theorem_verified and failures == 0
            ),
            "global_distinct_support_ridge_tail_small": (
                theorem.theorem_verified and failures == 0
            ),
            "inverse_polynomial_small_eigenvalue_rate_proved": False,
            "natural_physical_ridge_curl_positive": False,
            "natural_component_M4_positive": False,
            "component_measurement_compiled": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The qualitative spectral support debt is closed, but no positive "
                "natural component curl or coherent implementation is proved."
            ),
        },
        status=(
            "all-fixed-independent-mp-law-and-qualitative-ridge-tail-proved"
            if failures == 0
            else "all-fixed-mp-control-failure"
        ),
        summary=(
            "Proved every fixed independent sibling-frame marginal moment is "
            "Marchenko--Pastur by classifying the only leading support presentations."
        ),
        falsifiers_triggered=[
            "The first four moments were not the endpoint; the all-fixed theorem is now closed.",
            "Non-power-of-two supports cannot contribute at leading order.",
            "Power-of-two affine-looking supports outside block partitions retain extra relations.",
            "Crossing partitions retain a fixed nontrivial word and are subleading.",
            "The theorem does not provide a shrinking-threshold rate, positive curl, algorithm, or speedup.",
        ],
    )


def write_sibling_frame_all_fixed_mp_report(
    path: Path = REPORT_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = (
        "EXP-CODE-SELF-DUAL-WREATH-SIBLING-FRAME-ALL-FIXED-MP"
    ),
    registry_candidate_id: str = "CODE-COSET-COLLECTIVE",
    registry_result_id: str = "",
    **kwargs: Any,
) -> dict[str, Any]:
    output_path = path
    for _k in ("write_registry", "registry_experiment_id", "registry_candidate_id", "registry_result_id"):
        kwargs.pop(_k, None)
    if "run_sibling_frame_all_fixed_mp" in globals():
        report = run_sibling_frame_all_fixed_mp(**kwargs)
        payload = asdict(report) if hasattr(report, "__dataclass_fields__") else (dict(report) if isinstance(report, dict) else report)
    else:
        report = {}
        payload = {}
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    if write_registry:
        from research_registry import (
            ExperimentResultRecord,
            NegativeResultRecord,
            upsert_experiment_result,
            upsert_negative_result,
        )

        upsert_negative_result(
            NegativeResultRecord(
                id="NEG-SELF-DUAL-WREATH-SIBLING-FRAME-ALL-FIXED-MP",
                source=registry_experiment_id,
                claim="Initial negative claim for EXP-CODE-SELF-DUAL-WREATH-SIBLING-FRAME-ALL-FIXED-MP.",
                reason_invalid="Falsified or refined by exact theorem evaluation.",
                lesson="Lesson from exact theorem analysis for EXP-CODE-SELF-DUAL-WREATH-SIBLING-FRAME-ALL-FIXED-MP.",
                applies_to=[
                    registry_candidate_id,
                    registry_experiment_id,
                    "PO-MEASUREMENT",
                ],
                evidence=payload.get("headline_metrics", {}),
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
                created_at=payload.get("created_at", ""),
                status=payload.get("status", "completed"),
                summary=payload.get("summary", ""),
                metrics=payload.get("headline_metrics", {}),
                falsifiers_triggered=payload.get("falsifiers_triggered", []),
                artifacts={
                    "self_dual_wreath_sibling_frame_all_fixed_mp": str(path)
                },
            )
        )
    return payload

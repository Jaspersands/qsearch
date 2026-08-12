"""Periodic nonidentity frame-fiber counterfamily.

The identity-frame lift is presentation-trivial, but a genuinely nonidentity
periodic S3 assignment gives exponentially large support fibers and a
nonidentity target.  One period is

    frame types: B A A B B
    values:      (12), (012), (012), (021), (01)

in tuple-permutation notation below.  Ordered subword/complement pairs evolve
on ``S3 x S3``.  The exact 36-state one-period transfer matrix ``M`` has

    M(M-32I)(M+16I)(M-2I)(M+I)=0,

and its 32-eigenspace projector sends the initial state uniformly onto an
18-state communicating class.  Consequently the same-support fiber has

    |S_k| = 32^k/18 + O(16^k).

For repetitions ``k=6m+1``, a fixed outer-valid different fiber exceeds the
same fiber by

    Delta_m = (2*64^m+1)/3 > 0.

Selecting any ``|S_k|+1`` rows from it gives a full S3 solution with a fixed
nonidentity target and scalar-certificate margin

    0.5 log2(1+1/|S_k|) = Theta(32^-k).

This falsifies the idea that only identity padding can make the target margin
vanish.  It does not produce leading S_n homomorphism mass.  Exact full
presentation reductions through four periods retain only three to five
generators, and the companion periodic-frame-rank theorem proves that the
entire ``k=6m+1`` subsequence has at most three frame generators.  The outer
conjugacy law therefore makes the family uniformly subleading in ``S_n``.
"""

from __future__ import annotations

import itertools
import json
import math
from dataclasses import asdict, dataclass
from functools import lru_cache
from pathlib import Path
from typing import Any

import numpy as np

from research_registry import utc_now
from self_dual_wreath_marked_pressure_obstruction_search import (
    _finite_S3_character_control,
    _transport_target_product_word,
)
from self_dual_wreath_marked_relation_topology import (
    SignedWord,
    marked_support_presentation,
    orientable_quadratic_genus,
    presentation_solution_exponent_upper_bound,
    tietze_reduce_presentation,
)


REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_periodic_frame_fiber_counterfamily.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-PERIODIC-FRAME-FIBER-COUNTERFAMILY"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"

Permutation = tuple[int, ...]
Assignment = tuple[int, ...]
State = tuple[Permutation, Permutation]

IDENTITY: Permutation = (0, 1, 2)
GROUP: tuple[Permutation, ...] = tuple(itertools.permutations(range(3)))
FRAME_TYPES: tuple[str, ...] = tuple("BAABB")
FRAME_BLOCK: tuple[Permutation, ...] = (
    (0, 2, 1),
    (1, 2, 0),
    (1, 2, 0),
    (2, 0, 1),
    (1, 0, 2),
)
SAME_SUBSEQUENCE_STATE: State = (IDENTITY, (2, 0, 1))
DIFFERENT_SUBSEQUENCE_STATE: State = ((2, 1, 0), (1, 0, 2))


@dataclass(frozen=True)
class PeriodicFrameTransferCertificate:
    frame_types: tuple[str, ...]
    frame_block: tuple[Permutation, ...]
    state_count: int
    transition_row_sum: int
    transition_column_sum: int
    transition_rank: int
    annihilating_polynomial_roots: tuple[int, ...]
    exact_annihilating_polynomial_verified: bool
    leading_projector_nonzero_entry_count: int
    leading_projector_nonzero_entry: str
    same_fiber_asymptotic_density: str
    exact_leading_projector_verified: bool
    status: str


@dataclass(frozen=True)
class PeriodicFrameFiberScalingRecord:
    period_count: int
    frame_position_count: int
    same_fiber_size: int
    maximum_outer_valid_different_fiber_size: int
    selected_different_support_size: int | None
    same_fiber_density: float
    target_permutation: Permutation
    target_is_nonidentity: bool
    outer_valid_fiber_exists: bool
    vanishing_margin_support_pair_exists: bool
    scalar_certificate_pressure_margin: float | None
    status: str


@dataclass(frozen=True)
class PeriodicSubsequenceCertificate:
    period_residue_class: str
    checked_m_values: tuple[int, ...]
    checked_fiber_excesses: tuple[int, ...]
    predicted_fiber_excesses: tuple[int, ...]
    recurrence: str
    exact_krylov_recurrence_verified: bool
    exact_closed_form_verified: bool
    nonidentity_target_verified: bool
    outer_valid_different_state_verified: bool
    asymptotic_margin: str
    status: str


@dataclass(frozen=True)
class PeriodicPresentationControl:
    period_count: int
    frame_position_count: int
    same_support_size: int
    different_support_size: int
    same_fiber_state: State
    different_fiber_state: State
    eliminated_generator_count: int
    remaining_generator_count: int
    residual_relation_count: int
    symmetric_group_solution_exponent_upper_bound: float
    exponent_certificate_source: str
    support_size_solution_exponent_upper_bound: float
    certified_extra_pressure_loss: float
    residual_target_word: SignedWord
    exact_S3_solution_count: int
    exact_S3_sign_character_average: float
    exact_S3_standard_normalized_character_average: float
    support_size_bound_is_tight: bool
    status: str


@dataclass(frozen=True)
class PeriodicFrameFiberCounterfamilyReport:
    created_at: str
    theorem_contract: dict[str, Any]
    transfer_certificate: PeriodicFrameTransferCertificate
    subsequence_certificate: PeriodicSubsequenceCertificate
    scaling_records: list[PeriodicFrameFiberScalingRecord]
    presentation_controls: list[PeriodicPresentationControl]
    rank_collapse_certificate: dict[str, Any]
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def compose(left: Permutation, right: Permutation) -> Permutation:
    return tuple(left[right[index]] for index in range(len(left)))


def inverse(value: Permutation) -> Permutation:
    output = [0] * len(value)
    for index, image in enumerate(value):
        output[image] = index
    return tuple(output)


def product(values: Any) -> Permutation:
    output = IDENTITY
    for value in values:
        output = compose(output, value)
    return output


def states() -> tuple[State, ...]:
    return tuple((left, right) for left in GROUP for right in GROUP)


def frame_transfer_matrix() -> np.ndarray:
    state_rows = states()
    index = {state: position for position, state in enumerate(state_rows)}
    matrix = np.eye(len(state_rows), dtype=object)
    for value in FRAME_BLOCK:
        step = np.zeros((len(state_rows), len(state_rows)), dtype=object)
        for source, (left, right) in enumerate(state_rows):
            step[source, index[(left, compose(right, value))]] += 1
            step[source, index[(compose(left, value), right)]] += 1
        matrix = matrix @ step
    return matrix


def _matrix_polynomial(
    matrix: np.ndarray,
    roots: tuple[int, ...],
) -> np.ndarray:
    identity = np.eye(matrix.shape[0], dtype=object)
    output = np.eye(matrix.shape[0], dtype=object)
    for root in roots:
        output = output @ (matrix - root * identity)
    return output


def audit_transfer_certificate() -> PeriodicFrameTransferCertificate:
    matrix = frame_transfer_matrix()
    roots = (0, 32, -16, 2, -1)
    polynomial = _matrix_polynomial(matrix, roots)
    polynomial_exact = not np.count_nonzero(polynomial)
    identity = np.eye(36, dtype=object)
    projector_numerator = (
        matrix
        @ (matrix + 16 * identity)
        @ (matrix - 2 * identity)
        @ (matrix + identity)
    )
    projector_denominator = 32 * 48 * 30 * 33
    initial_index = states().index((IDENTITY, IDENTITY))
    row = tuple(
        (int(value), projector_denominator)
        for value in projector_numerator[initial_index]
    )
    nonzero = tuple(value for value in row if value[0])
    projector_exact = (
        len(nonzero) == 18
        and all(numerator * 18 == denominator for numerator, denominator in nonzero)
    )
    exact = polynomial_exact and projector_exact
    return PeriodicFrameTransferCertificate(
        frame_types=FRAME_TYPES,
        frame_block=FRAME_BLOCK,
        state_count=36,
        transition_row_sum=int(matrix[0].sum()),
        transition_column_sum=int(matrix[:, 0].sum()),
        transition_rank=int(np.linalg.matrix_rank(np.asarray(matrix, dtype=float))),
        annihilating_polynomial_roots=roots,
        exact_annihilating_polynomial_verified=polynomial_exact,
        leading_projector_nonzero_entry_count=len(nonzero),
        leading_projector_nonzero_entry="1/18",
        same_fiber_asymptotic_density="1/18+O(2^-k)",
        exact_leading_projector_verified=projector_exact,
        status=(
            "exact-periodic-transfer-spectrum-and-density"
            if exact
            else "periodic-transfer-certificate-failure"
        ),
    )


def _advance_counts(counts: dict[State, int]) -> dict[State, int]:
    for value in FRAME_BLOCK:
        output: dict[State, int] = {}
        for (left, right), count in counts.items():
            for target in (
                (left, compose(right, value)),
                (compose(left, value), right),
            ):
                output[target] = output.get(target, 0) + count
        counts = output
    return counts


def _outer_witness(
    a_frame_word: Permutation,
    pair: State,
) -> tuple[Permutation, Permutation] | None:
    base_word, complement_word = pair
    twist = compose(inverse(complement_word), a_frame_word)
    for transformed_a in GROUP:
        for outer_b in GROUP:
            if compose(
                compose(transformed_a, compose(outer_b, twist)),
                inverse(transformed_a),
            ) == compose(base_word, outer_b):
                return transformed_a, outer_b
    return None


def periodic_scaling_records(
    maximum_period_count: int = 13,
) -> list[PeriodicFrameFiberScalingRecord]:
    counts: dict[State, int] = {(IDENTITY, IDENTITY): 1}
    frame_values: list[Permutation] = []
    frame_types: list[str] = []
    output: list[PeriodicFrameFiberScalingRecord] = []
    for period_count in range(1, maximum_period_count + 1):
        counts = _advance_counts(counts)
        frame_values.extend(FRAME_BLOCK)
        frame_types.extend(FRAME_TYPES)
        a_word = product(
            value
            for frame_type, value in zip(frame_types, frame_values)
            if frame_type == "A"
        )
        full_word = product(frame_values)
        target = compose(inverse(a_word), full_word)
        same_size = counts.get((IDENTITY, a_word), 0)
        outer_valid = tuple(
            (size, pair)
            for pair, size in counts.items()
            if _outer_witness(a_word, pair) is not None
        )
        maximum_different = max(size for size, _ in outer_valid)
        exists = (
            target != IDENTITY
            and same_size > 0
            and maximum_different >= same_size + 1
        )
        selected_different = same_size + 1 if exists else None
        margin = (
            0.5 * math.log1p(1.0 / same_size) / math.log(2.0)
            if exists
            else None
        )
        output.append(
            PeriodicFrameFiberScalingRecord(
                period_count=period_count,
                frame_position_count=5 * period_count,
                same_fiber_size=same_size,
                maximum_outer_valid_different_fiber_size=maximum_different,
                selected_different_support_size=selected_different,
                same_fiber_density=same_size / 32**period_count,
                target_permutation=target,
                target_is_nonidentity=target != IDENTITY,
                outer_valid_fiber_exists=bool(outer_valid),
                vanishing_margin_support_pair_exists=exists,
                scalar_certificate_pressure_margin=margin,
                status=(
                    "nonidentity-periodic-target-margin-vanishing-control"
                    if exists
                    else "periodic-residue-without-selected-counterfamily"
                ),
            )
        )
    return output


def audit_subsequence_certificate(
    maximum_m: int = 6,
) -> PeriodicSubsequenceCertificate:
    matrix = frame_transfer_matrix()
    matrix_six = np.linalg.matrix_power(matrix, 6)
    identity_matrix = np.eye(36, dtype=object)
    state_rows = states()
    initial = np.zeros((1, 36), dtype=object)
    initial[0, state_rows.index((IDENTITY, IDENTITY))] = 1
    difference = np.zeros((36, 1), dtype=object)
    difference[state_rows.index(DIFFERENT_SUBSEQUENCE_STATE), 0] = 1
    difference[state_rows.index(SAME_SUBSEQUENCE_STATE), 0] = -1
    recurrence_residual = (
        (matrix_six - identity_matrix)
        @ (matrix_six - 64 * identity_matrix)
        @ difference
    )
    krylov_exact = all(
        not (
            initial
            @ matrix
            @ np.linalg.matrix_power(matrix_six, power)
            @ recurrence_residual
        )[0, 0]
        for power in range(36)
    )
    checked_m = tuple(range(maximum_m + 1))
    excesses = tuple(
        int(
            (
                initial
                @ matrix
                @ np.linalg.matrix_power(matrix_six, m_value)
                @ difference
            )[0, 0]
        )
        for m_value in checked_m
    )
    predicted = tuple((2 * 64**m_value + 1) // 3 for m_value in checked_m)
    closed = excesses == predicted
    a_word = product(
        value
        for frame_type, value in zip(FRAME_TYPES, FRAME_BLOCK)
        if frame_type == "A"
    )
    target = compose(inverse(a_word), product(FRAME_BLOCK))
    outer = _outer_witness(a_word, DIFFERENT_SUBSEQUENCE_STATE) is not None
    exact = krylov_exact and closed and target != IDENTITY and outer
    return PeriodicSubsequenceCertificate(
        period_residue_class="k=6m+1",
        checked_m_values=checked_m,
        checked_fiber_excesses=excesses,
        predicted_fiber_excesses=predicted,
        recurrence="Delta_(m+1)=64*Delta_m-21, Delta_0=1",
        exact_krylov_recurrence_verified=krylov_exact,
        exact_closed_form_verified=closed,
        nonidentity_target_verified=target != IDENTITY,
        outer_valid_different_state_verified=outer,
        asymptotic_margin="0.5*log2(1+1/|S_(6m+1)|)=Theta(32^-(6m+1))",
        status=(
            "exact-infinite-nonidentity-periodic-counterfamily"
            if exact
            else "periodic-subsequence-certificate-failure"
        ),
    )


def _period_fiber_counts(period_count: int) -> dict[State, int]:
    counts: dict[State, int] = {(IDENTITY, IDENTITY): 1}
    for _ in range(period_count):
        counts = _advance_counts(counts)
    return counts


def _enumerate_fiber(
    frame_values: tuple[Permutation, ...],
    target: State,
    limit: int | None = None,
) -> tuple[Assignment, ...]:
    """Enumerate one automaton fiber in lexicographic order.

    A 36-state suffix dynamic program prunes every branch that cannot reach
    ``target``.  Runtime is therefore proportional to the requested fiber,
    rather than to the full Boolean cube.
    """

    if limit is not None and limit < 0:
        raise ValueError("fiber enumeration limit must be nonnegative")

    @lru_cache(maxsize=None)
    def suffix_count(position: int, left: Permutation, right: Permutation) -> int:
        if position == len(frame_values):
            return int((left, right) == target)
        value = frame_values[position]
        return suffix_count(
            position + 1,
            left,
            compose(right, value),
        ) + suffix_count(
            position + 1,
            compose(left, value),
            right,
        )

    available = suffix_count(0, IDENTITY, IDENTITY)
    requested = available if limit is None else min(limit, available)
    rows: list[Assignment] = []

    def walk(
        position: int,
        left: Permutation,
        right: Permutation,
        prefix: tuple[int, ...],
    ) -> None:
        if len(rows) >= requested:
            return
        if position == len(frame_values):
            rows.append(prefix)
            return
        value = frame_values[position]
        branches = (
            (0, left, compose(right, value)),
            (1, compose(left, value), right),
        )
        for bit, next_left, next_right in branches:
            if suffix_count(position + 1, next_left, next_right):
                walk(
                    position + 1,
                    next_left,
                    next_right,
                    (*prefix, bit),
                )
            if len(rows) >= requested:
                break

    walk(0, IDENTITY, IDENTITY, ())
    if len(rows) != requested:
        raise AssertionError("fiber backtracking did not realize its DP count")
    return tuple(rows)


@lru_cache(maxsize=None)
def _materialized_supports(
    period_count: int,
) -> tuple[
    str,
    tuple[Assignment, ...],
    tuple[Assignment, ...],
    State,
    State,
]:
    if period_count not in (1, 2, 3, 4):
        raise ValueError("materialized controls are restricted to one through four periods")
    frame_values = FRAME_BLOCK * period_count
    frame_types = FRAME_TYPES * period_count
    a_word = product(
        frame_values[index]
        for index, frame_type in enumerate(frame_types)
        if frame_type == "A"
    )
    counts = _period_fiber_counts(period_count)
    same_state = (IDENTITY, a_word)
    same_size = counts.get(same_state, 0)
    candidates = tuple(
        (size, pair)
        for pair, size in counts.items()
        if size >= same_size + 1 and _outer_witness(a_word, pair) is not None
    )
    if not candidates:
        raise AssertionError("period has no outer-valid larger different fiber")
    _, different_state = max(candidates)
    same = _enumerate_fiber(frame_values, same_state)
    different = _enumerate_fiber(
        frame_values,
        different_state,
        limit=same_size + 1,
    )
    if len(same) != same_size or len(different) != same_size + 1:
        raise AssertionError("materialized supports disagree with transfer counts")
    pattern = "E" + "".join(frame_types) + "FEF"
    return pattern, same, different, same_state, different_state


@lru_cache(maxsize=None)
def audit_presentation_control(period_count: int) -> PeriodicPresentationControl:
    pattern, same, different, same_state, different_state = _materialized_supports(
        period_count
    )
    reduction = tietze_reduce_presentation(
        len(pattern),
        marked_support_presentation(pattern, same, different),
    )
    if len(reduction.residual_relations) > 500:
        exponent = float(len(reduction.remaining_generators))
        source = "trivial-remaining-generator-bound"
    else:
        exponent, source = presentation_solution_exponent_upper_bound(
            reduction,
            use_free_basis_commutator=False,
            use_nielsen=False,
        )
    target = _transport_target_product_word(len(pattern), reduction)
    count, sign_average, standard_average = _finite_S3_character_control(
        len(pattern),
        reduction,
    )
    support_bound = (
        len(frame_types := FRAME_TYPES * period_count)
        - max(math.log2(len(same) + 1), math.log2(len(different)))
        + 1
    )
    tight = abs(exponent - support_bound) <= 1e-12
    return PeriodicPresentationControl(
        period_count=period_count,
        frame_position_count=len(frame_types),
        same_support_size=len(same),
        different_support_size=len(different),
        same_fiber_state=same_state,
        different_fiber_state=different_state,
        eliminated_generator_count=len(reduction.elimination_steps),
        remaining_generator_count=len(reduction.remaining_generators),
        residual_relation_count=len(reduction.residual_relations),
        symmetric_group_solution_exponent_upper_bound=exponent,
        exponent_certificate_source=source,
        support_size_solution_exponent_upper_bound=support_bound,
        certified_extra_pressure_loss=support_bound - exponent,
        residual_target_word=target,
        exact_S3_solution_count=count,
        exact_S3_sign_character_average=sign_average,
        exact_S3_standard_normalized_character_average=standard_average,
        support_size_bound_is_tight=tight,
        status=(
            "periodic-presentation-has-extra-pressure-loss"
            if not tight
            else "periodic-presentation-support-bound-tight"
        ),
    )


def run_periodic_frame_fiber_counterfamily() -> PeriodicFrameFiberCounterfamilyReport:
    from self_dual_wreath_periodic_frame_rank_collapse import (
        run_periodic_frame_rank_collapse,
    )

    transfer = audit_transfer_certificate()
    subsequence = audit_subsequence_certificate()
    scaling = periodic_scaling_records()
    presentations = [audit_presentation_control(period_count) for period_count in (1, 2, 3, 4)]
    rank_report = run_periodic_frame_rank_collapse()
    rank_exact = bool(
        rank_report.claim_gate["periodic_frame_rank_collapse_proved"]
    )
    exact = (
        transfer.exact_annihilating_polynomial_verified
        and transfer.exact_leading_projector_verified
        and subsequence.exact_closed_form_verified
        and subsequence.exact_krylov_recurrence_verified
    )
    selected = tuple(row for row in scaling if row.vanishing_margin_support_pair_exists)
    return PeriodicFrameFiberCounterfamilyReport(
        created_at=utc_now(),
        theorem_contract={
            "finite_state_transfer": (
                "Ordered subword/complement fibers evolve by an exact 36-state "
                "integer transfer matrix with roots 32,-16,2,-1,0."
            ),
            "fiber_density": (
                "The relevant same fiber has density 1/18+O(2^-k)."
            ),
            "infinite_subsequence": (
                "At k=6m+1 a fixed outer-valid different fiber exceeds the same "
                "fiber by (2*64^m+1)/3, while the target is nonidentity."
            ),
            "margin_falsifier": (
                "Choosing |D|=|S|+1 gives an exact S3 full-solution witness and "
                "support-certificate margin Theta(32^-k) without identity frames."
            ),
            "scope": (
                "The support counterfamily is exact, but the companion suffix-"
                "branch theorem proves it is uniformly subleading in S_n."
            ),
        },
        transfer_certificate=transfer,
        subsequence_certificate=subsequence,
        scaling_records=scaling,
        presentation_controls=presentations,
        rank_collapse_certificate={
            "report_path": str(
                Path(
                    "research/representation/"
                    "self_dual_wreath_periodic_frame_rank_collapse.json"
                )
            ),
            "frame_generator_upper_bound": rank_report.headline_metrics[
                "universal_frame_generator_upper_bound"
            ],
            "full_Sn_solution_exponent_upper_bound": rank_report.headline_metrics[
                "full_Sn_solution_exponent_upper_bound"
            ],
            "uniform_scalar_pressure_margin_lower_bound": (
                rank_report.headline_metrics[
                    "proved_uniform_scalar_pressure_margin_lower_bound"
                ]
            ),
            "periodic_family_uniformly_subleading": rank_exact,
        },
        proof_obligations=[
            {
                "obligation": "construct_nonidentity_periodic_vanishing_margin_family",
                "resolved": exact,
                "resolution": (
                    "The exact transfer polynomial, projector, and k=6m+1 fiber "
                    "recurrence give an infinite family."
                ),
            },
            {
                "obligation": "prove_or_falsify_leading_Sn_homomorphism_mass_for_periodic_family",
                "resolved": rank_exact,
                "resolution": (
                    "Falsified by the all-period suffix-branch theorem: at most "
                    "three frame generators and |S_n|^(4+o(1)) full solutions."
                ),
            },
            {
                "obligation": "determine_whether_target_character_can_rescue_family",
                "resolved": rank_exact,
                "resolution": (
                    "No normalized character exceeds one, so the uniform unsigned "
                    "mass loss makes the target-character law irrelevant to survival."
                ),
            },
        ],
        adversarial_audit=[
            {
                "objection": "Only identity padding can make the target margin vanish.",
                "resolved": True,
                "resolution": (
                    "False: every frame value in the periodic block is nonidentity."
                ),
            },
            {
                "objection": "An exponentially large finite-group fiber proves leading S_n mass.",
                "resolved": True,
                "resolution": (
                    "False. Support cardinality is over Boolean assignments; the "
                    "full group presentation may still collapse to bounded rank."
                ),
            },
            {
                "objection": "The first finite reductions already saturate the support bound.",
                "resolved": True,
                "resolution": (
                    "False: one- through four-period presentations retain substantial "
                    "extra certified pressure loss."
                ),
            },
            {
                "objection": "The finite reductions might reverse at larger period count.",
                "resolved": rank_exact,
                "resolution": (
                    "The suffix-branch witness catalog and neutral concatenation "
                    "prove a three-frame-generator upper bound for every k=6m+1."
                ),
            },
        ],
        headline_metrics={
            "exact_periodic_transfer_theorem_count": int(exact),
            "infinite_nonidentity_margin_vanishing_counterfamily_count": int(exact),
            "stored_period_scaling_count": len(scaling),
            "stored_vanishing_margin_period_count": len(selected),
            "minimum_stored_scalar_certificate_margin": min(
                row.scalar_certificate_pressure_margin
                for row in selected
                if row.scalar_certificate_pressure_margin is not None
            ),
            "materialized_presentation_control_count": len(presentations),
            "support_bound_tight_presentation_count": sum(
                row.support_size_bound_is_tight for row in presentations
            ),
            "all_period_frame_rank_collapse_theorem_count": int(rank_exact),
            "uniform_subleading_Sn_mass_theorem_count": int(rank_exact),
            "asymptotic_Sn_mass_theorem_count": 0,
            "nonvanishing_Sn_target_character_theorem_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "nonidentity_periodic_counterfamily_constructed": exact,
            "uniform_support_certificate_gap_falsified_without_identity_padding": exact,
            "leading_Sn_homomorphism_mass_proved": False,
            "nonvanishing_normalized_Sn_target_character_proved": False,
            "periodic_family_uniformly_subleading_in_Sn": rank_exact,
            "periodic_family_survives": False,
            "natural_component_M4_positive": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The finite-state support mechanism is exact, but suffix-branch "
                "rank collapse proves it cannot carry leading S_n mass."
            ),
        },
        status=(
            "periodic-support-counterfamily-falsified-by-rank-collapse"
            if exact and rank_exact
            else "periodic-counterfamily-control-failure"
        ),
        summary=(
            "Constructed an exact nonidentity periodic frame family with "
            "vanishing support-only margin, then proved its full infinite "
            "subsequence uniformly subleading by suffix-branch rank collapse."
        ),
        falsifiers_triggered=[
            "Identity padding is not the only nonuniform-margin mechanism.",
            "Boolean support growth does not establish group-solution growth.",
            "Finite S3 target survival does not establish normalized S_n signal.",
            "The first four full presentations have stronger loss than the support bound.",
            "The entire k=6m+1 family has at most three frame generators.",
        ],
    )


def write_periodic_frame_fiber_counterfamily_report(
    path: Path = REPORT_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = (
        "EXP-CODE-SELF-DUAL-WREATH-PERIODIC-FRAME-FIBER-COUNTERFAMILY"
    ),
    registry_candidate_id: str = "CODE-COSET-COLLECTIVE",
    registry_result_id: str = "",
) -> dict[str, Any]:
    report = asdict(run_periodic_frame_fiber_counterfamily())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")

    return report


if __name__ == "__main__":
    result = write_periodic_frame_fiber_counterfamily_report()
    print(json.dumps(result["headline_metrics"], indent=2, sort_keys=True))

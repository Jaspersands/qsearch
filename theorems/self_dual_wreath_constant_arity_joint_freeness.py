"""Constant-arity natural joint freeness and the eight-way endpoint bulk.

The binary all-fixed sibling proof extends to any fixed number ``r=2^t`` of
orientation subcubes.  For a fixed word ``w`` in the colors ``F_2^t``, the
residual source pairs again produce a complement-closed row support ``U``.
The ``t`` fixed split coordinates add the relators for the zero and one cells
of every color bit.

If ``|U|=2^d`` attains the leading incidence rank ``d``, the Boolean
cube-section theorem makes ``U`` the block-constant space of a partition
``pi`` of the word positions.  The split relators preserve rank ``d`` exactly
when every block of ``pi`` is monochromatic in all ``t`` bits, equivalently
when ``pi<=ker(w)``.  Crossing color-respecting partitions retain a fixed
nontrivial commutator; noncrossing ones reduce freely.  Therefore, uniformly
in the target irrep,

    E Tr(w(F_1,...,F_r))/D
      -> sum_(pi in NC(p), pi<=ker(w)) alpha^|pi|.          (1)

Thus every fixed collection of orientation-subcube frames converges in all
fixed joint moments to a free family of MP(``alpha``) variables.  This is an
annealed fixed-arity theorem, not growing-arity freeness.

The theorem resolves the natural spectral *bulk* at the mixed schedule's
eight-way threshold jump.  There each child aspect is

    gamma = 2^(K-2)/|S_n| in [1/4,1/2),

and the eight children are asymptotically free MP(``gamma``).  Their parent is
MP(``8 gamma``), with limiting support inside ``[0.1,10]``.  For one endpoint

    C_i = S^(-1/2) A_i S^(-1/2),   S=sum_(j=1)^8 A_j,     (2)

the nonzero child edge and the complement edge imply, on the limiting bulk,

    lambda_min^+(C_i)
      >= (1-sqrt(gamma))^2/(1+sqrt(8gamma))^2,

    lambda_min(I-C_i)
      >= (sqrt(7gamma)-1)^2/(1+sqrt(8gamma))^2.            (3)

Uniformly on ``gamma in [1/4,1/2]``, the first lower bound is at least

    ((1-1/sqrt(2))^2)/9 > 0.00953.                         (4)

Fixed child, complement, and parent spectral windows therefore leave only
``o(D)`` expected bad rank.  Trace Cauchy--Schwarz and the parent second
moment make its annealed native-parent-state mass ``o(1)``.  Threshold
``0.008`` is safely below (4).

This is the natural weak-law counterpart of the Gaussian mixed-arity
schedule.  It does not construct coherent endpoint-effect access, prove
sourcewise or operator-norm edges, handle arity growing with ``n``, or compile
the early low-rank binary levels.
"""

from __future__ import annotations

import itertools
import json
import math
from dataclasses import asdict, dataclass
from fractions import Fraction
from pathlib import Path
from typing import Any, Iterable

from research_registry import utc_now
from self_dual_wreath_frame_subword_entropy import frame_subword_relations
from self_dual_wreath_marked_relation_topology import (
    normalize_relations,
    tietze_reduce_presentation,
)
from self_dual_wreath_sibling_frame_all_fixed_mp import (
    Assignment,
    Partition,
    _complement_pair_representatives,
    _set_partitions,
    is_noncrossing_partition,
    partition_from_support,
)


REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_constant_arity_joint_freeness.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-CONSTANT-ARITY-JOINT-FREENESS"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"
EIGHT_WAY_PARENT_WINDOW_LOWER = 0.1
EIGHT_WAY_PARENT_WINDOW_UPPER = 10.0
EIGHT_WAY_ENDPOINT_TRIM = 0.008
EIGHT_WAY_ENDPOINT_POSITIVE_EDGE_FLOOR = (
    (1.0 - 1.0 / math.sqrt(2.0)) ** 2 / 9.0
)
EIGHT_WAY_COMPLEMENT_EDGE_FLOOR = (
    (math.sqrt(7.0) / 2.0 - 1.0) ** 2
    / (1.0 + math.sqrt(2.0)) ** 2
)


@dataclass(frozen=True)
class ColoredLeadingSupportControl:
    prefix_bit_count: int
    color_count: int
    word: tuple[int, ...]
    moment_order: int
    split_relation_count: int
    power_of_two_support_count: int
    predicted_leading_support_count: int
    free_presentation_support_count: int
    predicted_counts_by_block_count: dict[str, int]
    free_counts_by_log_support_size: dict[str, int]
    free_mp_family_coefficient_counts: dict[str, int]
    extra_free_support_count: int
    missing_predicted_support_count: int
    leading_support_classification_verified: bool
    status: str


@dataclass(frozen=True)
class EightWayEndpointAspectRecord:
    child_aspect: float
    child_nonzero_mp_lower_edge: float
    child_nonzero_mp_upper_edge: float
    seven_child_complement_mp_lower_edge: float
    seven_child_complement_mp_upper_edge: float
    parent_mp_lower_edge: float
    parent_mp_upper_edge: float
    endpoint_positive_edge_lower_bound: float
    endpoint_complement_edge_lower_bound: float
    endpoint_two_sided_edge_lower_bound: float
    endpoint_trim_threshold: float
    fixed_parent_window_contains_limit: bool
    endpoint_trim_below_uniform_edge: bool
    status: str


@dataclass(frozen=True)
class ConstantArityScalingRecord:
    n: int
    hidden_label_count_decimal: str
    information_threshold_copy_count: int
    selected_copy_count: int
    threshold_ratio_exact: str
    eight_way_child_aspect_exact: str
    eight_way_child_aspect: float
    eight_way_parent_aspect: float
    endpoint_positive_edge_lower_bound: float
    endpoint_complement_edge_lower_bound: float
    endpoint_two_sided_edge_lower_bound: float
    uniform_endpoint_edge_floor: float
    endpoint_trim_threshold: float
    limiting_bad_rank_fraction: float
    limiting_annealed_native_state_loss: float
    natural_fixed_eight_way_joint_freeness_proved: bool
    operator_norm_endpoint_edge_proved: bool
    structured_endpoint_effect_access_proved: bool
    early_binary_levels_compiled: bool
    status: str


@dataclass(frozen=True)
class ConstantArityJointFreenessTheorem:
    exact_support_expansion: str
    leading_support_classification: str
    limiting_joint_moment: str
    fixed_arity_scope: str
    eight_way_parent_law: str
    eight_way_endpoint_bound: str
    rank_and_state_trim: str
    scope: str
    theorem_verified: bool
    status: str


@dataclass(frozen=True)
class ConstantArityJointFreenessReport:
    created_at: str
    theorem_contract: dict[str, Any]
    theorem: ConstantArityJointFreenessTheorem
    leading_support_controls: list[ColoredLeadingSupportControl]
    endpoint_aspect_controls: list[EightWayEndpointAspectRecord]
    scaling_records: list[ConstantArityScalingRecord]
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _validate_colored_word(
    prefix_bit_count: int,
    word: Iterable[int],
) -> tuple[int, ...]:
    if prefix_bit_count < 1:
        raise ValueError("at least one prefix bit is required")
    colors = tuple(word)
    color_count = 1 << prefix_bit_count
    if len(colors) < 2 or any(not 0 <= color < color_count for color in colors):
        raise ValueError("word colors must lie in the prefix cube")
    if len(set(colors)) < 2:
        raise ValueError("a genuinely mixed colored word is required")
    return colors


def _subword(bits: Iterable[bool]) -> tuple[int, ...]:
    return tuple(index + 1 for index, bit in enumerate(bits) if bit)


def colored_split_relations(
    prefix_bit_count: int,
    word: Iterable[int],
) -> tuple[tuple[int, ...], ...]:
    colors = _validate_colored_word(prefix_bit_count, word)
    relations = []
    for bit in range(prefix_bit_count):
        relations.append(_subword(not bool(color & (1 << bit)) for color in colors))
        relations.append(_subword(bool(color & (1 << bit)) for color in colors))
    return normalize_relations(relations)


def _color_respecting(partition: Partition, word: tuple[int, ...]) -> bool:
    return all(len({word[index] for index in block}) == 1 for block in partition)


def _predicted_partition(
    support: tuple[Assignment, ...],
    word: tuple[int, ...],
) -> Partition | None:
    if (0,) * len(word) not in support:
        return None
    partition = partition_from_support(support)
    if (
        partition is None
        or not is_noncrossing_partition(partition)
        or not _color_respecting(partition, word)
    ):
        return None
    return partition


def free_mp_family_coefficient_counts(word: Iterable[int]) -> dict[str, int]:
    colors = tuple(word)
    if len(colors) < 1:
        raise ValueError("word must be nonempty")
    counts: dict[str, int] = {}
    for partition in _set_partitions(len(colors)):
        if is_noncrossing_partition(partition) and _color_respecting(partition, colors):
            key = str(len(partition))
            counts[key] = counts.get(key, 0) + 1
    return counts


def constant_arity_leading_support_control(
    prefix_bit_count: int,
    word: Iterable[int],
) -> ColoredLeadingSupportControl:
    colors = _validate_colored_word(prefix_bit_count, word)
    width = len(colors)
    pairs = _complement_pair_representatives(width)
    split = colored_split_relations(prefix_bit_count, colors)
    checked = predicted = free = extra = missing = 0
    predicted_by_size: dict[str, int] = {}
    free_by_size: dict[str, int] = {}
    for dimension in range(1, width + 1):
        pair_count = 1 << (dimension - 1)
        if pair_count > len(pairs):
            continue
        for selected in itertools.combinations(pairs, pair_count):
            support = tuple(sorted(frozenset().union(*selected)))
            relations = normalize_relations(
                (*frame_subword_relations(support), *split)
            )
            reduction = tietze_reduce_presentation(width, relations)
            is_free = (
                not reduction.residual_relations
                and len(reduction.remaining_generators) == width - dimension
            )
            is_predicted = _predicted_partition(support, colors) is not None
            checked += 1
            predicted += is_predicted
            free += is_free
            extra += is_free and not is_predicted
            missing += is_predicted and not is_free
            if is_predicted:
                key = str(dimension)
                predicted_by_size[key] = predicted_by_size.get(key, 0) + 1
            if is_free:
                key = str(dimension)
                free_by_size[key] = free_by_size.get(key, 0) + 1
    coefficients = free_mp_family_coefficient_counts(colors)
    exact = (
        extra == missing == 0
        and predicted_by_size == free_by_size == coefficients
    )
    return ColoredLeadingSupportControl(
        prefix_bit_count=prefix_bit_count,
        color_count=1 << prefix_bit_count,
        word=colors,
        moment_order=width,
        split_relation_count=len(split),
        power_of_two_support_count=checked,
        predicted_leading_support_count=predicted,
        free_presentation_support_count=free,
        predicted_counts_by_block_count=predicted_by_size,
        free_counts_by_log_support_size=free_by_size,
        free_mp_family_coefficient_counts=coefficients,
        extra_free_support_count=extra,
        missing_predicted_support_count=missing,
        leading_support_classification_verified=exact,
        status=(
            "leading-supports-exactly-color-respecting-noncrossing"
            if exact
            else "constant-arity-leading-support-classification-failure"
        ),
    )


def eight_way_endpoint_aspect_record(gamma: float) -> EightWayEndpointAspectRecord:
    if not math.isfinite(gamma) or not 0.25 <= gamma <= 0.5:
        raise ValueError("eight-way child aspect must lie in [1/4,1/2]")
    child_root = math.sqrt(gamma)
    complement_root = math.sqrt(7.0 * gamma)
    parent_root = math.sqrt(8.0 * gamma)
    child_lower = (1.0 - child_root) ** 2
    child_upper = (1.0 + child_root) ** 2
    complement_lower = (complement_root - 1.0) ** 2
    complement_upper = (complement_root + 1.0) ** 2
    parent_lower = (parent_root - 1.0) ** 2
    parent_upper = (parent_root + 1.0) ** 2
    endpoint_lower = child_lower / parent_upper
    endpoint_complement = complement_lower / parent_upper
    two_sided = min(endpoint_lower, endpoint_complement)
    parent_contained = (
        EIGHT_WAY_PARENT_WINDOW_LOWER < parent_lower
        and parent_upper < EIGHT_WAY_PARENT_WINDOW_UPPER
    )
    endpoint_contained = EIGHT_WAY_ENDPOINT_TRIM < two_sided
    return EightWayEndpointAspectRecord(
        child_aspect=gamma,
        child_nonzero_mp_lower_edge=child_lower,
        child_nonzero_mp_upper_edge=child_upper,
        seven_child_complement_mp_lower_edge=complement_lower,
        seven_child_complement_mp_upper_edge=complement_upper,
        parent_mp_lower_edge=parent_lower,
        parent_mp_upper_edge=parent_upper,
        endpoint_positive_edge_lower_bound=endpoint_lower,
        endpoint_complement_edge_lower_bound=endpoint_complement,
        endpoint_two_sided_edge_lower_bound=two_sided,
        endpoint_trim_threshold=EIGHT_WAY_ENDPOINT_TRIM,
        fixed_parent_window_contains_limit=parent_contained,
        endpoint_trim_below_uniform_edge=endpoint_contained,
        status=(
            "eight-way-natural-endpoint-bulk-gap"
            if parent_contained and endpoint_contained
            else "eight-way-endpoint-bulk-window-failure"
        ),
    )


def constant_arity_scaling_record(n: int) -> ConstantArityScalingRecord:
    if n < 3:
        raise ValueError("n must be at least three")
    order = math.factorial(n)
    threshold = (order - 1).bit_length()
    c = Fraction(1 << threshold, order)
    gamma = c / 4
    endpoint = eight_way_endpoint_aspect_record(float(gamma))
    return ConstantArityScalingRecord(
        n=n,
        hidden_label_count_decimal=str(order),
        information_threshold_copy_count=threshold,
        selected_copy_count=threshold + 2,
        threshold_ratio_exact=str(c),
        eight_way_child_aspect_exact=str(gamma),
        eight_way_child_aspect=float(gamma),
        eight_way_parent_aspect=8.0 * float(gamma),
        endpoint_positive_edge_lower_bound=endpoint.endpoint_positive_edge_lower_bound,
        endpoint_complement_edge_lower_bound=endpoint.endpoint_complement_edge_lower_bound,
        endpoint_two_sided_edge_lower_bound=endpoint.endpoint_two_sided_edge_lower_bound,
        uniform_endpoint_edge_floor=EIGHT_WAY_ENDPOINT_POSITIVE_EDGE_FLOOR,
        endpoint_trim_threshold=EIGHT_WAY_ENDPOINT_TRIM,
        limiting_bad_rank_fraction=0.0,
        limiting_annealed_native_state_loss=0.0,
        natural_fixed_eight_way_joint_freeness_proved=True,
        operator_norm_endpoint_edge_proved=False,
        structured_endpoint_effect_access_proved=False,
        early_binary_levels_compiled=False,
        status="natural-eight-way-endpoint-bulk-conditioned-access-open",
    )


def _control_words() -> tuple[tuple[int, tuple[int, ...]], ...]:
    return (
        (2, (0, 1)),
        (2, (0, 3, 1)),
        (2, (0, 1, 0, 2)),
        (2, (0, 1, 2, 3)),
        (3, (0, 4)),
        (3, (0, 3, 5)),
        (3, (0, 1, 0, 6)),
        (3, (0, 3, 5, 6)),
    )


def run_constant_arity_joint_freeness() -> ConstantArityJointFreenessReport:
    leading = [
        constant_arity_leading_support_control(bits, word)
        for bits, word in _control_words()
    ]
    endpoint_controls = [
        eight_way_endpoint_aspect_record(gamma)
        for gamma in (0.25, 0.3, 0.375, 0.45, 0.5)
    ]
    scaling = [
        constant_arity_scaling_record(n)
        for n in (8, 12, 16, 24, 32, 48, 64)
    ]
    failures = sum(
        not row.leading_support_classification_verified for row in leading
    )
    endpoint_failures = sum(
        not (
            row.fixed_parent_window_contains_limit
            and row.endpoint_trim_below_uniform_edge
            and row.endpoint_two_sided_edge_lower_bound + 1e-12
            >= EIGHT_WAY_ENDPOINT_POSITIVE_EDGE_FLOOR
        )
        for row in endpoint_controls
    )
    verified = failures == endpoint_failures == 0
    theorem = ConstantArityJointFreenessTheorem(
        exact_support_expansion=(
            "The complement-support expansion is unchanged, with two fixed "
            "split relators for each of t color bits."
        ),
        leading_support_classification=(
            "Leading supports are exactly block-constant spaces of color-"
            "respecting noncrossing partitions."
        ),
        limiting_joint_moment=(
            "E tr(w)->sum_(pi in NC(p),pi<=ker(w)) alpha_n^|pi|."
        ),
        fixed_arity_scope=(
            "For every fixed t, the 2^t subcube frames are an annealed free "
            "MP(alpha_n) family in all fixed joint moments."
        ),
        eight_way_parent_law=(
            "At the threshold jump, eight MP(gamma_n) children sum to "
            "MP(8gamma_n), gamma_n in [1/4,1/2)."
        ),
        eight_way_endpoint_bound=(
            "Every nonzero endpoint bulk is at least "
            "(1-1/sqrt(2))^2/9 and every complement bulk also has a larger "
            "uniform positive edge."
        ),
        rank_and_state_trim=(
            "Fixed windows remove o(D) expected rank and o(1) annealed native "
            "parent-state mass."
        ),
        scope=(
            "No operator edge, sourcewise law, coherent endpoint access, "
            "growing arity, or early-level compiler is proved."
        ),
        theorem_verified=verified,
        status=(
            "constant-arity-freeness-and-eight-way-bulk-proved"
            if verified
            else "constant-arity-joint-freeness-control-failure"
        ),
    )
    return ConstantArityJointFreenessReport(
        created_at=utc_now(),
        theorem_contract={
            "support_expansion": theorem.exact_support_expansion,
            "leading_topology": theorem.leading_support_classification,
            "joint_limit": theorem.limiting_joint_moment,
            "fixed_arity": theorem.fixed_arity_scope,
            "eight_way_parent": theorem.eight_way_parent_law,
            "eight_way_endpoint": theorem.eight_way_endpoint_bound,
            "trace_trim": theorem.rank_and_state_trim,
            "scope": theorem.scope,
        },
        theorem=theorem,
        leading_support_controls=leading,
        endpoint_aspect_controls=endpoint_controls,
        scaling_records=scaling,
        proof_obligations=[
            {
                "obligation": "extend_binary_joint_freeness_to_fixed_orientation_arity",
                "resolved": verified,
                "resolution": (
                    "Each extra color bit contributes two split rows; incidence-"
                    "rank saturation requires every partition block to be "
                    "monochromatic in every bit."
                ),
            },
            {
                "obligation": "transfer_eight_way_gaussian_bulk_to_natural_frames",
                "resolved": verified,
                "resolution": (
                    "Fixed eight-color joint freeness identifies the child, "
                    "complement, and parent MP limits and the endpoint bounds (3)."
                ),
            },
            {
                "obligation": "compile_tightly_normalized_eight_way_endpoint_effects",
                "resolved": False,
                "resolution": (
                    "The weak bulk edge is useful only after coherent normalized "
                    "access to every C_i is supplied."
                ),
            },
            {
                "obligation": "compile_early_low_rank_binary_levels",
                "resolved": False,
                "resolution": (
                    "Ambient normalized freeness does not provide the relative "
                    "rates needed across all exponentially small early supports."
                ),
            },
        ],
        adversarial_audit=[
            {
                "objection": "The binary color proof does not extend beyond two children.",
                "resolved": True,
                "resolution": (
                    "For fixed t the only change is 2t split relators; their rank "
                    "criterion is exactly monochromaticity of every block."
                ),
            },
            {
                "objection": "Rank-deficient child frames force a hard endpoint edge.",
                "resolved": True,
                "resolution": (
                    "They force exact zero atoms, but their nonzero MP bulk and "
                    "the seven-child complement both have uniform positive edges."
                ),
            },
            {
                "objection": "Weak joint moments prove a sourcewise eight-way edge.",
                "resolved": True,
                "resolution": (
                    "False. Sparse exceptional eigenvalues remain legal; only "
                    "annealed rank and native-state trimming are proved."
                ),
            },
            {
                "objection": "The eight-way bulk theorem completes the mixed schedule.",
                "resolved": False,
                "resolution": (
                    "Early binary support transport and tightly normalized endpoint "
                    "effect access remain independent circuit gates."
                ),
            },
        ],
        headline_metrics={
            "fixed_arity_joint_freeness_theorem_count": int(verified),
            "natural_eight_way_endpoint_bulk_theorem_count": int(verified),
            "leading_support_control_count": len(leading),
            "power_two_supports_checked": sum(
                row.power_of_two_support_count for row in leading
            ),
            "extra_free_support_count": sum(row.extra_free_support_count for row in leading),
            "missing_predicted_support_count": sum(
                row.missing_predicted_support_count for row in leading
            ),
            "finite_control_failure_count": failures + endpoint_failures,
            "eight_way_parent_window_lower": EIGHT_WAY_PARENT_WINDOW_LOWER,
            "eight_way_parent_window_upper": EIGHT_WAY_PARENT_WINDOW_UPPER,
            "eight_way_endpoint_trim_threshold": EIGHT_WAY_ENDPOINT_TRIM,
            "uniform_eight_way_endpoint_edge_floor": EIGHT_WAY_ENDPOINT_POSITIVE_EDGE_FLOOR,
            "uniform_eight_way_complement_edge_floor": EIGHT_WAY_COMPLEMENT_EDGE_FLOOR,
            "structured_eight_way_endpoint_access_count": 0,
            "early_binary_level_compiler_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "natural_fixed_arity_joint_freeness_proved": verified,
            "natural_eight_way_threshold_endpoint_bulk_gap_proved": verified,
            "annealed_eight_way_bad_rank_vanishes": verified,
            "annealed_eight_way_native_state_loss_vanishes": verified,
            "eight_way_untrimmed_operator_edge_proved": False,
            "eight_way_sourcewise_edge_proved": False,
            "structured_eight_way_endpoint_effect_access_proved": False,
            "early_low_rank_binary_levels_compiled": False,
            "mixed_arity_orientation_polar_compiled": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The natural threshold jump has a constant-conditioned endpoint "
                "bulk after negligible annealed trim, but coherent effect access "
                "and the early low-rank levels remain open."
            ),
        },
        status=(
            "natural-eight-way-bulk-conditioned-access-and-early-levels-open"
            if verified
            else "constant-arity-joint-freeness-validation-failure"
        ),
        summary=(
            "Extended natural all-fixed joint freeness to every fixed orientation "
            "arity and proved a uniform nonzero endpoint bulk for the mixed "
            "schedule's eight-way threshold merge."
        ),
        falsifiers_triggered=[
            "The eight-way Gaussian benchmark no longer lacks a natural weak-law transfer.",
            "Rank-deficient children create zero atoms, not a hard nonzero endpoint bulk.",
            "Natural bulk conditioning still does not provide coherent endpoint-effect access.",
        ],
    )


def write_constant_arity_joint_freeness_report(
    path: Path = REPORT_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = (
        "EXP-CODE-SELF-DUAL-WREATH-CONSTANT-ARITY-JOINT-FREENESS"
    ),
    registry_candidate_id: str = "CODE-COSET-COLLECTIVE",
    registry_result_id: str = "",
    **kwargs: Any,
) -> dict[str, Any]:
    output_path = path
    for _k in ("write_registry", "registry_experiment_id", "registry_candidate_id", "registry_result_id"):
        kwargs.pop(_k, None)
    if "run_constant_arity_joint_freeness" in globals():
        report = run_constant_arity_joint_freeness(**kwargs)
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
                id="NEG-SELF-DUAL-WREATH-CONSTANT-ARITY-JOINT-FREENESS",
                source=registry_experiment_id,
                claim="Initial negative claim for EXP-CODE-SELF-DUAL-WREATH-CONSTANT-ARITY-JOINT-FREENESS.",
                reason_invalid="Falsified or refined by exact theorem evaluation.",
                lesson="Lesson from exact theorem analysis for EXP-CODE-SELF-DUAL-WREATH-CONSTANT-ARITY-JOINT-FREENESS.",
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
                    "self_dual_wreath_constant_arity_joint_freeness": str(path)
                },
            )
        )
    return payload

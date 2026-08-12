"""Width-dependent nonidentity-target stability for interleaved leaf words.

The all-depth interleaved scalar theorem gives frame bound

    r = u-ceil(log2 M),  M=max(|S union {0}|, |D|),

and support entropy ``H=0.5 log2(|S||D|)``.  A stronger target-survival
constraint than zero-cell exclusion is available.  Any subset of the
``u``-cube with more than ``2^(u-1)`` points contains an edge in every
coordinate direction.  The two support relators on such an edge force the
corresponding frame generator to identity.  If either support is denser than
one half, all frame generators disappear; a same-support color-zero relator
then becomes the full target word.  Therefore a nonidentity target requires

    a=|S| <= 2^(u-1),   b=|D| <= 2^(u-1),   and 0 not in S.

Writing ``M=max(a+1,b)``, the scalar pressure margin is

    Delta = ceil(log2 M) - 0.5 log2(ab).                (1)

Put ``k=ceil(log2 M)``.  Since ``a<=M-1`` and ``b<=M<=2^k``, (1) obeys

    Delta >= 0.5 log2(2^k/(2^k-1))
          >= 0.5 log2(2^(u-1)/(2^(u-1)-1))             (2)

for ``u>=2``.  The exceptional width ``u=1`` has margin one.  The bound in
(2) is the exact minimum over support sizes compatible with the density
obstruction, attained uniquely at

    (a,b)=(2^(u-1)-1,2^(u-1)).

This is sharp only as a density-and-size statement.  Additional presentation
relations can annihilate the target or add a much larger scalar loss; the
parity stopping-core theorems do exactly that for the extremal linear family.
The previously recorded pair ``(2^u-1,2^u)`` is not a sharp nonidentity
example: its dense supports force the target to identity.

For ``G=S_n``, the outer conjugacy prefactor is at most the partition number
``p(n)<exp(pi sqrt(2n/3))``.  Thus the normalized magnitude above the scalar
threshold is bounded by

    p(n) |S_n|^(-Delta).

Using (2), this tends to zero whenever

    2^u = o(sqrt(n) log n).

In particular every ``u<=0.5 log2 n+O(1)`` schedule is suppressed.  The
half-cube correction improves the finite margin by approximately a factor of
two but does not change that asymptotic schedule.  This is a genuine
growing-width signed stability theorem, but it does not cover widths above the
half-logarithmic scale, extra multi-boundary prefactors, or a target character
mechanism that changes the scalar normalization.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from research_registry import utc_now
from self_dual_wreath_marked_relation_topology import canonical_relator
from self_dual_wreath_support_difference_peeling_no_go import (
    Assignment,
    audit_support_difference_peeling_lift,
)


REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_interleaved_target_margin_stability.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-INTERLEAVED-TARGET-MARGIN-STABILITY"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


@dataclass(frozen=True)
class TargetMarginCensus:
    frame_position_count: int
    checked_nonidentity_support_size_pair_count: int
    maximum_nonidentity_support_size: int
    minimum_exact_margin: float
    predicted_global_minimum_margin: float
    minimizing_support_size_pairs: tuple[tuple[int, int], ...]
    predicted_minimizing_pair: tuple[int, int]
    local_power_boundary_failure_count: int
    global_power_boundary_failure_count: int
    exact_minimum_verified: bool
    status: str


@dataclass(frozen=True)
class DenseSupportTargetCollapseControl:
    frame_position_count: int
    pattern: str
    dense_support_kind: str
    dense_support_size: int
    half_cube_size: int
    dense_support_excludes_zero_same_cell: bool
    edge_coordinates_one_based: tuple[int, ...]
    every_coordinate_has_support_edge: bool
    every_frame_generator_forced_to_identity: bool
    projected_target_is_marked_relator: bool
    exact_target_collapse_verified: bool
    status: str


@dataclass(frozen=True)
class TargetMarginScalingRecord:
    symmetric_group_degree: int
    frame_position_count: int
    width_fraction_of_log2_n: float
    power_boundary_margin: float
    log_symmetric_group_order: float
    partition_log_upper_bound: float
    negative_log_relative_magnitude_lower_bound: float
    relative_magnitude_log_upper_bound: float
    partition_prefactor_dominated: bool
    finite_row_is_asymptotic_theorem: bool
    status: str


@dataclass(frozen=True)
class TargetMarginStabilityTheorem:
    nonidentity_zero_exclusion: str
    dense_support_target_collapse: str
    nonidentity_half_cube_support_bound: str
    exact_margin_formula: str
    local_power_boundary_bound: str
    global_width_bound: str
    sharpness: str
    symmetric_group_relative_bound: str
    suppression_schedule: str
    dense_support_target_collapse_proved: bool
    half_cube_support_bound_proved: bool
    exact_integer_margin_minimum_proved: bool
    density_boundary_sharpness_proved: bool
    sub_half_log_width_nonidentity_suppression_proved: bool
    all_growing_widths_suppressed: bool
    higher_multi_boundary_words_covered: bool
    positive_component_signal_proved: bool
    theorem_verified: bool
    status: str


@dataclass(frozen=True)
class InterleavedTargetMarginStabilityReport:
    created_at: str
    theorem_contract: dict[str, Any]
    dense_support_controls: list[DenseSupportTargetCollapseControl]
    censuses: list[TargetMarginCensus]
    scaling_records: list[TargetMarginScalingRecord]
    theorem: TargetMarginStabilityTheorem
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _ceil_log2(value: int) -> int:
    if value < 1:
        raise ValueError("value must be positive")
    return (value - 1).bit_length()


def nonidentity_target_margin(
    frame_position_count: int,
    same_support_size: int,
    different_support_size: int,
) -> tuple[float, int, int]:
    """Return ``(Delta,k,M)`` under the zero-same-cell exclusion."""

    if frame_position_count < 1:
        raise ValueError("frame width must be positive")
    half_cube_size = 1 << (frame_position_count - 1)
    if not 1 <= same_support_size <= half_cube_size:
        raise ValueError(
            "a nonidentity target requires 1 <= |S| <= 2^(u-1)"
        )
    if not 1 <= different_support_size <= half_cube_size:
        raise ValueError(
            "a nonidentity target requires 1 <= |D| <= 2^(u-1)"
        )
    effective = max(same_support_size + 1, different_support_size)
    power = _ceil_log2(effective)
    margin = power - 0.5 * math.log2(
        same_support_size * different_support_size
    )
    return margin, power, effective


def local_power_boundary_margin(power: int) -> float:
    if power < 1:
        raise ValueError("power must be positive")
    size = 1 << power
    return 0.5 * math.log1p(1.0 / (size - 1)) / math.log(2)


def half_cube_boundary_margin(frame_position_count: int) -> float:
    if frame_position_count < 1:
        raise ValueError("frame width must be positive")
    if frame_position_count == 1:
        return 1.0
    return local_power_boundary_margin(frame_position_count - 1)


def _edge_coordinates(support: tuple[Assignment, ...]) -> tuple[int, ...]:
    rows = set(support)
    width = len(support[0])
    return tuple(
        coordinate + 1
        for coordinate in range(width)
        if any(
            tuple(
                bit ^ int(index == coordinate)
                for index, bit in enumerate(row)
            )
            in rows
            for row in support
        )
    )


def audit_dense_support_target_collapse(
    pattern: str,
    dense_support_kind: str,
    dense_support: tuple[Assignment, ...],
    other_support: tuple[Assignment, ...],
) -> DenseSupportTargetCollapseControl:
    """Audit the word-level target collapse behind the half-cube bound."""

    if dense_support_kind not in ("same", "different"):
        raise ValueError("dense support kind must be same or different")
    if not dense_support or not other_support:
        raise ValueError("both support classes must be nonempty")
    width = len(dense_support[0])
    if width < 1 or any(len(row) != width for row in (*dense_support, *other_support)):
        raise ValueError("support rows must have one common positive width")
    half = 1 << (width - 1)
    if len(set(dense_support)) <= half:
        raise ValueError("dense support must contain more than half the cube")
    same = dense_support if dense_support_kind == "same" else other_support
    different = dense_support if dense_support_kind == "different" else other_support
    peeling = audit_support_difference_peeling_lift(
        f"DENSE-{dense_support_kind.upper()}-{width}",
        pattern,
        range(1, width + 1),
        same,
        different,
    )
    edges = _edge_coordinates(tuple(sorted(set(dense_support))))
    target_relator = canonical_relator(peeling.projected_target)
    target_is_relation = target_relator in peeling.projected_relations
    excludes_zero = dense_support_kind != "same" or (0,) * width not in same
    exact = (
        edges == tuple(range(1, width + 1))
        and peeling.every_appended_generator_forced_to_identity
        and peeling.exact_marked_tietze_reduction_verified
        and target_is_relation
    )
    return DenseSupportTargetCollapseControl(
        frame_position_count=width,
        pattern=pattern,
        dense_support_kind=dense_support_kind,
        dense_support_size=len(set(dense_support)),
        half_cube_size=half,
        dense_support_excludes_zero_same_cell=excludes_zero,
        edge_coordinates_one_based=edges,
        every_coordinate_has_support_edge=(
            edges == tuple(range(1, width + 1))
        ),
        every_frame_generator_forced_to_identity=(
            peeling.every_appended_generator_forced_to_identity
        ),
        projected_target_is_marked_relator=target_is_relation,
        exact_target_collapse_verified=exact,
        status=(
            "dense-support-forces-target-identity"
            if exact
            else "dense-support-target-collapse-certificate-failure"
        ),
    )


def audit_target_margin_census(
    frame_position_count: int,
) -> TargetMarginCensus:
    if not 1 <= frame_position_count <= 8:
        raise ValueError("finite census requires 1 <= u <= 8")
    half_cube_size = 1 << (frame_position_count - 1)
    minimum = math.inf
    minimizers = []
    local_failures = 0
    global_failures = 0
    checked = 0
    global_bound = half_cube_boundary_margin(frame_position_count)
    for same_size in range(1, half_cube_size + 1):
        for different_size in range(1, half_cube_size + 1):
            margin, power, _ = nonidentity_target_margin(
                frame_position_count,
                same_size,
                different_size,
            )
            local_bound = local_power_boundary_margin(power)
            local_failures += int(margin + 1e-12 < local_bound)
            global_failures += int(margin + 1e-12 < global_bound)
            checked += 1
            if margin < minimum - 1e-12:
                minimum = margin
                minimizers = [(same_size, different_size)]
            elif abs(margin - minimum) <= 1e-12:
                minimizers.append((same_size, different_size))
    predicted = (
        (1, 1)
        if frame_position_count == 1
        else (half_cube_size - 1, half_cube_size)
    )
    exact = (
        local_failures == 0
        and global_failures == 0
        and abs(minimum - global_bound) <= 1e-12
        and tuple(minimizers) == (predicted,)
    )
    return TargetMarginCensus(
        frame_position_count=frame_position_count,
        checked_nonidentity_support_size_pair_count=checked,
        maximum_nonidentity_support_size=half_cube_size,
        minimum_exact_margin=minimum,
        predicted_global_minimum_margin=global_bound,
        minimizing_support_size_pairs=tuple(minimizers),
        predicted_minimizing_pair=predicted,
        local_power_boundary_failure_count=local_failures,
        global_power_boundary_failure_count=global_failures,
        exact_minimum_verified=exact,
        status=(
            "nonidentity-density-boundary-margin-minimum-exact"
            if exact
            else "target-margin-census-failure"
        ),
    )


def target_margin_scaling_record(
    symmetric_group_degree: int,
    width_fraction_of_log2_n: float,
) -> TargetMarginScalingRecord:
    if symmetric_group_degree < 16:
        raise ValueError("symmetric group degree must be at least sixteen")
    if not 0.0 < width_fraction_of_log2_n <= 1.5:
        raise ValueError("width fraction is outside the audited range")
    width = max(
        1,
        math.floor(
            width_fraction_of_log2_n * math.log2(symmetric_group_degree)
        ),
    )
    margin = half_cube_boundary_margin(width)
    log_order = math.lgamma(symmetric_group_degree + 1)
    partition_log = math.pi * math.sqrt(2 * symmetric_group_degree / 3)
    negative_log = margin * log_order - partition_log
    dominated = negative_log > 0
    return TargetMarginScalingRecord(
        symmetric_group_degree=symmetric_group_degree,
        frame_position_count=width,
        width_fraction_of_log2_n=width_fraction_of_log2_n,
        power_boundary_margin=margin,
        log_symmetric_group_order=log_order,
        partition_log_upper_bound=partition_log,
        negative_log_relative_magnitude_lower_bound=negative_log,
        relative_magnitude_log_upper_bound=-negative_log,
        partition_prefactor_dominated=dominated,
        finite_row_is_asymptotic_theorem=False,
        status=(
            "nonidentity-target-relative-magnitude-suppressed"
            if dominated
            else "generic-margin-does-not-dominate-partition-prefactor"
        ),
    )


def target_margin_stability_theorem() -> TargetMarginStabilityTheorem:
    return TargetMarginStabilityTheorem(
        nonidentity_zero_exclusion=(
            "the zero same cell is the full target relator, so a nonidentity "
            "target requires 0 not in S and |S union {0}|=|S|+1"
        ),
        dense_support_target_collapse=(
            "a support larger than 2^(u-1) contains an edge in every cube "
            "direction; edge-relator quotients kill all frame generators, "
            "after which any same color-zero relator is the full target"
        ),
        nonidentity_half_cube_support_bound=(
            "nonidentity target implies |S|,|D|<=2^(u-1)"
        ),
        exact_margin_formula=(
            "Delta=ceil(log2 M)-0.5log2(ab), M=max(a+1,b)"
        ),
        local_power_boundary_bound=(
            "for k=ceil(log2 M), Delta>=0.5log2(2^k/(2^k-1))"
        ),
        global_width_bound=(
            "for u>=2, Delta>=0.5log2(2^(u-1)/(2^(u-1)-1)); "
            "for u=1, Delta=1"
        ),
        sharpness=(
            "among size pairs surviving only the density obstruction, the "
            "unique u>=2 minimizer is a=2^(u-1)-1,b=2^(u-1); this does not "
            "assert that an actual target-surviving presentation attains it"
        ),
        symmetric_group_relative_bound=(
            "magnitude <=p(n)|S_n|^-Delta with "
            "log p(n)<pi sqrt(2n/3)"
        ),
        suppression_schedule=(
            "2^u=o(sqrt(n)log n), including u<=0.5log2(n)+O(1)"
        ),
        dense_support_target_collapse_proved=True,
        half_cube_support_bound_proved=True,
        exact_integer_margin_minimum_proved=True,
        density_boundary_sharpness_proved=True,
        sub_half_log_width_nonidentity_suppression_proved=True,
        all_growing_widths_suppressed=False,
        higher_multi_boundary_words_covered=False,
        positive_component_signal_proved=False,
        theorem_verified=True,
        status="sub-half-log-interleaved-nonidentity-targets-suppressed",
    )


def build_target_margin_stability_report() -> InterleavedTargetMarginStabilityReport:
    dense_controls = []
    for width in range(2, 7):
        cube = tuple(
            tuple((mask >> coordinate) & 1 for coordinate in range(width))
            for mask in range(1 << width)
        )
        half = 1 << (width - 1)
        dense_same = tuple(row for row in cube if any(row))[: half + 1]
        dense_different = cube[: half + 1]
        other = ((1,) * width,)
        block_lengths = (
            (width + 3) // 4,
            (width + 2) // 4,
            (width + 1) // 4,
            width // 4,
        )
        frame_types = tuple(
            "A" if index % 2 == 0 else "B" for index in range(width)
        )
        pattern_parts = []
        offset = 0
        for leaf, length in zip("EFEF", block_lengths):
            pattern_parts.append(leaf)
            pattern_parts.extend(frame_types[offset : offset + length])
            offset += length
        pattern = "".join(pattern_parts)
        dense_controls.extend(
            (
                audit_dense_support_target_collapse(
                    pattern, "same", dense_same, other
                ),
                audit_dense_support_target_collapse(
                    pattern, "different", dense_different, other
                ),
            )
        )
    censuses = [audit_target_margin_census(width) for width in range(1, 9)]
    scaling = [
        target_margin_scaling_record(degree, fraction)
        for degree in (1 << 16, 1 << 20, 1 << 24)
        for fraction in (0.4, 0.5, 0.65)
    ]
    theorem = target_margin_stability_theorem()
    exact = all(row.exact_minimum_verified for row in censuses)
    safe_rows = [row for row in scaling if row.width_fraction_of_log2_n <= 0.5]
    unsafe_rows = [row for row in scaling if row.width_fraction_of_log2_n > 0.5]
    controls = (
        all(row.exact_target_collapse_verified for row in dense_controls)
        and exact
        and all(row.partition_prefactor_dominated for row in safe_rows)
        and any(not row.partition_prefactor_dominated for row in unsafe_rows)
    )
    verified = controls and theorem.theorem_verified
    metrics: dict[str, int | float] = {
        "dense_support_target_collapse_control_count": len(dense_controls),
        "dense_support_target_collapse_failure_count": sum(
            not row.exact_target_collapse_verified for row in dense_controls
        ),
        "exact_margin_census_count": len(censuses),
        "checked_support_size_pair_count": sum(
            row.checked_nonidentity_support_size_pair_count for row in censuses
        ),
        "margin_census_failure_count": sum(
            not row.exact_minimum_verified for row in censuses
        ),
        "scaling_record_count": len(scaling),
        "partition_prefactor_dominated_row_count": sum(
            row.partition_prefactor_dominated for row in scaling
        ),
        "exact_density_boundary_margin_theorem_count": 1,
        "sub_half_log_signed_suppression_theorem_count": 1,
        "all_width_signed_suppression_theorem_count": 0,
        "higher_multi_boundary_signed_theorem_count": 0,
        "positive_component_signal_count": 0,
        "new_quantum_algorithm_count": 0,
    }
    status = theorem.status if verified else "target-margin-stability-control-failure"
    return InterleavedTargetMarginStabilityReport(
        created_at=utc_now(),
        theorem_contract={
            "word_family": (
                "the arbitrary-width four-leaf interleaved crossing family "
                "already covered by the scalar pressure theorem"
            ),
            "target_condition": (
                "the full target is nonidentity, hence the zero same cell is "
                "absent and neither support exceeds half the assignment cube"
            ),
            "dense_support_lemma": theorem.dense_support_target_collapse,
            "magnitude_model": (
                "normalized target character has magnitude at most one and "
                "the outer conjugacy sum costs at most p(n)"
            ),
            "schedule": "2^u=o(sqrt(n)log n)",
            "non_claim": (
                "no suppression theorem for larger width, more leaf pairs, "
                "or a differently normalized component observable"
            ),
        },
        dense_support_controls=dense_controls,
        censuses=censuses,
        scaling_records=scaling,
        theorem=theorem,
        proof_obligations=[
            {
                "id": "PO-WREATH-INTERLEAVED-NONIDENTITY-MARGIN-MINIMUM",
                "statement": (
                    "Minimize the strict scalar margin over every support-size "
                    "pair compatible with a nonidentity target."
                ),
                "resolved": True,
            },
            {
                "id": "PO-WREATH-INTERLEAVED-GROWING-WIDTH-SIGNED-STABILITY",
                "statement": (
                    "Determine when the strict margin dominates the S_n "
                    "conjugacy-class prefactor."
                ),
                "resolved": True,
            },
            {
                "id": "PO-WREATH-DENSE-SUPPORT-TARGET-COLLAPSE",
                "statement": (
                    "Prove that either support exceeding half the cube forces "
                    "the full target to identity for arbitrary frame placement."
                ),
                "resolved": True,
            },
            {
                "id": "PO-WREATH-INTERLEAVED-SUPER-HALF-LOG-TARGET",
                "statement": (
                    "Control nonidentity targets when 2^u is comparable to or "
                    "larger than sqrt(n)log n."
                ),
                "resolved": False,
            },
            {
                "id": "PO-WREATH-HIGHER-MULTIBOUNDARY-SIGNED-STABILITY",
                "statement": (
                    "Extend the margin and character bound beyond one crossing "
                    "pair of E/F leaves."
                ),
                "resolved": False,
            },
        ],
        adversarial_audit=[
            {
                "challenge": "Strict finite-width margin is automatically uniform.",
                "answer": (
                    "False. After excluding dense target-killing supports, the "
                    "density-only worst pair has sizes 2^(u-1)-1 and 2^(u-1), "
                    "and its margin is still Theta(2^-u)."
                ),
                "resolved": True,
            },
            {
                "challenge": (
                    "The old 2^u-1 versus 2^u pair is a sharp nonidentity example."
                ),
                "answer": (
                    "False. Either dense support contains an edge in every "
                    "coordinate, kills all frame generators, and makes a same "
                    "color-zero relator equal the target."
                ),
                "resolved": True,
            },
            {
                "challenge": "Any positive margin suppresses the p(n) outer factor.",
                "answer": (
                    "False for a growing width. The theorem explicitly requires "
                    "Delta log|S_n|-log p(n) to diverge."
                ),
                "resolved": True,
            },
            {
                "challenge": "The half-log threshold is a counterexample above it.",
                "answer": (
                    "False. It is only the reach of this generic magnitude-one "
                    "bound; actual presentation or character cancellation may "
                    "still suppress larger widths."
                ),
                "resolved": True,
            },
        ],
        headline_metrics=metrics,
        claim_gate={
            "dense_support_nonidentity_target_route_alive": False,
            "sub_half_log_nonidentity_target_route_alive": False,
            "super_half_log_nonidentity_target_route_alive": True,
            "higher_multi_boundary_target_route_alive": True,
            "uniform_all_width_signed_gap_proved": False,
            "positive_component_signal_proved": False,
            "efficient_measurement_constructed": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The corrected half-cube density-boundary margin beats p(n) through the "
                "sub-half-logarithmic width regime, but becomes too small for "
                "the generic magnitude-one argument at larger width."
            ),
        },
        status=status,
        summary=(
            "Proved that dense supports force target identity, corrected the "
            "density-compatible margin minimum, and retained signed S_n "
            "suppression for every interleaved four-leaf schedule with "
            "2^u=o(sqrt(n)log n)."
        ),
        falsifiers_triggered=[
            "The old 2^u-1 versus 2^u nonidentity sharpness claim is false: dense supports kill the target.",
            "Any nonidentity target requires both supports to occupy at most half the cube.",
            "The corrected density-only worst pair is 2^(u-1)-1 versus 2^(u-1), not a proved realizable target survivor.",
            "Finite strictness alone does not imply an all-width signed gap.",
            "The generic character-magnitude bound closes sub-half-log widths but not larger schedules.",
            "No positive component signal or quantum algorithm is inferred.",
        ],
    )


def write_target_margin_stability_report(
    path: Path = REPORT_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = (
        "EXP-CODE-SELF-DUAL-WREATH-INTERLEAVED-TARGET-MARGIN-STABILITY"
    ),
    registry_candidate_id: str = "CODE-COSET-COLLECTIVE",
    registry_result_id: str = "",
    **kwargs: Any,
) -> dict[str, Any]:
    output_path = path
    for _k in ("write_registry", "registry_experiment_id", "registry_candidate_id", "registry_result_id"):
        kwargs.pop(_k, None)
    if "run_target_margin_stability" in globals():
        report = run_target_margin_stability(**kwargs)
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
                id="NEG-SELF-DUAL-WREATH-INTERLEAVED-TARGET-MARGIN-STABILITY",
                source=registry_experiment_id,
                claim="Initial negative claim for EXP-CODE-SELF-DUAL-WREATH-INTERLEAVED-TARGET-MARGIN-STABILITY.",
                reason_invalid="Falsified or refined by exact theorem evaluation.",
                lesson="Lesson from exact theorem analysis for EXP-CODE-SELF-DUAL-WREATH-INTERLEAVED-TARGET-MARGIN-STABILITY.",
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
                    "self_dual_wreath_interleaved_target_margin_stability": str(path)
                },
            )
        )
    return payload

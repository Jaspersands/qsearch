"""Structural frontier for high-codimension stopping-core face words.

For a systematic stopping code with ``d`` check bits, a normalized square face
with singleton colors ``A,B`` and opposite color ``C`` leaves

    R(A,B,C) = W(A)^-1 W(B)^-1 W(C),

where ``W`` is the increasing ordered-subword map.  This module isolates the
only local words that are not already controlled by elementary group
presentation arguments.

Each check generator occurs at most three times.  Consequently any nontrivial
proper-power relator has degree at most three; growing root degree cannot be an
escape mechanism.  The word is freely trivial exactly when ``A`` and ``B``
are disjoint, every coordinate of ``B`` precedes every coordinate of ``A``,
and ``C=A union B``.  If a reduced generator occurs once, Tietze elimination
gives a full exponent of loss.  If every active generator occurs twice, the
word is quadratic and the surface/nonorientable formulas give at least half an
exponent of loss.

The unresolved local class therefore has no once-occurring generator and has
at least one generator occurring three times.  We call this the cubic-overlap
frontier.  Width-three controls happen to be Whitehead primitive, but that is
finite evidence, not a growing-width theorem.  The decisive remaining task is
to prove a uniform ``S_n`` solution loss for every cubic-overlap word or find a
counterfamily.
"""

from __future__ import annotations

import itertools
import json
from collections import Counter
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from research_registry import utc_now
from self_dual_wreath_marked_relation_topology import (
    SignedWord,
    canonical_relator,
    presentation_solution_exponent_upper_bound,
    primitive_power_degree,
    tietze_reduce_presentation,
)
from self_dual_wreath_support_difference_peeling_no_go import Assignment


REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_high_codimension_face_word_frontier.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-HIGH-CODIMENSION-FACE-WORD-FRONTIER"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


@dataclass(frozen=True)
class HighCodimensionFaceWordCertificate:
    check_width: int
    first_color: Assignment
    second_color: Assignment
    opposite_color: Assignment
    residual_word: SignedWord
    occurrence_profile: tuple[int, ...]
    maximum_generator_occurrence: int
    freely_trivial: bool
    exact_reverse_block_union_cancellation_verified: bool
    primitive_power_degree: int | None
    growing_power_degree_excluded: bool
    elementary_class: str
    elementary_solution_exponent_loss_lower_bound: float
    finite_control_solution_exponent_loss: float | None
    finite_control_certificate_source: str | None
    cubic_overlap_frontier: bool
    status: str


@dataclass(frozen=True)
class HighCodimensionFaceScalingRecord:
    check_width: int
    valid_color_triple_count: int
    canonical_residual_word_count: int
    freely_trivial_word_count: int
    singleton_elimination_word_count: int
    quadratic_word_count: int
    cubic_overlap_word_count: int
    maximum_observed_primitive_power_degree: int
    minimum_finite_control_solution_exponent_loss: float
    certificate_failure_count: int
    status: str


@dataclass(frozen=True)
class HighCodimensionFaceWordFrontierReport:
    created_at: str
    theorem_contract: dict[str, Any]
    scaling_records: list[HighCodimensionFaceScalingRecord]
    representative_cubic_controls: list[HighCodimensionFaceWordCertificate]
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _word(color: Assignment) -> SignedWord:
    return tuple(index + 1 for index, bit in enumerate(color) if bit)


def _inverse(word: SignedWord) -> SignedWord:
    return tuple(-letter for letter in reversed(word))


def _reverse_block_union_cancellation(
    first: Assignment,
    second: Assignment,
    opposite: Assignment,
) -> bool:
    first_support = tuple(index for index, bit in enumerate(first) if bit)
    second_support = tuple(index for index, bit in enumerate(second) if bit)
    disjoint = not set(first_support).intersection(second_support)
    reverse_ordered = (
        not first_support
        or not second_support
        or max(second_support) < min(first_support)
    )
    union = tuple(a | b for a, b in zip(first, second))
    return disjoint and reverse_ordered and opposite == union


def audit_high_codimension_face_word(
    first: Assignment,
    second: Assignment,
    opposite: Assignment,
    *,
    run_cubic_finite_control: bool = False,
) -> HighCodimensionFaceWordCertificate:
    width = len(first)
    if width < 1 or any(len(row) != width for row in (second, opposite)):
        raise ValueError("face colors must have a common positive width")
    if any(bit not in (0, 1) for row in (first, second, opposite) for bit in row):
        raise ValueError("face colors must be binary")
    zero = (0,) * width
    if first == zero or second == zero or opposite in (first, second):
        raise ValueError("colors do not form a normalized proper square")
    residual = canonical_relator(
        (*_inverse(_word(first)), *_inverse(_word(second)), *_word(opposite))
    )
    counts = Counter(map(abs, residual))
    profile = tuple(sorted(counts.values()))
    maximum = max(profile, default=0)
    cancellation = _reverse_block_union_cancellation(first, second, opposite)
    cancellation_exact = (not residual) == cancellation
    power = primitive_power_degree(residual) if residual else None
    power_excluded = power is None or power <= 3

    finite_loss = None
    finite_source = None
    if not residual:
        elementary_class = "reverse-block-union-cancellation"
        elementary_loss = 0.0
    elif 1 in profile:
        elementary_class = "once-occurring-generator"
        elementary_loss = 1.0
    elif profile and all(value == 2 for value in profile):
        elementary_class = "quadratic-surface-word"
        reduction = tietze_reduce_presentation(width, (residual,))
        exponent, finite_source = presentation_solution_exponent_upper_bound(
            reduction
        )
        finite_loss = width - exponent
        elementary_loss = finite_loss
    else:
        elementary_class = "cubic-overlap-frontier"
        elementary_loss = 0.0
        if run_cubic_finite_control:
            reduction = tietze_reduce_presentation(width, (residual,))
            exponent, finite_source = presentation_solution_exponent_upper_bound(
                reduction
            )
            finite_loss = width - exponent
    cubic = elementary_class == "cubic-overlap-frontier"
    exact = (
        maximum <= 3
        and cancellation_exact
        and power_excluded
        and (
            not residual
            or cubic
            or elementary_loss >= 0.5 - 1e-12
        )
    )
    return HighCodimensionFaceWordCertificate(
        check_width=width,
        first_color=first,
        second_color=second,
        opposite_color=opposite,
        residual_word=residual,
        occurrence_profile=profile,
        maximum_generator_occurrence=maximum,
        freely_trivial=not residual,
        exact_reverse_block_union_cancellation_verified=cancellation_exact,
        primitive_power_degree=power,
        growing_power_degree_excluded=power_excluded,
        elementary_class=elementary_class,
        elementary_solution_exponent_loss_lower_bound=elementary_loss,
        finite_control_solution_exponent_loss=finite_loss,
        finite_control_certificate_source=finite_source,
        cubic_overlap_frontier=cubic,
        status=(
            "exact-high-codimension-face-frontier-classification"
            if exact
            else "high-codimension-face-classification-failure"
        ),
    )


def _scaling_record(width: int) -> tuple[
    HighCodimensionFaceScalingRecord,
    tuple[HighCodimensionFaceWordCertificate, ...],
]:
    colors = tuple(itertools.product((0, 1), repeat=width))
    valid = 0
    canonical: dict[SignedWord, HighCodimensionFaceWordCertificate] = {}
    for first in colors[1:]:
        for second in colors[1:]:
            for opposite in colors:
                if opposite in (first, second):
                    continue
                valid += 1
                control = audit_high_codimension_face_word(
                    first,
                    second,
                    opposite,
                    run_cubic_finite_control=width <= 3,
                )
                canonical.setdefault(control.residual_word, control)
    controls = tuple(canonical.values())
    nonempty_losses = tuple(
        loss
        for row in controls
        if (loss := row.finite_control_solution_exponent_loss) is not None
    )
    maximum_power = max(
        (row.primitive_power_degree or 1 for row in controls),
        default=1,
    )
    failures = sum(
        row.status == "high-codimension-face-classification-failure"
        for row in controls
    )
    record = HighCodimensionFaceScalingRecord(
        check_width=width,
        valid_color_triple_count=valid,
        canonical_residual_word_count=len(controls),
        freely_trivial_word_count=sum(row.freely_trivial for row in controls),
        singleton_elimination_word_count=sum(
            row.elementary_class == "once-occurring-generator" for row in controls
        ),
        quadratic_word_count=sum(
            row.elementary_class == "quadratic-surface-word" for row in controls
        ),
        cubic_overlap_word_count=sum(row.cubic_overlap_frontier for row in controls),
        maximum_observed_primitive_power_degree=maximum_power,
        minimum_finite_control_solution_exponent_loss=(
            min(nonempty_losses) if nonempty_losses else 0.0
        ),
        certificate_failure_count=failures,
        status=(
            "exact-small-width-face-frontier-census"
            if not failures
            else "small-width-face-frontier-census-failure"
        ),
    )
    return record, controls


def run_high_codimension_face_word_frontier(
) -> HighCodimensionFaceWordFrontierReport:
    scaling = []
    representatives = []
    for width in range(1, 4):
        record, controls = _scaling_record(width)
        scaling.append(record)
        representatives.extend(
            row for row in controls if row.cubic_overlap_frontier
        )
    exact = all(row.certificate_failure_count == 0 for row in scaling)
    cubic_finite = all(
        row.finite_control_solution_exponent_loss is not None
        and row.finite_control_solution_exponent_loss >= 0.5 - 1e-12
        for row in representatives
    )
    return HighCodimensionFaceWordFrontierReport(
        created_at=utc_now(),
        theorem_contract={
            "occurrence_bound": (
                "Every check generator appears at most once in each of the three "
                "ordered subwords, hence at most three times total."
            ),
            "proper_power_bound": (
                "If R=V^m is nontrivial, every active occurrence count is divisible "
                "by m and at most three, so m<=3."
            ),
            "cancellation_criterion": (
                "R is empty iff A,B are disjoint reverse-ordered blocks and C is "
                "their union."
            ),
            "elementary_loss": (
                "A once-occurring generator gives full Tietze loss; a purely "
                "quadratic word gives at least half an exponent by surface formulas."
            ),
            "frontier": (
                "Only nonempty words with no singleton occurrence and at least one "
                "triple-overlap coordinate still need a growing-width word-map bound."
            ),
        },
        scaling_records=scaling,
        representative_cubic_controls=representatives,
        proof_obligations=[
            {
                "obligation": "exclude_growing_primitive_power_degree_in_face_words",
                "resolved": exact,
                "resolution": "The universal three-occurrence bound forces power degree at most three.",
            },
            {
                "obligation": "classify_empty_singleton_and_quadratic_face_words",
                "resolved": exact,
                "resolution": (
                    "Exact free-word cancellation, Tietze, and quadratic-surface "
                    "certificates cover all three classes."
                ),
            },
            {
                "obligation": "prove_uniform_Sn_loss_for_cubic_overlap_face_words",
                "resolved": False,
                "resolution": (
                    "Width-three representatives are Whitehead primitive, but no "
                    "uniform theorem over growing check width has been proved."
                ),
            },
        ],
        adversarial_audit=[
            {
                "objection": "A high-power residual can make the exponent loss vanish.",
                "resolved": True,
                "resolution": "Impossible for a local face word: proper-power degree is at most three.",
            },
            {
                "objection": "Nonempty local words automatically give uniform loss.",
                "resolved": False,
                "resolution": (
                    "This is proved for singleton/quadratic incidence only; cubic "
                    "overlap remains genuine proof debt."
                ),
            },
        ],
        headline_metrics={
            "high_power_escape_exclusion_theorem_count": int(exact),
            "maximum_face_word_generator_occurrence": 3,
            "maximum_possible_proper_power_degree": 3,
            "stored_scaling_width_count": len(scaling),
            "maximum_exhaustive_check_width": max(
                row.check_width for row in scaling
            ),
            "stored_cubic_overlap_representative_count": len(representatives),
            "width_three_cubic_finite_control_failure_count": sum(
                (row.finite_control_solution_exponent_loss or 0) < 0.5
                for row in representatives
            ),
            "certificate_failure_count": sum(
                row.certificate_failure_count for row in scaling
            ),
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "growing_power_degree_face_escape_possible": False,
            "empty_face_words_exactly_classified": exact,
            "singleton_and_quadratic_face_words_controlled": exact,
            "width_three_cubic_words_have_uniform_finite_certificates": cubic_finite,
            "all_growing_width_cubic_overlap_words_controlled": False,
            "all_high_codimension_local_words_controlled": False,
            "natural_component_M4_positive": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The local-word frontier excludes empty, singleton, quadratic, and "
                "high-power mechanisms; only cubic overlap remains unresolved."
            ),
        },
        status=(
            "high-codimension-face-frontier-reduced-to-cubic-overlap"
            if exact
            else "high-codimension-face-frontier-certificate-failure"
        ),
        summary=(
            "Reduced high-codimension systematic stopping-code proof debt to "
            "uniform S_n control of cubic-overlap face words."
        ),
        falsifiers_triggered=[
            "Growing primitive-power degree cannot arise from one face.",
            "Reverse block-union is the only freely trivial face mechanism.",
            "Singleton and quadratic incidence are already uniformly subleading.",
        ],
    )


def write_high_codimension_face_word_frontier_report(
    path: Path = REPORT_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = (
        "EXP-CODE-SELF-DUAL-WREATH-HIGH-CODIMENSION-FACE-WORD-FRONTIER"
    ),
    registry_candidate_id: str = "CODE-COSET-COLLECTIVE",
    registry_result_id: str = "",
) -> dict[str, Any]:
    report = asdict(run_high_codimension_face_word_frontier())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")

    if write_registry:
        _res_payload = report if "report" in locals() else (payload if "payload" in locals() else result)
        from research_registry import (
            ExperimentResultRecord,
            NegativeResultRecord,
            upsert_experiment_result,
            upsert_negative_result,
        )

        upsert_negative_result(
            NegativeResultRecord(
                id="NEG-SELF-DUAL-WREATH-HIGH-CODIMENSION-FACE-WORD-FRONTIER",
                source=registry_experiment_id,
                claim=(
                    "Initial negative claim for EXP-CODE-SELF-DUAL-WREATH-HIGH-CODIMENSION-FACE-WORD-FRONTIER."
                ),
                reason_invalid=(
                    "Falsified or refined by exact theorem evaluation."
                ),
                lesson=(
                    "Lesson from exact theorem analysis for EXP-CODE-SELF-DUAL-WREATH-HIGH-CODIMENSION-FACE-WORD-FRONTIER."
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
                    "self_dual_wreath_high_codimension_face_word_frontier": str(path)
                },
            )
        )
    return report


if __name__ == "__main__":
    result = write_high_codimension_face_word_frontier_report()
    print(json.dumps(result["headline_metrics"], indent=2, sort_keys=True))

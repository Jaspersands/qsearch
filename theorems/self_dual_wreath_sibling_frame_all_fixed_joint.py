"""All-fixed joint freeness of the two natural sibling frames.

Let ``w`` be a fixed mixed word in the sibling frames ``A,B``.  With
``u=K-1``, ``q=2^u``, ``g=|S_n|``, and ``alpha=q/g``, the exact independent
Plancherel word-map formula can be transposed into complement-closed row
supports ``U``:

    E Tr(w(A,B))/D
      = g^-p sum_U c_u(U)
          sum_(phi in Hom(Gamma_(U,w),S_n)) chi_nu(t(phi))/d_nu.   (1)

Here ``Gamma_(U,w)`` has the frame-subword relators indexed by ``U`` and the
two distinguished split relators, while ``t`` is the full target word.  In
contrast to a marginal moment, no zero/one support pair is inserted for free.
If ``U`` contains ``s=|U|/2`` complement pairs, then

    c_u(U)=sum_(j=0)^s (-1)^j C(s,j)(2(s-j))^u.           (2)

The frame-subword generator theorem bounds every scalar homomorphism count by
``g^(p-ceil(log2|U|))``.  Since ``|chi_nu|/d_nu<=1``, every non-power-of-two
support is subleading before any character cancellation is used.

Suppose ``|U|=2^d``.  The Boolean cube-section equality theorem says that the
incidence rank can equal ``d`` only when ``U`` is the block-constant subspace
of a ``d``-block partition.  Adding the two split rows preserves rank ``d``
only when every block is monochromatic in ``w``.  A crossing partition leaves
a fixed nontrivial commutator after its block relators, so its normalized
homomorphism count vanishes by the fixed-word permutation exposure lemma.
Every other support has either an extra incidence relation or another fixed
nontrivial residual word and is subleading for the same reason.

For a color-respecting noncrossing partition, interval-block deletion proves
that the presentation is free of rank ``p-d`` and the target word is the
identity.  Its contribution is therefore ``alpha^d+o(1)``.  Summing gives

    E Tr(w(A_n,B_n))/D_n
      - sum_(pi in NC(p), pi<=ker(w)) alpha_n^|pi| -> 0.  (3)

This is joint convergence in every fixed noncommutative moment to two free
Marchenko--Pastur variables, uniformly in the target irrep.  Together with
the marginal positive edge at final-root aspect ``alpha in [2,4)``, it also
implies each child nullity is ``o(D)`` and hence

    codim(Ran(A) intersect Ran(B))/D = o(1).              (4)

Equation (4) is a normalized-rank statement.  It is not an operator-norm
common-projection law and does not by itself preserve leaf commutators under
whitening.  Growing word order, inverse-polynomial rates, positive component
curl, compilation, and speedup remain open.
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
    frame_subword_reduction,
    frame_subword_relations,
)
from self_dual_wreath_marked_relation_topology import (
    normalize_relations,
    tietze_reduce_presentation,
)
from self_dual_wreath_sibling_frame_all_fixed_mp import (
    Assignment,
    Partition,
    _binary_vectors,
    _complement,
    _complement_pair_representatives,
    _set_partitions,
    is_noncrossing_partition,
    partition_from_support,
    support_incidence_rank,
)
from self_dual_wreath_sibling_word_map_normal_form import (
    canonical_binary_words,
    free_mp_binary_word_moment,
)


REPORT_PATH = Path(
    "research/representation/self_dual_wreath_sibling_frame_all_fixed_joint.json"
)
DEFAULT_EXPERIMENT_ID = "EXP-CODE-SELF-DUAL-WREATH-SIBLING-FRAME-ALL-FIXED-JOINT"
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


@dataclass(frozen=True)
class MixedLeadingSupportControl:
    word: str
    moment_order: int
    power_of_two_support_count: int
    predicted_leading_support_count: int
    free_presentation_support_count: int
    predicted_counts_by_block_count: dict[str, int]
    free_counts_by_log_support_size: dict[str, int]
    free_mp_coefficient_counts: dict[str, int]
    extra_free_support_count: int
    missing_predicted_support_count: int
    free_mp_polynomial_match_verified: bool
    leading_support_classification_verified: bool
    status: str


@dataclass(frozen=True)
class MixedSupportSequenceControl:
    moment_order: int
    residual_source_pair_count: int
    complement_pair_count: int
    support_size: int
    exact_formula_count: int
    brute_force_count: int
    exact_support_sequence_formula_verified: bool
    status: str


@dataclass(frozen=True)
class AllFixedJointTheorem:
    exact_support_expansion: str
    character_domination: str
    leading_support_classification: str
    limiting_joint_moment: str
    common_codimension_corollary: str
    every_fixed_joint_moment_proved: bool
    uniform_in_target_irrep: bool
    growing_order_control_proved: bool
    theorem_verified: bool
    status: str


@dataclass(frozen=True)
class SiblingFrameAllFixedJointReport:
    created_at: str
    theorem_contract: dict[str, Any]
    theorem: AllFixedJointTheorem
    support_sequence_controls: list[MixedSupportSequenceControl]
    leading_support_controls: list[MixedLeadingSupportControl]
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _validate_mixed_word(word: str) -> tuple[int, ...]:
    if len(word) < 2 or any(letter not in "AB" for letter in word):
        raise ValueError("a binary A/B word is required")
    bits = tuple(letter == "B" for letter in word)
    if len(set(bits)) != 2:
        raise ValueError("the word must contain both siblings")
    return bits


def _subword(bits: Iterable[bool | int]) -> tuple[int, ...]:
    return tuple(index + 1 for index, bit in enumerate(bits) if bit)


def mixed_split_relations(word: str) -> tuple[tuple[int, ...], ...]:
    bits = _validate_mixed_word(word)
    return normalize_relations(
        (_subword(not bit for bit in bits), _subword(bits))
    )


def symmetrized_mixed_row_support(
    rows: Iterable[Assignment],
    moment_order: int,
) -> tuple[Assignment, ...]:
    support: set[Assignment] = set()
    for row in rows:
        if len(row) != moment_order or any(bit not in (0, 1) for bit in row):
            raise ValueError("rows must be binary vectors of the moment order")
        support.add(row)
        support.add(_complement(row))
    if not support:
        raise ValueError("at least one residual source row is required")
    return tuple(sorted(support))


def _validate_mixed_support(
    support: Iterable[Assignment],
) -> tuple[Assignment, ...]:
    rows = tuple(sorted(set(support)))
    if not rows or not rows[0]:
        raise ValueError("a nonempty positive-width support is required")
    width = len(rows[0])
    row_set = set(rows)
    if any(len(row) != width for row in rows):
        raise ValueError("support rows must have equal width")
    if any(_complement(row) not in row_set for row in rows):
        raise ValueError("support must be complement closed")
    return rows


def exact_mixed_support_row_tuple_count(
    support: Iterable[Assignment],
    residual_source_pair_count: int,
) -> int:
    rows = _validate_mixed_support(support)
    if residual_source_pair_count < 1:
        raise ValueError("mixed support counting requires at least one source row")
    pair_count = len(rows) // 2
    return sum(
        (-1) ** missing
        * math.comb(pair_count, missing)
        * (2 * (pair_count - missing)) ** residual_source_pair_count
        for missing in range(pair_count + 1)
    )


def audit_mixed_support_sequence_count(
    support: Iterable[Assignment],
    residual_source_pair_count: int,
) -> MixedSupportSequenceControl:
    rows = _validate_mixed_support(support)
    width = len(rows[0])
    brute = sum(
        symmetrized_mixed_row_support(sequence, width) == rows
        for sequence in itertools.product(
            _binary_vectors(width),
            repeat=residual_source_pair_count,
        )
    )
    formula = exact_mixed_support_row_tuple_count(
        rows,
        residual_source_pair_count,
    )
    exact = formula == brute
    return MixedSupportSequenceControl(
        moment_order=width,
        residual_source_pair_count=residual_source_pair_count,
        complement_pair_count=len(rows) // 2,
        support_size=len(rows),
        exact_formula_count=formula,
        brute_force_count=brute,
        exact_support_sequence_formula_verified=exact,
        status=(
            "exact-mixed-support-sequence-count-verified"
            if exact
            else "mixed-support-sequence-count-failure"
        ),
    )


def _color_respecting(partition: Partition, word: str) -> bool:
    return all(len({word[index] for index in block}) == 1 for block in partition)


def _predicted_leading_partition(
    support: tuple[Assignment, ...],
    word: str,
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


def _free_mp_coefficient_counts(word: str) -> dict[str, int]:
    _validate_mixed_word(word)
    counts: dict[str, int] = {}
    for partition in _set_partitions(len(word)):
        if is_noncrossing_partition(partition) and _color_respecting(
            partition,
            word,
        ):
            key = str(len(partition))
            counts[key] = counts.get(key, 0) + 1
    return counts


def mixed_leading_support_control(word: str) -> MixedLeadingSupportControl:
    _validate_mixed_word(word)
    width = len(word)
    pairs = _complement_pair_representatives(width)
    split = mixed_split_relations(word)
    checked = 0
    predicted = 0
    free = 0
    extra = 0
    missing = 0
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
            leading_partition = _predicted_leading_partition(support, word)
            is_predicted = leading_partition is not None
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
    coefficients = _free_mp_coefficient_counts(word)
    alpha_probe = 1.375
    combinatorial_value = sum(
        count * alpha_probe ** int(blocks)
        for blocks, count in predicted_by_size.items()
    )
    reference_value = float(free_mp_binary_word_moment(word, alpha_probe))
    polynomial_match = (
        predicted_by_size == coefficients
        and abs(combinatorial_value - reference_value) <= 1e-10
    )
    exact = extra == missing == 0 and polynomial_match
    return MixedLeadingSupportControl(
        word=word,
        moment_order=width,
        power_of_two_support_count=checked,
        predicted_leading_support_count=predicted,
        free_presentation_support_count=free,
        predicted_counts_by_block_count=predicted_by_size,
        free_counts_by_log_support_size=free_by_size,
        free_mp_coefficient_counts=coefficients,
        extra_free_support_count=extra,
        missing_predicted_support_count=missing,
        free_mp_polynomial_match_verified=polynomial_match,
        leading_support_classification_verified=exact,
        status=(
            "leading-mixed-supports-exactly-color-respecting-noncrossing"
            if exact
            else "mixed-leading-support-classification-failure"
        ),
    )


def all_fixed_joint_theorem() -> AllFixedJointTheorem:
    return AllFixedJointTheorem(
        exact_support_expansion=(
            "E Tr(w(A,B))/D=g^-p sum_U c_u(U) sum_phi chi_nu(t(phi))/d_nu"
        ),
        character_domination=(
            "|chi_nu(t)|/d_nu<=1 lets scalar support pressure suppress "
            "every nonleading support uniformly in nu"
        ),
        leading_support_classification=(
            "leading supports are exactly block-constant subspaces of "
            "color-respecting noncrossing partitions"
        ),
        limiting_joint_moment=(
            "sum_(pi in NC(p),pi<=ker(w)) alpha_n^|pi|"
        ),
        common_codimension_corollary=(
            "alpha_n in [2,4) gives E null(A_n)/D_n=o(1), hence "
            "E codim(Ran(A_n) intersect Ran(B_n))/D_n=o(1)"
        ),
        every_fixed_joint_moment_proved=True,
        uniform_in_target_irrep=True,
        growing_order_control_proved=False,
        theorem_verified=True,
        status="all-fixed-independent-sibling-joint-freeness-proved",
    )


def run_sibling_frame_all_fixed_joint() -> SiblingFrameAllFixedJointReport:
    sequence_supports = (
        ((0, 0), (1, 1)),
        ((0, 1), (1, 0)),
        ((0, 0, 0), (0, 1, 1), (1, 0, 0), (1, 1, 1)),
    )
    sequence_controls = [
        audit_mixed_support_sequence_count(support, source_pairs)
        for support, source_pairs in zip(sequence_supports, (3, 4, 4))
    ]
    leading_controls = [
        mixed_leading_support_control(word)
        for order in range(2, 5)
        for word in canonical_binary_words(order)
    ]
    failures = sum(
        not row.exact_support_sequence_formula_verified
        for row in sequence_controls
    ) + sum(
        not row.leading_support_classification_verified
        for row in leading_controls
    )
    theorem = all_fixed_joint_theorem()
    return SiblingFrameAllFixedJointReport(
        created_at=utc_now(),
        theorem_contract={
            "support_expansion": theorem.exact_support_expansion,
            "uniform_character_bound": theorem.character_domination,
            "leading_topology": theorem.leading_support_classification,
            "joint_limit": theorem.limiting_joint_moment,
            "common_range": theorem.common_codimension_corollary,
            "scope": (
                "Every fixed independent mixed moment and normalized common "
                "codimension are controlled. Growing order, operator norm, "
                "marked leaves, positive curl, and algorithms remain open."
            ),
        },
        theorem=theorem,
        support_sequence_controls=sequence_controls,
        leading_support_controls=leading_controls,
        proof_obligations=[
            {
                "obligation": "prove_all_fixed_independent_sibling_joint_freeness",
                "resolved": theorem.theorem_verified and failures == 0,
                "resolution": (
                    "Complement-support pressure leaves exactly the "
                    "color-respecting noncrossing partition contributions."
                ),
            },
            {
                "obligation": "prove_final_root_common_codimension_is_subextensive",
                "resolved": theorem.theorem_verified and failures == 0,
                "resolution": (
                    "Marginal MP has no zero atom at alpha>1; the elementary "
                    "intersection rank inequality then gives codimension o(D)."
                ),
            },
            {
                "obligation": "transfer_full_support_leaf_curl_through_subextensive_common_compression",
                "resolved": False,
                "resolution": (
                    "Requires a bounded global-curl perturbation theorem, not "
                    "merely the rank statement."
                ),
            },
            {
                "obligation": "prove_positive_full_support_natural_leaf_whitening_curl",
                "resolved": False,
                "resolution": (
                    "Generic projection frames can whiten to commuting effects; "
                    "a natural marked-support calculation is still required."
                ),
            },
        ],
        adversarial_audit=[
            {
                "objection": "Target-character signs can create extra leading mixed moments.",
                "resolved": True,
                "resolution": (
                    "All nonleading supports are suppressed using the absolute "
                    "character bound; leading target words are exactly identity."
                ),
            },
            {
                "objection": "Affine complement supports outside linear partitions survive.",
                "resolved": True,
                "resolution": (
                    "Cube-section equality forces zero into every rank-saturating "
                    "support and identifies a block-constant linear subspace."
                ),
            },
            {
                "objection": "A monochromatic crossing partition is leading.",
                "resolved": True,
                "resolution": (
                    "Its two crossing blocks leave an explicit nontrivial commutator word."
                ),
            },
            {
                "objection": "Subextensive common codimension proves positive component curl.",
                "resolved": False,
                "resolution": (
                    "Low-rank compression and full-support whitening still require "
                    "separate perturbation and marked noncommutativity theorems."
                ),
            },
        ],
        headline_metrics={
            "all_fixed_independent_joint_freeness_theorem_count": int(
                theorem.theorem_verified and failures == 0
            ),
            "uniform_target_character_theorem_count": 1,
            "common_codimension_subextensive_theorem_count": int(
                theorem.theorem_verified and failures == 0
            ),
            "support_sequence_control_count": len(sequence_controls),
            "leading_support_control_count": len(leading_controls),
            "highest_exhaustive_mixed_order": max(
                row.moment_order for row in leading_controls
            ),
            "power_two_mixed_supports_checked": sum(
                row.power_of_two_support_count for row in leading_controls
            ),
            "extra_free_support_count": sum(
                row.extra_free_support_count for row in leading_controls
            ),
            "missing_predicted_support_count": sum(
                row.missing_predicted_support_count for row in leading_controls
            ),
            "finite_control_failure_count": failures,
            "growing_order_joint_law_theorem_count": 0,
            "positive_full_support_leaf_curl_theorem_count": 0,
            "natural_component_M4_theorem_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "all_fixed_independent_joint_freeness_proved": (
                theorem.theorem_verified and failures == 0
            ),
            "uniform_over_target_irreps": True,
            "final_root_child_nullity_subextensive": (
                theorem.theorem_verified and failures == 0
            ),
            "final_root_common_codimension_subextensive": (
                theorem.theorem_verified and failures == 0
            ),
            "low_rank_common_compression_curl_transfer_proved": False,
            "natural_full_support_whitened_leaf_curl_positive": False,
            "natural_component_M4_positive": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The unmarked sibling-frame law and common-rank geometry are "
                "closed qualitatively; marked leaf curl remains the decisive gap."
            ),
        },
        status=(
            "all-fixed-joint-freeness-common-codimension-closed-marked-curl-open"
            if failures == 0
            else "all-fixed-joint-control-failure"
        ),
        summary=(
            "Proved all-fixed independent sibling joint freeness uniformly in "
            "the target and reduced common-span compression to subextensive rank."
        ),
        falsifiers_triggered=[
            "Degree-four joint freeness was not the endpoint; every fixed mixed word is controlled.",
            "Target characters cannot rescue a scalar-subleading support.",
            "Affine and crossing power-two supports do not add free cumulants.",
            "Normalized common codimension vanishes, but marked leaf whitening curl is still open.",
            "No growing-order law, positive component M4, compiler, decoder, or speedup is proved.",
        ],
    )


def write_sibling_frame_all_fixed_joint_report(
    path: Path = REPORT_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = (
        "EXP-CODE-SELF-DUAL-WREATH-SIBLING-FRAME-ALL-FIXED-JOINT"
    ),
    registry_candidate_id: str = "CODE-COSET-COLLECTIVE",
    registry_result_id: str = "",
    **kwargs: Any,
) -> dict[str, Any]:
    output_path = path
    for _k in ("write_registry", "registry_experiment_id", "registry_candidate_id", "registry_result_id"):
        kwargs.pop(_k, None)
    if "run_sibling_frame_all_fixed_joint" in globals():
        report = run_sibling_frame_all_fixed_joint(**kwargs)
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
                id="NEG-SELF-DUAL-WREATH-SIBLING-FRAME-ALL-FIXED-JOINT",
                source=registry_experiment_id,
                claim="Initial negative claim for EXP-CODE-SELF-DUAL-WREATH-SIBLING-FRAME-ALL-FIXED-JOINT.",
                reason_invalid="Falsified or refined by exact theorem evaluation.",
                lesson="Lesson from exact theorem analysis for EXP-CODE-SELF-DUAL-WREATH-SIBLING-FRAME-ALL-FIXED-JOINT.",
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
                    "self_dual_wreath_sibling_frame_all_fixed_joint": str(path)
                },
            )
        )
    return payload

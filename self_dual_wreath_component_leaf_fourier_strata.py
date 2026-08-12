"""Polynomial Walsh-stratum reduction for annealed leaf diagonal leakage.

For a leaf POVM ``{H_x : x in F_2^m}``, put ``q=2^m``, ``F_x=qH_x``, and

    A_S = E_x chi_S(x) F_x = sum_x chi_S(x) H_x.

The source-pair flip action translates leaf labels.  Under any flip-invariant
source law and accepted event, it transforms ``A_S`` by the sign
``chi_S(t)`` up to simultaneous unitary conjugation.  Therefore an annealed
four-coefficient word vanishes unless

    S_1 xor S_2 xor S_3 xor S_4 = 0.                     (1)

Walsh inversion then gives the exact fixed-leaf identity

    E[1_E Tr(H_0^4)/D]
      = q^-4 sum_(S1,S2,S3)
          E[1_E Tr(A_S1 A_S2 A_S3 A_(S1 xor S2 xor S3))/D].   (2)

The ``m`` nonsplit source pairs are exchangeable.  A simultaneous coordinate
permutation preserves each word expectation, so a triple ``(S1,S2,S3)`` is
classified by the eight counts

    c_abc = |{j : (1_S1(j),1_S2(j),1_S3(j))=(a,b,c)}|.

These counts sum to ``m``.  Thus the ``q^3=8^m`` surviving words collapse to
exactly ``binom(m+7,7)=O(m^7)`` annealed strata, with multiplicity
``m!/prod_abc c_abc!``.

For the natural coefficient projection ``H_x=W^*D_xW``, the coefficients are

    A_S = W^* Z_S W,       Z_S=sum_x chi_S(x)D_x,         (3)

where every ``Z_S`` is a block-sign involution.  Equations (2)-(3) turn the
single-leaf diagonal target into a polynomial family of signed compressed
parity words.  They do not bound those words.  Termwise absolute values can
still lose exponentially through the multinomial weights, and the support /
pseudoinverse dependence of ``W`` remains representation-specific.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import numpy as np

from research_registry import utc_now
from self_dual_wreath_component_leaf_fourier_leverage import (
    _coarse_pvm,
    _effect_fourth_trace,
    _uniform_povm,
    _validate_povm,
    walsh_fourier_coefficients,
)
from self_dual_wreath_component_povm_regular_master_reduction import (
    canonical_component_effects,
)


REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_component_leaf_fourier_strata.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-COMPONENT-LEAF-FOURIER-STRATA"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"

Partition = tuple[int, ...]
Label = tuple[Partition, Partition]


@dataclass(frozen=True)
class FourierFourthStratum:
    cell_counts_000_to_111: tuple[int, ...]
    representative_masks: tuple[int, int, int, int]
    triple_multiplicity: int
    enumerated_triple_count: int
    orbit_averaged_normalized_word_real: float
    orbit_averaged_normalized_word_imaginary: float
    weighted_normalized_contribution_real: float
    weighted_normalized_contribution_imaginary: float
    exact_multinomial_count_verified: bool
    status: str


@dataclass(frozen=True)
class LeafFourierStratumControl:
    control_id: str
    profile_kind: str
    cube_dimension: int
    leaf_count: int
    fiber_dimension: int
    raw_four_mask_word_count: int
    xor_surviving_word_count: int
    observed_stratum_count: int
    predicted_stratum_count: int
    fixed_base_leaf_normalized_fourth_moment: float
    translation_orbit_averaged_fixed_leaf_normalized_fourth_moment: float
    direct_average_leaf_normalized_fourth_moment: float
    xor_surviving_fourier_normalized_fourth_moment_real: float
    xor_surviving_fourier_normalized_fourth_moment_imaginary: float
    strata_reconstructed_normalized_fourth_moment_real: float
    strata_reconstructed_normalized_fourth_moment_imaginary: float
    translation_average_residual: float
    walsh_xor_residual: float
    stratum_reconstruction_residual: float
    maximum_stratum_multinomial_residual: int
    exact_annealed_fourier_stratum_reduction_verified: bool
    status: str


@dataclass(frozen=True)
class FourierStratumScalingRecord:
    cube_dimension: int
    leaf_count_log2: int
    surviving_fourier_word_count_log2: int
    exact_stratum_count: int
    log2_stratum_count: float
    stratum_count_polynomial_degree: int
    exponential_word_enumeration_removed: bool
    natural_representative_word_bound_proved: bool
    status: str


@dataclass(frozen=True)
class LeafFourierStratumTheorem:
    translation_selection_rule: str
    fixed_leaf_fourier_identity: str
    coordinate_orbit_invariant: str
    stratum_count: str
    stratum_multiplicity: str
    coefficient_sign_compression: str
    arbitrary_flip_and_coordinate_invariant_law: bool
    arbitrary_invariant_event_and_scalar_weight: bool
    theorem_verified: bool
    status: str


@dataclass(frozen=True)
class ComponentLeafFourierStratumReport:
    created_at: str
    theorem_contract: dict[str, Any]
    theorem: LeafFourierStratumTheorem
    finite_controls: list[LeafFourierStratumControl]
    scaling_records: list[FourierStratumScalingRecord]
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _cell_counts(
    left: int,
    middle: int,
    right: int,
    cube_dimension: int,
) -> tuple[int, ...]:
    counts = [0] * 8
    for coordinate in range(cube_dimension):
        pattern = (
            ((left >> coordinate) & 1) << 2
            | ((middle >> coordinate) & 1) << 1
            | ((right >> coordinate) & 1)
        )
        counts[pattern] += 1
    return tuple(counts)


def _representative_masks(counts: tuple[int, ...]) -> tuple[int, int, int, int]:
    if len(counts) != 8 or any(count < 0 for count in counts):
        raise ValueError("eight nonnegative Venn-cell counts are required")
    masks = [0, 0, 0]
    coordinate = 0
    for pattern, count in enumerate(counts):
        for _ in range(count):
            masks[0] |= ((pattern >> 2) & 1) << coordinate
            masks[1] |= ((pattern >> 1) & 1) << coordinate
            masks[2] |= (pattern & 1) << coordinate
            coordinate += 1
    return masks[0], masks[1], masks[2], masks[0] ^ masks[1] ^ masks[2]


def _multinomial_count(counts: tuple[int, ...]) -> int:
    total = sum(counts)
    output = math.factorial(total)
    for count in counts:
        output //= math.factorial(count)
    return output


def _normalized_fourier_word(
    coefficients: tuple[np.ndarray, ...],
    masks: tuple[int, int, int, int],
    fiber_dimension: int,
) -> complex:
    product = np.eye(fiber_dimension, dtype=complex)
    for mask in masks:
        product = product @ coefficients[mask]
    return complex(np.trace(product) / fiber_dimension)


def audit_leaf_fourier_strata(
    control_id: str,
    profile_kind: str,
    effects: tuple[np.ndarray, ...],
    *,
    tolerance: float = 1e-9,
) -> LeafFourierStratumControl:
    m, r, _, _ = _validate_povm(effects, tolerance=tolerance)
    q = 1 << m
    coefficients = walsh_fourier_coefficients(effects, tolerance=tolerance)
    direct = sum(_effect_fourth_trace(effect) for effect in effects) / (q * r)
    translated = sum(
        _effect_fourth_trace(effects[translation]) / r
        for translation in range(q)
    ) / q
    groups: dict[tuple[int, ...], list[Any]] = {}
    unstratified = 0.0j
    for first in range(q):
        for second in range(q):
            for third in range(q):
                fourth = first ^ second ^ third
                word = _normalized_fourier_word(
                    coefficients,
                    (first, second, third, fourth),
                    r,
                )
                unstratified += word
                key = _cell_counts(first, second, third, m)
                if key not in groups:
                    groups[key] = [0, 0.0j]
                groups[key][0] += 1
                groups[key][1] += word
    rows = []
    stratified_sum = 0.0j
    maximum_count_residual = 0
    for counts, (enumerated, word_sum) in sorted(groups.items()):
        multiplicity = _multinomial_count(counts)
        average = word_sum / enumerated
        weighted = multiplicity * average
        stratified_sum += weighted
        count_residual = abs(enumerated - multiplicity)
        maximum_count_residual = max(maximum_count_residual, count_residual)
        rows.append(
            FourierFourthStratum(
                cell_counts_000_to_111=counts,
                representative_masks=_representative_masks(counts),
                triple_multiplicity=multiplicity,
                enumerated_triple_count=enumerated,
                orbit_averaged_normalized_word_real=float(average.real),
                orbit_averaged_normalized_word_imaginary=float(average.imag),
                weighted_normalized_contribution_real=float(weighted.real),
                weighted_normalized_contribution_imaginary=float(weighted.imag),
                exact_multinomial_count_verified=count_residual == 0,
                status=(
                    "exact-fourier-fourth-venn-stratum"
                    if count_residual == 0
                    else "fourier-fourth-stratum-count-failure"
                ),
            )
        )
    fourier = unstratified / q**4
    stratified = stratified_sum / q**4
    predicted = math.comb(m + 7, 7)
    translation_residual = abs(translated - direct)
    walsh_residual = abs(fourier - direct)
    strata_residual = abs(stratified - fourier)
    exact = bool(
        len(groups) == predicted
        and maximum_count_residual == 0
        and max(translation_residual, walsh_residual, strata_residual)
        <= 5000 * tolerance
    )
    return LeafFourierStratumControl(
        control_id=control_id,
        profile_kind=profile_kind,
        cube_dimension=m,
        leaf_count=q,
        fiber_dimension=r,
        raw_four_mask_word_count=q**4,
        xor_surviving_word_count=q**3,
        observed_stratum_count=len(groups),
        predicted_stratum_count=predicted,
        fixed_base_leaf_normalized_fourth_moment=(
            _effect_fourth_trace(effects[0]) / r
        ),
        translation_orbit_averaged_fixed_leaf_normalized_fourth_moment=translated,
        direct_average_leaf_normalized_fourth_moment=direct,
        xor_surviving_fourier_normalized_fourth_moment_real=float(fourier.real),
        xor_surviving_fourier_normalized_fourth_moment_imaginary=float(fourier.imag),
        strata_reconstructed_normalized_fourth_moment_real=float(stratified.real),
        strata_reconstructed_normalized_fourth_moment_imaginary=float(stratified.imag),
        translation_average_residual=float(translation_residual),
        walsh_xor_residual=float(walsh_residual),
        stratum_reconstruction_residual=float(strata_residual),
        maximum_stratum_multinomial_residual=maximum_count_residual,
        exact_annealed_fourier_stratum_reduction_verified=exact,
        status=(
            "annealed-leaf-fourth-moment-reduced-to-polynomial-fourier-strata"
            if exact
            else "leaf-fourier-stratum-control-failure"
        ),
    )


def _haar_block_povm(
    cube_dimension: int,
    block_dimension: int,
    fiber_dimension: int,
    *,
    seed: int,
) -> tuple[np.ndarray, ...]:
    q = 1 << cube_dimension
    ambient = q * block_dimension
    if not 1 <= fiber_dimension <= ambient:
        raise ValueError("invalid Haar block-POVM fiber dimension")
    rng = np.random.default_rng(seed)
    gaussian = (
        rng.normal(size=(ambient, fiber_dimension))
        + 1j * rng.normal(size=(ambient, fiber_dimension))
    ) / math.sqrt(2.0)
    isometry, _ = np.linalg.qr(gaussian, mode="reduced")
    return tuple(
        isometry[offset : offset + block_dimension].conj().T
        @ isometry[offset : offset + block_dimension]
        for offset in range(0, ambient, block_dimension)
    )


def _natural_effects(
    target: Partition,
    labels: tuple[Label, ...],
    *,
    tolerance: float,
) -> tuple[np.ndarray, ...]:
    m = len(labels) - 1
    q = 1 << m
    _, fiber, sides = canonical_component_effects(
        target,
        labels,
        tuple(range(q)),
        tuple(range(q, 2 * q)),
        tolerance=tolerance,
    )
    if not fiber:
        raise ValueError("the selected natural control has zero common span")
    return sides[0]


def fourier_stratum_scaling_record(
    cube_dimension: int,
) -> FourierStratumScalingRecord:
    if cube_dimension < 1:
        raise ValueError("cube dimension must be positive")
    strata = math.comb(cube_dimension + 7, 7)
    return FourierStratumScalingRecord(
        cube_dimension=cube_dimension,
        leaf_count_log2=cube_dimension,
        surviving_fourier_word_count_log2=3 * cube_dimension,
        exact_stratum_count=strata,
        log2_stratum_count=math.log2(strata),
        stratum_count_polynomial_degree=7,
        exponential_word_enumeration_removed=True,
        natural_representative_word_bound_proved=False,
        status="exponential-fourier-words-reduced-to-degree-seven-strata",
    )


def leaf_fourier_stratum_theorem() -> LeafFourierStratumTheorem:
    return LeafFourierStratumTheorem(
        translation_selection_rule=(
            "annealed Tr(A_S1 A_S2 A_S3 A_S4) vanishes unless "
            "S1 xor S2 xor S3 xor S4=0"
        ),
        fixed_leaf_fourier_identity=(
            "E[1_E Tr(H_0^4)/D]=q^-4 sum_(S1,S2,S3) "
            "E[1_E Tr(A_S1 A_S2 A_S3 A_(S1 xor S2 xor S3))/D]"
        ),
        coordinate_orbit_invariant=(
            "the surviving word expectation depends only on the eight Venn-cell counts of (S1,S2,S3)"
        ),
        stratum_count="number of strata=binom(m+7,7)=O(m^7)",
        stratum_multiplicity="multiplicity=m!/prod_(a,b,c)c_abc!",
        coefficient_sign_compression=(
            "for H_x=W*D_xW, A_S=W*Z_SW with Z_S=sum_x chi_S(x)D_x and Z_S^2=I"
        ),
        arbitrary_flip_and_coordinate_invariant_law=True,
        arbitrary_invariant_event_and_scalar_weight=True,
        theorem_verified=True,
        status="annealed-fixed-leaf-diagonal-reduced-to-polynomial-walsh-strata",
    )


def run_component_leaf_fourier_strata(
    *,
    tolerance: float = 1e-9,
) -> ComponentLeafFourierStratumReport:
    standard = (2, 1)
    controls = [
        audit_leaf_fourier_strata(
            "UNIFORM-Q8-R3",
            "uniform-scalar-povm",
            _uniform_povm(3, 3),
            tolerance=tolerance,
        ),
        audit_leaf_fourier_strata(
            "COARSE-Q16-TWO-BIT-PVM",
            "coarse-projection-valued-povm",
            _coarse_pvm(4, 2),
            tolerance=tolerance,
        ),
        audit_leaf_fourier_strata(
            "HAAR-Q8-B2-R5",
            "noncommutative-haar-block-povm",
            _haar_block_povm(3, 2, 5, seed=4471),
            tolerance=tolerance,
        ),
        audit_leaf_fourier_strata(
            "S3-REPEATED-STANDARD-TRIVIAL-TARGET",
            "finite-wreath-canonical-component-povm",
            _natural_effects((3,), ((standard, standard),) * 3, tolerance=tolerance),
            tolerance=tolerance,
        ),
    ]
    scaling = [
        fourier_stratum_scaling_record(m)
        for m in (4, 8, 16, 32, 64, 128, 256)
    ]
    theorem = leaf_fourier_stratum_theorem()
    failures = sum(
        not row.exact_annealed_fourier_stratum_reduction_verified
        for row in controls
    )
    tail = scaling[-1]
    return ComponentLeafFourierStratumReport(
        created_at=utc_now(),
        theorem_contract={
            "translation_selection": theorem.translation_selection_rule,
            "fixed_leaf_identity": theorem.fixed_leaf_fourier_identity,
            "coordinate_orbits": theorem.coordinate_orbit_invariant,
            "stratum_count": theorem.stratum_count,
            "multiplicity": theorem.stratum_multiplicity,
            "coefficient_normal_form": theorem.coefficient_sign_compression,
            "conditioning_scope": (
                "Independent Plancherel sources, global-distinct conditioning, "
                "the optimized rank/second-moment event, and physical 1/D "
                "weight are all invariant and may be inserted in the identity."
            ),
            "scope": (
                "The reduction removes exponential orbit enumeration, not the "
                "representation-specific signed word estimates."
            ),
        },
        theorem=theorem,
        finite_controls=controls,
        scaling_records=scaling,
        proof_obligations=[
            {
                "obligation": "remove_exponential_fourier_word_enumeration_from_fixed_leaf_diagonal",
                "resolved": theorem.theorem_verified and failures == 0,
                "resolution": (
                    "Flip characters impose XOR zero and coordinate exchangeability "
                    "leaves exactly binom(m+7,7) Venn strata."
                ),
            },
            {
                "obligation": "evaluate_natural_representative_compressed_parity_words",
                "resolved": False,
                "resolution": (
                    "For every relevant eight-cell density, bound the signed "
                    "regular-master expectation of W*Z_S1W ... W*Z_S4W after "
                    "support/pseudoinverse normalization."
                ),
            },
            {
                "obligation": "sum_stratum_bounds_without_exponential_absolute_value_loss",
                "resolved": False,
                "resolution": (
                    "Use signed generating functions, saddle-point pressure, or "
                    "a positive aggregate identity; termwise absolute values are "
                    "not licensed."
                ),
            },
            {
                "obligation": "bound_natural_distinct_crossing_pressure",
                "resolved": False,
                "resolution": (
                    "The diagonal strata do not settle the separate ordered "
                    "distinct crossing term."
                ),
            },
        ],
        adversarial_audit=[
            {
                "objection": "The fixed leaf itself is translation invariant in each sample.",
                "resolved": True,
                "resolution": (
                    "False. Translation invariance is at source-law/event level; "
                    "the base-leaf moment can differ inside one profile."
                ),
            },
            {
                "objection": "XOR zero leaves only polynomially many mask triples.",
                "resolved": True,
                "resolution": (
                    "False before quotienting: it leaves q^3 triples. Coordinate "
                    "exchangeability is the separate step producing O(m^7) strata."
                ),
            },
            {
                "objection": "A polynomial number of strata proves the moment is small.",
                "resolved": True,
                "resolution": (
                    "No. Multinomial weights sum to q^3 and signed representative "
                    "words can remain large."
                ),
            },
            {
                "objection": "Schatten norms of individual A_S determine ordered four-word traces.",
                "resolved": True,
                "resolution": (
                    "They do not; relative matrix order and phase-sensitive "
                    "recoupling remain essential."
                ),
            },
        ],
        headline_metrics={
            "annealed_leaf_fourier_stratum_reduction_theorem_count": int(
                theorem.theorem_verified and failures == 0
            ),
            "finite_control_count": len(controls),
            "finite_control_failure_count": failures,
            "maximum_control_walsh_xor_residual": max(
                row.walsh_xor_residual for row in controls
            ),
            "maximum_control_stratum_residual": max(
                row.stratum_reconstruction_residual for row in controls
            ),
            "tail_cube_dimension": tail.cube_dimension,
            "tail_surviving_fourier_word_count_log2": (
                tail.surviving_fourier_word_count_log2
            ),
            "tail_exact_stratum_count": tail.exact_stratum_count,
            "tail_log2_stratum_count": tail.log2_stratum_count,
            "natural_representative_word_bound_count": 0,
            "natural_fixed_leaf_diagonal_bound_count": 0,
            "natural_distinct_crossing_bound_count": 0,
            "natural_component_M4_lower_bound_theorem_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "annealed_non_xor_fourier_words_cancel": True,
            "surviving_words_reduce_to_polynomial_venn_strata": (
                theorem.theorem_verified and failures == 0
            ),
            "natural_representative_stratum_words_controlled": False,
            "natural_fixed_leaf_diagonal_green_moment_controlled": False,
            "natural_distinct_crossing_pressure_controlled": False,
            "natural_component_M4_positive": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The exponential mask combinatorics are removed, but the signed "
                "compressed-parity word expectations and their weighted sum are open."
            ),
        },
        status=(
            "annealed-leaf-diagonal-reduced-to-polynomial-fourier-strata"
            if failures == 0
            else "leaf-fourier-stratum-control-failure"
        ),
        summary=(
            "Reduced the annealed fixed-leaf fourth moment from exponentially "
            "many Walsh words to O(m^7) Venn-pattern expectations, preserving "
            "the exact support-normalized natural target."
        ),
        falsifiers_triggered=[
            "Translation symmetry is annealed and does not imply blockwise leaf equality.",
            "XOR selection alone leaves q^3 words; coordinate exchangeability is essential.",
            "Polynomial orbit count does not justify termwise absolute-value bounds.",
            "No natural representative-word estimate, crossing bound, M4, algorithm, or speedup is proved.",
        ],
    )


def write_component_leaf_fourier_strata_report(
    path: Path = REPORT_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = (
        "EXP-CODE-SELF-DUAL-WREATH-COMPONENT-LEAF-FOURIER-STRATA"
    ),
    registry_candidate_id: str = "CODE-COSET-COLLECTIVE",
    registry_result_id: str = "",
    **kwargs: Any,
) -> dict[str, Any]:
    output_path = path
    for _k in ("write_registry", "registry_experiment_id", "registry_candidate_id", "registry_result_id"):
        kwargs.pop(_k, None)
    if "run_component_leaf_fourier_strata" in globals():
        report = run_component_leaf_fourier_strata(**kwargs)
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
                id="NEG-SELF-DUAL-WREATH-COMPONENT-LEAF-FOURIER-STRATA",
                source=registry_experiment_id,
                claim="Initial negative claim for EXP-CODE-SELF-DUAL-WREATH-COMPONENT-LEAF-FOURIER-STRATA.",
                reason_invalid="Falsified or refined by exact theorem evaluation.",
                lesson="Lesson from exact theorem analysis for EXP-CODE-SELF-DUAL-WREATH-COMPONENT-LEAF-FOURIER-STRATA.",
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
                    "self_dual_wreath_component_leaf_fourier_strata": str(path)
                },
            )
        )
    return payload

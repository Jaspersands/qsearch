"""Exact sibling-frame moments and the Marchenko--Pastur research boundary.

At one affine sibling split, fix the split bit and write

    A = sum_(e: e_j=0) E_e,    B = sum_(e: e_j=1) E_e.

Let ``G`` be a finite group of order ``g``, let ``K`` be the source-pair
count, ``N=2^K``, and put ``alpha=N/(2g)``.  Average the ``2K`` source irreps
independently from Plancherel measure and normalize traces by the full target
carrier dimension ``D``.  Character column orthogonality gives exactly

    E Tr(A)/D   = alpha,
    E Tr(A^2)/D = alpha(1-g^-1) + alpha^2,
    E Tr(AB)/D  = alpha^2,                                  (1)

and a three-word identity gives

    E Tr(A^3)/D
      = alpha(1-g^-1)(1-2g^-1)
        + 3 alpha^2(1-g^-1) + alpha^3.                      (2)

For (2), the source selected by the split forces ``x y z=1``.  Each remaining
source pair contributes 2, 4, or 8 according as the triple has zero, one, or
three identity entries.  The respective triple counts are
``(g-1)(g-2)``, ``3(g-1)``, and one.

The fourth moment is also exact.  For ``x_1x_2x_3x_4=1``, a remaining source
pair contributes ``q in {2,4,6,8,16}``.  The crossing two-two split is the
only new group-sensitive stratum: it counts commuting ordered pairs.  Thus
the distribution of ``q`` is determined by ``g``, the conjugacy-class count
``r``, and the number ``i`` of nonidentity involutions.  If ``C_q`` denotes
the counts returned by :func:`fourth_word_stratum_counts`, then

    E Tr(A^4)/D = g^-4 sum_q C_q q^(K-1).                  (3)

For ``S_n``, ``r=p(n)=exp(O(sqrt n))`` and ``i/g=o(1)``.  The crossing and
six-valued corrections vanish, so (3) tends to

    alpha + 6 alpha^2 + 6 alpha^3 + alpha^4,

the fourth Marchenko--Pastur moment.

As ``g`` grows, (1)-(2) converge to

    alpha,  alpha+alpha^2,  alpha+3alpha^2+alpha^3,

the first three Marchenko--Pastur moments.  This identifies a high-upside
free-probability route to child-frame spectral bounds.  It also kills the
wrong route: the best scalar mean-square residual is

    E ||A-alpha I||_F^2 / D = alpha(1-g^-1),                (4)

and ``E||A-B||_F^2/D=2alpha(1-g^-1)``.  These remain constant at the
information threshold.  Natural sibling frames are not Frobenius-small
perturbations of equal scalar operators.

The theorem is under independent Plancherel sampling.  Global-distinct
conditioning is not transferred here: the moment observable has a large
worst-case norm, so total-variation convergence alone is inadequate.  Nor do
three fixed moments control spectral edges or pseudoinverses.  The actual
research gate is a growing-moment/injective-Plancherel theorem strong enough
to bound the nonzero child-frame spectrum and then the compressed
pseudoinverse metrics.
"""

from __future__ import annotations

import itertools
import json
import math
from dataclasses import asdict, dataclass
from fractions import Fraction
from pathlib import Path
from typing import Any

import numpy as np

from representation_obstruction import hook_length_dimension, integer_partitions
from research_registry import utc_now
from self_dual_wreath_collision_free_frame_probe import Label
from self_dual_wreath_orientation_fourier_reduction import (
    orientation_invariant_projector,
)


REPORT_PATH = Path(
    "research/representation/self_dual_wreath_sibling_frame_mp_moments.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-SIBLING-FRAME-MP-MOMENTS"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"

Partition = tuple[int, ...]


@dataclass(frozen=True)
class SiblingMomentFormula:
    group_order: int
    copy_count: int
    orientation_count: int
    child_aspect_ratio: str
    expected_normalized_trace: str
    expected_normalized_second_moment: str
    expected_normalized_third_moment: str
    expected_normalized_fourth_moment: str
    expected_normalized_mixed_second_moment: str
    expected_normalized_sibling_difference_energy: str
    expected_best_scalar_residual_energy: str
    marchenko_pastur_first_moment: str
    marchenko_pastur_second_moment: str
    marchenko_pastur_third_moment: str
    marchenko_pastur_fourth_moment: str
    status: str


@dataclass(frozen=True)
class DirectSiblingMomentControl:
    n: int
    copy_count: int
    target_partition: Partition
    source_tuple_count: int
    maximum_formula_residual: float
    direct_projector_moments_verified: bool
    status: str


@dataclass(frozen=True)
class SiblingFrameScalingRecord:
    n: int
    group_order_decimal: str
    information_threshold_copy_count: int
    child_aspect_ratio: float
    scalar_residual_energy: float
    sibling_difference_energy: float
    sibling_difference_to_parent_second_moment_ratio: float
    second_moment_mp_residual: float
    third_moment_mp_residual: float
    fourth_moment_mp_residual: float
    wishart_edge_lower_heuristic: float
    wishart_edge_upper_heuristic: float
    wishart_condition_number_heuristic: float
    condition_number_endpoint_gap_heuristic: float
    globally_distinct_fixed_moments_proved: bool
    growing_moment_spectral_edge_proved: bool
    natural_pseudoinverse_comparability_proved: bool
    status: str


@dataclass(frozen=True)
class SiblingFrameMpMomentReport:
    created_at: str
    theorem_contract: dict[str, Any]
    exact_formula_controls: list[SiblingMomentFormula]
    direct_projector_controls: list[DirectSiblingMomentControl]
    scaling_records: list[SiblingFrameScalingRecord]
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def fourth_word_stratum_counts(
    group_order: int,
    conjugacy_class_count: int,
    nonidentity_involution_count: int,
) -> dict[int, int]:
    """Count the fourth-word source-pair values ``q`` in equation (3)."""

    g = group_order
    r = conjugacy_class_count
    involutions = nonidentity_involution_count
    if g < 2 or not 1 <= r <= g or not 0 <= involutions < g:
        raise ValueError("invalid finite-group counting data")
    nonidentity_commuting_pairs = g * r - (2 * g - 1)
    exactly_two_pairings = 3 * (g - 1 - involutions)
    exactly_one_pairing = (
        2 * (g - 1) * (g - 1)
        + nonidentity_commuting_pairs
        - 6 * (g - 1)
        + 3 * involutions
    )
    no_identity_total = g**3 - 4 * g * g + 6 * g - 3
    no_pairing = (
        no_identity_total
        - exactly_one_pairing
        - exactly_two_pairings
        - involutions
    )
    counts = {
        2: no_pairing,
        4: exactly_one_pairing + 4 * (g - 1) * (g - 2),
        6: exactly_two_pairings,
        8: involutions + 6 * (g - 1),
        16: 1,
    }
    if min(counts.values()) < 0 or sum(counts.values()) != g**3:
        raise ArithmeticError("fourth-word strata do not partition group triples")
    return counts


def symmetric_group_nonidentity_involution_count(n: int) -> int:
    if n < 1:
        raise ValueError("n must be positive")
    factorial = math.factorial(n)
    return sum(
        factorial
        // (
            (1 << transpositions)
            * math.factorial(transpositions)
            * math.factorial(n - 2 * transpositions)
        )
        for transpositions in range(1, n // 2 + 1)
    )


def sibling_moment_formula(
    group_order: int,
    copy_count: int,
    *,
    conjugacy_class_count: int | None = None,
    nonidentity_involution_count: int | None = None,
) -> SiblingMomentFormula:
    if group_order < 2 or copy_count < 1:
        raise ValueError("a nontrivial group and positive copy count are required")
    orientations = 1 << copy_count
    alpha = Fraction(orientations, 2 * group_order)
    inverse_order = Fraction(1, group_order)
    first = alpha
    second = alpha * (1 - inverse_order) + alpha * alpha
    mixed = alpha * alpha
    third = (
        alpha * (1 - inverse_order) * (1 - 2 * inverse_order)
        + 3 * alpha * alpha * (1 - inverse_order)
        + alpha**3
    )
    if (conjugacy_class_count is None) != (
        nonidentity_involution_count is None
    ):
        raise ValueError("fourth-moment group data must be supplied together")
    if conjugacy_class_count is None:
        fourth = Fraction()
        mp_fourth = Fraction()
    else:
        strata = fourth_word_stratum_counts(
            group_order,
            conjugacy_class_count,
            nonidentity_involution_count,
        )
        fourth = Fraction(
            sum(
                count * value ** (copy_count - 1)
                for value, count in strata.items()
            ),
            group_order**4,
        )
        mp_fourth = (
            alpha
            + 6 * alpha * alpha
            + 6 * alpha**3
            + alpha**4
        )
    difference = 2 * (second - mixed)
    scalar_residual = second - 2 * alpha * first + alpha * alpha
    mp_first = alpha
    mp_second = alpha + alpha * alpha
    mp_third = alpha + 3 * alpha * alpha + alpha**3
    return SiblingMomentFormula(
        group_order=group_order,
        copy_count=copy_count,
        orientation_count=orientations,
        child_aspect_ratio=str(alpha),
        expected_normalized_trace=str(first),
        expected_normalized_second_moment=str(second),
        expected_normalized_third_moment=str(third),
        expected_normalized_fourth_moment=str(fourth),
        expected_normalized_mixed_second_moment=str(mixed),
        expected_normalized_sibling_difference_energy=str(difference),
        expected_best_scalar_residual_energy=str(scalar_residual),
        marchenko_pastur_first_moment=str(mp_first),
        marchenko_pastur_second_moment=str(mp_second),
        marchenko_pastur_third_moment=str(mp_third),
        marchenko_pastur_fourth_moment=str(mp_fourth),
        status="exact-independent-plancherel-sibling-moments",
    )


def _formula_values(
    n: int,
    copy_count: int,
) -> tuple[float, ...]:
    group_order = math.factorial(n)
    row = sibling_moment_formula(
        group_order,
        copy_count,
        conjugacy_class_count=len(integer_partitions(n)),
        nonidentity_involution_count=(
            symmetric_group_nonidentity_involution_count(n)
        ),
    )
    return tuple(
        float(Fraction(value))
        for value in (
            row.expected_normalized_trace,
            row.expected_normalized_second_moment,
            row.expected_normalized_third_moment,
            row.expected_normalized_fourth_moment,
            row.expected_normalized_mixed_second_moment,
        )
    )


def audit_direct_sibling_moments(
    n: int,
    copy_count: int,
    target: Partition,
) -> DirectSiblingMomentControl:
    """Enumerate a small Plancherel source ensemble using explicit projectors."""

    if sum(target) != n:
        raise ValueError("target partition has the wrong size")
    partitions = tuple(integer_partitions(n))
    order = math.factorial(n)
    dimensions = {
        partition: hook_length_dimension(partition)
        for partition in partitions
    }
    weights = {
        partition: dimensions[partition] ** 2 / order
        for partition in partitions
    }
    direct = np.zeros(5)
    tuple_count = 0
    split_bit = 0
    left_masks = tuple(
        mask
        for mask in range(1 << copy_count)
        if not mask & (1 << split_bit)
    )
    right_masks = tuple(
        mask
        for mask in range(1 << copy_count)
        if mask & (1 << split_bit)
    )
    for sources in itertools.product(partitions, repeat=2 * copy_count):
        labels: tuple[Label, ...] = tuple(
            (sources[2 * index], sources[2 * index + 1])
            for index in range(copy_count)
        )
        probability = math.prod(weights[source] for source in sources)
        carrier_dimension = dimensions[target] * math.prod(
            dimensions[source] for source in sources
        )
        projectors = tuple(
            orientation_invariant_projector(target, labels, mask)
            for mask in range(1 << copy_count)
        )
        zero = np.zeros_like(projectors[0])
        left = sum((projectors[mask] for mask in left_masks), zero.copy())
        right = sum((projectors[mask] for mask in right_masks), zero.copy())
        direct += probability * np.asarray(
            (
                np.trace(left).real,
                np.trace(left @ left).real,
                np.trace(left @ left @ left).real,
                np.trace(left @ left @ left @ left).real,
                np.trace(left @ right).real,
            )
        ) / carrier_dimension
        tuple_count += 1
    predicted = np.asarray(_formula_values(n, copy_count))
    residual = float(np.max(np.abs(direct - predicted)))
    verified = residual <= 1e-10
    return DirectSiblingMomentControl(
        n=n,
        copy_count=copy_count,
        target_partition=target,
        source_tuple_count=tuple_count,
        maximum_formula_residual=residual,
        direct_projector_moments_verified=verified,
        status=(
            "direct-projector-sibling-moments-verified"
            if verified
            else "direct-projector-sibling-moment-mismatch"
        ),
    )


def sibling_frame_scaling_record(n: int) -> SiblingFrameScalingRecord:
    if n < 3:
        raise ValueError("n must be at least three")
    order = math.factorial(n)
    copy_count = math.ceil(math.lgamma(n + 1) / math.log(2))
    formula = sibling_moment_formula(
        order,
        copy_count,
        conjugacy_class_count=len(integer_partitions(n)),
        nonidentity_involution_count=(
            symmetric_group_nonidentity_involution_count(n)
        ),
    )
    alpha = float(Fraction(formula.child_aspect_ratio))
    scalar = float(Fraction(formula.expected_best_scalar_residual_energy))
    difference = float(
        Fraction(formula.expected_normalized_sibling_difference_energy)
    )
    second_exact = Fraction(formula.expected_normalized_second_moment)
    mixed_exact = Fraction(formula.expected_normalized_mixed_second_moment)
    mp_second_exact = Fraction(formula.marchenko_pastur_second_moment)
    third_exact = Fraction(formula.expected_normalized_third_moment)
    mp_third_exact = Fraction(formula.marchenko_pastur_third_moment)
    fourth_exact = Fraction(formula.expected_normalized_fourth_moment)
    mp_fourth_exact = Fraction(formula.marchenko_pastur_fourth_moment)
    second = float(second_exact)
    mixed = float(mixed_exact)

    # Heuristic only: these are the spectral edges of a Gaussian/Wishart
    # frame with the matching aspect. No natural-frame edge theorem is claimed.
    root = math.sqrt(alpha)
    edge_lower = (1 - root) ** 2
    edge_upper = (1 + root) ** 2
    condition = edge_upper / edge_lower
    gap = edge_lower / (edge_lower + edge_upper)
    return SiblingFrameScalingRecord(
        n=n,
        group_order_decimal=str(order),
        information_threshold_copy_count=copy_count,
        child_aspect_ratio=alpha,
        scalar_residual_energy=scalar,
        sibling_difference_energy=difference,
        sibling_difference_to_parent_second_moment_ratio=(
            difference / (2 * second + 2 * mixed)
        ),
        second_moment_mp_residual=float(abs(second_exact - mp_second_exact)),
        third_moment_mp_residual=float(abs(third_exact - mp_third_exact)),
        fourth_moment_mp_residual=float(abs(fourth_exact - mp_fourth_exact)),
        wishart_edge_lower_heuristic=edge_lower,
        wishart_edge_upper_heuristic=edge_upper,
        wishart_condition_number_heuristic=condition,
        condition_number_endpoint_gap_heuristic=gap,
        globally_distinct_fixed_moments_proved=False,
        growing_moment_spectral_edge_proved=False,
        natural_pseudoinverse_comparability_proved=False,
        status="mp-moment-signal-injective-growing-moment-proof-open",
    )


def run_sibling_frame_mp_moments() -> SiblingFrameMpMomentReport:
    formula_controls = [
        sibling_moment_formula(
            math.factorial(n),
            copy_count,
            conjugacy_class_count=len(integer_partitions(n)),
            nonidentity_involution_count=(
                symmetric_group_nonidentity_involution_count(n)
            ),
        )
        for n, copy_count in ((3, 2), (4, 3), (5, 4), (6, 5))
    ]
    direct_controls = [
        audit_direct_sibling_moments(3, 2, target)
        for target in integer_partitions(3)
    ]
    scaling = [
        sibling_frame_scaling_record(n)
        for n in (8, 12, 16, 20, 24, 28, 32, 36, 40, 44, 48)
    ]
    failures = sum(
        not row.direct_projector_moments_verified for row in direct_controls
    )
    verified = failures == 0
    tail = scaling[-1]
    metrics: dict[str, int | float] = {
        "exact_independent_plancherel_sibling_moment_theorem_count": 1,
        "highest_exact_moment_order": 4,
        "formula_control_count": len(formula_controls),
        "direct_projector_control_count": len(direct_controls),
        "direct_projector_control_failure_count": failures,
        "scaling_row_count": len(scaling),
        "tail_n": tail.n,
        "tail_child_aspect_ratio": tail.child_aspect_ratio,
        "tail_scalar_residual_energy": tail.scalar_residual_energy,
        "tail_sibling_difference_energy": tail.sibling_difference_energy,
        "tail_second_moment_mp_residual": tail.second_moment_mp_residual,
        "tail_third_moment_mp_residual": tail.third_moment_mp_residual,
        "tail_fourth_moment_mp_residual": tail.fourth_moment_mp_residual,
        "tail_wishart_endpoint_gap_heuristic": (
            tail.condition_number_endpoint_gap_heuristic
        ),
        "globally_distinct_fixed_moment_theorem_count": 0,
        "growing_moment_spectral_edge_theorem_count": 0,
        "natural_pseudoinverse_comparability_theorem_count": 0,
        "new_quantum_algorithm_count": 0,
    }
    return SiblingFrameMpMomentReport(
        created_at=utc_now(),
        theorem_contract={
            "first_second_moments": (
                "Independent Plancherel character orthogonality gives "
                "E Tr A/D=alpha, E Tr A^2/D=alpha(1-1/G)+alpha^2, "
                "and E Tr AB/D=alpha^2."
            ),
            "third_moment": (
                "Classifying xyz=1 triples by zero, one, or three identity "
                "entries gives the exact cubic formula."
            ),
            "fourth_moment": (
                "The q in {2,4,6,8,16} word strata are counted exactly from "
                "group order, commuting-pair count G times number of classes, "
                "and nonidentity involution count."
            ),
            "mp_limit": (
                "The first four moments converge to the Marchenko--Pastur "
                "polynomials at child aspect alpha=2^(K-1)/G."
            ),
            "scalarization_no_go": (
                "E||A-alpha I||_F^2/D=alpha(1-1/G), so scalar or equal-frame "
                "Frobenius perturbation does not vanish."
            ),
            "scope": (
                "The source law is independent Plancherel. Fixed moments do "
                "not transfer automatically to global distinctness and do not "
                "control spectral edges or pseudoinverses."
            ),
        },
        exact_formula_controls=formula_controls,
        direct_projector_controls=direct_controls,
        scaling_records=scaling,
        proof_obligations=[
            {
                "obligation": "derive_natural_sibling_frame_low_moments",
                "resolved": verified,
                "resolution": (
                    "Moments through order four are exact and match every "
                    "explicit S3 Plancherel projector control."
                ),
            },
            {
                "obligation": "transfer_sibling_moments_to_global_distinct_sources",
                "resolved": False,
                "resolution": (
                    "The normalized trace words have large worst-case bounds; "
                    "the injective Plancherel kernel must be evaluated or bounded "
                    "without a generic total-variation argument."
                ),
            },
            {
                "obligation": "prove_growing_moment_mp_law_and_spectral_edges",
                "resolved": False,
                "resolution": (
                    "Three fixed moments neither imply Marchenko--Pastur "
                    "universality nor bound the smallest nonzero child-frame eigenvalue."
                ),
            },
            {
                "obligation": "deduce_natural_pseudoinverse_frame_comparability",
                "resolved": False,
                "resolution": (
                    "This requires globally-distinct spectral-edge control and "
                    "compression to the random common child span."
                ),
            },
        ],
        adversarial_audit=[
            {
                "objection": "Many orientation leaves make each child frame close to a scalar operator.",
                "resolved": True,
                "resolution": (
                    "The best scalar Frobenius residual remains "
                    "alpha(1-1/G)=Theta(1)."
                ),
            },
            {
                "objection": "Sibling exchangeability makes A and B norm-close.",
                "resolved": True,
                "resolution": (
                    "Exchangeability gives equal laws, while the expected "
                    "squared Frobenius difference is 2alpha(1-1/G)=Theta(1)."
                ),
            },
            {
                "objection": "Three Marchenko--Pastur moments prove a Wishart spectral edge.",
                "resolved": False,
                "resolution": (
                    "A thin extreme-eigenvalue sector is invisible to any fixed "
                    "number of normalized trace moments."
                ),
            },
        ],
        headline_metrics=metrics,
        claim_gate={
            "independent_plancherel_moments_through_four_proved": verified,
            "child_frames_frobenius_close_to_equal_scalars": False,
            "marchenko_pastur_fixed_moment_signal_present": True,
            "globally_distinct_fixed_moments_proved": False,
            "marchenko_pastur_law_proved": False,
            "natural_child_frame_spectral_edges_proved": False,
            "natural_pseudoinverse_frame_comparability_proved": False,
            "polynomial_hierarchical_polar_sampler_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "Natural independent-source child frames have a Wishart-like "
                "low-moment signature, not scalar concentration. Injective "
                "growing-moment and spectral-edge theorems remain missing."
            ),
        },
        status=(
            "exact-mp-low-moment-signal-injective-spectral-edge-open"
            if verified
            else "sibling-frame-moment-control-failure"
        ),
        summary=(
            "Derived exact sibling-frame moments through order four, falsified "
            "scalar-frame concentration, and identified an injective "
            "Marchenko--Pastur spectral-edge program for pseudoinverse balance."
        ),
        falsifiers_triggered=[
            "Child frames do not become equal scalar operators in normalized Frobenius energy.",
            "Sibling exchangeability does not imply samplewise frame closeness.",
            "Fixed low moments cannot certify the pseudoinverse spectral edge.",
        ],
    )


def write_sibling_frame_mp_moment_report(
    path: Path = REPORT_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = (
        "EXP-CODE-SELF-DUAL-WREATH-SIBLING-FRAME-MP-MOMENTS"
    ),
    registry_candidate_id: str = "CODE-COSET-COLLECTIVE",
    registry_result_id: str = "",
) -> dict[str, Any]:
    payload = asdict(run_sibling_frame_mp_moments())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n")

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
                id="NEG-SELF-DUAL-WREATH-SIBLING-FRAME-MP-MOMENTS",
                source=registry_experiment_id,
                claim=(
                    "Initial negative claim for EXP-CODE-SELF-DUAL-WREATH-SIBLING-FRAME-MP-MOMENTS."
                ),
                reason_invalid=(
                    "Falsified or refined by exact theorem evaluation."
                ),
                lesson=(
                    "Lesson from exact theorem analysis for EXP-CODE-SELF-DUAL-WREATH-SIBLING-FRAME-MP-MOMENTS."
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
                    "self_dual_wreath_sibling_frame_mp_moments": str(path)
                },
            )
        )
    return payload


if __name__ == "__main__":
    report = write_sibling_frame_mp_moment_report()
    print(json.dumps(report, indent=2))

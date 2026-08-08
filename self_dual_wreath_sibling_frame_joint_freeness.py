"""Exact mixed sibling moments and the finite-order freeness boundary.

Let ``A`` and ``B`` be the two sibling orientation frames from
``self_dual_wreath_sibling_frame_mp_moments``.  Average the ``2K`` source
irreps independently from Plancherel measure, fix a target irrep ``nu`` of a
finite group ``G``, and normalize traces by the full target carrier dimension.
Write ``g=|G|``, ``N=2^K``, and ``alpha=N/(2g)``.

Expanding a trace word in orientation projectors reduces every unused source
pair to a two-color word count.  Up to cyclic rotation and swapping ``A,B``,
the mixed words through degree four are ``AB``, ``A^2B``, ``A^2B^2``, and
``ABAB``.  The first is ``alpha^2`` and the next three are exactly

  E tr(A^2B) = g^-3 [(g-1)4^(K-1) + 8^(K-1)],             (1)

  E tr(A^2B^2) = g^-4 [
      c4 4^(K-1) + c6 6^(K-1) + c8 8^(K-1) + 16^(K-1)],  (2)

where, for ``i`` nonidentity involutions,

  c4=g^2-4g+3+i, c6=2(g-1-i), c8=2(g-1)+i.

The crossing word has

  E tr(ABAB) = g^-4 [
      s2 2^(K-1) + d4 4^(K-1) + c6 6^(K-1)
      + c8 8^(K-1) + 16^(K-1)],                           (3)

where ``r`` is the conjugacy-class count, ``d=dim(nu)``,

  d4=gr-4g+3+i,    s2=g^2/d^2-gr.

Only (3) sees the target.  Its noncommuting contribution follows from the
classical commutator character identity

  sum_(x,y in G) chi_nu([x,y])/d = g^2/d^2.

For symmetric groups, ``r=p(n)=exp(O(sqrt(n)))`` and ``i/g=o(1)``.  Since
``K=log_2(g)+O(1)``, equations (1)--(3) converge, uniformly in the target
dimension, to

  alpha^2+alpha^3,
  alpha^2+2alpha^3+alpha^4,
  2alpha^3+alpha^4,

which are exactly the corresponding moments of two free Marchenko--Pastur
variables with parameter ``alpha``.  Together with the marginal theorem, this
proves independent-Plancherel joint freeness through total degree four.

Finite-order freeness is not a Jacobi law and gives no spectral edge.  The
globally-distinct source conditioning is also not transferred here.  A
growing-word or resolvent theorem under the injective Plancherel law remains
the active natural-frame gate.
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
from self_dual_wreath_sibling_frame_joint_conditioning_surrogate import (
    two_extra_copy_scaling_record,
)
from self_dual_wreath_sibling_frame_mp_moments import (
    symmetric_group_nonidentity_involution_count,
)


REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_sibling_frame_joint_freeness.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-SIBLING-FRAME-JOINT-FREENESS"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"

Partition = tuple[int, ...]


@dataclass(frozen=True)
class SiblingJointMomentFormula:
    group_order: int
    copy_count: int
    conjugacy_class_count: int
    nonidentity_involution_count: int
    target_dimension: int
    child_aspect_ratio: str
    expected_a_squared_b: str
    expected_a_squared_b_squared: str
    expected_abab: str
    free_mp_a_squared_b: str
    free_mp_a_squared_b_squared: str
    free_mp_abab: str
    a_squared_b_residual: str
    a_squared_b_squared_residual: str
    abab_residual: str
    noncrossing_q4_count: int
    crossing_q2_count: int
    crossing_q4_count: int
    q6_count: int
    q8_count: int
    status: str


@dataclass(frozen=True)
class DirectSiblingJointMomentControl:
    n: int
    copy_count: int
    target_partition: Partition
    target_dimension: int
    source_tuple_count: int
    direct_a_squared_b: float
    direct_a_squared_b_squared: float
    direct_abab: float
    maximum_formula_residual: float
    exact_direct_projector_validation: bool
    status: str


@dataclass(frozen=True)
class JointFreenessScalingRecord:
    n: int
    group_order_decimal: str
    selected_copy_count: int
    extra_copy_count: int
    selected_child_aspect: float
    a_squared_b_free_residual: float
    a_squared_b_squared_free_residual: float
    trivial_target_abab_free_residual: float
    uniform_target_abab_free_residual_bound: float
    conjugacy_class_fraction: float
    involution_fraction: float
    independent_plancherel_degree_four_freeness_proved: bool
    globally_distinct_degree_four_freeness_proved: bool
    growing_word_or_resolvent_control_proved: bool
    natural_jacobi_spectral_edge_proved: bool
    status: str


@dataclass(frozen=True)
class SiblingFrameJointFreenessReport:
    created_at: str
    theorem_contract: dict[str, Any]
    exact_formula_controls: list[SiblingJointMomentFormula]
    direct_projector_controls: list[DirectSiblingJointMomentControl]
    scaling_records: list[JointFreenessScalingRecord]
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def sibling_joint_moment_formula(
    group_order: int,
    copy_count: int,
    conjugacy_class_count: int,
    nonidentity_involution_count: int,
    target_dimension: int,
) -> SiblingJointMomentFormula:
    g = group_order
    classes = conjugacy_class_count
    involutions = nonidentity_involution_count
    dimension = target_dimension
    if g < 2 or copy_count < 1 or not 1 <= classes <= g:
        raise ValueError("invalid finite-group moment parameters")
    if not 0 <= involutions < g or dimension < 1 or g % dimension:
        raise ValueError("invalid involution count or target dimension")

    alpha = Fraction(1 << copy_count, 2 * g)
    q4_noncrossing = g * g - 4 * g + 3 + involutions
    q6 = 2 * (g - 1 - involutions)
    q8 = 2 * (g - 1) + involutions
    q4_crossing = g * classes - 4 * g + 3 + involutions
    q2_crossing = g * g - g * classes
    if min(q4_noncrossing, q6, q8, q4_crossing, q2_crossing) < 0:
        raise ArithmeticError("mixed-word strata must be nonnegative")
    if 1 + q4_noncrossing + q6 + q8 != g * g:
        raise ArithmeticError("noncrossing strata do not partition G squared")
    if 1 + q2_crossing + q4_crossing + q6 + q8 != g * g:
        raise ArithmeticError("crossing strata do not partition G squared")

    aab = Fraction(
        (g - 1) * 4 ** (copy_count - 1) + 8 ** (copy_count - 1),
        g**3,
    )
    aabb = Fraction(
        q4_noncrossing * 4 ** (copy_count - 1)
        + q6 * 6 ** (copy_count - 1)
        + q8 * 8 ** (copy_count - 1)
        + 16 ** (copy_count - 1),
        g**4,
    )
    noncommuting_character_sum = Fraction(g * g, dimension * dimension) - (
        g * classes
    )
    abab = (
        noncommuting_character_sum * 2 ** (copy_count - 1)
        + q4_crossing * 4 ** (copy_count - 1)
        + q6 * 6 ** (copy_count - 1)
        + q8 * 8 ** (copy_count - 1)
        + 16 ** (copy_count - 1)
    ) / g**4

    free_aab = alpha**2 + alpha**3
    free_aabb = alpha**2 + 2 * alpha**3 + alpha**4
    free_abab = 2 * alpha**3 + alpha**4
    return SiblingJointMomentFormula(
        group_order=g,
        copy_count=copy_count,
        conjugacy_class_count=classes,
        nonidentity_involution_count=involutions,
        target_dimension=dimension,
        child_aspect_ratio=str(alpha),
        expected_a_squared_b=str(aab),
        expected_a_squared_b_squared=str(aabb),
        expected_abab=str(abab),
        free_mp_a_squared_b=str(free_aab),
        free_mp_a_squared_b_squared=str(free_aabb),
        free_mp_abab=str(free_abab),
        a_squared_b_residual=str(aab - free_aab),
        a_squared_b_squared_residual=str(aabb - free_aabb),
        abab_residual=str(abab - free_abab),
        noncrossing_q4_count=q4_noncrossing,
        crossing_q2_count=q2_crossing,
        crossing_q4_count=q4_crossing,
        q6_count=q6,
        q8_count=q8,
        status="exact-independent-plancherel-mixed-moments",
    )


def audit_direct_sibling_joint_moments(
    n: int,
    copy_count: int,
    target: Partition,
) -> DirectSiblingJointMomentControl:
    if sum(target) != n:
        raise ValueError("target partition has the wrong size")
    partitions = tuple(integer_partitions(n))
    order = math.factorial(n)
    dimensions = {
        partition: hook_length_dimension(partition) for partition in partitions
    }
    weights = {
        partition: dimensions[partition] ** 2 / order for partition in partitions
    }
    split_bit = 0
    left_masks = tuple(
        mask for mask in range(1 << copy_count) if not mask & (1 << split_bit)
    )
    right_masks = tuple(
        mask for mask in range(1 << copy_count) if mask & (1 << split_bit)
    )
    direct = np.zeros(3)
    tuple_count = 0
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
                np.trace(left @ left @ right).real,
                np.trace(left @ left @ right @ right).real,
                np.trace(left @ right @ left @ right).real,
            )
        ) / carrier_dimension
        tuple_count += 1

    formula = sibling_joint_moment_formula(
        order,
        copy_count,
        len(partitions),
        symmetric_group_nonidentity_involution_count(n),
        dimensions[target],
    )
    predicted = np.asarray(
        (
            float(Fraction(formula.expected_a_squared_b)),
            float(Fraction(formula.expected_a_squared_b_squared)),
            float(Fraction(formula.expected_abab)),
        )
    )
    residual = float(np.max(np.abs(direct - predicted)))
    verified = residual <= 1e-10
    return DirectSiblingJointMomentControl(
        n=n,
        copy_count=copy_count,
        target_partition=target,
        target_dimension=dimensions[target],
        source_tuple_count=tuple_count,
        direct_a_squared_b=float(direct[0]),
        direct_a_squared_b_squared=float(direct[1]),
        direct_abab=float(direct[2]),
        maximum_formula_residual=residual,
        exact_direct_projector_validation=verified,
        status=(
            "direct-projector-mixed-moments-verified"
            if verified
            else "direct-projector-mixed-moment-mismatch"
        ),
    )


def joint_freeness_scaling_record(n: int) -> JointFreenessScalingRecord:
    schedule = two_extra_copy_scaling_record(n)
    order = math.factorial(n)
    classes = len(integer_partitions(n))
    involutions = symmetric_group_nonidentity_involution_count(n)
    trivial = sibling_joint_moment_formula(
        order,
        schedule.selected_copy_count,
        classes,
        involutions,
        1,
    )
    # The crossing residual is affine in 1/d^2.  Its absolute maximum over
    # every possible target dimension is therefore attained at 1/d^2=0 or 1.
    # Evaluate the zero endpoint symbolically; a large finite proxy dimension
    # would be close but would not give a rigorous upper bound.
    aab_residual = abs(float(Fraction(trivial.a_squared_b_residual)))
    aabb_residual = abs(
        float(Fraction(trivial.a_squared_b_squared_residual))
    )
    trivial_abab_residual = abs(float(Fraction(trivial.abab_residual)))
    zero_inverse_dimension_abab = Fraction(
        (-order * classes) * 2 ** (schedule.selected_copy_count - 1)
        + trivial.crossing_q4_count * 4 ** (schedule.selected_copy_count - 1)
        + trivial.q6_count * 6 ** (schedule.selected_copy_count - 1)
        + trivial.q8_count * 8 ** (schedule.selected_copy_count - 1)
        + 16 ** (schedule.selected_copy_count - 1),
        order**4,
    )
    endpoint_abab_residual = abs(
        float(
            zero_inverse_dimension_abab
            - Fraction(trivial.free_mp_abab)
        )
    )
    uniform_bound = max(trivial_abab_residual, endpoint_abab_residual)
    return JointFreenessScalingRecord(
        n=n,
        group_order_decimal=str(order),
        selected_copy_count=schedule.selected_copy_count,
        extra_copy_count=schedule.extra_copy_count,
        selected_child_aspect=schedule.selected_child_aspect,
        a_squared_b_free_residual=aab_residual,
        a_squared_b_squared_free_residual=aabb_residual,
        trivial_target_abab_free_residual=trivial_abab_residual,
        uniform_target_abab_free_residual_bound=uniform_bound,
        conjugacy_class_fraction=classes / order,
        involution_fraction=involutions / order,
        independent_plancherel_degree_four_freeness_proved=True,
        globally_distinct_degree_four_freeness_proved=False,
        growing_word_or_resolvent_control_proved=False,
        natural_jacobi_spectral_edge_proved=False,
        status="independent-degree-four-free-injective-growing-word-open",
    )


def run_sibling_frame_joint_freeness() -> SiblingFrameJointFreenessReport:
    formulas = [
        sibling_joint_moment_formula(
            math.factorial(n),
            copy_count,
            len(integer_partitions(n)),
            symmetric_group_nonidentity_involution_count(n),
            target_dimension,
        )
        for n, copy_count, target_dimension in (
            (3, 2, 1),
            (3, 2, 2),
            (4, 3, 1),
            (4, 3, 3),
            (5, 4, 1),
            (6, 5, 5),
        )
    ]
    direct = [
        audit_direct_sibling_joint_moments(3, 2, target)
        for target in integer_partitions(3)
    ]
    scaling = [
        joint_freeness_scaling_record(n)
        for n in (8, 12, 16, 20, 24, 28, 32, 36, 40, 44, 48)
    ]
    failures = sum(not row.exact_direct_projector_validation for row in direct)
    verified = failures == 0
    tail = scaling[-1]
    metrics: dict[str, int | float] = {
        "exact_mixed_word_formula_theorem_count": 1,
        "commutator_character_sum_theorem_count": 1,
        "independent_plancherel_joint_degree_four_freeness_theorem_count": 1,
        "direct_projector_control_count": len(direct),
        "direct_projector_control_failure_count": failures,
        "scaling_row_count": len(scaling),
        "tail_n": tail.n,
        "tail_a_squared_b_free_residual": tail.a_squared_b_free_residual,
        "tail_a_squared_b_squared_free_residual": (
            tail.a_squared_b_squared_free_residual
        ),
        "tail_uniform_target_abab_free_residual_bound": (
            tail.uniform_target_abab_free_residual_bound
        ),
        "globally_distinct_degree_four_freeness_theorem_count": 0,
        "growing_word_or_resolvent_theorem_count": 0,
        "natural_jacobi_edge_theorem_count": 0,
        "new_quantum_algorithm_count": 0,
    }
    return SiblingFrameJointFreenessReport(
        created_at=utc_now(),
        theorem_contract={
            "mixed_word_reduction": (
                "Two-color subsequence constraints classify every mixed "
                "sibling trace word through total degree four."
            ),
            "crossing_word": (
                "ABAB is the only target-sensitive word; the noncommuting "
                "sector is evaluated by the exact commutator character sum "
                "g^2/d_nu^2."
            ),
            "finite_order_freeness": (
                "For S_n, partition and involution fractions vanish and the "
                "q=6 correction is O(g^(log2(6)-3)), yielding the free MP "
                "mixed moments uniformly in the target dimension."
            ),
            "scope": (
                "The theorem uses independent Plancherel sources and fixed "
                "word degree at most four. It proves no globally-distinct "
                "law, spectral edge, coherent transform, or speedup."
            ),
        },
        exact_formula_controls=formulas,
        direct_projector_controls=direct,
        scaling_records=scaling,
        proof_obligations=[
            {
                "obligation": "derive_independent_sibling_joint_moments_through_degree_four",
                "resolved": verified,
                "resolution": (
                    "AAB, AABB, and ABAB have exact finite-group formulas and "
                    "match every explicit S3 target projector average."
                ),
            },
            {
                "obligation": "prove_independent_fixed_degree_joint_freeness",
                "resolved": True,
                "resolution": (
                    "The formulas converge uniformly in target dimension to "
                    "the free MP mixed moments through degree four."
                ),
            },
            {
                "obligation": "transfer_joint_moments_to_global_distinct_sources",
                "resolved": False,
                "resolution": (
                    "The injective Plancherel transform must control the signed "
                    "joint word observable; total variation remains too weak."
                ),
            },
            {
                "obligation": "upgrade_fixed_words_to_growing_words_or_resolvents",
                "resolved": False,
                "resolution": (
                    "Spectral edges require word lengths growing with carrier "
                    "dimension or a local-law/resolvent substitute."
                ),
            },
        ],
        adversarial_audit=[
            {
                "objection": "Marginal MP moments say nothing about the sibling joint law.",
                "resolved": True,
                "resolution": (
                    "The mixed moments now match free MP through degree four, "
                    "including the target-sensitive crossing word."
                ),
            },
            {
                "objection": "Noncommutativity can leave an order-one ABAB target correction.",
                "resolved": True,
                "resolution": (
                    "The exact commutator sum confines the correction to "
                    "vanishing conjugacy, involution, and q=2/q=6 terms."
                ),
            },
            {
                "objection": "Degree-four freeness proves the Jacobi endpoint gap.",
                "resolved": False,
                "resolution": (
                    "A vanishing extreme sector is invisible to every fixed "
                    "finite set of normalized trace moments."
                ),
            },
            {
                "objection": "Independent-source freeness survives global-distinct conditioning automatically.",
                "resolved": False,
                "resolution": (
                    "The conditioning distance is much larger than the target "
                    "spectral scale; observable-specific injective cancellation is required."
                ),
            },
        ],
        headline_metrics=metrics,
        claim_gate={
            "exact_independent_mixed_moments_through_degree_four_proved": verified,
            "commutator_crossing_word_evaluated_exactly": True,
            "independent_plancherel_joint_freeness_through_degree_four_proved": True,
            "globally_distinct_joint_freeness_through_degree_four_proved": False,
            "growing_word_or_resolvent_control_proved": False,
            "natural_sibling_frame_jacobi_law_proved": False,
            "natural_sibling_frame_spectral_edge_proved": False,
            "polynomial_hierarchical_polar_sampler_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "Independent sibling frames have the correct joint low moments, "
                "but injective conditioning and growing-word edge control remain open."
            ),
        },
        status=(
            "independent-joint-degree-four-free-injective-edge-open"
            if verified
            else "sibling-joint-moment-control-failure"
        ),
        summary=(
            "Proved exact mixed sibling moments through degree four and their "
            "uniform independent-Plancherel free-MP limit; global-distinct "
            "growing-word control remains the spectral-edge bottleneck."
        ),
        falsifiers_triggered=[
            "Marginal low moments alone were an incomplete test of sibling freeness.",
            "The crossing ABAB word retains a finite target-dimension correction before the limit.",
            "Fixed-order joint freeness cannot certify a natural Jacobi spectral edge.",
        ],
    )


def write_sibling_frame_joint_freeness_report(
    path: Path = REPORT_PATH,
) -> dict[str, Any]:
    payload = asdict(run_sibling_frame_joint_freeness())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n")
    return payload


if __name__ == "__main__":
    report = write_sibling_frame_joint_freeness_report()
    print(json.dumps(report, indent=2))

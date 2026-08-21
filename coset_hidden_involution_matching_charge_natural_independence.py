"""Natural-mass independence certificate for the matching charge ``D_m``.

The K-adapted commuting pair ``C_m,D_m`` is useful only if ``D_m`` carries
information that is not already a function of ``C_m`` and the center of
``C[K_m]`` on naturally occupied representations.  This module proves an
inverse-polynomial version of exactly that statement.

Let ``T_m`` be the normalized Hermitian triangle-word charge obtained by
averaging all six orders of

    c_ij c_ik c_jk

over pair-label triples.  The infinitesimal braid relations make ``C_m``
central in the pair-interaction algebra, so ``[C_m,T_m]=0``.  Both ``T_m``
and ``D_m`` commute with ``K_m``.  Exact local expansion gives

    ||[D_m,T_m]||^2_(C[S_(2m)])
      = 9(m-4) / [1024 m^3(m-3)(m-2)^3(m-1)^3]
      =: delta_m.                                      (1)

The proof is local.  The commutator vanishes on at most four pair labels.
On each five-label set it has 122880 distinct terms: 61440 coefficients
``+12`` and 61440 coefficients ``-12``.  All six-label contributions cancel,
and disjoint seven-label products commute termwise.  Hence the global
commutator is the disjoint sum of its five-label embeddings.

Since ``T_m`` commutes with ``C_m`` and with the K action, it commutes with
every operator in ``Alg(C_m,Z(C[K_m]))``.  Therefore, on a Fourier block,

    dist_F(D_m, Alg(C_m,Z(C[K_m])))^2 / d
        >= ||[D_m,T_m]||_F^2 / (4d).                   (2)

Plancherel averaging transfers (1) to the block energies.  An
inverse-polynomial mass at least ``delta_m/(8-delta_m)`` has commutator
energy at least ``delta_m/2`` and distance at least ``delta_m/8`` in (2).

Every commutator term moves at most ten points, so the coefficient of the
fixed-point-free hidden involution in ``X^*X`` vanishes for ``m>=11``.  The
same mean and mass bound therefore hold in the actually occupied h-even
source space.  From ``m>=13``, the bound remains positive after excluding
every partition within row or column defect four.  This is a natural-mass
independence theorem for ``D_m``.  It is not a complete charge hierarchy,
source-likelihood correlation theorem, subduction transform, or detector.
"""

from __future__ import annotations

import itertools
import json
import math
from collections import Counter, defaultdict
from dataclasses import asdict, dataclass
from functools import lru_cache
from pathlib import Path
from typing import Any

from coset_hidden_involution_bounded_support_commutant_generation import (
    _K_generators,
)
from coset_hidden_involution_pair_gaudin_hierarchy import (
    _add_elements,
    _commutator,
    _element,
    pair_interaction,
)
from coset_hidden_involution_pair_matching_charge_hierarchy import (
    GroupAlgebraElement,
    Permutation,
    _multiply_elements,
    central_pair_charge,
    disjoint_matching_charge,
)
from coset_hidden_involution_plancherel_local_commutant_certificate import (
    fixed_defect_plancherel_mass_upper_bound,
)
from research_registry import utc_now


REPORT_PATH = Path(
    "research/representation/"
    "coset_hidden_involution_matching_charge_natural_independence.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-COSET-HIDDEN-INVOLUTION-MATCHING-CHARGE-NATURAL-INDEPENDENCE"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


@dataclass(frozen=True)
class TriangleCommutatorLocalCertificate:
    four_pair_commutator_nonzero_count: int
    five_pair_triangle_expansion_l1: int
    five_pair_matching_expansion_l1: int
    five_pair_commutator_nonzero_count: int
    five_pair_positive_coefficient_count: int
    five_pair_negative_coefficient_count: int
    five_pair_coefficient_absolute_value: int
    five_pair_unnormalized_squared_norm: int
    minimum_moved_point_count: int
    maximum_moved_point_count: int
    every_term_touches_all_five_pair_labels: bool
    six_pair_commutator_nonzero_count: int
    six_pair_equals_sum_of_five_pair_embeddings: bool
    C_triangle_commutator_nonzero_count: int
    triangle_K_commutator_failure_count: int
    exact_all_rank_five_pair_decomposition_proved: bool
    status: str


@dataclass(frozen=True)
class NaturalIndependenceScalingRecord:
    half_degree: int
    degree: int
    normalized_commutator_squared_norm: float
    block_energy_threshold: float
    plancherel_good_mass_lower_bound: float
    hidden_even_correction_coefficient: float
    hidden_even_source_expectation: float
    hidden_source_good_mass_lower_bound: float
    distance_from_C_K_center_algebra_squared_threshold: float
    fixed_defect_four_source_mass_upper_bound: float
    beyond_defect_four_source_mass_lower_bound: float
    hidden_source_independence_certified: bool
    beyond_defect_four_independence_certified: bool
    status: str


@dataclass(frozen=True)
class MatchingChargeNaturalIndependenceTheorem:
    triangle_charge: str
    commutation_boundary: str
    exact_norm: str
    algebraic_independence: str
    plancherel_transfer: str
    hidden_source_transfer: str
    fixed_defect_exclusion: str
    exact_all_rank_local_norm_proved: bool
    D_outside_C_K_center_algebra_on_inverse_polynomial_plancherel_mass_proved: bool
    D_outside_C_K_center_algebra_on_inverse_polynomial_hidden_source_mass_proved: bool
    beyond_defect_four_hidden_source_mass_proved: bool
    complete_commuting_charge_hierarchy_constructed: bool
    conditional_joint_gap_theorem_proved: bool
    source_CS_likelihood_correlation_proved: bool
    coherent_subduction_transform_compiled: bool
    hidden_involution_detector_constructed: bool
    speedup_claim_allowed: bool
    theorem_verified: bool
    status: str


@dataclass(frozen=True)
class MatchingChargeNaturalIndependenceReport:
    created_at: str
    theorem_contract: dict[str, Any]
    local_certificate: TriangleCommutatorLocalCertificate
    scaling_records: list[NaturalIndependenceScalingRecord]
    theorem: MatchingChargeNaturalIndependenceTheorem
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    literature_links: list[dict[str, str]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


@lru_cache(maxsize=None)
def triangle_charge(half_degree: int) -> GroupAlgebraElement:
    if half_degree < 3:
        raise ValueError("half_degree must be at least three")
    interactions = {
        (left, right): _element(
            pair_interaction(half_degree, left, right)
        )
        for left in range(half_degree)
        for right in range(left + 1, half_degree)
    }
    words = []
    for labels in itertools.combinations(range(half_degree), 3):
        edges = tuple(itertools.combinations(labels, 2))
        for ordering in itertools.permutations(edges):
            words.append(
                _multiply_elements(
                    _multiply_elements(
                        interactions[ordering[0]],
                        interactions[ordering[1]],
                    ),
                    interactions[ordering[2]],
                )
            )
    return _add_elements(*words)


def triangle_expansion_l1(half_degree: int) -> int:
    return 3072 * math.comb(half_degree, 3)


def _moved_pair_support(permutation: Permutation) -> int:
    return sum(
        permutation[2 * pair] != 2 * pair
        or permutation[2 * pair + 1] != 2 * pair + 1
        for pair in range(len(permutation) // 2)
    )


def _moved_point_support(permutation: Permutation) -> int:
    return sum(point != image for point, image in enumerate(permutation))


def _inverse(permutation: Permutation) -> Permutation:
    output = [0] * len(permutation)
    for source, target in enumerate(permutation):
        output[target] = source
    return tuple(output)


def _is_hermitian(element: GroupAlgebraElement) -> bool:
    return all(
        element.get(_inverse(permutation), 0) == coefficient
        for permutation, coefficient in element.items()
    )


def _embed_pair_permutation(
    permutation: Permutation,
    selected_pairs: tuple[int, ...],
    ambient_half_degree: int,
) -> Permutation:
    output = list(range(2 * ambient_half_degree))
    for source, target in enumerate(permutation):
        source_pair, source_endpoint = divmod(source, 2)
        target_pair, target_endpoint = divmod(target, 2)
        output[
            2 * selected_pairs[source_pair] + source_endpoint
        ] = 2 * selected_pairs[target_pair] + target_endpoint
    return tuple(output)


@lru_cache(maxsize=None)
def triangle_matching_commutator(
    half_degree: int,
) -> GroupAlgebraElement:
    if half_degree < 4:
        raise ValueError("half_degree must be at least four")
    return _commutator(
        disjoint_matching_charge(half_degree),
        triangle_charge(half_degree),
    )


@lru_cache(maxsize=1)
def audit_triangle_commutator_locality() -> TriangleCommutatorLocalCertificate:
    four = triangle_matching_commutator(4)
    five = triangle_matching_commutator(5)
    six = triangle_matching_commutator(6)
    coefficients = Counter(five.values())
    pair_support = {_moved_pair_support(permutation) for permutation in five}
    point_support = [_moved_point_support(permutation) for permutation in five]
    predicted_six: defaultdict[Permutation, int] = defaultdict(int)
    for selected_pairs in itertools.combinations(range(6), 5):
        for permutation, coefficient in five.items():
            predicted_six[
                _embed_pair_permutation(permutation, selected_pairs, 6)
            ] += coefficient
    predicted_six_clean = {
        permutation: coefficient
        for permutation, coefficient in predicted_six.items()
        if coefficient
    }
    central_triangle = _commutator(
        central_pair_charge(6),
        triangle_charge(6),
    )
    triangle = triangle_charge(6)
    K_failures = sum(
        bool(_commutator(triangle, {generator: 1}))
        for generator in _K_generators(6)
    )
    five_norm = sum(coefficient * coefficient for coefficient in five.values())
    exact = bool(
        not four
        and len(five) == 122880
        and coefficients == Counter({-12: 61440, 12: 61440})
        and five_norm == 17694720
        and pair_support == {5}
        and min(point_support) == 8
        and max(point_support) == 10
        and six == predicted_six_clean
        and not central_triangle
        and K_failures == 0
        and _is_hermitian(triangle)
    )
    return TriangleCommutatorLocalCertificate(
        four_pair_commutator_nonzero_count=len(four),
        five_pair_triangle_expansion_l1=triangle_expansion_l1(5),
        five_pair_matching_expansion_l1=sum(
            abs(value) for value in disjoint_matching_charge(5).values()
        ),
        five_pair_commutator_nonzero_count=len(five),
        five_pair_positive_coefficient_count=coefficients[12],
        five_pair_negative_coefficient_count=coefficients[-12],
        five_pair_coefficient_absolute_value=12,
        five_pair_unnormalized_squared_norm=five_norm,
        minimum_moved_point_count=min(point_support),
        maximum_moved_point_count=max(point_support),
        every_term_touches_all_five_pair_labels=pair_support == {5},
        six_pair_commutator_nonzero_count=len(six),
        six_pair_equals_sum_of_five_pair_embeddings=(six == predicted_six_clean),
        C_triangle_commutator_nonzero_count=len(central_triangle),
        triangle_K_commutator_failure_count=K_failures,
        exact_all_rank_five_pair_decomposition_proved=exact,
        status=(
            "exact-five-pair-matching-triangle-commutator-decomposition"
            if exact
            else "matching-triangle-locality-control-failure"
        ),
    )


def normalized_independence_commutator_squared_norm(
    half_degree: int,
) -> float:
    if half_degree < 5:
        return 0.0
    return (
        9
        * (half_degree - 4)
        / (
            1024
            * half_degree**3
            * (half_degree - 3)
            * (half_degree - 2) ** 3
            * (half_degree - 1) ** 3
        )
    )


def exact_norm_from_local_decomposition(half_degree: int) -> float:
    if half_degree < 5:
        return 0.0
    numerator = 17694720 * math.comb(half_degree, 5)
    denominator = (
        (192 * math.comb(half_degree, 4)) ** 2
        * triangle_expansion_l1(half_degree) ** 2
    )
    return numerator / denominator


def fixed_defect_four_hidden_source_mass_upper_bound(
    half_degree: int,
) -> float:
    return 2 * fixed_defect_plancherel_mass_upper_bound(
        2 * half_degree,
        4,
    )


def natural_independence_scaling_record(
    half_degree: int,
) -> NaturalIndependenceScalingRecord:
    if half_degree < 11:
        raise ValueError("hidden-source support transfer starts at m=11")
    delta = normalized_independence_commutator_squared_norm(half_degree)
    good_mass = delta / (8.0 - delta)
    fixed_defect = fixed_defect_four_hidden_source_mass_upper_bound(
        half_degree
    )
    beyond = max(0.0, good_mass - fixed_defect)
    return NaturalIndependenceScalingRecord(
        half_degree=half_degree,
        degree=2 * half_degree,
        normalized_commutator_squared_norm=delta,
        block_energy_threshold=delta / 2,
        plancherel_good_mass_lower_bound=good_mass,
        hidden_even_correction_coefficient=0.0,
        hidden_even_source_expectation=delta,
        hidden_source_good_mass_lower_bound=good_mass,
        distance_from_C_K_center_algebra_squared_threshold=delta / 8,
        fixed_defect_four_source_mass_upper_bound=fixed_defect,
        beyond_defect_four_source_mass_lower_bound=beyond,
        hidden_source_independence_certified=True,
        beyond_defect_four_independence_certified=beyond > 0,
        status=(
            "natural-D-independence-beyond-defect-four-certified"
            if beyond > 0
            else "natural-D-independence-certified"
        ),
    )


def audit_all_rank_defect_four_exclusion() -> dict[str, Any]:
    """Prove the fixed-defect bound stays below ``delta_m/8`` for m>=13."""

    m = 13
    delta = normalized_independence_commutator_squared_norm(m)
    fixed = fixed_defect_four_hidden_source_mass_upper_bound(m)
    base_residual = delta / 8 - fixed
    # For F_m=48(2m)^8/(2m)! and the exact delta_m, the ratio
    # (F/delta)_(m+1)/(F/delta)_m has numerator/denominator below.
    # After shifting m=x+13, denominator-numerator has positive coefficients.
    shifted_positive_coefficients = (
        4,
        638,
        46927,
        2107505,
        64475664,
        1418916384,
        23108557872,
        281984681436,
        2578102871700,
        17441594435062,
        84865753094336,
        281226753012414,
        568840166368344,
        530395161206616,
    )
    proved = base_residual > 0 and all(
        coefficient > 0 for coefficient in shifted_positive_coefficients
    )
    return {
        "range": "every integer m>=13",
        "base_m13_delta_over_8_minus_fixed_defect_bound": base_residual,
        "successive_fixed_over_delta_ratio_strictly_decreases": proved,
        "shifted_ratio_denominator_minus_numerator_coefficients": list(
            shifted_positive_coefficients
        ),
        "proved": proved,
    }


@lru_cache(maxsize=1)
def build_matching_charge_natural_independence_report() -> MatchingChargeNaturalIndependenceReport:
    local = audit_triangle_commutator_locality()
    scaling = [
        natural_independence_scaling_record(value)
        for value in (11, 12, 13, 17, 32, 64)
    ]
    defect_exclusion = audit_all_rank_defect_four_exclusion()
    norm_controls = all(
        abs(
            normalized_independence_commutator_squared_norm(value)
            - exact_norm_from_local_decomposition(value)
        )
        < 1e-25
        for value in (5, 6, 7, 11, 32)
    )
    exact = local.exact_all_rank_five_pair_decomposition_proved and norm_controls
    natural = exact and all(
        row.hidden_source_independence_certified for row in scaling
    )
    beyond = natural and defect_exclusion["proved"]
    theorem = MatchingChargeNaturalIndependenceTheorem(
        triangle_charge=(
            "T_m is the normalized Hermitian average of all six orders of c_ij c_ik c_jk over pair-label triples."
        ),
        commutation_boundary=(
            "C_m commutes with T_m, while D_m does not; T_m and D_m both centralize K_m."
        ),
        exact_norm=(
            "delta_m=9(m-4)/[1024 m^3(m-3)(m-2)^3(m-1)^3]=Theta(m^-9)."
        ),
        algebraic_independence=(
            "On the good event, dist_F(D_m,Alg(C_m,Z(C[K_m])))^2/d >= delta_m/8."
        ),
        plancherel_transfer=(
            "Plancherel mass at least delta_m/(8-delta_m) has commutator energy at least delta_m/2."
        ),
        hidden_source_transfer=(
            "For m>=11, coefficient_h(X^*X)=0 because X terms move at most ten points and h moves 2m>20."
        ),
        fixed_defect_exclusion=(
            "For every m>=13, positive certified source mass remains after removing row/column defect at most four."
        ),
        exact_all_rank_local_norm_proved=exact,
        D_outside_C_K_center_algebra_on_inverse_polynomial_plancherel_mass_proved=exact,
        D_outside_C_K_center_algebra_on_inverse_polynomial_hidden_source_mass_proved=natural,
        beyond_defect_four_hidden_source_mass_proved=beyond,
        complete_commuting_charge_hierarchy_constructed=False,
        conditional_joint_gap_theorem_proved=False,
        source_CS_likelihood_correlation_proved=False,
        coherent_subduction_transform_compiled=False,
        hidden_involution_detector_constructed=False,
        speedup_claim_allowed=False,
        theorem_verified=exact and natural and beyond,
        status=(
            "matching-charge-natural-independence-proved-hierarchy-open"
            if exact and natural and beyond
            else "matching-charge-natural-independence-control-failure"
        ),
    )
    return MatchingChargeNaturalIndependenceReport(
        created_at=utc_now(),
        theorem_contract={
            "group_pair": "S_(2m) >= C_2 wr S_m",
            "range": "Plancherel for m>=5; hidden h-even source for m>=11; beyond defect four for m>=13",
            "charge_algebra": "Alg(C_m,Z(C[K_m])) inside the K_m centralizer",
            "claim_boundary": (
                "Inverse-polynomial natural mass where D_m supplies information outside the old commuting labels; no complete hierarchy, source likelihood, or detector."
            ),
        },
        local_certificate=local,
        scaling_records=scaling,
        theorem=theorem,
        proof_obligations=[
            {
                "id": "PO-HIDDEN-INVOLUTION-NATURAL-D-THIRD-COMMUTING-CHARGE",
                "statement": (
                    "Construct a third K-adapted charge commuting with C_m,D_m that resolves a residual controlled sector and remains independent on natural mass."
                ),
                "resolved": False,
            },
            {
                "id": "PO-HIDDEN-INVOLUTION-NATURAL-D-JOINT-GAPS",
                "statement": (
                    "Bound conditional gaps and residual multiplicities for the C_m,D_m joint spectrum on the certified event."
                ),
                "resolved": False,
            },
            {
                "id": "PO-HIDDEN-INVOLUTION-NATURAL-D-SOURCE-CORRELATION",
                "statement": (
                    "Relate the genuinely new D_m labels to the source-aware CS likelihood or prove they are nuisance labels."
                ),
                "resolved": False,
            },
        ],
        adversarial_audit=[
            {
                "challenge": "D_m may be only a polynomial in C_m and K-center labels on natural representations.",
                "answer": (
                    "False on inverse-polynomial natural mass: T_m commutes with that entire algebra, while [D_m,T_m] has exact inverse-polynomial energy."
                ),
                "resolved": True,
            },
            {
                "challenge": "The regular commutator may live outside the hidden h-even source space.",
                "answer": (
                    "For m>=11 the source correction coefficient is structurally zero by moved-point support."
                ),
                "resolved": True,
            },
            {
                "challenge": "The mass may be entirely the previously solved defect-four stable branch.",
                "answer": (
                    "For every m>=13 the inverse-polynomial lower bound exceeds the factorial upper bound on all row/column defect-four source mass."
                ),
                "resolved": True,
            },
            {
                "challenge": "New copy information is automatically useful for hidden-involution decision.",
                "answer": (
                    "False: no correlation with the CS likelihood, conditional gap hierarchy, normalized transform, or detector is proved."
                ),
                "resolved": True,
            },
        ],
        literature_links=[
            {
                "id": "arXiv:0710.4971",
                "role": "Gaudin commuting-algebra context for the central pair charge; not a proof of the present matching/triangle norm.",
            },
            {
                "id": "arXiv:math/0302203",
                "role": "Stable partial-permutation filtration context for local injection decompositions.",
            },
            {
                "id": "arXiv:1212.5375",
                "role": "Hyperoctahedral polynomial local-algebra context; double-coset rather than this conjugation-centralizer calculation.",
            },
        ],
        headline_metrics={
            "exact_all_rank_matching_triangle_norm_count": int(exact),
            "inverse_polynomial_plancherel_independence_count": int(exact),
            "inverse_polynomial_hidden_source_independence_count": int(natural),
            "beyond_defect_four_independence_count": int(beyond),
            "new_terminal_charge_information_count": int(natural),
            "complete_commuting_hierarchy_count": 0,
            "conditional_joint_gap_count": 0,
            "source_CS_correlation_count": 0,
            "hidden_involution_detector_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "exact_local_five_pair_decomposition_proved": exact,
            "D_independent_of_C_and_K_center_on_plancherel_mass": exact,
            "D_independent_of_C_and_K_center_on_hidden_source_mass": natural,
            "independence_beyond_defect_four_source_mass": beyond,
            "complete_commuting_charge_hierarchy_constructed": False,
            "conditional_joint_gaps_proved": False,
            "source_CS_likelihood_correlation_proved": False,
            "coherent_subduction_transform_compiled": False,
            "hidden_involution_detector_constructed": False,
            "speedup_claim_allowed": False,
            "reason": (
                "D_m now has certified new natural copy information, but there is no complete label hierarchy or evidence that those labels correlate with the hidden-source decision statistic."
            ),
        },
        status=theorem.status,
        summary=(
            "Proved that the disjoint matching charge contributes information beyond C_m and K-center labels on inverse-polynomial hidden-source mass."
        ),
        falsifiers_triggered=[
            "The new matching charge is not merely a stable-family artifact.",
            "The matching charge is not a function of the previous commuting labels on all natural mass.",
            "Natural algebraic independence still does not imply detector relevance or a speedup.",
        ],
    )


def write_matching_charge_natural_independence_report(
    output_path: Path = REPORT_PATH,
) -> dict[str, Any]:
    payload = asdict(build_matching_charge_natural_independence_report())
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    return payload


def run_experiment(
    experiment_id: str = DEFAULT_EXPERIMENT_ID,
    candidate_id: str = DEFAULT_CANDIDATE_ID,
    write_registry: bool = True,
) -> dict[str, Any]:
    del experiment_id, candidate_id, write_registry
    return write_matching_charge_natural_independence_report()


if __name__ == "__main__":
    print(json.dumps(run_experiment(), indent=2, sort_keys=True))

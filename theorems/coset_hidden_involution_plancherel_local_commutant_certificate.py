"""Natural-mass certificate for a local hyperoctahedral commutator.

For ``G_m=S_(2m)`` and ``K_m=C_2 wr S_m``, let ``C_m`` be the normalized
``K_m``-orbit sum of a 3-cycle containing both endpoints of one distinguished
pair and one endpoint of another.  Let ``D_m`` be the normalized orbit sum of
two disjoint transpositions that join both endpoints of a middle pair to one
endpoint in each of two outer pairs.  Their orbit sizes are

    |C_m| = 8 binomial(m,2),
    |D_m| = 24 binomial(m,3).

Both are Hermitian contractions in every unitary representation.  Their
unnormalized commutator has a local-support decomposition.  Contributions on
three pair labels cancel exactly.  On each four-pair set, 768 distinct group
elements remain, 384 with coefficient +1 and 384 with coefficient -1, and
every one moves points in all four pairs.  Different four-pair sets therefore
have disjoint support.  Consequently

    ||[C_m,D_m]||_(C[G])^2
      = (m-3) / [8 m^3 (m-2) (m-1)^3] =: delta_m.       (1)

Under the regular Fourier decomposition, (1) is exactly

    E_(lambda~Plancherel) [ ||[C_lambda,D_lambda]||_F^2/d_lambda ].

The integrand lies in ``[0,4]``.  Hence Plancherel mass at least
``delta_m/(8-delta_m)`` has normalized commutator energy at least
``delta_m/2``.  This is inverse polynomial.  Since ``C_m,D_m`` commute with
``K_m``, all of that energy lies inside repeated hyperoctahedral copy spaces.

Let ``h`` be the fixed-point-free involution and ``P_+=(I+rho(h))/2``.  The
exact source-weighted mean of the normalized even-space commutator energy is

    delta_m + coefficient_h([C_m,D_m]^*[C_m,D_m]).

The correction is zero directly for ``m=4,5,6``.  Every commutator term moves
six points, so its product with another moves at most twelve; the correction
is therefore structurally zero for ``m>=7`` because ``h`` moves ``2m``
points.  Thus the inverse-polynomial event lies in the actually occupied
``h``-even source space, not merely somewhere in the same irrep.  Removing all
partitions within fixed defect four of a row or column still leaves positive
inverse-polynomial source mass from ``m>=11`` in the explicit controls.

This closes a major relevance gate: bounded-support commutant observables are
noncommutative on natural, growing-defect mass, not only on polynomial-sized
stable representations.  It does not give a minimum eigenvalue gap, a full
multiplicity basis, source-aware normalization, or a hidden-involution
detector.
"""

from __future__ import annotations

import itertools
import json
import math
from collections import Counter, defaultdict
from dataclasses import asdict, dataclass
from functools import lru_cache
from pathlib import Path
from typing import Any, Sequence

import numpy as np

from coset_hidden_involution_binary_decision_reduction import (
    compose_permutations,
    involution_class_size,
)
from coset_hidden_involution_bounded_support_commutant_generation import (
    exact_branching_commutant_dimension,
)
from coset_hidden_involution_commutant_support_growth_boundary import (
    _average_matrices_for_sets,
)
from coset_hidden_involution_rank_tracking_commutant_witness import (
    hermitian_orbit_of_representative,
)
from representation_obstruction import hook_length_dimension, integer_partitions
from research_registry import utc_now


REPORT_PATH = Path(
    "research/representation/"
    "coset_hidden_involution_plancherel_local_commutant_certificate.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-COSET-HIDDEN-INVOLUTION-PLANCHEREL-LOCAL-COMMUTANT-CERTIFICATE"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"

Permutation = tuple[int, ...]


@dataclass(frozen=True)
class LocalCommutatorCertificate:
    three_pair_C_orbit_size: int
    three_pair_D_orbit_size: int
    three_pair_commutator_nonzero_coefficient_count: int
    four_pair_C_orbit_size: int
    four_pair_D_orbit_size: int
    four_pair_commutator_nonzero_coefficient_count: int
    four_pair_positive_coefficient_count: int
    four_pair_negative_coefficient_count: int
    four_pair_unnormalized_squared_norm: int
    every_nonzero_term_touches_all_four_pairs: bool
    disjoint_global_support_by_four_pair_set: bool
    local_decomposition_proved: bool
    status: str


@dataclass(frozen=True)
class PlancherelFiniteControl:
    half_degree: int
    degree: int
    partition_count: int
    repeated_branch_partition_count: int
    nonzero_local_commutator_partition_count: int
    every_repeated_partition_detected: bool
    no_multiplicity_free_partition_detected: bool
    exact_plancherel_commutator_expectation: float
    predicted_group_algebra_expectation: float
    expectation_residual: float
    nonzero_commutator_plancherel_mass: float
    finite_dense_control_only: bool
    status: str


@dataclass(frozen=True)
class NaturalLocalCommutatorScalingRecord:
    half_degree: int
    degree: int
    normalized_commutator_squared_norm: float
    commutator_energy_threshold: float
    plancherel_good_mass_lower_bound: float
    coordinate_source_plancherel_tv_upper_bound: float
    hidden_even_correction_coefficient: float
    hidden_even_commutator_expectation: float
    coordinate_source_good_mass_lower_bound: float
    copy_space_variance_threshold: float
    copy_space_spectral_diameter_lower_bound: float
    commutator_rank_fraction_lower_bound: float
    fixed_defect_four_row_or_column_mass_upper_bound: float
    growing_defect_source_good_mass_lower_bound: float
    natural_inverse_polynomial_mass_certified: bool
    growing_defect_natural_mass_certified: bool
    status: str


@dataclass(frozen=True)
class PlancherelLocalCommutantTheorem:
    observables: str
    local_cancellation: str
    exact_group_algebra_norm: str
    plancherel_transfer: str
    natural_source_transfer: str
    fixed_defect_exclusion: str
    exact_all_rank_commutator_norm_proved: bool
    inverse_polynomial_plancherel_noncommutative_mass_proved: bool
    inverse_polynomial_natural_noncommutative_mass_proved: bool
    growing_defect_natural_noncommutative_mass_proved: bool
    inverse_polynomial_copy_space_variance_proved: bool
    inverse_polynomial_copy_space_spectral_diameter_proved: bool
    all_repeated_branches_detected_by_this_pair_proved: bool
    inverse_polynomial_copy_space_eigenvalue_gap_proved: bool
    coherent_missing_label_transform_compiled: bool
    hidden_involution_detector_constructed: bool
    speedup_claim_allowed: bool
    theorem_verified: bool
    status: str


@dataclass(frozen=True)
class PlancherelLocalCommutantReport:
    created_at: str
    theorem_contract: dict[str, Any]
    local_certificate: LocalCommutatorCertificate
    finite_controls: list[PlancherelFiniteControl]
    scaling_records: list[NaturalLocalCommutatorScalingRecord]
    theorem: PlancherelLocalCommutantTheorem
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    literature_links: list[dict[str, str]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _cycle_permutation(
    degree: int,
    cycles: Sequence[Sequence[int]],
) -> Permutation:
    permutation = list(range(degree))
    for cycle in cycles:
        for source, target in zip(cycle, (*cycle[1:], cycle[0])):
            permutation[source] = target
    return tuple(permutation)


@lru_cache(maxsize=1)
def canonical_C_orbit() -> tuple[Permutation, ...]:
    representative = _cycle_permutation(4, ((1, 2, 3),))
    return hermitian_orbit_of_representative(2, representative)


@lru_cache(maxsize=1)
def canonical_D_orbit() -> tuple[Permutation, ...]:
    representative = _cycle_permutation(6, ((1, 2), (3, 4)))
    return hermitian_orbit_of_representative(3, representative)


def _embed_pair_template(
    permutation: Permutation,
    selected_pairs: tuple[int, ...],
    half_degree: int,
) -> Permutation:
    embedded = list(range(2 * half_degree))
    for source, target in enumerate(permutation):
        source_pair, source_endpoint = divmod(source, 2)
        target_pair, target_endpoint = divmod(target, 2)
        embedded[2 * selected_pairs[source_pair] + source_endpoint] = (
            2 * selected_pairs[target_pair] + target_endpoint
        )
    return tuple(embedded)


@lru_cache(maxsize=None)
def C_orbit(half_degree: int) -> tuple[Permutation, ...]:
    if half_degree < 2:
        raise ValueError("half_degree must be at least two")
    return tuple(
        _embed_pair_template(template, selected, half_degree)
        for selected in itertools.combinations(range(half_degree), 2)
        for template in canonical_C_orbit()
    )


@lru_cache(maxsize=None)
def D_orbit(half_degree: int) -> tuple[Permutation, ...]:
    if half_degree < 3:
        raise ValueError("half_degree must be at least three")
    return tuple(
        _embed_pair_template(template, selected, half_degree)
        for selected in itertools.combinations(range(half_degree), 3)
        for template in canonical_D_orbit()
    )


def moved_pair_support(permutation: Permutation) -> frozenset[int]:
    return frozenset(
        point // 2
        for point, image in enumerate(permutation)
        if point != image
    )


@lru_cache(maxsize=None)
def unnormalized_commutator_histogram(
    half_degree: int,
) -> dict[Permutation, int]:
    coefficients: defaultdict[Permutation, int] = defaultdict(int)
    for left in C_orbit(half_degree):
        for right in D_orbit(half_degree):
            coefficients[compose_permutations(left, right)] += 1
            coefficients[compose_permutations(right, left)] -= 1
    return {
        permutation: coefficient
        for permutation, coefficient in coefficients.items()
        if coefficient
    }


@lru_cache(maxsize=1)
def audit_local_commutator() -> LocalCommutatorCertificate:
    three_pair = unnormalized_commutator_histogram(3)
    four_pair = unnormalized_commutator_histogram(4)
    coefficient_counts = Counter(four_pair.values())
    touches_all = all(
        len(moved_pair_support(permutation)) == 4
        for permutation in four_pair
    )
    norm = sum(coefficient**2 for coefficient in four_pair.values())
    proved = (
        len(canonical_C_orbit()) == 8
        and len(canonical_D_orbit()) == 24
        and not three_pair
        and len(four_pair) == 768
        and coefficient_counts == {-1: 384, 1: 384}
        and norm == 768
        and touches_all
    )
    return LocalCommutatorCertificate(
        three_pair_C_orbit_size=len(C_orbit(3)),
        three_pair_D_orbit_size=len(D_orbit(3)),
        three_pair_commutator_nonzero_coefficient_count=len(three_pair),
        four_pair_C_orbit_size=len(C_orbit(4)),
        four_pair_D_orbit_size=len(D_orbit(4)),
        four_pair_commutator_nonzero_coefficient_count=len(four_pair),
        four_pair_positive_coefficient_count=coefficient_counts[1],
        four_pair_negative_coefficient_count=coefficient_counts[-1],
        four_pair_unnormalized_squared_norm=norm,
        every_nonzero_term_touches_all_four_pairs=touches_all,
        disjoint_global_support_by_four_pair_set=touches_all,
        local_decomposition_proved=proved,
        status=(
            "exact-four-pair-local-commutator-certificate"
            if proved
            else "local-commutator-certificate-failure"
        ),
    )


def normalized_commutator_squared_norm(half_degree: int) -> float:
    if half_degree < 4:
        return 0.0
    numerator = half_degree - 3
    denominator = (
        8
        * half_degree**3
        * (half_degree - 2)
        * (half_degree - 1) ** 3
    )
    return numerator / denominator


def hidden_involution(half_degree: int) -> Permutation:
    if half_degree < 1:
        raise ValueError("half_degree must be positive")
    return tuple(point ^ 1 for point in range(2 * half_degree))


@lru_cache(maxsize=None)
def hidden_even_correction_coefficient(half_degree: int) -> float:
    """Return the coefficient of ``h`` in the normalized ``X^*X``.

    For ``m>=7`` it vanishes by support: every term of ``X=[C_m,D_m]``
    moves six points, so a product of two terms cannot equal the involution
    moving all ``2m>12`` points.  The remaining ranks are exact controls.
    """

    if half_degree < 4:
        raise ValueError("half_degree must be at least four")
    if half_degree >= 7:
        return 0.0
    histogram = unnormalized_commutator_histogram(half_degree)
    involution = hidden_involution(half_degree)
    numerator = sum(
        coefficient
        * histogram.get(
            compose_permutations(permutation, involution),
            0,
        )
        for permutation, coefficient in histogram.items()
    )
    denominator = (
        len(C_orbit(half_degree)) ** 2
        * len(D_orbit(half_degree)) ** 2
    )
    return numerator / denominator


@lru_cache(maxsize=None)
def audit_plancherel_irreps(
    half_degree: int,
    *,
    tolerance: float = 1e-12,
) -> PlancherelFiniteControl:
    if half_degree not in (4, 5):
        raise ValueError("dense controls are intentionally limited to m=4,5")
    degree = 2 * half_degree
    group_order = math.factorial(degree)
    partitions = integer_partitions(degree)
    repeated_partitions: set[tuple[int, ...]] = set()
    detected_partitions: set[tuple[int, ...]] = set()
    expectation = 0.0
    detected_mass = 0.0
    for partition in partitions:
        dimension = hook_length_dimension(partition)
        _, _, _, repeated = exact_branching_commutant_dimension(
            partition,
            half_degree,
        )
        if repeated:
            repeated_partitions.add(partition)
        left, right = _average_matrices_for_sets(
            partition,
            [C_orbit(half_degree), D_orbit(half_degree)],
        )
        commutator = left @ right - right @ left
        energy = float(np.linalg.norm(commutator, "fro") ** 2 / dimension)
        weight = dimension**2 / group_order
        expectation += weight * energy
        if energy > tolerance:
            detected_partitions.add(partition)
            detected_mass += weight
    predicted = normalized_commutator_squared_norm(half_degree)
    exact_detection = detected_partitions == repeated_partitions
    residual = abs(expectation - predicted)
    return PlancherelFiniteControl(
        half_degree=half_degree,
        degree=degree,
        partition_count=len(partitions),
        repeated_branch_partition_count=len(repeated_partitions),
        nonzero_local_commutator_partition_count=len(detected_partitions),
        every_repeated_partition_detected=exact_detection,
        no_multiplicity_free_partition_detected=exact_detection,
        exact_plancherel_commutator_expectation=expectation,
        predicted_group_algebra_expectation=predicted,
        expectation_residual=residual,
        nonzero_commutator_plancherel_mass=detected_mass,
        finite_dense_control_only=True,
        status=(
            "local-pair-detects-every-repeated-finite-branch"
            if exact_detection and residual < 1e-12
            else "finite-local-commutator-control-failure"
        ),
    )


def fixed_defect_plancherel_mass_upper_bound(
    degree: int,
    defect: int,
) -> float:
    """Bound row-or-column defect at most ``defect`` under Plancherel.

    For ``lambda=(n-s,nu)``, choose the ``s`` entries below the first row and
    a standard tableau of ``nu``.  This gives ``d_lambda<=n^s``.  There are
    ``p(s)`` tails and the conjugate family gives the factor two.
    """

    tail_count = sum(len(integer_partitions(size)) for size in range(defect + 1))
    log_bound = (
        math.log(2 * tail_count)
        + 2 * defect * math.log(degree)
        - math.lgamma(degree + 1)
    )
    return min(1.0, math.exp(log_bound))


def natural_local_commutator_scaling_record(
    half_degree: int,
    *,
    fixed_defect: int = 4,
) -> NaturalLocalCommutatorScalingRecord:
    if half_degree < 4:
        raise ValueError("half_degree must be at least four")
    degree = 2 * half_degree
    delta = normalized_commutator_squared_norm(half_degree)
    plancherel_mass = delta / (8.0 - delta)
    candidates = involution_class_size(degree, half_degree)
    tv = 1 / (2 * math.sqrt(candidates))
    even_correction = hidden_even_correction_coefficient(half_degree)
    even_expectation = delta + even_correction
    source_mass = even_expectation / (8.0 - even_expectation)
    # p_H(lambda)=2 d_lambda r_lambda^+/|G| <= 2 d_lambda^2/|G|.
    fixed_defect_mass = 2 * fixed_defect_plancherel_mass_upper_bound(
        degree,
        fixed_defect,
    )
    growing_defect_mass = max(
        0.0,
        source_mass - fixed_defect_mass,
    )
    natural = source_mass > 0
    growing = growing_defect_mass > 0
    return NaturalLocalCommutatorScalingRecord(
        half_degree=half_degree,
        degree=degree,
        normalized_commutator_squared_norm=delta,
        commutator_energy_threshold=delta / 2,
        plancherel_good_mass_lower_bound=plancherel_mass,
        coordinate_source_plancherel_tv_upper_bound=tv,
        hidden_even_correction_coefficient=even_correction,
        hidden_even_commutator_expectation=even_expectation,
        coordinate_source_good_mass_lower_bound=source_mass,
        copy_space_variance_threshold=delta / 8,
        copy_space_spectral_diameter_lower_bound=math.sqrt(delta / 2),
        commutator_rank_fraction_lower_bound=delta / 8,
        fixed_defect_four_row_or_column_mass_upper_bound=fixed_defect_mass,
        growing_defect_source_good_mass_lower_bound=growing_defect_mass,
        natural_inverse_polynomial_mass_certified=natural,
        growing_defect_natural_mass_certified=growing,
        status=(
            "growing-defect-natural-local-noncommutativity-certified"
            if growing
            else (
                "natural-local-noncommutativity-certified"
                if natural
                else "finite-preasymptotic-TV-bound"
            )
        ),
    )


@lru_cache(maxsize=1)
def build_plancherel_local_commutant_report() -> PlancherelLocalCommutantReport:
    local = audit_local_commutator()
    finite = [audit_plancherel_irreps(value) for value in (4, 5)]
    scaling_half_degrees = (4, 5, 8, 10, 11, 17, 32, 64)
    scaling = [
        natural_local_commutator_scaling_record(value)
        for value in scaling_half_degrees
    ]
    finite_exact = all(
        row.every_repeated_partition_detected
        and row.no_multiplicity_free_partition_detected
        and row.expectation_residual < 1e-12
        for row in finite
    )
    asymptotic_natural = all(
        row.natural_inverse_polynomial_mass_certified
        for row in scaling
        if row.half_degree >= 4
    )
    growing_defect = all(
        row.growing_defect_natural_mass_certified
        for row in scaling
        if row.half_degree >= 11
    )
    theorem_verified = (
        local.local_decomposition_proved
        and finite_exact
        and asymptotic_natural
        and growing_defect
    )
    theorem = PlancherelLocalCommutantTheorem(
        observables=(
            "C_m is the full-pair-plus-single 3-cycle average; D_m is the three-pair path-matching average."
        ),
        local_cancellation=(
            "The three-pair commutator vanishes; each four-pair set contributes 768 orthogonal +/-1 coefficients."
        ),
        exact_group_algebra_norm=(
            "delta_m=(m-3)/[8 m^3 (m-2) (m-1)^3]=Theta(m^-6)."
        ),
        plancherel_transfer=(
            "Regular Fourier decomposition and the operator-norm bound four give mass at least delta_m/(8-delta_m) above energy delta_m/2."
        ),
        natural_source_transfer=(
            "Source-weighting by P_+=(I+rho(h))/2 changes the mean by coefficient_h(X^*X), which is exactly zero; the occupied even-space mean is delta_m."
        ),
        fixed_defect_exclusion=(
            "Row-or-column defect at most four has source mass at most 48(2m)^8/(2m)!, leaving growing-defect natural mass from m>=11."
        ),
        exact_all_rank_commutator_norm_proved=local.local_decomposition_proved,
        inverse_polynomial_plancherel_noncommutative_mass_proved=(
            local.local_decomposition_proved
        ),
        inverse_polynomial_natural_noncommutative_mass_proved=asymptotic_natural,
        growing_defect_natural_noncommutative_mass_proved=growing_defect,
        inverse_polynomial_copy_space_variance_proved=asymptotic_natural,
        inverse_polynomial_copy_space_spectral_diameter_proved=(
            asymptotic_natural
        ),
        all_repeated_branches_detected_by_this_pair_proved=False,
        inverse_polynomial_copy_space_eigenvalue_gap_proved=False,
        coherent_missing_label_transform_compiled=False,
        hidden_involution_detector_constructed=False,
        speedup_claim_allowed=False,
        theorem_verified=theorem_verified,
        status=(
            "bounded-support-noncommutativity-on-growing-defect-natural-mass-proved"
            if theorem_verified
            else "plancherel-local-commutator-certificate-failure"
        ),
    )
    return PlancherelLocalCommutantReport(
        created_at=utc_now(),
        theorem_contract={
            "group_pair": "S_(2m) >= C_2 wr S_m",
            "range": "every integer m>=4, with positive growing-defect source mass from m>=11",
            "access_model": (
                "Normalized polynomial-size K-conjugacy orbit averages in Young-basis Fourier blocks."
            ),
            "claim_boundary": (
                "Inverse-polynomial natural mass with noncommutative local action; not an eigenbasis transform or detector."
            ),
        },
        local_certificate=local,
        finite_controls=finite,
        scaling_records=scaling,
        theorem=theorem,
        proof_obligations=[
            {
                "id": "PO-HIDDEN-INVOLUTION-LOCAL-COMMUTATOR-GAP-DISTRIBUTION",
                "statement": (
                    "Bound copy-space eigenvalue gaps or local branching widths for C_m,D_m on the certified natural event."
                ),
                "resolved": False,
            },
            {
                "id": "PO-HIDDEN-INVOLUTION-LOCAL-CHARGE-HIERARCHY",
                "statement": (
                    "Construct a nested polynomial charge family that resolves exponentially large natural multiplicities with polynomial precision."
                ),
                "resolved": False,
            },
            {
                "id": "PO-HIDDEN-INVOLUTION-LOCAL-COMMUTATOR-SOURCE-CORRELATION",
                "statement": (
                    "Prove that the local copy-space labels correlate with the source-aware CS signal rather than merely resolving nuisance multiplicity."
                ),
                "resolved": False,
            },
        ],
        adversarial_audit=[
            {
                "challenge": "The commutator may be supported only on the solved fixed-defect families.",
                "answer": (
                    "No asymptotically: their total Plancherel mass is factorially smaller than the inverse-polynomial good-event lower bound."
                ),
                "resolved": True,
            },
            {
                "challenge": "A nonzero regular commutator could have exponentially rare irrep support.",
                "answer": (
                    "The integrand is bounded by four, forcing irrep mass at least delta_m/(8-delta_m)=Theta(m^-6)."
                ),
                "resolved": True,
            },
            {
                "challenge": "Plancherel relevance does not imply hidden-involution source relevance.",
                "answer": (
                    "Direct h-even projector weighting leaves the exact mean unchanged because coefficient_h(X^*X)=0."
                ),
                "resolved": True,
            },
            {
                "challenge": "Noncommutativity proves an efficient missing-label transform.",
                "answer": (
                    "It proves inverse-polynomial variance and spectral diameter for one local charge, but not minimum adjacent gaps, a hierarchical basis, normalization, or decoding."
                ),
                "resolved": True,
            },
        ],
        literature_links=[
            {
                "id": "DOI:10.1145/258533.258548",
                "role": "Efficient symmetric-group QFT and Young-basis representation controls.",
            },
            {
                "id": "arXiv:math/0302203",
                "role": "Partial-permutation filtrations and stable local-support algebra context.",
            },
            {
                "id": "arXiv:1212.5375",
                "role": "Hyperoctahedral partial-bijection locality and polynomial structure coefficients; double-coset rather than conjugation algebra."
            },
        ],
        headline_metrics={
            "exact_all_rank_local_commutator_norm_count": int(
                local.local_decomposition_proved
            ),
            "inverse_polynomial_plancherel_natural_mass_count": int(
                asymptotic_natural
            ),
            "growing_defect_natural_commutator_mass_count": int(growing_defect),
            "finite_repeated_branch_detection_control_count": len(finite),
            "finite_repeated_branch_detection_failure_count": sum(
                not row.every_repeated_partition_detected for row in finite
            ),
            "minimum_positive_natural_half_degree": min(
                row.half_degree
                for row in scaling
                if row.natural_inverse_polynomial_mass_certified
            ),
            "minimum_positive_growing_defect_half_degree": min(
                row.half_degree
                for row in scaling
                if row.growing_defect_natural_mass_certified
            ),
            "commutator_squared_norm_exponent": 6,
            "inverse_polynomial_gap_theorem_count": 0,
            "inverse_polynomial_copy_space_variance_count": int(
                asymptotic_natural
            ),
            "inverse_polynomial_copy_space_diameter_count": int(
                asymptotic_natural
            ),
            "coherent_missing_label_transform_count": 0,
            "hidden_involution_detector_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "exact_local_support_decomposition_proved": (
                local.local_decomposition_proved
            ),
            "bounded_support_reaches_growing_defect_natural_mass": growing_defect,
            "support_three_copy_space_variance_inverse_polynomial": (
                asymptotic_natural
            ),
            "support_three_copy_space_spectral_diameter_inverse_polynomial": (
                asymptotic_natural
            ),
            "all_repeated_branches_detected_by_local_pair": False,
            "inverse_polynomial_copy_space_eigenvalue_gap_proved": False,
            "hierarchical_missing_label_transform_compiled": False,
            "source_aware_normalized_recoupling_compiled": False,
            "hidden_involution_detector_constructed": False,
            "speedup_claim_allowed": False,
            "reason": (
                "Local noncommutative action now reaches natural mass, but Hilbert-Schmidt energy does not provide resolvable labels or source correlation."
            ),
        },
        status=theorem.status,
        summary=(
            "Proved that two support-at-most-four hyperoctahedral orbit averages act noncommutatively on inverse-polynomial, growing-defect natural Fourier mass."
        ),
        falsifiers_triggered=[
            "Bounded-support commutant action is not confined to polynomial-dimensional stable shapes.",
            "The finite support-threshold sequence does not imply an asymptotic support lower bound.",
            "Regular noncommutator energy alone does not imply a useful eigenbasis or hidden signal."
        ],
    )


def write_plancherel_local_commutant_report(
    output_path: Path = REPORT_PATH,
) -> dict[str, Any]:
    payload = asdict(build_plancherel_local_commutant_report())
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    return payload


def run_experiment(
    experiment_id: str = DEFAULT_EXPERIMENT_ID,
    candidate_id: str = DEFAULT_CANDIDATE_ID,
    write_registry: bool = True,
) -> dict[str, Any]:
    del experiment_id, candidate_id, write_registry
    return write_plancherel_local_commutant_report()


if __name__ == "__main__":
    print(json.dumps(run_experiment(), indent=2, sort_keys=True))

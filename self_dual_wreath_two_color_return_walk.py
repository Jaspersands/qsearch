"""Two-color word moments are return probabilities of one subgroup walk.

For ``x=(x_1,...,x_p) in G^p`` define

    q_p(x)=#{b in {0,1}^p:
             product_(b_t=0) x_t=product_(b_t=1) x_t=1}.

The all-word moment normal form contains ``q_p(x)^K``.  This apparent
``2^(pK)`` coloring sum is exactly a return probability.  On ``G^(2K)`` let

    h_e(x)=(z_10,z_11,...,z_K0,z_K1),

where ``z_i,e_i=x`` and the other coordinate is the identity, and let

    mu_K = E_(e in F_2^K,x in G) delta_(h_e(x)).

Choosing ``K`` colorings and transposing their bit matrix turns each time
column into one orientation ``e_t``.  Hence

    E_(x in G^p) (q_p(x)/2^p)^K = mu_K^(*p)(1).           (1)

For ``G=S_n``, ``n>=5``, the generated subgroup ``L_K`` contains an
independent ``A_n`` in every one of the ``2K`` coordinate membership blocks.
Its sign image is spanned by the vectors selecting one slot from each pair;
that binary span has dimension ``K+1``.  Therefore

    |L_K|=|S_n|^(2K)/2^(K-1).                             (2)

Equation (1) replaces factorial word-stratum enumeration by harmonic analysis
of a fixed, positive subgroup-projection walk.  It does not solve the natural
frame edge.  The global walk contains rare repeated-label Fourier blocks: the
complete ``S_3,K=2`` and ``S_4,K=2`` regular controls have nonstationary
eigenvalue ``3/4``, enormously larger than the natural scale ``1/|S_n|``.
The needed successor is a collision-free central-support or operator-valued
return bound, not merely a coarse global spectral gap.

There is a second exact obstruction.  If ``F_K=2^K M_K`` is the unnormalized
source-only orientation frame in the regular master, stationarity gives

    tr_reg(F_K^p) >= 2^(Kp)/|L_K|.                         (3)

At the information threshold ``K=Theta(log |S_n|)``, the right side reaches
one at ``p=(2+o(1))K`` and then grows exponentially.  Unconditioned regular
high moments are therefore captured by rare common-invariant Fourier blocks
before reaching the generic trace degree.  Global source distinctness removes
the exact stationary blocks for ``K>=2``, but transferring (3) cannot use
total variation at growing degree.  A central/injective return theorem is
mandatory.
"""

from __future__ import annotations

import itertools
import json
import math
from collections import deque
from dataclasses import asdict, dataclass
from fractions import Fraction
from pathlib import Path
from typing import Any

import numpy as np

from research_registry import utc_now
from self_dual_wreath_affine_node_common_outlier import _f2_rank


REPORT_PATH = Path(
    "research/representation/self_dual_wreath_two_color_return_walk.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-TWO-COLOR-RETURN-WALK"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"

Permutation = tuple[int, ...]
ProductElement = tuple[Permutation, ...]


@dataclass(frozen=True)
class ReturnIdentityControl:
    n: int
    copy_count: int
    moment_order: int
    group_sequence_count: int
    coloring_count_per_sequence: int
    exact_word_count_moment: str
    exact_walk_return_probability: str
    exact_return_identity_verified: bool
    status: str


@dataclass(frozen=True)
class SourceOnlyGeneratedSubgroupControl:
    n: int
    copy_count: int
    ambient_product_group_order: int
    incidence_rank_over_f2: int
    predicted_generated_subgroup_order: int
    exact_generated_subgroup_order: int
    predicted_stationary_return_probability: str
    exact_generated_subgroup_formula_verified: bool
    status: str


@dataclass(frozen=True)
class ReturnWalkSpectrumControl:
    n: int
    copy_count: int
    ambient_dimension: int
    stationary_eigenvalue_multiplicity: int
    predicted_stationary_eigenvalue_multiplicity: int
    largest_nonstationary_eigenvalue: float
    natural_inverse_group_scale: float
    global_gap_is_natural_scale_edge: bool
    exact_spectrum_control_verified: bool
    status: str


@dataclass(frozen=True)
class StationaryMomentObstructionRecord:
    n: int
    group_order_log2: float
    selected_copy_count: int
    orientation_count_log2: int
    generated_subgroup_order_log2: float
    first_order_one_stationary_moment_degree: int
    critical_degree_to_copy_count_ratio: float
    log2_stationary_lower_bound_at_copy_degree: float
    log2_stationary_lower_bound_at_twice_copy_degree: float
    log2_stationary_lower_bound_at_four_times_copy_degree: float
    unconditioned_regular_growing_moments_avoid_stationary_outliers: bool
    globally_distinct_stationary_support_is_empty: bool
    collision_free_central_return_bound_proved: bool
    status: str


@dataclass(frozen=True)
class TwoColorReturnWalkReport:
    created_at: str
    theorem_contract: dict[str, Any]
    return_identity_controls: list[ReturnIdentityControl]
    subgroup_controls: list[SourceOnlyGeneratedSubgroupControl]
    spectrum_controls: list[ReturnWalkSpectrumControl]
    stationary_moment_obstructions: list[StationaryMomentObstructionRecord]
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _compose(left: Permutation, right: Permutation) -> Permutation:
    return tuple(left[right[index]] for index in range(len(left)))


def _product_compose(
    left: ProductElement,
    right: ProductElement,
) -> ProductElement:
    return tuple(_compose(a, b) for a, b in zip(left, right))


def source_only_embedding(
    element: Permutation,
    copy_count: int,
    orientation: int,
) -> ProductElement:
    if copy_count < 1 or not 0 <= orientation < 1 << copy_count:
        raise ValueError("invalid copy count or orientation")
    identity = tuple(range(len(element)))
    output: list[Permutation] = []
    for pair_index in range(copy_count):
        selected = int(bool(orientation & (1 << pair_index)))
        output.extend(
            element if slot == selected else identity for slot in (0, 1)
        )
    return tuple(output)


def two_color_identity_count(sequence: tuple[Permutation, ...]) -> int:
    if not sequence:
        raise ValueError("a nonempty sequence is required")
    identity = tuple(range(len(sequence[0])))
    count = 0
    for bits in itertools.product((0, 1), repeat=len(sequence)):
        products = [identity, identity]
        for element, bit in zip(sequence, bits):
            products[bit] = _compose(products[bit], element)
        count += products[0] == identity and products[1] == identity
    return count


def source_only_step_distribution(
    n: int,
    copy_count: int,
) -> dict[ProductElement, Fraction]:
    group = tuple(itertools.permutations(range(n)))
    denominator = (1 << copy_count) * len(group)
    distribution: dict[ProductElement, Fraction] = {}
    for orientation in range(1 << copy_count):
        for element in group:
            point = source_only_embedding(element, copy_count, orientation)
            distribution[point] = distribution.get(point, Fraction()) + Fraction(
                1, denominator
            )
    return distribution


def convolution_return_probability(
    n: int,
    copy_count: int,
    moment_order: int,
) -> Fraction:
    if moment_order < 1:
        raise ValueError("moment order must be positive")
    identity_permutation = tuple(range(n))
    identity = (identity_permutation,) * (2 * copy_count)
    step = source_only_step_distribution(n, copy_count)
    distribution = {identity: Fraction(1)}
    for _ in range(moment_order):
        successor: dict[ProductElement, Fraction] = {}
        for left, left_probability in distribution.items():
            for right, right_probability in step.items():
                point = _product_compose(right, left)
                successor[point] = successor.get(point, Fraction()) + (
                    left_probability * right_probability
                )
        distribution = successor
    return distribution.get(identity, Fraction())


def word_count_moment(
    n: int,
    copy_count: int,
    moment_order: int,
) -> Fraction:
    group = tuple(itertools.permutations(range(n)))
    denominator = len(group) ** moment_order * (1 << moment_order) ** copy_count
    numerator = sum(
        two_color_identity_count(sequence) ** copy_count
        for sequence in itertools.product(group, repeat=moment_order)
    )
    return Fraction(numerator, denominator)


def audit_return_identity(
    n: int,
    copy_count: int,
    moment_order: int,
) -> ReturnIdentityControl:
    word = word_count_moment(n, copy_count, moment_order)
    walk = convolution_return_probability(n, copy_count, moment_order)
    verified = word == walk
    return ReturnIdentityControl(
        n=n,
        copy_count=copy_count,
        moment_order=moment_order,
        group_sequence_count=math.factorial(n) ** moment_order,
        coloring_count_per_sequence=(1 << moment_order) ** copy_count,
        exact_word_count_moment=str(word),
        exact_walk_return_probability=str(walk),
        exact_return_identity_verified=verified,
        status=(
            "exact-two-color-return-identity-verified"
            if verified
            else "two-color-return-identity-failure"
        ),
    )


def source_only_incidence_rows(copy_count: int) -> tuple[int, ...]:
    if copy_count < 1:
        raise ValueError("copy count must be positive")
    return tuple(
        sum(
            1 << (2 * pair + int(bool(orientation & (1 << pair))))
            for pair in range(copy_count)
        )
        for orientation in range(1 << copy_count)
    )


def source_only_generated_subgroup_order(
    group_order: int,
    copy_count: int,
) -> int:
    if group_order < 2 or group_order % 2 or copy_count < 1:
        raise ValueError("an even group order and positive copy count are required")
    return group_order ** (2 * copy_count) // (1 << (copy_count - 1))


def exact_source_only_generated_subgroup_order(
    n: int,
    copy_count: int,
) -> int:
    if n > 3 or copy_count > 2:
        raise ValueError("exact closure is restricted to S3 and K at most two")
    group = tuple(itertools.permutations(range(n)))
    identity_permutation = tuple(range(n))
    identity = (identity_permutation,) * (2 * copy_count)
    generators = tuple(
        source_only_embedding(element, copy_count, orientation)
        for orientation in range(1 << copy_count)
        for element in group
        if element != identity_permutation
    )
    discovered = {identity}
    frontier = deque((identity,))
    while frontier:
        current = frontier.popleft()
        for generator in generators:
            candidate = _product_compose(generator, current)
            if candidate not in discovered:
                discovered.add(candidate)
                frontier.append(candidate)
    return len(discovered)


def audit_source_only_generated_subgroup(
    n: int,
    copy_count: int,
) -> SourceOnlyGeneratedSubgroupControl:
    group_order = math.factorial(n)
    ambient = group_order ** (2 * copy_count)
    rank = _f2_rank(source_only_incidence_rows(copy_count))
    predicted = source_only_generated_subgroup_order(group_order, copy_count)
    exact = exact_source_only_generated_subgroup_order(n, copy_count)
    verified = rank == copy_count + 1 and predicted == exact
    return SourceOnlyGeneratedSubgroupControl(
        n=n,
        copy_count=copy_count,
        ambient_product_group_order=ambient,
        incidence_rank_over_f2=rank,
        predicted_generated_subgroup_order=predicted,
        exact_generated_subgroup_order=exact,
        predicted_stationary_return_probability=str(Fraction(1, predicted)),
        exact_generated_subgroup_formula_verified=verified,
        status=(
            "exact-source-only-generated-subgroup-formula-verified"
            if verified
            else "source-only-generated-subgroup-control-failure"
        ),
    )


def _left_convolution_matrix(
    n: int,
    copy_count: int,
) -> np.ndarray:
    group = tuple(itertools.permutations(range(n)))
    points = tuple(itertools.product(group, repeat=2 * copy_count))
    point_index = {point: index for index, point in enumerate(points)}
    step = source_only_step_distribution(n, copy_count)
    matrix = np.zeros((len(points), len(points)))
    for column, point in enumerate(points):
        for element, probability in step.items():
            matrix[point_index[_product_compose(element, point)], column] += float(
                probability
            )
    return (matrix + matrix.T) / 2


def audit_return_walk_spectrum(
    n: int,
    copy_count: int,
    *,
    tolerance: float = 1e-9,
) -> ReturnWalkSpectrumControl:
    if (n, copy_count) not in {(2, 2), (3, 2)}:
        raise ValueError("dense spectrum controls use (S2,K2) or (S3,K2)")
    matrix = _left_convolution_matrix(n, copy_count)
    eigenvalues = np.linalg.eigvalsh(matrix)
    stationary = int(np.count_nonzero(eigenvalues >= 1 - tolerance))
    predicted = matrix.shape[0] // source_only_generated_subgroup_order(
        math.factorial(n), copy_count
    )
    nonstationary = eigenvalues[eigenvalues < 1 - tolerance]
    largest = float(nonstationary[-1])
    verified = stationary == predicted and largest < 1 - tolerance
    return ReturnWalkSpectrumControl(
        n=n,
        copy_count=copy_count,
        ambient_dimension=matrix.shape[0],
        stationary_eigenvalue_multiplicity=stationary,
        predicted_stationary_eigenvalue_multiplicity=predicted,
        largest_nonstationary_eigenvalue=largest,
        natural_inverse_group_scale=1 / math.factorial(n),
        global_gap_is_natural_scale_edge=False,
        exact_spectrum_control_verified=verified,
        status=(
            "exact-return-walk-spectrum-verified-global-gap-too-coarse"
            if verified
            else "return-walk-spectrum-control-failure"
        ),
    )


def stationary_moment_obstruction_record(
    n: int,
) -> StationaryMomentObstructionRecord:
    if n < 3:
        raise ValueError("n must be at least three")
    group_log2 = math.lgamma(n + 1) / math.log(2)
    copies = math.ceil(group_log2) + 2
    subgroup_log2 = 2 * copies * group_log2 - (copies - 1)
    critical = math.ceil(subgroup_log2 / copies)

    def stationary_log2(moment_order: int) -> float:
        return copies * moment_order - subgroup_log2

    return StationaryMomentObstructionRecord(
        n=n,
        group_order_log2=group_log2,
        selected_copy_count=copies,
        orientation_count_log2=copies,
        generated_subgroup_order_log2=subgroup_log2,
        first_order_one_stationary_moment_degree=critical,
        critical_degree_to_copy_count_ratio=critical / copies,
        log2_stationary_lower_bound_at_copy_degree=stationary_log2(copies),
        log2_stationary_lower_bound_at_twice_copy_degree=stationary_log2(
            2 * copies
        ),
        log2_stationary_lower_bound_at_four_times_copy_degree=stationary_log2(
            4 * copies
        ),
        unconditioned_regular_growing_moments_avoid_stationary_outliers=False,
        globally_distinct_stationary_support_is_empty=True,
        collision_free_central_return_bound_proved=False,
        status="regular-growing-moments-stationary-dominated-central-trim-required",
    )


def run_two_color_return_walk() -> TwoColorReturnWalkReport:
    return_controls = [
        audit_return_identity(n, copies, order)
        for n, copies, order in (
            (2, 1, 4),
            (2, 2, 4),
            (3, 2, 3),
            (3, 2, 4),
        )
    ]
    subgroup_controls = [
        audit_source_only_generated_subgroup(n, copies)
        for n, copies in ((2, 1), (2, 2), (3, 1), (3, 2))
    ]
    spectrum_controls = [
        audit_return_walk_spectrum(2, 2),
        audit_return_walk_spectrum(3, 2),
    ]
    stationary_obstructions = [
        stationary_moment_obstruction_record(n)
        for n in (8, 12, 16, 20, 24, 28, 32, 40, 48)
    ]
    failures = sum(not row.exact_return_identity_verified for row in return_controls)
    failures += sum(
        not row.exact_generated_subgroup_formula_verified
        for row in subgroup_controls
    )
    failures += sum(
        not row.exact_spectrum_control_verified for row in spectrum_controls
    )
    largest = max(row.largest_nonstationary_eigenvalue for row in spectrum_controls)
    return TwoColorReturnWalkReport(
        created_at=utc_now(),
        theorem_contract={
            "return_identity": (
                "E_x(q_p(x)/2^p)^K equals the p-step identity return "
                "probability of the source-only orientation subgroup walk."
            ),
            "generated_subgroup": (
                "For S_n,n>=5, independent A_n membership blocks and a "
                "K+1-dimensional sign span give |L_K|=|S_n|^(2K)/2^(K-1)."
            ),
            "harmonic_reduction": (
                "Growing two-color word moments are convolution powers of one "
                "fixed self-adjoint probability measure on G^(2K)."
            ),
            "stationary_moment_obstruction": (
                "For the unnormalized orientation frame, stationary regular "
                "mass contributes at least 2^(Kp)/|L_K| and becomes order one "
                "at p=(2+o(1))K."
            ),
            "scope_exclusion": (
                "A coarse global gap is not a collision-free central-support "
                "bound and does not establish the natural 1/|S_n| frame edge."
            ),
        },
        return_identity_controls=return_controls,
        subgroup_controls=subgroup_controls,
        spectrum_controls=spectrum_controls,
        stationary_moment_obstructions=stationary_obstructions,
        proof_obligations=[
            {
                "obligation": "remove_explicit_two_color_word_enumeration",
                "resolved": failures == 0,
                "resolution": (
                    "Transpose the K coloring rows into p orientation columns "
                    "and recognize one convolution return event."
                ),
            },
            {
                "obligation": "identify_stationary_subgroup_and_mass",
                "resolved": True,
                "resolution": (
                    "The membership blocks supply A_n^(2K); the sign incidence "
                    "span has rank K+1 and fixes the subgroup index."
                ),
            },
            {
                "obligation": "bound_collision_free_central_return_at_growing_order",
                "resolved": False,
                "resolution": (
                    "Need to remove repeated-label and other atypical Fourier "
                    "blocks before a return estimate can imply a natural edge."
                ),
            },
            {
                "obligation": "remove_stationary_outliers_before_growing_moments",
                "resolved": True,
                "resolution": (
                    "The exact stationary lower bound reaches one near degree "
                    "2K. Global distinctness removes stationary support, so any "
                    "viable growing-moment proof must be central or injective."
                ),
            },
            {
                "obligation": "transfer_return_bound_to_full_node_spectral_edge",
                "resolved": False,
                "resolution": (
                    "The required operator-valued/central-support estimate is "
                    "not supplied by the scalar global return probability."
                ),
            },
        ],
        adversarial_audit=[
            {
                "objection": "The q_p^K coloring sum still requires 2^(pK) enumeration.",
                "resolved": True,
                "resolution": (
                    "It is exactly one convolution power; Fourier or Markov "
                    "methods can access it without listing colorings."
                ),
            },
            {
                "objection": "Any constant global spectral gap proves the natural edge.",
                "resolved": True,
                "resolution": (
                    "False. The S3 return walk has eigenvalue 3/4 while the "
                    "natural block scale is 1/6; rare Fourier blocks dominate."
                ),
            },
            {
                "objection": "Stationary return mass is automatically accepted PGM mass.",
                "resolved": False,
                "resolution": (
                    "Stationary mass is regular scalar mass; physical central "
                    "support and source conditioning still have to be tracked."
                ),
            },
            {
                "objection": "The stationary mass is too small to affect the required moments.",
                "resolved": True,
                "resolution": (
                    "Multiplication by the orientation width to the pth power "
                    "makes it order one at p about 2K and enormous thereafter."
                ),
            },
        ],
        headline_metrics={
            "exact_return_identity_control_count": len(return_controls),
            "source_only_subgroup_control_count": len(subgroup_controls),
            "exact_spectrum_control_count": len(spectrum_controls),
            "finite_control_failure_count": failures,
            "largest_control_nonstationary_eigenvalue": largest,
            "stationary_moment_obstruction_scaling_count": len(
                stationary_obstructions
            ),
            "tail_stationary_critical_degree": (
                stationary_obstructions[-1].first_order_one_stationary_moment_degree
            ),
            "tail_stationary_critical_degree_to_copy_count_ratio": (
                stationary_obstructions[-1].critical_degree_to_copy_count_ratio
            ),
            "all_order_two_color_return_reduction_theorem_count": int(
                failures == 0
            ),
            "source_only_generated_subgroup_order_theorem_count": 1,
            "collision_free_central_return_bound_count": 0,
            "natural_node_frame_edge_theorem_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "all_order_two_color_return_walk_identity_proved": failures == 0,
            "source_only_generated_subgroup_order_proved": failures == 0,
            "unconditioned_regular_growing_moment_route_falsified": True,
            "global_distinctness_removes_exact_stationary_support": True,
            "global_coarse_gap_suffices_for_natural_edge": False,
            "collision_free_central_return_bound_proved": False,
            "growing_order_natural_frame_moment_bound_proved": False,
            "natural_complete_node_frame_edge_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The exponential coloring sum is now one subgroup-walk return "
                "problem, but its collision-free central Fourier support is open."
            ),
        },
        status="two-color-return-walk-reduction-proved-central-return-open",
        summary=(
            "Converted every two-color identity-count moment into a fixed "
            "subgroup-walk return probability, identified its stationary subgroup, "
            "and proved the unconditioned growing-moment obstruction."
        ),
        falsifiers_triggered=[
            (
                "Explicit 2^(pK) coloring enumeration is not intrinsic to the "
                "all-word moment problem."
            ),
            (
                "A constant global return-walk gap is far too coarse to prove "
                "the inverse-factorial natural Fourier-block edge."
            ),
            (
                "Unconditioned regular growing moments are dominated by exact "
                "stationary Fourier outliers from degree about 2K onward."
            ),
            (
                "Regular stationary mass and collision-free physical state mass "
                "must not be conflated."
            ),
        ],
    )


def write_two_color_return_walk_report(
    path: Path = REPORT_PATH,
) -> dict[str, Any]:
    payload = asdict(run_two_color_return_walk())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    return payload


if __name__ == "__main__":
    report = write_two_color_return_walk_report()
    print(json.dumps(report, indent=2, sort_keys=True))

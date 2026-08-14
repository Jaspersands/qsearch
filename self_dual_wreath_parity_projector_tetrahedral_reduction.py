"""Parity-coset tetrahedral sums as signed invariant-projector overlaps.

For six irreducible representations ``lambda_1,...,lambda_6`` of ``S_n``
write ``d=product_i d_i``.  In the coefficient-axis convention used by the
physical recoupling modules, the six tetrahedral words are

    (gk, ghk, hk, g, h, k).

On ``V=V_1 tensor ... tensor V_6`` define the three diagonal actions

    U_g(s)=rho_1(s) tensor rho_2(s) tensor rho_4(s),
    U_h(s)=rho_2(s) tensor rho_3(s) tensor rho_5(s),
    U_k(s)=rho_1(s) tensor rho_2(s) tensor rho_3(s) tensor rho_6(s),

with identities on omitted factors.  Let ``P_a^+`` and ``P_a^-`` be the
trivial and sign isotypic projectors of action ``U_a`` and put

    J_a(x)=P_a^+ + (-1)^x P_a^-.

Expanding the three independent group averages gives the exact identity

    average_(parity(g,h,k)=x) product_i r_i(W_i)
      = Tr(J_g(x_g) J_h(x_h) J_k(x_k))/d.                 (1)

Consequently the unnormalized parity-coset partition function is

    F_x=(|S_n|/2)^3 Tr(J_g J_h J_k)/d.                    (2)

This identifies the missing cancellation as a signed three-projector angle,
equivalently a tetrahedral recoupling/6j quantity.  It is stronger than a
pointwise character formula because each complete group sum is performed
before an absolute value is taken.

The reduction also closes another tempting but inadequate route.  If every
``d_i>D``, the support rank of each signed projector obeys

    rank(P_a^+ + P_a^-)/d <= min_(i active in a) 2/d_i^2
                           <= 2/D^2.                      (3)

This follows from ``g(lambda,mu,nu)d_nu<=d_lambda d_mu`` for both the
trivial and sign multiplicities.  Schatten/rank bounds on (1) therefore give
only

    |F_x| <= (|S_n|/2)^3 min(1,2/D^2).                   (4)

At the canonical ``D=sqrt(n!)/(p(n)log_2(n!))``, (4) grows like
``(n!)^2(p(n)log n!)^2/4``.  Even the exact independent-Plancherel average
support fraction, ``2/n!``, leaves a vacuous absolute-overlap bound.  A valid
asymptotic proof must control the *relative angles* of all three invariant
subspaces (or the corresponding 6j contraction), not just their ranks,
dimensions, or marginal Plancherel laws.

This module proves the normal form and the rank-method no-go.  It does not
bound the canonical signed overlap, decide adaptive-syndrome survival, or
construct an algorithm.

There is a useful cancellation at the outer Plancherel level.  For six
non-self-conjugate sign orbits, the coarse weight is

    Q(O_1,...,O_6)=2^6 d^2/|S_n|^6.

Combining this with (2) gives the exact tuplewise energy identity

    Q(O_1,...,O_6) F_x(O_1,...,O_6)^2
      = Tr(J_g J_h J_k)^2.                                (5)

Thus the fully transpose-paired part of either canonical energy is literally
a sum of squared signed tetrahedral projector traces, with no hidden
dimension weights.  The all-``S_5`` high-dimensional paired control is
positive in both sector types; this is a finite falsifier of accidental
zero, not asymptotic survival evidence.
"""

from __future__ import annotations

import itertools
import json
import math
from dataclasses import asdict, dataclass
from functools import lru_cache
from pathlib import Path
from typing import Any

import numpy as np

from coset_jucys_murphy_label_transform import (
    adjacent_transposition_matrices,
    standard_young_tableaux,
)
from representation_obstruction import hook_length_dimension, integer_partitions
from research_registry import utc_now
from self_dual_wreath_character_moments import (
    compose_permutations,
    permutation_cycle_type,
)
from self_dual_wreath_character_triangle_barrier import partition_number
from self_dual_wreath_alternating_base_orbit_reduction import (
    coarse_alternating_plancherel_weights,
)
from self_dual_wreath_alternating_parity_coset_channel import (
    parity_coset_word_likelihood_arrays,
)
from symmetric_character import kronecker_coefficient, symmetric_character


REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_parity_projector_tetrahedral_reduction.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-PARITY-PROJECTOR-TETRAHEDRAL-REDUCTION"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"

Partition = tuple[int, ...]
Permutation = tuple[int, ...]
BitVector = tuple[int, int, int]


@dataclass(frozen=True)
class ParityProjectorControl:
    control_id: str
    n: int
    partitions: tuple[Partition, ...]
    parity: BitVector
    tensor_dimension: int
    direct_coset_average: float
    signed_projector_trace_average: float
    projector_trace_residual: float
    maximum_character_trace_residual: float
    maximum_isotypic_projector_residual: float
    active_support_rank_fractions: tuple[float, float, float]
    active_rank_upper_bounds: tuple[float, float, float]
    exact_signed_projector_normal_form_verified: bool
    status: str


@dataclass(frozen=True)
class ProjectorRankBarrierRecord:
    n: int
    group_order_log2: float
    canonical_dimension_threshold_log2: float
    rank_only_overlap_bound_log2: float
    rank_only_partition_function_bound_log2: float
    rank_only_seven_sector_energy_bound_log2: float
    exact_full_plancherel_signed_support_fraction: float
    rank_only_method_certifies_decay: bool
    status: str


@dataclass(frozen=True)
class FullyPairedTraceEnergyControl:
    n: int
    minimum_dimension_exclusive: int
    retained_nonself_orbit_count: int
    retained_orbit_tuple_count: int
    retained_coarse_product_mass: float
    face_parity: BitVector
    face_direct_energy: float
    face_sum_squared_projector_traces: float
    face_energy_residual: float
    face_nonzero_trace_count: int
    face_maximum_absolute_trace: float
    opposite_parity: BitVector
    opposite_direct_energy: float
    opposite_sum_squared_projector_traces: float
    opposite_energy_residual: float
    opposite_nonzero_trace_count: int
    opposite_maximum_absolute_trace: float
    exact_tuplewise_weight_cancellation_verified: bool
    finite_positive_signal_is_asymptotic_evidence: bool
    status: str


@dataclass(frozen=True)
class ParityProjectorTetrahedralReport:
    created_at: str
    theorem_contract: dict[str, Any]
    finite_controls: list[ParityProjectorControl]
    paired_trace_energy_controls: list[FullyPairedTraceEnergyControl]
    scaling_records: list[ProjectorRankBarrierRecord]
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _permutation_sign(permutation: Permutation) -> int:
    inversions = sum(
        permutation[left] > permutation[right]
        for left in range(len(permutation))
        for right in range(left + 1, len(permutation))
    )
    return -1 if inversions % 2 else 1


def _adjacent_permutation(n: int, index: int) -> Permutation:
    values = list(range(n))
    values[index], values[index + 1] = values[index + 1], values[index]
    return tuple(values)


@lru_cache(maxsize=None)
def young_irrep_matrices(partition: Partition) -> dict[Permutation, np.ndarray]:
    """Build every small-``n`` Young orthogonal matrix by a Cayley BFS."""

    n = sum(partition)
    dimension = len(standard_young_tableaux(partition))
    identity = tuple(range(n))
    generators = tuple(_adjacent_permutation(n, index) for index in range(n - 1))
    generator_matrices = adjacent_transposition_matrices(partition)
    matrices = {identity: np.eye(dimension)}
    pending = [identity]
    while pending:
        current = pending.pop()
        for generator, matrix in zip(generators, generator_matrices):
            neighbor = compose_permutations(current, generator)
            if neighbor not in matrices:
                matrices[neighbor] = matrices[current] @ matrix
                pending.append(neighbor)
    if len(matrices) != math.factorial(n):
        raise AssertionError("adjacent transpositions did not generate S_n")
    return matrices


def _tensor_action(
    partitions: tuple[Partition, ...],
    permutation: Permutation,
    active_factors: tuple[int, ...],
) -> np.ndarray:
    active = set(active_factors)
    factors = []
    for index, partition in enumerate(partitions):
        dimension = hook_length_dimension(partition)
        factors.append(
            young_irrep_matrices(partition)[permutation]
            if index in active
            else np.eye(dimension)
        )
    result = factors[0]
    for factor in factors[1:]:
        result = np.kron(result, factor)
    return result


def parity_isotypic_operators(
    partitions: tuple[Partition, ...],
    active_factors: tuple[int, ...],
) -> tuple[np.ndarray, np.ndarray]:
    if len(partitions) != 6 or len({sum(partition) for partition in partitions}) != 1:
        raise ValueError("six partitions of one n are required")
    n = sum(partitions[0])
    group = tuple(itertools.permutations(range(n)))
    shape = math.prod(hook_length_dimension(partition) for partition in partitions)
    trivial = np.zeros((shape, shape), dtype=float)
    sign = np.zeros_like(trivial)
    for permutation in group:
        action = _tensor_action(partitions, permutation, active_factors)
        trivial += action
        sign += _permutation_sign(permutation) * action
    return trivial / len(group), sign / len(group)


def signed_projector_coset_average(
    partitions: tuple[Partition, ...],
    parity: BitVector,
) -> tuple[float, tuple[float, float, float], float]:
    if parity not in tuple(itertools.product((0, 1), repeat=3)):
        raise ValueError("parity must lie in F_2^3")
    active_sets = ((0, 1, 3), (1, 2, 4), (0, 1, 2, 5))
    signed = []
    rank_fractions = []
    residual = 0.0
    tensor_dimension = math.prod(
        hook_length_dimension(partition) for partition in partitions
    )
    for bit, active in zip(parity, active_sets):
        trivial, sign = parity_isotypic_operators(partitions, active)
        identity_residual = max(
            np.linalg.norm(trivial @ trivial - trivial, ord=2),
            np.linalg.norm(sign @ sign - sign, ord=2),
            np.linalg.norm(trivial @ sign, ord=2),
            np.linalg.norm(trivial - trivial.T, ord=2),
            np.linalg.norm(sign - sign.T, ord=2),
        )
        residual = max(residual, float(identity_residual))
        signed.append(trivial + ((-1) ** bit) * sign)
        rank_fractions.append(
            float(np.trace(trivial + sign).real) / tensor_dimension
        )
    value = float(np.trace(signed[0] @ signed[1] @ signed[2]).real) / tensor_dimension
    return value, tuple(rank_fractions), residual


def direct_parity_coset_average(
    partitions: tuple[Partition, ...],
    parity: BitVector,
) -> float:
    if len(partitions) != 6 or len({sum(partition) for partition in partitions}) != 1:
        raise ValueError("six partitions of one n are required")
    n = sum(partitions[0])
    group = tuple(itertools.permutations(range(n)))
    selected = {
        bit: tuple(
            permutation
            for permutation in group
            if (_permutation_sign(permutation) < 0) == bool(bit)
        )
        for bit in (0, 1)
    }
    dimensions = tuple(hook_length_dimension(partition) for partition in partitions)
    total = 0.0
    for g in selected[parity[0]]:
        for h in selected[parity[1]]:
            gh = compose_permutations(g, h)
            for k in selected[parity[2]]:
                words = (
                    compose_permutations(g, k),
                    compose_permutations(gh, k),
                    compose_permutations(h, k),
                    g,
                    h,
                    k,
                )
                total += math.prod(
                    symmetric_character(partition, permutation_cycle_type(word))
                    / dimension
                    for partition, dimension, word in zip(
                        partitions,
                        dimensions,
                        words,
                    )
                )
    return total / math.prod(len(selected[bit]) for bit in parity)


def active_rank_fraction_upper_bounds(
    partitions: tuple[Partition, ...],
) -> tuple[float, float, float]:
    active_sets = ((0, 1, 3), (1, 2, 4), (0, 1, 2, 5))
    dimensions = tuple(hook_length_dimension(partition) for partition in partitions)
    return tuple(
        min(1.0, min(2.0 / dimensions[index] ** 2 for index in active))
        for active in active_sets
    )


def audit_fully_paired_trace_energy(
    n: int,
    minimum_dimension_exclusive: int,
    *,
    tolerance: float = 1e-10,
) -> FullyPairedTraceEnergyControl:
    """Verify equation (5) over every retained non-self-conjugate tuple."""

    if not 2 <= n <= 5 or minimum_dimension_exclusive < 0:
        raise ValueError("exact paired controls require 2<=n<=5 and a valid trim")
    orbits, arrays = parity_coset_word_likelihood_arrays(n)
    weighted_orbits, weights = coarse_alternating_plancherel_weights(n)
    if orbits != weighted_orbits:
        raise AssertionError("sign-orbit order mismatch")
    retained = tuple(
        index
        for index, orbit in enumerate(orbits)
        if len(orbit) == 2
        and hook_length_dimension(orbit[0]) > minimum_dimension_exclusive
    )
    tuples = tuple(itertools.product(retained, repeat=6))
    order = math.factorial(n)

    def sector(parity: BitVector) -> tuple[float, float, int, float]:
        direct = 0.0
        traces = []
        for indices in tuples:
            dimensions = tuple(
                hook_length_dimension(orbits[index][0]) for index in indices
            )
            value = float(arrays[parity][indices])
            coarse_weight = math.prod(weights[orbits[index]] for index in indices)
            trace = value * math.prod(dimensions) / (order / 2.0) ** 3
            direct += coarse_weight * value * value
            traces.append(trace)
        return (
            direct,
            sum(value * value for value in traces),
            sum(abs(value) > tolerance for value in traces),
            max((abs(value) for value in traces), default=0.0),
        )

    face_parity = (1, 0, 0)
    opposite_parity = (0, 0, 1)
    face_direct, face_trace, face_nonzero, face_maximum = sector(face_parity)
    opposite_direct, opposite_trace, opposite_nonzero, opposite_maximum = sector(
        opposite_parity
    )
    face_residual = abs(face_direct - face_trace)
    opposite_residual = abs(opposite_direct - opposite_trace)
    exact = max(face_residual, opposite_residual) <= tolerance
    retained_mass = sum(weights[orbits[index]] for index in retained) ** 6
    return FullyPairedTraceEnergyControl(
        n=n,
        minimum_dimension_exclusive=minimum_dimension_exclusive,
        retained_nonself_orbit_count=len(retained),
        retained_orbit_tuple_count=len(tuples),
        retained_coarse_product_mass=retained_mass,
        face_parity=face_parity,
        face_direct_energy=face_direct,
        face_sum_squared_projector_traces=face_trace,
        face_energy_residual=face_residual,
        face_nonzero_trace_count=face_nonzero,
        face_maximum_absolute_trace=face_maximum,
        opposite_parity=opposite_parity,
        opposite_direct_energy=opposite_direct,
        opposite_sum_squared_projector_traces=opposite_trace,
        opposite_energy_residual=opposite_residual,
        opposite_nonzero_trace_count=opposite_nonzero,
        opposite_maximum_absolute_trace=opposite_maximum,
        exact_tuplewise_weight_cancellation_verified=exact,
        finite_positive_signal_is_asymptotic_evidence=False,
        status=(
            "fully-paired-energy-is-sum-of-squared-projector-traces"
            if exact
            else "paired-projector-trace-energy-control-failure"
        ),
    )


def _maximum_character_trace_residual(partitions: tuple[Partition, ...]) -> float:
    n = sum(partitions[0])
    group = tuple(itertools.permutations(range(n)))
    return max(
        abs(
            float(np.trace(young_irrep_matrices(partition)[permutation]))
            - symmetric_character(partition, permutation_cycle_type(permutation))
        )
        for partition in set(partitions)
        for permutation in group
    )


def audit_parity_projector_control(
    control_id: str,
    partitions: tuple[Partition, ...],
    parity: BitVector,
    *,
    tolerance: float = 1e-8,
) -> ParityProjectorControl:
    direct = direct_parity_coset_average(partitions, parity)
    projected, ranks, projector_residual = signed_projector_coset_average(
        partitions,
        parity,
    )
    bounds = active_rank_fraction_upper_bounds(partitions)
    trace_residual = _maximum_character_trace_residual(partitions)
    identity_residual = abs(direct - projected)
    verified = bool(
        identity_residual <= tolerance
        and trace_residual <= tolerance
        and projector_residual <= tolerance
        and all(rank <= bound + tolerance for rank, bound in zip(ranks, bounds))
    )
    return ParityProjectorControl(
        control_id=control_id,
        n=sum(partitions[0]),
        partitions=partitions,
        parity=parity,
        tensor_dimension=math.prod(
            hook_length_dimension(partition) for partition in partitions
        ),
        direct_coset_average=direct,
        signed_projector_trace_average=projected,
        projector_trace_residual=identity_residual,
        maximum_character_trace_residual=trace_residual,
        maximum_isotypic_projector_residual=projector_residual,
        active_support_rank_fractions=ranks,
        active_rank_upper_bounds=bounds,
        exact_signed_projector_normal_form_verified=verified,
        status=(
            "exact-parity-coset-signed-projector-normal-form"
            if verified
            else "parity-projector-normal-form-control-failure"
        ),
    )


def full_plancherel_signed_support_fraction(n: int) -> float:
    """Evaluate the exact ``2/|S_n|`` rank-fraction identity."""

    if n < 2:
        raise ValueError("n must be at least two")
    partitions = tuple(integer_partitions(n))
    order = math.factorial(n)
    dimensions = {partition: hook_length_dimension(partition) for partition in partitions}
    numerator = 0.0
    for left in partitions:
        for right in partitions:
            for target in partitions:
                multiplicity = kronecker_coefficient(left, right, target)
                sign_multiplicity = kronecker_coefficient(
                    left,
                    right,
                    tuple(value for value in _transpose_partition(target)),
                )
                weight = (
                    dimensions[left] ** 2
                    * dimensions[right] ** 2
                    * dimensions[target] ** 2
                    / order**3
                )
                numerator += weight * (
                    (multiplicity + sign_multiplicity)
                    / (
                        dimensions[left]
                        * dimensions[right]
                        * dimensions[target]
                    )
                )
    return numerator


def _transpose_partition(partition: Partition) -> Partition:
    return tuple(
        sum(row > column for row in partition)
        for column in range(max(partition))
    )


def projector_rank_barrier_record(n: int) -> ProjectorRankBarrierRecord:
    if n < 3:
        raise ValueError("n must be at least three")
    log_order = math.lgamma(n + 1) / math.log(2.0)
    normalizer = partition_number(n) * log_order
    continuous_log_dimension = 0.5 * log_order - math.log2(normalizer)
    overlap_log = min(0.0, 1.0 - 2.0 * continuous_log_dimension)
    partition_log = 3.0 * (log_order - 1.0) + overlap_log
    energy_log = math.log2(7.0) + 2.0 * partition_log
    return ProjectorRankBarrierRecord(
        n=n,
        group_order_log2=log_order,
        canonical_dimension_threshold_log2=continuous_log_dimension,
        rank_only_overlap_bound_log2=overlap_log,
        rank_only_partition_function_bound_log2=partition_log,
        rank_only_seven_sector_energy_bound_log2=energy_log,
        exact_full_plancherel_signed_support_fraction=2.0 / math.factorial(n),
        rank_only_method_certifies_decay=False,
        status="invariant-projector-rank-bound-asymptotically-vacuous",
    )


def run_parity_projector_tetrahedral_reduction(
) -> ParityProjectorTetrahedralReport:
    standard = (2, 1)
    trivial3 = (3,)
    sign3 = (1, 1, 1)
    controls = [
        audit_parity_projector_control(
            "S3-ALL-STANDARD-EVEN-COSET",
            (standard,) * 6,
            (0, 0, 0),
        ),
        audit_parity_projector_control(
            "S3-ALL-STANDARD-FACE-COSET",
            (standard,) * 6,
            (1, 0, 0),
        ),
        audit_parity_projector_control(
            "S3-MIXED-OPPOSITE-COSET",
            (standard, trivial3, standard, sign3, standard, standard),
            (0, 0, 1),
        ),
    ]
    paired_controls = [
        audit_fully_paired_trace_energy(4, 1),
        audit_fully_paired_trace_energy(5, 1),
    ]
    scaling = [
        projector_rank_barrier_record(n)
        for n in (10, 16, 24, 32, 50, 75, 100)
    ]
    failures = sum(
        not control.exact_signed_projector_normal_form_verified
        for control in controls
    )
    failures += sum(
        not control.exact_tuplewise_weight_cancellation_verified
        for control in paired_controls
    )
    finite_plancherel_residual = max(
        abs(full_plancherel_signed_support_fraction(n) - 2.0 / math.factorial(n))
        for n in (2, 3, 4, 5)
    )
    verified = failures == 0 and finite_plancherel_residual <= 1e-12
    tail = scaling[-1]
    return ParityProjectorTetrahedralReport(
        created_at=utc_now(),
        theorem_contract={
            "signed_isotypic_projectors": (
                "J_a(x)=P_a(triv)+(-1)^x P_a(sign) for the g, h, and k "
                "diagonal tensor actions on coefficient axes ordered "
                "(gk,ghk,hk,g,h,k)."
            ),
            "exact_coset_normal_form": (
                "average_(parity(g,h,k)=x) product_i r_i(W_i)="
                "Tr(J_g J_h J_k)/product_i d_i."
            ),
            "unnormalized_partition_function": (
                "F_x=(|S_n|/2)^3 Tr(J_g J_h J_k)/product_i d_i."
            ),
            "rank_bound": (
                "rank supp(J_a)/d_total<=min_(active i)2/d_i^2."
            ),
            "plancherel_rank_identity": (
                "For three independent full Plancherel labels, the expected "
                "trivial-plus-sign support fraction is exactly 2/|S_n|."
            ),
            "fully_paired_energy": (
                "For six non-self-conjugate sign orbits, Q(O)F_x(O)^2="
                "Tr(J_g J_h J_k)^2 tuple by tuple."
            ),
            "methodological_no_go": (
                "Projector ranks, dimensions, and marginal Plancherel laws do not "
                "control the signed triple overlap at the required |S_n|^-3 scale."
            ),
            "scope": (
                "The remaining object is a relative-angle/6j contraction; no "
                "canonical decay, survival, algorithm, or speedup is proved."
            ),
        },
        finite_controls=controls,
        paired_trace_energy_controls=paired_controls,
        scaling_records=scaling,
        proof_obligations=[
            {
                "obligation": "derive_exact_parity_coset_invariant_projector_normal_form",
                "resolved": verified,
                "resolution": (
                    "Three complete parity-restricted group averages are the signed "
                    "trivial/sign isotypic operators of the overlapping tensor actions."
                ),
            },
            {
                "obligation": "test_projector_rank_only_route_at_canonical_trim",
                "resolved": verified,
                "resolution": (
                    "Kronecker dimension bounds leave a growing factorial upper bound; "
                    "the exact Plancherel mean rank is also insufficient."
                ),
            },
            {
                "obligation": "remove_outer_plancherel_weights_on_paired_sector",
                "resolved": verified,
                "resolution": (
                    "The six factors 2d_i^2/n! cancel the squared normalization "
                    "of F_x exactly, leaving one squared signed projector trace."
                ),
            },
            {
                "obligation": "bound_canonical_signed_three_projector_overlap",
                "resolved": False,
                "resolution": (
                    "Prove an L2 overlap estimate at little-o(|S_n|^-3), separately "
                    "for one face and one opposite-complement parity sector."
                ),
            },
            {
                "obligation": "connect_overlap_to_positive_mass_adaptive_information",
                "resolved": False,
                "resolution": (
                    "Use the denominator-free trim transfer only after the two signed "
                    "overlap energies are controlled."
                ),
            },
        ],
        adversarial_audit=[
            {
                "objection": "A parity coset average is not an invariant projector.",
                "resolved": True,
                "resolution": (
                    "Its normalized indicator is 1+(-1)^x sign, giving the exact "
                    "difference of the trivial and sign isotypic projectors."
                ),
            },
            {
                "objection": "Near-maximal irrep dimensions force the overlap small enough.",
                "resolved": True,
                "resolution": (
                    "The best dimension-only support-rank bound misses the required "
                    "scale by factorial powers at the canonical threshold."
                ),
            },
            {
                "objection": "Expected Plancherel projector rank supplies the missing angle.",
                "resolved": True,
                "resolution": (
                    "The exact mean support fraction is 2/n!, but the partition function "
                    "has prefactor (n!/2)^3; two further powers require relative-angle cancellation."
                ),
            },
            {
                "objection": "The signed-projector identity proves adaptive decoupling.",
                "resolved": False,
                "resolution": (
                    "It isolates the needed 6j overlap but supplies no asymptotic angle estimate."
                ),
            },
        ],
        headline_metrics={
            "signed_projector_normal_form_theorem_count": int(verified),
            "projector_rank_method_no_go_theorem_count": int(verified),
            "full_plancherel_signed_support_identity_count": int(verified),
            "finite_control_count": len(controls),
            "paired_trace_energy_control_count": len(paired_controls),
            "finite_control_failure_count": failures,
            "maximum_finite_projector_trace_residual": max(
                control.projector_trace_residual for control in controls
            ),
            "maximum_finite_plancherel_rank_identity_residual": (
                finite_plancherel_residual
            ),
            "maximum_paired_trace_energy_residual": max(
                max(control.face_energy_residual, control.opposite_energy_residual)
                for control in paired_controls
            ),
            "S5_high_dimensional_paired_face_energy": (
                paired_controls[-1].face_direct_energy
            ),
            "S5_high_dimensional_paired_opposite_energy": (
                paired_controls[-1].opposite_direct_energy
            ),
            "n100_rank_only_energy_bound_log2": (
                tail.rank_only_seven_sector_energy_bound_log2
            ),
            "canonical_signed_overlap_bound_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "parity_coset_signed_projector_normal_form_proved": verified,
            "fully_paired_energy_is_squared_projector_trace_sum": verified,
            "projector_rank_only_route_eliminated": verified,
            "relative_6j_angle_estimate_required": True,
            "canonical_face_energy_vanishes_proved": False,
            "canonical_opposite_energy_vanishes_proved": False,
            "canonical_adaptive_syndrome_survives_proved": False,
            "classical_separation_proved": False,
            "algorithm_claim_allowed": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The exact target is now a signed three-projector/6j overlap, but "
                "ranks and marginal laws provably do not estimate its relative angles."
            ),
        },
        status=(
            "adaptive-parity-energy-reduced-to-signed-three-projector-angle"
            if verified
            else "parity-projector-reduction-control-failure"
        ),
        summary=(
            "Converted each adaptive parity-coset partition function into an exact "
            "signed invariant-projector overlap and eliminated rank-only estimates."
        ),
        falsifiers_triggered=[
            "Parity restriction creates trivial/sign projector differences, not an ordinary positive projector.",
            "Near-maximal dimensions alone miss the required tetrahedral overlap scale by factorial powers.",
            "The exact 2/n! Plancherel support fraction is still only marginal information.",
            "The positive S5 fully paired trace energies are finite controls, not asymptotic survival evidence.",
            "A valid next proof must control relative projector angles or equivalent 6j cancellation.",
        ],
    )


def write_parity_projector_tetrahedral_reduction_report(
    path: Path = REPORT_PATH,
) -> dict[str, Any]:
    payload = asdict(run_parity_projector_tetrahedral_reduction())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    return payload


if __name__ == "__main__":
    result = write_parity_projector_tetrahedral_reduction_report()
    print(json.dumps(result["headline_metrics"], indent=2, sort_keys=True))

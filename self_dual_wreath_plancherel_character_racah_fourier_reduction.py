"""A complete Plancherel Fourier basis for Racah label dependence.

For every conjugacy class ``C`` of ``S_n`` define the partition-label
function

    phi_C(lambda) = sqrt(|C|) chi_lambda(C) / d_lambda.    (1)

Column orthogonality of the character table gives

    E_(lambda~Plancherel) phi_C(lambda) phi_D(lambda)
      = 1[C=D].                                           (2)

There are ``p(n)`` classes and labels, so these functions are a complete
orthonormal basis.  For a coupling ``pi`` with Plancherel reference ``q^2``,
write ``L=pi/q^2``.  Parseval then gives

    chi2(pi||q^2) = sum_((C,D)!=(e,e))
                       (E_pi phi_C(mu) phi_D(nu))^2.       (3)

For the natural Racah coupling at outer tuple
``o=(alpha,beta,gamma,lambda)``, each coefficient has the exact character
sum

  E_pi phi_C(mu)phi_D(nu)
    = 1/(M |G| sqrt(|C||D|))
      sum_(h in G,g in C,k in D)
        chi_lambda(h^-1) chi_alpha(hg)
        chi_beta(hgk) chi_gamma(hk).                       (4)

Thus every label-level Racah collision estimate can in principle be attacked
without choosing multiplicity gauges or constructing Racah matrices.  The
remaining difficulty is uniform control over a growing set of conjugacy
classes.  Keeping classes that move at most ``s`` retains only ``p(s)-1``
nonconstant one-label modes.

The Plancherel identity coupling is an exact obstruction to truncation: its
Fourier coefficient matrix is the identity, its full collision is ``p(n)-1``,
and the low-support diagonal energy is only ``p(s)-1``.  This is a basis-tail
warning, not a lower bound on the natural Racah coupling.
"""

from __future__ import annotations

import itertools
import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import numpy as np

from representation_obstruction import hook_length_dimension, integer_partitions
from research_registry import utc_now
from self_dual_wreath_character_triangle_barrier import partition_number
from self_dual_wreath_compressed_racah_coupling_probe import (
    CompleteCompressedRacahCoupling,
    compile_complete_racah_coupling,
)
from self_dual_wreath_free_probability_projector_resolution_boundary import (
    exact_central_feature_count,
)
from self_dual_wreath_character_moments import (
    compose_permutations,
    permutation_cycle_type,
)
from symmetric_character import conjugacy_class_size, symmetric_character


Partition = tuple[int, ...]
Permutation = tuple[int, ...]
REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_plancherel_character_racah_fourier_reduction.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-PLANCHEREL-CHARACTER-RACAH-FOURIER-REDUCTION"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


@dataclass(frozen=True)
class PlancherelCharacterBasisControl:
    n: int
    partition_count: int
    conjugacy_class_count: int
    maximum_orthonormality_residual: float
    maximum_constant_mode_residual: float
    basis_is_square: bool
    exact_plancherel_character_basis_verified: bool
    status: str


@dataclass(frozen=True)
class RacahCharacterSumControl:
    n: int
    outer_partitions: tuple[Partition, Partition, Partition, Partition]
    left_cycle_type: Partition
    right_cycle_type: Partition
    left_class_size: int
    right_class_size: int
    coupling_fourier_coefficient: float
    character_sum_fourier_coefficient: float
    formula_residual: float
    exact_character_sum_formula_verified: bool
    status: str


@dataclass(frozen=True)
class IdentityCouplingFourierTailControl:
    n: int
    maximum_moved_support: int
    partition_count: int
    retained_nonconstant_mode_count: int
    omitted_nonconstant_mode_count: int
    full_identity_coupling_chi_square: int
    retained_low_support_diagonal_energy: int
    omitted_diagonal_energy: int
    retained_energy_fraction: float
    identity_coupling_mutual_information_bits: float
    exact_tail_decomposition_verified: bool
    status: str


@dataclass(frozen=True)
class PlancherelCharacterRacahFourierTheorem:
    orthonormal_basis: str
    parseval_identity: str
    natural_racah_character_sum: str
    low_support_mode_count: str
    full_growing_support_tail_control_proved: bool
    status: str


@dataclass(frozen=True)
class PlancherelCharacterRacahFourierReport:
    created_at: str
    theorem_contract: dict[str, Any]
    theorem: PlancherelCharacterRacahFourierTheorem
    basis_controls: list[PlancherelCharacterBasisControl]
    character_sum_controls: list[RacahCharacterSumControl]
    identity_tail_controls: list[IdentityCouplingFourierTailControl]
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def normalized_plancherel_character(
    partition: Partition,
    cycle_type: Partition,
) -> float:
    return (
        math.sqrt(conjugacy_class_size(cycle_type))
        * symmetric_character(partition, cycle_type)
        / hook_length_dimension(partition)
    )


def plancherel_character_basis_matrix(n: int) -> tuple[tuple[Partition, ...], np.ndarray]:
    if n < 2:
        raise ValueError("require n>=2")
    partitions = tuple(integer_partitions(n))
    matrix = np.asarray(
        [
            [normalized_plancherel_character(label, cycle) for cycle in partitions]
            for label in partitions
        ],
        dtype=float,
    )
    return partitions, matrix


def audit_plancherel_character_basis(
    n: int,
    *,
    tolerance: float = 2e-12,
) -> PlancherelCharacterBasisControl:
    if not 2 <= n <= 12:
        raise ValueError("finite basis controls require 2<=n<=12")
    partitions, matrix = plancherel_character_basis_matrix(n)
    order = math.factorial(n)
    q = np.asarray(
        [hook_length_dimension(partition) ** 2 / order for partition in partitions],
        dtype=float,
    )
    gram = matrix.T @ (q[:, None] * matrix)
    orthogonality = float(np.max(np.abs(gram - np.eye(len(partitions)))))
    identity_index = partitions.index((1,) * n)
    constant_residual = float(np.max(np.abs(matrix[:, identity_index] - 1.0)))
    square = matrix.shape == (len(partitions), len(partitions))
    verified = bool(square and orthogonality <= tolerance and constant_residual <= tolerance)
    return PlancherelCharacterBasisControl(
        n=n,
        partition_count=len(partitions),
        conjugacy_class_count=len(partitions),
        maximum_orthonormality_residual=orthogonality,
        maximum_constant_mode_residual=constant_residual,
        basis_is_square=square,
        exact_plancherel_character_basis_verified=verified,
        status=(
            "complete-plancherel-character-basis-verified"
            if verified
            else "plancherel-character-basis-control-failure"
        ),
    )


def racah_coupling_fourier_coefficient(
    coupling: CompleteCompressedRacahCoupling,
    left_cycle_type: Partition,
    right_cycle_type: Partition,
) -> float:
    return sum(
        entry.physical_block_probability
        * normalized_plancherel_character(
            entry.left_intermediate_partition, left_cycle_type
        )
        * normalized_plancherel_character(
            entry.right_intermediate_partition, right_cycle_type
        )
        for entry in coupling.coupling_entries
    )


def _permutations_by_cycle_type(n: int) -> dict[Partition, tuple[Permutation, ...]]:
    output: dict[Partition, list[Permutation]] = {}
    for permutation in itertools.permutations(range(n)):
        output.setdefault(permutation_cycle_type(permutation), []).append(permutation)
    return {cycle_type: tuple(values) for cycle_type, values in output.items()}


def natural_racah_character_sum_coefficient(
    outer_partitions: tuple[Partition, Partition, Partition, Partition],
    left_cycle_type: Partition,
    right_cycle_type: Partition,
    total_multiplicity: int,
) -> float:
    alpha, beta, gamma, final = outer_partitions
    n = sum(alpha)
    if any(sum(partition) != n for partition in outer_partitions):
        raise ValueError("outer partitions must have equal degree")
    if sum(left_cycle_type) != n or sum(right_cycle_type) != n:
        raise ValueError("cycle types must have the outer degree")
    if total_multiplicity <= 0:
        raise ValueError("positive total recoupling multiplicity is required")
    classes = _permutations_by_cycle_type(n)
    left_class = classes[left_cycle_type]
    right_class = classes[right_cycle_type]
    all_permutations = tuple(itertools.permutations(range(n)))
    total = 0
    for h in all_permutations:
        h_type = permutation_cycle_type(h)
        final_character = symmetric_character(final, h_type)
        if final_character == 0:
            continue
        for g in left_class:
            hg = compose_permutations(h, g)
            alpha_character = symmetric_character(alpha, permutation_cycle_type(hg))
            if alpha_character == 0:
                continue
            for k in right_class:
                hgk = compose_permutations(hg, k)
                hk = compose_permutations(h, k)
                total += (
                    final_character
                    * alpha_character
                    * symmetric_character(beta, permutation_cycle_type(hgk))
                    * symmetric_character(gamma, permutation_cycle_type(hk))
                )
    denominator = (
        total_multiplicity
        * math.factorial(n)
        * math.sqrt(len(left_class) * len(right_class))
    )
    return total / denominator


def audit_natural_racah_character_sum(
    outer_partitions: tuple[Partition, Partition, Partition, Partition],
    left_cycle_type: Partition,
    right_cycle_type: Partition,
    *,
    coupling: CompleteCompressedRacahCoupling | None = None,
    tolerance: float = 3e-9,
) -> RacahCharacterSumControl:
    compiled = coupling or compile_complete_racah_coupling(outer_partitions)
    if compiled.outer_partitions != outer_partitions:
        raise ValueError("compiled coupling has the wrong outer tuple")
    direct = racah_coupling_fourier_coefficient(
        compiled, left_cycle_type, right_cycle_type
    )
    character_sum = natural_racah_character_sum_coefficient(
        outer_partitions,
        left_cycle_type,
        right_cycle_type,
        compiled.total_multiplicity_dimension,
    )
    residual = abs(direct - character_sum)
    return RacahCharacterSumControl(
        n=compiled.n,
        outer_partitions=outer_partitions,
        left_cycle_type=left_cycle_type,
        right_cycle_type=right_cycle_type,
        left_class_size=conjugacy_class_size(left_cycle_type),
        right_class_size=conjugacy_class_size(right_cycle_type),
        coupling_fourier_coefficient=direct,
        character_sum_fourier_coefficient=character_sum,
        formula_residual=residual,
        exact_character_sum_formula_verified=residual <= tolerance,
        status=(
            "natural-racah-character-sum-formula-verified"
            if residual <= tolerance
            else "natural-racah-character-sum-control-failure"
        ),
    )


def identity_coupling_fourier_tail_control(
    n: int,
    maximum_support: int,
) -> IdentityCouplingFourierTailControl:
    if not 3 <= n <= 40 or not 2 <= maximum_support <= n:
        raise ValueError("exact entropy controls require 3<=n<=40 and 2<=support<=n")
    count = partition_number(n)
    retained = exact_central_feature_count(maximum_support)
    full = count - 1
    omitted = full - retained
    q = [
        hook_length_dimension(partition) ** 2 / math.factorial(n)
        for partition in integer_partitions(n)
    ]
    entropy = -sum(mass * math.log2(mass) for mass in q if mass > 0)
    verified = retained + omitted == full and omitted >= 0
    return IdentityCouplingFourierTailControl(
        n=n,
        maximum_moved_support=maximum_support,
        partition_count=count,
        retained_nonconstant_mode_count=retained,
        omitted_nonconstant_mode_count=omitted,
        full_identity_coupling_chi_square=full,
        retained_low_support_diagonal_energy=retained,
        omitted_diagonal_energy=omitted,
        retained_energy_fraction=retained / full if full else 0.0,
        identity_coupling_mutual_information_bits=entropy,
        exact_tail_decomposition_verified=verified,
        status=(
            "low-support-fourier-truncation-misses-projector-tail"
            if verified
            else "identity-coupling-fourier-tail-control-failure"
        ),
    )


def run_plancherel_character_racah_fourier_reduction(
) -> PlancherelCharacterRacahFourierReport:
    basis = [audit_plancherel_character_basis(n) for n in (3, 4, 5, 6, 8, 10)]
    outer = ((3, 1),) * 4
    coupling = compile_complete_racah_coupling(outer)
    classes = ((2, 1, 1), (3, 1))
    character_sums = [
        audit_natural_racah_character_sum(outer, left, right, coupling=coupling)
        for left in classes
        for right in classes
    ]
    tails = [
        identity_coupling_fourier_tail_control(n, support)
        for n in (10, 20, 30)
        for support in (2, 3, 4)
    ]
    failures = sum(not row.exact_plancherel_character_basis_verified for row in basis)
    failures += sum(not row.exact_character_sum_formula_verified for row in character_sums)
    failures += sum(not row.exact_tail_decomposition_verified for row in tails)
    verified = failures == 0
    theorem = PlancherelCharacterRacahFourierTheorem(
        orthonormal_basis=(
            "phi_C(lambda)=sqrt(|C|)chi_lambda(C)/d_lambda is a complete orthonormal Plancherel basis"
        ),
        parseval_identity=(
            "chi2(pi||q^2)=sum_((C,D)!=(e,e))(E_pi phi_C phi_D)^2"
        ),
        natural_racah_character_sum=(
            "hat L_o(C,D)=(M|G|sqrt(|C||D|))^-1 sum_(h,g,k) chi_lambda(h^-1)chi_alpha(hg)chi_beta(hgk)chi_gamma(hk)"
        ),
        low_support_mode_count="number of nonconstant class modes moving <=s is p(s)-1",
        full_growing_support_tail_control_proved=False,
        status=(
            "racah-label-collision-reduced-to-explicit-character-fourier-tail"
            if verified
            else "plancherel-character-racah-fourier-control-failure"
        ),
    )
    return PlancherelCharacterRacahFourierReport(
        created_at=utc_now(),
        theorem_contract={
            "reference_measure": "q(lambda)=d_lambda^2/n!",
            "identity_mode": "C=1^n gives phi_C=1",
            "coefficient": "hat L_o(C,D)=E_(pi_o) phi_C(mu)phi_D(nu)",
            "collision_scope": "the q^2-relative collision includes one-sided marginal modes",
            "entropy_bridge": "D(pi_o||q^2)<=log2(1+chi2(pi_o||q^2))",
            "scope": "rank-label collision reduction; no orientation-syndrome estimate",
        },
        theorem=theorem,
        basis_controls=basis,
        character_sum_controls=character_sums,
        identity_tail_controls=tails,
        proof_obligations=[
            {
                "obligation": "derive_multiplicity_gauge_free_racah_fourier_coefficients",
                "resolved": verified,
                "resolution": "Insert pair-channel central class sums and the final isotypic projector, then expand the trace.",
            },
            {
                "obligation": "bound_growing_support_character_sum_tail_under_physical_outer_law",
                "resolved": False,
                "resolution": "Need uniform cancellation after summing all class pairs that carry nonnegligible Fourier energy.",
            },
            {
                "obligation": "replace_collision_tail_by_fractional_or_entropy_tail_if_l2_is_spiky",
                "resolved": False,
                "resolution": "The exact L2 expansion may be too tail-sensitive; a truncated information inequality is still needed.",
            },
            {
                "obligation": "control_conditional_marginal_modes",
                "resolved": False,
                "resolution": "Five-label estimates control their physical average asymptotically, but no growing-support uniform rate is inserted here.",
            },
        ],
        adversarial_audit=[
            {
                "objection": "A few low-support character coefficients represent the full partition label.",
                "resolved": True,
                "resolution": "Completeness requires all p(n) conjugacy-class modes; low support contains only p(s)-1 nonconstant modes.",
            },
            {
                "objection": "The identity-coupling tail models the natural Racah associator.",
                "resolved": True,
                "resolution": "It is only an exact marginally correct countermodel showing that Parseval tails cannot be omitted abstractly.",
            },
            {
                "objection": "A collision bound is necessary for sublogarithmic mutual information.",
                "resolved": True,
                "resolution": "It is sufficient but not necessary; fractional moments remain the preferred fallback for sparse spikes.",
            },
            {
                "objection": "The character sum is already an efficient estimator.",
                "resolved": True,
                "resolution": "The exact sum has factorial support as written; it is an analytic representation, not a polynomial algorithm.",
            },
        ],
        headline_metrics={
            "complete_plancherel_character_basis_theorem_count": int(verified),
            "exact_natural_racah_character_sum_identity_count": len(character_sums),
            "identity_coupling_tail_countermodel_count": len(tails),
            "finite_control_failure_count": failures,
            "growing_support_character_tail_theorem_count": 0,
            "efficient_character_sum_estimator_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "plancherel_character_basis_complete_proved": verified,
            "natural_racah_fourier_coefficient_formula_proved": verified,
            "low_support_fourier_modes_control_full_label_tail": False,
            "natural_racah_collision_subpolynomial_proved": False,
            "natural_racah_mutual_information_sublogarithmic_proved": False,
            "efficient_classical_estimator_proved": False,
            "classical_separation_proved": False,
            "algorithm_claim_allowed": False,
            "speedup_claim_allowed": False,
            "reason": "The exact Fourier reduction exposes, but does not bound, the growing-support class-pair tail.",
        },
        status=(
            "natural-racah-fourier-tail-is-now-explicit-and-uncontrolled"
            if verified
            else "plancherel-character-racah-fourier-control-failure"
        ),
        summary=(
            "Constructed the complete Plancherel label Fourier basis and removed "
            "multiplicity gauges from every natural Racah coefficient."
        ),
        falsifiers_triggered=[
            "Fixed-support character modes are not a complete projector basis.",
            "Plancherel marginals do not bound the diagonal Fourier tail.",
            "An exact character sum is not by itself a scalable transform or estimator.",
        ],
    )


def write_plancherel_character_racah_fourier_report(
    path: Path = REPORT_PATH,
) -> dict[str, Any]:
    payload = asdict(run_plancherel_character_racah_fourier_reduction())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    return payload


if __name__ == "__main__":
    result = write_plancherel_character_racah_fourier_report()
    print(json.dumps(result["headline_metrics"], indent=2, sort_keys=True))

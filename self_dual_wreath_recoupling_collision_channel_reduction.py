"""The canonical six-way moment is a Racah collision-channel norm.

Fix outer ``S_n`` labels ``(alpha,beta,gamma,lambda)`` and write

    M = sum_mu g(alpha,beta,mu) g(mu,gamma,lambda).

The recoupling unitary is block-decomposed by left and right intermediate
labels ``mu,nu``.  Put

    x_(mu,nu) = ||R_(mu,nu)||_HS^2,
    pi_(mu,nu) = x_(mu,nu)/M.                              (1)

Unitarity makes ``pi`` a probability coupling.  Its marginals are the
normalized Kronecker rank profiles

    p_mu = g(alpha,beta,mu)g(mu,gamma,lambda)/M,
    r_nu = g(beta,gamma,nu)g(alpha,nu,lambda)/M.           (2)

Let ``q_rho=d_rho^2/n!`` be Plancherel measure and define the total
multiplicity density

    Z = n! M/(d_alpha d_beta d_gamma d_lambda).           (3)

The physical six-label likelihood has the exact factorization

    L(alpha,beta,gamma,mu,nu,lambda)
      = Z pi_(mu,nu)/(q_mu q_nu).                          (4)

Consequently, for an intermediate dimension cut ``d_mu,d_nu>D``, its
conditional second moment is

    sum_(mu,nu retained) q_mu q_nu L^2
      = Z^2 C_D(pi),
    C_D(pi)=sum_(mu,nu retained) pi_(mu,nu)^2/(q_mu q_nu). (5)

After also cutting the four outer dimensions, the full six-label trimmed
moment is exactly ``E_(q^4)[Z^2 C_D(pi) 1_outer]``.  Aggregating transpose
orbits is a stochastic coarse-graining and the cut is orbit-invariant, so the
coarse alternating moment needed by the rank-transfer theorem is no larger.

Equations (1)--(5) identify the missing theorem: natural high-dimensional
symmetric-group recoupling must be delocalized relative to ``q tensor q``.
Correct row and column marginals do not imply this.  An identity orthogonal
matrix with block sizes ``d_lambda^2`` has exact Plancherel marginals but
``C(pi)=p(n)`` instead of one.  Thus unitarity, rank profiles, and one-label
Plancherel mixing alone permit an exponentially-in-sqrt(n) collision spike.

The fixed-row recoupling asymptotics of Christandl--Sahinoglu--Walter do not
close this target: their polynomial equivalence constants depend on a bounded
number of rows, whereas Plancherel diagrams have a growing row count.  No
delocalization, physical rank mixing, algorithm, or speedup is proved here.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import numpy as np

from representation_obstruction import hook_length_dimension, integer_partitions
from research_registry import utc_now
from self_dual_wreath_alternating_trimmed_sixway_renyi_transfer import (
    audit_trimmed_sixway_renyi,
)
from self_dual_wreath_character_triangle_barrier import partition_number
from self_dual_wreath_plancherel_kronecker_positivity import (
    kronecker_multiplicity,
)
from self_dual_wreath_tetrahedral_chi_square_tail_no_go import (
    finite_physical_likelihood_arrays,
)


REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_recoupling_collision_channel_reduction.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-RECOUPLING-COLLISION-CHANNEL-REDUCTION"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"

Partition = tuple[int, ...]


@dataclass(frozen=True)
class RecouplingCollisionChannelControl:
    control_id: str
    n: int
    outer_partitions: tuple[Partition, Partition, Partition, Partition]
    minimum_intermediate_dimension_exclusive: int
    total_multiplicity_dimension: int
    total_multiplicity_density: float
    coupling_probability_sum: float
    maximum_row_marginal_residual: float
    maximum_column_marginal_residual: float
    maximum_likelihood_factorization_residual: float
    maximum_negative_block_mass: float
    retained_recoupling_collision: float
    retained_direct_likelihood_second_moment: float
    retained_reduced_likelihood_second_moment: float
    retained_second_moment_identity_residual: float
    rank_independent_collision_benchmark: float
    recoupling_dependence_collision: float
    exact_recoupling_collision_channel_verified: bool
    status: str


@dataclass(frozen=True)
class FullToCoarseTrimControl:
    n: int
    minimum_dimension_exclusive: int
    full_partition_trimmed_second_moment: float
    recoupling_collision_decomposition: float
    coarse_transpose_orbit_trimmed_second_moment: float
    full_collision_decomposition_residual: float
    coarse_graining_slack: float
    transpose_orbit_data_processing_verified: bool
    status: str


@dataclass(frozen=True)
class PlancherelMarginalCountermodel:
    n: int
    partition_count: int
    abstract_orthogonal_dimension: int
    block_rank_sum: int
    exact_plancherel_row_marginals: bool
    exact_plancherel_column_marginals: bool
    independent_coupling_collision: float
    identity_block_coupling_collision: float
    collision_inflation: float
    log_collision_over_log_n: float
    collision_is_n_to_the_o_one: bool
    status: str


@dataclass(frozen=True)
class RecouplingCollisionChannelTheorem:
    likelihood_factorization: str
    trimmed_second_moment_identity: str
    coarse_graining_inequality: str
    missing_natural_recoupling_condition: str
    rank_marginals_sufficient: bool
    fixed_row_asymptotics_applicable_to_plancherel_shapes: bool
    status: str


@dataclass(frozen=True)
class RecouplingCollisionChannelReport:
    created_at: str
    theorem_contract: dict[str, Any]
    theorem: RecouplingCollisionChannelTheorem
    finite_channel_controls: list[RecouplingCollisionChannelControl]
    full_to_coarse_controls: list[FullToCoarseTrimControl]
    countermodel_scaling: list[PlancherelMarginalCountermodel]
    literature_boundary: list[dict[str, str | bool]]
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _total_multiplicity(
    alpha: Partition,
    beta: Partition,
    gamma: Partition,
    final: Partition,
) -> int:
    return sum(
        kronecker_multiplicity(alpha, beta, intermediate)
        * kronecker_multiplicity(intermediate, gamma, final)
        for intermediate in integer_partitions(sum(alpha))
    )


def audit_recoupling_collision_channel(
    control_id: str,
    n: int,
    outer_partitions: tuple[Partition, Partition, Partition, Partition],
    minimum_intermediate_dimension_exclusive: int = 0,
    *,
    tolerance: float = 2e-9,
) -> RecouplingCollisionChannelControl:
    if len(outer_partitions) != 4 or any(
        sum(partition) != n for partition in outer_partitions
    ):
        raise ValueError("four outer partitions of n are required")
    if not 3 <= n <= 5 or minimum_intermediate_dimension_exclusive < 0:
        raise ValueError("exact collision controls require 3<=n<=5 and D>=0")
    partitions, likelihood, _reference, _physical = (
        finite_physical_likelihood_arrays(n)
    )
    partition_index = {
        partition: index for index, partition in enumerate(partitions)
    }
    alpha, beta, gamma, final = outer_partitions
    outer_indices = tuple(
        partition_index[partition] for partition in outer_partitions
    )
    dimensions = {
        partition: hook_length_dimension(partition) for partition in partitions
    }
    order = math.factorial(n)
    total = _total_multiplicity(alpha, beta, gamma, final)
    if total <= 0:
        raise ValueError("outer labels have zero total recoupling multiplicity")
    outer_dimension_product = math.prod(dimensions[p] for p in outer_partitions)
    density = order * total / outer_dimension_product
    left_marginal = {
        intermediate: (
            kronecker_multiplicity(alpha, beta, intermediate)
            * kronecker_multiplicity(intermediate, gamma, final)
            / total
        )
        for intermediate in partitions
    }
    right_marginal = {
        intermediate: (
            kronecker_multiplicity(beta, gamma, intermediate)
            * kronecker_multiplicity(alpha, intermediate, final)
            / total
        )
        for intermediate in partitions
    }

    coupling: dict[tuple[Partition, Partition], float] = {}
    likelihood_residual = 0.0
    maximum_negative = 0.0
    direct_second = 0.0
    collision = 0.0
    rank_collision = 0.0
    dependence_collision = 0.0
    for mu in partitions:
        d_mu = dimensions[mu]
        q_mu = d_mu * d_mu / order
        for nu in partitions:
            d_nu = dimensions[nu]
            q_nu = d_nu * d_nu / order
            indices = (
                outer_indices[0],
                outer_indices[1],
                outer_indices[2],
                partition_index[mu],
                partition_index[nu],
                outer_indices[3],
            )
            observed_likelihood = float(likelihood[indices])
            common_scale = (
                outer_dimension_product * d_mu * d_nu / order**3
            )
            normalized_block_mass = common_scale * observed_likelihood
            block_hilbert_schmidt_square = normalized_block_mass * d_mu * d_nu
            probability = block_hilbert_schmidt_square / total
            coupling[mu, nu] = probability
            maximum_negative = max(maximum_negative, -probability)
            predicted_likelihood = density * probability / (q_mu * q_nu)
            likelihood_residual = max(
                likelihood_residual,
                abs(observed_likelihood - predicted_likelihood),
            )
            retained = (
                d_mu > minimum_intermediate_dimension_exclusive
                and d_nu > minimum_intermediate_dimension_exclusive
            )
            if retained:
                direct_second += q_mu * q_nu * observed_likelihood**2
                collision += probability**2 / (q_mu * q_nu)
                independent = left_marginal[mu] * right_marginal[nu]
                rank_collision += independent**2 / (q_mu * q_nu)
                if independent > 0:
                    dependence_collision += probability**2 / independent
                elif abs(probability) > tolerance:
                    dependence_collision = math.inf

    row_residual = max(
        abs(
            sum(coupling[mu, nu] for nu in partitions)
            - left_marginal[mu]
        )
        for mu in partitions
    )
    column_residual = max(
        abs(
            sum(coupling[mu, nu] for mu in partitions)
            - right_marginal[nu]
        )
        for nu in partitions
    )
    probability_sum = sum(coupling.values())
    reduced_second = density * density * collision
    second_residual = abs(direct_second - reduced_second)
    exact = bool(
        abs(probability_sum - 1.0) <= tolerance
        and row_residual <= tolerance
        and column_residual <= tolerance
        and likelihood_residual <= tolerance
        and maximum_negative <= tolerance
        and second_residual <= tolerance
    )
    return RecouplingCollisionChannelControl(
        control_id=control_id,
        n=n,
        outer_partitions=outer_partitions,
        minimum_intermediate_dimension_exclusive=(
            minimum_intermediate_dimension_exclusive
        ),
        total_multiplicity_dimension=total,
        total_multiplicity_density=density,
        coupling_probability_sum=probability_sum,
        maximum_row_marginal_residual=row_residual,
        maximum_column_marginal_residual=column_residual,
        maximum_likelihood_factorization_residual=likelihood_residual,
        maximum_negative_block_mass=maximum_negative,
        retained_recoupling_collision=collision,
        retained_direct_likelihood_second_moment=direct_second,
        retained_reduced_likelihood_second_moment=reduced_second,
        retained_second_moment_identity_residual=second_residual,
        rank_independent_collision_benchmark=rank_collision,
        recoupling_dependence_collision=dependence_collision,
        exact_recoupling_collision_channel_verified=exact,
        status=(
            "physical-likelihood-is-exact-recoupling-collision-density"
            if exact
            else "recoupling-collision-channel-control-failure"
        ),
    )


def _six_axis_mask(one_axis: np.ndarray, shape: tuple[int, ...]) -> np.ndarray:
    output = np.ones(shape, dtype=bool)
    for axis in range(6):
        axis_shape = [1] * 6
        axis_shape[axis] = len(one_axis)
        output &= one_axis.reshape(axis_shape)
    return output


def audit_full_to_coarse_trim(
    n: int,
    minimum_dimension_exclusive: int,
    *,
    tolerance: float = 2e-8,
) -> FullToCoarseTrimControl:
    if not 3 <= n <= 5 or minimum_dimension_exclusive < 0:
        raise ValueError("exact trim controls require 3<=n<=5 and D>=0")
    partitions, likelihood, reference, _physical = finite_physical_likelihood_arrays(n)
    dimensions = np.asarray(
        [hook_length_dimension(partition) for partition in partitions],
        dtype=int,
    )
    retained_one = dimensions > minimum_dimension_exclusive
    retained = _six_axis_mask(retained_one, likelihood.shape)
    full = float(np.sum(reference[retained] * likelihood[retained] ** 2))
    order = math.factorial(n)
    q = dimensions.astype(float) ** 2 / order
    reduced = 0.0
    retained_indices = tuple(np.flatnonzero(retained_one))
    for alpha, beta, gamma, final in (
        (partitions[a], partitions[b], partitions[c], partitions[f])
        for a in retained_indices
        for b in retained_indices
        for c in retained_indices
        for f in retained_indices
    ):
        total = _total_multiplicity(alpha, beta, gamma, final)
        if total == 0:
            continue
        outer = (alpha, beta, gamma, final)
        outer_indices = tuple(partitions.index(partition) for partition in outer)
        outer_dimensions = math.prod(hook_length_dimension(p) for p in outer)
        z_density = order * total / outer_dimensions
        outer_q = math.prod(q[index] for index in outer_indices)
        collision = 0.0
        for mu_index in retained_indices:
            mu = partitions[mu_index]
            d_mu = dimensions[mu_index]
            for nu_index in retained_indices:
                nu = partitions[nu_index]
                d_nu = dimensions[nu_index]
                six_indices = (
                    outer_indices[0],
                    outer_indices[1],
                    outer_indices[2],
                    mu_index,
                    nu_index,
                    outer_indices[3],
                )
                common = outer_dimensions * d_mu * d_nu / order**3
                block_mass = common * float(likelihood[six_indices])
                pi = block_mass * d_mu * d_nu / total
                collision += pi * pi / (q[mu_index] * q[nu_index])
        reduced += outer_q * z_density * z_density * collision
    coarse = audit_trimmed_sixway_renyi(
        n, minimum_dimension_exclusive
    ).retained_likelihood_second_moment
    residual = abs(full - reduced)
    slack = full - coarse
    verified = residual <= tolerance and slack >= -tolerance
    return FullToCoarseTrimControl(
        n=n,
        minimum_dimension_exclusive=minimum_dimension_exclusive,
        full_partition_trimmed_second_moment=full,
        recoupling_collision_decomposition=reduced,
        coarse_transpose_orbit_trimmed_second_moment=coarse,
        full_collision_decomposition_residual=residual,
        coarse_graining_slack=slack,
        transpose_orbit_data_processing_verified=verified,
        status=(
            "coarse-trimmed-moment-contracts-below-full-racah-collision"
            if verified
            else "full-to-coarse-recoupling-collision-control-failure"
        ),
    )


def plancherel_marginal_identity_countermodel(
    n: int,
) -> PlancherelMarginalCountermodel:
    if n < 2:
        raise ValueError("countermodel requires n>=2")
    count = partition_number(n)
    order = math.factorial(n)
    # Block lambda has d_lambda^2 coordinates.  The identity orthogonal matrix
    # couples each block only to itself, so pi(lambda,nu)=q_lambda 1[lambda=nu].
    rank_sum = sum(
        hook_length_dimension(partition) ** 2
        for partition in integer_partitions(n)
    )
    exact = rank_sum == order
    collision = float(count)
    return PlancherelMarginalCountermodel(
        n=n,
        partition_count=count,
        abstract_orthogonal_dimension=order,
        block_rank_sum=rank_sum,
        exact_plancherel_row_marginals=exact,
        exact_plancherel_column_marginals=exact,
        independent_coupling_collision=1.0,
        identity_block_coupling_collision=collision,
        collision_inflation=collision,
        log_collision_over_log_n=math.log(collision) / math.log(n),
        collision_is_n_to_the_o_one=False,
        status="exact-marginals-and-unitarity-permit-partition-count-collision",
    )


def run_recoupling_collision_channel_reduction(
) -> RecouplingCollisionChannelReport:
    controls = [
        audit_recoupling_collision_channel(
            "S4-STANDARD-OUTER", 4, ((3, 1),) * 4, 1
        ),
        audit_recoupling_collision_channel(
            "S5-STANDARD-OUTER", 5, ((4, 1),) * 4, 1
        ),
        audit_recoupling_collision_channel(
            "S5-BALANCED-OUTER", 5, ((3, 2),) * 4, 1
        ),
        audit_recoupling_collision_channel(
            "S5-MIXED-OUTER",
            5,
            ((4, 1), (3, 2), (4, 1), (3, 2)),
            1,
        ),
    ]
    trim_controls = [
        audit_full_to_coarse_trim(n, threshold)
        for n, threshold in ((3, 1), (4, 1), (4, 2), (5, 1), (5, 4), (5, 5))
    ]
    countermodels = [
        plancherel_marginal_identity_countermodel(n)
        for n in (5, 10, 20, 30, 40, 50)
    ]
    failures = sum(
        not row.exact_recoupling_collision_channel_verified for row in controls
    )
    failures += sum(
        not row.transpose_orbit_data_processing_verified for row in trim_controls
    )
    exact = failures == 0
    theorem = RecouplingCollisionChannelTheorem(
        likelihood_factorization="L=Z*pi(mu,nu)/(q_mu q_nu)",
        trimmed_second_moment_identity=(
            "M_D^full=E_(q^4)[1_outer Z^2 sum_(mu,nu retained) "
            "pi(mu,nu)^2/(q_mu q_nu)]"
        ),
        coarse_graining_inequality="M_D^coarse<=M_D^full",
        missing_natural_recoupling_condition=(
            "Plancherel-weighted collision delocalization of natural squared 6j blocks"
        ),
        rank_marginals_sufficient=False,
        fixed_row_asymptotics_applicable_to_plancherel_shapes=False,
        status=(
            "canonical-rank-target-is-natural-racah-collision-delocalization"
            if exact
            else "recoupling-collision-channel-reduction-failure"
        ),
    )
    return RecouplingCollisionChannelReport(
        created_at=utc_now(),
        theorem_contract={
            "coupling": (
                "pi(mu,nu)=||R_(mu,nu)||_HS^2/M with exact Kronecker-rank marginals"
            ),
            "likelihood": theorem.likelihood_factorization,
            "trimmed_second_moment": theorem.trimmed_second_moment_identity,
            "coarse_transfer": theorem.coarse_graining_inequality,
            "remaining_target": theorem.missing_natural_recoupling_condition,
            "scope": (
                "The reduction is exact. It supplies no all-n delocalization estimate "
                "for natural Plancherel-shaped symmetric-group recoupling."
            ),
        },
        theorem=theorem,
        finite_channel_controls=controls,
        full_to_coarse_controls=trim_controls,
        countermodel_scaling=countermodels,
        literature_boundary=[
            {
                "id": "christandl-sahinoglu-walter-recoupling-2016",
                "url": "https://arxiv.org/abs/1210.0463",
                "applicable": False,
                "boundary": (
                    "Its polynomial norm equivalence and quantum-marginal asymptotics "
                    "depend on a bounded maximal row count; Plancherel rows grow."
                ),
            },
            {
                "id": "pak-panova-yeliussizov-largest-kronecker-2018",
                "url": "https://arxiv.org/abs/1804.04693",
                "applicable": True,
                "boundary": (
                    "Large Plancherel-shaped Kronecker multiplicities show that high "
                    "irrep dimension alone cannot force sparse recoupling blocks."
                ),
            },
        ],
        proof_obligations=[
            {
                "obligation": "factor_physical_likelihood_through_recoupling_coupling",
                "resolved": exact,
                "resolution": (
                    "Racah block masses, unitarity marginals, and Plancherel weights "
                    "give equation (4) exactly."
                ),
            },
            {
                "obligation": "transfer_full_trimmed_collision_to_coarse_orbit_target",
                "resolved": exact,
                "resolution": (
                    "Conditional Jensen under transpose-orbit aggregation contracts "
                    "the orbit-invariant trimmed second moment."
                ),
            },
            {
                "obligation": "prove_natural_plancherel_racah_collision_delocalization",
                "resolved": False,
                "resolution": (
                    "Bound E[Z^2 C_D(pi)] by n^o(1), or bound retained positive "
                    "likelihood information directly if this Renyi norm has spikes."
                ),
            },
            {
                "obligation": "extend_recoupling_asymptotics_to_growing_row_shapes",
                "resolved": False,
                "resolution": (
                    "Existing fixed-row quantum-marginal asymptotics do not cover "
                    "VKLS/Plancherel diagrams."
                ),
            },
        ],
        adversarial_audit=[
            {
                "objection": "Correct left and right rank profiles imply joint mixing.",
                "resolved": True,
                "resolution": (
                    "The identity-block orthogonal countermodel has exact Plancherel "
                    "marginals but collision p(n)."
                ),
            },
            {
                "objection": "Unitarity makes squared block masses independent.",
                "resolved": True,
                "resolution": (
                    "Unitarity fixes only transportation marginals; orthostochastic "
                    "couplings can be maximally aligned."
                ),
            },
            {
                "objection": "Fixed-row 6j asymptotics cover typical partitions.",
                "resolved": True,
                "resolution": (
                    "Their row-dependent polynomial factors are uncontrolled when the "
                    "number of rows grows on the Plancherel scale."
                ),
            },
            {
                "objection": "A full-label collision bound proves non-Haar syndrome decay.",
                "resolved": True,
                "resolution": (
                    "It would close only the coarse rank-transfer obstruction; the "
                    "conditional Racah cumulants remain a separate target."
                ),
            },
        ],
        headline_metrics={
            "recoupling_collision_factorization_theorem_count": int(exact),
            "full_to_coarse_trim_transfer_theorem_count": int(exact),
            "finite_channel_control_count": len(controls),
            "finite_trim_control_count": len(trim_controls),
            "finite_control_failure_count": failures,
            "rank_marginal_sufficiency_counterexample_count": len(countermodels),
            "natural_plancherel_racah_delocalization_theorem_count": 0,
            "physical_rank_mixing_theorem_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "physical_likelihood_recoupling_collision_factorization_proved": exact,
            "coarse_trimmed_moment_bounded_by_full_collision_proved": exact,
            "rank_marginals_suffice_for_joint_recoupling_mixing": False,
            "fixed_row_recoupling_theorem_applies_to_plancherel_shapes": False,
            "natural_plancherel_racah_collision_subpolynomial_proved": False,
            "canonical_trimmed_sixway_subpolynomial_proved": False,
            "physical_rank_profile_mixes_proved": False,
            "irreducible_racah_cmi_vanishes_proved": False,
            "classical_separation_proved": False,
            "algorithm_claim_allowed": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The exact target is now a weighted collision norm of natural 6j block "
                "masses, but no growing-row delocalization theorem is known."
            ),
        },
        status=(
            "rank-target-reduced-to-growing-row-racah-collision-delocalization"
            if exact
            else "recoupling-collision-channel-control-failure"
        ),
        summary=(
            "Factored the physical likelihood through a Racah coupling and proved that "
            "rank marginals and unitarity alone cannot control its collision norm."
        ),
        falsifiers_triggered=[
            "Exact Plancherel marginals do not imply a product recoupling coupling.",
            "Orthogonal recoupling can be collision-localized despite perfect rank marginals.",
            "Bounded-row recoupling asymptotics cannot be silently applied to VKLS shapes.",
        ],
    )


def write_recoupling_collision_channel_report(
    path: Path = REPORT_PATH,
) -> dict[str, Any]:
    payload = asdict(run_recoupling_collision_channel_reduction())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    return payload


if __name__ == "__main__":
    result = write_recoupling_collision_channel_report()
    print(json.dumps(result["headline_metrics"], indent=2, sort_keys=True))

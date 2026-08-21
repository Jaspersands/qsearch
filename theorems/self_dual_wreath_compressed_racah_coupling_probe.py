"""Complete finite Racah couplings from compressed pairwise YJM fibers.

The block compiler computes a canonical mass ``x_(mu,nu)`` for one pair of
intermediate labels.  A research conclusion requires the complete coupling:

    sum_nu x_(mu,nu) = l_mu,
    sum_mu x_(mu,nu) = r_nu,
    sum_(mu,nu) x_(mu,nu) = M.                            (1)

After normalizing ``pi=x/M``, this module reports the conditional Racah mutual
information and fractional dependence moments

    S_theta = sum_(mu,nu) pi_(mu,nu)
                    (pi_(mu,nu)/(p_mu r_nu))^theta.       (2)

The full ``S_6`` coupling for the maximal-dimensional partition ``(3,2,1)``
is tractable with pair fibers even though the old dense approach diagonalized
the full three-copy representation.  This remains finite evidence.  A few
outer sectors do not estimate the physical Plancherel average, and the pair
representation dimensions remain exponential for growing ``n``.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from representation_obstruction import hook_length_dimension, integer_partitions
from research_registry import utc_now
from self_dual_wreath_compressed_racah_block_probe import (
    CompressedRacahBlockRecord,
    compile_compressed_racah_block,
    total_recoupling_multiplicity,
)
from symmetric_character import kronecker_coefficient


Partition = tuple[int, ...]
REPORT_PATH = Path(
    "research/representation/self_dual_wreath_compressed_racah_coupling_probe.json"
)
DEFAULT_EXPERIMENT_ID = "EXP-CODE-SELF-DUAL-WREATH-COMPRESSED-RACAH-COUPLING-PROBE"
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


@dataclass(frozen=True)
class RacahCouplingEntry:
    left_intermediate_partition: Partition
    right_intermediate_partition: Partition
    left_block_rank: int
    right_block_rank: int
    block_hilbert_schmidt_square: float
    physical_block_probability: float
    independent_rank_block_probability: float
    relative_block_overlap: float
    mutual_information_contribution_bits: float


@dataclass(frozen=True)
class CompleteCompressedRacahCoupling:
    n: int
    outer_partitions: tuple[Partition, Partition, Partition, Partition]
    source_irrep_dimension: int
    left_channel_count: int
    right_channel_count: int
    total_multiplicity_dimension: int
    block_count: int
    total_block_mass: float
    total_block_mass_residual: float
    maximum_left_rank_marginal_residual: float
    maximum_right_rank_marginal_residual: float
    conditional_racah_mutual_information_bits: float
    dependence_collision_moment: float
    dependence_collision_renyi_upper_bits: float
    fractional_dependence_moments: dict[str, float]
    fractional_renyi_upper_bits: dict[str, float]
    maximum_relative_block_overlap: float
    bad_mass_above_relative_overlap_2: float
    bad_mass_above_relative_overlap_4: float
    physical_outer_tuple_probability: float
    contribution_to_physical_average_mi_bits: float
    dense_three_copy_vector_dimension: int
    largest_pair_eigensolve_vector_dimension: int
    dense_to_pair_eigensolve_reduction_factor: float
    maximum_pair_embedding_isometry_residual: float
    maximum_independent_finite_likelihood_mass_residual: float | None
    coupling_entries: list[RacahCouplingEntry]
    exact_complete_coupling_verified: bool
    finite_representation_space_probe_only: bool
    status: str


@dataclass(frozen=True)
class CompleteCompressedRacahCouplingReport:
    created_at: str
    theorem_contract: dict[str, Any]
    records: list[CompleteCompressedRacahCoupling]
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _maximum_dimension_partition(n: int) -> Partition:
    return max(integer_partitions(n), key=hook_length_dimension)


def compile_complete_racah_coupling(
    outer_partitions: tuple[Partition, Partition, Partition, Partition],
    *,
    tolerance: float = 3e-6,
) -> CompleteCompressedRacahCoupling:
    """Compile all nonzero intermediate blocks for one outer-label tuple."""

    if len(outer_partitions) != 4:
        raise ValueError("four outer partitions are required")
    alpha, beta, gamma, final = outer_partitions
    n = sum(alpha)
    if any(sum(partition) != n for partition in outer_partitions):
        raise ValueError("outer partitions must have common size n")
    partitions = tuple(integer_partitions(n))
    left_ranks = {
        intermediate: (
            kronecker_coefficient(alpha, beta, intermediate)
            * kronecker_coefficient(intermediate, gamma, final)
        )
        for intermediate in partitions
    }
    right_ranks = {
        intermediate: (
            kronecker_coefficient(beta, gamma, intermediate)
            * kronecker_coefficient(alpha, intermediate, final)
        )
        for intermediate in partitions
    }
    left_channels = tuple(label for label, rank in left_ranks.items() if rank > 0)
    right_channels = tuple(label for label, rank in right_ranks.items() if rank > 0)
    total = total_recoupling_multiplicity(alpha, beta, gamma, final)
    if sum(left_ranks.values()) != total or sum(right_ranks.values()) != total:
        raise ArithmeticError("rank profiles disagree with total multiplicity")

    block_records: list[CompressedRacahBlockRecord] = []
    entries: list[RacahCouplingEntry] = []
    row_masses = {label: 0.0 for label in left_channels}
    column_masses = {label: 0.0 for label in right_channels}
    for mu in left_channels:
        for nu in right_channels:
            block = compile_compressed_racah_block(
                f"complete-s{n}-{mu}-{nu}",
                outer_partitions,
                mu,
                nu,
                tolerance=tolerance,
            )
            block_records.append(block)
            row_masses[mu] += block.block_hilbert_schmidt_square
            column_masses[nu] += block.block_hilbert_schmidt_square
            entries.append(
                RacahCouplingEntry(
                    left_intermediate_partition=mu,
                    right_intermediate_partition=nu,
                    left_block_rank=block.left_block_rank,
                    right_block_rank=block.right_block_rank,
                    block_hilbert_schmidt_square=(
                        block.block_hilbert_schmidt_square
                    ),
                    physical_block_probability=block.physical_block_probability,
                    independent_rank_block_probability=(
                        block.independent_rank_block_probability
                    ),
                    relative_block_overlap=block.relative_block_overlap,
                    mutual_information_contribution_bits=(
                        block.pointwise_mutual_information_contribution_bits
                    ),
                )
            )

    total_mass = sum(entry.block_hilbert_schmidt_square for entry in entries)
    total_residual = abs(total_mass - total)
    left_residual = max(
        abs(row_masses[label] - left_ranks[label]) for label in left_channels
    )
    right_residual = max(
        abs(column_masses[label] - right_ranks[label]) for label in right_channels
    )
    mutual_information = sum(
        entry.mutual_information_contribution_bits for entry in entries
    )
    fractional_orders = (0.25, 0.5, 1.0)
    fractional_moments = {
        str(order): sum(
            entry.physical_block_probability
            * entry.relative_block_overlap**order
            for entry in entries
            if entry.physical_block_probability > 0
        )
        for order in fractional_orders
    }
    fractional_upper = {
        str(order): math.log2(fractional_moments[str(order)]) / order
        for order in fractional_orders
    }
    collision = fractional_moments["1.0"]
    maximum_finite_residuals = [
        block.finite_likelihood_block_mass_residual
        for block in block_records
        if block.finite_likelihood_block_mass_residual is not None
    ]
    maximum_finite_residual = (
        max(maximum_finite_residuals, default=0.0)
        if maximum_finite_residuals
        else None
    )
    maximum_isometry = max(
        block.maximum_pair_embedding_isometry_residual for block in block_records
    )
    dimensions = [hook_length_dimension(p) for p in (alpha, beta, gamma)]
    dense_dimension = math.prod(dimensions)
    largest_pair = max(
        block.largest_pair_eigensolve_vector_dimension for block in block_records
    )
    order = math.factorial(n)
    outer_dimension_product = math.prod(
        hook_length_dimension(partition) for partition in outer_partitions
    )
    outer_probability = total * outer_dimension_product / order**3
    exact = bool(
        total_residual <= tolerance
        and left_residual <= tolerance
        and right_residual <= tolerance
        and maximum_isometry <= tolerance
        and (maximum_finite_residual is None or maximum_finite_residual <= tolerance)
        and mutual_information >= -tolerance
        and mutual_information <= math.log2(min(len(left_channels), len(right_channels))) + tolerance
        and all(
            mutual_information <= bound + tolerance
            for bound in fractional_upper.values()
        )
    )
    return CompleteCompressedRacahCoupling(
        n=n,
        outer_partitions=outer_partitions,
        source_irrep_dimension=hook_length_dimension(alpha),
        left_channel_count=len(left_channels),
        right_channel_count=len(right_channels),
        total_multiplicity_dimension=total,
        block_count=len(entries),
        total_block_mass=total_mass,
        total_block_mass_residual=total_residual,
        maximum_left_rank_marginal_residual=left_residual,
        maximum_right_rank_marginal_residual=right_residual,
        conditional_racah_mutual_information_bits=max(0.0, mutual_information),
        dependence_collision_moment=collision,
        dependence_collision_renyi_upper_bits=math.log2(collision),
        fractional_dependence_moments=fractional_moments,
        fractional_renyi_upper_bits=fractional_upper,
        maximum_relative_block_overlap=max(
            entry.relative_block_overlap for entry in entries
        ),
        bad_mass_above_relative_overlap_2=sum(
            entry.physical_block_probability
            for entry in entries
            if entry.relative_block_overlap > 2
        ),
        bad_mass_above_relative_overlap_4=sum(
            entry.physical_block_probability
            for entry in entries
            if entry.relative_block_overlap > 4
        ),
        physical_outer_tuple_probability=outer_probability,
        contribution_to_physical_average_mi_bits=(
            outer_probability * max(0.0, mutual_information)
        ),
        dense_three_copy_vector_dimension=dense_dimension,
        largest_pair_eigensolve_vector_dimension=largest_pair,
        dense_to_pair_eigensolve_reduction_factor=dense_dimension / largest_pair,
        maximum_pair_embedding_isometry_residual=maximum_isometry,
        maximum_independent_finite_likelihood_mass_residual=maximum_finite_residual,
        coupling_entries=entries,
        exact_complete_coupling_verified=exact,
        finite_representation_space_probe_only=True,
        status=(
            "complete-compressed-racah-coupling-verified"
            if exact
            else "complete-compressed-racah-coupling-control-failure"
        ),
    )


def build_complete_compressed_racah_coupling_report(
    n_values: tuple[int, ...] = (4, 5, 6),
) -> CompleteCompressedRacahCouplingReport:
    records = [
        compile_complete_racah_coupling((_maximum_dimension_partition(n),) * 4)
        for n in n_values
    ]
    failures = sum(not record.exact_complete_coupling_verified for record in records)
    maximum_n = max(record.n for record in records)
    return CompleteCompressedRacahCouplingReport(
        created_at=utc_now(),
        theorem_contract={
            "block_mass": "x_(mu,nu)=||R_(mu,nu)||_HS^2",
            "rank_marginals": (
                "sum_nu x=l_mu, sum_mu x=r_nu, sum_(mu,nu)x=M"
            ),
            "conditional_coupling": "pi_(mu,nu)=x_(mu,nu)/M",
            "conditional_mutual_information": (
                "I=sum_(mu,nu)pi log2(Mx/(l_mu r_nu))"
            ),
            "fractional_dependence_moment": (
                "S_theta=sum pi(Mx/(l_mu r_nu))^theta"
            ),
            "physical_outer_weight": (
                "P_outer(alpha,beta,gamma,lambda)="
                "M product_outer(d_rho)/|S_n|^3"
            ),
            "scope": (
                "complete finite conditional couplings for selected outer tuples; "
                "not a physical-average estimate or an asymptotic theorem"
            ),
        },
        records=records,
        proof_obligations=[
            {
                "obligation": "compute_complete_maxdim_s6_racah_coupling",
                "resolved": maximum_n >= 6 and failures == 0,
                "resolution": (
                    "Every allowed block is contracted and both exact rank marginals close."
                ),
            },
            {
                "obligation": "infer_scaling_from_conditional_couplings",
                "resolved": False,
                "resolution": (
                    "The S4--S6 sequence is nonmonotone and too short for asymptotic inference."
                ),
            },
            {
                "obligation": "estimate_physical_average_over_outer_labels",
                "resolved": False,
                "resolution": (
                    "A single maximal-dimension outer tuple may have vanishing asymptotic weight."
                ),
            },
            {
                "obligation": "prove_fractional_dependence_moment_bound",
                "resolved": False,
                "resolution": (
                    "Finite moments identify the observable but do not bound growing-row tails."
                ),
            },
        ],
        adversarial_audit=[
            {
                "objection": "Small S6 conditional MI proves physical rank mixing.",
                "resolved": True,
                "resolution": (
                    "False. The target is an average under the physical outer law, not one tuple."
                ),
            },
            {
                "objection": "The largest-dimension partition is automatically typical enough.",
                "resolved": True,
                "resolution": (
                    "Maximal dimension is only one Plancherel atom; typical-set averaging is still required."
                ),
            },
            {
                "objection": "The observed n sequence supports monotone decay.",
                "resolved": True,
                "resolution": (
                    "It does not: S5 conditional MI exceeds S4 before the sharp S6 drop."
                ),
            },
        ],
        headline_metrics={
            "complete_conditional_coupling_count": len(records),
            "complete_conditional_coupling_failure_count": failures,
            "maximum_complete_coupling_n": maximum_n,
            "maximum_complete_block_count": max(record.block_count for record in records),
            "s6_maxdim_conditional_racah_mi_bits": next(
                (
                    record.conditional_racah_mutual_information_bits
                    for record in records
                    if record.n == 6
                ),
                0.0,
            ),
            "physical_outer_average_estimate_count": 0,
            "growing_row_delocalization_theorem_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "complete_maxdim_s6_racah_coupling_verified": maximum_n >= 6 and failures == 0,
            "all_rank_marginal_checks_passed": failures == 0,
            "finite_conditional_mi_is_asymptotic_evidence": False,
            "physical_average_racah_mi_computed": False,
            "natural_racah_mi_sublogarithmic_proved": False,
            "coherent_racah_transform_polynomial_proved": False,
            "classical_separation_proved": False,
            "algorithm_claim_allowed": False,
            "speedup_claim_allowed": False,
            "reason": (
                "Complete selected conditional couplings now replace cherry-picked blocks, "
                "but physical outer averaging and growing-row asymptotics remain open."
            ),
        },
        status=(
            "complete-finite-racah-couplings-verified-physical-average-open"
            if failures == 0
            else "complete-compressed-racah-coupling-control-failure"
        ),
        summary=(
            f"Computed complete maximal-dimension conditional Racah couplings through S{maximum_n}."
        ),
        falsifiers_triggered=[
            "Selected low-overlap blocks cannot substitute for complete coupling coverage.",
            "A small conditional entropy at one outer tuple cannot substitute for physical averaging.",
            "The finite entropy sequence is nonmonotone and supports no fitted asymptotic law.",
        ],
    )


def write_complete_compressed_racah_coupling_report(
    path: Path = REPORT_PATH,
    **kwargs: Any,
) -> dict[str, Any]:
    payload = asdict(build_complete_compressed_racah_coupling_report(**kwargs))
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    return payload


if __name__ == "__main__":
    result = write_complete_compressed_racah_coupling_report()
    print(json.dumps(result["headline_metrics"], indent=2, sort_keys=True))

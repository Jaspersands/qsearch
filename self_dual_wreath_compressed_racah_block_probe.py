"""Gauge-invariant Racah block masses from pairwise YJM fibers.

Fix outer labels ``(alpha,beta,gamma,lambda)`` and intermediate labels
``mu,nu``.  Let ``E_ab^mu``, ``E_mu,c^lambda``, ``E_bc^nu`` and
``E_a,nu^lambda`` be orthonormal pairwise Clebsch--Gordan embeddings.  Their
four-tensor contraction is the Racah block

    R_(mu,nu)[i,j;k,t]
      = d_lambda^-1 Tr((E_ab^mu E_mu,c^lambda)^*
                       (E_bc^nu E_a,nu^lambda)).          (1)

Changing any multiplicity gauge left- or right-multiplies this block by an
orthogonal matrix.  Hence

    x_(mu,nu)=||R_(mu,nu)||_HS^2
             = d_lambda^-1 Tr(P_lambda P_mu^(12) P_nu^(23))              (2)

is canonical.  With left/right block ranks ``l,r`` and total multiplicity
``M``, the physical coupling and relative overlap are

    pi=x/M,             a=M x/(l r).                    (3)

This module computes (1) without a dense eigensolve on the three-copy tensor
space.  Its eigensolves live in pair spaces ``d_left d_right``.  The stored
embeddings and contractions remain exponential for Plancherel-shaped diagrams,
so the probe supplies finite scaling evidence, not an efficient all-``n``
Racah transform or a quantum algorithm.
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
from self_dual_wreath_tetrahedral_chi_square_tail_no_go import (
    finite_physical_likelihood_arrays,
)
from symmetric_character import kronecker_coefficient
from symmetric_yjm_pair_fiber import PairYJMFiberMetrics, pair_intertwiner_embeddings


Partition = tuple[int, ...]
REPORT_PATH = Path(
    "research/representation/self_dual_wreath_compressed_racah_block_probe.json"
)
DEFAULT_EXPERIMENT_ID = "EXP-CODE-SELF-DUAL-WREATH-COMPRESSED-RACAH-BLOCK-PROBE"
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


@dataclass(frozen=True)
class CompressedRacahBlockRecord:
    control_id: str
    n: int
    outer_partitions: tuple[Partition, Partition, Partition, Partition]
    left_intermediate_partition: Partition
    right_intermediate_partition: Partition
    final_irrep_dimension: int
    left_block_rank: int
    right_block_rank: int
    total_multiplicity_dimension: int
    dense_three_copy_vector_dimension: int
    largest_pair_eigensolve_vector_dimension: int
    pair_eigensolve_dimension_reduction_factor: float
    racah_block_shape: tuple[int, int]
    block_hilbert_schmidt_square: float
    block_operator_norm_square: float
    physical_block_probability: float
    independent_rank_block_probability: float
    relative_block_overlap: float
    pointwise_mutual_information_contribution_bits: float
    maximum_pair_embedding_isometry_residual: float
    exact_finite_likelihood_block_mass: float | None
    finite_likelihood_block_mass_residual: float | None
    finite_representation_space_probe_only: bool
    status: str


@dataclass(frozen=True)
class CompressedRacahProbeReport:
    created_at: str
    theorem_contract: dict[str, Any]
    pair_fiber_metrics: list[PairYJMFiberMetrics]
    block_records: list[CompressedRacahBlockRecord]
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def total_recoupling_multiplicity(
    alpha: Partition,
    beta: Partition,
    gamma: Partition,
    final: Partition,
) -> int:
    n = sum(alpha)
    if any(sum(partition) != n for partition in (beta, gamma, final)):
        raise ValueError("outer partitions must have common size n")
    return sum(
        kronecker_coefficient(alpha, beta, intermediate)
        * kronecker_coefficient(intermediate, gamma, final)
        for intermediate in integer_partitions(n)
    )


def _finite_likelihood_block_mass(
    outer: tuple[Partition, Partition, Partition, Partition],
    mu: Partition,
    nu: Partition,
) -> float | None:
    n = sum(outer[0])
    if n > 5:
        return None
    partitions, likelihood, _reference, _physical = finite_physical_likelihood_arrays(n)
    index = {partition: position for position, partition in enumerate(partitions)}
    alpha, beta, gamma, final = outer
    value = float(
        likelihood[
            index[alpha],
            index[beta],
            index[gamma],
            index[mu],
            index[nu],
            index[final],
        ]
    )
    order = math.factorial(n)
    dimension_product = math.prod(hook_length_dimension(p) for p in outer)
    return (
        dimension_product
        * hook_length_dimension(mu) ** 2
        * hook_length_dimension(nu) ** 2
        * value
        / order**3
    )


def racah_block_from_pair_embeddings(
    ab_mu: np.ndarray,
    mu_c_l: np.ndarray,
    bc_nu: np.ndarray,
    a_nu_l: np.ndarray,
) -> np.ndarray:
    """Contract four pair embeddings into one multiplicity-space Racah block."""

    final_dimension = mu_c_l.shape[-1]
    if a_nu_l.shape[-1] != final_dimension:
        raise ValueError("left and right coupling trees must have the same final irrep")
    # The tetrahedral network has a useful pairwise cut.  NumPy's default
    # four-tensor path otherwise pays the full six-index scalar-loop cost.
    left_half = np.einsum(
        "xabm,zbcn->xzamcn",
        ab_mu,
        bc_nu,
        optimize=True,
    )
    right_half = np.einsum(
        "ymcl,wanl->ywmcan",
        mu_c_l,
        a_nu_l,
        optimize=True,
    ).transpose(0, 1, 4, 2, 3, 5)
    left_matrix = left_half.reshape(
        left_half.shape[0] * left_half.shape[1],
        -1,
    )
    right_matrix = right_half.reshape(
        right_half.shape[0] * right_half.shape[1],
        -1,
    )
    return (
        (left_matrix @ right_matrix.T)
        .reshape(
            ab_mu.shape[0],
            bc_nu.shape[0],
            mu_c_l.shape[0],
            a_nu_l.shape[0],
        )
        .transpose(0, 2, 1, 3)
        .reshape(
            ab_mu.shape[0] * mu_c_l.shape[0],
            bc_nu.shape[0] * a_nu_l.shape[0],
        )
        / final_dimension
    )


def compile_compressed_racah_block(
    control_id: str,
    outer_partitions: tuple[Partition, Partition, Partition, Partition],
    left_intermediate: Partition,
    right_intermediate: Partition,
    *,
    tolerance: float = 2e-6,
) -> CompressedRacahBlockRecord:
    """Compile one Racah block and return only gauge-invariant diagnostics."""

    if len(outer_partitions) != 4:
        raise ValueError("four outer partitions are required")
    alpha, beta, gamma, final = outer_partitions
    n = sum(alpha)
    if any(
        sum(partition) != n
        for partition in (*outer_partitions, left_intermediate, right_intermediate)
    ):
        raise ValueError("all partitions must have common size n")
    g_ab_mu = kronecker_coefficient(alpha, beta, left_intermediate)
    g_mu_c_l = kronecker_coefficient(left_intermediate, gamma, final)
    g_bc_nu = kronecker_coefficient(beta, gamma, right_intermediate)
    g_a_nu_l = kronecker_coefficient(alpha, right_intermediate, final)
    if min(g_ab_mu, g_mu_c_l, g_bc_nu, g_a_nu_l) <= 0:
        raise ValueError("selected intermediate labels must define nonzero channels")

    ab_mu, metric_ab_mu = pair_intertwiner_embeddings(
        alpha, beta, left_intermediate
    )
    mu_c_l, metric_mu_c_l = pair_intertwiner_embeddings(
        left_intermediate, gamma, final
    )
    bc_nu, metric_bc_nu = pair_intertwiner_embeddings(
        beta, gamma, right_intermediate
    )
    a_nu_l, metric_a_nu_l = pair_intertwiner_embeddings(
        alpha, right_intermediate, final
    )
    pair_metrics = (metric_ab_mu, metric_mu_c_l, metric_bc_nu, metric_a_nu_l)
    left_rank = g_ab_mu * g_mu_c_l
    right_rank = g_bc_nu * g_a_nu_l
    block = racah_block_from_pair_embeddings(
        ab_mu,
        mu_c_l,
        bc_nu,
        a_nu_l,
    )
    singular_values = np.linalg.svd(block, compute_uv=False)
    hs_square = float(np.sum(singular_values**2))
    op_square = float(singular_values[0] ** 2) if len(singular_values) else 0.0
    total = total_recoupling_multiplicity(alpha, beta, gamma, final)
    probability = hs_square / total
    independent = left_rank * right_rank / (total * total)
    relative = total * hs_square / (left_rank * right_rank)
    information = probability * math.log2(relative) if probability > 0 else 0.0
    exact_mass = _finite_likelihood_block_mass(
        outer_partitions,
        left_intermediate,
        right_intermediate,
    )
    exact_residual = abs(hs_square - exact_mass) if exact_mass is not None else None
    maximum_isometry = max(metric.embedding_isometry_residual for metric in pair_metrics)
    valid = bool(
        hs_square >= -tolerance
        and hs_square <= min(left_rank, right_rank) + tolerance
        and op_square <= 1 + tolerance
        and maximum_isometry <= tolerance
        and (exact_residual is None or exact_residual <= tolerance)
    )
    dimensions = [hook_length_dimension(p) for p in (alpha, beta, gamma)]
    dense_dimension = math.prod(dimensions)
    largest_pair = max(metric.eigensolve_vector_dimension for metric in pair_metrics)
    return CompressedRacahBlockRecord(
        control_id=control_id,
        n=n,
        outer_partitions=outer_partitions,
        left_intermediate_partition=left_intermediate,
        right_intermediate_partition=right_intermediate,
        final_irrep_dimension=hook_length_dimension(final),
        left_block_rank=left_rank,
        right_block_rank=right_rank,
        total_multiplicity_dimension=total,
        dense_three_copy_vector_dimension=dense_dimension,
        largest_pair_eigensolve_vector_dimension=largest_pair,
        pair_eigensolve_dimension_reduction_factor=dense_dimension / largest_pair,
        racah_block_shape=(left_rank, right_rank),
        block_hilbert_schmidt_square=hs_square,
        block_operator_norm_square=op_square,
        physical_block_probability=probability,
        independent_rank_block_probability=independent,
        relative_block_overlap=relative,
        pointwise_mutual_information_contribution_bits=information,
        maximum_pair_embedding_isometry_residual=maximum_isometry,
        exact_finite_likelihood_block_mass=exact_mass,
        finite_likelihood_block_mass_residual=exact_residual,
        finite_representation_space_probe_only=True,
        status=(
            "compressed-racah-block-mass-verified"
            if valid
            else "compressed-racah-block-control-failure"
        ),
    )


def _maximum_dimension_partition(n: int) -> Partition:
    return max(integer_partitions(n), key=hook_length_dimension)


def _moderate_channel(source: Partition) -> Partition:
    """Choose a nontrivial channel that keeps the finite probe tractable."""

    n = sum(source)
    candidates = []
    for target in integer_partitions(n):
        multiplicity = kronecker_coefficient(source, source, target)
        if multiplicity >= 2:
            candidates.append(
                (
                    multiplicity**2 * hook_length_dimension(target) ** 2,
                    multiplicity,
                    hook_length_dimension(target),
                    target,
                )
            )
    if not candidates:
        raise ArithmeticError("no multiplicity-bearing channel found")
    return min(candidates)[3]


def build_compressed_racah_probe_report(
    scaling_n_values: tuple[int, ...] = (6, 7, 8),
) -> CompressedRacahProbeReport:
    blocks: list[CompressedRacahBlockRecord] = []
    # Exact S_5 controls use two distinct multiplicity-two channels and test
    # both diagonal and off-diagonal block contractions against the six-label law.
    source5 = _maximum_dimension_partition(5)
    channels5 = [
        target
        for target in integer_partitions(5)
        if kronecker_coefficient(source5, source5, target) == 2
    ]
    for left in channels5:
        for right in channels5:
            blocks.append(
                compile_compressed_racah_block(
                    f"s5-exact-{left}-{right}",
                    (source5, source5, source5, source5),
                    left,
                    right,
                )
            )
    for n in scaling_n_values:
        source = _maximum_dimension_partition(n)
        channel = _moderate_channel(source)
        blocks.append(
            compile_compressed_racah_block(
                f"maxdim-s{n}-moderate-self-block",
                (source, source, source, source),
                channel,
                channel,
            )
        )
    unique_metrics: dict[
        tuple[Partition, Partition, Partition], PairYJMFiberMetrics
    ] = {}
    # Recover metrics from precisely the pairs used above without exposing cache internals.
    for block in blocks:
        alpha, beta, gamma, final = block.outer_partitions
        mu = block.left_intermediate_partition
        nu = block.right_intermediate_partition
        for triple in (
            (alpha, beta, mu),
            (mu, gamma, final),
            (beta, gamma, nu),
            (alpha, nu, final),
        ):
            _embedding, metric = pair_intertwiner_embeddings(*triple)
            unique_metrics[triple] = metric
    failures = sum(block.status.endswith("failure") for block in blocks)
    failures += sum(metric.status.endswith("failure") for metric in unique_metrics.values())
    exact_controls = sum(block.exact_finite_likelihood_block_mass is not None for block in blocks)
    verified_exact = all(
        block.finite_likelihood_block_mass_residual is None
        or block.finite_likelihood_block_mass_residual <= 2e-6
        for block in blocks
    )
    max_n = max(block.n for block in blocks)
    return CompressedRacahProbeReport(
        created_at=utc_now(),
        theorem_contract={
            "canonical_block_mass": (
                "x_(mu,nu)=||R_(mu,nu)||_HS^2="
                "Tr(P_lambda P_mu^(12) P_nu^(23))/d_lambda"
            ),
            "physical_coupling": "pi_(mu,nu)=x_(mu,nu)/M",
            "relative_overlap": "a_(mu,nu)=M x_(mu,nu)/(l_mu r_nu)",
            "compiler": (
                "four pairwise YJM fibers and one gauge-invariant tensor-network contraction"
            ),
            "eigensolve_dimension": "max of pair dimensions d_left d_right",
            "avoided_dense_dimension": "d_alpha d_beta d_gamma",
            "scope": (
                "finite exponential-dimension probe; no polynomial CG transform, all-n "
                "Racah delocalization theorem, or decoder"
            ),
        },
        pair_fiber_metrics=list(unique_metrics.values()),
        block_records=blocks,
        proof_obligations=[
            {
                "obligation": "verify_pairwise_yjm_embedding_and_racah_contraction",
                "resolved": failures == 0 and verified_exact,
                "resolution": (
                    "Pair embeddings are isometries and all S5 block masses agree with "
                    "the independent six-character physical likelihood."
                ),
            },
            {
                "obligation": "estimate_full_physical_average_racah_mutual_information",
                "resolved": False,
                "resolution": (
                    "Selected blocks do not control omitted block mass; importance sampling "
                    "or a full coupling contraction remains necessary."
                ),
            },
            {
                "obligation": "prove_growing_row_relative_overlap_tail",
                "resolved": False,
                "resolution": (
                    "Finite max-dimension blocks can guide conjectures but cannot establish "
                    "the required Plancherel-weighted asymptotic rate."
                ),
            },
            {
                "obligation": "compile_uniform_coherent_racah_transform",
                "resolved": False,
                "resolution": (
                    "The pair-space vectors and embedding tensors are exponentially large."
                ),
            },
        ],
        adversarial_audit=[
            {
                "objection": "Avoiding the triple tensor eigensolve makes the method polynomial.",
                "resolved": True,
                "resolution": (
                    "False. Typical irrep dimensions and the stored embeddings remain exponential in n."
                ),
            },
            {
                "objection": "One moderate self-block estimates mutual information.",
                "resolved": True,
                "resolution": (
                    "False. Mutual information is a signed sum of pointwise contributions, "
                    "and omitted blocks can dominate."
                ),
            },
            {
                "objection": "Multiplicity gauges can create an apparent overlap signal.",
                "resolved": True,
                "resolution": (
                    "The reported Hilbert--Schmidt mass and singular values are invariant "
                    "under every left/right multiplicity-basis rotation."
                ),
            },
        ],
        headline_metrics={
            "pair_fiber_compiler_count": len(unique_metrics),
            "racah_block_probe_count": len(blocks),
            "independent_s5_exact_block_control_count": exact_controls,
            "control_failure_count": failures,
            "maximum_probe_n": max_n,
            "maximum_dense_to_pair_eigensolve_reduction_factor": max(
                block.pair_eigensolve_dimension_reduction_factor for block in blocks
            ),
            "full_physical_average_racah_mi_estimate_count": 0,
            "growing_row_delocalization_theorem_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "pairwise_yjm_fiber_compiler_verified": failures == 0,
            "independent_s5_racah_block_mass_controls_passed": verified_exact,
            "selected_growing_row_blocks_computed": max_n >= 8,
            "full_physical_average_racah_mi_computed": False,
            "natural_racah_mi_sublogarithmic_proved": False,
            "coherent_racah_transform_polynomial_proved": False,
            "classical_separation_proved": False,
            "algorithm_claim_allowed": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The canonical block observable is now computable without triple-space "
                "diagonalization, but finite selected blocks neither prove delocalization "
                "nor provide an efficient coherent transform."
            ),
        },
        status=(
            "compressed-finite-racah-block-probe-verified"
            if failures == 0 and verified_exact
            else "compressed-racah-block-probe-control-failure"
        ),
        summary=(
            "Replaced dense three-copy Racah diagonalization by pairwise YJM fibers "
            f"and gauge-invariant contractions through S{max_n}."
        ),
        falsifiers_triggered=[
            "A reduction in eigensolve dimension is not a polynomial-time recoupling algorithm.",
            "Selected block delocalization is not a bound on physical-average mutual information.",
            "Finite max-dimension data are conjecture generators, not asymptotic evidence by themselves.",
        ],
    )


def write_compressed_racah_probe_report(
    path: Path = REPORT_PATH,
    **kwargs: Any,
) -> dict[str, Any]:
    payload = asdict(build_compressed_racah_probe_report(**kwargs))
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    return payload


if __name__ == "__main__":
    result = write_compressed_racah_probe_report()
    print(json.dumps(result["headline_metrics"], indent=2, sort_keys=True))

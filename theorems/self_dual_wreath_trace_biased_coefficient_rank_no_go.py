"""Reject every block-adaptive low-rank coefficient-output shortcut.

For one active Fourier block ``beta`` with orientation projectors ``E_e``, put

    F_beta=sum_e E_e,
    rho_beta[e,f]=Tr(E_e E_f)/Tr(F_beta).                 (1)

Equation (1) is the reduced orientation-register state obtained by applying
the exact analysis polar to the native input ``F_beta/Tr(F_beta)``.  It is a
density matrix: the projector Hilbert--Schmidt Gram is positive and its
diagonal sums to one.

Write ``r_e=Tr(E_e)`` and ``a=max_e r_e/Tr(F_beta)``.  Projector positivity
gives

    0<=rho_beta[e,f]<=min(r_e,r_f)/Tr(F_beta)<=a.

Consequently

    Tr(rho_beta^2)
      =sum_(e,f) rho_beta[e,f]^2
      <=a sum_(e,f)rho_beta[e,f]
      =a Tr(F_beta^2)/Tr(F_beta).                         (2)

At natural copy depth, the existing uniform orientation-rank theorem gives,
outside a product-Plancherel source event of probability ``delta_n``,

    a <= (1+epsilon)/(q(1-epsilon)), q=2^K,              (3)

simultaneously for every orientation and every target irrep.  Its union-bound
failure is ``delta_n=2^(-Theta(n(log n)^2))=o(1/q)``.

Under the physical native trace-biased joint block law, the source marginal
is exactly product Plancherel.  Regular-master decomposition also gives

    E[Tr(F_beta^2)/Tr(F_beta)]
      =1+(q-1)/|S_n|=:gamma=O(1)                         (4)

when ``K=ceil(log2(n!))+2``.  Conditioning all ``2K`` source labels to be
globally distinct, an event ``D`` with probability ``P_D->1``, equations
(2)--(4) imply

    E[Tr(rho_beta^2)|D]
      <= [((1+epsilon)/(1-epsilon)) gamma/q+delta_n]/P_D
      =O(1/q).                                            (5)

For any block-dependent coefficient effect ``0<=A_beta<=I`` with
``Tr(A_beta)<=m``, Hilbert--Schmidt Cauchy--Schwarz and Jensen give

    E Tr(A_beta rho_beta|D)
      <=sqrt(m E Tr(rho_beta^2|D)).                       (6)

Thus every source-and-target-label-adaptive rank ``m=o(q)`` coefficient
subspace, in any basis, retains vanishing native PGM mass.  Constant retained
mass requires ``Omega(q)`` coefficient dimension.

This is stronger than the Walsh-mode no-go but remains an output-rank theorem,
not a circuit lower bound.  A dense tensor transform, dense recoupling, or
direct rectangular-CS polar can use all ``q`` coefficient dimensions
efficiently and is not rejected.
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
from self_dual_wreath_global_collision_free_mass import (
    exact_global_collision_free_probability,
)
from self_dual_wreath_orientation_fusion_moment import (
    exact_orientation_projector_overlap,
)


REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_trace_biased_coefficient_rank_no_go.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-TRACE-BIASED-COEFFICIENT-RANK-NO-GO"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"

Partition = tuple[int, ...]
Label = tuple[Partition, Partition]


@dataclass(frozen=True)
class CoefficientPurityMixtureControl:
    control_id: str
    n: int
    copy_count: int
    orientation_count: int
    partition_count: int
    source_tuple_count: int
    active_fourier_block_count: int
    adaptive_rank_budget: int
    exact_joint_trace_normalization: str
    predicted_joint_trace_normalization: str
    source_marginal_identity_failure_count: int
    global_distinct_probability: str
    direct_trace_biased_global_distinct_probability: str
    average_total_coherence: str
    regular_master_total_coherence: str
    average_output_purity: float
    average_best_adaptive_rank_mass: float
    average_hilbert_schmidt_rank_bound: float
    globally_distinct_average_output_purity: float | None
    globally_distinct_average_best_adaptive_rank_mass: float | None
    globally_distinct_hilbert_schmidt_rank_bound: float | None
    maximum_pointwise_purity_inequality_residual: float
    minimum_output_density_eigenvalue: float
    maximum_output_density_trace_residual: float
    output_density_identity_verified: bool
    projector_entry_and_purity_inequality_verified: bool
    trace_biased_total_coherence_identity_verified: bool
    exact_source_marginal_plancherel_verified: bool
    adaptive_rank_bound_verified: bool
    status: str


@dataclass(frozen=True)
class CoefficientRankNoGoScalingRecord:
    n: int
    group_order_decimal: str
    copy_count: int
    orientation_count_decimal: str
    relative_rank_tolerance: float
    log2_uniform_rank_failure_upper_bound: float
    log2_orientation_count_times_rank_failure_upper_bound: float
    regular_master_total_coherence: float
    asymptotic_global_distinct_probability_lower_bound: float
    conditioned_output_purity_upper_bound: float
    polynomial_rank_budget: int
    adaptive_polynomial_retained_mass_upper_bound: float
    half_mass_required_rank_fraction_lower_bound: float
    finite_n_global_distinct_lower_bound_certified: bool
    arbitrary_basis_sublinear_rank_no_go_applies_once_mass_bound_holds: bool
    status: str


@dataclass(frozen=True)
class TraceBiasedCoefficientRankTheorem:
    output_state: str
    pointwise_purity: str
    uniform_rank: str
    trace_biased_coherence: str
    conditioned_purity: str
    adaptive_effect: str
    asymptotic_consequence: str
    scope: str
    theorem_verified: bool
    status: str


@dataclass(frozen=True)
class TraceBiasedCoefficientRankReport:
    created_at: str
    theorem_contract: dict[str, Any]
    theorem: TraceBiasedCoefficientRankTheorem
    finite_controls: list[CoefficientPurityMixtureControl]
    scaling_records: list[CoefficientRankNoGoScalingRecord]
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    literature_links: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def exact_block_output_density(
    target: Partition,
    labels: tuple[Label, ...],
) -> tuple[Fraction, tuple[tuple[Fraction, ...], ...]] | None:
    """Return ``Tr(F)`` and the exact reduced state (1)."""

    count = 1 << len(labels)
    overlaps = tuple(
        tuple(
            exact_orientation_projector_overlap(
                target,
                labels,
                left,
                right,
            )
            for right in range(count)
        )
        for left in range(count)
    )
    frame_trace = sum(
        (overlaps[index][index] for index in range(count)),
        Fraction(),
    )
    if not frame_trace:
        return None
    density = tuple(
        tuple(value / frame_trace for value in row) for row in overlaps
    )
    return frame_trace, density


def output_density_purity(
    density: tuple[tuple[Fraction, ...], ...],
) -> Fraction:
    return sum(
        (value * value for row in density for value in row),
        Fraction(),
    )


def pointwise_purity_upper_bound(
    density: tuple[tuple[Fraction, ...], ...],
) -> Fraction:
    maximum_diagonal = max(density[index][index] for index in range(len(density)))
    total_coherence = sum(
        (value for row in density for value in row),
        Fraction(),
    )
    return maximum_diagonal * total_coherence


def _best_rank_mass(
    density: tuple[tuple[Fraction, ...], ...],
    rank_budget: int,
) -> tuple[float, float, float]:
    matrix = np.asarray(
        [[float(value) for value in row] for row in density],
        dtype=float,
    )
    eigenvalues = np.linalg.eigvalsh((matrix + matrix.T) / 2)
    best = float(sum(sorted(eigenvalues, reverse=True)[:rank_budget]))
    return best, float(eigenvalues[0]), abs(float(np.trace(matrix)) - 1.0)


def audit_trace_biased_coefficient_purity(
    n: int,
    copy_count: int,
    *,
    adaptive_rank_budget: int = 1,
) -> CoefficientPurityMixtureControl:
    if n < 2 or copy_count < 1:
        raise ValueError("n and copy count are too small")
    count = 1 << copy_count
    if not 1 <= adaptive_rank_budget <= count:
        raise ValueError("adaptive rank budget is out of range")
    partitions = tuple(integer_partitions(n))
    dimensions = {
        partition: hook_length_dimension(partition) for partition in partitions
    }
    order = math.factorial(n)
    predicted_normalization = count * order ** (2 * copy_count)
    total_mass = Fraction()
    coherence_mass = Fraction()
    purity_mass = Fraction()
    adaptive_mass = 0.0
    distinct_mass = Fraction()
    distinct_purity_mass = Fraction()
    distinct_adaptive_mass = 0.0
    source_failures = 0
    active_blocks = 0
    pointwise_residual = Fraction()
    minimum_eigenvalue = math.inf
    trace_residual = 0.0
    adaptive_violation = 0.0

    for sources in itertools.product(partitions, repeat=2 * copy_count):
        labels = tuple(
            (sources[2 * index], sources[2 * index + 1])
            for index in range(copy_count)
        )
        source_multiplicity = math.prod(dimensions[source] for source in sources)
        target_weighted_frame_trace = Fraction()
        source_is_distinct = len(set(sources)) == len(sources)
        for target in partitions:
            block = exact_block_output_density(target, labels)
            if block is None:
                continue
            frame_trace, density = block
            active_blocks += 1
            target_dimension = dimensions[target]
            target_weighted_frame_trace += target_dimension * frame_trace
            weight = target_dimension * source_multiplicity * frame_trace
            purity = output_density_purity(density)
            purity_bound = pointwise_purity_upper_bound(density)
            coherence = sum(
                (value for row in density for value in row),
                Fraction(),
            )
            best, smallest, density_trace_residual = _best_rank_mass(
                density,
                adaptive_rank_budget,
            )
            hs_bound = math.sqrt(adaptive_rank_budget * float(purity))
            adaptive_violation = max(adaptive_violation, best - hs_bound)
            pointwise_residual = max(pointwise_residual, purity - purity_bound)
            minimum_eigenvalue = min(minimum_eigenvalue, smallest)
            trace_residual = max(trace_residual, density_trace_residual)
            total_mass += weight
            coherence_mass += weight * coherence
            purity_mass += weight * purity
            adaptive_mass += float(weight) * best
            if source_is_distinct:
                distinct_mass += weight
                distinct_purity_mass += weight * purity
                distinct_adaptive_mass += float(weight) * best
        if target_weighted_frame_trace != count * source_multiplicity:
            source_failures += 1

    event_probability = exact_global_collision_free_probability(n, copy_count)
    direct_event_probability = distinct_mass / total_mass
    average_coherence = coherence_mass / total_mass
    regular_coherence = 1 + Fraction(count - 1, order)
    average_purity = purity_mass / total_mass
    average_best = adaptive_mass / float(total_mass)
    average_hs = math.sqrt(adaptive_rank_budget * float(average_purity))
    if distinct_mass:
        distinct_purity = distinct_purity_mass / distinct_mass
        distinct_best = distinct_adaptive_mass / float(distinct_mass)
        distinct_hs = math.sqrt(adaptive_rank_budget * float(distinct_purity))
    else:
        distinct_purity = None
        distinct_best = None
        distinct_hs = None

    density_identity = bool(
        minimum_eigenvalue >= -1e-10 and trace_residual <= 1e-12
    )
    pointwise = pointwise_residual <= 0
    coherence_identity = average_coherence == regular_coherence
    source_marginal = bool(
        source_failures == 0
        and total_mass == predicted_normalization
        and direct_event_probability == event_probability
    )
    adaptive = bool(
        adaptive_violation <= 1e-10
        and average_best <= average_hs + 1e-10
        and (
            distinct_best is None
            or (distinct_hs is not None and distinct_best <= distinct_hs + 1e-10)
        )
    )
    verified = density_identity and pointwise and coherence_identity and source_marginal and adaptive
    return CoefficientPurityMixtureControl(
        control_id=f"S{n}-K{copy_count}-COEFFICIENT-PURITY",
        n=n,
        copy_count=copy_count,
        orientation_count=count,
        partition_count=len(partitions),
        source_tuple_count=len(partitions) ** (2 * copy_count),
        active_fourier_block_count=active_blocks,
        adaptive_rank_budget=adaptive_rank_budget,
        exact_joint_trace_normalization=str(total_mass),
        predicted_joint_trace_normalization=str(predicted_normalization),
        source_marginal_identity_failure_count=source_failures,
        global_distinct_probability=str(event_probability),
        direct_trace_biased_global_distinct_probability=str(
            direct_event_probability
        ),
        average_total_coherence=str(average_coherence),
        regular_master_total_coherence=str(regular_coherence),
        average_output_purity=float(average_purity),
        average_best_adaptive_rank_mass=average_best,
        average_hilbert_schmidt_rank_bound=average_hs,
        globally_distinct_average_output_purity=(
            float(distinct_purity) if distinct_purity is not None else None
        ),
        globally_distinct_average_best_adaptive_rank_mass=distinct_best,
        globally_distinct_hilbert_schmidt_rank_bound=distinct_hs,
        maximum_pointwise_purity_inequality_residual=float(pointwise_residual),
        minimum_output_density_eigenvalue=minimum_eigenvalue,
        maximum_output_density_trace_residual=trace_residual,
        output_density_identity_verified=density_identity,
        projector_entry_and_purity_inequality_verified=pointwise,
        trace_biased_total_coherence_identity_verified=coherence_identity,
        exact_source_marginal_plancherel_verified=source_marginal,
        adaptive_rank_bound_verified=adaptive,
        status=(
            "trace-biased-basis-independent-coefficient-rank-bound-verified"
            if verified
            else "trace-biased-coefficient-purity-control-failure"
        ),
    )


def coefficient_rank_scaling_record(
    n: int,
    *,
    relative_rank_tolerance: float = 0.5,
    asymptotic_distinct_probability_lower_bound: float = 0.5,
) -> CoefficientRankNoGoScalingRecord:
    if n < 5 or not 0 < relative_rank_tolerance < 1:
        raise ValueError("invalid rank-scaling parameters")
    if not 0 < asymptotic_distinct_probability_lower_bound <= 1:
        raise ValueError("invalid distinctness lower bound")
    order = math.factorial(n)
    copies = (order - 1).bit_length() + 2
    count = 1 << copies
    minimum_class_size = math.comb(n, 2)
    log2_partition_upper = math.pi * math.sqrt(2 * n / 3) / math.log(2)
    log2_failure = (
        copies
        + 2 * log2_partition_upper
        + (2 - copies) * math.log2(minimum_class_size)
        - 2 * math.log2(relative_rank_tolerance)
    )
    failure = min(1.0, math.exp2(log2_failure)) if log2_failure > -1074 else 0.0
    gamma = 1.0 + (count - 1) / order
    diagonal_factor = (1 + relative_rank_tolerance) / (
        1 - relative_rank_tolerance
    )
    purity_bound = (
        diagonal_factor * gamma / count + failure
    ) / asymptotic_distinct_probability_lower_bound
    budget = min(count, copies**6)
    retained = min(1.0, math.sqrt(budget * purity_bound))
    half_rank_fraction = min(1.0, 0.25 / (purity_bound * count))
    applies = bool(budget < count and log2_failure + copies < 0)
    return CoefficientRankNoGoScalingRecord(
        n=n,
        group_order_decimal=str(order),
        copy_count=copies,
        orientation_count_decimal=str(count),
        relative_rank_tolerance=relative_rank_tolerance,
        log2_uniform_rank_failure_upper_bound=log2_failure,
        log2_orientation_count_times_rank_failure_upper_bound=(
            log2_failure + copies
        ),
        regular_master_total_coherence=gamma,
        asymptotic_global_distinct_probability_lower_bound=(
            asymptotic_distinct_probability_lower_bound
        ),
        conditioned_output_purity_upper_bound=purity_bound,
        polynomial_rank_budget=budget,
        adaptive_polynomial_retained_mass_upper_bound=retained,
        half_mass_required_rank_fraction_lower_bound=half_rank_fraction,
        finite_n_global_distinct_lower_bound_certified=False,
        arbitrary_basis_sublinear_rank_no_go_applies_once_mass_bound_holds=applies,
        status="asymptotic-rank-and-distinctness-envelope-not-finite-n-certificate",
    )


def trace_biased_coefficient_rank_theorem() -> TraceBiasedCoefficientRankTheorem:
    return TraceBiasedCoefficientRankTheorem(
        output_state="rho_beta[e,f]=Tr(E_eE_f)/Tr(F_beta)",
        pointwise_purity=(
            "Tr(rho_beta^2)<=max_e[Tr(E_e)/Tr(F_beta)] "
            "Tr(F_beta^2)/Tr(F_beta)"
        ),
        uniform_rank=(
            "outside delta_n=o(2^-K) source mass, max_e Tr(E_e)/Tr(F) "
            "<=(1+epsilon)/(2^K(1-epsilon)) simultaneously for all targets"
        ),
        trace_biased_coherence=(
            "under the physical native block law, E[Tr(F_beta^2)/Tr(F_beta)] "
            "=1+(2^K-1)/|S_n|"
        ),
        conditioned_purity=(
            "E[Tr(rho_beta^2)|D]<=(((1+epsilon)/(1-epsilon))gamma/2^K+delta_n)/Pr(D)"
        ),
        adaptive_effect=(
            "every block-dependent 0<=A<=I with Tr(A)<=m retains average "
            "mass at most sqrt(m E Tr(rho_beta^2))"
        ),
        asymptotic_consequence=(
            "for globally distinct natural blocks and K=ceil(log2(n!))+2, "
            "every arbitrary-basis adaptive rank m=o(2^K) output loses all mass"
        ),
        scope=(
            "coefficient-output rank only; dense structured transforms, direct "
            "rectangular CS, complete polar, and arbitrary circuit complexity remain open"
        ),
        theorem_verified=True,
        status="physical-arbitrary-basis-sublinear-coefficient-rank-rejected",
    )


def run_trace_biased_coefficient_rank_no_go() -> TraceBiasedCoefficientRankReport:
    controls = [
        audit_trace_biased_coefficient_purity(3, 1),
        audit_trace_biased_coefficient_purity(4, 2),
    ]
    scaling = [
        coefficient_rank_scaling_record(n)
        for n in (8, 12, 16, 24, 32, 48, 64, 96, 128)
    ]
    theorem = trace_biased_coefficient_rank_theorem()
    failures = sum(
        not (
            row.output_density_identity_verified
            and row.projector_entry_and_purity_inequality_verified
            and row.trace_biased_total_coherence_identity_verified
            and row.exact_source_marginal_plancherel_verified
            and row.adaptive_rank_bound_verified
        )
        for row in controls
    )
    verified = theorem.theorem_verified and failures == 0
    return TraceBiasedCoefficientRankReport(
        created_at=utc_now(),
        theorem_contract=asdict(theorem),
        theorem=theorem,
        finite_controls=controls,
        scaling_records=scaling,
        proof_obligations=[
            {
                "obligation": "identify_the_exact_native_orientation_output_state",
                "resolved": verified,
                "resolution": (
                    "Polar cancellation on F/Tr(F) leaves the normalized "
                    "Hilbert--Schmidt Gram of the orientation projectors."
                ),
            },
            {
                "obligation": "bound_output_purity_without_a_fourth_moment",
                "resolved": verified,
                "resolution": (
                    "Entrywise projector overlap positivity converts purity to "
                    "maximum diagonal times total coherence."
                ),
            },
            {
                "obligation": "control_the_maximum_diagonal_on_natural_blocks",
                "resolved": verified,
                "resolution": (
                    "The existing simultaneous orientation/target Plancherel "
                    "rank theorem has failure o(2^-K)."
                ),
            },
            {
                "obligation": "control_trace_biased_total_coherence",
                "resolved": verified,
                "resolution": (
                    "Trace bias cancels the block denominator and regular-master "
                    "Tr(F^2)/Tr(F) is exactly 1+(q-1)/|S_n|."
                ),
            },
            {
                "obligation": "reject_arbitrary_block_adaptive_low_rank_output",
                "resolved": verified,
                "resolution": (
                    "Hilbert--Schmidt Cauchy--Schwarz is pointwise in the chosen "
                    "block effect, so its basis and source/target dependence are arbitrary."
                ),
            },
            {
                "obligation": "compile_dense_structured_orientation_polar",
                "resolved": False,
                "resolution": (
                    "The theorem forces linear coefficient dimension but gives "
                    "no lower bound on a succinct dense transform."
                ),
            },
        ],
        adversarial_audit=[
            {
                "objection": "Walsh flatness is being mistaken for basis-independent mixing.",
                "resolved": True,
                "resolution": (
                    "The new object is the full reduced-state purity, not one "
                    "measurement distribution; the proof uses rank and total coherence."
                ),
            },
            {
                "objection": "The trace-biased target law invalidates uniform source rank concentration.",
                "resolved": True,
                "resolution": (
                    "The good event is simultaneous over every target, while the "
                    "joint physical law has exact product-Plancherel source marginal."
                ),
            },
            {
                "objection": "A rare high-coherence block can dominate after conditioning.",
                "resolved": True,
                "resolution": (
                    "Its purity is at most one and the bad source event is "
                    "o(2^-K); global distinctness costs only division by P_D->1."
                ),
            },
            {
                "objection": "Linear output rank proves exponential gate complexity.",
                "resolved": True,
                "resolution": (
                    "False. Hadamards and many Fourier transforms have full output "
                    "rank with polynomial circuits. Only sparse-output shortcuts close."
                ),
            },
        ],
        literature_links=[
            {
                "paper": "Fast algorithm for quantum polar decomposition, pretty-good measurements, and the Procrustes problem",
                "url": "https://arxiv.org/abs/2106.07634",
                "used_for": (
                    "Context: generic QSVT polar algorithms remain singular-value/"
                    "condition-number dependent; no dense wreath compiler is imported"
                ),
                "external_theorem_needed_for_this_no_go": False,
            }
        ],
        headline_metrics={
            "native_output_density_identity_theorem_count": int(verified),
            "pointwise_output_purity_bound_theorem_count": int(verified),
            "trace_biased_total_coherence_theorem_count": int(verified),
            "arbitrary_basis_adaptive_sublinear_rank_no_go_count": int(verified),
            "finite_control_count": len(controls),
            "finite_control_failure_count": failures,
            "maximum_pointwise_purity_inequality_residual": max(
                row.maximum_pointwise_purity_inequality_residual for row in controls
            ),
            "minimum_output_density_eigenvalue": min(
                row.minimum_output_density_eigenvalue for row in controls
            ),
            "scaling_record_count": len(scaling),
            "tail_polynomial_rank_retained_mass_upper_bound": (
                scaling[-1].adaptive_polynomial_retained_mass_upper_bound
            ),
            "dense_structured_transform_no_go_count": 0,
            "complete_orientation_polar_compiler_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "native_orientation_output_density_matrix_identified": verified,
            "conditioned_average_output_purity_is_O_of_two_to_minus_K": verified,
            "source_and_target_adaptive_arbitrary_basis_o_of_two_to_K_rank_rejected": verified,
            "sparse_walsh_route_rejected_by_companion_theorem": True,
            "dense_structured_transform_rejected": False,
            "dense_structured_transform_compiled": False,
            "direct_rectangular_cs_polar_compiled": False,
            "complete_natural_orientation_polar_compiled": False,
            "classical_separation_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "Every sublinear-dimensional coefficient-output shortcut is "
                "closed, but a succinct dense representation-specific polar "
                "could still implement the target."
            ),
        },
        status=(
            "physical-arbitrary-basis-sublinear-coefficient-rank-rejected"
            if verified
            else "trace-biased-coefficient-rank-control-failure"
        ),
        summary=(
            "Upgraded Walsh sparsity to a basis-independent output-rank no-go: "
            "the physical native polar output has O(2^-K) average purity on "
            "globally distinct natural blocks."
        ),
        falsifiers_triggered=[
            "Changing from Walsh modes to a source-adaptive basis does not rescue any sublinear-rank coefficient router.",
            "A character fourth-moment theorem is unnecessary once uniform ranks and trace-biased total coherence are combined.",
            "Rare rank-imbalanced source tuples cannot dominate the physical joint block law.",
            "Full coefficient rank remains compatible with a polynomial dense transform, so circuit hardness is not claimed.",
        ],
    )


def write_trace_biased_coefficient_rank_report(
    path: Path = REPORT_PATH,
    **_: Any,
) -> dict[str, Any]:
    payload = json.loads(json.dumps(asdict(run_trace_biased_coefficient_rank_no_go())))
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    return payload


if __name__ == "__main__":
    report = write_trace_biased_coefficient_rank_report()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))

"""Exact entanglement structure of modular subset-sum fiber states.

For a coordinate split L|R and target t modulo M, define

    |psi_t> proportional to sum_{x: <A,x>=t mod M} |x>.

If L_r and R_r count left and right subsets with residue r, the coefficient
matrix is a direct sum of all-ones blocks.  Its nonzero squared Schmidt
coefficients are exactly

    L_r R_{t-r} / sum_u L_u R_{t-u}.

Hence the exact Schmidt rank is the number of residues represented on both
sides.  Pairwise independence of distinct nonempty subset sums gives a
Paley-Zygmund support bound.  When each half has q+O(1) labels modulo 2^q,
a constant fraction of random instances have Schmidt rank Omega(2^q).
Second-moment control of block weights and concentration of the full fiber
size also force 2^(q-O(log n)) bond rank for 99-percent Schmidt mass with high
probability, simultaneously over any fixed polynomial dictionary of balanced
coordinate layouts.  These results rule out exact and approximate
polynomial-bond density-one preparation.  They are not lower bounds for
general quantum circuits, arbitrary instance-adaptive layouts, or an
inverse-polynomial partial solver concentrated on another instance subset.
"""

from __future__ import annotations

import json
import math
import random
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Sequence

from research_registry import (
    ExperimentResultRecord,
    NegativeResultRecord,
    upsert_experiment_result,
    upsert_negative_result,
    utc_now,
)


DCP_FIBER_ENTANGLEMENT_PATH = Path(
    "research/phase_workbench/dcp_fiber_entanglement.json"
)
DEFAULT_EXPERIMENT_ID = "EXP-DHS-DCP-FIBER-ENTANGLEMENT"
DEFAULT_CANDIDATE_ID = "DHS-GOWERS-SIEVE"


@dataclass(frozen=True)
class FiberSchmidtTheorem:
    theorem_id: str
    exact_spectrum: str
    exact_rank: str
    side_support_probability_bound: str
    expected_rank_fraction_bound: str
    constant_probability_rank_bound: str
    expected_squared_block_weight_bound: str
    full_fiber_concentration_bound: str
    approximate_rank_bound: str
    polynomial_layout_family_bound: str
    exact_schmidt_decomposition_proved: bool
    constant_fraction_exponential_rank_proved: bool
    exact_polynomial_bond_density_one_route_ruled_out: bool
    approximate_polynomial_bond_density_one_route_ruled_out: bool
    polynomial_layout_dictionary_density_one_route_ruled_out: bool
    proof: str
    scope_exclusions: list[str]


@dataclass(frozen=True)
class FiberRankScalingRow:
    n_bits: int
    modulus_bits: int
    register_count: int
    left_register_count: int
    right_register_count: int
    left_mean_nonempty_subsets_per_residue: float
    right_mean_nonempty_subsets_per_residue: float
    side_support_probability_lower_bounds: tuple[float, float]
    expected_schmidt_rank_fraction_lower_bound: float
    certified_rank_fraction: float
    probability_of_certified_rank_lower_bound: float
    log2_certified_schmidt_rank: float
    exact_polynomial_bond_excluded_on_certified_fraction: bool
    side_second_moment_upper_bounds: tuple[float, float]
    full_fiber_mean_lower_bound: float
    schmidt_purity_upper_bound_on_event: float
    approximate_rank_schmidt_mass: float
    approximate_rank_lower_bound: float
    log2_approximate_rank_lower_bound: float
    approximate_rank_event_probability_lower_bound: float
    approximate_polynomial_bond_excluded_on_certified_fraction: bool
    layout_family_degree: int
    polynomial_layout_family_size: int
    second_moment_markov_factor: float
    polynomial_layout_family_hard_probability_lower_bound: float
    polynomial_layout_family_exponential_bond_certified: bool


@dataclass(frozen=True)
class FiberSchmidtFiniteRow:
    n_bits: int
    modulus_bits: int
    register_count: int
    trial_index: int
    target: int
    fiber_size: int
    exact_schmidt_rank: int
    log2_exact_schmidt_rank: float
    normalized_rank: float
    entanglement_entropy_bits: float
    normalized_entanglement_entropy: float
    schmidt_purity: float
    effective_schmidt_rank: float
    rank_for_90_percent_fidelity: int
    rank_for_99_percent_fidelity: int
    rank_for_999_percent_fidelity: int
    finite_approximate_rank_is_asymptotic_theorem: bool


@dataclass(frozen=True)
class FiberEntanglementReport:
    created_at: str
    theorem: FiberSchmidtTheorem
    scaling_rows: list[FiberRankScalingRow]
    finite_rows: list[FiberSchmidtFiniteRow]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, bool | str]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def residue_counts(labels: Sequence[int], modulus_bits: int) -> list[int]:
    modulus = 1 << modulus_bits
    counts = [0] * modulus
    counts[0] = 1
    for label in labels:
        shifted = [0] * modulus
        delta = label % modulus
        for residue, count in enumerate(counts):
            if count:
                shifted[(residue + delta) % modulus] += count
        counts = [left + right for left, right in zip(counts, shifted)]
    return counts


def fiber_schmidt_probabilities(
    left_counts: Sequence[int], right_counts: Sequence[int], target: int
) -> tuple[list[float], int]:
    if len(left_counts) != len(right_counts):
        raise ValueError("left and right residue tables must have equal length")
    modulus = len(left_counts)
    if modulus == 0 or modulus & (modulus - 1):
        raise ValueError("residue table length must be a nonzero power of two")
    weights = [
        left_counts[residue] * right_counts[(target - residue) % modulus]
        for residue in range(modulus)
    ]
    total = sum(weights)
    if total == 0:
        return [], 0
    return [weight / total for weight in weights if weight], total


def fidelity_rank(probabilities: Sequence[float], fidelity: float) -> int:
    if not 0.0 < fidelity <= 1.0:
        raise ValueError("fidelity must lie in (0,1]")
    cumulative = 0.0
    for rank, probability in enumerate(sorted(probabilities, reverse=True), start=1):
        cumulative += probability
        if cumulative + 1e-15 >= fidelity:
            return rank
    return len(probabilities)


def side_support_probability_lower_bound(
    register_count: int, modulus_bits: int
) -> float:
    modulus = 1 << modulus_bits
    mean = (2**register_count - 1) / modulus
    return mean / (mean + 1.0 - 1.0 / modulus)


def build_schmidt_theorem() -> FiberSchmidtTheorem:
    return FiberSchmidtTheorem(
        theorem_id="THEOREM-DCP-FIBER-EXACT-SCHMIDT-SPECTRUM",
        exact_spectrum=(
            "p_r=L_r*R_(t-r)/C_t for every residue with both factors nonzero, where C_t=sum_r L_r R_(t-r)"
        ),
        exact_rank="rank(psi_t)=|supp(L) intersect (t-supp(R))|",
        side_support_probability_bound=(
            "Pr[N_r>0] >= mu/(mu+1-1/M), mu=(2^d-1)/M, by pairwise independence and Paley-Zygmund"
        ),
        expected_rank_fraction_bound="E[rank]/M >= p_L*p_R for independent left and right labels",
        constant_probability_rank_bound=(
            "If c=p_L*p_R and gamma<c, Pr[rank>=gamma*M] >= (c-gamma)/(1-gamma); choose gamma=c/2"
        ),
        expected_squared_block_weight_bound=(
            "For Q=sum_r (L_r R_(t-r))^2, E[Q] <= M*B_L*B_R with B_d=(1+mu_d)^2+mu_d"
        ),
        full_fiber_concentration_bound=(
            "For C_t=sum_r L_r R_(t-r), Pr[C_t<mu_full/2] <= 4/mu_full by pairwise-independence variance"
        ),
        approximate_rank_bound=(
            "With Markov factor a, purity<=4a*M*B_L*B_R/mu_full^2 except with probability <=1/a+4/mu_full; "
            "Schmidt mass eta requires rank at least eta^2/purity"
        ),
        polynomial_layout_family_bound=(
            "For at most n^d instance-independent balanced cuts, choose Markov factor a=n^(d+2). A union bound "
            "gives simultaneous rank 2^(q-O(log n)) with failure at most n^-2+4/mu_full."
        ),
        exact_schmidt_decomposition_proved=True,
        constant_fraction_exponential_rank_proved=True,
        exact_polynomial_bond_density_one_route_ruled_out=True,
        approximate_polynomial_bond_density_one_route_ruled_out=True,
        polynomial_layout_dictionary_density_one_route_ruled_out=True,
        proof=(
            "Grouping basis rows and columns by subset-sum residue makes the coefficient matrix a direct sum of "
            "rank-one all-ones blocks, proving the spectrum. Distinct nonempty Boolean subset indicators have a "
            "2x2 minor of determinant +/-1, so their sums are pairwise independent over Z_(2^q). Paley-Zygmund "
            "bounds each side's support; independence of the two label halves and a bounded-variable tail argument "
            "give the exact-rank certificate. The same pairwise independence bounds side second moments and "
            "concentrates the full fiber count; Markov plus Cauchy-Schwarz then gives the approximate-rank certificate."
        ),
        scope_exclusions=[
            "general polynomial-size quantum circuits, which can create volume-law entanglement",
            "partial solvers succeeding on an inverse-polynomial subset of easier random instances",
            "approximate preparation concentrated on a selected inverse-polynomial easy-instance subset",
            "coordinate orderings outside the declared fixed polynomial balanced-layout dictionary",
            "instance-adaptive orderings selected from more than a fixed polynomial layout dictionary",
            "time lower bounds inferred only from Schmidt rank",
        ],
    )


def scaling_row(
    n_bits: int,
    register_offset: int = 4,
    depth_fraction: float = 0.5,
    schmidt_mass: float = 0.99,
    layout_family_degree: int = 4,
    union_slack_degree: int = 2,
) -> FiberRankScalingRow:
    modulus_bits = max(2, min(n_bits, math.floor(depth_fraction * n_bits) + 1))
    register_count = n_bits + register_offset
    left = register_count // 2
    right = register_count - left
    modulus = 1 << modulus_bits
    left_mean = (2**left - 1) / modulus
    right_mean = (2**right - 1) / modulus
    p_left = side_support_probability_lower_bound(left, modulus_bits)
    p_right = side_support_probability_lower_bound(right, modulus_bits)
    expected_fraction = p_left * p_right
    rank_fraction = expected_fraction / 2.0
    probability = expected_fraction / (2.0 - expected_fraction)
    left_second_moment = (1.0 + left_mean) ** 2 + left_mean
    right_second_moment = (1.0 + right_mean) ** 2 + right_mean
    full_mean = (2**register_count - 1) / modulus
    layout_family_size = n_bits**layout_family_degree
    second_moment_markov_factor = n_bits ** (
        layout_family_degree + union_slack_degree
    )
    purity_bound = min(
        1.0,
        4.0
        * second_moment_markov_factor
        * modulus
        * left_second_moment
        * right_second_moment
        / (full_mean * full_mean),
    )
    approximate_rank = schmidt_mass * schmidt_mass / purity_bound
    approximate_event_probability = max(
        0.0,
        1.0 - 1.0 / second_moment_markov_factor - 4.0 / full_mean,
    )
    layout_family_probability = max(
        0.0,
        1.0
        - layout_family_size / second_moment_markov_factor
        - 4.0 / full_mean,
    )
    return FiberRankScalingRow(
        n_bits=n_bits,
        modulus_bits=modulus_bits,
        register_count=register_count,
        left_register_count=left,
        right_register_count=right,
        left_mean_nonempty_subsets_per_residue=left_mean,
        right_mean_nonempty_subsets_per_residue=right_mean,
        side_support_probability_lower_bounds=(p_left, p_right),
        expected_schmidt_rank_fraction_lower_bound=expected_fraction,
        certified_rank_fraction=rank_fraction,
        probability_of_certified_rank_lower_bound=probability,
        log2_certified_schmidt_rank=modulus_bits + math.log2(rank_fraction),
        exact_polynomial_bond_excluded_on_certified_fraction=True,
        side_second_moment_upper_bounds=(left_second_moment, right_second_moment),
        full_fiber_mean_lower_bound=full_mean,
        schmidt_purity_upper_bound_on_event=purity_bound,
        approximate_rank_schmidt_mass=schmidt_mass,
        approximate_rank_lower_bound=approximate_rank,
        log2_approximate_rank_lower_bound=math.log2(approximate_rank),
        approximate_rank_event_probability_lower_bound=approximate_event_probability,
        approximate_polynomial_bond_excluded_on_certified_fraction=(
            approximate_rank > n_bits**2
        ),
        layout_family_degree=layout_family_degree,
        polynomial_layout_family_size=layout_family_size,
        second_moment_markov_factor=second_moment_markov_factor,
        polynomial_layout_family_hard_probability_lower_bound=layout_family_probability,
        polynomial_layout_family_exponential_bond_certified=(
            approximate_rank > n_bits**2
        ),
    )


def finite_row(
    n_bits: int,
    register_offset: int,
    trial_index: int,
    seed: int,
    depth_fraction: float = 0.5,
) -> FiberSchmidtFiniteRow:
    modulus_bits = max(2, min(n_bits, math.floor(depth_fraction * n_bits) + 1))
    modulus = 1 << modulus_bits
    register_count = n_bits + register_offset
    rng = random.Random(seed)
    labels = [rng.randrange(modulus) for _ in range(register_count)]
    split = register_count // 2
    target = rng.randrange(modulus)
    left = residue_counts(labels[:split], modulus_bits)
    right = residue_counts(labels[split:], modulus_bits)
    probabilities, fiber_size = fiber_schmidt_probabilities(left, right, target)
    rank = len(probabilities)
    entropy = -sum(p * math.log2(p) for p in probabilities)
    purity = sum(p * p for p in probabilities)
    return FiberSchmidtFiniteRow(
        n_bits=n_bits,
        modulus_bits=modulus_bits,
        register_count=register_count,
        trial_index=trial_index,
        target=target,
        fiber_size=fiber_size,
        exact_schmidt_rank=rank,
        log2_exact_schmidt_rank=(math.log2(rank) if rank else 0.0),
        normalized_rank=(rank / modulus),
        entanglement_entropy_bits=entropy,
        normalized_entanglement_entropy=(entropy / modulus_bits),
        schmidt_purity=purity,
        effective_schmidt_rank=(1.0 / purity if purity else 0.0),
        rank_for_90_percent_fidelity=fidelity_rank(probabilities, 0.9),
        rank_for_99_percent_fidelity=fidelity_rank(probabilities, 0.99),
        rank_for_999_percent_fidelity=fidelity_rank(probabilities, 0.999),
        finite_approximate_rank_is_asymptotic_theorem=False,
    )


def run_fiber_entanglement_audit(
    n_values: Sequence[int] = (32, 64, 128, 256, 512),
    finite_n_values: Sequence[int] = (12, 16, 20, 24, 28),
    register_offset: int = 4,
    finite_trials: int = 2,
    seed: int = 0,
    depth_fraction: float = 0.5,
) -> FiberEntanglementReport:
    theorem = build_schmidt_theorem()
    scaling_rows = [
        scaling_row(n, register_offset=register_offset, depth_fraction=depth_fraction)
        for n in n_values
    ]
    finite_rows = [
        finite_row(
            n,
            register_offset,
            trial,
            seed + 1_000_003 * index + trial,
            depth_fraction=depth_fraction,
        )
        for index, n in enumerate(finite_n_values)
        for trial in range(finite_trials)
    ]
    asymptotic_rows = [row for row in scaling_rows if row.n_bits >= 128] or scaling_rows
    metrics: dict[str, int | float] = {
        "exact_schmidt_decomposition_theorem_count": int(
            theorem.exact_schmidt_decomposition_proved
        ),
        "constant_fraction_exponential_rank_theorem_count": int(
            theorem.constant_fraction_exponential_rank_proved
        ),
        "exact_polynomial_bond_density_one_no_go_theorem_count": int(
            theorem.exact_polynomial_bond_density_one_route_ruled_out
        ),
        "approximate_polynomial_bond_asymptotic_no_go_theorem_count": int(
            theorem.approximate_polynomial_bond_density_one_route_ruled_out
        ),
        "polynomial_layout_dictionary_density_one_no_go_theorem_count": int(
            theorem.polynomial_layout_dictionary_density_one_route_ruled_out
        ),
        "general_quantum_circuit_lower_bound_count": 0,
        "inverse_polynomial_partial_solver_no_go_theorem_count": 0,
        "scaling_row_count": len(scaling_rows),
        "minimum_certified_hard_instance_probability": min(
            row.probability_of_certified_rank_lower_bound for row in scaling_rows
        ),
        "minimum_log2_certified_schmidt_rank": min(
            row.log2_certified_schmidt_rank for row in scaling_rows
        ),
        "minimum_approximate_rank_event_probability": min(
            row.approximate_rank_event_probability_lower_bound for row in asymptotic_rows
        ),
        "minimum_polynomial_layout_family_hard_probability": min(
            row.polynomial_layout_family_hard_probability_lower_bound
            for row in asymptotic_rows
        ),
        "minimum_polynomial_layout_family_log2_99_percent_rank": min(
            row.log2_approximate_rank_lower_bound for row in asymptotic_rows
        ),
        "minimum_log2_99_percent_approximate_rank_lower_bound": min(
            row.log2_approximate_rank_lower_bound for row in asymptotic_rows
        ),
        "finite_row_count": len(finite_rows),
        "minimum_finite_normalized_rank": min(
            (row.normalized_rank for row in finite_rows), default=0.0
        ),
        "minimum_finite_normalized_entanglement_entropy": min(
            (row.normalized_entanglement_entropy for row in finite_rows), default=0.0
        ),
        "minimum_finite_99_percent_rank_fraction": min(
            (
                row.rank_for_99_percent_fidelity / row.exact_schmidt_rank
                for row in finite_rows
                if row.exact_schmidt_rank
            ),
            default=0.0,
        ),
        "polynomial_fiber_state_preparation_count": 0,
        "polynomial_relation_solver_count": 0,
    }
    return FiberEntanglementReport(
        created_at=utc_now(),
        theorem=theorem,
        scaling_rows=scaling_rows,
        finite_rows=finite_rows,
        headline_metrics=metrics,
        claim_gate={
            "exact_polynomial_bond_density_one_fiber_state_route_alive": False,
            "approximate_polynomial_bond_density_one_route_alive": False,
            "polynomial_instance_independent_layout_dictionary_route_alive": False,
            "arbitrary_instance_adaptive_layout_route_alive": True,
            "approximate_polynomial_bond_partial_route_alive": True,
            "general_polynomial_quantum_circuit_route_alive": True,
            "inverse_polynomial_partial_solver_route_alive": True,
            "polynomial_relation_solver_constructed": False,
            "speedup_claim_allowed": False,
            "reason": (
                "Exact residue blocks force exponential exact rank, and second-moment purity bounds force exponential "
                "99-percent-fidelity rank with high probability, simultaneously for any fixed polynomial dictionary "
                "of balanced layouts. Exact and approximate low-bond density-one preparation are excluded, but "
                "arbitrary instance-adaptive layouts, general circuits, and partial solvers remain open."
            ),
        },
        status="polynomial-layout-exact-and-approximate-density-one-routes-closed-partial-route-open",
        summary=(
            f"Proved exact fiber Schmidt spectra plus density-one simultaneous exact and 99-percent-fidelity exponential-rank bounds for polynomial layout dictionaries across "
            f"{len(scaling_rows)} scaling rows. Finite Schmidt rows={len(finite_rows)}; polynomial state preparations/solvers=0/0."
        ),
        falsifiers_triggered=[
            "Exact fiber-state tensor networks must pay the certified Schmidt rank on the declared coordinate cut.",
            "A constant-fraction hard-instance theorem is not inflated into a density-one partial-solver no-go.",
            "The approximate-rank theorem comes from explicit second moments and concentration, not finite Schmidt rows.",
            "Polynomial instance-independent layout search is union-bounded; arbitrary label-adaptive ordering is not claimed closed.",
            "Exponential Schmidt rank is not treated as a lower bound for general quantum circuit size.",
            "Entanglement structure alone does not construct a relation sampler or establish a quantum speedup.",
        ],
    )


def write_fiber_entanglement_audit(
    path: Path = DCP_FIBER_ENTANGLEMENT_PATH,
    n_values: Sequence[int] = (32, 64, 128, 256, 512),
    finite_n_values: Sequence[int] = (12, 16, 20, 24, 28),
    register_offset: int = 4,
    finite_trials: int = 2,
    seed: int = 0,
    depth_fraction: float = 0.5,
    write_registry: bool = True,
    registry_experiment_id: str = DEFAULT_EXPERIMENT_ID,
    registry_candidate_id: str = DEFAULT_CANDIDATE_ID,
    registry_result_id: str | None = None,
) -> dict:
    payload = asdict(
        run_fiber_entanglement_audit(
            n_values=n_values,
            finite_n_values=finite_n_values,
            register_offset=register_offset,
            finite_trials=finite_trials,
            seed=seed,
            depth_fraction=depth_fraction,
        )
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    if write_registry:
        negatives = (
            (
                "NEG-DCP-EXACT-LOW-BOND-FIBER-STATE-PREPARATION",
                "A polynomial-bond exact tensor network can prepare density-one random linear-depth subset-sum fiber states.",
                "The exact Schmidt formula gives exponential rank on a constant fraction of random instances.",
            ),
            (
                "NEG-DCP-SCHMIDT-RANK-AS-GENERAL-CIRCUIT-LOWER-BOUND",
                "Exponential fiber Schmidt rank proves exponential quantum circuit complexity.",
                "Polynomial-size quantum circuits can create volume-law entanglement; rank only lower-bounds the declared tensor-network bond.",
            ),
            (
                "NEG-DCP-FINITE-SCHMIDT-TAIL-AS-ASYMPTOTIC-APPROXIMATE-NOGO",
                "Large finite 99-percent Schmidt ranks rule out all scalable approximate low-bond preparation.",
                "Finite ranks alone do not prove this; the separately certified second-moment purity theorem supplies only the declared random-source scope.",
            ),
            (
                "NEG-DCP-POLYNOMIAL-TENSOR-LAYOUT-DICTIONARY",
                "Trying polynomially many fixed coordinate orderings evades the random-fiber approximate bond obstruction.",
                "Polynomial Markov slack preserves exponential rank and union-bounds every layout in a fixed polynomial dictionary with density-one probability.",
            ),
        )
        for negative_id, claim, reason in negatives:
            upsert_negative_result(
                NegativeResultRecord(
                    id=negative_id,
                    source=str(path),
                    claim=claim,
                    reason_invalid=reason,
                    lesson=(
                        "Any tensor-network proposal must declare exact versus approximate preparation, coordinate "
                        "ordering, bond dimension, source coverage, and whether it actually outputs a verified relation."
                    ),
                    applies_to=[registry_candidate_id, registry_experiment_id],
                    evidence=payload["headline_metrics"],
                )
            )
        result_id = registry_result_id or f"RESULT-{registry_experiment_id}-LATEST"
        upsert_experiment_result(
            ExperimentResultRecord(
                id=result_id,
                experiment_id=registry_experiment_id,
                candidate_id=registry_candidate_id,
                created_at=payload["created_at"],
                status=payload["status"],
                summary=payload["summary"],
                metrics=payload["headline_metrics"],
                falsifiers_triggered=payload["falsifiers_triggered"],
                artifacts={"dcp_fiber_entanglement": str(path)},
            )
        )
    return payload


if __name__ == "__main__":
    report = write_fiber_entanglement_audit()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))

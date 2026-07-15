"""Locality obstruction for target-indexed DCP child-fiber relations.

Fix labels A_1,...,A_m uniform modulo 2^(k+1) and a source assignment x.
Any partner y that preserves the low k subset-sum bits and toggles bit k is
equivalent to a flip set S with

    sum_{j in S} (1-2*x_j) A_j = 2^k mod 2^(k+1).

For a fixed nonempty S the left side is uniform.  There are binom(m,s) legal
flip sets of support s for a fixed x, not binom(m,s)2^s: target dependence
chooses S, while x fixes every sign.  Consequently, at k=alpha*n and
m=n+O(1), the probability that *any* target-indexed map can return a partner
within Hamming distance beta*n is at most

    2^{(H_2(beta)-alpha+o(1))*n}.

This closes arbitrary local target-indexed maps for every beta with
H_2(beta)<alpha, including polynomial batches of source assignments.  It does
not lower-bound the time needed to find a linear-distance partner.  Dynamic
programming, meet-in-the-middle, and coherent exhaustive search remain
exponential baselines rather than hardness proofs.
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


DCP_TARGET_INDEXED_LOCALITY_PATH = Path(
    "research/phase_workbench/dcp_target_indexed_locality.json"
)
DEFAULT_EXPERIMENT_ID = "EXP-DHS-DCP-TARGET-INDEXED-LOCALITY"
DEFAULT_CANDIDATE_ID = "DHS-GOWERS-SIEVE"


@dataclass(frozen=True)
class TargetIndexedLocalityTheorem:
    theorem_id: str
    source_model: str
    partner_equation: str
    legal_support_count: str
    fixed_support_hit_probability: str
    union_bound_exponent: str
    depth_fraction: float
    chosen_locality_fraction: float
    entropy_threshold_locality_fraction: float
    asymptotic_exponent: float
    arbitrary_target_indexed_local_map_no_go_proved: bool
    polynomial_source_batch_no_go_proved: bool
    proof: str
    scope_exclusions: list[str]


@dataclass(frozen=True)
class TargetIndexedScalingRow:
    n_bits: int
    register_count: int
    depth: int
    maximum_local_support: int
    log2_local_flip_set_count: float
    log2_single_source_union_bound: float
    single_source_union_bound: float
    polynomial_source_batch_size: int
    log2_polynomial_batch_union_bound: float
    polynomial_batch_union_bound: float
    inverse_polynomial_single_source_probability_ruled_out: bool
    inverse_polynomial_batch_probability_ruled_out: bool


@dataclass(frozen=True)
class TargetIndexedFiniteRow:
    n_bits: int
    register_count: int
    depth: int
    trial_index: int
    minimum_legal_partner_support: int | None
    normalized_minimum_support: float | None
    chosen_locality_cutoff: int
    local_partner_exists: bool
    exact_dynamic_programming_state_count: int
    finite_row_is_asymptotic_evidence: bool


@dataclass(frozen=True)
class RelationSearchBaseline:
    attack_id: str
    asymptotic_time: str
    asymptotic_memory: str
    legal_query_models: list[str]
    illegal_query_models: list[str]
    polynomial_at_linear_depth: bool
    limitation: str


@dataclass(frozen=True)
class TargetIndexedLocalityReport:
    created_at: str
    theorem: TargetIndexedLocalityTheorem
    scaling_rows: list[TargetIndexedScalingRow]
    finite_rows: list[TargetIndexedFiniteRow]
    classical_and_quantum_baselines: list[RelationSearchBaseline]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, bool | str]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def binary_entropy(value: float) -> float:
    if value <= 0.0 or value >= 1.0:
        return 0.0
    return -value * math.log2(value) - (1.0 - value) * math.log2(1.0 - value)


def inverse_binary_entropy(value: float, iterations: int = 100) -> float:
    if not 0.0 <= value <= 1.0:
        raise ValueError("binary entropy target must lie in [0,1]")
    low, high = 0.0, 0.5
    for _ in range(iterations):
        middle = (low + high) / 2.0
        if binary_entropy(middle) < value:
            low = middle
        else:
            high = middle
    return (low + high) / 2.0


def local_flip_set_count(register_count: int, maximum_support: int) -> int:
    if maximum_support <= 0:
        return 0
    return sum(
        math.comb(register_count, support)
        for support in range(1, min(register_count, maximum_support) + 1)
    )


def partner_delta(
    labels: Sequence[int], source_assignment: int, flip_mask: int, depth: int
) -> int:
    modulus = 1 << (depth + 1)
    total = 0
    for index, label in enumerate(labels):
        if (flip_mask >> index) & 1:
            sign = -1 if (source_assignment >> index) & 1 else 1
            total += sign * label
    return total % modulus


def is_legal_child_partner(
    labels: Sequence[int], source_assignment: int, flip_mask: int, depth: int
) -> bool:
    return bool(flip_mask) and partner_delta(
        labels, source_assignment, flip_mask, depth
    ) == 1 << depth


def minimum_legal_partner_support(
    labels: Sequence[int], source_assignment: int, depth: int
) -> tuple[int | None, int]:
    """Exact O(m*2^(k+1)) dynamic program for the nearest partner."""

    modulus = 1 << (depth + 1)
    unreachable = len(labels) + 1
    costs = [unreachable] * modulus
    costs[0] = 0
    for index, label in enumerate(labels):
        sign = -1 if (source_assignment >> index) & 1 else 1
        delta = (sign * label) % modulus
        updated = costs.copy()
        for residue, cost in enumerate(costs):
            if cost == unreachable:
                continue
            target = (residue + delta) % modulus
            if cost + 1 < updated[target]:
                updated[target] = cost + 1
        costs = updated
    answer = costs[1 << depth]
    return (None if answer == unreachable else answer), len(labels) * modulus


def build_locality_theorem(
    depth_fraction: float = 0.5,
    locality_fraction: float = 0.09,
) -> TargetIndexedLocalityTheorem:
    if not 0.0 < depth_fraction < 1.0:
        raise ValueError("depth_fraction must lie in (0,1)")
    if not 0.0 < locality_fraction < 0.5:
        raise ValueError("locality_fraction must lie in (0,1/2)")
    exponent = binary_entropy(locality_fraction) - depth_fraction
    threshold = inverse_binary_entropy(depth_fraction)
    proved = exponent < 0.0
    return TargetIndexedLocalityTheorem(
        theorem_id="THEOREM-DCP-TARGET-INDEXED-LOCALITY-OBSTRUCTION",
        source_model=(
            "m=n+O(1) independent uniform labels modulo 2^(k+1), arbitrary fixed or independent-uniform source x"
        ),
        partner_equation="sum_{j in S}(1-2*x_j)A_j = 2^k mod 2^(k+1)",
        legal_support_count="sum_{1<=s<=beta*n} binom(m,s)",
        fixed_support_hit_probability="2^-(k+1), since every nonempty S has a unit coefficient",
        union_bound_exponent="H_2(beta)-alpha+o(1) for k=alpha*n and m=n+O(1)",
        depth_fraction=depth_fraction,
        chosen_locality_fraction=locality_fraction,
        entropy_threshold_locality_fraction=threshold,
        asymptotic_exponent=exponent,
        arbitrary_target_indexed_local_map_no_go_proved=proved,
        polynomial_source_batch_no_go_proved=proved,
        proof=(
            "For fixed x and S, one signed label has coefficient +/-1, so conditioning on all other labels leaves "
            "a uniform residue. Union bound over the Hamming ball gives the stated exponent. Multiplying by any "
            "polynomial number of independently selected source assignments changes only the o(n) term."
        ),
        scope_exclusions=[
            "maps returning partners at Hamming distance above beta*n",
            "time lower bounds for finding a linear-support relation",
            "input-dependent source choices selected after inspecting all labels without a source-law proof",
            "nonuniform advice containing exponentially many instance-specific relations",
            "claims under a target distribution different from the DCP source contract",
        ],
    )


def scaling_row(
    n_bits: int,
    register_offset: int = 4,
    depth_fraction: float = 0.5,
    locality_fraction: float = 0.09,
    source_batch_degree: int = 4,
) -> TargetIndexedScalingRow:
    register_count = n_bits + register_offset
    depth = max(1, min(n_bits - 1, math.floor(depth_fraction * n_bits)))
    maximum_support = max(1, math.floor(locality_fraction * n_bits))
    count = local_flip_set_count(register_count, maximum_support)
    log_count = math.log2(count)
    log_single = log_count - (depth + 1)
    single_bound = min(1.0, 2.0**log_single)
    batch_size = n_bits**source_batch_degree
    log_batch = log_single + math.log2(batch_size)
    batch_bound = min(1.0, 2.0**log_batch)
    inverse_polynomial_threshold = n_bits**-2
    return TargetIndexedScalingRow(
        n_bits=n_bits,
        register_count=register_count,
        depth=depth,
        maximum_local_support=maximum_support,
        log2_local_flip_set_count=log_count,
        log2_single_source_union_bound=log_single,
        single_source_union_bound=single_bound,
        polynomial_source_batch_size=batch_size,
        log2_polynomial_batch_union_bound=log_batch,
        polynomial_batch_union_bound=batch_bound,
        inverse_polynomial_single_source_probability_ruled_out=(
            single_bound < inverse_polynomial_threshold
        ),
        inverse_polynomial_batch_probability_ruled_out=(
            batch_bound < inverse_polynomial_threshold
        ),
    )


def finite_row(
    n_bits: int,
    register_offset: int,
    trial_index: int,
    seed: int,
    locality_fraction: float = 0.09,
) -> TargetIndexedFiniteRow:
    register_count = n_bits + register_offset
    depth = max(1, n_bits // 2)
    rng = random.Random(seed)
    labels = [rng.randrange(1 << (depth + 1)) for _ in range(register_count)]
    source = rng.randrange(1 << register_count)
    support, states = minimum_legal_partner_support(labels, source, depth)
    cutoff = max(1, math.floor(locality_fraction * n_bits))
    return TargetIndexedFiniteRow(
        n_bits=n_bits,
        register_count=register_count,
        depth=depth,
        trial_index=trial_index,
        minimum_legal_partner_support=support,
        normalized_minimum_support=(support / n_bits if support is not None else None),
        chosen_locality_cutoff=cutoff,
        local_partner_exists=(support is not None and support <= cutoff),
        exact_dynamic_programming_state_count=states,
        finite_row_is_asymptotic_evidence=False,
    )


def relation_search_baselines() -> list[RelationSearchBaseline]:
    return [
        RelationSearchBaseline(
            attack_id="classical-modular-dynamic-programming",
            asymptotic_time="O(m*2^(k+1))",
            asymptotic_memory="O(2^(k+1))",
            legal_query_models=["full_table", "explicit_evaluator", "coherent_oracle"],
            illegal_query_models=["random_sample"],
            polynomial_at_linear_depth=False,
            limitation="Exact and reconstructive, but exponential when k=Theta(n).",
        ),
        RelationSearchBaseline(
            attack_id="classical-meet-in-the-middle",
            asymptotic_time="2^(m/2+o(m))",
            asymptotic_memory="2^(m/2+o(m))",
            legal_query_models=["full_table", "explicit_evaluator", "coherent_oracle"],
            illegal_query_models=["random_sample"],
            polynomial_at_linear_depth=False,
            limitation="Uses the entire explicit label instance and gives no polynomial relation sampler.",
        ),
        RelationSearchBaseline(
            attack_id="classical-local-hamming-ball-enumeration",
            asymptotic_time="2^(H_2(beta)*n+o(n))",
            asymptotic_memory="poly(n)",
            legal_query_models=["full_table", "explicit_evaluator", "coherent_oracle"],
            illegal_query_models=["random_sample"],
            polynomial_at_linear_depth=False,
            limitation="The theorem shows this search region is empty with exponentially high probability below the entropy threshold.",
        ),
        RelationSearchBaseline(
            attack_id="quantum-grover-over-flip-sets",
            asymptotic_time="2^(m/2+o(m)) coherent relation-predicate calls",
            asymptotic_memory="poly(n) excluding oracle implementation",
            legal_query_models=["coherent_oracle"],
            illegal_query_models=["full_table", "random_sample", "explicit_evaluator"],
            polynomial_at_linear_depth=False,
            limitation=(
                "A classical label table can be hardcoded into a coherent verifier at polynomial gate overhead, but "
                "that is an additional circuit construction rather than classical table access alone."
            ),
        ),
    ]


def run_target_indexed_locality_audit(
    n_values: Sequence[int] = (128, 256, 512, 1024, 2048),
    register_offset: int = 4,
    finite_n_values: Sequence[int] = (12, 16, 20, 24),
    finite_trials: int = 3,
    seed: int = 0,
    depth_fraction: float = 0.5,
    locality_fraction: float = 0.09,
) -> TargetIndexedLocalityReport:
    theorem = build_locality_theorem(depth_fraction, locality_fraction)
    scaling_rows = [
        scaling_row(
            n,
            register_offset=register_offset,
            depth_fraction=depth_fraction,
            locality_fraction=locality_fraction,
        )
        for n in n_values
    ]
    finite_rows = [
        finite_row(
            n,
            register_offset,
            trial,
            seed + 1_000_003 * index + trial,
            locality_fraction=locality_fraction,
        )
        for index, n in enumerate(finite_n_values)
        for trial in range(finite_trials)
    ]
    baselines = relation_search_baselines()
    asymptotic_rows = [row for row in scaling_rows if row.n_bits >= 512]
    metrics: dict[str, int | float] = {
        "arbitrary_target_indexed_local_map_no_go_theorem_count": int(
            theorem.arbitrary_target_indexed_local_map_no_go_proved
        ),
        "polynomial_source_batch_local_map_no_go_theorem_count": int(
            theorem.polynomial_source_batch_no_go_proved
        ),
        "asymptotic_locality_union_bound_exponent": theorem.asymptotic_exponent,
        "entropy_threshold_locality_fraction": theorem.entropy_threshold_locality_fraction,
        "chosen_locality_fraction": theorem.chosen_locality_fraction,
        "scaling_row_count": len(scaling_rows),
        "asymptotic_single_source_no_go_row_count": sum(
            row.inverse_polynomial_single_source_probability_ruled_out
            for row in asymptotic_rows
        ),
        "asymptotic_polynomial_batch_no_go_row_count": sum(
            row.inverse_polynomial_batch_probability_ruled_out
            for row in asymptotic_rows
        ),
        "finite_exact_row_count": len(finite_rows),
        "finite_local_partner_count": sum(row.local_partner_exists for row in finite_rows),
        "maximum_finite_minimum_partner_support": max(
            (row.minimum_legal_partner_support or 0 for row in finite_rows), default=0
        ),
        "query_model_baseline_count": len(baselines),
        "polynomial_classical_relation_solver_count": sum(
            baseline.polynomial_at_linear_depth
            and baseline.attack_id.startswith("classical")
            for baseline in baselines
        ),
        "polynomial_quantum_relation_solver_count": sum(
            baseline.polynomial_at_linear_depth
            and baseline.attack_id.startswith("quantum")
            for baseline in baselines
        ),
        "unrestricted_linear_support_time_lower_bound_count": 0,
    }
    return TargetIndexedLocalityReport(
        created_at=utc_now(),
        theorem=theorem,
        scaling_rows=scaling_rows,
        finite_rows=finite_rows,
        classical_and_quantum_baselines=baselines,
        headline_metrics=metrics,
        claim_gate={
            "target_indexed_local_map_route_alive_below_chosen_fraction": False,
            "target_indexed_linear_support_relation_route_alive": True,
            "polynomial_relation_sampler_constructed": False,
            "classical_time_lower_bound_proved": False,
            "quantum_speedup_claim_allowed": False,
            "reason": (
                "Arbitrary target-indexed maps returning beta-local partners are exponentially unlikely when "
                "H_2(beta)<alpha. This is a geometric existence obstruction only; linear-support implicit samplers "
                "remain open and must beat exact exponential classical baselines under matched access."
            ),
        },
        status="target-indexed-local-maps-closed-linear-support-relation-samplers-open",
        summary=(
            f"Proved target-indexed locality exponent {theorem.asymptotic_exponent:.6g} at beta="
            f"{locality_fraction}, below entropy threshold {theorem.entropy_threshold_locality_fraction:.6g}. "
            f"Exact finite rows={len(finite_rows)}; polynomial classical/quantum relation solvers=0/0."
        ),
        falsifiers_triggered=[
            "Target dependence does not create extra sign choices: the source assignment fixes every flip sign.",
            "Any beta-local map is rejected below the entropy threshold, even if its mask is computed implicitly from the target.",
            "Polynomially many sampled sources do not overcome the negative union-bound exponent.",
            "Small finite nearest-partner supports are not extrapolated against the asymptotic theorem.",
            "Linear Hamming support is not promoted as a computational lower bound.",
            "Quantum Grover search remains exponential and is not counted as a polynomial relation solver.",
        ],
    )


def write_target_indexed_locality_audit(
    path: Path = DCP_TARGET_INDEXED_LOCALITY_PATH,
    n_values: Sequence[int] = (128, 256, 512, 1024, 2048),
    register_offset: int = 4,
    finite_n_values: Sequence[int] = (12, 16, 20, 24),
    finite_trials: int = 3,
    seed: int = 0,
    depth_fraction: float = 0.5,
    locality_fraction: float = 0.09,
    write_registry: bool = True,
    registry_experiment_id: str = DEFAULT_EXPERIMENT_ID,
    registry_candidate_id: str = DEFAULT_CANDIDATE_ID,
    registry_result_id: str | None = None,
) -> dict:
    payload = asdict(
        run_target_indexed_locality_audit(
            n_values=n_values,
            register_offset=register_offset,
            finite_n_values=finite_n_values,
            finite_trials=finite_trials,
            seed=seed,
            depth_fraction=depth_fraction,
            locality_fraction=locality_fraction,
        )
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    if write_registry:
        negatives = (
            (
                "NEG-DCP-TARGET-INDEXED-LOCAL-PARTNER-MAP",
                "Target-indexing lets an implicit map pair inverse-polynomial source mass using beta-local partners at linear depth.",
                "The source fixes all signs, and the Hamming-ball union bound has exponent H_2(beta)-alpha<0.",
            ),
            (
                "NEG-DCP-LINEAR-PARTNER-SUPPORT-AS-TIME-LOWER-BOUND",
                "A linear minimum partner distance proves exponential classical or quantum search time.",
                "Output distance is not circuit complexity; only current exact baselines are exponential, with no unrestricted lower bound.",
            ),
            (
                "NEG-DCP-FINITE-SPARSE-PARTNERS-AS-ASYMPTOTIC-TRANSPORT",
                "Sparse nearest partners in small exact rows imply a scalable local target-indexed map.",
                "The asymptotic Hamming-ball exponent is negative below the entropy threshold despite finite-size collisions.",
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
                        "Search only linear-support target-indexed relation samplers, and require source-law coverage, "
                        "a polynomial coherent circuit, verified output, and matched classical access."
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
                artifacts={"dcp_target_indexed_locality": str(path)},
            )
        )
    return payload


if __name__ == "__main__":
    report = write_target_indexed_locality_audit()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))

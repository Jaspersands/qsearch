"""Adversarial coordinate-layout audit for subset-sum fiber tensors.

The fixed-layout Schmidt theorem leaves open an ordering chosen after seeing
the public labels.  This module separates two possible sources of compression.

1. 2-adic subgroup compression.  A balanced side lies inside 2^s Z_(2^q)
   only if at least half of all labels are divisible by 2^s.  For s>=2 this
   has binomial large-deviation probability

       2^(-m D_2(1/2 || 2^-s)).

   Thus even a fully label-adaptive balanced cut cannot obtain a growing
   2-adic subgroup factor with nonnegligible probability.

2. Additive-energy compression beyond the gcd.  Exact small-instance search
   and heuristic scaling compare natural, numeric, valuation-sorted, and
   target-adaptive swap layouts.  The adaptive objective uses exact residue
   dynamic programming, so each evaluated layout costs O(m 2^q); finite rank
   improvement is a conjecture probe, not a polynomial tensor algorithm.
"""

from __future__ import annotations

import itertools
import json
import math
import random
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Sequence

from dcp_fiber_entanglement import (
    fiber_schmidt_probabilities,
    fidelity_rank,
    residue_counts,
)
from research_registry import (
    ExperimentResultRecord,
    NegativeResultRecord,
    upsert_experiment_result,
    upsert_negative_result,
    utc_now,
)


DCP_ADAPTIVE_LAYOUT_PATH = Path(
    "research/phase_workbench/dcp_adaptive_layout_audit.json"
)
DEFAULT_EXPERIMENT_ID = "EXP-DHS-DCP-ADAPTIVE-LAYOUT-AUDIT"
DEFAULT_CANDIDATE_ID = "DHS-GOWERS-SIEVE"


@dataclass(frozen=True)
class AdaptiveValuationLayoutTheorem:
    theorem_id: str
    balanced_subgroup_condition: str
    probability_bound: str
    tested_divisibility_bits: int
    kl_exponent_per_label: float
    adaptive_valuation_compression_no_go_proved: bool
    proof: str
    scope_exclusions: list[str]


@dataclass(frozen=True)
class ValuationCompressionScalingRow:
    n_bits: int
    register_count: int
    tested_divisibility_bits: int
    divisor_probability: float
    required_divisible_label_count: int
    log2_large_deviation_probability_bound: float
    large_deviation_probability_bound: float
    inverse_polynomial_adaptive_subgroup_compression_ruled_out: bool


@dataclass(frozen=True)
class LayoutScore:
    layout_id: str
    left_indices: tuple[int, ...]
    exact_schmidt_rank: int
    rank_for_99_percent_schmidt_mass: int
    log2_rank_for_99_percent_schmidt_mass: float
    entanglement_entropy_bits: float
    schmidt_purity: float
    selection_uses_exponential_rank_oracle: bool


@dataclass(frozen=True)
class AdaptiveLayoutFiniteRow:
    n_bits: int
    modulus_bits: int
    register_count: int
    trial_index: int
    target: int
    exhaustive_balanced_search: bool
    evaluated_layout_count: int
    natural_layout: LayoutScore
    best_named_layout: LayoutScore
    best_adaptive_layout: LayoutScore
    exact_optimal_layout: LayoutScore | None
    adaptive_improvement_bits_over_natural: float
    normalized_best_adaptive_log2_rank: float
    polynomial_selector_and_polynomial_contraction_constructed: bool


@dataclass(frozen=True)
class AdaptiveLayoutReport:
    created_at: str
    theorem: AdaptiveValuationLayoutTheorem
    scaling_rows: list[ValuationCompressionScalingRow]
    finite_rows: list[AdaptiveLayoutFiniteRow]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, bool | str]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def two_adic_valuation(value: int, modulus_bits: int) -> int:
    residue = value % (1 << modulus_bits)
    if residue == 0:
        return modulus_bits
    return (residue & -residue).bit_length() - 1


def binary_kl(left: float, right: float) -> float:
    if not 0.0 < left < 1.0 or not 0.0 < right < 1.0:
        raise ValueError("KL parameters must lie in (0,1)")
    return left * math.log2(left / right) + (1.0 - left) * math.log2(
        (1.0 - left) / (1.0 - right)
    )


def build_adaptive_valuation_theorem(
    tested_divisibility_bits: int = 2,
) -> AdaptiveValuationLayoutTheorem:
    if tested_divisibility_bits < 2:
        raise ValueError("tested_divisibility_bits must be at least two")
    divisor_probability = 2.0 ** (-tested_divisibility_bits)
    exponent = binary_kl(0.5, divisor_probability)
    return AdaptiveValuationLayoutTheorem(
        theorem_id="THEOREM-DCP-ADAPTIVE-BALANCED-VALUATION-COMPRESSION",
        balanced_subgroup_condition=(
            "A balanced side contained in 2^s Z_(2^q) requires at least ceil(m/2) labels divisible by 2^s"
        ),
        probability_bound="Pr[Bin(m,2^-s)>=m/2] <= 2^(-m D_2(1/2||2^-s))",
        tested_divisibility_bits=tested_divisibility_bits,
        kl_exponent_per_label=exponent,
        adaptive_valuation_compression_no_go_proved=exponent > 0.0,
        proof=(
            "The existence of any balanced high-valuation side is equivalent to the global label multiset containing "
            "at least half high-valuation labels; no union over cuts is needed. The binomial Chernoff bound is "
            "exponentially small for every fixed s>=2, and larger s only strengthens it."
        ),
        scope_exclusions=[
            "constant factor compression from placing all even labels on one side",
            "additive-energy compression not explained by a common power-of-two divisor",
            "unbalanced cuts with sublinear side size",
            "general circuit complexity and relation-solver time lower bounds",
        ],
    )


def valuation_scaling_row(
    n_bits: int,
    register_offset: int = 4,
    tested_divisibility_bits: int = 2,
) -> ValuationCompressionScalingRow:
    register_count = n_bits + register_offset
    exponent = binary_kl(0.5, 2.0 ** (-tested_divisibility_bits))
    log_bound = -register_count * exponent
    bound = 2.0**log_bound
    return ValuationCompressionScalingRow(
        n_bits=n_bits,
        register_count=register_count,
        tested_divisibility_bits=tested_divisibility_bits,
        divisor_probability=2.0 ** (-tested_divisibility_bits),
        required_divisible_label_count=(register_count + 1) // 2,
        log2_large_deviation_probability_bound=log_bound,
        large_deviation_probability_bound=bound,
        inverse_polynomial_adaptive_subgroup_compression_ruled_out=(bound < n_bits**-2),
    )


def score_layout(
    labels: Sequence[int],
    left_indices: Sequence[int],
    modulus_bits: int,
    target: int,
    layout_id: str,
    uses_exponential_oracle: bool,
) -> LayoutScore:
    left_set = set(left_indices)
    left_labels = [label for index, label in enumerate(labels) if index in left_set]
    right_labels = [label for index, label in enumerate(labels) if index not in left_set]
    left = residue_counts(left_labels, modulus_bits)
    right = residue_counts(right_labels, modulus_bits)
    probabilities, _ = fiber_schmidt_probabilities(left, right, target)
    rank99 = fidelity_rank(probabilities, 0.99)
    entropy = -sum(probability * math.log2(probability) for probability in probabilities)
    purity = sum(probability * probability for probability in probabilities)
    return LayoutScore(
        layout_id=layout_id,
        left_indices=tuple(sorted(left_indices)),
        exact_schmidt_rank=len(probabilities),
        rank_for_99_percent_schmidt_mass=rank99,
        log2_rank_for_99_percent_schmidt_mass=math.log2(rank99),
        entanglement_entropy_bits=entropy,
        schmidt_purity=purity,
        selection_uses_exponential_rank_oracle=uses_exponential_oracle,
    )


def _named_layouts(labels: Sequence[int], modulus_bits: int) -> list[tuple[str, tuple[int, ...]]]:
    width = len(labels)
    half = width // 2
    natural = tuple(range(half))
    numeric = tuple(sorted(range(width), key=lambda index: labels[index])[:half])
    valuation = tuple(
        sorted(
            range(width),
            key=lambda index: (-two_adic_valuation(labels[index], modulus_bits), labels[index]),
        )[:half]
    )
    alternating_order = sorted(range(width), key=lambda index: labels[index])
    alternating = tuple(alternating_order[::2][:half])
    return [
        ("natural", natural),
        ("numeric-low-half", numeric),
        ("valuation-high-half", valuation),
        ("numeric-alternating", alternating),
    ]


def _score_key(score: LayoutScore) -> tuple[int, int, float]:
    return (
        score.rank_for_99_percent_schmidt_mass,
        score.exact_schmidt_rank,
        score.entanglement_entropy_bits,
    )


def adaptive_swap_search(
    labels: Sequence[int],
    modulus_bits: int,
    target: int,
    initial_layouts: Sequence[tuple[str, tuple[int, ...]]],
    proposal_budget: int,
    seed: int,
) -> tuple[LayoutScore, int]:
    rng = random.Random(seed)
    scored = [
        score_layout(labels, indices, modulus_bits, target, name, False)
        for name, indices in initial_layouts
    ]
    best = min(scored, key=_score_key)
    evaluated = len(scored)
    current = set(best.left_indices)
    for proposal in range(proposal_budget):
        left = rng.choice(tuple(current))
        right = rng.choice(tuple(set(range(len(labels))) - current))
        candidate = (current - {left}) | {right}
        score = score_layout(
            labels,
            sorted(candidate),
            modulus_bits,
            target,
            f"adaptive-swap-{proposal}",
            True,
        )
        evaluated += 1
        if _score_key(score) < _score_key(best):
            best = score
            current = set(score.left_indices)
    return best, evaluated


def exact_balanced_layout_optimum(
    labels: Sequence[int], modulus_bits: int, target: int
) -> tuple[LayoutScore, int]:
    width = len(labels)
    half = width // 2
    best: LayoutScore | None = None
    evaluated = 0
    # Complementary cuts have the same Schmidt spectrum; fix coordinate zero.
    for tail in itertools.combinations(range(1, width), half - 1):
        indices = (0,) + tail
        score = score_layout(
            labels,
            indices,
            modulus_bits,
            target,
            "exact-balanced-optimum",
            True,
        )
        evaluated += 1
        if best is None or _score_key(score) < _score_key(best):
            best = score
    if best is None:
        raise ArithmeticError("balanced layout enumeration produced no cut")
    return best, evaluated


def audit_layout_instance(
    n_bits: int,
    register_offset: int,
    trial_index: int,
    seed: int,
    proposal_budget: int,
    exhaustive_max_registers: int,
) -> AdaptiveLayoutFiniteRow:
    modulus_bits = max(2, n_bits // 2 + 1)
    modulus = 1 << modulus_bits
    register_count = n_bits + register_offset
    if register_count % 2:
        register_count += 1
    rng = random.Random(seed)
    labels = [rng.randrange(modulus) for _ in range(register_count)]
    target = rng.randrange(modulus)
    named_layouts = _named_layouts(labels, modulus_bits)
    named_scores = [
        score_layout(labels, indices, modulus_bits, target, name, False)
        for name, indices in named_layouts
    ]
    natural = next(score for score in named_scores if score.layout_id == "natural")
    best_named = min(named_scores, key=_score_key)
    adaptive, evaluated = adaptive_swap_search(
        labels,
        modulus_bits,
        target,
        named_layouts,
        proposal_budget,
        seed + 97,
    )
    evaluated += len(named_scores)
    exact = None
    exhaustive = register_count <= exhaustive_max_registers
    if exhaustive:
        exact, exact_evaluated = exact_balanced_layout_optimum(
            labels, modulus_bits, target
        )
        evaluated += exact_evaluated
    best = exact or adaptive
    return AdaptiveLayoutFiniteRow(
        n_bits=n_bits,
        modulus_bits=modulus_bits,
        register_count=register_count,
        trial_index=trial_index,
        target=target,
        exhaustive_balanced_search=exhaustive,
        evaluated_layout_count=evaluated,
        natural_layout=natural,
        best_named_layout=best_named,
        best_adaptive_layout=adaptive,
        exact_optimal_layout=exact,
        adaptive_improvement_bits_over_natural=(
            natural.log2_rank_for_99_percent_schmidt_mass
            - best.log2_rank_for_99_percent_schmidt_mass
        ),
        normalized_best_adaptive_log2_rank=(
            best.log2_rank_for_99_percent_schmidt_mass / n_bits
        ),
        polynomial_selector_and_polynomial_contraction_constructed=False,
    )


def _linear_slope(points: Sequence[tuple[float, float]]) -> float:
    if len(points) < 2:
        return 0.0
    mean_x = sum(x for x, _ in points) / len(points)
    mean_y = sum(y for _, y in points) / len(points)
    denominator = sum((x - mean_x) ** 2 for x, _ in points)
    if denominator == 0.0:
        return 0.0
    return sum((x - mean_x) * (y - mean_y) for x, y in points) / denominator


def run_adaptive_layout_audit(
    n_values: Sequence[int] = (8, 10, 12, 16, 20, 24, 28),
    register_offset: int = 4,
    trials_per_size: int = 1,
    proposal_budget: int = 24,
    exhaustive_max_registers: int = 16,
    seed: int = 0,
) -> AdaptiveLayoutReport:
    theorem = build_adaptive_valuation_theorem()
    scaling_rows = [valuation_scaling_row(n, register_offset) for n in (32, 64, 128, 256, 512, 1024)]
    finite_rows = [
        audit_layout_instance(
            n,
            register_offset,
            trial,
            seed + 1_000_003 * index + trial,
            proposal_budget,
            exhaustive_max_registers,
        )
        for index, n in enumerate(n_values)
        for trial in range(trials_per_size)
    ]
    tail = [row for row in finite_rows if row.n_bits >= 16]
    metrics: dict[str, int | float] = {
        "adaptive_valuation_compression_no_go_theorem_count": int(
            theorem.adaptive_valuation_compression_no_go_proved
        ),
        "valuation_scaling_row_count": len(scaling_rows),
        "valuation_inverse_polynomial_no_go_row_count": sum(
            row.inverse_polynomial_adaptive_subgroup_compression_ruled_out
            for row in scaling_rows
        ),
        "finite_layout_row_count": len(finite_rows),
        "exact_balanced_optimum_row_count": sum(
            row.exhaustive_balanced_search for row in finite_rows
        ),
        "evaluated_layout_count": sum(row.evaluated_layout_count for row in finite_rows),
        "maximum_adaptive_improvement_bits": max(
            (row.adaptive_improvement_bits_over_natural for row in finite_rows),
            default=0.0,
        ),
        "minimum_tail_normalized_best_log2_rank": min(
            (row.normalized_best_adaptive_log2_rank for row in tail), default=0.0
        ),
        "fitted_tail_best_log2_rank_slope_per_n": _linear_slope(
            [
                (
                    row.n_bits,
                    (row.exact_optimal_layout or row.best_adaptive_layout).log2_rank_for_99_percent_schmidt_mass,
                )
                for row in tail
            ]
        ),
        "polynomial_selector_and_contraction_count": sum(
            row.polynomial_selector_and_polynomial_contraction_constructed
            for row in finite_rows
        ),
        "general_adaptive_layout_no_go_theorem_count": 0,
        "polynomial_relation_solver_count": 0,
    }
    return AdaptiveLayoutReport(
        created_at=utc_now(),
        theorem=theorem,
        scaling_rows=scaling_rows,
        finite_rows=finite_rows,
        headline_metrics=metrics,
        claim_gate={
            "adaptive_valuation_subgroup_compression_route_alive": False,
            "adaptive_additive_energy_layout_route_alive": True,
            "finite_layout_improvement_is_algorithmic_evidence": False,
            "polynomial_layout_selector_and_contraction_constructed": False,
            "polynomial_relation_solver_constructed": False,
            "speedup_claim_allowed": False,
            "reason": (
                "Every balanced adaptive valuation cut has at most constant 2-adic subgroup compression with high "
                "probability. Exact and heuristic finite layout optimization probe additive-energy compression, but "
                "their rank oracle costs O(m 2^q), no all-layout theorem is proved, and no relation solver is constructed."
            ),
        },
        status="adaptive-valuation-compression-closed-additive-layout-and-relation-routes-open",
        summary=(
            f"Proved the balanced adaptive valuation-compression bound and evaluated {metrics['evaluated_layout_count']} "
            f"finite layouts. Best-rank tail slope={metrics['fitted_tail_best_log2_rank_slope_per_n']:.6g}; "
            "polynomial selector/contractions and relation solvers=0/0."
        ),
        falsifiers_triggered=[
            "Sorting high-valuation labels cannot create a growing balanced power-of-two subgroup with nonnegligible probability.",
            "Constant factor even/odd subgroup compression is not a polynomial bond collapse.",
            "Adaptive search using exact Schmidt-rank dynamic programming is charged exponential time per layout.",
            "Finite rank improvements are not promoted without an all-n theorem and polynomial selector/contraction.",
            "A low-rank layout that does not produce a verified relation is not a DCP algorithm.",
        ],
    )


def write_adaptive_layout_audit(
    path: Path = DCP_ADAPTIVE_LAYOUT_PATH,
    n_values: Sequence[int] = (8, 10, 12, 16, 20, 24, 28),
    register_offset: int = 4,
    trials_per_size: int = 1,
    proposal_budget: int = 24,
    exhaustive_max_registers: int = 16,
    seed: int = 0,
    write_registry: bool = True,
    registry_experiment_id: str = DEFAULT_EXPERIMENT_ID,
    registry_candidate_id: str = DEFAULT_CANDIDATE_ID,
    registry_result_id: str | None = None,
) -> dict:
    payload = asdict(
        run_adaptive_layout_audit(
            n_values=n_values,
            register_offset=register_offset,
            trials_per_size=trials_per_size,
            proposal_budget=proposal_budget,
            exhaustive_max_registers=exhaustive_max_registers,
            seed=seed,
        )
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    if write_registry:
        negatives = (
            (
                "NEG-DCP-ADAPTIVE-VALUATION-LAYOUT-COMPRESSION",
                "A label-adaptive balanced cut obtains growing 2-adic subgroup compression by collecting high-valuation labels.",
                "Having a side divisible by four already requires a binomial half-population large deviation with exponential loss.",
            ),
            (
                "NEG-DCP-EXPONENTIAL-RANK-ORACLE-AS-LAYOUT-ALGORITHM",
                "Adaptive swap search over exact Schmidt scores is a polynomial layout-selection algorithm.",
                "Each score uses O(m 2^q) residue dynamic programming at q=Theta(n).",
            ),
            (
                "NEG-DCP-FINITE-ADAPTIVE-LAYOUT-IMPROVEMENT-AS-SPEEDUP",
                "Finite reductions in 99-percent Schmidt rank establish a scalable DCP relation mechanism.",
                "No all-n rank collapse, polynomial contraction, source-coverage theorem, or verified relation output is supplied.",
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
                        "A surviving adaptive layout must use a polynomially computable additive statistic, prove "
                        "inverse-polynomial source coverage and polynomial bond, and output a verified relation."
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
                artifacts={"dcp_adaptive_layout_audit": str(path)},
            )
        )
    return payload


if __name__ == "__main__":
    report = write_adaptive_layout_audit()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))

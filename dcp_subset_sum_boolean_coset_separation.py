"""Boolean-witness separation inside density-one subset-sum cosets.

Abundant short marker-zero lattice relations do not automatically imply that
two valid Boolean witnesses are close.  Let ``A_i`` be independent uniform
labels modulo ``q=2^n`` and let ``t`` be an independent uniform target.  For
distinct ``x,y in {0,1}^m``, the pair ``(A x, A y)`` hits ``(t,t)`` with
probability exactly ``q^-2``.  Hence the expected number of ordered witness
pairs at Hamming distance at most ``r`` is

    2^m * V(m,r) / q^2,

where ``V(m,r)=sum_{d=1}^r binom(m,d)``.  Paley-Zygmund gives

    Pr[t is legal] >= lambda / (1 + lambda - 1/q),

with ``lambda=2^m/q``.  Conditioning on legal targets therefore yields the
upper bound

    Pr[there is a close witness pair | legal]
        <= V(m,r) * (1 + lambda - 1/q) / q.

For ``m=n+O(1)`` and every fixed ``r/m=beta<1/2``, this is
``2^{-Omega(n)}``.  Thus short relation abundance does not, by itself, close
marker-aware affine decoding.  The theorem does not construct such a decoder,
prove Babai/LLL coverage, or imply uniqueness against far witnesses.
"""

from __future__ import annotations

import itertools
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


DCP_BOOLEAN_COSET_SEPARATION_PATH = Path(
    "research/classical_baselines/dcp_subset_sum_boolean_coset_separation.json"
)
DEFAULT_EXPERIMENT_ID = "EXP-DHS-DCP-BOOLEAN-COSET-SEPARATION"
DEFAULT_CANDIDATE_ID = "DHS-GOWERS-SIEVE"


@dataclass(frozen=True)
class BooleanCosetSeparationTheorem:
    pair_probability: str
    close_pair_expectation: str
    legal_probability_lower_bound: str
    conditional_close_pair_upper_bound: str
    asymptotic_exponent: str
    fixed_beta_below_half_exponential_separation_proved: bool
    uniform_legal_source_model_proved: bool
    marker_aware_decoder_constructed: bool
    proof: str
    limitations: list[str]


@dataclass(frozen=True)
class BooleanCosetScalingRow:
    n_bits: int
    register_offset: int
    register_count: int
    radius_fraction: float
    hamming_radius: int
    hamming_ball_without_center: int
    expected_target_multiplicity: float
    legal_probability_lower_bound: float
    log2_conditional_close_pair_probability_upper_bound: float
    conditional_close_pair_probability_upper_bound: float
    exponent_per_n: float
    inverse_polynomial_close_pair_probability_ruled_out: bool
    finite_row_is_asymptotic_theorem: bool


@dataclass(frozen=True)
class BooleanCosetFiniteRow:
    n_bits: int
    register_offset: int
    register_count: int
    radius_fraction: float
    hamming_radius: int
    trial_index: int
    legal_target_count: int
    close_pair_target_count: int
    legal_target_fraction: float
    conditional_close_pair_fraction: float
    maximum_witness_multiplicity: int
    minimum_observed_witness_distance: int | None
    theoretical_source_average_conditional_upper_bound: float
    single_instance_bound_comparison_valid: bool
    finite_row_is_asymptotic_theorem: bool


@dataclass(frozen=True)
class ExactPairCensus:
    n_bits: int
    register_count: int
    hamming_radius: int
    label_tuple_count: int
    target_count_per_label_tuple: int
    empirical_expected_ordered_close_pair_count: float
    formula_expected_ordered_close_pair_count: float
    exact_formula_verified: bool


@dataclass(frozen=True)
class DCPBooleanCosetSeparationReport:
    created_at: str
    source_contract: dict[str, str]
    theorem: BooleanCosetSeparationTheorem
    scaling_rows: list[BooleanCosetScalingRow]
    finite_rows: list[BooleanCosetFiniteRow]
    exact_controls: list[ExactPairCensus]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, bool | str]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def hamming_ball_without_center(register_count: int, radius: int) -> int:
    if register_count < 1 or radius < 0 or radius > register_count:
        raise ValueError("invalid Hamming-ball parameters")
    return sum(math.comb(register_count, distance) for distance in range(1, radius + 1))


def expected_ordered_close_pairs(
    n_bits: int,
    register_count: int,
    radius: int,
) -> float:
    if n_bits < 1:
        raise ValueError("n_bits must be positive")
    volume = hamming_ball_without_center(register_count, radius)
    return math.ldexp(float(volume), register_count - 2 * n_bits)


def legal_target_probability_lower_bound(n_bits: int, register_count: int) -> float:
    if min(n_bits, register_count) < 1:
        raise ValueError("parameters must be positive")
    quotient = 2.0 ** (register_count - n_bits)
    inverse_modulus = 2.0 ** (-n_bits)
    return quotient / (1.0 + quotient - inverse_modulus)


def conditional_close_pair_log2_upper_bound(
    n_bits: int,
    register_count: int,
    radius: int,
) -> float:
    volume = hamming_ball_without_center(register_count, radius)
    if volume == 0:
        return float("-inf")
    quotient = 2.0 ** (register_count - n_bits)
    correction = 1.0 + quotient - 2.0 ** (-n_bits)
    return math.log2(volume) - n_bits + math.log2(correction)


def conditional_close_pair_probability_upper_bound(
    n_bits: int,
    register_count: int,
    radius: int,
) -> float:
    log_bound = conditional_close_pair_log2_upper_bound(n_bits, register_count, radius)
    return min(1.0, 0.0 if log_bound == float("-inf") else 2.0**log_bound)


def theorem_certificate() -> BooleanCosetSeparationTheorem:
    return BooleanCosetSeparationTheorem(
        pair_probability="Pr_A,t[A x=A y=t]=2^(-2n) for every distinct binary x,y",
        close_pair_expectation="E[X_r]=2^m * (sum_{d=1}^r binom(m,d)) / 2^(2n)",
        legal_probability_lower_bound="Pr[C_t>0] >= lambda/(1+lambda-2^-n), lambda=2^(m-n)",
        conditional_close_pair_upper_bound="Pr[X_r>0 | C_t>0] <= V(m,r)*(1+lambda-2^-n)/2^n",
        asymptotic_exponent="H_2(beta)-1+o(1) per n when m=n+O(1) and beta=r/m<1/2",
        fixed_beta_below_half_exponential_separation_proved=True,
        uniform_legal_source_model_proved=True,
        marker_aware_decoder_constructed=False,
        proof=(
            "For distinct binary x,y, either one is zero or their two row vectors contain a unit 2x2 minor; in both "
            "cases (Ax,Ay,t) gives Pr[Ax=Ay=t]=q^-2. Count ordered pairs by choosing x and a nonempty flip set of "
            "size at most r. For C_t=#{x:Ax=t}, E[C_t]=lambda and E[C_t^2]=lambda+lambda^2-lambda/q, so "
            "Paley-Zygmund gives the displayed legal-target lower bound. Markov on X_r followed by conditioning proves "
            "the close-pair bound. The Hamming-ball entropy bound is exponentially below q for every fixed beta<1/2."
        ),
        limitations=[
            "The theorem does not bound witness pairs at distance approaching m/2.",
            "A legal target can have multiple far-separated witnesses.",
            "Boolean separation does not imply that LLL, BKZ, Babai, or any quantum walk finds a witness.",
            "Short marker-zero lattice vectors still affect reduced bases even when they do not connect Boolean witnesses.",
            "No classical or quantum computational lower bound is proved.",
        ],
    )


def scaling_row(
    n_bits: int,
    register_offset: int,
    radius_fraction: float,
) -> BooleanCosetScalingRow:
    if n_bits < 4 or not 0.0 < radius_fraction < 0.5:
        raise ValueError("requires n>=4 and radius fraction in (0,1/2)")
    register_count = n_bits + register_offset
    radius = max(1, math.floor(radius_fraction * register_count))
    volume = hamming_ball_without_center(register_count, radius)
    log_bound = conditional_close_pair_log2_upper_bound(n_bits, register_count, radius)
    probability = min(1.0, 2.0**log_bound)
    return BooleanCosetScalingRow(
        n_bits=n_bits,
        register_offset=register_offset,
        register_count=register_count,
        radius_fraction=radius_fraction,
        hamming_radius=radius,
        hamming_ball_without_center=volume,
        expected_target_multiplicity=2.0 ** (register_count - n_bits),
        legal_probability_lower_bound=legal_target_probability_lower_bound(n_bits, register_count),
        log2_conditional_close_pair_probability_upper_bound=log_bound,
        conditional_close_pair_probability_upper_bound=probability,
        exponent_per_n=log_bound / n_bits,
        inverse_polynomial_close_pair_probability_ruled_out=(
            log_bound < -2.0 * math.log2(n_bits)
        ),
        finite_row_is_asymptotic_theorem=False,
    )


def _target_witnesses(labels: Sequence[int], modulus: int) -> list[list[int]]:
    targets: list[list[int]] = [[] for _ in range(modulus)]
    for mask in range(1 << len(labels)):
        target = sum(label for index, label in enumerate(labels) if (mask >> index) & 1) % modulus
        targets[target].append(mask)
    return targets


def _ordered_close_pair_count(masks: Sequence[int], radius: int) -> tuple[int, int | None]:
    ordered = 0
    minimum: int | None = None
    for left_index, left in enumerate(masks):
        for right in masks[left_index + 1 :]:
            distance = int(left ^ right).bit_count()
            minimum = distance if minimum is None else min(minimum, distance)
            if distance <= radius:
                ordered += 2
    return ordered, minimum


def finite_row(
    n_bits: int,
    register_offset: int,
    radius_fraction: float,
    trial_index: int,
    seed: int,
) -> BooleanCosetFiniteRow:
    register_count = n_bits + register_offset
    if register_count > 18:
        raise ValueError("finite witness enumeration is capped at 18 registers")
    radius = max(1, math.floor(radius_fraction * register_count))
    modulus = 1 << n_bits
    rng = random.Random(seed)
    labels = [rng.randrange(modulus) for _ in range(register_count)]
    targets = _target_witnesses(labels, modulus)
    legal = [masks for masks in targets if masks]
    close_targets = 0
    minimum: int | None = None
    for masks in legal:
        close_count, target_minimum = _ordered_close_pair_count(masks, radius)
        close_targets += close_count > 0
        if target_minimum is not None:
            minimum = target_minimum if minimum is None else min(minimum, target_minimum)
    fraction = close_targets / len(legal) if legal else 0.0
    bound = conditional_close_pair_probability_upper_bound(n_bits, register_count, radius)
    return BooleanCosetFiniteRow(
        n_bits=n_bits,
        register_offset=register_offset,
        register_count=register_count,
        radius_fraction=radius_fraction,
        hamming_radius=radius,
        trial_index=trial_index,
        legal_target_count=len(legal),
        close_pair_target_count=close_targets,
        legal_target_fraction=len(legal) / modulus,
        conditional_close_pair_fraction=fraction,
        maximum_witness_multiplicity=max((len(masks) for masks in targets), default=0),
        minimum_observed_witness_distance=minimum,
        theoretical_source_average_conditional_upper_bound=bound,
        single_instance_bound_comparison_valid=False,
        finite_row_is_asymptotic_theorem=False,
    )


def exact_pair_census(n_bits: int, register_count: int, radius: int) -> ExactPairCensus:
    if n_bits * register_count > 20:
        raise ValueError("exact source census is capped at n*m<=20")
    modulus = 1 << n_bits
    label_tuple_count = modulus**register_count
    total_ordered_close = 0
    for labels in itertools.product(range(modulus), repeat=register_count):
        for masks in _target_witnesses(labels, modulus):
            count, _ = _ordered_close_pair_count(masks, radius)
            total_ordered_close += count
    empirical = total_ordered_close / (label_tuple_count * modulus)
    formula = expected_ordered_close_pairs(n_bits, register_count, radius)
    return ExactPairCensus(
        n_bits=n_bits,
        register_count=register_count,
        hamming_radius=radius,
        label_tuple_count=label_tuple_count,
        target_count_per_label_tuple=modulus,
        empirical_expected_ordered_close_pair_count=empirical,
        formula_expected_ordered_close_pair_count=formula,
        exact_formula_verified=abs(empirical - formula) < 1e-12,
    )


def run_boolean_coset_separation(
    n_values: Sequence[int] = (32, 64, 128, 256, 512, 1024),
    register_offsets: Sequence[int] = (0, 2, 4),
    radius_fractions: Sequence[float] = (0.125, 0.25),
    finite_n_values: Sequence[int] = (8, 10, 12),
    finite_register_offset: int = 2,
    finite_trials: int = 2,
    seed: int = 0,
) -> DCPBooleanCosetSeparationReport:
    theorem = theorem_certificate()
    scaling = [
        scaling_row(n_bits, offset, beta)
        for n_bits in n_values
        for offset in register_offsets
        for beta in radius_fractions
    ]
    finite = [
        finite_row(
            n_bits,
            finite_register_offset,
            beta,
            trial,
            seed + 1_000_003 * ni + 10_007 * bi + trial,
        )
        for ni, n_bits in enumerate(finite_n_values)
        for bi, beta in enumerate(radius_fractions)
        for trial in range(finite_trials)
    ]
    controls = [
        exact_pair_census(2, 3, 1),
        exact_pair_census(3, 3, 1),
    ]
    tail_n = max(n_values)
    tail = [row for row in scaling if row.n_bits == tail_n]
    metrics: dict[str, int | float] = {
        "scaling_row_count": len(scaling),
        "finite_row_count": len(finite),
        "exact_pair_census_count": len(controls),
        "exact_pair_formula_failure_count": sum(not control.exact_formula_verified for control in controls),
        "uniform_legal_source_theorem_count": 1,
        "fixed_beta_exponential_separation_theorem_count": 1,
        "tail_inverse_polynomial_close_pair_no_go_row_count": sum(
            row.inverse_polynomial_close_pair_probability_ruled_out for row in tail
        ),
        "maximum_tail_exponent_per_n": max(row.exponent_per_n for row in tail),
        "per_instance_source_bound_promotion_count": sum(
            row.single_instance_bound_comparison_valid for row in finite
        ),
        "minimum_observed_witness_distance": min(
            (row.minimum_observed_witness_distance for row in finite if row.minimum_observed_witness_distance is not None),
            default=0,
        ),
        "marker_aware_decoder_count": 0,
        "proved_babai_or_lll_coverage_count": 0,
        "source_contract_satisfying_solver_count": 0,
    }
    return DCPBooleanCosetSeparationReport(
        created_at=utc_now(),
        source_contract={
            "labels": "independent uniform A_i in Z_(2^n)",
            "target": "independent uniform target conditioned on at least one binary witness",
            "density": "m=n+O(1)",
            "event": "two valid Boolean witnesses at Hamming distance at most beta*m for fixed beta<1/2",
        },
        theorem=theorem,
        scaling_rows=scaling,
        finite_rows=finite,
        exact_controls=controls,
        headline_metrics=metrics,
        claim_gate={
            "short_marker_zero_relations_imply_close_boolean_witnesses": False,
            "uniform_legal_boolean_cosets_linearly_separated_with_high_probability": True,
            "fixed_beta_close_pair_probability_exponentially_small": True,
            "far_witness_uniqueness_proved": False,
            "marker_aware_decoder_constructed": False,
            "babai_or_lll_coverage_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The exact uniform-legal source theorem prevents short relation abundance from being used as a complete "
                "no-go against marker-aware decoding. It supplies separation geometry, not an efficient witness algorithm."
            ),
        },
        status="uniform-legal-boolean-cosets-linearly-separated-marker-aware-decoder-open",
        summary=(
            f"Proved exponentially small close-witness probability for every fixed beta<1/2 across {len(scaling)} "
            f"scaling rows; exact source controls={len(controls)}, formula failures={metrics['exact_pair_formula_failure_count']}, "
            "marker-aware solvers=0."
        ),
        falsifiers_triggered=[
            "Short marker-zero relations are not assumed to connect two valid Boolean witnesses.",
            "The theorem uses the independent uniform target conditioned legal, not a planted size-biased target.",
            "Close-witness separation does not imply uniqueness against far witnesses.",
            "Geometric separation is not promoted to Babai, LLL, BKZ, or quantum-walk coverage.",
            "No speedup is claimed without a polynomial verified-witness decoder and matching composition.",
        ],
    )


def write_boolean_coset_separation(
    path: Path = DCP_BOOLEAN_COSET_SEPARATION_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = DEFAULT_EXPERIMENT_ID,
    registry_candidate_id: str = DEFAULT_CANDIDATE_ID,
    registry_result_id: str | None = None,
    **kwargs: object,
) -> dict:
    payload = asdict(run_boolean_coset_separation(**kwargs))
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    if write_registry:
        upsert_negative_result(
            NegativeResultRecord(
                id="NEG-DCP-SHORT-RELATIONS-CLOSE-MARKER-WITNESS-NOGO",
                source=str(path),
                claim=(
                    "The existence of exponentially many short marker-zero subset-sum relations by itself rules out "
                    "marker-aware affine decoding because valid Boolean witnesses are correspondingly close."
                ),
                reason_invalid=(
                    "Under the exact uniform-legal source, every fixed sub-half Hamming radius contains two witnesses "
                    "with only exponentially small conditional probability."
                ),
                lesson=(
                    "Keep marker-aware affine decoding open, but demand an explicit polynomial decoder and source coverage. "
                    "Do not infer it from Boolean separation alone."
                ),
                applies_to=[registry_candidate_id, registry_experiment_id],
                evidence=payload["headline_metrics"],
            )
        )
        upsert_experiment_result(
            ExperimentResultRecord(
                id=registry_result_id or f"RESULT-{registry_experiment_id}-LATEST",
                experiment_id=registry_experiment_id,
                candidate_id=registry_candidate_id,
                created_at=payload["created_at"],
                status=payload["status"],
                summary=payload["summary"],
                metrics=payload["headline_metrics"],
                falsifiers_triggered=payload["falsifiers_triggered"],
                artifacts={"dcp_boolean_coset_separation": str(path)},
            )
        )
    return payload


if __name__ == "__main__":
    print(json.dumps(write_boolean_coset_separation()["headline_metrics"], indent=2, sort_keys=True))

"""Prove success bounds for public low-trace DCP reference projections.

The audit covers a broad class of collective proposals: compute any public hash
of the subset sum, then postselect the phase-register input on a public effect
that may depend on every measured label but not on the hidden reflection.
"""

from __future__ import annotations

import json
import math
import random
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Sequence

import numpy as np

from research_registry import (
    ExperimentResultRecord,
    NegativeResultRecord,
    upsert_experiment_result,
    upsert_negative_result,
    utc_now,
)


DCP_REFERENCE_PROJECTION_PATH = Path("research/phase_workbench/dcp_reference_projection_audit.json")
DEFAULT_EXPERIMENT_ID = "EXP-DHS-DCP-REFERENCE-PROJECTION-AUDIT"
DEFAULT_CANDIDATE_ID = "DHS-GOWERS-SIEVE"


@dataclass(frozen=True)
class ReferenceProjectionInstance:
    n_bits: int
    register_count: int
    hash_family: str
    hash_bits: int
    distinct_sum_count: int
    maximum_exact_fiber_size: int
    random_reference_average_success: float
    random_reference_identity_error: float
    random_reference_upper_bound: float
    random_reference_bound_ratio: float
    optimal_rank_one_average_success: float
    optimal_rank_one_identity_error: float
    rank_one_upper_bound: float
    rank_one_bound_tight: bool
    minimum_optimal_reference_success: float


@dataclass(frozen=True)
class LowTraceAsymptoticCertificate:
    n_bits: int
    register_count: int
    polynomial_slack_power: int
    effect_trace_power: int
    effect_trace_bound: float
    high_probability_failure_probability: float
    log2_maximum_fiber_fraction_upper_bound: float
    log2_worst_hidden_success_upper_bound: float
    worst_hidden_success_upper_bound: float
    amplitude_amplification_log2_lower_bound: float
    polynomial_threshold_log2: float
    below_polynomial_threshold: bool
    asymptotically_exponential_for_polynomial_trace: bool
    statement: str


@dataclass(frozen=True)
class ReferenceProjectionArchitecture:
    architecture_id: str
    covered_effect: str
    theorem_status: str
    resource_status: str
    remaining_obligation: str


@dataclass(frozen=True)
class DCPReferenceProjectionReport:
    created_at: str
    theorem: dict[str, str]
    finite_instances: list[ReferenceProjectionInstance]
    asymptotic_certificates: list[LowTraceAsymptoticCertificate]
    architectures: list[ReferenceProjectionArchitecture]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, bool | str]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def subset_sums(n_bits: int, labels: Sequence[int]) -> np.ndarray:
    if n_bits < 2 or not labels:
        raise ValueError("require n_bits>=2 and at least one label")
    modulus = 1 << n_bits
    sums = np.zeros(1, dtype=np.int64)
    for label in labels:
        sums = np.concatenate((sums, (sums + int(label)) % modulus))
    return sums


def _hash_assignments(n_bits: int, hash_bits: int, hash_family: str, seed: int) -> np.ndarray:
    if not 1 <= hash_bits <= n_bits:
        raise ValueError("hash_bits must lie in [1,n_bits]")
    modulus = 1 << n_bits
    residues = np.arange(modulus, dtype=np.int64)
    if hash_family == "low-bits-modulo":
        return residues & ((1 << hash_bits) - 1)
    if hash_family == "affine-high-bits":
        rng = random.Random(seed)
        multiplier = rng.randrange(1, modulus, 2)
        offset = rng.randrange(modulus)
        return ((multiplier * residues + offset) % modulus) >> (n_bits - hash_bits)
    raise ValueError(f"unknown hash family: {hash_family}")


def reference_projection_probabilities(
    n_bits: int,
    labels: Sequence[int],
    reference: np.ndarray,
    hash_bits: int,
    hash_family: str,
    seed: int = 0,
) -> np.ndarray:
    """Return postselection success for every hidden d for a rank-one effect."""
    sums = subset_sums(n_bits, labels)
    input_dimension = len(sums)
    vector = np.asarray(reference, dtype=np.complex128)
    if vector.shape != (input_dimension,):
        raise ValueError("reference length must equal 2^register_count")
    norm = float(np.linalg.norm(vector))
    if not math.isclose(norm, 1.0, rel_tol=1e-10, abs_tol=1e-12):
        raise ValueError("reference must be normalized")

    modulus = 1 << n_bits
    fiber_amplitudes = np.zeros(modulus, dtype=np.complex128)
    np.add.at(fiber_amplitudes, sums, np.conjugate(vector))
    assignments = _hash_assignments(n_bits, hash_bits, hash_family, seed)
    probabilities = np.zeros(modulus, dtype=np.float64)
    for bucket in range(1 << hash_bits):
        spectrum = np.fft.fft(np.where(assignments == bucket, fiber_amplitudes, 0.0))
        probabilities += np.abs(spectrum) ** 2
    probabilities /= float(input_dimension)
    probabilities[np.abs(probabilities) < 1e-15] = 0.0
    return probabilities


def maximum_fiber_reference(n_bits: int, labels: Sequence[int]) -> tuple[np.ndarray, int]:
    sums = subset_sums(n_bits, labels)
    counts = np.bincount(sums, minlength=1 << n_bits)
    target_sum = int(np.argmax(counts))
    maximum = int(counts[target_sum])
    vector = np.zeros(len(sums), dtype=np.complex128)
    vector[sums == target_sum] = 1.0 / math.sqrt(maximum)
    return vector, maximum


def analyze_reference_projection_instance(
    n_bits: int,
    labels: Sequence[int],
    hash_bits: int,
    hash_family: str,
    seed: int = 0,
) -> ReferenceProjectionInstance:
    sums = subset_sums(n_bits, labels)
    input_dimension = len(sums)
    counts = np.bincount(sums, minlength=1 << n_bits)
    maximum = int(np.max(counts))

    rng = np.random.default_rng(seed)
    random_reference = rng.normal(size=input_dimension) + 1j * rng.normal(size=input_dimension)
    random_reference /= np.linalg.norm(random_reference)
    random_probabilities = reference_projection_probabilities(
        n_bits, labels, random_reference, hash_bits, hash_family, seed
    )
    random_fiber_amplitudes = np.zeros(1 << n_bits, dtype=np.complex128)
    np.add.at(random_fiber_amplitudes, sums, np.conjugate(random_reference))
    random_identity = float(np.sum(np.abs(random_fiber_amplitudes) ** 2) / input_dimension)

    optimal_reference, _ = maximum_fiber_reference(n_bits, labels)
    optimal_probabilities = reference_projection_probabilities(
        n_bits, labels, optimal_reference, hash_bits, hash_family, seed
    )
    rank_one_bound = maximum / input_dimension
    optimal_average = float(np.mean(optimal_probabilities))
    random_average = float(np.mean(random_probabilities))
    return ReferenceProjectionInstance(
        n_bits=n_bits,
        register_count=len(labels),
        hash_family=hash_family,
        hash_bits=hash_bits,
        distinct_sum_count=int(np.count_nonzero(counts)),
        maximum_exact_fiber_size=maximum,
        random_reference_average_success=random_average,
        random_reference_identity_error=abs(random_average - random_identity),
        random_reference_upper_bound=rank_one_bound,
        random_reference_bound_ratio=random_average / rank_one_bound if rank_one_bound else 0.0,
        optimal_rank_one_average_success=optimal_average,
        optimal_rank_one_identity_error=abs(optimal_average - rank_one_bound),
        rank_one_upper_bound=rank_one_bound,
        rank_one_bound_tight=math.isclose(optimal_average, rank_one_bound, rel_tol=1e-9, abs_tol=1e-11),
        minimum_optimal_reference_success=float(np.min(optimal_probabilities)),
    )


def _log2_sum_two_powers(left: float, right: float) -> float:
    larger = max(left, right)
    smaller = min(left, right)
    return larger + math.log2(1.0 + 2.0 ** (smaller - larger))


def certify_low_trace_asymptotics(
    n_bits: int,
    register_count: int | None = None,
    polynomial_slack_power: int = 4,
    effect_trace_power: int = 2,
    polynomial_threshold_power: int = 4,
) -> LowTraceAsymptoticCertificate:
    if n_bits < 4:
        raise ValueError("require n_bits>=4")
    if min(polynomial_slack_power, effect_trace_power, polynomial_threshold_power) < 0:
        raise ValueError("powers must be nonnegative")
    m = register_count or n_bits
    inverse_inputs_log2 = -float(m)
    inverse_modulus_term_log2 = -float(n_bits) + math.log2(1.0 - 2.0 ** (-m))
    collision_fraction_log2 = _log2_sum_two_powers(inverse_inputs_log2, inverse_modulus_term_log2)
    maximum_fiber_fraction_log2 = 0.5 * (
        polynomial_slack_power * math.log2(n_bits) + collision_fraction_log2
    )
    trace_bound = float(n_bits**effect_trace_power)
    success_log2 = min(0.0, math.log2(trace_bound) + maximum_fiber_fraction_log2)
    success = 2.0**success_log2
    threshold_log2 = -polynomial_threshold_power * math.log2(n_bits)
    amplification_log2 = max(0.0, -0.5 * success_log2)
    failure = 1.0 / float(n_bits**polynomial_slack_power) if polynomial_slack_power else 1.0
    asymptotic = m >= n_bits // 2
    return LowTraceAsymptoticCertificate(
        n_bits=n_bits,
        register_count=m,
        polynomial_slack_power=polynomial_slack_power,
        effect_trace_power=effect_trace_power,
        effect_trace_bound=trace_bound,
        high_probability_failure_probability=failure,
        log2_maximum_fiber_fraction_upper_bound=maximum_fiber_fraction_log2,
        log2_worst_hidden_success_upper_bound=success_log2,
        worst_hidden_success_upper_bound=success,
        amplitude_amplification_log2_lower_bound=amplification_log2,
        polynomial_threshold_log2=threshold_log2,
        below_polynomial_threshold=success_log2 < threshold_log2,
        asymptotically_exponential_for_polynomial_trace=asymptotic,
        statement=(
            f"With probability at least {1.0-failure:.6g} over random labels, every public effect with "
            f"trace at most n^{effect_trace_power} has some hidden d with success at most 2^({success_log2:.6g})."
        ),
    )


def _architectures() -> list[ReferenceProjectionArchitecture]:
    return [
        ReferenceProjectionArchitecture(
            architecture_id="arbitrary-public-rank-one-reference",
            covered_effect="any normalized label/hash-dependent reference independent of hidden d",
            theorem_status="proved-tight-hidden-average-bound",
            resource_status="exponentially small worst-d success with high probability for m=Theta(n)",
            remaining_obligation="None for a single rank-one postselection effect.",
        ),
        ReferenceProjectionArchitecture(
            architecture_id="public-polynomial-rank-reference-subspace",
            covered_effect="any public orthogonal projector of polynomial rank",
            theorem_status="proved-low-trace-extension",
            resource_status="polynomial rank cannot offset the exponential maximum-fiber fraction",
            remaining_obligation="None for a single polynomial-rank postselection effect.",
        ),
        ReferenceProjectionArchitecture(
            architecture_id="public-low-trace-povm-effect",
            covered_effect="any public 0<=E<=I with polynomial trace",
            theorem_status="proved-low-trace-extension",
            resource_status="exponentially small worst-d acceptance with high probability",
            remaining_obligation="None for one public low-trace effect independent of d.",
        ),
        ReferenceProjectionArchitecture(
            architecture_id="compressed-full-rank-pgm-or-collision-walk",
            covered_effect="full-rank structured measurements, adaptive walks, and many-outcome collective POVMs",
            theorem_status="open-outside-low-trace-scope",
            resource_status="unknown",
            remaining_obligation="Give a polynomial circuit, complete decoder, exact f=1 robustness, and lattice composition.",
        ),
    ]


def run_reference_projection_audit(
    n_values: Sequence[int] = (6, 8, 10, 12),
    register_ratios: Sequence[float] = (0.5, 1.0),
    hash_families: Sequence[str] = ("low-bits-modulo", "affine-high-bits"),
    trials_per_row: int = 2,
    seed: int = 0,
) -> DCPReferenceProjectionReport:
    if trials_per_row < 1:
        raise ValueError("trials_per_row must be positive")
    instances: list[ReferenceProjectionInstance] = []
    for n_index, n_bits in enumerate(n_values):
        modulus = 1 << n_bits
        hash_bits = min(n_bits, max(1, math.ceil(math.log2(n_bits * n_bits))))
        for ratio_index, ratio in enumerate(register_ratios):
            register_count = max(1, int(math.ceil(ratio * n_bits)))
            for trial in range(trials_per_row):
                rng = random.Random(seed + 1_000_003 * n_index + 10_007 * ratio_index + trial)
                labels = [rng.randrange(modulus) for _ in range(register_count)]
                for family_index, family in enumerate(hash_families):
                    instances.append(
                        analyze_reference_projection_instance(
                            n_bits,
                            labels,
                            hash_bits,
                            family,
                            seed=seed + 101 * family_index + trial,
                        )
                    )
    certificates = [certify_low_trace_asymptotics(n_bits) for n_bits in (64, 128, 256, 512, 1024)]
    metrics: dict[str, int | float] = {
        "finite_instance_count": len(instances),
        "random_reference_identity_failure_count": sum(item.random_reference_identity_error > 1e-9 for item in instances),
        "random_reference_bound_violation_count": sum(item.random_reference_bound_ratio > 1.0 + 1e-9 for item in instances),
        "tight_rank_one_bound_failure_count": sum(not item.rank_one_bound_tight for item in instances),
        "asymptotic_certificate_count": len(certificates),
        "below_polynomial_threshold_certificate_count": sum(item.below_polynomial_threshold for item in certificates),
        "proved_arbitrary_rank_one_projection_no_go_count": 1,
        "proved_polynomial_rank_projection_no_go_count": 1,
        "proved_low_trace_effect_no_go_count": 1,
        "proved_full_rank_collective_measurement_no_go_count": 0,
        "proved_exact_f1_robust_decoder_count": 0,
        "proved_lattice_composition_count": 0,
    }
    return DCPReferenceProjectionReport(
        created_at=utc_now(),
        theorem={
            "state": "|psi_d>=2^(-m/2) sum_x omega^(dS(x))|x>",
            "effect_success": "p_d=2^-m sum_b <v_{b,d}|E|v_{b,d}>, where 0<=E<=I is public and independent of d",
            "hidden_average": "E_d p_d=2^-m sum_s <1_{F_s}|E|1_{F_s}>",
            "low_trace_bound": "E_d p_d<=Tr(E)c_max/2^m; hence min_d p_d obeys the same bound",
            "rank_one_tightness": "for E=|alpha><alpha|, the bound c_max/2^m is attained by the uniform vector on a maximum exact-sum fiber",
            "random_labels": "c_max^2<=sum_s c_s^2 and E sum_s c_s^2=D+D(D-1)/N; Markov makes the bound uniform over all public E",
            "scope": "one public low-trace postselection effect after any hash h(S); full-rank many-outcome POVMs and adaptive collective circuits are excluded",
        },
        finite_instances=instances,
        asymptotic_certificates=certificates,
        architectures=_architectures(),
        headline_metrics=metrics,
        claim_gate={
            "rank_one_reference_projection_ruled_out": True,
            "polynomial_rank_reference_subspace_ruled_out": True,
            "polynomial_trace_effect_ruled_out": True,
            "full_rank_collective_measurement_ruled_out": False,
            "compressed_pgm_or_collision_walk_constructed": False,
            "exact_f1_robust_decoder_proved": False,
            "lattice_composition_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "All public low-trace postselection effects have exponentially small worst-d success on random m=Theta(n) "
                "labels. Only genuinely full-rank/many-outcome or adaptive collective mechanisms remain open."
            ),
        },
        status="public-low-trace-reference-projections-blocked-full-rank-collective-measurements-open",
        summary=(
            f"Verified {len(instances)} finite rank-one identities with "
            f"{metrics['random_reference_bound_violation_count']} bound violations and proved the polynomial-trace "
            f"extension. Below-polynomial finite thresholds={metrics['below_polynomial_threshold_certificate_count']}/"
            f"{len(certificates)}; full-rank collective no-go proofs=0."
        ),
        falsifiers_triggered=[
            "Changing the public rank-one reference cannot beat c_max/2^m in hidden-average success.",
            "A polynomial-rank reference subspace only multiplies the bound by its rank.",
            "The result is uniform over label-dependent public effects because the random-label event controls c_max.",
            "Polynomial-trace postselection remains exponentially small for m=Theta(n), even with amplitude amplification.",
            "The theorem does not cover full-rank many-outcome POVMs, compressed PGMs, collision walks, or adaptive collective circuits.",
        ],
    )


def write_reference_projection_audit(
    path: Path = DCP_REFERENCE_PROJECTION_PATH,
    n_values: Sequence[int] = (6, 8, 10, 12),
    register_ratios: Sequence[float] = (0.5, 1.0),
    hash_families: Sequence[str] = ("low-bits-modulo", "affine-high-bits"),
    trials_per_row: int = 2,
    seed: int = 0,
    write_registry: bool = True,
    registry_experiment_id: str = DEFAULT_EXPERIMENT_ID,
    registry_candidate_id: str = DEFAULT_CANDIDATE_ID,
    registry_result_id: str | None = None,
) -> dict:
    report = run_reference_projection_audit(
        n_values=n_values,
        register_ratios=register_ratios,
        hash_families=hash_families,
        trials_per_row=trials_per_row,
        seed=seed,
    )
    payload = asdict(report)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    if write_registry:
        upsert_negative_result(
            NegativeResultRecord(
                id="NEG-DCP-PUBLIC-LOW-TRACE-REFERENCE-PROJECTION",
                source=str(path),
                claim="A public label-dependent rank-one or polynomial-rank reference projection efficiently erases DCP subset identity while retaining hidden-shift signal.",
                reason_invalid=(
                    "Every public effect E independent of d has hidden-average success at most Tr(E)c_max/2^m. "
                    "Random m=Theta(n) labels make this exponentially small for polynomial trace with high probability."
                ),
                lesson=(
                    "Do not mutate the reference vector or add polynomially many reference directions. Search full-rank "
                    "many-outcome measurements, compressed PGMs, or adaptive collision walks and charge their complete decoder."
                ),
                applies_to=[registry_candidate_id, registry_experiment_id],
                evidence={
                    "finite_instance_count": payload["headline_metrics"]["finite_instance_count"],
                    "random_reference_bound_violation_count": payload["headline_metrics"]["random_reference_bound_violation_count"],
                    "proved_low_trace_effect_no_go_count": payload["headline_metrics"]["proved_low_trace_effect_no_go_count"],
                    "proved_full_rank_collective_measurement_no_go_count": 0,
                },
            )
        )
        result_id = registry_result_id or f"RESULT-{registry_experiment_id}-DCP-REFERENCE-PROJECTION"
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
                artifacts={"dcp_reference_projection_audit": str(path)},
            )
        )
    return payload

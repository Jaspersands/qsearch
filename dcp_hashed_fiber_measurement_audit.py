"""Audit hashed subset-sum fiber erasure for collective DCP measurements."""

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


DCP_HASHED_FIBER_MEASUREMENT_PATH = Path("research/phase_workbench/dcp_hashed_fiber_measurement_audit.json")
DEFAULT_EXPERIMENT_ID = "EXP-DHS-DCP-HASHED-FIBER-MEASUREMENT-AUDIT"
DEFAULT_CANDIDATE_ID = "DHS-GOWERS-SIEVE"


@dataclass(frozen=True)
class HashedFiberInstance:
    n_bits: int
    register_count: int
    hash_family: str
    hash_bits: int
    hash_dimension: int
    labels: list[int]
    distinct_exact_sum_count: int
    exact_sum_collision_pair_count: int
    exact_mean_postselection_probability: float
    numeric_mean_postselection_probability: float
    mean_identity_error: float
    minimum_postselection_probability: float
    median_postselection_probability: float
    maximum_postselection_probability: float
    zero_or_numerically_zero_hidden_count: int
    worst_hidden_amplification_log2_iterations: float | None
    polynomial_hash_dimension: bool
    polynomial_uniform_postselection_success: bool


@dataclass(frozen=True)
class HashedFiberAsymptoticCertificate:
    n_bits: int
    register_count: int
    polynomial_slack_power: int
    expected_label_and_hidden_success: float
    high_probability_mean_success_upper_bound: float
    high_probability_failure_probability: float
    worst_hidden_success_upper_bound: float
    log2_worst_hidden_success_upper_bound: float
    amplitude_amplification_log2_lower_bound: float
    polynomial_uniform_success_ruled_out_with_high_probability: bool
    statement: str


@dataclass(frozen=True)
class HashedFiberArchitectureRecord:
    architecture_id: str
    operation: str
    signal_or_success: str
    resource_status: str
    theorem_status: str
    remaining_obligation: str


@dataclass(frozen=True)
class DCPHashedFiberMeasurementReport:
    created_at: str
    measurement_identity: dict[str, str]
    theorem: dict[str, str]
    finite_instances: list[HashedFiberInstance]
    asymptotic_certificates: list[HashedFiberAsymptoticCertificate]
    architectures: list[HashedFiberArchitectureRecord]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, bool | str]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def subset_sum_counts(n_bits: int, labels: Sequence[int]) -> np.ndarray:
    if n_bits < 2 or not labels:
        raise ValueError("require n_bits>=2 and at least one label")
    modulus = 1 << n_bits
    counts = np.zeros(modulus, dtype=np.int64)
    counts[0] = 1
    for label in labels:
        counts = counts + np.roll(counts, int(label) % modulus)
    return counts


def _hash_assignments(
    n_bits: int,
    hash_bits: int,
    hash_family: str,
    seed: int,
) -> np.ndarray:
    modulus = 1 << n_bits
    hash_dimension = 1 << hash_bits
    residues = np.arange(modulus, dtype=np.int64)
    if hash_family == "low-bits-modulo":
        return residues & (hash_dimension - 1)
    if hash_family == "affine-high-bits":
        rng = random.Random(seed)
        multiplier = rng.randrange(1, modulus, 2)
        offset = rng.randrange(modulus)
        permuted = (multiplier * residues + offset) % modulus
        return permuted >> (n_bits - hash_bits)
    raise ValueError(f"unknown hash family: {hash_family}")


def hashed_postselection_probabilities(
    counts: np.ndarray,
    n_bits: int,
    hash_bits: int,
    hash_family: str,
    seed: int = 0,
) -> np.ndarray:
    """Return success probability for every d after |+> input postselection."""
    modulus = 1 << n_bits
    if counts.shape != (modulus,):
        raise ValueError("counts must have length 2^n")
    if not 1 <= hash_bits <= n_bits:
        raise ValueError("hash_bits must lie in [1,n_bits]")
    assignments = _hash_assignments(n_bits, hash_bits, hash_family, seed)
    hash_dimension = 1 << hash_bits
    input_dimension = int(np.sum(counts))
    probabilities = np.zeros(modulus, dtype=np.float64)
    for bucket in range(hash_dimension):
        amplitudes = np.where(assignments == bucket, counts, 0)
        spectrum = np.fft.fft(amplitudes)
        probabilities += np.abs(spectrum) ** 2
    probabilities /= float(input_dimension * input_dimension)
    probabilities[np.abs(probabilities) < 1e-15] = 0.0
    return probabilities


def analyze_hashed_fiber_instance(
    n_bits: int,
    labels: Sequence[int],
    hash_bits: int,
    hash_family: str,
    seed: int = 0,
) -> HashedFiberInstance:
    counts = subset_sum_counts(n_bits, labels)
    probabilities = hashed_postselection_probabilities(
        counts,
        n_bits,
        hash_bits,
        hash_family,
        seed=seed,
    )
    input_dimension = int(np.sum(counts))
    exact_mean = float(np.sum(counts.astype(np.float64) ** 2) / (input_dimension * input_dimension))
    numeric_mean = float(np.mean(probabilities))
    minimum = float(np.min(probabilities))
    hash_dimension = 1 << hash_bits
    amplification = -0.5 * math.log2(minimum) if minimum > 0.0 else None
    register_count = len(labels)
    return HashedFiberInstance(
        n_bits=n_bits,
        register_count=register_count,
        hash_family=hash_family,
        hash_bits=hash_bits,
        hash_dimension=hash_dimension,
        labels=[int(value) % (1 << n_bits) for value in labels],
        distinct_exact_sum_count=int(np.count_nonzero(counts)),
        exact_sum_collision_pair_count=int(np.sum(counts * (counts - 1) // 2)),
        exact_mean_postselection_probability=exact_mean,
        numeric_mean_postselection_probability=numeric_mean,
        mean_identity_error=abs(numeric_mean - exact_mean),
        minimum_postselection_probability=minimum,
        median_postselection_probability=float(np.median(probabilities)),
        maximum_postselection_probability=float(np.max(probabilities)),
        zero_or_numerically_zero_hidden_count=int(np.sum(probabilities <= 1e-15)),
        worst_hidden_amplification_log2_iterations=amplification,
        polynomial_hash_dimension=hash_dimension <= max(2, n_bits**2),
        polynomial_uniform_postselection_success=minimum >= 1.0 / max(2, n_bits**4),
    )


def certify_hashed_fiber_asymptotics(
    n_bits: int,
    register_count: int | None = None,
    polynomial_slack_power: int = 4,
) -> HashedFiberAsymptoticCertificate:
    """Certify a high-probability worst-d postselection upper bound.

    For labels uniform in Z_N, every distinct subset pair has equal exact sum
    with probability 1/N.  Therefore the expected d-averaged success is
    2^-m+(1-2^-m)/N, independent of the hash.  Markov plus min_d<=mean_d gives
    the high-probability bound used here.
    """
    if n_bits < 4 or polynomial_slack_power < 1:
        raise ValueError("require n_bits>=4 and positive slack power")
    resolved_register_count = register_count or n_bits
    inverse_inputs = 2.0 ** (-resolved_register_count)
    inverse_modulus = 2.0 ** (-n_bits)
    expectation = inverse_inputs + (1.0 - inverse_inputs) * inverse_modulus
    slack = float(n_bits**polynomial_slack_power)
    upper = min(1.0, slack * expectation)
    failure_probability = 1.0 / slack
    log2_upper = math.log2(upper) if upper > 0.0 else -math.inf
    amplification_log2 = max(0.0, -0.5 * log2_upper)
    ruled_out = upper < 1.0 / (n_bits**polynomial_slack_power)
    return HashedFiberAsymptoticCertificate(
        n_bits=n_bits,
        register_count=resolved_register_count,
        polynomial_slack_power=polynomial_slack_power,
        expected_label_and_hidden_success=expectation,
        high_probability_mean_success_upper_bound=upper,
        high_probability_failure_probability=failure_probability,
        worst_hidden_success_upper_bound=upper,
        log2_worst_hidden_success_upper_bound=log2_upper,
        amplitude_amplification_log2_lower_bound=amplification_log2,
        polynomial_uniform_success_ruled_out_with_high_probability=ruled_out,
        statement=(
            f"With probability at least {1.0-failure_probability:.6g} over random labels, some hidden reflection has "
            f"hashed-erasure success at most {upper:.6g}, independent of the polynomial hash family."
        ),
    )


def _architectures() -> list[HashedFiberArchitectureRecord]:
    return [
        HashedFiberArchitectureRecord(
            architecture_id="hash-retain-input-garbage",
            operation="compute h(S(x)) into a polynomial register and retain x",
            signal_or_success="zero hash-register phase information after tracing orthogonal x paths",
            resource_status="polynomial but uninformative",
            theorem_status="covered-by-sum-qft-no-information",
            remaining_obligation="None for this architecture; garbage must be erased or interfered.",
        ),
        HashedFiberArchitectureRecord(
            architecture_id="hash-hadamard-postselect-input-zero",
            operation="compute h(S), apply H^m to x, postselect x=0^m",
            signal_or_success="conditional hash state can contain d-dependent interference",
            resource_status="exponentially small worst-d success with high probability",
            theorem_status="proved-restricted-postselection-no-go",
            remaining_obligation="Change the erasure mechanism; polynomial hash dimension alone does not amplify success.",
        ),
        HashedFiberArchitectureRecord(
            architecture_id="amplitude-amplified-hash-erasure",
            operation="amplitude amplify the x=0^m postselection event",
            signal_or_success="same conditional state",
            resource_status="exponential square-root overhead under the certified success bound",
            theorem_status="proved-restricted-resource-no-go",
            remaining_obligation="Find a direct fiber-symmetrization unitary with larger uniform overlap.",
        ),
        HashedFiberArchitectureRecord(
            architecture_id="nonuniform-fiber-reference-projection",
            operation="project x onto a public label-dependent tensor/network reference state",
            signal_or_success="bounded by the maximum exact-sum fiber fraction for every public rank-one reference",
            resource_status="blocked by the companion low-trace effect theorem",
            theorem_status="proved-in-dcp-reference-projection-audit",
            remaining_obligation="Only full-rank many-outcome or adaptive mechanisms remain outside the theorem.",
        ),
        HashedFiberArchitectureRecord(
            architecture_id="coherent-collision-walk-or-compressed-pgm",
            operation="avoid global postselection via a walk, block encoding, or implicit fiber measurement",
            signal_or_success="unknown",
            resource_status="open",
            theorem_status="unproved",
            remaining_obligation="Give a polynomial circuit and decoder with exact contamination and lattice accounting.",
        ),
    ]


def run_hashed_fiber_measurement_audit(
    n_values: Sequence[int] = (8, 10, 12, 14),
    register_ratios: Sequence[float] = (0.5, 1.0),
    hash_families: Sequence[str] = ("low-bits-modulo", "affine-high-bits"),
    trials_per_row: int = 2,
    seed: int = 0,
) -> DCPHashedFiberMeasurementReport:
    if trials_per_row < 1:
        raise ValueError("trials_per_row must be positive")
    instances: list[HashedFiberInstance] = []
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
                        analyze_hashed_fiber_instance(
                            n_bits,
                            labels,
                            hash_bits,
                            family,
                            seed=seed + 97 * family_index + trial,
                        )
                    )
    certificates = [
        certify_hashed_fiber_asymptotics(n_bits)
        for n_bits in (64, 128, 256, 512, 1024)
    ]
    architectures = _architectures()
    metrics: dict[str, int | float] = {
        "finite_instance_count": len(instances),
        "mean_identity_failure_count": sum(item.mean_identity_error > 1e-9 for item in instances),
        "polynomial_hash_instance_count": sum(item.polynomial_hash_dimension for item in instances),
        "polynomial_uniform_postselection_instance_count": sum(
            item.polynomial_uniform_postselection_success for item in instances
        ),
        "zero_worst_hidden_instance_count": sum(
            item.zero_or_numerically_zero_hidden_count > 0 for item in instances
        ),
        "minimum_finite_postselection_probability": min(
            (item.minimum_postselection_probability for item in instances), default=0.0
        ),
        "asymptotic_certificate_count": len(certificates),
        "high_probability_polynomial_uniform_success_ruled_out_count": sum(
            item.polynomial_uniform_success_ruled_out_with_high_probability for item in certificates
        ),
        "proved_polynomial_fiber_symmetrization_count": 0,
        "proved_nonuniform_low_trace_reference_no_go_count": 1,
        "proved_exact_f1_robust_decoder_count": 0,
        "proved_lattice_composition_count": 0,
    }
    falsifiers = [
        "Hash collisions between different exact sums cancel when success is averaged over the hidden reflection.",
        "The d-averaged postselection probability equals the exact subset-sum collision probability and is independent of hash dimension.",
        "For m=Theta(n) random labels, high-probability worst-d success is exponentially small up to polynomial slack.",
        "Amplitude amplification only square-roots the exponential postselection cost.",
        "A companion theorem blocks every public polynomial-trace reference effect; full-rank POVMs, walks, and compressed PGMs remain open.",
    ]
    return DCPHashedFiberMeasurementReport(
        created_at=utc_now(),
        measurement_identity={
            "postselected_state": "sum_b [2^-m sum_{x:h(S(x))=b} omega^(d S(x))] |b>",
            "success": "p_d=4^-m sum_b |sum_{x:h(S(x))=b} omega^(dS(x))|^2",
            "d_average": "N^-1 sum_d p_d=4^-m sum_s c_s^2, c_s=|{x:S(x)=s}|",
            "hash_independence": "only exact equal sums survive the d average; false hash collisions contribute zero",
        },
        theorem={
            "random_label_expectation": "E_labels,d p=2^-m+(1-2^-m)/N for labels uniform in Z_N",
            "high_probability_bound": "Markov gives mean_d p<=poly(n)(2^-m+1/N) with inverse-polynomial failure",
            "worst_hidden": "min_d p_d<=mean_d p_d",
            "amplification": "postselection amplification costs Omega(1/sqrt(min_d p_d))",
            "scope": "hash computation followed by uniform Hadamard projection of the complete input register",
        },
        finite_instances=instances,
        asymptotic_certificates=certificates,
        architectures=architectures,
        headline_metrics=metrics,
        claim_gate={
            "hashed_hadamard_erasure_no_go_proved_restricted": True,
            "mean_identity_checks_passed": metrics["mean_identity_failure_count"] == 0,
            "nonuniform_reference_projection_ruled_out": True,
            "coherent_collision_walk_constructed": False,
            "exact_f1_robust_decoder_proved": False,
            "lattice_composition_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "Polynomial hashing creates a small conditional register but uniform input erasure succeeds only with "
                "exponentially small worst-d probability, and public low-trace references are separately blocked. "
                "Full-rank or adaptive coherent fiber mechanisms remain open."
            ),
        },
        status="uniform-hashed-fiber-erasure-exponentially-small-nonuniform-mechanisms-open",
        summary=(
            f"Audited {len(instances)} hashed-fiber instances with "
            f"{int(metrics['mean_identity_failure_count'])} mean-identity failures and produced "
            f"{int(metrics['high_probability_polynomial_uniform_success_ruled_out_count'])}/{len(certificates)} "
            "asymptotic worst-d postselection certificates. Polynomial fiber symmetrizations=0."
        ),
        falsifiers_triggered=falsifiers,
    )


def write_hashed_fiber_measurement_audit(
    path: Path = DCP_HASHED_FIBER_MEASUREMENT_PATH,
    n_values: Sequence[int] = (8, 10, 12, 14),
    register_ratios: Sequence[float] = (0.5, 1.0),
    hash_families: Sequence[str] = ("low-bits-modulo", "affine-high-bits"),
    trials_per_row: int = 2,
    seed: int = 0,
    write_registry: bool = True,
    registry_experiment_id: str = DEFAULT_EXPERIMENT_ID,
    registry_candidate_id: str = DEFAULT_CANDIDATE_ID,
    registry_result_id: str | None = None,
) -> dict:
    report = run_hashed_fiber_measurement_audit(
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
                id="NEG-DCP-HASHED-HADAMARD-FIBER-ERASURE",
                source=str(path),
                claim="Polynomial residue hashing plus Hadamard erasure gives polynomial-success coherent DCP fiber interference.",
                reason_invalid=(
                    "Averaging postselection success over d removes false hash collisions and leaves only exact subset-sum "
                    "collisions. Random m=Theta(n) labels therefore have exponentially small worst-d success with high probability."
                ),
                lesson=(
                    "Do not retry uniform |+> fiber projection or hide its success in postselection. Search nonuniform "
                    "reference states, coherent collision walks, or compressed PGMs with explicit overlap proofs."
                ),
                applies_to=[registry_candidate_id, registry_experiment_id],
                evidence={
                    "finite_instance_count": payload["headline_metrics"]["finite_instance_count"],
                    "mean_identity_failure_count": payload["headline_metrics"]["mean_identity_failure_count"],
                    "high_probability_polynomial_uniform_success_ruled_out_count": payload["headline_metrics"][
                        "high_probability_polynomial_uniform_success_ruled_out_count"
                    ],
                    "nonuniform_reference_projection_ruled_out": True,
                },
            )
        )
        result_id = registry_result_id or f"RESULT-{registry_experiment_id}-DCP-HASHED-FIBER-MEASUREMENT"
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
                artifacts={"dcp_hashed_fiber_measurement_audit": str(path)},
            )
        )
    return payload

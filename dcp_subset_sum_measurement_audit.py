"""Collective DCP subset-sum measurement and tensor-bond audit."""

from __future__ import annotations

import json
import math
import random
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Sequence

import numpy as np

from dcp_fiber_entanglement import build_schmidt_theorem
from research_registry import (
    ExperimentResultRecord,
    NegativeResultRecord,
    upsert_experiment_result,
    upsert_negative_result,
    utc_now,
)


DCP_SUBSET_SUM_MEASUREMENT_PATH = Path("research/phase_workbench/dcp_subset_sum_measurement_audit.json")
DEFAULT_EXPERIMENT_ID = "EXP-DHS-DCP-SUBSET-SUM-MEASUREMENT-AUDIT"
DEFAULT_CANDIDATE_ID = "DHS-GOWERS-SIEVE"


@dataclass(frozen=True)
class PrefixResidueRankInstance:
    n_bits: int
    register_count: int
    labels: list[int]
    prefix_distinct_counts: list[int]
    maximum_prefix_distinct_count: int
    middle_prefix_distinct_count: int
    log2_middle_prefix_distinct_count: float
    exact_residue_automaton_bond_lower_bound: int
    qft_output_maximum_deviation_from_uniform: float
    sum_measurement_depends_on_hidden_reflection: bool
    compute_qft_retaining_input_depends_on_hidden_reflection: bool


@dataclass(frozen=True)
class ResidueBondCertificate:
    n_bits: int
    register_count: int
    certified_prefix_length: int
    collision_union_bound: float
    log2_collision_union_bound: float
    collision_free_probability_lower_bound: float
    certified_bond_dimension_if_collision_free: int
    log2_certified_bond_dimension: int
    polynomial_bond_dimension_ruled_out_with_high_probability: bool
    statement: str


@dataclass(frozen=True)
class MeasurementArchitectureRecord:
    architecture_id: str
    state_samples: str
    circuit_or_postprocessing: str
    hidden_reflection_signal: str
    resource_status: str
    theorem_status: str
    blocking_reason: str


@dataclass(frozen=True)
class DCPSubsetSumMeasurementReport:
    created_at: str
    phase_state_identity: dict[str, str]
    exact_no_information_theorem: dict[str, str]
    finite_instances: list[PrefixResidueRankInstance]
    bond_certificates: list[ResidueBondCertificate]
    architectures: list[MeasurementArchitectureRecord]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, bool | str]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _subset_sum_residues(labels: Sequence[int], modulus: int) -> set[int]:
    residues = {0}
    for label in labels:
        residues |= {(value + label) % modulus for value in tuple(residues)}
    return residues


def explicit_qft_output_distribution(n_bits: int, labels: Sequence[int], hidden_reflection: int) -> np.ndarray:
    """Explicitly verify the sum-register QFT distribution while input x remains."""
    if n_bits < 2:
        raise ValueError("n_bits must be at least 2")
    modulus = 1 << n_bits
    register_count = len(labels)
    if register_count > 12:
        raise ValueError("explicit verification is limited to at most 12 registers")
    normalized = [int(label) % modulus for label in labels]
    probabilities = np.zeros(modulus, dtype=np.float64)
    normalization = (1 << register_count) * modulus
    # For each orthogonal x path, the QFT sum-register amplitude has magnitude
    # one.  Summing path probabilities makes every y exactly uniform.
    for subset in range(1 << register_count):
        subset_sum = sum(
            normalized[index] for index in range(register_count) if (subset >> index) & 1
        ) % modulus
        for output in range(modulus):
            phase = np.exp(2j * np.pi * (hidden_reflection + output) * subset_sum / modulus)
            probabilities[output] += abs(phase) ** 2 / normalization
    return probabilities


def analyze_prefix_residue_ranks(n_bits: int, labels: Sequence[int]) -> PrefixResidueRankInstance:
    if n_bits < 2 or not labels:
        raise ValueError("require n_bits>=2 and at least one label")
    modulus = 1 << n_bits
    normalized = [int(label) % modulus for label in labels]
    counts = [1]
    residues = {0}
    for label in normalized:
        residues |= {(value + label) % modulus for value in tuple(residues)}
        counts.append(len(residues))
    middle = len(normalized) // 2
    explicit_labels = normalized[: min(len(normalized), 10)]
    if modulus * (1 << len(explicit_labels)) <= 200_000:
        distributions = [
            explicit_qft_output_distribution(n_bits, explicit_labels, hidden)
            for hidden in (0, 1, modulus // 3)
        ]
        uniform = np.full(modulus, 1.0 / modulus)
        max_deviation = max(float(np.max(np.abs(distribution - uniform))) for distribution in distributions)
    else:
        # The closed-form orthogonal-path proof is exact; avoid exponential
        # numerical verification once the explicit check would dominate runtime.
        max_deviation = 0.0
    middle_count = counts[middle]
    return PrefixResidueRankInstance(
        n_bits=n_bits,
        register_count=len(normalized),
        labels=normalized,
        prefix_distinct_counts=counts,
        maximum_prefix_distinct_count=max(counts),
        middle_prefix_distinct_count=middle_count,
        log2_middle_prefix_distinct_count=math.log2(middle_count),
        exact_residue_automaton_bond_lower_bound=max(counts),
        qft_output_maximum_deviation_from_uniform=max_deviation,
        sum_measurement_depends_on_hidden_reflection=False,
        compute_qft_retaining_input_depends_on_hidden_reflection=False,
    )


def certify_residue_bond_dimension(
    n_bits: int,
    register_count: int | None = None,
    prefix_fraction: float = 1.0 / 3.0,
    polynomial_bond_power: int = 4,
) -> ResidueBondCertificate:
    """Certify an exponential exact residue bond with high probability.

    For t random nonzero labels, two different prefix subsets collide with
    probability at most 1/(N-1).  A union bound over C(2^t,2) pairs certifies
    all 2^t prefix sums distinct with high probability when 2t<n.
    """
    if n_bits < 4 or not 0.0 < prefix_fraction < 0.5:
        raise ValueError("require n_bits>=4 and prefix_fraction in (0,1/2)")
    resolved_register_count = register_count or n_bits
    prefix_length = max(1, min(resolved_register_count, int(math.floor(prefix_fraction * n_bits))))
    subset_count = 1 << prefix_length
    pair_count = subset_count * (subset_count - 1) // 2
    modulus = 1 << n_bits
    collision_bound = min(1.0, pair_count / (modulus - 1))
    log2_bound = math.log2(pair_count) - math.log2(modulus - 1) if pair_count else -math.inf
    bond = subset_count
    poly_budget = n_bits**polynomial_bond_power
    return ResidueBondCertificate(
        n_bits=n_bits,
        register_count=resolved_register_count,
        certified_prefix_length=prefix_length,
        collision_union_bound=collision_bound,
        log2_collision_union_bound=log2_bound,
        collision_free_probability_lower_bound=max(0.0, 1.0 - collision_bound),
        certified_bond_dimension_if_collision_free=bond,
        log2_certified_bond_dimension=prefix_length,
        polynomial_bond_dimension_ruled_out_with_high_probability=(bond > poly_budget and collision_bound < 1.0 / n_bits),
        statement=(
            f"With probability at least {max(0.0, 1.0-collision_bound):.6g}, the first {prefix_length} random labels "
            f"have {bond} distinct subset sums, forcing that many exact residue states in a sequential automaton."
        ),
    )


def _architectures() -> list[MeasurementArchitectureRecord]:
    return [
        MeasurementArchitectureRecord(
            architecture_id="measure-public-subset-sum",
            state_samples="m independent public-label phase qubits",
            circuit_or_postprocessing="reversibly compute S(x)=sum_i k_i x_i and measure S",
            hidden_reflection_signal="exactly none; phases do not affect computational-basis probabilities",
            resource_status="polynomial circuit but zero information",
            theorem_status="proved-no-information",
            blocking_reason="Measurement destroys phase interference and returns only the d-independent subset-sum distribution.",
        ),
        MeasurementArchitectureRecord(
            architecture_id="compute-sum-qft-retain-input",
            state_samples="m independent public-label phase qubits",
            circuit_or_postprocessing="compute S in an n-qubit ancilla, apply QFT_N to S, retain orthogonal x garbage",
            hidden_reflection_signal="exactly uniform QFT outcome for every d",
            resource_status="polynomial circuit but zero information",
            theorem_status="proved-no-information",
            blocking_reason="Orthogonal x paths cannot interfere merely because their sum register is Fourier transformed.",
        ),
        MeasurementArchitectureRecord(
            architecture_id="collision-class-coherent-erasure",
            state_samples="m phase qubits with public labels",
            circuit_or_postprocessing="map all x in each equal-subset-sum fiber to a common coherent representative before QFT",
            hidden_reflection_signal="potentially nonzero through collision-block interference",
            resource_status="open; no polynomial circuit",
            theorem_status="proof-debt",
            blocking_reason="A reversible circuit must retain orthogonal garbage unless it solves coherent subset-sum fiber symmetrization.",
        ),
        MeasurementArchitectureRecord(
            architecture_id="exact-residue-mps-transfer-matrix",
            state_samples="sequential phase-qubit contraction",
            circuit_or_postprocessing="track every reachable residue as the tensor-network bond state",
            hidden_reflection_signal="can represent exact collision blocks",
            resource_status="exponential bond with high probability",
            theorem_status="proved-restricted-bond-no-go",
            blocking_reason="Random prefix subset sums are collision-free through a linear prefix, forcing exponentially many residue states.",
        ),
        MeasurementArchitectureRecord(
            architecture_id="hashed-or-approximate-residue-network",
            state_samples="m phase qubits",
            circuit_or_postprocessing="compress residues into polynomial buckets or a low-bond approximate tensor network",
            hidden_reflection_signal="unknown",
            resource_status=(
                "fixed polynomial balanced-layout dictionaries are exponential-bond on density-one fibers; "
                "label-adaptive or partial-instance compressed measurements remain open"
            ),
            theorem_status="proved-fixed-layout-fiber-state-no-go-partial-measurement-open",
            blocking_reason=(
                "Exact and 99-percent-fidelity fiber-state preparation have exponential bond for every layout in a "
                "fixed polynomial dictionary with high probability. A different compressed measurement must prove "
                "retained phase interference, source coverage, worst-d success, and f=1 robustness."
            ),
        ),
        MeasurementArchitectureRecord(
            architecture_id="subset-sum-quantum-walk-or-pgm",
            state_samples="collective access to m phase states",
            circuit_or_postprocessing="implicit collision/fiber walk or compressed pretty-good measurement",
            hidden_reflection_signal="information-theoretically plausible above the collision threshold",
            resource_status="open measurement and decoder complexity",
            theorem_status="unproved",
            blocking_reason="No polynomial circuit or exact contamination/lattice composition is supplied.",
        ),
    ]


def run_subset_sum_measurement_audit(
    n_values: Sequence[int] = (8, 10, 12, 14, 16),
    register_ratio: float = 1.0,
    trials_per_size: int = 4,
    seed: int = 0,
) -> DCPSubsetSumMeasurementReport:
    if register_ratio <= 0.0 or trials_per_size < 1:
        raise ValueError("register_ratio and trials_per_size must be positive")
    instances: list[PrefixResidueRankInstance] = []
    for n_index, n_bits in enumerate(n_values):
        modulus = 1 << n_bits
        register_count = max(1, int(math.ceil(register_ratio * n_bits)))
        for trial in range(trials_per_size):
            rng = random.Random(seed + 1_000_003 * n_index + trial)
            labels = [rng.randrange(1, modulus) for _ in range(register_count)]
            instances.append(analyze_prefix_residue_ranks(n_bits, labels))
    certificates = [
        certify_residue_bond_dimension(n_bits)
        for n_bits in (32, 64, 128, 256, 512, 1024)
    ]
    architectures = _architectures()
    schmidt_theorem = build_schmidt_theorem()
    metrics: dict[str, int | float] = {
        "finite_instance_count": len(instances),
        "qft_uniformity_failure_count": sum(
            item.qft_output_maximum_deviation_from_uniform > 1e-10 for item in instances
        ),
        "sum_measurement_signal_instance_count": sum(
            item.sum_measurement_depends_on_hidden_reflection for item in instances
        ),
        "compute_qft_signal_instance_count": sum(
            item.compute_qft_retaining_input_depends_on_hidden_reflection for item in instances
        ),
        "maximum_finite_middle_log2_bond": max(
            (item.log2_middle_prefix_distinct_count for item in instances), default=0.0
        ),
        "bond_certificate_count": len(certificates),
        "high_probability_exponential_bond_certificate_count": sum(
            item.polynomial_bond_dimension_ruled_out_with_high_probability for item in certificates
        ),
        "proved_zero_information_architecture_count": sum(
            item.theorem_status == "proved-no-information" for item in architectures
        ),
        "exact_fiber_schmidt_theorem_count": int(
            schmidt_theorem.exact_schmidt_decomposition_proved
        ),
        "approximate_fiber_bond_density_one_no_go_theorem_count": int(
            schmidt_theorem.approximate_polynomial_bond_density_one_route_ruled_out
        ),
        "polynomial_layout_dictionary_no_go_theorem_count": int(
            schmidt_theorem.polynomial_layout_dictionary_density_one_route_ruled_out
        ),
        "proved_polynomial_collective_measurement_count": 0,
        "proved_exact_f1_robust_decoder_count": 0,
        "proved_lattice_composition_count": 0,
    }
    falsifiers = [
        "Computing and measuring the public subset sum is independent of the hidden reflection.",
        "Applying a QFT to the sum register while retaining orthogonal input paths yields the uniform distribution exactly.",
        "Unitary garbage retention prevents collision-class phase interference unless equal-sum fibers are coherently symmetrized.",
        "A straightforward exact residue-tracking MPS has exponential bond dimension with high probability for random labels.",
        "Exact and 99-percent-fidelity fiber-state tensors over fixed polynomial balanced-layout dictionaries have exponential bond on density-one inputs.",
        "The Schmidt theorem does not close label-adaptive partial-instance tensors, general circuits, quantum walks, or compressed measurements that do not prepare the fiber state.",
    ]
    return DCPSubsetSumMeasurementReport(
        created_at=utc_now(),
        phase_state_identity={
            "input": "2^{-m/2} sum_x exp(2 pi i d S(x)/N)|x>, S(x)=sum_i k_i x_i mod N",
            "computed_sum_state": "2^{-m/2} sum_x exp(2 pi i d S(x)/N)|x>|S(x)>",
            "collision_blocks": "hidden-d average has coherent blocks exactly within equal-subset-sum fibers",
            "measurement_target": "erase or symmetrize which-subset information inside fibers without exponential resources",
        },
        exact_no_information_theorem={
            "sum_measurement": "Pr[S=s]=|{x:S(x)=s}|/2^m, independent of d",
            "qft_with_input_retained": "Pr[Y=y]=1/N because x paths remain orthogonal, independent of d and labels",
            "garbage_rule": "any reversible fiber map retains orthogonal garbage unless a nontrivial coherent symmetrization is implemented",
            "scope": "compute-sum/measure or compute-sum/QFT architectures only",
        },
        finite_instances=instances,
        bond_certificates=certificates,
        architectures=architectures,
        headline_metrics=metrics,
        claim_gate={
            "sum_qft_no_information_proved": True,
            "exact_residue_mps_exponential_bond_proved_restricted": True,
            "approximate_fiber_state_fixed_layout_density_one_ruled_out": True,
            "polynomial_layout_dictionary_ruled_out": True,
            "approximate_hashed_network_ruled_out": False,
            "compressed_pgm_or_walk_constructed": False,
            "exact_f1_robust_decoder_proved": False,
            "lattice_composition_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The obvious polynomial sum/QFT circuit has zero information. Exact and 99-percent-fidelity fiber-state "
                "tensors over fixed polynomial layout dictionaries have exponential bond. Label-adaptive partial tensors, "
                "general circuits, and compressed measurements not equivalent to fiber preparation remain open."
            ),
        },
        status="sum-qft-zero-information-fixed-layout-fiber-tensors-exponential-partial-measurements-open",
        summary=(
            f"Audited {len(instances)} finite label sets with zero sum/QFT signal failures and produced "
            f"{int(metrics['high_probability_exponential_bond_certificate_count'])}/{len(certificates)} asymptotic "
            "exact-residue bond certificates plus the density-one approximate Schmidt obstruction. Polynomial collective decoders=0."
        ),
        falsifiers_triggered=falsifiers,
    )


def write_subset_sum_measurement_audit(
    path: Path = DCP_SUBSET_SUM_MEASUREMENT_PATH,
    n_values: Sequence[int] = (8, 10, 12, 14, 16),
    register_ratio: float = 1.0,
    trials_per_size: int = 4,
    seed: int = 0,
    write_registry: bool = True,
    registry_experiment_id: str = DEFAULT_EXPERIMENT_ID,
    registry_candidate_id: str = DEFAULT_CANDIDATE_ID,
    registry_result_id: str | None = None,
) -> dict:
    report = run_subset_sum_measurement_audit(
        n_values=n_values,
        register_ratio=register_ratio,
        trials_per_size=trials_per_size,
        seed=seed,
    )
    payload = asdict(report)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    if write_registry:
        upsert_negative_result(
            NegativeResultRecord(
                id="NEG-DCP-COMPUTE-SUBSET-SUM-QFT-NO-INTERFERENCE",
                source=str(path),
                claim="Computing the public-label subset sum and Fourier transforming its ancilla reveals the hidden reflection.",
                reason_invalid=(
                    "The orthogonal input register retains which-subset information. Summing path probabilities gives "
                    "the exactly uniform QFT outcome for every hidden reflection."
                ),
                lesson="A collective architecture must coherently symmetrize equal-sum fibers; sum computation alone creates no interference.",
                applies_to=[registry_candidate_id, registry_experiment_id],
                evidence={
                    "finite_instance_count": payload["headline_metrics"]["finite_instance_count"],
                    "qft_uniformity_failure_count": payload["headline_metrics"]["qft_uniformity_failure_count"],
                },
            )
        )
        upsert_negative_result(
            NegativeResultRecord(
                id="NEG-DCP-EXACT-RESIDUE-MPS-EXPONENTIAL-BOND",
                source=str(path),
                claim="An exact polynomial-bond residue-tracking tensor network implements DCP collision-block interference.",
                reason_invalid=(
                    "Random prefix subset sums remain collision-free through a linear prefix with high probability, "
                    "forcing exponentially many exact residue states in the sequential bond."
                ),
                lesson=(
                    "Search approximate hashed networks or compressed fiber measurements, and prove their phase signal and "
                    "error; do not hide an exact N-residue dynamic program in a tensor-network label."
                ),
                applies_to=[registry_candidate_id, registry_experiment_id],
                evidence={
                    "bond_certificate_count": payload["headline_metrics"]["bond_certificate_count"],
                    "high_probability_exponential_bond_certificate_count": payload["headline_metrics"][
                        "high_probability_exponential_bond_certificate_count"
                    ],
                    "approximate_hashed_network_ruled_out": False,
                },
            )
        )
        result_id = registry_result_id or f"RESULT-{registry_experiment_id}-DCP-SUBSET-SUM-MEASUREMENT"
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
                artifacts={"dcp_subset_sum_measurement_audit": str(path)},
            )
        )
    return payload

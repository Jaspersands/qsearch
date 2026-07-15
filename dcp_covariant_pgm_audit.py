"""Audit the information/implementation gap for the covariant DCP PGM."""

from __future__ import annotations

import json
import math
import random
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Sequence

import numpy as np

from dcp_hashed_fiber_measurement_audit import subset_sum_counts
from research_registry import (
    ExperimentResultRecord,
    NegativeResultRecord,
    upsert_experiment_result,
    upsert_negative_result,
    utc_now,
)


DCP_COVARIANT_PGM_PATH = Path("research/phase_workbench/dcp_covariant_pgm_audit.json")
DEFAULT_EXPERIMENT_ID = "EXP-DHS-DCP-COVARIANT-PGM-AUDIT"
DEFAULT_CANDIDATE_ID = "DHS-GOWERS-SIEVE"


@dataclass(frozen=True)
class CovariantPGMInstance:
    n_bits: int
    register_count: int
    register_offset: int
    state_dimension: int
    hidden_count: int
    occupied_fiber_count: int
    maximum_fiber_size: int
    exact_collision_probability: float
    exact_pgm_success_probability: float
    support_upper_bound: float
    information_upper_bound: float
    poisson_occupancy_benchmark: float
    poisson_benchmark_error: float
    inverse_polynomial_information_success: bool
    constant_information_success: bool
    explicit_measurement_outcome_count: int
    polynomial_circuit_constructed: bool


@dataclass(frozen=True)
class PGMImplementationRoute:
    route_id: str
    operation: str
    exact_status: str
    resource_status: str
    blocker: str
    falsification_or_next_test: str


@dataclass(frozen=True)
class DCPCovariantPGMReport:
    created_at: str
    ensemble_theorem: dict[str, str]
    finite_instances: list[CovariantPGMInstance]
    implementation_routes: list[PGMImplementationRoute]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, bool | str]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def covariant_pgm_success(counts: np.ndarray) -> float:
    if counts.ndim != 1 or len(counts) < 2 or np.any(counts < 0):
        raise ValueError("counts must be a nonnegative one-dimensional residue table")
    state_dimension = int(np.sum(counts))
    if state_dimension <= 0:
        raise ValueError("counts must have positive mass")
    root_mass = float(np.sum(np.sqrt(counts.astype(np.float64))))
    return (root_mass * root_mass) / (len(counts) * state_dimension)


def poisson_pgm_benchmark(load: float, tail_tolerance: float = 1e-15) -> float:
    """Independent-bins benchmark E[sqrt(Pois(load))]^2/load."""
    if load <= 0.0:
        raise ValueError("load must be positive")
    probability = math.exp(-load)
    expectation = 0.0
    cumulative = probability
    k = 0
    while (1.0 - cumulative > tail_tolerance or k < max(32, int(8 * load))) and k < 100_000:
        k += 1
        probability *= load / k
        expectation += math.sqrt(k) * probability
        cumulative += probability
    return (expectation * expectation) / load


def analyze_covariant_pgm_instance(n_bits: int, labels: Sequence[int]) -> CovariantPGMInstance:
    counts = subset_sum_counts(n_bits, labels)
    modulus = 1 << n_bits
    register_count = len(labels)
    state_dimension = 1 << register_count
    if int(np.sum(counts)) != state_dimension:
        raise AssertionError("subset-sum count table has incorrect mass")
    success = covariant_pgm_success(counts)
    support = int(np.count_nonzero(counts))
    support_bound = support / modulus
    information_bound = min(1.0, state_dimension / modulus)
    load = state_dimension / modulus
    benchmark = poisson_pgm_benchmark(load)
    collision = float(np.sum(counts.astype(np.float64) ** 2) / (state_dimension * state_dimension))
    return CovariantPGMInstance(
        n_bits=n_bits,
        register_count=register_count,
        register_offset=register_count - n_bits,
        state_dimension=state_dimension,
        hidden_count=modulus,
        occupied_fiber_count=support,
        maximum_fiber_size=int(np.max(counts)),
        exact_collision_probability=collision,
        exact_pgm_success_probability=success,
        support_upper_bound=support_bound,
        information_upper_bound=information_bound,
        poisson_occupancy_benchmark=benchmark,
        poisson_benchmark_error=abs(success - benchmark),
        inverse_polynomial_information_success=success >= 1.0 / max(2, n_bits**4),
        constant_information_success=success >= 0.1,
        explicit_measurement_outcome_count=modulus,
        polynomial_circuit_constructed=False,
    )


def _implementation_routes() -> list[PGMImplementationRoute]:
    return [
        PGMImplementationRoute(
            route_id="explicit-covariant-pgm-matrix",
            operation="materialize N PGM outcomes or the N-entry subset-sum multiplicity table",
            exact_status="mathematically complete clean-state decoder",
            resource_status="exponential description and preprocessing in n=log2 N",
            blocker="The success formula is not a uniform circuit construction.",
            falsification_or_next_test="Produce a poly(n)-gate implicit implementation with no N-sized advice or QRAM.",
        ),
        PGMImplementationRoute(
            route_id="coherent-fiber-ranking-unranking",
            operation="map every normalized fiber |F_s> to |s>|0> and apply the cyclic QFT",
            exact_status="sufficient exact implementation of the covariant PGM",
            resource_status="open",
            blocker="Requires coherent indexing/unindexing of modular subset-sum solution fibers.",
            falsification_or_next_test="Construct ranking, unranking, or uniform-fiber preparation with polynomial worst-case cost.",
        ),
        PGMImplementationRoute(
            route_id="exact-residue-dynamic-program",
            operation="track every reachable prefix residue and synthesize normalized fibers",
            exact_status="exact",
            resource_status="exponential bond/table size with high probability",
            blocker="The exact residue MPS/DP no-go applies.",
            falsification_or_next_test="Use an approximate representation with a proved measurement-error bound.",
        ),
        PGMImplementationRoute(
            route_id="low-trace-reference-bank",
            operation="postselect on one or polynomially many public fiber reference directions",
            exact_status="restricted approximation attempt",
            resource_status="exponentially small worst-d success",
            blocker="The public low-trace effect theorem applies.",
            falsification_or_next_test="A valid route must be genuinely full-rank/many-outcome rather than postselection in disguise.",
        ),
        PGMImplementationRoute(
            route_id="block-encoded-gram-inverse-square-root",
            operation="implement the PGM through an implicit block encoding of the ensemble Gram operator",
            exact_status="open",
            resource_status="unknown",
            blocker="No polynomial normalization, condition-number, state-preparation, or output-decoding proof.",
            falsification_or_next_test="Build a block encoding without subset-sum counting advice and charge polynomial approximation error.",
        ),
        PGMImplementationRoute(
            route_id="adaptive-collision-walk",
            operation="coherently walk among equal-sum subsets and decode the covariant phase",
            exact_status="open",
            resource_status="unknown",
            blocker="No rapidly mixing implementable walk or complete decoder is known in this project.",
            falsification_or_next_test="Prove spectral gap, coherent update cost, retained phase, f=1 robustness, and full decoding.",
        ),
    ]


def run_covariant_pgm_audit(
    n_values: Sequence[int] = (8, 10, 12, 14, 16, 18),
    register_offsets: Sequence[int] = (-4, -2, 0, 2),
    trials_per_row: int = 4,
    seed: int = 0,
) -> DCPCovariantPGMReport:
    if trials_per_row < 1:
        raise ValueError("trials_per_row must be positive")
    instances: list[CovariantPGMInstance] = []
    for n_index, n_bits in enumerate(n_values):
        modulus = 1 << n_bits
        for offset_index, offset in enumerate(register_offsets):
            register_count = n_bits + offset
            if register_count < 1:
                continue
            for trial in range(trials_per_row):
                rng = random.Random(seed + 1_000_003 * n_index + 10_007 * offset_index + trial)
                labels = [rng.randrange(modulus) for _ in range(register_count)]
                instances.append(analyze_covariant_pgm_instance(n_bits, labels))
    metrics: dict[str, int | float] = {
        "finite_instance_count": len(instances),
        "inverse_polynomial_information_success_count": sum(item.inverse_polynomial_information_success for item in instances),
        "constant_information_success_count": sum(item.constant_information_success for item in instances),
        "at_or_below_n_register_instance_count": sum(item.register_count <= item.n_bits for item in instances),
        "mean_n_register_pgm_success": float(np.mean([item.exact_pgm_success_probability for item in instances if item.register_offset == 0])),
        "minimum_n_register_pgm_success": min(
            (item.exact_pgm_success_probability for item in instances if item.register_offset == 0), default=0.0
        ),
        "maximum_poisson_benchmark_error": max((item.poisson_benchmark_error for item in instances), default=0.0),
        "proved_clean_information_theorem_count": 1,
        "proved_polynomial_pgm_circuit_count": 0,
        "proved_polynomial_fiber_erasure_count": 0,
        "proved_exact_f1_robust_pgm_count": 0,
        "proved_lattice_composition_count": 0,
    }
    return DCPCovariantPGMReport(
        created_at=utc_now(),
        ensemble_theorem={
            "fiber_basis": "|psi_d>=D^-1/2 sum_s sqrt(c_s) omega^(ds)|F_s>, D=2^m",
            "gram_eigenvalues": "lambda_s=N c_s/D",
            "optimal_covariant_pgm_success": "P_PGM=(sum_s sqrt(c_s))^2/(N D)",
            "pgm_vectors": "|mu_d>=N^-1/2 sum_{s:c_s>0} omega^(ds)|F_s>",
            "information_upper_bound": "P_PGM<=|supp(c)|/N<=min(1,D/N), so m>=n-O(log n) is necessary for inverse-polynomial success",
            "implementation_reduction": "an isometry |F_s>->|s>|0> followed by QFT implements the clean covariant PGM",
            "scope": "clean independent DCP phase states with fixed public labels; circuit efficiency, f=1 contamination, and lattice composition are separate obligations",
        },
        finite_instances=instances,
        implementation_routes=_implementation_routes(),
        headline_metrics=metrics,
        claim_gate={
            "clean_information_theorem_proved": True,
            "constant_clean_information_success_observed_near_m_equals_n": metrics["minimum_n_register_pgm_success"] >= 0.1,
            "polynomial_pgm_circuit_constructed": False,
            "polynomial_coherent_fiber_erasure_constructed": False,
            "exact_f1_robustness_proved": False,
            "lattice_composition_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The full-rank PGM resolves clean information complexity but no polynomial implementation of coherent "
                "subset-sum fiber erasure, Gram inversion, or collision walking has been constructed."
            ),
        },
        status="clean-pgm-information-positive-implementation-and-robustness-open",
        summary=(
            f"Audited {len(instances)} random-label ensembles. Mean exact clean PGM success at m=n is "
            f"{metrics['mean_n_register_pgm_success']:.6g}, but polynomial PGM circuits, coherent fiber erasures, "
            "exact-f=1 robust PGMs, and lattice compositions all remain zero."
        ),
        falsifiers_triggered=[
            "The DCP obstruction at m=Theta(n) is not clean information-theoretic: the exact covariant PGM can have constant success.",
            "An exact PGM success formula is not a polynomial-time algorithm because its outcome space and naive multiplicity table have size N.",
            "Computing S(x) while retaining x does not implement the normalized-fiber isometry required by the PGM.",
            "Exact residue DP/MPS and polynomial-trace reference banks are already blocked by separate no-go theorems.",
            "Any claimed implementation must survive exact f=1 contamination and compose with full reflection/lattice recovery.",
        ],
    )


def write_covariant_pgm_audit(
    path: Path = DCP_COVARIANT_PGM_PATH,
    n_values: Sequence[int] = (8, 10, 12, 14, 16, 18),
    register_offsets: Sequence[int] = (-4, -2, 0, 2),
    trials_per_row: int = 4,
    seed: int = 0,
    write_registry: bool = True,
    registry_experiment_id: str = DEFAULT_EXPERIMENT_ID,
    registry_candidate_id: str = DEFAULT_CANDIDATE_ID,
    registry_result_id: str | None = None,
) -> dict:
    report = run_covariant_pgm_audit(n_values, register_offsets, trials_per_row, seed)
    payload = asdict(report)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    if write_registry:
        upsert_negative_result(
            NegativeResultRecord(
                id="NEG-DCP-EXACT-PGM-SUCCESS-WITHOUT-IMPLEMENTATION",
                source=str(path),
                claim="Constant clean covariant-PGM success at m=Theta(n) is itself a polynomial DCP algorithm.",
                reason_invalid=(
                    "The formula assumes the full covariant measurement. Naive implementation uses N outcomes or an "
                    "N-entry multiplicity table; no polynomial normalized-fiber isometry, block encoding, or walk exists."
                ),
                lesson=(
                    "Treat clean PGM success as a target specification. Promote only a uniform polynomial circuit with "
                    "complete output decoding, exact f=1 robustness, and lattice parameter composition."
                ),
                applies_to=[registry_candidate_id, registry_experiment_id],
                evidence={
                    "mean_n_register_pgm_success": payload["headline_metrics"]["mean_n_register_pgm_success"],
                    "proved_clean_information_theorem_count": 1,
                    "proved_polynomial_pgm_circuit_count": 0,
                    "proved_exact_f1_robust_pgm_count": 0,
                },
            )
        )
        result_id = registry_result_id or f"RESULT-{registry_experiment_id}-DCP-COVARIANT-PGM"
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
                artifacts={"dcp_covariant_pgm_audit": str(path)},
            )
        )
    return payload

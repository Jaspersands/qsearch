"""Formalize Regev's average-case subset-sum to f=1 DCP bridge."""

from __future__ import annotations

import itertools
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


DCP_SUBSET_SUM_BRIDGE_PATH = Path("research/reductions/dcp_subset_sum_bridge.json")
DEFAULT_EXPERIMENT_ID = "EXP-DHS-DCP-AVERAGE-SUBSET-SUM-BRIDGE"
DEFAULT_CANDIDATE_ID = "DHS-GOWERS-SIEVE"


@dataclass(frozen=True)
class PartialSubsetSumBaseline:
    n_bits: int
    register_count: int
    solver_id: str
    candidate_subset_count: int
    answered_target_count: int
    legal_target_count: int
    legal_instance_coverage: float
    time_class: str
    polynomial_time_in_n: bool
    inverse_polynomial_coverage_observed: bool
    source_contract_satisfied: bool


@dataclass(frozen=True)
class EnumerationCoverageCertificate:
    n_bits: int
    polynomial_candidate_power: int
    required_coverage_power: int
    log2_candidate_budget: float
    log2_random_target_coverage_upper_bound: float
    log2_required_inverse_polynomial_coverage: float
    explicit_polynomial_enumeration_ruled_out: bool
    statement: str


@dataclass(frozen=True)
class SubsetSumSolverRoute:
    route_id: str
    access_and_output: str
    bridge_status: str
    resource_status: str
    remaining_obligation: str


@dataclass(frozen=True)
class DCPSubsetSumBridgeReport:
    created_at: str
    primary_source_contract: dict[str, str]
    reduction_edges: list[dict[str, str]]
    finite_baselines: list[PartialSubsetSumBaseline]
    enumeration_certificates: list[EnumerationCoverageCertificate]
    solver_routes: list[SubsetSumSolverRoute]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, bool | str]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _reachable_low_weight(labels: Sequence[int], modulus: int, maximum_weight: int) -> set[int]:
    reachable = {0}
    for weight in range(1, maximum_weight + 1):
        for indices in itertools.combinations(range(len(labels)), weight):
            reachable.add(sum(labels[index] for index in indices) % modulus)
    return reachable


def _reachable_contiguous(labels: Sequence[int], modulus: int) -> set[int]:
    reachable = {0}
    for start in range(len(labels)):
        total = 0
        for end in range(start, len(labels)):
            total = (total + labels[end]) % modulus
            reachable.add(total)
    return reachable


def _reachable_sampled(labels: Sequence[int], modulus: int, budget: int, seed: int) -> set[int]:
    rng = random.Random(seed)
    reachable = set()
    for _ in range(budget):
        total = sum(label for label in labels if rng.randrange(2)) % modulus
        reachable.add(total)
    return reachable


def _baseline_record(
    n_bits: int,
    register_count: int,
    solver_id: str,
    reachable: set[int],
    legal_targets: set[int],
    time_class: str,
    polynomial: bool,
    required_coverage_power: int,
) -> PartialSubsetSumBaseline:
    answered = len(reachable & legal_targets)
    coverage = answered / len(legal_targets)
    inverse_polynomial = coverage >= 1.0 / n_bits**required_coverage_power
    return PartialSubsetSumBaseline(
        n_bits=n_bits,
        register_count=register_count,
        solver_id=solver_id,
        candidate_subset_count=len(reachable),
        answered_target_count=answered,
        legal_target_count=len(legal_targets),
        legal_instance_coverage=coverage,
        time_class=time_class,
        polynomial_time_in_n=polynomial,
        inverse_polynomial_coverage_observed=inverse_polynomial,
        # Finite coverage is diagnostic only; no tested baseline has a uniform
        # inverse-polynomial coverage theorem across growing n.
        source_contract_satisfied=False,
    )


def analyze_partial_subset_sum_baselines(
    n_bits: int,
    labels: Sequence[int],
    required_coverage_power: int = 2,
    random_candidate_power: int = 4,
    seed: int = 0,
) -> list[PartialSubsetSumBaseline]:
    modulus = 1 << n_bits
    counts = subset_sum_counts(n_bits, labels)
    legal_targets = set(np.flatnonzero(counts).tolist())
    rows = []
    for weight in (1, 2, 3):
        rows.append(
            _baseline_record(
                n_bits,
                len(labels),
                f"bounded-hamming-weight-{weight}",
                _reachable_low_weight(labels, modulus, weight),
                legal_targets,
                f"O(n^{weight}) explicit candidate subsets",
                True,
                required_coverage_power,
            )
        )
    rows.append(
        _baseline_record(
            n_bits,
            len(labels),
            "contiguous-index-subsets",
            _reachable_contiguous(labels, modulus),
            legal_targets,
            "O(n^2) explicit candidate subsets",
            True,
            required_coverage_power,
        )
    )
    sample_budget = n_bits**random_candidate_power
    rows.append(
        _baseline_record(
            n_bits,
            len(labels),
            "polynomial-random-subset-sampling",
            _reachable_sampled(labels, modulus, sample_budget, seed),
            legal_targets,
            f"O(n^{random_candidate_power}) sampled candidate subsets",
            True,
            required_coverage_power,
        )
    )
    rows.append(
        PartialSubsetSumBaseline(
            n_bits=n_bits,
            register_count=len(labels),
            solver_id="meet-in-the-middle-exact-control",
            candidate_subset_count=1 << len(labels),
            answered_target_count=len(legal_targets),
            legal_target_count=len(legal_targets),
            legal_instance_coverage=1.0,
            time_class="2^(Theta(n/2)) time and exponential table",
            polynomial_time_in_n=False,
            inverse_polynomial_coverage_observed=True,
            source_contract_satisfied=False,
        )
    )
    return rows


def certify_polynomial_enumeration_coverage(
    n_bits: int,
    polynomial_candidate_power: int = 6,
    required_coverage_power: int = 2,
) -> EnumerationCoverageCertificate:
    if n_bits < 4 or polynomial_candidate_power < 1 or required_coverage_power < 1:
        raise ValueError("invalid certificate parameters")
    log_budget = polynomial_candidate_power * math.log2(n_bits)
    log_coverage = min(0.0, log_budget - n_bits)
    log_required = -required_coverage_power * math.log2(n_bits)
    ruled_out = log_coverage < log_required
    return EnumerationCoverageCertificate(
        n_bits=n_bits,
        polynomial_candidate_power=polynomial_candidate_power,
        required_coverage_power=required_coverage_power,
        log2_candidate_budget=log_budget,
        log2_random_target_coverage_upper_bound=log_coverage,
        log2_required_inverse_polynomial_coverage=log_required,
        explicit_polynomial_enumeration_ruled_out=ruled_out,
        statement=(
            f"Enumerating at most n^{polynomial_candidate_power} explicit subsets covers at most n^{polynomial_candidate_power}/2^n "
            f"of uniform targets before collisions, below n^-{required_coverage_power}={2.0**log_required:.6g} at this n={n_bits}."
        ),
    )


def _solver_routes() -> list[SubsetSumSolverRoute]:
    return [
        SubsetSumSolverRoute(
            route_id="deterministic-classical-partial-average-case-solver",
            access_and_output="random A in Z_N^(n+O(1)), target t; output one valid subset or error",
            bridge_status="primary-source sufficient for polynomial f=1 DCP when inverse-polynomial legal coverage holds",
            resource_status="open",
            remaining_obligation="Construct a uniform poly(n)-time solver with inverse-polynomial legal-input coverage.",
        ),
        SubsetSumSolverRoute(
            route_id="reversible-deterministic-solver-in-regev-matching-routine",
            access_and_output="coherently evaluate the deterministic partial function S(A,t) and uncompute workspace",
            bridge_status="primary-source quantum routine specified",
            resource_status="conditional on the classical solver",
            remaining_obligation="Charge reversible implementation, matching search, repetitions, and complete d recovery.",
        ),
        SubsetSumSolverRoute(
            route_id="target-independent-shared-seed-randomized-partial-solver",
            access_and_output=(
                "R(A,t;r) is a valid-witness-or-error deterministic function for each explicit target-independent seed; "
                "the same coherent seed register is shared across paired endpoints"
            ),
            bridge_status="conditional interface extension proved by the coherent matching audit",
            resource_status="solver construction open",
            remaining_obligation=(
                "Construct a uniform poly(n)-time solver with inverse-polynomial average legal coverage and reversible "
                "fixed-seed evaluation."
            ),
        ),
        SubsetSumSolverRoute(
            route_id="arbitrary-quantum-relation-partial-solver",
            access_and_output=(
                "solver emits target-dependent witness amplitudes or garbage without an explicit shared-seed decomposition"
            ),
            bridge_status="not implied by the deterministic or shared-seed theorem",
            resource_status="open coherence and reduction debt",
            remaining_obligation=(
                "Prove canonical coherent witness selection or balanced paired amplitudes with inverse-polynomial "
                "workspace overlap and reversible erasure."
            ),
        ),
        SubsetSumSolverRoute(
            route_id="full-normalized-fiber-pgm",
            access_and_output="coherently map every normalized exact-sum fiber to its residue",
            bridge_status="sufficient but stronger than Regev's partial-solver route",
            resource_status="open",
            remaining_obligation="Do not require this stronger primitive if a partial deterministic solver suffices.",
        ),
        SubsetSumSolverRoute(
            route_id="explicit-polynomial-candidate-enumeration",
            access_and_output="test polynomially many low-weight, contiguous, or sampled subsets",
            bridge_status="restricted asymptotic coverage no-go",
            resource_status="polynomial but exponentially small random-target coverage",
            remaining_obligation="A survivor must compute witnesses structurally rather than list polynomially many candidates.",
        ),
    ]


def run_subset_sum_bridge_audit(
    n_values: Sequence[int] = (8, 10, 12, 14, 16, 18, 20),
    register_offset: int = 4,
    trials_per_size: int = 3,
    seed: int = 0,
) -> DCPSubsetSumBridgeReport:
    if trials_per_size < 1:
        raise ValueError("trials_per_size must be positive")
    baselines: list[PartialSubsetSumBaseline] = []
    for n_index, n_bits in enumerate(n_values):
        modulus = 1 << n_bits
        register_count = n_bits + register_offset
        for trial in range(trials_per_size):
            rng = random.Random(seed + 1_000_003 * n_index + trial)
            labels = [rng.randrange(modulus) for _ in range(register_count)]
            baselines.extend(
                analyze_partial_subset_sum_baselines(
                    n_bits,
                    labels,
                    seed=seed + 10_007 * n_index + trial,
                )
            )
    certificates = [certify_polynomial_enumeration_coverage(n_bits) for n_bits in (64, 128, 256, 512, 1024)]
    polynomial_rows = [row for row in baselines if row.polynomial_time_in_n]
    metrics: dict[str, int | float] = {
        "finite_baseline_count": len(baselines),
        "polynomial_baseline_count": len(polynomial_rows),
        "polynomial_inverse_coverage_row_count": sum(row.inverse_polynomial_coverage_observed for row in polynomial_rows),
        "source_contract_satisfying_row_count": sum(row.source_contract_satisfied for row in baselines),
        "exact_exponential_control_count": sum(row.solver_id == "meet-in-the-middle-exact-control" for row in baselines),
        "enumeration_certificate_count": len(certificates),
        "polynomial_enumeration_ruled_out_count": sum(item.explicit_polynomial_enumeration_ruled_out for item in certificates),
        "primary_source_conditional_dcp_reduction_count": 1,
        "proved_polynomial_partial_average_subset_sum_solver_count": 0,
        "proved_seeded_randomized_solver_bridge_count": 1,
        "proved_arbitrary_quantum_relation_solver_bridge_count": 0,
        "proved_randomized_or_quantum_solver_bridge_count": 0,
        "proved_polynomial_dcp_decoder_count": 0,
    }
    return DCPSubsetSumBridgeReport(
        created_at=utc_now(),
        primary_source_contract={
            "literature_id": "regev-lattice-dhsp-2003",
            "source_locator": "cs/0304005 quantum_average.tex lines 700-1065, subset-sum assumption through final DCP decoder",
            "instance_distribution": "uniform A=(a_1,...,a_r), target t in Z_N, with r=log2 N+O(1)",
            "legal_input": "there exists B subseteq [r] with sum_{i in B} a_i=t mod N",
            "solver_requirement": "deterministic polynomial-time S(A,t) answers an inverse-polynomial fraction of legal inputs and otherwise returns error",
            "conditional_consequence": "the reversible matching routines recover d in poly(log N) time under DCP failure parameter f=1",
            "important_scope": "a partial solver suffices; uniform all-fiber preparation and solving every target are not required",
        },
        reduction_edges=[
            {
                "source": "partial-average-case-modular-subset-sum-density-one",
                "target": "f1-dihedral-coset-problem",
                "direction": "solver-for-source-implies-solver-for-target",
                "status": "primary-source-conditional-theorem",
            },
            {
                "source": "f1-dihedral-coset-problem",
                "target": "theta-n-2.5-unique-svp",
                "direction": "solver-for-source-implies-solver-for-target",
                "status": "primary-source-theorem-contract",
            },
        ],
        finite_baselines=baselines,
        enumeration_certificates=certificates,
        solver_routes=_solver_routes(),
        headline_metrics=metrics,
        claim_gate={
            "primary_source_bridge_verified": True,
            "partial_solver_is_sufficient": True,
            "full_fiber_pgm_required": False,
            "polynomial_partial_subset_sum_solver_constructed": False,
            "seeded_randomized_solver_bridge_proved": True,
            "arbitrary_quantum_relation_solver_bridge_proved": False,
            "randomized_or_quantum_solver_bridge_proved": False,
            "polynomial_dcp_decoder_constructed": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The source gives a high-leverage conditional route, but every implemented polynomial explicit-candidate "
                "baseline has inadequate coverage and no structural partial solver has been constructed."
            ),
        },
        status="primary-source-subset-sum-bridge-verified-partial-solver-open",
        summary=(
            f"Audited {len(baselines)} partial subset-sum baseline rows. Source-contract satisfying polynomial rows="
            f"{metrics['source_contract_satisfying_row_count']}; asymptotic explicit-enumeration no-go certificates="
            f"{metrics['polynomial_enumeration_ruled_out_count']}/{len(certificates)}."
        ),
        falsifiers_triggered=[
            "A full normalized-fiber PGM is sufficient but not necessary; Regev's partial deterministic subset-sum solver already gives a conditional route.",
            "Solving every subset-sum target is unnecessary; inverse-polynomial coverage of legal random instances suffices.",
            "Enumerating polynomially many candidate subsets has exponentially small uniform-target coverage and cannot meet the source contract.",
            "Meet-in-the-middle supplies an exact control but remains exponential in n=log2 N.",
            "Explicit target-independent shared-seed randomness is interface-compatible, but this theorem supplies no solver.",
            "An arbitrary quantum witness relation can leave orthogonal which-path workspaces and is not interface-compatible without an overlap theorem.",
            "Randomized or quantum witness generators need a new coherent-consistency reduction before inheriting Regev's theorem.",
        ],
    )


def write_subset_sum_bridge_audit(
    path: Path = DCP_SUBSET_SUM_BRIDGE_PATH,
    n_values: Sequence[int] = (8, 10, 12, 14, 16, 18, 20),
    register_offset: int = 4,
    trials_per_size: int = 3,
    seed: int = 0,
    write_registry: bool = True,
    registry_experiment_id: str = DEFAULT_EXPERIMENT_ID,
    registry_candidate_id: str = DEFAULT_CANDIDATE_ID,
    registry_result_id: str | None = None,
) -> dict:
    report = run_subset_sum_bridge_audit(n_values, register_offset, trials_per_size, seed)
    payload = asdict(report)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    if write_registry:
        upsert_negative_result(
            NegativeResultRecord(
                id="NEG-DCP-POLYNOMIAL-EXPLICIT-SUBSET-CANDIDATE-COVERAGE",
                source=str(path),
                claim="Testing polynomially many explicit subsets can satisfy Regev's inverse-polynomial legal-input coverage assumption.",
                reason_invalid=(
                    "Against a uniform target, M explicit candidate sums cover at most M/N residues. Polynomial M is "
                    "exponentially below inverse-polynomial coverage for N=2^n."
                ),
                lesson=(
                    "Search structural average-case subset-sum algorithms, reversible algebraic decoders, or coherent "
                    "many-target methods. Do not mutate low-weight or random candidate enumeration."
                ),
                applies_to=[registry_candidate_id, registry_experiment_id],
                evidence={
                    "source_contract_satisfying_row_count": payload["headline_metrics"]["source_contract_satisfying_row_count"],
                    "polynomial_enumeration_ruled_out_count": payload["headline_metrics"]["polynomial_enumeration_ruled_out_count"],
                    "primary_source_conditional_dcp_reduction_count": 1,
                },
            )
        )
        result_id = registry_result_id or f"RESULT-{registry_experiment_id}-DCP-SUBSET-SUM-BRIDGE"
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
                artifacts={"dcp_subset_sum_bridge": str(path)},
            )
        )
    return payload

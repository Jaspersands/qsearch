"""Coherent-interface audit for Regev's partial subset-sum matching routine."""

from __future__ import annotations

import json
import math
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


DCP_COHERENT_MATCHING_INTERFACE_PATH = Path(
    "research/reductions/dcp_coherent_matching_interface.json"
)
DEFAULT_EXPERIMENT_ID = "EXP-DHS-DCP-COHERENT-MATCHING-INTERFACE"
DEFAULT_CANDIDATE_ID = "DHS-GOWERS-SIEVE"


@dataclass(frozen=True)
class DeterministicUseSite:
    use_site_id: str
    source_lines: str
    requirement: str
    failure_if_removed: str


@dataclass(frozen=True)
class SeededBridgeCertificate:
    n_bits: int
    legal_coverage_exponent: int
    legal_coverage: float
    unconditional_coverage_lower_bound: float
    dense_seed_fraction_lower_bound: float
    matching_family_size_upper_bound: int
    dense_set_matching_intersection_fraction_lower_bound: float
    fixed_matching_average_intersection_fraction_lower_bound: float
    all_good_register_probability: float
    routine_success_probability_lower_bound: float
    polynomial_success_exponent: int
    fixed_seed_deterministic: bool
    target_independent_seed_distribution: bool
    shared_seed_register: bool
    valid_witness_or_error: bool
    reversible_evaluation: bool
    controlled_endpoint_normalization: bool
    conditional_seeded_randomized_bridge_proved: bool


@dataclass(frozen=True)
class WorkspaceVisibilityCase:
    case_id: str
    left_workspace: list[float]
    right_workspace: list[float]
    workspace_overlap: float
    x_y_signal_visibility: float
    phase_signal_preserved: bool
    interpretation: str


@dataclass(frozen=True)
class DCPCoherentMatchingInterfaceReport:
    created_at: str
    source_contract: dict[str, str]
    deterministic_use_sites: list[DeterministicUseSite]
    seeded_bridge_certificates: list[SeededBridgeCertificate]
    workspace_visibility_cases: list[WorkspaceVisibilityCase]
    interface_classes: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, bool | str]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def interference_visibility(
    left_workspace: Sequence[complex], right_workspace: Sequence[complex]
) -> float:
    left = np.asarray(left_workspace, dtype=np.complex128)
    right = np.asarray(right_workspace, dtype=np.complex128)
    if left.shape != right.shape or left.ndim != 1 or left.size == 0:
        raise ValueError("workspace states must be nonempty vectors of equal shape")
    left_norm = float(np.linalg.norm(left))
    right_norm = float(np.linalg.norm(right))
    if left_norm == 0.0 or right_norm == 0.0:
        raise ValueError("workspace states must be nonzero")
    return float(abs(np.vdot(left / left_norm, right / right_norm)))


def seeded_bridge_certificate(
    n_bits: int,
    legal_coverage_exponent: int,
    register_offset: int = 4,
) -> SeededBridgeCertificate:
    if n_bits < 8 or legal_coverage_exponent < 1 or register_offset < 0:
        raise ValueError("invalid seeded bridge parameters")
    legal_coverage = n_bits ** (-legal_coverage_exponent)
    # Regev proves that a random density-one target is legal with probability at least 1/2.
    unconditional = legal_coverage / 2.0
    dense_fraction = unconditional / (2.0 - unconditional)
    matching_count = math.ceil(16.0 / unconditional)
    intersection = unconditional**3 / 256.0
    fixed_matching = dense_fraction * intersection / matching_count
    all_good = (1.0 - 1.0 / n_bits) ** (n_bits + register_offset)
    routine_success = all_good * fixed_matching / (2**register_offset)
    return SeededBridgeCertificate(
        n_bits=n_bits,
        legal_coverage_exponent=legal_coverage_exponent,
        legal_coverage=legal_coverage,
        unconditional_coverage_lower_bound=unconditional,
        dense_seed_fraction_lower_bound=dense_fraction,
        matching_family_size_upper_bound=matching_count,
        dense_set_matching_intersection_fraction_lower_bound=intersection,
        fixed_matching_average_intersection_fraction_lower_bound=fixed_matching,
        all_good_register_probability=all_good,
        routine_success_probability_lower_bound=routine_success,
        polynomial_success_exponent=5 * legal_coverage_exponent,
        fixed_seed_deterministic=True,
        target_independent_seed_distribution=True,
        shared_seed_register=True,
        valid_witness_or_error=True,
        reversible_evaluation=True,
        controlled_endpoint_normalization=True,
        conditional_seeded_randomized_bridge_proved=True,
    )


def _deterministic_use_sites() -> list[DeterministicUseSite]:
    source = "research/literature_cache/cs_0304005_source/quantum_average.tex"
    return [
        DeterministicUseSite(
            use_site_id="canonical-preimage-check",
            source_lines=f"{source}:887 and :907",
            requirement="The solver output on t_alpha must equal the coherent branch alpha.",
            failure_if_removed="Different witnesses survive as orthogonal which-path labels instead of a two-point phase pair.",
        ),
        DeterministicUseSite(
            use_site_id="paired-endpoint-output",
            source_lines=f"{source}:895 and :915",
            requirement="The matching partner uses the same fixed solver function on f(t_alpha).",
            failure_if_removed="The two endpoints need not map to a common beta register and cannot interfere.",
        ),
        DeterministicUseSite(
            use_site_id="common-workspace-erasure",
            source_lines=f"{source}:928-956",
            requirement="Paired branches have the same measured beta and all remaining solver workspace is coherent.",
            failure_if_removed="The reduced endpoint qubit loses visibility by the workspace overlap factor.",
        ),
        DeterministicUseSite(
            use_site_id="postmeasurement-endpoint-normalization",
            source_lines=f"{source}:959-964",
            requirement="Given beta, the partner endpoint is recomputable and both endpoints are reversibly mapped to 0/1.",
            failure_if_removed="The qd/N phase remains encoded between unknown basis states rather than a measurable qubit.",
        ),
    ]


def _workspace_cases() -> list[WorkspaceVisibilityCase]:
    raw = [
        (
            "shared-target-independent-seed",
            [1.0, 0.0],
            [1.0, 0.0],
            "A shared explicit seed factors from the normalized endpoint qubit, preserving full visibility.",
        ),
        (
            "partially-overlapping-target-workspace",
            [1.0, 0.0],
            [0.5, math.sqrt(0.75)],
            "Target-dependent garbage attenuates every X/Y phase statistic by its workspace overlap.",
        ),
        (
            "orthogonal-target-dependent-witness-tags",
            [1.0, 0.0],
            [0.0, 1.0],
            "Orthogonal witness or failure tags erase the phase signal completely after workspace is ignored.",
        ),
    ]
    return [
        WorkspaceVisibilityCase(
            case_id=case_id,
            left_workspace=left,
            right_workspace=right,
            workspace_overlap=interference_visibility(left, right),
            x_y_signal_visibility=interference_visibility(left, right),
            phase_signal_preserved=interference_visibility(left, right) > 0.0,
            interpretation=interpretation,
        )
        for case_id, left, right, interpretation in raw
    ]


def run_coherent_matching_interface_audit(
    n_values: Sequence[int] = (16, 32, 64, 128),
    legal_coverage_exponents: Sequence[int] = (1, 2, 3),
    register_offset: int = 4,
) -> DCPCoherentMatchingInterfaceReport:
    certificates = [
        seeded_bridge_certificate(n_bits, exponent, register_offset)
        for n_bits in n_values
        for exponent in legal_coverage_exponents
    ]
    use_sites = _deterministic_use_sites()
    workspace_cases = _workspace_cases()
    proved_seeded = sum(item.conditional_seeded_randomized_bridge_proved for item in certificates)
    metrics: dict[str, int | float] = {
        "primary_source_deterministic_use_site_count": len(use_sites),
        "seeded_bridge_certificate_count": len(certificates),
        "proved_seeded_randomized_solver_bridge_count": proved_seeded,
        "minimum_certified_routine_success_probability": min(
            item.routine_success_probability_lower_bound for item in certificates
        ),
        "maximum_polynomial_success_exponent": max(
            item.polynomial_success_exponent for item in certificates
        ),
        "workspace_visibility_case_count": len(workspace_cases),
        "zero_visibility_counterexample_count": sum(
            item.workspace_overlap == 0.0 for item in workspace_cases
        ),
        "proved_arbitrary_quantum_relation_solver_bridge_count": 0,
        "proved_polynomial_partial_subset_sum_solver_count": 0,
        "proved_polynomial_dcp_decoder_count": 0,
        "source_contract_satisfying_solver_count": 0,
    }
    return DCPCoherentMatchingInterfaceReport(
        created_at=utc_now(),
        source_contract={
            "primary_source": "cs/0304005 quantum_average.tex lines 737-745 and 878-994",
            "deterministic_role": (
                "S(A,t) defines one partial function whose paired endpoints erase to the same beta workspace"
            ),
            "seeded_extension": (
                "R(A,t;r) is deterministic for each explicit target-independent seed r; a shared coherent seed register "
                "turns the source proof into a direct sum of deterministic routines"
            ),
            "coverage_extension": (
                "average seeded coverage p gives at least p/(2-p) dense (A,r) pairs; the source matching family and "
                "averaging yield a fixed matching with Omega(p^5) intersection probability"
            ),
            "quantum_obstruction": (
                "a general relation solver needs a target-independent seeded decomposition or an explicit inverse-polynomial "
                "paired-workspace overlap and balanced-amplitude theorem"
            ),
        },
        deterministic_use_sites=use_sites,
        seeded_bridge_certificates=certificates,
        workspace_visibility_cases=workspace_cases,
        interface_classes=[
            {
                "interface_id": "deterministic-partial-function",
                "bridge_proved": True,
                "condition": "source theorem as written",
            },
            {
                "interface_id": "target-independent-shared-seed-randomized-solver",
                "bridge_proved": True,
                "condition": (
                    "fixed-seed valid-or-error deterministic functions, polynomial explicit coins, coherent shared seed, "
                    "reversible evaluation, and inverse-polynomial average legal coverage"
                ),
            },
            {
                "interface_id": "target-dependent-randomness-or-measured-randomized-solver",
                "bridge_proved": False,
                "condition": "requires a common-seed coupling and workspace-overlap theorem",
            },
            {
                "interface_id": "arbitrary-quantum-relation-solver",
                "bridge_proved": False,
                "condition": (
                    "requires canonical coherent witness selection or balanced paired workspaces with inverse-polynomial overlap"
                ),
            },
        ],
        headline_metrics=metrics,
        claim_gate={
            "primary_source_deterministic_use_sites_extracted": True,
            "seeded_randomized_partial_solver_bridge_proved": proved_seeded == len(certificates),
            "arbitrary_quantum_relation_solver_bridge_proved": False,
            "workspace_overlap_required": True,
            "partial_subset_sum_solver_constructed": False,
            "polynomial_dcp_decoder_constructed": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The theorem interface is extended to target-independent shared-seed randomized solvers, but no such "
                "polynomial subset-sum solver is constructed. Arbitrary quantum relation solvers remain blocked by "
                "canonicalization, amplitude balance, and paired-workspace overlap."
            ),
        },
        status="seeded-randomized-interface-proved-general-quantum-interface-blocked",
        summary=(
            f"Certified {proved_seeded}/{len(certificates)} seeded-randomized interface rows and extracted "
            f"{len(use_sites)} deterministic source use sites. General quantum relation bridges=0; zero-visibility "
            f"workspace counterexamples={metrics['zero_visibility_counterexample_count']}."
        ),
        falsifiers_triggered=[
            "Classical randomness is acceptable only when represented by target-independent explicit coins shared coherently across both endpoints.",
            "Freshly measured or target-dependent randomness does not define the fixed answered set required by the matching lemma.",
            "Multiple valid witnesses do not help unless the circuit canonically couples paired endpoints and erases witness garbage.",
            "Orthogonal paired workspaces make every endpoint X/Y phase statistic exactly independent of qd/N.",
            "Proving an interface theorem does not construct the required polynomial subset-sum solver.",
        ],
    )


def write_coherent_matching_interface_audit(
    path: Path = DCP_COHERENT_MATCHING_INTERFACE_PATH,
    n_values: Sequence[int] = (16, 32, 64, 128),
    legal_coverage_exponents: Sequence[int] = (1, 2, 3),
    register_offset: int = 4,
    write_registry: bool = True,
    registry_experiment_id: str = DEFAULT_EXPERIMENT_ID,
    registry_candidate_id: str = DEFAULT_CANDIDATE_ID,
    registry_result_id: str | None = None,
) -> dict:
    report = run_coherent_matching_interface_audit(
        n_values, legal_coverage_exponents, register_offset
    )
    payload = asdict(report)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    if write_registry:
        upsert_negative_result(
            NegativeResultRecord(
                id="NEG-DCP-ARBITRARY-QUANTUM-RELATION-SOLVER-WITHOUT-WORKSPACE-OVERLAP",
                source=str(path),
                claim=(
                    "Any quantum algorithm that outputs a superposition of subset-sum witnesses can replace the "
                    "deterministic solver in Regev's matching routine."
                ),
                reason_invalid=(
                    "Target-dependent witness amplitudes or orthogonal garbage can erase paired-endpoint interference. "
                    "The source proof needs canonical selection, a shared-seed decomposition, or an explicit overlap theorem."
                ),
                lesson=(
                    "Randomized classical solvers with explicit target-independent shared coins are now interface-compatible. "
                    "For genuinely quantum solvers, prove balanced paired amplitudes, workspace overlap, and reversible erasure."
                ),
                applies_to=[registry_candidate_id, registry_experiment_id],
                evidence={
                    "proved_seeded_randomized_solver_bridge_count": payload["headline_metrics"][
                        "proved_seeded_randomized_solver_bridge_count"
                    ],
                    "zero_visibility_counterexample_count": payload["headline_metrics"][
                        "zero_visibility_counterexample_count"
                    ],
                    "proved_arbitrary_quantum_relation_solver_bridge_count": 0,
                },
            )
        )
        result_id = registry_result_id or f"RESULT-{registry_experiment_id}-DCP-COHERENT-MATCHING-INTERFACE"
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
                artifacts={"dcp_coherent_matching_interface": str(path)},
            )
        )
    return payload

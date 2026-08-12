"""Conditional inversion reduction for coherent DCP fiber erasure.

An erasure-plus-QFT implementation of the DCP PGM would like a circuit E_a
such that

    E_a |u_s>|0> = |s>|g_s>.

Tracing out the garbage multiplies the off-diagonal ``|s><t|`` coherence by
``<g_t|g_s>``.  Exact preservation of all cyclic phase states therefore
requires all garbage states to agree up to an aligned phase.  If the common
garbage is the circuit's known reset state, the inverse circuit prepares
``|u_s>`` from ``|s>``.

This turns a coherent erasure shortcut into an average subset-sum solver.  For
the planted/source-weighted target law ``pi_s=c_s/D`` and the uniform-legal law
``q_s=1/L``,

    q_s / pi_s = D/(L c_s) <= D/L.

The quenched Poisson occupancy theorem gives ``L/D -> 1-e^-1`` in probability,
so source-weighted average preparation error transfers to uniform-legal error
with only a constant factor.  Measuring the prepared fiber state returns a
Boolean witness, which is then verified.

This is a conditional reduction, not a lower bound for arbitrary PGM
measurements.  A full-rank POVM not factored through coherent fiber erasure and
a cyclic QFT remains open.
"""

from __future__ import annotations

import json
import math
import random
from dataclasses import asdict, dataclass
from pathlib import Path

import numpy as np

from dcp_subset_sum_qtt_contraction_search import (
    exact_cyclic_subset_sum_counts,
)
from research_registry import (
    ExperimentResultRecord,
    NegativeResultRecord,
    upsert_experiment_result,
    upsert_negative_result,
    utc_now,
)


REPORT_PATH = Path(
    "research/reductions/dcp_global_erasure_inversion_reduction.json"
)
QUENCHED_OCCUPANCY_PATH = Path(
    "research/classical_baselines/"
    "dcp_subset_sum_quenched_occupancy_theorem.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-DHS-DCP-GLOBAL-ERASURE-INVERSION-REDUCTION"
)
DEFAULT_CANDIDATE_ID = "DHS-GOWERS-SIEVE"


@dataclass(frozen=True)
class CoherenceErasureCertificate:
    statement: str
    coherence_multiplier: str
    exact_coherence_condition: str
    common_garbage_conclusion: str
    inverse_preparation_conclusion: str
    proved: bool
    limitations: list[str]


@dataclass(frozen=True)
class TargetLawTransferControl:
    n_bits: int
    trial: int
    support_size: int
    support_fraction: float
    domination_constant: float
    maximum_exact_law_ratio: float
    domination_residual: float
    singleton_fiber_count: int
    doubleton_fiber_count: int
    status: str


@dataclass(frozen=True)
class ErasureInversionReduction:
    source_interface: str
    required_erasure_guarantee: str
    inverse_algorithm: str
    target_law_transfer: str
    witness_verification: str
    consequence: str
    proved: bool
    excluded_measurement_classes: list[str]


@dataclass(frozen=True)
class GlobalErasureInversionReport:
    created_at: str
    theorem_contract: dict[str, str]
    coherence_certificate: CoherenceErasureCertificate
    law_transfer_controls: list[TargetLawTransferControl]
    reduction: ErasureInversionReduction
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, bool | str]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def coherence_erasure_certificate() -> CoherenceErasureCertificate:
    return CoherenceErasureCertificate(
        statement=(
            "If E|u_s,0>=|s,g_s>, then tracing garbage maps "
            "|s><t| to <g_t|g_s>|s><t|."
        ),
        coherence_multiplier="<g_t|g_s>",
        exact_coherence_condition=(
            "<g_t|g_s>=1 for every legal s,t required by the cyclic "
            "phase-state support"
        ),
        common_garbage_conclusion=(
            "unit vectors with pairwise inner product one are identical; "
            "g_s=g is target independent"
        ),
        inverse_preparation_conclusion=(
            "if g is a known efficiently preparable reset state, "
            "E^dagger|s,g>=|u_s,0>"
        ),
        proved=True,
        limitations=[
            "Approximate average coherence needs an explicit quantitative garbage-Gram bound.",
            "A target-dependent garbage state may still support a different measurement that does not use a cyclic QFT.",
            "An arbitrary full-rank POVM need not expose an erasure factorization.",
            "The common garbage must be efficiently preparable to run the inverse.",
        ],
    )


def audit_target_law_transfer(
    n_bits: int,
    trial: int,
    seed: int,
) -> TargetLawTransferControl:
    if n_bits < 2:
        raise ValueError("n_bits must be at least two")
    modulus = 1 << n_bits
    rng = random.Random(seed)
    labels = [rng.randrange(modulus) for _ in range(n_bits)]
    counts = exact_cyclic_subset_sum_counts(labels, modulus)
    legal = counts > 0
    support_size = int(np.count_nonzero(legal))
    support_fraction = support_size / modulus
    q = np.zeros(modulus, dtype=np.float64)
    q[legal] = 1 / support_size
    pi = counts.astype(np.float64) / modulus
    ratios = q[legal] / pi[legal]
    domination = modulus / support_size
    residual = float(max(0.0, np.max(ratios) - domination))
    return TargetLawTransferControl(
        n_bits=n_bits,
        trial=trial,
        support_size=support_size,
        support_fraction=support_fraction,
        domination_constant=domination,
        maximum_exact_law_ratio=float(np.max(ratios)),
        domination_residual=residual,
        singleton_fiber_count=int(np.count_nonzero(counts == 1)),
        doubleton_fiber_count=int(np.count_nonzero(counts == 2)),
        status=(
            "uniform-legal-dominated-by-source-weighted-law"
            if residual <= 1e-12
            else "target-law-domination-failed"
        ),
    )


def build_global_erasure_inversion_report(
    n_values: tuple[int, ...] = (8, 10, 12, 14, 16, 18),
    trials_per_size: int = 4,
    seed: int = 0,
    occupancy_theorem_path: Path = QUENCHED_OCCUPANCY_PATH,
) -> GlobalErasureInversionReport:
    try:
        occupancy = (
            json.loads(occupancy_theorem_path.read_text())
            if occupancy_theorem_path.exists()
            else {}
        )
    except (json.JSONDecodeError, OSError):
        occupancy = {}
    support_law_proved = bool(
        occupancy.get("claim_gate", {}).get(
            "quenched_poisson_limit_proved", False
        )
    )
    controls = [
        audit_target_law_transfer(
            n_bits,
            trial,
            seed + 1009 * n_bits + trial,
        )
        for n_bits in n_values
        for trial in range(trials_per_size)
    ]
    certificate = coherence_erasure_certificate()
    control_failures = sum(
        row.status
        != "uniform-legal-dominated-by-source-weighted-law"
        for row in controls
    )
    asymptotic_domination = 1 / (1 - math.exp(-1))
    reduction_proved = (
        certificate.proved
        and support_law_proved
        and control_failures == 0
    )
    reduction = ErasureInversionReduction(
        source_interface=(
            "random public labels, source-weighted phase-state support "
            "pi_s=c_s/2^n, and a coherent erasure circuit with common "
            "efficiently preparable garbage"
        ),
        required_erasure_guarantee=(
            "inverse-polynomial implementation error averaged under pi and "
            "coherence sufficient for the final cyclic QFT"
        ),
        inverse_algorithm=(
            "sample a uniform legal target under the Regev source contract, "
            "prepare |s,g>, apply E_a^dagger, and measure x"
        ),
        target_law_transfer=(
            "q_s<=D/L*pi_s pointwise; quenched L/D->1-e^-1 makes "
            "the loss at most 1/(1-e^-1)+o(1)"
        ),
        witness_verification=(
            "accept only Boolean x satisfying sum_i a_i x_i=s mod 2^n"
        ),
        consequence=(
            "a polynomial coherent erasure-plus-QFT primitive yields a "
            "polynomial average-case density-one subset-sum witness solver"
        ),
        proved=reduction_proved,
        excluded_measurement_classes=[
            "arbitrary full-rank POVM with no erasure-plus-QFT factorization",
            "target-dependent garbage with insufficient retained coherence",
            "noninvertible channel whose environment is unavailable",
            "erasure with an unknown or inefficiently preparable common garbage state",
        ],
    )
    metrics: dict[str, int | float] = {
        "coherence_erasure_theorem_count": int(certificate.proved),
        "target_law_transfer_control_count": len(controls),
        "target_law_transfer_failure_count": control_failures,
        "maximum_finite_domination_constant": max(
            row.domination_constant for row in controls
        ),
        "tail_mean_domination_constant": float(
            np.mean(
                [
                    row.domination_constant
                    for row in controls
                    if row.n_bits == max(n_values)
                ]
            )
        ),
        "poisson_asymptotic_domination_constant": (
            asymptotic_domination
        ),
        "quenched_support_law_theorem_count": int(
            support_law_proved
        ),
        "proved_coherent_erasure_to_witness_reduction_count": int(
            reduction_proved
        ),
        "proved_arbitrary_pgm_to_witness_reduction_count": 0,
        "polynomial_coherent_erasure_circuit_count": 0,
        "polynomial_average_subset_sum_witness_solver_count": 0,
        "polynomial_arbitrary_full_rank_pgm_count": 0,
    }
    return GlobalErasureInversionReport(
        created_at=utc_now(),
        theorem_contract={
            "coherence": (
                "target-dependent garbage dephases the s register by its "
                "garbage Gram matrix before the cyclic QFT"
            ),
            "invertibility": (
                "exact common known garbage makes coherent erasure reversible "
                "into normalized-fiber preparation"
            ),
            "law_change": (
                "uniform-legal q is pointwise dominated by D/L times planted "
                "pi; quenched Poisson gives D/L->1/(1-e^-1)"
            ),
            "consequence": (
                "measure inverse-prepared |u_s> and verify to solve average "
                "density-one modular subset sum"
            ),
            "scope": (
                "conditional erasure-plus-QFT reduction only; arbitrary "
                "collective POVMs remain open"
            ),
        },
        coherence_certificate=certificate,
        law_transfer_controls=controls,
        reduction=reduction,
        headline_metrics=metrics,
        claim_gate={
            "coherent_erasure_requires_target_independent_garbage": True,
            "source_weighted_to_uniform_legal_transfer_proved": (
                support_law_proved and control_failures == 0
            ),
            "coherent_erasure_implies_average_witness_solver": (
                reduction_proved
            ),
            "arbitrary_full_rank_pgm_reduced_to_witness_solver": False,
            "polynomial_coherent_erasure_constructed": False,
            "polynomial_average_witness_solver_constructed": False,
            "speedup_claim_allowed": False,
            "reason": (
                "Any erasure-plus-QFT route that preserves the required "
                "coherence and has common preparable garbage is invertible. "
                "The quenched support law then turns it into an average "
                "subset-sum witness solver. This is a conditional equivalence, "
                "not a lower bound against arbitrary full-rank measurements."
            ),
        },
        status=(
            "coherent-erasure-reduced-to-average-witness-"
            "arbitrary-full-rank-pgm-open"
            if reduction_proved
            else "coherent-erasure-reduction-blocked-support-law-missing"
        ),
        summary=(
            f"Verified target-law domination on {len(controls)} controls with "
            f"{control_failures} failures. The quenched support theorem is "
            f"{'available' if support_law_proved else 'missing'}, so the "
            "coherent erasure-plus-QFT route is conditionally equivalent to "
            "an average subset-sum witness solver; arbitrary full-rank POVMs "
            "remain open."
        ),
        falsifiers_triggered=[
            "Target-dependent erasure garbage destroys exactly the off-diagonal target coherence needed by a following cyclic QFT.",
            "Common efficiently preparable garbage makes the erasure circuit invertible into normalized-fiber preparation.",
            "Source-weighted average fidelity cannot hide on large fibers: uniform-legal mass is pointwise dominated by D/L times source-weighted mass.",
            "The reduction produces and verifies a witness directly; fixed-variable self-reduction is unnecessary under the common-garbage interface.",
            "An arbitrary PGM implementation need not factor through coherent erasure and is not ruled out.",
        ],
    )


def write_global_erasure_inversion_report(
    output_path: Path = REPORT_PATH,
    *,
    write_registry: bool = True,
    registry_experiment_id: str = DEFAULT_EXPERIMENT_ID,
    registry_candidate_id: str = DEFAULT_CANDIDATE_ID,
    registry_result_id: str | None = None,
    n_values: tuple[int, ...] = (8, 10, 12, 14, 16, 18),
    trials_per_size: int = 4,
    seed: int = 0,
    occupancy_theorem_path: Path = QUENCHED_OCCUPANCY_PATH,
) -> dict[str, object]:
    payload = asdict(
        build_global_erasure_inversion_report(
            n_values=n_values,
            trials_per_size=trials_per_size,
            seed=seed,
            occupancy_theorem_path=occupancy_theorem_path,
        )
    )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(payload, indent=2, sort_keys=True)
    )
    return payload


if __name__ == "__main__":
    report = write_global_erasure_inversion_report()
    print(
        json.dumps(
            report["headline_metrics"], indent=2, sort_keys=True
        )
    )

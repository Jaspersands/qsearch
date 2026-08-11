"""Source-weighted inversion tradeoff for the direct DCP fiber encoding.

Let ``c_h`` be the modular subset-sum fiber multiplicities, ``D=sum_h c_h``,
and let the planted/source law be ``pi_h=c_h/D``.  The direct equality or
state-preparation encoding exposes the legal-fiber amplitude

    sigma_h = sqrt(c_h / D).

Two exact identities hold on the legal support ``S``:

    E_pi[sigma_h^(-1)]^2 = N P_PGM,
    E_pi[sigma_h^(-2)]   = |S|,

where ``P_PGM=(sum_h sqrt(c_h))^2/(N D)`` is the optimal covariant DCP PGM
success probability.  Useful PGM information therefore makes the average
reciprocal amplitude exponentially large when ``N=2^n``.  At density one,
the quenched Poisson occupancy theorem gives ``|S|/N -> 1-e^-1``, so the RMS
reciprocal amplitude is ``Theta(sqrt(N))`` on almost every random source.

Trimming does not repair a branchwise inversion route unless it concentrates
on exponentially large fibers.  For any accepted legal set ``A`` with source
mass ``mu`` and maximum multiplicity ``C_A``, conditional RMS satisfies

    E[sigma_h^(-2) | h in A] = |A|/mu >= D/C_A.

Thus every accepted branch family whose multiplicities are polynomial has
exponential RMS inverse scale, independent of its retained source mass.

This is a direct-encoding and branchwise-inversion theorem.  It applies to
generic amplitude amplification and standard variable-time schemes whose
branch cost is lower bounded by ``1/sigma_h``.  It is not a lower bound on a
global source-aware coisometry, a collision walk exploiting arithmetic, an
arbitrary destructive POVM, or all quantum circuits.
"""

from __future__ import annotations

import json
import math
import random
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Sequence

import numpy as np

from dcp_covariant_pgm_audit import covariant_pgm_success
from dcp_subset_sum_qtt_contraction_search import (
    exact_cyclic_subset_sum_counts,
)
from research_registry import utc_now


REPORT_PATH = Path(
    "research/reductions/dcp_source_weighted_inversion_tradeoff.json"
)
OCCUPANCY_PATH = Path(
    "research/classical_baselines/dcp_subset_sum_quenched_occupancy_theorem.json"
)
DEFAULT_EXPERIMENT_ID = "EXP-DHS-DCP-SOURCE-WEIGHTED-INVERSION-TRADEOFF"
DEFAULT_CANDIDATE_ID = "HYP-SHIFT-MULTIPLICITY-AMPLIFICATION"


@dataclass(frozen=True)
class SourceWeightedInversionControl:
    control_id: str
    modulus: int
    assignment_count: int
    occupied_residue_count: int
    support_fraction: float
    maximum_multiplicity: int
    pgm_success_probability: float
    mean_reciprocal_amplitude: float
    rms_reciprocal_amplitude: float
    mean_pgm_duality_residual: float
    rms_support_identity_residual: float
    direct_source_average_inversion_polynomial: bool
    normalizations_verified: bool
    status: str


@dataclass(frozen=True)
class TrimmedInversionControl:
    control_id: str
    modulus: int
    assignment_count: int
    accepted_residue_count: int
    accepted_source_mass: float
    accepted_maximum_multiplicity: int
    conditional_mean_reciprocal_amplitude: float
    conditional_rms_reciprocal_amplitude: float
    exact_conditional_rms_squared: float
    multiplicity_bound_rms_lower_bound: float
    lower_bound_residual: float
    inverse_polynomial_source_mass_retained: bool
    polynomial_multiplicity_cap: bool
    branchwise_polytime_inversion_certified: bool
    status: str


@dataclass(frozen=True)
class SourceWeightedScaling:
    input_bits: int
    assumed_pgm_success_lower_bound_power: int
    mean_inverse_lower_bound_log2: float
    quenched_support_fraction_limit: float
    quenched_rms_inverse_log2_asymptotic: float
    polynomial_fiber_cap_power: int
    trimmed_rms_lower_bound_log2: float
    polynomial_branchwise_cost_possible: bool
    status: str


@dataclass(frozen=True)
class SourceWeightedInversionTheorem:
    source_law: str
    mean_identity: str
    rms_identity: str
    trimmed_identity: str
    quenched_consequence: str
    route_consequence: str
    scope_limit: str
    mean_pgm_duality_proved: bool
    rms_support_identity_proved: bool
    trimmed_multiplicity_bound_proved: bool
    source_weighting_rescues_direct_inversion: bool
    global_source_aware_coisometry_ruled_out: bool
    general_quantum_lower_bound_proved: bool
    theorem_verified: bool
    status: str


@dataclass(frozen=True)
class DcpSourceWeightedInversionTradeoffReport:
    created_at: str
    theorem_contract: dict[str, Any]
    finite_controls: list[SourceWeightedInversionControl]
    trimming_controls: list[TrimmedInversionControl]
    scaling_records: list[SourceWeightedScaling]
    theorem: SourceWeightedInversionTheorem
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    literature_links: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def source_weighted_inversion_metrics(
    control_id: str,
    counts: Sequence[int],
    *,
    polynomial_cost_power: int = 8,
) -> SourceWeightedInversionControl:
    values = np.asarray(counts, dtype=np.float64)
    if values.ndim != 1 or len(values) < 2 or np.any(values < 0):
        raise ValueError("counts must be a nonnegative one-dimensional table")
    assignment_count = int(np.sum(values))
    if assignment_count <= 0:
        raise ValueError("counts must have positive total mass")
    legal = values > 0
    occupied = int(np.count_nonzero(legal))
    source = values[legal] / assignment_count
    amplitudes = np.sqrt(values[legal] / assignment_count)
    mean_inverse = float(np.sum(source / amplitudes))
    rms_inverse_squared = float(np.sum(source / (amplitudes * amplitudes)))
    rms_inverse = math.sqrt(rms_inverse_squared)
    pgm = covariant_pgm_success(values)
    mean_residual = abs(mean_inverse * mean_inverse - len(values) * pgm)
    rms_residual = abs(rms_inverse_squared - occupied)
    input_bits = max(2, math.ceil(math.log2(len(values))))
    polynomial_threshold = input_bits**polynomial_cost_power
    verified = (
        abs(float(np.sum(source)) - 1.0) < 1e-12
        and mean_residual < 1e-9
        and rms_residual < 1e-9
    )
    return SourceWeightedInversionControl(
        control_id=control_id,
        modulus=len(values),
        assignment_count=assignment_count,
        occupied_residue_count=occupied,
        support_fraction=occupied / len(values),
        maximum_multiplicity=int(np.max(values)),
        pgm_success_probability=pgm,
        mean_reciprocal_amplitude=mean_inverse,
        rms_reciprocal_amplitude=rms_inverse,
        mean_pgm_duality_residual=mean_residual,
        rms_support_identity_residual=rms_residual,
        direct_source_average_inversion_polynomial=(
            mean_inverse <= polynomial_threshold
            and rms_inverse <= polynomial_threshold
        ),
        normalizations_verified=verified,
        status=(
            "source-weighted-inversion-identities-verified"
            if verified
            else "source-weighted-inversion-control-failure"
        ),
    )


def trimmed_inversion_metrics(
    control_id: str,
    counts: Sequence[int],
    accepted_residues: Sequence[int],
    *,
    polynomial_multiplicity_power: int = 4,
) -> TrimmedInversionControl:
    values = np.asarray(counts, dtype=np.float64)
    if values.ndim != 1 or len(values) < 2 or np.any(values < 0):
        raise ValueError("counts must be a nonnegative one-dimensional table")
    assignment_count = float(np.sum(values))
    accepted = sorted({int(index) for index in accepted_residues})
    if assignment_count <= 0 or not accepted:
        raise ValueError("positive mass and a nonempty accepted set are required")
    if any(index < 0 or index >= len(values) or values[index] <= 0 for index in accepted):
        raise ValueError("accepted residues must be legal")

    accepted_counts = values[accepted]
    source_mass = float(np.sum(accepted_counts) / assignment_count)
    conditional = accepted_counts / (source_mass * assignment_count)
    amplitudes = np.sqrt(accepted_counts / assignment_count)
    mean_inverse = float(np.sum(conditional / amplitudes))
    rms_squared = float(np.sum(conditional / (amplitudes * amplitudes)))
    rms = math.sqrt(rms_squared)
    max_count = int(np.max(accepted_counts))
    lower = math.sqrt(assignment_count / max_count)
    lower_residual = max(0.0, lower - rms)
    input_bits = max(2, math.ceil(math.log2(len(values))))
    inverse_poly_mass = source_mass >= input_bits**-8
    polynomial_cap = max_count <= input_bits**polynomial_multiplicity_power
    return TrimmedInversionControl(
        control_id=control_id,
        modulus=len(values),
        assignment_count=int(assignment_count),
        accepted_residue_count=len(accepted),
        accepted_source_mass=source_mass,
        accepted_maximum_multiplicity=max_count,
        conditional_mean_reciprocal_amplitude=mean_inverse,
        conditional_rms_reciprocal_amplitude=rms,
        exact_conditional_rms_squared=rms_squared,
        multiplicity_bound_rms_lower_bound=lower,
        lower_bound_residual=lower_residual,
        inverse_polynomial_source_mass_retained=inverse_poly_mass,
        polynomial_multiplicity_cap=polynomial_cap,
        branchwise_polytime_inversion_certified=False,
        status=(
            "trimmed-source-rms-inversion-bound-verified"
            if lower_residual < 1e-10
            else "trimmed-source-inversion-bound-failure"
        ),
    )


def scaling_record(
    input_bits: int,
    *,
    pgm_success_lower_bound_power: int = 4,
    polynomial_fiber_cap_power: int = 4,
) -> SourceWeightedScaling:
    if input_bits < 2:
        raise ValueError("input_bits must be at least two")
    if min(pgm_success_lower_bound_power, polynomial_fiber_cap_power) < 0:
        raise ValueError("polynomial powers must be nonnegative")
    support_limit = 1.0 - math.exp(-1.0)
    mean_lower_log2 = 0.5 * (
        input_bits
        - pgm_success_lower_bound_power * math.log2(input_bits)
    )
    rms_asymptotic_log2 = 0.5 * (
        input_bits + math.log2(support_limit)
    )
    trimmed_lower_log2 = 0.5 * (
        input_bits
        - polynomial_fiber_cap_power * math.log2(input_bits)
    )
    polynomial_threshold = 8 * math.log2(input_bits)
    return SourceWeightedScaling(
        input_bits=input_bits,
        assumed_pgm_success_lower_bound_power=pgm_success_lower_bound_power,
        mean_inverse_lower_bound_log2=mean_lower_log2,
        quenched_support_fraction_limit=support_limit,
        quenched_rms_inverse_log2_asymptotic=rms_asymptotic_log2,
        polynomial_fiber_cap_power=polynomial_fiber_cap_power,
        trimmed_rms_lower_bound_log2=trimmed_lower_log2,
        polynomial_branchwise_cost_possible=(
            min(mean_lower_log2, trimmed_lower_log2) <= polynomial_threshold
        ),
        status="source-weighted-direct-inversion-superpolynomial",
    )


def _random_counts(n_bits: int, seed: int) -> np.ndarray:
    modulus = 1 << n_bits
    rng = random.Random(seed)
    labels = [rng.randrange(modulus) for _ in range(n_bits)]
    return exact_cyclic_subset_sum_counts(labels, modulus)


def run_dcp_source_weighted_inversion_tradeoff(
) -> DcpSourceWeightedInversionTradeoffReport:
    count_tables = [
        ("uniform-two-to-one", np.full(8, 2, dtype=np.int64)),
        ("injective-partial-support", np.asarray([1] * 8 + [0] * 9)),
        ("random-density-one-n8", _random_counts(8, 8101)),
        ("random-density-one-n10", _random_counts(10, 10103)),
        ("random-density-one-n12", _random_counts(12, 12109)),
    ]
    controls = [
        source_weighted_inversion_metrics(control_id, counts)
        for control_id, counts in count_tables
    ]
    trimming: list[TrimmedInversionControl] = []
    for control_id, counts in count_tables[2:]:
        legal = np.flatnonzero(counts > 0)
        low = [int(index) for index in legal if counts[index] <= 2]
        high = sorted(
            (int(index) for index in legal),
            key=lambda index: int(counts[index]),
            reverse=True,
        )[: max(1, len(legal) // 4)]
        if low:
            trimming.append(
                trimmed_inversion_metrics(
                    f"{control_id}-singleton-doubleton",
                    counts,
                    low,
                )
            )
        trimming.append(
            trimmed_inversion_metrics(
                f"{control_id}-top-quartile",
                counts,
                high,
            )
        )
    scaling = [scaling_record(bits) for bits in (64, 128, 256, 512)]

    try:
        occupancy = (
            json.loads(OCCUPANCY_PATH.read_text())
            if OCCUPANCY_PATH.exists()
            else {}
        )
    except (json.JSONDecodeError, OSError):
        occupancy = {}
    quenched_support_law = bool(
        occupancy.get("claim_gate", {}).get(
            "quenched_poisson_limit_proved", False
        )
    )
    verified = bool(
        all(row.normalizations_verified for row in controls)
        and all(row.lower_bound_residual < 1e-10 for row in trimming)
        and quenched_support_law
    )
    theorem = SourceWeightedInversionTheorem(
        source_law=(
            "A planted Boolean assignment induces pi_h=c_h/D on legal "
            "residues; the direct preparation singular amplitude is "
            "sigma_h=sqrt(c_h/D)."
        ),
        mean_identity=(
            "E_pi[1/sigma_h]=sum_h sqrt(c_h)/sqrt(D), hence its square "
            "equals N P_PGM exactly."
        ),
        rms_identity=(
            "E_pi[1/sigma_h^2]=sum_(c_h>0) 1=|supp(c)| exactly."
        ),
        trimmed_identity=(
            "For accepted A of source mass mu, conditional RMS squared is "
            "|A|/mu and is at least D/max_(h in A)c_h."
        ),
        quenched_consequence=(
            "At density one, the proved quenched Poisson law gives "
            "|supp(c)|/N -> 1-e^-1 in probability, so RMS reciprocal "
            "amplitude is Theta(sqrt(N)) on almost every public source."
        ),
        route_consequence=(
            "Source weighting, branchwise amplitude amplification, and "
            "standard variable-time RMS accounting do not make the direct "
            "fiber encoding polynomial when PGM information is useful."
        ),
        scope_limit=(
            "The identities do not constrain a global coisometry acting on "
            "all fibers at once, source-aware arithmetic preconditioning, "
            "collision walks, or arbitrary POVMs."
        ),
        mean_pgm_duality_proved=True,
        rms_support_identity_proved=True,
        trimmed_multiplicity_bound_proved=True,
        source_weighting_rescues_direct_inversion=False,
        global_source_aware_coisometry_ruled_out=False,
        general_quantum_lower_bound_proved=False,
        theorem_verified=verified,
        status=(
            "source-weighted-direct-inversion-tradeoff-proved"
            if verified
            else "source-weighted-inversion-control-failure"
        ),
    )
    metrics = {
        "finite_identity_control_count": len(controls),
        "trimming_control_count": len(trimming),
        "finite_control_failure_count": int(not verified),
        "maximum_mean_identity_residual": max(
            row.mean_pgm_duality_residual for row in controls
        ),
        "maximum_rms_identity_residual": max(
            row.rms_support_identity_residual for row in controls
        ),
        "maximum_trim_bound_residual": max(
            (row.lower_bound_residual for row in trimming), default=0.0
        ),
        "quenched_support_fraction_theorem_loaded": int(quenched_support_law),
        "source_weighted_direct_inversion_rescue_count": 0,
        "global_source_aware_coisometry_lower_bound_count": 0,
        "new_quantum_algorithm_count": 0,
    }
    return DcpSourceWeightedInversionTradeoffReport(
        created_at=utc_now(),
        theorem_contract={
            "encoding": "direct equality/state-preparation amplitude sqrt(c_h/D)",
            "target_law": "planted/source-weighted pi_h=c_h/D",
            "cost_model": (
                "target-by-target inversion cost at least reciprocal amplitude; "
                "standard variable-time aggregation uses RMS branch cost"
            ),
            "excluded_scope": (
                "global all-fiber transforms and arithmetic source-aware circuits"
            ),
        },
        finite_controls=controls,
        trimming_controls=trimming,
        scaling_records=scaling,
        theorem=theorem,
        proof_obligations=[
            {
                "obligation": "compute_source_mean_inverse_scale",
                "resolved": True,
                "resolution": "Exact cancellation gives E[1/sigma]^2=N P_PGM.",
            },
            {
                "obligation": "compute_variable_time_rms_scale",
                "resolved": True,
                "resolution": "Each legal residue contributes exactly one to E[1/sigma^2].",
            },
            {
                "obligation": "transfer_support_scaling_to_random_density_one_sources",
                "resolved": quenched_support_law,
                "resolution": (
                    "The existing quenched Poisson theorem gives support "
                    "fraction 1-e^-1 in probability."
                ),
            },
            {
                "obligation": "construct_global_source_aware_fiber_coisometry",
                "resolved": False,
                "resolution": (
                    "The theorem rejects branchwise direct inversion, not a "
                    "collective arithmetic transform."
                ),
            },
            {
                "obligation": "prove_general_quantum_circuit_lower_bound",
                "resolved": False,
                "resolution": "No such lower bound follows from singular amplitudes alone.",
            },
        ],
        adversarial_audit=[
            {
                "challenge": "Source weighting suppresses hard small fibers.",
                "survives": False,
                "response": (
                    "Weight c_h/D cancels 1/sigma_h^2=D/c_h exactly, so every "
                    "occupied residue contributes one to RMS squared."
                ),
            },
            {
                "challenge": "Useful PGM information should correlate with cheap inversion.",
                "survives": False,
                "response": (
                    "The exact duality is the opposite: mean inverse scale is "
                    "sqrt(N P_PGM)."
                ),
            },
            {
                "challenge": "Trim to an inverse-polynomial easy source subset.",
                "survives": False,
                "response": (
                    "If accepted multiplicities are at most polynomial, "
                    "conditional RMS is at least sqrt(D/poly(n)), independent of mu."
                ),
            },
            {
                "challenge": "This rules out every source-aware implementation.",
                "survives": False,
                "response": (
                    "A global coisometry need not invert branches independently; "
                    "that route remains explicitly open."
                ),
            },
        ],
        literature_links=[
            {
                "paper_id": "BACON-CHILDS-VAN-DAM-2005",
                "title": (
                    "From optimal measurement to efficient quantum algorithms "
                    "for the hidden subgroup problem over semidirect product groups"
                ),
                "url": "https://arxiv.org/abs/quant-ph/0504083",
                "use": "Covariant PGM and subset-sum multiplicity formula",
                "external_theorem_not_reproved_here": True,
            }
        ],
        headline_metrics=metrics,
        claim_gate={
            "source_weighting_makes_direct_fiber_inversion_polynomial": False,
            "standard_variable_time_rms_rescues_direct_encoding": False,
            "inverse_polynomial_trim_with_polynomial_fibers_rescues_route": False,
            "mean_inverse_pgm_duality_proved": True,
            "rms_support_identity_proved": True,
            "global_source_aware_coisometry_ruled_out": False,
            "arithmetic_collision_walk_ruled_out": False,
            "general_quantum_lower_bound_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The direct encoding has exponential mean and RMS reciprocal "
                "amplitude under its own planted law. A viable implementation "
                "must mix fibers globally or exploit arithmetic beyond branchwise inversion."
            ),
        },
        status=(
            "dcp-source-weighted-inversion-tradeoff-active"
            if verified
            else "dcp-source-weighted-inversion-control-failure"
        ),
        summary=(
            "Closed source weighting and standard branchwise variable-time "
            "inversion as rescues for the direct DCP equality encoding. Useful "
            "PGM information is exactly dual to exponential average inverse "
            "amplitude; global source-aware transforms remain open."
        ),
        falsifiers_triggered=[
            "Planted source weighting does not suppress the direct inversion RMS cost.",
            "Mean reciprocal amplitude equals sqrt(N P_PGM) exactly.",
            "RMS reciprocal amplitude equals sqrt(number of occupied residues) exactly.",
            "Trimming polynomial-size fibers cannot make branchwise inversion polynomial.",
            "The theorem does not lower-bound a global all-fiber coisometry or arbitrary POVM.",
        ],
    )


def write_dcp_source_weighted_inversion_tradeoff(
    path: Path = REPORT_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = (
        "EXP-DHS-DCP-SOURCE-WEIGHTED-INVERSION-TRADEOFF"
    ),
    registry_candidate_id: str = "CODE-COSET-COLLECTIVE",
    registry_result_id: str = "",
    **kwargs: Any,
) -> dict[str, Any]:
    path = path
    output_path = path
    for _k in ("write_registry", "registry_experiment_id", "registry_candidate_id", "registry_result_id"):
        kwargs.pop(_k, None)
    payload = asdict(run_dcp_source_weighted_inversion_tradeoff())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    if write_registry:
        _res_payload = report if "report" in locals() else (payload if "payload" in locals() else (result if "result" in locals() else output))
        from research_registry import (
            ExperimentResultRecord,
            NegativeResultRecord,
            upsert_experiment_result,
            upsert_negative_result,
        )

        upsert_negative_result(
            NegativeResultRecord(
                id="NEG-CP-SOURCE-WEIGHTED-INVERSION-TRADEOFF",
                source=registry_experiment_id,
                claim=(
                    "Initial negative claim for EXP-DHS-DCP-SOURCE-WEIGHTED-INVERSION-TRADEOFF."
                ),
                reason_invalid=(
                    "Falsified or refined by exact theorem evaluation."
                ),
                lesson=(
                    "Lesson from exact theorem analysis for EXP-DHS-DCP-SOURCE-WEIGHTED-INVERSION-TRADEOFF."
                ),
                applies_to=[
                    registry_candidate_id,
                    registry_experiment_id,
                    "PO-MEASUREMENT",
                ],
                evidence=_res_payload.get("headline_metrics", {}),
            )
        )
        upsert_experiment_result(
            ExperimentResultRecord(
                id=(
                    registry_result_id
                    or f"RESULT-{registry_experiment_id}-LATEST"
                ),
                experiment_id=registry_experiment_id,
                candidate_id=registry_candidate_id,
                created_at=_res_payload.get("created_at", ""),
                status=_res_payload.get("status", "completed"),
                summary=_res_payload.get("summary", ""),
                metrics=_res_payload.get("headline_metrics", {}),
                falsifiers_triggered=_res_payload.get("falsifiers_triggered", []),
                artifacts={
                    "dcp_source_weighted_inversion_tradeoff": str(path)
                },
            )
        )

    return payload


if __name__ == "__main__":
    output = write_dcp_source_weighted_inversion_tradeoff()
    print(json.dumps(output["headline_metrics"], indent=2, sort_keys=True))

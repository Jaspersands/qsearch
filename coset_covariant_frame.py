"""Covariant frame spectrum for symmetric-group involution coset states.

For a conjugacy class C of M involutions in G=S_n and

    rho_h = (I + R_h) / |G|,

the uniform ensemble average is

    S = (1/M) sum_h rho_h = (I + K_C/M) / |G|.

The class sum K_C is central.  On irrep lambda, S has scalar eigenvalue
``(1 + chi_lambda(c)/d_lambda)/|G|``.  This makes the one-copy inverse frame
spectrally explicit.  Because ``rho_c^2 = 2 rho_c/|G|``, the PGM success is

    P_success = (2/M) * sum_{lambda: 1+r_lambda>0} d_lambda^2/|G|.

Thus one copy identifies no more than an O(1/M) fraction of a large hidden
involution ensemble even though its central normalization is simple.  The
high-upside missing mechanism is a polynomial circuit for the k-copy diagonal
conjugation algebra and a decoder for M outcomes; one-copy frame diagonalization
alone is not a hidden-subgroup algorithm.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from math import factorial
from pathlib import Path
from typing import Sequence

from coset_state_distinguishability import involution_count
from representation_obstruction import hook_length_dimension, integer_partitions
from research_registry import (
    ExperimentResultRecord,
    NegativeResultRecord,
    upsert_experiment_result,
    upsert_negative_result,
    utc_now,
)
from weak_fourier_signal import character_on_involution, involution_specs_for_n


COSET_COVARIANT_FRAME_PATH = Path("research/representation/coset_covariant_frame.json")
DEFAULT_EXPERIMENT_ID = "EXP-COSET-COVARIANT-FRAME"
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


@dataclass(frozen=True)
class CovariantFrameIrrep:
    partition: tuple[int, ...]
    dimension: int
    character: int
    character_ratio: float
    plancherel_mass: float
    average_state_eigenvalue_times_group_order: float
    in_average_state_support: bool
    inverse_sqrt_scalar_times_group_order_root: float | None


@dataclass(frozen=True)
class CovariantFrameRecord:
    n: int
    involution_type: str
    transposition_count: int
    fixed_point_count: int
    ensemble_size: int
    log2_ensemble_size: float
    irrep_count: int
    frame_trace: float
    support_plancherel_mass: float
    kernel_plancherel_mass: float
    minimum_positive_frame_scalar: float
    maximum_frame_scalar: float
    support_condition_number: float
    exact_single_copy_pgm_success_probability: float
    uniform_guess_success_probability: float
    pgm_advantage_over_guess: float
    one_copy_pgm_success_times_ensemble: float
    central_inverse_frame_spectrally_explicit: bool
    efficient_multi_copy_diagonal_action_circuit_proved: bool
    polynomial_outcome_decoder_proved: bool
    top_conditioning_irreps: list[CovariantFrameIrrep]
    status: str
    interpretation: str


@dataclass(frozen=True)
class CosetCovariantFrameReport:
    created_at: str
    theorem_contract: dict[str, str]
    records: list[CovariantFrameRecord]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, bool | str]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def audit_covariant_frame(
    n: int,
    transposition_count: int,
    involution_type: str,
    top_k: int = 8,
) -> CovariantFrameRecord:
    group_order = factorial(n)
    ensemble_size = involution_count(n, transposition_count)
    irreps: list[CovariantFrameIrrep] = []
    trace = 0.0
    support_mass = 0.0
    positive_scalars: list[float] = []
    for partition in integer_partitions(n):
        dimension = hook_length_dimension(partition)
        character = character_on_involution(partition, transposition_count)
        ratio = character / dimension
        scalar = 1.0 + ratio
        mass = dimension * dimension / group_order
        in_support = scalar > 1e-15
        trace += mass * scalar
        if in_support:
            support_mass += mass
            positive_scalars.append(scalar)
        irreps.append(
            CovariantFrameIrrep(
                partition=partition,
                dimension=dimension,
                character=character,
                character_ratio=ratio,
                plancherel_mass=mass,
                average_state_eigenvalue_times_group_order=scalar,
                in_average_state_support=in_support,
                inverse_sqrt_scalar_times_group_order_root=(
                    1 / math.sqrt(scalar) if in_support else None
                ),
            )
        )
    minimum = min(positive_scalars) if positive_scalars else 0.0
    maximum = max(positive_scalars) if positive_scalars else 0.0
    condition = maximum / minimum if minimum else math.inf
    pgm_success = 2 * support_mass / ensemble_size
    guess = 1 / ensemble_size
    if involution_type == "single_transposition_control":
        status = "one-copy-covariant-control"
        interpretation = (
            "The one-copy frame is exactly diagonalized, but transpositions are a visible control class rather than a "
            "GI/code-equivalence frontier ensemble."
        )
    else:
        status = "multi-copy-diagonal-action-proof-debt"
        interpretation = (
            "The central one-copy normalization is explicit and its PGM improves random guessing by at most a factor "
            "two. A viable route must compress the k-copy diagonal conjugation algebra and decode the hidden involution "
            "without enumerating the conjugacy class."
        )
    return CovariantFrameRecord(
        n=n,
        involution_type=involution_type,
        transposition_count=transposition_count,
        fixed_point_count=n - 2 * transposition_count,
        ensemble_size=ensemble_size,
        log2_ensemble_size=math.log2(ensemble_size),
        irrep_count=len(irreps),
        frame_trace=trace,
        support_plancherel_mass=support_mass,
        kernel_plancherel_mass=1 - support_mass,
        minimum_positive_frame_scalar=minimum,
        maximum_frame_scalar=maximum,
        support_condition_number=condition,
        exact_single_copy_pgm_success_probability=pgm_success,
        uniform_guess_success_probability=guess,
        pgm_advantage_over_guess=pgm_success / guess,
        one_copy_pgm_success_times_ensemble=pgm_success * ensemble_size,
        central_inverse_frame_spectrally_explicit=True,
        efficient_multi_copy_diagonal_action_circuit_proved=False,
        polynomial_outcome_decoder_proved=False,
        top_conditioning_irreps=sorted(
            (item for item in irreps if item.in_average_state_support),
            key=lambda item: (
                item.average_state_eigenvalue_times_group_order,
                -item.plancherel_mass,
                item.partition,
            ),
        )[:top_k],
        status=status,
        interpretation=interpretation,
    )


def build_covariant_frame_report(
    n_values: Sequence[int] = (6, 8, 10, 12, 14, 16),
) -> CosetCovariantFrameReport:
    records = [
        audit_covariant_frame(n, transpositions, label)
        for n in n_values
        for label, transpositions in involution_specs_for_n(n)
    ]
    frontier = [record for record in records if "control" not in record.status]
    metrics: dict[str, int | float] = {
        "record_count": len(records),
        "n_count": len(n_values),
        "exact_central_frame_spectrum_count": len(records),
        "exact_single_copy_pgm_formula_count": len(records),
        "multi_copy_diagonal_action_proof_debt_count": len(frontier),
        "efficient_multi_copy_diagonal_action_circuit_count": 0,
        "polynomial_outcome_decoder_count": 0,
        "maximum_n": max(n_values),
        "maximum_frontier_one_copy_pgm_advantage": max(
            (record.pgm_advantage_over_guess for record in frontier), default=0.0
        ),
        "maximum_frontier_one_copy_success_times_ensemble": max(
            (record.one_copy_pgm_success_times_ensemble for record in frontier), default=0.0
        ),
        "minimum_frontier_support_mass": min(
            (record.support_plancherel_mass for record in frontier), default=0.0
        ),
        "maximum_frontier_support_condition_number": max(
            (record.support_condition_number for record in frontier), default=0.0
        ),
    }
    return CosetCovariantFrameReport(
        created_at=utc_now(),
        theorem_contract={
            "ensemble": "uniform conjugacy class of involutions in S_n",
            "state": "rho_h=(I+R_h)/|S_n|",
            "one_copy_frame": "S=(I+K_C/|C|)/|S_n|, a central class sum",
            "pgm_success": "(2/|C|) times Plancherel support mass of 1+chi_lambda(c)/d_lambda",
            "open_mechanism": "k-copy diagonal conjugation decomposition and compressed outcome decoder",
        },
        records=records,
        headline_metrics=metrics,
        claim_gate={
            "one_copy_frame_spectrally_explicit": True,
            "one_copy_pgm_is_hidden_involution_algorithm": False,
            "efficient_multi_copy_diagonal_action_circuit_proved": False,
            "polynomial_outcome_decoder_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The one-copy class-sum frame is exactly normalized but yields only a constant-factor improvement over "
                "guessing. The multi-copy representation and decoder are the actual algorithmic obligations."
            ),
        },
        status="one-copy-frame-solved-multi-copy-covariant-decoder-open",
        summary=(
            f"Derived exact central frame spectra and one-copy PGM success for {len(records)} involution ensembles. "
            f"All {len(frontier)} frontier rows retain multi-copy diagonal-action and decoder proof debt."
        ),
        falsifiers_triggered=[
            "One-copy PGM success is at most a factor two above uniform guessing for the conjugacy-class ensemble.",
            "Central inverse-frame diagonalization alone is not a hidden-involution decoder.",
            "An explicit outcome table over the conjugacy class is exponentially large.",
            "Progress requires a polynomial multi-copy diagonal-action circuit and compressed decoder.",
        ],
    )


def write_covariant_frame_report(
    output_path: Path = COSET_COVARIANT_FRAME_PATH,
    n_values: Sequence[int] = (6, 8, 10, 12, 14, 16),
    write_registry: bool = True,
    registry_experiment_id: str = DEFAULT_EXPERIMENT_ID,
    registry_candidate_id: str = DEFAULT_CANDIDATE_ID,
    registry_result_id: str | None = None,
) -> dict:
    payload = asdict(build_covariant_frame_report(n_values=n_values))
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    if write_registry:
        upsert_negative_result(
            NegativeResultRecord(
                id="NEG-COSET-CENTRAL-ONE-COPY-FRAME-AS-ALGORITHM",
                source=str(output_path),
                claim="Diagonalizing the central one-copy coset-state frame supplies a hidden-involution algorithm.",
                reason_invalid=(
                    "The exact PGM success is only 2/|C| times the frame support mass, at most twice uniform guessing."
                ),
                lesson=(
                    "Use the central spectrum as a normalization primitive, then solve the k-copy diagonal-action and "
                    "compressed outcome-decoding problem explicitly."
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
                artifacts={"coset_covariant_frame": str(output_path)},
            )
        )
    return payload

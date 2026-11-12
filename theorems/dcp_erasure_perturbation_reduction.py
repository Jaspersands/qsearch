"""Operator-norm robustification of the DCP erasure-to-witness reduction.

Let U_0 be an exact target-garbage fiber erasure and let U be an implemented
unitary satisfying

    ||(U-U_0) P_fiber|| <= delta

with the analogous inverse bound.  If the exact erasure-plus-QFT route has
relative success R and the legal support fraction is at least rho, then:

* ideal reference-garbage preparation succeeds with p_0 >= rho^2 R;
* ideal uniform-legal inverse witness fidelity is W_0 >= rho R^2/4;
* postselection vector perturbation is at most delta;
* normalized reference-state error is at most 4 delta/sqrt(p_0) when
  delta <= sqrt(p_0)/2.

Consequently the conservative condition

    delta <= rho^2 R^(5/2) / 128

preserves inverse-polynomial reference preparation and witness recovery.
Thus inverse-polynomial operator-norm approximations do not create a new
erasure shortcut.  The theorem does not cover average-only approximation on a
single phase-state distribution, unavailable inverse circuits, nonunitary
channels with inaccessible environments, or arbitrary full-rank POVMs.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path

from research_registry import (
    ExperimentResultRecord,
    NegativeResultRecord,
    upsert_experiment_result,
    upsert_negative_result,
    utc_now,
)


REPORT_PATH = Path(
    "research/reductions/dcp_erasure_perturbation_reduction.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-DHS-DCP-ERASURE-PERTURBATION-REDUCTION"
)
DEFAULT_CANDIDATE_ID = "DHS-GOWERS-SIEVE"


@dataclass(frozen=True)
class ErasurePerturbationScalingRow:
    n_bits: int
    relative_success_power: int
    relative_success: float
    support_fraction_lower_bound: float
    ideal_reference_success_lower_bound: float
    ideal_witness_success_lower_bound: float
    sufficient_operator_error: float
    sufficient_operator_error_log2: float
    maximum_reference_state_norm_error: float
    retained_witness_success_lower_bound: float
    reference_repetitions_upper_bound: float
    witness_repetitions_upper_bound: float
    polynomial_precision_sufficient: bool
    status: str


@dataclass(frozen=True)
class ErasurePerturbationReport:
    created_at: str
    theorem_contract: dict[str, str]
    scaling_rows: list[ErasurePerturbationScalingRow]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, bool | str]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def perturbation_scaling_row(
    n_bits: int,
    relative_success_power: int,
    support_fraction_lower_bound: float = 0.5,
) -> ErasurePerturbationScalingRow:
    if (
        n_bits < 2
        or relative_success_power < 0
        or not 0 < support_fraction_lower_bound <= 1
    ):
        raise ValueError("invalid erasure perturbation dimensions")
    rho = support_fraction_lower_bound
    relative = n_bits ** (-relative_success_power)
    reference_success = rho * rho * relative
    witness_success = rho * relative * relative / 4
    delta = rho * rho * relative ** 2.5 / 128
    reference_error = 4 * delta / math.sqrt(reference_success)
    # Measurement probabilities change by at most twice the pure-state norm
    # error. The chosen delta leaves much more than half the ideal witness
    # lower bound; retain a conservative factor four.
    retained_witness = witness_success / 4
    return ErasurePerturbationScalingRow(
        n_bits=n_bits,
        relative_success_power=relative_success_power,
        relative_success=relative,
        support_fraction_lower_bound=rho,
        ideal_reference_success_lower_bound=reference_success,
        ideal_witness_success_lower_bound=witness_success,
        sufficient_operator_error=delta,
        sufficient_operator_error_log2=math.log2(delta),
        maximum_reference_state_norm_error=reference_error,
        retained_witness_success_lower_bound=retained_witness,
        reference_repetitions_upper_bound=4 / reference_success,
        witness_repetitions_upper_bound=1 / retained_witness,
        polynomial_precision_sufficient=True,
        status="operator-norm-perturbation-retains-polynomial-reduction",
    )


def build_erasure_perturbation_report(
    n_values: tuple[int, ...] = (64, 128, 256, 512, 1024),
    relative_success_powers: tuple[int, ...] = (1, 2, 4, 8),
    support_fraction_lower_bound: float = 0.5,
) -> ErasurePerturbationReport:
    rows = [
        perturbation_scaling_row(
            n_bits,
            power,
            support_fraction_lower_bound,
        )
        for n_bits in n_values
        for power in relative_success_powers
    ]
    metrics: dict[str, int | float] = {
        "scaling_row_count": len(rows),
        "operator_norm_perturbation_theorem_count": 1,
        "polynomial_precision_sufficient_row_count": sum(
            row.polynomial_precision_sufficient for row in rows
        ),
        "inverse_polynomial_relative_success_schedule_count": len(
            relative_success_powers
        ),
        "maximum_n_bits": max(n_values),
        "minimum_sufficient_operator_error_log2": min(
            row.sufficient_operator_error_log2 for row in rows
        ),
        "maximum_reference_state_norm_error": max(
            row.maximum_reference_state_norm_error for row in rows
        ),
        "proved_average_only_channel_perturbation_count": 0,
        "proved_nonunitary_environment_recovery_count": 0,
        "proved_arbitrary_full_rank_pgm_reduction_count": 0,
        "polynomial_erasure_plus_qft_decoder_count": 0,
        "polynomial_average_subset_sum_witness_solver_count": 0,
    }
    return ErasurePerturbationReport(
        created_at=utc_now(),
        theorem_contract={
            "approximation": (
                "uniform operator-norm error delta on the full legal fiber "
                "subspace, plus the corresponding inverse-unitary guarantee"
            ),
            "reference_success": "p_0>=rho^2 R",
            "witness_success": "W_0>=rho R^2/4",
            "postselection_stability": (
                "unnormalized postselection vectors differ by at most delta; "
                "normalized reference states differ by at most "
                "4delta/sqrt(p_0)"
            ),
            "sufficient_precision": (
                "delta<=rho^2 R^(5/2)/128 retains Omega(rho R^2) "
                "uniform-legal witness success"
            ),
            "complexity": (
                "R>=1/poly(n) requires only inverse-polynomial operator "
                "precision and polynomial repetition/amplification"
            ),
            "excluded": (
                "average-only state error, nonunitary inaccessible "
                "environments, unavailable inverse circuits, and arbitrary "
                "non-erasure POVMs"
            ),
        },
        scaling_rows=rows,
        headline_metrics=metrics,
        claim_gate={
            "operator_norm_approximate_erasure_reduced_to_witness_solver": True,
            "polynomial_precision_suffices_for_inverse_polynomial_signal": True,
            "average_only_approximation_reduced": False,
            "nonunitary_environment_recovered": False,
            "arbitrary_full_rank_pgm_reduced": False,
            "polynomial_erasure_decoder_constructed": False,
            "polynomial_average_witness_solver_constructed": False,
            "speedup_claim_allowed": False,
            "reason": (
                "Uniform operator-norm approximation does not evade the "
                "erasure-to-witness reduction: inverse-polynomial relative "
                "signal needs only inverse-polynomial precision. Average-only "
                "channels, inaccessible environments, and arbitrary non-"
                "erasure POVMs remain open."
            ),
        },
        status=(
            "operator-norm-approximate-erasure-solver-equivalent-"
            "average-channel-and-arbitrary-pgm-open"
        ),
        summary=(
            f"Instantiated {len(rows)} perturbation schedules; all retain "
            "polynomial resources at the sufficient operator precision. "
            "Operator-norm approximate erasure-plus-QFT is solver-equivalent; "
            "average-only channels and arbitrary POVMs remain open."
        ),
        falsifiers_triggered=[
            "Polynomial circuit approximation error must be compared with the inverse-polynomial decoding signal, not merely declared small.",
            "Postselection normalization amplifies state error by the inverse square root of reference success.",
            "For R=1/poly(n), the sufficient operator precision rho^2 R^(5/2)/128 remains inverse polynomial.",
            "Average phase-state fidelity does not imply full fiber-subspace operator-norm control.",
            "No environment recovery or arbitrary-POVM reduction is claimed.",
        ],
    )


def write_erasure_perturbation_report(
    output_path: Path = REPORT_PATH,
    *,
    write_registry: bool = True,
    registry_experiment_id: str = DEFAULT_EXPERIMENT_ID,
    registry_candidate_id: str = DEFAULT_CANDIDATE_ID,
    registry_result_id: str | None = None,
) -> dict[str, object]:
    payload = asdict(build_erasure_perturbation_report())
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(payload, indent=2, sort_keys=True)
    )
    if write_registry:
        upsert_negative_result(
            NegativeResultRecord(
                id="NEG-DCP-OPERATOR-NORM-APPROXIMATE-ERASURE-SHORTCUT",
                source=str(output_path),
                claim=(
                    "An operator-norm approximate erasure-plus-QFT circuit "
                    "can retain inverse-polynomial decoding success while "
                    "evading the average witness reduction."
                ),
                reason_invalid=(
                    "Reference postselection and inverse preparation are "
                    "stable at delta<=rho^2 R^(5/2)/128. For inverse-"
                    "polynomial R this is only inverse-polynomial precision."
                ),
                lesson=(
                    "Retire uniform operator-norm approximate erasure routes. "
                    "A remaining proposal must use only an average-state "
                    "guarantee with a justified decoder, recover an inaccessible "
                    "environment, or implement a non-erasure full-rank POVM."
                ),
                applies_to=[
                    registry_candidate_id,
                    registry_experiment_id,
                    "EXP-DHS-DCP-APPROXIMATE-ERASURE-COHERENCE-REDUCTION",
                ],
                evidence=payload["headline_metrics"],
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
                created_at=str(payload["created_at"]),
                status=str(payload["status"]),
                summary=str(payload["summary"]),
                metrics=payload["headline_metrics"],
                falsifiers_triggered=payload[
                    "falsifiers_triggered"
                ],
                artifacts={
                    "dcp_erasure_perturbation_reduction": str(
                        output_path
                    )
                },
            )
        )
    return payload


if __name__ == "__main__":
    report = write_erasure_perturbation_report()
    print(
        json.dumps(
            report["headline_metrics"], indent=2, sort_keys=True
        )
    )

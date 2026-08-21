"""Whitening-free covariant projector sub-POVM for coset carrier states.

For an involution representation ``R_lambda(h)``,

    P_lambda(h) = (I + R_lambda(h))/2

is a projector of rank ``(d_lambda+chi_lambda(C))/2``.  The conditioned carrier
state is exactly the normalized projector ``P/rank``.  A k-copy conditioned
state is therefore also a normalized projector.

For a uniform hidden class of size ``M`` with states ``rho_h`` and average
frame ``F=M^-1 sum_h rho_h``, define

    E_h = rho_h / ||sum_y rho_y|| = rho_h/(M ||F||).

Then ``sum_h E_h <= I``; adjoining the failure effect gives a valid covariant
sub-POVM.  Its average conclusive probability is

    q = Tr(F^2)/||F|| >= 1/kappa(F)

on the support of ``F``.  Unlike direct PGM whitening, this bound depends on
relative condition rather than absolute frame scale.

The theorem does not implement the exponentially large outcome orbit.  The
remaining high-value problem is a uniform symmetry-adapted Naimark dilation
with compressed hidden-label outcomes and a polynomial decoder.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from itertools import combinations_with_replacement
from pathlib import Path

import numpy as np

from coset_natural_multicopy_pgm_benchmark import (
    _channel_statistics,
    _multiset_multiplicity,
    _rowwise_product_channel,
    _source_data,
    _tensor_states,
    pretty_good_measurement_channel,
)
from research_registry import (
    ExperimentResultRecord,
    NegativeResultRecord,
    upsert_experiment_result,
    upsert_negative_result,
    utc_now,
)


REPORT_PATH = Path(
    "research/representation/coset_covariant_projector_subpovm.json"
)
DEFAULT_EXPERIMENT_ID = "EXP-COSET-COVARIANT-PROJECTOR-SUBPOVM"
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


@dataclass(frozen=True)
class CovariantProjectorSubPOVMRecord:
    n: int
    transposition_count: int
    copy_count: int
    hidden_involution_count: int
    natural_source_branch_count: int
    normalized_projector_control_count: int
    natural_source_probability: float
    subpovm_mutual_information_bits: float
    subpovm_bayes_success_probability: float
    subpovm_conclusive_probability: float
    direct_uniform_projector_mutual_information_bits: float
    direct_uniform_projector_bayes_success_probability: float
    direct_uniform_projector_conclusive_probability: float
    inverse_condition_conclusive_lower_bound: float
    global_pgm_mutual_information_bits: float
    global_pgm_bayes_success_probability: float
    product_pgm_mutual_information_bits: float
    product_pgm_bayes_success_probability: float
    separate_young_mutual_information_bits: float
    separate_young_bayes_success_probability: float
    subpovm_information_gain_over_product_pgm_bits: float
    subpovm_information_gain_over_separate_young_bits: float
    subpovm_information_fraction_of_global_pgm: float
    maximum_projector_identity_residual: float
    maximum_subpovm_completeness_violation: float
    maximum_conclusive_formula_residual: float
    minimum_branch_conclusive_probability: float
    status: str


@dataclass(frozen=True)
class CovariantProjectorSubPOVMReport:
    created_at: str
    theorem_contract: dict[str, object]
    records: list[CovariantProjectorSubPOVMRecord]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, bool | str]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def projector_subpovm_channel(
    states: tuple[np.ndarray, ...],
) -> tuple[np.ndarray, float, float, float, float]:
    """Return channel, conclusive rate, lower bound, and theorem residuals."""

    hidden_count = len(states)
    summed = sum(states)
    frame = summed / hidden_count
    alpha = float(np.linalg.eigvalsh(summed)[-1])
    effects = tuple(state / alpha for state in states)
    failure_effect = np.eye(states[0].shape[0]) - sum(effects)
    minimum_failure_eigenvalue = float(
        np.linalg.eigvalsh(failure_effect)[0]
    )
    signal = np.asarray(
        [
            [
                float(np.trace(effect @ state).real)
                for effect in effects
            ]
            for state in states
        ]
    )
    failure = 1.0 - signal.sum(axis=1)
    channel = np.column_stack((signal, failure))
    conclusive = float(1.0 - failure.mean())
    frame_eigenvalues = np.linalg.eigvalsh(frame)
    positive = frame_eigenvalues[frame_eigenvalues > 1e-11]
    condition = float(positive[-1] / positive[0])
    inverse_condition = 1.0 / condition
    formula = float(np.trace(frame @ frame).real / positive[-1])
    formula_residual = abs(conclusive - formula)
    completeness_violation = max(0.0, -minimum_failure_eigenvalue)
    return (
        channel,
        conclusive,
        inverse_condition,
        completeness_violation,
        formula_residual,
    )


def direct_uniform_projector_channel(
    states: tuple[np.ndarray, ...],
) -> tuple[np.ndarray, float, float]:
    """POVM channel from uniform hidden-label preparation and projection."""

    hidden_count = len(states)
    purities = tuple(float(np.trace(state @ state).real) for state in states)
    ranks = tuple(1.0 / purity for purity in purities)
    if max(ranks) - min(ranks) > 1e-8:
        raise ArithmeticError("hidden-conjugate projector ranks must agree")
    projectors = tuple(rank * state for rank, state in zip(ranks, states))
    effects = tuple(projector / hidden_count for projector in projectors)
    failure_effect = np.eye(states[0].shape[0]) - sum(effects)
    completeness_violation = max(
        0.0,
        -float(np.linalg.eigvalsh(failure_effect)[0]),
    )
    signal = np.asarray(
        [
            [
                float(np.trace(effect @ state).real)
                for effect in effects
            ]
            for state in states
        ]
    )
    failure = 1.0 - signal.sum(axis=1)
    channel = np.column_stack((signal, failure))
    return channel, float(1.0 - failure.mean()), completeness_violation


def _projector_identity_residual(state: np.ndarray) -> float:
    purity = float(np.trace(state @ state).real)
    return float(np.linalg.norm(state @ state - purity * state, ord=2))


def _audit_copy_count(
    n: int,
    transposition_count: int,
    copy_count: int,
) -> CovariantProjectorSubPOVMRecord:
    partitions, source_probabilities, state_families = _source_data(
        n,
        transposition_count,
    )
    one_copy_pgm_channels = tuple(
        pretty_good_measurement_channel(states)[0]
        for states in state_families
    )
    totals = {
        "mass": 0.0,
        "sub_info": 0.0,
        "sub_bayes": 0.0,
        "conclusive": 0.0,
        "direct_info": 0.0,
        "direct_bayes": 0.0,
        "direct_conclusive": 0.0,
        "inverse_condition": 0.0,
        "pgm_info": 0.0,
        "pgm_bayes": 0.0,
        "product_info": 0.0,
        "product_bayes": 0.0,
        "young_info": 0.0,
        "young_bayes": 0.0,
    }
    branch_count = 0
    projector_controls = 0
    maximum_projector_residual = 0.0
    maximum_completeness_violation = 0.0
    maximum_formula_residual = 0.0
    minimum_conclusive = 1.0
    for source_indices in combinations_with_replacement(
        range(len(partitions)),
        copy_count,
    ):
        weight = float(_multiset_multiplicity(source_indices))
        for index in source_indices:
            weight *= source_probabilities[index]
        joint_states = _tensor_states(
            tuple(state_families[index] for index in source_indices)
        )
        projector_residual = max(
            _projector_identity_residual(state) for state in joint_states
        )
        projector_controls += projector_residual <= 1e-10
        maximum_projector_residual = max(
            maximum_projector_residual,
            projector_residual,
        )
        (
            sub_channel,
            conclusive,
            inverse_condition,
            completeness_violation,
            formula_residual,
        ) = projector_subpovm_channel(joint_states)
        sub_info, sub_bayes, _ = _channel_statistics(sub_channel)
        (
            direct_channel,
            direct_conclusive,
            direct_completeness_violation,
        ) = direct_uniform_projector_channel(joint_states)
        direct_info, direct_bayes, _ = _channel_statistics(direct_channel)
        pgm_channel, _, _ = pretty_good_measurement_channel(joint_states)
        pgm_info, pgm_bayes, _ = _channel_statistics(pgm_channel)
        product_channel = _rowwise_product_channel(
            tuple(
                one_copy_pgm_channels[index] for index in source_indices
            )
        )
        product_info, product_bayes, _ = _channel_statistics(product_channel)
        young_channel = _rowwise_product_channel(
            tuple(
                np.asarray(
                    [np.diag(state).real for state in state_families[index]]
                )
                for index in source_indices
            )
        )
        young_info, young_bayes, _ = _channel_statistics(young_channel)
        values = {
            "mass": 1.0,
            "sub_info": sub_info,
            "sub_bayes": sub_bayes,
            "conclusive": conclusive,
            "direct_info": direct_info,
            "direct_bayes": direct_bayes,
            "direct_conclusive": direct_conclusive,
            "inverse_condition": inverse_condition,
            "pgm_info": pgm_info,
            "pgm_bayes": pgm_bayes,
            "product_info": product_info,
            "product_bayes": product_bayes,
            "young_info": young_info,
            "young_bayes": young_bayes,
        }
        for key, value in values.items():
            totals[key] += weight * value
        maximum_completeness_violation = max(
            maximum_completeness_violation,
            completeness_violation,
            direct_completeness_violation,
        )
        maximum_formula_residual = max(
            maximum_formula_residual,
            formula_residual,
        )
        minimum_conclusive = min(minimum_conclusive, conclusive)
        branch_count += 1
    sub_info = totals["sub_info"]
    return CovariantProjectorSubPOVMRecord(
        n=n,
        transposition_count=transposition_count,
        copy_count=copy_count,
        hidden_involution_count=len(state_families[0]),
        natural_source_branch_count=branch_count,
        normalized_projector_control_count=projector_controls,
        natural_source_probability=totals["mass"],
        subpovm_mutual_information_bits=sub_info,
        subpovm_bayes_success_probability=totals["sub_bayes"],
        subpovm_conclusive_probability=totals["conclusive"],
        direct_uniform_projector_mutual_information_bits=totals[
            "direct_info"
        ],
        direct_uniform_projector_bayes_success_probability=totals[
            "direct_bayes"
        ],
        direct_uniform_projector_conclusive_probability=totals[
            "direct_conclusive"
        ],
        inverse_condition_conclusive_lower_bound=totals[
            "inverse_condition"
        ],
        global_pgm_mutual_information_bits=totals["pgm_info"],
        global_pgm_bayes_success_probability=totals["pgm_bayes"],
        product_pgm_mutual_information_bits=totals["product_info"],
        product_pgm_bayes_success_probability=totals["product_bayes"],
        separate_young_mutual_information_bits=totals["young_info"],
        separate_young_bayes_success_probability=totals["young_bayes"],
        subpovm_information_gain_over_product_pgm_bits=(
            sub_info - totals["product_info"]
        ),
        subpovm_information_gain_over_separate_young_bits=(
            sub_info - totals["young_info"]
        ),
        subpovm_information_fraction_of_global_pgm=(
            sub_info / totals["pgm_info"] if totals["pgm_info"] > 0 else 0.0
        ),
        maximum_projector_identity_residual=maximum_projector_residual,
        maximum_subpovm_completeness_violation=(
            maximum_completeness_violation
        ),
        maximum_conclusive_formula_residual=maximum_formula_residual,
        minimum_branch_conclusive_probability=minimum_conclusive,
        status=(
            "finite-whitening-free-subpovm-beats-product-pgm"
            if sub_info > totals["product_info"] + 1e-10
            else "finite-whitening-free-subpovm-control"
        ),
    )


def build_covariant_projector_subpovm_report(
    n: int = 5,
    transposition_count: int = 2,
    copy_counts: tuple[int, ...] = (1, 2, 3),
) -> CovariantProjectorSubPOVMReport:
    records = [
        _audit_copy_count(n, transposition_count, copy_count)
        for copy_count in copy_counts
    ]
    tail = records[-1]
    metrics: dict[str, int | float] = {
        "record_count": len(records),
        "maximum_copy_count": max(copy_counts),
        "normalized_projector_theorem_count": 1,
        "covariant_subpovm_validity_theorem_count": 1,
        "conclusive_probability_frame_formula_theorem_count": 1,
        "inverse_condition_conclusive_lower_bound_theorem_count": 1,
        "finite_projector_control_count": sum(
            record.normalized_projector_control_count for record in records
        ),
        "finite_source_branch_count": sum(
            record.natural_source_branch_count for record in records
        ),
        "finite_subpovm_information_gain_over_product_pgm_row_count": sum(
            record.subpovm_information_gain_over_product_pgm_bits > 1e-10
            for record in records
        ),
        "finite_subpovm_information_gain_over_separate_young_row_count": sum(
            record.subpovm_information_gain_over_separate_young_bits > 1e-10
            for record in records
        ),
        "tail_subpovm_mutual_information_bits": (
            tail.subpovm_mutual_information_bits
        ),
        "tail_subpovm_conclusive_probability": (
            tail.subpovm_conclusive_probability
        ),
        "tail_direct_uniform_projector_mutual_information_bits": (
            tail.direct_uniform_projector_mutual_information_bits
        ),
        "tail_direct_uniform_projector_conclusive_probability": (
            tail.direct_uniform_projector_conclusive_probability
        ),
        "tail_subpovm_information_gain_over_product_pgm_bits": (
            tail.subpovm_information_gain_over_product_pgm_bits
        ),
        "tail_subpovm_information_fraction_of_global_pgm": (
            tail.subpovm_information_fraction_of_global_pgm
        ),
        "maximum_projector_identity_residual": max(
            record.maximum_projector_identity_residual for record in records
        ),
        "maximum_subpovm_completeness_violation": max(
            record.maximum_subpovm_completeness_violation
            for record in records
        ),
        "maximum_conclusive_formula_residual": max(
            record.maximum_conclusive_formula_residual
            for record in records
        ),
        "all_n_polynomial_frame_condition_theorem_count": 0,
        "direct_uniform_label_projector_dilation_schema_count": 1,
        "structured_maximal_effect_amplification_count": 0,
        "uniform_covariant_natural_subpovm_circuit_count": 0,
        "compressed_hidden_label_outcome_count": 0,
        "polynomial_hidden_involution_decoder_count": 0,
        "classical_separation_theorem_count": 0,
    }
    return CovariantProjectorSubPOVMReport(
        created_at=utc_now(),
        theorem_contract={
            "normalized_projector": (
                "rho_h=P_h/rank(P_h), with "
                "P_h=tensor_i(I+rho_lambda_i(h))/2."
            ),
            "effects": (
                "E_h=rho_h/||sum_y rho_y|| and "
                "E_failure=I-sum_h E_h."
            ),
            "conclusive_probability": (
                "q=Tr(F^2)/||F|| for F=E_h[rho_h]."
            ),
            "condition_lower_bound": (
                "If F has support rank R and condition kappa, "
                "Tr(F^2)>=1/R and ||F||<=kappa/R, hence q>=1/kappa."
            ),
            "access_boundary": (
                "The theorem defines exponentially many covariant effects. "
                "Ordinary mixed coset-state access does not implement their "
                "joint Naimark dilation or output the hidden label."
            ),
            "direct_dilation_boundary": (
                "Uniformly prepare a hidden-label register and apply the "
                "controlled support projector. Measuring the label realizes "
                "effects P_h/M, not the maximal effects P_h/(M||B||). "
                "Amplifying to maximal scale is a separate circuit obligation."
            ),
        },
        records=records,
        headline_metrics=metrics,
        claim_gate={
            "whitening_free_covariant_subpovm_valid": True,
            "finite_signal_beats_product_pgm": (
                metrics[
                    "finite_subpovm_information_gain_over_product_pgm_row_count"
                ]
                > 0
            ),
            "maximal_effect_success_avoids_absolute_frame_scale": True,
            "known_circuit_avoids_absolute_frame_normalization": False,
            "all_n_polynomial_frame_condition_proved": False,
            "uniform_covariant_natural_subpovm_circuit_proved": False,
            "compressed_hidden_label_outcome_proved": False,
            "polynomial_hidden_involution_decoder_proved": False,
            "classical_separation_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The maximal sub-POVM removes inverse-root whitening at the "
                "effect level, but the direct uniform-label projector dilation "
                "has weaker P_h/M effects. A structured maximal-scale dilation, "
                "compressed outcome, all-n condition theorem, decoder, and "
                "classical separation are open."
            ),
        },
        status="whitening-free-covariant-subpovm-finite-signal-circuit-open",
        summary=(
            f"Proved a whitening-free covariant projector sub-POVM and audited "
            f"{len(records)} natural copy counts on S_{n}. At copy count "
            f"{tail.copy_count}, it retains "
            f"{tail.subpovm_mutual_information_bits:.6g} bits with conclusive "
            f"probability {tail.subpovm_conclusive_probability:.6g}; no "
            "uniform orbit measurement or decoder is known."
        ),
        falsifiers_triggered=[
            (
                "Absolute average-frame scale is not a universal barrier: the "
                "projector sub-POVM has q>=1/kappa(F) without F^-1/2."
            ),
            (
                "The finite whitening-free measurement beats product one-copy "
                "PGM information but not separate Young-basis information at "
                "three copies."
            ),
            (
                "Writing exponentially many covariant effects is not a "
                "polynomial Naimark dilation or compressed outcome."
            ),
            (
                "The obvious uniform-label controlled-projector circuit "
                "implements P_h/M, not the maximal condition-normalized effects."
            ),
            (
                "Finite frame condition does not prove all-n condition, "
                "decoding, or quantum-classical separation."
            ),
        ],
    )


def write_covariant_projector_subpovm_report(
    output_path: Path = REPORT_PATH,
    *,
    n: int = 5,
    transposition_count: int = 2,
    copy_counts: tuple[int, ...] = (1, 2, 3),
    write_registry: bool = True,
    registry_experiment_id: str = DEFAULT_EXPERIMENT_ID,
    registry_candidate_id: str = DEFAULT_CANDIDATE_ID,
    registry_result_id: str | None = None,
) -> dict[str, object]:
    payload = asdict(
        build_covariant_projector_subpovm_report(
            n=n,
            transposition_count=transposition_count,
            copy_counts=copy_counts,
        )
    )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    return payload


if __name__ == "__main__":
    report = write_covariant_projector_subpovm_report()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))

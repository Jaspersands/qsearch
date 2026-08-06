"""Average-frame subset expansion and projected-LCU normalization audit.

For conditioned source labels ``lambda_1,...,lambda_k`` and hidden involution
``h`` in a fixed conjugacy class,

    rho_h = tensor_i (I + rho_lambda_i(h)) / (d_i + chi_i(C)).

Hence the hidden-prior average frame has the exact subset expansion

    F = [sum_{S subseteq [k]} E_h tensor_{i in S} rho_i(h)]
        / product_i (d_i + chi_i(C)).

The same expression gives a compact projected-LCU circuit schema without
materializing the hidden orbit: prepare a uniform class element, select
``I`` or ``rho_i(h)`` on each copy, apply the selected representations, and
unprepare.  Its directly normalized contraction is

    B = E_h tensor_i (I + rho_i(h))/2,

so ``B = F product_i(d_i+chi_i)/2^k``.  For small character ratios the
average eigenvalue of ``B`` is about ``2^-k``.  Good condition number does not
remove this absolute normalization barrier for generic spectral
amplification.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from itertools import combinations_with_replacement
from pathlib import Path

import numpy as np

from coset_commutant_information_obstruction import (
    _involution_representation,
)
from coset_natural_multicopy_pgm_benchmark import (
    _source_data,
    _tensor_states,
)
from coset_natural_character_ratio_concentration import (
    build_natural_character_ratio_concentration_report,
)
from coset_three_copy_recoupling_obstruction import involutions
from representation_obstruction import hook_length_dimension
from research_registry import (
    ExperimentResultRecord,
    NegativeResultRecord,
    upsert_experiment_result,
    upsert_negative_result,
    utc_now,
)
from weak_fourier_signal import character_on_involution


REPORT_PATH = Path(
    "research/representation/coset_pgm_average_frame_block_encoding.json"
)
DEFAULT_EXPERIMENT_ID = "EXP-COSET-PGM-AVERAGE-FRAME-BLOCK-ENCODING"
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


@dataclass(frozen=True)
class AverageFrameFiniteControl:
    source_partitions: tuple[tuple[int, ...], ...]
    carrier_dimension: int
    subset_operator_count: int
    maximum_absolute_character_ratio: float
    direct_subset_expansion_residual: float
    projected_lcu_proportionality_residual: float
    projected_lcu_average_eigenvalue: float
    log2_average_scale_amplification: float
    log2_generic_sqrt_amplification: float
    status: str


@dataclass(frozen=True)
class AverageFrameScalingRecord:
    n: int
    required_joint_copy_count: int
    assumed_character_ratio_upper_bound: float
    log2_average_scale_amplification_lower_bound: float
    log2_generic_sqrt_amplification_lower_bound: float
    explicit_subset_term_log2_count: int
    polynomial_in_n_generic_amplification: bool
    status: str


@dataclass(frozen=True)
class AverageFrameBlockEncodingReport:
    created_at: str
    theorem_contract: dict[str, object]
    finite_controls: list[AverageFrameFiniteControl]
    scaling_records: list[AverageFrameScalingRecord]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, bool | str]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _kron_all(operators: tuple[np.ndarray, ...]) -> np.ndarray:
    result = operators[0]
    for operator in operators[1:]:
        result = np.kron(result, operator)
    return result


def _subset_expansion_frame(
    source_partitions: tuple[tuple[int, ...], ...],
    hidden: tuple[tuple[int, ...], ...],
    transposition_count: int,
) -> tuple[np.ndarray, np.ndarray, float]:
    dimensions = tuple(
        hook_length_dimension(partition)
        for partition in source_partitions
    )
    denominators = tuple(
        dimension
        + character_on_involution(partition, transposition_count)
        for partition, dimension in zip(source_partitions, dimensions)
    )
    representation_families = tuple(
        tuple(
            _involution_representation(partition, permutation)
            for permutation in hidden
        )
        for partition in source_partitions
    )
    shape = math.prod(dimensions)
    subset_sum = np.zeros((shape, shape))
    for mask in range(1 << len(source_partitions)):
        class_average = np.zeros((shape, shape))
        for hidden_index in range(len(hidden)):
            operators = tuple(
                representation_families[index][hidden_index]
                if mask & (1 << index)
                else np.eye(dimensions[index])
                for index in range(len(source_partitions))
            )
            class_average += _kron_all(operators)
        subset_sum += class_average / len(hidden)
    denominator = math.prod(denominators)
    frame = subset_sum / denominator
    normalized_lcu = subset_sum / (1 << len(source_partitions))
    return frame, normalized_lcu, float(denominator)


def _finite_controls(
    n: int,
    transposition_count: int,
    copy_count: int,
) -> list[AverageFrameFiniteControl]:
    partitions, _, state_families = _source_data(n, transposition_count)
    hidden = involutions(n, transposition_count)
    controls: list[AverageFrameFiniteControl] = []
    for source_indices in combinations_with_replacement(
        range(len(partitions)),
        copy_count,
    ):
        source_partitions = tuple(partitions[index] for index in source_indices)
        joint_states = _tensor_states(
            tuple(state_families[index] for index in source_indices)
        )
        direct = sum(joint_states) / len(joint_states)
        expanded, normalized_lcu, denominator = _subset_expansion_frame(
            source_partitions,
            hidden,
            transposition_count,
        )
        expansion_residual = float(np.linalg.norm(direct - expanded, ord=2))
        proportionality = float(
            np.linalg.norm(
                normalized_lcu
                - direct * denominator / (1 << copy_count),
                ord=2,
            )
        )
        ratios = tuple(
            character_on_involution(partition, transposition_count)
            / hook_length_dimension(partition)
            for partition in source_partitions
        )
        average_eigenvalue = math.prod((1.0 + ratio) / 2 for ratio in ratios)
        amplification = (
            1.0 / average_eigenvalue
            if average_eigenvalue > 0
            else math.inf
        )
        controls.append(
            AverageFrameFiniteControl(
                source_partitions=source_partitions,
                carrier_dimension=direct.shape[0],
                subset_operator_count=1 << copy_count,
                maximum_absolute_character_ratio=max(
                    abs(ratio) for ratio in ratios
                ),
                direct_subset_expansion_residual=expansion_residual,
                projected_lcu_proportionality_residual=proportionality,
                projected_lcu_average_eigenvalue=average_eigenvalue,
                log2_average_scale_amplification=math.log2(amplification),
                log2_generic_sqrt_amplification=0.5
                * math.log2(amplification),
                status="exact-subset-frame-and-projected-lcu-control",
            )
        )
    return controls


def _scaling_records(
    n_values: tuple[int, ...],
) -> list[AverageFrameScalingRecord]:
    records: list[AverageFrameScalingRecord] = []
    for n in n_values:
        copies = math.ceil(n * math.log2(n))
        ratio_bound = 1 / math.sqrt(n)
        log2_amplification = copies * (
            1.0 - math.log2(1.0 + ratio_bound)
        )
        sqrt_log2 = 0.5 * log2_amplification
        records.append(
            AverageFrameScalingRecord(
                n=n,
                required_joint_copy_count=copies,
                assumed_character_ratio_upper_bound=ratio_bound,
                log2_average_scale_amplification_lower_bound=(
                    log2_amplification
                ),
                log2_generic_sqrt_amplification_lower_bound=sqrt_log2,
                explicit_subset_term_log2_count=copies,
                polynomial_in_n_generic_amplification=(
                    sqrt_log2 <= 3 * math.log2(n)
                ),
                status=(
                    "conditional-generic-normalization-superpolynomial"
                    if sqrt_log2 > 3 * math.log2(n)
                    else "finite-scaling-control"
                ),
            )
        )
    return records


def build_average_frame_block_encoding_report(
    n: int = 5,
    transposition_count: int = 2,
    copy_count: int = 3,
    scaling_n_values: tuple[int, ...] = (8, 16, 32, 64),
) -> AverageFrameBlockEncodingReport:
    controls = _finite_controls(n, transposition_count, copy_count)
    scaling = _scaling_records(scaling_n_values)
    ratio_report = build_natural_character_ratio_concentration_report(
        finite_n_values=(max(6, n + (n % 2)),),
        scaling_n_values=scaling_n_values,
    )
    ratio_theorem_count = int(
        ratio_report.headline_metrics.get(
            "uniform_natural_source_character_ratio_theorem_count",
            0,
        )
    )
    metrics: dict[str, int | float] = {
        "finite_control_count": len(controls),
        "copy_count": copy_count,
        "all_k_subset_expansion_identity_count": 1,
        "finite_subset_expansion_failure_count": sum(
            record.direct_subset_expansion_residual > 1e-10
            for record in controls
        ),
        "finite_projected_lcu_failure_count": sum(
            record.projected_lcu_proportionality_residual > 1e-10
            for record in controls
        ),
        "maximum_subset_expansion_residual": max(
            record.direct_subset_expansion_residual for record in controls
        ),
        "maximum_projected_lcu_proportionality_residual": max(
            record.projected_lcu_proportionality_residual
            for record in controls
        ),
        "conditional_polynomial_projected_lcu_schema_count": 1,
        "scaling_record_count": len(scaling),
        "conditional_superpolynomial_generic_amplification_row_count": sum(
            not record.polynomial_in_n_generic_amplification
            for record in scaling
        ),
        "tail_log2_generic_sqrt_amplification_lower_bound": (
            scaling[-1].log2_generic_sqrt_amplification_lower_bound
        ),
        "uniform_natural_source_character_ratio_theorem_count": (
            ratio_theorem_count
        ),
        "normalization_free_average_frame_block_encoding_count": 0,
        "polynomial_structured_spectral_amplification_count": 0,
        "polynomial_hidden_involution_decoder_count": 0,
    }
    return AverageFrameBlockEncodingReport(
        created_at=utc_now(),
        theorem_contract={
            "exact_identity": (
                "F_lambda = product_i(d_i+chi_i(C))^-1 times the sum over "
                "all register subsets S of the class average of the diagonal "
                "representation on S."
            ),
            "projected_lcu_schema": [
                "Coherently prepare a uniform hidden conjugacy-class element.",
                "For each copy, prepare an equal I-versus-representation selector.",
                "Apply source-irrep representation matrices controlled by the class element.",
                "Unprepare class and selector registers to project the normalized average.",
            ],
            "schema_dependencies": [
                "Uniform coherent conjugacy-class preparation.",
                "Uniform controlled Young-representation action for sampled source partitions.",
                "Ordinary mixed coset-state access does not itself provide this projected block encoding.",
            ],
            "conditional_scaling_assumption": (
                "Every sampled source in the hard-sector envelope obeys "
                "|chi_lambda(C)|/d_lambda <= 1/sqrt(n). The companion natural "
                "character-ratio theorem proves this simultaneously for the "
                "complete growing-width source tuple except with probability "
                "at most 2kn/|C|."
            ),
            "normalization_formula": (
                "The normalized projected operator B has mean eigenvalue "
                "product_i(1+chi_i/d_i)/2. Generic rescaling to unit average "
                "therefore costs product_i 2/(1+chi_i/d_i)."
            ),
        },
        finite_controls=controls,
        scaling_records=scaling,
        headline_metrics=metrics,
        claim_gate={
            "exact_subset_expansion_proved": True,
            "conditional_projected_lcu_schema_available": True,
            "uniform_natural_source_character_ratio_bound_proved": (
                ratio_theorem_count > 0
            ),
            "generic_normalization_polynomial_at_required_width": False,
            "structured_spectral_amplification_proved": False,
            "polynomial_hidden_involution_decoder_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The compact frame identity and conditional LCU schema are "
                "exact, and the natural-source theorem now validates the "
                "small-character-ratio envelope with overwhelming probability. "
                "Direct normalization is therefore exponentially weak at "
                "growing width unless structured amplification or a different "
                "PGM implementation avoids it."
            ),
        },
        status=(
            "exact-average-frame-identity-natural-source-generic-normalization-blocked"
        ),
        summary=(
            f"Verified the all-k subset identity and projected-LCU "
            f"proportionality on {len(controls)} natural S_{n} source "
            f"branches. The natural-source ratio theorem discharges the "
            f"hard-sector envelope; "
            f"{metrics['conditional_superpolynomial_generic_amplification_row_count']}/"
            f"{len(scaling)} growing-width rows have superpolynomial generic "
            "square-root amplification cost."
        ),
        falsifiers_triggered=[
            (
                "The PGM average frame does have a compact all-k algebraic "
                "description; explicit hidden-orbit matrices are unnecessary "
                "for stating the operator."
            ),
            (
                "Expanding all subset class averages explicitly still uses "
                "2^k terms and is invalid at growing width."
            ),
            (
                "Finite condition number controls relative spectrum only; it "
                "does not remove absolute block-encoding normalization."
            ),
            (
                "The natural character-ratio concentration theorem validates "
                "the envelope but does not lower-bound non-LCU measurements."
            ),
        ],
    )


def write_average_frame_block_encoding_report(
    output_path: Path = REPORT_PATH,
    *,
    n: int = 5,
    transposition_count: int = 2,
    copy_count: int = 3,
    scaling_n_values: tuple[int, ...] = (8, 16, 32, 64),
    write_registry: bool = True,
    registry_experiment_id: str = DEFAULT_EXPERIMENT_ID,
    registry_candidate_id: str = DEFAULT_CANDIDATE_ID,
    registry_result_id: str | None = None,
) -> dict[str, object]:
    payload = asdict(
        build_average_frame_block_encoding_report(
            n=n,
            transposition_count=transposition_count,
            copy_count=copy_count,
            scaling_n_values=scaling_n_values,
        )
    )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    if write_registry:
        upsert_negative_result(
            NegativeResultRecord(
                id="NEG-COSET-PGM-DIRECT-PROJECTED-LCU-NORMALIZATION",
                source=str(output_path),
                claim=(
                    "The compact average-frame subset identity directly yields "
                    "a polynomial growing-width PGM circuit."
                ),
                reason_invalid=(
                    "The direct projected LCU has exponentially small average "
                    "spectral scale at k=Theta(n log n) under the stated hard-"
                    "sector character-ratio envelope. Explicit subset expansion "
                    "also has 2^k terms."
                ),
                lesson=(
                    "Search a representation-specific spectral amplifier, "
                    "different frame factorization, or direct covariant "
                    "measurement that avoids generic frame normalization."
                ),
                applies_to=[
                    registry_candidate_id,
                    registry_experiment_id,
                    "PO-MEASUREMENT",
                    "PO-COMPLEXITY",
                    "PO-SUCCESS",
                ],
                evidence=payload["headline_metrics"],
            )
        )
        result_id = (
            registry_result_id
            or f"RESULT-{registry_experiment_id}-COSET"
        )
        upsert_experiment_result(
            ExperimentResultRecord(
                id=result_id,
                experiment_id=registry_experiment_id,
                candidate_id=registry_candidate_id,
                created_at=str(payload["created_at"]),
                status=str(payload["status"]),
                summary=str(payload["summary"]),
                metrics=dict(payload["headline_metrics"]),
                falsifiers_triggered=list(payload["falsifiers_triggered"]),
                artifacts={
                    "coset_pgm_average_frame_block_encoding": str(output_path)
                },
            )
        )
    return payload


if __name__ == "__main__":
    report = write_average_frame_block_encoding_report()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))

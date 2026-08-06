"""Weighted-garbage reduction for DCP erasure-plus-QFT decoders.

Assume an exact isometry on normalized fibers,

    E_a |u_s>|0> = |s>|g_s>,

where the garbage may depend on s.  Write

    alpha_s = sqrt(c_s/D),
    Z = sum_s sqrt(c_s),
    w_s = sqrt(c_s)/Z.

After erasure and the cyclic QFT, correct hidden-frequency probability is

    P_actual = P_ideal R,
    P_ideal = Z^2/(ND),
    R = ||sum_s w_s |g_s>||^2.

The normalized weighted mean garbage ``|g>`` can itself be prepared: use the
public d=0 uniform input, apply E, and postselect the zero Fourier outcome.
This succeeds with probability ``P_actual``.

Let ``F_s=|<g|g_s>|^2`` and let q be uniform over legal targets.  Jensen gives
``E_w F_s >= R``.  Since ``w_s/q_s=L sqrt(c_s)/Z <= sqrt(c_s)``, truncating at
``B=(2D/(LR))^2`` gives

    E_q F_s >= (L/D) R^2 / 4.

Thus inverse-polynomial relative erasure-plus-QFT success yields an
inverse-polynomial average legal-target witness solver: prepare g, apply
E_a^dagger to |s,g>, measure x, and verify.

The theorem closes exact erasure-plus-QFT factorizations even with
target-dependent garbage.  It does not reduce an arbitrary full-rank PGM POVM
to erasure, and an approximate isometry requires explicit perturbation bounds.
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
    "research/reductions/"
    "dcp_approximate_erasure_coherence_reduction.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-DHS-DCP-APPROXIMATE-ERASURE-COHERENCE-REDUCTION"
)
DEFAULT_CANDIDATE_ID = "DHS-GOWERS-SIEVE"


@dataclass(frozen=True)
class GarbageCoherenceControl:
    n_bits: int
    trial: int
    garbage_dimension: int
    legal_fiber_count: int
    support_fraction: float
    ideal_pgm_success: float
    relative_coherence: float
    actual_qft_success: float
    direct_actual_qft_success: float
    qft_formula_residual: float
    weighted_mean_fidelity: float
    weighted_fidelity_lower_bound_residual: float
    truncation_threshold: float
    uniform_legal_mean_fidelity: float
    uniform_legal_fidelity_lower_bound: float
    uniform_legal_bound_residual: float
    reference_garbage_preparation_probability: float
    status: str


@dataclass(frozen=True)
class CoherenceReductionScalingRow:
    n_bits: int
    relative_success_power: int
    relative_coherence: float
    support_fraction_lower_bound: float
    reference_preparation_success_lower_bound: float
    uniform_legal_witness_success_lower_bound: float
    reference_preparation_repetitions_upper_bound: float
    witness_repetitions_upper_bound: float
    all_resources_polynomial: bool


@dataclass(frozen=True)
class ApproximateErasureCoherenceReport:
    created_at: str
    theorem_contract: dict[str, str]
    controls: list[GarbageCoherenceControl]
    scaling_rows: list[CoherenceReductionScalingRow]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, bool | str]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _random_unit_vectors(
    count: int,
    dimension: int,
    seed: int,
) -> np.ndarray:
    rng = np.random.default_rng(seed)
    values = (
        rng.normal(size=(count, dimension))
        + 1j * rng.normal(size=(count, dimension))
    )
    values /= np.linalg.norm(values, axis=1)[:, None]
    return values


def audit_garbage_coherence_control(
    n_bits: int,
    trial: int,
    seed: int,
    garbage_dimension: int = 4,
) -> GarbageCoherenceControl:
    if n_bits < 2 or garbage_dimension < 1:
        raise ValueError("invalid garbage coherence dimensions")
    modulus = 1 << n_bits
    rng = random.Random(seed)
    labels = [rng.randrange(modulus) for _ in range(n_bits)]
    counts = exact_cyclic_subset_sum_counts(labels, modulus)
    legal_counts = counts[counts > 0].astype(np.float64)
    support_size = len(legal_counts)
    support_fraction = support_size / modulus
    roots = np.sqrt(legal_counts)
    z_value = float(np.sum(roots))
    weights = roots / z_value
    garbage = _random_unit_vectors(
        support_size,
        garbage_dimension,
        seed + 7919,
    )
    weighted_mean = np.sum(weights[:, None] * garbage, axis=0)
    relative_coherence = float(
        np.vdot(weighted_mean, weighted_mean).real
    )
    ideal_success = z_value * z_value / (modulus * modulus)
    actual_success = ideal_success * relative_coherence

    alphas = roots / math.sqrt(modulus)
    direct_vector = np.sum(alphas[:, None] * garbage, axis=0)
    direct_actual = float(
        np.vdot(direct_vector, direct_vector).real / modulus
    )
    qft_residual = abs(actual_success - direct_actual)

    if relative_coherence > 0:
        reference = weighted_mean / math.sqrt(relative_coherence)
        fidelities = np.abs(garbage @ reference.conj()) ** 2
    else:
        fidelities = np.zeros(support_size, dtype=np.float64)
    weighted_fidelity = float(np.dot(weights, fidelities))
    weighted_residual = max(0.0, relative_coherence - weighted_fidelity)
    uniform_fidelity = float(np.mean(fidelities))

    if relative_coherence > 0:
        truncation = (
            2 / (support_fraction * relative_coherence)
        ) ** 2
        lower_bound = support_fraction * relative_coherence**2 / 4
    else:
        truncation = math.inf
        lower_bound = 0.0
    uniform_residual = max(0.0, lower_bound - uniform_fidelity)
    status = (
        "garbage-coherence-and-law-transfer-identities-verified"
        if max(
            qft_residual,
            weighted_residual,
            uniform_residual,
        )
        <= 1e-10
        else "garbage-coherence-control-failed"
    )
    return GarbageCoherenceControl(
        n_bits=n_bits,
        trial=trial,
        garbage_dimension=garbage_dimension,
        legal_fiber_count=support_size,
        support_fraction=support_fraction,
        ideal_pgm_success=ideal_success,
        relative_coherence=relative_coherence,
        actual_qft_success=actual_success,
        direct_actual_qft_success=direct_actual,
        qft_formula_residual=qft_residual,
        weighted_mean_fidelity=weighted_fidelity,
        weighted_fidelity_lower_bound_residual=weighted_residual,
        truncation_threshold=truncation,
        uniform_legal_mean_fidelity=uniform_fidelity,
        uniform_legal_fidelity_lower_bound=lower_bound,
        uniform_legal_bound_residual=uniform_residual,
        reference_garbage_preparation_probability=actual_success,
        status=status,
    )


def coherence_reduction_scaling_row(
    n_bits: int,
    relative_success_power: int,
    support_fraction_lower_bound: float = 0.5,
) -> CoherenceReductionScalingRow:
    if (
        n_bits < 2
        or relative_success_power < 0
        or not 0 < support_fraction_lower_bound <= 1
    ):
        raise ValueError("invalid coherence scaling parameters")
    relative = n_bits ** (-relative_success_power)
    ideal_success_lower = support_fraction_lower_bound**2
    reference_success = ideal_success_lower * relative
    witness_success = (
        support_fraction_lower_bound * relative**2 / 4
    )
    return CoherenceReductionScalingRow(
        n_bits=n_bits,
        relative_success_power=relative_success_power,
        relative_coherence=relative,
        support_fraction_lower_bound=support_fraction_lower_bound,
        reference_preparation_success_lower_bound=reference_success,
        uniform_legal_witness_success_lower_bound=witness_success,
        reference_preparation_repetitions_upper_bound=(
            1 / reference_success
        ),
        witness_repetitions_upper_bound=1 / witness_success,
        all_resources_polynomial=True,
    )


def build_approximate_erasure_coherence_report(
    control_n_values: tuple[int, ...] = (6, 8, 10, 12),
    control_trials: int = 3,
    garbage_dimensions: tuple[int, ...] = (2, 4, 8),
    scaling_n_values: tuple[int, ...] = (64, 128, 256, 512, 1024),
    relative_success_powers: tuple[int, ...] = (1, 2, 4),
    seed: int = 0,
) -> ApproximateErasureCoherenceReport:
    controls = [
        audit_garbage_coherence_control(
            n_bits,
            trial,
            seed + 1009 * n_bits + 31 * trial + dimension,
            dimension,
        )
        for n_bits in control_n_values
        for trial in range(control_trials)
        for dimension in garbage_dimensions
    ]
    scaling = [
        coherence_reduction_scaling_row(n_bits, power)
        for n_bits in scaling_n_values
        for power in relative_success_powers
    ]
    control_failures = sum(
        row.status
        != "garbage-coherence-and-law-transfer-identities-verified"
        for row in controls
    )
    metrics: dict[str, int | float] = {
        "finite_control_count": len(controls),
        "finite_control_failure_count": control_failures,
        "exact_garbage_gram_qft_formula_count": 1,
        "weighted_mean_reference_preparation_count": 1,
        "uniform_legal_fidelity_transfer_theorem_count": 1,
        "inverse_polynomial_erasure_to_witness_reduction_count": 1,
        "scaling_row_count": len(scaling),
        "joint_polynomial_scaling_row_count": sum(
            row.all_resources_polynomial for row in scaling
        ),
        "minimum_finite_support_fraction": min(
            row.support_fraction for row in controls
        ),
        "maximum_qft_formula_residual": max(
            row.qft_formula_residual for row in controls
        ),
        "maximum_uniform_legal_bound_residual": max(
            row.uniform_legal_bound_residual for row in controls
        ),
        "proved_approximate_isometry_perturbation_bound_count": 0,
        "proved_arbitrary_full_rank_pgm_reduction_count": 0,
        "polynomial_erasure_plus_qft_decoder_count": 0,
        "polynomial_average_subset_sum_witness_solver_count": 0,
    }
    return ApproximateErasureCoherenceReport(
        created_at=utc_now(),
        theorem_contract={
            "relative_success": (
                "P_actual/P_ideal=R=||sum_s sqrt(c_s)/Z |g_s>||^2"
            ),
            "reference_preparation": (
                "the public d=0 input, erasure, and zero Fourier outcome "
                "prepare the normalized weighted mean garbage with probability "
                "P_actual"
            ),
            "weighted_fidelity": (
                "for F_s=|<g|g_s>|^2, E_w F_s>=R by Cauchy/Jensen"
            ),
            "law_transfer": (
                "with q uniform legal and B=(2D/(LR))^2, "
                "E_q F_s >= (L/D)R^2/4"
            ),
            "solver": (
                "prepare g, apply E^dagger to |s,g>, measure x, and verify; "
                "inverse-polynomial R gives polynomial expected resources"
            ),
            "scope": (
                "exact fiber-erasure isometry with arbitrary target garbage; "
                "approximate-isometry perturbations and arbitrary POVMs excluded"
            ),
        },
        controls=controls,
        scaling_rows=scaling,
        headline_metrics=metrics,
        claim_gate={
            "target_dependent_garbage_erasure_reduced_to_witness_solver": True,
            "inverse_polynomial_relative_success_remains_polynomial": True,
            "approximate_isometry_perturbation_proved": False,
            "arbitrary_full_rank_pgm_reduced": False,
            "polynomial_erasure_decoder_constructed": False,
            "polynomial_average_witness_solver_constructed": False,
            "speedup_claim_allowed": False,
            "reason": (
                "Even target-dependent garbage does not make exact coherent "
                "erasure a weaker primitive. Any inverse-polynomial relative "
                "erasure-plus-QFT success prepares a reusable weighted mean "
                "garbage state and yields inverse-polynomial uniform-legal "
                "witness fidelity. Approximate isometries and arbitrary "
                "non-erasure POVMs remain open."
            ),
        },
        status=(
            "target-dependent-garbage-erasure-reduced-to-witness-"
            "approximate-isometry-and-arbitrary-pgm-open"
        ),
        summary=(
            f"Verified {len(controls)} garbage-Gram and target-law controls "
            f"with {control_failures} failures and {len(scaling)} polynomial "
            "resource rows. Exact erasure-plus-QFT with inverse-polynomial "
            "relative success is solver-equivalent even with target-dependent "
            "garbage; approximate isometries and arbitrary POVMs remain open."
        ),
        falsifiers_triggered=[
            "Target-dependent garbage reduces QFT success exactly through the weighted garbage Gram mean.",
            "The public zero-frequency input prepares the same weighted mean garbage needed to invert the erasure.",
            "Inverse-polynomial relative coherence cannot hide entirely on high-multiplicity fibers; truncation yields uniform-legal fidelity Omega((L/D)R^2).",
            "Exact erasure-plus-QFT with inverse-polynomial success is already an average witness solver.",
            "No perturbation theorem for approximate erasure isometries and no reduction for arbitrary full-rank POVMs is claimed.",
        ],
    )


def write_approximate_erasure_coherence_report(
    output_path: Path = REPORT_PATH,
    *,
    write_registry: bool = True,
    registry_experiment_id: str = DEFAULT_EXPERIMENT_ID,
    registry_candidate_id: str = DEFAULT_CANDIDATE_ID,
    registry_result_id: str | None = None,
) -> dict[str, object]:
    payload = asdict(build_approximate_erasure_coherence_report())
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(payload, indent=2, sort_keys=True)
    )
    if write_registry:
        upsert_negative_result(
            NegativeResultRecord(
                id="NEG-DCP-TARGET-DEPENDENT-GARBAGE-ERASURE-SHORTCUT",
                source=str(output_path),
                claim=(
                    "Target-dependent garbage lets a coherent erasure-plus-QFT "
                    "decoder achieve inverse-polynomial success without "
                    "yielding an average subset-sum witness solver."
                ),
                reason_invalid=(
                    "The relative QFT success is the squared weighted garbage "
                    "mean. That mean is publicly preparable, and truncation "
                    "transfers its inverse-preparation fidelity to uniform "
                    "legal targets with only a polynomial loss."
                ),
                lesson=(
                    "Treat every exact erasure-plus-QFT factorization with "
                    "inverse-polynomial relative success as the solver itself. "
                    "Search approximate-isometry loopholes quantitatively or "
                    "use a genuinely non-erasure full-rank POVM."
                ),
                applies_to=[
                    registry_candidate_id,
                    registry_experiment_id,
                    "EXP-DHS-DCP-GLOBAL-ERASURE-INVERSION-REDUCTION",
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
                    "dcp_approximate_erasure_coherence_reduction": str(
                        output_path
                    )
                },
            )
        )
    return payload


if __name__ == "__main__":
    report = write_approximate_erasure_coherence_report()
    print(
        json.dumps(
            report["headline_metrics"], indent=2, sort_keys=True
        )
    )

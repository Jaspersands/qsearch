"""Critical point energy does not determine operational distinguishability.

The natural carrier-traced point quotient has normalized Hilbert--Schmidt
energy

    S = D ||rho_j-B||_2^2,

where ``D=|S_n|2^k`` is the retained-register dimension and
``B=n^-1 sum_j rho_j``.  The copy-threshold theorem proves ``S>=n-1-o(1)``
at ``k=ceil(2 log_2(n!))``.  This module proves that this scalar fact alone
has no operational content.

For every ``D`` divisible by ``n`` there are two commuting, point-covariant
ensembles with exactly the same critical energy ``S=n-1``:

``flat partition``
    Split the ``D`` basis outcomes into ``n`` disjoint blocks and make
    ``rho_j`` uniform on block ``j``.  The average is ``I/D`` and the states
    are perfectly distinguishable.

``spiky simplex``
    On an ``n``-dimensional subspace put ``B=I/n`` and

        rho_j = B + a(|j><j|-I/n),    a=sqrt(n/D).

    Embed this subspace in dimension ``D``.  This ensemble also has
    ``D||rho_j-B||_2^2=n-1``, but its optimal success is only

        1/n + (n-1)/sqrt(nD).

At the natural critical width ``D=n! 2^ceil(2log_2(n!))`` the excess in the
second family is factorially small.  Thus equal critical energy is compatible
with either perfect recovery or negligible advantage.

The correct PGM scalar is relative, not ambient.  For any uniform ensemble,
write ``Delta_j=rho_j-B`` and use the Moore--Penrose inverse on ``supp(B)``.
The pretty-good measurement obeys the exact identity

    p_PGM = 1/n + n^-2 sum_j
      Tr(B^-1/2 Delta_j B^-1/2 Delta_j).                 (1)

For a covariant ensemble the sum has ``n`` equal terms.  In the two examples
the relative collision term is respectively ``n-1`` and ``n(n-1)/D``.
Equation (1), or the stronger optimal measurement, separates cases that
ambient Hilbert--Schmidt energy cannot.

This is a falsifier for an inference, not a no-go theorem for the natural
wreath ensemble.  The live obligation is to control its signal-weighted
relative spectrum (equivalently its child-star relative collision), then
compile the corresponding harmonic measurement.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import numpy as np

from research_registry import utc_now


REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_point_critical_energy_separation.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-POINT-CRITICAL-ENERGY-SEPARATION"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


@dataclass(frozen=True)
class ClassicalPointEnsembleMetrics:
    family: str
    point_count: int
    ambient_dimension: int
    average_support_rank: int
    normalized_average_top_eigenvalue: float
    normalized_hilbert_schmidt_energy: float
    maximum_energy_deviation: float
    average_relative_collision: float
    pgm_success_probability: float
    optimal_success_probability: float
    optimal_success_excess: float


@dataclass(frozen=True)
class CriticalEnergySeparationControl:
    n: int
    ambient_dimension: int
    common_normalized_energy: float
    normalized_energy_residual: float
    flat_relative_collision: float
    spiky_relative_collision: float
    flat_optimal_success: float
    spiky_optimal_success: float
    predicted_spiky_optimal_success: float
    spiky_success_formula_residual: float
    flat_perfectly_distinguishable: bool
    spiky_excess_smaller_than_inverse_dimension_quarter: bool
    same_energy_opposite_operational_behavior_verified: bool
    status: str


@dataclass(frozen=True)
class CriticalEnergyScalingRecord:
    n: int
    hidden_label_count_decimal: str
    critical_copy_count: int
    retained_dimension_decimal: str
    retained_dimension_log2: float
    common_normalized_energy: float
    flat_normalized_average_top_eigenvalue: float
    spiky_normalized_average_top_eigenvalue_log2: float
    flat_relative_collision: float
    spiky_relative_collision_log2: float
    flat_optimal_success: float
    spiky_optimal_excess: float
    spiky_optimal_excess_log2: float
    spiky_excess_superpolynomially_small: bool
    natural_relative_collision_proved: bool
    natural_harmonic_measurement_compiled: bool
    status: str


@dataclass(frozen=True)
class CriticalEnergySeparationTheorem:
    pgm_relative_collision_identity: str
    flat_family: str
    spiky_family: str
    equal_energy: str
    operational_separation: str
    natural_family_boundary: str
    theorem_verified: bool
    status: str


@dataclass(frozen=True)
class CriticalEnergySeparationReport:
    created_at: str
    theorem_contract: dict[str, Any]
    theorem: CriticalEnergySeparationTheorem
    finite_controls: list[CriticalEnergySeparationControl]
    scaling_records: list[CriticalEnergyScalingRecord]
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _exp2(log2_value: float) -> float:
    if log2_value < -1074.0:
        return 0.0
    if log2_value > 1023.0:
        return math.inf
    return math.exp2(log2_value)


def critical_register_parameters(n: int) -> tuple[int, int, int, float]:
    if n < 2:
        raise ValueError("n must be at least two")
    hidden_count = math.factorial(n)
    log2_hidden = math.lgamma(n + 1) / math.log(2.0)
    copies = math.ceil(2.0 * log2_hidden)
    dimension = hidden_count * (1 << copies)
    return hidden_count, copies, dimension, log2_hidden + copies


def flat_partition_probabilities(n: int, dimension: int) -> np.ndarray:
    if n < 2 or dimension < n or dimension % n:
        raise ValueError("dimension must be a positive multiple of n")
    block = dimension // n
    probabilities = np.zeros((n, dimension), dtype=float)
    for point in range(n):
        probabilities[point, point * block : (point + 1) * block] = 1.0 / block
    return probabilities


def spiky_simplex_probabilities(n: int, dimension: int) -> np.ndarray:
    if n < 2 or dimension < n:
        raise ValueError("dimension must be at least n")
    amplitude = math.sqrt(n / dimension)
    probabilities = np.zeros((n, dimension), dtype=float)
    probabilities[:, :n] = (1.0 - amplitude) / n
    for point in range(n):
        probabilities[point, point] += amplitude
    return probabilities


def classical_point_ensemble_metrics(
    probabilities: np.ndarray,
    *,
    family: str,
    tolerance: float = 1e-12,
) -> ClassicalPointEnsembleMetrics:
    probabilities = np.asarray(probabilities, dtype=float)
    if probabilities.ndim != 2 or probabilities.shape[0] < 2:
        raise ValueError("probabilities must be a point-by-outcome matrix")
    if np.min(probabilities) < -tolerance:
        raise ValueError("probabilities must be nonnegative")
    row_sums = np.sum(probabilities, axis=1)
    if np.max(np.abs(row_sums - 1.0)) > 100 * tolerance:
        raise ValueError("each point distribution must have unit mass")

    count, dimension = probabilities.shape
    average = np.mean(probabilities, axis=0)
    centered = probabilities - average
    energies = dimension * np.sum(centered * centered, axis=1)
    positive = average > tolerance
    relative = np.sum(
        centered[:, positive] ** 2 / average[positive],
        axis=1,
    )
    pgm = 1.0 / count + float(np.mean(relative)) / count
    optimal = float(np.sum(np.max(probabilities, axis=0)) / count)
    return ClassicalPointEnsembleMetrics(
        family=family,
        point_count=count,
        ambient_dimension=dimension,
        average_support_rank=int(np.count_nonzero(positive)),
        normalized_average_top_eigenvalue=dimension * float(np.max(average)),
        normalized_hilbert_schmidt_energy=float(np.mean(energies)),
        maximum_energy_deviation=float(np.max(np.abs(energies - np.mean(energies)))),
        average_relative_collision=float(np.mean(relative)),
        pgm_success_probability=pgm,
        optimal_success_probability=optimal,
        optimal_success_excess=optimal - 1.0 / count,
    )


def audit_critical_energy_separation(
    n: int,
    dimension: int,
    *,
    tolerance: float = 1e-10,
) -> CriticalEnergySeparationControl:
    flat = classical_point_ensemble_metrics(
        flat_partition_probabilities(n, dimension),
        family="flat-partition",
    )
    spiky = classical_point_ensemble_metrics(
        spiky_simplex_probabilities(n, dimension),
        family="spiky-simplex",
    )
    expected_energy = float(n - 1)
    expected_spiky = 1.0 / n + (n - 1) / math.sqrt(n * dimension)
    energy_residual = max(
        abs(flat.normalized_hilbert_schmidt_energy - expected_energy),
        abs(spiky.normalized_hilbert_schmidt_energy - expected_energy),
        flat.maximum_energy_deviation,
        spiky.maximum_energy_deviation,
    )
    success_residual = abs(spiky.optimal_success_probability - expected_spiky)
    perfect = abs(flat.optimal_success_probability - 1.0) <= 100 * tolerance
    small = spiky.optimal_success_excess < dimension ** -0.25
    verified = bool(
        energy_residual <= 100 * tolerance
        and success_residual <= 100 * tolerance
        and perfect
        and small
        and abs(flat.average_relative_collision - (n - 1)) <= 100 * tolerance
        and abs(
            spiky.average_relative_collision - n * (n - 1) / dimension
        )
        <= 100 * tolerance
    )
    return CriticalEnergySeparationControl(
        n=n,
        ambient_dimension=dimension,
        common_normalized_energy=expected_energy,
        normalized_energy_residual=energy_residual,
        flat_relative_collision=flat.average_relative_collision,
        spiky_relative_collision=spiky.average_relative_collision,
        flat_optimal_success=flat.optimal_success_probability,
        spiky_optimal_success=spiky.optimal_success_probability,
        predicted_spiky_optimal_success=expected_spiky,
        spiky_success_formula_residual=success_residual,
        flat_perfectly_distinguishable=perfect,
        spiky_excess_smaller_than_inverse_dimension_quarter=small,
        same_energy_opposite_operational_behavior_verified=verified,
        status=(
            "same-critical-energy-perfect-versus-negligible-success"
            if verified
            else "critical-energy-separation-validation-failure"
        ),
    )


def critical_energy_scaling_record(n: int) -> CriticalEnergyScalingRecord:
    hidden_count, copies, dimension, log2_dimension = critical_register_parameters(n)
    spiky_excess_log2 = (
        math.log2(n - 1) - 0.5 * (math.log2(n) + log2_dimension)
    )
    spiky_collision_log2 = (
        math.log2(n) + math.log2(n - 1) - log2_dimension
    )
    return CriticalEnergyScalingRecord(
        n=n,
        hidden_label_count_decimal=str(hidden_count),
        critical_copy_count=copies,
        retained_dimension_decimal=str(dimension),
        retained_dimension_log2=log2_dimension,
        common_normalized_energy=float(n - 1),
        flat_normalized_average_top_eigenvalue=1.0,
        spiky_normalized_average_top_eigenvalue_log2=(
            log2_dimension - math.log2(n)
        ),
        flat_relative_collision=float(n - 1),
        spiky_relative_collision_log2=spiky_collision_log2,
        flat_optimal_success=1.0,
        spiky_optimal_excess=_exp2(spiky_excess_log2),
        spiky_optimal_excess_log2=spiky_excess_log2,
        spiky_excess_superpolynomially_small=(
            spiky_excess_log2 < -math.log2(n) ** 2
        ),
        natural_relative_collision_proved=False,
        natural_harmonic_measurement_compiled=False,
        status="critical-energy-underdetermined-relative-spectrum-required",
    )


def build_critical_energy_separation_report() -> CriticalEnergySeparationReport:
    controls = [
        audit_critical_energy_separation(3, critical_register_parameters(3)[2]),
        audit_critical_energy_separation(4, critical_register_parameters(4)[2]),
    ]
    scaling = [
        critical_energy_scaling_record(n)
        for n in (5, 8, 16, 32, 64, 128, 256, 512)
    ]
    failures = sum(
        not row.same_energy_opposite_operational_behavior_verified
        for row in controls
    )
    verified = failures == 0
    theorem = CriticalEnergySeparationTheorem(
        pgm_relative_collision_identity=(
            "p_PGM=1/n+n^-2 sum_j Tr(B^-1/2 Delta_j B^-1/2 Delta_j)."
        ),
        flat_family=(
            "Uniform distributions on n disjoint blocks have B=I/D, S=n-1, "
            "relative collision n-1, and perfect success."
        ),
        spiky_family=(
            "rho_j=I_n/n+sqrt(n/D)(|j><j|-I_n/n), embedded in D dimensions."
        ),
        equal_energy="Both families have exactly D||rho_j-B||_2^2=n-1.",
        operational_separation=(
            "The spiky family has optimal success 1/n+(n-1)/sqrt(nD), while "
            "the flat family has success one."
        ),
        natural_family_boundary=(
            "No conclusion about the natural wreath point ensemble follows until "
            "its signal-weighted relative spectrum is bounded."
        ),
        theorem_verified=verified,
        status=(
            "critical-energy-only-inference-falsified-relative-spectrum-open"
            if verified
            else "critical-energy-separation-validation-failure"
        ),
    )
    return CriticalEnergySeparationReport(
        created_at=utc_now(),
        theorem_contract={
            "scope": "uniform point ensembles, including commuting covariant counterexamples",
            "ambient_dimension": "D=n! 2^ceil(2log2(n!)) for natural-width scaling",
            "fixed_scalar": "D||rho_j-B||_2^2=n-1",
            "decisive_relative_scalar": (
                "Tr(B^-1/2 Delta_j B^-1/2 Delta_j), not ambient energy"
            ),
            "claim_boundary": (
                "counterexample to energy-only inference, not a natural-family decoder no-go"
            ),
        },
        theorem=theorem,
        finite_controls=controls,
        scaling_records=scaling,
        proof_obligations=[
            {
                "id": "PO-POINT-CRITICAL-RELATIVE-COLLISION",
                "statement": (
                    "Bound the natural critical average of "
                    "Tr(B^-1/2 Delta_j B^-1/2 Delta_j) on typical public labels."
                ),
                "resolved": False,
            },
            {
                "id": "PO-POINT-CRITICAL-SIGNAL-WEIGHTED-SPECTRUM",
                "statement": (
                    "Locate critical Delta mass across the eigenvalue windows of B; "
                    "a global top-eigenvalue or purity bound is insufficient."
                ),
                "resolved": False,
            },
            {
                "id": "PO-POINT-CRITICAL-HARMONIC-NAIMARK",
                "statement": (
                    "Compile the information-carrying child-star relative effect "
                    "without factorial scalar amplification."
                ),
                "resolved": False,
            },
        ],
        adversarial_audit=[
            {
                "challenge": "S=n-1 forces inverse-polynomial point advantage.",
                "answer": (
                    "False. The spiky simplex has that exact S but only "
                    "(n-1)/sqrt(nD) optimal excess."
                ),
                "resolved": True,
            },
            {
                "challenge": "S=n-1 is necessarily operationally useless.",
                "answer": (
                    "False. The flat partition ensemble has the same S and perfect success."
                ),
                "resolved": True,
            },
            {
                "challenge": "The PGM is determined by ambient Hilbert--Schmidt energy.",
                "answer": (
                    "False. Its exact excess is a relative collision weighted by B^-1/2."
                ),
                "resolved": True,
            },
            {
                "challenge": "The counterexample rules out the natural point route.",
                "answer": (
                    "Too strong. It rules out only an inference from the existing "
                    "energy theorem; the natural relative operator remains open."
                ),
                "resolved": True,
            },
        ],
        headline_metrics={
            "exact_pgm_relative_collision_identity_count": int(verified),
            "same_energy_operational_separation_theorem_count": int(verified),
            "finite_control_count": len(controls),
            "finite_control_failure_count": failures,
            "perfect_success_same_energy_family_count": int(verified),
            "factorially_small_success_same_energy_family_count": int(verified),
            "tail_n": scaling[-1].n,
            "tail_spiky_optimal_excess_log2": scaling[-1].spiky_optimal_excess_log2,
            "natural_relative_collision_theorem_count": 0,
            "natural_harmonic_measurement_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "critical_ambient_energy_determines_point_advantage": False,
            "critical_energy_alone_supports_algorithmic_progress": False,
            "relative_collision_is_correct_pgm_scalar": verified,
            "same_energy_allows_perfect_or_negligible_optimal_success": verified,
            "natural_critical_relative_collision_proved": False,
            "natural_signal_weighted_spectral_window_proved": False,
            "critical_harmonic_naimark_compiled": False,
            "full_hidden_permutation_decoder_constructed": False,
            "classical_separation_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The factor-two ambient-energy phase transition is operationally "
                "underdetermined. Only a natural-family relative-spectrum theorem "
                "can distinguish useful flat signal from a spiky false positive."
            ),
        },
        status=theorem.status,
        summary=(
            "Constructed exact covariant commuting ensembles with identical critical "
            "point energy and opposite distinguishability, and isolated relative "
            "collision as the PGM quantity the natural theorem must control."
        ),
        falsifiers_triggered=[
            "Critical normalized Hilbert--Schmidt energy cannot be promoted to point advantage.",
            "Critical normalized Hilbert--Schmidt energy cannot be promoted to a no-go either.",
            "Global average-state purity or top norm is not a substitute for signal-weighted relative spectrum.",
            "Future critical work must evaluate relative child-star collision before attempting a decoder claim.",
        ],
    )


def write_critical_energy_separation_report(
    path: Path = REPORT_PATH,
    **_: Any,
) -> dict[str, Any]:
    payload = asdict(build_critical_energy_separation_report())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    return payload


if __name__ == "__main__":
    report = write_critical_energy_separation_report()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))

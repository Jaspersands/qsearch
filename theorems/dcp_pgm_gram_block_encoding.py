"""Exact Gram block encoding and normalization audit for the DCP PGM.

For public labels ``a in Z_N^m``, let

    c_s = |{x in {0,1}^m : <a,x> = s mod N}|,
    D = 2^m.

The clean DCP phase-state Gram operator is diagonalized by the cyclic Fourier
transform with eigenvalues ``N c_s / D``.  A reversible subset-sum circuit
immediately gives a projected block encoding of

    A = diag(c_s / D) = G / N

without an ``N``-entry table: prepare uniform ``x``, compute its subset sum,
and project on equality with ``s``.

This closes the vague "build a Gram block encoding" task, but exposes the real
normalization barrier.  A legal fiber of size ``c_s`` has preparation
amplitude ``sqrt(c_s/D)``.  Generic fiber amplification or inverse-square-root
resolution therefore costs ``sqrt(D/c_s)``.  Exact first and second moments
show that, conditioned on a random target being legal, all but an inverse
polynomial fraction of density-one inputs have only polynomial ``c_s``.  The
generic route is consequently exponential on almost all legal inputs.

The result is route-specific: it does not rule out a structured
preconditioner, collision walk, or another full-rank collective measurement.
"""

from __future__ import annotations

import json
import math
import random
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Sequence

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
    "research/phase_workbench/dcp_pgm_gram_block_encoding.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-DHS-DCP-PGM-GRAM-BLOCK-ENCODING"
)
DEFAULT_CANDIDATE_ID = "DHS-GOWERS-SIEVE"


@dataclass(frozen=True)
class GramBlockEncodingControl:
    n_bits: int
    register_count: int
    trial: int
    label_digest: str
    modulus: int
    assignment_count: int
    legal_fiber_count: int
    maximum_fiber_size: int
    projected_diagonal_residual: float
    gram_spectrum_residual: float
    projected_isometry_residual: float
    exact_count_normalization_verified: bool
    status: str


@dataclass(frozen=True)
class GramNormalizationScalingRow:
    n_bits: int
    register_count: int
    register_offset: int
    mean_fiber_size: float
    polynomial_fiber_cap_power: int
    polynomial_fiber_cap_log2: float
    legal_probability_lower_bound: float
    conditioned_high_fiber_probability_upper_bound: float
    gram_block_encoding_normalization_log2: int
    minimum_legal_scaled_eigenvalue_log2: int
    generic_fiber_amplification_log2_query_lower_bound: float
    polynomial_query_log2_threshold: float
    generic_fiber_amplification_superpolynomial: bool


@dataclass(frozen=True)
class DCPGramBlockEncodingReport:
    created_at: str
    operator_theorem: dict[str, str]
    circuit_contract: dict[str, object]
    controls: list[GramBlockEncodingControl]
    scaling_rows: list[GramNormalizationScalingRow]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, bool | str]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def subset_sums(
    labels: Sequence[int], modulus: int
) -> np.ndarray:
    sums = np.zeros(1, dtype=np.int64)
    for label in labels:
        sums = np.concatenate(
            (sums, (sums + int(label)) % modulus)
        )
    return sums


def projected_fiber_isometry(
    labels: Sequence[int], modulus: int
) -> tuple[np.ndarray, np.ndarray]:
    """Return W and the flag-one projector for the equality circuit."""

    sums = subset_sums(labels, modulus)
    assignment_count = len(sums)
    row_count = modulus * assignment_count * 2
    isometry = np.zeros(
        (row_count, modulus), dtype=np.float64
    )
    amplitude = 1 / math.sqrt(assignment_count)
    for target in range(modulus):
        for assignment, value in enumerate(sums):
            flag = int(value == target)
            row = (
                (target * assignment_count + assignment) * 2
                + flag
            )
            isometry[row, target] = amplitude
    projector = np.zeros(row_count, dtype=np.float64)
    projector[1::2] = 1.0
    return isometry, projector


def phase_state_gram(
    labels: Sequence[int], modulus: int
) -> np.ndarray:
    sums = subset_sums(labels, modulus)
    phases = np.exp(
        2j
        * np.pi
        * np.outer(sums, np.arange(modulus))
        / modulus
    )
    states = phases / math.sqrt(len(sums))
    return states.conj().T @ states


def _label_digest(labels: Sequence[int]) -> str:
    accumulator = 0xCBF29CE484222325
    for label in labels:
        accumulator ^= int(label)
        accumulator = (
            accumulator * 0x100000001B3
        ) & ((1 << 64) - 1)
    return f"{accumulator:016x}"


def audit_gram_control(
    n_bits: int,
    register_count: int,
    trial: int,
    seed: int,
) -> GramBlockEncodingControl:
    if n_bits < 2 or register_count < 1:
        raise ValueError("invalid DCP Gram control dimensions")
    modulus = 1 << n_bits
    rng = random.Random(seed)
    labels = [
        rng.randrange(modulus) for _ in range(register_count)
    ]
    counts = exact_cyclic_subset_sum_counts(labels, modulus)
    assignment_count = 1 << register_count
    isometry, projector = projected_fiber_isometry(
        labels, modulus
    )
    projected = (
        isometry.T
        @ (projector[:, None] * isometry)
    )
    expected_projected = np.diag(
        counts.astype(np.float64) / assignment_count
    )
    projected_residual = float(
        np.linalg.norm(projected - expected_projected)
    )
    isometry_residual = float(
        np.linalg.norm(
            isometry.T @ isometry - np.eye(modulus)
        )
    )

    gram = phase_state_gram(labels, modulus)
    observed_spectrum = np.sort(
        np.linalg.eigvalsh(
            (gram + gram.conj().T) / 2
        )
    )
    expected_spectrum = np.sort(
        modulus * counts.astype(np.float64) / assignment_count
    )
    gram_residual = float(
        np.max(
            np.abs(observed_spectrum - expected_spectrum)
        )
    )
    normalization_verified = (
        int(counts.sum()) == assignment_count
        and projected_residual < 1e-10
        and gram_residual < 1e-9
        and isometry_residual < 1e-10
    )
    return GramBlockEncodingControl(
        n_bits=n_bits,
        register_count=register_count,
        trial=trial,
        label_digest=_label_digest(labels),
        modulus=modulus,
        assignment_count=assignment_count,
        legal_fiber_count=int(np.count_nonzero(counts)),
        maximum_fiber_size=int(np.max(counts)),
        projected_diagonal_residual=projected_residual,
        gram_spectrum_residual=gram_residual,
        projected_isometry_residual=isometry_residual,
        exact_count_normalization_verified=normalization_verified,
        status=(
            "projected-gram-identity-verified"
            if normalization_verified
            else "projected-gram-control-failed"
        ),
    )


def normalization_scaling_row(
    n_bits: int,
    register_offset: int = 0,
    polynomial_fiber_cap_power: int = 4,
    polynomial_query_power: int = 8,
) -> GramNormalizationScalingRow:
    if n_bits < 2:
        raise ValueError("n_bits must be at least two")
    register_count = n_bits + register_offset
    if register_count < 1:
        raise ValueError("register count must be positive")
    if min(
        polynomial_fiber_cap_power,
        polynomial_query_power,
    ) < 0:
        raise ValueError("polynomial powers must be nonnegative")
    assignment_count = 1 << register_count
    modulus = 1 << n_bits
    mean = assignment_count / modulus
    second_moment = (
        mean
        + mean
        * mean
        * (1 - 1 / assignment_count)
    )
    legal_probability_lower_bound = (
        mean * mean / second_moment
    )
    cap_log2 = (
        polynomial_fiber_cap_power * math.log2(n_bits)
    )
    conditioned_high_upper = min(
        1.0,
        (
            1
            + mean * (1 - 1 / assignment_count)
        )
        / (n_bits**polynomial_fiber_cap_power),
    )
    amplification_log2 = max(
        0.0,
        0.5 * (register_count - cap_log2),
    )
    polynomial_threshold = (
        polynomial_query_power * math.log2(n_bits)
    )
    return GramNormalizationScalingRow(
        n_bits=n_bits,
        register_count=register_count,
        register_offset=register_offset,
        mean_fiber_size=mean,
        polynomial_fiber_cap_power=(
            polynomial_fiber_cap_power
        ),
        polynomial_fiber_cap_log2=cap_log2,
        legal_probability_lower_bound=(
            legal_probability_lower_bound
        ),
        conditioned_high_fiber_probability_upper_bound=(
            conditioned_high_upper
        ),
        gram_block_encoding_normalization_log2=n_bits,
        minimum_legal_scaled_eigenvalue_log2=-register_count,
        generic_fiber_amplification_log2_query_lower_bound=(
            amplification_log2
        ),
        polynomial_query_log2_threshold=polynomial_threshold,
        generic_fiber_amplification_superpolynomial=(
            amplification_log2 > polynomial_threshold
        ),
    )


def build_gram_block_encoding_report(
    control_n_values: tuple[int, ...] = (3, 4),
    control_trials: int = 2,
    scaling_n_values: tuple[int, ...] = (
        64,
        128,
        256,
        512,
        1024,
    ),
    register_offsets: tuple[int, ...] = (0, 2),
    seed: int = 0,
) -> DCPGramBlockEncodingReport:
    controls = [
        audit_gram_control(
            n_bits,
            n_bits,
            trial,
            seed + 1009 * n_bits + trial,
        )
        for n_bits in control_n_values
        for trial in range(control_trials)
    ]
    scaling_rows = [
        normalization_scaling_row(n_bits, offset)
        for n_bits in scaling_n_values
        for offset in register_offsets
    ]
    control_failures = sum(
        not control.exact_count_normalization_verified
        for control in controls
    )
    asymptotic_rows = sum(
        row.generic_fiber_amplification_superpolynomial
        for row in scaling_rows
    )
    metrics: dict[str, int | float] = {
        "finite_control_count": len(controls),
        "finite_control_failure_count": control_failures,
        "exact_projected_gram_identity_count": 1,
        "polynomial_projected_gram_block_encoding_count": 1,
        "gram_block_encoding_normalization_log2_slope": 1.0,
        "source_conditioned_low_fiber_theorem_count": 1,
        "scaling_row_count": len(scaling_rows),
        "maximum_n_bits": max(scaling_n_values),
        "generic_superpolynomial_fiber_amplification_row_count": (
            asymptotic_rows
        ),
        "minimum_tail_generic_amplification_log2_queries": min(
            row.generic_fiber_amplification_log2_query_lower_bound
            for row in scaling_rows
            if row.n_bits == max(scaling_n_values)
        ),
        "uniform_polynomial_gram_rescaling_count": 0,
        "uniform_polynomial_structured_preconditioner_count": 0,
        "polynomial_coherent_fiber_erasure_count": 0,
        "polynomial_pgm_circuit_count": 0,
        "proved_general_collective_measurement_lower_bound_count": 0,
    }
    return DCPGramBlockEncodingReport(
        created_at=utc_now(),
        operator_theorem={
            "fiber_count": (
                "c_s=#{x in {0,1}^m:<a,x>=s mod N}"
            ),
            "phase_gram_spectrum": (
                "QFT_N G QFT_N^*=diag(N*c_s/2^m)"
            ),
            "projected_encoding": (
                "<0|V^* Pi_equal V|0>=diag(c_s/2^m)=G/N"
            ),
            "first_moment": "E[c_s]=mu=2^m/N",
            "second_moment": (
                "E[c_s^2]=mu+mu^2(1-2^-m)"
            ),
            "legal_probability": (
                "Pr[c_s>0]>=mu/(1+mu(1-2^-m)) by Paley-Zygmund"
            ),
            "conditioned_tail": (
                "Pr[c_s>B|c_s>0]<=(1+mu(1-2^-m))/B"
            ),
        },
        circuit_contract={
            "prepare": (
                "Hadamards prepare uniform x; reversible modular addition "
                "computes <a,x>; an equality flag compares with s."
            ),
            "projected_block_encoding_cost": (
                "poly(n,m,log(1/epsilon)) gates and O(1) subset-sum "
                "compute/uncompute calls"
            ),
            "normalization": (
                "The polynomial circuit encodes G/N, not G. Legal singleton "
                "fibers have scaled eigenvalue 2^-m."
            ),
            "generic_fiber_erasure": (
                "Postselecting/amplifying equality for fiber s costs "
                "Theta(sqrt(2^m/c_s)) subset-sum calls."
            ),
            "scope_limit": (
                "The query charge applies to the direct projected-encoding, "
                "generic amplification, and generic inverse-square-root "
                "routes. It is not a lower bound against structured "
                "preconditioners or arbitrary collective measurements."
            ),
        },
        controls=controls,
        scaling_rows=scaling_rows,
        headline_metrics=metrics,
        claim_gate={
            "exact_gram_block_encoding_constructed": (
                control_failures == 0
            ),
            "block_encoding_has_polynomial_normalization_for_gram": False,
            "source_conditioned_polynomial_fiber_cap_proved": True,
            "generic_fiber_erasure_is_polynomial": False,
            "structured_preconditioner_constructed": False,
            "polynomial_pgm_circuit_constructed": False,
            "general_collective_measurement_lower_bound_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The exact projected encoding removes the N-entry table but "
                "encodes G/N. On all but inverse-polynomial legal-source mass, "
                "fibers are polynomially small and generic fiber amplification "
                "still costs 2^(Omega(n)). A structured rescaling mechanism "
                "remains open."
            ),
        },
        status=(
            "gram-block-encoding-exact-normalization-"
            "and-generic-fiber-erasure-exponential"
        ),
        summary=(
            f"Verified {len(controls)} projected Gram controls with "
            f"{control_failures} failures and instantiated "
            f"{len(scaling_rows)} source-conditioned scaling rows. "
            "The block encoding is polynomial, but its Gram normalization "
            "and direct fiber-erasure route retain exponential cost."
        ),
        falsifiers_triggered=[
            "An implicit projected block encoding alone does not remove the factor-N Gram normalization.",
            "Computing the subset sum in superposition does not coherently erase the subset identity.",
            "Generic equality postselection or amplitude amplification costs sqrt(2^m/c_s).",
            "Conditioned first/second moments put all but inverse-polynomial legal mass in polynomial-size fibers at density one.",
            "No lower bound against structured preconditioners, collision walks, or arbitrary full-rank measurements is claimed.",
        ],
    )


def write_gram_block_encoding_report(
    output_path: Path = REPORT_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = DEFAULT_EXPERIMENT_ID,
    registry_candidate_id: str = DEFAULT_CANDIDATE_ID,
    registry_result_id: str | None = None,
    control_n_values: tuple[int, ...] = (3, 4),
    control_trials: int = 2,
    scaling_n_values: tuple[int, ...] = (
        64,
        128,
        256,
        512,
        1024,
    ),
    register_offsets: tuple[int, ...] = (0, 2),
    seed: int = 0,
) -> dict[str, object]:
    payload = asdict(
        build_gram_block_encoding_report(
            control_n_values=control_n_values,
            control_trials=control_trials,
            scaling_n_values=scaling_n_values,
            register_offsets=register_offsets,
            seed=seed,
        )
    )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(payload, indent=2, sort_keys=True)
    )
    return payload


if __name__ == "__main__":
    report = write_gram_block_encoding_report()
    print(
        json.dumps(
            report["headline_metrics"], indent=2, sort_keys=True
        )
    )

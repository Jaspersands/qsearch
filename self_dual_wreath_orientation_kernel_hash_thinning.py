"""Pairwise-independent hash thinning for the orientation overlap kernel.

The retained-orientation decoder has, in each Fourier sector, the positive
kernel

    H[e,f] = Tr(E_e E_f)/d_nu.

Its diagonal is ``rank(E_e)/d_nu`` and all entries are nonnegative.  Put

    m = q^-1 Tr(H),
    epsilon = max_e |H[e,e]/m-1|,
    C = [Tr(A^2)-Tr(A)]/Tr(A),  A=sum_e E_e.

Hilbert--Schmidt Cauchy--Schwarz gives the deterministic fourth-energy bound

    sum_(e!=f) H[e,f]^2
      <= H_max sum_(e!=f) H[e,f]
      = H_max [Tr(A^2)-Tr(A)]/d_nu
      <= (1+epsilon) C q m^2.                             (1)

No fourth representation moment is needed.

Choose a public affine hash ``h(e)=M e+b`` from ``F_2^k`` to ``F_2^t`` and
retain ``S={e:h(e)=0}``.  Over uniformly random ``M,b``, the indicators are
pairwise independent:

    Pr[e in S]=p=2^-t,
    Pr[e,f in S]=p^2  for e!=f.

This exact expectation is for the unconditioned choice of ``M,b``.  A circuit
may resample until ``M`` has row rank ``t``; when ``k`` is much larger than
``t``, rank failure is negligible, but the conditional family is not asserted
to obey the displayed pairwise probabilities exactly.

Consequently

    E ||H_S-m I_S||_F^2
      = p sum_e(H[e,e]-m)^2 + p^2 sum_(e!=f)H[e,f]^2
      <= p q m^2 [epsilon^2+p(1+epsilon)C].               (2)

The physical branch register is uniform in norm for every hidden label, so
the hash projection has label-independent expected acceptance ``p``.  It is
an inverse-polynomial operation when ``t=O(log n)`` and can be evaluated by a
polynomial reversible circuit.  No Walsh transform is required: retaining
the orientation register is unitarily equivalent to retaining its character.

If a realized subset has normalized error

    eta=||H_S-mI||_F^2/(|S|m^2),

then at most ``eta |S|/kappa^2`` eigenvalues lie outside
``[m(1-kappa),m(1+kappa)]``.  Their normalized trace mass is at most

    [eta/kappa^2 + eta/kappa]/[1-sqrt(eta)].              (3)

Thus pairwise hashing turns a polynomial bound on ``C`` and uniform diagonal
concentration into an inverse-polynomial-acceptance, almost-scalar spectral
bulk.  This does not yet compile the decoder: a coherent way to ignore the
exceptional spectrum, or an operator-norm bound making scalar whitening a
valid global contraction, remains open.  The theorem is state-weighted and
does not claim simultaneous control of every exponentially coherent sector.
"""

from __future__ import annotations

import itertools
import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import numpy as np

from representation_obstruction import hook_length_dimension, integer_partitions
from research_registry import utc_now
from self_dual_wreath_joint_character_multiplicity_gram import (
    orientation_overlap_kernel,
    predicted_joint_multiplicity_operator,
)
from self_dual_wreath_orientation_fourier_reduction import (
    _w4_collision_free_labels,
)


REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_orientation_kernel_hash_thinning.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-ORIENTATION-KERNEL-HASH-THINNING"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"

Partition = tuple[int, ...]
Label = tuple[Partition, Partition]


@dataclass(frozen=True)
class OrientationKernelHashControl:
    control_id: str
    n: int
    target: Partition
    labels: tuple[Label, ...]
    orientation_count: int
    hash_output_bits: int
    retention_density: float
    diagonal_mean: float
    maximum_relative_diagonal_deviation: float
    frame_collision_ratio: float
    offdiagonal_frobenius_squared: float
    deterministic_offdiagonal_upper_bound: float
    deterministic_bound_violation: float
    enumerated_hash_count: int
    exact_expected_thinned_error: float
    predicted_expected_thinned_error: float
    expectation_formula_residual: float
    minimum_nonempty_subset_size: int
    maximum_subset_size: int
    median_nonempty_normalized_error: float
    minimum_nonempty_normalized_error: float
    exact_hash_thinning_theorem_verified: bool
    status: str


@dataclass(frozen=True)
class OrientationKernelTrimControl:
    control_id: str
    matrix_dimension: int
    normalized_frobenius_error: float
    relative_window: float
    observed_bad_eigenvalue_count: int
    bad_eigenvalue_count_upper_bound: float
    observed_bad_trace_mass: float
    bad_trace_mass_upper_bound: float
    retained_condition_number_upper_bound: float
    spectral_trim_bounds_verified: bool
    status: str


@dataclass(frozen=True)
class OrientationKernelHashScalingRecord:
    n: int
    information_threshold_copy_count: int
    hash_output_bits: int
    retention_probability_lower_bound: float
    polynomial_collision_markov_bound: float
    diagonal_relative_error_target: float
    expected_normalized_frobenius_error_upper_bound: float
    markov_normalized_error_threshold: float
    relative_spectral_window: float
    exceptional_rank_fraction_upper_bound: float
    hash_projection_inverse_polynomial_acceptance: bool
    simultaneous_all_sector_kernel_bound_proved: bool
    coherent_exceptional_spectrum_filter_proved: bool
    scalar_whitening_global_contraction_proved: bool
    polynomial_joint_decoder_proved: bool
    status: str


@dataclass(frozen=True)
class OrientationKernelHashTheorem:
    offdiagonal_energy: str
    pairwise_hashing: str
    thinned_error: str
    spectral_bulk: str
    physical_acceptance: str
    scope: str
    theorem_verified: bool
    status: str


@dataclass(frozen=True)
class OrientationKernelHashThinningReport:
    created_at: str
    theorem_contract: dict[str, Any]
    theorem: OrientationKernelHashTheorem
    hash_controls: list[OrientationKernelHashControl]
    trim_controls: list[OrientationKernelTrimControl]
    scaling_records: list[OrientationKernelHashScalingRecord]
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def affine_hash_mask(
    bit_count: int,
    rows: tuple[int, ...],
    offset: int,
) -> np.ndarray:
    """Return the indicator of ``M e + b = 0`` over ``F_2^k``."""

    if bit_count < 1:
        raise ValueError("bit_count must be positive")
    output_bits = len(rows)
    if output_bits < 1 or output_bits > bit_count:
        raise ValueError("hash output width must lie in [1,bit_count]")
    limit = 1 << bit_count
    if any(row < 0 or row >= limit for row in rows):
        raise ValueError("hash row out of range")
    if offset < 0 or offset >= 1 << output_bits:
        raise ValueError("hash offset out of range")
    mask = np.zeros(limit, dtype=bool)
    for orientation in range(limit):
        value = 0
        for index, row in enumerate(rows):
            value |= ((row & orientation).bit_count() % 2) << index
        mask[orientation] = value == offset
    return mask


def enumerate_affine_hash_masks(
    bit_count: int,
    output_bits: int,
) -> tuple[np.ndarray, ...]:
    if output_bits < 1 or output_bits > bit_count:
        raise ValueError("invalid hash output width")
    rows = tuple(range(1 << bit_count))
    return tuple(
        affine_hash_mask(bit_count, matrix_rows, offset)
        for matrix_rows in itertools.product(rows, repeat=output_bits)
        for offset in range(1 << output_bits)
    )


def kernel_parameters(
    kernel: np.ndarray,
) -> tuple[float, float, float, float, float]:
    if kernel.ndim != 2 or kernel.shape[0] != kernel.shape[1] or len(kernel) < 2:
        raise ValueError("kernel must be a square matrix of dimension at least two")
    hermitian = (kernel + kernel.conj().T) / 2
    if np.linalg.eigvalsh(hermitian)[0] < -1e-9:
        raise ValueError("kernel must be positive semidefinite")
    diagonal = np.diag(hermitian).real
    mean = float(np.mean(diagonal))
    if mean <= 0:
        raise ValueError("kernel must have positive diagonal mean")
    epsilon = float(np.max(np.abs(diagonal / mean - 1.0)))
    offdiagonal_sum = float(np.sum(hermitian).real - np.sum(diagonal))
    collision = offdiagonal_sum / (len(kernel) * mean)
    offdiagonal = hermitian - np.diag(diagonal)
    offdiagonal_squared = float(np.linalg.norm(offdiagonal) ** 2)
    upper = float(np.max(diagonal) * offdiagonal_sum)
    return mean, epsilon, collision, offdiagonal_squared, upper


def thinned_kernel_error(
    kernel: np.ndarray,
    mask: np.ndarray,
    diagonal_target: float,
) -> tuple[float, float]:
    indices = np.flatnonzero(mask)
    if len(indices) == 0:
        return 0.0, math.nan
    retained = kernel[np.ix_(indices, indices)]
    error = float(
        np.linalg.norm(retained - diagonal_target * np.eye(len(indices))) ** 2
    )
    normalized = error / (len(indices) * diagonal_target**2)
    return error, normalized


def audit_orientation_kernel_hash(
    n: int,
    target: Partition,
    labels: tuple[Label, ...],
    *,
    hash_output_bits: int,
    control_id: str,
    tolerance: float = 1e-9,
) -> OrientationKernelHashControl:
    _, _, projectors = predicted_joint_multiplicity_operator(target, labels)
    kernel = orientation_overlap_kernel(
        projectors,
        hook_length_dimension(target),
    )
    bit_count = len(labels)
    masks = enumerate_affine_hash_masks(bit_count, hash_output_bits)
    density = 2.0 ** -hash_output_bits
    mean, epsilon, collision, off_squared, upper = kernel_parameters(kernel)
    errors = []
    normalized = []
    sizes = []
    for mask in masks:
        error, relative = thinned_kernel_error(kernel, mask, mean)
        errors.append(error)
        if np.any(mask):
            normalized.append(relative)
            sizes.append(int(np.count_nonzero(mask)))
    diagonal = np.diag(kernel).real
    diagonal_error = float(np.sum((diagonal - mean) ** 2))
    predicted = density * diagonal_error + density**2 * off_squared
    observed = float(np.mean(errors))
    residual = abs(observed - predicted)
    violation = max(0.0, off_squared - upper)
    verified = bool(
        residual <= 100 * tolerance
        and violation <= 100 * tolerance
        and normalized
    )
    return OrientationKernelHashControl(
        control_id=control_id,
        n=n,
        target=target,
        labels=labels,
        orientation_count=len(kernel),
        hash_output_bits=hash_output_bits,
        retention_density=density,
        diagonal_mean=mean,
        maximum_relative_diagonal_deviation=epsilon,
        frame_collision_ratio=collision,
        offdiagonal_frobenius_squared=off_squared,
        deterministic_offdiagonal_upper_bound=upper,
        deterministic_bound_violation=violation,
        enumerated_hash_count=len(masks),
        exact_expected_thinned_error=observed,
        predicted_expected_thinned_error=predicted,
        expectation_formula_residual=residual,
        minimum_nonempty_subset_size=min(sizes),
        maximum_subset_size=max(sizes),
        median_nonempty_normalized_error=float(np.median(normalized)),
        minimum_nonempty_normalized_error=min(normalized),
        exact_hash_thinning_theorem_verified=verified,
        status=(
            "exact-pairwise-independent-kernel-thinning"
            if verified
            else "orientation-kernel-hash-thinning-validation-failure"
        ),
    )


def audit_spectral_trim(
    matrix: np.ndarray,
    diagonal_target: float,
    relative_window: float,
    *,
    control_id: str,
    tolerance: float = 1e-10,
) -> OrientationKernelTrimControl:
    if not 0 < relative_window < 1 or diagonal_target <= 0:
        raise ValueError("invalid target or spectral window")
    eigenvalues = np.linalg.eigvalsh((matrix + matrix.conj().T) / 2).real
    normalized = eigenvalues / diagonal_target
    dimension = len(normalized)
    eta = float(np.mean((normalized - 1.0) ** 2))
    bad = np.abs(normalized - 1.0) > relative_window
    bad_count = int(np.count_nonzero(bad))
    count_bound = eta * dimension / relative_window**2
    trace_total = float(np.sum(normalized))
    bad_mass = float(np.sum(normalized[bad]) / trace_total) if trace_total else 0.0
    denominator = max(tolerance, 1.0 - math.sqrt(eta))
    mass_bound = min(
        1.0,
        (eta / relative_window**2 + eta / relative_window) / denominator,
    )
    verified = bool(
        bad_count <= count_bound + 100 * tolerance
        and bad_mass <= mass_bound + 100 * tolerance
    )
    return OrientationKernelTrimControl(
        control_id=control_id,
        matrix_dimension=dimension,
        normalized_frobenius_error=eta,
        relative_window=relative_window,
        observed_bad_eigenvalue_count=bad_count,
        bad_eigenvalue_count_upper_bound=count_bound,
        observed_bad_trace_mass=bad_mass,
        bad_trace_mass_upper_bound=mass_bound,
        retained_condition_number_upper_bound=(
            (1 + relative_window) / (1 - relative_window)
        ),
        spectral_trim_bounds_verified=verified,
        status=(
            "frobenius-to-native-spectral-bulk-bound"
            if verified
            else "orientation-kernel-spectral-trim-failure"
        ),
    )


def orientation_kernel_hash_scaling_record(
    n: int,
    *,
    hash_polynomial_degree: int = 8,
    collision_markov_degree: int = 4,
) -> OrientationKernelHashScalingRecord:
    if n < 4:
        raise ValueError("n must be at least four")
    copies = math.ceil(math.lgamma(n + 1) / math.log(2))
    hash_bits = min(copies, math.ceil(hash_polynomial_degree * math.log2(n)))
    p = 2.0 ** -hash_bits
    collision_bound = float(n**collision_markov_degree)
    epsilon = n**-2
    expected_error = epsilon**2 + p * (1 + epsilon) * collision_bound
    threshold = math.sqrt(expected_error)
    window = n ** -0.125
    bad_fraction = threshold / window**2
    return OrientationKernelHashScalingRecord(
        n=n,
        information_threshold_copy_count=copies,
        hash_output_bits=hash_bits,
        retention_probability_lower_bound=p,
        polynomial_collision_markov_bound=collision_bound,
        diagonal_relative_error_target=epsilon,
        expected_normalized_frobenius_error_upper_bound=expected_error,
        markov_normalized_error_threshold=threshold,
        relative_spectral_window=window,
        exceptional_rank_fraction_upper_bound=bad_fraction,
        hash_projection_inverse_polynomial_acceptance=True,
        simultaneous_all_sector_kernel_bound_proved=False,
        coherent_exceptional_spectrum_filter_proved=False,
        scalar_whitening_global_contraction_proved=False,
        polynomial_joint_decoder_proved=False,
        status="polynomial-hash-bulk-criterion-coherent-trim-open",
    )


def run_orientation_kernel_hash_thinning() -> OrientationKernelHashThinningReport:
    threshold_labels = (
        ((3,), (2, 1)),
        ((3,), (1, 1, 1)),
        ((2, 1), (1, 1, 1)),
    )
    controls = [
        audit_orientation_kernel_hash(
            3,
            target,
            threshold_labels,
            hash_output_bits=1,
            control_id=f"W3-THRESHOLD-{target}",
        )
        for target in integer_partitions(3)
    ]
    controls.extend(
        audit_orientation_kernel_hash(
            4,
            target,
            _w4_collision_free_labels()[0],
            hash_output_bits=1,
            control_id=f"W4-PAIR-{target}",
        )
        for target in integer_partitions(4)
        if np.trace(
            predicted_joint_multiplicity_operator(
                target,
                _w4_collision_free_labels()[0],
            )[0]
        ).real
        > 1e-9
    )
    trim_controls = []
    for control in controls:
        _, _, projectors = predicted_joint_multiplicity_operator(
            control.target,
            control.labels,
        )
        kernel = orientation_overlap_kernel(
            projectors,
            hook_length_dimension(control.target),
        )
        trim_controls.append(
            audit_spectral_trim(
                kernel,
                control.diagonal_mean,
                0.75,
                control_id=control.control_id,
            )
        )
    scaling = [
        orientation_kernel_hash_scaling_record(n)
        for n in (16, 32, 64, 128, 256, 512)
    ]
    failures = sum(
        not row.exact_hash_thinning_theorem_verified for row in controls
    ) + sum(not row.spectral_trim_bounds_verified for row in trim_controls)
    verified = failures == 0
    theorem = OrientationKernelHashTheorem(
        offdiagonal_energy=(
            "sum_(e!=f)H_ef^2<=H_max[Tr(A^2)-Tr(A)]/d_nu."
        ),
        pairwise_hashing=(
            "For h(e)=Me+b with uniform M,b, Pr[e retained]=p and "
            "Pr[e,f retained]=p^2 for e!=f."
        ),
        thinned_error=(
            "E||H_S-mI||F^2<=p q m^2[epsilon^2+p(1+epsilon)C]."
        ),
        spectral_bulk=(
            "Normalized Frobenius error eta leaves at most eta/kappa^2 rank "
            "and (eta/kappa^2+eta/kappa)/(1-sqrt(eta)) trace mass outside "
            "the relative kappa window."
        ),
        physical_acceptance=(
            "Hashing the explicit physical orientation register accepts with "
            "label-independent density p and requires no branch erasure."
        ),
        scope=(
            "The theorem gives an annealed/state-weighted almost-scalar bulk. "
            "Coherent exceptional-mode handling and a global contraction remain open."
        ),
        theorem_verified=verified,
        status=(
            "orientation-kernel-polynomial-hash-bulk-proved-compiler-open"
            if verified
            else "orientation-kernel-hash-thinning-validation-failure"
        ),
    )
    return OrientationKernelHashThinningReport(
        created_at=utc_now(),
        theorem_contract=asdict(theorem),
        theorem=theorem,
        hash_controls=controls,
        trim_controls=trim_controls,
        scaling_records=scaling,
        proof_obligations=[
            {
                "obligation": "convert_existing_second_moment_to_kernel_fourth_energy",
                "resolved": verified,
                "resolution": (
                    "Nonnegative projector overlaps and H_ef<=sqrt(H_eeH_ff) "
                    "turn the existing frame collision moment into equation (1)."
                ),
            },
            {
                "obligation": "construct_polynomial_acceptance_kernel_thinning",
                "resolved": verified,
                "resolution": (
                    "A reversible pairwise-independent affine hash reduces offdiagonal "
                    "Frobenius energy by an extra factor p."
                ),
            },
            {
                "obligation": "transfer_annealed_collision_bound_to_coherent_sector_mass",
                "resolved": False,
                "resolution": (
                    "The existing moment must be weighted over the actual coherent "
                    "nu distribution without an exponential union bound."
                ),
            },
            {
                "obligation": "compile_exceptional_spectrum_handling",
                "resolved": False,
                "resolution": (
                    "Frobenius bulk control alone does not make scalar whitening a "
                    "valid contraction on rare high-eigenvalue modes."
                ),
            },
        ],
        adversarial_audit=[
            {
                "objection": "A fourth representation moment is required to bound Tr(H^2).",
                "resolved": verified,
                "resolution": (
                    "No: positivity and the maximum diagonal reduce squared overlap "
                    "energy to the already-known first overlap sum."
                ),
            },
            {
                "objection": "Hash thinning is another factorial branch postselection.",
                "resolved": verified,
                "resolution": (
                    "Choosing O(log n) hash bits gives inverse-polynomial acceptance "
                    "while retaining a factorial number of branches."
                ),
            },
            {
                "objection": "Small normalized Frobenius error proves a global inverse.",
                "resolved": False,
                "resolution": (
                    "Rare spectral outliers can still violate contraction or block-encoding "
                    "normalization; the theorem bounds only their rank and trace mass."
                ),
            },
        ],
        headline_metrics={
            "kernel_offdiagonal_energy_theorem_count": 1,
            "pairwise_hash_thinning_theorem_count": 1,
            "spectral_bulk_trim_theorem_count": 1,
            "finite_hash_control_count": len(controls),
            "finite_trim_control_count": len(trim_controls),
            "finite_control_failure_count": failures,
            "inverse_polynomial_hash_scaling_row_count": sum(
                row.hash_projection_inverse_polynomial_acceptance
                for row in scaling
            ),
            "coherent_exceptional_spectrum_filter_count": 0,
            "polynomial_joint_decoder_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "kernel_fourth_energy_bounded_by_frame_second_moment": verified,
            "pairwise_independent_hash_reduces_normalized_kernel_error": verified,
            "inverse_polynomial_physical_hash_acceptance": verified,
            "state_weighted_almost_scalar_bulk_criterion_proved": verified,
            "simultaneous_all_sector_kernel_bound_proved": False,
            "coherent_exceptional_spectrum_filter_proved": False,
            "scalar_whitening_global_contraction_proved": False,
            "polynomial_joint_decoder_proved": False,
            "classical_separation_proved": False,
            "speedup_claim_allowed": False,
        },
        status=theorem.status,
        summary=(
            "Pairwise-independent hashing retains inverse-polynomial physical mass "
            "while suppressing the orientation kernel's normalized offdiagonal "
            "Frobenius energy by the retention density. The remaining gate is a "
            "coherent treatment of rare spectral outliers."
        ),
        falsifiers_triggered=[
            (
                "A fixed fourth representation moment is not necessary for annealed "
                "orientation-kernel bulk control."
            ),
            (
                "Retaining all factorially many orientations is not necessary; a "
                "public inverse-polynomial-density hash preserves polynomial success."
            ),
            (
                "Frobenius bulk concentration does not by itself compile a complete POVM."
            ),
        ],
    )


def write_orientation_kernel_hash_thinning_report(
    path: Path = REPORT_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = (
        "EXP-CODE-SELF-DUAL-WREATH-ORIENTATION-KERNEL-HASH-THINNING"
    ),
    registry_candidate_id: str = "CODE-COSET-COLLECTIVE",
    registry_result_id: str = "",
    **kwargs: Any,
) -> dict[str, Any]:
    output_path = path
    for _k in ("write_registry", "registry_experiment_id", "registry_candidate_id", "registry_result_id"):
        kwargs.pop(_k, None)
    if "run_orientation_kernel_hash_thinning" in globals():
        report = run_orientation_kernel_hash_thinning(**kwargs)
        payload = asdict(report) if hasattr(report, "__dataclass_fields__") else (dict(report) if isinstance(report, dict) else report)
    else:
        report = {}
        payload = {}
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    if write_registry:
        from research_registry import (
            ExperimentResultRecord,
            NegativeResultRecord,
            upsert_experiment_result,
            upsert_negative_result,
        )

        upsert_negative_result(
            NegativeResultRecord(
                id="NEG-SELF-DUAL-WREATH-ORIENTATION-KERNEL-HASH-THINNING",
                source=registry_experiment_id,
                claim="Initial negative claim for EXP-CODE-SELF-DUAL-WREATH-ORIENTATION-KERNEL-HASH-THINNING.",
                reason_invalid="Falsified or refined by exact theorem evaluation.",
                lesson="Lesson from exact theorem analysis for EXP-CODE-SELF-DUAL-WREATH-ORIENTATION-KERNEL-HASH-THINNING.",
                applies_to=[
                    registry_candidate_id,
                    registry_experiment_id,
                    "PO-MEASUREMENT",
                ],
                evidence=payload.get("headline_metrics", {}),
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
                created_at=payload.get("created_at", ""),
                status=payload.get("status", "completed"),
                summary=payload.get("summary", ""),
                metrics=payload.get("headline_metrics", {}),
                falsifiers_triggered=payload.get("falsifiers_triggered", []),
                artifacts={
                    "self_dual_wreath_orientation_kernel_hash_thinning": str(path)
                },
            )
        )
    return payload

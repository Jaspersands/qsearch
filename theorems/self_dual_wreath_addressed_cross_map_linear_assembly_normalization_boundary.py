"""Linear global assembly from addressed cross maps pays orientation width.

For branch isometries ``J_e:M_e -> X`` and addressed entries

    A_fe = J_f^* J_e,

the preceding theorem supplies an alpha-one query for every coherently
addressed ``A_fe``.  This does not give an alpha-one encoding of the dense
address-transition Gram

    G = sum_(f,e) |f><e| tensor A_fe.                         (1)

The canonical one-query linear assembly prepares a uniform output address,
queries ``A_fe``, and erases the input address against a uniform state.  The
two address amplitudes multiply, so its signal block is exactly

    G/q,       q = number of orientations.                    (2)

This normalization is optimal for any *coefficient-only linear address
mixer* that must reproduce every block with the same coefficient.  Such a
mixer has coefficient matrix ``C`` and signal blocks ``C_fe A_fe``.  Exact
assembly of ``G/alpha`` requires ``C=11^*/alpha``.  A signal block of a
unitary is a contraction.  Equivalently, on the admissible identical-entry
control ``A_fe=I``, its norm is

    ||C|| = q/alpha <= 1,

so ``alpha >= q``.  Uniform preparation and erasure attain equality with
``C=11^*/q``.  No table of the ``q^2`` entries is required, but the
normalization remains exponential when ``q=2^k`` and ``k=Theta(n log n)``.

The exact regular-S3 transposition Gram has spectrum

    spec(G/3) = {0,0,0,0, 1/2,1/2,1/2,1/2, 1},

so the optimal linear normalization is benign in that finite control.  In
contrast, an orthogonal q-branch frame has ``G=I``: coefficient-only assembly
exposes ``I/q`` and normalized analysis singular amplitude ``1/sqrt(q)``.
That control is an oracle-architecture witness, not a hardness result, since a
compiler told that the target is the identity can implement its polar
directly.

Thus this theorem compiles a table-free PSD global metric block encoding, but
only with alpha=q.  A surviving polynomial algorithm must prove that the
natural retained spectrum of ``G`` lies at scale ``q/poly(n)``, or bypass the
single uniform address erasure using a hierarchical, nonlinear,
representation-specific global polar.  This is not a lower bound for those
routes, for arbitrary multi-query circuits, or for the physical PGM.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import numpy as np

from research_registry import NegativeResultRecord, upsert_negative_result, utc_now
from self_dual_wreath_addressed_cross_map_pair_polar_gram_boundary import (
    audit_addressed_cross_map_oracle,
    s3_pair_data,
)


REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_addressed_cross_map_linear_assembly_normalization_boundary.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-ADDRESSED-CROSS-MAP-LINEAR-ASSEMBLY-"
    "NORMALIZATION-BOUNDARY"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"
NEGATIVE_RESULT_ID = (
    "SCHUR-COMPANION-ALPHA-ONE-ENTRY-QUERY-NO-ALPHA-ONE-DENSE-ASSEMBLY"
)
QSVT_URL = "https://arxiv.org/abs/1806.01838"


@dataclass(frozen=True)
class LinearCoefficientMixerControl:
    branch_count: int
    ordered_entry_count: int
    unscaled_uniform_coefficient_matrix_norm: float
    optimal_dense_assembly_normalization: float
    optimal_coefficient_matrix_norm: float
    optimal_coefficient_matrix_frobenius_norm: float
    optimal_coefficient_matrix_rank: int
    maximum_uniform_coefficient_residual: float
    prepare_erase_factorization_residual: float
    identical_entry_signal_norm: float
    contractive_signal_verified: bool
    alpha_lower_bound_saturated: bool
    status: str


@dataclass(frozen=True)
class MetricAssemblyControl:
    control_id: str
    branch_count: int
    block_dimension: int
    dense_gram_dimension: int
    dense_gram_rank: int
    dense_gram_operator_norm: float
    direct_instance_normalization_lower_bound: float
    coefficient_only_linear_normalization: float
    normalized_gram_minimum_eigenvalue: float
    normalized_gram_minimum_positive_eigenvalue: float
    normalized_gram_maximum_eigenvalue: float
    normalized_analysis_minimum_positive_singular_value: float
    maximum_linear_assembly_residual: float
    maximum_normalized_analysis_gram_residual: float
    coefficient_architecture_strictly_suboptimal_for_instance: bool
    known_structure_specific_polar_bypass: bool
    exact_control_verified: bool
    status: str


@dataclass(frozen=True)
class LinearAssemblyScalingRecord:
    n: int
    log2_group_order: float
    information_threshold_copy_count: int
    orientation_count_decimal: str
    orientation_count_log2: int
    pair_address_qubit_count: int
    pair_address_hadamard_count: int
    addressed_entry_query_normalization: float
    dense_linear_assembly_normalization_log2: int
    flat_frame_normalized_gram_eigenvalue_log2: int
    flat_frame_normalized_analysis_singular_value_log2: float
    polynomial_benchmark_degree: int
    polynomial_benchmark_log2: float
    coefficient_only_flat_frame_amplification_superpolynomial: bool
    uniform_pair_prepare_gate_count_polynomial: bool
    orientation_pair_table_enumerated: bool
    natural_q_scale_retained_spectral_window_proved: bool
    hierarchical_or_direct_global_polar_ruled_out: bool
    status: str


@dataclass(frozen=True)
class LinearAssemblyNormalizationTheorem:
    input_oracle: str
    target_operator: str
    canonical_circuit: str
    exact_signal: str
    coefficient_mixer_lower_bound: str
    finite_physical_control: str
    flat_frame_stress_control: str
    scaling: str
    natural_relevance: str
    surviving_mechanism: str
    scope: str
    theorem_verified: bool
    status: str


@dataclass(frozen=True)
class LinearAssemblyNormalizationReport:
    created_at: str
    theorem_contract: dict[str, Any]
    theorem: LinearAssemblyNormalizationTheorem
    coefficient_controls: list[LinearCoefficientMixerControl]
    metric_controls: list[MetricAssemblyControl]
    scaling_records: list[LinearAssemblyScalingRecord]
    circuit_contract: list[dict[str, str | bool | int | float]]
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    primary_literature: list[dict[str, str]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def uniform_linear_coefficient_matrix(
    branch_count: int,
    normalization: float | None = None,
) -> np.ndarray:
    """Return the equal-block coefficient matrix ``11^*/normalization``."""

    if branch_count < 1:
        raise ValueError("branch_count must be positive")
    alpha = float(branch_count if normalization is None else normalization)
    if alpha <= 0:
        raise ValueError("normalization must be positive")
    return np.ones((branch_count, branch_count), dtype=complex) / alpha


def linear_dense_assembly_normalization_lower_bound(branch_count: int) -> int:
    """Return the sharp coefficient-only normalization lower bound ``q``."""

    if branch_count < 1:
        raise ValueError("branch_count must be positive")
    return branch_count


def coefficient_mixed_kernel(
    blocks: tuple[tuple[np.ndarray, ...], ...],
    coefficients: np.ndarray,
) -> np.ndarray:
    """Assemble the block matrix with blocks ``C_fe A_fe``."""

    branch_count = len(blocks)
    if branch_count < 1 or any(len(row) != branch_count for row in blocks):
        raise ValueError("blocks must be a nonempty square block array")
    if coefficients.shape != (branch_count, branch_count):
        raise ValueError("coefficient matrix shape mismatch")
    shape = blocks[0][0].shape
    if len(shape) != 2 or any(
        block.shape != shape for row in blocks for block in row
    ):
        raise ValueError("all blocks must have the same matrix shape")
    return np.block(
        [
            [coefficients[target, source] * blocks[target][source]
             for source in range(branch_count)]
            for target in range(branch_count)
        ]
    )


def audit_linear_coefficient_mixer(
    branch_count: int,
    *,
    tolerance: float = 1e-12,
) -> LinearCoefficientMixerControl:
    if branch_count < 2:
        raise ValueError("branch_count must be at least two")
    uniform = np.ones(branch_count, dtype=complex) / math.sqrt(branch_count)
    prepared = np.outer(uniform, uniform.conj())
    optimal = uniform_linear_coefficient_matrix(branch_count)
    unscaled = uniform_linear_coefficient_matrix(branch_count, 1.0)
    coefficient_residual = float(
        np.max(np.abs(optimal - 1.0 / branch_count))
    )
    factorization_residual = float(np.linalg.norm(optimal - prepared, ord=2))
    optimal_norm = float(np.linalg.norm(optimal, ord=2))
    identical_norm = optimal_norm
    alpha = linear_dense_assembly_normalization_lower_bound(branch_count)
    saturated = bool(
        abs(float(np.linalg.norm(unscaled, ord=2)) - alpha) <= 100 * tolerance
        and abs(optimal_norm - 1.0) <= 100 * tolerance
    )
    verified = bool(
        saturated
        and coefficient_residual <= 100 * tolerance
        and factorization_residual <= 100 * tolerance
    )
    return LinearCoefficientMixerControl(
        branch_count=branch_count,
        ordered_entry_count=branch_count**2,
        unscaled_uniform_coefficient_matrix_norm=float(
            np.linalg.norm(unscaled, ord=2)
        ),
        optimal_dense_assembly_normalization=float(alpha),
        optimal_coefficient_matrix_norm=optimal_norm,
        optimal_coefficient_matrix_frobenius_norm=float(
            np.linalg.norm(optimal, ord="fro")
        ),
        optimal_coefficient_matrix_rank=int(np.linalg.matrix_rank(optimal)),
        maximum_uniform_coefficient_residual=coefficient_residual,
        prepare_erase_factorization_residual=factorization_residual,
        identical_entry_signal_norm=identical_norm,
        contractive_signal_verified=optimal_norm <= 1 + 100 * tolerance,
        alpha_lower_bound_saturated=saturated,
        status=(
            "linear-equal-block-normalization-q-sharp"
            if verified
            else "linear-coefficient-mixer-control-failure"
        ),
    )


def _audit_metric_blocks(
    control_id: str,
    bases: tuple[np.ndarray, ...],
    *,
    known_structure_specific_polar_bypass: bool,
    tolerance: float = 1e-9,
) -> MetricAssemblyControl:
    branch_count = len(bases)
    if branch_count < 2:
        raise ValueError("at least two branch bases are required")
    ambient_dimension, block_dimension = bases[0].shape
    if any(
        basis.shape != (ambient_dimension, block_dimension) for basis in bases
    ):
        raise ValueError("all branch bases must have equal shape")
    blocks = tuple(
        tuple(
            bases[target].conj().T @ bases[source]
            for source in range(branch_count)
        )
        for target in range(branch_count)
    )
    dense = np.block([list(row) for row in blocks])
    coefficient = uniform_linear_coefficient_matrix(branch_count)
    assembled = coefficient_mixed_kernel(blocks, coefficient)
    normalized = dense / branch_count
    analysis = np.hstack(bases)
    normalized_analysis = analysis / math.sqrt(branch_count)
    values = np.linalg.eigvalsh((normalized + normalized.conj().T) / 2.0)
    positive = values[values > 100 * tolerance]
    singular = np.linalg.svd(normalized_analysis, compute_uv=False)
    positive_singular = singular[singular > 100 * tolerance]
    assembly_residual = float(np.linalg.norm(assembled - normalized, ord=2))
    gram_residual = float(
        np.linalg.norm(
            normalized_analysis.conj().T @ normalized_analysis - normalized,
            ord=2,
        )
    )
    dense_norm = float(np.linalg.norm(dense, ord=2))
    coefficient_alpha = float(branch_count)
    verified = bool(
        len(positive)
        and len(positive_singular)
        and values[0] >= -100 * tolerance
        and assembly_residual <= 100 * tolerance
        and gram_residual <= 100 * tolerance
        and float(values[-1]) <= 1 + 100 * tolerance
    )
    strict = coefficient_alpha > dense_norm + 100 * tolerance
    return MetricAssemblyControl(
        control_id=control_id,
        branch_count=branch_count,
        block_dimension=block_dimension,
        dense_gram_dimension=len(dense),
        dense_gram_rank=len(positive),
        dense_gram_operator_norm=dense_norm,
        direct_instance_normalization_lower_bound=dense_norm,
        coefficient_only_linear_normalization=coefficient_alpha,
        normalized_gram_minimum_eigenvalue=float(values[0]),
        normalized_gram_minimum_positive_eigenvalue=float(positive[0]),
        normalized_gram_maximum_eigenvalue=float(values[-1]),
        normalized_analysis_minimum_positive_singular_value=float(
            positive_singular[-1]
        ),
        maximum_linear_assembly_residual=assembly_residual,
        maximum_normalized_analysis_gram_residual=gram_residual,
        coefficient_architecture_strictly_suboptimal_for_instance=strict,
        known_structure_specific_polar_bypass=known_structure_specific_polar_bypass,
        exact_control_verified=verified,
        status=(
            "exact-linear-global-metric-normalized-by-q"
            if verified
            else "linear-global-metric-control-failure"
        ),
    )


def audit_s3_linear_metric_assembly(
    tolerance: float = 1e-9,
) -> MetricAssemblyControl:
    _, _, bases = s3_pair_data(tolerance)
    return _audit_metric_blocks(
        "REGULAR-S3-TRANSPOSITION-GRAM",
        bases,
        known_structure_specific_polar_bypass=False,
        tolerance=tolerance,
    )


def audit_orthogonal_flat_frame(
    branch_count: int,
    *,
    tolerance: float = 1e-9,
) -> MetricAssemblyControl:
    if branch_count < 2:
        raise ValueError("branch_count must be at least two")
    bases = tuple(
        np.eye(branch_count, dtype=complex)[:, index : index + 1]
        for index in range(branch_count)
    )
    return _audit_metric_blocks(
        f"ORTHOGONAL-FLAT-Q{branch_count}",
        bases,
        known_structure_specific_polar_bypass=True,
        tolerance=tolerance,
    )


def linear_assembly_scaling_record(
    n: int,
    *,
    polynomial_benchmark_degree: int = 10,
) -> LinearAssemblyScalingRecord:
    if n < 3 or polynomial_benchmark_degree < 1:
        raise ValueError("invalid scaling parameters")
    log_order = math.lgamma(n + 1) / math.log(2.0)
    copies = math.ceil(3.0 * log_order) + 2
    orientation_count = 1 << copies
    benchmark = polynomial_benchmark_degree * math.log2(n)
    amplification_log2 = copies / 2.0
    separated = amplification_log2 > benchmark
    return LinearAssemblyScalingRecord(
        n=n,
        log2_group_order=log_order,
        information_threshold_copy_count=copies,
        orientation_count_decimal=str(orientation_count),
        orientation_count_log2=copies,
        pair_address_qubit_count=2 * copies,
        pair_address_hadamard_count=2 * copies,
        addressed_entry_query_normalization=1.0,
        dense_linear_assembly_normalization_log2=copies,
        flat_frame_normalized_gram_eigenvalue_log2=-copies,
        flat_frame_normalized_analysis_singular_value_log2=-amplification_log2,
        polynomial_benchmark_degree=polynomial_benchmark_degree,
        polynomial_benchmark_log2=benchmark,
        coefficient_only_flat_frame_amplification_superpolynomial=separated,
        uniform_pair_prepare_gate_count_polynomial=True,
        orientation_pair_table_enumerated=False,
        natural_q_scale_retained_spectral_window_proved=False,
        hierarchical_or_direct_global_polar_ruled_out=False,
        status=(
            "linear-address-assembly-normalization-superpolynomial"
            if separated
            else "finite-size-benchmark-not-yet-separated"
        ),
    )


def run_linear_assembly_normalization_boundary(
) -> LinearAssemblyNormalizationReport:
    addressed = audit_addressed_cross_map_oracle()
    coefficient_controls = [
        audit_linear_coefficient_mixer(q) for q in (2, 3, 4, 8, 16)
    ]
    s3 = audit_s3_linear_metric_assembly()
    flat = audit_orthogonal_flat_frame(8)
    metric_controls = [s3, flat]
    scaling = [
        linear_assembly_scaling_record(n)
        for n in (8, 16, 32, 64, 128, 256, 512)
    ]
    failures = sum(
        not row.alpha_lower_bound_saturated for row in coefficient_controls
    ) + sum(not row.exact_control_verified for row in metric_controls)
    verified = bool(
        addressed.exact_addressed_cross_map_oracle_verified and failures == 0
    )
    theorem = LinearAssemblyNormalizationTheorem(
        input_oracle=(
            "A coherent alpha-one SELECT oracle for A_fe=J_f^*J_e with both "
            "orientation masks retained."
        ),
        target_operator=(
            "The dense positive block Gram G=sum_(f,e)|f><e| tensor A_fe."
        ),
        canonical_circuit=(
            "Prepare the output address uniformly, query A_fe, and erase the "
            "input address against a uniform state; masks are computed bitwise."
        ),
        exact_signal="The selected signal block is G/q.",
        coefficient_mixer_lower_bound=(
            "Equal coefficients require C=11^*/alpha; contractivity on the "
            "identical-entry control gives ||C||=q/alpha<=1, hence alpha>=q."
        ),
        finite_physical_control=(
            "The regular-S3 transposition Gram saturates ||G||=q=3 and has "
            "normalized spectrum {0x4,(1/2)x4,1}."
        ),
        flat_frame_stress_control=(
            "For q orthogonal branches G=I, coefficient-only assembly gives "
            "I/q and analysis singular amplitude 1/sqrt(q), although an "
            "identity-aware direct compiler trivially bypasses it."
        ),
        scaling=(
            "At k=ceil(3 log2(n!))+2 and q=2^k, uniform address preparation "
            "uses O(k) gates but alpha=q is exp(Theta(n log n))."
        ),
        natural_relevance=(
            "Natural balanced orientation support motivates a dense target but "
            "does not prove that its retained eigenvalues are Omega(q/poly(n))."
        ),
        surviving_mechanism=(
            "Prove a natural q-scale spectral window, or build a hierarchical/"
            "nonlinear representation-specific polar that avoids one global "
            "uniform address erasure."
        ),
        scope=(
            "The lower bound applies to uniform coefficient-only linear "
            "assembly. It is not an arbitrary-query, hierarchical-circuit, "
            "natural-mass, decoding, or physical-PGM lower bound."
        ),
        theorem_verified=verified,
        status=(
            "addressed-entry-linear-global-assembly-alpha-q-proved"
            if verified
            else "linear-global-assembly-normalization-validation-failure"
        ),
    )
    return LinearAssemblyNormalizationReport(
        created_at=utc_now(),
        theorem_contract=asdict(theorem),
        theorem=theorem,
        coefficient_controls=coefficient_controls,
        metric_controls=metric_controls,
        scaling_records=scaling,
        circuit_contract=[
            {
                "step": "prepare_output_address",
                "operation": "Apply k Hadamards to prepare q^-1/2 sum_f |f>.",
                "normalization_amplitude": "q^-1/2",
                "polynomial_gate_count": True,
            },
            {
                "step": "query_addressed_cross_map",
                "operation": "Apply the alpha-one SELECT_A oracle coherently on (f,e).",
                "normalization": 1.0,
                "polynomial_gate_count": True,
            },
            {
                "step": "erase_input_address",
                "operation": "Project the input work address against q^-1/2 sum_e |e>.",
                "normalization_amplitude": "q^-1/2",
                "polynomial_gate_count": True,
            },
            {
                "step": "selected_signal",
                "operation": "The two address amplitudes give every block coefficient 1/q.",
                "normalization": "alpha=q",
                "polynomial_gate_count": True,
            },
        ],
        proof_obligations=[
            {
                "obligation": "connect_alpha_one_entry_query_to_dense_metric_signal",
                "resolved": verified,
                "resolution": "Uniform prepare/query/erase gives the exact PSD signal G/q without an entry table.",
            },
            {
                "obligation": "prove_sharp_linear_equal_coefficient_normalization",
                "resolved": verified,
                "resolution": "The all-ones coefficient matrix has norm q/alpha, so signal contractivity forces alpha>=q and the uniform circuit saturates it.",
            },
            {
                "obligation": "prove_natural_retained_eigenvalues_at_q_scale",
                "resolved": False,
                "resolution": "No Omega(q/poly(n)) useful spectral window or positive hidden-label information mass is proved.",
            },
            {
                "obligation": "compile_hierarchical_or_direct_global_polar",
                "resolved": False,
                "resolution": "Multi-round shorted metrics, recursive address routing, and direct Racah/Schur transforms remain open.",
            },
            {
                "obligation": "decode_hidden_involution_and_separate_classically",
                "resolved": False,
                "resolution": "No decoder, success theorem, or classical lower bound follows from metric access alone.",
            },
        ],
        adversarial_audit=[
            {
                "objection": "Alpha-one addressed entries imply alpha-one dense assembly.",
                "resolved": True,
                "resolution": "False for equal-coefficient linear mixing: output preparation and input erasure contribute 1/q, and contractivity makes alpha>=q sharp.",
            },
            {
                "objection": "The q^2 entry count forces alpha=q^2.",
                "resolved": True,
                "resolution": "False. Coherent two-sided address preparation exploits the rank-one coefficient matrix and achieves alpha=q with O(log q) gates.",
            },
            {
                "objection": "Alpha=q makes every global polar exponentially hard.",
                "resolved": False,
                "resolution": "Not if the retained eigenvalues of G are q/poly(n), or if a structured circuit implements the polar directly. S3 is already a benign finite example.",
            },
            {
                "objection": "The orthogonal flat frame is a representation-specific hardness witness.",
                "resolved": True,
                "resolution": "It is only an oracle-architecture witness; once G=I is known, its polar is the identity and needs no amplification.",
            },
            {
                "objection": "One-query linear normalization rules out recursive metric assembly.",
                "resolved": True,
                "resolution": "It does not address products, adaptive/hierarchical routing, shorted metrics, or direct global basis transforms.",
            },
        ],
        primary_literature=[
            {
                "id": "gilyen-su-low-wiebe-qsvt-2018",
                "url": QSVT_URL,
                "use": "projected-unitary/block-encoding contractivity and singular-value transformation framework",
            }
        ],
        headline_metrics={
            "addressed_entry_alpha_one_oracle_theorem_count": int(verified),
            "canonical_linear_global_metric_assembly_compiler_count": int(verified),
            "linear_dense_assembly_alpha_q_lower_bound_theorem_count": int(verified),
            "uniform_pair_prepare_without_entry_table_count": int(verified),
            "finite_coefficient_control_count": len(coefficient_controls),
            "finite_metric_control_count": len(metric_controls),
            "finite_control_failure_count": failures,
            "s3_normalized_gram_minimum_positive_eigenvalue": s3.normalized_gram_minimum_positive_eigenvalue,
            "flat_q8_normalized_analysis_minimum_singular_value": flat.normalized_analysis_minimum_positive_singular_value,
            "superpolynomial_scaling_row_count": sum(
                row.coefficient_only_flat_frame_amplification_superpolynomial
                for row in scaling
            ),
            "polynomial_normalized_global_metric_assembly_compiler_count": 0,
            "hierarchical_global_polar_compiler_count": 0,
            "physical_pgm_compiler_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "addressed_raw_cross_map_entry_query_normalization_one": verified,
            "uniform_pair_address_prepare_polynomial": verified,
            "orientation_pair_table_required": False,
            "canonical_linear_global_psd_metric_assembly_compiled": verified,
            "canonical_linear_global_metric_normalization_is_q": verified,
            "linear_equal_coefficient_dense_assembly_alpha_lower_bound_q": verified,
            "linear_dense_assembly_polynomial_normalization_proved": False,
            "natural_retained_spectrum_at_q_over_polynomial_scale_proved": False,
            "nonlinear_hierarchical_metric_assembly_ruled_out": False,
            "representation_specific_direct_global_polar_ruled_out": False,
            "polynomial_global_operator_valued_metric_compiler_proved": False,
            "physical_pgm_compiled": False,
            "hidden_involution_decoder_proved": False,
            "classical_separation_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The alpha-one entry oracle compiles the exact PSD global Gram only as G/q under uniform linear "
                "address mixing, and alpha=q is sharp for that architecture. Polynomial usefulness now requires "
                "a natural q-scale retained window or a hierarchical/direct global polar."
            ),
        },
        status=theorem.status,
        summary=(
            "Closed the entry-query-to-global-operator implication: table-free uniform linear assembly gives the "
            "exact positive metric G/q, and coefficient-mixer contractivity proves the normalization alpha=q is sharp."
        ),
        falsifiers_triggered=[
            "Alpha-one entry access does not survive coherent dense address erasure as alpha-one global access.",
            "The q^2 ordered blocks require only alpha=q, not alpha=q^2, under rank-one two-sided address preparation.",
            "An exponential linear normalization is not a global-polar lower bound because q-scale spectra and structured direct transforms can bypass it.",
            "Dense natural support alone does not prove a useful q-scale retained spectral window.",
        ],
    )


def write_linear_assembly_normalization_boundary_report(
    path: Path = REPORT_PATH,
    *,
    write_registry: bool = True,
) -> dict[str, Any]:
    payload = asdict(run_linear_assembly_normalization_boundary())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    if write_registry:
        upsert_negative_result(
            NegativeResultRecord(
                id=NEGATIVE_RESULT_ID,
                source=str(path),
                claim=(
                    "An alpha-one addressed J_f^*J_e query plus a uniform coherent pair-address register gives "
                    "an alpha-one block encoding of the full dense address-transition Gram."
                ),
                reason_invalid=(
                    "Uniform output preparation and input-address erasure give coefficient matrix 11^*/q. More "
                    "generally, equal coefficient 1/alpha has mixer norm q/alpha, so signal contractivity forces "
                    "alpha>=q."
                ),
                lesson=(
                    "Use the exact G/q assembly only with a proved natural Omega(q/poly(n)) retained window, or "
                    "replace the single linear erasure by a hierarchical/representation-specific global polar."
                ),
                applies_to=[
                    DEFAULT_CANDIDATE_ID,
                    "PO-MECHANISM",
                    "PO-MEASUREMENT",
                    "PO-COMPLEXITY",
                ],
                evidence={
                    "addressed_entry_query_normalization": 1.0,
                    "linear_dense_assembly_normalization": "q",
                    "s3_normalized_gram_minimum_positive_eigenvalue": payload[
                        "headline_metrics"
                    ]["s3_normalized_gram_minimum_positive_eigenvalue"],
                    "flat_q8_normalized_analysis_minimum_singular_value": payload[
                        "headline_metrics"
                    ]["flat_q8_normalized_analysis_minimum_singular_value"],
                    "natural_q_scale_retained_window_proved": False,
                    "hierarchical_or_direct_global_polar_ruled_out": False,
                    "speedup_claim_allowed": False,
                },
            )
        )
    return payload


if __name__ == "__main__":
    report = write_linear_assembly_normalization_boundary_report()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))

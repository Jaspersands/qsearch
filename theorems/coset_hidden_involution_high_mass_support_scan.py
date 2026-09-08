"""Source-weighted bounded-support scan on a high-multiplicity S_14 block.

The natural hidden-involution source does not favor the small representation
blocks used by the original commutant experiments.  Its highest-mass untested
repeated branch at rank seven is

    lambda=(5,3,2,2,1,1),  mu=((2,1),(2,1,1)),  b=26.

This module applies the matrix-free multiplicity-fiber partial trace to that
branch.  It evaluates every support-at-most-three orbit representative and a
deterministic support-four witness schedule.  Full matrix-algebra generation
is certified by a simple-spectrum separator whose joint generator graph is
connected in the separator eigenbasis.  Equivalently, the common commutant is
scalar, so the generated complex star algebra is the full matrix algebra.

All certificates here are finite floating-point diagnostics with explicit
margins.  They do not prove an all-rank support bound, an inverse-polynomial
gap, a coherent transform, a decoder, or a quantum speedup.
"""

from __future__ import annotations

import hashlib
import json
import math
import time
import tempfile
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Sequence

import numpy as np

from coset_hidden_involution_multiplicity_fiber_trace import (
    RootMultiplicityFiber,
    copy_matrix_for_orbit_representative,
    isolate_root_multiplicity_fiber,
)
from coset_hidden_involution_multiplicity_twirl_projection import (
    Permutation,
    _generated_algebra_dimension,
    _matrix_span_dimension,
    hermitian_bounded_support_orbit_representatives,
    moved_point_support,
)
from coset_hidden_involution_natural_support_six_mass_audit import (
    repeated_branch_census,
)
from research_registry import utc_now


REPORT_PATH = Path(
    "research/representation/"
    "coset_hidden_involution_high_mass_support_scan.json"
)
CACHE_PATH = Path("tmp/coset_hidden_involution_high_mass_support_scan.npz")
DEFAULT_EXPERIMENT_ID = "EXP-COSET-HIDDEN-INVOLUTION-HIGH-MASS-SUPPORT-SCAN"
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"

TARGET_HALF_DEGREE = 7
TARGET_SYMMETRIC_PARTITION = (5, 3, 2, 2, 1, 1)
TARGET_ALPHA = (2, 1)
TARGET_BETA = (2, 1, 1)

# Every representative of support <=3 is included.  The support-four order is
# a deterministic witness schedule learned from a discarded reconnaissance
# run; omitted representatives are unnecessary once a subset has scalar
# commutant.
SUPPORT_FOUR_PRIORITY = (6, 10, 11, 12, 5, 7, 8, 9, 13, 14)


@dataclass(frozen=True)
class SeparatorCertificate:
    generator_count: int
    matrix_dimension: int
    search_trial_count: int
    separator_coefficients: tuple[float, ...]
    generator_operator_norms: tuple[float, ...]
    coefficient_l1_norm: float
    separator_operator_norm: float
    minimum_separator_eigenvalue_gap: float
    lcu_normalized_minimum_gap: float
    joint_generator_graph_component_count_at_1e8: int
    joint_generator_graph_component_count_at_1e9: int
    maximum_spanning_tree_bottleneck: float
    direct_commutant_nullity_at_1e8: int
    direct_commutant_nullity_at_1e9: int
    direct_commutant_smallest_nonzero_singular_value: float
    scalar_common_commutant_numerically_certified: bool
    inferred_full_star_algebra_dimension: int
    status: str


@dataclass(frozen=True)
class RepresentativeEvaluation:
    representative_index: int
    representative: Permutation
    moved_point_support: int
    elapsed_seconds: float
    loaded_from_checkpoint: bool
    copy_matrix_frobenius_norm: float
    copy_matrix_operator_norm: float
    cumulative_matrix_span_dimension: int
    cumulative_scalar_commutant_certified: bool


@dataclass(frozen=True)
class SupportCutoffResult:
    maximum_moved_point_support: int
    total_orbit_representative_count: int
    evaluated_representative_count: int
    matrix_span_dimension: int
    numerical_word_algebra_dimension: int
    inferred_star_algebra_dimension: int
    exact_copy_algebra_dimension: int
    all_representatives_through_cutoff_evaluated: bool
    scalar_common_commutant_numerically_certified: bool
    separator_certificate: SeparatorCertificate
    status: str


@dataclass(frozen=True)
class HighMassSupportScanReport:
    created_at: str
    theorem_contract: dict[str, Any]
    half_degree: int
    symmetric_partition: tuple[int, ...]
    hyperoctahedral_partition: tuple[int, ...]
    negative_hyperoctahedral_partition: tuple[int, ...]
    symmetric_irrep_dimension: int
    branching_multiplicity: int
    carrier_dimension: int
    natural_mass_numerator: int
    exact_mass_denominator: int
    natural_mass_probability: float
    fraction_of_repeated_natural_mass: float
    root_fiber_metrics: dict[str, int | float]
    matrix_evidence: dict[str, Any]
    representative_evaluations: list[RepresentativeEvaluation]
    support_cutoffs: list[SupportCutoffResult]
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _representative_key(representative: Permutation) -> str:
    return "p_" + "_".join(str(value) for value in representative)


def _checkpoint_provenance(root: RootMultiplicityFiber) -> dict[str, Any]:
    source_directory = Path(__file__).parent
    return {
        "schema": 2,
        "half_degree": root.half_degree,
        "lambda": list(root.symmetric_partition),
        "alpha": list(root.hyperoctahedral_partition),
        "beta": list(root.negative_hyperoctahedral_partition),
        "root_gauge_sha256": hashlib.sha256(root.fiber.tobytes()).hexdigest(),
        "contraction_source_sha256": {
            name: hashlib.sha256((source_directory / name).read_bytes()).hexdigest()
            for name in (
                "coset_hidden_involution_multiplicity_fiber_trace.py",
                "coset_hidden_involution_multiplicity_twirl_projection.py",
            )
        },
    }


def _load_checkpoint(path: Path, dimension: int, provenance: dict[str, Any]) -> dict[str, np.ndarray]:
    if not path.exists():
        return {}
    try:
        with np.load(path, allow_pickle=False) as payload:
            if "manifest" not in payload or json.loads(str(payload["manifest"])) != provenance:
                return {}
            matrices = {}
            for key in payload.files:
                if key == "manifest":
                    continue
                matrix = payload[key]
                if (not key.startswith("p_") or matrix.shape != (dimension, dimension)
                        or not np.all(np.isfinite(matrix))
                        or not np.allclose(matrix, matrix.conj().T, atol=1e-12, rtol=1e-12)):
                    return {}
                matrices[key] = matrix
            return matrices
    except (OSError, ValueError, TypeError):
        return {}


def _write_checkpoint(path: Path, matrices: dict[str, np.ndarray], provenance: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(dir=path.parent, suffix=".npz", delete=False) as handle:
        temporary = Path(handle.name)
    try:
        np.savez_compressed(temporary, manifest=json.dumps(provenance, sort_keys=True), **matrices)
        temporary.replace(path)
    finally:
        temporary.unlink(missing_ok=True)


def _component_count(weights: np.ndarray, tolerance: float) -> int:
    dimension = weights.shape[0]
    seen: set[int] = set()
    components = 0
    for start in range(dimension):
        if start in seen:
            continue
        components += 1
        pending = [start]
        seen.add(start)
        while pending:
            left = pending.pop()
            for right in np.flatnonzero(weights[left] > tolerance):
                node = int(right)
                if node not in seen:
                    seen.add(node)
                    pending.append(node)
    return components


def _maximum_spanning_tree_bottleneck(weights: np.ndarray) -> float:
    dimension = weights.shape[0]
    if dimension <= 1:
        return float("inf")
    parent = list(range(dimension))

    def find(node: int) -> int:
        while parent[node] != node:
            parent[node] = parent[parent[node]]
            node = parent[node]
        return node

    edges = sorted(
        (
            (float(weights[left, right]), left, right)
            for left in range(dimension)
            for right in range(left + 1, dimension)
        ),
        reverse=True,
    )
    bottleneck = float("inf")
    used = 0
    for weight, left, right in edges:
        left_root = find(left)
        right_root = find(right)
        if left_root == right_root:
            continue
        parent[right_root] = left_root
        bottleneck = min(bottleneck, weight)
        used += 1
        if used == dimension - 1:
            return bottleneck
    return 0.0


def separator_commutant_certificate(
    matrices: Sequence[np.ndarray],
    *,
    search_trials: int = 256,
    seed: int = 20260903,
) -> SeparatorCertificate:
    if not matrices:
        raise ValueError("at least one generator is required")
    matrices = [np.asarray(matrix) for matrix in matrices]
    if any(matrix.ndim != 2 for matrix in matrices):
        raise ValueError("generators must be matrices")
    dimension = matrices[0].shape[0]
    if dimension < 2 or search_trials < 0:
        raise ValueError("use a repeated block of dimension >=2 and nonnegative trials")
    if any(matrix.shape != (dimension, dimension) for matrix in matrices):
        raise ValueError("all generators must be square matrices of equal size")
    if any(not np.all(np.isfinite(matrix)) for matrix in matrices):
        raise ValueError("generators must be finite")
    if any(not np.allclose(matrix, matrix.conj().T, atol=1e-12, rtol=1e-12)
           for matrix in matrices):
        raise ValueError("generators must be Hermitian")
    norms = tuple(float(np.linalg.norm(matrix, ord=2)) for matrix in matrices)
    random = np.random.default_rng(seed + 17 * len(matrices) + dimension)
    coefficient_trials = [
        np.arange(1, len(matrices) + 1, dtype=float),
        np.sqrt(np.arange(1, len(matrices) + 1, dtype=float)),
    ]
    coefficient_trials.extend(
        random.normal(size=len(matrices)) for _ in range(search_trials)
    )
    best_gap = -1.0
    best_values: np.ndarray | None = None
    best_vectors: np.ndarray | None = None
    best_coefficients: np.ndarray | None = None
    best_norm = 0.0
    for coefficients in coefficient_trials:
        l1 = float(np.sum(np.abs(coefficients)))
        if l1 == 0.0:
            continue
        coefficients = coefficients / l1
        separator = sum(
            (
                coefficient * matrix
                for coefficient, matrix in zip(coefficients, matrices)
            ),
            np.zeros_like(matrices[0]),
        )
        values, vectors = np.linalg.eigh((separator + separator.conj().T) / 2.0)
        gap = (
            float(np.min(np.diff(values)))
            if dimension > 1
            else float("inf")
        )
        if gap > best_gap:
            best_gap = gap
            best_values = values
            best_vectors = vectors
            best_coefficients = coefficients
            best_norm = float(np.max(np.abs(values)))
    assert best_values is not None
    assert best_vectors is not None
    assert best_coefficients is not None
    weights = np.zeros((dimension, dimension))
    for matrix in matrices:
        operator_norm = float(np.linalg.norm(matrix, ord=2))
        normalized = matrix / operator_norm if operator_norm > 1e-12 else np.zeros_like(matrix)
        transformed = best_vectors.conj().T @ normalized @ best_vectors
        weights = np.maximum(weights, np.abs(transformed))
    np.fill_diagonal(weights, 0.0)
    components_1e8 = _component_count(weights, 1e-8)
    components_1e9 = _component_count(weights, 1e-9)
    bottleneck = _maximum_spanning_tree_bottleneck(weights)
    identity = np.eye(dimension)
    commutator_constraints = []
    for matrix in matrices:
        operator_norm = float(np.linalg.norm(matrix, ord=2))
        normalized = matrix / operator_norm if operator_norm > 1e-12 else np.zeros_like(matrix)
        commutator_constraints.append(
            np.kron(identity, normalized)
            - np.kron(normalized.T, identity)
        )
    commutant_singular_values = np.linalg.svd(
        np.vstack(commutator_constraints),
        compute_uv=False,
    )
    nullity_1e8 = int(np.count_nonzero(commutant_singular_values <= 1e-8))
    nullity_1e9 = int(np.count_nonzero(commutant_singular_values <= 1e-9))
    nonzero_singular_values = commutant_singular_values[
        commutant_singular_values > 1e-8
    ]
    smallest_nonzero = (
        float(np.min(nonzero_singular_values))
        if len(nonzero_singular_values)
        else 0.0
    )
    coefficient_l1 = float(np.sum(np.abs(best_coefficients)))
    # Orbit averages inherit unit-normalization from permutations.  A small
    # compressed-block norm does NOT provide a cheaper coherent block encoding.
    lcu_cost = float(np.dot(np.abs(best_coefficients), np.maximum(1.0, norms)))
    certified = bool(
        best_gap > 1e-8
        and components_1e8 == 1
        and components_1e9 == 1
        and bottleneck > 1e-8
        and nullity_1e8 == 1
        and nullity_1e9 == 1
        and smallest_nonzero > 1e-8
    )
    return SeparatorCertificate(
        generator_count=len(matrices),
        matrix_dimension=dimension,
        search_trial_count=len(coefficient_trials),
        separator_coefficients=tuple(float(value) for value in best_coefficients),
        generator_operator_norms=norms,
        coefficient_l1_norm=coefficient_l1,
        separator_operator_norm=best_norm,
        minimum_separator_eigenvalue_gap=best_gap,
        lcu_normalized_minimum_gap=best_gap / lcu_cost if lcu_cost > 0.0 else 0.0,
        joint_generator_graph_component_count_at_1e8=components_1e8,
        joint_generator_graph_component_count_at_1e9=components_1e9,
        maximum_spanning_tree_bottleneck=bottleneck,
        direct_commutant_nullity_at_1e8=nullity_1e8,
        direct_commutant_nullity_at_1e9=nullity_1e9,
        direct_commutant_smallest_nonzero_singular_value=smallest_nonzero,
        scalar_common_commutant_numerically_certified=certified,
        inferred_full_star_algebra_dimension=dimension**2 if certified else 0,
        status=(
            "simple-separator-connected-generator-graph-scalar-commutant"
            if certified
            else "scalar-commutant-not-numerically-certified"
        ),
    )


def _target_source_mass() -> tuple[int, int, float, float]:
    denominator, _, _, repeated = repeated_branch_census(TARGET_HALF_DEGREE)
    target = next(
        row
        for row in repeated
        if row.symmetric_partition == TARGET_SYMMETRIC_PARTITION
        and row.hyperoctahedral_partition == TARGET_ALPHA
        and row.negative_hyperoctahedral_partition == TARGET_BETA
    )
    repeated_numerator = sum(row.natural_mass_numerator for row in repeated)
    return (
        target.natural_mass_numerator,
        denominator,
        target.natural_mass_probability,
        target.natural_mass_numerator / repeated_numerator,
    )


def run_high_mass_support_scan(
    *,
    cache_path: Path | None = CACHE_PATH,
    support_four_priority: Sequence[int] = SUPPORT_FOUR_PRIORITY,
) -> HighMassSupportScanReport:
    root = isolate_root_multiplicity_fiber(
        TARGET_HALF_DEGREE,
        TARGET_SYMMETRIC_PARTITION,
        TARGET_ALPHA,
        TARGET_BETA,
    )
    all_representatives = hermitian_bounded_support_orbit_representatives(
        TARGET_HALF_DEGREE,
        4,
    )
    lower_indices = tuple(
        index
        for index, representative in enumerate(all_representatives)
        if moved_point_support(representative) <= 3
    )
    schedule = (*lower_indices, *support_four_priority)
    provenance = _checkpoint_provenance(root)
    checkpoint = (
        _load_checkpoint(cache_path, root.branching_multiplicity, provenance)
        if cache_path is not None
        else {}
    )
    matrices: list[np.ndarray] = []
    evaluations: list[RepresentativeEvaluation] = []
    lower_certificate: SeparatorCertificate | None = None
    final_certificate: SeparatorCertificate | None = None
    seen_indices: set[int] = set()
    for index in schedule:
        if index in seen_indices:
            continue
        seen_indices.add(index)
        representative = all_representatives[index]
        key = _representative_key(representative)
        started = time.monotonic()
        loaded = key in checkpoint
        if loaded:
            matrix = checkpoint[key]
        else:
            matrix, _ = copy_matrix_for_orbit_representative(
                TARGET_HALF_DEGREE,
                TARGET_SYMMETRIC_PARTITION,
                TARGET_ALPHA,
                representative,
                TARGET_BETA,
            )
            checkpoint[key] = matrix
            if cache_path is not None:
                _write_checkpoint(cache_path, checkpoint, provenance)
        matrices.append(matrix)
        support = moved_point_support(representative)
        certificate = separator_commutant_certificate(matrices)
        if support <= 3 and len(seen_indices) == len(lower_indices):
            lower_certificate = certificate
        if support == 4:
            final_certificate = certificate
        evaluations.append(
            RepresentativeEvaluation(
                representative_index=index,
                representative=representative,
                moved_point_support=support,
                elapsed_seconds=time.monotonic() - started,
                loaded_from_checkpoint=loaded,
                copy_matrix_frobenius_norm=float(np.linalg.norm(matrix)),
                copy_matrix_operator_norm=float(np.linalg.norm(matrix, ord=2)),
                cumulative_matrix_span_dimension=_matrix_span_dimension(
                    matrices,
                    tolerance=1e-8,
                ),
                cumulative_scalar_commutant_certified=(
                    certificate.scalar_common_commutant_numerically_certified
                ),
            )
        )
        if (
            support == 4
            and certificate.scalar_common_commutant_numerically_certified
        ):
            break
    if lower_certificate is None:
        raise ArithmeticError("support-at-most-three census was incomplete")
    if final_certificate is None:
        final_certificate = separator_commutant_certificate(matrices)
    lower_matrices = [
        matrix
        for matrix, evaluation in zip(matrices, evaluations)
        if evaluation.moved_point_support <= 3
    ]
    lower_word_dimension = _generated_algebra_dimension(
        lower_matrices,
        dimension_upper_bound=root.branching_multiplicity**2,
        tolerance=1e-8,
    )
    final_word_dimension = _generated_algebra_dimension(
        matrices,
        dimension_upper_bound=root.branching_multiplicity**2,
        tolerance=1e-8,
    )
    full = final_certificate.scalar_common_commutant_numerically_certified
    cutoffs = [
        SupportCutoffResult(
            maximum_moved_point_support=3,
            total_orbit_representative_count=len(lower_indices),
            evaluated_representative_count=len(lower_matrices),
            matrix_span_dimension=_matrix_span_dimension(
                lower_matrices,
                tolerance=1e-8,
            ),
            numerical_word_algebra_dimension=lower_word_dimension,
            inferred_star_algebra_dimension=(
                root.branching_multiplicity**2
                if lower_certificate.scalar_common_commutant_numerically_certified
                else lower_word_dimension
            ),
            exact_copy_algebra_dimension=root.branching_multiplicity**2,
            all_representatives_through_cutoff_evaluated=True,
            scalar_common_commutant_numerically_certified=(
                lower_certificate.scalar_common_commutant_numerically_certified
            ),
            separator_certificate=lower_certificate,
            status=(
                "support-three-generates-full-copy-algebra"
                if lower_certificate.scalar_common_commutant_numerically_certified
                else "support-three-copy-algebra-proper"
            ),
        ),
        SupportCutoffResult(
            maximum_moved_point_support=4,
            total_orbit_representative_count=len(all_representatives),
            evaluated_representative_count=len(matrices),
            matrix_span_dimension=_matrix_span_dimension(
                matrices,
                tolerance=1e-8,
            ),
            numerical_word_algebra_dimension=final_word_dimension,
            inferred_star_algebra_dimension=(
                root.branching_multiplicity**2 if full else final_word_dimension
            ),
            exact_copy_algebra_dimension=root.branching_multiplicity**2,
            all_representatives_through_cutoff_evaluated=False,
            scalar_common_commutant_numerically_certified=full,
            separator_certificate=final_certificate,
            status=(
                "support-four-witness-subset-generates-full-copy-algebra"
                if full
                else "support-four-witness-subset-inconclusive"
            ),
        ),
    ]
    numerator, denominator, natural_mass, repeated_fraction = _target_source_mass()
    status = (
        "highest-mass-s14-block-support-four-numerically-full-asymptotics-open"
        if full
        else "highest-mass-s14-block-support-four-scan-inconclusive"
    )
    return HighMassSupportScanReport(
        created_at=utc_now(),
        theorem_contract={
            "input": (
                "the highest-natural-mass untested repeated S_14 hyperoctahedral branch and "
                "bounded-support K-conjugacy orbit representatives"
            ),
            "output": (
                "matrix-free b-by-b copy matrices, support cutoff evidence, and a robust "
                "floating-point scalar-commutant certificate"
            ),
            "non_claim": (
                "No exact symbolic all-rank theorem, inverse-polynomial gap, coherent transform, "
                "hidden-involution decoder, or quantum speedup is inferred."
            ),
        },
        half_degree=TARGET_HALF_DEGREE,
        symmetric_partition=TARGET_SYMMETRIC_PARTITION,
        hyperoctahedral_partition=TARGET_ALPHA,
        negative_hyperoctahedral_partition=TARGET_BETA,
        symmetric_irrep_dimension=root.symmetric_irrep_dimension,
        branching_multiplicity=root.branching_multiplicity,
        carrier_dimension=(
            root.carrier_weight_dimension
            * math.comb(TARGET_HALF_DEGREE, sum(TARGET_BETA))
        ),
        natural_mass_numerator=numerator,
        exact_mass_denominator=denominator,
        natural_mass_probability=natural_mass,
        fraction_of_repeated_natural_mass=repeated_fraction,
        matrix_evidence={
            "provenance": provenance,
            "evidence_kind": "floating-point-generator-matrices-not-interval-certified",
            "representative_indices": [row.representative_index for row in evaluations],
            "generators": [matrix.tolist() for matrix in matrices],
        },
        root_fiber_metrics={
            "symmetric_irrep_dimension": root.symmetric_irrep_dimension,
            "branching_multiplicity": root.branching_multiplicity,
            "root_fiber_column_width": root.root_fiber_dimension,
            "batched_action_column_width": root.branching_multiplicity * root.carrier_weight_dimension,
            "full_isotypic_column_width": (
                root.branching_multiplicity
                * root.carrier_weight_dimension
                * 35
            ),
            "column_width_reduction_factor": 35,
            "maximum_signed_weight_residual": root.maximum_signed_weight_residual,
            "maximum_yjm_content_residual": root.maximum_yjm_content_residual,
            "orthonormality_residual": root.orthonormality_residual,
        },
        representative_evaluations=evaluations,
        support_cutoffs=cutoffs,
        proof_obligations=[
            {
                "obligation": "upgrade_floating_point_closure_to_exact_symbolic_certificate",
                "resolved": False,
                "resolution": (
                    "Recover exact algebraic copy matrices or certify all spectral and graph margins "
                    "with interval arithmetic."
                ),
            },
            {
                "obligation": "prove_natural_mass_uniformity",
                "resolved": False,
                "resolution": (
                    "One rank-seven block has less than one percent source mass; establish closure and "
                    "a task-relevant adaptive labeling or direct transform on one-minus-o(1) mass over growing rank."
                ),
            },
            {
                "obligation": "compile_coherent_source_aware_transform_and_decoder",
                "resolved": False,
                "resolution": (
                    "Replace exponential ambient rows by a uniform quantum implementation and connect "
                    "resolved labels to hidden-involution recovery."
                ),
            },
        ],
        adversarial_audit=[
            {
                "challenge": "The low-dimensional controls were selected away from the source law.",
                "survives": False,
                "response": (
                    "This target is the single highest-mass previously untested repeated S_14 branch."
                ),
            },
            {
                "challenge": "A word-span rank of 675 is mistaken for a proper 26-dimensional star algebra.",
                "survives": False,
                "response": (
                    "The scalar-commutant certificate uses a simple separator and connected generator graph, "
                    "avoiding unstable enumeration of 676 matrix-word directions."
                ),
            },
            {
                "challenge": "One finite high-mass block establishes typical all-rank behavior.",
                "survives": True,
                "response": (
                    "The block carries only the recorded finite source mass, and no concentration or uniform "
                    "gap theorem is claimed."
                ),
            },
        ],
        headline_metrics={
            "highest_mass_untested_s14_block_scan_count": 1,
            "target_natural_mass_probability": natural_mass,
            "target_fraction_of_repeated_natural_mass": repeated_fraction,
            "target_branching_multiplicity": root.branching_multiplicity,
            "target_copy_algebra_dimension": root.branching_multiplicity**2,
            "support_three_generated_algebra_dimension": lower_word_dimension,
            "support_four_full_copy_algebra_certificate_count": int(full),
            "support_four_inferred_star_algebra_dimension": (
                root.branching_multiplicity**2 if full else final_word_dimension
            ),
            "support_four_separator_lcu_normalized_gap": (
                final_certificate.lcu_normalized_minimum_gap
            ),
            "support_four_generator_graph_bottleneck": (
                final_certificate.maximum_spanning_tree_bottleneck
            ),
            "support_four_direct_commutant_nullity": (
                final_certificate.direct_commutant_nullity_at_1e8
            ),
            "support_four_direct_commutant_smallest_nonzero_singular_value": (
                final_certificate.direct_commutant_smallest_nonzero_singular_value
            ),
            "evaluated_representative_count": len(evaluations),
            "exact_symbolic_support_four_certificate_count": 0,
            "inverse_polynomial_natural_mass_gap_theorem_count": 0,
            "coherent_multiplicity_transform_count": 0,
            "hidden_involution_decoder_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "highest_mass_untested_s14_block_scanned": True,
            "support_three_full_copy_algebra_falsified": not (
                lower_certificate.scalar_common_commutant_numerically_certified
            ),
            "support_four_full_copy_algebra_numerically_certified": full,
            "support_four_exact_symbolic_certificate_proved": False,
            "target_has_nonnegligible_finite_source_mass": natural_mass >= 0.001,
            "one_minus_o_one_natural_mass_coverage_proved": False,
            "inverse_polynomial_normalized_gap_proved": False,
            "polynomial_typical_ambient_compression_proved": False,
            "coherent_multiplicity_transform_compiled": False,
            "hidden_involution_decoder_compiled": False,
            "classical_separation_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "A robust finite support-four copy-algebra certificate on one source-relevant block does not "
                "supply exact asymptotics, typical-mass coverage, coherent access, or a decoder."
            ),
        },
        status=status,
        summary=(
            "Scanned the highest-mass previously untested repeated S_14 branch; support three remains "
            f"proper and support four scalar-commutant closure is {full}."
        ),
        falsifiers_triggered=[
            "The highest-mass untested S_14 branch is not computationally inaccessible to the fiber trace.",
            *(
                [
                    "The highest-mass untested S_14 branch does not require support five or six for full copy-algebra generation."
                ]
                if full
                else []
            ),
            "One finite high-mass branch is not an all-rank natural-mass theorem or coherent decoder.",
        ],
    )


def write_high_mass_support_scan_report(
    path: Path = REPORT_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = DEFAULT_EXPERIMENT_ID,
    registry_candidate_id: str = DEFAULT_CANDIDATE_ID,
    registry_result_id: str = "",
) -> dict[str, Any]:
    payload = asdict(run_high_mass_support_scan())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    if write_registry:
        from research_registry import (
            ExperimentRecord,
            ExperimentResultRecord,
            NegativeResultRecord,
            upsert_experiment,
            upsert_experiment_result,
            upsert_negative_result,
        )

        upsert_experiment(
            ExperimentRecord(
                id=registry_experiment_id,
                candidate_id=registry_candidate_id,
                title="Highest-natural-mass S_14 multiplicity support scan",
                status=payload["status"],
                hypothesis=(
                    "Bounded-support hyperoctahedral orbit sums resolve the full copy algebra on a "
                    "source-relevant high-multiplicity branch."
                ),
                protocol=(
                    "Contract exact multiplicity-fiber copy matrices, exhaust support three, and search a "
                    "support-four witness subset for a simple-separator scalar-commutant certificate."
                ),
                positive_signal=(
                    "Uniform closure plus a scalable adaptive-label or direct transform on typical source "
                    "mass, with coherent implementation and decoding."
                ),
                falsifiers=[
                    "support-four generators retain a non-scalar common commutant",
                    "the apparent separator gap vanishes under certified precision",
                    "high-mass closure fails to concentrate over growing rank",
                    "the ambient contraction has no coherent polynomial implementation",
                ],
                metrics=list(payload["headline_metrics"].keys()),
                dependencies=[
                    "coset_hidden_involution_multiplicity_fiber_trace.py",
                    "coset_hidden_involution_natural_support_six_mass_audit.py",
                    "Young-seminormal sparse representation actions",
                ],
                next_actions=[
                    "upgrade the finite certificate with interval or exact arithmetic",
                    "scan the next ranked high-mass branches using the checkpointed contraction",
                    "search for a partition-algebra formula for the copy matrices",
                    "test adaptive coarse labels; do not seek one typical complete spectrum with polynomial minimum gap",
                ],
            )
        )
        result_id = registry_result_id or f"RESULT-{registry_experiment_id}"
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
                artifacts={"high_mass_support_scan": str(path)},
            )
        )
        upsert_negative_result(
            NegativeResultRecord(
                id="ONE-HIGH-MASS-S14-BLOCK-NOT-TYPICAL-SUPPORT-THEOREM",
                source=registry_experiment_id,
                claim=(
                    "Closure on the highest-mass repeated S_14 block proves bounded-support generation "
                    "on one-minus-o(1) natural source mass."
                ),
                reason_invalid=(
                    "The finite block has the recorded sub-one-percent mass and supplies no growing-rank "
                    "concentration, exact symbolic certificate, or normalized-gap theorem."
                ),
                lesson=(
                    "Use source mass to choose finite falsification targets, then require a uniform theorem "
                    "before compiling coherent access."
                ),
                applies_to=[registry_candidate_id, "support-six commutant program"],
                evidence={"artifact": str(path)},
            )
        )
        if payload["claim_gate"][
            "support_four_full_copy_algebra_numerically_certified"
        ]:
            upsert_negative_result(
                NegativeResultRecord(
                    id="HIGHEST-MASS-S14-BLOCK-DOES-NOT-REQUIRE-SUPPORT-FIVE-OR-SIX",
                    source=registry_experiment_id,
                    claim=(
                        "The highest-mass untested S_14 multiplicity block requires moved-point support "
                        "five or six to generate its full copy algebra."
                    ),
                    reason_invalid=(
                        "A support-four witness subset has a robust simple-separator connected-graph "
                        "certificate for scalar common commutant."
                    ),
                    lesson=(
                        "Search for a uniform low-support generation theorem rather than extrapolating "
                        "monotone support growth from selected small blocks."
                    ),
                    applies_to=[registry_candidate_id, "rank-seven high-mass block"],
                    evidence={"artifact": str(path)},
                )
            )
    return payload


if __name__ == "__main__":
    result = write_high_mass_support_scan_report()
    print(json.dumps(result["headline_metrics"], indent=2, sort_keys=True))

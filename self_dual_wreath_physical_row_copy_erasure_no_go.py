"""Native-state no-go for one-pass erasure after physical row-copy.

The physical PGM intertwiner supplies a coherent generalized-Fourier row-copy
map.  This module identifies its exact range and proves that the obvious
one-pass branch-erasure continuation still has superpolynomial cost.

Fix an isotypic label ``nu`` and Fourier row ``a``.  If the aligned physical
restriction is ``U=direct_sum_e sigma_e``, generalized Fourier row-copy gives a
partial isometry ``C_(nu,a)``.  Its output in orientation ``e`` lies in

    E_e = Inv(V_nu tensor sigma_e).

The multiplicity of ``nu`` in ``U`` is the sum of its multiplicities in the
``sigma_e``.  Containment plus this dimension identity gives the exact range

    C_(nu,a) C_(nu,a)^* = direct_sum_e E_e.              (1)

Thus row-copy fills the entire direct sum of active orientation ranges; it is
not itself the narrow diagonal correlation that would make a Walsh erasure
deterministic.

Put

    R x = sum_e |e>E_e x,       A=R^*R=sum_e E_e,
    N=Tr(A)=sum_e rank(E_e),    Q=polar(R).

For the physical average state restricted to its support, row-copy produces
exactly the native polar-image state

    tau = R R^*/N = Q A Q^*/N.                             (2)

Consider one-pass erasure: arbitrary branch-controlled carrier unitaries,
then a branch-only unitary with selected row ``f``, then one retained output
branch.  Let ``L`` be its Kraus map, ``r_max=max_e rank(E_e)``, and

    m2 = Tr(A^2)/N.

If ``K=direct_sum_e ran(E_e)`` and ``P_M=supp(tau)``, then

    Tr(P_M L^*L) <= Tr(P_K L^*L)
                  = sum_e |f_e|^2 rank(E_e) <= r_max.      (3)

Splitting (2) at an arbitrary eigenvalue threshold ``B>0`` gives

    Pr[accept] <= B r_max/N + m2/B.

Optimizing ``B`` proves the exact native bound

    Pr[accept] <= 2 sqrt(m2 r_max/N).                       (4)

For a fixed-arity early child with ``q`` orientations, the repository's
uniform orientation-rank theorem gives ``r_max/N=(1+o(1))/q`` simultaneously.
The exact natural second-moment identity, Markov, and a union bound over a
fixed number of children and all partition targets give
``m2<=exp(O(sqrt(n))) poly(n)`` with high probability.  Since
``q=2^(ceil(log2(n!))+O(1))/R`` for fixed ``R``, equation (4) is
``exp(-Omega(n log n))``.  Even amplitude amplification remains
superpolynomial.

The no-go is scoped to one-pass block-diagonal carrier processing followed by
one branch-only erasure row (or any subfactorial number of retained rows).  It
does not rule out a multi-round transform that coherently relocates the
orientation index, exploits cross-branch representation actions, or retains
the branch character as part of a different final decoder.  It also does not
invalidate the physical interference filter, which intentionally accepts a
linear fraction of characters rather than erasing them.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import numpy as np

from representation_obstruction import hook_length_dimension
from research_registry import utc_now
from self_dual_wreath_orientation_fourier_reduction import (
    orientation_invariant_projector,
)
from self_dual_wreath_physical_pgm_intertwiner import (
    _branch_representation_rows,
    _fourier_offsets,
    _orientation_order_sector_row,
    _sector_row_block,
    generalized_fourier_row_copy_isometry,
)


REPORT_PATH = Path(
    "research/representation/self_dual_wreath_physical_row_copy_erasure_no_go.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-PHYSICAL-ROW-COPY-ERASURE-NO-GO"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"

Partition = tuple[int, ...]
Label = tuple[Partition, Partition]


@dataclass(frozen=True)
class RowCopyRangeControl:
    control_id: str
    n: int
    labels: tuple[Label, ...]
    orientation_count: int
    active_sector_row_count: int
    inactive_sector_row_count: int
    maximum_range_projector_residual: float
    maximum_range_rank_residual: int
    maximum_invariant_range_leakage: float
    exact_full_direct_sum_range_verified: bool
    status: str


@dataclass(frozen=True)
class NativeRowErasureControl:
    control_id: str
    ambient_dimension: int
    branch_count: int
    branch_ranks: tuple[int, ...]
    total_coefficient_rank: int
    frame_rank: int
    maximum_branch_rank: int
    frame_second_moment_per_trace: float
    exact_acceptance_probability: float
    optimized_acceptance_upper_bound: float
    optimizing_spectral_threshold: float
    row_copy_native_state_identity_residual: float
    support_trace_budget: float
    support_trace_budget_upper_bound: float
    native_one_pass_bound_verified: bool
    status: str


@dataclass(frozen=True)
class NaturalRowErasureScalingRecord:
    n: int
    group_order_log2: float
    information_threshold_copy_count: int
    fixed_jump_log2_arity: int
    early_child_orientation_log2: int
    early_child_aspect: float
    partition_count_log2_upper_bound: float
    simultaneous_second_moment_markov_factor_log2: float
    rank_relative_error: float
    one_pass_native_success_log2_upper_bound: float
    amplitude_amplification_query_log2_lower_bound: float
    polynomial_benchmark_log2: float
    rank_concentration_dependency: str
    second_moment_dependency: str
    one_pass_native_erasure_superpolynomial: bool
    multi_round_source_adapted_transform_ruled_out: bool
    status: str


@dataclass(frozen=True)
class PhysicalRowCopyErasureTheorem:
    row_copy_range: str
    physical_native_state: str
    trace_budget: str
    spectral_split: str
    natural_transfer: str
    scope: str
    theorem_verified: bool
    status: str


@dataclass(frozen=True)
class PhysicalRowCopyErasureNoGoReport:
    created_at: str
    theorem_contract: dict[str, Any]
    theorem: PhysicalRowCopyErasureTheorem
    row_copy_controls: list[RowCopyRangeControl]
    native_erasure_controls: list[NativeRowErasureControl]
    scaling_records: list[NaturalRowErasureScalingRecord]
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _block_diagonal(matrices: tuple[np.ndarray, ...]) -> np.ndarray:
    total = sum(matrix.shape[0] for matrix in matrices)
    output = np.zeros((total, total), dtype=complex)
    offset = 0
    for matrix in matrices:
        width = matrix.shape[0]
        output[offset : offset + width, offset : offset + width] = matrix
        offset += width
    return output


def audit_row_copy_range(
    n: int,
    labels: tuple[Label, ...],
    *,
    control_id: str,
    tolerance: float = 1e-9,
) -> RowCopyRangeControl:
    if not labels:
        raise ValueError("at least one source label is required")
    orientation_count = 1 << len(labels)
    carrier_dimension = math.prod(
        hook_length_dimension(left) * hook_length_dimension(right)
        for left, right in labels
    )
    row_copy, _, partitions = generalized_fourier_row_copy_isometry(
        n,
        _branch_representation_rows(labels),
    )
    offsets = _fourier_offsets(n)
    active = 0
    inactive = 0
    maximum_projector_residual = 0.0
    maximum_rank_residual = 0
    maximum_leakage = 0.0
    for partition in partitions:
        dimension = hook_length_dimension(partition)
        projectors = tuple(
            orientation_invariant_projector(partition, labels, orientation)
            for orientation in range(orientation_count)
        )
        range_projector = _block_diagonal(projectors)
        expected_rank = sum(
            int(round(float(np.trace(projector).real)))
            for projector in projectors
        )
        for row_index in range(dimension):
            sector = _sector_row_block(
                row_copy,
                group_offset=offsets[partition],
                irrep_dimension=dimension,
                row_index=row_index,
                residual_dimension=orientation_count * carrier_dimension,
            )
            oriented = _orientation_order_sector_row(
                sector,
                orientation_count=orientation_count,
                irrep_dimension=dimension,
                carrier_dimension=carrier_dimension,
            )
            image = oriented @ oriented.conj().T
            numerical_rank = int(
                np.count_nonzero(np.linalg.svd(oriented, compute_uv=False) > 100 * tolerance)
            )
            residual = float(np.linalg.norm(image - range_projector, ord=2))
            leakage = float(
                np.linalg.norm(
                    (np.eye(len(range_projector)) - range_projector) @ oriented,
                    ord=2,
                )
            )
            maximum_projector_residual = max(maximum_projector_residual, residual)
            maximum_rank_residual = max(
                maximum_rank_residual,
                abs(numerical_rank - expected_rank),
            )
            maximum_leakage = max(maximum_leakage, leakage)
            if expected_rank:
                active += 1
            else:
                inactive += 1
    verified = bool(
        active
        and maximum_projector_residual <= 1000 * tolerance
        and maximum_rank_residual == 0
        and maximum_leakage <= 1000 * tolerance
    )
    return RowCopyRangeControl(
        control_id=control_id,
        n=n,
        labels=labels,
        orientation_count=orientation_count,
        active_sector_row_count=active,
        inactive_sector_row_count=inactive,
        maximum_range_projector_residual=maximum_projector_residual,
        maximum_range_rank_residual=maximum_rank_residual,
        maximum_invariant_range_leakage=maximum_leakage,
        exact_full_direct_sum_range_verified=verified,
        status=(
            "physical-row-copy-range-equals-orientation-direct-sum"
            if verified
            else "physical-row-copy-range-control-failure"
        ),
    )


def _hermitian(matrix: np.ndarray) -> np.ndarray:
    return (matrix + matrix.conj().T) / 2.0


def _support_projector(matrix: np.ndarray, tolerance: float) -> np.ndarray:
    values, vectors = np.linalg.eigh(_hermitian(matrix))
    active = values > 100 * tolerance
    return vectors[:, active] @ vectors[:, active].conj().T


def _polar_factor(matrix: np.ndarray, tolerance: float) -> np.ndarray:
    gram = _hermitian(matrix.conj().T @ matrix)
    values, vectors = np.linalg.eigh(gram)
    inverse = np.zeros_like(values)
    active = values > 100 * tolerance
    inverse[active] = values[active] ** -0.5
    return matrix @ ((vectors * inverse) @ vectors.conj().T)


def _validate_projectors(
    projectors: tuple[np.ndarray, ...],
    tolerance: float,
) -> int:
    if len(projectors) < 2:
        raise ValueError("at least two orientation projectors are required")
    dimension = projectors[0].shape[0]
    if any(projector.shape != (dimension, dimension) for projector in projectors):
        raise ValueError("orientation projectors must share one square space")
    for projector in projectors:
        if max(
            np.linalg.norm(projector - projector.conj().T, ord=2),
            np.linalg.norm(projector @ projector - projector, ord=2),
        ) > 1000 * tolerance:
            raise ValueError("orientation effects must be projections")
    return dimension


def audit_native_row_erasure(
    control_id: str,
    projectors: tuple[np.ndarray, ...],
    branch_row: tuple[complex, ...],
    *,
    block_unitaries: tuple[np.ndarray, ...] | None = None,
    tolerance: float = 1e-9,
) -> NativeRowErasureControl:
    dimension = _validate_projectors(projectors, tolerance)
    count = len(projectors)
    row = np.asarray(branch_row, dtype=complex)
    if row.shape != (count,) or abs(float(np.linalg.norm(row)) - 1.0) > 100 * tolerance:
        raise ValueError("branch row must be a normalized vector of matching width")
    if block_unitaries is None:
        block_unitaries = tuple(np.eye(dimension, dtype=complex) for _ in range(count))
    if len(block_unitaries) != count:
        raise ValueError("one block unitary is required per orientation")
    for unitary in block_unitaries:
        if unitary.shape != (dimension, dimension) or np.linalg.norm(
            unitary.conj().T @ unitary - np.eye(dimension), ord=2
        ) > 1000 * tolerance:
            raise ValueError("carrier blocks must be unitary")

    analysis = np.vstack(projectors)
    frame = _hermitian(analysis.conj().T @ analysis)
    total = float(np.trace(frame).real)
    if total <= tolerance:
        raise ValueError("orientation frame must have positive trace")
    polar = _polar_factor(analysis, tolerance)
    native_from_polar = polar @ frame @ polar.conj().T / total
    native_from_row_copy = analysis @ analysis.conj().T / total
    native_identity = float(
        np.linalg.norm(native_from_polar - native_from_row_copy, ord=2)
    )
    eraser = np.hstack(
        tuple(row[index] * block_unitaries[index] for index in range(count))
    )
    success = float(
        np.trace(eraser @ native_from_row_copy @ eraser.conj().T).real
    )
    support = polar @ polar.conj().T
    support_budget = float(np.trace(support @ eraser.conj().T @ eraser).real)
    ranks = tuple(int(round(float(np.trace(projector).real))) for projector in projectors)
    maximum_rank = max(ranks)
    budget_upper = float(sum(abs(row[index]) ** 2 * ranks[index] for index in range(count)))
    second_per_trace = float(np.trace(frame @ frame).real / total)
    threshold = math.sqrt(second_per_trace * total / maximum_rank)
    raw_bound = 2.0 * math.sqrt(second_per_trace * maximum_rank / total)
    bound = min(1.0, raw_bound)
    frame_rank = int(round(float(np.trace(_support_projector(frame, tolerance)).real)))
    verified = bool(
        native_identity <= 1000 * tolerance
        and support_budget <= budget_upper + 1000 * tolerance
        and budget_upper <= maximum_rank + 1000 * tolerance
        and success <= bound + 1000 * tolerance
    )
    return NativeRowErasureControl(
        control_id=control_id,
        ambient_dimension=dimension,
        branch_count=count,
        branch_ranks=ranks,
        total_coefficient_rank=int(round(total)),
        frame_rank=frame_rank,
        maximum_branch_rank=maximum_rank,
        frame_second_moment_per_trace=second_per_trace,
        exact_acceptance_probability=success,
        optimized_acceptance_upper_bound=bound,
        optimizing_spectral_threshold=threshold,
        row_copy_native_state_identity_residual=native_identity,
        support_trace_budget=support_budget,
        support_trace_budget_upper_bound=budget_upper,
        native_one_pass_bound_verified=verified,
        status=(
            "native-row-copy-one-pass-erasure-bound-verified"
            if verified
            else "native-row-erasure-control-failure"
        ),
    )


def _partition_count_log2_upper_bound(n: int) -> float:
    return math.pi * math.sqrt(2.0 * n / 3.0) / math.log(2.0)


def natural_row_erasure_scaling_record(
    n: int,
    *,
    fixed_jump_log2_arity: int = 24,
    extra_copies: int = 2,
    markov_power: int = 4,
    rank_relative_error: float = 0.5,
    polynomial_benchmark_degree: int = 10,
) -> NaturalRowErasureScalingRecord:
    if n < 8 or fixed_jump_log2_arity < 3 or extra_copies < 0:
        raise ValueError("invalid scaling parameters")
    if not 0 < rank_relative_error < 1 or markov_power < 1:
        raise ValueError("invalid concentration parameters")
    log_order = math.lgamma(n + 1) / math.log(2.0)
    copies = math.ceil(log_order) + extra_copies
    if copies <= fixed_jump_log2_arity:
        raise ValueError("fixed jump consumes the entire orientation register")
    child_log2 = copies - fixed_jump_log2_arity
    alpha = math.exp2(child_log2 - log_order)
    partition_log = _partition_count_log2_upper_bound(n)
    # Union-bound Markov over all partition targets and the fixed R children.
    markov_log = (
        fixed_jump_log2_arity
        + partition_log
        + markov_power * math.log2(n)
    )
    h = math.exp2(-log_order) if log_order < 1074 else 0.0
    moment_ratio_log = (
        markov_log
        + math.log2((1.0 - h + alpha) / (1.0 - rank_relative_error))
    )
    rank_ratio_log = (
        math.log2((1.0 + rank_relative_error) / (1.0 - rank_relative_error))
        - child_log2
    )
    raw_success_log = 1.0 + 0.5 * (moment_ratio_log + rank_ratio_log)
    success_log = min(0.0, raw_success_log)
    amplification_log = max(0.0, -success_log / 2.0)
    benchmark = polynomial_benchmark_degree * math.log2(n)
    separated = amplification_log > benchmark
    return NaturalRowErasureScalingRecord(
        n=n,
        group_order_log2=log_order,
        information_threshold_copy_count=copies,
        fixed_jump_log2_arity=fixed_jump_log2_arity,
        early_child_orientation_log2=child_log2,
        early_child_aspect=alpha,
        partition_count_log2_upper_bound=partition_log,
        simultaneous_second_moment_markov_factor_log2=markov_log,
        rank_relative_error=rank_relative_error,
        one_pass_native_success_log2_upper_bound=success_log,
        amplitude_amplification_query_log2_lower_bound=amplification_log,
        polynomial_benchmark_log2=benchmark,
        rank_concentration_dependency=(
            "existing simultaneous all-orientation/all-target Plancherel rank concentration, after global-distinct conditioning"
        ),
        second_moment_dependency=(
            "existing exact sparse-frame second moment plus Markov and a union bound over fixed-R children and partition targets"
        ),
        one_pass_native_erasure_superpolynomial=separated,
        multi_round_source_adapted_transform_ruled_out=False,
        status=(
            "natural-native-one-pass-erasure-superpolynomial"
            if separated
            else "finite-size-native-erasure-separation-not-visible"
        ),
    )


def _random_projector(
    dimension: int,
    rank: int,
    rng: np.random.Generator,
) -> np.ndarray:
    raw = rng.normal(size=(dimension, rank)) + 1j * rng.normal(size=(dimension, rank))
    basis, _ = np.linalg.qr(raw)
    return basis @ basis.conj().T


def _random_unitary(dimension: int, rng: np.random.Generator) -> np.ndarray:
    raw = rng.normal(size=(dimension, dimension)) + 1j * rng.normal(
        size=(dimension, dimension)
    )
    basis, diagonal = np.linalg.qr(raw)
    phases = np.diag(diagonal)
    phases = np.where(np.abs(phases) > 0, phases / np.abs(phases), 1.0)
    return basis @ np.diag(phases.conj())


def _walsh_row(branch_count: int, character: int = 0) -> tuple[complex, ...]:
    if branch_count < 2 or branch_count & (branch_count - 1):
        raise ValueError("branch_count must be a power of two")
    values = []
    for orientation in range(branch_count):
        sign = -1.0 if (orientation & character).bit_count() % 2 else 1.0
        values.append(sign / math.sqrt(branch_count))
    return tuple(values)


def _finite_native_controls() -> list[NativeRowErasureControl]:
    rng = np.random.default_rng(8112026)
    controls = []
    for index, (dimension, count, rank) in enumerate(
        ((16, 4, 2), (24, 4, 3), (32, 8, 2), (48, 8, 3))
    ):
        projectors = tuple(
            _random_projector(dimension, rank, rng) for _ in range(count)
        )
        controls.append(
            audit_native_row_erasure(
                f"RANDOM-{index}-IDENTITY",
                projectors,
                _walsh_row(count, character=index % count),
            )
        )
        controls.append(
            audit_native_row_erasure(
                f"RANDOM-{index}-CONTROLLED",
                projectors,
                _walsh_row(count, character=(index + 1) % count),
                block_unitaries=tuple(
                    _random_unitary(dimension, rng) for _ in range(count)
                ),
            )
        )
    return controls


def run_physical_row_copy_erasure_no_go() -> PhysicalRowCopyErasureNoGoReport:
    row_copy_controls = [
        audit_row_copy_range(
            3,
            (((3,), (2, 1)),),
            control_id="W3-SINGLE-UNEQUAL",
        ),
        audit_row_copy_range(
            3,
            (
                ((3,), (2, 1)),
                ((3,), (1, 1, 1)),
                ((2, 1), (1, 1, 1)),
            ),
            control_id="W3-COLLISION-FREE-THRESHOLD",
        ),
        audit_row_copy_range(
            4,
            (
                ((4,), (3, 1)),
                ((2, 2), (2, 1, 1)),
            ),
            control_id="W4-COLLISION-FREE-PAIR",
        ),
    ]
    native_controls = _finite_native_controls()
    scaling = [
        natural_row_erasure_scaling_record(n)
        for n in (16, 20, 24, 32, 40, 48, 64, 80, 96, 128)
    ]
    failures = sum(
        not row.exact_full_direct_sum_range_verified for row in row_copy_controls
    ) + sum(not row.native_one_pass_bound_verified for row in native_controls)
    separated = [
        row for row in scaling if row.one_pass_native_erasure_superpolynomial
    ]
    verified = bool(not failures and separated)
    theorem = PhysicalRowCopyErasureTheorem(
        row_copy_range=(
            "For every nu and Fourier row a, C_(nu,a)C_(nu,a)^*=direct_sum_e E_(nu,e); containment is upgraded to equality by multiplicity additivity."
        ),
        physical_native_state=(
            "Under row-copy, the normalized physical average on its support is tau=RR^*/Tr(A)=Q A Q^*/Tr(A)."
        ),
        trace_budget=(
            "For any one-pass selected branch row, Tr(supp(tau)L^*L)<=sum_e |f_e|^2 rank(E_e)<=r_max."
        ),
        spectral_split=(
            "Thresholding A at B gives p<=B r_max/N+[Tr(A^2)/N]/B, hence p<=2 sqrt((Tr(A^2)/N) r_max/N)."
        ),
        natural_transfer=(
            "Uniform orientation-rank concentration and the exact sparse second moment make the bound exp(-Omega(n log n)) for every fixed-R early child, simultaneously after a subfactorial union bound."
        ),
        scope=(
            "Only one-pass block-controlled carrier operations followed by a branch-only erasure row are excluded. Multi-round source-adapted transforms and decoders retaining branch characters remain open."
        ),
        theorem_verified=verified,
        status=(
            "physical-row-copy-one-pass-erasure-refuted"
            if verified
            else "physical-row-copy-erasure-control-failure"
        ),
    )
    return PhysicalRowCopyErasureNoGoReport(
        created_at=utc_now(),
        theorem_contract=asdict(theorem),
        theorem=theorem,
        row_copy_controls=row_copy_controls,
        native_erasure_controls=native_controls,
        scaling_records=scaling,
        proof_obligations=[
            {
                "obligation": "determine_fixed_row_physical_row_copy_range",
                "resolved": verified,
                "resolution": "The range is exactly the full direct sum of active orientation invariant ranges, not merely contained in it.",
            },
            {
                "obligation": "test_one_pass_branch_erasure_on_actual_native_support",
                "resolved": verified,
                "resolution": "The trace-budget and spectral-split theorem applies directly to tau=RR^*/Tr(A), including arbitrary branch-controlled carrier unitaries.",
            },
            {
                "obligation": "transfer_to_natural_fixed_arity_early_children",
                "resolved": verified,
                "resolution": "Existing uniform rank concentration and exact second moments imply a high-probability subfactorial m2 factor versus factorial q width.",
            },
            {
                "obligation": "construct_multi_round_orientation_index_relocation",
                "resolved": False,
                "resolution": "A surviving circuit must move branch information coherently through carrier/ancilla structure before erasure or avoid erasure in the final decoder.",
            },
            {
                "obligation": "prove_simultaneous_operational_error_for_approximate_pgm",
                "resolved": False,
                "resolution": "The theorem bounds conclusive probability of the one-pass architecture; it does not lower-bound every approximate coherent PGM implementation.",
            },
        ],
        adversarial_audit=[
            {
                "objection": "The row-copy output may already be a diagonal branch correlation that Walsh erases.",
                "resolved": True,
                "resolution": "Equation (1) shows the unrestricted fixed-row image is the entire direct sum; the hidden-state support is ran(Q), whose native density is equation (2).",
            },
            {
                "objection": "A small support codimension could still concentrate all native mass into one character.",
                "resolved": True,
                "resolution": "Equation (4) uses the native eigenvalue distribution through Tr(A^2), not codimension alone.",
            },
            {
                "objection": "Arbitrary branch-controlled carrier unitaries can beat the trace budget.",
                "resolved": True,
                "resolution": "Their Hilbert-Schmidt contribution on branch e remains |f_e|^2 rank(E_e); positivity gives equation (3).",
            },
            {
                "objection": "A union over partition targets destroys the natural asymptotic bound.",
                "resolved": True,
                "resolution": "p(n)=exp(O(sqrt(n))) and fixed R are subfactorial, while q=exp(Theta(n log n)); the gap survives Markov and union bounds.",
            },
            {
                "objection": "This rules out the physical orientation interference filter.",
                "resolved": True,
                "resolution": "That filter keeps q-1 characters (or another linear-rank set) and is not a one-row branch eraser.",
            },
            {
                "objection": "This is an arbitrary-circuit lower bound for the physical PGM.",
                "resolved": False,
                "resolution": "No. Alternating branch/carrier transforms, coherent index relocation, and final decoders that retain orientation characters remain outside the theorem.",
            },
        ],
        headline_metrics={
            "exact_row_copy_full_range_theorem_count": int(verified),
            "native_one_pass_erasure_bound_theorem_count": int(verified),
            "row_copy_control_count": len(row_copy_controls),
            "native_erasure_control_count": len(native_controls),
            "finite_control_failure_count": failures,
            "superpolynomial_scaling_row_count": len(separated),
            "multi_round_orientation_index_relocation_count": 0,
            "physical_orientation_polar_compiler_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "fixed_row_copy_range_equals_full_orientation_direct_sum": verified,
            "physical_native_state_equals_RRstar_over_trace": verified,
            "one_pass_native_erasure_moment_bound_proved": verified,
            "natural_one_pass_erasure_superpolynomial": bool(separated),
            "physical_interference_filter_refuted": False,
            "multi_round_source_adapted_transform_ruled_out": False,
            "branch_character_retaining_decoder_ruled_out": False,
            "arbitrary_physical_orientation_polar_ruled_out": False,
            "physical_orientation_polar_compiled": False,
            "speedup_claim_allowed": False,
        },
        status=theorem.status,
        summary=(
            "The physical row-copy interface fills the full orientation-range direct sum, and its hidden-state support carries native density RR*/Tr(A). A trace-budget plus spectral split proves that every one-pass branch-controlled carrier circuit followed by one branch-erasure row has exp(-Omega(n log n)) success on natural fixed-R early children. Any surviving physical router must be genuinely multi-round or retain branch characters in a different coherent decoder."
        ),
        falsifiers_triggered=[
            "Physical row-copy is not by itself the correlated diagonal embedding needed for deterministic Walsh erasure.",
            "Native-state weighting does not rescue one-pass erasure once rank balance and the second moment are charged.",
            "The direct physical route remains open only beyond the one-pass block-controlled/branch-only architecture.",
        ],
    )


def write_physical_row_copy_erasure_no_go_report(
    path: Path = REPORT_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = (
        "EXP-CODE-SELF-DUAL-WREATH-PHYSICAL-ROW-COPY-ERASURE-NO-GO"
    ),
    registry_candidate_id: str = "CODE-COSET-COLLECTIVE",
    registry_result_id: str = "",
    **kwargs: Any,
) -> dict[str, Any]:
    output_path = path
    for _k in ("write_registry", "registry_experiment_id", "registry_candidate_id", "registry_result_id"):
        kwargs.pop(_k, None)
    if "run_physical_row_copy_erasure_no_go" in globals():
        report = run_physical_row_copy_erasure_no_go(**kwargs)
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
                id="NEG-SELF-DUAL-WREATH-PHYSICAL-ROW-COPY-ERASURE-NO-GO",
                source=registry_experiment_id,
                claim="Initial negative claim for EXP-CODE-SELF-DUAL-WREATH-PHYSICAL-ROW-COPY-ERASURE-NO-GO.",
                reason_invalid="Falsified or refined by exact theorem evaluation.",
                lesson="Lesson from exact theorem analysis for EXP-CODE-SELF-DUAL-WREATH-PHYSICAL-ROW-COPY-ERASURE-NO-GO.",
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
                    "self_dual_wreath_physical_row_copy_erasure_no_go": str(path)
                },
            )
        )
    return payload

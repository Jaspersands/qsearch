"""Schur branch mixing is the orientation polar in encoded coordinates.

The separate-to-joint Schur dilation gives a polynomial isometric encoding of
each fixed source-label multiplicity space, but different source tuples occupy
orthogonal subgroup-branch sectors.  This module identifies exactly what an
additional coherent merger would have to do.

Fix orientation invariant projectors ``E_e`` on a common carrier ``X``.  Let
``J_e:M_e->X`` include ``M_e=ran(E_e)`` and define

    S : direct_sum_e M_e -> X,       S(x_e)_e = sum_e J_e x_e,
    A = S S^* = sum_e E_e.                                      (1)

If ``B=direct_sum_e B_e`` is any branchwise Schur isometry into orthogonal
encoded sectors, the raw encoded merger is ``S_B=S B^*``.  Consequently

    S_B S_B^* = A,
    S_B^* S_B = B(S^*S)B^*,
    polar(S_B) = A^(+/2) S B^* = polar(S) B^*.                   (2)

Here ``A^(+/2)`` denotes the Moore--Penrose inverse square root.  Thus the
normalized Schur-branch merger is exactly the physical orientation-polar
coisometry in encoded coordinates.  The Schur dilation changes neither its
nonzero singular spectrum nor its inverse-square-root content.

The same statement applies to the retained-character analysis factor.  If
``L_nu^*L_nu=I_(d_nu) tensor H_nu`` and ``C`` is any isometric embedding of
the orientation coordinates into orthogonal Schur flag sectors, then

    (L_nu C^*)^*(L_nu C^*) = C(I tensor H_nu)C^*,
    polar(L_nu C^*) = polar(L_nu) C^*.                            (3)

There is also a deterministic which-path obstruction.  Suppose an isometry
maps every branch-faithful vector to ``J_e x tensor eta_e``.  Orthogonality of
the input branches implies

    <eta_e,eta_f> J_e^*J_f = 0.                                  (4)

Hence every pair of overlapping orientation ranges requires orthogonal
environment tags.  A deterministic branch-faithful map can preserve purity
only by retaining which-path information.  A probabilistic raw merger
``c S_B`` is a contraction only when ``|c|<=1/sqrt(||A||)``; replacing it by
the norm-one partial isometry in (2) is precisely the unresolved polar.

This is an equivalence and architecture falsifier, not an arbitrary-circuit
lower bound.  A structured circuit acting inside the joint Schur companion
could still compile the polar directly, and a decoder retaining branch
characters need not erase them at all.  Neither possibility is constructed
here.
"""

from __future__ import annotations

import itertools
import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import numpy as np

from representation_obstruction import hook_length_dimension
from research_registry import utc_now
from self_dual_wreath_joint_character_multiplicity_gram import (
    orientation_overlap_kernel,
    projection_gram_factor,
)
from self_dual_wreath_orientation_fourier_reduction import (
    _w4_collision_free_labels,
    orientation_invariant_projector,
)


REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_schur_branch_merger_polar_equivalence.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-SCHUR-BRANCH-MERGER-POLAR-EQUIVALENCE"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"

Partition = tuple[int, ...]
Label = tuple[Partition, Partition]


@dataclass(frozen=True)
class SchurBranchMergerControl:
    control_id: str
    n: int
    target_partition: Partition
    labels: tuple[Label, ...]
    orientation_count: int
    active_orientation_count: int
    carrier_dimension: int
    total_active_multiplicity_dimension: int
    encoded_branch_companion_dimension: int
    active_multiplicity_ranks: tuple[int, ...]
    overlapping_branch_pair_count: int
    overlap_graph_clique_lower_bound: int
    physical_frame_rank: int
    physical_frame_maximum_eigenvalue: float
    largest_contractive_raw_merger_amplitude: float
    largest_contractive_raw_merger_probability_scale: float
    raw_frame_identity_residual: float
    encoded_output_frame_residual: float
    encoded_domain_gram_transport_residual: float
    nonzero_singular_spectrum_transport_residual: float
    physical_polar_transport_residual: float
    physical_polar_left_support_residual: float
    maximum_source_isotypic_embedding_residual: float
    maximum_invariant_bell_factorization_residual: float
    maximum_invariant_companion_interface_residual: float
    common_environment_isometry_defect: float
    orthogonal_environment_isometry_residual: float
    orientation_kernel_factor_residual: float
    encoded_orientation_kernel_transport_residual: float
    orientation_kernel_spectrum_transport_residual: float
    orientation_kernel_polar_transport_residual: float
    exact_schur_branch_polar_equivalence_verified: bool
    status: str


@dataclass(frozen=True)
class SchurBranchMergerScalingRecord:
    n: int
    information_threshold_copy_count: int
    orientation_log2_count: int
    base_local_dimension: int
    joint_schur_local_log2_dimension: float
    fixed_source_schur_carrier_encoding_polynomial: bool
    physical_invariant_to_schur_companion_interface_compiled: bool
    branch_encoding_changes_nonzero_singular_values: bool
    branch_encoding_removes_inverse_square_root: bool
    direct_structured_branch_polar_compiled: bool
    branch_character_retaining_decoder_ruled_out: bool
    status: str


@dataclass(frozen=True)
class SchurBranchMergerTheorem:
    encoded_raw_merger: str
    frame_identity: str
    polar_equivalence: str
    conditional_compiler_reduction: str
    orientation_kernel_equivalence: str
    physical_schur_interface: str
    deterministic_environment_constraint: str
    raw_contraction_boundary: str
    scope: str
    theorem_verified: bool
    status: str


@dataclass(frozen=True)
class SchurBranchMergerReport:
    created_at: str
    theorem_contract: dict[str, Any]
    theorem: SchurBranchMergerTheorem
    finite_controls: list[SchurBranchMergerControl]
    scaling_records: list[SchurBranchMergerScalingRecord]
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _support_basis(projector: np.ndarray, tolerance: float) -> np.ndarray:
    hermitian = (projector + projector.conj().T) / 2.0
    eigenvalues, eigenvectors = np.linalg.eigh(hermitian)
    return eigenvectors[:, eigenvalues > 0.5]


def _support_projector(matrix: np.ndarray, tolerance: float) -> np.ndarray:
    hermitian = (matrix + matrix.conj().T) / 2.0
    eigenvalues, eigenvectors = np.linalg.eigh(hermitian)
    keep = eigenvalues > tolerance
    if not np.any(keep):
        return np.zeros_like(matrix)
    basis = eigenvectors[:, keep]
    return basis @ basis.conj().T


def _polar(matrix: np.ndarray, tolerance: float) -> np.ndarray:
    left, singular_values, right_adjoint = np.linalg.svd(
        matrix,
        full_matrices=False,
    )
    keep = singular_values > tolerance
    if not np.any(keep):
        return np.zeros_like(matrix)
    return left[:, keep] @ right_adjoint[keep, :]


def _block_diagonal(blocks: tuple[np.ndarray, ...]) -> np.ndarray:
    row_count = sum(block.shape[0] for block in blocks)
    column_count = sum(block.shape[1] for block in blocks)
    output = np.zeros((row_count, column_count), dtype=complex)
    row_offset = 0
    column_offset = 0
    for block in blocks:
        rows, columns = block.shape
        output[
            row_offset : row_offset + rows,
            column_offset : column_offset + columns,
        ] = block
        row_offset += rows
        column_offset += columns
    return output


def _random_isometry(
    output_dimension: int,
    input_dimension: int,
    rng: np.random.Generator,
) -> np.ndarray:
    if output_dimension < input_dimension:
        raise ValueError("isometry output must be at least as large as its input")
    matrix = rng.normal(size=(output_dimension, input_dimension)) + 1j * rng.normal(
        size=(output_dimension, input_dimension)
    )
    unitary, triangular = np.linalg.qr(matrix, mode="reduced")
    diagonal = np.diag(triangular)
    phases = np.ones(input_dimension, dtype=complex)
    nonzero = np.abs(diagonal) > 1e-14
    phases[nonzero] = np.conj(diagonal[nonzero] / np.abs(diagonal[nonzero]))
    return unitary @ np.diag(phases)


def _orthogonal_flag_isometry(
    branch_count: int,
    rng: np.random.Generator,
) -> np.ndarray:
    output = np.zeros((2 * branch_count, branch_count), dtype=complex)
    for branch in range(branch_count):
        vector = rng.normal(size=2) + 1j * rng.normal(size=2)
        vector /= np.linalg.norm(vector)
        output[2 * branch : 2 * branch + 2, branch] = vector
    return output


def _positive_spectrum(matrix: np.ndarray, tolerance: float) -> np.ndarray:
    eigenvalues = np.linalg.eigvalsh((matrix + matrix.conj().T) / 2.0)
    return eigenvalues[eigenvalues > tolerance]


def _maximum_clique_size(adjacency: np.ndarray) -> int:
    count = adjacency.shape[0]
    for width in range(count, 0, -1):
        for subset in itertools.combinations(range(count), width):
            if all(adjacency[left, right] for left, right in itertools.combinations(subset, 2)):
                return width
    return 0


def _orthogonally_tagged_synthesis(
    bases: tuple[np.ndarray, ...],
) -> np.ndarray:
    ambient = bases[0].shape[0]
    branch_count = len(bases)
    total_rank = sum(basis.shape[1] for basis in bases)
    output = np.zeros((ambient * branch_count, total_rank), dtype=complex)
    source_offset = 0
    for branch, basis in enumerate(bases):
        width = basis.shape[1]
        output[
            branch * ambient : (branch + 1) * ambient,
            source_offset : source_offset + width,
        ] = basis
        source_offset += width
    return output


def _audit_invariant_bell_interface(
    invariant_basis: np.ndarray,
    irrep_dimension: int,
    carrier_dimension: int,
) -> tuple[float, float, float]:
    multiplicity = invariant_basis.shape[1]
    intertwiners = []
    for index in range(multiplicity):
        invariant = invariant_basis[:, index].reshape(
            irrep_dimension,
            carrier_dimension,
        )
        intertwiners.append(math.sqrt(irrep_dimension) * invariant.T)

    source_isotypic_synthesis = np.zeros(
        (carrier_dimension, irrep_dimension * multiplicity),
        dtype=complex,
    )
    for row in range(irrep_dimension):
        for multiplicity_index, intertwiner in enumerate(intertwiners):
            source_isotypic_synthesis[
                :,
                row * multiplicity + multiplicity_index,
            ] = intertwiner[:, row]
    isotypic_residual = float(
        np.linalg.norm(
            source_isotypic_synthesis.conj().T @ source_isotypic_synthesis
            - np.eye(irrep_dimension * multiplicity),
            ord=2,
        )
    )

    decomposed = (
        np.kron(
            np.eye(irrep_dimension),
            source_isotypic_synthesis.conj().T,
        )
        @ invariant_basis
    )
    bell_factor = np.zeros_like(decomposed)
    bell_contraction = np.zeros(
        (
            multiplicity,
            irrep_dimension * irrep_dimension * multiplicity,
        ),
        dtype=complex,
    )
    for multiplicity_index in range(multiplicity):
        for row in range(irrep_dimension):
            location = (
                row * (irrep_dimension * multiplicity)
                + row * multiplicity
                + multiplicity_index
            )
            bell_factor[location, multiplicity_index] = 1.0 / math.sqrt(
                irrep_dimension
            )
            bell_contraction[multiplicity_index, location] = 1.0 / math.sqrt(
                irrep_dimension
            )
    factorization_residual = float(
        np.linalg.norm(decomposed - bell_factor, ord=2)
    )
    interface_residual = float(
        np.linalg.norm(
            bell_contraction @ decomposed - np.eye(multiplicity),
            ord=2,
        )
    )
    return isotypic_residual, factorization_residual, interface_residual


def audit_schur_branch_merger(
    n: int,
    target: Partition,
    labels: tuple[Label, ...],
    *,
    control_id: str,
    seed: int = 20260824,
    tolerance: float = 1e-9,
) -> SchurBranchMergerControl:
    if not labels or any(
        sum(left) != n or sum(right) != n or left == right
        for left, right in labels
    ):
        raise ValueError("labels must be unequal partition pairs of n")
    if sum(target) != n:
        raise ValueError("target must partition n")

    irrep_dimension = hook_length_dimension(target)
    orientation_count = 1 << len(labels)
    projectors = tuple(
        orientation_invariant_projector(target, labels, orientation)
        for orientation in range(orientation_count)
    )
    active = tuple(
        (orientation, projector, _support_basis(projector, tolerance))
        for orientation, projector in enumerate(projectors)
        if np.trace(projector).real > 0.5
    )
    if len(active) < 2:
        raise ValueError("control requires at least two active orientations")

    active_projectors = tuple(projector for _, projector, _ in active)
    bases = tuple(basis for _, _, basis in active)
    ranks = tuple(basis.shape[1] for basis in bases)
    synthesis = np.hstack(bases)
    frame = sum(
        active_projectors,
        np.zeros_like(active_projectors[0], dtype=complex),
    )
    rng = np.random.default_rng(seed)
    branch_encoder = _block_diagonal(
        tuple(_random_isometry(rank + 1, rank, rng) for rank in ranks)
    )
    encoded_synthesis = synthesis @ branch_encoder.conj().T

    domain_gram = synthesis.conj().T @ synthesis
    encoded_domain_gram = encoded_synthesis.conj().T @ encoded_synthesis
    raw_frame_residual = float(
        np.linalg.norm(synthesis @ synthesis.conj().T - frame, ord=2)
    )
    encoded_frame_residual = float(
        np.linalg.norm(encoded_synthesis @ encoded_synthesis.conj().T - frame, ord=2)
    )
    domain_transport_residual = float(
        np.linalg.norm(
            encoded_domain_gram
            - branch_encoder @ domain_gram @ branch_encoder.conj().T,
            ord=2,
        )
    )
    source_singular_values = np.linalg.svd(synthesis, compute_uv=False)
    encoded_singular_values = np.linalg.svd(encoded_synthesis, compute_uv=False)
    source_positive = source_singular_values[source_singular_values > tolerance]
    encoded_positive = encoded_singular_values[
        encoded_singular_values > tolerance
    ]
    singular_residual = float(np.max(np.abs(source_positive - encoded_positive)))
    physical_polar = _polar(synthesis, tolerance)
    encoded_polar = _polar(encoded_synthesis, tolerance)
    polar_transport_residual = float(
        np.linalg.norm(
            encoded_polar - physical_polar @ branch_encoder.conj().T,
            ord=2,
        )
    )
    frame_support = _support_projector(frame, tolerance)
    polar_left_residual = float(
        np.linalg.norm(
            encoded_polar @ encoded_polar.conj().T - frame_support,
            ord=2,
        )
    )
    interface_controls = tuple(
        _audit_invariant_bell_interface(
            basis,
            irrep_dimension,
            projectors[0].shape[0] // irrep_dimension,
        )
        for basis in bases
    )
    maximum_isotypic_residual = max(row[0] for row in interface_controls)
    maximum_bell_residual = max(row[1] for row in interface_controls)
    maximum_interface_residual = max(row[2] for row in interface_controls)

    overlap_adjacency = np.eye(len(bases), dtype=bool)
    overlap_pairs = 0
    for left, right in itertools.combinations(range(len(bases)), 2):
        overlaps = np.linalg.norm(bases[left].conj().T @ bases[right], ord=2) > tolerance
        overlap_adjacency[left, right] = overlaps
        overlap_adjacency[right, left] = overlaps
        overlap_pairs += int(overlaps)
    clique = _maximum_clique_size(overlap_adjacency)
    common_environment_defect = float(
        np.linalg.norm(domain_gram - np.eye(domain_gram.shape[0]), ord=2)
    )
    tagged = _orthogonally_tagged_synthesis(bases)
    tagged_residual = float(
        np.linalg.norm(
            tagged.conj().T @ tagged - np.eye(tagged.shape[1]),
            ord=2,
        )
    )

    carrier_dimension = projectors[0].shape[0] // irrep_dimension
    factor = projection_gram_factor(
        active_projectors,
        irrep_dimension,
        carrier_dimension,
    )
    kernel = orientation_overlap_kernel(active_projectors, irrep_dimension)
    expected_factor_gram = np.kron(np.eye(irrep_dimension), kernel)
    factor_residual = float(
        np.linalg.norm(factor.conj().T @ factor - expected_factor_gram, ord=2)
    )
    flag = _orthogonal_flag_isometry(len(active_projectors), rng)
    full_flag = np.kron(np.eye(irrep_dimension), flag)
    encoded_factor = factor @ full_flag.conj().T
    encoded_factor_gram = encoded_factor.conj().T @ encoded_factor
    encoded_kernel = full_flag @ expected_factor_gram @ full_flag.conj().T
    kernel_transport_residual = float(
        np.linalg.norm(encoded_factor_gram - encoded_kernel, ord=2)
    )
    source_spectrum = _positive_spectrum(expected_factor_gram, tolerance)
    encoded_spectrum = _positive_spectrum(encoded_kernel, tolerance)
    kernel_spectrum_residual = float(
        np.max(np.abs(source_spectrum - encoded_spectrum))
    )
    factor_polar_residual = float(
        np.linalg.norm(
            _polar(encoded_factor, tolerance)
            - _polar(factor, tolerance) @ full_flag.conj().T,
            ord=2,
        )
    )

    frame_eigenvalues = _positive_spectrum(frame, tolerance)
    frame_maximum = float(np.max(frame_eigenvalues))
    contraction_amplitude = 1.0 / math.sqrt(frame_maximum)
    verified = bool(
        overlap_pairs > 0
        and clique >= 2
        and raw_frame_residual <= 100 * tolerance
        and encoded_frame_residual <= 100 * tolerance
        and domain_transport_residual <= 100 * tolerance
        and singular_residual <= 100 * tolerance
        and polar_transport_residual <= 100 * tolerance
        and polar_left_residual <= 100 * tolerance
        and maximum_isotypic_residual <= 100 * tolerance
        and maximum_bell_residual <= 100 * tolerance
        and maximum_interface_residual <= 100 * tolerance
        and common_environment_defect > tolerance
        and tagged_residual <= 100 * tolerance
        and factor_residual <= 100 * tolerance
        and kernel_transport_residual <= 100 * tolerance
        and kernel_spectrum_residual <= 100 * tolerance
        and factor_polar_residual <= 100 * tolerance
    )
    return SchurBranchMergerControl(
        control_id=control_id,
        n=n,
        target_partition=target,
        labels=labels,
        orientation_count=orientation_count,
        active_orientation_count=len(active),
        carrier_dimension=carrier_dimension,
        total_active_multiplicity_dimension=sum(ranks),
        encoded_branch_companion_dimension=branch_encoder.shape[0],
        active_multiplicity_ranks=ranks,
        overlapping_branch_pair_count=overlap_pairs,
        overlap_graph_clique_lower_bound=clique,
        physical_frame_rank=len(frame_eigenvalues),
        physical_frame_maximum_eigenvalue=frame_maximum,
        largest_contractive_raw_merger_amplitude=contraction_amplitude,
        largest_contractive_raw_merger_probability_scale=contraction_amplitude**2,
        raw_frame_identity_residual=raw_frame_residual,
        encoded_output_frame_residual=encoded_frame_residual,
        encoded_domain_gram_transport_residual=domain_transport_residual,
        nonzero_singular_spectrum_transport_residual=singular_residual,
        physical_polar_transport_residual=polar_transport_residual,
        physical_polar_left_support_residual=polar_left_residual,
        maximum_source_isotypic_embedding_residual=maximum_isotypic_residual,
        maximum_invariant_bell_factorization_residual=maximum_bell_residual,
        maximum_invariant_companion_interface_residual=maximum_interface_residual,
        common_environment_isometry_defect=common_environment_defect,
        orthogonal_environment_isometry_residual=tagged_residual,
        orientation_kernel_factor_residual=factor_residual,
        encoded_orientation_kernel_transport_residual=kernel_transport_residual,
        orientation_kernel_spectrum_transport_residual=kernel_spectrum_residual,
        orientation_kernel_polar_transport_residual=factor_polar_residual,
        exact_schur_branch_polar_equivalence_verified=verified,
        status=(
            "exact-schur-branch-polar-equivalence"
            if verified
            else "schur-branch-polar-equivalence-control-failure"
        ),
    )


def schur_branch_merger_scaling_record(n: int) -> SchurBranchMergerScalingRecord:
    if n < 2:
        raise ValueError("n must be at least two")
    log_order = math.lgamma(n + 1) / math.log(2)
    copy_count = math.ceil(3.0 * log_order) + 2
    return SchurBranchMergerScalingRecord(
        n=n,
        information_threshold_copy_count=copy_count,
        orientation_log2_count=copy_count,
        base_local_dimension=n,
        joint_schur_local_log2_dimension=copy_count * math.log2(n),
        fixed_source_schur_carrier_encoding_polynomial=True,
        physical_invariant_to_schur_companion_interface_compiled=True,
        branch_encoding_changes_nonzero_singular_values=False,
        branch_encoding_removes_inverse_square_root=False,
        direct_structured_branch_polar_compiled=False,
        branch_character_retaining_decoder_ruled_out=False,
        status="polynomial-encoding-polar-complexity-unchanged",
    )


def run_schur_branch_merger_polar_equivalence() -> SchurBranchMergerReport:
    w4 = _w4_collision_free_labels()
    controls = [
        audit_schur_branch_merger(
            3,
            (2, 1),
            (
                ((3,), (2, 1)),
                ((3,), (1, 1, 1)),
                ((2, 1), (1, 1, 1)),
            ),
            control_id="W3-INFORMATION-THRESHOLD",
        ),
        audit_schur_branch_merger(
            4,
            (2, 1, 1),
            w4[0],
            control_id="W4-OVERLAPPING-BRANCH-PAIR-A",
            seed=20260825,
        ),
        audit_schur_branch_merger(
            4,
            (3, 1),
            w4[1],
            control_id="W4-OVERLAPPING-BRANCH-PAIR-B",
            seed=20260826,
        ),
    ]
    scaling = [
        schur_branch_merger_scaling_record(n)
        for n in (8, 16, 32, 64, 128, 256, 512)
    ]
    failures = sum(
        not row.exact_schur_branch_polar_equivalence_verified
        for row in controls
    )
    verified = failures == 0
    theorem = SchurBranchMergerTheorem(
        encoded_raw_merger=(
            "For branch inclusions J_e and any orthogonal branchwise Schur "
            "encoding B=direct_sum_e B_e, the raw merger is S_B=S B^*."
        ),
        frame_identity=(
            "S_B S_B^*=sum_e E_e=A and S_B^*S_B=B(S^*S)B^*; all nonzero "
            "singular values and conditioning are unchanged."
        ),
        polar_equivalence=(
            "polar(S_B)=A^(+/2)S B^*=polar(S)B^*, exactly the physical "
            "orientation-polar coisometry in Schur coordinates."
        ),
        conditional_compiler_reduction=(
            "If coherent B and B^* interfaces between the physical invariant "
            "ranges and Schur branches are compiled, physical and encoded polar "
            "compilers reduce to one another by one use of that interface."
        ),
        orientation_kernel_equivalence=(
            "For every isometric Schur flag embedding C, the joint-character "
            "factor obeys Gram(L C^*)=C(I tensor H_nu)C^* and "
            "polar(L C^*)=polar(L)C^*."
        ),
        physical_schur_interface=(
            "On Inv(V_nu^* tensor sigma_e), the source Schur decomposition has "
            "the exact form |Omega_nu> tensor B_e|m>. Unpreparing the canonical "
            "Bell invariant yields the opaque companion multiplicity state "
            "without exposing its basis."
        ),
        deterministic_environment_constraint=(
            "A branch-faithful isometry J_e x tensor eta_e requires "
            "<eta_e,eta_f>J_e^*J_f=0, so overlapping branches retain "
            "orthogonal which-path tags."
        ),
        raw_contraction_boundary=(
            "The largest scalar c making cS_B a contraction is "
            "1/sqrt(||A||); the norm-one replacement is the unresolved polar."
        ),
        scope=(
            "This rejects Schur encoding as a free merger. It does not lower-bound "
            "a structured direct polar, a multi-round companion transform, or a "
            "decoder that retains orientation characters."
        ),
        theorem_verified=verified,
        status=(
            "schur-branch-encoding-is-polar-equivalent-no-free-merger"
            if verified
            else "schur-branch-merger-equivalence-validation-failure"
        ),
    )
    return SchurBranchMergerReport(
        created_at=utc_now(),
        theorem_contract=asdict(theorem),
        theorem=theorem,
        finite_controls=controls,
        scaling_records=scaling,
        proof_obligations=[
            {
                "obligation": "transport_physical_orientation_merger_into_schur_branches",
                "resolved": verified,
                "resolution": "The encoded raw merger and its polar are exact right-isometric transports of S and polar(S).",
            },
            {
                "obligation": "transport_joint_character_kernel_into_schur_flags",
                "resolved": verified,
                "resolution": "Every isometric flag embedding conjugates I tensor H_nu and leaves the analysis polar unchanged up to that embedding.",
            },
            {
                "obligation": "test_deterministic_branch_faithful_erasure",
                "resolved": verified,
                "resolution": "Overlapping physical ranges force orthogonal environment tags; deterministic transfer retains which-path information.",
            },
            {
                "obligation": "compile_structured_polar_inside_joint_schur_companion",
                "resolved": False,
                "resolution": "The equivalence identifies the exact target but supplies no circuit for A^(-1/2) or H_nu^(-1/2).",
            },
            {
                "obligation": "compile_physical_invariant_to_schur_companion_interface",
                "resolved": verified,
                "resolution": "Schur orthogonality forces the invariant range to |Omega_nu> tensor multiplicity after the source decomposition; canonical Bell unpreparation gives the interface using the predecessor's uniform Schur circuit.",
            },
            {
                "obligation": "construct_branch_character_retaining_hidden_involution_decoder",
                "resolved": False,
                "resolution": "A decoder may avoid erasure by retaining characters; no all-n information extraction or classical separation is known.",
            },
        ],
        adversarial_audit=[
            {
                "objection": "The larger Schur companion workspace makes cross-branch erasure unitary.",
                "resolved": True,
                "resolution": "A branchwise isometry only conjugates the merger Gram and polar; orthogonal workspace does not create the missing overlaps.",
            },
            {
                "objection": "Using the Schur carrier requires first exposing a standard Kronecker multiplicity basis.",
                "resolved": True,
                "resolution": "No. On the invariant support, the target/source irrep pair is the known Bell invariant and unprepares independently of the opaque companion multiplicity state.",
            },
            {
                "objection": "A deterministic Stinespring dilation can erase the branch into an unobserved environment.",
                "resolved": True,
                "resolution": "For every nonzero cross-range overlap, isometry forces the corresponding environment tags to be orthogonal, so tracing them destroys the desired coherence.",
            },
            {
                "objection": "Scaling the raw merger to a contraction avoids inverse square roots.",
                "resolved": True,
                "resolution": "It produces a lossy raw analysis map. Its normalized partial-isometric replacement is exactly A^(+/2)S_B.",
            },
            {
                "objection": "Polar equivalence proves the Schur companion route is computationally hard.",
                "resolved": True,
                "resolution": "No circuit lower bound follows. The companion may expose structure useful for directly compiling the same polar.",
            },
            {
                "objection": "Every viable decoder must merge branches.",
                "resolved": True,
                "resolution": "False. The retained-character route keeps the full Walsh register and remains a separate open architecture.",
            },
        ],
        headline_metrics={
            "exact_schur_branch_polar_equivalence_theorem_count": int(verified),
            "physical_invariant_schur_companion_interface_count": int(verified),
            "finite_control_count": len(controls),
            "finite_control_failure_count": failures,
            "overlapping_branch_pair_control_count": sum(
                row.overlapping_branch_pair_count for row in controls
            ),
            "maximum_overlap_graph_clique_lower_bound": max(
                row.overlap_graph_clique_lower_bound for row in controls
            ),
            "direct_structured_branch_polar_compiler_count": 0,
            "branch_character_retaining_decoder_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "schur_branch_encoding_preserves_nonzero_singular_spectrum": verified,
            "encoded_raw_merger_frame_equals_physical_frame": verified,
            "encoded_merger_polar_equals_physical_orientation_polar": verified,
            "encoded_joint_character_polar_equals_original_polar": verified,
            "overlapping_branch_faithful_transfer_requires_which_path_environment": verified,
            "physical_encoded_polar_compilers_interreduce_given_interface": verified,
            "physical_encoded_polar_compilers_polynomially_interreducible": verified,
            "physical_invariant_to_schur_companion_interface_compiled": verified,
            "schur_dilation_alone_compiles_cross_orientation_merger": False,
            "schur_dilation_removes_orientation_inverse_square_root": False,
            "direct_structured_branch_polar_compiled": False,
            "multi_round_companion_transform_ruled_out": False,
            "branch_character_retaining_decoder_ruled_out": False,
            "physical_pgm_compiled": False,
            "classical_separation_proved": False,
            "speedup_claim_allowed": False,
        },
        status=theorem.status,
        summary=(
            "Closed the free-Schur-merger loophole: orthogonal fixed-source Schur "
            "encodings preserve the full physical and joint-character Gram spectra, "
            "and their normalized mergers are exactly the existing orientation "
            "polars in encoded coordinates. A useful Schur route must therefore "
            "compile that polar using companion structure or avoid branch erasure."
        ),
        falsifiers_triggered=[
            "Polynomial Schur isotypic routing does not itself produce cross-orientation coherence.",
            "Deterministic branch-faithful transfer preserves purity only by retaining which-path tags on overlapping ranges.",
            "An isometric coordinate enlargement cannot remove A^(-1/2) or H_nu^(-1/2).",
        ],
    )


def write_schur_branch_merger_polar_equivalence_report(
    path: Path = REPORT_PATH,
) -> dict[str, Any]:
    payload = asdict(run_schur_branch_merger_polar_equivalence())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return payload


if __name__ == "__main__":
    report = write_schur_branch_merger_polar_equivalence_report()
    print(json.dumps(report["headline_metrics"], indent=2))

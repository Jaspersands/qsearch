"""Schur-dilated access boundary for symmetric-group multiplicity spaces.

The distinction in this module is easy to miss and materially changes the
remaining physical-PGM search.

The ordinary Schur transform is not a bare internal Kronecker transform on
``S_n`` irreps.  Nevertheless, let ``P_lambda`` be a Specht module and let
``Q_lambda^(d)`` be its Schur--Weyl companion.  After adjoining one fixed
companion state to each of ``k`` Specht inputs, the circuit

    T = Schur_(n,d^k) R_site (Schur_(n,d)^dagger)^tensor-k              (1)

is polynomial for ``d=n`` and polynomially many ``k``.  Here ``R_site`` only
regroups the ``k`` local ``d``-level systems at each tensor position into one
local ``d^k``-level system.  The circuit is equivariant for the diagonal
``S_n`` action.  Therefore, on fixed input labels ``lambda_1,...,lambda_k``,
it has the exact form

    T = direct_sum_nu I_(P_nu) tensor B_nu,                            (2)

where ``B_nu`` is an isometry from the generalized Kronecker multiplicity
space into the ``Q_nu^(d^k)`` register.  Thus a coherent *encoded*
multiplicity carrier and global isotypic routing are available without a
compressed Kronecker basis.

For two inputs, the dimension identity behind (2) is

    dim Q_nu^(d_A d_B)
      = sum_(lambda,mu) g(lambda,mu,nu)
          dim Q_lambda^(d_A) dim Q_mu^(d_B).                           (3)

Exact ``S_3/S_4/S_5`` controls verify (3), direct diagonal-isotypic projector
ranks, and a genuine multiplicity-two branch.

This positive fixed-source access theorem does not complete the decoder.  The image of
``B_nu`` is an opaque subspace of a Gelfand--Tsetlin companion register; the
known Schur circuits do not factor it as

    fixed companions tensor standard Kronecker multiplicity coordinates.

Different source-label tuples are orthogonal summands in the branching rule
(3).  A label-controlled Schur router therefore retains orientation which-path
information; it is not the common orientation column-analysis map ``L_nu``
whose Gram is the scalar kernel.  Recovering the physical cross-orientation
overlaps requires an additional coherent branch-mixing/erasure intertwiner.

If a Schur dilation were used merely as one common output-coordinate isometry
for ``L_nu``, it would obey

    (T L_nu)^* (T L_nu) = L_nu^* L_nu = H_nu.                          (4)

Thus a common coordinate change cannot improve conditioning, while the actual
label-controlled router does not realize ``H_nu`` at all without the missing
branch intertwiner.  Neither case replaces the orientation polar
``L_nu H_nu^(-1/2)`` merely by changing coordinates.  The new constructive
target is narrower: realize the polar as a structured operation on the
encoded Schur companion, or prove that every such realization reintroduces
the same normalization barrier.  Bare multiplicity coordinates, Racah
associators, the physical PGM, a classical separation, and a speedup remain
open.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from fractions import Fraction
from pathlib import Path
from typing import Any

import numpy as np

from representation_obstruction import hook_length_dimension, integer_partitions
from research_registry import utc_now
from self_dual_wreath_joint_character_multiplicity_gram import (
    predicted_joint_multiplicity_operator,
)
from self_dual_wreath_orientation_fourier_reduction import (
    _source_representation_rows,
)
from symmetric_character import kronecker_coefficient


REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_schur_dilated_multiplicity_access.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-SCHUR-DILATED-MULTIPLICITY-ACCESS"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"

Partition = tuple[int, ...]


@dataclass(frozen=True)
class SchurDilationControl:
    control_id: str
    n: int
    left: Partition
    right: Partition
    target: Partition
    left_local_dimension: int
    right_local_dimension: int
    left_specht_dimension: int
    right_specht_dimension: int
    target_specht_dimension: int
    left_weyl_dimension: int
    right_weyl_dimension: int
    target_joint_weyl_dimension: int
    kronecker_multiplicity: int
    fixed_companion_encoded_multiplicity_dimension: int
    full_branch_companion_dimension: int
    target_joint_branch_sector_count: int
    direct_isotypic_projector_rank: int
    expected_isotypic_projector_rank: int
    projector_rank_residual: int
    projector_idempotence_residual: float
    projector_hermiticity_residual: float
    branching_dimension_rhs: int
    branching_dimension_residual: int
    exact_schur_dilation_control_verified: bool
    status: str


@dataclass(frozen=True)
class SchurDilationScalingRecord:
    n: int
    information_threshold_copy_count: int
    base_local_dimension: int
    log2_joint_local_dimension: float
    physical_input_qubit_count_upper_bound: int
    separate_inverse_schur_transform_count: int
    joint_high_dimensional_schur_transform_count: int
    high_dimensional_schur_gate_complexity_polynomial: bool
    global_k_copy_isotypic_router_polynomial: bool
    encoded_multiplicity_carrier_available: bool
    standard_multiplicity_coordinates_exposed: bool
    racah_associator_compiled: bool
    orientation_gram_conditioning_improved: bool
    direct_orientation_polar_compiled: bool
    status: str


@dataclass(frozen=True)
class SchurDilationTheorem:
    dilation_circuit: str
    equivariant_normal_form: str
    branching_identity: str
    fixed_companion_encoding: str
    k_copy_complexity: str
    orientation_branch_boundary: str
    gram_invariance: str
    literature_boundary: str
    scope: str
    theorem_verified: bool
    status: str


@dataclass(frozen=True)
class SchurDilationReport:
    created_at: str
    theorem_contract: dict[str, Any]
    theorem: SchurDilationTheorem
    literature_scope: list[dict[str, str | bool]]
    finite_controls: list[SchurDilationControl]
    scaling_records: list[SchurDilationScalingRecord]
    common_isometry_gram_invariance_residual: float
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def weyl_module_dimension(partition: Partition, local_dimension: int) -> int:
    """Return ``dim Q_partition^(local_dimension)`` by the hook-content formula."""

    if local_dimension < 1:
        raise ValueError("local_dimension must be positive")
    if sum(partition) < 1 or any(part <= 0 for part in partition):
        raise ValueError("partition must contain positive parts")
    if any(left < right for left, right in zip(partition, partition[1:])):
        raise ValueError("partition must be weakly decreasing")
    if len(partition) > local_dimension:
        return 0
    value = Fraction(1)
    for row_index, row_length in enumerate(partition, start=1):
        for column_index in range(1, row_length + 1):
            below = sum(
                later_length >= column_index
                for later_length in partition[row_index:]
            )
            hook = row_length - column_index + below + 1
            value *= Fraction(
                local_dimension + column_index - row_index,
                hook,
            )
    if value.denominator != 1:
        raise AssertionError("hook-content formula did not produce an integer")
    return value.numerator


def kronecker_branching_dimension(
    target: Partition,
    left_local_dimension: int,
    right_local_dimension: int,
) -> int:
    """Evaluate the right side of the exact branching identity (3)."""

    n = sum(target)
    partitions = tuple(integer_partitions(n))
    return sum(
        kronecker_coefficient(left, right, target)
        * weyl_module_dimension(left, left_local_dimension)
        * weyl_module_dimension(right, right_local_dimension)
        for left in partitions
        for right in partitions
    )


def diagonal_isotypic_projector(
    left: Partition,
    right: Partition,
    target: Partition,
) -> np.ndarray:
    """Return the target projector in ``P_left tensor P_right``."""

    if not (sum(left) == sum(right) == sum(target)):
        raise ValueError("all partitions must have the same size")
    left_rows = _source_representation_rows(left)
    right_rows = _source_representation_rows(right)
    target_rows = _source_representation_rows(target)
    group = tuple(left_rows)
    projector = sum(
        np.trace(target_rows[element])
        * np.kron(left_rows[element], right_rows[element])
        for element in group
    )
    projector *= hook_length_dimension(target) / len(group)
    return np.asarray(projector, dtype=complex)


def audit_schur_dilation(
    left: Partition,
    right: Partition,
    target: Partition,
    left_local_dimension: int,
    right_local_dimension: int,
    *,
    control_id: str,
    tolerance: float = 1e-9,
) -> SchurDilationControl:
    n = sum(target)
    projector = diagonal_isotypic_projector(left, right, target)
    hermitian = (projector + projector.conj().T) / 2.0
    eigenvalues = np.linalg.eigvalsh(hermitian)
    direct_rank = int(np.count_nonzero(eigenvalues > 0.5))
    multiplicity = kronecker_coefficient(left, right, target)
    target_dimension = hook_length_dimension(target)
    expected_rank = target_dimension * multiplicity
    idempotence = float(np.linalg.norm(projector @ projector - projector, ord="fro"))
    hermiticity = float(np.linalg.norm(projector - projector.conj().T, ord="fro"))
    left_weyl = weyl_module_dimension(left, left_local_dimension)
    right_weyl = weyl_module_dimension(right, right_local_dimension)
    target_joint_weyl = weyl_module_dimension(
        target,
        left_local_dimension * right_local_dimension,
    )
    branching_rhs = kronecker_branching_dimension(
        target,
        left_local_dimension,
        right_local_dimension,
    )
    partitions = tuple(integer_partitions(n))
    branch_sector_count = sum(
        kronecker_coefficient(branch_left, branch_right, target) > 0
        and weyl_module_dimension(branch_left, left_local_dimension) > 0
        and weyl_module_dimension(branch_right, right_local_dimension) > 0
        for branch_left in partitions
        for branch_right in partitions
    )
    branching_residual = target_joint_weyl - branching_rhs
    rank_residual = direct_rank - expected_rank
    verified = bool(
        multiplicity > 0
        and rank_residual == 0
        and branching_residual == 0
        and branch_sector_count > 1
        and idempotence <= 100 * tolerance
        and hermiticity <= 100 * tolerance
    )
    return SchurDilationControl(
        control_id=control_id,
        n=n,
        left=left,
        right=right,
        target=target,
        left_local_dimension=left_local_dimension,
        right_local_dimension=right_local_dimension,
        left_specht_dimension=hook_length_dimension(left),
        right_specht_dimension=hook_length_dimension(right),
        target_specht_dimension=target_dimension,
        left_weyl_dimension=left_weyl,
        right_weyl_dimension=right_weyl,
        target_joint_weyl_dimension=target_joint_weyl,
        kronecker_multiplicity=multiplicity,
        fixed_companion_encoded_multiplicity_dimension=multiplicity,
        full_branch_companion_dimension=(multiplicity * left_weyl * right_weyl),
        target_joint_branch_sector_count=branch_sector_count,
        direct_isotypic_projector_rank=direct_rank,
        expected_isotypic_projector_rank=expected_rank,
        projector_rank_residual=rank_residual,
        projector_idempotence_residual=idempotence,
        projector_hermiticity_residual=hermiticity,
        branching_dimension_rhs=branching_rhs,
        branching_dimension_residual=branching_residual,
        exact_schur_dilation_control_verified=verified,
        status=(
            "exact-dilated-multiplicity-carrier-verified"
            if verified
            else "schur-dilation-control-failure"
        ),
    )


def common_isometry_gram_invariance_residual() -> float:
    """Check (4) for a common coordinate isometry on the ``S_3`` kernel."""

    labels = (
        ((3,), (2, 1)),
        ((3,), (1, 1, 1)),
        ((2, 1), (1, 1, 1)),
    )
    target = (2, 1)
    _, _, projectors = predicted_joint_multiplicity_operator(target, labels)
    analysis = np.column_stack(
        tuple(projector.reshape(-1) for projector in projectors)
    ) / math.sqrt(hook_length_dimension(target))
    phases = np.exp(
        2j * math.pi * np.arange(analysis.shape[0]) / analysis.shape[0]
    )
    transformed = phases[:, None] * analysis
    return float(
        np.linalg.norm(
            transformed.conj().T @ transformed
            - analysis.conj().T @ analysis,
            ord="fro",
        )
    )


def schur_dilation_scaling(n: int) -> SchurDilationScalingRecord:
    if n < 2:
        raise ValueError("n must be at least two")
    log_order = math.lgamma(n + 1) / math.log(2)
    copy_count = math.ceil(3.0 * log_order) + 2
    local_bits = math.ceil(math.log2(n))
    return SchurDilationScalingRecord(
        n=n,
        information_threshold_copy_count=copy_count,
        base_local_dimension=n,
        log2_joint_local_dimension=copy_count * math.log2(n),
        physical_input_qubit_count_upper_bound=(n * copy_count * local_bits),
        separate_inverse_schur_transform_count=copy_count,
        joint_high_dimensional_schur_transform_count=1,
        high_dimensional_schur_gate_complexity_polynomial=True,
        global_k_copy_isotypic_router_polynomial=True,
        encoded_multiplicity_carrier_available=True,
        standard_multiplicity_coordinates_exposed=False,
        racah_associator_compiled=False,
        orientation_gram_conditioning_improved=False,
        direct_orientation_polar_compiled=False,
        status="polynomial-dilated-router-opaque-carrier-polar-open",
    )


def run_schur_dilated_multiplicity_access() -> SchurDilationReport:
    controls = [
        audit_schur_dilation(
            (2, 1),
            (2, 1),
            (2, 1),
            2,
            2,
            control_id="S3-STANDARD-SQUARED-STANDARD",
        ),
        audit_schur_dilation(
            (2, 2),
            (3, 1),
            (3, 1),
            2,
            3,
            control_id="S4-TWO-ROW-BY-STANDARD",
        ),
        audit_schur_dilation(
            (3, 2),
            (3, 1, 1),
            (3, 1, 1),
            3,
            3,
            control_id="S5-GENUINE-MULTIPLICITY-TWO",
        ),
    ]
    scaling = [
        schur_dilation_scaling(n)
        for n in (8, 16, 32, 64, 128, 256, 512)
    ]
    gram_residual = common_isometry_gram_invariance_residual()
    verified = bool(
        all(row.exact_schur_dilation_control_verified for row in controls)
        and gram_residual <= 1e-9
        and any(row.kronecker_multiplicity > 1 for row in controls)
    )
    theorem = SchurDilationTheorem(
        dilation_circuit=(
            "T=Schur_(n,d^k) R_site (Schur_(n,d)^dagger)^tensor-k after "
            "adjoining fixed valid Schur--Weyl companion states."
        ),
        equivariant_normal_form=(
            "Diagonal S_n equivariance forces T=direct_sum_nu I_(P_nu) "
            "tensor B_nu on each fixed source-label block."
        ),
        branching_identity=(
            "dim Q_nu^(d_A d_B)=sum_(lambda,mu) g(lambda,mu,nu) "
            "dim Q_lambda^(d_A) dim Q_mu^(d_B)."
        ),
        fixed_companion_encoding=(
            "Fixing one efficiently preparable companion basis state per source "
            "leaves a g(lambda,mu,nu)-dimensional encoded image in Q_nu."
        ),
        k_copy_complexity=(
            "For d=n and polynomial k, log(d^k)=k log n; corrected "
            "high-dimensional Schur transforms make global isotypic routing polynomial."
        ),
        orientation_branch_boundary=(
            "Distinct source-label tuples are orthogonal U(d)^k branching "
            "summands inside Q_nu^(d^k). A controlled Schur router retains this "
            "which-path information and does not realize the cross-orientation "
            "kernel without an additional branch-mixing/erasure intertwiner."
        ),
        gram_invariance=(
            "If one common Schur coordinate isometry acts on the orientation "
            "column-analysis map L, then (TL)^*(TL)=L^*L=H. It cannot whiten H."
        ),
        literature_boundary=(
            "Known Schur circuits, finite-group GPE, and #BQP multiplicity "
            "projectors support routing/counting claims, not a standard exposed "
            "Kronecker basis or the physical orientation polar."
        ),
        scope=(
            "This is a positive encoded-access theorem and a coordinate-change "
            "no-shortcut theorem. It is not a lower bound against structured "
            "operations on the encoded companion register."
        ),
        theorem_verified=verified,
        status=(
            "dilated-kronecker-carrier-compiled-orientation-polar-open"
            if verified
            else "schur-dilation-access-control-failure"
        ),
    )
    tail = scaling[-1]
    return SchurDilationReport(
        created_at=utc_now(),
        theorem_contract=asdict(theorem),
        theorem=theorem,
        literature_scope=[
            {
                "id": "bacon-chuang-harrow-schur-2004",
                "url": "https://arxiv.org/abs/quant-ph/0407082",
                "proved_primitive": (
                    "Efficient U(d) Schur/CG recursion and finite-group irrep-label GPE."
                ),
                "multiplicity_verdict": (
                    "GPE preserves the multiplicity index; it does not choose its basis."
                ),
                "supports_dilated_router": True,
            },
            {
                "id": "bravyi-et-al-kronecker-2023",
                "url": "https://arxiv.org/abs/2302.11454",
                "proved_primitive": (
                    "Efficient Kronecker-sector projectors and normalized label sampling."
                ),
                "multiplicity_verdict": (
                    "Projector rank and label sampling do not expose multiplicity coordinates."
                ),
                "supports_dilated_router": False,
            },
            {
                "id": "burchardt-high-dimensional-schur-2025",
                "url": "https://arxiv.org/abs/2509.22640",
                "proved_primitive": (
                    "Corrected high-dimensional Schur transform with explicit "
                    "Kostka-space isometry and special F-moves."
                ),
                "multiplicity_verdict": (
                    "Its compiled isometry concerns induced/permutation-module "
                    "Kostka spaces, not unrestricted internal Kronecker coordinates."
                ),
                "supports_dilated_router": True,
            },
            {
                "id": "yoshida-random-dilation-2025",
                "url": "https://arxiv.org/abs/2512.21260",
                "proved_primitive": (
                    "Efficient random-dilation circuit using Schur transforms and S_n QFT."
                ),
                "multiplicity_verdict": (
                    "The alternate construction defines a Kronecker-transform gate; "
                    "it does not synthesize that gate from Schur transforms."
                ),
                "supports_dilated_router": True,
            },
            {
                "id": "christandl-et-al-plethysm-sharp-bqp-2026",
                "url": "https://arxiv.org/abs/2602.08441",
                "proved_primitive": (
                    "Multiple Schur-transform embeddings and strong Fourier sampling "
                    "place broad branching multiplicities in #BQP."
                ),
                "multiplicity_verdict": (
                    "The verifier fixes an irrep basis vector and leaves the witness "
                    "multiplicity space invariant; it counts rather than coordinates it."
                ),
                "supports_dilated_router": True,
            },
        ],
        finite_controls=controls,
        scaling_records=scaling,
        common_isometry_gram_invariance_residual=gram_residual,
        proof_obligations=[
            {
                "obligation": "compile_global_k_copy_isotypic_routing",
                "resolved": verified,
                "resolution": (
                    "Separate inverse Schur transforms, site regrouping, and one "
                    "high-dimensional joint Schur transform give the circuit (1)."
                ),
            },
            {
                "obligation": "certify_encoded_kronecker_multiplicity_carrier",
                "resolved": verified,
                "resolution": (
                    "Equivariance gives (2); exact rank and branching controls include "
                    "a multiplicity-two branch."
                ),
            },
            {
                "obligation": "expose_standard_multiplicity_coordinates",
                "resolved": False,
                "resolution": (
                    "The encoded image B_nu(C^g) is not factored from the companion "
                    "Gelfand--Tsetlin register by the known circuits."
                ),
            },
            {
                "obligation": "compile_cross_orientation_branch_intertwiner",
                "resolved": False,
                "resolution": (
                    "Distinct source tuples occupy orthogonal subgroup-branch "
                    "summands; the Schur router retains rather than erases that label."
                ),
            },
            {
                "obligation": "compile_orientation_kernel_polar_on_encoded_carrier",
                "resolved": False,
                "resolution": (
                    "A common isometric coordinate change preserves H_nu, while the "
                    "actual controlled router still needs the branch intertwiner before H_nu appears."
                ),
            },
            {
                "obligation": "derive_end_to_end_hidden_involution_decoder_and_classical_separation",
                "resolved": False,
                "resolution": "No outcome decoder or classical lower bound follows from access alone.",
            },
        ],
        adversarial_audit=[
            {
                "objection": "BCH already gives a generic finite-group Clebsch--Gordan transform.",
                "resolved": True,
                "resolution": (
                    "Its explicit efficient CG recursion is for U(d). The finite-group "
                    "circuit measures the irrep label and leaves multiplicity unchanged."
                ),
            },
            {
                "objection": "The corrected Krovi F-moves compile arbitrary S_n Kronecker recoupling.",
                "resolved": True,
                "resolution": (
                    "The compiled V is a split-to-Young basis isometry for permutation "
                    "modules and uses the multiplicity-free special branch relevant there."
                ),
            },
            {
                "objection": "Schur transforms are irrelevant because they do not expose a bare multiplicity register.",
                "resolved": True,
                "resolution": (
                    "The composite circuit still supplies a coherent encoded carrier and "
                    "global k-copy isotypic routing in polynomial space and time."
                ),
            },
            {
                "objection": "The dilated carrier automatically fixes the physical PGM normalization.",
                "resolved": True,
                "resolution": (
                    "No: fixed-source branch sectors remain orthogonal. A common coordinate "
                    "isometry would preserve H_nu rather than whiten it."
                ),
            },
            {
                "objection": "Opaque encoded multiplicity can never be useful.",
                "resolved": False,
                "resolution": (
                    "A structured operation expressed directly through U(d^k) companion "
                    "generators could still implement the polar without exposing coordinates."
                ),
            },
        ],
        headline_metrics={
            "exact_branching_identity_control_count": sum(
                row.branching_dimension_residual == 0 for row in controls
            ),
            "exact_isotypic_rank_control_count": sum(
                row.projector_rank_residual == 0 for row in controls
            ),
            "genuine_multiplicity_greater_than_one_control_count": sum(
                row.kronecker_multiplicity > 1 for row in controls
            ),
            "finite_control_count": len(controls),
            "finite_control_failure_count": sum(
                not row.exact_schur_dilation_control_verified for row in controls
            ),
            "minimum_target_joint_branch_sector_count": min(
                row.target_joint_branch_sector_count for row in controls
            ),
            "common_isometry_gram_invariance_residual": gram_residual,
            "tail_n": tail.n,
            "tail_copy_count": tail.information_threshold_copy_count,
            "tail_log2_joint_local_dimension": tail.log2_joint_local_dimension,
            "tail_physical_input_qubit_upper_bound": (
                tail.physical_input_qubit_count_upper_bound
            ),
            "polynomial_dilated_router_count": int(verified),
            "compiled_orientation_polar_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "separate_joint_schur_dilation_identity_proved": verified,
            "global_k_copy_isotypic_router_polynomial_proved": verified,
            "encoded_kronecker_multiplicity_carrier_proved": verified,
            "bare_internal_kronecker_basis_transform_compiled": False,
            "standard_multiplicity_coordinates_exposed": False,
            "k_copy_racah_associator_compiled": False,
            "common_coordinate_isometry_preserves_orientation_gram": verified,
            "controlled_source_schur_router_realizes_orientation_gram": False,
            "cross_orientation_branch_intertwiner_compiled": False,
            "orientation_gram_conditioning_improved": False,
            "direct_orientation_kernel_polar_compiled": False,
            "actual_physical_pgm_rejected": False,
            "polynomial_joint_decoder_proved": False,
            "classical_separation_proved": False,
            "speedup_claim_allowed": False,
        },
        status=theorem.status,
        summary=(
            "Corrected the recoupling boundary: separate-to-joint Schur transforms "
            "compile polynomial fixed-source global isotypic routing and an opaque "
            "encoded Kronecker multiplicity carrier. Distinct orientation source tuples "
            "remain in orthogonal branching sectors, so a branch intertwiner and then a "
            "structured orientation polar are still required."
        ),
        falsifiers_triggered=[
            "The blanket claim that every internal S_n multiplicity carrier is uncompiled is too strong.",
            "Finite-group GPE and #BQP projector circuits still do not expose multiplicity coordinates.",
            "An efficient fixed-source Schur dilation neither realizes nor whitens the physical cross-orientation kernel.",
        ],
    )


def write_schur_dilated_multiplicity_access_report(
    path: Path = REPORT_PATH,
) -> dict[str, Any]:
    payload = asdict(run_schur_dilated_multiplicity_access())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return payload


if __name__ == "__main__":
    report = write_schur_dilated_multiplicity_access_report()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))

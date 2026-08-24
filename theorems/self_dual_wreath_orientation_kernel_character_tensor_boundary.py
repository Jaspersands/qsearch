"""Character tensor-network boundary for the physical orientation kernel.

The surviving physical joint-character PGM requires a structured polar of

    H_nu[e,f] = Tr(E_e E_f)/d_nu.

This module gives an exact entry formula that exposes both the available
structure and the cost hidden by several tempting simplifications.  Let
``x,y in S_n``.  For source pair ``(lambda_i,mu_i)``, define the local
orientation matrix

    Q_i(x,y) = [[d_mu chi_lambda(xy), chi_lambda(x)chi_mu(y)],
                [chi_lambda(y)chi_mu(x), d_lambda chi_mu(xy)]].

Then

    H_nu[e,f] = 1/(d_nu |G|^2) sum_(x,y)
                  chi_nu(xy) product_i Q_i(x,y)[e_i,f_i]. (1)

Equivalently, ``H_nu`` is a sum of ``|G|^2`` tensor-product operators on the
orientation qubits.  This is a useful exact tensor network, but not yet an
efficient contraction.

The summand is invariant under simultaneous conjugation of ``(x,y)``.  The
number of pair orbits is

    orb_2(G)=|G|^-1 sum_z |C_G(z)|^2.

For ``S_n`` this equals ``sum_(alpha|-n) z_alpha`` and is at least ``n!``
because the identity class contributes ``z_(1^n)=n!``.  Thus explicit orbit
enumeration remains factorial even after exploiting every simultaneous-
conjugacy symmetry in (1).

Exact ``S_3/S_4`` controls also reject three universal local shortcuts:

* ``H_nu`` need not depend only on ``e xor f``, so the Boolean Walsh transform
  does not generally diagonalize it;
* its operator-Schmidt rank across orientation cuts can be maximal, so it is
  not a product kernel or a uniformly rank-one bond;
* the local matrices ``Q_i(x,y)`` do not commute, so no fixed one-qubit basis
  simultaneously diagonalizes the character summands.

These are falsifiers for simple ansatzes, not asymptotic lower bounds on
source-dependent tensor networks.  A viable direct polar must coherently
contract the global ``S_n x S_n`` character network, equivalently implement
the unresolved internal Kronecker/Racah multiplicity transform.  Polynomial
entry evaluation, an efficient ``S_n`` QFT, or explicit pair-orbit listing is
not that transform.
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
from self_dual_wreath_character_moments import compose_permutations
from self_dual_wreath_joint_character_multiplicity_gram import (
    Label,
    Partition,
    orientation_overlap_kernel,
    predicted_joint_multiplicity_operator,
    walsh_matrix,
)
from self_dual_wreath_orientation_fourier_reduction import (
    Permutation,
    _source_representation_rows,
    _w4_collision_free_labels,
)
from self_dual_wreath_shared_pair_recoupling_decoupling import (
    class_centralizer_size,
)


REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_orientation_kernel_character_tensor_boundary.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-ORIENTATION-KERNEL-CHARACTER-TENSOR-BOUNDARY"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


@dataclass(frozen=True)
class CharacterTensorKernelControl:
    control_id: str
    n: int
    target: Partition
    labels: tuple[Label, ...]
    group_order: int
    orientation_qubit_count: int
    orientation_dimension: int
    character_pair_summand_count: int
    simultaneous_pair_orbit_count_formula: int
    simultaneous_pair_orbit_count_direct: int
    pair_orbit_count_residual: int
    character_tensor_formula_residual: float
    hermiticity_residual: float
    minimum_kernel_eigenvalue: float
    boolean_translation_invariance_residual: float
    walsh_offdiagonal_frobenius_norm: float
    walsh_offdiagonal_fraction: float
    operator_schmidt_ranks: tuple[int, ...]
    operator_schmidt_maximum_possible_ranks: tuple[int, ...]
    maximum_local_character_factor_commutator_norm: float
    boolean_walsh_diagonalization_valid: bool
    product_orientation_kernel_valid: bool
    fixed_local_simultaneous_diagonalization_valid: bool
    exact_character_tensor_boundary_verified: bool
    status: str


@dataclass(frozen=True)
class CharacterTensorScalingRecord:
    n: int
    log2_group_order: float
    information_threshold_orientation_qubits: int
    log2_raw_character_pair_summand_count: float
    log2_simultaneous_pair_orbit_count_lower_bound: float
    simultaneous_conjugacy_orbit_enumeration_polynomial: bool
    symmetric_group_qft_alone_contracts_pair_network: bool
    internal_kronecker_multiplicity_transform_compiled: bool
    direct_orientation_kernel_polar_compiled: bool
    status: str


@dataclass(frozen=True)
class CharacterTensorBoundaryTheorem:
    exact_character_network: str
    simultaneous_conjugacy: str
    orbit_count: str
    walsh_boundary: str
    tensor_product_boundary: str
    local_basis_boundary: str
    surviving_transform: str
    scope: str
    theorem_verified: bool
    status: str


@dataclass(frozen=True)
class CharacterTensorBoundaryReport:
    created_at: str
    theorem_contract: dict[str, Any]
    theorem: CharacterTensorBoundaryTheorem
    finite_controls: list[CharacterTensorKernelControl]
    scaling_records: list[CharacterTensorScalingRecord]
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _inverse_permutation(permutation: Permutation) -> Permutation:
    output = [0] * len(permutation)
    for source, target in enumerate(permutation):
        output[target] = source
    return tuple(output)


def _conjugate(
    conjugator: Permutation,
    permutation: Permutation,
) -> Permutation:
    return compose_permutations(
        compose_permutations(conjugator, permutation),
        _inverse_permutation(conjugator),
    )


def local_character_factor_matrix(
    label: Label,
    left_group_element: Permutation,
    right_group_element: Permutation,
) -> np.ndarray:
    """Return the local ``Q_i(x,y)`` matrix in equation (1)."""

    left, right = label
    left_rows = _source_representation_rows(left)
    right_rows = _source_representation_rows(right)
    left_x = left_rows[left_group_element]
    left_y = left_rows[right_group_element]
    right_x = right_rows[left_group_element]
    right_y = right_rows[right_group_element]
    return np.asarray(
        [
            [
                right_x.shape[0] * np.trace(left_x @ left_y),
                np.trace(left_x) * np.trace(right_y),
            ],
            [
                np.trace(left_y) * np.trace(right_x),
                left_x.shape[0] * np.trace(right_x @ right_y),
            ],
        ],
        dtype=complex,
    )


def character_tensor_orientation_kernel(
    target: Partition,
    labels: tuple[Label, ...],
) -> np.ndarray:
    """Evaluate the exact two-group-variable character network (1)."""

    if not labels:
        raise ValueError("at least one source pair is required")
    target_rows = _source_representation_rows(target)
    group = tuple(target_rows)
    count = 1 << len(labels)
    dimension = hook_length_dimension(target)
    output = np.zeros((count, count), dtype=complex)
    for left_element in group:
        for right_element in group:
            target_character = np.trace(
                target_rows[left_element] @ target_rows[right_element]
            )
            local = tuple(
                local_character_factor_matrix(
                    label,
                    left_element,
                    right_element,
                )
                for label in labels
            )
            for orientation in range(count):
                for other in range(count):
                    value = target_character
                    for index, matrix in enumerate(local):
                        value *= matrix[
                            (orientation >> index) & 1,
                            (other >> index) & 1,
                        ]
                    output[orientation, other] += value
    output /= dimension * len(group) ** 2
    return output


def simultaneous_pair_orbit_count_formula(n: int) -> int:
    if n < 1:
        raise ValueError("n must be positive")
    return sum(
        class_centralizer_size(cycle_type)
        for cycle_type in integer_partitions(n)
    )


def simultaneous_pair_orbit_count_direct(n: int) -> int:
    group = tuple(_source_representation_rows((n,)))
    unseen = set(itertools.product(group, repeat=2))
    count = 0
    while unseen:
        left, right = next(iter(unseen))
        orbit = {
            (_conjugate(element, left), _conjugate(element, right))
            for element in group
        }
        unseen.difference_update(orbit)
        count += 1
    return count


def boolean_translation_invariance_residual(kernel: np.ndarray) -> float:
    count = len(kernel)
    return max(
        abs(kernel[left ^ shift, right ^ shift] - kernel[left, right])
        for shift in range(count)
        for left in range(count)
        for right in range(count)
    )


def orientation_operator_schmidt_ranks(
    kernel: np.ndarray,
    bit_count: int,
    *,
    tolerance: float = 1e-9,
) -> tuple[tuple[int, ...], tuple[int, ...]]:
    count = 1 << bit_count
    if kernel.shape != (count, count):
        raise ValueError("kernel dimension does not match bit count")
    ranks = []
    maxima = []
    for cut in range(1, bit_count):
        left_count = 1 << cut
        right_count = 1 << (bit_count - cut)
        reshaped = np.zeros(
            (left_count**2, right_count**2),
            dtype=complex,
        )
        for left in range(count):
            for right in range(count):
                left_row = left & (left_count - 1)
                right_row = left >> cut
                left_column = right & (left_count - 1)
                right_column = right >> cut
                reshaped[
                    left_row * left_count + left_column,
                    right_row * right_count + right_column,
                ] = kernel[left, right]
        ranks.append(int(np.linalg.matrix_rank(reshaped, tol=tolerance)))
        maxima.append(min(left_count**2, right_count**2))
    return tuple(ranks), tuple(maxima)


def maximum_local_factor_commutator_norm(
    label: Label,
) -> float:
    group = tuple(_source_representation_rows(label[0]))
    unique: dict[tuple[float, ...], np.ndarray] = {}
    for left in group:
        for right in group:
            matrix = local_character_factor_matrix(label, left, right)
            key = tuple(float(round(value.real, 12)) for value in matrix.reshape(-1))
            unique[key] = matrix
    matrices = tuple(unique.values())
    return max(
        (
            float(np.linalg.norm(left @ right - right @ left, ord="fro"))
            for left in matrices
            for right in matrices
        ),
        default=0.0,
    )


def audit_character_tensor_kernel(
    n: int,
    target: Partition,
    labels: tuple[Label, ...],
    *,
    control_id: str,
    tolerance: float = 1e-9,
) -> CharacterTensorKernelControl:
    _, _, projectors = predicted_joint_multiplicity_operator(target, labels)
    direct = orientation_overlap_kernel(
        projectors,
        hook_length_dimension(target),
    )
    predicted = character_tensor_orientation_kernel(target, labels)
    formula_residual = float(np.linalg.norm(direct - predicted, ord="fro"))
    hermiticity = float(np.linalg.norm(direct - direct.conj().T, ord="fro"))
    minimum = float(np.linalg.eigvalsh((direct + direct.conj().T) / 2.0)[0])
    translation = float(boolean_translation_invariance_residual(direct))
    walsh = walsh_matrix(len(labels))
    transformed = walsh @ direct @ walsh.conj().T
    offdiagonal = transformed - np.diag(np.diag(transformed))
    offdiagonal_norm = float(np.linalg.norm(offdiagonal, ord="fro"))
    total_norm = float(np.linalg.norm(transformed, ord="fro"))
    ranks, maxima = orientation_operator_schmidt_ranks(direct, len(labels))
    commutator = max(
        maximum_local_factor_commutator_norm(label) for label in labels
    )
    formula_orbits = simultaneous_pair_orbit_count_formula(n)
    direct_orbits = simultaneous_pair_orbit_count_direct(n)
    orbit_residual = abs(formula_orbits - direct_orbits)
    walsh_valid = translation <= 100 * tolerance and offdiagonal_norm <= 100 * tolerance
    product_valid = all(rank <= 1 for rank in ranks)
    local_basis_valid = commutator <= 100 * tolerance
    verified = bool(
        formula_residual <= 100 * tolerance
        and hermiticity <= 100 * tolerance
        and minimum >= -100 * tolerance
        and orbit_residual == 0
        and not walsh_valid
        and not product_valid
        and not local_basis_valid
    )
    return CharacterTensorKernelControl(
        control_id=control_id,
        n=n,
        target=target,
        labels=labels,
        group_order=math.factorial(n),
        orientation_qubit_count=len(labels),
        orientation_dimension=1 << len(labels),
        character_pair_summand_count=math.factorial(n) ** 2,
        simultaneous_pair_orbit_count_formula=formula_orbits,
        simultaneous_pair_orbit_count_direct=direct_orbits,
        pair_orbit_count_residual=orbit_residual,
        character_tensor_formula_residual=formula_residual,
        hermiticity_residual=hermiticity,
        minimum_kernel_eigenvalue=minimum,
        boolean_translation_invariance_residual=translation,
        walsh_offdiagonal_frobenius_norm=offdiagonal_norm,
        walsh_offdiagonal_fraction=(offdiagonal_norm / total_norm if total_norm else 0.0),
        operator_schmidt_ranks=ranks,
        operator_schmidt_maximum_possible_ranks=maxima,
        maximum_local_character_factor_commutator_norm=commutator,
        boolean_walsh_diagonalization_valid=walsh_valid,
        product_orientation_kernel_valid=product_valid,
        fixed_local_simultaneous_diagonalization_valid=local_basis_valid,
        exact_character_tensor_boundary_verified=verified,
        status=(
            "exact-character-tensor-network-simple-transforms-rejected"
            if verified
            else "character-tensor-boundary-control-failure"
        ),
    )


def character_tensor_scaling(n: int) -> CharacterTensorScalingRecord:
    if n < 2:
        raise ValueError("n must be at least two")
    log_order = math.log2(math.factorial(n))
    return CharacterTensorScalingRecord(
        n=n,
        log2_group_order=log_order,
        information_threshold_orientation_qubits=math.ceil(log_order),
        log2_raw_character_pair_summand_count=2.0 * log_order,
        log2_simultaneous_pair_orbit_count_lower_bound=log_order,
        simultaneous_conjugacy_orbit_enumeration_polynomial=False,
        symmetric_group_qft_alone_contracts_pair_network=False,
        internal_kronecker_multiplicity_transform_compiled=False,
        direct_orientation_kernel_polar_compiled=False,
        status="character-network-exact-global-recoupling-transform-open",
    )


def run_character_tensor_boundary() -> CharacterTensorBoundaryReport:
    threshold_labels = (
        ((3,), (2, 1)),
        ((3,), (1, 1, 1)),
        ((2, 1), (1, 1, 1)),
    )
    w4_labels = _w4_collision_free_labels()[0]
    controls = [
        audit_character_tensor_kernel(
            3,
            (2, 1),
            threshold_labels,
            control_id="W3-THRESHOLD-STANDARD-CHARACTER-TENSOR",
        ),
        audit_character_tensor_kernel(
            4,
            (2, 2),
            w4_labels,
            control_id="W4-COLLISION-FREE-22-CHARACTER-TENSOR",
        ),
        audit_character_tensor_kernel(
            4,
            (2, 1, 1),
            w4_labels,
            control_id="W4-COLLISION-FREE-211-CHARACTER-TENSOR",
        ),
    ]
    scaling = [character_tensor_scaling(n) for n in (8, 16, 32, 64, 128, 256, 512)]
    verified = all(row.exact_character_tensor_boundary_verified for row in controls)
    theorem = CharacterTensorBoundaryTheorem(
        exact_character_network=(
            "H_nu[e,f]=(d_nu|G|^2)^-1 sum_(x,y) chi_nu(xy) "
            "product_i Q_i(x,y)[e_i,f_i]."
        ),
        simultaneous_conjugacy=(
            "Every summand is invariant under (x,y)->(gxg^-1,gyg^-1)."
        ),
        orbit_count=(
            "The simultaneous-pair orbit count is |G|^-1 sum_z |C_G(z)|^2; "
            "for S_n it is sum_alpha z_alpha>=n!."
        ),
        walsh_boundary=(
            "Exact controls violate H[e xor a,f xor a]=H[e,f], so Boolean Walsh "
            "diagonalization is not a universal source-conditioned transform."
        ),
        tensor_product_boundary=(
            "Exact controls attain nontrivial and sometimes maximal operator-Schmidt "
            "rank across orientation cuts."
        ),
        local_basis_boundary=(
            "The local Q_i(x,y) family has nonzero commutators, excluding a fixed "
            "one-qubit simultaneous eigenbasis."
        ),
        surviving_transform=(
            "A positive route must coherently contract the global character network "
            "through internal Kronecker/Racah multiplicity registers."
        ),
        scope=(
            "The finite structural falsifiers reject universal simple ansatzes, not "
            "source-dependent polynomial-bond tensor networks or arbitrary circuits."
        ),
        theorem_verified=verified,
        status=(
            "orientation-character-network-identified-global-recoupling-open"
            if verified
            else "character-tensor-boundary-control-failure"
        ),
    )
    tail = scaling[-1]
    return CharacterTensorBoundaryReport(
        created_at=utc_now(),
        theorem_contract=asdict(theorem),
        theorem=theorem,
        finite_controls=controls,
        scaling_records=scaling,
        proof_obligations=[
            {
                "obligation": "derive_exact_orientation_kernel_character_network",
                "resolved": verified,
                "resolution": (
                    "Expanding both invariant projectors factors every source pair "
                    "into the local 2x2 matrix Q_i(x,y)."
                ),
            },
            {
                "obligation": "test_boolean_walsh_diagonalization_shortcut",
                "resolved": verified,
                "resolution": "Rejected by exact nontranslation-invariant controls.",
            },
            {
                "obligation": "test_product_or_fixed_local_basis_shortcuts",
                "resolved": verified,
                "resolution": (
                    "Operator-Schmidt ranks and local factor commutators reject both "
                    "universal ansatzes."
                ),
            },
            {
                "obligation": "compile_global_kronecker_racah_character_contraction",
                "resolved": False,
                "resolution": (
                    "Neither pair-orbit enumeration nor the label-only S_n QFT resolves "
                    "internal multiplicity spaces."
                ),
            },
        ],
        adversarial_audit=[
            {
                "objection": "H_nu is a Boolean convolution because orientations are bit strings.",
                "resolved": True,
                "resolution": (
                    "Bit labels do not imply XOR covariance; unequal source irreps make "
                    "the orientation diagonal and overlap depend on absolute bits."
                ),
            },
            {
                "objection": "The character formula is efficient because characters are polynomial-time computable.",
                "resolved": True,
                "resolution": (
                    "Entry evaluation and coherent global contraction are different. "
                    "The simultaneous-conjugacy quotient still has at least n! terms."
                ),
            },
            {
                "objection": "A fixed local rotation diagonalizes every Q_i(x,y).",
                "resolved": True,
                "resolution": "Exact local commutators are nonzero in every control.",
            },
            {
                "objection": "Finite maximal Schmidt rank proves every tensor network is exponential.",
                "resolved": False,
                "resolution": (
                    "No. Source-dependent recoupling trees with polynomial internal bond "
                    "descriptions remain possible and require an asymptotic theorem."
                ),
            },
        ],
        headline_metrics={
            "exact_character_tensor_network_theorem_count": int(verified),
            "simultaneous_pair_orbit_formula_count": int(verified),
            "boolean_walsh_shortcut_falsifier_count": sum(
                not row.boolean_walsh_diagonalization_valid for row in controls
            ),
            "product_kernel_shortcut_falsifier_count": sum(
                not row.product_orientation_kernel_valid for row in controls
            ),
            "fixed_local_basis_shortcut_falsifier_count": sum(
                not row.fixed_local_simultaneous_diagonalization_valid
                for row in controls
            ),
            "finite_control_count": len(controls),
            "finite_control_failure_count": sum(
                not row.exact_character_tensor_boundary_verified for row in controls
            ),
            "tail_n": tail.n,
            "tail_log2_pair_orbit_lower_bound": (
                tail.log2_simultaneous_pair_orbit_count_lower_bound
            ),
            "global_kronecker_racah_transform_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "orientation_kernel_character_tensor_network_identified": verified,
            "simultaneous_conjugacy_orbit_formula_proved": verified,
            "boolean_walsh_diagonalization_is_universal": False,
            "product_orientation_transform_is_universal": False,
            "fixed_local_diagonalizing_basis_exists": False,
            "explicit_pair_orbit_enumeration_polynomial": False,
            "global_kronecker_racah_transform_compiled": False,
            "direct_orientation_kernel_polar_compiled": False,
            "actual_physical_pgm_rejected": False,
            "polynomial_joint_decoder_proved": False,
            "classical_separation_proved": False,
            "speedup_claim_allowed": False,
        },
        status=theorem.status,
        summary=(
            "Identified the exact two-group character tensor network for H_nu and "
            "rejected Walsh, product-kernel, fixed-local-basis, and explicit orbit "
            "enumeration shortcuts. The remaining target is a genuinely global "
            "Kronecker/Racah multiplicity transform."
        ),
        falsifiers_triggered=[
            "Orientation bit strings do not make the physical kernel an XOR convolution.",
            "Polynomial character evaluation does not collapse the factorial simultaneous-pair orbit space.",
            "A direct physical polar cannot be assembled from one fixed local orientation basis.",
        ],
    )


def write_character_tensor_boundary_report(
    path: Path = REPORT_PATH,
) -> dict[str, Any]:
    payload = asdict(run_character_tensor_boundary())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return payload


if __name__ == "__main__":
    report = write_character_tensor_boundary_report()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))

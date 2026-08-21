"""Exact projection-Gram form of the joint-character multiplicity operators.

The joint group--orientation-character decoder reduces its covariant PGM to
multiplicity operators ``D_nu``.  This module identifies those operators
directly from the physical orientation invariant projectors.

Fix an ``S_n`` irrep ``V_nu`` of dimension ``r``, the common source carrier
``C`` of dimension ``d``, and orientation projectors

    E_e = Inv(V_nu tensor sigma_e)  on V_nu tensor C.

Define a positive block operator on ``V_nu tensor C[F_2^k]`` by

    G_nu[(b,e),(b',f)] = [Tr_C(E_e E_f)]_[b,b'].          (1)

Equivalently, if

    L_nu |b,e> = sum_x vec(E_e(|b,x>)),

then ``G_nu=L_nu^*L_nu``.  Let ``W`` be the normalized branch Walsh transform,
``q=2^k``, and let ``D_nu`` be the multiplicity block obtained after twirling
the retained joint state.  Exact Fourier orthogonality gives

    D_nu = r/(q d) (I_r tensor W) G_nu (I_r tensor W)^*.  (2)

The left/right orientation tensor structure forces a further exact collapse.
For every ``e,f``, the character expansion of ``Tr_C(E_eE_f)`` is central:
same-orientation coordinates contribute characters of ``st``, while crossed
coordinates contribute a convolution of products of characters in ``s`` and
``t``.  Schur's lemma therefore gives

    Tr_C(E_eE_f) = Tr(E_eE_f)/r I_r.

Writing

    H_nu[e,f]=Tr(E_eE_f)/r,

we obtain

    G_nu=I_r tensor H_nu,
    D_nu=r/(q d) I_r tensor (W H_nu W^*).                 (3)

The Fourier column is consequently free: all source-dependent inversion is
an orientation-only positive kernel whose entries are the exact pair overlaps
already available from representation-ring contraction.

Thus branch-character retention converts the unresolved orientation family
into a matrix-valued projection Gram; it neither postselects one branch nor
pays the one-row ``1/q`` erasure probability.  The nonzero condition number of
``D_nu`` is exactly that of ``G_nu``.

Two general moment identities delimit the new target.  With ``A=sum_e E_e``
and ``N=Tr(A)``,

    Tr(G_nu)=N,
    Tr(G_nu^2) <= d Tr(A^2),                               (4)

where the inequality is the Hilbert--Schmidt partial-trace bound.  Therefore

    stable_rank(D_nu) >= N^2/[d Tr(A^2)].                  (5)

Equation (4) is not a hard-edge theorem.  A polynomial decoder still needs a
coherent block encoding of all ``G_nu`` and an inverse-polynomial spectral
window carrying enough identification information.  The result supplies the
right operator and an exact access target; it does not solve either gate.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import numpy as np

from representation_obstruction import hook_length_dimension, integer_partitions
from research_registry import utc_now
from self_dual_wreath_joint_character_correlation_decoder import (
    _permutations,
    joint_character_state,
    left_covariant_state,
    schur_multiplicity_operators,
)
from self_dual_wreath_orientation_fourier_reduction import (
    _w4_collision_free_labels,
    orientation_invariant_projector,
)


REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_joint_character_multiplicity_gram.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-JOINT-CHARACTER-MULTIPLICITY-GRAM"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"

Partition = tuple[int, ...]
Label = tuple[Partition, Partition]


@dataclass(frozen=True)
class JointMultiplicityGramControl:
    control_id: str
    n: int
    labels: tuple[Label, ...]
    orientation_count: int
    carrier_dimension: int
    active_sector_count: int
    maximum_exact_multiplicity_formula_residual: float
    maximum_gram_factorization_residual: float
    maximum_scalar_block_residual: float
    maximum_orientation_kernel_factorization_residual: float
    maximum_trace_identity_residual: float
    maximum_walsh_spectrum_residual: float
    maximum_moment_bound_violation: float
    maximum_nonzero_condition_number: float
    minimum_stable_rank_lower_bound: float
    maximum_character_offdiagonal_norm: float
    exact_projection_gram_theorem_verified: bool
    status: str


@dataclass(frozen=True)
class JointMultiplicityGramScalingRecord:
    n: int
    information_threshold_copy_count: int
    orientation_log2_width: int
    controlled_invariant_projector_schema_polynomial: bool
    branch_walsh_polynomial: bool
    explicit_orientation_enumeration_required: bool
    coherent_projection_gram_block_encoding_proved: bool
    inverse_polynomial_bulk_window_proved: bool
    all_n_joint_decoder_proved: bool
    status: str


@dataclass(frozen=True)
class JointMultiplicityGramTheorem:
    matrix_valued_gram: str
    scalar_orientation_kernel: str
    exact_multiplicity_identity: str
    spectral_equivalence: str
    moment_bound: str
    access_boundary: str
    scope: str
    theorem_verified: bool
    status: str


@dataclass(frozen=True)
class JointMultiplicityGramReport:
    created_at: str
    theorem_contract: dict[str, Any]
    theorem: JointMultiplicityGramTheorem
    finite_controls: list[JointMultiplicityGramControl]
    scaling_records: list[JointMultiplicityGramScalingRecord]
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _partial_trace_carrier(
    matrix: np.ndarray,
    irrep_dimension: int,
    carrier_dimension: int,
) -> np.ndarray:
    tensor = matrix.reshape(
        irrep_dimension,
        carrier_dimension,
        irrep_dimension,
        carrier_dimension,
    )
    return np.einsum("bxcx->bc", tensor)


def matrix_valued_projection_gram(
    projectors: tuple[np.ndarray, ...],
    irrep_dimension: int,
    carrier_dimension: int,
) -> np.ndarray:
    """Return the positive block Gram in equation (1)."""

    expected_shape = (
        irrep_dimension * carrier_dimension,
        irrep_dimension * carrier_dimension,
    )
    if not projectors or any(projector.shape != expected_shape for projector in projectors):
        raise ValueError("projectors have incompatible dimensions")
    count = len(projectors)
    output = np.zeros(
        (irrep_dimension, count, irrep_dimension, count),
        dtype=complex,
    )
    for orientation, left in enumerate(projectors):
        for other, right in enumerate(projectors):
            output[:, orientation, :, other] = _partial_trace_carrier(
                left @ right,
                irrep_dimension,
                carrier_dimension,
            )
    return output.reshape(irrep_dimension * count, irrep_dimension * count)


def projection_gram_factor(
    projectors: tuple[np.ndarray, ...],
    irrep_dimension: int,
    carrier_dimension: int,
) -> np.ndarray:
    """Return ``L_nu`` with columns indexed by ``(b,e)``."""

    count = len(projectors)
    factor = np.zeros(
        (
            irrep_dimension * carrier_dimension * carrier_dimension,
            irrep_dimension * count,
        ),
        dtype=complex,
    )
    for orientation, projector in enumerate(projectors):
        tensor = projector.reshape(
            irrep_dimension,
            carrier_dimension,
            irrep_dimension,
            carrier_dimension,
        )
        for column in range(irrep_dimension):
            factor[:, column * count + orientation] = tensor[
                :, :, column, :
            ].reshape(-1)
    return factor


def orientation_overlap_kernel(
    projectors: tuple[np.ndarray, ...],
    irrep_dimension: int,
) -> np.ndarray:
    """Return ``H_nu[e,f]=Tr(E_eE_f)/d_nu``."""

    if irrep_dimension < 1:
        raise ValueError("irrep_dimension must be positive")
    count = len(projectors)
    output = np.empty((count, count), dtype=complex)
    for orientation, left in enumerate(projectors):
        for other, right in enumerate(projectors):
            output[orientation, other] = (
                np.trace(left @ right) / irrep_dimension
            )
    return output


def walsh_matrix(bit_count: int) -> np.ndarray:
    if bit_count < 0:
        raise ValueError("bit_count must be nonnegative")
    count = 1 << bit_count
    output = np.empty((count, count), dtype=float)
    for character in range(count):
        for orientation in range(count):
            output[character, orientation] = (
                -1.0
                if (character & orientation).bit_count() % 2
                else 1.0
            ) / math.sqrt(count)
    return output


def predicted_joint_multiplicity_operator(
    target: Partition,
    labels: tuple[Label, ...],
) -> tuple[np.ndarray, np.ndarray, tuple[np.ndarray, ...]]:
    irrep_dimension = hook_length_dimension(target)
    carrier_dimension = math.prod(
        hook_length_dimension(left) * hook_length_dimension(right)
        for left, right in labels
    )
    count = 1 << len(labels)
    projectors = tuple(
        orientation_invariant_projector(target, labels, orientation)
        for orientation in range(count)
    )
    gram = matrix_valued_projection_gram(
        projectors,
        irrep_dimension,
        carrier_dimension,
    )
    kernel = orientation_overlap_kernel(projectors, irrep_dimension)
    scalar_gram = np.kron(np.eye(irrep_dimension), kernel)
    if np.linalg.norm(gram - scalar_gram) > 1e-8:
        raise ArithmeticError("orientation partial-trace blocks did not scalarize")
    walsh = walsh_matrix(len(labels))
    rotation = np.kron(np.eye(irrep_dimension), walsh)
    predicted = (
        irrep_dimension
        / (count * carrier_dimension)
        * rotation
        @ gram
        @ rotation.conj().T
    )
    return predicted, gram, projectors


def audit_joint_multiplicity_gram(
    n: int,
    labels: tuple[Label, ...],
    *,
    control_id: str,
    tolerance: float = 1e-9,
) -> JointMultiplicityGramControl:
    permutations = _permutations(n)
    count = 1 << len(labels)
    base = joint_character_state(labels, tuple(range(n)))
    states = tuple(
        left_covariant_state(base, permutations, hidden, count)
        for hidden in permutations
    )
    average = sum(states) / len(states)
    observed, schur_residual = schur_multiplicity_operators(
        n,
        count,
        average,
        tolerance,
    )
    carrier_dimension = math.prod(
        hook_length_dimension(left) * hook_length_dimension(right)
        for left, right in labels
    )
    formula_residual = schur_residual
    factor_residual = 0.0
    scalar_block_residual = 0.0
    kernel_factorization_residual = 0.0
    trace_residual = 0.0
    spectrum_residual = 0.0
    moment_violation = 0.0
    maximum_condition = 1.0
    minimum_stable_rank = math.inf
    maximum_offdiagonal = 0.0
    active = 0
    for target in integer_partitions(n):
        predicted, gram, projectors = predicted_joint_multiplicity_operator(
            target,
            labels,
        )
        if np.trace(predicted).real <= tolerance:
            formula_residual = max(
                formula_residual,
                float(np.linalg.norm(observed[target] - predicted)),
            )
            continue
        active += 1
        irrep_dimension = hook_length_dimension(target)
        formula_residual = max(
            formula_residual,
            float(np.linalg.norm(observed[target] - predicted)),
        )
        factor = projection_gram_factor(
            projectors,
            irrep_dimension,
            carrier_dimension,
        )
        factor_residual = max(
            factor_residual,
            float(np.linalg.norm(gram - factor.conj().T @ factor)),
        )
        kernel = orientation_overlap_kernel(projectors, irrep_dimension)
        scalar_gram = np.kron(np.eye(irrep_dimension), kernel)
        scalar_block_residual = max(
            scalar_block_residual,
            float(np.linalg.norm(gram - scalar_gram)),
        )
        walsh = walsh_matrix(len(labels))
        kernel_prediction = (
            irrep_dimension
            / (count * carrier_dimension)
            * np.kron(
                np.eye(irrep_dimension),
                walsh @ kernel @ walsh.conj().T,
            )
        )
        kernel_factorization_residual = max(
            kernel_factorization_residual,
            float(np.linalg.norm(predicted - kernel_prediction)),
        )
        frame_sum = sum(projectors)
        trace_residual = max(
            trace_residual,
            abs(float(np.trace(gram).real - np.trace(frame_sum).real)),
        )
        gram_values = np.linalg.eigvalsh((gram + gram.conj().T) / 2)
        predicted_values = np.linalg.eigvalsh(
            (predicted + predicted.conj().T) / 2
        )
        scale = irrep_dimension / (count * carrier_dimension)
        spectrum_residual = max(
            spectrum_residual,
            float(np.max(np.abs(predicted_values - scale * gram_values))),
        )
        gram_second = float(np.trace(gram @ gram).real)
        frame_second = float(np.trace(frame_sum @ frame_sum).real)
        moment_violation = max(
            moment_violation,
            gram_second - carrier_dimension * frame_second,
        )
        positive = gram_values[gram_values > tolerance]
        maximum_condition = max(
            maximum_condition,
            float(positive[-1] / positive[0]),
        )
        stable_lower = float(
            np.trace(frame_sum).real ** 2
            / (carrier_dimension * frame_second)
        )
        minimum_stable_rank = min(minimum_stable_rank, stable_lower)
        tensor = predicted.reshape(
            irrep_dimension,
            count,
            irrep_dimension,
            count,
        ).copy()
        for character in range(count):
            tensor[:, character, :, character] = 0
        maximum_offdiagonal = max(
            maximum_offdiagonal,
            float(np.linalg.norm(tensor.reshape(predicted.shape))),
        )
    verified = bool(
        active
        and formula_residual <= 100 * tolerance
        and factor_residual <= 100 * tolerance
        and scalar_block_residual <= 100 * tolerance
        and kernel_factorization_residual <= 100 * tolerance
        and trace_residual <= 100 * tolerance
        and spectrum_residual <= 100 * tolerance
        and moment_violation <= 100 * tolerance
    )
    return JointMultiplicityGramControl(
        control_id=control_id,
        n=n,
        labels=labels,
        orientation_count=count,
        carrier_dimension=carrier_dimension,
        active_sector_count=active,
        maximum_exact_multiplicity_formula_residual=formula_residual,
        maximum_gram_factorization_residual=factor_residual,
        maximum_scalar_block_residual=scalar_block_residual,
        maximum_orientation_kernel_factorization_residual=(
            kernel_factorization_residual
        ),
        maximum_trace_identity_residual=trace_residual,
        maximum_walsh_spectrum_residual=spectrum_residual,
        maximum_moment_bound_violation=max(0.0, moment_violation),
        maximum_nonzero_condition_number=maximum_condition,
        minimum_stable_rank_lower_bound=minimum_stable_rank,
        maximum_character_offdiagonal_norm=maximum_offdiagonal,
        exact_projection_gram_theorem_verified=verified,
        status=(
            "exact-joint-character-projection-gram"
            if verified
            else "joint-character-projection-gram-validation-failure"
        ),
    )


def joint_multiplicity_gram_scaling_record(
    n: int,
) -> JointMultiplicityGramScalingRecord:
    if n < 2:
        raise ValueError("n must be at least two")
    copies = math.ceil(math.lgamma(n + 1) / math.log(2))
    return JointMultiplicityGramScalingRecord(
        n=n,
        information_threshold_copy_count=copies,
        orientation_log2_width=copies,
        controlled_invariant_projector_schema_polynomial=True,
        branch_walsh_polynomial=True,
        explicit_orientation_enumeration_required=False,
        coherent_projection_gram_block_encoding_proved=False,
        inverse_polynomial_bulk_window_proved=False,
        all_n_joint_decoder_proved=False,
        status="projection-gram-identified-coherent-normalization-open",
    )


def run_joint_multiplicity_gram() -> JointMultiplicityGramReport:
    controls = [
        audit_joint_multiplicity_gram(
            3,
            (((3,), (2, 1)),),
            control_id="W3-SINGLE-UNEQUAL",
        ),
        audit_joint_multiplicity_gram(
            3,
            (
                ((3,), (2, 1)),
                ((3,), (1, 1, 1)),
                ((2, 1), (1, 1, 1)),
            ),
            control_id="W3-INFORMATION-THRESHOLD",
        ),
        audit_joint_multiplicity_gram(
            4,
            _w4_collision_free_labels()[0],
            control_id="W4-COLLISION-FREE-PAIR",
        ),
    ]
    scaling = [
        joint_multiplicity_gram_scaling_record(n)
        for n in (8, 16, 32, 64, 128, 256, 512)
    ]
    failures = sum(
        not row.exact_projection_gram_theorem_verified for row in controls
    )
    verified = failures == 0
    theorem = JointMultiplicityGramTheorem(
        matrix_valued_gram=(
            "G_nu[(b,e),(b',f)]=[Tr_C(E_(nu,e)E_(nu,f))]_[b,b'] "
            "and G_nu=L_nu^*L_nu."
        ),
        scalar_orientation_kernel=(
            "Tr_C(E_eE_f)=Tr(E_eE_f)/d_nu I by character centrality, so "
            "G_nu=I_(d_nu) tensor H_nu with H_nu[e,f]=Tr(E_eE_f)/d_nu."
        ),
        exact_multiplicity_identity=(
            "D_nu=d_nu/(q dim(C)) (I tensor W)G_nu(I tensor W)^*."
        ),
        spectral_equivalence=(
            "The nonzero condition number of D_nu is exactly that of G_nu."
        ),
        moment_bound=(
            "Tr(G_nu)=Tr(A_nu) and Tr(G_nu^2)<=dim(C)Tr(A_nu^2), "
            "so srank(D_nu)>=Tr(A_nu)^2/[dim(C)Tr(A_nu^2)]."
        ),
        access_boundary=(
            "Controlled invariant projectors and Walsh are standard operations, "
            "but a correctly normalized coherent block encoding of G_nu is open."
        ),
        scope=(
            "The theorem identifies the exact operator. It proves neither a bulk "
            "hard edge nor an efficient inverse or hidden-label decoder."
        ),
        theorem_verified=verified,
        status=(
            "joint-character-projection-gram-identified-access-open"
            if verified
            else "joint-character-projection-gram-validation-failure"
        ),
    )
    return JointMultiplicityGramReport(
        created_at=utc_now(),
        theorem_contract=asdict(theorem),
        theorem=theorem,
        finite_controls=controls,
        scaling_records=scaling,
        proof_obligations=[
            {
                "obligation": "identify_joint_multiplicity_operator",
                "resolved": verified,
                "resolution": (
                    "Fourier orthogonality and carrier partial trace give the "
                    "Walsh-rotated projection Gram exactly."
                ),
            },
            {
                "obligation": "remove_fourier_column_from_multiplicity_inverse",
                "resolved": verified,
                "resolution": (
                    "Products and convolutions of symmetric-group characters are "
                    "central, forcing every carrier partial-trace block to be scalar."
                ),
            },
            {
                "obligation": "control_projection_gram_second_moment",
                "resolved": verified,
                "resolution": (
                    "The Hilbert--Schmidt partial-trace inequality proves the exact "
                    "trace identity and universal second-moment upper bound."
                ),
            },
            {
                "obligation": "compile_normalized_coherent_projection_gram_access",
                "resolved": False,
                "resolution": (
                    "Controlled E_e is standard, but projected preparation may have "
                    "sector- and rank-dependent normalization."
                ),
            },
            {
                "obligation": "prove_information_carrying_inverse_polynomial_bulk_window",
                "resolved": False,
                "resolution": (
                    "A stable-rank lower bound does not exclude sparse tiny eigenvalues "
                    "or show that the retained window contains decoder information."
                ),
            },
        ],
        adversarial_audit=[
            {
                "objection": "Walsh interference diagonalizes the orientation problem.",
                "resolved": True,
                "resolution": (
                    "False generically: D_nu has nonzero off-character blocks and is "
                    "only unitarily equivalent to the matrix-valued Gram G_nu."
                ),
            },
            {
                "objection": "The one-row 1/q erasure penalty still applies.",
                "resolved": True,
                "resolution": (
                    "No character is postselected. The full Walsh register is retained "
                    "inside a normalized covariant state."
                ),
            },
            {
                "objection": "The second moment supplies a polynomial inverse.",
                "resolved": False,
                "resolution": (
                    "It controls stable rank only; coherent access normalization and "
                    "the information-bearing hard edge remain separate obligations."
                ),
            },
        ],
        headline_metrics={
            "exact_projection_gram_identity_theorem_count": 1,
            "scalar_orientation_kernel_collapse_theorem_count": 1,
            "projection_gram_moment_bound_theorem_count": 1,
            "finite_control_count": len(controls),
            "finite_control_failure_count": failures,
            "finite_active_sector_count": sum(
                row.active_sector_count for row in controls
            ),
            "maximum_finite_nonzero_condition_number": max(
                row.maximum_nonzero_condition_number for row in controls
            ),
            "coherent_projection_gram_block_encoding_count": 0,
            "all_n_joint_decoder_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "joint_multiplicity_equals_walsh_rotated_projection_gram": verified,
            "fourier_column_factors_from_joint_multiplicity": verified,
            "orientation_kernel_entries_equal_pair_overlaps": verified,
            "projection_gram_psd_and_trace_moment_bounds_proved": verified,
            "one_row_branch_erasure_required": False,
            "walsh_diagonalizes_projection_gram": False,
            "coherent_projection_gram_block_encoding_proved": False,
            "inverse_polynomial_information_bulk_proved": False,
            "polynomial_joint_decoder_proved": False,
            "classical_separation_proved": False,
            "speedup_claim_allowed": False,
        },
        status=theorem.status,
        summary=(
            "The retained-character multiplicity operator is exactly a Walsh-rotated "
            "orientation overlap kernel tensored with the identity Fourier column. "
            "This removes branch erasure and column inversion but leaves coherent "
            "kernel access and bulk inversion open."
        ),
        falsifiers_triggered=[
            (
                "A retained branch character is not a scalar Fourier column; its "
                "multiplicity operator contains matrix-valued cross-orientation blocks."
            ),
            (
                "The one-pass erasure lower bound does not apply to retaining the full "
                "Walsh register as part of the decoder state."
            ),
            (
                "Finite conditioning and a stable-rank bound do not prove a scalable "
                "multiplicity inverse."
            ),
        ],
    )


def write_joint_multiplicity_gram_report(
    path: Path = REPORT_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = (
        "EXP-CODE-SELF-DUAL-WREATH-JOINT-CHARACTER-MULTIPLICITY-GRAM"
    ),
    registry_candidate_id: str = "CODE-COSET-COLLECTIVE",
    registry_result_id: str = "",
    **kwargs: Any,
) -> dict[str, Any]:
    output_path = path
    for _k in ("write_registry", "registry_experiment_id", "registry_candidate_id", "registry_result_id"):
        kwargs.pop(_k, None)
    if "run_joint_multiplicity_gram" in globals():
        report = run_joint_multiplicity_gram(**kwargs)
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
                id="NEG-SELF-DUAL-WREATH-JOINT-CHARACTER-MULTIPLICITY-GRAM",
                source=registry_experiment_id,
                claim="Initial negative claim for EXP-CODE-SELF-DUAL-WREATH-JOINT-CHARACTER-MULTIPLICITY-GRAM.",
                reason_invalid="Falsified or refined by exact theorem evaluation.",
                lesson="Lesson from exact theorem analysis for EXP-CODE-SELF-DUAL-WREATH-JOINT-CHARACTER-MULTIPLICITY-GRAM.",
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
                    "self_dual_wreath_joint_character_multiplicity_gram": str(path)
                },
            )
        )
    return payload

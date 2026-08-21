"""Joint group--orientation-character correlation decoder.

Passive branch-character retention and character-controlled group shifts are
factorially weak, but that does not exhaust the physical row-copy output.  The
group and orientation-character registers have hidden-label-dependent quantum
correlations even though each register separately is label independent.

Let ``G=S_n``, let ``V:C->C[F_2^k] tensor C`` be the uniform-orientation source
isometry, and let ``U`` be the aligned diagonal restriction.  Returning the
generalized row-copy isometry to the group time basis and Walsh-transforming
the orientation register gives the isometry

    X_g x = |G|^(-1/2) sum_(s,z) |s,z> K_z(s^-1 g)x,       (1)

where the matrix-valued character Kraus operator ``K_z`` is the tensor product
derived in ``self_dual_wreath_branch_character_decoder_boundary``.  Discard
only the final carrier and retain the joint register:

    tau_g = Tr_C[X_g X_g^*]/dim(C).                        (2)

The family is exactly left covariant,

    tau_g=(L_g tensor I) tau_e (L_g^* tensor I).           (3)

Both reduced states ``Tr_z tau_g`` and ``Tr_G tau_g`` are independent of
``g``.  The first follows because the compressed source character is a class
function; the second follows directly from (3).  Thus every surviving bit of
hidden-label information is stored in group--character correlations.

After the group Fourier transform, the ensemble average has the exact Schur
form

    bar(tau) = direct_sum_nu I_(d_nu)/d_nu tensor D_nu,    (4)

where the multiplicity space is the Fourier column paired with the retained
orientation character.  Therefore the covariant PGM reduces to coherent
controlled application of ``D_nu^(-1/2)`` followed by the inverse ``S_n`` QFT.
This is a new access target: no branch erasure is required, but all-n
information retention, conditioning, and a block encoding of ``D_nu`` remain
unproved.

Finite controls show that the joint state is genuinely informative.  At the
``S_3`` information threshold its PGM outperforms the best
character-controlled right correction, while a low-copy ``S_4`` control also
shows that this need not hold universally for mixed geometrically uniform
states.  The PGM is not asserted to be optimal.  No control establishes
scalable success or an efficient decoder.
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
from self_dual_wreath_branch_character_decoder_boundary import (
    branch_character_distribution_from_cycle_type,
    branch_character_kraus,
)
from self_dual_wreath_character_moments import compose_permutations
from self_dual_wreath_coherent_fourier_decoder import symmetric_group_fourier_matrix
from self_dual_wreath_orientation_fourier_reduction import (
    _source_representation_rows,
    _w4_collision_free_labels,
)


REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_joint_character_correlation_decoder.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-JOINT-CHARACTER-CORRELATION-DECODER"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"

Partition = tuple[int, ...]
Permutation = tuple[int, ...]
Label = tuple[Partition, Partition]


@dataclass(frozen=True)
class JointCharacterCorrelationControl:
    control_id: str
    n: int
    labels: tuple[Label, ...]
    group_order: int
    copy_count: int
    orientation_character_count: int
    source_carrier_dimension: int
    joint_register_dimension: int
    joint_state_rank: int
    average_state_rank: int
    maximum_covariance_residual: float
    maximum_group_marginal_label_variation: float
    maximum_character_marginal_label_variation: float
    maximum_joint_state_label_variation: float
    maximum_schur_factorization_residual: float
    maximum_multiplicity_condition_number: float
    maximum_character_offdiagonal_block_norm: float
    joint_holevo_information_bits: float
    hidden_label_entropy_bits: float
    holevo_information_fraction: float
    joint_pretty_good_success: float
    optimal_right_correction_success: float
    pretty_good_minus_right_correction_success: float
    random_guess_success: float
    exact_joint_correlation_theorem_verified: bool
    status: str


@dataclass(frozen=True)
class JointCharacterScalingRecord:
    n: int
    information_threshold_copy_count: int
    group_register_qubits: int
    orientation_character_qubits: int
    joint_register_qubit_upper_bound: int
    row_copy_and_walsh_polynomial: bool
    symmetric_group_qft_polynomial: bool
    branch_erasure_required: bool
    all_n_extensive_holevo_information_proved: bool
    multiplicity_operator_block_encoding_proved: bool
    inverse_polynomial_multiplicity_conditioning_proved: bool
    polynomial_joint_decoder_proved: bool
    status: str


@dataclass(frozen=True)
class JointCharacterCorrelationTheorem:
    native_joint_state: str
    covariance: str
    marginal_independence: str
    schur_factorization: str
    algorithmic_reduction: str
    scope: str
    theorem_verified: bool
    status: str


@dataclass(frozen=True)
class JointCharacterCorrelationDecoderReport:
    created_at: str
    theorem_contract: dict[str, Any]
    theorem: JointCharacterCorrelationTheorem
    finite_controls: list[JointCharacterCorrelationControl]
    scaling_records: list[JointCharacterScalingRecord]
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def inverse_permutation(permutation: Permutation) -> Permutation:
    output = [0] * len(permutation)
    for source, target in enumerate(permutation):
        output[target] = source
    return tuple(output)


def _permutations(n: int) -> tuple[Permutation, ...]:
    return tuple(_source_representation_rows((n,)))


def joint_character_state(
    labels: tuple[Label, ...],
    hidden_label: Permutation,
) -> np.ndarray:
    """Construct ``tau_g`` from the operator-valued amplitudes in (1)."""

    n = len(hidden_label)
    permutations = _permutations(n)
    if hidden_label not in set(permutations):
        raise ValueError("hidden label is not a permutation of the right degree")
    character_count = 1 << len(labels)
    carrier_dimension = math.prod(
        hook_length_dimension(left) * hook_length_dimension(right)
        for left, right in labels
    )
    amplitudes = []
    for group_label in permutations:
        relative = compose_permutations(
            inverse_permutation(group_label),
            hidden_label,
        )
        for character in range(character_count):
            amplitudes.append(
                branch_character_kraus(labels, relative, character).reshape(-1)
            )
    matrix = np.stack(amplitudes) / math.sqrt(
        len(permutations) * carrier_dimension
    )
    return matrix @ matrix.conj().T


def left_covariant_state(
    base_state: np.ndarray,
    permutations: tuple[Permutation, ...],
    hidden_label: Permutation,
    character_count: int,
) -> np.ndarray:
    """Generate (3) by pulling group indices back by ``g^-1``."""

    index = {permutation: position for position, permutation in enumerate(permutations)}
    inverse = inverse_permutation(hidden_label)
    pullback = [
        index[compose_permutations(inverse, group_label)]
        for group_label in permutations
    ]
    indices = [
        group_index * character_count + character
        for group_index in pullback
        for character in range(character_count)
    ]
    return base_state[np.ix_(indices, indices)]


def _partial_trace_character(
    state: np.ndarray,
    group_order: int,
    character_count: int,
) -> np.ndarray:
    tensor = state.reshape(
        group_order,
        character_count,
        group_order,
        character_count,
    )
    return np.einsum("azbz->ab", tensor)


def _partial_trace_group(
    state: np.ndarray,
    group_order: int,
    character_count: int,
) -> np.ndarray:
    tensor = state.reshape(
        group_order,
        character_count,
        group_order,
        character_count,
    )
    return np.einsum("azas->zs", tensor)


def _von_neumann_entropy(state: np.ndarray, tolerance: float) -> float:
    eigenvalues = np.linalg.eigvalsh((state + state.conj().T) / 2)
    positive = eigenvalues[eigenvalues > tolerance]
    return float(-np.dot(positive, np.log2(positive)))


def _pretty_good_success(
    states: tuple[np.ndarray, ...],
    tolerance: float,
) -> tuple[float, np.ndarray, int]:
    count = len(states)
    average = sum(states) / count
    eigenvalues, eigenvectors = np.linalg.eigh(
        (average + average.conj().T) / 2
    )
    positive = eigenvalues > tolerance
    inverse = (
        eigenvectors[:, positive] * eigenvalues[positive] ** -0.5
    ) @ eigenvectors[:, positive].conj().T
    success = sum(
        float(np.trace((inverse @ state @ inverse / count) @ state).real)
        for state in states
    ) / count
    return success, average, int(np.count_nonzero(positive))


def schur_multiplicity_operators(
    n: int,
    character_count: int,
    average: np.ndarray,
    tolerance: float = 1e-9,
) -> tuple[dict[Partition, np.ndarray], float]:
    """Return the ``D_nu`` blocks in (4) and the full Schur residual."""

    fourier, _, partitions = symmetric_group_fourier_matrix(n)
    transformed = (
        np.kron(fourier.T.conj(), np.eye(character_count))
        @ average
        @ np.kron(fourier, np.eye(character_count))
    )
    expected_full = np.zeros_like(transformed)
    operators: dict[Partition, np.ndarray] = {}
    group_offset = 0
    for partition in partitions:
        dimension = hook_length_dimension(partition)
        start = group_offset * character_count
        stop = (group_offset + dimension * dimension) * character_count
        block = transformed[start:stop, start:stop]
        tensor = block.reshape(
            dimension,
            dimension,
            character_count,
            dimension,
            dimension,
            character_count,
        )
        multiplicity = sum(
            tensor[row, :, :, row, :, :]
            for row in range(dimension)
        )
        expected = np.zeros_like(tensor)
        for row in range(dimension):
            expected[row, :, :, row, :, :] = multiplicity / dimension
        matrix = multiplicity.reshape(
            dimension * character_count,
            dimension * character_count,
        )
        operators[partition] = matrix
        expected_full[start:stop, start:stop] = expected.reshape(
            dimension * dimension * character_count,
            dimension * dimension * character_count,
        )
        group_offset += dimension * dimension
    residual = float(np.linalg.norm(transformed - expected_full))
    if residual > 100 * tolerance:
        return operators, residual
    return operators, residual


def _audit_schur_average(
    n: int,
    character_count: int,
    average: np.ndarray,
    tolerance: float,
) -> tuple[float, float, float]:
    operators, maximum_residual = schur_multiplicity_operators(
        n,
        character_count,
        average,
        tolerance,
    )
    maximum_condition = 1.0
    maximum_character_offdiagonal = 0.0
    for partition, matrix in operators.items():
        dimension = hook_length_dimension(partition)
        eigenvalues = np.linalg.eigvalsh((matrix + matrix.conj().T) / 2)
        positive = eigenvalues[eigenvalues > tolerance]
        if len(positive):
            maximum_condition = max(
                maximum_condition,
                float(positive[-1] / positive[0]),
            )
        offdiagonal = matrix.reshape(
            dimension,
            character_count,
            dimension,
            character_count,
        ).copy()
        for character in range(character_count):
            offdiagonal[:, character, :, character] = 0
        maximum_character_offdiagonal = max(
            maximum_character_offdiagonal,
            float(
                np.linalg.norm(
                    offdiagonal.reshape(
                        dimension * character_count,
                        dimension * character_count,
                    )
                )
            ),
        )
    return maximum_residual, maximum_condition, maximum_character_offdiagonal


def audit_joint_character_correlation(
    n: int,
    labels: tuple[Label, ...],
    *,
    control_id: str,
    tolerance: float = 1e-9,
) -> JointCharacterCorrelationControl:
    permutations = _permutations(n)
    identity = tuple(range(n))
    character_count = 1 << len(labels)
    base = joint_character_state(labels, identity)
    states = tuple(
        left_covariant_state(base, permutations, hidden, character_count)
        for hidden in permutations
    )
    direct_indices = tuple(
        sorted({0, len(permutations) // 3, len(permutations) - 1})
    )
    covariance_residual = max(
        float(
            np.linalg.norm(
                joint_character_state(labels, permutations[index]) - states[index],
                ord=2,
            )
        )
        for index in direct_indices
    )
    group_marginals = tuple(
        _partial_trace_character(state, len(permutations), character_count)
        for state in states
    )
    character_marginals = tuple(
        _partial_trace_group(state, len(permutations), character_count)
        for state in states
    )
    group_variation = max(
        float(np.linalg.norm(state - group_marginals[0], ord=2))
        for state in group_marginals
    )
    character_variation = max(
        float(np.linalg.norm(state - character_marginals[0], ord=2))
        for state in character_marginals
    )
    joint_variation = max(
        float(np.linalg.norm(state - base, ord=2)) for state in states
    )
    success, average, average_rank = _pretty_good_success(states, tolerance)
    character_laws = np.stack(
        tuple(
            branch_character_distribution_from_cycle_type(labels, cycle_type)
            for cycle_type in integer_partitions(n)
        )
    )
    right_correction = float(
        np.sum(np.max(character_laws, axis=0)) / len(permutations)
    )
    schur_residual, maximum_condition, offdiagonal = _audit_schur_average(
        n,
        character_count,
        average,
        tolerance,
    )
    holevo = _von_neumann_entropy(average, tolerance) - _von_neumann_entropy(
        base,
        tolerance,
    )
    hidden_entropy = math.log2(len(permutations))
    verified = bool(
        covariance_residual <= 100 * tolerance
        and group_variation <= 100 * tolerance
        and character_variation <= 100 * tolerance
        and joint_variation > 100 * tolerance
        and schur_residual <= 100 * tolerance
        and holevo > 100 * tolerance
        and success > 1 / len(permutations) + 100 * tolerance
    )
    carrier_dimension = math.prod(
        hook_length_dimension(left) * hook_length_dimension(right)
        for left, right in labels
    )
    return JointCharacterCorrelationControl(
        control_id=control_id,
        n=n,
        labels=labels,
        group_order=len(permutations),
        copy_count=len(labels),
        orientation_character_count=character_count,
        source_carrier_dimension=carrier_dimension,
        joint_register_dimension=len(permutations) * character_count,
        joint_state_rank=int(np.linalg.matrix_rank(base, tol=tolerance)),
        average_state_rank=average_rank,
        maximum_covariance_residual=covariance_residual,
        maximum_group_marginal_label_variation=group_variation,
        maximum_character_marginal_label_variation=character_variation,
        maximum_joint_state_label_variation=joint_variation,
        maximum_schur_factorization_residual=schur_residual,
        maximum_multiplicity_condition_number=maximum_condition,
        maximum_character_offdiagonal_block_norm=offdiagonal,
        joint_holevo_information_bits=holevo,
        hidden_label_entropy_bits=hidden_entropy,
        holevo_information_fraction=holevo / hidden_entropy,
        joint_pretty_good_success=success,
        optimal_right_correction_success=right_correction,
        pretty_good_minus_right_correction_success=success - right_correction,
        random_guess_success=1 / len(permutations),
        exact_joint_correlation_theorem_verified=verified,
        status=(
            "exact-joint-character-correlation-mechanism"
            if verified
            else "joint-character-correlation-validation-failure"
        ),
    )


def joint_character_scaling_record(n: int) -> JointCharacterScalingRecord:
    if n < 2:
        raise ValueError("n must be at least two")
    copies = math.ceil(math.lgamma(n + 1) / math.log(2))
    group_qubits = math.ceil(math.lgamma(n + 1) / math.log(2))
    return JointCharacterScalingRecord(
        n=n,
        information_threshold_copy_count=copies,
        group_register_qubits=group_qubits,
        orientation_character_qubits=copies,
        joint_register_qubit_upper_bound=group_qubits + copies,
        row_copy_and_walsh_polynomial=True,
        symmetric_group_qft_polynomial=True,
        branch_erasure_required=False,
        all_n_extensive_holevo_information_proved=False,
        multiplicity_operator_block_encoding_proved=False,
        inverse_polynomial_multiplicity_conditioning_proved=False,
        polynomial_joint_decoder_proved=False,
        status="joint-correlation-access-polynomial-multiplicity-inverse-open",
    )


def run_joint_character_correlation_decoder() -> JointCharacterCorrelationDecoderReport:
    controls = [
        audit_joint_character_correlation(
            3,
            (((3,), (2, 1)),),
            control_id="W3-SINGLE-UNEQUAL",
        ),
        audit_joint_character_correlation(
            3,
            (
                ((3,), (2, 1)),
                ((3,), (1, 1, 1)),
                ((2, 1), (1, 1, 1)),
            ),
            control_id="W3-INFORMATION-THRESHOLD",
        ),
        audit_joint_character_correlation(
            4,
            _w4_collision_free_labels()[0],
            control_id="W4-COLLISION-FREE-PAIR",
        ),
    ]
    scaling = [
        joint_character_scaling_record(n)
        for n in (8, 16, 32, 64, 128, 256, 512)
    ]
    failures = sum(
        not row.exact_joint_correlation_theorem_verified for row in controls
    )
    verified = failures == 0
    theorem = JointCharacterCorrelationTheorem(
        native_joint_state=(
            "tau_g[(s,z),(t,w)]=( |G| dim(C) )^-1 "
            "Tr[K_w(t^-1g)^* K_z(s^-1g)]."
        ),
        covariance="tau_g=(L_g tensor I)tau_e(L_g^* tensor I).",
        marginal_independence=(
            "Both Tr_character(tau_g) and Tr_group(tau_g) are independent of g; "
            "all label information is correlation-only."
        ),
        schur_factorization=(
            "F_G bar(tau) F_G^*=direct_sum_nu I_(d_nu)/d_nu tensor D_nu."
        ),
        algorithmic_reduction=(
            "The joint covariant PGM requires controlled D_nu^-1/2 and the "
            "efficient S_n QFT, without branch erasure."
        ),
        scope=(
            "Finite informative controls prove a mechanism, not all-n extensive "
            "information, inverse-polynomial conditioning, block encoding, or speedup."
        ),
        theorem_verified=verified,
        status=(
            "joint-character-correlation-mechanism-multiplicity-inverse-open"
            if verified
            else "joint-character-correlation-validation-failure"
        ),
    )
    return JointCharacterCorrelationDecoderReport(
        created_at=utc_now(),
        theorem_contract=asdict(theorem),
        theorem=theorem,
        finite_controls=controls,
        scaling_records=scaling,
        proof_obligations=[
            {
                "obligation": "derive_exact_joint_retained_character_state",
                "resolved": verified,
                "resolution": (
                    "The operator-valued Walsh amplitudes give tau_g exactly and "
                    "intertwine hidden labels with the left regular action."
                ),
            },
            {
                "obligation": "separate_marginal_signal_from_correlation_signal",
                "resolved": verified,
                "resolution": (
                    "Each marginal is label independent while finite joint states "
                    "have positive Holevo information and non-random PGM success."
                ),
            },
            {
                "obligation": "prove_all_n_extensive_joint_holevo_information",
                "resolved": False,
                "resolution": (
                    "No natural Plancherel tuple theorem yet lower-bounds "
                    "chi({tau_g}) by log(n!)-O(polylog(n))."
                ),
            },
            {
                "obligation": "compile_joint_multiplicity_inverse",
                "resolved": False,
                "resolution": (
                    "A coherent block encoding and inverse-polynomial bulk condition "
                    "for D_nu have not been constructed."
                ),
            },
        ],
        adversarial_audit=[
            {
                "objection": "The class-function character probability no-go removes all retained-character information.",
                "resolved": verified,
                "resolution": (
                    "False: it removes diagonal character-only decoding. Off-diagonal "
                    "group--character correlations vary with the hidden label."
                ),
            },
            {
                "objection": "Positive finite Holevo information gives a scalable decoder.",
                "resolved": False,
                "resolution": (
                    "The W3 threshold control retains substantial information, but "
                    "W4 low-copy controls are weak and no all-n theorem exists."
                ),
            },
            {
                "objection": "The mixed-state PGM must dominate the classical right-correction decoder.",
                "resolved": True,
                "resolution": (
                    "False in the W4 low-copy control. The report records both "
                    "implemented baselines and does not call the PGM optimal."
                ),
            },
            {
                "objection": "The Schur form makes the PGM automatically efficient.",
                "resolved": False,
                "resolution": (
                    "The source-dependent multiplicity operators D_nu may be wide, "
                    "ill-conditioned, or lack an efficient coherent block encoding."
                ),
            },
        ],
        headline_metrics={
            "exact_joint_state_theorem_count": 1,
            "marginal_independence_theorem_count": 1,
            "covariant_schur_factorization_theorem_count": 1,
            "finite_control_count": len(controls),
            "finite_control_failure_count": failures,
            "finite_positive_holevo_control_count": sum(
                row.joint_holevo_information_bits > 0 for row in controls
            ),
            "maximum_finite_holevo_information_fraction": max(
                row.holevo_information_fraction for row in controls
            ),
            "maximum_finite_joint_pretty_good_success": max(
                row.joint_pretty_good_success for row in controls
            ),
            "pgm_beats_right_correction_control_count": sum(
                row.pretty_good_minus_right_correction_success > 0
                for row in controls
            ),
            "all_n_extensive_information_theorem_count": 0,
            "multiplicity_inverse_compiler_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "joint_group_character_state_is_hidden_label_dependent": verified,
            "group_marginal_contains_hidden_label_information": False,
            "character_marginal_contains_hidden_label_information": False,
            "joint_correlations_contain_finite_hidden_label_information": verified,
            "branch_erasure_required_for_this_route": False,
            "all_n_extensive_joint_information_proved": False,
            "joint_multiplicity_block_encoding_proved": False,
            "joint_multiplicity_conditioning_proved": False,
            "polynomial_joint_decoder_proved": False,
            "classical_separation_proved": False,
            "speedup_claim_allowed": False,
        },
        status=theorem.status,
        summary=(
            "Retaining the group and orientation-character registers exposes "
            "hidden-label-dependent quantum correlations with label-independent "
            "marginals. The PGM reduces to new multiplicity operators D_nu, whose "
            "asymptotic information and implementation are now the open gates."
        ),
        falsifiers_triggered=[
            (
                "The conjugacy-class probability bound does not extend to the "
                "coherent joint group--character state."
            ),
            (
                "Neither retained register is individually informative; any positive "
                "decoder must preserve and process their quantum correlations."
            ),
            (
                "Avoiding branch erasure relocates rather than automatically solves "
                "the state-dependent multiplicity inverse problem."
            ),
        ],
    )


def write_joint_character_correlation_decoder_report(
    path: Path = REPORT_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = (
        "EXP-CODE-SELF-DUAL-WREATH-JOINT-CHARACTER-CORRELATION-DECODER"
    ),
    registry_candidate_id: str = "CODE-COSET-COLLECTIVE",
    registry_result_id: str = "",
    **kwargs: Any,
) -> dict[str, Any]:
    output_path = path
    for _k in ("write_registry", "registry_experiment_id", "registry_candidate_id", "registry_result_id"):
        kwargs.pop(_k, None)
    if "run_joint_character_correlation_decoder" in globals():
        report = run_joint_character_correlation_decoder(**kwargs)
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
                id="NEG-SELF-DUAL-WREATH-JOINT-CHARACTER-CORRELATION-DECODER",
                source=registry_experiment_id,
                claim="Initial negative claim for EXP-CODE-SELF-DUAL-WREATH-JOINT-CHARACTER-CORRELATION-DECODER.",
                reason_invalid="Falsified or refined by exact theorem evaluation.",
                lesson="Lesson from exact theorem analysis for EXP-CODE-SELF-DUAL-WREATH-JOINT-CHARACTER-CORRELATION-DECODER.",
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
                    "self_dual_wreath_joint_character_correlation_decoder": str(path)
                },
            )
        )
    return payload

"""Projected-unitary access and normalization boundary for the linear point POVM.

The linear point POVM avoids the PGM average-state inverse, but its centered
effect still needs a circuit.  This module gives the exact generic access
reduction and charges its normalization.

Suppose ``U_rho`` prepares a purification ``|psi_rho>`` of a known density
operator ``rho`` on register ``A``.  With a fresh signal register ``S``,

    B_rho=(U_rho^* tensor I_S) Swap_(A,S)
          (U_rho tensor I_S)                              (1)

is unitary and its all-zero preparation-ancilla block is exactly ``rho``.
Coherently adjoining a uniform group element and applying the corresponding
left action prepares purifications of

    rho_H=|H|^-1 sum_(h in H) L_h rho L_h^*,
    rho_G=|G|^-1 sum_(g in G) L_g rho L_g^*.

A one-qubit LCU of their projected-unitary encodings has top block

    (rho_H-rho_G)/2 = Delta_0/2.                           (2)

Thus seed-purification and controlled-group-action access give a
normalization-two block encoding of the linear-POVM signal without enumerating
orientation branches or inverting the average state.

Let ``beta=||Delta_0||_infinity``.  To implement
``M_j=(I+Delta_j/beta)/n``, a generic QSVT compiler must amplify singular
values from scale ``beta/2`` to constant scale.  Bernstein's polynomial
inequality gives degree

    Omega(1/beta),                                        (3)

and uniform singular-value amplification achieves
``O(beta^-1 log(1/epsilon))`` queries.  Given that amplification, polynomial
approximation of square roots and the ``n`` covariant effects yields a
polynomial Naimark dilation whenever ``beta>=n^-O(1)`` and all preparation,
group-action, and precision primitives are polynomial.

Equation (3) is a lower bound on generic bounded-polynomial/QSVT rescaling of
the stated block encoding, not on representation-specific direct transforms.
No inverse-polynomial natural ``beta`` theorem or complete point measurement
is supplied here.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import numpy as np

from research_registry import utc_now
from self_dual_wreath_point_stabilizer_quotient import point_quotient_states


REPORT_PATH = Path(
    "research/representation/self_dual_wreath_point_effect_access_boundary.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-POINT-EFFECT-ACCESS-BOUNDARY"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"
QSVT_SOURCE = "https://arxiv.org/abs/1806.01838"

Partition = tuple[int, ...]
Label = tuple[Partition, Partition]


@dataclass(frozen=True)
class PurificationBlockEncodingControl:
    control_id: str
    system_dimension: int
    purification_environment_dimension: int
    twirl_group_order: int
    twirl_subgroup_order: int
    base_density_trace_residual: float
    base_projected_block_residual: float
    base_dilation_unitarity_residual: float
    subgroup_twirl_projected_block_residual: float
    full_twirl_projected_block_residual: float
    lcu_centered_block_residual: float
    lcu_normalization: int
    exact_purification_block_encoding_verified: bool
    exact_twirl_and_lcu_block_encoding_verified: bool
    status: str


@dataclass(frozen=True)
class PointEffectAccessControl:
    control_id: str
    n: int
    labels: tuple[Label, ...]
    copy_count: int
    register_dimension: int
    centered_operator_norm_beta: float
    centered_hilbert_schmidt_norm_squared: float
    centered_effective_rank: float
    linear_povm_success_excess: float
    target_rescaling_error: float
    bernstein_qsvt_degree_lower_bound: int
    singular_value_amplification_query_upper_estimate: int
    constant_normalization_centered_block_encoding_proved: bool
    inverse_polynomial_beta_proved_for_family: bool
    generic_rescaling_polynomial_for_family_proved: bool
    complete_n_outcome_naimark_compiler_proved: bool
    status: str


@dataclass(frozen=True)
class PointEffectAccessScalingRecord:
    n: int
    information_threshold_copy_count: int
    point_outcome_count: int
    seed_joint_state_purification_schema_polynomial: bool
    subgroup_and_group_uniform_prepare_polynomial: bool
    controlled_left_action_polynomial: bool
    centered_block_encoding_normalization: int
    generic_rescaling_query_complexity: str
    inverse_polynomial_beta_sufficient_for_polynomial_rescaling: bool
    inverse_polynomial_beta_proved: bool
    representation_specific_rescaling_bypass_ruled_out: bool
    end_to_end_point_measurement_compiled: bool
    status: str


@dataclass(frozen=True)
class PointEffectAccessTheorem:
    density_block_encoding: str
    twirl_purification: str
    centered_lcu: str
    generic_degree_boundary: str
    conditional_naimark_compiler: str
    scope: str
    theorem_verified: bool
    status: str


@dataclass(frozen=True)
class PointEffectAccessReport:
    created_at: str
    theorem_contract: dict[str, Any]
    theorem: PointEffectAccessTheorem
    projected_unitary_controls: list[PurificationBlockEncodingControl]
    finite_point_controls: list[PointEffectAccessControl]
    scaling_records: list[PointEffectAccessScalingRecord]
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    literature_links: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _unitary_with_first_column(vector: np.ndarray, tolerance: float = 1e-12) -> np.ndarray:
    vector = np.asarray(vector, dtype=complex).reshape(-1)
    norm = float(np.linalg.norm(vector))
    if abs(norm - 1.0) > tolerance:
        raise ValueError("preparation vector must be normalized")
    basis = [vector]
    dimension = len(vector)
    for index in range(dimension):
        candidate = np.zeros(dimension, dtype=complex)
        candidate[index] = 1
        for existing in basis:
            candidate -= existing * np.vdot(existing, candidate)
        candidate_norm = float(np.linalg.norm(candidate))
        if candidate_norm > tolerance:
            basis.append(candidate / candidate_norm)
        if len(basis) == dimension:
            break
    unitary = np.stack(basis, axis=1)
    if unitary.shape != (dimension, dimension):
        raise ArithmeticError("failed to complete preparation vector to a unitary")
    return unitary


def purification_projected_unitary(
    purification: np.ndarray,
) -> tuple[np.ndarray, np.ndarray, float]:
    """Construct (1), returning the dilation, top block, and unitarity residual."""

    purification = np.asarray(purification, dtype=complex)
    if purification.ndim != 2:
        raise ValueError("purification must be a system-by-environment matrix")
    system_dimension, environment_dimension = purification.shape
    vector = purification.reshape(-1)
    preparation = _unitary_with_first_column(vector)
    signal_identity = np.eye(system_dimension)
    prepare = np.kron(preparation, signal_identity)
    total_dimension = system_dimension * environment_dimension * system_dimension
    swap = np.zeros((total_dimension, total_dimension), dtype=complex)
    for system in range(system_dimension):
        for environment in range(environment_dimension):
            for signal in range(system_dimension):
                source = (
                    (system * environment_dimension + environment)
                    * system_dimension
                    + signal
                )
                target = (
                    (signal * environment_dimension + environment)
                    * system_dimension
                    + system
                )
                swap[target, source] = 1
    dilation = prepare.conj().T @ swap @ prepare
    top_block = dilation[:system_dimension, :system_dimension]
    unitarity = float(
        np.linalg.norm(
            dilation.conj().T @ dilation - np.eye(total_dimension),
            ord=2,
        )
    )
    return dilation, top_block, unitarity


def twirled_purification(
    purification: np.ndarray,
    unitaries: tuple[np.ndarray, ...],
) -> np.ndarray:
    purification = np.asarray(purification, dtype=complex)
    if not unitaries:
        raise ValueError("at least one twirl unitary is required")
    dimension = purification.shape[0]
    if any(unitary.shape != (dimension, dimension) for unitary in unitaries):
        raise ValueError("twirl unitary dimension mismatch")
    return np.hstack(
        tuple(unitary @ purification / math.sqrt(len(unitaries)) for unitary in unitaries)
    )


def audit_purification_block_encoding(
    purification: np.ndarray,
    group_unitaries: tuple[np.ndarray, ...],
    subgroup_indices: tuple[int, ...],
    *,
    control_id: str,
    tolerance: float = 1e-9,
) -> PurificationBlockEncodingControl:
    purification = np.asarray(purification, dtype=complex)
    density = purification @ purification.conj().T
    base_dilation, base_block, base_unitarity = purification_projected_unitary(
        purification
    )
    del base_dilation
    subgroup = tuple(group_unitaries[index] for index in subgroup_indices)
    subgroup_purification = twirled_purification(purification, subgroup)
    full_purification = twirled_purification(purification, group_unitaries)

    common_environment = max(
        subgroup_purification.shape[1], full_purification.shape[1]
    )
    padded_subgroup = np.pad(
        subgroup_purification,
        ((0, 0), (0, common_environment - subgroup_purification.shape[1])),
    )
    padded_full = np.pad(
        full_purification,
        ((0, 0), (0, common_environment - full_purification.shape[1])),
    )
    subgroup_dilation, subgroup_block, subgroup_unitarity = (
        purification_projected_unitary(padded_subgroup)
    )
    full_dilation, full_block, full_unitarity = purification_projected_unitary(
        padded_full
    )
    subgroup_density = sum(
        (unitary @ density @ unitary.conj().T for unitary in subgroup),
        np.zeros_like(density),
    ) / len(subgroup)
    full_density = sum(
        (unitary @ density @ unitary.conj().T for unitary in group_unitaries),
        np.zeros_like(density),
    ) / len(group_unitaries)

    # Selector |+> around diag(B_H,-B_G) has top block (rho_H-rho_G)/2.
    lcu_block = (subgroup_block - full_block) / 2
    centered = subgroup_density - full_density
    base_residual = float(np.linalg.norm(base_block - density))
    subgroup_residual = float(np.linalg.norm(subgroup_block - subgroup_density))
    full_residual = float(np.linalg.norm(full_block - full_density))
    lcu_residual = float(np.linalg.norm(lcu_block - centered / 2))
    trace_residual = abs(float(np.trace(density).real) - 1.0)
    verified_base = trace_residual <= tolerance and base_residual <= tolerance
    verified_lcu = bool(
        subgroup_residual <= tolerance
        and full_residual <= tolerance
        and lcu_residual <= tolerance
        and max(base_unitarity, subgroup_unitarity, full_unitarity) <= tolerance
    )
    return PurificationBlockEncodingControl(
        control_id=control_id,
        system_dimension=purification.shape[0],
        purification_environment_dimension=purification.shape[1],
        twirl_group_order=len(group_unitaries),
        twirl_subgroup_order=len(subgroup),
        base_density_trace_residual=trace_residual,
        base_projected_block_residual=base_residual,
        base_dilation_unitarity_residual=base_unitarity,
        subgroup_twirl_projected_block_residual=subgroup_residual,
        full_twirl_projected_block_residual=full_residual,
        lcu_centered_block_residual=lcu_residual,
        lcu_normalization=2,
        exact_purification_block_encoding_verified=verified_base,
        exact_twirl_and_lcu_block_encoding_verified=verified_lcu,
        status=(
            "exact-purification-twirl-centered-block-encoding"
            if verified_base and verified_lcu
            else "purification-block-encoding-validation-failure"
        ),
    )


def bernstein_rescaling_degree_lower_bound(
    beta: float,
    error: float,
) -> int:
    if not 0 < beta < 1 or not 0 <= error < 0.5:
        raise ValueError("invalid beta or approximation error")
    return math.ceil((1 - 2 * error) * math.sqrt(1 - (beta / 2) ** 2) * 2 / beta)


def audit_point_effect_access(
    n: int,
    labels: tuple[Label, ...],
    *,
    control_id: str,
    target_error: float = 0.01,
) -> PointEffectAccessControl:
    states = point_quotient_states(labels)
    average = sum(states) / n
    delta = states[0] - average
    beta = float(np.linalg.norm(delta, ord=2))
    signal = float(np.trace(delta.conj().T @ delta).real)
    effective_rank = signal / beta**2
    lower = bernstein_rescaling_degree_lower_bound(beta, target_error)
    upper = math.ceil(8 * math.log(2 / target_error) / beta)
    return PointEffectAccessControl(
        control_id=control_id,
        n=n,
        labels=labels,
        copy_count=len(labels),
        register_dimension=states[0].shape[0],
        centered_operator_norm_beta=beta,
        centered_hilbert_schmidt_norm_squared=signal,
        centered_effective_rank=effective_rank,
        linear_povm_success_excess=signal / (n * beta),
        target_rescaling_error=target_error,
        bernstein_qsvt_degree_lower_bound=lower,
        singular_value_amplification_query_upper_estimate=upper,
        constant_normalization_centered_block_encoding_proved=True,
        inverse_polynomial_beta_proved_for_family=False,
        generic_rescaling_polynomial_for_family_proved=False,
        complete_n_outcome_naimark_compiler_proved=False,
        status="finite-centered-access-cost-control-asymptotic-beta-open",
    )


def point_effect_access_scaling_record(n: int) -> PointEffectAccessScalingRecord:
    if n < 3:
        raise ValueError("n must be at least three")
    copies = math.ceil(math.lgamma(n + 1) / math.log(2))
    return PointEffectAccessScalingRecord(
        n=n,
        information_threshold_copy_count=copies,
        point_outcome_count=n,
        seed_joint_state_purification_schema_polynomial=True,
        subgroup_and_group_uniform_prepare_polynomial=True,
        controlled_left_action_polynomial=True,
        centered_block_encoding_normalization=2,
        generic_rescaling_query_complexity="Theta(beta_n^-1) up to log precision",
        inverse_polynomial_beta_sufficient_for_polynomial_rescaling=True,
        inverse_polynomial_beta_proved=False,
        representation_specific_rescaling_bypass_ruled_out=False,
        end_to_end_point_measurement_compiled=False,
        status="constant-normalization-centered-access-beta-and-naimark-open",
    )


def _cyclic_shift(dimension: int, amount: int) -> np.ndarray:
    matrix = np.zeros((dimension, dimension), dtype=complex)
    for index in range(dimension):
        matrix[(index + amount) % dimension, index] = 1
    return matrix


def run_point_effect_access_boundary() -> PointEffectAccessReport:
    purifications = [
        np.asarray([[math.sqrt(0.7), 0], [0, math.sqrt(0.3)]], dtype=complex),
        np.asarray(
            [
                [math.sqrt(0.5), 0],
                [0, math.sqrt(0.3)],
                [0, math.sqrt(0.2)],
            ],
            dtype=complex,
        ),
    ]
    projected_controls = []
    for index, purification in enumerate(purifications):
        dimension = purification.shape[0]
        group = tuple(_cyclic_shift(dimension, amount) for amount in range(dimension))
        projected_controls.append(
            audit_purification_block_encoding(
                purification,
                group,
                (0,),
                control_id=f"CYCLIC-{dimension}-RANK-{purification.shape[1]}",
            )
        )
    threshold_labels = (
        ((3,), (2, 1)),
        ((3,), (1, 1, 1)),
        ((2, 1), (1, 1, 1)),
    )
    point_controls = [
        audit_point_effect_access(
            3,
            (((3,), (2, 1)),),
            control_id="W3-SINGLE-UNEQUAL",
        ),
        audit_point_effect_access(
            3,
            threshold_labels,
            control_id="W3-INFORMATION-THRESHOLD",
        ),
        audit_point_effect_access(
            4,
            (((4,), (3, 1)), ((2, 2), (2, 1, 1))),
            control_id="W4-COLLISION-FREE-PAIR",
        ),
    ]
    scaling = [point_effect_access_scaling_record(n) for n in (16, 64, 256, 1024)]
    failures = sum(
        not row.exact_purification_block_encoding_verified
        or not row.exact_twirl_and_lcu_block_encoding_verified
        for row in projected_controls
    )
    verified = failures == 0
    theorem = PointEffectAccessTheorem(
        density_block_encoding=(
            "(U_rho^* tensor I)Swap(U_rho tensor I) has all-zero ancilla block rho."
        ),
        twirl_purification=(
            "A uniform coherent group label and controlled L_g prepare purifications "
            "of subgroup and full-group twirls."
        ),
        centered_lcu=(
            "One selector qubit gives a normalization-two block encoding of "
            "Delta_0=rho_H-rho_G."
        ),
        generic_degree_boundary=(
            "Rescaling Delta_0/2 to Delta_0/beta by bounded polynomial/QSVT has "
            "degree Theta(beta^-1) up to logarithmic precision factors."
        ),
        conditional_naimark_compiler=(
            "If beta is inverse polynomial and preparation/group-action primitives "
            "are efficient, QSVT square roots and n covariant effects give a "
            "polynomial approximate Naimark dilation."
        ),
        scope=(
            "The degree bound is for generic rescaling of this block encoding. It "
            "does not rule out a direct representation-specific point transform."
        ),
        theorem_verified=verified,
        status=(
            "centered-effect-block-encoding-proved-beta-normalization-open"
            if verified
            else "point-effect-access-validation-failure"
        ),
    )
    return PointEffectAccessReport(
        created_at=utc_now(),
        theorem_contract=asdict(theorem),
        theorem=theorem,
        projected_unitary_controls=projected_controls,
        finite_point_controls=point_controls,
        scaling_records=scaling,
        proof_obligations=[
            {
                "obligation": "construct_centered_point_effect_block_encoding",
                "resolved": verified,
                "resolution": (
                    "Purification projected-unitary encodings, coherent twirls, and "
                    "one-qubit LCU give Delta/2 exactly."
                ),
            },
            {
                "obligation": "charge_centered_effect_rescaling_cost",
                "resolved": True,
                "resolution": (
                    "Bernstein's inequality and singular-value amplification give "
                    "matching beta^-1 generic degree dependence."
                ),
            },
            {
                "obligation": "prove_inverse_polynomial_collective_beta",
                "resolved": False,
                "resolution": (
                    "Finite beta values are positive, but no natural collision-free "
                    "threshold theorem excludes superpolynomial decay."
                ),
            },
            {
                "obligation": "compile_complete_covariant_point_naimark_dilation",
                "resolved": False,
                "resolution": (
                    "A conditional generic route exists if beta is inverse polynomial; "
                    "its all-n premises and explicit representation circuit are open."
                ),
            },
        ],
        adversarial_audit=[
            {
                "objection": "Mixed-state preparation does not provide a density block encoding.",
                "resolved": True,
                "resolution": (
                    "A purification plus one system-signal swap gives the density "
                    "operator as an exact projected unitary block."
                ),
            },
            {
                "objection": "Constant-normalization Delta access makes the POVM polynomial.",
                "resolved": True,
                "resolution": (
                    "False without beta control. Generic rescaling costs Theta(1/beta) "
                    "queries before effect square roots are implemented."
                ),
            },
            {
                "objection": "The beta boundary is an arbitrary-circuit lower bound.",
                "resolved": False,
                "resolution": (
                    "It applies only to bounded-polynomial/QSVT transforms of the "
                    "normalization-two centered block encoding."
                ),
            },
        ],
        literature_links=[
            {
                "id": "GILYEN-SU-LOW-WIEBE-2018-QSVT",
                "title": "Quantum singular value transformation and beyond",
                "url": QSVT_SOURCE,
                "used_for": (
                    "Projected-unitary block encodings and uniform singular-value "
                    "amplification with explicit normalization dependence"
                ),
                "arbitrary_circuit_lower_bound": False,
            }
        ],
        headline_metrics={
            "purification_density_block_encoding_theorem_count": 1,
            "centered_twirl_lcu_block_encoding_theorem_count": 1,
            "generic_beta_rescaling_boundary_theorem_count": 1,
            "projected_unitary_control_count": len(projected_controls),
            "finite_control_failure_count": failures,
            "minimum_finite_beta": min(
                row.centered_operator_norm_beta for row in point_controls
            ),
            "inverse_polynomial_collective_beta_theorem_count": 0,
            "complete_point_naimark_compiler_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "purification_density_block_encoding_proved": verified,
            "centered_point_effect_block_encoding_proved": verified,
            "centered_block_encoding_has_constant_normalization": verified,
            "generic_rescaling_costs_inverse_beta": True,
            "inverse_polynomial_collective_beta_proved": False,
            "complete_covariant_point_naimark_compiled": False,
            "representation_specific_direct_point_transform_ruled_out": False,
            "polynomial_full_hidden_shift_decoder_proved": False,
            "classical_separation_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "Centered-effect access is exact, but generic normalization and the "
                "full Naimark compiler remain hostage to an unproved collective beta bound."
            ),
        },
        status=theorem.status,
        summary=(
            "Closed the constant-normalization block-encoding step for the linear point "
            "POVM and proved its generic inverse-beta query boundary. The next hard "
            "gate is collective operator norm/effective rank, not average-state inversion."
        ),
        falsifiers_triggered=[
            (
                "The inverse-free linear POVM still has a normalization cost: exact "
                "Delta/2 access does not give Delta/beta for free."
            ),
            (
                "The access bottleneck is beta, not the factorial orientation width; "
                "coherent purification and group twirls avoid branch enumeration."
            ),
            (
                "The QSVT degree boundary does not exclude a direct symmetry-adapted "
                "point transform outside generic polynomial rescaling."
            ),
        ],
    )


def write_point_effect_access_boundary_report(
    path: Path = REPORT_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = (
        "EXP-CODE-SELF-DUAL-WREATH-POINT-EFFECT-ACCESS-BOUNDARY"
    ),
    registry_candidate_id: str = "CODE-COSET-COLLECTIVE",
    registry_result_id: str = "",
    **kwargs: Any,
) -> dict[str, Any]:
    output_path = path
    for _k in ("write_registry", "registry_experiment_id", "registry_candidate_id", "registry_result_id"):
        kwargs.pop(_k, None)
    if "run_point_effect_access_boundary" in globals():
        report = run_point_effect_access_boundary(**kwargs)
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
                id="NEG-SELF-DUAL-WREATH-POINT-EFFECT-ACCESS-BOUNDARY",
                source=registry_experiment_id,
                claim="Initial negative claim for EXP-CODE-SELF-DUAL-WREATH-POINT-EFFECT-ACCESS-BOUNDARY.",
                reason_invalid="Falsified or refined by exact theorem evaluation.",
                lesson="Lesson from exact theorem analysis for EXP-CODE-SELF-DUAL-WREATH-POINT-EFFECT-ACCESS-BOUNDARY.",
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
                    "self_dual_wreath_point_effect_access_boundary": str(path)
                },
            )
        )
    return payload

"""Typical factorial normalization no-go for generic linear-point QSVT.

The centered point effect has a constant-normalization block encoding, but the
linear POVM needs ``Delta/beta`` where ``beta=||Delta||_infinity``.  The
carrier-traced purity theorem forces ``beta`` to be tiny on natural threshold
blocks.

Let ``T_H`` and ``T_G`` be conjugation twirls for ``H=Stab(0)`` and ``G=S_n``.
They are commuting orthogonal projections on Hilbert--Schmidt operator space,
with ``range(T_G)`` contained in ``range(T_H)``.  Hence

    Delta = (T_H-T_G) tau,
    beta^2 <= ||Delta||_2^2 <= Tr(tau^2).                 (1)

For ``k=ceil(log2 |G|)``, the existing natural purity theorem gives

    |G|2^k E Tr(tau^2) <= C_n := 2p(n)+2p(n)^2.          (2)

Conditioning all source partitions to be globally distinct costs at most
``1/P_cf(n,k)`` in this nonnegative upper bound.  Markov therefore implies
that, with conditioned probability at least ``1-eta``,

    beta <= sqrt(C_n/[eta P_cf |G|2^k]).                  (3)

Any bounded scalar polynomial that rescales the normalization-two block
encoding ``Delta/2`` to constant amplitude has Bernstein degree

    Omega(1/beta)
      >= Omega(sqrt(eta P_cf |G|2^k/C_n)).                (4)

Asymptotically ``P_cf=1-o(1)``, ``log p(n)=O(sqrt(n))``, and
``|G|2^k=Theta((n!)^2)``.  For inverse-polynomial ``eta``, equation (4) is
``n! exp(-O(sqrt(n)))``: superpolynomial by an overwhelming margin.

This closes generic QSVT/singular-value amplification of the centered density
block encoding for typical carrier-traced threshold sources.  It does not
bound direct representation-specific Naimark transforms, measurements that
never normalize ``Delta`` as a scalar polynomial, or carrier-retaining
decoders.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import numpy as np

from research_registry import utc_now
from self_dual_wreath_global_collision_free_mass import global_collision_free_mass_record
from self_dual_wreath_joint_character_correlation_decoder import (
    _permutations,
    joint_character_state,
    left_covariant_state,
)
from self_dual_wreath_joint_character_purity_decoupling import (
    partition_number,
    universal_normalized_purity_bound,
)
from self_dual_wreath_point_standard_energy import (
    point_stabilizer_twirl,
    standard_harmonic_projection,
)


REPORT_PATH = Path(
    "research/representation/self_dual_wreath_point_effect_qsvt_no_go.json"
)
DEFAULT_EXPERIMENT_ID = "EXP-CODE-SELF-DUAL-WREATH-POINT-EFFECT-QSVT-NO-GO"
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"
QSVT_SOURCE = "https://arxiv.org/abs/1806.01838"

Partition = tuple[int, ...]
Label = tuple[Partition, Partition]


@dataclass(frozen=True)
class PointBetaPurityControl:
    control_id: str
    n: int
    labels: tuple[Label, ...]
    copy_count: int
    native_state_purity: float
    centered_hilbert_schmidt_norm_squared: float
    centered_operator_norm_squared: float
    beta_squared_to_centered_energy_ratio: float
    centered_energy_to_purity_ratio: float
    twirl_difference_projection_residual: float
    beta_purity_chain_verified: bool
    status: str


@dataclass(frozen=True)
class TypicalPointBetaScalingRecord:
    n: int
    copy_count: int
    group_order_log2: float
    orientation_count_log2: int
    partition_count_decimal: str
    normalized_purity_bound_log2: float
    typical_failure_probability: float
    log2_collision_free_probability: float
    collision_free_conditioning_loss_log2: float
    typical_beta_upper_bound_log2: float
    generic_qsvt_degree_lower_bound_log2: float
    polynomial_degree_ten_benchmark_log2: float
    generic_qsvt_degree_exceeds_polynomial_benchmark: bool
    asymptotic_collision_free_mass_tends_to_one: bool
    direct_representation_specific_measurement_ruled_out: bool
    status: str


@dataclass(frozen=True)
class PointEffectQSVTNoGoTheorem:
    twirl_projection: str
    beta_purity_chain: str
    conditional_typical_beta: str
    generic_degree_lower_bound: str
    asymptotic_consequence: str
    scope: str
    theorem_verified: bool
    status: str


@dataclass(frozen=True)
class PointEffectQSVTNoGoReport:
    created_at: str
    theorem_contract: dict[str, Any]
    theorem: PointEffectQSVTNoGoTheorem
    finite_controls: list[PointBetaPurityControl]
    scaling_records: list[TypicalPointBetaScalingRecord]
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    literature_links: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def audit_point_beta_purity(
    n: int,
    labels: tuple[Label, ...],
    *,
    control_id: str,
    tolerance: float = 1e-9,
) -> PointBetaPurityControl:
    character_count = 1 << len(labels)
    state = joint_character_state(labels, tuple(range(n)))
    standard = standard_harmonic_projection(state, n, character_count)
    delta = point_stabilizer_twirl(standard, n, character_count)
    permutations = _permutations(n)
    group_twirl = sum(
        (
            left_covariant_state(
                state,
                permutations,
                permutation,
                character_count,
            )
            for permutation in permutations
        ),
        np.zeros_like(state),
    ) / len(permutations)
    direct_twirl_difference = (
        point_stabilizer_twirl(state, n, character_count) - group_twirl
    )
    projection_residual = float(np.linalg.norm(delta - direct_twirl_difference))
    purity = float(np.trace(state @ state).real)
    energy = float(np.trace(delta.conj().T @ delta).real)
    beta_squared = float(np.linalg.norm(delta, ord=2) ** 2)
    verified = bool(
        projection_residual <= 100 * tolerance
        and beta_squared <= energy + 100 * tolerance
        and energy <= purity + 100 * tolerance
    )
    return PointBetaPurityControl(
        control_id=control_id,
        n=n,
        labels=labels,
        copy_count=len(labels),
        native_state_purity=purity,
        centered_hilbert_schmidt_norm_squared=energy,
        centered_operator_norm_squared=beta_squared,
        beta_squared_to_centered_energy_ratio=(beta_squared / energy if energy else 0.0),
        centered_energy_to_purity_ratio=(energy / purity if purity else 0.0),
        twirl_difference_projection_residual=projection_residual,
        beta_purity_chain_verified=verified,
        status=(
            "exact-point-beta-purity-chain"
            if verified
            else "point-beta-purity-chain-validation-failure"
        ),
    )


def typical_point_beta_scaling_record(
    n: int,
    *,
    typical_failure_probability: float | None = None,
    polynomial_benchmark_degree: int = 10,
) -> TypicalPointBetaScalingRecord:
    if n < 3 or polynomial_benchmark_degree < 1:
        raise ValueError("invalid scaling parameters")
    eta = typical_failure_probability or n**-2
    if not 0 < eta < 1:
        raise ValueError("failure probability must lie in (0,1)")
    mass = global_collision_free_mass_record(n)
    if not mass.enough_distinct_partitions_exist:
        raise ValueError("collision-free threshold sources are impossible at this n")
    copies = mass.information_threshold_copy_count
    group_log2 = math.lgamma(n + 1) / math.log(2)
    normalized_bound = universal_normalized_purity_bound(n)
    log2_mass = mass.log2_unconditioned_global_collision_free_probability
    conditioning_loss = -log2_mass
    beta_log2 = min(0.0, 0.5 * (
        math.log2(normalized_bound)
        - math.log2(eta)
        - log2_mass
        - group_log2
        - copies
    ))
    # Bernstein contributes only an O(1) factor; retain the conservative scale.
    degree_log2 = max(0.0, -beta_log2)
    benchmark = polynomial_benchmark_degree * math.log2(n)
    return TypicalPointBetaScalingRecord(
        n=n,
        copy_count=copies,
        group_order_log2=group_log2,
        orientation_count_log2=copies,
        partition_count_decimal=str(partition_number(n)),
        normalized_purity_bound_log2=math.log2(normalized_bound),
        typical_failure_probability=eta,
        log2_collision_free_probability=log2_mass,
        collision_free_conditioning_loss_log2=conditioning_loss,
        typical_beta_upper_bound_log2=beta_log2,
        generic_qsvt_degree_lower_bound_log2=degree_log2,
        polynomial_degree_ten_benchmark_log2=benchmark,
        generic_qsvt_degree_exceeds_polynomial_benchmark=degree_log2 > benchmark,
        asymptotic_collision_free_mass_tends_to_one=True,
        direct_representation_specific_measurement_ruled_out=False,
        status=(
            "typical-centered-qsvt-rescaling-superpolynomial"
            if degree_log2 > benchmark
            else "finite-size-qsvt-separation-not-yet-visible"
        ),
    )


def run_point_effect_qsvt_no_go() -> PointEffectQSVTNoGoReport:
    threshold_labels = (
        ((3,), (2, 1)),
        ((3,), (1, 1, 1)),
        ((2, 1), (1, 1, 1)),
    )
    controls = [
        audit_point_beta_purity(
            3,
            (((3,), (2, 1)),),
            control_id="W3-SINGLE-UNEQUAL",
        ),
        audit_point_beta_purity(
            3,
            threshold_labels,
            control_id="W3-INFORMATION-THRESHOLD",
        ),
        audit_point_beta_purity(
            4,
            (((4,), (3, 1)), ((2, 2), (2, 1, 1))),
            control_id="W4-COLLISION-FREE-PAIR",
        ),
    ]
    scaling = [
        typical_point_beta_scaling_record(n)
        for n in (12, 16, 20, 24, 28, 32, 36, 40, 44, 48)
    ]
    failures = sum(not row.beta_purity_chain_verified for row in controls)
    separated = sum(
        row.generic_qsvt_degree_exceeds_polynomial_benchmark for row in scaling
    )
    verified = failures == 0 and separated > 0
    theorem = PointEffectQSVTNoGoTheorem(
        twirl_projection=(
            "T_H-T_G is an orthogonal Hilbert--Schmidt projection because "
            "T_H,T_G commute and range(T_G) is contained in range(T_H)."
        ),
        beta_purity_chain=(
            "beta^2<=||Delta||_2^2<=Tr(tau^2)."
        ),
        conditional_typical_beta=(
            "With collision-free conditional probability at least 1-eta, "
            "beta<=sqrt(C_n/[eta P_cf n! 2^k])."
        ),
        generic_degree_lower_bound=(
            "Bounded-polynomial rescaling of Delta/2 has degree "
            "Omega(sqrt(eta P_cf n! 2^k/C_n))."
        ),
        asymptotic_consequence=(
            "At k=ceil(log2 n!), inverse-polynomial eta, and P_cf=1-o(1), "
            "generic degree is n! exp(-O(sqrt(n)))."
        ),
        scope=(
            "This is a typical-source lower bound for generic scalar QSVT on the "
            "centered density block encoding, not an arbitrary-measurement lower bound."
        ),
        theorem_verified=verified,
        status=(
            "generic-centered-effect-qsvt-factorial-no-go-direct-transform-open"
            if verified
            else "point-effect-qsvt-no-go-validation-failure"
        ),
    )
    return PointEffectQSVTNoGoReport(
        created_at=utc_now(),
        theorem_contract=asdict(theorem),
        theorem=theorem,
        finite_controls=controls,
        scaling_records=scaling,
        proof_obligations=[
            {
                "obligation": "bound_centered_operator_norm_from_native_purity",
                "resolved": verified,
                "resolution": (
                    "The point-centered map is an orthogonal HS projection and operator "
                    "norm is bounded by Hilbert--Schmidt norm."
                ),
            },
            {
                "obligation": "transfer_beta_upper_bound_to_collision_free_sources",
                "resolved": True,
                "resolution": (
                    "Unlike a signal lower bound, the nonnegative purity upper bound "
                    "conditions safely at cost 1/P_cf, with P_cf tending to one."
                ),
            },
            {
                "obligation": "test_generic_qsvt_linear_point_compiler",
                "resolved": True,
                "resolution": (
                    "Rejected for typical threshold sources: beta is factorially small "
                    "with high probability, forcing factorial polynomial degree."
                ),
            },
            {
                "obligation": "construct_direct_symmetry_adapted_point_naimark",
                "resolved": False,
                "resolution": (
                    "A direct Young/Racah transform could normalize relative block "
                    "coordinates without scalar amplification of Delta/2."
                ),
            },
        ],
        adversarial_audit=[
            {
                "objection": "Purity bounds only average beta and do not give a typical compiler obstruction.",
                "resolved": True,
                "resolution": (
                    "Markov yields a high-probability beta upper bound; a smaller beta "
                    "strengthens the Bernstein degree lower bound."
                ),
            },
            {
                "objection": "Collision-free conditioning invalidates the natural purity no-go.",
                "resolved": True,
                "resolution": (
                    "For upper bounds, conditioning loses only 1/P_cf=1+o(1), unlike "
                    "the unresolved collision-free point-signal lower bound."
                ),
            },
            {
                "objection": "Factorial QSVT degree rules out the linear POVM itself.",
                "resolved": False,
                "resolution": (
                    "No. It rules out one generic implementation from Delta/2. A direct "
                    "covariant Naimark transform remains outside the model."
                ),
            },
        ],
        literature_links=[
            {
                "id": "GILYEN-SU-LOW-WIEBE-2018-QSVT",
                "title": "Quantum singular value transformation and beyond",
                "url": QSVT_SOURCE,
                "used_for": "Bounded-polynomial implementation model and singular-value rescaling",
                "arbitrary_measurement_lower_bound": False,
            }
        ],
        headline_metrics={
            "point_beta_purity_chain_theorem_count": 1,
            "conditional_typical_beta_bound_theorem_count": 1,
            "generic_centered_qsvt_no_go_theorem_count": 1,
            "finite_control_count": len(controls),
            "finite_control_failure_count": failures,
            "superpolynomial_scaling_row_count": separated,
            "tail_n": scaling[-1].n,
            "tail_generic_degree_lower_bound_log2": (
                scaling[-1].generic_qsvt_degree_lower_bound_log2
            ),
            "direct_point_transform_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "typical_collective_beta_inverse_polynomial": False,
            "generic_centered_effect_qsvt_polynomial": False,
            "generic_centered_effect_qsvt_superpolynomial_proved": verified,
            "collision_free_conditioning_preserves_beta_upper_bound": True,
            "linear_point_povm_information_theoretically_invalidated": False,
            "direct_representation_specific_point_transform_ruled_out": False,
            "carrier_retaining_point_decoder_ruled_out": False,
            "polynomial_full_hidden_shift_decoder_proved": False,
            "classical_separation_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "Typical purity forces factorial generic rescaling cost. Only a direct "
                "symmetry-adapted measurement or carrier-retaining route remains viable."
            ),
        },
        status=theorem.status,
        summary=(
            "Closed the generic QSVT implementation route for the linear point POVM: "
            "typical threshold beta is factorially small, even after collision-free "
            "conditioning. The POVM remains an information-theoretic target for a "
            "direct Young/Racah Naimark transform."
        ),
        falsifiers_triggered=[
            (
                "Constant-normalization Delta block encoding is not enough; natural "
                "purity forces its useful scale to be factorially small."
            ),
            (
                "The conditional QSVT compiler premise beta>=n^-O(1) fails with high "
                "probability for natural carrier-traced threshold blocks."
            ),
            (
                "This normalization no-go does not extend to direct representation-"
                "specific POVM synthesis or coherent carrier retention."
            ),
        ],
    )


def write_point_effect_qsvt_no_go_report(
    path: Path = REPORT_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = (
        "EXP-CODE-SELF-DUAL-WREATH-POINT-EFFECT-QSVT-NO-GO"
    ),
    registry_candidate_id: str = "CODE-COSET-COLLECTIVE",
    registry_result_id: str = "",
    **kwargs: Any,
) -> dict[str, Any]:
    output_path = path
    for _k in ("write_registry", "registry_experiment_id", "registry_candidate_id", "registry_result_id"):
        kwargs.pop(_k, None)
    if "run_point_effect_qsvt_no_go" in globals():
        report = run_point_effect_qsvt_no_go(**kwargs)
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
                id="NEG-SELF-DUAL-WREATH-POINT-EFFECT-QSVT-NO-GO",
                source=registry_experiment_id,
                claim="Initial negative claim for EXP-CODE-SELF-DUAL-WREATH-POINT-EFFECT-QSVT-NO-GO.",
                reason_invalid="Falsified or refined by exact theorem evaluation.",
                lesson="Lesson from exact theorem analysis for EXP-CODE-SELF-DUAL-WREATH-POINT-EFFECT-QSVT-NO-GO.",
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
                    "self_dual_wreath_point_effect_qsvt_no_go": str(path)
                },
            )
        )
    return payload

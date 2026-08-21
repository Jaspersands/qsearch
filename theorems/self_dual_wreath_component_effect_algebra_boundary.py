"""Operator-algebra boundary for natural component POVMs.

The component nonscalarity defect

    D_ns = sum_e (H_e-h_e I)^2,       h_e=Tr(H_e)/r       (1)

detects failure of one global scalar distribution.  It does *not* detect the
genuinely nonabelian structure that makes a matrix POVM difficult.  A
coordinate projective measurement has full-rank ``D_ns`` but all effects
commute and can be implemented after a simultaneous eigenbasis transform.

The exact nonabelian diagnostic is the commutator defect

    D_com = sum_(e<f) [H_e,H_f]^* [H_e,H_f].              (2)

Because (2) is a sum of positive operators,

    D_com=0  iff  [H_e,H_f]=0 for every e,f
             iff  C^*(H_e) is a commutative finite-dimensional algebra. (3)

The regular-master functional calculus preserves source-block direct sums, so
central support of ``D_com`` is exactly the event that a source block has a
noncommutative component-effect algebra.  Its common-span cutdown is the
physical noncommutative-support mass.

The natural final-root results now prove constant source/physical mass and
asymptotically full rank for ``D_ns``.  Equations (1)-(3) show why that is not
yet a quantum-mechanism theorem: no deterministic rank, trace, or component-
aspect implication from ``D_ns`` to ``D_com`` exists.  The orthogonal PVM
control is an exact counterexample.

The next natural theorem must therefore prove positive central/physical support
of ``D_com`` (or another nonabelian algebra invariant) on the final-root event,
or prove that the natural effects are asymptotically commuting and exploit the
resulting classical conditional structure.  Finite S6 noncommutativity remains
only finite, low-source-mass evidence.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import numpy as np

from research_registry import utc_now


REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_component_effect_algebra_boundary.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-COMPONENT-EFFECT-ALGEBRA-BOUNDARY"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


@dataclass(frozen=True)
class ComponentEffectAlgebraControl:
    control_id: str
    fiber_dimension: int
    outcome_count: int
    nonscalarity_defect_rank: int
    nonscalarity_defect_minimum_positive_eigenvalue: float
    commutator_defect_rank: int
    commutator_defect_minimum_positive_eigenvalue: float
    maximum_effect_commutator_norm: float
    generated_unital_star_algebra_dimension: int
    full_matrix_algebra_dimension: int
    generated_algebra_commutative: bool
    effects_globally_scalar: bool
    effects_pairwise_commute: bool
    nonscalarity_defect_full_rank: bool
    noncommutative_effect_algebra: bool
    effect_sum_identity_residual: float
    exact_commutator_criterion_verified: bool
    status: str


@dataclass(frozen=True)
class ComponentEffectAlgebraBoundaryReport:
    created_at: str
    theorem_contract: dict[str, Any]
    finite_controls: list[ComponentEffectAlgebraControl]
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _orthonormal_algebra_basis(
    generators: tuple[np.ndarray, ...],
    tolerance: float,
) -> tuple[np.ndarray, ...]:
    """Close a small matrix family under products using HS Gram--Schmidt."""

    dimension = generators[0].shape[0]
    basis_vectors: list[np.ndarray] = []
    basis_matrices: list[np.ndarray] = []

    def add(matrix: np.ndarray) -> bool:
        vector = matrix.reshape(-1).astype(complex)
        for existing in basis_vectors:
            vector -= np.vdot(existing, vector) * existing
        norm = float(np.linalg.norm(vector))
        if norm <= 100 * tolerance:
            return False
        vector /= norm
        basis_vectors.append(vector)
        basis_matrices.append(vector.reshape(dimension, dimension))
        return True

    add(np.eye(dimension, dtype=complex))
    for generator in generators:
        add(generator)
        add(generator.conj().T)
    changed = True
    while changed and len(basis_matrices) < dimension * dimension:
        changed = False
        snapshot = tuple(basis_matrices)
        for left in snapshot:
            for right in snapshot:
                if add(left @ right):
                    changed = True
                    if len(basis_matrices) == dimension * dimension:
                        break
            if len(basis_matrices) == dimension * dimension:
                break
    return tuple(basis_matrices)


def audit_component_effect_algebra(
    control_id: str,
    effects: tuple[np.ndarray, ...],
    *,
    tolerance: float = 1e-9,
) -> ComponentEffectAlgebraControl:
    if not effects:
        raise ValueError("at least one component effect is required")
    dimension = effects[0].shape[0]
    if dimension < 1 or any(effect.shape != (dimension, dimension) for effect in effects):
        raise ValueError("effects must share one positive square fiber")
    identity = np.eye(dimension, dtype=complex)
    hermitian_effects = []
    nonscalarity = np.zeros_like(identity)
    globally_scalar = True
    for effect in effects:
        hermitian = (effect + effect.conj().T) / 2.0
        values = np.linalg.eigvalsh(hermitian)
        if values[0] < -100 * tolerance or values[-1] > 1 + 100 * tolerance:
            raise ValueError("component is not a valid effect")
        scalar = float(np.trace(hermitian).real / dimension)
        centered = hermitian - scalar * identity
        nonscalarity += centered @ centered
        globally_scalar = bool(
            globally_scalar
            and np.linalg.norm(centered, ord=2) <= 1000 * tolerance
        )
        hermitian_effects.append(hermitian)
    sum_residual = float(
        np.linalg.norm(
            sum(hermitian_effects, np.zeros_like(identity)) - identity,
            ord=2,
        )
    )
    if sum_residual > 1000 * tolerance:
        raise ValueError("effects do not form a POVM")

    commutator_defect = np.zeros_like(identity)
    maximum_commutator = 0.0
    for index, left in enumerate(hermitian_effects):
        for right in hermitian_effects[index + 1 :]:
            commutator = left @ right - right @ left
            maximum_commutator = max(
                maximum_commutator,
                float(np.linalg.norm(commutator, ord=2)),
            )
            commutator_defect += commutator.conj().T @ commutator

    nonscalar_values = np.linalg.eigvalsh(
        (nonscalarity + nonscalarity.conj().T) / 2.0
    )
    commutator_values = np.linalg.eigvalsh(
        (commutator_defect + commutator_defect.conj().T) / 2.0
    )
    nonscalar_positive = nonscalar_values[nonscalar_values > 1000 * tolerance]
    commutator_positive = commutator_values[
        commutator_values > 1000 * tolerance
    ]
    commute = bool(maximum_commutator <= 1000 * tolerance)
    algebra = _orthonormal_algebra_basis(tuple(hermitian_effects), tolerance)
    algebra_commutes = bool(all(
        np.linalg.norm(left @ right - right @ left, ord=2) <= 1000 * tolerance
        for index, left in enumerate(algebra)
        for right in algebra[index + 1 :]
    ))
    criterion = bool(
        commute == (len(commutator_positive) == 0)
        and commute == algebra_commutes
    )
    return ComponentEffectAlgebraControl(
        control_id=control_id,
        fiber_dimension=dimension,
        outcome_count=len(effects),
        nonscalarity_defect_rank=len(nonscalar_positive),
        nonscalarity_defect_minimum_positive_eigenvalue=(
            float(nonscalar_positive[0]) if len(nonscalar_positive) else 0.0
        ),
        commutator_defect_rank=len(commutator_positive),
        commutator_defect_minimum_positive_eigenvalue=(
            float(commutator_positive[0]) if len(commutator_positive) else 0.0
        ),
        maximum_effect_commutator_norm=maximum_commutator,
        generated_unital_star_algebra_dimension=len(algebra),
        full_matrix_algebra_dimension=dimension * dimension,
        generated_algebra_commutative=algebra_commutes,
        effects_globally_scalar=globally_scalar,
        effects_pairwise_commute=commute,
        nonscalarity_defect_full_rank=len(nonscalar_positive) == dimension,
        noncommutative_effect_algebra=not commute,
        effect_sum_identity_residual=sum_residual,
        exact_commutator_criterion_verified=criterion,
        status=(
            "noncommutative-component-effect-algebra-verified"
            if criterion and not commute
            else "commutative-nonscalar-component-algebra-verified"
            if criterion and not globally_scalar
            else "globally-scalar-component-algebra-verified"
            if criterion
            else "component-effect-algebra-control-failure"
        ),
    )


def _orthogonal_projective_povm(outcomes: int) -> tuple[np.ndarray, ...]:
    effects = []
    for outcome in range(outcomes):
        effect = np.zeros((outcomes, outcomes), dtype=complex)
        effect[outcome, outcome] = 1.0
        effects.append(effect)
    return tuple(effects)


def _trine_povm() -> tuple[np.ndarray, ...]:
    effects = []
    for index in range(3):
        angle = 2 * np.pi * index / 3
        vector = np.asarray([[np.cos(angle)], [np.sin(angle)]], dtype=complex)
        effects.append((2 / 3) * vector @ vector.conj().T)
    return tuple(effects)


def _scalar_povm() -> tuple[np.ndarray, ...]:
    identity = np.eye(3, dtype=complex)
    return 0.2 * identity, 0.3 * identity, 0.5 * identity


def _direct_sum(left: np.ndarray, right: np.ndarray) -> np.ndarray:
    output = np.zeros(
        (left.shape[0] + right.shape[0], left.shape[1] + right.shape[1]),
        dtype=complex,
    )
    output[: left.shape[0], : left.shape[1]] = left
    output[left.shape[0] :, left.shape[1] :] = right
    return output


def _mixed_commutative_noncommutative_povm() -> tuple[np.ndarray, ...]:
    left = _trine_povm()
    right = (
        np.diag([1.0, 0.0]).astype(complex),
        np.diag([0.0, 1.0]).astype(complex),
        np.zeros((2, 2), dtype=complex),
    )
    return tuple(_direct_sum(a, b) for a, b in zip(left, right))


def run_component_effect_algebra_boundary() -> ComponentEffectAlgebraBoundaryReport:
    controls = [
        audit_component_effect_algebra(
            "GLOBAL-SCALAR-THREE-OUTCOME",
            _scalar_povm(),
        ),
        audit_component_effect_algebra(
            "ORTHOGONAL-PVM-FULL-NONSCALAR-DEFECT",
            _orthogonal_projective_povm(4),
        ),
        audit_component_effect_algebra(
            "TRINE-NONCOMMUTATIVE-QUBIT",
            _trine_povm(),
        ),
        audit_component_effect_algebra(
            "DIRECT-SUM-NONCOMMUTATIVE-AND-COMMUTATIVE-SECTORS",
            _mixed_commutative_noncommutative_povm(),
        ),
    ]
    failures = sum(not row.exact_commutator_criterion_verified for row in controls)
    pvm = controls[1]
    trine = controls[2]
    separation = bool(
        pvm.nonscalarity_defect_full_rank
        and pvm.effects_pairwise_commute
        and trine.noncommutative_effect_algebra
    )
    exact = failures == 0 and separation
    return ComponentEffectAlgebraBoundaryReport(
        created_at=utc_now(),
        theorem_contract={
            "nonscalarity_boundary": (
                "D_ns=0 iff every effect equals its global normalized trace "
                "times identity; D_ns can be full rank for a commuting PVM."
            ),
            "commutator_criterion": (
                "D_com=sum_[e<f][H_e,H_f]^*[H_e,H_f] vanishes iff all effects "
                "commute iff their generated finite-dimensional C*-algebra is commutative."
            ),
            "regular_master_lift": (
                "Products, adjoints, sums, and spectral supports preserve the "
                "regular-master source-block direct sum, so central support of "
                "D_com is the noncommutative source-block event."
            ),
            "scope": (
                "Natural positive mass is proved for D_ns only. No natural "
                "central or physical mass theorem for D_com is known."
            ),
        },
        finite_controls=controls,
        proof_obligations=[
            {
                "obligation": "distinguish_nonscalar_component_support_from_noncommutative_effect_algebra",
                "resolved": exact,
                "resolution": "The orthogonal PVM has full-rank D_ns and zero D_com, while the trine POVM generates M_2 and has nonzero D_com."
            },
            {
                "obligation": "prove_natural_noncommutative_component_algebra_source_mass",
                "resolved": False,
                "resolution": "Evaluate central support of D_com under the globally distinct final-root source law, or prove an asymptotic commuting approximation with a coherent joint eigenbasis."
            },
            {
                "obligation": "prove_natural_physical_noncommutative_support_mass",
                "resolved": False,
                "resolution": "A source-block event alone is insufficient; control the common-span cutdown/support rank or state weight of D_com."
            },
            {
                "obligation": "compile_commuting_or_noncommuting_component_branch",
                "resolved": False,
                "resolution": "The commuting case still needs a coherent simultaneous eigenbasis and conditional probability preparation; the noncommuting case needs matrix square-root/support access."
            },
        ],
        adversarial_audit=[
            {
                "objection": "Asymptotically full nonscalarity-defect rank proves genuinely quantum component structure.",
                "resolved": True,
                "resolution": "False. An orthogonal coordinate PVM has full-rank D_ns but a commutative diagonal effect algebra."
            },
            {
                "objection": "Nonzero pairwise commutator is merely a basis artifact.",
                "resolved": True,
                "resolution": "False. Pairwise commutation is invariant under unitary conjugation and exactly characterizes a commutative generated C*-algebra."
            },
            {
                "objection": "Finite S6 noncommutativity proves positive natural noncommutative mass.",
                "resolved": False,
                "resolution": "The known S6 mechanism uses asymptotically negligible low-dimensional anchors. High-dimensional globally distinct source mass remains unproved."
            },
            {
                "objection": "Commuting natural effects would kill the algorithmic route.",
                "resolved": False,
                "resolution": "Not necessarily. A coherently accessible simultaneous eigenbasis could make the component dilation easier, but that transform and conditional distributions must be compiled."
            },
        ],
        headline_metrics={
            "exact_component_commutator_criterion_theorem_count": int(exact),
            "finite_control_count": len(controls),
            "finite_control_failure_count": failures,
            "full_rank_nonscalarity_commuting_counterexample_count": int(
                pvm.nonscalarity_defect_full_rank and pvm.effects_pairwise_commute
            ),
            "noncommutative_full_matrix_algebra_control_count": int(
                trine.generated_unital_star_algebra_dimension
                == trine.full_matrix_algebra_dimension
            ),
            "natural_nonscalarity_positive_mass_theorem_input_count": 1,
            "natural_noncommutative_effect_algebra_source_mass_theorem_count": 0,
            "natural_physical_noncommutative_support_mass_theorem_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "nonscalarity_defect_support_implies_noncommutative_effect_algebra": False,
            "commutator_defect_exactly_detects_global_effect_commutativity": exact,
            "natural_component_nonscalarity_source_and_physical_mass_proved": True,
            "natural_noncommutative_component_algebra_source_mass_proved": False,
            "natural_physical_noncommutative_component_support_mass_proved": False,
            "coherent_commuting_component_diagonalization_compiled": False,
            "coherent_noncommutative_component_dilation_compiled": False,
            "physical_pgm_outside_mrs_transcript_postprocessing_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "Natural nonscalarity mass is now rigorous, but it may be "
                "entirely commuting. The genuinely nonabelian component-algebra "
                "mass and either branch's coherent compiler remain open."
            ),
        },
        status=(
            "nonscalarity-versus-noncommutative-algebra-boundary-proved-natural-mass-open"
            if exact
            else "component-effect-algebra-boundary-control-failure"
        ),
        summary=(
            "Separated full-rank component nonscalarity from genuinely "
            "noncommutative effect-algebra structure and identified the exact "
            "regular-master commutator-support target."
        ),
        falsifiers_triggered=[
            "Full-rank component nonscalarity does not imply a noncommutative effect algebra.",
            "Positive natural support mass of D_ns is not positive natural support mass of commutators.",
            "Finite low-dimensional noncommutativity is not an asymptotic natural-mass theorem.",
            "A commuting effect algebra may be algorithmically favorable if its joint eigenbasis is coherently accessible.",
        ],
    )


def write_component_effect_algebra_boundary_report(
    path: Path = REPORT_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = (
        "EXP-CODE-SELF-DUAL-WREATH-COMPONENT-EFFECT-ALGEBRA-BOUNDARY"
    ),
    registry_candidate_id: str = "CODE-COSET-COLLECTIVE",
    registry_result_id: str = "",
) -> dict[str, Any]:
    payload = asdict(run_component_effect_algebra_boundary())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")

    return payload


if __name__ == "__main__":
    report = write_component_effect_algebra_boundary_report()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))

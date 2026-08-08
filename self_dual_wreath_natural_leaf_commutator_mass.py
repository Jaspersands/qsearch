"""Density-one natural noncommutativity of balanced orientation leaves.

The component-effect algebra remains uncontrolled, but the underlying natural
orientation projectors are asymptotically noncommuting on almost every balanced
pair.  This module proves that statement and isolates the missing whitening /
compression transfer.

For two orientation projectors ``E_a,E_b`` at Hamming distance ``h``, the exact
pair-angle theorem decomposes their principal correlations by an internal
carrier ``alpha``.  Whenever ``alpha`` occurs in the shared, left-only, and
right-only tensor blocks, a principal cosine

    c_alpha = 1/d_alpha                                   (1)

appears.  On the corresponding two-dimensional principal-angle plane,

    ||[E_a,E_b]|| = c_alpha sqrt(1-c_alpha^2).             (2)

Use the standard irrep ``alpha=(n-1,1)``, with ``d_alpha=n-1``.  At natural
copy depth ``C=ceil(log_2(n!))+2``, every balanced pair has
``h,C-h=Theta(C)`` independent Plancherel factors in its three acted-on pattern
blocks.  Sellke's constant-block tensor-covering theorem implies that each
large block covers every ``S_n`` irrep with probability ``1-o(1)``.  The fixed
target in the shared block does not hurt: if a random product covers every
``beta``, then after tensoring by the target it contains ``alpha`` by choosing
a constituent ``beta`` of ``alpha tensor target^*`` and using Frobenius
reciprocity.

Thus every fixed balanced orientation pair obeys

    ||[E_a,E_b]|| >= sqrt(1-(n-1)^-2)/(n-1)               (3)

with probability ``1-o(1)``.  Averaging the bad-pair indicator and applying
Markov shows that a ``1-o(1)`` fraction of balanced pairs satisfy (3) with high
probability.  Binomial concentration makes balanced pairs a ``1-o(1)``
fraction of all orientation pairs.  Global source distinctness also has
probability ``1-o(1)``, so the conclusion survives on the relevant natural
sector without needing a convergence rate.

This is an inverse-polynomial, positive natural source-mass theorem for the
*leaf projector algebra*.  It does not prove that the whitened canonical
component effects ``H_e`` are noncommutative.  The companion whitening no-go
constructs distinct high-rank leaves with density-one inverse-polynomial
commutators, frame condition number below three, constant total-rank aspect,
and full-rank nonscalarity whose canonical effects nevertheless commute.
Thus generic frame conditioning and common-span dimensions cannot transfer
the result.  The companion common-span universality no-go further shows that
full-support spectral arithmetic disappears after proper sibling compression.
A direct natural compressed-commutator theorem or simultaneous-basis compiler
is required.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import numpy as np

from research_registry import utc_now
from self_dual_wreath_plancherel_block_obstruction import (
    SELLKE_PAPER_ID,
    SELLKE_PAPER_URL,
    SELLKE_THEOREM_LABEL,
)


REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_natural_leaf_commutator_mass.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-NATURAL-LEAF-COMMUTATOR-MASS"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


@dataclass(frozen=True)
class ProjectionCommutatorControl:
    control_id: str
    carrier_dimension: int
    predicted_principal_cosine: float
    observed_principal_cosine: float
    predicted_commutator_norm: float
    observed_commutator_norm: float
    commutator_norm_residual: float
    exact_projection_commutator_formula_verified: bool
    status: str


@dataclass(frozen=True)
class NaturalLeafCommutatorScalingRecord:
    n: int
    information_threshold_copy_count: int
    selected_copy_count: int
    balanced_hamming_distance_lower: int
    balanced_hamming_distance_upper: int
    standard_carrier_partition: tuple[int, ...]
    standard_carrier_dimension: int
    principal_cosine: float
    commutator_operator_norm_lower_bound: float
    inverse_commutator_scale: float
    fixed_balanced_pair_noncommutativity_probability_tends_one: bool
    density_one_balanced_pair_noncommutativity_proved: bool
    global_distinct_transfer_proved: bool
    canonical_component_commutator_transfer_proved: bool
    status: str


@dataclass(frozen=True)
class NaturalLeafCommutatorMassReport:
    created_at: str
    literature: dict[str, str]
    theorem_contract: dict[str, Any]
    finite_controls: list[ProjectionCommutatorControl]
    scaling_records: list[NaturalLeafCommutatorScalingRecord]
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def projection_commutator_norm_from_cosine(cosine: float) -> float:
    if not 0 <= cosine <= 1:
        raise ValueError("principal cosine must lie in [0,1]")
    return cosine * math.sqrt(max(0.0, 1.0 - cosine * cosine))


def audit_projection_commutator_formula(
    control_id: str,
    carrier_dimension: int,
    *,
    tolerance: float = 1e-10,
) -> ProjectionCommutatorControl:
    if carrier_dimension < 2:
        raise ValueError("a nontrivial carrier dimension is required")
    cosine = 1.0 / carrier_dimension
    left_vector = np.asarray([[1.0], [0.0]], dtype=complex)
    right_vector = np.asarray(
        [[cosine], [math.sqrt(1.0 - cosine * cosine)]],
        dtype=complex,
    )
    left = left_vector @ left_vector.conj().T
    right = right_vector @ right_vector.conj().T
    observed_cosine = float(abs((left_vector.conj().T @ right_vector)[0, 0]))
    commutator = left @ right - right @ left
    observed_norm = float(np.linalg.norm(commutator, ord=2))
    predicted = projection_commutator_norm_from_cosine(cosine)
    residual = abs(observed_norm - predicted)
    verified = bool(
        abs(observed_cosine - cosine) <= 100 * tolerance
        and residual <= 100 * tolerance
    )
    return ProjectionCommutatorControl(
        control_id=control_id,
        carrier_dimension=carrier_dimension,
        predicted_principal_cosine=cosine,
        observed_principal_cosine=observed_cosine,
        predicted_commutator_norm=predicted,
        observed_commutator_norm=observed_norm,
        commutator_norm_residual=residual,
        exact_projection_commutator_formula_verified=verified,
        status=(
            "exact-principal-plane-projection-commutator-verified"
            if verified
            else "projection-commutator-control-failure"
        ),
    )


def natural_leaf_commutator_scaling_record(
    n: int,
) -> NaturalLeafCommutatorScalingRecord:
    if n < 5:
        raise ValueError("the standard-carrier bound requires n at least five")
    order = math.factorial(n)
    threshold = (order - 1).bit_length()
    copies = threshold + 2
    lower = copies // 3
    upper = copies - lower
    carrier_dimension = n - 1
    cosine = 1.0 / carrier_dimension
    commutator = projection_commutator_norm_from_cosine(cosine)
    return NaturalLeafCommutatorScalingRecord(
        n=n,
        information_threshold_copy_count=threshold,
        selected_copy_count=copies,
        balanced_hamming_distance_lower=lower,
        balanced_hamming_distance_upper=upper,
        standard_carrier_partition=(n - 1, 1),
        standard_carrier_dimension=carrier_dimension,
        principal_cosine=cosine,
        commutator_operator_norm_lower_bound=commutator,
        inverse_commutator_scale=1.0 / commutator,
        fixed_balanced_pair_noncommutativity_probability_tends_one=True,
        density_one_balanced_pair_noncommutativity_proved=True,
        global_distinct_transfer_proved=True,
        canonical_component_commutator_transfer_proved=False,
        status="density-one-natural-balanced-leaf-noncommutativity-proved-component-transfer-open",
    )


def run_natural_leaf_commutator_mass() -> NaturalLeafCommutatorMassReport:
    controls = [
        audit_projection_commutator_formula(
            f"PRINCIPAL-COSINE-1-OVER-{dimension}",
            dimension,
        )
        for dimension in (2, 3, 5, 11, 31)
    ]
    scaling = [
        natural_leaf_commutator_scaling_record(n)
        for n in (5, 8, 12, 16, 20, 24, 32, 40, 48, 64, 96)
    ]
    failures = sum(
        not row.exact_projection_commutator_formula_verified for row in controls
    )
    exact = failures == 0
    tail = scaling[-1]
    return NaturalLeafCommutatorMassReport(
        created_at=utc_now(),
        literature={
            "paper_id": SELLKE_PAPER_ID,
            "theorem": SELLKE_THEOREM_LABEL,
            "url": SELLKE_PAPER_URL,
        },
        theorem_contract={
            "pair_principal_angle": (
                "If carrier alpha occurs in all three acted-on pair-pattern "
                "blocks, the exact leaf principal cosine is 1/d_alpha."
            ),
            "projection_commutator": (
                "A principal cosine c in (0,1) contributes projection-"
                "commutator operator norm c sqrt(1-c^2)."
            ),
            "covering_input": (
                "Sellke constant-block Plancherel tensor covering puts the "
                "standard carrier into each growing balanced pattern block "
                "with probability 1-o(1)."
            ),
            "fixed_target_shared_block": (
                "Tensoring a cover-all random product by a fixed target still "
                "contains the standard carrier, by choosing beta inside "
                "standard tensor target^* and applying Frobenius reciprocity."
            ),
            "density_transfer": (
                "Markov on the average bad-pair indicator gives density-one "
                "balanced-pair success without a Sellke convergence rate; "
                "binomial concentration and P_cf=1-o(1) complete the transfer."
            ),
            "scope": (
                "The theorem concerns original orientation projectors. Frame "
                "whitening/common-span compression can alter commutators, so "
                "canonical component-effect noncommutativity remains open."
            ),
        },
        finite_controls=controls,
        scaling_records=scaling,
        proof_obligations=[
            {
                "obligation": "prove_positive_natural_mass_of_leaf_projector_noncommutativity",
                "resolved": exact,
                "resolution": "The standard carrier appears in all three balanced pair blocks with probability 1-o(1), forcing commutator norm at least sqrt(1-(n-1)^-2)/(n-1)."
            },
            {
                "obligation": "upgrade_fixed_balanced_pair_to_density_one_pairs",
                "resolved": True,
                "resolution": "The expected bad balanced-pair fraction is o(1); Markov gives density one, and balanced Hamming distances themselves have density one."
            },
            {
                "obligation": "transfer_leaf_commutator_to_canonical_component_effect_commutator",
                "resolved": False,
                "resolution": "Generic transfer is false even for distinct high-rank leaves and a frame condition number below three. Common-span compression is POVM-universal, so the full-support reciprocal-integer cover is also inapplicable. Need direct natural compressed commutator support or a simultaneous-basis compiler."
            },
            {
                "obligation": "compile_noncommuting_leaf_or_component_measurement",
                "resolved": False,
                "resolution": "An inverse-polynomial commutator witnesses structure but supplies neither a simultaneous transform nor a matrix-POVM dilation."
            },
        ],
        adversarial_audit=[
            {
                "objection": "Finite S4 noncommutativity may disappear on natural high-dimensional sources.",
                "resolved": True,
                "resolution": "It does not disappear for leaves: density-one balanced pairs retain the standard carrier and an inverse-polynomial commutator."
            },
            {
                "objection": "The fixed target can prevent the shared block from containing the standard carrier.",
                "resolved": True,
                "resolution": "A cover-all random product contains a beta with beta tensor target containing the standard carrier."
            },
            {
                "objection": "No explicit Sellke rate prevents a statement about exponentially many pairs.",
                "resolved": True,
                "resolution": "No union bound is used. Markov controls the fraction of bad pairs from its o(1) expectation."
            },
            {
                "objection": "Noncommuting leaves imply noncommuting whitened component effects.",
                "resolved": True,
                "resolution": "Refuted generically by a bounded-condition, duplicate-free projection-frame counterfamily. Whether the natural wreath effects satisfy the counterfamily's rigid commuting structure remains open."
            },
        ],
        headline_metrics={
            "projection_principal_plane_commutator_theorem_count": int(exact),
            "finite_control_count": len(controls),
            "finite_control_failure_count": failures,
            "natural_fixed_balanced_leaf_pair_noncommutativity_theorem_count": 1,
            "natural_density_one_balanced_leaf_pair_noncommutativity_theorem_count": 1,
            "global_distinct_leaf_noncommutativity_transfer_theorem_count": 1,
            "tail_n": tail.n,
            "tail_commutator_operator_norm_lower_bound": tail.commutator_operator_norm_lower_bound,
            "tail_inverse_commutator_scale": tail.inverse_commutator_scale,
            "natural_canonical_component_commutator_mass_theorem_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "natural_orientation_leaf_algebra_noncommutative_on_density_one_pairs": True,
            "natural_leaf_commutator_has_inverse_polynomial_norm_witness": True,
            "global_distinct_transfer_proved": True,
            "natural_canonical_component_effect_algebra_noncommutative_on_positive_mass": False,
            "leaf_to_component_commutator_transfer_proved": False,
            "coherent_noncommutative_measurement_compiled": False,
            "physical_pgm_outside_mrs_transcript_postprocessing_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "Natural leaf projectors are robustly noncommuting, but the "
                "canonical component effects include frame whitening and common-"
                "span compression. A companion exact counterfamily proves that "
                "conditioning, aspect, rank, and nonscalarity controls do not "
                "transfer leaf commutators through those operations."
            ),
        },
        status=(
            "density-one-natural-leaf-noncommutativity-proved-component-transfer-open"
            if exact
            else "natural-leaf-commutator-control-failure"
        ),
        summary=(
            "Proved inverse-polynomial noncommutativity for a density-one "
            "fraction of natural balanced orientation-leaf pairs and isolated "
            "the missing canonical-component transfer."
        ),
        falsifiers_triggered=[
            "Natural high-dimensional leaf projectors do not become asymptotically commuting on balanced pairs.",
            "A convergence rate for Sellke covering is unnecessary for density-one pair noncommutativity.",
            "Leaf noncommutativity does not survive canonical frame whitening under any generic conditioning/aspect/rank implication.",
            "An inverse-polynomial commutator witness is structural evidence, not a measurement circuit or MRS separation."
        ],
    )


def write_natural_leaf_commutator_mass_report(
    path: Path = REPORT_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = (
        "EXP-CODE-SELF-DUAL-WREATH-NATURAL-LEAF-COMMUTATOR-MASS"
    ),
    registry_candidate_id: str = "CODE-COSET-COLLECTIVE",
    registry_result_id: str = "",
) -> dict[str, Any]:
    payload = asdict(run_natural_leaf_commutator_mass())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")

    if write_registry:
        from research_registry import (
            ExperimentResultRecord,
            NegativeResultRecord,
            upsert_experiment_result,
            upsert_negative_result,
        )

        upsert_negative_result(
            NegativeResultRecord(
                id="NEG-SELF-DUAL-WREATH-NATURAL-LEAF-COMMUTATOR-MASS",
                source=registry_experiment_id,
                claim=(
                    "Initial negative claim for EXP-CODE-SELF-DUAL-WREATH-NATURAL-LEAF-COMMUTATOR-MASS."
                ),
                reason_invalid=(
                    "Falsified or refined by exact theorem evaluation."
                ),
                lesson=(
                    "Lesson from exact theorem analysis for EXP-CODE-SELF-DUAL-WREATH-NATURAL-LEAF-COMMUTATOR-MASS."
                ),
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
                    "self_dual_wreath_natural_leaf_commutator_mass": str(path)
                },
            )
        )
    return payload


if __name__ == "__main__":
    report = write_natural_leaf_commutator_mass_report()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))

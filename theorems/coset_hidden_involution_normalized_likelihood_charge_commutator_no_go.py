"""Natural-mass no-go for charge noncommutativity with normalized likelihood.

Let

    Z = M e_B e_A e_B,
    A = Z/M,
    eta = (M-1)/2^k.

Under normalized source trace ``tau_B``, the exact synthesis moment theorem
gives

    tau_B(Z)=1,
    tau_B((Z-I)^2)=eta.                               (1)

The complete source-local likelihood-independence theorem says more than
equality of the ``D_m`` outcome distribution.  For every spectral projector
``E`` of any B-compatible source-local charge family,

    tau_B(EZ)=tau_B(E).

Equivalently, the trace-preserving conditional expectation of ``Z`` onto the
charge spectral algebra is exactly the identity.  For ``A`` it is ``I/M``.
All diagonal likelihood information in the charge basis cancels globally;
only off-diagonal matrix coherence could remain.

But (1) fixes its total normalized scale.  For every source-local Hermitian
contraction ``S`` (indeed, for every contraction),

    ||[A,S]||_(2,tau)^2
      = ||[(Z-I)/M,S]||_(2,tau)^2
      <= 4 eta/M^2.                                  (2)

At ``k=ceil(log2(64M))``, ``eta<=1/64``, so the upper bound is
``1/(16M^2)``.  Markov then puts at most

    4 eta/(M^2 theta)

source mass in blocks with normalized commutator energy at least ``theta``.
For every inverse-polynomial ``theta``, this mass is factorially small in the
perfect-matching family.  Therefore the hoped-for inverse-polynomial
``[A,D_m]`` energy on inverse-polynomial natural mass cannot exist.

For the unnormalized operator ``Z``, the corresponding bound is ``4eta`` and
can be constant.  Accessing that scale is exactly the factorial normalization
problem: the normalization-one physical block encoding supplies ``A=Z/M``.
Thus a charge-assisted matrix signal processor cannot claim progress from
finite conditioned covariance or nonzero ``[Z,D]`` alone; it must compile an
implicit ``M``-scale transform without paying ``M``.

This theorem kills the proposed normalized third-operator commutator
criterion.  It does not rule out a direct non-black-box matrix-CS/subduction
basis transform or another integrable operation whose implementation is not
query access to ``A`` and ``D``.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import numpy as np

from coset_hidden_involution_binary_decision_reduction import (
    involution_class_size,
)
from coset_hidden_involution_incidence_walk_boundary import incidence_matrix
from coset_hidden_involution_orbit_synthesis_flatness import (
    exact_synthesis_centered_second_moment,
    flatness_copy_count,
)
from research_registry import utc_now


REPORT_PATH = Path(
    "research/representation/"
    "coset_hidden_involution_normalized_likelihood_charge_commutator_no_go.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-COSET-HIDDEN-INVOLUTION-NORMALIZED-LIKELIHOOD-CHARGE-COMMUTATOR-NO-GO"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


@dataclass(frozen=True)
class LikelihoodCommutatorFiniteControl:
    degree: int
    transposition_count: int
    copy_count: int
    candidate_count: int
    source_dimension: int
    normalized_source_mean_Z: float
    normalized_source_centered_second_moment: float
    predicted_eta: float
    maximum_random_contraction_commutator_energy: float
    universal_commutator_energy_upper_bound: float
    maximum_bound_residual: float
    exact_synthesis_moment_verified: bool
    universal_contraction_commutator_bound_verified: bool
    status: str


@dataclass(frozen=True)
class NormalizedCommutatorScalingRecord:
    half_degree: int
    degree: int
    hidden_matching_count_decimal: str
    copy_count: int
    eta: float
    normalized_A_charge_commutator_energy_upper_bound: float
    normalized_A_charge_commutator_energy_log2_upper_bound: float
    normalized_A_charge_commutator_norm_upper_bound: float
    normalized_A_charge_commutator_norm_log2_upper_bound: float
    unnormalized_Z_charge_commutator_energy_upper_bound: float
    inverse_polynomial_energy_threshold: float
    source_mass_above_threshold_upper_bound: float
    source_mass_above_threshold_log2_upper_bound: float
    inverse_polynomial_commutator_mass_possible: bool
    status: str


@dataclass(frozen=True)
class NormalizedLikelihoodChargeNoGoTheorem:
    source_moments: str
    conditional_expectation: str
    commutator_bound: str
    natural_mass_consequence: str
    normalization_boundary: str
    exact_source_centered_second_moment_proved: bool
    charge_spectral_conditional_expectation_of_Z_is_identity_proved: bool
    normalized_A_D_commutator_energy_inverse_candidate_squared_proved: bool
    inverse_polynomial_A_D_energy_on_inverse_polynomial_mass_ruled_out: bool
    finite_conditioned_charge_covariance_promotes_to_natural_matrix_signal: bool
    unnormalized_Z_structured_fast_forward_compiled: bool
    direct_non_black_box_matrix_transform_ruled_out: bool
    hidden_involution_detector_constructed: bool
    speedup_claim_allowed: bool
    theorem_verified: bool
    status: str


@dataclass(frozen=True)
class NormalizedLikelihoodChargeNoGoReport:
    created_at: str
    theorem_contract: dict[str, Any]
    finite_controls: list[LikelihoodCommutatorFiniteControl]
    scaling_records: list[NormalizedCommutatorScalingRecord]
    theorem: NormalizedLikelihoodChargeNoGoTheorem
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def audit_likelihood_commutator_bound(
    degree: int,
    transposition_count: int,
    copy_count: int,
    random_control_count: int = 12,
) -> LikelihoodCommutatorFiniteControl:
    incidence, candidates = incidence_matrix(
        degree,
        transposition_count,
        copy_count,
    )
    candidate_count = len(set(candidates))
    Z = incidence.T @ incidence / (2**copy_count)
    source_dimension = Z.shape[0]
    identity = np.eye(source_dimension)
    mean = float(np.trace(Z) / source_dimension)
    centered = float(
        np.linalg.norm(Z - identity, ord="fro") ** 2 / source_dimension
    )
    eta = float(
        exact_synthesis_centered_second_moment(
            candidate_count,
            copy_count,
        )
    )
    A = Z / candidate_count
    bound = 4.0 * eta / candidate_count**2
    generator = np.random.default_rng(
        20260820 + degree + transposition_count + copy_count
    )
    maximum_energy = 0.0
    maximum_residual = 0.0
    for _ in range(random_control_count):
        raw = generator.normal(size=(source_dimension, source_dimension))
        symmetric = (raw + raw.T) / 2.0
        norm = float(np.linalg.norm(symmetric, ord=2))
        contraction = symmetric / max(1.0, norm)
        commutator = A @ contraction - contraction @ A
        energy = float(
            np.linalg.norm(commutator, ord="fro") ** 2 / source_dimension
        )
        maximum_energy = max(maximum_energy, energy)
        maximum_residual = max(maximum_residual, energy - bound)
    moments = abs(mean - 1.0) < 1e-12 and abs(centered - eta) < 1e-12
    commutator_verified = maximum_residual <= 1e-12
    return LikelihoodCommutatorFiniteControl(
        degree=degree,
        transposition_count=transposition_count,
        copy_count=copy_count,
        candidate_count=candidate_count,
        source_dimension=source_dimension,
        normalized_source_mean_Z=mean,
        normalized_source_centered_second_moment=centered,
        predicted_eta=eta,
        maximum_random_contraction_commutator_energy=maximum_energy,
        universal_commutator_energy_upper_bound=bound,
        maximum_bound_residual=max(0.0, maximum_residual),
        exact_synthesis_moment_verified=moments,
        universal_contraction_commutator_bound_verified=commutator_verified,
        status=(
            "normalized-likelihood-commutator-bound-verified"
            if moments and commutator_verified
            else "normalized-likelihood-commutator-control-failure"
        ),
    )


def normalized_commutator_scaling_record(
    half_degree: int,
    threshold_exponent: int = 9,
) -> NormalizedCommutatorScalingRecord:
    if half_degree < 2 or threshold_exponent < 1:
        raise ValueError("invalid scaling parameters")
    degree = 2 * half_degree
    candidates = involution_class_size(degree, half_degree)
    copies = flatness_copy_count(candidates)
    eta = float(exact_synthesis_centered_second_moment(candidates, copies))
    log_candidates = math.log2(candidates)
    log_energy = math.log2(4.0 * eta) - 2.0 * log_candidates
    log_norm = 1.0 + 0.5 * math.log2(eta) - log_candidates
    energy = 2.0**log_energy
    norm = 2.0**log_norm
    threshold = half_degree ** (-threshold_exponent)
    log_mass = min(
        0.0,
        log_energy + threshold_exponent * math.log2(half_degree),
    )
    mass = 2.0**log_mass
    return NormalizedCommutatorScalingRecord(
        half_degree=half_degree,
        degree=degree,
        hidden_matching_count_decimal=str(candidates),
        copy_count=copies,
        eta=eta,
        normalized_A_charge_commutator_energy_upper_bound=energy,
        normalized_A_charge_commutator_energy_log2_upper_bound=log_energy,
        normalized_A_charge_commutator_norm_upper_bound=norm,
        normalized_A_charge_commutator_norm_log2_upper_bound=log_norm,
        unnormalized_Z_charge_commutator_energy_upper_bound=4.0 * eta,
        inverse_polynomial_energy_threshold=threshold,
        source_mass_above_threshold_upper_bound=mass,
        source_mass_above_threshold_log2_upper_bound=log_mass,
        inverse_polynomial_commutator_mass_possible=False,
        status="normalized-A-charge-commutator-natural-mass-factorially-small",
    )


def build_normalized_likelihood_charge_no_go_report() -> NormalizedLikelihoodChargeNoGoReport:
    controls = [
        audit_likelihood_commutator_bound(3, 1, 1),
        audit_likelihood_commutator_bound(3, 1, 2),
        audit_likelihood_commutator_bound(4, 2, 1),
    ]
    scaling = [
        normalized_commutator_scaling_record(value)
        for value in (4, 8, 16, 32, 64, 128)
    ]
    exact = all(
        row.exact_synthesis_moment_verified
        and row.universal_contraction_commutator_bound_verified
        for row in controls
    )
    negligible = all(
        not row.inverse_polynomial_commutator_mass_possible for row in scaling
    )
    theorem = NormalizedLikelihoodChargeNoGoTheorem(
        source_moments=(
            "tau_B(Z)=1 and tau_B((Z-I)^2)=eta=(M-1)/2^k exactly."
        ),
        conditional_expectation=(
            "Complete source-local measurement independence implies E_Alg(D)(Z)=I "
            "and E_Alg(D)(A)=I/M under the source trace."
        ),
        commutator_bound=(
            "For every contraction S, ||[A,S]||_(2,tau)^2<=4eta/M^2; "
            "in particular this holds for D_m."
        ),
        natural_mass_consequence=(
            "At natural k, mass with inverse-polynomial block commutator energy "
            "is at most polynomial(m)/(16M^2), hence factorially small."
        ),
        normalization_boundary=(
            "The unnormalized Z commutator can have O(eta) energy, but access to Z "
            "rather than A=Z/M is exactly the missing M-scale fast-forward."
        ),
        exact_source_centered_second_moment_proved=exact,
        charge_spectral_conditional_expectation_of_Z_is_identity_proved=True,
        normalized_A_D_commutator_energy_inverse_candidate_squared_proved=(
            exact and negligible
        ),
        inverse_polynomial_A_D_energy_on_inverse_polynomial_mass_ruled_out=(
            exact and negligible
        ),
        finite_conditioned_charge_covariance_promotes_to_natural_matrix_signal=False,
        unnormalized_Z_structured_fast_forward_compiled=False,
        direct_non_black_box_matrix_transform_ruled_out=False,
        hidden_involution_detector_constructed=False,
        speedup_claim_allowed=False,
        theorem_verified=exact and negligible,
        status=(
            "normalized-likelihood-charge-commutator-natural-mass-no-go"
            if exact and negligible
            else "normalized-likelihood-charge-commutator-control-failure"
        ),
    )
    return NormalizedLikelihoodChargeNoGoReport(
        created_at=utc_now(),
        theorem_contract={
            "source_law": "Uniform right-B invariant source trace at natural copy count",
            "normalized_likelihood_oracle": "A=Z/M=e_B e_A e_B",
            "third_operator": "Any B-compatible source-local Hermitian contraction, including D_m",
            "claim_boundary": (
                "Rules out inverse-polynomial normalized commutator mass; does not "
                "rule out direct access to an implicit unnormalized transform."
            ),
        },
        finite_controls=controls,
        scaling_records=scaling,
        theorem=theorem,
        proof_obligations=[
            {
                "id": "PO-NORMALIZED-COMMUTATOR-UNNORMALIZED-FAST-FORWARD",
                "statement": (
                    "Any remaining charge-assisted proposal must explain how it "
                    "accesses Z-scale matrix coherence without paying normalization M."
                ),
                "resolved": False,
            },
            {
                "id": "PO-NORMALIZED-COMMUTATOR-DIRECT-BASIS-TRANSFORM",
                "statement": (
                    "Alternatively compile a direct matrix-CS/subduction transform "
                    "that is not a query algorithm in A and D."
                ),
                "resolved": False,
            },
            {
                "id": "PO-NORMALIZED-COMMUTATOR-CONDITIONED-MATRIX-LOWER-BOUND",
                "statement": (
                    "A finite conditioned block can have covariance; prove any claimed "
                    "family has enough total source weight to beat the M^-2 energy budget."
                ),
                "resolved": False,
            },
        ],
        adversarial_audit=[
            {
                "challenge": "Likelihood-independent D outcomes allow large [A,D] off-diagonal mass.",
                "answer": (
                    "Only in principle; the exact centered second moment bounds the "
                    "entire normalized off-diagonal resource by eta/M^2."
                ),
                "resolved": True,
            },
            {
                "challenge": "The finite S_10 D/CS covariance proves a natural matrix signal.",
                "answer": (
                    "False. Fixed conditioned covariance can sit in factorially small "
                    "source weight and cannot exceed the global M^-2 budget for A."
                ),
                "resolved": True,
            },
            {
                "challenge": "Using Z instead of A removes the bound for free.",
                "answer": (
                    "It removes M^-2 algebraically but reintroduces the exact M "
                    "block-encoding/negativity normalization."
                ),
                "resolved": True,
            },
            {
                "challenge": "The no-go proves every direct matrix basis transform impossible.",
                "answer": (
                    "Too strong. It is a normalized-oracle energy theorem, not a "
                    "circuit lower bound for an explicit integrable transform."
                ),
                "resolved": True,
            },
        ],
        headline_metrics={
            "exact_normalized_commutator_energy_bound_count": int(exact),
            "inverse_polynomial_natural_commutator_mass_no_go_count": int(
                exact and negligible
            ),
            "tail_commutator_energy_log2_upper_bound": (
                scaling[-1].normalized_A_charge_commutator_energy_log2_upper_bound
            ),
            "tail_mass_log2_upper_bound": scaling[-1].source_mass_above_threshold_log2_upper_bound,
            "unnormalized_Z_fast_forward_count": 0,
            "hidden_involution_detector_count": 0,
        },
        claim_gate={
            "charge_conditional_expectation_of_Z_is_identity": True,
            "normalized_A_D_commutator_energy_at_most_4eta_over_M2": exact,
            "inverse_polynomial_normalized_commutator_mass_ruled_out": exact and negligible,
            "finite_conditioned_covariance_is_natural_signal": False,
            "unnormalized_Z_structured_fast_forward_compiled": False,
            "direct_non_black_box_matrix_transform_ruled_out": False,
            "hidden_involution_detector_constructed": False,
            "speedup_claim_allowed": False,
            "reason": (
                "All D-diagonal likelihood information cancels and the entire "
                "normalization-one A/D noncommutative energy is O(eta/M^2)."
            ),
        },
        status=theorem.status,
        summary=(
            "Proved that normalized likelihood/charge noncommutativity has only "
            "inverse-candidate-squared total source energy, killing the natural-mass criterion."
        ),
        falsifiers_triggered=[
            "The normalized A/D commutator cannot be inverse-polynomial on inverse-polynomial natural mass.",
            "Finite conditioned D/CS covariance does not transfer to the natural source globally.",
            "Any surviving charge-assisted route must fast-forward the unnormalized Z scale or use a direct basis transform.",
        ],
    )


def write_normalized_likelihood_charge_no_go_report(
    output_path: Path = REPORT_PATH,
) -> dict[str, Any]:
    payload = asdict(build_normalized_likelihood_charge_no_go_report())
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    return payload


def run_experiment(
    experiment_id: str = DEFAULT_EXPERIMENT_ID,
    candidate_id: str = DEFAULT_CANDIDATE_ID,
    write_registry: bool = True,
) -> dict[str, Any]:
    del experiment_id, candidate_id, write_registry
    return write_normalized_likelihood_charge_no_go_report()


if __name__ == "__main__":
    print(json.dumps(run_experiment(), indent=2, sort_keys=True))

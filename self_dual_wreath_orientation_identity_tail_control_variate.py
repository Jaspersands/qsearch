"""Identity-tail control variate for orientation-syndrome Racah signals.

Let ``mu_y=A_y/D`` be the normalized word-map amplitude of one six-label
transpose-pair orbit, ``G=|S_n|``, and ``D=prod_i d_i``.  The single word
triple ``g=h=k=e`` contributes exactly ``G^-3`` to every ``mu_y``.  Define

    ell_y = G^3 mu_y = 1 + delta_y.                       (1)

The coarse independent sign-orbit product mass and physical mass are

    Q_orbit = 64 D^2/G^6,
    P_orbit = 8 D^2 sum_y(mu_y)/G^3.                      (2)

Consequently

    P_orbit/Q_orbit = (1/8) sum_y ell_y
                    = 1 + (1/8) sum_y delta_y,            (3)

and the conditional orientation-syndrome law is

    p_y = ell_y / sum_z ell_z
        = (1+delta_y)/(8 P_orbit/Q_orbit).                (4)

Thus the identity triple is exactly the product-law null, not evidence for
Racah structure.  All non-Haar information lives in the signed nonidentity
residual ``delta``.  Subtracting the identity contribution is an exact
classical control variate, although it does not make the residual efficiently
computable.

The raw uniform word estimator also has a rigorous variance warning.  Since
its squared value is one at the identity triple,

    Var(X_y) >= G^-3 - mu_y^2.                            (5)

This is a lower bound only for that raw estimator.  The identity control
variate removes (5), so it is not a classical query lower bound.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from research_registry import utc_now
from self_dual_wreath_compressed_orientation_racah_cumulant_probe import (
    CompressedOrientationRacahControl,
    audit_s5_exact_amplitude_cross_check,
    compile_orientation_racah_channel,
)


REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_orientation_identity_tail_control_variate.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-ORIENTATION-IDENTITY-TAIL-CONTROL-VARIATE"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


@dataclass(frozen=True)
class OrientationIdentityTailControl:
    control_id: str
    n: int
    group_order: int
    dimension_product: int
    normalized_amplitudes: tuple[float, ...]
    identity_rescaled_likelihoods: tuple[float, ...]
    nonidentity_residuals: tuple[float, ...]
    coarse_product_orbit_mass: float
    physical_orbit_mass: float
    physical_to_product_likelihood_ratio: float
    likelihood_ratio_from_residual_mean: float
    likelihood_identity_residual: float
    conditional_syndrome_probabilities_from_residual: tuple[float, ...]
    maximum_conditional_probability_residual: float
    maximum_absolute_nonidentity_residual: float
    mean_nonidentity_residual: float
    negative_nonidentity_residual_count: int
    raw_estimator_minimum_relative_variance_lower_bound: float
    raw_estimator_maximum_relative_variance_lower_bound: float
    irreducible_racah_cmi_bits: float
    identity_subtracted_residual_efficiently_computable: bool
    exact_identity_product_null_verified: bool
    status: str


@dataclass(frozen=True)
class OrientationIdentityTailControlVariateReport:
    created_at: str
    theorem_contract: dict[str, Any]
    controls: list[OrientationIdentityTailControl]
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def coarse_sign_orbit_product_mass(dimension_product: int, group_order: int) -> float:
    if dimension_product < 1 or group_order < 1:
        raise ValueError("positive dimensions and group order are required")
    return 64.0 * dimension_product**2 / group_order**6


def raw_relative_variance_lower_bound(
    normalized_amplitude: float,
    group_order: int,
) -> float:
    """Identity-event lower bound for the unmodified uniform estimator."""

    if normalized_amplitude <= 0:
        return math.inf
    return max(0.0, group_order**-3 / normalized_amplitude**2 - 1.0)


def audit_orientation_identity_tail(
    control: CompressedOrientationRacahControl,
) -> OrientationIdentityTailControl:
    group_order = math.factorial(control.n)
    dimension_product = math.prod(control.base_dimensions)
    amplitudes = tuple(
        entry.normalized_syndrome_amplitude / dimension_product
        for entry in control.entries
    )
    likelihoods = tuple(group_order**3 * value for value in amplitudes)
    residuals = tuple(value - 1.0 for value in likelihoods)
    product_mass = coarse_sign_orbit_product_mass(dimension_product, group_order)
    likelihood_ratio = control.physical_sign_orbit_tuple_mass / product_mass
    residual_likelihood = 1.0 + sum(residuals) / 8.0
    total_likelihood = sum(likelihoods)
    probabilities = tuple(value / total_likelihood for value in likelihoods)
    probability_residual = max(
        abs(left - right)
        for left, right in zip(
            probabilities, control.conditional_syndrome_probabilities
        )
    )
    variance_bounds = tuple(
        raw_relative_variance_lower_bound(value, group_order)
        for value in amplitudes
    )
    finite_bounds = tuple(value for value in variance_bounds if math.isfinite(value))
    verified = bool(
        abs(likelihood_ratio - residual_likelihood) <= 2e-10
        and probability_residual <= 2e-10
        and all(value >= -2e-10 for value in likelihoods)
    )
    return OrientationIdentityTailControl(
        control_id=control.control_id,
        n=control.n,
        group_order=group_order,
        dimension_product=dimension_product,
        normalized_amplitudes=amplitudes,
        identity_rescaled_likelihoods=likelihoods,
        nonidentity_residuals=residuals,
        coarse_product_orbit_mass=product_mass,
        physical_orbit_mass=control.physical_sign_orbit_tuple_mass,
        physical_to_product_likelihood_ratio=likelihood_ratio,
        likelihood_ratio_from_residual_mean=residual_likelihood,
        likelihood_identity_residual=abs(likelihood_ratio - residual_likelihood),
        conditional_syndrome_probabilities_from_residual=probabilities,
        maximum_conditional_probability_residual=probability_residual,
        maximum_absolute_nonidentity_residual=max(map(abs, residuals)),
        mean_nonidentity_residual=sum(residuals) / 8.0,
        negative_nonidentity_residual_count=sum(value < -1e-12 for value in residuals),
        raw_estimator_minimum_relative_variance_lower_bound=(
            min(finite_bounds) if finite_bounds else math.inf
        ),
        raw_estimator_maximum_relative_variance_lower_bound=max(variance_bounds),
        irreducible_racah_cmi_bits=control.irreducible_racah_cmi_bits,
        identity_subtracted_residual_efficiently_computable=False,
        exact_identity_product_null_verified=verified,
        status=(
            "identity-triple-is-exact-product-null-control-variate"
            if verified
            else "identity-tail-product-null-control-failure"
        ),
    )


def run_orientation_identity_tail_control_variate(
) -> OrientationIdentityTailControlVariateReport:
    _cross_check, s5 = audit_s5_exact_amplitude_cross_check()
    s6 = compile_orientation_racah_channel(
        "S6-REPEATED-DIMENSION-10", ((3, 1, 1, 1),) * 6
    )
    s7 = compile_orientation_racah_channel(
        "S7-REPEATED-DIMENSION-35", ((3, 2, 1, 1),) * 6
    )
    controls = [audit_orientation_identity_tail(row) for row in (s5, s6, s7)]
    failures = sum(not row.exact_identity_product_null_verified for row in controls)
    s6_row, s7_row = controls[1], controls[2]
    return OrientationIdentityTailControlVariateReport(
        created_at=utc_now(),
        theorem_contract={
            "identity_contribution": "mu_y^(identity)=|S_n|^-3 for every syndrome y",
            "rescaled_amplitude": "ell_y=|S_n|^3 mu_y=1+delta_y",
            "coarse_product_mass": "Q_orbit=64 D^2/|S_n|^6",
            "physical_likelihood": "P_orbit/Q_orbit=(1/8) sum_y ell_y=1+mean_y delta_y",
            "conditional_channel": "p_y=(1+delta_y)/(8 P_orbit/Q_orbit)",
            "raw_variance_warning": "Var(X_y)>=|S_n|^-3-mu_y^2 before control-variate subtraction",
            "scope": "exact null decomposition; no efficient residual algorithm or lower bound",
        },
        controls=controls,
        proof_obligations=[
            {
                "obligation": "separate_product_null_from_nonhaar_orientation_signal",
                "resolved": failures == 0,
                "resolution": "The identity triple contributes exactly the entire independent coarse-orbit product null.",
            },
            {
                "obligation": "subtract_all_polynomially_enumerable_low_support_word_strata",
                "resolved": False,
                "resolution": "Identity subtraction is only the first control variate; fixed-support conjugacy strata may explain further residual mass.",
            },
            {
                "obligation": "prove_residual_survives_on_positive_natural_mass",
                "resolved": False,
                "resolution": "S6 is low mass and S7 is nearly product in aggregate; no scalable residual family exists.",
            },
            {
                "obligation": "give_efficient_classical_or_coherent_residual_estimator",
                "resolved": False,
                "resolution": "The signed nonidentity correction remains a Racah/three-projector contraction.",
            },
        ],
        adversarial_audit=[
            {
                "objection": "The identity event itself is a quantum structural signal.",
                "resolved": True,
                "resolution": "It reconstructs exactly the independent coarse product-law mass and a uniform syndrome contribution.",
            },
            {
                "objection": "The raw estimator variance is a classical lower bound.",
                "resolved": True,
                "resolution": "Subtracting the known identity event removes that variance term exactly; other estimators remain possible.",
            },
            {
                "objection": "High S7 physical orbit mass means a large non-Haar effect.",
                "resolved": True,
                "resolution": "Its physical/product likelihood ratio is about 0.997935 and its irreducible CMI is about 2.3e-5 bits.",
            },
            {
                "objection": "The S6 one-bit channel is robust positive structure.",
                "resolved": True,
                "resolution": "Six amplitudes result from near-total signed cancellation of the identity baseline, the orbit mass is about 1.07e-4, and exact zero is still unproved.",
            },
        ],
        headline_metrics={
            "exact_identity_product_null_control_count": len(controls) - failures,
            "finite_control_failure_count": failures,
            "S6_physical_to_product_likelihood_ratio": s6_row.physical_to_product_likelihood_ratio,
            "S6_maximum_absolute_nonidentity_residual": s6_row.maximum_absolute_nonidentity_residual,
            "S7_physical_to_product_likelihood_ratio": s7_row.physical_to_product_likelihood_ratio,
            "S7_maximum_absolute_nonidentity_residual": s7_row.maximum_absolute_nonidentity_residual,
            "S7_irreducible_cmi_bits": s7_row.irreducible_racah_cmi_bits,
            "efficient_nonidentity_residual_estimator_count": 0,
            "classical_lower_bound_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "identity_is_exact_product_null_proved": failures == 0,
            "identity_control_variate_available": True,
            "S6_spike_survives_identity_audit_as_scalable_signal": False,
            "S7_high_mass_sector_has_large_aggregate_nonhaar_likelihood": False,
            "fixed_support_residuals_subtracted": False,
            "residual_positive_mass_scaling_proved": False,
            "efficient_classical_residual_estimator_proved": False,
            "classical_lower_bound_proved": False,
            "algorithm_claim_allowed": False,
            "speedup_claim_allowed": False,
            "reason": "The product null is now explicit; only a signed nonidentity Racah residual remains, with no scalable positive-mass family or complexity separation.",
        },
        status=(
            "orientation-signals-reduced-to-signed-nonidentity-racah-residual"
            if failures == 0
            else "orientation-identity-tail-control-failure"
        ),
        summary=(
            "Proved that the identity word triple is exactly the independent "
            "sign-orbit product null and demoted both finite orientation signals "
            "to unresolved signed nonidentity residuals."
        ),
        falsifiers_triggered=[
            "Raw word-estimator rarity is removable by an exact identity control variate.",
            "Large physical orbit mass can coincide with an almost unit product-law likelihood ratio.",
            "A finite one-bit channel created by cancellation is not a robust asymptotic mechanism.",
        ],
    )


def write_orientation_identity_tail_control_variate_report(
    path: Path = REPORT_PATH,
) -> dict[str, Any]:
    payload = asdict(run_orientation_identity_tail_control_variate())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    return payload


if __name__ == "__main__":
    report = write_orientation_identity_tail_control_variate_report()
    print(json.dumps(report, indent=2, sort_keys=True))

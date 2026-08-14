"""Irreducible Racah information reduces to two quadratic Walsh cumulants.

Let ``p(g,h,k)`` be one normalized adaptive syndrome channel and write its
Walsh coefficients as

    r_abc = sum_(g,h,k) (-1)^(ag+bh+ck) p(g,h,k).

For a fixed value of ``k``, define the unnormalized ``2 x 2`` slice determinant

    delta_k = p(0,0,k)p(1,1,k)-p(0,1,k)p(1,0,k).          (1)

The channel is in the rank-compatible Markov family ``G--K--H`` exactly when
``delta_0=delta_1=0``.  Writing ``s=(-1)^k``, direct Walsh inversion gives

    16 delta_k = C_s,

    C_s = (1+s r_001)(r_110+s r_111)
          -(r_100+s r_101)(r_010+s r_011).                (2)

Thus the irreducible non-Haar Racah target is precisely two quadratic
cumulants of the seven parity-coset ratios ``F_x/F_0``.  This is more
structured than controlling all seven coefficients separately.

Let ``t_k=P(K=k)``, ``r_gk=P(G=g,K=k)``, and
``c_hk=P(H=h,K=k)``.  The information projection ``q=Pi_M(p)`` obeys the exact
entrywise residual

    p(g,h,k)-q(g,h,k)=(-1)^(g+h) delta_k/t_k.              (3)

Consequently

    TV(p,q)=2 sum_(k:t_k>0) |delta_k|/t_k,                (4)

    chi2(p||q)=sum_k delta_k^2 t_k /
                         (r_0k r_1k c_0k c_1k),           (5)

with the usual support conventions.  Since
``D_bits(p||q)=I(G;H|K)``, Pinsker and the chi-square inequality give

    2 TV(p,q)^2/ln(2) <= I(G;H|K) <= log2(1+chi2(p||q)).  (6)

Equations (2)--(6) are exact proof interfaces.  A lower bound on either
properly normalized determinant proves irreducible Racah information; an
upper bound must also control small conditional marginals.

The even/odd cube binomial is only the product of the two conditional odds
ratios and is weaker than the pair of minors.  A strictly positive rational
channel can satisfy the cube binomial while both conditional determinants are
nonzero.  Therefore the earlier cube test is a useful obstruction but cannot
replace the two-cumulant target.

No asymptotic cumulant bound, coherent estimator, classical separation,
algorithm, or speedup is proved here.
"""

from __future__ import annotations

import itertools
import json
import math
from dataclasses import asdict, dataclass
from fractions import Fraction
from pathlib import Path
from typing import Any, Iterable

from research_registry import utc_now
from self_dual_wreath_parity_projector_orbit_variance import BITS, walsh_transform
from self_dual_wreath_parity_racah_information_projection import (
    audit_information_projection,
    conditional_independence_minor_residual,
    kl_divergence_bits,
    markov_information_projection,
)
from self_dual_wreath_parity_racah_toric_obstruction import (
    cube_binomial_defect,
    exact_natural_syndrome_amplitudes,
)


REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_parity_racah_conditional_cumulant.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-PARITY-RACAH-CONDITIONAL-CUMULANT"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


@dataclass(frozen=True)
class ConditionalCumulantControl:
    control_id: str
    probabilities: tuple[float, ...]
    walsh_coefficients: tuple[float, ...]
    direct_conditional_determinants: tuple[float, float]
    walsh_conditional_determinants: tuple[float, float]
    maximum_walsh_determinant_residual: float
    conditional_k_masses: tuple[float, float]
    exact_total_variation_from_markov_projection: float
    determinant_total_variation_formula: float
    total_variation_formula_residual: float
    exact_chi_square_from_markov_projection: float
    determinant_chi_square_formula: float
    chi_square_formula_residual: float
    irreducible_racah_cmi_bits: float
    pinsker_lower_bound_bits: float
    chi_square_upper_bound_bits: float
    information_bound_violation: float
    exact_conditional_cumulant_reduction_verified: bool
    status: str


@dataclass(frozen=True)
class CubeInsufficiencyControl:
    exact_probabilities: tuple[str, ...]
    exact_cube_binomial_defect: str
    exact_conditional_determinants: tuple[str, str]
    conditional_mutual_information_bits: float
    strictly_positive: bool
    cube_identity_holds: bool
    conditionally_independent: bool
    exact_cube_insufficiency_verified: bool
    status: str


@dataclass(frozen=True)
class ParityRacahConditionalCumulantReport:
    created_at: str
    theorem_contract: dict[str, Any]
    channel_controls: list[ConditionalCumulantControl]
    cube_insufficiency_counterexample: CubeInsufficiencyControl
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def normalize_probabilities(values: Iterable[float]) -> tuple[float, ...]:
    entries = tuple(max(0.0, float(value)) for value in values)
    if len(entries) != 8:
        raise ValueError("eight syndrome values are required")
    total = sum(entries)
    if total <= 0:
        raise ValueError("syndrome channel must have positive mass")
    return tuple(value / total for value in entries)


def conditional_determinants(
    probabilities: Iterable[float | Fraction],
) -> tuple[float | Fraction, float | Fraction]:
    entries = dict(zip(BITS, tuple(probabilities)))
    if len(entries) != 8:
        raise ValueError("eight syndrome values are required")
    return tuple(
        entries[0, 0, k] * entries[1, 1, k]
        - entries[0, 1, k] * entries[1, 0, k]
        for k in (0, 1)
    )


def walsh_conditional_determinants(
    walsh_coefficients: Iterable[float],
) -> tuple[float, float]:
    coefficients = dict(zip(BITS, tuple(float(value) for value in walsh_coefficients)))
    if len(coefficients) != 8:
        raise ValueError("eight Walsh coefficients are required")
    if abs(coefficients[0, 0, 0] - 1.0) > 1e-9:
        raise ValueError("normalized channel must have Walsh coefficient r_000=1")
    output = []
    for k in (0, 1):
        sign = 1.0 if k == 0 else -1.0
        cumulant = (
            (1.0 + sign * coefficients[0, 0, 1])
            * (coefficients[1, 1, 0] + sign * coefficients[1, 1, 1])
            - (coefficients[1, 0, 0] + sign * coefficients[1, 0, 1])
            * (coefficients[0, 1, 0] + sign * coefficients[0, 1, 1])
        )
        output.append(cumulant / 16.0)
    return tuple(output)


def markov_residual_total_variation_formula(
    probabilities: Iterable[float],
) -> float:
    entries = dict(zip(BITS, tuple(float(value) for value in probabilities)))
    determinants = conditional_determinants(entries.values())
    result = 0.0
    for k, determinant in enumerate(determinants):
        mass = sum(entries[g, h, k] for g in (0, 1) for h in (0, 1))
        if mass > 0:
            result += 2.0 * abs(float(determinant)) / mass
    return result


def markov_residual_chi_square_formula(
    probabilities: Iterable[float],
) -> float:
    entries = dict(zip(BITS, tuple(float(value) for value in probabilities)))
    determinants = conditional_determinants(entries.values())
    result = 0.0
    for k, determinant in enumerate(determinants):
        mass = sum(entries[g, h, k] for g in (0, 1) for h in (0, 1))
        rows = tuple(sum(entries[g, h, k] for h in (0, 1)) for g in (0, 1))
        columns = tuple(sum(entries[g, h, k] for g in (0, 1)) for h in (0, 1))
        denominator = math.prod((*rows, *columns))
        if denominator == 0:
            if abs(float(determinant)) > 1e-15:
                return math.inf
            continue
        result += float(determinant) ** 2 * mass / denominator
    return result


def audit_conditional_cumulant(
    control_id: str,
    probabilities: Iterable[float],
    *,
    tolerance: float = 1e-9,
) -> ConditionalCumulantControl:
    normalized = normalize_probabilities(probabilities)
    walsh = walsh_transform(normalized)
    direct = tuple(float(value) for value in conditional_determinants(normalized))
    from_walsh = walsh_conditional_determinants(walsh)
    walsh_residual = max(abs(a - b) for a, b in zip(direct, from_walsh))
    projection = markov_information_projection(normalized)
    exact_tv = 0.5 * sum(abs(a - b) for a, b in zip(normalized, projection))
    determinant_tv = markov_residual_total_variation_formula(normalized)
    tv_residual = abs(exact_tv - determinant_tv)
    exact_chi = sum(
        (value - reference) ** 2 / reference
        for value, reference in zip(normalized, projection)
        if reference > 0
    )
    determinant_chi = markov_residual_chi_square_formula(normalized)
    chi_residual = abs(exact_chi - determinant_chi)
    cmi = kl_divergence_bits(normalized, projection)
    pinsker = 2.0 * exact_tv**2 / math.log(2.0)
    chi_upper = math.log2(1.0 + exact_chi)
    bound_violation = max(0.0, pinsker - cmi, cmi - chi_upper)
    k_masses = tuple(
        sum(normalized[BITS.index((g, h, k))] for g in (0, 1) for h in (0, 1))
        for k in (0, 1)
    )
    verified = bool(
        walsh_residual <= tolerance
        and tv_residual <= tolerance
        and chi_residual <= tolerance
        and bound_violation <= tolerance
    )
    return ConditionalCumulantControl(
        control_id=control_id,
        probabilities=normalized,
        walsh_coefficients=walsh,
        direct_conditional_determinants=direct,
        walsh_conditional_determinants=from_walsh,
        maximum_walsh_determinant_residual=walsh_residual,
        conditional_k_masses=k_masses,
        exact_total_variation_from_markov_projection=exact_tv,
        determinant_total_variation_formula=determinant_tv,
        total_variation_formula_residual=tv_residual,
        exact_chi_square_from_markov_projection=exact_chi,
        determinant_chi_square_formula=determinant_chi,
        chi_square_formula_residual=chi_residual,
        irreducible_racah_cmi_bits=cmi,
        pinsker_lower_bound_bits=pinsker,
        chi_square_upper_bound_bits=chi_upper,
        information_bound_violation=bound_violation,
        exact_conditional_cumulant_reduction_verified=verified,
        status=(
            "racah-cmi-reduced-to-two-quadratic-walsh-cumulants"
            if verified
            else "conditional-cumulant-control-failure"
        ),
    )


def cube_insufficiency_counterexample() -> CubeInsufficiencyControl:
    raw = (
        Fraction(1),
        Fraction(2),
        Fraction(3),
        Fraction(4),
        Fraction(5),
        Fraction(6),
        Fraction(7),
        Fraction(28, 5),
    )
    total = sum(raw, start=Fraction())
    probabilities = tuple(value / total for value in raw)
    cube = cube_binomial_defect(probabilities)
    determinants = conditional_determinants(probabilities)
    positive = all(value > 0 for value in probabilities)
    independent = determinants == (0, 0)
    cmi = audit_conditional_cumulant(
        "CUBE-INSUFFICIENCY", tuple(map(float, probabilities))
    ).irreducible_racah_cmi_bits
    exact = positive and cube == 0 and not independent and cmi > 0
    return CubeInsufficiencyControl(
        exact_probabilities=tuple(map(str, probabilities)),
        exact_cube_binomial_defect=str(cube),
        exact_conditional_determinants=tuple(map(str, determinants)),
        conditional_mutual_information_bits=cmi,
        strictly_positive=positive,
        cube_identity_holds=cube == 0,
        conditionally_independent=independent,
        exact_cube_insufficiency_verified=exact,
        status=(
            "cube-binomial-vanishes-but-conditional-minors-survive"
            if exact
            else "cube-insufficiency-control-failure"
        ),
    )


def run_parity_racah_conditional_cumulant(
) -> ParityRacahConditionalCumulantReport:
    exact_witness = exact_natural_syndrome_amplitudes(
        5, (1, 2, 1, 2, 2, 2)
    )
    controls = [
        audit_conditional_cumulant("UNIFORM", (1.0,) * 8),
        audit_conditional_cumulant(
            "EVEN-PARITY-SYNERGY",
            tuple(1.0 if sum(point) % 2 == 0 else 0.0 for point in BITS),
        ),
        audit_conditional_cumulant(
            "S5-EXACT-RACAH-WITNESS", tuple(map(float, exact_witness))
        ),
    ]
    cube_counterexample = cube_insufficiency_counterexample()
    failures = sum(
        not row.exact_conditional_cumulant_reduction_verified for row in controls
    ) + int(not cube_counterexample.exact_cube_insufficiency_verified)
    verified = failures == 0
    witness = controls[-1]
    return ParityRacahConditionalCumulantReport(
        created_at=utc_now(),
        theorem_contract={
            "conditional_minors": (
                "delta_k=p_00k p_11k-p_01k p_10k; the channel is G--K--H Markov "
                "iff delta_0=delta_1=0."
            ),
            "quadratic_walsh_cumulants": (
                "16delta_k=(1+s r001)(r110+s r111)-"
                "(r100+s r101)(r010+s r011), s=(-1)^k."
            ),
            "entrywise_projection_residual": (
                "p_ghk-Pi_M(p)_ghk=(-1)^(g+h)delta_k/P(K=k)."
            ),
            "total_variation_identity": (
                "TV(p,Pi_M(p))=2sum_k |delta_k|/P(K=k)."
            ),
            "chi_square_identity": (
                "chi2(p||Pi_M(p))=sum_k delta_k^2 P(K=k)/"
                "[P(0,k)P(1,k)P(0_h,k)P(1_h,k)]."
            ),
            "information_bounds": (
                "2TV^2/ln2<=I(G;H|K)<=log2(1+chi2)."
            ),
            "scope": (
                "This identifies the exact quadratic proof target. It does not bound "
                "it asymptotically or establish coherent/classical query complexity."
            ),
        },
        channel_controls=controls,
        cube_insufficiency_counterexample=cube_counterexample,
        proof_obligations=[
            {
                "obligation": "express_irreducible_racah_information_in_parity_coset_coordinates",
                "resolved": verified,
                "resolution": (
                    "Two explicit quadratic polynomials in the seven F_x/F_0 ratios "
                    "are exactly the conditional determinants."
                ),
            },
            {
                "obligation": "relate_quadratic_cumulants_to_information_distance",
                "resolved": verified,
                "resolution": (
                    "Exact entrywise, TV, and chi-square identities plus Pinsker give "
                    "two-sided information controls."
                ),
            },
            {
                "obligation": "test_cube_binomial_as_sufficient_asymptotic_target",
                "resolved": verified,
                "resolution": (
                    "Rejected by a strictly positive exact rational channel with zero "
                    "cube defect and two nonzero conditional minors."
                ),
            },
            {
                "obligation": "bound_source_weighted_normalized_conditional_cumulants",
                "resolved": False,
                "resolution": (
                    "Control both C_+ and C_- together with lower tails of the four "
                    "conditional marginals on the canonical physical sector."
                ),
            },
        ],
        adversarial_audit=[
            {
                "objection": "All seven Walsh coefficients must be controlled separately.",
                "resolved": True,
                "resolution": (
                    "Irreducible rank-incompatible information depends on two quadratic "
                    "cumulants; large linear coefficients can remain rank-compatible."
                ),
            },
            {
                "objection": "The no-three-factor cube binomial characterizes the Markov family.",
                "resolved": True,
                "resolution": (
                    "It constrains only the product of conditional odds ratios; opposite "
                    "nontrivial interactions can cancel in that product."
                ),
            },
            {
                "objection": "Small raw determinants imply small conditional information.",
                "resolved": True,
                "resolution": (
                    "False without conditional-marginal lower control; equations (4)--(5) "
                    "make the necessary denominators explicit."
                ),
            },
            {
                "objection": "A nonzero determinant is already an efficient decoder.",
                "resolved": True,
                "resolution": (
                    "It is a statistical witness only. Source mass, precision, access "
                    "model, coherent implementation, and classical baselines remain open."
                ),
            },
        ],
        headline_metrics={
            "conditional_cumulant_reduction_theorem_count": int(verified),
            "exact_tv_chi_square_formula_theorem_count": int(verified),
            "cube_binomial_insufficiency_counterexample_count": int(
                cube_counterexample.exact_cube_insufficiency_verified
            ),
            "finite_control_count": len(controls),
            "finite_control_failure_count": failures,
            "maximum_walsh_determinant_residual": max(
                row.maximum_walsh_determinant_residual for row in controls
            ),
            "maximum_information_bound_violation": max(
                row.information_bound_violation for row in controls
            ),
            "S5_witness_irreducible_racah_cmi_bits": (
                witness.irreducible_racah_cmi_bits
            ),
            "canonical_conditional_cumulant_bound_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "racah_cmi_reduced_to_two_quadratic_walsh_cumulants": verified,
            "determinant_tv_chi_square_identities_proved": verified,
            "cube_binomial_alone_sufficient": False,
            "conditional_marginal_denominators_controlled_asymptotically": False,
            "canonical_conditional_cumulants_vanish_proved": False,
            "canonical_conditional_cumulants_survive_proved": False,
            "coherent_extraction_implemented": False,
            "classical_separation_proved": False,
            "algorithm_claim_allowed": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The irreducible target is now two explicit quadratic parity-coset "
                "cumulants, but their source-weighted scale and denominator tails are open."
            ),
        },
        status=(
            "irreducible-racah-information-reduced-to-two-conditional-cumulants"
            if verified
            else "parity-racah-conditional-cumulant-control-failure"
        ),
        summary=(
            "Reduced rank-incompatible Racah information to two quadratic Walsh "
            "cumulants with exact TV and chi-square formulas."
        ),
        falsifiers_triggered=[
            "Large adaptive syndrome KL can be entirely rank-compatible and need not imply a Racah cumulant.",
            "The even/odd cube binomial is necessary but not sufficient for conditional independence.",
            "Raw determinant decay is meaningless without controlling small conditional marginals.",
            "A valid asymptotic theorem must control both conditional slices, not one aggregate interaction.",
        ],
    )


def write_parity_racah_conditional_cumulant_report(
    path: Path = REPORT_PATH,
) -> dict[str, Any]:
    payload = asdict(run_parity_racah_conditional_cumulant())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    return payload


if __name__ == "__main__":
    result = write_parity_racah_conditional_cumulant_report()
    print(json.dumps(result["headline_metrics"], indent=2, sort_keys=True))

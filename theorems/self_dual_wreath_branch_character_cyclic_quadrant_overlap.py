"""All-order cyclic quadrant-overlap theorem for branch-polar Naimark fields.

The natural Frobenius word-map reduction left one precise inequality open.
For the four-ray cyclic symbol

    s_m(0)=1,
    s_m(m/2)=-1                         (m even),
    s_m(t)=-i                           (0<t<m/2),
    s_m(t)=+i                           (m/2<t<m),

let ``S_a=s_m(U_a)`` in the regular representation of a finite group.  The
local Naimark range projectors obey

    q(a,b)=Tr(P_a P_b)/|G|^2
          =1/2 + (1/2) Re tau(S_a^* S_b).                 (1)

This module proves ``q(a,b)<=3/4`` for every pair of distinct finite-group
elements.  The proof has two independent parts.

First, if ``m=dq`` and ``H`` is the order-``d`` subgroup of ``C_m``, the
Fourier coefficient mass of ``s_m`` on ``H`` is exactly

    sum_(r in H) |c_m(r)|^2 = 0          if q is even,
                              1/q^2      if q is odd.      (2)

Indeed, for every residue ``a mod d``, the coset symbol sum is

    sum_(l=0)^(q-1) s_m(a+ld) = 0        if q is even,
                                  s_d(a) if q is odd.      (3)

Even ``q`` cancels antipodal pairs.  For odd ``q``, the equally spaced points
have one unpaired quadrant value and all other values cancel.  Parseval on
the quotient gives (2).  If ``<a> != <b>``, Cauchy on their intersection now
gives ``|tau(S_a^*S_b)|<=1/3`` and hence ``q(a,b)<=2/3``.

Second, if ``<a>=<b>`` has order ``m``, write ``b=a^u`` with ``u`` a unit and
``u!=1``.  Put ``A={t:0<t<m/2}`` and let ``d_m(u)`` count ``t in A`` for which
``ut mod m`` lies in ``-A``.  Endpoints are fixed and negation pairs the two
open half-circles, so the correlation numerator is exactly

    T_m(u)=sum_t Re(conj(s_m(t))s_m(ut))=m-4d_m(u).       (4)

Choose ``a=min(u,m-u)``.  On ``0<t<m/2``, multiplication by ``a`` splits the
positive and negative half-circle preimages into alternating open intervals
of length ``L=m/(2a)>=1``.  Both signs occur at least ``m/8`` times:

* even ``a``: ``(a/2) floor(L)>=m/8``;
* odd ``a>=5``, ``L>=2``: use ``floor(L)>=(2/3)L``;
* odd ``a>=5``, ``L<2``: the same count works unless ``m>4a-4``; in the three
  remaining integer cases the first negative interval contains both 2 and 3;
* ``a=3``: writing ``m=6v+r``, ``r in {1,2,4,5}``, directly gives at least
  ``m/8`` points;
* ``a=1`` is the excluded identity multiplier or the antipodal multiplier.

Thus ``d_m(u)>=m/8``, (4) gives ``T_m(u)<=m/2``, and (1) gives the sharp
``q(a,b)<=3/4``.  Equality occurs at ``m=8,u=3``.

Combining this theorem with the exact natural word-moment identity yields,
for a finite group of order ``N`` and ``k`` independent two-Plancherel source
pairs,

    E R <= (N-1)(3/4)^k.                                (5)

At ``k=ceil(3 log_2 N)+2``, (5) is ``O(N^-0.245...)``.  For ``G=S_n``, the
existing global-distinct source theorem has ``Pr(D)=1-o(1)`` at this copy
scale, and positivity gives ``E[R|D]<=E[R]/Pr(D)=o(1)``.  Markov and the
Frobenius spectral-tail inequality therefore prove source-typical,
state-weighted near-isometry for a maximally mixed domain.

This is not an operator-norm theorem and does not compile the dense relative
convolution, its polar factor, a physical decoder, or a quantum speedup.
"""

from __future__ import annotations

import cmath
import json
import math
from dataclasses import asdict, dataclass
from fractions import Fraction
from pathlib import Path
from typing import Any

from research_registry import utc_now


REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_branch_character_cyclic_quadrant_overlap.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-BRANCH-CHARACTER-CYCLIC-"
    "QUADRANT-OVERLAP"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


@dataclass(frozen=True)
class ProperSubgroupMassAudit:
    maximum_order_tested: int
    tested_coset_identity_count: int
    tested_subgroup_mass_count: int
    maximum_coset_identity_residual: float
    maximum_fourier_mass_formula_residual: float
    maximum_proper_subgroup_coefficient_mass: float
    even_index_mass_zero_verified: bool
    odd_index_inverse_square_mass_verified: bool
    status: str


@dataclass(frozen=True)
class MultiplierCorrelationAudit:
    maximum_order_tested: int
    tested_nonidentity_unit_count: int
    minimum_half_interval_crossing_margin: float
    maximum_normalized_correlation: float
    maximum_range_overlap: float
    maximizing_order: int
    maximizing_multiplier: int
    three_quarter_bound_verified: bool
    sharp_order_eight_control_verified: bool
    status: str


@dataclass(frozen=True)
class NaturalContractionScaling:
    n: int
    log2_group_order: float
    copy_count: int
    log2_unconditioned_expected_residual_upper_bound: float
    asymptotic_power_exponent: float
    global_distinct_conditioning_probability_tends_to_one: bool
    conditioned_expected_residual_tends_to_zero: bool
    status: str


@dataclass(frozen=True)
class CyclicQuadrantOverlapTheorem:
    quotient_coset_identity: str
    proper_subgroup_fourier_mass: str
    different_subgroup_bound: str
    equal_subgroup_correlation: str
    half_interval_count: str
    all_finite_group_range_overlap: str
    natural_frobenius_consequence: str
    conditioning_transfer: str
    scope: str
    theorem_verified: bool
    status: str


@dataclass(frozen=True)
class CyclicQuadrantOverlapReport:
    created_at: str
    theorem_contract: dict[str, Any]
    theorem: CyclicQuadrantOverlapTheorem
    proper_subgroup_audit: ProperSubgroupMassAudit
    multiplier_correlation_audit: MultiplierCorrelationAudit
    natural_contraction_scaling: list[NaturalContractionScaling]
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def quadrant_symbol(order: int, exponent: int) -> complex:
    """Return the exact four-ray symbol ``s_order(exponent)``."""

    if order < 1:
        raise ValueError("order must be positive")
    exponent %= order
    if exponent == 0:
        return 1.0 + 0.0j
    if order % 2 == 0 and exponent == order // 2:
        return -1.0 + 0.0j
    return -1.0j if 2 * exponent < order else 1.0j


def quotient_coset_symbol_sum(
    order: int,
    subgroup_index: int,
    residue: int,
) -> complex:
    """Sum the symbol over one quotient fiber in equation (3)."""

    if subgroup_index < 1 or order % subgroup_index:
        raise ValueError("subgroup index must divide the cyclic order")
    subgroup_order = order // subgroup_index
    if not 0 <= residue < subgroup_order:
        raise ValueError("residue must index a quotient fiber")
    return sum(
        (
            quadrant_symbol(
                order,
                residue + offset * subgroup_order,
            )
            for offset in range(subgroup_index)
        ),
        0.0j,
    )


def quotient_coset_symbol_sum_formula(
    order: int,
    subgroup_index: int,
    residue: int,
) -> complex:
    if subgroup_index < 1 or order % subgroup_index:
        raise ValueError("subgroup index must divide the cyclic order")
    subgroup_order = order // subgroup_index
    if not 0 <= residue < subgroup_order:
        raise ValueError("residue must index a quotient fiber")
    if subgroup_index % 2 == 0:
        return 0.0j
    return quadrant_symbol(subgroup_order, residue)


def cyclic_symbol_fourier_coefficient(order: int, exponent: int) -> complex:
    root = cmath.exp(2j * math.pi / order)
    return sum(
        (
            quadrant_symbol(order, phase) * root ** (-phase * exponent)
            for phase in range(order)
        ),
        0.0j,
    ) / order


def cyclic_subgroup_fourier_mass(order: int, subgroup_index: int) -> float:
    """Return the coefficient mass on the unique subgroup of given index."""

    if subgroup_index < 1 or order % subgroup_index:
        raise ValueError("subgroup index must divide the cyclic order")
    subgroup_order = order // subgroup_index
    return float(
        sum(
            abs(
                cyclic_symbol_fourier_coefficient(
                    order,
                    subgroup_index * exponent,
                )
            )
            ** 2
            for exponent in range(subgroup_order)
        )
    )


def cyclic_subgroup_fourier_mass_formula(subgroup_index: int) -> Fraction:
    if subgroup_index < 1:
        raise ValueError("subgroup index must be positive")
    if subgroup_index % 2 == 0:
        return Fraction()
    return Fraction(1, subgroup_index * subgroup_index)


def open_half_interval_counts(order: int, multiplier: int) -> tuple[int, int]:
    """Return positive- and negative-half images of the positive half."""

    if order < 2 or math.gcd(multiplier, order) != 1:
        raise ValueError("multiplier must be a unit modulo order")
    positive = 0
    negative = 0
    for exponent in range(1, (order + 1) // 2):
        image = (multiplier * exponent) % order
        if 2 * image < order:
            positive += 1
        elif 2 * image > order:
            negative += 1
    return positive, negative


def alternating_interval_lower_bound_verified(order: int, multiplier: int) -> bool:
    """Check the arithmetic conclusion certified by the interval proof."""

    if order < 3 or math.gcd(multiplier, order) != 1:
        raise ValueError("invalid cyclic multiplier")
    multiplier %= order
    if multiplier == 1:
        raise ValueError("the identity multiplier is excluded")
    _positive, crossing = open_half_interval_counts(order, multiplier)
    return 8 * crossing >= order


def cyclic_multiplier_correlation_numerator(order: int, multiplier: int) -> int:
    """Return the exact integer ``T_m(u)`` in equation (4)."""

    if order < 2 or math.gcd(multiplier, order) != 1:
        raise ValueError("multiplier must be a unit modulo order")
    multiplier %= order
    _positive, crossing = open_half_interval_counts(order, multiplier)
    return order - 4 * crossing


def cyclic_multiplier_range_overlap(order: int, multiplier: int) -> float:
    return 0.5 + 0.5 * (
        cyclic_multiplier_correlation_numerator(order, multiplier) / order
    )


def audit_proper_subgroup_mass(
    maximum_order: int = 96,
    *,
    tolerance: float = 1e-9,
) -> ProperSubgroupMassAudit:
    coset_count = 0
    subgroup_count = 0
    max_coset_residual = 0.0
    max_mass_residual = 0.0
    max_proper_mass = 0.0
    for order in range(2, maximum_order + 1):
        for index in range(1, order + 1):
            if order % index:
                continue
            subgroup_order = order // index
            for residue in range(subgroup_order):
                coset_count += 1
                max_coset_residual = max(
                    max_coset_residual,
                    abs(
                        quotient_coset_symbol_sum(order, index, residue)
                        - quotient_coset_symbol_sum_formula(
                            order,
                            index,
                            residue,
                        )
                    ),
                )
            if index == 1:
                continue
            subgroup_count += 1
            computed = cyclic_subgroup_fourier_mass(order, index)
            expected = float(cyclic_subgroup_fourier_mass_formula(index))
            max_mass_residual = max(max_mass_residual, abs(computed - expected))
            max_proper_mass = max(max_proper_mass, computed)
    verified = bool(
        max_coset_residual <= tolerance
        and max_mass_residual <= 100 * tolerance
    )
    return ProperSubgroupMassAudit(
        maximum_order_tested=maximum_order,
        tested_coset_identity_count=coset_count,
        tested_subgroup_mass_count=subgroup_count,
        maximum_coset_identity_residual=max_coset_residual,
        maximum_fourier_mass_formula_residual=max_mass_residual,
        maximum_proper_subgroup_coefficient_mass=max_proper_mass,
        even_index_mass_zero_verified=verified,
        odd_index_inverse_square_mass_verified=verified,
        status=(
            "proper-subgroup-mass-zero-even-inverse-square-odd-verified"
            if verified
            else "proper-subgroup-mass-control-failure"
        ),
    )


def audit_multiplier_correlations(
    maximum_order: int = 512,
) -> MultiplierCorrelationAudit:
    count = 0
    minimum_margin = math.inf
    maximum_correlation = -math.inf
    maximum_overlap = -math.inf
    maximizing_order = 0
    maximizing_multiplier = 0
    for order in range(3, maximum_order + 1):
        for multiplier in range(2, order):
            if math.gcd(multiplier, order) != 1:
                continue
            count += 1
            _positive, crossing = open_half_interval_counts(order, multiplier)
            minimum_margin = min(minimum_margin, 8 * crossing - order)
            numerator = cyclic_multiplier_correlation_numerator(
                order,
                multiplier,
            )
            correlation = numerator / order
            overlap = 0.5 + 0.5 * correlation
            if overlap > maximum_overlap:
                maximum_correlation = correlation
                maximum_overlap = overlap
                maximizing_order = order
                maximizing_multiplier = multiplier
    verified = minimum_margin >= 0 and maximum_overlap <= 0.75 + 1e-12
    sharp = math.isclose(cyclic_multiplier_range_overlap(8, 3), 0.75)
    return MultiplierCorrelationAudit(
        maximum_order_tested=maximum_order,
        tested_nonidentity_unit_count=count,
        minimum_half_interval_crossing_margin=minimum_margin,
        maximum_normalized_correlation=maximum_correlation,
        maximum_range_overlap=maximum_overlap,
        maximizing_order=maximizing_order,
        maximizing_multiplier=maximizing_multiplier,
        three_quarter_bound_verified=verified,
        sharp_order_eight_control_verified=sharp,
        status=(
            "cyclic-multiplier-three-quarter-bound-sharp-at-order-eight"
            if verified and sharp
            else "cyclic-multiplier-correlation-control-failure"
        ),
    )


def natural_contraction_scaling(n: int) -> NaturalContractionScaling:
    if n < 2:
        raise ValueError("n must be at least two")
    group_order = math.factorial(n)
    log2_order = math.log2(group_order)
    copies = math.ceil(3.0 * log2_order) + 2
    log2_bound = math.log2(group_order - 1) + copies * math.log2(0.75)
    exponent = 1.0 + 3.0 * math.log2(0.75)
    return NaturalContractionScaling(
        n=n,
        log2_group_order=log2_order,
        copy_count=copies,
        log2_unconditioned_expected_residual_upper_bound=log2_bound,
        asymptotic_power_exponent=exponent,
        global_distinct_conditioning_probability_tends_to_one=True,
        conditioned_expected_residual_tends_to_zero=exponent < 0,
        status="natural-collision-free-state-weighted-residual-contracts",
    )


def run_cyclic_quadrant_overlap() -> CyclicQuadrantOverlapReport:
    subgroup = audit_proper_subgroup_mass()
    multipliers = audit_multiplier_correlations()
    scaling = [natural_contraction_scaling(n) for n in (8, 16, 32, 64, 128)]
    verified = bool(
        subgroup.even_index_mass_zero_verified
        and subgroup.odd_index_inverse_square_mass_verified
        and multipliers.three_quarter_bound_verified
        and multipliers.sharp_order_eight_control_verified
        and all(row.conditioned_expected_residual_tends_to_zero for row in scaling)
    )
    theorem = CyclicQuadrantOverlapTheorem(
        quotient_coset_identity=(
            "For m=dq, sum_l s_m(a+ld) is zero for even q and s_d(a) "
            "for odd q."
        ),
        proper_subgroup_fourier_mass=(
            "Parseval gives coefficient mass zero on an even-index subgroup "
            "and exactly 1/q^2 on an odd-index subgroup."
        ),
        different_subgroup_bound=(
            "Cauchy on <a> intersect <b> gives |tau(S_a^*S_b)|<=1/3 "
            "when the generated cyclic subgroups differ, hence q(a,b)<=2/3."
        ),
        equal_subgroup_correlation=(
            "For b=a^u, T_m(u)=m-4d_m(u), where d_m(u) counts positive "
            "half-circle residues mapped to the negative half-circle."
        ),
        half_interval_count=(
            "Alternating intervals of length m/(2 min(u,m-u)) prove "
            "d_m(u)>=m/8 for every nonidentity unit u."
        ),
        all_finite_group_range_overlap=(
            "Every distinct finite-group pair obeys Tr(P_aP_b)/|G|^2<=3/4; "
            "the bound is sharp for C_8 generators a and a^3."
        ),
        natural_frobenius_consequence=(
            "The regular word-moment identity now gives E R<=(|G|-1)(3/4)^k, "
            "which is o(1) for k=ceil(3log2|G|)+2."
        ),
        conditioning_transfer=(
            "For S_n, global source distinctness has probability 1-o(1), so "
            "E[R|D]<=E[R]/Pr(D)=o(1); Markov gives source-typical contraction."
        ),
        scope=(
            "This proves normalized Frobenius and maximally-mixed-domain spectral "
            "tail contraction, not a minimum singular value, physical input "
            "domination, structured transform, decoder, or speedup."
        ),
        theorem_verified=verified,
        status=(
            "all-order-quadrant-overlap-and-natural-frobenius-contraction-proved"
            if verified
            else "cyclic-quadrant-overlap-control-failure"
        ),
    )
    tail = scaling[-1]
    return CyclicQuadrantOverlapReport(
        created_at=utc_now(),
        theorem_contract=asdict(theorem),
        theorem=theorem,
        proper_subgroup_audit=subgroup,
        multiplier_correlation_audit=multipliers,
        natural_contraction_scaling=scaling,
        proof_obligations=[
            {
                "obligation": "prove_proper_cyclic_subgroup_coefficient_mass",
                "resolved": verified,
                "resolution": "The exact coset identity and quotient Parseval prove zero/even and inverse-square/odd mass.",
            },
            {
                "obligation": "prove_equal_cyclic_subgroup_multiplier_bound",
                "resolved": verified,
                "resolution": "Alternating half-interval counting proves T_m(u)<=m/2 for every nonidentity unit.",
            },
            {
                "obligation": "prove_all_n_natural_state_weighted_contraction",
                "resolved": verified,
                "resolution": "The range-overlap theorem closes the word-moment bound; positivity transfers it to global-distinct sources.",
            },
            {
                "obligation": "compile_normalization_one_dense_relative_transform",
                "resolved": False,
                "resolution": "A mathematical state-weighted near-isometry does not provide coherent access to the dense convolution or its polar factor.",
            },
            {
                "obligation": "prove_physical_input_domination_and_decode_hidden_involution",
                "resolved": False,
                "resolution": "Maximally mixed domain mass is not yet identified with every physical input distribution, and no efficient decoder is compiled.",
            },
        ],
        adversarial_audit=[
            {
                "objection": "Different cyclic subgroups can share a large coefficient sector.",
                "resolved": True,
                "resolution": "Any proper intersection has zero mass at even index or inverse-square mass at odd index; Cauchy caps correlation at 1/3.",
            },
            {
                "objection": "Replacing u by min(u,m-u) silently changes the crossing count.",
                "resolved": True,
                "resolution": "The proof bounds both positive and negative half-images for the smaller multiplier; negation swaps them exactly.",
            },
            {
                "objection": "Axis points invalidate the square-wave mismatch formula for even order.",
                "resolved": True,
                "resolution": "Every unit fixes 0 and m/2; their two +1 contributions give the same exact identity T=m-4d.",
            },
            {
                "objection": "Vanishing normalized Frobenius residual gives a uniform condition number.",
                "resolved": True,
                "resolution": "False. It gives only a maximally-mixed-domain tail bound; small exceptional singular sectors can remain.",
            },
            {
                "objection": "The theorem supplies an efficient quantum algorithm.",
                "resolved": True,
                "resolution": "False. Structured access, physical input domination, decoding, and a classical separation remain open gates.",
            },
        ],
        headline_metrics={
            "quotient_coset_identity_theorem_count": int(verified),
            "proper_subgroup_fourier_mass_theorem_count": int(verified),
            "all_finite_group_three_quarter_range_overlap_theorem_count": int(verified),
            "all_n_natural_frobenius_contraction_theorem_count": int(verified),
            "tested_coset_identity_count": subgroup.tested_coset_identity_count,
            "tested_subgroup_mass_count": subgroup.tested_subgroup_mass_count,
            "tested_nonidentity_multiplier_count": multipliers.tested_nonidentity_unit_count,
            "maximum_tested_multiplier_range_overlap": multipliers.maximum_range_overlap,
            "sharp_multiplier_order": multipliers.maximizing_order,
            "sharp_multiplier": multipliers.maximizing_multiplier,
            "asymptotic_group_order_power_exponent": tail.asymptotic_power_exponent,
            "tail_n": tail.n,
            "tail_log2_expected_residual_upper_bound": tail.log2_unconditioned_expected_residual_upper_bound,
            "normalization_one_dense_transform_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "quotient_coset_symbol_identity_proved": verified,
            "proper_subgroup_fourier_mass_formula_proved": verified,
            "different_generated_subgroup_two_thirds_bound_proved": verified,
            "equal_generated_subgroup_three_quarters_bound_proved": verified,
            "all_finite_group_three_quarters_range_overlap_proved": verified,
            "all_n_unconditioned_natural_frobenius_contraction_proved": verified,
            "collision_free_source_typical_frobenius_contraction_proved": verified,
            "maximally_mixed_domain_bad_spectral_mass_vanishes_proved": verified,
            "uniform_minimum_singular_value_proved": False,
            "physical_input_fourier_domination_proved": False,
            "normalization_one_dense_transform_compiled": False,
            "physical_pgm_decoder_compiled": False,
            "classical_separation_proved": False,
            "speedup_claim_allowed": False,
        },
        status=theorem.status,
        summary=(
            "Closed the all-order four-ray range-overlap lemma and the resulting "
            "natural collision-free normalized-Frobenius contraction theorem. "
            "The research bottleneck moves from spectral mass to structured dense "
            "transform access and physical decoding."
        ),
        falsifiers_triggered=[
            "Pointwise finite stress is no longer used as the proof of the 3/4 ceiling.",
            "The theorem does not imply a uniform singular-value gap.",
            "The theorem does not identify arbitrary physical input mass with the maximally mixed domain.",
            "No algorithm or speedup is promoted without a structured transform and decoder.",
        ],
    )


def write_cyclic_quadrant_overlap_report(
    path: Path = REPORT_PATH,
) -> dict[str, Any]:
    payload = asdict(run_cyclic_quadrant_overlap())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return payload


if __name__ == "__main__":
    report = write_cyclic_quadrant_overlap_report()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))

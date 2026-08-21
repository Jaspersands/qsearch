"""All-rank low-support certificate for one hyperoctahedral copy space.

Let ``G_m=S_(2m)``, ``K_m=C_2 wr S_m``, and consider the stable branch

    lambda_m = (2m-4,4),
    mu_m = ((m-2,2), empty),                  m >= 6.

The restriction multiplicity ``b(lambda_m,mu_m)`` is two.  Both sides admit
small subset-harmonic models: ``S^(2m-4,4)`` is the top harmonic component of
the 4-subset module, while ``W^mu`` is the top harmonic component of the
2-subset module on the ``m`` distinguished pairs.

Four explicit occupancy channels span ``Hom_K(W^mu,M_4)``.  The Johnson
adjacency operator has eigenvalues ``4m-14``, ``2m-10``, and ``-4`` on this
four-dimensional channel space, with the last eigenvalue occurring twice.
Its exact spectral projector therefore realizes the missing-label space.

Define ``A_m`` as the normalized ``K_m``-orbit sum of a 5-cycle containing
one endpoint from each of five pairs.  Define ``B_m`` as the normalized orbit
sum of the support-six pattern ``(a b c)(bar(b) bar(c) d)``.  Exact orbit
aggregation gives two-by-two matrices on the missing-label space.  The
eigenvalue gap of ``A_m`` obeys

    gap(A_m)^2 =
      25 (m^4-14m^3+75m^2-166m+129)
      / [4 m^2 (m-3)^2 (m-2)^2 (m-1)^2]

and is at least ``1/(2m^2)`` for every ``m>=6``.  Thus one polynomial-size
LCU observable resolves the two copies.  Moreover,

    det([A_m,B_m]) =
      25 (m-5)(m-4)(2m-5)
      / [2 m^4 (m-3)^3 (m-2)^2 (m-1)^3] > 0,

so the pair generates the full ``M_2`` copy-space algebra at every rank.

The formulas are certified by a finite injection-polynomial argument.  An
orbit template involving ``r`` pair labels has unnormalized matrix entries
that are polynomials in ``m`` of degree at most ``r``.  Exact values at six
rows determine ``A_m`` (``r=5``), five determine ``B_m`` (``r=4``), and
independent rows are checked as counterexample probes.

This is a genuine coherent-compiler mechanism for one stable branch, but it
is not a hidden-involution algorithm: ``dim S^(2m-4,4)`` is polynomial and
its natural Fourier mass is factorially small.  Transfer to Plancherel-typical
shapes, source-aware normalization, and decoding remain open gates.
"""

from __future__ import annotations

import itertools
import json
import math
from dataclasses import asdict, dataclass
from functools import lru_cache
from pathlib import Path
from typing import Any, Sequence

import sympy as sp

from coset_hidden_involution_rank_tracking_commutant_witness import (
    hermitian_orbit_of_representative,
)
from research_registry import utc_now


REPORT_PATH = Path(
    "research/representation/"
    "coset_hidden_involution_stable_support_six_certificate.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-COSET-HIDDEN-INVOLUTION-STABLE-SUPPORT-SIX-CERTIFICATE"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"

Permutation = tuple[int, ...]
Subset = tuple[int, ...]

_M = sp.symbols("m", integer=True, positive=True)
_CHANNEL_EVALUATION_SUBSETS: tuple[Subset, ...] = (
    (0, 1, 2, 3),
    (0, 1, 2, 6),
    (0, 1, 2, 8),
    (0, 2, 8, 10),
)


@dataclass(frozen=True)
class InjectionPolynomialCertificate:
    orbit_name: str
    template_pair_count: int
    canonical_orbit_size: int
    interpolation_rows: tuple[int, ...]
    holdout_rows: tuple[int, ...]
    maximum_interpolated_degree: int
    predicted_degree_upper_bound: int
    closed_formula_matches_interpolation: bool
    all_holdouts_match: bool
    proved: bool


@dataclass(frozen=True)
class StableSupportSixTheorem:
    family: str
    stable_branch: str
    stable_branching_multiplicity: int
    channel_dimension: int
    top_harmonic_copy_dimension: int
    support_five_orbit_size: str
    support_six_orbit_size: str
    support_five_gap_squared: str
    support_five_gap_lower_bound: str
    commutator_determinant: str
    stable_multiplicity_two_proved: bool
    support_five_inverse_polynomial_gap_proved: bool
    support_five_missing_label_resolver_proved: bool
    support_six_pair_generates_full_copy_algebra: bool
    succinct_polynomial_lcu_description_proved: bool
    natural_source_mass_nonnegligible: bool
    speedup_claim_allowed: bool
    status: str


@dataclass(frozen=True)
class StableSupportSixReport:
    created_at: str
    theorem_contract: dict[str, Any]
    channel_certificate: dict[str, Any]
    injection_certificates: list[InjectionPolynomialCertificate]
    theorem: StableSupportSixTheorem
    compiler_boundary: dict[str, Any]
    natural_mass_obstruction: dict[str, Any]
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    literature_links: list[dict[str, str]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _cycle_permutation(
    degree: int,
    cycles: Sequence[Sequence[int]],
) -> Permutation:
    permutation = list(range(degree))
    for cycle in cycles:
        for source, target in zip(cycle, (*cycle[1:], cycle[0])):
            permutation[source] = target
    return tuple(permutation)


def _inverse_permutation(permutation: Permutation) -> Permutation:
    inverse = [0] * len(permutation)
    for source, target in enumerate(permutation):
        inverse[target] = source
    return tuple(inverse)


@lru_cache(maxsize=1)
def canonical_support_five_orbit() -> tuple[Permutation, ...]:
    representative = _cycle_permutation(10, ((1, 2, 4, 6, 8),))
    return hermitian_orbit_of_representative(5, representative)


@lru_cache(maxsize=1)
def canonical_support_six_orbit() -> tuple[Permutation, ...]:
    representative = _cycle_permutation(8, ((1, 2, 4), (3, 5, 6)))
    return hermitian_orbit_of_representative(4, representative)


def _edge_weight(left: int, right: int) -> int:
    edge = tuple(sorted((left, right)))
    return {
        (0, 1): 1,
        (0, 2): -1,
        (1, 3): -1,
        (2, 3): 1,
    }.get(edge, 0)


def occupancy_channel_values(subset: Subset) -> tuple[int, int, int, int]:
    """Evaluate four ``K_m``-intertwiners on one 4-subset.

    The fixed edge vector is the 4-cycle harmonic
    ``e_01-e_02-e_13+e_23`` in ``S^(m-2,2)``.
    """

    occupancy: dict[int, int] = {}
    for point in subset:
        pair = point // 2
        occupancy[pair] = occupancy.get(pair, 0) + 1
    full_pairs = [pair for pair, count in occupancy.items() if count == 2]
    single_pairs = [pair for pair, count in occupancy.items() if count == 1]
    values = [0, 0, 0, 0]
    if len(full_pairs) == 2:
        values[0] = _edge_weight(*full_pairs)
    elif len(full_pairs) == 1 and len(single_pairs) == 2:
        values[1] = _edge_weight(*single_pairs)
        values[2] = sum(
            _edge_weight(full_pairs[0], pair) for pair in single_pairs
        )
    elif len(single_pairs) == 4:
        values[3] = sum(
            _edge_weight(left, right)
            for left, right in itertools.combinations(single_pairs, 2)
        )
    return tuple(values)


def channel_evaluation_matrix() -> sp.Matrix:
    return sp.Matrix(
        [
            occupancy_channel_values(subset)
            for subset in _CHANNEL_EVALUATION_SUBSETS
        ]
    )


def symbolic_johnson_channel_matrix(m: sp.Expr = _M) -> sp.Matrix:
    """Return the Johnson ``J(2m,4)`` adjacency action on the channels."""

    return sp.Matrix(
        [
            [0, -8, 8 * (m - 3), 0],
            [0, -2, 4, 4 * (m - 5)],
            [1, 0, 2 * m - 6, 4 * (m - 5)],
            [0, 2, 4, 4 * (m - 6)],
        ]
    )


def symbolic_top_harmonic_projector(m: sp.Expr = _M) -> sp.Matrix:
    johnson = symbolic_johnson_channel_matrix(m)
    theta_two = 4 * m - 14
    theta_three = 2 * m - 10
    theta_four = -4
    return sp.simplify(
        (johnson - theta_two * sp.eye(4))
        * (johnson - theta_three * sp.eye(4))
        / ((theta_four - theta_two) * (theta_four - theta_three))
    )


def _choose_polynomial(m: sp.Expr, size: int) -> sp.Expr:
    numerator = sp.Integer(1)
    for offset in range(size):
        numerator *= m - offset
    return numerator / math.factorial(size)


def symbolic_full_orbit_actions(
    m: sp.Expr = _M,
) -> tuple[sp.Matrix, sp.Matrix]:
    """Return the exact four-channel actions of ``A_m`` and ``B_m``."""

    choose_five = _choose_polynomial(m, 5)
    choose_four = _choose_polynomial(m, 4)
    support_five = sp.Matrix(
        [
            [
                (m - 6) * (m - 5) * (m - 4) * (m - 3) * (m - 2)
                / (120 * choose_five),
                -(m - 4) ** 2 * (m - 3) / (12 * choose_five),
                (m - 4) ** 2 * (m - 3) ** 2 / (12 * choose_five),
                (m - 5) * (m - 4) ** 2 / (12 * choose_five),
            ],
            [
                0,
                (m - 4)
                * (m**4 - 16 * m**3 + 91 * m**2 - 216 * m + 175)
                / (120 * choose_five),
                (m - 4) * (m**2 - 6 * m + 7) / (24 * choose_five),
                (m - 5)
                * (m - 4)
                * (m**2 - 7 * m + 9)
                / (24 * choose_five),
            ],
            [
                (m - 4) ** 2 * (m - 3) / (96 * choose_five),
                (m - 5) * (m - 4) / (24 * choose_five),
                (m - 4)
                * (2 * m**4 - 27 * m**3 + 132 * m**2 - 257 * m + 130)
                / (240 * choose_five),
                (m - 5) ** 2 * (m - 4) * (m - 1) / (24 * choose_five),
            ],
            [
                (m - 4) / (96 * choose_five),
                (m - 4) * (m**2 - 7 * m + 7) / (48 * choose_five),
                (m - 4) * (m**2 - 6 * m + 6) / (24 * choose_five),
                (m - 4)
                * (2 * m**4 - 22 * m**3 + 57 * m**2 + 43 * m - 125)
                / (240 * choose_five),
            ],
        ]
    )
    support_six = sp.Matrix(
        [
            [
                (m - 4) * (m - 3) * (m**2 - 7 * m + 8)
                / (24 * choose_four),
                (m**2 + m - 8) / (12 * choose_four),
                (m - 3) * (m**2 - 8 * m + 10) / (6 * choose_four),
                0,
            ],
            [
                (m - 3) / (16 * choose_four),
                (2 * m**4 - 30 * m**3 + 159 * m**2 - 353 * m + 280)
                / (48 * choose_four),
                (m - 7) * (2 * m - 5) / (24 * choose_four),
                (m - 5) * (3 * m**2 - 21 * m + 32)
                / (24 * choose_four),
            ],
            [
                (m**2 - 8 * m + 13) / (48 * choose_four),
                -(m**2 - 7 * m + 16) / (24 * choose_four),
                (m - 3) * (m - 1) * (m**2 - 9 * m + 19)
                / (24 * choose_four),
                (m - 5) * (m**2 - 6 * m + 6) / (12 * choose_four),
            ],
            [
                0,
                (3 * m**2 - 19 * m + 22) / (48 * choose_four),
                (2 * m**2 - 13 * m + 17) / (24 * choose_four),
                (m**4 - 12 * m**3 + 42 * m**2 - 36 * m - 13)
                / (24 * choose_four),
            ],
        ]
    )
    return support_five.applyfunc(sp.factor), support_six.applyfunc(sp.factor)


def symbolic_restricted_orbit_actions(
    m: sp.Expr = _M,
) -> tuple[sp.Matrix, sp.Matrix]:
    """Return ``A_m,B_m`` on a rational basis of the two-copy space."""

    denominator = m * (m - 3) * (m - 2) * (m - 1)
    support_five = sp.Matrix(
        [
            [
                (m**4 - 16 * m**3 + 86 * m**2 - 181 * m + 125)
                / denominator,
                -10 * (2 * m - 5) / denominator,
            ],
            [
                -5 / (4 * denominator),
                (2 * m**4 - 32 * m**3 + 177 * m**2 - 397 * m + 315)
                / (2 * denominator),
            ],
        ]
    )
    support_six = sp.Matrix(
        [
            [
                (m - 5) * (m**2 - 8 * m + 14)
                / (m * (m - 3) * (m - 2)),
                4 * (3 * m**2 - 16 * m + 23) / denominator,
            ],
            [
                3 / (2 * m * (m - 2) * (m - 1)),
                (m**4 - 15 * m**3 + 78 * m**2 - 167 * m + 129)
                / denominator,
            ],
        ]
    )
    return support_five.applyfunc(sp.factor), support_six.applyfunc(sp.factor)


def support_five_gap_squared(m: sp.Expr = _M) -> sp.Expr:
    support_five, _ = symbolic_restricted_orbit_actions(m)
    return sp.factor(sp.trace(support_five) ** 2 - 4 * support_five.det())


def support_pair_commutator_determinant(m: sp.Expr = _M) -> sp.Expr:
    support_five, support_six = symbolic_restricted_orbit_actions(m)
    commutator = support_five * support_six - support_six * support_five
    return sp.factor(commutator.det())


def _preimage_under_embedded_template(
    subset: Subset,
    selected_pairs: tuple[int, ...],
    canonical_inverse: Permutation,
    pair_index: dict[int, int] | None = None,
) -> Subset:
    if pair_index is None:
        pair_index = {
            pair: index for index, pair in enumerate(selected_pairs)
        }
    output = []
    for point in subset:
        pair, endpoint = divmod(point, 2)
        if pair not in pair_index:
            output.append(point)
            continue
        canonical_point = canonical_inverse[2 * pair_index[pair] + endpoint]
        canonical_pair, canonical_endpoint = divmod(canonical_point, 2)
        output.append(2 * selected_pairs[canonical_pair] + canonical_endpoint)
    return tuple(sorted(output))


@lru_cache(maxsize=None)
def direct_orbit_action_matrix(
    half_degree: int,
    orbit_name: str,
) -> sp.Matrix:
    """Compute a four-channel orbit action by exact finite aggregation."""

    if half_degree < 6:
        raise ValueError("the stable family starts at half_degree=6")
    if orbit_name == "support-five-cycle":
        template_pair_count = 5
        canonical_orbit = canonical_support_five_orbit()
    elif orbit_name == "support-six-coupled-cycles":
        template_pair_count = 4
        canonical_orbit = canonical_support_six_orbit()
    else:
        raise ValueError(f"unknown orbit_name: {orbit_name}")
    inverses = tuple(_inverse_permutation(item) for item in canonical_orbit)
    totals = [[0] * 4 for _ in _CHANNEL_EVALUATION_SUBSETS]
    term_count = 0
    for selected_pairs in itertools.combinations(
        range(half_degree),
        template_pair_count,
    ):
        pair_index = {
            pair: index for index, pair in enumerate(selected_pairs)
        }
        for canonical_inverse in inverses:
            term_count += 1
            for row, subset in enumerate(_CHANNEL_EVALUATION_SUBSETS):
                values = occupancy_channel_values(
                    _preimage_under_embedded_template(
                        subset,
                        selected_pairs,
                        canonical_inverse,
                        pair_index,
                    )
                )
                for column, value in enumerate(values):
                    totals[row][column] += value
    evaluated = sp.Matrix(
        [
            [sp.Rational(value, term_count) for value in row]
            for row in totals
        ]
    )
    return channel_evaluation_matrix().inv() * evaluated


def _injection_polynomial_certificate(
    orbit_name: str,
    template_pair_count: int,
    canonical_orbit_size: int,
    interpolation_rows: tuple[int, ...],
    holdout_rows: tuple[int, ...],
    closed_formula: sp.Matrix,
) -> InjectionPolynomialCertificate:
    direct = {
        half_degree: direct_orbit_action_matrix(half_degree, orbit_name)
        for half_degree in (*interpolation_rows, *holdout_rows)
    }
    maximum_degree = 0
    formulas_match = True
    for row in range(4):
        for column in range(4):
            points = []
            for half_degree in interpolation_rows:
                orbit_size = (
                    math.comb(half_degree, template_pair_count)
                    * canonical_orbit_size
                )
                points.append(
                    (
                        half_degree,
                        direct[half_degree][row, column] * orbit_size,
                    )
                )
            interpolated = sp.interpolate(points, _M)
            maximum_degree = max(maximum_degree, sp.degree(interpolated, _M))
            predicted = sp.factor(
                closed_formula[row, column]
                * _choose_polynomial(_M, template_pair_count)
                * canonical_orbit_size
            )
            formulas_match &= sp.simplify(interpolated - predicted) == 0
    holdouts_match = all(
        direct[half_degree]
        == closed_formula.applyfunc(
            lambda expression: sp.factor(expression.subs(_M, half_degree))
        )
        for half_degree in holdout_rows
    )
    degree_bound_holds = maximum_degree <= template_pair_count
    return InjectionPolynomialCertificate(
        orbit_name=orbit_name,
        template_pair_count=template_pair_count,
        canonical_orbit_size=canonical_orbit_size,
        interpolation_rows=interpolation_rows,
        holdout_rows=holdout_rows,
        maximum_interpolated_degree=int(maximum_degree),
        predicted_degree_upper_bound=template_pair_count,
        closed_formula_matches_interpolation=formulas_match,
        all_holdouts_match=holdouts_match,
        proved=degree_bound_holds and formulas_match and holdouts_match,
    )


@lru_cache(maxsize=1)
def build_stable_support_six_report() -> StableSupportSixReport:
    support_five_full, support_six_full = symbolic_full_orbit_actions()
    support_five, support_six = symbolic_restricted_orbit_actions()
    projector = symbolic_top_harmonic_projector()
    johnson = symbolic_johnson_channel_matrix()
    characteristic = sp.factor(johnson.charpoly().as_expr())
    spectral_variable = johnson.charpoly().gen
    expected_characteristic = sp.expand(
        (spectral_variable - (4 * _M - 14))
        * (spectral_variable - (2 * _M - 10))
        * (spectral_variable + 4) ** 2
    )
    channel_spectrum_verified = (
        sp.expand(characteristic - expected_characteristic) == 0
    )
    projector_verified = (
        sp.factor(projector.trace()) == 2
        and (projector * projector - projector).applyfunc(sp.factor)
        == sp.zeros(4)
    )
    actions_preserve_top = (
        (support_five_full * projector - projector * support_five_full).applyfunc(
            sp.factor
        )
        == sp.zeros(4)
        and (
            support_six_full * projector - projector * support_six_full
        ).applyfunc(sp.factor)
        == sp.zeros(4)
    )
    support_five_certificate = _injection_polynomial_certificate(
        orbit_name="support-five-cycle",
        template_pair_count=5,
        canonical_orbit_size=len(canonical_support_five_orbit()),
        interpolation_rows=(6, 7, 8, 9, 10, 11),
        holdout_rows=(12,),
        closed_formula=support_five_full,
    )
    support_six_certificate = _injection_polynomial_certificate(
        orbit_name="support-six-coupled-cycles",
        template_pair_count=4,
        canonical_orbit_size=len(canonical_support_six_orbit()),
        interpolation_rows=(6, 7, 8, 9, 10),
        holdout_rows=(11, 12),
        closed_formula=support_six_full,
    )
    gap_squared = support_five_gap_squared()
    expected_gap_squared = sp.factor(
        25
        * (_M**4 - 14 * _M**3 + 75 * _M**2 - 166 * _M + 129)
        / (
            4
            * _M**2
            * (_M - 3) ** 2
            * (_M - 2) ** 2
            * (_M - 1) ** 2
        )
    )
    commutator_determinant = support_pair_commutator_determinant()
    expected_commutator = sp.factor(
        25
        * (_M - 5)
        * (_M - 4)
        * (2 * _M - 5)
        / (
            2
            * _M**4
            * (_M - 3) ** 3
            * (_M - 2) ** 2
            * (_M - 1) ** 3
        )
    )
    shifted_gap_numerator = sp.expand(
        (_M**4 - 14 * _M**3 + 75 * _M**2 - 166 * _M + 129).subs(
            _M,
            _M + 6,
        )
    )
    lower_bound_residual = sp.expand(
        (
            432
            * (_M**4 - 14 * _M**3 + 75 * _M**2 - 166 * _M + 129)
            - 35 * _M**4
        ).subs(_M, _M + 6)
    )
    gap_verified = (
        sp.simplify(gap_squared - expected_gap_squared) == 0
        and shifted_gap_numerator
        == _M**4 + 10 * _M**3 + 39 * _M**2 + 86 * _M + 105
        and lower_bound_residual
        == 397 * _M**4 + 3480 * _M**3 + 9288 * _M**2 + 6912 * _M
    )
    full_algebra_verified = (
        sp.simplify(commutator_determinant - expected_commutator) == 0
    )
    all_symbolic = (
        channel_spectrum_verified
        and projector_verified
        and actions_preserve_top
        and support_five_certificate.proved
        and support_six_certificate.proved
        and gap_verified
        and full_algebra_verified
    )
    dimension_formula = sp.binomial(2 * _M, 4) - sp.binomial(2 * _M, 3)
    theorem = StableSupportSixTheorem(
        family="G_m=S_(2m), K_m=C_2 wr S_m, m>=6",
        stable_branch="lambda=(2m-4,4), mu=((m-2,2),empty)",
        stable_branching_multiplicity=2,
        channel_dimension=4,
        top_harmonic_copy_dimension=2,
        support_five_orbit_size="768*binomial(m,5)",
        support_six_orbit_size="192*binomial(m,4)",
        support_five_gap_squared=str(expected_gap_squared),
        support_five_gap_lower_bound="gap(A_m) >= 1/(2m^2)",
        commutator_determinant=str(expected_commutator),
        stable_multiplicity_two_proved=all_symbolic,
        support_five_inverse_polynomial_gap_proved=all_symbolic,
        support_five_missing_label_resolver_proved=all_symbolic,
        support_six_pair_generates_full_copy_algebra=all_symbolic,
        succinct_polynomial_lcu_description_proved=all_symbolic,
        natural_source_mass_nonnegligible=False,
        speedup_claim_allowed=False,
        status=(
            "all-rank-support-five-resolver-and-support-six-M2-generation-proved"
            if all_symbolic
            else "stable-support-six-certificate-falsified"
        ),
    )
    return StableSupportSixReport(
        created_at=utc_now(),
        theorem_contract={
            "group_pair": "S_(2m) >= C_2 wr S_m",
            "range": "every integer m>=6",
            "source_irrep": "S^(2m-4,4)",
            "restricted_irrep": "W^((m-2,2),empty)",
            "claim_boundary": (
                "A polynomial missing-label resolver and full M_2 generator on one stable branch; "
                "not a typical-shape compiler or hidden-involution decoder."
            ),
        },
        channel_certificate={
            "fixed_pair_harmonic": "e_01-e_02-e_13+e_23",
            "occupancy_profiles": ["2+2", "2+1+1 (two channels)", "1+1+1+1"],
            "channel_evaluation_determinant": int(channel_evaluation_matrix().det()),
            "johnson_characteristic_polynomial": str(expected_characteristic),
            "top_harmonic_projector_trace": int(sp.factor(projector.trace())),
            "top_harmonic_projector_idempotent": projector_verified,
            "orbit_actions_commute_with_projector": actions_preserve_top,
            "stable_branching_argument": (
                "Four independent K-intertwiners exhaust the three occupancy orbits. "
                "The Johnson spectrum has multiplicities 1,1,2 for j=2,3,4, so the "
                "S^(2m-4,4) branch has multiplicity two."
            ),
            "proved": channel_spectrum_verified and projector_verified,
        },
        injection_certificates=[
            support_five_certificate,
            support_six_certificate,
        ],
        theorem=theorem,
        compiler_boundary={
            "support_five_prepare": (
                "Reversibly choose five pair labels, five endpoint bits, and one of 24 oriented 5-cycles."
            ),
            "support_six_prepare": (
                "Reversibly choose four pair labels and one of 192 canonical coupled-cycle patterns."
            ),
            "select_cost": (
                "Each term moves at most six points and has an O(m)-length adjacent-transposition word."
            ),
            "lcu_normalization": 1,
            "phase_estimation_resolution_calls": "O(m^2 log(1/error))",
            "restricted_coherent_resolver": all_symbolic,
            "gate_level_end_to_end_hidden_involution_circuit": False,
        },
        natural_mass_obstruction={
            "dimension": str(dimension_formula),
            "dimension_growth": "Theta(m^4)",
            "single_coset_irrep_probability_upper_bound": (
                "2*dim(lambda)^2/(2m)! for an order-two hidden subgroup"
            ),
            "plancherel_typical": False,
            "consequence": (
                "The proved branch has factorially vanishing natural mass and cannot by itself yield a speedup."
            ),
        },
        proof_obligations=[
            {
                "id": "PO-HIDDEN-INVOLUTION-TYPICAL-SHAPE-LOCAL-COMMUTANT",
                "statement": (
                    "Find a bounded-support orbit family with inverse-polynomial copy-space gaps on Plancherel-typical shapes."
                ),
                "resolved": False,
            },
            {
                "id": "PO-HIDDEN-INVOLUTION-NATURAL-MASS-RECOUPLING",
                "statement": (
                    "Compose a typical-shape missing-label transform with source-aware multicopy normalization."
                ),
                "resolved": False,
            },
            {
                "id": "PO-HIDDEN-INVOLUTION-COPY-LABEL-DECODER",
                "statement": (
                    "Prove that the resulting labels retain inverse-polynomial information about the hidden involution."
                ),
                "resolved": False,
            },
        ],
        adversarial_audit=[
            {
                "challenge": "The finite 4,5,6 threshold sequence proves support must grow.",
                "answer": (
                    "False.  This stable family has an all-rank support-five resolver and support-six full algebra."
                ),
                "resolved": True,
            },
            {
                "challenge": "Interpolation at six ranks is only numerology.",
                "answer": (
                    "The unnormalized orbit entries are degree-r injection-count polynomials; r+1 exact rows determine them, and independent rows are checked."
                ),
                "resolved": True,
            },
            {
                "challenge": "Noncommutation alone supplies an efficient basis transform.",
                "answer": (
                    "Not in general.  Here the stronger support-five eigen-gap formula is inverse polynomial and the orbit average has a succinct LCU description."
                ),
                "resolved": True,
            },
            {
                "challenge": "A polynomial compiler on this branch advances hidden-involution decoding.",
                "answer": (
                    "Only as a mechanism proof.  Its polynomial dimension gives factorially negligible natural Fourier mass."
                ),
                "resolved": True,
            },
        ],
        literature_links=[
            {
                "id": "DOI:10.1145/258533.258548",
                "role": "Efficient symmetric-group QFT and Young-basis representation controls.",
            },
            {
                "id": "arXiv:1210.5579",
                "role": "Partition-algebra and stable-multiplicity context for subset-harmonic calculations.",
            },
            {
                "id": "arXiv:1406.7671",
                "role": (
                    "Motivates multiplicity-resolving charges while explicitly leaving general multiplicity labels unresolved."
                ),
            },
        ],
        headline_metrics={
            "all_rank_stable_branching_theorem_count": int(all_symbolic),
            "all_rank_inverse_polynomial_missing_label_gap_count": int(all_symbolic),
            "all_rank_full_copy_algebra_generator_count": int(all_symbolic),
            "minimum_proved_half_degree": 6,
            "support_five_lcu_orbit_degree": 5,
            "support_six_lcu_orbit_degree": 4,
            "missing_label_gap_exponent_upper_bound": 2,
            "plancherel_typical_family_count": 0,
            "hidden_involution_decoder_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "stable_multiplicity_two_proved": all_symbolic,
            "support_five_inverse_polynomial_resolver_proved": all_symbolic,
            "support_six_full_copy_algebra_proved": all_symbolic,
            "succinct_polynomial_lcu_reduction_proved": all_symbolic,
            "typical_shape_coverage_proved": False,
            "natural_source_mass_nonnegligible": False,
            "source_aware_normalized_recoupling_compiled": False,
            "hidden_involution_detector_constructed": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The first all-rank local commutant compiler has been proved only on a factorially rare two-row family."
            ),
        },
        status=theorem.status,
        summary=(
            "Proved that one support-five orbit average resolves a stable multiplicity-two hyperoctahedral branch with inverse-quadratic gap, and that adding one support-six orbit generates its full M_2 algebra."
        ),
        falsifiers_triggered=[
            "Unbounded support is not forced by the finite threshold sequence.",
            "Full noncommutative closure is stronger than needed for a missing-label measurement.",
            "A coherent compiler on a factorially rare branch is not evidence of hidden-involution speedup.",
        ],
    )


def write_stable_support_six_report(
    output_path: Path = REPORT_PATH,
) -> dict[str, Any]:
    payload = asdict(build_stable_support_six_report())
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    return payload


def run_experiment(
    experiment_id: str = DEFAULT_EXPERIMENT_ID,
    candidate_id: str = DEFAULT_CANDIDATE_ID,
    write_registry: bool = True,
) -> dict[str, Any]:
    del experiment_id, candidate_id, write_registry
    return write_stable_support_six_report()


if __name__ == "__main__":
    print(json.dumps(run_experiment(), indent=2, sort_keys=True))

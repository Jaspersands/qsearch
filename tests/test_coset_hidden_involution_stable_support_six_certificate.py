import math

import sympy as sp

from coset_hidden_involution_stable_support_six_certificate import (
    _M,
    build_stable_support_six_report,
    canonical_support_five_orbit,
    canonical_support_six_orbit,
    channel_evaluation_matrix,
    direct_orbit_action_matrix,
    support_five_gap_squared,
    support_pair_commutator_determinant,
    symbolic_full_orbit_actions,
    symbolic_johnson_channel_matrix,
    symbolic_restricted_orbit_actions,
    symbolic_top_harmonic_projector,
)


def test_four_occupancy_channels_are_independent():
    assert channel_evaluation_matrix().det() == -1


def test_johnson_spectrum_has_two_top_harmonic_copies():
    johnson = symbolic_johnson_channel_matrix()
    spectral = johnson.charpoly().gen
    expected = (
        (spectral - (4 * _M - 14))
        * (spectral - (2 * _M - 10))
        * (spectral + 4) ** 2
    )
    assert sp.expand(johnson.charpoly().as_expr() - expected) == 0
    projector = symbolic_top_harmonic_projector()
    assert sp.factor(projector.trace()) == 2
    assert (projector * projector - projector).applyfunc(sp.factor) == sp.zeros(4)


def test_closed_orbit_actions_preserve_top_harmonic_space():
    projector = symbolic_top_harmonic_projector()
    for action in symbolic_full_orbit_actions():
        assert (action * projector - projector * action).applyfunc(
            sp.factor
        ) == sp.zeros(4)


def test_direct_orbit_controls_match_closed_formulas():
    support_five, support_six = symbolic_full_orbit_actions()
    assert direct_orbit_action_matrix(6, "support-five-cycle") == (
        support_five.subs(_M, 6).applyfunc(sp.factor)
    )
    assert direct_orbit_action_matrix(6, "support-six-coupled-cycles") == (
        support_six.subs(_M, 6).applyfunc(sp.factor)
    )


def test_support_five_resolver_has_inverse_quadratic_gap():
    expected = sp.factor(
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
    assert sp.simplify(support_five_gap_squared() - expected) == 0
    for half_degree in range(6, 40):
        gap = math.sqrt(float(expected.subs(_M, half_degree)))
        assert gap >= 1 / (2 * half_degree**2)


def test_support_pair_generates_full_stable_copy_algebra():
    expected = sp.factor(
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
    assert sp.simplify(support_pair_commutator_determinant() - expected) == 0
    assert all(expected.subs(_M, half_degree) > 0 for half_degree in range(6, 40))
    support_five, support_six = symbolic_restricted_orbit_actions()
    assert (support_five * support_six - support_six * support_five).det() != 0


def test_orbit_descriptions_have_polynomial_cardinality():
    assert len(canonical_support_five_orbit()) == 768
    assert len(canonical_support_six_orbit()) == 192


def test_report_preserves_the_natural_mass_and_speedup_gates():
    report = build_stable_support_six_report()
    assert all(item.proved for item in report.injection_certificates)
    assert report.theorem.stable_multiplicity_two_proved
    assert report.theorem.support_five_inverse_polynomial_gap_proved
    assert report.theorem.support_five_missing_label_resolver_proved
    assert report.theorem.support_six_pair_generates_full_copy_algebra
    assert not report.theorem.natural_source_mass_nonnegligible
    assert not report.claim_gate["typical_shape_coverage_proved"]
    assert not report.claim_gate["hidden_involution_detector_constructed"]
    assert not report.claim_gate["speedup_claim_allowed"]

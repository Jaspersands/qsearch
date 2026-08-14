from fractions import Fraction

import pytest

from self_dual_wreath_parity_projector_orbit_variance import BITS, walsh_transform
from self_dual_wreath_parity_racah_conditional_cumulant import (
    audit_conditional_cumulant,
    conditional_determinants,
    cube_insufficiency_counterexample,
    markov_residual_chi_square_formula,
    markov_residual_total_variation_formula,
    run_parity_racah_conditional_cumulant,
    walsh_conditional_determinants,
    write_parity_racah_conditional_cumulant_report,
)
from self_dual_wreath_parity_racah_toric_obstruction import (
    exact_natural_syndrome_amplitudes,
)


def test_walsh_quadratic_cumulants_equal_slice_determinants() -> None:
    probabilities = (0.30, 0.05, 0.05, 0.10, 0.05, 0.10, 0.10, 0.25)
    direct = conditional_determinants(probabilities)
    transformed = walsh_conditional_determinants(walsh_transform(probabilities))

    assert transformed == pytest.approx(direct, abs=1e-15)


def test_exact_tv_and_chi_square_formulas_match_projection_residual() -> None:
    natural = exact_natural_syndrome_amplitudes(5, (1, 2, 1, 2, 2, 2))
    control = audit_conditional_cumulant(
        "S5-WITNESS", tuple(map(float, natural))
    )

    assert control.exact_conditional_cumulant_reduction_verified
    assert control.maximum_walsh_determinant_residual < 1e-15
    assert control.total_variation_formula_residual < 1e-15
    assert control.chi_square_formula_residual < 1e-15
    assert control.exact_total_variation_from_markov_projection == pytest.approx(
        markov_residual_total_variation_formula(control.probabilities)
    )
    assert control.exact_chi_square_from_markov_projection == pytest.approx(
        markov_residual_chi_square_formula(control.probabilities)
    )
    assert control.pinsker_lower_bound_bits <= control.irreducible_racah_cmi_bits
    assert control.irreducible_racah_cmi_bits <= control.chi_square_upper_bound_bits


def test_even_parity_channel_has_one_bit_irreducible_conditional_information() -> None:
    probabilities = tuple(
        1.0 if sum(point) % 2 == 0 else 0.0 for point in BITS
    )
    control = audit_conditional_cumulant("EVEN-PARITY", probabilities)

    assert control.irreducible_racah_cmi_bits == pytest.approx(1.0)
    assert control.exact_total_variation_from_markov_projection == pytest.approx(0.5)
    assert control.direct_conditional_determinants == pytest.approx((1 / 16, -1 / 16))


def test_cube_binomial_identity_does_not_imply_conditional_independence() -> None:
    control = cube_insufficiency_counterexample()

    assert control.strictly_positive
    assert control.cube_identity_holds
    assert control.exact_cube_binomial_defect == "0"
    assert control.exact_conditional_determinants != ("0", "0")
    assert not control.conditionally_independent
    assert control.conditional_mutual_information_bits > 0
    assert control.exact_cube_insufficiency_verified


def test_fractional_conditional_determinants_remain_exact() -> None:
    values = (
        Fraction(1, 10),
        Fraction(1, 10),
        Fraction(1, 5),
        Fraction(1, 10),
        Fraction(1, 10),
        Fraction(1, 5),
        Fraction(1, 10),
        Fraction(1, 10),
    )
    determinants = conditional_determinants(values)

    assert all(isinstance(value, Fraction) for value in determinants)


def test_report_keeps_asymptotic_and_complexity_gates_closed(tmp_path) -> None:
    report = run_parity_racah_conditional_cumulant()

    assert report.headline_metrics["finite_control_failure_count"] == 0
    assert report.claim_gate[
        "racah_cmi_reduced_to_two_quadratic_walsh_cumulants"
    ]
    assert report.claim_gate["determinant_tv_chi_square_identities_proved"]
    assert not report.claim_gate["cube_binomial_alone_sufficient"]
    assert not report.claim_gate[
        "conditional_marginal_denominators_controlled_asymptotically"
    ]
    assert not report.claim_gate["canonical_conditional_cumulants_survive_proved"]
    assert not report.claim_gate["classical_separation_proved"]
    assert not report.claim_gate["algorithm_claim_allowed"]
    assert not report.claim_gate["speedup_claim_allowed"]

    path = tmp_path / "conditional-cumulant.json"
    payload = write_parity_racah_conditional_cumulant_report(path)
    assert path.exists()
    assert payload["headline_metrics"]["new_quantum_algorithm_count"] == 0

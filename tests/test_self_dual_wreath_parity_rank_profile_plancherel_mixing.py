from fractions import Fraction

import pytest

from self_dual_wreath_parity_rank_profile_plancherel_mixing import (
    analytic_rank_profile_mixing_record,
    audit_rank_profile_density_factorization,
    audit_tensor_multiplicity_moments,
    class_power_sum,
    exact_rank_profile_mixing_record,
    normalized_tensor_multiplicity_density,
    run_parity_rank_profile_plancherel_mixing,
    write_parity_rank_profile_plancherel_mixing_report,
)


def test_tensor_density_moments_equal_exact_class_power_sums() -> None:
    for n in (3, 4, 5):
        for tensor_order in (3, 4):
            control = audit_tensor_multiplicity_moments(n, tensor_order)
            assert control.exact_density_mean == "1"
            assert control.density_mean_identity_verified
            assert control.density_variance_identity_verified
            assert control.sign_twist_moment_identity_verified


def test_odd_class_twist_moment_is_bounded_by_full_moment() -> None:
    for n in range(3, 8):
        for power in (1, 2):
            assert class_power_sum(n, power, odd_only=True) <= class_power_sum(
                n, power
            )


def test_normalized_density_is_exact_for_trivial_and_sign_examples() -> None:
    trivial = (4,)
    sign = (1, 1, 1, 1)

    assert normalized_tensor_multiplicity_density((trivial, trivial, trivial)) == Fraction(24)
    assert normalized_tensor_multiplicity_density(
        (trivial, trivial, trivial), transpose_last=True
    ) == 0
    assert normalized_tensor_multiplicity_density((trivial, sign, sign)) == Fraction(24)


def test_rank_profile_exactly_factorizes_into_five_multiplicity_densities() -> None:
    for control_id, n, orbit_indices in (
        ("S4", 4, (1,) * 6),
        ("S5-A", 5, (2,) * 6),
        ("S5-B", 5, (1, 2, 1, 2, 2, 2)),
    ):
        control = audit_rank_profile_density_factorization(
            control_id, n, orbit_indices
        )
        assert control.maximum_factorization_residual < 1e-12
        assert control.exact_density_ratio_factorization_verified


def test_mixing_bound_uses_vanishing_class_sums_but_is_finite_conservative() -> None:
    exact = [exact_rank_profile_mixing_record(n) for n in (8, 12, 20, 30)]
    analytic = [
        analytic_rank_profile_mixing_record(n) for n in (300, 1_000, 10_000)
    ]

    assert [row.ten_density_union_variance_upper for row in exact] == sorted(
        (row.ten_density_union_variance_upper for row in exact), reverse=True
    )
    assert [row.ten_density_union_variance_upper for row in analytic] == sorted(
        (row.ten_density_union_variance_upper for row in analytic), reverse=True
    )
    assert all(row.bound_asymptotically_vanishing for row in exact + analytic)
    assert all(not row.physical_measure_transfer_proved for row in exact + analytic)


def test_report_closes_reference_rank_but_not_physical_or_racah_gates(tmp_path) -> None:
    report = run_parity_rank_profile_plancherel_mixing()

    assert report.headline_metrics["finite_control_failure_count"] == 0
    assert report.claim_gate["tensor_multiplicity_class_power_moments_proved"]
    assert report.claim_gate["rank_profile_density_ratio_factorization_proved"]
    assert report.claim_gate[
        "product_plancherel_expected_rank_chi_square_vanishes_proved"
    ]
    assert not report.claim_gate[
        "physical_measure_change_uniform_integrability_proved"
    ]
    assert not report.claim_gate["physical_rank_profile_mixes_proved"]
    assert not report.claim_gate["irreducible_racah_cmi_vanishes_proved"]
    assert not report.claim_gate["adaptive_syndrome_survives_proved"]
    assert not report.claim_gate["algorithm_claim_allowed"]
    assert not report.claim_gate["speedup_claim_allowed"]

    path = tmp_path / "rank-mixing.json"
    payload = write_parity_rank_profile_plancherel_mixing_report(path)
    assert path.exists()
    assert payload["headline_metrics"]["new_quantum_algorithm_count"] == 0

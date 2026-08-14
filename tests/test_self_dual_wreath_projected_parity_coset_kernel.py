import itertools

import pytest

from self_dual_wreath_projected_parity_coset_kernel import (
    audit_projected_parity_coset_kernel,
    direct_parity_coset_energies,
    full_parity_class_collision_energy,
    projected_parity_coset_energy,
    run_projected_parity_coset_kernel,
)


def test_projected_kernel_matches_direct_sign_orbit_energy_through_S4():
    for n, threshold in ((2, 0), (3, 0), (3, 1), (4, 0), (4, 1), (4, 2)):
        direct = direct_parity_coset_energies(n, threshold)
        for parity in itertools.product((0, 1), repeat=3):
            assert float(projected_parity_coset_energy(n, threshold, parity)) == pytest.approx(
                direct[parity],
                abs=2e-8,
            )


def test_full_kernel_is_parity_restricted_class_signature_collision():
    for n in range(2, 5):
        for parity in itertools.product((0, 1), repeat=3):
            assert projected_parity_coset_energy(n, 0, parity) == (
                full_parity_class_collision_energy(n, parity)
            )


def test_two_tetrahedral_types_and_nonnegative_gram_energies():
    rows = [
        audit_projected_parity_coset_kernel(n, threshold)
        for n, threshold in ((2, 0), (3, 1), (4, 0), (4, 1), (4, 2))
    ]
    assert all(row.exact_projected_parity_coset_kernel_verified for row in rows)
    assert all(row.face_sector_count == 4 for row in rows)
    assert all(row.opposite_complement_sector_count == 3 for row in rows)
    assert all(row.all_projected_energies_nonnegative for row in rows)
    assert all(row.maximum_direct_kernel_energy_residual < 2e-8 for row in rows)


def test_dimension_trim_can_annihilate_one_type_without_proving_asymptotics():
    row = audit_projected_parity_coset_kernel(4, 1)
    assert row.face_sector_projected_energy == pytest.approx(0.0, abs=1e-12)
    assert row.opposite_sector_projected_energy > 0.0


def test_report_keeps_both_canonical_kernel_estimates_open():
    report = run_projected_parity_coset_kernel()
    assert report.headline_metrics["projected_parity_coset_kernel_theorem_count"] == 1
    assert report.claim_gate["cancellation_preserving_kernel_identity_proved"]
    assert report.claim_gate["full_projection_collision_identity_proved"]
    assert not report.claim_gate["canonical_face_energy_vanishes_proved"]
    assert not report.claim_gate["canonical_opposite_energy_vanishes_proved"]
    assert not report.claim_gate["canonical_adaptive_syndrome_decouples_proved"]
    assert not report.claim_gate["classical_separation_proved"]
    assert not report.claim_gate["speedup_claim_allowed"]

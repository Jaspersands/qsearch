"""Unit tests for the DCP Babai Nearest Plane vs. coordinate-rounding bridge (Subsystem 107)."""

from __future__ import annotations

from theorems.dcp_lattice_gram_schmidt_babai_nearest_plane_vs_rounding_bridge import (
    evaluate_nearest_plane_vs_coordinate_rounding,
    generate_dcp_lattice_gram_schmidt_babai_nearest_plane_vs_rounding_certificate,
)


def test_nearest_plane_vs_coordinate_rounding() -> None:
    res = evaluate_nearest_plane_vs_coordinate_rounding(
        [[4.0, 0.0, 0.0], [2.0, 4.0, 0.0], [2.0, 2.0, 4.0]],
        [1.4, -1.4, 0.0],
    )
    assert res["exact_separation_verified"] is True
    assert res["nearest_plane_recovered_exact_lattice_point"] is True
    assert res["coordinate_rounding_recovered_exact_lattice_point"] is False


def test_certificate_generation() -> None:
    cert = generate_dcp_lattice_gram_schmidt_babai_nearest_plane_vs_rounding_certificate()
    assert cert["all_checks_passed"] is True
    assert len(cert["certificate_sha256_16"]) == 16

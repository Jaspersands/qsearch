"""Unit tests for the DCP Smith Normal Form invariant-factor channel decoupling bridge (Subsystem 138)."""

from __future__ import annotations

from theorems.dcp_modular_hermite_normal_form_determinant_smith_peeling_bridge import (
    evaluate_smith_normal_form_channel_decoupling,
    generate_dcp_modular_hermite_normal_form_determinant_smith_peeling_certificate,
)


def test_smith_normal_form_decoupling() -> None:
    res = evaluate_smith_normal_form_channel_decoupling(8, [[1, 3], [2, 7]], [[3, 2], [4, 3]], [1, 2])
    assert res["exact_snf_laws_verified"] is True
    assert res["explicit_image_cardinality"] == 32


def test_certificate_generation() -> None:
    cert = generate_dcp_modular_hermite_normal_form_determinant_smith_peeling_certificate()
    assert cert["all_checks_passed"] is True
    assert len(cert["certificate_sha256_16"]) == 16

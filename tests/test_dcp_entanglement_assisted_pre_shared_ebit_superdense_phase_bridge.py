"""Unit tests for the DCP entanglement-assisted Bell-pair X-fault immunity bridge (Subsystem 129)."""

from __future__ import annotations

import math
from theorems.dcp_entanglement_assisted_pre_shared_ebit_superdense_phase_bridge import (
    evaluate_bell_assisted_phase_and_bitflip_immunity,
    generate_dcp_entanglement_assisted_pre_shared_ebit_superdense_phase_certificate,
)


def test_bell_assisted_bitflip_immunity() -> None:
    res = evaluate_bell_assisted_phase_and_bitflip_immunity(math.pi / 3.0, 0.88, [0.0, 0.50, 1.0])
    assert res["all_verified"] is True
    assert abs(res["records"][1]["xx_parity_expectation_explicit"] - 0.44) < 1e-12


def test_certificate_generation() -> None:
    cert = generate_dcp_entanglement_assisted_pre_shared_ebit_superdense_phase_certificate()
    assert cert["all_checks_passed"] is True
    assert len(cert["certificate_sha256_16"]) == 16

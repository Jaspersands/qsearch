"""Unit tests for the DCP post-selected weak-value phase amplification obstruction (Subsystem 96)."""

from __future__ import annotations

import math
from theorems.dcp_post_selected_weak_value_phase_amplification_obstruction import (
    evaluate_weak_value_post_selection_fisher_budget,
    generate_dcp_post_selected_weak_value_phase_amplification_certificate,
)


def test_weak_value_fisher_conservation() -> None:
    res = evaluate_weak_value_post_selection_fisher_budget(0.05, 0.95, [0.05, math.pi / 2.0])
    assert res["all_verified"] is True
    assert res["records"][0]["net_per_copy_post_selected_fisher_info"] < res["records"][1]["net_per_copy_post_selected_fisher_info"]


def test_certificate_generation() -> None:
    cert = generate_dcp_post_selected_weak_value_phase_amplification_certificate()
    assert cert["all_checks_passed"] is True
    assert len(cert["certificate_sha256_16"]) == 16

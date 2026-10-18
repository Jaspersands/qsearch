"""Tests for dcp_dyadic_valuation_anchor_invariance_hierarchy_bridge."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

from theorems.dcp_dyadic_valuation_anchor_invariance_hierarchy_bridge import (
    generate_dcp_dyadic_valuation_anchor_invariance_hierarchy_certificate,
    verify_dyadic_level_anchor_invariance,
)


def test_dyadic_level_anchor_invariance_iff() -> None:
    c1 = verify_dyadic_level_anchor_invariance([[1, 3]], [1, 1], t_bits=3, k_level=1)
    assert c1["iff_characterization_verified"] is True
    assert c1["anchor_invariant_mod_2k"] is True

    c2_odd = verify_dyadic_level_anchor_invariance([[1, 3]], [1, 1], t_bits=3, k_level=2)
    assert c2_odd["iff_characterization_verified"] is True
    assert c2_odd["anchor_invariant_mod_2k"] is False
    assert abs(c2_odd["matching_anchor_fraction"] - 0.5) < 1e-12

    c2_even = verify_dyadic_level_anchor_invariance([[2, 6, 1]], [1, 1, 0], t_bits=3, k_level=2)
    assert c2_even["iff_characterization_verified"] is True
    assert c2_even["anchor_invariant_mod_2k"] is True


def test_certificate_and_reduction_artifact_match() -> None:
    cert = generate_dcp_dyadic_valuation_anchor_invariance_hierarchy_certificate()
    assert cert["all_checks_passed"] is True
    artifact_path = (
        Path(__file__).resolve().parent.parent
        / "research"
        / "reductions"
        / "dcp_dyadic_valuation_anchor_invariance_hierarchy_bridge.json"
    )
    on_disk = json.loads(artifact_path.read_text(encoding="utf-8"))
    assert cert == on_disk


def test_nodejs_crosscheck() -> None:
    script = (
        Path(__file__).resolve().parent.parent
        / "research"
        / "certificates"
        / "dcp_dyadic_valuation_anchor_invariance_hierarchy_bridge_crosscheck.js"
    )
    proc = subprocess.run(["node", str(script)], capture_output=True, text=True, check=True)
    data = json.loads(proc.stdout.strip())
    assert data["status"] == "OK"

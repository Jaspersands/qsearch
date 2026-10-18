"""Tests for dcp_twisted_convolution_pretty_good_measurement_gram_bridge."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

from theorems.dcp_twisted_convolution_pretty_good_measurement_gram_bridge import (
    generate_dcp_twisted_convolution_pretty_good_measurement_gram_certificate,
    verify_ensemble_fiber_spectrum_and_pgm_identity,
)


def test_bijective_and_collision_pgm_controls() -> None:
    bij = verify_ensemble_fiber_spectrum_and_pgm_identity([[1, 2]], q=4)
    assert bij["pgm_formula_exact"] is True
    assert abs(bij["p_pgm_closed_form"] - 1.0) < 1e-12

    col = verify_ensemble_fiber_spectrum_and_pgm_identity([[2, 2]], q=4)
    assert col["pgm_formula_exact"] is True
    assert abs(col["p_pgm_closed_form"] - 0.5) < 1e-12


def test_certificate_and_reduction_artifact_match() -> None:
    cert = generate_dcp_twisted_convolution_pretty_good_measurement_gram_certificate()
    assert cert["all_checks_passed"] is True
    artifact_path = (
        Path(__file__).resolve().parent.parent
        / "research"
        / "reductions"
        / "dcp_twisted_convolution_pretty_good_measurement_gram_bridge.json"
    )
    on_disk = json.loads(artifact_path.read_text(encoding="utf-8"))
    assert cert == on_disk


def test_nodejs_crosscheck() -> None:
    script = (
        Path(__file__).resolve().parent.parent
        / "research"
        / "certificates"
        / "dcp_twisted_convolution_pretty_good_measurement_gram_bridge_crosscheck.js"
    )
    proc = subprocess.run(["node", str(script)], capture_output=True, text=True, check=True)
    data = json.loads(proc.stdout.strip())
    assert data["status"] == "OK"

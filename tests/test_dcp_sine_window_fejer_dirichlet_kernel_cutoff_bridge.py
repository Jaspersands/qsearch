"""Tests for dcp_sine_window_fejer_dirichlet_kernel_cutoff_bridge."""

from __future__ import annotations

import json
import subprocess
import math
from pathlib import Path

import pytest

from theorems.dcp_sine_window_fejer_dirichlet_kernel_cutoff_bridge import (
    generate_dcp_sine_window_fejer_dirichlet_kernel_cutoff_certificate,
    verify_sine_window_three_dirichlet_identity_and_controls,
    centered_sine_characteristic_explicit,
    centered_sine_characteristic_three_dirichlet,
    centered_dirichlet_kernel,
    principal_sidelobe_bound,
)


def test_periodic_main_lobe_alias_refutes_old_unrestricted_claim():
    p = 8
    phi = 2 * math.pi * 7.5 / p
    sine = abs(centered_sine_characteristic_explicit(phi, p))
    box = abs(centered_dirichlet_kernel(phi, p))
    assert sine == pytest.approx(0.8485962650110124)
    assert sine > box
    assert not principal_sidelobe_bound(phi, p)["sidelobe_bound_applies"]


@pytest.mark.parametrize("p", [4, 5, 8, 16, 31])
def test_principal_sidelobe_bound_with_periodic_aliases(p):
    for j in range(65):
        angle = 4 * math.pi / p + (math.pi - 4 * math.pi / p) * j / 64
        for sign in (-1, 1):
            for period in (-3, 0, 2):
                phi = sign * angle + 2 * math.pi * period
                bound = principal_sidelobe_bound(phi, p)
                assert abs(centered_sine_characteristic_explicit(phi, p)) <= bound["upper_bound"] + 1e-12
                assert abs(centered_sine_characteristic_explicit(phi, p)) == pytest.approx(
                    abs(centered_sine_characteristic_explicit(angle, p)), abs=1e-12)


@pytest.mark.parametrize("p", [2, 3, 4, 5, 8])
def test_identity_includes_small_windows_and_aliased_frequencies(p):
    for phi in (0, 0.3, math.pi, 2 * math.pi, 7 * math.pi + 0.2):
        assert centered_sine_characteristic_explicit(phi, p) == pytest.approx(
            centered_sine_characteristic_three_dirichlet(phi, p), abs=1e-12)


@pytest.mark.parametrize("p", [0, 1, 3.5, True])
def test_invalid_window_does_not_produce_certificate(p):
    with pytest.raises(ValueError):
        centered_sine_characteristic_explicit(0, p)


def test_sine_window_three_dirichlet_identity() -> None:
    res = verify_sine_window_three_dirichlet_identity_and_controls(
        p_window=8, test_phis=[0.0, 0.25, 0.73, 1.5]
    )
    assert res["exact_identity_and_controls_verified"] is True
    assert abs(res["sine_at_first_harmonic_2pi_over_P"] - 0.5) < 1e-12


def test_certificate_and_reduction_artifact_match() -> None:
    cert = generate_dcp_sine_window_fejer_dirichlet_kernel_cutoff_certificate()
    assert cert["all_checks_passed"] is True
    artifact_path = (
        Path(__file__).resolve().parent.parent
        / "research"
        / "reductions"
        / "dcp_sine_window_fejer_dirichlet_kernel_cutoff_bridge.json"
    )
    on_disk = json.loads(artifact_path.read_text(encoding="utf-8"))
    assert cert == on_disk


def test_nodejs_crosscheck() -> None:
    script = (
        Path(__file__).resolve().parent.parent
        / "research"
        / "certificates"
        / "dcp_sine_window_fejer_dirichlet_kernel_cutoff_bridge_crosscheck.js"
    )
    proc = subprocess.run(["node", str(script)], capture_output=True, text=True, check=True)
    data = json.loads(proc.stdout.strip())
    assert data["status"] == "OK"

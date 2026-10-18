"""Tests for native_higher_call_composite_modulus_crt_factorization_audit."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

from theorems.native_higher_call_composite_modulus_crt_factorization_audit import (
    generate_native_higher_call_composite_modulus_crt_factorization_certificate,
    verify_crt_character_and_product_channel_factorization,
    verify_non_factoring_window_crt_coupling_control,
)


def test_crt_product_channel_factorization() -> None:
    res = verify_crt_character_and_product_channel_factorization(
        q1=2, q2=3, p1=[0.75, 0.25], p2=[0.6, 0.2, 0.2], b_matrix=[[1, 2, 5]]
    )
    assert res["exact_crt_factorization"] is True


def test_contiguous_window_crt_coupling_control() -> None:
    ctrl = verify_non_factoring_window_crt_coupling_control(q1=2, q2=3, window_support=[0, 1])
    assert ctrl["archimedean_window_couples_crt_factors"] is True


def test_certificate_and_reduction_artifact_match() -> None:
    cert = generate_native_higher_call_composite_modulus_crt_factorization_certificate()
    assert cert["all_checks_passed"] is True
    artifact_path = (
        Path(__file__).resolve().parent.parent
        / "research"
        / "reductions"
        / "native_higher_call_composite_modulus_crt_factorization_audit.json"
    )
    on_disk = json.loads(artifact_path.read_text(encoding="utf-8"))
    assert cert == on_disk


def test_nodejs_crosscheck() -> None:
    script = (
        Path(__file__).resolve().parent.parent
        / "research"
        / "certificates"
        / "native_higher_call_composite_modulus_crt_factorization_audit_crosscheck.js"
    )
    proc = subprocess.run(["node", str(script)], capture_output=True, text=True, check=True)
    data = json.loads(proc.stdout.strip())
    assert data["status"] == "OK"

"""Pytest suite for `theorems/native_higher_call_prime_power_survival_closed_form.py`."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

from theorems.native_higher_call_prime_power_survival_closed_form import (
    ARTIFACT_PATH,
    CONTRACT_PATH,
    DOC_PATH,
    audit_eisenstein_isomorphism_and_simplex_injectivity,
    audit_prime_power_survival_closed_forms,
    build_native_higher_call_prime_power_survival_closed_form_report,
    eisenstein_coords,
    eisenstein_norm,
    fourier_spectral_survival_count,
    histogram_congruence_survival_count,
    squared_trinomial_zero_count,
)
from theorems.native_response_path_valuation import DIGITS, local_difference_counts


ROOT = Path(__file__).resolve().parents[1]
CROSSCHECK_JS = (
    ROOT
    / "research"
    / "certificates"
    / "native_higher_call_prime_power_survival_closed_form_crosscheck.js"
)


def test_files_and_contract_exist() -> None:
    assert CONTRACT_PATH.exists()
    assert DOC_PATH.exists()
    assert CROSSCHECK_JS.exists()
    contract = json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))
    assert contract["contract_id"] == "native-higher-call-prime-power-survival-closed-form-contract"
    assert contract["guardrails"]["accepted_speedup_candidate"] is False


def test_eisenstein_isomorphism_maps_digits_to_cube_roots_of_unity() -> None:
    images = [eisenstein_coords(dx, dy) for dx, dy in DIGITS]
    assert images == [(1, 0), (0, 1), (-1, -1)]
    assert all(eisenstein_norm(u, v) == 1 for u, v in images)


@pytest.mark.parametrize("k", [1, 2, 3, 4, 5, 6, 7, 8])
def test_squared_trinomial_zero_difference_law(k: int) -> None:
    diffs = local_difference_counts(k)
    assert diffs[(0, 0)] == squared_trinomial_zero_count(k)


def test_eisenstein_and_simplex_injectivity_audit() -> None:
    rows = audit_eisenstein_isomorphism_and_simplex_injectivity()
    assert len(rows) == 10
    for row in rows:
        assert row["matches_theorem_1"] is True


def test_prime_power_survival_closed_forms() -> None:
    rows = audit_prime_power_survival_closed_forms()
    assert len(rows) == 21
    for row in rows:
        assert row["matches_theorems_2_and_3"] is True


@pytest.mark.parametrize(("k", "h"), [(2, 1), (3, 2), (4, 2), (5, 3)])
def test_histogram_congruence_matches_fourier_spectral_sum(k: int, h: int) -> None:
    exact = histogram_congruence_survival_count(k, h)
    spectral = fourier_spectral_survival_count(k, h)
    assert abs(spectral - float(exact)) < 1e-8


def test_report_and_nodejs_crosscheck() -> None:
    report = build_native_higher_call_prime_power_survival_closed_form_report()
    assert all(report["verification"].values())
    assert ARTIFACT_PATH.exists()
    saved = json.loads(ARTIFACT_PATH.read_text(encoding="utf-8"))
    assert saved == report

    proc = subprocess.run(
        ["node", str(CROSSCHECK_JS)],
        capture_output=True,
        text=True,
        check=True,
    )
    payload = json.loads(proc.stdout)
    assert payload["status"] == "ok"
    assert payload["trinomial_call_counts_verified"] == 10
    assert payload["prime_power_survival_configs_verified"] == 21


def test_cli_execution() -> None:
    proc = subprocess.run(
        [
            sys.executable,
            "-m",
            "theorems.native_higher_call_prime_power_survival_closed_form",
            "--no-write",
        ],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
        check=True,
    )
    out = json.loads(proc.stdout)
    assert out["subsystem"] == "native_higher_call_prime_power_survival_closed_form"
    assert all(out["verification"].values())

"""Pytest suite for `theorems/lattice_qft_cutoff_phase_fidelity_bridge.py`."""

from __future__ import annotations

from fractions import Fraction
import json
import subprocess
import sys
from pathlib import Path

import numpy as np
import pytest
from qiskit.quantum_info import Operator

from theorems.lattice_qft_cutoff_phase_fidelity_bridge import (
    ARTIFACT_PATH,
    CONTRACT_PATH,
    DOC_PATH,
    analytical_cutoff_qft_matrix,
    audit_cube_source_cutoff_channel,
    banded_dyadic_phase_fraction,
    build_lattice_qft_cutoff_phase_fidelity_bridge_report,
    max_tail_fraction_bound,
    omitted_dyadic_tail_fraction,
)
from theorems.lattice_qft_precision import QFTUsage, compile_qft, precision_plan


ROOT = Path(__file__).resolve().parents[1]
CROSSCHECK_JS = ROOT / "research" / "certificates" / "lattice_qft_cutoff_phase_fidelity_bridge_crosscheck.js"


def test_files_and_contract_exist() -> None:
    assert CONTRACT_PATH.exists()
    assert DOC_PATH.exists()
    assert CROSSCHECK_JS.exists()
    contract = json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))
    assert contract["contract_id"] == "lattice-qft-cutoff-phase-fidelity-bridge-contract"
    assert contract["guardrails"]["accepted_speedup_candidate"] is False


@pytest.mark.parametrize(
    ("ell", "b"),
    [
        (3, 0),
        (3, 1),
        (3, 2),
        (4, 0),
        (4, 1),
        (4, 2),
        (4, 3),
        (5, 2),
        (5, 4),
    ],
)
def test_analytical_cutoff_qft_matrix_matches_compiled_qft(ell: int, b: int) -> None:
    plan = precision_plan(ell, QFTUsage(), "1/10", cutoff=b)
    u_qiskit = Operator(compile_qft(plan)).data
    u_analytical = analytical_cutoff_qft_matrix(ell, b)
    assert np.allclose(u_qiskit, u_analytical, atol=1e-13)
    assert np.allclose(np.abs(u_analytical), 1.0 / np.sqrt(1 << ell), atol=1e-15)


@pytest.mark.parametrize(("ell", "b"), [(3, 0), (4, 1), (5, 2)])
def test_exact_dyadic_tail_decomposition_and_bound(ell: int, b: int) -> None:
    N = 1 << ell
    bound = max_tail_fraction_bound(ell, b)
    for k in range(N):
        for x in range(N):
            banded = banded_dyadic_phase_fraction(ell, b, k, x)
            tail = omitted_dyadic_tail_fraction(ell, b, k, x)
            assert (banded + tail) % 1 == Fraction((k * x) % N, N)
            assert tail <= bound


def test_cube_source_cutoff_channel_uniform_labels_and_visibility_bounds() -> None:
    rows = audit_cube_source_cutoff_channel()
    assert len(rows) == 7
    for row in rows:
        assert row["marginal_label_distribution_exact_uniform"] is True
        assert row["tail_fraction_bound_respected"] is True
        assert row["quadrature_correlation_equals_half_v_eff"] is True
        assert row["v_eff_respects_analytical_lower_bound"] is True


def test_report_and_nodejs_crosscheck() -> None:
    report = build_lattice_qft_cutoff_phase_fidelity_bridge_report()
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
    assert payload["kernel_configs_verified"] == len(report["banded_dyadic_kernel_audit"])


def test_cli_execution() -> None:
    proc = subprocess.run(
        [sys.executable, "-m", "theorems.lattice_qft_cutoff_phase_fidelity_bridge", "--no-write"],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
        check=True,
    )
    out = json.loads(proc.stdout)
    assert out["subsystem"] == "lattice_qft_cutoff_phase_fidelity_bridge"
    assert all(out["verification"].values())

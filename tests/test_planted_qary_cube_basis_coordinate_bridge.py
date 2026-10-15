"""Pytest suite for `theorems/planted_qary_cube_basis_coordinate_bridge.py`."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

from theorems.planted_qary_cube_basis_coordinate_bridge import (
    ARTIFACT_PATH,
    CONTRACT_PATH,
    DOC_PATH,
    basis_coordinates_from_public_lattice,
    build_planted_qary_cube_basis_coordinate_bridge_report,
    build_exact_ternary_saturation_family,
    compute_basis_coordinates_analytical,
    fixed_q_ternary_pivot_bound,
    ternary_pivot_envelope,
)
from theorems.planted_qary_usvp_source import generate_source


ROOT = Path(__file__).resolve().parents[1]
CROSSCHECK_JS = ROOT / "research" / "certificates" / "planted_qary_cube_basis_coordinate_bridge_crosscheck.js"


@pytest.mark.parametrize("q", [3, 5, 7])
@pytest.mark.parametrize("support", range(1, 13))
def test_fixed_modulus_bound_matches_exhaustive_reachable_numerators(q: int, support: int) -> None:
    reachable = {-1, 0, 1}
    for _ in range(support):
        reachable = {x + c for x in reachable for c in range(-(q // 2), q // 2 + 1)}
    maximum = max(abs(x // q) for x in reachable if x % q == 0)
    assert fixed_q_ternary_pivot_bound(support, q) == maximum
    assert maximum <= ternary_pivot_envelope(support)


def test_old_universal_fixed_modulus_sharpness_claim_is_falsified() -> None:
    assert fixed_q_ternary_pivot_bound(9, 3) == 3
    assert ternary_pivot_envelope(9) == 4


def test_replacement_saturation_witnesses_obey_FULL_vector_norm_premise() -> None:
    for row in build_exact_ternary_saturation_family():
        u = row["analysis"]["u_vec"]
        assert any(u) and all(abs(x) <= 1 for x in u)
        assert row["analysis"]["u_inf"] == 1
        assert row["achieved_d_piv_0"] == fixed_q_ternary_pivot_bound(row["s_F"], row["q"])


@pytest.mark.parametrize("value", [True, 1.5, "3", 0, -1])
def test_ternary_envelope_rejects_nonexact_or_nonpositive_support(value) -> None:
    with pytest.raises(ValueError):
        ternary_pivot_envelope(value)


def test_crosscheck_rejects_corrupted_saturation_witness(tmp_path) -> None:
    report = json.loads(ARTIFACT_PATH.read_text())
    report["ternary_saturation_family"][0]["analysis"]["d_full"][0] += 1
    path = tmp_path / "tampered.json"
    path.write_text(json.dumps(report))
    proc = subprocess.run(["node", str(CROSSCHECK_JS), str(path)], capture_output=True, text=True)
    assert proc.returncode != 0


def test_files_and_contract_exist() -> None:
    assert CONTRACT_PATH.exists()
    assert DOC_PATH.exists()
    assert CROSSCHECK_JS.exists()
    contract = json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))
    assert contract["contract_id"] == "planted-qary-cube-basis-coordinate-bridge-contract"
    assert contract["guardrails"]["accepted_speedup_candidate"] is False


@pytest.mark.parametrize(
    ("n", "m", "q", "support", "seed"),
    [
        (4, 2, 257, 3, 10),
        (6, 3, 1009, 4, 20),
        (8, 4, 65537, 5, 30),
        (10, 5, 1000003, 6, 40),
        (12, 6, 1000000007, 8, 50),
    ],
)
def test_analytical_basis_coordinates_match_public_lattice_and_satisfy_q_independent_bounds(
    n: int, m: int, q: int, support: int, seed: int
) -> None:
    gen = generate_source(
        n=n,
        m=m,
        q=q,
        gap=2,
        support=support,
        plant_seed=seed,
        matrix_seed=seed + 100,
    )
    problem = gen.problem
    planted_u = gen.private.plant
    analysis = compute_basis_coordinates_analytical(problem, planted_u)
    d_public = basis_coordinates_from_public_lattice(problem, planted_u)
    assert tuple(analysis["d_full"]) == d_public
    assert analysis["nonzero_free_support_satisfied"] is True
    assert analysis["free_support_s_F"] >= 1
    assert analysis["pivot_support_bound_satisfied"] is True
    assert analysis["pivot_worst_bound_satisfied"] is True
    assert analysis["l1_support_bound_satisfied"] is True
    assert analysis["l1_worst_bound_satisfied"] is True


def test_nonzero_free_support_theorem_rejects_pure_pivot_short_vectors() -> None:
    gen = generate_source(n=6, m=3, q=257, gap=2, support=4, plant_seed=15, matrix_seed=115)
    problem = gen.problem
    piv_cols = problem.pivots
    bad_u = [0] * problem.dimension
    bad_u[piv_cols[0]] = 1
    with pytest.raises(ValueError, match="not in ker"):
        compute_basis_coordinates_analytical(problem, bad_u)


def test_report_and_nodejs_crosscheck() -> None:
    report = build_planted_qary_cube_basis_coordinate_bridge_report()
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
    assert payload["planted_instances_verified"] == len(report["planted_instance_audit"])


def test_cli_execution() -> None:
    proc = subprocess.run(
        [sys.executable, "-m", "theorems.planted_qary_cube_basis_coordinate_bridge", "--no-write"],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
        check=True,
    )
    out = json.loads(proc.stdout)
    assert out["subsystem"] == "planted_qary_cube_basis_coordinate_bridge"
    assert all(out["verification"].values())

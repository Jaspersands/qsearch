"""Regression checks for 2026-11-11 wired Rees SDE tools: P0-free kernel reduction, linedata --no-brute, and sparse2 accounting."""

from __future__ import annotations

import importlib.util
import json
import random
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REVIEWS = ROOT / "research" / "audits" / "reviews"
NEAR_LINEAR = REVIEWS / "2026-11-11-rees-sde-near-linear-total"
INTERVAL_S = REVIEWS / "2026-11-11-rees-sde-interval-s"
BELOW_QTR = REVIEWS / "2026-11-11-rees-sde-p5-below-quarter"


def _load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_p0_kernel_reduction_matches_solutions_proj() -> None:
    sdecore = _load("sdecore", NEAR_LINEAR / "sdecore.py")
    rng = random.Random(20261111)
    for p, kap, d in ((7, 3, 2), (13, 3, 3), (19, 3, 3), (13, 4, 4)):
        _, cos = sdecore.coset_table(p, kap)
        n = 2 * d + 1
        for _ in range(10):
            cols = [[rng.randrange(p) for _ in range(d)] for _ in range(n)]
            expected = sdecore.solutions_proj(cols, p, cos).shape[0]
            got = sdecore.solutions_count_p0(cols, p, kap)
            assert got == expected

    dead7 = [[1, 1, 2], [2, 4, 6], [1, 1, 0], [2, 1, 6], [4, 4, 3], [4, 0, 2], [5, 5, 1]]
    dead13 = [[0, 11, 1], [8, 6, 9], [4, 3, 12], [12, 8, 5], [1, 9, 6], [4, 7, 1], [4, 3, 4]]
    assert sdecore.solutions_count_p0(dead7, 7, 3) == 0
    assert sdecore.solutions_count_p0(dead13, 13, 3) == 0


def test_linedata_no_brute_and_q17_coverage(tmp_path: Path) -> None:
    out11 = subprocess.run(
        [sys.executable, "-I", str(INTERVAL_S / "linedata.py"), "11", "2", "--no-brute"],
        cwd=tmp_path,
        capture_output=True,
        text=True,
        check=True,
    )
    assert "admissible (u,v) != 0: 600; agree with (3): True" in out11.stdout
    built11 = json.loads((tmp_path / "linedata_p11_K2.json").read_text(encoding="utf-8"))
    committed11 = json.loads((INTERVAL_S / "linedata_p11_K2.json").read_text(encoding="utf-8"))
    assert built11 == committed11

    meta17 = json.loads((INTERVAL_S / "linedata_p17_K4.json").read_text(encoding="utf-8"))
    assert meta17["p"] == 17 and meta17["K"] == 4
    assert meta17["n_adm"] == 13824
    assert len(meta17["orbits"]) == 12
    assert sum(orb[2] for orb in meta17["orbits"]) == 13824

    cov = subprocess.run(
        [sys.executable, "-I", str(INTERVAL_S / "coverage_e1.py"), "17", "4", "cases_e1_p17.txt"],
        cwd=INTERVAL_S,
        capture_output=True,
        text=True,
        check=True,
    )
    assert "outside A: 0; missing from A: 0" in cov.stdout
    assert "COVERAGE OK" in cov.stdout


def test_p5_below_quarter_accounting_and_count_check() -> None:
    acc = subprocess.run(
        [sys.executable, "-I", str(BELOW_QTR / "accounting.py")],
        capture_output=True,
        text=True,
        check=True,
    )
    assert "stage inequality violations (q <= 30000): 0" in acc.stdout
    assert "closed-form violations (1.92n+3, n <= 30000): 0 []" in acc.stdout
    assert "G(n) < B'(n) for every n in [29, 30000]" in acc.stdout

    chk = subprocess.run(
        [sys.executable, "-W", "error::SyntaxWarning", "-I", str(NEAR_LINEAR / "count_check.py")],
        capture_output=True,
        text=True,
        check=True,
    )
    assert chk.stdout == (NEAR_LINEAR / "count_check.out").read_text(encoding="utf-8")


def test_dead_w3_search_outputs_and_p0_budget_smoke() -> None:
    lines = (NEAR_LINEAR / "dead_w3_search.out").read_text(encoding="utf-8").splitlines()
    rows = [ln.split() for ln in lines if ln.startswith("3 ") and ln.split()[1] in {"19", "31", "37"}]
    assert len(rows) >= 9
    seen = {(int(r[2]), int(r[1])) for r in rows}
    assert seen == {(d, p) for d in (3, 4, 5) for p in (19, 31, 37)}
    assert all(r[4] == "False" and int(r[8]) > 0 for r in rows)

    res = subprocess.run(
        [sys.executable, "-I", str(NEAR_LINEAR / "dead_w3_search.py"), "--item5", "--ssc", "--budget", "1"],
        capture_output=True,
        text=True,
        check=True,
    )
    out_rows = [ln.split() for ln in res.stdout.splitlines() if ln.startswith("3 ")]
    assert len(out_rows) == 9
    assert all(r[4] == "False" for r in out_rows)


def test_p7_m4_both_orbits_and_six_point_m3_certificates() -> None:
    import itertools

    bounded = REVIEWS / "2026-11-11-rees-sde-bounded-p"
    lrat_lines = (bounded / "lines7_lrat.out").read_text(encoding="utf-8").splitlines()
    assert any("L=file:p7_L4a.txt" in ln and ": UNSAT " in ln and "LRAT VERIFIED" in ln for ln in lrat_lines)
    assert any("L=file:p7_L4b.txt" in ln and ": UNSAT " in ln and "LRAT VERIFIED" in ln for ln in lrat_lines)

    norm = lambda u: (1, (u[1] * pow(u[0], 5, 7)) % 7) if u[0] else (0, 1)
    gl2 = [(a, b, c, d) for a, b, c, d in itertools.product(range(7), repeat=4) if (a * d - b * c) % 7]

    def lines_of(fname: str) -> tuple[tuple[int, int], ...]:
        rows = {tuple(int(x) % 7 for x in ln.split()) for ln in (bounded / fname).read_text().splitlines() if ln.strip()}
        assert len(rows) == 24
        return tuple(sorted({norm(u) for u in rows}))

    orbits = []
    for fname in ("p7_L4a.txt", "p7_L4b.txt"):
        quad = lines_of(fname)
        assert len(quad) == 4
        orb = {tuple(sorted(norm(((a * u[0] + b * u[1]) % 7, (c * u[0] + d * u[1]) % 7)) for u in quad)) for a, b, c, d in gl2}
        orbits.append(orb)
    assert orbits[0].isdisjoint(orbits[1])
    assert {len(orbits[0]), len(orbits[1])} == {28, 42}
    assert len(orbits[0] | orbits[1]) == 70

    m3_lines = (REVIEWS / "2026-11-11-rees-sde-p5-d3" / "small" / "lrat_six_m3_stream.out").read_text(encoding="utf-8").splitlines()
    verified_cases = [ln for ln in m3_lines if ln.startswith("  case ") and "UNSAT=True verified=True chk_rc=0" in ln]
    assert len(verified_cases) == 480
    assert any(ln.startswith("TOTAL | 001 002 010 020 100 112 121 133 200 211 | m=3 support-3 streamed | cases 480 verified 480 |") for ln in m3_lines)


def test_p13_and_p17_streamed_lrat_verifications() -> None:
    p13_lines = (REVIEWS / "2026-11-09-lrat-checker-fix" / "recheck" / "cases13_cases.out").read_text(encoding="utf-8").splitlines()
    assert any("TOTAL: 37/37 cases certified (tie-in OK, UNSAT, LRAT VERIFIED by the fixed checker); 0 skipped, 0 not certified;" in ln for ln in p13_lines)

    p17_lines = (INTERVAL_S / "cases17_K4_lrat.out").read_text(encoding="utf-8").splitlines()
    p17_verified = [ln for ln in p17_lines if ln.startswith("case ") and "UNSAT=True verified=True chk_rc=0" in ln]
    assert len(p17_verified) == 12
    assert any("TOTAL: 12/12 orbits UNSAT LRAT VERIFIED |" in ln for ln in p17_lines)

    p17_zero = (INTERVAL_S / "cases17_K4_zero_equi.out").read_text(encoding="utf-8")
    assert "UNSAT=True verified=True chk_rc=0" in p17_zero


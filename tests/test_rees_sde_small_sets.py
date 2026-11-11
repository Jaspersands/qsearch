"""Tests verifying p = 5, d = 3 small-set orbit enumeration, Burnside counts, and witness checking."""

from __future__ import annotations

import gzip
import hashlib
import shutil
import subprocess
import sys
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
SMALL_DIR = ROOT / "research" / "audits" / "reviews" / "2026-11-11-rees-sde-p5-d3" / "small"


def _compiler() -> str | None:
    return shutil.which("clang") or shutil.which("gcc")


def _expected_hashes() -> dict[str, tuple[int, str]]:
    entries: dict[str, tuple[int, str]] = {}
    for line in (SMALL_DIR / "hashes.txt").read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        name, count, digest = line.split()
        entries[name] = (int(count), digest)
    return entries


def test_small_sets_orbits_models_and_burnside(tmp_path: Path) -> None:
    cc = _compiler()
    if cc is None:
        pytest.skip("No C compiler (clang or gcc) found on PATH")

    orbits_bin = tmp_path / "orbits"
    burnside_bin = tmp_path / "burnside"
    subprocess.run([cc, "-O2", str(SMALL_DIR / "orbits.c"), "-o", str(orbits_bin)], check=True)
    subprocess.run([cc, "-O2", str(SMALL_DIR / "burnside.c"), "-o", str(burnside_bin)], check=True)

    # Rebuild Q_3..Q_6 and compare line counts + SHA-256 against hashes.txt.
    subprocess.run([str(orbits_bin), "6", str(tmp_path / "Q")], check=True)
    hashes = _expected_hashes()
    for k in (3, 4, 5, 6):
        q_name = f"Q_{k}.txt"
        q_path = tmp_path / q_name
        data = q_path.read_bytes()
        expected_count, expected_sha = hashes[q_name]
        assert len(data.splitlines()) == expected_count
        assert hashlib.sha256(data).hexdigest() == expected_sha

        f_name = f"F_{k}.txt"
        with gzip.open(SMALL_DIR / "models" / f"{f_name}.gz", "rb") as src:
            f_bytes = src.read()
        expected_f_count, expected_f_sha = hashes[f_name]
        assert len(f_bytes.splitlines()) == expected_f_count
        assert hashlib.sha256(f_bytes).hexdigest() == expected_f_sha
        (tmp_path / f_name).write_bytes(f_bytes)

    # Verify F_3..F_6 witness models and Q_3..Q_6 closure under small/check_models.py.
    res_models = subprocess.run(
        [sys.executable, str(SMALL_DIR / "check_models.py"), str(tmp_path), "3", "6"],
        capture_output=True,
        text=True,
        check=True,
    )
    for k in (3, 4, 5, 6):
        assert f"k={k} lines " in res_models.stdout
        assert "(all pass check_model), INF 0" in res_models.stdout

    res_closure = subprocess.run(
        [sys.executable, str(SMALL_DIR / "check_models.py"), str(tmp_path), "3", "6", "--closure"],
        capture_output=True,
        text=True,
        check=True,
    )
    for k in (3, 4, 5, 6):
        assert f"k={k}: " in res_closure.stdout
        assert "pairwise inequivalent, spanning" in res_closure.stdout
    for k in (3, 4, 5):
        assert f"k={k} -> {k + 1}:" in res_closure.stdout
        assert "all equivalent to a listed rep" in res_closure.stdout

    # Run burnside.c and compare output with burnside.out.
    res_burnside = subprocess.run([str(burnside_bin)], capture_output=True, text=True, check=True)
    assert res_burnside.stdout == (SMALL_DIR / "burnside.out").read_text(encoding="utf-8")

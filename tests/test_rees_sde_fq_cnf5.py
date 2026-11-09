"""Finite-field SDE gadget SAT encoding (research/audits/reviews/2026-11-08-rees-sde-fq-nest).

gadget_cnf5.py writes the binary-clause CNF, solves it with CaDiCaL and accepts an UNSAT answer
only after lrat-check verifies the LRAT proof.  Two exact controls:
  * p = 7, S = {0, 1, 2, 4} (pow:2), k = d = 2, nested label set, with the first Lemma U case
    fixed (1,0,1:3,0;0,1,1:0,3): UNSAT, LRAT VERIFIED;
  * p = 5, pow:2, k = d = 2, nested: SAT (the p = 5 gadget exists; the model is expanded and
    re-verified inside gadget_cnf5.py).
Plus a checker negative control (9 Nov 2026 audit X1): the upstream lrat-check verified an empty
clause without a conflict, so a satisfiable CNF with a one-line proof must NOT verify.
lrat-check: env LRAT_CHECK, else the fixed build in research/audits/reviews/2026-11-09-lrat-checker-fix
(run its build.sh), else PATH. Skipped when cadical, lrat-check, z3 or pycosat is missing.
"""
import os
import shutil
import subprocess
import sys

import pytest

FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "research", "audits",
                      "reviews", "2026-11-08-rees-sde-fq-nest")
FIXED_LRAT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "research", "audits",
                          "reviews", "2026-11-09-lrat-checker-fix", "lrat-check")
LRAT = (os.environ.get("LRAT_CHECK") or (FIXED_LRAT if os.path.exists(FIXED_LRAT) else None)
        or shutil.which("lrat-check"))
needs_tools = pytest.mark.skipif(
    not (shutil.which("cadical") and LRAT and os.path.exists(LRAT)),
    reason="requires cadical and lrat-check (set LRAT_CHECK)")
needs_checker = pytest.mark.skipif(not (LRAT and os.path.exists(LRAT)),
                                   reason="requires lrat-check (set LRAT_CHECK)")


def _run(args):
    pytest.importorskip("z3")
    pytest.importorskip("pycosat")
    env = dict(os.environ, LRAT_CHECK=LRAT)
    r = subprocess.run([sys.executable, "-B", "gadget_cnf5.py", *args, "--quiet"], cwd=FOLDER,
                       capture_output=True, text=True, env=env, timeout=120)
    assert r.returncode == 0, r.stderr[-500:]
    return r.stdout


@needs_tools
def test_p7_case_unsat_with_verified_lrat_proof():
    out = _run(["7", "pow:2", "2", "2", "nest", "--fix", "1,0,1:3,0;0,1,1:0,3"])
    assert ": UNSAT" in out and "'proof': 'LRAT VERIFIED'" in out, out[-400:]


@needs_tools
def test_p5_nest_gadget_exists():
    out = _run(["5", "pow:2", "2", "2", "nest"])
    assert ": SAT" in out and "UNSAT" not in out, out[-400:]


@needs_checker
def test_lrat_check_rejects_bogus_empty_clause_proofs(tmp_path):
    def verified(cnf, prf):
        a, b = tmp_path / "c.cnf", tmp_path / "c.lrat"
        a.write_text(cnf)
        b.write_text(prf)
        r = subprocess.run([LRAT, str(a), str(b)], capture_output=True, text=True, timeout=60)
        return r.returncode == 0 and "c VERIFIED" in r.stdout.splitlines()
    # satisfiable CNFs: an empty clause without a conflict, with no hint, a RAT hint, or satisfied hints
    assert not verified("p cnf 1 1\n1 0\n", "2 0 0\n")
    assert not verified("p cnf 1 1\n1 0\n", "2 0 1 -1 0\n")
    assert not verified("p cnf 2 2\n1 0\n2 0\n", "3 0 1 2 0\n")
    # unsatisfiable CNF: wrong hint rejected, correct proof verified
    assert not verified("p cnf 1 2\n1 0\n-1 0\n", "3 0 1 0\n")
    assert verified("p cnf 1 2\n1 0\n-1 0\n", "3 0 1 2 0\n")

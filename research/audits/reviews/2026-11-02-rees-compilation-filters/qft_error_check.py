"""Item 7(a)(iii): QFT error accounting against the core's eps split.

1. Exact (Fraction) recomputation from rees_uniform_instrument.json and from
   theorems/rees_uniform_instrument.py (read-only import) on a profile sweep:
   N_QFT*eta <= eps/3, per-instrument q_max*eta = eps/(3 N_instr).
2. Compares the core check's q_max formula max(m, max_d M_d g_d)
   (2026-11-01-rees-core-proof-check.md section 6.2) with the per-instrument
   transform count the compilation note actually charges,
   max(D_c, n, max_d(2 M_d r_d + D_{d-1})).
3. Float check of the restricted-domain hybrid on a toy QFT_5 embedded in
   3 qubits, with leakage into padding and arbitrary ideal behaviour there.

    /opt/anaconda3/bin/python -B research/audits/reviews/2026-11-02-rees-compilation-filters/qft_error_check.py
"""
import json
import random
import sys
from fractions import Fraction
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT))
from theorems.rees_uniform_instrument import prime_field_instrument_budget  # noqa: E402


def core_qmax(case):
    rb = case["recovery_budget"]
    g = rb["lower_central_dimensions"]
    m = g[0]
    return max([m] + [s["arity"] * s["rank"] for s in rb["stages_top_down"]])


def actual_qmax(case):
    rb = case["recovery_budget"]
    D = sum(rb["lower_central_dimensions"])
    return max([D, rb["lower_central_dimensions"][0]] +
               [s["qft_calls_per_conversion"] for s in case["stages_top_down"]])


def frac(x):
    return Fraction(x["numerator"], x["denominator"]) if isinstance(x, dict) else Fraction(x)


def check_case(case, eps, out, label):
    rb = case["recovery_budget"]
    I = rb["complete_instrument_calls"]
    q = case["qft_calls_per_instrument_cap"]
    eta = frac(case["qft_isometry_error_per_call"])
    nq = case["single_coordinate_qft_calls"]
    assert eta == eps / (3 * I * q)
    assert q == actual_qmax(case)
    assert nq <= I * q and nq * eta <= eps / 3
    assert frac(rb["rank_failure_bound"]) <= eps / 3
    assert frac(rb["solver_abort_bound"]) <= eps / 3
    total = frac(rb["rank_failure_bound"]) + frac(rb["solver_abort_bound"]) + nq * eta
    assert total <= eps
    bits = (int(1 / eta) - 1).bit_length() if (1 / eta).denominator == 1 else None
    qc = core_qmax(case)
    agg_core = Fraction(nq, I * qc)  # N_QFT*eta_core / (eps/3)
    out(f" {label}: N_instr={I} q_max={q} eta=eps/{3*I*q} bits={case['qft_precision_bits']}"
        f" N_QFT*eta/(eps/3)={float(Fraction(nq, I*q)):.4f} total/eps={float(total/eps):.4f}"
        f" | core-check q_max={qc} ({'UNDERCOUNTS per instrument' if qc < q else 'ok'};"
        f" aggregate with it {float(agg_core):.4f} of eps/3)")
    return qc < q, agg_core > 1


def hybrid_float_check(out, seed=7):
    rng = np.random.default_rng(seed)
    p, dim = 5, 8
    w = np.exp(2j * np.pi / p)
    F = np.eye(dim, dtype=complex)
    F[:p, :p] = np.array([[w ** (a * b) for b in range(p)] for a in range(p)]) / np.sqrt(p)
    # ideal extended arbitrarily on padding {5,6,7}: a random unitary block there
    Q, _ = np.linalg.qr(rng.normal(size=(3, 3)) + 1j * rng.normal(size=(3, 3)))
    F[p:, p:] = Q
    J = np.eye(dim)[:, :p]  # canonical embedding
    worst = 0.0
    for trial in range(200):
        eta_target = 10 ** rng.uniform(-4, -1)
        H = rng.normal(size=(dim, dim)) + 1j * rng.normal(size=(dim, dim))
        H = (H + H.conj().T) / 2
        # actual C = F expm(i t H); choose t so that ||C J - F J||_op == eta_target
        evals, evecs = np.linalg.eigh(H)

        def C_of(t):
            return F @ (evecs @ np.diag(np.exp(1j * t * evals)) @ evecs.conj().T)
        lo, hi = 0.0, 1.0
        for _ in range(60):
            mid = (lo + hi) / 2
            if np.linalg.norm(C_of(mid) @ J - F @ J, 2) < eta_target:
                lo = mid
            else:
                hi = mid
        C = C_of(lo)
        eta = np.linalg.norm(C @ J - F @ J, 2)
        # ideal arithmetic: +1 mod p on canonical, a random permutation on padding
        P = np.zeros((dim, dim))
        for a in range(p):
            P[(a + 1) % p, a] = 1
        perm = rng.permutation(3) + p
        for a in range(3):
            P[perm[a], p + a] = 1
        n_calls = int(rng.integers(1, 30))
        ideal, actual = np.eye(dim, dtype=complex), np.eye(dim, dtype=complex)
        for _ in range(n_calls):
            ideal, actual = P @ F @ ideal, P @ C @ actual
        err = np.linalg.norm((actual - ideal) @ J, 2)
        leak = np.linalg.norm((np.eye(dim) - J @ J.T) @ actual @ J, 2)
        assert err <= n_calls * eta + 1e-12
        worst = max(worst, err / (n_calls * eta))
    out(f" hybrid float check: 200 random trials, max ||(actual-ideal)J|| / (N*eta) = {worst:.4f} (<= 1);"
        f" last trial leaked mass into padding {leak:.2e}")


def main():
    lines = []
    out = lines.append
    eps = Fraction(1, 3)
    out("== committed artifact rees_uniform_instrument.json (eps = 1/3)")
    art = json.loads((ROOT / "research/reductions/rees_uniform_instrument.json").read_text())
    for case in art["cases"]:
        rb = case["recovery_budget"]
        check_case(case, eps, out, f"{tuple(rb['lower_central_dimensions'])} p={rb['supplied_prime']}")

    out("== sweep: random profiles, classes 2..6, p = 2^61-1, eps in {1/3, 1/1000}")
    rng = random.Random(11)
    under = agg_fail = total = 0
    p = 2 ** 61 - 1
    for _ in range(150):
        c = rng.randint(2, 6)
        g = sorted((rng.randint(1, 9) for _ in range(c)), reverse=True)
        eps2 = rng.choice([Fraction(1, 3), Fraction(1, 1000)])
        try:
            case = prime_field_instrument_budget(tuple(g), prime=p, error=eps2)
        except ValueError:
            continue
        u, a = check_case(case, eps2, lambda s: None, "")
        under += u
        agg_fail += a
        total += 1
    out(f" {total} profiles: all exact checks pass; core-check q_max undercounts the per-instrument"
        f" transform count in {under}; its aggregate allocation would also fail in {agg_fail}")
    hybrid_float_check(out)
    text = "\n".join(lines)
    print(text)
    Path(__file__).with_suffix(".out").write_text(text + "\n")


if __name__ == "__main__":
    main()

"""Brute-force checks, independent of the cone code.

(1) For each example bank printed by deadcone (w2 and tri modes) at kappa = 6,
    p in {13, 19, 31, 37, 43}: enumerate all x in P0^n, confirm no nonzero x has
    sum x_i lambda_i = 0 (dead), and confirm the brute-force cone equals F_p^2
    (equivalently: every one-column extension is solvable, i.e. local maximality).
(2) Random banks (sizes 3..7, few projective points so dead banks are frequent):
    the dead flag of `deadcone p 6 check` equals the brute-force flag.
Run: nice -n 19 /opt/anaconda3/bin/python -I brute_verify.py
"""
import ast
import random
import re
import subprocess

import numpy as np

HERE = "/Users/jaspersands/Developer/qsearch/research/audits/reviews/2026-11-12-rees-sde-dead-k6"
KAP = 6


def p0(p, kap):
    return np.array(sorted({pow(x, kap, p) for x in range(p)}), dtype=np.int64)


def cone_brute(bank, p, kap):
    """Return (#nonzero solutions, boolean p x p cone) by enumerating P0^n."""
    P0 = p0(p, kap)
    S = np.zeros((1, 2), dtype=np.int64)
    nz = np.zeros(1, dtype=bool)  # whether x so far is nonzero
    for (u, v) in bank:
        add = np.stack([P0 * u, P0 * v], axis=1) % p  # |P0| x 2
        S = (S[:, None, :] + add[None, :, :]).reshape(-1, 2) % p
        nz = (nz[:, None] | (P0 != 0)[None, :]).reshape(-1)
    sols = int(np.sum(nz & (S[:, 0] == 0) & (S[:, 1] == 0)))
    C = np.zeros((p, p), dtype=bool)
    C[S[:, 0], S[:, 1]] = True
    return sols, C


def main():
    out = []
    for p in [13, 19, 31, 37, 43]:
        for mode in ["w2", "tri"]:
            txt = subprocess.run([HERE + "/deadcone", str(p), str(KAP), mode], capture_output=True, text=True).stdout
            line = [ln for ln in txt.splitlines() if ln.startswith(mode + " kappa") and "m2=" in ln][0]
            m2 = int(re.search(r"m2=(\d+)", line).group(1))
            bank = ast.literal_eval(line.split("example=")[1])
            sols, C = cone_brute(bank, p, KAP)
            rank = np.linalg.matrix_rank(np.array(bank, dtype=float))
            out.append(f"p={p} {mode}: m2={m2} n={len(bank)} rank={rank} nonzero_solutions={sols} "
                       f"cone_is_all={bool(C.all())} bank={bank}")
            print(out[-1], flush=True)
            assert len(bank) == m2 and sols == 0 and C.all()
    rng = random.Random(20261112)
    for p in [13, 19, 31, 37, 43]:
        banks = []
        for _ in range(400):
            n = rng.randint(3, 7)
            npts = rng.randint(2, 4)
            pts = [(1, rng.randrange(p)) if rng.random() < 0.9 else (0, 1) for _ in range(npts)]
            bank = []
            for _ in range(n):
                (u, v) = rng.choice(pts)
                s = rng.randrange(1, p)
                bank.append((u * s % p, v * s % p))
            banks.append(bank)
        inp = "".join(f"{len(b)} " + " ".join(f"{u} {v}" for (u, v) in b) + "\n" for b in banks)
        flags = subprocess.run([HERE + "/deadcone", str(p), str(KAP), "check"], input=inp,
                               capture_output=True, text=True).stdout.split()
        agree = ndead = 0
        for b, f in zip(banks, flags):
            sols, _ = cone_brute(b, p, KAP)
            bd = int(sols == 0)
            agree += (bd == int(f))
            ndead += bd
        out.append(f"random p={p}: {len(banks)} banks, dead={ndead}, agree={agree}")
        print(out[-1], flush=True)
        assert agree == len(banks)
    print("ALL CHECKS PASSED")


if __name__ == "__main__":
    main()

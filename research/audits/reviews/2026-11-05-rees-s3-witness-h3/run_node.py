"""The fixed-arity node at an FCS grade d (kappa = gcd(d, p-1), h = (p-1)/kappa), with the
conversion of (F4)-(F5): kappa-th roots, Bezout exponent, exact check sum s_i^d lambda_i = 0.

Node: t = g + ceil(log_p(2/tau)) spanning labels; later labels written in the echelon basis of
their span W (abort if outside W); the level-0 solver runs on up to k = ceil(log2(2/tau))
disjoint blocks of L = ceil(2 * Nbar_0(g)) labels (Nbar_0 = N_0 with the public bound
min(p, ceil(2 log2(p-1)) + 4) for s_p); abort if every run overruns.  Arity M = t + k L.
Labels are i.i.d. uniform on a random a-dimensional subspace V of F_p^g, a uniform in [0, g].

Usage: python run_node.py out.json [quick]
"""
import json
import math
import sys
import numpy as np

from wh_lib import Chain, Stream, solve, Exhausted, expected_reads, sigma_public


class Outside(Exception):
    pass


def rref(A, p):
    A = [list(map(int, r)) for r in A]
    piv, r = [], 0
    rows, cols = len(A), len(A[0])
    for c in range(cols):
        i = next((i for i in range(r, rows) if A[i][c] % p), None)
        if i is None:
            continue
        A[r], A[i] = A[i], A[r]
        inv = pow(A[r][c], p - 2, p)
        A[r] = [v * inv % p for v in A[r]]
        for i2 in range(rows):
            if i2 != r and A[i2][c] % p:
                f = A[i2][c]
                A[i2] = [(v - f * w) % p for v, w in zip(A[i2], A[r])]
        piv.append(c)
        r += 1
        if r == rows:
            break
    return np.array(A[:r], dtype=np.int64).reshape(r, cols), piv


def egcd(a, b):
    if b == 0:
        return a, 1, 0
    g, x, y = egcd(b, a % b)
    return g, y, x - (a // b) * y


def run_node(ch, d, g, a, tau, rng):
    p, h, J = ch.p, ch.h, ch.J
    kappa = (p - 1) // h
    assert math.gcd(d, p - 1) == kappa and 2 <= kappa < p - 1
    t = g + math.ceil(math.log(2 / tau, p))
    k = math.ceil(math.log2(2 / tau))
    L = math.ceil(2 * float(expected_reads(J, g, sigma_public(p))))
    M = t + k * L
    # hidden subspace V of dimension a
    while True:
        E = rng.integers(0, p, (g, a))
        if a == 0 or rref(E.T, p)[0].shape[0] == a:
            break
    labels = {}

    def label(i):
        lam = (E @ rng.integers(0, p, a)) % p if a else np.zeros(g, dtype=np.int64)
        labels[i] = lam
        return lam

    T0 = np.array([label(i) for i in range(t)])
    B, piv = rref(T0, p)
    r = len(piv)
    nxt = [t]

    def gen_block(base):
        def gen(kk):
            out = np.empty((kk, max(r, 1)), dtype=np.int64)
            for j in range(kk):
                lam = label(nxt[0])
                nxt[0] += 1
                c = lam[piv] if r else np.zeros(0, dtype=np.int64)
                if np.any((c @ B - lam) % p if r else lam % p):
                    raise Outside
                out[j, :r] = c
                if r == 0:
                    out[j, 0] = 0
            return out
        return gen

    for b in range(k):
        base = t + b * L
        nxt[0] = base
        st = Stream(p, r, rng, cap=L, gen=gen_block(base))
        try:
            I, W = solve(ch, 0, r, np.zeros(r, dtype=np.int64), st)
        except Exhausted:
            continue
        except Outside:
            return {"status": "abort_span", "M": M, "r": r}
        y = {base + int(i): int(w) % p for i, w in zip(I, W)}
        # conversion: kappa-th roots and Bezout exponent alpha with alpha*d = kappa mod (p-1)
        gg, al, _ = egcd(d, p - 1)
        assert gg == kappa
        root = {}
        for x in range(1, p):
            root.setdefault(pow(x, kappa, p), x)
        s = {}
        for i, yi in y.items():
            if yi == 0:
                continue
            assert yi in root, "witness entry outside P_kappa u {0}"
            s[i] = pow(root[yi], al % (p - 1), p)
            assert pow(s[i], d, p) == yi
        tot = np.zeros(g, dtype=np.int64)
        for i, si in s.items():
            tot = (tot + pow(si, d, p) * labels[i]) % p
        ok = bool(s) and not np.any(tot)
        return {"status": "ok" if ok else "WRONG", "M": M, "r": r, "reads": int(st.count),
                "block": b, "support": len(s)}
    return {"status": "abort_overrun", "M": M, "r": r}


if __name__ == "__main__":
    quick = len(sys.argv) > 2
    rng = np.random.default_rng(5112026)
    GRID = [  # (h, p, d, g values)
        (3, 7, 2, [2, 4, 8, 12]), (3, 13, 4, [2, 4, 8, 12]), (3, 13, 8, [4]),
        (3, 19, 6, [2, 3, 4, 5]), (3, 31, 10, [2, 3, 4, 5]),
        (4, 13, 3, [2, 4, 8, 12]), (4, 13, 9, [4]), (4, 17, 4, [2, 3, 4, 5]),
    ]
    out = {"rows": []}
    for h, p, d, gs in GRID:
        ch = Chain(h, p)
        for g in gs:
            for tau in (0.05, 0.5):
                Nexp = float(expected_reads(ch.J, g, sigma_public(p)))
                trials = int(min(150, max(10, (3e4 if quick else 2e5) // max(Nexp, 1))))
                res = [run_node(ch, d, g, int(rng.integers(0, g + 1)), tau, rng) for _ in range(trials)]
                st = {}
                for x in res:
                    st[x["status"]] = st.get(x["status"], 0) + 1
                row = {"h": h, "p": p, "d": d, "kappa": (p - 1) // h, "J": ch.J, "g": g, "tau": tau,
                       "M": res[0]["M"], "trials": trials, "status": st,
                       "abort_rate": (trials - st.get("ok", 0)) / trials,
                       "mean_reads_ok": float(np.mean([x["reads"] for x in res if x["status"] == "ok"]))
                       if st.get("ok") else None}
                out["rows"].append(row)
                print(row, flush=True)
    out["any_wrong"] = any("WRONG" in r["status"] for r in out["rows"])
    out["max_abort_rate_vs_tau"] = max(r["abort_rate"] / r["tau"] for r in out["rows"])
    with open(sys.argv[1], "w") as f:
        json.dump(out, f, indent=1)
    print("any wrong", out["any_wrong"], "max abort/tau", out["max_abort_rate_vs_tau"])

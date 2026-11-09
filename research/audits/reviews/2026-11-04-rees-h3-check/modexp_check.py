"""Scratch check: controlled in-place modular multiplication x <- k x mod N (N odd,
composite allowed) from the blocks of theorems/rees_circuit_arith.py, and the
modular exponentiation of Shor's order finding. Exhaustive on canonical inputs."""
import sys, math, itertools
sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4]))
from theorems.rees_circuit_arith import Ops, Anc, anc_size, const_mul_acc

def cmul_ops(N, k, X, T, c, A):
    kinv = pow(k, -1, N)
    ops = Ops()
    const_mul_acc(ops, N, T, X, k, A, c)          # T += c*k*X
    inv = Ops(); const_mul_acc(inv, N, X, T, kinv, A, c)
    ops += inv.inverse()                          # X -= c*kinv*T
    for xq, tq in zip(X, T):                      # controlled swap
        ops.cx(tq, xq); ops.ccx(c, xq, tq); ops.cx(tq, xq)
    return ops

def run(ops, state):
    s = dict(state)
    for g, q in ops:
        if g == "x": s[q[0]] ^= 1
        elif g == "cx": s[q[1]] ^= s[q[0]]
        elif g == "ccx": s[q[2]] ^= s[q[0]] & s[q[1]]
        elif g == "swap": s[q[0]], s[q[1]] = s[q[1]], s[q[0]]
    return s

def layout(b, tbits):
    q = list(range(tbits + 2*b + anc_size(b)))
    E = q[:tbits]; X = q[tbits:tbits+b]; T = q[tbits+b:tbits+2*b]; A = Anc(q[tbits+2*b:], b)
    return q, E, X, T, A

def check_cmul(N):
    b = N.bit_length()
    q, E, X, T, A = layout(b, 1)
    worst = 0
    for k in range(1, N):
        if math.gcd(k, N) != 1: continue
        ops = cmul_ops(N, k, X, T, E[0], A)
        worst = max(worst, len(ops))
        for c in (0, 1):
            for x in range(N):
                st = {i: 0 for i in q}; st[E[0]] = c
                for j in range(b): st[X[j]] = x >> j & 1
                out = run(ops, st)
                xv = sum(out[X[j]] << j for j in range(b))
                want = (k*x % N) if c else x
                assert xv == want, (N, k, c, x, xv)
                assert all(out[i] == 0 for i in T + A.all), (N, k, c, x)
                assert out[E[0]] == c
    return b, worst

def check_modexp(N, a, tbits):
    b = N.bit_length()
    q, E, X, T, A = layout(b, tbits)
    ops = Ops(); ops.x(X[0])                      # X = 1
    for j in range(tbits):
        ops += cmul_ops(N, pow(a, 2**j, N), X, T, E[j], A)
    for e in range(2**tbits):
        st = {i: 0 for i in q}
        for j in range(tbits): st[E[j]] = e >> j & 1
        out = run(ops, st)
        assert sum(out[X[j]] << j for j in range(b)) == pow(a, e, N)
        assert all(out[i] == 0 for i in T + A.all)
    return len(ops)

if __name__ == "__main__":
    for N in (9, 15, 21, 25, 27, 33, 35, 45, 49, 51, 55, 57, 63):
        b, w = check_cmul(N)
        print(f"cmul N={N} b={b} exhaustive ok, max gates={w} <= 80b^2+27b={80*b*b+27*b}: {w <= 80*b*b+27*b}")
    for N, a in ((15, 7), (21, 2), (33, 5), (35, 3)):
        print("modexp", N, a, check_modexp(N, a, 5))
    # gate count of one controlled multiplication as a function of b (worst constant k)
    for b in range(2, 33, 5):
        N = (1 << b) - 1 if b > 1 else 3
        N |= 1
        q, E, X, T, A = layout(b, 1)
        k = N - 2 if math.gcd(N - 2, N) == 1 else 1
        # worst case for Hamming weights: count over a few k
        ws = [len(cmul_ops(N, kk, X, T, E[0], A)) for kk in (k, 1, 3, N-1) if math.gcd(kk, N) == 1]
        print("b", b, "N", N, "max gates", max(ws), "bound 80b^2+27b", 80*b*b + 27*b, "ok", max(ws) <= 80*b*b + 27*b)

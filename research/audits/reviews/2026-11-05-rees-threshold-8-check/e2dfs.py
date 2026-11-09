r"""Independent exact decision of p in E_2(kappa) (threshold-8 checker, 2026-11-05).

Written from the definition in appendix-schedule2.tex (Lemma lem:app-s2-normal and the
normal form after it); shares no code with dfs2b, rcdfs.c or the threshold-8 folder.

Normal form: beta_0 = 0, alpha_0 = 1. Then row 0 forces alpha_j in Qc[-j] and column 0
forces beta_i in Qc[-i] - 1, where Qc[m] = Q_m u {0}. Given beta, the columns j >= 1 are
independent: alpha_j exists iff C_j(beta) = {x in Qc[-j] : x + beta_i in Qc[-(i+j)] for all i}
is nonempty. So p notin E_2 iff some beta (beta_0 = 0, beta_i in Qc[-i]-1) leaves every
C_j nonempty.

Search: DFS over the rows i >= 1 with forward checking. At a node, the domain of an
unassigned row i is D_i = (Qc[-i]-1) n  /\_j (Qc[-(i+j)] - C_j), the exact set of values of
beta_i compatible with the current column sets (computed as a union of shifts when the
C_j are small, else by testing each candidate value). The next row is the one with the
smallest domain; an empty domain prunes. Sets are Python-int bitsets over Z_p.
Complete: every beta in the product of the initial domains that leaves all C_j nonempty
is reached. Every FEASIBLE witness (alpha, beta) is re-checked on all kappa^2 cells with
pow() and a coset generator chosen independently of the search tables.

usage: e2dfs.py kappa pmin pmax [time_limit_s_per_prime]
"""
import sys, time

def primes_upto(n):
    s = bytearray([1]) * (n + 1); s[0] = s[1] = 0
    for i in range(2, int(n ** 0.5) + 1):
        if s[i]:
            s[i * i::i] = bytearray(len(s[i * i::i]))
    return [i for i in range(n + 1) if s[i]]

def factor_primes(n):
    fs, d = [], 2
    while d * d <= n:
        if n % d == 0:
            fs.append(d)
            while n % d == 0: n //= d
        d += 1
    if n > 1: fs.append(n)
    return fs

def coset_generator(p, k, start=2):
    """least xi >= start with xi^h of exact order k"""
    h = (p - 1) // k
    for x in range(start, p):
        z = pow(x, h, p)
        if all(pow(z, k // q, p) != 1 for q in factor_primes(k)):
            return x

class Inst:
    def __init__(self, p, k):
        self.p, self.k = p, k
        self.h = (p - 1) // k
        xi = coset_generator(p, k)
        self.xi = xi
        zeta = pow(xi, self.h, p)
        zp = {}
        z = 1
        for e in range(k):
            zp[z] = e; z = z * zeta % p
        ind = [None] * p
        for x in range(1, p):
            ind[x] = zp[pow(x, self.h, p)]
        self.ind = ind
        self.full = (1 << p) - 1
        Qc = [1 for _ in range(k)]  # bit 0 = the element 0
        for x in range(1, p):
            Qc[ind[x]] |= 1 << x
        self.Qc = Qc

    def shift(self, S, a):
        """S - a = {s - a mod p}"""
        p = self.p
        a %= p
        if a == 0: return S
        return ((S >> a) | (S << (p - a))) & self.full

    def elems(self, S):
        out = []
        while S:
            low = S & -S
            out.append(low.bit_length() - 1)
            S ^= low
        return out

def solve(I, tlimit):
    p, k, Qc = I.p, I.k, I.Qc
    t0 = time.time()
    # initial column sets C_j = Qc[-j] (alpha_j with beta_0 = 0), j = 1..k-1
    C0 = [None] + [Qc[(-j) % k] for j in range(1, k)]
    D0 = {i: I.shift(Qc[(-i) % k], 1) for i in range(1, k)}   # Qc[-i] - 1
    nodes = [0]

    def domain(i, C, base):
        # values b in base with: for every j >= 1, exists x in C_j, x + b in Qc[-(i+j)]
        tot = sum(bin(C[j]).count("1") for j in range(1, k))
        nb = bin(base).count("1")
        if tot <= nb * (k - 1):
            D = base
            for j in range(1, k):
                T = Qc[(-(i + j)) % k]
                U = 0
                for x in I.elems(C[j]):
                    U |= I.shift(T, x)           # {t - x}
                D &= U
                if not D: return 0
            return D
        D = 0
        for b in I.elems(base):
            ok = True
            for j in range(1, k):
                if not (C[j] & I.shift(Qc[(-(i + j)) % k], b)):
                    ok = False; break
            if ok: D |= 1 << b
        return D

    def rec(C, doms, beta):
        nodes[0] += 1
        if time.time() - t0 > tlimit:
            raise TimeoutError
        if not doms:
            return (dict(beta), C)
        newd = {}
        for i, base in doms.items():
            d = domain(i, C, base)
            if not d: return None
            newd[i] = d
        i = min(newd, key=lambda r: bin(newd[r]).count("1"))
        rest = {r: d for r, d in newd.items() if r != i}
        for b in I.elems(newd[i]):
            C2 = [None] + [C[j] & I.shift(Qc[(-(i + j)) % k], b) for j in range(1, k)]
            if not all(C2[1:]): continue
            beta[i] = b
            r = rec(C2, rest, beta)
            if r is not None:
                return r
            del beta[i]
        return None

    res = rec(C0, D0, {0: 0})
    return res, nodes[0], time.time() - t0

def check_cells(p, k, xi, alpha, beta):
    h = (p - 1) // k
    zeta = pow(xi, h, p)
    zpow = [pow(zeta, e, p) for e in range(k)]
    if (alpha[0] + beta[0]) % p == 0: return False
    for i in range(k):
        for j in range(k):
            c = (alpha[j] + beta[i]) % p
            if c == 0: continue
            if pow(c, h, p) != zpow[(-(i + j)) % k]:
                return False
    return True

def main():
    k, pmin, pmax = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
    tl = float(sys.argv[4]) if len(sys.argv) > 4 else 600.0
    for p in primes_upto(pmax):
        if p < pmin or p % k != 1: continue
        I = Inst(p, k)
        try:
            res, nodes, dt = solve(I, tl)
        except TimeoutError:
            print(f"k={k} p={p} UNDECIDED (time limit)", flush=True); continue
        if res is None:
            print(f"k={k} p={p} INFEASIBLE nodes={nodes} t={dt:.1f}", flush=True)
        else:
            bd, C = res
            beta = [bd[i] for i in range(k)]
            alpha = [1] + [I.elems(C[j])[0] for j in range(1, k)]
            ok = check_cells(p, k, I.xi, alpha, beta)
            assert ok, (p, k)
            print(f"k={k} p={p} FEASIBLE nodes={nodes} t={dt:.1f} xi={I.xi} "
                  f"alpha={alpha} beta={beta} powcheck=OK", flush=True)

if __name__ == "__main__":
    main()

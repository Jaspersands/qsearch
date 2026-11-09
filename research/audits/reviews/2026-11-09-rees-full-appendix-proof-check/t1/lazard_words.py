"""t1 check of lem:tb-integral, lem:tb-words, lem:tb-evaluation (appendix-torsion-blackbox.tex).

Builds Pi_T exactly as in the proof of lem:tb-words (W_{k+1} = W_k * prod_b C_b^{r_b},
r_b = coef_w(D_k)/k via Dynkin-Specht-Wever), in the truncated free associative algebra
Q<X,Y>/(deg > c), and checks:
  (a) every intermediate D_k is a Lie element with theta(D_k) = k D_k (DSW) and coefficients
      in R_c = Z[1/c!]; the commutator series log(e^-U e^-V e^U e^V) has R_c coefficients;
  (b) the program evaluates to exp T exactly (T = X+Y and T = [X,Y]);
  (c) all exponents r have denominators dividing a power of c! (so prime to p > c);
  (d) evaluated in UT_n(Z/p^e) (n-1 = c < p) with powers z^{a/b} taken as z^n,
      n = a b^{-1} mod p^e (lem:tb-evaluation), the program gives log x + log y and
      [log x, log y] for the matrix logarithm (independent model of log G).
Finite checks only; they can falsify, not prove.
"""
from fractions import Fraction as Fr
import itertools, random, sys, json, math


class TA:
    """Truncated tensor algebra Q<X_0,X_1>/(deg>c); elements dict word(tuple)->Fraction."""

    def __init__(self, c):
        self.c = c

    def mul(self, a, b):
        r = {}
        for wa, ca in a.items():
            la = len(wa)
            for wb, cb in b.items():
                if la + len(wb) > self.c:
                    continue
                w = wa + wb
                r[w] = r.get(w, 0) + ca * cb
        return {w: v for w, v in r.items() if v != 0}

    def add(self, a, b, s=1):
        r = dict(a)
        for w, v in b.items():
            r[w] = r.get(w, 0) + s * v
        return {w: v for w, v in r.items() if v != 0}

    def scal(self, a, t):
        return {w: v * t for w, v in a.items() if v * t != 0}

    def exp(self, a):
        assert () not in a
        res = {(): Fr(1)}
        term = {(): Fr(1)}
        for k in range(1, self.c + 1):
            term = self.scal(self.mul(term, a), Fr(1, k))
            if not term:
                break
            res = self.add(res, term)
        return res

    def log(self, g):
        w = dict(g)
        assert w.get((), 0) == 1
        del w[()]
        res = {}
        term = {(): Fr(1)}
        for k in range(1, self.c + 1):
            term = self.mul(term, w)
            if not term:
                break
            res = self.add(res, self.scal(term, Fr((-1) ** (k + 1), k)))
        return res

    def bch(self, a, b):
        return self.log(self.mul(self.exp(a), self.exp(b)))

    def br(self, a, b):
        return self.add(self.mul(a, b), self.mul(b, a), -1)

    def lbr(self, w):
        """left-normed Lie bracket [..[X_w1,X_w2],..,X_wk] as a TA element"""
        r = {(w[0],): Fr(1)}
        for i in w[1:]:
            r = self.br(r, {(i,): Fr(1)})
        return r

    def theta(self, a):
        r = {}
        for w, v in a.items():
            r = self.add(r, self.scal(self.lbr(w), v))
        return r


def is_csmooth_den(fr, c):
    """denominator divides a power of c! (equivalently, all prime factors <= c)"""
    d = fr.denominator
    for q in range(2, c + 1):
        while d % q == 0:
            d //= q
    return d == 1


def check_lie_and_integral(A, u, c, name):
    """u: TA element. Check each homogeneous part u_n satisfies theta(u_n) = n u_n (Lie element)
    and has R_c coefficients."""
    ok = True
    for n in range(1, c + 1):
        un = {w: v for w, v in u.items() if len(w) == n}
        if not un:
            continue
        if A.theta(un) != A.scal(un, n):
            print("NOT LIE", name, n)
            ok = False
        if not all(is_csmooth_den(v, c) for v in un.values()):
            print("NOT R_c", name, n)
            ok = False
    return ok


def build_program(T, c):
    A = TA(c)
    prog = [("in", 0), ("in", 1)]
    vals = [{(0,): Fr(1)}, {(1,): Fr(1)}]

    def emit(ins, val):
        prog.append(ins)
        vals.append(val)
        return len(prog) - 1

    def mul(i, j):
        return emit(("mul", i, j), A.bch(vals[i], vals[j]))

    def pw(i, r):
        return emit(("pow", i, r), A.scal(vals[i], r))

    inv_cache = {}

    def inv(i):
        if i not in inv_cache:
            inv_cache[i] = pw(i, Fr(-1))
        return inv_cache[i]

    def comm(i, j):  # (g,h) = g^-1 h^-1 g h
        t = mul(inv(i), inv(j))
        t = mul(t, i)
        return mul(t, j)

    ccache = {}

    def C(w):
        if w in ccache:
            return ccache[w]
        r = w[0] if len(w) == 1 else comm(C(w[:-1]), w[-1])
        ccache[w] = r
        return r

    allok = True
    W = None
    for k in range(1, c + 1):
        Z = dict(T) if W is None else A.bch(A.scal(vals[W], -1), T)
        if not all(len(w) >= k for w in Z):
            print("degree invariant fails at k", k)
            allok = False
        Dk = {w: v for w, v in Z.items() if len(w) == k}
        if not Dk:
            continue
        allok &= check_lie_and_integral(A, Dk, c, "D_%d" % k)
        # D_k = sum_w (coef_w/k) [w]  (DSW)
        P = None
        for w, v in sorted(Dk.items()):
            if len(w) >= 2 and w[0] == w[1]:
                continue  # [w] = 0 and C_w = 1
            r = v / k
            # log C_w in [w] + Lambda^(k+1)
            lc = vals[C(w)]
            low = {u: x for u, x in lc.items() if len(u) <= k}
            if low != A.lbr(w):
                print("log C_w not in [w] + Lambda^(k+1)", w)
                allok = False
            t = pw(C(w), r)
            P = t if P is None else mul(P, t)
        if P is not None:
            W = P if W is None else mul(W, P)
    if vals[W] != {w: v for w, v in T.items() if v != 0}:
        print("FINAL MISMATCH")
        allok = False
    # make W the last instruction
    if W != len(prog) - 1:
        W = pw(W, Fr(1))
    return prog, allok


def prog_stats(prog, c):
    nm = sum(1 for ins in prog if ins[0] == "mul")
    npow = sum(1 for ins in prog if ins[0] == "pow")
    nontriv = sum(1 for ins in prog if ins[0] == "pow" and ins[2] not in (Fr(1), Fr(-1)))
    dens = sorted({ins[2].denominator for ins in prog if ins[0] == "pow"})
    smooth = all(is_csmooth_den(ins[2], c) for ins in prog if ins[0] == "pow")
    return dict(mults=nm, powers=npow, nontrivial_powers=nontriv, denominators=dens, csmooth=smooth)


# ---------------- evaluation in UT_n(Z/p^e) -----------------

def matmul(A, B, n, M):
    return [[sum(A[i][k] * B[k][j] for k in range(n)) % M for j in range(n)] for i in range(n)]


def matpow(A, e, n, M):
    R = [[int(i == j) for j in range(n)] for i in range(n)]
    B = A
    while e:
        if e & 1:
            R = matmul(R, B, n, M)
        B = matmul(B, B, n, M)
        e >>= 1
    return R


def matlog(A, n, M):
    N = [[(A[i][j] - (i == j)) % M for j in range(n)] for i in range(n)]
    res = [[0] * n for _ in range(n)]
    P = [[int(i == j) for j in range(n)] for i in range(n)]
    for k in range(1, n):
        P = matmul(P, N, n, M)
        coef = ((-1) ** (k + 1)) * pow(k, -1, M)
        for i in range(n):
            for j in range(n):
                res[i][j] = (res[i][j] + coef * P[i][j]) % M
    return res


def eval_prog_group(prog, x, y, mul, powf, M):
    v = [x, y]
    for ins in prog[2:]:
        if ins[0] == "mul":
            v.append(mul(v[ins[1]], v[ins[2]]))
        else:
            r = ins[2]
            nexp = (r.numerator * pow(r.denominator, -1, M)) % M
            v.append(powf(v[ins[1]], nexp))
    return v[-1]


def test_UT(progs, n, p, e, trials, rng):
    M = p ** e
    mul = lambda A, B: matmul(A, B, n, M)
    powf = lambda A, k: matpow(A, k, n, M)
    bad = 0
    for _ in range(trials):
        X = [[(rng.randrange(M) if j > i else int(i == j)) for j in range(n)] for i in range(n)]
        Y = [[(rng.randrange(M) if j > i else int(i == j)) for j in range(n)] for i in range(n)]
        lx, ly = matlog(X, n, M), matlog(Y, n, M)
        sp = eval_prog_group(progs["plus"], X, Y, mul, powf, M)
        sb = eval_prog_group(progs["br"], X, Y, mul, powf, M)
        want_p = [[(lx[i][j] + ly[i][j]) % M for j in range(n)] for i in range(n)]
        xy = matmul(lx, ly, n, M)
        yx = matmul(ly, lx, n, M)
        want_b = [[(xy[i][j] - yx[i][j]) % M for j in range(n)] for i in range(n)]
        if matlog(sp, n, M) != want_p or matlog(sb, n, M) != want_b:
            bad += 1
    return bad


def main():
    rng = random.Random(20261109)
    out = {}
    cmax = int(sys.argv[1]) if len(sys.argv) > 1 else 4
    for c in range(1, cmax + 1):
        A = TA(c)
        # tb-integral input: the commutator series and the conjugation series
        U, V = {(0,): Fr(1)}, {(1,): Fr(1)}
        com = A.log(A.mul(A.mul(A.exp(A.scal(U, -1)), A.exp(A.scal(V, -1))), A.mul(A.exp(U), A.exp(V))))
        ok_com = check_lie_and_integral(A, com, c, "commutator series")
        deg2 = {w: v for w, v in com.items() if len(w) == 2}
        ok_com &= (deg2 == A.br(U, V)) or c < 2
        # every higher multihomogeneous part contains both letters
        ok_com &= all((0 in w and 1 in w) for w in com)
        bch = A.bch(U, V)
        ok_bch = check_lie_and_integral(A, bch, c, "BCH")
        progs = {}
        res = {"c": c, "commutator_series_ok": ok_com, "bch_ok": ok_bch}
        for name, T in (("plus", A.add(U, V)), ("br", A.br(U, V))):
            if name == "br" and c < 2:
                T = {}
            if not T:
                continue
            prog, ok = build_program(T, c)
            progs[name] = prog
            res[name] = dict(prog_stats(prog, c), exact=ok)
        if c >= 2:
            n = c + 1
            for p in [q for q in (3, 5, 7, 11) if q > c][:2]:
                for e in (1, 2, 3):
                    bad = test_UT(progs, n, p, e, 30, rng)
                    res["UT_%d_p%d_e%d_bad" % (n, p, e)] = bad
        out[c] = res
        print(json.dumps(res, default=str))
    return out


if __name__ == "__main__":
    main()

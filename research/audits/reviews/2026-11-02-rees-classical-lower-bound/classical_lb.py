"""Exact checks for the classical query lower bound of the Rees HSP note.

Run:  /opt/anaconda3/bin/python -B classical_lb.py  (writes classical_lb.json here)

Checks, all on explicit Lazard groups G=(L,*) with truncated BCH, class<=3:
  1. structure: exponent p, every line a subgroup, normal lines = central lines,
     subalgebra enumeration (m<=4) with Frattini ranks d(H)=dim h/[h,h];
  2. lower bound: the best deterministic q-query success against the uniform
     prior on lines (or on noncentral lines) is (cov*(q)+1)/N, cov*(q)<=C(q,2);
     exhaustive cov* where feasible, otherwise an exhibited set attaining C(q,2);
  3. upper bound: exact success of the birthday algorithm for every subgroup,
     the exact minimal Q for worst-case success>=2/3, the closed-form Q(eps);
  4. Monte Carlo of the birthday algorithm on the real group (float check);
  5. base-K family counts (normal and non-normal H over an ideal K);
  6. Schedule-1 quantum query count vs classical bounds, with crossover primes.
"""
from __future__ import annotations

import itertools
import json
import math
import random
from fractions import Fraction
from pathlib import Path

HERE = Path(__file__).resolve().parent


# ---------------------------------------------------------------- Lie algebras
class Lie:
    """Nilpotent Lie algebra over F_p from brackets [e_i,e_j] = sum c e_k."""

    def __init__(self, name, p, m, brackets, cls):
        self.name, self.p, self.m, self.cls = name, p, m, cls
        assert p > cls, "Lazard needs class < p"
        self.T = {}
        for (i, j), vec in brackets.items():
            v = tuple(x % p for x in vec)
            self.T[i, j] = v
            self.T[j, i] = tuple((-x) % p for x in v)
        self.inv2 = pow(2, -1, p)
        self.inv12 = pow(12, -1, p) if cls >= 3 else None
        self._jacobi()

    def br(self, x, y):
        p, out = self.p, [0] * self.m
        for (i, j), v in self.T.items():
            a = x[i] * y[j] % p
            if a:
                for k in range(self.m):
                    if v[k]:
                        out[k] = (out[k] + a * v[k]) % p
        return tuple(out)

    def add(self, *vs):
        return tuple(sum(c) % self.p for c in zip(*vs))

    def scal(self, s, x):
        return tuple(s * a % self.p for a in x)

    def bch(self, x, y):
        """Truncated BCH, exact for class <= 3."""
        assert self.cls <= 3
        xy = self.br(x, y)
        terms = [x, y, self.scal(self.inv2, xy)]
        if self.cls >= 3:
            terms.append(self.scal(self.inv12, self.br(x, xy)))
            terms.append(self.scal((-self.inv12) % self.p, self.br(y, xy)))
        return self.add(*terms)

    def diff(self, x, y):
        """log(x^{-1} * y); x^{-1} = -x in the BCH chart."""
        return self.bch(self.scal(-1, x), y)

    def _jacobi(self):
        e = units(self.m)
        z = (0,) * self.m
        for a, b, c in itertools.product(e, repeat=3):
            s = self.add(self.br(a, self.br(b, c)), self.br(b, self.br(c, a)),
                         self.br(c, self.br(a, b)))
            assert s == z, "Jacobi fails"

    def elements(self):
        return list(itertools.product(range(self.p), repeat=self.m))


def units(m):
    return [tuple(int(i == j) for j in range(m)) for i in range(m)]


def line_id(v, p):
    """Canonical generator of the line F_p v (first nonzero coordinate 1)."""
    for a in v:
        if a:
            inv = pow(a, -1, p)
            return tuple(x * inv % p for x in v)
    return None


def rref(rows, p, m):
    rows = [list(r) for r in rows]
    basis, col = [], 0
    r = 0
    for col in range(m):
        piv = next((i for i in range(r, len(rows)) if rows[i][col]), None)
        if piv is None:
            continue
        rows[r], rows[piv] = rows[piv], rows[r]
        inv = pow(rows[r][col], -1, p)
        rows[r] = [x * inv % p for x in rows[r]]
        for i in range(len(rows)):
            if i != r and rows[i][col]:
                f = rows[i][col]
                rows[i] = [(a - f * b) % p for a, b in zip(rows[i], rows[r])]
        r += 1
    return tuple(tuple(x) for x in rows[:r])


def span_contains(basis_rref, v, p, m):
    return len(rref(list(basis_rref) + [v], p, m)) == len(basis_rref)


def heis(p):
    return Lie("Heis(F_%d)" % p, p, 3, {(0, 1): (0, 0, 1)}, 2)


def abelian(p, m):
    return Lie("F_%d^%d (abelian control)" % (p, m), p, m, {}, 1)


def filiform4(p):
    # [e0,e1]=e2, [e0,e2]=e3 : class 3, g=(4,2,1)
    return Lie("Fil4(F_%d)" % p, p, 4, {(0, 1): (0, 0, 1, 0), (0, 2): (0, 0, 0, 1)}, 3)


def free23(p):
    # x=e0, y=e1, [x,y]=e2, [x,[x,y]]=e3, [y,[x,y]]=e4 : free class 3, g=(5,3,2)
    return Lie("Free(2,3)(F_%d)" % p, p, 5,
               {(0, 1): (0, 0, 1, 0, 0), (0, 2): (0, 0, 0, 1, 0), (1, 2): (0, 0, 0, 0, 1)}, 3)


# ------------------------------------------------------------- 1. structure
def structure(L):
    p, m = L.p, L.m
    els = L.elements()
    zero = (0,) * m
    # exponent p: x^p = exp(p x) checked by repeated BCH
    for x in els:
        y = zero
        for _ in range(p):
            y = L.bch(y, x)
        assert y == zero
    # BCH associativity on a sample (exact group law check)
    rnd = random.Random(1)
    for _ in range(300):
        a, b, c = (rnd.choice(els) for _ in range(3))
        assert L.bch(L.bch(a, b), c) == L.bch(a, L.bch(b, c))
    lines = sorted({line_id(v, p) for v in els if v != zero})
    N = len(lines)
    assert N == (p ** m - 1) // (p - 1)
    # each line closed under BCH; normal iff central
    center = [v for v in lines if all(L.br(v, e) == zero for e in units(m))]
    for v in lines:
        pts = [L.scal(s, v) for s in range(p)]
        assert all(L.bch(a, b) in pts for a in pts for b in pts)
        normal = all(L.add(L.br(e, v)) in pts for e in units(m))  # [L,v] in Fv
        assert normal == (v in center)
    z = round(math.log(len(center) * (p - 1) + 1, p))
    return {"group": L.name, "p": p, "m": m, "class": L.cls, "order": p ** m,
            "lines_N": N, "center_dim_z": z, "central_lines": len(center),
            "noncentral_lines": N - len(center),
            "checks": "exponent p (all elements); BCH associativity (300 samples); "
                      "every line a subgroup; normal line <=> central line"}


def subalgebras(L):
    """All subalgebras as RREF bases (m<=4, small p)."""
    p, m = L.p, L.m
    vecs = [v for v in L.elements() if any(v)]
    found = {(): None}
    frontier = [()]
    while frontier:
        nxt = []
        for B in frontier:
            for v in vecs:
                if B and span_contains(B, v, p, m):
                    continue
                C = rref(list(B) + [v], p, m)
                if C in found:
                    continue
                # closed under bracket?
                if all(span_contains(C, L.br(a, b), p, m) for a in C for b in C):
                    found[C] = None
                    nxt.append(C)
        frontier = nxt
    out = []
    for B in found:
        der = rref([L.br(a, b) for a in B for b in B] or [(0,) * m], p, m) if B else ()
        der = tuple(r for r in der if any(r))
        ideal = all(span_contains(B, L.br(e, b), p, m) for e in units(m) for b in B) if B else True
        out.append({"basis": B, "k": len(B), "d": len(B) - len(der), "normal": ideal})
    return out


# ------------------------------------------------------------- 2. lower bound
def diff_lines(L, X):
    p = L.p
    return {line_id(L.diff(x, y), p) for x, y in itertools.combinations(X, 2)}


def target_cov(N, succ=Fraction(2, 3)):
    """Smallest cov with (cov+1)/N >= succ."""
    return max(0, math.ceil(succ * N) - 1)


def q_union_bound(N, succ=Fraction(2, 3)):
    """Smallest q with C(q,2) >= target_cov: the lower bound's value."""
    t = target_cov(N, succ)
    q = max(1, math.isqrt(2 * t) - 2)
    while q * (q - 1) // 2 < t:
        q += 1
    return q


def exhaustive_cov(L, q, allowed):
    """Exact max over q-subsets containing 0 of #covered allowed lines."""
    els = [v for v in L.elements() if any(v)]
    zero = (0,) * L.m
    best, arg = -1, None
    for rest in itertools.combinations(els, q - 1):
        X = (zero,) + rest
        c = len(diff_lines(L, X) & allowed)
        if c > best:
            best, arg = c, X
            if best == q * (q - 1) // 2:
                break
    return best, arg


def greedy_cov(L, q, allowed, tries=400, seed=0, stop_at=10 ** 9):
    """Random-restart greedy: try to find q points covering many allowed lines."""
    rnd = random.Random(seed)
    els = [v for v in L.elements()]
    best, arg = -1, None
    for _ in range(tries):
        X = [(0,) * L.m]
        cov = set()
        while len(X) < q:
            cand = rnd.sample(els, min(len(els), 60))
            sc = []
            for c in cand:
                if c in X:
                    continue
                new = {line_id(L.diff(x, c), L.p) for x in X}
                sc.append((len((new - cov) & allowed), rnd.random(), c, new))
            sc.sort(reverse=True)
            _, _, c, new = sc[0]
            X.append(c)
            cov |= new
        val = len(cov & allowed)
        if val > best:
            best, arg = val, tuple(X)
            if best >= min(q * (q - 1) // 2, stop_at):
                break
    return best, arg


def lower_bound_check(L, which="all"):
    p, m = L.p, L.m
    zero = (0,) * m
    lines = {line_id(v, p) for v in L.elements() if v != zero}
    central = {v for v in lines if all(L.br(v, e) == zero for e in units(m))}
    allowed = lines if which == "all" else lines - central
    N = len(allowed)
    q_lb = q_union_bound(N)
    need = target_cov(N)
    # For q < q_lb the union bound already proves failure; only q_lb needs a set.
    # If a q_lb-point set covers >= need lines, the exact optimum q is q_lb.
    rows = []
    small = p ** m <= 27
    for q in (range(2, q_lb + 1) if small else [q_lb]):
        cap = q * (q - 1) // 2
        if small:
            cov, X = exhaustive_cov(L, q, allowed)
            method = "exhaustive (exact cov*)"
        else:
            cov, X = greedy_cov(L, q, allowed, tries=200)
            method = "exhibited set (lower bound on cov*)"
        assert len(diff_lines(L, X) & allowed) == cov and cov <= cap
        rows.append({"q": q, "C(q,2)": cap, "cov_found": cov, "method": method,
                     "success_of_set": str(min(Fraction(1), Fraction(cov + 1, N))),
                     "union_bound_success": str(min(Fraction(1), Fraction(cap + 1, N))),
                     "witness": [list(x) for x in X]})
    last = rows[-1]
    q_exact = q_lb if last["cov_found"] >= need else None
    return {"group": L.name, "prior": which + " lines", "N": N,
            "success_target": "2/3", "cov_needed": need,
            "q_lower_bound_from_union_bound": q_lb,
            "q_min_exact_for_this_prior": q_exact,
            "union_bound_attained": q_exact == q_lb, "rows": rows}


# ------------------------------------------------------------- 3. upper bound
def occupancy_excess(Q, M):
    """Exact law of E = Q - #occupied bins, Q balls uniform into M bins."""
    dist = {0: Fraction(1)}  # occupied count
    for _ in range(Q):
        nd = {}
        for d, pr in dist.items():
            if d:
                nd[d] = nd.get(d, 0) + pr * Fraction(d, M)
            if d < M:
                nd[d + 1] = nd.get(d + 1, 0) + pr * Fraction(M - d, M)
        dist = nd
    return {Q - d: pr for d, pr in dist.items()}


def gen_prob(e, d, p):
    """Pr[e iid uniform elements of a p-group H with d(H)=d generate H]."""
    if e < d:
        return Fraction(0)
    out = Fraction(1)
    for i in range(d):
        out *= 1 - Fraction(1, p ** (e - i))
    return out


def birthday_success(Q, p, m, k, d):
    if k == 0:
        return Fraction(1)
    M = p ** (m - k)
    return sum(pr * gen_prob(e, d, p) for e, pr in occupancy_excess(Q, M).items())


def closed_form_Q(p, m, eps):
    t = math.ceil(math.log(2 / eps, p) - 1e-12)
    ln = math.log(2 / eps)
    phi1 = p ** (m - 1) * max(2 * (1 + t), 8 * ln)
    return 5 * (m + t) + 16 * math.ceil(ln) + math.ceil(math.sqrt(2 * phi1))


def upper_bound_check(L, subs):
    p, m = L.p, L.m
    types = sorted({(s["k"], s["d"]) for s in subs})
    worst_Q = None
    Q = 1
    table = {}
    while True:
        vals = {kd: birthday_success(Q, p, m, *kd) for kd in types}
        worst = min(vals.values())
        if worst >= Fraction(2, 3):
            worst_Q = Q
            table = {"%d,%d" % kd: float(v) for kd, v in vals.items()}
            worst_type = min(vals, key=vals.get)
            break
        Q += 1
    eps = 1 / 3
    Qc = closed_form_Q(p, m, eps)
    succ_c = min(birthday_success(Qc, p, m, *kd) for kd in types)
    return {"group": L.name, "subgroup_types_(k,d)": [list(t) for t in types],
            "exact_min_Q_worst_case_success_ge_2/3": worst_Q,
            "worst_type_at_that_Q": list(worst_type),
            "success_by_type_at_that_Q": table,
            "closed_form_Q(eps=1/3)": Qc,
            "exact_worst_success_at_closed_form_Q": float(succ_c),
            "closed_form_valid": succ_c >= Fraction(2, 3)}


# ------------------------------------------------------------- 4. Monte Carlo
def lie_closure(L, gens):
    p, m = L.p, L.m
    B = rref([g for g in gens if any(g)] or [(0,) * m], p, m)
    B = tuple(r for r in B if any(r))
    while True:
        new = [L.br(a, b) for a in B for b in B]
        C = tuple(r for r in rref(list(B) + new or [(0,) * m], p, m) if any(r))
        if C == B:
            return B
        B = C


def coset_key(L, x, Hbasis):
    """Label of the left coset x*H: canonical min over x*h, h in H (small H)."""
    p, m = L.p, L.m
    pts = [(0,) * m]
    for b in Hbasis:
        pts = [L.add(a, L.scal(s, b)) for a in pts for s in range(p)]
    return min(L.bch(x, h) for h in pts)


def monte_carlo(L, H, Q, trials, seed):
    rnd = random.Random(seed)
    els = L.elements()
    Hb = H["basis"]
    labels = {}
    perm = {}
    ok = 0
    for _ in range(trials):
        X = [rnd.choice(els) for _ in range(Q)]
        cls = {}
        for x in X:
            key = coset_key(L, x, Hb)
            if key not in perm:  # random injective relabelling of cosets
                perm[key] = rnd.getrandbits(64)
            cls.setdefault(perm[key], []).append(x)
        gens = []
        for pts in cls.values():
            for y in pts[1:]:
                gens.append(L.diff(pts[0], y))
        out = lie_closure(L, gens)
        ok += out == Hb
    return ok / trials


# ------------------------------------------------------------- 5. base-K family
def base_K_counts(L, subs):
    """For ideals K: #H with K<H, [H:K]=p, split normal/non-normal, and rho_K."""
    p = L.p
    out = []
    for K in subs:
        if not K["normal"] or K["k"] == L.m:
            continue
        sup = [H for H in subs if H["k"] == K["k"] + 1
               and all(span_contains(H["basis"], b, p, L.m) for b in K["basis"])]
        nn = sum(1 for H in sup if not H["normal"])
        out.append({"K_dim": K["k"], "K_basis": [list(b) for b in K["basis"]],
                    "num_H": len(sup), "normal_H": len(sup) - nn, "nonnormal_H": nn,
                    "predicted_num_H_(p^(m-k)-1)/(p-1)": (p ** (L.m - K["k"]) - 1) // (p - 1)})
    return out


# ------------------------------------------------------------- 6. comparison
def B(d, a):
    return (d ** (d * (d - 1) // 2) * (a + 1) ** d) ** math.ceil(math.log2(d + 1))


def quantum_schedule1(c, m, g, p, eps=Fraction(1, 3)):
    t = 0  # the paper's t = ceil(log_p(3/eps)) (Section sec:recursion)
    while p ** t < 3 / eps:
        t += 1
    prod = 1
    for d in range(2, c + 1):
        prod *= B(d, g[d - 1])
    return c * (m + t) * prod


def num_subspaces(p, m):
    tot = 0
    for k in range(m + 1):
        num = den = 1
        for i in range(k):
            num *= p ** m - p ** i
            den *= p ** k - p ** i
        tot += num // den
    return tot


def ehk_copies(p, m, eps=Fraction(1, 3)):
    """Barnum-Knill / Childs (10.10) with F<=1/sqrt2: k >= 4 log2(r/eps), r <= #subspaces."""
    r = num_subspaces(p, m)
    return math.ceil(4 * (math.log2(r) + math.log2(1 / eps)))


def classical_lb(p, m, succ=Fraction(2, 3)):
    N = (p ** m - 1) // (p - 1)
    return q_union_bound(N, succ)


def isqrt_ceil(n):
    r = math.isqrt(n)
    return r if r * r == n else r + 1


def is_prime(n):
    if n < 2:
        return False
    for q in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        if n % q == 0:
            return n == q
    d, s = n - 1, 0
    while d % 2 == 0:
        d //= 2
        s += 1
    for a in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        x = pow(a, d, n)
        if x in (1, n - 1):
            continue
        for _ in range(s - 1):
            x = x * x % n
            if x == n - 1:
                break
        else:
            return False
    return True


def crossover(c, m, g):
    """Smallest prime p>=max(c+1,11) with classical LB > Schedule-1 quantum count.

    For p >= 11, t = ceil(log_p 9) = 1 at eps = 1/3, so the quantum count is constant in p.
    """
    Qq = quantum_schedule1(c, m, g, 11)  # t = 1 for every p >= 11
    # need C(q,2) >= ceil(2N/3)-1 to fail at q = Qq, i.e. q_lb > Qq:
    # q_lb > Qq  <=>  C(Qq,2) < ceil(2N/3)-1.  Solve for N, then p.
    need = Qq * (Qq - 1) // 2 + 1  # ceil(2N/3)-1 >= need
    # N >= 3(need+1)/2 ; N = (p^m-1)/(p-1) ~ p^(m-1)
    lo = max(c + 1, 11)
    target = 3 * (need + 1) // 2 + 1
    # integer root search for p^(m-1) ~ target
    p = max(lo, int(round(target ** (1 / (m - 1)))) // 2 if target < 10 ** 300 else lo)
    if target >= 10 ** 300:
        # high precision root
        p = integer_root(target, m - 1) // 2
        p = max(p, lo)
    # binary search on monotone predicate
    def ok(x):
        return classical_lb(x, m) > Qq
    hi = max(p, lo)
    while not ok(hi):
        hi *= 2
    lo2 = lo
    while lo2 < hi:
        mid = (lo2 + hi) // 2
        if ok(mid):
            hi = mid
        else:
            lo2 = mid + 1
    x = lo2
    while not is_prime(x):
        x += 1
    return x, Qq


def integer_root(n, k):
    x = 1 << ((n.bit_length() + k - 1) // k)
    while True:
        y = ((k - 1) * x + n // x ** (k - 1)) // k
        if y >= x:
            return x
        x = y


def comparison():
    fams = [("Heisenberg", 2, 3, [3, 1]),
            ("filiform class 3", 3, 4, [4, 2, 1]),
            ("free 2-generator class 3", 3, 5, [5, 3, 2]),
            ("Dixmier-Lister (class 3)", 3, 8, [8, 4, 2]),
            ("class-9 profile (rees_hsp_reduction.json)", 9, 19, [19, 17, 16, 14, 12, 9, 6, 3, 1])]
    rows = []
    for name, c, m, g in fams:
        p_x, Qq = crossover(c, m, g)
        lb = classical_lb(p_x, m)
        rows.append({"family": name, "c": c, "m": m, "g": g,
                     "quantum_schedule1_queries(p>=11,eps=1/3)": str(Qq),
                     "log2_quantum": round(math.log2(Qq), 2),
                     "crossover_prime": str(p_x) if p_x < 10 ** 30 else "2^%.2f" % math.log2(p_x),
                     "log2_crossover_prime": round(math.log2(p_x), 2),
                     "classical_lb_at_crossover_log2": round(math.log2(lb), 2),
                     "ehk_information_copies_at_crossover": ehk_copies(p_x, m)})
    return rows


def main():
    out = {"note": "research/audits/reviews/2026-11-02-rees-classical-lower-bound.md"}
    groups = [abelian(3, 3), heis(3), heis(5), filiform4(5), heis(7)]
    out["structure"] = [structure(L) for L in groups]
    subs = {L.name: subalgebras(L) for L in groups if L.m <= 4}
    out["subalgebra_census"] = {
        n: {"total": len(s),
            "by_(k,d,normal)": sorted([list(t) + [sum(1 for x in s if (x["k"], x["d"], x["normal"]) == t)]
                                       for t in {(x["k"], x["d"], x["normal"]) for x in s}])}
        for n, s in subs.items()}
    lbs = []
    for L in groups:
        lbs.append(lower_bound_check(L, "all"))
        if L.cls >= 2:
            lbs.append(lower_bound_check(L, "noncentral"))
    out["lower_bound"] = lbs
    print("lower bound done", flush=True)
    out["upper_bound"] = [upper_bound_check(L, subs[L.name]) for L in groups if L.name in subs]
    # Monte Carlo on real groups at the exact minimal Q
    mc = []
    for L in [heis(3), heis(5), filiform4(5)]:
        s = subs[L.name]
        ub = next(u for u in out["upper_bound"] if u["group"] == L.name)
        Q = ub["exact_min_Q_worst_case_success_ge_2/3"]
        rnd = random.Random(7)
        picks = [x for x in s if x["k"] in (1, 2)]
        rnd.shuffle(picks)
        for H in picks[:4]:
            pred = float(birthday_success(Q, L.p, L.m, H["k"], H["d"]))
            obs = monte_carlo(L, H, Q, 2000, seed=hash(H["basis"]) % 1000)
            mc.append({"group": L.name, "H_basis": [list(b) for b in H["basis"]],
                       "k": H["k"], "d": H["d"], "normal": H["normal"], "Q": Q,
                       "exact_success": round(pred, 4), "monte_carlo_2000": obs,
                       "within_4_sigma": abs(pred - obs) <= 4 * math.sqrt(pred * (1 - pred) / 2000) + 1e-9})
    out["monte_carlo"] = mc
    print("monte carlo done", flush=True)
    out["base_K"] = {n: base_K_counts(L, subs[n]) for L in groups if (n := L.name) in subs and L.cls >= 2}
    out["comparison"] = comparison()
    # sanity: class-9 count against the JSON's ceil(log2) = 1573
    q9 = quantum_schedule1(9, 19, [19, 17, 16, 14, 12, 9, 6, 3, 1], 11)
    out["class9_ceil_log2_check"] = {"computed": math.ceil(math.log2(q9)), "json": 1573}
    (HERE / "classical_lb.json").write_text(json.dumps(out, indent=1, default=str) + "\n")
    # assertions that make the run a check
    assert all(r["closed_form_valid"] for r in out["upper_bound"])
    assert all(r["within_4_sigma"] for r in mc)
    for L in groups:
        if L.name in out["base_K"]:
            for r in out["base_K"][L.name]:
                assert r["num_H"] == r["predicted_num_H_(p^(m-k)-1)/(p-1)"]
    print(json.dumps({k: out[k] for k in ("comparison", "class9_ceil_log2_check")}, indent=1))
    for r in lbs:
        print(r["group"], r["prior"], "N", r["N"], "q_LB", r["q_lower_bound_from_union_bound"],
              "q_exact", r["q_min_exact_for_this_prior"], "attained", r["union_bound_attained"])
    for r in out["upper_bound"]:
        print(r["group"], "Qmin", r["exact_min_Q_worst_case_success_ge_2/3"], r["worst_type_at_that_Q"],
              "closed", r["closed_form_Q(eps=1/3)"], r["exact_worst_success_at_closed_form_Q"])
    for r in mc:
        print(r["group"], r["k"], r["d"], r["normal"], r["exact_success"], r["monte_carlo_2000"])


if __name__ == "__main__":
    main()

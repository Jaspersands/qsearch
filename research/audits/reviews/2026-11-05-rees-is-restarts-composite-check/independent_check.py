"""Independent recheck of the composite-kappa restart counts (2026-11-05 composite note).

Written from scratch by the checker; it does not import composite_restarts.py.
It uses from theorems/rees_is_sde_solver.py only the algorithm pieces a real run
executes (PiParts.split, Classifier, lemma12, _kernel_vector, _row_reduce, _Restart,
is_sde_solve for the full-solver validation). Everything else is independent:

  * rho is computed from a fresh factorisation;
  * the anchor test T is an order test (x in <eta>^kappa iff x^(|eta|/g) = 1, g =
    gcd(kappa, |eta|)), not the solver's _anchor_witness;
  * eta is a generator of the target subgroup taken as a power of a fixed generator
    of H_pi (a different generator than PiParts.join returns), so the counts are
    checked to depend only on the subgroup <eta>;
  * the families A and C are rebuilt by new code;
  * the lattice maximum is a brute-force search over explicit subgroups (sets).

Run: nice -n 10 /opt/anaconda3/bin/python independent_check.py  (from the repo root).
"""
import random
import sys
from math import gcd

sys.path.insert(0, "/Users/jaspersands/Developer/qsearch")
from flint import fmpz  # noqa: E402
import theorems.rees_is_sde_solver as S  # noqa: E402


# ---------------------------------------------------------------- arithmetic

def factor_small(n):
    out, f = {}, 2
    while f*f <= n:
        while n % f == 0:
            out[f] = out.get(f, 0)+1
            n //= f
        f += 1
    if n > 1:
        out[n] = out.get(n, 0)+1
    return out


def val(n, q):
    v = 0
    while n % q == 0:
        n //= q
        v += 1
    return v


def my_rho(p, kappa):
    qs = factor_small(kappa)
    nu = sum(val(p-1, q) for q in qs)
    return nu - min(val((p-1)//kappa, q) for q in qs), nu


def my_rho_alt(p, kappa):
    qs = factor_small(kappa)
    return max(e+sum(val(p-1, r) for r in qs if r != q) for q, e in qs.items())


def find_prime(exps, start=1):
    base = 1
    for q, n in exps.items():
        base *= q**n
    k = start
    while True:
        if all(k % q for q in exps):
            p = k*base+1
            if fmpz(p).is_prime():
                return p
        k += 1


def hpi_data(p, kappa):
    qs = sorted(factor_small(kappa))
    n_pi = 1
    for q in qs:
        n_pi *= q**val(p-1, q)
    # a generator of H_pi: g^((p-1)/n_pi) for a primitive root g (found by testing)
    pf = factor_small_big(p-1, qs)
    g = 2
    while True:
        if all(pow(g, (p-1)//q, p) != 1 for q in pf):
            break
        g += 1
    return qs, n_pi, pow(g, (p-1)//n_pi, p)


def factor_small_big(n, known):
    """Prime factors of n where n / (known part) is assumed small enough to trial-divide,
    or otherwise prime-tested; enough for the test primes used here."""
    out = set()
    for q in known:
        if n % q == 0:
            out.add(q)
            while n % q == 0:
                n //= q
    f = 2
    while f*f <= n and f < 10**6:
        if n % f == 0:
            out.add(f)
            while n % f == 0:
                n //= f
        f += 1
    if n > 1:
        assert fmpz(n).is_prime(), "cofactor not prime; choose another p"
        out.add(n)
    return out


def elt_order_pi(x, p, n_pi, qs):
    n = n_pi
    for q in qs:
        while n % q == 0 and pow(x, n//q, p) == 1:
            n //= q
    return n


class Group:
    """Subgroups of the cyclic H_pi = <gH> by their order; eta(order) = gH^(n_pi/order)."""

    def __init__(self, p, kappa):
        self.p, self.kappa = p, kappa
        self.qs, self.n_pi, self.gH = hpi_data(p, kappa)
        self.parts = S.PiParts(p, kappa)
        assert self.parts.n_pi == self.n_pi

    def gen(self, order):
        assert self.n_pi % order == 0
        return pow(self.gH, self.n_pi//order, self.p)

    def order(self, x):
        return elt_order_pi(x, self.p, self.n_pi, self.qs)

    def elt(self, q, j):
        """The element of H_pi of order q^j, as a power of gH."""
        return pow(self.gH, self.n_pi//q**j, self.p)


def lcm(a, b):
    return a*b//gcd(a, b)


def my_test(G, order, gammas):
    """T at the subgroup of the given order: all gamma_k gamma_0^-1 in <eta>^kappa."""
    p = G.p
    g = gcd(G.kappa, order)
    g0inv = pow(gammas[0], -1, p)
    for x in gammas:
        y = x*g0inv % p
        assert pow(y, order, p) == 1
        if pow(y, order//g, p) != 1:
            return False
    return True


# ---------------------------------------------------------------- restart driver

def driver(G, prefix, level, *, collapse, use_join=False):
    """Restart loop of is_sde_solve on consecutive level-`level` Lemma 12 nodes covering
    `prefix` (the first computations of every real run, depth-first order)."""
    p, kappa, parts = G.p, G.kappa, G.parts
    reduced, rank = S._row_reduce(p, prefix)
    assert reduced == [tuple(c) for c in prefix]
    size = kappa**(level*(level-1)//2)*(rank+1)**level
    assert len(prefix) % size == 0
    indexed = list(enumerate(reduced))
    order, eta = 1, 1
    if collapse:
        alpha = S._kernel_vector(p, reduced[:rank+1])
        gammas = [parts.split(a)[0] for a in alpha if a]
        for x in gammas:
            order = lcm(order, G.order(x))
        eta = G.gen(order)
        if use_join:
            eta = 1
            for x in gammas:
                eta = parts.join(eta, x)
            assert G.order(eta) == order
        if my_test(G, order, gammas):
            return dict(runs=0, restarts=0, collapsed=True, final=order)
    restarts = 0
    while True:
        cl = S.Classifier(parts, eta)
        stats = dict(kernels=0, spread=False)
        try:
            for t in range(len(prefix)//size):
                S.lemma12(cl, indexed[t*size:(t+1)*size], level, stats)
        except S._Restart as r:
            new = lcm(order, G.order(r.element))
            assert new > order and new % order == 0
            order = new
            eta = parts.join(eta, r.element) if use_join else G.gen(order)
            assert G.order(eta) == order
            if collapse and my_test(G, order, gammas):
                return dict(runs=restarts+1, restarts=restarts, collapsed=True, final=order)
            restarts += 1
            continue
        return dict(runs=restarts+1, restarts=restarts, collapsed=False, final=order)


# ---------------------------------------------------------------- families (new code)

def my_chain(G, star):
    qs = G.qs
    nu_q = {q: val(G.p-1, q) for q in qs}
    e_q = {q: val(G.kappa, q) for q in qs}
    steps = [(star, j) for j in range(1, e_q[star]+1)]
    for q in qs:
        if q != star:
            steps += [(q, j) for j in range(1, nu_q[q]+1)]
    steps += [(star, j) for j in range(e_q[star]+1, nu_q[star]+1)]
    zs = [G.elt(q, j) for q, j in steps]
    # sanity: <z_1..z_i> has order growing by a prime each step and ends at H_pi
    o = 1
    for z in zs:
        o2 = lcm(o, G.order(z))
        assert o2 // o in qs
        o = o2
    assert o == G.n_pi
    return zs


def best_star(p, kappa):
    qs = factor_small(kappa)
    return min(qs, key=lambda q: (val(p-1, q)-qs[q], q))


def block(p, a, c):
    cols = [tuple(1 if i == j else 0 for i in range(a)) for j in range(a)]
    cols.append(tuple((-x) % p for x in c))
    return cols


def fam_a(G, a, star):
    p, kappa = G.p, G.kappa
    zs = my_chain(G, star)
    nblocks = kappa*(a+1)
    assert (nblocks-1)*a >= len(zs)-1
    rest = list(zs[1:])
    coeffs = [[zs[0]]+[1]*(a-1)]
    for _ in range(nblocks-1):
        c = rest[:a]
        rest = rest[a:]
        coeffs.append(c+[1]*(a-len(c)))
    cols = []
    for c in coeffs:
        cols += block(p, a, c)
    return cols


def fam_c3(G, a, star, length=None):
    """One good level-3 node (kappa >= 3): spine child 0, scaled copy child 1, free children."""
    p, kappa = G.p, G.kappa
    zs = my_chain(G, star)
    if length is not None:
        zs = zs[:length]
    x = zs[0]
    todo = list(zs[1:])

    def scaled(cols, s):
        return [tuple(v*s % p for v in col) for col in cols]

    def level2(y):
        c0 = block(p, a, [x]+[1]*(a-1))
        out = []
        for ch in range(kappa*(a+1)):
            out += scaled(c0, (-y) % p) if ch == 1 else c0
        return out
    spine = level2(x)
    out = spine+scaled(spine, (-x) % p)
    for _ in range(2, kappa**2*(a+1)):
        y = todo.pop(0) if todo else x
        out += level2(y)
    assert not todo, "chain longer than the 3-level slots"
    return out


# ---------------------------------------------------------------- lattice brute force

def lattice_max(p, kappa, anchors_mode="pairs"):
    """Max over anchors of the longest chain H_1 = S_0 < ... < S_R with T failing at
    every S_i, by brute force on explicit element sets. Returns (max R, #anchors)."""
    G = Group(p, kappa)
    n = G.n_pi
    elems = [pow(G.gH, i, p) for i in range(n)]
    divs = [d for d in range(1, n+1) if n % d == 0]
    sub = {d: set(pow(G.gen(d), i, p) for i in range(d)) for d in divs}
    kpow = {d: set(pow(x, kappa, p) for x in sub[d]) for d in divs}

    def fails(d, gammas):
        g0inv = pow(gammas[0], -1, p)
        return any(x*g0inv % p not in kpow[d] for x in gammas)

    def h1(gammas):
        o = 1
        for x in gammas:
            o = lcm(o, G.order(x))
        return o
    best, count = -1, 0
    anchors = [(g, 1) for g in elems]
    if anchors_mode == "triples" and n <= 64:
        anchors += [(g, h, 1) for g in elems for h in elems]
    for gammas in anchors:
        count += 1
        start = h1(gammas)
        if not fails(start, gammas):
            continue
        memo = {}

        def longest(d):
            if d in memo:
                return memo[d]
            r = 0
            for e in divs:
                if e != d and e % d == 0 and fails(e, gammas):
                    r = max(r, 1+longest(e))
            memo[d] = r
            return r
        best = max(best, longest(start))
    return best, count


# ---------------------------------------------------------------- main

def main():
    out = []
    say = lambda s: (print(s, flush=True), out.append(s))  # noqa: E731

    # 1. rho closed forms, special cases
    for kappa in (6, 10, 12, 15, 30, 4, 8, 9, 3):
        for p in range(3, 3000):
            if (p-1) % kappa or not fmpz(p).is_prime():
                continue
            r, nu = my_rho(p, kappa)
            assert r == my_rho_alt(p, kappa)
            qs = factor_small(kappa)
            if len(qs) == 1:
                assert r == list(qs.values())[0]
            else:
                assert 1+max(val(p-1, q) for q in qs) <= r <= nu
            if kappa == 6:
                assert r == 1+max(val(p-1, 2), val(p-1, 3))
    say("1. rho closed form = max form; prime power gives e; kappa=6 gives 1+max(nu2,nu3); "
        "1+max <= rho <= nu: OK for p < 3000")

    # 2. lattice brute force
    tot = 0
    for kappa in (6, 10, 12):
        for p in range(3, 700):
            if (p-1) % kappa or not fmpz(p).is_prime():
                continue
            mode = "triples"
            best, cnt = lattice_max(p, kappa, mode)
            tot += cnt
            r, _ = my_rho(p, kappa)
            assert best == r-1, (p, kappa, best, r)
    say(f"2. brute-force lattice: max failing chain = rho-1 for kappa in (6,10,12), p < 700; "
        f"{tot} anchors")

    # 3. driver validation against the full solver (kappa = 2, 3: full arity is small)
    for p, kappa, a in ((1459, 3, 1), (163, 3, 1), (7681, 2, 2), (257, 2, 2)):
        G = Group(p, kappa)
        star = best_star(p, kappa)
        pre = fam_a(G, a, star)
        need = S.columns_required(p, kappa, a)
        rng = random.Random(1)
        cols = pre+[tuple(rng.randrange(1, p) for _ in range(a)) for _ in range(need-len(pre))]
        for collapse in (False, True):
            w = S.is_sde_solve(p, kappa, cols, collapse=collapse)
            d = driver(G, pre, 2, collapse=collapse)
            dj = driver(G, pre, 2, collapse=collapse, use_join=True)
            assert (w.restarts, w.collapsed) == (d["restarts"], d["collapsed"]) \
                == (dj["restarts"], dj["collapsed"]), (p, kappa, collapse, w, d)
        r, nu = my_rho(p, kappa)
        say(f"3. full solver = driver at p={p} kappa={kappa} a={a}: default {nu+1} runs, "
            f"variant {r} runs")

    # 4. family A and family C at composite kappa
    cases = [(6, {2: 1, 3: 20}), (6, {2: 15, 3: 15}), (6, {2: 40, 3: 2}), (6, {2: 3, 3: 3}),
             (6, {2: 1, 3: 1}), (6, {2: 2, 3: 1}), (10, {2: 30, 5: 1}), (10, {2: 6, 5: 6}),
             (10, {2: 1, 5: 20}), (10, {2: 1, 5: 1}), (12, {2: 2, 3: 25}),
             (12, {2: 20, 3: 10}), (12, {2: 3, 3: 3}), (12, {2: 2, 3: 1})]
    for kappa, exps in cases:
        p = find_prime(exps)
        G = Group(p, kappa)
        r, nu = my_rho(p, kappa)
        star = best_star(p, kappa)
        a = 1
        while (kappa*(a+1)-1)*a < nu-1:
            a += 1
        pre = fam_a(G, a, star)
        dv = driver(G, pre, 2, collapse=True)
        dd = driver(G, pre, 2, collapse=False)
        dvj = driver(G, pre, 2, collapse=True, use_join=True)
        assert dv["runs"] == dvj["runs"] == r, (kappa, p, dv, r)
        assert dd["runs"] == nu+1 and dd["final"] == G.n_pi and not dd["collapsed"]
        # exactness: variant ends by collapse, or with eta = H_pi (no later trigger possible)
        assert dv["collapsed"] or dv["final"] == G.n_pi
        line = (f"4. kappa={kappa} p={p} ({p.bit_length()} bits) nu={nu} rho={r}: "
                f"A(a={a}) variant {dv['runs']} default {dd['runs']}")
        if nu-1 <= kappa**2*2-2:
            prec = fam_c3(G, 1, star)
            cv = driver(G, prec, 3, collapse=True)
            cd = driver(G, prec, 3, collapse=False)
            cvj = driver(G, prec, 3, collapse=True, use_join=True)
            assert cv["runs"] == cvj["runs"] == r and (cv["collapsed"] or cv["final"] == G.n_pi)
            assert cd["runs"] >= r+1
            if r < nu:
                assert cd["runs"] >= r+2
            line += f"; C(a=1, level 3) variant {cv['runs']} default {cd['runs']}"
        if nu-1 <= kappa**2*3-2 and kappa == 6:
            prec2 = fam_c3(G, 2, star)
            cv2 = driver(G, prec2, 3, collapse=True)
            assert cv2["runs"] == r
            line += f"; C(a=2) variant {cv2['runs']}"
        say(line)

    # 5. every l* in family A gives rho_{l*}
    p = find_prime({2: 8, 3: 3, 5: 2})
    G = Group(p, 30)
    got = {}
    for star in (2, 3, 5):
        e = val(30, star)
        rs = e+sum(val(p-1, q) for q in (2, 3, 5) if q != star)
        d = driver(G, fam_a(G, 2, star), 2, collapse=True)
        assert d["runs"] == rs
        got[star] = d["runs"]
    say(f"5. kappa=30 p={p}: family A with each l* gives {got}; rho = {my_rho(p, 30)[0]}")

    # 6. random prefixes: Theorem A upper bound, and default <= nu+1
    rng = random.Random(7)
    worst = {}
    for kappa, exps in ((6, {2: 3, 3: 2}), (10, {2: 2, 5: 2}), (12, {2: 3, 3: 2})):
        p = find_prime(exps)
        G = Group(p, kappa)
        r, nu = my_rho(p, kappa)
        hp = [pow(G.gH, i, p) for i in range(G.n_pi)]
        mx = 0
        for trial in range(150):
            a = rng.choice((1, 2))
            cols = []
            for _ in range(kappa*(a+1)):
                c = [rng.choice(hp)*pow(rng.randrange(1, p), kappa, p) % p for _ in range(a)]
                cols += block(p, a, c)
            dv = driver(G, cols, 2, collapse=True)
            dd = driver(G, cols, 2, collapse=False)
            assert dv["runs"] <= r and dd["runs"] <= nu+1
            mx = max(mx, dv["runs"])
        worst[(kappa, p)] = (mx, r)
    say(f"6. random level-2 prefixes (150 per case): variant runs <= rho; max seen vs rho: {worst}")
    say("ALL OK")
    return out


if __name__ == "__main__":
    main()

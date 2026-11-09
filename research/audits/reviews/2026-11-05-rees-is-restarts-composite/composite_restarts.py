"""Restart counts of the Ivanyos-Santha classifier at composite kappa (2026-11-05 composite note).

Report: research/audits/reviews/2026-11-05-rees-is-restarts-composite.md.

Contents
- rho(p, kappa): the sharp run bound nu - min_l v_l((p-1)/kappa) of the collapse
  variant (Theorem A of the report); per_anchor_bound(...): its per-anchor form.
- chain(...), family_a(...), family_b(...): the explicit columns of Theorem B.
- prefix_run(...): the restart loop of is_sde_solve (default or collapse=True),
  run on the first level-2 nodes of the input with the solver's own Classifier,
  lemma12, _anchor_split and _anchor_witness. In the real solver these nodes are
  the first computations of every run (depth-first order), so every restart this
  driver records is a restart of the full solver (report, Lemma 3).
- lattice_max_restarts(...): exhaustive longest failing chain over the subgroup
  lattice of H_pi, with the solver's _anchor_witness as the test (Theorem A, exact check).

Run: nice -n 10 /opt/anaconda3/bin/python composite_restarts.py   (prints ALL OK)
"""
import sys
from math import gcd

REPO = "/Users/jaspersands/Developer/qsearch"
if REPO not in sys.path:
    sys.path.insert(0, REPO)

from flint import fmpz  # noqa: E402

from theorems.rees_is_sde_solver import (  # noqa: E402
    Classifier, PiParts, _Restart, _anchor_split, _anchor_witness, _kernel_vector,
    _prime_divisors, _row_reduce, lemma12)


# ---------------------------------------------------------------- arithmetic

def vval(n, ell):
    v = 0
    while n % ell == 0:
        n //= ell
        v += 1
    return v


def nus(p, kappa):
    """{l: (nu_l, e_l)} with nu_l = v_l(p-1), e_l = v_l(kappa), l over the primes of kappa."""
    return {ell: (vval(p-1, ell), vval(kappa, ell)) for ell in _prime_divisors(kappa)}


def nu(p, kappa):
    return sum(n for n, _ in nus(p, kappa).values())


def rho(p, kappa):
    """Sharp worst-case run count of the collapse variant: nu - min_l v_l((p-1)/kappa)."""
    data = nus(p, kappa)
    return sum(n for n, _ in data.values()) - min(n-e for n, e in data.values())


def rho_star(p, kappa, ell_star):
    """e_{l*} + sum_{l != l*} nu_l: the count attained by the family built on l*."""
    data = nus(p, kappa)
    return data[ell_star][1]+sum(n for ell, (n, _) in data.items() if ell != ell_star)


def best_ell_star(p, kappa):
    data = nus(p, kappa)
    return min(data, key=lambda ell: (data[ell][0]-data[ell][1], ell))


def sylow_generators(p, kappa):
    """{l: g_l} with g_l of exact order l^{nu_l} (search; used only to build families)."""
    out = {}
    for ell, (n, _) in nus(p, kappa).items():
        x = 2
        while pow(x, (p-1)//ell, p) == 1:
            x += 1
        out[ell] = pow(x, (p-1)//ell**n, p)
        assert pow(out[ell], ell**(n-1), p) != 1 and pow(out[ell], ell**n, p) == 1
    return out


def chain(p, kappa, ell_star):
    """z_1, ..., z_nu in H_pi: each <z_1..z_i> has prime index in <z_1..z_{i+1}>.

    Order: the l*-part up to l*^{e*} (z_1 = omega*, of order l*), then every other prime
    to its full Sylow part, then the l*-part from l*^{e*} up to l*^{nu*}.
    """
    data, gens = nus(p, kappa), sylow_generators(p, kappa)
    n_star, e_star = data[ell_star]
    steps = [(ell_star, j) for j in range(1, e_star+1)]
    for ell in sorted(data):
        if ell != ell_star:
            steps += [(ell, j) for j in range(1, data[ell][0]+1)]
    steps += [(ell_star, j) for j in range(e_star+1, n_star+1)]
    return [pow(gens[ell], ell**(data[ell][0]-j), p) for ell, j in steps]


# ---------------------------------------------------------------- the families

def _block(p, a, coefficients):
    """a+1 columns in F_p^a whose first-free-column kernel vector is (coefficients, 1)."""
    assert len(coefficients) == a
    basis = [tuple(int(i == j) for i in range(a)) for j in range(a)]
    return basis+[tuple((-c) % p for c in coefficients)]


def family_a_slots(kappa, a):
    """Chain slots after z_1 inside the first level-2 node (kappa(a+1) blocks of a+1)."""
    return (kappa*(a+1)-1)*a


def family_a(p, kappa, a, ell_star, length=None):
    """First level-2 node of family A: block 0 = anchor (z_1, 1, ..., 1 | 1), then z_2, z_3, ...

    `length` = number of chain elements placed (default: all nu of them). Unused slots get 1.
    Returns the kappa (a+1)^2 columns of that node; the full input continues with any
    nonzero columns (e.g. repeats of e_1) up to the solver's arity.
    """
    z = chain(p, kappa, ell_star)
    length = len(z) if length is None else length
    if length-1 > family_a_slots(kappa, a):
        raise ValueError("not enough slots in the first level-2 node")
    rest = z[1:length]
    blocks = [[z[0]]+[1]*(a-1)]
    for _ in range(kappa*(a+1)-1):
        take, rest = rest[:a], rest[a:]
        blocks.append(take+[1]*(a-len(take)))
    cols = [c for coeffs in blocks for c in _block(p, a, coeffs)]
    assert len(cols) == kappa*(a+1)**2
    return cols


def family_b(p, kappa, ell_star, nodes):
    """First `nodes` level-2 nodes of family B (a = 1, kappa >= 3).

    Node t: child 0 = (1, -x) and children 2.. = (1, -x), whose kernel is (x, 1);
    child 1 = (c, -c x) = c * child 0 with c = -z_{t+2}, so the merge kernel is (z_{t+2}, 1, 0..).
    x = z_1 = omega*. Every level-1 coefficient is x or 1; the chain only appears at level 2.
    """
    z = chain(p, kappa, ell_star)
    x = z[0]
    cols = []
    for t in range(nodes):
        y = z[t+1] if t+1 < len(z) else 1
        c = (-y) % p
        for child in range(2*kappa):
            if child == 1:
                cols += [(c,), ((-c*x) % p,)]
            else:
                cols += [(1,), ((-x) % p,)]
    return cols


# ---------------------------------------------------------------- the prefix driver

def node_size(kappa, rank, level):
    """B_level = kappa^{level(level-1)/2} (rank+1)^level, the column count of a Lemma 12 node."""
    return kappa**(level*(level-1)//2)*(rank+1)**level


def prefix_run(p, kappa, prefix, *, collapse, spread=False, level=2, max_runs=10**4):
    """The restart loop of is_sde_solve on the level-`level` nodes covering `prefix`.

    Mirrors is_sde_solve line by line: same anchor (kernel of columns 0..rank), same
    eta_1, same anchor test at every trigger, restart counted only when the test fails.
    Each run evaluates lemma12(level) on consecutive blocks of B_level columns; these
    are the first computations of the real run when level < kappa and the prefix has at
    most kappa^level (rank+1) such blocks (depth-first order of Lemma 12). Returns a dict
    with restarts, runs, collapsed, completed (prefix finished without trigger), the eta
    after every join (etas) and the eta of every run (run_etas).
    """
    parts = PiParts(p, kappa)
    reduced, rank = _row_reduce(p, prefix)
    assert reduced == [tuple(c) for c in prefix], "family columns are already row-reduced"
    size = node_size(kappa, rank, level)
    assert len(prefix) % size == 0
    indexed = list(enumerate(reduced))
    eta, combination, collapsed, anchor = 1, None, False, None
    if collapse:
        anchor, eta = _anchor_split(parts, _kernel_vector(p, reduced[:rank+1], spread))
        combination = _anchor_witness(parts, eta, anchor)
        if combination is not None:
            return dict(restarts=0, runs=0, collapsed=True, completed=False, etas=[eta],
                        run_etas=[])
    restarts, etas, run_etas = 0, [eta], []
    for _ in range(max_runs):
        run_etas.append(eta)
        classifier = Classifier(parts, eta)
        stats = dict(kernels=0, spread=spread)
        try:
            for t in range(len(prefix)//size):
                lemma12(classifier, indexed[t*size:(t+1)*size], level, stats)
        except _Restart as restart:
            eta = parts.join(eta, restart.element)
            etas.append(eta)
            if collapse and _anchor_witness(parts, eta, anchor) is not None:
                return dict(restarts=restarts, runs=restarts+1, collapsed=True,
                            completed=False, etas=etas, run_etas=run_etas)
            restarts += 1
            continue
        return dict(restarts=restarts, runs=restarts+1, collapsed=False, completed=True,
                    etas=etas, run_etas=run_etas)
    raise RuntimeError("no termination")


# ---------------------------------------------------------------- family C (any rank, any p)

def family_c_slots(kappa, a, level):
    """Chain slots of a good level-`level` node: s_3 = n_3 - 2, s_L = (n_L - 1) s_{L-1}."""
    def n(L):
        return kappa**(L-1)*(a+1)
    if level == 2:
        return 1
    s = n(3)-2
    for L in range(4, level+1):
        s *= n(L)-1
    return s


def family_c(p, kappa, a, ell_star, level, children=None, length=None):
    """A good level-`level` node (report, Theorem B(iii)), or its first `children` children.

    Level 2 (merge coefficient y): child 0 = block (x, 1, ..., 1 | 1), child 1 = (-y) * child 0,
    other children = child 0. A spine level-2 node has y = x; a free one takes the next chain
    element (or x when the chain is used up). Level L >= 3: child 0 = good level-(L-1) node
    whose own level-2 child 0 is a spine node, child 1 = (-x) * child 0 (scaled copy),
    children 2.. = good level-(L-1) nodes. x = z_1 = omega*, the anchor is block 0.
    """
    z = chain(p, kappa, ell_star)
    length = len(z) if length is None else length
    x, todo = z[0], list(z[1:length])

    def scale(cols, s):
        return [tuple(c*s % p for c in col) for col in cols]

    def build(L, spine):
        if L == 2:
            y = x if spine or not todo else todo.pop(0)
            child0 = _block(p, a, [x]+[1]*(a-1))
            out = []
            for child in range(kappa*(a+1)):
                out += scale(child0, -y) if child == 1 else child0
            return out
        first = build(L-1, True)
        out = first+scale(first, -x)
        count = kappa**(L-1)*(a+1) if children is None or L < level else children
        for _ in range(2, count):
            out += build(L-1, False)
        return out
    cols = build(level, True)
    if todo:
        raise ValueError("chain longer than the slots used")
    return cols




def full_solver_trace(p, kappa, columns, **kw):
    """is_sde_solve on the full input, with the eta of every run recorded (Classifier.__init__)."""
    import theorems.rees_is_sde_solver as solver
    log, original = [], solver.Classifier.__init__

    def init(self, parts, eta=1):
        log.append(eta)
        original(self, parts, eta)
    solver.Classifier.__init__ = init
    try:
        w = solver.is_sde_solve(p, kappa, columns, **kw)
    finally:
        solver.Classifier.__init__ = original
    assert solver.verify(p, kappa, columns, w.s)
    return w, log


def full_input(p, kappa, prefix, rank, seed=0):
    """prefix + seeded random nonzero columns up to the solver's arity."""
    import random
    from theorems.rees_is_sde_solver import columns_required
    rng = random.Random(seed)
    need = columns_required(p, kappa, rank)
    assert need >= len(prefix)
    return list(prefix)+[tuple(rng.randrange(1, p) for _ in range(rank))
                         for _ in range(need-len(prefix))]


def cross_check(p, kappa, prefix, rank, *, spread=False, early_exit=True, seed=0):
    """Full solver vs prefix driver: same restarts, same collapsed flag, same run etas."""
    cols = full_input(p, kappa, prefix, rank, seed)
    out = {}
    for collapse in (False, True):
        w, log = full_solver_trace(p, kappa, cols, collapse=collapse, spread=spread,
                                   early_exit=early_exit)
        pr = prefix_run(p, kappa, prefix, collapse=collapse, spread=spread)
        assert w.restarts == pr["restarts"], (p, kappa, collapse, w.restarts, pr["restarts"])
        assert w.collapsed == pr["collapsed"]
        assert log[:len(pr["run_etas"])] == pr["run_etas"]
        if pr["collapsed"]:
            assert log == pr["run_etas"]
        out[collapse] = (w.restarts, w.collapsed, len(log))
    return out


# ---------------------------------------------------------------- lattice check

def pi_generator(p, kappa):
    out = 1
    for g in sylow_generators(p, kappa).values():
        out = out*g % p
    return out


def _divisors(n):
    return [d for d in range(1, n+1) if n % d == 0]


def anchor_from_pi_parts(parts, gammas):
    return [(k, (g % parts.p, 1)) for k, g in enumerate(gammas)]


def lattice_max_restarts(p, kappa, gammas, _cache={}):
    """Longest chain H_1 = S_0 < S_1 < ... < S_R in H_pi with the anchor test failing at
    every S_i (i >= 0): the most restarts any trigger sequence can force on this anchor.

    Returns None when the test succeeds at H_1 (the variant makes no run).
    """
    key = (p, kappa)
    if key not in _cache:
        parts = PiParts(p, kappa)
        n = parts.n_pi
        gen = pi_generator(p, kappa)
        divs = [d for d in range(1, n+1) if n % d == 0]
        _cache.clear()
        _cache[key] = (parts, n, {h: pow(gen, n//h, p) for h in divs})
    parts, n, gens = _cache[key]
    anchor = anchor_from_pi_parts(parts, gammas)
    eta1 = 1
    for g in gammas:
        eta1 = parts.join(eta1, g)
    h1 = parts.order(eta1)
    fails = {h: _anchor_witness(parts, gens[h], anchor) is None
             for h in gens if h % h1 == 0}
    if not fails[h1]:
        return None
    memo = {}

    def f(h):
        if h not in memo:
            memo[h] = max([1+f(k) for k in fails if k != h and k % h == 0 and fails[k]],
                          default=0)
        return memo[h]
    return f(h1)


def per_anchor_bound(p, kappa, gammas):
    """Closed form of lattice_max_restarts (report, Theorem A(ii))."""
    parts = PiParts(p, kappa)
    data = nus(p, kappa)

    def comp(x, ell):
        return parts._component(x, ell)

    def lv(x, ell):
        return vval(parts.order(comp(x, ell)), ell) if comp(x, ell) != 1 else 0
    h1 = {ell: max(lv(g, ell) for g in gammas) for ell in data}
    g0 = gammas[0]
    delta = {ell: max(lv(g*pow(g0, -1, p) % p, ell) for g in gammas) for ell in data}
    failing = [ell for ell in data if delta[ell] and h1[ell] <= delta[ell]+data[ell][1]-1]
    if not failing:
        return None
    return max(sum(data[ell][0]-h1[ell] for ell in data if ell != s)
               + min(data[s][0], delta[s]+data[s][1]-1)-h1[s] for s in failing)


# ---------------------------------------------------------------- primes

def find_prime(kappa, exps, start=1, limit=10**6):
    """Least prime p = 1 + prod l^{exps[l]} * q with q >= start coprime to kappa."""
    base = 1
    for ell, k in exps.items():
        base *= ell**k
    assert base % kappa == 0
    for q in range(start, start+limit):
        if gcd(q, kappa) == 1 and fmpz(base*q+1).is_prime():
            return base*q+1
    raise ValueError


# ---------------------------------------------------------------- main sweep

def sweep_lattice(kappas=(6, 10, 12, 15, 30), pmax=4000, verbose=True, pairs=None):
    """Exhaustive check of Theorem A on all primes p < pmax with kappa | p-1:
    every anchor (gamma, 1) with gamma in H_pi, and every ordered pair (gamma, gamma', 1)
    when n_pi <= 60."""
    count = 0
    for kappa in kappas:
        for p in range(kappa+1, pmax, kappa):
            if not fmpz(p).is_prime():
                continue
            parts = PiParts(p, kappa)
            n = parts.n_pi
            gen = pi_generator(p, kappa)
            elems = [pow(gen, i, p) for i in range(n)]
            anchors = [[g, 1] for g in elems]
            if n <= 60:
                anchors += [[g, h, 1] for g in elems for h in elems]
            best = 0
            for gam in anchors:
                lat = lattice_max_restarts(p, kappa, gam)
                assert lat == per_anchor_bound(p, kappa, gam), (p, kappa, gam)
                if lat is not None:
                    best = max(best, lat)
                count += 1
            assert best == rho(p, kappa)-1, (p, kappa, best, rho(p, kappa))
            if pairs is not None:
                pairs.append((p, kappa))
            if verbose:
                print(f"lattice kappa={kappa} p={p} n_pi={n} nu={nu(p, kappa)} "
                      f"rho={rho(p, kappa)} max_restarts={best} anchors={len(anchors)}")
    return count


def family_cases():
    """(kappa, p) test cases with large kappa-smooth parts of p-1."""
    out = []
    specs = {6: [{2: 10, 3: 1}, {2: 4, 3: 6}, {2: 30, 3: 1}, {2: 60, 3: 2}, {2: 1, 3: 40}],
             10: [{2: 20, 5: 1}, {2: 2, 5: 12}, {2: 50, 5: 3}],
             12: [{2: 12, 3: 1}, {2: 2, 3: 20}, {2: 40, 3: 8}],
             15: [{3: 10, 5: 1}, {3: 1, 5: 9}, {3: 30, 5: 5}],
             30: [{2: 8, 3: 3, 5: 2}, {2: 30, 3: 1, 5: 1}, {2: 1, 3: 12, 5: 10}]}
    for kappa, rows in specs.items():
        for exps in rows:
            out.append((kappa, find_prime(kappa, exps)))
    return out


def check_family(kappa, p, verbose=True):
    data = nus(p, kappa)
    n_total, r = nu(p, kappa), rho(p, kappa)
    star = best_ell_star(p, kappa)
    assert rho_star(p, kappa, star) == r
    results = {}
    # The variant collapses on the chain iff the l*-part can still grow past l*^{e*};
    # otherwise the chain ends at eta = H_pi and the last run completes.
    grows = data[star][0] > data[star][1]
    # Family A, smallest a with room for the whole chain (exact default count nu).
    a = 1
    while family_a_slots(kappa, a) < n_total-1:
        a += 1
    pre = family_a(p, kappa, a, star)
    for spread in (False, True):
        v = prefix_run(p, kappa, pre, collapse=True, spread=spread)
        d = prefix_run(p, kappa, pre, collapse=False, spread=spread)
        assert v["runs"] == r and v["collapsed"] == grows, (kappa, p, v["runs"], r)
        assert d["runs"] == n_total+1 and d["completed"], (kappa, p, d["runs"], n_total)
        results[("A", spread)] = (v["runs"], d["runs"])
    # Family B (a = 1): chain only through level-2 merges; needs r - 1 <= 2 kappa^2 - 1.
    nodes = min(r+1, 2*kappa*kappa)
    if r <= 2*kappa*kappa:
        pre = family_b(p, kappa, star, nodes)
        v = prefix_run(p, kappa, pre, collapse=True)
        assert v["runs"] == r and v["collapsed"] == grows, (kappa, p, v["runs"], r)
        results["B"] = v["runs"]
    if verbose:
        print(f"family kappa={kappa} p={p} ({p.bit_length()} bits) nu_l,e_l={data} nu={n_total} "
              f"rho={r} l*={star} a_A={a} A(variant,default)={results[('A', False)]} "
              f"B(variant)={results.get('B')}")
    return results


def cross_checks(verbose=True):
    """Full solver (is_sde_solve) vs prefix driver where the full run is feasible."""
    rows = []
    for p, kappa, a in ((65537, 2, 3), (786433, 2, 3), (7681, 2, 2), (40961, 2, 3),
                        (163, 3, 1), (1459, 3, 1), (39367, 3, 2), (17, 4, 1), (97, 4, 1),
                        (193, 4, 1)):
        pre = family_a(p, kappa, a, best_ell_star(p, kappa))
        # early_exit=False forces full accumulation in all nu+1 default runs; at kappa = 4
        # (65536 columns) that exceeds the time budget on the loaded machine, so kappa = 4
        # is cross-checked in the default setting only.
        settings = ((False, True),) if kappa == 4 else ((False, True), (True, False))
        for spread, ee in settings:
            out = cross_check(p, kappa, pre, a, spread=spread, early_exit=ee)
            assert out[False][0] == nu(p, kappa) and out[True][0]+1 == rho(p, kappa)
            rows.append(("A", p, kappa, a, spread, ee, out))
            if verbose:
                print("cross-check", rows[-1], flush=True)
    for p in (163, 1459, 39367):
        out = cross_check(p, 3, family_b(p, 3, 3, 18), 1)
        rows.append(("B", p, 3, 1, False, True, out))
        if verbose:
            print("cross-check", rows[-1], flush=True)
    return rows


def family_c_checks(verbose=True):
    for kappa, p in family_cases():
        star, r = best_ell_star(p, kappa), rho(p, kappa)
        pre = family_c(p, kappa, 1, star, 3)
        v = prefix_run(p, kappa, pre, collapse=True, level=3)
        d = prefix_run(p, kappa, pre, collapse=False, level=3)
        assert v["runs"] == r and d["runs"] >= r+1
        if verbose:
            print(f"family C level 3 kappa={kappa} p={p} rho={r} variant runs={v['runs']} "
                  f"default runs={d['runs']} (nu+1={nu(p, kappa)+1})")
    for exps in ({2: 75, 3: 1}, {2: 72, 3: 3}):
        p = find_prime(6, exps)
        pre = family_c(p, 6, 1, best_ell_star(p, 6), 4, children=3)
        v = prefix_run(p, 6, pre, collapse=True, level=3)
        d = prefix_run(p, 6, pre, collapse=False, level=3)
        assert v["runs"] == rho(p, 6) and d["runs"] >= rho(p, 6)+1
        if verbose:
            print(f"family C level 4 (3 children) kappa=6 p={p} nu={nu(p, 6)} rho={rho(p, 6)} "
                  f"variant runs={v['runs']} default runs={d['runs']}")


def every_ell_star(verbose=True):
    p = find_prime(30, {2: 8, 3: 3, 5: 2})
    out = {}
    for star in (2, 3, 5):
        out[star] = prefix_run(p, 30, family_a(p, 30, 1, star), collapse=True)["runs"]
        assert out[star] == rho_star(p, 30, star)
    if verbose:
        print(f"every l* at kappa=30 p={p}: runs {out}")
    return out


if __name__ == "__main__":
    pairs = []
    print("lattice anchors checked:", sweep_lattice(pairs=pairs), "pairs:", len(pairs))
    every_ell_star()
    for kappa, p in family_cases():
        check_family(kappa, p)
    cross_checks()
    family_c_checks()
    print("ALL OK")

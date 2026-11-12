"""Referee checks (exact integers) for Lemma E, Step 2 and Step 3 of Theorem A in
../2026-11-12-rees-h3z-infinite-index.md.  Reuses the induced polycyclic basis class Sub from
../2026-11-12-rees-h3z-infinite-index/h3z_struct.py (read-only import).
Checks can only falsify; nothing here proves a statement for other instances.
Usage: nice -n 19 /opt/anaconda3/bin/python struct_referee.py [maxb] [trials] [seed]
"""
import sys, os, random, itertools
from math import gcd
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                '..', '2026-11-12-rees-h3z-infinite-index'))
from h3z_struct import Sub, mul, inv, pw, comm, ONE

def C2(t): return t * (t - 1) // 2
def bl(x): return abs(x).bit_length()

def rank(H): return (H.X is not None) + (H.Y is not None)

def phi_lift(g, e):
    """g in A (e | a)  ->  (alpha, beta, gamma) with g = x^{e alpha} y^beta z^gamma."""
    assert g[0] % e == 0
    return (g[0] // e, g[1], g[2] - g[0] * g[1])

def elt(al, be, ga, e):
    """x^{e al} y^{be} z^{ga} as a triple."""
    return mul(mul(pw((1, 0, 0), e * al), pw((0, 1, 0), be)), pw((0, 0, 1), ga))

def L_basis(H):
    """Generators of L = {(al,be,ga): x^{e al} y^be z^ga in H} (Kuperberg's Z^3 instance)."""
    e = H.e(); X, Y = H.X, H.Y
    gens = [(0, 0, e)]
    if X is not None:
        i0 = e // gcd(e, X[0]); gens.append(phi_lift(pw(X, i0), e))
    if Y is not None: gens.append(phi_lift(Y, e))
    return gens

def check_instance(gens, b, stats, rng):
    H = Sub(gens); e = H.e()
    if e == 0: return
    r = rank(H)
    # Step 2: phi is a homomorphism A -> Z^2 x Z_e with kernel <z^e> (signed, random)
    for _ in range(5):
        p = tuple(rng.randint(-40, 40) for _ in range(3)); q = tuple(rng.randint(-40, 40) for _ in range(3))
        g, h = elt(*p, e), elt(*q, e)
        lhs = phi_lift(mul(g, h), e); assert lhs[:2] == (p[0] + q[0], p[1] + q[1])
        assert (lhs[2] - p[2] - q[2]) % e == 0, 'phi not a homomorphism'
        # F hides L: F(p) = F(q) <=> g^{-1} h in H <=> q - p in L  (test via membership of difference)
        d = tuple(qq - pp for pp, qq in zip(p, q))
        assert H.contains(mul(inv(g), h)) == H.contains(elt(*d, e)), 'F does not hide L'
    Lb = L_basis(H)
    for v in Lb: assert H.contains(elt(*v, e))
    stats['L_maxbits_over_b'] = max(stats.get('L_maxbits_over_b', 0), max(bl(c) for v in Lb for c in v) / b)
    if r == 2:
        idx = abs(H.X[0] * H.Y[1]) * e        # [G:H] = [Z^2:pi(H)] * e for induced basis
        stats['rk2'] = stats.get('rk2', 0) + 1
        stats['rk2_index_over_2^(4b+2)_max'] = max(stats.get('rk2_index_over_2^(4b+2)_max', 0), idx / 2 ** (4 * b + 2))
        assert idx < 2 ** (4 * b + 2), ('rk2 index bound', gens, idx)
    if r == 1:
        stats['rk1'] = stats.get('rk1', 0) + 1
        u = H.X if H.X is not None else H.Y
        dd = gcd(u[0], u[1]); v = (u[0] // dd, u[1] // dd)
        # direction from S (any element of H cap A with nonzero projection)
        w = pw(u, e // gcd(e, u[0]) if u[0] else 1); dw = gcd(w[0], w[1])
        assert (w[0] // dw, w[1] // dw) == v
        assert all(abs(c) < 2 ** b for c in v)
        def iota(t, s): return (t * v[0], t * v[1], s + C2(t) * v[0] * v[1])
        def iota_inv(g):
            t = g[0] // v[0] if v[0] else g[1] // v[1]; return (t, g[2] - C2(t) * v[0] * v[1])
        for _ in range(5):
            p = (rng.randint(-50, 50), rng.randint(-50, 50)); q = (rng.randint(-50, 50), rng.randint(-50, 50))
            assert mul(iota(*p), iota(*q)) == iota(p[0] + q[0], p[1] + q[1]), 'iota not a hom'
        for g in gens: assert g[0] * v[1] - g[1] * v[0] == 0, 'H not in A_v'
        tu, su = iota_inv(u)
        idx = abs(tu) * e                       # basis (tu, su), (0, e) of iota^{-1}(H)
        stats['rk1_index_over_2^(3b+1)_max'] = max(stats.get('rk1_index_over_2^(3b+1)_max', 0), idx / 2 ** (3 * b + 1))
        assert idx < 2 ** (3 * b + 1), ('rk1 index bound', gens, idx)
        # the two output generators iota(tu,su), z^e generate H: recheck every input generator
        K = Sub([iota(tu, su), (0, 0, e)])
        assert all(K.contains(g) for g in gens) and H.contains(iota(tu, su))
    stats['e_over_2^(3b+1)_max'] = max(stats.get('e_over_2^(3b+1)_max', 0), e / 2 ** (3 * b + 1))
    assert e < 2 ** (3 * b + 1), ('Lemma E', gens, e)

def main():
    maxb = int(sys.argv[1]) if len(sys.argv) > 1 else 3
    trials = int(sys.argv[2]) if len(sys.argv) > 2 else 3000
    rng = random.Random(int(sys.argv[3]) if len(sys.argv) > 3 else 7)
    random.seed(1)
    # (1) explicit near-extremal rank-1 family: v = (1,1), t1 = 2^b - 1, t2 = -(2^b - 2), c = +-(2^b - 1)
    print('(1) rank-1 family attaining e ~ 2^(3b):')
    for b in range(2, 11):
        t1, t2, c = 2 ** b - 1, -(2 ** b - 2), 2 ** b - 1
        best = 0
        for c1, c2 in itertools.product((-c, 0, c), repeat=2):
            H = Sub([(t1, t1, c1), (t2, t2, c2)]); best = max(best, H.e())
        print(f'   b={b:2d}  e={best}  log2(e)/b={best.bit_length()/b:.3f}  e/2^(3b+1)={best/2**(3*b+1):.4f}')
    # (2) exhaustive two-generator rank-1 search for small b, all primitive directions
    print('(2) exhaustive two-generator rank-1 maxima of e:')
    for b in range(1, maxb + 1):
        M = 2 ** b; best = (0, None)
        dirs = {(p // gcd(p, q), q // gcd(p, q)) for p in range(-M + 1, M) for q in range(-M + 1, M) if (p, q) != (0, 0)}
        for v in dirs:
            ts = [t for t in range(-M + 1, M) if t and abs(t * v[0]) < M and abs(t * v[1]) < M]
            els = [(t * v[0], t * v[1], c) for t in ts for c in range(-M + 1, M)]
            for g1, g2 in itertools.combinations(els, 2):
                H = Sub([g1, g2]); e = H.e()
                if e > best[0]: best = (e, (g1, g2))
        print(f'   b={b}  max e={best[0]}  bound 2^(3b+1)={2**(3*b+1)}  witness={best[1]}')
    # (3) random instances, signed, 1-4 generators, a third forced rank 1
    stats = {}
    for _ in range(trials):
        b = rng.randint(1, 6); M = 2 ** b; m = rng.randint(1, 4)
        if rng.random() < 0.4:
            v = (rng.randint(-3, 3), rng.randint(-3, 3)); v = v if v != (0, 0) else (1, -1)
            gens = []
            for _ in range(m):
                k = rng.randint(-M, M)
                gens.append((k * v[0], k * v[1], rng.randint(-M + 1, M - 1)))
        else:
            gens = [tuple(rng.randint(-M + 1, M - 1) for _ in range(3)) for _ in range(m)]
        gens = [g for g in gens if max(abs(x) for x in g) < M] or [(0, 0, 1)]
        check_instance(gens, b, stats, rng)
    print('(3) random signed instances:', trials)
    for k, val in sorted(stats.items()): print(f'   {k}: {val if isinstance(val, int) else round(val, 4)}')
    # (4) query-box blowup for Step 2: (al,be,ga) with |.| < 2^T maps to entries up to e*2^(2T)
    print('(4) entries of x^{e al} y^be z^ga for |al|,|be|,|ga| <= 2^T - 1:')
    for b, T in ((3, 20), (5, 40)):
        e = 2 ** (3 * b + 1) - 1; m = 2 ** T - 1
        g = elt(-m, m, m, e)
        print(f'   b={b} T={T} e=2^{3*b+1}-1: max |entry| bits = {max(bl(c) for c in g)}  (2T+3b+1 = {2*T+3*b+1})')
    print('all asserts passed')

if __name__ == '__main__':
    main()

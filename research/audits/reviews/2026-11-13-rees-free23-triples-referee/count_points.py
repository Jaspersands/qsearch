"""#C(F_p) on the torus (projective, u1 = 1) for the level-2 weight variety, p = 2 mod 3 (cube roots unique).
(AI-written, pending human review; exact.)  Heuristic for one geometrically irreducible F_p-component: count ~ p."""
import sys, json, itertools, numpy as np
p = int(sys.argv[1]); D = json.load(open('curve_%d.json' % p)); assert p % 3 == 2
d3 = (2 * p - 1) // 3
def inv(a): return pow(int(a) % p, -1, p)
for ci, c in enumerate(D['configs']):
    K = np.array(c['K'], dtype=object) % p; E = np.array(c['E'], dtype=np.int64) % p
    # pick two columns of K forming an invertible 2x2
    pair = next((a, b) for a, b in itertools.combinations(range(1, 6), 2) if (K[0, a] * K[1, b] - K[0, b] * K[1, a]) % p)
    free = [j for j in range(1, 6) if j not in pair]
    a, b = pair; det = int((K[0, a] * K[1, b] - K[0, b] * K[1, a]) % p); di = inv(det)
    Ki = np.array([[K[1, b], -K[0, b]], [-K[1, a], K[0, a]]], dtype=np.int64) * di % p   # inverse of K[:, pair]
    Kf = np.array(K[:, [0] + free], dtype=np.int64) % p
    cube = np.array([pow(x, d3, p) for x in range(p)], dtype=np.int64)
    cnt = 0
    r = np.arange(1, p, dtype=np.int64)
    G1, G2 = np.meshgrid(r, r, indexing='ij'); G1 = G1.ravel(); G2 = G2.ravel()
    for x in range(1, p):
        uf = np.stack([np.ones_like(G1), np.full_like(G1, x), G1, G2], 1)   # u1=1, free coords
        v = uf ** 3 % p
        rhs = (-(v @ Kf.T)) % p                                             # K[:,pair] v_pair = rhs
        vp = (rhs @ Ki.T) % p
        ok = (vp != 0).all(1)
        up = cube[vp]
        U = np.zeros((len(G1), 6), dtype=np.int64); U[:, 0] = 1
        U[:, free] = uf[:, 1:]; U[:, list(pair)] = up
        e = (U ** 2 % p) @ E.T % p
        cnt += int((ok & (e == 0).all(1)).sum())
    print('p=%d config %d: #C(F_p) on torus = %d   (p = %d; ratio %.3f)' % (p, ci, cnt, p, cnt / p), flush=True)

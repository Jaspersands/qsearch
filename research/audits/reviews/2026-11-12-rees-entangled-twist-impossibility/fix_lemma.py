"""Fix lemma, exhaustive over F_p (p = 5, 7): free23 = <x,y> class 3 and each quotient free23/Z'
(Z' a line of gamma_3; these are the filiform fil4).  For every automorphism tau (images of x, y),
T = induced map on V = L/gamma_3 = heis3 (basis xb, yb, zb).  Hard lines K of V: v = v1 + c zb,
v1 != 0 (p^2 + p of them).  Checks:
  (a) T = id_V  =>  tau acts as the identity on the top layer (gamma_3, resp. gamma_3/Z');
  (b) every T != id_V fixes at most p+1 hard lines, and the bound is attained;
  (c) the fixed hard lines of T != id_V lie on <= 2 v1-lines, or in one plane W with W meet zb-axis = 0
      (the poly-time 'hint' computable from T);
  (d) the same bound for the subset of tau that act nontrivially on the top layer.
Finite check only."""
import itertools, sys, numpy as np
sys.path.insert(0, '../2026-11-12-rees-direct-twist-class3-referee')
from lie import tensor, br
FREE = (5, {(0, 1): {2: 1}, (0, 2): {3: 1}, (1, 2): {4: 1}})   # x y z=[x,y] u=[x,z] w=[y,z]

def run(p):
    C = tensor(*FREE, p)
    hard = []
    for v1 in [(1, b) for b in range(p)] + [(0, 1)]:
        for c in range(p): hard.append(np.array([v1[0], v1[1], c]))
    assert len(hard) == p * p + p
    def isfixed(T, v):
        w = (T @ v) % p
        return (w[0] * v[1] - w[1] * v[0]) % p == 0 and (w[0] * v[2] - w[2] * v[0]) % p == 0 and (w[1] * v[2] - w[2] * v[1]) % p == 0
    lines3 = [np.array([1, 0]), *[np.array([a, 1]) for a in range(p)]]  # lines of gamma_3=(u,w)
    quots = [None] + [tuple(q) for q in lines3]
    res = {}
    for q in quots:
        stats = dict(n_aut=0, n_nontriv_top=0, max_fix_Tneid=0, max_fix_nontriv=0, a_fail=0, c_fail=0, b_fail=0)
        for a, b, c, d in itertools.product(range(p), repeat=4):
            det = (a * d - b * c) % p
            if det == 0: continue
            for e, f in itertools.product(range(p), repeat=2):
                X = np.array([a, c, e, 0, 0]); Y = np.array([b, d, f, 0, 0])
                Zi = br(X, Y, C, p); U = br(X, Zi, C, p); W = br(Y, Zi, C, p)
                M = np.array([[U[3], W[3]], [U[4], W[4]]]) % p      # action on gamma_3: columns = images of u, w
                if q is None:
                    top_id = (M == np.eye(2, dtype=np.int64)).all()
                else:
                    qv = np.array(q); img = (M @ qv) % p
                    if (img[0] * qv[1] - img[1] * qv[0]) % p: continue   # does not induce an endo of free23/Z'
                    r = np.array([0, 1]) if q[0] else np.array([1, 0])   # complement of Z'
                    ir = (M @ r) % p
                    # coefficient of r in ir modulo Z': solve ir = s r + t q
                    A2 = np.array([r, qv]).T % p
                    s = None
                    for ss, tt in itertools.product(range(p), repeat=2):
                        if ((ss * r + tt * qv - ir) % p == 0).all(): s = ss; break
                    top_id = (s == 1)
                stats['n_aut'] += 1
                T = np.array([[a, b, 0], [c, d, 0], [e, f, Zi[2]]]) % p
                Tid = (T == np.eye(3, dtype=np.int64)).all()
                if Tid and not top_id: stats['a_fail'] += 1
                if not top_id: stats['n_nontriv_top'] += 1
                if Tid: continue
                fx = [v for v in hard if isfixed(T, v)]
                n = len(fx)
                stats['max_fix_Tneid'] = max(stats['max_fix_Tneid'], n)
                if not top_id: stats['max_fix_nontriv'] = max(stats['max_fix_nontriv'], n)
                if n > p + 1: stats['b_fail'] += 1
                # structure (c)
                v1lines = {tuple(v[:2]) for v in fx}
                ok = len(v1lines) <= 2
                if not ok:
                    # plane W = {(s,t, al*s+be*t)} containing all fx ?
                    ok = any(all((al * v[0] + be * v[1] - v[2]) % p == 0 for v in fx)
                             for al, be in itertools.product(range(p), repeat=2))
                if not ok: stats['c_fail'] += 1
        res[q] = stats
        print(p, 'free23' if q is None else f'free23/<{q[0]}u+{q[1]}w>', stats, flush=True)
    return res

if __name__ == '__main__':
    for p in (5, 7):
        run(p)

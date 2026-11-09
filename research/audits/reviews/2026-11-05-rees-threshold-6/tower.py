"""End-to-end check of the tower (multi-level) schedule of the report, Theorem 2.3.
For a prime p, kappa | p-1 and a chain of steps, it takes M arbitrary random columns in
F_p^a, runs the construction, and checks EXACTLY that the output c is nonzero, has every
nonzero entry a kappa-th power, and satisfies sum_b c_b lambda_b = 0; it then extracts
kappa-th roots u_b and re-checks sum_b u_b^kappa lambda_b = 0.
A step is (Dp, R, K): modulus D', input coefficient classes in R (mod D'), output classes
in K (mod D').  Its pair (alpha, beta) is obtained from ./rectu for that prime and checked here.
Usage: python tower.py p kappa a trials "Dp:R:K;Dp:R:K;..."   e.g.  "2:0,1:0;4:0,2:0;8:0,4:0"
"""
import sys, random, subprocess
from sympy import primitive_root, nthroot_mod

def nullvec(vecs, p):
    """nonzero eta with sum eta_nu vecs[nu] = 0 (vecs: list of length-n lists, len(vecs) > n)."""
    n = len(vecs[0]); m = len(vecs)
    A = [[vecs[nu][i] % p for nu in range(m)] for i in range(n)]   # n x m
    piv = []; row = 0
    for col in range(m):
        pr = next((r for r in range(row, n) if A[r][col]), None)
        if pr is None: continue
        A[row], A[pr] = A[pr], A[row]
        inv = pow(A[row][col], p-2, p); A[row] = [x*inv % p for x in A[row]]
        for r in range(n):
            if r != row and A[r][col]:
                f = A[r][col]; A[r] = [(x - f*y) % p for x, y in zip(A[r], A[row])]
        piv.append(col); row += 1
        if row == n: break
    free = next(c for c in range(m) if c not in piv)
    eta = [0]*m; eta[free] = 1
    for r, c in enumerate(piv): eta[c] = (-A[r][free]) % p
    assert any(eta)
    return eta

class Field:
    def __init__(self, p):
        self.p = p; self.g = primitive_root(p)
    def cls(self, x, D):
        """class of x != 0 modulo P_D: the c in Z_D with x in g^c P_D."""
        p = self.p; e = (p-1)//D
        y = pow(x, e, p); z = pow(self.g, e, p); t = 1
        for c in range(D):
            if t == y: return c
            t = t*z % p
        raise ValueError

def get_pair(p, Dp, R, K):
    out = subprocess.run(['./rectu', str(Dp), ','.join(map(str, R)), ','.join(map(str, K)), str(p), str(p), '1', '1'],
                         capture_output=True, text=True).stdout.split()
    if len(out) < 2 or out[1] != 'FEASIBLE': return None
    bi = out.index('beta'); ai = out.index('alpha')
    beta = dict(zip(R, map(int, out[bi+1:ai]))); alpha = list(map(int, out[ai+1:ai+1+Dp]))
    return alpha, beta

def run(p, kappa, a, steps, rng):
    F = Field(p)
    pairs = []
    for (Dp, R, K) in steps:
        pr = get_pair(p, Dp, R, K)
        if pr is None: return 'no-pair'
        alpha, beta = pr
        for i in R:                         # independent re-check of the pair
            for j in range(Dp):
                v = (alpha[j] + beta[i]) % p
                if (i, j) == (0, 0): assert v and F.cls(v, Dp) == 0
                elif v: assert (F.cls(v, Dp) + i + j) % Dp in [k % Dp for k in K]
        pairs.append((alpha, beta))
    # arity
    M = a + 1
    for (Dp, R, K) in steps: M *= (len(R)-1)*a + 1
    mode = getattr(run, 'mode', 'random')
    if mode == 'random':
        lam = [[rng.randrange(p) for _ in range(a)] for _ in range(M)]
    else:   # structured / degenerate columns: zeros, repeats, unit vectors, a few random
        pool = [[0]*a] + [[1 if t == i else 0 for t in range(a)] for i in range(a)] + [[rng.randrange(p) for _ in range(a)] for _ in range(2)]
        lam = [list(rng.choice(pool)) for _ in range(M)]
    def build(level, cols):
        """returns dict b -> coefficient: a relation on the column indices cols."""
        if level == 0:
            eta = nullvec([lam[b] for b in cols], p)
            return {b: e for b, e in zip(cols, eta) if e}
        Dp, R, K = steps[level-1]; alpha, beta = pairs[level-1]; r = len(R)
        N = (r-1)*a + 1; sz = len(cols)//N
        rels = []
        for nu in range(N):
            c = build(level-1, cols[nu*sz:(nu+1)*sz])
            # normalise: need some coefficient of class 0 mod Dp (rescale only if the
            # previous level's output set is a group, i.e. previous K == [0]).
            if not any(F.cls(v, Dp) == 0 for v in c.values()):
                prevK = steps[level-2][2] if level >= 2 else None
                assert level == 1 or prevK == [0]
                s = pow(next(iter(c.values())), p-2, p); c = {b: v*s % p for b, v in c.items()}
            assert all(F.cls(v, Dp) in R for v in c.values()), 'class outside R'
            rels.append(c)
        U = []
        for c in rels:
            vec = []
            for i in R[1:]:
                acc = [0]*a
                for b, v in c.items():
                    if F.cls(v, Dp) == i:
                        acc = [(x + v*y) % p for x, y in zip(acc, lam[b])]
                vec += acc
            U.append(vec)
        eta = nullvec(U, p)
        nus = next(nu for nu in range(N) if eta[nu] and any(F.cls(v, Dp) == 0 for v in rels[nu].values()))
        s = pow(eta[nus], p-2, p); eta = [e*s % p for e in eta]
        out = {}
        for nu, c in enumerate(rels):
            if not eta[nu]: continue
            j = F.cls(eta[nu], Dp)
            for b, v in c.items():
                w = eta[nu]*(alpha[j] + beta[F.cls(v, Dp)]) % p * v % p
                if w: out[b] = w
        return out
    c = build(len(steps), list(range(M)))
    assert c, 'zero output'
    for v in c.values(): assert pow(v, (p-1)//kappa, p) == 1, 'not a kappa-th power'
    for i in range(a): assert sum(v*lam[b][i] for b, v in c.items()) % p == 0, 'relation fails'
    u = {b: nthroot_mod(v, kappa, p) for b, v in c.items()}
    for i in range(a): assert sum(pow(x, kappa, p)*lam[b][i] for b, x in u.items()) % p == 0
    return f'ok M={M} support={len(c)}'

if __name__ == '__main__':
    p, kappa, a, trials = map(int, sys.argv[1:5])
    steps = []
    for s in sys.argv[5].split(';'):
        Dp, R, K = s.split(':')
        steps.append((int(Dp), [int(x) for x in R.split(',')], [int(x) for x in K.split(',')]))
    assert steps[-1][0] == kappa or kappa % steps[-1][0] == 0
    rng = random.Random(p*1000 + a)
    run.mode = sys.argv[6] if len(sys.argv) > 6 else 'random'
    res = [run(p, kappa, a, steps, rng) for _ in range(trials)]
    print(p, kappa, a, sys.argv[5], res[0] if len(set(res)) == 1 else res)

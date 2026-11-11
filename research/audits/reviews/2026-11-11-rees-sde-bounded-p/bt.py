"""Independent backtracking decision procedure for the gadget problem of
2026-11-08-rees-sde-fq-nest.md (Lemma 2): is a label set L in F_p^k \\ 0 d-feasible with weak
nondegeneracy, for S = P u {0}, P = kappa-th powers?

Encoding (independent of gadget_cnf*.py; it uses the proved reductions only):
  * Lemma R (per-slot form): gamma is P-equivariant in alpha, gamma at (unit direction, coset 1) = 0;
    so one gamma in F_p^k per slot (projective direction D, coset c of P in F_p^*).
  * Lemma Q + Lemma N: labels up to P-scaling, Phi P-equivariant in the label.
  * Search: assign Phi(l) in S^d label by label (fewest live values first); each slot keeps the
    bitmask of gamma values still consistent; a leaf needs every slot mask nonempty and, for every
    direction D, some coset c and some gamma in its mask with a nonzero value on some label
    (weak nondegeneracy).
Every SAT answer is expanded to all alpha in F_p^d \\ 0 and all labels of the P-closure and checked
by plain arithmetic (verify()).  UNSAT answers of this program are [computed], not certified.
"""
import itertools, sys, time


def powers(p, kappa):
    return sorted({pow(x, kappa, p) for x in range(1, p)})


def setup(p, kappa, k, d):
    P = powers(p, kappa)
    S = sorted(set(P) | {0})
    Sset = set(S)
    Pset = set(P)
    creps, seen = [], set()
    for x in range(1, p):
        if x not in seen:
            creps.append(x)
            seen |= {(x * l) % p for l in P}
    dirs = [a for a in itertools.product(range(p), repeat=d)
            if any(a) and a[next(i for i, x in enumerate(a) if x)] == 1]
    unit = {tuple(1 if i == j else 0 for i in range(d)) for j in range(d)}
    gvals = list(itertools.product(range(p), repeat=k))
    phis = list(itertools.product(S, repeat=d))
    return dict(p=p, kappa=kappa, k=k, d=d, P=P, S=S, Sset=Sset, creps=creps, dirs=dirs,
                unit=unit, gvals=gvals, phis=phis)


def pclass_reps(p, P, L):
    seen, reps = set(), []
    for l in L:
        l = tuple(x % p for x in l)
        if l in seen:
            continue
        reps.append(l)
        for lam in P:
            seen.add(tuple((lam * x) % p for x in l))
    return reps


def pclosure(p, P, L):
    return sorted({tuple((lam * x) % p for x in l) for l in L for lam in P})


class Solver:
    def __init__(self, ctx, L):
        self.c = c = ctx
        p, k, d = c['p'], c['k'], c['d']
        self.labels = pclass_reps(p, c['P'], L)
        self.slots = [(D, ci) for D in range(len(c['dirs'])) for ci in range(len(c['creps']))]
        self.alpha = {s: tuple((c['creps'][s[1]] * x) % p for x in c['dirs'][s[0]]) for s in self.slots}
        self.fixed = {s for s in self.slots if s[1] == 0 and c['dirs'][s[0]] in c['unit']}
        G = c['gvals']
        # dot[l][g] = <g, l>
        dot = {l: [sum(g[i] * l[i] for i in range(k)) % p for g in G] for l in self.labels}
        self.A, self.NZ = {}, {}
        for s in self.slots:
            a = self.alpha[s]
            for l in self.labels:
                for fi, ph in enumerate(c['phis']):
                    base = sum(a[j] * ph[j] for j in range(d)) % p
                    m = nz = 0
                    for gi in range(len(G)):
                        v = (base + dot[l][gi]) % p
                        if v in c['Sset']:
                            m |= 1 << gi
                            if v:
                                nz |= 1 << gi
                    self.A[s, l, fi] = m
                    self.NZ[s, l, fi] = nz
        self.full = (1 << len(G)) - 1
        self.nodes = 0

    def solve(self, node_limit=None):
        masks = {s: (1 if s in self.fixed else self.full) for s in self.slots}  # gamma index 0 = zero vector
        self.node_limit = node_limit
        self.assign = {}
        r = self._rec(masks)
        return r

    def _live(self, l, masks):
        out = []
        for fi in range(len(self.c['phis'])):
            ok = True
            for s in self.slots:
                if not (masks[s] & self.A[s, l, fi]):
                    ok = False
                    break
            if ok:
                out.append(fi)
        return out

    def _rec(self, masks):
        self.nodes += 1
        if self.node_limit and self.nodes > self.node_limit:
            raise TimeoutError
        rest = [l for l in self.labels if l not in self.assign]
        if not rest:
            return self._leaf(masks)
        best, bl = None, None
        for l in rest:
            lv = self._live(l, masks)
            if not lv:
                return False
            if best is None or len(lv) < len(best):
                best, bl = lv, l
                if len(lv) == 1:
                    break
        for fi in best:
            nm = {s: masks[s] & self.A[s, bl, fi] for s in self.slots}
            self.assign[bl] = fi
            if self._rec(nm):
                return True
            del self.assign[bl]
        return False

    def _leaf(self, masks):
        c = self.c
        choice = {}
        for D in range(len(c['dirs'])):
            okD = False
            for ci in range(len(c['creps'])):
                s = (D, ci)
                nz = 0
                for l, fi in self.assign.items():
                    nz |= self.NZ[s, l, fi]
                good = masks[s] & nz
                if good:
                    okD = True
                    choice[s] = (good & -good).bit_length() - 1
                else:
                    choice[s] = (masks[s] & -masks[s]).bit_length() - 1
            if not okD:
                return False
        self.sol = (dict(self.assign), choice)
        return True

    def expand(self):
        """expand to all alpha and all labels of the P-closure"""
        c = self.c; p = c['p']
        assign, choice = self.sol
        gamma = {}
        for s, gi in choice.items():
            a, g = self.alpha[s], c['gvals'][gi]
            for lam in c['P']:
                gamma[tuple((lam * x) % p for x in a)] = tuple((lam * x) % p for x in g)
        Phi = {}
        for l, fi in assign.items():
            ph = c['phis'][fi]
            for lam in c['P']:
                Phi[tuple((lam * x) % p for x in l)] = tuple((lam * x) % p for x in ph)
        return Phi, gamma


def verify(ctx, L, Phi, gamma):
    """plain-arithmetic check of Lemma 2(A) feasibility + weak nondegeneracy on the P-closure of L"""
    p, k, d, Sset = ctx['p'], ctx['k'], ctx['d'], ctx['Sset']
    Lc = pclosure(p, ctx['P'], L)
    dir_ok = {}
    for a in itertools.product(range(p), repeat=d):
        if not any(a):
            continue
        if a not in gamma:
            return False, ('missing gamma', a)
        anynz = False
        for l in Lc:
            y = (sum(a[j] * Phi[l][j] for j in range(d)) + sum(gamma[a][i] * l[i] for i in range(k))) % p
            if y not in Sset:
                return False, (a, l, y)
            anynz |= y != 0
        lead = next(x for x in a if x)
        key = tuple((x * pow(lead, -1, p)) % p for x in a)
        dir_ok[key] = dir_ok.get(key, False) or anynz
    if not all(dir_ok.values()):
        return False, 'degenerate'
    return True, None


def has_S_functional(ctx, L):
    p, k = ctx['p'], ctx['k']
    Lc = pclosure(p, ctx['P'], L)
    for g in itertools.product(range(p), repeat=k):
        if any(g) and all(sum(g[i] * l[i] for i in range(k)) % p in ctx['Sset'] for l in Lc):
            return g
    return None


def decide(p, kappa, k, d, L, node_limit=None):
    ctx = setup(p, kappa, k, d)
    sv = Solver(ctx, L)
    t = time.time()
    try:
        r = sv.solve(node_limit)
    except TimeoutError:
        return 'timeout', sv.nodes, time.time() - t, None
    if r:
        Phi, gamma = sv.expand()
        ok, why = verify(ctx, L, Phi, gamma)
        assert ok, why
        return 'SAT', sv.nodes, time.time() - t, (Phi, gamma)
    return 'UNSAT', sv.nodes, time.time() - t, None


def named(p, k, spec):
    if spec == 'all':
        return [l for l in itertools.product(range(p), repeat=k) if any(l)]
    if spec == 'nest':
        return [l for l in itertools.product(range(p), repeat=k) if l[0] != 0]
    raise ValueError(spec)


if __name__ == '__main__':
    p, kappa, k, d = map(int, sys.argv[1:5])
    spec = sys.argv[5]
    L = named(p, k, spec)
    r, nodes, dt, _ = decide(p, kappa, k, d, L)
    print(f'p={p} kappa={kappa} k={k} d={d} L={spec} |L|={len(L)}: {r} nodes={nodes} {dt:.1f}s', flush=True)

"""s2b: independent unpruned search for RC(D;R->K) contractions (appendix-schedule2.tex
Subsections app:s2-tower, app:s2-chains, app:s2-scope).  Written from the definitions in the
paper only.  Normal form alpha_0 = 1, beta_0 = 0 (paper, before the chain definition).
DFS over beta_i (i in R minus 0) with forward checking of the D-1 column sets; no symmetry
breaking.  Every witness is re-checked by verify(), which uses exponentiation, not the index
table.  Usage: python rcsearch.py TASK  (tasks: e2 sym3 tower4 tower5 tower6 tower8 chains k7)
Finite checks only: a passing check is not a proof."""
import sys, time
from collections import deque
import numpy as np
from sympy import primerange, primitive_root

class Fld:
    def __init__(self, p, kappa, u=1):
        self.p, self.kappa = p, kappa
        g = primitive_root(p)
        self.g = g
        self.xi = pow(g, u, p)
        e = (p - 1) // kappa
        zeta = pow(self.xi, e, p)
        lut = np.full(p, -1, dtype=np.int64)
        z = 1
        for m in range(kappa):
            lut[z] = m; z = z * zeta % p
        x = np.arange(p, dtype=np.int64)
        # vectorised x^e mod p (p < 2^31, so products fit in int64)
        res = np.ones(p, dtype=np.int64); base = x % p; ee = e
        while ee:
            if ee & 1: res = res * base % p
            base = base * base % p; ee >>= 1
        ind = lut[res]
        ind[0] = -1
        assert (ind[1:] >= 0).all()
        self.ind = ind
        self.mask = (1 << p) - 1
        self.cos = {}

    def coset(self, D, m):
        key = (D, m % D)
        if key not in self.cos:
            bits = np.zeros(self.p, dtype=np.uint8)
            bits[1:] = (self.ind[1:] % D == key[1])
            self.cos[key] = int.from_bytes(np.packbits(bits, bitorder='little').tobytes(), 'little')
        return self.cos[key]

    def sh(self, S, b):
        """{y - b mod p : y in S}"""
        p = self.p
        b %= p
        if b == 0: return S
        return ((S >> b) | (S << (p - b))) & self.mask

class Limit(Exception):
    pass

def rc_search(F, D, R, K, nonzero=False, node_limit=None):
    R = sorted(set(r % D for r in R)); K = sorted(set(k % D for k in K))
    assert 0 in R and 0 in K
    def T(i, j):
        b = 0 if nonzero else 1
        for k in K:
            b |= F.coset(D, k - i - j)
        return b
    cols = list(range(1, D))
    rows = [i for i in R if i != 0]
    init = [T(0, j) for j in cols]
    cand = {i: F.sh(T(i, 0), 1) for i in rows}
    Tij = {(i, j): T(i, j) for i in rows for j in cols}
    cnt = [0]
    beta = {}
    def dfs(level, Fs):
        cnt[0] += 1
        if node_limit and cnt[0] > node_limit:
            raise Limit()
        if level == len(rows):
            return [((f & -f).bit_length() - 1) for f in Fs]
        i = rows[level]
        c = cand[i]
        while c:
            low = c & -c
            b = low.bit_length() - 1
            c ^= low
            newF = []
            for jj, j in enumerate(cols):
                f = Fs[jj] & F.sh(Tij[(i, j)], b)
                if not f:
                    break
                newF.append(f)
            else:
                beta[i] = b
                r = dfs(level + 1, newF)
                if r is not None:
                    return r
                del beta[i]
        return None
    res = dfs(0, init)
    if res is None:
        return None, cnt[0]
    alpha = {0: 1}
    for jj, j in enumerate(cols):
        alpha[j] = res[jj]
    bet = {0: 0}; bet.update(beta)
    assert verify(F, D, R, K, alpha, bet, nonzero), "witness failed verification"
    return (alpha, bet), cnt[0]

def verify(F, D, R, K, alpha, beta, nonzero=False):
    p = F.p; e = (p - 1) // D
    zeta = pow(F.xi, e, p)
    pw = [pow(zeta, m, p) for m in range(D)]
    assert len(set(pw)) == D
    def cls(y):
        return pw.index(pow(y, e, p))
    for i in R:
        for j in range(D):
            y = (alpha[j] + beta[i]) % p
            if (i, j) == (0, 0):
                if y == 0 or cls(y) != 0: return False
            elif y == 0:
                if nonzero: return False
            elif (cls(y) + i + j) % D not in K:
                return False
    return True

def two_level(F, D, **kw):
    return rc_search(F, D, range(D), [0], **kw)

def tower(F, kappa, chain, **kw):
    """chain: list 1 = D_0 | D_1 | ... | D_L = kappa; step t is RC(D_t; D_{t-1} Z_{D_t})"""
    for t in range(1, len(chain)):
        Dp, Dt = chain[t - 1], chain[t]
        R = [x for x in range(Dt) if x % Dp == 0]
        w, _ = rc_search(F, Dt, R, [0], **kw)
        if w is None:
            return False
    return True

def union_chain(F, kappa, K, **kw):
    w, _ = rc_search(F, kappa, range(kappa), K, **kw)
    if w is None: return False
    w, _ = rc_search(F, kappa, K, [0], **kw)
    return w is not None

def divisor_chains(kappa):
    out = []
    def rec(ch):
        if ch[-1] == kappa:
            out.append(list(ch)); return
        for d in range(ch[-1] + 1, kappa + 1):
            if kappa % d == 0 and d % ch[-1] == 0:
                rec(ch + [d])
    rec([1])
    return out

def subsets0(D, sizes=None):
    res = []
    for mask in range(2 ** (D - 1)):
        K = (0,) + tuple(i for i in range(1, D) if mask >> (i - 1) & 1)
        if sizes is None or len(K) in sizes:
            res.append(K)
    return res

def any_construction(F, kappa, Ksizes, node_limit=None):
    """two-level, any tower, or union chain Z_kappa -> K -> {0} with |K| in Ksizes"""
    for ch in divisor_chains(kappa):          # includes [1, kappa] = two-level
        if tower(F, kappa, ch, node_limit=node_limit):
            return ("tower", tuple(ch))
    for K in subsets0(kappa, Ksizes):
        if union_chain(F, kappa, K, node_limit=node_limit):
            return ("union", K)
    return None

def chain_bfs(F, kappa, first_D_max=None, node_limit=None):
    """reachability (1,{0}) -> (kappa,{0}) in the graph of the chain definition;
    first_D_max restricts D_1 <= first_D_max"""
    divs = [d for d in range(2, kappa + 1) if kappa % d == 0]
    start = (1, (0,)); target = (kappa, (0,))
    prev = {start: None}
    q = deque([start]); memo = {}
    while q:
        node = q.popleft()
        D0, K0 = node
        for D1 in divs:
            if D1 % D0: continue
            if node == start and first_D_max and D1 > first_D_max: continue
            R = tuple(x for x in range(D1) if (x % D0) in K0)
            for K in subsets0(D1):
                nxt = (D1, K)
                if nxt in prev: continue
                key = (D1, R, K)
                if key not in memo:
                    w, _ = rc_search(F, D1, R, K, node_limit=node_limit)
                    memo[key] = w is not None
                if memo[key]:
                    prev[nxt] = node
                    if nxt == target:
                        path = [nxt]
                        while prev[path[-1]] is not None:
                            path.append(prev[path[-1]])
                        return path[::-1]
                    q.append(nxt)
    return None

out = []
def say(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); out.append(s)

def task_e2():
    TAceil = {4: 869, 5: 12658, 6: 233578}
    for kappa in (4, 5):
        for nz in (False, True):
            ex = []; t0 = time.time(); nodes = 0
            for p in primerange(3, TAceil[kappa]):
                if p % kappa != 1: continue
                F = Fld(p, kappa)
                w, n = two_level(F, kappa, nonzero=nz); nodes += n
                if w is None: ex.append(p)
            say("E_2(%d)%s up to ceil(T_A)=%d: %s  [%.1fs, %d nodes]" % (
                kappa, " nonzero-entries" if nz else "", TAceil[kappa], ex, time.time() - t0, nodes))
    # kappa = 6 up to T_A(6): exceptional count and largest
    kappa = 6; ex = []; t0 = time.time(); nodes = 0
    for p in primerange(3, TAceil[6]):
        if p % 6 != 1: continue
        F = Fld(p, 6)
        w, n = two_level(F, 6); nodes += n
        if w is None: ex.append(p)
    say("E_2(6) up to %d: %d primes, largest %s  [%.1fs, %d nodes]" % (TAceil[6], len(ex), max(ex), time.time() - t0, nodes))
    say("   ", ex)

def task_sym3():
    # symmetric form: t in F_p^3, C_ij = z_i z_j (t_i + t_j) in Q_0 cup {0}, C_00 != 0
    for nz in (False, True):
        fails = []
        for p in primerange(7, 400):
            if p % 3 != 1: continue
            F = Fld(p, 3)
            ind = F.ind
            def ok(y, i, j):
                y %= p
                if y == 0: return (not nz) and (i, j) != (0, 0)
                return (ind[y] + i + j) % 3 == 0
            found = False
            t0 = (p + 1) // 2   # 1/2: 2 t_0 = 1 in Q_0 (scaling by Q_0 normalises t_0)
            for t1 in range(p):
                if not (ok(t0 + t1, 0, 1) and ok(2 * t1, 1, 1)): continue
                for t2 in range(p):
                    if ok(t0 + t2, 0, 2) and ok(t1 + t2, 1, 2) and ok(2 * t2, 2, 2):
                        found = True; break
                if found: break
            if not found: fails.append(p)
        say("kappa=3 symmetric form%s fails at (p<400): %s" % (" (nonzero entries)" if nz else "", fails))

def task_tower(kappa, pmax, Ksizes, node_limit=None, plist=None):
    t0 = time.time()
    fails = []; unknown = []
    primes = plist if plist else [p for p in primerange(3, pmax) if p % kappa == 1]
    for p in primes:
        F = Fld(p, kappa)
        try:
            r = any_construction(F, kappa, Ksizes, node_limit=node_limit)
        except Limit:
            unknown.append(p); continue
        if r is None: fails.append(p)
    say("kappa=%d, primes p=1 mod kappa below %s: no two-level/tower/union(|K| in %s) at %s; UNKNOWN (node limit) at %s  [%.1fs]" % (
        kappa, pmax, Ksizes, fails, unknown, time.time() - t0))

def task_tower5():
    E25 = [11, 31, 41, 61, 71, 101, 131, 151, 181]
    for u in range(1, 5):
        fails = []
        for p in E25:
            F = Fld(p, 5)
            if not union_chain(F, 5, (0, u)): fails.append(p)
        say("kappa=5: chain Z_5 -> {0,%d} -> {0} (xi = least prim. root) fails at E_2(5) primes %s" % (u, fails))
    fails = []
    for p in E25:
        F = Fld(p, 5)
        if any_construction(F, 5, (2, 3)) is None: fails.append(p)
    say("kappa=5: no two-level/union(|K| in 2,3) at E_2(5) primes: %s" % fails)

def task_chains():
    cases = [(4, [5, 13, 17, 29, 37, 53]), (5, [11, 31]), (6, [7, 13, 19, 31, 43, 67]), (7, [29, 71, 43, 113]), (8, [17])]
    for kappa, ps in cases:
        for p in ps:
            t0 = time.time()
            F = Fld(p, kappa)
            try:
                path = chain_bfs(F, kappa, node_limit=2_000_000)
                msg = "chain %s" % path if path else "NO chain"
                if kappa in (6, 8, 9) and path:
                    path2 = chain_bfs(F, kappa, first_D_max=kappa // 2, node_limit=2_000_000)
                    msg += "; with 1<D_1<kappa: %s" % path2
            except Limit:
                msg = "UNKNOWN (node limit)"
            say("kappa=%d p=%d: %s  [%.1fs]" % (kappa, p, msg, time.time() - t0))

def task_k7():
    # three-step chains Z_7 -> u{0,1,2} -> u{0,1} -> {0}, xi = least primitive root
    t0 = time.time()
    bad = {u: [] for u in range(1, 7)}; none = []
    for p in primerange(29, 3300):
        if p % 7 != 1: continue
        F = Fld(p, 7)
        okany = False
        for u in range(1, 7):
            K1 = tuple(sorted({0, u % 7, 2 * u % 7})); K2 = tuple(sorted({0, u % 7}))
            w1, _ = rc_search(F, 7, range(7), K1)
            ok = False
            if w1 is not None:
                w2, _ = rc_search(F, 7, K1, K2)
                if w2 is not None:
                    w3, _ = rc_search(F, 7, K2, [0])
                    ok = w3 is not None
            if not ok: bad[u].append(p)
            okany |= ok
        if not okany: none.append(p)
    say("kappa=7, p=1 mod 7 in [29,3300): no u works at %s; u=1 fails at %s; u=2 fails at %s  [%.1fs]" % (
        none, bad[1], bad[2], time.time() - t0))
    say("   u=3..6 fail at: %s" % {u: bad[u] for u in range(3, 7)})

def task_k9():
    # tower 1|3|9 alone over all primes p = 1 mod 9 below 135000; then the full
    # construction list (with a node limit) at the primes where the tower fails
    t0 = time.time(); tf = []
    for p in primerange(19, 135000):
        if p % 9 != 1: continue
        F = Fld(p, 9)
        if not tower(F, 9, [1, 3, 9]): tf.append(p)
    say("kappa=9: tower 1|3|9 fails (p < 135000) at %d primes: %s  [%.1fs]" % (len(tf), tf, time.time() - t0))
    fails = []; unknown = []
    for p in tf:
        F = Fld(p, 9)
        try:
            r = any_construction(F, 9, (2, 3), node_limit=1_000_000)
        except Limit:
            unknown.append(p); continue
        if r is None: fails.append(p)
    say("kappa=9: no two-level/tower/union(|K| in 2,3) at %s; UNKNOWN (node limit) at %s  [%.1fs]" % (fails, unknown, time.time() - t0))

def task_k9b():
    # the 14 primes below 135000 where tower 1|3|9 fails (task k9, first phase; recorded in
    # rcsearch-k9b.out): two-level, tower 1|9, union chains |K| in {2,3}; per-search node
    # limit, a limit hit marks that construction UNKNOWN and the search moves on
    tf = [19, 37, 73, 109, 127, 163, 181, 199, 271, 307, 379, 433, 487, 523]
    t0 = time.time()
    for p in tf:
        if time.time() - t0 > 170:
            say("p=%d: not run (time cap)" % p); continue
        F = Fld(p, 9)
        found = None; unk = []
        try:
            w, _ = two_level(F, 9, node_limit=300_000)
            if w is not None: found = "two-level"
        except Limit:
            unk.append("two-level")
        if not found:
            for K in subsets0(9, (2, 3)):
                try:
                    if union_chain(F, 9, K, node_limit=100_000):
                        found = "union %s" % (K,); break
                except Limit:
                    unk.append(K)
        say("kappa=9 p=%d: %s; undecided: %d of 37 constructions  [%.1fs]" % (
            p, ("FOUND " + found) if found else "none found", len(unk), time.time() - t0))

def task_k9c():
    # the four primes below 135000 where tower 1|3|9 fails but that are not in the list of
    # Remark tower-scope: some construction must exist there
    t0 = time.time()
    for p in [271, 379, 487, 523]:
        F = Fld(p, 9)
        found = None; unk = 0
        try:
            w, _ = two_level(F, 9, node_limit=300_000)
            if w is not None: found = "two-level"
        except Limit:
            unk += 1
        if not found:
            for K in subsets0(9, (2, 3)):
                try:
                    if union_chain(F, 9, K, node_limit=50_000):
                        found = "union chain Z_9 -> %s -> {0}" % (K,); break
                except Limit:
                    unk += 1
        say("kappa=9 p=%d: %s (limit hits before it: %d)  [%.1fs]" % (p, ("FOUND " + found) if found else "none found", unk, time.time() - t0))

def task_k10():
    # Remark local-scope: every prime p = 1 mod 10 up to 8191 is in E_2(10) except 3361, 3761,
    # 5821; every prime p = 1 mod 12 up to 10453 is in E_2(12).  Spot checks only.
    t0 = time.time()
    res = {}
    for p in [p for p in primerange(3300, 3800) if p % 10 == 1] + [5821]:
        F = Fld(p, 10)
        try:
            w, n = two_level(F, 10, node_limit=3_000_000)
            res[p] = "contraction" if w is not None else "exceptional"
        except Limit:
            res[p] = "UNKNOWN"
    say("kappa=10, p in [3300,3800) and 5821: %s  [%.1fs]" % (res, time.time() - t0))
    res = {}
    for p in [10453, 10429]:
        if time.time() - t0 > 140: res[p] = "not run"; continue
        F = Fld(p, 12)
        try:
            w, n = two_level(F, 12, node_limit=3_000_000)
            res[p] = "contraction" if w is not None else "exceptional"
        except Limit:
            res[p] = "UNKNOWN"
    say("kappa=12: %s  [%.1fs]" % (res, time.time() - t0))

if __name__ == "__main__":
    task = sys.argv[1]
    if task == "e2": task_e2()
    elif task == "sym3": task_sym3()
    elif task == "tower4": task_tower(4, 97, (2, 3))
    elif task == "tower5": task_tower5()
    elif task == "tower6": task_tower(6, 649, (2, 3), node_limit=3_000_000)
    elif task == "tower8": task_tower(8, 2433, (2, 3), node_limit=2_000_000)
    elif task == "chains": task_chains()
    elif task == "k7": task_k7()
    elif task == "k9": task_k9()
    elif task == "k9b": task_k9b()
    elif task == "k9c": task_k9c()
    elif task == "k10": task_k10()
    open(__file__.replace('.py', '-%s.out' % task), 'w').write("\n".join(out) + "\n")

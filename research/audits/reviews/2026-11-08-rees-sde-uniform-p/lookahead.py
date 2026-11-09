"""Control structure (fan-in) of a leaf and three back substitutions.

Leaf = flag rounds 1..L (q1core Round objects with S, delta, blocks, bclass, W, e, start, end),
Ub = concatenated generators W_{l,1..n_l-1} (basis of U_L), src = source columns.
Work in Ub-coordinates throughout: tau_l is a coordinate vector supported on indices < R_l.end.

Pair (j,b,b'), c_b != c_b': phi(v) = v[b] - v[b'] on the Omega_j-coordinates (index 0 -> 0).
F_{j,bb'} = phi(tau_j) = phi(tau_L) - sum_{l>j} s_l phi(e_l).
Control index ctrl(pair) = least l > j with phi(e_l) != 0, else 'source'.
Source control = last source (in the chosen order) with phi(sigma) != 0.
Fan-in N_l = #pairs with ctrl = l; N_src[i] = #source-controlled pairs controlled by source i.

Modes
  plain : Lemma 2 (t i.i.d. in P, s_l uniform in Good_l).
  look  : t_i uniform in P minus the values that zero a pair it controls; s_l uniform in
          Good_l minus Bad_l = {phi(tau_l)/phi(e_l) : ctrl(pair) = l}.  If the allowed set is
          empty, fall back to the plain choice and record the event.
"""
from collections import Counter

from sss import solve_in_span
import numpy as np

_CT = {}


def _cls_table(Fd):
    """Class of each y in F_p (-1 for y = 0), as a numpy array (cached per (p, k))."""
    key = (Fd.p, Fd.k)
    if key not in _CT:
        p, k = Fd.p, Fd.k
        t = -np.ones(p, dtype=np.int64)
        y = 1
        for e in range(p - 1):
            t[y] = e % k
            y = y * Fd.g % p
        _CT[key] = t
    return _CT[key]


def coords(Ub, v, p):
    if not any(v):
        return [0] * len(Ub)
    c = solve_in_span(Ub, v, p)
    assert c is not None
    return c


class Ctl:
    def __init__(self, Fd, cols, rounds, Ub, src):
        p = self.p = Fd.p
        self.Fd, self.cols, self.rounds, self.Ub, self.src = Fd, cols, rounds, Ub, list(src)
        self.n = len(Ub)
        self.ce = [coords(Ub, R.e, p) for R in rounds]
        self.cs = [coords(Ub, cols[s], p) for s in self.src]
        self.pairs = []          # (j, b, b2)
        for j, R in enumerate(rounds):
            nb = len(R.blocks)
            for b in range(nb):
                for b2 in range(b + 1, nb):
                    if R.bclass[b] != R.bclass[b2]:
                        self.pairs.append((j, b, b2))
        L = len(rounds)
        self.ctrl = []
        for (j, b, b2) in self.pairs:
            m = next((l for l in range(j + 1, L) if self.phi(j, b, b2, self.ce[l])), None)
            if m is None:
                i = max((i for i in range(len(self.src)) if self.phi(j, b, b2, self.cs[i])),
                        default=None)
                assert i is not None, "(S) fails"
                self.ctrl.append(("src", i))
            else:
                self.ctrl.append(("lev", m))
        self.by_lev = {}
        self.by_src = {}
        for k, c in enumerate(self.ctrl):
            (self.by_lev if c[0] == "lev" else self.by_src).setdefault(c[1], []).append(k)
        self.N_lev = max([len(v) for v in self.by_lev.values()] + [0])
        self.N_src = max([len(v) for v in self.by_src.values()] + [0])
        self.n_src_ctrl = sum(len(v) for v in self.by_src.values())
        # locality: ctrl level - j for level-controlled pairs
        self.gap = Counter(c[1] - self.pairs[k][0] for k, c in enumerate(self.ctrl) if c[0] == "lev")

    def phi(self, j, b, b2, v):
        R = self.rounds[j]
        x = v[R.start + b - 1] if b else 0
        y = v[R.start + b2 - 1] if b2 else 0
        return (x - y) % self.p

    def summary(self):
        return dict(rho=len(self.pairs), N_lev=self.N_lev, N_src=self.N_src,
                    src_ctrl=self.n_src_ctrl, L=len(self.rounds), nsrc=len(self.src),
                    maxgap=max(self.gap) if self.gap else 0)

    # ------------------------------------------------------------------
    def good_set(self, beta, bclass):
        Fd, p = self.Fd, self.p
        ok = lambda s: all(Fd.in_class0(beta[b] + s, -bclass[b]) for b in range(len(beta)))
        return [s for s in range(p) if ok(s)]

    def good_draw(self, beta, bclass, bad, rng):
        """Uniform element of Good minus bad (exact enumeration for p <= 300000, rejection above)."""
        p, Fd = self.p, self.Fd
        ok = lambda s: all(Fd.in_class0(beta[b] + s, -bclass[b]) for b in range(len(beta)))
        if p <= 300000:
            ct = _cls_table(Fd)
            sv = np.arange(p)
            m = np.ones(p, dtype=bool)
            for b in range(len(beta)):
                row = ct[(beta[b] + sv) % p]
                m &= (row < 0) | (row == (-bclass[b]) % Fd.k)
            G = [int(v) for v in np.nonzero(m)[0]]
            G2 = [s for s in G if s not in bad]
            if G2:
                return rng.choice(G2), "ok"
            if G:
                return rng.choice(G), "fanin_exhausted"
            return None, "emptyGood"
        for _ in range(400000):
            s = rng.randrange(p)
            if s not in bad and ok(s):
                return s, "ok"
        for _ in range(400000):
            s = rng.randrange(p)
            if ok(s):
                return s, "fanin_exhausted"
        return None, "emptyGood?"

    def backward(self, rng, mode="look"):
        p, Fd, cols = self.p, self.Fd, self.cols
        ev = Counter()
        x = [0] * len(cols)
        tau = [0] * self.n
        Pset = Fd.P
        for i, s_ in enumerate(self.src):
            if mode == "look" and i in self.by_src:
                bad = set()
                for k in self.by_src[i]:
                    j, b, b2 = self.pairs[k]
                    A = self.phi(j, b, b2, tau)
                    f = self.phi(j, b, b2, self.cs[i])
                    bad.add(A * pow(f, p - 2, p) % p)       # A - t f = 0
                allowed = [t for t in Pset if t not in bad]
                if allowed:
                    t = rng.choice(allowed)
                else:
                    t = Fd.randP(rng)
                    ev["src_fanin_exhausted"] += 1
            else:
                t = Fd.randP(rng)
            x[s_] = t
            tau = [(u - t * v) % p for u, v in zip(tau, self.cs[i])]
        for l in range(len(self.rounds) - 1, -1, -1):
            R = self.rounds[l]
            beta = [0] + tau[R.start:R.end]
            bad = set()
            if mode == "look":
                for k in self.by_lev.get(l, []):
                    j, b, b2 = self.pairs[k]
                    A = self.phi(j, b, b2, tau)
                    f = self.phi(j, b, b2, self.ce[l])
                    bad.add(A * pow(f, p - 2, p) % p)
            s, why = self.good_draw(beta, R.bclass, bad, rng)
            if why != "ok":
                ev[why] += 1
            if s is None:
                ev["fail_level_%d" % l] += 1
                return None, ev
            for b, G in enumerate(R.blocks):
                for i in G:
                    x[i] = R.delta[i] * (beta[b] + s) % p
            # value in coordinates: beta on Omega_l plus s * e_l (e_l in U_{l-1})
            for k in range(R.start, R.end):
                tau[k] = 0
            tau = [(u - s * v) % p for u, v in zip(tau, self.ce[l])]
        assert not any(tau), "residual"
        return x, ev

"""Referee's own implementation of Theorem L's lookahead back substitution, tested on the leaves
that the UNMODIFIED ALG-T (subquad.py, Theorem A folder) produces on uniform and EC banks.

For each leaf (rounds, Ub, src) the script:
  * computes, in its own code, the steering functionals phi_{j,bb'} in the W-basis coordinates,
    the control variable of every cross pair (least l > j with phi(e_l) != 0, else last source with
    phi(sigma) != 0), the fan-ins N_l, N_{src,i};
  * runs PASSES lookahead passes.  At every level it asserts the proof's inductive invariants:
      (I1) no cross-class coincidence at the current level (every pair there was protected earlier);
      (I2) if |Good_l| >= N_l + 1 then the allowed set is nonempty;
    and at every source |P| >= N_{src,i} + 1 implies the allowed set is nonempty.
    It records whether the leaf satisfies the *leaf-dependent* hypothesis
      H(leaf): min_l |Good_l| (over the passes) >= N*_lev + 1 and (p-1)/kappa >= N*_src + 1,
    and whether any fallback / failure happened.  Theorem L predicts: H(leaf) => 0 fallback.
    (The theorem's hypothesis G*_E(p) >= N*_lev + 1 implies H(leaf); checking H(leaf) is the
    sharper test of the mechanism.)
  * also runs the deterministic variant (least allowed value) once and checks the witness.
Also verifies the 'last-drawn nonzero coefficient' claim directly: after the control variable is
drawn, F_pi is recomputed at every later draw and asserted unchanged.

Usage: lookahead_check.py kappa J p ranks(comma) banks passes seed [fams=uniform,EC]
"""
import os
import random
import sys
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "2026-11-07-rees-sde-subquad-A"))
import subquad as SQ  # noqa
import sss  # noqa
from sss import rank, solve_in_span, check  # noqa

k, J, p = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
ranks = [int(x) for x in sys.argv[4].split(",")]
banks, PASSES, seed = int(sys.argv[5]), int(sys.argv[6]), int(sys.argv[7])
fams = sys.argv[8].split(",") if len(sys.argv) > 8 else ["uniform", "EC"]
rng = random.Random(seed)
Fd = SQ.Field(p, k)
Par = SQ.Params(J, k)
Q0 = [set([0]) | {y for y in range(1, p) if Fd.cls(y) == c} for c in range(k)]


def coords(Ub, v):
    if not any(v):
        return [0] * len(Ub)
    c = solve_in_span(Ub, v, p)
    assert c is not None
    return c


def good_set(beta, bclass):
    return [s for s in range(p) if all((beta[b] + s) % p in Q0[(-bclass[b]) % k] for b in range(len(beta)))]


class Leaf:
    def __init__(self, cols, rounds, Ub, src):
        self.cols, self.rounds, self.Ub, self.src = cols, rounds, Ub, list(src)
        self.ce = [coords(Ub, R.e) for R in rounds]
        self.cs = [coords(Ub, cols[s]) for s in self.src]
        self.pairs = [(j, b, b2) for j, R in enumerate(rounds) for b in range(len(R.blocks))
                      for b2 in range(b + 1, len(R.blocks)) if R.bclass[b] != R.bclass[b2]]
        L = len(rounds)
        self.ctrl = {}
        for pi in self.pairs:
            j = pi[0]
            m = next((l for l in range(j + 1, L) if self.phi(pi, self.ce[l])), None)
            if m is None:
                i = max(i for i in range(len(self.src)) if self.phi(pi, self.cs[i]))   # (S)
                self.ctrl[pi] = ("src", i)
            else:
                self.ctrl[pi] = ("lev", m)
        self.N_lev = Counter(c[1] for c in self.ctrl.values() if c[0] == "lev")
        self.N_src = Counter(c[1] for c in self.ctrl.values() if c[0] == "src")

    def phi(self, pi, v):
        j, b, b2 = pi
        R = self.rounds[j]
        x = v[R.start + b - 1] if b else 0
        y = v[R.start + b2 - 1] if b2 else 0
        return (x - y) % p

    def F(self, pi, tau):
        """Offset difference of pair pi given the current partial tau (coordinates)."""
        return self.phi(pi, tau)

    def run(self, rng, deterministic=False):
        cols = self.cols
        x = [0] * len(cols)
        tau = [0] * len(self.Ub)
        ev = Counter()
        final = {}          # pi -> value of F once its control variable was drawn
        minGood = None
        fell = False        # once a fallback happened the invariants are no longer claimed
        for i, s_ in enumerate(self.src):
            bad = set()
            for pi, c in self.ctrl.items():
                if c == ("src", i):
                    A = self.F(pi, tau)
                    f = self.phi(pi, self.cs[i])
                    bad.add(A * pow(f, p - 2, p) % p)
            allowed = [t for t in Fd.P if t not in bad]
            assert len(bad) <= self.N_src[i]
            if len(Fd.P) >= self.N_src[i] + 1:
                assert allowed, "source allowed set empty although |P| >= N_src + 1"
            if not allowed:
                allowed = list(Fd.P)
                ev["src_fallback"] += 1
                fell = True
            t = allowed[0] if deterministic else rng.choice(allowed)
            x[s_] = t
            tau = [(u - t * v) % p for u, v in zip(tau, self.cs[i])]
            for pi, c in self.ctrl.items():
                if c == ("src", i):
                    final[pi] = self.F(pi, tau)
                    assert fell or final[pi] != 0
            for pi in final:          # invariance of F after its control variable
                assert self.F(pi, tau) == final[pi], "F changed after control draw (source stage)"
        for l in range(len(self.rounds) - 1, -1, -1):
            R = self.rounds[l]
            beta = [0] + tau[R.start:R.end]
            # (I1) no cross-class coincidence at level l
            for (j, b, b2) in self.pairs:
                if j == l:
                    assert fell or beta[b] != beta[b2], "cross-class coincidence at level %d" % l
                    assert final[(j, b, b2)] == (beta[b] - beta[b2]) % p
            G = good_set(beta, R.bclass)
            minGood = len(G) if minGood is None else min(minGood, len(G))
            bad = set()
            for pi, c in self.ctrl.items():
                if c == ("lev", l):
                    A = self.F(pi, tau)
                    f = self.phi(pi, self.ce[l])
                    bad.add(A * pow(f, p - 2, p) % p)
            assert len(bad) <= self.N_lev[l]
            allowed = [s for s in G if s not in bad]
            if len(G) >= self.N_lev[l] + 1:
                assert allowed, "(I2) violated"
            if not allowed:
                if not G:
                    ev["emptyGood"] += 1
                    return None, ev, minGood
                allowed = G
                ev["lev_fallback"] += 1
                fell = True
            s = allowed[0] if deterministic else rng.choice(allowed)
            for b, G_ in enumerate(R.blocks):
                for i in G_:
                    x[i] = R.delta[i] * (beta[b] + s) % p
            for q in range(R.start, R.end):
                tau[q] = 0
            tau = [(u - s * v) % p for u, v in zip(tau, self.ce[l])]
            for pi, c in self.ctrl.items():
                if c == ("lev", l):
                    final[pi] = self.F(pi, tau)
                    assert fell or final[pi] != 0
            for pi in final:
                if pi[0] < l:          # pairs at levels still to come must keep their F
                    assert self.F(pi, tau) == final[pi], "F changed after control draw (level stage)"
        assert not any(tau)
        assert check(Fd, cols, x), "invalid witness"
        return x, ev, minGood


# ---- hook ALG-T's leaf: replace sss.backward so that every leaf is captured
captured = []


def fake_backward(Fd_, cols, rounds, Ub, src, rng_):
    captured.append((cols, rounds, Ub, list(src)))
    return sss_backward_orig(Fd_, cols, rounds, Ub, src, rng_)


sss_backward_orig = SQ.sss.backward
SQ.sss.backward = fake_backward


def uniform_bank(r, M):
    while True:
        cols = [[rng.randrange(p) for _ in range(r)] for _ in range(M)]
        if rank(cols[:3 * r], p)[0] == r:
            return cols


def ec_bank(L, M):
    r = (J - 1) * L

    def rinv():
        while True:
            A = [[rng.randrange(p) for _ in range(r)] for _ in range(r)]
            if rank(A, p)[0] == r:
                return A
    A, B = rinv(), rinv()
    cols = [list(v) for v in B]
    for l in range(L):
        us = A[(J - 1) * l:(J - 1) * (l + 1)]
        while True:
            c = [rng.randrange(1, p) for _ in us]
            if len({Fd.cls((-ci) % p) for ci in c} | {0}) > 1:
                break
        w = [sum(ci * u[t] for ci, u in zip(c, us)) % p for t in range(r)]
        cols += [list(u) for u in us] + [w]
    while len(cols) < M:
        cols.append([rng.randrange(p) for _ in range(r)])
    return cols


summary = Counter()
for r in ranks:
    for fam in fams:
        for bi in range(banks):
            if fam == "EC":
                if r % (J - 1):
                    continue
                cols = ec_bank(r // (J - 1), Par.F(r))
            elif fam == "ECshuf":          # same bank, columns in uniformly random order = random scan order
                if r % (J - 1):
                    continue
                cols = ec_bank(r // (J - 1), Par.F(r))
                rng.shuffle(cols)
            else:
                cols = uniform_bank(r, Par.F(r))
            captured.clear()
            st = SQ.new_stats()
            try:
                x = SQ.solve_T(Fd, cols, Par, random.Random(rng.randrange(10 ** 9)), st)
            except AssertionError as ex:
                print("ALG-T assertion:", repr(ex)[:100])
                continue
            for (cols_, rounds, Ub, src) in captured:
                lf = Leaf(cols_, rounds, Ub, src)
                Nlev = max(lf.N_lev.values(), default=0)
                Nsrc = max(lf.N_src.values(), default=0)
                evs = Counter()
                fails = 0
                minG = None
                for _ in range(PASSES):
                    xx, ev, mg = lf.run(rng)
                    evs.update(ev)
                    fails += xx is None
                    minG = mg if minG is None else min(minG, mg if mg is not None else minG)
                xd, evd, _ = lf.run(rng, deterministic=True)
                nb = max(len(R.blocks) for R in rounds)
                H = (minG is not None and minG >= Nlev + 1 and len(Fd.P) >= Nsrc + 1)
                fb = evs["src_fallback"] + evs["lev_fallback"] + evs["emptyGood"]
                summary["leaves"] += 1
                summary["H_holds"] += H
                summary["H_holds_and_fallback"] += (H and fb > 0)
                summary["fallback_leaves"] += fb > 0
                summary["det_ok"] += xd is not None
                print("r=%2d %-7s leaf: L=%2d maxblocks=%d rho=%3d N*_lev=%2d N*_src=%2d min|Good|=%s "
                      "H(leaf)=%s | passes=%d fails=%d events=%s | deterministic: %s"
                      % (r, fam, len(rounds), nb, len(lf.pairs), Nlev, Nsrc, minG, H, PASSES, fails,
                         dict(evs), "ok" if xd is not None else "FAIL"), flush=True)
print("SUMMARY", dict(summary))

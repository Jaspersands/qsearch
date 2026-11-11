"""Scoping prototype (not the sampler): sequential importance sampling of (C1) configurations, sampling step only.
(C1): ind(s_j - t_i) = a_j + b_i (mod k) for all i, j; uniform on unordered (S, T) = uniform on ordered sequences.
Order s1, t1, s2, t2, ..., sk, tk. A new s must satisfy ind(s - t_i) - ind(s - t_1) = ind(s_1 - t_i) - ind(s_1 - t_1)
(i = 2..b); a new t must satisfy ind(s_j - t) - ind(s_1 - t) = ind(s_j - t_1) - ind(s_1 - t_1) (j = 2..a). Each step
picks uniformly among the candidates (unused points meeting the constraints); weight W = product of candidate counts
(0 on a dead end). E[W] = number of ordered (C1) sequences, so N1 = E[W] (p+1)/(p(p^2-1)) (mc_classes.py convention).
Prints: success rate, time per attempt, ESS fraction of the successes, N1/mu1 with se, per-step mean candidate counts.
Usage: nice -n 19 python -I c1_seq_proto.py k p attempts [seed]"""
import sys, math, time
import numpy as np
sys.path.insert(0, '.')
from mc_classes import primroot
k, p, n = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]); seed = int(sys.argv[4]) if len(sys.argv) > 4 else 1
assert (p - 1) % k == 0
g = primroot(p); ind = np.full(p, -1, dtype=np.int64); x = 1
for e in range(p - 1):
    ind[x] = e; x = x * g % p
chi = (ind % k).astype(np.int8); chi[0] = -1
xs = np.arange(p); rng = np.random.default_rng(seed)
t0 = time.time(); W = np.zeros(n); steps = np.zeros((n, 2 * k)); ok = 0
for a in range(n):
    used = np.zeros(p, dtype=bool)
    s1 = int(rng.integers(p)); used[s1] = True
    t1 = int(rng.choice(np.flatnonzero(~used))); used[t1] = True
    w = float(p) * (p - 1); steps[a, 0], steps[a, 1] = p, p - 1
    cs1 = chi[(s1 - xs) % p]                  # ind(s1 - x)
    ct1 = chi[(xs - t1) % p]                  # ind(x - t1)
    maskT = np.ones(p, dtype=bool); maskS = np.ones(p, dtype=bool)
    S = [s1]; T = [t1]; dead = False
    for step in range(2, 2 * k):
        side = 'S' if step % 2 == 0 else 'T'
        m = (maskS if side == 'S' else maskT) & ~used
        cand = np.flatnonzero(m); c = len(cand); steps[a, step] = c
        if c == 0:
            dead = True; break
        y = int(cand[rng.integers(c)]); w *= c; used[y] = True
        if side == 'S':
            S.append(y)                       # constrains future t: ind(y - t) - ind(s1 - t) = ind(y - t1) - ind(s1 - t1)
            tgt = (int(chi[(y - t1) % p]) - int(chi[(s1 - t1) % p])) % k
            maskT &= ((chi[(y - xs) % p].astype(np.int64) - cs1) % k) == tgt
        else:
            T.append(y)                       # constrains future s: ind(s - y) - ind(s - t1) = ind(s1 - y) - ind(s1 - t1)
            tgt = (int(chi[(s1 - y) % p]) - int(chi[(s1 - t1) % p])) % k
            maskS &= ((chi[(xs - y) % p].astype(np.int64) - ct1) % k) == tgt
    if not dead:
        S, T = np.array(S), np.array(T)       # check (C1) directly
        Mx = chi[(S[:, None] - T[None, :]) % p].astype(np.int64)
        assert (((Mx - Mx[:, :1] - Mx[:1, :] + Mx[0, 0]) % k) == 0).all()
        W[a] = w; ok += 1
dt = time.time() - t0
T1 = math.prod(range(p - k + 1, p - 1)) * math.prod(range(p - 2 * k + 1, p - k + 1)); mu1 = T1 * float(k) ** (-(k - 1) ** 2)
f = (p + 1) / (p * (p * p - 1)) / mu1
Ws = W[W > 0]; ess = Ws.sum() ** 2 / (Ws ** 2).sum() if len(Ws) else 0
print('k=%d p=%d lambda=%.3f attempts %d  successes %d (%.3f)  %.1f ms/attempt  ESS %.0f (%.2f of successes)' % (
    k, p, p / k ** (k - 1), n, ok, ok / n, 1000 * dt / n, ess, ess / max(ok, 1)))
print('  N1/mu1 = %.3f +- %.3f   (time per effective configuration %.2f s)' % (W.mean() * f, W.std(ddof=1) / math.sqrt(n) * f, dt / max(ess, 1)))
reach = (steps > 0).mean(0)
print('  mean candidates per step (over attempts reaching it): ' + ' '.join('%.3g' % (steps[steps[:, j] > 0, j].mean() if (steps[:, j] > 0).any() else 0) for j in range(2 * k)))
print('  fraction reaching each step: ' + ' '.join('%.2f' % r for r in reach))

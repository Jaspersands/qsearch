"""Check 2 (exact, finite): three copies whose central labels lie on ONE line lam_i = m_i lam_0
are jointly a linear hidden-polynomial instance, and the BCvD-type measurement
(compute Gamma(s) = sum_i C_i(s_i) in F_p^3, measure the fiber index, QFT over F_p^3)
returns theta = (delta_0, c, lam_0(v_3)) / D_0, hence the line of v_1.
Usage: python check_aligned.py p trials"""
import sys, random, numpy as np
from collections import defaultdict
from core import *

p = int(sys.argv[1]); trials = int(sys.argv[2])
rng = random.Random(7 * p)
labels = [(a, b) for a in range(p) for b in range(p) if (a, b) != (0, 0)]
i2, i6 = pow(2, -1, p), pow(6, -1, p)


def C(s, m, kap):
    im = pow(m, -1, p)
    return np.array([((-kap * s - s ** 3 * i6) * im * im) % p, (-s * s * i2 * im) % p, s % p])


stats = []; bad_lin = bad_dec = bad_sim = 0
for tr in range(trials):
    lam0 = rng.choice(labels)
    while True:
        v = random_v(p, rng)
        if Frame(lam0, 0, p).D(v):
            break
    F0 = Frame(lam0, 0, p)
    D0 = F0.D(v); iD0 = pow(D0, -1, p)
    delta0 = int(v[X] * F0.xp[Y] - v[Y] * F0.xp[X]) % p
    theta = np.array([delta0 * iD0, v[Z] * iD0, (lam0[0] * v[U] + lam0[1] * v[W]) * iD0]) % p
    ms = [rng.randrange(1, p) for _ in range(3)]; ks = [rng.randrange(p) for _ in range(3)]
    frames = [Frame(((m * lam0[0]) % p, (m * lam0[1]) % p), k, p) for m, k in zip(ms, ks)]
    # linearity: Phi_i(s) = theta . C_i(s)
    for F, m, k in zip(frames, ms, ks):
        a1, a2, a3 = F.phase_coeffs(v)
        for s in range(p):
            if (a1 * s + a2 * s * s + a3 * s ** 3 - theta @ C(s, m, k)) % p:
                bad_lin += 1; break
    # fibers of Gamma
    fib = defaultdict(list)
    for s1 in range(p):
        for s2 in range(p):
            for s3 in range(p):
                y = tuple(((C(s1, ms[0], ks[0]) + C(s2, ms[1], ks[1]) + C(s3, ms[2], ks[2])) % p))
                fib[y].append((s1, s2, s3))
    nmax = max(len(f) for f in fib.values())
    Nj = [sum(1 for f in fib.values() if len(f) > j) for j in range(nmax)]
    P_formula = sum(n * n for n in Nj) / p ** 6
    # simulate the quantum measurement on the actual product of fixed vectors
    if p <= 7 and tr < 20:
        psis = [F.fixed_vector_formula(v) for F in frames]
        state = np.einsum('a,b,c->abc', *psis)
        # outcome theta_hat = theta, fiber index j: amplitude sum_y p^{-3/2} w^{-theta.y} amp(s_j(y))
        om = np.exp(2j * np.pi / p); P_sim = 0.0
        for j in range(nmax):
            amp = 0j
            for y, f in fib.items():
                if len(f) > j:
                    amp += om ** (-(theta @ np.array(y)) % p) * state[f[j]]
            P_sim += abs(amp) ** 2 / p ** 3
        if abs(P_sim - P_formula) > 1e-9:
            bad_sim += 1
    # decode line of v_1 from theta_1 : v_1 ~ x'_0 - theta_1 y'_0
    v1hat = (F0.xp - theta[0] * F0.yp) % p
    if (v1hat[X] * v[Y] - v1hat[Y] * v[X]) % p:
        bad_dec += 1
    stats.append(P_formula)
st = np.array(stats)
print(f'p={p} trials={trials} linearity_failures={bad_lin} decode_failures={bad_dec} '
      f'sim_vs_formula_mismatch={bad_sim}  P(theta exact): min={st.min():.4f} '
      f'mean={st.mean():.4f} max={st.max():.4f}')

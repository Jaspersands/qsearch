"""Lemma 1 stress toy on Gamma = S_3 (reviewer). X: group register (6), R: 4-level
register. omega: random ENTANGLED mixed state on X (x) R. Program: random unitary on R,
controlled right translation x -> x u(r), random unitary on R, a second right
translation, readout = computational basis of R. Law must be invariant under
L_g on X for all g (hypotheses hold). Controls that violate one hypothesis each:
(c1) a left translation x -> u(r) x as segment; (c2) a segment that writes R from X
(r -> r + f(x)), i.e. r' depends on x; (c3) readout that measures X."""
import itertools, json
import numpy as np
rng = np.random.default_rng(20261105)
G = list(itertools.permutations(range(3)))
ix = {g: i for i, g in enumerate(G)}
mul = lambda a, b: tuple(a[b[i]] for i in range(3))
nX, nR = 6, 4
D = nX*nR
idx = lambda x, r: x*nR + r
def perm_op(f):
    P = np.zeros((D, D))
    for x in range(nX):
        for r in range(nR):
            P[idx(*f(x, r)), idx(x, r)] = 1
    return P
def haar(n):
    z = (rng.normal(size=(n, n)) + 1j*rng.normal(size=(n, n)))/np.sqrt(2)
    q, rr = np.linalg.qr(z); return q*(np.diag(rr)/abs(np.diag(rr)))
def on_R(U):
    return np.kron(np.eye(nX), U)
L = {g: perm_op(lambda x, r, g=g: (ix[mul(g, G[x])], r)) for g in G}
u1 = [G[i] for i in rng.integers(0, 6, nR)]; u2 = [G[i] for i in rng.integers(0, 6, nR)]
right = lambda u: perm_op(lambda x, r: (ix[mul(G[x], u[r])], r))
left = lambda u: perm_op(lambda x, r: (ix[mul(u[r], G[x])], r))
f = rng.integers(0, nR, nX)
write_R = perm_op(lambda x, r: (x, (r + f[x]) % nR))
A, B = on_R(haar(nR)), on_R(haar(nR))
def law(W, omega, readout):
    w = W @ omega @ W.conj().T
    d = np.real(np.diag(w)).reshape(nX, nR)
    return d.sum(0) if readout == "R" else d.sum(1)
K = rng.normal(size=(D, 3)) + 1j*rng.normal(size=(D, 3))
omega = K @ K.conj().T; omega /= np.trace(omega)
def spread(W, readout="R"):
    base = law(W, omega, readout)
    return max(float(np.abs(law(W, L[g] @ omega @ L[g].conj().T, readout) - base).max()) for g in G)
out = {
 "hypotheses_hold_max_dev": spread(right(u2) @ B @ right(u1) @ A),
 "c1_left_translation_segment": spread(left(u2) @ B @ left(u1) @ A),
 "c2_segment_writes_R_from_X": spread(B @ write_R @ right(u1) @ A),
 "c3_readout_on_X": spread(right(u2) @ B @ right(u1) @ A, readout="X"),
}
print(json.dumps(out, indent=1))

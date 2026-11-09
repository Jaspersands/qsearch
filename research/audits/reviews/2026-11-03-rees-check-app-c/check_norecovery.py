"""Item 3 (campaign 4): what happens without the recovery W^dag (Lemma app-sub-lcu remark).

Claim in the appendix: at d = r = 3, k = 2 the leak outside wedge^2 V is 0.500
with J = DFT and 0.093 with another completion of J.
Here: with the two-outcome measurement {|0><0|, I - |0><0|} the kept state
does not depend on the completion, because
  tr_anc[(I-P0) J^dag Y J (I-P0)] = tr_anc[(I - |f><f|) Y],   f = J|0>.
We test many completions and inputs, and also a variant that measures the
ancilla in its computational basis (that one does depend on J).
"""
import numpy as np
from check_growth import (antisym, completion, build_W, random_density_in, frame,
                          ptrace_first, ptrace_last, haar_unitary)

rng = np.random.default_rng(11)


def kept_norec(nu, d, k, J, full_measure=False):
    L = k + 1
    n = d ** (k + 1)
    W = build_W(d, k, J)
    e0 = np.zeros((L, L)); e0[0, 0] = 1
    st = W @ np.kron(e0, nu) @ W.conj().T
    if not full_measure:
        P = np.kron(np.eye(L) - e0, np.eye(n))
        rej = P @ st @ P
        pr = np.trace(rej).real
        return [(pr, ptrace_last(ptrace_first(rej, (L,), 1), d, k + 1) / pr)]
    outs = []
    for j in range(1, L):
        ej = np.zeros((L, L)); ej[j, j] = 1
        P = np.kron(ej, np.eye(n))
        b = P @ st @ P
        pr = np.trace(b).real
        if pr > 1e-12:
            outs.append((pr, ptrace_last(ptrace_first(b, (L,), 1), d, k + 1) / pr))
    return outs


for d, r, k in ((3, 3, 2), (4, 3, 2), (4, 4, 3)):
    Y = frame(d, r)
    PV = Y @ Y.conj().T
    Pk = antisym(d, k, dtype=float)
    PVk = PV
    for _ in range(k - 1):
        PVk = np.kron(PVk, PV)
    PkV = Pk @ PVk
    two, full = [], []
    for trial in range(20):
        J = completion(k + 1, ["dft", "householder", "random"][trial % 3])
        if trial >= 3:
            # arbitrary completion: J = [f | U'] with U' random on f-perp
            f = np.ones(k + 1) / np.sqrt(k + 1)
            Q = haar_unitary(k + 1)
            Q[:, 0] = f
            Q, _ = np.linalg.qr(Q)
            Q = Q * (f[0] / Q[0, 0])  # fix global phase so column 0 is f
            J = Q
            assert np.allclose(J[:, 0], f) and np.allclose(J.conj().T @ J, np.eye(k + 1))
        rank = 1 + trial % 3
        nu = np.kron(random_density_in(PkV, rank=rank), PV / r)
        pr, kept = kept_norec(nu, d, k, J)[0]
        two.append(1 - np.trace(PkV @ kept).real)
        fm = kept_norec(nu, d, k, J, full_measure=True)
        full.append(max(1 - np.trace(PkV @ s).real for _, s in fm))
    print(f"d={d} r={r} k={k}: two-outcome leak min {min(two):.4f} max {max(two):.4f};"
          f"  computational-basis leak per outcome ranges {min(full):.3f}..{max(full):.3f}")

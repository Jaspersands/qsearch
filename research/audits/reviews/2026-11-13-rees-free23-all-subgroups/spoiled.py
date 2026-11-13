"""Lemma 0' (spoiled copies), exact check on TRUE mixed states.  AI-written 2026-11-13, pending human review.
Finite check only (falsification).  Reuses the second referee's group code (read-only import).

For a hard cyclic H = <exp eta> and a label lam != 0 with lam.e = 0 ("spoiled"), the labelled copy is the mixture,
over base points g, of the label-lam component of |gH>.  Base points g = (g0, g1, gz, 0, 0) cover every coset of
K = H gamma_3 (each p times), and the label component depends on the K-coset only up to a global phase, so the
sum over these g is (a multiple of) the exact mixed state.  For each front-end outcome y = (j, k, l) we form the
exact x-register block rho_y = sum_g |phi_{g,y}><phi_{g,y}| and check Lemma 0':
  (i)  rho_y is diagonal;
  (ii) its support is R_y = {x : q_y'(x) = 0}, q_y(x) = A1 x + A2 x^2 + A3 x^3 (Lemma 0 forms, referee convention
       CONV, evaluated at the true theta), with equal weights on R_y;
  (iii) Pr[y] is proportional to |R_y| (joint law uniform on the incidence set {(y, x0) : q_y'(x0) = 0}).
Usage: python spoiled.py p n_instances seed
"""
import sys, os, numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '2026-11-13-rees-free23-theorem-referee'))
from ref_core import Field, Group, bch, FrontEnd

CONV = (-1, -1, 1)

def front_blocks(fe, psi):
    """all front-end blocks: array Fy[j, k, l, x] (unnormalised), copied from FrontEnd.run without sampling"""
    F = fe.F; p = F.p; l0, l1 = fe.lam
    Q = np.indices((p,) * 4).reshape(4, -1).T.astype(np.int64)
    amp = psi[Q[:, 0], Q[:, 1], Q[:, 2]] * F.om ** Q[:, 3]
    x = ((l0 * Q[:, 0] + l1 * Q[:, 1]) * F.inv(fe.n)) % p
    mx = np.zeros_like(Q); mx[:, 0] = (-x * fe.xp[0]) % p; mx[:, 1] = (-x * fe.xp[1]) % p
    N = fe.bchL(Q, mx)
    a = (N[:, 0] * F.inv(fe.g0[0])) % p if fe.g0[0] else (N[:, 1] * F.inv(fe.g0[1])) % p
    Psi = np.zeros((p, p, p, p), dtype=complex); Psi[a, N[:, 2], N[:, 3], x] = amp
    return np.fft.fftn(Psi, axes=(0, 1, 2))

def main():
    p, ninst, seed = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
    F = Field(p); G = Group(F); rng = np.random.default_rng(seed)
    base = np.array([[a, b, c, 0, 0] for a in range(p) for b in range(p) for c in range(p)], dtype=np.int64)
    tot_y = bad_diag = bad_supp = bad_weight = bad_law = 0; supp_sizes = {}
    for inst in range(ninst):
        while True:
            eta = rng.integers(0, p, 5)
            if eta[0] % p or eta[1] % p: break
        # spoiled labels: lam proportional to (-e1, e0)
        c = int(rng.integers(1, p)); lam = ((-c * eta[1]) % p, (c * eta[0]) % p)
        fe = FrontEnd(F, lam, rng)
        assert fe.f(eta[:2]) == 0
        rho = None; pry = np.zeros((p, p, p))
        cu, cw = np.meshgrid(np.arange(p), np.arange(p), indexing='ij')
        for g in base:
            pts = bch(np.broadcast_to(g, (p, 5)), (np.arange(p)[:, None] * eta[None]) % p, F)
            vec = np.zeros(p ** 5, dtype=complex); vec[G.idx(pts)] = 1 / np.sqrt(p)
            Fq = np.fft.fft2(vec.reshape((p,) * 5), axes=(3, 4))
            psi = Fq[:, :, :, lam[0], lam[1]]
            nrm = np.linalg.norm(psi)
            assert nrm > 1e-9
            psi = psi / nrm
            Fy = front_blocks(fe, psi)                       # (p, p, p, p)
            blk = np.einsum('jklx,jkly->jklxy', Fy, Fy.conj())
            rho = blk if rho is None else rho + blk
        tr = np.einsum('jklxx->jkl', rho).real; tr = tr / tr.sum()
        xs = np.arange(p)
        for j in range(p):
            for k in range(p):
                for l in range(p):
                    if tr[j, k, l] < 1e-12: continue
                    tot_y += 1
                    R = rho[j, k, l]; R = R / np.trace(R).real
                    off = R - np.diag(np.diag(R))
                    bad_diag += int(np.abs(off).max() > 1e-9)
                    # public forms at outcome y (convention CONV maps the front-end outcome to Lemma 0's (j, k))
                    fe.y = (j, k, l)
                    A1, A2, A3 = [int(np.asarray(a, dtype=np.int64) @ eta % p) for a in fe.A_forms(CONV)]
                    Ry = [x for x in range(p) if (A1 + 2 * A2 * x + 3 * A3 * x * x) % p == 0]
                    supp = [x for x in range(p) if R[x, x].real > 1e-9]
                    supp_sizes[len(Ry)] = supp_sizes.get(len(Ry), 0) + 1
                    bad_supp += int(supp != Ry)
                    if supp == Ry and Ry:
                        bad_weight += int(max(abs(R[x, x].real - 1 / len(Ry)) for x in Ry) > 1e-9)
                    bad_law += int(abs(tr[j, k, l] - len(Ry) / p ** 2) > 1e-9)
        print('instance %d: eta=%s lam=%s chart x\'=%s: outcomes with mass %d' % (inst, eta.tolist(), lam, fe.xp, int((tr > 1e-12).sum())), flush=True)
    print('SUMMARY p=%d: %d (instance, y) blocks; non-diagonal %d; support != R_y %d; unequal weights %d; '
          'Pr[y] != |R_y|/p^2 %d; |R_y| histogram %s' % (p, tot_y, bad_diag, bad_supp, bad_weight, bad_law, supp_sizes))

if __name__ == '__main__':
    main()

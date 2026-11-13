"""End-to-end exact simulation of Algorithm A of Theorem F23 (route A) with TRUE states and TRUE measurements.
AI-written, pending human review; imports nothing from the audited folders.

Per attempt: two runs + eta_c step + verification, exactly as in sec. 5 of the target:
  run:  sigma uniform in Aut(free23); every copy is a true labelled copy of H (coset state, random base point,
        label sampled), then U_sigma is applied to the dense state;  3 level-2 states, each from m = 9 g3^2
        admissible triples; Lemma-B weights from the labels' power sums; IS front ends (own code); S measured;
        level-2 coset measured (exact sampling of the quotient outcome); public Q3 (Lemma W); level 3 with
        Lemma C's choice of u' on the conic; public R; QFT over F_p^2; z sampled from |FFT|^2 of the true state;
        equation l = (z - a, -C); pulled back by T_sigma^T.
  solve eps ~ l1 x l2; eta_c from 2 copies with independent labels (restriction to K-hat cosets via a canonical
        transversal, then Fourier over K-hat = F_p^3); verification: phase estimation of R_hhat on 2 fresh copies
        (pass probability computed exactly, then sampled).
NO conditioning on H: spoiled copies (lam'.e' = 0) are NOT avoided.  The truth is used only for diagnostics.
Usage: python e2e.py p n_attempts seed"""
import sys, itertools, time, numpy as np
from ref_core import *

CONV = (-1, -1, 1)          # fitted in check_lemma0.py; asserted again here on every non-spoiled copy

def theta_of(eta): return np.asarray(eta, dtype=np.int64)          # (e0, e1, e3, cU, cW)

class Run:
    def __init__(s, F, G, rng, eta, stats):
        s.F, s.G, s.rng, s.eta, s.st = F, G, rng, np.asarray(eta) % F.p, stats

    def copy(s, S):
        s.st['copies'] += 1
        return labelled_copy(s.G, s.eta, s.rng, S)

    def level2_state(s, S, etap):
        F, p, rng = s.F, s.F.p, s.rng; m = 9 * g3(p) ** 2
        trips = []
        while len(trips) < m:
            cps = [s.copy(S) for _ in range(3)]
            labs = [c[0] for c in cps]
            if admissible(labs, p): trips.append(cps)
            else: s.st['inadmissible_batches'] += 1
        data = [triple_data([c[0] for c in t], F) for t in trips]
        u = level2_weights([d[1] for d in data], [d[2] for d in data], F, rng)
        supp = [j for j in range(m) if u[j]]
        T = []
        for j in supp:
            sj = data[j][0]; fes = []; phis = []
            for (lam, psi) in trips[j]:
                fe = FrontEnd(F, lam, rng); y, phi = fe.run(psi, rng)
                spoiled = fe.f(etap[:2]) == 0
                s.st['spoiled_copies'] += int(spoiled)
                if not spoiled:
                    E = phase_exponents(phi, F)
                    assert not (lemma0_predict(fe, etap, CONV, F) - E).any(), 'Lemma 0 violated'
                fes.append(fe); phis.append(phi)
            # triple product state, S = sum n_i x_i measured exactly
            Phi = np.einsum('a,b,c->abc', *phis)
            ns = [fe.n for fe in fes]
            X3 = np.indices((p, p, p)).reshape(3, -1).T
            Sv = (X3 @ np.array(ns)) % p
            pr = np.bincount(Sv, weights=(np.abs(Phi.ravel()) ** 2), minlength=p); pr = pr / pr.sum()
            r = int(rng.choice(p, p=pr))
            xr = [r * F.inv(ns[0]) % p, 0, 0]
            # plane parametrisation a in F_p^2 -> x_r + (s_i f_i(a))_i ; chi(a)
            A = np.indices((p, p)).reshape(2, -1).T
            coords = [(xr[i] + sj[i] * ((fes[i].lam[0] * A[:, 0] + fes[i].lam[1] * A[:, 1]) * F.inv(fes[i].n))) % p for i in range(3)]
            assert ((np.array(ns) @ np.array(coords)) % p == r).all()
            chi = Phi[coords[0], coords[1], coords[2]].reshape(p, p)
            assert abs((np.abs(chi) ** 2).sum() - pr[r] * (np.abs(Phi) ** 2).sum()) < 1e-9   # covers the fibre
            chi = chi / np.linalg.norm(chi)
            T.append(dict(fes=fes, s=sj, xr=xr, r=r, chi=chi, u=u[j]))
        # level-2 coset measurement of {(u_j w)_j} in the a-coordinates: sample a_j/u_j, report differences
        bs = []
        for t in T:
            W = np.indices((p, p)).reshape(2, -1).T
            pr = np.abs(t['chi'][(t['u'] * W[:, 0]) % p, (t['u'] * W[:, 1]) % p]) ** 2
            bs.append(W[int(rng.choice(p * p, p=pr / pr.sum()))])
        d = [(b - bs[0]) % p for b in bs]
        W1, W2 = np.meshgrid(np.arange(p), np.arange(p), indexing='ij')
        Psi = np.ones((p, p), dtype=complex)
        for t, dj in zip(T, d):
            Psi = Psi * t['chi'][(t['u'] * (W1 + dj[0])) % p, (t['u'] * (W2 + dj[1])) % p]
            # public base coordinates X_ji at w = 0
            t['X'] = [int((t['xr'][i] + t['s'][i] * (t['fes'][i].lam[0] * t['u'] * dj[0] + t['fes'][i].lam[1] * t['u'] * dj[1]) * F.inv(t['fes'][i].n)) % p) for i in range(3)]
        Psi = Psi / np.linalg.norm(Psi)
        st = dict(T=T, Psi=Psi, supp=len(supp), labs=[c[0] for t in trips for c in t], supp_labs=[fe.lam for t in T for fe in t['fes']])
        s.public_level2(st)
        Psi = Psi * F.om ** s.qeval(st['q'], W1, W2); st['Psi'] = Psi / np.linalg.norm(Psi)
        return st

    @staticmethod
    def qeval(q, W1, W2): return (q[0] * W1 ** 3 + q[1] * W1 ** 2 * W2 + q[2] * W1 * W2 ** 2 + q[3] * W2 ** 3)

    def public_level2(s, st):
        F, p = s.F, s.F.p
        Mq = [[3, 0, 0, 0], [0, 2, 0, 0], [0, 0, 1, 0], [0, 1, 0, 0], [0, 0, 2, 0], [0, 0, 0, 3]]
        T6 = [0] * 6
        Bf = [[0] * 5 for _ in range(2)]       # B(w, e): Bf[b] = theta-form coefficient of w_b
        for t in st['T']:
            uj = int(t['u'])
            for i, fe in enumerate(t['fes']):
                A1, A2, A3 = [[int(x) for x in A] for A in fe.A_forms(CONV)]
                fn = F.inv(fe.n); fv = [int(fe.lam[0]) * fn % p, int(fe.lam[1]) * fn % p]
                si = int(t['s'][i]); X = t['X'][i]
                c = 3 * pow(uj, 3, p) * pow(si, 3, p)
                mono = [fv[0] * fv[0], 2 * fv[0] * fv[1], fv[1] * fv[1]]
                for a in range(2):
                    for k in range(3): T6[3 * a + k] = (T6[3 * a + k] + c * A3[a] * mono[k]) % p
                cB = uj * uj * si * si % p
                for b in range(2):
                    for th in range(5): Bf[b][th] = (Bf[b][th] + cB * fv[b] * (A2[th] + 3 * A3[th] * X)) % p
        q = solve_mod(Mq, [(-x) % p for x in T6], p)
        assert q is not None, 'Lemma W: no public Q3'
        assert all(Bf[b][th] == 0 for b in range(2) for th in (2, 3, 4)), 'E3 / eta_c part of B nonzero'
        st['q'] = q; st['B'] = [[Bf[b][a] for a in range(2)] for b in range(2)]     # B[b][a]: w_b e_a
        st['c'] = (st['B'][0][1] - st['B'][1][0]) % p
        # D: e3-coefficient of the tau-coefficient at the base point (and the full tau-form, for mu)
        st['D'] = s.tau_form(st, (0, 0))[2]
        # Lemma C0 closed form (in this convention: k -> -k, global sign -1): D = -sum_j u_j sum_i s_ji (n_ji X_ji + k_ji)
        Dc = (-sum(int(t['u']) * int(t['s'][i]) * (int(fe.n) * t['X'][i] + fe.y[1]) for t in st['T'] for i, fe in enumerate(t['fes']))) % p
        s.st['C0_closed_form_fail'] = s.st.get('C0_closed_form_fail', 0) + int(Dc != st['D'])

    def tau_form(s, st, wl):
        """theta-form of the tau-coefficient of Phi_l + q_l along e at the point wl (level-2 variable)."""
        F, p = s.F, s.F.p; out = [0] * 5
        for t in st['T']:
            uj = int(t['u'])
            for i, fe in enumerate(t['fes']):
                A1, A2, A3 = [[int(x) for x in A] for A in fe.A_forms(CONV)]
                fn = F.inv(fe.n); si = int(t['s'][i])
                Y = (t['X'][i] + uj * si * (int(fe.lam[0]) * wl[0] + int(fe.lam[1]) * wl[1]) * fn) % p
                for th in range(5): out[th] = (out[th] + uj * si * (A1[th] + 2 * A2[th] * Y + 3 * A3[th] * Y * Y)) % p
        q = st['q']; w0, w1 = int(wl[0]), int(wl[1])
        g0 = (3 * q[0] * w0 * w0 + 2 * q[1] * w0 * w1 + q[2] * w1 * w1) % p
        g1 = (q[1] * w0 * w0 + 2 * q[2] * w0 * w1 + 3 * q[3] * w1 * w1) % p
        out[0] = (out[0] + g0) % p; out[1] = (out[1] + g1) % p
        return out

    def go(s):
        F, G, p, rng = s.F, s.G, s.F.p, s.rng
        S = random_aut(F, rng); etap = (S @ s.eta) % p; Tsig = S[:3, :3] % p
        states = [s.level2_state(S, etap) for _ in range(3)]
        lines = set()
        for st in states:
            for lam in st['supp_labs']:
                l = (int(lam[0]) % p, int(lam[1]) % p)
                # line ker(lam.) in P^1 as a normalised representative of g0 = (l1, -l0)
                v = (l[1], (-l[0]) % p); k = next(x for x in v if x); iv = F.inv(k)
                lines.add(((v[0] * iv) % p, (v[1] * iv) % p))
        spoiled = any((int(lam[0]) * int(etap[0]) + int(lam[1]) * int(etap[1])) % p == 0 for st in states for lam in st['supp_labs'])
        cs = [st['c'] for st in states]; D = [st['D'] for st in states]
        good = []
        for up in itertools.product(range(p), repeat=3):
            if not any(up) or next(x for x in up if x) != 1: continue
            if sum(c * x * x for c, x in zip(cs, up)) % p: continue
            if sum(dd * x for dd, x in zip(D, up)) % p: good.append(up)
        if not good:
            print('     debug D=%s c=%s supp=%s' % (D, cs, [st['supp'] for st in states]))
            return dict(ok=False, why='C forced 0', spoiled=spoiled, nB=len(lines))
        up = good[int(rng.integers(len(good)))]
        # R = -Sym(sum u'^2 B_l)
        Bs = [[sum(up[l] ** 2 * states[l]['B'][b][a] for l in range(3)) % p for a in range(2)] for b in range(2)]
        assert (Bs[0][1] - Bs[1][0]) % p == 0
        r = [(-Bs[0][0]) % p, (-2 * Bs[0][1]) % p, (-Bs[1][1]) % p]
        act = [l for l in range(3) if up[l]]
        W = np.indices((p, p)).reshape(2, -1).T
        bs = {}
        for l in act:
            pr = np.abs(states[l]['Psi'][(up[l] * W[:, 0]) % p, (up[l] * W[:, 1]) % p]) ** 2
            bs[l] = W[int(rng.choice(p * p, p=pr / pr.sum()))]
        W1, W2 = np.meshgrid(np.arange(p), np.arange(p), indexing='ij')
        Psi = np.ones((p, p), dtype=complex); mu = [0] * 5
        for l in act:
            dl = (bs[l] - bs[act[0]]) % p; wl = (up[l] * dl) % p
            Psi = Psi * states[l]['Psi'][(wl[0] + up[l] * W1) % p, (wl[1] + up[l] * W2) % p]
            tf = s.tau_form(states[l], wl)
            for th in range(5): mu[th] = (mu[th] + up[l] * tf[th]) % p
        Psi = Psi * F.om ** ((r[0] * W1 ** 2 + r[1] * W1 * W2 + r[2] * W2 ** 2) % p); Psi = Psi / np.linalg.norm(Psi)
        assert mu[3] == 0 and mu[4] == 0, 'eta_c in mu'
        C = mu[2]; assert C == sum(up[l] * D[l] for l in range(3)) % p, 'Lemma C0 closed form'
        prob = np.abs(np.fft.fft2(Psi) / p) ** 2
        mu_true = (mu[0] * etap[0] + mu[1] * etap[1] + C * etap[2]) % p
        Z = np.indices((p, p)).reshape(2, -1).T
        on = ((Z @ etap[:2]) % p == mu_true)
        mass_on = float(prob.ravel()[on].sum())
        z = Z[int(rng.choice(p * p, p=prob.ravel() / prob.sum()))]
        ell = np.array([(z[0] - mu[0]) % p, (z[1] - mu[1]) % p, (-C) % p], dtype=np.int64)
        ellp = (Tsig.T @ ell) % p
        holds = int(ellp @ s.eta[:3] % p == 0)
        return dict(ok=True, ell=ellp, holds=holds, mass_on=mass_on, spoiled=spoiled, nB=len(lines),
                    supp=[st['supp'] for st in states])

# ---------------- eta_c step and verification on true states ----------------
def etac_step(F, G, rng, eta, epsh, stats):
    """2 copies with independent labels; restriction to cosets of K-hat = exp(F_p eta_V-hat) gamma_3 via a canonical
    transversal; Fourier over K-hat.  Returns eta_c-hat (or None)."""
    p = F.p; etaV = np.array([epsh[0], epsh[1], epsh[2], 0, 0], dtype=np.int64) % p
    i0 = 0 if etaV[0] else 1
    rows = []; vals = []
    while True:
        stats['copies'] += 1
        lam, psi = labelled_copy(G, eta, rng)
        if lam == (0, 0): continue
        if rows and det2(rows[0], lam) % p == 0: continue
        vec = dense_from_label(lam, psi, F)
        A = G.ALL; t = (A[:, i0] * F.inv(etaV[i0])) % p
        rfull = bch(A, (-t[:, None] * etaV[None]) % p, F)          # g * exp(-t eta_V) = r * c_r
        assert (rfull[:, i0] == 0).all()
        cr = rfull[:, 3:5]; rr = rfull[:, [1 - i0, 2]]
        cnt = np.zeros((p,) * 5, dtype=np.int64); np.add.at(cnt, (rr[:, 0], rr[:, 1], t, cr[:, 0], cr[:, 1]), 1)
        assert (cnt == 1).all()
        kU = cr[:, 0]; kW = cr[:, 1]
        arr = np.zeros((p, p, p, p, p), dtype=complex)                # (r-coords, t, kU, kW)
        arr[rr[:, 0], rr[:, 1], t, kU, kW] = vec
        Fk = np.fft.fftn(arr, axes=(2, 3, 4))
        pr = (np.abs(Fk) ** 2).sum(axis=(0, 1)).ravel(); pr = pr / pr.sum()
        k = int(rng.choice(p ** 3, p=pr)); tau, k0, k1 = np.unravel_index(k, (p, p, p))
        stats['etac_maxprob'] = min(stats.get('etac_maxprob', 1.0), float(pr.max()))
        # chi(exp(t eta_V) c) = w^{lam.c - t lam(eta_c)}: Fourier peak at (tau, kappa) = (-lam(eta_c), lam)
        rows.append(lam); vals.append((-int(tau)) % p)
        if len(rows) == 2: break
    sol = solve_mod([list(r) for r in rows], vals, p)
    return None if sol is None else np.array(sol, dtype=np.int64)

def verify(F, G, rng, eta, etah, stats, ncop=2):
    p = F.p; ok = True; pmax = 0.0
    shifts = [G.idx(bch(G.ALL, np.broadcast_to((t * etah) % p, G.ALL.shape), F)) for t in range(p)]
    for _ in range(ncop):
        stats['copies'] += 1
        lam, psi = labelled_copy(G, eta, rng); vec = dense_from_label(lam, psi, F)
        # <psi| R_{h^t} |psi>, R_x|g> = |g x>
        amp = sum(np.vdot(vec[sh], vec) for sh in shifts) / p
        ppass = float(np.real(amp)); pmax = max(pmax, ppass)
        if rng.random() >= ppass: ok = False
    return ok, pmax

def proportional(a, b, p): return all((a[i] * b[j] - a[j] * b[i]) % p == 0 for i in range(3) for j in range(3))

def main():
    p, natt, seed = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
    F = Field(p); G = Group(F); rng = np.random.default_rng(seed)
    stats = dict(copies=0, inadmissible_batches=0, spoiled_copies=0)
    agg = dict(attempts=0, success=0, wrong_output=0, no_output=0, runs=0, run_ok=0, run_holds=0, run_spoiled=0,
               run_unspoiled_holds=0, run_unspoiled=0, run_spoiled_holds=0, C_forced0=0, prop=0, verif_reject_correct=0,
               mass_on_unspoiled_min=1.0)
    t0 = time.time()
    while True:
        eta = rng.integers(0, p, 5)
        if eta[0] % p or eta[1] % p: break
    print('p=%d, m=%d triples per level-2 state, hidden eta=%s (one H for the whole experiment)' % (p, 9 * g3(p) ** 2, eta.tolist()), flush=True)
    for att in range(natt):
        agg['attempts'] += 1; eqs = []
        for rr in range(2):
            R = Run(F, G, rng, eta, stats).go(); agg['runs'] += 1
            agg['run_spoiled'] += int(R['spoiled'])
            if not R['ok']: agg['C_forced0'] += 1; print('   run: C forced 0 (spoiled %s)' % R['spoiled'], flush=True); continue
            agg['run_ok'] += 1; agg['run_holds'] += R['holds']
            if R['spoiled']: agg['run_spoiled_holds'] += R['holds']
            else:
                agg['run_unspoiled'] += 1; agg['run_unspoiled_holds'] += R['holds']
                agg['mass_on_unspoiled_min'] = min(agg['mass_on_unspoiled_min'], R['mass_on'])
            eqs.append(R['ell'])
            print('   run: supp %s, |B| = %d, spoiled %s, eq %s holds %d, mass on predicted line %.6f' %
                  (R['supp'], R['nB'], R['spoiled'], R['ell'].tolist(), R['holds'], R['mass_on']), flush=True)
        out = None
        if len(eqs) == 2:
            if proportional(eqs[0], eqs[1], p): agg['prop'] += 1
            x = np.cross(eqs[0], eqs[1]) % p
            if x.any() and (x[0] or x[1]):
                etac = etac_step(F, G, rng, eta, x, stats)
                if etac is not None:
                    etah = np.array([x[0], x[1], x[2], etac[0], etac[1]]) % p
                    ok, pm = verify(F, G, rng, eta, etah, stats)
                    correct = all((etah[i] * eta[j] - etah[j] * eta[i]) % p == 0 for i in range(5) for j in range(5))
                    if correct and not ok: agg['verif_reject_correct'] += 1
                    if ok: out = (etah, correct)
                    print('  attempt %d: candidate %s correct %s, verification pass-prob max %.4f, passed %s' %
                          (att, etah.tolist(), correct, pm, ok), flush=True)
        if out is None: agg['no_output'] += 1; print('  attempt %d: no output' % att, flush=True)
        elif out[1]: agg['success'] += 1
        else: agg['wrong_output'] += 1
    print('SUMMARY p=%d: %s; copies %s; wall %.0f s' % (p, agg, stats, time.time() - t0), flush=True)

if __name__ == '__main__':
    main()

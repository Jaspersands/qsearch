"""Structure of the HYP1 (line of v_1) state of a dependent pair (lam, c lam), c not in {0,-1}, after the lossless
merge (measure r: x1 = r - c x, x2 = x).  Claim (Lemma K): averaging over the nuisance e3 leaves coherence only inside
two-point orbits {x, 2 x0 - x} (x0 known from r and the IS block labels), and the off-diagonal phase is
    theta(u) = beta * K(u) + K0(u)   (mod p),   u = x - x0,
with beta the chart slope of the line of v_1 and K, K0 independent of beta, |off-diagonal| independent of beta.
That is a dihedral-type (Kuperberg) hidden-shift qubit in beta with a known label K(u).
(AI-written, pending human review; exact up to float round-off; finite check only.)
"""
import sys, os, itertools, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from isbasis import Chart, all_etas                       # noqa: E402
from pairmeas import copy_data, _cols                     # noqa: E402
from lemma_s import beta as beta_of                       # noqa: E402


def main(p, c):
    lams = [(1, 0), (c, 0)]; F1, E = all_etas(p); charts = [Chart(p, l) for l in lams]
    per = [copy_data(ch, E) for ch in charts]
    nh1 = len(F1); d = (-c) % p
    R_, X_ = np.meshgrid(np.arange(p), np.arange(p), indexing='ij'); perm = (((R_ + d * X_) % p) * p + X_).ravel()
    gen = [l for l in range(nh1) if all(dd['pure'][l * p ** 3] for dd in per)]
    betas = {l: int(beta_of(charts[0], np.array(F1[l]))) for l in gen}
    stats = dict(blocks=0, support_bad=0, center_bad=0, mod_bad=0, lin_bad=0, Knonzero=0, pairs=0)
    probs = []        # rows: outcome probabilities (weight-scaled) for each generic line, outcomes = (block, orbit, bit)
    wts = []
    for (i1, (y1, _)), (i2, (y2, _)) in itertools.product(list(enumerate(per[0]['reps'])), list(enumerate(per[1]['reps']))):
        Ms = {}
        for l in gen:
            sl = slice(l * p ** 3, (l + 1) * p ** 3)            # all e3, eta_c of this line
            parts = [_cols(per[i]['pure'][sl], per[i]['amp'][sl, ii][:, None], per[i]['diag'][sl, ii][:, None], p)[:, 0]
                     for i, ii in ((0, i1), (1, i2))]
            V = np.einsum('nam,nbq->abnmq', *parts).reshape(p * p, -1)
            R = (V @ V.conj().T) / p ** 3
            Q = R[perm][:, perm].reshape(p, p, p, p)
            Ms[l] = np.einsum('rarb->rab', Q)                    # (r, x, x')
        w = per[0]['reps'][i1][1] * per[1]['reps'][i2][1]
        for r in range(p):
            stats['blocks'] += 1
            # orbit + X-basis measurement (orbits from the H-independent support of the generic-line states)
            refm = Ms[gen[0]][r]; offm = np.abs(refm - np.diag(np.diag(refm))) > 1e-12
            done = set(); outs = []
            for x in range(p):
                if x in done: continue
                if offm[x].any():
                    xp = int(np.argmax(offm[x])); done.update({x, xp})
                    for sg in (1, -1):
                        outs.append([np.real(Ms[l][r][x, x] + Ms[l][r][xp, xp] + sg * 2 * np.real(Ms[l][r][x, xp])) / 2 for l in gen])
                else:
                    done.add(x); outs.append([np.real(Ms[l][r][x, x]) for l in gen])
            probs.extend(outs); wts.extend([w] * len(outs))
            ref = Ms[gen[0]][r]
            off = np.abs(ref - np.diag(np.diag(ref))) > 1e-12
            if (off.sum(axis=1) > 1).any(): stats['support_bad'] += 1; continue
            xs = [x for x in range(p) if off[x].any()]
            partners = {x: int(np.argmax(off[x])) for x in xs}
            centers = {((x + partners[x]) * pow(2, -1, p)) % p for x in xs}
            if len(centers) > 1: stats['center_bad'] += 1; continue
            for x in xs:
                xp = partners[x]
                if x > xp: continue
                stats['pairs'] += 1
                vals = np.array([Ms[l][r][x, xp] for l in gen])
                if np.abs(np.abs(vals) - np.abs(vals[0])).max() > 1e-12: stats['mod_bad'] += 1; continue
                th = (np.round(np.angle(vals) / (2 * np.pi) * p).astype(int)) % p
                if np.abs(np.exp(2j * np.pi * th / p) * np.abs(vals[0]) - vals).max() > 1e-10: stats['lin_bad'] += 1; continue
                b = np.array([betas[l] for l in gen])
                # fit th = K*b + K0 mod p
                K = ((th[1] - th[0]) * pow(int((b[1] - b[0]) % p), -1, p)) % p
                if (((K * b + th[0] - K * b[0]) - th) % p).any(): stats['lin_bad'] += 1
                stats['Knonzero'] += int(K != 0)
    P = np.array(probs).T                     # (lines, outcomes), each row sums to 1/(weight-sum) normalisation
    wv = np.array(wts, float)
    def Hrow(q):
        q = np.where(q > 1e-300, q, 1.0); return float(-(wv * q * np.log2(q)).sum())
    mi = Hrow(P.mean(axis=0)) - np.mean([Hrow(q) for q in P])
    succ = float((wv * P.max(axis=0)).sum()) / len(gen)
    stats['orbitX_MI_HYP1g'] = round(mi, 4); stats['orbitX_succ_HYP1g'] = round(succ, 4)
    stats['norm'] = round(float((wv * P[0]).sum()), 6)
    return stats, len(gen)


if __name__ == '__main__':
    ps = [int(a) for a in sys.argv[1].split(',')] if len(sys.argv) > 1 else [5, 7]
    cs = [int(a) for a in sys.argv[2].split(',')] if len(sys.argv) > 2 else None
    for p in ps:
        for c in (cs or range(1, p - 1)):
            s, ng = main(p, c)
            print('p=%d c=%d (generic lines: %d): %s' % (p, c, ng, s), flush=True)

"""Which partial information about K = H gamma_3 unlocks a twist?  free23, p = 5, 7, exhaustive.

Aut(free23) acts on L/gamma_3 = span(x, y, z) and on gamma_3 = span(u, w) through the group
  {(A, b)}:  x -> a11 x + a12 y + b1 z,  y -> a21 x + a22 y + b2 z,  z -> det(A) z,
  gamma_3 -> det(A) * A   (row convention),  order |GL_2(p)| p^2  (every such map lifts: L is free).
A family F of candidate K's admits a common twist iff some g in this group fixes every K in F and
acts on gamma_3 nontrivially.  Prediction (argued in the note): for a family whose members have at
least three distinct v_1-lines this happens iff all members lie in one plane W of L/gamma_3 with
z notin W (a degree-one complement; then the dilations of the grading with L_1 = W work).
The script checks the prediction on every triple of K's, and checks the two extreme families:
all K with a given v_1-line (Prop T' situation inside one line) and all K (Prop T)."""
import itertools, json, numpy as np

def run(p):
    # group elements
    G = []
    for a11, a12, a21, a22 in itertools.product(range(p), repeat=4):
        det = (a11 * a22 - a12 * a21) % p
        if not det: continue
        for b1, b2 in itertools.product(range(p), repeat=2):
            Q = np.array([[a11, a12, b1], [a21, a22, b2], [0, 0, det]], dtype=np.int64)
            Zm = det * np.array([[a11, a12], [a21, a22]], dtype=np.int64) % p
            G.append((Q, Zm))
    # K's: lines F_p(v) in L/gamma_3 with (v_x, v_y) != 0
    Ks = []
    for v in itertools.product(range(p), repeat=3):
        if (v[0] or v[1]):
            nz = next(i for i in range(3) if v[i])
            if v[nz] == 1: Ks.append(np.array(v, dtype=np.int64))
    nK = len(Ks); KV = np.array(Ks)
    def norm(v):
        nz = next(i for i in range(3) if v[i] % p); return tuple((v * pow(int(v[nz]), -1, p) % p).tolist())
    keys = {tuple(k.tolist()): i for i, k in enumerate(Ks)}
    fix = np.zeros((len(G), nK), dtype=bool); nontriv = np.zeros(len(G), dtype=bool)
    I2 = np.eye(2, dtype=np.int64)
    for gi, (Q, Zm) in enumerate(G):
        img = KV @ Q % p
        fix[gi] = [keys[norm(r)] == i for i, r in enumerate(img)]
        nontriv[gi] = (Zm % p != I2).any()
    out = dict(p=p, group_order=len(G), K=nK)
    # single K: always a nontrivial common twist?
    out['single_K_with_twist'] = int(sum((fix[:, i] & nontriv).any() for i in range(nK)))
    # all K with the same v_1-line
    lines = {}
    for i, k in enumerate(Ks): lines.setdefault(norm(np.array([k[0], k[1], 0])), []).append(i)
    out['same_v1_family_with_twist'] = int(sum((fix[:, idx].all(1) & nontriv).any() for idx in lines.values()))
    out['v1_lines'] = len(lines)
    out['all_K_with_twist'] = bool((fix.all(1) & nontriv).any())
    # triples with three distinct v_1-lines
    v1 = [norm(np.array([k[0], k[1], 0])) for k in Ks]
    tested = mism = pos = 0
    packed = np.packbits(fix & nontriv[:, None], axis=0)      # (bytes, nK)
    for i, j, k in itertools.combinations(range(nK), 3):
        if len({v1[i], v1[j], v1[k]}) < 3: continue
        tested += 1
        has = bool((packed[:, i] & packed[:, j] & packed[:, k]).any())
        M = np.array([Ks[i], Ks[j], Ks[k]])
        coplanar = round(abs(np.linalg.det(M.astype(float)))) % p == 0
        # plane W spanned; z notin W automatically when the three v_1-lines are distinct (W maps onto L/gamma_2)
        pred = coplanar
        pos += int(has); mism += int(has != pred)
    out.update(triples_tested=tested, triples_with_twist=pos, triples_pred_mismatch=mism)
    # pairs with distinct v_1-lines: always a twist?
    pairs = [(i, j) for i, j in itertools.combinations(range(nK), 2) if v1[i] != v1[j]]
    out['pairs_distinct_v1'] = len(pairs)
    out['pairs_with_twist'] = int(sum(bool((packed[:, i] & packed[:, j]).any()) for i, j in pairs))
    print(json.dumps(out), flush=True)

if __name__ == '__main__':
    for p in (5, 7): run(p)

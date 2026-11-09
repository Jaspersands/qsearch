"""One exact source/sign/spectral falsifier plus numerical learned-frame readout.

Run with /opt/anaconda3/envs/qsearch-cas/bin/python. No scaling inference.
The decoder receives only computed moments, never the generating rotations.
"""
from itertools import combinations
from pathlib import Path
import json
import numpy as np
from sage.all import QQ, QuadraticField, matrix, vector

F = QuadraticField(-1, "ii")
ii = F.gen()


def majorana(v, a):
    j, odd = divmod(a, 2)
    out = {}
    for z, amp in v.items():
        sign = -1 if (z & ((1 << j) - 1)).bit_count() % 2 else 1
        phase = sign * (ii * (-1 if z & (1 << j) else 1) if odd else 1)
        out[z ^ (1 << j)] = amp * phase
    return out


def product(v, indices):
    for a in reversed(indices):
        v = majorana(v, a)
    return v


def rotation(v, a, b, c, s):
    w = product(v, (a, b))
    return {z: c * v.get(z, 0) + s * w.get(z, 0) for z in v.keys() | w.keys()
            if c * v.get(z, 0) + s * w.get(z, 0) != 0}


def mean(v, indices):
    w = product(v, indices)
    norm = sum(a.conjugate() * a for a in v.values())
    return sum(a.conjugate() * w.get(z, 0) for z, a in v.items()) / norm


def moments(v, n):
    C = matrix(QQ, 2*n)
    for a, b in combinations(range(2*n), 2):
        C[a, b] = QQ(ii * mean(v, (a, b)))
        C[b, a] = -C[a, b]
    T = {q: QQ(-mean(v, q)) for q in combinations(range(2*n), 4)}
    return C, T


def wedge(C, q):
    a, b, c, d = q
    return C[a,b]*C[c,d] - C[a,c]*C[b,d] + C[a,d]*C[b,c]


def flatten(C, T):
    pairs = list(combinations(range(C.nrows()), 2))
    out = matrix(QQ, len(pairs))
    for r, ab in enumerate(pairs):
        for s, cd in enumerate(pairs):
            q = ab + cd
            if len(set(q)) < 4:
                continue
            sign = (-1)**sum(q[i] > q[j] for i in range(4) for j in range(i+1,4))
            sortedq = tuple(sorted(q))
            out[r,s] = sign * (T[sortedq] - wedge(C, sortedq))
    return out, pairs


def canonical_frame(J, B):
    """Only recovered real matrices, no source rotation or branch bits."""
    cols = []
    for A in (J, B):
        for seed in np.eye(len(J)):
            v = -A @ A @ seed
            for u in cols:
                v -= np.dot(u, v) * u
            if np.linalg.norm(v) < 1e-9:
                continue
            v /= np.linalg.norm(v)
            w = -A @ v
            cols += [v, w]
    Q = np.column_stack(cols)
    if np.linalg.det(Q) < 0:
        Q[:, -1] *= -1
    assert np.linalg.norm(Q.T @ Q - np.eye(len(Q))) < 1e-10
    return Q


def apply_majorana_array(v, a):
    j, odd = divmod(a, 2)
    out = np.zeros_like(v)
    for z, amp in enumerate(v):
        sign = -1 if (z & ((1 << j)-1)).bit_count() % 2 else 1
        phase = sign * (1j * (-1 if z & (1 << j) else 1) if odd else 1)
        out[z ^ (1 << j)] = phase * amp
    return out


def apply_gaussian(v, R):
    A = R.copy()
    rotations = []
    for j in range(len(A)-1):
        for b in range(len(A)-1, j, -1):
            a = b-1
            r = np.hypot(A[a,j], A[b,j])
            if r < 1e-12:
                continue
            c, s = A[a,j]/r, A[b,j]/r
            A[[a,b],:] = np.array([[c,s],[-s,c]]) @ A[[a,b],:]
            rotations.append((a,b,-np.arctan2(s,c)))
    assert np.linalg.norm(A - np.eye(len(A))) < 1e-9
    for a,b,angle in reversed(rotations):
        w = apply_majorana_array(apply_majorana_array(v,b),a)
        v = np.cos(angle/2)*v + np.sin(angle/2)*w
    return v, len(rotations)


def dense(v, n):
    out = np.zeros(2**n, dtype=complex)
    for z, amp in v.items():
        out[z] = complex(amp)
    return out / np.linalg.norm(out)


n, k = 7, 6
source_rotations = [(0,12), (1,7), (4,13), (8,3)]
branches = []
for z in (0, (1<<k)-1):
    v = {z: F(1)}
    for a,b in source_rotations:
        v = rotation(v,a,b,QQ(3)/5,QQ(4)/5)
    branches.append(v)
v = {z: branches[0].get(z,0)+ii*branches[1].get(z,0)
     for z in branches[0].keys() | branches[1].keys()}
v_other_phase = {z: branches[0].get(z,0)+branches[1].get(z,0)
                 for z in branches[0].keys() | branches[1].keys()}
C,T = moments(v,n)
assert (C,T) == moments(v_other_phase,n)
C0,T0 = moments(branches[0],n)
C1,T1 = moments(branches[1],n)
assert all(T0[q] == wedge(C0,q) and T1[q] == wedge(C1,q) for q in T)
assert C == (C0+C1)/2
assert all(T[q] == (T0[q]+T1[q])/2 for q in T)
K,pairs = flatten(C,T)
poly = K.charpoly()
x = poly.parent().gen()
assert poly == x**25 * (x-5) * (x-1)**30 * (x+1)**35
measured_top = max(root for root, multiplicity in poly.roots(QQ))
ker = (K-measured_top).right_kernel()
assert ker.dimension() == 1
vtop = ker.basis()[0]
scale = (QQ(k)/vtop.dot_product(vtop)).sqrt()
J = matrix(QQ,2*n)
for (a,b), val in zip(pairs, vtop):
    J[a,b] = scale*val
    J[b,a] = -J[a,b]
assert J == (C0-C1)/2 or J == (C1-C0)/2
P = -J*J
assert P*P == P and P.rank() == 2*k and C*J == 0

# Matched supplied-description baseline: Gaussian branch Wick/Pfaffian
# moments above reproduce all low-order data classically. Coherent phase
# requires the learned frame readout, not that low-order mixture.
B = (1-P)*C*(1-P)
Jnum, Bnum = np.array(J,dtype=float), np.array(B,dtype=float)
Q = canonical_frame(Jnum,Bnum)
Gamma = [Bnum+Jnum,Bnum-Jnum]
strings = []
for g in Gamma:
    gdec = Q.T @ g @ Q
    bits = [int(gdec[2*j,2*j+1] > 0) for j in range(n)]
    strings.append(sum(b<<j for j,b in enumerate(bits)))
decoded, gates = apply_gaussian(dense(v,n),Q.T)
block = np.outer(decoded[strings],decoded[strings].conjugate())
weight = float(np.trace(block).real)
vals,vecs = np.linalg.eigh(block)
learned_core = vecs[:,-1]
learned = np.zeros(2**n,dtype=complex)
learned[strings] = learned_core
learned,_ = apply_gaussian(learned,Q)
fidelity = float(abs(np.vdot(dense(v,n),learned))**2)
assert weight > 1-1e-10 and fidelity > 1-1e-10
assert abs(block[0,1]) > .49

# Exact k4 countercontrol: coherent quartic term invalidates mixture formula.
v4={0:F(1),15:F(1)}
C4,T4=moments(v4,4)
g4,_=moments({0:F(1)},4)
cross=(0,2,4,6)
assert C4.is_zero() and T4[cross] != wedge(g4,cross)
# k2 covariance mixture also fails: the state itself remains Gaussian.
C2,_=moments({0:F(1),3:F(1)},2)
assert not C2.is_zero() and C2*C2 == -matrix.identity(QQ,4)
result={
    "status":"passed", "n":n,"active_modes":k,"input_phase":"i",
    "exact_spectrum":{"5":1,"1":30,"-1":35,"0":25},
    "raw_wick_sign_and_classical_branch_baseline":True,
    "low_moments_phase_blind":True,"exact_top_recovers_active_J":True,
    "decoder_uses_only_moments":True,"learned_frame_givens":gates,
    "decoded_strings":strings,"span_weight":weight,"output_fidelity":fidelity,
    "k4_mixture_countercontrol":True,"k2_covariance_countercontrol":True,
    "full_learner_executed":False,"sampling_complexity_verified_by_test":False,
    "quantum_execution":False,"novelty":False,"classical_separation":False}
Path(__file__).with_suffix('.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result))

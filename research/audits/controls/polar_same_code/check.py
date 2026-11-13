"""One exact finite convention fixture; no asymptotic inference or parameter sweep.
Run with /opt/anaconda3/envs/qsearch-cas/bin/python.
"""
from sage.all import QQ, GF, matrix, vector, diagonal_matrix, identity_matrix, zero_matrix
from itertools import product
from pathlib import Path
import json

REPO = Path('/Users/jaspersands/Developer/qsearch')
OUT = REPO / 'research/audits/controls/polar_same_code'
N = 4
alpha = QQ(1)/4
F = (0, 2)
states = list(product((0, 1), repeat=N))
field = GF(2)
kernel = matrix(field, [[1, 0], [1, 1]])
G = kernel.tensor_product(kernel)
J = matrix(field, N, N, lambda i,j: int(j == N-1-i))
assertions = 0

def check(condition):
    global assertions
    assertions += 1
    assert condition

def transform(u):
    return tuple(int(x) for x in vector(field,u)*G)

def xor(u,v):
    return tuple(a^b for a,b in zip(u,v))

def tv(p,q):
    return sum((abs(p.get(k,QQ(0))-q.get(k,QQ(0))) for k in set(p)|set(q)),QQ(0))/2

def weight(x):
    return alpha**sum(x)*(1-alpha)**(N-sum(x))

P = {(u,y): QQ(1)/(2**N)*weight(xor(y,transform(u))) for u in states for y in states}
check(sum(P.values()) == 1)
# Exact posterior of each bit for every public y and observed prefix.
posterior = {}
prefix_mass = {}
for i in range(N):
    for prefix in product((0,1),repeat=i):
        for y in states:
            den = sum((P[u,y] for u in states if u[:i] == prefix),QQ(0))
            prefix_mass[i,prefix,y] = den
            for bit in (0,1):
                num = sum((P[u,y] for u in states if u[:i] == prefix and u[i] == bit),QQ(0))
                posterior[i,prefix,y,bit] = num/den
Q = {}
for u in states:
    for y in states:
        q = QQ(1)/(2**N)
        for i in range(N):
            q *= QQ(1)/2 if i in F else posterior[i,u[:i],y,u[i]]
        Q[u,y] = q
check(sum(Q.values()) == 1)
d_by_bit = []
for i in range(N):
    d_by_bit.append(sum((mass*abs(posterior[i,prefix,y,0]-QQ(1)/2)
        for (j,prefix,y),mass in prefix_mass.items() if j == i),QQ(0)))
dF = sum((d_by_bit[i] for i in F),QQ(0))
full_tv = tv(P,Q)
check(full_tv <= dF)
slices = []
zeroP = zeroQ = None
for frozen in product((0,1),repeat=len(F)):
    keys = [(u,y) for u in states for y in states if tuple(u[i] for i in F)==frozen]
    pm = sum((P[k] for k in keys),QQ(0)); qm = sum((Q[k] for k in keys),QQ(0))
    check(pm == QQ(1)/4 and qm == QQ(1)/4)
    p = {k:P[k]/pm for k in keys};q = {k:Q[k]/qm for k in keys}
    slice_tv = tv(p,q)
    check(slice_tv == full_tv)
    slices.append({'frozen':list(frozen),'P_mass':str(pm),'Q_mass':str(qm),'joint_slice_TV':str(slice_tv)})
    if frozen==(0,0):zeroP,zeroQ=p,q

# Fixed frozen assignment 00: check target identification and uniform offset law.
K = sorted(transform(u) for u in states if all(u[i]==0 for i in F))
check(len(set(K)) == 4)
offset_data = []
R = {}
pY = {}
for y in states:
    pm = sum((v for (u,z),v in zeroP.items() if z==y),QQ(0))
    qm = sum((v for (u,z),v in zeroQ.items() if z==y),QQ(0))
    pY[y]=pm
    check(qm == QQ(1)/16)
    output = {}; target_u = {}; sampler_u = {}
    for u in states:
        if not all(u[i]==0 for i in F): continue
        target_u[u] = zeroP[u,y]/pm
        sampler_u[u] = zeroQ[u,y]/qm
        R[u,y] = QQ(1)/16*target_u[u]
        output[xor(y,transform(u))] = sampler_u[u]
    coset = sorted(xor(y,k) for k in K)
    Z = sum((weight(x) for x in coset),QQ(0))
    target = {x:weight(x)/Z for x in coset}
    check(pm == QQ(1)/4*Z)
    check(all(target_u[u]==target[xor(y,transform(u))] for u in target_u))
    conditional_tv = tv(output,target)
    check(conditional_tv == tv(sampler_u,target_u))
    offset_data.append({'offset':''.join(map(str,y)),'coset': [''.join(map(str,x)) for x in coset],
                        'Z_b':str(Z),'conditional_coset_TV':str(conditional_tv)})
average_tv = sum((QQ(row['conditional_coset_TV']) for row in offset_data),QQ(0))/16
weighted_Y_tv = tv(pY,{y:QQ(1)/16 for y in states})
check(tv(zeroP,R) == weighted_Y_tv)
check(tv(zeroQ,R) == average_tv)
check(average_tv <= 2*dF)
check(average_tv <= 2*full_tv)
# Verify same conditional-TV value for all representatives of each coset.
coset_values = {}
for row in offset_data:
    key=tuple(row['coset'])
    if key in coset_values:check(coset_values[key] == row['conditional_coset_TV'])
    else:coset_values[key]=row['conditional_coset_TV']
check(G.inverse().transpose() == J*G*J)
check(G*G == identity_matrix(field,N))

# Independent exact heatbath fixture: row-generator acting on functions.
hstates = [(0,0),(0,1),(1,0),(1,1)]
moves = [(1,0),(0,1),(1,1)]
w = [QQ(1)/4**sum(x) for x in hstates]
sqrtw = [QQ(1)/2**sum(x) for x in hstates]
S = diagonal_matrix(QQ,sqrtw)
L = zero_matrix(QQ,4,4); H = zero_matrix(QQ,4,4)
for move in moves:
    for i,x in enumerate(hstates):
        j=hstates.index(xor(x,move))
        rate=w[j]/(w[i]+w[j])
        L[i,j]+=rate;L[i,i]-=rate
        if i<j:
            den=w[i]+w[j]
            H[i,i]+=w[j]/den;H[j,j]+=w[i]/den
            H[i,j]-=sqrtw[i]*sqrtw[j]/den;H[j,i]-=sqrtw[i]*sqrtw[j]/den
check(L*vector(QQ,[1]*4) == vector(QQ,[0]*4))
check(H == S*(-L)*S.inverse())
check(H == H.transpose())
check(H*vector(QQ,sqrtw) == vector(QQ,[0]*4))
check(all(w[i]*L[i,j] == w[j]*L[j,i] for i in range(4) for j in range(4)))
result = {
 'scope':'One finite exact convention check only; N4/F02/alpha1over4 and one4state heatbath. No theorem from finite controls; no sweep.',
 'exact':True,'assertions_passed':assertions,
 'polar':{'N':N,'alpha':str(alpha),'frozen_indices':list(F),'row_kernel':[[1,0],[1,1]],
  'G':[[int(x) for x in row] for row in G.rows()], 'J':[[int(x) for x in row] for row in J.rows()],
  'joint_pairs_enumerated':len(P),'d_by_bit':[str(x) for x in d_by_bit],'d_F':str(dF),'two_d_F':str(2*dF),
  'full_joint_TV':str(full_tv),'frozen_slices':slices,'weighted_Y_to_uniform_TV':str(weighted_Y_tv),
  'actual_uniform_offset_average_conditional_coset_TV':str(average_tv),'all_offsets':offset_data,
  'distinct_coset_TVs':[{'coset':list(k),'TV':v} for k,v in sorted(coset_values.items())],
  'G_inverse_transpose_equals_JGJ':True},
 'heatbath':{'states':hstates,'moves':moves,'weights':[str(x) for x in w],'S_diagonal':[str(x) for x in sqrtw],
  'L_row_generator':[[str(x) for x in row] for row in L.rows()],
  'H_independent_pair_blocks':[[str(x) for x in row] for row in H.rows()],
  'H_equals_S_negative_L_S_inverse':True,'detailed_balance':True,'symmetric_H':True,'annihilates_sqrt_weights':True},
 'issues':[]
}
with (OUT/'result.json').open('x') as f:json.dump(result,f,indent=2);f.write('\n')
print(json.dumps({'assertions':assertions,'d_by_bit':result['polar']['d_by_bit'],'dF':str(dF),'fullTV':str(full_tv),
 'sliceTVs':[x['joint_slice_TV'] for x in slices],'average_cosetTV':str(average_tv),'two_dF':str(2*dF),
 'weighted_Y_TV':str(weighted_Y_tv),'distinct_coset_TVs':result['polar']['distinct_coset_TVs'],'heatbath_similarity':True,'issues':[]},indent=2))

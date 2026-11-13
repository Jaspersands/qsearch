from sage.all import QQ, QuadraticField, matrix, vector, identity_matrix
from pathlib import Path
import json
K=QuadraticField(-1,'ii'); ii=K.gen(); size=16
ann=[]
for j in range(4):
    a=matrix(K,size,size)
    for b in range(size):
        if b&(1<<j): a[b^(1<<j),b]=(-1)**((b&((1<<j)-1)).bit_count())
    ann.append(a)
maj=[]
for a in ann: maj.extend([a+a.conjugate_transpose(),-ii*(a-a.conjugate_transpose())])
def state(terms):
    v=vector(K,size)
    for word,c in terms.items(): v[sum(1<<j for j in word)]=c
    return v
def expectation(v,A):
    return (v.conjugate().dot_product(A*v))/(v.conjugate().dot_product(v))
def cov(v):
    return matrix(K,8,8,lambda j,k:0 if j==k else ii*expectation(v,maj[j]*maj[k]))
O=state({(0,3):9,(1,2):-16}); E=state({(0,1):1,(2,3):1})
Phi=12*E+O
assert Phi.dot_product(Phi)==625 and O.dot_product(O)==337
GO,GE=cov(O),cov(E)
l=QQ(175)/337
assert GE.is_zero() and GO.transpose()*GO==l*l*identity_matrix(K,8)
p_target=expectation(O,ann[0].conjugate_transpose()*ann[0])
pmin=QQ(337)/625*(1-l)/2+QQ(288)/625/2
assert p_target==QQ(81)/337 and pmin==QQ(9)/25
bound=pmin-p_target
assert bound==QQ(1008)/8425
out={'scope':'EXACT_COVARIANCE_CONTROL; all-unitary bound is analytic',
 'odd_probability':'337/625','even_probability':'288/625',
 'odd_covariance_norm':str(l),'even_covariance_zero':True,
 'target_mode_a_probability':str(p_target),'architecture_mode_a_lower_bound':str(pmin),
 'TV_lower_bound':str(bound),'scope_excludes':['ancillas','additional measurements','postselection','arbitrary classical outcome relabeling'],
 'general_sampling_no_go':False,'classical_hardness':False,'quantum_speedup':False}
Path(__file__).with_name('result.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out))

from sage.all import QQ, matrix, identity_matrix, vector
from pathlib import Path
from itertools import combinations
from functools import reduce
import json, hashlib

root=Path.cwd()
source=root/'research/audits/controls/gaudin_local_agp/certificate.json'
raw=source.read_bytes(); cert=json.loads(raw)
eps=list(map(QQ,[0,1,3,7])); coupling=QQ(1)/3
I2=identity_matrix(QQ,2); X=matrix(QQ,[[0,1],[1,0]])
J=matrix(QQ,[[0,-1],[1,0]]) # Pauli Y = i J
Z=matrix(QQ,[[1,0],[0,-1]])
plus=matrix(QQ,[[0,1],[0,0]]); minus=plus.transpose()
def site(op,i):
    return reduce(lambda A,B:A.tensor_product(B),[op if j==i else I2 for j in range(4)])
xs=[site(X,i) for i in range(4)]; js=[site(J,i) for i in range(4)]
zs=[site(Z,i) for i in range(4)]
ps=[site(plus,i) for i in range(4)]; ms=[site(minus,i) for i in range(4)]
I=identity_matrix(QQ,16); zero=matrix(QQ,16,16)
n=[(I+zs[i])/2 for i in range(4)]
V=[]
for i in range(4):
    V.append(sum(((xs[i]*xs[j]-js[i]*js[j]+zs[i]*zs[j]-I)/(4*(eps[i]-eps[j])) for j in range(4) if j!=i),zero))
Q=[n[i]+coupling*V[i] for i in range(4)]
def comm(A,B):return A*B-B*A
assert all(comm(n[i],n[j])==zero and comm(n[i],V[j])+comm(V[i],n[j])==zero and comm(V[i],V[j])==zero for i in range(4) for j in range(4))
states=[format(j,'04b') for j in range(16) if format(j,'04b').count('1')==2]
indices=[int(s,2) for s in states]
assert states==cert['basis_bitstrings']
def sector(A):return A.matrix_from_rows_and_columns(indices,indices)
q=list(map(sector,Q)); v=list(map(sector,V)); z6=matrix(QQ,6,6)
def decode(A):return matrix(QQ,[[QQ(x) for x in row] for row in A])
assert q==list(map(decode,cert['charges_Q_i']))
assert v==list(map(decode,cert['derivatives_V_i']))
assert sum(q,z6)==2*identity_matrix(QQ,6) and sum(v,z6)==z6
K=decode(cert['full_antisymmetric_solution_K'])
assert K.transpose()==-K
assert all(comm(q[j],v[i]-comm(K,q[i]))==z6 for i in range(4) for j in range(4))
expected=QQ(355248848800449)/QQ(125250068977266446)
assert K[0,5]==expected and expected!=0
basis=[]; pairs=[]
for a,b in combinations(range(6),2):
    T=matrix(QQ,6,6);T[a,b]=1;T[b,a]=-1
    basis.append(T);pairs.append((a,b))
def column(T):return [x for i in range(4) for j in range(4) for x in comm(q[j],comm(T,q[i])).list()]
A=matrix(QQ,[column(T) for T in basis]).transpose()
rhs=vector(QQ,[x for i in range(4) for j in range(4) for x in comm(q[j],v[i]).list()])
assert A.nrows()==576 and A.ncols()==15
assert A.rank()==15 and A.augment(matrix(QQ,576,1,list(rhs))).rank()==15
rows=list(A.transpose().pivots()); minor=A.matrix_from_rows(rows)
assert len(rows)==15 and minor.det()!=0
allowed=[i for i,(a,b) in enumerate(pairs) if sum(x!=y for x,y in zip(states[a],states[b]))<=3]
Aallowed=A.matrix_from_columns(allowed)
assert len(allowed)==12 and Aallowed.rank()==12
assert Aallowed.augment(matrix(QQ,576,1,list(rhs))).rank()==13
currents=[]
for a,b in combinations(range(4),2):
    C=ps[a]*ms[b]-ms[a]*ps[b]
    currents.append(sector(C))
    for c in range(4):
        if c not in (a,b):currents.append(sector(zs[c]*C))
assert currents==list(map(decode,cert['ansatz_generators']))
Ac=matrix(QQ,[column(T) for T in currents]).transpose()
assert Ac.rank()==12 and Ac.augment(matrix(QQ,576,1,list(rhs))).rank()==13
w=vector(QQ,576)
for entry in cert['witness']['sparse_support']:
    row=entry['constraint_row'];w[row]=QQ(entry['weight'])
    assert list(Ac.row(row))==list(map(QQ,entry['A_row']))
    assert rhs[row]==QQ(entry['rhs_entry'])
assert Ac.transpose()*w==vector(QQ,18) and w.dot_product(rhs)==1
cp=q[0].charpoly(); gcddeg=cp.gcd(cp.derivative()).degree()
result={
 'scope':'Single stored N4 M2 instance; independent full-Pauli reconstruction, exact rational verification only',
 'certificate_sha256':hashlib.sha256(raw).hexdigest(),
 'native_input':{'N':4,'M':2,'sites':['0','1','3','7'],'g':'1/3'},
 'basis':states,
 'full_pauli_native_matrices_match_certificate':True,
 'charge_commutativity_polynomial_in_g_checked':True,
 'derivatives_match_certificate':True,
 'K_antisymmetric':True,
 'all_576_joint_transport_constraints_zero':True,
 'full_constraint_rank':15,'full_augmented_rank':15,
 'full_rank_minor_row_indices':[int(i) for i in rows],
 'full_rank_minor_determinant':str(minor.det()),
 'hamming_le3_subspace_dimension':12,'restricted_constraint_rank':12,'restricted_augmented_rank':13,
 'currents_match_certificate':True,'stored_13_term_inconsistency_witness_verified':True,
 'Q0_characteristic_polynomial':str(cp),'Q0_charpoly_derivative_gcd_degree':int(gcddeg),
 'forbidden_matrix_entry':{'bra':'0011','ket':'1100','value':str(K[0,5]),'hamming_distance':4},
 'no_eigensolver_no_parameter_sweep':True
}
(root/'research/audits/reviews/2026-11-13-gaudin-three-local/result.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))

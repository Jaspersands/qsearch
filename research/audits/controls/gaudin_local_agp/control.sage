# One exact rational N=4, M=2 locality falsifier and full antisymmetric control.
# No eigensolver, floating arithmetic, other sites/couplings or N=6 sweep.
from sage.all import QQ, matrix, vector, identity_matrix
from itertools import product, combinations
from pathlib import Path
import json

outdir = Path("research/audits/controls/gaudin_local_agp").resolve()
N = int(4); M = int(2); eps = [QQ(0),QQ(1),QQ(3),QQ(7)]; g = QQ(1)/3
states = [tuple(b) for b in product([int(0),int(1)], repeat=N) if sum(b)==M]
index = {b:k for k,b in enumerate(states)}; D = len(states)
I = identity_matrix(QQ,D); zero = matrix(QQ,D,D)
def comm(A,B): return A*B-B*A
def encode(A): return [[str(A[r,c]) for c in range(A.ncols())] for r in range(A.nrows())]
def nnz(A): return int(sum(a != 0 for a in A.list()))
def swap(a,b):
    P = matrix(QQ,D,D)
    for col,bs in enumerate(states):
        target = list(bs); target[a],target[b] = target[b],target[a]
        P[index[tuple(target)],col] = 1
    return P
def current(a,b):
    # sigma^+ = |0><1|, sigma^- = |1><0|, Z|bit>=(1-2bit)|bit>.
    # The first product maps (1,0) at (a,b) to (0,1) with +1.
    C = matrix(QQ,D,D)
    for col,bs in enumerate(states):
        if bs[a] != bs[b]:
            target = list(bs); target[a],target[b] = target[b],target[a]
            C[index[tuple(target)],col] = 1 if bs[a]==1 else -1
    assert C.transpose()==-C
    return C
charges=[]; derivatives=[]
for i in range(N):
    n_i = matrix(QQ,D,D,lambda r,c: 1-states[r][i] if r==c else 0)
    V_i = sum(((swap(i,j)-I)/(2*(eps[i]-eps[j])) for j in range(N) if j!=i),zero)
    Q_i = n_i+g*V_i
    assert Q_i.transpose()==Q_i and V_i.transpose()==V_i
    charges.append(Q_i); derivatives.append(V_i)
charge_commutators=[{"i":int(i),"j":int(j),"nonzero_entries":nnz(comm(charges[i],charges[j]))} for i in range(N) for j in range(N)]
assert all(r["nonzero_entries"]==0 for r in charge_commutators)
assert sum(charges,zero)==M*I and sum(derivatives,zero)==zero
ansatz=[]; labels=[]
for a,b in combinations(range(N),2):
    C=current(a,b); ansatz.append(C); labels.append("C_"+str(a)+str(b))
    for c in range(N):
        if c not in [a,b]:
            Zc=matrix(QQ,D,D,lambda r,k: 1-2*states[r][c] if r==k else 0)
            ZC=Zc*C
            assert ZC.transpose()==-ZC
            ansatz.append(ZC); labels.append("Z_"+str(c)+"*C_"+str(a)+str(b))
full=[]; full_labels=[]
for a,b in combinations(range(D),2):
    E=matrix(QQ,D,D); E[a,b]=1; E[b,a]=-1
    full.append(E); full_labels.append("E_"+str(a)+str(b))
# Each of the 16 pairs (i,j) contributes all 36 exact matrix-entry constraints.
row_labels=[(int(i),int(j),int(r),int(c)) for i in range(N) for j in range(N) for r in range(D) for c in range(D)]
rhs=vector(QQ,[x for i in range(N) for j in range(N) for x in comm(charges[j],derivatives[i]).list()])
def constraints(Kbasis):
    columns=[[x for i in range(N) for j in range(N) for x in comm(charges[j],comm(K,charges[i])).list()] for K in Kbasis]
    return matrix(QQ,columns).transpose()
A=constraints(ansatz); Afull=constraints(full)
rankA=int(A.rank()); rankAug=int(A.augment(matrix(QQ,len(rhs),1,list(rhs))).rank())
rankFull=int(Afull.rank()); rankFullAug=int(Afull.augment(matrix(QQ,len(rhs),1,list(rhs))).rank())
ansatz_span_rank=int(matrix(QQ,[K.list() for K in ansatz]).rank())
assert rankFull==rankFullAug
full_coeff=Afull.solve_right(rhs)
Kfull=sum((c*K for c,K in zip(full_coeff,full)),zero)
assert Kfull.transpose()==-Kfull
full_residuals=[{"i":int(i),"j":int(j),"nonzero_entries":nnz(comm(charges[j],derivatives[i]-comm(Kfull,charges[i])))} for i in range(N) for j in range(N)]
assert all(r["nonzero_entries"]==0 for r in full_residuals)
witness_data=None; ansatz_solution=None
if rankAug>rankA:
    # Solve A^T y=0 and rhs^T y=1 directly; no numerical nullspace.
    B=A.transpose().stack(matrix(QQ,1,len(rhs),list(rhs)))
    y=B.solve_right(vector(QQ,[0]*A.ncols()+[1]))
    assert A.transpose()*y==vector(QQ,A.ncols()) and y.dot_product(rhs)==1
    support=[]
    for row,value in enumerate(y):
        if value!=0:
            support.append({"constraint_row":int(row),"i_j_matrixrow_matrixcol":list(row_labels[row]),"weight":str(value),"A_row":[str(v) for v in A.row(row)],"rhs_entry":str(rhs[row])})
    witness_data={"type":"exact_left_null_inconsistency_witness","left_pairings_with_every_A_column":[str(v) for v in A.transpose()*y],"pairing_with_rhs":str(y.dot_product(rhs)),"sparse_support":support}
    outcome="THREE_SITE_ANSATZ_INCONSISTENT_AT_THIS_SINGLE_INSTANCE"
else:
    sol=A.solve_right(rhs); Kansatz=sum((c*K for c,K in zip(sol,ansatz)),zero)
    assert all(comm(charges[j],derivatives[i]-comm(Kansatz,charges[i]))==zero for i in range(N) for j in range(N))
    ansatz_solution={"coefficients":[str(v) for v in sol],"K":encode(Kansatz)}
    outcome="THREE_SITE_ANSATZ_PASSES_THIS_SINGLE_INSTANCE_ONLY"
certificate={
    "native_input":{"N":N,"M":M,"sites":[str(v) for v in eps],"g":str(g)},
    "basis_bitstrings":["".join(str(v) for v in bs) for bs in states],
    "convention":"n_i=(I+Z_i)/2; bit0 has Z=+1. Here Hamming weight2 and sum(n_i)=2 coincide. C_ab=sigma_a^+sigma_b^- - sigma_a^-sigma_b^+ with a<b.",
    "linear_system_convention":"A_column(K) stacks [Q_j,[K,Q_i]], rhs stacks [Q_j,V_i]; ordering (i,j,matrixrow,matrixcol), all 576 entries retained.",
    "charges_Q_i":[encode(Q) for Q in charges],"derivatives_V_i":[encode(V) for V in derivatives],
    "ansatz_labels":labels,"ansatz_generators":[encode(K) for K in ansatz],
    "ansatz_nominal_generators":len(ansatz),"ansatz_sector_span_rank":ansatz_span_rank,
    "rankA":rankA,"rankAug":rankAug,"witness":witness_data,"ansatz_solution":ansatz_solution,
    "full_antisymmetric_labels":full_labels,"full_antisymmetric_coefficients":[str(v) for v in full_coeff],"full_antisymmetric_solution_K":encode(Kfull),
    "full_rankA":rankFull,"full_rankAug":rankFullAug,"full_constraint_residuals":full_residuals,
    "exact_charge_commutators":charge_commutators,
}
(outdir/"certificate.json").write_text(json.dumps(certificate,indent=2,sort_keys=True)+"\n")
result={"status":"EXACT_CONTROL_COMPLETED","outcome":outcome,"native_input":certificate["native_input"],"sector_dimension":D,
    "constraints":int(A.nrows()),"ansatz":{"nominal_generators":len(ansatz),"sector_span_dimension":ansatz_span_rank,"rankA":rankA,"rankAug":rankAug,"consistent":rankA==rankAug,"inconsistency_witness_rhs_pairing":witness_data["pairing_with_rhs"] if witness_data else None,"witness_support_size":len(witness_data["sparse_support"]) if witness_data else 0},
    "full_antisymmetric_positive_control":{"generators":len(full),"rankA":rankFull,"rankAug":rankFullAug,"consistent":True,"exact_all_i_j_residuals_zero":True},
    "exact_charge_commutators":charge_commutators,"sum_Q_equals_M_identity":True,"sum_V_zero":True,
    "certificate":"certificate.json","cas":"/opt/anaconda3/envs/qsearch-cas/bin/sage",
    "scope":"One exact rational N4,M2 instance only; tests the stated at-most-three-site current span. No eigensolver, floating residual, N6 sweep, quantum implementation, larger-locality or general-impossibility inference."}
(outdir/"result.json").write_text(json.dumps(result,indent=2,sort_keys=True)+"\n")
print(json.dumps({"outcome":outcome,"sector_dimension":D,"ansatz":result["ansatz"],"full_antisymmetric_positive_control":result["full_antisymmetric_positive_control"],"exact_charge_commutators_all_zero":True},indent=2))

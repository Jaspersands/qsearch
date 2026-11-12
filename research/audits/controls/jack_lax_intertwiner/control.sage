# One D=3, lambda=(2,1), alpha=3 exact coefficient control.
# No other degree, statevector simulation, floating arithmetic, or theory promotion.
from sage.all import QQ, SymmetricFunctions, Partitions, matrix, vector, diagonal_matrix, identity_matrix, factorial
from collections import Counter
from pathlib import Path
import json

outdir = Path("research/audits/controls/jack_lax_intertwiner").resolve()
D = int(3); alpha = QQ(3); lam = (int(2),int(1))
Sym = SymmetricFunctions(QQ)
p = Sym.powersum()
J = Sym.jack(t=alpha).J()
def sorted_partition(parts): return tuple(sorted((int(k) for k in parts),reverse=True))
def weight(mu):
    z = QQ(1)
    for k,m in Counter(mu).items(): z *= QQ(k)**m*factorial(m)
    return z*alpha**len(mu)
def encoded_matrix(A): return [[str(A[r,c]) for c in range(A.ncols())] for r in range(A.nrows())]
def coefficients(sf): return {tuple(int(k) for k in mu):QQ(c) for mu,c in p(sf).monomial_coefficients().items()}
def as_rows(coef,basis): return [{"partition":list(mu),"coefficient":str(coef.get(mu,0))} for mu in basis]
source_parts=[tuple(int(k) for k in mu) for mu in Partitions(D)]
target_parts=[tuple(int(k) for k in mu) for mu in Partitions(D+1)]
basis=[(tuple(int(k) for k in mu),int(ell)) for ell in range(D+1) for mu in Partitions(D-ell)]
index={b:i for i,b in enumerate(basis)}; target_index={mu:i for i,mu in enumerate(target_parts)}
assert len(basis)==7 and len(target_parts)==5
L=matrix(QQ,len(basis),len(basis))
for col,(mu,ell) in enumerate(basis):
    L[col,col] += 2*ell
    for k,m in Counter(mu).items():
        parts=list(mu); parts.remove(k)
        L[index[(sorted_partition(parts),ell+k)],col] += 3*k*m
    for k in range(1,ell+1):
        L[index[(sorted_partition(list(mu)+[k]),ell-k)],col] += 1
A=matrix(QQ,len(target_parts),len(basis))
for col,(mu,ell) in enumerate(basis): A[target_index[sorted_partition(list(mu)+[ell+1])],col] = 1
Pi0=matrix(QQ,len(source_parts),len(basis))
for row,mu in enumerate(source_parts): Pi0[row,index[(mu,0)]]=1
Wsource=diagonal_matrix(QQ,[weight(mu) for mu,ell in basis])
Wtarget=diagonal_matrix(QQ,[weight(mu) for mu in target_parts])
assert Wsource*L==L.transpose()*Wsource
Adagger=Wsource.inverse()*A.transpose()*Wtarget
AAadj=A*Adagger
coisometry_ok=AAadj==3*(D+1)*identity_matrix(QQ,len(target_parts))
assert coisometry_ok
Jlambda=p(J[list(lam)])
Jcoef=coefficients(Jlambda)
Jvec=vector(QQ,[Jcoef.get(mu,0) for mu in source_parts])
expected_Jlambda= p[1,1,1]+2*p[2,1]-3*p[3]
assert Jlambda==expected_Jlambda
corners=[((int(2),int(0)),QQ(6),(int(3),int(1))),((int(1),int(1)),QQ(2),(int(2),int(2))),((int(0),int(2)),QQ(-2),(int(2),int(1),int(1)))]
rows=[]; failures=[]
for corner,content,nu in corners:
    assert alpha*corner[0]-corner[1]==content
    B=(L-content*identity_matrix(QQ,len(basis))).stack(Pi0)
    rhs=vector(QQ,[0]*len(basis)+list(Jvec))
    rankB=int(B.rank()); rankAug=int(B.augment(matrix(QQ,len(rhs),1,list(rhs))).rank())
    assert rankB==rankAug==len(basis), (corner,"Eigenvector plus pi0 constraints not uniquely solvable",rankB,rankAug)
    psi=B.solve_right(rhs)
    assert L*psi==content*psi and Pi0*psi==Jvec
    image=A*psi
    target_sf=p(J[list(nu)]); target_coef=coefficients(target_sf)
    target_vec=vector(QQ,[target_coef.get(mu,0) for mu in target_parts])
    pivot=next(i for i,c in enumerate(target_vec) if c!=0)
    scalar=image[pivot]/target_vec[pivot]
    diff=image-scalar*target_vec
    equal=scalar!=0 and diff==vector(QQ,len(target_parts))
    if not equal: failures.append({"corner":list(corner),"content":str(content),"target_partition":list(nu),"reason":"A psi is not a nonzero scalar multiple of the target integral Jack"})
    rows.append({"corner":list(corner),"content":str(content),"target_partition":list(nu),"constraint_rank":rankB,"augmented_constraint_rank":rankAug,"unique_solution":True,
        "psi_coefficients":[{"partition":list(mu),"w_power":ell,"coefficient":str(c)} for (mu,ell),c in zip(basis,psi)],
        "L_psi_minus_content_psi_zero":True,"pi0_psi_equals_integral_Jlambda":True,
        "A_psi_power_sum_coefficients":[{"partition":list(mu),"coefficient":str(c)} for mu,c in zip(target_parts,image)],
        "target_integral_J_power_sum_coefficients":as_rows(target_coef,target_parts),
        "scalar_multiple":str(scalar),"nonzero_scalar":scalar!=0,"all_exact_coefficients_match":equal,
        "difference_coefficients":[{"partition":list(mu),"coefficient":str(c)} for mu,c in zip(target_parts,diff)]})
result={"status":"PASS" if not failures else "FAIL","scope":"One exact alpha3,D3,lambda(2,1) control at its three specified addable corners only. Finite nonfalsification is not an all-degree intertwining theorem or efficient quantum transform.",
    "cas":"/opt/anaconda3/envs/qsearch-cas/bin/sage","D":D,"alpha":str(alpha),"lambda":list(lam),"domain_dimension":len(basis),"target_dimension":len(target_parts),
    "native_operator":"L=2w*d_w + sum(3k*d_Vk*w^k) + sum(Vk*pi(w^-k)); A(V_mu*w^ell)=V_mu*V_(ell+1)",
    "source_convention":"Mickler-Moll Definition1.1 and Theorem1.4, epsilon1=3, epsilon2=-1, epsilon=2, hbar=3; V_k=p_k and j_lambda=integral J_lambda.",
    "fock_convention":"p_mu orthogonal with weight z_mu*3^length(mu); w powers mutually orthogonal of norm1. Domain product inner product.",
    "source_integral_Jlambda_power_sum_coefficients":as_rows(Jcoef,source_parts),"domain_basis":[{"partition":list(mu),"w_power":ell} for mu,ell in basis],"target_power_sum_basis":[list(mu) for mu in target_parts],
    "L_matrix":encoded_matrix(L),"A_matrix":encoded_matrix(A),"A_adjoint_matrix":encoded_matrix(Adagger),"domain_fock_weights":[str(weight(mu)) for mu,ell in basis],"target_fock_weights":[str(weight(mu)) for mu in target_parts],
    "L_self_adjoint_in_fock_metric":True,"A_Aadjoint_matrix":encoded_matrix(AAadj),"A_Aadjoint_equals_3Dplus1_identity":coisometry_ok,"coisometry_scalar":str(3*(D+1)),"normalized_coisometry":"A/sqrt(12), with (A/sqrt(12))*(A/sqrt(12))^dagger=I on degree4, at this fixed test only.","corners":rows,"failures":failures}
(outdir/"result.json").write_text(json.dumps(result,indent=2,sort_keys=True)+"\n")
print(json.dumps({"status":result["status"],"domain_dimension":len(basis),"A_Aadjoint_scalar":result["coisometry_scalar"],"A_Aadjoint_exact_identity":coisometry_ok,"corner_results":[{"corner":r["corner"],"content":r["content"],"target":r["target_partition"],"scalar":r["scalar_multiple"],"exact_match":r["all_exact_coefficients_match"]} for r in rows],"failures":failures},indent=2))
if failures: raise SystemExit(1)

# One fixed global-D3 normalization/interference control on its seven diagrams.
from sage.all import QQ, PolynomialRing, SymmetricFunctions, Partitions, Partition, matrix, vector, diagonal_matrix, identity_matrix, factorial
from collections import Counter
from pathlib import Path
import json

REPO=Path("/Users/jaspersands/Developer/qsearch")
out=REPO/"research/audits/controls/macdonald_newton_degree3/result.json"
D=int(3);t=QQ(3)/4;q=t**3
# Known Sage rational-specialization conversion issue: convert generically first.
polys=PolynomialRing(QQ,names=("q","t"));rational_functions=polys.fraction_field()
qsym,tsym=rational_functions.gens();evaluate_polynomial=polys.hom([q,t],QQ)
def specialize(c):
    f=rational_functions(c)
    denominator=evaluate_polynomial(f.denominator())
    assert denominator!=0,"Generic rational coefficient has zero specialized denominator"
    return QQ(evaluate_polynomial(f.numerator())/denominator)
Sym=SymmetricFunctions(rational_functions);power=Sym.powersum();Mac=Sym.macdonald(q=qsym,t=tsym);P=Mac.P();Q=Mac.Q()
basis=[tuple(int(a) for a in lam) for d in range(D+1) for lam in Partitions(d)]
index={lam:i for i,lam in enumerate(basis)};size=len(basis)
assertions=[]
def check(cond,label):
    assert cond,label
    assertions.append(label)
def pcoeff(f):return {tuple(int(a) for a in mu):specialize(c) for mu,c in power(f).monomial_coefficients().items()}
def rratio(r):return (1-q**r)/(1-t**r)
def hall_weight(mu):
    z=QQ(1)
    for r,m in Counter(mu).items():z*=QQ(r)**m*factorial(m)*rratio(r)**m
    return z
def inner_from_power(c,d):return sum((a*d.get(mu,0)*hall_weight(mu) for mu,a in c.items()),QQ(0))
def encode(A):return [[str(A[i,j]) for j in range(A.ncols())] for i in range(A.nrows())]
check(q==QQ(27)/64,"global_q_t_cubed_fixed")
check(size==7,"seven_diagrams_degree_at_most_three")
r={k:rratio(k) for k in range(1,D+1)}
for k in r:check(r[k]==1+t**k+t**(2*k),"r_ratio_identity_"+str(k))
expansions={lam:pcoeff(P[Partition(lam)]) for lam in basis}
h={lam:inner_from_power(expansions[lam],expansions[lam]) for lam in basis}
for lam in basis:check(h[lam]>0,"positive_exact_Hall_norm_"+str(lam))
for a,lam in enumerate(basis):
    for nu in basis[:a]:
        if sum(lam)==sum(nu):check(inner_from_power(expansions[lam],expansions[nu])==0,"monic_P_orthogonality_"+str((lam,nu)))
H=diagonal_matrix(QQ,[h[lam] for lam in basis]);I=identity_matrix(QQ,size)
g={k:Q[[k]] for k in range(1,D+1)}
G={0:I};T={0:I};newton={};direct={}
for k in range(1,D+1):
    check(pcoeff(g[k])=={mu:c/h[(k,)] for mu,c in expansions[(k,)].items()},"Q_row_exact_duality_"+str(k))
    Gn=matrix(QQ,size,size)
    for col,lam in enumerate(basis):
        if sum(lam)+k<=D:
            product=P(g[k]*P[Partition(lam)])
            for nu,c in product.monomial_coefficients().items():Gn[index[tuple(int(a) for a in nu)],col]=specialize(c)
    G[k]=Gn;T[k]=H.inverse()*Gn.transpose()*H
    check(H*T[k]==Gn.transpose()*H,"metric_adjoint_"+str(k))
for k in range(1,D+1):
    newton[k]=k*r[k]*T[k]-r[k]*sum((newton[i]*T[k-i]/r[i] for i in range(1,k)),matrix(QQ,size,size))
    direct[k]=matrix(QQ,size,size)
    for col,lam in enumerate(basis):
        deriv=power.zero()
        for rho,c in expansions[lam].items():
            multiplicity=rho.count(k)
            if multiplicity:
                smaller=list(rho);smaller.remove(k)
                deriv+=c*k*r[k]*multiplicity*power[Partition(smaller)]
        for nu,c in P(deriv).monomial_coefficients().items():direct[k][index[tuple(int(a) for a in nu)],col]=specialize(c)
    for a in range(size):
        for b in range(size):check(newton[k][a,b]==direct[k][a,b],"Newton_direct_entry_"+str((k,a,b)))
f_re=vector(QQ,size);f_im=vector(QQ,size)
f_re[index[(3,)]]=1;f_re[index[(1,1,1)]]=-1;f_im[index[(2,1)]]=1
def norm2(v):return v.dot_product(H*v)
f_norm=norm2(f_re)+norm2(f_im)
check(f_norm>0,"coherent_f_positive_norm")
mode_rows=[];lhs=QQ(0)
for k in range(1,D+1):
    re=newton[k]*f_re;im=newton[k]*f_im;value=norm2(re)+norm2(im);lhs+=value/r[k]
    incoherent=QQ(0)
    for lam in [(3,),(2,1),(1,1,1)]:
        e=vector(QQ,size);e[index[lam]]=1;incoherent+=norm2(newton[k]*e)
    mode_rows.append({"r":int(k),"r_ratio":str(r[k]),"D_r_f_norm_squared":str(value),"Euler_contribution":str(value/r[k]),"deletion_probability":str(value/(r[k]*D*f_norm)),"real_output_coefficients":[str(v) for v in re],"imag_output_coefficients":[str(v) for v in im],"incoherent_sum_norm_squared":str(incoherent),"coherent_interference_difference":str(value-incoherent)})
check(lhs==D*f_norm,"Euler_identity_for_specified_complex_f")
result={"status":"PASS","scope":"Exactly globalD3,t3/4,q27/64 and its seven diagrams. Exact normalization/interference falsifier only; no all-degree support or sampler/theorem inference, no parameter/shape sweep.","cas":"/opt/anaconda3/envs/qsearch-cas/bin/sage","initial_api_blocker":{"type":"TypeError","message":"sage.rings.rational.Rational object is not callable","location":"sage/combinat/sf/macdonald.py:1175, lambda c: c(t,q)","stage":"Direct rational-specialized monic Macdonald P to power-sum conversion"},"repair":"One bounded generic Macdonald P/Q conversion over Frac(QQ[q,t]); evaluate each rational coefficient by polynomial numerator/denominator homomorphism q=27/64,t=3/4 before matrix arithmetic.","constants":{"D":D,"t":str(t),"q":str(q),"r_ratios":{str(k):str(v) for k,v in r.items()}},"basis":[list(lam) for lam in basis],"monic_P_power_sum_expansions":[{"partition":list(lam),"coefficients":[{"rho":list(mu),"coefficient":str(c)} for mu,c in sorted(expansions[lam].items(),reverse=True)]} for lam in basis],"Hall_norms":[{"partition":list(lam),"h":str(h[lam])} for lam in basis],"G_multiplication_matrices":{str(k):encode(G[k]) for k in range(1,D+1)},"T_metric_adjoint_matrices":{str(k):encode(T[k]) for k in range(1,D+1)},"Newton_D_matrices":{str(k):encode(newton[k]) for k in range(1,D+1)},"direct_p_dagger_matrices":{str(k):encode(direct[k]) for k in range(1,D+1)},"exact_Newton_entry_comparisons":int(D*size*size),"all_retained_Newton_entries_match":True,"coherent_f":"P_(3)+i*P_(2,1)-P_(1,1,1)","coherent_f_norm_squared":str(f_norm),"mode_results":mode_rows,"Euler_lhs":str(lhs),"Euler_rhs":str(D*f_norm),"Euler_exact":lhs==D*f_norm,"assertions_passed":len(assertions),"assertion_labels":assertions}
out.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n")
print(json.dumps({"status":result["status"],"constants":result["constants"],"diagrams":size,"exact_Newton_entry_comparisons":result["exact_Newton_entry_comparisons"],"assertions_passed":len(assertions),"coherent_f_norm_squared":str(f_norm),"Euler_lhs":str(lhs),"Euler_rhs":str(D*f_norm),"mode_results":[{k:v for k,v in row.items() if k not in ["real_output_coefficients","imag_output_coefficients"]} for row in mode_rows]},indent=2))

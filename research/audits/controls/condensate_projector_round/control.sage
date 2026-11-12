# One fixed D3 exact rational phase/projection control, no sweep.
from sage.all import QQ, PolynomialRing, binomial
from pathlib import Path
import json
REPO=Path("/Users/jaspersands/Developer/qsearch")
out=REPO/"research/audits/controls/condensate_projector_round/result.json"
D=int(3);t=QQ(3)/4;q=t**3;tau=QQ(157464)/37
shapes={"R":(3,),"M":(2,1),"C":(1,1,1)}
E={name:sum(((q**(-part)-1)*t**i for i,part in enumerate(lam)),QQ(0)) for name,lam in shapes.items()}
a=tau*(E["R"]-E["M"]);b=tau*(E["M"]-E["C"])
checks={"global_q_27_over_64":q==QQ(27)/64,"first_phase_identity":a==28394,"second_phase_identity":b==QQ(21087)/2,"first_relative_phase_integer":a.denominator()==1,"second_relative_phase_half_integer_odd":(2*b).denominator()==1 and int(2*b)%2==1}
C=[QQ(1),QQ(1),QQ(-1),QQ(-1)]
X=[QQ(binomial(D,m))*sum((QQ(-1)**r*binomial(D-m,r)*C[m+r] for r in range(D-m+1)),QQ(0)) for m in range(D+1)]
expected=[QQ(-4),QQ(6),QQ(0),QQ(-1)]
for m in range(D+1):checks["projected_coefficient_"+str(m)]=X[m]==expected[m]
Rz=PolynomialRing(QQ,"z");z=Rz.gen()
G=sum((binomial(D,j)*C[j]*(z-1)**j for j in range(D+1)),Rz(0))
checks["generating_polynomial_identity"]=G==-4+6*z-z**3
checks["projected_entries_sum_one"]=sum(X)==1
checks["negative_zero_count_entry"]=X[0]<0
checks["negative_three_count_entry"]=X[3]<0
assert all(checks.values()),checks
result={"status":"PASS","scope":"One exact globalD3 rational phase and samplewise binomial-projection control only. It verifies the stated signed vector, not the full probabilistic coupling, a Gaussian approximation theorem, variance lower bound or general classical impossibility.","cas":"/opt/anaconda3/envs/qsearch-cas/bin/sage","D":D,"t":str(t),"q":str(q),"tau":str(tau),"eigenvalue_formula":"E_lambda=sum_i(q^(-lambda_i)-1)*t^(i-1), with i starting1","eigenvalues":{name:str(v) for name,v in E.items()},"tau_E3_minus_E21":str(a),"tau_E21_minus_E111":str(b),"relative_phase_signs":{"R_vs_M":int(1),"M_vs_C":int(-1)},"input_moment_vector":[int(c) for c in C],"projection_formula":"X_m=binomial(3,m)*sum_r(-1)^r*binomial(3-m,r)*C_(m+r)","projected_vector":[int(v) for v in X],"projected_generating_polynomial":str(G),"assertions_passed":int(len(checks)),"assertions":checks}
out.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n")
print(json.dumps({"status":result["status"],"eigenvalues":result["eigenvalues"],"tau_E3_minus_E21":str(a),"tau_E21_minus_E111":str(b),"projected_vector":result["projected_vector"],"generating_polynomial":str(G),"assertions_passed":int(len(checks))},indent=2))

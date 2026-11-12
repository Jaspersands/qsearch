# Exactly the two prescribed degree-six shapes; no sweep or floating arithmetic.
from sage.all import QQ, SymmetricFunctions, Partition, factorial
from collections import Counter
from pathlib import Path
import json

REPO = Path("/Users/jaspersands/Developer/qsearch")
out = REPO / "research/audits/controls/jack_work_energy_collision/result.json"
alpha = QQ(3)
Sym = SymmetricFunctions(QQ)
p = Sym.powersum()
J = Sym.jack(t=alpha).J()
rows = []
for shape in [(3,3),(4,1,1)]:
    lam = Partition(shape)
    A = sum(k*k for k in lam)
    B = sum(k*k for k in lam.conjugate())
    assert sum(lam)==6 and A==18 and B==12
    coeffs = p(J[lam]).monomial_coefficients()
    norm = QQ(0); moment1 = QQ(0); moment2 = QQ(0); terms=[]
    for rho,c in sorted(coeffs.items(),key=lambda item:tuple(item[0]),reverse=True):
        z = QQ(1)
        for k,m in Counter(rho).items():z *= QQ(k)**m*factorial(m)
        weight = z*alpha**len(rho)
        n2 = sum(k*k for k in rho)
        mass = c*c*weight
        norm += mass; moment1 += mass*n2; moment2 += mass*n2*n2
        terms.append({"rho":[int(k) for k in rho],"Jack_power_sum_coefficient":str(c),"Hall_weight":str(weight),"N2_eigenvalue":int(n2),"unnormalized_mass":str(mass)})
    assert norm>0
    meanN2 = moment1/norm
    secondN2 = moment2/norm
    meanK = 42-2*meanN2
    secondS = (QQ(42)**2-168*meanN2+4*secondN2)/3
    rows.append({"lambda":[int(k) for k in lam],"D":int(sum(lam)),"A":int(A),"B":int(B),"alpha":"3","Jack_norm_squared":str(norm),"normalized_mean_N2":str(meanN2),"normalized_second_moment_N2":str(secondN2),"mean_K":str(meanK),"mean_S":"3*sqrt(3)" if meanK==9 else str(meanK)+"/sqrt(3)","mean_S_equals_3sqrt3":meanK==9,"normalized_second_moment_S":str(secondS),"variance_S_if_mean_3sqrt3":str(secondS-27) if meanK==9 else None,"power_sum_terms":terms})
second_difference = QQ(rows[0]["normalized_second_moment_S"])-QQ(rows[1]["normalized_second_moment_S"])
result={"status":"EXACT_MOMENT_CONTROL_COMPLETED","scope":"Only lambda=(3,3) and mu=(4,1,1) at alpha3. Different second moments refute only dependence of the final S-energy law on (A,B); no hardness claim. Equal second moments alone would not establish equality of full laws.","cas":"/opt/anaconda3/envs/qsearch-cas/bin/sage","conventions":{"state":"Sage integral Jack J at alpha3 in the power-sum basis","inner_product":"<p_rho,p_rho>=z_rho*3^length(rho)","N2":"N2*p_rho=(sum of squared parts of rho)*p_rho","energy_identity":"K=sqrt(3)*S; (K+2*N2)*J=42*J","second_S_formula":"(42^2-168*<N2>+4*<N2^2>)/3"},"cases":rows,"comparison":{"same_A_B":True,"mean_S_both_3sqrt3":all(r["mean_S_equals_3sqrt3"] for r in rows),"second_moments_S_equal":second_difference==0,"second_moment_S_lambda_minus_mu":str(second_difference),"outcome":"A_B_ONLY_DISTRIBUTION_SHORTCUT_REFUTED_BY_THIS_PAIR" if second_difference!=0 else "SECOND_MOMENTS_COINCIDE_ONLY_NO_FULL_LAW_INFERENCE"}}
out.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n")
print(json.dumps({"cases":[{k:r[k] for k in ["lambda","A","B","Jack_norm_squared","normalized_mean_N2","normalized_second_moment_N2","mean_S","normalized_second_moment_S"]} for r in rows],"comparison":result["comparison"]},indent=2))

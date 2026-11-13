from pathlib import Path
import itertools,json
import sympy as s
q,d,z=s.symbols("q delta zeta", positive=True)
split_cov=s.factor(-z*(1-z)*d**2/(q*(1-q)))
E=(8,9,10,11); A=(0,1,2,3); B=(4,5,6,7); C=(0,1,4,5); D=(2,3,6,7)
q0=s.Rational(1,4); eps=s.Rational(1,8); v=q0*(1-q0)
f=lambda signs,edge:s.prod(signs[i] for i in edge)/s.Integer(8)
values=[]
for signs in itertools.product((-1,1),repeat=12):
 vals=[f(signs,edge) for edge in (E,A,B,C,D)]
 fe,fa,fb,fc,fd=vals
 values.append(eps**4*fa*fb*fc*fd*(v+eps*fe*(1-2*q0)-eps**2*fe**2)/v**3)
observed=s.factor(sum(values)/len(values))
beta2=eps**2/v
expected=s.factor(beta2**2/s.Integer(8)**4*(1-beta2/s.Integer(64)))
assert observed==expected and observed>0
r=q+d/2
actual={(0,0):(1-q)*(1-q-d),(1,1):q*(q+d),(0,1):q*(1-q)+d*(1-2*q)/2,(1,0):q*(1-q)+d*(1-2*q)/2}
ideal={(a,b):(r if a else 1-r)*(r if b else 1-r) for a,b in actual}
chi=s.factor(sum((actual[k]-ideal[k])**2/ideal[k] for k in actual))
assert s.simplify(chi-d**4/(16*r**2*(1-r)**2))==0
out={"scope":"Exact finite and symbolic falsifiers only; no asymptotic algorithm conclusion", "masked_covariance":str(split_cov),"native_p":4,"native_k":2,"lambda":3,"shared":list(E),"row_unique":[list(A),list(B)],"column_unique":[list(C),list(D)],"q":str(q0),"epsilon":str(eps),"labels_enumerated":len(values),"lemma58_claimed_average":0,"actual_average_covariance":str(observed),"positive_formula":"beta^4/8^4*(1-beta^2/64)","approx_clone_chi_squared":str(chi)}
Path(__file__).with_suffix(".json").write_text(json.dumps(out,indent=2)+"\n")
print("EXACT_CONTROLS_PASS",observed,"clone_chi2",chi)

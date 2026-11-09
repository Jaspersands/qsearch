from sage.all import *
from pathlib import Path
import json,time
started=time.monotonic();logpath=Path(__file__).with_name('qsearch_cubic_circular_p313_bridge.log');logfile=logpath.open('w')
def log(stage,**kw):
 obj={'stage':stage,'elapsed_seconds':float(round(time.monotonic()-started,3)),**kw};s=json.dumps(obj,sort_keys=True);print(s,flush=True);logfile.write(s+'\n');logfile.flush()
d=json.loads(Path(__file__).with_name('qsearch_cubic_circular_p313.json').read_text());p=d['p'];g=d['g'];ell=(p-1)//3;r=pow(g,ell,p)
R=PolynomialRing(QQ,'x');K=NumberField(R(d['field_polynomial']),names='t');t=K.gen();sig=K.hom([K(d['sigma_t'])],K)
alpha=K(d['alpha']);c=K(d['c']);delta=c*c;assert sig(alpha)/alpha==delta
P=K.ideal(p,t-104);assert P.norm()==p and P.ramification_index()==3
S=PolynomialRing(K,'v');v=S.gen();F=K.extension(v*v+v+1,names='rho');rho=F.gen()
eta0=F(t);eta1=F(sig(t));eta2=F(sig(sig(t)))
tau=eta0+rho*eta1+rho*rho*eta2;taubar=eta0+rho*rho*eta1+rho*eta2
assert tau*taubar==p
A=F.absolute_field(names='w');toF,fromF=A.structure();assert toF.domain()==A and fromF.domain()==F
rhoa=fromF(rho);alphaa=fromF(F(alpha));taua=fromF(tau);taubara=fromF(taubar)
primes=A.primes_above(p);assert len(primes)==2
prime_report=[]
for q in primes:
 va=int((rhoa-r).valuation(q));vb=int((rhoa-pow(r,-1,p)).valuation(q))
 prime_report.append({'ideal':str(q),'norm':int(q.norm()),'ramification_index':int(q.ramification_index()),'rho_minus_r_valuation':va,'rho_minus_r_inverse_valuation':vb,'alpha_valuation':int(alphaa.valuation(q)),'tau_valuation':int(taua.valuation(q)),'taubar_valuation':int(taubara.valuation(q))})
log('degree_six_values',local_r=r,local_r_inverse=pow(r,-1,p),absolute_polynomial=str(A.defining_polynomial()),prime_data=prime_report)
# Local reduction from the common first-order uniformizer pi=t-104.
# Integral coefficients in Q(rho), with coefficient ramification index3:
# reducing rho to r changes coefficients by multiples of the local prime,
# hence contributes valuation at least3, irrelevant to the linear terms.
k=GF(p);u=k(104);pr=PolynomialRing(k,'s');s=pr.gen()
coeffpoly=lambda a:pr([k(q) for q in K(a).list()])
eta_polys=[coeffpoly(t),coeffpoly(sig(t)),coeffpoly(sig(sig(t)))]
a_poly=coeffpoly(alpha)
def tau_poly(rv,conjugated):
 rv=k(rv)
 return eta_polys[0]+(rv*rv if conjugated else rv)*eta_polys[1]+(rv if conjugated else rv*rv)*eta_polys[2]
local=[]
for rv in (r,pow(r,-1,p)):
 for conj in (False,True):
  tp=tau_poly(rv,conj);assert a_poly(u)==0 and tp(u)==0
  anum=a_poly.derivative()(u);den=tp.derivative()(u)
  entry={'rho_residue':rv,'denominator':'taubar' if conj else 'tau','alpha_linear_coefficient':int(anum),'denominator_linear_coefficient':int(den)}
  if den:
   entry['unit_residue']=int(anum/den)
  else:
   assert tp.derivative(2)(u)!=0
   entry['ratio_valuation']=-1
  local.append(entry)
fac=int(k(factorial(ell)));good=[q for q in local if q['rho_residue']==r and q['denominator']=='taubar'][0]
assert good['unit_residue']==fac
log('local_factorial_congruence',factorial_index=ell,factorial_residue=fac,local_expansions=local,uniformizer_norm_valuation=int((t-104).valuation(P)))
# Hilbert90 using a PARI principal-ideal generator; alpha is validation only.
bnf=K.pari_bnf(proof=True);assert int(bnf.bnfcertify())==1
princip=bnf.bnfisprincipal(P.pari_hnf(),1);classcoords=[int(a) for a in princip[0]];assert all(a==0 for a in classcoords)
beta=K(K.pari_nf().nfbasistoalg(princip[1]));assert K.ideal(beta)==P
if beta.norm()<0:beta=-beta
assert beta.norm()==p
U=K.unit_group(proof=True);units=list(U.gens_values());free=[i for i,z in enumerate(U.invariants()) if z==0]
UL=lambda a:vector(ZZ,[int(z) for z in U.log(a)])
T=matrix(ZZ,[[UL(sig(units[i]))[j] for j in free] for i in free]).transpose()
correction=delta/(sig(beta)/beta);coords=UL(correction);target=vector(ZZ,[coords[i] for i in free]);sol=(T-identity_matrix(ZZ,2)).solve_right(target)
assert all(v in ZZ for v in sol);sol=vector(ZZ,sol)
epsilon=prod((units[i]**sol[j] for j,i in enumerate(free)),K.one());recovered=beta*epsilon
assert sig(recovered)/recovered==delta
if recovered.norm()<0:recovered=-recovered
assert recovered.norm()==p and recovered==alpha
report={'p':p,'g':g,'character_convention':'chi(g)=rho; sigma(zeta)=zeta^g','local_r_g_pow_104':r,'local_r_inverse':pow(r,-1,p),'factorial_104_mod_p':fac,'prime_data':prime_report,'local_expansions':local,'beta':str(beta),'beta_norm':int(beta.norm()),'beta_principal_class_coordinates':classcoords,'delta':str(delta),'hilbert90_correction':str(correction),'hilbert90_correction_unit_coordinates':list(map(int,coords)),'hilbert90_free_solution':list(map(int,sol)),'epsilon':str(epsilon),'recovered_alpha':str(recovered),'recovered_equals_cyclotomic_truth':recovered==alpha,'source_control_only':True,'scope':'same single p313 exact classical control; alpha used as validation truth, not substituted for candidate algorithm; full quantum arithmetic not executed'}
Path(__file__).with_name('qsearch_cubic_circular_p313_bridge.json').write_text(json.dumps(report,indent=2,sort_keys=True)+'\n');log('complete',**report);logfile.close()

from sage.all import *
from pathlib import Path
import json,time
start=time.monotonic();out=Path(__file__).with_suffix('.log').open('w')
def log(stage,**kw):
 z={'stage':stage,'elapsed_seconds':float(round(time.monotonic()-start,3)),**kw};s=json.dumps(z,sort_keys=True);print(s,flush=True);out.write(s+'\n');out.flush()
ell=5;p=11;k=(p-1)//ell;g=int(primitive_root(p));r=pow(g,k,p)
Z=CyclotomicField(p,names='z');z=Z.gen();H=sorted({pow(g,ell*i,p) for i in range(k)})
theta=sum((z**i for i in H),Z.zero());Q=PolynomialRing(QQ,'x');K=NumberField(theta.minpoly(),names='t');t=K.gen();emb=K.hom([theta],Z)
# Here g=2, so the public conjugate is t^2-2; verify against cyclotomic truth.
sig=K.hom([t*t-2],K);assert g==2 and emb(sig(t))==sum((z**((g*i)%p) for i in H),Z.zero())
assert sig(sig(sig(sig(sig(t)))))==t
alpha=K(2)-t;assert emb(alpha)==prod((1-z**i for i in H),Z.one()) and alpha.norm()==p
delta=sig(alpha)/alpha;c=delta.sqrt();assert c*c==delta
RR=CyclotomicField(ell,names='rhoR');rhoR=RR.gen();lam=rhoR-1
eta2=rhoR**int(Zmod(ell)((1-2)/ZZ(2)))*(1+rhoR)
assert eta2.conjugate()==eta2 and eta2.is_unit()
w=eta2**(ell-1);assert w!=1 and w.conjugate()==w and w.is_unit()
b=(w-1)/lam;a=(w-1)/(lam*lam)
assert w.denominator()==1 and b.denominator()==1 and a.denominator()==1

def act(v,h):
 coeff=h.list();ans=K.one();cur=v
 for a0 in coeff:
  assert a0 in ZZ
  ans*=cur**ZZ(a0);cur=sig(cur)
 return ans
c2=act(c,w);delta2=c2*c2;epsilon=act(delta,b);alpha2=alpha*epsilon
assert delta2==act(delta,w) and sig(alpha2)/alpha2==delta2
assert epsilon.norm()==1 and alpha2.norm()==p and alpha2!=alpha
badc=act(c,eta2);baddelta=badc*badc;badcorrection=baddelta/delta
P=K.ideal(p,t-2);assert P.norm()==p and P.ramification_index()==ell and (t-2).valuation(P)==1
S=PolynomialRing(K,'v');v=S.gen();F=K.extension(sum(v**i for i in range(ell)),names='rho');rho=F.gen()
periods=[];cur=t
for i in range(ell):periods.append(cur);cur=sig(cur)
tau=sum((rho**i*F(periods[i]) for i in range(ell)),F.zero());taubar=sum((rho**(-i)*F(periods[i]) for i in range(ell)),F.zero())
assert tau*taubar==p
A=F.absolute_field(names='a');toF,fromF=A.structure();rhoA=fromF(rho);alphaA=fromF(F(alpha));alpha2A=fromF(F(alpha2));tauA=fromF(tau);taubarA=fromF(taubar)
prime_rows=[]
for q in A.primes_above(p):
 roots=[a0 for a0 in range(p) if (rhoA-a0).valuation(q)>0];assert len(roots)==1
 prime_rows.append({'rho_residue':roots[0],'norm':int(q.norm()),'ramification_index':int(q.ramification_index()),'alpha_valuation':int(alphaA.valuation(q)),'alpha2_valuation':int(alpha2A.valuation(q)),'tau_valuation':int(tauA.valuation(q)),'taubar_valuation':int(taubarA.valuation(q))})
selected=[row for row in prime_rows if row['rho_residue']==r][0];assert selected['alpha2_valuation']==selected['taubar_valuation']==1
# Exact local reduction by the uniformizer pi=t-2. Coefficient p-multiples
# have valuation at least ell=5, above the first-order terms used here.
fp=GF(p);Pp=PolynomialRing(fp,'s');s=Pp.gen();poly=lambda q:Pp([fp(x) for x in K(q).list()])
tbp=sum((fp(r)**(-i)*poly(periods[i]) for i in range(ell)),Pp.zero())
assert tbp(fp(2))==0
linear_den=tbp.derivative()(fp(2));assert linear_den!=0
linear_alpha=poly(alpha).derivative()(fp(2));linear_alpha2=poly(alpha2).derivative()(fp(2))
res1=int(linear_alpha/linear_den);res2=int(linear_alpha2/linear_den);fac=int(fp(factorial(k)))
assert res1==res2==fac
assert poly(delta)(fp(2))==fp(r) and poly(delta2)(fp(2))==fp(r)
assert poly(baddelta)(fp(2))==fp(r)**2 and poly(baddelta)(fp(2))!=fp(r)
# The bad multiplier must fail the exact integer Hilbert90 equation.
bnf=K.pari_bnf(proof=True);cert=int(bnf.bnfcertify());assert cert==1
U=K.unit_group(proof=True);units=list(U.gens_values());free=[i for i,a0 in enumerate(U.invariants()) if a0==0]
coords=lambda v:vector(ZZ,[int(x) for x in U.log(v)])
T=matrix(ZZ,[[coords(sig(units[i]))[j] for j in free] for i in free]).transpose()
M=T-identity_matrix(ZZ,ell-1);badcoords=coords(badcorrection);badsol=M.solve_right(vector(ZZ,[badcoords[i] for i in free]))
assert abs(M.det())==ell and any(x not in ZZ for x in badsol)
goodcorrection=delta2/delta;goodcoords=coords(goodcorrection);goodsol=M.solve_right(vector(ZZ,[goodcoords[i] for i in free]));assert all(x in ZZ for x in goodsol)
report={'ell':ell,'p':p,'k':k,'g':g,'local_r':r,'K_polynomial':str(K.defining_polynomial()),'K_discriminant':int(K.discriminant()),'F_degree':int(A.degree()),'sigma_t':str(sig(t)),'canonical_alpha':str(alpha),'canonical_c':str(c),'eta2':str(eta2),'w_eta2_pow_ell_minus_1':str(w),'w_minus_1_over_lambda':str(b),'w_minus_1_over_lambda_squared':str(a),'c2':str(c2),'alpha2':str(alpha2),'alpha2_differs_from_alpha':alpha2!=alpha,'alpha2_norm':int(alpha2.norm()),'alpha2_over_alpha':str(epsilon),'epsilon_residue_mod_P':int(poly(epsilon)(fp(2))),'prime_valuation_data':prime_rows,'selected_denominator_linear_coefficient':int(linear_den),'alpha_linear_coefficient':int(linear_alpha),'alpha2_linear_coefficient':int(linear_alpha2),'canonical_local_residue':res1,'modified_local_residue':res2,'factorial_mod_p':fac,'bad_eta2_delta_residue':int(poly(baddelta)(fp(2))),'required_delta_residue':r,'bad_hilbert90_free_solution':[str(x) for x in badsol],'good_hilbert90_free_solution':[str(x) for x in goodsol],'bnfcertify':cert,'unit_action_T':[[int(x) for x in row] for row in T.rows()],'scope':'one exact classical finite validation at ell5,p11; beta=canonical alpha used as explicit validation truth, no PIP computation or quantum arithmetic execution; no prime sweep'}
Path(__file__).with_suffix('.json').write_text(json.dumps(report,indent=2,sort_keys=True)+'\n');log('complete',**report);out.close()

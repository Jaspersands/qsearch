from sage.all import *
from pathlib import Path
import json,time
started=time.monotonic()
logfile=Path(__file__).with_name('qsearch_cubic_circular_p313.log').open('w')
def log(tag,**kw):
 obj={'stage':tag,'elapsed_seconds':float(round(time.monotonic()-started,3)),**kw}
 out=json.dumps(obj,sort_keys=True);print(out,flush=True);logfile.write(out+'\n');logfile.flush()
p=313;g=int(primitive_root(p));H=sorted({pow(g,3*k,p) for k in range((p-1)//3)})
assert len(H)==104
log('input',p=p,g=g,cubic_residue_count=len(H))
L=CyclotomicField(p,names='z');z=L.gen();sigL=L.hom([z**g],L)
theta=sum((z**a for a in H),L.zero());f=theta.minpoly()
K=NumberField(f,names='t');t=K.gen();emb=K.hom([theta],L)
def coeffvec(v):
 v=L(v);a=v.list();return vector(QQ,a+[0]*(L.degree()-len(a)))
M=matrix(QQ,[coeffvec(emb(t**i)) for i in range(3)]).transpose()
rows=list(M.transpose().pivots());Minv=M.matrix_from_rows(rows).inverse()
def back(v):
 cv=coeffvec(v);w=Minv*vector(QQ,[cv[i] for i in rows]);ans=sum((K(w[i])*t**i for i in range(3)),K.zero())
 assert emb(ans)==v
 return ans
st=back(sigL(theta));sig=K.hom([st],K)
assert sig(sig(sig(t)))==t and sig(t)!=t
log('cubic_field',polynomial=str(f),discriminant=int(K.discriminant()),sigma_t=str(st))
bnf=K.pari_bnf(proof=True);cert=int(bnf.bnfcertify());assert cert==1
Cl=K.class_group(proof=True);U=K.unit_group(proof=True)
log('certified_arithmetic',bnfcertify=cert,class_invariants=[int(x) for x in Cl.invariants()],unit_invariants=[int(x) for x in U.invariants()],unit_generators=[str(x) for x in U.gens_values()])
alpha=prod((1-z**a for a in H),L.one());alpha1=sigL(alpha)
a0=back(alpha);a1=back(alpha1);ratio=a1/a0
log('alpha',alpha=str(a0),alpha1=str(a1),ratio=str(ratio),alpha_norm=int(a0.norm()))
c=ratio.sqrt();assert c*c==ratio
units=list(U.gens_values());invs=list(U.invariants());free=[i for i,v in enumerate(invs) if v==0];assert len(free)==2
ulogs=lambda u:[int(x) for x in U.log(u)]
freelog=lambda u:vector(ZZ,[ulogs(u)[i] for i in free])
T=matrix(ZZ,[freelog(sig(units[i])) for i in free]).transpose()
assert T**3==identity_matrix(ZZ,2) and T*T+T+identity_matrix(ZZ,2)==0
cvec=freelog(c);scvec=freelog(sig(c));assert T*cvec==scvec
log('unit_action',c=str(c),c_log=ulogs(c),sigma_c_log=ulogs(sig(c)),T=[list(map(int,row)) for row in T.rows()])
assert list(Cl.invariants())==[7]
I=list(Cl.gens_ideals())[0];J=K.ideal([sig(x) for x in I.gens()])
i_coord=[int(x) for x in bnf.bnfisprincipal(I.pari_hnf(),0)]
j_coord=[int(x) for x in bnf.bnfisprincipal(J.pari_hnf(),0)]
assert len(i_coord)==len(j_coord)==1 and i_coord[0]%7!=0
r=int(GF(7)(j_coord[0])/GF(7)(i_coord[0]));rinv=int(GF(7)(r)**(-1))
assert r in (2,4)
V=ZZ**2;Lc=V.submodule([cvec,scvec]);basis=identity_matrix(ZZ,2)
def fitting(r):
 A=T-r*basis
 return V.submodule([7*v for v in basis.columns()]+list(A.columns()))
Lf=fitting(r);Lrev=fitting(rinv)
matlist=lambda A:[list(map(int,row)) for row in A.rows()]
report={'p':p,'g':g,'field_polynomial':str(f),'field_discriminant':int(K.discriminant()),'sigma_t':str(st),'bnfcertify':cert,'class_invariants':[7],'class_generator_ideal':str(I),'sigma_class_generator_ideal':str(J),'class_generator_coordinates':i_coord,'sigma_class_generator_coordinates':j_coord,'r':r,'r_inverse':rinv,'unit_generators':[str(x) for x in units],'unit_action_T':matlist(T),'alpha':str(a0),'alpha1':str(a1),'c_squared':str(ratio),'c':str(c),'c_unit_coordinates':ulogs(c),'sigma_c_unit_coordinates':ulogs(sig(c)),'circular_basis_rows':matlist(Lc.basis_matrix()),'fitting_same_action_basis_rows':matlist(Lf.basis_matrix()),'fitting_reverse_action_basis_rows':matlist(Lrev.basis_matrix()),'circular_index':int(abs(Lc.basis_matrix().det())),'fitting_index':int(abs(Lf.basis_matrix().det())),'reverse_fitting_index':int(abs(Lrev.basis_matrix().det())),'same_action_equal':Lc==Lf,'reverse_action_equal':Lc==Lrev,'scope':'single exact classical CAS control; explicit degree312 cyclotomic field allowed for control only; no quantum arithmetic execution'}
Path(__file__).with_name('qsearch_cubic_circular_p313.json').write_text(json.dumps(report,indent=2,sort_keys=True)+'\n')
log('complete',**report)
logfile.close()

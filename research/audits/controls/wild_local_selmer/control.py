"""Exact classical algebra controls; not an implementation or asymptotic proof.
Run with /opt/anaconda3/envs/qsearch-cas/bin/python (Sage CAS).
"""
import json
from pathlib import Path
from sage.all import QQ, ZZ, PolynomialRing, NumberField, Qp
R=PolynomialRing(QQ, 'x');x=R.gen()
h=x*x-3;k=x**3-9;f=h*k
assert f.is_squarefree() and f.degree()==5
K=NumberField(h,'a');a=K.gen();L=NumberField(k,'b');b=L.gen()
A=9-3*a;B=b*b-3
assert A.norm()==54 and B.norm()==54
pa=K.primes_above(3);pb=L.primes_above(3)
assert len(pa)==len(pb)==1
va=int(K.ideal(A).valuation(pa[0]));vb=int(L.ideal(B).valuation(pb[0]))
assert (va,vb)==(3,3)
assert int(pa[0].ramification_index())==2
assert int(pb[0].ramification_index())==3
F=Qp(3,prec=32);Rp=PolynomialRing(F,'z');z=Rp.gen()
factors=Rp(f).factor()
assert sorted(t.degree() for t,e in factors)==[2,3]
rows=[]
for N in [1,2,4,8]:
 roots=[ZZ(1)]+[3**N*j for j in range(1,5)]
 fN=R.one()
 for r in roots:fN*=x-r
 assert fN.is_squarefree()
 assert all((F(1-r)).is_square() for r in roots[1:])
 rows.append({'N':N,'degree':int(fN.degree()),'rational_factors':len(fN.factor()),'coefficient_bits':max(abs(ZZ(c)).nbits() for c in fN),'discriminant_3_valuation':int(fN.discriminant().valuation(3)),'raw_constant_hit_fraction':str(QQ(1)/3**N)})
result={'status':'PASS','scope':'Exact classical algebra only; all-unramified and density statements proved separately in topic note.','f':str(f),'factor_degrees_Q3':[2,3],'genus':2,'local_image_dimension_by_Stoll_4_4':1,'branch_label':['9-3*a','b^2-3'],'norms':[54,54],'total_norm':54**2,'normalized_valuations':[va,vb],'ramification_indices':[2,3],'sampler_family':rows,'general_selmer_algorithm':False,'general_wild_local_algorithm':False,'speedup_or_hardness':False,'quantum_execution':False}
Path(__file__).with_suffix('.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'status':'PASS','norms':result['norms'],'valuations':result['normalized_valuations'],'family_cases':len(rows)}))

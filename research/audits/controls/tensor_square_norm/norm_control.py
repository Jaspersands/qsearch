"""One exact non-Galois tensor-norm and integer-saturation control, no full solver."""
import json
from itertools import combinations
from pathlib import Path
from sage.all import QQ, ZZ, GF, PolynomialRing, NumberField, matrix, gcd, prod, pari

R = PolynomialRing(QQ,'x');x=R.gen();f=x**5-x-1
L=NumberField(f,'a');a=L.gen()
assert L.discriminant()==2869
assert int(pari('polgalois(x^5-x-1)')[0])==120
Y=PolynomialRing(L,'y');y=Y.gen()
g=(y**5-y-1).quo_rem(y-a)
assert g[1]==0
g=g[0]
assert g.degree()==4 and g.is_irreducible()

# Unramified p=2 has degrees 2,3. Construct an element of the pair factor
# reducing to zero on the oriented (degree2,degree3) component only.
F2=PolynomialRing(GF(2),'t');t=F2.gen()
u=t**2+t+1;v=t**3+t**2+1
assert F2(f)==u*v
one,s,tcoef=u.xgcd(v)
assert one==1
EA=(tcoef*v) % F2(f)
e=R([int(z) for z in EA.list()])
assert (EA%u)==1 and (EA%v)==0
P=sorted(L.primes_above(2),key=lambda p:p.residue_class_degree())
assert [int(p.residue_class_degree()) for p in P]==[2,3]

values=None
for offset in [0,1]:
    first=1-e(a)*(1-e(y))+2*offset
    second=1-e(y)*(1-e(a))+2*offset
    n1=g.resultant(first);n2=g.resultant(second)
    assert n1 and n2
    ratio=n1/n2
    vals=[int(L.ideal(ratio).valuation(p)) for p in P]
    if vals==[3,-2]:
        values=(n1,n2,ratio,offset,vals);break
assert values is not None
n1,n2,ratio,offset,vals=values
assert ratio.norm()==1 and ratio!=1
assert n1.norm()==n2.norm()

# Tensor trace determinant: no auxiliary-field/maximal-order assumption.
T=matrix(QQ,5,5,lambda i,j:(a**(i+j)).trace())
assert T.det()==2869
assert T.tensor_product(T).det()==2869**10

# Integer kernels: a fixed star and raw nonprimitive moves lose saturation.
def saturation_index(M):
    rank=M.rank()
    minors=[abs(M.matrix_from_rows_and_columns(rows,cols).det())
            for rows in combinations(range(M.nrows()),rank)
            for cols in combinations(range(M.ncols()),rank)]
    return int(gcd(minors))
star=matrix(ZZ,[[3,-2,0],[5,0,-2]])
allpairs=matrix(ZZ,[[3,-2,0],[5,0,-2],[0,5,-3]])
assert saturation_index(star)==2 and saturation_index(allpairs)==1
assert saturation_index(matrix(ZZ,[[4,-2]]))==2
assert saturation_index(matrix(ZZ,[[2,-1]]))==1

# Standard CLASSICAL PARI norm solver on the same degree5 field, positive
# witness verified directly. This finite baseline is not a complexity claim.
baseline=pari('bnfisnorm(bnfinit(z^5-z-1),31)')
assert baseline[1]==1 and baseline[0].norm()==31
assert (a+2).norm()==31

# Compact powers: use exact finite prime coordinates for this control only.
# The general written algorithm uses a classical gcd-free basis instead.
large=ZZ(2)**256+1
atoms=[n1,n2,L(12),L(18),L(8),a+2,L(-1)]
exponents=[large,-large,2*large,-large,-large,ZZ(1),ZZ(1)]
norms=[QQ(b.norm()) for b in atoms]
coordinates={}
sign=0
for value,power in zip(norms,exponents):
    if value<0: sign=(sign+power)%2
    for prime,multiplicity in abs(value).factor():
        coordinates[int(prime)]=coordinates.get(int(prime),ZZ(0))+power*multiplicity
coordinates={str(p):int(z) for p,z in coordinates.items() if z}
assert coordinates=={'31':1} and sign==1
assert sign!=0  # sign-free comparison would incorrectly accept target +31
assert max(z.nbits() for z in exponents)==258

out={'scope':'one exact degree5 field plus fixed saturation/compact-output controls',
     'field':'Q[a]/(a^5-a-1)','degree':5,'galois_group_order':120,
     'tensor_factor_degrees':[5,20],'field_discriminant':2869,
     'p2_residue_degrees':[2,3],'cross_pair_residue_degree':6,
     'paired_norm_ratio_nontrivial':True,'paired_absolute_norm':str(ratio.norm()),
     'paired_p2_valuations':vals,'chosen_offset':offset,
     'tensor_order_discriminant_identity':True,
     'fixed_star_index':2,'all_pair_index':1,'unprimitive_index':2,
     'pari_classical_positive_witness_norm':'31',
     'compact_max_exponent_bits':258,'compact_norm':'-31',
     'compact_power_expansion':False,'sign_omission_rejected':True,
     'claims':{'general_solver_executed':False,'quantum_execution':False,
               'asymptotic_from_control':False,'GRH_verified':False,'speedup':False}}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,separators=(',',':')))

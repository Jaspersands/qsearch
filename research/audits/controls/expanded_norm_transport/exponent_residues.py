"""Exact finite falsifiers; no compact backend or asymptotic claim."""
from sage.all import QQ, PolynomialRing, NumberField, matrix, vector, QuaternionAlgebra
from pathlib import Path
import json

def relative_norm(z, K, gen, degree):
    cols=[]
    for j in range(degree):
        a=list((z*gen**j).list()); a += [K(0)]*(degree-len(a))
        cols.append(vector(K,a))
    return matrix(K,cols).transpose().det()

def run(K, degree, scalar, name):
    R=PolynomialRing(K,'t'); t=R.gen()
    L=K.extension(t**degree-scalar,name); v=L.gen()
    if K is QQ:
        u=v-1
    else:
        u=(1+v)/(1-v)
    nu=relative_norm(u,K,v,degree)
    assert nu in (K(1),K(-1))
    huge=2**160+1; exps=[huge+2,huge+1,-degree*(huge+1)]
    atoms=[u,L(scalar),v]
    assert v**degree==L(scalar)
    target=nu**(exps[0] % 2)
    residues=[e % degree for e in exps]
    beta0=L(1)
    for atom,e in zip(atoms,residues): beta0 *= atom**e
    c=relative_norm(beta0,K,v,degree)/target
    P=PolynomialRing(K,'Z'); Z=P.gen()
    roots=(Z**degree-c).roots(multiplicities=False)
    assert roots
    out=beta0/L(roots[0])
    assert relative_norm(out,K,v,degree)==target
    return dict(base_degree=int(K.degree()),relative_degree=degree,exponent_bits=max(abs(e).bit_length() for e in exps),residues=residues,root_correction=str(roots[0]),norm_verified=True)

results=[run(QQ,d,QQ(2),'v'+str(d)) for d in (2,3,5)]
R=PolynomialRing(QQ,'x'); K=NumberField(R.gen()**2-3,'a')
results.append(run(K,2,1+K.gen(),'w'))
B=QuaternionAlgebra(QQ,-1,-1,names=('i','j','k')); i,j,k=B.gens()
r=1+i; u=(i+j)*r; v=r; c=QQ(-2)
assert u.reduced_norm()+c*v.reduced_norm()==0
assert u*v.conjugate()+v*u.conjugate()==0
x=u/v; y0=i-j; y=(x/2)*y0
assert x*x==c and y*y==-1 and x*y==-y*x
C=matrix(QQ,[[1,0,-1],[1,0,1],[0,-1,0]])
A=matrix.diagonal(QQ,[2,1,2]); Id=matrix.identity(QQ,3)
assert C.transpose()*Id*C==A
assert C.det()==2 and all((2*q).denominator()==1 for q in C.inverse().list())
# Clifford agreement alone is insufficient: determinant squareclass matters.
assert not QQ(2).is_square()
report={'scope':'Finite exact controls only. Huge original powers never evaluated. No norm backend, local-offset algorithm or all-input theorem tested.','norm_cases':results,'quaternion_noncentral_denominator':True,'expanded_isometry':True,'exceptional_prime_support':[2],'determinant_guard':True}
Path(__file__).with_name('result.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({'norm_cases':len(results),'quaternion':True,'isometry':True,'determinant_guard':True}))

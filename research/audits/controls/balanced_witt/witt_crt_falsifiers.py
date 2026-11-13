"""Exact algebra controls for proposed Witt height repair; no height theorem."""
from sage.all import QQ, PolynomialRing, NumberField, matrix, vector, floor
from pathlib import Path
import json

R = PolynomialRing(QQ, 'x'); x = R.gen()
K = NumberField(x*x+5, 'w'); w=K.gen()
O=K.maximal_order()
I=K.ideal(2,1+w)
assert I.norm()==2 and not I.is_principal()
crt=[]
for power in (1,3,7):
    J=I**power
    # A supplied nonzero element suffices for this finite congruence control.
    # The theorem separately must pay the Minkowski-LLL short-vector bound.
    gamma=min(J.basis(),key=lambda z: abs(z.norm()))
    assert gamma and gamma in J
    for u0 in (K(12345)+987*w,K(-22)+333*w):
        coeffs=list((u0/gamma).list()); coeffs += [QQ(0)]*(2-len(coeffs))
        m=[floor(c+QQ(1)/2) for c in coeffs]
        u=u0-gamma*(m[0]+m[1]*w)
        assert u in O and u-u0 in J
        residual=list((u/gamma).list()); residual += [QQ(0)]*(2-len(residual))
        assert all(abs(c)<=QQ(1)/2 for c in residual)
        crt.append({'power':power,'modulus_norm':str(J.norm()),'congruence':True})

# Half-integral relative coordinates in integral quadratic elements.
E=NumberField(x*x+15, 't'); t=E.gen(); z=(1+t)/2
a=QQ(3); b=QQ(5); zbar=(1-t)/2
s0=(z+zbar)/2; t0=a*(z-zbar)/(2*t)
assert z.is_integral() and (2*b*s0).is_integral() and (2*b*t0).is_integral()
assert 2*b*t0 == -(z-zbar)*t
assert a*(2*b*s0)**2+b*(2*b*t0)**2 == a*(2*b)**2*z*zbar

# Hyperbolic normalization and complementary projection over imaginary K.
A=matrix.diagonal(K,[1,2,-1,3]); v=vector(K,[1,0,1,0])
assert v*A*v==0
y=vector(K,[1,0,0,0])/(v*A*vector(K,[1,0,0,0]))
y=y-(y*A*y)*v/2
assert v*A*y==1 and y*A*y==0
comp=[]
for u in [vector(K,[0,1,0,0]),vector(K,[0,0,0,1])]:
    u=u-(u*A*y)*v-(u*A*v)*y
    assert u*A*v==0 and u*A*y==0
    comp.append(u)
P=matrix(K,[v,y]+comp).transpose()
assert P.det()!=0
assert P.transpose()*A*P==matrix(K,[[0,1,0,0],[1,0,0,0],[0,0,2,0],[0,0,0,3]])
report={'scope':'Finite exact controls only. No norm/LLL backend, height bound, or native Witt algorithm tested.',
        'nonprincipal_crt':crt,'integral_2b_parameters':True,'hyperbolic_projection':True}
Path(__file__).with_name('witt_crt_result.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({'crt_cases':len(crt),'integral_parameters':True,'hyperbolic_projection':True}))

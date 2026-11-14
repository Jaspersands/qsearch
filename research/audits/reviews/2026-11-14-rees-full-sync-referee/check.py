from fractions import Fraction as F
import sympy as sp
def s(p): return F(p-3,p)**2*F(p-1,p)
def q(p): return F((p*p-1)*(p*p-p)*(p-1)**2, p**6)
for p in [5,7,11,13,5000,5003]:
    m = 36 if p%3==2 else 144
    print(p, 's=',float(s(p)), 'qadm=',float(q(p)), 'copies=',float(18*m/q(p)+2))
# counts
for p in [5,7]:
    print(p, 1+(p+1)+p*p+1+p*(p+1)+1+2*p**3*(p+1)+2*p*p*(p+1)+p*(p+1)+(p+1)+1)
# i*=1 case: P2 = sum s_i^2 lam_i with s1 l1+s2 l2+s3 l3=0
s1,s2,s3=sp.symbols('s1 s2 s3'); l1=sp.Matrix(sp.symbols('a0 a1')); l2=sp.Matrix(sp.symbols('b0 b1'))
l3=-(s1*l1+s2*l2)/s3
P2=sp.simplify(s1**2*l1+s2**2*l2+s3**2*l3)
print('P2 =',sp.factor(P2[0]))
# coefficient on l2 is s2(s2-s3): zero iff s2=s3; then kappa
kap=sp.simplify((P2.subs(s3,s2))[0]/l1[0]) if False else sp.factor(sp.expand(P2.subs(s3,s2))[0])
print('P2|s3=s2 :',kap)
# Lemma W: tensor varpi(e) m(z)^2, nonsym part
e0,e1,z0,z1,x0,x1,L0,L1=sp.symbols('e0 e1 z0 z1 x0 x1 L0 L1')
n=L0*x0+L1*x1
varpi=lambda v:(x0*v[1]-x1*v[0])/n
mm=lambda v:L0*v[0]+L1*v[1]
e=(e0,e1); z=(z0,z1)
T=sp.Rational(1,2)*varpi(e)*mm(z)**2
Sym=sp.Rational(1,2)*(varpi(e)*mm(z)**2+2*mm(e)*varpi(z)*mm(z))/3
print('nonsym + (1/3)det(e,z)m(z):', sp.simplify(T-Sym + sp.Rational(1,3)*(e0*z1-e1*z0)*mm(z)))
# Lemma 0': character value vs -q'
j,k,psi,e3,etc,t,nn=sp.symbols('j k psi e3 etac t n')
A3=-nn**2/6*psi; A2=k*nn/2*psi+nn/2*e3; A1=-j*psi-k*e3+etc
qp=A1+2*A2*t+3*A3*t**2
chi=j*psi+k*(e3-t*psi*nn)-(etc+t*nn*e3-t**2/2*psi*nn**2)
print('chi + qprime =', sp.simplify(chi+qp))
# expansion f23:expand
Y,tau,c,ss,phi=sp.symbols('Y tau c s phi')
qq=lambda X:A1*X+A2*X**2+A3*X**3
v=c*ss*phi
lhs=sp.expand((qq(Y+tau*v)-qq(Y))/phi)
rhs=sp.expand(tau*c*ss*sp.diff(qq(Y),Y)+tau**2*c**2*ss**2*phi*(A2+3*A3*Y)+tau**3*c**3*ss**3*phi**2*A3)
print('expand diff:', sp.simplify(lhs-rhs))

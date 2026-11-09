# Gauge-fixed block formulation of Aut(L_DL (x) K) (checker id: dl, 9 Nov 2026). Independent of earlier scripts.
# Same block form as gen_block_ideal.py, with M, C, N substituted by the formulas forced by the homomorphism
# conditions, and the gauge B e1 = B e2 = 0.  The gauge is valid because for every derivation D of the
# paper's 4-parameter family (lambda,mu,nu,rho; x_j=0; checked to be derivations in derivations.sage),
# exp(D)=1+D+D^2/2 is an automorphism (D^2 L lies in the centre, so all terms [D^j x, D^l y] with j+l>=3 vanish),
# acting trivially on (A,M,C) and moving B to B + M*D_W, and {B e1 = B e2 = 0} is a complement of
# {D_W} = {(b1,b2,J'b2,Jb1)}.  So the projection to (A,M,C) and the image on the centre are unchanged.
import sys, itertools, sympy as sp
N8=8
TABLE = {(1,2):{5:1},(1,3):{6:1},(1,4):{7:1},(1,5):{8:-1},(2,3):{8:1},
         (2,4):{6:1},(2,6):{7:-1},(3,4):{5:-1},(3,5):{7:-1},(4,6):{8:-1}}
def br_basis(i,j):
    if (i,j) in TABLE: return TABLE[(i,j)]
    if (j,i) in TABLE: return {k:-c for k,c in TABLE[(j,i)].items()}
    return {}
def bracket(x,y):
    out=[0]*N8
    for i in range(N8):
        if x[i]==0: continue
        for j in range(N8):
            if y[j]==0: continue
            for k,c in br_basis(i+1,j+1).items():
                out[k-1]+=c*x[i]*y[j]
    return [sp.expand(o) for o in out]
def e(k):
    v=[0]*N8; v[k-1]=1; return v
A=sp.Matrix(4,4,lambda r,c: sp.Symbol(f'a{r+1}{c+1}'))
B=sp.Matrix(2,4,lambda r,c: 0 if c<2 else sp.Symbol(f'b{r+1}{c+1}'))
t=sp.Symbol('t')
def V(j): return [A[k,j-1] for k in range(4)]+[B[0,j-1],B[1,j-1],0,0]   # phi(e_j), j<=4
def Aonly(j): return [A[k,j-1] for k in range(4)]+[0,0,0,0]
br12=bracket(Aonly(1),Aonly(2)); br13=bracket(Aonly(1),Aonly(3))
M=sp.Matrix([[br12[4],br13[4]],[br12[5],br13[5]]])                 # columns M e5, M e6
Me5=[0,0,0,0,M[0,0],M[1,0],0,0]; Me6=[0,0,0,0,M[0,1],M[1,1],0,0]
x35=bracket(Aonly(3),Me5); x15=bracket(Aonly(1),Me5)
C=sp.Matrix([[-x35[6],-x15[6]],[-x35[7],-x15[7]]])                  # columns C e7, C e8 (from [e3,e5]=-e7,[e1,e5]=-e8)
f12=bracket(V(1),V(2)); f13=bracket(V(1),V(3))
Nm=sp.Matrix([[f12[6],f13[6]],[f12[7],f13[7]]])                     # columns N e5, N e6
eqs=[]
for i,j in itertools.combinations(range(1,5),2):
    bxy=bracket(e(i),e(j)); Wxy=sp.Matrix(bxy[4:6]); Zxy=sp.Matrix(bxy[6:8])
    b=bracket(V(i),V(j))
    for k in range(2): eqs.append(sp.expand(b[4+k]-(M*Wxy)[k]))
    for k in range(2): eqs.append(sp.expand(b[6+k]-(Nm*Wxy)[k]-(C*Zxy)[k]))
for i in range(1,5):
    for w,Mw in ((5,Me5),(6,Me6)):
        bxw=bracket(e(i),e(w)); Zxw=sp.Matrix(bxw[6:8])
        b=bracket(Aonly(i),Mw)
        for k in range(8):
            target=(C*Zxw)[k-6] if k>=6 else 0
            eqs.append(sp.expand(b[k]-target))
eqs.append(sp.expand(A.det()*t-1))
eqs=[q for q in dict.fromkeys(eqs) if q!=0]
Avars=[str(s) for s in A]; Bv=['b13','b23','b14','b24']
def s(q): return str(q).replace('**','^')
mode=sys.argv[1]; char=sys.argv[2]; out=sys.argv[3]
minpoly=sys.argv[4] if len(sys.argv)>4 else None
ringchar = f'({char},w)' if minpoly else char
with open(out,'w') as f:
    f.write(f'// gauge-fixed block formulation, {len(eqs)} generators, char {char}, mode {mode}\n')
    f.write('LIB "primdec.lib";\n')
    f.write(f'ring r = {ringchar}, ({",".join(Bv+["t"]+Avars)}), dp;\n')
    if minpoly: f.write(f'minpoly = {minpoly};\n')
    f.write('option(redSB);\n')
    f.write('ideal I = '+',\n'.join(s(q) for q in eqs)+';\n')
    f.write('int t0 = rtimer;\nI = std(I);\nprint("dim, vdim of the gauge-fixed automorphism ideal:"); print(dim(I)); print(vdim(I));\n')
    f.write('ideal R = std(radical(I)); print("vdim of radical (number of component points over the algebraic closure):"); print(vdim(R));\n')
    cpolys=[s(sp.expand(C[r,c])) for r in range(2) for c in range(2)]
    f.write(f'ring r2 = {ringchar}, ({",".join(Bv+["t"]+Avars)},c11,c12,c21,c22,z,x), (dp(21),dp(6));\n')
    if minpoly: f.write(f'minpoly = {minpoly};\n')
    f.write('option(redSB);\nideal R = imap(r,R);\n')
    f.write(f'ideal Cdef = c11-({cpolys[0]}), c12-({cpolys[1]}), c21-({cpolys[2]}), c22-({cpolys[3]});\n')
    elim='*'.join(Bv+['t']+Avars)
    f.write(f'ideal Jc = eliminate(R+Cdef+ideal(z,x), {elim});\n')
    f.write(f'ring rc = {ringchar}, (c11,c12,c21,c22), dp;\n')
    if minpoly: f.write(f'minpoly = {minpoly};\n')
    f.write('option(redSB);\nideal Jc = std(imap(r2,Jc));\nprint("image on the centre (C e7 = c11 e7 + c21 e8, C e8 = c12 e7 + c22 e8): vdim of radical =");\nideal RC=std(radical(Jc)); print(vdim(RC)); print(RC);\n')
    f.write('print("minimal associated primes of the image (each is one point over the base field or a Galois orbit):");\nlist L=minAssGTZ(RC); int k; for(k=1;k<=size(L);k++){print(L[k]); print("--");}\n')
    f.write('setring r2;\n')
    f.write(f'ideal Jz = eliminate(R+Cdef+ideal(c12,c21,c11-z,c22-z,x), {elim}*c11*c12*c21*c22*x);\n')
    f.write(f'ideal Jx = eliminate(R+Cdef+ideal(x^2-(c11+c22)*x+(c11*c22-c12*c21), z), {elim}*c11*c12*c21*c22*z);\n')
    f.write(f'ring rz = {ringchar}, (z,x), dp;\n')
    if minpoly: f.write(f'minpoly = {minpoly};\n')
    f.write('ideal Jz = std(imap(r2,Jz)); ideal Jx = std(imap(r2,Jx));\nprint("SCALARS: ideal in z of zeta with C = zeta*Id:"); print(Jz); int kk; for(kk=1;kk<=size(Jz);kk++){print(factorize(Jz[kk]));}\nprint("EIGENVALUES on the centre: ideal in x:"); print(Jx); for(kk=1;kk<=size(Jx);kk++){print(factorize(Jx[kk]));}\n')
    f.write('print("seconds:"); print(rtimer-t0);\nquit;\n')
print(len(eqs),'generators ->',out)

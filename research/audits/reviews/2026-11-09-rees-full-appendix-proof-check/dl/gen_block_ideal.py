# Block formulation of Aut(L_DL (x) K) for Groebner elimination (checker id: dl, 9 Nov 2026). Independent of earlier scripts.
# L = V + W + Z with V=span(e1..e4), W=span(e5,e6), Z=span(e7,e8) (W+Z = gamma_2, Z = gamma_3 = centre; both are
# characteristic ideals, so every automorphism has the block form below).  phi(x) = A x + B x (+ central part, which
# enters no bracket) for x in V; phi(w) = M w + N w for w in W; phi(z) = C z for z in Z.  The homomorphism conditions are
#   (E1) W-part of [Ax+Bx, Ay+By] = M (W-part of [x,y])                       x,y in V
#   (E2) [A x, M w] = C [x, w]                                                 x in V, w in W
#   (E3) Z-part of [Ax+Bx, Ay+By] = N (W-part of [x,y]) + C (Z-part of [x,y])  x,y in V
# (all other pairs hold trivially since [W,W]=[W,Z]=[V,Z]=0), plus det(A) t = 1.  A homomorphism with A invertible is
# surjective (L nilpotent), hence an automorphism.  B and N enter linearly; the unipotent part of Aut acts only on (B,N),
# so the projection to (A,M,C) is the finite 'component' set.
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
A=sp.Matrix(4,4,lambda r,c: sp.Symbol(f'a{r+1}{c+1}'))   # column c = coords of A e_{c+1} in e1..e4
B=sp.Matrix(2,4,lambda r,c: sp.Symbol(f'b{r+1}{c+1}'))   # column c = W-coords (e5,e6) of B e_{c+1}
M=sp.Matrix(2,2,lambda r,c: sp.Symbol(f'm{r+1}{c+1}'))
Nm=sp.Matrix(2,2,lambda r,c: sp.Symbol(f'n{r+1}{c+1}'))
C=sp.Matrix(2,2,lambda r,c: sp.Symbol(f'c{r+1}{c+1}'))   # column c = coords of C e_{7+c} in (e7,e8)
t=sp.Symbol('t')
def full(vV=None,vW=None,vZ=None):
    v=[0]*8
    if vV is not None:
        for k in range(4): v[k]=vV[k]
    if vW is not None:
        for k in range(2): v[4+k]=vW[k]
    if vZ is not None:
        for k in range(2): v[6+k]=vZ[k]
    return v
eqs=[]
for i,j in itertools.combinations(range(1,5),2):
    x=e(i); y=e(j); bxy=bracket(x,y); Wxy=sp.Matrix(bxy[4:6]); Zxy=sp.Matrix(bxy[6:8])
    px=full(list(A[:,i-1]),list(B[:,i-1])); py=full(list(A[:,j-1]),list(B[:,j-1]))
    b=bracket(px,py)
    for k in range(2): eqs.append(sp.expand(b[4+k]-(M*Wxy)[k]))                       # E1
    for k in range(2): eqs.append(sp.expand(b[6+k]-(Nm*Wxy)[k]-(C*Zxy)[k]))          # E3
for i in range(1,5):
    for w in (5,6):
        x=e(i); bxw=bracket(x,e(w)); Zxw=sp.Matrix(bxw[6:8])
        b=bracket(full(list(A[:,i-1])),full(None,list(M[:,w-5])))
        for k in range(8):
            target=(C*Zxw)[k-6] if k>=6 else 0
            d=sp.expand(b[k]-target)
            if d!=0: eqs.append(d)                                                   # E2
eqs.append(sp.expand(A.det()*t-1))
eqs=[q for q in dict.fromkeys(eqs) if q!=0]
Avars=[str(s) for s in A]; Mv=[str(s) for s in M]; Cv=['c11','c12','c21','c22']; Bv=[str(s) for s in B]; Nv=[str(s) for s in Nm]
def s(q): return str(q).replace('**','^')
char=sys.argv[1]; out=sys.argv[2]; fieldeq=(len(sys.argv)>3 and sys.argv[3]=='rational')
allv=Bv+Nv+Avars+Mv+['t']+Cv
with open(out,'w') as f:
    f.write(f'// block formulation, {len(eqs)} generators, char {char}, rational-points mode {fieldeq}\n')
    f.write('LIB "primdec.lib";\n')
    f.write(f'ring r = {char}, ({",".join(allv)}), dp;\noption(redSB);\n')
    f.write('ideal I = '+',\n'.join(s(q) for q in eqs)+';\n')
    if fieldeq:
        p=int(char)
        f.write('ideal F = '+','.join(f'{v}^{p}-{v}' for v in Avars+Mv+Cv)+';\nI = I + F;\n')
    f.write('int t0 = rtimer;\n')
    f.write('ideal J0 = eliminate(I, '+'*'.join(Bv+Nv)+');\n')
    f.write('ring r0 = '+char+', ('+','.join(Avars+Mv+['t']+Cv)+'), dp;\noption(redSB);\nideal J0 = std(imap(r,J0));\n')
    f.write('print("component ideal in (A,M,t,C): dim, vdim, vdim of radical:");\nprint(dim(J0)); print(vdim(J0)); ideal R0=std(radical(J0)); print(vdim(R0));\n')
    f.write('ideal J1 = eliminate(R0, '+'*'.join(Avars+Mv+['t'])+');\n')
    f.write('ring rc = '+char+', ('+','.join(Cv)+'), dp;\noption(redSB);\nideal J1 = std(imap(r0,J1));\n')
    f.write('print("image on the centre, ideal in c11,c12,c21,c22 (column convention: C e7 = c11 e7 + c21 e8):");\nprint(J1);\nprint("dim, vdim, vdim radical:"); print(dim(J1)); print(vdim(J1)); ideal R1=std(radical(J1)); print(vdim(R1));\n')
    f.write('print("characteristic polynomials / minimal associated primes of the image:");\nlist L=minAssGTZ(R1); int k; for(k=1;k<=size(L);k++){print(L[k]);}\n')
    f.write('ring rz = '+char+', (z,'+','.join(Cv)+'), dp;\nideal S = imap(rc,R1) + ideal(c12, c21, c11-z, c22-z);\nideal Jz = eliminate(S, c11*c12*c21*c22);\nring rzz = '+char+', (z), dp;\nideal Jz = std(imap(rz,Jz));\nprint("scalar set: ideal in z of central scalars:");\nprint(Jz); if(size(Jz)>0){print(factorize(Jz[1]));}\n')
    f.write('ring rt = '+char+', (x,'+','.join(Cv)+'), dp;\nideal T = imap(rc,R1) + ideal(x^2-(c11+c22)*x+(c11*c22-c12*c21));\nideal Jx = eliminate(T, c11*c12*c21*c22);\nring rxx = '+char+', (x), dp;\nideal Jx = std(imap(rt,Jx));\nprint("eigenvalue set: ideal in x of all eigenvalues on the centre:");\nprint(Jx); if(size(Jx)>0){print(factorize(Jx[1]));}\n')
    f.write('print("seconds:"); print((rtimer-t0));\nquit;\n')
print(len(eqs),'generators ->',out)

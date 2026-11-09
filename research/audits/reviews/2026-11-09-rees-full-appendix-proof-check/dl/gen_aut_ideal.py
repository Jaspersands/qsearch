# Generates Singular scripts for the automorphism variety of L_DL (checker id: dl, 9 Nov 2026).
# Independent of earlier scripts.  An automorphism phi is given by phi(e_j) = sum_{k<=6} a(6(j-1)+k) e_k, j=1..4
# (the e7,e8 parts of phi(e_1..e_4) never enter a bracket, so they are set to 0 WLOG),
# phi(e5)=[phi e1,phi e2], phi(e6)=[phi e1,phi e3], phi(e7)=[phi e1,phi e4], phi(e8)=[phi e2,phi e3]
# (forced for every homomorphism), and the ideal imposes phi[e_i,e_j]=[phi e_i,phi e_j] for all 28 pairs,
# det(A)*t=1 for the 4x4 block A (equivalent to bijectivity for a homomorphism of a nilpotent algebra),
# and either phi(e7)=z e7, phi(e8)=z e8 (mode 'scalar') or phi(e7)=c11 e7+c21 e8, phi(e8)=c12 e7+c22 e8 (mode 'image').
import sys, itertools, sympy as sp
N=8
TABLE = {(1,2):{5:1},(1,3):{6:1},(1,4):{7:1},(1,5):{8:-1},(2,3):{8:1},
         (2,4):{6:1},(2,6):{7:-1},(3,4):{5:-1},(3,5):{7:-1},(4,6):{8:-1}}
def br_basis(i,j):
    if (i,j) in TABLE: return TABLE[(i,j)]
    if (j,i) in TABLE: return {k:-c for k,c in TABLE[(j,i)].items()}
    return {}
def bracket(x,y):
    out=[0]*N
    for i in range(N):
        if x[i]==0: continue
        for j in range(N):
            if y[j]==0: continue
            for k,c in br_basis(i+1,j+1).items():
                out[k-1]+=c*x[i]*y[j]
    return [sp.expand(o) for o in out]
a=sp.symbols('a1:25'); t,z=sp.symbols('t z'); c11,c12,c21,c22=sp.symbols('c11 c12 c21 c22')
phi=[None]*8
for j in range(4):
    phi[j]=[a[6*j+k] for k in range(6)]+[0,0]
phi[4]=bracket(phi[0],phi[1]); phi[5]=bracket(phi[0],phi[2]); phi[6]=bracket(phi[0],phi[3]); phi[7]=bracket(phi[1],phi[2])
eqs=[]
for i,j in itertools.combinations(range(1,9),2):
    lhs=[0]*N
    for k,c in br_basis(i,j).items():
        lhs=[l+c*m for l,m in zip(lhs,phi[k-1])]
    rhs=bracket(phi[i-1],phi[j-1])
    for l,r in zip(lhs,rhs):
        d=sp.expand(l-r)
        if d!=0: eqs.append(d)
A=sp.Matrix(4,4,lambda j,k:a[6*j+k])
eqs.append(sp.expand(A.det()*t-1))
mode=sys.argv[1]; char=sys.argv[2]; out=sys.argv[3]
if mode=='scalar':
    for k in range(8):
        eqs.append(sp.expand(phi[6][k]-(z if k==6 else 0)))
        eqs.append(sp.expand(phi[7][k]-(z if k==7 else 0)))
    extra='t,z'
elif mode=='image':
    for k in range(8):
        eqs.append(sp.expand(phi[6][k]-(c11 if k==6 else c21 if k==7 else 0)))
        eqs.append(sp.expand(phi[7][k]-(c12 if k==6 else c22 if k==7 else 0)))
    extra='t,c11,c12,c21,c22'
eqs=[q for q in dict.fromkeys(eqs) if q!=0]
def s(q): return str(q).replace('**','^')
vars_=','.join(f'a{i}' for i in range(1,25))
elimprod='*'.join(f'a{i}' for i in range(1,25))+'*t'
with open(out,'w') as f:
    f.write(f'// {len(eqs)} generators, mode {mode}, char {char}\n')
    f.write(f'ring r = {char}, ({vars_},{extra}), dp;\noption(redSB);\n')
    f.write('ideal I = '+',\n'.join(s(q) for q in eqs)+';\n')
    f.write('int t0=timer;\n')
    f.write(f'ideal J = eliminate(I, {elimprod});\n')
    if mode=='scalar':
        f.write('ring rz = '+char+', (z), dp;\nideal J = imap(r, J);\nJ = std(J);\nprint("elimination ideal in z:");\nprint(J);\nprint(factorize(J[1]));\n')
    else:
        f.write('ring rc = '+char+', (c11,c12,c21,c22), dp;\nideal J = imap(r, J);\nJ = std(J);\nprint("elimination ideal in c (image on centre):");\nprint(J);\nprint("dim:"); print(dim(J)); print("vdim (number of points with multiplicity, over the algebraic closure):"); print(vdim(J));\nprint("radical vdim:"); LIB "primdec.lib"; ideal R=radical(J); R=std(R); print(vdim(R));\n')
    f.write('quit;\n')
print(len(eqs),'equations written to',out)

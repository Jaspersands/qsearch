# Slice (as dl2) + scalar central action zeta: test, for each zeta in F_p^x, whether any automorphism
# over the algebraic closure of F_p acts on the centre as zeta (ideal = (1) means none).
import sys, time
T = {(1,2):(5,1),(1,3):(6,1),(1,4):(7,1),(1,5):(8,-1),(2,3):(8,1),(2,4):(6,1),(2,6):(7,-1),(3,4):(5,-1),(3,5):(7,-1),(4,6):(8,-1)}
def br(x,y):
    z=[0]*8
    for (a,b),(c,s) in T.items():
        z[c-1]+= s*(x[a-1]*y[b-1]-x[b-1]*y[a-1])
    return z
for mode in sys.argv[1:]:
    F = QQ if mode=='Q' else GF(int(mode))
    names=['a%d%d'%(k,j) for j in range(1,5) for k in range(1,7)]+['t','z']
    R=PolynomialRing(F,names,order='degrevlex'); g=R.gens(); t=g[-2]; z=g[-1]
    X={}; idx=0
    for j in range(1,5):
        for k in range(1,7):
            X[k,j]=g[idx]; idx+=1
    phi={j:[X[k,j] for k in range(1,7)]+[R(0),R(0)] for j in range(1,5)}
    phi[5]=br(phi[1],phi[2]); phi[6]=br(phi[1],phi[3]); phi[7]=br(phi[1],phi[4]); phi[8]=br(phi[2],phi[3])
    eqs=[X[5,1],X[6,1],X[5,2],X[6,2]]
    eqs+=[phi[7][k]-(z if k==6 else 0) for k in range(8)]+[phi[8][k]-(z if k==7 else 0) for k in range(8)]
    for a in range(1,9):
      for b in range(a+1,9):
        lhs=br(phi[a],phi[b]); rhs=[R(0)]*8
        if (a,b) in T:
            c,s=T[(a,b)]; rhs=[s*w for w in phi[c]]
        eqs+=[l-r for l,r in zip(lhs,rhs)]
    A=matrix(R,4,4,lambda k,j:X[k+1,j+1]); eqs.append(t*A.det()-1)
    I=R.ideal([q for q in set(eqs) if q!=0]); t0=time.time()
    if mode=='Q':
        E=I.elimination_ideal(list(g[:-1]))
        print("Q elimination ideal in zeta:",[factor(q) for q in E.gens()],"time %.1f"%(time.time()-t0))
    else:
        out=[(int(c),'none' if (I+R.ideal([z-c])).groebner_basis()==[1] else 'EXISTS') for c in F if c!=0]
        print(mode,out,"time %.1f"%(time.time()-t0))
    sys.stdout.flush()

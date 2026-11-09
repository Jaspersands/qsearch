import sys, time
T = {(1,2):(5,1),(1,3):(6,1),(1,4):(7,1),(1,5):(8,-1),(2,3):(8,1),(2,4):(6,1),(2,6):(7,-1),(3,4):(5,-1),(3,5):(7,-1),(4,6):(8,-1)}
def br(x,y,F):
    z=[F(0)]*8
    for (a,b),(c,s) in T.items():
        z[c-1]+= s*(x[a-1]*y[b-1]-x[b-1]*y[a-1])
    return z
def E(j,F):
    v=[F(0)]*8; v[j-1]=F(1); return v
mode=sys.argv[1]
if mode=='table':
    K.<I>=QuadraticField(-1)
    e=[E(j,K) for j in range(1,9)]
    # Jacobi
    bad=0
    for a in e:
      for b in e:
        for c in e:
          j=[x+y+z for x,y,z in zip(br(a,br(b,c,K),K),br(b,br(c,a,K),K),br(c,br(a,b,K),K))]
          bad+= any(j)
    print("Jacobi failures:",bad)
    add=lambda *vs:[sum(t) for t in zip(*vs)]
    sc=lambda s,v:[s*t for t in v]
    u1=add(sc(I,e[0]),e[3]); u2=add(e[2],sc(-I,e[1])); u3=add(e[3],sc(-I,e[0])); u4=add(e[2],sc(I,e[1]))
    vp=add(e[4],sc(I,e[5])); vm=add(e[4],sc(-I,e[5]))
    for nm,x,y in [("u1u2",u1,u2),("u3u4",u3,u4),("u1u3",u1,u3),("u2u4",u2,u4),("u1u4",u1,u4),("u2u3",u2,u3),("u1v+",u1,vp),("u2v+",u2,vp),("u3v-",u3,vm),("u4v-",u4,vm),("u1v-",u1,vm),("u2v-",u2,vm),("u3v+",u3,vp),("u4v+",u4,vp),("v+v-",vp,vm)]:
        print(nm, br(x,y,K))
    print("2v+",sc(2,vp),"2v-",sc(2,vm))
    sys.exit()
# Groebner: phi(e_j)=sum_{k<=6} X[k,j] e_k for j=1..4 ; phi(e5..e8) defined via brackets
F = QQ if mode=='Q' else GF(int(mode))
names=['a%d%d'%(k,j) for j in range(1,5) for k in range(1,7)]+['z','t']
R=PolynomialRing(F,names,order='degrevlex')
g=R.gens(); z=g[-2]; t=g[-1]
X={}
idx=0
for j in range(1,5):
    for k in range(1,7):
        X[k,j]=g[idx]; idx+=1
phi={}
for j in range(1,5):
    phi[j]=[X[k,j] for k in range(1,7)]+[R(0),R(0)]
phi[5]=br(phi[1],phi[2],R); phi[6]=br(phi[1],phi[3],R)
phi[7]=br(phi[1],phi[4],R); phi[8]=br(phi[2],phi[3],R)
eqs=[]
eqs+= [phi[7][k]-(z if k==6 else 0) for k in range(8)]
eqs+= [phi[8][k]-(z if k==7 else 0) for k in range(8)]
for a in range(1,9):
  for b in range(a+1,9):
    lhs=br(phi[a],phi[b],R)
    rhs=[R(0)]*8
    if (a,b) in T:
        c,s=T[(a,b)]; rhs=[s*w for w in phi[c]]
    eqs+=[l-r for l,r in zip(lhs,rhs)]
A=matrix(R,4,4,lambda k,j:X[k+1,j+1])
eqs.append(t*A.det()-1)
eqs=[q for q in set(eqs) if q!=0]
I=R.ideal(eqs)
t0=time.time()
if len(sys.argv)>2 and sys.argv[2]=='elim':
    J=I.elimination_ideal([v for v in g if v!=z])
    print(mode,"elimination ideal in z:",J.gens(), [factor(q) for q in J.gens()], "time",time.time()-t0)
else:
    out=[]
    for c in F:
        if c==0: continue
        one = (I+R.ideal([z-c])).groebner_basis()==[1]
        out.append((c, 'none' if one else 'EXISTS'))
    print(mode, out, "time", time.time()-t0)

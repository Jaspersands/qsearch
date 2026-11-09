import sympy as sp, itertools
n=8
br={(1,2):{5:1},(1,3):{6:1},(1,4):{7:1},(1,5):{8:-1},(2,3):{8:1},(2,4):{6:1},(2,6):{7:-1},(3,4):{5:-1},(3,5):{7:-1},(4,6):{8:-1}}
def b(i,j):
    v=[0]*(n+1)
    if (i,j) in br:
        for k,c in br[(i,j)].items(): v[k]+=c
    elif (j,i) in br:
        for k,c in br[(j,i)].items(): v[k]-=c
    return v
def bv(x,y):
    r=[0]*(n+1)
    for i in range(1,n+1):
        for j in range(1,n+1):
            if x[i] and y[j]:
                w=b(i,j)
                for k in range(1,n+1): r[k]+=x[i]*y[j]*w[k]
    return r
E=lambda i:[1 if k==i else 0 for k in range(n+1)]
bad=0
for i,j,k in itertools.combinations(range(1,n+1),3):
    a=bv(E(i),bv(E(j),E(k)));bb=bv(E(j),bv(E(k),E(i)));c=bv(E(k),bv(E(i),E(j)))
    if any(a[t]+bb[t]+c[t] for t in range(n+1)): bad+=1
print('jacobi failures',bad)
D=sp.Matrix(n,n,lambda r,c: sp.Symbol(f'd{r}_{c}'))
eqs=[]
for i,j in itertools.combinations(range(1,n+1),2):
    lhs=D*sp.Matrix(b(i,j)[1:])
    Di=D[:,i-1];Dj=D[:,j-1]
    rhs=sp.Matrix(bv([0]+list(Di),E(j))[1:])+sp.Matrix(bv(E(i),[0]+list(Dj))[1:])
    eqs+=list(lhs-rhs)
syms=list(D)
A,_=sp.linear_eq_to_matrix(eqs,syms)
print('eqs',len(eqs),'rank Q',A.rank())
for p in [5,7,11,13,17,19,23]:
    print(p, sp.Matrix(A).applyfunc(lambda x: x% p).rank(iszerofunc=lambda x: x%p==0))
l,mu,nu,rho=sp.symbols('l mu nu rho'); xs=sp.symbols('x1:9')
cols={1:{5:l,6:mu,7:xs[0],8:xs[1]},2:{5:-nu,6:rho,7:xs[2],8:xs[3]},3:{5:-rho,6:-nu,7:xs[4],8:xs[5]},4:{5:mu,6:-l,7:xs[6],8:xs[7]},5:{7:mu,8:nu},6:{7:l,8:rho},7:{},8:{}}
Dm=sp.zeros(n,n)
for c,d in cols.items():
    for r,v in d.items(): Dm[r-1,c-1]=v
sub=dict(zip(syms,list(Dm)))
res=[sp.simplify(e.subs(sub)) for e in eqs]
print('family derivation failures',sum(1 for e in res if e!=0))
def rank_mod(M,p):
    M=[[int(x)%p for x in row] for row in M]; r=0; cols=len(M[0])
    for c in range(cols):
        piv=next((i for i in range(r,len(M)) if M[i][c]),None)
        if piv is None: continue
        M[r],M[piv]=M[piv],M[r]; inv=pow(M[r][c],-1,p)
        M[r]=[x*inv%p for x in M[r]]
        for i in range(len(M)):
            if i!=r and M[i][c]:
                f=M[i][c]; M[i]=[(a-f*b)%p for a,b in zip(M[i],M[r])]
        r+=1
    return r
Al=A.tolist()
print({p:rank_mod(Al,p) for p in [2,3,5,7,11,13,17,19,23,29,31]})

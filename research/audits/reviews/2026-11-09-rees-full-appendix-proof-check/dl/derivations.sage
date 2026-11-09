# Derivation system of L_DL over Z (checker id: dl, 9 Nov 2026). Independent of earlier scripts.
# Unknown D = (d_{kl}), D e_l = sum_k d_{kl} e_k ; equations D[e_i,e_j] = [D e_i, e_j] + [e_i, D e_j], 1<=i<j<=8.
import itertools
TABLE = {(1,2):{5:1},(1,3):{6:1},(1,4):{7:1},(1,5):{8:-1},(2,3):{8:1},
         (2,4):{6:1},(2,6):{7:-1},(3,4):{5:-1},(3,5):{7:-1},(4,6):{8:-1}}
def brb(i,j):
    if (i,j) in TABLE: return TABLE[(i,j)]
    if (j,i) in TABLE: return {k:-c for k,c in TABLE[(j,i)].items()}
    return {}
idx = lambda k,l: 8*(k-1)+(l-1)   # variable index of d_{kl}
rows=[]
for i,j in itertools.combinations(range(1,9),2):
    for out in range(1,9):
        row=[0]*64
        # D[e_i,e_j] coefficient on e_out: sum_m c_m d_{out,m}
        for m,c in brb(i,j).items(): row[idx(out,m)]+=c
        # [D e_i, e_j]: sum_k d_{k i} [e_k,e_j]
        for k in range(1,9):
            for o,c in brb(k,j).items():
                if o==out: row[idx(k,i)]-=c
            for o,c in brb(i,k).items():
                if o==out: row[idx(k,j)]-=c
        rows.append(row)
Mz=matrix(ZZ,rows)
print("equations x variables:", Mz.nrows(), "x", Mz.ncols(), " (nonzero rows:", sum(1 for r in Mz.rows() if r!=0), ")")
print("rank over Q:", Mz.rank())
ed=[d for d in Mz.elementary_divisors() if d!=0]
print("nonzero elementary divisors (count, distinct values):", len(ed), sorted(set(ed)))
print("primes dividing some elementary divisor:", sorted(set(p for d in ed for p in ZZ(d).prime_factors())))
for p in primes(2,60):
    print("p=%d: rank mod p = %d, dim Der = %d" % (p, Mz.change_ring(GF(p)).rank(), 64-Mz.change_ring(GF(p)).rank()))
# kernel over Q vs the paper's parametrisation (main.tex l.455-460)
K=Mz.right_kernel()
print("dim Der over Q:", K.dimension())
def Dmat(lam,mu,nu,rho,X):  # X: 4x2 list, x_j = X[j][0] e7 + X[j][1] e8
    D=matrix(QQ,8,8)
    col={1:{5:lam,6:mu},2:{5:-nu,6:rho},3:{5:-rho,6:-nu},4:{5:mu,6:-lam}}
    for l in range(1,5):
        for k,c in col[l].items(): D[k-1,l-1]+=c
        D[6,l-1]+=X[l-1][0]; D[7,l-1]+=X[l-1][1]
    D[6,4]+=mu; D[7,4]+=nu; D[6,5]+=lam; D[7,5]+=rho
    return D
gens=[]
for a in range(4):
    v=[0]*4; v[a]=1; gens.append(Dmat(*v,[[0,0]]*4))
for j in range(4):
    for s in range(2):
        X=[[0,0] for _ in range(4)]; X[j][s]=1; gens.append(Dmat(0,0,0,0,X))
vecs=[vector(QQ,[g[k,l] for k in range(8) for l in range(8)]) for g in gens]
print("paper's 12 generators satisfy the system:", all(Mz*v==0 for v in vecs), "; they span dim", matrix(vecs).rank())
print("paper's span equals the full kernel over Q:", span(vecs)==K.change_ring(QQ))
# char 3: does some derivation fail to map L into [L,L] = span(e5..e8), or fail to be nilpotent?
K3=Mz.change_ring(GF(3)).right_kernel()
print("char 3: dim Der =", K3.dimension())
bad=[v for v in K3.basis() if any(v[idx(k,l)]!=0 for k in range(1,5) for l in range(1,9))]
print("char 3: basis derivations with a component D e_l -> e_k, k<=4:", len(bad))
nonnil=0
for v in K3.basis():
    D=matrix(GF(3),8,8,lambda k,l: v[8*k+l])
    if D^8!=0: nonnil+=1
print("char 3: non-nilpotent basis derivations:", nonnil)
# random combinations in char 3
import random
random.seed(int(1))
cnt=0
for trial in range(int(200)):
    v=sum(GF(3)(random.randint(int(0),int(2)))*b for b in K3.basis())
    D=matrix(GF(3),8,8,lambda k,l: v[8*k+l])
    if D^8!=0: cnt+=1
print("char 3: non-nilpotent among 200 random derivations:", cnt)

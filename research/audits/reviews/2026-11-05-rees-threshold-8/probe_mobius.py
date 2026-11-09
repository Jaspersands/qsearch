# Probe: is the witness row set {y_i} (points of P^1) invariant under a Mobius map?
import sys, itertools
INF=None
def mob(M,x,p):
    a,b,c,d=M
    if x is INF:
        return INF if c==0 else a*pow(c,-1,p)%p
    num=(a*x+b)%p; den=(c*x+d)%p
    return INF if den==0 else num*pow(den,-1,p)%p
def mob_from3(src,dst,p):
    # Mobius sending src[0..2] -> dst[0..2]; use cross-ratio construction via matrices
    def to01inf(z):
        z1,z2,z3=z
        # map z1->0, z2->inf, z3->1 : (x-z1)(z3-z2)/((x-z2)(z3-z1))
        def m(v):
            return v
        # build matrix
        if z1 is INF: A=(0,(z3-z2)%p,1,(-z2)%p)  # x-> (z3-z2)/(x-z2)
        elif z2 is INF: A=(1,(-z1)%p,0,(z3-z1)%p)
        elif z3 is INF: A=(1,(-z1)%p,1,(-z2)%p)
        else: A=((z3-z2)%p,(-z1*(z3-z2))%p,(z3-z1)%p,(-z2*(z3-z1))%p)
        return A
    def mul(A,B):
        a,b,c,d=A; e,f,g,h=B
        return ((a*e+b*g)%p,(a*f+b*h)%p,(c*e+d*g)%p,(c*f+d*h)%p)
    def inv(A):
        a,b,c,d=A; return (d,(-b)%p,(-c)%p,a)
    return mul(inv(to01inf(dst)),to01inf(src))
def run(p,pts):
    S=set(pts); found=[]
    for img in itertools.permutations(pts,3):
        M=mob_from3(pts[:3],list(img),p)
        if all(mob(M,x,p) in S for x in pts):
            # order
            o=1; x=pts[0]; 
            perm={x:mob(M,x,p) for x in pts}
            if any(perm[x]!=x for x in pts): found.append((M,perm))
    return found
if __name__=='__main__':
    p=3529
    u=[1, 0, 2787, 1922, 1194, 1102, 71, 708, 954]
    pts=[INF if t==0 else pow(t,-1,p) for t in u]
    f=run(p,pts)
    print('nontrivial Mobius symmetries of the 9-point row set at p=3529:',len(f))
    for M,perm in f[:5]: print(M)

# Independent symbolic checks for prop:dl-central-scalars (checker id: dl, 9 Nov 2026).
# Written from the paper text only (T/main.tex lines 446-492); no earlier script reused.
# Run: nice -n 19 timeout 600 /opt/anaconda3/bin/python dl_symbolic.py
import itertools, sympy as sp

N = 8
# structure constants: (i,j) -> {k: coeff}, 1-based, only i<j listed (table of main.tex l.450-452)
TABLE = {(1,2):{5:1},(1,3):{6:1},(1,4):{7:1},(1,5):{8:-1},(2,3):{8:1},
         (2,4):{6:1},(2,6):{7:-1},(3,4):{5:-1},(3,5):{7:-1},(4,6):{8:-1}}
def br_basis(i,j):
    if i==j: return {}
    if (i,j) in TABLE: return dict(TABLE[(i,j)])
    if (j,i) in TABLE: return {k:-c for k,c in TABLE[(j,i)].items()}
    return {}
def bracket(x,y):
    """x,y: lists of length 8 (any ring elements)"""
    out=[0]*N
    for i in range(N):
        if x[i]==0: continue
        for j in range(N):
            if y[j]==0: continue
            for k,c in br_basis(i+1,j+1).items():
                out[k-1]+= c*x[i]*y[j]
    return out
def e(k):
    v=[0]*N; v[k-1]=1; return v

ok=True
# 1. Jacobi over Z
for a,b,c in itertools.combinations(range(1,N+1),3):
    s=[sum(t) for t in zip(bracket(e(a),bracket(e(b),e(c))),bracket(e(b),bracket(e(c),e(a))),bracket(e(c),bracket(e(a),e(b))))]
    if any(s): ok=False; print('Jacobi FAIL',a,b,c,s)
print('Jacobi over Z on all 56 triples:', 'OK' if ok else 'FAIL')

# 2. centre, gamma_2, gamma_3 over Q and mod p
def span_rank(vecs, p=None):
    M=sp.Matrix(vecs) if vecs else sp.zeros(1,N)
    if p is None: return M.rank()
    from sympy import GF
    from sympy.polys.matrices import DomainMatrix
    dM=DomainMatrix.from_Matrix(M).convert_to(GF(p))
    return dM.rank()
g2=[bracket(e(i),e(j)) for i in range(1,9) for j in range(1,9)]
g3=[bracket(e(i),v) for i in range(1,9) for v in g2]
g4=[bracket(e(i),v) for i in range(1,9) for v in g3]
for p in [None,3,5,7,11,13]:
    r2=span_rank(g2,p); r3=span_rank(g3,p); r4=span_rank(g4,p)
    # centre = kernel of x -> (ad x) ; matrix of x |-> [x,e_j] for all j stacked
    rows=[]
    for j in range(1,9):
        for k in range(N):
            rows.append([bracket(e(i),e(j))[k] for i in range(1,9)])
    rc=span_rank(rows,p)
    print(f'p={p}: dim g2={r2}, dim g3={r3}, dim g4={r4}, dim centre={N-rc}')
# g2 spanned by e5..e8, g3 by e7,e8 (exact over Z): check membership
assert all(all(v[k]==0 for k in range(4)) for v in g2)
assert all(all(v[k]==0 for k in range(6)) for v in g3)

# 3. new basis over Z[i] (sympy I), bracket table of the proof (main.tex l.471-479)
I=sp.I
def vec(d):
    v=[0]*N
    for k,c in d.items(): v[k-1]+=c
    return v
u1=vec({1:I,4:1}); u2=vec({3:1,2:-I}); u3=vec({4:1,1:-I}); u4=vec({3:1,2:I})
vp=vec({5:1,6:I}); vm=vec({5:1,6:-I}); e7=e(7); e8=e(8)
NB=[u1,u2,u3,u4,vp,vm,e7,e8]; names=['u1','u2','u3','u4','v+','v-','e7','e8']
B=sp.Matrix(NB).T  # columns = new basis in e-coordinates
print('det of change of basis =', sp.factor(sp.simplify(B.det())))
Binv=B.inv()
def coords(x):
    return [sp.nsimplify(sp.expand(c)) for c in (Binv*sp.Matrix(x))]
claimed={('u1','u2'):{'v+':2},('u3','u4'):{'v-':2},('u1','u3'):{'e7':2*I},('u2','u4'):{'e8':-2*I},
         ('u1','v+'):{'e8':-2*I},('u2','v+'):{'e7':-2},('u3','v-'):{'e8':2*I},('u4','v-'):{'e7':-2}}
bad=0
table_out=[]
for a,b in itertools.combinations(range(8),2):
    c=coords(bracket(NB[a],NB[b]))
    got={names[k]:sp.simplify(c[k]) for k in range(8) if sp.simplify(c[k])!=0}
    want=claimed.get((names[a],names[b]),{})
    if got!=want:
        bad+=1; print('MISMATCH',names[a],names[b],'got',got,'want',want)
    if got: table_out.append(f'[{names[a]},{names[b]}] = {got}')
print('new-basis bracket table: all 28 pairs', 'agree with the proof (incl. all zero brackets)' if bad==0 else f'{bad} mismatches')
for t in table_out: print('   ',t)

# 4. same identities in F_p[i] = F_p[x]/(x^2+1), p = 3,5,7,11,13 (pairs (a,b) = a+b i)
class Gi:
    def __init__(s,a,b,p): s.a=a%p; s.b=b%p; s.p=p
    def __add__(s,o):
        o=s._c(o); return Gi(s.a+o.a,s.b+o.b,s.p)
    __radd__=__add__
    def __mul__(s,o):
        o=s._c(o); return Gi(s.a*o.a-s.b*o.b,s.a*o.b+s.b*o.a,s.p)
    __rmul__=__mul__
    def __neg__(s): return Gi(-s.a,-s.b,s.p)
    def _c(s,o): return o if isinstance(o,Gi) else Gi(o,0,s.p)
    def __eq__(s,o):
        o=s._c(o); return s.a==o.a and s.b==o.b
    def __ne__(s,o): return not s.__eq__(o)
    def __repr__(s): return f'({s.a}+{s.b}i)'
for p in [3,5,7,11,13]:
    z=Gi(0,0,p); one=Gi(1,0,p); ii=Gi(0,1,p)
    def V(d):
        v=[z]*N
        for k,c in d.items(): v[k-1]=v[k-1]+c
        return v
    U1=V({1:ii,4:one}); U2=V({3:one,2:-ii}); U3=V({4:one,1:-ii}); U4=V({3:one,2:ii})
    VP=V({5:one,6:ii}); VM=V({5:one,6:-ii})
    def BR(x,y):
        out=[z]*N
        for i_ in range(N):
            for j_ in range(N):
                for k,c in br_basis(i_+1,j_+1).items():
                    out[k-1]=out[k-1]+c*x[i_]*y[j_]
        return out
    chk=[(BR(U1,U2),[c*2 for c in VP]),(BR(U3,U4),[c*2 for c in VM]),(BR(U1,U3),V({7:2*ii})),
         (BR(U2,U4),V({8:-2*ii})),(BR(U1,U4),V({})),(BR(U2,U3),V({})),
         (BR(U1,VP),V({8:-2*ii})),(BR(U2,VP),V({7:-2*one})),(BR(U3,VM),V({8:2*ii})),(BR(U4,VM),V({7:-2*one})),
         (BR(U1,VM),V({})),(BR(U2,VM),V({})),(BR(U3,VP),V({})),(BR(U4,VP),V({})),(BR(VP,VM),V({}))]
    good=all(all(a==b for a,b in zip(x,y)) for x,y in chk)
    print(f'F_{p}[i]: 15 bracket identities of the proof hold:', good)

# 5. psi maps and the determinant -1 claims
def br_e78(x,y):
    c=bracket(x,y); assert all(sp.simplify(c[k])==0 for k in range(6)); return sp.Matrix([c[6],c[7]])
psip=sp.Matrix.hstack(br_e78(u1,vp),br_e78(u2,vp)); psim=sp.Matrix.hstack(br_e78(u3,vm),br_e78(u4,vm))
print('psi+ matrix (cols u1,u2 -> (e7,e8)):',psip.tolist(),' det',sp.simplify(psip.det()))
print('psi- matrix (cols u3,u4 -> (e7,e8)):',psim.tolist(),' det',sp.simplify(psim.det()))
R1=sp.simplify(psim.inv()*psip); R2=sp.simplify(psip.inv()*psim)
print('psi-^{-1} psi+ in bases (u1,u2)->(u3,u4):',R1.tolist(),'det',R1.det())
print('psi+^{-1} psi- in bases (u3,u4)->(u1,u2):',R2.tolist(),'det',R2.det())

# 6. explicit automorphisms: sign map (paper), Z/3-grading map, permutation map tau
w=sp.symbols('w')  # w^2+w+1=0
def red(x): return sp.rem(sp.expand(x),w**2+w+1,w)
def is_aut(diag_or_map):
    # map: list of 8 image vectors
    phi=diag_or_map
    for a,b in itertools.combinations(range(1,9),2):
        lhs=[0]*N
        for k,c in br_basis(a,b).items():
            lhs=[l+c*m for l,m in zip(lhs,phi[k-1])]
        rhs=bracket(phi[a-1],phi[b-1])
        if any(red(l-r)!=0 for l,r in zip(lhs,rhs)): return False
    return True
def diagmap(ws): return [[ws[k] if j==k else 0 for j in range(N)] for k in range(N)]
sign=diagmap([1,-1,1,-1,-1,1,-1,-1])
print('sign automorphism (fix e1,e3,e6; negate others) is an automorphism:',is_aut(sign))
grad3=diagmap([w**2,w,w,w**2,1,1,w,w**2])
print('Z/3-grading map e1,e4->w^2, e2,e3->w, e5,e6->1, e7->w, e8->w^2 (w^2+w+1=0) is an automorphism:',is_aut(grad3))
tau=[e(3),e(4),e(1),e(2),[-c for c in e(5)],[-c for c in e(6)],[-c for c in e(8)],[-c for c in e(7)]]
print('tau: e1<->e3, e2<->e4, e5->-e5, e6->-e6, e7->-e8, e8->-e7 is an automorphism:',is_aut(tau))
# composite sign*grad3 acts on e7 by -w^2 (a primitive 6th root of unity)
print('sign o grad3 on e7: factor', sp.expand(-w**2), '(order 6 since w primitive cube root)')

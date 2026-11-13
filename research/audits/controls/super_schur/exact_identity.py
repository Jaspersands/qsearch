from sage.all import *
import json
from pathlib import Path

SF=SymmetricFunctions(QQ).schur()
rows=[]

def complete(E,O,n,R):
    h=[R.one()]+[R.zero() for _ in range(n)]
    for z in E:
        for r in range(1,n+1): h[r]+=z*h[r-1]
    for z in O:
        for r in range(n,0,-1): h[r]+=z*h[r-1]
    return h

def schur(part,h,R):
    if not part: return R.one()
    l=len(part)
    return matrix(R,l,l,lambda i,j:h[part[i]-i+j] if 0<=part[i]-i+j<len(h) else R.zero()).det()

def hook(part,d): return len(part)<=d or part[d]<=d

for d,e,max_n in [(1,1,6),(2,1,4),(2,2,4)]:
    R=PolynomialRing(QQ,names=tuple('x'+str(i) for i in range(d))+tuple('y'+str(i) for i in range(d))+tuple('u'+str(i) for i in range(e))+tuple('v'+str(i) for i in range(e)),order='lex')
    vv=R.gens(); x=vv[:d];y=vv[d:2*d];u=vv[2*d:2*d+e];v=vv[2*d+e:]
    E=[a*b for a in x for b in u]+[a*b for a in y for b in v]
    O=[a*b for a in x for b in v]+[a*b for a in y for b in u]
    hx=complete(x,y,max_n,R);hz=complete(u,v,max_n,R);ht=complete(E,O,max_n,R)
    for n in range(1,max_n+1):
        parts=list(Partitions(n));A=[a for a in parts if hook(a,d)];B=[b for b in parts if hook(b,e)]
        X={tuple(a):schur(a,hx,R) for a in parts};Z={tuple(b):schur(b,hz,R) for b in parts}
        assert all(X[tuple(a)]==0 for a in parts if not hook(a,d))
        assert all(Z[tuple(b)]==0 for b in parts if not hook(b,e))
        for a in A:
            expected=tuple(list(a[:d])+[0]*max(0,d-len(a))+[max(a.conjugate()[j]-d,0) if j<len(a.conjugate()) else 0 for j in range(d)]+[0]*(2*e))
            assert tuple(X[tuple(a)].exponents()[0])==expected
            assert X[tuple(a)].coefficients()[0]==1
        products={(tuple(a),tuple(b)): SF[a].kronecker_product(SF[b]) for a in A for b in B}
        for nu in parts:
            rhs=sum((products[(tuple(a),tuple(b))].coefficient(nu)*X[tuple(a)]*Z[tuple(b)] for a in A for b in B),R.zero())
            assert schur(nu,ht,R)==rhs,(d,e,n,nu)
        rows.append({'d':d,'e':e,'n':n,'targets':len(parts),'basis_pairs':len(A)*len(B),'identity':True,'hook_vanishing':True,'unit_leading_monomials':True})
    # Deliberately wrong tensor parity must disagree already at n=2.
    wrong=complete(E+O,[],2,R)
    assert schur(Partition([2]),wrong,R)!=schur(Partition([2]),ht,R)

out={'scope':'Finite exact Sage falsifiers only. No asymptotic theorem or speedup inferred. Ordinary Kronecker products are Sage reference values.','rows':rows,'wrong_tensor_parity_detected':True}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'cases':len(rows),'target_identities':sum(r['targets'] for r in rows),'wrong_parity_detected':True}))

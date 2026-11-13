from sage.all import GF, QQ, matrix
from itertools import combinations
from collections import Counter
import json
from pathlib import Path

def check(name, A):
    n, r = A.ncols(), A.rank()
    cache = {}
    def rank(S):
        key=tuple(sorted(S))
        if key not in cache:
            cache[key]=A.matrix_from_columns(key).rank() if key else 0
        return cache[key]
    def closure(S):
        S=set(S); q=rank(S)
        return {e for e in range(n) if rank(S|{e})==q}
    bases=[tuple(B) for B in combinations(range(n),r) if rank(B)==r]
    faces=[tuple(F) for F in combinations(range(n),r-1) if rank(F)==r-1]
    boundary=matrix(QQ,len(faces),len(bases)); rows={F:i for i,F in enumerate(faces)}
    for j,B in enumerate(bases):
        for a in range(r): boundary[rows[B[:a]+B[a+1:]],j]=(-1)**a
    L=boundary.transpose()*boundary
    expected=Counter()
    for B in bases:
        B1=set(B)
        while B1:
            V=closure(B1); active=[]
            for b in sorted(B1):
                bond={b}|{e for e in V-B1 if rank((B1-{b})|{e})==len(B1)}
                if b==min(bond): active.append(b)
            if not active: break
            B1.remove(active[0])
        expected[n-len(closure(B1))]+=1
    actual=Counter({int(a):int(m) for a,m in L.charpoly().roots(QQ)})
    assert sum(actual.values())==len(bases), 'nonrational eigenvalue'
    assert actual==expected, (actual,expected)
    return {'name':name,'rank':int(r),'n':n,'basis_count':len(bases),
            'exact_spectrum_multiplicities':dict(sorted(actual.items())),
            'greedy_decomposition_multiplicities':dict(sorted(expected.items())),
            'top_betti':int(L.ncols()-L.rank())}

u=matrix(GF(3),[[1,0,1,1],[0,1,1,2]])
edges=list(combinations(range(4),2))
g=matrix(GF(2),3,len(edges),lambda i,j:int(i in edges[j]))
result={'scope':'EXACT_FINITE_CONTROL_ONLY; proof uses KRS and ALOV, not finite spectra',
        'cases':[check('U_2_4',u),check('graphic_K4',g)],
        'quantum_advantage':False,'arbitrary_input_spectral_measure':False}
Path(__file__).with_name('result.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result))

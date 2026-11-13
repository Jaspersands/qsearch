from sage.all import QQ, matrix, identity_matrix, PolynomialRing
from itertools import product
from pathlib import Path
import json
V=matrix(QQ,[[1,1],[1,-1],[1,1],[1,-1]])/2
assert V.transpose()*V==identity_matrix(QQ,2)
P=PolynomialRing(QQ,['x','y']);x,y=P.gens()
A=[sum((V.row(j).column()*matrix(QQ,1,2,list(V.row(j))) for j in pair),matrix(QQ,2,2)) for pair in [(0,1),(2,3)]]
Z=(x*A[0]+y*A[1]).det().monomial_coefficient(x*y)
assert Z==QQ(1)/2
rows=[]
for z in product([0,1],repeat=2):
 R=V.matrix_from_rows([z[0],2+z[1]])
 if R.det()==0:continue
 X=V.matrix_from_rows([1-z[0],2+(1-z[1])])*R.inverse()
 assert X.transpose()*X==identity_matrix(QQ,2)
 rows.append({'choice':list(z),'chart_matrix':[list(map(str,row)) for row in X.rows()],'norm_exact':'1'})
assert len(rows)==2
out={'scope':'EXACT_BASE_BLOCK; direct sums prove the all-size chart counterfamily',
 'projection_normalizer':str(Z),'valid_charts':rows,'printed_Gram_scalar_left':5,'printed_Gram_scalar_right':17,
 'general_classical_sampler_closed':False,'hardness_claim':False}
Path(__file__).with_name('result.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out))

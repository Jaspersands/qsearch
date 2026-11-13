# Finite falsifier only: expanded huge square representatives, no theorem inference.
import json
R.<t> = QQ[]
F.<a> = NumberField(t^2-2)
eps=1+a
rows=[]
for k in [1, 10, 100, 1000]:
    alpha=3*eps^(2*k)/5^(2*k)
    ib=[F(5^k), 5^k*a]
    G=matrix(ZZ,2,2,lambda i,j: (alpha*ib[i]*ib[j]).trace())
    assert G.det()==72
    U=matrix(ZZ,pari(G).qflllgram())
    gamma=sum(U[i,0]*ib[i] for i in range(2))
    beta=alpha*gamma^2
    assert gamma!=0 and beta.is_integral()
    assert (beta/alpha).is_square()
    assert max(abs(c) for c in beta.list())<=12
    rows.append(dict(k=int(k), input_coefficient_bits=int(max(max(abs(c.numerator()).nbits(),c.denominator().nbits()) for c in alpha.list())), output_coefficients=[str(c) for c in beta.list()], gram_determinant=int(G.det())))
print(json.dumps(dict(scope='finite controls only, not growing-degree proof', rows=rows),indent=2))

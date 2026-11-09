"""Exact asymmetric F5 controls; finite algebraic falsifiers, not scaling evidence."""
from itertools import product

q = 5
F = GF(q)
mu = [QQ(v)/10 for v in [0, 1, 2, 3, 4]]
a = [QQ(v)/10 for v in [4, 0, 1, 3, 2]]
b = [QQ(v)/10 for v in [1, 4, 2, 0, 3]]
hs = [F(2), F(3), F(4)]

# Enumerate the actual planted observation and compare its outgoing error.
observed = [QQ(0)] * q
for x0, x1, x2, n, e1, e2 in product(range(q), repeat=6):
    j = F(n) - hs[0]*x0 - hs[1]*x1 - hs[2]*x2
    y1, y2 = F(x1+e1), F(x2+e2)
    y0 = -(j + hs[1]*y1 + hs[2]*y2)/hs[0]
    observed[int(y0-F(x0))] += mu[n]*a[e1]*b[e2]/q**3
predicted = [QQ(0)] * q
for n, e1, e2 in product(range(q), repeat=3):
    error = -(F(n)+hs[1]*e1+hs[2]*e2)/hs[0]
    predicted[int(error)] += mu[n]*a[e1]*b[e2]
assert observed == predicted and sum(observed) == 1
assert observed != [observed[(-j) % q] for j in range(q)]

# Enumerate both observations, keeping the actual relative-shift flag.
joint = {}
for x, e1, e2 in product(range(q), repeat=3):
    y1, y2 = (x+e1) % q, (x+e2) % q
    key = ((y1-y2) % q, y2, e2)
    joint[key] = joint.get(key, QQ(0)) + a[e1]*b[e2]/q
for h in range(q):
    d = sum(a[(j+h) % q]*b[j] for j in range(q))
    for y2 in range(q):
        assert sum(joint.get((h,y2,j),0) for j in range(q)) == d/q
        if d:
            for j in range(q):
                assert joint.get((h,y2,j),0)/(d/q) == a[(j+h) % q]*b[j]/d

# Independent Gram diagonalization versus the original-spin partition sum.
K = CyclotomicField(q)
omega = K.gen()
spectral = [sum(mu[z]*omega**(d*z) for z in range(q)) for d in range(q)]
checked = 0
for rows in [[[1,2,3], [2,4,1]], [[1,2,3], [2,1,4]]]:
    H = matrix(F, rows)
    code = list(H.right_kernel())
    image = list(H.row_space())
    N = len(code)
    gram = matrix(K, N, N, lambda i,j:
        prod(spectral[int(code[j][l]-code[i][l])] for l in range(3)))
    seen = set()
    for jt in product(range(q), repeat=3):
        J = vector(F, jt)
        coset = frozenset(tuple(int(v) for v in J+w) for w in image)
        if coset in seen:
            continue
        seen.add(coset)
        lam = N*sum(prod(mu[v] for v in z) for z in coset)
        character = vector(K, [omega**(-int(c.dot_product(J))) for c in code])
        assert gram*character == lam*character
        spin_partition = sum(prod(q*mu[int(z)] for z in J+H.transpose()*vector(F,x))
                             for x in product(range(q), repeat=H.nrows()))/q**H.nrows()
        assert spin_partition == lam
        checked += 1
    assert len(seen) == N
print('PASS: asymmetric F5 factor/error and weighted relative-shift laws.')
print('PASS: %d exact Gram/count eigenvalue controls, including rank deficiency.' % checked)

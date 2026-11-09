"""Exact output-stage controls; no growing-genus or parity-rank experiment."""
from itertools import product
F = GF(7)

def align(C, B):
    k, m = C.nrows(), C.ncols()
    equations = []
    for j in range(k):
        for i in range(m):
            row = [F(0)] * (k*k+m)
            for t in range(k):
                row[j*k+t] = C[t,i]
            row[k*k+i] = -B[j,i]
            equations.append(row)
    return matrix(F, equations).right_kernel()

points = list(F)
C = matrix(F, [[x**j for x in points] for j in range(2)])
U = matrix(F, [[x**j for x in points] for j in range(3)])
gamma = vector(F, [1,2,3,4,5,6,1])
S = matrix(F, [[1,2], [3,1]])
B = S*C*diagonal_matrix(gamma)
solutions = align(C,B)
assert solutions.dimension() == 1
v = solutions.basis()[0]
R, alpha = matrix(F,2,2,list(v[:4])), vector(F,v[4:])
assert R.det() and all(alpha)
assert R*C == B*diagonal_matrix(alpha)
distance = min((x*C).hamming_weight() for x in F**2 if x)
assert distance == 6 and 2*distance > C.ncols()

# A disconnected code at d=m/2 does not have a unique frame alignment.
split = matrix(F, [[1,1,0,0], [0,0,1,1]])
split_solutions = align(split,split)
assert split_solutions.dimension() == 2
assert min((x*split).hamming_weight() for x in F**2 if x) == 2
assert any(not all(v[4:]) for v in split_solutions.basis())

# All F7 points have barycentric residue -1; transport to the actual B.
h = -alpha
for i,j in product(range(3), repeat=2):
    assert B*vector(F,[h[t]*U[i,t]*U[j,t] for t in range(7)]) == 0
nu = F(3)
assert not nu.is_square()
a = vector(F,[1,1,0,0,0,0,0])
M = 2*B*diagonal_matrix(vector(F,[h[i]*a[i] for i in range(7)]))*U.transpose()
c = B*vector(F,[h[i]*(a[i]**2-nu) for i in range(7)])
assert M.rank() == 2
verified = 0
for s in F**2:
    t = M.solve_right(s-c)
    u = a+U.transpose()*t
    y = vector(F,[h[i]*(u[i]**2-nu) for i in range(7)])
    assert all(y) and B*y == s
    verified += 1

# Offset moments are provably uniform; enumerate the induced four dimensions.
moments = matrix(F, [[x**j for x in points] for j in range(4)])
assert moments.rank() == 4
bad = sum(matrix(F,[[z[0],z[1],z[2]],[z[1],z[2],z[3]]]).rank()<2
          for z in product(F, repeat=4))
assert bad == 49
assert QQ(bad)/7**4 < QQ(1)/7
print('PASS: unique frame recovery and strict-distance split-code countercontrol.')
print('PASS: %d original full-support syndromes; offset-rank failure49/2401.' % verified)

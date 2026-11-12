"""Exact count of Aut(L_DL (x) F_5) and of its image on the centre, to check the remark after
Prop 3.7 ("order 4*5^12 ... acts on the centre through a group of order 4 ... only scalars +-1").

Method (independent of the paper's GAP run):
 (1) verify by enumeration that the x in U = span(e1..e4) whose [x,L] has dimension 1 modulo gamma_3
     are exactly (U+ u U-) \ 0, so every automorphism's linear part A on L/gamma_2 preserves or swaps
     U+ and U- (U+ = <u1,u2>, U- = <u3,u4>, i = 2 in F_5);
 (2) for every such A (2 * |GL_2(F_5)|^2 = 460800 candidates) solve the (affine-linear) system for the
     e5,e6-components b of phi(e1..e4); the e7,e8-components are free (central, 5^8);
 (3) |Aut| = 5^8 * sum_A #solutions(b); collect the matrices of phi on gamma_3.
"""
from itertools import product
from lie import dixmier_lister, rank, rref, nullspace

p = 5
L = dixmier_lister(p)
I = 2
assert (I * I) % p == p - 1

def vec(d):
    v = [0] * 8
    for k, c in d.items():
        v[k] = c % p
    return v

e = [vec({i: 1}) for i in range(8)]
br = L.br

# (1) rank-1 locus
U_plus = [[(a * I) % p, (-b * I) % p, b, a] for a in range(p) for b in range(p)]  # a*u1 + b*u2
U_minus = [[(-a * I) % p, (b * I) % p, b, a] for a in range(p) for b in range(p)]  # a*u3 + b*u4
union = {tuple(x) for x in U_plus + U_minus if any(x)}
rank1 = set()
for x4 in product(range(p), repeat=4):
    if not any(x4):
        continue
    x = list(x4) + [0] * 4
    rows = [br(x, e[j])[4:6] for j in range(8)]
    if rank(rows, p) == 1:
        rank1.add(x4)
print("(1) rank-1 locus == (U+ u U-)\\0 :", rank1 == union, "size", len(rank1))

# change of basis T: columns u1..u4 in e1..e4 coordinates
u = [[I, 0, 0, 1], [0, -I % p, 1, 0], [-I % p, 0, 0, 1], [0, I, 1, 0]]
T = [[u[j][i] for j in range(4)] for i in range(4)]

def matmul(X, Y):
    return [[sum(X[i][k] * Y[k][j] for k in range(len(Y))) % p for j in range(len(Y[0]))] for i in range(len(X))]

def matinv(X):
    n = len(X)
    aug = [X[i][:] + [1 if i == j else 0 for j in range(n)] for i in range(n)]
    R, piv = rref(aug, p)
    assert piv == list(range(n))
    return [r[n:] for r in R]

Tinv = matinv(T)
GL2 = [[[a, b], [c, d]] for a, b, c, d in product(range(p), repeat=4) if (a * d - b * c) % p]

# affine elements: (const vector in F^8, list of 8 coefficient vectors for the b-variables)
NB = 8  # b_{j,t}: coefficient of e_{5+t} in phi(e_{j+1}), j=0..3, t=0..1

def aff_const(v):
    return (v[:], [[0] * 8 for _ in range(NB)])

def aff_add(X, Y, s=1):
    return ([(a + s * b) % p for a, b in zip(X[0], Y[0])], [[(a + s * b) % p for a, b in zip(r1, r2)] for r1, r2 in zip(X[1], Y[1])])

def aff_scale(X, s):
    return ([(s * a) % p for a in X[0]], [[(s * a) % p for a in r] for r in X[1]])

def aff_br(X, Y):
    const = br(X[0], Y[0])
    lin = [[(a + b) % p for a, b in zip(br(X[0], Y[1][k]), br(X[1][k], Y[0]))] for k in range(NB)]
    for k in range(NB):
        for l in range(NB):
            if any(X[1][k]) and any(Y[1][l]):
                assert not any(br(X[1][k], Y[1][l])), "quadratic term"
    return (const, lin)

pairs_table = {}
for i in range(8):
    for j in range(i + 1, 8):
        pairs_table[(i, j)] = br(e[i], e[j])

total = 0
centre_mats = set()
survivors = 0
for case in ("preserve", "swap"):
    for P in GL2:
        for Q in GL2:
            if case == "preserve":
                M = [[P[0][0], P[0][1], 0, 0], [P[1][0], P[1][1], 0, 0], [0, 0, Q[0][0], Q[0][1]], [0, 0, Q[1][0], Q[1][1]]]
            else:
                M = [[0, 0, Q[0][0], Q[0][1]], [0, 0, Q[1][0], Q[1][1]], [P[0][0], P[0][1], 0, 0], [P[1][0], P[1][1], 0, 0]]
            A = matmul(matmul(T, M), Tinv)  # column j = image of e_{j+1} in U
            cols = [[A[r][j] for r in range(4)] + [0] * 4 for j in range(4)]
            # quick prefilter modulo gamma_3: degree-2 relations
            b12 = br(cols[0], cols[1]); b13 = br(cols[0], cols[2])
            ok = True
            for (i, j) in [(0, 3), (1, 2), (1, 3), (2, 3)]:
                lhs = br(cols[i], cols[j])[4:6]
                rel = pairs_table[(i, j)]
                rhs = [(rel[4] * b12[4] + rel[5] * b13[4]) % p, (rel[4] * b12[5] + rel[5] * b13[5]) % p]
                if lhs != rhs:
                    ok = False
                    break
            if not ok:
                continue
            survivors += 1
            phi = [None] * 8
            for j in range(4):
                c_, lin = aff_const(cols[j])
                lin[2 * j][4] = 1
                lin[2 * j + 1][5] = 1
                phi[j] = (c_, lin)
            phi[4] = aff_br(phi[0], phi[1]); phi[5] = aff_br(phi[0], phi[2])
            phi[6] = aff_br(phi[0], phi[3]); phi[7] = aff_br(phi[1], phi[2])
            rows = []
            for (i, j), rel in pairs_table.items():
                lhs = aff_br(phi[i], phi[j])
                rhs = aff_const([0] * 8)
                for k in range(8):
                    if rel[k]:
                        rhs = aff_add(rhs, aff_scale(phi[k], rel[k]))
                d = aff_add(lhs, rhs, -1)
                for coord in range(8):
                    rows.append([d[1][kk][coord] for kk in range(NB)] + [(-d[0][coord]) % p])
            R, piv = rref(rows, p)
            if NB in piv:
                continue  # inconsistent
            dim = NB - len(piv)
            total += p ** dim
            # enumerate solutions to collect the action on gamma_3 = <e7,e8>
            part = [0] * NB
            for r, pc in zip(R, piv):
                part[pc] = r[NB]
            kern = nullspace([r[:NB] for r in R], NB, p)
            for coefs in product(range(p), repeat=len(kern)):
                bsol = part[:]
                for cc, kv in zip(coefs, kern):
                    bsol = [(x + cc * y) % p for x, y in zip(bsol, kv)]
                def ev(X):
                    return [(X[0][t] + sum(bsol[k] * X[1][k][t] for k in range(NB))) % p for t in range(8)]
                f7, f8 = ev(phi[6]), ev(phi[7])
                assert not any(f7[:6]) and not any(f8[:6])
                centre_mats.add(((f7[6], f8[6]), (f7[7], f8[7])))
print("(2) candidates passing the mod-gamma_3 prefilter:", survivors)
print("(3) sum_A #b =", total, " => |Aut| = 5^8 * %d = %d ; 4*5^12 = %d ; equal: %s" % (total, total * 5 ** 8, 4 * 5 ** 12, total * 5 ** 8 == 4 * 5 ** 12))
print("    image on the centre: %d matrices: %s" % (len(centre_mats), sorted(centre_mats)))
scal = [m for m in centre_mats if m[0][1] == 0 and m[1][0] == 0 and m[0][0] == m[1][1]]
print("    scalar ones:", scal)

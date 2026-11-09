"""Finite group falsifiers only; no hiding oracle or quantum algorithm."""
from sage.libs.gap.libgap import libgap

def subgroups(G):
    return [H for cl in libgap.ConjugacyClassesSubgroups(G) for H in cl.Elements()]

def permutes(H, K):
    return libgap.Size(libgap.ClosureGroup(H,K)) == (
        libgap.Size(H)*libgap.Size(K)/libgap.Size(libgap.Intersection(H,K)))

P = libgap.SmallGroup(27,4)
assert int(P.Exponent()) == 9 and not bool(P.IsAbelian())
subs = subgroups(P)
choices = [H for H in subs if int(H.Size()) == 3 and not bool(libgap.IsNormal(P,H))
           and all(permutes(H,K) for K in subs)]
assert choices
H = choices[0]
S = libgap.Subgroup(P, [x for x in P.Elements() if int(x.Order()) == 3])
assert int(S.Size()) == 9 and int(S.Exponent()) == 3
assert bool(libgap.IsSubgroup(S,H)) and bool(libgap.IsNormal(S,H))
print('PASS: nonnormal permutable order3 H in modular order27 P; normal in its order9 socle.')

U = libgap.SmallGroup(27,3)
assert int(U.Exponent()) == 3 and not bool(U.IsAbelian())
usubs = subgroups(U)
J = next(J for J in usubs if int(J.Size()) == 3 and not bool(libgap.IsNormal(U,J)))
assert any(not permutes(J,K) for K in usubs)
print('PASS: nonnormal Heisenberg line fails permutability; promise cannot be dropped.')

D = libgap.DihedralGroup(8)
killed = [x for x in D.Elements() if int(x.Order()) <= 2]
assert len(killed) == 6
assert int(libgap.Subgroup(D,killed).Size()) == 8
R = Integers(9)
X = matrix(R, [[0,1],[0,0]])
Y = matrix(R, [[-3,0],[0,0]])
assert X*Y-Y*X == 3*X
Id = identity_matrix(R,2)
exp_X, exp_Y = Id+X, Id+Y
exp_XplusY = Id+X+Y+(X+Y)**2/R(2)
assert exp_X.inverse()*exp_XplusY not in [exp_Y**j for j in range(3)]
print('PASS: D8 killed-by-2 set is not a subgroup; modular whole-ring additive shortcut also fails.')

# A nonhomomorphic public cube map still hides its torsion subgroup exactly.
from itertools import product
Id3 = identity_matrix(R,3)
matrices = [matrix(R,[[1,a,c],[0,1,b],[0,0,1]])
            for a,b,c in product(range(9), repeat=3)]
key = lambda M: tuple(M.list())
fibers = {}
for M in matrices:
    fibers.setdefault(key(M**3), []).append(M)
omega = fibers[key(Id3)]
assert len(omega) == 27 and len(fibers) == 27
for fiber in fibers.values():
    assert len(fiber) == 27
    assert {key(M) for M in fiber} == {key(fiber[0]*N) for N in omega}
g = matrix(R,[[1,1,0],[0,1,0],[0,0,1]])
h0 = matrix(R,[[1,0,0],[0,1,1],[0,0,1]])
assert (g*h0)**3 != (g**3)*(h0**3)
print('PASS: all729 UT3(Z/9) cube fibers equal the27 torsion cosets; cube is not a homomorphism.')

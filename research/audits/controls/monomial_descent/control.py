"""One exact classical cyclotomic control; no asymptotic solver is executed."""
from pathlib import Path
import json
from sage.all import CyclotomicField, ZZ, QQ, matrix, vector, identity_matrix, prod

E = CyclotomicField(7, names="z")
z = E.gen()
sigma = E.hom([z**3], E)
def sg(x, k):
    for _ in range(k % 6):
        x = sigma(x)
    return x

P = matrix(ZZ, [[0, 0, 1], [1, 0, 0], [0, 1, 0]])
B = matrix(ZZ, [[1, 1, 0], [0, 1, 1], [0, 0, 1]])
A = B * P * B.inverse()
assert A**3 == identity_matrix(ZZ, 3)
assert min(A.list()) < 0
def star(xs, k, reverse=False):
    ak = A**(-k if reverse else k)
    return [prod(sg(xs[j], k)**ak[i,j] for j in range(3)) for i in range(3)]

u = z + z**(-1)
t = u + 3
assert sg(t, 3) == t and t.norm() == 13**2
primes = E.primes_above(13)
assert len(primes) == 3
assert [int(p.residue_class_degree()) for p in primes] == [2, 2, 2]
tv = [int(E.ideal(t).valuation(p)) for p in primes]
assert sorted(tv) == [0, 0, 1]
m = B * vector(ZZ, [1, 0, 0])
transfer = [prod(sg(t, k)**((A**k * m)[i]) for k in range(3)) for i in range(3)]
assert all(star(transfer, k) == transfer for k in range(6))
assert star(transfer, 1, reverse=True) != transfer
at = primes[tv.index(1)]
primitive = vector(ZZ, [E.ideal(v).valuation(at) for v in transfer])
assert primitive == m
# D=<sigma^3> acts trivially on this lattice. Its norm is 2I, not invariants.
assert (identity_matrix(ZZ, 3) + A**3) * m == 2*m
assert any(int(v) % 2 for v in m)

beta = t / sg(t, 1)
assert beta.norm() == 1
beta_v = [int(E.ideal(beta).valuation(p)) for p in primes]
assert sorted(beta_v) == [-1, 0, 1]
y = [beta, z, -E.one()]
cocycle = [[y[i] / star(y, k)[i] for i in range(3)] for k in range(6)]
assert all(a.norm() == 1 for row in cocycle for a in row)
assert any(E.ideal(a).valuation(p) for row in cocycle for a in row for p in primes)

# Matched CLASSICAL arithmetic on this small field, not quantum S-units.
units = E.S_unit_group(S=primes)
gens = list(units.gens_values())
logs = lambda x: vector(ZZ, units.log(x))
w = int(units.gens_orders()[0])
assert w == 14
kappa = len(gens)
bg = [matrix(ZZ, [logs(sg(g, k)) for g in gens]).transpose() for k in range(6)]
rhs = matrix(ZZ, [logs(a) for a in cocycle[1]])

# One generator equation; Smith solving pays the finite classical endpoint.
M = matrix(ZZ, 3*kappa, 3*kappa+3)
for i in range(3):
    for ell in range(kappa):
        row = i*kappa+ell
        for j in range(3):
            for q in range(kappa):
                M[row, j*kappa+q] = int(i==j and ell==q) - A[i,j]*bg[1][ell,q]
        if ell == 0:
            M[row, 3*kappa+i] = -w
target = vector(ZZ, rhs.list())
D, L, R = M.smith_form()
v = L*target
coeff = vector(ZZ, M.ncols())
rank = M.rank()
for j in range(rank):
    assert v[j] % D[j,j] == 0
    coeff[j] = v[j] // D[j,j]
assert all(v[j] == 0 for j in range(rank, M.nrows()))
sol = R*coeff
assert M*sol == target
Z = matrix(ZZ, 3, kappa, list(sol[:3*kappa]))
def check(exponents):
    for k in range(6):
        rem = exponents - A**k*exponents*bg[k].transpose() - matrix(ZZ, [logs(a) for a in cocycle[k]])
        assert all(rem[i,0] % w == 0 for i in range(3))
        assert all(rem[i,j] == 0 for i in range(3) for j in range(1, kappa))
check(Z)

huge = ZZ(2)**256 + 1
ZI = matrix(ZZ, [logs(x) for x in transfer])
compact = Z + huge*ZI
check(compact)
eta = gens[0]
assert eta != 1 and eta.multiplicative_order() == w
assert eta**int(huge % w) != 1
assert all(logs(eta)[j] == 0 for j in range(1, kappa))

out = {
    "scope": "one degree6 cyclotomic field and exact classical S-unit descent control",
    "degree": 6, "galois_order": 6, "decomposition_order_at_13": 2,
    "residue_degrees": [2,2,2], "primitive_transfer_valuation": list(map(int, primitive)),
    "wrong_inverse_action_rejected": True, "norm_average_misses_primitive": True,
    "norm_one_hidden_support": beta_v, "all_cocycle_coordinate_norms": "1",
    "classical_S_unit_generator_count": kappa, "torsion_order": w,
    "integer_solve_verified_all_group_elements": True,
    "compact_exponent_max_bits": max(abs(e).nbits() for e in compact.list()),
    "compact_powers_expanded": False, "torsion_saturation_false_positive_rejected": True,
    "claims": {"general_solver_executed": False, "general_LS_executed": False,
               "quantum_execution": False, "GRH_verified": False, "speedup": False}
}
Path(__file__).with_suffix(".json").write_text(json.dumps(out, indent=2)+"\n")
print(json.dumps(out))

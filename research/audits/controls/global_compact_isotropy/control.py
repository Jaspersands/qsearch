"""Exact falsifiers/baselines, not execution of the proposed quantum solver."""
from pathlib import Path
import json
from sage.all import QQ, ZZ, PolynomialRing, NumberField, QuaternionAlgebra
from sage.all import matrix, vector, diagonal_matrix, pari

out = {"scope": "exact classical baseline and algebra controls only"}
R = PolynomialRing(QQ, "x")
x = R.gen()

# Literal fractional-input failure of Koprowski v2 Algorithm6.
a, b, forbidden, k = QQ(1), QQ(1)/27, QQ(1)/3, 1
value = a + b * QQ(3)**(2*k)
assert 2*k > a.valuation(3) + b.valuation(3)
assert value / forbidden == 4
out["source_fractional_counterexample"] = {
    "value": str(value), "forbidden_class_ratio": str(value / forbidden)}

# The classical rational-form endpoint is already implemented in PARI.
q4 = diagonal_matrix(QQ, [1, -2, -3, 4])
w = vector(QQ, list(pari(q4).qfsolve()))
assert w != 0 and w*q4*w == 0
q5 = diagonal_matrix(QQ, [1, 1, 1, 1, -7])
w5 = vector(QQ, list(pari(q5).qfsolve()))
assert w5 != 0 and w5*q5*w5 == 0
aniso = pari(diagonal_matrix(QQ, [1, 1, -3])).qfsolve()
assert aniso.type() == "t_INT"
out["pari_baseline"] = {"q4_witness": list(map(str,w)),
                        "q5_witness": list(map(str,w5)),
                        "ternary_obstruction": str(aniso)}

# Nontrivial discriminant extension. A supplied zero divisor builds an
# EXACT TEST representation; it is not used as advice to a native solver.
L = NumberField(x*x-6, "t")
t = L.gen()
B = QuaternionAlgebra(L, 2, 3, names=("i","j","k"))
i, j, ij = B.gens()
z = B(1)+i+j+(t/3)*ij
assert z.reduced_norm() == 0 and z != 0
co = lambda v: vector(L, v.coefficient_tuple())
basis = [B(1), i, j, ij]
U = matrix(L, [co(v*z) for v in basis]).row_space()
assert U.dimension() == 2
ub = [B(list(v)) for v in U.basis()]
rho = lambda v: matrix(L, [U.coordinate_vector(co(v*u)) for u in ub]).transpose()
G = matrix(L, [[1,t+1],[t-2,2]])
assert G.det() != 0
rho0 = rho
rho = lambda v: G.inverse()*rho0(v)*G
I, J = rho(i), rho(j)
assert I*I == 2 and J*J == 3 and I*J == -J*I
e1 = vector(L, [1,0])
A = matrix(L, [e1, I*e1, J*e1, (t/3)*(I*J)*e1]).transpose()
sigma = L.hom([-t], L)
As = A.apply_map(sigma)
stacked = A.stack(As)
assert A.rank() == 2 and stacked.rank() == 3
v = stacked.right_kernel().basis()[0]
v = v / next(y for y in v if y != 0)
assert all(sigma(y) == y for y in v)
vv = vector(QQ, list(v))
assert vv*q4*vv == 0 and vv != 0
out["quaternary_descent"] = {"extension": "Q(sqrt(6))",
    "plane_rank": int(A.rank()), "stack_rank": int(stacked.rank()),
    "descended_vector": list(map(str,vv))}

# Forgetting conjugation of the discriminant factor leaves the wrong plane.
L2 = NumberField(x*x-2, "r")
r = L2.gen()
A2 = matrix(L2, [[1,1,0,0],[0,0,1,r]])
correct = A2.stack(A2.apply_map(L2.hom([-r],L2)))
assert correct.rank() == 3 and A2.stack(A2).rank() == 2
out["lost_discriminant_sign"] = {"correct_rank": 3, "wrong_rank": 2}

# Quadratic-decomposition local square oracle, including p=2.
def locally_square_rational(y, p):
    y = QQ(y)
    if y.is_square():
        return True
    E = NumberField(x*x-y, "u")
    return len(E.primes_above(p)) == 2

assert locally_square_rational(13,3) and not QQ(13).is_square()
E = NumberField(x*x-5, "u")
u = E.gen()
omega = (1+u)/2
P = E.primes_above(2)[0]
assert P.ramification_index() == 1 and P.residue_class_degree() == 2
norms = [(1+bb*E(2)**ii).norm() for ii in (1,2) for bb in (E(1),omega)]
assert -1 in norms and not locally_square_rational(-1,2)
assert (2+u).norm() == -1
out["unramified_dyadic_norm"] = {"generator_norms": list(map(str,norms)),
    "selected_pair": ["2","1"], "binary_value": "-1"}

# Ramified dyadic base, unramified quadratic local extension: two residue
# basis elements and four unit-filtration levels (no class enumeration).
K = NumberField(x*x-2, "r")
r = K.gen()
S = PolynomialRing(K, "y")
y = S.gen()
T = K.extension(y*y-5, "s")
s = T.gen()
om = (1+s)/2
unit_generators = [1+bb*T(r)**ii for ii in range(1,5) for bb in (T(1),om)]
relative_norms = [g.norm() for g in unit_generators]
assert K(-1) in relative_norms
Ki = K.extension(y*y+1,"ii").absolute_field("iiabs")
assert len(Ki.primes_above(2)) == 1
out["ramified_dyadic_base"] = {"base": "Q(sqrt(2))",
    "unit_generator_count": len(unit_generators), "contains_nonsquare_norm_minus1": True}

out["claim_gates"] = {name: False for name in (
    "full_solver_execution", "quantum_execution", "classical_separation",
    "novelty", "expanded_output_bound", "asymptotic_inference_from_control")}
Path(__file__).with_suffix(".json").write_text(json.dumps(out,indent=2)+"\n")
print(json.dumps({"status":"passed", "controls":len(out)-2,
                  "artifact":str(Path(__file__).with_suffix('.json'))}))

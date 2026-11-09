"""One exact local Kummer falsifier control; no full/asymptotic algorithm run."""
import json
from pathlib import Path
from collections import Counter
from sage.all import GF, QQ, ZZ, PolynomialRing, NumberField, matrix, vector, prod

# Native split degree-five generic disc above the Weil threshold.
q, d = 10007, 5
k = GF(q)
R = PolynomialRing(k, "z")
z = R.gen()
F = prod(z-i for i in range(d))

def bit(a):
    assert a != 0
    return int(a**((q-1)//2) != 1)

patterns = Counter()
for a in k:
    if F(a) == 0 or bit(F(a)):
        continue
    label = tuple(bit(a-i) for i in range(d))
    assert sum(label) % 2 == 0
    patterns[label] += 1
rank = int(matrix(GF(2), list(patterns)).rank())
valid = sum(patterns.values())
counts = {}
for mask in range(1 << d):
    count = sum(n for v, n in patterns.items()
                if sum(v[i] for i in range(d) if (mask >> i) & 1) % 2)
    counts[str(mask)] = count
positive = [c for c in counts.values() if c]
assert rank == 4 and len(patterns) == 16
assert all(8*c >= q for c in positive)
assert counts["31"] == 0  # R=F: constant zero on valid points.
assert 8*valid >= q       # A negative fixed sign makes that bit always one.
assert min(patterns.values())*8 < q  # Every-pattern density claim is false.
nonsquare = k.multiplicative_generator()
assert all(bit(a*a) == 0 and bit(nonsquare*a*a) == 1 for a in k if a)

# Bad reduction: roots of valuation 1/2, a rootless exceptional child.
S = PolynomialRing(QQ, "X")
X = S.gen()
p = 7
f = (X*X-p)*(X-1)*(X-2)*(X-3)
Delta = int(ZZ(f.discriminant()).valuation(p))
shift = f(p*X)
c = min(int(ZZ(v).valuation(p)) for v in shift if v)
primitive = PolynomialRing(GF(p), "u")([ZZ(v/p**c) for v in shift])
assert c == 1 and primitive.degree() == 0
assert all(ZZ(f(p*j)).valuation(p) == 1 for j in range(p*p))
# x^2-7 is Eisenstein, hence its roots have valuation 1/2, outside 7 Z_7.
assert (X*X-p).is_irreducible()

# Exact norm/Cramer normalization using a genuine integral basis locally at7.
E = NumberField(X*X-p, "a")
a = E.gen()
m = 9
elt = a**m*(3+a)  # The normalized unit has nonsquare residue3 mod7.

def multmat(t):
    return matrix(QQ, [list(t), list(t*a)]).transpose()

M = multmat(a**m)
b = vector(QQ, list(elt))
det = M.det()
out = M.adjugate()*b/det
assert out == vector(QQ, [3, 1])
assert ZZ(elt.norm()).valuation(p) == m
assert ZZ(det).valuation(p) == m
assert not GF(p)(out[0]).is_square()
assert GF(p)(det) == 0  # Ignoring determinant valuation forbids inversion.

result = {
    "scope": "one exact control, not full local-image or quantum execution",
    "generic_disc": {
        "p": q, "degree": d, "valid_residues": valid, "span_rank": rank,
        "patterns": len(patterns), "min_detectable_functional_count": min(positive),
        "min_pattern_count": min(patterns.values()), "functional_counts": counts,
        "norm_square_dependency_caught": True,
        "constant_square_degeneracies_checked": True,
        "false_every_pattern_density_rejected": True},
    "fractional_child": {
        "p": p, "f": str(f), "discriminant_valuation": Delta,
        "child": "7 Z_7", "root_valuations": "1/2", "gauss_parity": c % 2,
        "primitive_reduction": str(primitive),
        "closed_child_root_claim_rejected": True},
    "coordinate_normalization": {
        "field": "Q_7(sqrt7)", "valuation": m,
        "determinant_valuation": int(ZZ(det).valuation(p)),
        "normalized_unit": "3+sqrt7", "unit_square_bit": 1,
        "cramer_exact": True, "unit_inverse_without_loss_rejected": True},
    "general_theorem_inferred": False,
    "full_local_algorithm_executed": False, "quantum_execution": False}
Path(__file__).with_suffix(".json").write_text(json.dumps(result, indent=2)+"\n")
print(json.dumps({"rank": rank, "valid": valid, "min_functional": min(positive),
                  "fractional_child_parity": c % 2, "cramer": True}))

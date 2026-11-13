"""One exact p=43 control for the specified quaternion-field palette.

Run with /opt/anaconda3/envs/qsearch-cas/bin/python.  This is not a prime
sweep and does not infer the all-prime theorem from finite evidence.
"""

import hashlib
import json
from pathlib import Path

from sage.all import GF, NumberField, PolynomialRing, QQ, QuaternionAlgebra, ZZ
from sage.all import gcd, kronecker, matrix, pari, vector


ROOT = Path(__file__).resolve().parents[4]
SOURCE = ROOT / "research/audits/sources/integral_quaternion_selection/page.txt"
p = ZZ(43)
assert p.is_prime() and p % 120 == 43
R = PolynomialRing(QQ, "x")
x = R.gen()
FpX = PolynomialRing(GF(p), "x")

A = QuaternionAlgebra(QQ, 2, 3, names="i,j,k")
i, j, k = A.gens()
assert i * i == 2 and j * j == 3 and i * j == k and j * i == -k
assert (i + j) ** 2 == 5 and (2 * j + k) ** 2 == 6
assert A.discriminant() == 6
local_hilbert = {str(v): int(pari(f"hilbert(2,3,{v})")) for v in (2, 3, 43)}
assert local_hilbert == {"2": -1, "3": -1, "43": 1}

field_records = []
for d in (2, 3, 5, 6):
    K = NumberField(x ** 2 - d, f"a{d}")
    dec = K.primes_above(p)
    ef = sorted((int(P.ramification_index()), int(P.residue_class_degree())) for P in dec)
    expected = [(1, 2)] if d in (2, 3, 5) else [(1, 1), (1, 1)]
    assert ef == expected
    symbol = int(kronecker(d, p))
    assert symbol == (-1 if d in (2, 3, 5) else 1)
    field_records.append({
        "radicand": d,
        "field_discriminant": int(K.discriminant()),
        "kronecker_at_43": symbol,
        "prime_decomposition_ef": ef,
        "factorization_mod_43": [[str(h), int(e)] for h, e in FpX(x ** 2 - d).factor()],
    })

# Dependent-character alternative, embedded in the SAME quaternion algebra.
sqrt6 = 2 * j + k
beta = 7 + sqrt6
assert beta.reduced_norm() == p
assert (7 + sqrt6) * (7 - sqrt6) == p
K6 = NumberField(x ** 2 - 6, "a6b")
assert (7 + K6.gen()).norm() == p
assert kronecker(2, p) * kronecker(3, p) == kronecker(6, p)

# An actual maximal order containing the standard integral quaternion order.
O = A.maximal_order(order_basis=(A(1), i, j, k))
OB = matrix(QQ, [b.coefficient_tuple() for b in O.basis()])
OBinv = OB.inverse()


def coordinates_in_order(z):
    return vector(QQ, z.coefficient_tuple()) * OBinv


beta_coordinates = coordinates_in_order(beta)
assert all(c.denominator() == 1 for c in beta_coordinates)
inverse = beta.conjugate() / p
assert beta * inverse == 1 and inverse * beta == 1
assert all(c.denominator() == 1 for c in coordinates_in_order(p * inverse))
IB = [beta * b for b in O.basis()]
IC = matrix(QQ, [coordinates_in_order(b) for b in IB])
assert all(c.denominator() == 1 for c in IC.list())
assert abs(IC.det()) == p ** 2
norm_content = [b.reduced_norm() for b in IB]
norm_content.extend(
    (IB[r] + IB[s]).reduced_norm() - IB[r].reduced_norm() - IB[s].reduced_norm()
    for r in range(4) for s in range(r + 1, 4)
)
assert all(c.denominator() == 1 for c in norm_content)
norm_ideal_generator = gcd([ZZ(c) for c in norm_content])
assert norm_ideal_generator == p

data = {
    "status": "PASS_exact_single_prime_control_only",
    "execution_note": "Initial invocation passed the field/palette and explicit norm checks, then failed at maximal_order because the cached Sage API requires a tuple, not a list. Corrected that argument and reran the same p=43 control; no parameter scan.",
    "prime": int(p),
    "quaternion_invariants": [2, 3],
    "quaternion_reduced_discriminant": int(A.discriminant()),
    "hilbert_symbols": local_hilbert,
    "original_field_embeddings": [str(i), str(j), str(i + j)],
    "field_records": field_records,
    "fixed_palette_valuation_obstruction": {
        "palette": [2, 3, 5],
        "all_unramified_inert_at_43": True,
        "every_nonzero_field_norm_valuation": "even (including negative valuations)",
        "central_reduced_norm_valuation": "even",
        "arbitrary_ordered_product_norm_valuation": "even by multiplicativity",
        "target_reduced_norm_43_valuation": 1,
    },
    "dependent_palette_limit": {
        "palette": [2, 3, 6],
        "character_identity": "chi_6 = chi_2 * chi_3 away from 2,3",
        "sqrt6_embedding": str(sqrt6),
        "sqrt6_square": str(sqrt6 ** 2),
        "explicit_witness": str(beta),
        "witness_reduced_norm": str(beta.reduced_norm()),
        "field_norm_7_plus_sqrt6": str((7 + K6.gen()).norm()),
        "global_palette_completeness": "NOT CLAIMED",
    },
    "integral_witness_control": {
        "maximal_order_basis": [str(b) for b in O.basis()],
        "order_discriminant": str(O.discriminant()),
        "witness_coordinates": [str(c) for c in beta_coordinates],
        "inverse": str(inverse),
        "43_times_inverse_is_integral": True,
        "principal_right_ideal_basis": [str(b) for b in IB],
        "index_in_order": str(abs(IC.det())),
        "reduced_norm_ideal_generator": str(norm_ideal_generator),
    },
    "scope": "Specified palette only; no all-finite-palette, adaptive-field, norm-one, or ternary-witness no-go.",
    "source_sha256": hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
    "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
}
target = Path(__file__).with_name("result.json")
target.write_text(json.dumps(data, indent=2) + "\n")
print(json.dumps({"status": data["status"], "prime": 43, "result": str(target)}, indent=2))

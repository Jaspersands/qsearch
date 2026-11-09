"""Exact classical control; no quantum circuit or asymptotic inference."""
import json
from pathlib import Path
from sage.all import GF, Matrix, VectorSpace, vector

field = GF(2)
space = VectorSpace(field, 3)
basis = space.basis()
matrix = Matrix(field, [[1, 1, 0], [0, 1, 1], [0, 0, 1]])
assert matrix.is_invertible()
# Recover the advertised linear map from public basis evaluations.
recovered = Matrix(field, [list(matrix * e) for e in basis]).transpose()
assert recovered == matrix
target = vector(field, [1, 1, 1])
optimum = recovered.transpose().solve_right(target)
assert recovered.transpose() * optimum == target
assert all((recovered.transpose() * y).dot_product(z)
           == y.dot_product(recovered * z) for y in space for z in space)

def nonlinear(z):
    return vector(field, [z[0], z[1], z[2] + z[0] * z[1]])

assert len({tuple(nonlinear(z)) for z in space}) == 8
implied_matrix = Matrix(field, [list(nonlinear(e)) for e in basis]).transpose()
y, z = basis[2], basis[0] + basis[1]
left = (implied_matrix.transpose() * y).dot_product(z)
right = y.dot_product(nonlinear(z))
assert left == 0 and right == 1
out = {
    "scope": "One exact invertible-linear control and one nonlinear counterexample",
    "linear_matrix": [[int(a) for a in row] for row in matrix.rows()],
    "recovered_from_basis_queries": recovered == matrix,
    "classical_maximizer": [int(a) for a in optimum],
    "max_score": 3,
    "linear_pairings_checked": 64,
    "toffoli_is_permutation": True,
    "counterexample_y": [int(a) for a in y],
    "counterexample_z": [int(a) for a in z],
    "pairing_left": int(left),
    "pairing_right": int(right),
    "general_theorem_from_control": False,
    "quantum_execution": False,
}
destination = Path(__file__).with_suffix(".json")
destination.write_text(json.dumps(out, indent=2) + "\n")
print(json.dumps(out, separators=(",", ":")))

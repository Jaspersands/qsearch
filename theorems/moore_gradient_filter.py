"""Semantic Moore-form recognition from a public division-free circuit.

This is a classical application falsifier, not a quantum algorithm or a
general polynomial stabilizer solver. Recognition is Monte Carlo; its
ideal-random error bound does not certify a seeded diagnostic run.
"""
from dataclasses import dataclass
from fractions import Fraction
import random

from flint import fq_default_ctx

from theorems.frobenius_circuit_lift import lift_frobenius_circuit
from theorems.polynomial_orbit_module import MooreMinor
from theorems.symbolic_scalar_phase_erasure import _fmpz_solve_coordinates
from theorems.ut5_matrix_phase_alignment import (
    _basis, _canonical, _lists, _matrix, _product, _rank,
)


class CircuitBuilder:
    """Binary arithmetic DAG used to compile falsifier inputs, not hypotheses."""

    def __init__(self, prime):
        self.prime, self.nodes, self.memo = prime, [], {}
        self.zero = self.node(("const", 0))
        self.one = self.node(("const", 1))

    def node(self, entry):
        if entry not in self.memo:
            self.memo[entry] = len(self.nodes)
            self.nodes.append(entry)
        return self.memo[entry]

    def constant(self, value):
        return self.node(("const", value % self.prime))

    def add(self, left, right):
        if left == self.zero:
            return right
        if right == self.zero:
            return left
        return self.node(("add", left, right))

    def mul(self, left, right):
        if self.zero in (left, right):
            return self.zero
        if left == self.one:
            return right
        if right == self.one:
            return left
        return self.node(("mul", left, right))

    def neg(self, value):
        return self.mul(self.constant(-1), value)

    def total(self, values):
        result = self.zero
        for value in values:
            result = self.add(result, value)
        return result

    def power(self, value, exponent):
        if type(exponent) is not int or exponent < 0:
            raise ValueError("nonnegative integer exponent required")
        result = self.one
        while exponent:
            if exponent & 1:
                result = self.mul(result, value)
            exponent >>= 1
            if exponent:
                value = self.mul(value, value)
        return result

    def determinant(self, matrix):
        """Samuelson--Berkowitz recurrence, no division or factorial expansion.

        For [[a,R],[C,M]], the Toeplitz column is
        (1,-a,-RC,-RMC,...); multiply it by charpoly(M).
        The deliberately simple sequential circuit has polynomial size.
        """
        n = len(matrix)
        if any(len(row) != n for row in matrix):
            raise ValueError("square matrix of circuit nodes required")
        coefficients = [self.one]
        for start in range(n-1, -1, -1):
            row = matrix[start][start+1:]
            vector = [matrix[i][start] for i in range(start+1, n)]
            tail = [values[start+1:] for values in matrix[start+1:]]
            column = [self.one, self.neg(matrix[start][start])]
            for power in range(len(row)):
                column.append(self.neg(self.total(self.mul(a, b) for a, b in zip(row, vector))))
                if power+1 < len(row):
                    vector = [self.total(self.mul(a, b) for a, b in zip(values, vector))
                              for values in tail]
            coefficients = [self.total(self.mul(column[i-j], coefficients[j])
                                       for j in range(min(i, len(coefficients)-1)+1))
                            for i in range(len(coefficients)+1)]
        return self.neg(coefficients[-1]) if n % 2 else coefficients[-1]


def moore_circuit(prime, dimension, rows, scalar=1):
    """Compile a known control; the recognizer never receives its row advice."""
    rows = tuple(tuple(row) for row in rows)
    if not rows or type(dimension) is not int or dimension < 1:
        raise ValueError("nonempty row space and positive dimension required")
    for row in rows:
        _canonical(row, dimension, prime)
    if _rank(rows, prime) != len(rows):
        raise ValueError("independent base-field rows required")
    builder = CircuitBuilder(prime)
    variables = [builder.node(("var", i)) for i in range(dimension)]
    current = [builder.total(builder.mul(builder.constant(a), x)
                             for a, x in zip(row, variables)) for row in rows]
    matrix = [current]
    for _ in range(1, len(rows)):
        current = [builder.power(x, prime) for x in current]
        matrix.append(current)
    output = builder.mul(builder.constant(scalar), builder.determinant(matrix))
    return tuple(builder.nodes), output


@dataclass(frozen=True)
class MooreRecognition:
    status: str
    prime: int
    dimension: int
    rows: tuple
    scalar: int | None
    circuit_nodes: int
    formal_degree_bound: int
    extension_degree: int
    gradient_probes: int
    identity_tests: int
    error_bound: Fraction
    randomness: str

    @property
    def accepted(self):
        return self.status == "MOORE_FORM_MONTE_CARLO"

    def matrix_fixes_polynomial(self, matrix):
        """Exact for the recognized form; recognition itself remains probabilistic.

        For arbitrary GL matrices, preserving W is NOT enough: the
        determinant on W must be one. This condition is automatic for
        elements of a promised characteristic-p p-group.
        """
        if not self.accepted:
            raise ValueError("no accepted Moore identity")
        if len(matrix) != self.dimension:
            raise ValueError("square ambient matrix required")
        for row in matrix:
            _canonical(row, self.dimension, self.prime)
        if _rank(matrix, self.prime) != self.dimension:
            raise ValueError("invertible ambient matrix required")
        inverse = _lists(_matrix(matrix, self.prime).inv())
        transformed = _product(self.rows, inverse, self.prime)
        action = [_fmpz_solve_coordinates(self.rows, row, self.prime) for row in transformed]
        return all(row is not None for row in action) and int(_matrix(action, self.prime).det()) == 1


def recognize_moore_form(prime, dimension, nodes, output=None, *,
                         error_budget=Fraction(1, 100), seed=None):
    """Recover and verify F = a det(ell_j(x)^(p^i)) from the circuit alone.

    Only ordinary var/const/add/mul nodes are accepted. Reverse derivatives
    therefore pass THROUGH binary implementations of p-th powers, yielding
    their true zero derivative. There is no Frobenius-root advice.
    FLINT field construction is verified but is not a separately capped
    construction backend. See the accompanying proof for its resource cost.
    """
    if any(not node or node[0] not in ("var", "const", "add", "mul") for node in nodes):
        raise ValueError("ordinary division-free circuit nodes required")
    circuit = lift_frobenius_circuit(prime, dimension, nodes, output)
    if not isinstance(error_budget, Fraction) or not 0 < error_budget < 1:
        raise ValueError("exact error budget in (0,1) required")
    if seed is not None and type(seed) is not int:
        raise ValueError("integer diagnostic seed or None required")
    degree = circuit.degree_bound
    largest_moore_degree = sum(prime**i for i in range(dimension))
    bound = max(degree, largest_moore_degree)
    k, q = 1, prime
    while (dimension+2)*bound*error_budget.denominator > q*error_budget.numerator:
        k, q = k+1, q*prime
    field = fq_default_ctx(prime, k)
    if not field.modulus().is_irreducible():
        raise ArithmeticError("extension modulus failed irreducibility verification")
    rng = random.SystemRandom() if seed is None else random.Random(seed)
    rows, probes, tests = [], 0, 0

    def point():
        return tuple(field([rng.randrange(prime) for _ in range(k)]) for _ in range(dimension))

    def finish(status, scalar=None):
        return MooreRecognition(status, prime, dimension, tuple(map(tuple, rows)), scalar,
                                len(nodes), degree, k, probes, tests,
                                Fraction((dimension+2)*bound, q),
                                "system_random" if seed is None else "seeded_diagnostic")

    for _ in range(dimension):
        _, gradient = circuit.value_and_gradient(point(), field)
        digits = [value.to_list() for value in gradient]
        # Expand over F_p. A span over E would be a different input model.
        vectors = [tuple(int(value[i]) if i < len(value) else 0 for value in digits)
                   for i in range(k)]
        rows = _basis(rows+vectors, prime)
        probes += 1
        if len(rows) == dimension:
            break
    if not rows:
        return finish("NO_NONZERO_GRADIENT")

    moore = MooreMinor(prime, len(rows), tuple(range(len(rows))))

    def candidate(x):
        values = tuple(sum((a*v for a, v in zip(row, x)), field(0)) for row in rows)
        return moore(values, field)

    x = point()
    denominator = candidate(x)
    if denominator.is_zero():
        return finish("ANCHOR_ABORT")
    ratio = circuit.value_and_gradient(x, field)[0]/denominator
    digits = ratio.to_list()
    if ratio.is_zero() or any(int(value) for value in digits[1:]):
        return finish("MOORE_IDENTITY_REJECTED")
    scalar = int(digits[0])
    # The identity and scalar are fixed BEFORE this independent test.
    x = point()
    tests += 1
    if circuit.value_and_gradient(x, field)[0] != scalar*candidate(x):
        return finish("MOORE_IDENTITY_REJECTED")
    return finish("MOORE_FORM_MONTE_CARLO", scalar)


def report():
    examples = []
    for prime, dimension, indices in [(5, 6, (0, 1, 2, 3, 4)),
                                       (43, 50, (0, 10, 20, 30, 40)),
                                       (2**127-1, 6, (0, 3))]:
        rows = [tuple(int(i == j) for j in range(dimension)) for i in indices]
        nodes, output = moore_circuit(prime, dimension, rows)
        result = recognize_moore_form(prime, dimension, nodes, output, seed=29)
        examples.append(dict(prime=prime, dimension=dimension, moore_rank=len(indices),
                             polynomial_degree=sum(prime**i for i in range(len(indices))),
                             circuit_nodes=len(nodes), syntactic_degree_bound=result.formal_degree_bound,
                             status=result.status, recovered_correct_space=result.rows == tuple(rows),
                             extension_degree=result.extension_degree,
                             gradient_probes=result.gradient_probes, identity_tests=result.identity_tests,
                             ideal_random_error_bound=str(result.error_bound),
                             randomness=result.randomness))
    return dict(status="CLASSICAL_RECOGNITION_FILTER_UNDER_REVIEW", examples=examples,
                scalable_family=dict(group="UT_10(F_p)^m, p>9", class_bound=9,
                                     dimension="10*m", moore_rank="m", orbit_rank="10**m",
                                     rank_argument="exact symbolic exterior-coordinate proof, not a fitted exponent",
                                     live_example_m=5, live_example_orbit_rank=10**5),
                public_circuit_required=True, quantum_copies_only_covered=False,
                stabilizer_solver_executed=False, formal_proof_verified=False,
                independently_reviewed=False, novel_algorithm_claimed=False,
                quantum_advantage_claimed=False)


if __name__ == "__main__":
    import argparse
    import json
    from pathlib import Path

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    payload = json.dumps(report(), indent=2)+"\n"
    if args.write:
        path = Path(__file__).resolve().parents[1]/"research/reductions/moore_gradient_filter.json"
        path.write_text(payload)
    print(payload, end="")

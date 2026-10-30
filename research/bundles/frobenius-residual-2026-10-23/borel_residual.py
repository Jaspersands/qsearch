"""Public rank-zero reduction to an existing GL2/SL2 Borel HSP.

Only the embedding and output conversion are implemented. The imported
quantum receiver and the original geometric hiding function are not.
"""

from dataclasses import dataclass
from fractions import Fraction
import sys

from sympy import Matrix, eye, zeros

from residual import (
    ROOT, SmoothPowerRoots, alternating_form, check_prime, column_basis,
    integer_matrix, inverse_mod, mod, nullspace,
)

sys.path.insert(0, str(ROOT / "quadratic-cancellation-2026-10-23"))
from quadratic_cancellation import quadratic_witness


def diagonalize_symmetric(form, prime):
    """Congruence elimination, with no field-element enumeration."""
    form = mod(integer_matrix(form), prime)
    if form.rows != form.cols or form != form.T:
        raise ValueError("symmetric form required")
    n, frame = form.rows, eye(form.rows)
    for k in range(n):
        current = mod(frame.T * form * frame, prime)
        pivot = next((j for j in range(k, n) if current[j, j]), None)
        if pivot is None:
            pair = next(((i, j) for i in range(k, n) for j in range(i + 1, n)
                         if current[i, j]), None)
            if pair is None:
                raise ValueError("nondegenerate form required")
            i, j = pair
            frame[:, i] = mod(frame[:, i] + frame[:, j], prime)
            pivot = i
        frame.col_swap(k, pivot)
        current = mod(frame.T * form * frame, prime)
        denominator = pow(int(current[k, k]), -1, prime)
        for j in range(k + 1, n):
            frame[:, j] = mod(frame[:, j] - int(current[k, j]) * denominator * frame[:, k], prime)
    diagonal = mod(frame.T * form * frame, prime)
    if any(diagonal[i, j] for i in range(n) for j in range(n) if i != j):
        raise ArithmeticError("congruence diagonalization failed")
    return frame, tuple(int(diagonal[i, i]) for i in range(n))


def solve_full_row_rank(matrix, rhs, prime):
    matrix, rhs = integer_matrix(matrix), integer_matrix(rhs)
    pivots, basis = [], zeros(matrix.rows, 0)
    for i in range(matrix.cols):
        extended = basis.row_join(matrix[:, i])
        if column_basis(extended, prime).cols > basis.cols:
            pivots.append(i)
            basis = extended
    if basis.cols != matrix.rows or rhs.shape != (matrix.rows, 1):
        raise ValueError("consistent full-row-rank linear system required")
    values = mod(inverse_mod(basis, prime) * rhs, prime)
    result = zeros(matrix.cols, 1)
    for i, value in zip(pivots, values):
        result[i] = value
    if mod(matrix * result - rhs, prime) != zeros(matrix.rows, 1):
        raise ArithmeticError("linear solve failed")
    return result


@dataclass(frozen=True)
class BorelReduction:
    prime: int
    d: int
    beta: Matrix
    frame: Matrix
    splitting_type: str
    domain: str
    exceptional_planes: tuple
    abort_bound: str
    random_draws: int
    quantum_receiver_executed: bool = False
    geometric_input_verified: bool = False

    def embed(self, element):
        p = self.prime
        element = mod(integer_matrix(element), p)
        if element.shape != (2, 2):
            raise ValueError("two by two group element required")
        determinant = int(element.det()) % p
        if not determinant or (self.domain == "SL2" and determinant != 1):
            raise ValueError("element is outside the reduction domain")
        other = inverse_mod(element, p).T if self.domain == "GL2" else element
        embedded = mod(self.frame * Matrix.diag(element, other) * inverse_mod(self.frame, p), p)
        j = alternating_form(2)
        if mod(embedded.T * j * embedded - j, p) != zeros(4):
            raise ArithmeticError("embedding is not symplectic")
        if mod(embedded * self.beta - self.beta * embedded, p) != zeros(4):
            raise ArithmeticError("embedding does not centralize beta")
        return embedded

    def kernel_from_line(self, line):
        p = self.prime
        line = mod(integer_matrix(line), p)
        if line.shape != (2, 1) or line == zeros(2, 1):
            raise ValueError("nonzero projective line representative required")
        first = self.frame[:, :2] * line
        if self.domain == "GL2":
            annihilator = Matrix([-line[1], line[0]])
            second = self.frame[:, 2:] * annihilator
        else:
            second = self.beta * first
        kernel = mod(first.row_join(second), p)
        if column_basis(kernel, p).cols != 2:
            raise ArithmeticError("output kernel does not have rank two")
        if mod(kernel.T * alternating_form(2) * kernel, p) != zeros(2):
            raise ArithmeticError("output kernel is not Lagrangian")
        if column_basis(kernel.row_join(self.beta * kernel), p).cols != 2:
            raise ArithmeticError("output kernel is not beta stable")
        return kernel

    def restricted_label(self, element, original_hiding_function):
        """One call to the original source, not an invented Borel oracle."""
        return original_hiding_function(self.embed(element))


def build_borel_reduction(beta, ell, characteristic, *, rng=None, security_bits=64):
    check_prime(ell)
    check_prime(characteristic)
    if characteristic <= 3 or characteristic == ell:
        raise ValueError("p>3 distinct from ell required")
    if type(security_bits) is not int or security_bits <= 0:
        raise ValueError("positive integer security bits required")
    beta = mod(integer_matrix(beta), ell)
    d, j = -characteristic % ell, alternating_form(2)
    if beta.shape != (4, 4) or mod(beta * beta - d * eye(4), ell) != zeros(4):
        raise ValueError("four-dimensional beta with beta squared = -p required")
    if mod(beta.T * j + j * beta, ell) != zeros(4):
        raise ValueError("skew-adjoint beta required")
    if pow(d, (ell - 1) // 2, ell) == 1:
        roots = SmoothPowerRoots(ell, 2, rng=rng, attempt_cap=security_bits)
        value = roots.root(d)
        x, y = nullspace(beta - value * eye(4), ell), nullspace(beta + value * eye(4), ell)
        if x.cols != 2 or y.cols != 2:
            raise ArithmeticError("split skew eigenspaces must each have dimension two")
        y = mod(y * inverse_mod(x.T * j * y, ell), ell)
        frame = mod(x.row_join(y), ell)
        form = zeros(4)
        form[:2, 2:], form[2:, :2] = eye(2), -eye(2)
        expected = Matrix.diag(value * eye(2), -value * eye(2))
        kind, domain, exceptions = "split", "GL2", (x, y)
        bound, draws = str(roots.abort_bound), roots.stats.generator_draws
    else:
        diagonalizer, coefficients = diagonalize_symmetric(j * beta, ell)
        witness = quadratic_witness([coefficients], ell, 1, rng=rng,
                                    security_bits=security_bits)
        u = mod(diagonalizer * Matrix(witness.weights), ell)
        equations = (u.T * j).col_join(u.T * j * beta)
        v = solve_full_row_rank(equations, Matrix([1, 0]), ell)
        value = int((v.T * j * beta * v)[0]) % ell
        v = mod(v + value * pow(2 * d, -1, ell) * beta * u, ell)
        frame = mod(Matrix.hstack(u, v, beta * u, beta * v), ell)
        form = Matrix.diag(alternating_form(1), -d * alternating_form(1))
        expected = zeros(4)
        expected[:2, 2:], expected[2:, :2] = d * eye(2), eye(2)
        kind, domain, exceptions = "nonsplit", "SL2", ()
        bound = witness.conditional_abort_bound
        draws = witness.root_counters["generator_draws"]
        if witness.scalar_report is not None:
            scalar_counts = witness.scalar_report["counters"]
            draws += scalar_counts["generator_draws"] + scalar_counts["curve_trials"]
    if not int(frame.det()) % ell:
        raise ArithmeticError("constructed frame is singular")
    if mod(frame.T * j * frame - form, ell) != zeros(4):
        raise ArithmeticError("constructed form identity failed")
    if mod(beta * frame - frame * expected, ell) != zeros(4):
        raise ArithmeticError("constructed beta identity failed")
    if Fraction(bound) > Fraction(1, 2**security_bits):
        raise ArithmeticError("abort bound exceeds declared budget")
    return BorelReduction(ell, d, beta, frame, kind, domain, exceptions, bound, draws)


@dataclass(frozen=True)
class ExceptionalResult:
    kernel: Matrix | None
    original_label_queries: int
    source_hsp_promise_verified: bool = False


def check_exceptional_planes(reduction, original_hiding_function):
    """At most five original calls; exclude split singleton orbits first."""
    if not reduction.exceptional_planes:
        return ExceptionalResult(None, 0)
    reference, calls = original_hiding_function(eye(4)), 1
    for kernel in reduction.exceptional_planes:
        matches = []
        for i in range(2):
            v = kernel[:, i]
            transvection = mod(eye(4) + v * v.T * alternating_form(2), reduction.prime)
            matches.append(original_hiding_function(transvection) == reference)
            calls += 1
        if all(matches):
            return ExceptionalResult(kernel, calls)
    return ExceptionalResult(None, calls)

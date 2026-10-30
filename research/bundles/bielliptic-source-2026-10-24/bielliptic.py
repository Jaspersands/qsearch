"""Discover actual curve maps; classify their conditional source pullbacks.

Curve controls use odd prime fields and supplied, checked split branch
points. Root factoring, extension fields, Jacobian torsion evaluation and
the geometric hiding function are NOT implemented here.
"""

from dataclasses import dataclass
from itertools import permutations
from pathlib import Path
import sys

from sympy import Matrix, Poly, eye, symbols, zeros

ROOT = Path(__file__).resolve().parent.parent
for directory in ("source-pullback-2026-10-23", "frobenius-residual-2026-10-23"):
    sys.path.insert(0, str(ROOT / directory))
from pullback import adjoint, column_basis
from residual import nullspace
from scalar_cancellation import check_prime
from kernel_output import (
    action, alternating_form, check_split, integer_matrix, matrix_multiply,
    matrix_star, mod, product_actions,
)

X, Z = symbols("X Z")


def point_key(point, prime):
    x, z = (int(v) % prime for v in integer_matrix(point))
    if z:
        return (x * pow(z, -1, prime) % prime, 1)
    if x:
        return (1, 0)
    raise ValueError("nonzero projective point required")


def matrix_key(matrix, prime):
    m = mod(integer_matrix(matrix), prime)
    if m.shape != (2, 2) or not int(m.det()) % prime:
        raise ValueError("invertible two by two matrix required")
    first = next(int(v) for v in m if v)
    return tuple(int(v) for v in mod(m * pow(first, -1, prime), prime))


@dataclass(frozen=True)
class SplitSextic:
    prime: int
    coefficients: tuple  # coefficient i multiplies X^i Z^(6-i)

    def __post_init__(self):
        check_prime(self.prime)
        if len(self.coefficients) != 7 or any(type(x) is not int for x in self.coefficients):
            raise ValueError("seven integral sextic coefficients required")
        object.__setattr__(self, "coefficients", tuple(x % self.prime for x in self.coefficients))
        f = Poly(self.expression.subs(Z, 1), X, modulus=self.prime)
        if f.degree() not in (5, 6) or f.gcd(f.diff()).degree() != 0:
            raise ValueError("smooth binary sextic required, including its root at infinity")

    @property
    def expression(self):
        return sum(c * X**i * Z**(6-i) for i, c in enumerate(self.coefficients))

    def value(self, x, z):
        return sum(c * pow(x, i, self.prime) * pow(z, 6-i, self.prime)
                   for i, c in enumerate(self.coefficients)) % self.prime

    @classmethod
    def from_branches(cls, prime, points):
        check_prime(prime)
        points = tuple(point_key(p, prime) for p in points)
        if len(points) != 6 or len(set(points)) != 6:
            raise ValueError("six distinct projective branch points required")
        expression = 1
        for x, z in points:
            expression *= z*X - x*Z
        f = Poly(expression, X, Z, modulus=prime)
        return cls(prime, tuple(int(f.coeff_monomial(X**i * Z**(6-i))) % prime
                                for i in range(7)))


def _triple_frame(triple, prime):
    """Send infinity, zero, one to the ordered distinct triple."""
    p, q, r = (Matrix(point_key(x, prime)) for x in triple)
    frame = p.row_join(q)
    coordinates = mod(frame.inv_mod(prime)*r, prime)
    if not coordinates[0] or not coordinates[1]:
        raise ValueError("three distinct projective points required")
    return mod(frame * Matrix.diag(*coordinates), prime)


@dataclass(frozen=True)
class CurveLift:
    matrix: tuple
    kappa: int
    square_scalar: int
    status: str
    lift_field_degree: int


def classify_involution(curve, matrix):
    """Prove the lift order from the binary form, without guessing y's sign."""
    p = curve.prime
    key = matrix_key(matrix, p)
    m = Matrix(2, 2, key)
    if m == eye(2):
        raise ValueError("nonidentity reduced involution required")
    squared = mod(m*m, p)
    scalar = int(squared[0, 0])
    if not scalar or squared != scalar*eye(2):
        raise ValueError("reduced map does not have order two")
    changed = Poly(curve.expression.subs(
        {X: m[0, 0]*X+m[0, 1]*Z, Z: m[1, 0]*X+m[1, 1]*Z},
        simultaneous=True), X, Z, modulus=p)
    coefficients = tuple(int(changed.coeff_monomial(X**i*Z**(6-i))) % p
                         for i in range(7))
    index = next(i for i, c in enumerate(curve.coefficients) if c)
    kappa = coefficients[index] * pow(curve.coefficients[index], -1, p) % p
    if not kappa or coefficients != tuple(kappa*c % p for c in curve.coefficients):
        raise ValueError("reduced map does not preserve the branch divisor")
    cube = pow(scalar, 3, p)
    if kappa == cube:
        status = "ELLIPTIC_INVOLUTION"
    elif kappa == -cube % p:
        status = "ORDER_FOUR_LIFT_NOT_SELF_ADJOINT"
    else:
        raise ArithmeticError("inconsistent involution lift multiplier")
    degree = 1 if pow(kappa, (p-1)//2, p) == 1 else 2
    return CurveLift(key, kappa, scalar, status, degree)


def discover_involutions(curve, branch_points):
    """120 triple images, independent of field size; no field enumeration."""
    p = curve.prime
    points = tuple(point_key(point, p) for point in branch_points)
    if len(points) != 6 or len(set(points)) != 6:
        raise ValueError("six distinct projective branch points required")
    if any(curve.value(*point) for point in points):
        raise ValueError("supplied branch points do not match the actual curve")
    inverse = _triple_frame(points[:3], p).inv_mod(p)
    found = {}
    for targets in permutations(points, 3):
        m = mod(_triple_frame(targets, p)*inverse, p)
        if {point_key(m*Matrix(point), p) for point in points} != set(points):
            continue
        key = matrix_key(m, p)
        normalized = Matrix(2, 2, key)
        square = mod(normalized*normalized, p)
        if normalized == eye(2) or square != square[0, 0]*eye(2):
            continue
        found[key] = classify_involution(curve, normalized)
    return tuple(found[key] for key in sorted(found))


def curve_point_key(point, prime):
    x, z, y = (int(v) % prime for v in integer_matrix(point))
    if not x and not z:
        raise ValueError("invalid weighted projective curve point")
    scale = pow(z if z else x, -1, prime)
    return (x*scale % prime, z*scale % prime, y*pow(scale, 3, prime) % prime)


def apply_curve_lift(curve, lift, point, y_multiplier):
    """Evaluate on a curve point, NOT on a Mumford encoding with a free basepoint."""
    p = curve.prime
    checked = classify_involution(curve, Matrix(2, 2, lift.matrix))
    if checked != lift:
        raise ValueError("lift metadata does not match the curve")
    if type(y_multiplier) is not int or y_multiplier*y_multiplier % p != lift.kappa:
        raise ValueError("a valid square root in the current field is required")
    x, z, y = curve_point_key(point, p)
    if y*y % p != curve.value(x, z):
        raise ValueError("point is not on the curve")
    m = Matrix(2, 2, lift.matrix)
    return curve_point_key((m[0, 0]*x+m[0, 1]*z, m[1, 0]*x+m[1, 1]*z,
                            y_multiplier*y), p)


def even_elliptic_quotients(curve):
    """Actual quotient equations for y^2=A*x^6+B*x^4+C*x^2+D."""
    d, odd1, c, odd3, b, odd5, a = curve.coefficients
    if odd1 or odd3 or odd5 or not a or not d:
        raise ValueError("smooth even sextic with nonzero endpoints required")
    p = curve.prime
    return ((a*a*d % p, a*c % p, b, 1), (a*d*d % p, b*d % p, c, 1))


def map_even_quotient(curve, point, side):
    """Degree-two curve quotient; None denotes the elliptic point at infinity."""
    even_elliptic_quotients(curve)
    if side not in (0, 1):
        raise ValueError("quotient side must be zero or one")
    p = curve.prime
    x, z, y = curve_point_key(point, p)
    if y*y % p != curve.value(x, z):
        raise ValueError("point is not on the curve")
    denominator, numerator = (z, x) if side == 0 else (x, z)
    if not denominator:
        return None
    scale = curve.coefficients[6 if side == 0 else 0]
    inverse = pow(denominator, -1, p)
    return (scale*numerator*numerator*inverse*inverse % p,
            scale*y*pow(inverse, 3, p) % p)


@dataclass(frozen=True)
class SourceSplit:
    kind: str
    embeddings: Matrix
    polarization_multiplier: int
    smooth_jacobian_target_possible: bool


def source_involution_geometry(order, beta):
    """Classify a Rosati-unitary involution on the GIVEN product polarization."""
    beta = integer_matrix(beta)
    one, zero = order.unit, zeros(4, 1)
    identity = Matrix.vstack(one, zero, zero, one)
    if beta.shape != (16, 1) or matrix_star(order, beta) != beta:
        raise ValueError("integral self-adjoint source map required")
    if matrix_multiply(order, beta, beta) != identity:
        raise ValueError("source involution required")
    a, b, c, d = (beta[4*i:4*i+4, :] for i in range(4))
    if b == c == zero and ((a == one and d == -one) or (a == -one and d == one)):
        embeddings = identity if a == one else Matrix.vstack(zero, one, one, zero)
        return SourceSplit("DIAGONAL_SIGN_PRODUCT_TARGET_ONLY", embeddings, 1, False)
    if a != zero or d != zero or c != order.star(b) or order.multiply(b, c) != one:
        raise ValueError("non-scalar product involution must be a unitary exchange")
    embeddings = Matrix.vstack(one, one, c, -c)
    if matrix_multiply(order, matrix_star(order, embeddings), embeddings) != 2*identity:
        raise ArithmeticError("elliptic source embeddings have incorrect polarization")
    return SourceSplit("UNITARY_EXCHANGE", embeddings, 2, True)


def eigenspace_frame(beta, ell):
    """Known self-adjoint involution -> two symplectic planes, not hidden lines."""
    check_prime(ell)
    beta = mod(integer_matrix(beta), ell)
    if beta.shape != (4, 4) or mod(beta-adjoint(beta), ell) != zeros(4):
        raise ValueError("self-adjoint four dimensional operator required")
    if mod(beta*beta, ell) != eye(4):
        raise ValueError("involution relation required")
    planes = [nullspace(beta-sign*eye(4), ell) for sign in (1, -1)]
    j = alternating_form(2)
    for plane in planes:
        if plane.shape != (4, 2):
            raise ValueError("two dimensional plus and minus eigenspaces required")
        pairing = int((plane[:, 0].T*j*plane[:, 1])[0]) % ell
        if not pairing:
            raise ValueError("nondegenerate eigenspace required")
        plane[:, 1] = mod(plane[:, 1]*pow(pairing, -1, ell), ell)
    frame = mod(Matrix.hstack(*planes), ell)
    if mod(frame.T*j*frame, ell) != mod(j, ell):
        raise ArithmeticError("eigenspace symplectic normalization failed")
    return frame


@dataclass(frozen=True)
class InvolutionResult:
    status: str
    ell: int
    image: Matrix
    beta_coordinates: Matrix
    frame: Matrix
    compatible_lagrangian_count: int
    source_split: SourceSplit | None = None
    geometric_input_verified: bool = False
    quantum_receiver_executed: bool = False


def analyze_pullback(order, ell, splitting, alpha):
    """Exact source-coordinate checks; the original geometric promise remains."""
    check_prime(ell)
    check_split(order, splitting, ell)
    alpha = integer_matrix(alpha)
    if alpha.shape != (16, 1):
        raise ValueError("sixteen source-order coordinates required")
    identity = Matrix.vstack(order.unit, zeros(4, 1), zeros(4, 1), order.unit)
    if matrix_star(order, alpha) != alpha:
        raise ValueError("elliptic-involution pullback must be self-adjoint")
    if matrix_multiply(order, alpha, alpha) != ell*ell*identity:
        raise ValueError("pullback square must equal ell squared")
    if (order.traces*(alpha[:4, :]+alpha[12:, :]))[0] != 0:
        raise ValueError("elliptic-involution pullback must have trace zero")
    actions = product_actions(splitting)
    image = column_basis(action(alpha, actions), ell)
    if image.cols == 2:
        if mod(image.T*alternating_form(2)*image, ell) != zeros(2):
            raise ArithmeticError("image is not isotropic")
        return InvolutionResult("CLASSICAL_KERNEL_UNDER_INPUT_PROMISE", ell, image,
                                zeros(16, 0), zeros(4, 0), 1)
    if image.cols:
        raise ArithmeticError("self-adjoint nilpotent surface image cannot have rank one")
    beta = integer_matrix(alpha/ell)
    frame = eigenspace_frame(action(beta, actions), ell)
    return InvolutionResult("TWO_HIDDEN_LINES_NOT_CLASSICALLY_SOLVED", ell, image,
                            beta, frame, (ell+1)**2, source_involution_geometry(order, beta))


def embed_factors(result, plus, minus):
    """Legal restriction to SL2 x SL2 inside the ORIGINAL Sp4 source."""
    if result.status != "TWO_HIDDEN_LINES_NOT_CLASSICALLY_SOLVED":
        raise ValueError("a residual two-line result is required")
    ell, frame = result.ell, result.frame
    if frame.shape != (4, 4) or mod(frame.T*alternating_form(2)*frame, ell) != mod(alternating_form(2), ell):
        raise ValueError("valid symplectic frame required")
    factors = [mod(integer_matrix(a), ell) for a in (plus, minus)]
    if any(a.shape != (2, 2) or int(a.det()) % ell != 1 for a in factors):
        raise ValueError("each factor must be in SL2; a GL2 extension is not supplied")
    return mod(frame*Matrix.diag(*factors)*frame.inv_mod(ell), ell)


def assemble_kernel(result, plus_line, minus_line):
    """Compose lines returned by a receiver; does not certify those hidden answers."""
    embed_factors(result, eye(2), eye(2))
    ell = result.ell
    lines = [mod(integer_matrix(v), ell) for v in (plus_line, minus_line)]
    if any(v.shape != (2, 1) or v == zeros(2, 1) for v in lines):
        raise ValueError("two nonzero projective line generators required")
    kernel = zeros(4, 2)
    kernel[:2, 0], kernel[2:, 1] = lines
    return mod(result.frame*kernel, ell)

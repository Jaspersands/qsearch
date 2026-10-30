"""Signed genus-one level-four theta conversion over a declared finite field.

Requires full rational 8-torsion and the normalization roots in that field.
The latter are guaranteed after a further degree-four extension, which this
module does not construct. Computes torsion by constant-degree
polynomial root finding, not enumeration of field elements. This is not a
dimension-16 quotient, canonical-label oracle, or quantum implementation.
"""

from dataclasses import dataclass
from itertools import combinations

from flint import fq_default_poly_ctx


def key(value):
    return tuple(int(x) for x in value.to_list())


def point_key(point):
    return () if point is None else tuple(key(x) for x in point)


def matmul(a, b):
    zero = a[0][0]*0
    return [[sum((a[i][k]*b[k][j] for k in range(len(b))), zero)
             for j in range(len(b[0]))] for i in range(len(a))]


def identity(field, n=4):
    return [[field(int(i == j)) for j in range(n)] for i in range(n)]


def scale(matrix, scalar):
    return [[scalar*x for x in row] for row in matrix]


def rref(matrix):
    a = [list(row) for row in matrix]
    rank, pivots = 0, []
    for col in range(len(a[0])):
        pivot = next((i for i in range(rank, len(a)) if a[i][col] != 0), None)
        if pivot is None:
            continue
        a[rank], a[pivot] = a[pivot], a[rank]
        inverse = a[rank][col].inverse()
        a[rank] = [x*inverse for x in a[rank]]
        for i in range(len(a)):
            if i != rank and a[i][col] != 0:
                coefficient = a[i][col]
                a[i] = [x-coefficient*y for x, y in zip(a[i], a[rank])]
        pivots.append(col)
        rank += 1
        if rank == len(a):
            break
    return a, pivots


def nullspace(matrix):
    reduced, pivots = rref(matrix)
    zero = matrix[0][0]*0
    vectors = []
    for free in range(len(matrix[0])):
        if free in pivots:
            continue
        vector = [zero for _ in matrix[0]]
        vector[free] = zero+1
        for row, pivot in enumerate(pivots):
            vector[pivot] = -reduced[row][free]
        vectors.append(vector)
    return vectors


def inverse(matrix):
    n = len(matrix)
    zero = matrix[0][0]*0
    augmented = [list(row)+[zero+int(i == j) for j in range(n)]
                 for i, row in enumerate(matrix)]
    reduced, pivots = rref(augmented)
    if pivots[:n] != list(range(n)):
        raise ValueError("singular coordinate matrix")
    return [row[n:] for row in reduced]


def projective(vector):
    pivot = next((x for x in vector if x != 0), None)
    if pivot is None:
        raise ValueError("zero projective vector")
    return tuple(x/pivot for x in vector)


def apply(matrix, vector):
    return tuple(row[0] for row in matmul(matrix, [[x] for x in vector]))


@dataclass
class EllipticCurve:
    field: object
    a: object
    b: object

    def __post_init__(self):
        if int(self.field.characteristic()) <= 3:
            raise ValueError("characteristic greater than three required")
        self.a, self.b = self.field(self.a), self.field(self.b)
        if 4*self.a**3+27*self.b**2 == 0:
            raise ValueError("singular curve")

    def contains(self, point):
        return point is None or point[1]**2 == point[0]**3+self.a*point[0]+self.b

    def neg(self, point):
        return None if point is None else (point[0], -point[1])

    def add(self, left, right):
        if left is None:
            return right
        if right is None:
            return left
        x, y = left
        u, v = right
        if x == u and y == -v:
            return None
        slope = (3*x*x+self.a)/(2*y) if left == right else (v-y)/(u-x)
        z = slope*slope-x-u
        return z, slope*(x-z)-y

    def multiply(self, scalar, point):
        if scalar < 0:
            return self.multiply(-scalar, self.neg(point))
        result = None
        while scalar:
            if scalar & 1:
                result = self.add(result, point)
            point = self.add(point, point)
            scalar //= 2
        return result

    def quartic(self, point):
        if not self.contains(point):
            raise ValueError("point not on the input curve")
        if point is None:
            return tuple(self.field(x) for x in (0, 0, 0, 1))
        x, y = point
        return self.field.one(), x, y, x*x

    def torsion_eight(self):
        ring = fq_default_poly_ctx(self.field)
        x = ring.gen()
        cubic = x**3+self.a*x+self.b
        two = cubic.roots(multiplicities=False)
        if len(two) != 3:
            raise ValueError("full rational 8-torsion requires full rational 2-torsion")
        numerator = x**4-2*self.a*x*x-8*self.b*x+self.a*self.a
        denominator = 4*cubic
        xs = {key(v): v for v in two}
        root_calls = 1
        for _ in range(2):
            preimages = {key(v): v for v in two}
            for value in xs.values():
                roots = (numerator-value*denominator).roots(multiplicities=False)
                root_calls += 1
                preimages.update((key(v), v) for v in roots)
            xs = preimages
        points = [None]
        for value in sorted(xs.values(), key=key):
            roots = (ring.gen()**2-cubic(value)).roots(multiplicities=False)
            root_calls += 1
            points.extend((value, y) for y in sorted(roots, key=key))
        if len(points) != 64 or any(self.multiply(8, p) is not None for p in points):
            raise ValueError("declared field does not contain full rational 8-torsion")
        return points, {"polynomial_root_calls": root_calls, "maximum_polynomial_degree": 4,
                        "field_elements_enumerated": False, "torsion_points": len(points)}


def translation_matrix(curve, translation, points):
    if translation is None or curve.multiply(4, translation) is not None:
        raise ValueError("nonzero 4-torsion translation required")
    good = [p for p in points if p is not None and p != curve.neg(translation)][:9]
    if len(good) != 9 or len({point_key(p) for p in good}) != 9:
        raise ValueError("nine distinct regular points required")
    equations = []
    for point in good:
        old = curve.quartic(point)
        new = curve.quartic(curve.add(point, translation))
        for i, j in combinations(range(4), 2):
            row = [curve.field.zero() for _ in range(16)]
            for k in range(4):
                row[4*i+k] += new[j]*old[k]
                row[4*j+k] -= new[i]*old[k]
            equations.append(row)
    basis = nullspace(equations)
    if len(basis) != 1:
        raise ArithmeticError("translation has no unique projective linear lift")
    matrix = [basis[0][4*i:4*i+4] for i in range(4)]
    inverse(matrix)
    if not verify_translation(curve, translation, matrix):
        raise ArithmeticError("symbolic translation identity failed")
    # Independent points include the origin and pole of the affine formula.
    for point in points:
        if projective(apply(matrix, curve.quartic(point))) != projective(
                curve.quartic(curve.add(point, translation))):
            raise ArithmeticError("translation identity failed")
    return matrix


def verify_translation(curve, translation, matrix):
    """Exact cross-products in F[x,y]/(y^2-x^3-a*x-b), not point sampling."""
    ring = fq_default_poly_ctx(curve.field)
    x = ring.gen()
    cubic = x**3+curve.a*x+curve.b
    zero, one = ring.zero(), ring.one()

    def plus(left, right):
        return tuple(a+b for a, b in zip(left, right))

    def times(left, right):
        a, b = left
        c, d = right
        return a*c+b*d*cubic, a*d+b*c

    def neg(value):
        return tuple(-v for v in value)

    u, v = translation
    delta = x-u
    line = (-ring(v), one)
    xx = plus(times(line, line), (-((x+u)*delta**2), zero))
    yy = plus((zero, -delta**3), times(line, plus((x*delta**2, zero), neg(xx))))
    target = [(delta**4, zero), times(xx, (delta**2, zero)),
              times(yy, (delta, zero)), times(xx, xx)]
    source = [(one, zero), (x, zero), (zero, one), (x*x, zero)]
    transformed = []
    for row in matrix:
        value = (zero, zero)
        for coefficient, entry in zip(row, source):
            value = plus(value, (coefficient*entry[0], coefficient*entry[1]))
        transformed.append(value)
    return all(times(transformed[i], target[j]) == times(transformed[j], target[i])
               for i, j in combinations(range(4), 2))


def scalar_matrix(matrix):
    value = matrix[0][0]
    if value == 0 or any(matrix[i][j] != (value if i == j else value*0)
                        for i in range(4) for j in range(4)):
        raise ValueError("nonzero scalar matrix required")
    return value


def symmetric_order_four(curve, matrix):
    fourth = matmul(matmul(matrix, matrix), matmul(matrix, matrix))
    value = scalar_matrix(fourth)
    ring = fq_default_poly_ctx(curve.field)
    roots = (ring.gen()**4-value.inverse()).roots(multiplicities=False)
    j = identity(curve.field)
    j[2][2] = -j[2][2]
    for root in sorted(roots, key=key):
        normalized = scale(matrix, root)
        if matmul(matmul(j, normalized), j) == inverse(normalized):
            return normalized
    raise ValueError("symmetric order-four lift needs a compatible constant field extension")


@dataclass
class ThetaConversion:
    curve: EllipticCurve
    coordinates: list
    undo_coordinates: list
    first: tuple
    second: tuple
    root_unity: object
    torsion: list
    resources: dict

    def encode(self, point):
        return projective(apply(self.coordinates, self.curve.quartic(point)))

    def decode(self, vector):
        if len(vector) != 4:
            raise ValueError("four theta coordinates required")
        old = projective(apply(self.undo_coordinates, vector))
        if old[0] == 0:
            if old != self.curve.quartic(None):
                raise ValueError("invalid point at infinity")
            return None
        point = old[1], old[2]
        if old[3] != old[1]**2 or not self.curve.contains(point):
            raise ValueError("point not on the embedded curve")
        return point


def convert(curve):
    points, resources = curve.torsion_eight()
    fourth = sorted({point_key(curve.multiply(2, p)): curve.multiply(2, p)
                     for p in points}.values(), key=point_key)
    first = next(p for p in fourth if curve.multiply(2, p) is not None)
    second = next(p for p in fourth if curve.multiply(2, p) is not None
                  and curve.multiply(2, p) != curve.multiply(2, first))
    a = symmetric_order_four(curve, translation_matrix(curve, first, points))
    b = symmetric_order_four(curve, translation_matrix(curve, second, points))
    commutator = matmul(matmul(matmul(a, b), inverse(a)), inverse(b))
    root = scalar_matrix(commutator)
    if root*root != -curve.field.one():
        raise ArithmeticError("translations do not give a primitive fourth-root commutator")
    eigenspace = nullspace([[a[i][j]-curve.field(int(i == j)) for j in range(4)]
                           for i in range(4)])
    if len(eigenspace) != 1:
        raise ArithmeticError("theta eigenspace is not one dimensional")
    columns = [eigenspace[0]]
    for _ in range(3):
        columns.append(apply(b, columns[-1]))
    undo = [[column[i] for column in columns] for i in range(4)]
    forward = inverse(undo)
    clock = [[curve.field.zero() for _ in range(4)] for _ in range(4)]
    shift = [[curve.field.zero() for _ in range(4)] for _ in range(4)]
    reflection = [[curve.field.zero() for _ in range(4)] for _ in range(4)]
    j = identity(curve.field)
    j[2][2] = -j[2][2]
    for i in range(4):
        clock[i][i] = root**i
        shift[(i+1) % 4][i] = curve.field.one()
        reflection[(-i) % 4][i] = curve.field.one()
    for source, expected in ((a, clock), (b, shift), (j, reflection)):
        if matmul(matmul(forward, source), undo) != expected:
            raise ArithmeticError("symmetric Heisenberg frame verification failed")
    resources = {**resources, "normalization_root_calls": 2,
                 "symbolic_translation_checks": 2, "level": 4,
                 "signed_points_preserved": True}
    result = ThetaConversion(curve, forward, undo, first, second, root, points, resources)
    null = result.encode(None)
    if null[1] != null[3] or 2*null[1]**4 != null[0]*null[2]*(null[0]**2+null[2]**2):
        raise ArithmeticError("level-four elliptic theta-null relation failed")
    for point in points:
        v = result.encode(point)
        coefficient = null[0]**2+null[2]**2
        if (null[1]**2*(v[0]**2+v[2]**2) != coefficient*v[1]*v[3]
                or null[1]**2*(v[1]**2+v[3]**2) != coefficient*v[0]*v[2]):
            raise ArithmeticError("level-four elliptic theta equations failed")
        if result.decode(v) != point:
            raise ArithmeticError("signed point round trip failed")
    return result

"""Public jet alignment for a proposed UT_5(F_p)^r matrix-source reduction.

This is exact classical control algebra, NOT a quantum HSP solver. It receives
neither a hidden subgroup nor coefficients of its potential. The returned
symplectic matrix can be realized by prime_clifford_realization at the
arithmetic-qudit level; qubit compilation and error accounting remain. See
research/UT5_MATRIX_PHASE_ALIGNMENT.md for the source and scope obligations.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

from flint import fmpz_mod_ctx, fmpz_mod_mat

from theorems.prime_character_opi import ring


def _matrix(rows, p):
    return fmpz_mod_mat([list(row) for row in rows], fmpz_mod_ctx(p))


def _lists(matrix):
    return [[int(matrix[i, j]) for j in range(matrix.ncols())]
            for i in range(matrix.nrows())]


def _transpose(rows):
    return [list(row) for row in zip(*rows)]


def _basis(vectors, p):
    if not vectors:
        return []
    reduced, rank = _matrix(vectors, p).rref()
    return _lists(reduced)[:rank]


def _rank(rows, p):
    return len(_basis(rows, p))


def _identity(n):
    return [[int(i == j) for j in range(n)] for i in range(n)]


def _product(left, right, p):
    return _lists(_matrix(left, p) * _matrix(right, p))


def symplectic_pair(left, right, p):
    """[v,w] = z.x' - x.z', in global (x_1..x_R,z_1..z_R) order."""
    if len(left) != len(right) or len(left) % 2:
        raise ValueError("matching even-dimensional vectors required")
    half = len(left) // 2
    return sum(left[half+i]*right[i] - left[i]*right[half+i]
               for i in range(half)) % p


def _canonical(vector, length, p):
    if len(vector) != length or any(type(x) is not int or not 0 <= x < p
                                    for x in vector):
        raise ValueError("canonical public field coordinates required")


@dataclass(frozen=True)
class PublicJetMaps:
    p: int
    factors: int
    quotient_width: int
    active_indices: tuple[int, ...]
    quadratic: tuple[tuple[int, ...], ...]
    linear: tuple[tuple[int, ...], ...]

    @property
    def carrier_width(self):
        return self.factors * len(self.active_indices)

    @property
    def jet_width(self):
        return 2*self.factors*(self.quotient_width + 1)


def public_jet_maps(p, labels, scales, outcomes):
    """Build K and J from public data; verify quartic cancellation and rank.

    W coordinates are (b_1..b_r,a_1..a_r). For an unknown common quadratic
    Q: F_p^m -> W, stacked displacements have quadratic part K Q_2(q)
    and linear part J T q, T=(Q_1, Hessian rows of Q). Zero-scale input
    packets are consumed and excluded, never recycled.
    """
    ring(p)
    if p <= 4 or not labels or not labels[0] or not outcomes or not outcomes[0]:
        raise ValueError("p>4 and positive source dimensions required")
    if len(labels) != len(scales) or len(labels) != len(outcomes):
        raise ValueError("one scale and outcome per source required")
    r, m = len(labels[0]), len(outcomes[0])
    _canonical(scales, len(labels), p)
    for label, outcome in zip(labels, outcomes):
        _canonical(label, r, p)
        _canonical(outcome, m, p)
        if not all(label):
            raise ValueError("every Heisenberg central label must be nonzero")
    active = tuple(i for i, scale in enumerate(scales) if scale)
    if not active:
        raise ValueError("at least one active source required")
    if any(sum(pow(s, 4, p)*label[j] for label, s in zip(labels, scales)) % p
           for j in range(r)):
        raise ValueError("quartic central-label cancellation failed")
    R, w = r*len(active), 2*r
    K = [[0]*w for _ in range(2*R)]
    J = [[0]*(w*(m+1)) for _ in range(2*R)]
    for block, source in enumerate(active):
        s, label, y = scales[source], labels[source], outcomes[source]
        for coordinate in range(w):
            local = coordinate % r
            row = block*r + local + (R if coordinate >= r else 0)
            factor = label[local] if coordinate >= r else 1
            K[row][coordinate] = s*s*factor % p
            for jet, coefficient in enumerate([1] + list(y)):
                J[row][jet*w+coordinate] = s*factor*coefficient % p
    if _rank([a+b for a, b in zip(K, J)], p) != w*(m+2):
        raise ValueError("public jet design is rank deficient")
    return PublicJetMaps(p, r, m, active, tuple(map(tuple, K)), tuple(map(tuple, J)))


def _orthogonal_basis(vectors, width, p):
    half = width//2
    rows = _basis([v[half:]+[-x % p for x in v[:half]] for v in vectors], p)
    pivots = [next(i for i, x in enumerate(row) if x) for row in rows]
    result = []
    for free in range(width):
        if free in pivots:
            continue
        vector = [int(i == free) for i in range(width)]
        for pivot, row in zip(pivots, rows):
            vector[pivot] = -row[free] % p
        result.append(vector)
    return result


def extend_symplectic_isometry(p, source, target):
    """Deterministic Witt extension of independent, equal-Gram vector lists.

    Returns (matrix, transvection_count). No field enumeration or random
    trials; at most two transvections per supplied vector. This is public
    finite-field algebra, not a Clifford circuit or a new Witt theorem.
    """
    ring(p)
    if p == 2 or not source or len(source) != len(target):
        raise ValueError("odd prime and matching nonempty vector lists required")
    width = len(source[0])
    if width == 0 or width % 2:
        raise ValueError("positive even ambient width required")
    for vector in list(source)+list(target):
        _canonical(vector, width, p)
    if _rank(source, p) != len(source) or _rank(target, p) != len(target):
        raise ValueError("independent source and target lists required")
    if any(symplectic_pair(a, b, p) != symplectic_pair(c, d, p)
           for a, c in zip(source, target) for b, d in zip(source, target)):
        raise ValueError("matching alternating Gram matrices required")
    source, target = [list(v) for v in source], [list(v) for v in target]
    S, count = _matrix(_identity(width), p), 0

    def move(u, v):
        nonlocal S, count
        inverse = pow(symplectic_pair(u, v, p), -1, p)
        difference = [(a-b) % p for a, b in zip(u, v)]
        # T(x)=x+[x,u-v]*(u-v)/[u,v]; form T*S by a rank-one update.
        covector = [-x % p for x in difference[width//2:]]+difference[:width//2]
        S = S + _matrix([[inverse*x % p] for x in difference], p)*(_matrix([covector], p)*S)
        count += 1

    for index, (original, wanted) in enumerate(zip(source, target)):
        current = [row[0] for row in _lists(S*_matrix([[x] for x in original], p))]
        if current == wanted:
            continue
        if symplectic_pair(current, wanted, p):
            move(current, wanted)
            continue
        complement = _orthogonal_basis(target[:index], width, p)
        direction = next(v for v in complement if symplectic_pair(current, v, p))
        if not symplectic_pair(wanted, direction, p):
            other = next(v for v in complement if symplectic_pair(wanted, v, p))
            direction = (other if symplectic_pair(current, other, p)
                         else [(x+y) % p for x, y in zip(direction, other)])
        middle = [(x+y) % p for x, y in zip(current, direction)]
        move(current, middle)
        move(middle, wanted)
    return tuple(map(tuple, _lists(S))), count


class JetMaps(Protocol):
    p: int
    quadratic: tuple[tuple[int, ...], ...]
    linear: tuple[tuple[int, ...], ...]

    @property
    def carrier_width(self) -> int: ...

    @property
    def jet_width(self) -> int: ...


@dataclass(frozen=True)
class JetAlignment:
    maps: JetMaps
    symplectic: tuple[tuple[int, ...], ...]
    transvections: int


def verify_alignment(alignment):
    """Check the output identities, including canonical rather than varying jets."""
    maps = alignment.maps
    p, R, D = maps.p, maps.carrier_width, maps.jet_width
    S = alignment.symplectic
    if len(S) != 2*R:
        return False
    try:
        for row in S:
            _canonical(row, 2*R, p)
    except ValueError:
        return False
    form = [[0]*(2*R) for _ in range(2*R)]
    for i in range(R):
        form[i][R+i], form[R+i][i] = p-1, 1
    if _product(_product(_transpose(S), form, p), S, p) != form:
        return False
    if any(any(row) for row in _product(S, maps.quadratic, p)[:R]):
        return False
    expected = [[int(i == j) for j in range(D)] for i in range(R)]
    return _product(S, maps.linear, p)[:R] == expected


def align_public_jets(p, labels, scales, outcomes):
    """Canonicalize unknown linear jets while killing quadratic X displacement.

    Deterministically returns S with (SK)_X=0 and (SJ)_X=(I_D,0)^T
    for a verified rank/isotropy design and R>=D+w. All inputs are public.
    """
    maps = public_jet_maps(p, labels, scales, outcomes)
    return align_jet_maps(maps)


def align_jet_maps(maps: JetMaps):
    """Shared checked geometry; the noncentral width need not be even."""
    p, R, D = maps.p, maps.carrier_width, maps.jet_width
    ring(p)
    if not maps.quadratic or not maps.quadratic[0] or D < 1:
        raise ValueError("positive public map dimensions required")
    w = len(maps.quadratic[0])
    if len(maps.quadratic) != 2*R or len(maps.linear) != 2*R:
        raise ValueError("matching public map row dimensions required")
    for row in maps.quadratic:
        _canonical(row, w, p)
    for row in maps.linear:
        _canonical(row, D, p)
    columns = _transpose(maps.quadratic)
    if any(symplectic_pair(a, b, p) for a in columns for b in columns):
        raise ValueError("quadratic image must be isotropic")
    if _rank([list(a)+list(b) for a, b in zip(maps.quadratic, maps.linear)], p) != w+D:
        raise ValueError("public jet design is rank deficient")
    if R < D + w:
        raise ValueError("insufficient carrier width for the explicit target embedding")
    linear = _transpose(maps.linear)
    target = []
    for index, vector in enumerate(columns):
        image = [0]*(2*R)
        image[R:R+D] = [symplectic_pair(vector, v, p) for v in linear]
        image[R+D+index] = 1
        target.append(image)
    half = pow(2, -1, p)
    for index, vector in enumerate(linear):
        image = [0]*(2*R)
        image[index] = 1
        image[R:R+D] = [half*symplectic_pair(vector, v, p) % p for v in linear]
        target.append(image)
    S, count = extend_symplectic_isometry(p, columns+linear, target)
    alignment = JetAlignment(maps, S, count)
    if not verify_alignment(alignment):
        raise ArithmeticError("public symplectic jet alignment failed verification")
    return alignment

"""Public SL4 -> SO6 oracle pullback and flag conversion, prime fields only.

This implements the reduction, NOT the imported quantum parabolic solver.
Decoding a supplied singular space is an algebraic control, not a hidden
subspace learner. No hidden space enters the oracle wrapper.
"""

from itertools import combinations
from pathlib import Path
import sys

from flint import fmpz_mat

sys.path.insert(0, str(Path(__file__).resolve().parent.parent /
                       "orthogonal-three-probe-2026-10-23"))
import orthogonal_probe as op

# Coordinates are e12,e13,e14,e34,-e24,e23; Pfaffian is x.y.
PAIRS = ((0, 1), (0, 2), (0, 3), (2, 3), (1, 3), (1, 2))
SIGNS = (1, 1, 1, 1, -1, 1)


def wedge(u, v, p):
    if len(u) != 4 or len(v) != 4:
        raise ValueError("four-dimensional vectors required")
    return tuple(s*(u[i]*v[j]-u[j]*v[i]) % p for (i, j), s in zip(PAIRS, SIGNS))


def exterior_square(g, p):
    op.make_probe(op.eye(6)[0], p)
    if len(g) != 4 or any(len(row) != 4 for row in g):
        raise ValueError("4 by 4 matrix required")
    if int(fmpz_mat(g).det()) % p != 1:
        raise ValueError("SL4 input required; GL4 oracle access is NOT granted")
    columns = op.transpose(g)
    result = op.transpose(tuple(op.scale(s, wedge(columns[i], columns[j], p), p)
                                for (i, j), s in zip(PAIRS, SIGNS)))
    if not op.is_orthogonal(result, p) or int(fmpz_mat(result).det()) % p != 1:
        raise ArithmeticError("exterior-square isometry check failed")
    return result


class PullbackOracle:
    """One original SO6/O6 query per legal SL4 query; no hidden-data input."""

    def __init__(self, original_oracle, p):
        op.make_probe(op.eye(6)[0], p)
        self.original_oracle, self.p, self.calls = original_oracle, p, 0

    def __call__(self, g):
        image = exterior_square(g, self.p)
        label = self.original_oracle(image)
        self.calls += 1
        return label


def flag_to_singular(flag, p):
    """Postprocess the flag returned by the imported SL4 solver."""
    flag = tuple(op.basis(space, p) for space in flag)
    if any(any(len(v) != 4 for v in space) for space in flag):
        raise ValueError("flag vectors must have width four")
    dimensions = tuple(len(space) for space in flag)
    if dimensions == (2,):
        return op.basis((wedge(*flag[0], p),), p)
    if dimensions == (1,):
        return op.basis(tuple(wedge(flag[0][0], v, p) for v in op.eye(4)), p)
    if dimensions == (3,):
        return op.basis(tuple(wedge(v, w, p) for v, w in combinations(flag[0], 2)), p)
    if dimensions == (1, 3) and len(op.basis(flag[0]+flag[1], p)) == 3:
        return op.basis(tuple(wedge(flag[0][0], v, p) for v in flag[1]), p)
    raise ValueError("allowed flag types are (2), (1,3), (1), (3)")


def bivector_support(v, p):
    if len(v) != 6:
        raise ValueError("six-dimensional bivector required")
    a = [[0]*4 for _ in range(4)]
    for value, (i, j), sign in zip(v, PAIRS, SIGNS):
        a[i][j], a[j][i] = sign*value % p, -sign*value % p
    return op.basis(op.transpose(a), p)


def supplied_space_to_flag(space, p):
    """Control inverse only. Calling this on a secret would be hidden advice."""
    space = op.basis(space, p)
    if not 1 <= len(space) <= 3 or any(len(v) != 6 for v in space):
        raise ValueError("nonzero singular space of rank at most three required")
    if any(op.quadratic(v, p) for v in space) or any(op.polar(v, w, p) for v in space for w in space):
        raise ValueError("totally singular space required")
    supports = tuple(bivector_support(v, p) for v in space)
    common = supports[0]
    for support in supports[1:]:
        common = op.intersection(common, support, 4, p)
    total = op.basis(tuple(v for support in supports for v in support), p)
    if len(space) == 1:
        flag = (total,)
    elif len(space) == 2:
        flag = (common, total)
    elif len(common) == 1:
        flag = (common,)
    else:
        flag = (total,)
    if flag_to_singular(flag, p) != space:
        raise ArithmeticError("Klein correspondence inversion failed")
    return flag


def image_flag(g, flag, p):
    return tuple(op.image(g, space, p) for space in flag)

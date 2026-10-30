"""Equality-only meet-in-the-middle baseline for rank-two Siegel HSP.

Input is the SAME legal Sp_4(F_p) left-coset oracle as the proposed source.
The solver never receives the hidden plane or coefficients from its labels.
It is exponential in log p, not a dequantization to polynomial bit time.
"""

from math import isqrt
from pathlib import Path
import sys

from sympy import Matrix, eye, isprime, zeros

sys.path.insert(0, str(Path(__file__).resolve().parent.parent/"prime-square-flags-2026-10-23"))
from prime_square_flags import mod, nullspace, symplectic_form


def inverse(matrix, p):
    return mod(Matrix(matrix).inv_mod(p), p)


def uniform_symplectic(p, rng):
    j, space, columns = symplectic_form(2), eye(4), []
    while space.cols:
        while True:
            coefficients = Matrix([rng.randrange(p) for _ in range(space.cols)])
            if any(coefficients):
                break
        v = mod(space*coefficients, p)
        constraint = mod(v.T*j*space, p)
        pivot = next(i for i in range(space.cols) if constraint[i])
        coordinates = [rng.randrange(p) if i != pivot else 0 for i in range(space.cols)]
        coordinates[pivot] = ((1-sum(int(constraint[i])*coordinates[i] for i in range(space.cols)))
                              *pow(int(constraint[pivot]), -1, p)) % p
        w = mod(space*Matrix(coordinates), p)
        columns.extend((v, w))
        space = mod(space*nullspace((v.T*j*space).col_join(w.T*j*space), p), p)
    result = Matrix.hstack(*columns)
    if mod(result.T*j*result-j, p) != zeros(4):
        raise AssertionError("symplectic basis sampling failed")
    return result


def translation(t):
    return Matrix([[1, t], [0, 1]])


def levi(a, p):
    a = mod(a, p)
    out, dual = zeros(4), inverse(a, p).T
    for i in range(2):
        for j in range(2):
            out[2*i, 2*j] = a[i, j]
            out[2*i+1, 2*j+1] = dual[i, j]
    return out


def embed_plane(a, index):
    out = eye(4)
    out[2*index:2*index+2, 2*index:2*index+2] = a
    return out


def difference_sets(p):
    m = isqrt(p)
    if m*m < p:
        m += 1
    return range(m), tuple(m*j % p for j in range((p+m-1)//m))


def cross_collision(left, right, p):
    aa, bb = difference_sets(p)
    table = {}
    for a in aa:
        table.setdefault(left(a), a)
    for b in bb:
        label = right(b)
        if label in table:
            return table[label], b
    return None


def eigenspace_frame(involution, p):
    j, columns = symplectic_form(2), []
    for sign in (-1, 1):
        space = nullspace(involution-sign*eye(4), p)
        if space.cols != 2:
            raise AssertionError("expected two symplectic eigenplanes")
        v, w = space[:, 0], space[:, 1]
        pairing = int((v.T*j*w)[0]) % p
        if not pairing:
            raise AssertionError("degenerate eigenplane")
        columns.extend((v, mod(w*pow(pairing, -1, p), p)))
    frame = Matrix.hstack(*columns)
    if mod(frame.T*j*frame-j, p) != zeros(4):
        raise AssertionError("eigenplane frame is not symplectic")
    return frame


def covering_frames(p):
    """Four coordinate graph charts, each with shifts c -> c and c -> c+1."""
    rotation = Matrix([[0, -1], [1, 0]])
    frames = []
    for first in (False, True):
        for second in (False, True):
            c = embed_plane(rotation if first else eye(2), 0)*embed_plane(rotation if second else eye(2), 1)
            for shift in (0, 1):
                frames.append(mod(c*embed_plane(translation(-shift), 1), p))
    return tuple(frames)


def recover_line(query, identity_label, plane, p):
    def call(a):
        return query(embed_plane(a, plane))
    if call(translation(1)) == identity_label:
        return Matrix([1, 0])
    if p == 3:
        j = symplectic_form(1)
        for z in range(p):
            v = Matrix([z, 1])
            if call(eye(2)+v*v.T*j) == identity_label:
                return v
        raise AssertionError("valid split-line oracle must reveal one line")
    scale = Matrix.diag(2, pow(2, -1, p))
    collision = cross_collision(lambda a: call(translation(a)),
                                lambda b: call(translation(b)*scale), p)
    if collision is None:
        raise AssertionError("finite-line difference cover has no collision")
    a, b = collision
    z = (a-b)*pow(3, -1, p) % p
    return Matrix([z, 1])


def recover(oracle, p, *, chart_budget=8):
    if not isprime(p) or p == 2 or not 1 <= chart_budget <= 8:
        raise ValueError("odd prime and chart budget between one and eight required")
    calls, j = 0, symplectic_form(2)
    def query(matrix):
        nonlocal calls
        matrix = mod(matrix, p)
        if matrix.shape != (4, 4) or mod(matrix.T*j*matrix-j, p) != zeros(4):
            raise ValueError("every oracle query must be in Sp_4")
        calls += 1
        label = oracle(matrix)
        hash(label)
        return label
    identity_label = query(eye(4))
    reflection = Matrix.diag(-1, 1)
    aa, bb = difference_sets(p)
    block_budget = len(aa)+len(bb)
    bound = chart_budget*block_budget+2*max(block_budget+1, 4)+3
    for attempt, c in enumerate(covering_frames(p)[:chart_budget], 1):
        c_inverse = inverse(c, p)
        def chart_query(matrix):
            return query(c*matrix*c_inverse)
        collision = cross_collision(lambda a: chart_query(levi(translation(a), p)),
                                    lambda b: chart_query(levi(translation(b)*reflection, p)), p)
        if collision is None:
            continue
        a, b = collision
        involution = mod(c*levi(translation(b-a)*reflection, p)*c_inverse, p)
        frame = eigenspace_frame(involution, p)
        frame_inverse = inverse(frame, p)
        def split_query(matrix):
            return query(frame*matrix*frame_inverse)
        lines = [recover_line(split_query, identity_label, plane, p) for plane in range(2)]
        coordinate_basis = zeros(4, 2)
        for plane, line in enumerate(lines):
            coordinate_basis[2*plane:2*plane+2, plane] = line
        recovered = mod(frame*coordinate_basis, p)
        for i in range(2):
            v = recovered[:, i]
            if query(eye(4)+v*v.T*j) != identity_label:
                raise AssertionError("final transvection certificate failed")
        if calls > bound:
            raise AssertionError("query budget violated")
        return {"status": "RECOVERED_UNDER_ORACLE_PROMISE", "basis": recovered,
                "queries": calls, "query_bound": bound, "charts_tried": attempt,
                "full_cover_budget": chart_budget == 8}
    if calls > bound:
        raise AssertionError("query budget violated")
    return {"status": "ABORT", "basis": None, "queries": calls,
            "query_bound": bound, "charts_tried": chart_budget,
            "full_cover_budget": chart_budget == 8}

"""Exact local-order controls, not native curve recovery or a new oracle task.

Frames and target orders in these tests are supplied. Native use would need
charged local-to-global lifting and actual endomorphism division.
"""

from sympy import Matrix, Rational, eye, isprime


def prime(q):
    if type(q) is not int or not isprime(q):
        raise ValueError("prime local level required")


def rational_matrix(value):
    value = Matrix(value)
    if value.shape != (2, 2) or any(x.is_Rational is not True for x in value):
        raise ValueError("exact rational 2 by 2 matrix required")
    return value


def units():
    return tuple(Matrix(2, 2, [int(i == j) for i in range(4)]) for j in range(4))


def local_integral(value, q):
    prime(q)
    return all(x.q % q != 0 for x in rational_matrix(value))


def contains(frame, value, q):
    """Membership in the SUPPLIED End(frame Z_q^2)."""
    frame, value = rational_matrix(frame), rational_matrix(value)
    if frame.det() == 0:
        raise ValueError("nonsingular lattice frame required")
    return local_integral(frame.inv()*value*frame, q)


def neighbor_frames(q):
    """Enumerative O(q) arithmetic control; never a poly(log q) algorithm."""
    prime(q)
    return tuple(Matrix([[1, 0], [t, q]]) for t in range(q)) + (Matrix.diag(q, 1),)


def scalar_order_basis(q):
    prime(q)
    e11, e12, e21, _ = units()
    return (eye(2), q*e11, q*e12, q*e21)


def path_intersection_basis(q, lo, hi):
    prime(q)
    if type(lo) is not int or type(hi) is not int or not 0 <= lo <= hi:
        raise ValueError("ordered nonnegative path endpoints required")
    e11, e12, e21, e22 = units()
    return (e11, Rational(1, q**lo)*e12, q**hi*e21, e22)


def recover_path_vertex(q, length, membership):
    """Known Eichler-path binary selection; callback is NOT a native backend.

    A real callback must test the globally lifted basis, not just its local
    matrix. UNKNOWN/timeout must not be treated as a negative observation.
    """
    prime(q)
    if type(length) is not int or length < 0:
        raise ValueError("nonnegative path length required")
    lo, hi, calls = 0, length, 0
    while lo < hi:
        mid = (lo+hi)//2
        answers = []
        for value in path_intersection_basis(q, lo, mid):
            answer = membership(value)
            calls += 1
            if type(answer) is not bool:
                raise ValueError("membership must be exact bool, not UNKNOWN")
            answers.append(answer)
        if all(answers):
            hi = mid
        else:
            lo = mid+1
    return {"vertex": lo, "membership_calls": calls,
            "native_recovery_executed": False}


def residue(value, q):
    if not local_integral(value, q):
        raise ValueError("matrix not integral at the local prime")
    return rational_matrix(value).applyfunc(
        lambda x: int(x.p)*pow(int(x.q), -1, q) % q)


def invariant_lines(value, q):
    reduced = residue(value, q)
    lines = tuple(Matrix([1, t]) for t in range(q)) + (Matrix([0, 1]),)
    return tuple(i for i, v in enumerate(lines)
                 if int(Matrix.hstack(v, reduced*v).det()) % q == 0)

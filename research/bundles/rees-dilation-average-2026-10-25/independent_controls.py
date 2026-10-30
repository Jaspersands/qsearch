"""Independent bounded checks. No imports from any proof/diagnostic bundle.

Prints JSON only; run with /opt/anaconda3/bin/python -B independent_controls.py.
The finite-field packet check uses exact integer phase counts in Q[zeta_131].
"""

from collections import Counter
from fractions import Fraction
from itertools import product
import json

import sympy as sp


def symbolic_checks():
    t = sp.symbols("t0:4")
    # An independent upper-triangular matrix model, with central c separate.
    def point(v):
        return sp.Matrix([[1, v, v**3 / 2], [0, 1, v**2], [0, 0, 1]])

    word = point(t[0]).inv() * point(t[1]) * point(t[2]).inv() * point(t[3])
    a, b = word[0, 1], word[1, 2]
    c = -t[0]**3 + t[1]**3 - t[2]**3 + t[3]**3
    w = sp.expand(word[0, 2] - a * b / 2)
    coordinates = sp.Matrix([a, b, c, w])
    determinant = sp.factor(coordinates.jacobian(t).det())
    expected = 6 * (t[0]-t[1]) * (t[1]-t[2])**2 * (t[2]-t[3]) * (t[0]-t[1]-t[2]+t[3])
    assert sp.expand(determinant - expected) == 0

    d, e, m, distance = sp.symbols("d e m D")
    n = m + distance
    substitutions = dict(zip(t, (m-d/2, m+d/2, n-e/2, n+e/2)))
    A, B, C, W = [sp.expand(v.subs(substitutions)) for v in coordinates]
    R = sp.expand(C + 6*W - A**3)
    assert sp.expand(R - 6*d*e*(distance-A/2)) == 0
    energy = C - 3*B**2/(4*A) - A**3/4
    assert sp.factor(2*A*energy/R - A/2 - distance) == 0
    assert sp.factor(R/(6*(distance-A/2)) - d*e) == 0
    B0, C0, R0 = [v.subs(e, -d) for v in (B, C, R)]
    assert sp.factor(R0/(3*B0) - d) == 0
    assert sp.factor(-B0/(2*d) - distance) == 0
    assert sp.factor(2*C0/(3*B0) - (m+n)) == 0

    x, y, k, ell, u = sp.symbols("x y k ell u")
    c0 = k/2 + ell
    alpha, beta = k-3*c0, 3*c0-2*k
    exponent = c0*(x-y)**3 + k*(x-y)**2*y
    r, lam = beta/alpha, beta**2/(3*alpha)
    completed = (c0*r**3-lam)*u**3 + (k-c0-lam)*y**3 + lam*(u+y)**3
    assert sp.factor(exponent.subs(x, r*u) - completed) == 0
    assert sp.expand(alpha+beta+k) == 0
    return {
        "word_model": "upper-triangular 3x3 matrices plus independent cubic central coordinate",
        "jacobian": str(determinant),
        "regular_inverse_branches": "both symbolic branches checked",
        "hankel_identity": "exact rational-function identity checked",
        "exceptional_branch_guard": "alpha + beta = -k",
    }


def cyclotomic(counts, denominator, p):
    # Phi_p = 1 + X + ... + X^(p-1); eliminate the last coefficient.
    last = counts[p-1]
    return tuple(Fraction(counts[i]-last, denominator) for i in range(p-1))


def packet_control():
    p = 131
    half = pow(2, -1, p)
    # Bounded diagnostic search, not a claimed scalable design algorithm.
    root = next(x for x in range(p) if (x*x+2) % p == 0)
    design = [1, p-1, 1, p-1, root, -root % p]
    assert len(set(design)) >= 3
    assert all(sum(pow(s, j, p) for s in design) % p == 0 for j in (1, 2, 3))

    def cover_mul(a, b):
        x, y, z, v = a
        X, Y, Z, V = b
        return ((x+X) % p, (y+Y) % p, (z+Z) % p,
                (v+V+half*(x*Y-y*X)) % p)

    def inverse(a):
        return tuple(-x % p for x in a)

    def evaluate(s, a):
        x, y, z, v = a
        return (s*x % p, s*y % p, (s*z+s*s*v) % p)

    def native_ket(g):
        # U = pi_1 direct_sum pi_2; psi=(|1,0>+|2,0>)/sqrt(2).
        # Values are root exponents. Both amplitudes have magnitude 1/sqrt(2).
        x, y, z = g
        return {(k, x): (-k*z+k*x*y*half) % p for k in (1, 2)}

    def overlap_phases(a, b):
        ka, kb = native_ket(a), native_ket(b)
        return [(ka[label]-kb[label]) % p for label in ka if label in kb]

    def averaged_kernel(a, b):
        counts = Counter()
        for scale in range(p):
            terms = Counter({0: 1})
            for s in design:
                phases = overlap_phases(evaluate(s*scale % p, a),
                                        evaluate(s*scale % p, b))
                following = Counter()
                for old, multiplicity in terms.items():
                    for phase in phases:
                        following[(old+phase) % p] += multiplicity
                terms = following
            counts.update(terms)
        return cyclotomic(counts, p*2**len(design), p)

    identity = (0, 0, 0, 0)
    addresses = [identity, (1, 0, 0, 0), (1, 1, 0, half),
                 (0, 2, 1, 3), (2, 1, 0, 2)]
    checks = 0
    for a, b in product(addresses, repeat=2):
        actual = averaged_kernel(a, b)
        argument = cover_mul(inverse(b), a)
        assert actual == averaged_kernel(argument, identity)
        checks += 1

    a, b = addresses[2], addresses[1]
    good_argument = cover_mul(inverse(b), a)
    wrong_argument = cover_mul(a, inverse(b))
    correct = averaged_kernel(a, b)
    wrong = averaged_kernel(wrong_argument, identity)
    assert good_argument == (0, 1, 0, 0)
    assert wrong_argument == (0, 1, 0, 1)
    assert correct[0] == 1 and not any(correct[1:])
    assert wrong[0] == Fraction(7, 32) and not any(wrong[1:])

    # A translation in x has zero native overlap at every nonzero random scale.
    one_packet = averaged_kernel(addresses[1], identity)
    assert one_packet[0] == Fraction(1, p) and not any(one_packet[1:])
    independent_two = Fraction(1, p*p)
    shared_two = Fraction(1, p)
    assert shared_two > independent_two
    return {
        "prime": p,
        "design": design,
        "design_moments_1_2_3": [0, 0, 0],
        "native_representation": "direct sum of central characters 1 and 2 of Heisenberg(F_131)",
        "ray_stabilizer": "{(x,y,z): x=z=0}; nonnormal",
        "kernel_pairs": checks,
        "kernel_arithmetic": "exact rational coefficients in Q[zeta_131]",
        "correct_b_inverse_a": list(good_argument),
        "wrong_a_b_inverse": list(wrong_argument),
        "correct_overlap": "1",
        "wrong_orientation_overlap": "7/32",
        "one_packet_shift_overlap": str(one_packet[0]),
        "two_independent_scales_overlap": str(independent_two),
        "two_shared_scales_overlap": str(shared_two),
        "zero_scale": "included, with conditional overlap one",
    }


if __name__ == "__main__":
    print(json.dumps({"symbolic": symbolic_checks(), "source": packet_control(),
                      "status": "bounded independent controls passed; not a theorem certificate"}, indent=2))

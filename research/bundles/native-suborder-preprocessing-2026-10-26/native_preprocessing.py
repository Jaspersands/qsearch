"""Exact interfaces for the native-suborder preprocessing argument.

Trace reconstruction consumes small-torsion action transcripts. Dictionary
extraction consumes an already split rational tensor algebra; the published
polynomial-time tensor splitter is NOT implemented here. Neither interface
authenticates the geometric provenance of supplied data.
"""

from itertools import product
from math import lcm, prod
from pathlib import Path
import sys

from sympy import Matrix, eye, isprime, zeros
from sympy.ntheory.modular import crt

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "kernel-output-2026-10-23"))
from kernel_output import QuaternionOrder, action, flat


def _rational_matrix(value, shape):
    matrix = Matrix(value)
    if matrix.shape != shape or any(x.is_Rational is not True for x in matrix):
        raise ValueError("rational matrix of the declared shape required")
    return matrix


def check_order(order):
    """Check identities, integrality and definiteness, not native provenance."""
    basis = [eye(4)[:, i] for i in range(4)]
    unit = _rational_matrix(order.unit, (4, 1))
    trace = _rational_matrix(order.traces, (1, 4))
    involution = _rational_matrix(order.involution, (4, 4))
    if len(order.products) != 4 or any(len(row) != 4 for row in order.products):
        raise ValueError("four-dimensional multiplication table required")
    entries = list(unit) + list(trace) + list(involution)
    for row in order.products:
        for value in row:
            entries.extend(_rational_matrix(value, (4, 1)))
    if any(x.q != 1 for x in entries):
        raise ValueError("integral order data required")
    if (trace*unit)[0] != 2 or involution**2 != eye(4):
        raise ValueError("trace or involution identity failed")
    for x in basis:
        if order.multiply(unit, x) != x or order.multiply(x, unit) != x:
            raise ValueError("unit identity failed")
        if order.star(x) != (trace*x)[0]*unit-x:
            raise ValueError("canonical involution identity failed")
    for x, y in product(basis, repeat=2):
        if order.star(order.multiply(x, y)) != order.multiply(order.star(y), order.star(x)):
            raise ValueError("anti-involution identity failed")
        z = x+y
        norm = order.multiply(z, order.star(z))
        if norm != (trace*norm)[0]/2*unit:
            raise ValueError("scalar reduced norm required")
    for x, y, z in product(basis, repeat=3):
        if order.multiply(order.multiply(x, y), z) != order.multiply(x, order.multiply(y, z)):
            raise ValueError("associativity failed")
    gram = Matrix(4, 4, lambda i, j: (trace*order.multiply(basis[i], order.star(basis[j])))[0])
    if gram != gram.T or any(gram[:i, :i].det() <= 0 for i in range(1, 5)):
        raise ValueError("positive definite trace norm form required")
    return gram


def recover_order(transcripts, degree_bound, characteristic):
    """Recover the order from genuine action matrices, given a degree bound.

    Each transcript is (prime, four integral 2x2 action matrices). No supplied
    multiplication table or dual-map evaluator is needed. The uniform CRT
    bound 2*B^2 covers reduced traces of products of up to three basis maps.
    """
    if type(degree_bound) is not int or degree_bound < 1:
        raise ValueError("positive integer degree bound required")
    if not isprime(characteristic) or characteristic <= 3:
        raise ValueError("prime characteristic greater than three required")
    primes, matrices = [], []
    for prime, actions in transcripts:
        if not isprime(prime) or prime == characteristic or prime in primes:
            raise ValueError("distinct prime-to-characteristic torsion levels required")
        if len(actions) != 4:
            raise ValueError("four basis actions required")
        actions = tuple(_rational_matrix(a, (2, 2)) for a in actions)
        if any(x.q != 1 for a in actions for x in a):
            raise ValueError("integral action representatives required")
        primes.append(int(prime))
        matrices.append(actions)
    bound = 2*degree_bound**2
    modulus = prod(primes)
    if modulus <= 2*bound:
        raise ValueError("insufficient CRT modulus for the declared degree bound")

    def word_trace(word):
        residues = []
        for prime, actions in zip(primes, matrices):
            value = eye(2)
            for index in word:
                value = value*actions[index]
            residues.append(int(value.trace()) % prime)
        value = int(crt(primes, residues)[0])
        if 2*value > modulus:
            value -= modulus
        if abs(value) > bound:
            raise ValueError("trace outside the declared CRT bound")
        return value

    traces = Matrix([[word_trace((i,)) for i in range(4)]])
    pairing = Matrix(4, 4, lambda i, j: word_trace((i, j)))
    if pairing.det() == 0:
        raise ValueError("rank-four nondegenerate trace pairing required")
    inverse = pairing.inv()
    unit = inverse*traces.T
    products = tuple(tuple(inverse*Matrix([word_trace((i, j, k)) for k in range(4)])
                           for j in range(4)) for i in range(4))
    order = QuaternionOrder(products, unit, unit*traces-eye(4), traces)
    check_order(order)
    for i in range(4):
        norm = (traces[i]**2-pairing[i, i])/2
        if norm.q != 1 or not 0 < norm <= degree_bound:
            raise ValueError("recovered basis norm exceeds the declared degree bound")
    for prime, actions in zip(primes, matrices):
        equations = [action(unit, actions)-eye(2)]
        equations.extend(action(products[i][j], actions)-actions[i]*actions[j]
                         for i, j in product(range(4), repeat=2))
        if any(int(x) % prime for equation in equations for x in equation):
            raise ValueError("reconstructed order disagrees with a torsion action")
    return order


def check_dictionary(source, target, coordinates):
    """Columns give images of source basis elements in the target basis."""
    coordinates = _rational_matrix(coordinates, (4, 4))
    if coordinates.det() == 0:
        raise ValueError("invertible dictionary required")
    if coordinates*source.unit != target.unit:
        raise ValueError("dictionary does not preserve the unit")
    for i, j in product(range(4), repeat=2):
        if coordinates*source.products[i][j] != target.multiply(coordinates[:, i], coordinates[:, j]):
            raise ValueError("dictionary does not preserve multiplication")
    if coordinates*source.involution != target.involution*coordinates:
        raise ValueError("dictionary does not preserve the involution")
    return coordinates


def dictionary_from_bimodule(source, target, left, right, vector):
    """Extract A -> B from an A tensor B^op representation on Q^4.

    `right` must be an ANTI-representation. For division A and B every
    nonzero vector is cyclic; no invertible-vector search is necessary.
    A certified tensor splitter, not this extraction, supplies the matrices.
    """
    if len(left) != 4 or len(right) != 4:
        raise ValueError("four left and four right actions required")
    left = tuple(_rational_matrix(a, (4, 4)) for a in left)
    right = tuple(_rational_matrix(a, (4, 4)) for a in right)
    vector = _rational_matrix(vector, (4, 1))
    if vector == zeros(4, 1):
        raise ValueError("nonzero cyclic vector required")
    if action(source.unit, left) != eye(4) or action(target.unit, right) != eye(4):
        raise ValueError("bimodule unit identity failed")
    for i, j in product(range(4), repeat=2):
        if left[i]*left[j] != action(source.products[i][j], left):
            raise ValueError("left representation identity failed")
        if right[i]*right[j] != action(target.products[j][i], right):
            raise ValueError("right opposite-algebra identity failed")
        if left[i]*right[j] != right[j]*left[i]:
            raise ValueError("left and right actions do not commute")
    tensor_basis = Matrix.hstack(*(flat(a*b) for a, b in product(left, right)))
    if tensor_basis.det() == 0:
        raise ValueError("tensor representation is not faithful")
    left_frame = Matrix.hstack(*(a*vector for a in left))
    right_frame = Matrix.hstack(*(a*vector for a in right))
    if left_frame.det() == 0 or right_frame.det() == 0:
        raise ValueError("vector not cyclic; division-algebra promise failed")
    return check_dictionary(source, target, right_frame.inv()*left_frame)


def clear_denominators(source, target, dictionary):
    dictionary = check_dictionary(source, target, dictionary)
    denominator = lcm(*(int(x.q) for x in dictionary))
    scaled = denominator*dictionary
    if any(x.q != 1 for x in scaled):
        raise ArithmeticError("failed to clear the lattice inclusion")
    return denominator, scaled


def reference_half_frobenius(curve, point, half):
    """Native finite control for (1+pi)/2 on y^2=x^3-x, p=3 mod 4.

    The caller supplies an actual half point in its declared field. Finding
    halves over field extensions and descending the result is NOT performed.
    The map is integral because pi fixes this curve's complete 2-torsion.
    """
    p = int(curve.field.characteristic())
    if p % 4 != 3 or curve.a != -1 or curve.b != 0:
        raise ValueError("reference model y^2=x^3-x, p=3 mod 4 required")
    if not curve.contains(point) or not curve.contains(half) or curve.multiply(2, half) != point:
        raise ValueError("valid half point required")
    image = None if half is None else (half[0]**p, half[1]**p)
    return curve.add(half, image)

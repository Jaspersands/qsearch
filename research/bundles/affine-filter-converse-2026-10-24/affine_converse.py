"""Exact small-block audit of the affine-filter/positive-mixture equivalence.

Inputs are codeword-indexed contribution Gram matrices, not unknown quantum
states. Exponential enumeration is capped and is only a proof-control tool.
"""

from dataclasses import dataclass
from fractions import Fraction as F


def rational(x):
    if type(x) not in (int, F, str):
        raise ValueError("exact rational required")
    return F(x)


def size_check(n):
    if type(n) is not int or n < 2 or n > 16 or n & (n-1):
        raise ValueError("control requires 2..16 codewords, power of two")
    return n.bit_length()-1


def character(x, y):
    return -1 if (x & y).bit_count() % 2 else 1


def subspace(v, n):
    if (type(v) is not tuple or not v or v != tuple(sorted(set(v))) or v[0] != 0
            or any(type(x) is not int or not 0 <= x < n for x in v)
            or any(a ^ b not in v for a in v for b in v)):
        raise ValueError("canonical binary subspace required")
    return v


def annihilator(v, n):
    size_check(n)
    subspace(v, n)
    return tuple(y for y in range(n) if all(character(y, x) == 1 for x in v))


def cosets(v, n):
    size_check(n)
    subspace(v, n)
    unseen, out = set(range(n)), []
    while unseen:
        a = min(unseen)
        group = tuple(sorted(a ^ x for x in v))
        out.append(group)
        unseen.difference_update(group)
    return tuple(out)


def psd(matrix):
    """Exact Schur pivots; a zero diagonal must have an identically zero row."""
    a = [list(map(rational, row)) for row in matrix]
    n = len(a)
    if not n or any(len(row) != n for row in a):
        raise ValueError("square matrix required")
    if any(a[i][j] != a[j][i] for i in range(n) for j in range(n)):
        return False
    for k in range(n):
        pivot = a[k][k]
        if pivot < 0:
            return False
        if pivot == 0:
            if any(a[k][j] for j in range(k+1, n)):
                return False
            continue
        for i in range(k+1, n):
            for j in range(i, n):
                a[i][j] -= a[i][k]*a[k][j]/pivot
                a[j][i] = a[i][j]
    return True


@dataclass(frozen=True)
class Effect:
    label_direction: tuple[int, ...]
    label_coset_representative: int
    gram: tuple[tuple[F, ...], ...]


@dataclass(frozen=True)
class Branch:
    frequency_coset: tuple[int, ...]
    weight: F
    label_direction: tuple[int, ...]


def gram_from_q(q):
    q = tuple(map(rational, q))
    n = len(q)
    size_check(n)
    return tuple(tuple(sum(q[y]*character(y, a ^ b) for y in range(n))
                       for b in range(n)) for a in range(n))


def audit(q, effects):
    q = tuple(map(rational, q))
    n = len(q)
    dimension = size_check(n)
    if any(x < 0 for x in q) or sum(q) != 1:
        raise ValueError("normalized nonnegative spectrum required")
    grouped, seen = {}, set()
    for effect in effects:
        if not isinstance(effect, Effect):
            raise ValueError("explicit Gram effect required")
        v = subspace(effect.label_direction, n)
        a = effect.label_coset_representative
        if (len(v) == n or type(a) is not int or not 0 <= a < n
                or min(a ^ x for x in v) != a):
            raise ValueError("proper affine outcome with canonical coset required")
        if (v, a) in seen:
            raise ValueError("duplicate outcome")
        seen.add((v, a))
        matrix = tuple(tuple(map(rational, row)) for row in effect.gram)
        if len(matrix) != n or any(len(row) != n for row in matrix):
            raise ValueError("Gram dimension mismatch")
        allowed = {a ^ x for x in v}
        if any(matrix[i][j] != 0 for i in range(n) for j in range(n)
               if i not in allowed or j not in allowed):
            raise ValueError("outcome is not unambiguous")
        if not psd(matrix):
            raise ValueError("outcome Gram is not PSD")
        total = grouped.setdefault(v, [[F(0) for _ in range(n)] for _ in range(n)])
        for i in range(n):
            for j in range(n):
                total[i][j] += matrix[i][j]

    used, branches, outcomes = [F(0)]*n, [], []
    for v, matrix in sorted(grouped.items()):
        if any(matrix[i][j] != matrix[0][i ^ j] for i in range(n) for j in range(n)):
            raise ValueError("measurement is not translation covariant")
        mass = tuple(sum(matrix[0][w]*character(y, w) for w in range(n))/n
                     for y in range(n))
        if any(x < 0 for x in mass):
            raise ArithmeticError("PSD Gram had a negative Fourier eigenvalue")
        before = len(branches)
        for group in cosets(annihilator(v, n), n):
            if any(mass[y] != mass[group[0]] for y in group):
                raise ArithmeticError("unambiguous covariance did not imply coset flatness")
            if mass[group[0]]:
                branches.append(Branch(group, len(group)*mass[group[0]], v))
        probability = sum(branch.weight for branch in branches[before:])
        if probability != matrix[0][0]:
            raise ArithmeticError("branch probability not preserved")
        outcomes.append({"label_direction": list(v), "probability": str(probability),
                         "unresolved_bits": len(v).bit_length()-1,
                         "revealed_bits": dimension-(len(v).bit_length()-1)})
        used = [u+x for u, x in zip(used, mass)]

    residual = tuple(x-u for x, u in zip(q, used))
    if any(x < 0 for x in residual):
        raise ValueError("residual effect is not PSD: spectrum budget exceeded")
    branches += [Branch((y,), weight, tuple(range(n)))
                 for y, weight in enumerate(residual) if weight]
    reconstructed = tuple(sum(b.weight/len(b.frequency_coset) for b in branches
                              if y in b.frequency_coset) for y in range(n))
    if reconstructed != q or sum(b.weight for b in branches) != 1:
        raise ArithmeticError("positive affine decomposition did not reconstruct source")
    load = sum(b.weight*(len(b.label_direction).bit_length()-1) for b in branches)
    return {"dimension": dimension, "branches": branches, "outcomes": outcomes,
            "residual_spectrum": residual, "mean_unresolved_bits": load,
            "source_reconstructed_exactly": True,
            "fixed_instance_Gibbs_sampler_certified": False,
            "efficient_for_growing_blocks_certified": False}


def mixture_effects(q, mixtures):
    """Construct control inputs; independently checked against physical POVMs."""
    n = len(q)
    size_check(n)
    grouped = {}
    for group, weight in mixtures:
        if (not group or group != tuple(sorted(set(group)))
                or any(type(x) is not int or not 0 <= x < n for x in group)):
            raise ValueError("canonical frequency coset required")
        direction = tuple(sorted(x ^ group[0] for x in group))
        v = annihilator(direction, n)
        weight = rational(weight)
        if weight < 0:
            raise ValueError("nonnegative branch weight required")
        if len(v) == n:
            continue
        for labels in cosets(v, n):
            matrix = grouped.setdefault((v, labels[0]), [[F(0)]*n for _ in range(n)])
            for a in labels:
                for b in labels:
                    matrix[a][b] += weight*character(group[0], a ^ b)
    return [Effect(v, a, tuple(map(tuple, matrix)))
            for (v, a), matrix in sorted(grouped.items())]


def four_message(c):
    c = rational(c)
    if not 0 <= c <= 1:
        raise ValueError("overlap must lie in [0,1]")
    p0, p1 = (1+c)/2, (1-c)/2
    q = tuple(p0**(4-y.bit_count())*p1**y.bit_count()
              + p0**y.bit_count()*p1**(4-y.bit_count()) for y in range(8))
    mixture = [(tuple(range(8)), (1-c*c)**2)]
    mixture += [((0, v), (c*c-c**4)/2) for v in (1, 2, 4, 7)]
    mixture += [((0,), c**4)]
    return q, mixture_effects(q, mixture)


def fixed_sign_countercontrol():
    """A one-bit public factor with a rare but tilted four-equation branch."""
    n, epsilon = 16, F(1, 64)
    q = tuple((1-epsilon)/n+(epsilon if y == 0 else 0) for y in range(n))
    result = audit(q, mixture_effects(q, [(tuple(range(n)), 1-epsilon)]))
    if sum(result["residual_spectrum"]) != epsilon:
        raise ArithmeticError("rank-defect branch probability mismatch")
    # Public map A*x=(x,x,x,x). Full-space branch samples x uniformly;
    # point branch has four equations but rank one and falls back to x=0.
    proposed_zero = (1+epsilon)/2
    cases = []
    for b in range(n):
        target_zero = q[b]/(q[b]+q[b ^ 15])
        cases.append({"sign_mask": b, "target_zero": str(target_zero),
                      "proposal_zero": str(proposed_zero),
                      "tv": str(abs(target_zero-proposed_zero))})
    mean_tv = sum(F(row["tv"]) for row in cases)/n
    return {"epsilon": str(epsilon), "sign_average_bound": str(3*epsilon),
            "all_sign_mean_tv": str(mean_tv), "cases": cases,
            "fixed_zero_sign_exceeds_average_bound": F(cases[0]["tv"]) > 3*epsilon,
            "all_sign_average_obeys_bound": mean_tv <= 3*epsilon}

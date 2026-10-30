"""Verified two-component norm completion; no fixed-prime scaling claim."""

from fractions import Fraction
from itertools import combinations_with_replacement
import random

from flint import fmpz, nmod_mat


def rows(matrix):
    return [[int(matrix[i, j]) for j in range(matrix.ncols())]
            for i in range(matrix.nrows())]


def checked_matrix(data, p):
    data = [list(row) for row in data]
    if not data or not data[0] or any(len(row) != len(data[0]) for row in data):
        raise ValueError("nonempty rectangular matrix required")
    if any(type(x) is not int or not 0 <= x < p for row in data for x in row):
        raise ValueError("canonical prime-field entries required")
    return data


def nullspace(matrix, p):
    raw, dimension = nmod_mat(matrix, p).nullspace()
    return [[int(raw[i, j]) for j in range(dimension)]
            for i in range(len(matrix[0]))]


def rank(matrix, p):
    return 0 if not matrix or not matrix[0] else nmod_mat(matrix, p).rank()


def affine_solution(matrix, target, p):
    """Return a checked particular point and column nullspace basis."""
    width = len(matrix[0])
    reduced, _ = nmod_mat([row+[value] for row, value in zip(matrix, target)], p).rref()
    data = rows(reduced)
    point = [0]*width
    for row in data:
        pivot = next((j for j in range(width) if row[j]), None)
        if pivot is None:
            if row[-1]:
                raise ValueError("inconsistent affine system")
        else:
            point[pivot] = row[-1]
    if any((sum(a*b for a, b in zip(row, point))-t) % p
           for row, t in zip(matrix, target)):
        raise ArithmeticError("particular solution failed")
    return point, nullspace(matrix, p)


class NormCompletion:
    def __init__(self, p, parity, auxiliary, h, nonsquare):
        if type(p) is not int or not 3 <= p < 2**63 or not fmpz(p).is_prime():
            raise ValueError("verified odd prime below 2^63 required")
        self.p = p
        self.B, self.A = checked_matrix(parity, p), checked_matrix(auxiliary, p)
        self.k, self.m, self.r = len(self.B), len(self.B[0]), len(self.A)
        if len(self.A[0]) != self.m:
            raise ValueError("auxiliary width mismatch")
        if rank(self.B, p) != self.k or rank(self.A, p) != self.r:
            raise ValueError("independent input rows required")
        self.h = self.vector(h, self.m)
        if (type(nonsquare) is not int or not 0 < nonsquare < p
                or pow(nonsquare, (p-1)//2, p) != p-1):
            raise ValueError("verified nonsquare required")
        self.nu = nonsquare
        self.T = [i for i, x in enumerate(self.h) if x]
        if not self.T:
            raise ValueError("nonzero annihilator required")
        for u, v in combinations_with_replacement(self.A, 2):
            term = [self.h[i]*u[i]*v[i] % p for i in range(self.m)]
            if any(sum(b*t for b, t in zip(row, term)) % p for row in self.B):
                raise ValueError("mixed quadratic annihilator identity fails")

    def vector(self, data, size):
        data = list(data)
        if len(data) != size or any(type(x) is not int or not 0 <= x < self.p for x in data):
            raise ValueError("canonical vector of required size expected")
        return data

    def verifies(self, word, syndrome):
        word, syndrome = self.vector(word, self.m), self.vector(syndrome, self.k)
        return all(word) and all(sum(x*y for x, y in zip(row, word)) % self.p == s
                                 for row, s in zip(self.B, syndrome))

    def evaluate(self, coefficients, a, b):
        coefficients = self.vector(coefficients, 2*self.r)
        a, b = self.vector(a, len(self.T)), self.vector(b, len(self.T))
        word = [1]*self.m
        for j, i in enumerate(self.T):
            u = (a[j]+sum(coefficients[t]*self.A[t][i] for t in range(self.r))) % self.p
            v = (b[j]+sum(coefficients[self.r+t]*self.A[t][i] for t in range(self.r))) % self.p
            word[i] = self.h[i]*(u*u-self.nu*v*v) % self.p
        return word

    def prepare(self, syndrome, a, b):
        syndrome = self.vector(syndrome, self.k)
        a, b = self.vector(a, len(self.T)), self.vector(b, len(self.T))
        p, r = self.p, self.r
        base = self.evaluate([0]*(2*r), a, b)
        matrix = []
        for row in self.B:
            left = [2*sum(row[i]*self.h[i]*a[j]*self.A[t][i]
                          for j, i in enumerate(self.T)) % p for t in range(r)]
            right = [-2*self.nu*sum(row[i]*self.h[i]*b[j]*self.A[t][i]
                                   for j, i in enumerate(self.T)) % p for t in range(r)]
            matrix.append(left+right)
        if rank(matrix, p) != self.k:
            return {"status": "UNKNOWN_SYNDROME_RANK", "matrix": matrix}
        target = [(s-sum(x*y for x, y in zip(row, base))) % p
                  for s, row in zip(syndrome, self.B)]
        point, kernel = affine_solution(matrix, target, p)
        dimension = len(kernel[0])
        events = []
        for j, i in enumerate(self.T):
            pair = [(a[j]+sum(point[t]*self.A[t][i] for t in range(r))) % p,
                    (b[j]+sum(point[r+t]*self.A[t][i] for t in range(r))) % p]
            image = [[sum(self.A[t][i]*kernel[start+t][v] for t in range(r)) % p
                      for v in range(dimension)] for start in (0, r)]
            rho = rank(image, p)
            attainable = rank([row+[(-value) % p] for row, value in zip(image, pair)], p) == rho
            probability = Fraction(1, p**rho) if attainable else Fraction(0)
            events.append({"coordinate": i, "rank": rho, "zero_attainable": attainable,
                           "probability": probability})
        return {"status": "CERTIFIED_AFFINE_FIBER", "matrix": matrix,
                "point": point, "kernel": kernel, "dimension": dimension,
                "a": a, "b": b, "events": events,
                "zero_union_bound": sum((e["probability"] for e in events), Fraction(0))}

    def sample(self, prepared, rng):
        if prepared["status"] != "CERTIFIED_AFFINE_FIBER":
            raise ValueError("a prepared affine fiber is required")
        free = [rng.randrange(self.p) for _ in range(prepared["dimension"])]
        coefficients = [(x+sum(a*b for a, b in zip(row, free))) % self.p
                        for x, row in zip(prepared["point"], prepared["kernel"])]
        return self.evaluate(coefficients, prepared["a"], prepared["b"])

    def solve(self, syndrome, *, seed, offset_attempts=8, kernel_attempts=8):
        syndrome = self.vector(syndrome, self.k)
        if any(type(cap) is not int or cap < 1 for cap in (offset_attempts, kernel_attempts)):
            raise ValueError("positive attempt caps required")
        rng = random.Random(seed)
        history = []
        for trial in range(offset_attempts):
            a, b = ([rng.randrange(self.p) for _ in self.T] for _ in range(2))
            prepared = self.prepare(syndrome, a, b)
            record = {"status": prepared["status"]}
            if prepared["status"] != "CERTIFIED_AFFINE_FIBER":
                history.append(record)
                continue
            eta = prepared["zero_union_bound"]
            record.update(zero_union_bound=eta, kernel_dimension=prepared["dimension"],
                          marginal_ranks=[e["rank"] for e in prepared["events"]])
            history.append(record)
            if eta > Fraction(1, 2):
                record["status"] = "UNKNOWN_PROBABILITY_CERTIFICATE"
                continue
            for attempt in range(kernel_attempts):
                word = self.sample(prepared, rng)
                if any(sum(x*y for x, y in zip(row, word)) % self.p != s
                       for row, s in zip(self.B, syndrome)):
                    raise ArithmeticError("linearized sample violates original syndrome")
                if self.verifies(word, syndrome):
                    return {"status": "VERIFIED_NATIVE_WITNESS", "word": word,
                            "syndrome": syndrome, "offset_trials": trial+1,
                            "last_kernel_samples": attempt+1, "history": history,
                            "uniform_native_sampling": False}
        return {"status": "UNKNOWN_ATTEMPT_CAP", "word": None, "history": history,
                "hardness_evidence": False, "uniform_native_sampling": False}

"""Full HDQI pilot sampling for a supplied line-graph root.

Exact rational DPP/interference back end; numerical, NOT interval-certified,
matrix-function front end. Cost is exponential in cycle rank, not vertex count.
No dense Hilbert-space operations occur in this module.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction as F
import math
import random

import numpy as np
from scipy.linalg import eigh


def _integer(value):
    return isinstance(value, int) and not isinstance(value, bool)


@dataclass(frozen=True)
class Root:
    n: int
    edges: tuple[tuple[int, int], ...]
    couplings: tuple[float, ...]
    forest: tuple[int, ...]
    chords: tuple[int, ...]
    components: tuple[int, ...]
    parents: tuple[tuple[int, int], ...]
    order: tuple[int, ...]

    @property
    def cycle_rank(self):
        return len(self.chords)

    @property
    def line_edges(self):
        return tuple((i, j) for i, e in enumerate(self.edges)
                     for j in range(i + 1, len(self.edges))
                     if set(e).intersection(self.edges[j]))


def root(n, edges, couplings=None):
    if not _integer(n) or n < 1:
        raise ValueError("root needs a positive integer number of vertices")
    normalized = []
    for edge in edges:
        if len(edge) != 2 or any(not _integer(v) for v in edge):
            raise ValueError("each edge needs two integer endpoints")
        u, v = sorted(edge)
        if not 0 <= u < v < n or (u, v) in normalized:
            raise ValueError("invalid, duplicate, or loop edge")
        normalized.append((u, v))
    js = tuple([1.0] * len(normalized) if couplings is None else couplings)
    if (len(js) != len(normalized)
            or any(isinstance(j, (bool, complex)) or not np.isfinite(j)
                   or abs(j) > 1 for j in js)):
        raise ValueError("need finite real edge couplings with |J| <= 1")
    representatives = list(range(n))

    def find(a):
        while representatives[a] != a:
            a = representatives[a]
        return a

    forest, chords = [], []
    adjacency = [[] for _ in range(n)]
    for e, (u, v) in enumerate(normalized):
        ru, rv = find(u), find(v)
        if ru == rv:
            chords.append(e)
        else:
            representatives[ru] = rv
            forest.append(e)
            adjacency[u].append((v, e))
            adjacency[v].append((u, e))
    components = [-1] * n
    parents = [(-1, -1)] * n
    order = []
    for start in range(n):
        if components[start] != -1:
            continue
        stack = [start]
        components[start] = start
        while stack:
            u = stack.pop()
            order.append(u)
            for v, e in adjacency[u]:
                if components[v] == -1:
                    components[v] = start
                    parents[v] = (u, e)
                    stack.append(v)
    return Root(n, tuple(normalized), tuple(map(float, js)), tuple(forest),
                tuple(chords), tuple(components), tuple(parents), tuple(order))


def boundary(model, y):
    if not _integer(y) or not 0 <= y < 1 << len(model.edges):
        raise ValueError("invalid edge word")
    answer = 0
    for e, (u, v) in enumerate(model.edges):
        if (y >> e) & 1:
            answer ^= (1 << u) | (1 << v)
    return answer


def chord_word(model, y):
    boundary(model, y)
    return sum(((y >> e) & 1) << a for a, e in enumerate(model.chords))


def decode(model, x, c):
    """Invert incidence plus chord coordinates, retaining every cycle bit."""
    if (not _integer(x) or not 0 <= x < 1 << model.n or not _integer(c)
            or not 0 <= c < 1 << model.cycle_rank):
        raise ValueError("invalid endpoint or chord label")
    y = sum(((c >> a) & 1) << e for a, e in enumerate(model.chords))
    residual = x ^ boundary(model, y)
    for v in reversed(model.order):
        u, e = model.parents[v]
        if u != -1 and (residual >> v) & 1:
            y |= 1 << e
            residual ^= (1 << v) | (1 << u)
    if residual:
        raise ValueError("endpoint parity must be even in EACH root component")
    return y


def word_phase(model, y):
    """phi_0(P(y)) = i**phase gamma_boundary(y), with ascending gamma order."""
    boundary(model, y)
    phase, mask = 0, 0
    for e, endpoints in enumerate(model.edges):
        if (y >> e) & 1:
            phase = (phase + 1) % 4
            for v in endpoints:
                phase = (phase + 2 * (mask >> (v + 1)).bit_count()) % 4
                mask ^= 1 << v
    return phase, mask


def matrix_function(model, beta, flux=0):
    """K=-i tanh(beta iA/2)=tan(beta A/2), and Gaussian log normalizers."""
    if (isinstance(beta, (bool, complex)) or not np.isfinite(beta) or beta < 0
            or not _integer(flux) or not 0 <= flux < 1 << model.cycle_rank):
        raise ValueError("invalid temperature or flux")
    a = np.zeros((model.n, model.n))
    chord_index = {e: j for j, e in enumerate(model.chords)}
    for e, ((u, v), j) in enumerate(zip(model.edges, model.couplings)):
        sign = -1 if e in chord_index and (flux >> chord_index[e]) & 1 else 1
        a[u, v], a[v, u] = sign * j, -sign * j
    values, vectors = eigh(1j * a)
    with np.errstate(over="raise", invalid="raise"):
        t = beta * values
        k_complex = -1j * ((vectors * np.tanh(t / 2)) @ vectors.conj().T)
        log_c = float(np.sum(np.logaddexp(t / 2, -t / 2) - math.log(2)) / 2)
        log_z = float(np.sum(np.logaddexp(t, -t) - math.log(2)) / 2)
    if np.max(np.abs(k_complex.imag)) > 1e-10:
        raise ArithmeticError("matrix-function reality control failed")
    k = (k_complex.real - k_complex.real.T) / 2
    for i in range(model.n):
        for j in range(model.n):
            if model.components[i] != model.components[j]:
                k[i, j] = 0
    return k, log_c, log_z


def determinant(matrix):
    a = [list(map(F, row)) for row in matrix]
    n, result = len(a), F(1)
    if any(len(row) != n for row in a):
        raise ValueError("matrix must be square")
    for i in range(n):
        p = next((p for p in range(i, n) if a[p][i]), None)
        if p is None:
            return F(0)
        if p != i:
            a[i], a[p] = a[p], a[i]
            result = -result
        pivot = a[i][i]
        result *= pivot
        for j in range(i + 1, n):
            ratio = a[j][i] / pivot
            for k in range(i + 1, n):
                a[j][k] -= ratio * a[i][k]
    return result


def pfaffian(matrix):
    a = [list(map(F, row)) for row in matrix]
    n = len(a)
    if any(len(row) != n for row in a):
        raise ValueError("matrix must be square")
    if any(a[i][j] != -a[j][i] for i in range(n) for j in range(n)):
        raise ValueError("Pfaffian requires exact skew symmetry")
    if n % 2:
        return F(0)
    answer = F(1)
    for i in range(0, n, 2):
        p = next((p for p in range(i + 1, n) if a[i][p]), None)
        if p is None:
            return F(0)
        if p != i + 1:
            a[p], a[i + 1] = a[i + 1], a[p]
            for row in a:
                row[p], row[i + 1] = row[i + 1], row[p]
            answer = -answer
        pivot = a[i][i + 1]
        answer *= pivot
        for j in range(i + 2, n):
            for k in range(j + 1, n):
                a[j][k] += (a[i + 1][j] * a[i][k]
                            - a[i][j] * a[i + 1][k]) / pivot
                a[k][j] = -a[j][k]
    return answer


def minor(matrix, x):
    ids = [i for i in range(len(matrix)) if (x >> i) & 1]
    return [[matrix[i][j] for j in ids] for i in ids]


def marginal_kernel(k):
    n = len(k)
    a = [[F(i == j) + k[i][j] for j in range(n)]
         + [F(i == j) for j in range(n)] for i in range(n)]
    for i in range(n):
        p = next((p for p in range(i, n) if a[p][i]), None)
        if p is None:
            raise ArithmeticError("I+K must be invertible for real skew K")
        a[i], a[p] = a[p], a[i]
        pivot = a[i][i]
        a[i] = [entry / pivot for entry in a[i]]
        for j in range(n):
            if j != i:
                ratio = a[j][i]
                a[j] = [u - ratio * v for u, v in zip(a[j], a[i])]
    return tuple(tuple(F(i == j) - a[i][n + j] for j in range(n)) for i in range(n))


def condition(kernel, included):
    p = kernel[0][0]
    if not 0 <= p <= 1:
        raise ArithmeticError("invalid conditional probability; never clip")
    denominator = p if included else p - 1
    if not denominator:
        raise ValueError("zero-probability conditional branch")
    return tuple(tuple(kernel[i][j] - kernel[i][0] * kernel[0][j] / denominator
                       for j in range(1, len(kernel)))
                 for i in range(1, len(kernel)))


def coin(p, rng):
    if not isinstance(p, F) or not 0 <= p <= 1:
        raise ValueError("exact coin needs a rational probability")
    return bool(p) and (p == 1 or rng.randrange(p.denominator) < p.numerator)


def sample_dpp(kernel, rng):
    x = 0
    for i in range(len(kernel)):
        take = coin(kernel[0][0], rng)
        x |= int(take) << i
        kernel = condition(kernel, take)
    return x


@dataclass(frozen=True)
class Sector:
    k: tuple[tuple[F, ...], ...]
    scale: F
    norm: F
    marginal: tuple[tuple[F, ...], ...]


@dataclass(frozen=True)
class Prepared:
    model: Root
    beta: float
    bits: int
    sectors: tuple[Sector, ...]
    total_norm: F
    native_error_certified: bool = False


def prepare(model, beta, bits=32, max_cycle_rank=6):
    if not _integer(bits) or not 8 <= bits <= 52:
        raise ValueError("float front end supports 8..52 quantization bits")
    if not _integer(max_cycle_rank) or max_cycle_rank < 0:
        raise ValueError("invalid explicit sector-work cap")
    if model.cycle_rank > max_cycle_rank:
        raise ValueError("cycle-rank cap exceeded; exponential work is not free")
    data = [matrix_function(model, beta, z) for z in range(1 << model.cycle_rank)]
    top = max(row[1] for row in data)
    scale = 1 << bits
    sectors = []
    for k, log_c, _ in data:
        rational = [[F(0) for _ in range(model.n)] for _ in range(model.n)]
        for i in range(model.n):
            for j in range(i + 1, model.n):
                rational[i][j] = F(round(float(k[i, j]) * scale), scale)
                rational[j][i] = -rational[i][j]
        rational = tuple(map(tuple, rational))
        prefactor = F(round(math.exp(log_c - top) * scale), scale)
        norm = determinant([[F(i == j) + rational[i][j] for j in range(model.n)]
                            for i in range(model.n)])
        sectors.append(Sector(rational, prefactor, norm, marginal_kernel(rational)))
    total = sum((s.scale ** 2 * s.norm for s in sectors), F(0))
    return Prepared(model, float(beta), bits, tuple(sectors), total)


def amplitudes(prepared, x):
    return tuple(s.scale * pfaffian(minor(s.k, x)) for s in prepared.sectors)


def coherent_numerator(values, c):
    return sum(((-1 if (z & c).bit_count() % 2 else 1) * value
                for z, value in enumerate(values)), F(0))


def probability(prepared, y):
    values = amplitudes(prepared, boundary(prepared.model, y))
    numerator = coherent_numerator(values, chord_word(prepared.model, y))
    return numerator ** 2 / (len(values) * prepared.total_norm)


def proposal_probability(prepared, y):
    values = amplitudes(prepared, boundary(prepared.model, y))
    return sum((v * v for v in values), F(0)) / (len(values) * prepared.total_norm)


def acceptance(values, c):
    norm = sum((v * v for v in values), F(0))
    if not norm:
        raise ValueError("zero-mass proposal")
    result = coherent_numerator(values, c) ** 2 / (len(values) * norm)
    if not 0 <= result <= 1:
        raise ArithmeticError("interference envelope failed")
    return result


def perturbation_bound(n, cycle_rank, entry_error, scale_error):
    """Conditional TV bound: callers must CERTIFY the supplied source errors.

    The numerical front end does not provide these certificates. Both errors
    are absolute; entry_error bounds every skew-matrix entry and scale_error
    bounds every exp(log(C_z)-max(log(C))) prefactor.
    """
    if (not _integer(n) or n < 1 or not _integer(cycle_rank) or cycle_rank < 0
            or not isinstance(entry_error, F) or not isinstance(scale_error, F)
            or entry_error < 0 or scale_error < 0 or n * entry_error > 1):
        raise ValueError("need certified nonnegative rational errors; n*entry_error<=1")
    return min(F(1), (1 << (n + cycle_rank + 1))
               * (scale_error + n * (n - 1) * entry_error / 2))


def sample(prepared, rng=None, max_trials=10000):
    if not _integer(max_trials) or max_trials < 1:
        raise ValueError("need a positive rejection cap")
    rng = random.Random() if rng is None else rng
    count = len(prepared.sectors)
    for trial in range(1, max_trials + 1):
        remaining = prepared.total_norm
        chosen = None
        for sector in prepared.sectors:
            weight = sector.scale ** 2 * sector.norm
            if coin(weight / remaining, rng):
                chosen = sector
                break
            remaining -= weight
        if chosen is None:
            raise ArithmeticError("sector selection exhausted positive mass")
        x = sample_dpp(chosen.marginal, rng)
        c = rng.randrange(count)
        values = amplitudes(prepared, x)
        if coin(acceptance(values, c), rng):
            return {"word": decode(prepared.model, x, c), "trials": trial}
    raise RuntimeError("INCONCLUSIVE: rejection cap exhausted; no sample returned")

"""Classical falsifier of the coordinate MM orbit-residual extension.

Uses only forward evaluation of an explicit triangular permutation. The
general determinant proof does not require an inverse or supplied zero.
"""

from dataclasses import dataclass
from fractions import Fraction as F
from pathlib import Path
import random
import sys

from flint import nmod_mat

sys.path.insert(0, str(Path(__file__).resolve().parents[1]/"orbit-residual-decoder-2026-10-24"))
from orbit_decoder import field, geometry, integer  # noqa: E402


@dataclass(frozen=True)
class Form:
    p: int
    shift: tuple[int, ...]
    scale: int
    offset: int

    def __post_init__(self):
        field(self.p)
        if type(self.shift) is not tuple:
            raise ValueError("explicit permutation shift required")
        integer(len(self.shift), "half-width", 1, 7)
        for x in self.shift:
            integer(x, "shift", 0, self.p-1)
        integer(self.scale, "nonzero public multiplier", 1, self.p-1)
        integer(self.offset, "offset", 0, self.p-1)

    def permutation(self, y):
        if len(y) != len(self.shift):
            raise ValueError("wrong permutation dimension")
        for v in y:
            integer(v, "field coordinate", 0, self.p-1)
        z = [(a-b) % self.p for a, b in zip(y, self.shift)]
        return tuple((v+(z[j-1]**2 if j else 0)) % self.p for j, v in enumerate(z))

    def g(self, y):
        return (self.offset+sum((j+1)*x**3 for j, x in enumerate(y))) % self.p

    def residual(self, block):
        k = len(self.shift)
        if len(block) != 2*k+1:
            raise ValueError("wrong block dimension")
        x, y, last = block[:k], block[k:2*k], block[-1]
        return (last+self.scale*(sum(a*b for a, b in zip(x, self.permutation(y)))+self.g(y))) % self.p


def instance(p, width, seed):
    integer(width, "odd orbit width", 3, 15)
    if not width % 2:
        raise ValueError("MM block needs odd width 2k+1")
    field(p)
    M, k = (p-1)//width, (width-1)//2
    L = (k+1)*M
    g = geometry(p, width, (L+width-1)//width)
    rng = random.Random(seed)
    forms = [Form(p, tuple(rng.randrange(p) for _ in range(k)), rng.randrange(1, p), rng.randrange(p))
             for _ in range(M)]
    allowed = [tuple(sorted(rng.sample(range(p), (p-1)//2))) for _ in range(M)]
    return g, forms, allowed


def validate(g, forms, allowed):
    if not g.width % 2:
        raise ValueError("odd orbit width required")
    k, M = (g.width-1)//2, len(g.representatives)
    if len(forms) != M or len(allowed) != M:
        raise ValueError("one public form and halfset per orbit required")
    for form, row in zip(forms, allowed):
        if not isinstance(form, Form) or form.p != g.p or len(form.shift) != k:
            raise ValueError("wrong public form")
        if len(row) != (g.p-1)//2 or len(set(row)) != len(row):
            raise ValueError("explicit distinct halfset required")
        for x in row:
            integer(x, "allowed field value", 0, g.p-1)
    L = (k+1)*M
    if g.dimension < L:
        raise ValueError("below the classical interpolation threshold")
    return k, M, L


def linear_attempt(g, forms, allowed, ys):
    k, M, L = validate(g, forms, allowed)
    if len(ys) != M:
        raise ValueError("one fixed y tuple per orbit required")
    rows, rhs = [], []
    for points, form, targets, y in zip(g.points, forms, allowed, ys):
        pi = form.permutation(y)
        vectors = [[pow(a, j, g.p) for j in range(L)] for a in points]
        rows.extend(vectors[k:2*k])
        rhs.extend(y)
        rows.append([(vectors[-1][j]+form.scale*sum(pi[t]*vectors[t][j] for t in range(k))) % g.p
                     for j in range(L)])
        rhs.append((targets[0]-form.scale*form.g(y)) % g.p)
    matrix = nmod_mat(rows, g.p)
    rank = matrix.rank()
    if rank != L:
        return {"status": "RETRY_SINGULAR", "rank": rank, "constraints": L}
    solution = matrix.solve(nmod_mat([[x] for x in rhs], g.p))
    coefficients = [int(solution[i, 0]) for i in range(L)]
    checked = verify(g, forms, allowed, coefficients)
    if not checked["all_predicates_pass"]:
        raise ArithmeticError("classical interpolation failed native replay")
    return {"status": "VERIFIED_NATIVE_PERFECT", "rank": rank, "constraints": L,
            "coefficients": coefficients, "verification": checked}


def verify(g, forms, allowed, coefficients):
    validate(g, forms, allowed)
    if not coefficients or len(coefficients) > g.dimension:
        raise ValueError("one polynomial below the original dimension required")
    for x in coefficients:
        integer(x, "coefficient", 0, g.p-1)
    residuals = []
    for points, form in zip(g.points, forms):
        values = []
        for x in points:
            value = 0
            for c in reversed(coefficients):
                value = (value*x+c) % g.p
            values.append(value)
        # Native replay deliberately expands the concrete forward formula,
        # rather than using the linear system or its supplied y tuples.
        k = len(form.shift)
        y = values[k:2*k]
        z = [(v-c) % g.p for v, c in zip(y, form.shift)]
        dot = sum(values[j]*(z[j]+(z[j-1]**2 if j else 0)) for j in range(k))
        cubic = form.offset+sum((j+1)*v**3 for j, v in enumerate(y))
        residuals.append((values[-1]+form.scale*(dot+cubic)) % g.p)
    score = sum(r in row for r, row in zip(residuals, allowed))
    return {"score": score, "M": len(allowed), "all_predicates_pass": score == len(allowed),
            "degree_upper": len(coefficients)-1, "original_dimension": g.dimension,
            "residuals": residuals, "verification": "Horner_at_all_original_points_and_original_halfsets"}


def solve(g, forms, allowed, seed, attempts=3):
    k, M, L = validate(g, forms, allowed)
    integer(attempts, "paid attempts", 1, 100)
    rng, history = random.Random(seed), []
    for number in range(1, attempts+1):
        ys = [tuple(rng.randrange(g.p) for _ in range(k)) for _ in range(M)]
        result = linear_attempt(g, forms, allowed, ys)
        history.append({"status": result["status"], "rank": result["rank"]})
        if result["status"] == "VERIFIED_NATIVE_PERFECT":
            break
    return {**result, "attempt_history": history, "attempts_executed": number,
            "field_random_draws": number*k*M, "system_forward_permutation_calls": number*M,
            "matrix_dimension": L, "one_attempt_failure_bound": str(F(M, g.p)),
            "capped_failure_bound": str(F(M, g.p)**attempts),
            "proof_bound_requires_independent_uniform_draws": True,
            "seeded_run_is_only_a_deterministic_control": True,
            "work_counter_scope": "draws_and_system_evaluations_only_not_all_arithmetic_or_native_replay",
            "permutation_inverse_or_root_used": False, "quantum_resources": 0}

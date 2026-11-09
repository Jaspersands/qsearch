"""Item 7(a): exact checks of Theorem uniform-compilation (i), (ii), (iv).

Read-only use of theorems/uniform_bch_rees.py:bch_via_ode and the committed
artifact research/reductions/rees_uniform_instrument.json. Exact arithmetic
mod p throughout. Run from the repo root:

    /opt/anaconda3/bin/python -B research/audits/reviews/2026-11-02-rees-compilation-filters/bch_compilation_check.py
"""
import itertools
import json
import random
import sys
from math import factorial
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT))
from theorems.uniform_bch_rees import bch_via_ode  # noqa: E402

rng = random.Random(20261102)


def formula(c):
    return (c - 1) * c * (c + 1) * (c + 2) // 6


# ---- strictly upper triangular N x N matrices over F_p, class N-1 ----------
def basis_positions(N):
    return [(i, j) for i in range(N) for j in range(i + 1, N)]


def to_mat(v, N, p):
    M = [[0] * N for _ in range(N)]
    for (i, j), a in zip(basis_positions(N), v):
        M[i][j] = a % p
    return M


def to_vec(M, N, p):
    return tuple(M[i][j] % p for (i, j) in basis_positions(N))


def mul(A, B, p):
    n = len(A)
    return [[sum(A[i][k] * B[k][j] for k in range(n)) % p for j in range(n)]
            for i in range(n)]


def add(A, B, p, s=1):
    return [[(a + s * b) % p for a, b in zip(r, q)] for r, q in zip(A, B)]


def scal(A, s, p):
    return [[(s * a) % p for a in r] for r in A]


def eye(N):
    return [[int(i == j) for j in range(N)] for i in range(N)]


def mexp(X, p):
    N = len(X)
    out, power = eye(N), eye(N)
    for j in range(1, N):  # X^N = 0 and N <= p
        power = mul(power, X, p)
        out = add(out, scal(power, pow(factorial(j), -1, p), p), p)
    return out


def mlog(G, p):
    N = len(G)
    Y = add(G, eye(N), p, -1)
    out, power = [[0] * N for _ in range(N)], eye(N)
    for j in range(1, N):
        power = mul(power, Y, p)
        out = add(out, scal(power, (-1) ** (j + 1) * pow(j, -1, p), p), p)
    return out


def make_bracket(N, p, counter):
    def bracket(u, v):
        counter[0] += 1
        A, B = to_mat(u, N, p), to_mat(v, N, p)
        return to_vec(add(mul(A, B, p), mul(B, A, p), p, -1), N, p)
    return bracket


def next_prime(k):
    q = k + 1
    while any(q % d == 0 for d in range(2, int(q ** 0.5) + 1)):
        q += 1
    return q


def bch(u, v, N, p, counter=None):
    counter = counter if counter is not None else [0]
    return bch_via_ode(u, v, prime=p, nilpotency_class=N - 1,
                       bracket=make_bracket(N, p, counter))


def main():
    lines = []
    out = lines.append

    # (i) exact bracket count, every class 1..12, and correctness vs matrix exp/log.
    out("== (i) bracket calls of bch_via_ode versus (c-1)c(c+1)(c+2)/6")
    for c in range(1, 13):
        N, p = c + 1, next_prime(c)
        dim = len(basis_positions(N))
        counts = set()
        for _ in range(2):
            ctr = [0]
            x = tuple(rng.randrange(p) for _ in range(dim))
            y = tuple(rng.randrange(p) for _ in range(dim))
            bch(x, y, N, p, ctr)
            counts.add(ctr[0])
        assert counts == {formula(c)}, (c, counts)
        out(f" c={c:2d} p={p:2d}: calls={sorted(counts)} formula={formula(c)} EXACT")

    out("== (i) correctness: bch_via_ode == log(exp X exp Y) in n_N(F_p), N=c+1<=p")
    cases = [(1, 2), (2, 3), (2, 5), (3, 5), (4, 5), (4, 7), (5, 7), (6, 7), (6, 11), (7, 11)]
    for c, p in cases:
        N = c + 1
        dim = len(basis_positions(N))
        trials = 60 if N <= 5 else 15
        for _ in range(trials):
            x = tuple(rng.randrange(p) for _ in range(dim))
            y = tuple(rng.randrange(p) for _ in range(dim))
            want = to_vec(mlog(mul(mexp(to_mat(x, N, p), p), mexp(to_mat(y, N, p), p), p), p), N, p)
            assert bch(x, y, N, p) == want, (c, p, x, y)
        out(f" c={c} p={p}: {trials} random pairs agree (boundary p=c+1: {p == c + 1})")

    # Understated class is wrong (documented in the docstring): class-3 algebra, c=2 passed.
    N, p = 4, 5
    dim = len(basis_positions(N))
    bad = 0
    for _ in range(40):
        x = tuple(rng.randrange(p) for _ in range(dim))
        y = tuple(rng.randrange(p) for _ in range(dim))
        lo = bch_via_ode(x, y, prime=p, nilpotency_class=2, bracket=make_bracket(N, p, [0]))
        bad += lo != bch(x, y, N, p)
    out(f" control: class-3 algebra evaluated with c=2 is wrong on {bad}/40 pairs (must be >0)")
    assert bad > 0

    # (ii) four-pass clean map |u>|v> -> |u>|u*v> on canonical pairs, exhaustive.
    out("== (ii) clean |u>|v> -> |u>|u*v> by two XOR evaluators (4 BCH passes)")
    for N, p in [(3, 3), (3, 5), (4, 5)]:
        dim = len(basis_positions(N))
        elems = list(itertools.product(range(p), repeat=dim))
        pairs = itertools.product(elems, elems) if len(elems) <= 125 else (
            (tuple(rng.randrange(p) for _ in range(dim)), tuple(rng.randrange(p) for _ in range(dim)))
            for _ in range(3000))
        images, n_pairs, passes_per_pair = set(), 0, set()
        for u, v in pairs:
            ctr = [0]
            passes = 0
            # registers (u, v, 0); evaluator 1: compute w=u*v (pass), XOR-copy, uncompute (pass)
            w = bch(u, v, N, p, ctr); passes += 2
            reg = [u, v, w]
            # evaluator 2: compute u^{-1}*w with u^{-1} = -u (pass), subtract into reg 1, uncompute (pass)
            uinv = tuple((-a) % p for a in u)
            back = bch(uinv, reg[2], N, p, ctr); passes += 2
            reg[1] = tuple((a - b) % p for a, b in zip(reg[1], back))
            assert reg[1] == (0,) * dim, "scratch not cleared"
            assert bch(u, uinv, N, p) == (0,) * dim
            images.add((u, reg[2]))
            passes_per_pair.add(passes)
            n_pairs += 1
        if len(elems) <= 125:
            assert len(images) == n_pairs == len(elems) ** 2  # bijection on canonical pairs
        out(f" n_{N}(F_{p}), {'all' if len(elems) <= 125 else 'sampled'} {n_pairs} pairs: "
            f"scratch cleared, passes={sorted(passes_per_pair)} (each BCH pass = {formula(N - 1)} brackets)")

    # Artifact cross-check: brackets are counted with the GRADE d of each stage, not c.
    out("== artifact rees_uniform_instrument.json: per-stage bracket accounting")
    art = json.loads((ROOT / "research/reductions/rees_uniform_instrument.json").read_text())
    for case in art["cases"]:
        rb = case["recovery_budget"]
        c = len(rb["lower_central_dimensions"])
        tot = 0
        for st in case["stages_top_down"]:
            d = st["grade"]
            assert st["bracket_calls_per_bch_pass"] == formula(d)
            assert st["bch_evaluation_passes"] == 4 * st["controlled_right_actions"]
            assert st["group_dimension"] == sum(rb["lower_central_dimensions"][:d])
            tot += st["bch_evaluation_passes"] * formula(d)
        assert tot == case["bracket_calls"]
        uniform_c = case["bch_evaluation_passes"] * formula(c)
        out(f" profile {tuple(rb['lower_central_dimensions'])} p={rb['supplied_prime']}: "
            f"brackets={case['bracket_calls']} = sum_d passes_d*B(d); "
            f"passes*B(c)={uniform_c} ({'equal' if uniform_c == tot else 'DIFFERENT: theorem (i) reads B(c), table uses B(d)'})")
        # (iv) depth-first register bound 2 + sum (M_d - 1)
        ar = [s["arity"] for s in rb["stages_top_down"]]
        df = 2 + sum(a - 1 for a in ar) if ar else 1
        assert df == rb["depth_first_group_register_bound"], (df, rb["depth_first_group_register_bound"])
        out(f"   (iv) arities {ar}: 2+sum(M_d-1)={df} matches artifact")

    text = "\n".join(lines)
    print(text)
    (Path(__file__).with_suffix(".out")).write_text(text + "\n")


if __name__ == "__main__":
    main()

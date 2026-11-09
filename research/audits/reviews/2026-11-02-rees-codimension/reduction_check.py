"""Lie-level falsifier hunt for Sections 1-4 of research/BOUNDED_CODIMENSION_HSP_REDUCTION.md.

For random nilpotent matrix Lie algebras L <= n_N(F_p) (class <= N-1 < p), filiform algebras of
large class, and random subalgebras h of codimension <= k, run the whole reduction:
  Section 1: maximal abelian ideal A with random choices; check A abelian, ideal, flag
             [L,A_i] <= A_{i-1}, C_L(A) = A, dim L <= a(a+1)/2, class L <= 2a-1.
  Section 2: if a > k: K = h cap A (truth; the quantum step is an abelian HSP),
             dim K >= a-k > 0, h <= S = N_L(K), K ideal of S, codim_{S/K}(h/K) = codim h - (n - dim S),
             class(S/K) <= class(L), dim strictly decreases.
  Section 3: linear section with RANDOM complement; recovered h = sigma(h/K) + K.
  Section 4: terminal (abelian, k = 0, or a <= k): if nonabelian, dim <= k(k+1)/2,
             class <= 2k-1, every Rees label rank a_d = g_d - dim(h cap gamma_d) <= k,
             and total steps <= n.
Two policies for k: the fixed initial promise, and the updated bound k - (n - dim S).
Exact arithmetic throughout. Run: /opt/anaconda3/bin/python reduction_check.py [trials]
"""
import random
import sys
from collections import defaultdict
from codim_lib import (Lie, random_upper_triangular_algebra, filiform, span_basis, rank,
                       intersect, in_span, coords, lin, unit, rand_vec)

STATS = defaultdict(int)
TERM = defaultdict(lambda: (0, 0))      # k -> max (dim, class) of nonabelian terminals
FAIL = []


def fail(msg, ctx):
    FAIL.append((msg, ctx))


def flag_ok(L, A):
    p, n = L.p, L.n
    for i, x in enumerate(A):
        for b in range(n):
            if not in_span(L.br(unit(b, n), x), A[:i], p, n):
                return False
    return True


def reduce(L, h, k, rng, policy, ctx, depth=0):
    """Returns (recovered basis of h, steps). h is the truth at this level."""
    p, n = L.p, L.n
    if n == 0:
        return [], 0
    codim = n - rank(h, p, n)
    if codim > k:
        fail("codim promise violated at depth %d" % depth, ctx)
    if k == 0:
        STATS['term_k0'] += 1
        return L.basis(), 0
    if not L.bracket_span(L.basis(), L.basis()):
        STATS['term_abelian'] += 1
        return span_basis(h, p, n), 0
    A = L.max_abelian_ideal(rng)
    a = len(A)
    cls = L.nil_class()
    STATS['ideals'] += 1
    if any(L.br(x, y) != (0,) * n for x in A for y in A):
        fail("A not abelian", ctx)
    if not flag_ok(L, A):
        fail("flag property fails", ctx)
    C = L.centralizer(A)
    if rank(C, p, n) != a or rank(list(C) + A, p, n) != a:
        fail("A not self-centralizing", ctx)
    if n > a * (a + 1) // 2:
        fail("dim L > a(a+1)/2", ctx)
    if cls > 2 * a - 1:
        fail("class L > 2a-1", ctx)
    if a <= k:
        STATS['term_small'] += 1
        if n > k * (k + 1) // 2 or cls > 2 * k - 1:
            fail("terminal size bound", ctx + (n, cls, k))
        g = L.lcs()
        for d, gd in enumerate(g, start=1):
            ad = len(gd) - len(intersect(h, gd, p, n))
            if ad > k:
                fail("a_d > k at terminal", ctx)
        dm, cm = TERM[k]
        TERM[k] = (max(dm, n), max(cm, cls))
        return span_basis(h, p, n), 0
    K = intersect(h, A, p, n)
    if len(K) < a - k or len(K) == 0:
        fail("dim K < a-k", ctx)
        return None, 0
    S = L.normalizer(K)
    if not all(in_span(x, S, p, n) for x in h):
        fail("h not in N(K)", ctx)
    if not all(in_span(L.br(s, x), K, p, n) for s in S for x in K):
        fail("K not ideal of S", ctx)
    Q, sig = L.quotient(S, K, rng, random_section=True)
    full = sig + list(K)
    hQ = span_basis([coords(x, full, p)[:len(sig)] for x in h], p, Q.n)
    d = n - len(S)
    codimQ = Q.n - len(hQ)
    if codimQ != codim - d:
        fail("codim relation", ctx)
    if Q.n >= n:
        fail("no dimension decrease", ctx)
    if not Q.check():
        fail("quotient not a Lie algebra", ctx)
    if Q.n and Q.nil_class() > cls:
        fail("quotient class grew", ctx)
    if not Q.is_subalgebra(hQ):
        fail("h/K not subalgebra", ctx)
    STATS['abelian_calls'] += 1
    k2 = k if policy == 'fixed' else k - d
    rec, steps = reduce(Q, hQ, k2, rng, policy, ctx, depth + 1)
    if rec is None:
        return None, steps + 1
    lifted = span_basis([lin(v, sig, p, n) for v in rec] + list(K), p, n)
    return lifted, steps + 1


def same_space(U, W, p, n):
    return rank(U, p, n) == rank(W, p, n) == rank(list(U) + list(W), p, n)


def random_h(L, j, rng):
    """Closure of n-j random vectors: a subalgebra of codim <= j."""
    p, n = L.p, L.n
    return L.closure([rand_vec(p, n, rng) for _ in range(max(0, n - j))])


def run_case(L, h, rng, ctx):
    p, n = L.p, L.n
    codim = n - rank(h, p, n)
    for k in sorted({codim, codim + 1}):
        for policy in ('fixed', 'updated'):
            rec, steps = reduce(L, h, k, rng, policy, ctx + (k, policy))
            STATS['runs'] += 1
            if rec is None or not same_space(rec, h, p, n):
                fail("recovery mismatch", ctx + (k, policy))
            if steps > n:
                fail("too many steps", ctx)


def main():
    trials = int(sys.argv[1]) if len(sys.argv) > 1 else 300
    rng = random.Random(4)
    cases = 0
    # filiform family with assorted subalgebras, large class
    for m in (6, 9, 12):
        p = {6: 7, 9: 11, 12: 13}[m]
        L = filiform(m, p)
        hs = [[unit(i, m) for i in range(1, m - 1)],                     # remark's h
              [unit(0, m)] + [unit(i, m) for i in range(2, m)],          # codim 1
              [unit(0, m), unit(m - 1, m)],                               # abelian subalgebra
              [unit(i, m) for i in range(3, m)]]                         # ideal, codim 3
        for _ in range(6):
            hs.append(random_h(L, rng.randrange(1, 5), rng))
        for h in hs:
            run_case(L, span_basis(h, p, m), rng, ('filiform', m, p))
            cases += 1
    # random matrix algebras
    for t in range(trials):
        N = rng.choice([3, 4, 5, 5, 6, 6, 7])
        p = rng.choice([q for q in (7, 11, 13) if q >= N])
        L, _ = random_upper_triangular_algebra(N, rng.randrange(2, 5), p, rng)
        if L is None or L.n < 2 or L.n > 16:
            continue
        for _ in range(2):
            h = random_h(L, rng.randrange(1, 6), rng)
            run_case(L, h, rng, ('ut', N, p, L.n, t))
            cases += 1
    print(f"cases (L,h): {cases}; runs (k, policy): {STATS['runs']}")
    print(f"ideal constructions: {STATS['ideals']}; abelian-HSP steps: {STATS['abelian_calls']}")
    print(f"terminals: abelian {STATS['term_abelian']}, k=0 {STATS['term_k0']}, "
          f"nonabelian a<=k {STATS['term_small']}")
    print("max nonabelian terminal (dim, class) observed per k vs bound (k(k+1)/2, 2k-1):")
    for k in sorted(TERM):
        print(f"  k={k}: observed {TERM[k]}  bound {(k * (k + 1) // 2, 2 * k - 1)}")
    print(f"failures: {len(FAIL)}")
    for f in FAIL[:20]:
        print("  ", f)


if __name__ == "__main__":
    main()

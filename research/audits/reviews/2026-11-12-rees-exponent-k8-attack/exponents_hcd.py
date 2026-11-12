#!/opt/anaconda3/bin/python
"""Exponent of m with the half-degree collision descent (rule R6 = R5 + HCD).  Finite exact computation.

R5 is imported read-only from ../2026-11-12-rees-exponent-discharge/exponents.py (law-free all-prime
rule of that note).  R6(kappa, p) = min(R5, HCD) where, for even kappa and D = kappa/2 (Theorem HC of
2026-11-12-rees-exponent-k8-attack.md), HCD = min over s >= 1 of s*R6(D, p) + finish, with finish:
  F0: 0 in Tn_s (a nontrivial P-weighted zero sum of the 2^s rep ratios)          -> + 0
  F1: Tn_s contains F_p^*  (Gaussian elimination on a+1 objects)                   -> + 1
  F2: rho*P_{D'} subset of Tn_s for a divisor D' < kappa (a D'-solver on objects)   -> + R6(D', p)
  F3: a two-level union step RC(kappa; Z_kappa -> K) exists with K + c subset of the classes of Tn_s
                                                                                     -> + 2
T_s / Tn_s = all / nontrivial sums sum_k y_k c_k, y in (P u 0)^{R_s}; R_0 = {1}, R_{s+1} = R_s u eps R_s,
eps = -omega^{-1}, omega in P_D \\ P_kappa.
Only applied where R5 >= 5 (HCD >= 3 always; this avoids union-step searches at large p).
"""
import sys, os, math, functools, itertools
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), '2026-11-12-rees-exponent-discharge'))
import exponents as X   # read-only import; its main() is not run

PMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 30000


@functools.lru_cache(None)
def classes(p, k):
    g = X.primitive_root(p)
    ind, x = {}, 1
    for e in range(p - 1):
        ind[x] = e % k
        x = x * g % p
    return g, ind


NODE_CAP = 100_000
UNDECIDED = []


@functools.lru_cache(None)
def union_step_exists(p, k, K):
    """Exhaustive backtracking (exact): alpha_j + beta_i in {0} u U_{m in K} Q_{m-i-j}, A(0,0) != 0.
    If the search exceeds NODE_CAP nodes it is abandoned and treated as NON-existent (conservative:
    only upper bounds on exponents are claimed); such cases are listed in UNDECIDED."""
    g, ind = classes(p, k)
    full = (1 << p) - 1
    cls_mask = [0] * k
    for x, e in ind.items():
        cls_mask[e] |= 1 << x
    def allowed(i, j):
        m = 1  # value 0 allowed
        for kk in K:
            m |= cls_mask[(kk - i - j) % k]
        return m
    A = [[allowed(i, j) for j in range(k)] for i in range(k)]
    def shift(mask, b):  # {x : x + b in mask} = mask rotated by -b
        b %= p
        return ((mask >> b) | (mask << (p - b))) & full
    X0 = [A[0][j] for j in range(k)]
    X0[0] &= ~1
    cnt = [0]
    class Cap(Exception):
        pass
    def rec(i, Xs):
        if i == k:
            return True
        cnt[0] += 1
        if cnt[0] > NODE_CAP:
            raise Cap
        for b in range(p):
            Y = []
            for j in range(k):
                y = Xs[j] & shift(A[i][j], b)
                if not y:
                    break
                Y.append(y)
            else:
                if rec(i + 1, Y):
                    return True
        return False
    try:
        return rec(1, X0)
    except Cap:
        UNDECIDED.append((p, k, K))
        return False


def r5(k, p):
    if k == 1:
        return 1
    return X.e_grade('R5', p, k)   # e_grade uses gcd(d, p-1) = k for k | p-1


@functools.lru_cache(None)
def r6(k, p, detail=False):
    base = r5(k, p)
    best, how = base, 'R5'
    if k % 2 or base < 5:
        return (best, how) if detail else best
    Dh = k // 2
    eD = r6(Dh, p)
    g, ind = classes(p, k)
    P = {x for x, e in ind.items() if e == 0}
    # omega: element of P_{k/2} not in P_k, i.e. class k/2
    omega = next(x for x, e in ind.items() if e == k // 2)
    eps = (-pow(omega, p - 2, p)) % p
    T, Tn = P | {0}, set(P)
    for s in range(1, 8):
        cost = s * eD
        if cost >= best:
            break
        T, Tn = ({(x + eps * y) % p for x in T for y in T},
                 {(x + eps * y) % p for x in Tn for y in T} | {(x + eps * y) % p for x in T for y in Tn})
        cand = []
        if 0 in Tn:
            cand.append((cost, f'HCD s={s} F0'))
        if len(Tn - {0}) == p - 1:
            cand.append((cost + 1, f'HCD s={s} F1'))
        C = {ind[x] for x in Tn if x}
        for Dp in range(2, k):
            if k % Dp == 0:
                cp = {(m * Dp) % k for m in range(k // Dp)}   # classes of P_{D'} inside Z_k
                if any({(c + m) % k for m in cp} <= C for c in range(k)):
                    cand.append((cost + r6(Dp, p), f'HCD s={s} F2 D\'={Dp}'))
        if cost + 2 < best:
            for c in sorted(C):
                Kt = tuple(sorted({(m - c) % k for m in C}))
                if union_step_exists(p, k, Kt):
                    cand.append((cost + 2, f'HCD s={s} F3 K={Kt}'))
                    break
        for v, h in cand:
            if v < best:
                best, how = v, h
    return (best, how) if detail else best


def E(rule, c, p):
    f = r5 if rule == 'R5' else r6
    return 1 + sum(f(math.gcd(d, p - 1), p) for d in range(2, c + 1))


if __name__ == '__main__':
    P = [q for q in X.primes_upto(PMAX) if q > 2]
    print('primes 3..%d; R5 imported from exponents.py; R6 = R5 + half-degree collision descent' % PMAX)
    print('per-(kappa,p) improvements (R5 -> R6) at primes where R5 >= 5:')
    for k in (4, 6, 8):
        for p in P:
            if (p - 1) % k == 0 and r5(k, p) >= 5:
                v, h = r6(k, p, True)
                print(f'  kappa={k} p={p}: R5={r5(k, p)} R6={v} via {h}')
    for rule in ('R5', 'R6'):
        row = []
        for c in range(2, 10):
            best, arg = max((E(rule, c, p), p) for p in P if p > c)
            row.append(f'{best}(p={arg})')
        print(f'{rule:3s}', ' '.join(row))
    vals = sorted(((E('R6', 9, p), p) for p in P if p > 9), reverse=True)[:12]
    print('c=9 R6 top primes:', vals)
    bp = vals[0][1]
    print('c=9 R6 argmax p=%d e_d =' % bp, [r6(math.gcd(d, bp - 1), bp) for d in range(2, 10)],
          'kappa_d =', [math.gcd(d, bp - 1) for d in range(2, 10)])
    for p in (41, 73, 17, 19, 37, 31, 13, 2521):
        print(f'c=9 p={p}: R5={E("R5", 9, p)} R6={E("R6", 9, p)} e_d(R6)=',
              [r6(math.gcd(d, p - 1), p) for d in range(2, 10)])

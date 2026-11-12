#!/opt/anaconda3/bin/python
"""Core-standard rule S1H: Schedule 1 at zero-sum depth (T1 of the discharge note) + half-degree collision
descent whose inner solvers are again S1H, with finishes F0 / F1 / F2 only (no Schedule 2, no union steps,
no E_2 data).  Inputs: the IS import (as thm:main), Gaussian elimination, and the Weil bound for diagonal
curves (used only to certify F1 at large p).  Finite exact computation + analytic tail.

  S1H(1) = 1;  S1H(k) = min( S1t(k), HCD(k) ),  S1t(k) = k*ceil(log2 t(p,k))  (t = p if k = p-1),
  HCD(k) (k even, D = k/2) = s*S1H(D) + finish, finishes F0 (+0), F1 (+1), F2 (+S1H(D')).
If p + 1 - (k-1)(k-2)sqrt(p) > 3k, every eta != 0 is u^k + eps v^k with uv != 0 (Weil), so s = 1 with F1
works and is optimal among HCD options: HCD = S1H(D) + 1.  Otherwise the sets T_s, Tn_s are computed exactly.
"""
import sys, os, math, functools, itertools
HERE = os.path.dirname(os.path.abspath(__file__))
ARGV = sys.argv[:]; sys.argv = sys.argv[:1]
sys.path.insert(0, HERE)
import exponents_hcd as H
sys.argv = ARGV
X = H.X
PMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 30000
PBIG = int(sys.argv[2]) if len(sys.argv) > 2 else 3000000


def s1t(k, p):
    return 1 if k == 1 else X.e_grade('S1t', p, k)


def weil(p, k):
    return p + 1 - (k - 1) * (k - 2) * math.sqrt(p) > 3 * k


@functools.lru_cache(None)
def s1h(k, p, detail=False):
    base = s1t(k, p)
    best, how = base, 'S1t'
    if k % 2 == 0:
        eD = s1h(k // 2, p)
        if weil(p, k) and k < p - 1:
            if eD + 1 < best:
                best, how = eD + 1, 'HCD s=1 F1 (Weil)'
        else:
            g, ind = H.classes(p, k)
            P = {x for x, e in ind.items() if e == 0}
            omega = next(x for x, e in ind.items() if e == k // 2)
            eps = (-pow(omega, p - 2, p)) % p
            T, Tn = P | {0}, set(P)
            for s in range(1, 6):
                cost = s * eD
                if cost >= best:
                    break
                eT, eTn = {eps * y % p for y in T}, {eps * y % p for y in Tn}
                T, Tn = ({(x + y) % p for x in T for y in eT},
                         {(x + y) % p for x in Tn for y in eT} | {(x + y) % p for x in T for y in eTn})
                cands = []
                if 0 in Tn:
                    cands.append((cost, f'HCD s={s} F0'))
                if len(Tn - {0}) == p - 1:
                    cands.append((cost + 1, f'HCD s={s} F1'))
                C = {ind[x] for x in Tn if x}
                for Dp in range(2, k):
                    if k % Dp == 0:
                        cp = {(m * Dp) % k for m in range(k // Dp)}
                        if any({(c + m) % k for m in cp} <= C for c in range(k)):
                            cands.append((cost + s1h(Dp, p), f'HCD s={s} F2 D\'={Dp}'))
                for v, h in cands:
                    if v < best:
                        best, how = v, h
    return (best, how) if detail else best


def E(f, c, p):
    return 1 + sum(f(math.gcd(d, p - 1), p) for d in range(2, c + 1))


if __name__ == '__main__':
    P = [q for q in X.primes_upto(PMAX) if q > 2]
    for name, f in (('S1t', s1t), ('S1H', s1h)):
        row = []
        for c in range(2, 10):
            best, arg = max((E(f, c, p), p) for p in P if p > c)
            row.append(f'{best}(p={arg})')
        print(f'{name:4s} p<={PMAX}:', ' '.join(row))
    top = sorted(((E(s1h, 9, p), p) for p in P if p > 9), reverse=True)[:10]
    print('c=9 S1H top primes:', top)
    for v, p in top[:3] + [(None, 2521), (None, 41)]:
        print(f'  p={p}: e_d =', [s1h(math.gcd(d, p - 1), p, True) for d in range(2, 10)],
              'kappa_d =', [math.gcd(d, p - 1) for d in range(2, 10)], 'E =', E(s1h, 9, p))
    big = [q for q in X.primes_upto(PBIG) if q > PMAX]
    for c in (8, 9):
        vb = max((E(s1h, c, p), p) for p in big)
        print(f'c={c} S1H max over primes in ({PMAX}, {PBIG}]: {vb}  (all kappa <= 9 satisfy the Weil test there)')
    print('analytic tail: for p > 30000 and kappa <= 9, t <= 3 and the Weil test holds, so S1H(k) depends only on')
    print('the parities of (p-1)/k; the residue classes are all realised below 3e6 (see max above).')

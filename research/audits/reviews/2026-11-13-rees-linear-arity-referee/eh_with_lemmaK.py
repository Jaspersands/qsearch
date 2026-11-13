"""What would Lemma K + prop:triangular-sde do to the core's E_H(c)?

Degree-only recursion of Definition def:schedule1h (core), with ONE extra candidate:
at kappa = 3 (every p = 1 mod 3) the triangular solver of degree 2 (Lemma K).
Reuses, read-only, Field / t_len / T_sequence of the applied 38 calculator
(research/audits/reviews/2026-11-13-rees-headline-38-applied/halved_schedule.py).
Control: with the extra candidate switched off it must reproduce E_H(c) = 3,6,10,14,20,25,29,38.

Usage: /opt/anaconda3/bin/python eh_with_lemmaK.py
"""
import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "2026-11-13-rees-headline-38-applied"))
import halved_schedule as hs  # noqa: E402

SMALL = 4 * 9 ** 4


def degrees(p, use_K):
    F = hs.Field(p) if p < SMALL else None
    e = {}
    for kappa in range(1, 10):
        if (p - 1) % kappa:
            continue
        if kappa == 1:
            e[1] = 1
            continue
        t = hs.t_len(F, kappa) if F is not None else (2 if ((p - 1) // kappa) % 2 == 0 else 3)
        best = kappa * math.ceil(math.log2(t))
        if use_K and kappa == 3:
            best = min(best, 2)
        if kappa % 2 == 0:
            D = kappa // 2
            if p >= 4 * kappa ** 4:
                cand = [(1, 'F1')]
            else:
                cand = []
                for s, T in enumerate(hs.T_sequence(F, kappa, 40), start=1):
                    if T[1]:
                        cand.append((s, 'F0'))
                    if len(T[0]) == kappa:
                        cand.append((s, 'F1'))
            for s, fin in cand:
                best = min(best, s * e[D] + (fin == 'F1'))
        e[kappa] = best
    return e


_CACHE = {}


def EH(c, use_K, primes):
    best, arg = 0, []
    for p in primes:
        if p <= c:
            continue
        if (p, use_K) not in _CACHE:
            _CACHE[(p, use_K)] = degrees(p, use_K)
        e = _CACHE[(p, use_K)]
        tot = 1 + sum(e[math.gcd(d, p - 1)] for d in range(2, c + 1))
        if tot > best:
            best, arg = tot, [p]
        elif tot == best:
            arg.append(p)
    return best, arg


def main():
    small = [p for p in hs.PRIMES if p < SMALL]
    # large-prime representatives: one prime >= 26244 in each unit class mod 2*lcm(1..9) = 5040
    N = 5040
    reps = {}
    q = SMALL
    while len(reps) < sum(1 for r in range(N) if math.gcd(r, N) == 1):
        q += 1
        if all(q % s for s in range(2, int(q ** 0.5) + 1)):
            reps.setdefault(q % N, q)
    large = sorted(reps.values())
    for use_K in (False, True):
        row = []
        for c in range(2, 10):
            b1, a1 = EH(c, use_K, small)
            b2, a2 = EH(c, use_K, large)
            row.append((c, max(b1, b2), (a1[:4] if b1 >= b2 else []) + (a2[:2] if b2 >= b1 else [])))
        tag = "with Lemma K (kappa=3 degree 2)" if use_K else "core Schedule 1H (control)"
        print(tag)
        for c, v, a in row:
            print(f"   c={c}: E_H = {v}   attained at (first few) {a}")
        sys.stdout.flush()


if __name__ == "__main__":
    main()

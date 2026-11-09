"""Brute-force cross-check of good_threshold.scan_prime (no normalisation, no FFT)."""
import itertools

from common import F, is_prime
import good_threshold as gt


def bf(p, k, E):
    Fd = F(p, k)
    gmin = None
    for e in range(2, E + 1):
        for cl in itertools.product(range(k), repeat=e):
            if len(set(cl)) < 2:
                continue
            need = [(-c) % k for c in cl]
            for beta in itertools.permutations(range(p), e):
                n = 0
                for s in range(p):
                    if all(((b + s) % p == 0) or Fd.cls(b + s) == c for b, c in zip(beta, need)):
                        n += 1
                gmin = n if gmin is None else min(gmin, n)
    return gmin


if __name__ == "__main__":
    bad = 0
    for (k, E, pmax) in [(2, 3, 23), (3, 3, 31), (2, 4, 13), (4, 3, 17)]:
        for p in range(3, pmax + 1):
            if not is_prime(p) or (p - 1) % k:
                continue
            g1 = bf(p, k, E)
            ex, g2, _ = gt.scan_prime(p, k, E)
            ok = ((g1 == 0) == ex) and (ex or g1 == g2)
            bad += not ok
            print(f"k={k} E={E} p={p} brute_gmin={g1} scan=({ex},{g2}) {'OK' if ok else 'MISMATCH'}", flush=True)
    print("mismatches:", bad)

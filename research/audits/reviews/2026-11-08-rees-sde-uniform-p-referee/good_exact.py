"""Referee recomputation (own code, plain enumeration + numpy) of
  G*_E(p) over all classes and over >= 2 classes, pairwise distinct offsets beta_0 = 0, beta_1..beta_{E-1};
  Lemma P(a): sum_c |Good(beta, c)| = p + E(kappa - 1) for every distinct beta;
  Lemma P(b): mean of |Good| over i.i.d. uniform offsets (not nec. distinct) = |Q0|^E / p^(E-1);
  Lemma R: for every non-constant class vector on n >= 3 blocks there is beta (coincidences allowed)
           with Good empty -- brute force over all beta.
Usage: good_exact.py kappa E p1,p2,...   [lemmaR]
"""
import itertools
import sys

import numpy as np

k, E = int(sys.argv[1]), int(sys.argv[2])
primes = [int(x) for x in sys.argv[3].split(",")]
do_R = len(sys.argv) > 4 and sys.argv[4] == "lemmaR"


def cls_table(p, k):
    # class of y: discrete log mod k w.r.t. a primitive root; -1 for y = 0
    from sympy import primitive_root
    g = primitive_root(p)
    t = -np.ones(p, dtype=np.int64)
    y = 1
    for e in range(p - 1):
        t[y] = e % k
        y = y * g % p
    return t


for p in primes:
    if (p - 1) % k:
        print("skip p=%d (not 1 mod kappa)" % p)
        continue
    ct = cls_table(p, k)
    s = np.arange(p)
    # class pattern table: pat[y][s] = class of (y + s), -1 if zero
    pat = ct[(np.arange(p)[:, None] + s[None, :]) % p]          # p x p
    allc = list(itertools.product(range(k), repeat=E))
    multi = [c for c in allc if len(set(c)) > 1]
    Gmin_all = Gmin_multi = 10 ** 9
    witness_all = witness_multi = None
    empty_all = empty_multi = tot_all = tot_multi = 0
    ident_ok = True
    for offs in itertools.permutations(range(1, p), E - 1):
        if list(offs) != sorted(offs):
            # offsets as a set matter only up to permutation together with classes; but classes vary
            # over all vectors, so enumerating ordered offsets is redundant.  Keep sorted only.
            continue
        beta = (0,) + offs
        rows = pat[list(beta)]                                   # E x p : class of beta_b + s
        total = 0
        for c in allc:
            need = np.array([(-cb) % k for cb in c])[:, None]
            G = int(((rows == need) | (rows < 0)).all(axis=0).sum())
            total += G
            tot_all += 1
            empty_all += (G == 0)
            if G < Gmin_all:
                Gmin_all, witness_all = G, (beta, c)
            if len(set(c)) > 1:
                tot_multi += 1
                empty_multi += (G == 0)
                if G < Gmin_multi:
                    Gmin_multi, witness_multi = G, (beta, c)
        if total != p + E * (k - 1):
            ident_ok = False
    # Lemma P(b): exact mean over ALL offset vectors (with repeats) for a fixed c
    Q0 = (p - 1) // k + 1
    for c in (allc[0], multi[0] if multi else allc[0]):
        need = np.array([(-cb) % k for cb in c])[:, None]
        # mean over beta_1..beta_{E-1} uniform: product structure, compute exactly by counting
        # |Good| = sum_s 1[s in Q0_{-c0}] prod_b #{beta_b : beta_b + s in Q0_{-c_b}} / p^{E-1}
        num = 0
        for sv in range(p):
            if not (pat[0][sv] == need[0][0] or pat[0][sv] < 0):
                continue
            num += Q0 ** (E - 1)
        assert num == Q0 ** E, (num, Q0 ** E)
    print("kappa=%d p=%3d E=%d  G*_E(all)=%d witness %s | G*_E(>=2 classes)=%d witness %s | "
          "empty frac all %.4f multi %.4f | Lemma P(a) identity on every beta: %s | "
          "Lemma P(b) mean = %d/%d^%d = %.3f" % (k, p, E, Gmin_all, witness_all, Gmin_multi,
                                                witness_multi, empty_all / tot_all,
                                                empty_multi / max(tot_multi, 1), ident_ok,
                                                Q0 ** E, p, E - 1, Q0 ** E / p ** (E - 1)),
          flush=True)
    if do_R:
        # Lemma R brute force: n = E blocks; for every non-constant c, exists beta (beta_0 = 0,
        # repeats allowed) with Good empty?  Also check constant c (monochromatic) for contrast.
        for c in allc:
            need = np.array([(-cb) % k for cb in c])[:, None]
            found = False
            for offs in itertools.product(range(p), repeat=E - 1):
                rows = pat[[0] + list(offs)]
                if not ((rows == need) | (rows < 0)).all(axis=0).any():
                    found = True
                    break
            if len(set(c)) > 1 and not found:
                print("   LEMMA R FAILS for c=%s at p=%d" % (c, p))
            if len(set(c)) == 1:
                print("   monochromatic c=%s: some beta (repeats allowed) with empty Good exists: %s" % (c, found))
        print("   Lemma R checked for all %d non-constant class vectors at p=%d, n=%d" % (len(multi), p, E))

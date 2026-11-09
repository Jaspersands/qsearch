"""Mutation tests for rtf_check.py (do the checks have teeth?) and two extra checks.
  m1 frozen normalizer: S' = S instead of I_S(K')            -> expect a failure on nonabelian rings
  m2 socle tensor without the division by p^{a_k-1}           -> expect a hiding failure when the socle
                                                                 bracket lands in p^{a-1}u with a > 1
  m3 non-homomorphic section: sigma(t) + k(t), k(t) in K random -> lem:tb-quotient-oracle: must PASS
  gap: write GAP files with the regular permutation representation of (L,*) to count subgroups
"""
import sys, random, json, itertools
import numpy as np
sys.path.insert(0, ".")
import rtf_check as RC


def run(ring_name, mutant):
    rng = random.Random(7)
    L = [r for r in RC.rings() if ring_name in r.name][0]
    orig_ideal, orig_socle, orig_present = RC.idealizer, RC.socle, RC.present_section
    if mutant == "m1":
        def frozen(L_, S, K):
            I, X, ok = orig_ideal(L_, S, K)
            return S, X, ok   # keep the true normalizer test data: only downstream invariants can fail
        RC.idealizer = frozen
    if mutant == "m2":
        def socle_nodiv(L_, dk, us, coord):
            a, T = orig_socle(L_, dk, us, coord)
            p = L_.p
            k = len(dk)
            sb = [L_.red(u * (p ** (ai - 1))) for u, ai in zip(us, a)]
            T2 = np.zeros_like(T)
            for i in range(k):
                for j in range(k):
                    t = coord(L_.br(sb[i], sb[j]))
                    for kk in range(k):
                        T2[i, j, kk] = t[kk] % p
            return a, T2
        RC.socle = socle_nodiv
    if mutant == "m3":
        def present_rand(L_, S, K):
            dk, us, coord, sigma = orig_present(L_, S, K)
            Kel = L_.elements(K)
            def sigma2(T):
                X = sigma(T)
                h = [hash(tuple(int(v) for v in t)) % len(Kel) for t in T]
                return L_.red(X + Kel[h])
            return dk, us, coord, sigma2
        RC.present_section = present_rand
    st = RC.Stats()
    subs = RC.all_subrings(L)
    fails = 0
    first = None
    for Hh in subs:
        lab = RC.coset_labels(L, Hh)
        try:
            Kout, calls, valid = RC.rtf(L, Hh, lab, "truth", rng, st)
            if Kout != Hh:
                raise AssertionError("wrong output")
        except AssertionError as ex:
            fails += 1
            if first is None:
                first = str(ex)
    RC.idealizer, RC.socle, RC.present_section = orig_ideal, orig_socle, orig_present
    return dict(ring=L.name, mutant=mutant, subrings=len(subs), failures=fails, first_failure=first)


def gapfile(ring_name, path):
    L = [r for r in RC.rings() if ring_name in r.name][0]
    gens = []
    for i in range(L.m):
        g = np.zeros(L.m, dtype=np.int64)
        g[i] = 1
        Y = L.bch(g[None, :], L.all)      # left multiplication x -> g * x
        gens.append([int(v) + 1 for v in L.idx(Y)])
    with open(path, "w") as fh:
        fh.write("G := Group(%s);;\n" % ",".join("PermList([%s])" % ",".join(map(str, g)) for g in gens))
        fh.write('Print("%s: |G| = ", Size(G), ", subgroups = ", Sum(ConjugacyClassesSubgroups(G), Size), "\\n");\n' % L.name)


if __name__ == "__main__":
    mode = sys.argv[1]
    if mode == "gap":
        for i, nm in enumerate(sys.argv[2:]):
            gapfile(nm, "subcount_%d.g" % i)
    else:
        for nm in sys.argv[2:]:
            print(json.dumps(run(nm, mode)))
            sys.stdout.flush()

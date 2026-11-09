# Erroneous-branch probe for lem:tb-howell-rounds: an ill-defined chart reachable when the samples of
# Lemma tb-kernel span a proper subgroup of (ker pi)^perp. Run: /opt/anaconda3/bin/python -I bad_chart.py
import os, sys, itertools, traceback, collections
here = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(here, "ref_check.py")).read().rsplit("main()", 1)[0]
for line in ['        validate_present(L, S, K, Sset, Kset, P)', '        assert setof(L, Kp) == Kp_brute, "N5"',
             '        assert setof(L, Sp) == brute, "N6 idealizer"', '        assert eq == (Sset == Kset)']:
    assert src.count(line) == 1; src = src.replace(line, '        pass')   # brute checks assume a Lie ring
sys.argv = [sys.argv[0], "0"]; exec(src)
# F = F_{2,2} over Z/9 (X1, X2, X3 = [X1,X2]), G = (F,*), ker pi = 0. Samples Y spanning {(a,3b,c)}:
Y = [[1, 0, 0], [0, 3, 0], [0, 0, 1]]
Yu = lambda u: tuple(sum(Y[r][j] * u[j] for j in range(3)) % 9 for r in range(3))
brF = lambda u, v: [0, 0, (u[0] * v[1] - u[1] * v[0]) % 9]
kerY = [u for u in itertools.product(range(9), repeat=3) if Yu(u) == (0, 0, 0)]
print("|ker Y| =", len(kerY), "; ker Y an ideal of F:",
      all(Yu(brF(list(u), list(v))) == (0, 0, 0) for u in kerY for v in itertools.product(range(9), repeat=3)))
print("chart: eps = Y X1 (order 9), Y X2 (order 3), Y X3 (order 9); [eps1,eps2] = Y X3 = eps3,",
      "so 3*c_12^3 = 3 != 0 mod 9: constants ill-defined")
class Raw(LieRing):
    def __init__(self, Z, es, c): self.Z, self.es, self.m, self.c = Z, es, len(es), c
c = {}; put(c, 3, 0, 1, [0, 0, 1]); L = Raw(Zpe(3, 2), [2, 1, 2], c)
where = collections.Counter(); ok = 0
for seed in range(400):
    rng.seed(seed)
    try: rtf(L, {tuple(rng.choice(L.elements())), (0, 0, 0)}, "random"); ok += 1
    except AssertionError:
        where[traceback.extract_tb(sys.exc_info()[2])[-1].name] += 1
print("random-oracle RtF runs completed:", ok, "; invariant K <= S or a step precondition failed:", dict(where))

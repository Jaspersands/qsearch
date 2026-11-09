"""Tower checker: end-to-end run of union chains Z_k -> K -> {0} with the report's
own step witnesses (read from 2026-11-05-rees-threshold-6/), on random and
adversarial columns. Classes by exponentiation with xi = the witness's g."""
import random
import sys
sys.path.insert(0, __file__.rsplit("/", 1)[0])
from tower_check import nullvec, final_check, column_families, Field  # noqa: E402
from sympy.ntheory.residue_ntheory import nthroot_mod  # noqa: E402

SRC = "/Users/jaspersands/Developer/qsearch/research/audits/reviews/2026-11-05-rees-threshold-6/"


def read_witness(fname, p):
    for l in open(SRC + fname):
        f = l.split()
        if f and int(f[0]) == p and f[1] == "FEASIBLE":
            g = int(f[2].split("=")[1])
            bi, ai = f.index("beta"), f.index("alpha")
            return g, [int(x) for x in f[bi + 1:ai]], [int(x) for x in f[ai + 1:]]
    raise KeyError((fname, p))


class F2(Field):
    def __init__(self, p, kappa, g):
        super().__init__(p, kappa)
        self.xi = g
        self._zeta = {}


def union_solve(F, steps, lams):
    """steps: list of (D, R, K, alpha, beta). Level-0 blocks, then each step as in the
    union-target version of the refinement lemma; designated coefficient kept of class 0."""
    p = F.p
    a = len(lams[0])
    M = len(lams)
    groups = []
    for s in range(0, M, a + 1):
        idx = list(range(s, s + a + 1))
        v = nullvec([lams[b] for b in idx], p)
        k0 = next(k for k in range(len(v)) if v[k])
        inv = pow(v[k0], p - 2, p)
        groups.append(({idx[k]: v[k] * inv % p for k in range(len(v)) if v[k]}, idx[k0]))
    for (D, R, K, alpha, beta) in steps:
        bmap = dict(zip(R, beta))
        N = (len(R) - 1) * a + 1
        new = []
        for s in range(0, len(groups), N):
            chunk = groups[s:s + N]
            V = []
            for rel, bs in chunk:
                assert F.cls(rel[bs], D) == 0
                U = {i: [0] * a for i in R}
                for b, c in rel.items():
                    i = F.cls(c, D)
                    assert i in U
                    for k in range(a):
                        U[i][k] = (U[i][k] + c * lams[b][k]) % p
                V.append([U[i][k] for i in R[1:] for k in range(a)])
            eta = nullvec(V, p)
            n0 = next(n for n in range(N) if eta[n])
            inv = pow(eta[n0], p - 2, p)
            eta = [e * inv % p for e in eta]
            out = {}
            for n, (rel, bs) in enumerate(chunk):
                if eta[n]:
                    j = F.cls(eta[n], D)
                    for b, c in rel.items():
                        v = eta[n] * (alpha[j] + bmap[F.cls(c, D)]) % p * c % p
                        if v:
                            out[b] = v
                            assert F.cls(v, D) in K
            bstar = chunk[n0][1]
            assert F.cls(out[bstar], D) == 0
            new.append((out, bstar))
        groups = new
    rel = groups[0][0]
    u = [0] * M
    for b, c in rel.items():
        assert F.in_PD(c, F.kappa)
        r = nthroot_mod(c, F.kappa, p)
        u[b] = r if isinstance(r, int) else r[0]
    return u


def run(kappa, p, s1, s2, K, a_list=(1, 2)):
    g1, b1, a1 = read_witness(s1, p)
    g2, b2, a2 = read_witness(s2, p)
    assert g1 == g2
    F = F2(p, kappa, g1)
    steps = [(kappa, list(range(kappa)), K, a1, b1), (kappa, list(K), [0], a2, b2)]
    rng = random.Random(p)
    ok = True
    for a in a_list:
        M = (a + 1) * ((kappa - 1) * a + 1) * ((len(K) - 1) * a + 1)
        for name, lams in column_families(p, a, M, rng).items():
            u = union_solve(F, steps, lams)
            ok &= final_check(F, lams, u, rng)
    print(f"union chain kappa={kappa} p={p} K={K} (witnesses {s1},{s2}): {'OK' if ok else 'FAIL'}", flush=True)


if __name__ == "__main__":
    run(4, 29, "uw_k4_K0-1_s1.out", "uw_k4_K0-1_s2.out", [0, 1])
    for p in (79, 139):
        run(6, p, "uw_k6_K0-1_s1.out", "uw_k6_K0-1_s2.out", [0, 1])
    run(8, 761, "uw_k8_K0-1_s1.out", "uw_k8_K0-1_s2.out", [0, 1], a_list=(1,))
    run(9, 271, "uw_k9_K0-4_s1.out", "uw_k9_K0-4_s2.out", [0, 4], a_list=(1,))
    run(9, 523, "uw_k9_K0-1-2_s1.out", "uw_k9_K0-1-2_s2.out", [0, 1, 2], a_list=(1,))
    for p in (31, 41, 61, 71, 101, 131, 151, 181):
        run(5, p, "u5_step1_lo.out", "u5_step2.out", [0, 1])

"""t2 check 1b: explicit failure-branch charts (Lemma tb-chart run on a Y whose rows generate a
PROPER subgroup of (ker pi)^perp, as on the failure event of Lemma tb-kernel with exact
transforms).  Prints the first chart that passes the Lie-ring check stated after
lem:tb-howell-rounds (antisymmetry, c_ii = 0, p^{e_i} c_ij^k = 0 mod p^{e_k}, Jacobi) but has
class > c; also, for e = 1 (no check at all in Theorem bb-envelope), the first chart that is not
a Lie algebra or has class > c.  Finite search; reproducible with the fixed seed.
"""
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from zmod import Ring, ZLattice, dual_generators, FreeLieZ  # noqa: E402
import check_chart as cc  # noqa: E402

cc.rng = random.Random(7)
OUT = []


def say(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    OUT.append(s)


def find(p, e, s, c, want, tries=400):
    R = Ring(p, e)
    FL = FreeLieZ(s, c)
    d = FL.d
    for _ in range(tries):
        I_lat = cc.random_ideal(FL, R, cc.rng.randrange(1, 4))
        idx, n = I_lat.index(), 0
        while idx % p == 0:
            idx //= p
            n += 1
        Ncols = dual_generators(I_lat)
        for kk in range(1, n + 1):
            Y = cc.sample_perp(Ncols, R, d, kk)
            if cc.span_order(Y, d, R.M) == p ** n:
                continue
            ch = cc.chart(R, FL, Y)
            br = cc.lie_check(R, ch["exps"], ch["c"])
            lie = bool(br)
            cls_ok = cc.chart_class(R, ch["exps"], br, c) if lie else None
            if (want == "lie_but_class" and lie and not cls_ok) or \
               (want == "any_invalid" and (not lie or not cls_ok)):
                say(f"-- (p,e,s,c)=({p},{e},{s},{c}), d={d}, Lyndon basis {FL.words}")
                say("   ker pi = I generated (with M Z^d) by", I_lat.basis(), f"; |F/I| = {p}^{n}")
                say("   Y (rows, exact-law samples generating a proper subgroup of I^perp) =", Y)
                say("   chart orders p^e_i, e_i =", ch["exps"])
                nz = {k: v for k, v in ch["c"].items() if any(v)}
                say("   nonzero structure constants c_ij =", nz)
                say("   Lie-ring check passes:", lie, "; class <= c:", cls_ok)
                if lie and not cls_ok:
                    m = len(ch["exps"])
                    E = [[1 if t == i else 0 for t in range(m)] for i in range(m)]
                    # exhibit a nonzero left-normed bracket of length c+1 on basis vectors
                    from itertools import product
                    for word in product(range(m), repeat=c + 1):
                        x = E[word[0]]
                        for t in word[1:]:
                            x = br(x, E[t])
                        if any(x):
                            say(f"   nonzero bracket of length {c + 1}: indices {word} -> {x}")
                            break
                return True
    say(f"-- (p,e,s,c)=({p},{e},{s},{c}): none found in {tries} ideals ({want})")
    return False


if __name__ == "__main__":
    find(3, 2, 2, 2, "lie_but_class")
    find(5, 2, 2, 3, "lie_but_class")
    find(3, 1, 2, 2, "any_invalid")
    find(5, 1, 2, 3, "any_invalid")
    (Path(__file__).resolve().parent / "failure_example.out").write_text("\n".join(OUT) + "\n")

"""Counts: lower bound G_E(a) of Theorem B versus the block-steered general-position
count D_J(a)+a (rem:sde-worst-case(b)) and M_J(a) (rem:sde-block-steered)."""
from functools import lru_cache


def G(E, q):
    """Fewest columns for pieces of gain <= E, each piece costing (codim+1) columns,
    to bring the codimension from q to 0 (then one more column to finish)."""
    tot = 0
    while q > 0:
        tot += q + 1
        q -= min(E, q)
    return tot + 1


@lru_cache(None)
def D(J, q):
    if q == 0:
        return 0
    return max(k + 1 + D(J, q - min(J - 1, k)) for k in range(1, q + 1))


if __name__ == "__main__":
    print("a  E  G_E(a)  G_{E-1}(a)=M_E(a)  D_E(a)+a  a^2/(2E)  (a+1)(a+2)/2")
    for a in (8, 16, 32, 64, 128, 256):
        for E in (2, 3, 4, 6, 8):
            ge = G(E, a)
            ge1 = G(E - 1, a)
            de = D(E, a) + a if a <= 64 else float("nan")
            print(f"{a:4d} {E:2d} {ge:7d} {ge1:9d} {de:9} {a*a/(2*E):9.1f} {(a+1)*(a+2)//2:7d}")


def LB(E, a):
    """Theorem B: sum over pieces at codimension q > E of (q+1), pieces gaining <= E."""
    tot, q = 0, a
    while q > E:
        tot += q + 1
        q -= E
    return tot


def check_lb():
    bad = 0
    for E in range(1, 40):
        for a in range(2 * E, 600):
            if LB(E, a) < (a * a - 4 * E * E) / (2 * E):
                bad += 1
    return bad

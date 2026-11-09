"""Item A1/A3 of research/REES_EXTENSIONS_CHECK_BRIEF.md: exact integer checks of the
Schedule 3 (random-column) bounds when the class c grows with r = dim[L,L].

Cor fpt-r takes u = r+1, so c <= u and a_d <= u-1. This script evaluates, with exact
integers, every c-dependent quantity of Thm random-column at the worst case c = u and
a_d = u-1 at every grade, for the smallest admissible prime p >= 16u^2 and for a 61-bit
prime:

  mu_d = ((h+1)^M - 1)/(h p^a)  >=  2^(8u+1) u^(2u+1)        (claimed lower bound)
  per-trial acceptance |S|/(2p^M) >= 1/(4 kappa^M)
  bank failures over the whole tree  T_tree * max_d (4/mu_d + 2p^(a-M)) <= 1/64
  log2 of the quantum leaves and classical trials per tree, divided by r log2(r+2).

It also checks the filiform family (c = r+1 exactly) and, for A3, that
p^r < (16(r+1)^2)^r is 2^O(r log(r+2)).

Run: /opt/anaconda3/bin/python a1_uniformity.py   (pure Python, a few seconds)
"""
from fractions import Fraction
from math import gcd, log2, ceil


def is_prime(n):
    if n < 2:
        return False
    for q in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        if n % q == 0:
            return n == q
    d, s = n - 1, 0
    while d % 2 == 0:
        d //= 2
        s += 1
    for a in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):  # deterministic below 3.3e24
        x = pow(a, d, n)
        if x in (1, n - 1):
            continue
        for _ in range(s - 1):
            x = x * x % n
            if x == n - 1:
                break
        else:
            return False
    return True


def next_prime(n):
    while not is_prime(n):
        n += 1
    return n


def prev_prime(n):
    while not is_prime(n):
        n -= 1
    return n


def check_r(r, p):
    u = r + 1
    c = u                      # worst case allowed by c <= r+1
    M = 4 * u
    a = u - 1                  # worst case allowed by a_d <= g_d <= r
    assert p >= 16 * u * u
    T_tree = sum(M ** j for j in range(c - 1))   # merge nodes
    P_tree = M ** (c - 1)                        # leaves
    B = ceil(log2(64 * P_tree))
    worst_beta = Fraction(0)
    mu_ok = acc_ok = True
    kmax = 1
    for d in range(2, c + 1):
        k = gcd(d, p - 1)
        kmax = max(kmax, k)
        h = (p - 1) // k
        N0 = (h + 1) ** M - 1
        # mu >= 2^(8u+1) u^(2u+1)  <=>  N0 >= h p^a 2^(8u+1) u^(2u+1)
        mu_ok &= N0 >= h * p ** a * 2 ** (8 * u + 1) * u ** (2 * u + 1)
        # |S|/(2p^M) >= 1/(4 k^M)  <=>  4 N0 k^M >= 2 p^M
        acc_ok &= 4 * N0 * k ** M >= 2 * p ** M
        beta = Fraction(4 * h * p ** a, N0) + Fraction(2, p ** (M - a))
        worst_beta = max(worst_beta, beta)
    bank_tree = T_tree * worst_beta
    bank_tree_leaves = P_tree * worst_beta
    tree_abort = Fraction(3, 64) + bank_tree     # three capped arithmetic failures + banks
    log_queries = log2(c) + log2(P_tree)         # c queries per leaf, one tree
    log_classical = log2(T_tree) + log2(4 * B) + M * log2(kmax)
    scale = r * log2(r + 2)
    return dict(r=r, p=p, mu_ok=mu_ok, acc_ok=acc_ok,
                bank_ok=bank_tree <= Fraction(1, 64),
                bank_leaves_ok=bank_tree_leaves <= Fraction(1, 64),
                abort_ok=tree_abort <= Fraction(1, 16),
                log2_bank=float(log2(bank_tree.numerator) - log2(bank_tree.denominator)),
                q_ratio=log_queries / scale, cl_ratio=log_classical / scale, B=B)


def filiform_profile(r, p):
    """Filiform: basis x, e_1..e_{r+1}, [x,e_i] = e_{i+1}.  dim [L,L] = r, class r+1."""
    n = r + 2
    # lower central series by span dimension over F_p (basis vectors are e_2..e_{r+1})
    g = []
    span = set(range(2, r + 2))          # gamma_2 = span(e_2..e_{r+1})
    while span:
        g.append(len(span))
        span = {i + 1 for i in span if i + 1 <= r + 1}   # [x, e_i] = e_{i+1}
    c = len(g) + 1
    strictly_decreasing = all(g[i] > g[i + 1] for i in range(len(g) - 1))
    return n, g, c, strictly_decreasing


def main():
    print("== A1: Schedule 3 at c = u = r+1, a_d = u-1 at every grade (worst case), exact integers")
    rows = []
    for r in list(range(1, 41)) + [60, 80, 100, 150, 200, 300]:
        u = r + 1
        for p in (next_prime(16 * u * u), 2 ** 61 - 1):
            if p < 16 * u * u:
                continue
            rows.append(check_r(r, p))
    bad = [x for x in rows if not (x['mu_ok'] and x['acc_ok'] and x['bank_ok'] and x['abort_ok'])]
    print(f" cases: {len(rows)}; failures of mu bound / acceptance / bank<=1/64 / abort<=1/16: {len(bad)}")
    print(f" bank sum with P_tree leaves (paper's looser count) <= 1/64 in all cases: "
          f"{all(x['bank_leaves_ok'] for x in rows)}")
    for x in rows:
        if x['r'] in (1, 2, 3, 5, 10, 20, 40, 100, 300):
            print(f"  r={x['r']:3d} p={x['p']:<20d} log2(tree bank failure)={x['log2_bank']:10.1f} "
                  f"B={x['B']:5d} log2(queries/tree)/(r log2(r+2))={x['q_ratio']:.3f} "
                  f"log2(classical/tree)/(r log2(r+2))={x['cl_ratio']:.3f}")
    print(f" max ratios over all r: queries {max(x['q_ratio'] for x in rows):.3f}, "
          f"classical {max(x['cl_ratio'] for x in rows):.3f}")

    print("\n== A2: filiform family attains c = r+1 (g_2 > ... > g_c >= 1)")
    for r in (1, 2, 3, 5, 8, 20):
        n, g, c, dec = filiform_profile(r, 101)
        print(f"  r={r}: dim L={n}, (g_2..g_c)={tuple(g)}, class={c}, c==r+1: {c == r + 1}, "
              f"strictly decreasing: {dec}")

    print("\n== A3: IMS regime p < 16(r+1)^2: log2(p^r) / (r log2(r+2)) with p the largest such prime")
    worst = 0.0
    for r in range(1, 301):
        p = prev_prime(16 * (r + 1) ** 2 - 1)
        ratio = r * log2(p) / (r * log2(r + 2))
        worst = max(worst, ratio)
        if r in (1, 2, 5, 10, 50, 100, 300):
            print(f"  r={r:3d} p={p:7d} ratio={ratio:.3f}")
    print(f"  max ratio over r=1..300: {worst:.3f} (bounded: log2 p < 4 + 2 log2(r+1))")


if __name__ == "__main__":
    main()

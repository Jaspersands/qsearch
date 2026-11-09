"""Route (a): look for structure in the FEASIBLE witnesses of dfs2b.

Reads every line 'FEASIBLE k=K p=P g=G ... beta=... alpha=...' from the files given
on the command line (read-only).  For each witness it
  1. re-checks all K^2 cells against the definition (A_m = Q_m u {0}, index via
     pow(y, (p-1)/K, p) compared with powers of zeta = g^((p-1)/K));
  2. counts zero cells;
  3. tests every linear "shift-scale" symmetry: (r,t) != (0,0), lambda in F_p^*, c with
        lambda*alpha_{j+t} = alpha_j + c,  lambda*beta_{i+r} = beta_i - c   for all i, j
     (these are the fixed-point ansatze of section 2 of the note);
  4. tests every "transpose" symmetry: lambda*(alpha_{i+b} + beta_{j+a}) = alpha_j + beta_i;
  5. tests whether {alpha_j} or {-beta_i} is an arithmetic or geometric progression in some
     cyclic order j -> j+t, and records the multiplicative orders of the ratios
     alpha_j/alpha_k, M_ij/M_kl (small orders would signal subgroup structure);
  6. compares the number of ratio pairs of order dividing 2K with the expectation for
     uniform random nonzero elements (sum over pairs of #{x: ord(x) | 2K}/(p-1)).
Usage: python witness_structure.py FILE [FILE ...]
"""
import re
import sys
from math import gcd
from itertools import product


def parse(files):
    pat = re.compile(r"FEASIBLE k=(\d+) p=(\d+) g=(\d+).*beta=([\d,]+) alpha=([\d,]+)")
    seen = {}
    for f in files:
        for line in open(f):
            m = pat.search(line)
            if m:
                K, p, g = int(m.group(1)), int(m.group(2)), int(m.group(3))
                beta = [int(x) for x in m.group(4).split(",")]
                alpha = [int(x) for x in m.group(5).split(",")]
                seen[(K, p)] = (g, alpha, beta)
    return seen


def index_fn(p, K, g):
    h = (p - 1) // K
    z = pow(g, h, p)
    table = {pow(z, e, p): e for e in range(K)}
    assert len(table) == K
    def ind(y):
        y %= p
        if y == 0:
            return None
        return table[pow(y, h, p)]
    return ind


def mult_order(x, p, fac):
    o = p - 1
    for q in fac:
        while o % q == 0 and pow(x, o // q, p) == 1:
            o //= q
    return o


def factor(n):
    f, q = [], 2
    while q * q <= n:
        if n % q == 0:
            f.append(q)
            while n % q == 0:
                n //= q
        q += 1
    if n > 1:
        f.append(n)
    return f


def analyse(K, p, g, alpha, beta):
    ind = index_fn(p, K, g)
    out = {}
    zeros = 0
    for i in range(K):
        for j in range(K):
            v = (alpha[j] + beta[i]) % p
            if v == 0:
                zeros += 1
                continue
            assert ind(v) == (-(i + j)) % K, (K, p, i, j)
    assert (alpha[0] + beta[0]) % p != 0
    out["zeros"] = zeros
    inv = lambda x: pow(x % p, p - 2, p)
    # 3. shift-scale symmetries
    shift = []
    for r, t in product(range(K), repeat=2):
        if (r, t) == (0, 0):
            continue
        # lambda from alpha: lambda*(alpha_{j+t} - alpha_t) = alpha_j - alpha_0
        lam = None
        ok = True
        for j in range(1, K):
            d = (alpha[(j + t) % K] - alpha[t]) % p
            e = (alpha[j] - alpha[0]) % p
            if d == 0:
                ok = ok and e == 0
                continue
            l = e * inv(d) % p
            if lam is None:
                lam = l
            elif l != lam:
                ok = False
                break
        if not ok or lam is None or lam == 0:
            continue
        c = (lam * alpha[t] - alpha[0]) % p
        if all((lam * beta[(i + r) % K] - beta[i] + c) % p == 0 for i in range(K)):
            shift.append((r, t, lam))
    out["shift_sym"] = shift
    # 4. transpose symmetries: lam*(alpha_{i+b} + beta_{j+a}) = alpha_j + beta_i
    trans = []
    for a, b in product(range(K), repeat=2):
        # alpha_j - lam*beta_{j+a} = lam*alpha_{i+b} - beta_i = const
        # lam from differences: alpha_j - alpha_0 = lam*(beta_{j+a} - beta_a)
        lam, ok = None, True
        for j in range(1, K):
            d = (beta[(j + a) % K] - beta[a]) % p
            e = (alpha[j] - alpha[0]) % p
            if d == 0:
                ok = ok and e == 0
                continue
            l = e * inv(d) % p
            if lam is None:
                lam = l
            elif l != lam:
                ok = False
                break
        if not ok or lam is None:
            continue
        c1 = (alpha[0] - lam * beta[a]) % p
        if all((lam * alpha[(i + b) % K] - beta[i] - c1) % p == 0 for i in range(K)):
            trans.append((a, b, lam))
    out["transpose_sym"] = trans
    # 5. progressions in cyclic orders j -> j + t (t a unit), on alpha and on -beta
    prog = []
    for name, vec in (("alpha", alpha), ("-beta", [(-x) % p for x in beta])):
        for t in range(1, K):
            if gcd(t, K) != 1:
                continue
            seq = [vec[(t * k) % K] for k in range(K)]
            diffs = {(seq[k + 1] - seq[k]) % p for k in range(K - 1)}
            if len(diffs) == 1:
                prog.append((name, "AP", t))
            if all(x != 0 for x in seq):
                rats = {seq[k + 1] * inv(seq[k]) % p for k in range(K - 1)}
                if len(rats) == 1:
                    prog.append((name, "GP", t))
            # GP after removing the best affine shift: seq_k - c geometric
            # (c determined by three consecutive terms)
            a0, a1, a2 = seq[0], seq[1], seq[2]
            den = (a2 - 2 * a1 + a0) % p
            if den:
                c = (a0 * a2 - a1 * a1) * inv(den) % p
                s2 = [(x - c) % p for x in seq]
                if all(s2):
                    rats = {s2[k + 1] * inv(s2[k]) % p for k in range(K - 1)}
                    if len(rats) == 1:
                        prog.append((name, "affineGP", t))
    out["progressions"] = prog
    # 6. small-order ratios among nonzero cells M_ij
    fac = factor(p - 1)
    cells = [(alpha[j] + beta[i]) % p for i in range(K) for j in range(K)]
    cells = [x for x in cells if x]
    smallord = 0
    pairs = 0
    for u in range(len(cells)):
        for v in range(u + 1, len(cells)):
            pairs += 1
            o = mult_order(cells[u] * inv(cells[v]) % p, p, fac)
            if (2 * K) % o == 0:
                smallord += 1
    nsmall = sum(1 for d in range(1, 2 * K + 1) if (2 * K) % d == 0 and (p - 1) % d == 0
                 for _ in [0]) and None
    # number of x in F_p^* with ord(x) | 2K is gcd(2K, p-1)
    expect = pairs * gcd(2 * K, p - 1) / (p - 1)
    out["small_order_ratio_pairs"] = (smallord, pairs, round(expect, 3))
    return out


def main():
    data = parse(sys.argv[1:])
    tot_small, tot_exp = 0, 0.0
    nshift = ntrans = nprog = 0
    for (K, p), (g, alpha, beta) in sorted(data.items()):
        o = analyse(K, p, g, alpha, beta)
        s, pairs, e = o["small_order_ratio_pairs"]
        tot_small += s
        tot_exp += e
        nshift += bool(o["shift_sym"])
        ntrans += bool(o["transpose_sym"])
        nprog += bool(o["progressions"])
        print(f"K={K} p={p} zeros={o['zeros']} shift_sym={o['shift_sym']} "
              f"transpose_sym={o['transpose_sym']} progressions={o['progressions']} "
              f"small_order_ratio_pairs={s}/{pairs} (expected {e})")
    print(f"SUMMARY witnesses={len(data)} with_shift_sym={nshift} with_transpose_sym={ntrans} "
          f"with_progression={nprog} small_order_pairs={tot_small} expected_random={tot_exp:.2f}")


if __name__ == "__main__":
    main()

"""Exact check of E_W(c) (Theorem bb-envelope, Lemma tb-count-exponent).

e_d(p) = 1 if kappa_d = 1; 2 if kappa_d >= 2 and p >= 16 kappa^(2kappa+2);
otherwise kappa_d * ceil(log2(kappa_d + 1)),  kappa_d = gcd(d, p-1).
E_W(c) = max over primes p > c of 1 + sum_{d=2}^c e_d(p).

e_d(p) depends on p only through p mod L (L = lcm(2..c)) and the threshold
interval containing p.  We enumerate (unit residue u mod L, interval) pairs,
which gives an upper bound, then look for an actual prime witness for the
maximizing pairs.  AI-checked, pending human review.
"""
from math import gcd, ceil, log2
from functools import reduce
from sympy import isprime, nextprime

def clog(x):  # ceil(log2(x)) for integer x >= 1, exact
    return (x - 1).bit_length()

def T(k):
    return 16 * k ** (2 * k + 2)

def lcm(a, b):
    return a * b // gcd(a, b)

def e(d, p_mod_L, p_ge):  # p_ge: function k -> bool (p >= T(k))
    k = gcd(d, p_mod_L - 1)
    if k == 1:
        return 1
    if p_ge(k):
        return 2
    return k * clog(k + 1)

def E1(c):
    return 1 + sum(d * clog(d + 1) for d in range(2, c + 1))

def EW(c, verbose=False):
    L = reduce(lcm, range(2, c + 1), 1)
    ths = sorted(set(T(k) for k in range(2, c + 1)))
    # intervals [lo, hi): [c+1, ths[0]), [ths[0], ths[1]), ..., [ths[-1], inf)
    bounds = [c + 1] + ths + [None]
    best = None
    best_pairs = []
    units = [u for u in range(1, L + 1) if gcd(u, L) == 1] if L > 1 else [1]
    for i in range(len(bounds) - 1):
        lo, hi = bounds[i], bounds[i + 1]
        p_ge = lambda k, lo=lo: lo >= T(k)
        for u in units:
            val = 1 + sum(e(d, u, p_ge) for d in range(2, c + 1))
            if best is None or val > best:
                best, best_pairs = val, [(u, lo, hi)]
            elif val == best:
                best_pairs.append((u, lo, hi))
    # find a prime witness for some maximizing pair; else descend
    vals = {}
    for i in range(len(bounds) - 1):
        lo, hi = bounds[i], bounds[i + 1]
        p_ge = lambda k, lo=lo: lo >= T(k)
        for u in units:
            val = 1 + sum(e(d, u, p_ge) for d in range(2, c + 1))
            vals.setdefault(val, []).append((u, lo, hi))
    for val in sorted(vals, reverse=True):
        for (u, lo, hi) in vals[val]:
            # smallest p >= lo with p = u mod L, p prime, p < hi
            start = lo + ((u - lo) % L)
            p = start
            tries = 0
            while (hi is None or p < hi) and tries < 200000:
                if p > c and isprime(p):
                    return val, p, best
                p += L
                tries += 1
    return None

if __name__ == "__main__":
    paper = {2: 5, 3: 11, 4: 23, 5: 38, 6: 56, 7: 77, 8: 107, 9: 143}
    wit = {2: 3, 3: 7, 4: 13, 5: 61, 6: 61, 7: 421, 8: 2521, 9: 2521}
    for c in range(2, 14):
        val, p, ub = EW(c)
        L = reduce(lcm, range(2, c + 1), 1)
        # lemma's dichotomy
        some_small = any(isprime(q) for q in range(L + 1, 1024, L))
        lemma = E1(c) if some_small else E1(c) - 2
        flag = "" if val == lemma else "  <-- Lemma tb-count-exponent dichotomy FAILS"
        print(f"c={c}: E_W={val} (prime witness p={p}; residue/interval upper bound {ub}), "
              f"E_1={E1(c)}, lemma predicts {lemma}{flag}"
              + (f", paper value {paper[c]}" if c in paper else ""))
        if c in paper:
            assert val == paper[c], (c, val)
            # check the paper's listed witness attains it
            q = wit[c]
            assert isprime(q)
            v = 1 + sum(e(d, q % L if q % L else L, lambda k: q >= T(k)) for d in range(2, c + 1))
            assert v == paper[c], (c, q, v)
    print("2521 prime:", isprime(2521), "; 841 = 29^2:", 29 * 29 == 841)
    print("16*3^8 =", 16 * 3 ** 8, "(the lemma says thresholds 'exceed 104976 for d>=3'; at d=3 it is equal)")
    print("candidates p = 1 mod 27720 in [1024,104976):", [(q, isprime(q)) for q in range(27721, 104976, 27720)])
    print("lcm(2..13) =", reduce(lcm, range(2, 14), 1), "> 104976")

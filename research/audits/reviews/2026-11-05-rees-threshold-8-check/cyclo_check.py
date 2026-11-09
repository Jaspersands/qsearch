"""Independent check (threshold-8 checker, 2026-11-05) of the cyclotomic criterion.

Written from the definitions, sharing no code with 2026-11-05-rees-threshold-8/.
For each kappa in 3..16 and each prime p = 1 mod kappa below W_2(kappa):
  * A(u,v) = #{w in Q_u : w-1 in Q_v} from a discrete-log table of the least
    primitive root g (coset generator xi = g), and again with a second coset
    generator xi' = g^u0 (u0 the least unit != 1 mod kappa, when one exists);
  * the set E2row(kappa) = {p : A(u,v) = 0 for some u != 0, v != eps, u != v};
  * the difference-set test Q0' - Qb' >= F_p^x for every b != 0, done directly
    with Python sets (independent of A), must agree with the A test;
  * |P| = (k-1)(k-2) or k^2-3k+3, sum A = p-2, the Weil deviation bound of
    Cor. 3(3), and that every p <= k^2-3k+3 is in E2row;
  * W_2(kappa) recomputed.
"""
import math, sys

def primes_upto(n):
    s = bytearray([1]) * (n + 1); s[0] = s[1] = 0
    for i in range(2, int(n ** 0.5) + 1):
        if s[i]:
            s[i * i::i] = bytearray(len(s[i * i::i]))
    return [i for i in range(n + 1) if s[i]]

def primroot(p):
    fs = [q for q in primes_upto(int(p ** 0.5) + 1) if (p - 1) % q == 0]
    m = p - 1
    for q in fs:
        while m % q == 0: m //= q
    if m > 1: fs.append(m)
    for g in range(2, p):
        if all(pow(g, (p - 1) // q, p) != 1 for q in fs):
            return g

def W2(k):
    p = 3
    while not (p - 2 > (k - 1) * (k - 2) * math.sqrt(p) + 3 * (k - 1)):
        p += 1
    return p

def ind_table(p, xi, k):
    # index of x w.r.t. coset generator xi: x^h = zeta^ind, zeta = xi^h
    h = (p - 1) // k
    zeta = pow(xi, h, p)
    zpow = {}
    z = 1
    for e in range(k):
        zpow[z] = e; z = z * zeta % p
    assert len(zpow) == k
    ind = [None] * p
    # x^h for all x via a primitive root walk (fast), checked against pow on a sample
    g = primroot(p)
    gh = pow(g, h, p)
    x, y = 1, 1
    for _ in range(p - 1):
        ind[x] = zpow[y]
        x = x * g % p; y = y * gh % p
    for x in (2, 3, p - 1, (p + 1) // 2):
        assert ind[x] == zpow[pow(x, h, p)]
    return ind

def Atable(p, k, ind):
    A = [[0] * k for _ in range(k)]
    for w in range(2, p):
        A[ind[w]][ind[w - 1]] += 1
    return A

def tworow_A(p, k, ind):
    A = Atable(p, k, ind)
    eps = ind[p - 1]
    P = [(u, v) for u in range(k) for v in range(k) if u != 0 and v != eps and u != v]
    assert len(P) == ((k - 1) * (k - 2) if eps == 0 else k * k - 3 * k + 3)
    assert sum(map(sum, A)) == p - 2
    dev = max(abs(k * k * A[u][v] - (p - 2)) for u in range(k) for v in range(k))
    assert dev <= 3 * (k - 1) + (k - 1) * (k - 2) * math.sqrt(p) + 1e-9, (p, k, dev)
    zero = any(A[u][v] == 0 for (u, v) in P)
    return zero, dev

def tworow_direct(p, k, ind):
    cos = [set() for _ in range(k)]
    for x in range(1, p):
        cos[ind[x]].add(x)
    Q0 = cos[0] | {0}
    for b in range(1, k):
        Qb = cos[b] | {0}
        diff = {(x - y) % p for x in Q0 for y in Qb}
        if len(diff - {0}) < p - 1:
            return True
    return False

def main():
    kmin, kmax = int(sys.argv[1]), int(sys.argv[2])
    direct_upto = int(sys.argv[3]) if len(sys.argv) > 3 else 1500
    for k in range(kmin, kmax + 1):
        w = W2(k)
        ps = [p for p in primes_upto(w) if p % k == 1]
        E = []
        maxratio = 0.0
        for p in ps:
            g = primroot(p)
            ind = ind_table(p, g, k)
            z, dev = tworow_A(p, k, ind)
            # second coset generator
            u0 = next((u for u in range(2, k) if math.gcd(u, k) == 1), None)
            if u0 is not None:
                ind2 = ind_table(p, pow(g, u0, p), k)
                z2, _ = tworow_A(p, k, ind2)
                assert z2 == z, (k, p)
            if p <= direct_upto:
                assert tworow_direct(p, k, ind) == z, (k, p)
            if p <= k * k - 3 * k + 3:
                assert z, ("pigeonhole fails", k, p)
            if z:
                E.append(p)
        print(f"k={k} W2={w} primes={len(ps)} E2row={E} max={max(E) if E else '-'}"
              f" max/k^2={max(E)/k**2 if E else 0:.2f}", flush=True)

if __name__ == "__main__":
    main()

#!/opt/anaconda3/bin/python
"""Exponent of m in the Rees query count under several per-grade rules.

Finite exact computation (AI-run, pending human review).  For each class c = 2..9 and each prime
p > c it computes E(c,p) = 1 + sum_{d=2}^c e_d(p), where e_d(p) is the degree in g_d of the arity
M_d chosen at grade d, and reports max_{p>c} E(c,p) and a maximizing prime.

Rules (see 2026-11-12-rees-exponent-discharge.md, section 3):
  PAPER  : combined rule of main.tex rem:combined-schedule (kappa=1 -> 1; p >= 16 k^(2k+2) -> 2;
           else Schedule 1 at degree k with B_k: k*ceil(log2(k+1))).  Should give 5,11,23,38,56,77,107,143.
  S1ONLY : Schedule 1 at degree d at every grade (core Theorem main): 1 + sum d*ceil(log2(d+1)).
  R1     : PAPER with the sharpened threshold 4 k^(2k+2) (appendix-schedule2 rem:app-s2-four).
  R2     : quadratic whenever p notin E_2(k) (prop:decoupled-sde / prop:triangular-sde), else B_k.
  R3     : R2, with the Schedule 1 fallback at its zero-sum length t(p,k): k*ceil(log2 t)
           (main.tex sec:schedule1 'More precisely ... G(k,a)^ceil(log2 l_d)'); t = 2 for odd k.
  R4     : R3 plus the prime-factor tower of appendix s2-tower for composite k where its
           threshold holds (degree Omega(k)+1).
  LAW    : weight-doubling Schedule 3(iii) (rem:fc-witness-h3(c)): 1 + j*_h at 2 <= k < p-1,
           1 + ceil(log2(p-1)) at k = p-1, 1 at k = 1.  Should give 3,6,8,10,13,14,16,19.
  LAWMIX : per grade min(R4, LAW)  (law-based nodes mixed with worst-case nodes).

E_2 data: E_2(2) = E_2(3) = {} ; E_2(4), E_2(5) as printed in main.tex; E_2(6) from
2026-11-02-rees-threshold-2/xval_k6.out; E_2(7) from 2026-11-02-rees-threshold-2/E2_k7.txt;
E_2(8), E_2(9) on p <= 20000 from 2026-11-10-rees-dfs2b-queue-final/E2_k{8,9}_le20000.json.
Above 20000: E_2(8) is empty (determined, max 14281); every prime p = 1 mod 9 above 20000 is
treated as a MEMBER of E_2(9) (conservative: only upper bounds on the exponent are claimed).
"""
import json, math, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
REV = os.path.dirname(HERE)
PMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 30_000
PBIG = int(sys.argv[2]) if len(sys.argv) > 2 else 3_000_000


def primes_upto(n):
    s = bytearray([1]) * (n + 1)
    s[0] = s[1] = 0
    for i in range(2, int(n ** 0.5) + 1):
        if s[i]:
            s[i * i::i] = bytearray(len(s[i * i::i]))
    return [i for i in range(n + 1) if s[i]]


def load_e2():
    e2 = {2: set(), 3: set(), 4: {5, 13, 17, 29, 37, 53},
          5: {11, 31, 41, 61, 71, 101, 131, 151, 181}}
    e6 = set()
    for line in open(os.path.join(REV, '2026-11-02-rees-threshold-2', 'xval_k6.out')):
        if line.startswith('INFEASIBLE'):
            e6.add(int(line.split('p=')[1].split()[0]))
    assert len(e6) == 53 and max(e6) == 859
    e2[6] = e6
    e7 = {int(x) for x in open(os.path.join(REV, '2026-11-02-rees-threshold-2', 'E2_k7.txt')).read().split()}
    assert len(e7) == 56 and max(e7) == 3221
    e2[7] = e7
    for k, n, mx in ((8, 293, 14281), (9, 342, 19963)):
        d = json.load(open(os.path.join(REV, '2026-11-10-rees-dfs2b-queue-final', 'E2_k%d_le20000.json' % k)))
        assert not d['undecided']
        e2[k] = set(d['members'])
        assert len(e2[k]) == n and max(e2[k]) == mx
    return e2


E2 = load_e2()


def in_E2(p, k):
    """Upper-bound-safe membership: True if p in E_2(k) or undecided."""
    if k == 9 and p > 20000:
        return True  # conservative
    if k == 8 and p > 20000:
        return False  # E_2(8) determined, subset of [3,20000]
    return p in E2[k]


def kth_powers(p, k):
    g = primitive_root(p)
    h = (p - 1) // k
    out, x, gk = set(), 1, pow(g, k, p)
    for _ in range(h):
        out.add(x)
        x = x * gk % p
    return out


_pr = {}


def primitive_root(p):
    if p in _pr:
        return _pr[p]
    if p == 2:
        return 1
    fs, n, q = [], p - 1, 2
    while q * q <= n:
        if n % q == 0:
            fs.append(q)
            while n % q == 0:
                n //= q
        q += 1
    if n > 1:
        fs.append(n)
    for g in range(2, p):
        if all(pow(g, (p - 1) // f, p) != 1 for f in fs):
            _pr[p] = g
            return g


_t = {}


def zero_sum_length(p, k):
    """Least t >= 2 with x_1^k + ... + x_t^k = 0, all x_i nonzero (exact)."""
    if (p, k) in _t:
        return _t[(p, k)]
    if ((p - 1) // k) % 2 == 0:  # -1 is a k-th power
        _t[(p, k)] = 2
        return 2
    # Weil bound for the Fermat curve X^k + Y^k + Z^k = 0: at least p + 1 - (k-1)(k-2) sqrt(p)
    # projective points, at most 3k of them with XYZ = 0; so t <= 3 once that count exceeds 3k.
    if p + 1 - (k - 1) * (k - 2) * math.sqrt(p) > 3 * k:
        _t[(p, k)] = 3
        return 3
    Q = kth_powers(p, k)
    if any(((p - 1 - q) % p) in Q for q in Q):  # -1 = q + q'
        _t[(p, k)] = 3
        return 3
    mask = (1 << p) - 1
    cur = 0
    for q in Q:
        cur |= 1 << q
    qs = sorted(Q)
    t = 1
    while True:
        t += 1
        # cur = set of sums of (t-1) nonzero k-th powers; test whether -1*... : need s + q = 0 for some q
        # i.e. some element of cur equals p - q for q in Q.
        if any((cur >> ((p - q) % p)) & 1 for q in qs):
            _t[(p, k)] = t
            return t
        nxt = 0
        for q in qs:
            nxt |= ((cur << q) | (cur >> (p - q))) & mask
        cur = nxt
        assert t <= p + 1


def omega(k):
    n, q, c = k, 2, 0
    while q * q <= n:
        while n % q == 0:
            n //= q
            c += 1
        q += 1
    return c + (1 if n > 1 else 0)


def prime_factors_desc(k):
    n, q, fs = k, 2, []
    while q * q <= n:
        while n % q == 0:
            fs.append(q)
            n //= q
        q += 1
    if n > 1:
        fs.append(n)
    return sorted(fs, reverse=True)


def tower_ok(p, k):
    """Threshold of the prime-factor tower (main.tex rem:two-level-threshold-size / app s2-tower)."""
    fs = prime_factors_desc(k)
    if len(fs) < 2:
        return False
    if all(f == 2 for f in fs):
        return p > ((k - 1) ** 2 + 1) ** 2
    q1 = fs[0]
    if q1 >= 5:
        return False  # needs p > T_A(q1); not used here (no composite k <= 9 has q1 >= 5)
    return p > max(4 * k ** (q1 + 1), 4 * q1 * q1 * k ** 5)


_j = {}


def jstar(p, k):
    """j*_h of rem:fc-witness-h3(a): least J with D_J = F_p, D_0 = P_k u {0}, D_{j+1} = D_j - D_j."""
    if (p, k) in _j:
        return _j[(p, k)]
    if math.isqrt(p) > (k - 1) * (k - 2) + 3 and math.sqrt(p) > (k - 1) * (k - 2) + 3:
        _j[(p, k)] = 1
        return 1
    D = kth_powers(p, k) | {0}
    J = 0
    while len(D) < p:
        D = {(x - y) % p for x in D for y in D}
        J += 1
    _j[(p, k)] = J
    return J


# appendix-schedule2 rem:app-s2-tower-scope: primes p = 1 mod k at which neither the two-level
# construction, nor a tower, nor a union chain with |K| in {2,3} (k = 7: also 4) was found.
NOSTD = {4: {5, 13}, 5: {11}, 6: {7, 13, 19, 31, 43, 67}, 7: {29, 43, 71, 113},
         8: {17, 41, 73, 89, 137, 233}, 9: {19, 37, 73, 109, 127, 163, 181, 199, 307, 433}}
# rem:app-s2-chains-scope: three-step chain Z_7 -> u{0,1,2} -> u{0,1} -> {0} (degree 4) works at
# every prime p = 1 mod 7 except 29 and 71.
CHAIN4_K7_FAIL = {29, 71}
# degree of the standard constructions at p in E_2(k) \ NOSTD[k]: union chain (degree 3) or tower
# (degree Omega(k)+1); conservatively the max of the two.
STD_DEG = {4: 3, 5: 3, 6: 3, 7: 3, 8: 4, 9: 3}


# appendix-schedule2 Table tab:app-s2-thresholds: T_A(k) (p > T_A(k) implies p notin E_2(k)).
T_A = {2: 8.42, 3: 79.0, 4: 869, 5: 1.27e4, 6: 2.34e5, 7: 4.94e6, 8: 117441563, 9: 3.10e9}


def e_grade(rule, p, d):
    if rule == 'S1ONLY':
        return d * math.ceil(math.log2(d + 1))
    k = math.gcd(d, p - 1)
    if k == 1:
        return 1
    if rule == 'S1t':  # Schedule 1 alone at degree k with its zero-sum depth (no Schedule 2)
        t = p if k == p - 1 else (2 if k % 2 == 1 else zero_sum_length(p, k))
        return k * math.ceil(math.log2(t))
    s1_full = k * math.ceil(math.log2(k + 1))
    if rule == 'S1ONLY':
        return d * math.ceil(math.log2(d + 1))
    if rule == 'PAPER':
        return 2 if p >= 16 * k ** (2 * k + 2) else s1_full
    if rule == 'R1':
        return 2 if p >= 4 * k ** (2 * k + 2) else s1_full
    if rule in ('R1t', 'RTAt') and k < p - 1:
        thr = 4 * k ** (2 * k + 2) if rule == 'R1t' else T_A[k]
        if p >= thr:
            return 2
        t = 2 if k % 2 == 1 else zero_sum_length(p, k)
        return k * math.ceil(math.log2(t))
    if k == p - 1:  # zero-sum grade (p = c+1 prime, d = c); E_2(p-1) contains p
        t = p
        free = k * math.ceil(math.log2(t)) if rule in ('R1t', 'RTAt', 'R3', 'R4', 'R5', 'LAWMIX', 'LAWMIX5') else s1_full
        if p == 3 and rule in ('R1t', 'RTAt', 'R3', 'R4', 'R5', 'LAWMIX', 'LAWMIX5'):
            free = 2  # F_3 subset sum n^2/4 + O(n^{3/2}) (2026-11-08-rees-sde-p3-nest.md), worst case
        if rule == 'LAW':
            return 1 + math.ceil(math.log2(p - 1))
        if rule in ('LAWMIX', 'LAWMIX5'):
            return min(free, 1 + math.ceil(math.log2(p - 1)))
        return free
    if rule == 'LAW':
        return 1 + jstar(p, k)
    quad = not in_E2(p, k) or p >= 4 * k ** (2 * k + 2)
    if rule in ('R5', 'LAWMIX5'):
        if quad:
            free = 2
        else:
            t = 2 if k % 2 == 1 else zero_sum_length(p, k)
            free = k * math.ceil(math.log2(t))
            if tower_ok(p, k):
                free = min(free, omega(k) + 1)
            if p not in NOSTD[k]:
                free = min(free, STD_DEG[k])
            if k == 7 and p not in CHAIN4_K7_FAIL:
                free = min(free, 4)
        if rule == 'LAWMIX5':
            return min(free, 1 + jstar(p, k))
        return free
    if rule == 'R2':
        return 2 if quad else s1_full
    if quad:
        free = 2
    else:
        t = 2 if k % 2 == 1 else zero_sum_length(p, k)
        free = k * math.ceil(math.log2(t))
        if rule in ('R4', 'LAWMIX') and tower_ok(p, k):
            free = min(free, omega(k) + 1)
    if rule == 'LAWMIX':
        return min(free, 1 + jstar(p, k))
    return free


def main():
    P = [q for q in primes_upto(PMAX) if q > 2]
    rules = ['S1ONLY', 'S1t', 'PAPER', 'R1', 'R1t', 'RTAt', 'R2', 'R3', 'R4', 'R5', 'LAW', 'LAWMIX', 'LAWMIX5']
    print('primes scanned: 3..%d (%d primes); above %d see the analytic bound in the note' % (PMAX, len(P), PMAX))
    for rule in rules:
        row = []
        for c in range(2, 10):
            best, arg = -1, None
            for p in P:
                if p <= c:
                    continue
                E = 1 + sum(e_grade(rule, p, d) for d in range(2, c + 1))
                if E > best:
                    best, arg = E, p
                if rule == 'S1ONLY':
                    break
            row.append('%d(p=%d)' % (best, arg))
        print('%-7s' % rule, ' '.join(row))
    # detail of the maximizer for c = 9
    for rule in ('S1t', 'PAPER', 'R3', 'R4', 'R5', 'LAWMIX', 'LAWMIX5'):
        best, arg = -1, None
        for p in P:
            if p <= 9:
                continue
            E = 1 + sum(e_grade(rule, p, d) for d in range(2, 10))
            if E > best:
                best, arg = E, p
        print('c=9 %-6s max %d at p=%d, e_d =' % (rule, best, arg),
              [e_grade(rule, arg, d) for d in range(2, 10)],
              'kappa_d =', [math.gcd(d, arg - 1) for d in range(2, 10)])
    # all primes attaining the R4 maximum at c = 9, and the top values
    vals = {}
    for p in P:
        if p > 9:
            vals[p] = 1 + sum(e_grade('R5', p, d) for d in range(2, 10))
    top = sorted(vals.items(), key=lambda x: -x[1])[:12]
    print('c=9 R5 top primes:', top)
    PB = [q for q in primes_upto(PBIG) if q > 20000]
    for rule in ('S1t', 'R4', 'R5', 'LAWMIX5'):
        vb = {p: 1 + sum(e_grade(rule, p, d) for d in range(2, 10)) for p in PB}
        for lo in (20000, 300000, 2125764):
            sel = [v for p, v in vb.items() if p > lo]
            if sel:
                print('c=9 %s max over primes in (%d, %d]: %d' % (rule, lo, PBIG, max(sel)))

if __name__ == '__main__':
    main()

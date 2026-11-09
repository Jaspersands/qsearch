"""Permanent weights of the type certificate and the thresholds they imply (REPORT.md Sec. 4).

P(r) = sum_{sigma in S_k} omega^{-sum_i r_i sigma(i)}  (permanent of (omega^{-r_i j})), r in Z_k^k.
P depends only on the multiset of r, vanishes unless sum r = 0 mod k, P(0) = k!, sum_{r != 0} P(r) = -k!.
w(r) = |P(r)|/k!, W1 = sum_{r != 0} w(r), m(r) = |supp r|.  Weight of rho = (r, c) is w(r) w(c).

Thresholds (p real, n = p + 1 - 2k, m = |supp r| + |supp c|):
  T_abs        : sum_{rho != 0} w(rho) ((m-2) sqrt p + 2k - m) < n   [original PW + per-orbit Weil bound, rigorous]
  T_pairsigned : same, pair one-sided classes bounded by k-2, RHS n + k^2 (k-1)   [PW_pair, rigorous]
  T_A = (k-1) k^k,  T_B = (k-1) k^(k-1) + k - 1 (pigeonhole existence of C1 configurations).
  Conditional on Conjecture OSC(B): N1 >= p^(2k-2) k^-(k-1)^2 / B;  'low' rho: |Fh/Fh0| <= B k / p;
  other rho: |Fh/Fh0| <= B sqrt(m / N1).  strong: low = (m <= 5, not pair one-sided);
  weak: low = (min(|supp r|,|supp c|) <= 2).  T_H = random-phase part alone (B = 1).
Usage: python weights.py kmax
"""
import sys, math, itertools
import numpy as np


def perm_ryser(M):
    k = M.shape[0]
    tot = 0j
    for mask in range(1, 1 << k):
        cols = [j for j in range(k) if mask >> j & 1]
        rs = M[:, cols].sum(1)
        tot += (-1) ** len(cols) * np.prod(rs)
    return (-1) ** k * tot


def weights(k):
    om = np.exp(-2j * np.pi / k)
    kf = math.factorial(k)
    out = {}  # m -> (count of r, sum of w)
    sumP = 0j
    for n in itertools.product(range(k + 1), repeat=k):
        if sum(n) != k or sum(a * n[a] for a in range(k)) % k:
            continue
        r = [a for a in range(k) for _ in range(n[a])]
        M = np.array([[om ** ((ri * j) % k) for j in range(k)] for ri in r])
        P = perm_ryser(M)
        mult = kf // math.prod(math.factorial(x) for x in n)
        m = k - n[0]
        c, s = out.get(m, (0, 0.0))
        out[m] = (c + mult, s + mult * abs(P) / kf)
        if m:
            sumP += mult * P
    return out, sumP / kf


def solve(A, B, C):
    """smallest p >= 1 with A sqrt(p) + B < p + C (A, B >= 0)."""
    # y^2 - A y + (C - B) > 0, y = sqrt p
    disc = A * A - 4 * (C - B)
    if disc < 0:
        return 1.0
    y = (A + math.sqrt(disc)) / 2
    return y * y


if __name__ == '__main__':
    kmax = int(sys.argv[1])
    for k in range(3, kmax + 1):
        out, sP = weights(k)
        W1 = sum(s for m, (c, s) in out.items() if m)
        cs = math.sqrt(k ** (k - 1) * k ** k * math.factorial(k)) / math.factorial(k)
        Wtot = (1 + W1) ** 2 - 1
        ms = sorted(m for m in out if m)
        # one-sided: rho = (0, c) or (r, 0): weight w(c); two-sided: w(r) w(c)
        A1 = 2 * sum(out[m][1] * (m - 2) for m in ms)
        B1 = 2 * sum(out[m][1] * (k - m) for m in ms)
        B1abs = 2 * sum(out[m][1] * (2 * k - m) for m in ms)
        A2 = sum(out[a][1] * out[b][1] * (a + b - 2) for a in ms for b in ms)
        B2 = sum(out[a][1] * out[b][1] * (2 * k - a - b) for a in ms for b in ms)
        T_abs = solve(A1 + A2, B1abs + B2 + 2 * k - 1, 0.0)
        T_sign = solve(A1 + A2, B1 + B2, 1.0)
        T_A = (k - 1) * k ** k
        T_B = (k - 1) * k ** (k - 1) + k - 1
        Wp = out[2][1]  # = C(k,2): w-sum over pair-supported r
        # rigorous, pair-signed certificate (REPORT Sec. 3): pair one-sided terms bounded by (k-2), RHS n + k^2 (k-1)
        A_ps = A1 + A2
        B_ps = 2 * Wp * (k - 2) + 2 * sum(out[m][1] * (2 * k - m) for m in ms if m > 2) + B2
        T_ps = solve(A_ps, B_ps + 2 * k - 1, k * k * (k - 1))

        def T_cond(Bc, strong):
            # pair one-sided: proved |E| <= k-2 ; other rho: 'low' -> Bc k / p ; 'high' -> Bc sqrt(m / N1),
            # N1 = p^(2k-2) k^-(k-1)^2 / Bc.  weak: low = min(|supp r|,|supp c|) <= 2 ; strong: low = m <= 5.
            low_w, high_s = 0.0, 0.0
            sides = [0] + ms
            for a in sides:
                for b in sides:
                    if a == 0 and b == 0:
                        continue
                    wa = 1.0 if a == 0 else out[a][1]
                    wb = 1.0 if b == 0 else out[b][1]
                    w = wa * wb
                    if (a == 0 and b == 2) or (a == 2 and b == 0):
                        continue
                    low = (min(a, b) <= 2) if not strong else (a + b <= 5)
                    if low:
                        low_w += w
                    else:
                        high_s += w * math.sqrt(a + b)
            def f(p):
                n = p + 1 - 2 * k
                rhs = 1 + k * k * (k - 1) / n
                return 2 * Wp * (k - 2) / n + Bc * k * low_w / p + Bc ** 1.5 * high_s * math.exp(-((2 * k - 2) * math.log(p) - (k - 1) ** 2 * math.log(k)) / 2) - rhs
            lo, hi = 4.0 * k, 1e40
            for _ in range(400):
                mid = math.sqrt(lo * hi)
                if f(mid) > 0:
                    lo = mid
                else:
                    hi = mid
            return hi, low_w, (high_s * float(k) ** ((k - 1) ** 2 / 2)) ** (1 / (k - 1))
        tw1, lw1, _ = T_cond(1, False)
        tw4, _, _ = T_cond(4, False)
        ts1, lws, tH = T_cond(1, True)
        ts4, _, _ = T_cond(4, True)
        print(k, 'W1=%.5g' % W1, 'CS=%.4g' % cs, 'Wtot=%.4g' % Wtot, 'W_pair1=%.4g' % (2 * Wp),
              'T_abs=%.3e' % T_abs, 'T_pairsigned=%.3e' % T_ps, 'T_A=%.3e' % T_A, 'T_B=%.3e' % T_B,
              '| W_low(weak)=%.4g T_weak(B=1)=%.3e T_weak(B=4)=%.3e | W_low(strong)=%.4g T_strong(B=1)=%.3e T_strong(B=4)=%.3e'
              % (lw1, tw1, tw4, lws, ts1, ts4), '| T_H(random-phase part alone, B=1)=%.3e  k^(k/2+9/4)=%.3e  1.5k^((k+1)/2)=%.3e' % (tH, k ** (k / 2 + 9 / 4), 1.5 * k ** ((k + 1) / 2)),
              'sum_{r!=0}P/k!=%.3f' % sP.real, flush=True)
        print('    per support m: ' + '  '.join('m=%d:#%d,w=%.4g' % (m, out[m][0], out[m][1]) for m in ms))

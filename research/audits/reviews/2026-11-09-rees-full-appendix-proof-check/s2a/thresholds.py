# s2a: recompute every constant of Table tab:app-s2-thresholds and the numerical
# claims of Prop. prop:app-s2-TW / prop:app-s2-TA / Cor. cor:app-s2-small / main.tex
# from the closed forms of appendix-schedule2.tex (lines 199-397).
# Run: nice -n 19 timeout 600 /opt/anaconda3/bin/python -I thresholds.py
import mpmath as mp
from mpmath import mpf, sqrt, exp, iv

mp.mp.dps = 60

def Delta(k, p):
    k = mpf(k); p = mpf(p)
    return ((k-1)*(k-2)*sqrt(p) + 2*(k-1)) / (p - k - 1)

def Emax(k, D):
    k = mpf(k)
    u = mpf(1)/2 - D/3 - 1/(k*(1-D))
    v = D/(sqrt(k)*(1-D))
    smax = sqrt(k)*D
    f = lambda s: -u*s*s + v*s
    cands = [mpf(0), f(smax)]
    if u > 0:
        s = v/(2*u)
        if 0 <= s <= smax:
            cands.append(f(s))
    return max(cands)

def U(k, p):
    p = mpf(p); kk = mpf(k)
    D = Delta(k, p)
    assert D <= mpf(1)/2, (k, p, D)
    return kk**kk * p**(kk-1) / (p-1)**kk + exp(Emax(k, D))

def pDelta(k):
    # solve Delta(p) = 1/2 : p - 2 c1 sqrt p - (c3 + 2 c2) = 0
    c1 = mpf((k-1)*(k-2)); c2 = mpf(2*(k-1)); c3 = mpf(k+1)
    s = c1 + sqrt(c1*c1 + c3 + 2*c2)
    return s*s*(1+mpf(10)**-50)

def thresh(k, target, strict):
    lo = pDelta(k)
    # if condition already holds at lo, threshold is lo
    if (U(k, lo) < target) if strict else (U(k, lo) <= target):
        return lo, 'Delta'
    hi = lo*2
    while not (U(k, hi) < target):
        hi *= 2
    for _ in range(400):
        mid = (lo+hi)/2
        if U(k, mid) < target:
            hi = mid
        else:
            lo = mid
    return hi, 'U'

def TW(k):
    k = mpf(k)
    A = (k-2)*k**k + 1
    return ((A + sqrt(A*A + 4*k**k))/2)**2

print("=== Table tab:app-s2-thresholds (recomputed) ===")
print("k | 16k^(2k+2) | T_W | T_A (binding) | (k-1)k^k | T_S (binding) | Delta(T_A) | Delta(T_S)")
TA = {}; TS = {}
for k in range(2, 41):
    ta, ba = thresh(k, mpf(k)/(k-1), True)
    ts, bs = thresh(k, 1 + mpf(1)/(8*k), False)
    TA[k] = ta; TS[k] = ts
    if k <= 9:
        print(k, mp.nstr(16*mpf(k)**(2*k+2), 4), mp.nstr(TW(k), 4), mp.nstr(ta, 8), ba,
              (k-1)*k**k, mp.nstr(ts, 6), bs, mp.nstr(Delta(k, ta), 4), mp.nstr(Delta(k, ts), 4))

print("\nT_A(3) =", mp.nstr(TA[3], 10), " T_A(2) =", mp.nstr(TA[2], 10), " T_S(2) =", mp.nstr(TS[2], 10))
print("T_A(7) =", mp.nstr(TA[7], 12), " < 5e6 ?", TA[7] < 5e6)
print("T_A(8) =", mp.nstr(TA[8], 15), " ceil =", int(mp.ceil(TA[8])), " claimed 117441563")
print("T_A(9) =", mp.nstr(TA[9], 15), " 9^9/2 =", mpf(9)**9/2, " 9^9/2 < T_A(9)?", mpf(9)**9/2 < TA[9])
print("(k-1)k^k at 8:", 7*8**8, " T_A(8) - 7*8^8 =", mp.nstr(TA[8]-7*8**8, 8))

print("\n=== Prop TA(ii) claims for 2..40 ===")
bad = []
for k in range(2, 41):
    if not TA[k] > (k-1)*mpf(k)**k: bad.append(('TA>(k-1)k^k', k))
    if k >= 3 and not TA[k] <= mpf(k)**(k+1): bad.append(('TA<=k^(k+1)', k))
    if k >= 3 and not TS[k] <= 10*mpf(k)**(k+1): bad.append(('TS<=10k^(k+1)', k))
    if k >= 4 and not TS[k] <= 9*mpf(k)**(k+1): bad.append(('TS<=9k^(k+1)', k))
print("violations:", bad)
print("TS/k^(k+1):", [(k, mp.nstr(TS[k]/mpf(k)**(k+1), 4)) for k in (3, 4, 5, 6, 10, 20, 40)])
print("TA/k^(k+1):", [(k, mp.nstr(TA[k]/mpf(k)**(k+1), 4)) for k in (2, 3, 4, 5, 6, 10, 20, 40)])

print("\n=== direct evaluations at P = k^(k+1), k = 3,4,5 (Prop TA(ii) proof) ===")
for k in (3, 4, 5):
    P = mpf(k)**(k+1)
    u = U(k, P)
    print(k, "Delta(P) =", mp.nstr(Delta(k, P), 6), " U(P) =", mp.nstr(u, 8),
          " margin k/(k-1)-U =", mp.nstr(mpf(k)/(k-1) - u, 6))

print("\n=== ratio 16k^(2k+2)/T_W(k) ===")
print([(k, mp.nstr(16*mpf(k)**(2*k+2)/TW(k), 5)) for k in range(2, 10)])
print("T_W(2) =", mp.nstr(TW(2), 8), " ((1+sqrt17)/2)^2 =", mp.nstr(((1+sqrt(17))/2)**2, 8))
print("T_W(k)/((k-2)^2 k^(2k)):", [(k, mp.nstr(TW(k)/((k-2)**2*mpf(k)**(2*k)), 5)) for k in (3, 5, 9, 20, 50)])
print("4((k-1)k^k+1)^2 vs 16k^(2k+2):", [(k, mp.nstr(4*((k-1)*mpf(k)**k+1)**2, 4), mp.nstr(16*mpf(k)**(2*k+2), 4)) for k in range(2, 10)])
print("kappa*p at p=4((k-1)k^k+1)^2 over k^(2k+3):", [(k, mp.nstr(k*4*((k-1)*mpf(k)**k+1)**2/mpf(k)**(2*k+3), 4)) for k in range(2, 10)])

print("\n=== constants of the k >= 6 argument (Prop TA(ii)), k = 6..200 ===")
viol = []
for k in range(6, 201):
    kk = mpf(k); P = kk**(k+1)
    D = Delta(k, P)
    b1 = kk**((kk+5)/2)*(1 + 2*kk**(-(kk+3)/2)) / (kk**(kk+1)*(1 - 2*kk**(-kk)))
    if not (D <= b1 <= mpf('1.01')*kk**((3-kk)/2) <= mpf('0.1')): viol.append(('Delta', k))
    u = mpf(1)/2 - D/3 - 1/(kk*(1-D))
    if not u >= mpf('0.28'): viol.append(('u', k))
    v = D/(sqrt(kk)*(1-D))
    E = Emax(k, D)
    if not (E <= v*v/(4*u) <= D*D/(4*mpf('0.28')*mpf('0.81')*kk) <= mpf('1.2')*kk**(2-kk) <= 1): viol.append(('E', k))
    first = kk**kk*P**(kk-1)/(P-1)**kk
    if not first <= 1/kk + 2*kk**(-kk-1): viol.append(('first', k))
    lhs = 2*kk**(1-kk) + mpf('2.4')*kk**(4-kk)
    if not lhs < 1: viol.append(('final', k))
    if k == 6:
        print("k=6: Delta(P) =", mp.nstr(D, 6), " bound chain", mp.nstr(b1, 6), mp.nstr(mpf('1.01')*kk**((3-kk)/2), 6),
              " u =", mp.nstr(u, 6), " lhs =", mp.nstr(lhs, 6))
    if not U(k, P) < kk/(kk-1): viol.append(('U(P)', k))
print("violations:", viol)

print("\n=== interval re-check of the bracketing of T_A(k), T_S(k), k = 2..9 ===")
# verify with interval arithmetic that the condition fails slightly below and holds slightly above
iv.dps = 40
def U_iv(k, p):
    p = iv.mpf(p); kk = iv.mpf(k)
    D = ((kk-1)*(kk-2)*iv.sqrt(p) + 2*(kk-1)) / (p - kk - 1)
    u = iv.mpf(1)/2 - D/3 - 1/(kk*(1-D))
    v = D/(iv.sqrt(kk)*(1-D))
    smax = iv.sqrt(kk)*D
    # bound E_max from above and below: evaluate candidates with intervals
    fsmax = -u*smax*smax + v*smax
    cands_hi = [0, fsmax.b]
    cands_lo = [0, fsmax.a]
    if u.a > 0:
        s = v/(2*u)
        if s.b <= smax.a:
            val = v*v/(4*u)
            cands_hi.append(val.b); cands_lo.append(val.a)
        elif s.a > smax.b:
            pass
        else:
            val = v*v/(4*u)
            cands_hi.append(val.b)
    elif u.b > 0:
        # sign of u uncertain; crude upper bound
        cands_hi.append((v*v/(4*abs(u))).b if u.a > 0 else mp.inf)
    Elo = max(cands_lo); Ehi = max(cands_hi)
    first = kk**kk * p**(kk-1)/(p-1)**kk
    return first.a + mp.exp(Elo), first.b + mp.exp(Ehi)
for k in range(2, 10):
    for name, T, tgt in (("T_A", TA[k], mpf(k)/(k-1)), ("T_S", TS[k], 1+mpf(1)/(8*k))):
        lo_p = T*(1-mpf(10)**-12); hi_p = T*(1+mpf(10)**-12)
        if Delta(k, lo_p) > mpf(1)/2:
            okbelow = 'Delta>1/2 below'
        else:
            a, b = U_iv(k, lo_p); okbelow = a > tgt
        a, b = U_iv(k, hi_p); okabove = b < tgt if name == "T_A" else b <= tgt
        print(k, name, mp.nstr(T, 12), "fails below:", okbelow, " holds above:", okabove)

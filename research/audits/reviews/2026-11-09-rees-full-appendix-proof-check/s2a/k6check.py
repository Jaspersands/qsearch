# s2a: re-run the k >= 6 constant chain of Prop TA(ii) at high precision (k = 6..200),
# replacing E <= v^2/(4u) by the exact vertex test; plus T_W(9) digits.
import mpmath as mp
from mpmath import mpf, sqrt, exp
mp.mp.dps = 700
def Delta(k, p):
    k = mpf(k); p = mpf(p)
    return ((k-1)*(k-2)*sqrt(p) + 2*(k-1)) / (p - k - 1)
viol = []
for k in range(6, 201):
    kk = mpf(k); P = kk**(k+1)
    D = Delta(k, P)
    b1 = kk**((kk+5)/2)*(1 + 2*kk**(-(kk+3)/2)) / (kk**(kk+1)*(1 - 2*kk**(-kk)))
    if not (D <= b1 <= mpf('1.01')*kk**((3-kk)/2) <= mpf('0.1')): viol.append(('Delta', k))
    u = mpf(1)/2 - D/3 - 1/(kk*(1-D))
    if not u >= mpf('0.28'): viol.append(('u', k))
    v = D/(sqrt(kk)*(1-D))
    smax = sqrt(kk)*D
    s = v/(2*u)
    E = v*v/(4*u) if s <= smax else (-u*smax*smax + v*smax)
    if not (E <= v*v/(4*u)*(1+mpf(10)**-600)): viol.append(('E1', k))
    if not (v*v/(4*u) <= D*D/(4*mpf('0.28')*mpf('0.81')*kk)): viol.append(('E2', k))
    if not (D*D/(4*mpf('0.28')*mpf('0.81')*kk) <= mpf('1.2')*kk**(2-kk) <= 1): viol.append(('E3', k))
    if not exp(E) <= 1 + 2*E: viol.append(('expE', k))
    first = kk**kk*P**(kk-1)/(P-1)**kk
    if not first <= 1/kk + 2*kk**(-kk-1): viol.append(('first', k))
    if not (kk/P <= mpf(1)/2): viol.append(('k/P', k))
    lhs = 2*kk**(1-kk) + mpf('2.4')*kk**(4-kk)
    if not lhs < 1: viol.append(('final', k))
    if not (2*kk**(-kk-1) + mpf('2.4')*kk**(2-kk) < 1/(kk*(kk-1))): viol.append(('pre-final', k))
print("violations k=6..200:", viol)
mp.mp.dps = 50
k = mpf(9); A = (k-2)*k**k + 1
print("T_W(9) =", mp.nstr(((A + sqrt(A*A + 4*k**k))/2)**2, 12))
print("16*9^20 =", 16*9**20)

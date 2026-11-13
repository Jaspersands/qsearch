"""Crude second-moment thresholds for RC(D; R -> K) contractions (Lemma SM of the fragment).
Uses only Weil's bound for two-variable diagonal equations |N - p| <= (D-1)^2 sqrt(p).
rho_j <= 1/E[n_j] + gamma^(r-1),  gamma = (1 + (D-1)^2/sqrt p) (p/(p-1))^2,
E[n_0] = h (k h/p)^(r-1), E[n_j] = k h (k h/p)^(r-1) (j != 0), h = (p-1)/D, k = |K|.
Existence if Phi = sum_j (1 - 1/rho_j) < 1;  sampler if sum_j 4 (rho_j - 1) <= 1/2.
Both are decreasing in p; thresholds by bisection over reals, reported as ceil.  Exact rational
arithmetic is not needed: the reported integer T is re-checked with mpmath at 50 digits."""
import mpmath as mp
mp.mp.dps = 50

def rho_bounds(p, D, r, k):
    p = mp.mpf(p); h = (p - 1) / D
    gam = (1 + (D - 1) ** 2 / mp.sqrt(p)) * (p / (p - 1)) ** 2
    E0 = h * (k * h / p) ** (r - 1)
    Ej = k * h * (k * h / p) ** (r - 1)
    rho0 = 1 / E0 + gam ** (r - 1)
    rhoj = 1 / Ej + gam ** (r - 1)
    return rho0, rhoj

def Phi(p, D, r, k):
    r0, rj = rho_bounds(p, D, r, k)
    return (1 - 1 / r0) + (D - 1) * (1 - 1 / rj)

def Psi(p, D, r, k):
    r0, rj = rho_bounds(p, D, r, k)
    return 4 * (r0 - 1) + 4 * (D - 1) * (rj - 1)

def thresh(f, D, r, k, bound):
    lo, hi = mp.mpf(D + 2), mp.mpf(10) ** 14
    assert f(hi, D, r, k) < bound
    for _ in range(300):
        mid = (lo + hi) / 2
        if f(mid, D, r, k) < bound: hi = mid
        else: lo = mid
    T = int(mp.ceil(hi))
    assert f(T, D, r, k) < bound and f(T + 10 ** 6, D, r, k) < bound
    return T

STEPS = {  # name: (D, r, k)
    'two-level 3': (3, 3, 1), 'two-level 4': (4, 4, 1), 'two-level 5': (5, 5, 1),
    'two-level 6': (6, 6, 1), 'two-level 7': (7, 7, 1), 'two-level 8': (8, 8, 1), 'two-level 9': (9, 9, 1),
    'tower step (9;{0,3,6})': (9, 3, 1), 'tower step (6;{0,3})': (6, 2, 1), 'tower step (6;{0,2,4})': (6, 3, 1),
    'tower step (8;{0,4})': (8, 2, 1), 'tower step (4;{0,2})': (4, 2, 1),
    'union step (7;Z7->{0,m})': (7, 7, 2), 'union step (7;Z7->3 classes)': (7, 7, 3),
    'step (7;{0,m}->{0})': (7, 2, 1), 'step (7;3 classes->{0})': (7, 3, 1),
    'union step (9;Z9->{0,m})': (9, 9, 2), 'union step (5;Z5->{0,m})': (5, 5, 2),
}

if __name__ == '__main__':
    for name, (D, r, k) in STEPS.items():
        T = thresh(Phi, D, r, k, 1)
        TS = thresh(Psi, D, r, k, mp.mpf(1) / 2)
        print(f'{name:32s} D={D} r={r} k={k}  T_exist = {T:>14d}   T_sampler = {TS:>16d}')

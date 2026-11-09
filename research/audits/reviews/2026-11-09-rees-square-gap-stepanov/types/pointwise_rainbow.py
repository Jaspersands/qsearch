"""Rigorous but weak: for ANY C1 orbit o, Z(o) = #{charts z with bijective type} satisfies
Z(o) >= hat1B(0)(p-2k+1) - sum_{rho!=0}|hat1B(rho)| ((2k-2) sqrt p + 2k-1)   (one-variable Weil).
So Z(o) > 0 once sqrt(p) > (2k-2) L + small, L = sum_{rho!=0}|hat1B(rho)| / hat1B(0).
Here B = bijective types (U,V) in the type group Z_k^{2k}/(shifts); computed exactly."""
import itertools, math, sys
import numpy as np
for k in map(int, sys.argv[1:]):
    om = np.exp(2j * np.pi / k)
    allr = np.array(list(itertools.product(range(k), repeat=k)))
    P = np.zeros(len(allr), dtype=complex)
    for sg in itertools.permutations(range(k)):
        P += om ** ((allr * np.array(sg)).sum(1) % k)
    A = np.abs(P)
    ok = (allr.sum(1) % k == 0)  # characters of the type group need sum r = 0
    a0 = A[0]
    S = A[ok].sum()
    L = (S * S - a0 * a0) / (a0 * a0)
    X = ((2 * k - 2) * L) ** 2
    print('k=%d  L=%.4g  pointwise-rainbow threshold ~ ((2k-2)L)^2 = %.3e   vs  T_A ~ (k-1)k^k = %.3e   (ek)^(2k) = %.3e' % (k, L, X, (k - 1) * k ** k, (math.e * k) ** (2 * k)))

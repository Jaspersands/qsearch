import sys; sys.path.insert(0, '.')
from gm import *
print("K | T_A | T_A/K^K | T_C | best m | T_C/K^K | T_A/T_C | (K-1)K^K/T_C")
for K in list(range(3, 21)) + [23, 29, 31, 37, 40, 43, 53, 60, 71, 100, 200]:
    kk = mp.mpf(K) ** K
    ta = TA(K); tc, m = TC(K)
    print(K, "|", mp.nstr(ta, 7), "|", mp.nstr(ta / kk, 6), "|", mp.nstr(tc, 7), "|", m, "|",
          mp.nstr(tc / kk, 6), "|", mp.nstr(ta / tc, 5), "|", mp.nstr((K - 1) * kk / tc, 5), flush=True)

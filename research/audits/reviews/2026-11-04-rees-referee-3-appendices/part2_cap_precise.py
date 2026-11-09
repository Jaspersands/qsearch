"""Referee 3: per-node trial cap of Theorem free-coordinate(ii) at a_d = g_d, to 4 decimals."""
from math import gcd, log2, log, ceil
g = {2: 17, 3: 16, 4: 14, 5: 12, 6: 9, 7: 6, 8: 3, 9: 1}
B = 56
for p in [5281, 105019, 2**31 - 1, 2**61 - 1, 194522647344910884721, 2**127 - 1]:
    best = max((log2(ceil(2*B*log(2)*((p)/((p-1)//gcd(d,p-1)+1))**g[d])), d, gcd(d,p-1)) for d in g)
    print(p, "max log2 cap %.4f at grade %d (kappa=%d)" % best)

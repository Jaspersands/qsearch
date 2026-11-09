"""Query exponent of Theorem free-coordinate(iii) with weight-doubling nodes at every grade.

For class c and prime p > c: grade d has kappa_d = gcd(d, p-1), h_d = (p-1)/kappa_d.
  kappa_d = 1           -> linear node, degree 1;
  kappa_d = p-1 (Gamma_0, d = p-1) -> binary weight-doubling node, degree 1 + ceil(log2(p-1));
  otherwise (Gamma_F)   -> mu_h-digit node, degree 1 + J(h_d, p).
E_new(c, p) = 1 + sum_d degree_d (the 1 is S ~ m; g_d <= m; log factors not counted).
For p beyond P(c) = max_{kappa <= c} ((kappa-1)(kappa-2)+3)^2 every Gamma_F grade has J = 1
(Weil), so E_new(c, p) = 1 + sum_d (1 + [kappa_d >= 2]) there; the scan covers p <= P(c).
Also: Schedule 1 degrees kappa ceil(log2(kappa+1)) at the same grades (as a reference only).

Usage: python run_exponent.py out.json
"""
import json
import math
import sys
from sympy import primerange
from wh_lib import depth_fft

out = {}
cache = {}


def J(h, p):
    if (h, p) not in cache:
        cache[(h, p)] = depth_fft(h, p)[0]
    return cache[(h, p)]


for c in range(2, 13):
    P = max(((k - 1) * (k - 2) + 3) ** 2 for k in range(1, c + 1))
    best = (-1, None)
    s1best = (-1, None)
    rows = {}
    for p in primerange(c + 1, P + 2):
        e, s1 = 1, 1
        for d in range(2, c + 1):
            k = math.gcd(d, p - 1)
            if k == 1:
                e += 1
                s1 += 1
            elif k == p - 1:
                e += 1 + math.ceil(math.log2(p - 1))
                s1 += k * math.ceil(math.log2(k + 1))
            else:
                e += 1 + J((p - 1) // k, p)
                s1 += k * math.ceil(math.log2(k + 1))
        rows[p] = e
        if e > best[0]:
            best = (e, p)
        if s1 > s1best[0]:
            s1best = (s1, p)
    # beyond P: J = 1 at every Gamma_F grade
    beyond = 1 + sum(2 for d in range(2, c + 1))
    out[c] = {"scan_up_to": P, "max_exponent": best[0], "argmax_p": best[1],
              "exponent_beyond_scan_at_most": beyond,
              "schedule1_at_kappa_max_over_scan": s1best[0], "schedule1_argmax_p": s1best[1]}
    print(c, out[c], flush=True)

with open(sys.argv[1], "w") as f:
    json.dump(out, f, indent=1)

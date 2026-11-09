"""E_2(kappa) for kappa = 4..7 as stated in the paper (main.tex, prop:decoupled-sde paragraph).
E_2(6) is recomputed by e2six.py (complete search, every prime p = 1 mod 6 below 3000)."""
E2 = {4: [5, 13, 17, 29, 37, 53],
      5: [11, 31, 41, 61, 71, 101, 131, 151, 181],
      7: [int(x) for x in """29 43 71 113 127 197 211 239 281 337 379 421 449 463 491 547 617 631 659
    673 701 743 757 827 883 911 953 1009 1051 1093 1163 1289 1303 1373 1471
    1499 1583 1597 1667 1709 1877 2017 2087 2143 2213 2297 2339 2381 2423
    2591 2731 2801 2843 2969 3137 3221""".split()]}
try:
    import json, os
    E2[6] = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'e2six.json')))
except Exception:
    pass

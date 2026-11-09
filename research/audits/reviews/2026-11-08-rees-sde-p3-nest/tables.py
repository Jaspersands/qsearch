"""Guaranteed worst-case m(n) of WNEST (exact recursion from the per-piece bounds) against the
sharpened KOW-type recursion (wnest.kow_recursion, not KOW's own recursion (8)) and the closed form n^2/4 + (8/9)(n+2)^{3/2} + 4n + 12; then WNEST+ (Las Vegas
refinement with the same guarantee) on random instances [sampled]."""
import sys, math
import numpy as np
from wnest import Run, stream_random, guarantee, kow_recursion, pool_size

print("n     WNEST guarantee   closed form   sharpened KOW-type recursion   n^2/4    n^2/3   guarantee/n^2")
cross = None
for n in (16, 32, 64, 100, 128, 150, 200, 256, 400, 512, 1000, 2000, 4000):
    g, k = guarantee(n), kow_recursion(n)
    cf = n * n / 4 + (8 / 9) * (n + 2) ** 1.5 + 4 * n + 12
    print(f"{n:5d}  {g:12d}   {cf:11.0f}   {k:27d}   {n*n//4:7d}  {n*n//3:7d}   {g/n/n:.4f}")
    assert g <= cf, (n, g, cf)
for n in range(4, 3000):
    assert guarantee(n) <= n * n / 4 + (8 / 9) * (n + 2) ** 1.5 + 4 * n + 12
    if cross is None and guarantee(n) < kow_recursion(n):
        cross = n
print("closed form verified for 4 <= n < 3000; first n with WNEST guarantee < sharpened KOW-type recursion:", cross)
lose = [n for n in range(35, 3000) if guarantee(n) >= kow_recursion(n)]
print("n in [35,3000) with WNEST guarantee >= sharpened KOW-type recursion:", lose, len(lose))
print("pool_size(q) <= 1.5q + 2 sqrt(q) + 6 for 4 <= q < 3000:",
      all(pool_size(q) <= 1.5 * q + 2 * math.sqrt(q) + 6 for q in range(4, 3000)))

rng = np.random.default_rng(7)
print("\nWNEST+ (lightest of deterministic codeword and 300 samples with wt >= r*+2) on uniformly random instances [sampled]")
print(" n    m_used            m_used/n^2          max(|X|-q)")
for n in (30, 60, 90, 120, 150):
    ms, mx = [], []
    for rep in range(3 if n <= 90 else 2):
        R = Run(n, stream_random(n, rng), "wnest+", rng=rng)
        assert R.run(rng) is not None
        ms.append(len(R.stream)); mx.append(max(c[2] - c[0] for c in R.costs if c[1] == 2))
    print(f"{n:3d}  {ms}  {[round(m/n/n, 4) for m in ms]}  {mx}")
    sys.stdout.flush()
print("all witnesses verified by direct summation")

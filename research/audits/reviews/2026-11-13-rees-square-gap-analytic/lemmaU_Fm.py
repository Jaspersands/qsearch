"""Lemma U, case a, b >= 2 at the worst case kappa = 3: F(m) > 0 for 4 <= m <= 10^6, where
F(m) = (2/3) c_m s0 - (m-2)^2/4 - (m^2/2 - m)/(3 s0) - m^2/(18 s0^2),
c_m = 2m/3 - 1 + 3^-m, s0 = max(c_m, sqrt 7).  (For m >= 100 the report gives an analytic bound.)"""
import numpy as np
m = np.arange(4, 10 ** 6 + 1, dtype=float)
c = 2 * m / 3 - 1 + 3.0 ** (-np.minimum(m, 600))
s0 = np.maximum(c, np.sqrt(7))
F = (2 / 3) * c * s0 - (m - 2) ** 2 / 4 - (m * m / 2 - m) / (3 * s0) - m * m / (18 * s0 * s0)
i = int(np.argmin(F))
print(f"min F(m) over 4..1e6 = {F[i]:.4f} at m = {int(m[i])}; F/m^2 at 1e6 = {F[-1]/m[-1]**2:.5f} (limit 8/27-1/4 = {8/27-0.25:.5f})")
print("F(4..12):", " ".join(f"{v:.3f}" for v in F[:9]))

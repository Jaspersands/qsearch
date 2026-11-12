"""Extension of malcev_fourier_ratio.py to |v| = 8.06 (R = 48). Finite check only.
Run: nice -n 19 /opt/anaconda3/bin/python malcev_fourier_ratio2.py"""
import math
from malcev_fourier_tv import law, heis_step, abel_step, tv_uniform
for h in [(4,7,0)]:
    R = int(round(6*math.hypot(h[0],h[1]))); T = R*R
    p, N = law(R, T, heis_step(h)); pa, _ = law(R, T, abel_step(h))
    print(f"h={h} |v|={math.hypot(h[0],h[1]):.2f} R={R} T={T}: TV Heis {tv_uniform(p,N):.4f}  TV abel {tv_uniform(pa,N):.4f}", flush=True)

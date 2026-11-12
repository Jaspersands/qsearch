"""TV(p_<h>, uniform) at fixed box-to-|v| ratio R = 6|v|, T = R^2.
Run: nice -n 19 /opt/anaconda3/bin/python malcev_fourier_ratio.py   (finite check only)"""
from malcev_fourier_tv import law, heis_step, abel_step, tv_uniform
for h in [(1,1,0),(1,2,0),(2,3,0),(3,5,0)]:
    import math
    R = int(round(6*math.hypot(h[0],h[1]))); T = R*R
    p, N = law(R, T, heis_step(h)); pa, _ = law(R, T, abel_step(h))
    print(f"h={h} |v|={math.hypot(h[0],h[1]):.2f} R={R} T={T}: TV Heis {tv_uniform(p,N):.4f}  TV abel {tv_uniform(pa,N):.4f}", flush=True)

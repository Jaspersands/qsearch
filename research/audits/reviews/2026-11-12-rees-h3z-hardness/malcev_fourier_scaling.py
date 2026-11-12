"""Scaling of single-copy Mal'cev-coordinate Fourier sampling information with |v|.

Run: nice -n 19 /opt/anaconda3/bin/python malcev_fourier_scaling.py
Finite check only (TRAPS 7). Uses law() from malcev_fourier_tv.py.
Prints TV(p_<h>, uniform) and TV between the laws of two hidden subgroups
<h>, <h'> with different directions, versus |v|, at fixed box.
"""
import numpy as np
from malcev_fourier_tv import law, heis_step, abel_step, tv_uniform

R, T = 24, 576
print(f"box R={R}, T={T}")
print(f"{'h':>12} {'|v|^2':>6} {'TV(<h>,1)':>10} {'TV abel':>8}")
laws = {}
for h in [(1,0,0),(1,1,0),(1,2,0),(1,3,0),(2,3,0),(1,4,0),(3,4,0),(1,5,0),(2,5,0),(4,5,0),(5,6,0)]:
    p, N = law(R, T, heis_step(h)); laws[h] = p
    pa, _ = law(R, T, abel_step(h))
    print(f"{str(h):>12} {h[0]**2+h[1]**2:>6} {tv_uniform(p,N):>10.4f} {tv_uniform(pa,N):>8.4f}")
print("\npairwise TV between laws of different directions:")
pairs = [((1,2,0),(2,1,0)),((2,3,0),(3,2,0)),((2,5,0),(5,2,0)),((4,5,0),(5,4,0)),((4,5,0),(5,6,0)),((1,5,0),(2,5,0))]
for h, g in pairs:
    print(f"{str(h):>10} vs {str(g):>10}: {0.5*np.abs(laws.get(h, law(R,T,heis_step(h))[0]) - laws.get(g, law(R,T,heis_step(g))[0])).sum():.4f}")
print("\nsame direction, different central parameter c:")
for c2 in [1, 2, 7]:
    p1 = law(R, T, heis_step((2,3,0)))[0]; p2 = law(R, T, heis_step((2,3,c2)))[0]
    print(f"(2,3,0) vs (2,3,{c2}): {0.5*np.abs(p1-p2).sum():.4f}")

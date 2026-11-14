#!/usr/bin/env python3
"""Positive control for the rc_631.py DFS at D = 7: first prime p = 1 mod 7 (p > 700) with TL7."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from rc_631 import available_scaled
from rc_exhaust import least_prim_root, verify
p = 701
while True:
    p += 7
    if all(p % q for q in range(2, int(p**.5) + 1)):
        xi = least_prim_root(p)
        r, n = available_scaled(p, 7, xi)
        if r:
            verify(p, 7, list(range(7)), [0], r[0], r[1], xi)
            print(f"TL7 first available at p={p} (xi={xi}), witness verified beta={r[0]} alpha={r[1]}")
            break
        print(f"TL7 at {p}: NONE ({n} nodes)", flush=True)
    if p > 60000:
        print("no TL7 below 60000"); break

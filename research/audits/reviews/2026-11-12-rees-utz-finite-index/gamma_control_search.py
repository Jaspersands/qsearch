#!/usr/bin/env python
"""Search for H of finite index in UT_n(Z) with Gamma(N') not inside H, N' = prod e_ij.
(Control for the (n-1)! factor in M = (n-1)! N'.)  Run: nice -n 19 /opt/anaconda3/bin/python gamma_control_search.py"""
import math, random
import utz_e2e_check as U
rng = random.Random(4242)
for (n, M0, T) in [(3, 8, 3000), (3, 16, 2000), (3, 9, 2000), (4, 8, 1500), (4, 4, 2000), (4, 9, 1000), (5, 4, 800), (5, 8, 300), (3, 27, 1000)]:
    bad = tot = 0
    ex = None
    for _ in range(T):
        inst = U.Instance(n, M0, rng)
        if inst.N == 1:
            continue
        GZ = inst.GZ; fI = inst.f(GZ.one)
        per = {}
        for p in GZ.pos:
            t = 1
            while inst.f(GZ.elem(p, t)) != fI:
                t += 1
            per[p] = t
        Np = math.prod(per.values())
        tot += 1
        if not all(inst.f(GZ.elem(p, Np)) == fI for p in GZ.pos):
            bad += 1
            if ex is None:
                ex = (inst.N, per)
    print(f"n={n} M0={M0}: Gamma(N') not in H in {bad}/{tot}" + (f"; example N={ex[0]} periods={ex[1]}" if ex else ""), flush=True)

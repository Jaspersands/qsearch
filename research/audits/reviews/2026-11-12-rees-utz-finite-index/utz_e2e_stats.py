#!/usr/bin/env python
"""Instance statistics for utz_e2e_check.py (same generator, different seed).

Records, per instance, whether H is normal in UT_n(Z), whether a prime q >= n divides
[G:H] (the branch that needs Cor. cor:black-box-pe, i.e. Theorem thm:main), the
quotient class of G/Core(H) is not computed.  Re-runs the reduction and the
<output> = H check.  Run: nice -n 19 /opt/anaconda3/bin/python utz_e2e_stats.py [trials] [cap]
"""
import math, random, sys
import utz_e2e_check as U

def main():
    trials = int(sys.argv[1]) if len(sys.argv) > 1 else 15
    U.NCAP = int(sys.argv[2]) if len(sys.argv) > 2 else 1500
    rng = random.Random(777)
    configs = [(4, 10), (4, 15), (4, 25), (4, 30), (5, 10), (4, 35)]
    rows = []
    for (n, M0) in configs:
        for _ in range(trials):
            for _a in range(300):
                inst = U.Instance(n, M0, rng)
                if 1 < inst.N <= U.NCAP:
                    break
            else:
                continue
            per, Np, M, out = U.run_reduction(inst, True, rng)
            res = U.check_instance(inst, per, Np, M, out, rng)
            GZ = inst.GZ
            fI = inst.f(GZ.one)
            normal = True
            for h in out:
                for p in GZ.pos:
                    for s in (1, -1):
                        x = GZ.elem(p, s)
                        if inst.f(GZ.mul(GZ.mul(GZ.inv(x), h), x)) != fI:
                            normal = False
            bigq = [q for q in U.factor(inst.N) if q >= n]
            rows.append((n, M0, inst.N, normal, bool(bigq), all(res.values())))
    tot = len(rows)
    print(f"instances: {tot}")
    print(f"all checks pass: {sum(r[5] for r in rows)}/{tot}")
    print(f"non-normal H: {sum(not r[3] for r in rows)}/{tot}")
    print(f"a prime q >= n divides [G:H] (Rees branch exercised): {sum(r[4] for r in rows)}/{tot}")
    print(f"non-normal AND q >= n divides index: {sum((not r[3]) and r[4] for r in rows)}/{tot}")
    print("sample indices:", sorted(set(r[2] for r in rows))[:30])

if __name__ == '__main__':
    main()

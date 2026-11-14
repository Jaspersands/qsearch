"""Draft helper (2026-11-14): the four small rows of tab:query-crossover recomputed with the
Schedule 1H+ arities A+_2(a) = (a+1)^2 (every odd p) and A+_3(a) = (a+1)(2a+1) at p = 1 (mod 3)
(chain (GE; TL_3), available at every prime p = 1 (mod 3): Lemma plus-sm for p >= 430, certificates
below), a+1 at p = 2 (mod 3).  Crossover logic copied from
2026-11-13-rees-headline-38-applied/halved_schedule.py (lines 258-313); classical_lb.py imported read-only.
Control: with the Schedule 1H arities (A_3(a) = G(3,a) = 27(a+1)^3 at p = 1 mod 3) it must reproduce
the core's table (14.83/863/305/163, 17.68/431/196/221, 18.91/41/27/350; Heisenberg 5.00/29/none/50)."""
import math, sys, importlib.util
from fractions import Fraction
from pathlib import Path
ROOT = Path(__file__).resolve().parents[4]
spec = importlib.util.spec_from_file_location("classical_lb", ROOT / "research/audits/reviews/2026-11-02-rees-classical-lower-bound/classical_lb.py")
CL = importlib.util.module_from_spec(spec); spec.loader.exec_module(CL)
def closed_Q_int(p, m, eps_num=1, eps_den=3):
    t = 0
    while p ** t * eps_num < 2 * eps_den: t += 1
    ln = math.log(2 * eps_den / eps_num); w = max(2 * (1 + t), 15)
    return 5 * (m + t) + 16 * math.ceil(ln) + CL.isqrt_ceil(2 * w * p ** (m - 1))
def closed_Q_exact8l(p, m): return CL.closed_form_Q(p, m, Fraction(1, 3))
def row(name, m, Qq):
    ok = lambda x: CL.classical_lb(x, m) > Qq
    hi = 11
    while not ok(hi): hi *= 2
    lo = 11
    while lo < hi:
        mid = (lo + hi) // 2
        if ok(mid): hi = mid
        else: lo = mid + 1
    px = lo
    while not CL.is_prime(px): px += 1
    lo2, hi2 = 11, 11
    while closed_Q_int(hi2, m) < Qq: hi2 *= 2
    while lo2 < hi2:
        mid = (lo2 + hi2) // 2
        if closed_Q_int(mid, m) >= Qq: hi2 = mid
        else: lo2 = mid + 1
    q = 11
    while closed_Q_exact8l(q, m) < Qq: q += 1
    print(f"{name:22s} m={m} Q_q={Qq} log2={math.log2(Qq):.2f} LB>Q from {px}  (v)<Q for p< {lo2}  "
          f"exact-8l first integer {q}  copies {CL.ehk_copies(px, m)}")
A2 = lambda a: (a + 1) ** 2
for label, A3 in (("Schedule 1H (control)", lambda a: 27 * (a + 1) ** 3), ("Schedule 1H+", lambda a: (a + 1) * (2 * a + 1))):
    print("==", label)
    row("Heisenberg", 3, 2 * (3 + 1) * A2(1))
    row("filiform", 4, 3 * (4 + 1) * A2(2) * A3(1))
    row("free, two generators", 5, 3 * (5 + 1) * A2(3) * A3(2))
    row("Dixmier-Lister", 8, 3 * (8 + 1) * A2(4) * A3(2))

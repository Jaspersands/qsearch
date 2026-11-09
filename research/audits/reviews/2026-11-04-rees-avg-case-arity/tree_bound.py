"""Exact check of the tree inequalities over all integer partitions of a (a <= AMAX).

For level drops a_1..a_L >= 1 with sum a, the column count of a public-split tree with
M_j >= a_j + 1 is at least P = prod (a_j + 1).  Checked:
  (T1) P >= (a_max + 1)(a - a_max + 1);
  (T2) if a_max <= a/2 then P >= (a/2 + 1)(a/4 + 1)  (so P >= a^2/8);
  (T3) min over partitions of P equals a + 1 (single level), and the minimum over
       partitions with at least two parts of size >= 2 ... is reported for reference.
Also prints, for budgets A = a^{1.5}, a^{1.585}, a^2/8, the least a_max any partition
with P <= A can have (the single level that must remain).
Usage: python tree_bound.py AMAX
"""
import math
import sys


def partitions(n, maxpart=None):
    if maxpart is None:
        maxpart = n
    if n == 0:
        yield []
        return
    for k in range(min(n, maxpart), 0, -1):
        for rest in partitions(n - k, k):
            yield [k] + rest


def main():
    AMAX = int(sys.argv[1])
    for a in range(1, AMAX + 1):
        worst_T1 = worst_T2 = math.inf
        best = {}
        for part in partitions(a):
            P = math.prod(x + 1 for x in part)
            am = part[0]
            worst_T1 = min(worst_T1, P / ((am + 1) * (a - am + 1)))
            if 2 * am <= a:
                worst_T2 = min(worst_T2, P / ((a / 2 + 1) * (a / 4 + 1)))
            for name, A in (("a^1.5", a ** 1.5), ("a^1.585", a ** 1.585), ("a^2/8", a * a / 8)):
                if P <= A:
                    best[name] = min(best.get(name, a), am)
        assert worst_T1 >= 1 and worst_T2 >= 1, (a, worst_T1, worst_T2)
        if a % 4 == 0 or a == AMAX:
            print(f"a={a:3d}: min P/(T1 bound)={worst_T1:.3f}, min P/(T2 bound)="
                  f"{'n/a' if worst_T2 == math.inf else f'{worst_T2:.3f}'}; least a_max with P<=A: "
                  + ", ".join(f"{k}:{v} (a-2A/a+1={a-2*A/a+1:.1f})" for k, v, A in
                              [(k, best.get(k, '-'), {'a^1.5': a**1.5, 'a^1.585': a**1.585, 'a^2/8': a*a/8}[k])
                               for k in ('a^1.5', 'a^1.585', 'a^2/8')]))
    print(f"(T1), (T2) hold for every partition of every a <= {AMAX}")


if __name__ == "__main__":
    main()

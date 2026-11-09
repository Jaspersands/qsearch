"""Tabulate witness symmetry types by kappa, h-parity and p / kappa^((kappa+1)/2).

Symmetry types (section 1 of the note):
  H  : shift-scale symmetry (r,t) = (K/2, K/2), lambda = -1   (half-shift family)
  S* : any other shift-scale symmetry (always found together with H here)
  P  : transpose symmetry with lambda = -1 and a + b = 0 mod K  (Paley / zero-cell family)
  T1 : transpose symmetry with lambda = 1 and a + b = 0          (symmetric family)
  G  : none of these (generic)
Usage: python witness_table.py FILE [FILE ...]
"""
import sys
from collections import defaultdict
from witness_structure import parse, analyse


def classify(K, p, o):
    types = set()
    for (r, t, lam) in o["shift_sym"]:
        if K % 2 == 0 and r == K // 2 and t == K // 2 and lam == p - 1:
            types.add("H")
        else:
            types.add("S*")
    for (a, b, lam) in o["transpose_sym"]:
        if (a + b) % K == 0 and lam == p - 1:
            types.add("P")
        elif (a + b) % K == 0 and lam == 1:
            types.add("T1")
        else:
            types.add("T*")
    return types or {"G"}


def main():
    data = parse(sys.argv[1:])
    tab = defaultdict(lambda: defaultdict(int))
    rows = []
    for (K, p), (g, alpha, beta) in sorted(data.items()):
        o = analyse(K, p, g, alpha, beta)
        ty = classify(K, p, o)
        hpar = "h even" if ((p - 1) // K) % 2 == 0 else "h odd"
        ratio = p / K ** ((K + 1) / 2)
        band = "<=2" if ratio <= 2 else ">2"
        for t in ty:
            tab[(K, hpar, band)][t] += 1
        tab[(K, hpar, band)]["n"] += 1
        rows.append((K, p, hpar, round(ratio, 3), o["zeros"], "+".join(sorted(ty))))
    print("per-witness: K p h-parity p/K^((K+1)/2) zeros types")
    for r in rows:
        print(*r)
    print()
    print("summary: K, h-parity, band of p/K^((K+1)/2): n and counts per type")
    for key in sorted(tab):
        d = tab[key]
        print(key, "n=%d" % d["n"], {k: v for k, v in sorted(d.items()) if k != "n"})


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Independent CNF encoding of l-level Omega-contractions (core Def. plus-ell), cell-value form.

Written 2026-11-14 from the statement of Definition plus-ell of main-core.tex only (it does not
import or copy sat3.py / sat3_stream.py / rc3_sat.py, which use the F1+F2+F3 parametrisation with
gauge fixing).

Reduction used (proved in the report, section 2):
  (iii) <=> C lies in Ann(W^{(x)l}) = sum_r F^{(x)(r-1)} (x) span(z) (x) F^{(x)(l-r)}
        <=> B(y) := C_y / z^y has vanishing l-fold mixed difference prod_r (1 - E_r) B = 0,
            where E_r sets y_r := 0.
  (i)   <=> B(y) = 0 or cl(B(y)) in Omega - |y|          (cl(z^y) = |y| mod kappa)
  (ii)  <=> B(0) in P; by scaling with B(0)^{-1} in P we fix B(0) = 1 (classes and (iii) unchanged).
Variables: one-hot cell values B(y) over their allowed sets (all l-tuples y), plus auxiliary
partial sums for l = 3. No gauge fixing other than B(0) = 1.

usage: cellsat.py p kappa l OMEGA out.cnf [xi]
   OMEGA: comma list of classes, e.g. 0  or 0,4
"""
import sys, itertools, json


def is_prim_root(g, p):
    n = p - 1
    fs = [q for q in range(2, n + 1) if n % q == 0 and all(q % r for r in range(2, int(q ** .5) + 1))]
    return all(pow(g, n // q, p) != 1 for q in fs)


def least_prim_root(p):
    for g in range(2, p):
        if is_prim_root(g, p):
            return g


def classes(p, kappa, xi):
    """cl[x] in Z_kappa for x in F_p^*, via x^{(p-1)/kappa} compared with powers of xi^{(p-1)/kappa}."""
    h = (p - 1) // kappa
    base = pow(xi, h, p)
    tab = {}
    acc = 1
    for i in range(kappa):
        tab[acc] = i
        acc = acc * base % p
    assert len(tab) == kappa, "xi does not generate F_p^*/P_kappa"
    return {x: tab[pow(x, h, p)] for x in range(1, p)}


def build(p, kappa, l, Omega, xi):
    cl = classes(p, kappa, xi)
    cells = list(itertools.product(range(kappa), repeat=l))

    def dom(y):
        if all(c == 0 for c in y):
            return [1]
        s = sum(y) % kappa
        allowed = {(k - s) % kappa for k in Omega}
        return [0] + [x for x in range(1, p) if cl[x] in allowed]

    nv = [0]
    def new():
        nv[0] += 1
        return nv[0]
    var = {}
    for y in cells:
        var[y] = {v: new() for v in dom(y)}
    clauses = []
    for y in cells:
        vs = list(var[y].values())
        clauses.append(vs)
        for i in range(len(vs)):
            for j in range(i + 1, len(vs)):
                clauses.append([-vs[i], -vs[j]])
    nz = range(1, kappa)
    if l == 2:
        for m1 in nz:
            for m2 in nz:
                y = (m1, m2)
                for a, va in var[(m1, 0)].items():
                    for b, vb in var[(0, m2)].items():
                        t = (a + b - 1) % p
                        lit = var[y].get(t)
                        clauses.append([-va, -vb] + ([lit] if lit else []))
    elif l == 3:
        Z = (0, 0, 0)
        R12 = {}
        for m1 in nz:
            for m2 in nz:
                aux = {}
                for a, va in var[(m1, m2, 0)].items():
                    for b, vb in var[(m1, 0, 0)].items():
                        for c, vc in var[(0, m2, 0)].items():
                            r = (a - b - c + 1) % p
                            if r not in aux:
                                aux[r] = new()
                            clauses.append([-va, -vb, -vc, aux[r]])
                R12[(m1, m2)] = aux
        R13 = {}
        for m1 in nz:
            for m3 in nz:
                aux = {}
                for a, va in var[(m1, 0, m3)].items():
                    for b, vb in var[(0, 0, m3)].items():
                        r = (a - b) % p
                        if r not in aux:
                            aux[r] = new()
                        clauses.append([-va, -vb, aux[r]])
                R13[(m1, m3)] = aux
        for m1 in nz:
            for m2 in nz:
                for m3 in nz:
                    y = (m1, m2, m3)
                    T = {}
                    for r, vr in R12[(m1, m2)].items():
                        for s, vs in R13[(m1, m3)].items():
                            t = (r + s) % p
                            if t not in T:
                                T[t] = new()
                            clauses.append([-vr, -vs, T[t]])
                    for t, vt in T.items():
                        for c, vc in var[(0, m2, m3)].items():
                            u = (t + c) % p
                            lit = var[y].get(u)
                            clauses.append([-vt, -vc] + ([lit] if lit else []))
    else:
        raise SystemExit("l must be 2 or 3")
    return nv[0], clauses, var


def main():
    p, kappa, l = map(int, sys.argv[1:4])
    Omega = sorted({int(x) % kappa for x in sys.argv[4].split(',')})
    assert 0 in Omega
    out = sys.argv[5]
    xi = int(sys.argv[6]) if len(sys.argv) > 6 else least_prim_root(p)
    assert (p - 1) % kappa == 0
    n, clauses, var = build(p, kappa, l, Omega, xi)
    with open(out, 'w') as f:
        f.write(f"c cellsat p={p} kappa={kappa} l={l} Omega={Omega} xi={xi}\n")
        f.write(f"p cnf {n} {len(clauses)}\n")
        for c in clauses:
            f.write(' '.join(map(str, c)) + ' 0\n')
    with open(out + '.map.json', 'w') as f:
        json.dump({'p': p, 'kappa': kappa, 'l': l, 'Omega': Omega, 'xi': xi,
                   'var': {','.join(map(str, y)): {str(v): x for v, x in d.items()} for y, d in var.items()}}, f)
    print(f"p={p} kappa={kappa} l={l} Omega={Omega} xi={xi} vars={n} clauses={len(clauses)}")


if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""Decode a SAT model of cellsat.py and check it directly against Definition plus-ell.

The check does not use the B-form: it rebuilds C_y = xi^{y_1+...+y_l} B(y) and tests
 (i)  cl(C_y) in Omega for C_y != 0   (class via a discrete-log table of xi, not via powering)
 (ii) C_0 in P
 (iii) C paired with every basis tensor (x)_r (e_{m_r} - z_{m_r} e_0), m in (Z_kappa \\ 0)^l, is 0.
usage: check_table.py out.cnf.map.json model.txt     (model = solver stdout with 'v' lines)
"""
import sys, json, itertools


def main():
    mp = json.load(open(sys.argv[1]))
    p, kappa, l, Omega, xi = mp['p'], mp['kappa'], mp['l'], set(mp['Omega']), mp['xi']
    true = set()
    for line in open(sys.argv[2]):
        if line.startswith('v'):
            true.update(int(t) for t in line.split()[1:] if int(t) > 0)
    dlog = {}
    x = 1
    for e in range(p - 1):
        dlog[x] = e
        x = x * xi % p
    assert len(dlog) == p - 1, "xi is not a primitive root (checker assumes one)"
    B = {}
    for key, d in mp['var'].items():
        y = tuple(map(int, key.split(',')))
        vals = [int(v) for v, lit in d.items() if lit in true]
        assert len(vals) == 1, (y, vals)
        B[y] = vals[0]
    z = [pow(xi, m, p) for m in range(kappa)]
    C = {y: pow(xi, sum(y), p) * B[y] % p for y in B}
    bad = 0
    for y, c in C.items():
        if c and dlog[c] % kappa not in Omega:
            bad += 1
    assert C[(0,) * l] and dlog[C[(0,) * l]] % kappa == 0, "(ii) fails"
    nbad3 = 0
    for m in itertools.product(range(1, kappa), repeat=l):
        s = 0
        for S in itertools.product((0, 1), repeat=l):
            y = tuple(0 if S[r] else m[r] for r in range(l))
            coef = 1
            for r in range(l):
                if S[r]:
                    coef = coef * (-z[m[r]]) % p
            s = (s + coef * C[y]) % p
        if s:
            nbad3 += 1
    nnz = sum(1 for c in C.values() if c)
    print(f"p={p} kappa={kappa} l={l} Omega={sorted(Omega)} xi={xi}: class failures {bad}, "
          f"(iii) failures {nbad3} of {(kappa-1)**l}, nonzero cells {nnz}/{len(C)} -> "
          + ("VERIFIED" if bad == 0 and nbad3 == 0 else "FAILED"))


if __name__ == '__main__':
    main()

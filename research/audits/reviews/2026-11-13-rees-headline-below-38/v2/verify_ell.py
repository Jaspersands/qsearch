"""v2: third, independent check of the l-level {0}-contraction tables of 2026-11-13-rees-k9-below-21
(read-only).  Written from the definition (k9-below-21 Sec. 2), sharing no code with that folder.
Table key y (digit string), value B(y); C(y) = g^{|y|} B(y), g = least primitive root (certs.prim_root,
factorisation of p-1).  Checks, exactly over F_p:
 (iii) A^{(x) l} C = 0, where A: F_p^k -> F_p^{k-1}, (A x)_m = x_m - z_m x_0 (m = 1..k-1), z_m = g^m.
       Rows of A span the dual of ker(sum_m z_m x_m) (z_0 = 1), so this is 'C annihilates every X
       satisfying all axis relations' (that set is the l-fold tensor power of the kernel).
       Applied axis by axis (contraction), not via the basis tensors used by verify_full_basis.py.
 (i)   every nonzero C(y) is a k-th power: C(y)^((p-1)/k) = 1  (class 0; no discrete logs).
 (ii)  C(0) != 0.
Negative controls: perturbed tables, the wrong generator, and K = {1} read as class-1 test."""
import json, sys, os, itertools
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
from certs import prim_root

def load(path):
    tab = json.load(open(path))
    l = len(next(iter(tab)))
    return tab, l

def check(p, k, tab, l, g=None, cls=0):
    g = prim_root(p) if g is None else g
    z = [pow(g, m, p) for m in range(k)]
    C = np.zeros((k,) * l, dtype=object)
    for key, b in tab.items():
        y = tuple(int(c) for c in key)
        C[y] = pow(g, sum(y), p) * int(b) % p
    assert len(tab) == k ** l
    A = np.zeros((k - 1, k), dtype=object)
    for m in range(1, k):
        A[m - 1, m] = 1; A[m - 1, 0] = (-z[m]) % p
    T = C
    for ax in range(l):
        T = np.tensordot(A, T, axes=([1], [ax]))       # new axis 0; move to position ax
        T = np.moveaxis(T, 0, ax)
        T = np.vectorize(lambda v: v % p, otypes=[object])(T)
    nonzero_ann = int(sum(1 for v in T.flat if v % p))
    e = (p - 1) // k
    target = pow(g, e * cls, p)
    bad_cls = int(sum(1 for v in C.flat if v % p and pow(int(v), e, p) != target))
    c0 = int(C[(0,) * l])
    ok = nonzero_ann == 0 and bad_cls == 0 and c0 != 0
    return ok, nonzero_ann, bad_cls, c0, int(sum(1 for v in C.flat if v % p))

SRC = os.path.join(HERE, '..', '..', '2026-11-13-rees-k9-below-21')
CASES = [(37, 9, 'B4_37.json'), (19, 9, 'B4_19.json'), (73, 9, 'B4_73.json'),
         (13, 4, 'B3_13_4.json'), (13, 6, 'B3_13_6.json')]
NEG = [(37, 9, 'B4_37_perturbed.json'), (13, 4, 'B3_13_4_perturbed.json'), (13, 6, 'B3_13_6_perturbed.json')]
if __name__ == '__main__':
    for p, k, f in CASES:
        tab, l = load(os.path.join(SRC, f))
        ok, na, bc, c0, nz = check(p, k, tab, l)
        print(f'{f}: p={p} k={k} l={l} g={prim_root(p)}: nonzero entries of A^(x)l C: {na}/{(k-1)**l}, '
              f'non-k-th-power entries {bc}, C(0)={c0}, nonzero {nz}/{k**l} -> {"VERIFIED" if ok else "FAILED"}', flush=True)
    print('negative controls (each must FAIL):')
    for p, k, f in NEG:
        tab, l = load(os.path.join(SRC, f))
        ok, na, bc, c0, nz = check(p, k, tab, l)
        print(f'  {f}: ann {na}, cls {bc} -> {"VERIFIED (BAD CONTROL)" if ok else "FAILED (good)"}')
    for p, k, f in CASES:   # wrong generator: next primitive root
        g0 = prim_root(p)
        g1 = next(h for h in range(g0 + 1, p) if all(pow(h, (p - 1) // q, p) != 1 for q in {q for q in range(2, p) if (p - 1) % q == 0 and all(q % r for r in range(2, q))}))
        tab, l = load(os.path.join(SRC, f))
        ok, na, bc, c0, nz = check(p, k, tab, l, g=g1)
        print(f'  {f} with generator {g1} instead of {g0}: ann {na}, cls {bc} -> {"VERIFIED (BAD CONTROL)" if ok else "FAILED (good)"}')
    for p, k, f in CASES:   # read as class-1 table
        tab, l = load(os.path.join(SRC, f))
        ok, na, bc, c0, nz = check(p, k, tab, l, cls=1)
        print(f'  {f} as class-1 test: cls violations {bc} -> {"VERIFIED (BAD CONTROL)" if ok else "FAILED (good)"}')

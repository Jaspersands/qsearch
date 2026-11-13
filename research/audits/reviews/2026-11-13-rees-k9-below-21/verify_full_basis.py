#!/opt/anaconda3/bin/python
"""Second, independent verifier of an l-level K-contraction table (shares no code with ell_common.py / compose.py).

Input: JSON table key = digit string y (y in Z_k^l), value B(y).  Forms C(y) = g^{y_1+...+y_l} B(y) mod p and checks
  (1) <C, b_{r_1} (x) ... (x) b_{r_l}> = 0 for ALL (k-1)^l basis tensors of W^{(x)l}, b_r = e_r - g^r e_0 (exact);
  (2) every nonzero C(y) has class in K, by a discrete-log table built by repeated multiplication;
  (3) C(0) != 0.
usage: verify_full_basis.py p k K table.json
"""
import sys, json, itertools

p, k = int(sys.argv[1]), int(sys.argv[2])
K = {int(x) % k for x in sys.argv[3].split(',')}
tab = json.load(open(sys.argv[4]))
l = len(next(iter(tab)))
g = next(h for h in range(2, p) if len({pow(h, e, p) for e in range(p - 1)}) == p - 1)
dl, x = {}, 1
for e in range(p - 1):
    dl[x] = e
    x = x * g % p
C = {}
for key, b in tab.items():
    y = tuple(int(c) for c in key)
    C[y] = pow(g, sum(y), p) * b % p
assert len(C) == k ** l
zs = [pow(g, r, p) for r in range(k)]
bad_ann = 0
for rs in itertools.product(range(1, k), repeat=l):
    s = 0
    for mask in range(1 << l):       # b_r has entries 1 at r and -z_r at 0
        y, coef = [], 1
        for t in range(l):
            if (mask >> t) & 1:
                y.append(0); coef = coef * (-zs[rs[t]]) % p
            else:
                y.append(rs[t])
        s += coef * C[tuple(y)]
    bad_ann += s % p != 0
bad_cls = sum(1 for y, c in C.items() if c and dl[c] % k not in K)
ok = bad_ann == 0 and bad_cls == 0 and C[(0,) * l] != 0
print(f'p={p} k={k} K={sorted(K)} l={l} g={g}: basis tensors not annihilated {bad_ann}/{(k-1)**l}, '
      f'class violations {bad_cls}, C(0)={C[(0,)*l]}, nonzero {sum(1 for c in C.values() if c)}/{k**l}')
print('VERIFIED' if ok else 'FAILED')

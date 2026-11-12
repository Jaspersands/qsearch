#!/opt/anaconda3/bin/python
"""Independent, deterministic verifier of a sat3.py model (does not import sat3.py or exponents_hcd.py).

Reads a solver model ('v' lines) for the CNF written by `sat3.py p k K out.cnf`, decodes F1, F2, F3 using the
variable layout of sat3.py (variables 1.. in the order t = 1,2,3; a = 0..k-1; b = 0..k-1; value 0..p-1), and checks
  (a) each F(t,a,b) has exactly one true value variable,
  (b) B(i,j,l) = F1(j,l) + F2(i,l) + F3(i,j) is 0 or has class in K - (i+j+l)  (own discrete log, least primitive root),
  (c) B(0,0,0) != 0,
  (d) C(i,j,l) = z_i z_j z_l B(i,j,l), z_i = g^i, annihilates the full basis {b_r (x) b_s (x) b_t} of W^{(x)3},
      W = {w : sum_i z_i w_i = 0}, b_r = e_r - z_r e_0 (r = 1..k-1)  -- all (k-1)^3 basis tensors, exact.
Prints the decoded F tables and B's class pattern.  usage: verify_model.py p k K model.txt
"""
import sys, itertools

p, k = int(sys.argv[1]), int(sys.argv[2])
K = {int(x) % k for x in sys.argv[3].split(',')}
true = set()
for line in open(sys.argv[4]):
    if line.startswith('v'):
        true |= {int(x) for x in line.split()[1:] if int(x) > 0}
g = next(h for h in range(2, p) if len({pow(h, e, p) for e in range(p - 1)}) == p - 1)
dl = {pow(g, e, p): e for e in range(p - 1)}
F, ok, v = {}, True, 0
for t in (1, 2, 3):
    for a in range(k):
        for b in range(k):
            vals = [u for u in range(p) if v + 1 + u in true]
            v += p
            if len(vals) != 1:
                ok = False
                print('one-hot violated at', (t, a, b), vals)
            F[(t, a, b)] = vals[0] if vals else 0
B = {(i, j, l): (F[(1, j, l)] + F[(2, i, l)] + F[(3, i, j)]) % p for i, j, l in itertools.product(range(k), repeat=3)}
bad = [c for c, x in B.items() if x and (dl[x] + sum(c)) % k not in K]
ok &= not bad and B[(0, 0, 0)] != 0
z = [pow(g, i, p) for i in range(k)]
C = {c: z[c[0]] * z[c[1]] * z[c[2]] * x % p for c, x in B.items()}
def bvec(r):
    w = [0] * k
    w[r] = 1
    w[0] = (-z[r]) % p
    return w
basis = [bvec(r) for r in range(1, k)]
ann_bad = 0
for w1, w2, w3 in itertools.product(basis, repeat=3):
    s = 0
    for (i, j, l), c in C.items():
        if c and w1[i] and w2[j] and w3[l]:
            s += c * w1[i] * w2[j] * w3[l]
    ann_bad += s % p != 0
ok &= ann_bad == 0
print(f'p={p} k={k} K={sorted(K)} g={g}: class violations {len(bad)}, B(0,0,0)={B[(0,0,0)]}, '
      f'basis tensors not annihilated {ann_bad} of {(k-1)**3}, nonzero cells {sum(1 for x in B.values() if x)}/{k**3}')
print('VERIFIED' if ok else 'FAILED')
for t in (1, 2, 3):
    print(f'F{t} rows a=0..{k-1} (cols b):')
    for a in range(k):
        print('   ', ' '.join('%3d' % F[(t, a, b)] for b in range(k)))

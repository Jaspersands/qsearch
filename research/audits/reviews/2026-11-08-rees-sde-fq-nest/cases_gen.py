"""Case split for the two unit-direction functionals (Lemma U of the note): for S with P S = S and
lambda S cap S = {0} for lambda not in P (true for S = P u {0}), the slots gamma_{(r,0)}, gamma_{(0,r)}
(r = a non-P coset representative) are nonzero, and under the label symmetries (a,b) -> (lambda a,
mu b + nu a) together with the swap of the two unit directions, the pair of functionals
(w1, w2) = (gamma_{(r,0)}/r, gamma_{(0,r)}/r) is equivalent to one of
   (a, b), (a, g a) [g != 0], (b, g b) [g != 0], (b, a + g b) [g != 0]       (3p - 2 cases).
Prints the --fix strings (gamma = r * w)."""
import sys
from gadget_sat import parse_S
from gadget_cnf3 import cosets
p, Sspec = int(sys.argv[1]), sys.argv[2]
S = parse_S(p, Sspec)
P, creps = cosets(p, S)
r = creps[1]
A, B = (1, 0), (0, 1)
pairs = [(A, B)] + [(A, (g, 0)) for g in range(1, p)] + [(B, (0, g)) for g in range(1, p)] + [(B, (1, g)) for g in range(1, p)]
for w1, w2 in pairs:
    g1 = tuple((r * x) % p for x in w1); g2 = tuple((r * x) % p for x in w2)
    print(f'1,0,1:{g1[0]},{g1[1]};0,1,1:{g2[0]},{g2[1]}')

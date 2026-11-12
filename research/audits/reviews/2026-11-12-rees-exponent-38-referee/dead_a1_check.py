"""N(8,1,41): least n such that every n columns in F_41 admit nonzero x in (P8 u 0)^n with sum x_b lam_b = 0."""
import itertools
p = 41; P = sorted({pow(u, 8, p) for u in range(1, p)}); g = 6
Q = [sorted({pow(g, m, p) * x % p for x in P}) for m in range(8)]
def dead(classes):
    reach = {0: False}  # value -> achieved with nonzero
    for c in classes:
        new = dict(reach)
        for v, nz in reach.items():
            for y in Q[c]:
                w = (v + y) % p
                if w not in new or not new[w]: new[w] = True
        reach = new
    return not reach.get(0, False)
for n in range(1, 7):
    deads = [cl for cl in itertools.combinations_with_replacement(range(8), n) if dead(cl)]
    print(n, 'dead class-multisets:', len(deads), deads[:6])
    if not deads: print('N(8,1,41) =', n); break

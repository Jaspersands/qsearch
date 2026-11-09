"""Exact normalization/failure controls, not a random-ensemble sampler."""
from itertools import product

q = 3
xs = list(product(range(q), repeat=2))
for label, old, expected in [
    ("nonconstant", [(x,z) for x,z in xs if (x+z)%q], QQ(1)/6),
    ("zero_boundary", [(x,z) for x,z in xs if x == z], QQ(1)/3),
]:
    new = [s for s in old if s[0] != 0]
    po = {z: QQ(sum(s[1] == z for s in old))/len(old) for z in range(q)}
    pn = {z: QQ(sum(s[1] == z for s in new))/len(new) for z in range(q)}
    w = {z: QQ(sum(s[1] == z for s in new))/sum(s[1] == z for s in old)
         for z in range(q)}
    p = QQ(len(new))/len(old)
    tv = sum(abs(po[z]-pn[z]) for z in range(q))/2
    identity = sum(po[z]*abs(w[z]-p) for z in range(q))/(2*p)
    assert tv == identity == expected
    print(label, "p", p, "conditional probabilities", w, "exact TV", tv)

# All original offsets and prefixes, including empty final targets.
rows = [(1,1), (1,2), (1,0)]
counts = {}
for i in range(4):
    for J in product(range(q), repeat=i):
        z = sum(all((sum(a*b for a,b in zip(row,x))+j)%q
                    for row,j in zip(rows,J)) for x in xs)
        counts[J] = QQ(z)/(q**2*(QQ(2)/3)**i)
for i in range(3):
    for J in product(range(q), repeat=i):
        assert sum(counts[J+(j,)] for j in range(q))/q == counts[J]
        for j in range(q):
            if counts[J]:
                p = (QQ(2)/3)*counts[J+(j,)]/counts[J]
                assert counts[J+(j,)] == counts[J]*p/(QQ(2)/3)
assert len(counts) == 40
print("40 prefix counts: martingale and planted-density cancellation exact")

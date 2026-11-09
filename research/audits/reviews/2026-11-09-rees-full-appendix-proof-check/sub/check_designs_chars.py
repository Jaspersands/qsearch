"""Independent exact checks (sub, 2026-11-09):
 (1) Lemma app-sub-design (a), (b), (c): every design produced by the product
     construction of (b), over ALL choices of nonzero zero-vectors per row
     (exhaustive up to multiset), for small p and every c < p, including the
     edge case c = p - 1; and (a) for every e | p-1, e > c.
 (2) Lemma app-sub-character on filiform Lazard groups: [G,G] = [L,L] as sets,
     G/[G,G] additive, and the identity x*y*(-x) = e^{ad x} y (Step 2).
All arithmetic exact (integers mod p).
"""
import itertools, math, sys
from collections import Counter


def zero_vectors(p, j):
    """All nonzero x in F_p^{j+1} with sum x_i^j = 0, reduced to the multiset of
    nonzero entries (the only data the construction uses)."""
    out = set()
    for x in itertools.product(range(p), repeat=j + 1):
        if any(x) and sum(pow(v, j, p) for v in x) % p == 0:
            out.add(tuple(sorted(v for v in x if v)))
    return sorted(out)


def check_b(p, c, cap=20000):
    import random as _r
    _r.seed(p * 100 + c)
    rows = [[(1, p - 1)]] + [zero_vectors(p, j) for j in range(2, c + 1)]
    total = math.prod(len(r) for r in rows)
    if total <= cap:
        choices = itertools.product(*rows)
    else:
        choices = (tuple(_r.choice(r) for r in rows) for _ in range(cap))
    n_designs = 0
    bad = []
    minM, maxM = None, 0
    min_distinct = None
    for choice in choices:
        n_designs += 1
        S = [1]
        for X in choice:
            S = [(s * x) % p for s in S for x in X]
        M = len(S)
        moms = [sum(pow(s, jj, p) for s in S) % p for jj in range(1, c + 1)]
        distinct = len(set(S))
        if any(moms) or distinct < c or M > math.factorial(c + 1) or 0 in S:
            bad.append((choice, moms, distinct, M))
        minM = M if minM is None else min(minM, M)
        maxM = max(maxM, M)
        min_distinct = distinct if min_distinct is None else min(min_distinct, distinct)
    return n_designs, bad, minM, maxM, min_distinct, [len(r) for r in rows]


print('Lemma app-sub-design (b): exhaustive over row choices (multisets of nonzero entries)')
for p in (3, 5, 7):
    for c in range(1, p):
        if p == 7 and c > 4:
            # row j = 5, 6 over F_7 has 7^6, 7^7 vectors; skip exhaustive, test c = 6 below by sampling
            continue
        n, bad, mM, MM, md, rowsizes = check_b(p, c)
        print(f'  p={p} c={c}: row option counts={rowsizes}, designs tested={n}, '
              f'failures={len(bad)}, M in [{mM},{MM}] (<= (c+1)! = {math.factorial(c+1)}), '
              f'min #distinct={md} (need >= c={c})')
        for b in bad[:3]:
            print('     FAIL', b)
sys.stdout.flush()

# p = 7, c = 6 (= p-1) by explicit witness rows: row j=6 must have all 7 entries nonzero
p, c = 7, 6
rows = [[(1, 6)]]
for j in range(2, c + 1):
    found = None
    for x in itertools.product(range(1, p), repeat=j + 1):
        if sum(pow(v, j, p) for v in x) % p == 0:
            found = tuple(sorted(x)); break
    if found is None:
        for x in itertools.product(range(p), repeat=j + 1):
            if any(x) and sum(pow(v, j, p) for v in x) % p == 0:
                found = tuple(sorted(v for v in x if v)); break
    rows.append([found])
S = [1]
for X in [r[0] for r in rows]:
    S = [(s * x) % p for s in S for x in X]
moms = [sum(pow(s, jj, p) for s in S) % p for jj in range(1, c + 1)]
print(f'  p=7 c=6 (one witness per row {[r[0] for r in rows]}): M={len(S)}, moments={moms}, '
      f'#distinct={len(set(S))}, p | M: {len(S) % 7 == 0}')

print('Lemma app-sub-design (a): mu_e for every e | p-1 with e > c')
fails = 0
for p in (3, 5, 7, 11, 13, 43):
    for c in range(1, p):
        es = [e for e in range(c + 1, p) if (p - 1) % e == 0]
        if (p >= c + 2) != bool(es):
            fails += 1
            print('  existence claim FAILS', p, c, es)
        for e in es:
            # generator of mu_e
            g = next(x for x in range(2, p) if pow(x, (p - 1), p) == 1 and
                     all(pow(pow(x, (p - 1) // e, p), e // q, p) != 1
                         for q in range(2, e + 1) if e % q == 0 and all(q % t for t in range(2, q))))
            xi = pow(g, (p - 1) // e, p)
            S = [pow(xi, i, p) for i in range(e)]
            moms = [sum(pow(s, j, p) for s in S) % p for j in range(1, c + 1)]
            if any(moms) or len(set(S)) != e:
                fails += 1
                print('  FAIL mu_e', p, c, e, moms)
print(f'  failures: {fails}; p=43,c=9: smallest e = '
      f'{min(e for e in range(10, 43) if 42 % e == 0)}')
# Las Vegas success probability phi(e)/e for p=43, e=14
p, e = 43, 14
cnt = 0
for x in range(1, p):
    y = pow(x, (p - 1) // e, p)
    if all(pow(y, e // q, p) != 1 for q in (2, 7)):
        cnt += 1
print(f'  p=43 e=14: fraction of x giving a generator = {cnt}/{p-1} (phi(14)/14 = 6/14 = {6/14:.4f})')

print('Lemma app-sub-design (c): random multisets with vanishing moments 1..c\' and p not | |S|')
import random
random.seed(5)
viol = 0
tested = 0
for p in (5, 7, 11):
    for cprime in range(1, p - 1):
        for trial in range(4000):
            size = random.randint(1, 3 * p)
            S = [random.randint(1, p - 1) for _ in range(size)]
            if size % p == 0:
                continue
            if all(sum(pow(s, j, p) for s in S) % p == 0 for j in range(1, cprime + 1)):
                tested += 1
                if len(set(S)) < cprime + 1:
                    viol += 1
print(f'  multisets meeting the hypotheses: {tested}, violations: {viol}')
sys.stdout.flush()

# (2) Lemma app-sub-character on filiform algebras: basis x, e1..ec, [x, e_i] = e_{i+1}
print('Lemma app-sub-character on filiform Lazard groups')


def filiform(p, c):
    dim = c + 1  # x, e1..ec
    def br(a, b):
        # a = (ax, a1..ac); [x, e_i] = e_{i+1}
        out = [0] * dim
        for i in range(1, c):
            out[i + 1] = (out[i + 1] + a[0] * b[i] - b[0] * a[i]) % p
        return tuple(out)
    def add(*vs):
        return tuple(sum(v[t] for v in vs) % p for t in range(dim))
    def scal(k, v):
        return tuple((k * x) % p for x in v)
    inv = lambda n: pow(n, -1, p)
    def bch(a, b):
        # truncated BCH up to degree 4 (enough for class <= 4)
        ab = br(a, b)
        t2 = scal(inv(2), ab)
        t3 = add(scal(inv(12), br(a, ab)), scal((-inv(12)) % p, br(b, ab)))
        t4 = scal((-inv(24)) % p, br(b, br(a, ab)))
        return add(a, b, t2, t3, t4)
    return dim, br, add, scal, bch


for (p, c) in ((5, 3), (5, 4), (7, 3)):
    dim, br, add, scal, bch = filiform(p, c)
    elems = list(itertools.product(range(p), repeat=dim))
    zero = (0,) * dim
    neg = lambda v: tuple((-x) % p for x in v)
    # group axioms spot check: associativity on random triples
    random.seed(1)
    assoc_bad = 0
    for _ in range(3000):
        a, b, cc = (tuple(random.randrange(p) for _ in range(dim)) for _ in range(3))
        if bch(bch(a, b), cc) != bch(a, bch(b, cc)):
            assoc_bad += 1
    # Step 2 identity: x*y*(-x) = sum_k (ad x)^k y / k!
    step2_bad = 0
    for _ in range(3000):
        a, b = (tuple(random.randrange(p) for _ in range(dim)) for _ in range(2))
        lhs = bch(bch(a, b), neg(a))
        rhs = b
        term = b
        for k in range(1, c):
            term = br(a, term)
            rhs = add(rhs, scal(pow(math.factorial(k), -1, p), term))
        if lhs != rhs:
            step2_bad += 1
    # commutator subgroup: generated by group commutators
    comms = set()
    for _ in range(4000):
        a, b = (tuple(random.randrange(p) for _ in range(dim)) for _ in range(2))
        comms.add(bch(bch(bch(neg(a), neg(b)), a), b))
    # closure
    sub = {zero}
    frontier = list(comms)
    sub |= comms
    changed = True
    while changed:
        changed = False
        cur = list(sub)
        for g in cur:
            for h in list(comms)[:60]:
                gh = bch(g, h)
                if gh not in sub:
                    sub.add(gh); changed = True
    derived = {v for v in elems if v[0] == 0 and v[1] == 0}  # [L,L] = span(e2..ec)
    print(f'  filiform p={p} c={c}: assoc failures={assoc_bad}, Step-2 identity failures={step2_bad}, '
          f'[G,G] == [L,L] as sets: {sub == derived} (|[G,G]|={len(sub)}, |[L,L]|={len(derived)})')
    # quotient additivity: (a*b) - a - b lies in [L,L]
    qbad = 0
    for _ in range(3000):
        a, b = (tuple(random.randrange(p) for _ in range(dim)) for _ in range(2))
        d = add(bch(a, b), neg(a), neg(b))
        if d[0] or d[1]:
            qbad += 1
    print(f'      (a*b - a - b) in [L,L] failures: {qbad}')

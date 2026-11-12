#!/opt/anaconda3/bin/python
"""Path statistics of HCD (collision_descent.py) on uniform and repeated-column banks; every output verified."""
import random, collections, collision_descent as cd
rng = random.Random(7)
for a, trials in ((1, 300), (2, 150), (3, 40)):
    A4 = (a + 1) * (3 * a + 1); n = A4 * A4 * (a + 1)
    for kind in ('uniform', 'all-e1', 'two-values'):
        cnt = collections.Counter(); bad = 0
        for _ in range(trials):
            if kind == 'uniform':
                L = [[rng.randrange(41) for _ in range(a)] for _ in range(n)]
            elif kind == 'all-e1':
                L = [[1] + [0] * (a - 1) for _ in range(n)]
            else:
                S = [[rng.randrange(41) for _ in range(a)] for _ in range(2)]
                L = [rng.choice(S) for _ in range(n)]
            cd.PATH.clear(); x = cd.hcd(L, a)
            bad += not cd.verify(x, L, a); cnt[cd.PATH[-1]] += 1
        print(f'a={a} M={n} {kind:10s} trials={trials} failures={bad} paths={dict(cnt)}')

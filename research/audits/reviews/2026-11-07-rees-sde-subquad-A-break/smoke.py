import random, sys
from harness import Tally, run_bank
from algt import Par
p, k, J, a = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
rng = random.Random(1)
par = Par(J, k)
T = Tally()
for it in range(int(sys.argv[5])):
    M = par.F(a)
    # mildly structured: columns from few-dim flats
    bank = []
    for i in range(M):
        d = rng.choice([1, 2, 3, a])
        v = [0]*a
        for t in range(d):
            j = rng.randrange(a); v[j] = rng.randrange(p)
        if not any(v): v[0] = 1
        bank.append(v)
    rng.shuffle(bank)
    out, rec, ex = run_bank(bank, p, k, J, T, passes=5, tag="smoke")
print(T.summary())
print(T.fail[:5])

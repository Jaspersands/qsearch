"""rem:sde-subquadratic(a) examples and a brute-force recheck of a nbank.py witness."""
import itertools, random
import numpy as np
import sympy

def squares0(p):
    return sorted({x * x % p for x in range(p)})  # includes 0

# (1) kappa = 2, columns e1, e2, -e1-e2: R_0(S) = {(x1-x3, x2-x3)}
full = []
for p in sympy.primerange(3, 400):
    Po = squares0(p)
    R = {((x1 - x3) % p, (x2 - x3) % p) for x1 in Po for x2 in Po for x3 in Po}
    if len(R) == p * p:
        full.append(p)
print("kappa=2: primes p<400 with R_0({e1,e2,-e1-e2}) = F_p^2:", full)
print("  29,53,101 included:", all(q in full for q in (29, 53, 101)))
print("  p=1 mod 4 primes < 400 NOT full:", [p for p in sympy.primerange(3, 400) if p % 4 == 1 and p not in full])
print("  p=3 mod 4 primes < 400 full:", [p for p in full if p % 4 == 3])

# (2) random sets of 5 columns in F_p^3 (2-dim relation space), kappa = 2
random.seed(1)
for p in (13, 29):
    Po = np.array(squares0(p))
    cnt_full, trials = 0, 30
    for _ in range(trials):
        while True:
            L = np.array([[random.randrange(p) for _ in range(3)] for _ in range(5)])
            if np.linalg.matrix_rank(L.astype(float)) == 3:
                break
        X = np.array(list(itertools.product(Po, repeat=5)))  # all weight vectors
        V = (X @ L) % p
        keys = V[:, 0] * p * p + V[:, 1] * p + V[:, 2]
        if len(np.unique(keys)) == p ** 3:
            cnt_full += 1
    print(f"kappa=2 p={p}: random 5-column sets in F_p^3 with R_0(S)=F_p^3: {cnt_full}/{trials}")

# (3) brute force: bank [(1,0),(0,1),(1,2),(1,4),(3,1)] in F_7^2, kappa=3, P u {0} = {0,1,6}
p = 7
Po = [0, 1, 6]
bank = [(1, 0), (0, 1), (1, 2), (1, 4), (3, 1)]
sols = [x for x in itertools.product(Po, repeat=5) if any(x) and
        sum(xi * b[0] for xi, b in zip(x, bank)) % p == 0 and sum(xi * b[1] for xi, b in zip(x, bank)) % p == 0]
print("kappa=3 p=7 witness bank nonzero solutions:", len(sols))
bank = [(1, 0), (0, 1), (1, 2), (1, 5), (2, 12)]
P17 = sorted({pow(x, 4, 17) for x in range(1, 17)})
sols = [x for x in itertools.product([0] + P17, repeat=5) if any(x) and
        sum(xi * b[0] for xi, b in zip(x, bank)) % 17 == 0 and sum(xi * b[1] for xi, b in zip(x, bank)) % 17 == 0]
print("kappa=4 p=17 witness bank nonzero solutions:", len(sols))

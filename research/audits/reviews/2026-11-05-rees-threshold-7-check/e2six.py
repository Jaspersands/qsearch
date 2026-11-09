import json
from rc import feasible, is_prime
bad = []
for p in range(7, 3000, 6):
    if is_prime(p):
        st, a, b, n = feasible(p, 6, list(range(6)), [0]); assert st in (0, 1)
        if st == 0: bad.append(p)
print("E_2(6) below 3000: %d primes, max %d" % (len(bad), max(bad))); print(bad)
json.dump(bad, open('e2six.json', 'w'))

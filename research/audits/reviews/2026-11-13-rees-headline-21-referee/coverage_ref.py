import json, os
import rule_ref as R
C = json.load(open(os.path.join(R.SRC, 'certs_stage1.json')))
pr = R.sieve(2 * 10 ** 6)
for nm, (tag, D, Rr) in R.NAME.items():
    T = R.TEX[tag]; need = [p for p in pr if p % D == 1 and p < T]
    found = set(int(x) for x in C[nm]['found']); miss = [p for p in need if p not in found]
    extra = [p for p in found if p >= T or p % D != 1]
    print(f'{tag}: primes = 1 mod {D} below {T}: {len(need)}; certified {len(found)}; uncovered {miss}; extra {extra[:5]}')
print('Tier B primes', len(R.TB_PRIMES), R.TB_PRIMES)
print('primes = 1 mod 2520 below 2e6:', sum(1 for p in pr if p % 2520 == 1))

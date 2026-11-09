"""Internal-consistency checks of the numbers in prov:s2-exceptional (E2-UPDATE region).
Read-only; pure arithmetic with sympy. Usage: /opt/anaconda3/bin/python -I e2_consistency.py"""
from sympy import isprime, primerange
def nxt(p, k):
    q = p + 1
    while not (isprime(q) and q % k == 1): q += 1
    return q
print("16993 prime, =1 mod 8:", isprime(16993), 16993 % 8, "next:", nxt(16993, 8))
print("16633 prime, =1 mod 9:", isprime(16633), 16633 % 9, "next:", nxt(16633, 9))
print("13873:", isprime(13873), 13873 % 8, " 16363:", isprime(16363), 16363 % 9)
print("14281 in E2(8)? prime, mod 8:", isprime(14281), 14281 % 8, " 18199:", isprime(18199), 18199 % 9)
print("6073:", isprime(6073), 6073 % 8, " 6067:", isprime(6067), 6067 % 9)
L = [17551, 17623, 17659, 17713, 17749, 17839, 17911, 17929, 18127, 18181, 18199, 18217, 18307, 20071, 20089, 20107]
print("k9 list all prime and =1 mod 9:", all(isprime(x) and x % 9 == 1 for x in L), [x for x in L if not (isprime(x) and x % 9 == 1)])
print("k9 list sorted, all > 16633:", L == sorted(L), all(x > 16633 for x in L))
c8 = [p for p in primerange(2, 2442) if p % 8 == 1]; c9 = [p for p in primerange(2, 3584) if p % 9 == 1]
print("#primes =1 mod 8 below 2442:", len(c8), " #primes =1 mod 9 below 3584:", len(c9))
print("8^8/2 =", 8**8 // 2, " 9^9/2 =", 9**9 / 2)
g = [p for p in primerange(20001, 49418) if p % 16 == 9]
print("#primes =9 mod 16 in (20000,49417]:", len(g))
print("primes =1 mod 8 in (9769,20000]:", len([p for p in primerange(9770, 20001) if p % 8 == 1]))
print("9473, 9769 prime and mod 8:", isprime(9473), 9473 % 8, isprime(9769), 9769 % 8, " 17623 mod 9:", 17623 % 9)
print("20071, 20089, 20107 prime =1 mod 9:", [(x, isprime(x), x % 9) for x in (20071, 20089, 20107)])
print("424549 prime, mod 9:", isprime(424549), 424549 % 9)

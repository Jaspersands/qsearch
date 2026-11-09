import sys
sys.path.insert(0, '/private/tmp/claude-501/-Users-jaspersands-Developer-qsearch/6a6cfdd7-c9d4-4169-9805-7e18625bbdd7/scratchpad')
from regimes_check import mixed, B_IS
from fractions import Fraction as Fr
from math import gcd
prof=[19,17,16,14,12,9,6,3,1]; gs={i+1:g for i,g in enumerate(prof)}
for p in [11,1031,5281,2**31-1,2**61-1,2**127-1]:
    comb={}
    for d in range(2,10):
        k=gcd(d,p-1)
        comb[d]='lin' if k==1 else ('S2' if p>=16*k**(2*k+2) else 'S1@%d'%k)
    mx=mixed(p,gs,Fr(1,3))
    print(p.bit_length(), 'combined', comb, 'mixed', mx and mx['typ'])

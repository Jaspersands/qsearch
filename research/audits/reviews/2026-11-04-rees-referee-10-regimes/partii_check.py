import sys
sys.path.insert(0, '/private/tmp/claude-501/-Users-jaspersands-Developer-qsearch/6a6cfdd7-c9d4-4169-9805-7e18625bbdd7/scratchpad')
from regimes_check import beta, lg
from fractions import Fraction as Fr
from math import gcd, log, log2, ceil
prof=[19,17,16,14,12,9,6,3,1]; gs={i+1:g for i,g in enumerate(prof)}
u=18; M=72; n0=37; B=56
for p in [5281,105019,2**31-1,2**61-1,194522647344910884721,2**127-1]:
    bank=Fr(0); cap=0
    for d in range(2,10):
        k=gcd(d,p-1); h=(p-1)//k; q=Fr(h+1,p); g=gs[d]
        bank += Fr(M)**(d-2)*beta(p,k,M,n0,g)
        c_=2*B*log(2)*2**lg(1/q**g); cap=max(cap,c_)
    print(p.bit_length(), 'bank sum log2=%.1f'%lg(bank), 'cap log2=%.2f'%log2(ceil(cap)))

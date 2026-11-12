"""Explicit C4 parameters and error budget (report Sec. 5).  Exact integers from common.params.
Usage: nice -n 19 /opt/anaconda3/envs/qsearch-cas/bin/python params_table.py"""
import math, sys
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from common import params

def lg(x): return math.log2(x)

print('| b | log2 Mb | K | log2 Q | log2 mu_max | log2 P | log2 N (window) | log2 R | log2 N0 | log2 F_A | B (box exponent) |')
print('|---|---|---|---|---|---|---|---|---|---|---|')
for b in [1, 2, 4, 6, 8, 10, 20, 50]:
    p = params(b)
    print(f"| {b} | {p['logMb']} | {p['K']} | {lg(p['Q']):.1f} | {lg(p['mu_max']):.1f} | {lg(p['P']):.1f} | {lg(p['N']):.1f} | "
          f"{lg(p['R']):.1f} | {p['n0']} | {p['logFA']} | {p['B']} |")
print()
print('Error budget per stage-1 sample (eta_s = 2^-10), b = 10:')
p = params(10); Mb = p['Mb']; mu = p['mu_max']
phase = 4 * math.pi ** 2 * (2.0 ** -p['K'] * 2.5 * Mb * Mb) ** 2
trunc = 2 * 2 * (1.2 * mu * Mb / p['P'] + p['D'] / p['N'])
print(f"  phase term 4 pi^2 (2^-K 2.5 Mb^2)^2 = {phase:.3e}  (<= eta_s^2/2 = {p['eta_s']**2/2:.3e})")
print(f"  truncation term 2 sum_i (1.2|mu_i| Mb/P + D_i/N) <= {trunc:.3e}  (<= eta_s^2/2)")
print(f"  bad-coset probability 2V/R = {2*p['V']/p['R']:.3e}  (<= eta_s)")
print(f"  => TV(actual sample law, P*_alpha) <= sqrt(E||Phi-Phi*||^2) + 2V/R <= {math.sqrt(phase+trunc) + 2*p['V']/p['R']:.3e} (<= 2 eta_s = {2*p['eta_s']:.3e})")
for b in [1, 6, 10, 50]:
    p = params(b); N0 = p['N0']; Q = p['Q']; eps = 2.0 ** p['logeps']
    print(f"  b={b}: N0 >= 2R: {N0 >= 2*p['R']}; N0 >= 600 Q/eps^2: {N0 >= 600*Q*2**(2*(p['K']+1))}; Q/(eps N0) = 2^{lg(Q)-p['logeps']-p['n0']:.1f}")

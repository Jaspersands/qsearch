"""Slack probe for Lemma D (stage 1): shrink the Fourier box Mb below the proved choice 2^{3b+26}
(strip width gamma = 2^{b+7}/Mb, other parameters unchanged) and record direction / h recovery.
Shows where the decoder starts to fail; the proof's conditions are violated below 3b+26.
Usage: nice -n 19 /opt/anaconda3/envs/qsearch-cas/bin/python margins.py [trials] [seed] [b]"""
import random, sys
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from common import params
from decode_sim import trial

trials = int(sys.argv[1]) if len(sys.argv) > 1 else 100
rng = random.Random(int(sys.argv[2]) if len(sys.argv) > 2 else 7)
b = int(sys.argv[3]) if len(sys.argv) > 3 else 10
print(f'| b | log2 Mb | log2 gamma | trials | direction ok, 1st batch | h recovered, 1st batch |')
print('|---|---|---|---|---|---|')
for logMb in [b + 8, b + 10, 2 * b + 6, 2 * b + 12, 3 * b + 26]:
    p = params(b); p['logMb'] = logMb; p['Mb'] = 1 << logMb; p['log_gamma1'] = b + 7 - logMb
    st = []
    for _ in range(trials): trial(rng, b, p, st)
    print(f"| {b} | {logMb} | {b + 7 - logMb} | {trials} | {sum(s['dir_first'] for s in st)}/{trials} | {sum(s['first'] for s in st)}/{trials} |", flush=True)

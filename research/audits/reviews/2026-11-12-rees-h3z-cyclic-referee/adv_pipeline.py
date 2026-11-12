"""Adversarial full-pipeline run: the proof folder's decode_sim.trial (stage 1 + stage 2 + period
finding + prime-by-prime certification) on PRESCRIBED worst-case h instead of random h.
A rigged RNG feeds the three randrange draws trial() uses to pick h (a, b, c; the random()
draw for the c bit-size is then irrelevant); everything after that is the trial's own randomness.
Success = h_out in {h, h^-1} within 3 batches.  Finite check only falsifies.
Usage: nice -n 19 /opt/anaconda3/envs/qsearch-cas/bin/python adv_pipeline.py [trials] [seed] [b]"""
import random, sys
sys.path.insert(0, __file__.rsplit('/', 2)[0] + '/2026-11-12-rees-h3z-cyclic-proof')
from common import params, C2
import decode_sim

class Rig(random.Random):
    def __init__(self, seed):
        super().__init__(seed); self.qr = []; self.qf = []
    def randrange(self, *a, **k):
        if self.qr: return self.qr.pop(0)
        return super().randrange(*a, **k)

def main():
    trials = int(sys.argv[1]) if len(sys.argv) > 1 else 10
    seed = int(sys.argv[2]) if len(sys.argv) > 2 else 5
    b = int(sys.argv[3]) if len(sys.argv) > 3 else 10
    B = 1 << b; p = params(b); rng = Rig(seed)
    hs = [
        ('g = 512 (l = 512 l^), w = 512(1,1)', (B // 2, B // 2, B // 4)),
        ('w = (0, 2^(b-1)), g = gcd(2^(b-1), c)', (0, B // 2, B // 2)),
        ('h^-1 small: h = (a,b,ab+B-1), |c| ~ 2^(2b)', (B - 1, B - 1, (B - 1) ** 2 + (B - 1))),
        ('v huge primitive, c = 0', (B - 1, -(B - 2), 0)),
        ('X3 = 0, large c', (B - 2, B - 1, (B - 2) * (B - 1) // 2)),
        ('(1,0,0)', (1, 0, 0)),
        ('(0,1,0)', (0, 1, 0)),
        ('(1,1,0)', (1, 1, 0)),
        ('a = -(2^b-1), b = 2^b-1, c = -(2^b-1)', (-(B - 1), B - 1, -(B - 1))),
        ('w = (3,1)2^(b-2), c = -1', (3 * (B // 4), B // 4, -1)),
    ]
    print(f'b={b}, {trials} trials per h, decode_sim.trial with prescribed h (seed {seed})')
    print('| case | h | g = gcd(l) | h recovered, 1st batch | h recovered, <= 3 batches | direction ok / batches |')
    print('|---|---|---|---|---|---|')
    for name, h in hs:
        a, bb, c = h
        import math
        d = math.gcd(a, bb); v = (a // d, bb // d); s0 = c - C2(d) * v[0] * v[1]; g = math.gcd(d, s0)
        st = []
        for _ in range(trials):
            # trial(): a_, b_ = randrange, randrange; cbits = b if random() < .5 else 2b; c_ = randrange
            rng.qr = [a, bb, c]   # the random() draw for the c bit-size is irrelevant: c comes from the queue
            decode_sim.trial(rng, b, p, st)
        nb = sum(s['batches'] for s in st)
        print(f"| {name} | {h} | {g} | {sum(s['first'] for s in st)}/{trials} | {sum(s['any'] for s in st)}/{trials} | "
              f"{sum(s['dir_ok'] for s in st)}/{nb} |", flush=True)

if __name__ == '__main__':
    main()

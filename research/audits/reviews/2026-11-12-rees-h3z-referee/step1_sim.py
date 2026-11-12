"""Referee check of Theorem A, Step 1 (detection of e by period finding on t -> f(z^t)).
Exact output distribution of one run of standard period finding (uniform superposition over
[0,Q), label register measured, QFT_Q, measure k), followed by continued fractions of k/Q.
Q = 2^(6b+3), acceptance bound R = 2^(3b+1), acceptance test f(z^r) = f(1) <=> e | r.
Reports, per e, the probability that a run produces an ACCEPTED candidate r != e
(necessarily a proper multiple of e). Floating point; it can only falsify, not prove.
Usage: nice -n 19 /opt/anaconda3/bin/python step1_sim.py [b]
"""
import sys
from fractions import Fraction
import numpy as np

def convergent_denoms(k, Q):
    """Denominators of all convergents of k/Q."""
    a, b = k, Q
    h0, h1 = 1, 0      # denominators q_{-2} = 1, q_{-1} = 0
    out = []
    while b:
        q = a // b
        a, b = b, a - q * b
        h0, h1 = h1, q * h1 + h0
        out.append(h1)
    return out

def dist(e, Q):
    k = np.arange(Q)
    P = np.zeros(Q)
    for l in range(e):
        m = (Q - 1 - l) // e + 1          # number of t in [0,Q) with t = l mod e
        th = 2 * np.pi * k * e / Q
        num = np.sin(m * th / 2) ** 2
        den = np.sin(th / 2) ** 2
        exact = (k * e) % Q == 0
        with np.errstate(divide='ignore', invalid='ignore'):
            g = np.where(exact, float(m * m), num / np.where(exact, 1.0, den))
        P += g
    return P / Q ** 2

def main():
    b = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    Q, R = 2 ** (6 * b + 3), 2 ** (3 * b + 1)
    print(f'b={b} Q=2^{6*b+3} R=2^{3*b+1}')
    worst = (0, None, None)
    for e in range(1, R + 1):
        P = dist(e, Q)
        assert abs(P.sum() - 1) < 1e-9
        p_last_bad = p_any_bad = p_last_good = 0.0
        example = None
        for k in range(Q):
            if P[k] < 1e-15: continue
            ds = [d for d in convergent_denoms(k, Q) if 1 <= d <= R]
            if not ds: continue
            last = ds[-1]                  # usual rule: last convergent with q <= R
            if last % e == 0 and last != e:
                p_last_bad += P[k]
                if example is None: example = (k, last)
            if last == e: p_last_good += P[k]
            if any(d % e == 0 and d != e for d in ds):
                p_any_bad += P[k]
        if p_last_bad > worst[0]: worst = (p_last_bad, e, example)
        if e <= 12 or p_last_bad > 0.01:
            print(f'  e={e:4d}  P[accepted r=e]={p_last_good:.4f}  '
                  f'P[accepted r=multiple!=e] last-rule={p_last_bad:.4f} any-convergent={p_any_bad:.4f}'
                  + (f'  e.g. k={example[0]} -> r={example[1]}' if example else ''))
    print('worst P[accepted proper multiple] (last-convergent rule):', round(worst[0], 4),
          'at e =', worst[1], 'example (k, r) =', worst[2])

if __name__ == '__main__':
    main()

#!/opt/anaconda3/bin/python
"""Build and verify the 4-level {0}-contractions at kappa = 9 from (kappa=3 two-level step) x (RC3 step).

For each p given: reads rc3_<p>_9_036_0.json (decoded SAT model of RC3(9; {0,3,6} -> {0})), composes it with the
two-level RC(3; Z_3 -> {0}) witness, writes the full table B4_<p>.json (6561 entries, key = digits x1x2x3x4) and
verifies it with ell_common.verify (exact mixed difference on all cells, exact classes, B(0) != 0, plus a
sample of product tensors of W^{(x)4}).  usage: build_nodes.py p [p ...]
"""
import sys, os, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import ell_common as E
import compose as C

KAPPA3 = {37: ([1, 0, 12], {0: 0, 1: 2, 2: 1}),
          19: ([1, 0, 5], {0: 0, 1: 3, 2: 1}),
          73: ([1, 14, 26], {0: 0, 1: 1, 2: 3})}

for p in map(int, sys.argv[1:]):
    d = json.load(open(os.path.join(HERE, f'rc3_{p}_9_036_0.json')))
    assert d['bad'] == [] and d['p'] == p and d['D'] == 9 and d['R'] == [0, 3, 6] and d['K'] == [0]
    F = {(i, j): d['F'][i][j] for i in range(9) for j in range(9)}
    G = {(int(s), j): v[j] for s, v in d['G'].items() for j in range(9)}
    H = {(int(s), i): v[i] for s, v in d['H'].items() for i in range(9)}
    a3, b3 = KAPPA3[p]
    steps = [C.two_level(3, (0, 1, 2), (0,), a3, b3), C.three_level(9, (0, 3, 6), (0,), F, G, H)]
    B, l = C.compose(p, 9, steps)
    ok, info = E.verify(B, p, 9, (0,), l, sample=40)
    json.dump({''.join(map(str, x)): v for x, v in B.items()}, open(os.path.join(HERE, f'B4_{p}.json'), 'w'))
    # negative control: same table against K = {1}; and against the gauge-broken table (one G entry changed)
    ok_neg, info_neg = E.verify(B, p, 9, (1,), l, sample=0)
    G2 = dict(G); G2[(3, 4)] = (G2[(3, 4)] + 1) % p
    try:
        B2, _ = C.compose(p, 9, [steps[0], C.three_level(9, (0, 3, 6), (0,), F, G2, H)])
        neg2 = 'composed (unexpected)'
        ok2, info2 = E.verify(B2, p, 9, (0,), l, sample=0)
        neg2 = f'verify={ok2} class_violations={info2["class_violations"]}'
    except AssertionError as e:
        neg2 = 'step cell condition rejected: ' + str(e.args[0][0])
    print(f'p={p}: 4-level {{0}}-contraction {"VERIFIED" if ok else "FAILED"} {info}')
    print(f'   neg control K={{1}}: verify={ok_neg} class_violations={info_neg["class_violations"]};  perturbed G(3,4): {neg2}')

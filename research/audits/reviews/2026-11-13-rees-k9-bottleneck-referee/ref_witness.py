#!/opt/anaconda3/bin/python
"""Referee checks of the report's kappa = 9 witnesses and non-existence claims (finite exact; can only falsify).
1. Report witnesses (typed in from witness_dump.out / report sec. 3) re-checked cell by cell (own dlog table).
2. Own complete searches: two-level union steps RC(9; Z_9 -> {0,m}) at 19, 37, 73; tower step RC(9;{0,3,6}->{0});
   stage steps RC(9;{0,3,6}->{0,m}); RC(4;Z4->{0}), RC(6;Z6->{0}) at 37 (E_2 membership).
3. Complete chain reachability (fixpoint) at (9,19), (9,37), (9,73): is (9,{0}) reachable? shortest {0,m}.
4. Tn after one {0,m} stage at 19, 37, 73: size and classes.
"""
import time, itertools
from ref_common import *

t0 = time.time()
W = [  # (p, D, R, K, alpha, beta)
    (37, 3, (0, 1, 2), (0,), [1, 0, 12], {0: 0, 1: 2, 2: 1}),
    (37, 9, (0, 3, 6), (0, 4), [1, 0, 17, 10, 36, 34, 0, 10, 32], {0: 0, 3: 1, 6: 27}),
    (37, 9, tuple(range(9)), (0, 2, 5), [1, 35, 8, 24, 20, 21, 30, 0, 26],
     dict(zip(range(9), [0, 11, 36, 2, 29, 13, 17, 16, 7]))),
    (73, 3, (0, 1, 2), (0,), [1, 14, 26], {0: 0, 1: 1, 2: 3}),
    (73, 9, (0, 3, 6), (0, 1), [1, 0, 0, 43, 67, 28, 45, 48, 34], {0: 0, 3: 6, 6: 25}),
    (19, 3, (0, 1, 2), (0,), [1, 0, 5], {0: 0, 1: 3, 2: 1}),
    (19, 9, (0, 3, 6), (0, 1), [1, 9, 9, 7, 0, 0, 16, 15, 15], {0: 0, 3: 4, 6: 10}),
    (19, 9, tuple(range(9)), (0, 1, 4, 7), [1, 0, 9, 16, 0, 9, 16, 0, 9],
     dict(zip(range(9), [0, 10, 3, 1, 10, 3, 1, 10, 3]))),
    (19, 9, (0, 1, 4, 7), (0, 3, 8), [1, 4, 5, 1, 0, 11, 11, 13, 1], {0: 0, 1: 8, 4: 18, 7: 14}),
    (127, 3, (0, 1, 2), (0,), [1, 18, 56], {0: 0, 1: 8, 2: 2}),
    (127, 9, (0, 3, 6), (0, 3), [1, 45, 71, 0, 39, 26, 0, 17, 3], {0: 0, 3: 0, 6: 4}),
    (127, 9, (0, 3), (0,), [1, 45, 71, 47, 105, 75, 0, 17, 3], {0: 0, 3: 4}),
    (181, 3, (0, 1, 2), (0,), [1, 0, 17], {0: 0, 1: 2, 2: 1}),
    (181, 9, (0, 3, 6), (0, 1), [1, 1, 72, 80, 7, 87, 129, 152, 138], {0: 0, 3: 6, 6: 4}),
    (181, 9, (0, 1), (0,), [1, 75, 54, 68, 0, 16, 95, 138, 97], {0: 0, 1: 10}),
    (433, 3, (0, 1, 2), (0,), [1, 0, 26], {0: 0, 1: 6, 2: 2}),
    (433, 9, (0, 3, 6), (0, 1), [1, 143, 12, 103, 131, 242, 0, 0, 22], {0: 0, 3: 1, 6: 2}),
    (433, 9, (0, 1), (0,), [1, 9, 81, 302, 55, 19, 84, 14, 0], {0: 0, 1: 8}),
]
print('== 1. report witnesses, own cell check (g = least primitive root)')
allok = True
for (p, D, R, K, al, be) in W:
    ok = rc_check(p, D, R, K, al, be)
    allok &= ok
    print(f'  p={p} g={prim_root(p)} RC({D}; {R} -> {K}): {ok}')
# chain condition of each listed path
print('  all witnesses pass:', allok)
print('  chain conditions: 37/73/19 stage: R_2 = {0,3,6} = lift(K_1={0}) -> OK by construction;',
      '19 finish: R_2 = {0,1,4,7} = K_1 -> OK; 127: R_3 = {0,3} = K_2; 181/433: R_3 = {0,1} = K_2')

print('== 2. own complete searches')
for p in (19, 37, 73):
    res = {}
    for m in range(1, 9):
        st, a, b = rc_search(p, 9, tuple(range(9)), (0, m))
        res[m] = st
    print(f'  p={p}: two-level union step RC(9;Z9->{{0,m}}) status by m=1..8:', [res[m] for m in range(1, 9)])
    st, a, b = rc_search(p, 9, (0, 3, 6), (0,))
    print(f'  p={p}: tower step RC(9;{{0,3,6}}->{{0}}):', st)
    st3, a3, b3 = rc_search(p, 3, (0, 1, 2), (0,))
    print(f'  p={p}: RC(3;Z3->{{0}}):', st3, a3, b3)
    print(f'  p={p}: stage steps RC(9;{{0,3,6}}->{{0,m}}) m=1..8:',
          [rc_search(p, 9, (0, 3, 6), (0, m))[0] for m in range(1, 9)])
for kap in (2, 3, 4, 6, 9):
    st, a, b = rc_search(37, kap, tuple(range(kap)), (0,))
    print(f'  p=37: two-level contraction RC({kap};Z{kap}->{{0}}) (p notin E_2({kap}) iff 1):', st)
for kap in (2, 3, 4, 6, 8, 9):
    st, a, b = rc_search(73, kap, tuple(range(kap)), (0,))
    print(f'  p=73: two-level contraction RC({kap};Z{kap}->{{0}}):', st)
for kap in (2, 3, 6, 9):
    st, a, b = rc_search(19, kap, tuple(range(kap)), (0,))
    print(f'  p=19: two-level contraction RC({kap};Z{kap}->{{0}}):', st)
print('  time %.1fs' % (time.time() - t0), flush=True)

print('== 3. complete chain reachability (fixpoint, no length limit)')
for p in (19, 37, 73):
    level, parent, tests, und = chain_bfs(9, p)
    deg = chain_degrees(9, level)
    maxL = max(level.values())
    print(f'  p={p}: tests={len(tests)} undecided={len(und)} nodes={len(level)} max level={maxL};',
          '(9,{0}) reachable:', (9, (0,)) in level or any(D == 9 and K == (0,) for (D, K) in level),
          '; deg[{0}] =', deg[(0,)])
    print('     deg[{0,m}] m=1..8:', [deg[(0, m)] for m in range(1, 9)])
    for m in range(1, 9):
        c = [(l, n) for n, l in level.items() if n[0] > 1 and set(lift(n[0], n[1], 9)) <= {0, m}]
        if c:
            l, n = min(c)
            print(f'     {{0,{m}}} via', ' -> '.join(f'({d},{set(k)})' for d, k in path(parent, n)))
    print('  time %.1fs' % (time.time() - t0), flush=True)

print('== 4. Tn after one {0,m} stage, eps = -g^{-m}')
for p in (19, 37, 73):
    g, L = dlog(p)
    P = {x for x in range(1, p) if L[x] % 9 == 0}
    P0 = P | {0}
    for m in range(1, 9):
        eps = (-pow(pow(g, m, p), p - 2, p)) % p
        Tn = {(y1 + eps * y2) % p for y1 in P0 for y2 in P0 if (y1, y2) != (0, 0)}
        C = sorted({L[x] % 9 for x in Tn if x})
        print(f'  p={p} m={m}: |Tn\\0|={len(Tn - {0})} 0 in Tn: {0 in Tn} classes={C}')
print('done %.1fs' % (time.time() - t0))

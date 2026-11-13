import rule_ref as R
from rule_ref import lift
def chains_paths(p, kap, e, LMAX=3):
    E = R.EDGES.get(p, set())
    best = {(1, frozenset([0])): (1, None)}
    for D in range(2, kap):
        if kap % D == 0: best[(D, frozenset([0]))] = (e[D], ('solver', D))
    front = {k: v[0] for k, v in best.items()}
    for _ in range(LMAX):
        new = {}
        for (D, K), dg in front.items():
            for (D2, Rr, K2) in E:
                if kap % D2 or D2 % D or D2 < 2: continue
                if Rr != lift(K, D, D2) or len(Rr) < 2: continue
                if dg + 1 < min(best.get((D2, K2), (99,))[0], new.get((D2, K2), (99,))[0]):
                    new[(D2, K2)] = (dg + 1, ((D, K), (D2, Rr, K2)))
        front = {k: v[0] for k, v in new.items()}; best.update(new)
        if not new: break
    return best
def path(best, node):
    out = []
    while True:
        dg, par = best[node]
        if par is None: out.append(('GE',)); break
        if par[0] == 'solver': out.append(('solver', par[1], dg)); break
        out.append(par[1]); node = par[0]
    return out[::-1]
if __name__ == '__main__':
    for p, kap in [(13, 4), (13, 6), (19, 6), (19, 9), (37, 4), (37, 6), (37, 9), (73, 6), (73, 8), (73, 9), (43, 7), (5, 4)]:
        e, pl = R.degrees(p)
        b = chains_paths(p, kap, e)
        print(p, kap, 'e=', e[kap], pl[kap])
        for node in b:
            if node[0] == kap: print('    ', sorted(node[1]), b[node][0], path(b, node))

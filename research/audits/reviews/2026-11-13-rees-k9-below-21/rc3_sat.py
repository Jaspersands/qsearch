#!/opt/anaconda3/bin/python
"""CNF for a three-level chain step RC3(D; R -> K) and its decoder.  /opt/anaconda3/bin/python.

Unknowns: F(i,j), G(s,j), H(s,i) in F_p for s in R, i, j in Z_D.  f(s,i,j) = F(i,j) + G(s,j) + H(s,i).
Cell condition for every s in R, i, j:  f = 0  or  cl_D(f) in K - s - i - j;  and f(0,0,0) != 0.
Gauge (PROVED in the report, Lemma G3): G(0,.) = 0, H(0,.) = 0, H(.,0) = 0; P_D-scaling: f(0,0,0) = g^c with
c the least element of K... we only fix f(0,0,0) in {g^c : c in K, c = 0 mod D-class} -- see option.
With the gauge, f(0,i,j) = F(i,j), so F(i,j) ranges over the allowed set of cell (0,i,j) only.
Encoding: one-hot F, G(s,.), H(s,.) (s != 0); auxiliary S(s,i,j) with S[u+v] <= G(s,j)=u & H(s,i)=v;
forbid (S = w, F = t) when w + t is not allowed.  Exactly as in sat3.py's argument, a model gives a valid step
and a valid step gives a model (S = exact sum), so UNSAT is sound given the gauge lemma.
usage: rc3_sat.py gen p D R(comma) K(comma) out.cnf      -> writes CNF and out.cnf.map (json)
       rc3_sat.py dec out.cnf.map model.txt              -> prints JSON of F, G, H and re-checks the cell conditions
"""
import sys, json, itertools, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ell_common as E


def allowed_set(p, g, D, K, s, i, j, ind):
    tgt = {(m - s - i - j) % D for m in K}
    A = {x for x in range(1, p) if ind[x] in tgt}
    if (s % D, i, j) != (0, 0, 0):
        A.add(0)
    return A


def gen(p, D, R, K, path, scale_one=True, ansatz=None):
    g = E.primitive_root(p)
    ind = {x: E.cls(x, p, g, D) for x in range(1, p)}
    R = [0] + sorted({r % D for r in R} - {0})
    nv = [0]
    cl = []
    def new(n):
        v = list(range(nv[0] + 1, nv[0] + n + 1)); nv[0] += n; return v
    def onehot(vs):
        cl.append(list(vs))
        for a, b in itertools.combinations(vs, 2):
            cl.append([-a, -b])
    var = {}
    # F(i,j): domain = allowed set of cell (0,i,j)
    for i in range(D):
        for j in range(D):
            dom = sorted(allowed_set(p, g, D, K, 0, i, j, ind))
            if (i, j) == (0, 0) and scale_one:
                # P_D-scaling: f(0,0,0) has class c0 in K; any element of Q_{c0} can be scaled to g^{c0}
                dom = sorted({pow(g, c % D, p) for c in K})  # representatives g^c, c in K
            vs = new(len(dom)); onehot(vs)
            var[('F', i, j)] = dict(zip(dom, vs))
    for s in R[1:]:
        for j in range(D):
            vs = new(p); onehot(vs); var[('G', s, j)] = dict(zip(range(p), vs))
        for i in range(D):
            if i == 0:
                vs = new(1); cl.append([vs[0]]); var[('H', s, i)] = {0: vs[0]}
            else:
                vs = new(p); onehot(vs); var[('H', s, i)] = dict(zip(range(p), vs))
    def tie(a_, b_):
        for v in set(a_) | set(b_):
            if v in a_ and v in b_:
                cl.append([-a_[v], b_[v]]); cl.append([a_[v], -b_[v]])
            elif v in a_:
                cl.append([-a_[v]])
            else:
                cl.append([-b_[v]])
    if ansatz == 'sym19':      # periodic3 on G, H plus F(i+3, j-3) = F(i, j) (the symmetry of the p = 19 witness)
        for i in range(D):
            for j in range(D):
                tie(var[('F', (i + 3) % D, (j - 3) % D)], var[('F', i, j)])
        ansatz = 'periodic3'
    if ansatz == 'periodic3':   # optional restriction (SAT stays valid; UNSAT then only excludes the ansatz)
        for s in R[1:]:
            for nm in ('G', 'H'):
                for j in range(3, D):
                    a_, b_ = var[(nm, s, j)], var[(nm, s, j % 3)]
                    for v in range(p):
                        if v in a_ and v in b_:
                            cl.append([-a_[v], b_[v]]); cl.append([a_[v], -b_[v]])
                        elif v in a_:
                            cl.append([-a_[v]])
                        elif v in b_:
                            cl.append([-b_[v]])
    for s in R[1:]:
        for i in range(D):
            for j in range(D):
                A = allowed_set(p, g, D, K, s, i, j, ind)
                Sv = new(p)
                for u, a in var[('G', s, j)].items():
                    for w, b in var[('H', s, i)].items():
                        cl.append([-a, -b, Sv[(u + w) % p]])
                for t, c in var[('F', i, j)].items():
                    for w in range(p):
                        if (w + t) % p not in A:
                            cl.append([-Sv[w], -c])
    with open(path, 'w') as f:
        f.write('p cnf %d %d\n' % (nv[0], len(cl)))
        for c in cl:
            f.write(' '.join(map(str, c)) + ' 0\n')
    json.dump({'p': p, 'D': D, 'R': R, 'K': list(K), 'g': g,
               'var': {'%s,%d,%d' % k: {str(a): b for a, b in v.items()} for k, v in var.items()}},
              open(path + '.map', 'w'))
    return nv[0], len(cl)


def decode(mapfile, model):
    M = json.load(open(mapfile))
    true = set()
    for line in open(model):
        if line.startswith('v'):
            true |= {int(x) for x in line.split()[1:] if int(x) > 0}
    p, D, R, K = M['p'], M['D'], M['R'], M['K']
    val = {}
    for key, dom in M['var'].items():
        hits = [int(a) for a, b in dom.items() if b in true]
        assert len(hits) == 1, (key, hits)
        val[key] = hits[0]
    F = {(i, j): val['F,%d,%d' % (i, j)] for i in range(D) for j in range(D)}
    G = {(s, j): (val['G,%d,%d' % (s, j)] if s else 0) for s in R for j in range(D)}
    H = {(s, i): (val['H,%d,%d' % (s, i)] if s else 0) for s in R for i in range(D)}
    return p, D, R, K, F, G, H


def check_step(p, D, R, K, F, G, H):
    g = E.primitive_root(p)
    bad = []
    for s in R:
        for i in range(D):
            for j in range(D):
                v = (F[(i, j)] + G[(s, j)] + H[(s, i)]) % p
                if v == 0:
                    if (s, i, j) == (0, 0, 0): bad.append((s, i, j, 'zero at origin'))
                    continue
                if (E.cls(v, p, g, D) + s + i + j) % D not in {m % D for m in K}:
                    bad.append((s, i, j, v))
    return bad


if __name__ == '__main__':
    if sys.argv[1] == 'gen':
        p, D = int(sys.argv[2]), int(sys.argv[3])
        R = [int(x) for x in sys.argv[4].split(',')]; K = [int(x) for x in sys.argv[5].split(',')]
        print('vars %d clauses %d' % gen(p, D, R, K, sys.argv[6], ansatz=(sys.argv[7] if len(sys.argv) > 7 else None)))
    else:
        p, D, R, K, F, G, H = decode(sys.argv[2], sys.argv[3])
        bad = check_step(p, D, R, K, F, G, H)
        print(json.dumps({'p': p, 'D': D, 'R': R, 'K': K, 'bad': bad,
                          'F': [[F[(i, j)] for j in range(D)] for i in range(D)],
                          'G': {s: [G[(s, j)] for j in range(D)] for s in R},
                          'H': {s: [H[(s, i)] for i in range(D)] for s in R}}))

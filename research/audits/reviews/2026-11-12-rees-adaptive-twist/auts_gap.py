"""Compute Aut(G) generators with GAP/autpgrp for G = exp(L) and convert them to Lie automorphism
matrices of L (rows = images of the adapted basis), each verified to be a Lie automorphism.
Output: auts/<name>_<p>.json  {name,p,m,cls,level,D,size,gens}"""
import sys, os, json, subprocess, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from alg import HAND, degraaf, adapt, gap_pc, br, bch
GAP = '/opt/anaconda3/envs/qsearch-cas/bin/gap'
OUT = os.path.join(HERE, 'auts'); os.makedirs(OUT, exist_ok=True)

def log_word(a, D, p, cls):
    m = D.shape[0]; X = np.zeros(m, dtype=np.int64)
    for i in range(m):
        if a[i]:
            e = np.zeros(m, dtype=np.int64); e[i] = a[i] % p
            X = bch(X, e, D, p, cls)
    return X % p

def run(name, m, brk, p):
    fn = os.path.join(OUT, f'{name}_{p}.json')
    if os.path.exists(fn): return json.load(open(fn))
    D, level, cls = adapt(m, brk, p)
    if cls >= p or cls > 4: return None
    g = gap_pc(name, D, level, cls, p)
    tmp = os.path.join(OUT, f'{name}_{p}.g'); res = os.path.join(OUT, f'{name}_{p}.gout')
    with open(tmp, 'w') as f:
        f.write('LoadPackage("autpgrp");;\n' + g + '\n')
        f.write(f'''pc := FamilyPcgs(G);; if not IsConfluent(G) then Print("NOTCONFLUENT\\n"); fi;
A := AutomorphismGroup(G);;
PrintTo("{res}", "SIZE ", Size(A), "\\n");
for a in GeneratorsOfGroup(A) do AppendTo("{res}", "GEN ", List(pc, x -> ExponentsOfPcElement(pc, Image(a, x))), "\\n"); od;
AppendTo("{res}", "END\\n");
QUIT;
''')
    subprocess.run(['nice', '-n', '19', GAP, '-q', tmp], stdin=subprocess.DEVNULL, capture_output=True, timeout=3000)
    txt = open(res).read().replace('\n ', '').replace('\\\n', '')
    assert 'END' in txt, txt[:500]
    size = int(txt.split('SIZE ')[1].split()[0]); gens = []
    for line in txt.splitlines():
        if line.startswith('GEN '):
            ex = json.loads(line[4:].replace(' ', ''))
            M = np.array([log_word(a, D, p, cls) for a in ex], dtype=np.int64)
            for i in range(m):
                for j in range(m):
                    assert ((D[i, j] @ M) % p == br(M[i], M[j], D, p)).all(), (name, p, 'not a Lie aut')
            gens.append(M.tolist())
    rec = dict(name=name, p=p, m=m, cls=cls, level=level, D=D.tolist(), size=size, gens=gens)
    json.dump(rec, open(fn, 'w'))
    return rec

if __name__ == '__main__':
    only = sys.argv[1:]
    for p in (5, 7):
        algs = dict(HAND); algs.update(degraaf(p))
        for name, (m, brk) in algs.items():
            if only and name not in only: continue
            pass
            r = run(name, m, brk, p)
            if r: print(name, p, 'class', r['cls'], '|Aut| =', r['size'], 'gens', len(r['gens']), flush=True)

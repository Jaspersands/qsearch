import json
def pf(n):
    s=set(); d=2
    while d*d<=n:
        while n%d==0: s.add(d); n//=d
        d+=1
    if n>1: s.add(n)
    return s
def lpr(p):
    fs=pf(p-1)
    for g in range(2,p):
        if all(pow(g,(p-1)//q,p)!=1 for q in fs): return g
print(lpr(229), lpr(7), lpr(13))
base='/Users/jaspersands/Developer/qsearch/research/audits/reviews/2026-11-13-rees-headline-below-38/'
d=json.load(open(base+'v2/certs_tl6_all.json'))
bad=[p for p,v in d['found'].items() if v['g']!=lpr(int(p))]
print('tl6 certs with g != least primitive root:', len(bad), 'of', len(d['found']), bad[:5])
d=json.load(open(base+'certs_stage1.json'))
for k,v in d.items():
    bad=[p for p,c in v['found'].items() if c['g']!=lpr(int(p))]
    print(k, len(bad), 'of', len(v['found']), bad[:3])

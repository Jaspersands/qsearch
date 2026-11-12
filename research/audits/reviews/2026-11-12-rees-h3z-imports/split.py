import sys
txt=open(sys.argv[1],encoding='utf-8').read()
pages=txt.split('\f')
out=[]
for pi,p in enumerate(pages):
    lines=p.split('\n')
    W=max((len(l) for l in lines),default=0)
    if W<100:
        out.append(f'=== PAGE {pi+1} (single) ===\n'+p); continue
    # find best cut: column c in [50,W-30] where most lines have space at c and c-1
    best=None;bs=-1
    for c in range(50,min(W-20,110)):
        s=sum(1 for l in lines if len(l)<=c or (l[c-1]==' ' and l[c]==' '))
        if s>bs: bs=s;best=c
    L=[l[:best].rstrip() for l in lines]; R=[l[best:].strip() for l in lines]
    out.append(f'=== PAGE {pi+1} LEFT (cut {best}) ===\n'+'\n'.join(x for x in L)+f'\n=== PAGE {pi+1} RIGHT ===\n'+'\n'.join(R))
open(sys.argv[2],'w').write('\n'.join(out))

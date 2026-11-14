import difflib,sys,re
snap=open('2026-11-14-rees-full-sync/core-snapshot-68pp.tex').read().split('\n')
slim=open('2026-11-14-rees-core-slim/main-core-slim.tex').read().split('\n')
for n in map(int,sys.argv[1:]):
    l=slim[n-1]; w=l.split()
    best=max(range(len(snap)),key=lambda i: difflib.SequenceMatcher(None,w,snap[i].split(),autojunk=False).ratio() if abs(len(snap[i])-len(l))<3*len(l)+200 else 0)
    sw=snap[best].split()
    print(f'=== slim L{n} vs snap L{best+1}')
    sm=difflib.SequenceMatcher(None,sw,w,autojunk=False)
    for op,a,b,c,d in sm.get_opcodes():
        if op!='equal': print(f'  {op}: [-{" ".join(sw[a:b])}-] {{+{" ".join(w[c:d])}+}}'[:1500])

"""Word diff of one labelled environment (+ following proof): snapshot vs full version.
Prints [-snapshot-only-] and {+full-only+} spans. Read-only."""
import re,glob,difflib,sys
D='/Users/jaspersands/Developer/qsearch/'
snap=open(D+'research/audits/reviews/2026-11-14-rees-full-sync/core-snapshot-68pp.tex').read()
full=open(D+'docs/papers/rees-hsp/main.tex').read()
for f in sorted(glob.glob(D+'docs/papers/rees-hsp/appendix-*.tex')):
    full+='\n\n'+open(f).read()
ENV=r'(theorem|lemma|proposition|corollary|remark|definition|table)'
def envs(t):
    out={}
    for m in re.finditer(r'\\begin\{'+ENV+r'\}',t):
        e=m.group(1); end=t.find('\\end{'+e+'}',m.end())
        body=t[m.start():end]
        lab=re.search(r'\\label\{([^}]*)\}',body)
        if not lab: continue
        rest=t[end:end+20000]
        pm=re.match(r'\s*\\end\{'+e+r'\}\s*(\\begin\{proof\}.*?\\end\{proof\})',rest,re.S)
        out[lab.group(1)]=body+(pm.group(1) if pm else '')
    return out
S=envs(snap);F=envs(full)
for k in sys.argv[1:]:
    if k not in S or k not in F: print('##',k,'not in both', k in S, k in F); continue
    a=S[k].split();b=F[k].split()
    sm=difflib.SequenceMatcher(None,a,b,autojunk=False)
    print('##',k,'ratio=%.3f'%sm.ratio())
    for op,i1,i2,j1,j2 in sm.get_opcodes():
        if op=='equal': continue
        print('  [-%s-] {+%s+}'%(' '.join(a[i1:i2]),' '.join(b[j1:j2])))

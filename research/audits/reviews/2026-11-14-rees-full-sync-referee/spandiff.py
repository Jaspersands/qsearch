"""Word diff of two line ranges: snapshot a1-a2 vs full main.tex b1-b2. Read-only."""
import sys,difflib
D='/Users/jaspersands/Developer/qsearch/'
S=open(D+'research/audits/reviews/2026-11-14-rees-full-sync/core-snapshot-68pp.tex').read().split('\n')
F=open(D+'docs/papers/rees-hsp/main.tex').read().split('\n')
a1,a2,b1,b2=map(int,sys.argv[1:5])
a=' '.join(S[a1-1:a2]).split(); b=' '.join(F[b1-1:b2]).split()
sm=difflib.SequenceMatcher(None,a,b,autojunk=False)
print('ratio=%.3f'%sm.ratio())
for op,i1,i2,j1,j2 in sm.get_opcodes():
    if op!='equal': print('  [-%s-] {+%s+}'%(' '.join(a[i1:i2]),' '.join(b[j1:j2])))

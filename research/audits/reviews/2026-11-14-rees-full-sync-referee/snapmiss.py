"""Snapshot sentences (>=40 chars) absent from the synced full version after normalising whitespace,
theta->lambda, \\bigcup->\\cup, sec:proof-main->sec:main-proof. Read-only."""
import re,glob
D='/Users/jaspersands/Developer/qsearch/'
snap=open(D+'research/audits/reviews/2026-11-14-rees-full-sync/core-snapshot-68pp.tex').read()
snap=snap[snap.find('\\begin{document}'):]
new=open(D+'docs/papers/rees-hsp/main.tex').read()
for f in glob.glob(D+'docs/papers/rees-hsp/appendix-*.tex'): new+=open(f).read()
def norm(s):
    s=re.sub(r'%[^\n]*','',s)
    s=s.replace('\\theta','\\lambda').replace('\\bigcup','\\cup').replace('sec:proof-main','sec:main-proof').replace('\\fullv','this version')
    return re.sub(r'\s+',' ',s).strip()
N=norm(new)
for s in re.split(r'(?<=[.;:])\s+(?=[A-Z\\(])',norm(snap)):
    if len(s)>=40 and s not in N: print('-',s[:300]);print()

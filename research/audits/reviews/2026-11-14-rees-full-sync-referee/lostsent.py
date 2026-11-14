"""Sentences of the pre-sync full main.tex absent (after whitespace normalisation) from the synced full version
(main.tex + appendices). Read-only."""
import re,glob
D='/Users/jaspersands/Developer/qsearch/'
old=open(D+'research/audits/reviews/2026-11-09-rees-paper-pass-prep/backup-full-pre-sync-2026-11-14/main.tex').read()
new=open(D+'docs/papers/rees-hsp/main.tex').read()
for f in glob.glob(D+'docs/papers/rees-hsp/appendix-*.tex'): new+=open(f).read()
norm=lambda s:re.sub(r'\s+',' ',s).strip()
N=norm(new)
sents=re.split(r'(?<=[.;])\s+(?=[A-Z\\])',old)
for s in sents:
    s2=norm(s)
    if len(s2)<40: continue
    if s2 not in N:
        print('-',s2[:400]);print()

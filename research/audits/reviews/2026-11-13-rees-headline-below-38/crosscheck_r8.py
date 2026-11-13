"""Cross-check of rule.py against exponents_r8.py (2026-11-13-rees-k9-bottleneck, imported read-only).
R8 uses inputs that are not proved here (two-level contractions at kappa >= 6 from the E_2 tables,
etc.), so R8 <= ours is expected; ours < R8 would flag a bug or a node R8 lacks."""
import sys, os, math
HERE = os.path.dirname(os.path.abspath(__file__))
K9 = os.path.join(HERE, '..', '2026-11-13-rees-k9-bottleneck')
PM = int(sys.argv[1]) if len(sys.argv) > 1 else 3000
sys.path.insert(0, K9); old = sys.argv; sys.argv = [old[0], str(PM)]
cwd = os.getcwd(); os.chdir(K9)
import exponents_r8 as R8
os.chdir(cwd); sys.argv = old
import rule
rule.CERTS = rule.load_certs()
import json
raw = json.load(open(os.path.join(HERE, 'tierB.json')))
for k, v in raw.items():
    p, kappa, kind = k.split('|'); rule.TIERB[(int(p), int(kappa), kind)] = v
lt, gt, eq = [], [], 0
Eours, Er8 = {}, {}
for p in rule.HS.sieve(PM):
    if p < 3: continue
    e = rule.degrees(p)
    for k in e:
        a, b = e[k][0], R8.r8(k, p)
        if a < b: lt.append((p, k, a, b, e[k][1]))
        elif a > b: gt.append((p, k, a, b))
        else: eq += 1
    if p > 9:
        Eours[p] = rule.E_of(e, p, 9); Er8[p] = R8.E(R8.r8, 9, p)
print('pairs equal', eq, ' ours < R8:', len(lt), lt[:20])
print(' ours > R8:', len(gt), gt[:40])
print('c=9 max ours', max(Eours.values()), sorted(q for q in Eours if Eours[q] == max(Eours.values())))
print('c=9 max R8  ', max(Er8.values()), sorted(q for q in Er8 if Er8[q] == max(Er8.values())))
print('primes with E_ours != E_R8 at c=9:', [(q, Eours[q], Er8[q]) for q in Eours if Eours[q] != Er8[q]][:40])

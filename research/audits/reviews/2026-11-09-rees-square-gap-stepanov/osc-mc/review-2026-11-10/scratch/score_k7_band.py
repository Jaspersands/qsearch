"""Score mechanical item 6 by osc-mc/predictions_k7_lam03_band.txt (written 12:24:39 before the runs).
Run from osc-mc:  nice -n 19 python -I review-2026-11-10/scratch/score_k7_band.py <dir with the npz files>"""
import sys, os, statistics as st
sys.path.insert(0, '.')
import k6_spike_survey as ks
from scipy.stats import spearmanr
SP = sys.argv[1]
files = {34259: 'mc_k7_p34259_s19.npz', 34273: 'mc_k7_p34273_s21.npz', 34469: 'mc_k7_p34469_s23.npz',
         35281: 'mc_k7_p35281_s25.npz', 36541: 'mc_k7_p36541_s27.npz', 35099: 'mc_k7_p35099_s13.npz',
         34847: 'mc_k7_p34847_s13.npz', 34693: 'split_k7_p34693_all.npz'}
symR = {34259: 22.05, 34273: 9.43, 34469: 16.69, 35281: 15.79, 36541: 15.32, 35099: 21.33, 34847: 16.26,
        36037: 44.19, 34693: 44.22}
R = {p: ks.analyse(os.path.join(SP, f)) for p, f in files.items()}
R[36037] = ks.analyse('mc_k7_p36037_s13.npz')
print('    p    lam   symR  conf  N1/mu1        B_L (z; 2sig)            B_D (z; <2sig)   PW_pair [floor]  CS')
for p in sorted(R):
    r = R[p]
    print('%6d  %.3f  %5.2f  %5d  %.3f(%.3f)  %.3f (%5.1f; %.3f-%.3f)  %6.2f (%5.1f; <%6.2f)  %.3f [%.3f] %.3f' % (
        p, r['lam'], symR[p], r['nconf'], r['N1mu1'], r['N1mu1_se'], r['L'], r['L_z'], r['L_lo'], r['L_hi'],
        r['D'], r['D_z'], r['D_hi'], r['PW'], r['PW_floor'], r['PW_cs']))
band = [34259, 34273, 34469, 35281, 36541, 35099, 34847]
BL = [R[p]['L'] for p in band]; med = st.median(BL); maxhi = max(R[p]['L_hi'] for p in band)
print('band (7 primes not picked on symR): B_L %s; median %.3f, range %.3f-%.3f, max 2sig upper end %.3f' % (
    ' '.join('%.3f' % b for b in BL), med, min(BL), max(BL), maxhi))
a, b = R[36037], R[34693]
r1a = a['L_lo'] > maxhi; r1b = a['L'] / med >= 1.54
if any(x >= 0.50 for x in BL): r1 = 'NOT SHOWN'
elif r1a and r1b: r1 = 'SPIKE'
else: r1 = 'INCONCLUSIVE'
print('R1: 36037 B_L %.3f, 2sig lower %.3f vs band max upper %.3f (%s); ratio to band median %.2f (>= 1.54: %s) -> %s' % (
    a['L'], a['L_lo'], maxhi, r1a, a['L'] / med, r1b, r1))
if b['L_lo'] > maxhi: r2 = 'ABOVE'
elif any(x >= 0.387 for x in BL): r2 = 'INSIDE'
else: r2 = 'INCONCLUSIVE'
print('R2: 34693 B_L %.3f, 2sig lower %.3f vs band max upper %.3f -> %s (ratio to band median %.2f)' % (
    b['L'], b['L_lo'], maxhi, r2, b['L'] / med))
nine = sorted(symR); rho = spearmanr([symR[p] for p in nine], [R[p]['L'] for p in nine]).correlation
rho7 = spearmanr([symR[p] for p in band], [R[p]['L'] for p in band]).correlation
print('R3: Spearman(symR, B_L) over nine %.3f -> %s; over the seven band primes alone %.3f (not pre-registered)' % (
    rho, 'consistent' if rho >= 0.60 else ('no sign' if rho <= 0.20 else 'inconclusive'), rho7))
new = [34259, 34273, 34469, 35281, 36541]
print('predictions: each new B_L in 0.18-0.35: %s; band median in 0.22-0.30: %s; R1 SPIKE: %s; R2 ABOVE: %s; R3 rho 0.3-0.8: %s' % (
    all(0.18 <= R[p]['L'] <= 0.35 for p in new), 0.22 <= med <= 0.30, r1 == 'SPIKE', r2 == 'ABOVE', 0.3 <= rho <= 0.8))

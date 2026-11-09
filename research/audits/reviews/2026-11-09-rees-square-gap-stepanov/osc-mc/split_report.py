"""Group constants of the structured / unstructured parts written by mc_split.py (same estimators as
k6_spike_survey.analyse).  Usage: python split_report.py prefix [prefix ...]   (prefix = split/split_k6_p1657)"""
import sys
sys.path.insert(0, '.')
import k6_spike_survey as ks
print(' p     part  conf   N1/mu1   PW_pair db [floor]   B_L (z) <2sig    B_D[k^2/p] (z) <2sig   nu_D   c    B_L^cl  B_D^cl')
for pre in sys.argv[1:]:
    for q in ('all', 'str', 'uns'):
        r = ks.analyse('%s_%s.npz' % (pre, q))
        print('%5d  %s  %5d   %6.2f   %6.2f [%5.2f]    %6.3f (%5.1f) <%6.3f   %6.2f (%5.1f) <%6.2f  %5.2f  %5.2f  %6.3f %6.2f' % (
            r['p'], q, r['nconf'], r['N1mu1'], r['PW'], r['PW_floor'], r['L'], r['L_z'], r['L_hi'], r['D'], r['D_z'], r['D_hi'],
            r['D_nu'], r['c'], r['L_cl'], r['D_cl']))

"""kappa = 7 class values with the k6_spike_survey.analyse estimators (the equal_p_chain.py estimators).
Run from osc-mc: python -I review-2026-11-10/scratch/k7_class_values.py mc_k7_p36037_s13.npz mc_k7_p47041_s12.npz ..."""
import sys
sys.path.insert(0, '.')
import k6_spike_survey as ks
print('     p   lam   nS        conf  N1/mu1 (se)   PW_pair db [floor] CS  | B_L (z) <2sig        | B_D [k^2/p] (z) <2sig  nu_D | c     infl | B_D^cl (z)')
for f in sys.argv[1:]:
    r = ks.analyse(f)
    print('%6d %5.3f %9d %6d  %5.2f (%.2f)  %6.3f [%5.3f] %5.3f  | %5.3f (%5.1f) <%5.3f  | %6.2f (%5.1f) <%6.2f  %5.2f | %5.3f %5.2f | %5.2f (%4.1f)' % (
        r['p'], r['lam'], r['nS'], r['nconf'], r['N1mu1'], r['N1mu1_se'], r['PW'], r['PW_floor'], r['PW_cs'],
        r['L'], r['L_z'], r['L_hi'], r['D'], r['D_z'], r['D_hi'], r['D_nu'], r['c'], r['infl'], r['D_cl'], r['D_cl_z']))

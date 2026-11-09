"""Referee scratch: mc_classes vs mc_split at equal (k, p, nconf, seed); parts sum to the total."""
import numpy as np, sys
o = sys.argv[1]
m = np.load(o + '/mc_check.npz'); s = {q: np.load('%s/split_check_%s.npz' % (o, q)) for q in ('all', 'str', 'uns')}
print('nS %d/%d nconf %d/%d' % (m['nS'], s['all']['nS'], m['nconf'], s['all']['nconf']))
print('max|dS1| all-vs-mc_classes %.3g  max|dS2| %.3g  cnt equal %s  N1/mu1 %.4f/%.4f' % (
    abs(m['S1'] - s['all']['S1']).max(), abs(m['S2'] - s['all']['S2']).max(), (m['cnt'] == s['all']['cnt']).all(),
    float(m['N1']) / float(m['mu1']), float(s['all']['N1']) / float(s['all']['mu1'])))
print('parts: max|S1_str+S1_uns-S1_all| %.3g  cnt sum ok %s  N1 sum %.6g vs %.6g  Nunl sum %.6g vs %.6g  structured %d of %d' % (
    abs(s['str']['S1'] + s['uns']['S1'] - s['all']['S1']).max(), (s['str']['cnt'] + s['uns']['cnt'] == s['all']['cnt']).all(),
    float(s['str']['N1']) + float(s['uns']['N1']), float(s['all']['N1']), float(s['str']['Nunl']) + float(s['uns']['Nunl']), float(s['all']['Nunl']),
    int(s['str']['cnt'].sum()), int(s['all']['cnt'].sum())))

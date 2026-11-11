"""Case list for the e1-line-data split (2026-11-11-rees-sde-interval-s.md, section 3).
One case per orbit of admissible line data of the direction e1 = (1,0) (linedata_p{p}_K{K}.json):
fix gamma at the slots (e1, r), r = 2..m, to (u_r, v_r) of the orbit representative.
Output: one --fix string per line (int_cnf.py format 'D1,D2,lam:x,y;...').
usage: cases_e1.py p K > cases_e1_p{p}.txt
"""
import sys, json
p, K = int(sys.argv[1]), int(sys.argv[2])
J = json.load(open(f'linedata_p{p}_K{K}.json'))
for u, v, sz in J['orbits']:
    print(';'.join(f'1,0,{r}:{u[i]},{v[i]}' for i, r in enumerate(J['R'])))

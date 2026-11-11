"""E2 check: strong Fourier sampling over the whole (non-abelian) group G = free23, p = 5, 7.
For hard cyclic H = <exp eta> (eta has a degree-one component) and M = H gamma_2: the probability,
under Fourier sampling of the coset state, that the measured irrep sigma admits ANY M-eigenvector
(chi_sigma restricted to M has a linear constituent).  Prediction: exactly 1/p.
Uses GAP character tables; pc presentation from alg.py."""
import sys, os, json, random, subprocess, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from alg import HAND, adapt, gap_pc, normal_word
GAP = '/opt/anaconda3/envs/qsearch-cas/bin/gap'
for p in (5, 7):
    m, brk = HAND['free23']; D, level, cls = adapt(m, brk, p)
    etas = [e for e in __import__('itertools').product(range(p), repeat=m) if e[0] or e[1]]
    sel = random.Random(1).sample(etas, 4)
    words = [normal_word(np.array(e), D, p, cls) for e in sel]
    g = gap_pc('free23', D, level, cls, p)
    res = os.path.join(HERE, f'e2_free23_{p}.gout')
    script = g + f'''
pc := FamilyPcgs(G);; T := CharacterTable(G);; irr := Irr(T);;
PrintTo("{res}", "");
for w in {words} do
  h := PcElementByExponents(pc, w);; H := Subgroup(G, [h]);; M := ClosureGroup(H, DerivedSubgroup(G));;
  TM := CharacterTable(M);; lin := LinearCharacters(M);;
  tot := 0;; eig := 0;; eig_nonlin := 0;;
  for chi in irr do
    pr := chi[1] / Size(G) * Sum(List(Elements(H), x -> x^chi));;
    tot := tot + pr;;
    r := RestrictedClassFunction(chi, M);;
    if ForAny(lin, psi -> ScalarProduct(r, psi) > 0) then eig := eig + pr;; if chi[1] > 1 then eig_nonlin := eig_nonlin + pr;; fi; fi;
  od;
  AppendTo("{res}", w, " total ", tot, " eigen_possible ", eig, " from_deg_p ", eig_nonlin, "\\n");
od;
QUIT;
'''
    fn = os.path.join(HERE, f'e2_free23_{p}.g'); open(fn, 'w').write(script)
    subprocess.run(['nice', '-n', '19', GAP, '-q', fn], stdin=subprocess.DEVNULL, capture_output=True, timeout=3000)
    print('p =', p, 'eta =', sel); print(open(res).read(), flush=True)

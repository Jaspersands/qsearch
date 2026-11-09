"""One exact classical relative-norm control; never a full-solver proof."""
from pathlib import Path
import json
from sage.all import pari

pari('control_bnf = bnfinit(y^2-5)')
pari('control_r = Mod(y,y^2-5)')
pari('control_target = (40+17*control_r)/(40-17*control_r)')
pari('control_data = rnfisnorminit(control_bnf,x^3-2,0)')
pari('control_answer = rnfisnorm(control_data,control_target,50)')
assert int(pari('control_answer[2] == 1')) == 1
assert int(pari('norm(control_answer[1]) == control_target')) == 1

# Independent determinant of multiplication by 2+sqrt(5)+cuberoot(2).
pari('control_b = 2+control_r')
pari('control_M = [control_b,0,2;1,control_b,0;0,1,control_b]')
pari('control_U = [1,control_r,0;0,1,1;0,0,1]')
assert int(pari('matdet(control_M) == 40+17*control_r')) == 1
assert int(pari('matdet(control_U^-1*control_M*control_U) == matdet(control_M)')) == 1
pari('control_witness = Mod((2+control_r+x)/(2-control_r+x),x^3-2)')
assert int(pari('norm(control_witness) == control_target')) == 1

# Absolute norm loses finite support at the two primes above 31.
assert int(pari('norm(control_target)')) == 1
valuations = [int(pari(f'idealval(control_bnf,control_target,idealprimedec(control_bnf,31)[{j}])')) for j in (1, 2)]
assert sorted(valuations) == [-1, 1]
denominator = int(pari('denominator(lift(control_target),1)'))
assert denominator == 31
absolute_disc = int(pari('nfdisc(polcompositum(y^2-5,y^3-2)[1])'))
assert absolute_disc % 31 != 0

# Relative torsion norms need not be rational signs: degree two over Q(zeta3).
pari('control_zeta = Mod(y,y^2+y+1)')
pari('control_torsion_norm = matdet([control_zeta,0;0,control_zeta])')
assert int(pari('control_torsion_norm != 1 && control_torsion_norm != -1')) == 1
assert int(pari('control_torsion_norm^3 == 1')) == 1

result = {
    'status': 'PASS',
    'scope': 'Exact finite classical algebra and an existing PARI baseline only.',
    'base': 'K=Q(sqrt(5))',
    'extension': 'L=K(cuberoot(2)), non-Galois degree three',
    'target': str(pari('control_target')),
    'pari_rnfisnorm_witness': str(pari('control_answer[1]')),
    'pari_relative_norm_verified': True,
    'independent_relative_determinant_verified': True,
    'basis_change_determinant_verified': True,
    'absolute_norm_of_target': 1,
    'valuations_at_primes_above_31': valuations,
    'target_denominator': denominator,
    'absolute_discriminant_L': absolute_disc,
    'absolute_norm_only_support_rejected': True,
    'relative_torsion_norm': str(pari('control_torsion_norm')),
    'relative_torsion_is_not_just_sign': True,
    'full_solver_execution': False,
    'quantum_execution': False,
    'novelty_or_speedup': False,
}
Path(__file__).with_suffix('.json').write_text(json.dumps(result, indent=2) + '\n')
print('PASS: PARI norm witness, determinant, support cancellation and relative torsion.')

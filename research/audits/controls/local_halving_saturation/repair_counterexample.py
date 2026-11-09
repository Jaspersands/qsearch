"""Exact counterexample to an unqualified Claude chart-repair bound."""
import json
from pathlib import Path
import sympy as s
x,h=s.symbols('x h')
f=x**3+4*x-1; a=x-s.Rational(1,4); b=s.Rational(1,8)
assert f.subs(x,s.Rational(1,4)) == b*b
assert s.discriminant(f,x) == -283
c=s.cancel((f-b*b)/a)
ap=s.expand(c-2*h*b-h*h*a)
r=s.factor(s.resultant(a,f,x)); rp=s.factor(s.resultant(ap,f,x))
num=8*h**3-268*h**2+6*h-1
assert r == -s.Rational(1,64)
assert s.factor(rp-num**2/s.Integer(4096)) == 0
assert s.Poly(num,h,modulus=2).as_expr() == 1
# Every h in Z2 has odd numerator, so the two exact valuations are -6,-12.
# The report's claimed lower bound would require 6 <= -12.
assert not 6 <= -12
result={
 'status':'PASS','scope':'All integral dyadic h; falsifies the report bound, not halving.',
 'f':str(f),'point':['1/4','1/8'],'c':str(c),
 'resultant_a_f':str(r),'resultant_a_prime_f':str(rp),
 'v2_resultants':[-6,-12],'claimed_lower_bound':6,
 'numerator_odd_for_every_h_in_Z2':True,
 'source_of_error':'Unstated integrality of a,b; actual near-infinity inputs are not integral.',
 'first_inline_attempt':'Resultants computed correctly; a guessed sign/polynomial assertion was wrong. Corrected from exact CAS and rerun once.',
 'claim_gates':{'full_local_image':False,'global_selmer':False,'quantum_execution':False,'hardness':False}}
Path(__file__).with_name('repair_counterexample.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'status':result['status'],'v2_resultants':result['v2_resultants'],'bound_refuted':True}))

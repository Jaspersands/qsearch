"""Exact phase-sensitive finite falsifiers; no learner/asymptotic inference."""
from pathlib import Path
import json
from sage.all import QQ, CyclotomicField, matrix, vector, prod

K = CyclotomicField(4)
ii = K.gen()
alpha = [K(QQ(3)/5), (12+16*ii)/25]
conj = lambda z: z.conjugate()
norm2 = lambda z: QQ(z*conj(z))
assert sum(map(norm2,alpha)) == 1
amps = [K(0)]*64
for x in range(64):
    y = x ^ (63 if x.bit_count()%2 else 0)
    amps[y] = prod(alpha[(x>>j)&1] for j in range(6))
assert sum(map(norm2,amps)) == 1
assert all((x ^ (63 if x.bit_count()%2 else 0)).bit_count()%4
           == x.bit_count()%4 for x in range(64))

prob_total, nonzero = QQ(0), 0
for a in range(2):
 for c in range(2):
  bell1 = sum((-1)**(c*z)*alpha[z^a]*alpha[z] for z in range(2))
  for b in range(2):
   for d in range(2):
    bell2 = sum((-1)**(d*w)*alpha[w^b]*alpha[w] for w in range(2))
    branch = []
    for r in range(4):
     total = K(0)
     for z in range(2):
      for w in range(2):
       bits=[r&1,z^a,z,w^b,w,(r>>1)&1]
       y=sum(bit<<j for j,bit in enumerate(bits))
       total += (-1)**(c*z+d*w)*amps[y]/2
     branch.append(total)
    u,v=a^b,c^d
    corrected=[(-1)**(v*y)*alpha[y^u] for y in range(2)]
    predicted=[(-1)**(v*u)*bell1*bell2/2*corrected[r&1]*corrected[(r>>1)&1]
               for r in range(4)]
    assert branch == predicted
    probability=sum(map(norm2,branch))
    assert probability == norm2(bell1)*norm2(bell2)/4
    prob_total += probability
    nonzero += int(probability != 0)
assert prob_total == 1 and nonzero == 9

rho = matrix(K,2,2,lambda a,b:sum(amps[a+2*z]*conj(amps[b+2*z]) for z in range(32)))
pin=matrix(K,2,2,lambda a,b:alpha[a]*conj(alpha[b]))
paulis=[matrix(K,[[0,1],[1,0]]),matrix(K,[[0,-ii],[ii,0]]),matrix(K,[[1,0],[0,-1]])]
rin=[QQ((P*pin).trace()) for P in paulis]
rout=[QQ((P*rho).trace()) for P in paulis]
assert rout == [r**5 for r in rin]

# Native CCZ state: exact Pauli expectations from its Boolean cubic.
def f(x):
    return int((x&7)==7)
coeffs=[]
for a in range(8):
 for b in range(8):
  value=ii**((a&b).bit_count())*sum(
      (-1)**(f(x)+f(x^a)+(b&x).bit_count()) for x in range(8))/8
  assert value.imag()==0
  coeffs.append(QQ(value))
assert sum(abs(r)==1 for r in coeffs)==1
assert max(abs(r) for r in coeffs if abs(r)!=1)==QQ(1)/2

# A linear derivative can be canceled by the Pauli phase. The criterion
# is constancy of the TOTAL quadratic phase, not of the derivative alone.
qphase=lambda x:int((x&3)==3)
derivative=[qphase(x)^qphase(x^1) for x in range(4)]
assert len(set(derivative))==2
assert QQ(sum((-1)**(derivative[x]+((2&x).bit_count())) for x in range(4)))/4==1

out={"scope":"exact finite phase and Pauli controls only",
     "complex_input":list(map(str,alpha)),"bell_outcomes":16,
     "nonzero_bell_outcomes":nonzero,"total_probability":str(prob_total),
     "input_pauli_xyz":list(map(str,rin)),"output_pauli_xyz":list(map(str,rout)),
     "ccz_signed_pauli_stabilizers":1,"ccz_max_nonstabilizer_magnitude":"1/2",
     "linear_derivative_canceled_by_pauli":True,
     "claim_gates":{key:False for key in ["learner","quantum_execution","novelty",
         "classical_separation","general_coherent_receiver_impossibility",
         "asymptotic_inference_from_controls"]}}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({"status":"passed","all_bell_branches":16,"nonzero":nonzero,
                  "complex_phase_and_Y_sign":"exact","ccz_gap":"exact finite check"}))

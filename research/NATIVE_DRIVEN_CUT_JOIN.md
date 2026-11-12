# Native driven cut-and-join candidate: explicit control, no addressed gates

Research candidate, NOT established theorem. Input numerical total momentum D, explicit occupation partition mu of D, an explicit list of m pulses (label S or N, signed binary rational time 2*pi*a/c), and TV tolerance 2^-b. Native canonical bosonic modes 1..D, sum k n_k=D. Output full occupation nu.
S=sum_(i,j>=1) sqrt(i*j*(i+j)) [a_i^dag a_j^dag a_(i+j)+a_(i+j)^dag a_i a_j], with ordered i,j and i+j<=D.
N=sum_k k^2 n_k. Both preserve D. N diagonal integer; S is the alpha=1 cut-and-join Hamiltonian, eigenvalue 2*sum_boxes(column-row), integers. Norms O(D^2). N evolution is directly computable. For the proposed reduction, S is simulated by its native O(D^2)-sparse occupation matrix at polynomial TOTAL ABSOLUTE DURATION; this suffices for a quantum polynomial upper bound. No general binary-time Schur fast-forwarding interface is required or promoted here. The immutable paid packet unnecessarily admitted that stronger interface; do not import it as a verified result. No free arbitrary target gates, chosen couplings, measurements/feedforward, or state loading.

Motivation: driven quantum Benjamin-Ono-type dynamics and whether efficient integrable transformations become programmable under native dispersion kicks. Target constructive proof: uniform classical polynomial-time compilation of an n-qubit size-G circuit into these TWO controls, with D,m,total bit length polynomial(n,G,1/epsilon) at inverse-polynomial epsilon. Initial occupation and decoded output must be explicit. If proven, full sampler classically polynomial would imply BPP=BQP (standard assumption only, no unconditional hardness or Shor-level novelty). General sampler baseline dense p(D)=exp(O(sqrt D)) linear algebra; N alone is trivial on occupation inputs. S is free fermionic, but a classical sampler for arbitrary BOSONIC occupation input/readout is NOT granted by that fact. Their composition is not automatically Gaussian. No circuit implementation requested.

Parent proposed mechanism (attack before extending):
1. Under conjugation by exp(i theta N), C_ij=a_i^dag a_j^dag a_(i+j) has frequency i^2+j^2-(i+j)^2=-2ij. Discrete Fourier averaging over M>2D^2 roots isolates fixed product ij. Use only actual N/S pulses, signed rational times, product formulas and polynomial operator-norm/error bounds. No free linear combinations or exponential commutator depth.
2. Choose 2n DISTINCT ODD PRIMES p_i,q_i with all unordered pair sums unique (Sidon). Greedy selection among polynomially many primes should work: each new prime forbids O(n^3) sums/differences; sieve polynomial range. Need explicit bound/proof. All local sum modes c_i=p_i+q_i and cross sum modes p_i+p_j distinct and even, hence distinct from primes. D=sum c_i polynomial n.
3. For semiprime pq, only factor pairs (p,q) and (1,pq). Arrange pq>D so latter has 1+pq>D, hence absent. This condition is CRITICAL: small first primes do not ensure it! Choose primes in a polynomial interval [R,2R], with R sufficiently large relative n, enough candidates for greedy Sidon, then D<=4nR and pq>=R^2>D for R>4n. Need elementary proven prime count/sieve bound; do not hide number theory promise.
4. Encode qubit i: |0>=one boson in c_i and none p_i,q_i; |1>=one each in p_i,q_i and none c_i. Both total momentum c_i; initial |0...0> is occupation mu=(c_1,...,c_n). Isolated C_pq+C_pq^dag gives X, conjugated quadrature gives Y; account ordered-pair factor 2 and sqrt(pqc). Unwanted transitions? Show exact invariant two-level code per local gate.
5. For two qubits isolate C=a_(p_i)^dag a_(p_j)^dag a_r, r=p_i+p_j initially empty. Algebra [C,C^dag]=n_pi*n_pj - n_r*(n_pi+n_pj+1), up to sign depending convention. Commutator of X=C+Cdag,Y=i(Cdag-C) gives diagonal cross-Kerr. On code with n_r=0 it is n_pi*n_pj, a CZ generator. A bounded-length group-commutator product formula approximates this diagonal evolution with polynomial pulses/error/norm at polynomial D. Ancilla need only return up to controlled global error; full error budget and final bad-code decode paid. No exact exponentially long BCH isolation.
6. Finite coefficient/angle approximation and discrete average synthesis charged. It is sufficient polynomial(1/epsilon) for a BQP reduction, NOT claimed poly(log1/epsilon) compiler. Each supplied native pulse may still be fast-forwarded in its binary time. No log-number-of-pulses access.

Strong falsifiers: semiprime alias survives cutoff, Sidon prime construction costs superpoly, code leakage under local gate, shared ancilla collisions, commutator control requires exponential words, coefficient/angle/time precision exponential, actual S normalization differs, polynomial classical representation preserved by both controls. Mere Lie-algebra full rank or finite simulations are insufficient. Corpus been-tried and baselines ran Nov13; retrieved matches did not contain this exact mechanism, not novelty evidence. Primary MM Eq2.1 and its alpha=1 statement checked in attached excerpt. No general bosonic-universality theorem is imported.

## Parent repair: exact cycle entangler and paid scope

Do not use BCH commutator simulation for the entangler. For distinct signal
modes a=p_i,b=p_j and empty r=a+b, put C=a_a^dag*a_b^dag*a_r and X=C+C^dag.
On code, signal populations are0/1. All blocks except signal11 are dark.
The11 block has conserved charges n_a+n_r=n_b+n_r=1 and basis
|11,0_r>,|00,1_r>; X is exactly PauliX there. Therefore exp(-i*pi*X)
is CZ on the logical code and returns r to vacuum. Spectator modes and
reference systems unchanged. This is an all-code algebraic deduction,
not finite controllability. Independent prime/code review in progress.

Actual Niu/Chuang/Shapiro1704.03431 Eq2–4/Theorem1 uses the same one-pump
qubit encoding and a sum-frequency pi cycle, with separately addressed
optical operations. Parent read actual proof. No novelty for this encoding
or addressed three-wave universality is claimed. Our remaining obligation
is the actual TWO-GLOBAL-CONTROL frequency compiler and polynomial mode
construction; no extra source optical operations are granted.

Primary prime supply: actual Rosser--Schoenfeld1962 Cor3 Eq3.8 supplies
pi(2R)-pi(R)>3R/(5logR) (use R>=2^20). Local source
sources/native_driven/rosser_schoenfeld_1962.txt physicalLF231–258 checked.
Greedy Sidon selection excludes O(n^3) integers at each of2n stages;
R=2^20*(2n+1)^4 is a candidate explicit all-n supply. D<=4nR<R²,
so selected semiprime pq>D and the factor pair1,pq is outside momentum.

Parent frequency derivation, under audit: choose M>2D²,theta_l=pi*l/M,
S_l=e^(i theta_l N) S e^(-i theta_l N). For m=pq, no other admitted pair
has this product. Then
 (2/M) sum_l cos(2pi*m*l/M) S_l = g*(C+Cdag),
 (2/M) sum_l sin(2pi*m*l/M) S_l = g*i*(Cdag-C),
where g=2*sqrt(pq(p+q)) (ordered distinct pair factor2).
After division by g the sum of weighted term norms <=2D²/g. First-order
unitary product formulas with r=poly(D,1/eta) cycles implement any bounded
X/Y angle to operator error eta; actual pulses are N conjugation, S weighted
small time, inverse N. Irrational cos/g coefficients are approximated by
binary rationals with total pulse-angle error budget paid. Full m=poly(n,G,
1/epsilon), BIT clock likewise. This is NOT a log(1/epsilon) reduction.

These constructed pulses have only polynomial total duration. If the
encoding closes, ordinary sparse Hamiltonian simulation already gives its
quantum upper bound: no fast-forwarding speedup, quantum-transform novelty,
or Shor-level algorithm follows. It concerns an explicit DRIVEN protocol;
no hardness transfers to the earlier static Macdonald condensate or BO
single-quench problem. A hypothetical polynomial classical full sampler
for all allowed driven inputs would simulate BQP; this conditional
complexity consequence is not an unconditional separation.

## First paid control reports: parent dispositions

Claude frequency completed201LF and entangler completed133LF, fully read;
whole OAI compiler and independent code proof still pending. Both derive
modulated discrete frequency projection and exact cycle CZ. Use the
unmerged native pulse list. In the frequency report, optional adjacent N
merge has wrong sign: chronological (2pi-theta_k)+theta_(k+1) is +2pi/M
mod2pi, not2pi-2pi/M. This does not affect its correct unmerged list.
Reject its blanket square-product obstruction: P9,D6 has only admitted
pair3,3. Frequency sees PRODUCTS; addressability depends on the full
admitted factor fiber. Keep the sufficient strict semiprime/cutoff guard.
The entangler report calls uniform unweighted averaging a parent error;
the packet actually requested Fourier filtering, not unweighted averaging.
Uniform averaging does vanish, so explicit modulation is essential.

Bothreports independently check exact alias/collision falsifiers. Without
cutoff, primepairs(3,11),(7,13),(5,17),D56: cross product3*7 has unwanted
pair1,21 and occupied sum22; a target pi cycle produces leakage
sin²(pi*sqrt(11/5)) from that independent alias block. Without ancilla
distinctness, pairs(3,7),(13,17),(5,11),D56 have cross3+13=16 equalc3;
input signals(1,0),pump1 couples with amplitude sqrt2, giving leakage
sin²(pi*sqrt2). These are construction-specific falsifiers, not no-go
for the native controls. Finite code dimension alone is never a classical
lower bound. Guarded full compiler remains under independent review.

## Closed written uniform encoding (parent composition)

Parent checked the complete249LF independent proof
reviews/2026-11-13-driven-prime-code-independent.md, including its elementary
prime supply, all greedy forbidden cases, whole-sector filtering, exact
code blocks and unitary product-formula clock. This closes a WRITTEN
uniform encoded-computation theorem for the stated TWO native controls.
For every n-qubit G-gate circuit over a fixed universal gate set and
0<epsilon<1, a deterministic classical poly(n,G,1/epsilon) BIT compiler
produces numerical D=O(n^5), explicit occupation mu, and polynomially many
signed rational-time S/N pulses. Total absolute duration and description
length are polynomial. Its decoded occupation output is epsilon-close
in TV to the circuit output. The proof is all-n; the singleD8 fixture is
only a normalization/alias check, fully parent-inspected (1004 assertions).

Composition details: compile the fixed universal one-qubit/CZ gates into
O(G) bounded-angle X/Y rotations and pi cycles. Use per-primitive norm
budget epsilon/(8G) in the independent pulse construction, with stricter
r/rounding constants as necessary. Telescoping preserves the full input
code and arbitrary reference up to total norm<epsilon/2; approximation
leakage is NOT reset between gates. Deterministic decoder checks every
code triple and all other modes and maps invalid patterns to a fixed bit
string, with no rejection. Trace-distance contraction bounds decoded TV.

The mathematical native-pulse endpoint is quantum polynomial at these
polynomial durations: explicitly prepare the occupation encoding, simulate
the O(D²)-sparse S and diagonal N with a total norm budget epsilon/2, and
measure/decode. Square-root weights are polynomial-bit computable; total
absolute duration bounds precision and accumulated simulation cost.
For complexity terminology take D unary (or retain complexity explicitly
polynomial in numericalD). No arbitrary-binary-time endpoint is asserted.
A classical polynomial sampler for ALL these native protocols at a fixed
small TV error would put BQP in BPP by composing this compiler with the
sampler and the deterministic decoder, using an amplified decision gap.
This is a conditional consequence, not an unconditional classical lower
bound or Shor-level algorithm. The construction uses ordinary universal
quantum simulation; it does not exploit or prove a fast-forwarding advantage.

Whole OAI report completed612LF and was fully parent-read/reaped. Its
all-n prime/filter/clock/decoder proof agrees with the retained independent
proof. Retain the already checked direct polynomial norm bound instead of
its optional tighter D^6 pulse exponent, and replace its unnecessarily
admitted general pulse implementation by ordinary sparse simulation at
the actually polynomial total duration. Explicit H,T decompositions check
with Y=-standardPauliY. Its exact Schur D4 witness <4|N|22>=1/3+2-10/3=-1
is parent-hand-checked and falsifies ONLY the common free-fermion Gaussian
shortcut; two occupied fermion substitutions cannot be a quadratic matrix
element. No extra finite test is needed.
No more control-infrastructure work is selected: exact addressed chi²
encoding is known, and a universal-control translation alone does not
answer the original STATIC integrable sampling problem.

Terminal35hash native_driven_round:3.396948USD estimated increment,
cumulative246.167200USD/191priced(Anth147.724550,OAI98.442650),FOURunknown
bills excluded. Estimates are not invoices/balances. All three reports
completed/nonempty/parent-read/reaped; no failed retry.

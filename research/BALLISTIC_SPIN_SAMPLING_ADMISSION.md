# Two-color full-reversal rational scattering: classical-prefix question

2026-11-14. PARKED after one bounded constructive classical attempt.
Known quantum circuit endpoint; reviewed scoped baselines and exact small-
prefix classical simulation, not a new full sampler or a new quantum algorithm.
No new quantum algorithm, novelty, hardness or separation is admitted.

## Selection and exact native model

Start STATE/TRAPS; BCS occupation readout is now classically matched. The
independent168-line selection note compares scattering, curve-zeta arithmetic
and a uniform-trace Khovanov receiver. Curve zeta is an already used published
primitive; the topology receiver has an elementary normalization problem and
no new preparation operation. Neither justifies a new subsystem. Scattering
has an actual polynomial circuit and a concrete classical-prefix question.
Corpus been-tried then actual primary-source checks preceded this admission;
results and PDFs are in audits/sources/ballistic_scattering_selection/.
The corpus baseline's LLL suggestion is an irrelevant text match, not an
applicable classical algorithm. Exact sector propagation, stochastic swaps,
fermionic/DPP sampling, tensor contraction and Bethe determinant formulas
are the real competitors.

Native input: N distinct rational rapidities v_0>...>v_(N-1), c>0 rational,
initial bitstring b with arbitrary extensive weight M, and accuracy epsilon.
There are TWO colors and N qubits, not N distinct distinguishable labels.
Output: the entire N-bit Born sample after COMPLETE all-pairs reversal.
All rational bit lengths are charged. No roots, eigenvectors, wave packets,
spectral gap, intermediate measurements, postselection or arbitrary gates.
Finite physical wave-packet scattering is NOT included without a paid
reduction. The explicit algebraic S-matrix circuit is the target here.

Fix the braid/position-wire convention, resolving the selection note's open
R versus checked-R ambiguity:
 R(d)=(c I+i d SWAP)/(c+i d), d=v_left-v_right>0.
This differs only by a global phase from exp(i atan(d/c) SWAP).
The source AppendixA coefficient (-ic I+d SWAP)/(ic+d) has the same
projective action. Track momentum labels through crossings deterministically.
Bubble the largest remaining rapidity to the right, then repeat on the
remaining prefix. Every unordered pair crosses once; output rapidities are
in increasing order. Yang-Baxter gives equivalent reduced reversal words.

R is exactly unitary with rational Q(i) entries and two unit-modulus
eigenvalues 1 and (c-id)/(c+id). Preparing b, compiling N(N-1)/2 bounded
2-qubit gates to error O(epsilon/N²), and measuring uses
poly(N,input bits,log(1/epsilon)) gates. Tiny/large d/c costs its input bits,
not inverse separation. This circuit is KNOWN prior machinery. Potential
advantage of its full extensive-spin output remains unestablished.

## Actual primary-source boundary

Aaronson--Bouland--Kuperberg--Mehraban arxiv1610.06646, physicalLF235--298,
Section3.3 LF612--705, AppendixA LF998--1083 and AppendixP LF2945--2956:
rapidity-constrained exchange circuits are prior art. Their Cor3.11 concerns
MeasRQBall, with N distinct labels, special/arbitrary input superpositions,
intermediate demolition measurements and MULTIPLICATIVE error. It cannot be
transferred to our two-color product input, no-intermediate-measurement,
full-reversal TV sampling. AppendixP explicitly asks about removing the
measurements. This is a statement about that source, not proof that the
present exact target has remained open in all later literature.
Their DQC1 single-amplitude theorem is not a complete Born sampler.

Alagic--Bapat--Jordan arxiv1407.1361 actual equation1 LF25--31 and
Theorems1/3/5 LF283--296,631--689: CONSTANT Yang-Baxter gates, a joint-product-
basis monomial family, or a Clifford family. A fixed generic R(d) above does
not satisfy the constant YBE. Moreover SWAP commutes with every Q tensor Q,
so such joint basis conjugation leaves R(d) unchanged; it cannot make its
nontrivial two-entry columns monomial. The fixed constant-YBE theorem does
not directly apply. This excludes those hypotheses, not every classical
method. Search found no verified current all-input classical sampler; no
absence/novelty conclusion is drawn from that search.

## Cheapest exact classical attacks

One exact Sage Q(i) control, audits/controls/ballistic_scattering_baselines/.
For N3,c1,v=(2,1,0), input bitmask2, word(0,1),(1,2),(0,1):
Born probabilities on masks1,2,4 are (2/5,1/5,2/5). Independent per-crossing
swap coins, probability d²/(c²+d²), give (3/10,3/10,2/5). TV=1/10.
This rejects ONLY measuring/dephasing at every crossing. The entire M1
sector is classically polynomial, so this example is not hardness evidence.
Exact unitarity, parameter-dependent YBE and failure of the constant YBE
were checked in the same finite control.

For N4,c1,v=(3,2,1,0), input occupied sites{0,2}, the six output probabilities
in lexicographic pairs01,02,03,12,13,23 are
 (4/125,169/500,9/100,9/100,81/500,36/125).
The determinant sampler built from the actual single-excitation transfer
matrix differs by TV48/125. More strongly NO complex two-particle Slater
state has this Born law: Plucker gives a triangle inequality among
 sqrt(p01*p23)=12/125, sqrt(p02*p13)=117/500,
 sqrt(p03*p12)=9/100.
The middle exceeds the other two by6/125. This is an exact algebraic
obstruction for ANY pure Slater orbital matrix, not only the obvious one.
It does not rule out mixtures, conditioned non-projection DPPs, tensor
networks, integrable probability, or general classical sampling.

For fixed min(M,N-M), exact sector propagation is polynomial in N. For
extensive M it costs binomial(N,M) storage in its literal implementation;
that is not a lower bound. Sparse tensor/determinant/Bethe shortcuts must
pay full conditioned-prefix probabilities and numerical conditioning.
Passing these two scoped falsifiers does NOT create an advantage claim.

## Single next hard question

Can Yang-Baxter/unitarity eliminate the doubled scattering network into a
POSITIVE polynomial-size classical state that is closed under observing
one more output spin? An explicit recurrence for arbitrary native b and
every positive-probability prefix would give an end-to-end classical sampler.
Approximation may use an epsilon-budgeted bounded sampler, but cannot assume
relative estimates of exponentially rare prefixes or uncharged roots.
This is the only admitted constructive test, before more quantum work.
An unbounded tensor frontier, a signed estimator without a variance bound,
or a determinant valid only for special boundary conditions fails the gate.
If no such operation survives a bounded independent attempt, park this
known quantum endpoint and compare independent directions again.

## Independent scope/bit review and further primary checks

Full138-line independent review parent-read:
audits/reviews/2026-11-14-ballistic-source-baselines.md. Both finite controls
were independently verified by exact hand propagation; all-pure-Slater scope
and the source global phase check. The classical constant-YBE Theorem1 is
only additive single-amplitude estimation; Theorem5 is log-local observables,
so even their own hypotheses would not automatically give ALL prefixes.
The review checked retained F-basis/RG/Sklyanin/tractable-state premises:
none of those inspected statements supplies this arbitrary-b prefix evaluator.
This is a source-scope conclusion, not an absence or hardness theorem.

Useful exact-bit deduction: write each d/c=r/s in lowest terms. Every
amplitude has common denominator D=product_gates(s+i*r), of O(N²*B) bits.
The numerator of each amplitude is a Gaussian integer. Unitarity gives
sum_x|a_x|²=|D|², so each prefix probability has an integer numerator
0<=Z_z<=|D|² over that same denominator. If a polynomial prefix numerator
recurrence exists, conditional coins Z_zb/Z_z have polynomial bit length,
including arbitrarily rare positive prefixes. Capped rational sampling is
then paid. This deduction does not compute Z_z or provide an approximate
rare-prefix oracle.

Two additional actual sources were screened while the constructive call
was running; they were NOT silently included in that request's context.
Maillet--Sanchez de Santos q-alg/9612012 Proposition4.3 and its proof
(LF1657--1709, factorizing_f.txt) give F-conjugation of a 2^n-dimensional
scalar-product generating matrix to a product diagonal matrix. Reading
that operator identity as a polynomial scalar contraction would be an
unpaid step; the source proof itself is triangularity, not a bit algorithm.
De Gier--Kenyon--Wheeler--Zhou2606.22004v2, actual Eq2.3 and Thm2.1
(LF125--204, five_vertex.txt), gives a determinant for a FIVE-vertex
rectangular partition function with empty side boundaries and w2=0.
Its displayed local L has rank<=3, whereas our R(d) is invertible rank4.
Thus simple invertible vertex gauges/rescaling cannot identify the models.
A more elaborate reduction of the doubled Born network is unproved, not
excluded. The new determinant theorem is not imported by title/abstract.

Paid constructive-prefix request: session13630, Opus/high48k, local ceiling
1.3USD (not a charge or provider cap), exact packet/provenance in
api_inputs/2026-11-14-ballistic-prefix/. Terminal disposition below; no retry.
OpenAI remains disabled.

## Partial constructive result: exact k-prefix channel (parent proof)

For k selected LOWEST rapidities, reverse those k lines internally first.
Their block state is rho=U_B|b_B><b_B|U_B*. In increasing spatial order its
rapidities are a_l=v_(N-l), l=1,...,k. For j=N-k-1 down to0, prepend the
fresh basis state |b_j> on the left, move its rapidity v_j across every block
line in order with R(v_j-a_l), then trace out that environment qubit on the
right. Let this completely positive trace-preserving update be Phi_(j,k).
After all updates,
 p(x_0,...,x_(k-1))=<x|Phi_(0,k)...Phi_(N-k-1,k)(rho)|x>.

Proof: append all environment-environment crossings at the very end. The
constructed crossing schedule is a reduced full-reversal word: every pair
crosses once and final rapidities are sorted. Thus parameter-dependent YBE
identifies it with the native U. The final environment-only unitary cancels
under partial trace. Each processed environment qubit never interacts with
the block again, so tracing it immediately gives the channel above.
The full206-line independent review, including its complete channel proof,
was parent-read and checked. This is a written classical upper bound.

The block density matrix has4^k entries. Sparse local R updates yield
O((N*k+k²)*4^k) exact rational arithmetic operations, with polynomial input
bit lengths by the common-denominator argument. Consequently O(log N)-bit
prefixes are classically computable/sampleable in polynomial time. This is
an UPPER bound; no exponential rank or lower bound is inferred.
For k=1 the block state stays diagonal. Initialize p=b_(N-1), and for
j=N-2 down to0 apply
 p <- [d_j²*p+c²*b_j]/[c²+d_j²], d_j=v_j-v_(N-1).
This is an exact classical first-output-bit law. Conditioned remaining spins
are generally coherent; resetting them to a product/diagonal state does not
produce the full Born law. The N3 control already exhibits this interference.

## Terminal paid attempt and disposition

The NEW constructive-prefix request ended truncated/max_tokens with4885bytes
of final text, all parent-read; session13630 reaped exit1. Estimate1.006308USD
(input11577/output48000), not invoice/balance. No retry or paidOpenAI.
It gives an exact but exponential full-state recurrence and starts the
positive k-prefix channel above; its proof is cut off midway. Parent
completed the proof directly, not from the report's verdict. The two hand
checks agree with our exact controls. Its lazy Bernoulli bit comparison is
EXPECTED time, so its 'TV0/polynomial clock' wording is not a fixed-clock
claim: use capped exact rational sampling and charge epsilon for the tail.
The report supplies no polynomial-size arbitrary-prefix state and no full
sampler. This failure is not hardness or a no-go. A blanket stronger
coefficient-square/logconcavity closure is separately tested below, not
assumed from positivity of the density matrix.

## Final scoped result and stop rule

The SAME N4 exact law also fails Lorentzian/strong log-concavity. Its
quadratic Hessian H_ij=p_ij, diagonal0, has
 detH=(b²-(a+c)²)(b²-(a-c)²)=10773/9765625>0,
where a=48/500,b=117/500,c=45/500. Trace0 and the positive all-ones Rayleigh
quotient force inertia(2,2). This is an exact native obstruction to directly
applying those log-concavity sampling theorems, not a mixing lower bound.
No new finite test was needed. Independent section5 verifies the deduction.

Established: source-correct native circuit convention; local-coin and
all-pure-Slater falsifiers; native non-log-concavity; classical exact first-
bit and O(log N)-prefix simulation with full rational/error clock.
Unestablished: a polynomial full extensive-output classical sampler, any
quantum advantage/hardness, a new quantum algorithm, or finite wave-packet
physics. The positive density-channel representation grows as4^k; no new
closed polynomial state survived the bounded constructive attempt.
Decision: PARK the line. Reopen only with an explicit new arbitrary-prefix
compression, verified direct all-input classical source, or a concrete NEW
native application reduction. Do not repeat the failed broad recurrence
request, enlarge an empty budget, scan bigger systems, or build quantum
infrastructure. The next research action is an independent direction
comparison selected by external value, with corpus then primary sources.

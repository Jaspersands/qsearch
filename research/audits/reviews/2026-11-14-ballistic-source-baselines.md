# Ballistic two-color reversal: independent source and baseline audit

2026-11-14. Read current STATE/TRAPS, the topic, both retained primary texts,
the terminal control script/result, and the relevant retained Bethe formulas.
No control was rerun; no network/API/Git or shared-note edit. Source locators
below are physical LF. This review admits no full classical sampler or hardness.

## 1. Convention and native circuit

Write P for the swap on the two POSITION wires at a crossing and d>0 for
their current rapidity difference. The native gate is

 R(d)=(cI+idP)/(c+id)=exp(-i theta) exp(i theta P), theta=atan(d/c).

Its symmetric/antisymmetric eigenvalues are 1 and (c-id)/(c+id), so it is
unitary. The source's AppendixA gate is S(d)=(-icI+dP)/(ic+d), and EXACTLY

 S(d)=[(d-ic)/(d+ic)] R(d).                                (1)

The bracket is one scalar phase, including on equal-color basis states.
Thus this is not an unnoticed extra swap or a change of Born probabilities.
Aaronson--Bouland--Kuperberg--Mehraban, `ball_permutations.txt`,
LF1054--1107 derives S and its parameter-dependent braid equation.

Momentum labels move through crossings deterministically, separately from
the quantum colors. Swap the two stored rapidities after each gate. Starting
in decreasing order, bubbling the largest remaining rapidity to the right
and repeating crosses every unordered pair exactly once and ends in increasing
order. In particular N4 gives (j,d)=(0,1),(1,2),(2,3),(0,1),(1,2),(0,1).
Holding d fixed by wire position after a crossing would define another model.

The relation R12(u)R23(u+v)R12(v)=R23(v)R12(u+v)R23(u) follows by expanding
in P12,P23, using P_i^2=I and their braid relation. Together with disjoint
commutation it gives equality for reduced full-reversal words. The phases
in (1) multiply to the same product over unordered rapidity pairs.
The source prose at LF253 has a self-referential rapidity typo; AppendixA
LF1107 states the correct u,u+v,v relation used here.

## 2. Exact controls independently verified algebraically

For N3,c=1,v=(2,1,0), initial occupied site1, direct multiplication gives
the three amplitudes on sites0,1,2 proportional to

 (-2+2i,-2i,-2+2i), denominator D3=(1+i)^2(1+2i), |D3|^2=20.

Hence the law is (2/5,1/5,2/5). Replacing the successive gates by swap coins
with probabilities 1/2,4/5,1/2 gives (3/10,3/10,2/5); TV=1/10.
This refutes that dephased local-coin operation. This one-particle sector
itself has a polynomial classical propagator.

For N4,c=1,v=(3,2,1,0), initial occupied pair02, the six numerator amplitudes
in order01,02,03,12,13,23 are

 (-8i,10-24i,12+6i,12+6i,-18,24),
 D4=(1+i)^3(1+2i)^2(1+3i), |D4|^2=2000.

This yields exactly (4/125,169/500,9/100,9/100,81/500,36/125).
The stored one-particle determinant law is also consistent: its columns0,2,
before division by D4, are respectively
 (-2-14i,6-18i,24-12i,12+24i), (24-12i,-12+16i,22-6i,6-18i).
Their six squared minors give the stored DPP probabilities; subtracting the
native probabilities gives TV48/125. No numerical fitting is involved.

More strongly, any pure two-fermion Slater state has decomposable amplitudes
A_ij satisfying A01 A23-A02 A13+A03 A12=0. Their magnitudes must therefore
form a triangle. The required magnitudes here are

 sqrt(p01 p23)=12/125, sqrt(p02 p13)=117/500,
 sqrt(p03 p12)=9/100;   117/500-12/125-9/100=6/125>0.

Thus NO choice of complex pure Slater orbital matrix has this Born law.
Changing orbital/site phases cannot repair the magnitude inequality.
This does not exclude Slater mixtures, fixed-size nonprojection DPPs,
postselected Gaussian states, integrable formulas, or general sampling.

## 3. Published scope: neither a hardness transfer nor a sampler import

`ball_permutations.txt` Definition3.5, Theorem3.10 and Corollary3.11
LF657--695 use distinguishable labels, special/arbitrary initial states,
intermediate demolition measurements, and multiplicative error. Our two-color
product input with no intermediate measurements is a restricted representation
and access model; the hardness construction is not a reduction to it.
AppendixP LF2948--2956 expressly leaves measurement removal and DQC1 sampling
open in that paper. Theorem3.3 LF340--366 concerns additive single amplitudes
in the regular permutation representation, not full two-color Born sampling.
None of these statements determines what subsequent literature may prove.

Alagic--Bapat--Jordan, `yang_baxter_classical.txt`, Eq1 LF25--31 uses the
CONSTANT braid equation. For a=c/(c+id), b=id/(c+id), direct expansion gives

 (aI+bP12)(aI+bP23)(aI+bP12) - (aI+bP23)(aI+bP12)(aI+bP23)
 =a^2 b(P12-P23),

nonzero for the native c,d>0. Also P commutes with every invertible Q tensor Q,
so joint basis conjugation cannot turn the generic R(d) into the monomial
gate of Theorem1 LF283--291. Its other constant-YBE family is Clifford-based.
There is a further output guard: Theorem1 estimates single amplitudes
additively; Theorem5 LF685--687 computes O(log N)-local observables. Neither
statement by itself is a full arbitrary-prefix sampler, even for its own gates.

## 4. Retained determinant and prefix formulas

The source comparison is concrete, not an assertion that no formula exists:

- SciPost18,187, `bethe_prefix_admission/f_basis.txt`, Eq26 LF458--482
  does factor permutation R-operators as F_sigma^-1 F. This is an operator
  identity on an exponential space, not a Born-prefix contraction rule.
  Eq39 LF634--675 builds B(u1)...B(uM)|0...0> with uniform auxiliary boundary
  states, and its explicit MPS has bond dimension2^M. No identification of
  our arbitrary input b with that boundary problem is supplied. The later
  Gram determinants have binomial-size matrices (Table2/LF1338--1367);
  their displayed construction is not a polynomial extensive-M compiler.
- Claeys et al., `bethe_prefix_admission/gaudin.txt`, Eqs58--61 LF714--745
  give a determinant for a SPECIFIED Richardson--Gaudin Bethe state against
  an occupation basis vector. The dual/eigenstate normalization LF747--802
  uses that state's rapidity/eigenvalue data. It is not an identity for the
  arbitrary full-reversal output or its conditioned-prefix sums.
- Sklyanin, `bethe_prefix_admission/correlators.txt`, Theorem2 LF272--287
  assumes the Bethe equations for its norm determinant. Its general overlap
  LF368--385 is a sum over set partitions, not a proved polynomial prefix
  algorithm for the present scattering state.
- Van den Nest, `bethe_transform_selection/tractable_states.txt`, Lemma1
  LF379--386 converts efficiently COMPUTABLE marginals into sampling;
  Definition1 LF344--349 requires sampling separately from amplitude access.
  It supplies a valid reduction, not the missing native prefix evaluator.

One useful bit guard is elementary: after clearing each rational d/c, every
gate has denominator s+ir and Gaussian-integer numerator sI+irP. All output
amplitudes share D=product(s+ir), of O(N^2 B) bits. Any prefix probability
has integer numerator over |D|^2, between0 and|D|^2. Exact conditional coins
would therefore have polynomial bit cost IF those numerators were computed
in polynomial time. This does not supply their computation or a variance bound.

Disposition: the convention and both scoped falsifiers are sound. None of
the inspected determinant/prefix statements currently establishes the native
extensive-input sampler. That sampler remains UNKNOWN, not hard or absent.
An explicit positive prefix state closed under the next observation remains
the precise constructive obligation; no full-algorithm status is promoted.

## 5. Same-control log-concavity consequence

Let H_ij=p_ij for i!=j and H_ii=0, the Hessian of sum_(i<j)p_ij z_i z_j.
Set a=48/500,b=117/500,c=45/500, the three square-root products above.
Then det H=(b^2-(a+c)^2)(b^2-(a-c)^2)
=(63/3125)(171/3125)=10773/9765625>0. H has trace0 and a positive
Rayleigh quotient on the all-ones vector, so its inertia is (2,2).
Thus this NATIVE Born quadratic is not Lorentzian or strongly log-concave.
This rejects those hypotheses as a black-box sampler input, not mixing or
general sampling; no new finite control was run.

## 6. Exact small-prefix channel: completed proof of the useful paid fragment

The terminal `claude_runs/2026-11-14-ballistic-prefix/response.md` was read
fully. It truncates inside its R2 proof and is not a completed review. The
following argument independently completes that statement, without importing
its optional MPS side claim or its expected-only rational-coin clock.

Fix k and let B be the lowest k rapidities. Reverse their last-k input block
internally, obtaining the order a_l=v_(N-l), l=1,...,k. Initialize rho_B as
that k-qubit output density. For j=N-k-1,N-k-2,...,0, apply the channel

 rho_B <- Tr_last [ V_j (|b_j><b_j| tensor rho_B) V_j^dagger ],
 V_j=R_(k-1,k)(v_j-a_k) ... R_(0,1)(v_j-a_1).               (2)

The rightmost factor acts first. The last output position is the discarded
environment line; the first k positions remain B in its increasing order.

To prove (2), complete this schedule by reversing the remaining environment
lines AFTER all the displayed crossings. Initially they are in decreasing
order. Each B--B, B--environment, and environment--environment pair now crosses
exactly once, always by adjacent swaps. The total is N(N-1)/2 crossings and
the final rapidities increase. This is a reduced reversal word, so the
parameter-dependent braid relation identifies it with the native circuit.
The final environment unitary cancels in the partial trace. Once it is
dropped, each processed environment line is never touched again; its trace
may be taken immediately even when it is entangled with B. Each unprocessed
line is still its fresh product-state input. This proves the exact channel
and the exact first-k-output marginal for every native input bitstring.

Local updates on a dense k-qubit density matrix cost O(4^k) rational
operations per gate. Preparation plus all channels therefore costs
O((k^2+Nk)4^k) operations and O(4^k) storage. The common-denominator argument
above applies to the retained crossing subword and its adjoint; partial traces
introduce sums, not new denominators or normalization. Every matrix entry has
polynomial native bit length. Hence k<=C log N, fixed C, gives a polynomial
BIT algorithm for the full first-k joint law and its conditional coins.

For k=1, rho stays diagonal. Start p=b_(N-1); for j=N-2 down to0 use

 p <- (d^2 p+c^2 b_j)/(c^2+d^2),  d=v_j-v_(N-1).           (3)

This first-bit marginal is exactly classical. It does not turn all crossings
into independent coins: the N3 control already refutes that joint-law claim.
Nor does rho_k provide a paid update to rho_(k+1): a line traced out for k
becomes an observed output for k+1, so its lost correlations cannot be reset.

The paid R1 peeling recurrence is also algebraically correct: move the next
smallest line left, project its now-final output bit, and keep the remaining
unnormalized pure vector. Its dimension is binomial(N-k,M-|prefix|), generally
exponential. Lazy exact coins give only an expected clock. Instead round each
exact conditional probability to a b-bit dyadic, b=ceil(log2(2N/epsilon)),
and use exactly b random bits. Sequential coupling bounds total TV by
N*2^-b<=epsilon/2, including arbitrarily small probabilities. Exact rational
arithmetic has already-paid polynomial bit heights; state SIZE remains the
unpaid exponential cost. These repairs establish small-prefix simulation,
not a full extensive-output sampler or a new quantum endpoint.

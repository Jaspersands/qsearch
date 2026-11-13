# Polar DQI: a classical sampler on the same explicit code

2026-11-14. Parent-derived finite-bound construction; independent paid review
completed and parent-checked. Not a new general DQI decoder, arbitrary-code theorem, all-offset
sampler, novelty or quantum advantage claim. Main question: can a polar-code
nonlocal decoder create an unmatched native optimization/sampling endpoint?

## Selection, input and proposed mechanisms

STATE/TRAPS and corpus been-tried/baselines preceded actual primary sources.
The sparse DQI source2611.12718v1 leaves its classical Conj6.7 conditional;
its optimal-decoder theorem does not implement the PGM. A natural weighted
code-check parent was separately matched to heat-bath dynamics (below).
Polar codes are a different constructive global-decoder route, with a
stronger SAME-CODE classical source-encoding baseline to test first.

Input N=2^s, G=[[1,0],[1,1]] tensor^s overF2 in row convention, explicit
F subset{0,...,N-1}, binary rational0<alpha<1/2, and explicit b uniform in
F2^N. Let K={uG:u_F=0}, C=K-perp. Output x in b+K, with target

    pi_b(x)=alpha^|x| (1-alpha)^(N-|x|) / Z_b.

The performance metric is E_b TV(output_b,pi_b). The code and b are the
same native input to both methods. A score-only statement is weaker.
Known DQI would use product amplitudes, uniform C, and a coherent decoder
and its adjoint. Even a hypothetical efficient polar decoder supplies no
advantage here if the classical construction below matches the output law.
An exact coherent Gibbs state is a different task, not claimed classically.

Expected quantum benefit of the candidate was efficient global decoding
beyond local BPQM; the test is a direct constructive classical counterpart,
not an assumption that the quantum decoder is inefficient. Resources are
poly(N,bit(alpha),log(1/eta)); no likelihood oracle, hidden good-set selector,
Gibbs oracle, coherent advice or exponential table is allowed.

Primary sources retained in audits/sources/nov14_decoder_selection/:
Korada--Urbanke0903.0307, actual Lemmas2,5--9; Renes1701.05583,
Section3.2/Corollary2/Theorem2; and actual DQI2611.12718v1 definitions.
No theorem is imported from the withdrawn MQ paper2411.14697.

## Finite SAME-CODE claim and joint-distribution proof

Let P(U,Y)=2^-N W_alpha^N(Y|UG), where W_alpha is the classical BSC.
Thus P_Y is uniform. Write p_i=P(U_i=0|U_<i,Y), and define

    d_F=sum_{i in F} E_P |p_i-1/2|.

Construct Q by Y uniform, fair independent bits at frozen positions F,
and the EXACT P posterior at other positions. Actual Korada Lemma2 gives
TV(P,Q)<=d_F (its displayed L1 bound is2d_F).

For every a inF2^N, the gauge map

    (U,Y) -> (U+a,Y+aG)

preserves P: it preserves Y-UG. The posterior transforms with the same
prefix and output translations, so it also preserves Q, including its fair
frozen coins. Both frozen marginals are uniform. This map bijects every
fixed-frozen sector with every other sector. Hence their conditional joint
TV distances are ALL equal, and averaging gives the exact identity

    TV(P(.|U_F=0),Q(.|U_F=0)) = TV(P,Q) <= d_F.       (1)

No division by2^-|F| occurs. This is stronger than the source's marginal
quantization-error conclusion, and must be checked at the JOINT level.
Under Q conditioned on U_F=0, Y stays uniform: each frozen coin was fair
independently of Y and all previous choices. This conditional Q is exactly
the implemented successive randomized encoder with frozen bits fixed0.

Put P0=P(.|U_F=0). Its Y marginal is generally NOT uniform; it is weighted
by Z_Y. Define R(U,Y)=2^-N P0(U|Y). Then

    TV(P0,R)=TV(P0_Y,uniform)<=d_F,
    TV(Q(.|U_F=0),R)<=2d_F.                           (2)

Under P0(U|Y=b), the deterministic map x=b+UG has law pi_b. Applying
that map to (2) proves the proposed averaged-offset output bound2d_F.
It makes no claim that each individual rare offset has small error.
All Z_b>0 because0<alpha<1/2.

## Polar duality and what it does NOT assume

Let V_i be the BSC synthesized channel in SC order, with Bhattacharyya Z_i.
Its posterior bias obeys

    E|p_i-1/2| <= (1/2)*sqrt(1-Z_i^2).

Let e_j be the Helstrom error for bit j of the synthesized pure-state
channel, with all input bits uniform and the true earlier bits supplied as
classical output registers. For the channel dual to V_i, Renes min/max
duality gives

    e_{J(i)}=(1-Z_i)/2,
    d_F <= sum_{i in F} sqrt(e_{J(i)}(1-e_{J(i)}))
         <= sum_{j in J(F)} sqrt(e_j).                 (3)

The BSC dual is the pure-state channel
z -> sqrt(1-alpha)|0>+(-1)^z sqrt(alpha)|1>, up to a public basis change.
Renes Corollary2 complements every plus/minus polarization index. Also
G^-T=J G J with J complementing the index bits, i->N-1-i (not bit-order
reversal). Thus C is, up
to the public coordinate permutation J, the polar code with information
set J(F). This is the relevant SAME-code relation. The usual output
bit-reversal convention is a public coordinate permutation for a memoryless
channel; it is not a change of supplied code to a separately chosen code.

These statements refer to explicit per-synthesized-bit quality criteria.
In particular all future bits, including future frozen bits, are uniform
in these auxiliary channels. They are not the actual fixed-frozen block
decoding problem. For N=2, F={1}, C={00,01} and alpha=1/10, the actual
code Helstrom error is1/5 while e_0=8/25. This elementary calculation uses
the single-state overlap1-2alpha and the two-copy check-channel difference;
it refutes identifying these errors, not every possible inequality.
They do NOT say that arbitrary PGM block success, any polar information
set, or every nonlocal quantum decoder forces (3) to be small. The code
input already supplies F; the sampler itself never computes Z_i or e_i.
Public asymptotically good-code construction and its finite threshold must
be sourced separately before claiming a uniform constructor. No good-set
oracle is inserted. Korada's source-coding family is the known baseline.

## Bit clock and falsifiers

The classical output algorithm sets Y=b, runs SC randomized rounding with
u_F=0, and returns b+uG. SC likelihood updates and encoding cost O(NlogN)
arithmetic operations. For alpha=a/d in binary, exact likelihood numerators
and denominators have O(N(logd+1)) bits: they represent sums of products of
at most N channel factors, not arbitrary repeated circuit squaring.
Classical source arithmetic must retain this common-denominator bound.
For a deterministic cap, replace each exact coin probability L0/(L0+L1)
by floor(2^t L0/(L0+L1))/2^t, using t=ceil(log2(N/eta)) random bits per
coin. Each history-dependent conditional law changes by at most2^-t;
a hybrid coupling charges at mosteta overN steps. Total work/space are
polynomial in native bits and log(1/eta). This works for arbitrary rational
alpha=a/d: the starting integer likelihood pair is(d-a,a). The paid report's
dyadic-only notation is unnecessarily restrictive. No float precision or
conditioning-on-success assumption is used. The earlier capped-rejection
alternative also works by coupling, but is not needed.

Decisive falsifiers: a gauge failure for fixed frozen bits; incorrectly
equating marginal noise TV with conditional coset TV; missing weighted-Y
normalization; a transpose/index mismatch; exponentially large exact
likelihood representations; or silently promoting average-offset error to
worst-offset error. Passing finite examples cannot establish the theorem.

## Adjacent screened route: the filtered-check parent

The independent149-line review
audits/reviews/2026-11-14-dqi-nonlocal-selection.md was parent-read. For
explicit binary moves v_i spanning K and w(x)=exp(-beta|x|), the pair block

    h_i = [[w(y),-sqrt(w(x)w(y))],
           [-sqrt(w(x)w(y)),w(x)]]/(w(x)+w(y)), y=x+v_i

annihilates sqrt(w). On a coset, H=sumh_i is EXACTLY S(-L)S^-1 with
S=diag(sqrt(pi)) and heat-bath rate L(x,y)=w(y)/(w(x)+w(y)). For r moves,
the discrete random-move chain has gap gap(H)/r and
log(1/minpi)<=dim(K)log2+beta*N. Thus an inverse-polynomial gap for this
parent also pays a classical TV sampler. Public nonlocal Gaussian-elimination
moves change neither identity nor polynomial cost. Zero moves are discarded.
This scoped match does not refute different nonlocal decoders or prove
Conj6.7. No spectrum sweep is warranted.

## Independent audit and exact control

Claude Opus/high, max48000tokens, local ceiling2USD, process session1300:
audits/api_inputs/2026-11-14-polar-dqi-match/ and matching claude_runs/.
Completed/end_turn, full215LF report parent-read, reapedexit0. Runner estimate
0.724264USD (18541input/32505output), not an invoice or balance. The
fixed-frozen joint law and the weighted-offset correction were reproved.
The J(i) index correction is accepted; the original notation called W_i
the dual of V_i but did not identify its actual decoder index. The distinction
between synthesized-channel and fixed-code errors is accepted. The dyadic
restriction is repaired above. O3 is independently checked against actual
DQI2611.12718v1 Theorem3.3 and its proof at textLF1119--1172: the target uses
|Phi(x)|^2 restricted to the SAME coset. Its uniform-offset TV guarantee is
sqrt(blockerror), with successful-check retries charged. That does not imply
small d_F. O1/O2 are CLOSED by the full155LF independent review
audits/reviews/2026-11-14-polar-conventions.md, parent-read against the
actual source formulas. The induction splits u=(a,b): first-half decoding
uses W-minus after summing bG; second-half decoding retains the reversible
prefix aG and uses W-plus. Thus every binary index choice is complemented
by Renes duality for allN, not by extrapolation fromN=2. Optimizing the
classical fidelity gives Q(V_i)=(1+Z_i)/2 with all prefix registers retained.
The same-code corollary is therefore a reviewed WRITTEN classical match
under the stated small-sum-sqrt(e_j) certificate. It is not a match under
arbitrary small block-decoder error alone.

Single exact Sage convention control, audits/controls/polar_same_code/,
terminalexit0: N=4, alpha=1/4, F={0,2}. d_F=5/32;
TV(P,Q)=TV(P0,Q0)=315/2176 for each of the four frozen sectors;
actual averaged cosetTV=2/25<=2d_F=5/16. Individual coset errors differ.
Also G^-T=JGJ and the four-state/three-move heatbath similarity are exact.
These controls falsify convention errors only; the symbolic proofs, not
the finite results or an ACCEPT label, support the stated bounds.
OpenAI disabled. No quantum code or broader finite sweep is queued.

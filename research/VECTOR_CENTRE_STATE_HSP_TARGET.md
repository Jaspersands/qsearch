# Vector-Centre StateHSP Without Sector Collisions

LOCAL DERIVATION / IMPLEMENTED SPECIFICATION / REVIEW PENDING. No new candidate,
novelty, general nilpotent solver, cryptographic attack or Shor-level result.
This extends `CYCLIC_CENTRE_STATE_HSP_RECEIVER.md`. Implemented control flow
and finite literal instruments do not replace external mathematical review
or a scalable hardware backend.

## Source And Proposed Escape

Use a PUBLIC bilinear extension G=F3^d x F3^k with vector cocycle B:

    (x,z)*(y,w)=(x+y,z+w+B(x,y)).

Given IID copies of ONE unknown rho, known controlled R, original Bose
gap epsilon>0 and efficient supplied coordinates/B. Let S be its Bose
subgroup and Z0=S intersect Z. The cyclic-centre pass cannot simply bucket
3^k characters: an observed character can have exponentially small weight.
Do NOT pay for identical characters. Use disjoint blocks of DIFFERENT
measured central characters whose VECTOR SUM is zero.

The repo's existing F3 `zero_sum_support` in `ternary_cyclic_extractor.py`
finds a nonempty such subset among W=(k+1)^2 labels with at most k+2 field
kernel calls. This is KNOWN zero-sum mathematics, not a novelty claim.
Iterating must cover ALL BUT <W source indices, with each support size<=W.
Use a streaming W-register buffer and refill unused slots; do not call the
existing quadratic-in-pool-size list-filtering recycler on a giant pool.
Every supplied register is used at most once, or explicitly left/discarded.
Labels choose the supports; internal Fourier outcomes must NOT feed back
into this selection. Do not assert IID retained label values after selection.

## Exact Mixed-Sector Linearisation

On central sector lambda_i, U_i(x)=R(x,0) has cocycle
omega^(lambda_i dot B(x,y)). For a zero-sum block I, apply the known action

    A_I(x)=tensor_(i in I) U_i(x)

to the actual supplied conditional states rho_(lambda_i). Because sum lambda_i=0,
this is a genuine LINEAR action of F3^d on the prepared tensor sector. It is
not a homomorphism on arbitrary unprepared workspace. It consumes exactly
|I| copies and known controlled R calls. No identical states, inverse,
cloning, signed extra copies or hidden phase oracle is needed.

For x in pi(S), choose (x,z) in S. Each sector expectation equals
omega^(-lambda_i dot z); their product is EXACTLY1. ONE ordinary Fourier
sampling experiment per block yields a character annihilating pi(S).
Consequently T=intersection of ALL sampled character kernels contains
pi(S) with certainty. Its computation is field nullspace, not secret search.

## Why Coverage, Not A Conditional Gap, Is Enough

Write phi_i(x)=Tr(U_i(x)rho_(lambda_i)) and delta=1/16. For a pair x,y,
its central commutator is c=B(x,y)-B(y,x). If lambda_i dot c!=0, the cyclic
pass's purified approximate-eigenvector argument implies

    |phi_i(x)|<=1-delta OR |phi_i(y)|<=1-delta.

Otherwise the commutator's squared norm would be <32*delta=2, whereas
a nonzero ternary central phase has squared norm EXACTLY3. This sharper
constant uses characteristic3 specifically; it is not a general-prime claim.
For a purification psi and phase alpha=phi/|phi|,
||(U-alpha)psi||^2=2*(1-|phi|). Triangle inequality bounds
||(UV-VU)psi|| by twice the sum of the two individual defects. Squaring
gives <32*delta, contradicting the exact scalar commutator distance3.

In a block containing such an index, at least one of the two tensor
expectations has modulus<=1-delta. Thus the probability that its Fourier
outcome annihilates BOTH x and y is <=1-delta/2. No minimum conditional gap
and no independence between x and y tests are assumed.

For ANY c outside Z0, the original gap gives

    Pr_lambda[lambda dot c!=0] >=epsilon/2.

Among N original independent central measurements, simultaneous Chernoff
bounds can force at least W+H such indices for EVERY c outside Z0. Discarding
<W leftovers leaves at least H included witnesses. Since supports have
size<=W, at least H/W DISJOINT blocks contain witnesses. Conditional on the
COMPLETE centre-label transcript, their quantum states and measurements
are independent, even though their labels are not IID after selection.

For fixed x,y with c outside Z0, survival in T therefore has probability
<=exp(-delta*H/(2W)). Union over the 3^(2d) ordered pairs, not over a chosen
basis that was itself data-selected. With high probability ALL commutators
of T lie in Z0. There is no global matrix commutativity-repair primitive.

## Recover Z0 And Compile The Final Quotient

Use ALL measured central characters, including leftovers, to compute
their common kernel. Under the same simultaneous count event it equals
Z0 EXACTLY; no extra quantum inputs are needed. Compute T from the block
records. Check B(x,y)-B(y,x) lies in the learned Z0 on all basis pairs of T.
If not, return FAILURE rather than quotienting by an unknown subgroup.

L=pi^(-1)(T) may still be NONABELIAN as a group. But L/Z0 is abelian, and
original rho is supported on the Z0-fixed invariant subspace. Let V be a
basis of T and C a public complement to Z0 in F3^k. The chart

    (t,a) -> (V*t, C*a+2*B(V*t,V*t)) mod Z0

is a homomorphism: B becomes symmetric modulo Z0. Its section need not be
a homomorphism on the full workspace. Controlled R implements the quotient
action on the original state's SUPPORT, which is the scope needed for
Fourier sampling. This distinction must survive records and independent
replay. Do not confuse an actual commuting overgroup with this quotient.

Fresh ORIGINAL-state abelian sampling recovers S/Z0; lift its basis together
with Z0 generators. This final step retains central/eigenvalue phases that
pi(S) alone loses. The original epsilon gap survives in L/Z0.

## Conservative Exact Integer Ledger

With failure bits b>=1 and W=(k+1)^2, use

    delta=1/16,
    H=32*W*(4*d+b+2),
    N=ceil((2/epsilon)*(2*(W+H)+8*(2*k+b+2))),
    M=ceil((2/epsilon)*(2*(d+k)+b+2)).

For each c outside Z0, mean count>=N*epsilon/2>=2*(W+H)+8*(2*k+b+2).
Chernoff gives probability of count<W+H <=2^(-2*k-b-2); union over
3^k<=2^(2k) gives <=2^(-b-2). Conditional pair-survival probability is
<=2^(-4*d-b-2); union over3^(2d)<=2^(4d) gives another <=2^(-b-2).
Final subgroup sampling gives <=2^(-b-2). Total ideal failure<=3*2^(-b-2).

Original copies<=N+M; controlled R calls<=2*N+M (one centre call per input,
one tensor call per included input, one per fresh final input). Central QFT
acts on k trits; each block QFT on d trits. Streaming conditional quantum
buffer<=W registers; final stages require fresh originals, not buffer reuse.
Classical finite-field work is polynomial in the explicit ledger and B size.
Do not enumerate the 3^k central labels, 3^d quotient or 3^(d+k) group to
IMPLEMENT the selector/decoder. Such tables are small CALIBRATION only.

## Implementation And Falsifiers

`theorems/vector_centre_state_hsp_receiver.py` implements the streaming
selector, general measurement-only control flow, quotient chart and full
subgroup lift (including fixed central generators). Its backend contract
requires actual supplied registers. Distinct integer indices alone cannot
certify physical IID inputs or the correctness of a measurement backend.

Finite controls implement the actual known sector action

    R_lambda(a,b,z)=omega^(lambda dot z)
                    (X^a Z^(lambda_0*b)) tensor Z^b.

For the nonnormal-line source the conditional vector is
|0> tensor |-lambda dot tau_b>. For the nonabelian-preimage source lambda_0=0
and the first vector is F_(lambda dot tau_a), an X eigenvector. The original
centre distribution is a mixture of a uniform annihilator spectrum with
weight gamma and the zero character with weight1-gamma. Different labels
give different conditional states; zero-sum blocks have the exact recorded
Fourier laws without same-sector supply. The original overlap gap is gamma.

IMPORTANT: the final original-state law is a MIXTURE of two uniform
character-space laws, not a uniform law when gamma<1. The reference driver
executes this mixture. Literal original-state Kraus controls replay ALL
branches independently of that closed-law sampler. A source-specific
alternative reads the known clock basis, and (in the second case) the
known first-register Fourier basis, then solves classical F3 equations.
It uses fresh counterfactual copies, not copies also spent by the collective
receiver. This baseline kills any advantage inference from these fixtures;
it does not classically solve general unknown-state StateHSP.

Required controls:

- Vector-bilinear group and central quotient charts using existing field APIs.
- Streaming disjoint zero-sum partition with complete original-index ledger,
  exact vector sums, bounded support sizes and <W leftovers.
- Actual distinct-sector Fourier instruments: common R(x,0) acting on each
  supplied register, full probability/retained-phase checks at small size.
- Receiver control flow reconstructing Z0, T, final quotient and full S.
- Literal negative controls: cocycle sums nonzero, conditional copies reused,
  meaningful labels left uncovered, wrong quotient gauge, phase-losing output,
  and sampling/selection using internal outcomes.
- Growing integer resource artifacts without population/character enumeration.
- Independent field/cyclotomic replay and focused mathematical tests.

Test a source with LARGE uniform vector-centre spectrum and almost no repeated
labels; require successful heterogeneous blocks without inventing a chosen
same-sector supply. Also test highly skewed label distributions, rank-deficient
central spectra, conditional near-symmetries, nonnormal S and nonzero Z0.
The ordinary nil-2 HSP baseline is already polynomial; this is not a new
classical problem separation. External theorem/priority review is required.
Relevant primary sources: [Holt--Subramanian, Problem6.41 and Section9.3.2](https://arxiv.org/html/2609.38085v1),
[Ivanyos--Santha, diagonal systems, Proposition9](https://arxiv.org/pdf/1503.09016),
and [Ivanyos--Sanselme--Santha, nil-2 HSP](https://arxiv.org/abs/0707.1260).
The mixed-sector coverage and robust overgroup arguments here are LOCAL
derivations, not attributed theorems from these papers.

The proof would fail if recycling leaves an unbounded discarded tail; if a
block has size>W; if source copies are correlated after conditioning; if
selection reads internal measurements; if the original norm gap is replaced
by a weaker unsupported average promise; or if a quotient section is treated
as linear outside its invariant source subspace. Approximate source/action
error is still separate. Higher nilpotency, characteristic2, higher roots,
native DCP/CCP state conversion and a general central-extension solution
remain OPEN. Merely increasing calibration dimensions does not supply them.

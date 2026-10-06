# Singer Membership: Known-Solver Query Closure

**LOCAL DERIVATION / REVIEW PENDING.** Not a new algorithm, accepted candidate,
independently reviewed theorem, classical dequantization or generic DHSP bound.
This is a follow-up to [the residual-hardness audit](SINGER_RESIDUAL_HARDNESS.md).
Its purpose is to close a misleading search direction with a paid known-solver
upper route, not to introduce another artificial oracle problem.

## Research Decision

For this specific public-field Singer source, there is a Shor-assisted route
with O(sqrt(q)) charged membership queries and polynomial work per query.
The preceding sparse membership bound requires Omega(sqrt(q)) queries for
constant mean recovery as q grows. Thus the query order is closed up to constants
for this source, conditional on standard known quantum arithmetic and the
supplied public field representation. An unrestricted growing-q source still
requires exponential time in log(q). For fixed q it is already addressed by
known arithmetic, not a new Shor-level mechanism.

Stop using whole-shift brute force, rare positive samples or a missing Fourier
phase compiler as evidence that this family conceals a new algorithm. There is
an alternative route that needs neither a table of unknown membership values
nor a generalized Gauss-sum phase compiler. It does, however, use a known
quantum discrete-log solver. This dependence must never disappear from costs.

[Shor's discrete-log algorithm](https://arxiv.org/abs/quant-ph/9508027) is the
known arithmetic ingredient. [Roetteler's difference-set framework](https://arxiv.org/abs/1608.02005)
is the existing Singer lead. The composition and bounds below are local
derivations, not claims of novelty or statements attributed to those papers.
No priority search, independent human review or actual coherent Shor compiler
has been completed.

## Exact Interface

Public E=F_(q^m), q a prime power, m>=2, primitive alpha, polynomial field
arithmetic, a public embedding of F_q, and trace pairing. The only secret
input is the coherent XOR bit oracle

`O_s: |k,b> -> |k,b XOR [Tr_(E/F_q)(alpha^(k+s))=0]>`,

where k is canonical in Z_v, v=(q^m-1)/(q-1). beta=alpha^s is NOT supplied.
The trace source convention is D_s(k)=D(k+s); our output is its multiplicative
exponent s, not the set-translation -s. Field/primitive setup is supplied by
the promise, not certified efficient classical preprocessing by the controls.

Known DLog calls below take public alpha and arbitrary field coordinate x,
not an unknown hiding-function output. They are not a free inverse to O_s.
There is no second unknown oracle, secret-correlated initial memory, supplied
normal, secret-dependent driver, free coset projector or hidden-state cloning.

## Paid Coordinate Conversion

For x!=0, compute L(x)=log_alpha(x) coherently, reduce k=L(x) mod v, query O_s,
then uncompute both k and L. Since alpha^v is a base-field scalar, the result
is the zero predicate Tr(beta*x)=0. The logarithm is known quantum arithmetic
on an explicit public field; its polynomial bit cost is charged.

At x=0 define the predicate to be one. There is no log(0). A clean phase marker
still uses ONE unknown XOR invocation: prepare its target in |+> at x=0 and
|-> otherwise. The former is insensitive to the dummy query argument k=0;
the latter acquires the membership phase. Undo the target preparation and
apply a known minus sign at x=0. This yields the unitary

`M_beta |x> = (-1)^[Tr(beta*x)=0] |x>`

with all logarithm/target workspace cleaned. This construction uses the XOR
structure of the declared oracle, not free control of an arbitrary black-box
unitary. The zero branch and dummy query are executed in the calibration.

Exponentiation alone does NOT give a clean inverse coordinate map: computing
alpha^k while retaining k leaves an entangled record. The known logarithm and
uncomputation are substantive resource dependencies, not optional cleanup.

## Full-State Readout, No Positive-Sample Postselection

Let H_beta={x:Tr(beta*x)=0}, so |H_beta|=q^(m-1), density 1/q including zero.
Prepare uniform |u> on all E. Put theta=asin(1/sqrt(q)). A Grover step is the
known diffusion R_u=2|u><u|-I after M_beta. After j steps,

`|psi_j> = sin((2j+1)theta)|H_beta> + cos((2j+1)theta)|E \ H_beta>`.

The states on the right are individually normalized, but no measurement or
renormalization has discarded either branch. The additive Fourier transform
is implemented in known field-coordinate registers. In a polynomial basis
e_i, define the public trace-pairing matrix T_ij=Tr(e_i*e_j). For prime q the
Fourier coordinate of a normal z is y=T*z, NOT generally the coordinates of z.

Fourier(|H_beta>) is uniform on the q-element annihilator line. At zero its
amplitude is 1/sqrt(q); at each nonzero coordinate it is also 1/sqrt(q).
Fourier(|E \ H_beta>) has zero amplitude sqrt((q-1)/q) and each nonzero-line
amplitude -1/sqrt(q*(q-1)). All other coordinates have zero amplitude.
Consequently the COMPLETE output law is

`Pr[y=0] = cos^2(2j*theta)`,
`Pr[y=a*T*beta] = sin^2(2j*theta)/(q-1)`, each a in F_q*,
`Pr[all other y] = 0`.

Each nonzero y gives z=T^-1*y=a*beta. Compute

`gamma=alpha^(q-1), w=z^(q-1)=gamma^s`.

One known quantum subgroup discrete logarithm recovers the canonical s.
The zero output is an explicit failed attempt, not a successful sample with
an unspecified selection cost. There is no extra unknown oracle verification
in the ideal promised problem; compiler/residual-solver failure remains paid.

For q=2, one step has success ONE: this is the usual linear-phase Fourier
readout after paid coordinate conversion. It does not solve DLog classically.
For q>2, one step has success 4(q-1)/q^2, which is small for large q. Amplification
improves this to constant success using sqrt(q) queries, not polylog(q) queries.

For q=p^b, use the additive QFT over F_p^(bm), with absolute trace pairing.
The annihilator is the F_q normal line because the trace is transitive and
the base-field trace pairing is nondegenerate. This requires a supplied usable
subfield embedding. Literal implemented statevector controls use prime q only;
large prime-power records are parameter ledgers, not embedding/QFT simulations.

## Exact Randomized Schedule And Matching Cost

Avoid assuming exponentially accurate special-angle rotations or rounding a
huge floating-point j. Choose j uniformly from {0,...,J-1}, where

`J=ceil(q/sqrt(q-1))`.

Let P_j=sin^2(2j*theta). Then

`mean(P_j)=1/2 - Re(sum_(j=0)^(J-1) exp(4ijtheta))/(2J)`.

The geometric sum has modulus at most 1/sin(2theta), while
sin(2theta)=2sqrt(q-1)/q. Hence J*sin(2theta)>=2 and mean(P_j)>=1/4.
Each attempt costs at most J-1 membership calls, expected (J-1)/2.
Independent repetitions have all-zero-output probability at most (3/4)^R.
For R=16 this is about .01002. This is a success bound, not a large-field
runtime measurement. Random integer selection is public and independent of s.

The ledger computes J with integer arithmetic and certifies BOTH
J^2(q-1)>=q^2 and (J-1)^2(q-1)<q^2. Every large count is a decimal string.
For q=2^128,m=3,R=16 the maximum membership cost exceeds 2^64, despite
polynomial bit cost per known arithmetic operation. This is not efficient in
the original input length. It is the expected sqrt(q) access obstruction.

The prior lower bound with v=(q^m-1)/(q-1), k=(q^(m-1)-1)/(q-1) implies

`T >= (sqrt(c)-1/sqrt(v))/(2sqrt(k/v))`

whenever mean exact-shift success is at least c. For fixed c>0 and growing q
this is Omega(sqrt(q)). The upper uses the SAME only-secret XOR membership
model, with public known quantum processing. Thus there is no query-order
gap to close here. Neither result is a computational lower bound for an
unrelated full-function DHSP interface or a white-box beta input.

## Coherent Arithmetic Is Not A Measured Subroutine

A measured DLog answer on a superposition cannot be fed back without decohering
the source. A bounded-error known algorithm must be boosted uniformly over ALL
coordinate inputs, used with compute/copy/uncompute, and keep the input register
unchanged. If its worst-case output error is e, the clean function map differs
from its ideal map by norm at most 2sqrt(e) on initialized workspace. Two such
maps per membership phase give at most 4sqrt(e). A reference-prefix unitary
hybrid for Q phase calls gives norm, hence final measurement TV, <=4Qsqrt(e).

To budget process TV <=delta, require e<=(delta/(4Q))^2. The producer records
this EXACT rational requirement with delta=1/1000. Boosting costs polynomial
log(1/e); it cannot remove the Q membership calls. There are 2Q clean known-log
maps, each internally invoking the underlying boosted algorithm and inverse,
hence 4Q underlying computation/inverse invocations. Residual-solver output
error, QFT/rotation error and physical compilation error are ADDITIONAL budgets.
No unimplemented compiler precision is certified by ideal statevector tests.

## Adversarial Checks And Remaining Failure Modes

1. **Could this be a new arithmetic speedup?** No: coordinate cleanup explicitly
   requires known Shor arithmetic. Removing it is an unproved replacement
   algorithm, not a free implementation choice. A non-Shor replacement with a
   natural useful reduction would be a different proposal requiring its own audit.
2. **Can uncomputation be dropped?** No for this construction. The calibration
   log label is injective, including a zero sentinel. Tracing it out leaves
   a diagonal field-coordinate density matrix. Additive Fourier measurement
   becomes uniform; correct normal probability falls to (q-1)/q^m. A literal
   reduced-density countercontrol executes this partial trace.
3. **Could a generic coset-state solver use this coordinate change?** Not without
   a reduction supplying this public trace/field promise. Random hiding labels
   have no such known logarithmic coordinate map. No theorem is transferred.
4. **Do classical positive-sample costs establish novelty?** No. The previous
   audit separates known quantum residuals from complete classical dequantization.
   The strongest known classical residual comparator still applies after normal
   extraction; the new route establishes a known quantum benchmark, not hardness.
5. **Is every q represented in actual controls?** No. Prime-power subfield
   embeddings and a uniform coherent Shor circuit are proof/implementation debt.
   Their absence prevents a completed compiler claim, not permission to ignore
   the already-known solver route when evaluating novelty.
6. **Does the numerical Fourier state prove an asymptotic theorem?** No.
   Orthogonality of characters and the two-dimensional Grover recurrence prove
   the ideal formulas locally; bounded independent replays detect implementation
   errors. Human review remains outstanding. An off-line Fourier outcome with
   non-negligible probability under the exact promise, a failed trace-pairing
   decoder, or a charged schedule below 1/4 would falsify this implementation.
7. **Noise or masks?** An arbitrary mask, fresh stochastic bit oracle or a changed
   field representation changes the promise. Do not claim robustness without
   bounding the full coherent channel and natural reduction that supplies it.

## Evidence And Handoff

Twelve unfiltered controls: q,m=(2,3),(3,3),(5,3),(7,2),(11,2),(13,2), two
canonical shifts each. All 38 schedule branches retain all outputs. Small
tables replace known logarithms for calibration ONLY; the hidden beta is used
only by the declared oracle and scoring. Full unknown XOR kickback and target/
log cleanup are executed, not assigned a secret-dependent phase for free.

Independent JavaScript reconstructs field arithmetic, 78 trace-pairing entries,
170 source bits, the known log permutation, dual/residual decoding, all 38
Grover/Fourier branches and 3,558 full output probabilities. Five large ledgers
and their coherent-error requirements replay with BigInt rationals. Independent
language replay is not independent human theorem review.

Files: `theorems/singer_shor_access_closure.py`, focused tests, report under
`research/phase_workbench/`, independent checker under `research/certificates/`,
matching hypothesis contract and literature audit. No production CLI/UI/registry
wiring, full-suite claim, commit or push. Routine integration belongs to Gemini.

Gemini: expose this as a KNOWN-SOLVER/ACCESS-CLOSED benchmark, alongside the
residual-hardness report, not as a candidate. Keep ideal and physical errors,
known quantum arithmetic and growing-q query costs visible. Repair existing
writer omissions and run full production validation separately.

Next mathematical work should LEAVE this family unless a natural reduction
changes an explicit assumption. Seek a consequential action/state-conversion
problem with an implementable public structure and a residual not already
solved by known quantum arithmetic. An abstract promise is not such a reduction.

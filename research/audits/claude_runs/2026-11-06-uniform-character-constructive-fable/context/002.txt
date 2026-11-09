# Actual success boundary of the split-source Hankel receiver

2026-11-05. Closed mathematical question: a sharper analysis of the SAME
2d-1-root coefficient Fourier/Hankel operation cannot give inverse-polynomial
success in growing d. An elementary packing argument proves this already
for every clean irreducible target. No arithmetic-progression splitting
hypothesis, finite scan, general quantum lower bound, novelty, or classical
hardness claim is used.

Read the current `STATE.md` and `TRAPS.md` before this derivation. The
operation is the one specified in `LEGENDRE_HANKEL_RESULTANT_READOUT.md`.
The question was whether its actual Q-specific success could be much larger
than the virtual-overlap factorial lower bound. It can exceed that lower
bound, but cannot become inverse polynomial in d.

## Exact residue-fiber law

Let Q in F_p[X] be monic irreducible of degree d>=2, let m=2d-1, and assume
p>=m so the distinct-root source exists. Let S be the set of squarefree,
completely split polynomials of exact degree m with nonzero leading
coefficient. Write

    N=|S|=(p-1)binom(p,m),
    A=F_p[X]/(Q),
    L:F_p[X]_{<=m}->A,
    K=|ker L|=p^(m+1-d)=p^d,
    C_v=#{R in S:R mod Q=v}.

Here K is a cardinality, not a verification repetition count. Since Q is
irreducible of degree at least two, no R in S is divisible by Q, so C_0=0.
For the normalized CLEAN coefficient state, all amplitudes within a residue
fiber have the same phase: up to the known global resultant sign it is

    psi_R=chi_A(v)/sqrt(N),  v=R mod Q.

Let H=(ker L)^perp in coefficient Fourier space. Projection onto H is
averaging over the K-element residue fibers in the original coefficient
basis. Consequently the exact conditional Fourier probability is

    Pr(H)=sum_v C_v^2/(N K).                                      (1)

For irreducible Q, the Q-specific correct Hankel-decoder event is EXACTLY
D_Q=H\{0}, not merely a superset containing the virtual support. To check
the converse direction, the first d entries of any y determine a unique
t in A by nondegeneracy of the trace pairing. If the Hankel solve returns
Q, its d equations impose the recurrence of Q on y_d,...,y_(2d-1).
Induction therefore forces every entry to equal Tr(t theta^j). Invertible
Hankel then means t!=0. The forward direction is the reviewed trace-Gram
argument. Hence

    Pr(D_Q)=sum_v C_v^2/(N K)
       - |sum_v chi_A(v)C_v|^2/(N p^(m+1)).                      (2)

The second term is the actual zero-frequency probability, which must not be
counted as a decodable outcome. For odd d it vanishes by scalar symmetry:
C_(av)=C_v for a in F_p^*, while chi_A(a)=chi_p(a)^d and sum_a chi_p(a)=0.
For even d no such automatic cancellation is asserted.

Equations (1)--(2) concern the state CONDITIONED on the known distinctness
projection. The joint ideal per-attempt correctness multiplies (2) by
alpha=(p)_m/p^m. All failed source attempts consume their original copies.

## An elementary packing upper bound

Fix a residue v. Suppose distinct R,R' in its fiber share d rational roots
x_1,...,x_d. Then Q divides R-R', and product_i(X-x_i) also divides R-R'.
These two divisors are coprime because Q is irreducible of degree>=2.
Their product has degree 2d, whereas deg(R-R')<=m=2d-1. Thus R-R'=0,
a contradiction. This also excludes distinct leading scalars on one root
set within a fiber; coefficients, not merely monic root sets, are counted.

Each R contributes binom(m,d) d-element subsets of its roots. No such subset
is contributed by two distinct R in the same residue fiber. There are only
binom(p,d) available subsets, so for EVERY v,

    C_v binom(m,d)<=binom(p,d).

Using sum_v C_v=N in (1) gives

    Pr(D_Q)<=Pr(H)<=max_v C_v/K
      <= binom(p,d)/(p^d binom(2d-1,d))
      <= (d-1)!/(2d-1)!
      = 1/[d(d+1)...(2d-1)]
      <= d^(-d).                                                 (3)

This is an exact all-p bound under the stated source support conditions.
The joint all-flags probability is no larger. For p>=256d^2, combine it
with the reviewed clean lower bound 1/(32(2d-1)!): the ideal clean
irreducible-target success has exp(-Theta(d log d)) order, uniformly in
that regime. Improving constants or the probability analysis cannot turn
this operation into an inverse-polynomial-success receiver.

## Reweighting or rephasing this support cannot fix it

There is a useful stronger scope statement that still concerns only THIS
coefficient support and Fourier/Hankel measurement. For ANY normalized
coefficient state psi supported on S, Cauchy-Schwarz in each fiber gives

    Pr_psi(H)=(1/K)sum_v |sum_(R in S:L(R)=v) psi_R|^2
       <=(1/K)sum_v C_v sum_(R in S:L(R)=v)|psi_R|^2
       <=max_v C_v/K.

Thus (3) also applies to arbitrary phases and weights on the same split
support, including fixed corrupted F sources. The exact C_v^2 identity (1)
is specific to the uniform clean source; the upper bound is not. The same
inequality extends to mixed states or retained ancillary workspace by
convexity/vector-valued Cauchy-Schwarz, provided the measured coefficient
register remains supported on S and the successful event is the same D_Q.

This rules out obtaining polynomial-degree success merely by refining the
overlap estimate, altering split-source weights, or changing its phases.
It does NOT rule out a different coefficient support, a different collective
measurement, use of information from multiple outcomes in another decoder,
or other quantum circuits. It is not a general query/copy/time lower bound.
The reviewed exp(O(d log d)) algorithm remains valid. Its exponentially
small per-attempt success is an actual feature of this operation, not only
an artifact of its overlap lower bound. A new end-to-end improvement must
change something outside the above support/measurement contract.

## One cheapest optional algebraic falsifier

The parent completed this sole exact check, reusing ONLY the saved
`p5_irreducible_quadratic` case in
`classical_baselines/hankel_resultant_control.json`:

    p=5, Q=X^2+2, d=2, m=3, N=40, K=25.

Enumerate its existing 40 public split coefficient labels, reduce each
modulo this public analysis Q, and count C_v exactly in Sage. Check C_0=0,
sum C_v=40, and 3*C_v<=10 for every fiber. Compute (1)--(2) from those
counts and compare with the saved Fourier/Hankel probability for this same
case; no new FFT or additional parameter scan is required. The pure packing
bound is Pr(H)<=floor(10/3)/25=3/25. Supplying Q to this diagnostic count is
analysis-only and must not be added to the native source/receiver inputs.
These finite checks could expose an implementation/counting mistake; the
all-parameter theorem is the divisibility and Cauchy-Schwarz proof above.

The exact Sage result was: eight fibers of size1, sixteen of size2,
sum C_v^2=72, and sum chi_A(v)C_v=8. Therefore

    Pr(H)=9/125, Pr(0)=8/3125, Pr(D_Q)=217/3125.

The last fraction agrees with the existing saved floating FFT to 1e-12.
No new FFT or parameter scan was run. A second independent mathematical
helper read the complete closed note and accepted the exact D_Q event,
packing proof, arbitrary-weight and ancilla extension, and conditional/joint
distinction. The parent independently checked these arguments too.

## Constructive alternatives compared before further work

The external target remains a decoder polynomial in both d and logp for
the published native character-reconstruction problem. The existing circuit
has exp(O(d logd)) cost; classical competitors remain Kopparty full-table
poly(p) under its actual radius/degree promises and empirical exhaustive
BIT decoding with polylog queries but p^d enumeration. None is a classical
time lower bound, and copy-only input does not supply classical values.
The corpus and primary-literature lookups did not supply a new native
operation. No external splitting-distribution theorem is needed above.

**A concrete coefficient-translation proposal.** Keep the native character
source and translate a split coefficient label R to R+h, potentially
outside the split locus. The hoped mechanism was to correct the phase by
a public diagonal depending on R,h, then combine shifted sources into a
larger-support resultant state and use the same moment decoder. A genuine
polynomial-cost transport with inverse-polynomial total success could
remove the identified source restriction. Translation itself costs
poly(d,logp); the missing obligation is the target-dependent ratio
chi(Res(Q,R+h))/chi(Res(Q,R)), with every native query and heralding flag paid.

The cheapest exact falsifier already rejects a Q-independent pointwise
phase correction. At p=7 take

    Q1=X^2+1, Q2=X^2-X+4,
    R=X(X-1)(X-2), h=3(X-2),
    R+h=(X^2-X+3)(X-2).

Both Q1,Q2 are irreducible, and both native sign triples at0,1,2 are
(+1,+1,-1). The original resultant character is -1 in both cases, while
the shifted characters are +1 and -1 respectively. Thus even the original
queried-root signs do not determine the required correction. Parent Sage
evaluation independently reproduced every value. Additional native queries
or collective interference are outside this counterexample, but no explicit
polynomial-cost transport using them was admitted. An extension-field or
arbitrary-resultant oracle would supply the missing input rather than solve
the native problem. No broad impossibility for public unitaries follows.

**Independent full-table scalar OPI comparison.** The input is unchanged:
q=2^t, m=q-1, degree<k=Rm and independent complete half-set tables F_i.
The target is the known DQI score0.840625 at R1/4 in polynomial explicit-input
time. The candidate was classical unequal-symbol KV reliabilities from
exact small-neighborhood acceptance-conditioned RS marginals. The desired
operation would supply noncircular unequal weights and meet the actual KV
certificate; its strongest retained comparators are real Prange restarts,
Algorithm H's verified finite outputs and failed q512 continuation, and
published systematic-basis line search/annealing. No weaker replacement
benchmark was run.

The algebraic first test rejects this candidate before implementation. For
any fixed tables and table-selected T with |T|<=k-1, a uniformly chosen
degree-<k polynomial has its value at i outside T independent uniform of
all evaluations on T. Conditioning on acceptance in T therefore leaves
row i uniform. Also conditioning on its own acceptance gives the uniform
distribution on F_i: precisely the old equal-within-list weights. This
per-instance argument allows selecting T from the tables, not selection
based on hidden sampled-polynomial values. Nontrivial cross-row dependence
requires at least k+1 distinct evaluation rows. Naive exact joint enumeration
costs q^Omega(k); no polynomial contraction was supplied. This is proposal
triage, not a lower bound for other unequal weights or all classical OPI.

Neither alternative is admitted for implementation. Do not add a weight,
shift, noise or degree sweep. Before extending this line, compare independent
high-upside native problems; reopening requires an explicit paid operation
outside this support/measurement boundary and its first decisive falsifier.


## Overcomplete packets and consecutive-window decoding

6 November 2026. Independent core derivation and actual-text mathematical
review accepted. This pass tests a CONCRETE attempted repair: use m>=2d-1 native
copies (for example m=O(d logd)), keep the resulting degree-m split
coefficient register, Fourier transform it, and decode any consecutive
2d-coordinate window. The intended advantage is polynomial(d,logp)
native character reconstruction in place of exp(O(d logd)) cost. No
hidden root labels or chosen extension-field evaluations are supplied.
Public source roots are the uniformly sampled x inputs, NOT independent
observations of the unknown roots of Q; coupon-collector reasoning does
not supply such observations.

Resource requirements of the proposal are explicit: m fresh copies,
distinctness herald alpha=(p)_m/p^m, and scalar phase chi(a)^d, NOT
chi(a)^m. The resultant sign chi(-1)^(dm) is global. Reversible public
degree-m coefficient conversion, shared-seed root erasure and m+1 field
QFTs cost poly(m,logp,log1/eta) for total approximation error eta; scanning
all windows costs O(m d^3) field operations. Failed heralds consume their
copies. The bound below already concerns the ideal conditional state;
approximation error must be charged, not counted as useful success.
An output-law TV error eta adds at most eta to the success bound; choosing
eta<=d^(-d)/100 uses only O(d logd) additional precision bits.

The corpus been-tried/baselines lookups and a primary-literature check
preceded this calculation. Actual Russell--Shparlinski Section4/Theorem6
provides an O(d)-query POVM under its degree/prime hypothesis, not an
efficient receiver circuit. Actual Ivanyos et al., arXiv:1502.06631,
Theorems8/9 retain e^(d/2) quantum or e^d classical time with classical
power-oracle queries; e=(p-1)/2 is not polynomial in logp. Kopparty,
arXiv:2601.07137, provides the stronger poly(p) FULL-TABLE classical
baseline. Although Theorem1 states d<=epsilon sqrt(p), retain the audited
sufficient Algorithm A/Theorem3.1 condition d<=(epsilon/16)sqrt(p), with
corruption<(1/8-epsilon)p.
Those oracle/table inputs are not supplied by phase copies. Existing
native classical controls and their access distinctions are reused; no
new quantum construction or classical scaling scan is needed for the
algebraic falsifier below. The old uniform exp(O(d logd)) upper bound
remains valid, with no classical hardness or priority claim.

Assume Q is monic irreducible of degree d>=2, p odd, and
2d-1<=m<=p. Let S_m contain all squarefree completely split degree-m
polynomials with nonzero leading scalar. All claims below hold for ANY
normalized state whose coefficient register is supported on S_m,
including arbitrary phases, weights, mixtures and retained workspace.
They therefore already cover more than the clean native source, without
charging any target-dependent state preparation as an available resource.

### Full recurrence event

For H=(ker reduction modQ)^perp, residue fibers have ambient size
K=p^(m+1-d). Put r=m+1-d. Two different R,R' in one fiber cannot share r
rational roots: Q and their root product would both divide R-R', forcing
a nonzero polynomial of degree<=m to have a divisor of degree m+1.
Each R contains binom(m,r) such root subsets, so a fiber contains at most
binom(p,r)/binom(m,r) elements of S_m. Fiberwise Cauchy--Schwarz gives

    Pr(H) <= binom(p,r)/(p^r binom(m,r)) <= (d-1)!/m!.

For arbitrary weights/workspace the same argument applies to the vector
sum in each fiber; scalar phase agreement is not assumed. Conditioning
on distinctness cannot improve the joint probability beyond this bound.
Thus demanding a globally consistent longer trace sequence worsens the
factorial ceiling. This is not yet the bound for discarding coordinates.

### Partial readout and all consecutive windows

For j=0,...,m-2d+1, apply the d-by-d Hankel decoder to
(y_j,...,y_(j+2d-1)). Define the d-dimensional coefficient subspace

    W_j = { X^j Q(X) A(X) : deg A<d }.

Its Fourier annihilator enforces exactly the d Q-recurrences in that
window. The first d window entries determine a unique t in F_p[X]/Q
through the trace pairing. The recurrences force all remaining window
entries to be Tr(t theta^r), r=0,...,2d-1. Irreducibility makes its Hankel
matrix invertible exactly when t!=0. Consequently correct decoding is
W_j^perp with the ZERO WINDOW removed; all outside Fourier coordinates
remain unrestricted. It is not the full-register H minus its origin.

Pulling back the W_j^perp projector averages over affine cosets of W_j,
of size p^d. Coefficients outside this window are fixed within each such
coset. This remains the marginal projector if outside Fourier outcomes
are measured and discarded. Hence success is at most the maximum S_m
occupancy of a coset, divided by p^d.

For j=0, two distinct labels in one coset differ by Q A with deg A<d.
If they shared d rational roots, the same coprimality argument would force
A=0. Counting d-subsets of roots gives

    B_0 <= binom(p,d)/(p^d binom(m,d)) <= (m-d)!/m!.

For j>=1 the difference is X^j Q A. Use d shared NONZERO roots, to avoid
the extra factor X^j. Every R in S_m has at least m-1 nonzero roots, so

    B_j <= binom(p-1,d)/(p^d binom(m-1,d))
        <= (m-d-1)!/(m-1)!.

Neither proof assumes independent windows or independent Fourier outcomes.
A decoder that examines every consecutive window and then verifies any
candidate can succeed only in their union. For m>=2d its probability is
at most

    F_d(m) = (m-d)!/m! + (m-2d+1)(m-d-1)!/(m-1)!.

In fact this is uniformly factorially small for ALL allowed m, not just
m=O(d logd). Set B(m)=(m-d-1)!/(m-1)!. Then

    F_d(m)=B(m)[m-2d+2-d/m],    B(m+1)/B(m)=(m-d)/m.

The difference between successive bracketed expressions, after accounting
for that ratio and multiplying by m, is

    (d-1)(m-2d) + d(m-d)/(m+1) >= 0.

Thus F_d is decreasing for m>=2d. At m=2d it is exactly
(3/2)(d-1)!/(2d-1)!. At m=2d-1 there is only the prefix window and the
previous bound applies. For every allowed packet length,

    Pr(any correct consecutive-window decode)
        <= (3/2)(d-1)!/(2d-1)! <= (3/2)d^(-d).

This is the ideal conditional measurement bound; source failures consume
copies and can only lower joint success. It covers choosing the window
after seeing the entire outcome, but NOT a decoder combining imperfect
windows or multiple failed outcomes to infer Q by another rule. Extra
packet length alone cannot pay growing-degree success for this operation.
No numerical control is necessary: the exact coprimality/packing proof
and elementary monotonicity calculation decide this proposed repair.

Disposition: no packet-length sweep, more-source wrapper or new receiver
subsystem. The constructive question must now change the measurement,
the support, or the way imperfect outcomes are decoded. A paid operation
for that change is still required; these possibilities are UNKNOWN, not
hard or ruled out. In particular do not turn the source labels into
unavailable hidden-root observations. This scoped rejection leaves the
known parameterized receiver and all previous exact controls intact.

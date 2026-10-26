# Outer-Coded Chirps: A Constructive Proposal And A Classical Falsifier

2026-10-19. Local mathematical derivation REVIEW PENDING. No new quantum
algorithm, novelty, classical hardness or speedup is asserted. This is a
DIFFERENT explicit moment-square task, not a solution of the unresolved
punctured folded-norm problem. The initial full-support probe is followed by
explicitly scoped sparse-support extensions below. No accepted candidate or
central negative.

## Scientific Question And Portfolio Decision

After the bounded global MQ probe gave no new witness, another generic solver
budget was not justified. DCP still lacks a new constructive receiver; generic
Hamiltonian/GI changes of subject would not supply one either. This pass instead
tests a SPECIFIC alternative mechanism for explicit diagonal quadratic systems:
can local quadratic-phase readout and a decodable outer code remove the
quadratic-source erasure problem without making native search classically easy?

The mechanism is not conjugate-copy polarization: it proposes ONE chirp per
coordinate, retains the original square constraints, and uses outer coding.
The direct full-field Reed--Solomon realization fails the search-advantage
test: a deterministic classical construction below solves EVERY target in
the entire proposed useful rate range, and beyond. Retain the local primitive
and counteralgorithm; do not build a large quantum compiler for this family.

The [quadratic-DQI manuscript](https://arxiv.org/html/2510.08061v2) explicitly
withdraws its state-preparation theorem because its per-register step has
exponentially small joint success. That is motivation to examine a new route,
not an established algorithm used by this pass. The existing repo's conjugate-
chirp repair is different and already fails by changing the objective.

## Original Public Problem

Let p>=5 be an odd prime and N=p-1. There is one ORIGINAL F_p variable x_a
for EVERY a in F_p*. The public target b in F_p^r specifies

```text
sum_(a in F_p*) a^k * x_a^2 = b_k mod p,   0<=k<r.
```

The full Vandermonde coefficients/support are public arithmetic input, not
oracle calls, planted witnesses or a chosen-query hidden function. Find ANY
native vector satisfying these equations, with zeros allowed. Homogeneous
targets can additionally request a nonzero vector; the construction returns
one. Neither exact weighted sampling nor nonzero EVERY coordinate is claimed.

N=p-1 is essential. The algorithm is polynomial in the actual full variable/
matrix size and log p, NOT polynomial in log p for an implicitly enormous
support. It does not expand the existing61-bit,127-position input to a field
table and call that an efficient attack. Main controls here instead have
p31/127/1021 and N30/126/1020.

## Proposed Quantum Mechanism: Not Yet A Theorem

Write G_(a,k)=a^k. For a label y in F_p^r, c=G*y is a standard RS codeword.
Its product quadratic chirp is

```text
|Phi_y> = p^(-N/2) sum_x exp(2*pi*i*y.(G^T*x^2)/p) |x>.
```

If labels could be erased coherently on the needed source, a Fourier-weighted
sum over y with phase -b.y would produce the original moment-square solution
state, NOT an unconstrained linear replacement. That is the constructive
motivation. It would use reversible G evaluation, local chirps, local readout,
an outer decoder and its reverse, QFT precision and every failure flag.

The intended local readout has correct-symbol probability approaching1/2.
The known [Guruswami--Sudan decoder](https://people.csail.mit.edu/madhu/papers/1998/gs.pdf)
suggests trying r/N<1/4, since its familiar agreement threshold is approximately
sqrt(r/N). This is a DESIGN WINDOW, not an executed polynomial-time
outer decoder or quantum gate bound. The bounded exhaustive decoder below
does not establish that window. Other decoding codes/windows are separate
questions, not excluded here.

IMPORTANT COHERENCE OBLIGATION: good classical identification on each basis
label does not by itself prove a uniform coherent erasure bound on arbitrary
superpositions. Near-orthogonality/Gram normalization, interference between
decoding failures, list selection, source support and the FULL flagged channel
must be bounded. Do not promote this proposal by substituting a measured
classical decoder or an assumed isometry. A bounded full instrument is now
executed below, but no scalable outer coherent receiver is supplied.
The native classical falsifier makes that investment unnecessary for this task.

## Actual Local Unitary, No Local Postselection

For nonzero square u, let s be one of its square roots and choose a verified
nonsquare nu. Define a unitary C by

```text
C (|s>+|-s>)/sqrt(2) = |u>,
C (|s>-|-s>)/sqrt(2) = |nu*u>,
C |0> = |0>.
```

The pair states are an orthonormal basis and the output square/nonsquare
cosets partition F_p*. Reversible squaring, a canonical square root, a sign
Hadamard and quadratic-character tag cleanup give a specified local route;
it does not use another unknown chirp copy. For p3mod4 square roots use the
usual modular exponent, with ordinary public arithmetic/precision costs.
A scalable fault-tolerant circuit is NOT implemented.

On |phi_d>=p^(-1/2) sum_x exp(2*pi*i*d*x^2/p)|x>, followed by inverse-sign
Fourier readout, amplitude at t is

```text
A(t|d) = [1 + sqrt(2)*sum_(u nonzero square) exp(2*pi*i*(d-t)*u/p)] / p.
P(t=d) = [1+(p-1)/sqrt(2)]^2 / p^2.
```

The channel is translation covariant. For p3mod4 the nonzero Gauss sum is
imaginary, so every wrong label has probability (1-Pcorrect)/(p-1). For p1mod4
the two wrong-label cosets differ; the implementation tests this distinction
instead of claiming a q-ary symmetric channel universally. Correct-symbol
probability stays as above. Dropping chirp phases instead gives identical
columns for every label and average identification1/p, not approximately1/2.

Dense native unitaries at p5/7/11/13 independently check orthogonality, all
labels, output normalization, exact predicted probabilities and this phase
countercontrol. These are physical identity controls, not hard benchmarks.

## Deterministic Classical Completion For EVERY Target

Here is the decisive stronger baseline. Suppose

```text
1 <= r < N/2,       d=N/2+1,
F(X)=X^(N+2) - sum_(k=0)^(r-1) b_k*X^(N-k).
```

Compute the monic polynomial part R0 of the formal square root of F at
infinity using the repo's EXISTING `root_at_infinity`, then set

```text
R=R0-R0(0),        x_a=R(a) for every a in F_p*.
```

No square-root solvability oracle, norm completion, random target or search
is involved: F is monic of degree2d and2 is invertible. Formal Newton series
gives deg(R0^2-F)<d. Removing the constant changes the square by degree at
most d, hence

```text
deg(R^2-F)<=d,
[X^(N-k)] R^2 = -b_k  for all0<=k<r,
R(0)=0.
```

The strict inequality r<N/2 ensures N-r+1>d, so no prescribed coefficient
is touched. Native finite-field power sums give

```text
sum_(a in F_p*) a^j = -1 if N divides j, and0 otherwise.
```

For k<r, deg(X^k*R^2)<2N. The only possible alias exponents are0 and N.
The exponent0 contribution vanishes because R(0)=0. The exponent N
contribution is -[X^(N-k)]R^2=b_k, exactly the ORIGINAL equation. This is
an algebraic all-target argument, not an inference from successful seeds.
Since R is monic of degree d<N, it cannot vanish at all N distinct points;
even b=0 produces a nontrivial homogeneous solution.

The strict rank guard is not an infeasibility assertion. At the excluded
r=N/2 boundary, removing the constant can destroy a prescribed coefficient:
p7,N6,r3,b=(0,0,1), F=X^8-X^4 is an explicit countercontrol. Other algorithms
may still solve that target. Strict nonzero coordinates and weighted exact
sampling are also different tasks.

## Dense Puncturing Does Not Automatically Rescue It

Let S be ANY distinct nonzero evaluation support of size L and T=F_p* minus S,
with M=|T|. The original problem now sums only over S. If

```text
1<=r<L-(p-1)/2,
```

keep the same F and R0 above, set W(X)=X*product_(a in T)(X-a), and take
R=W*quotient(R0,W). Thus R differs from R0 by a remainder of degree at most M,
vanishes at0 and EVERY omitted point, and is still monic of degree d.
Now deg(R^2-F)<=d+M<N-r+1 by exactly the stated strict inequality. All
prescribed coefficients survive, so the same full-field power-sum proof
applies with omitted variables exactly zero. The vector returned contains
ONLY the original S coordinates in their original order; no target or matrix
is silently replaced. A monic degree d<N polynomial cannot vanish on all S
as well as its forced complement, so a zero target still gets a nonzero vector.

The gate implies p<2L. Enumerating the complement and polynomial setup is
therefore polynomial in the actual input/output size. Sparse p61/127-position
supports are REJECTED BEFORE field expansion, not claimed solved or hard.
For support density L/(p-1)>2/3, the classical guarantee covers the ENTIRE
asymptotic proposed RS local-readout window r/L<1/4. Other densities may leave
a gap; this is not a general punctured-code dequantization.

## Costs, Tests And Research Decision

The live producer exhaustively verifies all175 small full-support targets and
all42 support/target combinations at p7,L5,r1; the report saves those counts
and SIX complete native witness records: (L,r)=(30,6),
(126,24),(1020,240),(1020,509),(100,24),(800,190). The last two use unchanged
proper subsets; their omitted points are forced to zero, not silently dropped.
Every original equation is independently replayed. Local physical unitarity
error is at most2.23e-16 and predicted probability error at most3.34e-16.
The strict JSON report binds its producer/dependencies. The initial local/
classical pass had14 tests within an82-test connected regression passing25.98s.
The coherence extension below adds focused tests; its final verification is
recorded in AGENT_HANDOFF.md. These are NOT full repository suite counts and
overlap the earlier462-test milestone; the counts must not be added.

Formal-root series work is polynomial in N and log p, using FLINT. The
reference independently evaluates R by native integer Horner at every point
and recomputes every original equation, paying O(N*d+N*r) field products.
Its counters are expression counts, not a complete bit budget. The entire
classical witness, target, root, removed constant and root certificate are saved.
There is no degree/fp-to-extension relaxation or source reroll.

This classical algorithm covers EVERY fixed r/N<1/2 for sufficiently large N,
including the proposed ordinary-RS local-readout/list-decoding window below1/4.
Consequently no asymptotic SEARCH advantage remains for this particular
candidate family, regardless of whether its coherent-erasure obligation can
eventually be solved. The result is a local application of known formal-root
machinery, with independent mathematical review/novelty review still pending.

Do not transfer it to arbitrary diagonal MQ, other code generators, punctured
RS supports, translated folded extension-norm predicates, or exact quantum
sampling. The dense puncturing regime above is covered, arbitrary sparse
puncturing is NOT. Any re-entry must identify a different explicit code/source whose
original search task survives a matched classical attack AND provide the
coherent erasure/Gram argument. Merely changing the name of the outer code or
assuming a decoder is not a new mechanism.

```sh
python theorems/outer_coded_chirp_probe.py --write
python -m pytest -q tests/test_outer_coded_chirp_probe.py
```

Routine optional qsearch/EXP exposure should call this actual producer and
preserve the search-only/explicit-support/no-quantum-compiler scope, separating
the dense and sparse classical guarantees below. No central
negative/proof/candidate admission is needed for an unadmitted proposal.

## Full Coherent Instrument: Bounded Execution Completed

The v2 producer retains the original F_p variables and ALL residual labels.
For each public support it constructs the actual complex source, applies
U tensor L, computes a target-independent maximum-likelihood decoder D(t),
subtracts D(t) from the label, cleans its workspace while t is still available,
and applies the actual adjoint readout. The reversible permutation models this
workspace cleanup; no inverse of a hidden history is assumed. D uses only the
public code and received word, with canonical tie breaking, not b or the true y.

The native comparison is independently built from the original equations:

```text
M=p^r, alpha_b[y]=exp(-2*pi*i*b.y/p)/sqrt(M),
v_b[x]=sqrt(M/p^L) * 1[G^T*x^2=b],
lambda_b=||v_b||^2=M*number_of_native_solutions/p^L.
```

The ideal is deliberately UNNORMALIZED. Every target is retained, including
infeasible ones with lambda_b=0; normalized fidelity is undefined for those.
The report distinguishes herald probability, herald AND native validity,
conditional validity, full flagged fidelity and conditional fidelity. They
are not interchangeable. Exact integer histograms of decoder-correct received
words, together with rational sqrt(2) enclosures, bound the finite decoder
error without a Monte Carlo confidence claim.

### Average Identity, Not A Worst-Target Theorem

Let E=U tensor L * Phi, let q=(1/M) sum_y sum_(t:D(t)=y)|E[t,y]|^2 and
epsilon=1-q. Each normalized actual full flagged output A_b obeys:

```text
P_b[zero residual label]=q, for every Fourier target b;
(1/M) sum_b ||A_b-|0>v_b||^2 = 2*epsilon;
mean_b P_b[zero flag AND ORIGINAL equations] >= max(0,1-2*epsilon).
```

Proof: the Fourier alpha_b form an orthonormal label basis. Averaging the
ideal squared norms gives1 because every source column is normalized.
Averaging the actual/ideal inner product gives q, since the zero-label part
retains exactly E[t,y] with D(t)=y. Actual norms are1, yielding2-2q.
The complement of the zero-flag native-valid subspace annihilates the ideal,
so its actual probability is at most the squared vector error. This also
covers infeasible targets without normalizing them. A bound for EVERY target
derived solely from this mean loses a factor M: max(0,1-2*M*epsilon).

This is a local application of known decoding-to-state-preparation reasoning,
not a novelty claim. The [soft-decoder analysis](https://arxiv.org/html/2411.12553v2)
discusses the coherent-error issue and averaged inhomogeneous targets; the
[quantum decoding manuscript](https://eprint.iacr.org/2023/1686.pdf) is also
relevant prior art. These sources are not substitutes for the native checks.

### Actual Controls And Falsifiers

| p | L | r | All targets | Infeasible retained | Label success q | Mean paid native validity | Mean squared vector error |
|---|---|---|---|---|---|---|---|
| 3 | 2 | 2 | 9 | 5 | 0.419390 | recorded in live report | 1.161221 |
| 7 | 4 | 2 | 49 | 0 | 0.449399 | 0.208795 | 1.101202 |
| 11 | 5 | 1 | 11 | 0 | 0.827765 | 0.691976 | 0.344470 |

All69 targets are executed, not a favorable subset. Mean error identities
agree within1.2e-14 in the exploratory runs. Some targets exceed the mean
bound: at p11 the worst squared error is0.351898, not0.344470. The rigorous
mean native-validity lower bound is about0.655530 there, but the corresponding
worst-target bound is vacuous. The rank-one case is classically easy: sample
a first coordinate a and test whether b-a^2 is square. For p3mod4 and b!=0,
at least(p+1)/2 choices work; verified square roots use modular exponentiation.
Two coordinates suffice, with expected at most2 proposals under independent
uniform randomness. Seeded transcripts are not confidence certificates.

Two adversarial countercontrols are saved:

- Replacing U-adjoint by U-transpose at p7,L3,r1,b1 leaves normalization and
  herald probability0.681050 unchanged, but full flagged fidelity falls from
  0.401053 to0.000599. Paid native validity falls from0.410618 to0.071621.
- A public unitary rotating two Fourier modes in dimension M has basis
  decoding error4/M-6/M^2 but one Fourier target's conditional fidelity
  1/(M^2-4M+6). At M=2^20 the error is below4e-6 and fidelity below1e-12.
  M17 is checked as an actual dense unitary; the large case uses exact rational
  formulas only. This disproves a GENERIC worst-target inference, not a
  source-specific RS theorem or a general quantum algorithm possibility.

### Costs And Remaining Blockers

The full model stores p^(L+r) complex amplitudes per bank, enumerates p^r
codewords and p^L received words, and executes every Fourier target. The
largest bank has1771561 amplitudes. These are EXPONENTIAL identity calibrations,
not a polynomial-time quantum decoder, scaling experiment or speedup evidence.
No accepted candidate, central negative or proof promotion is generated.

Sparse RS evaluation supports avoid the dense formal-square proof but do not
thereby become hard. Re-entry requires an actual polynomial outer decoder on
the proposed source, controlled complex phases and precision, a clearly stated
average-versus-worst-target objective, and matched high-rank sparse classical
attacks. The average identity is useful but does not supply that decoder or
classical hardness. The separate folded-norm global classical question remains
open; no reduction between these two explicit tasks is asserted.

The coherence pass ended at a clean pause point. The user subsequently resumed
work and requested that Claude's notes be read; the next pass follows.

## Sparse Barycentric Completion: Sparsity Alone Is Not An Escape

2026-10-19 resumed pass, local derivation REVIEW PENDING. No novelty claim.
Claude's merged corpus/rediscovery/failure-mode audits recommend checking
retained failures before building another receiver. Corpus queries for sparse
RS chirp completion and barycentric square-class completion retrieve the dense
formal-root attack and the existing Lagrange-weight identity, but not this
all-target construction. Retrieval is not a novelty certificate. Related
classical machinery is standard [GRS duality](https://users.math.msu.edu/users/halljo/classes/codenotes/GRS.pdf)
and [self-dual GRS evaluation-set construction](https://arxiv.org/abs/2005.11732).
The latter includes subgroup/coset constructions; no new code duality is claimed.

The previous dense proof needed p<2L because it enumerated missing field points.
That guard remains correct for THAT algorithm. The new algorithm never uses
the complement: it has a different, explicitly testable support condition.

### Exact Claim And Algorithm

Let p=3 mod4 be prime, S contain L distinct nonzero ORIGINAL points, and
A(X)=product_(a in S)(X-a). Suppose all A'(a) have the SAME quadratic character.
For EVERY target b in F_p^r with1<=r<=floor(L/2), a deterministic classical
algorithm polynomial in L and log p returns a nontrivial native vector solving

```text
sum_(a in S) a^k*x_a^2=b_k,  0<=k<r.
```

Choose kappa=A'(a_0). Each kappa/A'(a) is square; compute its verified root
s_a by exponent(p+1)/4. Define the linear functional

```text
T(P)=sum_(a in S) P(a)/A'(a).
```

Lagrange interpolation gives T(X^j)=0 for j<L-1 and T(X^(L-1))=1.
Compute its further moments only through degree L+r-2. A triangular solve
chooses B supported in degrees L-r,...,L-1 so T(X^k B)=b_k/kappa.
Explicitly, choose B_(L-1-k) in increasing k; its coefficient in the kth
equation is1 and lower-index coefficients do not contribute.

Set d=ceil(L/2), choose the monic even-degree polynomial

```text
F=A+B       if L is even,
F=X*A+B     if L is odd,
```

and let R be its formal-square polynomial part at infinity, deg R=d.
Then deg(R^2-F)<d and F(a)=B(a). For k<r, d+r<=L implies
deg(X^k*(R^2-F))<=d+r-2<=L-2, so T annihilates this residual.
Finally return x_a=s_a R(a), retaining the original support, coefficient field,
moment equations and target. Indeed

```text
sum a^k*x_a^2 = kappa*T(X^k R^2)
               = kappa*T(X^k B) = b_k.
```

Since R is monic of degree d<L and each s_a is nonzero, the returned vector
cannot be identically zero, including when b=0. The algorithm needs degree
O(L) polynomials, O(L*(L+r)) quadrature products, L modular square roots and
native replay; there is no array, loop, generator search or factorization
whose size is the ambient p. The reference arithmetic counts are not complete
bit-operation or wall-time claims.

The strict all-coordinates-nonzero version is ALSO classically solved when
r<floor(L/2). Choose a scalar c avoiding the L forbidden values -R(a), using
at most L+1 public candidates; L<p guarantees one exists. Replacing R by R+c
changes its square by degree at most d. Since d+r<L, quadrature still
annihilates that change for every required moment. Thus the same target is
preserved and every coordinate is nonzero. The implementation verifies this
directly. At r=floor(L/2), it deliberately refuses the strict guarantee;
the last equation can change. This is a degree boundary, not infeasibility.

### Why It Is A Meaningful Sparse Attack

Any odd-order multiplicative subgroup, nonzero scalar coset, or affine image
avoiding0 satisfies this condition: its vanishing polynomial is
(X-h)^L-c, whose derivative at a is L*(a-h)^(L-1). The power factor is square
because L-1 is even. The solver takes the public support and verifies the
condition; subgroup recognition or a discrete-log oracle is unnecessary.

The live controls use p=2^61-1 and L155, with (rank,strict)=(38,true),
(77,false),(76,true): the local decoder's proposed quarter-rate window,
the half-rate algebraic boundary, and a strict near-boundary case. They
preserve all155 native variables and verify every original equation.
Support generation for the control factors ONLY155=5*31 and tries explicit
public bases2,3 with modular order checks, which are recorded and charged.
An affine-shifted/scaled support checks that special full-field power sums
are not silently being used. All7 targets at p7,L3,r1 and all121 targets at
p11,L4,r2 are also replayed, including homogeneous ones.

### Attempts To Break The Argument And Scope

- Without the common derivative square class, some s_a do not exist in F_p.
  The implementation refuses this case instead of using F_(p^2), changing
  signs or claiming hardness. The support(1,2,3,4) at p11 is a countercontrol.
- The multipliers are necessary: returning R(a) WITHOUT s_a solves a different
  weighted problem and fails an explicit native target. Tests replay scalings
  using products of point differences, independently of polynomial derivatives.
- The half-rate boundary is from annihilating the residual's degree, not from
  Chevalley-Warning existence or finite experiments. Above it the function
  refuses; refusal is not an UNSAT certificate.
- The p3mod4 restriction is an implemented deterministic-square-root boundary,
  not a mathematical assertion that the construction fails for other primes.
- This supplies search witnesses, not uniform/exact quantum solution sampling.
  It does not solve arbitrary sparse support, arbitrary simultaneous quadrics,
  the old folded m31 norm problem, or a hidden-shift oracle problem.

Research decision: do not rescue the rejected dense candidate by moving it
onto an odd-order subgroup or a support meeting this derivative criterion.
Those sparse native search families also have a uniform classical solver.
Generic sparse supports with mixed derivative classes still need their OWN
classical attacks and a constructive scalable decoder; neither their hardness
nor a quantum speedup follows from this scoped result.

### Further Hard Check: Mixed Classes Do Not All Escape, Either

There is a derived extension, NOT YET IMPLEMENTED by this pass. Choose the
majority derivative class and let M be the minority points, |M|=m. Multiply
by W=product_(a in M)(X-a): replace the formal root R0 by
R=W*quotient(R0,W). The removed remainder has degree<m, so
deg(R^2-F)<=d+m-1. The same quadrature proof works if

```text
r <= floor(L/2)-m.
```

Set minority coordinates exactly0 and use the native square scalings on
majority coordinates. This is still a solution of the original zero-allowing
equations, not deletion of those equations. It does NOT yield a strict
all-coordinates-nonzero witness when m>0. This construction and its finite
tests belong in the mechanical follow-up only after preserving this contract.

An actual direct point-difference calculation at p=2^61-1, S=(1,...,127)
gives71 nonsquare and56 square derivatives. This extension would cover only
r<=63-56=7, NOT the quarter-rate rank31 question. Thus it does not justify
declaring general sparse RS solved. The original folded-norm input is a
different system and is not addressed by this calculation at all.

## Polynomial Decoder Certificate And The OPI Equivalence

The next hard check replaces an assumed exponential ML table by a specified
polynomial classical decoder at the theorem level. This is an analytic
certificate, NOT execution of a quantum state or a new implementation of GS.
[Chatterjee--Harsha--Kumar, Theorem1.1](https://arxiv.org/html/2511.05176v2)
supplies deterministic list decoding in poly(L,log p) at integer agreement
t>sqrt(L*(r-1)). It avoids a hidden randomized-factorization assumption for
coherent decoding over large prime fields. The local application still needs
independent review and a full quantum precision/resource contract.

### A Decoder With No Hidden List-Selection Advice

List every degree<r polynomial agreeing with the received word at least t
times. Choose greatest agreement, canonical ties, and label0 if the list is
empty. Do not ask for the true message or original target to select a list item.

For p3mod4 the actual product chirp readout is memoryless q-ary symmetric:
q0>1/2 and each particular wrong symbol has q1<1/(2*(p-1)). For ANY transmitted
codeword, bound its probability of fewer than t correct positions by

```text
E_true <= 2^(-L) * sum_(j=0)^(t-1) binom(L,j).
```

Any other degree<r polynomial agrees with the true one on at most r-1
positions. To obtain t agreements it needs u=t-r+1 accidental matches.
Independence and a union bound over position subsets and ALL other words give

```text
E_wrong <= (p^r-1)*binom(L,u) / [2*(p-1)]^u,
epsilon <= min(1,E_true+E_wrong).
```

No words are enumerated by this calculation. If the true word reaches t and
no other word does, selection is uniquely correct. The bound holds for every
basis label, and the earlier full-channel identity consequently gives
uniform-target mean paid ORIGINAL validity >=max(0,1-2*epsilon). It is not a
worst-target guarantee. For any fixed rate R<1/4 choose sqrt(R)<t/L<1/2;
then t/L>2R, so the true-word tail is exp(-Omega(L)) and the competitor bound
is exp(-Omega(L log p)) as L grows with L<p. This is an algorithmic reduction
using known decoding results, not evidence for classical hardness or novelty.

The v5 artifact evaluates exact rational bounds, rounded OUTWARD to96 dyadic
bits. Rounding a very small positive bound upward is deliberate, never0.
At p=2^61-1:

| L | r | t | Decoder-error upper bound (approximate display) |
|---|---|---|---|
| 512 | 64 | 200 | 2.67e-7 |
| 1024 | 128 | 400 | 8.36e-13 |

These are symbolic guarantees under the ideal specified instrument, not runs
at those quantum register counts. A uniform full-flagged implementation trace
error delta must be subtracted from the mean validity bound. For p3mod4 a
public nonsquare can be -1, not an assumed free nonresidue search; local C
can be built using reversible squaring, canonical modular square roots and
a conditional Hadamard on the root sign. Source/QFT phases, approximate
uniform field states, reversible decoder workspace cleanup and total error
still require an explicit costed implementation. Tests/report gates keep
those obligations OPEN. No central proof or candidate is promoted.

### This Is An Existing OPI Route In Different Coordinates

Before treating that mechanism as new, apply standard GRS duality. For ANY
distinct support S, construct the same target lift B but without dividing b by
kappa. Then all solutions z to sum a^k*z_a=b_k are EXACTLY

```text
z_a=(B(a)+P(a))/A'(a),    deg(P)<K=L-r.
```

The inclusion follows from quadrature on degree<=L-2 polynomials; equality
follows since the nullspace and the polynomial space both have dimension K.
The native square problem is therefore OPI with public shift -B(a),
orientation equal to the quadratic character of A'(a), and degree bound K.
Square-root each accepted native z_a to recover x_a in the ORIGINAL field.
Conversely, interpolating A'(a)*x_a^2-B(a) gives such a degree<K polynomial
for every native solution. This is a bijection on square-coordinate solutions,
not necessarily on their multiple choices of square-root signs.

Thus r/L<1/4 is a HIGH-RATE K/L>3/4 explicit-character OPI problem, not an
independent new quantum primitive. The [soft-decoder framework](https://arxiv.org/html/2411.12553v2)
already supplies the relevant inhomogeneous reduction paradigm. Its stated
full-support convention is not a reason to overlook GRS-dual weights on a
punctured input. A new name does not remove the repo's classical OPI attacks.

The new wrapper calls the EXISTING norm solver, without editing or replacing
it, on one fixed p=2^61-1, S=(1,...,127), r31 input. The equivalent OPI has
K96,56 square orientations and71 nonsquare orientations. Public seed6611 and
cap128 produce a perfect OPI witness in16 charged base-field factorizations,
then127 native square roots satisfy ALL31 original moment equations. All127
coordinates happen to be nonzero; the control did not request a strict-mode
population guarantee. Every rejected norm target and the winning polynomial
are saved. This refutes the finite control as advantage evidence, NOT every
target, every sparse input or the old folded extension-norm problem.

### A Correct Average-Case Transfer, With An Important Limit

There is a further exact distinction from the old fixed-input norm analysis.
Let b be uniform in F_p^r and let M be an INDEPENDENT uniform polynomial of
degree<K. The high-r-coefficient triangular construction of B_b and the low-K
coefficient space are complementary. Therefore

```text
(b,M) -> B_b+M -> its L evaluations -> negative OPI shifts
```

is a linear bijection onto F_p^L: the induced shifts really ARE IID uniform.
Adding M preserves the native syndrome, since it is in the kernel. Running
OPI on shifts -(B_b+M) and recovering x from (B_b+M+P)/A' never rerolls the
original b. Consequently the existing norm attack's one-trial IID population
lower bound transfers to UNIFORM native targets plus independent kernel masks,
when its explicit degree and field hypotheses hold. For the above support,
D72 and K96 meet those hypotheses; the exact lower bound I_p(72)/p^72 is
saved. The seeded fixed-input witness did NOT execute that population process.

For a FIXED b, random M reaches only p^K shifts, not p^L; it is not IID.
Also E_b[q(b)]>=1/poly does NOT prove high-probability success on most b,
nor justify replacing E_b[(1-q(b))^T] by (1-E_b q(b))^T. This removes a claim
of negligible classical population success but does not fully match the
quantum mean bound. The distribution of q(b), rather than more finite seeds,
is the next meaningful probability question. All source/IID/amplification
gates remain explicit and independent review is pending.

FOLLOW-UP: [native-variable masking](MOMENT_TARGET_MASKING.md) now BYPASSES
that probability gap for certified splits, rather than claiming the old
unmasked q(b) is well behaved. It reserves ORIGINAL coordinates, uses their
exact MDS/Gauss near-uniform moment law, then applies a kernel mask and the
existing norm solver to the residual target. At the same p61,L127,r31,
reserving32 coordinates yields a local fixed-b floor>=0.0208117541, with two
actual witnesses in6 attempts each. Its separate artifact and review-pending
proof do not retroactively change the v5 unmasked protocol's status flags.

Final resumed-pass verification:124 connected tests passed6.44s, including
the existing OPI norm-attack tests and exhaustive bidirectional reduction /
uniform-target-plus-mask checks. This is not the full repository suite.
The live schema v5 binds the producer and three dependencies. Registry
validation valid:true/issues:[], Python compilation, recursive site JavaScript
syntax, site checks and whitespace checks pass. No commits or central claim
promotions were made; unrelated concurrent arXiv-watch changes were preserved.

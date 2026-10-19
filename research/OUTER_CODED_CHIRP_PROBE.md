# Outer-Coded Chirps: A Constructive Proposal And A Classical Falsifier

2026-10-19. Local mathematical derivation REVIEW PENDING. No new quantum
algorithm, novelty, classical hardness or speedup is asserted. This is a
DIFFERENT explicit full-support task, not a solution of the unresolved
punctured folded-norm problem. No accepted candidate or central negative.

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
preserve the search-only/full-support/no-quantum-compiler scope. No central
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

This is a clean pause point. No additional research pass is started.

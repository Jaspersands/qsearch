# Native Line Source And Incidence Decoder

LOCAL DERIVATION / REVIEW PENDING. This is a source-transfer certificate and
a final-field baseline, NOT a new full-depth quantum algorithm. No accepted
candidate, general decoder lower bound, or speedup claim.

## Why This Pass

The adaptive retention ceiling obstructs constant-rate all-component linear
top-degree erasure at growing depth. A different possibility is learning the
few shared secret weights directly from native states. This pass supplies an
exact one-output source interface and checks a concrete direct learner. It
also identifies where the learner fails rather than extrapolating field
success to prime-power phases.

## Full-Depth Source Law

Let L=2r+1, Q=3^(r+1), R=3^r. Input labels are independent uniform canonical
native labels. The low-label matrix A defines a kernel chart j=x+Vz over F3.
Measure its pivot coordinates, retain its first free coordinate, and measure
all other free coordinates. The frame depends ONLY on low labels; every
measurement branch is retained. With m=n+1 there is always a free coordinate.

Conditional on the low labels, each scalar native frequency pair has unique
coordinates

```text
C1=a+3b mod Q, C2=2*C1+3d mod Q,
b,d independent uniform in Z_R, a fixed modulo3.
```

For a physical coordinate on which the line is nonzero, its digits
(j0,j1,j2) permute (0,1,2). Its contribution to the two residual frequency
differences, divided by3, is an affine map of (b,d) with integer matrix

```text
[(j1-j0), (1[j1=2]-1[j0=2])]
[(j2-j0), (1[j2=2]-1[j0=2])].
```

All six determinants are +/-1. Conditional on every other high coordinate,
this map is a bijection on Z_R^2. It holds independently for each secret
component, since the selected coordinate is low-defined and its high lifts
are independent across components. Thus the two output frequency vectors
are independent uniform vectors in Z_R^n. Their even-level inverse chart
gives an exact uniform native label at L-1. Fresh disjoint batches give IID
outputs. No field substitution is used in this proof.

The input amplitudes are flat. The initial syndromes and measured complement
coordinates are uniform and independent of full labels and secret; each
branch has probability3^-(m-1). Relative amplitudes of the surviving qutrit
are exactly those of the lower-level source, up to a global phase.

Charge n+1 ODD-LEVEL input qutrits per output, m-1 measured registers, and all
public arithmetic. This does not supply the intermediate odd-level source
from original samples, recover the initially lost top secret digit, prove
independence of several outputs from one packet, or close a recursion cost.
High-label-adaptive frames are outside this uniformity proof.

## Exact Final-Field Decoder

At R=3 write the public component table as alpha*lambda+beta*lambda^2:
alpha=f2-f1, beta=2*f1-f2. Choose uniform b in F3, apply the known inverse
quadratic phase b*lambda^2, and measure with inverse ternary Fourier transform.
For the unknown field secret s,

```text
beta.s=b  =>  outcome o=alpha.s deterministically;
beta.s!=b =>  o uniform over F3.
```

Every legal outcome supplies a NOISE-FREE cubic constraint

```text
[1-(beta.v-b)^2]*(alpha.v-o)=0 over F3.
```

Use polynomial functions with x_i^3=x_i. Their degree-at-most3 feature space
has dimension

```text
D=1+n+n(n+1)/2+n(n-1)+binomial(n,3).
```

Streaming exact field elimination targets rank D-1. The remaining nullvector
must normalize its constant feature to1 and agree with every monomial
evaluation at the recovered linear features. Insufficient rank, inconsistent
data, zero affine normalization and non-evaluation nullvectors never produce
an accepted secret. There is no enumeration of3^n guesses. Dense arithmetic
cost O(M*D^2), storage O(D^2+nD); original source consumption M*(n+1).
This recovers ONLY s mod3, not the parent secret mod9.

### Span And Probability Argument

Translate w=v-s; put A=alpha.w, B=beta.w, c=b-beta.s, d=o-alpha.s.
The allowed pairs are (0,0) with probability1/3, and each
(+/-1,d), d in F3, with probability1/9. They are independent of alpha,beta.
Their relations are

```text
R_00=(1-B^2)A,
R_cd=(-B^2-cB)(A-d) for c=+/-1.
```

Differences between d=1 and d=0, followed by sums/differences between c=+1
and c=-1, yield B and B^2. Sums/differences with d=0 yield B^2*A and B*A;
R_00 then yields A. Squares of linear forms span quadratic forms because2
is invertible. B^2*A spans cubic terms: repeated-index terms are direct,
and xyz follows by polarizing (y+z)^2*x. Pure cubes reduce to linear terms.
Hence the feasible relation support spans the full D-1 dimensional space
of features vanishing at s, including every translated degree<=3 monomial
with no constant term.

For any strict row span choose a functional annihilating it but not that
hyperplane. For some allowed (c,d), its value on R_cd is a nonzero polynomial
of total beta-degree<=2 and affine alpha-degree<=1. A nonzero coefficient
in beta is nonzero on at least1/3 of beta assignments; the resulting affine
alpha polynomial is nonzero on at least2/3. The chosen (c,d) has probability
at least1/9. Therefore each fresh sample escapes a strict span with
probability at least2/81, conditional on all earlier samples.

For K=D-1 and confidence bits kappa>=1, M=81*(K+4*kappa) suffices for failure
probability<=2^-kappa. Couple rank progress to Bernoulli(2/81) until full
rank. Its mean is2K+8*kappa, and the lower-half Chernoff bound is at most
exp(-K/4-kappa)<=2^-kappa. This is a LOCAL proof awaiting review, not a
probability theorem established by a few successful seeds.

## Higher Roots: Precise Failure Boundary

For actual phase modulus R=3^r, the same MUB outcome amplitude is proportional
to1+zeta_R^u+zeta_R^v. Three unit complex numbers sum to zero iff they form an
equilateral triangle. Thus exactly two of the R^2 independent phase-frequency
pairs have zero probability for a fixed basis/outcome. Some outcome among all
nine basis/outcome choices is zero iff f1 and f2 both belong to(R/3)Z_R:

```text
fixed outcome zero fraction =2/R^2;
any MUB zero fraction =9/R^2.
```

For n>=2 take true s=e1 and trial t=e2. Their frequency pairs are independent
under the actual uniform even native source. Whatever the true measurement
outcome, the trial is excluded by an exact support-zero constraint with
probability2/R^2. Across fresh batches it survives M constraints with
probability(1-2/R^2)^M. Its elimination probability is at most2M/R^2.
Any rule requiring a unique support-consistent secret needs M>=tau*R^2/2
to reach success probability tau on this true/trial pair.

THIS IS NOT a general sample, computational, classical or quantum lower
bound. It concerns only this single-qutrit MUB support-elimination rule.
Positive likelihoods differ and can carry information; collective receivers
are untouched. Correlated true/trial frequency pairs need separate analysis.

An actual L5 native countercontrol, three labels(1,0), zero initial syndrome
and zero measured complement, has residual table(0,8,8) mod9. Its formal
quadratic coefficients are alpha=3,beta=5, whose low shadow is(0,2).
For s=1,b=2 that shadow falsely predicts only o=0. Actual o=1 and o=2 each
have probability(2-2*cos(4*pi/9))/9>0.18. Either yields a false cubic relation.
The API rejects every actual phase modulus other than3.

## Literature And Novelty Gate

[Ivanyos and Santha, Theorem5/Corollary6](https://arxiv.org/html/1503.09016v2)
already solve constant-degree univariate hidden polynomial graph problems
over prime fields with growing parameter dimension. Final-field decoding is
known-easy territory; the explicit incidence baseline is not a novelty claim.

[Boucher, Fouque and Shen, Lemma7 and Sections4.2-4.3](https://arxiv.org/html/2609.34996v1)
use low-only selection to preserve uniform high lifts in a native zero-sum
sieve. Compare complete recursive costs, not one merger. Our weighted-line
proof concerns integer-secret packets; it does not certify arbitrary ring
secrets or an improvement to their general sieve.

[Arunachalam et al., Theorem8](https://arxiv.org/html/2208.07851v2)
learn the same unknown Boolean-domain phase from copies; the generalized
result assumes even q and explicitly charges q-dependence. It is not a free
transfer to varying native ternary packets or growing roots.

## Verification And Next Research

`python theorems/ternary_incidence_decoder.py` produces the source census,
growing-depth controls, live native final-field decoders and exclusion ledgers.
`node research/certificates/ternary_incidence_crosscheck.js` independently
reconstructs the small source and re-eliminates the live public constraints.
Focused tests include complete feasible constraint spans and all one-variable
nontrivial escape functionals. These are bounded checks of the derivations.

Gemini owns CLI/registry wiring and full production validation. Do not create
an accepted algorithm candidate from these controls. Record the shadow
counterexample as a scoped negative result, not a generic decoder no-go.

GPT NEXT: develop a likelihood-sensitive or collective native receiver with
an implicit implementation and charged source budget. Alternatively prove an
even-to-odd source transfer improvement that closes the remaining recursion
cost. Kill either mechanism against known sieves and legal classical
postprocessing before calling it algorithmic progress. No more fixed-field
benchmarks unless they directly falsify a proposed growing-depth mechanism.

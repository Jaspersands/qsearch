# EDCP: Correlated Centers, Clean Samples, And Source Contracts

Date: 2026-09-24. LOCAL DERIVATION / REVIEW PENDING.

This is a theory handoff, not a new implemented algorithm or a claim of
novelty. The elementary identities below have bounded numerical checks;
neither those checks nor the cited papers establish a new LWE algorithm.
No candidate, proof status, runtime bound, or speedup gate is promoted.

## 1. Research Decision

The repository's scalar DCP arithmetic work misses an important adjacent
question: can we obtain many usable **vector-label** phase states from the
Gaussian, unknown-center reduction, without destroying their secret phase?

The concrete target is a paired-state factory with a shared unknown center
and independent public phase labels. Section 3 gives an all-outcome center
cancellation if that resource exists. Sections 4-6 reject three immediate
shortcuts. Finding this factory, or an alternative joint measurement that
uses the nuisance instead of discarding it, has more leverage than another
thermal-arithmetic constant sweep.

This is a conditional research target, not evidence that the factory exists.
Structured EDCP is a separate promising branch; preserve its correlated
coefficient registers instead of reducing it immediately to scalar DCP.

## 2. Primary Literature And Noninterchangeable Promises

The following are source summaries, not locally established theorems.

- Bai, Jangir, Kirshanova, Ngo, Youmans,
  [ePrint 2025/1046](https://eprint.iacr.org/2025/1046.pdf), Section 4:
  for power-of-two modulus q, the vector-label EDCP algorithm uses
  2^{O(log n log q)} time and comparably many clean samples. It is
  quasi-polynomial when q is polynomial in dimension n. One merge measures
  a binary syndrome of n+1 qubits and retains a two-element affine fiber.
  Section 4.3 explicitly identifies the carry error in extending this to
  larger digits. The polynomial clean-sample budget of the usual LWE
  reduction does not supply this algorithm's input. These are published
  mechanisms, not discoveries of this project.
- Chen, Hu, Liu, Luo, Tu,
  [arXiv:2310.00644v2](https://arxiv.org/pdf/2310.00644), Sections 3-6:
  known amplitudes, deliberately quadratic-phased amplitudes, and
  unknown-phase amplitudes have different algorithmic guarantees. Section 5
  generates exponentially accurate Gaussian EDCP states with an unknown
  center; after Fourier transformation this becomes an unknown linear
  phase. Its width can be handled by a finite error-norm guess, but its
  per-output center is not thereby known. Theorem 48 specifies the
  distribution, quantifiers, sample count, and reduction cost. The
  quadratic-phase algorithm is not an algorithm for ordinary Gaussian
  samples just because a diagonal chirp is easy to apply.
- Wen and Zheng,
  [ePrint 2026/155](https://eprint.iacr.org/2026/155.pdf), Definition 22,
  Theorems 4-5 and Section 2.5:
  structured EDCP retains a polynomial's coefficient vector in a coherent
  register. The module-LWE connection has ring, rank, noise, sample and
  secret-distribution conditions. Its direct scalar reduction uses modulus
  f(q), not q. The paper explicitly asks for algorithms exploiting the
  structure. Its informal equivalence must not substitute for the full
  parameter inequalities when admitting a candidate.

Read the exact versions above. In particular, distinguish amplitude widths
from widths of squared-amplitude distributions; Gaussian conventions vary.
No claim about a deployed cryptosystem follows from this audit.

## 3. Constructive Target: Cancel A Shared Unknown Center

Use q for the phase modulus and n for vector-label dimension. Our amplitude
convention is g_{sigma,c}(j)=exp(-pi*(j-c)^2/sigma^2), with
Z_sigma(c)=sum_{j in Z} g_{sigma,c}(j)^2. Work initially on integer registers:

    |G(a,c)> = Z_sigma(c)^(-1/2)
                sum_j g_{sigma,c}(j) omega_q^{j<a,s>} |j>.

This is a model of the Fourier-transformed unknown-center source, not an
oracle for preparing it from a known secret. A finite implementation needs
an explicitly charged tail bound and an unwrapped integer sum register.

Suppose two independently prepared states have labels a1,a2, common width
sigma, and centers c1,c2. Compute and measure the INTEGER sum w=j1+j2.
Retain j=j1 and reversibly erase j2=w-j. Direct completion of the square gives

    g_{sigma,c1}(j) g_{sigma,c2}(w-j)
      = C(w,c1,c2) g_{sigma/sqrt(2), (w+c1-c2)/2}(j).

The secret phase is, up to a branch-global factor,

    omega_q^{j<a1-a2,s>}.

Thus, when c1=c2, the remaining center is the KNOWN value w/2, for EVERY
outcome w. Translating by floor(w/2) leaves center 0 or 1/2, both public.
There is no rare w=0 postselection and no center estimator. The width only
shrinks by sqrt(2). If the two labels are independent uniform and independent
of the center-matching condition, their difference is uniform too.

For known sigma>=1, projection onto the two integers surrounding the known
center, followed by known-amplitude balancing, gives a clean phase qubit
with probability Omega(1/sigma). More explicitly, after recentering let
eta in {0,1/2}, sigma'=sigma/sqrt(2), and h_b=g_{sigma',eta}(b), b=0,1.
The diagonal success filter has amplitudes min(h_0,h_1)/h_b. Including the
projection, its success is

    2 min(h_0^2,h_1^2) / Z_{sigma'}(eta).

It depends only on public width and parity. For polynomial sigma this is
an inverse-polynomial loss, not a quasipolynomial one. A polynomial-cost
factory for arbitrarily many such matched pairs, with sufficiently small
joint source error, would therefore feed the known vector-label sieve.
For power-of-two q=poly(n), a verified connection to the LWE source could
yield a quasi-polynomial LWE algorithm. Other moduli need an additional
charged reduction or a different solver. This conditional implication is the upside;
the paired factory is NOT supplied here.

Required factory contract:

1. State law and joint center law, not merely equal one-register marginals.
2. Common width, or a proved unequal-width replacement.
3. Independent usable labels, or a proof for their actual joint law.
4. Heralded matching, a known center difference, or charged approximation.
5. Total generation cost, success rate and error across all requested pairs.
6. No cloning, secret/noise-coordinate oracle, or free replay of a measurement.

For approximate matching, the residual center error is Delta=(c1-c2)/2.
For width sigma', the exact positive Gaussian overlap between centers u,v is

    exp(-pi*(u-v)^2/(2 sigma'^2))
      * Z_{sigma'}((u+v)/2) / sqrt(Z_{sigma'}(u) Z_{sigma'}(v)).

At smooth widths the normalization ratio is 1 plus an exponentially small
periodic correction. The trace-distance error is then at most approximately
sqrt(pi/2)*|c1-c2|/sigma for small mismatch. This is a per-state bound, not
permission to reuse the same tolerance for quasipolynomially many outputs.
Track the joint error. Unknown unheralded good-pair probability is not a
clean-state success flag.

## 4. Adversarial Checks On The Factory

### Independent centers do not purify themselves

The output's unknown part is (c1-c2)/2, not zero. Before conditioning on w,
independent center variables with variance v have difference-half variance
v/2; the squared width is also halved. The variance-to-width ratio v/sigma^2
therefore does not improve. For covariance rho*v it becomes
(1-rho)*v/sigma^2 instead. Correlation, not two-copy availability, is the
resource. In the continuous independent-Gaussian model the difference is
independent of the measured sum, so selecting sums does not fix this.
This conditional-independence statement is not asserted without correction
for arbitrary discrete or non-Gaussian center laws.

### Replaying a full measurement record is not a source

In the reduction, an output has form y=A^T v+x, with uniform v and an
injective A^T. Equivalently one can bound the measured distribution directly
before the change of variables. For each fixed remaining random choice,
at most one v yields any specified y. Consequently max_y Pr[y]<=q^(-n).
Independent repetition hits a specified full record only with this small
probability; the expected number of exact record collisions among L fresh
preparations is at most binomial(L,2)/q^n.

This rejects full-record rejection replay. It does NOT rule out matching a
coarser invariant, another correlated preparation, or center equality between
different records. In particular, center collision probability and the ability
to recognize a collision are different questions.

### Sharing only a linear readout can cancel the signal as well

Consider a proposed two-input factory whose retained amplitudes and all
environment registers depend on the uniform variables v1,v2 only through
v1+v2. The state is invariant under

    (v1,v2) -> (v1+h,v2-h).

Fourier transforming these registers therefore supports only a1=a2. Sum
conditioning of j1,j2 then leaves secret frequency a1-a2=0 in the protocol
above. This is an exact finite-group symmetry argument, not a noise estimate.
It applies to the simple construction that computes only the sum of the two
reduction readouts. More generally, a shared linear readout restricts Fourier
labels to the annihilator of its kernel; directions invisible to that readout
carry no corresponding secret phase.

Computing separate readouts and later ignoring their difference is different:
the difference still holds which-branch information if it remains in an
environment. Tracing it out does not implement coherent erasure. This
argument is not a no-go for every possible correlated-state factory.

## 5. Exact Stress Test For A Naive Noisy Vector Sieve

There is also a cheap way to turn any smooth unknown-center state into a
nearly clean phase qubit. It is insufficient for the following naive sieve.

Choose a random offset in {0,1}, measure which adjacent integer pair contains
j, and relabel that pair as {0,1}. Randomly apply X while also replacing the
public label a by -a. Discard the offset, bin and random-sign record. For an
independent uniform label, the resulting qubit has equal populations and
visibility

    V_sigma(c) = sum_j g(j)g(j+1)/Z_sigma(c)
               = exp(-pi/(2 sigma^2)) Z_sigma(c-1/2)/Z_sigma(c).

Poisson summation gives Z_sigma(c)=(sigma/sqrt(2)) times
sum_k exp(-pi*sigma^2*k^2/2) exp(2*pi*i*k*c). Hence the normalization ratio
is 1+O(exp(-pi*sigma^2/2)) uniformly in c at large sigma. This protocol needs
neither c nor sigma. It deliberately discards potentially useful side data.

Now assume independent qubits with common visibility V, independent uniform
labels in Z_q^n, and q a power of two. Apply the published n+1-to-1 binary
syndrome merge, conditioning on full row rank. Its nonzero kernel vector k
is uniform among all 2^(n+1)-1 nonzero binary vectors. The two retained
assignments differ precisely on supp(k), so their coherence is V^wt(k).
Higher label bits make the new label uniform independently of this kernel.
After discarding internal records, the exact recurrence is

    F_n(V) = ((1+V)^(n+1)-1)/(2^(n+1)-1).

In particular, for 0<=V<=1,

    F_n(V) <= ((1+V)/2)^(n+1)
            <= exp(-(n+1)*(1-V)/2).

If the initial loss is at least c/n for constant c>0, the first merge leaves
visibility bounded below 1, and the second leaves exp(-Omega(n)) visibility.
For sigma=sqrt(n), the leading-Gaussian values are:

| n | Initial V | One Merge | Two Merges | Three Merges |
|---|---:|---:|---:|---:|
| 16 | 0.906490 | 0.443072 | 0.00388633 | 5.20040e-7 |
| 64 | 0.975755 | 0.452587 | 9.38181e-10 | 1.65291e-27 |
| 256 | 0.993883 | 0.455092 | 3.14850e-36 | 3.49405e-111 |

These are analytic recurrence evaluations, NOT growing-size simulations.
Use expm1((n+1)*log1p(V))/(2^(n+1)-1) or an equivalent stable expression;
subtracting two nearly equal exponentials gives false small-V values.

The precise recurrence assumes discarded records and independent fresh input
blocks. It neither rules out retaining amplitude information nor proves that
Gaussian unknown-center states lack sufficient information. Larger widths
require their own quantitative analysis; do not turn the c/n condition into
a universal statement about all reductions.

## 6. Two Additional Category Errors To Reject

For a translated error amplitude sum_e g(e)|t+e>, a physically applied chirp
exp(i*kappa*y^2) produces error-coordinate phase

    kappa*e^2 + 2*kappa*t*e + kappa*t^2.

Only the last term is global. The cross term depends on the unknown center
t=<a,s>. One has NOT obtained the known quadratic-phase input by applying
a known chirp to the visible register. A unitary also preserves all pairwise
input overlaps; it cannot replace a hard-to-distinguish translation family
by a more distinguishable one without an additional charged resource.

For larger-digit syndrome merging, use the explicit carry counterexample
q=16, digit alphabet {0,1,2,3}, Y=(1,1), syndrome 0 modulo 4. The fiber is

    (0,0), (1,3), (2,2), (3,1).

Its lifted sums are 0,4,4,4, not 0,4,8,12. At secret 1 the phases are
(1,i,i,i), not (1,i,-1,-i). Gaussian elimination modulo 4 does not remove
the carry-dependent secret phases modulo 16. This is a concrete control for
the already published Section 4.3 obstruction, not a new general no-go.

## 7. Preserve The Structured EDCP Branch

Let Q=f(q), z=(1,q,...,q^(d-1)), and start from a product coefficient amplitude:

    sum_c prod_j h(c_j) |c> |x+<c,z>s mod Q>.

Fourier-transform and measure the second register to obtain a uniform label
a. Up to a global phase, the remaining state factors exactly as

    tensor_j sum_u h(u) omega_Q^{u<q^j a,s>} |u>.

The d registers are conditionally in a product state, but their PUBLIC labels
are a,q*a,...,q^(d-1)*a, not independent samples. This distinction matters
even if every label marginal is uniform. For f(x)=x^d+1, gcd(q,Q)=1, and
the deterministic label relations survive. The modulus has Theta(d log q)
bits. For q>2 and power-of-two degree d>=2, Q is not a power of two:
it is odd when q is even, and is 2 modulo 8 when q is odd.

Therefore neither the small-modulus complexity nor the independent-label
merge analysis transfers automatically. Do not discard d-1 registers and
then claim to have tested the structural opportunity. Equally, a relation
whose total frequency is exactly zero carries no secret information.

Next theory target on this branch: a collective operation on these geometric
label families that retains nonzero secret frequency, with its actual modulus,
coefficient width, natural probability, and reduction-supplied sample budget.
The full module-LWE parameter inequalities still need an independent audit.

### Source-level trace-distance repair

In the inspected 2026/155 version, Lemma 23's displayed measurement equality
and Lemma 24's replacement of pure-state density matrices by diagonal
probability matrices cannot be used as written. These bookkeeping issues
do not by themselves refute the reduction. Local counterexamples and repairs:

- Computational-basis measurement maps |+> and |->, whose input trace
  distance is 1, to identical outcome-conditioned density operators.
  Thus a maximum over the displayed branch distances need not equal the
  input distance. Normalized postselection is not generally contractive.
- If a normalized pure state loses squared mass epsilon under a support
  truncation, its distance from the normalized truncation is sqrt(epsilon),
  not epsilon. This follows from their overlap sqrt(1-epsilon). The
  square-root loss still preserves an exponentially small tail guarantee.
- For the PARTICULAR Fourier conditioning used here, every label has the
  same probability. The conditional coefficient states differ only by the
  same diagonal phase and the support truncation. Their overlap remains
  sqrt(1-epsilon) for EACH label. This directly repairs that distance step
  without an invalid generic postselection rule.

These are analytic observations, not an independent verification of the full
paper. The registry must retain the exact reduction promises and pending
parameter audit rather than treating a citation as a completed proof gate.

## 8. Bounded Checks Actually Executed

These were small independent mathematical probes, not the project test suite.
All Gaussian sums used integer indices -64 through 64 (phase tests used
-48 through 48); the widest amplitude width was 8. The identities themselves
above are exact on Z. Numerical agreement is not a substitute for a tail
bound in production code.

- 165 Gaussian product cases: widths 2,4,8; center pairs (0,0),(.7,.7),
  (-2.3,-2.3),(.7,-1.1),(2.3,.2); sums -5 through 5.
  Maximum normalized-amplitude residual 4.45e-16.
- The adjacent-overlap identity on those 15 width/center combinations:
  maximum residual 2.23e-16.
- 72 phase-preserving product controls: widths 2,4,8; center pairs (.7,.7)
  and (.7,-1.1); (a1,a2,s)=(1,5,3),(2,7,1),(0,3,5), modulus 16;
  sums -3,0,1,4. Maximum infidelity 8.89e-16. These are prescribed secret
  cases, NOT an all-secret exhaustive test.
- All binary n-by-(n+1) matrices for n=1,2,3: respectively 3,42,2520
  full-rank matrices. Every nonzero kernel vector had equal multiplicity.
  Five visibility values 0,.1,.5,.9,1 matched the recurrence to 2.23e-16.
- All 4096 modulus-4 label matrices for n=2, including all four syndrome
  outcomes of each full-rank matrix: each of the four output labels appeared
  exactly 2688 times. No invalid rank-deficient input was silently accepted.
- 160 direct mixed-state pair projections with input visibility .71,
  secret (1,3): maximum matrix residual 1.86e-16.
- A sum-only-readout Fourier symmetry check at modulus 8, A=(1,3),
  b=(4,0), y=(0,2), j1,j2 in {-1,0,1}: off-diagonal label amplitude
  at most 9.82e-18 across all nine choices.
- Unequal-center falsifier: sigma=4, c1=2.3, c2=.2, w=1 has fidelity
  0.6486102046 with the incorrectly centered target. The carry counterexample
  also rejects its incorrect phase progression.

No production code, full-suite run, CLI workflow, registry refresh, or candidate
acceptance was performed. Gemini owns those tasks. No new commit was made.

## 9. Gemini Handoff: Implementation Only After Contract Review

1. Add a vector-label Gaussian phase-state reference with explicit amplitude
   convention, center provenance, joint label law and finite-tail accounting.
   Known-secret dense states are verification references, not supplied sources.
2. Implement the integer-sum instrument, complete branch probabilities, known
   recentering and the charged two-point filter. Include unequal centers,
   unequal widths, modular-wrap traps, and independent-versus-correlated labels.
3. Implement the exact binary merge visibility recurrence and mixed-state
   controls above. Keep the known algorithm's citation and scope in artifacts.
   Do not label a recurrence evaluation as a quantum simulation.
4. Keep candidates requiring matched centers blocked until a source factory
   is supplied. Record sample error, replay cost and phase-label rank as proof
   obligations. A positive input fixture does not discharge those obligations.
5. Add the structured EDCP source schema without pretending its geometric
   labels are independent or its modulus is q. Defer a search engine until
   there is an actual proposed collective operation.

Main-model continuation: derive or falsify a source-level correlated-center
factory beyond the sum-only symmetry obstruction, or a structure-preserving
operation for the coefficient-register family. Do not spend theory usage
building CLI/report plumbing for this note.

## 10. Follow-Up: Two More Source-Level Shortcuts Fail

### Matching the public lattice syndrome

The full-record replay bound alone leaves an obvious loophole: match only
the class of y modulo the known q-ary lattice. That can be computed without
recovering its short representative. However, independent rejection matching
still has a small clean success probability, as follows.

Use the ideal unwrapped source variables before the reduction measures y:
J has squared Gaussian amplitude of width alpha, X_0 in Z^m has independent
squared Gaussian coordinates of width B, and the fixed integer error vector
is e. Put R=X_0-J*e. Then exactly

    Pr[R=r] = sum_j Pr[J=j] prod_i exp(-2*pi*(r_i+j*e_i)^2/B^2)/Z_B^m,
    Z_B = sum_{x in Z} exp(-2*pi*x^2/B^2).

This is a mixture of translated product Gaussians, so its largest point mass
is at most Z_B^(-m) <= (sqrt(2)/B)^m, using Poisson summation at zero.
For independent residuals, both inside the open ball of radius lambda_1/2,
equal public lattice syndromes force identical residuals: their difference
is a lattice vector shorter than lambda_1. Thus

    Pr[syndromes match AND both residuals are short]
       = sum_{r short} Pr[R=r]^2 <= Z_B^(-m).

Among L independent preparations, multiply by binomial(L,2) for an upper
bound on any such clean collision. If a residual is outside the unique
short-representative region, syndrome equality no longer implies matching
centers. Its failure probability cannot be counted as clean success.
Simple rejection or its amplitude-amplified version remains expensive when
this bound is exponential. This is not a lower bound for all coherent
collision algorithms or all source factories.

An exact finite-support mixture check used m=2, q=257, lattice generator
(1,11), error e=(1,2), B=3, alpha=2.5, X_0 coordinates -12..12 and J=-8..8.
Its residual mass summed to 1; maximum point mass was 0.1284977598 against
the finite-normalization bound 0.2222215778. All 97 short residuals had
different syndromes, short mass 0.9977031106, and matching-short-pair mass
0.0545017328. The lattice minimum squared was 122. Adding (1,11) produces
an explicit alias outside the short-region argument. These finite checks
do not establish the actual high-dimensional reduction's tail probability.

### Universal exact center-blind extraction

There is a simple obstruction to a proposed universal exact cleanup filter.
On a finite consecutive register j=0,...,D-1, fix a secret phase theta. Apart
from normalization, a Gaussian state with center c has coordinates

    exp(-pi*j^2/sigma^2) exp(i*theta*j) x^j,
    x=exp(2*pi*c/sigma^2)>0.

For D distinct centers these vectors span the full register, by the
Vandermonde determinant. If a Kraus operator K must map every such input
to a scalar times one fixed clean output |phi_theta>, then range(K) is
contained in span(|phi_theta>). If the same promise holds for a second
secret phase with a noncollinear clean output, K must be zero. Allowing
some centers to have zero success probability does not evade this argument.
It also holds for independent center grids on several inputs, whose spans
tensor to the full space, and for each Kraus operator of a pure-output
success branch.

This rejects a UNIVERSAL EXACT center-blind pure-state extractor under that
finite-family promise. It does not rule out approximate or mixed outputs,
secret information in classical outcome probabilities, extra public center
information, restricted center laws, or a source with correlated centers.
The actual reduction's record-dependent center is not automatically the
independent full-span promise.

Exact symbolic constraints had full rank 2D for D=2,...,7 when the target
outputs were |+> and |->. Conversely, the shared-center two-register
restriction j1+j2=1 leaves the same scalar x on both terms and gives a
nonzero clean-phase filter. This positive control explains precisely why
the common-center proposal is not contradicted by the obstruction.

REVISED PRIORITY: do not build a syndrome-replay factory or universal exact
center-cleanup circuit. The constructive next work is now in
`research/STRUCTURED_EDCP_GAUSSIAN_FIBERS.md`: a native one-block compiler
and the genuinely harder random-multiplier two-block fiber.

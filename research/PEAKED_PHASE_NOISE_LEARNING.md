# Learning through high-entropy phase noise

2026-10-30. A mathematical extension of the
[exterior phase learner](EXTERIOR_NOISY_PHASE_LEARNING.md), with exact
resource/reference controls. Not a hardware execution, novelty certificate,
or a classical-input speedup. The input promise remains exact and important.

For the quadratic/unknown-stabilizer-basis specialization, the later
[full Pauli symmetry analysis](PAULI_CONJUGATION_SYMMETRY_LEARNING.md) removes
R<p when a global symmetry gap and inverse purity bound are supplied.
Its preferred direct skew Bell route avoids graph charts and is assembled
from existing sampling/verification machinery. It does not identify a
designated original basis and does not extend the higher-degree theorem here.

## Theorem target: replace low rank by one heavy component

Let p be an odd prime, D<p fixed, and F:F_p^n -> F_p an unknown polynomial
of degree at most D. Input consists only of fresh IID copies of

    rho = sum_(b in F_p^n) w_b |psi_(F+b.x)><psi_(F+b.x)|.

The weights may have FULL support and exponentially large entropy/rank.
Supply an integer R<p such that max_b w_b >= 1/R. The proposed algorithm
recovers the nonlinear coefficients of F in polynomial resources in
n,R,log p,1/epsilon at fixed D, using the existing published primitives
and reviewed pure-copy learner. Its exact SDE, spectral and synthesis
backends are not all implemented here. Reviewer Mendel independently checked
the spectral extension, quadratic gap and stabilizer-basis reduction below.
This is automated review, not human peer review. R is a numeric resource parameter,
not a free logarithmic-size promise with polynomial-in-log(R) cost.

There is no input rank bound, known heavy label, minweight, classical
evaluator, preparation inverse, conjugate-state source or global symmetry
gap. There IS an exact phase-diagonal promise in one unknown F-basis.
This is stronger than having inverse-polynomial fidelity with some phase
state: a mixture of two distinct nonlinear phase states can have large
fidelity with both and does not identify either as a designated target.

## Fixed spectral selection

The component states are orthonormal, so their weights are eigenvalues.
Let alpha=1/R, ell=(alpha+1/p)/2 and W=(alpha-1/p)/2. Choose one threshold
tau uniformly from a rational midpoint grid in (ell,alpha), indexed by
uniform bits. Its thresholds need not themselves be dyadic rationals. Then

    tau > 1/p, tau > 1/(2R), tau < alpha,
    W >= 1/(2R(R+1)).

The top eigenvalue is retained. Trace one implies that the retained rank
satisfies 1<=r<=K=min(p-1,2R-1); hence r is nonzero modulo p even when
the original rank is p^n. Retained mass is at least alpha, and the
normalized retained minimum eigenvalue is at least w=1/(2R).

Choose beta=epsilon/16, M=2^ceil(log2(32R/beta)), one uniform a in [0,M),

    tau_a = ell + W (2a+1)/(2M),   Delta = W/(4M).

Threshold spacing is 4Delta. An eigenvalue spoils at most one offset.
Every eigenvalue within Delta of this grid exceeds 1/(4R), so at most
4R eigenvalues, counting multiplicity, can spoil any offset. The exponentially
many small eigenvalues are irrelevant to this union bound. Consequently

    Pr[bad grid] <= 4R/M <= beta/8.

Bad-grid failure is charged, not detected. Always enforce finite clocks.
Degenerate eigenvalues are retained or removed as whole eigenspaces;
the corresponding wedge is basis-independent up to global phase.

## Rank, filtering and complete clocks

Use the existing [copy-based spectral primitives](REES_MIXED_SPECTRAL_SOURCE.md),
not a supplied eigenvalue oracle. On a good grid, let

    h=min(Delta/2,w^2/128), kappa=zeta=w/128,
    m=128 w^-2 ceil(log2(2/beta)).

Perform m independent eigenvalue-estimation experiments on fresh targets
and program banks. Clip Y to [0,1]; average 1_(Y>=tau)/Y, with zero below
tau. Its mean estimates the integer rank because eigenvalue lambda is
sampled with probability lambda. The bias is <=1/32 and deviation >1/8
has probability <=beta. Round to an integer and abort outside [1,K].
No incorrect rank is silently certified by this range check.

For a deterministic maximum T of requested wedges, take

    b=ceil(log2(KT/beta)), N=2RK b,
    S=T(N+1), C=2R ceil(log2(S/beta)), A=S C.

N bounds growth attempts per wedge. K=1 permits zero growth instead.
C bounds filter trials per required accepted input. Growth and filter
timeouts each cost <=beta in the ideal run; either aborts the whole run.
Apply each complete threshold instrument with half-diamond error
beta/(2A), and allocate beta/2 total to growth-gate synthesis. The full
adaptive preparation, including rejected branches, then differs from its
ideal reference by <=beta. Do not divide by the probability of a rare
relative-coordinate outcome.

Beyond m training targets and at most A filtering targets, program copies
cost

    O(m h^-2 zeta^-1 log^2(2/kappa))
    + O(A^2 Delta^-2 beta^-1 log^2(2A/beta)).

Negative-time cleanup uses fresh programs. Only the threshold bit is
measured after eigenvalue-work uncomputation. Approximate physical filters
need not have exact support; rank statements refer to the ideal comparison.
Delta^-1 is polynomial in R,1/beta even when p is exponentially large.
Register and arithmetic costs are polynomial in n,log p and precision.
Comparing a finite phase estimate with a rational threshold uses exact
integer arithmetic; the grid needs no exact non-dyadic quantum phase gate.

Fix the threshold and retained support throughout the entire learning run.
Its wedge produces the same fixed unknown
J=F+mean(B_tau).x under varying public maps A_u, exactly as in the earlier
proof. All selected errors retain the same nonlinear F. Discarding most
of the original probability mass therefore causes no nonlinear bias.
Allocate epsilon/2 to the capped core, including its quantum precision:
total failure/error is <=epsilon/2+5beta<epsilon.

The new code exposes target-copy caps and labels the exclusion of program
copies. The two O-bounds above, rather than the target count alone, describe
the asymptotic source consumption. There is no complete compiled filter
or rank acquisition in the implementation.

## A stronger direct quadratic competitor

For F(x)=x^T A x/2+ell.x, use the
[four-copy cancellation instrument](NOISY_QUADRATIC_PHASE_FILTER.md).
It gives (y,z=Ay+e), uniform y independent of e, and

    Pr(e=0) >= sum_b w_b^4 >= R^-4.

For a candidate Pauli W=Z_z X_y and f=z-Ay,

    d(f)=Tr(rho^2)-Tr(rho W rho W^dagger)
        =(1/2) sum_b (w_b-w_(b-f))^2.

Choose a point b_star of weight a>=1/R. Since R<p, its next R f-translates
are distinct from each other and from b_star. At least one of those R
points has weight <=(1-a)/R. The drop from a is therefore at least1/R^2.
Telescoping along a path of length at most R and Cauchy-Schwarz give

    d(f) >= (1/2) (1/R^2)^2/R = 1/(2R^5).

This simpler bound was supplied independently by Zeno after Mendel checked
the earlier two-regime bound. Thus g=1/(2R^5) is a valid uniform gap. No exact
rank or heavy label is needed. This gap is between purity and a tested
conjugation overlap, not a promised minimum spectral spacing.

One explicit conservative clock, for failure epsilon, uses

    T=16R^4 (n+ceil(log2(4/epsilon))) candidates,
    m_swap=ceil(128 g^-2 ceil(log2(8(T+1)/epsilon))) trials/estimate.

Estimate purity once and each of T candidate overlaps, with fresh copies.
Each mean's tolerance g/8 implies difference error <=g/4; accept at loss
<g/2. Conditional on correct verification, correct y's are uniform.
Before spanning n dimensions each candidate increases the span with
probability at least R^-4(1-1/p). Chernoff bounds the failure under the
displayed T by epsilon/4. Simultaneous Hoeffding bounds charge epsilon/4
for all T+1 estimates. Reserve epsilon/4 each for bounded conic-witness
generation and complete quantum-instrument precision. Raw copies are

    4T + 2(T+1)m_swap = O-tilde(R^14(n+log(1/epsilon))).

This avoids spectral filtering and wedges for quadratics. It is a loose
polynomial guarantee, not a practical copy estimate. Gaussian elimination
recovers A; the original linear phase remains a gauge.

## Unknown stabilizer basis under arbitrary Pauli noise

There is a stronger native QUANTUM-input consequence. Suppose rho is
diagonal in an unknown maximal stabilizer eigenbasis on n odd-prime qudits.
Equivalently it is an unknown pure stabilizer state subjected to an
arbitrary Pauli mixture. Allow full rank; retain only the same peak promise
max eigenvalue>=1/R with R<p. Recover the phase-free Lagrangian label space
L, NOT the original pure state's eigenvalue signs, which noise can relabel.

Pauli conjugation acts on the joint eigenlabels by a translation whose
kernel is L=L^perp. Any Pauli outside L shifts along cycles of length p.
Conjugation invariance would repeat a maximum weight at least p times,
contradicting p/R>1. Thus the Pauli conjugation stabilizer is exactly L,
even with degenerate eigenvalues. The preceding purity-loss bound g is
basis-independent and separates EVERY outside Pauli from L.

Choose a uniform symplectic matrix S and lift it to a known Clifford.
Uniformity is not justified by an unspecified short random gate word.
One exact construction recursively samples a nonzero vector u uniformly,
a vector v uniformly from [u,v]=1, and a symplectic basis of their
orthogonal complement. All ordered symplectic bases are equiprobable.
Use finite rejection clocks for field sampling and nonzero-vector draws.
Existing public symplectic elimination supplies the Clifford decomposition;
modular arithmetic, phase synthesis and Fourier transforms are charged in
binary p. This note does not implement the uniform sampler or full receiver.

A uniform image SL is transverse to the computational Z-space with
probability

    p^(n(n+1)/2) / product_(j=1..n)(p^j+1)
      = product_(j=1..n)(1+p^-j)^-1 > 1/2.

The numerator counts symmetric graph matrices. On this event,
SL={(y,Ay):y in F_p^n} for a symmetric A, and its eigenbasis is exactly
the full-computational-support quadratic-phase basis. Apply the four-copy
instrument and original-copy SWAP verifier above.

On a nontransverse chart the regression law is NOT asserted. Instead,
enforce the same finite clocks and only return after n verified candidates
have independent translation parts y. Honest verification places each
candidate in SL. Independent y then forces SL to be a graph: success
itself certifies the missing chart condition. Check Y invertible and
A=ZY^-1 symmetric, and map the generators back with S^-1. Incorrect
verification remains a charged failure, not an absolute certificate.
Verification can act on original copies using pulled-back Paulis, without
applying the trial Clifford to those copies.

For an explicit wrapper let H=ceil(log2(4/epsilon)). Give each of H trials
the preceding quadratic budget with error epsilon/(4H), and reserve
epsilon/4 each for uniform-Clifford sampling abort and Clifford precision.
No good chart occurs with probability <=2^-H<=epsilon/4. Classification
and good-chart failures sum to <=epsilon/4. Total error is <=epsilon;
copy cost is H times the single-chart bound, still polynomial in
n,R,log p,log(1/epsilon). All bad-chart branches stop at fixed clocks.

This is a general stabilizer-BASIS learner under a noise-spectrum promise,
not arbitrary mixed-state tomography, recovery of a designated noiseless
state, or a new classical-input quantum speedup. Known pure-stabilizer and
candidate-verifier primitives remain prior art. Exact subsumption and
novelty require separate specialist review.

## Sharp qualifications and falsifiers

At maximum weight1/p, a uniform error distribution on F_p e_1 can hide
the difference between F and F+x_1^2. Thus no universal exact learner
exists under the weakened promise max weight>=1/p. For a mixture of
that periodic distribution with an extra weight xi on a single label,
the peak exceeds1/p by xi(1-1/p), yet the two phases' k-copy distance
is <=k xi. Recovering both with success>=2/3 requires k>=1/(3xi).
A merely positive binary-encoded margin is not enough for efficient
learning; the integer R<p promise supplies an inverse-polynomial margin.

The endpoint ambiguity example has full support when n=1, but not when
n>1. Do not claim exact endpoint nonidentifiability for every full-support
n>1 source: its top-eigenvalue multiplicity is then below p. There is still
no uniform copy guarantee at the endpoint even WITH strict full support.
For d=p^n, n>1, use

    w=(1-s-t)u_line+s u_all+t delta_0,
    t=s(1/p-1/d)/(1-1/p),

with arbitrarily small s>0. All weights are positive and the maximum is
exactly1/p. The line and maximally mixed parts are unchanged by adding
x_1^2 to F; the source distance is at most t. Constant-success recovery
therefore requires Omega(1/t) copies.

Near this boundary, the R^-5 purity-loss order cannot be replaced by the
R^-3 bound available when p>2R. For p=2m+1, R=p-1, set

    h_j=m-min(j,p-j),
    w_j=1/p+(h_j-m^2/p)/(R m(m+1)).

All p weights are positive, max w_j=1/R, and the shift-one loss is
1/[R^2 m(m+1)^2]=Theta(R^-5). Tests retain this full-support countercontrol.

### Measuring away information is a real failure, not just a weak statistic

At p=5, take scalar phase-error weights

    w_j=(1+(2/3)cos(2pi j/5))/5.

They are all positive, sum to one, and have maximum1/3, so R=3<p.
Their additive Fourier support is {0,+1,-1}, with nonzero coefficients
1,1/3,1/3. Every nonzero four-component coefficient vector satisfying
sum a_i=sum a_i^2=0 is a permutation of (1,2,3,4). If a coefficient t
repeated, the other two would have discriminant2t^2, a nonsquare unless
all coefficients vanish. Four distinct residues summing to zero omit0.

For E=sum a_i b_i, each nonzero Fourier coefficient is therefore a product
over all four nonzero frequencies and vanishes. E is EXACTLY uniform.
The measured regression law (y,Ay+E) is independent of the scalar A:
NO classical postprocessing of any number of these outcomes can recover it.
Keeping all measured mu_i does not help; they are jointly uniform and
independent of E. This holds for every allowed coefficient choice in
this four-copy instrument, not for every possible quantum measurement.

The original quantum sources do differ. For a nonzero residual shift t,
their purity-verifier loss is (2/45)(1-cos(2pi t/5)), bounded below by
(5-sqrt(5))/90. Paid verification retains information that the classical
output discarded. For n>1 a product noise distribution can give full
support while retaining a uniform first coordinate in E; the same
obstruction hides the (1,1) Hessian entry. This does not contradict the
classical direct-regression baseline in the linked source audit: the
instrument's convolution noise no longer has that baseline's peak promise.

Do not replace phase diagonality by high fidelity. For example the equal
mixture of |psi_0> and |psi_(x^2)> over F_5 has fidelity >1/2 with both
nonlinearly inequivalent states. A designated F cannot be identified from
that input under an arbitrary-fidelity promise alone.

Global depolarizing noise is covered when its surviving phase component
meets the peak promise. Constant independent per-coordinate noise usually
gives an exponentially small largest label weight, so is NOT automatically
covered. For degree>2, arbitrary Pauli X errors do not generally reduce to
linear phase errors. No ordinary-LWE conversion follows.

## Executed scope

    python qsearch.py phase-copy-baseline --peaked-noise --write
    python -m pytest -q tests/test_peaked_phase_source.py

The report uses a compressed exact spectrum of rank101^40 with one
weight1/3; it does not enumerate the space or claim to learn that spectrum.
Tests check strict threshold/rank bounds, bad-grid events, degeneracies,
full-rank density matrices, the peak/margin obstructions, target-copy and
SWAP budgets. No quantum learner, native classical-input reduction or
speedup claim is promoted by these controls.

The general core uses published antisymmetrization and diagonal-equation
phase elimination; attribution is retained in the linked earlier notes.
Independent proof and primary-literature reviews must be kept separate
from execution or novelty certification.

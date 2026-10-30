# Exterior-Square Probes Recover Low-Rank Hidden Singular Spaces

27 October 2026. Proposed quantum oracle algorithm, not a natural-input
speedup, novelty certificate, hardware execution, or human-reviewed result.
The finite reference controls are supplementary to the argument below.

## 1. Scientific Question And Input

The existing orthogonal receiver recovers a hidden totally singular U only
when its unknown dimension k is at least three. Its three-functionals
reconstruction genuinely fails at k=1,2. Can a different public additive
probe recover these ranks, without hidden coordinates or rank advice?

Let V=F_q^n + F_q^n, Q(x,y)=x.y, with q odd, n>=3 and an effective finite
field presentation. The ordinary coherent fixed-width oracle on either
O^+(2n,q) or SO^+(2n,q) obeys

    f(g)=f(h) iff g^-1 h belongs to Stab_G(U),

for an unknown NONZERO totally singular U. The FULL stabilizer promise is
essential. Output a basis of U. No vector-membership oracle, basis of U,
hidden rank, or oracle extension to GL is supplied.

**Proposed theorem:** for 1<=k<=n-2, the exterior receiver below succeeds in
poly(n,log q,label width,log(1/epsilon)) time. For k=n-1,n its exact-kernel
version produces no informative probe and fails explicitly, rather than
returning an incorrect subspace. Combining it with the previously reviewed
k>=3 receiver covers ALL 1<=k<=n when n>=4, without knowing k.
This does not settle n=2, the remaining n=3/k=2 case, characteristic two,
nonsplit forms, flags, or arbitrary hidden subgroups.

## 2. Probe Kernel And An Observable Good-Probe Screen

Sample a public maximal totally singular R, and compute a Witt complement
R*. In these coordinates let

    T_A(x,y)=(x+A y,y),    A^T=-A.

Then T_A T_B=T_(A+B), the parameter map is injective, and all T_A lie in
SO. Conjugating by a publicly computed Witt frame does not change this
determinant, even if that frame itself has determinant -1. The additive
domain has dimension a=n(n-1)/2 over F_q. Restrict the SAME original oracle
to this domain and learn its linear hidden kernel by abelian HSP.

Write X=U intersect R and Y=projection_(R*) U. Since T_A-I has square zero,
the actual kernel is exactly

    K_R={A alternating: A Y is contained in X}.

This is an F_q-linear space, not merely a set of successful membership
tests. Compute its image support

    W_R=sum_(A in a linear basis of K_R) image(A), embedded in R.

There are three cases:

* X is nonzero: W_R=R.
* X=0 and d=n-k>=2: K_R=exterior_square(Y^ann), and
  W_R=Y^ann=R intersect U^perp has dimension d.
* X=0 and d<=1: K_R=0 and W_R=0.

For the first case, isotropy gives X subset Y^ann. Every rank-two
alternating map x wedge v, with x in X and v in R, sends Y into X; hence
X wedge R is contained in K_R. Fixing any nonzero x, the images of these
maps span all R. For X=0, choose coordinates with Y a coordinate space:
all its rows and columns in an allowed alternating matrix vanish. The
remaining matrices are exactly exterior_square(Y^ann). Their images span
Y^ann precisely when its dimension is at least two.

Thus a NONZERO PROPER support W_R is a public screen for a disjoint probe
R intersect U=0 in the theorem's rank range. It also reveals k=n-d. Neither
test needs U as input. Bad intersecting probes are identifiable and safely
discarded. The two high ranks are an explicit blind boundary of this probe,
not a failure of the existing higher-rank algorithm.

## 3. Uniform Maximal-Space Sampling Is Paid

Sample over BOTH families of maximal singular spaces. Fix the public
coordinate maximal E. The cell with j=dim(R intersect E) has

    [n choose j]_q * q^((n-j)(n-j-1)/2)

members. Choose j with these integer weights, choose a uniform j-space
X in E by uniform independent rows, and complete its basis publicly.
Modulo X, all possible R are graphs of alternating (n-j)-square matrices
from the complementary dual space to E/X. Choose their independent entries
uniformly. This is a bijective parameterization: no rejection proportional
to 1/q is needed. The total weight is 2 product_(i=1..n-1)(q^i+1).
Computing weights and sampling their O(n^2 log q)-bit tickets is polynomial.

The implementation caps both row trials and random-integer rejection.
Couple it to the uncapped uniform sampler; the total abort/distribution
error is bounded in Section 5. Conditioning the capped sampler on success
is NOT silently asserted to be exactly uniform across different cells.
The seeded PRNG used for finite replay is not a proof of uniform randomness.

## 4. Constant-Probability Spanning, Including Hidden Rank One

A fixed singular line belongs to a uniform maximal R with probability
1/(q^(n-1)+1). A union bound over lines in U gives

    Pr[R intersects U nontrivially]
      <= (q^k-1)/[(q-1)(q^(n-1)+1)] < 1/[q(q-1)] <=1/6

for k<=n-2. Thus good probes have probability at least 5/6.

Conditional on goodness, W_R is uniform among the d=n-k dimensional
singular subspaces of U^perp that are disjoint from U and project to a
maximal singular space M of the split quotient U^perp/U. To see uniformity,
each such W has the same number q^(k(k-1)/2) of good extensions R: in the
split 2k-space W^perp/W, these are the maximal spaces complementary to the
image of U. Every maximal M has exactly q^(kd) lifts W, all graphs of
linear maps from M to U. Both maximal families are retained.

For any proper hyperplane H of U^perp, let ell define it.

* If ell is nonzero on U, a uniform lift M->U makes ell|W a uniform
  functional on M. Thus Pr[W subset H | good]=q^(-d)<=1/9.
* Otherwise ell descends to a nonzero functional on U^perp/U, represented
  by a vector v under its nondegenerate polar form. Since M=M^perp in
  that quotient, W subset H iff v belongs to M. This has probability zero
  for nonsingular v, and 1/(q^(d-1)+1)<=1/4 for singular nonzero v.

Consequently any incomplete accumulated subspace S of U^perp grows on
one public probe with probability at least (5/6)(3/4)=5/8: choose any
hyperplane of U^perp containing S. There is no dependence on an unknown
mixing time or a rare oracle-label collision.

The first good support determines k. Accumulate good W_R until their span
has dimension 2n-k, then return its polar orthogonal. With exact kernels,
all accumulated vectors lie in U^perp, so this stopping rule returns U.
Before the first good probe the same growth bound applies to S=0.

## 5. Bounded Clock And Error Accounting

Choose L with 2n(3/8)^L<=epsilon/4 and use T=2nL probes. Divide this clock
conceptually into 2n blocks of L probes. While incomplete, a block fails
to increase dimension with probability at most (3/8)^L. At most 2n-1
increases are needed, giving the stated union bound. No actual hidden rank
is needed to allocate this clock.

For each probe use m=a+s independent additive Fourier samples, with

    T/[(q-1)q^s] <= epsilon/4.

This bounds every annihilator rank failure by the hyperplane union bound.
For extension fields use trace characters and a public field basis/dual
basis. The annihilator is F_q-linear, so F_q spans recover it. The prime-
field reference code does NOT implement extension-field arithmetic.

The total original oracle calls are at most T*m, one per quantum Fourier
sample. Reversibly compute the public g_A from A, query f once, and
uncompute g_A and its deterministic workspace using A. Retain or discard
the oracle-label register, then Fourier-transform A. Do NOT erase unknown
labels for free or leave an injective g_A register entangled with A.

Choose complete-instrument approximation error delta=epsilon/(4Tm) per
sample. Here error means operational total variation from the ideal sample
instrument, uniformly over allowed inputs and classical histories; a
half-diamond-distance bound including an arbitrary reference is a stronger
sufficient condition. It is NOT per-entry or per-amplitude precision.
Include preparation, transform, arithmetic and workspace cleanup in that
whole-instrument target. The ordinary oracle is exact under the input
promise; a noisy oracle would need an additional budget. A hybrid argument
coupled to the ideal adaptive process bounds the sum by epsilon/4. Public
matrix arithmetic and reversible compilation are polynomial. Do not assume
that conditioning on all learners being correct preserves the probe law.

For the classical maximal-space sampler, cap each independent-row trial
at b with T*n*q^(-b)<=epsilon/8. A trial rejects with probability at most
1/q. There are at most C=T[1+n^2 b+a] uniform integer requests. Cap their
bit-rejection attempts at h with C*2^(-h)<=epsilon/8. Couple to ideal
uncapped draws. The two sampler failure contributions total at most
epsilon/4. All caps and bit widths are polynomial in the input/error size.

**Important difference from the earlier receiver:** an undersampled kernel
is a superspace of K_R, but its image support can be a proper subspace of
R containing vectors OUTSIDE U^perp. The screen alone is not an equality
certificate. Every rank failure must be charged; the regression suite
includes this concrete counterexample. There is no claim of zero-error
soundness under arbitrary incomplete or malformed learner outputs.

## 6. Combining Receivers Without Rank Advice

For n>=4 run this low-rank receiver, then the existing general-rank receiver
if the first returns no candidate. Split total error between the routines.
If k<=n-2, this receiver succeeds with the stated bound. If k=n-1 or n,
every exact exterior probe has full or zero support and is rejected; the
existing k>=3 receiver then succeeds. Its containment proof applies to
every nonzero hidden U; its old rank/probe gates cannot incorrectly accept
k=1 or2 with exact kernels. Approximation and rank failures of both calls
are included in the total budget. This is a mathematical composition, not
a claim that a combined CLI or compiled quantum circuit has been built.

## 7. Classical Baselines, Literature And Falsifiers

The SAME ordinary oracle permits classical full-table additive-kernel
learning, costing q^a calls per probe; that is exactly what the dense
reference uses to simulate Fourier distributions. The existing reflection
attack on O uses O(n q^k) expected original queries when k<n. Its hit
probability is (q^(n-k)-1)/(q^n-1); at fixed q and small k it is polynomial.
Those reflections have determinant -1 and are not individual legal queries
on SO. These are UPPER bounds, not a proof that a better classical method
cannot match the new receiver at every rank.

The separate CLASSICAL_COMPARATOR.md gives a proposed uniform fixed-line
bound and adaptive-label coupling: hidden LINES require Omega(sqrt(q))
classical queries in the same opaque oracle model. If both arguments hold,
this gives an exponential-in-log(q) oracle separation already at fixed
n>=3. No comparable bound is supplied here for all other ranks. No
cryptanalytic, code-equivalence or other natural hard input has been reduced
to the full-stabilizer oracle. Do not advertise an oracle separation as a
Shor-level result or a new generic HSP mechanism.

The closest inspected primary comparisons remain
[Decker et al., 2014](https://arxiv.org/html/1406.6511v1), whose theorem is
for GL over finite fields, and [Imran, 2026](https://arxiv.org/html/2610.28368v2),
whose Theorem1.1 is for GL over finite chain rings. Additive probes and
subspace reconstruction are established ideas. Those GL contracts do not
by themselves extend our oracle outside O/SO. A bounded search did not
establish whether this specific exterior-support construction is already
known; absence of a search hit is NOT novelty evidence.

Decisive falsifiers are an admissible U,R violating the kernel/support
screen, unequal good-extension multiplicities, a hyperplane violating the
escape bound, an uncharged source/precision assumption, or an existing
paid reduction that already solves this exact contract. A classical
poly(n,log q) algorithm for the SAME opaque oracle would remove the
speedup motivation without refuting the quantum construction.

## 8. Implementation Scope And Next Decision

exterior_probe.py supplies public prime-field probes, a capped maximal-
space sampler, an opaque-oracle dense reference controller and a resource
ledger. exterior_controls.py alone accesses the hidden subspace to build/check
fixtures. Native controller arguments contain no hidden U or k. Tests
exhaust finite fibers, support classifications, extension multiplicities,
hyperplane counts and the undersampling failure; large-prime tests check
only supplied-secret algebra, NOT a scalable learner.

One independent AI mathematical review found no fatal defect in the receiver
or line-only lower bound. Read REVIEW_RESPONSE.md and VERIFICATION.md for
scope and evidence; this is not human review or a code audit. The next
scientific question is exact prior-art subsumption
or a useful native-input reduction for this receiver, not more field/ring/
flag variants or sharper constants in its line-query bound. The main Rees
theorem still awaits human correctness/novelty assessment. Nothing here
authorizes external contact.

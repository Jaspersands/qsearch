# Fixed-degree Legendre reconstruction by resultant hyperplanes

2026-11-05. Independently reviewed written derivation; finite source
falsifiers completed. No quantum execution, novelty, speedup,
separation or classical-hardness claim. The theorem below is for fixed degree
and sufficiently large primes, not uniform polynomial dependence on degree.

## Scientific contract and selection

Problem: recover an unknown monic irreducible Q in F_p[X] of fixed degree
d>=2, with p growing, from fresh pure tensor copies
|f_Q>=p^(-1/2) sum_x chi(Q(x))|x>. A BIT oracle or an uncontrolled raw
phase oracle can supply each copy with one native query. No extension-field
oracle, inverse source preparation, controlled unknown unitary, or target
root is supplied. Output the d coefficients, with error at most eta.

The mechanism is an abelian Fourier measurement on coefficient vectors of
publicly factorable polynomials. Its native state has constant overlap with
a VIRTUAL norm-character state whose Fourier support is the unknown
hyperplane Q-perp. Constant-dimensional outlier-tolerant linear algebra and
fresh-copy verification complete reconstruction. Expected resource target:
C_d poly(log p,log(1/eta)) gates and copies; C_d can grow factorially or worse.
This is a polynomial quantum upper bound, not a proved asymptotic separation.

Portfolio check: interleaved OPI was already investigated in
PRIME_CHARACTER_INTERLEAVED_PROBE.md and PRIME_CHARACTER_PHASE_FEEDBACK.md;
the support-coherence operation remains unpaid. Existing quadratic GL2
reconstruction is written and reviewed. Cubic reconstruction has independent
cryptographic motivation and tests a genuinely different operation. Orbital
Fourier formulas for binary cubics motivated coefficient coordinates but
are NOT a needed source theorem or an implementation of the resultant kernel.

Prior-work lookup: corpus searches for cubic character reconstruction,
central coefficient windows and resultant/Fourier hyperplanes found no exact
match; these noisy lookups do not establish novelty. Primary comparisons:
Russell--Shparlinski, quant-ph/0212016, Theorem 6 gives O(d) quantum QUERY
complexity through a POVM; it does not implement this coefficient readout.
Ivanyos et al., arXiv:1502.06631, Section 3 uses classical oracle access and
Grover search with e^(d/2) time, not this coherent native source. KKK 2020
Section 4 gives the full-table cubic collision comparator. Local sources are
under audits/sources/legendre_prf/. A broader priority review remains open.

Strongest current native cubic comparator: the companion central-window
derivation proves p-query O(M(p)log p+p) field-operation reconstruction
for all p>=23; the independent reviewer accepted its gap/degree proof. Its finite control already
refutes universal rank-three at p=13. For quadratics retain the reviewed
expected sqrt(p) classical attack. Neither is a lower bound. Full-table
interpolation is paid; the quantum receiver below never reads that table.

Decisive falsifiers: wrong resultant sign/scaling; lost root-permutation
coherence; unavailable clean root erasure; nonflat virtual Fourier spectrum;
overlap insufficient to escape every proper subspace; uncharged rejects;
wrong candidate verification; indistinguishable small-prime inputs. No
claim is inferred from finite controls.

## 1. The native split-polynomial state

Let V=F_p^(d+1), with ascending coefficient vectors for degree<=d polynomials.
Take d fresh copies and project onto pairwise distinct finite x_i. Success is
alpha=(p)_d/p^d. Map the ordered tuple reversibly to (sorted roots, permutation
rank). The phase product is symmetric; conditional on distinctness the
permutation register is exactly uniform on S_d and independent of the sorted
roots. Unprepare that known uniform register. Do not discard sorting garbage.

Append a uniform nonzero a with the PUBLIC phase chi(a)^d. Form
R=a product_i(X-x_i). Reversibly erase its canonical sorted roots using a
public split-polynomial factorization procedure (Section 4). This gives

 S_Q = N^(-1/2) sum_{R in S} chi(a)^d product_i chi(Q(x_i)) |R>,
 N=(p-1) binom(p,d),

where S consists of squarefree, completely split polynomials of exact degree
d with nonzero leading coefficient. The resultant identity is

 Res(Q,R)=(-1)^(d*d) a^d product_i Q(x_i).

Thus S_Q agrees up to the SINGLE global sign chi(-1)^d with the restriction
of R -> chi(Res(Q,R)). The public scalar phase is essential for odd d.
Distinctness rejection consumes the original copies; failed copies are never
reused. One successful/failed Fourier attempt consumes exactly d copies.

## 2. A virtual flat-spectrum state

Only for the proof, let E=F_p[X]/(Q), theta=X mod Q, and L_Q(R)=R(theta).
This is a surjective F_p-linear map V->E with kernel span(Q). Since Q is
monic, Res(Q,R)=Norm_E/Fp(R(theta)). Consequently chi composed with Norm is
the nontrivial quadratic character chi_E of E. No evaluation at theta is an
algorithmic operation.

Define the normalized virtual state

 N_Q = [p(p^d-1)]^(-1/2) sum_{R in V} chi_E(L_Q(R)) |R>.

Each nonzero element of E has p preimages. The additive Fourier transform
on V of N_Q vanishes off H=span(Q)^perp and at zero. For every nonzero
y in H, it has absolute amplitude 1/sqrt(p^d-1). Indeed characters trivial
on ker L_Q descend to additive characters of E; every nontrivial one has
quadratic Gauss sum of absolute value p^(d/2). The p-to-one fibers and the
unitary Fourier normalization give the stated amplitude. The unknown Gauss
phases are never computed or cancelled.

Because no split R shares an irreducible degree-d factor with Q,

 |<N_Q,S_Q>|^2 = delta = N/[p(p^d-1)].

This overlap tends to 1/d!, uniformly in Q, for fixed d and p growing.

## 3. Reconstruction despite Fourier outliers

For EVERY proper linear subspace W of H, flatness implies

 ||Pi_W F N_Q||^2 <= (p^(d-1)-1)/(p^d-1) < 1/p.

Decompose the overlap into W and H\W and use Cauchy--Schwarz. Therefore

 Pr_{F S_Q}[y in H\W] >=
 [sqrt(delta)-sqrt((p^(d-1)-1)/(p^d-1))]_+^2.

In particular this bound is uniform over the span of all previously drawn
genuine independent samples. This is not an inference from total inlier
mass alone. A block of d fresh Fourier attempts has probability at least

 q(p,d) = [alpha * (sqrt(delta)-1/sqrt(p))_+^2]^d

of producing d independent vectors in H, including all distinctness flags.
The decoder does not need to identify inliers in advance: solve the d by
d+1 system for each block. Abort that block unless rank is d, the kernel
line has nonzero last coordinate, and its monic representative is irreducible
of degree d. On the all-genuine event this representative is exactly Q.

A convenient sufficient threshold is

 P_d=max{d(d-1),16 d!,16(2d-1)^2}.

For p>=P_d, alpha>=1/2, delta>=1/(4d!), each conditional escape probability
is at least 1/(16d!), and q(p,d)>=q0=(32d!)^(-d). These conservative constants
are not performance estimates. Small primes below this fixed-degree
threshold are OUTSIDE the stated theorem. Some small inputs are not
identifiable at all (e.g. degree3 at p5 has 40 irreducibles but only 32 sign
tables); do not assert a universal brute-force fallback.

## 4. Paid clean coefficient encoding

One option is bounded-error canonical finite-field factoring followed by
compute/copy/uncompute. A simpler global-seed construction is available.
Choose L=ceil(log2(8p^2/eta)) independent uniform shifts t_j in F_p. For any
r!=s, the trit pair chi(r+t),chi(s+t) agrees for exactly (p-3)/2 choices of
t, so all L signatures coincide with probability at most 2^(-L).
A union bound makes all p signatures distinct with failure at most eta/16.

On this one good PUBLIC seed event, split EVERY squarefree split R by gcds
with X+t_j and (X+t_j)^((p-1)/2) +/-1, reducing modulo each current factor.
Every final factor is linear; extract its root and sort canonically. Only
O(dL) current factors/operations of bounded polynomial degree are needed.
There is no table of p signatures and no supplied advice about Q. The same
polynomial-size reversible circuit correctly factors every supported R, so
inverse coefficient encoding erases the original roots coherently. On bad
seeds the total algorithm may fail; their probability is charged globally.
Sample each shift using ceil(log2 p) fair bits, rejecting values >=p, with
J=ceil(log2(8L/eta)) attempts per shift. Each cap fails with probability
<=2^(-J); their union costs at most eta/8. Conditional on no ABORT the
accepted shifts are still IID uniform. The irreducibility check is polynomial in
d log p using X^(p^d) mod Q and the usual proper-divisor gcd tests.

## 5. Verification, precision and bounded retries

For distinct monic irreducible degree-d Q,Q', Weil's bound gives

 |<f_Q',f_Q>| <= (2d-1)/sqrt(p) <= 1/4  for p>=P_d.

Prepare the PUBLIC known-candidate phase state and project a fresh unknown
copy onto it. True candidates pass with probability one ideally; false ones
pass with probability at most 1/16. This uses neither unknown preparation
inverses nor classical values supplied for free. BIT access can alternatively
verify by fresh uniform original-domain queries, with its own agreement bound.

All arithmetic, sorting and seed-based root cleanup are exact logical
circuits on the good seed event. Approximate uniform states and F_p QFTs
are synthesized with total per-block operator error <=q0/8, which implies
per-block event error <=q0/4. Thus true
candidate probability is at least q0/2. Choose

 R=ceil((4/q0) ln(4/eta)),
 K=ceil(ln(4R/eta)/ln(8)).

Require per-verification-test event error <=min{1/16,1/(4K)}. A false
candidate passes all K fresh tests with probability <=(1/8)^K; a true
candidate passes with probability >=3/4. Hence each block yields an accepted
true candidate with probability >=q0/4, and missing all R costs <=eta/4.
A union bound over false acceptances costs <=eta/4. Public seeds and capped
samplers can each be given eta/8; total is below eta. Use the same good-seed
conditioning for every block, not a fresh hidden assumption per sample.

Uniform public interval states use reversible binary prefix-count rotations:
the two child probabilities are the numbers of admissible labels below
each child prefix divided by the parent's count. Counts and the required
rotation angles are computable in poly(log p,log(1/epsilon)) time. This
handles a in F_p^*, uniform F_p states and the fixed-size permutation rank
without uncharged postselection. For prime-modulus Fourier transforms use
Kitaev, quant-ph/9511026, Section 5, equations (22)-(25), Theorems 1-2 and
the operator-norm convention in Section 2.4.2. To obtain Fourier operator
error epsilon, its coherent eigenvalue readout can use error O(epsilon^2/p)
in Theorem 2; the logarithm of its inverse is O(log p+log(1/epsilon)).
Controlled cyclic powers are ordinary public modular additions. Fourier
state preparation T_q uses the same public interval state and additive
phases; Q_q^(-1) erases its original label. This explicitly pays a uniform
approximate Fourier circuit, not an assumed exact prime-dimensional gate.
The local primary text is audits/sources/legendre_prf/kitaev_abelian_9511026.txt.
Allocate the summed preparation/transform error over all calls in a block
to q0/8, and over each known-candidate projector to half its stated event
budget. Invalid binary padding is included in the approximation error or
returns ABORT; it is never silently reinterpreted as a field element.

Copy cap R(d^2+K). The precision logs, seed length, arithmetic, coefficient
encoding, d+1 abelian transforms and linear algebra all cost
C_d poly(log p,log(1/eta)). Fresh tensor-power inputs are essential. No
extension to correlated banks, noisy sources or growing-degree efficiency
has been proved here.

## Reviewed squarefree extension and updated classical source

LEGENDRE_SQUAREFREE_RESULTANT_READOUT.md extends the paid receiver to every
monic squarefree polynomial of each fixed degree, for sufficiently large
primes, with lambda(0)=+1 phase copies and no root indicator. The original
irreducible theorem above retains its own sharper support and constants.
The extension uses a virtual product algebra; its Fourier support is NOT
all nonzero Q-perp. It includes a p11 padded collision excluding any
unqualified small-prime fallback.

The later primary-source audit found Kopparty, arXiv:2601.07137, Algorithm A
and Theorem 3.1: a full-table poly(p) classical decoder, with constant-error
tolerance and growing-degree scope. It reads all p original values; it is
not a poly(logp) native attack. Padded roots count as errors. The scoped
source/reduction review records its proved constants and why arbitrary IID
OPI halfsets do not inherit its structured character-fiber decoder. The
quasilinear cubic and expected-sqrt(p) quadratic comparators remain valid.

## Review and experimental status

- Independent proof review: audits/reviews/2026-11-05-resultant-hyperplane-review.md
  accepts the core fixed-degree theorem, clean encoding and rank-growth
  proof; its resource addendum checks the explicit retry/error allocation.
- Prespecified finite control: (p,d)=(5,2),(7,3), every irreducible Q;
  classical_baselines/resultant_hyperplane_control.py/.json completed for
  all 10 and 112 secrets. Native phases, virtual Fourier support/flatness,
  overlap and all 60/6384 proper-hyperplane checks pass. Minimum inlier mass
  is .36/.1510204; minimum escape is .232/.1037901. The cubic lower bound
  at p7 is vacuous. Retaining injective root/scalar labels gives uniform
  Fourier output with inlier mass 1/p; omitting chi(a)^3 kills the cubic
  overlap. Exact Sage field algebra and floating normalized NumPy FFT;
  maximum virtual flatness residual <3.5e-17. No coherent factoring or
  quantum circuit is executed, and no asymptotic theorem follows from this.
- Classical window proof/control: audits/reviews/2026-11-05-cubic-character-window-review.md
  and classical_baselines/cubic_character_window_control.py/.json.
- The independent reviewer also accepted the cubic central-window proof:
  a long coefficient gap propagates through a first-order recurrence, and
  a low-degree Wronskian contradiction forces rank three for every p>=23.
  The p13 exceptions do not contradict that threshold theorem.
- Next hard question: is there a poly(log p) classical reconstruction on the
  ORIGINAL character-only oracle, or a known theorem covering this exact
  coefficient-space measurement? Require a new operation before new attack
  sweeps. Re-rank independent high-upside directions before extending degree
  or source promises. Broader prior-art review is required before novelty.

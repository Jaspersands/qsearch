# Sparse Fock learning: a moment-blind torus completion

REVIEWED QUANTITATIVE FALSIFIER; exact control complete (7 November2026).
No general learning impossibility, novelty, hardness or quantum execution.

## Selection and candidate contract

The externally motivated question is whether learning the complete
quadratic stabilizer and completing its maximal torus supplies the missing
Gaussian basis for GENERAL polynomial-sparse Fock-state learning. The
two-branch learner is complete; merely extending its tensor backend is not
the task. Here the proposed operation is a different explicit one: acquire
all second/fourth Majorana means, form the centered quadratic-Hamiltonian
variance Gram matrix, extract its null Lie algebra, diagonalize a maximal
commuting torus, and use known-basis sparse tomography in a completion.

Native input: exact IID copies of parity-definite G sum_(j=1..r)alpha_j|x_j>,
unknown even Gaussian G, known physical Majoranas, unknown Fock support,
r=poly(n). Output an epsilon-close preparation in poly(n,r,1/epsilon)
time/copies. No input basis, inverse, branch weights or exact moment advice.
Granting EXACT moments below strengthens the failed proposal. Acquisition
uses O(n^4) bounded observables and polynomial copies at inverse-polynomial
accuracy. Classical linear algebra and compact Lie algebra operations are
the proposed mechanism; the desired gain is over general exponential
tomography, not a classical-input computational separation.

The diagonal stabilizer in the true frame has dimension at least n-r+1:
each of r-1 occupation differences imposes one linear equation on diagonal
quadratic coefficients. The unpaid claim was that a maximal-torus
completion preserves polynomial approximate support, or leaves only
O(log r) modes requiring tomography. The cheapest tests are a constant-gap
moment-blind family and an APPROXIMATE sparsity bound. Exact support
proliferation alone would be insufficient for approximate learning.

Classical baselines: covariance Gaussian compression, fixed-compressibility
learning, and supplied-description sums of r Slater determinants/Pfaffians.
The first cannot discard even one mode on the family below; the latter
efficiently simulates its supplied finite control but does not infer the
unknown basis from copies. No quantum construction was built.

Independent comparison also considered a full classical attack on sparse
characteristic-zero relation lattices. Small cyclotomic specialization plus
the existing Alg lattice and finite-algebra relation interface is concrete
IF a good root of polynomial degree is found. Actual CIT source only tests
a specified root; it does not pay that existence/search bound. No new OPI
decoder emerged. The torus operation was selected for a decisive test of
the broader native learning problem, not for another two-branch variant.

## An explicit polynomial-sparse family

Let n=p>=11 be prime, p=3 mod4, D the nonzero quadratic residues modulo p,
w=(p-1)/2 and lambda=(p-3)/4. Define

    psi = (1/sqrt(n)) sum_(a in Z_p) |D+a>.

It has r=n distinct equal-weight Fock branches, fixed particle number w
and hence fixed parity. Every passive Gaussian U gives another input in
the SAME unknown-Gaussian sparse class. No preparing circuit is supplied.

The Paley character identity gives |D intersect(D+h)|=lambda for h!=0.
One can derive it by expanding (1+chi(x)-1_(x=0))/2 twice, using
sum_x chi(x)chi(x-h)=-1 and chi(-h)=-chi(h). Thus the support distance is
2(w-lambda)=(n+1)/2>=6. The translate incidence matrix A obeys

    A A^T=(w-lambda)I+lambda 11^T.

It is nonsingular and its rows affinely span the constant-weight hyperplane.
Each coordinate is occupied in w branches, each pair in lambda branches.
This is a standard Paley difference set, not a new construction; actual
primary Section4.2 is retained under `audits/sources/sparse_fock_torus/`.

## Complete low-degree data and the stabilizer

Off-diagonal branch matrix elements of Majorana degree<=4 vanish by the
distance. The one-particle RDM is (w/n)I; the two-particle RDM is
w(w-1)/[n(n-1)] times the identity on exterior² C^n, with increasing-pair
indexing. Number-changing means vanish. These equal the RDMs of the
maximally mixed w-particle sector. Normal ordering determines ALL second
and fourth Majorana means, so these data are invariant under EVERY passive
U(n). This is exact, not small signal or a finite observation.

Equivalently use J with standard 2x2 skew blocks, covariance convention
C_ab=i<gamma_a gamma_b>, and T_abcd=-<gamma_a gamma_b gamma_c gamma_d>.
Then

    C=-J/n,       T=-W(J)/n,
    W(J)_abcd=Jab Jcd-Jac Jbd+Jad Jbc.

In pair coordinates v=(Jab)_(a<b), the centered Gram of Hermitian bilinears
P_ab=i gamma_a gamma_b is

    V=I-L_J/n-vv^T/n²,   L_J(X)=<J,X>J+JXJ.

Its spectrum is EXACTLY

    0 (multiplicity1),
    (n+1)/n (multiplicity n²-1),
    (n-1)/n (multiplicity n(n-1)).

The zero direction is total particle number minus its scalar offset. In
particular the nonzero gap is >=10/11 and all original weights are1/n.
No amplitude threshold, precision improvement or more low-degree samples
can resolve the missing frame.

A direct stabilizer proof is useful independently of that spectrum. A
general quadratic H contains hopping, pairing and diagonal terms. Every
off-diagonal term changes two occupations. Such an output cannot equal
an original support word or an output from another support word, by
distance>=6. For each pair the design supplies a branch enabling the
hopping/pairing term, so zero variance forces each coefficient to zero.
The remaining condition A h=c1 forces h constant. The COMPLETE compact
quadratic ray-stabilizer Lie algebra is therefore just u(1), generated by N.
Its maximal torus has n equal frequency pairs. Compatible orbital frames
are all passive U(n), with none selected by the measured moments.

## Quantitative approximate-sparsity failure

Let d=binom(n,w). For ANY fixed unit vector phi in exterior^w C^n, Haar
U in U(n), and occupation probabilities p_S(U)=|<S|U phi>|², write

    d2=d²(n+1)/[(w+1)(n-w+1)].

The Slater ray |S> is a highest-weight coherent state. Its tensor square
belongs to the single Cartan-product irrep of highest weight2 omega_w,
partition(2^w), of dimension d2. Schur twirling gives

    integral (U†|S><S|U)^tensor2 dU = Pi_(2 omega_w)/d2.

The central U(1) only gives a global phase, so SU(n) and U(n) give the same
projector integral. This is precisely the known Sugita SectionIII
equations14--16; the rectangular dimension follows from SectionIV(ii),
equation31 at q=2. It is NOT a new Haar-moment theorem. Consequently

    E_U sum_S p_S(U)²
      = (d/d2)||Pi_(2 omega_w) phi^tensor2||² <= d/d2.

For every subset A of at most R strings, its probability mass squared is
<= R sum_S p_S². The inequality holds simultaneously for ALL A, even
when A is selected after observing U. Markov therefore proves

    Pr_U[max_(|A|<=R) sum_(S in A)p_S >=1-epsilon²]
      <= min(1, R d/[d2(1-epsilon²)²]).

For a jointly U-independent list of L passive frames, use Haar invariance
for each fixed frame and a union bound; multiply the RHS by L. Condition
on the list's randomness first. List entries need not be independent of
one another. At w=(n-1)/2, d/d2=(n+3)/(4d), and d=exp(Omega(n)). Thus
polynomial L and R succeed only with exponentially small probability.
The bound gives the best possible R-sparse approximation in each proposed
frame: squared fidelity is precisely its largest R-coordinate mass.

Every member U psi nevertheless has an EXACT n-sparse description in
its original unknown Gaussian frame. Exact second/fourth means are
identical across U, so any frame list using only those means is independent
of U. The same holds for complete adaptive transcripts when each fresh
copy yields ONE individual +/-1 Majorana-degree2/4 observable outcome:
its Bernoulli law is fixed by the invariant mean. Known Gaussian rotations
of such individual observables preserve the relevant degree.

This rejects the claimed polynomial-list TORUS-COMPATIBLE completion,
including constant-error approximate support, not only exact sparsity.
It does NOT cover joint occupation records on one copy, arbitrary spectral
measurements of a quadratic sum, arbitrary low-QUBIT-weight observables,
higher Majorana degree, unrestricted non-passive frame choices, coherent
multi-copy processing, or a full learner allowed those additional data.
In particular a known-basis learner may use higher-degree phase data;
the obstruction is choosing a useful basis from the specified means alone.

## Gaussian compression does not supply an alternative endpoint

All covariance singular values are1/n. Any state having even one pure
Gaussian mode factor has some norm-one rotated Majorana bilinear of mean
+/-1. The input's expectation of that same operator has magnitude<=1/n.
By the trace-distance observable bound, their distance is at least
(1-1/n)/2. Hence constant-error compression to O(log r) active modes
cannot replace the unpaid frame choice. The original sparse completion
still exists; no contradiction or general hardness follows.

## Independent arithmetic screen: an unresolved existence bound

For the native sparse characteristic-zero field/units, a small cyclotomic
specialization preserving denominators and unit norms would inject every
algebraic constant generated by Alg into the finite Q-algebra. Intersecting
the specialized full relations with Alg would then recover FullRel. A
nonzero algebraic constant cannot map to zero under a unital Q-algebra
map: its minimal polynomial has nonzero constant coefficient. At a given
polynomial numerical prime ell this is a paid finite-degree operation;
no discriminant nonvanishing is required for this injection argument.

After injective Kronecker substitution let P be the nonzero denominator/
unit-norm obstruction polynomial, with ||P||1<=H, degP<=D. The retained
note already bounds logH,logD polynomially. Put s=ord_(X=1)P and
Q=P/(X-1)^s. Then

    0<|Q(1)|=|P^(s)(1)/s!|<=H binom(D,s).

If prime ell is bad, Phi_ell divides P, hence divides Q over Z[X], and
ell=Phi_ell(1) divides Q(1). There are at most log2H+s log2D distinct bad
prime orders (use max(1,D) for the constant case). A polynomial bound on s
for THESE native norms would pay a polynomial prime scan. None is proved.

Do not import a general determinant multiplicity bound without its cost:
such a bound would yield deterministic symbolic-determinant PIT. For an
n-by-n affine-linear symbolic matrix, substitute x_i=X^((n+1)^(i-1)).
The determinant's individual variable degrees are<=n, so nonzeroness is
preserved; the sparse entries and binary exponent sizes remain polynomial.
A polynomial bound on ord_1 then allows a polynomial truncated-Taylor test.
This reduction is not an impossibility result and does not automatically
transfer to the narrower multiplication-norm matrices.

Actual Balaji--Perifel--Shirmohammadi--Worrell2007.13179v2 defines monomial
input gates of syntactic degree1 and proves Bounded-CIT in randomized NC
(Theorem2). It tests a SPECIFIED root of unity, not a good one of small
field degree. No tester/backend or additional conditional algorithm is
implemented. FullRel and this existence question remain OPEN.

## Controls, review and next decision

Structural proof: `audits/reviews/2026-11-07-sparse-fock-torus-counterexample.md`.
Actual-source/quantifier review is
`audits/reviews/2026-11-07-sparse-fock-moment-sources.md`; it accepts the
normalization, rectangular dimension, maximum-over-support event and
independent-list quantifiers. The parent read Sugita's actual equations
14--16 and31, the Paley statement, and the CIT definition/Theorem2.
Primary PDFs/text/hashes are under
`audits/sources/sparse_fock_torus/`; previous Sen and compression sources
are reused, not fetched or reinterpreted as new theorems.

The exact p11 control `audits/controls/sparse_fock_torus/control.py` and
`.json` PASSED: full231-dimensional variance spectrum
0^1,(12/11)^120,(10/11)^110; identical low means and full Gram after a
nontrivial passive rotation; overlap43/55, so these are different states.
The occupation triple(0,2,4), a degree<=6 observable, changes from1/11 to
9/275. WeylCharacterRing independently gives Cartan dimension60984,
Hilbert dimension462 and IPR bound1/132. This uses exact classical
Slater/Fock action and Sage algebra, not a quantum construction. No Haar
tail or all-n theorem is inferred from this finite control.

One focused Fable5.1/high Claude audit completed:
`audits/claude_runs/2026-11-07-sparse-fock-torus/`; immutable prompt under
`audits/claude_inputs/2026-11-07-sparse-fock-torus/`. Estimated usage
USD0.596230, end_turn, no retry or pending call. Accepted after checking:
Cartan multiplicity/trace normalization, hook-content dimension, Cauchy--
Schwarz/Markov, and U-independent random-list conditioning. Its statement
that the same bound specifically FAILS for active/Bogoliubov frames is
NOT accepted: the provided argument discusses arbitrary sector vectors
and does not supply a Gaussian-frame counterexample. Such frames remain
outside the proved scope. Suggested Monte Carlo confirmation was omitted;
the exact source/proof and dimension control already resolve the claim.
No source equality characterization is needed here. Agent agreement alone
does not establish novelty, a general lower bound or a speedup.

Decision: reject quadratic-variance/maximal-torus completion as a general
sparse learner. The next pass must independently compare native mechanisms;
do not optimize its eigensolver, run a gap sweep or solve the constructed
counterfamily merely to keep this line active. General sparse learning
needs a paid observable/decoder outside this interface, and the arithmetic
alternative needs a paid good-specialization bound before implementation.

Milestone checks passed: exact current STATE/handoff title, Now/parked row,
all three primary PDF hashes, immutable Claude prompt/context, terminal
usage, review artifacts and exact control false gates. Scoped whitespace
check passed. No full-suite run, unchanged experiment rerun, commit or push.

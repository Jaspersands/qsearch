# Independent review: squarefree resultant reconstruction

2026-11-05. Read the current `research/STATE.md`, `research/TRAPS.md`, and
`audits/sources/legendre_prf/kopparty_noisy_2601_07137.txt`, Theorem 1,
its introduction, Algorithm A, and Theorem 3.1. This is a focused all-parameter proof review, not a finite
scan. No archive, network, Git, registry, or external-service action.

## Verdict and model

ACCEPT the proposed extension of the written resultant-hyperplane algorithm
to every monic SQUAREFREE polynomial of each fixed degree d>=2, including
reducible polynomials, for sufficiently large odd primes p. The source is
fresh exact pure tensor copies of

    |phi_Q> = p^(-1/2) sum_{x in F_p} lambda(Q(x)) |x>,
    lambda(0)=+1, lambda(z)=chi_p(z) for z!=0.

No zero indicator or root locations are supplied. A classical trit oracle
for chi_p(Q(x)) can prepare these padded states coherently. A raw phase
oracle must explicitly mean the padded unitary with phase lambda(Q(x));
chi_p(0)=0 is not a unitary phase. No controlled unknown oracle, source
inverse, extension-field oracle, or factorization of hidden Q is used.

A safe sufficient threshold and ideal all-good block lower bound are

    p >= max{4d^2,128d!,256d^2},
    q0 = (128d!)^(-d).

The first threshold term is redundant but records its role in the proof.
Gate and copy costs are C_d poly(log p,log(1/eta)); no uniform polynomial
in d, small-prime universality, noisy/correlated-source theorem, novelty,
classical hardness, asymptotic separation, or quantum execution is claimed.

## 1. Actual state: no hidden rejection of unknown roots

Take d copies, project only onto distinct input labels, reversibly fold the
ordered tuple to sorted roots plus its uniform independent permutation
register, and unprepare that known register. This projection succeeds with

    alpha=(p)_d/p^d,

because every padded source amplitude has absolute value p^(-1/2), even at
roots of Q. Append the coherent public scalar state with phase chi_p(a)^d,
a in F_p^*, and use the same paid clean split-polynomial coefficient encoding
as in the irreducible proof. There are

    N0=(p-1)binom(p,d)

supported squarefree split degree-d polynomials R=a product_j(X-x_j).
The actual state has constant-magnitude amplitude on ALL these R, with phase

    chi_p(a)^d product_j lambda(Q(x_j)).

In particular, R sharing a rational root with Q remains in the actual state.
It is not detected, discarded, or postselected away. This distinction is
necessary for the stated source model.

Let r be the number of rational roots of Q; r<=d is used only in the proof.
Exactly

    Ngood=(p-1)binom(p-r,d)

supported R are coprime to Q. On these good labels, the phase is, up to the
single Q-independent global sign chi_p(-1)^d, chi_p(Res(Q,R)). On other
labels the virtual state below has zero amplitude, so their padded phases
cause no cancellation in the comparison overlap.

The public-shift clean factorization procedure from the previous review
remains valid without change: it factors the PUBLIC split R, never Q, and
its one good-seed event works simultaneously for every supported R. The
source zeros do not affect its signature separation, seed probability,
reversible workspace cleanup, or bounded sampler costs.

## 2. Virtual finite etale algebra and exact Fourier support

Write Q=product_i Q_i with distinct monic irreducible factors of degrees d_i.
For analysis only,

    A=F_p[X]/(Q) = product_i F_{p^(d_i)},
    U=|A^*|=product_i(p^(d_i)-1).

The evaluation map L:V=F_p^(d+1)->A, R |-> R mod Q, is surjective with
one-dimensional kernel K=span(coeff(Q)). Squarefreeness makes A a product
of fields and its trace pairing nondegenerate. Define

    c(z)=chi_p(Norm_A/Fp(z))=product_i chi_i(z_i),

where every component quadratic character is extended by zero. Thus c is
zero exactly on nonunits, and has absolute value one on A^*. The virtual
normalized state is

    |N_Q>=[p U]^(-1/2) sum_R c(L(R)) |R>.

It is not prepared by the algorithm. Neither the CRT factorization, hidden
Q, field roots, dual coordinates, nor a norm oracle is supplied.

The additive Fourier transform is zero off H=K^perp. A character in H
corresponds, via the nondegenerate product trace pairing, to a unique tuple
t=(t_i) in A. The Fourier sum factors into component quadratic Gauss sums.
If any t_i=0, the corresponding sum of the nontrivial chi_i is zero. If
every t_i!=0, the product has absolute value p^(d/2). Including the p-element
kernel, the unitary Fourier factor p^(-(d+1)/2), and [pU]^(-1/2), gives

    |<y|F N_Q>| = 1/sqrt(U)

on exactly U labels, corresponding to dual-unit tuples, and zero elsewhere.
The dual-unit set lies in H but is usually not all H\{0}. No stronger
irreducible-case support statement is used.

Since the actual and virtual phases agree on precisely the Ngood good
labels and the virtual amplitudes vanish on the others,

    |<N_Q|S_Q>| = gamma = Ngood/sqrt(N0 p U).

This is an exact overlap, with no uncharged normalization or root rejection.

## 3. Uniform escape and constants

For every proper linear subspace W<H, its dimension is at most d-1. Since
F N_Q is flat on its dual-unit support,

    ||Pi_W F N_Q||^2 <= p^(d-1)/U.

Cauchy-Schwarz applied to the W and H\W parts of the overlap therefore gives

    Pr_{F S_Q}[y in H\W]
      >= [gamma-sqrt(p^(d-1)/U)]_+^2.

This remains uniform when W is the span of all previously obtained genuine
independent samples; no assumption about recognizing those samples is made.

At p>=4d^2, the following conservative bounds hold:

- alpha>=1/2 by the union bound for a repeated pair of roots.
- Ngood/N0>=1/2: in a uniform distinct d-tuple, each coordinate is uniform
  on F_p, so hitting one of r roots has probability at most dr/p<=d^2/p.
- N0/p^(d+1)=(1-1/p)alpha/d!>=1/(4d!).
- U/p^d=product_i(1-p^(-d_i))>=1-sum_i p^(-d_i)>=1-d/p>=1/2.

Also U<=p^d. Consequently

    gamma^2=(Ngood/N0)^2 * N0/(pU) >=1/(16d!).

At p>=128d!, sqrt(p^(d-1)/U)<=sqrt(2/p)<=1/(8sqrt(d!)),
while gamma>=1/(4sqrt(d!)). Thus the conditional escape probability is at
least 1/(64d!). Including the known distinctness flag gives at least
1/(128d!) per attempt. A block of d fresh attempts, consuming d^2 copies,
has probability at least q0=(128d!)^(-d) of producing d independent vectors
in H. Their nullspace is exactly span(Q).

The decoder solves each d-by-(d+1) system, rejects rank deficiency or zero
leading coordinate, normalizes to monic, and checks degree d and
squarefreeness by gcd(C,C')=1. An irreducibility filter would wrongly reject
the newly admitted reducible targets and must be replaced. Outlier blocks
are candidate generators whose results are verified with fresh copies.

## 4. Verification with shared factors and padded zeros

Let Q,Q' be distinct monic squarefree polynomials of degree d. Set
D=gcd(Q,Q'), k=deg D<=d-1, and

    T=(Q/D)(Q'/D).

T is nonconstant squarefree of degree 2(d-k); D is coprime to T. At points
where neither Q nor Q' vanishes, lambda(Q)lambda(Q')=chi_p(T), because D^2
is a nonzero square. At each rational root of D, the padded product is +1
and chi_p(T) is +/-1, causing discrepancy at most 2. At each rational root
of T, chi_p(T)=0 and the padded product is +/-1, causing discrepancy at most
1. Therefore the total discrepancy of the two character sums is at most

    2k + 2(d-k) = 2d.

Applying Weil to T gives the safe bound

    |<phi_Q'|phi_Q>|
      <= [(2d-2k-1)sqrt(p)+2d]/p
      <= [(2d-1)sqrt(p)+2d]/p.

At p>=256d^2 this is strictly less than 1/4 (indeed at most
1/8+1/(128d)). A public candidate-state projection hence accepts a wrong
candidate with probability <=1/16 and the true candidate with probability
one, ideally. This treats shared factors explicitly; applying a squarefree
Weil statement directly to Q Q' without removing common factors would be
an incomplete justification.

The previous bounded schedule and precision proof applies after replacing
q0 and the candidate test: R=ceil((4/q0)ln(4/eta)),
K=ceil(ln(4R/eta)/ln8), per-block event error<=q0/4, per-test event error
<=min(1/16,1/(4K)). A true candidate is accepted per block with probability
at least q0/4; wrong acceptance per candidate is <=8^(-K). The same public
seed event, bounded uniform-shift samplers, approximate public uniform
states, arbitrary-modulus QFTs, and public candidate inverses retain their
previous accounting. The copy cap is R(d^2+K). No fresh unknown source
inverse, free root indicator, or omitted rejection is introduced.

## 5. Matched classical baseline and scope counterexamples

Kopparty, `kopparty_noisy_2601_07137.txt`, gives a matched full-table
classical comparator even for the padded convention. There is a source
constant discrepancy: introductory Theorem 1 prints degree<=epsilon sqrt(p),
whereas the explicit Algorithm A correctness theorem, Theorem 3.1, assumes
degree<=(epsilon/16)sqrt(p). I inspected both statements directly. Use the
proved sufficient Algorithm A regime: with epsilon=1/16 and
p>=(256d)^2, d<=sqrt(p)/256, and the full padded table differs from chi_p
composed with Q at only r<=d<p/16 entries. Thus Algorithm A runs in poly(p)
time and recovers Q from p original padded-bit queries in this sufficient
regime. This does not invalidate the source or change the fixed-degree
asymptotic comparison; it avoids silently transferring the introductory
constant to the proved algorithm. The QUANTUM threshold p>=256d^2 above is
unchanged and follows from its own proof. The classical algorithm is
polynomial in field size, not input bit length log p. Its noise tolerance
does not imply noisy quantum copies are handled here.

The earlier quasilinear full-table cubic central-window theorem was proved
for IRREDUCIBLE cubics. It should not be silently extended to reducible
padded tables: changing values at rational roots changes the interpolant
and its coefficient equations. For original trit access with zeros retained,
that separate generalization requires its own proof.

Squarefreeness is a real identifiability restriction. Already the padded
states for (X-s)^2 are constant +1 for every s, including at the roots.
More strongly, Q=A^2 with A any monic irreducible quadratic gives constant
+1 even with the original trit character oracle because there are no
rational zeros. Distinct choices of A give distinct degree-four Q with
identical native information. No exact coefficient recovery theorem for all
monic polynomials can follow without a quotient promise or changed output.

The present result is a reviewed written algorithm for the stated fixed-d
squarefree, sufficiently-large-p, exact-copy model. Finite controls may
falsify its implementation identities but cannot establish this theorem,
priority, execution, a classical lower bound, or a speedup.

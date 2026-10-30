# CM Orientations Do Not Supply The Missing Weak Isogeny

2026-10-25. Local mathematical deduction and source audit. Independent
review and novelty assessment pending. No cryptographic break, geometric
source implementation, classical lower bound or new quantum algorithm.

## Decision

Do not register the recently published oriented-surface construction as
an application of our weak-isogeny HSP chain. The bridge is missing.
There are TWO different obstacles, not just an unfinished implementation:

1. Endpoint orientation evaluations do not identify the unknown connecting
   isogeny's auxiliary-torsion map, even up to the allowed common scalar.
2. In the prime-multiplier, regular-spectrum regime, adding an efficient
   genuine weak evaluator and the existing geometric source also enables
   our classical bounded-list attack. It is not exclusively quantum access.

This does not rule out other attacks or establish the published protocol's
security. Unknown composite-degree vectorization is a different task.

## Literature Input, Not A New Repository Result

[Castryck--Dina--Kutas--Lorenzon, arXiv:2610.27922v1](https://arxiv.org/html/2610.27922v1),
Section 4.3, represents endpoint CM endomorphisms through torsion
interpolation data. After a horizontal isogeny, the data are re-expressed
in a deterministic endpoint basis; they are not published as aligned
images of the original source basis. Section 7 discusses abelian hidden
shift attacks. Appendix I gives a heuristic subexponential quantum
endomorphism-ring algorithm under additional assumptions, and a heuristic
classical polynomial case for small discriminant. These are published
baselines, not results of this project. Their existence does not supply
our missing weak evaluator.

The exact scope of the new local analysis below is OUR proposed bridge.
It does not assume that the paper's unknown connecting map has a known
prime multiplier, or that its target order is public.

## 1. Fixed Input And Local Ambiguity

Fix principally polarized surfaces A,B and compatible orientations of the
SAME quartic CM field K. Consider horizontal polarized maps phi:A->B
with phi^dagger phi=[ell], ell an odd prime different from the geometric
characteristic. Require a public integral generator gamma of K whose
degree-four characteristic polynomial is squarefree modulo ell and all
auxiliary primes r below. Full source-order data are needed only when
applying the old algorithmic attack, not for the counting argument.

At an auxiliary prime r != ell, the input reveals matrices Gamma_A and
Gamma_B for gamma in independent endpoint bases. A proposed map W has
to satisfy

    W Gamma_A = Gamma_B W,
    W^t J_B W = ell J_A.

This normalized multiplier describes common-unit weak evaluations too:
if a weak matrix has multiplier u^2 ell, scaling by either square root
of u^2 gives a normalized representative. Exactly +/-1 preserve the
normalized multiplier. Thus weak projective classes correspond to
normalized matrices modulo +/-1, not to a single canonical matrix.

Assume the local solution set is nonempty, and fix one solution W0 FOR
THE PROOF. Every solution is uniquely W0 C where C commutes with Gamma_A
and C^dagger C=1. Regularity identifies the commutant with the rank-four
etale algebra K mod r. Its Rosati involution is CM conjugation. These
facts follow by diagonalizing Gamma_A over an algebraic closure: four
distinct eigenvalues give a faithful rank-one module over the algebra.

CM conjugation pairs the four embeddings without fixed points. Frobenius
commutes with this pairing. Its cycles either come in conjugate pairs of
length d, contributing r^d-1 norm-one elements, or are individually
conjugation-stable of length 2d, contributing r^d+1. In the latter case,
conjugation is the unique order-two power of the cycle, so the equation
is z^(r^d+1)=1 in F_(r^(2d)). In the paired case one component freely
determines the other by inversion. Consequently the possible orders are

    (r-1)^2, (r-1)(r+1), (r+1)^2, r^2-1, r^2+1.

The local weak-class count is HALF this order. A basis choice cannot
remove the ambiguity about which of these maps came from the same global
phi. Canonicalizing the two endpoint bases merely fixes coordinates.
This is a nonidentification statement about the stated local equations;
it does NOT prove that an algorithm using endpoint geometry cannot find
the desired globally correlated map.

## 2. At Most Four Horizontal Prime-Multiplier Kernels

The kernel of phi on A[ell] is a gamma-invariant Lagrangian plane. Over
the algebraic closure, every invariant subspace is a sum of distinct
eigenlines. The polarization pairs an embedding's eigenline only with
its conjugate's: move gamma across the pairing using its Rosati adjoint.
Thus an invariant Lagrangian must select exactly ONE eigenline from
each of the TWO conjugate pairs. There are four choices. Retain only
Frobenius-stable choices to descend to F_ell. This leaves 0, 2 or 4.

The factorization over F_ell computes these choices without enumerating
ell field elements: multiply selected distinct irreducible factors to
degree two, take the kernel of that polynomial in Gamma_A, and test
isotropy. The full source order's public local splitting supplies the
abstract matrix when available. It does NOT supply geometric ell points.

This sharpens the six-plane regular-spectrum bound for the additional
horizontal CM promise. It does not by itself identify which quotient is
the given B or construct that quotient in polynomial time in log ell.
An exponential-degree geometric quotient is not a free verification step.

For a hypothetical supplied weak phi, horizontality also gives the exact
source pullback alpha=phi^dagger gamma_B phi=ell gamma_A. Hence the old
regular-spectrum attack is specifically in its rank-zero branch.
IF the existing original source f is implemented with its promised fibers
f(M)=f(N) iff MK=NK, test each candidate's two basis vectors with their
symplectic transvections and f(I). At most 1+2*4=9 classical source calls
select the true K. All source costs remain charged. No new callback or
oracle is constructed in this bundle. The proof of that selection step
and its previous controls are in regular-spectrum-kernel-2026-10-25.

## 3. A Global-Consistency Counting Falsifier

Even orientation AND full pairings together do not make independently
chosen local intertwiners into evaluations of one global map.

For each of the at most four horizontal kernels, maps to the fixed
oriented polarized B form, when nonempty, a torsor for oriented polarized
Aut(B). The centralizer of the maximal subfield K in End^0(B) is K.
Such an automorphism is therefore an algebraic-integer unit a in K with
a*bar(a)=1. Every complex conjugate has absolute value one. The integer
minimal-polynomial coefficients of all powers of a are bounded; there
are finitely many such polynomials and roots, so two powers coincide.
Thus a is a root of unity. A quartic number field has at most 12 roots
of unity: if a primitive m-th root is present, phi(m) divides 4, giving
m in {1,2,3,4,5,6,8,10,12}. Modulo +/-1 there are at most six maps per
kernel and at most 24 globally realizable weak tuples altogether.

For DISTINCT auxiliary primes with local norm-one group orders T_r,
sample each compatible local weak class independently and uniformly.
For FIXED oriented endpoints and FIXED prime multiplier ell,

    Pr[the tuple comes from one global horizontal phi]
        <= min(1, 24 / product_r (T_r/2)).

This is a counting upper bound for that specific random-completion
strategy. It neither tests actual tuples for global consistency nor
applies negatively to honest evaluations, which already satisfy the
global promise. Adaptive geometric correlation is not covered. Choosing
endpoints or degrees after sampling also changes the experiment.

For a simple reproducible algebra control, K=Q(zeta_8) has conjugation
zeta->zeta^-1 and polynomial x^4+1. At r=17,41,73 all four roots split,
so T_r=(r-1)^2. The conditional bound is 1/11059200 for any admissible
ell different from these primes. NO actual oriented endpoints or phi
were constructed for this control. Small-discriminant CM itself is not
our proposed hard family. Its role here is exact arithmetic validation.

## 4. Adversarial Scope Check

- **Could deterministic bases secretly reveal W?** They reveal coordinates
  for the endomorphism action. Multiplication by ANY nonscalar norm-one
  element of the CM algebra preserves all the local equations. The
  explicit x element of F_r[x]/(x^4+1) is a countercontrol, even at a
  127-bit prime. Geometry could still choose a global solution; it needs
  a separate charged algorithm, not this local calculation.
- **Could the constant kernel list break vectorization?** No. It assumes
  a fixed prime-multiplier horizontal isogeny. A long product of ideals
  has a different, generally enormous degree and many factorizations.
  Computing which path reaches B is not supplied by a single-step list.
- **Could more orientation generators remove the ambiguity?** Generators
  of the SAME commutative field commute with the same norm-one torus.
  They do not. A genuine map outside that field could change the answer,
  but obtaining it is extra input, not another CM expression.
- **What about bad primes or ramified/nonmaximal orders?** The regular
  generator premise is essential. The result must not be extrapolated
  to repeated spectra or a non-etale reduction. No hardness is inferred
  in excluded cases.
- **Does this invalidate the weak-isogeny source theorem?** No: a genuine
  weak evaluator remains a valid input. We have rejected a proposed way
  of obtaining it and narrowed where it could give an advantage.
- **What would reverse the decision?** A construction from the ORIGINAL
  public key that gives one globally consistent weak map of a useful
  multiplier, together with a matched classical comparison surviving
  the regular-spectrum attack. Neither is present in the checked source.

## Next Decision

Keep general oriented vectorization open; do not label it solved or hard.
Do not spend another pass generating endpoint-matrix variants or local
intertwiner samplers. A new route must recover global ideal/isogeny data
or supply a genuinely different native algorithmic mechanism. Additional
bounded-class HSP receiver engineering does not repair this source gap.

The new finite-chain-ring parabolic-HSP paper
[Imran, arXiv:2610.28368v2](https://arxiv.org/html/2610.28368v2) solves a
specified GL_n parabolic promise from a hiding oracle. It is relevant
receiver prior art, not a native source generator. No reduction from our
arbitrary nilpotent subgroup problem to that promise was established by
this inspection, and no novelty conclusion follows.

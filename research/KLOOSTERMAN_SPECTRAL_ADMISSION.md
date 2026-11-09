# Growing-prime Kloosterman evaluation: spectral admission test

2026-11-06. Source audit and classical-first falsifiers. No new algorithm,
novelty, separation or general computational lower bound is claimed.

## Native question and admission decision

Input: explicit odd prime p, a in F_p^*, standard additive character
psi(x)=exp(2*pi*i*x/p), epsilon>0 and failure probability delta>0. Output
an additive-epsilon approximation to

    K_p(a)/sqrt(p),   K_p(a)=sum_(x!=0) psi(x+a/x).

The proposed target is poly(logp,1/epsilon,log1/delta) time, space and
coherent arithmetic, with no supplied Frobenius matrix, hard spectral
oracle or hidden advice. This is a longstanding explicit arithmetic
problem with applications to hidden nonlinear structures, rather than
an oracle invented for this repository. It is an independent alternative
to the current native polynomial-character reconstruction question.

**Decision:** no concrete new operation passes admission in this pass.
Published state preparation and walk simulation retain a sqrt(p) scale
loss. The proposed elliptic/full-zeta shortcuts fail the tests below.
Do not implement another walk, graph or Frobenius wrapper on this evidence.
The general scalar problem remains UNKNOWN, not hard or classically solved.

## Corpus, literature and classical comparison

The been-tried query was `normalized Kloosterman Frobenius eigenvalue
compression growing prime`; the baseline query was `Kloosterman exponential
sum Frobenius eigenvalues`. Legacy KLOOSTERMAN_TRACE registry records do
not by themselves solve this problem: some concern rational-phase hidden
shifts or finite candidate recovery. RECIPROCAL_TRACE_SOURCE_ACCESS.md
does solve a characteristic-two reciprocal-trace problem by elliptic
point counting. Its input family is different from growing odd p here.

Classical baselines under the actual input model:

- Direct summation costs p-1 explicit terms and polynomial precision work
  per term. To obtain epsilon on K/sqrt(p), per-term error O(epsilon/sqrt(p))
  suffices. This is an upper bound, not a best-classical lower bound.
- Uniform sampling of psi(x+a/x), rescaled by (p-1)/sqrt(p), gives the
  elementary O(p*epsilon^-2*log1/delta) sample upper bound; enumeration
  avoids repeated samples. Cancellation does not make constant samples
  sufficient for the requested additive scale.
- Kedlaya's introduction records classical curve methods polynomial in
  p,g,log_p(q), and fixed-genus methods polynomial in logq with exponential
  genus dependence. Fixed characteristic/controlled genus is not p=q
  growing with the Artin--Schreier genus below.
- Quadratically TWISTED Salie sums have explicit formulas. They are not
  the untwisted target. The affine quadratic character learner already
  knows the polynomial x^2-4a here; recovering it does not evaluate its
  selected Fourier coefficient.

No claim that the enumeration baseline is optimal, and no exhaustive
classification of all classical exponential-sum algorithms, is made.

## The published quantum operations do not pay the target scale

Bruin, Theorem 1.1 and Section 5, prepares the global state with amplitudes
K_p(a)/sqrt(N_1), where N_1=p^2-p-1. The desired scalar is that amplitude
times sqrt(N_1/p)=Theta(sqrt(p)). Section 6 and Theorem 1.2 explicitly pay
O(sqrt(p)/(delta*epsilon))*polylog(p). This is a published quantum upper
bound, not the sought polylog(p) algorithm. The multiplicative basis and
discrete-log conversion costs are accounted for in that construction.

Bruin also describes two Frobenius eigenvalues whose normalized sum is
K_p(a)/sqrt(p), and explicitly asks for an efficient unitary carrying
them. A rank-two conjugacy class does not supply that unitary, its inverse,
controlled powers, initialization, or precision guarantees.

Childs Section 8.1 already proposes the centered quadratic-character
Cayley Hamiltonian. Its useful spectral norm is O(sqrt(p)), while the
entrywise absolute matrix has norm (p^2-1)/(2p)=Theta(p). The published
walk simulation therefore retains the sqrt(p) scale loss. Subtracting
the uniform eigenvector is already included in this calculation.
Changing the name to a Hecke or nonbacktracking operator supplies no paid
improvement. No black-box lower bound or arithmetic impossibility follows.

An admitted spectral candidate would need an explicit circuit and
initialization with polynomial cost, controlled powers, epsilon/delta
ledger, and a proof that its observable carries K/sqrt(p) at constant
scale. Its first falsifier is its actual block normalization and spectral
weight, not a small-instance plot of the eigenvalues.

## Exact algebraic falsifier of the elliptic shortcut

Kononen--Rinta-aho--Vaananen, Theorem 1 (attributed there to Wan), says that
the n-dimensional sum with nonzero absolute trace generates the subfield
of Q(zeta_p) of degree (p-1)/gcd(n+1,p-1). Our sum has n=1, q=p and
Tr(a)=a!=0. Therefore, for EVERY prime p>=5 and EVERY a!=0,

    Q(K_p(a))=Q(zeta_p+zeta_p^-1),  degree=(p-1)/2.

In particular K_p(a), and its negative, cannot be an elliptic-curve
Frobenius trace, which is an integer. The same conclusion holds for
equality of normalized traces with the same denominator sqrt(p).
The congruence paper listed below uses a sum INCLUDING x=0, equal to
our K+1; its congruences must not be copied without that correction.

This is a published algebraic-degree theorem, NOT a complexity lower
bound. High algebraic degree does not obstruct efficient approximate
quantum phases. A rank-two object over a growing coefficient field or an
unrelated reduction is not ruled out.

## Whole-curve zeta loses the additive-character label

Consider the smooth projective normalization C_a of

    y^p-y=x+a/x.

Its two simple poles give, by the Artin--Schreier different formula and
Riemann--Hurwitz, 2g-2=-2p+2*2(p-1), hence g=p-1. Kedlaya's quantum
poly(g,logp) full-zeta theorem therefore does not provide the requested
polylog(p) guarantee. Its output numerator has degree 2p-2.

There is a second, separate issue even if that cost is ignored. For any
r in F_p^*, (x,y)->(r*x,r*y) is an F_p-isomorphism

    C_a -> C_(r^2*a).

Indeed (r*y)^p-r*y=r*(x+a/x)=r*x+r^2*a/(r*x). Thus these curves have the
SAME whole zeta function over every extension. But

    K_p(r^2*a)=sigma_r(K_p(a)),   sigma_r(zeta_p)=zeta_p^r,

and the exact field-degree theorem makes these unequal whenever r!=+/-1.
For p>=5, the unmarked zeta output alone cannot identify the requested
member of this conjugate family. The translation tau:y->y+1 is carried
to tau^r by the isomorphism: forgetting that mark forgets the additive
character label. This does not rule out using the original a, a marked
curve, or extra arithmetic. Computing the selected constituent with
those resources is the still-unpaid task, not an output of full counting.

At p=5,a=1,r=2 the two values are (3-sqrt(5))/2 and (3+sqrt(5))/2, both
with minimal polynomial X^2-3X+1. The exact Sage control in
classical_baselines/kloosterman_rank_two_control.py/.json confirms unequal
conjugates, both genera4, the rational-function isomorphism identity, a
bijection of the ten affine points and projective counts12. Full zeta
computation was NOT executed. This is a prescribed counterexample, not a
finite-size argument for the general statements above.

## Sources, review and next decision

Primary PDFs/texts are in audits/sources/legendre_prf/:

- [Bruin, 1807.03600](https://arxiv.org/abs/1807.03600): Theorems 1.1/1.2,
  Sections 5/6, introduction's explicit rank-two unitary question.
- [Childs, 0810.0312](https://arxiv.org/abs/0810.0312): Section 8.1. Its
  small-characteristic remark cites a QUANTUM zeta algorithm; that remark
  alone is not the source for the classical baseline.
- [Kononen et al., 1107.0188](https://arxiv.org/abs/1107.0188): definition
  and Theorem 1. The theorem suffices without later distinctness promises.
- [Gologlu et al., 1012.0964](https://arxiv.org/abs/1012.0964): definition
  and Theorem 13; note the +1 convention.
- [Kedlaya, math/0411623](https://arxiv.org/abs/math/0411623): introduction,
  Theorem 1 and Section 6 input convention. The introduction separately
  records the classical Lauder--Wan and Schoof/Pila bounds.

Independent actual-source audit confirmed the normalization, theorem
quantifiers, small-characteristic scope and +1 convention. It supplied no
new paid spectral operation. The parent checked the cited source text.
A separate elementary scope check accepted the isomorphism and changed
translation mark; this is not a general algorithmic impossibility review.

Next hard decision: compare a genuinely different paid operation for
uniform native polynomial-character reconstruction with an independent
high-upside candidate. Do not continue Kloosterman by studying another
formal rank-two representation. Re-admit it only with a concrete circuit
or marked-arithmetic reduction that survives the normalization and
character-label tests. All algorithm, separation, novelty, hardness,
quantum-execution and general-classical-solution gates remain false.

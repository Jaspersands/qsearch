# A Concrete Candidate Beyond Positive Sparse Pinning

2026-10-20. Local comparison REVIEW PENDING. This is an audit of a KNOWN
constructive algorithm, not discovery of a quantum algorithm or a general
classical lower bound. Producer: `theorems/nonlinear_filter_pinning.py`.
Artifact: `research/reductions/nonlinear_filter_pinning.json`.

## Decision

The previous relative-Gibbs pass supplied a strong classical sampler. Simply
requesting its TFD instead is not a useful computational problem. Sector-wise
one-dimensional simulation is a serious competitor for physical observables;
it does NOT by itself simulate arbitrary coherent target measurements. We
did not create another broad tensor-network no-go or TFD workbench.

Instead, retain the explicit nonlinear residual-chain optimization problem
from [Shang and Stilck Franca, Section 5](https://arxiv.org/abs/2609.35101).
It has a constructive quantum algorithm and classically verifiable outputs.
The question tested here is narrow and decisive: can the positive sparse-pin
mechanism that matched the Gibbs window reproduce this polynomial guide?

Answer: not through a bounded residual-cylinder decomposition. An exact
tail witness forces exponential absolute coefficient weight in that
representation. Other classical algorithms remain entirely open.

## Problem And Constructive Mechanism

Public input: an odd prime p, ordered distinct nonzero evaluation points,
nonzero multipliers a_i and explicit half-size field subsets F_i. Return
coefficients of a polynomial P of degree below n maximizing the number of
tests P(alpha_(i+1))+a_i P(alpha_i)^2 in F_i. Every proposed witness is
checked by modular arithmetic. No oracle-hidden random function is supplied.
Explicit tables cost O(p^2 log p) bits in the full-length family and must be
read and coherently implemented, not charged as free membership queries.

The known construction uses the invertible residual coordinates
r_i=x_(i+1)+a_i*x_i^2. Uniform source coordinates give independent pass bits
of density rho=(p-1)/(2p). A score-polynomial guide has Fourier labels supported
on at most 2D vertices. Sparse RS syndrome recovery clears that label before
the final Fourier readout. The source preparation and decoding are known;
we do not relabel them as repository discoveries.

Our implementation reuses the existing syndrome-only Prony decoder at
p2053,L2052,n205,cap100. It reconstructs an actual 100-error control from
205 public syndrome coordinates, without receiving its support. This is
classical BASIS verification of a reversible subroutine, not execution on
the coherent pilot or a claim that this seeded error has the pilot's law.

## Exact Readout, Not A Guessed Score Distribution

Let M=L-1 and E_k be the elementary symmetric degree-k polynomial in the
independent centered pass bits C_i-rho. Their squared norms and recurrence are

    h_k = binom(M,k) [rho(1-rho)]^k,
    S E_k = (k+1) E_(k+1) + [M rho+(1-2rho)k] E_k
              + rho(1-rho)(M-k+1) E_(k-1).

Numerics only propose radial coefficients. Dyadic inverse-square-root
enclosures define explicit RATIONAL coefficients b_k and a real guide
g(S)=sum b_k E_k(S). All normalization and moment calculations then use
exact fractions and this recurrence, not rounded eigenvalues.

RS interpolation transfers the r-th filtered score moment when
2*(2D+r)<=n: a product of 2D+r pairwise tests touches at most twice as many
vertices. At n205,D50, TWO moments are available, not three or a full score
law. The bounded p7,n4 control has exact normalization transfer but a different
native mean outside the mean-transfer budget. This guards against importing
the whole binomial source distribution as the target distribution.

For mean mu, variance v, integer threshold t and a=mu-(t-1)>0, set
c=mu+v/a. The quadratic

    q(s) = 1 - (s-c)^2 / (c-(t-1))^2

is below 1[s>=t] at every physical score. Its expectation is
a^2/(v+a^2). The verifier checks every integer s=0,...,M and the exact
expectation, independently of the numerical coefficient proposal.

At the published parameters, our rational guide has mean fraction
0.6431342271562736 and variance about490.141. The exact certificate gives
Pr[S>=1299]>0.47523 for EVERY input with the specified structure. With a
separately proved per-execution circuit TV error<=0.01, five independent
executions would succeed with probability>0.95. These are conditional ATTEMPT
counts, not gate counts or a completed quantum implementation.

This extends the repository's existing `OPI_FILTER_TAIL_CERTIFICATE.md`
machinery to biased pairwise tests; the new scientific comparison is below.
No additional filter-degree or seed campaign is warranted.

## What Sparse Positive Pinning Cannot Reproduce

Define the comparator exactly: each component is the UNIFORM SOURCE law
conditioned on fixed values, or fixed pass/fail outcomes, of at most K
residual coordinates. The initial root remains uniform. Components may have
arbitrary input-dependent mixture weights, but may not inspect or condition
the remaining residual values inside the component. This is not a definition
of every classical algorithm or every information-set search.

In each component, the remaining pass bits are independent Bernoulli(rho).
Granting all K pinned residuals a passing value therefore bounds its tail by

    b_K(t) = Pr[K + Bin(M-K,rho) >= t].

Every positive mixture inherits that bound. If a signed mixture of normalized
components has coefficients c_j summing to one, total absolute weight C,
and approximates the source guide law within TV epsilon, then

    (C+1)/2 * b_K(t) >= Pr_guide[S>=t]-epsilon,
    C >= 2*(Pr_guide[S>=t]-epsilon)/b_K(t)-1.

The code computes the binomial tail with exact integer recurrence and rounds
UP to a512-bit dyadic. The guide tail is rounded DOWN. With epsilon0.01 and
t1299, the resulting finite certificates are:

| Residual pin cap | Component tail upper | Absolute weight lower |
| --- | --- | --- |
| 100=2D | 1.449e-24 | 6.42e23 |
| 204=n-1 | 6.155e-16 | 1.51e15 |

Thus a low-degree expansion of the filter density is not automatically a
tractable positive-pin mixture. Ordinary sign-reweighting of this particular
representation encounters enormous normalization. This is NOT a universal
Monte Carlo lower bound, nor a proof that every estimator has that variance.
Allowing variable pin counts does not make the exceptional part negligible:
a positive mixture within TV0.01 must place more than0.4652 of its weight on
components exceeding either listed cap. The bound is (q-epsilon-b)/(1-b).

The asymptotic issue is not peculiar to the finite example. At rate R=1/10,
the known quantum mean tends to 1/2+sqrt(39)/40>0.65. For threshold0.6M,
the bounded-score mean argument gives eventual guide success>=1/8. If
K<=M/20, the component mean is at most0.525M, and Hoeffding gives
b_K<=exp(-9M/800). Exact representation therefore needs
C>=(1/4)exp(9M/800)-1. This is a method-specific exponential obstruction.

Crucially, the SOURCE guide is itself classically sampleable by drawing its
score shell, residuals and inverse triangular map. That fact does not produce
a feasible RS polynomial. Conversely, the source decomposition obstruction
does NOT prove that a positive decomposition only on the code is impossible:
different source functions can coincide after restriction. That is an explicit
remaining escape, not a loophole hidden in a hardness claim.

## Research Contract And Falsifiers

- Expected upside: a fully explicit coding/optimization task with a real
  polynomial quantum mechanism, not a new oracle separation. A substantial
  classical time advantage is OPEN; the current mechanism is already known.
- Strongest competitors: authors' interpolation, block search, annealing,
  tempering and inference/projection attacks; code-aware arithmetic attacks
  not expressible as source pin mixtures; direct target-only positive models.
- The [authors' frozen package](https://zenodo.org/records/22975424) contains
  actual instances and witnesses. We have NOT reproduced that campaign or
  validated those witnesses. Its incomplete raw-batch coverage must remain
  visible. Universal parameter certificates are not an instance reproduction.
- The folded membership-oracle separation in
  [Kramer et al.](https://arxiv.org/abs/2610.02145) is NOT a classical lower
  bound for these public scalar half-set tables. Do not import it.
- A classical method reaching the same witness threshold at a comparable
  complete-work budget weakens the finite advantage case. Exceeding a mean
  does not alone settle the whole quantum success curve.
- A reduction or proof showing code-restricted positive completion with paid
  polynomial preprocessing would directly defeat this proposed escape.
- Coherent source preparation, reversible decoder arithmetic, precision,
  full-input access and verification must all be charged before runtime claims.

Next GPT task: investigate a CODE-AWARE classical mechanism or a genuinely
stronger constructive decoder, not more tail certificates. One concrete
arithmetic formulation is to lift Q=P^2 and write the residual vector as
shifted evaluations of P plus diag(a) times evaluations of Q. The linear
relaxation has about3n variables but owes the nonlinear Q=P^2 identity; an
unconstrained lifted witness is NOT feasible. Determine whether this relation
helps reconstruction or leaves an exponential completion cost.

Gemini can verify the frozen author's witnesses and inventory implemented
classical attacks. No central proof/negative promotion or large benchmark
campaign before independent review and a genuinely new attack hypothesis.

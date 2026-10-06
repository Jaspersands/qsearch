# Native Likelihood Statistics: A Scoped Barrier

LOCAL DERIVATION / REVIEW PENDING. An application of standard orthogonality,
Bessel and statistical-query arguments. No new algorithm, general classical
hardness theorem, or independent mathematical review.

## Source And Exact Likelihood

Take IID uniform even-level native qutrit sources with residual modulus
R=3^r and secret s in Z_R^n. Keep ALL public frequency vectors a,c. A state is

```text
(|0>+zeta_R^(a.s)|1>+zeta_R^(c.s)|2>)/sqrt3.
```

Choose uniform independent b in F3; apply inverse quadratic phase and inverse
F3 Fourier transform, obtaining o in F3. A classical record is(a,c,b,o).
This is the same lawful source used by the final-field incidence decoder.
No label compression, chosen-label oracle, or manufactured phase query.

Let Q be the reference law with uniform independent a,c,b,o. Let P_s be the
physical law. Its density L_s=dP_s/dQ is3 times its Born outcome probability.
Writing chi_a(s)=zeta_R^(a.s), omega=exp(2*pi*i/3),

```text
L_s=1+(1/3)*[
  omega^(-b-o)*chi_a(s) + conjugate
 +omega^(-b-2o)*chi_c(s) + conjugate
 +omega^(-o)*chi_(c-a)(s) + conjugate ].
```

For each fixed record this is a seven-term sparse Fourier expression in s.
Multiplying many record likelihoods does NOT remain seven-sparse: its support
is a signed-difference modular subset-sum support. An explicit Fourier table,
group FFT, or expanded product costs up to the full group size R^n. None is
granted as a polynomial-time optimizer here.

## Exact Orthogonality On All Secrets

Treat L_s-1 as a sum of six characters of the public record group
Z_R^n x Z_R^n x F3 x F3. Their indices are

```text
( s, 0,2,2), (-s, 0,1,1),
( 0, s,2,1), ( 0,-s,1,2),
(-s, s,0,2), ( s,-s,0,1).
```

Each coefficient is1/3. The final two coordinates distinguish all six terms,
including when s=0. Two different secrets never give the same character
with the same control indices. Orthogonality therefore gives EXACTLY

```text
E_Q L_s=1;
<L_s-1,L_t-1>_Q=(2/3)*1[s=t].
```

Zero, nonprimitive and opposite secrets are included; no primitive-secret
conditioning or negation-orbit quotient is needed. Keeping b and o in the
record is essential. Conditional-on-a-label or basis-adaptive source changes
need a new proof; this identity does not automatically apply to them.

For k IID records and the same unknown s, the density is L_s^(k)=product_i L_s.
Independence gives

```text
<L_s^(k)-1,L_t^(k)-1>_(Q^k)=((5/3)^k-1)*1[s=t].
```

This is an exact native application of standard Fourier algebra, not a
claimed new general theorem.

## Bounded-Expectation Inference Gate

A STAT(tau) query is any real bounded function h of k records, |h|<=1.
The oracle returns an estimate of E_(P_s^k)h within absolute tolerance tau.
Only these expectation answers are available; not raw records.

Let d_k=(5/3)^k-1 and delta_s=<h,L_s^(k)-1>. Orthogonal normalized likelihoods
and Bessel imply

```text
sum_s delta_s^2 <= d_k * E_(Q^k)h^2 <= d_k.
```

Thus at most floor(d_k/tau^2) secrets force a reference answer E_(Q^k)h
to be invalid. Follow the algorithm's adaptive all-reference-answer path.
After T queries, at most T*floor(d_k/tau^2) secrets are exceptional. For the
others a legal oracle can keep answering the reference mean; only one can
match its final guess. Consequently under a uniform secret, against a legal
adversarial tolerance oracle,

```text
P(correct) <= min(1,[T*floor(d_k/tau^2)+1]/R^n).
```

The argument also handles algorithm randomization: for each secret the oracle
answers the reference until it ceases to be legal, then answers the true mean.
Condition on random coins to count the all-reference path, then average.
If different queries have different tolerances/arity, sum their individual
affected-secret bounds rather than using the minimum cost silently.

For fixed k, polynomial T and inverse-polynomial tolerance, this rules out
high-success identification when R^n is superpolynomial. It screens passive
single/fixed-arity bounded moment, correlation and approximate-gradient
proposals that genuinely fit this oracle model. It does NOT exclude arbitrary
machine learning, unbounded query normalization, raw-sample elimination,
chosen-label queries, altered quantum measurements, or growing-arity joint
inference. Growing k makes d_k exponential and the screen can be vacuous.
No statistical-query hardness is promoted to general classical hardness.

The general SQ model and its separation from raw-sample access are described
in [Feldman's primary COLT paper](https://proceedings.mlr.press/v65/feldman17c.html).
The six-character identity and numerical constants here are local applications,
not claims quoted from that paper.

## Observation-Density Converse, Even With Unlimited Processing

There is a second, distinct consequence for the same classical record source.
Let N=R^n, M IID records. Any optimal classical-record decoder selects a
likelihood maximizer at each observation. Randomization, unbounded computation,
or quantum computation on ONLY these classical records cannot improve its
optimal uniform-secret success. Relative to Q^M,

```text
P(correct)=(1/N)*E_Q max_s L_s^(M)
 <= (1/N)*sqrt(E_Q sum_s (L_s^(M))^2)
 =sqrt((5/3)^M/N).
```

Abstention only reduces unconditional success. At the native qutrit entropy
width M=nr, squared success is at most(5/9)^(nr). Positive likelihoods do
not rescue this particular measurement at that density. Avoiding this bound
requires at least M>=log(N)/log(5/3), approximately2.15*nr records; that is
only a necessary condition for THIS obstruction to be vacuous, not an
efficient decoder or a sufficient sample guarantee.

Unlike the SQ screen, this bounds all processing of the raw classical records
at the specified density. Unlike a generic quantum lower bound, it says
nothing about different single-qutrit POVMs, label-adaptive bases, collective
receivers, retained quantum states, or additional legitimately charged samples.
It does not import the earlier binary full-coordinate Fourier-noise theorem
onto a different ternary source.

## Mandatory Counterexample To Overclaiming

At R=3, the incidence decoder recovers s from these SAME record distributions
in polynomial time using exact algebraic relations of individual observations.
The report includes a fresh native n8 field decoder; its public records are
replayed by tests. Yet the family still has exponentially many orthogonal
single-record likelihoods and the fixed-arity SQ screen above.

Therefore a large SQ dimension, uncorrelated public Fourier moments or a
failed spectral baseline DOES NOT establish classical hardness or quantum
advantage. This counterexample is an explicit falsifier of that interpretation.
The decoder uses surplus records and exact raw-sample elimination; neither
the near-entropy converse nor the bounded-expectation screen excludes it.

## Verification And Revised Next Work

The theory module compiles exact characters without secret/source enumeration.
Bounded controls independently evaluate Born amplitudes for every label,
basis, outcome and secret at(n,R)=(1,3),(1,9),(2,3),(1,27), checking the whole
centered Gram matrix. Sparse secret-frequency likelihood terms are separately
tested against the actual measurement. Deep ledgers use exact fractions.
`node research/certificates/ternary_likelihood_crosscheck.js` independently
recomputes every Gram entry from Born amplitudes and exact rational ledgers.

Gemini: expose the report as a SCOPED classical-baseline gate, retain the
known-easy counterexample, and run production validation. No accepted candidate
or generic dequantization declaration follows from this pass.

GPT NEXT: raw-sample, multirecord algebraic inference that retains growing
root phases; or a genuinely implementable collective subgroup-covariant
receiver. A fixed-arity approximate-moment proposal needs to escape the exact
likelihood screen; a local-MUB receiver must charge its surplus density.
The hard step remains an implicit full-depth decoder, not producing samples.

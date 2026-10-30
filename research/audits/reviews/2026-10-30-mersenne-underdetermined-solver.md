# Mersenne Quartic Parametrization: Underdetermined-Solver Scope

2026-10-30. Task B. Written mathematical deductions and a primary-theorem
scope check; no native solver execution, independent review, novelty,
hardness, or speedup claim. No general-input polynomial solver is obtained.

Read first: [native target](../../MERSENNE_RECIPROCAL_RESEARCH_TARGET.md),
[global Fourier access](../../MERSENNE_GLOBAL_FOURIER_ACCESS.md), and the
current [handoff](../../AGENT_HANDOFF.md). Selective prior-work checks included
the [balanced partial-norm exclusion](../../MERSENNE_PARTIAL_NORM_FILTER.md),
the older [conic solver audit](../../independent_review_2026_10_22/CONIC_REFORMULATION.md),
and the [SDE scope discussion](../../POWER_SDE_SYMMETRIC_CONTRACTION.md).
The excluded balanced-factor construction is not retried here.

**Result.** The quartic formulation satisfies the Chevalley-Warning degree
inequality for every allowed n, but its consequence is even fiber counts,
not a constructive arbitrary-target solver. Its binary equation count
grows with its variable count. The diagonal-system theorems do not apply
to these mixed monomials. Importantly, their large sufficient arities are
NOT necessary arities, and genuine diagonal systems over the actual
binary field are easier still: they are linear as functions. The central
missing reduction is diagonality compatible with both sets of constraints.

## 1. Exact Native System And Field Accounting

Retain without restriction

```
n odd prime >= 17, q = 2^n, N = n^2, K = (N-1)/8,
s = floor((n-3)/4), r = n-4s in {3,5}, d = 2^s-1,
f_s(x) = Tr(inv0(x)^d), inv0(0) = 0,
H[j,i] = alpha_i^j, 0 <= j < K,
Omega_b = {x : Hx=0 and f_s(x_i)=b_i for every i}.
```

The public field representation, arbitrary distinct alpha_i, and arbitrary
bits b_i are unchanged. Put sigma(t)=t^(2^s). The established permutation

```
Phi(t) = (t sigma(t) sigma^2(t) sigma^3(t))^(2^r)
```

obeys f_s(Phi(t))=g_r(t), where g_r(t)=Tr(t^(2^r-1)), including zero.
Thus T_b={t : H Phi(t)=0, g_r(t_i)=b_i} maps bijectively to Omega_b.
Witnesses transfer, and uniform distributions transfer if a uniform
sampler for T_b is actually supplied.

Choose any public binary basis of F_q. Each Frobenius map is F_2-linear.
Each output bit of Phi is consequently a polynomial of degree at most 4
in the n input bits. The product

```
t^(2^r-1) = t t^2 ... t^(2^(r-1))
```

gives degree at most r for g_r. The exact Boolean degree is r: the n
cyclic shifts of the r consecutive one-bits in its exponent are distinct,
so the trace polynomial has noncancelling terms of binary weight r.

There are V=nN=n^3 Boolean variables and the following presentation:

| Constraints | Number | Degree bound |
|---|---:|---:|
| Binary coordinates of H Phi(t)=0 | nK | 4 |
| g_r(t_i)+b_i=0 | N | r |

Consequently

```
M = nK+N = (n^3+8n^2-n)/8,
V/M = 8n^2/(n^2+8n-1) < 8,
S = 4nK+rN = (n^3-n)/2 + r n^2,
Delta = V-S = n(n^2-2rn+1)/2 > 0.
```

S is a degree-sum upper bound, not a claimed lower bound on every
equivalent presentation. All these counts concern equations over F_2,
not nK equations over F_q.

| n | r | V | M | S | Delta |
|---:|---:|---:|---:|---:|---:|
| 17 | 5 | 4913 | 901 | 3893 | 1020 |
| 19 | 3 | 6859 | 1216 | 4503 | 2356 |
| 31 | 3 | 29791 | 4681 | 17763 | 12028 |
| 61 | 5 | 226981 | 32086 | 132065 | 94916 |

**Do not mix field and Boolean degree.** As a univariate F_q polynomial,
Phi has exponent E=2^r(1+2^s+2^(2s)+2^(3s)), of exponential ordinary
degree in n. It is not an ordinary quartic in one F_q variable. Treating
its Frobenius factors as independent variables requires their consistency
equations; over F_q, sigma(t)=t^(2^s) is not linear. Expanding over F_2
makes those maps linear but restores the n-fold equation/variable counts.
One cannot simultaneously claim N field variables and ordinary degree 4.

## 2. Exact Chevalley-Warning Consequence

**Lemma 1.** Every T_b has even cardinality. More generally, restrict all
the displayed equations to any injectively parametrized binary affine
subspace with ell>S free bits. Its solution count is even, for every b.

**Proof.** For the binary coordinate parity polynomials P_a and local
polynomials G_i=g_r(t_i)+b_i, the Boolean solution indicator is

```
J_b(t) = product_a (1+P_a(t)) product_i (1+G_i(t)).
```

Its degree is at most S. An affine substitution cannot increase degree.
The sum over F_2^ell of every monomial of degree below ell is zero in
F_2: some variable is absent, and summing over that variable contributes
two identical terms. Therefore the parity of the solution count is zero.
This proves the claimed specialization directly, without invoking a
constructive solving theorem. Since n>=17>2r, Delta is positive. QED.

For b=0 the known point t=0 implies a second solution exists. For a
nonzero target, zero is not a solution; an even count could be zero.
The existing native Fourier/MDS fiber bound separately proves that every
T_b is nonempty. Neither that existence proof nor the parity argument
locates a point. Likewise, a parity-count query on any affine restriction
with ell>S always returns zero, even when the restriction is nonempty.
A parity-only search needs further restriction or isolation; the degree
inequality does not supply its cost or success probability.

### Homogenization Does Not Force The Requested Target

Take formal homogeneous representatives P_a of degree 4 and g_r of
degree r, obtained by multiplying their binary-linear Frobenius factors
before multilinear reduction. Introduce h and solve

```
P_a(t)=0,
g_r(t_i)+b_i h^r=0.
```

The h=1 section is the requested problem. The h=0 section is T_0,
independent of b. Lemma 1 guarantees a nonzero t in T_0, since it contains
zero and has even cardinality. Thus a solver allowed to return any
nonzero homogeneous solution may validly return (t,0), which decodes to
the wrong target whenever b!=0. This is a native-family counterexample
to that output contract, not a claim that the h=1 section is empty.
Adding h=1 simply restores the inhomogeneous task. A stronger solver
that enforces h!=0 would be useful, but is not supplied by homogeneity.

## 3. What The Diagonal Solving Theorems Actually Supply

Use L for a theorem's variable count, m for its equation count, Q for its
field size, and delta for its pure-power exponent, avoiding native n,s,d.
SDE asks for a nonzero solution of sum_l a_jl z_l^delta=0. It does not
include mixed monomials or arbitrary prescribed output bits.

The primary [Ivanyos--Santha manuscript, Definition 1, Theorem 11 and
Section 3](https://arxiv.org/html/1503.09016v2) first reduces the exponent
to gcd(delta,Q-1). For a nontrivial reduced exponent dividing Q-1, its
collision construction uses

```
G(delta,m) = delta^(delta(delta-1)/2) (m+1)^delta
```

variables and time polynomial in G and log Q for fixed delta. In
characteristic two the two disjoint colliding representations sum to a
nonzero solution, so G itself is a sufficient SDE arity. Without that
sign simplification, the proof of Theorem 3 gives the sufficient bound
G(delta,m)^ceil(log2(delta+1)). These are algorithmic sufficient bounds,
not minimal arities or lower bounds on other solvers.

For example, the characteristic-two collision bounds are

```
delta=3: L = 27(m+1)^3,
delta=5: L = 5^10(m+1)^5.
```

Substituting m=M=Theta(n^3) would ask for Theta(n^9) or Theta(n^15)
variables, with constants depending only on delta; the native binary
presentation has only n^3. Even a hypothetical successful reduction
with m=Theta(N)=Theta(n^2) would not fit those bounds with n^3 variables.
If treating the parity-only problem over F_q, N/K tends to 8 as well;
there is still only a constant-factor surplus, not these superlinear
arities. None of these comparisons licenses discarding equations.

### Essential Qualification: Native Diagonal Systems Would Be Easy

Over F_2, z^delta=z for every positive integer delta. A genuine diagonal
system, homogeneous or inhomogeneous, is just binary linear algebra.
There is no need for the preceding superlinear sufficient arities.

More generally, if gcd(delta,Q-1)=1, substitution y_l=z_l^delta reduces
sum_l a_jl z_l^delta=c_j to Ay=c. Gaussian elimination costs
O(m^2 L) field operations; inverse powering costs O(L log Q) field
multiplications, plus polynomial-bit extended Euclidean arithmetic.
For a consistent system, uniform affine-kernel sampling followed by the
bijection gives uniform solutions, with its field random bits charged.
This is a constructive lemma for genuinely diagonal systems.

For native Q=2^n and odd prime n>=17, the powers 3,4,5,7,31 all have
gcd(delta,Q-1)=1. For 7 and 31 this follows from
gcd(2^a-1,2^n-1)=2^gcd(a,n)-1 with a=3,5; for 3 and 5 the respective
orders of 2 are 2 and 4. Phi itself is also a power permutation.
Thus it would be misleading to say that an actual native diagonal
problem fails solely because its variable surplus is too small.

What fails is the reduction to that contract:

* In the binary presentation, quartic parity terms and degree-r local
  terms mix bits. A sum of individual powers is an affine function on
  binary inputs, whereas g_r has degree r>1. No invertible affine change
  of bits, even with invertible linear recombination of the equation
  functions, makes this entire list diagonal. This does not exclude a
  different encoding of its zero set or a nonlinear change of variables.
* Over F_q, replacing Phi(t_i) by independent x_i linearizes parity,
  but returns precisely f_s(x_i)=b_i. Replacing t_i^(2^r-1) by u_i
  linearizes each trace condition, but transforms parity nonlinearly.
  Permutation-root extraction is already paid and available; it has not
  simultaneously linearized these two families.
* Characteristic-two fourth powers cannot absorb the mixed quartic
  terms by a usual power-of-linear-form expansion:
  (sum_l c_l z_l)^4=sum_l c_l^4 z_l^4. Introducing independent monomials
  without their multiplicative consistency constraints is a relaxation,
  not an exact diagonalization. Adding unused variables to reach a
  theorem's arity similarly permits a nonzero answer supported entirely
  on those unused variables, with no native witness.

The source's diagonality and homogeneous-output premises, its growing-m
dependence, and its easy power-permutation cases must all be retained.
No hardness conclusion follows from this non-application.

## 4. A Quantified Check On Affine Subspace Choices

There is also a simple general-input bound on a specific proposed way
of reducing the variable count. Write the existing exact fiber estimate as

```
|T_b| = |Omega_b| = lambda_b 2^(V-M),
1-eta <= lambda_b <= 1+eta, eta < q^(-N/8).
```

**Lemma 2.** Fix any ell-dimensional binary linear subspace U of the
t-space, possibly chosen using the public points and targets. Draw a
uniform independent translation a in F_2^V. Then

```
E_a |(a+U) intersect T_b| = lambda_b 2^(ell-M),
Pr_a[(a+U) intersect T_b is nonempty]
    <= min(1, (1+eta) 2^(ell-M)).
```

**Proof.** For each fixed t, exactly 2^ell of the 2^V offsets a place t
in a+U. Sum over T_b and use the first-moment bound. QED.

Consequently polynomially many such trials with ell=O(log n) fail with
probability tending to one, even granting a perfect solver inside each
trial for free. For inverse-polynomial one-trial success this method
needs ell>=M-O(log n)=Theta(n^3), not a fixed number of variables.
At n=17, M=901; an ell=17 uniformly translated subspace has success at
most (1+eta)2^-884. These are bounds, not executions.

This statement is only about uniformly translated subspaces. It does not
exclude target-adaptive offsets, subspaces designed to enforce parity,
nonlinear parametrizations, or correlations proven to increase incidence.
Lemma 1 and Lemma 2 together quantify the distinction: parity counts are
automatically zero above S, while a randomly translated small subspace
below M has tiny probability of containing a solution. Neither fact
rules out a specialized solver at intermediate dimension.

## 5. Cost And Disposition

All identities use the supplied modulus and points. Input reading is
Theta(nN) bits up to encoding overhead; modulus/point validation is
polynomial. No field table, planted witness, oracle, or favorable layout
is used. The binary equations have polynomial-size evaluation circuits;
explicit coefficients can also be recovered by Boolean subset evaluation
up to degree 5, with polynomial overhead charged if a solver needs them.

Native verification computes Hx and the ORIGINAL f_s(x_i), including
the zero convention. Powering/inversion/trace can be done with O(n)
field operations per coordinate; parity and its coefficient construction
use O(NK) field operations. A conservative schoolbook bit bound is
O((NK+Nn)n^2)=O(n^6), plus input validation. Reconstructing x=Phi(t)
is polynomial and does not substitute for that independent native check.

The established signed Walsh evaluator and approximate local sampler
remain polynomial written constructions, not native executions. They
are neither withdrawn nor treated as missing oracles here. No search
algorithm or uniform sampler follows from this audit. The paid existing
systematic-completion benchmark still has success lambda_b 2^-K per
trial and is exactly uniform conditional on success; failure to improve
it here is not evidence of hardness.

**Concrete conclusion:** low Boolean degree does satisfy the counting
inequality, but does not instantiate a constructive arbitrary-target
theorem. The exact missing ingredient for this route is a solution-
preserving reduction that handles the mixed quartic/local constraints
with an applicable solver contract and charged growing equation count.
The lemmas above specify what ordinary homogenization, diagonal-power
substitution, and uniform affine restriction do and do not accomplish.

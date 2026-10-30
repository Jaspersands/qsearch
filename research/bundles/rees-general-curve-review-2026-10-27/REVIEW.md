# Independent Adversarial Review: General Weighted-Curve Gap

2026-10-27. Single-reviewer mathematical audit, not a novelty assessment,
formal verification, implementation audit, or independent test report.

## 1. Verdict And Scope

**No fatal algebraic, Jacobian, fiber-counting, Fourier, or source-composition
error found under the stated hypotheses.** The large-prime curve theorem in
`RESULT.md` has a complete conventional mathematical proof. In particular,
the bounded positive-word closure, the total coordinate-degree bound, the
nonsingular-fiber bound, and the use of `(T^* T)^m` all withstand review.
The conservative substitution `D_*=2^c-1` is valid.

The source conclusion remains conditional on the stated pure-copy access,
uniform coherent LINEAR representation, robustness promise, supplied
zero-moment design, and independently valid receiver/resource contract.
These are substantive assumptions, not consequences of the curve theorem.
The small spectral-population corollary in `APPLICATION_BOUNDARY.md` is also
correct. It does not remove the marked-word population obstruction.

No blocking finding requires changing the proposed large-prime theorem.
Important boundaries that must survive subsequent use are:

- The conjugacy closure is a cumulative vector-space closure, with ALL
  specified generators applied at each round. Generation alone is not a
  substitute for the characteristic-p Jacobian argument.
- A Jacobian witness may depend on p. One characteristic-zero determinant
  need not remain nonzero modulo every legal prime.
- The good pushforward is UNNORMALIZED. The fiber bound applies only to
  the selected nonzero-minor subset, not the full fiber.
- The alternating convolution gives `(T^* T)^m`, not a power of T. Neither
  the original curve mean nor the good-part Fourier transform is assumed
  Hermitian or positive semidefinite.
- H and K need not be normal in the ambient group. No quotient by H is
  being used as a group.
- One scale is shared by the entire moment packet; different packets have
  independent scales and fresh copies. Explicit failure controls appear
  below.
- The factorial moment-design bound, its construction cost, the receiver,
  and the older application lower bound are imported results, not results
  independently established by this audit.
- No small-prime extension, growing-class efficiency, mixed-state source
  theorem, natural hard family, or speedup follows from this review.

### Material Reviewed

The main proof was reconstructed from the proposed argument before reading
the new draft, then compared with the following files:

1. [Prior dilation source](/Users/jaspersands/Developer/qsearch-research-work/rees-dilation-average-2026-10-25/DILATION_AVERAGED_SOURCE.md),
   Sections 1-3 and the adjacent source/resource contract.
   SHA-256: `ac7e78705bf5172a3b2f0a0f527dcded72fed1a52d0aa859eddd388acd8d022b`.
2. [General-curve draft](/Users/jaspersands/Developer/qsearch-research-work/rees-general-curve-2026-10-27/RESULT.md),
   Sections 1-6.
   SHA-256: `a320541ad551c89014d6b5284af46f6f7c0a1db915595841f4aff16c0af40788`.
3. [Application boundary](/Users/jaspersands/Developer/qsearch-research-work/rees-general-curve-2026-10-27/APPLICATION_BOUNDARY.md).
   SHA-256: `77313bf49b9bea6279d39e173cbbc6f10e5d057d84b2a5ebfad4126d314b9203`.

These hashes identify the observed versions, not an immutable copied
snapshot. Parent code and tests were not audited or rerun. The reported
45 initial tests and subsequent 139 selected tests, syntax checks, receipt,
and main validation remain parent-reported evidence. They are neither
needed for nor a substitute for the proof below. No Git or UI operations
were used. This review is the only file written by this audit.

## 2. Exact Mathematical Statement

Let c be a fixed positive integer and p>c a prime. Let F_c be the free Lie
algebra over F_p on X_1,...,X_c, with X_j of weight j, modulo all homogeneous
components of weight greater than c. Use a homogeneous Lie basis and write

```text
D = dim(F_c),                 G_c = exp(F_c),
A(t) = sum_(j=1..c) t^j X_j,  g(t) = exp(A(t)),
T_pi = E_(t in F_p) pi(g(t)),
m = 2D^2+1,
P(c,D) = max(16*c^D, 4D(c-1), 4(c-1)^2, c+1).
```

For every prime p>=P(c,D) and every nontrivial irreducible complex unitary
representation pi of G_c, the proposed conclusion is

```text
||T_pi||_op <= theta = 2^(-1/(2m)) <= 1 - 1/(4m).
```

It consequently holds on the orthogonal complement of invariants in any
finite-dimensional unitary representation. Inflation transfers it to every
quotient of G_c. The claim concerns operator norm, not merely eigenvalues.

The dimensions are bounded independently of the ambient input dimension:
the weight-w component of the free associative algebra has one word per
composition of w, hence dimension 2^(w-1). The free Lie algebra embeds in
this tensor algebra; retaining weights <=c gives

```text
D <= sum_(w=1..c) 2^(w-1) = 2^c-1 = D_*.
```

This is valid in the present characteristic as well. No associative
identity is being imposed on the free Lie algebra beyond the weight
truncation. The stated dimensions 1,2,4,7,13,22 for c=1,...,6 are consistent
with the weighted free-Lie Hilbert series, but those examples do not enter
the proof.

## 3. Algebra And Bounded Conjugation Closure

### 3.1 Lazard, Group Powers, And Curve Generation

F_c has nilpotency class at most c<p. The truncated BCH construction and
its subgroup/Lie-subalgebra correspondence therefore apply. All required
denominators are units; the restriction is on nilpotency degree, not D.
In particular,

```text
(exp B)^r = exp(rB),    (exp B)^p = 1.
```

Thus G_c is an exponent-p group of order p^D. Subgroup logarithms are
F_p-Lie subalgebras; they need not be ideals. Normal subgroups correspond
to ideals. These are standard parts of the Lazard correspondence; see
[Glauberman, Section 4 and Theorem 4.8](https://ems.press/content/serial-article-files/29483?nt=1).

The matrix `(s^j)_(1<=s,j<=c)` is invertible because it is a Vandermonde
matrix multiplied by the nonzero row factors s. Hence the logarithms
A(1),...,A(c) linearly span X_1,...,X_c. The subgroup generated by
g(1),...,g(c) has logarithm containing these generators and is all G_c.

This group-generation observation is correct but does not, by itself,
establish separability of a word map in characteristic p. The following
tangent argument supplies the missing differential information explicitly.

### 3.2 Right Logarithmic Tangent

With `ad(A)B=[A,B]`, the RIGHT logarithmic derivative is

```text
W(t) = g'(t)g(t)^(-1)
     = sum_(k=0..c-1) ad(A(t))^k A'(t)/(k+1)!.
```

The positive signs match this right-derivative convention. A left
logarithmic derivative would have different signs. This is a formal
identity in the truncated algebra, not an analytic derivative on a finite
set. Its largest potentially used factorial is c!, so p>c suffices.

In a term of homogeneous weight j, differentiating the scalar attached to
one generator lowers its total t-degree by exactly one. Therefore

```text
W(t) = sum_(j=1..c) t^(j-1) Y_j,
Y_j = j X_j + B_j(X_1,...,X_(j-1)).
```

Here B_j consists of brackets of total weight j. They are made from
lower-weight generators, but are NOT themselves of weight less than j.
This distinction resolves the potentially misleading phrase "lowerweight
brackets" in the initial proposal. The new draft states the triangular
claim correctly.

The c distinct evaluations t=0,...,c-1 span the Y_j by ordinary
Vandermonde inversion. Inductively, Y_1 gives X_1 and Y_j gives X_j after
the lower generators have been recovered. Thus the Y_j Lie-generate F_c.
Their distinct nonzero homogeneous leading components also give
`dim V_0=c`, although the weaker fact `dim V_0>=1` suffices below.

For comparison with the existing c=3 result, with Z=[X_1,X_2],

```text
W(t) = X_1 + 2t X_2 + t^2 (3X_3 + Z/2).
```

These values span three dimensions, not the full four-dimensional algebra.
Conjugation is genuinely necessary in that example.

### 3.3 Saturation And Short Positive Words

Define exactly the cumulative chain used in the new draft:

```text
V_(r+1) = V_r + sum_(s=1..c) Ad(g(s)) V_r.
```

If V_(r+1)=V_r=V, each Ad(g(s)) preserves V. Since
`Ad(exp A)=exp(ad A)` and ad A raises weight, its logarithm truncates
before any denominator divisible by p. Consequently V is preserved by

```text
log(Ad(g(s))) = ad(A(s)).
```

The nonzero-point Vandermonde inversion then makes V invariant under every
ad(X_j). Closure of preserving operators under commutators and linear
combinations makes V invariant under ad(F_c). Thus V is a Lie ideal.
It contains all Y_j, which Lie-generate F_c, and therefore V=F_c.

No proper plateau can occur. Every proper round strictly raises dimension,
so V_(D-1)=F_c. In fact D-c rounds suffice, but the proposed D-1 bound is
valid. Induction on r shows that V_r is spanned by vectors

```text
Ad(x) W(t),  t in {0,...,c-1},
x = g(s_1)...g(s_l),  l<=r,  s_i in {1,...,c}.
```

Selecting D independent spanning vectors gives the claimed basis with
positive-word lengths at most D-1. There is no hidden conversion of an
inverse into p-1 positive factors. Inverses appear later as signed factors
and do not increase the closure depth. Nor is a p-sized group search
required: exact finite-field linear algebra can retain a spanning set and
word labels at each round.

## 4. Jacobian, Alternating Embedding, And Degrees

For such a basis, put

```text
F(h) = product_(i=1..D) x_i g(t_i+h_i) g(t_i)^(-1) x_i^(-1).
```

Every block is identity at h=0. In logarithmic coordinates the derivative
of log at identity is the identity map, and product differentiation has
identity prefixes and suffixes. Its ith column is exactly
`Ad(x_i)W(t_i)`. The Jacobian is therefore invertible over F_p.

A block has `2*length(x_i)+2 <= 2D` signed curve factors. There are at most
N=2D^2 such factors in the whole word. An explicit padding rule removes
any ambiguity about alternation or parity:

```text
positive letter g(a):    use the pair g(0)^(-1) g(a);
negative letter g(a)^-1: use the pair g(a)^(-1) g(0).
```

Concatenating these pairs embeds F in N alternating pairs; pad any
remaining pairs with zeros. Thus m=2D^2+1 is more than sufficient. Each
variable h_i occurs in one positive factor only, with parameter t_i+h_i.
All other variables of Psi are fixed. This exhibits a specific D-column
minor J of log Psi that is nonzero at the corresponding F_p point.

The choice of columns, basis words, and point is permitted to depend on p.
The proof establishes their existence for EACH p>c with uniform size
bounds. It does not assert that a single rational determinant has no
exceptional prime divisors.

Now consider the unrestricted alternating word. Each logarithmic factor
is `+A(u_i)` or `-A(u_i)`. Every BCH Lie monomial contributing to a
weight-w coordinate has total generator weight w. The attached scalar
monomial has ordinary total degree exactly w in the u_i. Truncation kills
weights greater than c. Induction through the BCH multiplications gives:

```text
each weight-w coordinate of log Psi is homogeneous of total degree w;
each coordinate has total degree <=c;
deg J <= sum_(basis coordinates b) (weight(b)-1) <= D(c-1).
```

These are formal polynomial degree bounds before replacing polynomials by
their values on F_p. Word length does not multiply the degree: BCH weight
controls every surviving monomial. Fixing constants only lowers degree.
In an arbitrary linear Lie basis, the <=c bound still holds; the sharper
homogeneity statement uses a homogeneous basis.

## 5. Nonsingular Fibers And The Fourier Bound

### 5.1 Fixed-Minor Good Part

Since J is a nonzero polynomial, the finite-field polynomial zero bound
gives

```text
beta = Pr_u[J(u)=0] <= D(c-1)/p.
```

For any fixed output y and any assignment to the 2m-D unselected variables,
the remaining D coordinates are a polynomial system in D variables of
degrees <=c. The retained solutions have determinant J!=0.

The exact theorem needed here is the nonsingular-root bound over an
arbitrary field. [Bafna, Sudan, Velusamy and Xiang, Definition 1.1 and
Corollary 1.3](https://arxiv.org/html/2102.00602v1) define their "isolated
zero" by a nonzero Jacobian determinant and bound its count by the product
of the degree bounds. The terminology is narrower than general geometric
isolation, but agrees exactly with this application. No assumption that
the entire fiber is zero-dimensional is required.

Thus each slice has at most c^D retained solutions. There are
p^(2m-D) slices, and each original input has mass p^(-2m), giving

```text
nu_good(y) <= c^D/p^D.
```

This is an UNNORMALIZED subprobability measure. Since its total mass is at
most one and |G_c|=p^D,

```text
|G_c| sum_y nu_good(y)^2
  <= p^D * max_y nu_good(y) * sum_y nu_good(y)
  <= c^D.
```

Conditioning and renormalizing by 1-beta would change these bounds and
must not be silently done. Singular components, including very large
identity fibers, are allowed. No equidistribution theorem or generic-fiber
claim is used.

### 5.2 Plancherel And Correct Group Powers

Use the convention `hat(nu)(pi)=sum_g nu(g)pi(g)` with unnormalized
Hilbert-Schmidt norm. Plancherel is

```text
sum_pi d_pi ||hat(nu_good)(pi)||_HS^2
  = |G_c| sum_g |nu_good(g)|^2 <= c^D.
```

Every nonlinear complex irreducible of a finite p-group has dimension at
least p. Hence its good-part operator norm is at most sqrt(c^D/p).
The bad measure has total mass beta, so the triangle inequality for
unitaries gives `||hat(nu_bad)(pi)||<=beta`.

Let mu_+ be the curve law and mu_- its inverse law. Independence of all
2m parameters and the ordering of the word give

```text
nu = (mu_- * mu_+)^(*m),
hat(nu)(pi) = (T_pi^* T_pi)^m,
||hat(nu)(pi)|| = ||T_pi||^(2m).
```

Thus for nonlinear irreducibles

```text
||T_pi||^(2m) <= sqrt(c^D/p) + D(c-1)/p.
```

The full Fourier transform is positive semidefinite because of its exact
`(T^*T)^m` form. The good-part transform need not be positive semidefinite,
even though nu_good is a nonnegative measure. Only Plancherel and the
triangle inequality are used for the split. No operator-order comparison
between the good and full transforms is justified or needed.

A nontrivial linear character factors through the abelianization with
basis X_1,...,X_c. On the curve it is

```text
omega^(alpha_1 t + ... + alpha_c t^c),  not all alpha_j zero.
```

Its polynomial is nonconstant of degree d<=c<p. The additive
[Weil bound](https://www.cambridge.org/core/books/abs/bounded-gaps-between-primes/weil-exponential-sum-bound/67671DDEA0272CDF690C363F311ECCBC)
gives norm at most (d-1)/sqrt(p), hence (c-1)/sqrt(p). Degree one gives
zero. This separate treatment is essential: G_c has many linear characters
and is not quasirandom in the all-nontrivial-irreducibles sense.

At p>=P(c,D), the two nonlinear terms are each at most 1/4, while the
linear bound is at most 1/2. This proves the claimed theta. The draft's
rational replacement also has the correct inequality direction:

```text
(1-1/(4m))^(2m) >= 1-2m/(4m) = 1/2
implies theta <= 1-1/(4m).
```

### 5.3 Conservative D_* Substitution

For any certified D_hat>=D, use m_hat=2D_hat^2+1 and P(c,D_hat). The short
word can be padded to this longer alternating word, and the same argument
has nonlinear bound at most

```text
sqrt(c^D_hat/p) + D_hat(c-1)/p.
```

Equivalently, the original norm bound implies the weaker norm bound for
the larger m_hat. Therefore D_*=2^c-1, or a larger upper bound, is safe for
the planner. The actual group order remains p^D and the actual minor has
D columns: substituting D_hat into those identities would be wrong.
The draft substitutes only into the conservative constants and does not
make that error. A smaller empirical dimension is not justified merely by
passing a finite set of tests.

## 6. Quotients, Nonnormal Subgroups, And Pure-State Defect

Let L have class at most c, and A_j belong to its lower-central term
gamma_j(L). An iterated bracket in these coefficients of total assigned
weight w belongs to gamma_w(L). All brackets of weight >c vanish, so
`X_j -> A_j` factors through F_c and surjects onto Lie<A_1,...,A_c>.
Exponentiating gives a surjection onto K. A representation of K inflated
to G_c has exactly the same invariant subspace and curve mean, so the
bound transfers without dependence on dim L.

Neither K nor H must be normal in exp L. The kernel of the universal
surjection is normal, as any homomorphism kernel is; this is a different
statement. Likewise h=log H is a Lie subalgebra, not necessarily an ideal.

For pure rho, take conjugation as a unitary representation on the complex
Hilbert-Schmidt space. Let P=T_K, the orthogonal projection onto its
invariants, and v=rho-P rho. Every group action preserves the invariant
subspace and its orthogonal complement. Hence, for the curve mean M,

```text
E_t |<psi|U(gamma_K(t))|psi>|^2
  = <rho,M rho>
  = ||P rho||_HS^2 + <v,Mv>
  <= ||P rho||_HS^2 + theta ||v||_HS^2
  = 1-(1-theta)||rho-P rho||_HS^2.
```

The left side is real and nonnegative; alternatively take real parts of
the middle expression and use the operator norm. M itself need not be
self-adjoint. Orthogonality gives

```text
||rho-P rho||_HS^2 = 1-Tr(rho P rho).
```

For pure rho and any state sigma,
`TD(rho,sigma) <= sqrt(1-Tr(rho sigma))`, with TD equal to half the trace
norm. Therefore the stated subgroup-twirl promise implies HS defect at
least delta^2. It is enough to assume this promise only for the coefficient
subgroups K actually encountered; the all-subgroups version is stronger.

The proof of the curve gap is unconditional within its algebraic setting.
The robustness promise is an additional input hypothesis; neither the
Jacobian certificate nor any finite spectral test certifies it for an
unknown native state. Conjugation/vectorization is used analytically and
does not provide or require a conjugate-state input to the compiler.

## 7. Whole-Packet Source, Exact Stabilizer, And Positivity

Write the lower-central Rees Lie algebra as the graded sum of
`z^j gamma_j(L)`, with evaluation

```text
E_u(sum_j z^j A_j) = sum_j u^j A_j.
```

This is a Lie homomorphism for every u, including zero, because brackets
respect weight and gamma_(>c)(L)=0. It exponentiates to a group
homomorphism. At u=0 it is the trivial homomorphism, not an invertible
dilation. No invertibility is needed for this source operation.

Let h=log H and use the lifted subgroup with Lie algebra
`sum_j z^j (h intersect gamma_j(L))`. This is a subalgebra whether or not
h is an ideal. If a lies outside it, at least one coefficient A_j is
outside h, so K=exp Lie<A_1,...,A_c> is not contained in H. Conversely,
coefficient membership puts every evaluated curve element in H. Enough
distinct nonzero evaluations also recover coefficient membership by
Vandermonde inversion if one defines the lift through evaluations.

Assume a supplied nonempty multiset S of nonzero field elements satisfying
`sum_(s in S) s^j=0` for j=1,...,c. For one fresh uniform u shared across
the whole packet, define

```text
R_u(a) = tensor_(s in S) U(exp(E_(su)(log a))),
f_u(a) = <psi^tensorM | R_u(a) | psi^tensorM>,
Fbar(a) = E_u f_u(a).
```

Each R_u is a genuine unitary representation. Thus f_u is a normalized
positive-definite matrix coefficient, and Fbar is positive definite by
convex averaging. In particular the address matrix
`Fbar(b^(-1)a)/|A|` is positive semidefinite with trace one. Complex-valued
off-diagonal overlaps do not jeopardize positivity.

On H, U acts on the ray of psi by a character chi. Since H has exponent p,
write `chi(exp B)=omega^lambda(B)` for an F_p-linear functional on h
annihilating [h,h]. This follows by applying the Lazard correspondence to
the character into the additive group F_p. For a in the lifted subgroup,
the packet phase exponent is

```text
sum_j u^j lambda(A_j) sum_(s in S) s^j = 0.
```

Consequently f_u(a)=1 for EVERY u, not just on average. The shared-scale
moment identity gives exact one, not merely modulus one. This establishes
the exact lifted-H condition without normality or a quotient group A/H.

For an outside address, choose any s_0 in S. All overlap factors have
modulus at most one; s_0 u is uniform in the entire field. Therefore

```text
|Fbar(a)|
 <= E_u product_s |<psi|U(gamma_K(su))|psi>|
 <= E_u |<psi|U(gamma_K(s_0 u))|psi>|
 <= sqrt(E_u |<psi|U(gamma_K(s_0 u))|psi>|^2)
 <= sqrt(1-(1-theta)delta^2)
 <= 1-(1-theta)delta^2/2.
```

Replacing 1-theta by the draft's smaller `g_c=1/(4m)` is valid. This
calculation bounds the modulus of the averaged product, not a product of
separately averaged factors.

Discarding the scale and target registers gives precisely this averaged
address state. With independent packets and fresh copies, the coefficient
becomes Fbar(a)^k. It remains positive definite, either by the tensor
representation construction or the Schur product theorem. Retained or
reused scale information is a different joint source and requires a
different receiver analysis.

## 8. Adversarial Controls And Failure Boundaries

1. **Nonnormal matrix powers.** The matrix with first row (0,1) and second
   row (0,0) has norm one but square zero. A small norm of T^r cannot
   establish a small norm of T. The actual proof avoids this error by
   using the positive operator T^*T before taking a power.

2. **Large singular fibers.** Setting u_(2i-1)=u_(2i) makes every pair in
   Psi identity. There are p^m such inputs in the identity fiber. Thus an
   unsliced global c^D-preimage claim would be false. The retained-root
   count after fixing the other variables is the correct claim.

3. **Missing weighted filtration.** For c=2 the universal weighted algebra
   is abelian. Mapping X_1 and X_2 to two noncommuting generators of a
   Heisenberg algebra cannot define a homomorphism. This violates the
   required A_2 in gamma_2(L) condition and shows why that condition cannot
   be removed merely because the ambient algebra has class two.

4. **Independent scales inside a packet destroy ray cancellation.** For
   c=1, odd p, S={1,-1}, and the one-dimensional representation
   U(a)=omega^a, the entire group stabilizes the pure state. A common scale
   gives packet coefficient one. Independent scales u_1,u_2 instead give
   E omega^((u_1-u_2)a)=0 for nonzero a, destroying the exact-H condition.

5. **Reusing a scale across packets can defeat amplification.** Still with
   c=1 and S={1,-1}, take U(a)=diag(1,omega^a) and psi=(|0>+|1>)/sqrt(2).
   For nonzero a, f_u(a)=cos^2(pi*u*a/p). One packet averages to 1/2, so
   fresh independent scales give 2^(-k). Reusing a single scale gives
   E_u f_u(a)^k >= 1/p because the u=0 term is one. The claimed independent
   exponential amplification cannot be inferred for that reused source.

6. **A few prime checks do not establish all legal primes.** A nonzero
   integer determinant can vanish modulo an untested prime. The theorem
   proves fresh witnesses over each F_p; a fixed rational certificate
   needs its own exceptional-prime analysis or exact finite-field fallback.

7. **Purity and ideal symmetry are real restrictions.** The Hilbert-Schmidt
   norm-one identity and squared pure-state overlap are not mixed-state
   source formulas. Approximate physical actions also do not preserve
   exact overlap one on H; their effect belongs in a complete channel
   error budget, not in the ideal algebraic identity.

## 9. Prime Range And Resource Accounting

The reviewed draft explicitly restricts its theorem to p>=P(c,D) and makes
no small-prime extension. That is sound. For c<p<P(c,D), the proof of a
nonzero minor still works, but the displayed large-prime estimates may
give no contraction.

There is no qualitative obstruction to a fixed-c finite-prime completion:
for each such p, the curve support contains identity and generates G_c.
If a nontrivial irreducible had ||T||=1, a maximizing unit vector would
give equality in averaging unit vectors. All pi(g(t))v would coincide;
the t=0 term forces them to equal v. Curve generation would then make v
invariant, a contradiction. Thus ||T||<1 for each fixed p. A finite exact
enumeration or certified spectral computation could produce a separate
worst-case constant for those primes. It does NOT automatically prove the
same theta stated for large primes. Ordinary floating-point spectra are
not exact certificates. Nothing here covers p<=c.

For the source, put `a_gap=g_c*delta^2/2`, or use the stronger theta-based
gap. With N=|A|, the ideal address-state difference from the exact coset
source has zero entries within cosets and other entries bounded by
`(1-a_gap)^k/N`. Hence

```text
||difference||_HS <= (1-a_gap)^k,
TD <= (sqrt(N)/2) * (1-a_gap)^k.
```

For B receiver leaves, the usual sequential channel hybrid adds at most
B times the per-leaf source error, including adaptive receivers. Therefore
the draft's more conservative choice

```text
k = ceil((ell + ceil(log2(4B/epsilon))) / a_gap),
ell >= log2 N,
Q = B*k*M
```

is sufficient for its claimed epsilon/4 source allocation. With half-diamond
per-action error eta=epsilon/(8Q), Q action replacements contribute at
most epsilon/8, assuming the error guarantee applies uniformly with all
controls and references. The remaining error budget is not certified by
the new argument.

Q counts both fresh native copies and uniform coherent SELECT calls for
this source construction. The elementary-gate bill additionally includes
`Q*C_U(eta)`, native width q and action description, public Rees arithmetic,
address preparation, field sampling, design construction, state acquisition,
and the full receiver. The 2m alternating factors are a mathematical
proof device, not 2m additional source calls or a demand for inverse-state
preparation. There is no claim of a full gate algorithm from a unit-cost
SELECT oracle alone.

The gap constants do not depend on ambient n, but the full problem costs
certainly can: for instance log|A|, the native width, arithmetic, and the
receiver may all depend on n. Constant-class does not mean a practical
constant or efficiency when c grows.

`RESULT.md` imports M<=(c+1)! and the general-class design construction.
This audit checks how a valid such design is used, not that earlier
construction or its runtime. The old c<=3 bound M<=24 alone does not prove
the general factorial claim. Keep the exact prior lemma/contract available
when presenting a standalone source theorem. The same qualification
applies to the receiver cap B.

## 10. Optional Application Corollary Check

The spectral-population argument in `APPLICATION_BOUNDARY.md` is correct
for the stated pure state and exact exponent-p linear action. For any g,
let P_r be the projectors onto the DISTINCT eigenvalues omega^r, and put
w_r=||P_r psi||^2. Averaging over <g> removes cross terms between different
eigenvalues, even if their angular separation is very small:

```text
T_<g>(rho) = sum_r P_r rho P_r,
Tr(rho T_<g>(rho)) = sum_r w_r^2.
```

If max_r w_r<=1-alpha, then `sum_r w_r^2<=max_r w_r<=1-alpha`.
For g in K, the K-invariant Hilbert-Schmidt subspace is contained in the
<g>-invariant subspace. Orthogonal projections onto nested subspaces give

```text
||T_K(rho)||_HS^2 <= ||T_<g>(rho)||_HS^2,
1-Tr(rho T_K(rho)) >= 1-Tr(rho T_<g>(rho)) >= alpha.
```

This requires no normality of <g> in K. If each nonrelation has the stated
population bound, every K not contained in H contains a suitable g. In
fact the weaker condition of one suitable g in every relevant K is enough.

The source proof can consequently use the HS promise directly:

```text
E_t |overlap(t)|^2 <= 1-g_c*alpha,
|Fbar(a)| <= sqrt(1-g_c*alpha) <= 1-g_c*alpha/2.
```

There is no need to turn alpha into a trace-distance lower bound and then
square it. This is a valid strengthening of the input-promise formulation,
not a method for estimating or certifying unknown populations.

For the two-population marked control, with a=1-1/d and b=1/d,

```text
HS defect = 1-(a^2+b^2) = 2ab = 2(d-1)/d^2,
TD(rho,T_<g>(rho)) = sqrt(ab) = sqrt(d-1)/d.
```

The second equality follows because the difference in the normalized
two-component basis has zero diagonal and off-diagonal entries of modulus
sqrt(ab), with eigenvalues +sqrt(ab) and -sqrt(ab). Degeneracy inside an
eigenspace does not change this calculation for a pure input.

Thus the inverse-defect multiplier in this source bound is still of order
d. Direct HS accounting improves constants relative to the TD-squared
route in this example, not the population scaling. The claim that an
independent Choi-copy lower bound is Omega(d) was not re-audited here; these
identities are consistent with it but do not prove it. Nor was the full
encoder/action reduction, its conjugate-action implementation cost, or
its classical baselines re-reviewed. They remain imported application
obligations. No new candidate infrastructure is justified by this check.

## 11. Certificate Boundary And Final Assessment

A public exact certificate can usefully record the field and weighted
basis, tangent coefficients, cumulative spans with positive-word labels,
chosen independent columns, padded alternating word, and its nonzero
Jacobian evaluation modulo p. An independent product-rule computation is
a good implementation control. To avoid circular checks, it should not
merely reuse the same tangent-basis determinant under a different name.
It must also distinguish actual D from the conservative planner bound.

Those are prospective validation requirements, not claims about whether
the uninspected `curve_certificate.py` implements them. Passing c<=6
examples, even at the smallest legal primes, cannot establish the general
theorem; the proof above does not rely on such extrapolation. Conversely,
the conventional proof does not certify any particular program or receipt.

**Final assessment:** accept the large-prime weighted-curve norm lemma and
its conditional pure-state packet-source consequence as mathematically
sound on this review. Accept the stated direct-HS population corollary.
Keep the source access, imported design/receiver, prime range, fixed-class
dependence, and population promise explicit. No fatal counterexample was
found; no novelty, implementation, natural-application, or speedup claim
has been endorsed.

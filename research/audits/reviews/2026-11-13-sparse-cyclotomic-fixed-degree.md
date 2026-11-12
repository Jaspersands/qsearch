# Cyclotomic specialization: fixed-degree full classical disposition

2026-11-13. Independent review of the completed sparse-cyclotomic report.
No sweep, implementation, external call, or novelty claim.

**Admitted.** For every fixed `delta`, the already proved classical `Alg`
algorithm, cyclotomic specialization below, and the checked
Lenstra--Silverberg finite-Q-algebra relation theorem give a bounded-error
classical polynomial sparse-BIT algorithm for the **full** relation lattice.
The numbers of variables and original atoms, and their binary exponents,
may all grow. The time is polynomial in the native input length and
`log(1/eta)`; its polynomial degree may depend on fixed `delta`. No integer
factorization oracle or supplied constant field is introduced.

**Rejected.** The report's Section 4 resultant criterion is not equivalent
to partial-component acceptance. It is a sufficient stronger condition.
The fixed-degree positive proof does not require that false equivalence.
No growing-degree full solver or lower bound is admitted.

Reviewed inputs: `GENERAL_SPARSE_CONSTANTS_ATTACK.md`; the completed
`audits/claude_runs/2026-11-13-sparse-cyclotomic/response.md`; retained LS
Theorem 1.11 in
`audits/sources/sparse_charzero_relations/finite_Q_relations.txt`; and the
actual Oki introduction and Remark 12 in
`audits/sources/general_sparse_constants/oki.txt`. The previously checked
LS structure-constant input contract and the established `Alg` theorem are
used without enlarging their scope.

## 1. The sparse-factor probability lemma

Let `P=sum_{j=1}^K c_j T^{e_j}` be nonzero, with nonzero rational
coefficients, distinct exponent vectors, and `|e_{ji}|<2^b`. For a prime
`q>K`, assume no difference `e_j-e_l` is zero as a vector modulo `q`.
For uniform `a in F_q^s`, each pair of dot products collides with
probability `1/q`. Off all these collisions,

\[
 P(\zeta_q^{a_1},\ldots,\zeta_q^{a_s})
   =\sum_jc_j\zeta_q^{r_j},\qquad 0\le r_j<q,
\]

has `K<q` distinct nonzero monomials. A rational polynomial of degree at
most `q-1` vanishing at `zeta_q` must be a scalar multiple of
`Phi_q=1+X+...+X^(q-1)`, and hence needs `q` terms. Therefore

\[
 \Pr_a[P(\zeta_q^a)=0]\le {K\choose2}/q.                \tag{1}
\]

For a list of protected nonzero polynomials, let
`Pi=sum_P binom(|supp P|,2)` and bound all exponent coordinates by
`2^b`. For each pair choose one nonzero integer coordinate of its
difference, for the proof only. Its absolute value is below `2^(b+1)`;
thus fewer than `(b+1)/log_2 X` primes at least `X` divide it. The already
checked Rosser--Schoenfeld bound gives more than `3X/(5 ln X)` primes in
`[X,2X]` for `X>=21`. Consequently a uniform prime in this interval is bad
for some pair with probability at most

\[
 \frac{5\ln2}{3}\frac{\Pi(b+1)}X.
\]

Conditional on avoiding those primes, the union of (1) is at most
`Pi/X`. In total the failure probability is below

\[
 2.2\,\Pi(b+1)/X<1/2                                  \tag{2}
\]

when `X>=max(21, max_P |supp P|+1, 5 Pi(b+1))`. The report's final
constant is valid; its intermediate coordinate-difference bound needs
the extra bit for signed exponents, already covered by `b+1` in (2).
Rational coefficients are never reduced modulo `q`, so no coefficient-
content exclusion is missing here.

## 2. The fixed-degree Sylvester bound is sufficient

Normalize each input numerator/denominator pair by rational scalar
clearing, which does not change its support. Let `m>=2` bound the support
of every input polynomial. There are at most `delta` nonleading
coefficients of the monic `f`, and at most `delta` coefficients of each
`u_i`. With their respective denominator products `beta_f,beta_i`, put

\[
 \widehat f=\beta_f f,\qquad \widehat u_i=\beta_i u_i.
\]

Every Y-coefficient in either cleared polynomial is a product of at most
`delta` input polynomials, and therefore has at most `m^delta` monomials.
If `d_i=deg_Y u_i<delta`, the Sylvester matrix has size
`delta+d_i<=2delta-1`. Hence the nonzero polynomial

\[
 P_i=\operatorname{Res}_Y(\widehat f,\widehat u_i)
    =\beta_f^{d_i}\beta_i^{\delta}
       \operatorname{Norm}_{F/\mathbf Q(T)}(u_i)          \tag{3}
\]

has support at most

\[
 K_\delta=(2\delta-1)!\,m^{\delta(2\delta-1)}.           \tag{4}
\]

Nonzeroness follows from irreducibility of `f` and the promised nonzero
Y-basis element `u_i`. Constant-in-Y atoms, including `delta=1`, satisfy
the same formula and bound. Cancellation can only reduce support.

If input exponent coordinates have absolute value below `2^b0`, those
of each determinant term are below
`delta(2delta-1)2^b0`. Thus
`b=b0+ceil(log_2(2delta^2))` suffices in (2). Protect the `L` original
denominator polynomials **separately**, together with the `k` polynomials
`P_i`; one can use

\[
 \Pi\le Lm^2+kK_\delta^2.                              \tag{5}
\]

For fixed `delta`, the numerical values of (4), (5), and the required
`X` are polynomial in the sparse input bit length. No product of all
norms or expanded determinant support is needed by the algorithm: these
are proof bounds. The exponent bit bound, rather than the numerical
T-degree, enters `X`.

On the event in (2), every coefficient denominator evaluates nonzero and
every specialized norm is nonzero. All original atoms are then units in
the full finite algebra `Q(zeta_q)[Y]/f_t`. This is a sufficient success
event of probability greater than one half. The argument does not require
the specialized polynomial to be separable.

## 3. Exact partial-component acceptance and constants

The algorithm may accept more points than that sufficient event. Reject
when an original denominator evaluates to zero. Otherwise let

\[
 r=\operatorname{rad}(f_t)
   =f_t/\gcd(f_t,f_t'),
\]

and successively replace `g=r` by `g/gcd(g,u_i(t))`. Since `g` is
squarefree, one pass per original atom suffices. Accept exactly when
`deg g>=1`, and use

\[
 E=\mathbf Q(\zeta_q)[Y]/g.                            \tag{6}
\]

This needs polynomial gcd operations, not factorization of `f_t`.
The algebra (6) is nonzero and every original `u_i(t)` is a unit.

Let `A=Q[T,Den^{-1},Y]/(f)[u_1^{-1},...,u_k^{-1}]`, embedded in the
given function field. Monicity and irreducibility make the unlocalized
quotient a domain, and the nonzero atoms permit its localization. Its
subring `C_A` of elements algebraic over Q is a field: the inverse of a
nonzero algebraic element is a rational polynomial in that element.
The accepted point gives a unital map `A->E`. Its restriction to the
field `C_A` is injective because `E` is not the zero ring. It is not
necessary that all algebraic constants of `Frac(A)` lie in `A`.

For every `e in Alg`, the product `u^e` lies in `C_A`. Therefore

\[
 \operatorname{Rel}_F(u_1,\ldots,u_k)
 =\operatorname{Alg}\ \cap\
   \operatorname{Rel}_E(u_1(t),\ldots,u_k(t)).            \tag{7}
\]

This is exact for every accepted point, regardless of how it was sampled.
Discarding killed components does not lose the joint embedding of the
remaining constants. Neither a discriminant test nor an etale-fibre
promise is needed.

## 4. Native costs, full relations, and confidence

All binary T-exponents are reduced modulo `q` before evaluation. In the
power basis of `Q(zeta_q)`, the evaluated sparse coefficients have
polynomial bit length. Nonzero coefficient denominators are inverted by
exact linear algebra of dimension `q-1`; determinant/cofactor bounds pay
the inverse heights. The polynomial gcds above and the construction of
the rational structure constants of (6) have polynomial bit cost.
Its Q-dimension is at most `delta(q-1)`.

Apply the checked LS Theorem 1.11 to this explicit finite commutative
Q-algebra and the **original** specialized atoms. It returns their full
integer relation lattice, including torsion constraints. Intersect that
lattice with the previously computed `Alg` using integer kernel/HNF
operations, not merely intersection of rational spans. No Alg-basis
product or its potentially huge expanded algebraic value is ever formed.
Equation (7) then gives the full, possibly nonsaturated, relation lattice.

Keep `X` independent of `eta`: increasing cyclotomic degree polynomially
in `1/eta` would not give the required `log(1/eta)` clock. Instead take
`R=ceil(log_2(4/eta))` independent point trials. The ideal sampling process
fails to accept with probability at most `2^{-R}<=eta/4`.
Because `X` is polynomial in the native input length for fixed `delta`,
one may even enumerate the primes of `[X,2X]` deterministically and sample
uniformly from that list. Exact uniform selection of the prime index and
each residue coordinate uses binary rejection sampling. Cap each such
selection after
`ceil(log_2(4R(s+1)/eta))` trials and abort on exhaustion. Coupling with
the ideal process bounds the total sampling-cap failure by `eta/4`;
no biased-conditional-distribution assertion is needed.

Run the established general `Alg` algorithm with error allowance `eta/2`.
The full failure/abort budget is at most `eta`. Point acceptance and LS
are exact, but the **whole** algorithm remains bounded-error because the
`Alg` computation is bounded-error; it is not thereby converted to a
Las Vegas full-relation algorithm.

## 5. Rejected equivalence and scoped barrier claims

For any odd prime `q`, take

\[
 f=Y^2-T^q,\qquad u=Y-1.
\]

The generic `f` is irreducible, but at every `T=zeta_q^a` its radical is
`(Y-1)(Y+1)`. Removing the first factor leaves `g=Y+1`, where `u=-2`
is a unit. Every point is accepted, although
`Norm(u)=1-T^q` vanishes on the entire q-torsion grid. Thus a zero
norm-resultant means that some component is killed, not that every
component is killed. The report's Section 4 "exact criterion" and its
Section 5 identification `rho_q=0` with killing every branch are false.
The actual fibre criterion is `deg(r/gcd(r,product_i u_i(t)))>0`, with
the denominator checks retained.

Also, `Q[(Z/q)^s]` becomes a product of copies of C only **after scalar
extension to C**. A nonzero group-ring image of the product of protected
denominators and norm polynomials correctly expresses the stronger
sufficient condition, not the weakened acceptance condition.

Oki's actual Remark 12 does support the following conditional statement:
a polynomial-order cyclotomic hitting theorem for arbitrary nonzero
sparse-entry determinants would yield deterministic symbolic-determinant
identity testing. Kronecker exponents have polynomial bit length, and
in one variable all prime orders and residues below a polynomial bound
can be enumerated. The source introduction states the consequent circuit-
lower-bound implication. It does **not** prove such a theorem impossible,
exclude randomized algorithms, or embed general determinants into the
native monic irreducible Sylvester/norm family.

Accordingly, the report's "out of reach" language and structural
"necessary falsifier" descriptions are not admitted as general barriers.
In particular, the stronger norm test cannot be substituted for partial
acceptance, and one sparse or T-free atom alone does not control the
other atoms' bad loci. None of these defects affects the fixed-degree
positive proof above. The growing-`delta` full counterpart remains open.

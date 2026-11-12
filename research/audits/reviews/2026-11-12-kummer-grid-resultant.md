# Native local Kummer grid and branch-resultant repair

2026-11-12. Independent mathematical review of
`audits/openai_runs/2026-11-12-fast-kummer-build/response.md`.
Read current `STATE.md`, the paired
`audits/api_inputs/2026-11-12-accelerated/stoll-excerpts.md`, and the
seed/volume and finite-precision ledgers in `LOCAL_HALVING_SATURATION.md`
and `LOCAL_SATURATION_FINITE_PRECISION.md`. No Git, network, API, code,
numerical control, or sweep. Interpreter, if needed:
`/opt/anaconda3/bin/python`.

## Disposition

Both claimed representative-choice subtheorems are valid with their stated
input charges. The sampler provides actual signed-divisor points in a
specific full-rank subgroup of the ORIGINAL `E`, without numerically
inverting logarithms. The finite parameter grid gives a correctly scaled,
discriminant-controlled nonzero branch resultant and a corresponding
Sylvester inverse bound. The report's auxiliary polynomial-grid tail bound
also checks.

These are substantive advances. They do not compose directly into
ONE-HALF: the sampler outputs a signed divisor expression, whereas the
resultant lemma assumes an already certified reduced Mumford pair with
a charged numerical coefficient-pole bound. Converting `h+2 sigma(z)`
to such a pair, squarefree/root operations, the Stoll matrix bounds, and
the final actual-half certificate remain open. The report explicitly
retains these boundaries; no full Smith-minor theorem is required to
accept its two narrower results.

## 1. The native sampler: accepted

Retain the ACTUAL seed exponent `n_s>=2`, parameters `t_i=2^n_s i`,
closed seed lattice `L`, and `E=2L`. The existing determinant proof gives
the integral full-rank logarithm matrix `S` with determinant valuation
`D0`. Consequently

```
2^(D0+1) Z2^g subset 2 S Z2^g = log E.
```

Set `R=D0+1` and

```
sigma(z)=sum_i [P(t_i+2^R z_i)-P(t_i)],
W_(k,i)=-t_i^(2k)/sqrt(F(t_i^2)),
H=n_s g(g-1)+sum_(i<j) v2(j^2-i^2).
```

Every displayed point lies in the same torsion-free formal neighborhood
as the seeds. For `t in 4Z2`, the logarithm series is 1-Lipschitz in the
needed integral sense: a change by `2^R z` changes every component by
an element of `2^R Z2`. Thus `log sigma(z)` lies in `log E` and
injectivity of the formal logarithm proves actual membership in `E`.
This is stronger than a Kummer-label equality.

The derivative matrix `W` is a Vandermonde matrix in `t_i^2`, with unit
column factors. Hence `v2(det W)=H` exactly, independently of bad
reduction of the affine model. Moreover

```
D0-H=n_s g+sum_i v2(i)>=2g.
```

The report's Taylor coefficient bound can be checked term by term.
The coefficient of `z_i^a` from the logarithm term indexed by `b` has
valuation at least

```
R a - 2b + 2[2(k+b)+1-a]
 = R a + 4k+2b+2-2a.
```

Only terms with `2(k+b)+1>=a` occur. Their valuations are therefore
at least `(R-1)a+1`, as claimed. Removing the exact linear term and
using `v2(W^-1 entries)>=-H` yields

```
log sigma(z)=2^R W[z+epsilon(z)],
epsilon's coefficients have valuation >=R-H-1=D0-H>=2.
```

The remaining series is restricted, with coefficients tending to zero.
It is strictly contracting in the supremum norm. Therefore
`z -> z+epsilon(z)` is a bijection of `Z2^g`, with a compatible
permutation modulo every `2^m`. This proves, without performing an
inverse numerically,

```
U=sigma(Z2^g) is a subgroup,
log U=2^R W Z2^g,
2^(R+H)Z2^g subset log U subset 2^R Z2^g.
```

Finite integer-grid sampling consequently gives EXACT uniform classes
in `U/2^m U`. Haar-uniform `z` would give Haar measure on `U`.
A finite-grid representative is not itself a Haar sample of the whole
continuous group and is not automatically a conditioning-success sample.

For clarity, this is generally a strict subgroup of `E`, not a uniform
sampler of all `E`. In the ledger's differential normalization,

```
mu(U)=2^(-gR-H),
log2[E:U]=gR+H-D0-g=(g-1)D0+H.
```

Both depths are polynomial for the standard `n_s=2`. This is enough
for a future quantitative local tail argument, but that tail is not
proved by openness or finite-quotient uniformity.

## 2. Actual sampled points and precision: accepted, with exact interface

Let `T_max=n_s+floor(log2 g)`. The stated `R>T_max` follows from the
seed determinant formula, including `g=1`. Thus the perturbation cannot
cancel the leading term of any `t_i`, even for arbitrary `z_i in Z2`.
All sampled parameters are nonzero, retain their seed valuations, and
give the claimed polynomial pole bounds for `x=t^-2` and
`y=t^(-2g-1)sqrt(F(t^2))`.

For a finite-grid parameter, `t` is an explicit integer of bit length
`O(R+m+log g)`. Since `F(t^2)=1 mod16`, there is a unique square root
congruent to one modulo eight. Hensel's inequality at one, or the
displayed binomial series, supplies its existence and uniqueness.
For `u=F(t^2)-1`,

```
v2(binomial(1/2,a) u^a)
 >=4a-a-v2(a!) >=2a.
```

The proposed truncation therefore gives absolute `Q`-digit coordinate
accuracy after paying the `y` pole bound. Integer/rational numerators
and denominators in this truncation have polynomial bit length in the
listed numerical parameters. The certificate consisting of `t`, the
square-root equation, its residue class, and the error bound names an
ACTUAL `Q2` curve point. Keeping the `2g` signed terms avoids both a
quadratic-field compositum and an implicit Abel--Jacobi inverse.

For an actual input point `h`, `h_z=h+2 sigma(z)` has the same
`E`-coset, and any exact half `q_z` has certified residual
`2q_z-h=2 sigma(z) in E`. A hypothetical half `q` moves to
`q+sigma(z)`; no knowledge of `q` is used to generate the input.

What is NOT supplied is a reduced, suitably conditioned Mumford pair
for that signed sum, or the computation of `q_z`. A signed-divisor
certificate is valid actual-point data, but does not pay every matrix
or division needed by the Stoll implementation. This is the precise
remaining materialization interface, not a flaw in the sampler.

## 3. Deterministic branch resultant: accepted

Assume the lemma's actual reduced Mumford input: monic `a` of degree
`e<=g`, `deg b<e`, `a | f-b^2`, and coefficient valuations at least
`-S0`, with `S0>=0` numerically charged. Put `n=2g+1`, `m=n-e`, and
`S=(m+2)S0`. Monic long division bounds the coefficients of
`c=(f-b^2)/a` below by `-S`. Since `m>e`, for every integral `u`,

```
A_u=c-2ub-u^2 a
```

is monic of degree `m`. The retained Stoll source identity proves that
`[A_u,-b-ua]=[a,b]`; this is a SAME-point replacement, even stronger
than preserving an `E`-coset. It need not be reduced or squarefree.

At an integral root `theta` of `f`, differentiating `f=b^2+ac` and
using the pole bound gives

```
min{v2(c(theta)), 1+v2(b(theta)), v2(a(theta))}
 <=v2(f'(theta))+S.
```

The direction of this inequality is correct: every derivative
evaluation is bounded below by `-S`, so the valuation of the sum
`f'(theta)` is at least the displayed minimum minus `S`. Squarefreeness
of `f` ensures the resulting content bound is finite.

The Gauss valuation of a polynomial is multiplicative, also over the
splitting field used ONLY for this proof. Thus the integral polynomial

```
R(U)=Res_x(f,2^S A_U),     deg R<=2n,
```

has coefficient content valuation at most `D+2nS`, where
`D=v2(disc f)`. Interpolation at `0,...,2n`, with Lagrange denominator
valuations at most `v2((2n)!)`, proves that some candidate satisfies

```
v2 R(u)<=K_br=D+2nS+v2((2n)!).
```

No cancellation of component valuations was ignored: multiplicativity
of Gauss content is the relevant fact. This scaled UPPER bound also
avoids the previously refuted positive lower bound for an unscaled
resultant with nonintegral input coefficients.

For the selected candidate, `gcd(A_u,f)=1`. The scaled Sylvester
matrix is integral and invertible over `Q2`; its nonnegative Smith valuations
sum to the resultant valuation. Each is consequently at most `K_br`.
This pays a genuine branch-avoidance/gcd/CRT matrix, not `M_j` or `B_j`.
The native integer discriminant is computable, and its valuation is
polynomially bounded by genus and coefficient bits.

## 4. The stated numerical clock: accepted

The long-division loss deserves a degree-sensitive check; a crude
product bound would double-count losses. Reverse the monic divisor:
`a^*(T)=1+sum_(j>=1) a_(e-j) T^j`. Its inverse coefficient of degree
`l` has valuation at least `-l S0`. If the nonleading input coefficients
change at absolute precision `P`, the inverse-series identity

```
(a^*)^-1-(a_tilde^*)^-1
 =(a^*)^-1(a_tilde^*-a^*)(a_tilde^*)^-1
```

bounds its degree-`l>=1` change by `P-(l-1)S0`. The numerator
`f-b^2` has coefficients bounded below by `-2S0` and perturbation
precision at least `P-S0`. Therefore the quotient coefficient `r`
places below its leading term changes at precision at least
`P-(r+1)S0`. For `r<=m` this is stronger than `P-S`.

Hence `P>=K_br+S+1` conservatively allows the scaled Sylvester entries
and determinant to be computed modulo `2^(K_br+1)`. Integral determinant
arithmetic is Lipschitz at that precision; a nonzero residue certifies
the actual nonzero resultant. It uses no division by an uncertain
nonunit. The standard identity for perturbing an inverse loses at most
`2K_br`, so `P>=Q+2K_br+S+2` suffices for the asserted inverse-map
precision. Applying it to a right-hand side with poles would additionally
charge those poles; the integral CRT right-hand sides cause no new loss.

These costs are polynomial in numerical `S0`, not proof that `S0` is
uniformly polynomial in the original native input. In particular, the
sampler's individual curve-coordinate pole bounds do not yet imply such
a bound for the reduced Mumford coefficients of their sum with `h`.

## 5. Auxiliary grid-tail lemma: accepted; analytic application conditional

For an integral one-variable polynomial of degree at most `d` and
content valuation at most `C`, factor only for analysis. Roots of negative
valuation contribute their constant Gauss-content part. For each integral
root, at most one integer in `0,...,2^m-1` can be closer than valuation
`m-1`, because distinct grid integers differ at valuation at most `m-1`.
Away from at most `d` exceptional grid points, the polynomial valuation
is at most `C+d(m-1)`. This proves the one-variable bound.

For several variables, choose a coefficient polynomial containing a
coefficient of minimal content and apply induction to that coefficient.
Except on at most `(g-1)d/2^m` of the preceding grid choices, the
specialized last-variable polynomial has content at most
`C+(g-1)d(m-1)`. The one-variable bound and a union bound then prove

```
Pr[v2(P(z))>C+g d(m-1)]<=g d/2^m.
```

The report's formula is therefore valid. For analytic Stoll witnesses,
the promised integral scaling, low-jet content bound, and uniform tail
control are still essential. The truncated tail must be below the
valuation threshold being tested; low-order nonvanishing alone does
not supply this. An analysis union bound over at most exponentially
many half branches costs polynomial extra random bits only once all
the individual witness bounds are uniform and paid. No branch enumeration
or unproved conditioning guarantee follows from the lemma.

## Next scientific action and unchanged gates

Accepted: an explicit fixed-`E` full-rank sampling chart with actual
signed-divisor certificates; exact finite-quotient uniformity; the
deterministic, denominator-aware branch-resultant repair and its stated
numerical clock; the polynomial grid-tail template. No substantive false
identity was found in these claims.

Repaired scope: the sampler is on `U subset E`, and its signed-divisor
output is not the reduced Mumford input assumed by the second lemma.
Finite-quotient uniformity is not yet a conditioning-success probability.

Open: uniform reduced-coordinate pole bounds along `h+2 sigma(z)`,
squarefree/subresultant and Stoll-square-root operations, the selected
`M_j` and injective `B_j` loss bounds, and recovery of an actual certified
half. A useful next proof can now work on the explicit parameter map,
rather than assuming an effective inverse to the formal logarithm or
generic good representatives. It must pay the actual witness contents,
tails, and representation changes. ONE-HALF, complete native local
Kummer images, and the resulting global Selmer composition remain open.
No code, sweep, or full algorithm claim is warranted by these subtheorems
alone.

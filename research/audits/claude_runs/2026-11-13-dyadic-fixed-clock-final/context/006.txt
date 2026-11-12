# Stoll Smith bounds from geometric coordinates and one pencil

2026-11-13. Independent local derivation from the actual Proposition 5.1
and proof in `audits/api_inputs/2026-11-13-dyadic-high-degree/primary-excerpts.md`.
STATE and the three specified local-Kummer notes were read. No API,
network, Git, numerical sweep, or arbitrary-matrix obstruction.

**Disposition.** On the generic full-degree-half chart, an explicit
resultant identity bounds the augmented Stoll matrix and every truncated
Stoll matrix. The only extra geometric term in the direct proof is a
MIXED input/half resultant. The parent's same-class pencil pays that term
simultaneously for every rational half, without constructing those halves.
Its discriminant leading coefficient is also as conjectured.

Thus a polynomial coordinate/branch/separation event for the reduced input
and all its halves, plus its constructive materialization, would supply
polynomial Stoll Smith bounds after this inexpensive representation change.
There is no further unaccounted RR interpolation determinant in this proof.
The global Haar tail and its finite-grid/materialization transfer are NOT
proved here. The accepted chart requires all halves to have degree `g`;
the avoidance of lower-degree half charts must be included in that event.

## 1. Exact generic chart and determinant identity

Work over `Q_2`. Let `f` be monic integral squarefree of degree `m=2g+1`.
Let `a` be monic squarefree of degree `1<=n<=m`, coprime to `f`, and let
`b^2=f mod a`. Set `epsilon=(-1)^n` and choose
`s^2=epsilon a mod f`, with `deg s<m`.

Let `(U,V,W)` be the minimal Stoll solution, normalized by `W` monic,
and assume `deg W=g`. Then

    V = s W mod f,       V = b U mod a,
    V^2-f U^2 = epsilon a W^2.                         (1)

Write the resulting reduced half as `[W,R]`, `deg R<g`, so

    R^2=f mod W,        V=-R U mod W.

For this derivation assume `W` squarefree and `gcd(W,af)=1`. These are
explicit open-chart conditions, not consequences of coefficient bounds.
The source's gcd argument gives `gcd(U,W)=1`. Also `gcd(U,a)=1`: at a
simple root of `a` disjoint from `W`, simultaneous vanishing of `U,V`
would make the left side of (1) vanish to order at least two. It follows
that `gcd(U,V)=1`. All resultants below are consequently nonzero.

Let `M_g` have the coefficient rows of

    v-s w mod f,        v-b u mod a,

with Stoll's original degree bounds

    deg u < n/2,  deg v <= g+floor(n/2),  deg w <= g.

It has `m+n` rows and `m+n+1` columns. Let `B_g` append the row extracting
the coefficient of `x^g` in `w`. In ordinary ascending coefficient bases,

\[
 \det B_g
 =\pm\frac{\operatorname{Res}(U,V)\operatorname{Res}(f,s)}
                {\operatorname{Res}(a,U)\operatorname{Res}(W,R)}.
 \tag{2}
\]

The unspecified factor is a sign; in particular there is no unrecorded
power of two. For conditioning, the convenient exact consequence is

\[
 2v_2(\det B_g)
 =2v_2\operatorname{Res}(U,W)
  -v_2\operatorname{Res}(a,U)
  +v_2\operatorname{Res}(f,a)
  -2v_2\operatorname{Res}(W,R).
 \tag{3}
\]

### Proof of the factorization

On the column complement `w_g=0`, put

    P=Vv-fUu-epsilon aWw,       deg P <= m+n-1.

If `F=v-sw mod f` and `A=v-bu mod a`, then

    P=sW F mod f,              P=bU A mod a.

Therefore the coefficient matrix `T` of this polar map satisfies

\[
 \det T
 =\pm\frac{\operatorname{Res}(f,sW)\operatorname{Res}(a,bU)}
               {\operatorname{Res}(f,a)}\det B_g.
 \tag{4}
\]

This uses only multiplication in the two residue algebras and the CRT;
the coefficient-basis remainder map for monic `f,a` has determinant
`±Res(f,a)`.

Here is a direct computation of the remaining determinant. Let `alpha_i`
be the roots of `a`, and `xi_l` those of `W`. Apply to `P` the evaluations
at the `alpha_i`, the values and first derivatives at the `xi_l`, and
its top coefficient. This confluent evaluation map has determinant

    +/- Vand(alpha) Vand(xi)^4 Res(a,W)^2.

Write `phi=u y-v`. Values at the input points `(alpha_i,b(alpha_i))`
and at `(xi_l,-R(xi_l))` give

    P(alpha_i)=-b(alpha_i)U(alpha_i) phi(alpha_i,b(alpha_i)),
    P(xi_l)=R(xi_l)U(xi_l) phi(xi_l,-R(xi_l)).

After these values and the top coefficient are eliminated, the derivative
rows act on `w(xi_l)` by `-epsilon a(xi_l)W'(xi_l)`.
The exact section `U y-V` is the one-dimensional value kernel. Its
top pole coefficient is a unit: for odd `n=2r+1`, `U` has degree `r`
and leading coefficient `±1`; for even `n=2r`, `V` has degree `g+r`
and leading coefficient `±1`. This follows from (1), since the two
terms on the left have opposite degree parity.

Let `E` be evaluation of a basis of `L((n+2g-1) infinity)` at the
`n+g` points just listed. At all these points `y=V/U`. Multiplying
each evaluation row by `U`, its polynomial columns become the relevant
monomial multiples of `U` and `V`. Their coefficient determinant is
the padded Sylvester determinant `±Res(U,V)`. Padding introduces only
powers of the unit leading coefficient identified above. Thus

    det E / [Vand(alpha) Vand(xi) Res(a,W)]
       = +/- Res(U,V) / [Res(a,U) Res(W,U)].

Substitution in the confluent evaluation determinant cancels these
factors and gives the particularly simple identity

    det T = +/- Res(U,V) Res(a,b) Res(W,R).             (5)

Combining (4)--(5), `Res(f,W)=±Res(W,R)^2`, and
`Res(f,s)^2=±Res(f,a)` proves (2). Finally (1) reduced modulo `U`
gives

    Res(U,V)^2 = +/- Res(U,a) Res(U,W)^2.

The degree-padding factors are again units by the same parity argument.
This proves (3). In particular the apparent RR determinant has been
evaluated, not left as an additional conditioning assumption.

## 2. Coefficient bounds and a constructive Bezout certificate

Suppose every coefficient of `a,b,W,R` has valuation at least `-S`,
where `S>=1` is a known integer. Suppose also that the following
nonnegative upper bounds are available:

    v Res(f,a) <= K_af,
    v Res(W,R) <= K_wr,
    v Res(W,a) <= K_aw.                               (6)

The last is the mixed term. Separate within-divisor separation does
not, by its statement alone, supply it.

First, `U,V` have coefficient valuations at least `-3S/2`, without
solving an ill-conditioned interpolation problem. For the Gauss valuation,

    v_G(V^2-fU^2)=2 min(v_G(U),v_G(V)).

Indeed, after primitive scaling, cancellation of the whole reduction
would make the odd-degree monic polynomial `f mod 2` a square in
`F_2(x)`, impossible by its odd pole order at infinity. Gauss
multiplicativity in (1) now proves the assertion.

Define the following exact polynomials by monic division:

    C=(f-R^2)/W,
    T_0=(V+RU)/W,
    Z=(CU+2RT_0)/W.

The last division is exact: (1) gives
`U(CU+2RT_0)=W(T_0^2-epsilon a)`, and `gcd(U,W)=1`.
Consequently

    UZ-T_0^2=-epsilon a,
    U(4R^2 Z-C^2 U) = -4 epsilon a R^2 mod W.          (7)

This is an explicit Bezout-type splitting. Put `H=4R^2Z-C^2U`.
Elementary monic long division gives the sufficient bounds

    v_G(C), v_G(T_0) >= -(g+4)S,
    v_G(Z) >= -(2g+8)S,
    v_G(H) >= -(2g+10)S,          deg H <= 3g+2.

Every root of the monic `W` has valuation at least `-S`. Thus

    v Res(W,H) >= -g(5g+12)S.

Taking resultants in (7) yields

    v Res(U,W)=2g+v Res(W,a)+2v Res(W,R)-v Res(W,H).    (8)

Also the Sylvester matrix gives
`v Res(a,U)>=-2(n+g)S`. Combining (3) and (8), one explicit cap is

    v det B_g <= D_B,
    D_B=2g+K_aw+K_wr+ceil(K_af/2)
        +[g(5g+12)+n+g] S.                          (9)

No upper bound on an arbitrary matrix minor was assumed.

For completeness, the square-root input `s` is also bounded. Multiplication
by `W` modulo integral monic `f` has entries of valuation at least `-S`
and determinant `Res(f,W)=±Res(W,R)^2`. Applying its adjugate to `V`
shows that the coefficients of `s=V/W mod f` have valuation at least
`-(2g+2)S-2K_wr`. This applies to whichever square root was chosen:
the geometric event is required for every corresponding rational half.

## 3. Integral Smith bounds and rank discovery

All entries of `B_g` have valuation at least `-S_M`, for example with

    S_M=(2g+3)S+2K_wr.

The reduction modulo `a` costs at most polynomially many multiples of
`S`; reduction modulo integral monic `f` loses none. Thus
`B'=2^S_M B_g` is integral and has determinant valuation at most

    K_B=(m+n+1) S_M+D_B.                             (10)

Every Smith valuation of this square invertible matrix is at most `K_B`.
Deleting its last row gives a right inverse for `2^S_M M_g` with the
same denominator bound. For `k<g`, embed the columns of `M_k` in `B'`;
the last row is then identically zero, so the inverse of `B'` supplies
a left inverse for `2^S_M M_k` with that bound. Therefore

    dim ker M_k=0 (k<g),       dim ker M_g=1,

and every nonzero Smith invariant of every such matrix is bounded by
`K_B`. This agrees with the retained general kernel formula
`ker M=t_0 k[x]_(<=g-j)` at `j=g`.

Visibility of the determinant below this cap certifies the generic rank
and monic normalization. No exact p-adic zero test or search through
unknown lower-degree ranks is required on the accepted chart. A sample
whose `B_g` has no visible determinant may be rejected at the fixed cap.
This is not a proof that every lower-degree chart is intrinsically bad;
its avoidance probability is a separate part of the proposed tail theorem.
The earlier conservative `M_out+K_M+2K_B` precision ledger may use
`K_M<=K_B`, in addition to the paid entry-construction/scaling losses.

## 4. The same-class pencil pays the mixed term

Here is a checked repair of (6), rather than an independence assumption.
Start with the actual reduced squarefree pair `[a_0,b_0]`,
`e=deg a_0<=g`, and put

    c=(f-b_0^2)/a_0,
    A_u=c-2u b_0-u^2 a_0,
    B_u=-b_0-u a_0.                                 (11)

Then `[A_u,B_u]=[a_0,b_0]`; `A_u` is monic of fixed degree
`n=2g+1-e`, hence within Proposition 5.1. Its coefficients and those
of `B_u` have a uniform polynomial pole cap for `u in Z_2`, by monic
division. This is an actual representation change, not a new half.

For any half polynomial `W`, at a root `beta` of `W` let

    mu_beta=min(v c(beta), 1+v b_0(beta), v a_0(beta)).

Since `b_0(beta)^2+a_0(beta)c(beta)=f(beta)`,
`mu_beta<=1+v f(beta)/2`. Gauss multiplicativity over a splitting field
(used only in the proof) therefore gives

    v_G,u Res(W,A_u) <= g + (1/2) v Res(W,f).          (12)

Its degree in `u` is at most `2g`. Nonzero branch separation of `W`
ensures this polynomial is not identically zero. A separate joint
Haar tail for collisions on the graph `(2q,q)` is unnecessary after
this pencil randomization.

The source's squarefree-input requirement is paid by a second exact
identity. Set `N=n-e=2g+1-2e`, a positive odd integer. Then

    deg_u Disc_x(A_u)=4g,
    [u^(4g)] Disc_x(A_u)=+/- N^N Disc(a_0).           (13)

Use `Disc(1)=1` when `e=0`. To prove (13), work formally at `u=infinity`.
The `e` finite roots tend to the simple roots of `a_0`. The other `N`
roots have leading form `u^(2/N) zeta_N`. Their internal discriminant
contributes `±N^N u^(2N-2)`; finite/large cross pairs contribute
`u^(4e)`; finite/finite pairs contribute `Disc(a_0)`. The total exponent
is `2N-2+4e=4g`. Lower terms, including `-2u b_0`, do not affect it.
Since `N` is odd, the leading coefficient has valuation exactly
`v Disc(a_0)`.

For the branch resultant, if `S_A` bounds all coefficient poles in the
pencil, the retained derivative/Bezout argument gives

    v_G,u Res(f,2^S_A A_u) <= v Disc(f)+2m S_A,

and degree at most `2m`. At a root of `f`, this follows directly by
differentiating `f=b_0^2+a_0 c`; the derivative coefficients have pole
cap `S_A` and the root is integral.

**Normalization guard.** If `W` has coefficient poles, scaling `A_u`
alone need not make the mixed resultant integral. With pole bounds
`S_W,S_A`, use

    Res(2^S_W W,2^S_A A_u)
      =2^(n S_W+g S_A) Res(W,A_u).

Similarly use `2^((2n-2)S_A) Disc(A_u)` for an integral discriminant
polynomial. These known additions to the content caps are polynomial.
Unqualified signed resultants or their cancellations cannot be used as
integral Smith bounds.

Finally, if a nonzero polynomial of degree at most `d` has Gauss valuation
at most `C`, then on a uniform integer grid modulo `2^(t+1)`,

    Pr[v P(u)>C+d t] <= d 2^(-t).

Indeed factor over the algebraic closure. An excess over the Gauss
valuation is a sum of positive distances to roots in the unit ball;
one must exceed `t`, and each such root meets at most one residue class
modulo `2^(t+1)`. This also counts exact roots as bad.

Apply this to (12) for all at most `2^(2g)` rational halves, and to the
branch and discriminant polynomials. Taking
`t=O(g+log(g/delta))` gives simultaneous polynomial caps with failure
at most `delta`. Draw ONE integer with this polynomial bit length;
do not enumerate halves or the grid. The resulting `A_u` is squarefree,
coprime to `f` and every half `W`, and provides the mixed cap in (6).

## Remaining native obligation

The conditional geometric-to-Smith bridge is now explicit, including
rank discovery, normalization and the extra same-class randomization.
The remaining input is the promised constructive probability/precision
theorem for the original sigma procedure: actual closed reduced
coordinates, polynomial pole and branch caps, input discriminant cap,
and full-degree squarefree half charts for every rational half. It must
survive the fixed finite-precision saturation invariant and repeated
steps. That theorem is being attacked separately and is not inferred
from Haar existence, genericity, or this determinant identity.

For an UNMODIFIED representative, this review does not prove that separate
input/half coordinate bounds alone control a near mixed collision, and
does not assert a native counterexample. The pencil supplies a concrete
way to avoid that unresolved implication. No complete local Kummer,
Selmer, quantum algorithm, or classical lower bound is claimed here.

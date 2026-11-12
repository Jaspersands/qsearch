# Native cubic lift of sparse resultant leading coefficients

2026-11-13. Independent proof review of
`audits/openai_runs/2026-11-13-sparse-structured/response.md`.
No new solver, numerical control, or source assumption is introduced.

**Disposition.** The native lift, irreducibility, exact norm identities,
and the stated `Alg`/`Rel` lattices are sound. Its sparse representation
and coefficient-height bounds are polynomial in the input bits and the
**charged numerical Y-degree**. It reduces resultant leading-coefficient
extraction to the proposed norm-leading-coefficient step at infinity.
It proves neither a lower bound nor an obstruction to arbitrary places,
aligned leading-coefficient methods, or full relation algorithms.

The cancellation control is also correct, with `lambda^d=-1` understood
in the normalized Puiseux scale `t=T^(-1/d)`. An arbitrary choice of
uniformizer instead gives `LC(v)^d=-LC(T)`.

## 1. Valid native input and irreducibility

Take sparse `p,q in Z[T,Y]`, with `p` monic of Y-degree `d>=2`,
`0<=m=deg_Y q<d`, and `R=Res_Y(p,q)!=0`. Let `beta>=1` bound their
T-degrees and set

\[
 D=(d+m)\beta,\qquad H=d(D+1)+1,\qquad
 \widehat q=q+T^{-H},\qquad
 f=p^3-p\widehat q^2-\widehat q^3.                       \tag{1}
\]

The top Y-degree in `f` is `3d`, with coefficient 1; the other two
summands have strictly smaller Y-degree. Negative T-powers are ordinary
native rational coefficients, represented by denominators `T^H` or
`T^(3H)`.

Let `c` be the real root in `(1,2)` of `X^3-X-1`, and `K=Q(c)`.
The rational-root test gives `[K:Q]=3`, and
`Norm(c)=1`, `c^-1=c^2-1`. In particular `c` is not a root of unity.
For

\[
 g=p-c\widehat q\in K(T)[Y],
\]

the constant coefficient has T-adic valuation `-H`; every other
nonleading coefficient has valuation at least zero. If a root has
valuation `r`, the defining equation has a unique least-valuation term
unless `d r=-H`. Thus every root has valuation `-H/d`.

A monic factor of degree `j` would have a nonzero constant coefficient of
valuation `-Hj/d`, an integer. Since `gcd(H,d)=1`, `d|j`; hence `g` is
irreducible over `K(T)`. For a root `y`, the nonzero polynomial
`qhat` has degree below `d`, so `qhat(y)!=0`, and

\[
 c=p(y)/\widehat q(y)\in\mathbf Q(T,y).
\]

Therefore `Q(T,y)=K(T,y)` has degree `3d` over `Q(T)`. The monic
degree-`3d` polynomial `f` vanishes at `y`, so it is irreducible.
This verifies the native field promise without supplying `K` as input
advice.

## 2. Original atoms and the exact two lattices

In the original Y-power basis supply

\[
 u=p(T,y),\qquad v=\widehat q(T,y),\qquad
 w=p(T,y)^2-\widehat q(T,y)^2.
\]

Their degrees are at most `2d<3d`, so no Y-reduction or inverse
computation is required to present them. Inside the field,

\[
 u=cv,\qquad w=(c^2-1)v^2=c^{-1}v^2.                    \tag{2}
\]

Every term of `q(T,y)` has valuation at least `-mH/d>-H`, since its
T-exponents are nonnegative. Thus `v` has valuation `-H`, and the three
atoms are nonzero and nonconstant. Algebraic constants have valuation
zero at this extension of the T-adic place. Consequently

\[
 u^a v^b w^z=c^{a-z}v^{a+b+2z}
\]

is algebraic exactly when `a+b+2z=0`. It is 1 exactly when, additionally,
`a=z`, because `c` is nontorsion. Hence

\[
 \operatorname{Alg}=\{(a,b,z):a+b+2z=0\},\qquad
 \operatorname{Rel}=\mathbf Z(1,-3,1).                  \tag{3}
\]

The difference between constants and relations is present in the same
nonconstant atoms: `u/v=c!=1`, while `uw/v^3=1`. No separate constant
atom has been appended. No identification of the entire constant field
is needed for this proof.

## 3. Norms and the leading-coefficient reduction

Write `R_H=Res_Y(p,qhat)`. Since `g` is monic and replacing `p` by
`p-c qhat` does not change this resultant,

\[
 N_{F/K(T)}(v)=R_H,\qquad
 N_{F/\mathbf Q(T)}(u)=N_{F/\mathbf Q(T)}(v)=R_H^3,
 \qquad N_{F/\mathbf Q(T)}(w)=R_H^6.                    \tag{4}
\]

The norm of `c` in the full tower is `Norm_{K/Q}(c)^d=1`, accounting
for all signs and factors in (4).

Expand only for the proof

\[
 \operatorname{Res}_Y(p,q+Z)=\sum_{j=0}^{d}r_j(T)Z^j.
\]

Its Sylvester matrix has size `d+m`; every entry has T-degree at most
`beta`. Hence `deg_T r_j<=D`, with `r_0=R` and `r_d=1`. Since `H>D`,

\[
 R_H=R+\sum_{j\ge1}r_j(T)T^{-jH}
\]

has the same degree and leading coefficient at infinity as the nonzero
polynomial `R`. All perturbing terms have negative degree. Thus

\[
 \operatorname{lc}_\infty N(v)=(\operatorname{lc}R)^3,
 \qquad \deg_\infty N(v)=3\deg R.                     \tag{5}
\]

An exact signed integer cube root recovers `lc R` from (5), in polynomial
bit time. If degree is also returned, divide it by 3. The reduction
covers arbitrary nonzero resultants within the stated monic-`p`,
`deg q<deg p`, explicitly sparse input class; no more general resultant
input model is silently assumed.

Also `R_H` is nonconstant: its lowest T-power is `T^(-dH)`, with
coefficient 1, because `r_d=1` and the other `r_j` are polynomials.
Therefore the relation lattice of the three norm images in (4) is
exactly the plane `Alg`, not the true rank-one lattice `Rel`.

## 4. Representation and height accounting

Put `A=1+||p||_1+||q||_1`, and let `S` be their total supplied term
count plus one. With `P=T^H p` and `Q=T^H q+1`,

\[
 T^{3H}f=P^3-PQ^2-Q^3.
\]

This uses `O(S^3)` sparse terms before collection, has T-degree at most
`3(H+beta)`, and coefficient l1 norm at most `A^3`. Indeed, if
`a=||p||_1` and `b=1+||q||_1`, then
`a^3+a b^2+b^3 <= (a+b)^3=A^3`. Atom construction costs only quadratic
products. Coefficient bit lengths are `O(log A)` and exponent bit lengths
are `O(log H+log beta)`; `log H` is polynomial in the input length and
`log d`. The Y-basis dimension `3d` is charged numerically, as required
by the native contract.

For `n=d+m`, the Sylvester determinant gives

\[
 \|\operatorname{Res}_Y(p,q+Z)\|_1\le C:=n!A^n,
 \qquad \|T^{dH}R_H\|_1\le C.
\]

Substitution can merge monomials but cannot increase this l1 bound.
A cleared numerator of `N(v)` has norm at most `C^3`, and
`log C=O(d log d+d log A)`. This bounds coefficient sizes, not the
number of expanded coefficients or the cost of locating the surviving
leading one. The actual Sylvester matrix for `f,qhat` has size
`3d+m<4d` and explicitly supplied sparse rational entries; no generic
matrix embedding or expanded multiplication matrix is needed.

## 5. Exact cancellation control and LC normalization

For `p=(Y-T^M)^d+T`, `q=Y-T^M`, with `d,M>=2`, the supplied input has
`O(d)` terms and polynomial bit length in `d,log M`. Direct substitution
in the linear-second-polynomial resultant gives

\[
 R=(-1)^dT,\qquad R_H=T^{-dH}+(-1)^dT,
 \qquad N(v)=(T^{-dH}+(-1)^dT)^3.                       \tag{6}
\]

Thus the actual norm degree at infinity is 3 and its leading coefficient
is `(-1)^d`. Terms of the uncombined leading-scale expression have
T-degree `3dM`, but their specialized coefficients cancel. Formula (6)
jumps over the cancellation exactly; it is not a lower-bound example.

To verify the original-atom leading coefficients, put `x=y-T^M` and
`t=T^(-1/d)`, and write `x=t^-1 X`. The equation `p=c qhat` becomes

\[
 X^d+1-c t^{d-1}X-c t^{d(H+1)}=0.                       \tag{7}
\]

Every root `lambda` of `X^d+1` is simple in characteristic zero, so
formal Hensel lifting gives the corresponding branch of (7). On this
normalized branch the original LC tuple is

\[
 (c\lambda,\lambda,c^{-1}\lambda^2),\qquad\lambda^d=-1.
\]

For odd `d`, `lambda=-1` gives the displayed valid tuple
`(-c,-1,c^2-1)` over the fixed field `Q(c)`. Rescaling an arbitrary
uniformizer rescales these leading coefficients; the unnormalized
identity is `LC(v)^d=-LC(T)`.

The entire lifted family already has the explicit full relation lattice
(3). In normalized T-adic scale its original-atom LC tuple is even
`(c,1,c^-1)`, by the dominant `T^-H` term. These facts make the scope
essential: the construction charges a particular **norm-LC-at-infinity**
operation with arbitrary sparse resultant LC extraction. It does not
force other LC constructions to compute that norm, and does not show
the native full relation problem hard. Polynomial coefficient heights,
native irreducibility, and nontrivial `Alg` alone do not pay the proposed
norm-LC extraction clock; no broader impossibility follows.

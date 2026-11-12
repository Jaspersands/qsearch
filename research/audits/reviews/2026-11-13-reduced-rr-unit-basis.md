# Low-degree RR: an integral unit basis and an explicit Smith cap

2026-11-13. Independent negative audit of the parent's elementary repair
to `reduced-rr-cokernel.md`. The argument survives input collisions,
input/output overlaps and `q=0`. No Serre-duality lattice comparison is
needed. No API, network, Git or numerical test.

**Exact conclusion.** Once the output Mumford PAIR has integral
coefficients, the low RR matrices at `N=m+g` and `N+1` are
unit-surjective onto the specified saturated input quotient. For original
integral inputs and output coefficient pole cap `S`, every Smith exponent
of the original `M*` is at most

    (2m+2g-1)L,       for any integer L>=S.             (1)

The minimum valuation of a nonzero maximal minor is at most `m` times
(1). These are bounds on the actual native quotient lattice, not on a
matrix in a maximal-order/evaluated-point basis. Construction of that
saturated input quotient remains the separately paid product-stage task.

## 1. Integral-pair theorem

Let `O=Z_2`, `K=Q_2`, and

    R=O[x,y]/(y^2-f),   f monic integral squarefree, deg f=2g+1.

Let `I_K` be the generic input ideal with divisor `D_in` of degree `m`,
where `m>=g`. It contains a monic integral polynomial `A` of degree `m`
(in the native construction, `A=product a_i`). Put `J=I_K intersect R`.
Assume the residual output is the generic reduced degree-`g` divisor
`D_out=(a,b)`, with `a` monic, `deg b<g`, and BOTH `a,b` integral.
The convention in the prompt has `D_in=iota D_input`.

Put `N=m+g`. The one-dimensional generic RR kernel has a section
`F=p+qy` with

    div(F)=D_in+D_out-N infinity,
    p^2-fq^2=epsilon alpha^2 A a,                      (2)

where `alpha` is its top pole coefficient and `epsilon` is a sign.
The full-degree reduced output ensures that the pole is exactly `N`.
Choose `F` primitive in the integral monomial RR lattice; this choice
exists because `J` is the intersection with the generic ideal.

**Primitivity pays the leading coefficient.** The reduction of monic
odd-degree `f` is not a square in `F_2(x)`. Therefore primitive `p,q`
cannot satisfy `p^2-fq^2=0 mod2`; the norm in (2) is primitive.
Since `A,a` are monic integral, (2) forces `v_2(alpha)=0`. Normalize
`alpha=1` using an integral unit. No exact p-adic zero test has been
assumed, and the output coefficients are used only in this proof.

Define the proof-only second section

    G_true=F(y+b)/a = r+s y,
    r=(p b+q f)/a,        s=(p+q b)/a.                 (3)

Both quotients are integral polynomials by monic division. Indeed
`p+qb=0 mod a` since `F` vanishes on `D_out`, and
`pb+qf=b(p+qb)=0 mod a`. At infinity `(y+b)/a` has pole order one and
leading coefficient one. Thus `G_true` has pole weight `N+1` and top
coefficient one.

**Overlaps cause no failure of membership.** The negative part of
`div((y+b)/a)` is at most `D_out+infinity`. Hence (2) implies
`G_true in I_K`. If an input point also belongs to `D_out`, the one
removed zero is precisely the output zero; the entire input multiplicity
remains. Points on the conjugate output divisor cause no extra pole.
Since (3) is integral, `G_true in J`. This argument does not require
input/output disjointness or an inverse of `q`.

## 2. These two sections equal the saturated input ideal

In the `O[x]` coefficient basis `(1,y)`,

    det [[p,r],[q,s]]=(p^2-fq^2)/a=epsilon A.          (4)

Let `S=O[x]F+O[x]G_true`. Its reduction matrix modulo two is injective
over `F_2[x]`, since its determinant is the NONZERO monic polynomial
`A mod2`. Consequently `S` is two-saturated in `R`: if `2v=M c`,
reduction modulo two gives `c=0 mod2`, and cancelling the factor two
shows `v in S`.

Over `K[x]`, (4) gives quotient dimension `m`. Also `S_K subset I_K`
and `R_K/I_K` has dimension `m`, even for repeated or overlapping input
divisors. Thus `S_K=I_K`. Two-saturation now gives

    J=O[x]F+O[x]G_true.                              (5)

This proves equality of the required integral lattice. It is not an
identification of the raw, unsaturated product with its saturation.

There is an independent weighted-basis check. The pole weights of `F`
and `G_true` are `N` and `N+1`, of opposite parity. For nonzero
polynomials `u,v`, the possible leading weights of `uF` and `vG_true`
are `N+2deg u` and `N+1+2deg v`; they cannot cancel. Their leading
coefficients are units. Monic weighted reduction therefore shows that

    {x^j, x^j y : pole weight < N}                    (6)

is an integral basis of `R/J`. There are exactly `N-g=m` such monomials,
because `N>=2g`. All reductions are integral and terminate by decreasing
pole weight.

It follows that the columns (6) give a unit determinant in ANY integral
quotient basis of `R/J`, including the primitive membership map `Lambda`
in the prompt. Thus both `Lambda E_N` and `Lambda E_(N+1)` are
unit-surjective. Every nonzero Smith exponent is ZERO in this
integral-pair setting. The claim would be false in general after replacing
the specified quotient lattice by an unrelated evaluated-point lattice;
that replacement is not made here.

## 3. Actual extraction, without knowing the output pair

The algorithm uses the known membership map and the monomial columns (6).
Their `m`-by-`m` image matrix is invertible modulo two. Unit linear solves
return:

1. `F` in the kernel at `N`, with coefficient of the weight-`N` monomial
   equal to one;
2. `G=r+s y` in the kernel at `N+1`, with coefficient of the
   weight-`N+1` monomial equal to one.

The kernel at `N` is `O F`; the kernel at `N+1` is `O F+O G_true`.
Therefore the computed `G` equals `G_true+lambda F` for an INTEGRAL
constant `lambda`. No polynomial of positive degree multiplying `F`
can fit in pole weight `N+1`.

Set

    Delta=p s-q r,
    a_out=(p^2-fq^2)/Delta,
    b_out=[(r p-s q f)/Delta] mod a_out.              (7)

Equation (4) gives `Delta=epsilon A`, unchanged by adding `lambda F`.
Moreover

    G bar(F)/Delta = y+b+lambda a.

Hence (7) recovers the ACTUAL monic reduced pair, including its sign
convention. Every division is by a polynomial with unit leading
coefficient. The procedure remains valid when `q=0`, when intermediate
polynomials have common factors, and when input and output supports
overlap. It does not factor a support polynomial or construct a support
splitting field.

Once `Lambda` is available at precision `P`, these unit solves and monic
divisions preserve absolute `P`-digit accuracy in the integral scaled
coordinates. Known ranks and leading weights fix all truncated output
degrees. This does not erase precision costs already incurred in
constructing the saturated input lattice.

## 4. Scaling and the original low-degree matrix

Write `n=2g+1`. For an integer `L>=0`, set

    X=2^(2L)x,       Y=2^(nL)y,
    f_L(X)=2^(2nL) f(2^(-2L)X).

The new curve polynomial is again monic integral. A monic pair of
degree `e` transforms by

    a_L(X)=2^(2eL) a(2^(-2L)X),
    b_L(X)=2^(nL) b(2^(-2L)X).                       (8)

If `e<=g` and coefficient poles are at most `L`, both polynomials in
(8) are integral: for `b`, the exponent `n-2j` is at least three.
Thus the same known `L` makes all native reduced input blocks AND the
unknown good output pair integral. This is sufficient for the direct
scaled product implementation. Arbitrarily high-degree blocks need not
retain integral `b_L`; do not extend this particular assertion to them.

There is nevertheless a direct proof of (1) for the original integral
input scope, independent of a block-degree restriction. Let
`T=R/(A)`, with its basis `x^j,x^j y`, `0<=j<m`. The scaled polynomial
`A_L=2^(2mL)A(2^(-2L)X)` is monic integral. Under the generic coordinate
isomorphism its quotient lattice `T_L` is diagonal in that basis, with
scalings `2^(2jL)` and `2^((2j+n)L)`. Hence, with

    C=(2m+n-2)L=(2m+2g-1)L,

one has

    2^C T subset T_L subset T.

Intersect both lattices with the SAME generic input ideal and take
quotients. Writing the resulting free lattices as `B` and `B_L`,

    2^C B subset B_L subset B.                       (9)

The scaled output pair is integral when `L>=S`. The theorem above
therefore makes scaled RR at `N` surjective onto `B_L`. Its monomial
RR lattice is contained in the original one: a monomial of pole weight
`w` is multiplied by `2^(Lw)`. Thus every element of `2^C B` is already
in the image of the ORIGINAL RR map. This proves that `2^C` annihilates
`coker M*`, giving (1) and the maximal-minor-content bound `mC`.

This comparison uses a proof-only scaled saturated quotient; its
definition does not require that every transformed input `b_i` be
integral. The native implementation with reduced blocks has the simpler
integral construction stated immediately after (8).

Finally, unscaling the extracted degree-`g` pair loses at most `nL`
absolute digits. Thus `P>=M_out+nL` suffices for `M_out` output digits,
in addition to the separately charged product/membership-map precision.
All dimensions, polynomial degrees, scaling exponents and bit operations
are polynomial in the charged native parameters and these numerical caps.

## Remaining scope

This proves the previously missing low-degree RR cokernel bound and a
concrete canonical-pair extraction, assuming the actual saturated input
membership map is supplied by its separate construction. Good unknown
output coefficients are a PROOF premise furnished by the separate
randomization theorem, not algorithmic output advice. No unresolved
integral duality or extra maximal-minor content term remains in this step.
This review does not by itself complete the whole finite-precision
saturation loop or assert a full local-image/Selmer algorithm.

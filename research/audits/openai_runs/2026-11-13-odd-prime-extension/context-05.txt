# Uniform saturation and RR bounds for native graph ideals

2026-11-13. Independent constructive review after current STATE/TRAPS and
Sections 2--4 of the completed
`audits/openai_runs/2026-11-13-dyadic-nonspecial-rr-compiler/response.md`.
No API, network, Git, implementation or numerical sweep. Commands used
`/opt/anaconda3/bin/python`; parent owns the shared notes.

## Verdict and scope

ACCEPT a uniform bound for the compiler's KNOWN-RANK ideal-product and
high-degree RR subspace computations. Pairwise support separation is not
needed. Coincident and arbitrarily close support points are included.

For integral graph blocks on the native monic model, the product quotient's
vertical torsion is killed by `(4 disc f)^(k-1)` for k blocks. If one saturates
after every product stage, each stage's nonzero Smith exponents are at most
`D+2`, where `D=v2(disc f)`. The final RR projection at
`N=m+2g+1` is actually surjective OVER Z2, and its maximal minors include a
unit. The top pole coefficient on the integral RR lattice is primitive too.

For graph coefficients with pole bound S, including high-degree b blocks,
explicit polynomial bounds are given below. A weighted change of variables
does NOT in general make a high-degree b integral. The proof pays its
remaining denominator instead of assuming it disappears.

This proves the missing loss bound for these particular linear-algebra
steps, given access to the input coefficients at the required precision.
Section 6 additionally proves a deterministic canonical materialization
attempt which succeeds whenever the true degree-g output obeys a given
coefficient cap. That cap is used for scaling and for the proof, not supplied
as unknown output coordinates. Two low-degree RR spaces suffice.
It does not bound the residual-divisor discriminant/resultant content of a
random section, Stoll's halving matrices, or an entire saturation-loop DAG.
It does not itself transfer the coordinate Haar event to a finite grid.
No ONE-HALF or complete native local-image claim is made.

## 1. An elementary almost-inverse for an integral graph ideal

Let O=Z2, K=Q2, d=2g+1, and

    R=O[x,y]/(y^2-f(x)),
    I=(a,y+b),       a monic, a,b integral, a | f-b^2.

Write `c=(f-b^2)/a`, which is integral by monic division, and set

    I^vee=(a,y-b),       M=I^vee/a.

These are fractional R-modules inside its fraction field when necessary.
The ring R is a domain because f has odd degree. Direct multiplication gives

    I M = (a,y+b,y-b,c) =: H  subset R.                 (1)

In particular `2y,2b,a,c` belong to H. Differentiating `f=b^2+ac` gives

    f' = 2b b' + a'c + ac'  in H.

Also `4f=(2y)^2` belongs to H. The integral Sylvester-adjugate identity
`U f+V f'=disc f` therefore implies

    delta R subset I M subset R,       delta=4 disc f. (2)

Its valuation is `D+2`. This is an explicit graph-ideal identity; no general
assertion about a singularity conductor is required.

The quotient `R/I=O[x]/a` is finite free, so I is 2-saturated. Here and below

    J^sat = J[1/2] intersect R.

This is vertical saturation, not integral closure of an ideal.

**Product lemma.** Suppose I and J are 2-saturated ideals and a fractional
module M satisfies `I M subset R` and `kappa in I M`, for nonzero kappa in O.
Then

    kappa (I J)^sat subset I J.                        (3)

Indeed, z in `(I J)^sat` lies in I because I is saturated. For t in M,
`tz` is therefore in R. Some `2^n z` belongs to I J, so `2^n tz` belongs
to J. Saturation of J gives `tz in J`. Express kappa as a finite sum of
products from I and M and multiply that expression by z to obtain (3).

Apply (3) successively to integral graph ideals I_1,...,I_k. Their individual
quotients are flat, and induction gives

    delta^(k-1) (I_1...I_k)^sat subset I_1...I_k.        (4)

Thus the 2-primary torsion of `R/(I_1...I_k)` has exponent at most
`(k-1)(D+2)`. The argument never divides by a difference of support points.

## 2. Consequence for the actual product matrices

Let `m=sum e_i`, `A=product a_i`, and `T=R/(A)`. Its standard coefficient
lattice is free of rank 2m with basis

    1,x,...,x^(m-1), y,xy,...,x^(m-1)y.

The product of the first i graph ideals contains A. Its image in T has
generic rank `r_i=2m-sum_(j<=i)e_j`, exactly the rank used in the report.
Its saturated lattice is the image of the saturated ideal in R.

Suppose V_(i-1) is an integral normalized basis for the previous saturated
lattice. The matrix

    C_i=[ a_i(X)V_(i-1) | (Y+b_i(X))V_(i-1) ]          (5)

has image `I_i J_(i-1)/(A)`, with J_(i-1) the preceding saturated ideal.
Equation (3) implies

    2^(D+2) image(C_i)^sat subset image(C_i).           (6)

Consequently EVERY nonzero Smith exponent of C_i is at most D+2. The
minimum valuation of a nonzero rank-r_i minor is at most `r_i(D+2)`.
The first stage in fact has no torsion, but the uniform bound is sufficient.

An integral basis with identity pivot rows is precisely a basis of the
saturated lattice: the coefficients of any integral vector in its K-span
are its pivot-row entries. Thus the source report's minimum-valuation
normalization satisfies the hypothesis needed at the next stage.

Known rank is essential for the numerical procedure. Once the bounded
nonzero pivots have been found, one stops at r_i; one does not attempt to
certify arbitrary exact zero entries from finite approximations.

## 3. Why the final RR projection has a unit minor

Use the standard proper odd-degree model C/O. Its two affine descriptions
are `y^2=f(x)` and

    w^2=u F_infty(u),
    u=1/x, w=y/x^(g+1), F_infty(0)=1.

It is a finite flat double cover of P1, with pushforward
`O_P1 direct-sum O_P1(-g-1)`. Hence every fibre has arithmetic genus g.
It is Gorenstein, and its infinity section is smooth and Cartier: the
u-derivative of the second equation at infinity is a unit.

The special fibre is GEOMETRICALLY INTEGRAL. Over an algebraic closure of
F2, the reduction of monic f still has odd degree. Its pole order at infinity
is odd, so it is not a square in the rational function field. Thus
`y^2-f_bar(x)` is irreducible. This assertion does not require good reduction
or a smooth special fibre.

Let J be the horizontal saturation of the generic product ideal. Because
J contains the monic A, Q=R/J is finite flat of rank m over O. Its support
is closed in the affine chart and extends to a finite flat subscheme of C
disjoint from infinity. Let the resulting ideal sheaf be J_C.

Flatness of Q makes the special-fibre sequence

    0 -> J_C,k -> O_Ck -> Q_k -> 0

exact. Therefore J_C,k is rank-one torsion-free of degree -m on the
integral Gorenstein curve C_k. For any n with `n-m>2g-2`,

    H^1(C_k, J_C,k(n infinity))=0.                      (7)

Here is the complete degree argument: by Serre duality a nonzero H^1 would
give a nonzero map from this rank-one torsion-free sheaf to the dualizing
line bundle of degree 2g-2. On an integral curve the map is injective, with
finite-length cokernel. That forces the source degree to be at most 2g-2,
a contradiction. This also covers genus one and singular special fibres.

The analogous H^1 over O vanishes: multiplication by 2 on that finite
O-module is surjective by (7) and the reduction exact sequence, so Nakayama
applies. The full integral lattice of ambient sections is exactly

    B_N={x^j:2j<=N} union {x^j y:2j+d<=N}.

Indeed the affine coordinate ring is O[x] direct-sum O[x]y, and the two
sets of monomials have distinct even/odd pole orders at smooth infinity.
There is no uncharged change of global-section lattice here.

At `N=m+d=m+2g+1`, (7) proves that restriction is surjective over O:

    O^(m+g+2)=H^0(C,O(N infinity)) -> Q=O^m.            (8)

The normalized quotient map Lambda_D in the source report identifies
`T/J` with O^m: its identity nonpivot block makes that identification
unimodular. Hence `M_D=Lambda_D E_N` is exactly the integral map (8).
All its nonzero Smith exponents are zero. Its integral kernel is exactly
`H^0(C,J_C(N infinity))`, not a substitute coefficient lattice.

The same argument applies at N-1, because `N-1-m=2g>2g-2`. Thus

    H^0(C,J_C(N infinity)) -> O_infinity(N infinity)

is surjective. In the displayed monomial basis this is the top pole
coefficient alpha, up to a unit. Therefore alpha is primitive on the
integral saturated RR kernel. Some vector of any integral basis has unit
alpha, visible modulo 2. This pays top-pole normalization, not the residual
discriminant or the other rejection polynomials.

## 4. Nonintegral graph coefficients, including high-degree b

Now let the original graph blocks be over K, with every coefficient of
a_i and b_i having valuation at least -S, where S is a nonnegative integer.
The leading coefficient of a_i is one, `deg b_i<e_i`, and
`a_i | f-b_i^2`. Assume e_i>=1; empty blocks can be omitted.

Make the common weighted change

    X=2^(2S)x,       Y=2^(dS)y,
    F(X)=2^(2dS) f(2^(-2S)X).

F is monic integral of degree d, with

    D'=v2(disc F)=D+2S d(d-1).                          (9)

Set

    A_i(X)=2^(2e_i S) a_i(2^(-2S)X),
    B_i(X)=2^(dS) b_i(2^(-2S)X),
    bcap_i=max(0,2e_i-d-1)S,       bcap=max_i bcap_i.

A_i is monic integral and B_i has coefficient poles at most bcap_i.
For e_i<=g+1 this bound is zero; for larger blocks it need not be zero.
Increasing S in this same weighted scaling would not fix that issue.

Work in `R'=O[X,Y]/(Y^2-F)`. Put

    I_i^+=(A_i,Y+B_i),
    I_i^-=(A_i,Y-B_i),
    J_i=(I_i^+[1/2]) intersect R'.

J_i is the horizontal closure ideal. It is saturated and its quotient is
finite flat of rank e_i. Explicitly, the image algebra in K[X]/A_i is
`O[X]/A_i + B_i(O[X]/A_i)`; it is closed under multiplication because
`B_i^2=F mod A_i`, and is a lattice between the monic power-basis lattice
and `2^(-bcap_i)` times that lattice.

Write B=bcap_i for the next calculation. Monic division gives the two bounds

    2^B I_i^+ subset J_i subset 2^(-B) I_i^+.           (10)

For the second inclusion, if `r=u+vY` is in J_i, then
`q=(u-vB_i)/A_i` is a polynomial, and `2^B q` is integral. Use
`r=q A_i+v(Y+B_i)`. This argument is valid for repeated roots as well.

Define

    H_i=I_i^+ I_i^-/A_i
       =(A_i,Y+B_i,Y-B_i,(F-B_i^2)/A_i).

Monic division shows `H_i subset 2^(-2B)R'`. The derivative calculation
in Section 1, now clearing the coefficients of B_i' and
`((F-B_i^2)/A_i)'`, proves

    2^(2B) * 4 disc F in H_i.                          (11)

Take the fractional module `M_i=2^(3B) I_i^-/A_i`. Equations (10)--(11)
give

    J_i M_i subset 2^(2B) H_i subset R',
    2^(6B) * 4 disc F in 2^(4B) H_i subset J_i M_i.     (12)

Thus the product lemma applies to J_i with scalar valuation
`D'+2+6B`. In particular, the product of all horizontal closure ideals has
torsion exponent at most `(k-1)(D'+2+6 bcap)`.

The actual two-generator multiplication matrix uses I_i^+, not a supplied
basis of J_i. After multiplying that matrix by 2^B its image is generated
by `2^B I_i^+`. Equation (10) implies

    2^(2B) J_i subset 2^B I_i^+ subset J_i.

Consequently, for every product stage with the preceding subspace saturated,
the nonzero Smith exponents of this cleared matrix are at most

    K_prod'=D'+2+8 bcap.                               (13)

No construction of an integral closure, a maximal order, or a support field
is hidden in this bound. It applies to the original two-generator matrices
after the explicit variable scaling and denominator clearing.

The final quotient in R' is still the horizontal saturation of a generic
degree-m divisor, contains `product A_i`, and is finite flat. Section 3
therefore applies unchanged: the scaled high-degree RR map has unit minors,
and its top pole coefficient is primitive.

## 5. Explicit bounds for the unscaled matrices too

The scaled implementation is sufficient, but one can also bound exactly the
unscaled coefficient matrices written in the paid report. This prevents
the proof from relying on an unnoticed favorable lattice.

Use these conservative integers:

    W=S(d+2m),
    E=S(1+m max(d,m)),
    N=m+d,       E_N=floor(N/2)mS,
    K_prod=E+K_prod'+W,
    K_RR=E_N+W.                                       (14)

The original standard lattice L in T and the scaled one L', transported
through the variable change, satisfy

    2^W L subset L' subset L.

This follows directly from the diagonal monomial scaling factors
`2^(2jS)` and `2^((d+2j)S)` for j<m. The same inclusions hold for the
intersection of either lattice with any fixed K-subspace, and for the
induced quotient lattices.

The original multiplication matrices have coefficient poles at most E:
the product A has poles at most mS, its companion matrix has poles at most
mS, and the degrees evaluated in it are at most max(d,m). Multiplication
by an integral normalized previous basis adds no pole loss.

After multiplying C_i by 2^E, its image contains 2^E times the image of
the corresponding scaled cleared matrix. Indeed the scaled generators
are the old ones multiplied by the integers `2^(2e_iS)` and `2^(dS)`,
and the previous scaled saturated lattice is contained in the old one.
Equation (13), followed by the lattice inclusion with exponent W, gives

    2^K_prod (image(C_i[1/2]) intersect L)
       subset image(2^E C_i).                          (15)

Every nonzero Smith exponent of `2^E C_i` is therefore at most K_prod.
The least valuation of a nonzero rank-r_i minor is at most `r_i K_prod`.

For the RR matrix, reduction of the ambient monomials modulo A has poles
at most E_N. The normalized quotient matrix Lambda_D is integral. The
scaled ambient section lattice lies inside the original ambient section
lattice and surjects onto the scaled quotient lattice by (8). Hence

    2^K_RR O^m subset image(2^E_N M_D).                 (16)

The nonzero Smith exponents of this cleared m-row matrix are at most K_RR,
and its least maximal-minor valuation is at most `m K_RR`.

The top coefficient on the original integral saturated RR kernel also has
content at most NS: transport an integral scaled section with unit alpha;
its original leading coefficient is `2^(NS)` times a unit. Thus even this
normalization has a polynomial numerical bound in the original coordinates.

All formulas are polynomial in g,m,D,S, with m=O(g) in the proposed compiler.
There are at most m product stages of dimension 2m. Known-rank DVR elimination
uses the bounded pivot valuations additively: requested output precision
plus the sum of these explicit determinant/clearing losses suffices.
Matrix formation has bounded polynomial degree and the displayed input
pole bounds, so its additional precision loss is polynomial too. This is
a uniform numerical precision statement, not merely a field-operation count.

The coefficients still have to be evaluated to that precision by the actual
input representation. The remaining random-section content bounds, finite-
grid materialization/stability, Stoll decisions and whole-loop precision
composition are separate obligations.

## 6. Low-degree canonical materialization on the coordinate-good event

The preceding high-degree vanishing argument alone would NOT pay an RR
computation at `N_0=m+g`. The following additional algebraic argument does.
It also extracts b without dividing by q modulo the output a.

Assume the input effective graph-block sum D has total degree m>=g and
represents `h=[D-m infinity]`. Assume its TRUE reduced representative is
`[a_out,b_out]` of degree exactly g, and its coefficient poles are at most
S_out. Input coefficient poles are at most S_in. Set

    L=max(S_in,S_out),
    X=2^(2L)x, Y=2^(dL)y,
    f_L(X)=2^(2dL)f(2^(-2L)X),       N_0=m+g.

Both bounds are known numerical parameters; the output pair is not an
input to the procedure. In these variables the true output polynomials
`a_*,b_*` are integral, a_* is monic of degree g, and `deg b_*<g`.
Indeed their nonleading coefficient valuations are at least
`2L-S_out` and `3L-S_out`, respectively.

All input a blocks are integral too. For the parent's selected invariant,
input blocks have e_i<=g (canonical generators and explicit point blocks),
so their b blocks are also integral. The per-stage bound is then simply
`D_L+2`, with `D_L=D+2L d(d-1)`. The general higher-degree-block proof in
Section 4 remains available if required.

Let J be the horizontal saturation of the input conjugate-divisor ideal,
and let A be the product of the scaled input a blocks. Over K the one-
dimensional RR space `L(N_0 infinity-iota D)` has a generator F with

    div(F)=iota D + D_* - N_0 infinity,

where D_* is the true reduced effective divisor. Its dimension is one:
`L(D_*)=K` for a degree-g reduced graph divisor. One can check this last
fact directly by writing a section as `H/a_*`; then H lies in
`L(2g infinity-iota D_*)`. That ambient space contains only polynomials in
X of degree at most g, and vanishing on the graph means divisibility by
the monic degree-g a_*. Thus H is a scalar multiple of a_*.

Choose F primitive in the integral coefficient lattice and write

    F=p+qY,       alpha=its coefficient of pole order N_0.

The output divisor is finite of degree g, so F has exact pole order N_0.
With epsilon=+1 for even N_0 and -1 for odd N_0, its norm satisfies

    p^2-f_L q^2 = epsilon alpha^2 A a_*.                (17)

Primitivity of p,q forces the norm to be primitive too. Otherwise reduction
modulo 2 would give `p_bar^2=f_L,bar q_bar^2`; the odd-degree monic f_L,bar
is not a rational square, so both p_bar and q_bar would be zero. Since A
and a_* are integral monic, (17) implies `v2(alpha)=0`. Normalize F so
alpha=1. No unknown small leading coefficient remains.

For the proof only, form

    G_0=F(Y+b_*)/a_*.                                 (18)

This is integral. In fact `a_* | p+q b_*`, and with
`c_*=(f_L-b_*^2)/a_*`, its two polynomial coefficients are

    (p b_*+q f_L)/a_* = b_*(p+q b_*)/a_* + q c_*,
    (p+q b_*)/a_*.

Monic division makes both integral. Generic divisor calculus shows that
G_0 also lies in J: multiplication by `(Y+b_*)/a_*` removes the D_*
part of div(F), while preserving the required input divisor iota D.
Its pole is N_0+1, with leading coefficient one.

Write `G_0=r_0+s_0Y`. The determinant of F and G_0 over O[X] is

    p s_0-q r_0 = (p^2-f_L q^2)/a_* = epsilon A.       (19)

They generate J over O[X]. To see this without assuming any model
invertibility, their generic ideal has colength m and is contained in
J[1/2], hence is equal to it. For z in J, the two generic polynomial
coordinates in this basis are obtained from the adjugate matrix divided
by epsilon A. Their numerators are integral and A is monic, so these
coordinates are integral. Thus `J=O[X]F+O[X]G_0`.

The leading pole orders N_0 and N_0+1 have opposite parity. They are unit
leading coefficients, so F,G_0 give an integral weighted polynomial
reduction basis: subtract the appropriate X-multiple to remove any term
of weight at least N_0. Leading terms from the two families cannot cancel.
It follows that

    R_L/J has O-basis {X^j:2j<N_0}
                       union {X^jY:2j+d<N_0}.          (20)

There are exactly `N_0-g=m` such monomials because N_0>=2g. Therefore BOTH
restriction matrices at N_0 and N_0+1 are surjective over O, with unit
maximal minors. Their integral kernels have respective bases F and
`F,G_0`. This pays the low-degree RR losses which high-degree nonspecial
vanishing alone did not address.

Here is an actual computation using no unknown output polynomial:

1. Build J's saturated image by the product matrices already bounded above.
2. Form its restriction matrices at N_0 and N_0+1. Look for full row rank
   modulo 2; abort the attempt if absent. Use unit pivots to compute their
   integral kernels.
3. Choose F in the first kernel with pole-N_0 coefficient one, and G in
   the second with pole-(N_0+1) coefficient one. Abort if these unit
   coefficient choices are unavailable. Subtracting a multiple of F to
   clear G's pole-N_0 coefficient is optional.
4. Write `F=p+qY`, `G=r+sY` and compute by monic polynomial division

       a_*=(p^2-f_L q^2)/(epsilon A),
       b_tilde=(p r-f_L q s)/(epsilon A),
       b_*=remainder of b_tilde modulo a_*.

On the coordinate-good event every test passes. Any such G equals
`G_0+lambda F` with lambda in O, so

    p s-q r=epsilon A,
    G conjugate(F)/(epsilon A)=Y+b_*+lambda a_*.

This proves the signs and both divisions in step 4, including when q=0,
when supports coincide, and when input and output supports overlap.
There is no inverse of q and no support-separation test.

The acceptance checks are sound independently of the output cap: successful
unit kernels and unit top coefficients produce F,G with those distinct
leading weights. Their monic weighted basis has quotient rank m, so their
ideal equals the already constructed J. Its determinant is epsilon A:
the presentation determinant gives the characteristic polynomial A of X
on the generic input divisor algebra, and the leading-weight parity gives
the scalar epsilon. Closure under Y then makes both
quotients in step 4 polynomial and gives `a_* | f_L-b_*^2`; the leading
terms make a_* monic of degree g. The resulting divisor has the required
Jacobian class because `J=(F/a_*)(a_*,Y+b_*)`, whose inverse graph-ideal
identity gives `div(F)=iota D+D_*-N_0 infinity`. Failure of a unit check
means ABORT, not an asserted exact rank drop.

Finally convert back by

    a_out(x)=2^(-2gL) a_*(2^(2L)x),
    b_out(x)=2^(-dL) b_*(2^(2L)x).

This costs at most dL additional absolute 2-adic digits. Matrix dimensions,
polynomial degrees, discriminant inflation, product saturation losses and
output conversion are all polynomial in g,m,D,L. The final kernel solves
and monic divisions have unit denominators in the scaled model. Thus this
is a genuine bounded-precision canonical materializer on the stated good
event, assuming the input DAG can supply the requested coefficients.

The earlier Haar theorem supplies a uniform cap for true reduced coordinates
on a set of large Haar probability; its nongeneric degree-drop locus has
measure zero. Turning that probability into success for an actual finite
grid, paying the input DAG throughout the loop, and paying Stoll's halving
step still require their separate proofs. No finite-grid or ONE-HALF claim
is inferred here.

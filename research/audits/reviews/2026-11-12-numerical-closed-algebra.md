# Extracting the numerical closed divisor algebra by RR quotients

2026-11-12. Focused review after current `STATE.md`, the numerical-lifting
note, the normalization-lattice review, and the target-closure
`etale-reconstruction.md` packet. Only the missing section-subspace to
closed-algebra conversion is considered. No Git, network, API, archive,
code, or numerical test. Interpreter if needed: `/opt/anaconda3/bin/python`.

**Disposition.** This step is proved using ONE class-dependent numerical
Riemann--Roch subspace and unit-pivot linear algebra. A Macaulay or
Groebner calculation over a nonfield is unnecessary. The finite divisor
algebra is already the restriction quotient of two RR spaces. A small
increase of the pole bound permits multiplication by the plane
coordinates inside that same ambient space. All new solves have unit
minors for geometric reasons, and preserve the supplied P-adic precision.

## 1. Inputs and what is not being assumed

Write R_e=O_L/P^e, where L is the charged unramified local extension used
by the numerical torsion algorithm; let f be its residue degree. The
input includes a faithful smooth proper curve model X over O_L, of
genus g, and its two paid normalization charts, multiplication tables,
and exact generic RR coordinates. Their reductions are faithful and
the relevant integral section lattices are saturated. The generic
coefficient field K_b and its chosen P-adic embedding are charged.
Work on one geometrically connected component; apply the construction
componentwise over the paid common field for the full frame cover.

The numerical torsion/canonical extraction supplies a flat effective
Cartier divisor D_t of degree g over R_e, via its numerical KM/RR data.
Residue h0(t+g b)=1 is what previously paid its unique compatible lift.
We do NOT assume a closed ideal for D_t, multiplication matrices on it,
an inverse-Abel algorithm beyond that paid extraction, individual
support points, or an exact global torsion field.

The numerical RR primitive in the question computes the FULL section
subspace H0(X_e,O(A-D_t)) inside the known H0(X_e,O(A)), with faithful
residue reduction. We use exactly this primitive, at a polynomially
enlarged A. Calling it on the supplied numerical KM divisor is not
calling RR on an as-yet-unconstructed closed ideal.

The divisor avoids the pole supports of the coordinates, the singular
plane locus, and the chosen normalization denominators already in the
finite bad set. Avoidance is imposed on the residue divisor, so these
functions remain units wherever needed over R_e. Nonreduced and
nonsplit support are allowed.

The case g=0 has D_t=0 and is empty. Assume g>=1 below. More generally
the same construction works for a degree-m divisor after replacing the
degree thresholds 3g by 2g+m and the output rank g by m.

## 2. A polynomial pole bound, with room for coordinate multiplication

First use a monic finite plane generator, with x=pi and

    F(x,y)=y^delta+sum_(i<delta) a_i(x)y^i,
    deg_x a_i<=D,   delta<=D.

Let H=pi^*(infinity), a relative effective Cartier divisor of degree
delta, disjoint from D_t. Both x and y are sections with controlled
poles:

    x in H0(O(H)),    y in H0(O(D H)).                   (1)

This is integral, not only a generic-fibre valuation estimate. For
u=1/x, the element u^D y satisfies a monic equation whose coefficient
of its i-th power is u^(D(delta-i)) a_i(1/u), a polynomial in u.
It therefore belongs to the integral normalization chart at infinity.

Set

    k=ceil(3g/delta),    C=D H,
    A=(k+D)H,           A_0=A-C=kH.                     (2)

Then

    deg(A_0-D_t)=k delta-g >= 2g,
    deg A <= 3g+delta+D delta = O(g+D^2).                (3)

All supports of A,C are disjoint from D_t. Define the known spaces

    V=H0(O(A)),        V_0=H0(O(A_0)),
    W=H0(O(A-D_t)).                                     (4)

Only W is class-dependent and numerical. Its dimension and the
ambient dimension are

    q=rank V=deg A-g+1,
    rank W=deg A-2g+1=q-g.                              (5)

The paid finite normalization basis and its Laurent transition matrix
also give an explicit polynomial coefficient truncation. If the
transition and inverse have exponents bounded by T, sections of O(jH)
have polynomial coefficients of degree at most j+T in the finite-chart
basis. Thus j=k+D in (2) uses degree at most k+D+T and at most
delta(k+D+T+1) scalar slots. T and the basis numerator degrees/bits
were already bounded in the normalization-lattice construction. No
unbounded ideal-membership computation is hidden in (4).

If the original F is not monic, use the already paid transformation
Y=q(x)y to a monic generator, and use its polynomially bounded degree
D' in (1)--(3). Compute multiplication by x,Y first. The original
coordinate is then recovered by

    M_y=q(M_x)^(-1) M_Y.                                (6)

The zeros of q must be included among the forbidden normalization
denominators. Since q is a unit on the residue divisor, (6) is another
unit solve. This keeps A a multiple of pi^*(infinity), as requested;
it does not require numerical RR for an arbitrary new finite pole
divisor. More general given coordinate ratios are handled in the same
way when their denominators are included in the avoidance set.

## 3. The quotient is the closed divisor algebra

For either L=O(A-D_t) or L=O(A_0-D_t), the special-fibre degree is
greater than 2g-2, so H1(L)=0. Cohomology and base change, or induction
through the square-zero layers P^j/P^(j+1), shows that H0(L) is free
over R_e, commutes with residue reduction, and has H1=0 over R_e.
The same applies to O(A) and O(A_0).

Because D_t is finite flat of degree g,

    Q=H0(D_t,O_D_t)

is free of rank g over R_e, including for nonreduced D_t. The canonical
section 1 trivializes O(A) and O(A_0) along D_t, since their poles are
disjoint from it. The restriction exact sequences therefore give

    0 -> W -> V -> Q -> 0,                              (7)
    V_0 -> Q surjective.                               (8)

These are actual restriction maps, so (7) identifies V/W with the
closed divisor algebra as a MODULE. It has not yet asserted that V
is a ring; V is generally not closed under multiplication.

Reduce (7)--(8) modulo P. From any integral basis of V_0 choose g
columns f_1,...,f_g whose residue classes form a complement to W_bar
inside V_bar. Such columns exist by (8). Lift them simply by keeping
those same known RR functions. If w_1,...,w_(q-g) is a basis of the
computed W, the matrix

    T_A=[w_1 ... w_(q-g) | f_1 ... f_g]                 (9)

in a basis of V has nonzero determinant modulo P. Its determinant is
therefore a unit in R_e, and (9) is a basis of V at the full precision.
The classes of the f_i are a basis of Q. This is also a constructive
proof that the cokernel of W -> V is flat; arbitrary matrix-rank
heuristics over a nonfield are not being substituted for (7).

## 4. Multiplication matrices from one unit system

Since f_i belongs to V_0 and (1) bounds the coordinate poles,

    x f_i, y f_i in V.                                  (10)

Their coordinates in V are computed from the paid normalization-chart
multiplication tables and exact RR coordinates. Apply T_A^(-1) to
each product. Its last g entries are the coordinates of x[f_i] or
y[f_i] in Q. They are the columns of M_x and M_y. Apply the same
matrix to the known section 1 to obtain the unit vector u_1 in Q.
Equation (6) replaces this direct y calculation in the nonmonic case.

All these operations are correct because (7) is restriction to D_t.
For example, replacing x f_i by its last g coordinates differs from
it by a section of W and hence has the same restriction. Therefore
the matrices commute, obey the curve equation, and represent the
actual multiplication operators, including the nilpotents encoding
multiplicities. No root evaluation or support splitting occurs.

All new coordinate conversions have unit minors:

* A faithful integral basis of V has independent residue functions in
  the finite-chart coefficient space. Some square coefficient minor
  is a unit and extracts the coordinates of products in (10).
* The full W is free and reduces to the true residue RR subspace by
  the paid numerical RR primitive and the vanishing above. A residue
  basis among redundant generators lifts to a basis.
* Matrix (9) is invertible by its explicitly selected residue minor.
* Any denominator matrix in (6) is invertible because its residue is.

Thus all divisions are by units. Computing modulo P^e does not reduce
the number of known P-adic digits. An arbitrary unsaturated section
matrix would not suffice: multiplying a true relation by P can change
its residue kernel and destroy these statements. This is precisely why
the faithful RR-lattice input remains explicit.

If numerical KM stores section evaluations rather than coefficient
vectors, the conversion is still a unit linear solve. Use more than
deg A distinct residue evaluation points outside poles. A nonzero
section of O(A) cannot vanish at all of them, so the evaluation matrix
of V has full column rank modulo P. Select its unit square minor and
solve to recover the coefficient vectors of W. Enlarging the already
paid evaluation bank to this polynomial size uses the same closed-
fibre/unramified-point procedure as the numerical-lifting input. These
evaluation points are auxiliary and do not split or select D_t's support.
If an extension is needed, choose one common finite residue field large
enough in advance, as in that procedure; do not take a compositum of
separately selected point fields.

## 5. The canonical A(T),B(T),C(T) encoding at full precision

Choose the common residue-good integer c supplied by the earlier
pair-collision/tangent exclusion argument, and let

    M_z=M_x+c M_y,
    U=[u_1, M_z u_1, ..., M_z^(g-1) u_1].               (11)

The residue conditions are that eta=F_y-cF_x is a unit on D_t and z
separates its distinct support points. They imply that z is a local
parameter at each point and that its powers generate every thickened
local factor. Therefore U_bar is invertible. This also gives a direct
root-free test: check that both U and eta(M_x,M_y) have unit determinant.

Compute

    (a_0,...,a_(g-1))^T = -U^(-1) M_z^g u_1,
    A(T)=T^g+sum_(j<g) a_j T^j,
    coeff(B)=U^(-1) M_x u_1,
    coeff(C)=U^(-1) M_y u_1.                             (12)

No divisions by integers 1,...,g or a field-only characteristic-polynomial
formula are needed. The relation A(M_z)u_1=0 annihilates every vector
because u_1 is cyclic. Monic division and the basis (11) then prove

    R_e[T]/(A) ~= Q,
    x=B(T),  y=C(T),  z=T.                              (13)

The kernel is exactly (A), not merely an ideal containing A: a remainder
of degree less than g maps to zero only when all its coefficients are
zero. In particular A is also the characteristic polynomial of M_z.
This proof works over R_e and for nonreduced divisors.

The resulting polynomials satisfy

    B+c C=T mod A,   F(B,C)=0 mod A,

and the chosen denominators are units modulo A. Although the auxiliary
bases and unit minors can depend on local choices, the polynomials
(12) are the unique coordinates of the same divisor in the fixed z
power basis. Hence they are independent of all those choices and
compatible with Galois/Frobenius transport of the actual divisor.

## 6. Complexity, exceptional sets, and exact scope

The ambient dimension q is O(g+D^2) in the monic setting, and the
normalization coefficient truncation is polynomial as in Section 2.
Every additional operation is polynomial-size polynomial arithmetic or
linear algebra over R_e. Inversion of a unit can be lifted without loss
of precision. Thus the added bit cost is polynomial in

    D, g, the charged chart/RR presentation size,
    e, f, log P.

The transformed monic equation's degree and height are charged when it
is used. The output comprises g-by-g coordinate matrices or O(g)
coefficients in (12), all to the requested precision. This does not
claim their exact number-field values before rational reconstruction.

For a denominator Delta(x), the number of geometric normalization
points in its zero fibre is at most delta*deg Delta. In the trace-lattice
presentation Delta=disc_y(F), with deg_x Delta<=2D(D-1), this is at most
2D^3. Additional leading-coefficient denominators contribute their
explicit degree times delta. Together with the earlier infinity and
plane-singularity count, all added forbidden points are polynomially
bounded in the presented plane degree. No individual zero or branch
needs to be adjoined to count or avoid them.

The proposed numerator ideal is mathematically valid as well: degree
at least 2g makes O(A-D_t) globally generated, first on the residue
curve and then over R_e by Nakayama. Its sections viewed in O(A)
generate exactly the ideal sheaf of D_t, with multiplicities. Clearing
denominators on the Delta-unit chart therefore gives the stated ideal
(F, section numerators, 1-w Delta), of quotient rank g. This review
does not infer a nonfield Groebner complexity theorem from that fact;
the RR quotient (7)--(12) provides the needed polynomial construction
directly.

The exact generic RR data only uses the constructible basepoint field
K_b and its selected local embedding, as specified in the task. All
class-dependent data in W remains numerical over R_e. No global
torsion field, closed support splitting, pre-existing divisor ideal,
or uncharged inverse-Abel operation is introduced by this conversion.

This closes the numerical section-subspace to closed-algebra microlemma
under the stated paid input contract. It does not re-prove numerical
torsion lifting, good-model construction, or the final Galois-invariant
rational reconstruction and target-prime order algorithms.

## 7. Source-checked completion: construct W from the lifted KM point

This addendum removes the extra W primitive in Section 1. Actual retained
source checked: Mascot `audits/sources/surface_module_2026/mascot_lift.txt`,
Section 2.1.1 and Remark 2.17 (background degree), the DivAdd proof at
physical lines 302--315, DivSub and its all-basis version at 335--399,
Algorithm 7 at 713--780, Remark 2.21 at 825--849, and Theorem 2.23.
The following shorter product construction suffices; it does not need a
canonical divisor ideal or a numerical RR call on that unknown ideal.

**Use a known background from the start.** Take

    D_0=d_0 b,       d_0>=2g+1,
    E_1=(d_0-g)b,    B=(d_0+g)b.                         (14)

Usually d_0=2g+1. The source allows ANY effective background of degree
at least 2g+1; taking d_0 close to 2g+1 is an efficiency convention.
All divisors in (14) are known over K_b. Initialize finite-field KM
and the unique numerical ell-torsion lift with this background. If a
previous lift used a different origin/background, do not silently
reinterpret its matrix: initialize the already known CLOSED residue
classes in (14), using the paid finite-field RR arithmetic, and rerun
the unique torsion lift. This is polynomial additional work and gives
the same torsion points. It makes no assumption of a free high-precision
change of KM representation or of an exact global torsion field.

**Extract a canonical subspace, without its zero ideal.** Feed the
lifted point x=-t to Mascot Algorithm 7 with E_1 as in (14), and stop
after line 5. Let D_rep be the auxiliary degree-d_0 effective divisor
represented by the input KM matrix; it need not be materialized.
The line-2 space is

    L(2D_0-D_rep-E_1) ~ L(gb+t).                        (15)

It has degree g and residue h0=1 by the chosen basepoint promise.
Its residue h1 is also zero, since its Euler characteristic is one.
Consequently this space lifts as a free rank-one module with base
change, and a primitive generator s has divisor identity

    (s)=-2D_0+D_rep+E_1+D_t.                            (16)

Its zero scheme as a section of the line bundle in (15) is a flat
effective Cartier divisor of degree g, since the section is nonzero
on the residue curve. This includes nonreduced zero schemes.

Indeed the source identity is [D_0-E_1-D_t]=x=-t; hence
[D_t-gb]=t, with the required unique effective representative. The
retained prose of Remark 2.21 has the opposite sign in its description
of a normal form. Equation (2.15) and the displayed Algorithm 7
divisor identity, not that prose sign, determine (16).

Line 5 computes exactly

    W_0=L(2D_0-E_1-D_t)=L(B-D_t).                       (17)

The zero divisor in (16) is only used in this proof; computing its
support or ideal is unnecessary. There is no E_2 and no scalar-valued
chart or injectivity assumption from the later steps of Algorithm 7.

Here are the degree and precision checks for lines 1--5. The initial
two product factors have degrees d_0 and d_0+g, so their full product
span has degree 2d_0+g and dimension 2d_0+1. The first DivSub has
denominator L(2D_0), which is globally generated, and its kernel is
the rank-one space (15). Multiplication by the primitive s is injective
on L(2D_0), with independent reduction; its output is a degree-2d_0
RR space. The second DivSub has globally generated denominator
L(2D_0-D_rep), of degree d_0, and output (17), of degree d_0 and
dimension d_0-g+1. All these operations satisfy the source's divisor
bounds inside L(5D_0). Use all basis products and all denominator-basis
constraints, not the practical random shortcuts.

Every high-degree space just listed has H1=0; the exceptional
degree-g space has H1=0 by (15). Their dimensions are the same on
generic and residue fibres. The product spans are surjective on the
residue fibre, and both DivSub kernels have the stated residue and
generic dimensions. Thus the matrices have no rank drop; their
nonzero Smith factors are units. This verifies the hypothesis of the
source's Theorem 2.23, so unit-pivot kernels and equation matrices
compute (17) to the original P^e precision. No division by the
function s at an evaluation point is performed.

**Multiply by a known RR space to obtain W.** Enlarge the A_0 in (2)
to kH with

    deg A_0 >= d_0+3g+1,
    A=A_0+C,       C=D H                               (18)

in the monic setting, or use the same charged monic transformation
as before. This preserves every hypothesis in Sections 2--6 and
keeps deg A=O(d_0+g+D^2). The completely known space

    U=L(A-B)

has divisor degree at least 2g+1, while B-D_t has degree d_0>=2g+1.
The multiplication theorem stated and used in Mascot's DivAdd proof
therefore gives

    U tensor W_0 -> L(A-D_t)    surjective.              (19)

Both inequalities are at least 2g+1; no endpoint refinement at degree
2g is being assumed. Compute ALL basis products in (19) and keep a
residue-independent subset of the known target dimension
deg A-2g+1. The target has H1=0 and is free with base change. Residue
surjectivity followed by Nakayama proves these selected products span
the entire integral/numerical target W. In the known ambient L(A),
they have a unit maximal minor. This constructs the W needed in (7)
using only the numerical point, known RR data, and unit operations.

Computing U does not reintroduce the missing divisor: B is the KNOWN
multiple (d_0+g)b. Inside the known L(A), impose vanishing of order
at least d_0+g at b by setting the jets of orders 0,...,d_0+g-1 to
zero, using its regular-fibre parameter pi-pi(b) and the paid
normalization chart. The required local jet/idempotent is at
the one known basepoint, not at D_t's unknown support. Degree (18)
makes the restriction map onto those jets surjective, so this known
RR computation also has unit pivots and polynomial size. Its exact
generic coefficients use only K_b and its given local embedding.

Do not call the source's L(5D_0)-restricted implementation on the new
pole divisor A without changing its ambient representation. Either
use the already paid normalization coefficient multiplication, or
enlarge the common evaluation bank to more than deg A+5d_0 distinct
residue points outside supp(A) union {b}. The existing common-field
point construction supplies this polynomial bank. Then all original
KM spaces and all new factors/products are faithfully evaluated.
In particular U has its poles in A, W_0 has its poles in B, and their
products have poles only in A, by (19). All evaluation and coefficient
conversions have the unit minors already proved in Sections 3--4.

This supplies the previously missing W input constructively. The
canonical divisor exists by (15)--(16), but its ideal is never queried:
(17)--(19) give its section subspace, and (7)--(13) give its closed
algebra and unique coordinate encoding. The argument is compatible
with transporting b and all known background divisors under Galois;
it does not use an unchanged-origin Frobenius row-permutation rule.

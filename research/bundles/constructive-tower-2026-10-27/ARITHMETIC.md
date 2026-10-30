# Bounded Arithmetic Contract Required By The Source Theorem

This incorporates the independent derivation in
../constructive-tower-review-2026-10-27/REVIEW.md, Sections4-6. Parent review
checked its trace-dual bound, test ideal, Frobenius nilradical construction,
primitive-element selection and reset logic. It is not a certified native
backend or a formal proof-assistant result.

## State At Each Level

Maintain a geometrically integral original-field plane equation F(x,y),
monic and separable in y, of total degree <=2g+2; normalized integral bases
over k[x] and k[1/x]; conversion matrices; divisors as fractional ideals with
COMPLETE infinity multiplicities; and marked places as ideals/residue maps on
the normalization. Plane coordinate pairs alone can merge distinct branches.
Keep actual RR functions and a rational marked point O. Rebuild
R_j=L(j*ell*O), ell=2g+2, through j=7 with exact field multiplication.

Divisor height means max(deg D_+,deg D_-), not abs(deg D). Relative to a
normalized integral basis, an effective finite divisor ideal has colength
deg D; HNF bounds its coefficient degrees. Fractional ideal inversion and
infinity valuations account for the negative part. Never propagate expanded
historical tower expressions as the current field representation.

## Normalization Without A Large-Characteristic Assumption

For a monic separable P(x,T), degree N in T and coefficient degrees <=H,
put A0=k[x][alpha] and delta=disc_T(P). Its normalization B satisfies

    A0 <= B <= A0^vee <= delta^(-1) A0.

The last inclusion follows from the inverse trace matrix. Thus delta*B<=A0
and dim_k(B/A0)<=N*deg(delta), with polynomial degree in N,H.

For each intermediate order A, form J=radical(delta*A). Away from delta,
A0 is etale over k[x] and already normal, so J is a test ideal. The
[Grauert-Remmert criterion, Proposition2.2](https://arxiv.org/html/0904.3561v3#S2)
says A=(J:J) precisely at normalization; otherwise the order strictly grows.
At most N*deg(delta) strict steps are possible.

Keep delta*A as an HNF module between delta*A0 and A0, of polynomial
colength. In A/delta*A, dimension N*deg(delta), the nilradical is the kernel
of a -> a^(q^b) for q^b at least that dimension. This is k-linear; repeated
modular powering constructs its matrix. Lift that kernel to J. Compute
(J:J) inside delta^(-1)A0 by multiplication-containment constraints and
polynomial-module kernels/HNF. The determinant trick keeps all colon elements
integral, preserving the fixed denominator bound. Constant nonzero delta
is the already-normal case. Repeat over k[u], u=1/x, after a polynomially
bounded integral scaling of alpha, for infinity arithmetic.

This finite-module route, not arbitrary growing-variable Groebner expansion,
justifies polynomial normalization even when characteristic <=N. RR then
uses the two ideal lattices and polynomial-matrix reduction of the classical
Appendix B of Eisentraeger-Hallgren. Defining-equation size, normalized bases
and divisor heights are charged; extension degree alone is insufficient.
The quantum unit/class-group routines in that paper are NOT used.

## Bounded Radicands And Next Model

From the certified rational2-primary presentation, represent each order-two
class by an effective E_i of degree ell with class [ell O-E_i]. Its negative
is the same class, so choose D_i=E_i-ell O and compute

    0 != f_i in L(2ell O-2E_i),  div(f_i)=2E_i-2ell O.

All f_i are regular away from O. The product of at most2g of them has pole
degree <=4g*ell=O(g^2). Recover E_i from its medium-model subspace using
its actual base ideal and the infinity valuation, not an abstract class label.
Local uniformizers come from P/P^2 on the normalization; leading units and
the necessary truncated expansions have polynomial precision bounds.

For z^2=f, use {y^i,y^i z} over k(x). Dimension and entry degrees are
polynomial in current g. To get a primitive presentation, try
alpha=y+c(x)z for more than N(N-1)/2 distinct polynomial c of degree
O(log_q N). Each pair of embeddings excludes at most one c; a full-degree
minimal polynomial is certified by linear algebra over k(x). Because y,z
are integral away from old infinity, this presentation is monic integral.
It has polynomial degree before normalization, so the procedure is not circular.

After normalization, choose one rational lift O' and functions with sole
pole orders2g'+1,2g'+2. Coprime poles prove they generate the same field.
Use the order prime to p for the separating coordinate. Their unique
weighted relation has total degree2g'+2. Recompute integral bases in this
fresh model, resetting representation size with a fixed polynomial exponent.
Store adjacent coordinate maps, not an expanded full tower composition.

Retain ALL marked branches. Pull back new integral-basis elements and use
regularized local residues to transfer their ideals/residue maps, including
displayed0/0 expressions. Choosing O' does not discard its other rational
sibling. One-point RR can also produce bounded denominators for inverse
coordinate maps, so those maps need not invoke unrestricted elimination.

## Remaining Cost And Verification

Use the reviewed fixed-p plane-order algorithm, bounded prime-class sampler,
normalized perfect Frey-Ruck pairing and relation-lattice saturation. The
known order2^s certifies full2-primary generation; include the O(s^4) internal
relation rows and their pairings, not only4s outer proposals. No odd-part
factorization or discrete logarithm is required. All adaptive tests need
fresh samples, not a reused random bank.

After each reset, all state has size poly(g). Summing per-level expected
poly(g_j) costs over geometrically growing g_j gives expected polynomial in
FINAL output size, NOT in log(e). There is no practical-runtime claim.

Independent controls include a separable degree4 model in characteristic3
and two distinct normalized branches over the same singular F5 plane point.
They test pitfalls, not the general proof or a working source generator.

# A Prime-Only Weak-Access Source

2026-10-25. Proposed constructive source improvement; independent review
and novelty assessment pending. No geometric quotient, canonical label,
coherent source or quantum recovery is executed in this bundle.

## Scientific Change

The previous dimension-two source required weak evaluations at small prime
SQUARE orders, including four. That requirement came from its chosen
multiplier D^2, not from the hidden-stabilizer problem itself. Modify the
public elementary lift so that its polarization trace t is always ODD.
Then an odd squarefree multiplier N suffices in the same eight-square
construction. All weak queries can be at odd PRIME orders.

This removes an extra source-access assumption and all non-free
prime-square kernel stages. It does not reduce the stabilized dimension
16, turn a short insufficient transcript into an oracle, or establish a
quantum advantage. It preserves the original single isogeny, hidden kernel,
Sp4 action and marked-label equivalence relation.

## 1. Exact Input And Unchanged Dependencies

Keep p>3, ell odd prime distinct from p, the product-polarized A=E^2 with
its full known evaluable order, the ORIGINAL modeled (B,lambda_B), and
one genuine ell-polarized phi:A->B. The paid common definition field
defines phi and all source-order maps. At each requested odd prime r,
the complete ordered source-basis images have ONE common nonzero mask.
The same phi underlies all responses. Compatible fields, point arithmetic,
torsion generation and known source-order splittings remain paid.

The required odd primes are fixed globally below; access to them must be
in the original contract. Prime-only means no weak PHI evaluations at
r^2 or four. It does NOT remove level-4 theta-coordinate machinery from
the PPAV model. Public bounded-order torsion on an already modeled B can
still be required and charged by those imported geometric algorithms.
The one quadratic base extension from SOURCE_FIELD_AUDIT.md makes all
intermediate 8-torsion rational, independently of querying phi there.

The published quotient/product/canonicalization primitives remain those
audited in [Corte-Real Santos--Piasecki--Wesolowski, 2026/1142](https://eprint.iacr.org/2026/1142).
The known four-square algorithms and norm identity remain imported tools,
not new claims. The receiver and full output-postprocessing obligations
are unchanged.

## 2. Force Odd Trace Without Changing The Group Query

For M in Sp4(F_ell), use the existing bounded elementary compiler. Its
word contains at most 156 quaternionic off-diagonal factors E_ab(q).
Instead of a centered lift z_i of each quaternion-basis coefficient,
lift it to

    z_i_even = 2 center_ell((2^(-1) mod ell) z_i).

This preserves the coefficient modulo ell, makes it even, and bounds its
absolute value by ell-1. Let sigma_0 be the product. Every factor is an
integral elementary automorphism, so sigma_0 has an explicit integral
inverse, reduces to M modulo ell, and is I modulo 2 in the FULL integral
source order. No splitting of that order at 2 is required.

Now set

    tau = [[1,ell],[0,1]],   sigma=sigma_0 tau.

Tau is an integral degree-one automorphism, is I modulo ell, and reduces
modulo 2 to [[1,1],[0,1]]. Therefore sigma still reduces to M, and

    S=sigma^dagger sigma = I + ell T0,
    S mod 2 = [[1,1],[1,0]].

The diagonal entries of a quaternion-Hermitian S are integers. Its trace
parameter t=S_11+S_22 is consequently odd. Positivity and Moore determinant
one give t>=2 and S^2-tS+I=0. Thus t>=3, so the old t=2 exceptional case
is absent. This argument does not merely replace an observed even trace
by an odd number; it changes the actual public integral lift.

For B0=sum_i nrd(b_i) in the supplied quaternion basis, the even lift obeys

    nrd(q) <= 4(ell-1)^2 B0.

Submultiplicativity, including the final tau, gives one public bound for
ALL group queries:

    U=2+4(ell-1)^2 B0,
    t <= T=U^156 (2+ell^2).

There are at most 157 quaternionic factors. These bounds use the actual
compiler, not a maximum seen during sampling. All numbers have polynomial
bit length. The reference wrapper reuses the old compiler's factor word;
its old intermediate lift is not the lift used in the new source.

## 3. A Squarefree Multiplier, Not A Squared Denominator

Choose ONE N as a product of distinct successive odd primes excluding
p and ell until N>T^2. For any actual odd t<=T,

    a=t+2, b=t-2, gcd(a,b)=1, N>a*b.

Take X=0 if b=1, otherwise X=N*a^(-1) mod b in [0,b-1], and set
Y=(N-aX)/b. Then X,Y are nonnegative integers and

    (t+2)X+(t-2)Y=N.

No factorization of t+2 or t-2 is needed, and N need not be their multiple.
Represent X and Y as four integer squares. With H=phi S phi^(-1), the
same eight commuting coefficients a_i(H+I), b_i(I-H) now yield

    C^dagger C = C C^dagger = N H8,
    F=H8^(-1) C^dagger,
    F^dagger H8 F=N I,       FC=CF=N I.

H is the SAME integral positive symmetric unit justified in the existing
source proof; H^(-1)=tI-H. Hence F is integral and N-polarized from the
old X=(B,lambda_B)^8 to (B,lambda_B H)^8. Its kernel is killed by N and
has order N^16. A formal ring certificate alone does not prove these
geometric/positivity premises.

## 4. Each Quotient Now Uses Only Prime Torsion

For each r|N, form H_r using the weak images at r and the known S action.
Then form F_r and C_r. Their coefficients only require arithmetic on B[r].
There is no lifting to r^2 anywhere in this procedure.

The r-adic Smith exponents of F are zero or one because FC=N I and
v_r(N)=1. The polarized-degree identity gives valuation 16 for its Tate
determinant. Exactly 16 exponents are one and 16 are zero. The same is
true of C, and FC=0 modulo r therefore gives

    ker(F_r)=im(C_r),   dimension 16.

This is a maximal isotropic subgroup of X[r], by the N-polarized kernel
criterion. This remains true if r divides t^2-4: no separability of the
quadratic polynomial modulo r is used. Such ramified auxiliary cases
are included in the exact controls.

Use linear algebra for a basis, interpret it in the known weak image
basis, and enumerate r^16 points for A26 at the PRIME r. A common nonzero
mask changes the generators but not the subgroup. Push later kernels
and marking points through this quotient, and repeat. Earlier degrees
are coprime to later primes. Scalar Frobenius from the paid source field
makes every kernel descend to the same base, as already proved in the
field audit. No compositum of all auxiliary point fields is taken.

Thus q:X->Y has multiplier N and precisely ker(F). There exists, without
having to compute it, a polarized isomorphism u:Y->(B,lambda_B H)^8 with
u q=F. This is the same universal-property argument as before, with N
in place of D^2. There is no flag choice or non-free kernel branch.

## 5. Marking Transport And Exact Hiding

For each fixed odd marking prime s avoiding p*ell*N, use the original
weak images to form Z=u_s (phi sigma^(-1))^8(P) in the OLD B^8 model.
Reusing the source response across copies preserves one common scalar.
The required marked point is

    q( [N^(-1) mod s] C(H) Z ).

Since F C=N I, it is u_s times the image under the integral ell-polarized
map u^(-1)(phi sigma^(-1))^8. Its kernel is (M K)^8. The old bound

    R=product_s s,       R^2 > 8*16^3*ell^2

and ONE shared polarized isomorphism/automorphism across all levels still
give label(M)=label(M') iff MK=M'K. The parity correction has not changed
the group action: tau reduces to I modulo ell. It can change intermediate
coordinates and polarization, but correct joint canonicalization removes
those choices. Independent per-level automorphism choices remain invalid.

## Resources And Falsifiers

- log N and the largest quotient prime are polynomial in log T, log p and
  log ell. Prime-only auxiliary fields have relative degree at most r-1
  under scalar Frobenius, rather than r(r-1) for the old r^2 requirement.
- Lists still have r^16 points and level-4 theta objects dimension 16.
  Constants remain enormous. The larger trace bound can increase the
  prime list; this is an access-model improvement, not a practical speedup.
- Fixed-width labels, uniform clocks, fixed random tapes and reversible
  compilation still require the old geometric analysis. No coherence or
  canonicalization cost is omitted by changing N.
- Even t can make the odd coin equation impossible: at t=4 its left side
  is even. Merely deleting prime-square requests without changing sigma
  is false. The test suite retains this decisive parity countercontrol.
- An odd nonsquare N is intentional. Substituting N^2 in verification or
  transporting marks with N^(-2) computes the wrong isogeny.
- Repeated prime factors reintroduce higher-order kernels. The plan must
  check squarefreeness by retaining its explicit list of distinct primes.
- Positive H, genuine weak evaluations and modeled PPAV operations remain
  promises. Integral matrix controls are not native geometry or hardness.

This replaces the old source's PRIME-SQUARE weak-access requirement, not
its remaining independent review, geometric execution or classical
advantage obligations. The product-target dichotomy and all other matched
classical attacks still apply unchanged to the original input.

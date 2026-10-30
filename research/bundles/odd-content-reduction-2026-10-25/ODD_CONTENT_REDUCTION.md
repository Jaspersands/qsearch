# Removing The Cyclic-Kernel Promise Without Changing The Source

2026-10-25. Conditional deduction, independently unreviewed. This is not a
new first solution of weak IsERP, not a bare-curve isogeny algorithm, and not
an executed native recovery. The earlier source's full geometric and clock
obligations remain. This pass concerns odd degrees only.

## Decision

The cyclic restriction in CYCLIC_ODD_DEGREE.md can be removed from the
ORIGINAL input, conditional on that full marked Sp4 source. Its elementary
lift, polarization identities, prime-only quotient construction and marking
rigidity do not use a free unknown kernel. The unknown kernel need only be
maximal isotropic of the prescribed order, as it is for any elliptic
degree-n isogeny after doubling.

Classical source comparisons determine the scalar content of the original
isogeny. The existing cyclic phase receiver then operates at smaller primary
moduli through the SAME source. There is no new weak evaluator, transcript,
hidden basis or quantum subroutine in this reduction.

## 1. Local Classification

Let phi:E->E' be an arbitrary separable isogeny of ODD degree n, coprime
to p, with the same full known source order and paid common-field promises.
Write n=product q^e with verified factorization. At a primary component,
identify E[q^e] abstractly with R^2, R=Z/q^e, using the known source order.
No q^e-torsion points are generated.

The local kernel K has order q^e. Its Smith invariants give

    K = q^a R v + q^b R w,
    a+b=e, 0<=a<=b, det(v,w)=1.

If a=b, K=q^a R^2 and has no directional information. Otherwise define
d=b-a=e-2a>0. Dividing by q^a and reducing modulo q^d identifies K with
the primitive line L=Rv modulo q^d. More precisely, K is the inverse image
of that line inside q^a R^2, including q^b R^2. Its direction only depends
on v modulo q^d, not on a chosen lift to q^e.

For any invertible four-dimensional local matrix M,

    M(K direct-sum K)=K direct-sum K
      iff (M mod q^d)(L direct-sum L)=L direct-sum L,   d>0.

For d=0 every M preserves the doubled kernel. This follows directly by
passing to q^a R^4/q^b R^4. It does not assume K is a free R-module.

## 2. Why The Existing Source Still Applies

Set Phi=phi x phi. Regardless of cyclicity, Phi^dagger Phi=[n], and its
kernel K direct-sum K is maximal isotropic in E^2[n]. A symplectic query M
preserves that property. The odd ring lift supplies sigma mod n=M and

    sigma^dagger sigma=I+nT0,
    H=Phi(sigma^dagger sigma)Phi^-1=I+Phi T0 Phi^dagger.

Every expression here remains integral, positive and symmetric as before.
The odd trace identity and prime-only norm decomposition are unchanged.
All quotient primes are coprime to n, so Phi is invertible on their torsion;
the unknown elementary divisors at q|n never enter that computation.

The original trace-free marking proof only uses the polarization multiplier
n and the equality of the marked maps up to the permitted projective
scalars. It never assumes that ker(Phi) is free. Therefore the same proposed
geometric source has the equality relation

    f(M)=f(M') iff M(K direct-sum K)=M'(K direct-sum K).

This checks the specific extension point; it does not independently verify
the imported PPAV primitives or prove that their backend has been executed.

## 3. Determining The Content By Classical Source Comparisons

At each q^e, use the two one-factor unipotents

    U_s=[[1,s],[0,1]],    V_s=[[1,0],[s,1]].

Embed diag(U_s,I2) or diag(V_s,I2) into Sp4(Z/n) by CRT, as identity at
all other components. Compare its ORIGINAL source label with f(I).
For a primitive direction v=(x,y) at depth d>0:

    U_s fixes K iff s*y^2=0 mod q^d,
    V_s fixes K iff s*x^2=0 mod q^d.

With s=q^k, the two acceptance thresholds are

    k_U=max(0,d-2 val_q(y)),
    k_V=max(0,d-2 val_q(x)).

At least one coordinate is a unit, hence

    d=max(k_U,k_V),    a=(e-d)/2.

For d=0 both thresholds are0, giving the scalar case correctly. Testing
k=0,...,e deterministically needs at most2 sum_q(e_q+1)+1 source calls,
including the cached identity label. The acceptance sequences must be
monotone, end in true, and give the indicated parities. Reject a malformed
record; those checks are necessary consistency tests, not a replacement for
the exact-source promise. Binary search can reduce this count but is not
needed for polynomial complexity.

No unknown vectors are inputs to this protocol. Its public query schedule
only uses n and its factors. Actual geometric labels are still required;
the control uses supplied Smith subgroups and is not a solver for phi.

## 4. Use The Same Source At The Smaller Modulus

When d>0, run the previous two-chart square-unit method over Z/q^d.
Implement its PUBLIC affine query at the full q^e level: choose the same
integer root a (a unit modulo q) and translation u, but form

    [[a,u/a],[0,1/a]] mod q^e.

Its reduction modulo q^d is the desired affine query. Charts I and the
coordinate swap have exact integral lifts. Lift any candidate primitive
line vector to q^e, then use certificate_queries at that full modulus,
CRT-embedded into the original n. The local classification proves that
both certificate comparisons succeed iff its reduction modulo q^d is the
correct line. Arbitrarily choosing higher q-adic digits neither creates
advice nor changes the kernel.

Thus the original local success bound at least2/9 and its two-query
certificate remain valid at depth d, including q=3. No attempt is needed
for d=0. Keep the original n-based source plan and all its weak levels;
there is no need to divide or re-query the weak representation.

## 5. Output The ORIGINAL Kernel Ideal

Let c=product q^a and m=n/c^2=product q^d. The original phi kills E[c], so
there is a unique isogeny psi with phi=psi[c] and deg(psi)=m. Its kernel is
cyclic. At each q, the recovered direction at depth d is precisely ker(psi)
under the corresponding source-order splitting. This is a deduction, not
an assertion that the weak input has been converted into a strong psi.

CRT-combine the active local lines modulo m and compute their LEFT
annihilator I_psi by the existing lattice routine. Then

    I_phi = c I_psi,    [O:I_phi]=c^4*m^2=n^2,    nrd(I_phi)=n.

Proof: any a in I_phi kills E[c], so a=b[c] with b in End(E). Conversely,
b[c] kills ker(phi) iff b kills [c](ker(phi))=ker(psi). Central scalar
multiplication commutes with b. This gives equality of the two left ideals,
not merely matching determinants. Their common kernel is the original K.

If m=1, psi is an isomorphism, K=E[c] and I_phi=cO directly. Do not fabricate
a primitive line over the zero-information modulus1. Known IdealToIsogeny
postprocessing is only applied after the true ideal has been recovered.

## 6. Falsifiers, Prior Art And Limits

- A line modulo q^e is the WRONG output for noncyclic K. Only its direction
  modulo q^(e-2a), together with a, determines the original subgroup.
- Measuring only one unipotent family can undercount d. The direction
  (1,q) has k_U=d-2 while k_V=d when d>=2. Both are mandatory.
- Dividing degree n by c instead of c^2 violates the polarization/ideal
  norm identity. Keep the lattice index n^2 as an independent check.
- Do not construct huge q^e-torsion point fields or assume a kernel basis.
  All pre-receiver queries are public arithmetic matrices.
- An incoherent source, bad common masks, noncanonical marked labels or
  uncharged geometry invalidates BOTH the classical content probe and the
  quantum direction step. No classical lower bound is established.
- This does not extend the odd-trace compiler to even n. Removing a large
  2-primary part from a weak representation is not free just because its
  prime is small; naive inverse-point lifting may grow the field degree.

The invariant-factor classification and isogeny scalar-content factorization
are standard. General-degree quantum weak-IsERP algorithms already exist
in Chen--Petit2025. The possible research contribution remains the proposed
replacement SOURCE, not new coverage of an unsolved quantum problem. The
specific reduction here removes our self-imposed cyclic restriction without
silently changing that source's input. Novelty and the geometric chain
remain unreviewed. A fresh attempt to retrieve the full Chen--Petit accepted
manuscript failed: the old institutional PDF URL now redirects to an invalid
identifier, and its public record exposes no downloadable file. Do not
claim a full-proof comparison based on an abstract or indexed excerpts.

Sources and dependencies: ../cyclic-odd-degree-source-2026-10-25/
CYCLIC_ODD_DEGREE.md; ../prime-only-source-2026-10-25/PRIME_ONLY_SOURCE.md;
the fixed-field audit; the original marked-source rigidity proof.
Prior-art record: [Chen--Petit](https://research.birmingham.ac.uk/en/publications/computing-the-endomorphism-ring-of-a-supersingular-elliptic-curve/).

Next decisive task: attack or execute the full same-input marked geometric
source. Another arithmetic subgroup benchmark cannot settle that question.

## Executed Algebraic Scope

In addition to supplied Smith-subgroup controls, the tests use the genuine
endomorphism phi=3(3+4i) on the known characteristic11 source. It has degree
225, scalar content3 and cyclic residual degree25. The reconstructed ideal
equals the principal LEFT ideal O*phi, checked in both lattice directions,
not merely by determinant. The endomorphism and subgroup are supplied;
there is no unknown-kernel recovery, curve-point generation or quotient.

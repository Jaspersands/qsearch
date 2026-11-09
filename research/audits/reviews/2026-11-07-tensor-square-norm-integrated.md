# Tensor-square rational norms: final integrated review

2026-11-07. ACCEPT the written end-to-end bounded-error quantum polynomial-
BIT composition in TENSOR_SQUARE_RATIONAL_NORMS.md under its explicit GRH
and input/output promises. No concrete mathematical or resource blocker
was found. This does not establish novelty, classical separation, an integral
norm solver, or execution of the asymptotic algorithm.

Reviewed current STATE/TRAPS, the complete main note and the closed support,
resource and compact/classical reviews. Actual Biasse--Song2510.02280v2
Theorem1, Section8.2 and the previously checked compact/complete-generation
passages support the imported interface; Section8.6 retains its stated
Galois scope. No Git/network/API, helper spawning, finite sweep or pending
CAS result was used. Interpreter: `/opt/anaconda3/bin/python`.

## Exact accepted contract

Input is an explicit integral basis and multiplication table for the MAXIMAL
order of an arbitrary number field L/Q, of growing degree n, and a binary
rational a. Maximality and the field representation are promises, not an
unproved conversion from any supplied polynomial/order. There is no supplied
normal closure, auxiliary field, class group, unit basis or solution.

For a!=0, return NO or a polynomial-size compact power product x in L*
with N_(L/Q)(x)=a, with correctness probability at least1-eta. Handle a=0
and n=1 directly. Time and description sizes are polynomial in the
stated explicit input parameters and log(1/eta), under GRH for the number
fields needed by the class-generator bound. The witness may have enormous
expanded coordinates; neither integrality nor small height is promised.

## Native input to paid finite support

1. The paired relative norm from each factor E of L tensor_Q L is an exact
   norm-one element of L, with its sign preserved. Ordinary ideal classes
   suffice; there is no narrow-class or positivity requirement.

2. At every prime outside the ramified support, unramified tensor factors
   supply the primitive integer divisor relation

       s_ij=(f_j/g_ij)e_i-(f_i/g_ij)e_j.

   The new Bezout proof in the main note is correct. With g=gcd_i f_i,
   h_i=f_i/g and sum_i b_i h_i=1, its double sum is

       sum_(i,j) b_i z_j(h_i e_j-h_j e_i)
         = z - (sum_j h_j z_j) sum_i b_i e_i = z.

   Moreover h_i e_j-h_j e_i=-(g_ij/g)s_ij, an INTEGER multiple. Thus all
   primitive pairs generate the full integral kernel, not a finite-index
   replacement. A fixed-star or unprimitive shortcut is not being used.

3. Principalizing the finitely supported fractional divisor in each tensor
   factor changes it only over S. Its paired norm removes the chosen
   outside-S divisor without changing the target rational norm. These
   elements depend on an existing solution only in the PROOF; the algorithm
   never requests them. No Hasse norm principle or local-to-global shortcut
   is assumed.

4. The trace-form tensor identity gives |disc(O_L tensor O_L)|=D^(2n).
   The index/discriminant formula then bounds every |disc E| by D^(2n).
   This pays the class-generation hypothesis with all rational primes up
   to the explicit integer cutoff 48*max(1,2n*bit_length(D))^2, together
   with primes dividing D and a. The cutoff is polynomial NUMERICALLY.
   Its logarithmic notation conceals no exponential enumeration.

5. No E, its maximal order, its class group, its embeddings or a Galois
   closure is computed. The proof-only discriminant bound therefore
   discharges the earlier support review's auxiliary-field construction
   concern. The source-backed48 bound is used as written. GRH is required
   for the auxiliary fields' class-generator theorem even though the
   algorithm does not construct those fields.

6. Checked/capped factoring supplies the primes dividing D and a. The
   explicit maximal-order table supports finite-algebra prime decomposition
   at every listed p, including ramified primes. At most n ideals occur
   over each p and log Norm(P)<=n log p. No invalid Dedekind power-basis
   assumption or residue-field enumeration enters the S-unit input.

## Complete compact units to exact norm image

The invoked S-unit result must return a COMPLETE generating basis/list
on its success event. Independence alone cannot justify NO. The source's
adjustable complete-generation event, deterministic lattice extraction and
exact compact recovery are the relevant interfaces; all sizes and clocks
are capped. Only the S-unit group of L is computed, not that of any E.

A free generating set modulo roots of unity plus the known element -1
has the full ABSOLUTE rational norm image. Other roots of unity have
norm+1, while N(-1)=(-1)^n. This is specific to a rational target and
does not silently supply torsion handling for arbitrary relative norms.

Norms of the small explicit compact atoms are exact multiplication
determinants of polynomial-bit matrices. A gcd-free basis of all their
rational numerators/denominators and of a yields faithful integer norm
coordinates, with a separate sign coordinate modulo2. Pairwise coprime
bases>1 suffice; primality, atom-norm factoring and expanded powers are
unnecessary. Factors outside S are retained until they cancel. The
compact/classical review supplies the polynomial gcd-free construction.

Adding the sign equation sigma*z-2t=sign(a) makes this an ordinary integer
linear system. Polynomial-bit HNF/SNF applies without saturation or a
mod2 reduction of finite rows. Polynomial-size solution exponents are
not an extra promise: choose a nonzero maximal minor Delta; nonpivot
coefficients can be reduced modulo |Delta| and pivot coefficients adjusted
integrally using its adjugate. Hadamard/Cramer bounds then give polynomial
binary lengths in the matrix and target data. Standard transformed integer
linear algebra computes such a solution.

Multiplying the compact generators to these binary exponents still gives
a polynomial-size signed power product. An independent deterministic
gcd-free norm computation verifies N(x)=a without expanding x or trusting
S-unit valuation metadata. Thus every positively accepted witness has an
exact classical certificate. On the complete-basis event, an insoluble
integer system is NO by the proved support theorem. Outside that event
NO is not certified; the theorem correctly retains bounded error.

## Error, scope and disposition

The eta/2 complete-S-unit failure budget and aggregate eta/2 budget for
capped checked factoring/finite-field randomized work sum to eta. All
norm-coordinate arithmetic, integer image solving and witness verification
are deterministic polynomial-bit operations. No voting on noncanonical
bases or implicit retry-until-success clock is needed.

The matched classical counterpart is this SAME support reduction with
classical S-unit arithmetic; the final image calculation is already
classical. The inspected BS Section8.6 restricts its direct composition
to Galois extensions, but that does not certify novelty of the tensor
support theorem. The original Simon2002 priority question remains open
in this review. Pending finite controls are falsifiers only and were not
used to infer any asymptotic claim.

One source-label correction was reported to the parent: the main Sources
paragraph's "Theorem8.6" should say "Section8.6". This is citation wording,
not a mathematical gate.

Disposition CLOSED: accept the explicit-maximal-order, GRH-conditional,
compact rational-field norm endpoint. Do not extend this acceptance to
integral/short solutions, arbitrary polynomial input preprocessing,
unconditional class generation, generic rational points, novelty,
classical hardness, practical efficiency or a quantum execution claim.
